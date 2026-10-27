# DNS, Load Balancers & Traffic Routing

Welcome to the definitive masterclass on internet traffic ingress and routing. When designing systems that handle millions of concurrent users, reliability begins the millisecond a packet leaves the user's browser. 

A production system does not simply consist of application servers and databases. Between the user and your backend code lies a sophisticated global routing fabric: **Hierarchical DNS resolvers**, **Anycast BGP routing**, **Layer 4 transport load balancers**, and **Layer 7 application reverse proxies**.

In this masterclass, we dissect every layer of the network stack that transports a user request from a domain name lookup to the exact CPU core of a healthy backend worker.

---

## Hierarchical DNS Resolution Flow

### 1. The Global Architecture of DNS
The **Domain Name System (DNS)** is a globally distributed, hierarchical, read-heavy database whose primary responsibility is mapping human-readable hostnames (e.g., `api.uber.com`) to machine-routable IP addresses (e.g., IPv4 `104.36.198.1` or IPv6 `2606:4700::6810:1`).

Because the internet cannot rely on a single centralized database, DNS is organized into an inverted hierarchical tree:

```
                          [ . ] (Root Zone)
                         /     |                             [.com]   [.org]     [.net] (Top-Level Domains - TLD)
                    /
             [uber.com] (Authoritative Name Server)
             /           [api.uber.com]  [m.uber.com] (Subdomains / Resource Records)
```

### 2. The 8-Step Recursive Resolution Walkthrough
When a client application requests `https://api.example.com` for the very first time with a cold cache, the resolution proceeds through 8 deterministic steps:

```
[Browser / OS Client]
   |
   | (1) Query: "api.example.com"
   v
[Recursive Resolver (ISP / 8.8.8.8 / 1.1.1.1)]
   |
   |--- (2) Query Root: "Where is .com?" -------------------> [Root Name Server]
   |<-- (3) Referral: Ask TLD Server (e.g., a.gtld-servers.net) -|
   |
   |--- (4) Query TLD: "Where is example.com?" -------------> [TLD Name Server (.com)]
   |<-- (5) Referral: Ask Authoritative Server (ns1.awsdns.com) -|
   |
   |--- (6) Query Authoritative: "What is A for api.example.com?" -> [Authoritative NS]
   |<-- (7) Answer: A Record = 93.184.216.34 (TTL = 300s) -----------|
   |
   | (8) Returns IP 93.184.216.34 to OS / Browser
   v
[Browser initiates TCP 3-Way Handshake to 93.184.216.34:443]
```

1. **Browser & OS Cache Lookup:** The browser checks its internal DNS cache (Chrome: `chrome://net-internals/#dns`). If missed, it queries the OS DNS stub resolver (which checks the local hosts file and OS DNS cache).
2. **Query to Recursive Resolver:** The OS forwards the query to the configured recursive resolver (typically assigned via DHCP by the ISP or configured to public Anycast resolvers like Google `8.8.8.8` or Cloudflare `1.1.1.1`).
3. **Query to Root Name Servers:** The recursive resolver queries one of the **13 logical Root Server clusters** (`[a-m].root-servers.net`). These 13 addresses are backed by over 1,500 physical server instances distributed globally using Anycast routing.
4. **Referral to TLD Name Servers:** The Root server responds with the Nameserver (NS) records for the `.com` Top-Level Domain registry (managed by Verisign).
5. **Query to TLD Name Servers:** The resolver queries the `.com` TLD servers.
6. **Referral to Authoritative Name Servers:** The TLD server responds with the NS records for `example.com` (e.g., pointing to AWS Route 53 or Cloudflare nameservers).
7. **Query to Authoritative Name Server:** The resolver queries the Authoritative nameserver, which holds the official zone file for `example.com`.
8. **Final Answer & Cache Injection:** The Authoritative server returns the `A` record (`93.184.216.34`) along with a **Time-To-Live (TTL)** value (e.g., `300` seconds). The recursive resolver caches this record for 300 seconds and returns it to the client.

> [!NOTE]
> **Latency Breakdown:** A cold DNS query traversing Root &rarr; TLD &rarr; Authoritative takes between **80ms to 250ms** across multiple WAN round-trips. A warm cache hit takes **< 1ms**. This is why DNS records rely on aggressive caching.

---

## DNS record types: A, AAAA, CNAME, MX, TXT, NS

In production infrastructure and system design interviews, you must understand the exact semantics, limitations, and performance implications of the primary DNS record types:

| Record Type | Full Name | Target Value | Practical System Design Use Case |
|---|---|---|---|
| **A** | Address Record | 32-bit IPv4 address (`192.0.2.1`) | Directs traffic directly to an IPv4 host, Anycast edge IP, or Layer 4 Load Balancer. |
| **AAAA** | IPv6 Address Record | 128-bit IPv6 address (`2001:db8::1`) | Modern mobile and cellular networks (many carriers run IPv6-only internal backbones). |
| **CNAME** | Canonical Name | Domain name alias (`lb-123.us-east-1.elb.amazonaws.com`) | Aliasing subdomains to cloud provider endpoints. **Rule: Cannot exist at the zone apex (`@` or root domain)!** |
| **ALIAS / ANAME** | Virtual Flattened Alias | IP addresses resolved at runtime | Cloud-specific record (Route 53 ALIAS) that enables CNAME-like behavior at the zone apex (`example.com`). |
| **NS** | Name Server | Hostname of authoritative server | Delegates a DNS zone to a specific DNS provider (e.g., `ns-1.awsdns.com`). |
| **MX** | Mail Exchange | Priority integer + mail server hostname | Routes inbound emails for `@domain.com`. |
| **TXT** | Text Record | Arbitrary UTF-8 string | Domain verification (Google Workspace), email anti-spoofing protocols (**SPF**, **DKIM**, **DMARC**). |
| **SRV** | Service Record | Host, port, priority, and weight | Internal microservice discovery (Consul, Active Directory, Kubernetes CoreDNS). |
| **CAA** | Certification Authority Authorization | Authorized Certificate Authorities | Restricts which CAs (e.g., Let's Encrypt, DigiCert) are legally allowed to issue TLS certificates for your domain. |

### The CNAME Apex Restriction Trap
A common architectural trap is attempting to map your apex root domain (`example.com`) directly to an AWS Elastic Load Balancer (ELB) using a standard CNAME:
$$	ext{example.com. IN CNAME my-load-balancer-123.amazonaws.com. (INVALID!)}$$
RFC 1034 states that **if a CNAME record exists at a node, no other data may exist at that node**. Because the apex domain must have `NS` and `SOA` records, placing a standard CNAME at the apex violates RFC specifications and breaks email (`MX`).

*Solution:* Use **CNAME Flattening** (Cloudflare) or **Route 53 ALIAS records**. The DNS server automatically resolves the external hostname internally and serves direct `A` records to the client, preserving RFC compliance.

---

## GeoDNS / latency-based routing (Route 53 / Cloudflare)

### 1. The Need for Global Traffic Steering
In global architectures, hosting all application servers in a single datacenter (e.g., North Virginia `us-east-1`) introduces massive physics-based propagation latency:
- A user in Sydney, Australia connecting to Virginia experiences **~200ms round-trip latency** purely due to the speed of light in fiber optic cables.
- If an SSL handshake requires 2 round-trips, establishing a secure connection takes nearly **half a second** before a single byte of application data is transferred!

```
[User in Tokyo] -------- 200ms WAN Ping --------> [Datacenter: us-east-1 (Virginia)]
                                                  (Terrible UX, sluggish mobile apps)

[User in Tokyo] -- 12ms --> [Datacenter: ap-northeast-1 (Tokyo)] (Optimal!)
```

### 2. How GeoDNS Works & The EDNS Client Subnet (ECS) Catch
**GeoDNS** resolves domain names to different IP addresses depending on the geographic location of the client querying the DNS server.

#### The Recursive Resolver Geolocation Flaw:
Traditional DNS servers only see the IP address of the **Recursive Resolver** (e.g., an ISP resolver or public DNS), not the actual client! If a user in London uses an open DNS resolver hosted in Texas, a naive GeoDNS server will mistakenly assume the user is in Texas and return a US IP address.

#### The Solution: EDNS0 Client Subnet (ECS — RFC 7871):
Modern recursive resolvers send an extension header containing the client's anonymized IP prefix (e.g., `/24` for IPv4: `203.0.113.0/24`). The Authoritative DNS server uses this client subnet to look up the user's true geographic location in a database (such as MaxMind GeoIP) and return the closest datacenter IP.

### 3. DNS Geolocation vs Anycast BGP Routing
In modern high-scale architectures, interviewers expect you to compare **DNS-based Routing** with **Anycast BGP Routing**:

| Routing Strategy | Mechanism | Failover Speed | Health Check Agility | Best Use Case |
|---|---|---|---|---|
| **GeoDNS** | DNS server returns different IPs based on resolver/client IP location. | Slow (Bound by DNS TTL caching; ISP resolvers may cache for hours). | Coarse-grained; dead IP removal depends on TTL expiration. | Multi-datacenter stateful routing; regional data sovereignty compliance (GDPR). |
| **Anycast (BGP)** | The **same single IP address** is advertised via BGP from hundreds of edge datacenters worldwide. Internet routers automatically send packets to the topologically closest PoP. | **Near Instantaneous (Seconds):** If a PoP fails, BGP withdraws the route, and internet routers instantly re-converge. | High; network-level failover without relying on client DNS caches. | **CDNs (Cloudflare, Akamai), DDoS protection, DNS root servers, Edge reverse proxies.** |

---

## L4 (TCP) load balancer — fast, blind to HTTP content

### 1. Transport Layer (Layer 4) Mechanics
A **Layer 4 Load Balancer** operates at the transport layer of the OSI model. It directs network traffic based solely on packet headers:
- Source and Destination **IP Addresses**.
- Source and Destination **Ports** (e.g., TCP port 443, UDP port 53).
- **Protocol** (TCP, UDP, SCTP).

An L4 load balancer is completely **content-agnostic**. It does **not** terminate TLS, does **not** read HTTP paths, and does **not** inspect cookies or headers. It acts as an ultra-high-speed packet forwarder.

```
Incoming TCP SYN: [Src: 203.0.113.5:54321 | Dst: 198.51.100.10:443]
                           |
                           v
               +-----------------------+
               |  Layer 4 Balancer     | (Hash IP 4-tuple: maps connection to Backend 2)
               +-----------------------+
                           |
                           v
Forwarded Packet: [Src: 203.0.113.5:54321 | Dst: 10.0.0.12:443]
```

### 2. High-Performance Implementations: Maglev, Katran, IPVS
Modern Tier-1 tech companies (Google, Meta, Cloudflare) do not use traditional user-space load balancers for Layer 4; user-space context switches kill throughput. Instead, they use:
- **IPVS (IP Virtual Server):** In-kernel Layer 4 transport load balancing inside Linux.
- **eBPF / XDP (eXpress Data Path):** Meta's open-source **Katran** processes packets directly at the network interface card (NIC) driver level using eBPF, bypassing the Linux kernel network stack entirely. A single commodity server can forward **tens of millions of packets per second (Mpps)**.
- **Consistent Hashing with Lookup Rings:** Google's **Maglev** assigns incoming connection flows to backend servers using a specialized consistent hashing table that maintains connection stability even when load balancer nodes crash.

### 3. Direct Server Return (DSR)
In traditional load balancing, both incoming request packets and outgoing response packets traverse the load balancer. However, internet traffic is radically asymmetric:
$$	ext{HTTP Request Size: } \sim 1 	ext{ KB (Small GET headers)} \quad \longleftrightarrow \quad 	ext{HTTP Response Size: } 5 	ext{ MB (Large video/HTML/images)}$$

If all return traffic must funnel back through the load balancer, the load balancer's network interface card saturates on egress bandwidth.

**Direct Server Return (DSR)** solves this asymmetry:
1. The client sends a request to the Virtual IP (VIP) hosted on the L4 load balancer.
2. The L4 load balancer forwards the packet to a backend worker by rewriting the Layer 2 MAC address (or using IP-in-IP encapsulation / GRE tunneling) *without modifying the destination IP in the IP header*.
3. The backend worker processes the request.
4. **The backend worker transmits the response packets directly back to the client over the internet router**, bypassing the load balancer completely!

```
[Client] ===== 1. Small Request (1 KB) =====> [L4 Load Balancer (VIP)]
   ^                                                   |
   |                                            2. Packet Forwarding
   |                                                   |
   |                                                   v
   +============= 3. Large Response (5 MB) ==== [Backend Server]
                     (Direct Server Return!)
```

---

## L7 (HTTP) load balancer — URL routing, sticky sessions, header inspection

### 1. Application Layer (Layer 7) Mechanics
A **Layer 7 Load Balancer** operates at the top of the OSI model. It terminates the incoming TCP connection, decrypts the TLS layer, and fully parses the HTTP protocol:
- Inspects **HTTP Methods** (`GET`, `POST`, `DELETE`).
- Parses **URIs and Query Strings** (`/api/v1/checkout` vs `/static/images/logo.png`).
- Reads **Headers** (`Host: payments.example.com`, `User-Agent: iOS`, `Authorization`).
- Evaluates **Cookies** (session identifiers).

Because an L7 load balancer understands application semantics, it acts as an intelligent traffic router.

### 2. Advanced Routing Capabilities
1. **Path-Based Routing:**
   - Traffic to `example.com/checkout/*` routes to the high-security Payment Service cluster.
   - Traffic to `example.com/stream/*` routes to optimized Video Streaming clusters.
2. **Host / Virtual Domain Routing:**
   A single load balancer IP can serve hundreds of domains (`site-a.com`, `site-b.com`) by inspecting the HTTP `Host` header and selecting the appropriate backend target group.
3. **Canary & Blue-Green Traffic Splitting:**
   The load balancer can route `95%` of traffic to production v1.0 and `5%` to canary v2.0 based on weighted targets or specific HTTP test headers (`X-Canary-User: true`).
4. **Sticky Sessions (Session Affinity):**
   For legacy stateful backend servers that store session data in local server RAM:
   - The L7 load balancer inspects an HTTP cookie (or injects an affinity cookie like `AWSALB=abc123xyz`).
   - All subsequent requests bearing that cookie are guaranteed to be routed to the exact same backend server.

> [!WARNING]
> **Why Sticky Sessions Break Elastic Scaling:**
> Sticky sessions violate the fundamental rule of cloud-native elasticity. If Server 3 holds sessions for heavy power users, Server 3 becomes CPU-saturated while Server 4 sits idle. Furthermore, if Server 3 crashes or auto-scales down, all active sessions on that machine are instantly destroyed.
> **Staff Engineer Best Practice:** Keep application servers completely **stateless**. Store session tokens in a distributed Redis cluster or use self-contained JWT tokens.

---

## LB algorithms: round robin, least-conn, IP hash, consistent hash, weighted

Choosing the right balancing algorithm prevents server starvation and tail-latency spikes.

### 1. Round Robin & Weighted Round Robin
- **Round Robin:** Requests are distributed sequentially: Server 1 &rarr; Server 2 &rarr; Server 3 &rarr; Server 1.
  - *When to use:* Identical backend servers handling short, uniform requests (e.g., serving static images or simple key-value reads).
- **Weighted Round Robin:** Servers are assigned integer weights based on hardware capacity. A server with 64 CPU cores receives 4x more requests than a server with 16 cores.

### 2. Least Connections & Weighted Least Connections
- **Least Connections:** Routes the new request to the server with the fewest active, concurrent TCP connections.
  - *When to use:* Long-running transactions, database queries, file uploads, or WebSocket connections where request durations vary wildly from 5 milliseconds to 10 minutes.

### 3. Power of Two Random Choices (P2C)
In high-throughput microservices, finding the absolute global least-connected server across a cluster of 500 nodes requires centralized coordination and creates mutex lock contention.
- **P2C Algorithm:** The load balancer randomly selects **two candidate servers** and picks the one with fewer active connections.
- *Mathematical Insight:* Proved by Michael Mitzenmacher, picking the best of two random choices achieves nearly the exact same load distribution as finding the global minimum, with zero shared state and $O(1)$ selection overhead!

### 4. IP Hash vs Consistent Hashing
- **Source IP Hash:** Computes a hash of the client's IP address modulo the number of servers:
  $$	ext{Target Server} = 	ext{hash}(	ext{Client\_IP}) \pmod N$$
  *Critical Flaw:* If 10,000 corporate employees access your website through a single corporate NAT proxy or VPN egress IP, **all 10,000 employees hash to the exact same server**, crashing it while other servers sit idle! Furthermore, adding a server ($N 	o N+1$) reshuffles almost all users.
- **Consistent Hashing:** Arranges servers on a $2^{32} - 1$ virtual ring. When a server joins or leaves, only $1/N$ of keys are remapped. Essential for distributed caches (Memcached, Redis) and stateful sharding.

---

## Health checks — active (ping) vs passive (track error rates)

A load balancer is only as reliable as its failure detection mechanism. If a backend server dies, sending traffic into the black hole destroys customer trust.

### 1. Active Health Checks (Synthetic Probing)
The load balancer's control plane periodically fires synthetic probes at each backend worker.
- **Configuration Parameters:**
  - **Interval:** Check every `5` seconds.
  - **Timeout:** Fail if no response within `2` seconds.
  - **Healthy Threshold:** Require `2` consecutive successes before marking a server healthy.
  - **Unhealthy Threshold:** Require `3` consecutive failures before ejecting a server from the active pool.
- **Endpoint Design (`GET /healthz`):**
  - **Shallow Health Check:** Verifies only that the local HTTP process and event loop are responsive.
  - **Deep Health Check:** Verifies local process *plus* connections to downstream databases and caches.

> [!CAUTION]
> **The Deep Health Check Cascading Outage Catastrophe:**
> Never let an active health check query your primary database (`SELECT 1 FROM users`). If your database becomes momentarily overloaded, the health check on all 100 app servers will fail. The load balancer will mark **all 100 app servers dead**, taking your entire platform completely offline!
> Health checks must verify the health of the *node itself*, not the shared infrastructure.

### 2. Passive Health Checks (Outlier Detection)
The load balancer monitors actual customer requests flowing through the system without sending artificial synthetic pings.
- **How it works (Envoy Outlier Detection):**
  - If a backend worker returns five consecutive `5xx` server error responses (or connection timeouts) on live customer traffic within a 10-second window, the load balancer temporarily **ejects** the server from the pool for 30 seconds.
  - After 30 seconds, it slowly bleeds a small fraction of traffic back to the node to test recovery.

---

## Reverse proxy — single ingress, SSL termination, request buffering

While the terms "Load Balancer" and "Reverse Proxy" are frequently used interchangeably, their architectural scopes have distinct nuances:

```
[Forward Proxy]: Sits in front of CLIENTS (e.g., Corporate VPN / Web Filter)
[Clients] ---> [Forward Proxy] ---> [The Public Internet]
(Hides client identity; enforces corporate security policies)

[Reverse Proxy]: Sits in front of SERVERS (e.g., Nginx, HAProxy, Envoy)
[The Public Internet] ---> [Reverse Proxy] ---> [Internal Backend Servers]
(Hides server identity; terminates SSL; accelerates performance)
```

### 1. SSL / TLS Termination & Offloading
Establishing an encrypted HTTPS connection requires asymmetric cryptography (RSA or Elliptic Curve Diffie-Hellman), consuming significant CPU cycles during the TLS handshake.
- The Reverse Proxy holds the SSL certificates and performs all cryptographic handshakes at the edge.
- Between the Reverse Proxy and internal backend servers, communication can flow over fast, unencrypted private VPC networks (or lightweight mTLS), freeing up backend CPU cores for core business logic.

### 2. Request & Response Buffering
Clients connecting over mobile cellular networks frequently experience packet loss and crawl at slow upload speeds (e.g., 50 KB/s on a 2 MB file upload).
- **Without Buffering:** A synchronous backend worker thread (e.g., in Python or Ruby) is held hostage for 40 seconds waiting for the slow mobile client to transmit the request body.
- **With Buffering (Nginx):** The high-performance asynchronous reverse proxy buffers the entire slow HTTP request in RAM/disk until the final byte arrives. Once complete, it sends the full request to the backend worker over local gigabit Ethernet in **0.5 milliseconds**, freeing the worker thread immediately!

### 3. Production Configuration Blueprint (Nginx)

```nginx
# High-Performance Production Reverse Proxy & Load Balancer Configuration
http {
    upstream backend_api_cluster {
        # Balancing Algorithm: Least Connections
        least_conn;
        
        server 10.0.1.10:8080 max_fails=3 fail_timeout=10s weight=2;
        server 10.0.1.11:8080 max_fails=3 fail_timeout=10s weight=1;
        server 10.0.1.12:8080 backup; # Active only if primary servers fail
        
        keepalive 64; # Maintain pooled TCP connections to backends
    }

    server {
        listen 443 ssl http2;
        server_name api.example.com;

        # SSL Configuration
        ssl_certificate /etc/ssl/certs/api_bundle.crt;
        ssl_certificate_key /etc/ssl/private/api.key;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;

        # Request Buffering to protect backends from Slowloris attacks
        proxy_buffering on;
        proxy_buffer_size 16k;
        proxy_buffers 8 32k;

        location / {
            proxy_pass http://backend_api_cluster;
            proxy_http_version 1.1;
            proxy_set_header Connection "";
            
            # Preserve original client IP & host identity
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # Timeouts
            proxy_connect_timeout 5s;
            proxy_read_timeout 15s;
        }
    }
}
```

---

> [!TIP]
> **Summary Decision Rule for System Design Interviews:**
> - Use **Anycast + GeoDNS** for global latency reduction and routing to regional edge datacenters.
> - Place an **L4 Load Balancer (e.g., Katran / AWS NLB)** at edge ingress for ultra-high packet-forwarding throughput and Direct Server Return (DSR).
> - Place an **L7 Reverse Proxy (e.g., Envoy / Nginx / AWS ALB)** behind L4 for SSL termination, path-based microservice routing, and request buffering.
> - Use **Least Connections / P2C** for variable-length requests; use **Consistent Hashing** for stateful caching.
> - Enforce **Shallow Active Health Checks** paired with **Passive Outlier Detection** to avoid cascading outages.
