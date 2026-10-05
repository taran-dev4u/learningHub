# CAP & PACELC Theorems

## Overview

When engineering distributed systems across networked machines, you are constrained by immutable physical laws. You cannot construct a globally distributed data store that guarantees instantaneous synchronization, perpetual uptime, and complete invulnerability to network disruptions.

The **CAP Theorem** (formulated by Eric Brewer and formally proven by Seth Gilbert and Nancy Lynch) and the **PACELC Theorem** (formulated by Daniel Abadi) represent the governing physics of distributed computing. In senior and staff system design interviews, superficial answers like *"You just pick two out of three"* are instant rejection signals. Interviewers expect you to articulate exact mathematical trade-offs, distinguish ACID consistency from CAP linearizability, analyze quorum mathematics ($R + W > N$), and explain how production architectures transition between normal operating conditions and network failure states.

---

## CAP Theorem — Consistency + Availability + Partition Tolerance

In 2000, Eric Brewer proposed the CAP principle, which was formally proven in 2002 as a fundamental impossibility theorem for asynchronous network models. The theorem asserts that any distributed data store can guarantee at most **two out of three** core properties simultaneously:

```
                          Consistency (C)
                         [Linearizability]
                               /\
                              /  \
                             /    \
                 CP Systems /      \ CA Systems
                (ZooKeeper)/        \ (Single-node RDBMS;
                (etcd)    /          \  Physically impossible
                         /   Network  \  over real networks)
                        /   Partition  \
                       /   (Reality)    \
                      /──────────────────\
        Availability (A)                  Partition Tolerance (P)
        (Every non-failing               (Network drops/delays
         node responds)                   messages between nodes)
                    \                    /
                     \                  /
                      \  AP Systems    /
                       \ (Cassandra)  /
                        \ (DynamoDB) /
```

### 1. Rigorous Definition of the Three Properties

#### Consistency (C) = Linearizability
In the context of the CAP theorem, **Consistency does NOT mean ACID consistency**. 
- In ACID, "C" denotes *Application Invariant Integrity* (e.g., account balance cannot drop below zero, foreign keys must exist).
- In CAP, "C" strictly denotes **Linearizability (Single-Copy Serializability)**: Every read operation must return the value of the most recent committed write, or throw an explicit error. To an external client, the cluster behaves exactly as if it were a single instantaneous machine running in memory.

#### Availability (A) = Every Non-Failing Node Responds
In CAP, **Availability does NOT simply mean "high uptime" (like 99.999% SLAs)**.
Availability formally requires that **every non-failing node in the distributed cluster must return a non-error response to every received request**, without infinite timeouts, even if that node has been completely severed from the rest of the cluster. If a node returns an HTTP `500 Internal Server Error`, a timeout, or refuses to accept writes because it cannot contact the leader, the system has formally sacrificed CAP Availability.

#### Partition Tolerance (P) = Resilience to Dropped / Delayed Packets
A **Network Partition** occurs when communication between two or more subnetworks is interrupted due to severed cables, hardware switch crashes, firewalls, or excessive packet latency. Partition Tolerance means the system continues to function correctly despite arbitrary message drops, delays, or reordering across physical network links.

---

## Partition Tolerance is non-negotiable on real networks

A ubiquitous junior developer misconception is: *"I will build a CA (Consistent and Available) distributed system."*

> [!WARNING]
> **The Fallacy of CA in Distributed Systems:**  
> **There is no such thing as a "CA distributed system".** Network hardware, transatlantic cables, top-of-rack switches, and virtualization layers *will* fail. Packet loss, transient routing flaps, and network partitions are inevitable physical realities. Therefore, **Partition Tolerance (P) is mandatory**. You cannot choose "CA"; you can only choose how your system behaves **in the presence of P**:
> - Choose **Consistency over Availability (CP)**: Refuse or fail requests to prevent divergent state.
> - Choose **Availability over Consistency (AP)**: Accept writes on all partitions and reconcile conflicts asynchronously.

### The Two-Node Formal Proof (Gilbert & Lynch)
Consider the simplest distributed database consisting of two nodes: $\text{Node}_A$ and $\text{Node}_B$.
1. A network partition occurs: the physical network link between $\text{Node}_A$ and $\text{Node}_B$ is severed.
2. A client connects to $\text{Node}_A$ and executes a write: `v = 10`.
3. Because the network is partitioned, $\text{Node}_A$ cannot transmit the write to $\text{Node}_B$.
4. Concurrently, another client connects to $\text{Node}_B$ and executes a read: `get(v)`.

```
 Client 1                       Client 2
    │                              │
    ▼ Write: v = 10                ▼ Read: v = ?
┌───────────┐      X X X X       ┌───────────┐
│  Node A   │ ◄── [Partition] ──►│  Node B   │
│ (v = 10)  │      X X X X       │  (v = 0)  │
└───────────┘                    └───────────┘
```

Now, $\text{Node}_B$ faces an existential architectural dilemma:
- **If $\text{Node}_B$ responds with its current value (`v = 0`):** $\text{Node}_B$ preserves **Availability** (it answered the client), but violates **Linearizable Consistency** because Client 2 read stale data.
- **If $\text{Node}_B$ refuses the request or waits indefinitely:** $\text{Node}_B$ preserves **Consistency**, but violates **Availability** by failing the client's request.

There is no algorithmic compromise that can overcome this spatial partition.

---

## CP systems: refuse writes during partitions (ZooKeeper, HBase, MongoDB strict)

When data correctness is paramount—such as in financial ledger accounting, distributed consensus, distributed locking, and inventory balance management—the system must enforce linearizability at the expense of availability.

### 1. Quorum Mechanics & Majority Consensus
CP architectures (such as Apache ZooKeeper, `etcd`, Google Spanner, and MongoDB with `w: "majority"`) utilize distributed consensus protocols (Raft, Paxos, ZAB).

A cluster of $N$ nodes requires a strict **Majority Quorum** ($Q$) to commit any state mutation:
$$Q = \left\lfloor \frac{N}{2} \right\rfloor + 1$$

| Cluster Size ($N$) | Majority Quorum ($Q$) | Max Node Failures Tolerated ($F$) |
| :--- | :--- | :--- |
| **3 nodes** | 2 nodes | 1 node |
| **5 nodes** | 3 nodes | 2 nodes |
| **7 nodes** | 4 nodes | 3 nodes |

### 2. Behavior During Network Partitions
Suppose a 5-node cluster is split into two isolated network partitions:
- **Partition 1 (Majority):** Nodes 1, 2, and 3 ($3 \text{ nodes} \ge 3$).
- **Partition 2 (Minority):** Nodes 4 and 5 ($2 \text{ nodes} < 3$).

```
        Partition 1 (Majority: 3 nodes)         Partition 2 (Minority: 2 nodes)
     ┌───────────┐ ┌───────────┐ ┌───────────┐       ┌───────────┐ ┌───────────┐
     │  Node 1   │ │  Node 2   │ │  Node 3   │ X X X │  Node 4   │ │  Node 5   │
     │  (Leader) │ │(Follower) │ │(Follower) │ X X X │(Follower) │ │(Follower) │
     └───────────┘ └───────────┘ └───────────┘       └───────────┘ └───────────┘
           ▲                                               ▲
           │                                               │
     Client Writes                                   Client Writes
     [STATUS: 200 OK]                                [STATUS: FAILED / BLOCKED]
```

- **Partition 1** retains the majority quorum ($3/5$). It continues to elect a valid leader and process linearizable reads and writes.
- **Partition 2** cannot form a majority ($2/5$). It cannot elect a leader or commit transactions. To prevent a **Split-Brain catastrophe** (where two separate leaders accept conflicting writes for the same key), Partition 2 **refuses all incoming client writes** and rejects stale reads.

### 3. Primary CP Implementations
- **ZooKeeper & etcd:** Provide linearizable key-value primitives for leader election, dynamic configuration, and distributed locks.
- **HBase:** Relies on ZooKeeper and HDFS NameNodes; if regions cannot achieve consensus, writes halt.
- **CockroachDB:** Uses Raft per range; ranges severed from a quorum reject write operations.

---

## AP systems: always accept, reconcile later (Cassandra, DynamoDB, CouchDB)

In high-scale consumer applications—such as social media timeline feeds, user presence, e-commerce shopping carts, telemetry logging, and messaging notifications—downtime is commercially unacceptable. If a user cannot add an item to their shopping cart because a transatlantic cable was severed, the retailer loses immediate revenue.

AP systems prioritize **uninterrupted availability**. Every operational node will accept client writes and reads regardless of network partitions, deferring conflict resolution to asynchronous background synchronization.

### 1. Conflict Resolution Strategies in AP Stores

When isolated partitions accept divergent writes to the same record, how is ground truth restored once the network heals?

#### Strategy A: Last-Write-Wins (LWW)
Every write carries a client or coordinator timestamp. When reconciling divergent replicas, the write with the highest physical timestamp overwrites all others.
- **Vulnerability:** Physical quartz clocks on commodity servers suffer from **clock skew** and **clock drift** (even with NTP synchronization). A node whose clock is 50 milliseconds fast will systematically overwrite legitimate newer writes from properly synchronized nodes, causing silent data loss.

#### Strategy B: Vector Clocks & Version Vectors
Instead of relying on fragile physical clocks, each node maintains a logical counter vector:
$$\text{Vector Clock} = \{ \text{Node}_A: c_A, \text{Node}_B: c_B, \dots \}$$
- If Vector Clock $V_1$ dominates Vector Clock $V_2$ across all entries, $V_1$ is causally newer.
- If neither dominates (e.g., $V_1 = \{A: 2, B: 1\}$ and $V_2 = \{A: 1, B: 2\}$), a **concurrent conflict** is detected. The database surfaces both versions (called "siblings" in Dynamo/Riak) to the client application to resolve via domain business logic (e.g., taking the union of items in a shopping cart).

#### Strategy C: CRDTs (Conflict-free Replicated Data Types)
CRDTs are mathematically proven data structures whose merge operations are **Associative**, **Commutative**, and **Idempotent** ($A \cup B = B \cup A$, and $A \cup A = A$).
- **PN-Counter (Positive-Negative Counter):** Enables distributed increment and decrement operations (e.g., YouTube video view counts) that converge to identical sums regardless of message delivery order.
- **LWW-Element-Set / OR-Set (Observed-Remove Set):** Enables distributed additions and removals from collections without lock coordination.

### 2. Configurable Tunable Consistency in Cassandra & DynamoDB
AP databases do not force pure eventual consistency; they offer **Tunable Consistency** per query via three variables:
- $N$: Replication factor (total replicas storing the data).
- $W$: Write consistency level (number of replicas that must acknowledge a write before success).
- $R$: Read consistency level (number of replicas that must respond to a read before returning).

$$\text{Strong Linearizable Consistency Condition: } R + W > N$$

```
Case 1: R + W > N (Strong Consistency)
Replicas N = 3, Write W = 2, Read R = 2
W (2) + R (2) = 4 > 3
┌───────────────┬───────────────┬───────────────┐
│   Replica 1   │   Replica 2   │   Replica 3   │
│  [Written ✓]  │  [Written ✓]  │               │
└───────────────┴───────────────┴───────────────┘
◄───────── Quorum Read (R=2) ──►
Overlap guaranteed! At least one read replica holds the latest write.
```

If $R + W \le N$ (e.g., $N=3, W=1, R=1$), the system operates in high-performance **Weak/Eventual Consistency** mode.

---

## PACELC: Latency vs Consistency even without partitions

The CAP theorem suffers from a severe practical limitation: **it only describes system trade-offs during a network partition**. In production enterprise cloud environments (AWS, GCP, Azure), networks function correctly **99.9% to 99.99% of the time**. 

What architectural trade-offs govern the database during the 99.9% of normal operations?

In 2010, Professor Daniel Abadi formulated the **PACELC Theorem** to close this critical theoretical gap:

```
                                    PACELC
                                      │
                   ┌──────────────────┴──────────────────┐
                   ▼                                     ▼
        If there is a Partition (P)                 Else (E)
        How do you trade off:                       How do you trade off:
        ┌─────────────┬─────────────┐               ┌─────────────┬─────────────┐
        ▼             ▼             ▼               ▼             ▼             ▼
   Availability  Consistency     Latency       Consistency     Latency
       (A)           (C)           (L)             (C)           (L)
```

$$\text{If } \mathbf{P} \text{ (Partition): Choose } \mathbf{A} \text{ or } \mathbf{C}; \quad \mathbf{E} \text{lse (Normal): Choose } \mathbf{L} \text{ or } \mathbf{C}.$$

### The Latency vs Consistency Trade-off Under Normal Conditions
Even when all fiber cables, routers, and switches are operating flawlessly:
- If an application demands **Strong Consistency ($C$)**, the database coordinator cannot return `200 OK` to the client until writes have traveled over physical fiber and been flushed to disk on multiple remote replica nodes. Physical light propagation through fiber takes time (~5 ms per 1,000 km). Thus, **Consistency penalizes Latency**.
- If an application demands **Sub-Millisecond Latency ($L$)**, the database must acknowledge writes immediately in local RAM on a single node and replicate to other nodes asynchronously in the background. Thus, **Latency penalizes Consistency** (replicas are momentarily stale).

### The Complete PACELC Classification Matrix

| Database | PACELC Type | Partition Behavior (P/A or P/C) | Normal Behavior (E/L or E/C) | Architectural Design Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **Apache Cassandra** | **PA/EL** | **Available** (accepts divergent writes) | **Low Latency** (async replication by default) | Built for massive write ingest and zero single points of failure. |
| **Amazon DynamoDB** | **PA/EL** | **Available** (eventual consistency default) | **Low Latency** (sub-10ms single-digit reads) | Can be tuned to PC/EC via strongly consistent read queries. |
| **Google Spanner** | **PC/EC** | **Consistent** (refuses split quorums) | **Consistent** (waits for atomic GPS/Atomic TrueTime) | True globally distributed ACID database; accepts latency for linearizability. |
| **Apache ZooKeeper** | **PC/EC** | **Consistent** (blocks minority partitions) | **Consistent** (leader sequences all state updates) | Coordination engine; stale configuration data is considered a failure. |
| **MongoDB** | **PC/EC** (default) | **Consistent** (primary step-down on partition) | **Consistent** (reads/writes routed to primary) | Can be reconfigured to PA/EL via secondary read preferences. |
| **VoltDB / Megastore**| **PC/EC** | **Consistent** (strict serializability) | **Consistent** (synchronous commit across replicas) | High-performance transactional ACID database. |

---

## Production Architectural Selection Framework

When selecting database technology in a system design interview:

1. **Financial, Billing, Identity, Inventory Allocations:**
   - **Requirement:** Zero tolerance for negative balances or phantom inventory.
   - **Verdict:** Choose **PC/EC** (PostgreSQL with synchronous replication, Google Cloud Spanner, CockroachDB).
2. **Social Feeds, Chat Presence, Metrics Telemetry, Video Recommendations:**
   - **Requirement:** Extreme throughput, global scale, tolerance for temporary seconds-long replication lag.
   - **Verdict:** Choose **PA/EL** (Apache Cassandra, ScyllaDB, Amazon DynamoDB).
3. **Distributed Coordination, Master Election, Service Discovery:**
   - **Requirement:** Single absolute source of truth for cluster state.
   - **Verdict:** Choose **PC/EC** (`etcd`, Apache ZooKeeper, Consul).

---

> [!NOTE]
> ### Teacher FAQ & Common Beginner Mistakes
>
> **Q: Isn't a single-node MySQL or PostgreSQL database a "CA" system?**  
> **Teacher's Answer:** A single-node relational database does not have network partitions because it does not have a distributed network; it has no $P$. However, a single node has a single point of failure (SPOF). The moment you add a read replica or failover standby over the network, you are now a distributed system subject to network partitions, and you are immediately bound by CAP: either replication is asynchronous (AP/EL) or synchronous (CP/EC).
>
> **Q: How does Google Spanner claim to provide both high availability and strict external consistency?**  
> **Teacher's Answer:** Marketing literature occasionally claims Spanner "beats CAP." It does not. Spanner is formally a **CP/EC** system. When a network partition occurs, minority quorums become unavailable. However, Google invests billions in private, redundant optical fiber meshes, independent routing hardware, and atomic clocks (TrueTime API). Because Google's physical network failure probability is extraordinarily low (five 9s), Spanner achieves pragmatic "operational availability" while remaining strictly mathematically CP.
>
> **Q: What is the difference between Eventual Consistency, Casual Consistency, and Linearizability?**  
> **Teacher's Answer:**  
> - **Linearizability (Strong):** Real-time global wall-clock ordering. If write $W_1$ finishes at 12:00:00.001, any read starting at 12:00:00.002 anywhere in the universe is guaranteed to observe $W_1$.
> - **Causal Consistency:** Operations that are causally related (e.g., a question and its answer) must be observed in the same order by all replicas. Unrelated operations can be seen in different orders.
> - **Eventual Consistency:** Weakest guarantee. If no further writes occur, all replicas will eventually converge to identical values. No bounds are placed on how long convergence takes.
