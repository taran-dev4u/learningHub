# Consistency Models

Welcome to the definitive masterclass on consistency models in distributed data systems. When designing scalable architectures, replication is mandatory: we duplicate data across multiple servers, availability zones, and geographical regions to survive hardware failures and eliminate read bottlenecks.

However, replication creates a fundamental dilemma: **As soon as multiple nodes hold copies of the same data, how do we guarantee they agree on what the current data is?**

In this masterclass, we explore the formal mathematical spectrum of consistency—from **Linearizability** and **Strict Serializability** down to **Causal Consistency**, **Session Guarantees**, and **Eventual Consistency with CRDTs**.

---

## Linearizability (strong) — every read returns latest write

### 1. Mathematical Definition of Linearizability
**Linearizability** (often referred to as **Strong Consistency**, **Atomic Consistency**, or **External Consistency**) is the strongest single-object consistency guarantee in distributed systems. Formulated by Maurice Herlihy and Jeannette Wing in 1990, linearizability guarantees:

1. **Global Real-Time Total Order:** All operations appear to take effect at a discrete, instantaneous point in time between their invocation and response.
2. **Freshness Guarantee:** Once a write completes (the client receives acknowledgment from the server at time $T_{finish}$), *any* read that begins at or after $T_{finish}$ **must** return the value of that write or a subsequent write.

```
Time ------------------------------------------------------------------------>

Client A:  [--- Write(x = 5) ---]
                                  ^ (Write completes at T1)
                                  
Client B:                           [--- Read(x) returns 5 ---]  (Valid)
Client C:                           [--- Read(x) returns 0 ---]  (VIOLATION! Stale read)
```

In a linearizable system, there is no stale data, no split-brain time travel, and no conflicting versions. The distributed system behaves as if there were only **one single copy of data in the entire universe**, updated atomically.

### 2. Linearizability vs Serializability (The Classic Interview Trap)
A senior engineer candidate must never confuse these two terms:

| Architectural Property | Linearizability | Serializability |
|---|---|---|
| **Scope** | **Single Object / Register**, Single Operation | **Multi-Object, Multi-Operation Transactions** |
| **Domain** | Distributed Systems & Network Replication | Database Transaction Isolation (ACID) |
| **Real-Time Constraint?** | **Yes:** Bound by global wall-clock time order. | **No:** Transactions must execute as if serial, but the order does not have to match real-time wall clock. |
| **Combined Gold Standard** | **Strict Serializability (External Consistency):** Transactions are serializable AND their order matches real-time wall-clock completion order (e.g., Google Spanner via TrueTime). |

### 3. How to Implement Linearizability
Linearizability cannot be achieved with simple asynchronous replication. It requires synchronous consensus or centralized coordination:
1. **Single Leader with Synchronous Replication:** All writes and reads funnel through a single leader node. Reads must either read from the leader or execute a **Read Index** / **Lease Read** check to prevent stale reads from a deposed leader during network partitions.
2. **Consensus Protocols (Raft, Multi-Paxos):** Updates must be accepted by a strict majority quorum ($Q > N/2$) of nodes before returning success.
3. **TrueTime Hardware Clocks (Google Spanner):** Uses atomic clocks and GPS receivers in every datacenter to bound clock uncertainty $\epsilon \le 7	ext{ms}$, guaranteeing strict real-time transaction ordering across global datacenters.

### 4. The PACELC Trade-Off
The CAP Theorem states that during a network **P**artition, you must choose between **A**vailability and **C**onsistency. Daniel Abadi extended this with the **PACELC Theorem**:
$$	ext{If } \mathbf{P} 	ext{ (Partition) } \longrightarrow \mathbf{A} 	ext{ vs } \mathbf{C}; \quad 	ext{Else } \mathbf{E} 	ext{ (Else/Normal) } \longrightarrow \mathbf{L} 	ext{ (Latency) vs } \mathbf{C} 	ext{ (Consistency)}$$

Even when the network is 100% healthy, **linearizability incurs severe latency penalties**. A write cannot return until round-trip network acknowledgments travel between replicas across the datacenter or cross-region fiber cables.

---

## Eventual consistency — replicas converge given enough time

### 1. The Asynchronous Replication Paradigm
At the opposite end of the spectrum lies **Eventual Consistency** (the foundation of Werner Vogels' seminal 2007 paper on Amazon's Dynamo architecture).

- **Core Guarantee:** If no further mutations are made to a given data item, all replicas will **eventually** converge to identical state.
- **Immediate Return:** Writes return `200 OK` as soon as the local node commits the change to disk, without waiting for remote replicas to acknowledge.
- **Asynchronous Replication:** Background replication threads propagate mutations over the network in the background.

```
[Client] --- Write(cart = [itemA]) ---> [Replica 1] (Returns 200 OK immediately!)
                                             |
                                    (Async Replication)
                                             |
                                             v (50ms - 200ms lag)
                                        [Replica 2]
                                        [Replica 3]
```

### 2. Quorum Mathematics ($R + W > N$)
Eventual consistency systems (Cassandra, DynamoDB, ScyllaDB) allow developers to configure consistency levels per-operation using Quorums:
- $N$ = Replication factor (e.g., 3 copies of data).
- $W$ = Number of replicas that must acknowledge a write before success.
- $R$ = Number of replicas that must respond to a read before returning to the client.

#### Strong Quorum Rule:
$$\mathbf{R + W > N}$$
By the Pigeonhole Principle, if $R + W > N$, the read quorum and the write quorum **must overlap by at least one replica**. That overlapping replica is guaranteed to hold the latest version!

```
Example: N = 3 Replicas [R1, R2, R3]
Write: W = 2 (Replicas R1, R2 acknowledge)
Read:  R = 2 (Replicas R2, R3 respond)
Overlap: R2 is present in both! R2 returns the newest timestamp.
```

#### Weak / Eventual Quorum ($R + W \le N$):
If $W = 1$ and $R = 1$ in an $N = 3$ system, $R + W = 2 \le 3$. Writes and reads can hit completely disjoint replicas, yielding stale reads. This provides maximum throughput and minimal latency at the expense of consistency.

### 3. Healing Mechanisms in Eventual Consistency
How do replicas converge when network packets are dropped?
1. **Read Repair:** When a client issues a quorum read ($R = 2$), the coordinator compares timestamps. If Replica 2 has version 5 and Replica 3 has version 4, the coordinator returns version 5 to the client and asynchronously pushes version 5 to Replica 3.
2. **Anti-Entropy with Merkle Trees:** In the background, nodes exchange cryptographic hash trees (**Merkle Trees**) representing their keyspaces. Nodes can compare millions of records in seconds by checking only the root hashes of subtrees, transferring only the exact divergent keys over the wire.
3. **Hinted Handoff:** If a replica is temporarily down, another node accepts the write and stores a "hint." Once the destination node recovers, the hint is delivered.

---

## Read-your-writes — you always see your own writes

### 1. The Human Expectation Dilemma
Consider the following real-world scenario on an eventual consistency platform:
1. User updates their profile bio: `"Senior Software Engineer at Google"`.
2. The HTTP `POST` completes and the browser redirects to the profile page.
3. The browser sends a `GET /profile`. The load balancer routes the request to a replica that is 50ms behind.
4. The user sees their **old bio**!
5. The user assumes the application is broken, gets frustrated, and submits the update 3 more times.

**Read-Your-Writes Consistency** (also known as **Read-After-Write Consistency**) guarantees that a given user will **always observe their own updates immediately**, even if all other users in the system continue to observe stale data for several seconds.

```
User Alice:   [Write(bio = "Google")] ----> [Replica 1]
                     |
User Alice:   [Read(bio)] ----------------> Must route to Replica 1! (Sees "Google")
User Bob:     [Read(bio)] ----------------> Routes to Replica 2 (Sees old bio temporarily; Valid!)
```

### 2. Production Implementation Architectures
How do high-scale distributed systems guarantee Read-Your-Writes without making the entire database linearizable?

1. **User-Pinned Sticky Routing:**
   - After any mutation, the API gateway sets a short-lived cookie: `X-Recently-Updated: true; Max-Age=60`.
   - Any read request bearing this cookie is automatically routed directly to the **Leader / Primary replica** (or the exact replica that accepted the write).
   - Reads from other users continue to hit load-balanced read replicas.
2. **Client-Side Version Tracking (Logical Sequence Vectors):**
   - When a write succeeds, the server returns the committed transaction version or timestamp: `{"version": 10842}`.
   - The client includes `X-Min-Version: 10842` in subsequent read headers.
   - A read replica checks its internal replication lag: if its local version is `< 10842`, it either waits for replication to catch up or delegates the query to the primary.
3. **Optimistic Local UI State (Client-Side Caching):**
   - The mobile or web app updates its local Redux/React state immediately upon API response without re-fetching from the backend.

---

## Causal consistency — causally related ops seen in same order

### 1. Causality & Lamport's Happens-Before Relation
In a distributed system, physical clocks drift. We cannot rely on wall-clock timestamps to determine what caused what. Leslie Lamport defined the **Happens-Before Relation ($a 	o b$)**:
- If event $a$ and event $b$ occur in the same process, and $a$ occurs before $b$, then $a 	o b$.
- If event $a$ is the sending of a message and event $b$ is the receipt of that message, then $a 	o b$.
- Transitivity: If $a 	o b$ and $b 	o c$, then $a 	o c$.

**Causal Consistency** guarantees that operations that are causally related are observed in the **exact same order by every node in the system**. Operations that are concurrent (not causally related) may be observed in different orders.

### 2. The Question-and-Answer Anomaly
Without causal consistency, casual observers experience bizarre temporal anomalies:

```
[Alice in New York]                     [Bob in London]                     [Charlie in Tokyo]
        |                                      |                                    |
(1) Posts Question:                            |                                    |
    "Who won the game?"                        |                                    |
        |--- (Replicated to Bob) ------------->|                                    |
        |                                (2) Bob replies:                           |
        |                                    "Real Madrid won!"                     |
        |                                      |--- (Replicated to Charlie) ------->|
        |                                      |                                    |
        |                                      |                        (Charlie sees Bob's reply)
        |                                      |                        "Real Madrid won!"
        |                                      |                                    |
        |--- (Network Lag: Replicated slowly to Charlie) -------------------------->|
        |                                                                           |
        |                                                               (Charlie finally sees Alice's post)
        |                                                               "Who won the game?"
```
Under naive eventual consistency, Charlie sees the answer *before* the question was ever asked! Causal consistency guarantees that Charlie's node buffers Bob's reply until Alice's question has arrived and been processed.

### 3. Implementation via Vector Clocks
To track causality across $K$ independent nodes, systems attach a **Vector Clock** $V$ (an array of logical counters, one per node) to every data mutation:
1. Each node increments its own counter before generating an event: $V_i[i] = V_i[i] + 1$.
2. The vector clock is transmitted with the message payload.
3. When node $j$ receives vector $V_{msg}$, it verifies whether $V_{msg}$ causally succeeds its local state. If so, it merges the vector:
   $$V_j[k] = \max(V_j[k], V_{msg}[k]) \quad orall k$$

---

## Monotonic reads — never see older value after reading newer

### 1. The Time-Travel Anomaly
Imagine you are browsing Reddit or Hacker News on your mobile phone:
1. You load the front page: you see an article with **100 upvotes** and **25 comments**.
2. You click on the article to read the comments. Your cellular connection bounces to a different cell tower, routing your HTTP request to a different read replica.
3. That read replica has 5 seconds of replication lag.
4. The page loads showing **80 upvotes** and **10 comments**!
5. To the user, data appears to have traveled backward in time!

**Monotonic Reads Consistency** guarantees that if a client has observed a value at state $S_1$, they will **never observe an earlier state $S_0$ on any subsequent read**.

```
Client Read 1 (Replica A, version 5)  -> Returns Version 5
Client Read 2 (Replica B, version 3)  -> BLOCKED or RE-ROUTED! Must not return Version 3.
```

### 2. Architectural Implementation
1. **Hash-Based Client Session Affinity:**
   Route all read requests from a given user ID to the same replica using consistent hashing or load balancer cookies. As long as the user talks to the same node, time only moves forward.
2. **Monotonic Version Headers:**
   The client stores the highest version number or timestamp it has ever observed (`last_seen_version`). On every subsequent read, the client transmits `If-Modified-Since` or `X-Min-Version`. If the selected replica is behind `last_seen_version`, the load balancer fails over to an up-to-date replica.

---

## CRDTs — conflict-free replicated data types for multi-master

### 1. Multi-Leader Replication & The Write Conflict Problem
In globally distributed applications (Google Docs, Figma, Apple Notes, edge databases), users must be able to write locally even when offline:
- Alice edits document paragraph 1 on an airplane.
- Bob edits document paragraph 1 in an office.
- When Alice's laptop reconnects to Wi-Fi, both replicas must synchronize.

If both nodes independently execute conflicting writes, traditional systems rely on **Last-Write-Wins (LWW)** using NTP timestamps.
> [!WARNING]
> **The Danger of Last-Write-Wins (LWW):**
> Last-Write-Wins silently destroys data! Because physical quartz clocks drift by up to 100-250ms per day across servers, an earlier write from a machine with a fast clock will permanently overwrite and obliterate a later write from a machine with an accurate clock.

### 2. Conflict-free Replicated Data Types (CRDTs)
Invented by Marc Shapiro and colleagues in 2011, **CRDTs** are mathematical data structures that can be replicated across multiple nodes concurrently. Even if replicas receive concurrent updates in completely different orders, **they are mathematically proven to converge to the exact same state without human intervention or distributed lock managers!**

#### The Semi-Lattice Mathematical Foundation:
A state-based CRDT forms a bounded semi-lattice equipped with a merge operator $\sqcup$ that satisfies three properties:
1. **Commutative:** $A \sqcup B = B \sqcup A$ (order of arrival does not matter).
2. **Associative:** $(A \sqcup B) \sqcup C = A \sqcup (B \sqcup C)$ (packet batching does not matter).
3. **Idempotent:** $A \sqcup A = A$ (duplicate packet delivery does not corrupt data).

### 3. Practical CRDT Types in Production

| CRDT Name | Full Type | Internal Mechanism | Production Use Case |
|---|---|---|---|
| **P-N Counter** | Positive-Negative Counter | Two integer arrays per node: `P[node_id]` (increments) and `N[node_id]` (decrements). Merge takes element-wise $\max$. Total value = $\sum P - \sum N$. | Discord active server member count, Reddit upvote/downvote counter. |
| **LWW-Element-Set** | Last-Write-Wins Element Set | Add-set and Remove-set containing `(element, timestamp)` tuples. Element is present if its add timestamp is greater than its remove timestamp. | User shopping carts, follower lists, social media bookmarking. |
| **OR-Set** | Observed-Removed Set | Assigns a unique UUID tag to each added element. Removing an element deletes all tags observed at that time. Resolves concurrent add/remove conflicts gracefully. | Distributed shopping cart items (Amazon Dynamo style). |
| **RGA / Yjs / Automerge** | Replicated Growable Array | Sequence CRDT where each character is a node with an immutable unique ID and pointer to its parent character. | **Collaborative text editors (Google Docs, Figma, Notion, VS Code Live Share).** |

---

### Comprehensive Consistency Spectrum Matrix

| Consistency Model | Performance / Latency | High Availability under Partition? | Prevents Stale Reads? | Common Implementation |
|---|---|---|---|---|
| **Linearizability** | Lowest (Synchronous WAN coordination) | **No (CP)** | **Guaranteed** | Raft, Paxos, Spanner TrueTime, etcd, ZooKeeper |
| **Sequential Consistency** | Low | **No (CP)** | No (Allows global lag, but identical order) | Lamport logical clocks, single thread execution |
| **Causal Consistency** | Medium | **Yes (AP)** | No (Preserves causality only) | Vector Clocks, MongoDB Causal Sessions |
| **Read-Your-Writes** | High | **Yes (AP)** | For author only | Sticky leader routing, version cookies |
| **Monotonic Reads** | High | **Yes (AP)** | Prevents time-travel only | Client version vectors, replica pinning |
| **Eventual Consistency** | **Highest (Immediate local commits)** | **Yes (AP)** | No (Stale reads permitted) | Cassandra, DynamoDB, CouchDB, CRDTs |

---

> [!TIP]
> **Summary Decision Rule for System Design Interviews:**
> - If designing **financial transfers, ticket booking, or password auth**: Enforce **Linearizable / Strict Serializability** (Raft / Paxos / RDBMS with 2PC).
> - If designing **social feeds, view counters, or analytics**: Use **Eventual Consistency with Tunable Quorums** ($R=1, W=1$).
> - If designing a **collaborative workspace or offline-first mobile app**: Use **CRDTs (Yjs / Automerge)** to guarantee seamless convergence.
> - For general consumer web apps: Deploy **Read-Your-Writes + Monotonic Reads** at the API gateway layer to eliminate user-facing time travel anomalies without sacrificing backend horizontal scalability.
