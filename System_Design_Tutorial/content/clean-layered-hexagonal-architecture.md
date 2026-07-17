# Clean, Layered & Hexagonal Architecture

Welcome to the foundation of maintainable codebases. Whether you are building a monolith or a microservice, if the internal structure of your application is a tangled mess, your architecture will fail. High-level system design (drawing boxes on a whiteboard) is useless if the low-level code inside those boxes cannot be maintained or tested.

In this masterclass, we will explore how elite engineers structure their applications to be resilient to change, framework-agnostic, and deeply aligned with business requirements.

---

## 1. Hexagonal Architecture (Ports and Adapters)

### Hexagonal Architecture — business logic core, adapters at boundary

Proposed by Alistair Cockburn, Hexagonal Architecture (also known as Ports and Adapters) fundamentally shifts how we think about dependencies. In a traditional layered architecture, the UI depends on the Business Logic, which depends on the Database.

Hexagonal Architecture says: **The Business Logic is the center of the universe. It depends on nothing.**

#### The "Why": Why invert the dependencies?
If your business logic directly imports SQL drivers or HTTP libraries, testing it requires spinning up a database and a web server. If you want to swap MySQL for MongoDB, you have to rewrite your core logic.

In a Hexagon:
- **The Core:** Contains pure business rules. No HTTP, no SQL, no JSON.
- **Ports (Interfaces):** The core defines *Interfaces* for what it needs. E.g., `UserRepositoryInterface` with a `save()` method.
- **Adapters (Implementations):** Code living *outside* the hexagon implements these ports. You might have a `PostgresUserAdapter` or a `MongoUserAdapter`.
- **Driving vs. Driven:** The UI (REST API) "drives" the core via an inbound port. The core "drives" the database via an outbound port.

> **Analogy:** Think of the business core as a video game console. The console itself has "Ports" (controller slots, HDMI out). The console doesn't care if you plug in a Sony TV or an LG TV (Adapters), as long as the TV speaks the HDMI protocol. The game logic remains completely unchanged.

---

## 2. Clean Architecture

### Clean Architecture — entities → use cases → interface adapters → frameworks

Popularized by "Uncle Bob" Martin, Clean Architecture is conceptually very similar to Hexagonal Architecture but provides a more prescriptive set of concentric layers. The Golden Rule is the **Dependency Rule**: *Source code dependencies must point only inward, toward higher-level policies.*

#### The Layers:
1. **Entities (Enterprise Business Rules):** The absolute core. These are business objects (e.g., a `Loan` object with calculating interest logic) that could be used by many different applications in the company.
2. **Use Cases (Application Business Rules):** Specific application flows. E.g., "User applies for a Loan." It orchestrates the flow of data to and from the entities.
3. **Interface Adapters:** Converts data from the format most convenient for the use cases to the format most convenient for external agencies like the DB or Web. This is where Presenters, Controllers, and Gateways live.
4. **Frameworks & Drivers:** The outermost layer. Web frameworks (Spring, Express), Databases (Postgres), UI (React). You write very little code here.

| Layer | Example Code | Allowed to Import |
|-------|--------------|-------------------|
| **Entities** | `class User { name, age }` | Nothing |
| **Use Cases** | `RegisterUserUseCase` | Entities |
| **Interface Adapters**| `UserController` (REST API) | Use Cases, Entities |
| **Frameworks** | SQL Driver, Express.js Setup | Interface Adapters, Use Cases, Entities |

---

## 3. Domain-Driven Design (DDD)

### Domain-Driven Design (DDD) — ubiquitous language, bounded contexts, aggregates

When software fails, it is rarely because of a technical limitation. It usually fails because the developers misunderstood the business requirements. Domain-Driven Design (DDD), introduced by Eric Evans, bridges the gap between technical experts and domain experts.

#### Core Concepts:
- **Ubiquitous Language:** Developers and business stakeholders must use the exact same terminology. If the business calls it a "Client" and the database calls it a "User", you have failed. The code must reflect the business language perfectly.
- **Bounded Contexts:** The definition of a concept changes depending on the context. In an e-commerce app, the "Shipping" context views a "Product" purely by its weight and dimensions. The "Catalog" context views a "Product" by its marketing description and photos. Instead of one massive `Product` table, you split it into separate contexts (which perfectly maps to defining Microservice boundaries!).
- **Aggregates:** A cluster of domain objects that can be treated as a single unit. For example, an `Order` and its `OrderLineItems`. The `Order` is the Aggregate Root. You cannot modify a LineItem directly; you must go through the Order, ensuring all business invariants (like total cost limits) are enforced.

#### The "Why": Why is DDD so critical?
Without bounded contexts, applications devolve into a "Big Ball of Mud" where a single entity (like `User`) has 150 columns and every team in the company modifies it, leading to constant merge conflicts and logic bugs.

---

## 4. The 12-Factor App

### 12-Factor App — config in env, stateless processes, backing services

The 12-Factor methodology is a set of best practices for building modern, cloud-native applications (SaaS). Originally authored by engineers at Heroku, these principles ensure your app scales seamlessly and is easily deployable on any cloud.

#### Key Highlights from the 12 Factors:
- **III. Config:** Store configuration in the environment (`.env`), not in the code. Never commit API keys or database URLs to Git.
- **IV. Backing Services:** Treat databases, message queues, and caches as attached resources. Your app shouldn't care if the MySQL database is running locally or hosted on AWS RDS. It just connects via a URL.
- **VI. Processes:** Execute the app as one or more **stateless** processes. Any data that needs to persist must be stored in a stateful backing service (like a database).
- **VIII. Concurrency:** Scale out via the process model. Instead of making your application heavily multi-threaded internally to handle load, simply spin up 10 independent instances of your web process.

> **Analogy:** A 12-Factor app is like a standardized shipping container. It doesn't matter if the container is on a truck, a train, or a cargo ship (AWS, GCP, Heroku). The outside environment provides everything it needs, and it can be moved or duplicated instantly without changing its contents.

---

> [!TIP]
> **Teacher's FAQ & Common Beginner Mistakes**
>
> **Q: Should I use Clean Architecture for a simple CRUD app?**
> *Probably not.* If your app just takes JSON and writes it directly to a database without any complex business rules, Clean Architecture is overkill. You will write 5 layers of boilerplate just to save a string. Start simple (like MVC) and refactor to Clean Architecture when business rules get complex.
>
> **Q: Is DDD a technical framework?**
> No. DDD is a way of *thinking* and organizing your code to match the business. You can implement DDD in Java, Python, Go, or even a monolithic application. It is primarily an organizational and communication tool.
>
> **Q: Why does the 12-Factor App say processes must be stateless?**
> If your application stores user session data in its own RAM, and a load balancer routes the user to a different instance on their next click, they will be logged out. If the server crashes, data is lost. By keeping processes stateless and putting sessions in Redis (a backing service), you can kill or scale servers dynamically with zero user impact.
