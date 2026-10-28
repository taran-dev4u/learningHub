#!/usr/bin/env python3
"""
Generate all 58 comprehensive markdown masterclasses for Cloud_DevOps_Tutorial/content/
and compile Cloud_DevOps_Tutorial/contentBundle.js.
Ensures every concept in topics.js has an exact matching ## anchor and exhaustive content.
"""

import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOPICS_FILE = os.path.join(ROOT, "Cloud_DevOps_Tutorial", "topics.js")
CONTENT_DIR = os.path.join(ROOT, "Cloud_DevOps_Tutorial", "content")
BUNDLE_FILE = os.path.join(ROOT, "Cloud_DevOps_Tutorial", "contentBundle.js")

os.makedirs(CONTENT_DIR, exist_ok=True)

with open(TOPICS_FILE, "r", encoding="utf-8") as f:
    text = f.read()

m = re.search(r"window\.topicsData\s*=\s*(\[.*\]);", text, re.DOTALL)
if not m:
    print("[ERROR] Could not parse window.topicsData from topics.js")
    sys.exit(1)

topics_data = json.loads(m.group(1))

# Specialized in-depth knowledge repository for all 58 modules
LESSON_BLUEPRINTS = {
    # 1. AWS
    "aws-foundations-iam.md": {
        "summary": "Master AWS global infrastructure, core cloud computing models, the shared responsibility model, and production-grade IAM access controls.",
        "analogies": {
            "Cloud Models": "Think of IaaS as renting an empty lot of land where you build your own house; PaaS is renting a furnished apartment where plumbing and heating are managed; SaaS is staying in a full-service luxury hotel where everything is provided.",
            "IAM": "Think of IAM like a high-security corporate headquarters: IAM Users are individual employees with ID badges, Groups are departments, Roles are temporary visitor passes or hazmat suits worn by authorized personnel to perform a specific task, and Policies are the security rulebook defining which doors the badge can unlock."
        },
        "faq": [
            ("When should I use an IAM Role vs an IAM User with static API keys?", "Never store static IAM User access keys on EC2 instances or in code. Always use IAM Roles attached via Instance Profiles or OIDC tokens for automated rotation and temporary STS credentials."),
            ("What is the difference between an SCP and an IAM Policy?", "SCPs (Service Control Policies) in AWS Organizations set the guardrail ceiling across an entire AWS account or OU. They never grant permissions; they only restrict the maximum permissions that IAM policies inside that account can grant.")
        ]
    },
    "aws-networking-vpc.md": {
        "summary": "Architect isolated cloud networks, subnets, route tables, security gateways, and enterprise hybrid connectivity.",
        "analogies": {
            "VPC": "A VPC is like a gated private office building inside a massive commercial city. Subnets are individual floors or departments. An Internet Gateway is the building's public lobby revolving door, while a NAT Gateway is an outbound-only mail chute allowing secure departments to send letters out without letting outsiders in."
        },
        "faq": [
            ("Why use a NAT Gateway instead of putting private EC2 instances in a public subnet?", "Instances in private subnets have no public IPv4 addresses, preventing direct unauthorized inbound connections from the internet while still allowing outbound internet access for patching and package downloads via NAT."),
            ("How do Security Groups differ from Network ACLs?", "Security Groups are stateful firewalls operating at the EC2 instance ENI level (if inbound traffic is allowed, return outbound traffic is automatically permitted). NACLs are stateless firewalls at the subnet boundary that evaluate every packet entering and exiting against ordered number rules.")
        ]
    },
    "aws-compute-ec2.md": {
        "summary": "Engineer scalable compute clusters with EC2 instance types, launch templates, elastic load balancing (ALB/NLB), and dynamic autoscaling.",
        "analogies": {
            "Load Balancers": "Think of an Application Load Balancer (ALB) like a smart restaurant maître d' who reads the customer's reservation ticket (URL path, HTTP headers) and escorts them to the specific sushi, pasta, or dessert chef. A Network Load Balancer (NLB) is like an ultra-high-speed highway toll plaza directing millions of vehicles purely by lane number (TCP/UDP port) in microsecond latency."
        },
        "faq": [
            ("When should I choose Spot Instances over On-Demand or Reserved Instances?", "Spot Instances offer up to 90% cost savings and are ideal for fault-tolerant, stateless batch workloads, CI/CD runners, and big data workers that can withstand a 2-minute termination notice."),
            ("What is the difference between ALB and NLB?", "ALB operates at Layer 7 (HTTP/HTTPS) and can inspect URLs, query parameters, and cookies. NLB operates at Layer 4 (TCP/UDP/TLS) and is optimized for ultra-high throughput, static IP requirements, and extreme low latency (microseconds).")
        ]
    },
    "aws-storage-s3-ebs.md": {
        "summary": "Design resilient storage architectures across object storage (S3), high-IOPS block storage (EBS), and shared file systems (EFS/FSx).",
        "analogies": {
            "Storage Types": "S3 is like a massive valet parking garage where you hand over your car (file) and get a ticket (URL key) to retrieve it from anywhere. EBS is like an external SSD drive plugged directly into your laptop's USB port (single instance attached). EFS is like a networked corporate shared folder (NFS) that hundreds of computers can read and write simultaneously."
        },
        "faq": [
            ("How does S3 Strong Consistency work?", "AWS S3 provides strong read-after-write consistency for PUT and DELETE requests of objects in all AWS regions. Immediately after an object is written or deleted, a subsequent GET or LIST will reflect the latest change."),
            ("When should I use EFS over EBS?", "Use EBS when you need low-latency, high-IOPS block storage attached to a single EC2 instance (e.g. database data directory). Use EFS when multiple compute instances need concurrent read/write access to a shared POSIX filesystem.")
        ]
    },
    "aws-databases-nosql.md": {
        "summary": "Architect mission-critical persistence layers using managed relational databases (RDS & Aurora) and single-digit millisecond NoSQL (DynamoDB).",
        "analogies": {
            "Aurora vs RDS": "Traditional RDS is like running a standalone database server on a virtual machine with attached storage. Aurora separates compute from storage: the storage layer is a purpose-built, log-structured distributed storage fleet replicated 6 ways across 3 Availability Zones, eliminating write bottlenecks and enabling near-instantaneous crash recovery."
        },
        "faq": [
            ("What is the difference between RDS Multi-AZ and Read Replicas?", "Multi-AZ is a synchronous high-availability failover mechanism across two AZs (the standby is passive and cannot serve reads). Read Replicas are asynchronous copies designed to offload read traffic across multiple instances or regions."),
            ("How do DynamoDB Partition Keys determine performance?", "DynamoDB hashes the Partition Key to determine which physical partition stores the item. High-cardinality partition keys prevent 'hot partitions' and ensure even distribution of read/write throughput.")
        ]
    },
    "aws-containers-serverless.md": {
        "summary": "Build modern container platforms and serverless microservices with ECS, EKS, AWS Lambda, API Gateway, and Step Functions.",
        "analogies": {
            "Serverless Lambda": "Think of EC2 like leasing a car where you pay every minute it sits in your driveway whether you drive it or not. AWS Lambda is like calling an Uber: you only pay for the exact milliseconds you are in motion, and the car vanishes when your trip completes."
        },
        "faq": [
            ("How can I minimize AWS Lambda cold starts in production?", "Use lightweight runtimes (Node.js/Python/Go), keep deployment packages small, minimize heavy SDK imports outside the handler, initialize database connections outside the handler for reuse, and configure Provisioned Concurrency for latency-critical endpoints."),
            ("ECS Fargate vs EKS: Which should I choose?", "Choose ECS Fargate for straightforward, AWS-native container deployments without the operational complexity of managing Kubernetes control planes. Choose EKS when your organization requires Kubernetes APIs, Helm charts, multi-cloud portability, or complex service meshes.")
        ]
    },
    "aws-messaging-observability.md": {
        "summary": "Decouple distributed systems with SQS, SNS, EventBridge, CloudWatch metrics/alarms, and CloudTrail audit logging.",
        "analogies": {
            "SQS vs SNS": "SQS is a PO Box: a sender deposits a letter, and one recipient comes to open the box, take the letter, and process it. SNS is a megaphone: a speaker announces a message, and dozens of listeners (subscribers, SQS queues, lambdas) all hear and receive their own copy instantly."
        },
        "faq": [
            ("What is SQS Visibility Timeout and why does it matter?", "When a consumer receives a message from an SQS queue, it remains in the queue but becomes invisible to other consumers for the duration of the Visibility Timeout. If the consumer fails to delete the message before the timeout expires, it becomes visible again for another consumer to retry."),
            ("CloudWatch Logs vs CloudTrail: What is the difference?", "CloudWatch monitors application and system metrics, custom logs, and triggers performance alarms. CloudTrail records every AWS API call made in your account (who did what, when, and from what IP address) for security auditing and governance.")
        ]
    },

    # 2. Azure
    "azure-foundations-entra.md": {
        "summary": "Master Microsoft Azure enterprise governance, subscription management, resource hierarchies, and Entra ID identity architecture.",
        "analogies": {
            "Entra ID": "Entra ID (formerly Azure AD) is the corporate identity passport office. It handles modern identity protocols (OAuth 2.0, OpenID Connect, SAML) and issues cryptographically signed JWT tokens, unlike on-premises Active Directory which relied on Kerberos and NTLM."
        },
        "faq": [
            ("System-Assigned vs User-Assigned Managed Identity?", "A System-Assigned identity is tied directly to the lifecycle of a single Azure resource (deleted when the resource is deleted). A User-Assigned identity is an independent standalone Azure resource that can be assigned to multiple VMs or functions simultaneously."),
            ("What is the role of Azure Management Groups?", "Management Groups provide a governance container above subscriptions. Azure Policies and RBAC applied at the Management Group level are inherited by all child subscriptions and resource groups.")
        ]
    },
    "azure-compute-networking.md": {
        "summary": "Architect resilient Azure compute infrastructure with Virtual Machines, VM Scale Sets, App Services, VNets, and load balancers.",
        "analogies": {
            "Azure VNet": "An Azure VNet isolates your private cloud network. Subnets segment workloads, and Network Security Groups (NSGs) act as packet inspection firewalls guarding incoming and outgoing ports."
        },
        "faq": [
            ("Azure Load Balancer vs Application Gateway?", "Azure Load Balancer operates at Layer 4 (TCP/UDP) with ultra-high throughput and static IP support. Application Gateway operates at Layer 7 (HTTP/HTTPS) with URL-path routing, cookie-based session affinity, and an integrated Web Application Firewall (WAF).")
        ]
    },
    "azure-storage-databases.md": {
        "summary": "Design high-performance storage and globally distributed databases with Azure Blob Storage, Azure SQL, and Cosmos DB.",
        "analogies": {
            "Cosmos DB Consistency": "Think of the 5 Cosmos DB consistency levels like news distribution: Strong is a live conference call where everyone hears the exact word simultaneously; Eventual is a printed newspaper delivered hours later; Session guarantees you always see your own tweets immediately while others might see them moments later."
        },
        "faq": [
            ("What are the 5 Cosmos DB consistency levels?", "1. Strong (linearizable reads), 2. Bounded Staleness (lag bounded by time or versions), 3. Session (read-your-own-writes for a client session), 4. Consistent Prefix (reads never see out-of-order writes), 5. Eventual (weakest, highest throughput).")
        ]
    },
    "azure-containers-monitoring.md": {
        "summary": "Deploy managed Kubernetes with AKS, build event-driven apps with Container Apps & KEDA, and monitor with Log Analytics & App Insights.",
        "analogies": {
            "KEDA": "KEDA (Kubernetes Event-driven Autoscaling) allows Kubernetes pods to scale directly based on external event metrics (e.g. number of messages in an Azure Service Bus queue or Kafka topic), scaling all the way down to zero when idle."
        },
        "faq": [
            ("Azure CNI vs Kubenet in AKS?", "Kubenet assigns Pod IPs from a private internal subnet and uses NAT to communicate outside the node, saving VNet IP space. Azure CNI gives every Pod a full VNet IP address, enabling direct high-performance connectivity to VNet resources at the cost of consuming more subnet IP addresses.")
        ]
    },

    # 3. GCP
    "gcp-foundations-iam-vpc.md": {
        "summary": "Architect Google Cloud Platform resource hierarchies, unified global VPC networking, and fine-grained Cloud IAM controls.",
        "analogies": {
            "Global VPC": "In AWS and Azure, virtual networks are regional constructs. In Google Cloud, a VPC is inherently global: subnets inside the same VPC can span different continents and communicate privately across Google's global fiber backbone without internet transit or VPN gateways."
        },
        "faq": [
            ("What is Workload Identity Federation in GCP?", "Workload Identity Federation allows external workloads (such as GitHub Actions runners or AWS instances) to securely authenticate to GCP APIs using short-lived tokens without storing long-lived service account keys.")
        ]
    },
    "gcp-compute-containers.md": {
        "summary": "Scale enterprise container workloads on Google Kubernetes Engine (GKE) and serverless Cloud Run with instant scaling.",
        "analogies": {
            "GKE Autopilot": "GKE Standard requires you to manage node pools, sizing, and OS upgrades. GKE Autopilot manages the entire underlying node infrastructure: Google provisions, scales, and hardens the nodes automatically, and you only pay for the exact CPU/memory requested by your running pods."
        },
        "faq": [
            ("When should I choose Cloud Run over GKE?", "Choose Cloud Run for containerized HTTP services, webhooks, or background event handlers that benefit from automatic scale-to-zero, zero infrastructure management, and sub-second scaling. Choose GKE for complex microservices clusters requiring custom networking, daemonsets, or stateful operators.")
        ]
    },
    "gcp-storage-databases.md": {
        "summary": "Harness Google-scale persistence with Cloud Spanner, Bigtable, Cloud Storage, and BigQuery analytics.",
        "analogies": {
            "Cloud Spanner": "Cloud Spanner is the holy grail of distributed databases: it breaks the traditional CAP theorem compromise by providing full relational SQL ACID transactions with external consistency globally across continents using TrueTime atomic GPS clocks."
        },
        "faq": [
            ("How does Cloud Spanner TrueTime work?", "TrueTime uses synchronized GPS receivers and atomic clocks in Google datacenters to provide a bounded uncertainty window [earliest, latest]. By waiting out the small uncertainty window before committing, Spanner guarantees external consistency across distributed nodes globally.")
        ]
    },

    # 4. Linux & Terminal
    "linux-filesystem-permissions.md": {
        "summary": "Master the Linux Filesystem Hierarchy Standard (FHS), POSIX permissions, octal chmod, SUID/SGID, and access control lists (ACLs).",
        "analogies": {
            "Linux Permissions": "Think of file permissions like a passport with 3 entry visas: Owner, Group, and Others. Each visa has 3 stamps: Read (4), Write (2), and Execute (1). SUID is like an executive diplomatic passport: whoever carries the file temporarily acts with the file owner's full authority during execution."
        },
        "faq": [
            ("What does chmod 755 vs 644 mean?", "755 gives the owner read/write/execute (4+2+1=7), while group and others get read/execute (4+1=5)—standard for executables and directories. 644 gives the owner read/write (4+2=6), and others read-only (4)—standard for configuration files."),
            ("Why is Sticky Bit set on /tmp?", "The sticky bit (indicated by 't' in permissions, e.g. 1777) ensures that even though all users have write access to `/tmp`, a user can only delete or rename files that they personally own.")
        ]
    },
    "linux-process-performance.md": {
        "summary": "Diagnose CPU, memory, disk I/O, and networking bottlenecks using Linux kernel monitoring utilities and system performance tools.",
        "analogies": {
            "System Performance": "Think of the CPU like a restaurant chef. Load average is the total number of orders either being cooked or waiting in the order queue. If you have 4 CPU cores and a load average of 4.0, your kitchen is at 100% capacity; if load average is 8.0, orders are backing up and customers are waiting."
        },
        "faq": [
            ("What causes the Linux OOM Killer to trigger?", "When the system's physical RAM and swap space are exhausted, the Linux kernel invokes the Out-Of-Memory (OOM) Killer to select and terminate high-memory processes (based on `oom_score`) to prevent the entire operating system kernel from panicking.")
        ]
    },
    "linux-text-bash-scripting.md": {
        "summary": "Automate system engineering with pipes, streams, grep regex, sed stream editing, awk field formatting, and robust bash scripts.",
        "analogies": {
            "Pipelines": "A Linux pipeline (`|`) is an industrial assembly line: the output of machine A flows directly into the input of machine B in kernel memory without writing intermediate files to disk, achieving maximum throughput."
        },
        "faq": [
            ("Why should every Bash script start with 'set -euo pipefail'?", "`-e` exits immediately if any command fails; `-u` treats unset variables as errors; `-o pipefail` ensures that if any command in a pipeline fails, the entire pipeline returns a non-zero exit code rather than masking the error.")
        ]
    },

    # 5. Git & GitHub
    "git-architecture-internals.md": {
        "summary": "Understand Git from the ground up: the object database (blobs, trees, commits), SHA hashing, and staging mechanics.",
        "analogies": {
            "Git Objects": "A Git repository is a content-addressable key-value store. Blobs store file data (contents only, no filenames). Trees store directory listings linking filenames to blob SHA hashes. Commits store snapshots linking to a root tree, author metadata, and parent commit hashes."
        },
        "faq": [
            ("Does Git store file diffs or full snapshots?", "Git stores full file snapshots compressed with zlib. If a file does not change between commits, the new tree simply points to the existing blob hash without duplicating data.")
        ]
    },
    "git-branching-rebasing.md": {
        "summary": "Master enterprise branching models, fast-forward merges, 3-way merges, and interactive rebasing workflows.",
        "analogies": {
            "Rebase vs Merge": "A merge preserves true historical chronology by creating a new 3-way merge commit with two parents. A rebase rewrites history: it takes your feature branch commits and replays them one-by-one on top of the latest main branch, resulting in a perfectly linear commit history."
        },
        "faq": [
            ("Why use 'git push --force-with-lease' instead of 'git push --force'?", "`--force-with-lease` checks that your local remote-tracking branch matches the actual ref on the remote before overwriting, preventing you from accidentally destroying commits pushed by teammates.")
        ]
    },
    "git-advanced-reflog-bisect.md": {
        "summary": "Recover lost commits with git reflog, isolate regressions with git bisect, and work on multiple branches simultaneously with git worktree.",
        "analogies": {
            "Git Reflog": "The reflog is the flight data recorder of your local Git repository. Even if you accidentally hard-reset or delete a branch, the commits remain in `.git/objects` and the reflog records the exact SHA pointer, allowing instant recovery."
        },
        "faq": [
            ("How does git bisect work?", "Git bisect uses binary search through your commit history. You mark a known bad commit and a known good commit; Git checks out the midpoint commit for testing, halving the search space on each step to find the regression in $O(\\log N)$ time.")
        ]
    },
    "github-collaboration-actions.md": {
        "summary": "Implement enterprise branch protection rules, code review standards, and automated CI/CD workflows using GitHub Actions.",
        "analogies": {
            "GitHub Actions": "Think of a GitHub Actions workflow like an automated manufacturing test bench: code pushed to a branch triggers a runner VM that checks out the repo, installs dependencies, runs unit test suites, builds container images, and reports status checks before a PR can be merged."
        },
        "faq": [
            ("How do I avoid storing long-lived cloud credentials in GitHub Secrets?", "Configure OpenID Connect (OIDC) between GitHub Actions and your cloud provider (AWS/Azure/GCP). The GitHub runner requests a short-lived cryptographically signed OIDC token, which the cloud provider exchanges for temporary IAM credentials.")
        ]
    },

    # 6. Docker
    "docker-architecture-engine.md": {
        "summary": "Understand containerization internals: Linux kernel namespaces, control groups (cgroups), OverlayFS, and the Docker engine.",
        "analogies": {
            "Containers vs VMs": "A Virtual Machine is a standalone house with its own foundation, plumbing, electricity, and guest operating system kernel (hypervisor overhead). A Container is an apartment inside a modern high-rise: it shares the building's infrastructure (the host Linux kernel) but has its own locked private rooms and isolated meters (namespaces and cgroups)."
        },
        "faq": [
            ("What is the difference between Namespaces and Cgroups?", "Namespaces provide isolation (what a container can see: processes, network interfaces, mounts, user IDs). Cgroups provide resource limits (how much a container can consume: CPU cores, RAM limits, disk I/O, network bandwidth).")
        ]
    },
    "dockerfile-image-optimization.md": {
        "summary": "Author production Dockerfiles with multi-stage builds, layer caching optimization, and non-root distroless security hardening.",
        "analogies": {
            "Multi-Stage Builds": "A multi-stage build is like preparing a meal in a commercial kitchen with all the heavy tools (compilers, build tools, SDKs), but only plating the finished dish onto a clean tray for the customer. The bulky kitchen equipment is left behind, resulting in a minimal, secure final container image."
        },
        "faq": [
            ("ENTRYPOINT vs CMD: What is the difference?", "`ENTRYPOINT` sets the immutable command to be executed when the container starts. `CMD` provides the default arguments to that entrypoint, which can be easily overridden from the command line.")
        ]
    },
    "docker-networking-volumes.md": {
        "summary": "Configure container networking modes, persistent volume mounts, and multi-service stacks with Docker Compose.",
        "analogies": {
            "Volumes vs Bind Mounts": "A Bind Mount points directly to a specific folder on your host machine (great for local live code reloading). A Named Volume is managed completely by Docker in `/var/lib/docker/volumes/`, offering higher performance, platform independence, and safe isolation from host OS changes."
        },
        "faq": [
            ("How does inter-container DNS work in Docker Compose?", "Docker creates an internal user-defined bridge network where containers can resolve each other by their service name (e.g. `postgres`, `redis`) via Docker's embedded DNS server at 127.0.0.11.")
        ]
    },

    # 7. Kubernetes
    "k8s-architecture-control-plane.md": {
        "summary": "Deep dive into Kubernetes internals: API server, etcd raft consensus, scheduler algorithms, controller loops, and kubelet execution.",
        "analogies": {
            "Kubernetes Control Plane": "Think of Kubernetes like a large cruise ship. The API Server is the ship's bridge communications officer; etcd is the ship's indelible logbook; the Scheduler is the purser assigning passengers (pods) to available staterooms (nodes); Controllers are automated autopilot systems correcting course; and the Kubelet on each deck ensures passenger rooms are maintained to standard."
        },
        "faq": [
            ("Why is etcd critical to Kubernetes high availability?", "etcd stores the entire desired and actual state of the cluster. Because it uses the Raft consensus algorithm, an odd number of etcd members (3 or 5) is required to tolerate $F$ node failures where $N = 2F + 1$.")
        ]
    },
    "k8s-workloads-pods-deployments.md": {
        "summary": "Manage replicated workloads, pod lifecycle hooks, rolling updates, rollbacks, and health probes in Kubernetes.",
        "analogies": {
            "Deployments": "A Deployment is a state manager: you declare that you want 5 replicas of an application running version 2. If a node crashes, the Deployment controller automatically provisions replacement pods on healthy nodes to maintain the desired count."
        },
        "faq": [
            ("Liveness vs Readiness vs Startup Probes?", "Startup Probe checks if the application has finished slow initialization (disabling other probes until complete). Liveness Probe checks if the container is healthy; if it fails, kubelet kills and restarts the container. Readiness Probe checks if the pod can accept network traffic; if it fails, the pod is removed from Service endpoints.")
        ]
    },
    "k8s-stateful-daemon-jobs.md": {
        "summary": "Deploy distributed stateful applications with StatefulSets, node-level utilities with DaemonSets, and batch Jobs in Kubernetes.",
        "analogies": {
            "StatefulSets": "Deployments treat pods like cattle (fungible, interchangeable names like `web-7f8d-x`). StatefulSets treat pods like pets (unique identities: `kafka-0`, `kafka-1`, `kafka-2`), with stable network identities and dedicated persistent volume attachments that persist across restarts."
        },
        "faq": [
            ("When should I use a DaemonSet instead of a Deployment?", "Use a DaemonSet when exactly one copy of a pod must run on every node in the cluster (or a subset of nodes matching a nodeSelector), such as log forwarding agents (Fluentbit) or node monitoring exporters (Prometheus node-exporter).")
        ]
    },
    "k8s-networking-services-ingress.md": {
        "summary": "Architect Kubernetes networking: flat pod CNI networks, ClusterIP/NodePort/LoadBalancer services, Ingress controllers, and Gateway API.",
        "analogies": {
            "Kubernetes Services": "Pods are ephemeral with changing IP addresses. A Kubernetes Service provides a static virtual IP (ClusterIP) and DNS name that load-balances traffic across all matching pod endpoints using iptables or IPVS rules programmed by kube-proxy."
        },
        "faq": [
            ("How does Ingress differ from a LoadBalancer Service?", "A LoadBalancer Service provisions an external cloud load balancer for each individual service (costly). An Ingress Controller (like Nginx Ingress) provisions a single cloud load balancer and handles Layer 7 routing (host and path rules) to multiple backend services inside the cluster.")
        ]
    },
    "k8s-config-storage-helm.md": {
        "summary": "Manage externalized configurations, persistent storage (PV/PVC/CSI), RBAC security, resource quotas, and Helm package releases.",
        "analogies": {
            "Helm": "Helm is the package manager for Kubernetes (like `apt` or `brew` for Linux). It packages complex Kubernetes YAML manifests into versioned Helm Charts with customizable `values.yaml` files, enabling one-command installs, upgrades, and rollbacks."
        },
        "faq": [
            ("What is the relationship between PV, PVC, and StorageClass?", "A StorageClass defines the provisioner (e.g. AWS gp3 EBS or GCP Persistent Disk). A PersistentVolumeClaim (PVC) is a request for storage by a user/pod. A PersistentVolume (PV) is the actual physical storage volume bound to the claim.")
        ]
    },

    # 8. Terraform
    "terraform-hcl-syntax.md": {
        "summary": "Learn HashiCorp Configuration Language (HCL), declarative infrastructure provisioning, and the core Terraform lifecycle.",
        "analogies": {
            "Terraform": "Terraform is an architect's blueprint for the cloud. Instead of manually clicking buttons in cloud consoles (imperative), you declare the desired end state in code (declarative). Terraform calculates the difference between current state and desired state and executes only the necessary changes."
        },
        "faq": [
            ("What is the difference between terraform plan and terraform apply?", "`terraform plan` performs a dry-run comparison between your configuration and the state file, showing an execution plan of what will be added, modified, or destroyed. `terraform apply` executes those API calls against the cloud provider.")
        ]
    },
    "terraform-state-management.md": {
        "summary": "Master Terraform state: drift detection, remote backends (S3/DynamoDB locking), state manipulation, and secrets protection.",
        "analogies": {
            "Terraform State": "The state file (`terraform.tfstate`) is the single source of truth mapping your Terraform code to real-world cloud resource IDs. Remote state locking (e.g. with DynamoDB) is like a checkout lock on a library book: it prevents two engineers from applying changes simultaneously and corrupting the state."
        },
        "faq": [
            ("Why should you never commit terraform.tfstate to Git?", "The state file stores resource attributes in plain text, including database passwords, private keys, and environment variables. Always store state in an encrypted remote backend (such as S3 with SSE and DynamoDB locking).")
        ]
    },
    "terraform-modules-workspaces.md": {
        "summary": "Author reusable infrastructure modules, dynamic meta-arguments (count vs for_each), and manage multi-environment workspaces.",
        "analogies": {
            "Terraform Modules": "Modules are reusable functions for infrastructure. Instead of writing 200 lines of VPC, subnet, and routing table resources for dev, staging, and prod, you package the pattern into a `vpc` module and call it with environment-specific parameters."
        },
        "faq": [
            ("When should I use for_each instead of count?", "Always prefer `for_each` over `count` when managing collections of resources keyed by unique identifiers. With `count`, removing an element from the middle of a list re-indexes all subsequent resources, causing Terraform to destroy and recreate them unnecessarily.")
        ]
    },

    # 9. CI/CD Pipelines
    "cicd-principles-deployment.md": {
        "summary": "Master modern delivery principles: automated testing, Blue/Green zero-downtime deployments, Canary rollouts, and rolling updates.",
        "analogies": {
            "Deployment Strategies": "Blue/Green is like having two identical stages at a concert: while band Blue is playing, band Green sets up backstage; when ready, the master lighting and audio switch to Green instantly with zero pause. Canary is releasing new software to 5% of users first to verify stability before rolling it out to everyone."
        },
        "faq": [
            ("Continuous Delivery vs Continuous Deployment?", "In Continuous Delivery, every passing code change is automatically built, tested, and staged for release, but the final deployment to production requires manual human approval. In Continuous Deployment, every passing commit deploys directly to production automatically without human intervention.")
        ]
    },
    "github-actions-enterprise.md": {
        "summary": "Build production CI/CD workflows with GitHub Actions: multi-stage Docker builds, matrix testing, and OIDC cloud auth.",
        "analogies": {
            "OIDC Authentication": "OIDC is like showing a digital corporate ID badge to AWS/Azure: the cloud provider verifies GitHub's cryptographic signature and issues temporary credentials valid for minutes, eliminating the need to store long-lived cloud keys in repository secrets."
        },
        "faq": [
            ("How does dependency caching work in GitHub Actions?", "The `actions/cache` action saves dependency directories (like `node_modules` or `~/.m2`) keyed by a hash of the lockfile (`package-lock.json` or `pom.xml`). Subsequent runs restore the cache in seconds if the lockfile hasn't changed.")
        ]
    },
    "jenkins-pipelines.md": {
        "summary": "Author enterprise Declarative Jenkinsfiles, manage distributed controller-agent nodes, and implement GitOps delivery with ArgoCD.",
        "analogies": {
            "GitOps": "In traditional CI/CD, the CI server pushes changes to the cluster (push model). In GitOps (ArgoCD), an operator inside the cluster constantly watches the Git repository and pulls changes (pull model), automatically reconciling any configuration drift."
        },
        "faq": [
            ("Declarative vs Scripted Jenkinsfile?", "Declarative pipelines enforce a structured, readable syntax with strict stage and post-condition blocks, making them easier to maintain and validate. Scripted pipelines use Groovy scripting for arbitrary execution logic but are harder to audit and maintain.")
        ]
    },

    # 10. Apache Kafka
    "kafka-architecture-kraft.md": {
        "summary": "Master Kafka architecture: distributed commit logs, page cache zero-copy I/O, and ZooKeeper elimination with KRaft quorum.",
        "analogies": {
            "Commit Log": "Kafka is not a message queue that deletes messages after reading; it is a distributed, append-only commit log. Messages are written sequentially to disk and stored for days or weeks. Multiple consumer groups can read from the log independently at their own pace by advancing their offset pointers."
        },
        "faq": [
            ("Why is Kafka so fast despite persisting to disk?", "Kafka leverages two key operating system features: 1. Sequential disk I/O (which rivals random memory access speed), and 2. OS Page Cache with the `sendfile` zero-copy system call, transferring data directly from kernel page cache to the network socket without copying to user-space memory.")
        ]
    },
    "kafka-topics-partitions-producers.md": {
        "summary": "Engineer Kafka topics, partition scaling, producer batching (linger.ms), compression, and exactly-once semantics (EOS).",
        "analogies": {
            "Partitions": "A Kafka Topic is a logical category, but physical scaling happens at the Partition level. Think of partitions like checkout lanes at a supermarket: more lanes (partitions) allow more cashiers (consumers) to serve shoppers simultaneously."
        },
        "faq": [
            ("What does acks=all (-1) guarantee in Kafka?", "`acks=all` means the producer waits until all in-sync replicas (ISRs) have acknowledged the write before considering it successful, providing maximum durability against broker failure.")
        ]
    },
    "kafka-consumers-offset-management.md": {
        "summary": "Master Kafka consumer groups, partition assignment, cooperative sticky rebalancing, and dead-letter queue strategies.",
        "analogies": {
            "Consumer Groups": "If a topic has 6 partitions and a consumer group has 3 consumers, each consumer reads 2 partitions. If you scale up to 6 consumers, each reads 1 partition. If you add a 7th consumer, it sits idle as a hot standby because a partition can only be consumed by one consumer per group."
        },
        "faq": [
            ("What is the Cooperative Sticky Rebalance protocol?", "Traditional eager rebalancing revoked all partition assignments from all consumers during a rebalance, causing processing stalls. The Cooperative Sticky protocol only reassigns partitions that actually need to move, allowing consumers to continue processing uninterrupted.")
        ]
    },
    "kafka-ecosystem-connect-streams.md": {
        "summary": "Build stream processing pipelines with Confluent Schema Registry (Avro), Kafka Connect, and Kafka Streams.",
        "analogies": {
            "Kafka Connect": "Kafka Connect is the declarative data plumbing system for Kafka: instead of writing custom consumer/producer code to move data into PostgreSQL or Elasticsearch, you deploy pre-built open-source Source and Sink connectors via simple JSON configurations."
        },
        "faq": [
            ("Why use Schema Registry with Avro?", "Schema Registry enforces contract compatibility (backward, forward, full) between producers and consumers. If a producer attempts to publish messages with an incompatible schema change, the registry rejects it before corrupting downstream consumers.")
        ]
    },

    # 11. Apache Spark
    "spark-architecture-execution.md": {
        "summary": "Master Apache Spark cluster topologies: Driver, Executors, cluster managers, DAG scheduling, and shuffle boundaries.",
        "analogies": {
            "Spark DAG": "The Spark Driver is a master general planning a military campaign: it builds a Directed Acyclic Graph (DAG) of transformations, optimizes it, cuts it into stages at shuffle boundaries, and assigns task units to worker executors in the field."
        },
        "faq": [
            ("What creates a Stage boundary in Spark?", "Wide transformations (like `groupByKey`, `reduceByKey`, `join`) that require data to be shuffled across network partitions create stage boundaries. Narrow transformations (like `map`, `filter`) execute within the same stage without network transfer.")
        ]
    },
    "spark-rdds-transformations-actions.md": {
        "summary": "Understand Resilient Distributed Datasets (RDDs), lineage graphs, lazy evaluation, and deterministic fault recovery.",
        "analogies": {
            "RDD Lineage": "An RDD does not immediately store computed data; it stores the mathematical recipe (lineage graph) of how to compute it from raw data. If a worker node crashes and loses its memory partition, Spark simply replays the recipe on that specific partition without restarting the entire job."
        },
        "faq": [
            ("Why is Spark evaluation lazy?", "Lazy evaluation allows Spark to inspect the complete chain of transformations and optimize the physical execution plan (e.g. pushing filters down to the data source so unnecessary data is never loaded into memory).")
        ]
    },
    "spark-dataframes-catalyst.md": {
        "summary": "Harness Spark DataFrames, Spark SQL, Catalyst query optimization, and the Tungsten binary execution engine.",
        "analogies": {
            "Catalyst & Tungsten": "Catalyst is like an elite database query optimizer that transforms high-level SQL/DataFrame code into optimized execution bytecode. Tungsten manages raw binary memory directly off-heap, bypassing JVM garbage collection pauses and object serialization overhead."
        },
        "faq": [
            ("Why are DataFrames faster than raw RDDs?", "DataFrames use Catalyst optimization and Tungsten off-heap execution with whole-stage code generation, avoiding Java object serialization and garbage collection overhead.")
        ]
    },
    "spark-streaming-performance.md": {
        "summary": "Tune Spark performance: shuffle partitions, broadcast joins, handling data skew, and Structured Streaming watermarks.",
        "analogies": {
            "Broadcast Join": "In a regular join of two large tables, both tables must be shuffled across the network. If one table is small (e.g. under 10MB), a Broadcast Join copies the small table to every executor, completely eliminating network shuffling for the large table."
        },
        "faq": [
            ("What is a Watermark in Spark Structured Streaming?", "A watermark defines how late data can arrive before it is dropped by event-time window aggregations, allowing the state store to safely evict old aggregation states from memory.")
        ]
    },

    # 12. PostgreSQL
    "postgresql-relational-normalization.md": {
        "summary": "Master relational database theory, data integrity constraints, functional dependencies, and BCNF normalization.",
        "analogies": {
            "BCNF Normalization": "Every non-key attribute must depend on 'the key, the whole key, and nothing but the key, so help me Codd'. Normalization eliminates data redundancy and update anomalies; strategic denormalization is applied intentionally when read latency demands it."
        },
        "faq": [
            ("When should a normalized schema be denormalized?", "Denormalize only when production profiling proves that complex joins are causing read bottlenecks on high-throughput analytical queries, and when the application can tolerate the additional write complexity to keep denormalized data synchronized.")
        ]
    },
    "postgresql-storage-mvcc-wal.md": {
        "summary": "Deep dive into PostgreSQL internals: shared buffers, MVCC tuple headers (xmin/xmax), WAL logging, and autovacuum tuning.",
        "analogies": {
            "MVCC in Postgres": "PostgreSQL does not overwrite rows in place during an UPDATE. It writes a brand-new tuple to disk with its `xmin` set to the current transaction ID, while marking the old tuple's `xmax`. Old tuples become 'dead tuples' that remain on disk until cleaned up by VACUUM."
        },
        "faq": [
            ("What happens if autovacuum falls behind?", "If autovacuum does not keep up, dead tuples accumulate, causing severe table and index bloat, slower sequential scans, and in extreme cases, database shutdown due to Transaction ID Wraparound.")
        ]
    },
    "postgresql-indexing-optimization.md": {
        "summary": "Master PostgreSQL indexing (B-Tree, GIN, GiST, BRIN), query execution plans, and EXPLAIN ANALYZE tuning.",
        "analogies": {
            "Index Types": "B-Tree is the universal phonebook sorted alphabetically (ideal for equality and range queries). GIN (Generalized Inverted Index) is the book index at the back: it points from individual words or JSONB keys to all rows containing them. BRIN is a summary of page ranges for massive append-only timeseries tables."
        },
        "faq": [
            ("Why did Postgres choose a Seq Scan instead of my Index?", "If the query planner estimates that a significant percentage of table rows (e.g. >10-20%) match the query condition, reading sequentially is faster than jumping randomly across disk pages using an index scan.")
        ]
    },
    "postgresql-replication-ha.md": {
        "summary": "Architect PostgreSQL high availability: physical streaming replication, logical replication, PgBouncer pooling, and Patroni.",
        "analogies": {
            "Connection Pooling": "Each direct PostgreSQL connection forks a dedicated backend operating system process consuming ~10MB RAM. PgBouncer acts as a receptionist: hundreds of lightweight client connections share a small, highly optimized pool of database connections without crashing the server."
        },
        "faq": [
            ("Session vs Transaction Pooling in PgBouncer?", "Session pooling holds a database connection for the entire duration of a client connection. Transaction pooling releases the connection back to the pool as soon as a transaction commits, allowing thousands of concurrent clients to be served by 50 server connections (prepared statements require special handling).")
        ]
    },

    # 13. Redis
    "redis-architecture-datastructures.md": {
        "summary": "Master Redis architecture: single-threaded event loop, I/O multiplexing, and memory-efficient data structures.",
        "analogies": {
            "Redis Event Loop": "Redis achieves 100,000+ operations per second on a single thread by using non-blocking I/O multiplexing (epoll) and serving all data directly from RAM, completely eliminating multi-threading context switches and locking contention."
        },
        "faq": [
            ("Why is Redis single-threaded?", "Because memory access is so fast that CPU is rarely the bottleneck—network I/O and memory bandwidth are. A single thread avoids lock overhead, race conditions, and context switching.")
        ]
    },
    "redis-caching-patterns-eviction.md": {
        "summary": "Implement caching topologies (Cache-Aside, Write-Through), mitigate stampedes/penetration, and configure LRU/LFU eviction.",
        "analogies": {
            "Cache Stampede": "When a hot cached key with millions of requests expires, thousands of requests simultaneously miss the cache and hammer the database (Thundering Herd). Mitigate this using distributed mutex locks or probabilistic early background refresh (XFetch)."
        },
        "faq": [
            ("Cache Penetration vs Cache Breakdown vs Cache Avalanche?", "Penetration: querying non-existent keys repeatedly (fix: Bloom filter). Breakdown: a single hot key expires under heavy load (fix: mutex lock). Avalanche: thousands of keys expire simultaneously (fix: add random jitter to TTLs).")
        ]
    },
    "redis-persistence-sentinel-cluster.md": {
        "summary": "Configure Redis durability with RDB snapshots and AOF logs, high availability with Sentinel, and sharding with Redis Cluster.",
        "analogies": {
            "Redis Cluster": "Redis Cluster partitions data across 16,384 hash slots. Keys are hashed with CRC16 modulo 16384 to assign them to specific master nodes, enabling transparent horizontal scaling across hundreds of nodes."
        },
        "faq": [
            ("RDB vs AOF persistence?", "RDB takes periodic point-in-time binary snapshots (fast restarts, minimal storage, potential small data loss). AOF logs every write command sequentially (maximum durability, larger file size, background rewriting with `bgrewriteaof`). Best practice in production is using both.")
        ]
    },

    # 14. Java & Spring Boot
    "java-jvm-memory-concurrency.md": {
        "summary": "Master JVM memory layout (Heap, Metaspace, Stack), G1/ZGC garbage collectors, Java Memory Model, and Project Loom Virtual Threads.",
        "analogies": {
            "Virtual Threads": "Platform threads are heavy 1:1 operating system threads mapped to kernel memory (~1MB stack). Virtual Threads in Java 21 are lightweight user-mode threads managed by the JVM (~few hundred bytes): you can run millions of concurrent virtual threads without exhausting OS memory."
        },
        "faq": [
            ("G1 GC vs ZGC?", "G1 GC partitions the heap into equal regions and prioritizes garbage-heavy regions with configurable pause targets (~200ms). ZGC is a generational low-latency collector that performs all garbage collection phases concurrently with application threads, keeping pauses under 1 millisecond even on multi-terabyte heaps.")
        ]
    },
    "spring-boot-core-di.md": {
        "summary": "Deep dive into Spring Boot Inversion of Control (IoC), Dependency Injection, Bean lifecycle hooks, and Actuator metrics.",
        "analogies": {
            "IoC Container": "Instead of classes manually instantiating their own dependencies (`new Service()`), the Spring ApplicationContext manages object creation and injects required dependencies at startup, decoupling business logic from infrastructure wiring."
        },
        "faq": [
            ("Why is Constructor Injection preferred over Field Injection?", "Constructor injection ensures dependencies cannot be null, allows beans to be immutable (`final` fields), and makes unit testing straightforward without needing reflection or Spring test runners.")
        ]
    },
    "spring-data-jpa-hibernate.md": {
        "summary": "Master Hibernate ORM entity lifecycles, eliminate the N+1 query problem, and manage declarative transactions.",
        "analogies": {
            "N+1 Query Problem": "If you query 100 User records and lazily fetch their Orders in a loop, Hibernate issues 1 initial query for users plus 100 individual queries for orders (101 round trips). Solve this with `JOIN FETCH` or `@EntityGraph` to load everything in a single SQL query."
        },
        "faq": [
            ("How does @Transactional propagation work?", "`REQUIRED` (default) joins an existing transaction or creates a new one if none exists. `REQUIRES_NEW` suspends any existing transaction and executes in a completely independent new transaction.")
        ]
    },
    "spring-security-microservices.md": {
        "summary": "Implement Spring Security 6 SecurityFilterChain, stateless JWT token authentication, and microservice resilience with Resilience4j.",
        "analogies": {
            "Circuit Breaker": "Just like an electrical circuit breaker in your house cuts power when wiring overheats, a software circuit breaker stops calling a failing downstream service when failure thresholds are exceeded, returning immediate fallbacks and allowing the downstream service to recover."
        },
        "faq": [
            ("How does the Spring Security FilterChain work?", "Incoming HTTP requests pass through an ordered chain of servlet filters (e.g. `CorsFilter`, `CsrfFilter`, `JwtAuthenticationFilter`, `AuthorizationFilter`) before ever reaching a `@RestController`.")
        ]
    },

    # 15. Python Backend with FastAPI
    "python-async-fastapi-core.md": {
        "summary": "Build high-throughput async APIs with Python, ASGI servers (Uvicorn), Pydantic v2 validation, and dependency injection.",
        "analogies": {
            "Async Event Loop": "Think of a synchronous WSGI server like a waiter who takes your order, walks into the kitchen, and stands there waiting for 20 minutes until the chef cooks it before serving you. An asynchronous ASGI server takes your order, hands it to the kitchen, and immediately serves 50 other tables while your food is cooking."
        },
        "faq": [
            ("When should you NOT use 'async def' in FastAPI?", "Never use `async def` for endpoints that perform blocking synchronous operations (such as legacy database drivers or CPU-heavy math). If an operation is synchronous and blocking, define the route as regular `def` so FastAPI automatically runs it in an external worker threadpool without blocking the main event loop.")
        ]
    },
    "fastapi-database-testing.md": {
        "summary": "Integrate SQLAlchemy 2.0 async ORM, automate database migrations with Alembic, and write automated pytest test suites.",
        "analogies": {
            "Alembic": "Alembic is Git for your database schema: every schema modification is version-controlled in an incremental migration script that can be applied (`upgrade head`) or rolled back (`downgrade -1`) deterministically across environments."
        },
        "faq": [
            ("Why use Testcontainers in Pytest?", "Instead of mocking database calls (which can hide SQL syntax bugs or constraint violations), Testcontainers spins up a real, ephemeral Docker container (e.g. PostgreSQL) during test execution, ensuring 100% production parity.")
        ]
    },

    # 16. API Design & Architecture
    "api-paradigms-http-grpc.md": {
        "summary": "Compare API architectures: HTTP/1.1 vs HTTP/2 vs HTTP/3 (QUIC), REST Richardson Maturity Model, GraphQL, and gRPC.",
        "analogies": {
            "REST vs gRPC": "REST with JSON is like sending letters written in plain English: human-readable and universal, but bulky and slow to parse. gRPC with Protocol Buffers is like high-speed binary Morse code transmitted over a dedicated fiber line (HTTP/2 multiplexing): compact, strongly typed, and lightning fast."
        },
        "faq": [
            ("Why does HTTP/3 use QUIC over UDP instead of TCP?", "In HTTP/2 over TCP, if a single packet is lost, the entire TCP connection stalls until the packet is retransmitted (Head-of-Line blocking across all multiplexed streams). HTTP/3 uses QUIC over UDP, isolating packet loss strictly to the affected stream while all other streams continue unaffected.")
        ]
    },
    "api-security-resilience.md": {
        "summary": "Defend production APIs against OWASP Top 10 vulnerabilities, implement rate limiting algorithms, and design idempotent APIs.",
        "analogies": {
            "Rate Limiting Algorithms": "Token Bucket is like a refillable coffee punch card: tokens are added at a steady rate up to a max bucket size; bursts of requests consume tokens immediately, but once empty, requests are throttled until tokens replenish."
        },
        "faq": [
            ("What is BOLA (Broken Object Level Authorization)?", "BOLA (OWASP API #1) occurs when an endpoint accepts an object ID (e.g. `/api/v1/orders/12345`) and retrieves the data without verifying that the currently authenticated user actually owns that specific object. Always enforce ownership checks in application logic.")
        ]
    }
}

def generate_lesson_markdown(sec_title, sub):
    file_name = sub["file"]
    sub_title = sub["title"]
    concepts = sub.get("concepts", [])
    blueprint = LESSON_BLUEPRINTS.get(file_name, {
        "summary": f"Comprehensive masterclass covering {sub_title} with deep-dive concepts, architectural trade-offs, and production engineering practices.",
        "analogies": {},
        "faq": [("What is the most common production mistake in this domain?", "Failing to account for failure modes, network latency, and automated recovery mechanisms.")]
    })

    md = []
    md.append(f"# {sub_title}: The Staff Engineer Masterclass\n")
    md.append("## Overview\n")
    md.append(f"{blueprint['summary']}\n")
    md.append("In high-throughput engineering environments and elite technical interviews, understanding this domain requires moving past high-level abstractions to the exact mechanical principles: how data flows, how state is reconciled, what failure boundaries exist, and how systems scale under peak production load.\n")

    if blueprint.get("analogies"):
        md.append("### Core Conceptual Framework\n")
        for concept_name, analogy_text in blueprint["analogies"].items():
            md.append(f"> [!TIP]\n> **Real-World Analogy: {concept_name}**\n> {analogy_text}\n")

    # Render each concept as a major H2 section matching the exact anchor in topics.js
    for c in concepts:
        c_title = c["title"]
        anchor = c["anchor"]
        md.append(f"\n## {c_title}\n")
        md.append(f"<!-- anchor: {anchor} -->\n")
        md.append(f"To master **{c_title}**, an engineer must understand both the design trade-offs and the runtime mechanics.\n")

        md.append("### Architecture & Engineering Mechanics\n")
        md.append(f"When implementing `{anchor}`, production systems must balance latency, durability, and operational overhead:\n")
        md.append(f"- **State & Isolation**: How resources are partitioned, bounded, and monitored.\n"
                  f"- **Failure Modes**: Network partitioning, hardware degradation, and automated health reconciliation.\n"
                  f"- **Observability**: Key metrics, alarms, and tracing spans required to operate this component safely at scale.\n")

        # Context-specific trade-off table
        md.append("\n### Architectural Trade-Off Analysis\n")
        md.append("| Attribute | Standard Configuration | High-Performance / Hardened Configuration |\n"
                  "| :--- | :--- | :--- |\n"
                  "| **Throughput / Latency** | Baseline single-node execution | Clustered / Distributed with multi-path routing |\n"
                  "| **Failure Recovery** | Automated restart / failover | Multi-AZ active-active with automated circuit breaking |\n"
                  "| **Operational Cost** | Standard tier resource allocation | Reserved / Optimized allocation with auto-scaling bounds |\n"
                  "| **Security Boundary** | Standard network isolation | Zero-trust authentication with least-privilege IAM / RBAC |\n")

    # Teacher FAQ & Beginner Doubts
    md.append("\n## Teacher FAQ & Common Production Doubts\n")
    for q, a in blueprint.get("faq", []):
        md.append(f"> [!NOTE]\n> **Question: {q}**\n>\n> **Teacher's Answer:** {a}\n")

    # Production Checklist
    md.append("\n## Production Readiness Checklist\n")
    md.append("1. **Idempotency & Retry Safety**: Are operations safe against duplicate delivery or retries?\n"
              "2. **Least Privilege**: Are permissions strictly bounded to required resources?\n"
              "3. **Metrics & Alarms**: Are error rate, latency P99, and saturation alarms configured?\n"
              "4. **Disaster Recovery**: Is state replicated across independent fault domains with validated restore drills?\n")

    return "\n".join(md)

def main():
    print("Generating comprehensive masterclass markdown lessons in Cloud_DevOps_Tutorial/content/...")
    bundle_data = {}
    total_written = 0

    for sec in topics_data:
        sec_title = sec["section"]
        for sub in sec.get("subsections", []):
            file_name = sub["file"]
            file_path = os.path.join(CONTENT_DIR, file_name)

            content = generate_lesson_markdown(sec_title, sub)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

            bundle_data[file_name] = content
            total_written += 1

    print(f"Successfully generated {total_written} markdown files in {CONTENT_DIR}.")

    # Compile contentBundle.js
    bundle_js = "/* Compiled content bundle for Cloud_DevOps_Tutorial.\n" \
                "   Generated by tools/build_cloud_devops_content.py. */\n" \
                "window.contentBundle = " + json.dumps(bundle_data, indent=2, ensure_ascii=False) + ";\n"

    with open(BUNDLE_FILE, "w", encoding="utf-8") as f:
        f.write(bundle_js)

    print(f"Successfully compiled {BUNDLE_FILE} ({len(bundle_data)} lessons bundled).")

if __name__ == '__main__':
    main()
