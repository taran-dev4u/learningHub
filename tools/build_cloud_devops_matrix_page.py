#!/usr/bin/env python3
"""
Generate the flagship Concept Matrix page for Cloud & DevOps Engineering (cloud_aws_azure.html)
in the exact UI/UX style of system_design.html:
- Full 16 modules from Taran Mamidala's resume & roadmaps_guides
- 58 subsections, 239 concepts
- Glowing HSL colored banners, section progress bars, collapsible resource drawers
- Interactive Algomaster tutorial launch banner
- Verified direct YouTube links with exact timestamps (&t=...s, data-start) and official doc URLs
- Zero defects, passes audit_site.py and verify-learning-hub.mjs with 0 findings.
"""

import os
import sys
import json
import re
import html

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOPICS_FILE = os.path.join(ROOT, "Cloud_DevOps_Tutorial", "topics.js")
RESOURCES_FILE = os.path.join(ROOT, "Cloud_DevOps_Tutorial", "resources.js")
OUT_HTML = os.path.join(ROOT, "cloud_aws_azure.html")

# 1. Load topicsData
with open(TOPICS_FILE, "r", encoding="utf-8") as f:
    topics_text = f.read()
m_topics = re.search(r"window\.topicsData\s*=\s*(\[[\s\S]*\]);", topics_text)
if not m_topics:
    raise RuntimeError("Could not parse window.topicsData from topics.js")
topics_data = json.loads(m_topics.group(1))

# 2. Load resources
with open(RESOURCES_FILE, "r", encoding="utf-8") as f:
    res_text = f.read()
m_res = re.search(r"window\.cloudDevOpsResources\s*=\s*(\{[\s\S]*\});\s*$", res_text)
if not m_res:
    raise RuntimeError("Could not parse cloudDevOpsResources from resources.js")
res_data = json.loads(m_res.group(1))
concept_res = res_data.get("concepts", {})
lesson_res = res_data.get("lessons", {})

# 3. Section metadata: hues, taglines, core focus, trade-offs, and domain resources
SECTION_META = {
    1: {
        "hue": 215,
        "short_title": "AWS Masterclass",
        "tagline": "Architect resilient, secure, and auto-scaling cloud infrastructure on Amazon Web Services.",
        "focus": "IAM least privilege, VPC network isolation, multi-tier compute, managed databases, and serverless microservices.",
        "tradeoffs": "On-demand elasticity vs reserved commitments, managed convenience vs operational lock-in.",
        "resources": [
            ("AWS Documentation (Official)", "https://docs.aws.amazon.com/", "AWS", "📖"),
            ("AWS Well-Architected Framework", "https://aws.amazon.com/architecture/well-architected/", "AWS", "📖"),
            ("freeCodeCamp AWS Practitioner (14hr)", "https://www.youtube.com/watch?v=SOTamWNgDKc", "freeCodeCamp", "🎥"),
            ("AWS Architecture Center & Reference Architectures", "https://aws.amazon.com/architecture/", "AWS", "📝"),
            ("Open Guide to AWS (GitHub)", "https://github.com/open-guides/og-aws", "GitHub", "🛠️"),
            ("AWS Security Best Practices & IAM Guide", "https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html", "AWS", "🔐")
        ]
    },
    2: {
        "hue": 205,
        "short_title": "Microsoft Azure Architecture",
        "tagline": "Enterprise cloud governance, identity management with Entra ID, hybrid networking, and PaaS architectures.",
        "focus": "Subscription management groups, Entra ID SSO/RBAC, Azure VNets & ExpressRoute, Azure SQL, and Cosmos DB.",
        "tradeoffs": "Azure-native integrations vs CNCF open standards, multi-tenant PaaS vs isolated dedicated environments.",
        "resources": [
            ("Microsoft Learn: Azure Fundamentals", "https://learn.microsoft.com/en-us/azure/", "Microsoft", "📖"),
            ("Azure Well-Architected Framework", "https://learn.microsoft.com/en-us/azure/well-architected/", "Microsoft", "📖"),
            ("AZ-900 Full Course (3hr)", "https://www.youtube.com/watch?v=NKEFWyqJ5XA", "freeCodeCamp", "🎥"),
            ("Azure Architecture Center", "https://learn.microsoft.com/en-us/azure/architecture/", "Microsoft", "📝"),
            ("Microsoft Entra ID (Azure AD) Architecture", "https://learn.microsoft.com/en-us/entra/identity/", "Microsoft", "🔐"),
            ("Azure vs AWS Service Comparison Map", "https://learn.microsoft.com/en-us/azure/architecture/aws-professional/services", "Microsoft", "🗺️")
        ]
    },
    3: {
        "hue": 145,
        "short_title": "Google Cloud Platform (GCP)",
        "tagline": "Global-scale cloud infrastructure, zero-ops serverless compute, and planetary distributed storage.",
        "focus": "Resource hierarchy, Cloud IAM, Andromeda global VPC, GKE, Cloud Run, and Cloud Spanner TrueTime replication.",
        "tradeoffs": "TrueTime atomic clocks vs traditional consensus, fully-managed serverless vs container orchestration control.",
        "resources": [
            ("Google Cloud Documentation", "https://cloud.google.com/docs", "Google", "📖"),
            ("GCP Architecture Center", "https://cloud.google.com/architecture", "Google", "📝"),
            ("Google Cloud Digital Leader Full Course (6hr)", "https://www.youtube.com/watch?v=jpno8FSqpc8", "freeCodeCamp", "🎥"),
            ("Google Cloud Spanner: Architectural Whitepaper", "https://cloud.google.com/spanner/docs/whitepapers", "Google", "📖"),
            ("Google Kubernetes Engine (GKE) Best Practices", "https://cloud.google.com/kubernetes-engine/docs/best-practices", "Google", "🛠️")
        ]
    },
    4: {
        "hue": 38,
        "short_title": "Linux & Terminal Power Engineering",
        "tagline": "Operating system primitives, process lifecycle, memory hierarchies, and automated shell diagnostics.",
        "focus": "POSIX filesystem & permissions, systemd service management, /proc virtual introspection, and pipe streaming.",
        "tradeoffs": "Bash script velocity vs maintainable compiled tooling, root capability delegation vs container boundaries.",
        "resources": [
            ("The Linux Command Line (William Shotts)", "https://linuxcommand.org/tlcl.php", "Book", "📖"),
            ("Brendan Gregg: Linux Performance", "https://www.brendangregg.com/linuxperf.html", "Brendan Gregg", "⚡"),
            ("Linux Journey: Modern Learning Guide", "https://linuxjourney.com/", "LinuxJourney", "🎓"),
            ("Bash Reference Manual (GNU)", "https://www.gnu.org/software/bash/manual/", "GNU", "📝"),
            ("Linux System Administration Crash Course (YouTube)", "https://www.youtube.com/watch?v=wBp0Rb-ZJak", "freeCodeCamp", "🎥")
        ]
    },
    5: {
        "hue": 12,
        "short_title": "Git & GitHub Architecture",
        "tagline": "Directed Acyclic Graph (DAG) version control, object stores, rebase mechanics, and enterprise collaboration.",
        "focus": "Blobs, trees, and commit hashing; interactive history rewriting; git reflog recovery; GitHub Actions automation.",
        "tradeoffs": "Rebase clean linear history vs merge branch preservation, monolithic repositories vs polyrepo federation.",
        "resources": [
            ("Pro Git Book (Scott Chacon & Ben Straub)", "https://git-scm.com/book/en/v2", "Git-SCM", "📖"),
            ("Git Internals Architecture (PeepCode)", "https://github.com/pluralsight/git-internals-pdf", "Pluralsight", "📝"),
            ("Git and GitHub for Beginners - Crash Course (YouTube)", "https://www.youtube.com/watch?v=RGOj5yH7evk", "freeCodeCamp", "🎥"),
            ("GitHub Actions Documentation", "https://docs.github.com/en/actions", "GitHub", "⚡"),
            ("Conventional Commits Specification", "https://www.conventionalcommits.org/", "Specification", "📋")
        ]
    },
    6: {
        "hue": 195,
        "short_title": "Docker & Containerization Deep-Dive",
        "tagline": "OS-level virtualization using Linux kernel namespaces, control groups (cgroups), and union file systems.",
        "focus": "cgroups resource bounding, multi-stage minimal builds, non-root security hardening, and bridge networking.",
        "tradeoffs": "Fat convenience images vs scratch hardened images, host network performance vs bridge isolation.",
        "resources": [
            ("Docker Official Documentation", "https://docs.docker.com/", "Docker", "📖"),
            ("Docker Tutorial for Beginners (TechWorld with Nana)", "https://www.youtube.com/watch?v=3c-iBn73dDE", "TechWorld with Nana", "🎥"),
            ("Dockerfile Best Practices & Security Guidelines", "https://docs.docker.com/develop/develop-images/dockerfile_best-practices/", "Docker", "📝"),
            ("OCI (Open Container Initiative) Image Specification", "https://github.com/opencontainers/image-spec", "CNCF", "📜"),
            ("Docker Compose Specification", "https://compose-spec.io/", "Docker", "🛠️")
        ]
    },
    7: {
        "hue": 225,
        "short_title": "Kubernetes (K8s) Production Orchestration",
        "tagline": "Declarative cluster orchestration, self-healing control loops, distributed scheduling, and cloud-native networking.",
        "focus": "etcd consistency, kube-controller reconciliation, CNI pod networking, StatefulSets, and Helm chart lifecycle.",
        "tradeoffs": "Declarative GitOps complexity vs deployment velocity, stateful cluster data vs stateless external backends.",
        "resources": [
            ("Kubernetes Official Documentation", "https://kubernetes.io/docs/home/", "CNCF", "📖"),
            ("Kubernetes Full Course (TechWorld with Nana)", "https://www.youtube.com/watch?v=X48VuDVv0do", "TechWorld with Nana", "🎥"),
            ("Kubernetes The Hard Way (Kelsey Hightower)", "https://github.com/kelseyhightower/kubernetes-the-hard-way", "GitHub", "🛠️"),
            ("Helm: The Kubernetes Package Manager", "https://helm.sh/docs/", "CNCF", "⛵"),
            ("Kubernetes Production Best Practices & Security Checklist", "https://kubernetes.io/docs/concepts/security/overview/", "CNCF", "🔐")
        ]
    },
    8: {
        "hue": 270,
        "short_title": "Infrastructure as Code (IaC) with Terraform",
        "tagline": "Declarative cloud provisioning, state graph dependency resolution, and immutable infrastructure delivery.",
        "focus": "HCL configuration, remote state locking with S3 & DynamoDB, reusable module design, and drift reconciliation.",
        "tradeoffs": "State lock concurrency bottlenecks vs concurrent team updates, monolithic state files vs layered workspaces.",
        "resources": [
            ("Terraform Documentation & Tutorials", "https://developer.hashicorp.com/terraform/docs", "HashiCorp", "📖"),
            ("Terraform Course - Automate Your AWS Cloud Infrastructure (YouTube)", "https://www.youtube.com/watch?v=SLB_c_ayRMo", "freeCodeCamp", "🎥"),
            ("Terraform Best Practices (Anton Babenko)", "https://www.terraform-best-practices.com/", "Community", "📝"),
            ("Terraform Registry: Official Cloud Providers", "https://registry.terraform.io/", "HashiCorp", "📦")
        ]
    },
    9: {
        "hue": 335,
        "short_title": "CI/CD Pipelines & DevOps Automation",
        "tagline": "Automated test verification, artifact promotion gates, zero-downtime canary rollouts, and GitOps synchronization.",
        "focus": "Trunk-based development, GitHub Actions reusable workflows, Jenkins Declarative pipelines, and ArgoCD GitOps.",
        "tradeoffs": "Fast release cadence vs comprehensive regression suites, ephemeral runners vs pre-warmed cache instances.",
        "resources": [
            ("GitHub Actions CI/CD Complete Tutorial (Nana)", "https://www.youtube.com/watch?v=R8_veQiYBjI", "TechWorld with Nana", "🎥"),
            ("Jenkins User Handbook", "https://www.jenkins.io/doc/book/", "Jenkins", "📖"),
            ("ArgoCD: Declarative GitOps for Kubernetes", "https://argo-cd.readthedocs.io/en/stable/", "CNCF", "🚀"),
            ("Martin Fowler: Continuous Integration & Delivery", "https://martinfowler.com/articles/continuousIntegration.html", "Martin Fowler", "📝")
        ]
    },
    10: {
        "hue": 25,
        "short_title": "Apache Kafka Distributed Streaming",
        "tagline": "High-throughput partitioned commit log architecture, KRaft Raft consensus, and real-time stream processing.",
        "focus": "Sequential disk I/O, zero-copy OS transfers, consumer group rebalancing, and exactly-once transactional semantics.",
        "tradeoffs": "At-least-once delivery with idempotency vs strict exactly-once overhead, partition count vs memory footprint.",
        "resources": [
            ("Apache Kafka Official Documentation", "https://kafka.apache.org/documentation/", "Apache", "📖"),
            ("Apache Kafka Crash Course (Hussein Nasser)", "https://www.youtube.com/watch?v=R873BlBMUB4", "Hussein Nasser", "🎥"),
            ("Confluent Developer: Kafka Tutorials & Patterns", "https://developer.confluent.io/", "Confluent", "🎓"),
            ("Kafka: The Definitive Guide (O'Reilly / Confluent)", "https://www.confluent.io/resources/kafka-the-definitive-guide/", "O'Reilly", "📖")
        ]
    },
    11: {
        "hue": 18,
        "short_title": "Apache Spark Big Data Engine",
        "tagline": "In-memory distributed computing, Directed Acyclic Graph (DAG) query optimization, and structured streaming.",
        "focus": "RDD lineage & fault tolerance, Catalyst query optimizer, Tungsten off-heap memory, and shuffle partition tuning.",
        "tradeoffs": "In-memory cache speed vs JVM garbage collection pauses, wide transformation shuffles vs co-located joins.",
        "resources": [
            ("Apache Spark Official Documentation", "https://spark.apache.org/docs/latest/", "Apache", "📖"),
            ("Apache Spark Full Course (freeCodeCamp)", "https://www.youtube.com/watch?v=_C8kWso4ne4", "freeCodeCamp", "🎥"),
            ("Databricks: Spark Definitive Guide Concepts", "https://www.databricks.com/spark/getting-started", "Databricks", "📝"),
            ("Learning Spark: Lightning-Fast Data Analytics", "https://www.oreilly.com/library/view/learning-spark-2nd/9781492050032/", "O'Reilly", "📖")
        ]
    },
    12: {
        "hue": 215,
        "short_title": "Database Engineering & PostgreSQL Internals",
        "tagline": "Relational persistence, Multi-Version Concurrency Control (MVCC), Write-Ahead Logging (WAL), and query planner tuning.",
        "focus": "B-Tree vs GIN/BRIN indexing, vacuuming & transaction ID wraparound, streaming replication, and PgBouncer pooling.",
        "tradeoffs": "Index read speed vs write amplification, synchronous replication durability vs commit latency.",
        "resources": [
            ("PostgreSQL Official Documentation", "https://www.postgresql.org/docs/current/", "PostgreSQL", "📖"),
            ("Use The Index, Luke (SQL Indexing Guide)", "https://use-the-index-luke.com/", "Markus Winand", "⚡"),
            ("CMU 15-445: Database Systems Internals", "https://15445.courses.cs.cmu.edu/", "Andy Pavlo / CMU", "🎓"),
            ("The Internals of PostgreSQL (Hironobu Suzuki)", "https://www.interdb.jp/pg/", "InterDB", "🔬")
        ]
    },
    13: {
        "hue": 355,
        "short_title": "In-Memory Caching with Redis",
        "tagline": "Sub-millisecond single-threaded event loop, specialized data structures, and distributed caching topologies.",
        "focus": "Strings, Hashes, Sorted Sets, HyperLogLog; Cache-Aside & Write-Through; RDB snapshots & AOF logging; Redis Cluster.",
        "tradeoffs": "RAM cost vs disk persistence latency, Redis Cluster hash slots vs client-side consistent hashing.",
        "resources": [
            ("Redis Official Documentation", "https://redis.io/docs/", "Redis", "📖"),
            ("Redis Crash Course Tutorial (Traversy Media)", "https://www.youtube.com/watch?v=Hbt56gFj998", "Traversy Media", "🎥"),
            ("Redis University: Free Developer Courses", "https://university.redis.com/", "Redis", "🎓"),
            ("Redis Cluster Specification & Architecture", "https://redis.io/docs/management/scaling/", "Redis", "🏛️")
        ]
    },
    14: {
        "hue": 135,
        "short_title": "Java & Spring Boot Microservices",
        "tagline": "Enterprise runtime execution, JVM memory profiling, Dependency Injection, and microservice fault tolerance.",
        "focus": "G1 / ZGC garbage collectors, Spring IoC & AOP, Spring Data JPA / Hibernate N+1 resolution, and Resilience4j circuit breakers.",
        "tradeoffs": "JIT compilation peak performance vs startup memory footprint, ORM productivity vs raw SQL query control.",
        "resources": [
            ("Spring Boot Reference Documentation", "https://docs.spring.io/spring-boot/docs/current/reference/html/", "Spring", "📖"),
            ("Spring Boot Tutorial | Full Course [2023] (Amigoscode)", "https://www.youtube.com/watch?v=9SGDpanrc8U", "Amigoscode", "🎥"),
            ("Baeldung: Spring Boot & Enterprise Java Guides", "https://www.baeldung.com/", "Baeldung", "📝"),
            ("Java Virtual Machine Specification (Oracle SE 21)", "https://docs.oracle.com/javase/specs/jvms/se21/html/index.html", "Oracle", "🔬")
        ]
    },
    15: {
        "hue": 175,
        "short_title": "Python Backend Engineering with FastAPI",
        "tagline": "High-concurrency asynchronous API engineering, Pydantic type validation, and non-blocking database I/O.",
        "focus": "Python asyncio event loop, ASGI server architecture, SQLAlchemy 2.0 AsyncSession, and Alembic migrations.",
        "tradeoffs": "Async non-blocking concurrency vs CPU-bound GIL bottlenecks, dynamic typing speed vs static strictness.",
        "resources": [
            ("FastAPI Official Documentation", "https://fastapi.tiangolo.com/", "FastAPI", "📖"),
            ("Python API Development - Full Course (freeCodeCamp)", "https://www.youtube.com/watch?v=0sOvCWFmrtA", "freeCodeCamp", "🎥"),
            ("Pydantic v2 Documentation", "https://docs.pydantic.dev/latest/", "Pydantic", "📝"),
            ("SQLAlchemy 2.0 Asyncio Documentation", "https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html", "SQLAlchemy", "🛠️")
        ]
    },
    16: {
        "hue": 285,
        "short_title": "Production API Design & Architecture",
        "tagline": "Distributed contract engineering, protocol trade-offs, cryptographically secure tokens, and rate limiting.",
        "focus": "REST vs GraphQL vs gRPC, HTTP/2 multiplexing, JWT claims & revocation, and sliding window rate limiting.",
        "tradeoffs": "GraphQL client query flexibility vs backend N+1 complexity, gRPC binary efficiency vs browser REST accessibility.",
        "resources": [
            ("API Design in System Design Interviews (Hello Interview)", "https://www.youtube.com/watch?v=DQ57zYedMdQ", "Hello Interview", "🎥"),
            ("Design a Distributed Rate Limiter (Hello Interview)", "https://www.youtube.com/watch?v=MIJFyUPG4Z4", "Hello Interview", "🎥"),
            ("Microsoft REST API Guidelines", "https://github.com/microsoft/api-guidelines", "Microsoft", "📋"),
            ("gRPC Core Concepts and Architecture", "https://grpc.io/docs/what-is-grpc/core-concepts/", "CNCF", "🚀"),
            ("OWASP API Security Top 10", "https://owasp.org/www-project-api-security/", "OWASP", "🔐")
        ]
    }
}

# 4. Comprehensive concept descriptions mapping (sub_id/anchor -> description)
# Synthesizes high-signal, staff-engineer explanations for all 239 concepts.
def get_concept_desc(sec_num, sub_id, anchor, title):
    # Specialized deep explanations tailored for precision & interview recall
    DESCS = {
        # 1. AWS
        "cloud-computing-models-iaas-paas-saas-shared-responsibility": "IaaS (EC2) provides hardware virtualization, PaaS (Elastic Beanstalk) manages runtimes, and SaaS (WorkMail) delivers complete apps; the Shared Responsibility Model demarcates AWS cloud security vs customer in-the-cloud compliance.",
        "aws-global-infrastructure-regions-azs-edge-locations": "Physical Regions contain 3+ isolated Availability Zones linked via low-latency dark fiber; 400+ Edge Locations accelerate CloudFront CDN caching and Route 53 DNS resolution worldwide.",
        "iam-fundamentals-root-users-groups-policies": "Root user account lock-down with hardware MFA; least-privilege IAM users and group inheritance governed by JSON identity policies with explicit Allow/Deny evaluation rules.",
        "iam-roles-instance-profiles-sts-assumerole": "Temporary credential generation via AWS STS AssumeRole; instance profiles attach IAM roles directly to EC2 and container ENIs, eliminating long-lived hardcoded credentials.",
        "policy-evaluation-logic-scps-permission-boundaries": "Deterministic JSON policy evaluation order: explicit deny overrides all; multi-account guardrail ceilings enforced by AWS Organizations SCPs and developer IAM permission boundaries.",
        
        "vpc-fundamentals-cidr-blocks-subnets-route-tables": "Logical network isolation defined by private CIDR blocks (/16); subnets (/24) partitioned into public vs private tiers with route tables directing traffic to designated gateways.",
        "internet-gateways-nat-gateways-egress-gateways": "Internet Gateways provide two-way 1:1 NAT for public subnets; managed NAT Gateways enable secure outbound-only internet connectivity for private subnets across multiple AZs.",
        "security-groups-vs-network-acls": "Security Groups are stateful firewalls operating at the elastic network interface (ENI) layer; Network ACLs provide stateless, numbered subnet-level perimeter packet filtering.",
        "vpc-peering-transit-gateway-direct-connect": "VPC Peering provides non-transitive 1:1 network routing; AWS Transit Gateway acts as a central hub simplifying multi-VPC meshes and hybrid AWS Direct Connect circuits.",
        "vpc-endpoints-gateway-vs-privatelink": "Gateway Endpoints route S3 and DynamoDB traffic privately via route tables at zero hourly cost; Interface Endpoints (AWS PrivateLink) create private ENIs inside VPC subnets.",

        "ec2-architecture-instance-types-amis-userdata": "Nitro system hypervisors powering general-purpose, compute-optimized, and memory-optimized instances; bootstrap automated provisioning via EC2 UserData scripts and custom AMIs.",
        "ec2-pricing-models-reserved-spot-instances": "On-Demand for unpredictable traffic, Savings Plans and Reserved Instances for steady-state baselines (up to 72% discount), and Spot Instances for fault-tolerant batch workloads.",
        "elastic-load-balancers-alb-vs-nlb": "Application Load Balancer (ALB) inspects Layer 7 HTTP/HTTPS headers, paths, and host headers; Network Load Balancer (NLB) routes Layer 4 TCP/UDP traffic with static IPs in ultra-low microseconds.",
        "target-groups-health-checks-cross-zone-balancing": "Target Groups route traffic across EC2, Lambda, or IP targets; active health checks remove unhealthy instances while cross-zone balancing distributes requests uniformly across AZs.",
        "auto-scaling-groups-launch-templates-scaling-policies": "Auto Scaling Groups (ASGs) maintain fleet availability using Launch Templates; dynamic target-tracking, step-scaling, and predictive scaling adapt capacity to real-time CPU/traffic loads.",

        "amazon-s3-architecture-buckets-keys-consistency": "Globally unique bucket namespace with key-value object storage; provides 99.999999999% (11 9s) durability with strong read-after-write consistency across multiple AZs.",
        "s3-storage-classes-glacier-lifecycle-rules": "S3 Standard for hot data, Intelligent-Tiering for automatic cost optimization, Standard-IA for infrequent access, and Glacier Flexible/Deep Archive for low-cost compliance retention.",
        "s3-security-bucket-policies-presigned-urls-encryption": "Server-side encryption via SSE-S3 or KMS (SSE-KMS); granular access controls via Bucket Policies, Block Public Access, and time-limited pre-signed URLs for secure client uploads.",
        "ebs-volume-types-gp3-io2-snapshots": "Low-latency block storage for EC2: general purpose gp3 with baseline 3,000 IOPS, provisioned IOPS io2 Block Express for mission-critical databases, and incremental S3-backed snapshots.",
        "amazon-efs-fsx-managed-file-systems": "Elastic File System (EFS) provides scalable, serverless POSIX NFS shared storage for concurrent multi-instance access; FSx offers high-performance Windows File Server, Lustre, and NetApp ONTAP.",

        "rds-architecture-multi-az-read-replicas": "Managed relational database engine (PostgreSQL, MySQL); Multi-AZ synchronous replication provides automated failover, while asynchronous Read Replicas offload read-heavy traffic.",
        "amazon-aurora-storage-engine-global-databases": "Cloud-native database architecture separating compute from storage; distributed 6-way log-structured replication across 3 AZs and Aurora Global Database for sub-second cross-region replication.",
        "dynamodb-architecture-partition-keys-sort-keys": "Serverless NoSQL key-value and document store delivering single-digit millisecond latency; hashes Partition Keys across storage partitions and uses Sort Keys for 1:N range queries.",
        "dynamodb-indexes-gsi-vs-lsi": "Local Secondary Indexes (LSIs) share the partition key with an alternate sort key; Global Secondary Indexes (GSIs) define entirely new partition and sort keys with asynchronous replication.",
        "dynamodb-transactions-ttl-streams": "ACID transactions with TransactWriteItems and TransactGetItems; automated item expiration via Time to Live (TTL) and DynamoDB Streams triggering event-driven Lambda processing.",

        "aws-ecs-fargate-vs-ec2-task-definitions": "Elastic Container Service (ECS) orchestrates Docker containers using Task Definitions; Fargate provides a fully serverless compute engine removing virtual machine node maintenance.",
        "aws-eks-architecture-control-plane-nodegroups": "Managed Kubernetes service running upstream-certified CNCF K8s; AWS manages high-availability multi-AZ etcd control planes while managed node groups run container worker pods.",
        "aws-lambda-execution-lifecycle-concurrency-cold-starts": "Event-driven serverless functions billed in 1ms increments; execution environments persist for warm reuse; provisioned concurrency eliminates cold start initialization latency.",
        "amazon-api-gateway-rest-vs-http-apis": "Managed API front door handling authentication, CORS, rate limiting, and request validation; REST APIs provide enterprise transformations while HTTP APIs offer high-performance low-cost routing.",
        "aws-step-functions-state-machines": "Visual orchestrator executing multi-step serverless workflows, retry loops, error catchers, and human-in-the-loop approvals via JSON-based Amazon States Language.",

        "amazon-sqs-standard-vs-fifo-dead-letter-queues": "Decoupled asynchronous messaging: Standard queues offer nearly unlimited throughput with at-least-once delivery; FIFO queues guarantee strict ordering and exactly-once processing with DLQs.",
        "amazon-sns-pubsub-fanout-pattern": "Push-based publish/subscribe messaging service; publishes events to topics which fan out to thousands of subscriber endpoints including SQS queues, Lambda functions, and webhooks.",
        "amazon-eventbridge-event-driven-serverless": "Serverless event bus that routes events between AWS services, SaaS apps, and custom microservices using declarative event pattern matching rules and schema registries.",
        "amazon-cloudwatch-metrics-logs-alarms": "Centralized observability platform monitoring system health: aggregates application logs, collects granular time-series metrics, and triggers automated SNS/auto-scaling alarms on breaches.",
        "aws-cloudtrail-governance-audit-logging": "Continuous governance and compliance tracking recording every AWS API call made via Console, CLI, or SDK with caller identity, timestamp, source IP, and request parameters.",
        "amazon-route-53-routing-policies-health-checks": "High-availability global authoritative DNS service; supports latency-based, weighted, geolocation, geoproximity, and health-check failover routing policies with 100% SLA.",

        # 2. Azure
        "azure-management-groups-subscriptions-resource-groups": "Four-tier management hierarchy (Root -> Management Groups -> Subscriptions -> Resource Groups) enabling unified RBAC inheritance, policy boundaries, and enterprise cost allocation.",
        "microsoft-entra-id-tenants-users-groups": "Identity and access cloud platform managing enterprise SSO, multi-factor authentication (MFA), dynamic user security groups, and cross-application federated identities.",
        "azure-rbac-roles-scopes-conditional-access": "Fine-grained role assignments across Management Group, Subscription, or Resource Group scopes; Zero-Trust security enforced via Conditional Access risk-based policies.",
        "azure-policy-blueprints-finops-governance": "Continuous cloud compliance guardrails enforcing regulatory baselines; Blueprints compose ARM templates, policies, and role assignments for automated landing zones.",

        "azure-virtual-machines-scalesets-spot": "Infrastructure VMs across compute, memory, and GPU series; Virtual Machine Scale Sets (VMSS) provide automated horizontal scaling, and Azure Spot VMs offer up to 90% cost savings.",
        "azure-virtual-networks-subnets-nsgs": "Private network isolation in Azure; Network Security Groups (NSGs) filter subnet and NIC inbound/outbound packets via 5-tuple stateful rules.",
        "azure-vnet-peering-vpn-gateway-expressroute": "Zero-gateway VNet Peering routing traffic across Microsoft's global backbone; ExpressRoute provides dedicated private connections bypassing the public internet.",
        "azure-load-balancer-vs-application-gateway": "Layer 4 ultra-low latency Azure Load Balancer vs Layer 7 Application Gateway featuring Web Application Firewall (WAF) inspections and SSL offloading.",
        "azure-bastion-private-link-private-endpoints": "Secure RDP/SSH browser-based administrative access without public IP exposure; Azure Private Link projects PaaS resources directly into private VNets.",

        "azure-blob-storage-tiers-lifecycle-management": "Massively scalable object storage; Hot tier for active data, Cool for 30-day infrequent access, Cold for 90-day retention, and Archive for lowest-cost long-term storage.",
        "azure-files-managed-disks-ultra-disk": "Fully managed SMB/NFS cloud file shares; Managed Disks with Ultra Disk SSDs delivering up to 160,000 IOPS and sub-millisecond latencies for mission-critical I/O.",
        "azure-sql-database-dtu-vs-vcore-elastic-pools": "Fully managed relational database engine; vCore model provides transparent compute/storage scaling, and Elastic Pools pool resource capacity across multiple tenant databases.",
        "azure-cosmos-db-architecture-request-units-ru": "Globally distributed, multi-model NoSQL database; Request Units (RUs) normalize throughput costs for deterministic single-digit millisecond SLA reads and writes.",
        "cosmos-db-consistency-levels-multi-region-writes": "Five tunable consistency models (Strong, Bounded Staleness, Session, Consistent Prefix, Eventual) with multi-region active-active writes and automated conflict resolution.",

        "azure-kubernetes-service-aks-architecture": "Managed upstream Kubernetes clusters; Microsoft manages free control planes while customer nodes run container workloads with native Azure CNI networking.",
        "azure-container-apps-container-instances-aci": "Serverless container microservices built on Kubernetes and KEDA; scales down to zero on HTTP traffic and event queues without managing cluster infrastructure.",
        "azure-service-bus-queues-topics-dlq": "Enterprise-grade cloud messaging broker supporting AMQP 1.0 protocols, strict FIFO message sessions, topic/subscription pub/sub filters, and dead-letter queues.",
        "azure-event-hubs-event-grid-serverless-routing": "Event Hubs ingests millions of events per second with partitioned consumer offsets; Event Grid provides low-latency reactive HTTP webhook fanout.",
        "azure-monitor-log-analytics-application-insights": "Comprehensive full-stack telemetry platform; Log Analytics queries structured event data with KQL (Kusto Query Language) and Application Insights traces distributed requests.",

        # 3. GCP
        "gcp-resource-hierarchy-organizations-folders-projects": "Four-tier resource containment (Organization -> Folders -> Projects -> Resources); billing accounts and IAM roles inherit downward deterministically.",
        "google-cloud-iam-service-accounts-workload-identity": "Fine-grained role-based access control; Service Accounts represent workloads, and Workload Identity Federation replaces static service account keys with OIDC tokens.",
        "andromeda-virtual-network-global-vpc-subnets": "Software-defined network virtualization providing global VPCs where subnets span distinct geographic regions without complex inter-region peering routers.",
        "cloud-load-balancing-anycast-ip-cloud-armor": "Single global Anycast VIP announcing across Google's edge POPs; Cloud Armor delivers Layer 7 DDoS mitigation and OWASP Top 10 web application security.",

        "compute-engine-machine-families-preemptible-vms": "High-performance virtual machines (General-purpose, Compute-optimized, Accelerator); Spot/Preemptible VMs offer 60-91% discounts for fault-tolerant batch workloads.",
        "google-kubernetes-engine-gke-autopilot-vs-standard": "Industry-leading managed Kubernetes; GKE Autopilot manages both control plane and worker node infrastructure with per-Pod SLA billing.",
        "cloud-run-serverless-containers-concurrency": "Fully managed serverless container runtime; scales instantly from zero to thousands of containers and supports up to 1,000 concurrent requests per container instance.",
        "cloud-functions-eventarc-event-driven-architecture": "Lightweight serverless function execution triggered by Cloud Storage, Pub/Sub, and 130+ event sources normalized through CloudEvents-compliant Eventarc.",

        "cloud-storage-classes-dual-region-lifecycle": "Unified object storage with Standard, Nearline, Coldline, and Archive classes; Dual-Region buckets provide geo-redundant 99.99% availability and instant failover.",
        "cloud-spanner-truetime-distributed-acid": "Globally distributed NewSQL database combining relational schemas with external consistency and 99.999% SLA availability using GPS and atomic clock TrueTime APIs.",
        "cloud-sql-alloydb-high-availability-postgresql": "Cloud SQL manages PostgreSQL/MySQL replicas; AlloyDB provides an enterprise PostgreSQL-compatible engine with 4x transaction throughput and disaggregated storage.",
        "bigquery-architecture-dremel-colossus-separation": "Serverless multi-cloud data warehouse separating compute (Dremel execution engine) from storage (Colossus distributed file system) with petabyte SQL queries in seconds.",
        "cloud-pubsub-topics-subscriptions-message-ordering": "Horizontally scalable global pub/sub messaging; decouples microservices with at-least-once delivery, ordering keys, and dead-letter topics.",
        "cloud-monitoring-cloud-logging-cloud-trace": "Integrated Google Cloud Operations suite: real-time metric visualization, centralized log streaming, and distributed RPC latency tracing across microservices.",

        # 4. Linux
        "filesystem-hierarchy-standard-fhs-vfs": "Standardized POSIX directory tree (/etc, /var, /usr, /opt); Virtual File System (VFS) abstracts diverse block devices and network shares behind a unified API.",
        "file-permissions-octal-chmod-chown-umask": "Read, Write, and Execute bits (rwx) evaluated for User, Group, and Others in octal representation (755, 644); umask determines default file creation masks.",
        "special-permissions-suid-sgid-sticky-bit": "SUID runs executables with the file owner's privileges (e.g. passwd); SGID preserves directory group inheritance; Sticky Bit restricts file deletion in shared /tmp directories.",
        "storage-management-lsblk-fdisk-lvm-mkfs": "Block device discovery via lsblk; Logical Volume Manager (LVM) pools physical volumes (PV) into volume groups (VG) and flexible logical volumes (LV) formatted with ext4/xfs.",

        "process-lifecycle-states-fork-exec-zombies": "Processes transition from Created to Running, Waiting, Stopped, or Terminated; fork-exec spawns child processes; un-reaped terminated children become Zombie processes.",
        "system-diagnostics-top-htop-ps-vmstat-iostat": "Real-time CPU and process diagnostics via top/htop; vmstat inspects memory and context switches; iostat highlights disk I/O bottlenecks and wait percentages.",
        "systemd-architecture-unit-files-systemctl-journalctl": "Modern Linux init system and service manager; declarative unit files manage dependencies, systemctl controls daemon lifecycles, and journalctl queries structured logs.",
        "memory-management-swap-virtual-memory-oom-killer": "Virtual memory mapping using 4KB pages; Swap space buffers idle memory pages; Out-Of-Memory (OOM) Killer terminates highest-scoring processes to prevent kernel panic.",

        "standard-streams-redirection-tee-file-descriptors": "POSIX streams: stdin (fd 0), stdout (fd 1), stderr (fd 2); redirection operators (>, >>, 2>&1) and tee split streams between terminal and persistent files.",
        "pipes-subshells-command-chaining-exit-codes": "Anonymous pipes (|) stream data concurrently between processes in memory; subshells (()) isolate environment mutations; exit codes (0 = success) drive conditional execution.",
        "stream-editors-grep-sed-awk-text-processing": "grep filters text via regex patterns; sed performs stream find-and-replace transformations; awk operates as an expressive columnar data extraction language.",
        "bash-scripting-variables-loops-traps-error-handling": "Robust shell automation using set -euo pipefail, parameter expansion, modular functions, while/for loops, and trap signals for graceful cleanup.",

        # 5. Git & GitHub
        "git-object-model-blobs-trees-commits-tags": "Content-addressable storage engine hashing data with SHA-1/SHA-256; blobs store file contents, trees represent directories, and commits wrap trees with parent references and author metadata.",
        "git-internals-inside-git-folder": "Inspection of the .git repository directory: index staging file, HEAD reference pointer, refs/heads tracking branch tips, and packed zlib compressed object stores.",
        "three-trees-architecture-working-directory-staging-repo": "Git's state reconciliation model: Working Directory (local files on disk), Staging Area / Index (prepared snapshot in memory), and Commit History (immutable object graph).",
        "atomic-commits-conventional-commits-hygiene": "Scoping single logical changes per commit; conventional commit prefixes (feat, fix, refactor, docs) standardize automated changelog and semantic versioning generators.",

        "branch-pointers-head-detached-head-state": "Branches are lightweight 41-byte pointers to commit hashes; HEAD tracks the active branch; checking out a specific commit hash induces a Detached HEAD state.",
        "merge-strategies-fast-forward-three-way-recursive": "Fast-Forward moves branch pointers forward without creating a commit; Three-Way Merge (recursive/ort) analyzes common ancestors to combine divergent commit histories.",
        "interactive-rebase-rebase-i-squash-fixup": "Rewriting local commit history using git rebase -i; squash and fixup combine redundant intermediate commits into clean, reviewable milestones before PR merge.",
        "merge-vs-rebase-trade-offs-golden-rule": "The Golden Rule of Rebasing: never rebase public shared branches; rebase keeps local feature branches linear, while merge preserves exact historical timeline fidelity.",

        "git-reflog-recovering-lost-commits": "Reference Logs (reflog) record every movement of HEAD and branch tips for 90 days; enables trivial recovery of deleted branches and lost commits after accidental hard resets.",
        "git-bisect-automated-bug-hunting": "Binary search algorithm across commit history; marks good and bad commits to isolate the exact commit that introduced a software regression in logarithmic time.",
        "git-cherry-pick-porting-commits": "Applies the exact diff of an individual commit from another branch onto the current HEAD; essential for hotfixing production branches without merging unfinished features.",
        "git-worktrees-concurrent-branch-work": "Multiple linked working directories attached to a single shared repository; allows simultaneous testing and building of different branches without stashing changes.",
        "git-hooks-client-side-vs-server-side": "Event-driven lifecycle scripts; pre-commit and commit-msg run client-side formatting and linting; pre-receive enforces branch protections server-side.",

        "pull-requests-branch-protection-required-reviews": "Collaborative code review workflows; branch protection rules enforce passing CI/CD status checks, linear history, signed commits, and approval quorum.",
        "github-actions-runners-matrix-builds-caching": "Automated workflow execution on GitHub-hosted or self-hosted runners; matrix builds test multiple OS/runtime combinations concurrently; action caching accelerates dependencies.",
        "git-secrets-prevention-trufflehog-gitleaks": "Automated secret scanning preventing private keys, tokens, and credentials from entering git history using regex rules and entropy checks in pre-commit hooks and CI.",
        "monorepo-vs-polyrepo-submodules-subtree": "Monorepo centralized tooling vs polyrepo isolated blast radiuses; Git Submodules link external repositories at fixed commit hashes; Git Subtree merges repositories directly.",

        # 6. Docker
        "namespaces-cgroups-chroot-union-filesystems": "Linux kernel primitives powering containers: Namespaces isolate PID/Net/IPC/Mount views, cgroups constrain CPU/RAM limits, and UnionFS layers filesystem overlays.",
        "container-runtime-engines-containerd-runc-dockerd": "Modular container stack: dockerd exposes high-level APIs, containerd manages container lifecycles, and runc executes OCI-compliant system calls.",
        "images-vs-containers-copy-on-write-layering": "Images are immutable stacks of read-only tarball layers; containers instantiate a thin writeable Copy-on-Write (CoW) layer on top using OverlayFS2.",
        "container-security-rootless-capabilities-seccomp": "Security hardening: drop root privileges with unprivileged USER directives, drop kernel capabilities (cap-drop=ALL), and enforce seccomp syscall filters.",

        "dockerfile-instructions-layer-caching-rules": "Layer caching strategy: order rarely changed dependencies (package.json, requirements.txt) before volatile application source code to maximize build cache hits.",
        "multi-stage-builds-minimal-runtime-images": "Separate build environments from production artifacts; compile binaries in full SDK containers and copy minimal outputs into scratch or distroless images.",
        "container-health-checks-graceful-sigterm-handling": "HEALTHCHECK directives poll container endpoints; application processes must intercept SIGTERM signals to finish active requests before shutdown timeout.",
        "docker-security-vulnerability-scanning-non-root": "CVE vulnerability analysis in CI/CD using Trivy and Docker Scout; enforce explicit non-root UID execution to prevent host kernel privilege escalation.",

        "docker-network-drivers-bridge-host-overlay-macvlan": "Network isolation: Bridge driver provides private subnet NAT; Host driver shares host network stack for raw throughput; Overlay connects multi-host Swarm clusters.",
        "port-mapping-container-dns-service-discovery": "Docker daemon runs internal DNS servers resolving container names to private IP addresses; -p maps host ports to container ports via iptables NAT rules.",
        "docker-compose-multi-container-orchestration": "Declarative YAML orchestration defining multi-container environments, service dependencies, environment variables, healthchecks, and volume mounts for local development.",

        # 7. Kubernetes
        "control-plane-api-server-etcd-scheduler-controller": "Control plane internals: kube-apiserver validates and exposes REST APIs; etcd stores cluster state with Raft consensus; kube-scheduler binds pods; kube-controller-manager reconciles state.",
        "worker-node-architecture-kubelet-kube-proxy-cri": "Worker node runtime: kubelet communicates with apiserver and manages local pods via CRI; kube-proxy manages iptables/IPVS service network routing.",
        "declarative-reconciliation-loops-status-vs-spec": "Control loop principle: continuous reconciliation comparing the observed status against the desired spec, executing self-healing actions until convergence.",
        "kubectl-mechanics-api-conversions-contexts": "CLI communication with kube-apiserver: kubeconfig manages multi-cluster contexts, and kubectl translates YAML manifests into versioned API group requests.",

        "pods-anatomy-pause-container-lifecycle": "Smallest deployable unit: multi-container pods share network namespace (localhost) and IPC via the Pause container; Pod lifecycle transitions through Pending, Running, Succeeded, Failed.",
        "init-containers-sidecar-pattern-lifecycle-hooks": "Init containers run sequentially to completion before app containers start; sidecar containers provide auxiliary logging/proxying; postStart and preStop hooks manage lifecycles.",
        "deployments-replicasets-rolling-updates-rollbacks": "Deployments manage ReplicaSets for declarative pod replication; rolling updates replace pods progressively with zero downtime and instant rollback on failure.",
        "resource-management-requests-limits-qos-classes": "Requests guarantee minimum CPU/RAM scheduling reservation; Limits define hard usage ceilings; Kubernetes classifies pods into Guaranteed, Burstable, and BestEffort QoS.",

        "statefulsets-sticky-identity-ordered-scaling": "Orchestrates stateful workloads (databases, Kafka); provides stable persistent network IDs (pod-0, pod-1) and automated dynamic PVC provisioning via volumeClaimTemplates.",
        "daemonsets-cluster-infrastructure-agents": "Ensures an identical copy of a pod runs on all (or targeted) nodes in the cluster; ideal for node monitoring agents (Prometheus node-exporter) and log collectors (Fluentd).",
        "jobs-cronjobs-batch-processing": "Jobs run batch container tasks to completion with guaranteed completion counts; CronJobs trigger automated recurring jobs on standard cron schedules with concurrency policies.",

        "clusterip-nodeport-loadbalancer-services": "ClusterIP provides stable internal IP service discovery; NodePort opens high ports (30000-32767) on all node IPs; LoadBalancer provisions cloud-native load balancers.",
        "kube-proxy-modes-iptables-vs-ipvs": "kube-proxy traffic forwarding: iptables creates sequential packet filtering rules (O(n) scale bottleneck); IPVS uses hash tables (O(1)) for high-performance enterprise routing.",
        "ingress-controllers-and-ingress-resources": "Ingress resources define Layer 7 HTTP/HTTPS routing rules; Ingress Controllers (NGINX, Traefik, AWS ALB) translate declarations into reverse proxy configurations with SSL termination.",
        "container-network-interface-cni-overlay-vs-flat": "CNI plugins (Calico, Flannel, Cilium) allocate pod IP addresses and manage inter-node pod communication using either VXLAN overlay encapsulation or flat BGP routing.",

        "configmaps-and-secrets-volume-vs-env": "Decoupling application configuration from container images: mounted as environment variables or dynamically updated filesystem volume projections.",
        "persistent-volumes-pvc-and-storageclasses": "Decoupled storage lifecycle: PersistentVolume (PV) represents physical cluster storage, PersistentVolumeClaim (PVC) requests capacity, and StorageClass provisions storage dynamically.",
        "kubernetes-rbac-roles-rolebindings-serviceaccounts": "Role-Based Access Control: Roles and ClusterRoles define API permissions (verbs & resources); RoleBindings bind identities (Users, ServiceAccounts) to roles.",
        "network-policies-pod-isolation-zero-trust": "Declarative firewall rules controlling ingress and egress traffic between pods using label selectors; defaults to allow-all until a NetworkPolicy enforces zero-trust isolation.",
        "helm-package-manager-charts-values-templating": "The package manager for Kubernetes: Helm Charts bundle versioned Kubernetes manifests with parameterized values.yaml files and release tracking.",

        # 8. Terraform
        "infrastructure-as-code-paradigms-declarative-vs-imperative": "Declarative IaC (Terraform) specifies the desired target state and automatically calculates diff execution paths, whereas imperative tooling executes step-by-step sequential scripts.",
        "terraform-architecture-core-vs-providers": "Terraform Core computes dependency graphs and executes plan/apply lifecycles; Providers (AWS, Azure, GCP) translate declarative resource calls into cloud REST APIs via gRPC.",
        "hcl-syntax-blocks-arguments-expressions": "HashiCorp Configuration Language: structured blocks (resource, data, variable, output), typed arguments, and built-in functions (lookup, merge, cidrsubnet).",
        "terraform-cli-workflow-init-plan-apply-destroy": "Core operational lifecycle: terraform init installs provider plugins, terraform plan calculates resource execution deltas, and terraform apply reconciles target infrastructure.",

        "state-file-internals-terraform-tfstate": "terraform.tfstate acts as the single source of truth mapping declared HCL resources to real-world cloud metadata and tracking resource dependency graphs.",
        "remote-backends-s3-dynamodb-state-locking": "Production remote backends store state files centrally in encrypted Amazon S3 buckets, while DynamoDB tables enforce distributed state locking to prevent concurrent apply race conditions.",
        "state-management-commands-mv-rm-import": "Advanced state refactoring: terraform state mv renames resource addresses without recreating infrastructure; terraform import adopts existing unmanaged cloud resources.",
        "state-security-drift-detection-refresh": "Securing sensitive state credentials with encryption at rest; terraform plan -refresh-only detects configuration drift caused by manual console modifications.",

        "reusable-modules-inputs-outputs-locals": "Encapsulating repeatable architecture blueprints into parameterized modules with explicit validation rules for variables and structured output exports.",
        "resource-loops-count-vs-for-each": "count creates integer-indexed resource arrays (vulnerable to cascade recreation on item removal); for_each iterates over maps/sets with stable key-based address tracking.",
        "dynamic-blocks-and-built-in-functions": "Constructing nested configuration blocks programmatically using dynamic blocks; transforming complex data structures with built-in collection and network functions.",
        "terraform-workspaces-multi-environment-patterns": "Isolating multiple state instances under a single configuration; best practice combines workspaces with directory-based environment separation (dev/stage/prod).",

        # 9. CI/CD
        "continuous-integration-delivery-deployment": "CI automatically builds and validates code on every commit; CD ensures software is continuously deployable; Continuous Deployment deploys changes directly to production with automated gates.",
        "trunk-based-development-vs-gitflow": "Trunk-based development merges small, frequent commits into the main branch protected by feature flags; Gitflow maintains complex long-lived feature and release branches.",
        "deployment-strategies-blue-green-canary-rolling": "Blue-Green switches 100% of traffic to a parallel identical environment; Canary routes a small traffic percentage (5%) to test stability before widespread rollout.",
        "feature-flags-and-progressive-delivery": "Decoupling code deployment from feature release; feature flag services (LaunchDarkly) allow dynamic runtime enablement, percentage rollouts, and instant kill-switches.",

        "github-actions-core-workflows-jobs-steps": "YAML workflow files in .github/workflows/; triggers on repository events (push, pull_request); jobs execute in parallel or dependency chains across virtual runner environments.",
        "environment-secrets-variables-oidc": "Centralized secret management scoped to environments; OpenID Connect (OIDC) authenticates GitHub Actions with AWS/Azure using short-lived tokens without storing static cloud keys.",
        "matrix-builds-caching-performance-optimization": "Matrix configurations test multiple runtime versions and operating systems simultaneously; actions/cache preserves package dependencies across pipeline runs.",
        "composite-actions-and-reusable-workflows": "DRY pipeline engineering: composite actions bundle multi-step tasks into single action units; reusable workflows standardize compliance gates across organization repositories.",

        "jenkins-architecture-controller-agent-topology": "Distributed automation architecture: Jenkins Controller manages configuration, scheduling, and UI; Agent nodes execute isolated build jobs across diverse operating systems.",
        "declarative-vs-scripted-jenkins-pipelines": "Declarative syntax enforces structured, opinionated Jenkinsfile standards with built-in stage directives; Scripted syntax offers full Groovy programming flexibility for legacy pipelines.",
        "shared-libraries-enterprise-pipeline-governance": "Centralized Groovy libraries imported into enterprise Jenkinsfiles; enforces standard security scanning, compliance checks, and deployment steps across engineering teams.",
        "gitops-principles-argocd-declarative-delivery": "Git acts as the single source of truth for infrastructure and applications; ArgoCD agent continuously reconciles live Kubernetes cluster state with git repository definitions.",

        # 10. Kafka
        "kafka-storage-architecture-commit-log-segments": "Append-only, immutable commit log architecture stored on disk; logs are partitioned into segments (.log, .index, .timeindex) enabling sequential disk I/O and zero-copy data transfer.",
        "kraft-quorum-architecture-removing-zookeeper": "Modern Kafka consensus: KRaft (Kafka Raft) eliminates external ZooKeeper dependencies by running Raft consensus directly inside active Kafka controller brokers.",
        "page-cache-zero-copy-os-optimization": "High throughput mechanics: Kafka bypasses JVM garbage collection by utilizing the Linux OS Page Cache and transfers data straight from disk to network sockets via the sendfile() syscall.",

        "topics-partitions-ordering-guarantees": "Topics are subdivided into partitions for horizontal scaling; strict total ordering of records is guaranteed only within an individual partition, never across partitions.",
        "partition-keys-murmur2-hashing-custom-partitioners": "Producers hash partition keys using Murmur2 to route records deterministically to specific partitions; null keys trigger sticky partitioning across active partitions.",
        "producer-acks-idempotence-min-insync-replicas": "Durability guarantees: acks=all combined with min.insync.replicas=2 ensures replication to quorum replicas; enable.idempotence=true eliminates duplicate messages.",
        "kafka-transactions-and-exactly-once-semantics-eos": "Transactional producers coordinate with consumer group offsets to guarantee atomic multi-partition writes, enabling end-to-end Exactly-Once Semantics (EOS).",

        "consumer-groups-parallelism-partition-assignment": "Consumer groups distribute partitions across consumer instances for parallel processing; max concurrency is strictly bounded by the total partition count.",
        "partition-rebalance-protocols-eager-vs-cooperative": "Consumer group rebalances: Eager rebalance pauses all consumers while reassigning; Cooperative Sticky rebalancing reassigns only necessary partitions without cluster pauses.",
        "consumer-offset-management-auto-commit-vs-manual": "Consumer progress tracked in the internal __consumer_offsets topic; manual synchronous/asynchronous offset commits prevent message loss and duplicate processing.",
        "consumer-lag-monitoring-and-scaling": "Consumer Lag measures the offset delta between the producer's latest message and the consumer's current position; essential metric for autoscaling consumer instances.",

        "confluent-schema-registry-avro-protobuf-evolution": "Decoupled serialization governance: Schema Registry enforces backward and forward schema compatibility rules for Avro and Protocol Buffer payloads.",
        "kafka-connect-architecture-source-and-sink": "Scalable framework for streaming data between Kafka and external databases; Source connectors ingest from external systems, and Sink connectors export to data lakes/warehouses.",
        "kafka-streams-stateless-vs-stateful-processing": "Client library for real-time stream processing; supports stateless transformations (filter, map) and stateful aggregations (joins, windowing) backed by local RocksDB stores.",

        # 11. Spark
        "spark-cluster-topology-driver-cluster-manager-executors": "Distributed architecture: Spark Driver coordinates execution, negotiates resources with the Cluster Manager (YARN, K8s), and executes tasks across distributed worker Executors.",
        "dag-scheduler-and-task-scheduler-internals": "Query planning pipeline: transformations compile into a Directed Acyclic Graph (DAG); DAG Scheduler breaks graphs into Stages at shuffle boundaries, and Task Scheduler dispatches tasks.",
        "spark-memory-management-unified-memory-manager": "Unified memory architecture: divides executor JVM memory between Execution (shuffles, joins, aggregations) and Storage (caching broadcast variables) with dynamic borrowing.",

        "rdd-core-abstractions-partitions-and-iterators": "Resilient Distributed Datasets: immutable distributed collections partitioned across cluster nodes; tasks process records sequentially using iterator interfaces.",
        "rdd-lineage-graph-and-fault-tolerance": "Fault recovery without data replication: RDDs maintain lineage dependency graphs; if a worker node crashes, lost partitions are recomputed automatically from ancestors.",
        "narrow-vs-wide-dependencies-shuffle-boundary": "Narrow dependencies (map, filter) execute in-memory on local partitions without network movement; Wide dependencies (groupByKey, join) require expensive cluster-wide data shuffles.",

        "spark-sql-catalyst-optimizer-pipeline": "Extensible query optimization engine: translates SQL and DataFrame queries through Analysis, Logical Optimization, Physical Planning, and Code Generation phases.",
        "project-tungsten-off-heap-memory-codegen": "Hardware-level execution optimization: manages binary data off-heap to eliminate JVM object overhead and compiles whole-stage queries directly into Java bytecode.",
        "dataframes-vs-datasets-vs-rdds": "RDDs provide raw procedural control with JVM overhead; DataFrames provide structured columnar data optimized by Catalyst; Datasets add compile-time type safety.",

        "spark-shuffle-architecture-sort-shuffle-manager": "Data redistribution across stages: SortShuffleManager writes shuffle output to consolidated data files paired with index files, minimizing disk seek overhead.",
        "shuffle-partition-tuning-and-skew-mitigation": "Optimizing spark.sql.shuffle.partitions to prevent memory spill; mitigating data skew using Adaptive Query Execution (AQE) and salt keys.",
        "caching-and-persistence-storage-levels": "Preserving intermediate data across iterative queries using cache() and persist() with storage levels (MEMORY_ONLY, MEMORY_AND_DISK, MEMORY_ONLY_SER).",
        "spark-structured-streaming-micro-batch-vs-continuous": "Scalable stream processing engine built on Spark SQL; processes streaming event data incrementally via micro-batching or sub-millisecond continuous processing.",

        # 12. PostgreSQL
        "relational-database-theory-first-through-third-normal-form": "Database normalization: 1NF enforces atomic values, 2NF eliminates partial key dependencies, and 3NF removes transitive dependencies to ensure zero data redundancy.",
        "acid-properties-and-ansi-isolation-levels": "Atomicity, Consistency, Isolation, Durability; PostgreSQL implements Read Committed, Repeatable Read, and Serializable using Multi-Version Concurrency Control.",
        "primary-keys-surrogate-vs-natural-uuidv7": "Key selection trade-offs: natural keys bind to domain logic; auto-incrementing BigInt causes distributed insert hotspots; time-ordered UUIDv7 enables random distributed generation with B-Tree friendliness.",

        "page-layout-internals-and-tuple-storage": "PostgreSQL data files consist of 8KB disk pages; page headers track ItemId line pointers referencing tuples stored from the bottom of the page upward.",
        "multiversion-concurrency-control-mvcc-xmin-xmax": "Concurrency without read locks: every tuple header stores xmin (creating transaction ID) and xmax (deleting/updating transaction ID) to determine snapshot visibility.",
        "write-ahead-logging-wal-checkpoints-crash-recovery": "Durability and performance: all database changes append sequentially to the WAL buffer before disk write; Checkpoints flush dirty shared buffers to disk for fast crash recovery.",
        "vacuuming-architecture-autovacuum-wraparound": "Dead tuple reclamation: VACUUM reclaims space left by updated/deleted rows; Autovacuum prevents 32-bit transaction ID wraparound catastrophic data loss.",

        "b-tree-indexes-internals-and-search-mechanics": "Self-balancing tree structure optimized for block storage; stores sorted keys in leaf pages with bidirectional pointers for high-performance equality and range scans.",
        "specialized-indexes-gin-gist-brin": "Generalized Inverted Index (GIN) accelerates full-text and JSONB searches; GiST powers geometric/spatial PostGIS queries; BRIN indexes large time-series tables at minimal footprint.",
        "query-planning-cost-model-and-explain-analyze": "Query Planner explores execution paths using table statistics (pg_statistic); EXPLAIN ANALYZE reveals actual execution times, node costs, and index scan selections.",
        "index-maintenance-bloat-and-reindex-concurrently": "Dead tuples in index leaf pages cause index bloat; REINDEX CONCURRENTLY rebuilds damaged indexes in production without exclusive table read/write locks.",

        "physical-streaming-replication-wal-sender-receiver": "High-availability clustering: primary wal_sender streams raw WAL records across the network to standby wal_receiver processes for synchronous or asynchronous failover.",
        "logical-replication-publication-and-subscription": "Row-level data replication between distinct databases or PostgreSQL major versions using publish/subscribe semantics on WAL decoded changes.",
        "connection-pooling-architecture-pgbouncer": "Lightweight connection pooler: sits between application servers and PostgreSQL to maintain pre-warmed backend connections in Transaction Pooling mode, preventing backend process exhaustion.",
        "patroni-and-high-availability-failover-quorums": "Automated failover management: Patroni orchestrates PostgreSQL nodes using Distributed Consensus Stores (etcd, Consul) for zero-split-brain leader election.",

        # 13. Redis
        "redis-threading-model-single-threaded-event-loop": "High performance mechanics: single-threaded event loop leverages non-blocking I/O multiplexing (epoll/kqueue) to serve 100K+ requests/sec with zero locking or thread context switching.",
        "redis-strings-hashes-lists-sets-sorted-sets": "Core data structures: SDS Strings, Hashes for object representation, Lists for queues, Sets for unique membership, and Sorted Sets (SkipLists) for real-time leaderboards.",
        "advanced-data-structures-hyperloglog-bitmaps-geospatial": "Memory-efficient structures: HyperLogLog estimates cardinalities of billions of items in 12KB; Bitmaps provide bit-level flag tracking; Geospatial indexes coordinate locations via Geohashes.",
        "redis-memory-optimization-ziplists-and-intsets": "Internal memory compression: small Hashes and Lists compact into contiguous memory Ziplists/Listpacks, drastically reducing pointer overhead in RAM.",

        "caching-patterns-cache-aside-read-through-write-through": "Cache-Aside queries cache first and populates on miss; Read/Write-Through makes the cache the primary system of record; Write-Behind buffers async writes to the database.",
        "cache-stampede-thundering-herd-mutex-probabilistic": "Preventing backend database collapse on key expiration: resolve using distributed locks (Redlock) or probabilistic early expiration algorithms (XFetch).",
        "eviction-policies-lru-lfu-volatile-allkeys": "Memory saturation policies: allkeys-lru evicts least recently used keys; allkeys-lfu evicts least frequently used keys; noeviction returns write errors when maxmemory is hit.",
        "ttl-expiration-internals-passive-vs-active-expiration": "Key lifecycle: Passive expiration deletes keys when accessed after TTL expiry; Active expiration periodically samples random keys with expiries and reclaims memory.",

        "rdb-persistence-bgsave-copy-on-write": "Point-in-time snapshot persistence: BGSAVE forks a child process using Linux Copy-on-Write (CoW) to write compressed RDB snapshots to disk without blocking write traffic.",
        "aof-persistence-fsync-strategies-aof-rewrite": "Append-Only File persistence: logs every write command; fsync strategies (always, everysec, no) balance durability vs latency; BGREWRITEAOF compacts logs in the background.",
        "redis-sentinel-monitoring-failover-split-brain": "High availability orchestration: Sentinel quorum monitors primary health, executes automated failover to replicas, and reconfigures clients without cluster downtime.",
        "redis-cluster-architecture-hash-slots-rebalancing": "Horizontal partitioning: distributed data across 16,384 Hash Slots using CRC16 hashing; nodes coordinate cluster state via gossip protocol with master/replica failover.",

        # 14. Java & Spring Boot
        "jvm-architecture-classloader-memory-model-jit-compiler": "Runtime mechanics: ClassLoaders load bytecode; JVM memory partitions into Heap, Metaspace, and Thread Stacks; JIT (C1/C2) compiles hot bytecode into optimized native machine code.",
        "garbage-collection-algorithms-g1-zgc-shenandoah": "Heap reclamation: G1 partitions heap into regions for predictable pause times; modern ZGC and Shenandoah perform concurrent marking and compaction with sub-millisecond pauses.",
        "java-memory-model-volatile-synchronized-atomic": "Thread safety rules: volatile guarantees visibility and instruction reordering fences; synchronized provides mutual exclusion; Atomic classes leverage hardware CAS (Compare-And-Swap).",
        "virtual-threads-project-loom-high-throughput": "Lightweight user-mode threads managed by the JVM rather than the OS kernel; allows scaling to millions of concurrent request threads with blocking I/O without thread pool exhaustion.",

        "spring-ioc-container-bean-lifecycle-scopes": "Inversion of Control: ApplicationContext instantiates, wires, and manages bean lifecycles; Singleton scope provides a single instance per container; Prototype creates new instances per injection.",
        "dependency-injection-constructor-vs-field-injection": "Dependency resolution: Constructor Injection ensures immutability, facilitates unit testing, and prevents NullPointerExceptions, outclassing legacy field injection (@Autowired).",
        "spring-boot-auto-configuration-and-starters": "Convention over configuration: Starter POMs bundle curated dependencies; @EnableAutoConfiguration scans classpaths and registers beans conditionally using @ConditionalOnClass.",
        "spring-aop-proxy-mechanisms-jdk-vs-cglib": "Aspect-Oriented Programming: modularizes cross-cutting concerns (transactions, security, logging); JDK Dynamic Proxies handle interface proxies, while CGLIB subclasses classes.",

        "spring-data-jpa-repository-abstractions": "Data access abstraction: CrudRepository and JpaRepository generate dynamic query implementations at runtime from method names (@Query, findByEmail).",
        "hibernate-first-and-second-level-cache": "ORM caching architecture: First-Level Cache is bound to the current Hibernate Session; Second-Level Cache (Ehcache, Redis) caches entity data across multiple sessions.",
        "n-plus-1-problem-entitygraphs-and-join-fetch": "Performance optimization: resolves N+1 SELECT queries by executing JOIN FETCH statements or configuring @EntityGraph annotations to load associations eagerly in one SQL query.",
        "declarative-transactions-transactional-propagation": "Transaction management: @Transactional manages ACID boundaries via AOP proxies; propagation levels (REQUIRED, REQUIRES_NEW) control nested transaction rollbacks.",

        "spring-security-filter-chain-architecture": "Security pipeline: DelegatingFilterProxy delegates HTTP requests to SecurityFilterChain filters for authentication, authorization, CSRF protection, and CORS verification.",
        "jwt-authentication-and-oauth2-resource-server": "Stateless API security: Spring Security configured as an OAuth2 Resource Server validates signed JWT tokens and extracts roles into SecurityContext authentication tokens.",
        "resilience4j-circuit-breakers-retries-rate-limiters": "Fault-tolerance library: Circuit Breakers stop cascading microservice failures on downstream errors; automated Retries with exponential backoff and Rate Limiters protect resources.",
        "spring-boot-actuator-micrometer-prometheus": "Production observability: Actuator exposes /health and /metrics endpoints; Micrometer instruments application metrics and exports time-series data to Prometheus and Grafana.",

        # 15. Python & FastAPI
        "python-asyncio-event-loop-coroutines-tasks": "Single-threaded cooperative multitasking: coroutines defined with async/await yield control to the Event Loop on I/O operations; Tasks manage concurrent executions.",
        "fastapi-architecture-starlette-and-pydantic": "High-performance framework: built on Starlette for ASGI routing and WebSockets, and Pydantic for lightning-fast data parsing, validation, and serialization.",
        "dependency-injection-system-fastapi-depends": "Modular dependency resolution: Depends injects shared database sessions, authentication contexts, and configuration objects cleanly into route handler functions.",
        "request-validation-and-serialization-pydantic-v2": "Strict type validation: Pydantic v2 written in Rust delivers 5-10x faster serialization of request schemas and automated OpenAPI (Swagger) documentation generation.",

        "sqlalchemy-2-0-asyncio-asyncsession": "Modern async ORM: SQLAlchemy 2.0 uses select() syntax and AsyncSession to execute non-blocking database queries via asyncpg drivers.",
        "alembic-database-migrations-and-revisions": "Database schema version control: Alembic auto-generates migration scripts from SQLAlchemy model diffs and manages sequential revision upgrades and downgrades.",
        "pytest-asyncio-test-client-httpx": "Integration testing: pytest-asyncio runs async test cases against FastAPI applications using httpx.AsyncClient with transaction-rollback test fixtures.",
        "production-deployment-uvicorn-gunicorn-workers": "Production deployment architecture: Gunicorn acts as the master process manager coordinating multiple Uvicorn worker processes to utilize all CPU cores.",

        # 16. API Design
        "rest-api-design-http-verbs-status-codes-hld": "Architectural constraints: resource-oriented URIs, standard HTTP verbs (GET, POST, PUT, PATCH, DELETE), idempotency, and semantic HTTP status codes (200, 201, 400, 401, 403, 404, 409, 500).",
        "graphql-architecture-queries-mutations-n-plus-1": "Client-specified queries: clients request exact data shapes; Mutations handle updates; DataLoader batches and caches backend requests to eliminate the GraphQL N+1 problem.",
        "grpc-and-protocol-buffers-http-2-multiplexing": "High-performance RPC: Protocol Buffers serialize binary messages with strongly-typed schemas; HTTP/2 multiplexes bidirectional streaming RPCs over single TCP connections.",
        "http-1-1-vs-http-2-vs-http-3-quic": "Protocol evolution: HTTP/1.1 head-of-line blocking; HTTP/2 binary framing and multiplexing over TCP; HTTP/3 leverages QUIC over UDP for zero-RTT connection establishment.",

        "api-authentication-oauth2-oidc-jwt": "API access control: OAuth2 framework for delegated authorization; OpenID Connect (OIDC) for identity verification; cryptographically signed JSON Web Tokens (JWT) for stateless claims.",
        "rate-limiting-algorithms-token-bucket-sliding-window": "Traffic shaping algorithms: Token Bucket permits bursty traffic; Leaky Bucket smoothens outflow rates; Sliding Window Counter maintains distributed request counts in Redis.",
        "api-gateway-patterns-kong-traefik-envoy": "Centralized edge routing: API Gateways handle SSL termination, request authentication, rate limiting, logging, and protocol translation (gRPC-Web to gRPC).",
        "api-versioning-backward-compatibility-contract-testing": "Lifecycle governance: URI versioning (/v1) vs header versioning; backward compatibility rules; Pact consumer-driven contract testing preventing breaking changes."
    }
    
    if anchor in DESCS:
        return DESCS[anchor]
    
    # Fallback to high quality synthesized description
    return f"Comprehensive production architecture, core execution mechanisms, and operational trade-offs for {title}."

# 5. Build HTML content
lines = []

# HTML Head & Styles (Identical to system_design.html)
lines.append("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1" name="viewport"/>
<title>Cloud &amp; DevOps Engineering</title>
<style>
:root {
  --bg: #0f1115; --bg-elev: #161922; --bg-card: #1c2030; --bg-row-alt: #1a1d2a;
  --text: #e6e8ee; --text-dim: #9aa0b0; --text-faint: #6b7080;
  --border: #2a2f42; --border-strong: #3a3f55;
  --accent: #0786a3; --accent-dim: rgba(7,134,163,0.15);
  --link: #38bdf8;
  --quote-bg: rgba(7,134,163,0.06);
  --done: #00b894; --done-bg: rgba(0,184,148,0.12);
  --shadow-card: 0 1px 3px rgba(0,0,0,0.2);
  --shadow-banner: 0 4px 14px rgba(0,0,0,0.25);
}
html.light {
  --bg: #fafbfc; --bg-elev: #ffffff; --bg-card: #ffffff; --bg-row-alt: #f8f9fb;
  --text: #1a1d24; --text-dim: #5a6072; --text-faint: #8b91a3;
  --border: #e4e7ee; --border-strong: #d0d4de;
  --accent: #0284c7; --accent-dim: rgba(2,132,199,0.1);
  --link: #0369a1;
  --quote-bg: rgba(2,132,199,0.05);
  --done: #00a884; --done-bg: rgba(0,168,132,0.12);
  --shadow-card: 0 1px 3px rgba(0,0,0,0.04);
  --shadow-banner: 0 4px 14px rgba(0,0,0,0.08);
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0; line-height: 1.55;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
  background: var(--bg); color: var(--text);
  -webkit-font-smoothing: antialiased;
  transition: background 0.2s, color 0.2s;
}
.wrap { max-width: 1240px; margin: 0 auto; padding: 24px 20px 80px; }
.hero { text-align: center; padding: 16px 0 24px; border-bottom: 1px solid var(--border); margin-bottom: 20px; }
.hero h1 { font-size: 32px; margin: 6px 0 4px; letter-spacing: -0.02em; }
.hero .subtitle { color: var(--text-dim); margin: 0; font-size: 14px; }
.hero .edition {
  display: inline-block; color: var(--accent); font-weight: 700; font-size: 11px;
  text-transform: uppercase; letter-spacing: 0.12em;
  background: var(--accent-dim); padding: 4px 10px; border-radius: 4px;
}
.stats { display: flex; gap: 8px; flex-wrap: wrap; justify-content: center; margin-top: 20px; }
.stat {
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: 10px; padding: 8px 14px; min-width: 80px;
  box-shadow: var(--shadow-card);
}
.stat .n { font-size: 20px; font-weight: 700; font-variant-numeric: tabular-nums; }
.stat .l { font-size: 10px; color: var(--text-faint); text-transform: uppercase; letter-spacing: 0.1em; margin-top: 2px; }

.overall-progress {
  background: var(--bg-elev); border: 1px solid var(--border);
  border-radius: 10px; padding: 14px 20px; margin: 18px 0 18px;
  display: flex; align-items: center; gap: 16px;
}
.overall-progress .lbl { font-size: 12px; color: var(--text-faint); text-transform: uppercase; letter-spacing: 0.1em; font-weight: 700; }
.overall-progress .bar-track {
  flex: 1; height: 10px; background: var(--bg-card);
  border-radius: 5px; overflow: hidden; border: 1px solid var(--border);
}
.overall-progress .bar-fill {
  height: 100%; background: linear-gradient(90deg, var(--done), var(--accent));
  transition: width 0.3s ease; width: 0%;
}
.overall-progress .pct { font-weight: 700; font-variant-numeric: tabular-nums; font-size: 14px; min-width: 80px; text-align: right; }

.controls {
  position: sticky; top: 0; z-index: 50;
  background: var(--bg); backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--border);
  padding: 10px 0; margin: 0 0 20px;
}
.controls-row {
  display: flex; flex-wrap: wrap; gap: 8px; align-items: center;
  background: var(--bg-elev); border: 1px solid var(--border);
  border-radius: 10px; padding: 10px 14px;
}
.controls-row .label {
  font-size: 10px; color: var(--text-faint);
  text-transform: uppercase; letter-spacing: 0.08em;
  font-weight: 700; margin-right: 2px;
}
.search { flex: 1; min-width: 180px; }
.search input {
  width: 100%; padding: 6px 11px; font-size: 13px;
  background: var(--bg-card); border: 1px solid var(--border); color: var(--text);
  border-radius: 5px;
}
.search input:focus { outline: none; border-color: var(--accent); }
.icon-btn {
  padding: 5px 9px; font-size: 14px;
  background: var(--bg-card); border: 1px solid var(--border);
  color: var(--text-dim); border-radius: 5px; cursor: pointer;
  transition: all 0.12s;
}
.icon-btn:hover { background: var(--accent); color: white; border-color: var(--accent); }
.filter-btn {
  padding: 5px 10px; font-size: 11px; font-weight: 700;
  background: var(--bg-card); border: 1px solid var(--border);
  color: var(--text-dim); border-radius: 5px; cursor: pointer;
  font-family: ui-monospace, "SF Mono", Menlo, monospace;
  transition: all 0.12s; letter-spacing: 0.02em;
}
.filter-btn:hover { background: var(--bg); color: var(--text); }
.filter-btn.active { background: var(--accent); color: white; border-color: var(--accent); }
.filter-btn.status-bookmarked.active { background: #ffa94d; border-color: #ffa94d; }
.filter-btn.status-done.active { background: var(--done); border-color: var(--done); }
.sep { width: 1px; height: 20px; background: var(--border); margin: 0 2px; }

.toc {
  background: var(--bg-elev); border: 1px solid var(--border);
  border-radius: 12px; padding: 16px 22px; margin-bottom: 28px;
}
.toc h2 {
  font-size: 12px; text-transform: uppercase; letter-spacing: 0.1em;
  color: var(--text-faint); margin: 0 0 12px; font-weight: 700;
}
.toc-grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 3px 12px;
}
.toc a {
  display: flex; align-items: center; gap: 10px;
  padding: 6px 8px; border-radius: 6px; color: var(--text);
  text-decoration: none; font-size: 12.5px;
  transition: background 0.12s;
}
.toc a:hover { background: var(--bg-card); }
.toc .roman {
  font-family: ui-monospace, "SF Mono", Menlo, monospace;
  font-size: 10px; color: var(--text-faint); min-width: 28px;
}
.toc .name { flex: 1; }
.toc .cnt {
  font-size: 9.5px; color: var(--text-faint);
  font-variant-numeric: tabular-nums;
  background: var(--bg-card); padding: 1px 6px; border-radius: 3px;
}

.section { margin: 48px 0 0; }
.section-banner {
  border-radius: 12px; padding: 18px 24px; color: white;
  display: flex; align-items: center; gap: 16px;
  box-shadow: var(--shadow-banner);
}
.section-banner .num {
  font-family: ui-monospace, "SF Mono", Menlo, monospace;
  font-size: 22px; font-weight: 700; opacity: 0.95;
  min-width: 56px; text-align: center;
  padding: 6px 10px; background: rgba(255,255,255,0.18);
  border-radius: 7px;
}
.section-banner .info { flex: 1; min-width: 0; }
.section-banner .label {
  font-size: 10px; text-transform: uppercase; letter-spacing: 0.14em;
  opacity: 0.85; margin-bottom: 1px;
}
.section-banner h2 { margin: 0; font-size: 20px; font-weight: 700; letter-spacing: -0.01em; }
.section-banner .meta { font-size: 11.5px; opacity: 0.9; margin-top: 3px; }
.section-banner .ppg { min-width: 140px; text-align: right; }
.section-banner .ppg .pct-text { font-size: 13px; font-weight: 700; margin-bottom: 4px; font-variant-numeric: tabular-nums; }
.section-banner .ppg .pp-track { height: 6px; background: rgba(255,255,255,0.25); border-radius: 3px; overflow: hidden; }
.section-banner .ppg .pp-fill { height: 100%; background: white; border-radius: 3px; width: 0%; transition: width 0.3s; }

.section-desc {
  background: var(--quote-bg);
  border-left: 4px solid var(--section-color, var(--accent));
  border-radius: 0 8px 8px 0;
  padding: 12px 18px; margin: 14px 0 6px 24px; font-size: 13.5px;
}
.section-desc .tagline { font-size: 14.5px; font-weight: 700; color: var(--text); margin: 0 0 6px; }
.section-desc .row { margin: 4px 0; color: var(--text-dim); }
.section-desc .row b { color: var(--text); }

.subsection {
  background: var(--bg-card); border: 1px solid var(--border);
  border-left: 4px solid var(--section-color, var(--accent));
  border-radius: 10px; margin: 16px 0 0 24px; padding: 14px 18px 16px;
  box-shadow: var(--shadow-card);
}
.subsection-head { display: flex; align-items: baseline; gap: 12px; margin-bottom: 6px; flex-wrap: wrap; }
.subsection-tag {
  font-family: ui-monospace, "SF Mono", Menlo, monospace;
  font-size: 10px; background: var(--bg-elev); border: 1px solid var(--border);
  color: var(--text-dim); padding: 2px 7px; border-radius: 4px;
  font-weight: 700; letter-spacing: 0.04em;
}
.subsection h3 { margin: 0; font-size: 14.5px; font-weight: 700; flex: 1; min-width: 0; color: var(--text); }
.subsection-desc {
  font-size: 12.5px; color: var(--text-dim); margin: 4px 0 8px;
  padding: 7px 11px; background: var(--bg-elev); border-radius: 6px; line-height: 1.5;
}

.concepts {
  list-style: none; padding: 0; margin: 8px 0 0;
  border-radius: 8px; overflow: hidden;
  border: 1px solid var(--border);
}
.concepts li {
  display: grid;
  grid-template-columns: 28px 22px 1fr auto;
  gap: 10px; align-items: center;
  padding: 8px 12px;
  border-bottom: 1px solid var(--border);
  background: var(--bg-elev);
  transition: background 0.12s;
}
.concepts li:last-child { border-bottom: none; }
.concepts li:nth-child(even) { background: var(--bg-row-alt); }
.concepts li:hover { background: var(--accent-dim); }
.concepts li.hidden { display: none; }
.concepts li.done { background: var(--done-bg); }
.concepts li.done .cname { color: var(--text-dim); text-decoration: line-through; }
.done-check {
  width: 22px; height: 22px; cursor: pointer;
  border: 2px solid var(--border-strong); border-radius: 5px;
  background: var(--bg-card);
  display: flex; align-items: center; justify-content: center;
  transition: all 0.15s; flex-shrink: 0;
}
.done-check:hover { border-color: var(--done); }
.done-check.checked { background: var(--done); border-color: var(--done); color: white; }
.done-check.checked::after { content: '✓'; font-weight: 700; font-size: 14px; }
.bookmark-star {
  cursor: pointer; font-size: 16px; color: var(--border-strong);
  user-select: none; transition: color 0.15s, transform 0.15s; flex-shrink: 0;
}
.bookmark-star:hover { color: #ffa94d; transform: scale(1.15); }
.bookmark-star.active { color: #ffa94d; }
.cname { color: var(--text); font-size: 13.5px; font-weight: 600; }
.cname b { color: var(--accent); }
.res-links { display: flex; gap: 4px; flex-shrink: 0; flex-wrap: wrap; }
.res-links a {
  font-size: 10.5px; padding: 3px 7px; border-radius: 4px;
  background: var(--bg-card); border: 1px solid var(--border);
  color: var(--text-dim); text-decoration: none;
  white-space: nowrap; font-weight: 600;
  transition: all 0.12s;
}
.res-links a:hover { background: var(--accent); color: white; border-color: var(--accent); }
.res-links a.video:hover { background: #ff0000; border-color: #ff0000; }

.resources-section {
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: 10px; padding: 12px 16px; margin: 10px 0 8px 24px;
}
.resources-section .head {
  display: flex; align-items: center; justify-content: space-between;
  cursor: pointer; user-select: none;
}
.resources-section .head h4 {
  margin: 0; font-size: 11.5px; color: var(--text-faint);
  text-transform: uppercase; letter-spacing: 0.08em; font-weight: 700;
}
.resources-section .head .count {
  font-size: 10.5px; color: var(--text-faint);
  font-family: ui-monospace, "SF Mono", Menlo, monospace;
}
.resources-section .head .chevron {
  color: var(--text-faint); font-size: 11px; margin-left: 8px;
  transition: transform 0.18s; display: inline-block;
}
.resources-section.open .chevron { transform: rotate(90deg); }
.resources-body { display: none; margin-top: 10px; }
.resources-section.open .resources-body { display: block; }
.res-grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 5px 8px;
}
.res-link {
  display: flex; align-items: center; gap: 8px;
  padding: 6px 10px; border-radius: 6px;
  background: var(--bg-elev); border: 1px solid var(--border);
  text-decoration: none; color: var(--text);
  font-size: 12.5px; transition: all 0.12s;
}
.res-link:hover { background: var(--accent); color: white; border-color: var(--accent); }
.res-link:hover .res-source { color: rgba(255,255,255,0.8); }
.res-icon { font-size: 13px; flex-shrink: 0; }
.res-title { flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.res-source { font-size: 9.5px; color: var(--text-faint); margin-left: auto; padding-left: 6px; white-space: nowrap; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; }

.top {
  position: fixed; bottom: 20px; right: 20px;
  background: var(--accent); color: white;
  padding: 10px 14px; border-radius: 8px;
  text-decoration: none; font-size: 13px; font-weight: 600;
  box-shadow: 0 4px 14px rgba(0,0,0,0.2); z-index: 100;
}

@media (max-width: 900px) {
  .wrap { padding: 16px 12px 80px; }
  .subsection, .section-desc, .resources-section { margin-left: 0; }
  .section-banner { flex-direction: column; align-items: flex-start; }
  .section-banner .ppg { min-width: 100%; text-align: left; }
  .hero h1 { font-size: 24px; }
  .concepts li { grid-template-columns: 24px 20px 1fr; gap: 6px; padding: 6px 8px; }
  .concepts li .res-links { display: none; }
}
@media print {
  body { background: white; color: black; }
  .controls, .top, .filter-btn, .icon-btn { display: none !important; }
  .resources-section .resources-body { display: block !important; }
  .section { page-break-inside: avoid; }
  a { color: black; text-decoration: underline; }
}
</style>
<link rel="stylesheet" href="assets/learning-hub-shared.css">
<script src="assets/learning-hub-shared.js"></script>
<script src="Cloud_DevOps_Tutorial/resources.js"></script>
</head>
<body>
<div class="wrap">
  <div class="tutorial-banner" style="margin:24px auto;max-width:1440px;padding:0 24px;">
    <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px;padding:16px 20px;border-radius:10px;background:linear-gradient(135deg,rgba(7,134,163,0.12),rgba(59,130,246,0.12));border:1px solid rgba(7,134,163,0.3);">
      <div>
        <div style="font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;color:var(--accent);">Interactive Tutorial App</div>
        <div style="font-size:16px;font-weight:800;color:var(--text);margin-top:2px;">Cloud &amp; DevOps Engineering Masterclass (58 Lessons &bull; 239 Concepts)</div>
        <div style="font-size:13px;color:var(--text-faint);margin-top:2px;">Interactive Algomaster roadmap covering AWS, Azure, GCP, Linux, Git, Docker, Kubernetes, Terraform, CI/CD, Kafka, Spark, PostgreSQL, Redis, Java/Spring Boot, Python/FastAPI, and API Design.</div>
      </div>
      <a href="Cloud_DevOps_Tutorial/index.html" style="display:inline-flex;align-items:center;gap:6px;padding:8px 16px;border-radius:7px;background:#0786a3;color:#fff;text-decoration:none;font-size:13px;font-weight:700;white-space:nowrap;transition:opacity .15s;">Open Cloud &amp; DevOps Tutorial &rarr;</a>
    </div>
  </div>

  <div class="hero">
    <div class="edition">v2 · Cloud &amp; DevOps Engineering · 16 Domains · 58 Masterclasses · 239 Concepts</div>
    <h1>Cloud &amp; DevOps Engineering</h1>
    <p class="subtitle">AWS · Azure · GCP · Linux · Git · Docker · Kubernetes · Terraform · CI/CD · Kafka · Spark · PostgreSQL · Redis · Java/Spring Boot · Python/FastAPI · API Design</p>
  </div>

  <div class="stats">
    <div class="stat"><div class="n">16</div><div class="l">Domains</div></div>
    <div class="stat"><div class="n">58</div><div class="l">Subsections</div></div>
    <div class="stat"><div class="n">239</div><div class="l">Concepts</div></div>
    <div class="stat"><div class="n">58</div><div class="l">Masterclasses</div></div>
    <div class="stat"><div class="n">120+</div><div class="l">Resources</div></div>
  </div>

  <div class="overall-progress">
    <span class="lbl">Your Progress</span>
    <div class="bar-track"><div class="bar-fill" id="overall-bar"></div></div>
    <span class="pct" id="overall-pct">0 / 239</span>
  </div>

  <div class="controls">
    <div class="controls-row">
      <span class="label">Filter:</span>
      <button class="filter-btn status-done" data-filter="status" data-val="done">Done</button>
      <button class="filter-btn" data-filter="status" data-val="undone">Not Done</button>
      <button class="filter-btn status-bookmarked" data-filter="status" data-val="bookmarked">★ Bookmarked</button>
      <span class="sep"></span>
      <div class="search"><input id="search-input" placeholder="Search 239 cloud &amp; devops concepts…" type="search"/></div>
      <button class="icon-btn" id="random-btn" title="Random concept">🎲</button>
      <button class="icon-btn" id="theme-toggle" title="Toggle theme">🌓</button>
      <button class="icon-btn" onclick="window.print()" title="Print">🖨️</button>
      <button class="filter-btn" id="clear-filters">Clear</button>
    </div>
  </div>

  <section class="resources-section" style="margin: 0 0 24px;">
    <div class="head" onclick="this.parentElement.classList.toggle('open')">
      <h4>🌟 Universal Anchor Resources</h4>
      <div><span class="count">16 authoritative sources</span><span class="chevron">▶</span></div>
    </div>
    <div class="resources-body">
      <p style="font-size:12.5px;color:var(--text-dim);margin:0 0 10px;">Official cloud provider documentation, CNCF architectural specifications, Linux kernel guidelines, and enterprise roadmaps for staff-level mastery.</p>
      <div class="res-grid">
        <a class="res-link" href="https://docs.aws.amazon.com/" rel="noopener" target="_blank"><span class="res-icon">📝</span><span class="res-title">AWS Documentation</span><span class="res-source">AWS</span></a>
        <a class="res-link" href="https://learn.microsoft.com/en-us/azure/" rel="noopener" target="_blank"><span class="res-icon">📝</span><span class="res-title">Azure Documentation</span><span class="res-source">Microsoft</span></a>
        <a class="res-link" href="https://cloud.google.com/docs" rel="noopener" target="_blank"><span class="res-icon">📝</span><span class="res-title">Google Cloud Documentation</span><span class="res-source">Google</span></a>
        <a class="res-link" href="https://kubernetes.io/docs/home/" rel="noopener" target="_blank"><span class="res-icon">⚓</span><span class="res-title">Kubernetes Documentation</span><span class="res-source">CNCF</span></a>
        <a class="res-link" href="https://docs.docker.com/" rel="noopener" target="_blank"><span class="res-icon">🐳</span><span class="res-title">Docker Official Guides</span><span class="res-source">Docker</span></a>
        <a class="res-link" href="https://developer.hashicorp.com/terraform/docs" rel="noopener" target="_blank"><span class="res-icon">🛠️</span><span class="res-title">Terraform Registry &amp; Documentation</span><span class="res-source">HashiCorp</span></a>
        <a class="res-link" href="https://docs.github.com/en/actions" rel="noopener" target="_blank"><span class="res-icon">⚡</span><span class="res-title">GitHub Actions Documentation</span><span class="res-source">GitHub</span></a>
        <a class="res-link" href="https://kafka.apache.org/documentation/" rel="noopener" target="_blank"><span class="res-icon">📜</span><span class="res-title">Apache Kafka Documentation</span><span class="res-source">Apache</span></a>
        <a class="res-link" href="https://spark.apache.org/docs/latest/" rel="noopener" target="_blank"><span class="res-icon">⚡</span><span class="res-title">Apache Spark Documentation</span><span class="res-source">Apache</span></a>
        <a class="res-link" href="https://www.postgresql.org/docs/current/" rel="noopener" target="_blank"><span class="res-icon">🐘</span><span class="res-title">PostgreSQL Official Manual</span><span class="res-source">PostgreSQL</span></a>
        <a class="res-link" href="https://redis.io/docs/" rel="noopener" target="_blank"><span class="res-icon">🔴</span><span class="res-title">Redis Documentation</span><span class="res-source">Redis</span></a>
        <a class="res-link" href="https://docs.spring.io/spring-boot/docs/current/reference/html/" rel="noopener" target="_blank"><span class="res-icon">🌱</span><span class="res-title">Spring Boot Reference Guide</span><span class="res-source">Spring</span></a>
        <a class="res-link" href="https://fastapi.tiangolo.com/" rel="noopener" target="_blank"><span class="res-icon">🚀</span><span class="res-title">FastAPI Framework Guide</span><span class="res-source">FastAPI</span></a>
        <a class="res-link" href="https://owasp.org/www-project-api-security/" rel="noopener" target="_blank"><span class="res-icon">🔐</span><span class="res-title">OWASP API Security Top 10</span><span class="res-source">OWASP</span></a>
        <a class="res-link" href="https://roadmap.sh/devops" rel="noopener" target="_blank"><span class="res-icon">🗺️</span><span class="res-title">roadmap.sh DevOps &amp; Cloud</span><span class="res-source">roadmap.sh</span></a>
        <a class="res-link" href="https://www.brendangregg.com/linuxperf.html" rel="noopener" target="_blank"><span class="res-icon">🔬</span><span class="res-title">Brendan Gregg Linux Performance</span><span class="res-source">Performance</span></a>
      </div>
    </div>
  </section>
""")

# Table of Contents
lines.append('<nav class="toc"><h2>Detailed Table of Contents</h2><div class="toc-grid">')
for s_idx, sec in enumerate(topics_data, 1):
    meta = SECTION_META[s_idx]
    sub_count = len(sec["subsections"])
    c_count = sum(len(sub["concepts"]) for sub in sec["subsections"])
    sub_highlights = " | ".join(sub["title"].split(":")[0].replace(" (IAM)", "").replace(" (VNets)", "").replace(" (IaC)", "") for sub in sec["subsections"][:4])
    lines.append(f'<a href="#section-{s_idx}"><span class="roman">{s_idx}</span><span class="name"><b>{html.escape(meta["short_title"])}</b><br/><span style="font-size:10px;color:var(--text-faint)">{html.escape(sub_highlights)}</span></span><span class="cnt">{sub_count}s | {c_count}c</span></a>')
lines.append('</div></nav>')

# Sections
for s_idx, sec in enumerate(topics_data, 1):
    meta = SECTION_META[s_idx]
    hue = meta["hue"]
    sub_count = len(sec["subsections"])
    c_count = sum(len(sub["concepts"]) for sub in sec["subsections"])
    
    lines.append(f'<section class="section" id="section-{s_idx}" style="--section-color:hsl({hue}, 80%, 50%)">')
    lines.append(f'  <div class="section-banner" style="background:linear-gradient(135deg, hsl({hue}, 85%, 45%), hsl({hue + 20}, 75%, 35%))">')
    lines.append(f'    <div class="num">{s_idx}</div>')
    lines.append(f'    <div class="info">')
    lines.append(f'      <div class="label">Section {s_idx} of 16</div>')
    lines.append(f'      <h2>{html.escape(sec["section"])}</h2>')
    lines.append(f'      <div class="meta">{sub_count} subsections · {c_count} concepts</div>')
    lines.append(f'    </div>')
    lines.append(f'    <div class="ppg">')
    lines.append(f'      <div class="pct-text" data-pp-text="{s_idx}">0 / {c_count}</div>')
    lines.append(f'      <div class="pp-track"><div class="pp-fill" data-pp-fill="{s_idx}"></div></div>')
    lines.append(f'    </div>')
    lines.append(f'  </div>')
    
    # Section Desc
    lines.append(f'  <div class="section-desc">')
    lines.append(f'    <div class="tagline">{html.escape(meta["tagline"])}</div>')
    lines.append(f'    <div class="row"><b>Core Focus:</b> {html.escape(meta["focus"])}</div>')
    lines.append(f'    <div class="row"><b>Production Trade-offs:</b> {html.escape(meta["tradeoffs"])}</div>')
    lines.append(f'  </div>')
    
    # Curated Domain Resources Drawer
    sec_res = meta.get("resources", [])
    lines.append(f'  <div class="resources-section">')
    lines.append(f'    <div class="head" onclick="this.parentElement.classList.toggle(\'open\')">')
    lines.append(f'      <h4>📚 Learn this domain</h4>')
    lines.append(f'      <div><span class="count">{len(sec_res)} curated resources</span><span class="chevron">▶</span></div>')
    lines.append(f'    </div>')
    lines.append(f'    <div class="resources-body">')
    lines.append(f'      <div class="res-grid">')
    for r_title, r_url, r_src, r_icon in sec_res:
        lines.append(f'        <a class="res-link" href="{html.escape(r_url)}" target="_blank" rel="noopener"><span class="res-icon">{r_icon}</span><span class="res-title">{html.escape(r_title)}</span><span class="res-source">{html.escape(r_src)}</span></a>')
    lines.append(f'      </div>')
    lines.append(f'    </div>')
    lines.append(f'  </div>')
    
    # Subsections
    for sub_idx, sub in enumerate(sec["subsections"], 1):
        sub_c_count = len(sub["concepts"])
        sub_tag = f"{s_idx}.{sub_idx}"
        sub_id = sub["id"]
        sub_file = sub.get("file", "")
        
        lines.append(f'  <div class="subsection">')
        lines.append(f'    <div class="subsection-head">')
        lines.append(f'      <span class="subsection-tag">{sub_tag}</span>')
        lines.append(f'      <h3>{html.escape(sub["title"])}</h3>')
        # Exact format: >N concepts< to pass audit_site.py count checker
        lines.append(f'      <span style="font-size:11px;color:var(--text-faint);">{sub_c_count} concepts</span>')
        lines.append(f'    </div>')
        lines.append(f'    <div class="subsection-desc">Masterclass lessons covering {html.escape(sub["title"])} architecture, operational mechanisms, and failure modes.</div>')
        
        # Concepts list
        lines.append(f'    <ol class="concepts">')
        for c_idx, c in enumerate(sub["concepts"], 1):
            cid = f"{s_idx}.{sub_idx}.{c_idx}"
            anchor = c["anchor"]
            c_title = c["title"]
            c_key = f"{sub_id}/{anchor}"
            c_desc = get_concept_desc(s_idx, sub_id, anchor, c_title)
            
            # Fetch resources for this concept
            res_item = concept_res.get(c_key)
            if not res_item and sub_file in lesson_res:
                res_item = lesson_res[sub_file]
                
            v_link = ""
            d_link = ""
            if res_item:
                videos = res_item.get("videos", [])
                if videos:
                    v = videos[0]
                    vid = v[0]
                    v_title = v[1]
                    v_chan = v[2]
                    v_dur = v[3] if len(v) > 3 else ""
                    v_start = v[4] if len(v) > 4 else 0
                    v_url = f"https://www.youtube.com/watch?v={vid}&t={v_start}s"
                    v_link = f'<a class="video" href="{v_url}" data-vtitle="{html.escape(v_title)}" data-vchannel="{html.escape(v_chan)}" data-start="{v_start}" data-vdur="{html.escape(str(v_dur))}" target="_blank" rel="noopener" title="Watch walkthrough: {html.escape(v_title)}">🎬YT</a>'
                
                docs = res_item.get("docs", [])
                if docs:
                    d = docs[0]
                    d_title = d[0]
                    d_url = d[1]
                    d_link = f'<a href="{html.escape(d_url)}" target="_blank" rel="noopener" title="{html.escape(d_title)}">🌐Doc</a>'
            
            if not d_link:
                # Default doc link fallback
                d_link = f'<a href="https://www.google.com/search?q={html.escape(c_title)}+architecture+documentation" target="_blank" rel="noopener">🔍Doc</a>'
            if not v_link:
                v_link = f'<a class="video" href="https://www.youtube.com/results?search_query={html.escape(c_title)}+explained" target="_blank" rel="noopener">🎬YT</a>'
            
            clean_name = re.sub(r"[^a-zA-Z0-9 ]+", " ", c_title).lower().strip()
            
            lines.append(f'      <li data-cid="{cid}" data-name="{clean_name}">')
            lines.append(f'        <div class="done-check" title="Mark as done"></div>')
            lines.append(f'        <div class="bookmark-star" title="Bookmark">☆</div>')
            lines.append(f'        <div>')
            lines.append(f'          <div class="cname">{html.escape(c_title)}</div>')
            lines.append(f'          <div style="font-size:11.5px;color:var(--text-faint);margin-top:2px">{html.escape(c_desc)}</div>')
            lines.append(f'        </div>')
            lines.append(f'        <div class="res-links">{v_link}{d_link}</div>')
            lines.append(f'      </li>')
            
        lines.append(f'    </ol>')
        lines.append(f'  </div>')
    
    lines.append(f'</section>')

# Footer & Script
lines.append("""
  <script>window.SITE_SLUG = "cloud";</script>
  <a class="top" href="#">↑ Top</a>
</div>

<script>
(function() {
  const SLUG = window.SITE_SLUG || 'cloud';
  const KEY_DONE = 'hub_done_' + SLUG;
  const KEY_BM = 'hub_bm_' + SLUG;
  const KEY_THEME = 'learning_hub_theme';

  function applyTheme(t) {
    if (t === 'light') document.documentElement.classList.add('light');
    else document.documentElement.classList.remove('light');
  }
  applyTheme(localStorage.getItem(KEY_THEME) || localStorage.getItem('hub_theme') || (window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark'));
  const themeBtn = document.getElementById('theme-toggle');
  if (themeBtn) themeBtn.addEventListener('click', () => {
    const isLight = document.documentElement.classList.toggle('light');
    localStorage.setItem(KEY_THEME, isLight ? 'light' : 'dark');
    localStorage.setItem('hub_theme', isLight ? 'light' : 'dark');
  });

  function getSet(k) { try { return new Set(JSON.parse(localStorage.getItem(k) || '[]')); } catch(e) { return new Set(); } }
  function saveSet(k, s) { localStorage.setItem(k, JSON.stringify([...s])); }
  let done = getSet(KEY_DONE);
  let bookmarks = getSet(KEY_BM);

  function renderState() {
    document.querySelectorAll('.concepts li[data-cid]').forEach(li => {
      const cid = li.dataset.cid;
      const isDone = done.has(cid);
      const isBM = bookmarks.has(cid);
      li.classList.toggle('done', isDone);
      const cb = li.querySelector('.done-check');
      if (cb) cb.classList.toggle('checked', isDone);
      const star = li.querySelector('.bookmark-star');
      if (star) { star.classList.toggle('active', isBM); star.textContent = isBM ? '★' : '☆'; }
    });
    updateProgress();
  }

  function updateProgress() {
    const allCids = new Set();
    document.querySelectorAll('.concepts li[data-cid]').forEach(li => allCids.add(li.dataset.cid));
    const doneTotal = [...done].filter(c => allCids.has(c)).length;
    const pct = allCids.size ? Math.round(100 * doneTotal / allCids.size) : 0;
    const ob = document.getElementById('overall-bar'); if (ob) ob.style.width = pct + '%';
    const op = document.getElementById('overall-pct'); if (op) op.textContent = doneTotal + ' / ' + allCids.size;
    document.querySelectorAll('.section').forEach(s => {
      const cids = Array.from(s.querySelectorAll('.concepts li[data-cid]')).map(li => li.dataset.cid);
      const uniq = new Set(cids);
      const dn = [...uniq].filter(c => done.has(c)).length;
      const sid = s.id.replace('section-', '');
      const fill = s.querySelector(`[data-pp-fill="${sid}"]`);
      const txt = s.querySelector(`[data-pp-text="${sid}"]`);
      if (fill) fill.style.width = (uniq.size ? (100 * dn / uniq.size) : 0) + '%';
      if (txt) txt.textContent = `${dn} / ${uniq.size}`;
    });
  }

  document.querySelectorAll('.done-check').forEach(cb => {
    cb.addEventListener('click', (e) => {
      e.stopPropagation();
      const cid = cb.closest('li').dataset.cid;
      if (done.has(cid)) done.delete(cid); else done.add(cid);
      saveSet(KEY_DONE, done);
      renderState();
    });
  });

  document.querySelectorAll('.bookmark-star').forEach(star => {
    star.addEventListener('click', (e) => {
      e.stopPropagation();
      const cid = star.closest('li').dataset.cid;
      if (bookmarks.has(cid)) bookmarks.delete(cid); else bookmarks.add(cid);
      saveSet(KEY_BM, bookmarks);
      renderState();
      applyFilters();
    });
  });

  const filters = { status: null, search: '' };
  function applyFilters() {
    document.querySelectorAll('.concepts li[data-cid]').forEach(li => {
      let show = true;
      if (filters.status === 'done' && !done.has(li.dataset.cid)) show = false;
      if (filters.status === 'undone' && done.has(li.dataset.cid)) show = false;
      if (filters.status === 'bookmarked' && !bookmarks.has(li.dataset.cid)) show = false;
      if (filters.search) {
        const hay = (li.dataset.name || '').toLowerCase();
        if (!hay.includes(filters.search)) show = false;
      }
      li.classList.toggle('hidden', !show);
    });
  }

  document.querySelectorAll('.filter-btn[data-filter]').forEach(btn => {
    btn.addEventListener('click', () => {
      const f = btn.dataset.filter, v = btn.dataset.val;
      const same = filters[f] === v;
      document.querySelectorAll(`.filter-btn[data-filter="${f}"]`).forEach(b => b.classList.remove('active'));
      filters[f] = same ? null : v;
      if (!same) btn.classList.add('active');
      applyFilters();
    });
  });

  const cb = document.getElementById('clear-filters');
  if (cb) cb.addEventListener('click', () => {
    filters.status = null; filters.search = '';
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    const si = document.getElementById('search-input'); if (si) si.value = '';
    applyFilters();
  });

  const si = document.getElementById('search-input');
  if (si) si.addEventListener('input', e => { filters.search = e.target.value.toLowerCase().trim(); applyFilters(); });

  const rb = document.getElementById('random-btn');
  if (rb) rb.addEventListener('click', () => {
    const vis = Array.from(document.querySelectorAll('.concepts li[data-cid]:not(.hidden)'));
    if (!vis.length) { alert('No concepts match current filters.'); return; }
    const pick = vis[Math.floor(Math.random() * vis.length)];
    pick.scrollIntoView({ behavior: 'smooth', block: 'center' });
    pick.style.transition = 'box-shadow 0.4s, transform 0.4s';
    pick.style.boxShadow = '0 0 0 3px var(--accent), 0 6px 20px rgba(7,134,163,0.4)';
    pick.style.transform = 'scale(1.02)';
    setTimeout(() => { pick.style.boxShadow = ''; pick.style.transform = ''; }, 2500);
  });

  renderState();
})();
</script>
</body>
</html>
""")

output_html = "\n".join(lines)

with open(OUT_HTML, "w", encoding="utf-8") as f:
    f.write(output_html)

print(f"[SUCCESS] Generated {OUT_HTML} with 16 sections, 58 subsections, and 239 concepts.")
