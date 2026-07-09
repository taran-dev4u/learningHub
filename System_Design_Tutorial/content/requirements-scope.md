# Requirements & Scope

## Overview
Welcome to the very first step of your System Design journey! Before we draw a single box or talk about databases and servers, we need to know **what** we are building and **how well** it needs to perform. 

This page covers the critical first 10 minutes of any System Design interview: extracting requirements, defining scale, understanding the boundary between HLD and LLD, and asking the right questions.

---

## Functional requirements checklist

**Functional requirements define the core behaviors of the system.** They answer the question: *"What should the system actually do for the user?"*

If we are designing Twitter, a functional requirement is: *"Users should be able to post a tweet."*
It is **not**: *"The system should handle 10,000 tweets per second."*

### The "Core Flows" Checklist
In a 45-minute interview, you cannot design all of Amazon. You must aggressively narrow down the scope to 2 or 3 **Core Flows**.

1. **Identify the Primary Actors:** Who uses this system? Normal users? Creators? Internal admins?
2. **Identify the Core Actions (Inputs & Outputs):**
   - **Read flows:** "Users can view a timeline of tweets."
   - **Write flows:** "Users can publish a 140-character text tweet."
3. **Identify Edge Cases & Features to Exclude:**
   - explicitly declare what you are **not** building. (e.g., "We will exclude analytics tracking for now.")

> [!TIP]
> **Teacher's Advice:** Always confirm the read and write flows explicitly. Systems are usually designed entirely differently depending on whether they are "Read-Heavy" or "Write-Heavy".

---

## Non-functional requirements

If functional requirements answer **"What does the system do?"**, Non-Functional Requirements (NFRs) answer **"How well does the system do it?"**

Your entire architecture—from the database to the load balancer—will be dictated entirely by these NFRs.

### The Big Six NFRs
1. **Scale (Traffic & Data):** QPS (Queries Per Second) and total Storage (Megabytes vs Petabytes).
2. **Latency (Performance):** How fast must the system respond? (e.g., 500ms for web, <10ms for trading).
3. **Availability:** What percentage of the time must the system be running? (Measured in "Nines" like 99.99%).
4. **Consistency:** Does every read guarantee it sees the most recent write? (Strong vs Eventual consistency).
5. **Durability:** Once data is saved, what is the probability it is lost forever?
6. **Compliance / Security:** GDPR rules, PCI compliance, HIPAA.

### The Ultimate Trade-off: You Can't Have It All
You cannot build a system that has 0 latency, 100% availability, absolute strong consistency, and infinite scale. 

| If you want... | You must usually sacrifice... | By doing... |
| :--- | :--- | :--- |
| **High Availability** | **Strong Consistency** | Using async replication. Nodes might have slightly stale data for a few milliseconds, but the system stays up. |
| **Low Latency** | **Fresh Data** | Aggressively caching data. The data is retrieved instantly, but it might be outdated. |

---

## HLD vs LLD: when to switch levels

System Design interviews fall into two categories: **High-Level Design (HLD)** and **Low-Level Design (LLD)**.

### High-Level Design (HLD)
The **"10,000-foot view"**. You don't care about specific `class` definitions. You care about how massive systems talk to each other over a network.
- **Topics:** Load balancers, Databases, Sharding, Microservices, Network Protocols.

### Low-Level Design (LLD)
The **"Microscopic view"**. It focuses on the internal code structure of a *single component*.
- **Topics:** Classes, Interfaces, Design Patterns (Factory, Strategy), Database Schemas.

### The Boundary: When to Switch
Start at HLD. Draw the big boxes. If the interviewer points to a specific box (e.g., "The Rate Limiter") and says, *"How would you actually code this box?"* — **You just switched to LLD.**

The perfect bridge between HLD and LLD is the **API Contract**. Defining endpoints satisfies HLD (how services communicate) and touches LLD (the exact JSON payload).

---

## Clarifying questions that score points

The biggest mistake candidates make is immediately drawing a database. A Senior Engineer does not write code until they understand the constraints. They ask **Clarifying Questions**.

### The "Big 5" Clarifying Questions Checklist
State your assumption and ask for confirmation. Do not ask open-ended questions.

1. **User Geography & Scale:** *"Are we targeting a global scale (100M DAU), or is this an internal tool for 1k employees?"*
2. **Read vs Write Ratio:** *"Is this system highly Read-Heavy (Twitter) or Write-Heavy (IoT logs)?"*
3. **Data Freshness & Consistency:** *"Does the data need to be strongly consistent, or is Eventual Consistency okay?"*
4. **Media Types & Storage:** *"Are we storing just text metadata, or heavy media files like videos?"*
5. **Historical Data Retention:** *"Do we need to store user data forever, or can we archive messages older than 30 days?"*

> [!NOTE]
> **Summary:** Never design in a vacuum. Start your interview by asking the Big 5 questions, confirm your Functional and Non-Functional requirements, and *then* pick up the marker.
