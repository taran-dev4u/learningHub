# Requirements & Scope

<div class="section-intro">
  <strong>The 10-Minute Foundation:</strong> Before drawing a single box or debating SQL vs NoSQL, a Senior Engineer extracts explicit architectural boundaries. This guide walks through the structured framework for functional requirements, non-functional thresholds (latency, consistency, availability), and high-scoring clarifying questions.
</div>

> [!ANSWER30]
> System design interviews are won or lost in the first 10 minutes. Always split requirements into **Functional** (*"what the user actually does"*) and **Non-Functional** (*"how fast, reliable, and scalable"*). Never assume: state your assumptions (e.g., 100M DAU, 5,000 QPS peak) and get explicit verbal sign-off from your interviewer before drawing architecture.

## Overview

Welcome to the very first step of your System Design journey! Before we draw a single box or talk about databases and servers, we need to know **what** we are building and **how well** it needs to perform. 

This page covers the critical first 10 minutes of any System Design interview: extracting requirements, defining scale, understanding the boundary between HLD and LLD, and asking the right questions.

<ul class="hsteps">
  <li>
    <span class="hsteps__no">01</span>
    <strong>Clarify & Scope</strong>
    Identify primary actors, core flows, and eliminate secondary features.
  </li>
  <li>
    <span class="hsteps__no">02</span>
    <strong>Capacity Sizing</strong>
    Estimate read/write QPS, storage over 5 years, and memory cache footprints.
  </li>
  <li>
    <span class="hsteps__no">03</span>
    <strong>High-Level Design</strong>
    Draw end-to-end component flow: DNS, CDN, Load Balancers, API gateways, and DBs.
  </li>
  <li>
    <span class="hsteps__no">04</span>
    <strong>Bottlenecks & Scale</strong>
    Address single points of failure, partition schemes, and caching tiers.
  </li>
</ul>

---

## Functional requirements checklist

**Functional requirements define the core behaviors of the system.** They answer the question: *"What should the system actually do for the user?"*

If we are designing Twitter, a functional requirement is: *"Users should be able to post a tweet."*
It is **not**: *"The system should handle 10,000 tweets per second."*

> [!SCOPE]
> **The Core Flows Rule of Three:**
> In a 45-minute interview, you cannot design all of Amazon. You must aggressively narrow down the scope to 2 or 3 **Core Flows**:
> 1. **Identify the Primary Actors:** Who uses this system? Normal users? Content creators? Internal automated workers?
> 2. **Identify Core Read & Write Flows:**
>    - **Read flows:** "Users can view a chronological home timeline of tweets."
>    - **Write flows:** "Users can publish a 140-character text tweet with optional media."
> 3. **Identify Explicit Non-Goals:** Explicitly eliminate scope traps upfront (e.g., "We will exclude search indexation, direct messaging, and recommendation models for this round").

<!-- break -->

> [!TIP]
> **Teacher's Advice:** Always confirm the read and write flows explicitly. Systems are designed fundamentally differently depending on whether they are "Read-Heavy" (99:1 read/write ratio like Twitter or Reddit) or "Write-Heavy" (like IoT telemetry logging or analytics ingestion).

---

## Non-functional requirements

If functional requirements answer **"What does the system do?"**, Non-Functional Requirements (NFRs) answer **"How well does the system do it?"**

Your entire architecture—from the database to the load balancer—will be dictated entirely by these NFRs.

### The Big Six NFRs
1. **Scale (Traffic & Data):** QPS (Queries Per Second) and total Storage (Megabytes vs Petabytes).
2. **Latency (Performance):** How fast must the system respond? (e.g., P99 < 100ms for web, < 10ms for financial order books).
3. **Availability:** What percentage of the time must the system be running? (Measured in "Nines" like 99.99%).
4. **Consistency:** Does every read guarantee it sees the most recent write? (Strong vs Eventual consistency).
5. **Durability:** Once data is saved, what is the probability it is preserved across power loss or disk failure?
6. **Compliance / Security:** GDPR rules, PCI-DSS compliance, zero-trust authentication.

> [!TRADEOFF]
> **Availability vs Consistency (CAP Trade-off):**
> You cannot build a system that simultaneously guarantees zero latency, 100% availability, absolute ACID consistency, and infinite linear scale across partitions.
> - **For High-Volume Social Feeds (Twitter/Instagram):** Favor **High Availability (AP)** with **Eventual Consistency**. Seeing a friend's post 2 seconds late is harmless; downtime causes user churn.
> - **For Financial Transactions & Checkouts:** Invert the priority. Favor **Strong Consistency (CP)**. Never allow double-spending or stale inventory balances, even if requests must queue during network partitions.

### Architectural SLA Impact Matrix

| Requirement Attribute | Target SLA Benchmark | Architectural Implementation Pattern |
| :--- | :--- | :--- |
| **P99 Read Latency** | < 50ms | Edge CDN caching + Distributed in-memory Redis cluster |
| **System Availability** | 99.99% ("Four Nines" &le; 52m downtime/yr) | Multi-AZ active-active deployment + automatic health checks |
| **Write Scalability** | 50,000+ QPS | Async message broker (Apache Kafka) + Horizontal worker pools |
| **Data Durability** | 99.999999999% ("11 Nines") | Object store with multi-region erasure coding (AWS S3) |
| **Read/Write Decoupling** | Read-Heavy (100:1) | CQRS pattern with Read Replicas and Write-Ahead Log (WAL) |

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
Start at HLD. Draw the big boxes. If the interviewer points to a specific box (e.g., *"How would you actually code this Rate Limiter token bucket?"*) — **You just switched to LLD.**

The perfect bridge between HLD and LLD is the **API Contract**. Defining endpoints satisfies HLD (how services communicate) and touches LLD (the exact JSON payload).

---

## Clarifying questions that score points

The biggest mistake candidates make is immediately drawing a database. A Senior Engineer does not write code until they understand the constraints. They ask **Clarifying Questions**.

> [!LEARN]
> **The Senior Engineer's Clarifying Checklist:**
> 1. **User Geography & Scale:** *"Are we targeting a global user base with multi-region latency demands (100M DAU), or is this a regional service?"*
> 2. **Read vs Write Ratio:** *"Is this system predominantly Read-Heavy (like Twitter timeline) or Write-Heavy (like sensor telemetry)?"*
> 3. **Data Freshness SLA:** *"Does the data require immediate ACID consistency, or is Eventual Consistency within seconds acceptable?"*
> 4. **Media Payloads:** *"Are we handling lightweight JSON text payloads, or heavy binary media streaming (images/4K video)?"*
> 5. **Retention & Archival:** *"What is the data retention policy? Do we retain records indefinitely or archive cold records after 90 days?"*

> [!NOTE]
> **Takeaway:** Never design in a vacuum. Start your interview by asking the Big 5 questions, confirm your Functional and Non-Functional requirements, and *then* pick up the marker.
