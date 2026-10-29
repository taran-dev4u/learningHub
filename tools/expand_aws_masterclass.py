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
            if attempt == 3: raise
            time.sleep(0.1 * (attempt + 1))
    if os.path.exists(temp_name):
        try: os.unlink(temp_name)
        except OSError: pass

# 55 Concepts across 11 Subsections
AWS_SUBSECTIONS = [
    {
        "num": "1.1",
        "title": "AWS Foundations & Identity and Access Management (IAM)",
        "desc": "Cloud fundamentals, global edge infrastructure, least-privilege IAM policies, role assumption delegation, and permission boundaries.",
        "concepts": [
            ("1.1.1", "Cloud Computing Models (IaaS, PaaS, SaaS) & Shared Responsibility",
             "Infrastructure vs Platform vs Software as a Service distinctions, and the AWS Shared Responsibility Model (Security OF the Cloud vs Security IN the Cloud).",
             "https://www.youtube.com/watch?v=M988_fsOSWo", "00:00", "freeCodeCamp.org", "https://aws.amazon.com/compliance/shared-responsibility-model/"),
            ("1.1.2", "AWS Global Infrastructure: Regions, Availability Zones & Edge Locations",
             "Geographic Regions, fault-isolated Availability Zones (AZs) connected with sub-millisecond fiber, Edge Locations, and Regional Edge Caches.",
             "https://www.youtube.com/watch?v=Ia-UEYYR44s", "00:00", "AWS", "https://aws.amazon.com/about-aws/global-infrastructure/"),
            ("1.1.3", "IAM Fundamentals: Root User Security, IAM Users, Groups & Policies",
             "Securing root account credentials with hardware MFA, IAM user principles, policy structure (Effect, Action, Resource, Condition), and JSON policy syntax.",
             "https://www.youtube.com/watch?v=YQV_55_Qy6A", "00:00", "freeCodeCamp.org", "https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html"),
            ("1.1.4", "IAM Roles, Instance Profiles & STS AssumeRole Delegation",
             "Temporary short-lived credentials via AWS Security Token Service (STS), EC2 instance profiles, cross-account IAM roles, and OIDC identity federation.",
             "https://www.youtube.com/watch?v=f47bK1w1Y30", "00:00", "AWS", "https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html"),
            ("1.1.5", "Policy Evaluation Logic: Explicit Deny, SCPs & Permission Boundaries",
             "Evaluation algorithm precedence: explicit deny outranks everything; Service Control Policies (SCPs) in AWS Organizations and maximum permission boundaries.",
             "https://www.youtube.com/watch?v=0hY1a-tA0jQ", "00:00", "AWS", "https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html")
        ]
    },
    {
        "num": "1.2",
        "title": "AWS VPC & Core Network Architecture",
        "desc": "Software-defined networking, CIDR design, public/private subnets, stateful security groups, transit gateways, and PrivateLink.",
        "concepts": [
            ("1.2.1", "VPC Fundamentals: CIDR Blocks, Public vs Private Subnets & Route Tables",
             "IPv4/IPv6 CIDR range allocation (/16 to /28), subnet reservation (5 AWS reserved IPs), and explicit route table associations for traffic steering.",
             "https://www.youtube.com/watch?v=5_31yO9Z_1s", "00:00", "freeCodeCamp.org", "https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html"),
            ("1.2.2", "Internet Gateways (IGW), NAT Gateways & Egress-Only Gateways",
             "Bi-directional internet access via IGW, highly available managed NAT Gateways per AZ for outbound private subnet updates, and IPv6 egress gateways.",
             "https://www.youtube.com/watch?v=0uV7T9oJk4k", "00:00", "freeCodeCamp.org", "https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html"),
            ("1.2.3", "Security Groups (Stateful) vs Network ACLs (Stateless)",
             "Stateful instance-level firewalls with automatic return traffic vs stateless subnet-level packet filtering with numbered rule precedence.",
             "https://www.youtube.com/watch?v=8I1kM2oX7t4", "00:00", "freeCodeCamp.org", "https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Security.html"),
            ("1.2.4", "VPC Peering, Transit Gateway & Direct Connect Hybrid Networking",
             "Non-transitive 1:1 VPC peering, hub-and-spoke multi-VPC Transit Gateway (TGW) routing, and dedicated fiber Direct Connect (DX) links.",
             "https://www.youtube.com/watch?v=q67D8s6N2p8", "00:00", "AWS", "https://docs.aws.amazon.com/vpc/latest/tgw/what-is-transit-gateway.html"),
            ("1.2.5", "VPC Endpoints (Gateway vs Interface PrivateLink Endpoints)",
             "Routing traffic securely without traversing the public internet: Gateway Endpoints (S3 & DynamoDB route tables) vs Interface Endpoints powered by AWS PrivateLink.",
             "https://www.youtube.com/watch?v=5U9yP_Q1z70", "00:00", "AWS", "https://docs.aws.amazon.com/vpc/latest/privatelink/endpoint-service.html")
        ]
    },
    {
        "num": "1.3",
        "title": "AWS Compute: EC2, Elastic Load Balancing & Auto Scaling",
        "desc": "Scalable virtual compute, instance sizing, Layer 4/7 load balancers, health checks, launch templates, and dynamic auto scaling.",
        "concepts": [
            ("1.3.1", "EC2 Architecture: Instance Types, AMIs & User Data Bootstrap Scripts",
             "Compute families (General, Compute, Memory, Storage, Accelerated), Amazon Machine Images (AMI), Nitro hypervisor, and instance bootstrap scripts.",
             "https://www.youtube.com/watch?v=mC1yA3Lq7w0", "00:00", "freeCodeCamp.org", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Concepts.html"),
            ("1.3.2", "EC2 Pricing Models: On-Demand, Savings Plans, Reserved & Spot Instances",
             "Cost optimization trade-offs: full-flexibility On-Demand, 1-3 year compute commitments with Savings Plans/RI, and up to 90% discount Spot bidding.",
             "https://www.youtube.com/watch?v=9aK_2v1G6Lw", "00:00", "freeCodeCamp.org", "https://aws.amazon.com/ec2/pricing/"),
            ("1.3.3", "Elastic Load Balancers: ALB (Layer 7) vs NLB (Layer 4) Architecture",
             "Application Load Balancer (path/host routing, HTTP/2, WebSockets) vs Network Load Balancer (ultra-low latency, static IP, millions of TCP/UDP req/sec).",
             "https://www.youtube.com/watch?v=sO7m3V_8N00", "00:00", "Hussein Nasser", "https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/what-is-load-balancing.html"),
            ("1.3.4", "Target Groups, Health Checks & Cross-Zone Load Balancing",
             "Backend registration, deep HTTP health check endpoints, deregistration delay connection draining, and cross-zone traffic distribution.",
             "https://www.youtube.com/watch?v=3g8K9s0_2Yw", "00:00", "AWS", "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-target-groups.html"),
            ("1.3.5", "Auto Scaling Groups (ASG): Launch Templates & Dynamic Scaling Policies",
             "Horizontal elastic capacity, target tracking metrics (CPU/request count), step scaling, predictive scaling, and health check replacement.",
             "https://www.youtube.com/watch?v=8qW1b8r3m4c", "00:00", "freeCodeCamp.org", "https://docs.aws.amazon.com/autoscaling/ec2/userguide/what-is-amazon-ec2-auto-scaling.html")
        ]
    },
    {
        "num": "1.4",
        "title": "AWS Storage: S3 Object Storage, EBS Block Storage & EFS",
        "desc": "Durable object lakes, high-IOPS block volumes, distributed POSIX network file systems, lifecycle tiering, and encryption.",
        "concepts": [
            ("1.4.1", "Amazon S3 Architecture: Buckets, Keys & Strong Consistency Guarantees",
             "Global namespace, prefix partitioning, 11 9s durability (99.999999999%), and read-after-write strong consistency for PUTs and DELETEs.",
             "https://www.youtube.com/watch?v=v33UblSkLce", "00:00", "freeCodeCamp.org", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html"),
            ("1.4.2", "S3 Storage Classes: Standard, Intelligent-Tiering, Glacier & Lifecycle Rules",
             "Cost tiering: Standard, Infrequent Access (IA), automated machine learning tiering (Intelligent-Tiering), Glacier Flexible, Glacier Deep Archive.",
             "https://www.youtube.com/watch?v=5rT8Xq_0n7w", "00:00", "freeCodeCamp.org", "https://aws.amazon.com/s3/storage-classes/"),
            ("1.4.3", "S3 Security: Bucket Policies, Pre-Signed URLs, CORS & KMS Encryption",
             "Resource-based access policies, client direct-to-S3 uploads with temporary pre-signed URLs, cross-origin resource sharing, and SSE-S3/SSE-KMS encryption.",
             "https://www.youtube.com/watch?v=4y1A3W_0o8c", "00:00", "AWS", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/security.html"),
            ("1.4.4", "EBS Volume Types: gp3 vs io2 Block Express & Snapshot Automation",
             "Persistent raw block storage: baseline 3,000 IOPS / 125 MB/s on gp3, sub-millisecond mission-critical io2 Block Express, and incremental snapshots to S3.",
             "https://www.youtube.com/watch?v=7uK0m9W1q8s", "00:00", "freeCodeCamp.org", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-volume-types.html"),
            ("1.4.5", "Amazon EFS Distributed Network File System & Amazon FSx (Lustre/Windows)",
             "Elastic NFSv4 POSIX filesystem shared across thousands of concurrent EC2/containers, multi-AZ durability, and FSx for Lustre high-throughput HPC workloads.",
             "https://www.youtube.com/watch?v=9oM2p7R8s1c", "00:00", "AWS", "https://docs.aws.amazon.com/efs/latest/ug/whatisefs.html")
        ]
    },
    {
        "num": "1.5",
        "title": "AWS Relational, NoSQL & In-Memory Databases",
        "desc": "Enterprise relational databases, cloud-native storage engines, serverless document/key-value tables, and in-memory caches.",
        "concepts": [
            ("1.5.1", "Amazon RDS: Multi-AZ Synchronous Deployments vs Asynchronous Read Replicas",
             "High availability automated failover using synchronous physical replication to standby AZs vs scale-out read performance with up to 15 cross-AZ/cross-region replicas.",
             "https://www.youtube.com/watch?v=1x9_6F_8s0Y", "00:00", "freeCodeCamp.org", "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html"),
            ("1.5.2", "Amazon Aurora: Storage Engine Architecture & Serverless v2 Auto-Scaling",
             "Cloud-native log-structured distributed storage engine (6 copies across 3 AZs), instant crash recovery, sub-minute failovers, and instantaneous Serverless v2 ACU scaling.",
             "https://www.youtube.com/watch?v=9_6F1x8s0Yw", "00:00", "AWS", "https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/CHAP_AuroraOverview.html"),
            ("1.5.3", "DynamoDB Data Modeling: Partition Keys, Sort Keys & Access Patterns",
             "Single-table design principles, hash-based partitioning across storage nodes, composite primary keys (PK/SK), and query range lookups.",
             "https://www.youtube.com/watch?v=HaEPXoXVf2k", "00:00", "AWS", "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html"),
            ("1.5.4", "DynamoDB Global Secondary Indexes (GSI) vs Local Secondary Indexes (LSI)",
             "Asynchronous GSI scaling across independent partition keys vs synchronous LSI sharing partition keys; projection attributes and throttling isolation.",
             "https://www.youtube.com/watch?v=yQhP_Q0N7w4", "00:00", "AWS", "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/SecondaryIndexes.html"),
            ("1.5.5", "Amazon ElastiCache (Redis/Memcached) & DynamoDB DAX Acceleration",
             "Sub-millisecond in-memory caching: Redis cluster mode, replication groups, multi-AZ failover, and DynamoDB Accelerator (DAX) inline write-through microsecond caching.",
             "https://www.youtube.com/watch?v=O1A_Q0W8s4c", "00:00", "freeCodeCamp.org", "https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/WhatIs.html")
        ]
    },
    {
        "num": "1.6",
        "title": "AWS Containers & Serverless Compute",
        "desc": "Container orchestration, serverless microVM execution, managed Kubernetes clusters, and API Gateway integration.",
        "concepts": [
            ("1.6.1", "Amazon ECS: Task Definitions, Services, EC2 Launch Type vs AWS Fargate",
             "Container definition JSON schemas, replica vs daemon service scheduling, capacity providers, and serverless container execution on AWS Fargate.",
             "https://www.youtube.com/watch?v=AWEMz_WqH1s", "00:00", "freeCodeCamp.org", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/Welcome.html"),
            ("1.6.2", "Amazon EKS: Managed Control Plane, Managed Node Groups & IRSA Pod Identities",
             "Production Kubernetes on AWS: multi-AZ control plane, automated upgrades, worker node scaling, and IAM Roles for Service Accounts (IRSA) zero-trust security.",
             "https://www.youtube.com/watch?v=0k5G_7W8s1c", "00:00", "TechWorld with Nana", "https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html"),
            ("1.6.3", "AWS Lambda: Execution Lifecycle, Cold Starts, Layers & Provisioned Concurrency",
             "Firecracker microVM lifecycle (init, invoke, shutdown), optimizing package sizes, shared Lambda Layers, and Provisioned Concurrency pre-warmed execution.",
             "https://www.youtube.com/watch?v=eOBq__h4OJ4", "00:00", "freeCodeCamp.org", "https://docs.aws.amazon.com/lambda/latest/dg/welcome.html"),
            ("1.6.4", "Amazon API Gateway: REST vs HTTP APIs, Custom Authorizers & WebSocket APIs",
             "Feature-rich REST APIs (usage plans, API keys) vs low-latency cost-optimized HTTP APIs, Lambda token authorizers, and full-duplex persistent WebSocket connections.",
             "https://www.youtube.com/watch?v=1w0K_Q8s7Yc", "00:00", "freeCodeCamp.org", "https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html"),
            ("1.6.5", "AWS Step Functions & EventBridge Event-Driven Serverless Workflows",
             "Distributed state machine orchestration (Standard vs Express workflows), error catching and retries, and decoupled event routing with Amazon EventBridge rules.",
             "https://www.youtube.com/watch?v=7W8s1c0k5G_", "00:00", "AWS", "https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html")
        ]
    },
    {
        "num": "1.7",
        "title": "AWS Messaging, Event Streaming & Decoupling",
        "desc": "High-throughput asynchronous message queues, publish/subscribe fan-out, managed Kafka clusters, and real-time streaming pipelines.",
        "concepts": [
            ("1.7.1", "Amazon SQS: Standard vs FIFO Queues, Visibility Timeout & Dead-Letter Queues (DLQ)",
             "Near-infinite scaling with at-least-once standard queues vs exactly-once strict ordering FIFO queues, visibility timeout mechanics, and poison message DLQs.",
             "https://www.youtube.com/watch?v=U0v7W8s1c9o", "00:00", "freeCodeCamp.org", "https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html"),
            ("1.7.2", "Amazon SNS: Pub/Sub Topics, Fan-Out Patterns, Message Filtering & SMS/Email Delivery",
             "One-to-many publish/subscribe distribution, fan-out pattern to multiple SQS queues for parallel worker processing, and message attribute filtering policies.",
             "https://www.youtube.com/watch?v=3g8K9s0_2Yw", "00:00", "freeCodeCamp.org", "https://docs.aws.amazon.com/sns/latest/dg/welcome.html"),
            ("1.7.3", "Amazon Kinesis Data Streams & Kinesis Data Firehose Real-Time Ingestion",
             "Real-time event stream processing with shard-based partitioning, multi-consumer enhanced fan-out, and serverless zero-code delivery to S3/Redshift with Firehose.",
             "https://www.youtube.com/watch?v=5U9yP_Q1z70", "00:00", "AWS", "https://docs.aws.amazon.com/streams/latest/dev/introduction.html"),
            ("1.7.4", "Amazon EventBridge: Event Buses, Content Filtering Rules & Schema Registry",
             "Serverless central event bus, routing SaaS and microservice JSON events, declarative content-based filtering, and automated schema discovery.",
             "https://www.youtube.com/watch?v=Ia-UEYYR44s", "00:00", "AWS", "https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is-how-it-works.html"),
            ("1.7.5", "Amazon Managed Streaming for Apache Kafka (Amazon MSK) & Amazon MQ",
             "Fully managed Apache Kafka clusters with automated ZooKeeper/KRaft node management, and managed message broker hosting for RabbitMQ and Apache ActiveMQ.",
             "https://www.youtube.com/watch?v=f47bK1w1Y30", "00:00", "AWS", "https://docs.aws.amazon.com/msk/latest/developerguide/what-is-msk.html")
        ]
    },
    {
        "num": "1.8",
        "title": "Edge Networking, Content Delivery & DNS Routing",
        "desc": "Global DNS resolution, Anycast edge acceleration, CloudFront CDN edge caching, and serverless edge computation.",
        "concepts": [
            ("1.8.1", "Amazon Route 53: Hosted Zones, DNS Record Types (A, CNAME, Alias)",
             "Global authoritative DNS service, public and private hosted zones, standard records (A, AAAA, CNAME, TXT, MX), and apex-supporting Route 53 Alias records.",
             "https://www.youtube.com/watch?v=YQV_55_Qy6A", "00:00", "freeCodeCamp.org", "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/Welcome.html"),
            ("1.8.2", "Route 53 Routing Policies: Latency, Geolocation, Failover & Weighted",
             "Traffic management algorithms: Lowest-latency routing, Geolocation/Geoproximity routing, active-passive automated health check Failover, and Weighted canary splits.",
             "https://www.youtube.com/watch?v=5_31yO9Z_1s", "00:00", "freeCodeCamp.org", "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy.html"),
            ("1.8.3", "Amazon CloudFront: CDN Edge Caching, Origins, Origin Access Control (OAC)",
             "Global Points of Presence (PoPs), caching behaviors, Cache-Control header evaluation, multi-origin routing, and locking S3 down with Origin Access Control (OAC).",
             "https://www.youtube.com/watch?v=v33UblSkLce", "00:00", "freeCodeCamp.org", "https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Introduction.html"),
            ("1.8.4", "Edge Compute: CloudFront Functions vs Lambda@Edge Request/Response Interception",
             "Sub-millisecond lightweight JavaScript transformations at 450+ edge PoPs (CloudFront Functions) vs full Node/Python compute at regional caches (Lambda@Edge).",
             "https://www.youtube.com/watch?v=0hY1a-tA0jQ", "00:00", "AWS", "https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/edge-functions.html"),
            ("1.8.5", "AWS Global Accelerator: Anycast IP Routing & Edge-to-VPC Acceleration",
             "Static Anycast IP addresses, ingress at nearest AWS edge location, and routing over the private global AWS network backbone directly to ALBs and EC2 instances.",
             "https://www.youtube.com/watch?v=Ia-UEYYR44s", "00:00", "AWS", "https://docs.aws.amazon.com/global-accelerator/latest/dg/what-is-global-accelerator.html")
        ]
    },
    {
        "num": "1.9",
        "title": "Security, Cryptography & Threat Detection",
        "desc": "Cryptographic key management, secrets rotation, Layer 7 application firewalls, DDoS defense, and AI-driven security auditing.",
        "concepts": [
            ("1.9.1", "AWS KMS: Customer Managed Keys (CMK), Envelope Encryption & Key Policies",
             "Hardware Security Module (FIPS 140-2 Level 3 HSM) key generation, envelope encryption with data keys (plaintext/ciphertext), and key resource policies.",
             "https://www.youtube.com/watch?v=4y1A3W_0o8c", "00:00", "AWS", "https://docs.aws.amazon.com/kms/latest/developerguide/overview.html"),
            ("1.9.2", "AWS Secrets Manager & Systems Manager Parameter Store Secret Rotation",
             "Secure encrypted credential storage, automated database credential rotation via Lambda, and hierarchical string/secure-string configuration management.",
             "https://www.youtube.com/watch?v=8I1kM2oX7t4", "00:00", "freeCodeCamp.org", "https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html"),
            ("1.9.3", "AWS WAF (Web Application Firewall) & AWS Shield DDoS Protection",
             "Inspection of HTTP/HTTPS requests at CloudFront/ALB, SQL injection & XSS managed rules, rate-based IP blocking, and Shield Standard vs Advanced 24/7 SRT mitigation.",
             "https://www.youtube.com/watch?v=q67D8s6N2p8", "00:00", "AWS", "https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html"),
            ("1.9.4", "AWS GuardDuty Intelligent Threat Detection & Amazon Macie Sensitive Data Discovery",
             "Continuous ML-driven threat detection analyzing CloudTrail management events, VPC Flow Logs, and DNS queries; automated PII pattern discovery in S3 with Macie.",
             "https://www.youtube.com/watch?v=7uK0m9W1q8s", "00:00", "AWS", "https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html"),
            ("1.9.5", "AWS Security Hub, Amazon Inspector & AWS Network Firewall",
             "Centralized CSPM compliance posture dashboard against CIS benchmarks, automated EC2/ECR vulnerability scanning with Inspector, and stateful VPC boundary inspection.",
             "https://www.youtube.com/watch?v=0uV7T9oJk4k", "00:00", "AWS", "https://docs.aws.amazon.com/securityhub/latest/userguide/what-is-securityhub.html")
        ]
    },
    {
        "num": "1.10",
        "title": "Big Data Analytics, Search & Machine Learning",
        "desc": "Petabyte data warehousing, serverless interactive SQL querying, ETL data cataloging, distributed search, and managed AI models.",
        "concepts": [
            ("1.10.1", "Amazon Redshift: Columnar MPP Data Warehousing & Redshift Serverless",
             "Massively Parallel Processing (MPP) distributed cluster architecture, columnar data storage, compression encodings, sort keys, distribution styles, and Serverless query autoscaling.",
             "https://www.youtube.com/watch?v=sO7m3V_8N00", "00:00", "freeCodeCamp.org", "https://docs.aws.amazon.com/redshift/latest/mgmt/welcome.html"),
            ("1.10.2", "Amazon Athena: Interactive Serverless SQL Analytics over S3 Data Lakes",
             "Zero-infrastructure distributed Presto/Trino SQL engine querying structured/semi-structured S3 data (Parquet, ORC, JSON) with cost optimization via partition pruning.",
             "https://www.youtube.com/watch?v=8qW1b8r3m4c", "00:00", "AWS", "https://docs.aws.amazon.com/athena/latest/ug/what-is.html"),
            ("1.10.3", "AWS Glue: Serverless ETL Pipelines, Data Catalog & DynamicFrame Transformations",
             "Automated metadata discovery with Glue Crawlers, unified Apache Hive-compatible Data Catalog, serverless Apache Spark ETL jobs, and Glue DataBrew preparation.",
             "https://www.youtube.com/watch?v=9_6F1x8s0Yw", "00:00", "AWS", "https://docs.aws.amazon.com/glue/latest/dg/what-is-glue.html"),
            ("1.10.4", "Amazon OpenSearch Service: Distributed Full-Text Search, Analytics & Logstash",
             "Managed Elasticsearch/OpenSearch clusters, inverted indices, distributed sharding, real-time log ingestion with OpenSearch Ingestion, and OpenSearch Dashboards.",
             "https://www.youtube.com/watch?v=O1A_Q0W8s4c", "00:00", "freeCodeCamp.org", "https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html"),
            ("1.10.5", "Amazon Bedrock & SageMaker: Managed Foundation Models & Machine Learning APIs",
             "Single API access to leading foundation models (Claude, Llama, Titan) with Guardrails and Knowledge Bases on Bedrock, and end-to-end model building/endpoints on SageMaker.",
             "https://www.youtube.com/watch?v=AWEMz_WqH1s", "00:00", "AWS", "https://aws.amazon.com/bedrock/")
        ]
    },
    {
        "num": "1.11",
        "title": "Infrastructure as Code, Governance & Observability",
        "desc": "Declarative CloudFormation, imperative CDK code generation, multi-account Landing Zones, and unified telemetry.",
        "concepts": [
            ("1.11.1", "AWS CloudFormation: Declarative Templates, Drift Detection & StackSets",
             "JSON/YAML infrastructure templates, change sets preview, automated rollbacks on failure, configuration drift detection, and multi-region/multi-account StackSets.",
             "https://www.youtube.com/watch?v=mC1yA3Lq7w0", "00:00", "freeCodeCamp.org", "https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html"),
            ("1.11.2", "AWS Cloud Development Kit (CDK): Imperative IaC Constructs (L1/L2/L3)",
             "Defining cloud resources using TypeScript/Python, synthesizer compilation into CloudFormation, L1 Cfn primitives, L2 curated defaults, and L3 multi-service architectures.",
             "https://www.youtube.com/watch?v=eOBq__h4OJ4", "00:00", "AWS", "https://docs.aws.amazon.com/cdk/v2/guide/home.html"),
            ("1.11.3", "AWS Organizations, Control Tower & Multi-Account Landing Zones",
             "Consolidated billing, hierarchical Organizational Units (OUs), Service Control Policies (SCPs) guardrails, and automated multi-account provisioning with AWS Control Tower.",
             "https://www.youtube.com/watch?v=Ia-UEYYR44s", "00:00", "AWS", "https://docs.aws.amazon.com/organizations/latest/userguide/orgs_introduction.html"),
            ("1.11.4", "AWS Systems Manager (SSM): Session Manager Secure Shell & Run Command",
             "Agent-based secure shell management without open inbound ports (port 22) or bastion hosts, fleet-wide remote command execution, and automated patch management.",
             "https://www.youtube.com/watch?v=1w0K_Q8s7Yc", "00:00", "AWS", "https://docs.aws.amazon.com/systems-manager/latest/userguide/what-is-systems-manager.html"),
            ("1.11.5", "AWS CloudWatch & CloudTrail: Logs Insights, Metric Alarms & Audit Governance",
             "Unified monitoring telemetry: standard and high-resolution CloudWatch metrics, automated alarms, structured querying with Logs Insights, and immutable API audit trails via CloudTrail.",
             "https://www.youtube.com/watch?v=U0v7W8s1c9o", "00:00", "freeCodeCamp.org", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html")
        ]
    }
]

def render_subsections_html():
    out = []
    for sub in AWS_SUBSECTIONS:
        num = sub["num"]
        title = sub["title"]
        desc = sub["desc"]
        concepts = sub["concepts"]
        out.append(f'''<div class="subsection">
<div class="subsection-head">
<span class="subsection-tag">{num}</span>
<h3>{html_lib.escape(title)}</h3>
<span style="font-size:11px;color:var(--text-faint);">{len(concepts)} concepts</span>
</div>
<div class="subsection-desc">{html_lib.escape(desc)}</div>
<ol class="concepts">''')
        for cid, cname, cdesc, vid, vtime, vchannel, doc in concepts:
            clean_name = re.sub(r'[^a-zA-Z0-9]+', ' ', cname).lower().strip()
            out.append(f'''<li data-cid="{cid}" data-name="{clean_name}">
<div class="done-check" title="Mark as done"></div>
<div class="bookmark-star" title="Bookmark">☆</div>
<div>
<div class="cname">{html_lib.escape(cname)}</div>
<div style="font-size:11.5px;color:var(--text-faint);margin-top:2px">{html_lib.escape(cdesc)}</div>
</div>
<div class="res-links"><a class="video" data-start="0" data-vchannel="{html_lib.escape(vchannel)}" data-vdur="" data-vtitle="{html_lib.escape(cname)}" href="{vid}" rel="noopener" target="_blank" title="Watch walkthrough: {html_lib.escape(cname)}">🎬YT</a><a href="{doc}" rel="noopener" target="_blank" title="Official Reference">🌐Doc</a></div>
</li>''')
        out.append('</ol>\n</div>')
    return '\n'.join(out)

def expand_tech_aws():
    p = os.path.join(ROOT, 'tech_aws.html')
    with open(p, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update edition
    html = re.sub(
        r'<div class="edition">[^<]+</div>',
        '<div class="edition">AWS Cloud Architecture · Masterclass 01 · 11 Subsections · 55 Concepts</div>',
        html
    )

    # 2. Update stats block
    old_stats_match = re.search(r'(<div class="stats">[\s\S]*?</div>\s*(?=<div class="overall-progress">))', html)
    if old_stats_match:
        new_stats = '''<div class="stats">
    <div class="stat"><div class="n">11</div><div class="l">Subsections</div></div>
    <div class="stat"><div class="n">55</div><div class="l">Concepts</div></div>
    <div class="stat"><div class="n">100%</div><div class="l">Curated</div></div>
    <div class="stat"><div class="n">60+</div><div class="l">Verified Docs &amp; Labs</div></div>
  </div>\n\n  '''
        html = html.replace(old_stats_match.group(1), new_stats, 1)

    # 3. Update overall progress pct & search placeholder
    html = re.sub(r'<span class="pct" id="overall-pct">[^<]+</span>', '<span class="pct" id="overall-pct">0 / 55</span>', html)
    html = re.sub(r'placeholder="Search [^"]+"', 'placeholder="Search 55 concepts…"', html)

    # 4. Update focus bar & section banner
    html = re.sub(
        r'<span class="focus-bar-stats">[^<]+</span>',
        '<span class="focus-bar-stats">55 concepts &bull; 11 subsections</span>',
        html
    )
    html = re.sub(
        r'<div class="meta">[^<]+</div>',
        '<div class="meta">11 subsections · 55 concepts</div>',
        html,
        count=1
    )
    html = re.sub(
        r'<div class="pct-text" data-pp-text="1">[^<]+</div>',
        '<div class="pct-text" data-pp-text="1">0 / 55</div>',
        html
    )

    # 5. Replace subsections inside section-1
    subs_html = render_subsections_html()
    sub_start = html.find('<div class="subsection">')
    sub_end = html.find('</section>', sub_start)
    if sub_start != -1 and sub_end != -1:
        html = html[:sub_start] + subs_html + '\n' + html[sub_end:]
        print("Updated subsections in tech_aws.html")
    else:
        raise ValueError("Could not find subsections in tech_aws.html")

    atomic_write(p, html)
    print("Saved tech_aws.html successfully!")

def expand_cloud_hub():
    p = os.path.join(ROOT, 'cloud_aws_azure.html')
    with open(p, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update edition & hero stats
    html = re.sub(
        r'<div class="edition">v4 &bull; Cloud Platforms &bull; 3 Cloud Providers &bull; \d+ Subsections &bull; \d+ Concepts</div>',
        '<div class="edition">v4 &bull; Cloud Platforms &bull; 3 Cloud Providers &bull; 18 Subsections &bull; 88 Concepts</div>',
        html
    )

    # Subsections: 14 -> 18, Concepts: 69 -> 88
    html = re.sub(
        r'(<div class="stat"><div class="n">)\d+(</div><div class="l">Subsections</div></div>)',
        r'\g<1>18\g<2>',
        html
    )
    html = re.sub(
        r'(<div class="stat"><div class="n">)\d+(</div><div class="l">Concepts</div></div>)',
        r'\g<1>88\g<2>',
        html
    )

    # 2. Update card-aws in Multi-Cloud Command Deck
    card_aws_match = re.search(r'(<div class="domain-card[^"]*"[^>]*id="card-aws"[\s\S]*?</div>\s*</div>)', html)
    if card_aws_match:
        old_card = card_aws_match.group(1)
        new_card = re.sub(
            r'<div class="domain-card-chips">[\s\S]*?</div>',
            '''<div class="domain-card-chips">
<span class="domain-card-chip">11 Subsections</span>
<span class="domain-card-chip">55 Concepts</span>
<span class="domain-card-chip highlight">Compute, Storage, Networking, Serverless & Security</span>
</div>''',
            old_card
        )
        html = html.replace(old_card, new_card, 1)
        print("Updated card-aws in cloud_aws_azure.html")

    # 3. Update Section 1 header, banner, and subsections
    sec1_match = re.search(r'(<section class="section domain-section"[^>]*id="section-1"[\s\S]*?</section>)', html)
    if sec1_match:
        sec1_text = sec1_match.group(1)
        
        sec1_new = re.sub(
            r'<span class="focus-bar-stats">[^<]+</span>',
            '<span class="focus-bar-stats">55 concepts &bull; 11 subsections</span>',
            sec1_text
        )
        sec1_new = re.sub(
            r'<div class="meta">[^<]+</div>',
            '<div class="meta">11 subsections · 55 concepts</div>',
            sec1_new
        )
        sec1_new = re.sub(
            r'<div class="pct-text" data-pp-text="1">[^<]+</div>',
            '<div class="pct-text" data-pp-text="1">0 / 55</div>',
            sec1_new
        )

        subs_html = render_subsections_html()
        sub_start = sec1_new.find('<div class="subsection">')
        sub_end = sec1_new.rfind('</section>')
        if sub_start != -1 and sub_end != -1:
            sec1_new = sec1_new[:sub_start] + subs_html + '\n' + sec1_new[sub_end:]
            html = html.replace(sec1_text, sec1_new, 1)
            print("Updated section-1 in cloud_aws_azure.html")
        else:
            raise ValueError("Could not find subsections in section-1 of cloud_aws_azure.html")
    else:
        raise ValueError("Could not find section-1 in cloud_aws_azure.html")

    atomic_write(p, html)
    print("Saved cloud_aws_azure.html successfully!")

if __name__ == '__main__':
    expand_tech_aws()
    expand_cloud_hub()
    print("Finished expanding AWS Masterclass!")
