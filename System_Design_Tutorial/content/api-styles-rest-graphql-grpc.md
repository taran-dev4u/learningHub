# API Styles: REST, GraphQL & gRPC

## Overview
How do microservices talk to each other? How does a mobile app ask the backend for data? The answer is an API (Application Programming Interface).

But not all APIs are created equal. Depending on whether you are building a public-facing developer platform, a heavily constrained mobile app, or lightning-fast internal microservices, you must choose the right architectural style. This masterclass covers the Big Three: REST, GraphQL, and gRPC.

---

## REST — stateless, resources + HTTP verbs, cacheable, uniform interface

**REST (Representational State Transfer)** is the undisputed king of web APIs. If you don't know what to build, build a REST API.

- **How it works:** It treats everything as a "Resource" (e.g., Users, Orders) identified by a URL (`/users/123`). You manipulate these resources using standard HTTP verbs (GET, POST, PUT, DELETE).
- **Stateless:** The server stores no session data about the client. Every request must contain all the information necessary to understand it (like an Auth Token).
- **Cacheable:** Because GET requests are standardized, CDNs and browsers can easily cache REST responses, making it highly scalable for read-heavy systems.

**The Trade-off:** "Over-fetching" and "Under-fetching." If a mobile app needs a user's name and their last 5 order IDs, it might have to hit `/users/123` (getting back 50 fields it doesn't need) and then make 5 separate calls to `/orders/{id}`.

---

## GraphQL — single endpoint, client picks fields, no over/under-fetching

Created by Facebook to solve the exact problems REST has with mobile data usage.

- **How it works:** Instead of hitting different URLs, the client sends a query to a *single endpoint* (`/graphql`). The query explicitly states exactly what fields it wants.
- **Example Query:** `query { user(id: 123) { name, orders(last: 5) { id } } }`
- **The Benefit:** No over-fetching (saving mobile data) and no under-fetching (saving network round-trips). The client gets exactly what it asked for in a single JSON response.

> [!WARNING]
> **Teacher's FAQ:** Why doesn't everyone just use GraphQL?
> **Answer:** It pushes extreme complexity to the backend! If a client can ask for any nested data, they can accidentally (or maliciously) write a query that joins 10 huge database tables and crashes your server. You must implement strict query complexity limits. Furthermore, because every request is a POST to `/graphql`, you cannot use standard HTTP caching via CDNs.

---

## gRPC — HTTP/2 + Protobuf, bidirectional streaming, ideal for internal microservices

Created by Google, gRPC is designed for raw speed and efficiency, not human readability.

- **How it works:** Instead of sending JSON strings over HTTP/1.1, gRPC sends highly compressed binary data (Protocol Buffers) over HTTP/2.
- **The Speed:** Because the data is binary and strongly typed, the server does not need to parse strings or figure out data types. It is magnitudes faster than REST/JSON.
- **Bidirectional Streaming:** Thanks to HTTP/2, the client and server can leave the connection open and continuously stream messages back and forth.
- **Use Case:** Internal microservice-to-microservice communication.

> [!NOTE]
> **Analogy:** REST/JSON is like writing a letter in English; anyone can read it, but it's wordy. gRPC/Protobuf is like sending Morse Code; it's incredibly fast and efficient, but you need a decoder ring (the `.proto` schema file) to understand it.

---

## API Gateway — auth, rate limiting, routing, transformation at ingress

When you have 50 different microservices, you do not want your mobile app trying to memorize 50 different IP addresses. You put an **API Gateway** in front of them all.

**Core Responsibilities:**
1. **Routing:** `GET /users` goes to the User Service. `POST /payments` goes to the Payment Service.
2. **Authentication:** The gateway validates the JWT token. If it's invalid, it rejects the request before it ever touches a microservice, saving internal CPU.
3. **Rate Limiting:** Drops requests if a user is spamming the API.
4. **Protocol Translation:** A client might send a REST/JSON request to the gateway, and the gateway translates it into a blazing fast gRPC call to the internal backend.

---

## Idempotency keys — safe retries, critical for payments and mutations

As mentioned in the HTTP module, network connections drop. If a mobile app sends a POST to `/charge-credit-card` and the connection drops before it gets a 200 OK, what should it do? If it retries, it might charge the user twice!

**The Solution:**
The client generates a unique UUID (e.g., `Idempotency-Key: 12345`) and sends it in the HTTP header.
1. The server receives the request, checks its database: "Have I seen key 12345 before?"
2. No? Process the payment, save the result in the DB linked to `12345`, and return 200 OK.
3. If the connection drops and the client retries with `12345`, the server sees it in the DB, skips processing the payment, and just returns the previously saved 200 OK.

---

## Webhooks — server pushes to registered callback URL on event

Polling an API to see if a long-running task is done is incredibly wasteful.

- **Polling (Bad):** Client asks "Is the video done rendering?" every 5 seconds for 10 minutes. 99% of requests return "No."
- **Webhooks (Good):** The client gives the server a URL (`https://client.com/webhook`). The client goes to sleep. When the video finishes rendering, the *server* makes an HTTP POST request to the client's URL with the payload.

**Analogy:** Polling is like a kid in the backseat asking "Are we there yet?" every 5 minutes. Webhooks are the parent saying "Go to sleep, I'll wake you up when we get there."
