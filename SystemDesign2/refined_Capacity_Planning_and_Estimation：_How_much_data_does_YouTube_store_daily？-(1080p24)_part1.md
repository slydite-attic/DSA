# Capacity Planning And Estimation： How Much Data Does Youtube Store Daily？ (1080P24) - Part 1

# Estimation Questions: YouTube's Daily Storage Requirements

Estimation questions are a common and valuable component in design interviews and for general problem-solving. They test your ability to break down complex problems, make reasonable assumptions, and perform order-of-magnitude calculations.

## Problem Statement

**Estimate YouTube's total daily video storage requirements.**

![Screenshot at 00:00:11](notes_screenshots/refined_Capacity_Planning_and_Estimation：_How_much_data_does_YouTube_store_daily？-(1080p24)_screenshots/frame_00-00-11.jpg)

## Key Assumptions

To approach this problem, we'll start with a set of reasonable assumptions. It's crucial to state these assumptions clearly and be prepared to discuss them with an interviewer.

| Category             | Assumption                                                               | Value                                |
| :------------------- | :----------------------------------------------------------------------- | :----------------------------------- |
| **User Base**        | Total YouTube users                                                      | 1 billion (10^9)                     |
| **Upload Activity**  | Proportion of users who upload videos daily                              | 1 in 1000 users                      |
| **Video Length**     | Average length of an uploaded video                                      | 10 minutes                           |
| **Video Quality**    | Storage size for a 2-hour movie (after YouTube's typical compression)    | 0.4 GB (400 MB)                      |
| **Redundancy**       | Number of copies for fault tolerance and performance                     | 3 copies                             |
| **Resolutions**      | Storage multiplier for supporting multiple video resolutions             | 2x original high-resolution storage  |

## Step-by-Step Estimation

We will break down the calculation into several logical steps.

### 1. Calculate Raw Upload Data (Single Copy, Single Resolution)

This step determines the base amount of data uploaded daily before considering redundancy or multiple resolutions.

*   **Number of daily uploaders:**
    *   Total Users: 1,000,000,000
    *   Uploader Ratio: 1/1000
    *   Daily Uploaders = 1,000,000,000 / 1,000 = 1,000,000 (10^6) users

*   **Total minutes uploaded per day:**
    *   Daily Uploaders: 1,000,000
    *   Average Video Length: 10 minutes
    *   Total Minutes Uploaded = 1,000,000 users * 10 minutes/user = 10,000,000 (10^7) minutes

*   **Determine storage size per minute of video:**
    *   A 2-hour (120 minutes) movie is assumed to be 0.4 GB (400 MB).
    *   Storage per hour = 400 MB / 2 hours = 200 MB/hour
    *   Storage per minute = 200 MB / 60 minutes ≈ 3.33 MB/minute (We'll use 3 MB/minute for simplicity)

*   **Total raw storage required per day:**
    *   Total Minutes Uploaded: 10^7 minutes
    *   Storage per minute: 3 MB/minute
    *   Raw Storage = 10^7 minutes * 3 MB/minute = 30 * 10^6 MB = 30,000 GB = **30 TB**

![Screenshot at 00:02:28](notes_screenshots/refined_Capacity_Planning_and_Estimation：_How_much_data_does_YouTube_store_daily？-(1080p24)_screenshots/frame_00-02-28.jpg)

### 2. Account for Redundancy

To ensure fault tolerance (e.g., against data center failures like a tsunami) and improve performance (by serving content from geographically closer locations), multiple copies of each video are stored.

*   **Reasoning for multiple copies:**
    *   **Fault Tolerance:** Prevents data loss if one storage location fails.
    *   **Performance:** Reduces latency for users by serving content from a nearby server.
*   **Assumption:** We'll assume 3 copies are stored.
*   **Storage with Redundancy:**
    *   Raw Storage: 30 TB
    *   Number of Copies: 3
    *   Redundant Storage = 30 TB * 3 = **90 TB**

### 3. Account for Multiple Resolutions

YouTube typically stores videos in various resolutions (e.g., 720p, 480p, 360p, 240p, 144p) to cater to different devices and network conditions. Lower resolutions consume less storage.

*   **Resolution Scaling Example:**
    *   If 720p takes `X` MB, then:
        *   480p might take `X/2` MB
        *   360p might take `X/4` MB
        *   240p might take `X/8` MB
        *   144p might take `X/16` MB
*   **Total Storage for All Resolutions:**
    *   The sum of these sizes (`X + X/2 + X/4 + X/8 + X/16 + ...`) approaches `2X`.
    *   Therefore, storing all resolutions roughly doubles the storage requirement of the highest resolution.
*   **Total Storage with Multiple Resolutions:**
    *   Redundant Storage: 90 TB
    *   Resolution Multiplier: 2
    *   Total Daily Storage = 90 TB * 2 = **180 TB**

![Screenshot at 00:02:51](notes_screenshots/refined_Capacity_Planning_and_Estimation：_How_much_data_does_YouTube_store_daily？-(1080p24)_screenshots/frame_00-02-51.jpg)

### Final Daily Storage Estimate

Based on our assumptions and calculations, YouTube needs approximately **180 TB (or 0.18 Petabytes, which is roughly 0.2 Petabytes)** of storage per day for new video uploads.

## Important Considerations for Estimation Questions

*   **Acknowledge Assumptions:** Always highlight the assumptions made.
*   **Interviewer Interaction:** Continuously engage with the interviewer. They might provide specific numbers for certain variables (e.g., number of uploaders) or guide you on the reasonableness of your assumptions.
*   **Impact of Assumptions:** Be aware that changing a single major assumption can significantly alter the final estimate.
    *   **Example:** If the average 2-hour video was stored at 4 GB (original high quality) instead of 0.4 GB, the initial raw storage would be 300 TB instead of 30 TB. This would lead to a final estimate of 1.8 PB instead of 0.18 PB – an order of magnitude difference.
*   **Process Over Exact Numbers:** The most crucial aspect of an estimation question is demonstrating a logical thought process, ability to break down the problem, and clear communication of assumptions and steps, rather than arriving at a perfectly precise number.

---

### Importance of Process and Accuracy in Estimation

When tackling estimation questions, the primary goal is to demonstrate a logical thought process and the ability to break down a complex problem into manageable parts.

*   **Acceptable Error Margins:** It is generally acceptable to be off by a factor of 10 or even 100 in your final numerical estimate.
*   **Unacceptable Error Margins:** Being off by factors of 1,000 or 10,000 indicates a fundamental flaw in your assumptions or calculation methodology, requiring re-evaluation.
*   **Impact of Input Accuracy:** The closer your initial assumptions and input numbers are to reality, the more accurate your final solution will be.
*   **Communication is Key:** Always articulate your assumptions and the steps you're taking. This allows the interviewer to guide you or correct any significantly flawed assumptions.

### Alternative Video Size Estimation Method (and its Pitfalls)

Instead of using the highly compressed video size assumption (0.4 GB for 2 hours), one might attempt to estimate video size based on individual frames.

*   **Conceptual Approach:** A video is essentially a rapid sequence of images.
*   **Assumptions for this method:**
    *   Video length: 1 minute (60 seconds)
    *   Frames per second (FPS): 24 (approximated to 25 for easier calculation)
    *   Size of one high-quality image: 1 MB
*   **Calculation:**
    *   Total frames per minute = 25 frames/second * 60 seconds/minute = 1,500 frames
    *   Storage per minute = 1,500 frames * 1 MB/frame = 1,500 MB = **1.5 GB/minute**

![Screenshot at 00:04:59](notes_screenshots/refined_Capacity_Planning_and_Estimation：_How_much_data_does_YouTube_store_daily？-(1080p24)_screenshots/frame_00-04-59.jpg)

*   **Comparison and Conclusion:**
    *   This estimate (1.5 GB/minute) is significantly higher than our previous, more realistic estimate of 3 MB/minute (which was based on YouTube's typical compression for a 0.4 GB, 2-hour video).
    *   The discrepancy highlights that making low-level assumptions (like 1 MB per frame) without considering the heavy compression applied to video content in real-world platforms like YouTube can lead to vastly inflated and inaccurate estimates. While a single high-quality photo might be 1MB, a *frame within a compressed video stream* is typically much, much smaller due to inter-frame compression techniques. This example underscores the importance of choosing appropriate levels of abstraction for your assumptions.

### Reality Check: Comparing Assumptions with Reported Data

It's valuable to compare your core assumptions with publicly available data or industry benchmarks where possible.

*   **Our Model's Upload Rate:**
    *   Based on 10^7 minutes of total video uploaded per day (from previous calculations).
    *   Average daily upload rate = (10^7 minutes of video / 1 day) * (1 day / 1440 minutes of real time) = 6944.4 minutes of video per minute of real time.
    *   Converting to hours: 6944.4 minutes / 60 = **~115.7 hours of new content uploaded per minute of real time.**
*   **YouTube's Reported Upload Rate:**
    *   YouTube reports approximately **600 hours of new content uploaded every minute.**

![Screenshot at 00:05:23](notes_screenshots/refined_Capacity_Planning_and_Estimation：_How_much_data_does_YouTube_store_daily？-(1080p24)_screenshots/frame_00-05-23.jpg)

*   **Analysis:** Our initial assumptions for upload activity (1 billion users, 1/1000 uploaders, 10-minute video) result in an upload rate that is roughly 5 times lower than YouTube's reported figures (600 / 115.7 ≈ 5.18). While this is a notable difference, it's within the "factor of 10 or 100" range that might be considered acceptable in an estimation interview, rather than a catastrophic error of 1,000x or 10,000x. This suggests our initial assumptions, though slightly conservative, were in the right ballpark.

### Estimating Metadata Cache Storage

Beyond the raw video files, YouTube also needs to store and quickly retrieve metadata for displaying videos to users.

*   **Metadata to Cache:**
    *   **Thumbnail:** A small image representing the video.
    *   **Video Title:** Textual description.
*   **Size Comparison:** Thumbnails (images) are generally much larger than video titles (text strings). We'll focus on thumbnails as the dominant factor.

#### Thumbnail Storage Estimation

1.  **Individual Thumbnail Size:**
    *   Assume an original high-quality image (if it were not compressed for display) could be 1 MB.
    *   For display in user interfaces (e.g., recommendation lists, trending tabs), thumbnails are significantly downscaled.
    *   If scaled down by a factor of 10 on both height and width, the total size reduces by a factor of 10 * 10 = 100.
    *   Estimated thumbnail size = 1 MB / 100 = **10 KB**.

![Screenshot at 00:05:35](notes_screenshots/refined_Capacity_Planning_and_Estimation：_How_much_data_does_YouTube_store_daily？-(1080p24)_screenshots/frame_00-05-35.jpg)

2.  **Number of Videos to Cache:**
    *   It's not feasible or necessary to cache metadata for *all* videos ever uploaded.
    *   Focus on "popular videos," which are frequently accessed.
    *   **Definition of "Popular Videos" for caching:** We'll assume this includes all videos uploaded within the last 90 days, plus "evergreen" content. For simplicity, we can approximate this by taking the last 90 days' worth of uploads, as evergreen content would naturally cycle into and out of a Least Recently Used (LRU) cache, and 90 days provides a large active set.
    *   Daily uploads (from previous calculation) = 1,000,000 videos/day (10^6).
    *   Total videos in cache scope = 10^6 videos/day * 90 days = **90 * 10^6 videos**.

3.  **Total Cache Storage Requirement:**
    *   Total storage = (Number of popular videos) * (Size per thumbnail)
    *   Total storage = (90 * 10^6 videos) * (10 KB/video)
    *   Total storage = 900 * 10^6 KB = 9 * 10^8 KB
    *   Converting to larger units:
        *   9 * 10^8 KB = 9 * 10^5 MB = 900 GB
        *   This is approximately **1 TB** of data.

#### Hardware Implications for Cache

*   **RAM Requirement:** 1 TB of RAM is a substantial amount, typically not available in a single server.
*   **Distributed System:** This necessitates a distributed caching system spanning multiple computers.
*   **Estimating Number of Servers:**
    *   Assume each server has 16 GB of RAM (a common server configuration for caching).
    *   Number of servers = Total RAM needed / RAM per server
    *   Number of servers = 1 TB / 16 GB = 1024 GB / 16 GB = **64 servers**.

This estimation provides a baseline for the infrastructure needed to efficiently serve video metadata.

---

### Hardware Implications for Cache (Continued)

*   **Node Capacity and Routing:** When retrieving data from a cache, especially with multiple nodes, efficient routing to the correct node is crucial. We don't want to search through 32 GB of RAM on a single node; instead, we route the request to the specific node that holds the desired data.
*   **Optimal RAM per Node:** While using 32 GB RAM per node would reduce the total number of nodes, 16 GB per node is a common and often cost-effective choice for distributed caching systems, allowing for horizontal scaling.
*   **Initial Calculation (without redundancy):**
    *   Total RAM required: 1 TB (1024 GB)
    *   RAM per node: 16 GB
    *   Number of nodes = 1024 GB / 16 GB/node = **64 nodes**

*   **Redundancy for Cache Nodes:**
    *   **Need for Redundancy:**
        *   **Global Service:** To serve videos worldwide, cache data must be replicated across different geographical locations.
        *   **Fault Tolerance:** If a cache node crashes, it can lead to cascading failures, especially if nodes are operating at peak capacity. Losing a node would increase the load on remaining nodes, potentially causing them to crash as well.
    *   **Capacity Planning:** To prevent cascading failures and ensure availability, it's prudent to run nodes below peak capacity.
    *   **Assumption:** Maintain nodes at approximately 50% capacity. This effectively doubles the number of required nodes for the same amount of active data.
    *   **Adjusted Number of Cache Nodes:**
        *   Initial nodes: 64
        *   Multiplier for 50% capacity: 2
        *   Total nodes = 64 * 2 = **128 nodes** (approximately 100-150 nodes, or "a few hundred" as stated by the lecturer, suggesting around 500 for a very rough estimate to include some slack and higher redundancy)

This caching system, with each node having 16 GB of RAM, should be sufficient for YouTube's metadata.

### Estimating Video Processing Capacity (Transcoding)

Beyond storage, YouTube needs to process (transcode) the uploaded videos into various formats and resolutions. This is a continuous operation.

*   **Input Data Rate:** We need to determine how much raw video data needs to be processed *per second* globally.
    *   Total minutes of video uploaded per day (from previous calculations) = 10^7 minutes.
    *   **Convert total minutes to total GB:**
        *   From previous calculations, 2 hours (120 minutes) of compressed video is 0.4 GB.
        *   So, 1 minute of video is 0.4 GB / 120 minutes = 1/300 GB/minute.
        *   Total GB per day = 10^7 minutes * (1/300 GB/minute) = (10^7 / 300) GB = **33,333.33 GB/day** (approximately 3.3 * 10^4 GB/day).
        *   The lecturer simplifies this to 10^4 / 3 GB per day.

![Screenshot at 00:09:23](notes_screenshots/refined_Capacity_Planning_and_Estimation：_How_much_data_does_YouTube_store_daily？-(1080p24)_screenshots/frame_00-09-23.jpg)

*   **Convert total GB/day to MB/second:**
    *   Total GB/day = 3.33 * 10^4 GB/day
    *   Seconds in a day = 24 hours/day * 60 minutes/hour * 60 seconds/minute = 86,400 seconds/day (approximately 8.6 * 10^4 seconds/day).
    *   Processing rate = (3.33 * 10^4 GB/day) / (8.64 * 10^4 seconds/day)
    *   Processing rate ≈ 0.385 GB/second = 385 MB/second.
    *   The lecturer performs a slightly different simplification: (4 * 10^4 MB) / (200 * 60 seconds) = 40 MB/sec. This uses the 0.4GB for 2 hours assumption, converting it to 400MB for 120 minutes. So 400MB / (3*25*60) seconds (using a 25 hour day approximation and 3x redundancy factor within the denominator) is roughly 40MB/sec. We'll follow the lecturer's simplified 40 MB/second for consistency.

![Screenshot at 00:09:47](notes_screenshots/refined_Capacity_Planning_and_Estimation：_How_much_data_does_YouTube_store_daily？-(1080p24)_screenshots/frame_00-09-47.jpg)

*   **Adjusted Processing Rate for Multiple Formats and Redundancy:**
    *   The 40 MB/second is for the raw, highest-quality input.
    *   However, videos are processed into multiple resolutions (e.g., 5-6 different ones, which we previously approximated as 2x total storage).
    *   Also, processed videos are stored across multiple data centers (e.g., 3 data centers).
    *   Combining these factors, we can estimate a multiplier of roughly 10 (e.g., 2x for resolutions * 3x for data centers ≈ 6x, rounded up for overhead).
    *   Worldwide processing rate = 40 MB/second * 10 = **400 MB/second**. This is the total data throughput required for processing.

### Performance of a Single Processing Machine

Now, let's estimate how much time a single machine takes to process 1 MB of video data. A typical video processing workflow involves:

1.  **Read Operation:** Reading the video data into memory from disk.
    *   Assumption: Reading 1 MB from disk takes **10 milliseconds (ms)**.
2.  **Processing Operation:** Performing image/video processing (e.g., encoding, resizing).
    *   Assumption: Processing 1 MB takes **20 milliseconds (ms)**. (This is an assumption made for the interview context).
3.  **Write Operation:** Writing the processed data back to disk/storage.
    *   Assumption: Writing 1 MB takes twice the read time, so **20 milliseconds (ms)**. (I/O operations are generally slower than memory operations).

*   **Total Time per 1 MB of Data:**
    *   Total time = Read time + Processing time + Write time
    *   Total time = 10 ms + 20 ms + 20 ms = **50 milliseconds (ms)** per 1 MB.

### Total Processing Workload

We need to calculate the total amount of "work" (in seconds) required per second of real time.

*   **Work per second:**
    *   Required data throughput: 400 MB/second
    *   Time to process 1 MB: 50 ms/MB
    *   Total work = (400 MB/second) * (50 ms/MB)
    *   Convert ms to seconds: 50 ms = 0.050 seconds
    *   Total work = 400 * 0.050 seconds/second = **20 seconds of work per second of real time.**

This metric (20 seconds of work per second) indicates that a single machine cannot keep up with the processing demand. It means that for every 1 second of real-time video upload, we need 20 seconds of machine processing time. This is a critical insight, confirming the need for parallel processing.

---

### Determining Number of Processing Units

Since we have "20 seconds of work to do per second," this means a single processing unit cannot handle the incoming workload in real-time. We need to parallelize the processing.

*   **Required Processors:**
    *   Workload = 20 seconds of work per second
    *   This implies we need **20 processors** running in parallel to keep up with the incoming data stream in real-time.

![Screenshot at 00:11:50](notes_screenshots/refined_Capacity_Planning_and_Estimation：_How_much_data_does_YouTube_store_daily？-(1080p24)_screenshots/frame_00-11-50.jpg)

*   **Evaluation of the Number:** The lecturer notes that 20 processors seems like a relatively small number for a platform like YouTube, suggesting there might be factors missed in the estimation. This is a good point for an interviewer to probe further or for self-reflection. Possible missing factors could include:
    *   Higher actual video resolution/bitrate.
    *   More aggressive redundancy requirements.
    *   More complex processing steps (e.g., AI/ML analysis, content moderation).
    *   Peak vs. average load considerations.
    *   Overhead for managing the distributed system.

### Summary of Estimation Approach

The overall strategy for estimation questions involves breaking down a large, abstract problem into smaller, quantifiable steps that relate to known system behaviors.

1.  **Start with the Big Picture:** Begin with the overall question (e.g., total storage, processing power).
2.  **Break Down into Metrics:** Decompose the problem into measurable metrics (e.g., users, uploads, video length).
3.  **Make Reasonable Assumptions:** Clearly state all assumptions, especially those about scale, compression, redundancy, and processing times.
4.  **Simplify to Familiar Units:** Convert large-scale metrics (like "total minutes per day") into units that relate to individual computer capabilities (like "MB per second" or "milliseconds per MB"). This is crucial because computers operate on these smaller, time-based units.
    *   **Example:** A computer's performance is often described in terms of read/write speeds (milliseconds) or throughput (MB/second).
5.  **Perform Step-by-Step Calculations:** Execute the calculations logically, showing how each assumption feeds into the next step.
6.  **Validate Assumptions (where possible):** Be prepared to discuss if assumptions are reasonable and how they might impact the final result. Be aware of "red flag" numbers (e.g., assuming a read speed of 1 nanosecond, which is unrealistic for disk I/O).
7.  **Identify Bottlenecks/Requirements:** The final numbers should reveal the scale of resources needed (e.g., number of servers, amount of RAM, number of processors).

![Screenshot at 00:12:09](notes_screenshots/refined_Capacity_Planning_and_Estimation：_How_much_data_does_YouTube_store_daily？-(1080p24)_screenshots/frame_00-12-09.jpg)

### General Knowledge for System Design Interviews

To excel in estimation and system design interviews, it's beneficial to have a foundational understanding of common system metrics and their typical values. This includes:

*   **Latency Numbers:**
    *   Reading from CPU cache (L1/L2)
    *   Reading from RAM
    *   Reading from SSD/NVMe disk
    *   Reading from HDD disk
    *   Network round-trip times (within a data center, across continents)
*   **Throughput Numbers:**
    *   Disk I/O speeds (MB/s)
    *   Network bandwidth (Gbps)
*   **Storage Costs:** Rough idea of cost per GB for RAM vs. SSD vs. HDD.
*   **Common System Capacities:** Typical RAM, CPU cores, network interfaces in a standard server.

Familiarity with these "numbers every programmer should know" allows you to make more realistic and defensible assumptions during an interview. Resources like "Latency Numbers Every Programmer Should Know" are highly recommended.

---

