# Real-Time Communication: Polling, SSE, WebSockets & WebRTC

## Overview
Standard HTTP is fundamentally designed for request-response: The client asks for data, the server answers, and the connection closes.

But what if you are building a Chat App, Live Sports Scores, or a Collaborative Document? The server needs to push data to the client the millisecond an event happens.

This masterclass breaks down the evolution of real-time communication, from hacky polling techniques to full-duplex WebSockets.

---

## Short polling — client requests every N seconds, wasteful

The easiest, but worst, way to simulate real-time updates.

**How it works:** The client sets a timer in JavaScript to make an AJAX HTTP request to the server every 5 seconds. *"Any new messages? Any new messages?"*
- **Pros:** Incredibly simple to implement. Works on every browser.
- **Cons:** Extremely wasteful. 99% of the time, the server responds with "No." This creates massive, unnecessary load on your servers, load balancers, and network bandwidth. It also guarantees a latency of up to 5 seconds.

---

## Long polling — server holds connection until data ready or timeout

To fix the wastefulness of Short Polling, engineers invented Long Polling.

**How it works:** The client makes an HTTP request to the server. But if the server has no new messages, it *does not reply immediately*. It holds the TCP connection open. It waits until a new message arrives, sends it back to the client, and closes the connection. The client immediately opens a new Long Poll connection.
- **Pros:** No empty responses. The moment a message arrives, it is delivered instantly (low latency).
- **Cons:** If you have 1 million users waiting for a message, your server has 1 million open TCP connections doing absolutely nothing. This requires heavy OS tuning (solving the C10K problem). Also, the constant opening and closing of HTTP connections incurs TLS handshake overhead.

---

## SSE (Server-Sent Events) — HTTP-based, server→client only, auto-reconnect

**Server-Sent Events (SSE)** is an elegant, native browser API that solves Long Polling's overhead while staying within standard HTTP.

**How it works:** The client makes a standard HTTP request. The server responds with `Content-Type: text/event-stream`. The connection is kept open indefinitely. The server can now push a continuous stream of text messages down that single pipe whenever it wants.
- **Pros:** Uses standard HTTP (no special Load Balancer tuning required). The browser handles automatic reconnections if the network drops.
- **Cons:** It is **Unidirectional** (Server -> Client only). The client cannot send messages back up the same pipe.
- **Use Case:** Live stock tickers, sports scores, Twitter feed updates, or ChatGPT streaming its text response back to you.

---

## WebSockets — full-duplex TCP, use for chat, real-time games, collaboration

If you need data flowing rapidly in *both* directions, you need WebSockets.

**How it works:** The client sends an HTTP "Upgrade" request. If the server agrees, the HTTP protocol is stripped away, leaving a persistent, raw, bidirectional TCP connection. Either side can send binary or text frames at any time with zero HTTP header overhead.
- **Pros:** **Full-Duplex**. Blazing fast. Lowest possible latency for two-way communication.
- **Cons:** Stateful and very difficult to scale (see below). Load balancers must be configured to support WebSocket upgrades.
- **Use Case:** Multiplayer gaming, Discord chat, collaborative whiteboards (Figma), WhatsApp.

---

## WebRTC — peer-to-peer media, used for video calls (Zoom, Meet)

If you are streaming a 4K video call from your laptop to your friend's laptop, sending that massive video feed through a centralized server is expensive and adds latency.

**How it works:** WebRTC (Web Real-Time Communication) uses a central server only to help the two laptops find each other (Signaling). Once they connect, the server steps away, and the video/audio data streams **Peer-to-Peer** via UDP directly between the laptops.
- **Pros:** Lowest latency for heavy media. Saves the company millions in bandwidth costs.
- **Cons:** Very complex to punch through corporate firewalls and NATs (requires STUN/TURN servers as fallbacks).

---

## Scaling WebSockets — sticky LB or message broker fan-out (Redis Pub/Sub)

In a standard HTTP architecture, scaling is easy because servers are stateless. WebSockets are **stateful**. If User A is connected to Server 1, and User B is connected to Server 2, how do they chat?

### 1. Sticky Sessions
You can configure the Load Balancer to ensure a user's TCP connection always stays pinned to a specific server. But this creates uneven loads and makes deployments dangerous (if you restart Server 1, you instantly drop 50,000 active connections).

### 2. Message Broker Fan-out (The Right Way)
You introduce a highly optimized Message Broker (like Redis Pub/Sub or Kafka) behind the WebSocket servers.
1. User A sends a chat message to Server 1.
2. Server 1 pushes the message into the Redis `chat_room_channel`.
3. All WebSocket servers (Server 1, 2, 3) are subscribed to that Redis channel.
4. Server 2 receives the message from Redis and pushes it down the open WebSocket connection to User B.

> [!NOTE]
> **Teacher's Advice:** In a system design interview, if you say "I will use WebSockets for the chat app," the interviewer will immediately ask "How do you scale it?" You must instantly draw the Redis Pub/Sub layer connecting the WebSocket servers to prove you understand stateful scaling.
