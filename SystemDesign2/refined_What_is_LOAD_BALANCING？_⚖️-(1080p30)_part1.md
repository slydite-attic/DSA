# What Is Load Balancing？ ⚖️ (1080P30) - Part 1

# Consistent Hashing

![Screenshot at 00:00:00](notes_screenshots/refined_What_is_LOAD_BALANCING？_⚖️-(1080p30)_screenshots/frame_00-00-00.jpg)

Consistent Hashing is a critical concept for building scalable systems. It addresses the challenge of efficiently distributing data or requests across a dynamic set of servers.

## Understanding Scalable Systems

To grasp the importance of consistent hashing, it's essential to understand what "scaling" in system design means.

### The Basic System - A Single Server

Imagine a single computer running an algorithm, which can be thought of as a **server**. A server is a program or device that provides functionality for other programs or devices, called "clients."

![Screenshot at 00:01:06](notes_screenshots/refined_What_is_LOAD_BALANCING？_⚖️-(1080p30)_screenshots/frame_00-01-06.jpg)

*   **Client-Server Interaction:**
    *   A client (e.g., a mobile phone) sends a **request** to the server.
    *   The server processes the request using its algorithm (e.g., a facial recognition algorithm that adds a mustache to an image).
    *   The server then sends a **response** back to the client (e.g., the modified image).

![Screenshot at 00:01:32](notes_screenshots/refined_What_is_LOAD_BALANCING？_⚖️-(1080p30)_screenshots/frame_00-01-32.jpg)

### The Challenge of Growth (Scaling)

Initially, a single server might handle requests efficiently. However, if the service becomes popular, thousands of requests can overwhelm a single computer. This is where the need for **scaling** arises.

*   **Scaling Up:** Increasing the resources (CPU, RAM, storage) of a single server. This has limits.
*   **Scaling Out:** Adding more servers to handle the increased load. This is often the preferred method for large-scale systems.

## Introducing Multiple Servers and Load Balancing

When demand outstrips the capacity of a single server, the solution is to add more servers to form a distributed system.

![Screenshot at 00:03:18](notes_screenshots/refined_What_is_LOAD_BALANCING？_⚖️-(1080p30)_screenshots/frame_00-03-18.jpg)

*   **The Problem:** With multiple servers (say, `N` servers), a new challenge emerges: how to decide which server should handle an incoming request?
*   **The Goal:** The primary objective is to **balance the load** evenly across all available servers. Each server has a "load" representing the processing work it needs to do for incoming requests. Distributing this load evenly ensures no single server becomes a bottleneck and that system resources are utilized efficiently.

![Screenshot at 00:03:58](notes_screenshots/refined_What_is_LOAD_BALANCING？_⚖️-(1080p30)_screenshots/frame_00-03-58.jpg)

*   **Load Balancing Definition:** The process of distributing network traffic evenly across multiple servers. This ensures maximum server availability, optimal performance, and prevents overloading any single server.

## Role of Consistent Hashing

Consistent hashing is a technique designed to help achieve effective load balancing, particularly in scenarios where servers are frequently added or removed.

*   **Objective:** To evenly distribute the "weight" (requests) across all `N` servers.
*   **Request Identification:** Each incoming request is typically associated with a `request ID`. This ID is often a uniformly random number within a defined range (e.g., from `0` to `M-1`). Consistent hashing uses this ID (or a hash derived from it) to map the request to a specific server.

---

### Simple Hashing for Load Balancing

A straightforward approach to distributing requests among `N` servers involves using a hash function on the request ID.

![Screenshot at 00:04:27](notes_screenshots/refined_What_is_LOAD_BALANCING？_⚖️-(1080p30)_screenshots/frame_00-04-27.jpg)

1.  **Request ID:** Each incoming request is assigned a unique `request ID`, typically a number ranging from `0` to `M-1`.
2.  **Hashing:** This `request ID` (let's call it `R`) is passed through a hash function, `h(R)`, which produces a numerical output.
3.  **Modulo Operation:** The hash output is then subjected to a modulo operation with the total number of servers, `N`. The result, `h(R) % N`, gives an index that corresponds to a specific server (`S0` to `SN-1`).

![Screenshot at 00:04:56](notes_screenshots/refined_What_is_LOAD_BALANCING？_⚖️-(1080p30)_screenshots/frame_00-04-56.jpg)

*   **Formula:** `Server_Index = h(Request_ID) % N`

![Screenshot at 00:06:10](notes_screenshots/refined_What_is_LOAD_BALANCING？_⚖️-(1080p30)_screenshots/frame_00-06-10.jpg)

*   **Example with N=4 servers (S0, S1, S2, S3):**
    *   If `h(R1)` results in `10`, then `10 % 4 = 2`. Request R1 is sent to server S2.
    *   If `h(R2)` results in `15`, then `15 % 4 = 3`. Request R2 is sent to server S3.
    *   If `h(R3)` results in `12`, then `12 % 4 = 0`. Request R3 is sent to server S0.

*   **Expected Distribution:** Assuming the `request ID`s are uniformly random and the hash function `h()` distributes values uniformly, this method is expected to distribute the load (`X` requests) evenly across `N` servers. Each server would ideally handle `X/N` requests, resulting in a load factor of `1/N` per server.

### The Problem with Changing Server Count (N)

The simple `hash(Request_ID) % N` method works well as long as the number of servers, `N`, remains constant. However, in dynamic, scalable systems, `N` often changes (e.g., adding new servers due to increased traffic or removing faulty ones).

*   **Impact of N Change:** When `N` changes to `N_new` (e.g., adding S4, so `N` becomes `5`), the modulo operation `h(Request_ID) % N_new` will produce different results for most `request ID`s.

*   **Example (N=4 to N=5):**
    *   **Original (N=4):**
        *   `h(R1) = 10` -> `10 % 4 = 2` (R1 goes to S2)
        *   `h(R2) = 15` -> `15 % 4 = 3` (R2 goes to S3)
        *   `h(R3) = 12` -> `12 % 4 = 0` (R3 goes to S0)
    *   **New (N=5, after adding S4):**
        *   `h(R1) = 10` -> `10 % 5 = 0` (R1 now goes to S0, *changed*)
        *   `h(R2) = 15` -> `15 % 5 = 0` (R2 now goes to S0, *changed*)
        *   `h(R3) = 12` -> `12 % 5 = 2` (R3 now goes to S2, *changed*)

*   **Massive Remapping:** As demonstrated, a change in `N` causes nearly all request-to-server mappings to become invalid. This necessitates re-calculating the server for almost every existing request and, more critically, re-distributing any data associated with those requests.

### Analogy: The Pie Diagram

![Screenshot at 00:07:39](notes_screenshots/refined_What_is_LOAD_BALANCING？_⚖️-(1080p30)_screenshots/frame_00-07-39.jpg)

Consider the total range of `request ID`s as a pie.

*   **Initial State (N=4 servers):** The pie is divided into 4 equal slices, with each server responsible for 25% of the `request ID`s (e.g., if there are 100 possible IDs, each server gets 25 IDs).

![Screenshot at 00:08:23](notes_screenshots/refined_What_is_LOAD_BALANCING？_⚖️-(1080p30)_screenshots/frame_00-08-23.jpg)

*   **Adding a Server (N=5 servers):** When a fifth server (S4) is added, the entire pie must be re-divided into 5 equal slices. Now, each server is responsible for 20% of the `request ID`s.
    *   This change means that a significant portion of the `request ID`s previously assigned to S0, S1, S2, and S3 must now be re-assigned to other servers, including the new S4, to maintain an even 20% distribution.
    *   For example, if a server previously handled IDs 0-24, it now needs to handle a new range (e.g., 0-19 or a non-contiguous set if the hash function changes significantly). This "churn" in assignments is highly inefficient, as it requires moving data or invalidating caches for a large percentage of items.

This drastic remapping is the fundamental problem that consistent hashing aims to solve by minimizing the number of items that need to be remapped when servers are added or removed.
</REFINEDNOTES>

---

### High Cost of Re-allocation with Simple Hashing

When using the simple `hash(Request_ID) % N` method, adding or removing a server (changing `N`) results in a complete re-evaluation of almost all request-to-server mappings.

![Screenshot at 00:09:23](notes_screenshots/refined_What_is_LOAD_BALANCING？_⚖️-(1080p30)_screenshots/frame_00-09-23.jpg)

*   **Example Continuation (N=4 to N=5):**
    *   Initially, with 4 servers (S0, S1, S2, S3), each server was responsible for 25% of the total `Request ID` range.
    *   When a fifth server (S4) is added, the ideal distribution becomes 20% per server.
    *   This means each of the original 4 servers must shed 5% of its assigned `Request ID`s, and the new server (S4) takes on 20%.
    *   The speaker illustrates this with a pie chart where sections are re-distributed.
    *   The "cost of change" refers to the number of `Request ID`s that are now mapped to a different server than before. In the simple modulo hashing, if `M` is the total range of `Request ID`s, then almost all `M` mappings must change. The sum of changes across all servers often equals `M`, meaning the entire system state (in terms of where requests are routed) is disrupted.

![Screenshot at 00:10:02](notes_screenshots/refined_What_is_LOAD_BALANCING？_⚖️-(1080p30)_screenshots/frame_00-10-02.jpg)

### Why Extensive Remapping is Problematic

The high cost of remapping is a significant issue in distributed systems due to the nature of `Request ID`s and the importance of caching.

![Screenshot at 00:11:19](notes_screenshots/refined_What_is_LOAD_BALANCING？_⚖️-(1080p30)_screenshots/frame_00-11-19.jpg)

*   **Non-Random Request IDs:** In practice, `Request ID`s are rarely purely random. They often encode or are directly derived from user-specific information, such as a `User ID`.
    *   For example, if a user named "Gorab" makes requests, hashing "Gorab" will consistently yield the same hash value.
    *   With `h(User_ID) % N`, this means "Gorab" will always be routed to the same server, say S2, as long as `N` remains constant.

*   **Leveraging Locality with Caching:**
    *   This consistent routing allows servers to cache user-specific data (e.g., user profiles, session information) locally.
    *   If "Gorab" repeatedly accesses their profile, S2 can store it in its local cache, avoiding repeated database lookups and significantly speeding up response times. This is a crucial optimization for performance.

![Screenshot at 00:11:31](notes_screenshots/refined_What_is_LOAD_BALANCING？_⚖️-(1080p30)_screenshots/frame_00-11-31.jpg)

*   **Cache Invalidation on Server Changes:**
    *   When `N` changes (e.g., adding S4), the `h(User_ID) % N` calculation changes.
    *   Suddenly, "Gorab" might be routed to S0 instead of S2.
    *   The cache on S2 for "Gorab's" profile becomes useless, and S0 will have to fetch the profile from the database, effectively nullifying the benefit of the previous caching.
    *   Since almost all users' mappings can change, a massive amount of cached data across all servers becomes invalid, leading to a significant performance hit and increased load on the backend data stores.

### The Desired Outcome for Dynamic Systems

![Screenshot at 00:12:48](notes_screenshots/refined_What_is_LOAD_BALANCING？_⚖️-(1080p30)_screenshots/frame_00-12-48.jpg)

The goal for a scalable, dynamic system is to minimize the impact of adding or removing servers.

*   **Minimal Change:** When a new server is added, ideally only a small fraction of the `Request ID`s (or data items) should need to be remapped.
*   **Target Distribution:** If a new server is added, it should take its proportional share of the load (e.g., 20% if `N` goes from 4 to 5). This 20% should be taken incrementally from the existing servers, such that each existing server gives up only a small portion of its previously assigned `Request ID`s.
*   **Preserving Cache:** This approach ensures that most existing mappings remain intact, preserving the effectiveness of local caches and reducing the amount of data migration required.

This is precisely the problem that **Consistent Hashing** is designed to solve, offering an advanced approach to maintain stability and efficiency in dynamic server environments.

---

