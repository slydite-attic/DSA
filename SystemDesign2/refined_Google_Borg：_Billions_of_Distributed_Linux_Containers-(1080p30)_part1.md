# Google Borg： Billions Of Distributed Linux Containers (1080P30) - Part 1

# Google Borg: A Foundation of Google's Infrastructure

![Screenshot at 00:00:00](notes_screenshots/refined_Google_Borg：_Billions_of_Distributed_Linux_Containers-(1080p30)_screenshots/frame_00-00-00.jpg)

Google Borg is a foundational system that has been operational at Google since 2005, predating its 2015 paper release by a decade. It serves as the absolute core of Google's infrastructure, providing compute and memory resources for processes across nearly all of its servers. An impressive 98% of all servers at Google rely on Borg for their operation.

## What is Google Borg?

Borg is a cluster management system responsible for the entire lifecycle of processes, from their initial deployment to their eventual termination. It abstracts away complex infrastructure concerns, allowing application developers to focus solely on their code.

Key responsibilities of Borg include:
*   **Deployment:** Finding suitable data centers and machines for application deployment.
*   **Resource Allocation:** Determining and allocating the correct number of resources (CPU, memory) for processes.
*   **Fault Tolerance:** Automatically restarting processes in case of crashes.
*   **Migration:** Migrating failing processes to healthier machines.
*   **End-to-End Management:** Handling all aspects of a process's lifecycle.

![Screenshot at 00:00:34](notes_screenshots/refined_Google_Borg：_Billions_of_Distributed_Linux_Containers-(1080p30)_screenshots/frame_00-00-34.jpg)

### Borg's Influence: Kubernetes

Borg's design and functionality were so effective that engineers who developed it at Google later created Kubernetes, an open-source container orchestration system. Kubernetes is extremely similar to Borg, sharing approximately 90% of its internal architectural principles, making the Borg paper highly relevant for understanding Kubernetes.

## Core Features and Functions

Borg provides a comprehensive suite of features essential for managing large-scale distributed systems:

![Screenshot at 00:01:32](notes_screenshots/refined_Google_Borg：_Billions_of_Distributed_Linux_Containers-(1080p30)_screenshots/frame_00-01-32.jpg)

1.  **Load Balancing:**
    *   Ensures services are judiciously distributed across available hardware.
    *   Optimizes resource utilization and cost efficiency by making the most of purchased hardware.

2.  **Process Lifecycle Management:**
    *   **Service Discovery:** Identifies and tracks the location of deployed processes.
        *   Example: If Google Maps is deployed across two clusters with 50 servers, Borg maintains a record of where each instance is running.
    *   **Borg Naming Server (BNS):** Similar to a Domain Name System (DNS), BNS provides a service registry that allows application developers to query the exact locations of their running application instances.
    *   Handles automatic restarts for crashed processes.

    ![Screenshot at 00:01:44](notes_screenshots/refined_Google_Borg：_Billions_of_Distributed_Linux_Containers-(1080p30)_screenshots/frame_00-01-44.jpg)

3.  **Auto Scaling:**
    *   Dynamically adjusts the number of resources allocated to applications based on demand.
    *   While common today, this was a significant advancement in 2005.

4.  **Capacity Planning:**
    *   Provides critical metrics and observability data.
    *   Enables DevOps engineers to analyze application resource needs and make informed business decisions, such as purchasing additional server fleets.

## Scale and Design Principles

Borg operates at an immense scale and adheres to critical design principles to meet Google's demands:

*   **Massive Scale:**
    *   Deploys approximately 4 billion containers (processes) every week across Google's infrastructure.
*   **Highly Configurable and Extensible:**
    *   Designed to accommodate the diverse and evolving requirements of virtually all Google engineers.
    *   This extensibility is crucial to prevent engineers from developing their own ad-hoc solutions, ensuring widespread adoption and centralized management.
*   **High Availability:**
    *   As core Google services like Google File System (GFS) and Spanner run on Borg, its failure would lead to a catastrophic outage for Google.
    *   Therefore, Borg is engineered for extreme reliability and availability, with extensive mechanisms in place to prevent downtime.

---

### Borg vs. Kubernetes: Key Differences

While Kubernetes was inspired by Borg, there are several key distinctions between the two systems, reflecting Borg's internal Google-specific nature and Kubernetes's open-source, community-driven development.

![Screenshot at 00:03:52](notes_screenshots/refined_Google_Borg：_Billions_of_Distributed_Linux_Containers-(1080p30)_screenshots/frame_00-03-52.jpg)

| Feature               | Google Borg                                          | Kubernetes                                                |
| :-------------------- | :--------------------------------------------------- | :-------------------------------------------------------- |
| **Source Model**      | Closed-source (internal to Google)                   | Open-source                                               |
| **Deployment Scale**  | Designed for very large clusters/cells               | Deployable at almost any scale (from single nodes to large clusters) |
| **Learning Curve**    | Less accessible, Google-specific terminology         | Easier to learn, better documentation, generic APIs       |
| **API Design**        | Google-specific or Borg-specific terms               | Generic terms, well-designed APIs                         |
| **Orchestration**     | Centralized (managed by a `Borgmaster` server)       | Decentralized (managed by a set of microservices)         |
| **Process Tagging**   | `Borglets` (equivalent to `Pods`) cannot be tagged directly; requires querying with regular expressions. | `Pods` can be tagged (e.g., "Google Maps," "production," "India"), improving queryability and debugging. |
| **Observability**     | Historically, potentially less sophisticated for external users. (Note: By 2025, Borg likely adopted many open-source observability improvements). | Enhanced observability and debugging capabilities due to tagging and rich API language. |

## Borg Internals: Job Prioritization and Constraints

Understanding Borg's internal mechanisms is crucial for appreciating its robust operation.

### Job Priorities

Every Borg job is assigned a state defined by its priority, which dictates its importance and behavior within the cluster.

![Screenshot at 00:05:26](notes_screenshots/refined_Google_Borg：_Billions_of_Distributed_Linux_Containers-(1080p30)_screenshots/frame_00-05-26.jpg)

Borg job priorities, in descending order of importance:

1.  **Monitoring:**
    *   Highest priority.
    *   These jobs are critical for system health and stability (e.g., detecting failures).
    *   They are the least likely to be preempted.

2.  **Production:**
    *   High priority, for real-time applications and critical services (e.g., Google Maps, search).
    *   **Crucial Rule:** Production jobs cannot be preempted by other jobs once they are running. This prevents cascading failures.

3.  **Batch:**
    *   Medium priority, for non-time-sensitive tasks (e.g., MapReduce jobs).
    *   Can be preempted by higher-priority (Monitoring, Production) incoming jobs.

4.  **Free:**
    *   Lowest priority, for opportunistic or non-essential tasks.
    *   Most susceptible to preemption.

**Preemption Mechanism:**
When a higher-priority job needs resources, it can preempt (kill) a lower-priority job running on a machine. The preempted job is then moved to another available machine, if possible, or rescheduled.

*   **Example:** A `Production` job arriving on a server running a `Batch` job will cause the `Batch` job to be killed and the `Production` job to take its place.
*   **Cascade Prevention:** The rule that `Production` jobs cannot be preempted is vital. Without it, a newly arriving `Monitoring` job could preempt a `Production` job, which then preempts a `Batch` job, which then preempts a `Free` job, leading to a detrimental chain reaction across the cluster.

### Job Constraints

Borg jobs can also include specific rules or constraints that guide their deployment and resource allocation.

![Screenshot at 00:06:19](notes_screenshots/refined_Google_Borg：_Billions_of_Distributed_Linux_Containers-(1080p30)_screenshots/frame_00-06-19.jpg)

*   **Types of Constraints:** Engineers can specify various requirements, such as:
    *   **Operating System Type:** The specific OS needed for the job.
    *   **IP Addresses:** Requirements related to network configuration.
    *   **Location:** Geographical region (e.g., "India").
    *   **Hardware Specifications:** Number and type of servers (e.g., "10 large servers").

*   **Allocation Challenge:** Satisfying these constraints while efficiently allocating resources across the cluster can resemble a complex linear programming problem. Borg is designed to solve these optimization challenges.

*   **Practical Usage:** While powerful, most engineers at Google do not frequently use highly complex constraints for their typical use cases, as Borg handles many generic requirements automatically.

---

### Execution Environment for Borg Jobs

![Screenshot at 00:07:22](notes_screenshots/refined_Google_Borg：_Billions_of_Distributed_Linux_Containers-(1080p30)_screenshots/frame_00-07-22.jpg)
![Screenshot at 00:07:46](notes_screenshots/refined_Google_Borg：_Billions_of_Distributed_Linux_Containers-(1080p30)_screenshots/frame_00-07-46.jpg)
![Screenshot at 00:08:10](notes_screenshots/refined_Google_Borg：_Billions_of_Distributed_Linux_Containers-(1080p30)_screenshots/frame_00-08-10.jpg)
![Screenshot at 00:08:23](notes_screenshots/refined_Google_Borg：_Billions_of_Distributed_Linux_Containers-(1080p30)_screenshots/frame_00-08-23.jpg)

Borg jobs (applications) do not typically run directly on Virtual Machines (VMs) due to their inherent slowness. Instead, they are executed within **Linux containers**, which offer a more lightweight and efficient execution environment.

Key Linux technologies underpinning Borg's containerization:
*   **`chroot jail`**: Manages security by isolating a process and its child processes to a specific directory tree, restricting access to other parts of the filesystem. This provides a form of security similar to file permissions (`chmod`).
*   **`cgroups` (Control Groups)**: Manages and allocates system resources (CPU, memory, network I/O, disk I/O) to containers. This ensures that each container receives its defined share of resources and prevents one container from monopolizing resources, thereby guaranteeing performance and stability.

**Process Management Signals:**
To restart a process, Borg uses standard Linux signals:
*   **`SIGTERM` (kill -15)**: A polite request for a process to terminate gracefully. The process can catch this signal and perform cleanup operations before exiting.
*   **`SIGKILL` (kill -9)**: A forceful termination signal that cannot be caught or ignored by the process. It immediately kills the process, forcing the container to shut down. This is used if `SIGTERM` is unsuccessful.

### Borg Cell Architecture

![Screenshot at 00:09:23](notes_screenshots/refined_Google_Borg：_Billions_of_Distributed_Linux_Containers-(1080p30)_screenshots/frame_00-09-23.jpg)

A **Borg cell** is a fundamental unit of Borg's infrastructure, comprising approximately 10,000 machines. While this might seem like a small number at Google's overall scale, it represents a substantial cluster.

Within each Borg cell:
*   **`Borgmaster`**: This is the central server responsible for managing the cell. It configures `Borglets` and assigns tasks.
    *   **Single Point of Failure (SPOF)**: The `Borgmaster` is a single point of failure within a cell. However, Borg's design ensures that if the `Borgmaster` goes down, existing `Borglets` (running tasks) continue to function, minimizing impact on availability.
*   **`Borglets`**: These are the equivalent of `Pods` in Kubernetes. They represent the actual running tasks or applications. The `Borgmaster` receives commands (e.g., "execute this application on 5,000 machines") and assigns these tasks to `Borglets` across the cell.

### Task Assignment: The Bin Packing Problem

Assigning tasks to machines within a Borg cell is a complex optimization challenge, often referred to as a **bin packing problem**. The `Borgmaster` aims to spread applications across different power domains and regions to ensure high fault tolerance.

Consider an incoming application (`App3`) that requires specific compute resources, and two existing machines (`Machine A` and `Machine B`) with available capacity:

| Machine    | Running Apps | Available Compute |
| :--------- | :----------- | :---------------- |
| Machine A  | `App1`       | 60%               |
| Machine B  | `App2`       | 30%               |

If `App3` requires 30% compute:

1.  **"Best Fit" Strategy:**
    *   **Concept:** Assign `App3` to `Machine B` (which has 30% available), resulting in `Machine B` running at 100% capacity. This maximizes machine utilization.
    *   **Pros:** Efficient use of resources.
    *   **Cons:**
        *   **Slower Assignment:** Requires searching for the *perfect* or *closest* fit.
        *   **Risk of Over-provisioning/Crashes:** If `App3` (like many MapReduce jobs) understates its resource needs and actually requires 35%, it will crash on `Machine B`. This directly impacts resilience.
        *   **Fragmentation:** If `Machine B` is now full, and `Machine A` has 60% remaining, a subsequent app requiring 40% might not fit anywhere if other machines are also fragmented.

2.  **"Fast Assignment" / "First Fit" Strategy:**
    *   **Concept:** Assign `App3` to the first available machine that can accommodate it, for example, `Machine A` (which has 60% available).
    *   **Pros:** Faster task assignment.
    *   **Cons:**
        *   **Potential for Wasted Compute:** `Machine A` would still have 30% remaining, potentially leading to less efficient overall cluster utilization if this pattern repeats.
        *   **Suboptimal Placement:** Does not prioritize maximizing individual machine utilization.

**Borg's Hybrid Approach:**
Borg adopts a hybrid approach, balancing the need for quick task assignment with efficient resource utilization and resilience. It aims to place applications in locations that have *some* space remaining, rather than strictly seeking the absolute best fit. This strategy prioritizes faster assignment and reduces the risk of crashes due to slight resource requirement underestimations, even if it means slightly less "perfect" bin packing in some instances.
</REFINEDNOTES>

---

### Borg Naming Service (BNS)

![Screenshot at 00:11:26](notes_screenshots/refined_Google_Borg：_Billions_of_Distributed_Linux_Containers-(1080p30)_screenshots/frame_00-11-26.jpg)
![Screenshot at 00:12:39](notes_screenshots/refined_Google_Borg：_Billions_of_Distributed_Linux_Containers-(1080p30)_screenshots/frame_00-12-39.jpg)

Once an application is assigned and running on a `Borglet` (e.g., utilizing 40% or 50% of its assigned resources), an entry is added to the **Borg Naming Service (BNS)**. BNS functions similarly to a Domain Name System (DNS), providing a server-to-IP mapping for all running `Borglets`.

The BNS naming convention allows for precise identification of `Borglets`:
*   **Format Example:** `30.app1.user-id.cell-id.borg.google.com`
    *   `30`: Represents the 30th server instance of the application.
    *   `app1`: The name of the application.
    *   `user-id`: The identifier of the user who initiated the task.
    *   `cell-id`: The specific Borg cell where the `Borglet` is running.
    *   `borg.google.com`: A standard domain suffix within Google's internal network.

This structured naming allows for reverse regular expression (`regex`) queries to retrieve information. For instance, an engineer can query BNS to "get all servers for this application, initiated by this user in this cell ID."

### Metadata Storage: Chubby

![Screenshot at 00:14:04](notes_screenshots/refined_Google_Borg：_Billions_of_Distributed_Linux_Containers-(1080p30)_screenshots/frame_00-14-04.jpg)

All metadata related to `Borglet` execution is stored in **Chubby**.
*   **Chubby's Role:** It is a Paxos-based persistent store used by Google, primarily serving as a distributed lock service and a consistent key-value store.
*   **Stored Metadata:** Chubby stores various states and health information for `Borglets`, such as:
    *   **Pending:** Task awaiting assignment to a `Borglet`.
    *   **Running:** Task actively executing on a `Borglet`.
    *   **Stopped:** Task that has been terminated.
    *   **Health Status:** The operational health of individual `Borglets`.
*   **Evolution:** While Chubby provides high consistency for its writes, the advent of Google Spanner (a highly consistent, highly available global database) raises questions about whether `Borgmaster` has transitioned to using Spanner for metadata storage, though this is not confirmed in the paper.

### Borglet Log Management

`Borglets` store their application logs in local files on the host machine, rather than directly sending them to a distributed file system like Google File System (GFS).
*   **Log Rotation and Deletion:** These local log files are periodically rotated and eventually deleted.
*   **Retention Policy:** Logs are typically purged within one to two days after a `Borglet` has finished processing an application or been migrated. This implies a short retention period for local logs.

### Monitoring and Observability

Borg leverages specialized systems for monitoring and observability:
*   **Monitoring System:**
    *   Historically, **Borgmon** was used for monitoring.
    *   Currently, **Monarch** is Google's time-series data store for metrics, providing comprehensive observability into system performance and health.
*   **Business Intelligence:**
    *   Application metrics are also sent to **Dremel**, a query service that allows engineers to run SQL queries.
    *   **Use Cases:** Dremel enables data-driven business decisions, such as:
        *   Determining required capacity.
        *   Identifying applications consuming the most compute power.

### Resource Exhaustion Management

When a machine (hosting `Borglets`) experiences resource exhaustion (e.g., runs out of memory or CPU), Borg takes proactive measures to maintain stability:
*   **Memory Exhaustion:** If a machine runs out of memory, Borg immediately begins killing processes. The killing order is strictly based on priority, starting with the lowest-priority jobs:
    1.  `Free` jobs
    2.  `Batch` jobs
    3.  (Production jobs are not preempted due to memory exhaustion on the same machine unless absolutely critical and unavoidable, but the primary mechanism targets lower priorities first).
*   **Temporary Resource Issues (e.g., 100% CPU usage):** For temporary spikes, Borg initially waits for a short period to see if the situation improves. If resource levels do not normalize, processes are killed, again starting from the lowest priority upwards.

### Borgmaster High Availability

Although the `Borgmaster` is a single point of failure within a cell (as `Borglets` cannot receive new tasks if it dies), its high availability is ensured through redundancy:
*   **Replicas:** There are five in-memory replicas of the `Borgmaster`.
*   **Leader Election:** These replicas use the **Paxos consensus algorithm** to elect a leader among themselves. This ensures that even if the active `Borgmaster` fails, a new leader can be quickly chosen, and the system can continue accepting new tasks with minimal interruption.
</REFINEDNOTES>

---

### Borgmaster High Availability (Continued)

![Screenshot at 00:15:29](notes_screenshots/refined_Google_Borg：_Billions_of_Distributed_Linux_Containers-(1080p30)_screenshots/frame_00-15-29.jpg)

The five in-memory replicas of the `Borgmaster` are synchronized. In the event of a `Borgmaster` failure, a new leader is elected using **Paxos consensus**. This new leader then takes over the provisioning of `Borglets`. All state information for the `Borgmaster` replicas is persistently stored in **Chubby**, ensuring that a newly elected leader can restore its state and continue operations seamlessly.

### Optimization Strategies for Task Assignment

Borg employs several caching and classification strategies to optimize the speed and efficiency of task assignment:

![Screenshot at 00:17:22](notes_screenshots/refined_Google_Borg：_Billions_of_Distributed_Linux_Containers-(1080p30)_screenshots/frame_00-17-22.jpg)

1.  **Caching `Borglet` Configuration and Scores:**
    *   **Static Parameters:** Each `Borglet` (representing a server or machine) has static parameters such as its region, physical size, power outlet connection, and other hardware attributes.
    *   **Pre-computed Scores:** These parameters, along with pre-computed "scores" indicating a `Borglet`'s suitability for various tasks, are heavily cached within the `Borgmaster`.
    *   **Benefit:** This caching allows the `Borgmaster` to quickly make assignment decisions without re-computing `Borglet` suitability every time, significantly speeding up the process of finding an appropriate `Borglet` for an incoming application. Changes to these cached values only occur if the physical server configuration changes.

2.  **Application Classes:**
    *   Instead of evaluating each application's specific requirements individually, Borg categorizes applications into **classes**.
    *   **Examples of Classes:** Applications might be classified as:
        *   **IO-intensive**
        *   **Memory-intensive**
        *   **CPU-intensive**
    *   **Benefit:** By constraining the number of variations, `Borgmaster` can quickly match an application's class with a suitable `Borglet` that has the necessary resources and characteristics for that class, further optimizing assignment.

3.  **Library Caching on `Borglets`:**
    *   When an application is to be assigned, Borg prioritizes `Borglets` that already possess the required libraries for that application. This is conceptually similar to how build systems like Bazel cache libraries.
    *   **Benefit:** This strategy drastically reduces application start times. For instance, deployment time can drop from 25 seconds to just 5 seconds. This makes deploying applications across thousands of servers a very fast and efficient process.

### Conclusion: The Enduring Impact of Google Borg

Google Borg is a testament to sophisticated system design, remaining a core component of Google's infrastructure for over two decades.
*   **Widespread Use:** It powers 98% of all servers at Google.
*   **Core Concepts:** Its fundamental architecture revolves around:
    *   **Cells:** Large clusters of machines.
    *   **`Borgmaster`:** The central controller for a cell.
    *   **`Borglets`:** The execution units (containers) running applications.
*   **Pioneering Innovation:** Developed in 2005, Borg introduced advanced concepts that were uncommon at the time, such as:
    *   Containerization logic.
    *   Sophisticated auto-scaling.
    *   Robust cross-region fault tolerance.

Borg's enduring success highlights the foresight and engineering prowess of Google's principal engineers who designed a system that has profoundly influenced modern cluster management, most notably through its open-source descendant, Kubernetes.

---

### Borgmaster High Availability (Continued)

The five in-memory replicas of the `Borgmaster` are synchronized. In the event of a `Borgmaster` failure, a new leader is elected using **Paxos consensus**. This new leader then takes over the provisioning of `Borglets`. All state information for the `Borgmaster` replicas is persistently stored in **Chubby**, ensuring that a newly elected leader can restore its state and continue operations seamlessly.

### Optimization Strategies for Task Assignment

Borg employs several caching and classification strategies to optimize the speed and efficiency of task assignment:

1.  **Caching `Borglet` Configuration and Scores:**
    *   **Static Parameters:** Each `Borglet` (representing a server or machine) has static parameters such as its region, physical size, power outlet connection, and other hardware attributes.
    *   **Pre-computed Scores:** These parameters, along with pre-computed "scores" indicating a `Borglet`'s suitability for various tasks, are heavily cached within the `Borgmaster`.
    *   **Benefit:** This caching allows the `Borgmaster` to quickly make assignment decisions without re-computing `Borglet` suitability every time, significantly speeding up the process of finding an appropriate `Borglet` for an incoming application. Changes to these cached values only occur if the physical server configuration changes.

2.  **Application Classes:**
    *   Instead of evaluating each application's specific requirements individually, Borg categorizes applications into **classes**.
    *   **Examples of Classes:** Applications might be classified as:
        *   **IO-intensive**
        *   **Memory-intensive**
        *   **CPU-intensive**
    *   **Benefit:** By constraining the number of variations, `Borgmaster` can quickly match an application's class with a suitable `Borglet` that has the necessary resources and characteristics for that class, further optimizing assignment.

3.  **Library Caching on `Borglets`:**
    *   When an application is to be assigned, Borg prioritizes `Borglets` that already possess the required libraries for that application. This is conceptually similar to how build systems like Bazel cache libraries.
    *   **Benefit:** This strategy drastically reduces application start times. For instance, deployment time can drop from 25 seconds to just 5 seconds. This makes deploying applications across thousands of servers a very fast and efficient process.

### Conclusion: The Enduring Impact of Google Borg

![Screenshot at 00:18:24](notes_screenshots/refined_Google_Borg：_Billions_of_Distributed_Linux_Containers-(1080p30)_screenshots/frame_00-18-24.jpg)

Google Borg is a testament to sophisticated system design, remaining a core component of Google's infrastructure for over two decades.
*   **Widespread Use:** It powers 98% of all servers at Google.
*   **Core Concepts:** Its fundamental architecture revolves around:
    *   **Cells:** Large clusters of machines.
    *   **`Borgmaster`:** The central controller for a cell.
    *   **`Borglets`:** The execution units (containers) running applications.
*   **Pioneering Innovation:** Developed in 2005, Borg introduced advanced concepts that were uncommon at the time, such as:
    *   Containerization logic.
    *   Sophisticated auto-scaling.
    *   Robust cross-region fault tolerance.

Borg's enduring success highlights the foresight and engineering prowess of Google's principal engineers who designed a system that has profoundly influenced modern cluster management, most notably through its open-source descendant, Kubernetes.

---

