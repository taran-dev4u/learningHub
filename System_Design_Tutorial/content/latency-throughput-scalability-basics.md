# Latency, Throughput & Scalability Basics

## Overview
Before we build distributed architectures, we must understand the three most fundamental forces in computing: **Latency** (how fast), **Throughput** (how much), and **Scalability** (how we grow).

If you confuse Latency and Throughput in an interview, it is an immediate red flag. This masterclass will solidify these concepts so you never mix them up again.

---

## Latency vs Throughput (The Highway Analogy)

To understand the difference, imagine a highway.
- **Latency:** How long it takes one car to travel from City A to City B. (Speed).
- **Throughput:** How many cars arrive at City B every hour. (Volume).

If you want to improve **Latency**, you make the cars drive faster (or shorten the road).
If you want to improve **Throughput**, you build more lanes on the highway so more cars can travel at the same time.

### Technical Definitions
| Metric | Definition | Unit of Measurement |
| :--- | :--- | :--- |
| **Latency** | The time it takes for a single request to complete its round trip. | Milliseconds (ms) |
| **Throughput** | The total number of requests the system can process in a given timeframe. | Queries Per Second (QPS) or Mbps |

> [!TIP]
> **Teacher's Secret:** You can have high latency *and* high throughput! Imagine a cargo ship. It takes 3 weeks to cross the ocean (terrible latency), but it carries 10,000 shipping containers (massive throughput). 

---

## P50 / P95 / P99 — tail latency dominates user experience

If you have 100 API requests, and you calculate the *Average (Mean)* latency, you are doing it wrong. Averages hide terrible performance. 

In System Design, we measure latency using **Percentiles**.

- **P50 (Median):** 50% of requests are faster than this. (The typical user experience).
- **P95:** 95% of requests are faster than this. (The slow users).
- **P99 (Tail Latency):** 99% of requests are faster than this. (The absolute worst-case scenario).

**Why P99 matters:**
If Amazon's web page requires 100 different microservices to load, and *each* microservice has a 1% chance of being slow (hitting the P99 latency), then the probability that a user experiences a slow page load is astronomically high! 
*Tail latency dominates distributed systems.* You must design your system to aggressively cut off slow responses using **Timeouts** and **Circuit Breakers**.

---

## Vertical scaling (scale-up) — simpler, limited by hardware

When your server hits 100% CPU, how do you handle more traffic? The easiest way is **Vertical Scaling (Scaling Up)**.

**What is it?** 
You turn off your server, throw away the small CPU, and put in a massive 64-core CPU with 1TB of RAM. 

| Pros of Vertical Scaling | Cons of Vertical Scaling |
| :--- | :--- |
| No code changes required. | **Hardware Limit:** You cannot buy a CPU with 10,000 cores. It hits a physical ceiling. |
| Extremely easy to manage (1 server). | **Single Point of Failure (SPOF):** If this one mega-server crashes, your entire company is offline. |
| No network overhead between nodes. | **Downtime:** Requires shutting the server down to upgrade hardware. |

---

## Horizontal scaling (scale-out) — stateless apps, requires LB

Because Vertical Scaling has a physical ceiling, tech giants use **Horizontal Scaling (Scaling Out)**.

**What is it?**
Instead of buying 1 massive server, you buy 1,000 cheap, weak servers and distribute the traffic across all of them.

### The Golden Rule of Horizontal Scaling
To scale horizontally, your application servers **MUST be stateless**. 
If Server A saves user login sessions in its local RAM, and the Load Balancer routes the user's next request to Server B, the user will be logged out! 
You must move all state (sessions, data) out of the application servers and into a shared external database or cache (like Redis).

| Pros of Horizontal Scaling | Cons of Horizontal Scaling |
| :--- | :--- |
| **Infinite Scale:** Just add more servers. | **Complexity:** You now have to manage hundreds of servers. |
| **High Availability:** If 5 servers die, 995 are still running. | Requires a **Load Balancer** to distribute the traffic. |
| Elastic (Auto-scaling based on traffic). | Distributed bugs (network partitions, clock drift). |

---

## Batching increases throughput at the cost of latency

We mentioned the Cargo Ship analogy earlier. This is the concept of **Batching**.

If you have to write 1,000 logs to a database:
- **Approach 1 (No Batching):** Open a network connection, send 1 log, close it. Do this 1,000 times.
  - *Result:* Great latency for the first log. Terrible overall throughput due to network overhead.
- **Approach 2 (Batching):** Wait 5 seconds, collect all 1,000 logs, open *one* network connection, and write them all at once.
  - *Result:* The first log had to wait 5 seconds (terrible latency), but the system processed 1,000 logs incredibly efficiently (massive throughput).

> [!NOTE]
> **Teacher's FAQ:** When should I use Batching? 
> **Answer:** Use it for asynchronous tasks where the user isn't waiting on the screen! Analytics processing, Kafka message production, and Database bulk inserts are prime candidates for batching. Never use batching for real-time chat APIs.
