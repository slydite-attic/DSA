# Whatsapp System Design： Chat Messaging Systems For Interviews (1080P25) - Part 1

# Designing WhatsApp: A Chat-Based Application

This video provides a guide to designing WhatsApp, a chat-based application. The principles discussed can be largely applied to designing any similar chat system.

## Key Features of WhatsApp

WhatsApp distinguishes itself with two primary features:
*   **Group Messaging:** Allows multiple users to communicate within a single chat.
*   **Read Receipts:** Indicates when a message has been seen by the recipient(s).

These are often key discussion points in system design interviews.

## System Design Interview Strategy

When approaching a system design interview for a chat application, it's crucial to:
1.  **Start Simple:** Begin with foundational features you are comfortable with.
2.  **Prioritize Known Areas:** The first feature you propose is often accepted by the interviewer, so choose one you understand well.
3.  **Manage Scope:** Select features that can be realistically discussed and designed within the allotted interview time (e.g., one hour).

## Core Features to Consider

The following features are important for a comprehensive chat application design. As shown in the screenshot below, these are often listed as key requirements.

![Screenshot at 00:02:40](notes_screenshots/refined_WHATSAPP_System_Design：_Chat_Messaging_Systems_for_Interviews-(1080p25)_screenshots/frame_00-02-40.jpg)

1.  **Group Messaging:**
    *   Allows multiple participants (e.g., WhatsApp groups can have up to 200 people).
    *   Requires robust handling of message distribution to all group members.
2.  **Image/Video Sharing:**
    *   A common and expected feature in modern chat applications.
    *   (Note: The storage and retrieval of images/videos has been covered in a separate "Tinder video" on this channel, which can serve as a reference).
3.  **Sent, Delivered, and Read Receipts:**
    *   Indicated by visual cues (e.g., tick marks) that show the status of a message.
    *   `Sent`: Message successfully sent from the sender's device.
    *   `Delivered`: Message successfully received by the recipient's device.
    *   `Read`: Message has been viewed by the recipient.
4.  **Online Status / Last Seen:**
    *   Indicates if a user is currently active or the last time they were seen on the platform.
    *   This feature is not critical to core messaging but is an engineering consideration for user experience.
5.  **Temporary vs. Permanent Chats:**
    *   **Temporary Chats (e.g., WhatsApp, Snapchat):**
        *   **Privacy:** Provides users with more control over their data, aligning with privacy expectations.
        *   **Storage Efficiency:** Messages are primarily stored on user devices, saving server-side storage space.
        *   **Implication:** If the application is deleted by both sender and receiver, chat history may be permanently lost.
    *   **Permanent Chats (e.g., Office Messaging Applications):**
        *   **Compliance & Official Communication:** Essential for retaining records for legal or business compliance.
        *   **Server-Side Storage:** Messages are stored indefinitely on servers for archival purposes.

## Initial Design Focus: One-to-One Chat

Before delving into complex features like group messaging, the fundamental requirement of **one-to-one chat** must be established. This forms the basis for all other communication functionalities.

## Foundational System Design Concepts

The design will leverage several core system design concepts, details of which can be found in a dedicated system design playlist:
*   **Load Balancing:** Distributing network traffic efficiently across multiple servers.
*   **Messaging Queues:** Decoupling services and ensuring reliable message delivery.
*   **Single Point of Failure (SPOF):** Designing systems to avoid any single component whose failure would bring down the entire system. These are crucial considerations for a robust application like WhatsApp.

---

## One-to-One Chat Architecture

This section details the architecture for one-to-one messaging, focusing on how a message travels from sender to receiver.

### 1. Client Connection via Gateway

![Screenshot at 00:03:35](notes_screenshots/refined_WHATSAPP_System_Design：_Chat_Messaging_Systems_for_Interviews-(1080p25)_screenshots/frame_00-03-35.jpg)

*   **Client Application:** The WhatsApp application installed on a user's mobile phone initiates a connection to the WhatsApp cloud infrastructure.
*   **Gateway Service:** This is the entry point for client connections.
    *   **External Protocol:** Clients (e.g., User A) communicate with the Gateway using an external protocol (e.g., TCP/IP with custom application-layer protocols designed for chat). This protocol often prioritizes security, authentication, and efficient message framing for external communication.
    *   **Internal Protocol:** The Gateway might communicate with internal WhatsApp services using a different, more lightweight internal protocol.
        *   **Reasoning:** Internal communication often doesn't require the same level of security overhead (e.g., large HTTP headers) as external client-server interactions, as security mechanisms are often handled at the Gateway level. This optimizes performance and resource usage within the internal network.
    *   **Microservice:** The Gateway itself is a microservice, often deployed with multiple instances to ensure high availability and prevent single points of failure.

### 2. Initial Message Flow (Problematic Approach)

Consider User A sending a message to User B.

![Screenshot at 00:04:33](notes_screenshots/refined_WHATSAPP_System_Design：_Chat_Messaging_Systems_for_Interviews-(1080p25)_screenshots/frame_00-04-33.jpg)

*   **User-to-Gateway Mapping (Inefficient):**
    *   An initial thought might be for each Gateway instance to store information about which users are connected to it (e.g., "User B is connected to Gateway 2").
    *   This would involve a `User ID` to `Gateway Box ID` mapping maintained directly by the Gateway.
*   **Drawbacks of Gateway-Managed Connections:**
    1.  **Memory Consumption:** Maintaining active TCP connections consumes memory on the Gateway servers. Storing additional mapping information directly on these servers further increases memory usage, limiting the maximum number of connections a single Gateway can handle.
    2.  **Duplication and Inconsistency:** This connection mapping information would either be:
        *   Duplicated across multiple Gateway instances (leading to potential inconsistencies).
        *   Managed by a caching mechanism or a dedicated database (which introduces complexity).
    3.  **Transient Data & High Update Rate:** Connection status is highly transient (users frequently connect/disconnect). Storing this volatile information on Gateways would lead to a high rate of updates, impacting performance and consistency.
    4.  **Tight Coupling:** This design creates tight coupling between the Gateway's primary function (handling client connections) and the routing logic (knowing where users are connected).

### 3. Decoupling with a Sessions Microservice (Improved Approach)

To address the drawbacks, the responsibility of managing user-to-Gateway mappings is decoupled into a dedicated **Sessions Microservice**.

![Screenshot at 00:04:44](notes_screenshots/refined_WHATSAPP_System_Design：_Chat_Messaging_Systems_for_Interviews-(1080p25)_screenshots/frame_00-04-44.jpg)

*   **Dumb Gateway Connections:**
    *   The TCP connection at the Gateway becomes "dumb" – its sole purpose is to receive and transmit data. It doesn't need to know the routing logic or where specific users are connected.
    *   This allows Gateways to maximize concurrent connections and reduce their internal state.
*   **Sessions Microservice Role:**
    *   This microservice is responsible for storing and providing information on "who is connected to which Gateway box."
    *   It acts as an indirect router, determining the correct Gateway for a recipient.
    *   **High Availability:** Multiple instances of the Sessions Microservice are deployed to avoid a single point of failure.

### 4. Message Flow with Sessions Microservice

![Screenshot at 00:05:31](notes_screenshots/refined_WHATSAPP_System_Design：_Chat_Messaging_Systems_for_Interviews-(1080p25)_screenshots/frame_00-05-31.jpg)

Let's trace the message from User A to User B:

1.  **User A Sends Message:** User A's client sends a "send message" request to its connected Gateway (e.g., Gateway 1), including the recipient's User ID (User B).
2.  **Gateway 1 Forwards to Sessions Service:** Gateway 1, being "dumb," doesn't know where User B is. It forwards the "send message to User B" request to the Sessions Microservice.
3.  **Sessions Service Routes:** The Sessions Microservice looks up User B's current connection status:
    *   It determines which Gateway (e.g., Gateway 2) User B is currently connected to.
    *   It then instructs Gateway 2 to deliver the message to User B.
4.  **Gateway 2 Delivers to User B:** Gateway 2 receives the message from the Sessions Service and pushes it down the established TCP connection to User B's client.

### 5. Server-to-Client Communication Protocol

*   **Problem with HTTP:** Standard HTTP is a client-to-server request-response protocol. A server cannot initiate a message push to a client using traditional HTTP.
*   **Solution:** For the server (Gateway 2) to send a message to User B, a different communication mechanism is required, such as:
    *   **Persistent TCP Connections:** Keeping the TCP connection open allows the server to push data to the client.
    *   **WebSockets:** A full-duplex communication protocol over a single TCP connection, ideal for real-time applications like chat.
    *   **Long Polling:** A technique where the client makes a request and the server holds it open until new data is available or a timeout occurs.

This setup ensures efficient routing, scalability, and resilience by decoupling concerns and utilizing appropriate communication protocols.

---

### Real-time Server-to-Client Communication

To enable real-time message delivery from the server to the client (e.g., Gateway 2 sending a message to User B), traditional HTTP (a client-pull model) is insufficient.

*   **Inefficient Alternatives:**
    *   **Polling:** User B could repeatedly ask the Gateway (or Sessions service) for new messages every minute. This is not real-time and creates unnecessary network traffic.
*   **Real-time Solution: WebSockets**
    *   **Protocol:** WebSockets provide a full-duplex, persistent connection over TCP.
    *   **Peer-to-Peer Semantics:** Unlike HTTP's client-server model, WebSockets allow both client and server to initiate communication, enabling true "peer-to-peer" messaging flow from a functional perspective.
    *   **Benefit:** This allows the server (Gateway 2) to directly push messages to User B's client as soon as they are available, crucial for chat applications.

### Implementing Sent, Delivered, and Read Receipts

This section details the message flow for providing feedback to the sender about the status of their message.

![Screenshot at 00:07:28](notes_screenshots/refined_WHATSAPP_System_Design：_Chat_Messaging_Systems_for_Interviews-(1080p25)_screenshots/frame_00-07-28.jpg)

#### 1. Sent Receipt

*   **Message Persistence:** When User A sends a message to User B, and the message reaches the Sessions Microservice, it's crucial to first persist this message in a **chat database**.
    *   **Purpose:** This ensures the message is safely stored and guaranteed to be delivered, even if User B is offline initially. The system can retry delivery until User B receives it.
*   **Acknowledgement to Sender (User A):**
    *   Upon successful receipt and persistence by the Sessions Microservice, a parallel response is sent back to Gateway 1 (User A's connected gateway).
    *   Gateway 1 then sends a "sent" receipt (e.g., a single tick mark) back to User A's client. This confirms that the message has been successfully submitted to the system.

#### 2. Delivered Receipt

![Screenshot at 00:07:40](notes_screenshots/refined_WHATSAPP_System_Design：_Chat_Messaging_Systems_for_Interviews-(1080p25)_screenshots/frame_00-07-40.jpg)

*   **Message Delivery to Recipient (User B):** Once the Sessions Microservice routes the message to Gateway 2, and Gateway 2 successfully delivers the message to User B's client.
*   **Acknowledgement from Recipient (User B):**
    *   User B's client, upon receiving the message, sends an acknowledgement back to Gateway 2. This is essentially a TCP acknowledgement at the application level.
    *   Gateway 2 forwards this acknowledgement to the Sessions Microservice.
*   **Update and Notify Sender:**
    *   The Sessions Microservice receives the acknowledgement, which contains "to" (User B) and "from" (User A) fields.
    *   It updates the message status in the chat database to "delivered."
    *   It then finds User A's connected Gateway (Gateway 1) via its own mapping.
    *   Finally, it sends a "delivered" receipt (e.g., a double tick mark) to Gateway 1, which then forwards it to User A's client.

#### 3. Read Receipt

*   **User Action:** When User B opens the chat application and specifically views the chat tab containing the message.
*   **Client Initiates "Read" Event:** User B's client sends a "read" message (containing message ID, sender ID, etc.) to its connected Gateway (Gateway 2).
*   **Same Flow as Delivery Receipt:** This "read" message follows the exact same path as the delivery receipt:
    *   Gateway 2 forwards to Sessions Microservice.
    *   Sessions Microservice updates the message status to "read" in the database.
    *   Sessions Microservice finds User A's Gateway (Gateway 1).
    *   Sessions Microservice sends a "read" receipt (e.g., blue double tick marks) to Gateway 1, which then forwards it to User A's client.

### Online Status / Last Seen Feature

This feature indicates if a user is currently online or when they were last active. At a large scale with millions of users, this becomes complex, but a principled architectural approach can be taken.

*   **Basic Requirement:** User A wants to know if User B is online.

![Screenshot at 00:10:21](notes_screenshots/refined_WHATSAPP_System_Design：_Chat_Messaging_Systems_for_Interviews-(1080p25)_screenshots/frame_00-10-21.jpg)

![Screenshot at 00:10:45](notes_screenshots/refined_WHATSAPP_System_Design：_Chat_Messaging_Systems_for_Interviews-(1080p25)_screenshots/frame_00-10-45.jpg)

This is typically handled by having clients periodically send "heartbeat" signals to the Sessions service or a dedicated presence service. When a client connects or disconnects, the Sessions service updates the user's status. Other clients can then query this service to get the online/offline status or subscribe to real-time updates.

---

### Online Status / Last Seen Feature (Continued)

The "online status" and "last seen" feature provides information about a user's recent activity.

*   **Querying User Status:** When User B wants to know User A's status, User B's client queries the server (specifically, a dedicated service for this purpose) asking "When was A online last?".
*   **Data Storage:** This requires a persistent storage (e.g., a database table) that stores `User ID` to `Last Seen Timestamp` mappings.
    *   Example: `User A -> 2023-10-27 10:30:05`
*   **Maintaining Last Seen Timestamp:**
    *   Whenever a user performs an **activity** (e.g., sending a message, reading a message, opening the app, or any client-initiated request), the current timestamp should be persisted in this `Last Seen` table.
    *   This ensures the timestamp is updated with every meaningful interaction.

![Screenshot at 00:11:19](notes_screenshots/refined_WHATSAPP_System_Design：_Chat_Messaging_Systems_for_Interviews-(1080p25)_screenshots/frame_00-11-19.jpg)

*   **"Online" Threshold:**
    *   If a user's `Last Seen Timestamp` is very recent (e.g., within the last 3, 10, or 15 seconds, depending on the chosen threshold), they should be displayed as "online."
    *   If the `Last Seen Timestamp` is older than this threshold, the actual timestamp ("Last seen at...") should be displayed.
    *   This provides a better user experience than showing "Last seen 3 seconds ago" when the user is actively using the app.

#### Last Seen Microservice for User Activity Tracking

To manage the `Last Seen` timestamp efficiently and accurately, a dedicated **Last Seen Microservice** is introduced.

![Screenshot at 00:11:41](notes_screenshots/refined_WHATSAPP_System_Design：_Chat_Messaging_Systems_for_Interviews-(1080p25)_screenshots/frame_00-11-41.jpg)

*   **Trigger for Update:** Any user activity that sends a request to the Gateway should trigger an update to the `Last Seen` timestamp.
*   **Differentiating Request Types:**
    *   **User Activities:** These are actions directly initiated by the user (e.g., typing a message, opening a chat).
    *   **Application-Generated Requests (App Requests):** These are background processes initiated by the application itself, not direct user interaction (e.g., a delivery receipt acknowledgement, polling for messages while the app is in the background but not actively used by the human).
*   **Client-Side Intelligence:** The client application needs to be "smart" enough to flag requests:
    *   If a request is a **user activity**, it should be flagged as such. This flag tells the Gateway to forward the request details to the Last Seen Microservice.
    *   If a request is an **app request** (e.g., a delivery receipt), it should *not* be sent to the Last Seen Microservice, as it doesn't indicate active user presence.
*   **Flow:**
    1.  User performs an activity (e.g., sends a message).
    2.  Client sends request to Gateway, flagged as "user activity."
    3.  Gateway forwards this to the Last Seen Microservice.
    4.  Last Seen Microservice updates the `Last Seen Timestamp` for that user in its database.
    5.  When User B queries User A's status, it queries the Last Seen Microservice, which returns the timestamp, allowing the client to determine "online" or "last seen at X."

This approach ensures that the "online" status is accurately reflected based on actual user interaction, not just background app processes.

### Next Steps: Group Messaging

Having established the core one-to-one chat, sent/delivered/read receipts, and online status features, the next major feature to tackle is **Group Messaging**.

![Screenshot at 00:14:20](notes_screenshots/refined_WHATSAPP_System_Design：_Chat_Messaging_Systems_for_Interviews-(1080p25)_screenshots/frame_00-14-20.jpg)
![Screenshot at 00:14:42](notes_screenshots/refined_WHATSAPP_System_Design：_Chat_Messaging_Systems_for_Interviews-(1080p25)_screenshots/frame_00-14-42.jpg)

Group messaging introduces additional complexities related to message distribution, membership management, and maintaining state for multiple recipients.

---

## Supporting Services (Brief Mentions)

Before diving into group messaging, it's worth noting some additional services that are typically part of a comprehensive system but might be deferred in an interview context:

*   **Load Balancer:** Essential for distributing client requests across multiple Gateway instances. (Assumed as a foundational component).
*   **Service Discovery / Heartbeat Maintenance:** Crucial for microservice architectures to allow services to find each other and monitor health. (Will be covered in a separate video).
*   **Authentication Service:** Handles user login, registration, and session management. (Will be discussed later as a basic principle).
*   **Generic Services (Not WhatsApp Specific):**
    *   **Profile Service:** Manages user profile information.
    *   **Image Service:** Handles image storage and retrieval (already covered in a separate video).
    *   **Email Service:** For sending emails (e.g., password resets).
    *   **SMS Service:** For sending SMS messages (e.g., OTPs, notifications).

The core of a chat application remains **sending messages**.

## Group Messaging Architecture

Group messaging is a critical feature that builds upon the one-to-one chat foundation.

![Screenshot at 00:14:54](notes_screenshots/refined_WHATSAPP_System_Design：_Chat_Messaging_Systems_for_Interviews-(1080p25)_screenshots/frame_00-14-54.jpg)

### Problem with Sessions Service Storing Group Info

*   If the Sessions service were to store all group membership information (e.g., "Red Group has Users X, Y, Z, connected to Gateway 1, 2, 3 respectively"), it would become overly complex and tightly coupled with group management.
*   This information is separate from individual user connection status.

### Decoupling with a Group Service

To address this, group membership information is decoupled into a dedicated **Group Service**.

![Screenshot at 00:15:13](notes_screenshots/refined_WHATSAPP_System_Design：_Chat_Messaging_Systems_for_Interviews-(1080p25)_screenshots/frame_00-15-13.jpg)

*   **Group Service Role:** This microservice stores which users belong to which groups.
*   **Message Flow for Group Message:**
    1.  **Sender Initiates:** A user (e.g., a "red" user connected to Gateway 1) sends a group message.
    2.  **Gateway to Sessions:** Gateway 1 forwards the group message request to the Sessions Microservice.
    3.  **Sessions Queries Group Service:** The Sessions Microservice, upon receiving a group message, asks the **Group Service**: "Who are the other members in this group?"
    4.  **Group Service Responds:** The Group Service responds with a list of User IDs belonging to that group (e.g., "10 members with these user IDs").
    5.  **Sessions Routes to Individual Members:**
        *   The Sessions Microservice then uses its own database (which maps `User ID` to `Gateway Box ID`) to determine which Gateway each of the 10 group members is connected to.
        *   It then routes the message to each of these Gateway instances one by one.
        *   Each designated Gateway then pushes the message to its respective connected group member.

### Limiting Group Size

*   **Fan-out Problem:** Sending a message to a large group involves "fanning out" the request to many recipients. If a group has millions of members (like a celebrity post on Instagram), this becomes impractical for real-time delivery.
    *   For such large-scale fan-out, solutions like batch processing or client-side polling are typically used.
*   **Real-time Constraint in Chat:** For chat applications, real-time delivery is highly desired, making pull mechanisms less suitable for core messaging.
*   **WhatsApp's Approach:** WhatsApp limits group size (e.g., maximum 200 people).
    *   **Reason:** This limit makes it feasible to fan out messages to all group members in near real-time without overwhelming the system. 200 is a "very reasonable number" compared to millions.
    *   Other chat applications might set limits around 500-600.

This architecture ensures that group messages are efficiently distributed to all relevant members while managing the scalability challenges associated with large fan-outs.

---

## Group Messaging: Implementation Details

The core functionality of group messaging relies on the Sessions service querying the Group Service for member lists and then fanning out messages. This section delves into optimizing this process.

### 1. Optimizing Gateway Responsibilities

![Screenshot at 00:18:10](notes_screenshots/refined_WHATSAPP_System_Design：_Chat_Messaging_Systems_for_Interviews-(1080p25)_screenshots/frame_00-18-10.jpg)

Gateways are critical for maintaining expensive WebSocket connections with users. To prevent them from starving for memory and CPU, their responsibilities should be minimized.

*   **Reduce Memory Footprint:**
    *   **Delegating Session Management:** Separating the Sessions service from the Gateway significantly reduces the Gateway's memory load.
    *   **Avoid Message Parsing:** Gateways should not be responsible for parsing incoming messages (e.g., JSON messages over HTTP). Parsing involves converting raw data into programming language objects, which consumes CPU and memory.
    *   **Avoid Authentication:** Authentication checks should also be offloaded from the Gateway.
*   **"Dumb" Gateway Principle:** The Gateway's primary role is to maintain WebSocket connections and forward raw, unparsed messages.

### 2. Introducing a Parser Microservice

![Screenshot at 00:19:14](notes_screenshots/refined_WHATSAPP_System_Design：_Chat_Messaging_Systems_for_Interviews-(1080p25)_screenshots/frame_00-19-14.jpg)

To handle message parsing without burdening the Gateway, a dedicated **Parser Microservice** is introduced.

*   **Functionality:**
    *   The Gateway receives an "unparsed" message (raw bytes).
    *   Instead of parsing it, the Gateway forwards this unparsed message to the Parser Microservice.
    *   The Parser Microservice converts the raw message into a structured, sensible programming language object.
    *   This object can then be routed to the correct downstream service (e.g., Sessions service, Group service).
*   **Internal Protocol:** This parsed message could use an efficient internal protocol like Thrift (used by Facebook) instead of HTTP, further optimizing internal communication.
*   **Benefits:**
    *   **Reduced Gateway Load:** Gateways perform minimal work, focusing solely on connection management.
    *   **Centralized Parsing Logic:** Parsing logic is isolated, making it easier to manage and scale.
    *   **Memory Efficiency:** Reduces memory footprint on the Gateways.

### 3. Efficient Group-to-User Mapping with Consistent Hashing

![Screenshot at 00:20:07](notes_screenshots/refined_WHATSAPP_System_Design：_Chat_Messaging_Systems_for_Interviews-(1080p25)_screenshots/frame_00-20-07.jpg)

The Group Service needs an efficient way to store and retrieve the `Group ID` to `User ID` (one-to-many) mapping.

*   **Challenge:** Storing this information across multiple Group Service instances (for high availability and scalability) without duplication and ensuring efficient lookups is crucial.
*   **Solution: Consistent Hashing**
    *   **Purpose:** Consistent hashing is a technique that helps distribute data (like group memberships) across multiple servers in a way that minimizes data movement when servers are added or removed.
    *   **Mechanism:** It allows routing requests for a specific `Group ID` to a specific Group Service instance that holds the membership information for that group.
    *   **Routing Key:** The `Group ID` is used as the key for consistent hashing.
    *   **Benefit:** This reduces memory footprint and duplication across Group Service instances by ensuring that a particular group's data resides on a specific server.

![Screenshot at 00:20:49](notes_screenshots/refined_WHATSAPP_System_Design：_Chat_Messaging_Systems_for_Interviews-(1080p25)_screenshots/frame_00-20-49.jpg)

*   **How it works (simplified):**
    1.  When a request for a `Group ID` comes to the Sessions service, it uses consistent hashing on the `Group ID` to determine which specific Group Service instance holds the membership data for that group.
    2.  The Sessions service then queries that particular Group Service instance.
    3.  The Group Service instance returns the list of User IDs for that group.
    4.  The Sessions service then proceeds to fan out the message to each user's Gateway.

### 4. Handling Failures in Group Service

*   **Resilience:** The system must be resilient to failures of the Group Service instances.
*   **Retry Mechanisms:** If a message intended for a Group Service instance fails to be processed (e.g., the instance is down), the system should implement retry mechanisms.
*   **Idempotency:** Messages sent to the Group Service (e.g., for adding/removing members, or querying group info) should ideally be **idempotent**. This means that performing the operation multiple times has the same effect as performing it once, preventing data inconsistencies in case of retries.
    *   (Note: The diagram shows "Retry + Idempotent" associated with the threads processing messages, implying that operations handled by downstream services, including the Group Service, should support these properties.)

This structured approach ensures that group messaging is robust, scalable, and efficient, even with a limited group size, by intelligently distributing responsibilities and leveraging techniques like consistent hashing.

---

## Group Messaging: Reliability and Optimizations

Ensuring reliability and performance in group messaging, especially under heavy load, requires specific architectural considerations.

### 1. Ensuring Message Delivery with Message Queues

![Screenshot at 00:21:44](notes_screenshots/refined_WHATSAPP_System_Design：_Chat_Messaging_Systems_for_Interviews-(1080p25)_screenshots/frame_00-21-44.jpg)

*   **Challenge:** If a Group Service instance (or any downstream service) fails, or a user is offline, how do we guarantee message delivery?
*   **Solution: Message Queues**
    *   **Mechanism:** Message queues (e.g., Kafka, RabbitMQ) are robust systems that ensure messages are eventually delivered. Once a message is placed in a queue, the queue takes responsibility for its delivery.
    *   **Configurable Options:**
        *   **Delivery Time:** Messages can be delivered immediately or after a configurable delay.
        *   **Retries:** Message queues can be configured to retry delivery multiple times (e.g., 5 retries) if the initial attempts fail.
        *   **Failure Notification:** If all retries fail, the message queue can notify the upstream service (and ultimately the client) about the delivery failure.
    *   **Benefit:** This decouples the sending and receiving components, making the system more resilient to transient failures and ensuring "at-least-once" delivery semantics.

### 2. Group Receipts (Delivered/Read)

*   **Cost of Group Receipts:** Providing "delivered" or "read" receipts for group messages is significantly more expensive than for one-to-one chats.
    *   **Reason:** Every member of the group needs to acknowledge receipt/read status, and this information then needs to be aggregated and sent back to the sender. This generates a large volume of network traffic and processing load.
*   **Common Practice:** Many chat applications (including WhatsApp to some extent for group read receipts) do not implement full group-level delivered/read receipts due to this high cost. It's an acceptable trade-off for scalability.

### 3. Idempotency and Ordering

![Screenshot at 00:21:53](notes_screenshots/refined_WHATSAPP_System_Design：_Chat_Messaging_Systems_for_Interviews-(1080p25)_screenshots/frame_00-21-53.jpg)

*   **Idempotency:** Operations should be idempotent, meaning performing them multiple times has the same effect as performing them once. This is crucial when retries are in place (e.g., via message queues) to prevent duplicate processing or inconsistent state.
*   **Ordering:** Maintaining the correct order of messages is also vital for chat applications. (This is a complex topic often handled with sequence numbers or timestamps, and careful design of message queues).

These principles contribute to a resilient and well-performing chat system.

### 4. System Resiliency and Performance Under Load

![Screenshot at 00:23:08](notes_screenshots/refined_WHATSAPP_System_Design：_Chat_Messaging_Systems_for_Interviews-(1080p25)_screenshots/frame_00-23-08.jpg)

![Screenshot at 00:23:17](notes_screenshots/refined_WHATSAPP_System_Design：_Chat_Messaging_Systems_for_Interviews-(1080p25)_screenshots/frame_00-23-17.jpg)

*   **Context:** Under extreme load conditions (e.g., New Year's Eve, major festivals like Diwali), chat systems experience a massive surge in messages.
*   **Mitigation Strategy: Message Prioritization (Deprioritization)**
    *   **Concept:** Instead of dropping messages entirely or letting the system crash, critical messages are prioritized, and less critical messages are deprioritized.
    *   **Examples of Deprioritization:**
        *   **Last Seen Updates:** The `Last Seen` feature can be temporarily ignored or updated less frequently. The system can function without real-time `Last Seen` updates.
        *   **Delivered/Read Receipts:** These are less critical than the actual message delivery. The system can choose to delay or skip sending these receipts during peak load.
        *   **Core Message Delivery:** The highest priority is given to ensuring the message is sent from the sender and received by the server (the initial "sent" receipt).
    *   **Benefits:**
        *   **System Health:** Prevents the system from crashing under extreme load.
        *   **Continued Functionality:** Allows core messaging to continue, albeit with some degraded functionality for non-critical features.
        *   **User Experience:** Users still get their messages delivered, which is the most important aspect, even if secondary features are delayed or temporarily unavailable.

This intelligent prioritization, often combined with rate limiting, ensures the system remains operational and provides acceptable performance during traffic spikes. This concludes the discussion on designing group messaging, which was requirement number one for the WhatsApp design.

---

## Conclusion of WhatsApp System Design

This concludes the comprehensive system design discussion for WhatsApp, covering key features like one-to-one chat, group messaging, read receipts, and online status.

### Summary of Key Architectural Components and Principles

![Screenshot at 00:24:50](notes_screenshots/refined_WHATSAPP_System_Design：_Chat_Messaging_Systems_for_Interviews-(1080p25)_screenshots/frame_00-24-50.jpg)

The system design relies on a microservice architecture to ensure scalability, reliability, and maintainability.

*   **Client Applications:** Users interact with the system via their mobile applications, maintaining persistent WebSocket connections.
*   **Gateways:**
    *   Act as the entry point for client connections.
    *   Maintain "dumb" WebSocket connections, primarily forwarding raw, unparsed messages.
    *   Offload heavy processing to other services to maximize connection capacity.
*   **Parser Microservice:**
    *   Receives unparsed messages from Gateways.
    *   Converts raw messages into structured objects for internal processing.
    *   Uses efficient internal protocols like Thrift.
*   **Sessions Microservice:**
    *   Manages user connection status (which user is connected to which Gateway).
    *   Stores `User ID` to `Gateway Box` mapping.
    *   Routes messages to the correct Gateway for one-to-one chats.
    *   Interacts with the Group Service for group message routing.
*   **Group Service:**
    *   Manages group membership information (`Group ID` to `User IDs` mapping).
    *   Leverages **Consistent Hashing** on `Group ID` to distribute group data efficiently across its instances, reducing duplication and improving lookup performance.
    *   Limits group size (e.g., 200 members in WhatsApp) to manage the fan-out problem for real-time delivery.
*   **Last Seen Microservice:**
    *   Tracks user activity to provide "online" or "last seen" status.
    *   Clients intelligently flag user-initiated activities versus app-generated requests.
*   **Chat Database:** Persistently stores messages to guarantee delivery and maintain chat history.
*   **Message Queues:**
    *   Used for asynchronous communication and ensuring reliable message delivery (e.g., to offline users or between services).
    *   Supports configurable retries and failure propagation.
*   **Other Supporting Services:** Load Balancer, Authentication Service, Profile Service, Image Service, Email Service, SMS Service.
*   **Core Principles:**
    *   **Decoupling:** Breaking down the system into independent microservices to manage complexity and enable scalability.
    *   **Resilience:** Implementing retry mechanisms and idempotency to handle failures gracefully.
    *   **Message Prioritization:** During peak loads, deprioritizing less critical features (like `Last Seen` updates or non-essential receipts) to maintain core messaging functionality and system health.

This robust architecture allows WhatsApp to handle a massive scale of real-time communication while providing a rich set of features.

---

