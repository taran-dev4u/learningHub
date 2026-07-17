# Rate Limiting Algorithms

## Overview
If you expose a public API, someone will abuse it. Whether it's a malicious DDoS attack, a competitor scraping your data, or a buggy script from a legitimate partner, you must protect your servers.

**Rate Limiting** controls how many requests a client can make in a given timeframe. In interviews, you are often asked not just *where* to put the rate limiter (usually the API Gateway), but *exactly how* the algorithm works.

This masterclass dissects the 4 primary algorithms and how to implement them in a distributed system.

---

## Token bucket — refill at fixed rate, allow bursts

The Token Bucket is the most widely used algorithm in the industry (used by Amazon and Stripe).

**The Analogy:** Imagine a bucket that holds a maximum of 10 tokens. Every minute, a machine drops 2 new tokens into the bucket. When a user makes an API request, they take 1 token out. If the bucket is empty, the request is rejected (429 Too Many Requests).

**Characteristics:**
- **Allows Bursts:** If the user hasn't made a request in a while, the bucket is full. They can suddenly fire off 10 rapid requests (a burst) before being throttled.
- **Memory Efficient:** You only need to store two variables per user: `tokens_left` and `last_refill_timestamp`. You calculate the refill dynamically on the next request using the time delta.

---

## Leaky bucket — smooth output rate, no bursts

Used heavily by Shopify, the Leaky Bucket is designed to smooth out traffic.

**The Analogy:** Imagine a bucket with a hole in the bottom. Users can pour water (requests) into the top of the bucket at any speed. However, the water leaks out the bottom at a *fixed, constant rate* (e.g., 5 requests per second) to be processed by the server. If the bucket fills to the top, new requests spill over and are rejected.

**Characteristics:**
- **No Bursts:** Even if 100 requests arrive in one second, the server will only process them at a smooth 5/sec.
- **Queueing:** It acts as a First-In-First-Out (FIFO) queue. It protects the database from sudden spikes, making it ideal for systems that require perfectly predictable loads.

---

## Fixed window — count per window, spike at window boundary

This is the simplest algorithm to implement, but it has a massive, potentially system-crashing flaw.

**How it works:** You divide time into fixed windows (e.g., 12:00 to 12:01). A user gets 100 requests per window. You keep a counter. At 12:01, the counter resets to 0.

**The Flaw: The Boundary Spike Problem.**
If a user sends 100 requests at 12:00:59, and then sends another 100 requests at 12:01:01, they have successfully sent **200 requests within a 2-second period**, completely bypassing the intended limit of 100 per minute! If millions of users coordinate this on the minute boundary, your servers will melt.

---

## Sliding window log / counter — accurate, more memory

To fix the Boundary Spike problem of the Fixed Window, we use a Sliding Window. There are two variations.

### 1. Sliding Window Log
Instead of keeping a simple counter, you log the *exact timestamp* of every single request a user makes (usually in Redis). When a new request arrives, you delete all timestamps older than 1 minute. If the remaining count of logs is < 100, you accept the request.
- **Pros:** 100% mathematically accurate. No boundary spikes.
- **Cons:** Extremely memory-intensive. Storing thousands of timestamps per user per minute will quickly overwhelm Redis.

### 2. Sliding Window Counter (The Hybrid)
This is the sweet spot. It combines Fixed Window and Sliding Window.
You track the counter for the *current* minute and the *previous* minute. If we are 30% of the way into the current minute, we calculate the total requests as:
`(Requests in Current Minute) + (Requests in Previous Minute * 0.7)`.
- **Pros:** Highly accurate, smooths out boundary spikes, and requires almost zero memory.

---

## Distributed rate limiting with Redis (Redlock / Lua scripts)

In the real world, you don't have one API Gateway. You have 10 API Gateways running in parallel.

If User A gets 5 requests per minute, how do Gateway 1 and Gateway 2 keep track of the same counter without overriding each other?

**The Solution: Centralized Datastore (Redis)**
All Gateways must read/write to a shared Redis instance. However, this introduces a **Race Condition**. If Gateway 1 and Gateway 2 read the Redis counter at the exact same millisecond, they both see `count = 4`, both increment to `5`, and both allow the request. The user got 6 requests!

**How to solve the Race Condition:**
1. **Redis Lua Scripts:** Redis is single-threaded. By writing the read-increment-check logic in a Lua script, Redis executes the entire block atomically. No two gateways can interleave their operations.
2. **Distributed Locks (Redlock):** Put a lock on the user's ID, fetch the count, increment it, write it back, and release the lock. (This is significantly slower than Lua scripts and is generally avoided for rate limiting).

> [!WARNING]
> **Performance Trade-off:** By moving rate limiting to a centralized Redis, you introduce latency to every single API call! To optimize this, some systems use local, in-memory rate limiting on each Gateway, and sync with Redis asynchronously (Eventual Consistency), sacrificing strict limits for blistering speed.
