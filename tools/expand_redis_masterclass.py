import os
import sys
import tempfile
import time
import re
import html as html_lib

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def atomic_write(filepath, content):
    d = os.path.dirname(os.path.abspath(filepath))
    with tempfile.NamedTemporaryFile('w', dir=d, delete=False, encoding='utf-8') as tf:
        tf.write(content)
        temp_name = tf.name
    for attempt in range(4):
        try:
            os.replace(temp_name, filepath)
            break
        except OSError:
            if attempt == 3:
                raise
            time.sleep(0.1 * (attempt + 1))
    if os.path.exists(temp_name):
        try:
            os.unlink(temp_name)
        except OSError:
            pass


REDIS_SUBSECTIONS = [
    {
        "num": "13.1",
        "title": "Redis Architecture, Event Loop, Memory Model & Wire Protocol",
        "desc": "How Redis achieves sub-millisecond tail latencies via single-threaded epoll/kqueue multiplexing, pipelined RESP2/RESP3 framing, jemalloc memory layout, and fork Copy-on-Write semantics.",
        "concepts": [
            ("13.1.1", "Single-Threaded Event Loop & I/O Multiplexing (epoll/kqueue, aeEventLoop & Redis 6+ Threaded I/O)",
             "Why a single command-execution thread eliminates mutex contention and context switching, how aeEventLoop polls thousands of non-blocking sockets via epoll/kqueue, and how Redis 6+ offloads socket read/write parsing to I/O threads.",
             "https://www.youtube.com/watch?v=No8JvCwR5P8", "00:00", "Yatharth Verma", "https://redis.io/docs/latest/develop/get-started/data-store/"),
            ("13.1.2", "RESP2 & RESP3 Wire Protocol, Command Pipelining & Round-Trip Time (RTT) Elimination",
             "Binary-safe length-prefixed framing in RESP2 vs RESP3 push/map/attribute types, batching hundreds of commands in a single TCP write with pipelining, and avoiding RTT bottlenecks without blocking other clients.",
             "https://www.youtube.com/watch?v=cNUC4qXZ_A8", "00:00", "PingToPrompt", "https://redis.io/docs/latest/develop/reference/protocol-spec/"),
            ("13.1.3", "Memory Allocator Internals (jemalloc), Fragmentation Ratio, redisObject & Listpack Compression",
             "Anatomy of 16-byte redisObject headers, jemalloc slab/arena allocation reducing fragmentation, mem_fragmentation_ratio > 1.5 vs < 1.0 swap danger, and compact ziplist/listpack encodings for small hashes and zsets.",
             "https://www.youtube.com/watch?v=h30k7YixrMo", "00:00", "Arpit Bhayani", "https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/memory-optimization/"),
            ("13.1.4", "Valkey, Redis Licensing Evolution & Forking Copy-on-Write (COW) Memory Overhead",
             "Open-source governance split to Linux Foundation Valkey 8+, multi-threaded I/O improvements, and why BGSAVE/BGREWRITEAOF fork() can double RAM usage under heavy write churn via OS 4KB page Copy-on-Write.",
             "https://www.youtube.com/watch?v=wWTjxLcMVsg", "00:00", "Anton Putra", "https://valkey.io/topics/"),
        ],
    },
    {
        "num": "13.2",
        "title": "Core & Advanced In-Memory Data Structures",
        "desc": "Internal representations, Big-O guarantees, and production engineering patterns for Strings, Hashes, Lists, Sets, Sorted Sets, HyperLogLog, Bloom Filters, and Redis Streams.",
        "concepts": [
            ("13.2.1", "Strings (SDS Dynamic Strings), Atomic Counters (INCR/DECR) & Bitfields (SETBIT / BITFIELD)",
             "Why Simple Dynamic Strings (SDS) store O(1) length and pre-allocate free space unlike C strings, binary-safe 512MB payloads, atomic INCR/INCRBY counters, and memory-dense daily active user tracking via Bitmaps.",
             "https://www.youtube.com/watch?v=vg71BKWJQdw", "00:00", "Concept && Coding - by Shrayansh", "https://redis.io/docs/latest/develop/data-types/strings/"),
            ("13.2.2", "Hashes (listpack vs hashtable), Lists (quicklist), Blocking Queues (BLPOP) & Sets (intset)",
             "Packing object fields efficiently in Hashes with listpack thresholds, doubly-linked quicklists of packed nodes for O(1) LPUSH/RPOP queues, BLPOP worker blocking, and O(1) Set intersections/unions.",
             "https://www.youtube.com/watch?v=ynKFI40oEKg", "00:00", "Eric Tech", "https://redis.io/docs/latest/develop/data-types/hashes/"),
            ("13.2.3", "Sorted Sets (ZSET: Dual dict + skiplist O(log N)), Real-Time Leaderboards & Priority Queues",
             "How Redis pairs a hash table (O(1) score lookup by member) with a probabilistic skiplist (O(log N) range queries by rank/score) to power real-time leaderboards, delayed job queues, and sliding-window logs.",
             "https://www.youtube.com/watch?v=MUKlxdBQZ7g", "00:00", "Redis", "https://redis.io/docs/latest/develop/data-types/sorted-sets/"),
            ("13.2.4", "Probabilistic & Streaming Structures: HyperLogLog (12KB), Bloom Filters, Geo & Redis Streams",
             "Estimating billions of unique visitors in a fixed 12KB HyperLogLog (<0.81% error), sub-linear Bloom Filter membership checks, Geohash proximity queries, and persistent Redis Streams with Consumer Groups & PEL.",
             "https://www.youtube.com/watch?v=MunL8nnwscQ", "00:00", "Redis", "https://redis.io/docs/latest/develop/data-types/streams/"),
        ],
    },
    {
        "num": "13.3",
        "title": "Caching Topologies, Eviction Policies & Failure Mode Mitigations",
        "desc": "Read/write caching architectures, approximated LRU/LFU eviction internals, defending against penetration/avalanche/stampede storms, and CDC cache invalidation.",
        "concepts": [
            ("13.3.1", "Caching Topologies: Cache-Aside (Lazy), Read-Through, Write-Through & Write-Behind (Write-Back)",
             "Comparing application-managed Cache-Aside against Read-Through providers, synchronous Write-Through durability, and high-throughput asynchronous Write-Behind batching (plus stale-cache race conditions).",
             "https://www.youtube.com/watch?v=V1oGVbxD8mk", "00:00", "CodeLucky", "https://redis.io/docs/latest/develop/use-cases/"),
            ("13.3.2", "Eviction Policies & Memory Pressure: Approximated allkeys-lru, volatile-lru, allkeys-lfu & maxmemory",
             "How Redis avoids global LRU doubly-linked list overhead using randomized N-key sampling (maxmemory-samples), 24-bit Morris counter logarithmic frequency decay in LFU, and volatile-ttl vs noeviction OOM errors.",
             "https://www.youtube.com/watch?v=72eZWhx4mDs", "00:00", "Java Techie", "https://redis.io/docs/latest/develop/reference/eviction/"),
            ("13.3.3", "Cache Failure Modes: Cache Penetration, Cache Avalanche (Jittered TTLs) & Cache Stampede",
             "Distinguishing missing-key DB floods (Penetration), synchronized mass key expiration (Avalanche), and hot-key expiration under massive concurrency (Stampede / Thundering Herd).",
             "https://www.youtube.com/watch?v=HpvokZchYKY", "00:00", "TheNextGenFreak", "https://redis.io/docs/latest/develop/data-types/probabilistic/bloom-filter/"),
            ("13.3.4", "Stampede & Consistency Mitigations: Singleflight Mutexes, XFetch Early Expiration & CDC Invalidation",
             "Coalescing duplicate origin fetches with singleflight / Redis mutex locks, mathematical Probabilistic Early Expiration (XFetch), caching short-TTL null sentinels, and Debezium CDC out-of-band cache invalidation.",
             "https://www.youtube.com/watch?v=WMH_zBio1Mo", "00:00", "SaaS RTO", "https://redis.io/docs/latest/develop/clients/patterns/distributed-locks/"),
        ],
    },
    {
        "num": "13.4",
        "title": "Persistence, Replication, Sentinel HA & Redis Cluster",
        "desc": "RDB snapshot forks vs AOF durability logs, PSYNC2 replication and Sentinel quorum failovers, and Redis Cluster 16,384 hash slot sharding internals.",
        "concepts": [
            ("13.4.1", "Persistence Mechanics: RDB Snapshots (BGSAVE Fork) vs AOF (Append-Only File & Multi-Part AOF)",
             "Point-in-time compact binary RDB dumps for fast restarts vs command-logged AOF durability, Redis 7+ Multi-Part AOF eliminating rewrite memory duplication, and recovery startup order.",
             "https://www.youtube.com/watch?v=mi7RNK-NFKI", "00:00", "TheNextGenFreak", "https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/"),
            ("13.4.2", "AOF Fsync Policies (always, everysec, no), bgrewriteaof & Hybrid RDB-AOF Preamble",
             "Latency vs durability across fsync=always, everysec (up to 1s data loss), and no, preventing fsync stalls during BGREWRITEAOF via no-appendfsync-on-rewrite, and fast RDB-preamble hybrid AOF loading.",
             "https://www.youtube.com/watch?v=r5qsVg1KvuU", "00:00", "Coditioning", "https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/"),
            ("13.4.3", "Replication & Redis Sentinel: PSYNC2 Partial Resync, Quorum (SDOWN/ODOWN) & Automatic Failover",
             "Asynchronous primary-replica replication via repl_backlog_buffer and replication IDs (PSYNC2), WAIT synchronous durability, Sentinel SDOWN vs ODOWN quorum voting, and min-replicas-to-write split-brain protection.",
             "https://www.youtube.com/watch?v=sbzz3KRZbPU", "00:00", "Prepare-sh", "https://redis.io/docs/latest/operate/oss_and_stack/management/sentinel/"),
            ("13.4.4", "Redis Cluster Architecture: 16,384 Hash Slots (CRC16), Gossip Bus, Hash Tags & MOVED/ASK Redirects",
             "Partitioning keyspace across 16,384 CRC16 slots, cluster gossip bus failure detection, pinning multi-key operations with {hashtag} keys to avoid CROSSSLOT errors, and live resharding MOVED vs ASK client redirects.",
             "https://www.youtube.com/watch?v=0G5_w2lX02o", "00:00", "System Design Lab", "https://redis.io/docs/latest/operate/oss_and_stack/management/scaling/"),
        ],
    },
    {
        "num": "13.5",
        "title": "Atomicity, Distributed Locking, Lua Scripting & Pub/Sub",
        "desc": "Optimistic WATCH/MULTI/EXEC pipelines, atomic Lua scripts and Redis 7 Functions, Redlock safety & fencing tokens, and Sharded Pub/Sub vs Streams.",
        "concepts": [
            ("13.5.1", "Redis Transactions (MULTI/EXEC), Optimistic Concurrency (WATCH CAS) & No-Rollback Semantics",
             "Queuing commands atomically inside MULTI/EXEC, implementing Compare-And-Set optimistic locking with WATCH, and why Redis intentionally executes valid queued commands even if one command fails at runtime.",
             "https://www.youtube.com/watch?v=zVMP1IuiZB4", "00:00", "Oddly Yogi", "https://redis.io/docs/latest/develop/interact/transactions/"),
            ("13.5.2", "Server-Side Atomicity: Lua Scripts (EVAL/EVALSHA) & Redis 7 Functions (FUNCTION LOAD)",
             "Executing multi-step read-modify-write logic atomically inside the single event loop via EVALSHA, avoiding script-cache eviction bugs with Redis 7 persistent Functions, and preventing long-running Lua scripts from blocking.",
             "https://www.youtube.com/watch?v=uptxcaf2s_4", "00:00", "DevMonk", "https://redis.io/docs/latest/develop/interact/programmability/eval-intro/"),
            ("13.5.3", "Distributed Locks: SET NX PX, Fencing Tokens, Lease Watchdogs & Redlock Controversy",
             "Safe single-instance locks using SET key token NX PX ttl with atomic Lua unlock verification, GC-pause lease expiry hazards, monotonic fencing tokens, and Kleppmann vs Antirez analysis of multi-node Redlock.",
             "https://www.youtube.com/watch?v=qY4MfWv01pI", "00:00", "ByteMonk", "https://redis.io/docs/latest/develop/clients/patterns/distributed-locks/"),
            ("13.5.4", "Pub/Sub Messaging vs Sharded Pub/Sub (SPUBLISH) vs Redis Streams & Keyspace Notifications",
             "Why classic Pub/Sub drops messages for disconnected subscribers and broadcasts across every cluster node, Redis 7 Sharded Pub/Sub (SPUBLISH/SSUBSCRIBE) slot routing, and Keyspace Notifications overhead.",
             "https://www.youtube.com/watch?v=61EOtB1vm8k", "00:00", "shubham.patel03", "https://redis.io/docs/latest/develop/interact/pubsub/"),
        ],
    },
    {
        "num": "13.6",
        "title": "Distributed Use Cases, Client Optimization, Security & Production Tuning",
        "desc": "Atomic Lua rate limiters and idempotency stores, RESP3 client-side caching, ACLs and TLS hardening, and Linux kernel/SLOWLOG production diagnostics.",
        "concepts": [
            ("13.6.1", "Distributed Use Cases: Rate Limiting (Token Bucket / Sliding Window Lua), Sessions & Idempotency",
             "Building exact Sliding Window Log (ZSET) and Token Bucket (Lua + Hash) distributed rate limiters, sticky-free session stores, and atomic Idempotency-Key deduplication caches.",
             "https://www.youtube.com/watch?v=LPtQguD8_K0", "00:00", "Real STEM", "https://redis.io/glossary/rate-limiting/"),
            ("13.6.2", "Client-Side Caching (CLIENT TRACKING BCAST/OPTIN), RESP3 Push Invalidation & Pool Sizing",
             "Eliminating even sub-millisecond network hops with L1 in-process caching backed by server-assisted RESP3 invalidation tables (Default vs Prefix BCAST mode), plus sizing multiplexed async client connections.",
             "https://www.youtube.com/watch?v=ILxO68z0OmQ", "00:00", "Salvatore Sanfilippo", "https://redis.io/docs/latest/develop/clients/client-side-caching/"),
            ("13.6.3", "Redis Security: ACLs (ACL SETUSER), TLS/mTLS Encryption, Command Hardening & Protected Mode",
             "Replacing shared requirepass with granular per-user ACL categories (@read, @write, -@dangerous) and key pattern restrictions (~app:*), disabling FLUSHALL/KEYS *, and enabling TLS 1.3 transport encryption.",
             "https://www.youtube.com/watch?v=57SgF5iht8Y", "00:00", "Redis", "https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/"),
            ("13.6.4", "Production Diagnostics & Linux Kernel Tuning: SLOWLOG, LATENCY DOCTOR, overcommit & Disabling THP",
             "Hunting O(N) blockers (KEYS *, HGETALL on huge hashes) with SLOWLOG GET and SCAN, LATENCY DOCTOR diagnostics, setting vm.overcommit_memory=1 and net.core.somaxconn, and disabling Transparent Huge Pages (THP).",
             "https://www.youtube.com/watch?v=HIrlMqbApv0", "00:00", "Nick Janetakis", "https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/latency/"),
        ],
    },
]

REDIS_RESOURCES_HTML = '''  <div class="resources-section">
    <div class="head" onclick="this.parentElement.classList.toggle('open')">
      <h4>📚 Learn this domain</h4>
      <div><span class="count">6 curated resources</span><span class="chevron">▶</span></div>
    </div>
    <div class="resources-body">
      <div class="res-grid">
        <a class="res-link" href="https://redis.io/docs/latest/" target="_blank" rel="noopener"><span class="res-icon">📖</span><span class="res-title">Redis Official Documentation</span><span class="res-source">Redis</span></a>
        <a class="res-link" href="https://redis.io/docs/latest/develop/data-types/" target="_blank" rel="noopener"><span class="res-icon">🧱</span><span class="res-title">Redis Data Types &amp; Internals Guide</span><span class="res-source">Redis</span></a>
        <a class="res-link" href="https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/" target="_blank" rel="noopener"><span class="res-icon">💾</span><span class="res-title">RDB &amp; AOF Persistence Specification</span><span class="res-source">Redis</span></a>
        <a class="res-link" href="https://redis.io/docs/latest/operate/oss_and_stack/management/scaling/" target="_blank" rel="noopener"><span class="res-icon">🏛️</span><span class="res-title">Redis Cluster &amp; Hash Slots Architecture</span><span class="res-source">Redis</span></a>
        <a class="res-link" href="https://redis.io/docs/latest/develop/clients/patterns/distributed-locks/" target="_blank" rel="noopener"><span class="res-icon">🔒</span><span class="res-title">Distributed Locks &amp; Redlock Pattern</span><span class="res-source">Redis</span></a>
        <a class="res-link" href="https://valkey.io/topics/" target="_blank" rel="noopener"><span class="res-icon">⚡</span><span class="res-title">Valkey Open-Source Documentation</span><span class="res-source">Linux Foundation</span></a>
      </div>
    </div>
  </div>'''

SISTER_GUIDES_HTML = '''  <div class="sister-guides-card">
    <div class="sister-title">🚀 Complete Engineering &amp; Cloud Masterclasses</div>
    <div class="sister-grid">
      <a class="sister-link" href="tech_aws.html">☁️ AWS Cloud</a>
      <a class="sister-link" href="tech_azure.html">🔷 Microsoft Azure</a>
      <a class="sister-link" href="tech_gcp.html">🌐 Google Cloud Platform</a>
      <a class="sister-link" href="tech_linux.html">🐧 Linux &amp; CLI</a>
      <a class="sister-link" href="tech_git.html">🌿 Git &amp; GitHub</a>
      <a class="sister-link" href="tech_docker_k8s.html">🐳 Docker &amp; Kubernetes</a>
      <a class="sister-link" href="tech_cicd.html">🚀 CI/CD Pipelines</a>
      <a class="sister-link" href="tech_terraform.html">🏗️ Terraform IaC</a>
      <a class="sister-link" href="tech_kafka.html">⚡ Apache Kafka</a>
      <a class="sister-link" href="tech_spark.html">📊 Apache Spark</a>
      <a class="sister-link" href="tech_postgres.html">🐘 PostgreSQL</a>
      <a class="sister-link" href="tech_redis.html">🔴 Redis Caching</a>
      <a class="sister-link" href="tech_java.html">☕ Java &amp; Spring Boot</a>
      <a class="sister-link" href="tech_fastapi.html">🐍 Python &amp; FastAPI</a>
      <a class="sister-link" href="tech_apis.html">🔌 Production APIs</a>
      <a class="sister-link active-hub" href="cloud_aws_azure.html">☁️ Cloud Platforms Hub &rarr;</a>
      <a class="sister-link active-hub" href="all_tech.html">🌐 All-in-One Tech Portal &rarr;</a>
    </div>
  </div>'''


def render_subsections_html(subsections):
    out = []
    for sub in subsections:
        num = sub["num"]
        title = sub["title"]
        desc = sub["desc"]
        concepts = sub["concepts"]

        out.append('  <div class="subsection">')
        out.append('    <div class="subsection-head">')
        out.append(f'      <span class="subsection-tag">{num}</span>')
        out.append(f'      <h3>{html_lib.escape(title)}</h3>')
        out.append(f'      <span style="font-size:11px;color:var(--text-faint);">{len(concepts)} concepts</span>')
        out.append('    </div>')
        out.append(f'    <div class="subsection-desc">{html_lib.escape(desc)}</div>')
        out.append('    <ol class="concepts">')

        for cid, cname, cdesc, yurl, ytime, ychan, docurl in concepts:
            norm_name = re.sub(r'[^a-z0-9]+', ' ', cname.lower()).strip()

            start_s = "0"
            m = re.search(r'[?&]t=(\d+)s?', yurl)
            if m:
                start_s = m.group(1)

            out.append(f'      <li data-cid="{cid}" data-name="{html_lib.escape(norm_name)}">')
            out.append('        <div class="done-check" title="Mark as done"></div>')
            out.append('        <div class="bookmark-star" title="Bookmark">☆</div>')
            out.append('        <div>')
            out.append(f'          <div class="cname">{html_lib.escape(cname)}</div>')
            out.append(f'          <div style="font-size:11.5px;color:var(--text-faint);margin-top:2px">{html_lib.escape(cdesc)}</div>')
            out.append('        </div>')
            out.append(
                f'        <div class="res-links">'
                f'<a class="video" href="{html_lib.escape(yurl)}" data-vtitle="{html_lib.escape(cname)}" '
                f'data-vchannel="{html_lib.escape(ychan)}" data-start="{start_s}" data-vdur="" '
                f'target="_blank" rel="noopener" title="Watch walkthrough: {html_lib.escape(cname)}">🎬YT</a>'
                f'<a href="{html_lib.escape(docurl)}" target="_blank" rel="noopener" title="Official Documentation">🌐Doc</a>'
                f'</div>'
            )
            out.append('      </li>')

        out.append('    </ol>')
        out.append('  </div>')
    return '\n'.join(out)


def update_section_13(sec13_text, standalone=False):
    sec13_new = re.sub(
        r'<span class="focus-bar-stats">[^<]+</span>',
        '<span class="focus-bar-stats">24 concepts &bull; 6 subsections</span>',
        sec13_text
    )
    if standalone:
        sec13_new = re.sub(
            r'\s*<div class="focus-bar-right">[\s\S]*?</div>\s*(?=</div>\s*<div class="section-banner")',
            '\n  ',
            sec13_new,
            count=1
        )
    sec13_new = re.sub(
        r'<div class="meta">[^<]+</div>',
        '<div class="meta">6 subsections · 24 concepts</div>',
        sec13_new
    )
    sec13_new = re.sub(
        r'<div class="pct-text" data-pp-text="13">[^<]+</div>',
        '<div class="pct-text" data-pp-text="13">0 / 24</div>',
        sec13_new
    )
    sec13_new = re.sub(
        r'<div class="section-desc">[\s\S]*?</div>\s*(?=<div class="resources-section">)',
        '''<div class="section-desc">
    <div class="tagline">Sub-millisecond in-memory computing: single-threaded epoll event loop, RESP3 pipelining, jemalloc &amp; listpack encodings, Cache-Aside &amp; XFetch stampede defense, RDB/AOF durability, Sentinel HA, 16,384-slot Redis Cluster, Lua atomicity &amp; Redlock.</div>
    <div class="row"><b>Core Focus:</b> SDS/Skiplist/HyperLogLog/Streams internals, approximated LRU/LFU eviction, BGSAVE fork Copy-on-Write, PSYNC2 failover, CRC16 hash tags, Lua/Redis Functions, CLIENT TRACKING &amp; Linux THP/overcommit tuning.</div>
    <div class="row"><b>Production Trade-offs:</b> RAM cost &amp; COW fork headroom vs persistence fsync durability, Redis Cluster cross-slot limits vs hash tags, and Redlock lease expiry vs monotonic fencing tokens.</div>
  </div>
''',
        sec13_new,
        count=1
    )
    sec13_new = re.sub(
        r'<div class="resources-section">[\s\S]*?</div>\s*</div>\s*</div>\s*(?=<div class="subsection">)',
        REDIS_RESOURCES_HTML + '\n',
        sec13_new,
        count=1
    )
    subs_html = render_subsections_html(REDIS_SUBSECTIONS)
    sub_start = sec13_new.find('<div class="subsection">')
    sub_end = sec13_new.rfind('</section>')
    if sub_start == -1 or sub_end == -1:
        raise ValueError("Could not locate subsection boundaries in section-13")
    return sec13_new[:sub_start] + subs_html + '\n' + sec13_new[sub_end:]


def expand_tech_redis():
    p = os.path.join(ROOT, 'tech_redis.html')
    with open(p, 'r', encoding='utf-8') as f:
        html = f.read()

    if '<body data-site="cloud">' not in html:
        html = html.replace('<body>', '<body data-site="cloud">', 1)
    html = re.sub(
        r'<div class="edition">[^<]+</div>',
        '<div class="edition">Caching &amp; In-Memory Data &middot; Masterclass 10 &middot; 6 Subsections &middot; 24 Concepts</div>',
        html
    )
    html = re.sub(
        r'<p class="subtitle">[^<]+</p>',
        '<p class="subtitle">Ultra-low-latency in-memory engineering: epoll event loop, RESP3 pipelining, jemalloc &amp; listpack memory, SDS/Skiplist/HyperLogLog/Streams, LRU/LFU eviction, stampede defense, RDB/AOF, Sentinel, Redis Cluster, Lua/Functions, Redlock, CLIENT TRACKING &amp; Linux tuning.</p>',
        html,
        count=1
    )
    html = re.sub(
        r'<div class="stats">[\s\S]*?</div>\s*</div>\s*</div>',
        '''<div class="stats">
    <div class="stat"><div class="n">6</div><div class="l">Subsections</div></div>
    <div class="stat"><div class="n">24</div><div class="l">Concepts</div></div>
    <div class="stat"><div class="n">100%</div><div class="l">Curated</div></div>
    <div class="stat"><div class="n">25+</div><div class="l">Verified Docs &amp; Labs</div></div>
  </div>''',
        html,
        count=1
    )
    html = re.sub(
        r'<span class="pct" id="overall-pct">[^<]+</span>',
        '<span class="pct" id="overall-pct">0 / 24</span>',
        html
    )
    html = re.sub(
        r'placeholder="Search \d+ concepts…"',
        'placeholder="Search 24 concepts…"',
        html
    )

    # Delegate theme-toggle to shared navbar toggle when available
    html = re.sub(
        r"  const themeBtn = document\.getElementById\('theme-toggle'\);\s*\n\s*if \(themeBtn\) themeBtn\.addEventListener\('click', \(\) => \{[\s\S]*?\}\);",
        '''  const themeBtn = document.getElementById('theme-toggle');
  if (themeBtn) themeBtn.addEventListener('click', () => {
    const navBtn = document.querySelector('[data-hub-theme]');
    if (navBtn) { navBtn.click(); return; }
    let cur = localStorage.getItem(KEY_THEME) || 'dark';
    let next = cur === 'light' ? 'dark' : (cur === 'dark' ? 'black' : 'light');
    localStorage.setItem(KEY_THEME, next);
    localStorage.setItem('hub_theme', next);
    applyTheme(next);
  });''',
        html,
        count=1
    )

    sec13_match = re.search(r'(<section class="section domain-section"[^>]*id="section-13"[\s\S]*?</section>)', html)
    if not sec13_match:
        raise ValueError("Could not find section-13 in tech_redis.html")

    sec13_text = sec13_match.group(1)
    sec13_new = update_section_13(sec13_text, standalone=True)
    html = html.replace(sec13_text, sec13_new, 1)

    html = re.sub(
        r'<div class="sister-guides-card">[\s\S]*?</div>\s*</div>\s*(?=</div>\s*<script>)',
        SISTER_GUIDES_HTML + '\n',
        html,
        count=1
    )

    atomic_write(p, html)
    print("Saved tech_redis.html successfully!")


def expand_all_tech():
    p = os.path.join(ROOT, 'all_tech.html')
    with open(p, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update card-redis in domain deck
    card_match = re.search(
        r'(<div class="domain-card[^"]*"[^>]*id="card-redis"[\s\S]*?)(?=<div class="domain-card"|<div class="domain-crosslink-card")',
        html
    )
    if not card_match:
        raise ValueError("Could not find card-redis in all_tech.html")
    old_card = card_match.group(1)
    new_card = re.sub(
        r'<p class="domain-card-desc">[\s\S]*?</p>',
        '<p class="domain-card-desc">Event loop &amp; RESP3, jemalloc/listpack memory, SDS/Skiplist/Streams, LRU/LFU eviction, stampede defense, RDB/AOF, Sentinel HA, Redis Cluster, Lua/Redlock &amp; Linux tuning.</p>',
        old_card,
        count=1
    )
    new_card = re.sub(
        r'<div class="domain-card-chips">[\s\S]*?</div>',
        '''<div class="domain-card-chips">
<span class="domain-card-chip">6 Subsections</span>
<span class="domain-card-chip">24 Concepts</span>
<span class="domain-card-chip highlight">Event Loop, Cluster, Redlock, Lua &amp; Tuning</span>
</div>''',
        new_card,
        count=1
    )
    html = html.replace(old_card, new_card, 1)
    print("Updated card-redis in all_tech.html")

    # 2. Update Section 13 (Redis) inside all_tech.html
    sec13_match = re.search(r'(<section class="section domain-section"[^>]*id="section-13"[\s\S]*?</section>)', html)
    if not sec13_match:
        raise ValueError("Could not find section-13 in all_tech.html")
    sec13_text = sec13_match.group(1)
    sec13_new = update_section_13(sec13_text, standalone=False)
    html = html.replace(sec13_text, sec13_new, 1)
    print("Updated section-13 in all_tech.html")

    # 3. Re-derive actual subsection and concept totals across all_tech.html
    total_subs = len(re.findall(r'<div class="subsection">', html))
    total_concepts = len(re.findall(r'<li[^>]*\bdata-cid="', html))
    print(f"Computed all_tech.html totals: {total_subs} subsections, {total_concepts} concepts")

    html = re.sub(
        r'<div class="edition">[^<]*All-in-One Tech[^<]*</div>',
        f'<div class="edition">v4 · All-in-One Tech &amp; Engineering Portal · 13 Disciplines · {total_subs} Subsections · {total_concepts} Concepts</div>',
        html,
        count=1
    )
    html = re.sub(
        r'(<div class="stat"><div class="n">)\d+(</div><div class="l">Subsections</div></div>)',
        rf'\g<1>{total_subs}\g<2>',
        html
    )
    html = re.sub(
        r'(<div class="stat"><div class="n">)\d+(</div><div class="l">Concepts</div></div>)',
        rf'\g<1>{total_concepts}\g<2>',
        html
    )
    html = re.sub(
        r'<span class="pct" id="overall-pct">[^<]+</span>',
        f'<span class="pct" id="overall-pct">0 / {total_concepts}</span>',
        html
    )
    html = re.sub(
        r'placeholder="Search \d+ engineering &amp; infrastructure concepts…"',
        f'placeholder="Search {total_concepts} engineering &amp; infrastructure concepts…"',
        html
    )

    atomic_write(p, html)
    print("Saved all_tech.html successfully!")


if __name__ == '__main__':
    expand_tech_redis()
    expand_all_tech()
    print("Finished expanding Redis & In-Memory Caching Masterclass!")
