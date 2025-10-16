# Monarch： Google'S Planet Scale In Memory Time Series Database (1080P25) - Part 1

# Google Monarch: A Time Series Data Store (2010)

![Screenshot at 00:00:01](notes_screenshots/refined_Monarch：_Google's_Planet-Scale_In-Memory_Time_Series_Database-(1080p25)_screenshots/frame_00-00-01.jpg)

## 1. Introduction to Monarch

Google Monarch is a time series data store, detailed in a 2010 paper. Its primary function is to store server-side metrics, such as CPU utilization, which can then be plotted as graphs over time. This allows engineers to monitor system performance, identify anomalies (e.g., spikes at a specific timestamp T1), and investigate issues.

## 2. Key Characteristics & Requirements

Monarch is designed to operate at Google's immense scale, necessitating specific capabilities:

*   **Scale of Data Ingestion:**
    *   **Rate:** 6 million data points per second.
    *   **Total Volume:** Petabytes of data.
    ![Screenshot at 00:00:59](notes_screenshots/refined_Monarch：_Google's_Planet-Scale_In-Memory_Time_Series_Database-(1080p25)_screenshots/frame_00-00-59.jpg)
*   **Low Latency:** Crucial for real-time metric tracking, requiring data access and processing in less than 100 milliseconds.
*   **Extremely High Availability:** Monarch is a critical system for Google's incident response. It cannot have hard dependencies on other core Google infrastructure services like Spanner or Colossus. If these systems fail, Monarch must remain operational to facilitate debugging and recovery.
    ![Screenshot at 00:01:23](notes_screenshots/refined_Monarch：_Google's_Planet-Scale_In-Memory_Time_Series_Database-(1080p25)_screenshots/frame_00-01-23.jpg)
    *   **Independence:** As shown in the diagram above, Monarch operates independently from other large Google systems (like Colossus and Spanner), ensuring it remains available even if those services experience outages.

## 3. The Problem: Pre-Monarch Monitoring (Borgmon)

Before Monarch, Google engineers faced significant challenges with their existing monitoring approach, primarily centered around a system called **Borgmon**.

*   **Borgmon Explained:**
    *   "Borgmon" stands for "Borg Monitor."
    *   It was a common library used by various server fleets across different Google services (e.g., Google Photos, Payments) to push metrics to their respective monitoring systems.
*   **Issues with Borgmon:**
    *   **Distributed Management:** Each team or service (e.g., Photos, Payments) deployed and managed its own instance of Borgmon on its servers.
    *   **Duplicate Work:** Multiple teams performed the same setup, configuration, and maintenance tasks for their individual Borgmon deployments, leading to wasted engineering time and resources.
    *   **Operational Burden:** If a team's Borgmon instance failed, they were responsible for managing and recovering it.
    *   **Complexity:** Using Borgmon required engineers to understand its internal workings, adding to the learning curve and operational overhead.
    ![Screenshot at 00:03:19](notes_screenshots/refined_Monarch：_Google's_Planet-Scale_In-Memory_Time_Series_Database-(1080p25)_screenshots/frame_00-03-19.jpg)
    *   **Inefficiency:** The decentralized nature of Borgmon resulted in inefficiencies, preventing Google from consolidating monitoring efforts and saving engineering costs.

## 4. The Solution: Centralizing with Monarch

To address the limitations of Borgmon, Google moved towards a centralized time series data store: Monarch.

*   **Centralized Approach:** Monarch serves as a common, company-wide time series data store where all various metrics are pushed.
*   **Simplified Usage:** Engineers no longer need to worry about the complexities of deploying and managing monitoring infrastructure. Instead, they interact with Monarch through **Monarch clients**, which periodically push data to the Monarch servers.
*   **Reduced Engineering Overhead:** This shift eliminated duplicate work, allowing engineers to focus on their core product development rather than monitoring system maintenance.

## 5. Initial Design Decision: In-Memory Data Store

An immediate design decision for Monarch was to implement it as an **in-memory data store**.

*   **Rationale:** To meet the extremely low latency requirements and handle petabytes of data that need to be accessed at any given point in time.
*   **Cost Implication:** While an in-memory system for petabytes of data is inherently expensive, the critical real-time monitoring and high availability requirements justified the cost.

---

## 6. Monarch Data Schema: Request Latency Monitoring

![Screenshot at 00:03:54](notes_screenshots/refined_Monarch：_Google's_Planet-Scale_In-Memory_Time_Series_Database-(1080p25)_screenshots/frame_00-03-54.jpg)

A crucial metric for system health is **request latency**. Servers emit events containing the time taken to process each request (e.g., 10ms, 5ms, 2ms).

*   **Traditional Visualization:** Plotting individual request latencies over time (time on X-axis, latency on Y-axis) can visually indicate anomalies.
    ![Screenshot at 00:04:39](notes_screenshots/refined_Monarch：_Google's_Planet-Scale_In-Memory_Time_Series_Database-(1080p25)_screenshots/frame_00-04-39.jpg)
    *   As seen in the graph above, a sudden spike (e.g., a request taking 90ms while others are low) is an anomaly.
*   **Monarch's Approach: Histograms for Latency Distribution:**
    *   Instead of raw latency points, Monarch generates **histograms** of request latencies for specific time windows.
    *   This makes anomaly detection and performance analysis significantly easier.
    *   **Example Histogram:**
        *   0-10 milliseconds: 8 requests
        *   11-20 milliseconds: 1 request (e.g., 16ms)
        *   81-90 milliseconds: 1 request (e.g., 81ms)
        ![Screenshot at 00:05:24](notes_screenshots/refined_Monarch：_Google's_Planet-Scale_In-Memory_Time_Series_Database-(1080p25)_screenshots/frame_00-05-24.jpg)
        *   This histogram clearly shows the distribution, making it easy to identify P99 (99th percentile) latencies and pinpoint anomalous ranges.
*   **Example Tracing for Anomalies:**
    *   Monarch stores **example requests** for each bin (window) in the histogram.
    *   For instance, it might store the trace ID of a request that took 16ms (in the 11-20ms bin) and another that took 81ms (in the 81-90ms bin).
    *   Engineers can use these trace IDs to "dig deeper" into the system and understand why a particular request experienced high latency.
*   **Time-Windowed Histograms:**
    *   Monarch stores a histogram for *every* time window.
    *   This allows engineers to analyze system performance within a single window or aggregate data across multiple histograms to observe trends over time.

## 7. Data Compression Techniques for In-Memory Storage

Storing billions of data points (petabytes) in memory is only feasible with aggressive compression. Google employs two main techniques:

### 7.1. Timestamp Sharing

*   **Problem:** Every metric and its corresponding histogram would typically have its own timestamp.
*   **Solution:** Monarch shares timestamps across all histograms generated for different metrics within the same time window.
    *   **Benefit 1: Storage Savings:** This results in approximately 90% savings when storing timestamp values.
        ![Screenshot at 00:06:20](notes_screenshots/refined_Monarch：_Google's_Planet-Scale_In-Memory_Time_Series_Database-(1080p25)_screenshots/frame_00-06-20.jpg)
        *   The diagram visually represents the significant reduction in storage needed for timestamps.
    *   **Benefit 2: Easier Interpolation and Joins:**
        *   Since different metrics (e.g., request latency and memory usage) share the same timestamps for a given window, it becomes much easier to correlate them.
        *   Engineers can readily analyze how one metric (e.g., request latency) reacts to changes in another (e.g., memory usage) because their data points are directly aligned by shared timestamps.

### 7.2. Delta Encoding for Time Series

*   **Observation:** In consecutive time windows, the values within histogram bins for a given metric are often very similar.
    *   **Example:** If a histogram for time window T1 has bin counts like `[8, 1, 1]`, the next histogram for T2 might have `[7, 2, 1]`.
*   **Solution:** Instead of storing the absolute counts for each bin in every histogram, Monarch stores the **differences (deltas)** between consecutive histograms.
    *   **Example:** For `[8, 1, 1]` followed by `[7, 2, 1]`, Monarch stores `[-1, +1, 0]`.
    *   **Benefit:** These delta values are typically smaller numbers, requiring fewer bits to store.
    *   **Impact:** This technique compresses each time series for every metric by approximately 90%.
*   **Overall Impact of Compression:** By applying these techniques, Monarch can store petabytes of data in memory, avoiding the need for exabytes of raw data and millions of expensive servers.

## 8. High-Level Architecture (Conceptual)

Monarch's high-level architecture is distributed hierarchically:

*   **Root Node:** A single global root node (conceptualized in blue).
*   **Zones:** Approximately 30-40 "zones" distributed worldwide. These act as child nodes to the root.
*   **Leaf Nodes:** Each zone contains a multitude of "leaf" nodes. (Details on leaf nodes will likely follow in the next section).

---

## 8. High-Level Architecture (Continued)

The Monarch architecture is hierarchical, similar to Google's Dremel, and designed for scalability and fault tolerance.

![Screenshot at 00:07:39](notes_screenshots/refined_Monarch：_Google's_Planet-Scale_In-Memory_Time_Series_Database-(1080p25)_screenshots/frame_00-07-39.jpg)

### 8.1. Architectural Components

*   **Root Node (Global):**
    *   There is typically only one root node globally.
    *   All incoming queries initially hit the root node.
    *   The root node is responsible for:
        *   Identifying which zones are relevant to an incoming query.
        *   Forwarding the query to the appropriate zones.
    *   It also contains an **Index** and a **Pre-computed Cache** for global query optimization.
*   **Zones (Regional):**
    *   Approximately 30-40 zones exist worldwide, acting as child nodes to the root.
    *   Each zone manages a cluster of leaf nodes within its geographical region.
    *   Like the root, each zone also has its own **Index** and **Pre-computed Cache** for local query handling.
*   **Leaf Nodes (Data Storage):**
    *   Each zone contains multiple leaf nodes.
    *   These nodes are where the actual data points (metrics) are stored.
    *   Leaf nodes are responsible for persisting data and serving queries for the data they hold.

### 8.2. Data Ingestion (Write Path)

1.  **Service Data Emission:** Services (e.g., servers tracking CPU consumption) emit data points (metrics) at regular intervals (e.g., every second).
2.  **Ingestion Server:** Data points are ingested into a dedicated server, which:
    *   Buffers the incoming data temporarily.
    *   Acts as a **router**.
3.  **Routing to Zones and Leaves:**
    *   The router determines the correct zone for the data.
    *   It then routes the data to the appropriate leaf node within that zone. This routing is based on a mapping of a "key" (presumably the metric identifier) to a specific leaf node.
    *   Data is then persisted on the designated leaf node.

### 8.3. Data Persistence and Fault Tolerance

*   **Colossus Integration:** Each leaf node is connected to **Colossus**, Google's distributed file store (the successor to Google File System or GFS).
*   **Log Storage:** Metrics are stored in Colossus, conceptually treated as log lines.
*   **Fault Tolerance:** If a leaf server crashes, it can retrieve its data from Colossus to rehydrate itself, ensuring data durability and system resilience.

### 8.4. Query Path

1.  **Query to Root:** All queries originate and hit the root node.
2.  **Root to Zones:** The root node uses its index to determine which zones are responsible for the requested data and forwards the query to those relevant zones.
3.  **Zones to Leaves:** Each zone then directs the query to the specific leaf nodes that contain the requested data.

![Screenshot at 00:08:30](notes_screenshots/refined_Monarch：_Google's_Planet-Scale_In-Memory_Time_Series_Database-(1080p25)_screenshots/frame_00-08-30.jpg)

This hierarchical structure, with components like indices and caches at different levels, allows for efficient routing, data storage, and query processing at Google's scale.

---

