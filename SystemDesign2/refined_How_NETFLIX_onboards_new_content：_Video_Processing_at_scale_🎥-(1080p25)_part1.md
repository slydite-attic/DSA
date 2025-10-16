# How Netflix Onboards New Content： Video Processing At Scale 🎥 (1080P25) - Part 1

![Screenshot at 00:00:09](notes_screenshots/refined_How_NETFLIX_onboards_new_content：_Video_Processing_at_scale_🎥-(1080p25)_screenshots/frame_00-00-09.jpg)
![Screenshot at 00:00:19](notes_screenshots/refined_How_NETFLIX_onboards_new_content：_Video_Processing_at_scale_🎥-(1080p25)_screenshots/frame_00-00-19.jpg)
![Screenshot at 00:00:29](notes_screenshots/refined_How_NETFLIX_onboards_new_content：_Video_Processing_at_scale_🎥-(1080p25)_screenshots/frame_00-00-29.jpg)

# Netflix Content Onboarding: Engineering Challenges and Solutions

This lecture explores the engineering challenges Netflix faces when onboarding new content (TV series, movies) onto its platform, beyond the legal aspects. The goal is to simplify complex technical details, especially concerning video encoding.

## Core Challenges in Content Uploading

When new content is uploaded, Netflix encounters several key challenges related to storage and delivery:

1.  **Multiple Formats (Codecs):**
    *   **Need:** Content must be stored in various video formats (e.g., MP4, AVI) to cater to diverse user internet connection speeds and desired video quality.
    *   **Quality Variations:**
        *   **High Quality:** Detailed formats with minimal data loss, offering maximum video quality, suitable for high-speed internet.
        *   **Low Quality:** Formats with reduced quality, often using lossy compression to achieve smaller file sizes, suitable for slower connections.
    *   **Codecs:** A codec (coder-decoder) is a technology used to compress and decompress video data.
        *   **Compression:** Reduces the original file size, which can be very large.
        *   **Lossy Compression:** A type of compression where some data is intentionally discarded to achieve significantly smaller file sizes. This results in a reduction of quality but is often acceptable for streaming.
        *   **Example:** A raw video might be very large; applying a codec reduces its size for efficient storage and streaming.

2.  **Multiple Resolutions:**
    *   **Need:** Different devices require different video resolutions.
    *   **Examples:**
        *   Cell phones require significantly lower resolutions.
        *   Televisions or laptops require much higher resolutions (e.g., 1080p, 720p).

## The Combinatorial Problem

The need for multiple formats and resolutions leads to a combinatorial problem:
*   If `F` is the number of required formats and `R` is the number of required resolutions, then each original video must be processed into `F * R` unique versions.
*   Each combination (e.g., high quality 720p, AVI 480p) represents a distinct video file that needs to be generated and stored.

![Screenshot at 00:03:04](notes_screenshots/refined_How_NETFLIX_onboards_new_content：_Video_Processing_at_scale_🎥-(1080p25)_screenshots/frame_00-03-04.jpg)

## The Video Encoding Process

Netflix continuously works to improve its video encoding techniques.
*   **Efficiency Gains:** New encoding techniques can drastically reduce file sizes (e.g., an older movie encoded at 6GB might be re-encoded to 1GB using a new process).
*   **Resource Intensity:** Re-encoding existing content or encoding new content is a time-consuming and computationally intensive process.
*   **Limitations of Single-Machine Processing:**
    *   Assigning the entire encoding responsibility to a single computer is inefficient due to the time required.
    *   It introduces a single point of failure; if the computer shuts down, the process halts.

## Netflix's Solution: Distributed Video Chunking

To overcome the limitations of single-machine processing, Netflix employs a smart strategy:

1.  **Video Segmentation:** The original video is broken down into smaller, manageable **chunks**.
2.  **Parallel Processing:** Each chunk can then be processed independently and in parallel across multiple machines for all required formats and resolutions.
    *   For example, a single chunk 'A' might be encoded into:
        *   `A.mp4` at 1080p resolution
        *   `A.avi` at 480p resolution
        *   And so on, for all `F * R` combinations.
3.  **Task Definition:** Each combination of a chunk, a resolution, and a format constitutes an independent task. This allows for massive parallelization, significantly speeding up the overall encoding process.

### Evolution of Chunking Strategies

Netflix's approach to chunking has evolved:

*   **Initial Approach: Fixed-Size Chunks**
    *   **Method:** Videos were typically broken into chunks of equal duration (e.g., three minutes each).
    *   **Perceived Benefit:** This seemed fair, as each processor would seemingly handle an equal amount of work.
    *   **Drawback:** The computational complexity of encoding a fixed-duration chunk can vary significantly depending on the content. For example, a three-minute action sequence with rapid motion and high detail will take much longer to encode than a three-minute static scene. This led to uneven workloads and bottlenecks in the processing pipeline.

---

### Refined Chunking Strategy: Scene-Based Segmentation

The initial approach of breaking videos into fixed-duration chunks (e.g., three minutes) posed a significant problem for user experience.

*   **Problem with Fixed-Time Chunks:** Imagine an action movie where a critical moment (e.g., a car chase climax) occurs at the boundary of a three-minute chunk. If a user makes an API call to load this chunk, and processing takes time, it results in a noticeable lag, disrupting the seamless viewing experience.
    ![Screenshot at 00:03:35](notes_screenshots/refined_How_NETFLIX_onboards_new_content：_Video_Processing_at_scale_🎥-(1080p25)_screenshots/frame_00-03-35.jpg)

*   **Solution: Scene-Based Chunking:** Netflix transitioned from time-based chunks to scene-based segmentation.
    *   **Shots:** Videos are broken into much finer-grained segments called "shots," typically around four seconds long.
    *   **Scenes:** Multiple shots are then collated to form a complete "scene" (e.g., an entire car chase sequence).
    *   **Benefit for User Experience:** When a user navigates to a specific point in a video, the video-serving algorithm can fetch an entire scene (composed of many four-second shots) as a single block. This ensures that critical moments or continuous sequences are loaded completely, minimizing lag and providing a much smoother user experience.
    ![Screenshot at 00:05:12](notes_screenshots/refined_How_NETFLIX_onboards_new_content：_Video_Processing_at_scale_🎥-(1080p25)_screenshots/frame_00-05-12.jpg)
    ![Screenshot at 00:05:33](notes_screenshots/refined_How_NETFLIX_onboards_new_content：_Video_Processing_at_scale_🎥-(1080p25)_screenshots/frame_00-05-33.jpg)

### Adaptive Content Delivery: Sparse vs. Dense Movies

Netflix's algorithm further optimizes content delivery by classifying movies based on viewing patterns:

*   **Sparse Movies (Sparsely Seen):**
    *   **Definition:** These are movies where users tend to jump between different points, watching specific scenes rather than a continuous linear progression.
    *   **Netflix's Assumption:** The system assumes users are arbitrarily clicking, indicating a non-linear viewing pattern.
    *   **Delivery Strategy:** For sparse movies, Netflix's recommendation/prediction algorithm avoids pre-fetching large amounts of data. Instead, it primarily sends only the specific data (chunks/scenes) that the user has explicitly requested, thereby conserving bandwidth and resources.

*   **Dense Movies (Engaging/Continuously Watched):**
    *   **Definition:** These are movies where users watch continuously for extended periods, following a linear narrative.
    *   **Netflix's Assumption:** The system can predict with high certainty that the next sequential parts of the movie will be watched.
    *   **Delivery Strategy:** For dense movies, the system proactively pre-fetches future parts of the video onto the user's device (into the buffer). This ensures uninterrupted playback and a truly seamless viewing experience.

### Content Storage: Amazon S3

Netflix stores its vast library of video content on **Amazon S3 (Simple Storage Service)**.

*   **Purpose:** S3 is a cloud-based object storage service designed for storing static data.
*   **Characteristics of Static Data:** The video files, once encoded into various formats and resolutions, do not frequently change.
*   **Advantages of S3:**
    *   **Cost-Effectiveness:** S3 is extremely cheap for storing large volumes of static data compared to traditional databases.
    *   **Scalability and Durability:** It offers high scalability and durability, crucial for a platform like Netflix with petabytes of content.
*   **Comparison to Databases:** Databases are typically more expensive because they offer additional guarantees such as transactional integrity, frequent updates, and complex querying capabilities, which are not required for storing static video assets.
    ![Screenshot at 00:06:16](notes_screenshots/refined_How_NETFLIX_onboards_new_content：_Video_Processing_at_scale_🎥-(1080p25)_screenshots/frame_00-06-16.jpg)

### Internet Service Provider (ISP) Fundamentals

To understand Netflix's innovation in content delivery, it's essential to grasp how the internet works at a basic level:

*   **Domain Name System (DNS):** When a user types a domain name (e.g., `facebook.com` or `netflix.com`) into a browser, the request first goes to their Internet Service Provider (ISP).
*   **IP Address Resolution:** The ISP uses a DNS server to translate the human-readable domain name into a numerical IP address. This IP address represents the physical location of a computer (server) on the internet.
*   **Direct Communication:** The user's device then communicates directly with that server. For example, typing `facebook.com` means the user's computer is literally "talking" to a Facebook server somewhere on the internet.

This foundational understanding of how ISPs connect users to online services sets the stage for exploring Netflix's unique and innovative content delivery network (CDN) strategy.

---

### Geographical Challenges and Caching

*   **Problem:** Netflix's main servers are typically geographically concentrated (e.g., in the US). For users far away (e.g., India), requests for content must travel long distances, leading to:
    *   **High Latency:** Increased time for signals to travel back and forth.
    *   **Slow Data Transfer:** Especially for video, which involves large amounts of data, this results in slow loading and poor user experience.
    ![Screenshot at 00:07:12](notes_screenshots/refined_How_NETFLIX_onboards_new_content：_Video_Processing_at_scale_🎥-(1080p25)_screenshots/frame_00-07-12.jpg)
    ![Screenshot at 00:07:22](notes_screenshots/refined_How_NETFLIX_onboards_new_content：_Video_Processing_at_scale_🎥-(1080p25)_screenshots/frame_00-07-22.jpg)
    ![Screenshot at 00:07:33](notes_screenshots/refined_How_NETFLIX_onboards_new_content：_Video_Processing_at_scale_🎥-(1080p25)_screenshots/frame_00-07-33.jpg)

*   **Engineering Solution: Caching:** A fundamental engineering principle to improve user experience is to cache information. This involves:
    *   **Pre-computing and Storing:** Pre-processed or frequently accessed data is stored closer to the users.
    *   **Example:** If a popular series like "Sacred Games" is released in India, it can be cached locally.

### Netflix Open Connect: Distributed Caching with ISPs

Netflix innovatively extended the caching concept by partnering directly with Internet Service Providers (ISPs) through its **Open Connect** program.

*   **Open Connect Boxes:** Netflix provides specialized caching servers, known as Open Connect boxes, to ISPs. These boxes are physically placed within the ISP's network infrastructure.
*   **Localized Content Storage:** These boxes store a vast amount of Netflix content, including popular local movies and series.
*   **Improved Request Handling:**
    *   When a user requests a movie (e.g., a Bollywood film in India), the ISP's network first checks its local Open Connect box.
    *   If the movie is found in the box, it is served directly from there.
*   **Benefits of Open Connect:**
    1.  **Reduced Latency & Faster Delivery:** Content is served from a geographically closer source, significantly reducing the time to deliver video and improving user experience.
    2.  **Bandwidth Savings:** ISPs save substantial bandwidth by not having to fetch the same content repeatedly from Netflix's distant US servers.
    3.  **Reduced Load on Netflix Servers:** A significant portion of traffic (around 90%) is handled by these local Open Connect boxes, drastically reducing the load on Netflix's central infrastructure.
    4.  **Localized Content:** Boxes can be configured to store content most popular in their specific region (e.g., Bollywood movies for India, different content for Britain).
    5.  **ISP Partnership:** ISPs are incentivized to host these boxes because it reduces their operational costs and improves their service quality, making them appear as "really nice guys" to their customers.
    *   **Industry Trend:** Other platforms like YouTube also use similar strategies (e.g., YouTube Red boxes) to achieve similar benefits.
    ![Screenshot at 00:09:58](notes_screenshots/refined_How_NETFLIX_onboards_new_content：_Video_Processing_at_scale_🎥-(1080p25)_screenshots/frame_00-09-58.jpg)

### Content Updates and Synchronization

*   **New Content Delivery:** When new series or movies are released, the Open Connect boxes need to be updated.
*   **Scheduled Updates:** Updates are typically performed during off-peak hours (e.g., around 4 AM local time) when the load on the boxes and network is minimal.
*   **Process:**
    1.  A new movie is registered and processed by Netflix (chunked, encoded into various formats/resolutions).
    2.  Netflix's central servers then push these new content chunks to the relevant Open Connect boxes.
    3.  This ensures that local boxes always have the latest content, keeping users happy with fresh, quickly accessible media.

## Conclusion

Netflix's ability to operate at scale and provide a seamless user experience globally is largely due to two key innovations:
1.  **Advanced Video Processing:** Breaking videos into scene-based chunks and adaptively delivering content based on viewing patterns (sparse vs. dense movies).
2.  **Distributed Content Delivery:** The revolutionary Open Connect program, which caches content directly within ISP networks, dramatically reducing latency, saving bandwidth, and offloading central servers. This system design approach highlights real-world solutions to complex engineering problems.

---

This concludes the discussion on Netflix's approach to content onboarding and delivery. The lecture highlighted the innovative engineering solutions that enable Netflix to provide a seamless streaming experience globally.

**Key Takeaways from the Entire Lecture:**

*   **Content Processing Challenges:** Handling multiple video formats (codecs) and resolutions to cater to diverse user devices and internet speeds.
*   **Distributed Encoding:** Breaking videos into smaller chunks for parallel processing to efficiently encode content into various permutations.
*   **Intelligent Chunking:** Evolving from fixed-time chunks to scene-based segmentation ("shots" and "scenes") to improve user experience by ensuring critical sequences are loaded seamlessly.
*   **Adaptive Delivery:** Distinguishing between "sparse" (non-linear viewing) and "dense" (continuous viewing) movies to optimize data pre-fetching and bandwidth usage.
*   **Global Content Delivery Network (CDN):** The revolutionary **Netflix Open Connect** program, which involves placing dedicated caching servers directly within ISP networks worldwide. This strategy significantly reduces latency, saves bandwidth for ISPs, and offloads 90% of traffic from Netflix's central servers.
*   **Scheduled Updates:** Utilizing off-peak hours (e.g., 4 AM) to efficiently update Open Connect boxes with new content, ensuring fresh media is readily available to local users.

These sophisticated system design choices, particularly in video processing and content serving, are crucial for Netflix to operate at its massive global scale.

---

