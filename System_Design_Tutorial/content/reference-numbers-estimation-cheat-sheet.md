# Reference Numbers & Estimation Cheat Sheet

## Overview
During a System Design interview, you will not have access to a calculator or a browser. You are expected to do "Back of the Envelope" math in your head or on a whiteboard. 

If you memorize the reference numbers in this cheat sheet, you will be able to estimate traffic, storage, and bandwidth for any system in under two minutes.

---

## Powers of 2: 2^10=1K · 2^20=1M · 2^30=1B · 2^40=1T

Computers operate in base-2. You must know how to translate powers of 2 into human-readable numbers (thousands, millions, billions). 

Memorize this table:

| Power of 2 | Exact Value | Approximation (Name) | Example Use Case |
| :--- | :--- | :--- | :--- |
| **2^10** | 1,024 | 1 Thousand (1 KB) | Size of a standard JSON payload |
| **2^20** | 1,048,576 | 1 Million (1 MB) | Size of a highly compressed photo |
| **2^30** | 1,073,741,824 | 1 Billion (1 GB) | Size of a standard movie file |
| **2^40** | 1,099,511,627,776 | 1 Trillion (1 TB) | Size of an enterprise database table |

**Why this matters:** If a question states a system handles 1 Billion requests a day, and each request is 1 KB, you immediately know the daily data generated is 1 TB (1 Billion * 1 KB = 1 Terabyte). 

---

## Read latencies: L1 0.5ns · L2 7ns · RAM 100ns · SSD 150μs · HDD 10ms · WAN 150ms

We covered this in the Capacity Estimation module, but it is so important it bears repeating. 
*Note: ns = nanosecond, μs = microsecond, ms = millisecond.*

- **L1 Cache:** 0.5 ns
- **RAM Read:** 100 ns
- **SSD Read:** 150 μs
- **HDD Read (Disk Seek):** 10 ms (10,000,000 ns)
- **Send packet CA to Europe and back:** 150 ms

> [!TIP]
> **Analogy:** If 1 CPU cycle (0.5 ns) is equivalent to **1 second**, reading from RAM takes **3 minutes**. Reading from a Hard Drive takes **10 months**. Sending a packet across the ocean takes **8 years**. 
> This is why caching in RAM is absolutely mandatory for fast APIs!

---

## 1B users, 10% DAU, 1 request/day → ~1157 QPS

You will often be given Monthly Active Users (MAU) or Total Users. You need to convert this to QPS (Queries Per Second).

**The Shortcut to memorize:**
There are 86,400 seconds in a day. For interview math, round this to **100,000 seconds**.

Let's do the math:
1. Total Users = 1 Billion.
2. 10% are Daily Active Users (DAU) = 100 Million DAU.
3. Each user makes 1 request per day = 100 Million requests / day.
4. 100,000,000 / 100,000 seconds = **1,000 QPS**.

*(The exact math dividing by 86,400 gives 1,157 QPS. In an interview, 1,000 is perfectly acceptable and shows you know how to estimate quickly).*

---

## 100GB/day data → ~3TB/month → ~36TB/year → can a single machine hold it?

Storage math is crucial for determining if you need a distributed database (Sharding).

**The Calculation:**
- 100 GB per day
- Multiply by 30 days = 3,000 GB / month (3 TB / month)
- Multiply by 12 months = 36 TB / year.
- For 5 years of retention: 36 * 5 = **180 TB.**

**The Architectural Decision:**
Can a single MySQL server hold 180 TB of data? 
*No.* High-end AWS RDS instances max out around 64 TB. 
Therefore, you must explicitly state: *"Since our 5-year storage is 180TB, a single database node will not suffice. We must horizontally shard the database, perhaps hashing by UserID, to distribute this data across at least 4 to 6 database nodes."*

---

## Text tweet: ~280 chars → image tweet: ~500KB → video: ~100MB

When estimating storage, you must make assumptions about the size of a single object. If the interviewer does not provide object sizes, state your assumptions clearly using these industry standards:

| Data Type | Estimated Size | Notes |
| :--- | :--- | :--- |
| **Character (ASCII)** | 1 Byte | |
| **Character (Unicode)** | 2-4 Bytes | Emojis take up more space! |
| **Short Text (Tweet/Message)** | 200 - 500 Bytes | Includes metadata like timestamps and IDs. |
| **Image (Compressed)** | 200 KB - 500 KB | Standard JPG/WebP on social media. |
| **Image (High Res)** | 2 MB - 5 MB | Raw camera uploads. |
| **Video (Standard Def)** | ~50 MB per minute | Highly dependent on compression (H.264). |

> [!NOTE]
> **Teacher's FAQ:** What if I guess the wrong size? 
> **Answer:** It doesn't matter! The interviewer is grading your *methodology*, not your exact bytes. If you say "Let's assume a profile picture is 200KB", the interviewer will just say "sounds good" or "actually, let's assume 2MB." Just state the assumption clearly before doing the math!
