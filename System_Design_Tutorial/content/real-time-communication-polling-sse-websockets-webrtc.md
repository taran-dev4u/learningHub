# Real-Time Communication: Polling, SSE, WebSockets & WebRTC

## Overview

The foundational architecture of the World Wide Web was built on a strictly synchronous, client-initiated request-response paradigm. Under HTTP/1.1, the browser initiates a TCP connection, sends an HTTP request, the server computes a response, delivers it, and the connection either closes or sits idle waiting for the client's next command. The server had no standardized physical mechanism to push data asynchronously to a client.

In modern distributed systems—spanning financial algorithmic trading terminals, collaborative document authoring (Google Docs, Figma), live video conferencing (Zoom, Google Meet), ride-sharing fleet tracking (Uber), and real-time chat platforms (Discord, WhatsApp)—the server must deliver state changes to clients within milliseconds of the event occurring.

Choosing the incorrect communication protocol is one of the most fatal failure modes in system design interviews. Defaulting to WebSockets for a read-only stock ticker wastes massive server memory; choosing Long Polling for an interactive collaborative canvas will melt your load balancers.

This masterclass deconstructs the physical networking layers, protocol framing, connection lifecycles, scalability bottlenecks, and architectural trade-offs across all real-time paradigms.

---

## The Protocol Evolution & Framing Physics

To understand why different protocols exist, we must inspect their physical byte framing over the wire.

```
1. SHORT / LONG POLLING (HTTP/1.1)
   Each update requires a complete HTTP request + response cycle:
   [ TCP SYN/ACK (Handshake) ] -> [ TLS 1.3 Handshake (Keys) ] -> 
   [ 800-byte HTTP Headers (Cookie, User-Agent, Auth) ] -> [ 50-byte Payload ] -> [ Connection Close / Keep-Alive ]
   * Massive header-to-payload tax (95% overhead).

2. SERVER-SENT EVENTS (SSE over HTTP/2)
   Single persistent HTTP connection using standard streaming MIME type:
   Client Request: GET /stream (Accept: text/event-stream)
   Server Response: HTTP/200 (Transfer-Encoding: chunked)
   [ event: price_update\ndata: {"AAPL": 182.4}\n\n ]  <-- Only payload bytes transferred!

3. WEBSOCKETS (RFC 6455 over TCP)
   Initial HTTP/1.1 Upgrade Handshake, then switches to minimal binary framing:
   [ 0x81 (Fin + Text Opcode) ] [ 0x85 (Mask + Len) ] [ Masking Key (4 bytes) ] [ Payload (N bytes) ]
   * Only 2 to 6 bytes of framing overhead per message! Full-Duplex over a single TCP stream.

4. WEBRTC (P2P UDP with DTLS / SRTP)
   Direct Peer-to-Peer without traversing central servers:
   [ IP Header ] [ UDP Header (8 bytes) ] [ SRTP Header (12 bytes) ] [ Encrypted Opus / VP9 Audio/Video ]
   * Sub-100ms ultra-low latency, peer-to-peer media transmission.
```

---

## Short Polling: The Naive Interval Loop

Short polling is the most primitive method for simulating real-time updates.

### How It Works
The client executes a periodic timer (e.g., `setInterval(fetchUpdates, 3000)` in JavaScript). Every 3 seconds, the browser fires an AJAX HTTP `GET /api/notifications` request to the server.
1. The server queries the database: *"Are there any new records for User ID 123 since timestamp T?"*
2. If no new events exist, the server returns an empty array: `HTTP 200 OK []`.
3. The client receives the empty payload, sleeps for 3 seconds, and repeats the cycle indefinitely.

```
Client                                                  Server / Database
  │                                                            │
  │─── GET /notifications (Are there new messages?) ──────────>│ (Queries DB: None)
  │<── HTTP 200 OK [] (No) ───────────────────────────────────│
  │                                                            │
  │    (Sleep 3000ms)                                          │
  │                                                            │
  │─── GET /notifications (Are there new messages?) ──────────>│ (Queries DB: None)
  │<── HTTP 200 OK [] (No) ───────────────────────────────────│
  │                                                            │
  │    [ EVENT OCCURS ON SERVER: Message Arrives at t=4100ms ] │
  │    (Client is unaware until next polling tick!)            │
  │                                                            │
  │─── GET /notifications (Are there new messages?) ──────────>│ (Queries DB: Found!)
  │<── HTTP 200 OK [{"id": 1, "text": "Hi"}] ─────────────────│
```

### The Architectural Fatal Flaws
1. **Catastrophic Resource Waste**: If 1,000,000 active users poll every 3 seconds, the backend infrastructure must absorb **333,333 Requests Per Second (RPS)**. Even if 99.9% of those requests return zero data, each request incurs full L7 routing, TLS decryption, authentication middleware checks, and database read IOPS.
2. **Guaranteed Delivery Latency**: If an event occurs at millisecond 100 of a 3,000ms polling interval, the user will experience an artificial 2.9-second latency before seeing the update.
3. **Mobile Battery & Data Drain**: Keeping the cellular radio in high-power state (DCH mode) drains smartphone batteries rapidly.

> [!NOTE]
> **When is Short Polling acceptable?**  
> Only when the polling interval is very long (e.g., checking for application software updates once every 6 hours), or for a short-lived asynchronous background job status check (e.g., polling `/api/jobs/export-pdf/status` every 5 seconds for a job expected to finish in 15 seconds).

---

## Long Polling (Comet / Hanging GET)

To eliminate the empty polling waste of short polling, engineers developed **Long Polling** (historically known as the Comet architecture).

### How It Works
1. The client sends an HTTP `GET /api/notifications` request.
2. The server receives the request. If no new data is currently available, **the server does NOT return an empty response**. Instead, the server suspends the request, holding the underlying TCP connection open (often using asynchronous event listeners or worker threads).
3. The connection hangs open until either:
   - **Data arrives**: The server immediately writes the payload into the open HTTP response stream and closes the connection.
   - **Timeout reached**: After an idle timeout (typically 30 to 60 seconds to prevent intermediate proxy timeouts), the server returns `HTTP 204 No Content` or `HTTP 304 Not Modified` and closes the connection.
4. The client receives the response (data or timeout) and **immediately opens a new Long Polling request**.

```
Client                                                  Server
  │                                                        │
  │─── GET /notifications ────────────────────────────────>│
  │    [ TCP Connection Held Open ]                        │ (No data; server waits...)
  │    [ ... Server does not reply ... ]                   │
  │    [ ... 14 seconds elapse ... ]                       │
  │                                                        │ [ EVENT ARRIVES! ]
  │<── HTTP 200 OK [{"msg": "Hello"}] (Closes conn) ───────│
  │                                                        │
  │─── GET /notifications (Immediately reconnects) ───────>│
  │    [ TCP Connection Held Open ]                        │ (Waiting for next event...)
```

### The Architectural Trade-offs
- **Advantage**: Zero latency lag. The instant an event is published, it pushes down the hanging connection immediately.
- **Disadvantage 1: The C10K / C100K Connection Problem**: If 100,000 users are waiting for updates, your server pool must maintain 100,000 concurrent, open, blocked TCP connections. In thread-per-connection architectures (like older Apache Tomcat or Ruby on Rails), 100,000 threads will exhaust operating system virtual memory and destroy CPU caches via context switching. (Requires event-driven runtimes like Node.js, Go goroutines, or Netty).
- **Disadvantage 2: Connection Churn & TLS Overhead**: In high-frequency environments (e.g., a busy chat room where messages arrive every second), long polling degrades into rapid opening and closing of TCP connections, causing massive CPU spikes due to repetitive TLS renegotiations.

---

## Server-Sent Events (SSE): The Lightweight Native Push

**Server-Sent Events (SSE)** is an official W3C web standard designed to provide a standardized, unidirectional (Server-to-Client) text streaming channel over standard HTTP.

### Protocol Mechanics
The client initiates a standard HTTP GET request with a specialized header:
```http
GET /api/v1/live-feed HTTP/1.1
Host: api.company.com
Accept: text/event-stream
Cache-Control: no-cache
```

The server responds with an HTTP 200 containing the `text/event-stream` MIME type and keeps the connection open indefinitely using chunked transfer encoding:
```http
HTTP/1.1 200 OK
Content-Type: text/event-stream
Cache-Control: no-cache
Connection: keep-alive
Transfer-Encoding: chunked

event: stock_tick
id: 1001
data: {"symbol": "NVDA", "price": 124.50}

event: stock_tick
id: 1002
data: {"symbol": "NVDA", "price": 125.10}
```

```
                  SERVER-SENT EVENTS (SSE) ARCHITECTURE

   Browser (Client)                                          Server (API)
          │                                                       │
          │── GET /stream (Accept: text/event-stream) ───────────>│
          │<─ HTTP 200 OK (Content-Type: text/event-stream) ──────│
          │                                                       │
          │   [ Connection remains open permanently ]             │
          │                                                       │
          │<─ event: user_joined \n data: {"name": "Alice"} ──────│ (Pushes event)
          │                                                       │
          │<─ event: price_tick  \n data: {"NVDA": 125.5} ────────│ (Pushes event)
          │                                                       │
          │   [ Network Glitch: Connection Drops! ]               │
          │                                                       │
          │── GET /stream (Last-Event-ID: 1002) ─────────────────>│ (Auto-Reconnects!)
          │<─ event: price_tick  \n data: {"NVDA": 126.0} ────────│ (Resumes stream!)
```

### Key Architectural Strengths of SSE
1. **Built-in Resiliency & Automatic Reconnection**: If the mobile network drops, the browser's native `EventSource` JavaScript API automatically reconnects with an exponential backoff.
2. **Lossless Event Recovery (`Last-Event-ID`)**: When reconnecting, the browser automatically transmits the header `Last-Event-ID: 1002`. The server inspects this ID, queries its recent event log or Redis stream, and replays all missed messages!
3. **HTTP/2 Multiplexing**: Unlike WebSockets (which require a raw dedicated TCP connection per socket), SSE runs over standard HTTP/2. Multiple SSE streams can share a **single TCP connection** multiplexed alongside normal REST API calls, bypassing browser connection limits (such as the 6-connection limit per domain in HTTP/1.1).
4. **Firewall & Corporate Proxy Friendly**: Because it is standard HTTP on port 443 with standard headers, enterprise firewalls, inspection proxies, and CDNs do not block or drop it.

### Limitations
- **Strictly Unidirectional**: Data flows only from Server to Client. If the client needs to reply, it must send an independent HTTP POST request.
- **Text-Only Framing**: Payloads must be UTF-8 text (JSON, strings). Sending raw binary data requires Base64 encoding, adding ~33% bandwidth overhead.

> [!TIP]
> **The Modern GenAI Use Case: LLM Streaming**  
> Every time you use ChatGPT, Claude, or Gemini and see tokens appearing word-by-word, that is **Server-Sent Events (SSE)**. An LLM generation task is inherently unidirectional: the user sends a prompt once (HTTP POST), and the model generates tokens over 30 seconds. Using WebSockets for LLM chat is an architectural antipattern; SSE is lighter, runs over HTTP/2, and provides built-in stream reconnection.

---

## WebSockets: Full-Duplex Bi-Directional TCP

When an application requires continuous, high-frequency, bidirectional communication in both directions with minimum latency, **WebSockets (RFC 6455)** is the undisputed gold standard.

### The WebSocket Upgrade Handshake
A WebSocket does not begin as a raw TCP connection. To safely bypass corporate firewalls and proxies, it begins life as a standard HTTP/1.1 request containing an **Upgrade Handshake**:

```http
CLIENT REQUEST:
GET /chat HTTP/1.1
Host: ws.company.com
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Sec-WebSocket-Version: 13

SERVER RESPONSE:
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
```

#### Cryptographic Handshake Mechanics:
1. The client generates a random 16-byte nonce, base64 encodes it, and sends it in `Sec-WebSocket-Key`.
2. The server concatenates this key with a globally fixed magic UUID (`258EAFA5-E914-47DA-95CA-C5AB0DC85B11`).
3. The server computes the SHA-1 hash of this string, base64 encodes it, and returns it in `Sec-WebSocket-Accept`.
4. The client verifies the SHA-1 digest. This proves that the server explicitly understands the WebSocket RFC and isn't a caching proxy that accidentally forwarded the request.
5. **The HTTP protocol is dismantled.** The underlying TCP socket remains open, transitioning to the binary WebSocket Framing Protocol.

```
                    WEBSOCKET BINARY FRAME STRUCTURE (RFC 6455)
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-------+-+-------------+-------------------------------+
|F|R|R|R| opcode|M| Payload len |    Extended payload length    |
|I|S|S|S|  (4)  |A|     (7)     |             (16/64)           |
|N|V|V|V|       |S|             |   (if payload len == 126/127) |
| |1|2|3|       |K|             |                               |
+-+-+-+-+-------+-+-------------+ - - - - - - - - - - - - - - - +
|     Masking-key (4 bytes, present ONLY if MASK bit == 1)      |
+-------------------------------+-------------------------------+
|                     Payload Data (Encrypted/Masked)           |
+---------------------------------------------------------------+
```

### Why WebSockets Are Blazingly Fast
- **Ultra-low Framing Overhead**: Normal HTTP requests carry 500 to 2,000 bytes of repetitive headers on every request. A WebSocket frame header is only **2 bytes** for small payloads (up to 125 bytes) and 6 bytes for larger payloads.
- **Zero Round-Trip Setup**: Once the handshake completes, either the client or the server can push a packet at any microsecond without requesting permission or completing TCP/TLS handshakes.
- **Full Binary Support**: Supports raw binary frames (`opcode 0x02`), allowing high-speed transmission of Protocol Buffers, FlatBuffers, or compressed audio/video chunks.

---

## WebRTC: Peer-to-Peer Sub-Second Media Streaming

If you are designing a high-definition video conferencing platform (like Zoom, Google Meet, or Discord Voice), routing millions of 4K video feeds through your central API Gateways will bankrupt the company in network egress costs and introduce unbearable latency.

**WebRTC (Web Real-Time Communication)** enables **direct browser-to-browser peer-to-peer (P2P)** media streaming.

```
                            WEBRTC ARCHITECTURE: 
             SIGNALING (CENTRAL) VS MEDIA STREAMING (P2P)

                      ┌──────────────────────┐
                      │   SIGNALING SERVER   │ (WebSocket / HTTP)
                      │ (Exchanges SDP Offer/│
                      │  Answer & ICE Info)  │
                      └───────┬──────┬───────┘
                     SDP Offer│      │SDP Answer
                              │      │
           ┌──────────────────┘      └──────────────────┐
           ▼                                            ▼
   ┌──────────────┐                              ┌──────────────┐
   │ Client Alice │                              │  Client Bob  │
   │ (IP: 10.0.1) │                              │ (IP: 192.168)│
   └──────┬───────┘                              └───────┬──────┘
          │                                              │
          │   1. Query STUN: "What is my public IP?"     │
          │<──────────────────┐      ┌──────────────────>│
          │                   ▼      ▼                   │
          │               ┌──────────────┐               │
          │               │ STUN Server  │               │
          │               └──────────────┘               │
          │                                              │
          │══════════════════════════════════════════════│
          │   2. DIRECT P2P MEDIA STREAM (SRTP / UDP)    │
          │   Sub-100ms Video / Audio (Bypasses Servers!)│
          │══════════════════════════════════════════════│
          │                                              │
          │  [ If Symmetric NAT Blocks Direct P2P: ]     │
          │                                              │
          └───> ┌──────────────┐ <───────────────────────┘
                │ TURN Relay   │ (Fallback Media Proxy)
                └──────────────┘
```

### The Three Pillars of WebRTC:
1. **Signaling (Centralized Discovery)**: WebRTC does not specify how peers find each other. You use a central WebSocket server for **Signaling**. Alice and Bob exchange their device capabilities, video codecs, and network session descriptions formatted as **SDP (Session Description Protocol)** packets.
2. **NAT Traversal (STUN & TURN)**:
   - **STUN (Session Traversal Utilities for NAT)**: Most home computers sit behind router NATs with private IP addresses (e.g., `192.168.1.5`). Alice contacts a public STUN server. The STUN server reflects back: *"To the public internet, your IP is `203.0.113.4` on port `45231`."*
   - **ICE (Interactive Connectivity Establishment)**: Alice and Bob exchange candidate IP/port pairs discovered via STUN and attempt to establish a direct P2P UDP tunnel.
   - **TURN (Traversal Using Relays around NAT)**: In ~10-15% of cases (e.g., strict symmetric corporate firewalls, mobile 4G/5G carrier-grade NATs), direct P2P connection is physically blocked. In this fallback scenario, traffic routes through a **TURN Relay Server**. (This consumes server bandwidth, but ensures 100% call connectivity).
3. **Transport (SRTP over UDP)**: Media flows over **SRTP (Secure Real-Time Transport Protocol)** on top of UDP. Packet loss is preferred over latency delays: if an audio packet drops, it is discarded rather than retried, maintaining crisp, natural conversational flow.

---

## Stateful Scaling: The 1 Million WebSocket Problem

Standard stateless REST microservices scale horizontally with trivial ease: put an AWS ALB in front of an Auto-Scaling Group, and route requests randomly.

**WebSockets break the stateless paradigm.** Once a client establishes a WebSocket connection, that specific TCP socket is pinned to a specific physical server instance in memory.

```
             THE STATEFUL MULTI-SERVER WEBSOCKET PROBLEM

   User Alice                                              User Bob
  (Connected to Server 1)                                (Connected to Server 2)
           │                                                        │
           ▼                                                        ▼
   ┌────────────────┐                                      ┌────────────────┐
   │  WS Server 1   │                                      │  WS Server 2   │
   │  Active Sockets│                                      │  Active Sockets│
   │  - Alice (FD#8)│                                      │  - Bob (FD#12) │
   └───────┬────────┘                                      └────────▲───────┘
           │                                                        │
           │ Alice sends:                                           │ How does
           │ "Hello Bob!"                                           │ Server 2 get
           │                                                        │ Alice's msg?
           ▼                                                        │
   ╔════════════════════════════════════════════════════════════════╧═════════╗
   ║                   DISTRIBUTED MESSAGE BUS (REDIS PUB/SUB)                ║
   ║  Channel: "room_general"                                                 ║
   ║  1. Server 1 publishes: PUBLISH room_general '{"to": "Bob", "msg": ..}'  ║
   ║  2. Redis broadcasts to ALL subscribed WebSocket servers                 ║
   ║  3. Server 2 receives event, looks up Bob in local socket map, and sends!║
   ╚══════════════════════════════════════════════════════════════════════════╝
```

### 1. The Distributed Routing Problem
If Alice is connected to `Server 1` in Availability Zone A, and Bob is connected to `Server 2` in Availability Zone B, `Server 1` cannot directly write bytes to Bob's socket descriptor.

#### The Solution: Distributed Pub/Sub Mesh
1. **Redis Pub/Sub or Kafka / NATS**: Every WebSocket server subscribes to the channels or rooms corresponding to its active local users.
2. When Alice sends a message to Room 42, `Server 1` publishes the message to the central Redis channel `chat:room:42`.
3. All WebSocket servers subscribed to `chat:room:42` receive the message.
4. `Server 2` inspects its in-memory map of local open connections: `local_connections.get(target_user_id)`. If Bob is connected to `Server 2`, it pushes the frame down Bob's TCP socket.

### 2. High-Density Operating System Tuning (C10M Challenge)
By default, a standard Linux kernel will crash or reject connections after ~1,000 to 4,000 open WebSockets. To support **1,000,000 concurrent WebSockets on a single powerful 64GB RAM instance**, you must tune the Linux OS kernel parameters:

```bash
# 1. Increase Maximum File Descriptors (Every open socket is a file descriptor)
sysctl -w fs.file-max=2097152
ulimit -n 1048576

# 2. Expand Ephemeral Port Range & TCP Socket Allocation
sysctl -w net.ipv4.ip_local_port_range="1024 65535"
sysctl -w net.core.somaxconn=65535

# 3. Minimize In-Memory Buffer Allocation Per Socket
# Sockets idle 99% of the time; reducing TCP read/write buffers from 128KB to 4KB
# reduces memory footprint from 128GB to 4GB RAM per million sockets!
sysctl -w net.ipv4.tcp_rmem="4096 4096 16777216"
sysctl -w net.ipv4.tcp_wmem="4096 4096 16777216"
```

### 3. Zombie Connections & Heartbeats (PING / PONG)
Mobile devices frequently drive through tunnels, switch from Wi-Fi to cellular, or experience sudden battery deaths. When a client abruptly disconnects without executing a TCP `FIN` or `RST` handshake, the server's TCP stack remains in an **ESTABLISHED** state indefinitely (a "half-open zombie socket").
- **Solution**: The WebSocket server must send a heartbeat **PING frame (`opcode 0x09`)** every 30 seconds.
- The client must respond with a **PONG frame (`opcode 0x0A`)** within 5 seconds.
- If no PONG is received, the server actively terminates the socket, frees the memory buffer, and updates the user's presence status to "Offline".

---

## Production Configuration: Nginx WebSocket Proxying

Standard reverse proxies close upstream connections when no data flows for 60 seconds. Below is a production Nginx configuration for proxying WebSocket traffic with protocol upgrade headers and persistent timeouts:

```nginx
# Map block to handle Connection header dynamically
map $http_upgrade $connection_upgrade {
    default upgrade;
    ''      close;
}

upstream websocket_backend {
    # Hash on client IP or user token for sticky session persistence
    ip_hash;
    server 10.0.2.10:8080;
    server 10.0.2.11:8080;
    keepalive 1000;
}

server {
    listen 443 ssl http2;
    server_name ws.company.com;

    ssl_certificate     /etc/ssl/certs/ws.crt;
    ssl_certificate_key /etc/ssl/private/ws.key;

    location /ws/ {
        proxy_pass http://websocket_backend;
        proxy_http_version 1.1;

        # Upgrade HTTP/1.1 to persistent WebSocket TCP connection
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        # Disable proxy buffering for real-time low latency
        proxy_buffering off;

        # Extend read/send timeouts to 24 hours (prevent proxy disconnects)
        proxy_read_timeout 86400s;
        proxy_send_timeout 86400s;
    }
}
```

---

## Master Comparison Matrix: Real-Time Protocols

| Dimension | Short Polling | Long Polling | Server-Sent Events (SSE) | WebSockets | WebRTC |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Directionality** | Client -> Server | Client -> Server (Hanging) | **Server -> Client** (Unidirectional) | **Full-Duplex** (Bidirectional) | **Peer-to-Peer** (Full-Duplex) |
| **Underlying Protocol** | HTTP/1.1 or HTTP/2 | HTTP/1.1 or HTTP/2 | HTTP/1.1 or **HTTP/2** | TCP (RFC 6455) | **UDP** (SRTP / SCTP) |
| **Framing Overhead** | ~800 bytes / request | ~800 bytes / cycle | ~20 bytes / event | **2 to 6 bytes / frame** | Minimal (RTP header) |
| **Latency** | High (Polling interval) | Low (~10ms) | Low (< 5ms) | **Ultra-low (< 2ms)** | **Sub-100ms (P2P Wire)** |
| **Server Statefulness** | Stateless | Stateful during hang | Stateful TCP connection | **Highly Stateful** | Stateless (after signaling) |
| **Auto-Reconnection** | N/A | Manual client code | **Native Browser Engine** | Manual client code | Complex ICE restarts |
| **Binary Data Support** | Base64 overhead | Base64 overhead | Text Only (Base64) | **Native Binary Support** | Native Audio/Video |
| **Scalability Difficulty** | High server load | Medium (C10K issue) | Low (HTTP/2 multiplex) | **High (Needs Redis Pub/Sub)**| Low (Offloaded to P2P) |
| **Ideal Production Use Case**| Infrequent background status checks | Legacy browser push, low-frequency alerts | **LLM Token Streaming, Stock Tickers, Live Dashboards** | **Multiplayer Gaming, Collaborative Editing, Live Chat** | **1-on-1 Video/Audio Calls (Zoom, Meet, Discord)** |

---

## Teacher FAQ & Common Interview Traps

> [!NOTE]
> **FAQ 1: "Why shouldn't I just use WebSockets for everything real-time?"**  
> Beginners love to proclaim: *"WebSockets is the best, I will use it for all live data!"* In senior interviews, this is a major red flag:
> 1. **No HTTP/2 Multiplexing**: Every WebSocket requires its own dedicated TCP socket. If a user opens 10 browser tabs to your SaaS application, that's 10 persistent TCP connections eating server memory and NAT translation tables.
> 2. **Loss of HTTP Caching & Edge CDNs**: WebSockets bypass HTTP caching entirely. Edge CDNs (Cloudflare, Akamai) cannot cache WebSocket frames.
> 3. **Firewall & Proxy Dropouts**: Many strict corporate firewalls, cellular gateways, and hotel Wi-Fi networks aggressively terminate idle TCP sockets or drop non-HTTP protocols after 60 seconds.
> 4. **Complex Load Balancing**: Rolling restarts of your backend become dangerous. If you restart a WebSocket node, 50,000 open connections disconnect simultaneously, firing a thundering herd reconnection storm against your remaining servers.

> [!WARNING]
> **FAQ 2: "How do we handle presence status (Online / Offline) for 100M users?"**  
> If an interviewer asks: *"How do you show green online indicators for 100 million users on Discord?"*  
> **Do not store presence status in a relational database.** Writing to Postgres on every connect/disconnect will crush your disks.
> - Store presence in an in-memory **Redis Sorted Set or Key-Value store with TTL**:
>   - When a user's WebSocket heartbeat succeeds, execute `SET user:presence:123 "online" EX 60`.
>   - If the user disconnects or their phone drops into an elevator, the 60-second TTL naturally expires, marking them offline automatically without requiring explicit teardown logic.

> [!TIP]
> **FAQ 3: "What about WebTransport and HTTP/3?"**  
> The future of real-time communication is **WebTransport** (built on top of **HTTP/3 and QUIC**):
> - Runs over **UDP**, eliminating the **Head-of-Line Blocking** inherent to TCP WebSockets. (If one packet drops in a TCP WebSocket, all subsequent messages are blocked until the dropped packet is retransmitted. In WebTransport/QUIC, independent streams do not block each other).
> - Provides both reliable streams and unreliable datagrams (perfect for gaming physics where lost packets should simply be skipped).
