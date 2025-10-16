# Introduction To Nosql Databases (1080P60) - Part 1

![Screenshot at 00:00:00](notes_screenshots/refined_Introduction_to_NoSQL_databases-(1080p60)_screenshots/frame_00-00-00.jpg)

# Introduction to NoSQL Databases

This lecture introduces NoSQL databases, discussing their applications, popularity, and fundamental differences from traditional SQL (Relational Database Management Systems - RDBMS).

## When to Use NoSQL Databases

It's crucial to understand when NoSQL databases are appropriate and when they are not. While NoSQL databases are often associated with scalability, it's a misconception that they are *always* required for large-scale applications or that RDBMS are only suitable for "toy apps." Both database types have specific scenarios where they excel.

### Scenarios Where NoSQL is NOT Always Used (Even at Scale)

Many popular, high-traffic applications successfully operate without NoSQL databases, indicating that NoSQL is not a universal solution for all scaling needs:

*   **YouTube**
*   **Stack Overflow**
*   **Instagram**

## SQL vs. NoSQL: Data Storage Comparison

The core difference between SQL and NoSQL databases lies in their data modeling and storage mechanisms.

### SQL (Relational) Data Model

![Screenshot at 00:01:34](notes_screenshots/refined_Introduction_to_NoSQL_databases-(1080p60)_screenshots/frame_00-01-34.jpg)

In SQL databases, data is organized into structured tables with predefined schemas. Relationships between different pieces of information are established using foreign keys.

Consider a `Person` entity with `ID`, `Name`, `Address`, `Age`, and `Role`. If `Address` is a complex object, it would typically be stored in a separate table to maintain data normalization.

*   **`Person` Table Example:**
    | ID  | Name      | Address_ID | Age | Role |
    | --- | --------- | ---------- | --- | ---- |
    | 123 | John Doe  | 23         | 30  | SDE  |

*   **`Address` Table Example:**
    | Address_ID | City    | Country | District |
    | ---------- | ------- | ------- | -------- |
    | 23         | Munich  | Germany | -        |

*   **Key Characteristics:**
    *   **Normalization:** Data is broken down into separate, related tables to reduce redundancy.
    *   **Foreign Keys:** Used to link records across different tables (e.g., `Address_ID` in `Person` table links to `Address` table).
    *   **Structured Schema:** Columns and their data types are predefined.
    *   **Joins:** Retrieving complete information often requires joining multiple tables, which can be computationally intensive.

### NoSQL (Document) Data Model

![Screenshot at 00:00:09](notes_screenshots/refined_Introduction_to_NoSQL_databases-(1080p60)_screenshots/frame_00-00-09.jpg)

NoSQL databases, particularly document databases (like MongoDB, which is often associated with this model), store data in flexible, schema-less formats, often using JSON-like documents. Related data is frequently embedded within a single document, reducing the need for joins.

For the same `Person` entity, all information, including the address, would be stored within a single document:

*   **Document Example (JSON):**
    ```json
    {
      "id": 123,
      "name": "John Doe",
      "address": {
        "id": 23,
        "city": "Munich",
        "country": "Germany"
        // "district" is omitted because it's null
      },
      "age": 30,
      "role": "SDE"
    }
    ```

*   **Key Characteristics:**
    *   **Denormalization:** Related data is often embedded directly within the main document.
    *   **No Foreign Keys:** Relationships are implicit through nested objects rather than explicit foreign key constraints.
    *   **Flexible Schema:** Documents in the same collection can have different structures. New fields can be added easily without altering a global schema.
    *   **Self-Contained:** A single document usually contains all necessary information for an entity.

### Comparison Table: SQL vs. NoSQL Data Representation

| Feature             | SQL (Relational)                               | NoSQL (Document)                                  |
| :------------------ | :--------------------------------------------- | :------------------------------------------------ |
| **Data Structure**  | Tables, Rows, Columns                          | Documents (JSON-like), Key-Value pairs, Graphs    |
| **Schema**          | Predefined, rigid                              | Dynamic, flexible, schema-less                    |
| **Relationships**   | Explicit Foreign Keys, Joins                   | Embedded documents, implicit relationships        |
| **Address Example** | Separate `Person` and `Address` tables linked  | `Address` embedded as an object within `Person` document |
| **Null Values**     | Stored as `NULL` in columns                    | Fields with null values often omitted             |

![Screenshot at 00:02:49](notes_screenshots/refined_Introduction_to_NoSQL_databases-(1080p60)_screenshots/frame_00-02-49.jpg)

## Why NoSQL Can Be Efficient

The efficiency of NoSQL databases, especially document-oriented ones, stems primarily from their data storage approach, which aligns well with common application access patterns.

*   **Data Locality:** When a user registers or updates their profile, all their information (name, address, age, role) is typically provided and inserted together. In a NoSQL document model, this entire "blob" of data can be written or read as a single unit.
*   **Reduced Joins:** Since related data is often stored together in one document, retrieving all information about a user usually requires only a single read operation on that document. This eliminates the need for complex and resource-intensive `JOIN` operations that are common in SQL databases when fetching data from multiple normalized tables.
*   **Common Query Patterns:** Many applications frequently need to retrieve *all* information about an entity (e.g., `SELECT *` from a user table). NoSQL's denormalized, document-centric approach makes these "select all" operations extremely fast because the data is physically co-located.
*   **Simplified API Interaction:** When data arrives from an API request (e.g., a user submission), it often comes as a single JSON object. This structure maps directly to a NoSQL document, simplifying the insertion process.

In essence, NoSQL's efficiency for certain use cases comes from optimizing for frequent, full-document reads and writes, reducing the overhead associated with managing relational integrity and distributed data across multiple tables.

---

### Efficiency of NoSQL (Continued)

The efficiency of NoSQL databases, particularly for document-oriented types, is further highlighted by common data access patterns:

*   **`SELECT *` Equivalence:** In many applications, users frequently need to retrieve all relevant data for a specific entity (e.g., all details for a user profile). This is analogous to a `SELECT *` query in SQL. In NoSQL, because all related data is typically contained within a single document, such operations are highly efficient, often requiring just one read operation to fetch the entire "blob" of data.
*   **Avoidance of Joins:** SQL databases, due to their normalized structure, often require `JOIN` operations to combine data from multiple tables (e.g., `Person` and `Address` tables). These joins can be computationally expensive. NoSQL's denormalized, embedded document model eliminates the need for joins in many scenarios, making data retrieval faster and simpler.

![Screenshot at 00:03:08](notes_screenshots/refined_Introduction_to_NoSQL_databases-(1080p60)_screenshots/frame_00-03-08.jpg)

## Advantages of NoSQL Databases

NoSQL databases offer several key advantages that make them suitable for specific use cases:

### 1. Data Locality and Efficient Retrieval

*   **Co-located Data:** All relevant data for an entity (e.g., a user's name, address, age, role) is stored together in a single document or "blob."
*   **Faster Insertions and Retrievals:** When data is inserted or retrieved, the entire document can be processed as a unit. This is highly efficient for applications where all data related to an entity is frequently accessed together.
*   **Reduced Overhead:** Unlike SQL databases that might need to traverse multiple tables via foreign keys (which can be expensive), NoSQL retrieves data from a single location.

### 2. Flexible Schema

![Screenshot at 00:03:19](notes_screenshots/refined_Introduction_to_NoSQL_databases-(1080p60)_screenshots/frame_00-03-19.jpg)

NoSQL databases are often referred to as "schema-less" or having a flexible schema, which provides significant benefits for development and evolution.

*   **Dynamic Structure:** The schema is not rigidly defined upfront. Documents within the same collection can have different fields.
*   **Handling Missing Data:** If a particular field (e.g., `district`) is null or not applicable for a specific record, it can simply be omitted from the document, saving storage space and simplifying the data model. In SQL, a column would still exist, potentially storing `NULL` values.
*   **Easy Attribute Addition:** Adding new attributes (e.g., `salary`) to data records is straightforward.
    *   **SQL Challenge:** In SQL, adding a new column to a large table is an expensive and risky operation. It typically requires locking the table, which can impact availability, and careful management to maintain data consistency.
    *   **NoSQL Simplicity:** In NoSQL, new fields can be added to individual documents as needed without affecting existing documents or requiring a schema migration. The database simply stores the new field if it's present in a document.

### 3. Horizontal Partitioning (Sharding)

![Screenshot at 00:03:53](notes_screenshots/refined_Introduction_to_NoSQL_databases-(1080p60)_screenshots/frame_00-03-53.jpg)

NoSQL databases are typically designed with scalability in mind, often featuring built-in support for horizontal partitioning, also known as sharding.

*   **Built for Scale:** They anticipate high volumes of data and user traffic.
*   **Distributed Data:** Data is automatically distributed across multiple servers or nodes (shards). This allows for scaling out by adding more machines, rather than scaling up by increasing resources on a single machine.
*   **Focus on Availability:** Horizontal partitioning inherently improves availability, as the failure of one node does not necessarily bring down the entire system. This aligns with the CAP theorem's emphasis on Availability over strong Consistency in distributed systems. (For more details on sharding, refer to resources on horizontal partitioning).

### 4. Built for Aggregations

NoSQL databases are well-suited for analytical queries and extracting insights from large datasets.

*   **Metric-Oriented:** They are designed to facilitate aggregations like calculating average age, total salary, or other metrics.
*   **Intelligent Data Retrieval:** The way data is stored (often denormalized) can be optimized for specific analytical queries, making it efficient to derive "intelligent data" or business insights.

## Disadvantages of NoSQL Databases

While NoSQL offers many advantages, it also comes with certain trade-offs, particularly concerning data consistency and update operations.

*   **Limited Update Support:** NoSQL databases are generally not ideal for applications requiring frequent, complex updates to individual fields across many documents. Updates can be less efficient compared to SQL, especially if they involve modifying nested structures.
*   **Potential for Inconsistency:** Due to their distributed nature and emphasis on availability (often favoring eventual consistency over strong immediate consistency), NoSQL databases can sometimes lead to data inconsistency.
    *   **Scenario:** It's possible for two different nodes in a distributed NoSQL system to temporarily hold different versions of data for the same ID. This means that a read operation might return stale data depending on which node is queried.
    *   **Trade-off:** This is a fundamental trade-off in distributed systems (CAP theorem), where achieving high availability and partition tolerance often comes at the cost of immediate strong consistency.

![Screenshot at 00:04:16](notes_screenshots/refined_Introduction_to_NoSQL_databases-(1080p60)_screenshots/frame_00-04-16.jpg)

---

### Disadvantages of NoSQL Databases (Continued)

*   **Consistency Issues (Lack of ACID Properties):**
    *   SQL databases typically guarantee **ACID properties** (Atomicity, Consistency, Isolation, Durability), which are crucial for transactional integrity, especially in financial systems.
    *   NoSQL databases, particularly those designed for high availability and horizontal scaling, often do not fully guarantee ACID properties. This means that data consistency across distributed nodes can be a challenge.
    *   **Implication:** For applications requiring strong transactional consistency, such as financial systems, NoSQL is generally not suitable for core transaction processing.

![Screenshot at 00:06:55](notes_screenshots/refined_Introduction_to_NoSQL_databases-(1080p60)_screenshots/frame_00-06-55.jpg)

*   **Not Optimized for Certain Read Patterns:**
    *   While NoSQL is efficient for retrieving entire documents, it can be less efficient for queries that need to filter or aggregate specific fields across many documents without retrieving the entire document.
    *   **Example:** If you need to find the average age of all employees, a NoSQL database might have to read the *entire document* for each employee, extract the age, and then perform the aggregation. In SQL, this could potentially be optimized by directly accessing and scanning only the 'age' column, which might be stored contiguously. This can lead to comparatively slower read times for such specific, column-oriented queries.

![Screenshot at 00:07:21](notes_screenshots/refined_Introduction_to_NoSQL_databases-(1080p60)_screenshots/frame_00-07-21.jpg)

*   **No Implicit Relations:**
    *   **RDBMS:** The "R" in RDBMS stands for "Relational," implying that relationships between data are a core feature. Foreign key constraints explicitly define how tables are related (e.g., `Address_ID 23` in the `Person` table implicitly relates to the `Address` table's row with `Address_ID 23`). This allows the database to enforce referential integrity.
    *   **NoSQL:** In NoSQL, relationships are not implicit or enforced by the database. If you have separate "tables" (collections) for different types of data, there's no inherent mechanism to define or enforce a foreign key-like constraint. This means developers must manage relationships at the application level.

![Screenshot at 00:08:26](notes_screenshots/refined_Introduction_to_NoSQL_databases-(1080p60)_screenshots/frame_00-08-26.jpg)

*   **Hard Joins (Manual Joins):**
    *   **SQL:** SQL databases excel at complex join operations (e.g., `INNER JOIN`, `OUTER JOIN`, `LEFT JOIN`), which are performed efficiently by the database engine based on defined relationships.
    *   **NoSQL:** Joins in NoSQL are generally not natively supported by the database engine in the same way. If you need to combine data from two different "collections" (analogous to tables), you often have to perform these "joins" manually in your application code. This involves:
        1.  Retrieving data from one collection.
        2.  Extracting relevant keys.
        3.  Using those keys to query the second collection.
        4.  Manually merging the results in memory.
    *   **Complexity:** This manual process can be complex, error-prone, and less performant for large datasets compared to database-optimized SQL joins.

## When to Use NoSQL Databases (Summary)

Based on the advantages and disadvantages, NoSQL databases are best suited for scenarios where:

*   **Data is "Block-Oriented":** When an entity's data is naturally grouped together and frequently accessed as a whole (e.g., a user profile document).
*   **Few Updates, Many Reads/Writes:** Ideal for workloads with a high volume of insertions and retrievals, especially when entire documents are being written or read, but infrequent or simple updates.
*   **Write-Optimized Systems:** Good for systems where the primary concern is rapidly ingesting large amounts of data.
*   **Inherent Redundancy Desired:** Some NoSQL systems allow for controlled redundancy, which can improve read performance and availability.
*   **Aggregations and Analytics:** Excellent for applications that need to perform analytical queries and derive metrics from large datasets.
*   **High Scalability and Availability:** When horizontal scaling and high availability are paramount, and some level of eventual consistency is acceptable.
*   **Flexible/Evolving Schema:** When the data model is expected to change frequently, or different records may have varying structures.

**Conversely, NoSQL is generally less suitable for:**

*   Systems requiring strict ACID transactions (e.g., financial ledgers).
*   Applications with complex, multi-table join requirements.
*   Workloads with frequent, complex updates across different data points.

## Introduction to Cassandra Architecture

To understand NoSQL databases in detail, we will examine Apache Cassandra as an example. Cassandra is a distributed NoSQL database known for its high availability and scalability.

![Screenshot at 00:09:57](notes_screenshots/refined_Introduction_to_NoSQL_databases-(1080p60)_screenshots/frame_00-09-57.jpg)

### Cassandra Cluster Overview

*   **Distributed System:** A Cassandra cluster consists of multiple nodes (servers) working together.
*   **High Cost:** Hosting and managing a Cassandra cluster can be an expensive undertaking due to the infrastructure requirements.
*   **Data Distribution:** Data (identified by `request IDs` or partition keys) is distributed across these nodes using a partitioning strategy.

### Data Partitioning in Cassandra

*   **Partitioning Scheme:** Cassandra uses a consistent hashing mechanism to distribute data. Each node is responsible for a specific range of "tokens" (hashes of partition keys).
*   **Example (Conceptual Range-based Partitioning):**
    *   If a cluster has 5 nodes, data might be distributed as follows:
        *   Node 1: Request IDs 0-99
        *   Node 2: Request IDs 100-199
        *   Node 3: Request IDs 200-299
        *   Node 4: Request IDs 300-399
        *   Node 5: Request IDs 400-499
*   **Request ID Mapping:** When a request with a specific `request ID` comes in, Cassandra determines which node is responsible for that ID based on its token range.
    *   **Example:** A `request ID = 123` would fall within the range 100-199, directing it to Node 2.

### Types of Request IDs (Partition Keys)

*   `Request IDs` are not limited to simple numeric values. They can be:
    *   **UUIDs (Universally Unique Identifiers):** Common for ensuring uniqueness across distributed systems.
    *   **Strings:** Such as a person's name, email, or any other unique identifier.
    *   **Composite Keys:** Combinations of multiple columns.

*   **NoSQL "IDs" vs. Relational IDs:** In NoSQL databases, the concept of an "ID" is often generalized to a "partition key" or "primary key" that determines where the data resides in the distributed system. This is different from a simple auto-incrementing integer ID in a relational database.

![Screenshot at 00:11:02](notes_screenshots/refined_Introduction_to_NoSQL_databases-(1080p60)_screenshots/frame_00-11-02.jpg)

---

### Data Partitioning in Cassandra (Continued)

*   **Hashing the Request ID:**
    *   To determine which node a `request ID` (or partition key) belongs to, the ID is first passed through a **hash function**.
    *   This hash function converts the `request ID` (which could be a number, string, UUID, etc.) into a numerical hash value.
    *   **Example:** `h(123) = 256` (where 256 is the resulting hash value).

![Screenshot at 00:11:15](notes_screenshots/refined_Introduction_to_NoSQL_databases-(1080p60)_screenshots/frame_00-11-15.jpg)

*   **Mapping Hash to Node:**
    *   The calculated hash value is then mapped to a node within the cluster.
    *   Cassandra typically uses a consistent hashing ring. If the hash value `256` falls within a node's assigned token range (e.g., 200-300 for Node 3), that node becomes the primary storage location.
    *   A common strategy in distributed hashing is to map the hash to the **next node in a clockwise direction** on the consistent hash ring if the hash doesn't fall exactly within a node's direct range. In the example, if 256 falls between 200 (Node 3) and 300 (Node 4), it might be assigned to Node 4.

![Screenshot at 00:11:38](notes_screenshots/refined_Introduction_to_NoSQL_databases-(1080p60)_screenshots/frame_00-11-38.jpg)

### Importance of a Good Hash Function

*   **Uniform Distribution:** A "nice" (uniformly distributed) hash function is critical for balanced load distribution across the cluster.
    *   If the hash function distributes `request IDs` evenly, then incoming requests will likely fall into different node ranges with equal probability.
    *   **Benefit:** This ensures that all nodes in the cluster receive approximately an equal share of the load (e.g., 20% each for a 5-node cluster), allowing them to operate at their full capacity without any single node becoming a bottleneck.

*   **Impact of a Bad Hash Function:**
    *   If the hash function is not uniform (e.g., `h(x) = 0` if `x < 100`, `h(x) = 1` if `x >= 100`), it can lead to severe load imbalance.
    *   **Example:** If most hash values map to Node 2, while other nodes (1, 3, 4, 5) remain largely idle, Node 2 will quickly become overloaded and crash. This effectively limits the entire cluster's capacity to that of a single overloaded node.

![Screenshot at 00:11:49](notes_screenshots/refined_Introduction_to_NoSQL_databases-(1080p60)_screenshots/frame_00-11-49.jpg)

### Multi-Level Sharding for Uneven Distribution

In scenarios where the primary hash function is problematic (e.g., cannot be changed, or data distribution is inherently skewed due to specific access patterns like geographical data during festivals), **multi-level sharding** can be employed.

*   **Concept:** Instead of storing data directly on the first-level node, that node acts as a gateway to a *secondary* cluster.
*   **Process:**
    1.  An initial request comes into the main cluster.
    2.  The primary hash function (H) directs the request to a specific node (e.g., Node 2).
    3.  Instead of storing data, Node 2 then applies a *different, more uniformly distributed hash function (H')* to the request's key.
    4.  This secondary hash (H') then directs the request to one of the nodes in a *secondary, smaller cluster* of nodes.
*   **Example: Google Maps during Diwali in India:**
    *   A primary hash might route all requests from "India" to a single node.
    *   During a festival like Diwali, this "India" node would experience extreme load.
    *   With multi-level sharding, the "India" node would then distribute these requests across a sub-cluster using a more granular hash function (e.g., based on city or region within India), balancing the load.
*   **Benefit:** This technique helps overcome limitations of a poor or skewed primary hash function by adding another layer of distribution. While more complex, it ensures better load balancing and prevents single points of failure due to data hot spots.

### Data Durability and Replication

A critical aspect of distributed databases like Cassandra is ensuring data durability and availability, even if nodes fail.

*   **Data Loss Prevention:** If a node responsible for storing data (e.g., Node 2) crashes, all data exclusively stored on that node would be lost. This is unacceptable for important data.
*   **Replication:** To prevent data loss and ensure high availability, Cassandra implements **replication**. This means that multiple copies (replicas) of each piece of data are stored on different nodes across the cluster.
*   **Replication Factor:** The number of copies made is determined by the `replication factor` configuration. If the replication factor is N, then N copies of each data item will exist on N different nodes.
*   **Benefit:** If one node fails, replicas of its data are still available on other nodes, allowing the cluster to continue operating without data loss or significant downtime.

![Screenshot at 00:12:23](notes_screenshots/refined_Introduction_to_NoSQL_databases-(1080p60)_screenshots/frame_00-12-23.jpg)

---

### Data Durability and Replication (Continued)

When a request is mapped to a primary node (e.g., Node 5 for `request ID 123` with hash `256`), Cassandra doesn't just store the data there. It also creates replicas on other nodes.

*   **Replica Placement:** Replicas are typically placed on subsequent nodes in the consistent hash ring (clockwise).
    *   **Example:** If a request falls on Node 5, and the replication factor is 3, then Node 5, Node 1, and Node 2 would store copies of that data. (Assuming clockwise placement, 5 -> 1 -> 2).
*   **Benefits of Replication:**
    *   **Data Guarantee (Redundancy):** If a primary node (e.g., Node 5) goes down, the data is not lost because copies exist on other nodes (e.g., Node 1 and Node 2). This significantly lowers the probability of data loss.
    *   **Read Optimization:** When a client makes a read query, it can be served by *any* of the nodes holding a replica of that data.
        *   **Example:** If data is replicated on Nodes 5, 1, and 2, a read request can be directed to any of these three nodes. This distributes the read load and improves read throughput.
        *   **Fault Tolerance for Reads:** If Node 5 is busy or down, the request can still be fulfilled by Node 1 or Node 2, ensuring high availability for read operations.
    *   **Write Optimization (Fault Tolerance):** Even during write operations, replication provides fault tolerance. If the primary node for a write (e.g., Node 5) fails to acknowledge the write, the write could potentially be completed on a replica node (e.g., Node 1), still achieving the desired replication factor and ensuring data persistence.

![Screenshot at 00:15:04](notes_screenshots/refined_Introduction_to_NoSQL_databases-(1080p60)_screenshots/frame_00-15-04.jpg)

## Distributed Consensus in NoSQL Databases

A crucial concept in distributed NoSQL databases like Cassandra is **distributed consensus**, especially given the eventual consistency model. This refers to how multiple nodes agree on the state of data, particularly when reads and writes are occurring concurrently or when nodes might have slightly different versions of data.

### The Problem: Inconsistent Reads

Consider a scenario with 5 nodes and a replication factor of 3 (e.g., data for `request ID 123` is on Nodes 5, 1, and 2).

1.  **Write Operation:** A user creates a profile, and the write operation is initiated on Node 5.
2.  **Replication Delay:** Nodes 1 and 2, which are supposed to receive replicas, might be momentarily slow or experiencing network issues, so they haven't yet received the updated data.
3.  **Primary Node Failure:** Node 5 (the coordinator for the write) crashes *before* Nodes 1 and 2 have fully replicated the new profile data.
4.  **Subsequent Read:** The user immediately tries to read their newly created profile. Since Node 5 is down, the read request is routed to one of the available replica nodes, say Node 1.
5.  **Inconsistent Result:** Node 1, not having received the latest update, reports "user not found" or an older version of the profile.

This leads to a confusing and frustrating user experience ("I just created my profile, why isn't it there?"). To prevent this, the database needs a mechanism to ensure that read operations return a consistent view of the data, or at least a graceful error.

![Screenshot at 00:16:00](notes_screenshots/refined_Introduction_to_NoSQL_databases-(1080p60)_screenshots/frame_00-16-00.jpg)

### Solution: Quorum

**Quorum** is a common mechanism used in distributed systems to achieve a desired level of consistency during read and write operations. It ensures that a sufficient number of nodes agree on the data's state before acknowledging an operation.

*   **Definition:** Quorum dictates that a certain minimum number of replica nodes must respond to a read or write request for the operation to be considered successful.
*   **Purpose:** It helps achieve a balance between consistency, availability, and performance in a distributed environment.

**How Quorum Works (Simplified):**

Let's assume a replication factor of `N=3` (data on Nodes 5, 1, 2) in a 5-node cluster.

*   **Write Quorum (W):** When a write request comes in, the coordinator node (e.g., Node 5) sends the write to all N replicas. For the write to be considered successful, at least `W` nodes must acknowledge the write.
*   **Read Quorum (R):** When a read request comes in, the coordinator sends the read request to all N replicas. For the read to be considered successful, at least `R` nodes must respond with data. The coordinator then typically returns the data with the latest timestamp (version ID) among the `R` responses.

**Example Scenario with Quorum:**

1.  **Read Request:** User requests their profile. Nodes 5, 1, and 2 hold replicas.
2.  **Node 5 crashes.**
3.  **Coordinator Routes to Replicas:** The read request is sent to Nodes 1 and 2.
4.  **Responses:**
    *   **Case A (Consistent):** Node 1 says "I don't have this profile yet," but Node 2 responds with the latest version of the profile (perhaps because it received the write just before Node 5 crashed). The coordinator picks the latest timestamped data from Node 2 and returns it to the user. The user is happy.
    *   **Case B (Inconsistent - Requires Error):** Both Node 1 and Node 2 respond, but *neither* has the user's profile, or they both have an outdated version, and no quorum is met for a successful read of the *latest* data. In this situation, the database should return a "database error" to the application (rather than "user not found"). This signals to the application that there's a temporary inconsistency or issue, prompting the application to inform the user to "wait for some time."

![Screenshot at 00:18:04](notes_screenshots/refined_Introduction_to_NoSQL_databases-(1080p60)_screenshots/frame_00-18-04.jpg)
![Screenshot at 00:18:26](notes_screenshots/refined_Introduction_to_NoSQL_databases-(1080p60)_screenshots/frame_00-18-26.jpg)

**Quorum Formula:**

A common setting to ensure **strong consistency** (where a read always returns the most recently written value) is to set `R + W > N`.
*   If `N=3` (replication factor):
    *   `W=2` (two nodes must confirm write)
    *   `R=2` (two nodes must confirm read)
    *   `R + W = 2 + 2 = 4`, which is greater than `N=3`. This ensures that there's always an overlap between the nodes that confirmed the write and the nodes that are queried for the read, guaranteeing the latest data.

Quorum is a fundamental concept for managing consistency in distributed NoSQL systems, allowing them to provide different consistency levels (from eventual to strong) based on application requirements.

---

### Quorum and Consistency Trade-offs

The choice of quorum values (`R` for reads, `W` for writes) directly impacts the consistency level of the database.

*   **Quorum of 2 with Replication Factor 3 (N=3, R=2, W=2):**
    *   This configuration means that for a read or write operation to succeed, at least two out of the three replica nodes must respond.
    *   **Scenario (Optimistic):** If Node 5 (primary) crashes, and Node 1 doesn't have the latest write, but Node 2 does (and has a newer timestamp), then the system can still return the correct, latest data to the user. This is an optimistic scenario where the system successfully recovers and provides the correct information.
    *   **Scenario (Pessimistic - Rare):** If Node 5 crashes *and* both Node 1 and Node 2 *have not* yet replicated the latest write (or both return outdated data), then the quorum of 2 for a read of the latest data cannot be met. In this case, the system would ideally return a database error (e.g., "unavailable for this request") rather than incorrect or outdated information.
    *   **Risk Acceptance:** This scenario, where multiple nodes fail or are inconsistent simultaneously during a critical window, is considered rare. NoSQL databases often accept this small risk to prioritize availability and performance over strict, immediate consistency. This aligns with the concept of **eventual consistency**.

*   **Quorum of 3 with Replication Factor 3 (N=3, R=3, W=3):**
    *   This configuration demands that *all three* replica nodes must respond and agree on a value for an operation to succeed.
    *   **Strong Consistency:** This provides strong consistency, where a read is guaranteed to return the latest committed write.
    *   **Impact on Availability:** If even one node (e.g., Node 5) fails or becomes unresponsive, a read or write operation requiring a quorum of 3 will *fail*. This prioritizes consistency over availability.
    *   **Example:** If Node 5 crashes, and a read request needs responses from 3 nodes, the request will fail because Node 5 cannot respond. The user would receive an error indicating unavailability.

![Screenshot at 00:18:48](notes_screenshots/refined_Introduction_to_NoSQL_databases-(1080p60)_screenshots/frame_00-18-48.jpg)
![Screenshot at 00:18:57](notes_screenshots/refined_Introduction_to_NoSQL_databases-(1080p60)_screenshots/frame_00-18-57.jpg)

### Distributed Consensus Mechanism

To manage quorum and consistency, distributed databases like Cassandra often employ a coordinator node or a more complex consensus protocol.

*   **Coordinator Role:** When a read or write request is received, a coordinator node (often the node that received the client's request) is responsible for:
    1.  Determining the set of replica nodes for the data.
    2.  Sending the request to these replicas.
    3.  Collecting responses from the replicas.
    4.  Evaluating if the quorum is met (e.g., counting votes, checking timestamps).
    5.  Returning the agreed-upon value (e.g., the one with the latest timestamp) or an error if quorum fails.
*   **Decentralized vs. Centralized Consensus:** While the explanation mentions a "central server" (like Node 3) for counting votes, many distributed NoSQL databases (including Cassandra) are designed to be masterless. The coordinator role is dynamic, and nodes communicate peer-to-peer to achieve consensus. More advanced distributed consensus protocols (like Paxos or Raft) are used for critical operations in such systems, which are typically covered in dedicated system design discussions.

## Cassandra's Data Storage and Write Mechanism

Beyond partitioning and replication, Cassandra (and other NoSQL databases like Elasticsearch) stands out in its fundamental approach to data storage and writing. This design is optimized for high write throughput and scalability.

### Append-Only Writes and Immutability

Cassandra employs an append-only, log-structured storage approach. Instead of updating data in place on disk, it primarily appends new data.

1.  **Memtable (In-Memory Buffer):** When a write request comes in, Cassandra first writes the data to an in-memory buffer called a **Memtable**. This is a highly efficient operation as it's purely in-memory.
2.  **Commit Log:** Simultaneously, the data is written to a **Commit Log** on disk. This log is append-only and provides durability. If the node crashes before the Memtable is flushed to disk, the Commit Log can be replayed to recover the data.
3.  **Memtable Flush to SSTable:** When the Memtable reaches a certain size or after a defined time interval, it is flushed to disk as an **SSTable (Sorted String Table)**. SSTables are immutable, sorted files on disk.
4.  **No In-Place Updates:** Instead of directly modifying existing SSTables, any updates or deletions generate *new* entries in the Memtable and then new SSTables. When data is updated, a new version is written. When data is deleted, a "tombstone" marker is written.
5.  **Compaction:** Over time, multiple SSTables containing different versions of the same data or tombstones are merged and compacted into new, consolidated SSTables. This process cleans up old versions and deleted data, improving read performance and reclaiming disk space.

### Benefits of this Write-Optimized Approach:

*   **High Write Throughput:** Writing to an in-memory Memtable and an append-only Commit Log is very fast, allowing Cassandra to handle a massive number of write operations per second.
*   **Durability:** The Commit Log ensures that data is durable even in the event of a sudden node crash.
*   **Sequential I/O:** Appending to the Commit Log and flushing Memtables as new SSTables primarily involves sequential disk writes, which are significantly faster than random writes.
*   **Eventual Consistency:** This architecture naturally lends itself to eventual consistency, where newly written data might take a short time to propagate and become visible across all replicas.

![Screenshot at 00:20:56](notes_screenshots/refined_Introduction_to_NoSQL_databases-(1080p60)_screenshots/frame_00-20-56.jpg)

---

### Cassandra's Write Path and Storage Mechanism

Cassandra's unique approach to storing and writing data is a key factor in its performance and scalability. This mechanism is shared by other NoSQL databases and is heavily inspired by Google's Bigtable data structure.

1.  **Memtable (In-Memory Write Buffer):**
    *   When a write request (key-value pair) arrives at a Cassandra node, the data is first written to an in-memory data structure called a **Memtable**.
    *   This is an efficient operation because it's a memory-based write, not a disk write.
    *   The Memtable acts like a temporary, in-memory table where new data records are accumulated.

2.  **Commit Log (Durability):**
    *   Simultaneously with writing to the Memtable, the data is also appended to a **Commit Log** on disk.
    *   The Commit Log is an append-only sequential file. This ensures data durability: if the node crashes before the Memtable contents are permanently saved, the Commit Log can be replayed during recovery to reconstruct the Memtable and prevent data loss.
    *   Writing to a sequential log file is significantly faster than random disk writes.

![Screenshot at 00:21:40](notes_screenshots/refined_Introduction_to_NoSQL_databases-(1080p60)_screenshots/frame_00-21-40.jpg)

3.  **SSTable (Sorted String Table - Persistent Storage):**
    *   Once the Memtable reaches a predefined size or after a certain time interval, its contents are flushed to disk as an **SSTable (Sorted String Table)**.
    *   **Sorted:** The data within an SSTable is sorted by key. This property is crucial for efficient lookups and range scans.
    *   **Persistent:** SSTables represent the persistent storage of data on the cluster nodes.
    *   **Immutable:** A fundamental characteristic of SSTables is that they are **immutable**. Once an SSTable is written to disk, it cannot be changed.
        *   This means that updates or deletions to existing data do not modify old SSTables. Instead, new data (with a newer timestamp) is written to the Memtable, which will eventually be flushed to a *new* SSTable.
        *   Deletions are handled by writing a special marker called a "tombstone" to a new SSTable.

![Screenshot at 00:22:44](notes_screenshots/refined_Introduction_to_NoSQL_databases-(1080p60)_screenshots/frame_00-22-44.jpg)

### Handling Updates and Duplicate Keys

Because SSTables are immutable, updates to existing keys result in multiple versions of the same key existing across different SSTables.

*   **Multiple Records for Same Key:** If a key `123` is initially written to `SSTable A`, and then later updated (e.g., changing "John Doe" to "John A. Doe"), the updated record for `123` will be written to `SSTable B` (after being in the Memtable and flushed).
*   **Timestamp-Based Resolution:** To resolve which version of a key is the "correct" one, Cassandra uses **timestamps**. Each record has an associated timestamp. When reading, Cassandra retrieves all versions of a key and returns the one with the latest timestamp.
*   **Storage Overhead:** The main challenge with multiple versions of the same key across different immutable SSTables is the increased storage consumption. Having 10 records for the same key means using 10 times the storage space for that key's data until old versions are cleaned up.

![Screenshot at 00:23:05](notes_screenshots/refined_Introduction_to_NoSQL_databases-(1080p60)_screenshots/frame_00-23-05.jpg)

### Compaction: Optimizing Storage and Read Performance

To address the issue of storage overhead and improve read performance, Cassandra and similar databases (like Elasticsearch) use a background process called **compaction**.

*   **Purpose:** Compaction merges multiple SSTables into new, consolidated SSTables.
*   **Process (Merge Sort Analogy):** Compaction is analogous to a merge sort algorithm. It takes two or more sorted SSTables (which are like sorted arrays) and merges them into a single new, sorted SSTable.
*   **Conflict Resolution:** During compaction, if multiple versions of the same key are encountered, only the record with the latest timestamp is kept, and older versions (and tombstones) are discarded. This cleans up obsolete data.
*   **Efficiency:** Compaction is an efficient operation, often `O(N)` for merging two sorted lists of total size `N`. The space complexity is also optimized (e.g., `O(min(M,N))` for merging two lists of size `M` and `N`).
*   **Benefits:**
    *   **Reduced Storage Space:** Eliminates duplicate and outdated records, reclaiming disk space.
    *   **Improved Read Performance:** Reduces the number of SSTables that need to be scanned when querying for a key, as the latest data is consolidated.
    *   **Background Process:** Compaction runs as a background process, minimizing impact on foreground read/write operations.

![Screenshot at 00:24:51](notes_screenshots/refined_Introduction_to_NoSQL_databases-(1080p60)_screenshots/frame_00-24-51.jpg)

### Summary of Cassandra's Storage Advantages:

*   **Fast Writes:** Immutable SSTables are quickly flushed to disk from memory.
*   **Durability:** Ensured by the Commit Log.
*   **Scalability:** The architecture is designed for distributed storage and high write throughput.
*   **Eventual Consistency:** Achieved through timestamp-based conflict resolution and background compaction.
*   **Read Optimization (Post-Compaction):** Efficient lookups due to sorted keys in SSTables and reduced number of files after compaction.

---

### Compaction: Handling Deleted Records (Tombstones)

Compaction is also essential for garbage collecting deleted records in an immutable storage system.

*   **Tombstones:** When a record is "deleted" in Cassandra (or other similar systems), it's not immediately removed from disk. Instead, a special marker called a **tombstone** is written.
    *   This tombstone is essentially a record with the key and a special flag indicating that the record is deleted, along with a timestamp.
    *   Like any other write, a tombstone is written to the Memtable and eventually flushed to an SSTable.
*   **Deletion During Reads:** When a read operation occurs, if the system encounters a tombstone with the latest timestamp for a particular key, it understands that the record is "dead" and should not be returned to the user.
*   **Deletion During Compaction:** During the compaction process, when multiple SSTables are merged:
    *   If a tombstone is the latest version for a key, all older versions of that key across other SSTables are permanently removed (garbage collected). The tombstone itself is also eventually removed after a configurable grace period, ensuring that deleted data is eventually purged from the system.
*   **Handling Updates on Deleted Records:** If an attempt is made to update a key for which a tombstone is the latest record, the system will typically throw an exception or error indicating that the record does not exist. This prevents "resurrecting" deleted data unintentionally.

![Screenshot at 00:25:12](notes_screenshots/refined_Introduction_to_NoSQL_databases-(1080p60)_screenshots/frame_00-25-12.jpg)
![Screenshot at 00:25:57](notes_screenshots/refined_Introduction_to_NoSQL_databases-(1080p60)_screenshots/frame_00-25-57.jpg)

## Conclusion: NoSQL Database Principles

The concepts discussed using Cassandra as an example (distributed architecture, consistent hashing, replication, quorum, Memtables, Commit Logs, SSTables, and compaction) are fundamental to many NoSQL databases.

*   **Extensibility:** These principles are not unique to Cassandra but are extensible to other NoSQL databases and distributed systems, including:
    *   **Elasticsearch:** Uses similar inverted index structures, immutable segments (like SSTables), and compaction.
    *   **Amazon DynamoDB:** A highly scalable, fully managed NoSQL database service that implements many of these distributed system design patterns.

Understanding these underlying mechanisms provides a solid foundation for comprehending how modern, highly scalable, and available data stores operate. The trade-offs between consistency and availability (as managed by quorum settings) and the optimization for write throughput through log-structured merge-trees (LSM-trees, which SSTables are a component of) are central to the design philosophy of many NoSQL solutions.

---

