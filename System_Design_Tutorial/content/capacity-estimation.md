# Capacity Estimation

## Overview
Welcome to **Capacity Estimation**! Before you can design a system that works, you need to know exactly how much data and traffic it will handle. 

Capacity estimation (often called "Back of the Envelope Math") proves to the interviewer that you understand the sheer physics of computing. If you guess the wrong numbers, you might design a single SQL database for a system that actually requires 50 distributed NoSQL nodes.

This masterclass covers the essential frameworks and numbers you must memorize.

---

## Back-of-envelope framework

Do not panic when asked to do math in an interview. You are not expected to be perfectly precise. You are expected to show a logical chain of thought. 

Use this foolproof 5-step framework:

1. **Daily Active Users (DAU):** Start with the user base. 
2. **Requests per User:** Estimate how many times a single user performs the core action per day.
3. **QPS (Queries Per Second):** Multiply DAU by Requests, then divide by 86,400 (seconds in a day).
4. **Storage Needed:** Multiply DAU by the size of the data they generate. Multiply by 365 for a year.
5. **Bandwidth:** Divide daily data by 86,400 to get bytes per second.

> [!TIP]
> **Teacher's Secret:** Round aggressively! 1 day = 86,400 seconds. In an interview, round this to **100,000 seconds**. 
> If you have 100 Million daily requests, dividing by 100,000 gives you exactly 1,000 QPS. Done in 2 seconds!

---

## QPS, storage and bandwidth math

Let's do a real example: **Designing Twitter**.

### 1. Traffic (QPS)
- **Assumptions:** 300 Million DAU. A user tweets 2 times a day and views the timeline 5 times a day.
- **Write QPS:** (300M * 2) / 100,000 seconds = **6,000 QPS**
- **Read QPS:** (300M * 5) / 100,000 seconds = **15,000 QPS**

### 2. Storage
- **Assumptions:** A tweet is mostly text (140 bytes) + some metadata (100 bytes). Let's round to **250 bytes**.
- **Daily Storage:** 600 Million tweets * 250 bytes = **150 GB / day**
- **5-Year Storage:** 150 GB * 365 * 5 ≈ **270 TB** 
*(Knowing this is 270TB instantly tells you a single hard drive cannot hold it. You need sharding!)*

### 3. Bandwidth
- **Ingress (Incoming):** 150 GB / 100,000 seconds = **1.5 MB/s**

---

## Latency numbers to memorize

In 2012, Jeff Dean (Google) published "Numbers Every Programmer Should Know". For System Design interviews, you only need to memorize these five:

| Operation | Latency | Real-world Analogy |
| :--- | :--- | :--- |
| **L1 Cache Reference** | 0.5 ns | Your heartbeat |
| **Main Memory (RAM) Read** | 100 ns | Looking at your phone |
| **Solid State Drive (SSD) Read** | 100 µs (micro) | Walking across the room |
| **Hard Disk (HDD) Read** | 10 ms (milli) | Driving to the grocery store |
| **Cross-Continent Network Packet** | 150 ms | Taking a flight to Europe |

**Why this matters:**
If you need to fetch a user's profile in 5ms, and your database is on a spinning Hard Disk (10ms), it is physically impossible. You **must** put a RAM cache (Redis) in front of it (100ns).

---

## Peak vs average traffic sizing

If you calculated an average of **1,000 QPS**, is that how many servers you provision? **No!**

Traffic is never perfectly smooth. It spikes during the Superbowl, breaking news, or standard evening hours. 
- **Rule of Thumb:** Peak Traffic is usually **2x to 5x** the average traffic.
- If Average QPS = 1,000, design your system to handle **3,000 to 5,000 Peak QPS**.

### How to handle the gap:
Do not pay for 5,000 QPS of servers if you only need them for one hour a day.
1. Design for the Peak (make sure your architecture *can* scale).
2. Pay for the Average (run only the servers you need).
3. Use **Auto-scaling groups** to bridge the gap automatically.

---

## Read/write ratio implications

During your calculations, always pay attention to the ratio of Reads to Writes.

### Read-Heavy Systems (e.g., Twitter, YouTube)
- **Ratio:** 100:1 to 1000:1 (Reads : Writes)
- **Architecture Strategy:** Aggressively use Caching (Redis/Memcached). Use Database Read Replicas. You can afford slower writes because reading is the bottleneck.

### Write-Heavy Systems (e.g., IoT Sensors, Server Logging)
- **Ratio:** 1:1 or even 1:100 (Reads : Writes)
- **Architecture Strategy:** Caching will not help you. You need databases optimized for massive write throughput, like **Cassandra** or **Time-Series Databases** that use Log-Structured Merge (LSM) trees. You will also heavily rely on Message Queues (Kafka) to buffer the incoming writes.

> [!NOTE]
> **Conclusion:** Capacity estimation dictates your entire architecture. Once you know your QPS and Storage, you can mathematically prove whether your design will survive or crash.
