# Kafka Architecture: The Distributed Commit Log

Welcome to the definitive masterclass on Apache Kafka and distributed commit log architecture. In modern distributed systems, data is not static; it is a continuous, high-velocity stream of real-time events. Originally developed at LinkedIn in 2010 to ingest billions of daily tracking events and open-sourced in 2011, **Apache Kafka** is not a traditional message queue (like RabbitMQ or ActiveMQ)—it is an append-only, horizontally scalable, fault-tolerant **distributed streaming platform**.

To design enterprise event-driven architectures, real-time analytics pipelines, and change data capture (CDC) backbones, you must understand Kafka at the operating system and protocol level: How does an append-only disk log outperform in-memory caching? How does Linux kernel zero-copy work? How does Kafka guarantee exactly-once processing across transactional boundaries?

---

## Topics, partitions, offsets — horizontal scale by adding partitions

### 1. Logical Topics vs Physical Partitions
In a relational database, records are organized into tables. In Apache Kafka, event records are categorized into **Topics**.
However, a topic is strictly a logical abstraction. If an entire topic lived on a single physical machine, your cluster would be hard-limited by the disk I/O, network bandwidth, and storage capacity of that single machine.

To enable horizontal scalability, Kafka shatters a topic into multiple **Partitions**:
- A partition is an immutable, ordered sequence of records physically stored on a **Kafka Broker** (server node).
- Partitions of the same topic are distributed across different brokers in the cluster.
- **Partitions are the atomic unit of parallelism in Kafka.** A topic with 32 partitions can support 32 concurrent producer threads and 32 concurrent consumer workers operating simultaneously without lock contention!

```
Topic: "orders" (Total 3 Partitions across 3 Brokers)

Broker 1: [Partition 0] -> [Offset 0][Offset 1][Offset 2][Offset 3]... (Append-only)
Broker 2: [Partition 1] -> [Offset 0][Offset 1][Offset 2]...
Broker 3: [Partition 2] -> [Offset 0][Offset 1][Offset 2][Offset 3][Offset 4]...
```

### 2. The Mechanics of Offsets
Within a single partition, every record is assigned a monotonic, sequential 64-bit integer called an **Offset** (0, 1, 2, 3...).
- **Immutable and Append-Only:** Once an event is written to an offset, it can never be altered or inserted out of order.
- **Partition-Scoped Ordering:** **Order is strictly guaranteed ONLY within a single partition.** Kafka provides NO global ordering across different partitions within the same topic.

### 3. Partition Keys & The Hashing Contract
How does Kafka decide which partition receives an incoming message?
1. **Round-Robin (No Key):** If `key == null`, Kafka distributes messages across available partitions using sticky round-robin batching to maximize network buffer compression.
2. **Key-Based Hashing:** If a key is provided (e.g., `user_id`, `order_id`), Kafka computes a 32-bit hash (MurmurHash2) modulo the number of partitions:
   $$	ext{Partition} = 	ext{murmur2}(	ext{Key}) \pmod{	ext{NumPartitions}}$$

> [!TIP]
> **Partition Key Golden Rule:**
> If business logic requires strict chronological ordering for an entity (e.g., all banking transactions for `Account_9912`), you **must** use the entity ID as the partition key. Because the hash of `Account_9912` is constant, all events for that account land in the exact same partition in strict sequential order!
>
> *Warning on Partition Resizing:* If you increase the partition count of an existing topic ($N 	o N+k$), the modulo changes, and future events for `Account_9912` will hash to a different partition, breaking temporal ordering! Always over-partition upfront (e.g., 30 to 100 partitions).

### 4. High-Water Mark (HWM) vs Log End Offset (LEO)
Every partition replica tracks two critical watermark pointers:
- **Log End Offset (LEO):** The offset of the next record to be written to the local broker's log.
- **High-Water Mark (HWM):** The highest offset that has been successfully replicated across all **In-Sync Replicas (ISR)**.
Consumers are strictly forbidden from reading messages beyond the High-Water Mark to prevent reading uncommitted data that could be lost during leader failover.

---

## Consumer groups — each group sees all messages; within group, each partition → one consumer

### 1. Scaling the Readers Horizontally
In traditional messaging, you have either **Queuing** (competing consumers process messages from a shared queue) or **Publish-Subscribe** (every subscriber gets a copy of every message).
Kafka unites both models through the concept of the **Consumer Group**.

A Consumer Group is a set of consumer processes (often Kubernetes pods) that work together to consume a topic:
- **Across Groups (Pub/Sub):** Every consumer group receives a complete, independent copy of all messages in the topic. The `AnalyticsGroup` and the `BillingGroup` both read all records at their own independent speeds.
- **Within a Group (Queue / Load Balanced):** Each partition is assigned to **EXACTLY ONE consumer instance** within the group!

```
Topic "page-views" (4 Partitions: P0, P1, P2, P3)

[Consumer Group A: 2 Pods]
  - Pod 1: Assigned P0, P1
  - Pod 2: Assigned P2, P3
  (Balanced: 2 partitions per consumer)

[Consumer Group B: 4 Pods]
  - Pod 1: P0 | Pod 2: P1 | Pod 3: P2 | Pod 4: P3
  (Maximum Parallelism: 1 partition per consumer)

[Consumer Group C: 6 Pods]
  - Pod 1: P0 | Pod 2: P1 | Pod 3: P2 | Pod 4: P3
  - Pod 5: IDLE | Pod 6: IDLE
  (WASTED RESOURCES: 2 consumers sit completely idle!)
```

> [!WARNING]
> **The Golden Partition-Consumer Invariant:**
> You can never have more active consumers in a group than there are partitions in the topic!
> If your topic has 8 partitions and your processing service is struggling with consumer lag, scaling your Kubernetes deployment from 8 pods to 16 pods will do **absolutely nothing**—the 8 new pods will sit 100% idle. To increase consumer parallelism, you must first increase the partition count on the Kafka broker!

### 2. Consumer Offset Management
Unlike RabbitMQ, where the broker deletes messages as soon as consumers acknowledge them, Kafka brokers are passive.
- Each consumer group maintains its own read pointer: the **Committed Offset**.
- Committed offsets are stored internally in a special, highly compacted Kafka system topic called `__consumer_offsets`.
- Because consumers manage their own offsets, a consumer can **replay past data** (rewinding to offset 0) or skip ahead at will.

### 3. Rebalance Protocols: Eager vs Cooperative Sticky
When a consumer crashes or a new pod scales up, Kafka triggers a **Consumer Group Rebalance** to redistribute partitions:
- **Eager Rebalance (Legacy):** All consumers stop processing, surrender all their partitions (Stop-the-World pause), and re-join the group. Creates massive latency spikes.
- **Cooperative Sticky Rebalance (Modern Kafka):** Consumers continue processing partitions that do not need to move. Only the specific partitions migrating to the new pod are temporarily paused, reducing rebalance latency from tens of seconds to milliseconds.

---

## Sequential disk I/O + zero-copy — why Kafka is fast

A common interview mystery is: *"Databases store data in RAM to be fast. Kafka writes every single message to physical persistent disk. How does it achieve 10 million messages per second?"*

Kafka's blistering throughput relies on two fundamental operating system and hardware engineering principles: **Sequential Disk Access** and **Linux Kernel Zero-Copy**.

### 1. Sequential vs Random Disk Access Mechanics
Physical disks (hard drives and NVMe SSDs) are heavily optimized for sequential block streaming:
- **Random Disk I/O:** The disk head must physically seek sectors (HDD) or navigate memory flash pages (SSD), suffering write amplification and latency: $\sim 100 	ext{ to } 500 	ext{ IOPS}$, throughput $\sim 1 	ext{ to } 10 	ext{ MB/s}$.
- **Sequential Disk I/O:** Data is streamed continuously into adjacent disk blocks: throughput exceeds **$600 	ext{ MB/s}$ on HDDs and $> 3.5 	ext{ GB/s}$ on NVMe SSDs!**

Sequential disk access is so fast that it often outpaces random RAM memory access (which incurs CPU cache misses and pointer dereference penalties). Kafka's log is **strictly append-only**, converting all writes into raw sequential disk streams.

### 2. The Linux Page Cache Architecture
Kafka does not maintain a massive user-space in-memory cache inside the JVM (Java Virtual Machine). Storing gigabytes of messages in Java heap memory causes catastrophic Garbage Collection (GC) pauses and doubles memory footprint due to Java object overhead.

Instead, Kafka lets the **Linux Kernel Page Cache** do all the work:
- All disk reads and writes automatically pass through the OS page cache in unallocated physical RAM.
- If a producer writes an event and a real-time consumer reads it 5ms later, the message is served **directly from the OS RAM page cache** without ever touching the physical disk platters!

### 3. Linux Kernel Zero-Copy (`sendfile`)
In a traditional web application or message queue, transferring data from disk to a network socket requires **4 user-kernel context switches and 4 memory buffer copies**:

```
Traditional File Transfer (4 Copies, 4 Context Switches):
[Disk] --(1. DMA Copy)--> [Kernel Page Cache] --(2. CPU Copy)--> [JVM User Space]
                                                                        |
[Network Socket Buffer] <--(4. DMA Copy)-- [Kernel Socket Buffer] <--(3. CPU Copy)--+
```

Kafka bypasses the JVM entirely using the Linux `sendfile()` system call (backed by Java's `FileChannel.transferTo()`):

```
Linux Kernel Zero-Copy via sendfile() (2 Copies, 2 Context Switches):
[Disk] --(1. DMA Copy)--> [Kernel Page Cache] ---------------------------------------+
                                  |                                                  |
                     (Zero-Copy: Descriptors only)                                   |
                                  v                                                  v
                     [Socket Buffer Descriptors] --(2. Gather DMA Copy)--> [NIC Buffer]
```
Data travels directly from the OS page cache to the Network Interface Card (NIC) via Direct Memory Access (DMA). **The data never crosses into JVM user-space memory**, eliminating CPU copy cycles and GC overhead.

---

## Retention — keep messages N days regardless of consumption

### 1. The Distributed Commit Log vs The Discard Queue
In traditional queues (RabbitMQ, SQS):
- Message arrives &rarr; Worker consumes message &rarr; Worker acknowledges &rarr; Message is deleted from disk.
- If a worker has a bug, the data is gone forever. New services cannot inspect past events.

In Kafka:
- Messages are **never deleted upon consumption**.
- A message is retained for a configurable retention window, regardless of whether 0, 1, or 1,000 consumer groups have read it.

### 2. Physical Segment Architecture
Kafka does not store an entire partition in a single massive file. A partition directory on disk contains multiple **Log Segments** (typically 1 GB each):
- `00000000000000000000.log`: The raw binary message payload file.
- `00000000000000000000.index`: A **sparse index** mapping logical offsets to byte positions in the `.log` file (allowing binary search lookups without loading the entire file into memory).
- `00000000000000000000.timeindex`: A sparse index mapping millisecond timestamps to offsets (enabling time-based replay).

Only the current active segment is open for writes. Closed older segments are read-only.

### 3. Retention Policies: Time, Size, and Compaction
Kafka supports two retention cleanup modes:

1. **Delete Retention (`cleanup.policy=delete`):**
   - **Time-based:** `log.retention.hours=168` (retains data for 7 days; segments older than 7 days are unlinked and reclaimed by the OS).
   - **Size-based:** `log.retention.bytes=107374182400` (retains up to 100 GB per partition).
2. **Log Compaction (`cleanup.policy=compact`):**
   - Essential for **Event Sourcing** and **Change Data Capture (CDC)** (e.g., replicating database tables via Debezium).
   - Kafka retains the **latest value for every key indefinitely**!
   - Background cleaner threads scan closed segments and purge older records with duplicate keys, keeping only the most recent state.
   - Deleting a key is accomplished by producing a **Tombstone record** (`value = null`).

```
Partition Log Before Compaction:
[Key: A, Val: 1] [Key: B, Val: 2] [Key: A, Val: 3] [Key: C, Val: 1] [Key: B, Val: 5]

Partition Log After Compaction:
[Key: C, Val: 1] [Key: A, Val: 3] [Key: B, Val: 5]
(Old values for A and B are purged; state is preserved forever!)
```

---

## Exactly-once semantics (Kafka transactions, idempotent producers)

In distributed messaging, three delivery semantics exist:
1. **At-Most-Once:** `acks=0`. Fast, but network drops cause silent data loss.
2. **At-Least-Once:** `acks=all` + retries. Guarantees no data loss, but network retries create duplicate messages.
3. **Exactly-Once Semantics (EOS):** Each event is processed and reflected in the downstream system exactly once, even during broker crashes and network partitions.

Introduced in Kafka 0.11, Exactly-Once Semantics is achieved through the synergy of **Idempotent Producers** and **Transactional Coordination**.

### 1. Idempotent Producer Mechanics
A standard producer retrying after a network timeout risks producing duplicates:

```
[Producer] --- Message "Transfer $50" ---> [Broker] (Commits to disk!)
                                             |
                                   (Network ACK drops!)
                                             |
[Producer] (Timeout!) Retries "Transfer $50" -> [Broker] (DUPLICATE PRODUCED!)
```

**How Idempotent Producers (`enable.idempotence=true`) Fix It:**
1. The broker assigns each producer a unique 64-bit **Producer ID (PID)** during handshake.
2. The producer tags each message with a monotonically increasing **Sequence Number** per partition.
3. The broker caches the last 5 committed sequence numbers for each PID.
4. When the broker receives a duplicate message with a sequence number it has already committed, it **acknowledges the message to the producer but drops the duplicate from the log!**

### 2. Transactional Processing (Read-Process-Write)
In stream processing (Kafka Streams, Flink), a worker reads an event from Topic A, updates state, and publishes a derived event to Topic B, then commits its consumer offset.
If the worker crashes mid-flight, the event might be published to Topic B without the offset being committed, causing duplicate processing upon restart.

**The Kafka Transaction Protocol:**
1. The application registers a persistent `transactional.id`.
2. A centralized **Transaction Coordinator** broker manages transaction state in an internal log: `__transaction_state`.
3. The producer begins a transaction: `producer.beginTransaction()`.
4. Messages are written to Topic B, and consumer offsets are written to `__consumer_offsets` as part of the *same atomic transaction*.
5. The Transaction Coordinator writes a **PREPARE_COMMIT** marker to its transaction log, followed by **COMMIT markers** into the target topic partitions.
6. Downstream consumers configured with `isolation.level=read_committed` buffer messages and only release them to the user application when the COMMIT marker is read! If the transaction aborts, the uncommitted messages are silently discarded.

---

> [!TIP]
> **Summary Decision Rule for System Design Interviews:**
> - Choose **Kafka** over traditional queues (RabbitMQ/SQS) when you need **high-throughput event streaming (> 100k msg/sec)**, **replayable history**, **multi-consumer pub/sub**, or **strict partition ordering**.
> - Always configure **`acks=all` and `min.insync.replicas=2`** for zero data loss on financial and critical business data.
> - Size topic partitions based on target throughput: $	ext{Partitions} = \max(	ext{ProducerThroughput} / 10	ext{MB/s}, 	ext{ConsumerThroughput} / 5	ext{MB/s})$.
> - Deploy **Log Compaction** for entity state changelogs (CDC / Key-Value history); deploy **Delete Retention** for time-series activity streams.
