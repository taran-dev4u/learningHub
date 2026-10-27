# Cache Failure Modes & Pitfalls

Caching is frequently treated as an architectural panacea. When a PostgreSQL or MySQL database exhibits 99th-percentile query latency of 400ms under heavy traffic, the instinctive reaction is to insert a Redis or Memcached cluster in front of it, dropping latency to 2ms.

However, distributed caching introduces intricate failure modes. When a caching layer malfunctions, it does not fail gracefully—it typically causes a **cascading collapse of the persistent database tier**.

As a senior or staff engineer, you are expected to understand not just how caching accelerates happy-path reads, but how to engineer bulletproof defenses against the five classic cache catastrophes: **Stampede (Thundering Herd)**, **Penetration**, **Avalanche**, **Hot Key (Celebrity Problem)**, and **Inconsistency Drift**.

---

## Cache stampede / thundering herd — many requests hit DB simultaneously on cache miss

### 1. Anatomy of a Stampede
A **Cache Stampede** (also known as the **Thundering Herd Problem**) occurs when a single, heavily requested cache key expires or is evicted while the system is serving thousands of concurrent requests per second.

```
Time: T0 (Cache Valid)
Clients 1..10,000 ---> [ Redis: Key "product:1001" (HIT) ] ---> Return in 2ms. (DB QPS = 0)

Time: T1 (Key Expires at second 60.000)
Client 1        ---> [ Redis: MISS ] ---------------------------> [ SQL DB: Heavy Query ]
Client 2        ---> [ Redis: MISS ] ---------------------------> [ SQL DB: Heavy Query ]
Client 3        ---> [ Redis: MISS ] ---------------------------> [ SQL DB: Heavy Query ]
...
Client 10,000   ---> [ Redis: MISS ] ---------------------------> [ SQL DB: Heavy Query ]

Result: 10,000 concurrent database connections spawn in 5ms.
DB Connection Pool Exhausted -> CPU at 100% -> DB Crashes -> Cascade to all services!
```

### 2. The Root Cause: Lack of Synchronization
In standard Cache-Aside logic:
1. Every application thread executes: `val = cache.get(key)`.
2. If `val is None`, *every thread independently* assumes responsibility for recomputing or querying the database.
3. If computing that key requires a 150ms SQL query with multiple table joins, all incoming traffic during that 150ms window hammers the relational database simultaneously.

---

## Fix: mutex / lock around cache miss, OR probabilistic early expiry

Senior engineers employ two distinct architectural patterns to eliminate cache stampedes:

### 1. Distributed Mutex Locking (Single-Flight Pattern)
When a cache miss occurs, the application threads do not all query the database. Instead, only the first thread acquires a distributed mutex lock for that specific key. All remaining threads wait briefly and re-read the cache.

```python
import time, json, uuid

def get_product_with_mutex(product_id: str, redis_client, db_client):
    cache_key = f"product:{product_id}"
    lock_key = f"lock:{cache_key}"
    
    # 1. First cache check
    val = redis_client.get(cache_key)
    if val:
        return json.loads(val)
        
    # 2. Acquire distributed lock (5-second timeout to prevent deadlocks)
    lock_token = str(uuid.uuid4())
    acquired = redis_client.set(lock_key, lock_token, nx=True, ex=5)
    
    if acquired:
        try:
            # Re-check cache inside lock (Double-Checked Locking Pattern)
            val = redis_client.get(cache_key)
            if val:
                return json.loads(val)
                
            # 3. Only ONE thread executes the expensive database query
            data = db_client.query("SELECT * FROM products WHERE id = %s", product_id)
            redis_client.setex(cache_key, 3600, json.dumps(data))
            return data
        finally:
            # Safe Lua script release verifying token ownership
            release_script = """
            if redis.call("get", KEYS[1]) == ARGV[1] then
                return redis.call("del", KEYS[1])
            else
                return 0
            end
            """
            redis_client.eval(release_script, 1, lock_key, lock_token)
    else:
        # 4. Other threads wait 50ms and retry reading cache
        time.sleep(0.05)
        return get_product_with_mutex(product_id, redis_client, db_client)
```

### 2. Probabilistic Early Expiration (The XFetch Algorithm)
In 2015, researchers from Vrije Universiteit Amsterdam and Salesforce published the seminal paper on the **XFetch algorithm** (Optimal Probabilistic Cache Stampede Prevention).

Instead of waiting for a key to strictly hit its hard expiration time $T$, requests probabilistically choose to refresh the cache in the background *before* it expires:

$$	ext{Should Refresh?} \iff -eta 	imes \delta 	imes \ln(	ext{rand}()) > 	ext{TTL}_{	ext{remaining}}$$

Where:
- $\delta$ is the delta computation time (how many seconds it takes to query the DB and compute the value).
- $eta > 0$ is an aggressiveness tuning multiplier (usually set to $1.0$).
- $	ext{rand}() \sim U(0, 1)$ generates a uniform random float between 0 and 1.
- As $	ext{TTL}_{	ext{remaining}} 	o 0$, the probability of a background refresh smoothly approaches 100%.

**The Triumph of XFetch:** The more popular a key is (higher QPS), the earlier and more reliably it gets refreshed in the background *without a single thread ever encountering a cache miss or waiting for a mutex lock*!

---

## Cache penetration — queries for non-existent keys bypass cache

### 1. The Vulnerability
**Cache Penetration** occurs when an external caller systematically queries keys that **do not exist in the database**.

```
Attacker Script:
GET /api/users/999999999999   ---> Redis: MISS ---> DB Query: SELECT ... (0 rows)
GET /api/users/999999999998   ---> Redis: MISS ---> DB Query: SELECT ... (0 rows)
GET /api/users/999999999997   ---> Redis: MISS ---> DB Query: SELECT ... (0 rows)
```

Because the records do not exist, the database returns empty results (`null` / empty set). Historically, naive code does not write `null` to Redis. Consequently:
- Every single malicious or erroneous request completely bypasses the caching layer.
- The relational database is forced to execute full primary key index seeks and table scans for non-existent records, saturating DB I/O.

---

## Fix: cache null values with short TTL, OR bloom filter at cache layer

Senior engineers deploy two defenses depending on data cardinality:

| Architectural Defense | How It Works | Trade-offs & Memory Footprint | Best Use Case |
|---|---|---|---|
| **Caching Null Values** | Store `SET key "NULL" EX 30` when DB returns empty. | Consumes Redis memory for junk keys. High key cardinality can evict legitimate hot keys. | Low volume of missing lookups; simple to implement. |
| **Bloom Filter at Edge** | Place a bit array in front of Redis. If Bloom filter returns "Negative", reject immediately! | Requires memory for bit array; zero false negatives, but small tunable false positive rate (e.g. 1%). | Massive ID space (e.g., e-commerce product catalog with millions of IDs). |

### 1. Bloom Filter Mathematical Mechanics
A Bloom filter is a space-efficient probabilistic data structure based on an array of $m$ bits and $k$ independent hash functions.
- To insert key $x$: compute $h_1(x), h_2(x), \dots, h_k(x)$ and set all corresponding bit indices to `1`.
- To query key $y$: check bits at $h_1(y), \dots, h_k(y)$.
  - If **ANY bit is 0**: the element is **guaranteed 100% NOT in the database**. Return 404 immediately without touching Redis or SQL!
  - If **ALL bits are 1**: the element *might* be in the database (proceed to cache/DB).

$$	ext{Optimal Bits: } m = -rac{n \ln p}{(\ln 2)^2}, \quad 	ext{Optimal Hash Functions: } k = rac{m}{n} \ln 2$$

> [!TIP]
> To protect 100 million product IDs with a false positive rate $p = 1\%$, a Bloom filter requires only **114 MB of RAM**! That is small enough to fit inside a single Redis instance or directly in application server memory.

---

## Cache avalanche — many keys expire simultaneously, DB overwhelmed

### 1. Anatomy of an Avalanche
A **Cache Avalanche** happens when a large proportion of keys across the entire cache cluster expire at the exact same point in time, or when a primary Redis instance restarts and boots up with an empty in-memory state.

```
Scenario: Batch ETL job runs at 12:00 AM and writes 5,000,000 product categories with TTL = 24 hours.

Time: 11:59:59 PM (Cache Hit Rate: 99.8%)
Time: 12:00:00 AM (5,000,000 keys expire simultaneously across the cluster!)

Result: Cache Hit Rate drops from 99.8% to 0.1% within 100 milliseconds!
A tsunami of diverse queries slams the database replicas, triggering failover loops and cascaded outages.
```

### 2. The Solutions: TTL Jitter and Warm-Up
1. **TTL Jitter (Random Uniform Perturbation):**
   Never use a static integer TTL. Always inject entropy:
   $$	ext{Actual TTL} = 	ext{Base TTL} + 	ext{random}(0, 	ext{Jitter Window})$$
   ```python
   import random

   def set_with_jitter(redis_client, key, value, base_ttl=3600, jitter_max=300):
       # Spreads expirations smoothly over a 5-minute window
       ttl = base_ttl + random.randint(0, jitter_max)
       redis_client.setex(key, ttl, value)
   ```
2. **Pre-Warming & Staged Traffic Shifting:**
   When spinning up a new cache node or deploying after maintenance:
   - Run a warm-up script that queries top-10% hot keys based on yesterday's access logs.
   - Use weighted load balancing (e.g. Envoy canary weighting) to slowly ramp up traffic from 5% $	o$ 25% $	o$ 100% over 10 minutes.

---

## Hot key — one key receives disproportionate traffic (celebrity problem)

### 1. The Scaling Bottleneck of Distributed Hashes
In a distributed Redis cluster, keys are mapped to 16,384 hash slots using CRC16:
$$	ext{Slot} = 	ext{CRC16}(	ext{key}) \pmod{16384}$$

Even if you scale your Redis cluster to 128 nodes with 10 terabytes of RAM:
- A specific key (e.g. `celebrity:taylorswift:posts` or `flash_sale:iphone16`) **strictly resides on exactly ONE Redis shard**!
- If 2 million requests per second target that single key, that single server's 10Gbps Network Interface Card (NIC) and single-threaded CPU core will saturate at 100%, causing connection timeouts and crashing the node, while the other 127 Redis nodes sit at 1% CPU utilization!

### 2. Architectural Solutions for Hot Keys
1. **Multi-Tier Caching (L1 Local In-Memory + L2 Distributed Redis):**
   - Application servers run a local in-process cache (Guava/Caffeine in Java, `node-cache` in Node, `LRU dict` in Python).
   - L1 has a tiny TTL (e.g. 1 to 3 seconds).
   - If an application cluster has 200 web instances, the 2,000,000 req/sec load on Redis is reduced by 99.9% to just 200 req/sec!
2. **Key Salting / Replication across Shards:**
   - Append a random suffix from $0$ to $N-1$ when writing the hot key:
     `hot_key_0`, `hot_key_1`, `hot_key_2`, $\dots$, `hot_key_9`.
   - Distribute the writes to all 10 keys.
   - Clients read by picking a random number: `f"hot_key_{random.randint(0, 9)}"`.
   - The read load is now evenly divided across 10 distinct Redis shards!

---

## Failure Modes Summary Matrix

| Failure Mode | Symptom | Primary Cause | Proven Industry Solution |
|---|---|---|---|
| **Cache Stampede** | Sudden DB connection spike for **one specific key** | Key expires under heavy concurrent load | **Distributed Mutex Lock** or **XFetch Probabilistic Early Refresh** |
| **Cache Penetration** | DB CPU pinned scanning empty indexes | Queries for non-existent IDs bypass cache | **Bloom Filters** or **Caching Null with short TTL** |
| **Cache Avalanche** | Global cache hit rate collapses to 0% | Synchronous bulk expiration of keys | **TTL Jitter (Randomization)** and **Pre-warming** |
| **Hot Key** | One Redis node crashes while cluster is idle | Traffic skew targeting single shard | **L1 Local In-Memory Cache** and **Key Salting** |

---

> [!NOTE]
> ### 🎓 Teacher FAQ & Common Beginner Mistakes
>
> **Q: "Why can't I just set the TTL to infinity and never expire keys?"**
> Setting TTL to infinity guarantees your cache will eventually serve corrupted or stale data when an application update bug skips an invalidation hook. Furthermore, without TTLs, old keys accumulate indefinitely until Redis runs out of memory and triggers its eviction policy, randomly kicking out active keys! A TTL is your system's automatic garbage collection guarantee.
>
> **Q: "When should I use Bloom Filters vs Caching Nulls?"**
> If your ID space is bounded (e.g. user IDs 1 to 10,000,000), caching `null` with a 30-second TTL is completely fine. But if you have an open endpoint vulnerable to random GUID or string attacks (e.g., searching for arbitrary usernames or scraping random URLs), attackers can flood your Redis instance with 50 GB of null keys, causing out-of-memory errors. In that scenario, Bloom Filters are mandatory.
