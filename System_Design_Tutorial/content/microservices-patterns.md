# Microservices Patterns

Welcome to the deep dive into Microservices Patterns. When you break a monolith apart, you don't just magically get an easily scalable system. Instead, you trade one set of problems (codebase complexity) for another (distributed systems complexity).

To tame this new distributed beast, the industry has developed a robust set of architectural patterns. In this masterclass, we will explore exactly how the largest tech companies wire their microservices together.

---

## 1. API Gateway

### API Gateway — single entry, auth, rate limit, routing, aggregation

An API Gateway is a server that acts as an API front-end, receiving API requests, enforcing throttling and security policies, passing requests to the back-end service, and then passing the response back to the requester.

#### The "Why": Why do you need an API Gateway?
Imagine you have an e-commerce app with 15 different microservices (Cart, Inventory, User Profile, Shipping, etc.). If the mobile client had to talk to every service directly, it would be a disaster:
- The client would need to know 15 different IP addresses or hostnames.
- The client would make 15 separate HTTP calls to load a single dashboard, draining the user's battery and maximizing latency.
- Every single microservice would have to implement its own JWT authentication, rate limiting, and SSL termination.

**The Solution:** You place an API Gateway (like Kong, AWS API Gateway, or NGINX) in front.
- **Routing:** It maps `/users` to the User Service and `/cart` to the Cart Service.
- **Cross-Cutting Concerns:** It handles SSL termination, Authentication (verifying the JWT), and Rate Limiting centrally.
- **Aggregation:** It can take one request from the client, fetch data from 3 services internally, combine the JSON, and return a single response to the client.

> **Analogy:** Think of the API Gateway as the receptionist at a massive corporate skyscraper. Instead of visitors wandering the halls trying to find the accounting department, they talk to the receptionist. The receptionist checks their ID (Authentication), ensures they aren't visiting too often (Rate Limiting), and tells them exactly which elevator to take (Routing).

---

## 2. Backends for Frontends (BFF)

### Backends for Frontends (BFF) — separate API gateway per client type

The BFF pattern is an evolution of the API Gateway pattern. Instead of having one massive, monolithic API Gateway that serves Web, iOS, Android, and 3rd-party developers, you build a separate, smaller API Gateway for each specific client interface.

#### The "Why": Why separate the gateways?
A web browser on a high-speed fiber connection has very different needs than an Android app on a spotty 3G network.
- The web app might want a massive JSON payload with 100 fields to render a complex dashboard.
- The mobile app only needs 5 fields and needs them optimized for low bandwidth.

If you use a single API Gateway, it becomes a bottleneck where the mobile team and the web team are constantly stepping on each other's toes to update the routing logic. By using BFFs, the iOS team owns the iOS BFF, and the Web team owns the Web BFF.

---

## 3. Service Discovery

### Service discovery — client-side (Eureka) vs server-side (Consul, K8s DNS)

In a microservices world, services are constantly spinning up and dying. IP addresses change dynamically as auto-scaling groups react to traffic. How does the Cart Service know the IP address of the currently healthy Inventory Service?

#### The "Why": Hardcoded IPs are dead
You cannot hardcode `192.168.1.15` because that server might be destroyed by AWS in 5 minutes. You need a dynamic registry.

**Client-Side Discovery (e.g., Netflix Eureka):**
1. The client (e.g., Cart Service) queries the Service Registry (Eureka) for "Inventory Service".
2. Eureka returns a list of healthy IP addresses.
3. The client applies its own load balancing (like Ribbon) to pick an IP and makes the call.

**Server-Side Discovery (e.g., Kubernetes DNS, AWS ALB):**
1. The client just makes a call to a static hostname like `http://inventory-service`.
2. A centralized load balancer or proxy intercepts the request.
3. The load balancer queries the registry, picks a healthy IP, and forwards the traffic.

| Pattern | Pros | Cons |
|---------|------|------|
| **Client-Side** | No extra network hop; very fast. | Client must implement load balancing logic (hard for polyglot systems). |
| **Server-Side** | Client is dumb and simple. Works across any language. | Extra network hop (client -> load balancer -> service). |

---

## 4. Service Mesh and Sidecar Pattern

### Sidecar pattern — helper container alongside main app for cross-cutting concerns

A Sidecar is a secondary container that runs right next to your primary application container in the same pod (in Kubernetes terms). It shares the same network lifecycle.

#### The "Why": Offloading operational logic
If your team writes a service in Go, and another writes one in Node.js, you don't want to write complex retry logic, circuit breaking, and metrics export libraries in both languages. You write your business logic in your main container, and attach a Sidecar (often a proxy like Envoy) to handle all network communication.

### Service mesh (Istio, Linkerd) — sidecar proxies handle mTLS, retries, LB

When you deploy a Sidecar proxy to *every single microservice* in your cluster, and centrally manage them, you have created a **Service Mesh**.

A Service Mesh intercepts all incoming and outgoing network traffic for every service.
- **mTLS:** It automatically encrypts traffic between services, zero-trust style.
- **Retries & Circuit Breaking:** It intercepts a failing HTTP call and retries it automatically without your application code knowing.
- **Observability:** It logs exactly how long the network hop took.

> **Analogy:** Imagine your microservice is a CEO. The CEO just wants to write letters (business logic). The Sidecar is the CEO's executive assistant. The CEO hands the letter to the assistant. The assistant handles putting it in an envelope, adding a stamp, encrypting it, mailing it, and resending it if it gets lost. A Service Mesh is an entire corporation where every CEO has an identical, highly-trained assistant.

---

## 5. Database-per-Service

### Database-per-service — each service owns its schema, no shared DBs

This is the golden rule of microservices: **Services must not share a database.**

#### The "Why": Why can't we just share the DB?
If the Order Service and the User Service both read and write directly to the `Users` table in a shared Postgres database:
1. **Coupling:** If the User team changes a column name, the Order team's service crashes in production.
2. **Scaling:** The single database becomes a massive scaling bottleneck.

Instead, the User Service has its own database, and the Order Service has its own database. If the Order Service needs user data, it must make an API call to the User Service. This ensures strict encapsulation.

---

## 6. The Strangler Fig Pattern

### Strangler Fig — incrementally replace monolith by routing slices to new services

How do you move from a massive legacy monolith to microservices without stopping all product development for a two-year rewrite? You use the Strangler Fig pattern.

#### The "Why": Mitigating risk
A "Big Bang" rewrite (shutting down the old app and turning on the new one) almost always fails. Instead, you put an API Gateway in front of your legacy monolith.
1. Day 1: 100% of traffic routes to the Monolith.
2. Day 10: You build a shiny new Payment Microservice. You tell the API Gateway: "Route `/payments` to the new service. Route everything else to the monolith."
3. Over time, you build more microservices, slowly routing more endpoints away from the monolith.
4. Eventually, the monolith receives zero traffic and can be safely deleted.

> **Analogy:** In nature, a strangler fig vine grows around a massive, old tree. Slowly, it wraps around the tree, stealing its sunlight and nutrients, growing its own structure. Eventually, the old tree dies and rots away, leaving only the complex structure of the strangler fig.

---

> [!WARNING]
> **Teacher's FAQ & Common Beginner Mistakes**
>
> **Q: With Database-per-Service, how do I do JOINs across tables?**
> *You don't.* You cannot do a SQL JOIN across two different databases. This is the hardest part of microservices. You must either aggregate the data in memory (via an API Gateway or BFF), or you must replicate the necessary data asynchronously using event streams (like Kafka) so a service has a local read-only copy of the data it needs.
>
> **Q: Should I use an API Gateway AND a Service Mesh?**
> Yes, they serve different purposes. The API Gateway handles **North-South traffic** (traffic entering your cluster from the outside world). A Service Mesh handles **East-West traffic** (internal traffic between your microservices inside the cluster).
>
> **Q: Does a Service Mesh eliminate the need for an API Gateway?**
> No. While some service meshes offer ingress gateways, a dedicated API Gateway is usually better suited for complex business-centric routing, OAuth integrations, and developer portals for external clients.
