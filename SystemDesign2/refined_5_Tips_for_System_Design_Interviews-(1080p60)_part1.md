# 5 Tips For System Design Interviews (1080P60) - Part 1

# System Design Interview Tips: Do's and Don'ts

This guide provides essential tips for approaching system design interviews, whether you're preparing for an upcoming interview or aiming to maximize your practice sessions.

## 1. Do Not Go Into Detail Prematurely

A common mistake in system design interviews is diving into excessive detail too early in the discussion.

### The Problem
When drawing out initial components like clients, services, and databases (as seen in ![Screenshot at 00:00:43](notes_screenshots/refined_5_Tips_for_System_Design_Interviews-(1080p60)_screenshots/frame_00-00-43.jpg) and ![Screenshot at 00:01:16](notes_screenshots/refined_5_Tips_for_System_Design_Interviews-(1080p60)_screenshots/frame_00-01-16.jpg)), candidates often prematurely elaborate on specific aspects.
*   **Examples of Premature Detail:**
    *   Immediately specifying communication protocols (e.g., "I'm going to use HTTP protocol externally, and TCP internally").
    *   Over-detailing database interactions (e.g., "We'll use two databases, one for read-only and one for write-only").
    *   Adding components like a gateway without first establishing the broader system overview.

### Consequences
*   **Wasted Time:** You spend a significant portion of the interview discussing granular details that might not be relevant or desired by the interviewer.
*   **Lack of Feedback:** The interviewer might not interrupt you even if you're going down an undesirable path. They may let you continue until you make a mistake.
*   **Backtracking:** Realizing a mistake later forces you to backtrack, which is a negative signal. In a real-world scenario, backtracking after significant design effort costs time and money.
*   **Missed Opportunity:** You miss the chance for the interviewer to guide you or ask clarifying questions, which is crucial for demonstrating your collaborative problem-solving skills.

### Solution
*   **High-Level Overview First:** Present your initial design at a high level.
*   **Pause and Seek Feedback:** After outlining a component or interaction, pause and wait for the interviewer's response or questions. This allows them to direct the conversation.
    *   Example: Instead of immediately detailing protocols, state: "The client will communicate with these services using a protocol. I prefer HTTP due to its wide usage and ease for clients." Then, wait for a response.
*   **Detail on Request:** Only delve into deeper specifics when explicitly prompted by the interviewer or when you're certain it's the next logical step to clarify the system definition. For databases, this might mean drawing an entity-relationship diagram when asked for details.

## 2. Don't Have a Set Architecture in Mind

Approaching a system design problem with a preconceived architectural pattern, regardless of the requirements, can be detrimental.

### The Problem
*   **Rigidity:** Relying on a "favorite" architecture (e.g., MVC, event-driven, publisher-subscriber model) that you've read about or used previously, and trying to force the given requirements into it.
*   **Ignoring Requirements:** This approach prioritizes a specific architecture over the actual problem constraints and functional/non-functional requirements.
    *   Example: Insisting on a publisher-subscriber model for all inter-service communication when it might not be the most optimal solution for the given scenario.

### Consequences
*   **Suboptimal Design:** The chosen architecture might not be the best fit, leading to inefficiencies, increased complexity, or difficulty in meeting specific requirements.
*   **Interviewer Challenge:** Interviewers often intentionally introduce new or changing requirements to test your flexibility and adaptability. If you're too rigid, you'll struggle to adjust your design.
*   **Demonstrates Inflexibility:** This shows an inability to critically evaluate options based on the problem statement, which is a key skill for a system designer.

### Solution
*   **Start with Requirements:** Always begin by thoroughly understanding and clarifying the problem's functional and non-functional requirements.
*   **Evaluate Options:** Based on the requirements, consider various architectural patterns and discuss their pros and cons in the context of the problem.
*   **Be Flexible:** Be prepared to adapt your design as requirements evolve or as the interviewer introduces new constraints. Your goal is to design the *best* system for the *given* problem, not to implement a pre-selected pattern.
*   **Iterative Design:** System design is often an iterative process. Be ready to revise your initial ideas based on feedback and new information.

---

### The Problem (Continued)
*   **Time Constraints:** Often, candidates fall into this trap due to limited preparation time, leading them to rely on generalized blog post architectures rather than tailoring solutions to specific problems. This can lead to the belief that a "silver bullet" architecture fits all scenarios, which is not true (e.g., WhatsApp and Uber have vastly different architectures).

## 3. Keep It Simple, Stupid (KISS Principle)

Avoid over-complicating a specific part of your system design.

### The Problem
*   **Narrow Focus:** Getting excessively detailed about a single service or component, losing sight of the overall system.
    *   Example: Adding a dedicated heartbeat server and a separate analytics database *just* for one service (as illustrated in ![Screenshot at 00:06:47](notes_screenshots/refined_5_Tips_for_System_Design_Interviews-(1080p60)_screenshots/frame_00-06-47.jpg) and ![Screenshot at 00:06:58](notes_screenshots/refined_5_Tips_for_System_Design_Interviews-(1080p60)_screenshots/frame_00-06-58.jpg)), rather than considering how these functionalities could be implemented system-wide.
*   **Imbalanced Design:** If one part of your diagram becomes disproportionately large or complex compared to others, it's a red flag. ![Screenshot at 00:06:58](notes_screenshots/refined_5_Tips_for_System_Design_Interviews-(1080p60)_screenshots/frame_00-06-58.jpg) visually represents this imbalance.

### Consequences
*   **Over-engineering:** Introducing unnecessary complexity for a specific component that could be handled more simply or by a shared system-level component.
*   **Loss of Perspective:** A narrow focus prevents you from seeing opportunities to generalize components or extend functionalities across the entire system.
*   **Suboptimal Overall Design:** The system becomes harder to manage, scale, and understand due to localized over-complexity.

### Solution
*   **Step Back Regularly:** Periodically review the entire architecture to maintain a holistic view.
*   **Identify Generalizable Components:** Look for common functionalities (e.g., analytics, monitoring, logging) that can be extracted and provided as a shared service across the system, rather than replicated per component.
*   **Balance in Diagram:** If your diagram shows one part as significantly more detailed or larger than others, it's an indicator that you might need to simplify that part or expand on other neglected areas.

## 4. Justify Your Points

This is one of the most common and critical mistakes in system design interviews.

### The Problem
*   **Unbacked Statements:** Making design decisions without providing a clear rationale.
    *   Example: Stating "I'll use a NoSQL database, specifically Cassandra" without explaining *why* Cassandra is suitable for the given requirements.
*   **Avoiding Silence:** Candidates often feel compelled to speak continuously to fill awkward silences during the interview, leading to half-hearted or ill-considered suggestions.
*   **Trend-Following:** Suggesting a technology merely because it's popular or "cool" (e.g., "Cassandra is really cool, so why not add that?").

### Consequences
*   **Negative Impression:** It indicates a lack of deep understanding or critical thinking.
*   **Weak Design:** Without justification, the design decision might be inappropriate for the problem, leading to a negative evaluation.
*   **Missed Opportunity to Impress:** Justifying your choices demonstrates your thought process, understanding of trade-offs, and ability to make informed decisions.

### Solution
*   **Think Before Speaking:** Always consider the "why" behind every design choice.
*   **Be Prepared to Explain:** For every component, technology, or pattern you propose, be ready to articulate:
    *   What problem it solves.
    *   Why it's a good fit for the current requirements.
    *   Its advantages and disadvantages compared to alternatives.
*   **Embrace Silence:** A brief pause to formulate a well-reasoned answer is always better than an unjustified, rushed statement.

## 5. Be Aware of Current Technologies

Familiarity with specific, off-the-shelf technologies demonstrates practical knowledge and efficiency.

### The Benefit
*   **Knowledge Demonstration:** Naming concrete technologies (as seen in ![Screenshot at 00:04:23](notes_screenshots/refined_5_Tips_for_System_Design_Interviews-(1080p60)_screenshots/frame_00-04-23.jpg)) shows that you are knowledgeable about industry standards and available solutions.
*   **Efficiency:** Using existing, proven technologies (instead of suggesting building custom solutions for common problems) implies:
    *   **Lesser Development Time:** Reduces the effort required for implementation.
    *   **Lesser Testing Time:** Leverages battle-tested solutions, reducing the need for extensive custom testing.
    *   **Reduced Costs:** Often, using mature, off-the-shelf solutions is more cost-effective than building from scratch.

### Examples of Specific Technologies
*   **NoSQL Databases:** Cassandra, Amazon DynamoDB
*   **Relational Databases:** MySQL, PostgreSQL
*   **Load Balancers:** Elastic Load Balancer (ELB - from AWS architecture)
*   **Heartbeat/Coordination Services:** Apache ZooKeeper
*   **Message Queues:** RabbitMQ, Apache Kafka

By demonstrating awareness of these tools, you show an interviewer that you can leverage existing solutions to build a robust system efficiently.

These five do's and don'ts are crucial for success in system design interviews, helping you present a thoughtful, well-justified, and practical design.

---

### Three Pillars of System Design Interview Success

Beyond the specific do's and don'ts, a successful system design interview hinges on three fundamental pillars:

1.  **Clarity of Thought:**
    *   **Importance:** The ability to articulate your thoughts and design decisions clearly to the interviewer is paramount.
    *   **Real-World Relevance:** This skill directly translates to effective communication with your teammates in a professional setting, which is a significant asset.

2.  **Flexibility:**
    *   **Importance:** As discussed previously, avoid being rigid with a preconceived architecture. Be prepared to adapt your design as new requirements or constraints emerge.
    *   **Adaptability:** The ability to "roll with the punches" and modify your system in response to interviewer feedback or changing scenarios is a critical design skill.

3.  **Knowledge:**
    *   **Importance:** Demonstrating awareness of current and relevant technologies and architectural patterns.
    *   **Practical Application:** This includes knowing appropriate off-the-shelf solutions and understanding how to apply them effectively to build a robust system.

![Screenshot at 00:07:20](notes_screenshots/refined_5_Tips_for_System_Design_Interviews-(1080p60)_screenshots/frame_00-07-20.jpg)

The image above summarizes the whiteboard content, visually reinforcing the discussion about various system components and technologies, which ties into the "Knowledge" pillar. These three pillars—Clarity, Flexibility, and Knowledge—form the foundation for successfully designing a system from scratch in an interview setting.

---

