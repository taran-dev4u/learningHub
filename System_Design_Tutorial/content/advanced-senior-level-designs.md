# Advanced Senior-Level Designs

Welcome to the Advanced Senior-Level Designs masterclass. If you are aiming for Staff/Principal levels at top tech companies, you must demonstrate mastery over deeply complex algorithms, consistency models, and hyper-scale infrastructure. These designs go beyond basic CRUD apps and require nuanced architectural decisions.

---

## 1. Uber / Rideshare — Geospatial Indexing, Matching, Real-time Location

Designing Uber is one of the most mechanically complex system design questions because it involves high-frequency real-time writes (location updates) and complex spatial queries (finding drivers near a rider).

### The Real-Time Location Problem
Drivers send their GPS coordinates to the server every 4 seconds. If you have 1 million active drivers, that's 250,000 writes per second.
You cannot write this to a standard SQL database. The disks will melt.
Instead, we use an **in-memory data grid** (like Redis) or a highly optimized NoSQL column store (like Cassandra) just to ingest this firehose of location data.

### Geospatial Indexing: Quad-Trees
How do we find 5 drivers within a 2-mile radius of a rider? Scanning all drivers is `O(N)`. We need `O(log N)` or better.
Uber uses **Quad-Trees** (specifically heavily modified versions, or Google's S2 library).
Imagine a square map of the city. We divide it into 4 smaller squares. If a square has more than 500 drivers, we divide that square into 4 even smaller squares. We keep doing this until every square has fewer than 500 drivers.
This creates a tree structure in memory. When a rider requests a car, we find the rider's current small square, get the drivers in it, and if we need more, we look at the neighboring squares.

### Dispatch & Matching
The Dispatch Service pulls the nearest drivers from the Quad-Tree, ranks them based on ETA (not just straight-line distance, but actual traffic conditions), and sends a push notification to the highest-ranked driver. If they decline, it goes to the next.

> [!NOTE]
> **Teacher FAQ: How do we keep the Quad-Tree updated if drivers move every 4 seconds?**
> Updating a global Quad-Tree 250,000 times a second causes massive locking contention.
> Instead, we shard the Quad-Tree by City. Furthermore, we don't update the tree on *every* GPS ping. We only update the driver's position in the tree if they cross a boundary from one grid square to another. Most 4-second pings stay within the same square, so we only update a simple hash map, significantly reducing tree-rebalancing load.

---

## 2. Google Search — Crawling, Indexing, PageRank, Serving

Designing a search engine requires understanding massive distributed data processing pipelines.

### 1. The Crawler
A fleet of worker nodes downloads HTML pages. They extract URLs from the page, put those URLs in a distributed queue, and download them.
To prevent DDoS-ing a website, we must strictly respect the `robots.txt` file and implement rate limiting per domain. We also compute a hash (MD5) of the page content to detect and discard exact duplicates.

### 2. The Indexer (Inverted Index)
How do we search billions of pages instantly? We build an **Inverted Index**.
Think of the index at the back of a textbook. Instead of mapping Document -> Words, we map Word -> Documents.
`"system": [Doc 1, Doc 42, Doc 99]`
`"design": [Doc 1, Doc 7, Doc 99]`
If a user searches for "system design", we fetch the lists for both words and perform an intersection `[Doc 1, Doc 99]`.
This index is massive. It is sharded across thousands of machines based on the Word ID (Term-partitioning) or Document ID (Doc-partitioning). Doc-partitioning is preferred for parallel query execution.

### 3. PageRank & Ranking
Finding matching documents is easy. Ranking them is hard.
**PageRank** calculates the "importance" of a page based on how many *other* important pages link to it. If Wikipedia links to your blog, your PageRank shoots up. This is calculated offline using massive MapReduce jobs (or Spark graph processing) iterating over the entire web graph.
At query time, the serving engine combines the pre-calculated PageRank with real-time text relevance (TF-IDF, position of words) and ML models to generate the final Top 10 list.

---

## 3. Google Drive / Dropbox — Chunked Upload, Dedup, Sync, Conflict Resolution

File storage systems must be extremely bandwidth-efficient and resilient to network drops.

### Chunked Uploads
You never upload a 5GB file in one single HTTP request. If the network drops at 4.9GB, you have to start over.
Instead, the client chunks the file into 4MB blocks. Each block is uploaded independently (often in parallel) with its own hash. If a chunk fails, only that 4MB is retried.

### Deduplication (Hashing)
Before uploading a chunk, the client hashes it (SHA-256) and asks the server: "Do you already have a chunk with this hash?"
If you upload a popular movie that someone else already uploaded, the server says "Yes!" and the client skips the upload entirely. The server just adds a metadata pointer. This saves millions of dollars in storage and bandwidth.

### Conflict Resolution
Alice and Bob edit `document.txt` offline at the same time, then reconnect. Which version wins?
We cannot just use "Last Write Wins" because Alice's work would be destroyed.
The server detects the conflict (because both clients try to upload a new version based on the same old version hash) and creates a second file: `document (Alice's conflicted copy).txt`. The users must resolve it manually.

---

## 4. Google Maps — Tile Generation, Routing (Dijkstra at Scale), Real-time Traffic

### Tile Generation
Google Maps does not render vectors on your phone for every pixel. It serves pre-rendered image "Tiles" (usually 256x256 pixels).
At zoom level 0 (the whole earth), there is 1 tile. At zoom level 1, there are 4 tiles. At zoom level 20 (street level), there are trillions. These tiles are generated offline, stored in massive CDN layers, and your phone simply downloads the 10-20 tiles needed for your current screen.

### Routing at Scale
Finding the shortest path is a classic Dijkstra's or A* algorithm problem. But running Dijkstra's across a graph with billions of nodes (every intersection on Earth) takes minutes, not milliseconds.
**Solution: Hierarchical Routing (Contraction Hierarchies).**
The map is pre-processed offline. We calculate the fastest routes between major highways. When you ask for a route from your house to a house 500 miles away, the algorithm only uses local roads to get you to the nearest highway, jumps to the pre-computed highway graph, and then uses local roads at the destination. This reduces the search space exponentially.

---

## 5. Google Docs — OT vs CRDTs, Conflict Resolution

Real-time collaborative editing is one of the hardest problems in computer science. If Alice types 'A' at index 0, and Bob types 'B' at index 0 at the same time, how do we ensure both screens eventually look exactly the same (`AB` or `BA`) without corrupting the document?

### Operational Transformation (OT)
This is what Google Docs uses.
Every keystroke is an "Operation" (e.g., `Insert 'A' at index 0`). The server acts as the single source of truth. It receives operations from clients, transforms the indices based on operations that happened simultaneously, and broadcasts the transformed operations back to the clients. OT requires a centralized server and incredibly complex mathematical proofs to ensure convergence.

### CRDTs (Conflict-free Replicated Data Types)
A modern alternative (used by Figma and local-first apps).
Instead of relying on a central server to transform indices, CRDTs assign a mathematically unique, globally ordered ID to *every single character*. Since characters don't rely on integer indices (like `index 5`), operations can be applied in any order, on any device, and the document will perfectly converge.

| Feature | OT | CRDT |
| :--- | :--- | :--- |
| **Server Requirement** | Requires a central authoritative server. | Can work peer-to-peer (P2P). |
| **Complexity** | Algorithm is terrifyingly complex to write. | Algorithm is simpler, but data structures are heavy. |
| **Memory Overhead** | Low overhead per character. | High memory overhead (each char has a huge metadata ID). |

---

## 6. Stock Exchange — Ultra-low Latency, Order Matching Engine

A stock exchange like NASDAQ processes millions of trades per second. The primary constraint is not just throughput, but **microsecond latency** and absolute determinism (FIFO fairness).

### The Architecture
You cannot use standard microservices over HTTP. The overhead of JSON parsing and network hops is too slow.
* **Network:** Multicast UDP over specialized fiber optic cables.
* **Data Structures:** The core "Order Book" is kept entirely in RAM using highly optimized Arrays and linked lists (no SQL databases in the critical path).
* **Language:** C or C++, heavily optimized to avoid garbage collection pauses and CPU cache misses.

### The Matching Engine
The matching engine maintains a queue of Bids (buy orders) and Asks (sell orders) for a stock. When a new order arrives, it must be matched against the opposite side in strict FIFO (First In, First Out) order.
To achieve redundancy, all incoming orders are written to a high-speed sequencer log (often replicated via hardware-level mirroring). If the primary matching engine crashes, a hot-standby instantly takes over from the exact same point in the log.

---

## 7. Facebook News Feed — Social Graph, Ranking, Fan-out at 3B Users

Unlike Twitter, Facebook connections are bidirectional (Friends) and significantly more complex (Pages, Groups, Events).

### The Social Graph
Storing the relationship graph ("Who is friends with who") is done using specialized Graph Databases (like TAO - The Associative Object store). TAO provides a highly optimized read-through cache for edges (connections) and nodes (users/posts).

### Feed Generation Pipeline
Because feeds are highly personalized and ML-driven, Fan-out on Write is impossible.
When you open Facebook:
1. The server queries TAO for all your friends and pages.
2. It fetches the 50 most recent posts from each of them.
3. This creates an initial pool of, say, 1000 candidate posts.
4. These posts are passed to a **Ranking Service**.
5. The ML model scores each post based on thousands of signals (affinity score, edge weight, time decay).
6. The top 20 are returned to your phone.

---

## 8. Distributed Locking Service (Chubby / Zookeeper) — Consensus, Lease Renewal

How do you guarantee that only *one* server in a 10,000-server cluster becomes the "Master" database? You need a distributed lock.

### The Problem with Redis Locks
For critical infrastructure (like electing a database master), Redis is not safe enough. If the Redis master crashes before replicating the lock to a replica, two servers might think they hold the lock simultaneously (Split-Brain).

### Consensus Protocols (Paxos / Raft)
We use a CP (Consistent and Partition-tolerant) system like ZooKeeper, etcd, or Google's Chubby.
These systems use Raft or Paxos to ensure that a lock is only granted if a strict majority (quorum) of the lock servers agree. If 3 out of 5 servers agree you have the lock, you have it, even if 2 servers crash.

### Leases and Heartbeats
If Server A gets the lock and then physically catches fire, the lock would be held forever.
Therefore, locks are granted as "Leases" (e.g., for 10 seconds). Server A must send a heartbeat every 5 seconds to renew the lease. If it crashes, the lease expires, and the cluster safely grants the lock to Server B.

> [!TIP]
> **Fencing Tokens:**
> What if Server A pauses for 12 seconds (Garbage Collection), its lease expires, Server B gets the lock, and then Server A wakes up and thinks it still has the lock?
> To prevent this, the lock service issues an incrementing **Fencing Token** with every lock. (Server A gets Token 1, Server B gets Token 2). The storage system must reject any write from a client whose Token is lower than the highest Token it has seen. When Server A finally writes with Token 1, the DB rejects it because it already saw Token 2 from Server B. Brilliant!
