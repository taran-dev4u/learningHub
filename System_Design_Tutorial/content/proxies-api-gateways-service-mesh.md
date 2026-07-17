# Proxies, API Gateways & Service Mesh

## Overview
As your architecture grows from a simple monolithic server into a sprawling microservices ecosystem, routing traffic becomes incredibly complex. You need dedicated infrastructure to manage how requests flow into your network (North-South traffic) and how services talk to each other internally (East-West traffic).

This masterclass dissects the layers of traffic management: Proxies, API Gateways, and the modern Service Mesh.

---

## Forward vs reverse proxy

The word "Proxy" just means "a middleman." To understand proxies, you just need to know who the middleman is protecting.

### Forward Proxy (Protects the Client)
A Forward Proxy sits in front of the **Client** (e.g., your laptop in a corporate office).
- **How it works:** When you try to visit `facebook.com`, your request goes to the corporate proxy first. The proxy checks its rules, sees Facebook is blocked, and denies the request. If you visit `google.com`, the proxy forwards the request on your behalf.
- **Goal:** Hide the client's IP from the internet, enforce corporate web filters, or cache outbound requests. (VPNs act as forward proxies).

### Reverse Proxy (Protects the Server)
A Reverse Proxy sits in front of the **Server** (e.g., inside an AWS datacenter).
- **How it works:** When a user tries to access your API, they don't hit your application server directly. They hit the Reverse Proxy (like Nginx). The proxy then forwards the request to an internal server.
- **Goal:** Hide internal IP addresses from hackers, terminate SSL/TLS encryption (saving CPU for the app servers), and compress outgoing responses.

---

## API gateway responsibilities

An API Gateway is essentially a highly-intelligent Reverse Proxy designed specifically for microservices. It acts as the single entry point (the front door) for all external clients (Mobile, Web, IoT).

**Core Responsibilities (The Cross-Cutting Concerns):**
1. **Authentication & Authorization:** Validates JWT tokens so your 50 microservices don't have to duplicate auth logic.
2. **Rate Limiting:** Protects backend services from DDoS attacks or scraping by throttling greedy IPs.
3. **Routing & Composition:** A client asks for `/dashboard`. The Gateway routes the request to the User Service, the Billing Service, and the Notification Service, merges the JSON responses, and sends a single payload back to the client.
4. **Protocol Translation:** Accepts HTTP/REST from the public internet and translates it into gRPC to talk to internal microservices.

---

## Load balancer L4 vs L7

(Note: We covered this deeply in the Load Balancers module, but let's review the architectural distinction here).

- **L4 (Transport Layer):** Operates on IP addresses and TCP/UDP ports. It is incredibly fast but "dumb." It doesn't know if the user is asking for a video or a text file. Used at the absolute edge of your network to distribute raw traffic across multiple API Gateways.
- **L7 (Application Layer):** Inspects the HTTP payload. It can read URLs, headers, and cookies. Used behind the scenes to route specific endpoints (e.g., `/api/payments`) to specific microservice clusters. **API Gateways operate at Layer 7.**

---

## Service mesh sidecars

An API Gateway handles **North-South** traffic (traffic entering your datacenter from the internet).
But what about **East-West** traffic? (e.g., Your Payment Service needs to talk to your User Service).

Historically, developers imported libraries (like Netflix Ribbon or Hystrix) into their application code to handle internal load balancing, retries, and circuit breakers. This was a nightmare if the Payment Service was written in Java and the User Service was written in Go.

**The Solution: Service Mesh (e.g., Istio, Linkerd)**
Instead of putting networking logic in the application code, a Service Mesh injects a **Sidecar Proxy** (usually Envoy) directly into the same server/container as your microservice.

**How it works:**
1. The Payment Service wants to call the User Service.
2. The Payment Service sends a basic HTTP request to `localhost:8080` (its own Sidecar).
3. The Sidecar takes over. It finds a healthy User Service instance, encrypts the traffic (mTLS), adds a distributed tracing header, handles any network retries if it fails, and securely delivers the payload to the User Service's Sidecar.

> [!TIP]
> **Teacher's Analogy:** A Service Mesh acts like a post office attached to your house. You just drop the letter in your own mailbox (the Sidecar), and the postal system handles the routing, security, delivery retries, and tracking automatically, regardless of what language you wrote the letter in.
