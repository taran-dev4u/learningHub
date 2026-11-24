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


SPARK_SUBSECTIONS = [
    {
        "num": "11.1",
        "title": "Spark Architecture, Cluster Topologies & DAG Execution Engine",
        "desc": "Distributed runtime internals: Driver/Executor coordination, Cluster Managers (Kubernetes, YARN, Standalone), DAG stage boundaries, and decoupled Spark Connect gRPC execution.",
        "concepts": [
            ("11.1.1", "Spark Cluster Architecture: Driver Program, Cluster Managers (K8s, YARN) & Executors",
             "How the Driver JVM runs SparkSession, DAGScheduler, and TaskScheduler while Cluster Managers (Kubernetes native scheduler, YARN ResourceManager, Standalone) provision isolated Executor JVMs with dynamic allocation and shuffle tracking.",
             "https://www.youtube.com/watch?v=c3RfF-Q2o0I", "00:00", "DataCeps", "https://spark.apache.org/docs/latest/cluster-overview.html"),
            ("11.1.2", "Execution Hierarchy: Applications, Jobs, Stages, Tasks & Data Locality",
             "Mapping eager Actions to Jobs, splitting Jobs at wide shuffle dependencies into ShuffleMapStages and ResultStages, and scheduling parallel Tasks (one per partition) using PROCESS_LOCAL, NODE_LOCAL, and RACK_LOCAL locality preferences.",
             "https://www.youtube.com/watch?v=PZGUFnd0So4", "00:00", "Under the Hood Data", "https://spark.apache.org/docs/latest/job-scheduling.html"),
            ("11.1.3", "Narrow vs Wide Dependencies & Shuffle Mechanics (Sort Shuffle & BypassMergeSort)",
             "Why Narrow transformations (map, filter, union) pipeline in-memory within a single stage, whereas Wide dependencies (groupByKey, join, repartition) materialize map-side sorted .data and .index files across disk and network.",
             "https://www.youtube.com/watch?v=JkirctZv6Nw", "00:00", "Arun Yadav", "https://spark.apache.org/docs/latest/rdd-programming-guide.html"),
            ("11.1.4", "Spark Connect (Client-Server gRPC) & Decoupled Spark 4.0 Architecture",
             "Thin client-server gRPC architecture separating IDEs, notebooks, and microservices from the Spark Driver JVM using unresolved Catalyst logical plans, eliminating driver OOM coupling and enabling multi-language clients.",
             "https://www.youtube.com/watch?v=QoKWzrHVbgo", "00:00", "Apache Spark", "https://spark.apache.org/docs/latest/spark-connect-overview.html"),
        ],
    },
    {
        "num": "11.2",
        "title": "Resilient Distributed Datasets (RDDs), Lineage & Shared Variables",
        "desc": "Core immutable distributed collection primitives, lazy DAG pipelining, fault recovery via lineage or checkpointing, and cluster-wide Broadcast and Accumulator mechanics.",
        "concepts": [
            ("11.2.1", "RDD Internals: Immutability, Partitioning, Compute() & Deterministic Lineage Graphs",
             "Understanding the five core properties of an RDD (partitions, compute function, dependencies, optional Hash/RangePartitioner, and preferred locations) and how deterministic lineage guarantees lock-free parallel recovery.",
             "https://www.youtube.com/watch?v=zGS6LFg4RLo", "00:00", "The Learning Pipeline", "https://spark.apache.org/docs/latest/rdd-programming-guide.html"),
            ("11.2.2", "Lazy Transformations vs Eager Actions: Pipelining, reduceByKey vs groupByKey & collect() Traps",
             "How lazy evaluation fuses chained maps/filters before execution, why map-side combining in reduceByKey/aggregateByKey avoids catastrophic shuffle bloat vs groupByKey, and why collect()/toPandas() crash the Driver.",
             "https://www.youtube.com/watch?v=rKkqSeU_idY", "00:00", "DE_With_Karim", "https://spark.apache.org/docs/latest/rdd-programming-guide.html"),
            ("11.2.3", "Fault Tolerance: Lineage Graph Recomputation vs Reliable Checkpointing (HDFS/S3)",
             "Recovering lost partitions by replaying narrow ancestor tasks vs truncating unbounded iterative or streaming lineage graphs onto durable storage via sparkContext.checkpoint() and localCheckpoint().",
             "https://www.youtube.com/watch?v=iNv90A44fpA", "00:00", "DataOrbitAI", "https://spark.apache.org/docs/latest/rdd-programming-guide.html"),
            ("11.2.4", "Shared Variables: Broadcast Variables (TorrentBroadcast) & Distributed Accumulators",
             "Distributing read-only lookup tables once per executor via BitTorrent-style peer-to-peer chunking instead of per-task closure serialization, and safely using write-only Accumulators despite speculative execution retries.",
             "https://www.youtube.com/watch?v=JB98Loobc7k", "00:00", "Ease With Data", "https://spark.apache.org/docs/latest/rdd-programming-guide.html"),
        ],
    },
    {
        "num": "11.3",
        "title": "DataFrames, Spark SQL, Catalyst Optimizer & Tungsten Engine",
        "desc": "Structured schema-aware processing, four-phase Catalyst query planning, Tungsten off-heap binary memory with Whole-Stage Codegen, and Spark 3.x+ Adaptive Query Execution.",
        "concepts": [
            ("11.3.1", "Structured APIs: DataFrames, Typed Datasets, Encoders & Unified Spark SQL Engine",
             "Why untyped Row-based DataFrames and type-safe JVM Datasets compile into the identical Catalyst physical plan, leveraging compact binary Encoders to outperform raw Java/Python RDD serialization.",
             "https://www.youtube.com/watch?v=nTYcvfmDLDE", "00:00", "Azurelib Academy", "https://spark.apache.org/docs/latest/sql-programming-guide.html"),
            ("11.3.2", "Catalyst Optimizer: Analysis, Logical Optimization, Physical Planning & Cost-Based Optimization",
             "Four-stage tree transformation pipeline: Catalog schema resolution, rule-based logical optimizations (Predicate Pushdown, Column Pruning, Constant Folding), and Cost-Based Optimizer (CBO) physical plan selection.",
             "https://www.youtube.com/watch?v=1to11_o63F8", "00:00", "SMAC Academy", "https://spark.apache.org/docs/latest/sql-programming-guide.html"),
            ("11.3.3", "Tungsten Execution Engine: Off-Heap Binary Memory, Cache-Aware Layout & Whole-Stage Codegen",
             "Eliminating JVM object overhead and GC pauses via sun.misc.Unsafe byte-packed InternalRow storage, L1/L2/L3 cache-friendly pointer sorting, and Janino runtime Java bytecode generation fusing operators into tight loops.",
             "https://www.youtube.com/watch?v=XourMIutDPc", "00:00", "OneStop Insightful Tech Log", "https://spark.apache.org/docs/latest/sql-performance-tuning.html"),
            ("11.3.4", "Adaptive Query Execution (AQE): Dynamic Partition Coalescing, Join Switching & Skew Mitigation",
             "Runtime plan re-optimization between shuffle stages using actual map output statistics: coalescing tiny post-shuffle partitions, converting Sort-Merge Joins into Broadcast Hash Joins, and splitting skewed partitions dynamically.",
             "https://www.youtube.com/watch?v=164OKvwW8T8", "00:00", "Ease With Data", "https://spark.apache.org/docs/latest/sql-performance-tuning.html"),
        ],
    },
    {
        "num": "11.4",
        "title": "Joins, Shuffle Tuning, Memory Management & Skew Elimination",
        "desc": "Physical distributed join algorithms, unified Execution/Storage memory pools and disk spilling, partition sizing, and diagnosing straggler data skew.",
        "concepts": [
            ("11.4.1", "Distributed Join Strategies: Broadcast Hash Join (BHJ), Shuffle Hash (SHJ) & Sort-Merge Join (SMJ)",
             "Physical join execution mechanics: autoBroadcastJoinThreshold (10 MB default), why Sort-Merge Join scales to multi-terabyte tables via external merge sort, Shuffle Hash memory trade-offs, and Broadcast Nested Loop pitfalls.",
             "https://www.youtube.com/watch?v=lkTvchqa_Ck", "00:00", "Sumit Mittal", "https://spark.apache.org/docs/latest/sql-ref-syntax-qry-select-hints.html"),
            ("11.4.2", "Unified Memory Management: Execution vs Storage Pools, Off-Heap & Disk Spilling",
             "How Spark partitions JVM heap (spark.memory.fraction=0.6, storageFraction=0.5) with dynamic borrowing and eviction, MEMORY_AND_DISK vs MEMORY_ONLY_SER caching, and UnsafeExternalSorter disk spilling under pressure.",
             "https://www.youtube.com/watch?v=McMQ7yMaL9Q", "00:00", "Ease With Data", "https://spark.apache.org/docs/latest/tuning.html"),
            ("11.4.3", "Partition Sizing & Shuffle Tuning: coalesce() vs repartition(), Small Files & Push-Based Shuffle",
             "Eliminating the Small Files Problem with maxRecordsPerFile, metadata-only coalesce() vs full-shuffle repartition(), sizing shuffle partitions to 128 MB-200 MB targets, and Push-Based Shuffle (Magnet).",
             "https://www.youtube.com/watch?v=PklT4Hm6u1w", "00:00", "Mastering Big Data Engineering", "https://spark.apache.org/docs/latest/configuration.html"),
            ("11.4.4", "Diagnosing & Fixing Data Skew: Key Salting, Null Isolation & AQE Skew Join Optimization",
             "Spotting 99%-stuck straggler tasks via p50 vs max task metrics in the Spark UI, applying deterministic N-way key salting with broadcast replication, isolating skewed NULL/sentinel keys, and tuning AQE skew thresholds.",
             "https://www.youtube.com/watch?v=rZGsc5y8AQk", "00:00", "Afaque Ahmad", "https://spark.apache.org/docs/latest/sql-performance-tuning.html"),
        ],
    },
    {
        "num": "11.5",
        "title": "PySpark Optimization, Columnar Storage & Open Lakehouse Formats",
        "desc": "Zero-copy Apache Arrow PySpark UDFs, Parquet/ORC columnar internals, ACID lakehouse table formats (Iceberg, Delta Lake, Hudi), and partition/bucket pruning.",
        "concepts": [
            ("11.5.1", "PySpark Execution Internals: Py4J Bridge, Arrow Vectorized UDFs & Pandas API on Spark",
             "Understanding the JVM-to-Python socket serialization tax of standard Python UDFs, accelerating vectorized batch transfers 10x-100x with Apache Arrow (@pandas_udf), and scaling Pandas workloads via pyspark.pandas.",
             "https://www.youtube.com/watch?v=N_e9S8wbX28", "00:00", "Databricks Events", "https://spark.apache.org/docs/latest/sql-pyspark-pandas-with-arrow.html"),
            ("11.5.2", "Columnar Storage Formats: Apache Parquet, ORC, Row Groups, Compression & Predicate Pushdown",
             "Parquet physical hierarchy (Row Groups, Column Chunks, Pages), Dictionary/RLE/Bit-packing encodings, min/max Footer statistics for page skipping, and Zstandard vs Snappy compression trade-offs.",
             "https://www.youtube.com/watch?v=BjssGRlSnfA", "00:00", "Learn Data with Mark", "https://spark.apache.org/docs/latest/sql-data-sources-parquet.html"),
            ("11.5.3", "Open Lakehouse Table Formats: Apache Iceberg, Delta Lake & Apache Hudi with Spark",
             "Bringing ACID transactions, Optimistic Concurrency Control (OCC), snapshot time travel, safe schema evolution, hidden partitioning, and Z-Ordering/Liquid Clustering directly onto S3/ADLS/GCS object stores.",
             "https://www.youtube.com/watch?v=8B7Ol16SnOg", "00:00", "SalesOptecs Academy", "https://iceberg.apache.org/docs/latest/spark-getting-started/"),
            ("11.5.4", "Catalogs, Dynamic Partition Pruning (DPP) & Pre-Shuffled Bucketing",
             "How Dynamic Partition Pruning (DPP) pushes dimension-table broadcast filters down into fact-table partition scans, avoiding high-cardinality directory over-partitioning, and eliminating shuffles with bucketBy() joins.",
             "https://www.youtube.com/watch?v=s8Z8Gex7VFw", "00:00", "Afaque Ahmad", "https://spark.apache.org/docs/latest/sql-data-sources-hive-tables.html"),
        ],
    },
    {
        "num": "11.6",
        "title": "Structured Streaming, State Stores, Reliability & Spark UI Diagnostics",
        "desc": "Incremental unbounded tables, event-time watermarks and RocksDB state stores, end-to-end exactly-once checkpoints, and production Spark UI / JVM GC troubleshooting.",
        "concepts": [
            ("11.6.1", "Spark Structured Streaming: Unbounded Tables, Micro-Batching & Continuous Processing",
             "Modeling streams as append-only unbounded DataFrames, trigger modes (processingTime, availableNow backfill, Continuous sub-millisecond mode), and output modes (Append, Update, Complete).",
             "https://www.youtube.com/watch?v=qxKCqcxRawc", "00:00", "Ease With Data", "https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html"),
            ("11.6.2", "Event-Time Processing, Watermarking, Windowing & RocksDB Stateful Streaming",
             "Bound state memory on late-arriving out-of-order events with event-time watermarks (withWatermark), tumbling/sliding/session windows, stream-stream joins, and RocksDB StateStoreProvider for million-key state.",
             "https://www.youtube.com/watch?v=8DaIDXvBtKA", "00:00", "Quantum Root", "https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html"),
            ("11.6.3", "Exactly-Once End-to-End Streaming: Checkpointing, Write-Ahead Logs & Idempotent Sinks",
             "Achieving end-to-end exactly-once semantics by pairing replayable sources (Kafka offsets), durable HDFS/S3 offset WAL + state snapshots in checkpointLocation, and idempotent/transactional sinks (Delta/Iceberg).",
             "https://www.youtube.com/watch?v=ec70A9MXCao", "00:00", "VerifyFix", "https://spark.apache.org/docs/latest/structured-streaming-kafka-integration.html"),
            ("11.6.4", "Spark UI Diagnostics, History Server & JVM/GC Production Troubleshooting",
             "Reading Spark UI DAG visualizations, SQL physical plan metrics (scan rows, shuffle read/write, memory/disk spill), tuning G1GC executor pauses, and diagnosing OOMKilled containers vs FetchFailedException.",
             "https://www.youtube.com/watch?v=iOUi_KF-sQ0", "00:00", "Data Architect Studio", "https://spark.apache.org/docs/latest/monitoring.html"),
        ],
    },
]

SPARK_RESOURCES_HTML = '''  <div class="resources-section">
    <div class="head" onclick="this.parentElement.classList.toggle('open')">
      <h4>📚 Learn this domain</h4>
      <div><span class="count">6 curated resources</span><span class="chevron">▶</span></div>
    </div>
    <div class="resources-body">
      <div class="res-grid">
        <a class="res-link" href="https://spark.apache.org/docs/latest/" target="_blank" rel="noopener"><span class="res-icon">📖</span><span class="res-title">Apache Spark Official Documentation</span><span class="res-source">Apache</span></a>
        <a class="res-link" href="https://spark.apache.org/docs/latest/sql-performance-tuning.html" target="_blank" rel="noopener"><span class="res-icon">⚡</span><span class="res-title">Spark SQL Performance Tuning &amp; AQE Guide</span><span class="res-source">Apache</span></a>
        <a class="res-link" href="https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html" target="_blank" rel="noopener"><span class="res-icon">🌊</span><span class="res-title">Structured Streaming Programming Guide</span><span class="res-source">Apache</span></a>
        <a class="res-link" href="https://iceberg.apache.org/docs/latest/spark-getting-started/" target="_blank" rel="noopener"><span class="res-icon">🧊</span><span class="res-title">Apache Iceberg + Spark Lakehouse Guide</span><span class="res-source">Iceberg</span></a>
        <a class="res-link" href="https://docs.delta.io/latest/delta-intro.html" target="_blank" rel="noopener"><span class="res-icon">🔺</span><span class="res-title">Delta Lake Architecture &amp; ACID Guide</span><span class="res-source">Delta Lake</span></a>
        <a class="res-link" href="https://www.youtube.com/watch?v=_C8kWso4ne4" target="_blank" rel="noopener"><span class="res-icon">🎥</span><span class="res-title">Apache Spark &amp; PySpark Full Course</span><span class="res-source">freeCodeCamp</span></a>
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


def update_section_11(sec11_text):
    sec11_new = re.sub(
        r'<span class="focus-bar-stats">[^<]+</span>',
        '<span class="focus-bar-stats">24 concepts &bull; 6 subsections</span>',
        sec11_text
    )
    sec11_new = re.sub(
        r'<div class="meta">[^<]+</div>',
        '<div class="meta">6 subsections · 24 concepts</div>',
        sec11_new
    )
    sec11_new = re.sub(
        r'<div class="pct-text" data-pp-text="11">[^<]+</div>',
        '<div class="pct-text" data-pp-text="11">0 / 24</div>',
        sec11_new
    )
    sec11_new = re.sub(
        r'<div class="section-desc">[\s\S]*?</div>\s*(?=<div class="resources-section">)',
        '''<div class="section-desc">
    <div class="tagline">In-memory distributed cluster computing: Driver/Executor DAGs &amp; Spark Connect, RDD lineage, Catalyst &amp; Tungsten AQE, Join/Shuffle/Skew tuning, PySpark Arrow, Lakehouses &amp; Structured Streaming.</div>
    <div class="row"><b>Core Focus:</b> Catalyst 4-phase optimization, Tungsten off-heap &amp; Whole-Stage Codegen, Adaptive Query Execution (AQE), Sort-Merge vs Broadcast Joins, Unified Memory spilling, Parquet/Iceberg/Delta &amp; RocksDB state stores.</div>
    <div class="row"><b>Production Trade-offs:</b> Shuffle network I/O vs broadcast memory, Python UDF serialization tax vs Arrow @pandas_udf, small-file explosion vs coalesce/repartition cost, and streaming micro-batch latency vs RocksDB state overhead.</div>
  </div>
''',
        sec11_new,
        count=1
    )
    sec11_new = re.sub(
        r'<div class="resources-section">[\s\S]*?</div>\s*</div>\s*</div>\s*(?=<div class="subsection">)',
        SPARK_RESOURCES_HTML + '\n',
        sec11_new,
        count=1
    )
    subs_html = render_subsections_html(SPARK_SUBSECTIONS)
    sub_start = sec11_new.find('<div class="subsection">')
    sub_end = sec11_new.rfind('</section>')
    if sub_start == -1 or sub_end == -1:
        raise ValueError("Could not locate subsection boundaries in section-11")
    return sec11_new[:sub_start] + subs_html + '\n' + sec11_new[sub_end:]


def expand_tech_spark():
    p = os.path.join(ROOT, 'tech_spark.html')
    with open(p, 'r', encoding='utf-8') as f:
        html = f.read()

    html = re.sub(
        r'<div class="edition">[^<]+</div>',
        '<div class="edition">Distributed In-Memory Cluster Computing &middot; Masterclass 08 &middot; 6 Subsections &middot; 24 Concepts</div>',
        html
    )
    html = re.sub(
        r'<p class="subtitle">[^<]+</p>',
        '<p class="subtitle">High-performance distributed cluster computing: Driver/Executor DAGs &amp; Spark Connect, RDD lineage &amp; shared variables, Catalyst &amp; Tungsten AQE, Join &amp; Shuffle tuning, PySpark Arrow, Parquet/Iceberg/Delta Lakehouses, Structured Streaming &amp; Spark UI diagnostics.</p>',
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

    # Clean up stray broken focus-bar-right / unmatched closing div in standalone tech_spark.html
    html = re.sub(
        r'<div id="spark"></div>\s*<div class="focus-bar-right">[\s\S]*?</div>\s*</div>\s*(?=<div class="section-banner")',
        '<div id="spark"></div>\n',
        html,
        count=1
    )

    # Wire #theme-toggle in inline script if not already wired
    if 'getElementById(\'theme-toggle\')' not in html:
        html = html.replace(
            '  updateProgress();',
            '''  const themeBtn = document.getElementById('theme-toggle');
  if (themeBtn) {
    themeBtn.addEventListener('click', () => {
      const navBtn = document.querySelector('[data-hub-theme]');
      if (navBtn) { navBtn.click(); return; }
      const themes = ['light', 'dark', 'black'];
      const cur = document.documentElement.getAttribute('data-theme') || 'light';
      const next = themes[(themes.indexOf(cur) + 1) % themes.length];
      document.documentElement.classList.toggle('dark', next !== 'light');
      document.documentElement.classList.toggle('light', next === 'light');
      document.documentElement.classList.toggle('black', next === 'black');
      document.documentElement.setAttribute('data-theme', next);
      try { localStorage.setItem('learning_hub_theme', next); } catch (e) {}
    });
  }

  updateProgress();''',
            1
        )

    sec11_match = re.search(r'(<section class="section domain-section"[^>]*id="section-11"[\s\S]*?</section>)', html)
    if not sec11_match:
        raise ValueError("Could not find section-11 in tech_spark.html")

    sec11_text = sec11_match.group(1)
    sec11_new = update_section_11(sec11_text)
    html = html.replace(sec11_text, sec11_new, 1)

    atomic_write(p, html)
    print("Saved tech_spark.html successfully!")


def expand_all_tech():
    p = os.path.join(ROOT, 'all_tech.html')
    with open(p, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update card-spark in domain deck
    card_match = re.search(r'(<div class="domain-card[^"]*"[^>]*id="card-spark"[\s\S]*?</div>\s*</div>\s*</div>)', html)
    if not card_match:
        raise ValueError("Could not find card-spark in all_tech.html")
    old_card = card_match.group(1)
    new_card = re.sub(
        r'<p class="domain-card-desc">[\s\S]*?</p>',
        '<p class="domain-card-desc">Driver/Executor DAGs &amp; Spark Connect, RDD lineage, Catalyst &amp; Tungsten AQE, Join/Shuffle/Skew tuning, PySpark Arrow, Parquet/Iceberg/Delta Lakehouses &amp; Structured Streaming.</p>',
        old_card,
        count=1
    )
    new_card = re.sub(
        r'<div class="domain-card-chips">[\s\S]*?</div>',
        '''<div class="domain-card-chips">
<span class="domain-card-chip">6 Subsections</span>
<span class="domain-card-chip">24 Concepts</span>
<span class="domain-card-chip highlight">Catalyst, Tungsten, AQE, Arrow &amp; Streaming</span>
</div>''',
        new_card,
        count=1
    )
    html = html.replace(old_card, new_card, 1)
    print("Updated card-spark in all_tech.html")

    # 2. Update Section 11 (Spark) inside all_tech.html
    sec11_match = re.search(r'(<section class="section domain-section"[^>]*id="section-11"[\s\S]*?</section>)', html)
    if not sec11_match:
        raise ValueError("Could not find section-11 in all_tech.html")
    sec11_text = sec11_match.group(1)
    sec11_new = update_section_11(sec11_text)
    html = html.replace(sec11_text, sec11_new, 1)
    print("Updated section-11 in all_tech.html")

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
    expand_tech_spark()
    expand_all_tech()
    print("Finished expanding Apache Spark Masterclass!")
