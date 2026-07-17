# Core Interview Designs

Welcome to the Core Interview Designs masterclass. If you are interviewing for a mid-to-senior backend role, these are the exact questions you will face. They test your ability to balance trade-offs, manage complex data flows, and handle massive concurrency.

---

## 1. Chat / WhatsApp / Slack — WebSockets, Message Ordering, Presence, Fan-out

Building a real-time chat application fundamentally changes how clients interact with servers. Standard HTTP (request/response) is inadequate because the server cannot easily "push" new messages to a client without the client constantly asking (polling).

### The Real-Time Connection
We use **WebSockets** for persistent, bidirectional communication.
1. The client opens an HTTP connection and sends an `Upgrade: websocket` header.
2. The server agrees, and the connection stays open indefinitely.
3. Both sides can now push data to each other with minimal overhead.

### Architecture & Data Flow
Imagine Alice wants to send a message to Bob.
1. Alice connects to **Chat Server A** via WebSocket.
2. Bob connects to **Chat Server B** via WebSocket.
3. Alice sends "Hi Bob". Chat Server A receives it.
4. Server A must know where Bob is. It queries a **Presence Server** or Redis cache: "Which server is Bob connected to?"
5. Redis replies: "Bob is on Server B."
6. Server A sends the message to Server B via an internal message bus (like Kafka or RabbitMQ).
7. Server B pushes the message down the open WebSocket connection to Bob.

### Group Chats (Fan-out)
If Alice sends a message to a group with 100 members, Server A finds out which chat servers the 100 members are connected to and fans out the message via the message broker.

> [!NOTE]
> **Teacher FAQ: How do we guarantee message ordering?**
> A common beginner mistake is relying on timestamps. Distributed server clocks drift (NTP isn't perfect). Instead, we use a central ID generator (like Snowflake) to generate monotonically increasing Message IDs, or we rely on a single sequencer per chat room/thread.

---

## 2. Twitter / X — Fan-out on Write vs Read; Hybrid for Celebrities

Twitter is fundamentally a pub/sub system. You publish a tweet, and all your followers must see it in their timelines.

### Approach A: Fan-out on Write (Push)
When an average user (say, Alice with 100 followers) tweets, the server immediately fetches her 100 followers. It then pushes the new tweet into the pre-computed Timeline Cache (Redis) of each of those 100 followers.
* **Pros:** Reading the timeline is insanely fast (`O(1)`).
* **Cons:** Doing this for Elon Musk (150M followers) would require 150 million cache updates. This would take minutes and crash the cache cluster.

### Approach B: Fan-out on Read (Pull)
When Alice tweets, the database simply stores the tweet: `{tweet_id: 123, author: alice}`.
When Bob opens Twitter, the server fetches Bob's 1000 followings, queries the DB for their recent tweets, merges them, sorts them by time, and serves the timeline.
* **Pros:** Tweeting is instant (`O(1)`).
* **Cons:** Opening the app is incredibly slow (`O(N)` queries and merging).

### The Master Solution: Hybrid Architecture
Twitter uses a hybrid approach.
1. For **normal users**, we use Fan-out on Write.
2. For **celebrities** (users with >100k followers), we use Fan-out on Read.
When Bob opens Twitter, his timeline is quickly pulled from his Redis cache (containing normal user tweets), and then dynamically merged with the latest tweets from the celebrities he follows. This perfectly balances the load!

---

## 3. YouTube / Netflix — Upload Pipeline, Transcoding, Adaptive Bitrate Streaming, CDN

Video streaming consumes the vast majority of internet bandwidth. It is a massive orchestration of storage, processing, and delivery.

### The Upload & Transcoding Pipeline
When a creator uploads a raw 4K `.mov` file:
1. It is saved to an S3 bucket (Block Storage).
2. A message is sent to a message queue (e.g., Kafka) triggering the **Transcoding Pipeline**.
3. Worker nodes pull the video and convert it into multiple resolutions (1080p, 720p, 480p, 144p) and multiple formats (HLS, DASH).
4. The transcoded chunks are saved back to S3.

### Adaptive Bitrate Streaming (ABR)
We don't send an entire 2GB video file to the user. We chop the video into 2-second segments. The video player downloads a **manifest file** listing all the available qualities for each segment.
If the user's Wi-Fi is fast, the player requests 1080p segments. If they drive into a tunnel and the connection drops, the player seamlessly requests the next 2-second segment in 144p to prevent buffering.

> [!TIP]
> **Performance Optimization:**
> Videos are always served via a **CDN**. Netflix actually places specialized hardware (Open Connect Appliances) directly inside Internet Service Providers (ISPs) like Comcast and AT&T. This means the video never even travels across the open internet!

---

## 4. Instagram / Photo Sharing — Media Upload, Feed Generation, S3+CDN

Instagram is similar to Twitter but significantly heavier due to media assets.

### Data Modeling
We need to store relations: User, Photo, Follows.
Because reads heavily outweigh writes, we denormalize data or use a NoSQL database (like Cassandra) to store User Feeds. However, metadata (User info, relationships) often remains in a highly replicated Relational DB (PostgreSQL).

### Media Storage
Photos are stored in Object Storage (AWS S3) and served via CDNs.
**Capacity Estimation:** If 100M users upload 1 photo/day (average 2MB), that's `100M * 2MB = 200TB / day`. Over a year, this is `73 Petabytes`. You cannot store this in a relational database.

---

## 5. Notification System — Multi-channel, Queues, Templates, Dedup

A centralized notification system abstracts away the complexity of sending Emails, SMS, and Push Notifications.

### The Flow
1. Microservices (e.g., PaymentService) send a generic payload to the NotificationService: `"Notify User 123 that their order shipped."`
2. The NotificationService queries the User DB to get their preferences and contact info (Email, Phone number, Device Push Tokens).
3. It pushes jobs onto specific message queues (Email Queue, SMS Queue, Push Queue).
4. Workers pick up jobs, apply localization (translating the message to Spanish if the user is in Spain), inject data into HTML templates, and call third-party APIs (SendGrid, Twilio, APNs).

### Deduplication
If the PaymentService crashes and retries, it might send the notification request twice. The NotificationService must use a Redis cache to track `notification_id` and prevent sending duplicate emails to the user.

---

## 6. Ticketmaster / Seat Booking — Inventory Locks, Distributed Txns

Booking systems are notorious for concurrency issues. Imagine 100,000 Taylor Swift fans trying to buy the same front-row seat at exactly the same millisecond.

### The Concurrency Problem
If 10 users select Seat A1, and we just check `if seat.status == 'AVAILABLE'`, all 10 read 'AVAILABLE', all 10 proceed to payment, and we double-book 9 people.

### Solution 1: Pessimistic Locking (Database Level)
When User 1 clicks Seat A1, the database runs `SELECT * FROM seats WHERE id = 'A1' FOR UPDATE`. This locks the row in MySQL. The other 9 users are blocked until User 1 finishes or timeouts.
* **Pros:** Perfectly safe.
* **Cons:** Terrible performance and deadlocks.

### Solution 2: Distributed Lock + Expiry (Redis) - Recommended
When User 1 clicks Seat A1, the server tries to acquire a lock in Redis: `SETNX seat:A1:lock user_1 EX 600` (Set if Not eXists, expire in 10 minutes).
* If successful, the UI gives the user 10 minutes to enter their credit card.
* If they pay, the seat is marked `SOLD` in the DB.
* If they don't pay in 10 minutes, the Redis lock expires automatically, and the seat becomes available for someone else.

---

## 7. Tinder / Matching — Geospatial Indexing, Swiping, Recommendations

Tinder's core challenge is quickly finding users within a specific geographic radius. A standard SQL query like `SELECT * FROM users WHERE lat BETWEEN x AND y` is devastatingly slow for millions of rows.

### Geospatial Indexing (Geohash / Quad-trees)
Instead of raw coordinates, we use a **Quad-tree** or **Geohash**.
A Geohash divides the world map into a grid and assigns a string to each grid square. E.g., New York is `dr5r`.
To find users within 5 miles, we just query the database for users whose Geohash starts with `dr5r`. This turns a complex math problem into a blazing-fast string prefix match! Redis has built-in geospatial commands (`GEOADD`, `GEORADIUS`) that handle this entirely in RAM.

---

## 8. TikTok / Short Video — ML-powered Feed, CDN, Video Encoding

TikTok combines the video pipeline of YouTube with the aggressive pre-computation of Twitter feeds, heavily driven by Machine Learning.

### The Endless Scroll (Pre-fetching)
Unlike a static timeline, TikTok's feed is a queue of videos. The client doesn't download 1 video at a time. It pre-fetches the next 5 videos in the background. When you swipe up, the video is already in RAM, providing zero-latency playback.

### ML Recommendation Engine
The backend tracks every micro-interaction: watch time, re-watches, likes, shares, and even scroll speed. This event stream goes into Kafka, is processed by Apache Flink (real-time stream processing), and updates user embeddings. The ML inference server uses these embeddings to constantly re-rank the user's upcoming video queue.

---

## 9. Airbnb / Booking — Double-booking, Calendar Availability

Airbnb is similar to Ticketmaster, but instead of single points in time (a seat for a concert), it deals with date ranges.

### The overlapping dates problem
How do you quickly check if a property is available from Aug 5 to Aug 10?
We cannot lock the entire property. We must store availability efficiently.
A common pattern is storing daily inventory. For a specific house, there are 365 rows per year in the DB (or a JSON array).
To book Aug 5-10, we start a database transaction and run:
`UPDATE availability SET status = 'BOOKED' WHERE property_id = 123 AND date BETWEEN '2023-08-05' AND '2023-08-10' AND status = 'AVAILABLE'`
If the number of affected rows != 6 (the number of days), someone else booked one of those days, and we rollback the transaction.

---

## 10. Payment System — Idempotency, Double-entry Bookkeeping, PCI-DSS

Moving money requires absolute, flawless consistency.

### Double-Entry Bookkeeping
Every transaction requires at least two ledger entries: a debit and a credit. If Alice pays Bob $10, we must deduct $10 from Alice and add $10 to Bob. These two operations must happen inside a strictly ACID-compliant relational database transaction (PostgreSQL or Spanner).

### Idempotency Keys
Network requests fail. If the client gets a network timeout, they will click "Pay" again. The API must require an `Idempotency-Key` (a unique UUID for that specific checkout cart). The backend checks the database: "Has this key already been processed?" If yes, it returns the previous success receipt without charging the card again.

> [!WARNING]
> **PCI-DSS Compliance:**
> Do not store raw credit card numbers unless absolutely necessary and you are willing to undergo massive security audits. Always use a payment gateway (Stripe/Braintree) tokenization system. The frontend sends the card to Stripe, gets a secure Token back, and sends that Token to your backend.

---

## 11. Distributed Message Queue (Kafka) — Ordering, Partitions, Consumer Groups

Kafka is an append-only distributed log, not a traditional queue.

### Partitions and Ordering
A Kafka "Topic" (e.g., `user_clicks`) is split into multiple "Partitions" (e.g., 10 partitions).
Messages within a single partition are strictly ordered. Messages across different partitions have no guaranteed order.
If you need strict ordering for a specific user (e.g., User A logged in, then logged out), you use the `user_id` as the routing key. All messages for User A will hash to the *same* partition, guaranteeing they are processed in order.

### Consumer Groups
Unlike RabbitMQ which deletes a message once consumed, Kafka keeps messages on disk for days. A Consumer Group allows multiple workers to share the load of reading a topic (each worker gets a few partitions). Multiple *different* Consumer Groups can read the exact same data without interfering with each other.

---

## 12. Reddit / HN — Voting, Ranking, Comment Threads

Social news aggregators face the challenge of constantly shifting rankings based on upvotes and time decay.

### The Ranking Algorithm (Hotness)
You cannot sort purely by upvotes, or a 10-year-old post will stay at the top forever. You must use an algorithm like Hacker News: `Score = (Upvotes - 1) / (Age_in_hours + 2)^Gravity`.
Because scores change every second as posts age, we cannot run this math in a SQL `ORDER BY` clause for every request.
Instead, a background cron job constantly recalculates the scores for recent posts and updates a **Redis Sorted Set** (`ZSET`). Reading the front page is simply `ZREVRANGE front_page 0 25`.

### Comment Trees
Storing threaded comments (replies to replies to replies) is tricky in SQL.
* **Path Enumeration (Materialized Path):** Store the full path in the row (e.g., `1/4/9`). To find all replies to comment 4, query `WHERE path LIKE '1/4/%'`. This is fast and scalable.

---

## 13. Autocomplete / Typeahead — Trie, Top-K, Prefix Cache

When you type "sys" in Google, it instantly suggests "system design". This must happen in < 50ms.

### The Trie Data Structure
We use a Trie (Prefix Tree) stored in RAM. The root is empty. Nodes represent characters (`s` -> `y` -> `s`).
At each node, we store a cached list of the **Top-K** most popular search terms that start with that prefix.
When the user types "sys", we traverse to the 's' node in `O(1)` time, and instantly return the pre-computed Top-K list.

### Updating the Trie
Rebuilding the Trie for billions of searches is computationally heavy. We process search analytics asynchronously (using Hadoop or Spark) once an hour, and then atomically hot-swap the old Trie in memory with the new Trie. We never update the active read-serving Trie on the fly.
