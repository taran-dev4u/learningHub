# HTTP, TLS & Protocol Fundamentals

## Overview
Every system design interview assumes you understand how computers talk to each other over the internet. You cannot design a Load Balancer or an API Gateway if you do not understand the underlying protocols (HTTP and TCP).

This masterclass goes deep into HTTP methods, status codes, the evolution from HTTP/1.1 to HTTP/3, and the critical TLS handshake.

---

## HTTP methods: GET/PUT/DELETE (idempotent) vs POST/PATCH (not idempotent)

HTTP verbs define *what* you want to do with a resource. The most important concept for interviews is **Idempotency**.

An operation is **Idempotent** if performing it once has the exact same effect as performing it 100 times.

| Method | Idempotent? | Use Case | Example |
| :--- | :--- | :--- | :--- |
| **GET** | Yes | Read a resource. Never mutates data. | `GET /users/123` |
| **PUT** | Yes | Completely replace a resource. | `PUT /users/123` (Sending the same user object 5 times results in the same final state). |
| **DELETE** | Yes | Remove a resource. | `DELETE /users/123` (Deleting it 5 times still results in it being deleted). |
| **POST** | **No** | Create a new resource. | `POST /orders` (Clicking "Submit" 5 times creates 5 distinct orders and charges your card 5 times!). |
| **PATCH** | **No** (Usually) | Partially update a resource. | `PATCH /users/123 { "age": age + 1 }` (Sending this 5 times ages the user 5 years). |

> [!WARNING]
> **Interview Trap:** If an interviewer asks, "How do you handle network retries when a client's POST request drops?", do not say "Just retry." You must implement an **Idempotency Key** (a unique ID sent by the client) so the server can deduplicate retries and prevent double-charging!

---

## Status codes: 2xx success · 3xx redirect · 4xx client · 5xx server

Status codes tell the client what happened without parsing a JSON body.

- **2xx (Success):** `200 OK`, `201 Created` (used after a successful POST), `202 Accepted` (used for async batch jobs where the server says "I got it, but I haven't processed it yet").
- **3xx (Redirect):** `301 Moved Permanently` (browsers cache this!), `302 Found` (temporary redirect).
- **4xx (Client Error):** You messed up. `400 Bad Request`, `401 Unauthorized` (You don't have a valid token), `403 Forbidden` (You have a token, but you lack admin rights), `429 Too Many Requests` (Rate limited).
- **5xx (Server Error):** We messed up. `500 Internal Server Error`, `503 Service Unavailable` (usually returned by a Load Balancer when backend servers are dead).

---

## HTTP/1.1 — text, one request per connection, head-of-line blocking

**HTTP/1.1** is the legacy standard.
- **How it works:** It uses plain text. To fetch a webpage with 10 images, the browser must open a TCP connection, ask for image 1, wait for the response, ask for image 2, wait, etc.
- **The Flaw:** Head-of-Line (HOL) Blocking. If image 1 is a massive 10MB file, images 2-10 cannot download until image 1 finishes, even if there is available bandwidth.

---

## HTTP/2 — binary framing, multiplexing, header compression (HPACK)

**HTTP/2** fixed the major flaws of 1.1 without changing the HTTP verbs or headers.
- **Binary Framing:** Data is broken down into binary frames instead of plain text, making it much faster for servers to parse.
- **Multiplexing:** Solves HTTP HOL blocking. You can send requests for images 1-10 simultaneously over a **single TCP connection**. The server can send back the chunks of images 2-10 even while image 1 is still downloading.
- **Header Compression:** Uses HPACK to compress headers (like heavy Cookies), drastically reducing bandwidth.

> [!NOTE]
> **Teacher's FAQ:** If HTTP/2 is multiplexed, did it solve Head-of-Line blocking completely?
> **Answer:** It solved *HTTP* HOL blocking, but not *TCP* HOL blocking. Since HTTP/2 still runs over TCP, if a single packet is lost at the network layer, TCP will halt all streams on that connection until the lost packet is retransmitted. This is why HTTP/3 was created!

---

## HTTP/3 — UDP-based QUIC, 0-RTT, no TCP HOL blocking

**HTTP/3** throws out TCP completely. It runs over **QUIC**, which is built on top of UDP.

- **No TCP HOL Blocking:** Because it uses UDP, if packet 3 of Image A is lost, only Image A is delayed. Image B continues to stream perfectly.
- **0-RTT Handshakes:** If a client has talked to a server before, QUIC can establish a secure connection in zero round trips, instantly sending data. This is massive for mobile networks with high latency.

---

## TLS 1.3 handshake — 1 RTT, forward secrecy

**TLS (Transport Layer Security)** is what makes HTTP into HTTPS.

When a client connects to a server, they must agree on an encryption key without anyone eavesdropping.
- **Legacy (TLS 1.2):** Required 2 Round Trips (RTT) to establish a connection. Over a slow 150ms connection, the user waits 300ms before a single byte of actual data is sent.
- **Modern (TLS 1.3):** Optimized to 1 RTT.
- **Perfect Forward Secrecy:** Uses Diffie-Hellman ephemeral keys. If a hacker records all your encrypted traffic today, and then steals the server's private key tomorrow, they *still* cannot decrypt the past traffic, because a unique, temporary key was used for that specific session.
