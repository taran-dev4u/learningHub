# Redis & Distributed Caching

Welcome to the definitive masterclass on Redis and distributed in-memory data systems. In modern high-scale system design, microservices cannot rely on disk-based relational databases alone to service millions of requests per second. A single round-trip query to PostgreSQL or MySQL hitting disk takes between **2ms and 25ms**; under peak traffic, connection pool exhaustion and lock contention cause catastrophic cascading outages.

To survive at FAANG and Tier-1 scale, distributed architectures place an in-memory caching tier in front of persistent storage. Operating entirely in RAM with access times under **0.5 milliseconds**, **Redis (Remote Dictionary Server)** is the undisputed industry standard.

However, treating Redis as merely a naive string key-value store is a junior engineering mistake. In this masterclass, we explore the internal C memory data structures, single-threaded event loop mechanics, the **16,384 hash-slot cluster sharding protocol**, the controversial **Redlock distributed locking algorithm**, atomic Lua scripting for rate limiters, and memory eviction mathematics.

---

## Redis data types: strings, lists, sets, sorted sets, hashes, streams

### 1. The Single-Threaded Event Loop Architecture
How does Redis execute over **100,000 queries per second (QPS)** on a single CPU core?
- **Zero Lock Contention:** Because command execution is strictly single-threaded, Redis never acquires mutexes, never deadlocks, and never wastes CPU cycles on multi-threaded context switching.
- **I/O Multiplexing (epoll / kqueue):** Redis uses a non-blocking reactor pattern. The Linux `epoll` kernel mechanism monitors thousands of concurrent client TCP sockets simultaneously, dispatching events to the single worker thread only when data is ready to be processed.
- **In-Memory Operations:** All data resides in RAM. The CPU avoids slow memory bus walks and disk seeks.

### 2. Under-the-Hood Data Structures
Redis does not use generic programming language objects. It implements hand-crafted, memory-efficient C data structures:

| High-Level Redis Type | Underlying C Implementation | Memory & Time Complexity | Optimal System Design Use Case |
|---|---|---|---|
| **Strings** | **SDS (Simple Dynamic String)**: Binary-safe, pre-allocates buffer, stores length upfront ($O(1)$ `strlen` vs $O(N)$ in C). | Up to 512 MB. $O(1)$ read/write/append. | Session tokens, serialized JSON blobs, atomic counters (`INCRBY`). |
| **Hashes** | **ZipList** (small hashes) &rarr; **Dict** (hashtable with incremental rehashing). | $O(1)$ average field lookup. | User profiles, cart objects (mutate `user:101.status` without re-serializing entire JSON blob). |
| **Lists** | **QuickList** (a doubly linked list of compact ZipLists). | $O(1)$ push/pop at head or tail. | Recent activity timelines, producer-consumer task queues (`LPUSH` / `BRPOP`). |
| **Sets** | **IntSet** (integers) &rarr; **HashTable** (strings). | $O(1)$ membership test (`SISMEMBER`). | Unique visitor IP tracking, tag matching, mutual friend graph intersections (`SINTER`). |
| **Sorted Sets (ZSET)** | **Skiplist (Skip List) + HashTable**: Probabilistic multi-level linked list with logarithmic traversal. | $O(\log N)$ insertion, deletion, and rank search. | **Global gaming leaderboards, sliding window rate limiters, proximity geo-indexing.** |
| **Streams** | **Radix Tree of MacroNodes**: Append-only log with persistent consumer group offsets. | $O(1)$ append, $O(\log N)$ range lookup. | Durable event sourcing, distributed audit logs, lightweight Kafka alternatives. |
| **HyperLogLog** | **Probabilistic 12 KB Register**: Uses Flajolet-Martin stochastic counting algorithm. | Constant **12 KB** memory. Max error: **0.81%**. | Counting 1 billion Unique Daily Active Users (DAU) without storing raw IDs! |
| **Bitmaps** | Raw binary bits within a String using bitwise offsets (`SETBIT`, `BITCOUNT`). | 1 bit per user (100M users = **12 MB RAM**!). | Daily user retention login trackers, binary feature flag toggles. |

---

## Redis cluster — consistent hash ring, 16384 slots, automatic sharding

### 1. Scaling Beyond a Single Node
A single Redis instance is bounded by the physical RAM of a single server (e.g., 64 GB or 128 GB). What happens when your social platform or e-commerce catalog requires **2 Terabytes of active in-memory cache**?

**Redis Cluster** provides automatic distributed sharding, data partitioning, and high-availability master-replica failover across up to 1,000 nodes without a centralized proxy.

```
Total Keyspace Partitioned into 16,384 Hash Slots:

[Master Node 1] <--- Gossip Bus ---> [Master Node 2] <--- Gossip Bus ---> [Master Node 3]
 Slots: 0 - 5460                     Slots: 5461 - 10922                  Slots: 10923 - 16383
       |                                    |                                    |
   (Async)                              (Async)                              (Async)
       v                                    v                                    v
 [Replica 1A]                         [Replica 2A]                         [Replica 3A]
```

### 2. The 16,384 Hash Slot Formula
Instead of traditional consistent hashing rings, Redis Cluster maps the entire keyspace into exactly **16,384 discrete Hash Slots** (from 0 to 16,383):
$$	ext{Slot} = 	ext{CRC16}(	ext{Key}) \pmod{16384}$$

- **Why exactly 16,384 slots?**
  Redis nodes continuously exchange heartbeat packets using a binary gossip protocol. With 16,384 slots, the slot configuration bitmap occupies only **2 KB of memory** ($16384 / 8 = 2048 	ext{ bytes}$). If Redis used 65,536 slots, the gossip message header would bloat to 8 KB per ping, wasting cluster network bandwidth.
- **Hash Tags `{...}` for Multi-Key Operations:**
  Normally, multi-key operations (like transactions or `MGET`) fail in Redis Cluster if the keys land on different nodes. By wrapping an entity ID in braces (e.g., `{user:42}:profile` and `{user:42}:orders`), Redis hashes **only the string inside the curly braces**, guaranteeing that all data for user 42 hashes to the exact same node!

### 3. Client Routing: MOVED vs ASK Redirects
Redis Cluster is decentralized; there is no intermediate load balancer. Smart clients (like Lettuce or Jedis) maintain an internal slot-to-node cache:
- **`MOVED` Redirect:** The slot has permanently migrated to Node B. The client updates its local routing table and resends the command to Node B.
- **`ASK` Redirect:** The slot is currently mid-migration. The client sends an `ASKING` command to Node B for this single request only, without altering its long-term routing table.

---

## Redlock — distributed lock algorithm using multiple Redis instances

### 1. Single-Instance Mutex: The `SET NX PX` Pattern
In distributed microservices, tasks like batch billing or inventory reservation must run by at most one worker at any given time.
On a single Redis instance, an atomic distributed lock is acquired with:

```bash
SET lock:order_9912 "unique_client_worker_uuid" NX PX 30000
```
- `NX`: Only set the key if it **Does Not Exist** (atomic mutex).
- `PX 30000`: Expire the key after **30,000 milliseconds** (prevents deadlocks if the worker crashes).
- `unique_client_worker_uuid`: A cryptographically random value ensuring that only the worker who acquired the lock can release it via an atomic Lua script:
  ```lua
  if redis.call("get", KEYS[1]) == ARGV[1] then
      return redis.call("del", KEYS[1])
  else
      return 0
  end
  ```

### 2. The Single-Node Failover Flaw
Because Redis replication is asynchronous, a single-master setup cannot guarantee mutual exclusion:
1. Client A acquires the lock on Master.
2. Master crashes **before** replicating the key to its Replica.
3. Sentinel promotes the Replica to Master.
4. Client B requests the same lock. The new Master grants it!
5. **Both Client A and Client B now hold the lock simultaneously**, causing double billing or inventory corruption.

### 3. The Multi-Node Redlock Algorithm
To solve this, Salvatore Sanfilippo (antirez) designed **Redlock**:
- Deploy **$N = 5$ independent Redis master nodes** (physically isolated, no replication).
- To acquire the lock:
  1. Record current timestamp $T_1$.
  2. Attempt to acquire the lock on all 5 nodes sequentially with a small timeout (e.g., 5-50ms).
  3. The lock is successfully acquired **if and only if** the client acquires the lock on a **majority quorum** (at least $\ge \lfloor N/2 floor + 1 = 3$ nodes) **AND** total elapsed time $(T_2 - T_1)$ is less than lock validity time.
  4. If acquisition fails, the client immediately issues unlock commands to all 5 nodes.

> [!WARNING]
> **The Martin Kleppmann vs Redlock Debate:**
> Distributed systems researcher Martin Kleppmann published a famous critique of Redlock: Redlock relies on physical wall-clock time assumptions. If a client experiences an unexpected 10-second GC pause or OS thread descheduling, its lock validity expires while the client is asleep. When it wakes up, it proceeds to write to storage, unaware that another worker has already acquired the lock!
> **Production Recommendation:** For absolute financial safety, always pair distributed locks with **Fencing Tokens** (monotonically increasing version numbers verified by the database during mutation).

---

## Redis Pub/Sub — fan-out to WebSocket servers for scaling real-time

### 1. The Real-Time Fan-Out Problem
In applications like Discord, Slack, or live sports tickers, hundreds of thousands of users are connected via WebSockets across dozens of stateless application servers.
When a user sends a chat message into a room with 5,000 members, how does Server 1 broadcast the message to users connected to Server 8 and Server 12?

**Redis Pub/Sub** provides an ultra-low-latency in-memory message distribution bus:

```
[WebSocket Server 1]          [WebSocket Server 2]          [WebSocket Server 3]
 (Connected: User A)           (Connected: User B)           (Connected: User C)
        |                             |                             |
  (SUBSCRIBE room:42)           (SUBSCRIBE room:42)           (SUBSCRIBE room:42)
        \                             |                             /
         \                            |                            /
          v                           v                           v
     +-----------------------------------------------------------------+
     |                  REDIS PUB/SUB BUS                              |
     |         PUBLISH room:42 '{"text": "Hello Everyone!"}'           |
     +-----------------------------------------------------------------+
```

### 2. Mechanics & Production Trade-Offs
- **Push Model:** Redis pushes messages immediately to all subscribed client TCP buffers.
- **Fire-and-Forget (Zero Durability):** Redis Pub/Sub does **NOT buffer or persist messages on disk**. If WebSocket Server 2 experiences a 500ms network hiccup when the message is published, **the message is lost forever** for User B!
- **When to Use:** Ephemeral live notifications, chat presence, invalidation events.
- **When NOT to Use:** Critical billing events, order fulfillment, audit trails. (Use **Kafka** or **Redis Streams** instead).

---

## Redis sorted sets — use for leaderboards, rate limiting with sliding window

### 1. Global Leaderboards with Millions of Users
Calculating ranks in SQL via `ORDER BY score DESC LIMIT 10` forces expensive table scans and disk sorting.
In Redis, a **Sorted Set (ZSET)** maintains elements ordered by a floating-point score using an in-memory **Skiplist** and **Hash Table**:
- `ZADD leaderboard 4500 "user_101"`: Inserts or updates score in $O(\log N)$ time.
- `ZREVRANGE leaderboard 0 9 WITHSCORES`: Fetches top 10 players globally in $O(\log N + M)$ time (sub-millisecond!).
- `ZREVRANK leaderboard "user_101"`: Returns the exact global standing (e.g., Rank #42 out of 10 million players) in $O(\log N)$ time!

### 2. Sliding Window Rate Limiting (Atomic Lua Script)
Fixed-window rate limiters suffer from the **Boundary Burst Problem** (a user sends 100 requests at 11:59:59 and another 100 at 12:00:01, doubling allowable traffic).
A **Sliding Window Log Rate Limiter** uses a Redis ZSET where:
- **Member:** Unique request ID or random UUID.
- **Score:** Current Unix timestamp in milliseconds.

```
Time Window (Last 60 Seconds):
[t - 60s] -----------------------------------------------------> [Current Time t]
  |--- (Purge older requests via ZREMRANGEBYSCORE) --->|
                                                       |--- (Count remaining via ZCARD) --->
```

#### Production Lua Script for Zero Race Conditions:
Executing multiple Redis commands from Python/Go creates network round-trips and race conditions. A Redis Lua script runs **atomically** on the Redis server:

```lua
-- KEYS[1]: Rate limit key (e.g., rate_limit:user:42)
-- ARGV[1]: Current timestamp in milliseconds
-- ARGV[2]: Window size in milliseconds (e.g., 60000 for 1 minute)
-- ARGV[3]: Maximum allowed requests (e.g., 100)

local key = KEYS[1]
local now = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local limit = tonumber(ARGV[3])
local clear_before = now - window

-- 1. Remove expired requests outside the sliding window
redis.call('ZREMRANGEBYSCORE', key, 0, clear_before)

-- 2. Count current active requests in window
local current_requests = redis.call('ZCARD', key)

if current_requests < limit then
    -- 3. Add current request and reset TTL
    redis.call('ZADD', key, now, now)
    redis.call('PEXPIRE', key, window)
    return 1 -- Allowed
else
    return 0 -- Rejected (HTTP 429 Too Many Requests)
end
```

---

### Memory Eviction Policies: When RAM is Exhausted
When Redis reaches `maxmemory`, it enforces one of 8 eviction policies:
1. **`noeviction`:** Returns errors on writes; safe for billing where data must never be lost.
2. **`allkeys-lru`:** Evicts least recently used keys across all keys; standard for general web caching.
3. **`volatile-lru`:** Evicts least recently used keys *only among keys with an expiration TTL set*.
4. **`allkeys-lfu`:** Evicts least frequently used keys; optimal when popular items stay hot over long durations.

---

> [!TIP]
> **Summary Decision Rule for System Design Interviews:**
> - Use **Redis Strings** for basic caching, distributed rate-limit counters, and idempotency locks.
> - Use **Redis Hashes** for structured domain models (user profiles, product attributes) to save memory and avoid full JSON serialization.
> - Use **Redis Sorted Sets (ZSET)** for global leaderboards and high-precision sliding-window rate limiters.
> - Use **Redis Cluster (16,384 slots)** when dataset size exceeds single-machine RAM (> 64 GB) or write throughput exceeds 100k QPS.
> - Deploy **Redlock + Fencing Tokens** when distributed coordination requires strict mutual exclusion.
