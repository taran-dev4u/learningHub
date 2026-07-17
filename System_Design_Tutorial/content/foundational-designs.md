# Foundational Designs

Welcome to the Foundational Designs masterclass. In this module, we will explore the core building blocks of modern distributed systems. These aren't just academic exercises; these are the actual architectures powering the internet. By understanding these deeply, you will be equipped to tackle any system design interview and architect real-world solutions.

---

## 1. URL Shortener (TinyURL/bit.ly) — Hash + Base62, Collision Handling, Analytics

When you look at a service like TinyURL, it seems trivially simple. You paste a long URL, and it gives you a short one. But beneath that simple facade lies a fascinating lesson in scalability, database choices, and mathematical transformations.

### Why Do We Need URL Shorteners?
Think of a URL shortener like a coat check at a fancy restaurant. You hand the attendant your heavy, bulky winter coat (the long URL), and they hand you back a tiny, easy-to-carry paper ticket with a number on it (the short URL). When you want your coat back, you just hand them the ticket, and they know exactly which coat is yours. We need this because platforms like Twitter originally had strict character limits, and long URLs can break in plain-text emails or look visually unappealing.

### Capacity Estimation & Math
Before we design, we must estimate. Let's assume:
* **Write load (new URLs):** 100 million per month.
* **Read load (clicks):** 10 billion per month (100:1 read-to-write ratio).

Let's calculate the Queries Per Second (QPS):
* **Write QPS:** `100,000,000 / (30 days * 24 hrs * 3600 sec) ≈ 40 URLs/second`.
* **Read QPS:** `10,000,000,000 / (30 * 24 * 3600) ≈ 4000 reads/second`.

Storage requirements for 10 years:
* `100 million * 12 months * 10 years = 12 billion records`.
* If each record is 500 bytes: `12 billion * 500 bytes = 6 Terabytes (TB)`.

This tells us two things: our system is incredibly **read-heavy**, and the storage is easily manageable on a few modern SSDs, but we still need a distributed database for high availability and throughput.

### The Core Logic: Hashing vs. Base62

How do we generate the short string? We have two main approaches.

#### Approach A: Hashing (MD5 or SHA-1)
If we hash the long URL using MD5, we get a 128-bit string (32 hex characters). But we only want 7 characters! If we take the first 7 characters of the MD5 hash, we risk **collisions** (two different URLs resulting in the same 7-character string).
If a collision happens, we append a predefined string or a sequence number and hash again. This requires a database round-trip to check if the hash exists.

#### Approach B: Base62 Conversion (The Industry Standard)
Instead of hashing the URL, we use an auto-incrementing integer (a unique ID generator like Twitter Snowflake or a centralized counter) and convert that integer into a Base62 string.
Base62 uses `[a-z, A-Z, 0-9]` which gives 62 possible characters.
* A 7-character Base62 string can represent `62^7 ≈ 3.5 trillion` unique URLs!
* Since the integer is strictly increasing, **collisions are mathematically impossible**.

> [!TIP]
> **Base62 Algorithm:**
> Let's say our unique ID is 125.
> `125 % 62 = 1` (character 'b')
> `125 / 62 = 2`
> `2 % 62 = 2` (character 'c')
> So, ID 125 becomes 'cb'.

### Architecture & Data Flow
1. Client sends a POST request with the long URL.
2. Web Server talks to a Unique ID Generator (e.g., ZooKeeper or a dedicated service) to get an integer ID.
3. Web Server converts the ID to Base62.
4. Web Server saves the mapping `{ short_url, long_url, user_id, timestamp }` in a NoSQL database (like Cassandra or DynamoDB) because we don't need complex relational joins, and we want high availability.
5. On a read request, the Web Server checks a Distributed Cache (Redis/Memcached). If there's a cache miss, it fetches from the DB, updates the cache, and sends an `HTTP 301` or `HTTP 302` redirect.

### Table: 301 vs 302 Redirect

| Feature | HTTP 301 (Permanent) | HTTP 302 (Temporary) |
| :--- | :--- | :--- |
| **Caching** | Browser caches the redirect. Future requests go directly to the long URL. | Browser does NOT cache. Every request hits our shortener service. |
| **Server Load** | Significantly lower, as we are bypassed on subsequent clicks. | Higher, as we process every single click. |
| **Analytics** | Terrible. We can't track how many times a user clicked because the browser bypassed us. | Excellent. We can track geolocation, device types, and click counts accurately. |

> [!NOTE]
> **Teacher FAQ: Why not use a relational database with an AUTO_INCREMENT primary key?**
> Beginners often suggest MySQL with `AUTO_INCREMENT`. While this works for a small scale, a single relational master database becomes a single point of failure and a bottleneck for writes. In a massive distributed system, generating sequential IDs across multiple data centers requires specialized services (like Twitter Snowflake) to ensure uniqueness without severe latency.

---

## 2. Distributed Cache (Redis cluster) — Consistent Hashing, Eviction, Replication

A cache is the secret sauce of performance. It stores frequently accessed data in RAM so that we don't have to repeatedly query our slow, disk-based databases. But what happens when one machine isn't enough to hold all our cached data? We must distribute it.

### The Problem with Simple Hashing
Imagine you have 4 Redis servers (N=4). To decide which server holds a specific key (e.g., `user:101`), you calculate `hash(key) % 4`.
This works perfectly until Black Friday hits, and you need to add a 5th server (N=5).
Suddenly, the formula is `hash(key) % 5`. Almost every single key will now map to a *different* server than before. Your cache hit rate drops to zero instantly. Your databases get slammed with requests, and the system crashes. This is known as a **cache stampede**.

### The Solution: Consistent Hashing
Think of Consistent Hashing like a giant roulette wheel (a ring) numbered from 0 to 359 degrees.
1. We hash our server IP addresses and place them on the ring (e.g., Server A at 10°, Server B at 90°).
2. We hash our data keys and place them on the same ring (e.g., Key 1 at 45°).
3. To find which server holds Key 1, we start at 45° and walk clockwise around the wheel until we hit a server (Server B at 90°).

If we add a new Server C at 50°, only the keys between 10° and 50° are reassigned to Server C. The rest of the ring remains completely untouched! We've solved the massive remapping problem.

### Virtual Nodes (VNodes)
In reality, placing just 4 servers on a massive ring leads to uneven data distribution. Server A might handle 80% of the wheel while Server B handles 5%.
To fix this, we create **Virtual Nodes**. We place Server A on the ring 100 times, Server B 100 times, etc., randomly scattered. This ensures a beautifully even distribution of data.

### Eviction Policies
RAM is expensive and limited. When the cache is full, who gets kicked out?

| Policy | How it works | Best Used For |
| :--- | :--- | :--- |
| **LRU (Least Recently Used)** | Evicts the item that hasn't been accessed for the longest time. | Standard web traffic, news articles, user profiles. |
| **LFU (Least Frequently Used)** | Evicts the item that has the lowest total access count. | Static assets, configurations that are occasionally checked. |
| **FIFO (First In, First Out)** | Evicts the oldest item, regardless of access patterns. | Time-series data, temporary tokens. |

> [!WARNING]
> **Common Beginner Mistake:** Assuming the cache is always perfectly synced with the database.
> You must handle **Cache Invalidation**. If a user updates their profile in the database, the old data in the cache must be explicitly deleted or updated. A common pattern is **Cache-Aside**: the application updates the DB and then deletes the cache key. The next read will naturally fetch the fresh DB data and repopulate the cache.

---

## 3. Key-Value Store — LSM Tree, Compaction, Range Queries

When we talk about massively scalable Key-Value stores like Cassandra, HBase, or RocksDB, we have to talk about how they store data on disk. Traditional relational databases use B-Trees, which are great for reads but terrible for high-volume writes because they require constant disk seeking and rebalancing.

### Why B-Trees Fail at Scale
Imagine writing a book by opening it, finding the exact alphabetical page for every new word, erasing lines, and rewriting them. That is a B-Tree write (random I/O). It's agonizingly slow.

### The LSM Tree (Log-Structured Merge-Tree)
The LSM Tree solves this by treating the database like an append-only log. Imagine writing all your thoughts sequentially in a notebook. You never go back and erase; if you change your mind, you just write the new thought at the end of the notebook. This is sequential I/O, which is incredibly fast on modern hard drives.

#### 1. The MemTable
When a write comes in, it goes directly into RAM in a sorted structure called a **MemTable** (often a Red-Black tree or Skip List). Because it's in RAM, it's lightning fast. To ensure we don't lose data if the power goes out, we simultaneously append the raw write to an append-only **Write-Ahead Log (WAL)** on disk.

#### 2. The SSTable (Sorted String Table)
When the MemTable gets too big (e.g., 16MB), it is flushed to disk as an **SSTable**. An SSTable is an immutable (unchangeable) file containing a sorted list of key-value pairs.
If a key is updated, it just gets written to a newer SSTable. If it's deleted, a "tombstone" marker is written to indicate deletion.

#### 3. Compaction
Over time, you will have hundreds of SSTables. To read a key, you might have to check many files. To prevent this, a background process called **Compaction** merges old SSTables together, discards the old versions of keys, removes tombstoned keys, and writes a fresh, consolidated SSTable.

### Range Queries
Because data within an SSTable is sorted by key, performing range queries (e.g., "Give me all users between IDs 1000 and 2000") is extremely efficient. The database uses an index to find the start of the block and then sequentially reads the keys.

> [!NOTE]
> **Teacher FAQ: If reads have to check multiple SSTables, aren't reads slow?**
> Yes, naive reads in an LSM tree are slower than B-Trees. To fix this, we use **Bloom Filters**. A Bloom Filter is a highly memory-efficient probabilistic data structure that can tell you definitively if a key is *not* in an SSTable. Before checking a disk file, the database checks the Bloom filter in RAM. If it says "No", we skip the file entirely, saving an expensive disk read.

---

## 4. Content Delivery Network (CDN) — Pull vs Push, Origin Shield, Cache Invalidation

A CDN is a geographically distributed network of proxy servers. Its goal is to provide high availability and high performance by serving content closer to end-users.

### The Real-World Analogy
Imagine a famous bakery in Paris (the Origin Server). People in Tokyo want the croissants, but shipping them individually takes 14 hours (high latency) and the bakery is overwhelmed (high load).
A CDN is like setting up franchise bakeries (Edge Servers) in Tokyo, New York, and Sydney. The franchises keep copies of the pastries. When a Tokyo resident wants a croissant, they get it instantly from the local Tokyo shop.

### Pull vs. Push CDNs

| Strategy | How It Works | Best For |
| :--- | :--- | :--- |
| **Pull CDN** | The CDN is passive. When a user requests an image, the Edge Server checks if it has it. If not, it "pulls" it from the Origin Server, caches it, and serves the user. | High-traffic sites with millions of dynamic assets (images, CSS, JS). You only cache what is actually requested. |
| **Push CDN** | The developers explicitly upload ("push") content to the CDN edge servers during their deployment process. | Small sites or highly static content (like a game patch or a video release) where you want 100% cache hits immediately. |

### The Origin Shield
What happens if a popular video drops, and all 500 edge servers globally realize they don't have it? They will all send a request to your Origin Server simultaneously, potentially crashing it. This is a cache stampede at the CDN level.
An **Origin Shield** is an intermediate caching layer placed directly in front of the Origin Server.
The 500 edge servers don't talk to the Origin; they talk to the Shield. The Shield collapses the 500 requests into a *single* request to the Origin, gets the video, caches it, and distributes it to the edges.

### Cache Invalidation Strategies
When content changes (e.g., updating a company logo), the CDN edges will still serve the old cached version until the Time-To-Live (TTL) expires.
1. **Purge/Invalidate API:** Send a command to the CDN provider to aggressively delete the cache. This can be slow.
2. **Object Versioning (Recommended):** Instead of overwriting `logo.png`, you upload `logo_v2.png` and update your HTML to point to the new URL. The CDN treats this as a brand new request, guaranteeing the latest asset is served instantly.

---

## 5. Rate Limiter (Distributed) — Token Bucket in Redis, Per-User Limits

A rate limiter controls the rate of traffic sent by a client or a service. It protects your APIs from DoS attacks, brute-force login attempts, and prevents single users from monopolizing server resources.

### The Algorithms

#### 1. Token Bucket (The Industry Standard)
Imagine a literal bucket that holds a maximum of 10 tokens. A background process drops 1 new token into the bucket every second.
When a user makes an API request, they must take a token out of the bucket.
* If the bucket has tokens: Request proceeds.
* If the bucket is empty: Request is dropped (HTTP 429 Too Many Requests).
**Why it's great:** It allows for short bursts of traffic (up to the bucket capacity) while maintaining a steady long-term rate. Stripe and Amazon use this.

#### 2. Leaky Bucket
Imagine a bucket with a hole in the bottom. Water (requests) pours in from the top. If water pours in faster than it leaks out, the bucket overflows, and requests are dropped.
**Why it's great:** It smooths out traffic into a perfectly steady stream.

#### 3. Sliding Window Log
Keep a timestamp log of every request a user makes in Redis. When a new request arrives, delete all timestamps older than 1 minute. If the remaining count is less than the limit, accept the request.
**Why it's bad:** Storing arrays of timestamps for millions of users consumes a massive amount of memory.

### Distributed Rate Limiting with Redis
In a distributed environment, user requests might hit Server A, then Server B. Storing rate limit counters in the local memory of a single server won't work.
We must use a centralized Redis cluster.

However, a naive implementation creates a **Race Condition**:
1. Server A reads the token count (it's 1).
2. Server B reads the token count (it's 1).
3. Server A decrements to 0.
4. Server B decrements to 0.
Both servers allowed a request, but there was only 1 token!

> [!IMPORTANT]
> **The Solution: Redis Lua Scripts**
> To solve race conditions, we use Lua scripts in Redis. Redis executes Lua scripts atomically. We write a script that checks the token count and decrements it in one atomic, uninterrupted operation. No race conditions, perfect accuracy.

---

## 6. Distributed Job Scheduler — Priority Queues, At-Least-Once Execution, Dedup

How do you build a system that executes jobs (like sending emails, processing payments, or generating reports) reliably, in the background, across thousands of worker nodes?

### The Architecture
1. **Client/Submitter:** Submits a job payload to a central queue.
2. **Message Broker (RabbitMQ / Kafka / SQS):** Holds the jobs. It acts as the buffer between fast submitters and slower workers.
3. **Worker Nodes:** Servers that continuously poll the broker for new jobs and execute them.
4. **Metadata Store (MySQL / Postgres):** Tracks the state of every job (Pending, Running, Failed, Completed) for auditing.

### Priority Queues
Not all jobs are equal. A password reset email (high priority) shouldn't wait behind 10,000 weekly newsletter emails (low priority).
Instead of a single queue, we use multiple queues based on priority. Workers are configured to drain the High Priority Queue completely before looking at the Low Priority Queue.

### Delivery Guarantees
* **At-Most-Once:** A job is delivered once. If the worker crashes mid-execution, the job is lost forever. (Terrible for payments).
* **At-Least-Once (Standard):** The broker delivers the job. It waits for an `ACK` (acknowledgment) from the worker. If the worker crashes before sending the `ACK`, the broker assumes failure and puts the job back in the queue to be processed by another worker.

### The Idempotency Problem (Dedup)
Because of "At-Least-Once" delivery, a worker might process a payment, but crash right before sending the `ACK`. The broker re-queues the job, and another worker processes the *same payment again*. The customer is charged twice.
**Idempotency** means an operation can be applied multiple times without changing the result beyond the initial application.

> [!TIP]
> **How to implement Idempotency:**
> Every job must have a unique `Idempotency-Key` (a UUID generated by the client).
> Before a worker executes a job, it checks the database: "Have I seen this Idempotency-Key before?"
> If yes, skip the execution and return success. If no, insert the key into the DB and proceed. This guarantees exactly-once processing semantics at the application layer.

### Dead Letter Queue (DLQ)
What if a job contains a bug that always crashes the worker? It will be re-queued infinitely, creating a "poison pill" that blocks the queue.
To fix this, we configure a retry limit (e.g., 3 attempts). If a job fails 3 times, the broker automatically moves it to a **Dead Letter Queue**. Engineers can then inspect the DLQ, fix the bug, and manually re-process the jobs.
