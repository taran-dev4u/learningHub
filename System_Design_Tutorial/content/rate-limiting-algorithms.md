# Rate Limiting Algorithms

## Overview

If you expose a network service to the public internet, it will be subjected to uncontrolled, adversarial, or accidentally catastrophic load. Whether it is an orchestrated Distributed Denial of Service (DDoS) assault, aggressive web crawlers extracting proprietary data, a malfunctioning third-party integration trapped in an infinite retry loop, or a sudden viral marketing surge ("the Oprah effect"), your system resources are finite. 

**Rate Limiting** is the practice of restricting the frequency and volume of requests a client, user, or IP address can transmit to a service within a predefined temporal boundary. In technical interviews, senior and staff candidates are evaluated on far more than merely diagramming an API Gateway box with a "Rate Limiter" label. You must articulate the mathematical mechanics, space/time complexities, concurrency race conditions, and distributed trade-offs across four foundational algorithms, alongside real-world production implementation strategies.

---

## Token bucket — refill at fixed rate, allow bursts

The **Token Bucket** algorithm is the gold standard for public API platforms, powering production infrastructure at Amazon AWS, Stripe, and Google Cloud.

### 1. Conceptual Mechanics & Analogy
Imagine a physical bucket mounted at an entrance turnstile. The bucket has a rigid maximum capacity $C$ (e.g., 10 tokens). A automated dispensing valve continuously drops fresh tokens into the bucket at a constant, fixed rate $r$ (e.g., 2 tokens every second). If the bucket reaches capacity $C$, newly arriving tokens simply overflow and are discarded.

When an inbound client request arrives:
1. The system inspects the bucket for available tokens.
2. If at least 1 token is present, 1 token is extracted, and the request is permitted through to the backend service.
3. If the bucket is empty (0 tokens available), the request is dropped immediately or rejected with HTTP status code `429 Too Many Requests`.

```
                    Token Dispenser
               (Refills at rate 'r' / sec)
                          │
                          ▼
                   ┌──────────────┐
                   │  ●  ●  ●  ●  │  <-- Capacity 'C'
                   │  ●  ●  ●     │      (Overflows if full)
                   └──────┬───────┘
                          │ 
      Incoming Request ──►│ Consume 1 Token?
                          ├─────── Yes ───► [Forward to Microservice]
                          └─────── No  ───► [429 Too Many Requests]
```

### 2. The Burst Dynamic
The critical design feature of Token Bucket is its native support for **traffic bursts**. If a client remains inactive for 10 seconds, their bucket fills up completely to capacity $C = 10$. If the client suddenly executes 10 parallel HTTP requests within a single millisecond, all 10 requests will find an available token and execute without delay. Subsequent requests will then be strictly throttled to the refill rate $r$ (2 requests/sec) until another idle period permits token accumulation.

### 3. Mathematical State & Zero-Daemon Refill
Beginners frequently make the fatal mistake of designing a background cron worker or timer daemon that iterates across millions of user accounts to add tokens every second. In production, this would annihilate your CPU and database.

Instead, the refill is computed **lazily on-demand** whenever a request actually arrives. For each rate-limited entity (e.g., `user_id`), we persist only two lightweight scalar variables:
1. `tokens`: Floating-point count of currently remaining tokens.
2. `last_refill`: Unix millisecond timestamp when the bucket was last evaluated.

Upon arrival of request at timestamp `now`:
$$\Delta t = \text{now} - \text{last\_refill}$$
$$\text{new\_tokens} = \min(C, \text{tokens} + \Delta t \times r)$$

If $\text{new\_tokens} \ge 1.0$:
$$\text{tokens} = \text{new\_tokens} - 1.0$$
$$\text{last\_refill} = \text{now}$$
$$\text{Status} \leftarrow \text{ALLOW}$$
Else:
$$\text{last\_refill} = \text{now}$$
$$\text{Status} \leftarrow \text{DROP (429)}$$

### 4. Algorithmic Complexity
- **Time Complexity:** $O(1)$ constant time arithmetic evaluation.
- **Space Complexity:** $O(1)$ per client identity (storing an 8-byte float and an 8-byte timestamp).

---

## Leaky bucket — smooth output rate, no bursts

While the Token Bucket accommodates instantaneous bursts up to capacity $C$, the **Leaky Bucket** algorithm is specifically engineered to **smooth out traffic spikes** into a perfectly uniform, predictable egress stream. It is widely implemented in e-commerce checkout pipelines (e.g., Shopify) and database write buffers where downstream storage engines choke on concurrency spikes.

### 1. Conceptual Mechanics & Analogy
Picture a rigid bucket with a small, calibrated hole drilled into its bottom. Water represents incoming network requests. Regardless of whether a client dumps a massive bucket of water all at once or drips water intermittently, the outflow from the hole occurs at an unvarying, fixed rate (e.g., exactly 5 requests per second).

If client requests arrive faster than the leakage rate, water accumulates in the bucket. As long as the bucket has remaining volume, requests are enqueued in memory. However, if the bucket fills to its brim (buffer capacity $B$), incoming requests overflow and are immediately rejected.

```
       Incoming Requests (Irregular, bursty spikes)
                          │ │ │ │ │
                          ▼ ▼ ▼ ▼ ▼
                   ┌──────────────┐
                   │  ░░░░░░░░░░  │  <-- Queue Buffer Capacity 'B'
                   │  ░░░░░░░░░░  │      (Overflow drops new requests)
                   └──────┬───────┘
                          │
                          ▼ (Constant leak rate 'r' req/sec)
               [Deterministic, Smooth Queue Output]
                          │
                          ▼
                 [Backend Database / Disk]
```

### 2. Implementation: FIFO Queue vs Virtual Leak
In software architecture, the Leaky Bucket is typically implemented as a bounded First-In-First-Out (FIFO) queue:
- Inbound requests push tasks onto the tail of the queue.
- If `queue.size() >= B`, the request is dropped with `429 Too Many Requests`.
- A dedicated background worker continuously pops items from the head of the queue at rate $r$.

> [!TIP]
> **Key Architecture Distinction:**
> - **Token Bucket:** Drops requests when the bucket is *empty*. Output traffic can be *bursty*.
> - **Leaky Bucket:** Drops requests when the bucket is *full*. Output traffic is *strictly uniform and paced*.

---

## Fixed window — count per window, spike at window boundary

The **Fixed Window Counter** algorithm is the simplest rate-limiting mechanism to conceptualize and code, yet it harbors an insidious structural vulnerability known as the **Boundary Spike Phenomenon**.

### 1. Conceptual Mechanics
Time is segmented into discrete, contiguous, non-overlapping chronological windows of duration $W$ (e.g., 60 seconds: `12:00:00 - 12:01:00`, `12:01:00 - 12:02:00`). Each window maintains an atomic counter initialized to 0. Every incoming request increments the active window's counter. If the counter surpasses threshold $L$ (e.g., 100 requests), all subsequent requests in that window are rejected. When the clock advances past the window boundary, a new window begins, and the counter resets.

### 2. The Boundary Spike Vulnerability
Consider a rate limit rule of **100 requests per minute**:
- Between `12:00:00` and `12:00:58`, a malicious actor sends 0 requests.
- At `12:00:59` (the final second of Window 1), the client fires **100 requests**. Because the counter was 0, all 100 requests are approved.
- At `12:01:00`, the window flips to Window 2. The counter resets to 0.
- At `12:01:01` (the first second of Window 2), the client fires another **100 requests**. Again, all 100 requests are approved.

```
Window 1 [12:00:00 - 12:01:00]       Window 2 [12:01:00 - 12:02:00]
                     100 reqs        100 reqs
                     [12:00:59]      [12:01:01]
                         │               │
                         ▼               ▼
─────────────────────────┴───────────────┴────────────────────────► Time
                         ◄───── 2 sec ───►
                           200 Total Reqs!
```

**The Consequence:** The client transmitted **200 requests within a 2-second interval** across the boundary—exceeding the intended server capacity limit by **200%**. In multi-tenant systems, coordinated boundary spikes will trigger cascading database lock exhaustion.

---

## Sliding window log / counter — accurate, more memory

To eliminate the boundary spike vulnerability of the Fixed Window while avoiding the queue latency of Leaky Bucket, engineers turn to the **Sliding Window** paradigm.

### 1. Sliding Window Log (Exact Precision)
The Sliding Window Log maintains an exact record of every individual request timestamp executed by a client.

#### Mechanics in Redis (Sorted Set `ZSET`):
1. Represent each client by a Redis Sorted Set key: `ratelimit:<client_id>`.
2. When a request arrives at timestamp $T_{\text{now}}$, remove all elements from the set whose score is older than the rolling window threshold:
   `ZREMRANGEBYSCORE ratelimit:<client_id> 0 (T_now - W)`
3. Query the current cardinality of the set:
   `count = ZCARD ratelimit:<client_id>`
4. If `count < Limit`:
   Add the current timestamp to the set: `ZADD ratelimit:<client_id> T_now T_now`
   Set key TTL to $W$: `EXPIRE ratelimit:<client_id> W`
   Permit request.
5. If `count >= Limit`: Reject request with 429.

#### Trade-off Analysis:
- **Advantage:** 100% mathematical precision. It is impossible for a user to transmit more than $L$ requests in *any* rolling $W$-second interval.
- **Disadvantage:** Severe memory overhead. Storing 100 64-bit integer timestamps plus Redis set metadata consumes ~4 KB per user. For 10 million active users, storing rolling logs demands 40 GB+ of pure RAM just for rate-limiting bookkeeping.

### 2. Sliding Window Counter (Memory-Optimized Approximation)
Cloudflare and modern high-throughput API gateways utilize the **Sliding Window Counter**, which merges the minimal memory footprint of Fixed Window with the boundary smoothing of Sliding Window Log.

#### The Sliding Window Counter Algorithm:
Instead of logging individual timestamps, we track only the aggregate count of the **current fixed window** ($C_{\text{curr}}$) and the aggregate count of the **immediately preceding fixed window** ($C_{\text{prev}}$).

When a request arrives at timestamp $T_{\text{now}}$:
1. Calculate how far along the current window has progressed as a percentage:
   $$\text{weight}_{\text{curr}} = \frac{T_{\text{now}} - \text{window\_start}}{W}$$
   $$\text{weight}_{\text{prev}} = 1.0 - \text{weight}_{\text{curr}}$$
2. Estimate the total requests in the rolling 60-second window:
   $$\text{Estimated Requests} = C_{\text{curr}} + (C_{\text{prev}} \times \text{weight}_{\text{prev}})$$
3. If $\text{Estimated Requests} < \text{Limit}$, increment $C_{\text{curr}}$ and allow; otherwise, reject.

#### Real-World Calculation Example:
- Window size: 60 seconds. Limit: 100 requests.
- Requests in previous minute ($C_{\text{prev}}$): 80 requests.
- Requests in current minute ($C_{\text{curr}}$): 30 requests.
- Current time is 18 seconds into the current minute ($\text{weight}_{\text{curr}} = 18 / 60 = 0.3$, so $\text{weight}_{\text{prev}} = 0.7$).
- Estimated rolling volume:
  $$30 + (80 \times 0.7) = 30 + 56 = 86 \text{ requests}$$
- Since $86 < 100$, the request is permitted.

```
Previous Window [12:00]                 Current Window [12:01]
Count = 80                              Count = 30
┌───────────────────────┬───────────────┬───────────────────────┐
│                       │   [ 70% ]     │   [ 30% ]             │
└───────────────────────┴───────────────┴───────────────────────┘
                        ◄──────── Rolling 60s Window ──────────►
                                 80 * 0.7 + 30 = 86 reqs
```

#### Trade-off Analysis:
- **Memory Footprint:** Tiny. Only two integers stored per user key in Redis ($< 64$ bytes).
- **Accuracy:** Over 99.9% accurate in empirical production benchmarks, mathematically preventing boundary bursts while consuming negligible RAM.

---

## Algorithm Decision Matrix

| Dimension | Token Bucket | Leaky Bucket | Fixed Window | Sliding Window Log | Sliding Window Counter |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Time Complexity** | $O(1)$ | $O(1)$ | $O(1)$ | $O(\log N + M)$ | $O(1)$ |
| **Space Complexity** | $O(1)$ (tokens, time) | $O(B)$ (queue size) | $O(1)$ (counter) | $O(N)$ (timestamps) | $O(1)$ (2 counters) |
| **Burst Handling** | Permits up to cap $C$ | Zero bursts allowed | Bursts 2x at boundary | Zero burst leaks | Smooths boundary |
| **Memory Pressure** | Extremely low | Medium (queue buffers) | Extremely low | Very high ($N$ entries) | Minimal ($< 64$ bytes) |
| **Downstream Impact** | Bursty spikes passed | Smooth deterministic load | Destructive spikes | Smooth | Smooth |
| **Primary Industry Use** | Stripe, AWS, GitHub APIs | Shopify, ingest pipelines | Basic internal quotas | Strict security auth | Cloudflare, Envoy Proxy |

---

## Distributed rate limiting with Redis (Redlock / Lua scripts)

In modern microservice architectures, incoming requests do not hit a single monolithic server; they are distributed across hundreds of stateless API Gateway instances via DNS Round-Robin or Layer-4 Load Balancers.

```
                Client Requests
                      │
                      ▼
             [ L4 Load Balancer ]
            ┌─────────┼─────────┐
            ▼         ▼         ▼
        [Gateway 1] [Gateway 2] [Gateway 3]
            │         │         │
            └─────────┼─────────┘
                      ▼
           [ Central Redis Cluster ]
             (Atomic Lua Scripts)
```

### 1. The Distributed Concurrency Race Condition
If User `alice` has a limit of 10 requests per minute and currently has 9 consumed tokens:
1. Gateway 1 receives Request A at $T = 0.001\text{ ms}$.
2. Gateway 2 receives Request B at $T = 0.001\text{ ms}$.
3. Both gateways read Redis asynchronously: `GET ratelimit:alice` returns `9`.
4. Both gateways independently conclude: `9 < 10`, request is valid!
5. Both gateways execute `SET ratelimit:alice 10`.
6. **Result:** Alice executed 11 requests, violating her strict service tier.

### 2. Solving Concurrency: Redis Atomic Lua Scripts
Redis operates as a single-threaded event loop for command execution. When a Lua script runs inside Redis via `EVAL` or `EVALSHA`, Redis guarantees that **no other command or script can interleave execution**. The entire read-compute-write lifecycle executes atomically.

Here is the production-grade Redis Lua script implementing the **Token Bucket Algorithm**:

```lua
-- KEYS[1]: Rate limit key, e.g., 'ratelimit:user_12345'
-- ARGV[1]: Max capacity 'C' (e.g., 10)
-- ARGV[2]: Refill rate 'r' tokens per millisecond
-- ARGV[3]: Current timestamp 'now' in milliseconds
-- ARGV[4]: Requested tokens (usually 1)

local key = KEYS[1]
local capacity = tonumber(ARGV[1])
local refill_rate = tonumber(ARGV[2])
local now = tonumber(ARGV[3])
local requested = tonumber(ARGV[4])

-- 1. Fetch current bucket state from Redis Hash
local data = redis.call("HMGET", key, "tokens", "last_refill")
local tokens = tonumber(data[1])
local last_refill = tonumber(data[2])

if tokens == nil then
    -- First request for this user: initialize bucket to full capacity
    tokens = capacity
    last_refill = now
else
    -- Compute elapsed time and lazy refill
    local delta = math.max(0, now - last_refill)
    tokens = math.min(capacity, tokens + (delta * refill_rate))
    last_refill = now
end

-- 2. Check if sufficient tokens exist
if tokens >= requested then
    tokens = tokens - requested
    redis.call("HMSET", key, "tokens", tokens, "last_refill", last_refill)
    -- Expire bucket if user is inactive for (capacity / refill_rate) ms
    local ttl = math.ceil(capacity / refill_rate / 1000)
    redis.call("EXPIRE", key, math.max(3600, ttl))
    return {1, math.floor(tokens)} -- Status: 1 (ALLOWED), remaining tokens
else
    redis.call("HMSET", key, "tokens", tokens, "last_refill", last_refill)
    return {0, math.floor(tokens)} -- Status: 0 (BLOCKED), remaining tokens
end
```

### 3. Client HTTP Headers Protocol
A compliant API must never silently discard or fail requests without providing structured feedback. RFC 6585 and IETF drafts dictate standard response headers:

- `X-RateLimit-Limit`: Maximum permitted request ceiling within the period (e.g., `100`).
- `X-RateLimit-Remaining`: Count of unused tokens or requests remaining in the active window (e.g., `3`).
- `X-RateLimit-Reset`: Unix epoch timestamp indicating when the quota fully refreshes (e.g., `1770198000`).
- When rejected (`429 Too Many Requests`):
  - `Retry-After`: Integer number of seconds the client must sleep before re-attempting (e.g., `12`).

```http
HTTP/1.1 429 Too Many Requests
Content-Type: application/json
Retry-After: 14
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1770198060

{
  "error": "rate_limit_exceeded",
  "message": "Quota of 100 requests per minute exceeded. Please retry in 14 seconds."
}
```

---

## Production Reliability: Failure Modes & Latency Optimization

### 1. Redis Failure Strategy: Fail Open vs Fail Closed
What happens if the Redis cluster crashes or suffers a network partition?
- **Fail Closed:** The API Gateway rejects 100% of incoming traffic. This protects backend databases from catastrophic collapse, but causes complete user-facing downtime.
- **Fail Open (Standard Best Practice):** If Redis connection times out (e.g., $> 20\text{ ms}$), the API Gateway logs a high-severity alert, bypasses the rate limiter, and permits the HTTP request through to backend services. Production platforms choose degraded service over guaranteed total outage.

### 2. Multi-Tiered Hybrid Rate Limiting
Querying a central Redis cluster over the network adds $1\text{ to }3\text{ ms}$ of latency to every single API call across your organization. At 500,000 QPS, Redis itself can become an architectural bottleneck.

To solve this, Tier-1 engineering teams use **Two-Tier Rate Limiting**:
1. **Local In-Memory Cache (Guava / LRU on Gateway):** Every gateway instance maintains a lightweight local token bucket that handles 80% of benign, regular client traffic with sub-microsecond local RAM access.
2. **Asynchronous Batch Synchronization:** Gateways flush token consumption deltas to centralized Redis in background batches every 200 ms, trading microsecond eventual consistency for massive horizontal scalability.

---

> [!NOTE]
> ### Teacher FAQ & Common Beginner Doubts
>
> **Q: What should I use as the rate limiting key: Client IP address or User ID?**  
> **Teacher's Answer:** In an interview, always mention that using raw IP address is flawed. Millions of corporate or university users share single egress NAT gateways (one public IP for 50,000 students); throttling by IP will block thousands of innocent users. Conversely, botnets rotate through tens of thousands of residential proxy IPs, rendering IP limits useless. The best practice is a **Hierarchical Keying Strategy**:
> - Authenticated endpoints: Throttle by `user_id` or `api_key`.
> - Unauthenticated endpoints (login/signup): Throttle by a composite key of `IP + User-Agent` or hashed fingerprint, coupled with CAPTCHA step-ups.
>
> **Q: Why shouldn't I use Redlock or distributed mutex locks for rate limiting?**  
> **Teacher's Answer:** Distributed locking introduces massive round-trip network overhead (acquiring the lock across multiple master nodes, executing operations, and releasing). Rate limiting is on the critical latency path of every single request. An atomic Redis Lua script executes directly in the Redis thread in sub-millisecond time without ever incurring lock contention or deadlock timeouts.
>
> **Q: How do we prevent clock drift between application servers and Redis?**  
> **Teacher's Answer:** Never use the application server's local machine time (`System.currentTimeMillis()`) to compute elapsed refill intervals, because Network Time Protocol (NTP) adjustments can make local clocks jump backward or skew by seconds. In the Lua script above, always query the Redis server's own internal clock via `redis.call('TIME')` to guarantee strict monotonic time ordering.
