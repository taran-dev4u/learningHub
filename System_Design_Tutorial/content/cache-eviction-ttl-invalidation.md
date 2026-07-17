# Cache Eviction, TTL & Invalidation

When building a high-performance system, it is crucial to understand that **cache is not a database**. Memory (RAM) is orders of magnitude more expensive than disk storage. You cannot fit everything into the cache. Eventually, your cache will reach its capacity limit, and you will have to kick something out to make room for new data. This process is called **Cache Eviction**.

At the same time, data in the cache can become stale if the underlying database changes. Deciding when to naturally expire data is handled via **TTL (Time-To-Live)**.

Let's master the strategies you need to manage the lifecycle of cached data.

---

## 1. LRU (Least Recently Used)
### The "If You Haven't Used It Lately, Lose It" Strategy

**LRU** is the most widely used cache eviction policy globally. It is the default policy for Redis in many setups. The premise is simple: the item that hasn't been accessed for the longest time is the first one evicted when the cache is full.

**How it works:**
Every time an item is read or written, it is moved to the "front" of the queue. The items at the "back" of the queue are the ones that haven't been touched in a long time. When space is needed, the tail is truncated.

**Real-World Analogy:**
Think of a pile of papers on your desk. When you read a document, you put it on top of the pile. The documents at the very bottom of the pile are the ones you haven't looked at in weeks. When you need to clear space, you throw away the bottom papers first.

**Why use it?**
LRU perfectly exploits **temporal locality**—the principle that if data was recently accessed, it is highly likely to be accessed again soon. For a news website, yesterday's articles will naturally age out as people read today's articles.

---

## 2. LFU (Least Frequently Used)
### The "Popularity Contest"

While LRU cares about *when* a key was accessed, **LFU** cares about *how many times* a key was accessed.

**How it works:**
The cache tracks an access counter for each item. When the cache is full, the item with the lowest counter is evicted, regardless of whether it was accessed 5 seconds ago or 5 days ago.

**Real-World Analogy:**
Imagine a grocery store shelf. You have space for only a few types of soda. Even if someone just bought a weird pickle-flavored soda 5 minutes ago, if it has only sold 2 cans this month, you pull it off the shelf to make room for Coke, which sells 500 cans a month.

**Why use it?**
LFU is superior when you have a set of data that is **consistently hot**, regardless of occasional spikes in other data.

> [!WARNING]
> The downside of LFU is that data that was historically extremely popular but is no longer relevant can stay in the cache forever (e.g., an article that got 1M views last week but 0 views today). Modern implementations (like Redis LFU) often use logarithmic counters that decay over time to solve this.

---

## 3. TTL-Based Expiry
### The "Self-Destruct Timer"

Instead of waiting for the cache to fill up before evicting items, you attach a **TTL (Time-To-Live)** to a cache key. Once the TTL expires, the key is automatically deleted.

**How it works:**
When you set `user:session:123` in Redis, you apply a TTL of 3600 seconds (1 hour). Exactly one hour later, the key vanishes.

**Real-World Analogy:**
A parking meter. You pay for 2 hours. After 2 hours, your time expires, and you are no longer allowed to occupy the spot.

**Why use it?**
TTL is non-negotiable for data that naturally expires or when you need a lazy way to ensure data doesn't drift too far from the database.
- **Session Tokens:** Security tokens should strictly expire after a set time.
- **Stock Prices:** Caching a stock price for 10 seconds prevents DB overload while ensuring no one sees data older than 10 seconds.

---

## 4. FIFO (First In, First Out)
### The "Conveyor Belt"

**FIFO** evicts the item that was added to the cache earliest, regardless of how often or how recently it has been accessed.

**How it works:**
It behaves like a strict queue. The first item to enter the cache is the first one pushed out when capacity is reached.

**Real-World Analogy:**
A grocery store rotating milk cartons. The oldest milk (first in) is always put at the front of the fridge to be sold first (first out).

**Why use it?**
FIFO is rarely used for standard object caching, but it is excellent for streaming logs or time-series buffers where you strictly care about retaining only the *newest* data.

---

## Comparison Summary

| Strategy | Metric Triggers Eviction | Best Use Case | Weakness |
| :--- | :--- | :--- | :--- |
| **LRU** | Longest time since last access | News articles, general purpose | Full cache scans can evict hot keys |
| **LFU** | Fewest total accesses | Leaderboards, persistent viral data | Historic data can get "stuck" in cache |
| **TTL** | Time elapsed since creation | Sessions, constantly updating prices | Requires tuning; expiring too soon hurts DB |
| **FIFO** | Time since entry into cache | Event logs, ordered buffers | Might evict a highly popular item just because it's old |

---

> [!NOTE]
> ### 🎓 Teacher FAQ & Common Beginner Mistakes
>
> **Q: "If I use TTL, do I still need an eviction policy like LRU?"**
> Yes! This is a classic interview trap. TTL only works if time expires. What if you have a 10GB Redis instance, all keys have a 24-hour TTL, but you try to write 12GB of data in the first 2 hours? The memory will fill up before any TTLs expire. You must configure Redis with an eviction policy (like `volatile-lru` or `allkeys-lru`) to handle out-of-memory events gracefully.
>
> **Q: "How exactly does Cache Invalidation work in practice?"**
> "Cache invalidation is one of the two hard things in Computer Science." The most robust way to invalidate a cache is **deletion**. When a user updates their profile in the database, do not try to manually update the Redis cache key with the new JSON. Instead, simply `DEL user:123`. The next read request will experience a cache miss, fetch the fresh data from the database, and write it securely to the cache. This eliminates nasty race conditions.
