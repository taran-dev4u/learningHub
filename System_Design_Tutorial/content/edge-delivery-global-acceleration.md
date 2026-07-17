# Edge Delivery & Global Acceleration

Moving beyond basic static file caching, **Edge Delivery** represents the frontier of modern distributed systems. It is about pushing logic, routing decisions, and security out of your centralized data centers and into the "Edge"—the networking nodes geographically closest to the end user.

If you want to design a system like Netflix, TikTok, or Uber, understanding the architecture of global acceleration is mandatory.

---

## 1. CDN Architecture
### PoPs and Origin Shields

To understand Edge Delivery, you must understand the physical architecture of these networks.

**PoPs (Points of Presence):**
A CDN provider (like Akamai or Fastly) leases rack space in internet exchange points around the world. These data centers are called PoPs. When a user in Mumbai types your URL, DNS routes them to the Mumbai PoP. The PoP contains proxy servers, cache storage, and edge compute nodes.

**The Origin Shield Pattern:**
Imagine you have 200 PoPs globally. If a viral video is requested simultaneously across the world, all 200 PoPs experience a cache miss and send 200 requests to your central Origin server in Ohio.
To protect your database, CDNs implement an **Origin Shield** (a mid-tier cache).
1. The 200 PoPs check their local cache (Miss).
2. All 200 PoPs forward the request to the Origin Shield (a massive, centralized CDN node near your Origin).
3. The Shield experiences *one* cache miss, fetches it from your Origin once, and distributes it to the 200 PoPs.

---

## 2. Edge Cache Invalidation Strategies
### Surrogate Keys & Stale-While-Revalidate

We discussed basic URL versioning in the CDN section. At the Edge, we use much more sophisticated HTTP headers.

**Surrogate Keys (Cache Tags):**
When your API returns a JSON response for an article, you can attach a hidden header: `Surrogate-Key: article_123, author_55`.
If the author updates their name, you issue a single API call to the CDN: `PURGE /tags/author_55`. The CDN instantly drops *every single cached response* that contained that tag across the globe. This allows granular invalidation of complex data graphs without purging the whole site.

**Stale-While-Revalidate (SWR):**
A powerful HTTP Cache-Control extension: `Cache-Control: max-age=60, stale-while-revalidate=86400`.
- **0–60s:** CDN serves fresh cache.
- **61s–24hrs (Stale Window):** User requests data. The CDN immediately serves the *stale* cached data (zero latency for the user!). Then, in the background, the CDN asynchronously fetches the fresh data from the Origin and updates the cache.
This guarantees the user never experiences a slow cache-miss, at the cost of occasionally seeing slightly outdated data.

---

## 3. Static vs Dynamic Acceleration
### Accelerating the Uncacheable

What if the data cannot be cached at all? (e.g., A real-time stock trade, or a multiplayer game move). You still use an Edge Network, but for **Dynamic Acceleration**.

**TCP Termination at the Edge:**
Creating a secure TLS connection requires 3 network round-trips (TCP handshake + TLS handshake).
- **Without Edge:** A user in Sydney making a TLS connection to New York (150ms ping) takes `3 * 150ms = 450ms` just to say hello.
- **With Edge Acceleration:** The user connects to the Sydney PoP (10ms ping). The TLS handshake takes `3 * 10ms = 30ms`. The Sydney PoP then uses a massive, pre-warmed, persistent fiber-optic connection (often a private backbone, bypassing the public internet) to forward the data to New York. The connection is drastically faster and more stable.

**Anycast Routing:**
CDNs use BGP Anycast. Instead of DNS returning different IP addresses for different regions, Anycast allows 100 different servers globally to advertise the *exact same IP address*. The internet backbone automatically routes the user's packets to the physically closest server advertising that IP.

---

## 4. Signed URLs and Token Auth
### Security at the Edge

If you are Netflix, you want to cache video files on the CDN for performance, but you absolutely cannot let non-paying users access those direct CDN URLs.

**How it works (Signed URLs):**
1. A paying user logs into your backend.
2. The backend generates a temporary URL to the video file on the CDN, appended with a cryptographic signature and an expiration timestamp:
   `cdn.netflix.com/movie.mp4?expires=169000&signature=X8f9a2B`
3. The user's browser requests this URL from the Edge PoP.
4. The Edge PoP uses a shared public key to verify the signature. If valid and not expired, it serves the cached video. If someone shares this link on Reddit, it will expire 5 minutes later, rendering it useless.

This pushes the heavy burden of authorization away from your origin servers and onto the edge compute layer.

---

> [!NOTE]
> ### 🎓 Teacher FAQ & Common Beginner Mistakes
>
> **Q: "If Anycast routes users to the closest server, why do we need GeoDNS?"**
> Anycast operates at the Network Layer (L3) and routes based on network topology (fewest hops), not necessarily geographic distance. Occasionally, routing anomalies can send a user in Texas to a PoP in Europe. GeoDNS operates at the Application Layer (L7) and looks up the user's IP to explicitly hand them the IP address of the Texas server. Modern global networks often use a combination of both.
>
> **Q: "Why can't I just use Edge Workers (Lambda@Edge) as my entire backend?"**
> You can, for very simple apps! But Edge Workers are stateless and have severe limitations on execution time (often capped at 10-50ms) and memory. Furthermore, they are far away from your primary database. If an Edge Worker in Sydney has to query a PostgreSQL database in Virginia, you've completely negated the latency benefit of the edge. Edge compute is for lightweight transformations, auth, and routing—not heavy data processing.
