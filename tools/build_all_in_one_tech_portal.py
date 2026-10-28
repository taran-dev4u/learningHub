"""
tools/build_all_in_one_tech_portal.py

Generates:
1. Updated cloud_aws_azure.html (All-in-One Tech & Engineering Portal with interactive Domain Deck,
   sticky pill bar, focused domain view, and 3-theme styling).
2. 5 Standalone Masterclass Pages:
   - tech_aws.html
   - tech_linux.html
   - tech_git.html
   - tech_docker_k8s.html
   - tech_cicd.html
"""
import os
import re
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_PATH = os.path.join(ROOT, 'cloud_aws_azure.html')

def atomic_write(filepath, content):
    tmp = filepath + '.atomic.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        f.write(content)
    for attempt in range(5):
        try:
            if os.path.exists(filepath):
                os.replace(tmp, filepath)
            else:
                os.rename(tmp, filepath)
            break
        except Exception:
            if attempt == 4:
                raise
            time.sleep(0.2)

# Load existing cloud_aws_azure.html
with open(SRC_PATH, 'r', encoding='utf-8') as f:
    orig_html = f.read()

# Metadata for all 16 domains
DOMAINS = [
    {
        "id": "section-1",
        "slug": "aws",
        "title": "AWS Cloud Architecture",
        "icon": "☁️",
        "desc": "Global infra, IAM least privilege, VPC network topology, EC2, Auto Scaling, S3, EBS, RDS, Aurora, DynamoDB, ECS, EKS, Lambda & CloudWatch.",
        "badge": "Compute, Storage, Networking, Serverless & Security",
        "page": "tech_aws.html",
        "page_title": "AWS Cloud Architecture Masterclass",
        "page_subtitle": "Production cloud infrastructure: IAM least privilege, VPC network isolation, multi-tier EC2/ELB compute, managed RDS/DynamoDB databases, and event-driven serverless architectures."
    },
    {
        "id": "section-2",
        "slug": "azure",
        "title": "Microsoft Azure Cloud",
        "icon": "🔷",
        "desc": "Entra ID, Virtual Machines, App Services, Blob Storage, Cosmos DB, Azure SQL, VNet, AKS container orchestration & Event Grid.",
        "badge": "Enterprise Identity, Microservices & Managed Data",
        "page": None,
        "page_title": "Microsoft Azure Masterclass",
        "page_subtitle": "Enterprise Azure architecture: Entra ID governance, VNet topology, AKS microservices, Cosmos DB global distribution, and hybrid cloud integration."
    },
    {
        "id": "section-3",
        "slug": "gcp",
        "title": "Google Cloud Platform (GCP)",
        "icon": "🌐",
        "desc": "Compute Engine, GKE, Cloud Run, Cloud Functions, Cloud Storage, BigQuery data analytics, Cloud Spanner & VPC networking.",
        "badge": "Containers, Serverless, Big Data & Analytics",
        "page": None,
        "page_title": "Google Cloud Platform (GCP) Masterclass",
        "page_subtitle": "Google Cloud architecture: GKE enterprise clusters, Cloud Run serverless scale-to-zero, BigQuery petabyte analytics, and global VPC routing."
    },
    {
        "id": "section-4",
        "slug": "linux",
        "title": "Linux & Terminal Power Engineering",
        "icon": "🐧",
        "desc": "Filesystem hierarchy (FHS), permissions, signals, systemd, process lifecycle, memory/IO diagnostics, pipes & production Bash automation.",
        "badge": "Kernel Primitives, Processes, Bash & Systems Troubleshooting",
        "page": "tech_linux.html",
        "page_title": "Linux & Terminal Power Engineering Masterclass",
        "page_subtitle": "Master the Linux kernel, process lifecycle, signals, systemd, memory/IO diagnostics, permissions, pipelines, and production Bash automation."
    },
    {
        "id": "section-5",
        "slug": "git",
        "title": "Git & GitHub Architecture",
        "icon": "🌿",
        "desc": "Git DAG object model (blobs, trees, commits), 3 trees, staging, branching models, interactive rebase, cherry-pick, merge conflicts & reflog.",
        "badge": "Object DB, Branching, Rebasing & Advanced Workflows",
        "page": "tech_git.html",
        "page_title": "Git & GitHub Architecture Masterclass",
        "page_subtitle": "Deep-dive into the Git DAG object model, index mechanics, interactive rebasing, cherry-picking, reflog disaster recovery, and enterprise GitHub workflows."
    },
    {
        "id": "section-6",
        "slug": "docker",
        "title": "Docker & Containerization Deep-Dive",
        "icon": "🐳",
        "desc": "Linux namespaces, cgroups, UnionFS Overlay2, multi-stage Dockerfile optimization, container networking & Compose orchestration.",
        "badge": "Cgroups, Multi-Stage Builds & Container Security",
        "page": "tech_docker_k8s.html",
        "page_title": "Docker & Kubernetes Container Orchestration Masterclass",
        "page_subtitle": "Complete container engineering: Linux cgroups & namespaces, multi-stage Docker builds, Kubernetes control plane, Pod lifecycle, Services, Ingress, StatefulSets, and Helm."
    },
    {
        "id": "section-7",
        "slug": "k8s",
        "title": "Kubernetes (K8s) Container Orchestration",
        "icon": "☸️",
        "desc": "Control plane, etcd quorum, Pod lifecycle, Deployments, Services, Ingress controllers, DaemonSets, StatefulSets & Helm packaging.",
        "badge": "Cluster Control Plane, Services, Ingress & Helm",
        "page": "tech_docker_k8s.html",
        "page_title": "Docker & Kubernetes Container Orchestration Masterclass",
        "page_subtitle": "Complete container engineering: Linux cgroups & namespaces, multi-stage Docker builds, Kubernetes control plane, Pod lifecycle, Services, Ingress, StatefulSets, and Helm."
    },
    {
        "id": "section-8",
        "slug": "terraform",
        "title": "Infrastructure as Code (IaC) with Terraform",
        "icon": "🏗️",
        "desc": "HCL syntax, providers, resources, remote state backend, DynamoDB state locking, reusable modules & state drift reconciliation.",
        "badge": "Declarative Cloud Provisioning & State Locking",
        "page": None,
        "page_title": "Terraform & Infrastructure as Code Masterclass",
        "page_subtitle": "Enterprise IaC: declarative HCL syntax, provider patterns, remote S3/GCS state backends, DynamoDB locking, modular architectures, and drift management."
    },
    {
        "id": "section-9",
        "slug": "cicd",
        "title": "CI/CD Pipelines & DevOps Automation",
        "icon": "🚀",
        "desc": "Continuous integration, automated test suites, delivery vs deployment, GitHub Actions workflows, Jenkins pipelines, Blue/Green & Canary rollouts.",
        "badge": "GitHub Actions, Blue-Green, Canary & Rollbacks",
        "page": "tech_cicd.html",
        "page_title": "CI/CD Pipelines & DevOps Automation Masterclass",
        "page_subtitle": "Modern continuous integration & deployment: automated test pipelines, GitHub Actions workflows, Jenkins architectures, Blue/Green deployments, Canary rollouts, and GitOps."
    },
    {
        "id": "section-10",
        "slug": "kafka",
        "title": "Apache Kafka Distributed Streaming",
        "icon": "⚡",
        "desc": "Distributed commit log, broker cluster architecture, partition rebalancing, consumer group protocols & exactly-once semantics (EOS).",
        "badge": "High-Throughput Distributed Event Streaming",
        "page": None,
        "page_title": "Apache Kafka Distributed Streaming Masterclass",
        "page_subtitle": "High-throughput event streaming: partition design, consumer rebalance protocols, idempotent producers, transaction coordinators, and Kafka Connect/Streams."
    },
    {
        "id": "section-11",
        "slug": "spark",
        "title": "Apache Spark Big Data Engine",
        "icon": "📊",
        "desc": "RDDs, DataFrames, Spark SQL, Catalyst optimizer, wide vs narrow transformations, cluster memory management & distributed shuffling.",
        "badge": "Distributed In-Memory Cluster Computing",
        "page": None,
        "page_title": "Apache Spark Big Data Masterclass",
        "page_subtitle": "Distributed big data compute: RDD/DataFrame DAG execution, Catalyst physical optimization, shuffle bottlenecks, memory tuning, and Structured Streaming."
    },
    {
        "id": "section-12",
        "slug": "postgres",
        "title": "Database Engineering & PostgreSQL Internals",
        "icon": "🐘",
        "desc": "ACID guarantees, MVCC transaction isolation, WAL logging, B-tree, Hash, GIN, GiST indexes, EXPLAIN ANALYZE query planning & connection pooling.",
        "badge": "MVCC, Indexing Internals, Sharding & Query Optimization",
        "page": None,
        "page_title": "Database Engineering & PostgreSQL Masterclass",
        "page_subtitle": "Relational database internals: ACID transaction isolation, MVCC vacuuming, WAL replication, index selector algorithms, query execution plans, and PgBouncer."
    },
    {
        "id": "section-13",
        "slug": "redis",
        "title": "In-Memory Caching with Redis",
        "icon": "🔴",
        "desc": "Single-threaded event loop, String, Hash, List, Set, Sorted Set, cache-aside, write-through, TTL eviction & Redis Sentinel / Cluster HA.",
        "badge": "Sub-Millisecond Cache Strategies & Distributed Locks",
        "page": None,
        "page_title": "In-Memory Caching with Redis Masterclass",
        "page_subtitle": "Ultra-low-latency in-memory data structures: non-blocking IO multiplexing, Redis Cluster sharding, Sentinel failover, cache stampede prevention, and Redlock."
    },
    {
        "id": "section-14",
        "slug": "java",
        "title": "Java & Spring Boot Microservices",
        "icon": "☕",
        "desc": "JVM memory model, G1/ZGC collectors, Spring IoC, Spring Boot auto-configuration, Spring Data JPA, Hibernate L1/L2 cache & Resilience4j.",
        "badge": "Enterprise Microservices & Cloud-Native Backends",
        "page": None,
        "page_title": "Java & Spring Boot Microservices Masterclass",
        "page_subtitle": "Enterprise backend engineering: JVM heap tuning, garbage collection algorithms, Spring dependency injection, Hibernate N+1 resolution, and resilient microservices."
    },
    {
        "id": "section-15",
        "slug": "python",
        "title": "Python Backend Engineering with FastAPI",
        "icon": "🐍",
        "desc": "Async/await event loop, ASGI vs WSGI, Pydantic data validation, dependency injection, SQLAlchemy 2.0 async ORM & high-concurrency APIs.",
        "badge": "Asynchronous High-Performance API Engineering",
        "page": None,
        "page_title": "Python & FastAPI Backend Masterclass",
        "page_subtitle": "Asynchronous Python backend engineering: uvloop event loop internals, ASGI concurrency, Pydantic type serialization, async SQLAlchemy, and Dockerized production APIs."
    },
    {
        "id": "section-16",
        "slug": "apis",
        "title": "Production API Design & Architecture",
        "icon": "🔌",
        "desc": "REST vs GraphQL vs gRPC, idempotent HTTP methods, API versioning strategies, token bucket rate limiting, OAuth2, JWT & OpenAPI governance.",
        "badge": "REST, gRPC, OAuth2, Rate Limiting & Contract Design",
        "page": None,
        "page_title": "Production API Design & Architecture Masterclass",
        "page_subtitle": "Enterprise API contracts: idempotent endpoint design, gRPC protobuf serialization, GraphQL schema federation, token bucket throttling, and OAuth2/OIDC security."
    }
]

# Extract sections
sec_starts = list(re.finditer(r'<section class="section[^"]*"\s+id="([^"]+)"[^>]*>', orig_html))
sections_data = {}
for i, m in enumerate(sec_starts):
    sid = m.group(1)
    start_pos = m.start()
    end_pos = sec_starts[i+1].start() if i+1 < len(sec_starts) else len(orig_html)
    gap_m = re.search(r'<!--gen-gap-start-->|<script>window\.SITE_SLUG', orig_html[start_pos:end_pos])
    if gap_m:
        end_pos = start_pos + gap_m.start()
    sec_content = orig_html[start_pos:end_pos].strip()
    sections_data[sid] = sec_content

# Calculate counts
for d in DOMAINS:
    sid = d["id"]
    content = sections_data.get(sid, "")
    subs = re.findall(r'<div class="subsection">[\s\S]*?<h3>(.*?)</h3>', content)
    concepts = re.findall(r'<li\b[^>]*data-cid="([^"]+)"[^>]*>', content)
    d["sub_count"] = len(subs)
    d["concept_count"] = len(concepts)

# CSS injection
CSS_INJECTION = '''
/* All-in-One Tech Portal Design System */
:root {
  --bg: #f7f8fb;
  --surface: #ffffff;
  --surface-2: #eef2f7;
  --surface-3: #e4eaf2;
  --text: #172033;
  --muted: #5b6578;
  --faint: #7a8599;
  --border: #dbe2ec;
  --navy: #172554;
  --navy-2: #1e3a8a;
  --blue: #2563eb;
  --amber: #f59e0b;
  --green: #0f9f6e;
  --red: #dc4c64;
  --violet: #7c3aed;
  --shadow: 0 4px 16px rgba(23, 32, 51, 0.06);
  --shadow-lift: 0 12px 32px rgba(23, 32, 51, 0.12);
  --bg-elev: var(--surface-2);
  --bg-card: var(--surface);
  --bg-row-alt: var(--surface-2);
  --text-dim: var(--muted);
  --text-faint: var(--faint);
  --border-strong: var(--border);
  --accent: var(--blue);
  --accent-dim: rgba(37, 99, 235, 0.1);
  --link: var(--blue);
  --quote-bg: rgba(37, 99, 235, 0.05);
  --done: var(--green);
  --done-bg: rgba(15, 159, 110, 0.12);
  --shadow-card: var(--shadow);
  --shadow-banner: 0 4px 14px rgba(0,0,0,0.08);
}
html.dark, html[data-theme="dark"] {
  --bg: #0b1120;
  --surface: #151f32;
  --surface-2: #1e293b;
  --surface-3: #27354a;
  --text: #f1f5f9;
  --muted: #94a3b8;
  --faint: #64748b;
  --border: #1e293b;
  --navy: #1e293b;
  --navy-2: #243552;
  --shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
  --shadow-lift: 0 12px 32px rgba(0, 0, 0, 0.5);
  --bg-elev: #151f32;
  --bg-card: #151f32;
  --bg-row-alt: #1a263d;
  --text-dim: #94a3b8;
  --text-faint: #64748b;
  --border-strong: #334155;
  --accent: #38bdf8;
  --accent-dim: rgba(56, 189, 248, 0.15);
  --link: #38bdf8;
  --quote-bg: rgba(56, 189, 248, 0.08);
  --done: #10b981;
  --done-bg: rgba(16, 185, 129, 0.15);
}
html.black, html[data-theme="black"] {
  --bg: #000000;
  --surface: #0a0a0a;
  --surface-2: #141414;
  --surface-3: #1f1f1f;
  --text: #ffffff;
  --muted: #888888;
  --faint: #555555;
  --border: #222222;
  --navy: #0e0e0e;
  --navy-2: #181818;
  --shadow: 0 4px 20px rgba(0, 0, 0, 0.7);
  --shadow-lift: 0 12px 32px rgba(0, 0, 0, 0.9);
  --bg-elev: #0e0e0e;
  --bg-card: #0a0a0a;
  --bg-row-alt: #121212;
  --text-dim: #888888;
  --text-faint: #555555;
  --border-strong: #2c2c2c;
  --accent: #60a5fa;
  --accent-dim: rgba(96, 165, 250, 0.18);
  --link: #60a5fa;
  --quote-bg: rgba(96, 165, 250, 0.08);
  --done: #22c55e;
  --done-bg: rgba(34, 197, 94, 0.15);
}
.wrap { max-width: 1440px; margin: 0 auto; padding: 20px 20px 80px; }
.tech-breadcrumb {
  display: flex; align-items: center; gap: 8px;
  font-size: 13px; font-weight: 700;
  margin: 0 0 16px; padding: 6px 12px;
  background: var(--surface-2); border: 1px solid var(--border);
  border-radius: 8px; width: fit-content;
}
.tech-bc-home { color: var(--accent); text-decoration: none; }
.tech-bc-home:hover { text-decoration: underline; }
.tech-bc-sep { color: var(--faint); }
.tech-bc-curr { color: var(--text); }
.domain-deck-section { margin: 24px 0 28px; }
.domain-deck-head {
  display: flex; align-items: center; justify-content: space-between;
  flex-wrap: wrap; gap: 12px; margin-bottom: 14px;
}
.domain-deck-head h2 {
  font-size: 20px; margin: 0; font-weight: 800; letter-spacing: -0.01em; color: var(--text);
}
.domain-deck-subtitle {
  font-size: 13px; color: var(--muted); margin: 2px 0 0;
}
.domain-deck {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(310px, 1fr)); gap: 14px;
}
.domain-card {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 12px; padding: 16px; display: flex; flex-direction: column;
  box-shadow: var(--shadow); transition: transform 0.18s ease, border-color 0.18s ease, box-shadow 0.18s ease;
  position: relative; cursor: pointer;
}
.domain-card:hover {
  transform: translateY(-2px); border-color: var(--accent); box-shadow: var(--shadow-lift);
}
.domain-card.active-deck-card {
  border-color: var(--accent); box-shadow: 0 0 0 2px var(--accent), var(--shadow-lift);
}
.domain-card-head { display: flex; align-items: flex-start; gap: 12px; margin-bottom: 10px; }
.domain-card-icon {
  font-size: 24px; line-height: 1; flex-shrink: 0;
  background: var(--surface-2); padding: 8px; border-radius: 10px; border: 1px solid var(--border);
}
.domain-card-meta { flex: 1; min-width: 0; }
.domain-card-idx {
  font-size: 10.5px; font-weight: 800; color: var(--accent);
  text-transform: uppercase; letter-spacing: 0.08em;
}
.domain-card-title {
  font-size: 15.5px; font-weight: 800; margin: 2px 0 0; color: var(--text); line-height: 1.3;
}
.domain-card-desc {
  font-size: 12px; color: var(--muted); line-height: 1.5; margin: 0 0 12px; flex: 1;
}
.domain-card-chips { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 14px; }
.d-chip {
  font-size: 11px; font-weight: 700; padding: 2px 8px; border-radius: 999px;
  background: var(--surface-2); border: 1px solid var(--border); color: var(--text-dim);
}
.d-chip.masterclass-badge {
  background: rgba(37, 99, 235, 0.12); border-color: var(--accent); color: var(--accent);
}
.domain-card-actions { display: flex; gap: 8px; align-items: center; margin-top: auto; }
.d-act-btn {
  flex: 1; min-height: 32px; padding: 5px 10px; border-radius: 7px;
  border: 1px solid var(--border); background: var(--surface-2); color: var(--text);
  font-size: 12px; font-weight: 700; cursor: pointer; display: inline-flex;
  align-items: center; justify-content: center; gap: 4px; transition: all 0.15s ease;
}
.d-act-btn:hover { background: var(--accent); color: #ffffff; border-color: var(--accent); }
.d-act-link {
  min-height: 32px; padding: 5px 11px; border-radius: 7px; border: 1px solid var(--accent);
  background: var(--accent); color: #ffffff; font-size: 12px; font-weight: 800;
  text-decoration: none; display: inline-flex; align-items: center; justify-content: center;
  gap: 4px; transition: all 0.15s ease; white-space: nowrap;
}
.d-act-link:hover { opacity: 0.9; transform: translateY(-1px); }
.domain-nav-bar {
  position: sticky; top: 53px; z-index: 60; background: var(--surface);
  border-bottom: 1px solid var(--border); border-top: 1px solid var(--border);
  padding: 8px 12px; margin: 0 -20px 22px; backdrop-filter: blur(12px);
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.domain-nav-scroll {
  display: flex; gap: 6px; overflow-x: auto; scrollbar-width: none;
  -webkit-overflow-scrolling: touch; max-width: 1440px; margin: 0 auto; padding: 0 8px;
}
.domain-nav-scroll::-webkit-scrollbar { display: none; }
.d-nav-pill {
  display: inline-flex; align-items: center; gap: 5px; min-height: 32px;
  padding: 4px 12px; border-radius: 999px; border: 1px solid var(--border);
  background: var(--surface-2); color: var(--muted); font-size: 12px;
  font-weight: 700; cursor: pointer; white-space: nowrap; transition: all 0.15s ease;
}
.d-nav-pill:hover { border-color: var(--accent); color: var(--text); transform: translateY(-1px); }
.d-nav-pill.active {
  background: var(--accent); border-color: var(--accent); color: #ffffff;
  box-shadow: 0 2px 10px rgba(37, 99, 235, 0.35);
}
.domain-focus-bar {
  display: flex; align-items: center; justify-content: space-between;
  flex-wrap: wrap; gap: 12px; padding: 12px 18px; margin-bottom: 16px;
  background: var(--surface); border: 1px solid var(--accent);
  border-radius: 10px; box-shadow: var(--shadow);
}
.focus-bar-left { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
.focus-bar-pill {
  font-size: 10.5px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em;
  padding: 3px 8px; border-radius: 6px; background: var(--accent-dim);
  color: var(--accent); border: 1px solid var(--accent);
}
.focus-bar-title { font-size: 15px; font-weight: 800; color: var(--text); }
.focus-bar-stats { font-size: 12px; color: var(--muted); font-weight: 600; }
.focus-bar-right { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }
.focus-btn {
  min-height: 30px; padding: 4px 10px; border-radius: 6px; border: 1px solid var(--border);
  background: var(--surface-2); color: var(--text); font-size: 12px; font-weight: 700;
  cursor: pointer; transition: all 0.15s ease;
}
.focus-btn:hover { background: var(--border); color: var(--text); }
.focus-btn.view-all-btn {
  background: var(--accent-dim); border-color: var(--accent); color: var(--accent);
}
.focus-btn.view-all-btn:hover { background: var(--accent); color: #ffffff; }
.focus-btn.masterclass-btn {
  background: var(--accent); border-color: var(--accent); color: #ffffff;
  text-decoration: none; display: inline-flex; align-items: center; gap: 4px;
}
.section.hidden-domain { display: none !important; }
.sister-guides-card {
  margin: 40px 0 20px; padding: 20px 24px;
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 12px; box-shadow: var(--shadow);
}
.sister-title { font-size: 15px; font-weight: 800; color: var(--text); margin-bottom: 12px; }
.sister-grid { display: flex; flex-wrap: wrap; gap: 8px; }
.sister-link {
  display: inline-flex; align-items: center; gap: 6px; padding: 8px 14px;
  border-radius: 8px; background: var(--surface-2); border: 1px solid var(--border);
  color: var(--text); text-decoration: none; font-size: 12.5px; font-weight: 700;
  transition: all 0.15s ease;
}
.sister-link:hover { border-color: var(--accent); background: var(--accent-dim); transform: translateY(-1px); }
.sister-link.active-hub { background: var(--accent); border-color: var(--accent); color: #ffffff; }
@media (max-width: 768px) {
  .hero h1 { font-size: 26px; }
  .domain-nav-bar { margin: 0 -12px 18px; }
  .domain-focus-bar { flex-direction: column; align-items: flex-start; }
}
'''

STANDALONE_JS = '''
(function() {
  const SLUG = 'cloud';
  const KEY_DONE = 'hub_done_' + SLUG;
  const KEY_BM = 'hub_bm_' + SLUG;
  const KEY_THEME = 'learning_hub_theme';

  function applyTheme(t) {
    if (t === 'light') {
      document.documentElement.classList.add('light');
      document.documentElement.classList.remove('dark', 'black');
    } else if (t === 'black') {
      document.documentElement.classList.add('black');
      document.documentElement.classList.remove('light', 'dark');
    } else {
      document.documentElement.classList.add('dark');
      document.documentElement.classList.remove('light', 'black');
    }
  }
  applyTheme(localStorage.getItem(KEY_THEME) || localStorage.getItem('hub_theme') || (window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark'));

  const themeBtn = document.getElementById('theme-toggle');
  if (themeBtn) themeBtn.addEventListener('click', () => {
    let cur = localStorage.getItem(KEY_THEME) || 'dark';
    let next = cur === 'light' ? 'dark' : (cur === 'dark' ? 'black' : 'light');
    localStorage.setItem(KEY_THEME, next);
    localStorage.setItem('hub_theme', next);
    applyTheme(next);
  });

  let doneSet = new Set(JSON.parse(localStorage.getItem(KEY_DONE) || '[]'));
  let bmSet = new Set(JSON.parse(localStorage.getItem(KEY_BM) || '[]'));

  function saveState() {
    localStorage.setItem(KEY_DONE, JSON.stringify(Array.from(doneSet)));
    localStorage.setItem(KEY_BM, JSON.stringify(Array.from(bmSet)));
    updateProgress();
  }

  function updateProgress() {
    const all = document.querySelectorAll('.concepts li[data-cid]');
    let d = 0;
    all.forEach(li => {
      if (doneSet.has(li.dataset.cid)) d++;
    });
    const pct = all.length ? Math.round((d / all.length) * 100) : 0;
    const bar = document.getElementById('overall-bar');
    const txt = document.getElementById('overall-pct');
    if (bar) bar.style.width = pct + '%';
    if (txt) txt.textContent = d + ' / ' + all.length;
  }

  document.querySelectorAll('.concepts li[data-cid]').forEach(li => {
    const cid = li.dataset.cid;
    const check = li.querySelector('.done-check');
    const star = li.querySelector('.bookmark-star');

    if (doneSet.has(cid)) {
      li.classList.add('done');
      if (check) check.classList.add('checked');
    }
    if (bmSet.has(cid)) {
      if (star) star.classList.add('active');
    }

    if (check) check.addEventListener('click', (e) => {
      e.stopPropagation();
      if (doneSet.has(cid)) {
        doneSet.delete(cid);
        li.classList.remove('done');
        check.classList.remove('checked');
      } else {
        doneSet.add(cid);
        li.classList.add('done');
        check.classList.add('checked');
      }
      saveState();
      applyFilters();
    });

    if (star) star.addEventListener('click', (e) => {
      e.stopPropagation();
      if (bmSet.has(cid)) {
        bmSet.delete(cid);
        star.classList.remove('active');
      } else {
        bmSet.add(cid);
        star.classList.add('active');
      }
      saveState();
      applyFilters();
    });
  });

  const filters = { status: null, search: '' };
  function applyFilters() {
    const q = filters.search.toLowerCase();
    document.querySelectorAll('.concepts li[data-cid]').forEach(li => {
      const cid = li.dataset.cid;
      const isDone = doneSet.has(cid);
      const isBm = bmSet.has(cid);
      const text = li.textContent.toLowerCase();

      let show = true;
      if (filters.status === 'done' && !isDone) show = false;
      if (filters.status === 'undone' && isDone) show = false;
      if (filters.status === 'bookmarked' && !isBm) show = false;
      if (q && !text.includes(q)) show = false;

      li.classList.toggle('hidden', !show);
    });
  }

  document.querySelectorAll('.filter-btn[data-filter]').forEach(btn => {
    btn.addEventListener('click', () => {
      const val = btn.dataset.val;
      if (filters.status === val) {
        filters.status = null;
        btn.classList.remove('active');
      } else {
        document.querySelectorAll('.filter-btn[data-filter]').forEach(b => b.classList.remove('active'));
        filters.status = val;
        btn.classList.add('active');
      }
      applyFilters();
    });
  });

  const clearBtn = document.getElementById('clear-filters');
  if (clearBtn) clearBtn.addEventListener('click', () => {
    filters.status = null;
    filters.search = '';
    const sInput = document.getElementById('search-input');
    if (sInput) sInput.value = '';
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    applyFilters();
  });

  const sInput = document.getElementById('search-input');
  if (sInput) sInput.addEventListener('input', e => {
    filters.search = e.target.value;
    applyFilters();
  });

  const randBtn = document.getElementById('random-btn');
  if (randBtn) randBtn.addEventListener('click', () => {
    const visible = Array.from(document.querySelectorAll('.concepts li[data-cid]:not(.hidden)'));
    if (!visible.length) return;
    const chosen = visible[Math.floor(Math.random() * visible.length)];
    chosen.scrollIntoView({ behavior: 'smooth', block: 'center' });
    chosen.style.transition = 'box-shadow 0.4s';
    chosen.style.boxShadow = '0 0 0 3px var(--accent)';
    setTimeout(() => { chosen.style.boxShadow = ''; }, 2000);
  });

  updateProgress();
})();
'''

# Extract base style from source HTML and combine with CSS_INJECTION
base_style_match = re.search(r'<style\b[^>]*>([\s\S]*?)</style>', orig_html)
base_style = (base_style_match.group(1) if base_style_match else "") + "\n" + CSS_INJECTION

# 1. Build Standalone Pages
def build_standalone_page(page_name, page_title, page_subtitle, badge, domain_keys):
    content_blocks = []
    total_subs = 0
    total_concepts = 0
    for key in domain_keys:
        d = next(item for item in DOMAINS if item["slug"] == key)
        sid = d["id"]
        sec_body = sections_data[sid]
        if not sec_body.endswith('</section>'):
            sec_body += '\n</section>'
        content_blocks.append(sec_body)
        total_subs += d["sub_count"]
        total_concepts += d["concept_count"]
    
    sections_html = "\n\n".join(content_blocks)
    
    page_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{page_title} | Taran's Learning Hub</title>
<link rel="stylesheet" href="assets/learning-hub-shared.css">
<script src="assets/learning-hub-shared.js"></script>
<style>
{base_style}
</style>
</head>
<body>
<div class="wrap">
  <div class="tech-breadcrumb">
    <a href="cloud_aws_azure.html" class="tech-bc-home">← All-in-One Tech Portal</a>
    <span class="tech-bc-sep">/</span>
    <span class="tech-bc-curr">{page_title}</span>
  </div>

  <div class="hero">
    <div class="edition">{badge} · {total_subs} Subsections · {total_concepts} Concepts</div>
    <h1>{page_title}</h1>
    <p class="subtitle">{page_subtitle}</p>
  </div>

  <div class="stats">
    <div class="stat"><div class="n">{total_subs}</div><div class="l">Subsections</div></div>
    <div class="stat"><div class="n">{total_concepts}</div><div class="l">Concepts</div></div>
    <div class="stat"><div class="n">100%</div><div class="l">Curated</div></div>
    <div class="stat"><div class="n">15+</div><div class="l">Verified Docs &amp; Labs</div></div>
  </div>

  <div class="overall-progress">
    <span class="lbl">Masterclass Progress</span>
    <div class="bar-track"><div class="bar-fill" id="overall-bar"></div></div>
    <span class="pct" id="overall-pct">0 / {total_concepts}</span>
  </div>

  <div class="controls">
    <div class="controls-row">
      <span class="label">Filter:</span>
      <button class="filter-btn status-done" data-filter="status" data-val="done">Done</button>
      <button class="filter-btn" data-filter="status" data-val="undone">Not Done</button>
      <button class="filter-btn status-bookmarked" data-filter="status" data-val="bookmarked">★ Bookmarked</button>
      <span class="sep"></span>
      <div class="search"><input id="search-input" placeholder="Search {total_concepts} concepts…" type="search"/></div>
      <button class="icon-btn" id="random-btn" title="Random concept">🎲</button>
      <button class="icon-btn" id="theme-toggle" title="Toggle theme">🌓</button>
      <button class="icon-btn" onclick="window.print()" title="Print">🖨️</button>
      <button class="filter-btn" id="clear-filters">Clear</button>
    </div>
  </div>

  {sections_html}

  <div class="sister-guides-card">
    <div class="sister-title">🚀 Companion Engineering Masterclasses</div>
    <div class="sister-grid">
      <a href="tech_aws.html" class="sister-link">☁️ AWS Cloud Masterclass</a>
      <a href="tech_linux.html" class="sister-link">🐧 Linux &amp; Terminal Masterclass</a>
      <a href="tech_git.html" class="sister-link">🌿 Git &amp; GitHub Masterclass</a>
      <a href="tech_docker_k8s.html" class="sister-link">🐳 Docker &amp; Kubernetes Masterclass</a>
      <a href="tech_cicd.html" class="sister-link">🚀 CI/CD Pipelines Masterclass</a>
      <a href="cloud_aws_azure.html" class="sister-link active-hub">🌐 All-in-One Tech Portal (16 Domains) &rarr;</a>
    </div>
  </div>
</div>

<script>
window.SITE_SLUG = "cloud";
</script>
<script>
{STANDALONE_JS}
</script>
</body>
</html>
'''
    atomic_write(os.path.join(ROOT, page_name), page_html)
    print(f"Generated {page_name} ({total_subs} subs, {total_concepts} concepts).")

# Build the 5 dedicated pages
build_standalone_page("tech_aws.html", "AWS Cloud Architecture Masterclass",
    "Production cloud infrastructure: IAM least privilege, VPC network isolation, multi-tier EC2/ELB compute, managed RDS/DynamoDB databases, and event-driven serverless architectures.",
    "Cloud Architecture · Masterclass 01", ["aws"])

build_standalone_page("tech_linux.html", "Linux & Terminal Power Engineering Masterclass",
    "Master the Linux kernel, process lifecycle, signals, systemd, memory/IO diagnostics, permissions, pipelines, and production Bash automation.",
    "Systems Engineering · Masterclass 02", ["linux"])

build_standalone_page("tech_git.html", "Git & GitHub Architecture Masterclass",
    "Deep-dive into the Git DAG object model, index mechanics, interactive rebasing, cherry-picking, reflog disaster recovery, and enterprise GitHub workflows.",
    "DevOps Architecture · Masterclass 03", ["git"])

build_standalone_page("tech_docker_k8s.html", "Docker & Kubernetes Container Orchestration Masterclass",
    "Complete container engineering: Linux cgroups & namespaces, multi-stage Docker builds, Kubernetes control plane, Pod lifecycle, Services, Ingress, StatefulSets, and Helm.",
    "Container Orchestration · Masterclass 04", ["docker", "k8s"])

build_standalone_page("tech_cicd.html", "CI/CD Pipelines & DevOps Automation Masterclass",
    "Modern continuous integration & deployment: automated test pipelines, GitHub Actions workflows, Jenkins architectures, Blue/Green deployments, Canary rollouts, and GitOps.",
    "DevOps Automation · Masterclass 05", ["cicd"])

# 2. Transform cloud_aws_azure.html
deck_cards = []
for i, d in enumerate(DOMAINS):
    slug = d["slug"]
    title = d["title"]
    icon = d["icon"]
    desc = d["desc"]
    sub_count = d["sub_count"]
    concept_count = d["concept_count"]
    page = d["page"]
    idx_str = f"{i+1:02d}"
    
    badge_html = f'<span class="d-chip masterclass-badge">Standalone Guide ↗</span>' if page else ''
    page_btn = f'<a href="{page}" class="d-act-link" onclick="event.stopPropagation()">Masterclass ↗</a>' if page else ''
    
    deck_cards.append(f'''    <div class="domain-card" data-domain="{slug}" id="card-{slug}" onclick="switchDomain('{slug}')">
      <div class="domain-card-head">
        <div class="domain-card-icon">{icon}</div>
        <div class="domain-card-meta">
          <span class="domain-card-idx">Domain {idx_str} / 16</span>
          <h3 class="domain-card-title">{title}</h3>
        </div>
      </div>
      <p class="domain-card-desc">{desc}</p>
      <div class="domain-card-chips">
        <span class="d-chip">{concept_count} concepts</span>
        <span class="d-chip">{sub_count} subsections</span>
        {badge_html}
      </div>
      <div class="domain-card-actions">
        <button type="button" class="d-act-btn">Explore Domain ↓</button>
        {page_btn}
      </div>
    </div>''')

domain_deck_html = f'''  <section class="domain-deck-section" id="domain-navigator">
    <div class="domain-deck-head">
      <div>
        <h2>Interactive Domain Navigator</h2>
        <p class="domain-deck-subtitle">Select any engineering discipline to isolate that domain, or open its dedicated masterclass.</p>
      </div>
      <button type="button" class="focus-btn view-all-btn" onclick="switchDomain('all')">🌐 View All 16 Domains</button>
    </div>
    <div class="domain-deck">
{chr(10).join(deck_cards)}
    </div>
  </section>'''

pill_items = ['''      <button type="button" class="d-nav-pill active" data-target="all" onclick="switchDomain('all')">
        <span>🌐</span> All Domains (16)
      </button>''']

for d in DOMAINS:
    slug = d["slug"]
    icon = d["icon"]
    short_label = {
        "aws": "AWS", "azure": "Azure", "gcp": "GCP", "linux": "Linux",
        "git": "Git", "docker": "Docker", "k8s": "Kubernetes", "terraform": "Terraform",
        "cicd": "CI/CD", "kafka": "Kafka", "spark": "Spark", "postgres": "PostgreSQL",
        "redis": "Redis", "java": "Java", "python": "FastAPI", "apis": "APIs"
    }.get(slug, d["title"])
    pill_items.append(f'''      <button type="button" class="d-nav-pill" data-target="{slug}" onclick="switchDomain('{slug}')">
        <span>{icon}</span> {short_label}
      </button>''')

sticky_bar_html = f'''  <div class="domain-nav-bar" id="domain-nav-bar">
    <div class="domain-nav-scroll">
{chr(10).join(pill_items)}
    </div>
  </div>'''

updated_html = orig_html

# Update title
updated_html = re.sub(r'<title>.*?</title>', '<title>All-in-One Tech & Engineering Portal | AWS, DevOps, Git, CI/CD, K8s, Backend</title>', updated_html)

# Update Hero
new_hero = '''  <div class="hero">
    <div class="edition">v3 · All-in-One Tech &amp; Engineering Portal · 16 Disciplines · 58 Subsections · 239 Concepts</div>
    <h1>All-in-One Tech &amp; Engineering Portal</h1>
    <p class="subtitle">Complete interactive curriculum across Cloud Architecture, DevOps, Containerization, Distributed Systems, Databases &amp; Modern Backend Engineering.</p>
  </div>'''
updated_html = re.sub(r'<div class="hero">[\s\S]*?</div>\s*<div class="stats">', new_hero + '\n\n  <div class="stats">', updated_html)

# Inject CSS into style
if '/* All-in-One Tech Portal Design System */' not in updated_html:
    updated_html = re.sub(r'(<style[\s\S]*?>)', r'\1\n' + CSS_INJECTION, updated_html, count=1)

# Inject Deck & Bar after controls
if 'id="domain-navigator"' not in updated_html:
    controls_end = re.search(r'</div>\s*</div>\s*(?=<section class="resources-section"|<section class="learning-coverage"|<nav class="toc">|<section class="section")', updated_html)
    if controls_end:
        insert_idx = controls_end.end()
        updated_html = updated_html[:insert_idx] + '\n\n' + domain_deck_html + '\n' + sticky_bar_html + '\n\n' + updated_html[insert_idx:]
        print("Injected Domain Deck and Sticky Nav Bar.")

# Update sections
for i, d in enumerate(DOMAINS):
    sid = d["id"]
    slug = d["slug"]
    title = d["title"]
    sub_count = d["sub_count"]
    concept_count = d["concept_count"]
    page = d["page"]
    page_btn = f'<a href="{page}" class="focus-btn masterclass-btn">Dedicated Masterclass ↗</a>' if page else ''
    
    focus_bar = f'''  <div class="domain-focus-bar">
    <div class="focus-bar-left">
      <span class="focus-bar-pill">Domain {i+1} of 16</span>
      <span class="focus-bar-title">{title}</span>
      <span class="focus-bar-stats">{concept_count} concepts &bull; {sub_count} subsections</span>
    </div>
    <div class="focus-bar-right">
      <button type="button" class="focus-btn" onclick="navigateDomain(-1)">← Prev Domain</button>
      <button type="button" class="focus-btn view-all-btn" onclick="switchDomain('all')">🌐 View All (16)</button>
      <button type="button" class="focus-btn" onclick="navigateDomain(1)">Next Domain →</button>
      {page_btn}
    </div>
  </div>'''

    sec_pattern = re.compile(rf'<section class="section[^"]*"\s+id="{sid}"([^>]*)>')
    def repl(m, s=slug, fb=focus_bar, sec_id=sid):
        extra_attrs = m.group(1)
        # Avoid duplicate data-domain if already applied
        if 'data-domain=' in extra_attrs:
            return m.group(0)
        return f'<section class="section domain-section" id="{sec_id}" data-domain="{s}"{extra_attrs}>\n  <div id="{s}"></div>\n{fb}'
    
    updated_html = sec_pattern.sub(repl, updated_html)

# Add client-side domain script
domain_js = '''
  // ============================================================
  // All-in-One Tech Portal Interactive Navigation & Routing
  // ============================================================
  const DOMAIN_SLUGS = ["aws","azure","gcp","linux","git","docker","k8s","terraform","cicd","kafka","spark","postgres","redis","java","python","apis"];
  let currentActiveDomain = 'all';

  window.switchDomain = function(slug) {
    if (!slug || slug === 'all') {
      currentActiveDomain = 'all';
      document.querySelectorAll('.section.domain-section').forEach(sec => {
        sec.classList.remove('hidden-domain');
      });
      document.querySelectorAll('.domain-card').forEach(card => {
        card.classList.remove('active-deck-card');
      });
      document.querySelectorAll('.d-nav-pill').forEach(pill => {
        pill.classList.toggle('active', pill.dataset.target === 'all');
      });
      if (history.replaceState) {
        history.replaceState(null, '', window.location.pathname + window.location.search);
      }
      return;
    }

    currentActiveDomain = slug;
    const target = document.querySelector(`.section.domain-section[data-domain="${slug}"]`) || document.getElementById(`section-${slug}`) || document.getElementById(slug);
    if (!target) return;

    document.querySelectorAll('.section.domain-section').forEach(sec => {
      if (sec === target || sec.getAttribute('data-domain') === slug) {
        sec.classList.remove('hidden-domain');
      } else {
        sec.classList.add('hidden-domain');
      }
    });

    document.querySelectorAll('.domain-card').forEach(card => {
      card.classList.toggle('active-deck-card', card.dataset.domain === slug);
    });

    document.querySelectorAll('.d-nav-pill').forEach(pill => {
      pill.classList.toggle('active', pill.dataset.target === slug);
    });

    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    if (history.replaceState) {
      history.replaceState(null, '', '#' + slug);
    }
  };

  window.navigateDomain = function(step) {
    let idx = DOMAIN_SLUGS.indexOf(currentActiveDomain);
    if (idx === -1) idx = step > 0 ? -1 : DOMAIN_SLUGS.length;
    let nextIdx = (idx + step + DOMAIN_SLUGS.length) % DOMAIN_SLUGS.length;
    window.switchDomain(DOMAIN_SLUGS[nextIdx]);
  };

  function checkUrlHash() {
    const hash = window.location.hash.replace(/^#/, '');
    if (!hash) return;
    if (DOMAIN_SLUGS.includes(hash)) {
      window.switchDomain(hash);
    } else if (hash.startsWith('section-')) {
      const secNum = parseInt(hash.replace('section-', ''), 10);
      if (secNum >= 1 && secNum <= DOMAIN_SLUGS.length) {
        window.switchDomain(DOMAIN_SLUGS[secNum - 1]);
      }
    }
  }

  window.addEventListener('hashchange', checkUrlHash);

  const sInputOriginal = document.getElementById('search-input');
  if (sInputOriginal) {
    sInputOriginal.addEventListener('input', (e) => {
      if (e.target.value.trim().length > 0 && currentActiveDomain !== 'all') {
        window.switchDomain('all');
      }
    });
  }

  checkUrlHash();
'''

if 'DOMAIN_SLUGS' not in updated_html:
    updated_html = updated_html.replace('</body>', f'<script>\n{domain_js}\n</script>\n</body>')
    print("Injected Portal JS logic.")

atomic_write(SRC_PATH, updated_html)
print("Updated cloud_aws_azure.html successfully.")
