# Backpressure, Throttling & Load Protection: The Masterclass

Welcome back, architects. When your system becomes successful, your biggest enemy isn't bugs or latency—it’s your own users. A viral marketing campaign, a malicious botnet, or a buggy client script can flood your APIs with traffic, bringing your entire backend to its knees.

In this masterclass, we will explore the mechanisms of **Rate Limiting, Throttling, and Backpressure**. We will examine the core algorithms that power these systems, their trade-offs, and how to scale them across a distributed architecture using tools like Redis.

---

## 1. The Core Philosophy: Why Do We Throttle?

### The "Why": Defending the Database
Imagine a popular nightclub with a maximum capacity of 500 people. If 5,000 people try to shove their way through the front door at the same time, people get crushed, the music stops, and the club is shut down by the fire marshal.

To prevent this, the club employs a **bouncer**. The bouncer forms a line and only lets a few people in at a time. This is **Rate Limiting**.

In system design, your database and your compute nodes have a maximum capacity. If you allow unbounded requests, you will exhaust your connections, max out your CPU, and crash the system. Throttling is your bouncer. It protects your expensive, stateful backend by rejecting excess requests at the cheap, stateless edge (like an API Gateway).

> [!WARNING]
> **The Golden Rule of Throttling:** It is always better to serve 500 requests successfully and reject 5,000, than to attempt to serve 5,500 and crash, serving zero.

---

## 2. Rate Limiting Algorithms

There are several ways to implement a rate limiter. We will cover the three most important algorithms you must know for system design interviews and real-world architectures.

### Token Bucket — burst-friendly, most common choice

The Token Bucket is the industry standard. Companies like Amazon and Stripe use this heavily.

**How it works:**
1. Imagine a bucket that holds a maximum of $B$ tokens.
2. Every $R$ seconds, a new token is added to the bucket (until it is full).
3. When a request arrives, it tries to take 1 token from the bucket.
4. If a token is available, the request is processed.
5. If the bucket is empty, the request is dropped (HTTP 429 Too Many Requests).

**The "Why" it is so popular:**
It allows for **bursts** of traffic. If your bucket holds 10 tokens and hasn't been used in a while, a user can instantly make 10 rapid-fire requests. Once the burst is over, they are limited to the refill rate.

| Pros | Cons |
| :--- | :--- |
| Allows bursts of traffic (user friendly). | Requires tuning two parameters: bucket size and refill rate. |
| Extremely memory efficient. | Harder to implement completely from scratch than fixed window. |

### Fixed Window — simple, vulnerable to edge-of-window spike

This is the most intuitive algorithm. You divide time into fixed intervals (e.g., 1-minute windows: 10:00–10:01, 10:01–10:02).

**How it works:**
1. You maintain a counter for the current window.
2. Each request increments the counter.
3. If the counter exceeds the limit (e.g., 100 requests/minute), reject.
4. When the next minute starts, the counter resets to 0.

**The Edge-of-Window Spike Problem:**
Imagine a limit of 100 requests per minute.
- A user sends 100 requests at 10:00:59. They are allowed.
- The clock strikes 10:01:00, and the counter resets.
- The user immediately sends another 100 requests at 10:01:01. They are allowed.

The user just sent **200 requests in a 2-second window**, effectively bypassing your 100 req/min limit and potentially crushing your backend.

> [!CAUTION]
> Avoid Fixed Window for mission-critical endpoints due to the spike problem, unless you are using it as a simple, high-level safeguard.

### Sliding Window Log — accurate, high memory usage

This algorithm fixes the edge-of-window problem by calculating rolling windows dynamically.

**How it works:**
1. Instead of a simple counter, you keep a timestamp log of *every* request the user has made.
2. When a new request arrives, you delete all timestamps older than 1 minute (the window size).
3. If the remaining number of timestamps is less than the limit, you add the new timestamp and allow the request.
4. Otherwise, reject.

**The Trade-off:**
It is 100% accurate. There are no edge spikes. However, keeping a log of *every single request timestamp* for millions of users consumes a massive amount of memory.

| Pros | Cons |
| :--- | :--- |
| Perfect accuracy. Smoothly handles edge cases. | High memory footprint. |
| No artificial resets. | Slow to calculate (must filter/trim arrays of data on every request). |

---

## 3. Distributed Rate Limiting with Redis

In modern architectures, you don't have just one server; you have a fleet of API servers. If you implement rate limiting strictly in the local memory of `Server A`, a user could just route their traffic to `Server B` to bypass the limit.

To enforce a *global* limit, you need a centralized datastore that all API servers can talk to quickly. **Redis** is the industry standard for this.

### The Problem: Race Conditions
If two API servers check Redis at the same time:
1. Server A reads counter = 99
2. Server B reads counter = 99
3. Server A increments to 100
4. Server B increments to 100

Both servers allowed the request, but the total is now 101. The limit was breached.

### The Solution: Redis Lua Scripts
Redis can execute **Lua scripts**. The magic of Redis Lua scripts is that they execute **atomically**. While the script is running, Redis blocks all other operations.

By writing your Token Bucket or Fixed Window logic in a short Lua script and sending it to Redis, you guarantee that the check, the increment, and the expiration set all happen as a single, uninterrupted transaction.

```lua
-- Example: Simplified Token Bucket in Lua
local tokens_key = KEYS[1]
local timestamp_key = KEYS[2]
-- ... logic to calculate refill and deduct token ...
return allowed
```

---

## Teacher FAQ & Common Beginner Mistakes

> [!NOTE]
> **Question:** Where should I put my rate limiter?
> **Answer:** As close to the edge as possible! An API Gateway, an Ingress Controller, or even a CDN (like Cloudflare). You want to drop bad traffic before it ever touches your application code.

> [!NOTE]
> **Question:** What is "Backpressure"? Is it the same as rate limiting?
> **Answer:** Rate limiting is usually externally facing (limiting user API calls). **Backpressure** is internal. It is a mechanism where a struggling downstream component (like a slow database or a message queue consumer) signals upstream to "stop sending me data, I'm full." It’s a cooperative push-back mechanism, whereas rate-limiting is a hard wall.

> [!NOTE]
> **Misconception:** "I can just rate limit by IP address."
> **Correction:** IP-based rate limiting is easily defeated by botnets (which have millions of IPs) or NATs (where thousands of legitimate users on a college campus share a single IP). Always rate limit by user ID, API key, or a combination of factors whenever possible.
