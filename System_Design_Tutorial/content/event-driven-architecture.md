# Event-Driven Architecture (EDA): Building Reactive Systems

Welcome to the pinnacle of asynchronous design. As systems grow from simple monoliths into sprawling microservice ecosystems, direct synchronous API calls (Service A calls Service B) become a tangled web of fragile dependencies.

**Event-Driven Architecture (EDA)** inverts this model. Instead of commanding another service to do something, a service simply announces, *"Hey, something just happened."* It is up to other services to listen and react.

Let's explore the fundamental patterns that make EDA robust, scalable, and complex.

## 1. Event Sourcing
### The State is the Sum of its History

In a traditional database (CRUD), we store the *current state*. If a user changes their address, we overwrite the old address. The history is lost.

**Event Sourcing** says: Do not store the current state. Store the *events* that led to the state.
Think of a bank account. A bank doesn't just store `balance = $500`. It stores an immutable ledger of transactions: `+$1000 (Deposit)`, `-$200 (Withdrawal)`, `-$300 (Transfer)`. The current balance is simply the **fold (aggregation) of all past events**.

- **Pros:** Perfect audit trail. 100% accurate history. You can "time travel" to see the system state at any point in the past. If you find a bug in how you calculate totals, you can fix the bug and replay all events to get the correct state.
- **Cons:** Complex. Event logs grow massive. Reading the current state requires replaying events, which is slow (solved by "snapshots" and CQRS).

## 2. CQRS (Command Query Responsibility Segregation)
### Splitting the Reads from the Writes

In traditional CRUD, the same data model is used for reading and writing. But in complex systems, the way you write data (validation, normalization) is wildly different from how you read data (fast aggregation, denormalized views).

**CQRS** separates them entirely:
- **Command Model (Writes):** Handles actions (`CreateUser`, `UpdateCart`). Highly normalized, optimized for business logic and data integrity. Often uses Event Sourcing.
- **Query Model (Reads):** Handles data retrieval. Optimized for fast reads. Data is denormalized, perhaps stored in Elasticsearch, Redis, or a flat NoSQL document.

**How they connect:** When a Command updates the write database, it publishes an Event. A worker listens to that event and updates the Query database.
*Note: This means your system is now **Eventually Consistent**.*

## 3. Choreography vs Orchestration
### How do Microservices coordinate a business process?

Imagine an e-commerce checkout: 1. Process Payment -> 2. Update Inventory -> 3. Ship Order. How do we manage this workflow across three separate microservices?

#### The Choreography Approach (Events)
Like dancers reacting to the music without a conductor.
- Order Service emits `OrderCreated`.
- Payment Service listens, charges the card, emits `PaymentSucceeded`.
- Inventory Service listens, reserves items, emits `InventoryReserved`.
- Shipping Service listens, ships the box.
- **Pros:** Highly decoupled. No single point of failure.
- **Cons:** Extremely hard to monitor. If an order gets stuck, it's difficult to track exactly *where* it stopped.

#### The Orchestration Approach (Central Coordinator)
Like a symphony with a conductor.
- An Orchestrator Service (e.g., AWS Step Functions, Temporal) receives the checkout request.
- It commands Payment Service: "Charge card." Waits for reply.
- It commands Inventory Service: "Reserve stock." Waits for reply.
- **Pros:** Centralized monitoring. Easy to implement complex retry logic and state tracking.
- **Cons:** The Orchestrator becomes a single point of failure and a potential bottleneck. Tightly couples the workflow logic.

> [!TIP]
> Use Orchestration for complex, critical business workflows (like payments and billing). Use Choreography for simple, highly decoupled reactions (like sending notification emails).

## 4. The SAGA Pattern
### Distributed Transactions without Locking

In a monolith, updating two tables is easy: you use a database transaction (ACID).
In microservices, you cannot use a single transaction across the Payment DB and the Inventory DB. Historically, systems used Two-Phase Commit (2PC), but it is blocking, slow, and scales poorly.

**The Saga Pattern** is a sequence of *local* database transactions.
Each step in the workflow updates local state and publishes an event to trigger the next step.

**What if something fails? (Compensating Actions)**
If Step 1 (Payment) succeeds, but Step 2 (Inventory) fails because the item is out of stock, we cannot "rollback" the Payment database transaction—it's already committed!
Instead, the Saga triggers a **Compensating Action**. It sends a `RefundPayment` command to undo the work of Step 1.
Sagas trade *Atomicity* for *Availability* and *Eventual Consistency*.

## 5. The Transactional Outbox Pattern
### The Dual-Write Problem

Here is a classic microservice bug:
You save a new User to your PostgreSQL database, and then you publish a `UserCreated` event to Kafka so the Email Service can send a welcome email.

```python
db.execute("INSERT INTO users ...") # Step 1: Write to DB
kafka.publish("UserCreated", user)  # Step 2: Publish to broker
```

**The Problem:** What if Step 1 succeeds, but the network crashes before Step 2? The user exists in the DB, but the event is never published. The Email Service never knows. The data is fundamentally out of sync. You cannot wrap a DB write and a Kafka publish in a single ACID transaction.

**The Solution: Transactional Outbox**
1. Create an `outbox` table in the *same database* as your user table.
2. In a single, atomic DB transaction, write the new user to the `users` table AND write the event payload to the `outbox` table.
3. A separate asynchronous process (a "Message Relay" or CDC tool like Debezium) continuously reads the `outbox` table and publishes the events to Kafka.
4. Once published, the event is marked as processed in the outbox.

This guarantees that if the DB write succeeds, the event *will* eventually be published. 100% reliable messaging.

---

> [!NOTE]
> ### Teacher FAQ & Common Beginner Mistakes
>
> **Q: Eventual Consistency scares me. What if a user creates an account, but the read database hasn't updated yet, so they get a "User Not Found" error when they log in?**
> **A:** This is a real UI/UX challenge! The most common solution is "Read Your Own Writes." The frontend caches the newly created user data locally, or the API routes reads from the *writer* for the first few seconds after an update, shielding the user from the backend latency.
>
> **Q: Is Debezium required for the Outbox pattern?**
> **A:** No. Debezium uses Change Data Capture (CDC) by reading the database's internal transaction log (like Postgres WAL), which is the most robust way. However, you can also just write a cron job or worker that queries `SELECT * FROM outbox WHERE status = 'pending'`, publishes to Kafka, and updates the status to 'sent'.
