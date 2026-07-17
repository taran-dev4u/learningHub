# Redis & Distributed Caching

When discussing caching in modern System Design interviews, **Redis** is the undisputed king. Redis (Remote Dictionary Server) is an open-source, in-memory data structure store. It is completely single-threaded (for command execution), ridiculously fast (sub-millisecond latency), and far more than just a simple key-value store.

To demonstrate seniority, you must move beyond saying "I'll put it in Redis." You need to explain *which data structure* you will use and *how you will scale it*.

---

## 1. Redis Data Types: Beyond Key-Value

Redis is famous for its rich data types, which push computation down to the database layer rather than forcing the application to process data.

| Data Type | Description | Best System Design Use Cases |
| :--- | :--- | :--- |
| **Strings** | Basic key-value (up to 512MB). Can increment integers. | Session tokens, JSON blobs, page views counters. |
| **Lists** | Linked lists of strings. Push/pop from head or tail. | Recent activity feeds, simple message queues, timeline arrays. |
| **Sets** | Unordered collections of unique strings. O(1) membership. | Tracking unique IP addresses, tags on a blog post, mutual friends (set intersection). |
| **Sorted Sets** | Sets ordered by a "score" (float). O(log N) updates. | Gaming leaderboards, proximity-based geo-search, sliding window rate limiters. |
| **Hashes** | Maps of string fields and string values (like a JSON object). | User profiles (update only the `avatar_url` without fetching the whole object). |
| **Streams** | Append-only log data structure (similar to Kafka). | Event sourcing, consumer groups processing background jobs. |

---

## 2. Redis Cluster & Automatic Sharding
### Scaling Beyond a Single Machine

A single Redis instance can hold tens of gigabytes of data and process ~100,000 QPS. But what if you need to store 5 Terabytes of cache? You use **Redis Cluster**.

**How it works:**
Redis Cluster uses a form of algorithmic sharding. The keyspace is divided into **16,384 Hash Slots**.
- When you set a key, Redis runs: `HASH_SLOT = CRC16(key) mod 16384`.
- If you have 3 Redis master nodes, Node A holds slots 0–5500, Node B holds 5501–11000, and Node C holds 11001–16383.
- When you add Node D, the cluster automatically moves a fraction of slots from A, B, and C over to D without downtime.

**Real-World Analogy:**
Imagine 16,384 safety deposit boxes. Instead of one bank vault, you have three bank vaults, each managing a third of the boxes. When a customer brings a key, the mathematical shape of the key tells them exactly which vault to go to.

---

## 3. Redlock: Distributed Locking
### Preventing Concurrency Disasters

In a distributed system, you often have 50 application servers running concurrently. If a cron job needs to process daily billing, you absolutely cannot have two servers running the billing script at the same time (double charging customers).

You use Redis to create a **Distributed Lock**.

**How it works (Redlock Algorithm):**
1. Server A tries to acquire a lock by writing a key: `SET lock:billing "serverA_uuid" NX PX 30000`.
   - `NX` means "Only set if it Does Not Exist" (atomic).
   - `PX 30000` is a 30-second TTL (so if Server A crashes, the lock is eventually released).
2. If successful, Server A processes billing.
3. If Server B tries to acquire the lock, the `NX` flag causes the command to fail. Server B backs off.

> [!WARNING]
> Standard Redis locking on a single node has a single point of failure. The official **Redlock algorithm** requires acquiring the lock across a quorum (e.g., 3 out of 5) of independent Redis master nodes to guarantee safety even if a Redis node crashes.

---

## 4. Redis Pub/Sub
### Real-Time Fan-Out

Redis Pub/Sub (Publish/Subscribe) is a messaging paradigm where senders push messages to "channels" without knowing who the receivers are.

**How it works:**
A WebSocket server maintains live connections with 10,000 users. When User A sends a chat message to a massive group, the chat service publishes the message to a Redis channel. All WebSocket servers subscribed to that channel instantly receive the message and push it down to the connected clients.

**Trade-offs:**
Pub/Sub is "fire and forget." If a subscriber is temporarily disconnected when the message is published, they will **never** receive it. For durable messaging, you must use Redis Streams or Kafka.

---

## 5. Redis Sorted Sets (Leaderboards & Rate Limiting)
### The ZSET Magic

**Sorted Sets (ZSET)** are one of Redis's most powerful features for interviews. Every element has a score. Redis keeps the set perfectly sorted in memory at all times.

**Use Case 1: Global Leaderboards**
If you are designing a game with 10 million players, running `SELECT * FROM users ORDER BY score DESC LIMIT 10` in SQL is too slow. In Redis:
`ZADD leaderboard 1500 "player_55"` (O(log N))
`ZREVRANGE leaderboard 0 9` (O(log N)) instantly returns the top 10 players globally.

**Use Case 2: Sliding Window Rate Limiting**
To prevent API abuse, you can use a ZSET where the member is the request UUID, and the score is the UNIX timestamp.
When a request comes in:
1. `ZREMRANGEBYSCORE` to delete all requests older than 1 minute.
2. `ZCARD` to count how many requests remain. If > 100, reject the request.
3. `ZADD` to add the current request timestamp.

---

> [!NOTE]
> ### 🎓 Teacher FAQ & Common Beginner Mistakes
>
> **Q: "Is Redis always in-memory? What if it crashes, do I lose everything?"**
> Redis is an in-memory database, but it offers **durability** via two mechanisms:
> 1. **RDB (Redis Database):** Point-in-time snapshots to disk (e.g., every 5 minutes). Fast, but you can lose minutes of data.
> 2. **AOF (Append Only File):** Logs every single write operation to disk as it happens. Slower, but highly durable.
> In interviews, clarify that Redis isn't purely ephemeral unless you configure it to be.
>
> **Q: "Why wouldn't I just use Memcached instead?"**
> Memcached is a fantastic, pure, multi-threaded key-value store. It is great for simple HTML string caching. However, Redis won the caching war because of its advanced data structures (Hashes, Sets, ZSets) and persistence options. If an interviewer asks you to compare them, mention that Memcached is multi-threaded (better vertical scaling on large instances for simple values), while Redis is single-threaded but feature-rich.
