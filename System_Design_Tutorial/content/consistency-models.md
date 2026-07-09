# Consistency Models

## Overview
When you have multiple copies of your data (replicas) to ensure High Availability, you introduce a massive problem: **What happens when the copies disagree?**

If a user updates their password on Replica A, and immediately tries to log in via Replica B, will it work? The answer depends entirely on the **Consistency Model** you choose. 

This masterclass explains the spectrum of consistency, from strict and slow, to chaotic and fast.

---

## Linearizability (strong) — every read returns latest write

**Linearizability (Strong Consistency)** is the gold standard of correctness. It gives the illusion that there is only one copy of the data in the entire world, and all operations happen atomically in real-time.

- **How it works:** If a write completes on Replica A, *no subsequent read anywhere in the system* can return the old value. The system must synchronize the update across all replicas before confirming the write, or it must route all reads to the leader.
- **The Trade-off:** High Latency. If Replica B is in a different datacenter, the system has to wait for network packets to cross the country before returning success to the user.
- **Use Case:** Financial transactions, password changes, inventory management (preventing double-booking).

---

## Eventual consistency — replicas converge given enough time

**Eventual Consistency** is the Wild West. It prioritizes speed over correctness.

- **How it works:** When a write hits Replica A, it returns success to the user immediately. Replica A will asynchronously copy the data to Replica B "eventually" (usually in milliseconds, but sometimes seconds).
- **The Trade-off:** Stale Data. If a user reads from Replica B before the sync happens, they will see old data. 
- **Use Case:** Facebook likes, YouTube view counts, search engine indexing. (If you see a video has 10,000 views, but it actually has 10,050, it does not matter).

---

## Read-your-writes — you always see your own writes

This is a step up from Eventual Consistency, focused entirely on the user experience. 

Imagine you comment on a YouTube video. The system uses Eventual Consistency, so your comment hits Replica A. You refresh the page, but your browser is routed to Replica B (which hasn't received the sync yet). Your comment disappears! You assume it broke, so you submit it again.

**How to fix it:**
We use **Read-your-writes (Session) Consistency**. 
- The system guarantees that a specific user will *always* see their own updates immediately, even if the rest of the world sees stale data. 
- **Implementation:** The system could route all reads from User 123 to the exact same replica they just wrote to, or it can temporarily cache the user's write locally on the client device.

---

## Causal consistency — causally related ops seen in same order

Sometimes, the exact order of events matters, but only for events that are actually related to each other.

**The Problem:**
1. Alice writes: *"I lost my job today."*
2. Bob replies to Alice: *"I'm so sorry!"*

Under pure eventual consistency, Replica B might receive Bob's reply *before* Alice's original post. A user reading from Replica B sees Bob saying "I'm so sorry!" out of nowhere.

**How to fix it (Causal Consistency):**
The system tracks the causal relationship (Bob's reply requires Alice's post to exist). It guarantees that no replica will display Bob's reply until it has successfully processed Alice's post first. 

---

## Monotonic reads — never see older value after reading newer

Imagine you are reading a news feed and refreshing the page.
1. You read from Replica A: You see 5 new articles.
2. You refresh. Your request hits Replica B (which is lagging behind).
3. You suddenly see only 3 articles. It looks like the system went backwards in time!

**Monotonic Reads Consistency** guarantees that time only moves forward for a single user. Once you have seen data from time `T`, you will never be served data older than `T` on subsequent reads.
- **Implementation:** Stick the user's session to a specific replica, or have the client pass a timestamp/version vector with every read request so the server knows not to serve stale data.

---

## CRDTs — conflict-free replicated data types for multi-master

If you allow users to write to *any* replica simultaneously (Multi-Master), you will inevitably get conflicts. 
What if Alice and Bob try to edit the exact same paragraph in a Google Doc at the exact same millisecond?

**CRDTs (Conflict-free Replicated Data Types)** are mathematical data structures that automatically resolve conflicts without needing a central coordinator.
- **How they work:** The data types (like Counters, Sets, or Text sequences) are designed so that the order of operations does not matter (they are commutative). No matter what order Replica A and Replica B receive the network packets, they will mathematically converge to the exact same final state.
- **Use Case:** Collaborative editing (Google Docs, Figma), distributed counters (Discord online users).

> [!NOTE]
> **Conclusion:** In an interview, default to Eventual Consistency for performance. Only reach for Strong Consistency if money, security, or critical inventory is involved. Always be ready to explain the user-experience trade-offs.
