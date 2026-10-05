#!/usr/bin/env python3
"""
Enriches cloud_aws_azure.html with staff-level architectural depth:
- Multi-region active-active vs active-passive topologies, RTO/RPO trade-offs
- Deep-dive storage & databases: Aurora Global Database (storage-level physical replication <1s lag),
  DynamoDB Global Tables (Streams-based multi-master with Last-Writer-Wins),
  Cosmos DB multi-region multi-write with 5 consistency levels
- Networking: VPC/VNet peering, Transit Gateway route tables, Direct Connect / ExpressRoute dedicated fiber,
  PrivateLink / Private Endpoints, ALB (L7) vs NLB (L4)
- Serverless compute scaling, Cold start mitigation via Provisioned Concurrency, S3 storage class tiering math
"""
import os, re, tempfile

CLOUD_HTML_PATH = os.path.join(os.path.dirname(__file__), "..", "cloud_aws_azure.html")

ENRICHMENTS = {
    # 1.1 Core Concepts
    "1.1.1": "<b>Cloud Delivery Models:</b> <b>IaaS (EC2, Azure VMs):</b> Vendor provisions physical hardware, virtualization, and networking; you manage OS patching, runtime, middleware, and data. <b>PaaS (Elastic Beanstalk, App Service):</b> Vendor manages OS, runtime, and scaling; you deploy code and configuration. <b>SaaS (Microsoft 365, Salesforce):</b> Fully vendor-managed application.",
    "1.1.2": "<b>Cloud Deployment Models:</b> <b>Public Cloud:</b> Multi-tenant shared infrastructure partitioned via hypervisor isolation. <b>Private Cloud:</b> Dedicated single-tenant infrastructure on-premises (OpenStack, VMware). <b>Hybrid Cloud:</b> Interconnected public and private environments via Direct Connect / ExpressRoute with unified control planes (AWS Outposts, Azure Arc).",
    "1.1.3": "<b>Economics & Elasticity:</b> Converts CapEx (capital expenditure on depreciating servers) to OpEx (operating expenditure paid on consumption). Elasticity enables dynamic scaling to match real-time load, preventing over-provisioning waste while maintaining p99 latency SLAs during unexpected traffic spikes.",

    # 1.2 AWS Global Infrastructure
    "1.2.1": "<b>Regions:</b> Independent geographic areas containing multiple physically separated, isolated data centers. Designed for fault isolation; regional outages do not cascade to other regions. Cross-region communication traverses encrypted private AWS/Azure fiber backbones with low latency.",
    "1.2.2": "<b>Availability Zones (AZs):</b> One or more discrete data centers with redundant power, cooling, and low-latency (&lt;1-2ms round-trip) interconnects within a region. Deploying active workloads across &ge;3 AZs guarantees high availability against datacenter floods, fires, or power grid failures.",
    "1.2.3": "<b>Edge Network & Points of Presence:</b> Hundreds of edge locations running CloudFront, Route 53, and AWS Global Accelerator worldwide. Terminates TLS at edge POPs close to end users, caches static assets, and proxies dynamic API traffic over optimized backbone links.",
    "1.2.4": "<b>Region Selection Criteria:</b> 1. <b>Data Sovereignty & Compliance:</b> GDPR (EU), HIPAA/FedRAMP (US); 2. <b>User Proximity:</b> Lowest network latency for primary user demographics; 3. <b>Service Availability:</b> Bleeding-edge features launch in primary regions (us-east-1, eastus) first; 4. <b>Cost Variance:</b> Cloud pricing varies up to 20-30% between regions due to local energy and tax rates.",

    # 1.3 Shared Responsibility & Governance
    "1.3.1": "<b>Security Division:</b> Cloud provider owns security <i>OF</i> the cloud (physical security of facilities, hardware maintenance, hypervisor patching, network infrastructure). Customer owns security <i>IN</i> the cloud (guest OS patching, IAM policies, firewall rules, encryption at rest/in transit, customer data).",
    "1.3.2": "<b>Well-Architected Pillars:</b> Operational Excellence (run operations as code, evolve), Security (defense in depth, least privilege), Reliability (auto-recovery, cross-AZ redundancy), Performance Efficiency (serverless, right-sizing), Cost Optimization (FinOps, reserved capacity), Sustainability (ARM Graviton, high utilization).",

    # 2.1 IAM Core
    "2.1.1": "<b>IAM Entities:</b> <b>Users:</b> Long-term credentials (passwords, access keys) for individuals (anti-pattern in production). <b>Groups:</b> Collections of users sharing policies. <b>Roles:</b> Credential-less identities assumed dynamically by services, users, or external IdPs issuing short-lived STS tokens.",
    "2.1.2": "<b>Workload Identity:</b> <b>AWS IAM Roles for EC2 / IRSA for EKS:</b> Injects temporary, auto-rotating credentials via Instance Metadata Service (IMDSv2). <b>Azure Managed Identity:</b> System-assigned or User-assigned identities managed by Microsoft Entra ID. Completely eliminates hardcoded API keys and secrets.",
    "2.1.3": "<b>Enterprise Federation:</b> Authenticates corporate users via external Identity Providers (Okta, Azure AD, Ping) using SAML 2.0 or OIDC. Exchanging enterprise assertions for scoped cloud STS session tokens eliminates duplicate user stores and centralizes Multi-Factor Authentication (MFA).",
    "2.1.4": "<b>Multi-Account Governance:</b> <b>AWS Organizations:</b> Hierarchical tree of Organizational Units (OUs) governed by Service Control Policies (SCPs). <b>Azure Management Groups:</b> Nested subscription hierarchy governed by Azure Policies. Segregates blast radius across Production, Staging, Security, and Shared Services accounts.",

    # 2.2 Access Control & Policies
    "2.2.1": "<b>IAM Policy Evaluation Logic:</b> Default Deny &rarr; Explicit Deny (evaluates first; immediately overrides any Allow) &rarr; Explicit Allow &rarr; Default Deny. Conditions allow granular attribute-based access control (ABAC) based on IP address, VPC endpoint source, MFA status, or resource tags.",
    "2.2.2": "<b>Azure Role-Based Access Control:</b> Security principals (Users, Groups, Service Principals) assigned built-in or custom roles (Owner, Contributor, Reader) scoped at Management Group, Subscription, Resource Group, or individual Resource levels.",
    "2.2.3": "<b>Policy Guardrails:</b> <b>AWS SCPs:</b> Organization-level filters setting the maximum permissible permissions for member accounts; cannot be bypassed even by the account root user. <b>Permission Boundaries:</b> Delegated administration guardrail preventing developers from creating overly permissive roles.",
    "2.2.4": "<b>Secrets Management:</b> Centralized vaults (AWS Secrets Manager, Azure Key Vault) storing database credentials, OAuth tokens, and certificates. Features automated rotation via Lambda functions, KMS envelope encryption at rest, and audit logging for every secret retrieval.",

    # 3.1 Virtual Machines
    "3.1.1": "<b>Instance Families:</b> <b>General Purpose (m/t, D-series):</b> Balanced compute, memory, and network for web servers. <b>Compute Optimized (c, F-series):</b> High compute-to-memory ratio for CPU-bound batch jobs and microservices. <b>Memory Optimized (r/x, E-series):</b> In-memory caches and relational databases. <b>Accelerated Computing (p/g, N-series):</b> NVIDIA GPUs for ML training/inference.",
    "3.1.2": "<b>Golden Images:</b> Pre-baked virtual machine snapshots (AMI, Azure VM Image) containing hardened OS, security agents, and static dependencies built via HashiCorp Packer. Accelerates autoscaling instance boot times from 15 minutes to under 60 seconds.",
    "3.1.3": "<b>Purchasing Models:</b> <b>On-Demand:</b> Pay by the second, zero commitment, highest unit price. <b>Savings Plans / Reserved Instances:</b> Commit to 1-3 year baseline usage for up to 72% discount. <b>Spot / Spot VMs:</b> Bid on spare cloud capacity for up to 90% discount, subject to 2-minute termination notice upon cloud reclamation; ideal for stateless workers.",
    "3.1.4": "<b>Auto Scaling:</b> <b>AWS ASG / Azure VMSS:</b> Automatically adjusts fleet size based on dynamic metric tracking (target CPU utilization, SQS queue depth per instance). Maintains target capacity across multiple Availability Zones with automated health-check replacement.",
    "3.1.5": "<b>Instance Bootstrapping:</b> Cloud-init and User Data shell scripts executed once during initial instance provisioning. Fetches runtime configs from Parameter Store, mounts storage volumes, and registers instance with discovery registries.",
    "3.1.6": "<b>Static Public IP:</b> Elastic IP (AWS) / Public IP (Azure): Static IPv4 addresses allocated to accounts and associated with ENIs. Enables persistent external endpoints that survive instance stop/start cycles without DNS propagation delays.",

    # 3.2 Containers & Kubernetes
    "3.2.1": "<b>AWS ECS vs Azure Container Instances:</b> <b>ECS:</b> Opinionated, deeply AWS-integrated container orchestrator managing Docker tasks across EC2 or Fargate without Kubernetes complexity. <b>ACI:</b> Hypervisor-isolated serverless container execution for quick burst tasks without orchestrator overhead.",
    "3.2.2": "<b>Managed Kubernetes:</b> <b>AWS EKS / Azure AKS:</b> Cloud vendor manages, scales, and patches the Kubernetes control plane (API server, etcd) across multiple AZs with high availability SLAs. Customer provisions and manages worker node pools.",
    "3.2.3": "<b>Serverless Containers:</b> <b>AWS Fargate / Azure Container Apps:</b> Run containers without provisioning, configuring, or scaling virtual machine clusters. Pay strictly for allocated vCPU and memory per second; eliminates OS security patching and node maintenance.",
    "3.2.4": "<b>Private Container Registries:</b> Managed OCI-compliant registries (ECR, ACR) storing container images. Integrates with CI/CD pipelines, IAM role-based image pull authentication, cross-region replication, and automated vulnerability scanning (Clair, Inspector).",

    # 3.3 Serverless Compute
    "3.3.1": "<b>Event-Driven FaaS:</b> Serverless execution model running stateless functions in response to HTTP requests, queue messages, or database mutations. Automatically scales from zero to tens of thousands of concurrent executions with sub-second billing.",
    "3.3.2": "<b>Cold Start Optimization:</b> Latency incurred when provisioning a new microVM container environment (initializing JVM/Python runtimes, loading packages). <b>Mitigations:</b> Provisioned Concurrency (pre-warming execution pools), lightweight compiled runtimes (Go/Rust), AWS SnapStart (microVM snapshot restoration).",
    "3.3.3": "<b>Execution Limits:</b> AWS Lambda caps execution time at 15 minutes, ephemeral storage at 10GB, and memory from 128MB to 10,240MB (allocating proportional CPU power). Default concurrency limit of 1,000 per region requires quota increase requests for high-throughput spikes.",
    "3.3.4": "<b>Stateful Workflow Orchestration:</b> <b>AWS Step Functions / Azure Logic Apps:</b> Visual declarative state machine orchestrating serverless distributed workflows. Manages sequential branching, parallel tasks, error retries with exponential backoff, and asynchronous human approval callbacks.",

    # 4.1 Object Storage
    "4.1.1": "<b>Object Storage Architecture:</b> Flat key-value namespace storing unstructured data (blobs) accessed via HTTP REST APIs. Objects identified by bucket name and key string; provides 99.999999999% (11 9s) durability by redundantly storing data across &ge;3 facilities.",
    "4.1.2": "<b>Storage Tiers & FinOps:</b> <b>S3 Standard:</b> $0.023/GB for frequent access. <b>Intelligent-Tiering:</b> Automatically shifts objects between frequent, infrequent, and archive tiers without retrieval fees. <b>Glacier Flexible:</b> $0.0036/GB (retrieval in minutes/hours). <b>Glacier Deep Archive:</b> $0.00099/GB (retrieval 12-48h, 90% cheaper than Standard).",
    "4.1.3": "<b>Versioning & Compliance:</b> Retains past iterations of overwritten or deleted objects to recover from accidental deletes. <b>Object Lock:</b> Enforces WORM (Write Once, Read Many) retention policies in Compliance or Governance mode to prevent deletion even by the account root user.",
    "4.1.4": "<b>Server-Side Encryption:</b> <b>SSE-S3:</b> AES-256 with vendor-managed keys (zero extra cost). <b>SSE-KMS:</b> Customer-managed KMS keys enabling envelope encryption, key rotation, and CloudTrail access audits (subject to KMS per-request pricing). <b>SSE-C:</b> Customer-provided keys.",
    "4.1.5": "<b>Pre-Signed URLs / SAS Tokens:</b> Cryptographically signed temporary URLs granting time-bounded GET or PUT permissions to private objects. Enables client browsers and mobile apps to upload/download directly to/from S3/Blob storage, completely bypassing backend web servers.",
    "4.1.6": "<b>Cross-Region Replication:</b> Asynchronously replicates objects across AWS regions or Azure accounts for disaster recovery, lower geographic read latency, and regulatory compliance. Supports KMS key translation and ownership overriding.",
    "4.1.7": "<b>Object Constraints & Multipart Upload:</b> Single object size limit is 5TB. Objects larger than 100MB should (and &gt;5GB must) use Multipart Upload: splits file into parallel chunk uploads, enabling resumption on failure and saturating network bandwidth.",

    # 4.2 Block & File Storage
    "4.2.1": "<b>EBS Volume Types:</b> <b>gp3:</b> Balanced SSD default with baseline 3,000 IOPS and 125 MB/s throughput independent of volume size. <b>io2 Block Express:</b> Sub-millisecond latency SSD scaling up to 256,000 IOPS and 4,000 MB/s for mission-critical OLTP databases. <b>st1:</b> Throughput-optimized HDD for big data sequential streaming.",
    "4.2.2": "<b>EBS Snapshots:</b> Point-in-time block-level incremental backups saved to Amazon S3. Only modified storage blocks are saved after initial snapshot. Supports fast snapshot restore (FSR) and cross-region snapshot copying for disaster recovery.",
    "4.2.3": "<b>Managed Elastic File Systems:</b> <b>AWS EFS / Azure Files:</b> Serverless, POSIX-compliant shared file storage mounted concurrently across thousands of compute instances via NFSv4 (Linux) or SMB 3.0 (Windows). Automatically grows and shrinks elastically.",
    "4.2.4": "<b>Storage Decision Matrix:</b> <b>EBS:</b> High-performance single-instance block storage for databases and file systems. <b>EFS:</b> Multi-instance shared POSIX file system for web content and shared home directories. <b>S3:</b> Scalable, cost-effective HTTP-accessible object store for media, backups, and data lakes.",

    # 5.1 Virtual Networking
    "5.1.1": "<b>CIDR Planning:</b> Allocate non-overlapping RFC 1918 private IPv4 blocks (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16) across on-premises datacenters and cloud VPCs/VNets. Reserve first 4 and last 1 IP in every AWS subnet (e.g. 10.0.0.0 network, .1 router, .2 DNS, .3 reserved, .255 broadcast).",
    "5.1.2": "<b>Subnet Topologies:</b> <b>Public Subnet:</b> Associated with a route table containing <code>0.0.0.0/0 &rarr; Internet Gateway (IGW)</code>. <b>Private Subnet:</b> Routes <code>0.0.0.0/0 &rarr; NAT Gateway</code> located in a public subnet. <b>Isolated Subnet:</b> Zero internet route; communicates exclusively via VPC Endpoints.",
    "5.1.3": "<b>Internet & NAT Gateways:</b> <b>IGW:</b> Highly available, horizontally scaled VPC gateway performing 1:1 NAT for public IPs at wire speed without bandwidth limits. <b>NAT Gateway:</b> Managed service providing outbound-only SNAT for private instances; billed per hour + per GB processed (use VPC Endpoints to bypass NAT fees!).",
    "5.1.4": "<b>Route Table Mechanics:</b> Controls subnet egress traffic using longest prefix match rule evaluation. Directs local subnet traffic within VPC CIDR automatically, and directs destination traffic to IGWs, NAT GWs, Virtual Private Gateways (VGW), or Transit Gateways.",
    "5.1.5": "<b>VPC / VNet Peering:</b> Direct private network connection between two VPCs using cloud backbone routing. Zero single point of failure, no bandwidth throttling, traffic stays encrypted on AWS global fiber. <b>Constraint:</b> Non-transitive (VPC A &harr; B and B &harr; C does not enable A &harr; C).",
    "5.1.6": "<b>Centralized Hub-and-Spoke:</b> <b>AWS Transit Gateway (TGW) / Azure Virtual WAN:</b> Regional network transit hub interconnecting thousands of VPCs, on-premises Direct Connect circuits, and VPN connections. Replaces complex mesh peering with centralized route table domains.",
    "5.1.7": "<b>Hybrid Dedicated Connectivity:</b> <b>IPSec VPN:</b> Encrypted tunnel over public internet (1.25 Gbps per tunnel, variable latency). <b>Direct Connect / ExpressRoute:</b> Dedicated physical fiber connection (1 Gbps to 100 Gbps) from customer datacenter to cloud router; delivers consistent sub-millisecond latency and private SLAs.",

    # 5.2 Network Security
    "5.2.1": "<b>Security Groups:</b> Stateful, instance-level virtual firewall attached to Elastic Network Interfaces (ENIs). Inbound allow rules automatically permit corresponding return outbound traffic regardless of outbound rules. Evaluated as a holistic set (no deny rules).",
    "5.2.2": "<b>Network Access Control Lists:</b> Stateless, subnet-level security boundary evaluated in numerical order (rule 100 before 200). Supports both explicit ALLOW and DENY rules. Because it is stateless, return traffic must explicitly permit ephemeral ports (1024-65535).",
    "5.2.3": "<b>Azure Network Security Groups:</b> Stateful security filter applied to subnets or NICs with 5-tuple matching (source IP, source port, destination IP, destination port, protocol). Evaluates prioritized rules from 100 to 4096 with default deny inbound.",
    "5.2.4": "<b>SG vs NACL Architectural Comparison:</b> <b>Security Groups:</b> Stateful, attached to ENI/instance, allow-only rules, evaluates all rules, first line of defence. <b>NACL:</b> Stateless, attached to subnet, allows and denies, ordered rule processing, acts as secondary blast-radius guardrail.",

    # 5.3 Load Balancing & Traffic Routing
    "5.3.1": "<b>Application vs Network Load Balancer:</b> <b>ALB:</b> Layer 7 (HTTP/HTTPS/gRPC) routing based on URL path, host header, HTTP method, and query params; integrates with AWS WAF and handles SSL termination. <b>NLB:</b> Layer 4 (TCP/UDP/TLS) ultra-low latency router handling tens of millions of RPS with static Anycast IPs.",
    "5.3.2": "<b>Azure Load Balancing Services:</b> <b>Application Gateway:</b> Regional Layer 7 load balancer with integrated Web Application Firewall (WAF) and URL-based routing. <b>Azure Load Balancer:</b> Ultra-fast Layer 4 TCP/UDP pass-through load balancer with sub-millisecond latencies.",
    "5.3.3": "<b>Edge Distribution & Global Balancing:</b> <b>CloudFront / Azure Front Door:</b> Global anycast CDN terminating TCP/TLS handshakes at edge POPs, caching dynamic and static content. AWS Global Accelerator routes non-HTTP TCP/UDP traffic over the private AWS global fiber backbone.",
    "5.3.4": "<b>Route 53 Routing Policies:</b> <b>Simple:</b> Single IP/DNS record. <b>Weighted:</b> Percentage split for canary deployments. <b>Latency-Based:</b> Routes user to lowest latency AWS region. <b>Failover:</b> Active-passive disaster recovery driven by health checks. <b>Geolocation:</b> Routes based on user country/continent.",

    # 6.1 Relational Databases
    "6.1.1": "<b>Managed Relational Database Service:</b> Automates hardware provisioning, OS/DB engine patching, automated continuous snapshots, and point-in-time recovery (PITR) up to 35 days. Storage auto-scaling dynamically expands EBS volumes without downtime.",
    "6.1.2": "<b>Cloud-Native Aurora Architecture:</b> Decouples compute from storage. Distributed log-structured storage layer replicates 6 copies across 3 Availability Zones (quorum write 4/6, quorum read 3/6). Eliminates dirty buffer flushing by writing redo logs directly to storage. <b>Serverless v2:</b> Scales compute instantly in fine-grained ACUs (0.5 to 128 ACUs).",
    "6.1.3": "<b>Multi-AZ High Availability:</b> Synchronous replication to a dedicated standby database instance in a separate Availability Zone. In the event of primary hardware failure, automated DNS failover flips traffic to standby in 60-120 seconds with Zero Data Loss (RPO = 0).",
    "6.1.4": "<b>Read Replicas & Scalability:</b> Asynchronous replication using database binlogs. Scales read-heavy workloads up to 15 read replicas in Aurora / 5 in standard RDS. Supports cross-region read replicas for low read latency globally and regional disaster recovery targets.",
    "6.1.5": "<b>Azure SQL DB & Managed Instance:</b> Managed SQL Server engine running on Azure. Hyperscale tier decouples compute and storage using page servers and log service, scaling up to 100TB with instant backups and sub-minute recovery.",

    # 6.2 NoSQL, Cache & Data Warehousing
    "6.2.1": "<b>Amazon DynamoDB Fundamentals:</b> Serverless, fully managed distributed NoSQL key-value and document store delivering single-digit millisecond latency at any scale. Supports On-Demand capacity (auto-scaling pay-per-request) and Provisioned capacity with auto-scaling RCU/WCU.",
    "6.2.2": "<b>Partition Key Design & Hotspots:</b> Internal storage partitions split when size &gt; 10GB or throughput &gt; 1,000 WCU / 3,000 RCU. Avoid low-cardinality keys (e.g. status) to prevent hot partition throttling. Use composite keys (PK + SK) and write-sharding (salting keys with random suffixes <code>#0-#N</code>) for uniform distribution.",
    "6.2.3": "<b>Multi-Region Multi-Master Databases:</b> <b>DynamoDB Global Tables:</b> Fully managed active-active replication across multiple AWS regions using DynamoDB Streams; uses Last-Writer-Wins (LWW) conflict resolution. <b>Azure Cosmos DB:</b> Globally distributed multi-model database supporting multi-region writes with 5 tunable consistency levels (Strong, Bounded Staleness, Session, Consistent Prefix, Eventual).",
    "6.2.4": "<b>In-Memory Caching:</b> <b>Amazon ElastiCache / Azure Cache for Redis:</b> Sub-millisecond in-memory cache layer. Redis Cluster provides distributed sharding across up to 500 nodes. Implements cache-aside or write-through caching patterns with memory eviction policies (volatile-lru, allkeys-lru).",
    "6.2.5": "<b>Analytical Data Warehouses:</b> <b>Amazon Redshift / Azure Synapse:</b> Columnar storage with Massively Parallel Processing (MPP) architecture. Distributes query execution across a cluster of compute nodes for petabyte-scale OLAP SQL queries. Redshift Spectrum queries raw Parquet data directly on S3 without loading.",

    # 7.1 Asynchronous Messaging
    "7.1.1": "<b>SQS Standard vs FIFO:</b> <b>Standard Queue:</b> Unlimited throughput, at-least-once delivery, best-effort message ordering (duplicates possible). <b>FIFO Queue:</b> Strict ordering within Message Group ID, exactly-once processing via deduplication ID; throughput capped at 3,000 msg/s with batching (300 msg/s without).",
    "7.1.2": "<b>SNS Pub/Sub Fan-Out:</b> Publisher pushes a single notification to an SNS topic; SNS fans out identical message copies asynchronously to multiple disparate subscriber endpoints (multiple SQS queues, Lambda functions, HTTPS webhooks, email).",
    "7.1.3": "<b>Azure Service Bus Enterprise Features:</b> Fully managed enterprise message broker with message queues and publish-subscribe topics. Supports message sessions (ordered FIFO), scheduled delivery, dead-letter queues, message deduplication, and atomic transactions.",
    "7.1.4": "<b>Dead-Letter Queue Architecture:</b> Fault-tolerant queue isolating poison messages that fail processing after a specified <code>maxReceiveCount</code>. Prevents unprocessable messages from blocking the queue in infinite retry loops; triggers CloudWatch alarms for developer remediation.",
    "7.1.5": "<b>EventBridge / Azure Event Grid:</b> Serverless enterprise event buses that route JSON events using declarative content filtering patterns. Decouples event producers from consumers and integrates with 100+ native SaaS platforms and cloud services without writing glue code.",

    # 7.2 Streaming Platforms
    "7.2.1": "<b>Kinesis Data Streams:</b> Real-time streaming platform ordered per shard. Each shard ingests up to 1 MB/s (1,000 records/s) and outputs 2 MB/s. Data retained from 24 hours to 365 days; multiple consumer applications process streams concurrently via Enhanced Fan-Out.",
    "7.2.2": "<b>Azure Event Hubs:</b> Scalable big data streaming platform capable of ingesting millions of events per second. Supports Kafka client protocol natively, partitioned consumer groups, and Event Hubs Capture for automated archival into Azure Blob Storage.",
    "7.2.3": "<b>Amazon MSK (Managed Kafka):</b> Fully managed Apache Kafka cluster handling broker provisioning, TLS encryption, Zookeeper/KRaft orchestration, and cluster patching. Best when migrating existing Kafka Connect connectors or Kafka Streams applications.",
    "7.2.4": "<b>Messaging Architectural Decision Guide:</b> <b>SQS:</b> Asynchronous point-to-point task queues and worker decoupling. <b>SNS + SQS:</b> Fan-out pub/sub to multiple downstream microservices. <b>Kinesis / Event Hubs:</b> High-throughput ordered event streams replayed by multiple analytical consumers. <b>EventBridge:</b> Event-driven architecture with complex payload routing.",

    # 8.1 Metrics & Alarms
    "8.1.1": "<b>CloudWatch Metrics Architecture:</b> Built-in hypervisor metrics (CPU utilization, network packets, disk read/write bytes). Detailed monitoring provides 1-minute granularity. Custom metrics published via <code>PutMetricData</code> API with dimensions; CloudWatch Metric Math calculates composite ratios.",
    "8.1.2": "<b>Alarm Actions & Composite Alarms:</b> Alarms monitor metrics crossing static thresholds or statistical anomaly detection bands. Triggers Auto Scaling policies, SNS notifications, or EC2 instance recovery. Composite alarms combine multiple conditions using boolean logic (AND/OR).",
    "8.1.3": "<b>Azure Monitor & Action Groups:</b> Unified telemetry solution collecting infrastructure metrics and diagnostic logs. Metric and log search alerts evaluate queries and trigger Action Groups (SMS, email, webhooks, automation runbooks, Logic Apps).",

    # 8.2 Logging, Tracing & Audit
    "8.2.1": "<b>CloudWatch Logs Management:</b> Log groups aggregate log streams from applications, containers, and Lambda. Structured JSON logging enables rapid querying using CloudWatch Logs Insights (aggregations, percentiles). Enforce retention policies to avoid unbounded storage costs.",
    "8.2.2": "<b>Azure Log Analytics & KQL:</b> Centralized analytics engine querying terabytes of logs using Kusto Query Language (KQL). Enables complex filtering, regex extraction, cross-resource joins, and time-chart visualization.",
    "8.2.3": "<b>Distributed Request Tracing:</b> <b>AWS X-Ray / Azure Application Insights:</b> Traces incoming HTTP requests across distributed microservice hops via trace headers (<code>X-Amzn-Trace-Id</code>). Visualizes dependency service maps and identifies bottleneck subsegments and database query latencies.",
    "8.2.4": "<b>Governance & Audit Trails:</b> <b>AWS CloudTrail / Azure Activity Log:</b> Immutable audit record capturing every API call (identity of caller, timestamp, source IP, request parameters, response). Essential for security forensic investigations and compliance audits.",

    # 9.1 Infrastructure as Code
    "9.1.1": "<b>AWS CloudFormation:</b> Declarative JSON/YAML template engine modeling and provisioning AWS resources as unified stacks. Features change sets (previewing modifications before deployment), rollback triggers on failure, and drift detection.",
    "9.1.2": "<b>AWS Cloud Development Kit (CDK):</b> Open-source software development framework to define cloud infrastructure using familiar programming languages (TypeScript, Python, Java, Go). Synthesizes object-oriented constructs into standardized CloudFormation templates.",
    "9.1.3": "<b>Azure Resource Manager & Bicep:</b> <b>ARM:</b> Declarative JSON syntax for Azure infrastructure. <b>Bicep:</b> Domain-Specific Language (DSL) with cleaner syntax, first-class modularity, and automatic dependency resolution that compiles into standard ARM templates.",
    "9.1.4": "<b>Terraform Multi-Cloud Engine:</b> HashiCorp's declarative configuration tool using HCL (HashiCorp Configuration Language). Employs providers for AWS, Azure, GCP, and SaaS APIs. Requires strict state file locking (S3 bucket + DynamoDB table for state lock) to prevent race conditions.",
    "9.1.5": "<b>Code-Native Pulumi:</b> General-purpose programming language IaC (TypeScript, Python, Go, C#). Provides full IDE autocomplete, native unit testing frameworks, real loops/conditionals, and automated deployment engines.",
    "9.1.6": "<b>IaC Enterprise Best Practices:</b> 1. <b>Modularity:</b> Decouple state by lifecycle (network, database, compute); 2. <b>Remote State Security:</b> Encrypt state at rest, enforce strict IAM access; 3. <b>CI/CD Automation:</b> Execute <code>plan</code> on pull requests and <code>apply</code> strictly via automated pipeline runners."
}

def enrich_cloud_html():
    with open(CLOUD_HTML_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    count = 0
    for cid, text in ENRICHMENTS.items():
        pattern = re.compile(
            rf'(<li\b[^>]*data-cid="{re.escape(cid)}"[^>]*>[\s\S]*?<div class="cname">[\s\S]*?<\/div>)\s*<div style="font-size:11.5px;color:var\(--text-faint\);margin-top:2px">([\s\S]*?)<\/div>',
            re.IGNORECASE
        )
        content, n = pattern.subn(
            rf'\1<div style="font-size:11.5px;color:var(--text-faint);margin-top:2px">{text}</div>',
            content
        )
        count += n

    dir_name = os.path.dirname(CLOUD_HTML_PATH)
    fd, temp_path = tempfile.mkstemp(dir=dir_name, text=True)
    with os.fdopen(fd, "w", encoding="utf-8") as tmp:
        tmp.write(content)
    os.replace(temp_path, CLOUD_HTML_PATH)
    print(f"Enriched {count} concepts in cloud_aws_azure.html!")

if __name__ == "__main__":
    enrich_cloud_html()
