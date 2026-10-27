# HTTP, TLS & Protocol Fundamentals

Welcome to the definitive masterclass on internet transport protocols and application delivery. In distributed systems engineering, **the network is the computer**. Every RPC call between microservices, every browser page load, and every mobile client synchronization event fundamentally rides on top of the protocols analyzed in this lesson.

Understanding HTTP, TLS, and TCP/UDP is not just trivia—it dictates your system's tail latency, connection pooling efficiency, throughput bottlenecks, and vulnerability to security breaches.

---

## HTTP methods: GET/PUT/DELETE (idempotent) vs POST/PATCH (not idempotent)

### 1. The Mathematical Concept of Idempotency
In computer science and distributed systems, an operation $f$ is **idempotent** if applying it multiple times has the exact same side-effect on the system state as applying it once:
$$f(f(x)) = f(x)$$

In HTTP API design (RFC 7231 / RFC 9110), methods are categorized by two fundamental orthogonal properties:
1. **Safe Methods:** Do not modify any server state (read-only). Safe methods are inherently idempotent.
2. **Idempotent Methods:** May modify server state, but executing the exact same request $N$ times leaves the database in the identical state as executing it 1 time.

| HTTP Method | Safe? | Idempotent? | Semantic Intent | SQL Equivalent | Distributed Retry Safe? |
|---|:---:|:---:|---|---|:---:|
| **GET** | **Yes** | **Yes** | Retrieve resource representation without side effects. | `SELECT` | **Yes (Safe to retry automatically)** |
| **HEAD** | **Yes** | **Yes** | Identical to GET but returns only headers (useful for checking cache headers or content length). | `SELECT COUNT(*)` | **Yes** |
| **OPTIONS** | **Yes** | **Yes** | Queries communication options / CORS preflight. | Metadata | **Yes** |
| **PUT** | No | **Yes** | **Complete replacement** of the resource at the URI. If it doesn't exist, create it. | `INSERT ... ON CONFLICT DO UPDATE SET (all fields)` | **Yes (Safe on network timeout)** |
| **DELETE** | No | **Yes** | Remove resource at the URI. 1st call deletes; subsequent calls return 404 but state remains deleted. | `DELETE FROM table WHERE id = ?` | **Yes (Safe on network timeout)** |
| **POST** | No | **No** | Create a subordinate resource or trigger an arbitrary state-transition workflow. | `INSERT INTO table` | **NO (Risks duplicate records/charges)** |
| **PATCH** | No | **No** (Conditionally) | Apply **partial delta modifications** to a resource (e.g. JSON Patch RFC 6902 or Merge Patch RFC 7396). | `UPDATE table SET field = field + 1` | **NO (Unless payload specifies absolute values)** |

### 2. Real-World Analogy: Light Switches vs Elevators
- **GET:** Looking at a light switch to see if it is ON or OFF. Looking at it 50 times changes nothing.
- **PUT:** Flipping the light switch strictly to the **ON** position. If you flip it to ON 1 time or 100 times, the light is still ON.
- **POST:** Pressing an elevator call button that queues a request into a dispatch counter. Pressing it 5 times might trigger 5 tickets in a poorly designed queue.
- **PATCH:** "Increase the room temperature by 2 degrees". Calling this 3 times increases the temperature by 6 degrees (non-idempotent!). However, "Set thermostat to 72 degrees" is an idempotent patch.

### 3. How Senior Engineers Handle Non-Idempotent Network Failures
Consider a payment processing API:
```
Client                      Payment Service               Stripe / Banking Gateway
  |                                |                                |
  |--- POST /v1/charges ($100) --->|                                |
  |    (Header: Idempotency-Key)   |--- Create Charge ($100) ------>|
  |                                |<-- Charge Succeeded -----------|
  |          [NETWORK TIMEOUT]     |                                |
  |   (Client never got response)  |                                |
  |                                |                                |
  |=== RETRY: POST /v1/charges ===>|                                |
  |    (Same Idempotency-Key)      |-- [Key found in Redis Cache] --|
  |                                |-- Return cached receipt -------|
  |<-- Charge Receipt ($100) ------|                                |
```

If a client experiences a network timeout after sending a `POST /charges`, did the payment go through or did it fail before reaching the server? The client cannot know!
- **The Idempotency Key Pattern:** The client generates a unique UUID v4 (`Idempotency-Key: 7b3f9c81-...`).
- The API gateway or service checks a distributed cache (Redis) with an atomic `SET key value NX EX 86400`.
- If the key is already processing, return `409 Conflict` or wait.
- If already processed, return the cached serialized HTTP response directly without re-executing the transaction.

---

## HTTP status codes: 2xx, 3xx, 4xx, 5xx categories

Status codes communicate the outcome of an HTTP transaction at the protocol layer before the client even inspects the payload:

### 1. 2xx: Success (Request Received, Understood, Accepted)
- **200 OK:** Standard success response for `GET`, `PUT`, or `PATCH`.
- **201 Created:** The request succeeded and led to the creation of a new resource (standard for `POST`). Must include a `Location` header pointing to the new resource URL.
- **202 Accepted:** The request has been accepted for asynchronous processing (e.g., queued in Kafka or RabbitMQ), but processing has not completed. Prevents blocking HTTP connections during heavy background jobs.
- **204 No Content:** Success, but there is no body to return (standard for `DELETE` operations or preflight `OPTIONS`).

### 2. 3xx: Redirection (Further Action Required)
- **301 Moved Permanently:** The resource now lives at a new URL permanently. **Critical interview detail:** Browsers and search engines aggressively cache 301 redirects in local storage. Never use 301 for temporary promotional routes or during canary deployments!
- **302 Found (Temporary Redirect):** Temporary redirect. Browsers do not cache this permanently.
- **304 Not Modified:** Sent during conditional `GET` requests (via `If-None-Match: "etag123"` or `If-Modified-Since`). The server informs the client that the locally cached copy is still fresh, saving 100% of the response bandwidth!
- **307 Temporary Redirect vs 308 Permanent Redirect:** Strictly preserves the original HTTP method (e.g. a `POST` must be resent as a `POST`, whereas legacy 301/302 allowed browsers to erroneously rewrite `POST` to `GET`).

### 3. 4xx: Client Error (The Caller Made a Mistake)
- **400 Bad Request:** Malformed syntax, invalid JSON, or failed schema validation.
- **401 Unauthorized:** Actually means **Unauthenticated**. The client has not supplied valid credentials (e.g. missing or expired JWT/API key).
- **403 Forbidden:** The client is authenticated, but **unauthorized** to access this resource (e.g., standard user trying to access admin endpoints).
- **404 Not Found:** Resource does not exist, or the server is hiding existence from unauthorized users.
- **409 Conflict:** The request conflicts with current server state (e.g. optimistic locking version mismatch, duplicate unique email registration, or concurrent idempotency lock).
- **422 Unprocessable Entity:** The payload is syntactically correct JSON, but violates business validation rules (e.g. end date is before start date).
- **429 Too Many Requests:** The client has exceeded their rate limit. Must return a `Retry-After: 60` header.

### 4. 5xx: Server Error (The Server or Infrastructure Failed)
- **500 Internal Server Error:** Unhandled exception in backend code.
- **502 Bad Gateway:** The reverse proxy / load balancer received an invalid or crashed response from the upstream microservice container.
- **503 Service Unavailable:** The server is overloaded or down for maintenance. Frequently returned by load balancers when all health checks fail.
- **504 Gateway Timeout:** The reverse proxy waited for the upstream backend, but the backend database query timed out before answering.

---

## HTTP/1.1 — text, one request per connection, head-of-line blocking

### 1. Architectural Model of HTTP/1.1 (RFC 2616)
Released in 1999, HTTP/1.1 introduced **Keep-Alive (persistent TCP connections)**:
Instead of tearing down the TCP connection after every single resource request (as in HTTP/1.0), a TCP connection could remain open to serve multiple sequential requests.

```
HTTP/1.1 Sequential Pipeline on 1 TCP Connection:

Client ----------------------- Server
  |--- GET /index.html ---------->|
  |<-- 200 OK (index.html) -------|  (Waits for full download)
  |--- GET /style.css ----------->|
  |<-- 200 OK (style.css) --------|  (Waits for full download)
  |--- GET /logo.png ------------>|
  |<-- 200 OK (logo.png) ---------|
```

### 2. The Core Flaw: Application-Layer Head-of-Line (HOL) Blocking
In HTTP/1.1, requests and responses are plain ASCII text streams without frame tags. Therefore, **responses must arrive in the exact order they were requested**:
- If request #1 is for a massive 50MB video file, and request #2 is for a critical 2KB JavaScript file, request #2 is completely blocked until request #1 finishes downloading!
- If the server experiences a database lock on request #1, all subsequent requests queued on that TCP connection stall.

### 3. Hacks Used to Survive HTTP/1.1 (And Why They Hurt)
To work around HOL blocking, web architectures invented costly workarounds:
1. **Domain Sharding:** Browsers limit parallel TCP connections per domain to 6. Engineers created `static1.example.com`, `static2.example.com` to trick browsers into opening 24-30 TCP connections simultaneously. (Cost: massive DNS overhead and server memory bloat).
2. **Sprite Sheets & CSS Concatenation:** Bundling hundreds of small icon images into one giant image to reduce HTTP request counts.
3. **Inlining Assets:** Pasting Base64 images directly into HTML/CSS. (Cost: prevents browser asset caching).

---

## HTTP/2 — binary framing, multiplexing, header compression (HPACK)

Released in 2015 (RFC 7540), HTTP/2 completely redesigned the transport layer while preserving the exact same semantics (`GET`, `POST`, headers, status codes).

```
HTTP/2 Multiplexing on a Single TCP Connection:

[ Stream 1: Header Frame (GET /index.html) ]
[ Stream 2: Header Frame (GET /style.css)   ]
[ Stream 1: Data Frame   (index.html chunk) ]
[ Stream 3: Header Frame (GET /logo.png)    ]
[ Stream 2: Data Frame   (style.css chunk)  ]
[ Stream 3: Data Frame   (logo.png chunk)   ]
```

### 1. Binary Framing Layer
Instead of delimiter-separated ASCII text (`\r\n`), HTTP/2 breaks every message into discrete, strongly-typed **Binary Frames**:
- Length (24 bits)
- Type (8 bits: `DATA`, `HEADERS`, `SETTINGS`, `RST_STREAM`, etc.)
- Flags (8 bits: `END_STREAM`, `END_HEADERS`)
- Stream Identifier (31 bits)

### 2. Full Multiplexing & Stream Prioritization
Because each binary frame carries a 31-bit **Stream ID**, hundreds of independent request-response exchanges can interleave asynchronously across a **single TCP connection**:
- A slow database query on Stream 1 does not block Stream 2 or Stream 3 from delivering their CSS and image assets immediately.
- Eliminates the need for domain sharding, sprite sheets, or multiple TCP connections.

### 3. Header Compression via HPACK (RFC 7541)
In modern web applications, HTTP headers (cookies, user-agents, authorization Bearer tokens) frequently total 1-2 KB per request.
- **The Problem:** Compressing headers with standard gzip is vulnerable to the **CRIME** attack (chosen-plaintext attack recovering secrets from compressed byte lengths).
- **The HPACK Solution:** HTTP/2 uses HPACK, which maintains two stateful lookup tables (a Static Table of common headers like `:method: GET` and a Dynamic Table updated per connection). If a request repeats headers, only small numeric indices (1-2 bytes) are sent over the wire!

---

## HTTP/3 — UDP-based QUIC, 0-RTT, no TCP HOL blocking

Despite HTTP/2 multiplexing, a fundamental bottleneck remained: **TCP-level Head-of-Line Blocking**.

```
HTTP/2 over TCP:
Packet 1 (Stream 1)  ---> [OK]
Packet 2 (Stream 2)  ---> [LOST IN NETWORK]
Packet 3 (Stream 3)  ---> [Arrives, but TCP OS buffer BLOCKS Stream 3 until Packet 2 retransmits!]

HTTP/3 over QUIC (UDP):
Packet 1 (Stream 1)  ---> [OK]
Packet 2 (Stream 2)  ---> [LOST IN NETWORK] (Stream 2 pauses)
Packet 3 (Stream 3)  ---> [DELIVERED IMMEDIATELY! Stream 3 processes without waiting!]
```

### 1. Why TCP Causes HOL Blocking in HTTP/2
TCP is an in-order, reliable byte-stream abstraction implemented inside the operating system kernel.
- If a single packet carrying Stream 2 is dropped due to WiFi jitter, TCP halts delivery of *all subsequent packets* in the kernel buffer—even if those packets belong to Stream 3 or Stream 4—until the missing packet is retransmitted (via TCP SACK / ACK timeout).
- On lossy mobile networks (3G/4G/public WiFi with 2% packet loss), HTTP/2 often performed **worse than HTTP/1.1**!

### 2. Enter QUIC (Quick UDP Internet Connections - RFC 9000)
HTTP/3 completely abandons TCP and operates over **UDP**.
- QUIC re-implements reliability, congestion control (BBR / Cubic), and loss recovery in **user space** on top of UDP datagrams.
- Each HTTP stream is recognized natively by QUIC: a dropped packet on Stream 2 stalls *only Stream 2*. Streams 1, 3, and 4 continue processing at full line speed without interference!

### 3. Connection Migration (Zero Mobile Reconnect Drops)
In standard TCP, a connection is identified by a 4-tuple: `(Source IP, Source Port, Destination IP, Destination Port)`.
- When a smartphone user walks out of their house and transitions from **Home WiFi to 5G Cellular**, their IP address changes instantly.
- In HTTP/1.1 and HTTP/2, all active TCP connections break. Video playback halts, file uploads abort, and a new 3-way handshake + TLS handshake must re-execute.
- In HTTP/3 QUIC, connections are identified by a 64-bit random **Connection ID (CID)** that is independent of IP addresses. The client seamlessly migrates from WiFi to 5G without resetting the connection!

---

## TLS 1.3 handshake — 1 RTT, forward secrecy

Transport Layer Security (TLS) encrypts application traffic to guarantee:
1. **Confidentiality:** Eavesdroppers cannot read payload bytes.
2. **Integrity:** MitM attackers cannot tamper with packets.
3. **Authentication:** Proves the server is who it claims to be (via X.509 certificates).

### 1. TLS 1.2 vs TLS 1.3 Handshake Architecture

```
TLS 1.2 Handshake (2 RTTs + TCP 1 RTT = 3 RTTs before data!):

Client                                           Server
  |--- TCP SYN ---------------------------------->|
  |<-- TCP SYN-ACK -------------------------------|  (1 RTT: TCP)
  |--- TCP ACK + ClientHello -------------------->|
  |<-- ServerHello + Certificate + ServerKeyEx ---|  (2 RTT: TLS negotiation)
  |--- ClientKeyEx + ChangeCipherSpec + Finished ->|
  |<-- NewSessionTicket + Finished ---------------|  (3 RTT: Cipher lock)
  |=== GET /api/data (Application Data) --------->|

Total Latency before first byte: 3 RTT! (Over 100ms mobile = 300ms delay!)
```

```
TLS 1.3 Handshake (1 RTT + TCP 1 RTT = 2 RTTs total!):

Client                                           Server
  |--- TCP SYN ---------------------------------->|
  |<-- TCP SYN-ACK -------------------------------|  (1 RTT: TCP)
  |--- TCP ACK + ClientHello + Key Share (Diffie)->|
  |<-- ServerHello + Key Share + Certificate + Finished -| (2 RTT: Done!)
  |=== GET /api/data (Application Data) --------->|

Total Latency before first byte: Reduced by 33-50%!
With QUIC + TLS 1.3 (HTTP/3): Connection + Security established in 1 RTT (or 0-RTT on reconnect)!
```

### 2. Perfect Forward Secrecy (PFS)
In legacy TLS 1.2, servers frequently used RSA key exchange where the client encrypted the premaster secret with the server's public key.
- **The Catastrophe:** If an adversary intercepts and archives encrypted traffic for 5 years, and later compromises the server's private RSA key, they can retroactively decrypt all 5 years of historical user traffic!
- **TLS 1.3 Mandatory Ephemeral Diffie-Hellman (ECDHE):** TLS 1.3 outlawed static RSA key exchange. Every session generates temporary, throwaway elliptic-curve key pairs ($g^a \pmod p, g^b \pmod p$). Once the session ends, the keys are wiped from RAM. Stealing the server's certificate in the future decrypts **zero past traffic**.

---

## Protocol Comparison Summary

| Metric / Feature | HTTP/1.1 | HTTP/2 | HTTP/3 (QUIC) |
|---|---|---|---|
| **Underlying Transport** | TCP | TCP | UDP |
| **Data Format** | Plaintext ASCII | Binary Frames | Binary Frames |
| **Multiplexing** | No (Sequential) | Yes (Application level) | Yes (Transport & App level) |
| **HOL Blocking** | Severe (HTTP level) | None at HTTP, Yes at TCP level | **Completely Eliminated** |
| **Handshake Latency** | 1 RTT (TCP) + 2 RTT (TLS 1.2) | 1 RTT (TCP) + 1 RTT (TLS 1.3) | **0 to 1 RTT Total (Integrated)** |
| **Connection Migration** | Breaks on IP change | Breaks on IP change | **Zero-drop migration via CID** |
| **Header Compression** | None | HPACK (Static + Dynamic) | QPACK (Out-of-order resilient) |

---

> [!NOTE]
> ### 🎓 Teacher FAQ & Common Beginner Mistakes
>
> **Q: "Is HTTP/3 always faster than HTTP/2?"**
> Surprisingly, not on localhost or datacenter LANs! Because Linux kernels have 30+ years of hardware offloading optimizations for TCP (TSO, LRO, checksum offload), running UDP in user space can sometimes consume 15-20% more CPU on server hardware. HTTP/3 shines primarily on the **public edge / last-mile mobile internet**, where packet loss and mobile network switching occur frequently.
>
> **Q: "Why can't we use 0-RTT for all requests in TLS 1.3?"**
> Because 0-RTT early data is vulnerable to **Replay Attacks**! An eavesdropper who intercepts an encrypted 0-RTT `POST /transfer?amount=100` packet cannot read it, but can retransmit it 50 times to the server. Never permit non-idempotent mutations over 0-RTT early data!
