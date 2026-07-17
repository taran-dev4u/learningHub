# HLD vs LLD Boundaries

Welcome to this masterclass on system design! Today, we are tackling a critical transition in software engineering: the boundary between High-Level Design (HLD) and Low-Level Design (LLD).

Many beginners blur the lines between these two phases. You might jump straight into writing classes when you should be defining APIs, or conversely, you might be drawing boxes for databases when your team needs class definitions. We are going to break down exactly where HLD ends and LLD begins, why both are absolutely necessary, and how to successfully hand off from one to the other.

## High-Level Design Scope

High-Level Design (HLD) is the 10,000-foot view of your system. If you are an architect designing a city, HLD is the city map showing highways, residential zones, commercial districts, and power grids.

### The "Why" Behind HLD
We need HLD because complex systems are too massive to comprehend line-by-line. We must first define the major moving parts. HLD focuses on **system architecture, data flow, scale, and integration**. It answers questions like:
- Which database should we use for user profiles? (e.g., PostgreSQL vs. MongoDB)
- How do we handle a surge in traffic? (e.g., Load Balancers, Auto-scaling groups)
- How do microservices communicate? (e.g., REST vs. gRPC vs. Message Queues like Kafka)

### Core Components of HLD
1. **Architecture Diagrams:** Block diagrams showing clients, load balancers, web servers, application servers, caches, and databases.
2. **Data Models (Logical):** Entity-Relationship (ER) diagrams indicating how major entities relate (e.g., User has many Orders).
3. **API Design (Macro):** Defining the RESTful endpoints (e.g., `POST /api/v1/orders`) without writing the exact JSON parsers.
4. **Capacity Planning:** Estimating QPS (Queries Per Second), storage, and network bandwidth.

> [!NOTE]
> **Teacher FAQ:** *Do I write any code during the HLD phase?*
> No! HLD is strictly language-agnostic. Whether you implement the system in Java, Go, or Python doesn't matter yet. The focus is purely on infrastructure, data flow, and component interactions.

## Low-Level Design Scope

If HLD is the city map, Low-Level Design (LLD) is the blueprint for a specific building. It shows where the electrical outlets are, the thickness of the drywall, and the plumbing layout. LLD dives into the **internal workings of a specific component or service**.

### The "Why" Behind LLD
HLD tells you *what* needs to be built, but it doesn't tell developers *how* to build it. Without LLD, five different developers might write code in five completely different, incompatible styles. LLD ensures that the codebase is maintainable, extensible, and robust.

### Core Components of LLD
1. **Class Diagrams:** Defining classes, attributes, methods, and relationships (Inheritance, Composition, Aggregation).
2. **Database Schema (Physical):** Exact SQL table definitions, data types, indexes, and foreign keys.
3. **Design Patterns:** Deciding to use a Factory Pattern for object creation or a Strategy Pattern for dynamic algorithms.
4. **Exception Handling:** Defining exactly how errors are caught and logged.

### Analogy: The Restaurant
- **HLD:** Deciding the restaurant needs a Kitchen, a Dining Area, a Drive-Thru, and a Point of Sale (POS) system. It defines that orders go from the Drive-Thru to the Kitchen via a ticket system (Message Queue).
- **LLD:** Defining the exact steps a chef takes to assemble a burger. It specifies the `BurgerBuilder` class, the `Grill` interface, and the `Cook(Patty p)` method.

## When to Switch from HLD to LLD

Knowing when to transition is an art. If you switch too early, you get bogged down in details before validating the system can scale. If you switch too late, your developers are blocked waiting for implementation details.

### The Trigger Points
1. **System Architecture is Finalized:** You have agreed on the major components (e.g., Client -> API Gateway -> Auth Service -> Order Service -> DB).
2. **APIs are Contractually Defined:** You know exactly what JSON the `Order Service` expects and returns.
3. **Data Model is Stable:** The core entities (User, Order, Product) are agreed upon.

Once these three pillars are set, you slice the system horizontally. The team assigned to the `Order Service` now begins the LLD for *just* their service.

| Phase | Focus | Audience | Artifacts |
|-------|-------|----------|-----------|
| **HLD** | System-wide view, scale, architecture | Stakeholders, Architects, Product Managers | Block diagrams, API contracts, Capacity estimates |
| **LLD** | Component-specific view, code structure | Developers, QA Engineers | Class diagrams, Sequence diagrams, DB schemas |

## API Contract vs Class Contract

This is a massive point of confusion. Both are contracts, but they operate at entirely different levels of abstraction.

### API Contract (HLD Level)
An API contract defines how two *different systems or microservices* communicate over a network (e.g., HTTP/REST).

**Example API Contract (Swagger/OpenAPI):**
```json
// POST /v1/payments
{
  "request": {
    "userId": "string",
    "amount": "number",
    "currency": "string"
  },
  "response": {
    "transactionId": "string",
    "status": "enum(SUCCESS, FAILED)"
  }
}
```
**Why it matters:** It allows the frontend team to build the UI while the backend team builds the payment processing logic, completely independently.

### Class Contract (LLD Level)
A Class Contract (or Interface) defines how two *objects* communicate within the *same memory space* (same codebase).

**Example Class Contract (Java):**
```java
public interface PaymentProcessor {
    /**
     * Processes a payment for a given user.
     * @param userId The ID of the user.
     * @param amount The amount to charge.
     * @throws PaymentDeclinedException if funds are insufficient.
     * @return The unique transaction ID.
     */
    String processPayment(String userId, double amount) throws PaymentDeclinedException;
}
```
**Why it matters:** It allows a developer to write a `StripePaymentProcessor` and a `PayPalPaymentProcessor` that can be swapped out seamlessly without breaking the rest of the application.

> [!WARNING]
> **Common Beginner Mistake:**
> Do not expose your Class Contracts directly as API Contracts! For instance, if your internal `User` class has a `hashedPassword` field, you must map it to a separate Data Transfer Object (DTO) before sending it over the API. Exposing internal class structures directly to the outside world is a massive security risk and coupling anti-pattern.
