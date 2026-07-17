# Consensus Algorithms: Raft & Paxos

Welcome to one of the most intellectually fascinating, yet notoriously intimidating areas of distributed systems: **Consensus Algorithms**.

If you've ever wondered how a cluster of independent servers managed by Kubernetes agrees on the current state of the world without breaking into utter chaos, or how a distributed database guarantees that an account balance doesn't simultaneously read as $100 and $0, you are about to find out.

In a distributed environment, nodes fail, networks drop packets, and servers pause for garbage collection. Despite these inevitable failures, the system must act as a single source of truth. **Consensus** is the process by which a collection of machines agree on a single value or a sequence of values, even if some of the machines are crashing or unreachable.

Let's dive into exactly how the industry solves this, focusing on the two heavyweight champions of consensus: **Paxos** and **Raft**.

## The Problem of Consensus: Why Do We Need It?

Imagine a team of five software engineers trying to decide where to eat lunch. If they are all in the same room, one person can shout "Pizza!" and if three people nod, it's decided. This is easy.
But now imagine the five engineers are in different rooms, communicating only by sliding notes under the doors. Sometimes the notes get lost. Sometimes an engineer falls asleep. How do they ever guarantee that they all ultimately agree on "Pizza" and that nobody secretly goes to get "Sushi"?

In distributed systems, this is the **State Machine Replication** problem. We want multiple servers to maintain identical copies of the same data (a replicated log). If a client sends a command "Set X = 5", all servers must apply "Set X = 5" in the exact same order, so their final states perfectly match.

> [!NOTE]
> **Teacher FAQ: Why not just use a single database?**
> A single database is a single point of failure. If that machine dies, your system goes down. To achieve High Availability (HA), we replicate data across multiple nodes. But the moment you have multiple copies of data, you need a mechanism to keep them strictly synchronized. That mechanism is the consensus algorithm.

---

## Paxos — The Original Heavyweight

Introduced by Leslie Lamport in the 1990s, **Paxos** is the theoretical grandfather of modern consensus.

### How Paxos Works (At a High Level)
Paxos operates in phases to agree on a single value. When applied repeatedly (Multi-Paxos), it agrees on a sequence of values (a log).
1. **Prepare Phase**: A Proposer asks a quorum (majority) of Acceptors if it's okay to propose a value, attaching a unique, strictly increasing proposal number.
2. **Promise Phase**: Acceptors promise not to accept any proposals with a lower number than the one they just saw.
3. **Accept Phase**: If the Proposer gets promises from a majority, it sends the actual value (the "Accept Request").
4. **Learn Phase**: Once a majority of Acceptors accept the value, it is considered chosen, and Learners are notified.

### Why is Paxos so infamous?
Lamport originally explained Paxos using a metaphor about a parliament on the fictional Greek island of Paxos. The academic paper was famously difficult to understand. Furthermore, the original paper only described how to agree on a *single* value. Building a practical system requires a continuous log of values (Multi-Paxos), and bridging the gap between theoretical Paxos and a production-grade Multi-Paxos implementation is remarkably difficult.

> [!WARNING]
> **Common Beginner Mistake**
> Many beginners think they can just "implement Paxos" over the weekend. In reality, Paxos is incredibly hard to implement correctly because it leaves many edge cases (like leader election, log truncation, and dynamic cluster membership) as exercises for the reader.

---

## Raft — Designed for Understandability

Because Paxos was so notoriously difficult to understand and implement, Diego Ongaro and John Ousterhout created **Raft** in 2014. The explicit goal of Raft was **understandability**—it decomposes the consensus problem into three distinct, independent sub-problems: **Leader Election**, **Log Replication**, and **Safety**.

### 1. Leader Election: Who's the Boss?

Raft enforces a strict strong-leader model. The system can only have one leader at a time, and all client requests must go through the leader.

Servers in Raft can be in one of three states:
- **Follower**: Passive. They only respond to requests from leaders and candidates.
- **Candidate**: A follower whose heartbeat timer has expired and is now campaigning to become the leader.
- **Leader**: The active boss. Handles all client requests and replicates the log to followers.

**The Election Process:**
1. **Heartbeats:** The leader continuously sends heartbeat messages (empty AppendEntries RPCs) to all followers to say "I'm still alive!"
2. **Election Timeout:** Followers wait for these heartbeats. If a follower doesn't receive a heartbeat within a randomly chosen time interval (e.g., 150ms - 300ms), it assumes the leader is dead.
3. **Campaigning:** The follower transitions to a **Candidate**, votes for itself, and sends RequestVote RPCs to all other nodes.
4. **Majority Rules:** If the candidate receives votes from a majority of nodes (a quorum) for that term, it becomes the new Leader.

> [!TIP]
> **Why Randomized Timeouts?**
> Imagine two followers notice the leader is dead at the exact same millisecond. They both become candidates, they both request votes, and they split the votes 50/50. Nobody gets a majority! This is a "split vote." By randomizing the election timeout (e.g., Node A waits 150ms, Node B waits 220ms), Node A will almost always wake up first, request votes, and win the election before Node B even realizes the leader is gone.

### 2. Log Replication: Keeping Everyone in Sync

Once a leader is elected, how does it process client requests?

Let's walk through the **Log Replication** flow step-by-step:
1. **Client Request:** A client sends a command to the leader (e.g., "Set X = 3").
2. **Append to Local Log:** The leader appends this command to its own log. It is currently *uncommitted*.
3. **Replicate:** The leader sends `AppendEntries` RPCs containing the command to all followers.
4. **Acknowledge:** Once a follower successfully writes the command to its local log, it replies "Success" to the leader.
5. **Commit:** The leader waits until a **quorum (majority)** of nodes have successfully replicated the entry. Once a majority is reached, the leader officially **commits** the entry to its state machine and replies "Success" to the client.
6. **Notify Followers:** In subsequent heartbeats, the leader tells followers that the entry is committed, and they apply it to their own state machines.

### 3. Safety Guarantees

Raft provides strict safety guarantees, ensuring that no two nodes will ever apply a different sequence of logs.
A key safety property is that **a leader must have all committed entries from previous terms.** When a candidate requests votes, it includes the index of its last log entry. A follower will deny the vote if its own log is more up-to-date than the candidate's log. This guarantees that only a node with all previously committed data can ever become a leader.

---

## Raft vs. Paxos: The Showdown

| Feature | Paxos | Raft |
| :--- | :--- | :--- |
| **Primary Goal** | Mathematical proof of correctness for consensus | Understandability and practical implementation |
| **Leader Model** | Can operate without a strict stable leader, though Multi-Paxos usually uses one | Strictly requires a single strong leader |
| **Understandability** | Notoriously difficult | Decomposed into logical components (Election, Replication) |
| **Log Matching** | Logs can have gaps that get filled in later | Logs are strictly continuous and matched from the beginning |
| **Popularity in modern systems** | Legacy systems, Google Spanner, Cassandra (lightly) | Almost all modern orchestration and coordination systems |

> [!NOTE]
> **Teacher FAQ: What is a "Quorum" and why is it always a majority?**
> A quorum is the minimum number of nodes that must agree for an operation to succeed. In a 5-node cluster, the quorum is 3. We use a simple majority $(N/2 + 1)$ because it guarantees that any two quorums will always overlap by at least one node. If Quorum A committed a write, and Quorum B is trying to elect a leader, the overlapping node guarantees that Quorum B knows about Quorum A's write. This prevents "split-brain" scenarios.

---

## Where Are They Used?

You interact with systems relying on these algorithms every day.

- **etcd**: The key-value store that acts as the brain of **Kubernetes**. It stores the entire cluster state and configuration. It uses **Raft**.
- **ZooKeeper**: Originally from the Hadoop ecosystem, used by Kafka (historically) for managing brokers and topics. It uses **ZAB** (ZooKeeper Atomic Broadcast), which is fundamentally very similar to Raft.
- **CockroachDB**: A distributed SQL database that uses **Raft** extensively for replicating ranges of data across nodes.
- **MongoDB**: Its Replica Sets use a consensus protocol heavily inspired by **Raft** for leader election and oplog replication.
- **Google Spanner**: Google's globally distributed database uses **Paxos** underneath to guarantee strict consistency across data centers.

### Summary
If you are designing a system that requires a bulletproof, strongly consistent metadata store or coordinator, you don't write your own consensus protocol. You pull an off-the-shelf system like etcd or ZooKeeper, which have spent years hardening their Raft/ZAB implementations against the chaos of distributed networks.
