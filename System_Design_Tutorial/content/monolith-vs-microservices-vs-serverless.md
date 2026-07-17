# Monolith vs Microservices vs Serverless

Welcome to one of the most debated and critical decisions in modern system design: choosing your architectural style. The path you choose here determines not just how your code runs, but how your engineering organization scales. If there is one thing you must remember from this masterclass, it is this: **Architecture is about trade-offs, and you are trading development speed for organizational scalability.**

Let's break down the evolution of service architecture, step-by-step, starting from the humble monolith.

---

## 1. Monolithic Architecture

### Monolithic — single deployable, fast initial dev, painful at 50+ engineers

A monolithic architecture means all your business logic, UI, data access, and background jobs are compiled and deployed as a single, cohesive unit. Whether it's a giant `.jar` file in Java, a massive Node.js Express server, or a Ruby on Rails application, everything lives together.

#### The "Why": Why start with a monolith?
When you are a startup with 3 engineers trying to find product-market fit, you do not need distributed systems. You need velocity. A monolith allows you to:
- Pass data in memory (sub-millisecond latency) instead of over the network.
- Have a single CI/CD pipeline.
- Maintain transactional integrity easily using a single database.
- Debug locally by just starting one process.

**The Breaking Point:**
As your company grows to 50+ engineers, the monolith becomes a nightmare.
- **Merge Conflicts:** Everyone is modifying the same codebase.
- **Deployment Fear:** Changing the billing logic might accidentally break the user login.
- **Scaling Inefficiency:** If your image processing module needs high CPU, you have to scale the *entire* monolith, even the parts that just serve static HTML.

> **Analogy:** Think of a monolith as a food truck. The chef, the cashier, and the prep cook are all in one tight space. Communication is instant. It's cheap and efficient to start. But if you try to put 50 chefs in that same food truck, nobody can move, and someone is getting burned.

---

## 2. The Middle Ground: Modular Monolith

### Modular monolith — strong internal boundaries, best of both worlds

Before leaping to microservices, many elite engineering teams (like Shopify and Stack Overflow) opt for a **Modular Monolith**.

A modular monolith is still deployed as a single application, but internally, the code is strictly separated into independent modules or domains (e.g., Billing, Inventory, Users) with strict interfaces. Module A cannot directly read Module B's database tables or call its internal functions; it must go through a well-defined public interface.

#### The "Why": Why modularize?
You get the benefits of a single deployable unit and easy local development, while preventing the codebase from becoming a "Big Ball of Mud." If you enforce strict boundaries today, extracting a module into a microservice tomorrow (if needed) becomes trivial.

| Feature | Monolith (Spaghetti) | Modular Monolith | Microservices |
|---------|----------------------|------------------|---------------|
| **Deployment** | Single | Single | Multiple |
| **Boundaries** | Weak / Non-existent | Strong (Enforced by code) | Strong (Enforced by network) |
| **Refactoring** | Painful | Moderate | Difficult (Distributed) |
| **Local Dev** | Trivial | Trivial | Complex |

---

## 3. Microservices

### Microservices — team autonomy, polyglot, independent deploy, complex operationally

Microservices architecture divides your application into a suite of small, independently deployable services, usually organized around business capabilities. Each service runs in its own process and communicates with others via lightweight mechanisms, typically HTTP/REST or gRPC.

#### The "Why": Why adopt microservices?
You adopt microservices when your organization is too large to fit in a single codebase. It is an **organizational scaling tool**, not necessarily a technical one.

- **Team Autonomy:** The Payments team can deploy 10 times a day without waiting for the Search team to finish their release.
- **Polyglot Persistence & Programming:** The AI team can use Python, while the high-throughput streaming team uses Go.
- **Independent Scaling:** You only scale the services that need it.

#### The Hidden Costs of Microservices
Do not let the hype fool you. Moving to microservices introduces immense operational complexity.
- **Network Latency:** What used to be a 1ms in-memory function call is now a 50ms network hop, susceptible to packet loss and network partitions.
- **Data Consistency:** You can no longer use simple ACID SQL transactions across services. You must rely on eventual consistency and complex patterns like the Saga pattern.
- **Debugging:** Tracing a request that fails after hopping through 7 different microservices requires distributed tracing (e.g., Jaeger, Zipkin).

> **Analogy:** Microservices are like an entire city of specialized restaurants instead of one food truck. You have a bakery, a butcher, and a produce market. They can all scale independently and hire specialized workers. But to cook a meal, you now need delivery trucks (the network) driving between them, coordinating logistics.

---

## 4. Serverless (Lambda/Functions)

### Serverless (Lambda/Functions) — event-triggered, no servers, pay-per-invocation

Serverless computing (like AWS Lambda, Google Cloud Functions) allows you to build and run applications without thinking about servers. You write a function, upload it, and the cloud provider handles the provisioning, scaling, and execution. You are billed purely on the milliseconds your code runs.

#### The "Why": When do you use Serverless?
- **Highly variable workloads:** If you have an image resizing service that gets 0 traffic at night but 10,000 requests per second during a super bowl ad, Serverless scales instantly from zero to thousands, and you don't pay for idle time.
- **Event-driven glues:** Triggering a function every time a file is uploaded to S3 or a message hits a queue.

#### Trade-offs:
- **Cold Starts:** If a function hasn't been invoked recently, the cloud provider must spin up a new container. This can add 500ms to 2 seconds of latency to the first request.
- **Vendor Lock-in:** You are deeply tying your architecture to AWS, GCP, or Azure's proprietary events and ecosystem.

---

## 5. SOA vs. Nanoservices

### SOA (Service-Oriented Architecture) — coarser than microservices, centralized ESB

Service-Oriented Architecture (SOA) was the precursor to microservices in the early 2000s.
- **The difference:** SOA services are usually massive (coarse-grained) and rely heavily on a centralized "Enterprise Service Bus" (ESB) for routing, transformation, and business logic orchestration.
- **Why it failed:** The ESB became a massive bottleneck and a single point of failure. Microservices favor "smart endpoints and dumb pipes" (e.g., simple HTTP routers or message brokers like Kafka) rather than putting logic in the pipes.

### Nanoservices antipattern — too fine-grained, network overhead dominates

If microservices are good, are tiny functions even better? No. A nanoservice is an antipattern where a service is so small (e.g., a service just for adding two numbers) that the overhead of network communication heavily outweighs the actual work being done.
If your services spend 90% of their time serializing JSON and waiting on network calls, you have built nanoservices. Group related operations together into properly sized microservices.

---

> [!NOTE]
> **Teacher's FAQ & Common Beginner Mistakes**
>
> **Q: Should I start my new project with Microservices to be "future-proof"?**
> *Absolutely not.* This is the #1 mistake junior engineers make. Start with a Modular Monolith. If you build microservices from day one, you are solving problems you don't have (team scaling) and paying costs you can't afford (operational complexity).
>
> **Q: What is the defining characteristic of a microservice?**
> Independent deployability. If you have to deploy Service A and Service B together because they depend on each other, you do not have microservices. You have a **distributed monolith**, which is the worst of both worlds.
>
> **Q: Are Serverless and Microservices mutually exclusive?**
> No! You can build microservices using serverless functions. "Microservice" describes the boundary of a domain, while "Serverless" describes the compute infrastructure.
