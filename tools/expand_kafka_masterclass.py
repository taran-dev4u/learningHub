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


KAFKA_SUBSECTIONS = [
    {
        "num": "10.1",
        "title": "Kafka Architecture, Distributed Commit Log & KRaft Quorum",
        "desc": "Foundational storage and control-plane internals: immutable partitioned commit logs, Linux OS page-cache zero-copy transfers, and Raft-based KRaft metadata consensus.",
        "concepts": [
            ("10.1.1", "Distributed Commit Log: Append-Only Segments, Offsets & Sequential Disk I/O",
             "Why Kafka treats topics as immutable, monotonically indexed append-only commit logs, achieving disk throughput near memory speeds by avoiding random seeks and tracking consumer positions via numeric offsets.",
             "https://www.youtube.com/watch?v=R873BlNVUB4", "00:00", "Hussein Nasser", "https://kafka.apache.org/44/getting-started/introduction/"),
            ("10.1.2", "Broker Internals: Linux OS Page Cache, Zero-Copy sendfile() & Network Threads",
             "Bypassing JVM heap overhead by relying on Linux OS page cache for writes/reads, DMA zero-copy socket transfers via sendfile() (4 copies -> 2 copies, 4 context switches -> 2), and acceptor/processor reactor thread pools.",
             "https://www.youtube.com/watch?v=V2tQ4kHZefw", "00:00", "Pipeline Whiteboard", "https://kafka.apache.org/44/design/design/"),
            ("10.1.3", "KRaft Consensus Architecture: ZooKeeper Elimination, Raft Controller Quorum & Metadata Log",
             "Replacing external ZooKeeper ensembles with an embedded Raft quorum storing cluster state in the __cluster_metadata topic, supporting millions of partitions with sub-second controller failover.",
             "https://www.youtube.com/watch?v=6YL0L4lb9iM", "00:00", "Confluent, an IBM Company", "https://kafka.apache.org/44/operations/kraft/"),
            ("10.1.4", "Topics, Partitions & Key-Based Sharding: Ordering Guarantees, Partition Sizing & Hot Partitions",
             "Scaling horizontal throughput via partition sharding, per-partition total order vs global non-ordering, Murmur2 key hashing, mitigating skewed hot keys, and balancing partition count against file descriptors and rebalance latency.",
             "https://www.youtube.com/watch?v=y9BStKvVzSs", "00:00", "Confluent, an IBM Company", "https://kafka.apache.org/44/implementation/distribution/"),
        ],
    },
    {
        "num": "10.2",
        "title": "Replication, Durability, Storage & Log Compaction",
        "desc": "High-availability replication protocols, In-Sync Replicas, High Watermark safety, segment index structures, and key-based log compaction mechanics.",
        "concepts": [
            ("10.2.1", "Partition Replication: Leader/Follower Model, In-Sync Replicas (ISR) & Unclean Leader Election",
             "How partition leaders serve all client reads/writes while followers pull replication batches, ISR membership thresholds (replica.lag.time.max.ms), Eligible Leader Replicas (ELR), and availability vs data-loss under unclean.leader.election.enable.",
             "https://www.youtube.com/watch?v=MDKQWx4Zvqs", "00:00", "SystemDR - Scalable System Design", "https://kafka.apache.org/44/operations/eligible-leader-replicas/"),
            ("10.2.2", "High Watermark (HW), Leader Epoch & Log Truncation Consistency",
             "Preventing consumers from reading uncommitted records via the High Watermark offset, why HW-only truncation caused silent divergence on rapid leader flaps, and how Leader Epochs guarantee deterministic log convergence.",
             "https://www.youtube.com/watch?v=9g5LdsnrM1o", "00:00", "DevXOps Tech", "https://kafka.apache.org/44/design/protocol/"),
            ("10.2.3", "Log Segments, Index Files (.index, .timeindex) & Retention Policies (Time/Size)",
             "Physical partition storage layout: rolling .log segments (segment.bytes / segment.ms), sparse offset (.index) and timestamp (.timeindex) binary-search indexes, and background retention deletion.",
             "https://www.youtube.com/watch?v=hDi2VPiAmt0", "00:00", "CodeOvation", "https://kafka.apache.org/44/implementation/log/"),
            ("10.2.4", "Log Compaction (cleanup.policy=compact): Tombstones, Cleaner Threads & State Materialization",
             "Retaining at least the latest value per message key forever for CDC and KTable state recovery, dirty-ratio compaction triggers, null-value tombstone records, and delete.retention.ms grace windows.",
             "https://www.youtube.com/watch?v=VAkhYxu1qII", "00:00", "Confluent, an IBM Company", "https://kafka.apache.org/44/configuration/topic-configs/"),
        ],
    },
    {
        "num": "10.3",
        "title": "Producer Internals, Delivery Guarantees & Exactly-Once Semantics (EOS)",
        "desc": "Client-side batching pipelines, compression trade-offs, durability acks, idempotent sequence numbers, and cross-partition transactional semantics.",
        "concepts": [
            ("10.3.1", "Producer Pipeline: Serialization, Partitioners (Sticky/Custom), RecordAccumulator & Sender Thread",
             "Thread-safe producer architecture: interceptors, serializers, UniformStickyPartitioner batch filling, per-partition Deque buffers in RecordAccumulator (buffer.memory, max.block.ms), and asynchronous Sender I/O.",
             "https://www.youtube.com/watch?v=dGCDrKmapoQ", "00:00", "Concept && Coding - by Shrayansh", "https://kafka.apache.org/44/implementation/network-layer/"),
            ("10.3.2", "Batching & Compression Tuning: linger.ms, batch.size, LZ4/Zstd/Snappy & Throughput vs Latency",
             "Maximizing network and broker efficiency by tuning batch.size and linger.ms, selecting end-to-end batch compression codecs (lz4, zstd, snappy, gzip), and avoiding broker-side recompression CPU spikes.",
             "https://www.youtube.com/watch?v=0oaMYAy7OYg", "00:00", "Interview Deep Dives", "https://kafka.apache.org/44/configuration/producer-configs/"),
            ("10.3.3", "Durability & Ack Semantics: acks=0/1/all, min.insync.replicas & retries / delivery.timeout.ms",
             "Configuring zero-loss writes with acks=all paired with topic min.insync.replicas=2 (RF=3), bounded delivery.timeout.ms retries, and understanding max.in.flight.requests.per.connection ordering interactions.",
             "https://www.youtube.com/watch?v=nW2EYHNuBKk", "00:00", "Codetuber", "https://docs.confluent.io/platform/current/installation/configuration/topic-configs.html"),
            ("10.3.4", "Idempotent Producers (PID, Sequence Numbers) & Transactional EOS (TransactionCoordinator, read_committed)",
             "Eliminating retry duplicates via Producer ID + per-partition monotonic sequence numbers, and achieving atomic multi-partition read-process-write EOS via transactional.id, __transaction_state two-phase commits, and isolation.level=read_committed.",
             "https://www.youtube.com/watch?v=Ki2D2o9aVl8", "00:00", "Confluent, an IBM Company", "https://kafka.apache.org/44/operations/transaction-protocol/"),
        ],
    },
    {
        "num": "10.4",
        "title": "Consumer Groups, Rebalancing Protocols & Resilience Patterns",
        "desc": "Group coordination, incremental cooperative rebalancing, safe offset commit mechanics, and production dead-letter / non-blocking retry topologies.",
        "concepts": [
            ("10.4.1", "Consumer Group Coordination: GroupCoordinator, __consumer_offsets, Poll Loop & Heartbeats",
             "Scaling consumption across group instances (max 1 consumer per partition), background heartbeat threads (session.timeout.ms, heartbeat.interval.ms), and avoiding poll-loop eviction (max.poll.interval.ms, max.poll.records).",
             "https://www.youtube.com/watch?v=e5uAhoT1hhU", "00:00", "Hussein Nasser", "https://kafka.apache.org/44/configuration/group-configs/"),
            ("10.4.2", "Partition Assignment & Rebalancing: Eager (Stop-the-World), CooperativeStickyAssignor & KIP-848",
             "Comparing Range, RoundRobin, and Sticky assignors; eliminating stop-the-world pauses with incremental CooperativeStickyAssignor; and the server-side KIP-848 next-gen consumer rebalance protocol.",
             "https://www.youtube.com/watch?v=CRz_2ygimgA", "00:00", "DevXOps Tech", "https://kafka.apache.org/44/operations/consumer-rebalance-protocol/"),
            ("10.4.3", "Offset Commit Strategies: Auto-Commit Risks, Manual commitSync/commitAsync & Static Membership",
             "Why enable.auto.commit=true risks at-most-once loss or duplicate spikes on crash, combining commitAsync() in the hot loop with commitSync() in rebalance listeners, and preventing rolling-restart storms via group.instance.id.",
             "https://www.youtube.com/watch?v=0OvLr6_wkn0", "00:00", "Interview Deep Dives", "https://kafka.apache.org/44/configuration/consumer-configs/"),
            ("10.4.4", "Poison Pills, Non-Blocking Retry Topics & Dead-Letter Queues (DLQ) with Backpressure",
             "Isolating malformed deserialization or transient downstream failures without stalling partition progress: tiered exponential retry topics, pause()/resume() backpressure, and dead-letter topic inspection/replay.",
             "https://www.youtube.com/watch?v=imD0PIR_Qdc", "00:00", "Code with Sam", "https://www.confluent.io/blog/error-handling-patterns-in-kafka/"),
        ],
    },
    {
        "num": "10.5",
        "title": "Kafka Ecosystem: Schema Registry, Kafka Connect & Kafka Streams",
        "desc": "Schema contract governance, declarative CDC and connector pipelines, and stateful real-time stream processing with local RocksDB state stores.",
        "concepts": [
            ("10.5.1", "Schema Registry & Wire Format: Avro, Protobuf, JSON Schema & Compatibility Modes",
             "Decoupling payload schemas from event bytes via 5-byte magic + schema ID headers, enforcing safe evolution rules (BACKWARD, FORWARD, FULL, TRANSITIVE), and preventing consumer deserialization breakages.",
             "https://www.youtube.com/watch?v=fT_tml-0eSw", "00:00", "The Lazy Senior", "https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html"),
            ("10.5.2", "Kafka Connect Architecture: Workers (Standalone vs Distributed), Source/Sink Connectors & SMTs",
             "Declarative data integration via Connector/Task parallelism, distributed internal config/offset/status topics, Single Message Transforms (SMTs) for lightweight routing/masking, and dead-letter error tolerance.",
             "https://www.youtube.com/watch?v=mdsNGujpsF8", "00:00", "Confluent, an IBM Company", "https://kafka.apache.org/44/kafka-connect/overview/"),
            ("10.5.3", "Change Data Capture (CDC) with Debezium: WAL Log Mining, Outbox Pattern & Snapshot Modes",
             "Streaming zero-impact row-level changes from PostgreSQL WAL / MySQL binlog, eliminating dual-write race conditions with the Transactional Outbox Pattern, and incremental lock-free snapshotting.",
             "https://www.youtube.com/watch?v=0Ib0hv90kvc", "00:00", "ByteDistrict", "https://debezium.io/documentation/reference/stable/architecture.html"),
            ("10.5.4", "Kafka Streams & ksqlDB: KStream, KTable, RocksDB State Stores, Changelog Topics & Windowing",
             "Stream-table duality, topology sub-task repartitioning, embedded RocksDB stateful aggregations backed by compacted changelog topics, standby replicas, and Tumbling/Hopping/Session event-time windows with grace periods.",
             "https://www.youtube.com/watch?v=eLugQaBSdPg", "00:00", "Interview Deep Dives", "https://kafka.apache.org/44/streams/architecture/"),
        ],
    },
    {
        "num": "10.6",
        "title": "Enterprise Operations, Tiered Storage, Geo-Replication & Observability",
        "desc": "Cloud-native object-storage offloading, multi-region disaster recovery, zero-trust mTLS/SASL/ACL security, and production lag/cluster telemetry.",
        "concepts": [
            ("10.6.1", "Tiered Storage (KIP-405) & RemoteLogManager: S3/GCS Object Offloading & Infinite Retention",
             "Separating compute from storage by asynchronously copying closed log segments to S3/GCS/Azure Blob while retaining hot segments on local NVMe, enabling fast broker replacements and historical replay without local disk bloat.",
             "https://www.youtube.com/watch?v=vzkOqLORBR8", "00:00", "Interview Deep Dives", "https://kafka.apache.org/44/operations/tiered-storage/"),
            ("10.6.2", "Multi-Cluster Geo-Replication: MirrorMaker 2 (MM2), Active-Active Topologies & Offset Translation",
             "Cross-region disaster recovery and active-active mirroring using Kafka Connect-based MM2, preventing replication loops via topic prefixing, checkpointing, and RemoteClusterUtils offset translation on failover.",
             "https://www.youtube.com/watch?v=S-qUM6kdtDw", "00:00", "Interview Deep Dives", "https://kafka.apache.org/44/operations/geo-replication-cross-cluster-data-mirroring/"),
            ("10.6.3", "Kafka Security: TLS Encryption, SASL (SCRAM/PLAIN/OAUTHBEARER), mTLS & Granular ACLs",
             "Securing client-broker and inter-broker traffic with TLS 1.3, authenticating principals via SASL/SCRAM-SHA-512, OIDC OAUTHBEARER, or mTLS certificates, and enforcing least-privilege topic/group ACLs.",
             "https://www.youtube.com/watch?v=1woDczncJyA", "00:00", "Interview Deep Dives", "https://kafka.apache.org/44/security/security-overview/"),
            ("10.6.4", "Production Observability & Capacity Planning: Consumer Lag, UnderReplicatedPartitions, JMX & Cruise Control",
             "Alerting on critical broker health invariants (UnderReplicatedPartitions, OfflinePartitionsCount, ActiveControllerCount, RequestHandlerAvgIdlePercent), tracking consumer lag with Burrow/Lag Exporter, and self-healing partition rebalancing via Cruise Control.",
             "https://www.youtube.com/watch?v=aTipSaBHSaA", "00:00", "Interview Deep Dives", "https://kafka.apache.org/44/operations/monitoring/"),
        ],
    },
]

KAFKA_RESOURCES_HTML = '''  <div class="resources-section">
    <div class="head" onclick="this.parentElement.classList.toggle('open')">
      <h4>📚 Learn this domain</h4>
      <div><span class="count">6 curated resources</span><span class="chevron">▶</span></div>
    </div>
    <div class="resources-body">
      <div class="res-grid">
        <a class="res-link" href="https://kafka.apache.org/documentation/" target="_blank" rel="noopener"><span class="res-icon">📖</span><span class="res-title">Apache Kafka Official Documentation</span><span class="res-source">Apache</span></a>
        <a class="res-link" href="https://www.youtube.com/watch?v=R873BlNVUB4" target="_blank" rel="noopener"><span class="res-icon">🎥</span><span class="res-title">Apache Kafka Crash Course (Hussein Nasser)</span><span class="res-source">Hussein Nasser</span></a>
        <a class="res-link" href="https://developer.confluent.io/" target="_blank" rel="noopener"><span class="res-icon">🎓</span><span class="res-title">Confluent Developer: Kafka Tutorials &amp; Patterns</span><span class="res-source">Confluent</span></a>
        <a class="res-link" href="https://www.confluent.io/resources/kafka-the-definitive-guide/" target="_blank" rel="noopener"><span class="res-icon">📖</span><span class="res-title">Kafka: The Definitive Guide (O&#x27;Reilly / Confluent)</span><span class="res-source">O&#x27;Reilly</span></a>
        <a class="res-link" href="https://debezium.io/documentation/reference/stable/architecture.html" target="_blank" rel="noopener"><span class="res-icon">🔄</span><span class="res-title">Debezium Change Data Capture Architecture</span><span class="res-source">Debezium</span></a>
        <a class="res-link" href="https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html" target="_blank" rel="noopener"><span class="res-icon">📐</span><span class="res-title">Schema Evolution &amp; Compatibility Reference</span><span class="res-source">Confluent</span></a>
      </div>
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


def update_section_10(sec10_text):
    sec10_new = re.sub(
        r'<span class="focus-bar-stats">[^<]+</span>',
        '<span class="focus-bar-stats">24 concepts &bull; 6 subsections</span>',
        sec10_text
    )
    sec10_new = re.sub(
        r'<div class="meta">[^<]+</div>',
        '<div class="meta">6 subsections · 24 concepts</div>',
        sec10_new
    )
    sec10_new = re.sub(
        r'<div class="pct-text" data-pp-text="10">[^<]+</div>',
        '<div class="pct-text" data-pp-text="10">0 / 24</div>',
        sec10_new
    )
    sec10_new = re.sub(
        r'<div class="section-desc">[\s\S]*?</div>\s*(?=<div class="resources-section">)',
        '''<div class="section-desc">
    <div class="tagline">High-throughput partitioned commit log architecture, KRaft Raft consensus, ISR durability, idempotent EOS, Connect/CDC, Streams &amp; Tiered Storage.</div>
    <div class="row"><b>Core Focus:</b> Zero-copy sendfile() &amp; page cache, KRaft quorum, High Watermark &amp; log compaction, CooperativeSticky rebalancing, Schema Registry, Debezium CDC &amp; MirrorMaker 2.</div>
    <div class="row"><b>Production Trade-offs:</b> At-least-once idempotency vs transactional EOS latency overhead, partition parallelism vs rebalance duration &amp; file handles, local NVMe vs KIP-405 Tiered Storage.</div>
  </div>
''',
        sec10_new,
        count=1
    )
    sec10_new = re.sub(
        r'<div class="resources-section">[\s\S]*?</div>\s*</div>\s*</div>\s*(?=<div class="subsection">)',
        KAFKA_RESOURCES_HTML + '\n',
        sec10_new,
        count=1
    )
    subs_html = render_subsections_html(KAFKA_SUBSECTIONS)
    sub_start = sec10_new.find('<div class="subsection">')
    sub_end = sec10_new.rfind('</section>')
    if sub_start == -1 or sub_end == -1:
        raise ValueError("Could not locate subsection boundaries in section-10")
    return sec10_new[:sub_start] + subs_html + '\n' + sec10_new[sub_end:]


def expand_tech_kafka():
    p = os.path.join(ROOT, 'tech_kafka.html')
    with open(p, 'r', encoding='utf-8') as f:
        html = f.read()

    html = re.sub(
        r'<div class="edition">[^<]+</div>',
        '<div class="edition">Distributed Streaming &middot; Masterclass 07 &middot; 6 Subsections &middot; 24 Concepts</div>',
        html
    )
    html = re.sub(
        r'<p class="subtitle">[^<]+</p>',
        '<p class="subtitle">High-throughput distributed event streaming: commit log &amp; KRaft internals, ISR &amp; compaction, idempotent EOS producers, CooperativeSticky rebalancing, Schema Registry, Debezium CDC, Streams, Tiered Storage &amp; MirrorMaker 2.</p>',
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

    sec10_match = re.search(r'(<section class="section domain-section"[^>]*id="section-10"[\s\S]*?</section>)', html)
    if not sec10_match:
        raise ValueError("Could not find section-10 in tech_kafka.html")

    sec10_text = sec10_match.group(1)
    sec10_new = update_section_10(sec10_text)
    html = html.replace(sec10_text, sec10_new, 1)

    atomic_write(p, html)
    print("Saved tech_kafka.html successfully!")


def expand_all_tech():
    p = os.path.join(ROOT, 'all_tech.html')
    with open(p, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update card-kafka in domain deck
    card_match = re.search(r'(<div class="domain-card[^"]*"[^>]*id="card-kafka"[\s\S]*?</div>\s*</div>\s*</div>)', html)
    if not card_match:
        raise ValueError("Could not find card-kafka in all_tech.html")
    old_card = card_match.group(1)
    new_card = re.sub(
        r'<p class="domain-card-desc">[\s\S]*?</p>',
        '<p class="domain-card-desc">Distributed commit log, KRaft quorum, ISR &amp; compaction, idempotent EOS producers, CooperativeSticky rebalancing, Schema Registry, Connect/Debezium CDC, Streams, Tiered Storage &amp; MirrorMaker 2.</p>',
        old_card,
        count=1
    )
    new_card = re.sub(
        r'<div class="domain-card-chips">[\s\S]*?</div>',
        '''<div class="domain-card-chips">
<span class="domain-card-chip">6 Subsections</span>
<span class="domain-card-chip">24 Concepts</span>
<span class="domain-card-chip highlight">KRaft, EOS, Connect/CDC, Streams &amp; KIP-405</span>
</div>''',
        new_card,
        count=1
    )
    html = html.replace(old_card, new_card, 1)
    print("Updated card-kafka in all_tech.html")

    # 2. Update Section 10 (Kafka) inside all_tech.html
    sec10_match = re.search(r'(<section class="section domain-section"[^>]*id="section-10"[\s\S]*?</section>)', html)
    if not sec10_match:
        raise ValueError("Could not find section-10 in all_tech.html")
    sec10_text = sec10_match.group(1)
    sec10_new = update_section_10(sec10_text)
    html = html.replace(sec10_text, sec10_new, 1)
    print("Updated section-10 in all_tech.html")

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
    expand_tech_kafka()
    expand_all_tech()
    print("Finished expanding Apache Kafka Masterclass!")
