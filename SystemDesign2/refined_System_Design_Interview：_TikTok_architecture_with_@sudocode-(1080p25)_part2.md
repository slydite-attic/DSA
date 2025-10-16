# System Design Interview： Tiktok Architecture With @Sudocode (1080P25) - Part 2

## Caching Strategies for Performance

### 1. Caching Video Metadata

*   **Location:** Metadata for "hot" or "trending" videos (highly viewed, frequently shared) can be cached.
*   **Purpose:** To avoid querying the main `Video Metadata` (NoSQL) store for every request, especially for popular content.
*   **Benefit:** Reduces database load and improves response times for fetching popular video information.

### 2. Caching Actual Video Content

*   **Responsibility:** The `CDN` is primarily responsible for caching the actual video files.
*   **Mechanism:** As videos are requested, the CDN caches them at edge locations. Subsequent requests for the same video from nearby users are served directly from the CDN's cache.
*   **Managed Service:** When using a third-party CDN, the caching mechanism (e.g., cache invalidation, cache population) is typically managed by the CDN provider. While advanced CDNs might offer APIs for explicit cache control (e.g., purging specific content or pre-populating caches), this is usually handled implicitly or through configuration.

## Interview Feedback and Key Learnings

### Strengths of the Design

![Screenshot at 00:40:17](notes_screenshots/refined_System_Design_Interview：_TikTok_architecture_with_@sudocode-(1080p25)_screenshots/frame_00-40-17.jpg)
![Screenshot at 00:41:28](notes_screenshots/refined_System_Design_Interview：_TikTok_architecture_with_@sudocode-(1080p25)_screenshots/frame_00-41-28.jpg)
![Screenshot at 00:41:40](notes_screenshots/refined_System_Design_Interview：_TikTok_architecture_with_@sudocode-(1080p25)_screenshots/frame_00-41-40.jpg)
![Screenshot at 00:42:50](notes_screenshots/refined_System_Design_Interview：_TikTok_architecture_with_@sudocode-(1080p25)_screenshots/frame_00-42-50.jpg)

The proposed system design demonstrates several strong engineering practices:

1.  **Decoupling Ingestion from Processing:**
    *   **Pipeline Architecture:** The use of a message queue and a worker pipeline for video ingestion and processing effectively decouples the upload rate from the processing rate.
    *   **Load Management:** This prevents system collapse during peak upload times (e.g., holidays) by allowing workers to process videos at their own pace, rather than requiring immediate, real-time processing.
    *   **Fault Tolerance:** The queue acts as a buffer, ensuring that even if processing workers fail, requests are not lost and can be retried.

2.  **High Availability and Fault Tolerance:**
    *   **Multi-Zone Replication:** Data (videos, metadata) is replicated across multiple availability zones and regions.
    *   **S3 and CDN:** Leveraging S3 for durable storage and CDN for global distribution ensures that content remains available even if a region or specific node experiences an outage.

3.  **Appropriate Database Choices:**
    *   Selecting MySQL for structured user data, NoSQL for flexible video metadata, and Object Storage (S3) for large video files demonstrates a good understanding of database types and their suitability for different data characteristics and access patterns.

4.  **CDN for Global Distribution:**
    *   The strategic use of a CDN is critical for achieving low-latency video streaming for a geographically dispersed user base. It minimizes network distance and optimizes content delivery.

5.  **Modular and Scalable Pipeline:**
    *   The video processing pipeline, with its chunking, parallel format, and resolution conversion, is highly scalable and extensible. It allows for easy adaptation to new devices, formats, or processing requirements.

### Areas for Improvement

1.  **Early Cost Estimation:**
    *   **Issue:** Cost estimation was discussed later in the interview, leading to some hesitation and assumptions about scalability (e.g., "is this scalable enough?").
    *   **Recommendation:** Incorporating a basic cost estimation (storage, bandwidth, processing) earlier in the design process would provide a clearer understanding of the system's economic feasibility and help validate architectural choices more smoothly. This helps in making informed trade-offs.

2.  **Network Protocols (Initial Hesitation):**
    *   **Issue:** There was some initial hesitation when discussing the specific network protocols for video upload (e.g., HTTP vs. FTP).
    *   **Recommendation:** While the eventual choice of HTTPS was correct, being more confident and articulate about the rationale for choosing standard web protocols (HTTPS for security, reliability, and web integration) over less suitable alternatives (like FTP) would strengthen the discussion.

This comprehensive design covers the core functional and non-functional requirements, demonstrating a robust and scalable architecture for a short video sharing platform.

---

## Interviewer's Closing Remarks and Feedback

![Screenshot at 00:43:38](notes_screenshots/refined_System_Design_Interview：_TikTok_architecture_with_@sudocode-(1080p25)_screenshots/frame_00-43-38.jpg)
![Screenshot at 00:45:24](notes_screenshots/refined_System_Design_Interview：_TikTok_architecture_with_@sudocode-(1080p25)_screenshots/frame_00-45-24.jpg)

The interviewer concluded the mock system design interview, expressing satisfaction with the overall design and highlighting key takeaways.

### Interviewer's Assessment:

*   **Overall Positive:** The design effectively addressed the problem, demonstrating good engineering practices and a scalable architecture.
*   **Key Strengths Reiterated:**
    *   **Decoupled Ingestion and Processing:** The use of a queue and worker pipeline for video processing was highly praised for its ability to manage load and ensure system stability during high traffic.
    *   **High Availability and Fault Tolerance:** The focus on multi-zone replication and leveraging S3 with CDN for global distribution was well-received.
    *   **Appropriate Data Storage:** The selection of different database types for different data (MySQL for user data, NoSQL for metadata, S3 for video files) was considered a strong point.
*   **Areas for Deeper Exploration (Had Time Permitted):**
    *   **Cost Estimation:** The interviewer noted that a more proactive and detailed cost estimation early in the discussion would have provided a smoother flow and stronger justification for architectural choices. This is often a critical aspect in real-world system design.
    *   **Network Protocols:** The interviewer observed some hesitation when discussing specific network protocols for video upload and download. While HTTPS was correctly chosen, a more confident and in-depth explanation of the alternatives and trade-offs would have been beneficial.

### Candidate's Reflection on Network Protocols:

*   **Honesty is Key:** The candidate acknowledged the hesitancy, explaining that their practical experience was primarily with HTTPS, and they lacked hands-on knowledge of other protocols like FTP for large file transfers.
*   **Learning Opportunity:** This highlights a valuable lesson for interviews: it's better to admit limited experience in an area and express willingness to learn, rather than guessing. Interviewers often look for self-awareness and a growth mindset.

### Conclusion

The mock interview successfully demonstrated the candidate's ability to design a complex, scalable, and fault-tolerant system for a short video platform. The discussion covered functional and non-functional requirements, architectural components, data storage choices, and processing pipelines, with valuable feedback provided for future improvement.

---

