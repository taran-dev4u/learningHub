# CDN Caching: Delivering Content at the Edge

A **Content Delivery Network (CDN)** is a globally distributed network of proxy servers designed to deliver content to users faster by serving it from a location geographically closest to them.

If your core servers are in Virginia, USA, a user in Tokyo will experience at least 150ms of network latency (the speed of light through fiber optics) just to establish a connection. A CDN solves this by placing caching servers in Tokyo.

Let's break down the strategies for managing content on these global edge networks.

---

## 1. Pull CDN (Lazy Loading)
### The "Fetch on Demand" Strategy

In a **Pull CDN** configuration, the CDN acts similarly to a Cache-Aside system. The CDN is empty by default. It "pulls" the content from your central server (the Origin) only when a user requests it.

**How it works:**
1. A user requests `image.png` from the CDN.
2. **Cache Miss:** The CDN does not have the file. It forwards the request to your Origin server.
3. The Origin returns the image to the CDN.
4. The CDN stores a copy (respecting the TTL headers) and sends the image to the user.
5. The next user who requests `image.png` gets the cached copy instantly.

**Pros & Cons:**
| Pros | Cons |
| :--- | :--- |
| **Low Maintenance:** You don't have to manage uploading files to the CDN. It just works automatically. | **Cold Starts:** The very first user in every geographic region experiences higher latency because of the initial cache miss. |
| **Storage Efficient:** The CDN only caches files that are actively requested by users. | **Redundant Traffic:** If a file expires from the CDN, the next request will hit your Origin server again. |

**Best For:** Heavy-traffic sites with massive amounts of dynamically generated media (e.g., user avatars, millions of product images).

---

## 2. Push CDN (Pre-Warming)
### The "Stock the Shelves" Strategy

In a **Push CDN**, the application engineers take active responsibility for pushing content to the CDN *before* any user requests it. Your build pipeline or backend services upload the files directly to the CDN's storage layer.

**How it works:**
1. You deploy a new version of your website.
2. Your CI/CD pipeline pushes `main.js` and `styles.css` to the CDN.
3. The CDN proactively replicates these files to all its servers globally.
4. When users request the site, the cache is 100% warm. There are no cache misses.

**Pros & Cons:**
| Pros | Cons |
| :--- | :--- |
| **Zero Cold Starts:** Maximum performance. Every user gets a cache hit from day one. | **High Complexity:** Your backend must manage the upload logic and handle failures. |
| **Origin Shielding:** Your origin server receives zero traffic for these static assets. | **Wasted Storage:** You pay the CDN to store and replicate files that users might never actually request. |

**Best For:** Small to medium static assets, critical CSS/JS bundles, or releasing major updates (like a highly anticipated video game patch).

---

## 3. Cache Invalidation Strategies
### Purging the Global Network

When a file changes at your Origin, the CDN doesn't magically know. If you update your company logo but keep the filename `logo.png`, the CDN will continue serving the old logo until its TTL expires. You have two options to fix this:

**Strategy A: URL Versioning (Recommended)**
Never update files in place. If you change a file, change its name.
- Old: `logo_v1.png`
- New: `logo_v2.png` (or append a hash: `logo.a3f9b.png`)
When your HTML requests the new URL, the CDN treats it as a brand new file, resulting in an immediate cache miss and pulling the fresh file. This entirely sidesteps the invalidation problem.

**Strategy B: Purge API**
If you *must* use the same URL (e.g., a live `index.html`), you can call the CDN's Purge/Invalidation API.
- You send an API call to Cloudflare: `DELETE /purge?url=site.com/logo.png`.
- The CDN propagates this delete command to hundreds of servers worldwide.
- *Warning:* Purging is slow (can take minutes globally) and expensive for the CDN provider.

---

## 4. CDN for Dynamic Content
### Pushing Logic to the Edge

Historically, CDNs only cached static files (images, CSS, JS). Modern CDNs (Cloudflare, Fastly, AWS CloudFront) can cache **Dynamic Content** and even execute code.

**Caching API Responses:**
You can configure a CDN to cache JSON responses from your REST API. If you have a `/api/top-10-movies` endpoint that updates daily, you can set the `Cache-Control` HTTP header to `max-age=3600`. The CDN will intercept the API call, cache the JSON string, and serve it directly to users, absorbing massive amounts of API traffic.

**Edge Workers / Edge Computing:**
You can deploy lightweight JavaScript/WASM functions directly onto the CDN servers (e.g., Cloudflare Workers).
Instead of sending a user back to your Origin to determine their geographic language preference, the Edge Worker executes a 2ms script in Tokyo, inspects the user's IP, and rewrites the request to fetch the Japanese version of the site directly from the edge cache.

---

> [!NOTE]
> ### 🎓 Teacher FAQ & Common Beginner Mistakes
>
> **Q: "If a Push CDN pushes to all servers, why does a Pull CDN have regional cold starts?"**
> Excellent question! A CDN is not one giant server; it is hundreds of independent PoPs (Points of Presence) around the world. In a Pull setup, if a user in London requests `image.png`, the London PoP pulls it and caches it. But if an hour later, a user in Sydney requests the same `image.png`, the Sydney PoP doesn't know London has it. Sydney experiences a cache miss and pulls it from your Origin.
>
> **Q: "Why should I bother with a CDN if my app is hosted on AWS in multiple regions?"**
> Multi-region AWS deployment is complex and expensive. You have to replicate databases, manage global load balancing, and handle cross-region synchronization. A CDN is a massive shortcut. By putting a CDN in front of a *single-region* AWS setup, you achieve 90% of the latency benefits for static/cached data with a fraction of the engineering effort.
