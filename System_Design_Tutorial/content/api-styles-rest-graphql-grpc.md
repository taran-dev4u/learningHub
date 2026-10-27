# API Styles: REST, GraphQL & gRPC

Welcome to the definitive masterclass on modern API architectures. In production distributed systems, communication protocols are not merely cosmetic implementation details—they dictate your latency envelopes, CPU consumption, bandwidth costs, caching strategies, and how teams decouple frontend clients from backend microservices.

An API (Application Programming Interface) is the contract between a consumer and a provider. Depending on whether your consumer is a low-power mobile device over a 3G cellular network, a public third-party developer, or an internal microservice executing thousands of remote procedure calls per second, choosing the wrong communication paradigm will degrade performance and developer velocity.

In this deep dive, we break down the engineering mechanics, protocol-level serialization formats, network transport layers, and architectural trade-offs of the Big Three: **REST**, **GraphQL**, and **gRPC**, followed by critical edge ingress patterns: **API Gateways**, **Idempotency Keys**, and **Webhooks**.

---

## REST — stateless, resources + HTTP verbs, cacheable, uniform interface

### 1. Architectural Principles of REST
Formulated in 2000 by Roy Fielding in his doctoral dissertation, **REST (Representational State Transfer)** is not a strict protocol or standard; it is an architectural style designed to leverage the existing strengths of the World Wide Web and HTTP (Hypertext Transfer Protocol).

True RESTful systems satisfy six fundamental architectural constraints:
1. **Client-Server Separation:** The user interface concerns are separated from the data storage concerns. The client doesn't care about database schemas; the server doesn't care about UI state.
2. **Statelessness:** Every request from client to server must contain *all* the context necessary to understand and process it (authentication tokens, query parameters, payload). The server never stores client session state between requests.
3. **Cacheability:** Responses must implicitly or explicitly define themselves as cacheable or non-cacheable to prevent clients from fetching stale data while eliminating redundant server round-trips.
4. **Uniform Interface:** The cornerstone of REST. Resources are identified by stable URIs (`/orders/9812`), manipulated through representations (usually JSON or XML), accompanied by self-descriptive messages (HTTP headers and status codes), and navigate through hypermedia (HATEOAS).
5. **Layered System:** A client cannot tell whether it is connected directly to the end server or to an intermediary (CDN, reverse proxy, load balancer).
6. **Code on Demand (Optional):** Servers can temporarily extend client functionality by transferring executable code (e.g., JavaScript).

### 2. HTTP Verbs, Semantics & Idempotency
A major interview failure mode is misunderstanding the semantics and safety/idempotency guarantees of standard HTTP verbs:

| HTTP Verb | CRUD Mapping | Safe? (Read-Only) | Idempotent? | Typical Status Codes | Description |
|---|---|---|---|---|---|
| **GET** | Read | **Yes** | **Yes** | `200 OK`, `304 Not Modified`, `404 Not Found` | Retrieves a resource representation. Must have no server-side side effects. |
| **POST** | Create / Action | **No** | **No** | `201 Created`, `200 OK`, `202 Accepted` | Submits data to create a subordinate resource or execute a non-idempotent operation. |
| **PUT** | Replace / Upsert | **No** | **Yes** | `200 OK`, `204 No Content`, `201 Created` | Completely replaces the target resource at the given URI with the request payload. |
| **PATCH** | Partial Update | **No** | **Conditional** | `200 OK`, `204 No Content` | Applies a delta or partial modification to a resource. |
| **DELETE** | Delete | **No** | **Yes** | `200 OK`, `204 No Content`, `404 Not Found` | Deletes the specified resource. Repeating DELETE yields the same server state. |
| **OPTIONS** | Pre-flight | **Yes** | **Yes** | `204 No Content`, `200 OK` | CORS preflight check; queries the communication options supported by the server. |

> [!NOTE]
> **Safety vs Idempotency:**
> - **Safe:** An operation that does not alter server state. `GET /users/42` is safe.
> - **Idempotent:** Calling the operation $N$ times produces the exact same server state as calling it once ($f(f(x)) = f(x)$). `DELETE /users/42` is idempotent because once deleted, subsequent deletes leave the user deleted. `POST /payments` is **not** idempotent because executing it twice charges the card twice!

### 3. The Over-Fetching and Under-Fetching Dilemma
While REST is the lingua franca of public APIs due to its simplicity and browser compatibility, modern client applications suffer from two fundamental network inefficiencies:

```
[REST Client: Mobile App]
       |
       +--- GET /users/42 ---------> [Returns 60 fields: address, SSN, preferences, stats...]
       |                             (Over-fetching: mobile app only needed 'name' and 'avatar_url')
       |
       +--- GET /users/42/orders ---> [Returns order IDs: 101, 102, 103...]
       |
       +--- GET /orders/101 -------> [Fetch details of order 101]
       +--- GET /orders/102 -------> [Fetch details of order 102]
       +--- GET /orders/103 -------> [Fetch details of order 103]
                                     (Under-fetching & N+1 Calls: 5 round-trips over cellular network!)
```

- **Over-fetching:** The endpoint returns more data than the client needs. A mobile app rendering an avatar might receive a 15 KB user JSON object containing billing history and audit logs. Bandwidth and battery are wasted parsing unused JSON.
- **Under-fetching (The N+1 Round-Trip Problem):** A single endpoint does not provide sufficient data to render a single UI view. The client must make cascading waterfall HTTP requests to assemble the view, introducing noticeable UI latency.

---

## GraphQL — single endpoint, client picks fields, no over/under-fetching

### 1. The Architecture of Declarative Data Fetching
Developed internally by Facebook in 2012 and open-sourced in 2015, **GraphQL** fundamentally inverts the client-server power dynamic. Instead of the server deciding the shape of the response, the **client declares exactly what data it needs**, down to individual fields.

- **Single Ingress Endpoint:** The client sends all queries and mutations as HTTP `POST` requests to a single URL (conventionally `/graphql`).
- **Strongly Typed Schema Definition Language (SDL):** The server publishes a contract defining available types, queries, and mutations.
- **Hierarchical Tree Traversal:** A GraphQL query mirrors the shape of the resulting JSON response.

```graphql
# Example GraphQL Query: Client fetches user and last 2 order summaries in 1 round trip
query GetUserDashboard($userId: ID!) {
  user(id: $userId) {
    id
    name
    avatarUrl
    orders(limit: 2) {
      id
      totalAmount
      status
      items {
        productName
        quantity
      }
    }
  }
}
```

The server returns:
```json
{
  "data": {
    "user": {
      "id": "42",
      "name": "Taran",
      "avatarUrl": "https://cdn.site.com/avatars/42.png",
      "orders": [
        {
          "id": "101",
          "totalAmount": 49.99,
          "status": "DELIVERED",
          "items": [{ "productName": "Ergonomic Keyboard", "quantity": 1 }]
        }
      ]
    }
  }
}
```

### 2. Solving the N+1 Database Query Problem with DataLoader
While GraphQL eliminates network round-trips between the client and API gateway, a naive GraphQL server creates an catastrophic **N+1 Database Query Problem** on the backend!

If each GraphQL field has its own resolver function:
- `user` resolver runs: `SELECT * FROM users WHERE id = 42;` (1 query)
- `orders` resolver returns 10 orders.
- For each order, the `items` resolver executes independently:
  - `SELECT * FROM items WHERE order_id = 1;`
  - `SELECT * FROM items WHERE order_id = 2;`
  - ... (10 separate queries!)

**The Solution: DataLoader Pattern:**
A DataLoader batches and caches lookups within a single execution tick of the event loop. Instead of firing 10 individual SQL queries, it aggregates the 10 order IDs and issues a single batch query:
$$	ext{SELECT * FROM items WHERE order_id IN (1, 2, 3, 4, 5, 6, 7, 8, 9, 10);}$$

### 3. Production Trade-offs & Vulnerabilities of GraphQL
Interviewers love asking why high-scale systems do not blindly replace all REST endpoints with GraphQL:

1. **Denial of Service via Nested Query Bombs:**
   Because clients formulate queries dynamically, an attacker can craft recursive, deeply nested queries:
   ```graphql
   query EvilQuery {
     author {
       books {
         author {
           books {
             author {
               books { id }
             }
           }
         }
       }
     }
   }
   ```
   *Mitigation:* Production servers must enforce **Query Depth Limiting** (e.g., max depth of 5) and **Query Cost Analysis** (assigning points to fields and rejecting queries exceeding 1000 points).
2. **Breakdown of HTTP & CDN Caching:**
   In REST, a `GET /products/101` has a unique URI that Akamai, Cloudflare, or Varnish can cache at the edge with `Cache-Control: public, max-age=3600`. In GraphQL, every request is a `POST /graphql` with a unique JSON body. CDNs cannot cache POST requests out of the box. You must implement persisted queries (hashing queries into unique IDs) or client-side normalized caches (Apollo Client / Relay).

---

## gRPC — HTTP/2 + Protobuf, bidirectional streaming, ideal for internal microservices

### 1. Protocol Buffers (Protobuf) Wire Format Mechanics
Created by Google, **gRPC (Remote Procedure Call)** is engineered for maximum throughput, minimal serialization latency, and bulletproof type safety across internal microservices.

Instead of human-readable text formats like JSON or XML, gRPC serializes structured data into **Protocol Buffers (Protobuf)**—a compact binary format.

```protobuf
syntax = "proto3";

package payment;

service PaymentService {
  // Unary RPC: Single request, single response
  rpc ProcessPayment (PaymentRequest) returns (PaymentResponse);
  
  // Server-streaming RPC: Single request, stream of updates
  rpc StreamTransactions (TransactionQuery) returns (stream Transaction);
  
  // Bidirectional streaming RPC: Full duplex simultaneous communication
  rpc RealtimeExchange (stream MarketOrder) returns (stream OrderStatus);
}

message PaymentRequest {
  string user_id = 1;
  int64 amount_cents = 2;
  string currency = 3;
}

message PaymentResponse {
  string transaction_id = 1;
  bool success = 2;
  int64 timestamp = 3;
}
```

#### Why is Protobuf 5x to 10x Faster than JSON?
1. **Field Numbers Instead of Field Names:** In JSON, every single payload transmits the field names repeatedly: `{"transaction_id": "tx_99", "amount_cents": 5000}`. Field names consume the vast majority of bytes. In Protobuf, the schema assigns each field an integer tag (`1`, `2`, `3`). Only the numeric tag and the binary value are transmitted over the wire!
2. **Varints (Variable-Length Integers):** Small integers don't take 32 or 64 bits. Integers are encoded using 7 bits per byte with the Most Significant Bit (MSB) indicating continuation. The number `1` takes a single byte instead of 4 or 8 bytes.
3. **Zero String Parsing:** In JSON, a CPU must scan strings byte by byte, parse quotation marks, escape slashes, convert string numbers `"5000"` to CPU registers, and allocate heap memory. Protobuf is decoded directly into typed memory structures with near-zero CPU overhead.

### 2. HTTP/2 Transport Multiplexing
gRPC relies strictly on **HTTP/2** as its underlying transport layer. Unlike HTTP/1.1 (which suffers from Head-of-Line blocking and requires opening multiple TCP connections), HTTP/2 introduces:
- **Binary Framing Layer:** Every request and response is broken down into small binary frames (HEADERS frame, DATA frame).
- **Stream Multiplexing over a Single TCP Connection:** Hundreds of independent RPC calls can fly concurrently over a single shared TCP socket without blocking each other.
- **HPACK Header Compression:** Common headers are compressed using static and dynamic Huffman tables.

```
HTTP/1.1 (Sequential / Connection Pool needed):
[Client] === Request 1 ===> [Server]
[Client] <== Response 1 == [Server]
[Client] === Request 2 ===> [Server]  (Blocked waiting for Request 1!)

HTTP/2 Multiplexing (Single TCP Connection):
[Client] === Stream 1 (Frame A) === Stream 2 (Frame A) === Stream 1 (Frame B) ===> [Server]
[Client] <== Stream 2 (Frame B) === Stream 1 (Frame C) <========================== [Server]
```

### 3. Comprehensive Architecture Comparison Matrix

| Architectural Feature | REST | GraphQL | gRPC |
|---|---|---|---|
| **Underlying Transport** | HTTP/1.1 or HTTP/2 | HTTP/1.1 or HTTP/2 | Strictly HTTP/2 |
| **Payload Serialization** | JSON, XML (Text-based) | JSON (Text-based) | Protocol Buffers (Binary) |
| **Contract / Typing** | OpenAPI / Swagger (Optional) | GraphQL Schema (Mandatory) | `.proto` Definitions (Mandatory) |
| **Network Overhead** | Moderate to Heavy (JSON strings) | Medium (Exact fields, but JSON) | **Ultra-Low (Binary tags + Varints)** |
| **CPU Serialization Cost** | High (String parsing & allocations) | High (Dynamic query execution) | **Ultra-Low (Direct binary decoding)** |
| **Streaming Capabilities** | Server-Sent Events (SSE) / Chunked | Subscriptions (via WebSockets) | **Native Unary, Client, Server, Bi-di** |
| **Edge CDN Caching** | **First-class (GET URLs + headers)** | Complex (POST queries break CDNs) | Not designed for edge CDN caching |
| **Browser Support** | Universal (All browsers) | Universal (Standard HTTP POST) | Requires gRPC-Web proxy (Envoy) |
| **Best Production Use Case** | Public developer APIs, CRUD apps | Mobile apps, diverse UI clients | **Inter-service microservice backbones** |

---

## API Gateway — auth, rate limiting, routing, transformation at ingress

### 1. Ingress Architecture in Distributed Systems
When an enterprise scales from a monolith to 50+ microservices, exposing individual service IPs to external clients is an architectural disaster:
- Clients must know internal topology, IPs, and port configurations.
- Authentication, SSL termination, and rate-limiting logic must be duplicated across every microservice.
- A change to an internal service breaks client mobile apps in the wild.

An **API Gateway** acts as the single reverse proxy ingress point that intercepts all external traffic and delegates it to internal services.

```
[Mobile Client]   [Web Browser]   [Third-Party Partner]
       \                |                /
        \               |               /
         v              v              v
   +-------------------------------------------+
   |             API GATEWAY                   |
   | - SSL / TLS Termination                   |
   | - JWT Validation & Authentication         |
   | - Token Bucket Distributed Rate Limiting  |
   | - Request Routing & Load Balancing       |
   | - Protocol Translation (JSON -> gRPC)     |
   | - Distributed Tracing & Metric Injection  |
   +-------------------------------------------+
         /              |                      /               |                      v (gRPC)         v (gRPC)         v (gRPC)
  [User Service] [Order Service] [Payment Service]
```

### 2. Core Operational Responsibilities
1. **SSL/TLS Termination:** Offloads cryptographic handshake overhead from internal services. Public clients speak HTTPS; internal VPC microservices can communicate over high-speed mutual TLS (mTLS) or private networks.
2. **Centralized Authentication & Authorization:** Validates JSON Web Tokens (JWT) or API Keys once at the boundary. Decoded claims (e.g., `X-User-ID: 42`, `X-User-Roles: admin`) are injected as downstream headers.
3. **Distributed Rate Limiting:** Enforces quotas using Token Bucket or Leaky Bucket algorithms backed by distributed Redis clusters. Protects downstream databases from thundering herds.
4. **Protocol Translation:** The gateway can accept standard public REST/JSON requests from mobile clients and seamlessly translate them into internal high-speed gRPC binary calls to the respective backend microservices.
5. **Circuit Breaking & Fault Tolerance:** If the Recommendation Service is failing, the gateway can return a cached fallback response instead of failing the entire landing page.

---

## Idempotency keys — safe retries, critical for payments and mutations

### 1. The Distributed Network Failure Problem
In a distributed network, failure is inevitable. When a client sends a mutation request (e.g., `POST /payments`), three distinct outcomes can occur:
1. The request fails before reaching the server (Client error).
2. The server crashes while processing the request (Server error).
3. The server **successfully processes the payment**, but the network connection drops *before* the `200 OK` response reaches the client!

In scenario 3, the client experiences a network timeout. If the client or user naively retries the payment, the user will be double-charged!

### 2. The Idempotency Key Architecture
To make non-idempotent operations safe to retry, the client generates a cryptographically unique identifier (UUIDv4) and includes it in the HTTP request header:
$$	ext{Idempotency-Key: 9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d}$$

```
[Client]                              [Payment Gateway]                           [Redis Cache / SQL DB]
   |                                          |                                              |
   |--- POST /payments (Key: UUID-1) -------->|                                              |
   |                                          |--- SETNX idempotency:UUID-1 "IN_PROGRESS" -->|
   |                                          |<-- Success (Lock acquired) ------------------|
   |                                          |                                              |
   |                                          |=== [Process Payment via Stripe API] =======|
   |                                          |                                              |
   |                                          |--- UPDATE idempotency:UUID-1 "COMPLETED" --->|
   |                                          |--- SAVE Cached Response (HTTP 200, JSON) --->|
   |<-- Network Drops! (Client gets Timeout) -x                                              |
   |                                                                                         |
   |=== [Client Retries Request with same Idempotency-Key: UUID-1] ==========================|
   |                                                                                         |
   |--- POST /payments (Key: UUID-1) -------->|                                              |
   |                                          |--- GET idempotency:UUID-1 ------------------>|
   |                                          |<-- Returns "COMPLETED" + Cached Response ----|
   |                                          |    (Skips payment processing completely!)    |
   |<-- Returns Cached HTTP 200 OK -----------|                                              |
```

### 3. Implementation State Machine
1. **Acquire Distributed Lock (Atomic `SETNX`):** The server attempts to store the key with status `IN_PROGRESS` and an expiration TTL (e.g., 120 seconds).
   - If the key already exists with status `IN_PROGRESS`: A duplicate concurrent request is running. Return `409 Conflict` or wait.
   - If the key already exists with status `COMPLETED`: Retrieve the stored response payload and return it immediately without re-executing business logic.
2. **Execute Transaction:** Execute the business operation inside a database transaction.
3. **Persist Result:** Save the final HTTP status code and response body under the idempotency key with a longer TTL (e.g., 24 hours).

---

## Webhooks — server pushes to registered callback URL on event

### 1. Polling vs Event-Driven Callbacks
When an operation is asynchronous and long-running (e.g., video encoding, Stripe credit card authorization, AI model fine-tuning), clients need to know when the task finishes:

- **Short Polling (Anti-pattern):** Client fires a `GET /tasks/123/status` every 2 seconds for 15 minutes. 99.8% of requests return `{"status": "PROCESSING"}`, consuming database queries, network bandwidth, and server threads.
- **Webhooks (Reverse API):** The client registers an HTTPS callback endpoint with the provider (e.g., `https://my-app.com/webhooks/stripe`). When the event occurs, the provider's server issues an HTTP `POST` request directly to the client's URL with the event payload.

### 2. Engineering Challenges of Webhook Systems
Designing a production-grade webhook infrastructure requires solving three critical distributed systems challenges:

1. **HMAC Signature Verification (Security):**
   How does the client know the incoming HTTP POST is truly from Stripe and not an attacker forging payment events?
   - The provider shares a secret key with the client during webhook registration.
   - For every webhook payload, the provider computes a Hash-based Message Authentication Code:
     $$	ext{Signature} = 	ext{HMAC-SHA256}(	ext{Secret}, 	ext{Timestamp} + "." + 	ext{PayloadBody})$$
   - The signature is sent in the `X-Signature` header. The receiver recomputes the HMAC and verifies equality using constant-time string comparison (preventing timing attacks).
2. **Exponential Backoff & Retries:**
   If the client's server is temporarily down (returns `503 Service Unavailable` or times out), the webhook provider must queue the event and retry with exponential backoff and jitter (e.g., retry at 1m, 5m, 30m, 2h, 12h, 24h).
3. **Idempotency on the Receiver:**
   Because webhooks retry on network failures, the receiver **will receive duplicate webhook events**. The receiver must treat incoming webhook IDs idempotently to prevent processing duplicate business actions.

---

> [!TIP]
> **Summary Decision Rule for System Design Interviews:**
> - If designing a **public developer API** or standard web app: Use **REST with OpenAPI**.
> - If building a **complex mobile dashboard** with multiple nested entities and bandwidth constraints: Use **GraphQL with DataLoader**.
> - If building **high-throughput inter-service microservice backbones**: Use **gRPC over HTTP/2 with Protobuf**.
> - If handling **financial transactions or non-idempotent mutations**: Require **Idempotency Keys**.
> - If notifying external systems of **asynchronous event completion**: Provide signed **Webhooks**.
