# Leader Election, Heartbeats & Failure Detection

In a distributed system consisting of hundreds or thousands of servers, one absolute truth reigns supreme: **Nodes will fail.** Hard drives will crash, network cables will be unplugged, and virtual machines will be aggressively terminated by your cloud provider.

If your system is designed around a group of worker nodes coordinating with each other, how do they know when one of their peers has vanished into the digital void? And if the node that vanished happened to be the boss (the Leader), how do the remaining nodes peacefully agree on a new boss without causing a civil war (a "split-brain" scenario)?

In this masterclass, we will dissect the critical mechanisms of **Failure Detection** and **Leader Election**.

---

## 1. Failure Detection: Are You Still There?

Before a cluster can react to a failure, it must first detect it. But detecting failure over a network is surprisingly tricky. If Node A asks Node B a question and Node B doesn't respond, did Node B crash? Is the network cable cut? Is Node B just paused for a massive 5-second Java Garbage Collection cycle? It is fundamentally impossible in an asynchronous network to perfectly distinguish between a crashed node and a very slow node.

### The Standard Approach: Heartbeats

A **Heartbeat** is the simplest and most common form of failure detection.
Think of it as a diver holding a flashlight under the water, flashing it every second. As long as the boat above sees the flash, they know the diver is alive.

- **Mechanism**: Node A periodically (e.g., every 1 second) sends a tiny "I am alive" network packet (a ping or heartbeat) to a central coordinator or to its peers.
- **Timeout**: The receiver maintains a timer. If it doesn't receive a heartbeat from Node A within a defined threshold (e.g., 5 seconds), it marks Node A as "Dead".

> [!WARNING]
> **The Timeout Dilemma**
> If your timeout is too short (e.g., 500ms), a momentary network blip or CPU spike will cause a **false positive**. The system will declare the node dead, spin up a replacement, and shift data around unnecessarily, causing huge system thrashing.
> If your timeout is too long (e.g., 60 seconds), a **real failure** goes unnoticed for a full minute, leaving clients waiting in limbo for a dead node to reply.

### Phi Accrual Failure Detector: The Smart Heartbeat

Because fixed timeouts are brittle in volatile cloud environments, systems like **Apache Cassandra** and **Akka** use a probabilistic model called the **Phi ($\Phi$) Accrual Failure Detector**.

Instead of a binary "Node is Alive / Node is Dead", Phi Accrual calculates a probability score that a node has crashed based on the historical arrival times of its heartbeats.

- It records a sliding window of recent heartbeat intervals.
- It calculates the mean and standard deviation of these intervals.
- If heartbeats normally arrive exactly every 1.0s, and suddenly it's been 2.5s, the $\Phi$ score spikes, indicating high confidence of a crash.
- If heartbeats are normally jittery (arriving anywhere from 0.8s to 3.0s), waiting 2.5s won't raise the $\Phi$ score much.

This allows the system to dynamically adapt to network congestion and provide a smooth sliding scale of suspicion rather than a hard timeout.

### Gossip Protocol: Decentralized Health Checking

What if there is no central coordinator to receive heartbeats? In a massive, masterless cluster (like Cassandra or Amazon DynamoDB), nodes use a **Gossip Protocol**.

Think of Gossip like an office rumor mill.
1. Every second, Node A picks 3 random nodes and whispers its current state and what it knows about the health of other nodes.
2. Node B hears this, merges the data with its own knowledge, and next second, whispers to 3 other random nodes.
3. Information about a node's death propagates exponentially fast through the cluster without any central bottleneck.

---

## 2. Leader Election: Choosing the Boss

Once a leader is declared dead via failure detection, the cluster must promote a follower to take its place. This is **Leader Election**.

Having a single leader simplifies concurrency tremendously. Instead of resolving conflicts between multiple nodes writing to the same database row, you just force all writes to go through the Leader. But electing that leader safely is paramount.

### Algorithm 1: Raft Leader Election

As we discussed in the Consensus algorithms section, **Raft** handles this elegantly.
- Followers expect constant heartbeats from the Leader.
- If a follower's randomized timer expires, it becomes a Candidate and requests votes.
- It needs a strict majority (quorum) to become the new Leader.
- Because timers are randomized, collisions are rare, and a single node usually wins the majority quickly.

### Algorithm 2: The Bully Algorithm

The **Bully Algorithm** is a classic, aggressive approach. It assumes every node has a unique, totally ordered ID (Node 1, Node 2, Node 3...).

When Node 2 detects the leader (Node 5) is dead:
1. Node 2 sends an "ELECTION" message to all nodes with a *higher* ID than itself (Nodes 3, 4, 5).
2. If Node 3 is alive, it tells Node 2 "I'll take over from here" and initiates its own election, bullying Node 2 into submission.
3. Node 4 does the same to Node 3.
4. Finally, the highest ID node that is alive (Node 4) realizes nobody is higher than it. It declares "I am the new Leader!" (a "COORDINATOR" message) to everyone else.

*Trade-offs*: Simple to understand, but if the highest ID node is unstable (flapping up and down), it will continuously bully its way into leadership, crash, and trigger endless elections.

### Algorithm 3: ZooKeeper Sequential Nodes (Practical Election)

In modern enterprise architectures, services often don't run their own complex election algorithms. Instead, they outsource the problem to a coordination service like **ZooKeeper** or **etcd**.

**How ZooKeeper Leader Election works:**
1. You have 5 microservice instances. You want exactly one to be the active job scheduler.
2. All 5 instances connect to ZooKeeper and try to create an **Ephemeral Sequential ZNode** under `/scheduler/node-`.
3. ZooKeeper guarantees atomic creation and appends an incrementing sequence number to the node.
   - Instance A creates `/scheduler/node-00001`
   - Instance B creates `/scheduler/node-00002`
   - Instance C creates `/scheduler/node-00003`
4. The rule is simple: **Whoever has the lowest sequence number is the Leader.**
5. Instance A is the leader. Instances B and C just watch the node right before them.
6. If Instance A crashes, its connection to ZooKeeper drops. Because the node was *ephemeral*, ZooKeeper automatically deletes `/scheduler/node-00001`.
7. Instance B gets an alert that `node-00001` is gone. It looks at the list, realizes its `node-00002` is now the lowest, and instantly assumes leadership!

> [!TIP]
> **Why Watch the Predecessor?**
> In ZooKeeper, you never want 10,000 nodes all watching the Leader node simultaneously. If the leader dies, ZK would have to send 10,000 notifications simultaneously (the "Thundering Herd" problem). By having Node $N$ only watch Node $N-1$, a leader crash only wakes up exactly *one* node (the next in line).

---

## Comparison of Election Strategies

| Strategy | Mechanism | Best Used For |
| :--- | :--- | :--- |
| **Raft** | Majority vote with randomized timeouts | Core distributed databases, orchestration (etcd, Consul) |
| **Bully Algorithm** | Highest ID wins, aggressively claims leadership | Academic study, legacy distributed systems |
| **ZooKeeper/etcd locks** | Lowest sequential ephemeral node wins | Microservices, distributed job schedulers, Kafka controllers |

> [!NOTE]
> **Teacher FAQ: What happens if two nodes think they are the leader? (Split-Brain)**
> This is a disaster. If a network partition cuts a cluster in half, both halves might try to elect a leader. This is why **Quorum** is mandatory. If you have 5 nodes partitioned into a group of 3 and a group of 2, the group of 3 can achieve a quorum and elect a leader. The group of 2 cannot, so they pause. The cluster continues with exactly one leader, safely isolated in the majority partition.
