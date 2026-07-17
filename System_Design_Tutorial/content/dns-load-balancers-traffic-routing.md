# DNS, Load Balancers & Traffic Routing

## Overview
How does typing `google.com` into a browser magically connect you to a server sitting in a datacenter 50 miles away?

This masterclass covers the journey of a network request: from translating a human-readable name into an IP address (DNS), to efficiently distributing that traffic across thousands of servers (Load Balancing).

---

## DNS resolution: recursive resolver → root → TLD → authoritative

DNS (Domain Name System) is the phonebook of the internet. It translates `google.com` to `142.250.190.46`.

**The 4-Step Resolution Process:**
1. **Recursive Resolver:** Your ISP (or Google's 8.8.8.8) receives your request. It checks its cache. If it doesn't know the IP, it starts the hunt.
2. **Root Name Server:** The resolver asks the Root server (the top of the internet tree). The Root says, "I don't know the IP for google.com, but I know the server in charge of all `.com` addresses. Go ask them."
3. **TLD Name Server:** The resolver asks the Top Level Domain (.com) server. The TLD says, "I don't know the exact IP, but I know the Authoritative Name Server that manages google.com. Go ask them."
4. **Authoritative Name Server:** The resolver asks the Authoritative server (usually managed by Route 53 or Cloudflare). This server holds the actual DNS record and returns `142.250.190.46`.

> [!TIP]
> **Performance Note:** This 4-step process is slow! That is why DNS relies heavily on layers of caching at the Browser level, OS level, and Router level to ensure you rarely have to do a full lookup.

---

## DNS record types: A, AAAA, CNAME, MX, TXT, NS

You must know the most common DNS records for an interview:

| Record Type | Stands For | Purpose | Example |
| :--- | :--- | :--- | :--- |
| **A** | Address | Maps a domain to an **IPv4** address. | `example.com -> 192.0.2.1` |
| **AAAA** | Quad-A | Maps a domain to an **IPv6** address. | `example.com -> 2001:db8::1` |
| **CNAME** | Canonical Name | Maps an alias domain to another domain name (never an IP). | `www.example.com -> example.com` |
| **MX** | Mail Exchange | Directs emails to your mail server. | Used to route `@example.com` emails. |
| **TXT** | Text | Arbitrary text. Used for verifying domain ownership and email security (SPF/DKIM). | `google-site-verification=12345` |
| **NS** | Name Server | Tells the internet which Authoritative server manages this domain. | `ns1.awsdns.com` |

---

## GeoDNS / latency-based routing (Route 53 / Cloudflare)

When a user in Tokyo types `netflix.com`, they should not be routed to a server in New York.

**GeoDNS** looks at the IP address of the user making the DNS request, determines their geographic location, and returns the IP address of the datacenter physically closest to them.
Alternatively, **Latency-based routing** dynamically checks which datacenter currently has the lowest network latency for that specific user and routes them there, avoiding regional network congestion.

---

## L4 (TCP) vs L7 (HTTP) Load Balancers

Once DNS returns the IP address of your Load Balancer, the Load Balancer must decide which backend server to send the traffic to.

### Layer 4 (Transport Layer) Load Balancer
- **How it works:** It only looks at the IP address and the Port (TCP/UDP).
- **Pros:** It is incredibly fast and consumes very little CPU because it doesn't look at the actual data payload. It just grabs packets and forwards them blindly.
- **Cons:** It is dumb. It cannot route traffic based on what the user is asking for.

### Layer 7 (Application Layer) Load Balancer
- **How it works:** It decrypts the TLS traffic, looks inside the HTTP request, and reads the URLs, Headers, and Cookies.
- **Pros:** Extremely smart. It can route `example.com/video` to the heavy video servers, and `example.com/api` to the fast API servers. It can also read a session cookie and always send User A to Server 1 (**Sticky Sessions**).
- **Cons:** Slower and requires more CPU because it must decrypt, inspect, and re-encrypt the data.

---

## LB algorithms: round robin, least-conn, IP hash, consistent hash

How does the Load Balancer actually pick a server?

1. **Round Robin:** Sequential. Server 1, Server 2, Server 3, Server 1... (Great if all servers and requests are equal).
2. **Least Connections:** Sends the request to the server with the fewest active connections. (Great if some requests take a long time to process, preventing one server from getting bogged down).
3. **IP Hash:** Hashes the client's IP address. This guarantees that a specific user will always be routed to the exact same server. (Useful for stateful apps, but bad if users are behind a massive corporate NAT/VPN).
4. **Consistent Hashing:** Used primarily for distributing data across caches or database shards. Ensures that if a server is added or removed, only a small fraction of keys need to be re-mapped.

---

## Health checks — active (ping) vs passive (track error rates)

A Load Balancer is useless if it sends traffic to a dead server.

- **Active Health Checks:** The LB constantly pings a specific endpoint on the backend server (e.g., `GET /health` every 5 seconds). If it gets a 200 OK, the server is healthy. If it gets a 500 or times out 3 times in a row, the LB removes the server from the rotation.
- **Passive Health Checks:** The LB doesn't send pings. Instead, it monitors the actual traffic. If it notices that Server A is suddenly returning 5xx errors for normal user requests, it ejects Server A.

> [!NOTE]
> **Reverse Proxy:** A Reverse Proxy is often synonymous with an L7 Load Balancer (like Nginx or HAProxy). Its job is to sit in front of your servers, terminate SSL/TLS to save backend CPU, buffer slow client uploads, and protect your internal IP addresses from the public internet.
