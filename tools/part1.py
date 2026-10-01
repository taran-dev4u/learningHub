# -*- coding: utf-8 -*-
# Curated System Design roadmap resources — part 1 (lessons 1-31).
# Format: file.md -> {"videos": [[id, title, channel]], "docs": [[label, url]]}
L1 = {
"requirements-scope.md": {"videos": [], "docs": [
  ["AlgoMaster — How to answer a system design question", "https://algomaster.io/learn/system-design-interviews/answering-framework"],
  ["Hello Interview — System design in a hurry: requirements", "https://www.hellointerview.com/learn/system-design/in-a-hurry/delivery"],
  ["System Design Primer — Step 1: outline use cases and constraints", "https://github.com/donnemartin/system-design-primer#step-1-outline-use-cases-constraints-and-assumptions"]]},

"capacity-estimation.md": {"videos": [], "docs": [
  ["Latency numbers every programmer should know", "https://gist.github.com/jboner/2841832"],
  ["Interactive latency numbers (by year)", "https://colin-scott.github.io/personal_website/research/interactive_latency.html"],
  ["System Design Primer — Back-of-the-envelope calculations", "https://github.com/donnemartin/system-design-primer#back-of-the-envelope-calculations"]]},

"architecture-diagrams-communication.md": {"videos": [], "docs": [
  ["The C4 model for software architecture", "https://c4model.com/"],
  ["Martin Fowler — Software architecture guide", "https://martinfowler.com/architecture/"],
  ["AWS architecture icons and diagram conventions", "https://aws.amazon.com/architecture/icons/"]]},

"5-step-interview-framework.md": {"videos": [], "docs": [
  ["AlgoMaster — Answering framework", "https://algomaster.io/learn/system-design-interviews/answering-framework"],
  ["Hello Interview — System design in a hurry", "https://www.hellointerview.com/learn/system-design/in-a-hurry/introduction"],
  ["System Design Primer — How to approach a system design interview", "https://github.com/donnemartin/system-design-primer#how-to-approach-a-system-design-interview-question"]]},

"senior-engineer-signals.md": {"videos": [], "docs": [
  ["Google SRE Book — Embracing risk", "https://sre.google/sre-book/embracing-risk/"],
  ["AWS Builders' Library — Challenges with distributed systems", "https://aws.amazon.com/builders-library/challenges-with-distributed-systems/"],
  ["Martin Fowler — Architectural trade-offs (Software Architecture Guide)", "https://martinfowler.com/architecture/"]]},

"reference-numbers-estimation-cheat-sheet.md": {"videos": [], "docs": [
  ["Latency numbers every programmer should know", "https://gist.github.com/jboner/2841832"],
  ["Interactive latency numbers (by year)", "https://colin-scott.github.io/personal_website/research/interactive_latency.html"],
  ["AlgoMaster — Latency vs throughput vs bandwidth", "https://algomaster.io/learn/system-design/latency-vs-throughput"]]},

"latency-throughput-scalability-basics.md": {"videos": [], "docs": [
  ["AlgoMaster — Scalability", "https://algomaster.io/learn/system-design/scalability"],
  ["AlgoMaster — Vertical vs horizontal scaling", "https://algomaster.io/learn/system-design/vertical-vs-horizontal-scaling"],
  ["AWS — Throughput vs latency", "https://aws.amazon.com/compare/the-difference-between-throughput-and-latency/"],
  ["Universal Scalability Law (Gunther)", "https://en.wikipedia.org/wiki/Neil_J._Gunther#Universal_Law_of_Computational_Scalability"]]},

"availability-reliability-slas.md": {"videos": [], "docs": [
  ["AlgoMaster — Availability", "https://algomaster.io/learn/system-design/availability"],
  ["Google SRE Book — Service level objectives", "https://sre.google/sre-book/service-level-objectives/"],
  ["Cockroach Labs — What is fault tolerance?", "https://www.cockroachlabs.com/blog/what-is-fault-tolerance/"],
  ["AlgoMaster — Single point of failure", "https://algomaster.io/learn/system-design/single-point-of-failure-spof"]]},

"consistency-models.md": {"videos": [["LAsMrghdFP0", "Eventual Consistency vs. Strong Consistency — how to decide", "Think Software"]], "docs": [
  ["Jepsen — Consistency models map", "https://jepsen.io/consistency"],
  ["AlgoMaster — Strong vs eventual consistency", "https://blog.algomaster.io/p/strong-vs-eventual-consistency"],
  ["Kleppmann — Linearizability vs serializability", "https://www.bailis.org/blog/linearizability-versus-serializability/"]]},

"cap-pacelc-theorems.md": {"videos": [], "docs": [
  ["CAP theorem revisited (Robert Greiner)", "https://robertgreiner.com/cap-theorem-revisited/"],
  ["The CAP FAQ (Henry Robinson)", "https://github.com/henryr/cap-faq"],
  ["AlgoMaster — CAP theorem", "https://algomaster.io/learn/system-design/cap-theorem"],
  ["PACELC theorem", "https://en.wikipedia.org/wiki/PACELC_theorem"]]},

"http-tls-protocol-fundamentals.md": {"videos": [], "docs": [
  ["High Performance Browser Networking (free book)", "https://hpbn.co/"],
  ["Cloudflare — What is SSL/TLS?", "https://www.cloudflare.com/learning/ssl/what-is-ssl/"],
  ["MDN — HTTP overview", "https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview"],
  ["AlgoMaster — TCP vs UDP", "https://algomaster.io/learn/system-design/tcp-vs-udp"]]},

"api-styles-rest-graphql-grpc.md": {"videos": [], "docs": [
  ["AlgoMaster — REST vs GraphQL", "https://blog.algomaster.io/p/rest-vs-graphql"],
  ["gRPC — Introduction and core concepts", "https://grpc.io/docs/what-is-grpc/introduction/"],
  ["GraphQL — Learn", "https://graphql.org/learn/"],
  ["Google API design guide", "https://cloud.google.com/apis/design"]]},

"dns-load-balancers-traffic-routing.md": {"videos": [["YM_dEeXmnuY", "Load Balancers: Algorithms and Design", "Gaurav Sen"]], "docs": [
  ["AlgoMaster — How DNS actually works", "https://blog.algomaster.io/p/how-dns-actually-works"],
  ["AlgoMaster — Load balancing algorithms explained with code", "https://blog.algomaster.io/p/load-balancing-algorithms-explained-with-code"],
  ["NGINX — Inside NGINX: designed for performance and scale", "https://www.nginx.com/blog/inside-nginx-how-we-designed-for-performance-scale/"],
  ["Google SRE Book — Load balancing at the datacenter", "https://sre.google/sre-book/load-balancing-datacenter/"]]},

"proxies-api-gateways-service-mesh.md": {"videos": [], "docs": [
  ["AlgoMaster — Proxy vs reverse proxy", "https://blog.algomaster.io/p/proxy-vs-reverse-proxy-explained"],
  ["AlgoMaster — What is an API gateway?", "https://blog.algomaster.io/p/what-is-an-api-gateway"],
  ["microservices.io — API gateway pattern", "https://microservices.io/patterns/apigateway.html"],
  ["Istio — What is a service mesh?", "https://istio.io/latest/about/service-mesh/"]]},

"rate-limiting-algorithms.md": {"videos": [["mhUQe4BKZXs", "Rate Limiting system design — token bucket, leaky bucket, sliding logs", "Tech Dummies - Narendra Lakshmana Gowda"]], "docs": [
  ["AlgoMaster — Rate limiting algorithms explained with code", "https://blog.algomaster.io/p/rate-limiting-algorithms-explained-with-code"],
  ["Cloudflare — How we built rate limiting (sliding window)", "https://blog.cloudflare.com/counting-things-a-lot-of-different-things/"],
  ["Stripe — Scaling your API with rate limiters", "https://stripe.com/blog/rate-limiters"]]},

"real-time-communication-polling-sse-websockets-webrtc.md": {"videos": [["1cFyfT0m3bA", "HTTP Long Polling vs Server Sent Events vs WebSockets", "Tech Primers"]], "docs": [
  ["AlgoMaster — Long polling vs WebSockets", "https://blog.algomaster.io/p/long-polling-vs-websockets"],
  ["MDN — Using server-sent events", "https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events"],
  ["MDN — WebSockets API", "https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API"],
  ["WebRTC — Getting started", "https://webrtc.org/getting-started/overview"]]},

"storage-types-block-object-file.md": {"videos": [], "docs": [
  ["AWS — Block vs file vs object storage", "https://aws.amazon.com/compare/the-difference-between-block-file-object-storage/"],
  ["Amazon S3 — How S3 works", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html"],
  ["The Google File System (paper)", "https://static.googleusercontent.com/media/research.google.com/en//archive/gfs-sosp2003.pdf"]]},

"sql-vs-nosql-decision-framework.md": {"videos": [], "docs": [
  ["AlgoMaster — SQL vs NoSQL", "https://algomaster.io/learn/system-design/sql-vs-nosql"],
  ["AlgoMaster — 15 types of databases", "https://blog.algomaster.io/p/15-types-of-databases"],
  ["MongoDB — Data modelling introduction", "https://www.mongodb.com/docs/manual/data-modeling/"],
  ["System Design Primer — SQL or NoSQL", "https://github.com/donnemartin/system-design-primer#sql-or-nosql"]]},

"acid-transactions-isolation.md": {"videos": [], "docs": [
  ["PostgreSQL — Transaction isolation levels", "https://www.postgresql.org/docs/current/transaction-iso.html"],
  ["AlgoMaster — ACID transactions", "https://algomaster.io/learn/system-design/acid-transactions"],
  ["Jepsen — Consistency and isolation models", "https://jepsen.io/consistency"],
  ["A critique of ANSI SQL isolation levels (paper)", "https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-95-51.pdf"]]},

"indexes-query-optimization.md": {"videos": [], "docs": [
  ["Use The Index, Luke! — SQL indexing and tuning", "https://use-the-index-luke.com/"],
  ["PostgreSQL — Indexes", "https://www.postgresql.org/docs/current/indexes.html"],
  ["AlgoMaster — Database indexing", "https://algomaster.io/learn/system-design/indexing"],
  ["MySQL — Slow query log", "https://dev.mysql.com/doc/refman/8.0/en/slow-query-log.html"]]},

"replication-read-scaling.md": {"videos": [], "docs": [
  ["MySQL — Replication", "https://dev.mysql.com/doc/refman/8.0/en/replication.html"],
  ["AlgoMaster — How to scale a database", "https://blog.algomaster.io/p/system-design-how-to-scale-a-database"],
  ["PostgreSQL — High availability and replication", "https://www.postgresql.org/docs/current/high-availability.html"]]},

"partitioning-sharding-data-distribution.md": {"videos": [["L521gizea4s", "Sharding in System Design Interviews (w/ Meta Staff Engineer)", "Hello Interview"]], "docs": [
  ["AlgoMaster — Database sharding", "https://algomaster.io/learn/system-design/sharding"],
  ["MongoDB — Sharding", "https://www.mongodb.com/docs/manual/sharding/"],
  ["Vitess — Horizontal sharding concepts", "https://vitess.io/docs/concepts/shard/"]]},

"consistent-hashing-rebalancing.md": {"videos": [["UF9Iqmg94tk", "Consistent Hashing | Algorithms You Should Know #1", "ByteByteGo"], ["zaRkONvyGr8", "What is CONSISTENT HASHING and where is it used?", "Gaurav Sen"]], "docs": [
  ["AlgoMaster — Consistent hashing", "https://algomaster.io/learn/system-design/consistent-hashing"],
  ["The magic of consistent hashing", "http://www.paperplanes.de/2011/12/9/the-magic-of-consistent-hashing.html"],
  ["Dynamo: Amazon's highly available key-value store (paper)", "https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf"]]},

"nosql-internals.md": {"videos": [], "docs": [
  ["The Log-Structured Merge-Tree (LSM-tree) paper", "https://www.cs.umb.edu/~poneil/lsmtree.pdf"],
  ["Bigtable: a distributed storage system (paper)", "https://static.googleusercontent.com/media/research.google.com/en//archive/bigtable-osdi06.pdf"],
  ["AlgoMaster — Bloom filters", "https://algomaster.io/learn/system-design/bloom-filters"],
  ["Cassandra — Storage engine and architecture", "https://cassandra.apache.org/doc/latest/cassandra/architecture/storage-engine.html"]]},

"cache-strategies.md": {"videos": [], "docs": [
  ["AlgoMaster — Caching strategies", "https://algomaster.io/learn/system-design/caching-strategies"],
  ["AWS Builders' Library — Caching challenges and strategies", "https://aws.amazon.com/builders-library/caching-challenges-and-strategies/"],
  ["AlgoMaster — Read-through vs write-through cache", "https://blog.algomaster.io/p/59cae60d-9717-4e20-a59e-759e370db4e5"]]},

"cache-eviction-ttl-invalidation.md": {"videos": [], "docs": [
  ["AlgoMaster — 7 cache eviction strategies", "https://blog.algomaster.io/p/7-cache-eviction-strategies"],
  ["Cache replacement policies", "https://en.wikipedia.org/wiki/Cache_replacement_policies"],
  ["Redis — Key eviction policies", "https://redis.io/docs/latest/develop/reference/eviction/"]]},

"cache-failure-modes-pitfalls.md": {"videos": [], "docs": [
  ["AWS Builders' Library — Caching challenges and strategies", "https://aws.amazon.com/builders-library/caching-challenges-and-strategies/"],
  ["Facebook — Scaling Memcache at Facebook (paper)", "https://www.usenix.org/system/files/conference/nsdi13/nsdi13-final170_update.pdf"],
  ["Cache stampede", "https://en.wikipedia.org/wiki/Cache_stampede"]]},

"redis-distributed-caching.md": {"videos": [], "docs": [
  ["AlgoMaster — Distributed caching", "https://blog.algomaster.io/p/distributed-caching"],
  ["Redis — Data types and when to use them", "https://redis.io/docs/latest/develop/data-types/"],
  ["Redis — Distributed locks with Redlock", "https://redis.io/docs/latest/develop/clients/patterns/distributed-locks/"],
  ["Redis — Cluster specification", "https://redis.io/docs/latest/operate/oss_and_stack/reference/cluster-spec/"]]},

"cdn-caching.md": {"videos": [["8zX0rue2Hic", "System Design: Content Delivery Networks (simplified)", "Gaurav Sen"]], "docs": [
  ["Cloudflare — What is a CDN?", "https://www.cloudflare.com/learning/cdn/what-is-a-cdn/"],
  ["Push vs pull CDNs", "https://www.geeksforgeeks.org/system-design/pull-cdn-vs-push-cdn/"],
  ["MDN — HTTP caching", "https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching"]]},

"edge-delivery-global-acceleration.md": {"videos": [], "docs": [
  ["Cloudflare — What is edge computing?", "https://www.cloudflare.com/learning/serverless/glossary/what-is-edge-computing/"],
  ["AWS — Global Accelerator: how it works", "https://docs.aws.amazon.com/global-accelerator/latest/dg/introduction-how-it-works.html"],
  ["Cloudflare — Anycast network", "https://www.cloudflare.com/learning/cdn/glossary/anycast-network/"]]},

"message-queues-vs-event-streams.md": {"videos": [["iJLL-KPqBpM", "System Design Interview — Distributed Message Queue", "System Design Interview"]], "docs": [
  ["AlgoMaster — Message queues", "https://algomaster.io/learn/system-design/message-queues"],
  ["Confluent — Event streaming vs message queues", "https://www.confluent.io/learn/event-streaming/"],
  ["AWS — Amazon SQS dead-letter queues", "https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html"]]},
}
