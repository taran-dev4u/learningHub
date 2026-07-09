# Senior Engineer Signals

## Overview
How does an interviewer decide if you get a **Mid-Level (L4)** offer or a **Senior (L5/L6)** offer? 

They don't just look at whether your design "works." Any junior engineer can draw a load balancer pointing to a web server pointing to a database. Interviewers are looking for specific **behavioral and technical signals** during the 45-minute session.

This module covers the exact behaviors that scream "Senior Engineer."

---

## Articulate trade-offs explicitly ('strong consistency costs us latency')

A Junior engineer says: *"I will use a relational database because it's good."*
A Senior engineer says: *"I will use a relational database because we need ACID transactions for payments. The trade-off is that it will be harder to horizontally scale later, and our write latency will be higher due to locking, but for this specific financial use case, consistency outweighs availability."*

### The "No Free Lunch" Rule
Every architectural decision has a downside. If you cannot explain the downside of your own design, the interviewer assumes you don't actually understand the technology.

| Choice | Pro | Trade-off (The Cost) |
| :--- | :--- | :--- |
| **Microservices** | Independent deployment, separate scaling | Network overhead, complex debugging, distributed transactions |
| **NoSQL (Cassandra)** | Massive write throughput, horizontal scaling | Eventual consistency, no complex JOINs |
| **Redis Cache** | Blazing fast reads (~1ms) | Data volatility, cache invalidation complexity |

---

## Quantify everything — QPS, P99 latency budget, GB/month storage

Senior engineers do not use words like "fast" or "big." They use numbers.

When asked to design a chat application:
- **Junior:** "We need a fast database because there are a lot of messages."
- **Senior:** "Assuming 50 million DAU sending 20 messages a day, we are looking at 11,500 write QPS on average, peaking at ~35,000 QPS. We need a datastore optimized for high write throughput, like Cassandra or HBase."

If you don't calculate your QPS and storage requirements in the first 10 minutes, you are flying blind.

---

## Failure-first thinking — 'what if the DB dies?' before happy path

Junior engineers design for the "Happy Path" where the network is 100% reliable and servers never crash.
Senior engineers know that **everything fails all the time.**

When drawing your architecture, proactively tell the interviewer what happens when a component dies.
> *"I've placed a Load Balancer here. However, a single Load Balancer is a single point of failure (SPOF). In a production environment, I would run two Load Balancers in an Active-Passive configuration using a heartbeat protocol (like Keepalived) so the backup takes over instantly if the primary dies."*

**Key Failure Modes to discuss:**
1. What if a datacenter loses power? (Cross-region replication)
2. What if a celebrity tweets and traffic spikes 100x in one minute? (Thundering herd, caching)
3. What if a downstream API takes 10 seconds to respond? (Circuit breakers, timeouts)

---

## Operational awareness — monitoring, deploys, on-call, rollback strategy

Designing the system is only 10% of a software engineer's job. Maintaining it in production is the other 90%.

If you have 5 minutes left in the interview, bring up **Observability**:
- *"To ensure this system stays healthy, I would emit metrics for API latency and error rates to a system like Datadog or Prometheus."*
- *"We need distributed tracing (like Jaeger) because a single request will hit 5 different microservices, and we need to know exactly where a bottleneck occurs."*

Discussing CI/CD pipelines, dark launches, and feature flags proves you have scars from production outages.

---

## Drive the interview — don't wait for the interviewer to fill silence

An L5/L6 interview is a **collaboration between peers**, not an exam.

- **Junior:** Answers the question, then waits quietly for the next question.
- **Senior:** Takes control of the whiteboard. Asks clarifying questions. Suggests deep dives.

**Example of driving:**
*"I've outlined the high-level API flow. We have 20 minutes left. I think the most complex part of this system is the real-time websocket connection management. Would you like me to deep dive into how we can fan-out those connections across multiple servers?"*

> [!NOTE]
> **Common Beginner Mistake:** Do not be defensive! If an interviewer challenges your design (e.g., "Why didn't you use MongoDB here?"), they are not attacking you. They want to see how you defend your technical choices. Say: *"MongoDB is a great document store, but since our data is highly relational with deep joins, Postgres is a safer bet. However, if we need flexible schemas later, we could absolutely introduce Mongo for the metadata layer."*
