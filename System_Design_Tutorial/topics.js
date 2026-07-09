window.topicsData = [
  {
    "section": "System Design Interview Process & Requirements",
    "subsections": [
      {
        "id": "requirements-scope",
        "title": "Requirements & Scope",
        "file": "requirements-scope.md",
        "concepts": [
          {
            "title": "Functional requirements checklist",
            "anchor": "functional-requirements-checklist"
          },
          {
            "title": "Non-functional requirements",
            "anchor": "non-functional-requirements"
          },
          {
            "title": "HLD vs LLD: when to switch levels",
            "anchor": "hld-vs-lld-when-to-switch-levels"
          },
          {
            "title": "Clarifying questions that score points",
            "anchor": "clarifying-questions-that-score-points"
          }
        ]
      },
      {
        "id": "capacity-estimation",
        "title": "Capacity Estimation",
        "file": "capacity-estimation.md",
        "concepts": [
          {
            "title": "Back-of-envelope framework",
            "anchor": "back-of-envelope-framework"
          },
          {
            "title": "QPS, storage and bandwidth math",
            "anchor": "qps-storage-and-bandwidth-math"
          },
          {
            "title": "Latency numbers to memorize",
            "anchor": "latency-numbers-to-memorize"
          },
          {
            "title": "Peak vs average traffic sizing",
            "anchor": "peak-vs-average-traffic-sizing"
          },
          {
            "title": "Read/write ratio implications",
            "anchor": "read-write-ratio-implications"
          }
        ]
      },
      {
        "id": "architecture-diagrams-communication",
        "title": "Architecture Diagrams & Communication",
        "file": "architecture-diagrams-communication.md",
        "concepts": [
          {
            "title": "C4 model levels",
            "anchor": "c4-model-levels"
          },
          {
            "title": "UML class and sequence diagrams",
            "anchor": "uml-class-and-sequence-diagrams"
          },
          {
            "title": "Activity and state diagrams",
            "anchor": "activity-and-state-diagrams"
          },
          {
            "title": "Whiteboard layout strategy",
            "anchor": "whiteboard-layout-strategy"
          }
        ]
      },
      {
        "id": "5-step-interview-framework",
        "title": "5-Step Interview Framework",
        "file": "5-step-interview-framework.md",
        "concepts": [
          {
            "title": "Step 1 \u2014 Clarify requirements (5 min): functional + non-functional, scale, constraints",
            "anchor": "step-1-clarify-requirements-5-min-functional-non-functional-scale-constraints"
          },
          {
            "title": "Step 2 \u2014 Back-of-envelope estimates: QPS, storage/yr, bandwidth",
            "anchor": "step-2-back-of-envelope-estimates-qps-storage-yr-bandwidth"
          },
          {
            "title": "Step 3 \u2014 High-level design: draw 4-8 boxes, trace key request flow",
            "anchor": "step-3-high-level-design-draw-4-8-boxes-trace-key-request-flow"
          },
          {
            "title": "Step 4 \u2014 Deep dives: schema, bottlenecks, failure modes; let interviewer steer",
            "anchor": "step-4-deep-dives-schema-bottlenecks-failure-modes-let-interviewer-steer"
          },
          {
            "title": "Step 5 \u2014 Trade-offs: what breaks at 10x? honest about limits = senior signal",
            "anchor": "step-5-trade-offs-what-breaks-at-10x-honest-about-limits-senior-signal"
          }
        ]
      },
      {
        "id": "senior-engineer-signals",
        "title": "Senior Engineer Signals",
        "file": "senior-engineer-signals.md",
        "concepts": [
          {
            "title": "Articulate trade-offs explicitly ('strong consistency costs us latency')",
            "anchor": "articulate-trade-offs-explicitly-strong-consistency-costs-us-latency"
          },
          {
            "title": "Quantify everything \u2014 QPS, P99 latency budget, GB/month storage",
            "anchor": "quantify-everything-qps-p99-latency-budget-gb-month-storage"
          },
          {
            "title": "Failure-first thinking \u2014 'what if the DB dies?' before happy path",
            "anchor": "failure-first-thinking-what-if-the-db-dies-before-happy-path"
          },
          {
            "title": "Operational awareness \u2014 monitoring, deploys, on-call, rollback strategy",
            "anchor": "operational-awareness-monitoring-deploys-on-call-rollback-strategy"
          },
          {
            "title": "Drive the interview \u2014 don't wait for the interviewer to fill silence",
            "anchor": "drive-the-interview-don-t-wait-for-the-interviewer-to-fill-silence"
          }
        ]
      },
      {
        "id": "reference-numbers-estimation-cheat-sheet",
        "title": "Reference Numbers & Estimation Cheat Sheet",
        "file": "reference-numbers-estimation-cheat-sheet.md",
        "concepts": [
          {
            "title": "Powers of 2: 2^10=1K \u00b7 2^20=1M \u00b7 2^30=1B \u00b7 2^40=1T",
            "anchor": "powers-of-2-2-10-1k-2-20-1m-2-30-1b-2-40-1t"
          },
          {
            "title": "Read latencies: L1 0.5ns \u00b7 L2 7ns \u00b7 RAM 100ns \u00b7 SSD 150\u03bcs \u00b7 HDD 10ms \u00b7 WAN 150ms",
            "anchor": "read-latencies-l1-0-5ns-l2-7ns-ram-100ns-ssd-150-s-hdd-10ms-wan-150ms"
          },
          {
            "title": "1B users, 10% DAU, 1 request/day \u2192 ~1157 QPS",
            "anchor": "1b-users-10-dau-1-request-day-1157-qps"
          },
          {
            "title": "100GB/day data \u2192 ~3TB/month \u2192 ~36TB/year \u2192 can a single machine hold it?",
            "anchor": "100gb-day-data-3tb-month-36tb-year-can-a-single-machine-hold-it"
          },
          {
            "title": "Text tweet: ~280 chars \u2192 image tweet: ~500KB \u2192 video: ~100MB",
            "anchor": "text-tweet-280-chars-image-tweet-500kb-video-100mb"
          }
        ]
      }
    ]
  },
  {
    "section": "Core System Design Fundamentals",
    "subsections": [
      {
        "id": "latency-throughput-scalability-basics",
        "title": "Latency, Throughput & Scalability Basics",
        "file": "latency-throughput-scalability-basics.md",
        "concepts": [
          {
            "title": "L1 cache ~0.5ns \u00b7 RAM ~100ns \u00b7 SSD ~150\u03bcs \u00b7 Network ~150ms",
            "anchor": "l1-cache-0-5ns-ram-100ns-ssd-150-s-network-150ms"
          },
          {
            "title": "P50 / P95 / P99 \u2014 tail latency dominates user experience",
            "anchor": "p50-p95-p99-tail-latency-dominates-user-experience"
          },
          {
            "title": "Vertical scaling (scale-up) \u2014 simpler, limited by hardware",
            "anchor": "vertical-scaling-scale-up-simpler-limited-by-hardware"
          },
          {
            "title": "Horizontal scaling (scale-out) \u2014 stateless apps, requires LB",
            "anchor": "horizontal-scaling-scale-out-stateless-apps-requires-lb"
          },
          {
            "title": "Back-of-envelope estimation (QPS, storage, bandwidth)",
            "anchor": "back-of-envelope-estimation-qps-storage-bandwidth"
          },
          {
            "title": "Batching increases throughput at the cost of latency",
            "anchor": "batching-increases-throughput-at-the-cost-of-latency"
          }
        ]
      },
      {
        "id": "availability-reliability-slas",
        "title": "Availability, Reliability & SLAs",
        "file": "availability-reliability-slas.md",
        "concepts": [
          {
            "title": "SLI / SLO / SLA \u2014 indicator, objective, agreement",
            "anchor": "sli-slo-sla-indicator-objective-agreement"
          },
          {
            "title": "99.9% (8.76 hrs/yr) \u00b7 99.99% (52 min/yr) \u00b7 99.999% (5.25 min/yr)",
            "anchor": "99-9-8-76-hrs-yr-99-99-52-min-yr-99-999-5-25-min-yr"
          },
          {
            "title": "Availability in series: multiply (A1 \u00d7 A2) \u2014 cascades",
            "anchor": "availability-in-series-multiply-a1-a2-cascades"
          },
          {
            "title": "Availability in parallel: 1 - (1-A)^n \u2014 redundancy helps",
            "anchor": "availability-in-parallel-1-1-a-n-redundancy-helps"
          },
          {
            "title": "Active-Active failover \u2014 both serve traffic, fastest failover",
            "anchor": "active-active-failover-both-serve-traffic-fastest-failover"
          },
          {
            "title": "Active-Passive failover \u2014 warm standby, ~60s RTO",
            "anchor": "active-passive-failover-warm-standby-60s-rto"
          }
        ]
      },
      {
        "id": "consistency-models",
        "title": "Consistency Models",
        "file": "consistency-models.md",
        "concepts": [
          {
            "title": "Linearizability (strong) \u2014 every read returns latest write",
            "anchor": "linearizability-strong-every-read-returns-latest-write"
          },
          {
            "title": "Eventual consistency \u2014 replicas converge given enough time",
            "anchor": "eventual-consistency-replicas-converge-given-enough-time"
          },
          {
            "title": "Read-your-writes \u2014 you always see your own writes",
            "anchor": "read-your-writes-you-always-see-your-own-writes"
          },
          {
            "title": "Causal consistency \u2014 causally related ops seen in same order",
            "anchor": "causal-consistency-causally-related-ops-seen-in-same-order"
          },
          {
            "title": "Monotonic reads \u2014 never see older value after reading newer",
            "anchor": "monotonic-reads-never-see-older-value-after-reading-newer"
          },
          {
            "title": "CRDTs \u2014 conflict-free replicated data types for multi-master",
            "anchor": "crdts-conflict-free-replicated-data-types-for-multi-master"
          }
        ]
      },
      {
        "id": "cap-pacelc-theorems",
        "title": "CAP & PACELC Theorems",
        "file": "cap-pacelc-theorems.md",
        "concepts": [
          {
            "title": "CAP Theorem \u2014 Consistency + Availability + Partition Tolerance",
            "anchor": "cap-theorem-consistency-availability-partition-tolerance"
          },
          {
            "title": "CP systems: refuse writes during partitions (ZooKeeper, HBase, MongoDB strict)",
            "anchor": "cp-systems-refuse-writes-during-partitions-zookeeper-hbase-mongodb-strict"
          },
          {
            "title": "AP systems: always accept, reconcile later (Cassandra, DynamoDB, CouchDB)",
            "anchor": "ap-systems-always-accept-reconcile-later-cassandra-dynamodb-couchdb"
          },
          {
            "title": "Partition Tolerance is non-negotiable on real networks",
            "anchor": "partition-tolerance-is-non-negotiable-on-real-networks"
          },
          {
            "title": "PACELC: Latency vs Consistency even without partitions",
            "anchor": "pacelc-latency-vs-consistency-even-without-partitions"
          }
        ]
      }
    ]
  },
  {
    "section": "Networking, APIs & Traffic Management",
    "subsections": [
      {
        "id": "http-tls-protocol-fundamentals",
        "title": "HTTP, TLS & Protocol Fundamentals",
        "file": "http-tls-protocol-fundamentals.md",
        "concepts": [
          {
            "title": "HTTP methods: GET/PUT/DELETE (idempotent) vs POST/PATCH (not idempotent)",
            "anchor": "http-methods-get-put-delete-idempotent-vs-post-patch-not-idempotent"
          },
          {
            "title": "Status codes: 2xx success \u00b7 3xx redirect \u00b7 4xx client \u00b7 5xx server",
            "anchor": "status-codes-2xx-success-3xx-redirect-4xx-client-5xx-server"
          },
          {
            "title": "HTTP/1.1 \u2014 text, one request per connection, head-of-line blocking",
            "anchor": "http-1-1-text-one-request-per-connection-head-of-line-blocking"
          },
          {
            "title": "HTTP/2 \u2014 binary framing, multiplexing, header compression (HPACK)",
            "anchor": "http-2-binary-framing-multiplexing-header-compression-hpack"
          },
          {
            "title": "HTTP/3 \u2014 UDP-based QUIC, 0-RTT, no TCP HOL blocking",
            "anchor": "http-3-udp-based-quic-0-rtt-no-tcp-hol-blocking"
          },
          {
            "title": "TLS 1.3 handshake \u2014 1 RTT, forward secrecy",
            "anchor": "tls-1-3-handshake-1-rtt-forward-secrecy"
          }
        ]
      },
      {
        "id": "api-styles-rest-graphql-grpc",
        "title": "API Styles: REST, GraphQL & gRPC",
        "file": "api-styles-rest-graphql-grpc.md",
        "concepts": [
          {
            "title": "REST \u2014 stateless, resources + HTTP verbs, cacheable, uniform interface",
            "anchor": "rest-stateless-resources-http-verbs-cacheable-uniform-interface"
          },
          {
            "title": "GraphQL \u2014 single endpoint, client picks fields, no over/under-fetching",
            "anchor": "graphql-single-endpoint-client-picks-fields-no-over-under-fetching"
          },
          {
            "title": "gRPC \u2014 HTTP/2 + Protobuf, bidirectional streaming, ideal for internal microservices",
            "anchor": "grpc-http-2-protobuf-bidirectional-streaming-ideal-for-internal-microservices"
          },
          {
            "title": "API Gateway \u2014 auth, rate limiting, routing, transformation at ingress",
            "anchor": "api-gateway-auth-rate-limiting-routing-transformation-at-ingress"
          },
          {
            "title": "Idempotency keys \u2014 safe retries, critical for payments and mutations",
            "anchor": "idempotency-keys-safe-retries-critical-for-payments-and-mutations"
          },
          {
            "title": "Webhooks \u2014 server pushes to registered callback URL on event",
            "anchor": "webhooks-server-pushes-to-registered-callback-url-on-event"
          }
        ]
      },
      {
        "id": "dns-load-balancers-traffic-routing",
        "title": "DNS, Load Balancers & Traffic Routing",
        "file": "dns-load-balancers-traffic-routing.md",
        "concepts": [
          {
            "title": "DNS resolution: recursive resolver \u2192 root \u2192 TLD \u2192 authoritative",
            "anchor": "dns-resolution-recursive-resolver-root-tld-authoritative"
          },
          {
            "title": "DNS record types: A, AAAA, CNAME, MX, TXT, NS",
            "anchor": "dns-record-types-a-aaaa-cname-mx-txt-ns"
          },
          {
            "title": "GeoDNS / latency-based routing (Route 53 / Cloudflare)",
            "anchor": "geodns-latency-based-routing-route-53-cloudflare"
          },
          {
            "title": "L4 (TCP) load balancer \u2014 fast, blind to HTTP content",
            "anchor": "l4-tcp-load-balancer-fast-blind-to-http-content"
          },
          {
            "title": "L7 (HTTP) load balancer \u2014 URL routing, sticky sessions, header inspection",
            "anchor": "l7-http-load-balancer-url-routing-sticky-sessions-header-inspection"
          },
          {
            "title": "LB algorithms: round robin, least-conn, IP hash, consistent hash, weighted",
            "anchor": "lb-algorithms-round-robin-least-conn-ip-hash-consistent-hash-weighted"
          },
          {
            "title": "Health checks \u2014 active (ping) vs passive (track error rates)",
            "anchor": "health-checks-active-ping-vs-passive-track-error-rates"
          },
          {
            "title": "Reverse proxy \u2014 single ingress, SSL termination, request buffering",
            "anchor": "reverse-proxy-single-ingress-ssl-termination-request-buffering"
          }
        ]
      },
      {
        "id": "proxies-api-gateways-service-mesh",
        "title": "Proxies, API Gateways & Service Mesh",
        "file": "proxies-api-gateways-service-mesh.md",
        "concepts": [
          {
            "title": "Forward vs reverse proxy",
            "anchor": "forward-vs-reverse-proxy"
          },
          {
            "title": "API gateway responsibilities",
            "anchor": "api-gateway-responsibilities"
          },
          {
            "title": "Load balancer L4 vs L7",
            "anchor": "load-balancer-l4-vs-l7"
          },
          {
            "title": "Service mesh sidecars",
            "anchor": "service-mesh-sidecars"
          }
        ]
      },
      {
        "id": "rate-limiting-algorithms",
        "title": "Rate Limiting Algorithms",
        "file": "rate-limiting-algorithms.md",
        "concepts": [
          {
            "title": "Token bucket \u2014 refill at fixed rate, allow bursts",
            "anchor": "token-bucket-refill-at-fixed-rate-allow-bursts"
          },
          {
            "title": "Leaky bucket \u2014 smooth output rate, no bursts",
            "anchor": "leaky-bucket-smooth-output-rate-no-bursts"
          },
          {
            "title": "Fixed window \u2014 count per window, spike at window boundary",
            "anchor": "fixed-window-count-per-window-spike-at-window-boundary"
          },
          {
            "title": "Sliding window log / counter \u2014 accurate, more memory",
            "anchor": "sliding-window-log-counter-accurate-more-memory"
          },
          {
            "title": "Distributed rate limiting with Redis (Redlock / Lua scripts)",
            "anchor": "distributed-rate-limiting-with-redis-redlock-lua-scripts"
          }
        ]
      },
      {
        "id": "real-time-communication-polling-sse-websockets-webrtc",
        "title": "Real-Time Communication: Polling, SSE, WebSockets & WebRTC",
        "file": "real-time-communication-polling-sse-websockets-webrtc.md",
        "concepts": [
          {
            "title": "Short polling \u2014 client requests every N seconds, wasteful",
            "anchor": "short-polling-client-requests-every-n-seconds-wasteful"
          },
          {
            "title": "Long polling \u2014 server holds connection until data ready or timeout",
            "anchor": "long-polling-server-holds-connection-until-data-ready-or-timeout"
          },
          {
            "title": "SSE (Server-Sent Events) \u2014 HTTP-based, server\u2192client only, auto-reconnect",
            "anchor": "sse-server-sent-events-http-based-server-client-only-auto-reconnect"
          },
          {
            "title": "WebSockets \u2014 full-duplex TCP, use for chat, real-time games, collaboration",
            "anchor": "websockets-full-duplex-tcp-use-for-chat-real-time-games-collaboration"
          },
          {
            "title": "WebRTC \u2014 peer-to-peer media, used for video calls (Zoom, Meet)",
            "anchor": "webrtc-peer-to-peer-media-used-for-video-calls-zoom-meet"
          },
          {
            "title": "Scaling WebSockets \u2014 sticky LB or message broker fan-out (Redis Pub/Sub)",
            "anchor": "scaling-websockets-sticky-lb-or-message-broker-fan-out-redis-pub-sub"
          }
        ]
      }
    ]
  },
  {
    "section": "Data Storage, Databases & Distribution",
    "subsections": [
      {
        "id": "storage-types-block-object-file",
        "title": "Storage Types: Block, Object & File",
        "file": "storage-types-block-object-file.md",
        "concepts": [
          {
            "title": "Block storage (EBS, Azure Disk) \u2014 attach to one VM, high IOPS, DBs/OS disks",
            "anchor": "block-storage-ebs-azure-disk-attach-to-one-vm-high-iops-dbs-os-disks"
          },
          {
            "title": "File storage (EFS, NFS, Azure Files) \u2014 multi-mount, POSIX semantics",
            "anchor": "file-storage-efs-nfs-azure-files-multi-mount-posix-semantics"
          },
          {
            "title": "Object storage (S3, GCS, Azure Blob) \u2014 flat namespace, infinite scale, HTTP API",
            "anchor": "object-storage-s3-gcs-azure-blob-flat-namespace-infinite-scale-http-api"
          },
          {
            "title": "S3 key design \u2014 prefix distribution for parallel requests (avoid sequential prefixes)",
            "anchor": "s3-key-design-prefix-distribution-for-parallel-requests-avoid-sequential-prefixes"
          },
          {
            "title": "Distributed file system (HDFS, Ceph) \u2014 large dataset processing, MapReduce",
            "anchor": "distributed-file-system-hdfs-ceph-large-dataset-processing-mapreduce"
          }
        ]
      },
      {
        "id": "sql-vs-nosql-decision-framework",
        "title": "SQL vs NoSQL Decision Framework",
        "file": "sql-vs-nosql-decision-framework.md",
        "concepts": [
          {
            "title": "SQL (RDBMS) \u2014 ACID, joins, schema, mature tooling (default pick)",
            "anchor": "sql-rdbms-acid-joins-schema-mature-tooling-default-pick"
          },
          {
            "title": "Document stores (MongoDB, CouchDB) \u2014 flexible schema, nested objects",
            "anchor": "document-stores-mongodb-couchdb-flexible-schema-nested-objects"
          },
          {
            "title": "Key-Value (Redis, DynamoDB) \u2014 sub-ms lookups, cache, sessions",
            "anchor": "key-value-redis-dynamodb-sub-ms-lookups-cache-sessions"
          },
          {
            "title": "Wide-column (Cassandra, HBase, ScyllaDB) \u2014 massive write throughput, time-series",
            "anchor": "wide-column-cassandra-hbase-scylladb-massive-write-throughput-time-series"
          },
          {
            "title": "Graph DBs (Neo4j, Neptune) \u2014 many-to-many, fraud detection, social graphs",
            "anchor": "graph-dbs-neo4j-neptune-many-to-many-fraud-detection-social-graphs"
          },
          {
            "title": "Time-series (InfluxDB, TimescaleDB) \u2014 append-heavy, retention policies, IoT metrics",
            "anchor": "time-series-influxdb-timescaledb-append-heavy-retention-policies-iot-metrics"
          },
          {
            "title": "Search engines (Elasticsearch / OpenSearch) \u2014 inverted index, full-text",
            "anchor": "search-engines-elasticsearch-opensearch-inverted-index-full-text"
          }
        ]
      },
      {
        "id": "acid-transactions-isolation",
        "title": "ACID, Transactions & Isolation",
        "file": "acid-transactions-isolation.md",
        "concepts": [
          {
            "title": "Atomicity \u2014 all-or-nothing, rollback on failure",
            "anchor": "atomicity-all-or-nothing-rollback-on-failure"
          },
          {
            "title": "Consistency \u2014 valid state to valid state (app-defined invariants)",
            "anchor": "consistency-valid-state-to-valid-state-app-defined-invariants"
          },
          {
            "title": "Isolation \u2014 concurrent txns appear serial (isolation levels control this)",
            "anchor": "isolation-concurrent-txns-appear-serial-isolation-levels-control-this"
          },
          {
            "title": "Durability \u2014 committed txns survive crashes (WAL, fsync)",
            "anchor": "durability-committed-txns-survive-crashes-wal-fsync"
          },
          {
            "title": "Isolation levels: Read Uncommitted \u2192 Committed \u2192 Repeatable Read \u2192 Serializable",
            "anchor": "isolation-levels-read-uncommitted-committed-repeatable-read-serializable"
          },
          {
            "title": "MVCC (Postgres, Oracle) \u2014 snapshot reads, no read locks",
            "anchor": "mvcc-postgres-oracle-snapshot-reads-no-read-locks"
          },
          {
            "title": "BASE model \u2014 Basically Available, Soft state, Eventual consistency (NoSQL alternative)",
            "anchor": "base-model-basically-available-soft-state-eventual-consistency-nosql-alternative"
          }
        ]
      },
      {
        "id": "indexes-query-optimization",
        "title": "Indexes & Query Optimization",
        "file": "indexes-query-optimization.md",
        "concepts": [
          {
            "title": "B-tree index \u2014 balanced tree, good for range + equality queries (default)",
            "anchor": "b-tree-index-balanced-tree-good-for-range-equality-queries-default"
          },
          {
            "title": "Hash index \u2014 O(1) equality, no range queries",
            "anchor": "hash-index-o-1-equality-no-range-queries"
          },
          {
            "title": "Composite index + leftmost prefix rule",
            "anchor": "composite-index-leftmost-prefix-rule"
          },
          {
            "title": "Covering index \u2014 all needed cols in index, no table read",
            "anchor": "covering-index-all-needed-cols-in-index-no-table-read"
          },
          {
            "title": "LSM tree (Cassandra, RocksDB) \u2014 write-optimized, sorted runs + compaction",
            "anchor": "lsm-tree-cassandra-rocksdb-write-optimized-sorted-runs-compaction"
          },
          {
            "title": "EXPLAIN ANALYZE \u2014 read query plan, spot Seq Scans on big tables",
            "anchor": "explain-analyze-read-query-plan-spot-seq-scans-on-big-tables"
          },
          {
            "title": "Index selectivity \u2014 high cardinality cols are good candidates",
            "anchor": "index-selectivity-high-cardinality-cols-are-good-candidates"
          }
        ]
      },
      {
        "id": "replication-read-scaling",
        "title": "Replication & Read Scaling",
        "file": "replication-read-scaling.md",
        "concepts": [
          {
            "title": "Single-leader (primary-replica) \u2014 all writes to primary, reads to replicas",
            "anchor": "single-leader-primary-replica-all-writes-to-primary-reads-to-replicas"
          },
          {
            "title": "Replication lag \u2014 async replicas may serve stale reads",
            "anchor": "replication-lag-async-replicas-may-serve-stale-reads"
          },
          {
            "title": "Multi-leader replication \u2014 conflict resolution required (LWW or CRDTs)",
            "anchor": "multi-leader-replication-conflict-resolution-required-lww-or-crdts"
          },
          {
            "title": "Leaderless (Cassandra/Dynamo) \u2014 quorum R+W>N for strong consistency",
            "anchor": "leaderless-cassandra-dynamo-quorum-r-w-n-for-strong-consistency"
          },
          {
            "title": "Synchronous vs asynchronous replication \u2014 durability vs performance tradeoff",
            "anchor": "synchronous-vs-asynchronous-replication-durability-vs-performance-tradeoff"
          },
          {
            "title": "Change Data Capture (CDC) \u2014 stream DB changes as events (Debezium, Netflix DBLog)",
            "anchor": "change-data-capture-cdc-stream-db-changes-as-events-debezium-netflix-dblog"
          }
        ]
      },
      {
        "id": "partitioning-sharding-data-distribution",
        "title": "Partitioning, Sharding & Data Distribution",
        "file": "partitioning-sharding-data-distribution.md",
        "concepts": [
          {
            "title": "Range sharding \u2014 split by key ranges (e.g., ID 0-1M, 1M-2M)",
            "anchor": "range-sharding-split-by-key-ranges-e-g-id-0-1m-1m-2m"
          },
          {
            "title": "Hash sharding \u2014 hash(key) % N. Even distribution but no range queries",
            "anchor": "hash-sharding-hash-key-n-even-distribution-but-no-range-queries"
          },
          {
            "title": "Consistent hashing \u2014 resharding moves only 1/N keys",
            "anchor": "consistent-hashing-resharding-moves-only-1-n-keys"
          },
          {
            "title": "Hot key problem \u2014 celebrity users, time-based skew, fix with salting",
            "anchor": "hot-key-problem-celebrity-users-time-based-skew-fix-with-salting"
          },
          {
            "title": "Cross-shard joins \u2014 expensive, avoid by denormalizing or keeping related data together",
            "anchor": "cross-shard-joins-expensive-avoid-by-denormalizing-or-keeping-related-data-together"
          }
        ]
      },
      {
        "id": "consistent-hashing-rebalancing",
        "title": "Consistent Hashing & Rebalancing",
        "file": "consistent-hashing-rebalancing.md",
        "concepts": [
          {
            "title": "Hash ring \u2014 nodes placed at positions, keys routed clockwise",
            "anchor": "hash-ring-nodes-placed-at-positions-keys-routed-clockwise"
          },
          {
            "title": "Virtual nodes \u2014 each server occupies multiple ring positions",
            "anchor": "virtual-nodes-each-server-occupies-multiple-ring-positions"
          },
          {
            "title": "Adding/removing node moves only 1/N keys (vs N keys in modulo hashing)",
            "anchor": "adding-removing-node-moves-only-1-n-keys-vs-n-keys-in-modulo-hashing"
          },
          {
            "title": "Used by: Cassandra, DynamoDB, Memcached, CDN routing",
            "anchor": "used-by-cassandra-dynamodb-memcached-cdn-routing"
          }
        ]
      },
      {
        "id": "nosql-internals",
        "title": "NoSQL Internals",
        "file": "nosql-internals.md",
        "concepts": [
          {
            "title": "Redis data structures: strings, hashes, sets, sorted sets, streams",
            "anchor": "redis-data-structures-strings-hashes-sets-sorted-sets-streams"
          },
          {
            "title": "Cassandra ring topology, token ring, virtual nodes",
            "anchor": "cassandra-ring-topology-token-ring-virtual-nodes"
          },
          {
            "title": "DynamoDB \u2014 partition key design, GSI, consistent reads vs eventually consistent",
            "anchor": "dynamodb-partition-key-design-gsi-consistent-reads-vs-eventually-consistent"
          },
          {
            "title": "MongoDB \u2014 documents, collections, embedded vs referenced, aggregation pipeline",
            "anchor": "mongodb-documents-collections-embedded-vs-referenced-aggregation-pipeline"
          },
          {
            "title": "Bloom filter \u2014 probabilistic, check if key MIGHT exist, no false negatives",
            "anchor": "bloom-filter-probabilistic-check-if-key-might-exist-no-false-negatives"
          },
          {
            "title": "HyperLogLog \u2014 approximate cardinality counting with tiny memory",
            "anchor": "hyperloglog-approximate-cardinality-counting-with-tiny-memory"
          }
        ]
      }
    ]
  },
  {
    "section": "Caching & Content Delivery",
    "subsections": [
      {
        "id": "cache-strategies",
        "title": "Cache Strategies",
        "file": "cache-strategies.md",
        "concepts": [
          {
            "title": "Cache-aside (lazy loading) \u2014 app checks cache, miss \u2192 read DB + write cache",
            "anchor": "cache-aside-lazy-loading-app-checks-cache-miss-read-db-write-cache"
          },
          {
            "title": "Read-through \u2014 cache library handles miss + load automatically",
            "anchor": "read-through-cache-library-handles-miss-load-automatically"
          },
          {
            "title": "Write-through \u2014 write to cache + DB synchronously, always consistent",
            "anchor": "write-through-write-to-cache-db-synchronously-always-consistent"
          },
          {
            "title": "Write-behind (write-back) \u2014 write to cache, async to DB, risk of data loss",
            "anchor": "write-behind-write-back-write-to-cache-async-to-db-risk-of-data-loss"
          },
          {
            "title": "Refresh-ahead \u2014 proactively refresh hot keys before TTL expires",
            "anchor": "refresh-ahead-proactively-refresh-hot-keys-before-ttl-expires"
          }
        ]
      },
      {
        "id": "cache-eviction-ttl-invalidation",
        "title": "Cache Eviction, TTL & Invalidation",
        "file": "cache-eviction-ttl-invalidation.md",
        "concepts": [
          {
            "title": "LRU (Least Recently Used) \u2014 default Redis policy, good for most workloads",
            "anchor": "lru-least-recently-used-default-redis-policy-good-for-most-workloads"
          },
          {
            "title": "LFU (Least Frequently Used) \u2014 better when hot items are consistently hot",
            "anchor": "lfu-least-frequently-used-better-when-hot-items-are-consistently-hot"
          },
          {
            "title": "TTL-based expiry \u2014 simplest, natural for session data",
            "anchor": "ttl-based-expiry-simplest-natural-for-session-data"
          },
          {
            "title": "FIFO \u2014 first item cached, first evicted",
            "anchor": "fifo-first-item-cached-first-evicted"
          }
        ]
      },
      {
        "id": "cache-failure-modes-pitfalls",
        "title": "Cache Failure Modes & Pitfalls",
        "file": "cache-failure-modes-pitfalls.md",
        "concepts": [
          {
            "title": "Cache stampede / thundering herd \u2014 many requests hit DB simultaneously on cache miss",
            "anchor": "cache-stampede-thundering-herd-many-requests-hit-db-simultaneously-on-cache-miss"
          },
          {
            "title": "Fix: mutex / lock around cache miss, OR probabilistic early expiry",
            "anchor": "fix-mutex-lock-around-cache-miss-or-probabilistic-early-expiry"
          },
          {
            "title": "Cache penetration \u2014 queries for non-existent keys bypass cache",
            "anchor": "cache-penetration-queries-for-non-existent-keys-bypass-cache"
          },
          {
            "title": "Fix: cache null values with short TTL, OR bloom filter at cache layer",
            "anchor": "fix-cache-null-values-with-short-ttl-or-bloom-filter-at-cache-layer"
          },
          {
            "title": "Cache avalanche \u2014 many keys expire simultaneously, DB overwhelmed",
            "anchor": "cache-avalanche-many-keys-expire-simultaneously-db-overwhelmed"
          },
          {
            "title": "Hot key \u2014 one key receives disproportionate traffic (celebrity problem)",
            "anchor": "hot-key-one-key-receives-disproportionate-traffic-celebrity-problem"
          }
        ]
      },
      {
        "id": "redis-distributed-caching",
        "title": "Redis & Distributed Caching",
        "file": "redis-distributed-caching.md",
        "concepts": [
          {
            "title": "Redis data types: strings, lists, sets, sorted sets, hashes, streams",
            "anchor": "redis-data-types-strings-lists-sets-sorted-sets-hashes-streams"
          },
          {
            "title": "Redis cluster \u2014 consistent hash ring, 16384 slots, automatic sharding",
            "anchor": "redis-cluster-consistent-hash-ring-16384-slots-automatic-sharding"
          },
          {
            "title": "Redlock \u2014 distributed lock algorithm using multiple Redis instances",
            "anchor": "redlock-distributed-lock-algorithm-using-multiple-redis-instances"
          },
          {
            "title": "Redis Pub/Sub \u2014 fan-out to WebSocket servers for scaling real-time",
            "anchor": "redis-pub-sub-fan-out-to-websocket-servers-for-scaling-real-time"
          },
          {
            "title": "Redis sorted sets \u2014 use for leaderboards, rate limiting with sliding window",
            "anchor": "redis-sorted-sets-use-for-leaderboards-rate-limiting-with-sliding-window"
          }
        ]
      },
      {
        "id": "cdn-caching",
        "title": "CDN Caching",
        "file": "cdn-caching.md",
        "concepts": [
          {
            "title": "Pull CDN \u2014 cache on first request (lazy), low setup, may have cold cache",
            "anchor": "pull-cdn-cache-on-first-request-lazy-low-setup-may-have-cold-cache"
          },
          {
            "title": "Push CDN \u2014 pre-upload content, guaranteed hot cache, high storage cost",
            "anchor": "push-cdn-pre-upload-content-guaranteed-hot-cache-high-storage-cost"
          },
          {
            "title": "Cache invalidation \u2014 URL versioning or purge API",
            "anchor": "cache-invalidation-url-versioning-or-purge-api"
          },
          {
            "title": "CDN for dynamic content \u2014 cache HTML + API responses at edge",
            "anchor": "cdn-for-dynamic-content-cache-html-api-responses-at-edge"
          }
        ]
      },
      {
        "id": "edge-delivery-global-acceleration",
        "title": "Edge Delivery & Global Acceleration",
        "file": "edge-delivery-global-acceleration.md",
        "concepts": [
          {
            "title": "CDN architecture (PoPs, origin shield)",
            "anchor": "cdn-architecture-pops-origin-shield"
          },
          {
            "title": "Edge cache invalidation strategies",
            "anchor": "edge-cache-invalidation-strategies"
          },
          {
            "title": "Static vs dynamic acceleration",
            "anchor": "static-vs-dynamic-acceleration"
          },
          {
            "title": "Signed URLs and token auth",
            "anchor": "signed-urls-and-token-auth"
          }
        ]
      }
    ]
  },
  {
    "section": "Asynchronous Messaging & Event Streaming",
    "subsections": [
      {
        "id": "message-queues-vs-event-streams",
        "title": "Message Queues vs Event Streams",
        "file": "message-queues-vs-event-streams.md",
        "concepts": [
          {
            "title": "Message queue (SQS, RabbitMQ) \u2014 message consumed \u2192 gone, work distribution",
            "anchor": "message-queue-sqs-rabbitmq-message-consumed-gone-work-distribution"
          },
          {
            "title": "Event stream (Kafka, Kinesis) \u2014 durable append-only log, replay, multiple consumer groups",
            "anchor": "event-stream-kafka-kinesis-durable-append-only-log-replay-multiple-consumer-groups"
          },
          {
            "title": "Pub/Sub (SNS, Google Pub/Sub) \u2014 topic fan-out to many subscribers",
            "anchor": "pub-sub-sns-google-pub-sub-topic-fan-out-to-many-subscribers"
          },
          {
            "title": "DB-as-queue antipattern \u2014 polling creates lock contention, never do this",
            "anchor": "db-as-queue-antipattern-polling-creates-lock-contention-never-do-this"
          }
        ]
      },
      {
        "id": "kafka-architecture",
        "title": "Kafka Architecture",
        "file": "kafka-architecture.md",
        "concepts": [
          {
            "title": "Topics, partitions, offsets \u2014 horizontal scale by adding partitions",
            "anchor": "topics-partitions-offsets-horizontal-scale-by-adding-partitions"
          },
          {
            "title": "Consumer groups \u2014 each group sees all messages; within group, each partition \u2192 one consumer",
            "anchor": "consumer-groups-each-group-sees-all-messages-within-group-each-partition-one-consumer"
          },
          {
            "title": "Sequential disk I/O + zero-copy \u2014 why Kafka is fast",
            "anchor": "sequential-disk-i-o-zero-copy-why-kafka-is-fast"
          },
          {
            "title": "Retention \u2014 keep messages N days regardless of consumption",
            "anchor": "retention-keep-messages-n-days-regardless-of-consumption"
          },
          {
            "title": "Exactly-once semantics (Kafka transactions, idempotent producers)",
            "anchor": "exactly-once-semantics-kafka-transactions-idempotent-producers"
          }
        ]
      },
      {
        "id": "delivery-semantics-reliability",
        "title": "Delivery Semantics & Reliability",
        "file": "delivery-semantics-reliability.md",
        "concepts": [
          {
            "title": "At-most-once \u2014 fire and forget, may lose messages",
            "anchor": "at-most-once-fire-and-forget-may-lose-messages"
          },
          {
            "title": "At-least-once \u2014 retry on failure, duplicates possible \u2192 make consumers idempotent",
            "anchor": "at-least-once-retry-on-failure-duplicates-possible-make-consumers-idempotent"
          },
          {
            "title": "Exactly-once \u2014 Kafka transactions or idempotency keys",
            "anchor": "exactly-once-kafka-transactions-or-idempotency-keys"
          },
          {
            "title": "Idempotency keys \u2014 safe retries, critical for payments (Airbnb, Stripe)",
            "anchor": "idempotency-keys-safe-retries-critical-for-payments-airbnb-stripe"
          },
          {
            "title": "Dead Letter Queue (DLQ) \u2014 park failed messages after N retries for inspection",
            "anchor": "dead-letter-queue-dlq-park-failed-messages-after-n-retries-for-inspection"
          }
        ]
      },
      {
        "id": "event-driven-architecture",
        "title": "Event-Driven Architecture",
        "file": "event-driven-architecture.md",
        "concepts": [
          {
            "title": "Event sourcing \u2014 state = fold(all events), full audit log, replayable",
            "anchor": "event-sourcing-state-fold-all-events-full-audit-log-replayable"
          },
          {
            "title": "CQRS \u2014 separate write model (commands) from read model (queries)",
            "anchor": "cqrs-separate-write-model-commands-from-read-model-queries"
          },
          {
            "title": "SAGA pattern \u2014 chain of local txns + compensating actions (replaces 2PC)",
            "anchor": "saga-pattern-chain-of-local-txns-compensating-actions-replaces-2pc"
          },
          {
            "title": "Choreography (events) vs Orchestration (central coordinator)",
            "anchor": "choreography-events-vs-orchestration-central-coordinator"
          },
          {
            "title": "Transactional Outbox \u2014 atomically write DB + outbox row, publish separately",
            "anchor": "transactional-outbox-atomically-write-db-outbox-row-publish-separately"
          }
        ]
      }
    ]
  },
  {
    "section": "Service Architecture Patterns",
    "subsections": [
      {
        "id": "monolith-vs-microservices-vs-serverless",
        "title": "Monolith vs Microservices vs Serverless",
        "file": "monolith-vs-microservices-vs-serverless.md",
        "concepts": [
          {
            "title": "Monolithic \u2014 single deployable, fast initial dev, painful at 50+ engineers",
            "anchor": "monolithic-single-deployable-fast-initial-dev-painful-at-50-engineers"
          },
          {
            "title": "Modular monolith \u2014 strong internal boundaries, best of both worlds",
            "anchor": "modular-monolith-strong-internal-boundaries-best-of-both-worlds"
          },
          {
            "title": "Microservices \u2014 team autonomy, polyglot, independent deploy, complex operationally",
            "anchor": "microservices-team-autonomy-polyglot-independent-deploy-complex-operationally"
          },
          {
            "title": "Serverless (Lambda/Functions) \u2014 event-triggered, no servers, pay-per-invocation",
            "anchor": "serverless-lambda-functions-event-triggered-no-servers-pay-per-invocation"
          },
          {
            "title": "SOA (Service-Oriented Architecture) \u2014 coarser than microservices, centralized ESB",
            "anchor": "soa-service-oriented-architecture-coarser-than-microservices-centralized-esb"
          },
          {
            "title": "Nanoservices antipattern \u2014 too fine-grained, network overhead dominates",
            "anchor": "nanoservices-antipattern-too-fine-grained-network-overhead-dominates"
          }
        ]
      },
      {
        "id": "microservices-patterns",
        "title": "Microservices Patterns",
        "file": "microservices-patterns.md",
        "concepts": [
          {
            "title": "API Gateway \u2014 single entry, auth, rate limit, routing, aggregation",
            "anchor": "api-gateway-single-entry-auth-rate-limit-routing-aggregation"
          },
          {
            "title": "Service discovery \u2014 client-side (Eureka) vs server-side (Consul, K8s DNS)",
            "anchor": "service-discovery-client-side-eureka-vs-server-side-consul-k8s-dns"
          },
          {
            "title": "Service mesh (Istio, Linkerd) \u2014 sidecar proxies handle mTLS, retries, LB",
            "anchor": "service-mesh-istio-linkerd-sidecar-proxies-handle-mtls-retries-lb"
          },
          {
            "title": "Sidecar pattern \u2014 helper container alongside main app for cross-cutting concerns",
            "anchor": "sidecar-pattern-helper-container-alongside-main-app-for-cross-cutting-concerns"
          },
          {
            "title": "Database-per-service \u2014 each service owns its schema, no shared DBs",
            "anchor": "database-per-service-each-service-owns-its-schema-no-shared-dbs"
          },
          {
            "title": "Strangler Fig \u2014 incrementally replace monolith by routing slices to new services",
            "anchor": "strangler-fig-incrementally-replace-monolith-by-routing-slices-to-new-services"
          },
          {
            "title": "Backends for Frontends (BFF) \u2014 separate API gateway per client type",
            "anchor": "backends-for-frontends-bff-separate-api-gateway-per-client-type"
          }
        ]
      },
      {
        "id": "clean-layered-hexagonal-architecture",
        "title": "Clean, Layered & Hexagonal Architecture",
        "file": "clean-layered-hexagonal-architecture.md",
        "concepts": [
          {
            "title": "Hexagonal Architecture (Ports and Adapters) \u2014 business logic core, adapters at boundary",
            "anchor": "hexagonal-architecture-ports-and-adapters-business-logic-core-adapters-at-boundary"
          },
          {
            "title": "Clean Architecture \u2014 entities \u2192 use cases \u2192 interface adapters \u2192 frameworks",
            "anchor": "clean-architecture-entities-use-cases-interface-adapters-frameworks"
          },
          {
            "title": "Domain-Driven Design (DDD) \u2014 ubiquitous language, bounded contexts, aggregates",
            "anchor": "domain-driven-design-ddd-ubiquitous-language-bounded-contexts-aggregates"
          },
          {
            "title": "12-Factor App \u2014 config in env, stateless processes, backing services",
            "anchor": "12-factor-app-config-in-env-stateless-processes-backing-services"
          }
        ]
      }
    ]
  },
  {
    "section": "Reliability, Resilience & Idempotency",
    "subsections": [
      {
        "id": "circuit-breakers-bulkheads-timeouts",
        "title": "Circuit Breakers, Bulkheads & Timeouts",
        "file": "circuit-breakers-bulkheads-timeouts.md",
        "concepts": [
          {
            "title": "Circuit breaker states: Closed (normal) \u2192 Open (failing) \u2192 Half-Open (testing)",
            "anchor": "circuit-breaker-states-closed-normal-open-failing-half-open-testing"
          },
          {
            "title": "Bulkhead \u2014 isolate resource pools so one busy area can't starve others",
            "anchor": "bulkhead-isolate-resource-pools-so-one-busy-area-can-t-starve-others"
          },
          {
            "title": "Timeouts \u2014 never call external service without one, default short",
            "anchor": "timeouts-never-call-external-service-without-one-default-short"
          },
          {
            "title": "Exponential backoff + jitter \u2014 wait 2^n seconds + random jitter, prevents stampede",
            "anchor": "exponential-backoff-jitter-wait-2-n-seconds-random-jitter-prevents-stampede"
          },
          {
            "title": "Retry storm antipattern \u2014 all layers retrying simultaneously = multiplicative load",
            "anchor": "retry-storm-antipattern-all-layers-retrying-simultaneously-multiplicative-load"
          }
        ]
      },
      {
        "id": "backpressure-throttling-load-protection",
        "title": "Backpressure, Throttling & Load Protection",
        "file": "backpressure-throttling-load-protection.md",
        "concepts": [
          {
            "title": "Token bucket \u2014 burst-friendly, most common choice",
            "anchor": "token-bucket-burst-friendly-most-common-choice"
          },
          {
            "title": "Fixed window \u2014 simple, vulnerable to edge-of-window spike",
            "anchor": "fixed-window-simple-vulnerable-to-edge-of-window-spike"
          },
          {
            "title": "Sliding window log \u2014 accurate, high memory usage",
            "anchor": "sliding-window-log-accurate-high-memory-usage"
          },
          {
            "title": "Distributed rate limiting with Redis Lua scripts",
            "anchor": "distributed-rate-limiting-with-redis-lua-scripts"
          }
        ]
      },
      {
        "id": "graceful-degradation-load-shedding",
        "title": "Graceful Degradation & Load Shedding",
        "file": "graceful-degradation-load-shedding.md",
        "concepts": [
          {
            "title": "Fallback responses \u2014 return stale cache or default when upstream is down",
            "anchor": "fallback-responses-return-stale-cache-or-default-when-upstream-is-down"
          },
          {
            "title": "Feature flags / kill switches \u2014 turn off expensive features under load",
            "anchor": "feature-flags-kill-switches-turn-off-expensive-features-under-load"
          },
          {
            "title": "Load shedding \u2014 reject low-priority requests early (return 503) before overload",
            "anchor": "load-shedding-reject-low-priority-requests-early-return-503-before-overload"
          },
          {
            "title": "Priority queues \u2014 critical work executes even when system is degraded",
            "anchor": "priority-queues-critical-work-executes-even-when-system-is-degraded"
          }
        ]
      },
      {
        "id": "distributed-locking-idempotency-safe-retries",
        "title": "Distributed Locking, Idempotency & Safe Retries",
        "file": "distributed-locking-idempotency-safe-retries.md",
        "concepts": [
          {
            "title": "Distributed lock use cases \u2014 prevent double-processing, inventory decrement",
            "anchor": "distributed-lock-use-cases-prevent-double-processing-inventory-decrement"
          },
          {
            "title": "Redlock \u2014 Redis-based algorithm using quorum of N nodes",
            "anchor": "redlock-redis-based-algorithm-using-quorum-of-n-nodes"
          },
          {
            "title": "ZooKeeper / etcd for distributed coordination (more robust than Redlock)",
            "anchor": "zookeeper-etcd-for-distributed-coordination-more-robust-than-redlock"
          },
          {
            "title": "Optimistic locking (version columns) \u2014 retry on conflict, no lock held",
            "anchor": "optimistic-locking-version-columns-retry-on-conflict-no-lock-held"
          }
        ]
      }
    ]
  },
  {
    "section": "Distributed Systems Coordination",
    "subsections": [
      {
        "id": "consensus-algorithms-raft-paxos",
        "title": "Consensus Algorithms: Raft & Paxos",
        "file": "consensus-algorithms-raft-paxos.md",
        "concepts": [
          {
            "title": "Raft \u2014 leader election, log replication, safety guarantees (easier than Paxos)",
            "anchor": "raft-leader-election-log-replication-safety-guarantees-easier-than-paxos"
          },
          {
            "title": "Raft leader election \u2014 candidate, follower, leader roles; randomized timeouts",
            "anchor": "raft-leader-election-candidate-follower-leader-roles-randomized-timeouts"
          },
          {
            "title": "Log replication \u2014 leader appends, replicates to quorum, commits",
            "anchor": "log-replication-leader-appends-replicates-to-quorum-commits"
          },
          {
            "title": "Paxos \u2014 original consensus algorithm, harder to understand and implement",
            "anchor": "paxos-original-consensus-algorithm-harder-to-understand-and-implement"
          },
          {
            "title": "Used in: etcd (Kubernetes), ZooKeeper, CockroachDB, MongoDB (replica sets)",
            "anchor": "used-in-etcd-kubernetes-zookeeper-cockroachdb-mongodb-replica-sets"
          }
        ]
      },
      {
        "id": "leader-election-heartbeats-failure-detection",
        "title": "Leader Election, Heartbeats & Failure Detection",
        "file": "leader-election-heartbeats-failure-detection.md",
        "concepts": [
          {
            "title": "Leader election \u2014 Raft / Bully algorithm / ZooKeeper sequential nodes",
            "anchor": "leader-election-raft-bully-algorithm-zookeeper-sequential-nodes"
          },
          {
            "title": "Heartbeats \u2014 periodic pings to detect node failure",
            "anchor": "heartbeats-periodic-pings-to-detect-node-failure"
          },
          {
            "title": "Gossip protocol \u2014 nodes share state probabilistically, no central coordinator",
            "anchor": "gossip-protocol-nodes-share-state-probabilistically-no-central-coordinator"
          },
          {
            "title": "Phi Accrual Failure Detector \u2014 probabilistic failure detection (Akka, Cassandra)",
            "anchor": "phi-accrual-failure-detector-probabilistic-failure-detection-akka-cassandra"
          }
        ]
      },
      {
        "id": "distributed-transactions-sagas",
        "title": "Distributed Transactions & Sagas",
        "file": "distributed-transactions-sagas.md",
        "concepts": [
          {
            "title": "Two-Phase Commit (2PC) \u2014 prepare + commit phases, blocks on coordinator failure",
            "anchor": "two-phase-commit-2pc-prepare-commit-phases-blocks-on-coordinator-failure"
          },
          {
            "title": "SAGA \u2014 chain of local txns + compensating actions, no distributed lock",
            "anchor": "saga-chain-of-local-txns-compensating-actions-no-distributed-lock"
          },
          {
            "title": "Transactional Outbox \u2014 write DB + outbox atomically, publish from outbox",
            "anchor": "transactional-outbox-write-db-outbox-atomically-publish-from-outbox"
          },
          {
            "title": "Vector clocks \u2014 track causality, detect concurrent writes",
            "anchor": "vector-clocks-track-causality-detect-concurrent-writes"
          }
        ]
      }
    ]
  },
  {
    "section": "Search Systems & Discovery",
    "subsections": [
      {
        "id": "search-indexing-ranking-typeahead",
        "title": "Search Indexing, Ranking & Typeahead",
        "file": "search-indexing-ranking-typeahead.md",
        "concepts": [
          {
            "title": "Inverted index fundamentals",
            "anchor": "inverted-index-fundamentals"
          },
          {
            "title": "Elasticsearch architecture",
            "anchor": "elasticsearch-architecture"
          },
          {
            "title": "Relevance scoring (TF-IDF, BM25)",
            "anchor": "relevance-scoring-tf-idf-bm25"
          },
          {
            "title": "Autocomplete / typeahead design",
            "anchor": "autocomplete-typeahead-design"
          }
        ]
      }
    ]
  },
  {
    "section": "Observability, SLOs, Testing & Delivery",
    "subsections": [
      {
        "id": "metrics-dashboards-alerting",
        "title": "Metrics, Dashboards & Alerting",
        "file": "metrics-dashboards-alerting.md",
        "concepts": [
          {
            "title": "4 Golden Signals: latency, traffic, errors, saturation (Google SRE)",
            "anchor": "4-golden-signals-latency-traffic-errors-saturation-google-sre"
          },
          {
            "title": "RED method (Rate, Errors, Duration) \u2014 per-service health",
            "anchor": "red-method-rate-errors-duration-per-service-health"
          },
          {
            "title": "USE method (Utilization, Saturation, Errors) \u2014 for infrastructure resources",
            "anchor": "use-method-utilization-saturation-errors-for-infrastructure-resources"
          },
          {
            "title": "Prometheus scrape model \u2014 pull metrics from /metrics endpoints",
            "anchor": "prometheus-scrape-model-pull-metrics-from-metrics-endpoints"
          },
          {
            "title": "Alertmanager \u2014 route alerts to PagerDuty, Slack, email",
            "anchor": "alertmanager-route-alerts-to-pagerduty-slack-email"
          }
        ]
      },
      {
        "id": "logging-distributed-tracing",
        "title": "Logging & Distributed Tracing",
        "file": "logging-distributed-tracing.md",
        "concepts": [
          {
            "title": "Structured logs \u2014 JSON with trace_id, user_id, latency_ms on every line",
            "anchor": "structured-logs-json-with-trace-id-user-id-latency-ms-on-every-line"
          },
          {
            "title": "Distributed tracing \u2014 trace_id threads requests across services (Jaeger, Zipkin)",
            "anchor": "distributed-tracing-trace-id-threads-requests-across-services-jaeger-zipkin"
          },
          {
            "title": "W3C Trace Context standard \u2014 interoperable trace propagation headers",
            "anchor": "w3c-trace-context-standard-interoperable-trace-propagation-headers"
          },
          {
            "title": "CloudTrail / Activity Log \u2014 audit trail for 'who did what when'",
            "anchor": "cloudtrail-activity-log-audit-trail-for-who-did-what-when"
          },
          {
            "title": "Alert fatigue \u2014 every alert must be actionable or it becomes noise",
            "anchor": "alert-fatigue-every-alert-must-be-actionable-or-it-becomes-noise"
          }
        ]
      },
      {
        "id": "slos-error-budgets-golden-signals",
        "title": "SLOs, Error Budgets & Golden Signals",
        "file": "slos-error-budgets-golden-signals.md",
        "concepts": [
          {
            "title": "SLI / SLO / SLA definitions",
            "anchor": "sli-slo-sla-definitions"
          },
          {
            "title": "Error budgets",
            "anchor": "error-budgets"
          },
          {
            "title": "Golden signals",
            "anchor": "golden-signals"
          },
          {
            "title": "Distributed tracing",
            "anchor": "distributed-tracing"
          }
        ]
      },
      {
        "id": "testing-chaos-safe-deployment",
        "title": "Testing, Chaos & Safe Deployment",
        "file": "testing-chaos-safe-deployment.md",
        "concepts": [
          {
            "title": "Load, stress and soak testing",
            "anchor": "load-stress-and-soak-testing"
          },
          {
            "title": "Chaos engineering",
            "anchor": "chaos-engineering"
          },
          {
            "title": "CI/CD pipeline design",
            "anchor": "ci-cd-pipeline-design"
          },
          {
            "title": "Canary and blue-green deployment",
            "anchor": "canary-and-blue-green-deployment"
          }
        ]
      }
    ]
  },
  {
    "section": "Security, Privacy & Threat Modeling",
    "subsections": [
      {
        "id": "authentication-authorization",
        "title": "Authentication & Authorization",
        "file": "authentication-authorization.md",
        "concepts": [
          {
            "title": "Sessions (server-side state) vs JWT (stateless signed tokens)",
            "anchor": "sessions-server-side-state-vs-jwt-stateless-signed-tokens"
          },
          {
            "title": "OAuth 2.0 \u2014 delegated authorization; flows: Auth Code, PKCE, Client Credentials",
            "anchor": "oauth-2-0-delegated-authorization-flows-auth-code-pkce-client-credentials"
          },
          {
            "title": "OpenID Connect (OIDC) \u2014 authentication layer on top of OAuth 2.0",
            "anchor": "openid-connect-oidc-authentication-layer-on-top-of-oauth-2-0"
          },
          {
            "title": "SAML \u2014 XML-based SSO, common in enterprise",
            "anchor": "saml-xml-based-sso-common-in-enterprise"
          },
          {
            "title": "MFA / WebAuthn \u2014 phishing-resistant hardware key, FIDO2",
            "anchor": "mfa-webauthn-phishing-resistant-hardware-key-fido2"
          },
          {
            "title": "RBAC (Role-Based) vs ABAC (Attribute-Based) access control",
            "anchor": "rbac-role-based-vs-abac-attribute-based-access-control"
          }
        ]
      },
      {
        "id": "owasp-top-10-api-security",
        "title": "OWASP Top 10 & API Security",
        "file": "owasp-top-10-api-security.md",
        "concepts": [
          {
            "title": "SQL/NoSQL/OS injection \u2014 user input as code; fix: parameterized queries",
            "anchor": "sql-nosql-os-injection-user-input-as-code-fix-parameterized-queries"
          },
          {
            "title": "XSS (Cross-Site Scripting) \u2014 injected JS in pages; fix: escape output, CSP",
            "anchor": "xss-cross-site-scripting-injected-js-in-pages-fix-escape-output-csp"
          },
          {
            "title": "CSRF (Cross-Site Request Forgery) \u2014 forged requests; fix: CSRF tokens, SameSite",
            "anchor": "csrf-cross-site-request-forgery-forged-requests-fix-csrf-tokens-samesite"
          },
          {
            "title": "SSRF (Server-Side Request Forgery) \u2014 server fetches internal URLs; exploits cloud metadata",
            "anchor": "ssrf-server-side-request-forgery-server-fetches-internal-urls-exploits-cloud-metadata"
          },
          {
            "title": "Broken authentication \u2014 weak passwords, no MFA, exposed session IDs",
            "anchor": "broken-authentication-weak-passwords-no-mfa-exposed-session-ids"
          },
          {
            "title": "API security: always authenticate, validate input, log all calls, rate limit",
            "anchor": "api-security-always-authenticate-validate-input-log-all-calls-rate-limit"
          }
        ]
      },
      {
        "id": "threat-modeling-abuse-cases",
        "title": "Threat Modeling & Abuse Cases",
        "file": "threat-modeling-abuse-cases.md",
        "concepts": [
          {
            "title": "STRIDE framework",
            "anchor": "stride-framework"
          },
          {
            "title": "Attack surface mapping",
            "anchor": "attack-surface-mapping"
          },
          {
            "title": "Data classification and encryption boundaries",
            "anchor": "data-classification-and-encryption-boundaries"
          },
          {
            "title": "Abuse and rate-limit threat cases",
            "anchor": "abuse-and-rate-limit-threat-cases"
          }
        ]
      }
    ]
  },
  {
    "section": "Cost & Performance Optimization",
    "subsections": [
      {
        "id": "cost-estimation-build-vs-buy-trade-offs",
        "title": "Cost Estimation & Build-vs-Buy Trade-offs",
        "file": "cost-estimation-build-vs-buy-trade-offs.md",
        "concepts": [
          {
            "title": "Cost vs performance trade-offs",
            "anchor": "cost-vs-performance-trade-offs"
          },
          {
            "title": "Compute vs storage vs network costs",
            "anchor": "compute-vs-storage-vs-network-costs"
          },
          {
            "title": "Autoscaling economics",
            "anchor": "autoscaling-economics"
          },
          {
            "title": "Build vs buy decisions",
            "anchor": "build-vs-buy-decisions"
          }
        ]
      }
    ]
  },
  {
    "section": "Classic HLD Case Studies",
    "subsections": [
      {
        "id": "foundational-designs",
        "title": "Foundational Designs",
        "file": "foundational-designs.md",
        "concepts": [
          {
            "title": "URL Shortener (TinyURL/bit.ly) \u2014 hash + base62, collision handling, analytics",
            "anchor": "url-shortener-tinyurl-bit-ly-hash-base62-collision-handling-analytics"
          },
          {
            "title": "Distributed Cache (Redis cluster) \u2014 consistent hashing, eviction, replication",
            "anchor": "distributed-cache-redis-cluster-consistent-hashing-eviction-replication"
          },
          {
            "title": "Key-Value Store \u2014 LSM tree, compaction, range queries",
            "anchor": "key-value-store-lsm-tree-compaction-range-queries"
          },
          {
            "title": "Content Delivery Network \u2014 pull vs push, origin shield, cache invalidation",
            "anchor": "content-delivery-network-pull-vs-push-origin-shield-cache-invalidation"
          },
          {
            "title": "Rate Limiter (distributed) \u2014 token bucket in Redis, per-user limits",
            "anchor": "rate-limiter-distributed-token-bucket-in-redis-per-user-limits"
          },
          {
            "title": "Distributed Job Scheduler \u2014 priority queues, at-least-once execution, dedup",
            "anchor": "distributed-job-scheduler-priority-queues-at-least-once-execution-dedup"
          }
        ]
      },
      {
        "id": "core-interview-designs",
        "title": "Core Interview Designs",
        "file": "core-interview-designs.md",
        "concepts": [
          {
            "title": "Chat / WhatsApp / Slack \u2014 WebSockets, message ordering, presence, fan-out",
            "anchor": "chat-whatsapp-slack-websockets-message-ordering-presence-fan-out"
          },
          {
            "title": "Twitter / X \u2014 fan-out on write vs read; hybrid for celebrities",
            "anchor": "twitter-x-fan-out-on-write-vs-read-hybrid-for-celebrities"
          },
          {
            "title": "YouTube / Netflix \u2014 upload pipeline, transcoding, adaptive bitrate streaming, CDN",
            "anchor": "youtube-netflix-upload-pipeline-transcoding-adaptive-bitrate-streaming-cdn"
          },
          {
            "title": "Instagram / Photo sharing \u2014 media upload, feed generation, S3+CDN",
            "anchor": "instagram-photo-sharing-media-upload-feed-generation-s3-cdn"
          },
          {
            "title": "Notification System \u2014 multi-channel (push/email/SMS), queues, templates, dedup",
            "anchor": "notification-system-multi-channel-push-email-sms-queues-templates-dedup"
          },
          {
            "title": "Ticketmaster / Seat Booking \u2014 inventory locks, payment timeout, distributed txns",
            "anchor": "ticketmaster-seat-booking-inventory-locks-payment-timeout-distributed-txns"
          },
          {
            "title": "Tinder / Matching \u2014 geospatial indexing, swiping at scale, recommendations",
            "anchor": "tinder-matching-geospatial-indexing-swiping-at-scale-recommendations"
          },
          {
            "title": "TikTok / Short Video \u2014 ML-powered feed, CDN, video encoding pipeline",
            "anchor": "tiktok-short-video-ml-powered-feed-cdn-video-encoding-pipeline"
          },
          {
            "title": "Airbnb / Booking \u2014 double-booking prevention, calendar availability, search",
            "anchor": "airbnb-booking-double-booking-prevention-calendar-availability-search"
          },
          {
            "title": "Payment System \u2014 idempotency, double-entry bookkeeping, audit logs, PCI-DSS",
            "anchor": "payment-system-idempotency-double-entry-bookkeeping-audit-logs-pci-dss"
          },
          {
            "title": "Distributed Message Queue (Kafka design) \u2014 ordering, partitions, consumer groups",
            "anchor": "distributed-message-queue-kafka-design-ordering-partitions-consumer-groups"
          },
          {
            "title": "Reddit / HN \u2014 voting, ranking, comment threads, subreddit feeds",
            "anchor": "reddit-hn-voting-ranking-comment-threads-subreddit-feeds"
          },
          {
            "title": "Autocomplete / Typeahead \u2014 trie, top-K, Redis sorted sets, prefix cache",
            "anchor": "autocomplete-typeahead-trie-top-k-redis-sorted-sets-prefix-cache"
          }
        ]
      },
      {
        "id": "advanced-senior-level-designs",
        "title": "Advanced Senior-Level Designs",
        "file": "advanced-senior-level-designs.md",
        "concepts": [
          {
            "title": "Uber / Rideshare \u2014 geospatial indexing (quad-tree/geohash), matching, real-time location",
            "anchor": "uber-rideshare-geospatial-indexing-quad-tree-geohash-matching-real-time-location"
          },
          {
            "title": "Google Search \u2014 crawling, indexing, ranking (PageRank), serving",
            "anchor": "google-search-crawling-indexing-ranking-pagerank-serving"
          },
          {
            "title": "Google Drive / Dropbox \u2014 chunked upload, dedup (hashing), sync, conflict resolution",
            "anchor": "google-drive-dropbox-chunked-upload-dedup-hashing-sync-conflict-resolution"
          },
          {
            "title": "Google Maps \u2014 tile generation, routing (Dijkstra at scale), real-time traffic",
            "anchor": "google-maps-tile-generation-routing-dijkstra-at-scale-real-time-traffic"
          },
          {
            "title": "Google Docs / Collaborative Editing \u2014 OT (Operational Transform) or CRDTs, conflict resolution",
            "anchor": "google-docs-collaborative-editing-ot-operational-transform-or-crdts-conflict-resolution"
          },
          {
            "title": "Stock Exchange \u2014 ultra-low latency, order matching engine, FIFO fairness",
            "anchor": "stock-exchange-ultra-low-latency-order-matching-engine-fifo-fairness"
          },
          {
            "title": "Facebook News Feed \u2014 social graph, ranking, fan-out strategies at 3B users",
            "anchor": "facebook-news-feed-social-graph-ranking-fan-out-strategies-at-3b-users"
          },
          {
            "title": "Distributed Locking Service (like Chubby) \u2014 consensus + lease renewal + callbacks",
            "anchor": "distributed-locking-service-like-chubby-consensus-lease-renewal-callbacks"
          }
        ]
      }
    ]
  },
  {
    "section": "Low-Level Design & Object-Oriented Design",
    "subsections": [
      {
        "id": "hld-vs-lld-boundaries",
        "title": "HLD vs LLD Boundaries",
        "file": "hld-vs-lld-boundaries.md",
        "concepts": [
          {
            "title": "High-level design scope",
            "anchor": "high-level-design-scope"
          },
          {
            "title": "Low-level design scope",
            "anchor": "low-level-design-scope"
          },
          {
            "title": "When to switch from HLD to LLD",
            "anchor": "when-to-switch-from-hld-to-lld"
          },
          {
            "title": "API contract vs class contract",
            "anchor": "api-contract-vs-class-contract"
          }
        ]
      },
      {
        "id": "object-oriented-foundations",
        "title": "Object-Oriented Foundations",
        "file": "object-oriented-foundations.md",
        "concepts": [
          {
            "title": "Encapsulation",
            "anchor": "encapsulation"
          },
          {
            "title": "Abstraction",
            "anchor": "abstraction"
          },
          {
            "title": "Inheritance vs composition",
            "anchor": "inheritance-vs-composition"
          },
          {
            "title": "Polymorphism",
            "anchor": "polymorphism"
          }
        ]
      },
      {
        "id": "design-principles",
        "title": "Design Principles",
        "file": "design-principles.md",
        "concepts": [
          {
            "title": "SOLID principles",
            "anchor": "solid-principles"
          },
          {
            "title": "DRY principle",
            "anchor": "dry-principle"
          },
          {
            "title": "KISS principle",
            "anchor": "kiss-principle"
          },
          {
            "title": "YAGNI principle",
            "anchor": "yagni-principle"
          }
        ]
      },
      {
        "id": "uml-interaction-modeling",
        "title": "UML & Interaction Modeling",
        "file": "uml-interaction-modeling.md",
        "concepts": [
          {
            "title": "Class diagrams",
            "anchor": "class-diagrams"
          },
          {
            "title": "Sequence diagrams",
            "anchor": "sequence-diagrams"
          },
          {
            "title": "Activity diagrams",
            "anchor": "activity-diagrams"
          },
          {
            "title": "State diagrams",
            "anchor": "state-diagrams"
          }
        ]
      },
      {
        "id": "design-patterns-for-lld",
        "title": "Design Patterns For LLD",
        "file": "design-patterns-for-lld.md",
        "concepts": [
          {
            "title": "Factory pattern",
            "anchor": "factory-pattern"
          },
          {
            "title": "Strategy pattern",
            "anchor": "strategy-pattern"
          },
          {
            "title": "Observer pattern",
            "anchor": "observer-pattern"
          },
          {
            "title": "Decorator pattern",
            "anchor": "decorator-pattern"
          },
          {
            "title": "State pattern",
            "anchor": "state-pattern"
          }
        ]
      },
      {
        "id": "machine-coding-lld-case-studies",
        "title": "Machine Coding & LLD Case Studies",
        "file": "machine-coding-lld-case-studies.md",
        "concepts": [
          {
            "title": "Parking lot design",
            "anchor": "parking-lot-design"
          },
          {
            "title": "Elevator system design",
            "anchor": "elevator-system-design"
          },
          {
            "title": "LRU cache design",
            "anchor": "lru-cache-design"
          },
          {
            "title": "BookMyShow / ticket booking LLD",
            "anchor": "bookmyshow-ticket-booking-lld"
          },
          {
            "title": "Splitwise / expense sharing LLD",
            "anchor": "splitwise-expense-sharing-lld"
          }
        ]
      }
    ]
  }
];
