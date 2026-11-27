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


POSTGRES_SUBSECTIONS = [
    {
        "num": "12.1",
        "title": "Relational Theory, Schema Design, Partitioning & Hybrid Modeling",
        "desc": "Foundational relational integrity, normalization vs materialized denormalization, declarative table partitioning with pruning, and modern JSONB/UUIDv7/pgvector hybrid modeling.",
        "concepts": [
            ("12.1.1", "Relational Theory & Integrity: Candidate/Surrogate Keys, Foreign Keys, CHECK, Exclusion Constraints & Domains",
             "Enforcing domain invariants directly in the storage engine with NOT NULL, UNIQUE, cascading Foreign Keys, CHECK constraints, custom DOMAINs, and GiST EXCLUDE USING constraints for non-overlapping intervals.",
             "https://www.youtube.com/watch?v=qw--VYLpxG4&t=317s", "05:17", "freeCodeCamp.org", "https://www.postgresql.org/docs/current/ddl-constraints.html"),
            ("12.1.2", "Functional Dependencies & Normalization (1NF-BCNF) vs Strategic Denormalization & Materialized Views",
             "Eliminating insertion, update, and deletion anomalies across 1NF, 2NF, 3NF, and BCNF versus controlled read-path denormalization, GENERATED ALWAYS AS STORED columns, and REFRESH MATERIALIZED VIEW CONCURRENTLY.",
             "https://www.youtube.com/watch?v=va-QO-dhilI", "00:00", "Anindita Das Bhattacharjee", "https://www.postgresql.org/docs/current/rules-materializedviews.html"),
            ("12.1.3", "Declarative Table Partitioning (Range, List, Hash), Partition Pruning & Time-Series Patterns",
             "Scaling multi-billion-row tables via native RANGE, LIST, and HASH partitioning, static and runtime partition pruning, instant DROP/DETACH PARTITION retention, and default partition pitfalls.",
             "https://www.youtube.com/watch?v=dKJyMj_P-XA", "00:00", "Microsoft Developer", "https://www.postgresql.org/docs/current/ddl-partitioning.html"),
            ("12.1.4", "Semi-Structured & Hybrid Data: JSONB Binary Storage, TOAST Compression, Arrays, UUIDv7 & pgvector",
             "Why JSONB pre-parses binary key-value structures for GIN indexing unlike raw JSON text, avoiding random UUIDv4 B-Tree page splits with time-ordered UUIDv7, and HNSW/IVFFlat vector similarity with pgvector.",
             "https://www.youtube.com/watch?v=wsBGpWBo0Ks", "00:00", "InterviewBuddies", "https://www.postgresql.org/docs/current/datatype-json.html"),
        ],
    },
    {
        "num": "12.2",
        "title": "Storage Engine Internals: Slotted Pages, MVCC, WAL & Vacuuming",
        "desc": "On-disk 8KB heap slotted pages, Shared Buffers clock-sweep eviction, tuple xmin/xmax visibility and HOT updates, Write-Ahead Logging recovery, and Autovacuum freeze mechanics.",
        "concepts": [
            ("12.2.1", "Physical Storage Internals: Heap Slotted Pages (8KB), CTID, FSM/VM Maps, TOAST & Shared Buffers Clock-Sweep",
             "Anatomy of an 8KB PostgreSQL page (PageHeaderData, line pointer array, tuple heap), (block, offset) ctid addressing, TOAST out-of-line >2KB storage, Free Space Map, and Shared Buffers clock-sweep eviction.",
             "https://www.youtube.com/watch?v=8-2yv4z0VZc", "00:00", "CMU Database Group", "https://www.postgresql.org/docs/current/storage-page-layout.html"),
            ("12.2.2", "Multi-Version Concurrency Control (MVCC): xmin/xmax Tuple Headers, Snapshots, HOT Updates & Visibility",
             "Non-blocking readers and writers via copy-on-write tuple versions stamped with xmin/xmax transaction IDs, Heap-Only Tuple (HOT) same-page updates avoiding index bloat, and Snapshot isolation visibility checks.",
             "https://www.youtube.com/watch?v=Q56kljmIN14", "00:00", "Hussein Nasser", "https://www.postgresql.org/docs/current/mvcc.html"),
            ("12.2.3", "Write-Ahead Logging (WAL): ARIES Steal/No-Force, Checkpoints, Full-Page Writes, LSNs & Crash Recovery",
             "Sequential WAL persistence before dirty data pages flush, 64-bit Log Sequence Numbers (LSN), torn-page protection via full_page_writes, checkpoint spreading, and automatic crash REDO replay.",
             "https://www.youtube.com/watch?v=XiH2LzjgWV4", "00:00", "New Horizons Bulgaria", "https://www.postgresql.org/docs/current/wal-intro.html"),
            ("12.2.4", "VACUUM & Autovacuum Internals: Dead Tuple Bloat, Visibility Map & XID Anti-Wraparound Freeze",
             "Reclaiming dead tuple space without table locks, setting Visibility Map all-visible bits for Index-Only Scans, tuning autovacuum_vacuum_scale_factor per hot table, and preventing 32-bit XID wraparound shutdown.",
             "https://www.youtube.com/watch?v=GsXIIMttPmI", "00:00", "AWS Events", "https://www.postgresql.org/docs/current/routine-vacuuming.html"),
        ],
    },
    {
        "num": "12.3",
        "title": "Concurrency Control, Locking, Transactions & Zero-Downtime Migrations",
        "desc": "ACID isolation anomalies and SSI, PostgreSQL's 8-mode table/row lock conflict matrix, LWLocks and deadlock resolution, and lock-safe zero-downtime DDL migrations.",
        "concepts": [
            ("12.3.1", "ACID Isolation Levels: Read Committed, Repeatable Read (SI) & Serializable (SSI / RW-Antidependencies)",
             "Why PostgreSQL Read Uncommitted maps to Read Committed, snapshot acquisition per-statement vs per-transaction, phantom & write-skew anomalies, and Serializable Snapshot Isolation (SSI) SIREAD predicate tracking.",
             "https://www.youtube.com/watch?v=Mkz6mmt0sWc", "00:00", "Sri Tech Labs", "https://www.postgresql.org/docs/current/transaction-iso.html"),
            ("12.3.2", "PostgreSQL Lock Hierarchy: Table Locks (ACCESS SHARE to ACCESS EXCLUSIVE), Row Locks & Deadlocks",
             "The 8-level table lock compatibility matrix, row-level FOR UPDATE / FOR NO KEY UPDATE / SKIP LOCKED job-queue patterns, MultiXact IDs, and automatic cycle-detection deadlock victim rollback.",
             "https://www.youtube.com/watch?v=URwmzTeuHdk", "00:00", "Hussein Nasser", "https://www.postgresql.org/docs/current/explicit-locking.html"),
            ("12.3.3", "Lightweight Locks (LWLocks), Spinlocks, Buffer Pinning, Lock Queues & Advisory Locks",
             "Internal shared-memory latch coordination (ProcArrayLock, WALInsertLock), how a queued ACCESS EXCLUSIVE DDL request starves concurrent readers behind it, and application-level pg_advisory_lock coordination.",
             "https://www.youtube.com/watch?v=UZUF76-w32U", "00:00", "JaneExplainsIT", "https://www.postgresql.org/docs/current/explicit-locking.html"),
            ("12.3.4", "Lock-Free Zero-Downtime Schema Migrations: Expand-Contract, CONCURRENTLY & lock_timeout Guardrails",
             "Avoiding production outages using SET lock_timeout, CREATE INDEX CONCURRENTLY two-phase scans, NOT VALID constraints with VALIDATE CONSTRAINT, and dual-write Expand-Contract schema evolution.",
             "https://www.youtube.com/watch?v=-1aO6UznfI0", "00:00", "Xata", "https://www.postgresql.org/docs/current/sql-createindex.html"),
        ],
    },
    {
        "num": "12.4",
        "title": "Indexing Internals & Cost-Based Query Optimization",
        "desc": "Lehman-Yao B-Tree mechanics and covering indexes, specialized GIN/GiST/BRIN structures, Cost-Based Optimizer statistics and cardinality math, and EXPLAIN (ANALYZE, BUFFERS) diagnostics.",
        "concepts": [
            ("12.4.1", "B-Tree Index Internals: Lehman-Yao Concurrent B-Trees, Composite Ordering, INCLUDE & Index-Only Scans",
             "Balanced high-fanout page splitting with sibling pointers, leftmost prefix column selectivity, deduplication, INCLUDE non-key covering payloads, and Visibility Map-enabled Index-Only Scans.",
             "https://www.youtube.com/watch?v=a1Z40OC553Y", "00:00", "Hussein Nasser", "https://www.postgresql.org/docs/current/indexes-types.html"),
            ("12.4.2", "Specialized Index Engines: GIN (JSONB/Full-Text), GiST (R-Tree/PostGIS), BRIN (Block Range) & Hash",
             "Matching workload to index engine: GIN inverted posting lists with fastupdate pending lists, GiST lossy bounding boxes for PostGIS & ranges, 100x-smaller BRIN min/max summaries for append-only tables, and Hash equality.",
             "https://www.youtube.com/watch?v=8s35iHLGHww", "00:00", "JaneExplainsIT", "https://www.postgresql.org/docs/current/indexes-types.html"),
            ("12.4.3", "Query Lifecycle & Cost-Based Optimizer (CBO): Parser, Rewriter, pg_statistic Histograms, MCVs & GEQO",
             "SQL parse trees, view/rule rewriting, ANALYZE sampling into pg_statistic (Most Common Values, equi-depth histograms, CREATE STATISTICS multi-column correlations), and dynamic programming join ordering.",
             "https://www.youtube.com/watch?v=wLpcVM9qxV0", "00:00", "Microsoft Developer", "https://www.postgresql.org/docs/current/planner-optimizer.html"),
            ("12.4.4", "Mastering EXPLAIN (ANALYZE, BUFFERS): Scan Types, Nested Loop/Hash/Merge Joins & CTE Materialization",
             "Reading actual vs estimated rows, shared hit/read/dirtied buffers, Seq Scan vs Bitmap Heap Scan, Nested Loop vs Hash Join vs Merge Join memory trade-offs, and PostgreSQL 12+ CTE inlining.",
             "https://www.youtube.com/watch?v=GmX8tjT7UcQ", "00:00", "InterviewBuddies", "https://www.postgresql.org/docs/current/using-explain.html"),
        ],
    },
    {
        "num": "12.5",
        "title": "Replication, High Availability, Connection Pooling & Horizontal Scaling",
        "desc": "Physical WAL streaming and replication slots, logical pgoutput CDC and zero-downtime upgrades, PgBouncer transaction pooling, and Patroni + etcd failover with Citus sharding.",
        "concepts": [
            ("12.5.1", "Physical Streaming Replication: WAL Sender/Receiver, Replication Slots, Sync vs Async & Cascading",
             "Byte-for-byte WAL streaming via walsender/walreceiver, preventing WAL premature deletion (and disk exhaustion traps) with physical replication slots, and synchronous_commit levels (off, local, remote_write, on, remote_apply).",
             "https://www.youtube.com/watch?v=9aFu7APZQmY", "00:00", "Hussein Nasser", "https://www.postgresql.org/docs/current/warm-standby.html"),
            ("12.5.2", "Logical Replication Internals: pgoutput Decoding, Publications/Subscriptions, Major Upgrades & CDC",
             "Decoding WAL records with wal_level=logical into row-level tuple changes via pgoutput, selective table Publications/Subscriptions, zero-downtime PostgreSQL major version upgrades, and Debezium CDC integration.",
             "https://www.youtube.com/watch?v=OvSzLjkMmQo", "00:00", "Code with Lucian", "https://www.postgresql.org/docs/current/logical-replication.html"),
            ("12.5.3", "Connection Pooling & Process-Per-Connection Limits: PgBouncer (Session, Transaction, Statement) & Prepared Statements",
             "Why PostgreSQL's fork-based process model degrades past hundreds of active connections (context switches, ProcArray snapshot contention), sizing pools with PgBouncer transaction mode, and protocol-level prepared statement handling.",
             "https://www.youtube.com/watch?v=nzX7yZRhRcU", "00:00", "Chirag Mahto", "https://www.pgbouncer.org/features.html"),
            ("12.5.4", "High Availability & Horizontal Scaling: Patroni + etcd Consensus Failover, Split-Brain Fencing & Citus Sharding",
             "Leader lease elections in Patroni backed by etcd/Consul Raft consensus, watchdog/STONITH split-brain prevention, HAProxy read/write routing, and horizontal distributed sharding with Citus & postgres_fdw.",
             "https://www.youtube.com/watch?v=RHwglGf_z40", "00:00", "Techno Tim", "https://patroni.readthedocs.io/en/latest/"),
        ],
    },
    {
        "num": "12.6",
        "title": "Backup/PITR, Security, Observability & Production Kernel Tuning",
        "desc": "Continuous WAL archiving and Point-in-Time Recovery (pgBackRest), SCRAM-SHA-256 and Row-Level Security, pg_stat_statements & wait-event diagnostics, and Linux/memory parameter tuning.",
        "concepts": [
            ("12.6.1", "Physical & Logical Backups: pg_basebackup, pgBackRest, Continuous WAL Archiving & Point-in-Time Recovery (PITR)",
             "Why pg_dump logical snapshots do not scale to multi-TB recovery, streaming physical base backups plus archive_command WAL segments to S3, incremental/delta restores with pgBackRest, and recovery_target_time PITR.",
             "https://www.youtube.com/watch?v=RkESdFnXo8I", "00:00", "mynoteoracledba", "https://www.postgresql.org/docs/current/continuous-archiving.html"),
            ("12.6.2", "PostgreSQL Security & Multi-Tenancy: pg_hba.conf, SCRAM-SHA-256, TLS/mTLS, RBAC & Row-Level Security (RLS)",
             "Host-based authentication rules, migrating from MD5 to SCRAM-SHA-256 salted challenge-response, enforcing TLS 1.3 client certificates, least-privilege schema roles, and tenant-isolating RLS USING / WITH CHECK policies.",
             "https://www.youtube.com/watch?v=vZT1Qx2xUCo", "00:00", "Microsoft Developer", "https://www.postgresql.org/docs/current/ddl-rowsecurity.html"),
            ("12.6.3", "Observability & Bottleneck Diagnostics: pg_stat_statements, pg_stat_activity, Wait Events & Bloat Metrics",
             "Identifying top CPU/I/O queries by total_exec_time and shared_blks_read in pg_stat_statements, diagnosing IO/LWLock/Lock wait_event stalls in pg_stat_activity, and tracking dead tuple bloat and cache hit ratios.",
             "https://www.youtube.com/watch?v=U8UGTyJp-K4", "00:00", "pganalyze", "https://www.postgresql.org/docs/current/pgstatstatements.html"),
            ("12.6.4", "Production Kernel & Memory Tuning: shared_buffers, work_mem, effective_cache_size, HugePages & Linux Dirty I/O",
             "Sizing shared_buffers (25% RAM) alongside OS page cache, avoiding OOM multipliers with per-sort/hash node work_mem, tuning random_page_cost=1.1 for NVMe SSDs, enabling Linux HugePages, and vm.dirty_background_bytes.",
             "https://www.youtube.com/watch?v=UMGaj8KJVmk", "00:00", "Postgres Conference", "https://www.postgresql.org/docs/current/runtime-config-resource.html"),
        ],
    },
]

POSTGRES_RESOURCES_HTML = '''  <div class="resources-section">
    <div class="head" onclick="this.parentElement.classList.toggle('open')">
      <h4>📚 Learn this domain</h4>
      <div><span class="count">6 curated resources</span><span class="chevron">▶</span></div>
    </div>
    <div class="resources-body">
      <div class="res-grid">
        <a class="res-link" href="https://www.postgresql.org/docs/current/" target="_blank" rel="noopener"><span class="res-icon">📖</span><span class="res-title">PostgreSQL Official Documentation</span><span class="res-source">PostgreSQL</span></a>
        <a class="res-link" href="https://www.interdb.jp/pg/" target="_blank" rel="noopener"><span class="res-icon">🔬</span><span class="res-title">The Internals of PostgreSQL (Hironobu Suzuki)</span><span class="res-source">InterDB</span></a>
        <a class="res-link" href="https://use-the-index-luke.com/" target="_blank" rel="noopener"><span class="res-icon">⚡</span><span class="res-title">Use The Index, Luke (SQL Indexing Guide)</span><span class="res-source">Markus Winand</span></a>
        <a class="res-link" href="https://15445.courses.cs.cmu.edu/" target="_blank" rel="noopener"><span class="res-icon">🎓</span><span class="res-title">CMU 15-445: Database Systems Internals</span><span class="res-source">Andy Pavlo / CMU</span></a>
        <a class="res-link" href="https://www.pgbouncer.org/features.html" target="_blank" rel="noopener"><span class="res-icon">🔌</span><span class="res-title">PgBouncer Connection Pooling Reference</span><span class="res-source">PgBouncer</span></a>
        <a class="res-link" href="https://pgbackrest.org/user-guide.html" target="_blank" rel="noopener"><span class="res-icon">💾</span><span class="res-title">pgBackRest Enterprise Backup &amp; PITR Guide</span><span class="res-source">pgBackRest</span></a>
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


def update_section_12(sec12_text, standalone=False):
    sec12_new = re.sub(
        r'<span class="focus-bar-stats">[^<]+</span>',
        '<span class="focus-bar-stats">24 concepts &bull; 6 subsections</span>',
        sec12_text
    )
    if standalone:
        sec12_new = re.sub(
            r'\s*<div class="focus-bar-right">[\s\S]*?</div>\s*(?=</div>\s*<div class="section-banner")',
            '\n  ',
            sec12_new,
            count=1
        )
    sec12_new = re.sub(
        r'<div class="meta">[^<]+</div>',
        '<div class="meta">6 subsections · 24 concepts</div>',
        sec12_new
    )
    sec12_new = re.sub(
        r'<div class="pct-text" data-pp-text="12">[^<]+</div>',
        '<div class="pct-text" data-pp-text="12">0 / 24</div>',
        sec12_new
    )
    sec12_new = re.sub(
        r'<div class="section-desc">[\s\S]*?</div>\s*(?=<div class="resources-section">)',
        '''<div class="section-desc">
    <div class="tagline">Relational persistence &amp; database engine internals: slotted 8KB pages, MVCC snapshots &amp; HOT updates, Write-Ahead Logging (WAL), Autovacuum, locking/SSI, B-Tree/GIN/GiST/BRIN indexes, EXPLAIN CBO tuning, PgBouncer, Patroni HA &amp; PITR.</div>
    <div class="row"><b>Core Focus:</b> Tuple xmin/xmax visibility, ARIES WAL crash recovery, lock-free CONCURRENTLY migrations, Lehman-Yao B-Trees &amp; Index-Only Scans, physical/logical replication, Patroni + etcd consensus &amp; Linux kernel memory tuning.</div>
    <div class="row"><b>Production Trade-offs:</b> Index write amplification vs read latency, synchronous_commit durability vs tail latency, transaction pooling vs prepared statements, and Autovacuum I/O budget vs dead tuple bloat.</div>
  </div>
''',
        sec12_new,
        count=1
    )
    sec12_new = re.sub(
        r'<div class="resources-section">[\s\S]*?</div>\s*</div>\s*</div>\s*(?=<div class="subsection">)',
        POSTGRES_RESOURCES_HTML + '\n',
        sec12_new,
        count=1
    )
    subs_html = render_subsections_html(POSTGRES_SUBSECTIONS)
    sub_start = sec12_new.find('<div class="subsection">')
    sub_end = sec12_new.rfind('</section>')
    if sub_start == -1 or sub_end == -1:
        raise ValueError("Could not locate subsection boundaries in section-12")
    return sec12_new[:sub_start] + subs_html + '\n' + sec12_new[sub_end:]


def expand_tech_postgres():
    p = os.path.join(ROOT, 'tech_postgres.html')
    with open(p, 'r', encoding='utf-8') as f:
        html = f.read()

    html = html.replace('<body>', '<body data-site="cloud">', 1)
    html = re.sub(
        r'<div class="edition">[^<]+</div>',
        '<div class="edition">Database Engineering &amp; Internals &middot; Masterclass 09 &middot; 6 Subsections &middot; 24 Concepts</div>',
        html
    )
    html = re.sub(
        r'<p class="subtitle">[^<]+</p>',
        '<p class="subtitle">Deep relational database engineering: schema &amp; partitioning, 8KB heap slotted pages, MVCC &amp; HOT updates, WAL crash recovery, Autovacuum, ACID isolation &amp; locks, zero-downtime DDL, B-Tree/GIN/GiST/BRIN indexes, CBO &amp; EXPLAIN, PgBouncer, Patroni HA, PITR, RLS &amp; Linux tuning.</p>',
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

    # Update theme-toggle handler to delegate to shared navbar toggle when available
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

    sec12_match = re.search(r'(<section class="section domain-section"[^>]*id="section-12"[\s\S]*?</section>)', html)
    if not sec12_match:
        raise ValueError("Could not find section-12 in tech_postgres.html")

    sec12_text = sec12_match.group(1)
    sec12_new = update_section_12(sec12_text, standalone=True)
    html = html.replace(sec12_text, sec12_new, 1)

    # Update sister-guides-card to include all 15 masterclasses + both hubs
    html = re.sub(
        r'<div class="sister-guides-card">[\s\S]*?</div>\s*</div>\s*(?=</div>\s*<script>)',
        SISTER_GUIDES_HTML + '\n',
        html,
        count=1
    )

    atomic_write(p, html)
    print("Saved tech_postgres.html successfully!")


def expand_all_tech():
    p = os.path.join(ROOT, 'all_tech.html')
    with open(p, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update card-postgres in domain deck
    card_match = re.search(r'(<div class="domain-card[^"]*"[^>]*id="card-postgres"[\s\S]*?</div>\s*</div>\s*</div>)', html)
    if not card_match:
        raise ValueError("Could not find card-postgres in all_tech.html")
    old_card = card_match.group(1)
    new_card = re.sub(
        r'<p class="domain-card-desc">[\s\S]*?</p>',
        '<p class="domain-card-desc">Slotted 8KB pages, MVCC &amp; HOT updates, WAL crash recovery, Autovacuum, Locking &amp; SSI, Zero-Downtime DDL, B-Tree/GIN/GiST/BRIN, EXPLAIN CBO, PgBouncer, Patroni HA &amp; PITR.</p>',
        old_card,
        count=1
    )
    new_card = re.sub(
        r'<div class="domain-card-chips">[\s\S]*?</div>',
        '''<div class="domain-card-chips">
<span class="domain-card-chip">6 Subsections</span>
<span class="domain-card-chip">24 Concepts</span>
<span class="domain-card-chip highlight">MVCC, WAL, Locking, Indexes, Patroni &amp; Tuning</span>
</div>''',
        new_card,
        count=1
    )
    html = html.replace(old_card, new_card, 1)
    print("Updated card-postgres in all_tech.html")

    # 2. Update Section 12 (PostgreSQL) inside all_tech.html
    sec12_match = re.search(r'(<section class="section domain-section"[^>]*id="section-12"[\s\S]*?</section>)', html)
    if not sec12_match:
        raise ValueError("Could not find section-12 in all_tech.html")
    sec12_text = sec12_match.group(1)
    sec12_new = update_section_12(sec12_text, standalone=False)
    html = html.replace(sec12_text, sec12_new, 1)
    print("Updated section-12 in all_tech.html")

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
    expand_tech_postgres()
    expand_all_tech()
    print("Finished expanding PostgreSQL & Database Engineering Masterclass!")
