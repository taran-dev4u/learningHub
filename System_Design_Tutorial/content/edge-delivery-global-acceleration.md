# Edge Delivery & Global Acceleration

> **Masterclass Lecture**: Global Request Distribution, Edge Computing, and Dynamic Acceleration  
> **Target Audience**: Staff Engineer / Distributed Systems Architect  
> **Reading Time**: ~45 minutes

Moving beyond basic static file caching, **Edge Delivery** represents the frontier of modern distributed systems. It is about pushing logic, routing decisions, and security out of centralized data centers and onto the "Edge"—the networking nodes geographically closest to the end user.

Whether architecting Netflix's multi-terabit video distribution, Cloudflare's global DDoS mitigation network, or Uber's real-time ride tracking, understanding edge topologies, BGP Anycast, tiered cache shielding, and dynamic protocol acceleration is mandatory for senior and staff engineering interviews.

---

## CDN Architecture (PoPs, Origin Shield)

### Physical Infrastructure: Inside a Point of Presence (PoP)

To understand Edge Delivery, we must first examine the physical reality of the internet. The internet is not a monolithic cloud; it is a federation of thousands of independent **Autonomous Systems (AS)** connected at **Internet Exchange Points (IXPs)**.

```
+-----------------------------------------------------------------------------------+
|                            GLOBAL ANYCAST NETWORK                                 |
|                                                                                   |
|  [ User in Tokyo ]       [ User in London ]          [ User in São Paulo ]        |
|         │                        │                            │                   |
|         ▼                        ▼                            ▼                   |
|   ┌───────────┐            ┌───────────┐                ┌───────────┐             |
|   │ Tokyo PoP │            │London PoP │                │SP PoP     │             |
|   │ (Edge)    │            │ (Edge)    │                │ (Edge)    │             |
|   └─────┬─────┘            └─────┬─────┘                └─────┬─────┘             |
|         │                        │                            │                   |
|         └───────────────┐        │       ┌────────────────────┘                   |
|                         ▼        ▼       ▼                                        |
|                     ┌─────────────────────────┐                                   |
|                     │   Origin Shield PoP     │  (Tier-2 Regional Cache)          |
|                     │   (e.g., US-East / EU)  │                                   |
|                     └────────────┬────────────┘                                   |
|                                  │  Private Backbone / Dedicated Fiber            |
|                                  ▼                                                |
|                     ┌─────────────────────────┐                                   |
|                     │   Core Origin Fleet     │  (AWS us-east-1 / GCP Datacenter) |
|                     │   API Servers & DBs     │                                   |
|                     └─────────────────────────┘                                   |
+-----------------------------------------------------------------------------------+
```

#### How Anycast BGP Works Under the Hood
In a traditional Unicast network, every IP address maps to a single physical machine or load balancer in one datacenter. If a user in Sydney accesses an IP hosted in North Virginia, packets must traverse the trans-Pacific undersea cables (~170ms one-way latency).

In an **Anycast** architecture:
1. The CDN provider announces the **exact same IP prefix** (e.g., `104.16.0.0/12`) from hundreds of edge datacenters worldwide via Border Gateway Protocol (BGP) to Tier-1 telecom transit providers.
2. When the user's ISP router looks up where to send packets destined for that IP, BGP selects the path with the shortest AS-Hop count.
3. The Sydney user routes directly to the Sydney PoP (3ms RTT), while the Frankfurt user routes to the Frankfurt PoP (2ms RTT).

#### The Internal Architecture of an Edge PoP
Each PoP is not just a hard drive with files; it is a high-density, multi-layer proxy cluster:
1. **L4 Load Balancer (e.g., Maglev / Katran):** Uses consistent hashing with ECMP (Equal-Cost Multi-Path) to distribute raw TCP/UDP packets across edge proxy nodes without connection state synchronization.
2. **L7 Proxy Engine (e.g., Nginx, Envoy, or Pingora):** Terminates TLS, inspects HTTP headers, evaluates edge worker rules, and negotiates protocols (HTTP/1.1, HTTP/2, HTTP/3 QUIC).
3. **Multi-Tiered Cache Storage:**
   - **L1 RAM Cache:** Extremely hot assets (top 1% popular objects), sub-millisecond retrieval.
   - **L2 NVMe SSD Array:** High-capacity local cache (terabytes of static assets, images, video segments).

---

### The Origin Shield Pattern: Protecting Core Infrastructure

Imagine a CDN with **300 global PoPs**. Suppose your application publishes a breaking news video or a new software release.

> [!WARNING]
> **The Origin Cache Stampede Disaster:**  
> If an asset is not yet cached globally, a simultaneous request from users across all 300 PoPs causes every single edge server to independently forward a cache miss back to your core origin datacenter.  
> 300 PoPs $\times$ 1,000 requests/sec = **300,000 RPS slamming your origin database simultaneously!**

```
WITHOUT ORIGIN SHIELD (Fan-Out Inundation):
[PoP 1] ─── Miss ───┐
[PoP 2] ─── Miss ───┼───▶ [ 300 Concurrent Misses ] ───▶ [ Origin DB Crashes ]
[PoP 300] ── Miss ──┘

WITH ORIGIN SHIELD (Tiered Coalescing):
[PoP 1] ─── Miss ───┐
[PoP 2] ─── Miss ───┼───▶ [ Origin Shield PoP ] ───▶ [ Exactly 1 Miss ] ───▶ [ Origin Safe ]
[PoP 300] ── Miss ──┘           │ (Collapses 299 duplicate
                                │  requests into 1 fetch)
```

#### How Origin Shield Solves This:
1. **Tiered Distribution:** The edge PoPs are configured with a parent-child relationship. Edge PoPs (children) do not talk directly to the customer origin; they query a designated **Origin Shield PoP** (parent) located geographically adjacent to the origin cloud region (e.g., AWS `us-east-1`).
2. **Request Coalescing (Collapse Forward):** When 50 edge PoPs request the same missing object concurrently, the Origin Shield holds 49 requests in a waiting queue and issues **exactly one request** to the origin. Once the response arrives, the Origin Shield fans it out to all waiting edge PoPs and stores it in its own regional cache.

---

### Quantitative Performance: Formulas to Memorize

#### 1. Effective Latency ($L_{eff}$)
$$L_{eff} = \text{CHR} \cdot L_{edge} + (1 - \text{CHR}) \cdot L_{origin}$$
Where:
- $\text{CHR}$: Cache Hit Ratio (e.g., $0.95 = 95\%$)
- $L_{edge}$: Round-trip time to local Edge PoP (typically $5\text{ms} - 20\text{ms}$)
- $L_{origin}$: Round-trip time to centralized cloud origin (typically $150\text{ms} - 250\text{ms}$)

*Example:* If $CHR = 98\%$, $L_{edge} = 10\text{ms}$, and $L_{origin} = 200\text{ms}$:
$$L_{eff} = (0.98 \times 10) + (0.02 \times 200) = 9.8 + 4 = 13.8\text{ms}$$
*Without CDN ($CHR = 0\%$):* Latency is **$200\text{ms}$** (over $14\times$ slower!).

#### 2. Origin Offload & Egress Cost Savings
$$\text{Offload \%} = \frac{\text{Bytes Delivered by CDN} - \text{Bytes Fetched from Origin}}{\text{Bytes Delivered by CDN}} \times 100$$
Cloud providers (AWS/GCP/Azure) charge steep egress fees ($\$0.08 - \$0.12$ per GB) for data exiting their regions. Origin shields and high edge hit ratios regularly reduce infrastructure egress bills by $80\% - 95\%$.

---

## Edge Cache Invalidation Strategies

Caching is easy; invalidation is notoriously one of the two hard problems in computer science. Stale data served from an edge node can cause checkout failures, privacy leaks, or broken user experiences.

### Invalidation Mechanisms Compared

| Strategy | Propagation Time | Origin Load | Use Case | Implementation Mechanism |
|---|---|---|---|---|
| **Hard Purge by URL** | $150\text{ms} - 5\text{s}$ | High (next request misses) | Critical bug fixes, security patch assets | HTTP `PURGE` request to CDN API |
| **Soft Purge (Stale-While-Revalidate)** | $150\text{ms}$ | Minimal (async background fetch) | News articles, catalog items, social feeds | RFC 5861 `stale-while-revalidate` |
| **Surrogate Keys / Cache-Tags** | $< 150\text{ms}$ | Selective & precise | E-commerce inventory, blog updates | HTTP Header `Surrogate-Key` or `Cache-Tag` |
| **URL Versioning / Content Hashing** | $0\text{ms}$ (Instant) | Zero (never invalidates) | JS/CSS bundles, media assets | `main.8f4a1c.js` with `Cache-Control: immutable` |

---

### Surrogate Keys (Cache-Tags) in Depth

In an e-commerce platform like Shopify or Amazon, a single product update (e.g., price drop from $\$99$ to $\$79$) affects dozens of cached pages:
1. The product detail page: `/products/nike-air-max`
2. The category page: `/category/running-shoes`
3. The brand page: `/brand/nike`
4. The search results: `/search?q=shoes`
5. The homepage featured carousel: `/`

Purging all these URLs individually by path is brittle and error-prone.

```
+------------------------------------------------------------------------------------+
|                         SURROGATE KEY / CACHE-TAG FLOW                             |
|                                                                                    |
|  1. Origin Response with Tags:                                                     |
|     HTTP/2 200 OK                                                                  |
|     Content-Type: text/html                                                        |
|     Cache-Control: public, max-age=86400                                           |
|     Surrogate-Key: product-1094 category-shoes brand-nike                         |
|                                                                                    |
|  2. CDN Edge stores HTML and indexes tags:                                         |
|     Tag "product-1094" -> [/products/nike-air-max, /category/shoes, /brand/nike] |
|                                                                                    |
|  3. Merchant updates price in Postgres:                                            |
|     Backend emits event: EventBus.publish("product_updated", id=1094)             |
|                                                                                    |
|  4. CDN Invalidation Worker calls Fastly/Cloudflare API:                           |
|     POST https://api.cdn.com/purge                                                 |
|     Headers: { "Key": "product-1094" }                                            |
|                                                                                    |
|  5. Result: All 3 cached pages invalidated across 300 PoPs within 150 milliseconds!|
+------------------------------------------------------------------------------------+
```

---

### RFC 5861: Stale-While-Revalidate & Stale-If-Error

Traditional caching suffers from the **Cache Eviction Spike**: the millisecond an item's TTL expires, the next user experiences a slow response while the edge waits for the origin.

RFC 5861 eliminates this latency spike entirely using two directives:

```http
Cache-Control: public, max-age=60, stale-while-revalidate=600, stale-if-error=86400
```

```
Timeline (Seconds):
0s                    60s                                            660s
├──────────────────────┼───────────────────────────────────────────────┤
│ Fresh Window         │ Stale-While-Revalidate Window                 │ Dead / Expired
│ (Serve from Edge)    │ 1. Serve stale cache INSTANTLY to user (10ms) │ Must block &
│                      │ 2. Edge triggers ASYNC fetch to origin        │ fetch from
│                      │ 3. Future users get updated fresh copy        │ origin (200ms)
```

1. **`max-age=60`**: For the first 60 seconds, the response is fresh.
2. **`stale-while-revalidate=600`**: Between second 60 and second 660, if a user requests this item, the edge **immediately returns the cached (stale) version in 5ms**. In the background, the edge proxy asynchronously fires a revalidation request to the origin. Once updated, subsequent users receive the fresh version. The user **never** experiences origin latency!
3. **`stale-if-error=86400`**: If your origin database crashes or returns `500 Internal Server Error` within 24 hours, the edge continues serving the last known good cached response rather than showing an error page.

---

## Static vs Dynamic Acceleration

Engineers often mistakenly assume CDNs are only for static image files, CSS, and video chunks. Modern distributed networks accelerate **fully dynamic, non-cacheable API calls** (e.g., `POST /api/v1/checkout` or `GET /api/v1/user/profile`).

### Dynamic Content Acceleration (DSA) Techniques

Even when the response payload cannot be cached for a single second, routing traffic through an edge network is drastically faster than routing over the public internet:

```
PUBLIC INTERNET (Slow, Congested, Many BGP Hops):
User (Tokyo) ──[ Unreliable Public BGP Routers ]──▶ Origin (Virginia)
Latency: 220ms RTT | Packet Loss: 2.1% | Slow TCP Slow-Start Window

DYNAMIC SITE ACCELERATION (Edge Termination & Private Fiber Backbone):
User (Tokyo) ──(5ms)──▶ [Tokyo Edge PoP] ═══════ Private Backbone ═══════▶ Origin (Virginia)
                             ▲                      (Optimized TCP,
                     TLS Handshake Here             Pre-warmed Connections,
                     (1-RTT saved locally)          Zero Packet Loss)
```

#### 1. Edge Connection Termination & TLS 1.3 Offloading
- Over the public internet, establishing a secure connection to Virginia from Tokyo requires:
  - DNS resolution: 1 RTT
  - TCP 3-Way Handshake: 1 RTT
  - TLS 1.3 Handshake: 1 RTT
  - **Total before 1 byte of application data is sent: 3 RTTs $\approx 600\text{ms}$!**
- With Dynamic Acceleration:
  - The TCP and TLS handshakes terminate at the **local Tokyo PoP** ($10\text{ms}$).
  - The request is then forwarded over an **already open, pre-warmed connection pool** to the origin.
  - Connection startup drops from $600\text{ms}$ to **$20\text{ms}$**!

#### 2. Private Backbone Route Optimization
The public internet routes packets based on commercial peering agreements between ISPs (BGP "hot potato routing"), which often takes circuitous physical paths. Major CDN backbones (Cloudflare, AWS CloudFront, Fastly) route traffic across private leased dark fiber with optimized BGP peering, avoiding congestion hotspots and reducing packet drops to near zero.

#### 3. Edge Computing (Cloudflare Workers, Fastly Compute@Edge, AWS Lambda@Edge)
Instead of executing application code in a central cloud region, lightweight V8 isolates or WebAssembly (Wasm) runtimes run logic inside the Edge PoP:

```typescript
// Example: Edge Worker validating JWT and routing without hitting Origin
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const authHeader = request.headers.get("Authorization");
    if (!authHeader) {
      return new Response("Unauthorized", { status: 401 });
    }

    // Validate HMAC-SHA256 signature locally at the edge in 0.5ms
    const isValid = await verifyJwtLocally(authHeader, env.JWT_SECRET);
    if (!isValid) {
      return new Response("Invalid Token", { status: 403 });
    }

    // Inspect user country from edge metadata and route to regional origin
    const country = request.cf?.country || "US";
    const backendOrigin = country === "JP" ? env.ORIGIN_TOKYO : env.ORIGIN_US;

    return fetch(backendOrigin, request);
  }
};
```

---

## Signed URLs and Token Auth

How do platforms like Netflix, Spotify, or Coursera serve private, paid video content from public edge CDN nodes without allowing unauthorized users to pirate the streams?

### Architecture of Signed URLs

A **Signed URL** (or Signed Cookie) embeds cryptographic authentication parameters into the query string, allowing the edge cache to verify access **without querying the origin authentication database**.

```
+------------------------------------------------------------------------------------+
|                             SIGNED URL LIFECYCLE                                   |
|                                                                                    |
|  1. Client Requests Video Access:                                                  |
|     Client ──▶ POST /api/v1/movies/42/watch ──▶ [ Auth Service / Origin ]          |
|                                                                                    |
|  2. Origin Validates Subscription & Generates Signed URL:                          |
|     - Asset Path: /hls/video_42_1080p.m3u8                                        |
|     - Expires: 1730000000 (valid for 2 hours)                                      |
|     - Client IP restriction: 203.0.113.19 (optional)                               |
|     - Signature: HMAC-SHA256(Path + Expires + IP, SecretKey)                       |
|                                                                                    |
|  3. Origin Returns URL to Client:                                                  |
|     https://cdn.movies.com/hls/video_42.m3u8?Expires=1730000000&Signature=9a7f...  |
|                                                                                    |
|  4. Client requests video segment directly from Edge PoP:                          |
|     Client ──▶ GET /hls/video_42.m3u8?Expires=... ──▶ [ Local Edge PoP ]          |
|                                                              │                     |
|  5. Edge PoP validates signature locally:                    │                     |
|     - Is current_time < Expires? (Yes)                       ▼                     |
|     - Does HMAC match local SecretKey? (Yes) ────────▶ [ Serve 4K Video Segment   |
|     (Origin is never contacted!)                         from Local NVMe SSD! ]    |
+------------------------------------------------------------------------------------+
```

### Python Implementation: Generating & Verifying Signed URLs

```python
import hmac
import hashlib
import time
from urllib.parse import urlencode

SECRET_KEY = b"shared-cdn-master-secret-key-faang-level"

def generate_signed_url(base_url: str, path: str, ttl_seconds: int = 3600, client_ip: str = None) -> str:
    """Generates a tamper-proof edge-verifiable URL."""
    expires = int(time.time()) + ttl_seconds
    
    # Canonical string to sign
    payload = f"{path}|{expires}"
    if client_ip:
        payload += f"|{client_ip}"
        
    signature = hmac.new(SECRET_KEY, payload.encode("utf-8"), hashlib.sha256).hexdigest()
    
    params = {"expires": expires, "sig": signature}
    if client_ip:
        params["ip"] = client_ip
        
    return f"{base_url}{path}?{urlencode(params)}"

def verify_signed_url_at_edge(path: str, expires: int, signature: str, client_ip: str = None) -> bool:
    """Executed by Edge Proxy (Envoy/Nginx/Worker) in < 1ms without database calls."""
    # 1. Check expiration
    if time.time() > expires:
        return False  # Expired token
        
    # 2. Recompute expected HMAC
    payload = f"{path}|{expires}"
    if client_ip:
        payload += f"|{client_ip}"
        
    expected_sig = hmac.new(SECRET_KEY, payload.encode("utf-8"), hashlib.sha256).hexdigest()
    
    # 3. Constant-time comparison to prevent timing attacks
    return hmac.compare_digest(expected_sig, signature)
```

---

## Real-World Failure Modes & Mitigations

### 1. Clock Skew Authentication Rejections
- **Symptom:** Users in certain regions receive intermittent `403 Forbidden` on valid signed URLs.
- **Root Cause:** Origin server clock is 30 seconds ahead of CDN Edge PoP clocks due to unsynchronized NTP servers.
- **Mitigation:**
  - Always enforce automated NTP daemon sync (Chrony) across all servers.
  - Implement a **grace window** (e.g., allow $\pm 60\text{s}$ tolerance) when validating time-based signatures.

### 2. The Cascading Cache Invalidation Storm
- **Symptom:** An engineer pushes a full CDN purge command (`PURGE /*`) during peak traffic hours. Origin CPU immediately hits $100\%$ and the primary database fails over.
- **Root Cause:** Purging the entire cache removes all shield buffers; millions of active users slam origin simultaneously.
- **Mitigation:**
  - **Soft Purge Only:** Mark assets as stale rather than purging them from disk; allow edge to serve stale content while revalidating gradually.
  - **Rate-Limited Purges:** Throttle invalidation propagation across PoPs over 5–10 minutes.
  - **Origin Shield Request Coalescing:** Ensure parent tier strictly bounds origin concurrency.

---

## Teacher FAQ & Common Interview Doubts

> [!NOTE]
> **Doubts Answered by Staff Engineers**

### Q1: "Can we cache personalized API responses (e.g., user account profile) on a CDN?"
**Answer:** Yes, using **Private Cache Keys** or **Edge Workers**.  
While you should never cache personalized responses under a generic URL (`/api/me`) with `Cache-Control: public`, you can:
1. Cache with a custom cache key combining URL + User ID: `cache_key = (request.url, jwt.sub)`.
2. Use **Edge Side Includes (ESI)** or micro-frontends: The edge caches the static layout shell (95% of HTML) and dynamically injects the small personalized snippet (user avatar, cart count) via an edge worker subrequest.

### Q2: "What is the difference between Anycast DNS and Anycast BGP?"
**Answer:**  
- **Anycast DNS:** Only the DNS query itself routes to the nearest DNS server (e.g., Google's `8.8.8.8` or Cloudflare's `1.1.1.1`). Once resolved, the client connects to whatever Unicast IP address the DNS returned.
- **Anycast BGP for HTTP:** Both the DNS resolution **and** the actual HTTP/TCP/TLS data packets route directly to the nearest physical PoP using the identical IP address.

### Q3: "What numbers must I memorize for edge networking in interviews?"
**Metrics to have on the tip of your tongue:**
- Edge PoP Round-Trip Time (RTT): **$5\text{ms} - 20\text{ms}$**
- Cross-Continental / Trans-Oceanic RTT: **$150\text{ms} - 250\text{ms}$**
- Edge Cache Purge Propagation SLA: **$< 150\text{ms}$** (modern Fastly/Cloudflare), vs **$1 - 5\text{min}$** (legacy Akamai/CloudFront)
- Target Static Cache Hit Ratio: **$> 95\%$**
- Target Dynamic API Cache Hit Ratio: **$> 60\% - 80\%$** (via `stale-while-revalidate`)
- TLS 1.3 0-RTT Session Resumption: Saves **1 full RTT** on repeat visits
