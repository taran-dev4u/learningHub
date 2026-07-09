# CAP & PACELC Theorems

## Overview
When you design a distributed database, you are forced to make impossible choices. You cannot have a system that is perfectly consistent, always available, and immune to network failures. 

The **CAP Theorem** and the **PACELC Theorem** are the fundamental laws of physics for distributed systems. Memorize these, and you will understand why different databases (like Postgres vs Cassandra) were built the way they were.

---

## CAP Theorem — Consistency + Availability + Partition Tolerance

In 2000, Eric Brewer presented the CAP Theorem, stating that any distributed data store can only guarantee **two out of the following three** properties:

1. **Consistency (C):** Every read receives the most recent write, or an error. (Strong Consistency).
2. **Availability (A):** Every request receives a non-error response, without the guarantee that it contains the most recent write.
3. **Partition Tolerance (P):** The system continues to operate despite an arbitrary number of messages being dropped or delayed by the network between nodes.

> [!WARNING]
> **Beginner Mistake:** People often say "You have to choose two: CA, CP, or AP." This is misleading. In the real world, networks *always* fail. **Partition Tolerance (P) is non-negotiable.** Therefore, you must always choose between Consistency (C) and Availability (A) when a network partition occurs.

---

## Partition Tolerance is non-negotiable on real networks

Imagine two datacenters, one in New York and one in London. A transatlantic fiber optic cable is cut by an anchor. The two datacenters can no longer talk to each other. This is a **Network Partition**.

Because P is forced upon us by reality, we must decide how our system reacts during this partition.

### The Decision
- **Option 1:** Allow both datacenters to keep accepting writes from users. (We choose **Availability** -> AP System). The trade-off is that data diverges.
- **Option 2:** Shut down one datacenter (refuse writes) to prevent data from diverging. (We choose **Consistency** -> CP System). The trade-off is downtime.

---

## CP systems: refuse writes during partitions (ZooKeeper, HBase, MongoDB strict)

If your system handles financial transactions, you cannot afford divergent data. You must choose Consistency.

**How a CP System works during a partition:**
If the network splits, the system will detect that nodes cannot communicate. To prevent conflicting writes, it will force nodes that cannot talk to the majority leader to shut down or reject writes entirely. It sacrifices Availability to guarantee that no user ever reads or writes corrupt/stale data.

- **Examples:** Apache ZooKeeper, HBase, etcd, MongoDB (when configured with majority read/write concerns).

---

## AP systems: always accept, reconcile later (Cassandra, DynamoDB, CouchDB)

If your system handles Facebook Likes or shopping cart items, you cannot afford downtime. You must choose Availability.

**How an AP System works during a partition:**
If the network splits, both the New York and London datacenters will continue to accept writes independently. 
Yes, the data will diverge. But the system prioritizes the user experience. Once the network is repaired, the system will use complex algorithms (like CRDTs or Last-Write-Wins) to merge the data back together.

- **Examples:** Apache Cassandra, Amazon DynamoDB, Couchbase.

---

## PACELC: Latency vs Consistency even without partitions

The CAP Theorem is great, but it has a massive flaw: It only applies *when the network breaks*. But networks are usually working fine 99.9% of the time! What trade-offs are we making during normal operation?

In 2010, Daniel Abadi proposed the **PACELC Theorem**, which fixes CAP's blind spot.

It states:
- If there is a **P**artition, how does the system trade off **A**vailability and **C**onsistency? (This is just CAP).
- **E**lse (when the system is running normally), how does the system trade off **L**atency and **C**onsistency?

### The Normal Operation Trade-off (L vs C)
Even without a network failure, if you want Strong Consistency, you have to wait for data to replicate across the globe before returning success to the user. This increases **Latency**. 
If you want low Latency, you return success immediately without waiting for replication. This sacrifices **Consistency**.

> [!NOTE]
> **Summary for Interviews:** 
> - Use **CAP** to explain how your database survives a datacenter outage.
> - Use **PACELC** to explain why your database is fast (low latency) or perfectly accurate (high consistency) during normal day-to-day operations.
