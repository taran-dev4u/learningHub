window.topicsData = [
  {
    "section": "1. AWS (Amazon Web Services) Masterclass",
    "subsections": [
      {
        "id": "aws-foundations-iam",
        "title": "AWS Foundations & Identity and Access Management (IAM)",
        "file": "aws-foundations-iam.md",
        "concepts": [
          {
            "title": "Cloud Computing Models (IaaS, PaaS, SaaS) & Shared Responsibility",
            "anchor": "cloud-computing-models-iaas-paas-saas-shared-responsibility"
          },
          {
            "title": "AWS Global Infrastructure: Regions, Availability Zones & Edge Locations",
            "anchor": "aws-global-infrastructure-regions-azs-edge-locations"
          },
          {
            "title": "IAM Fundamentals: Root User Security, IAM Users, Groups & Policies",
            "anchor": "iam-fundamentals-root-users-groups-policies"
          },
          {
            "title": "IAM Roles, Instance Profiles & STS AssumeRole Delegation",
            "anchor": "iam-roles-instance-profiles-sts-assumerole"
          },
          {
            "title": "Policy Evaluation Logic: Explicit Deny, SCPs & Permission Boundaries",
            "anchor": "policy-evaluation-logic-scps-permission-boundaries"
          }
        ]
      },
      {
        "id": "aws-networking-vpc",
        "title": "AWS VPC & Network Architecture",
        "file": "aws-networking-vpc.md",
        "concepts": [
          {
            "title": "VPC Fundamentals: CIDR Blocks, Public vs Private Subnets & Route Tables",
            "anchor": "vpc-fundamentals-cidr-blocks-subnets-route-tables"
          },
          {
            "title": "Internet Gateways (IGW), NAT Gateways & Egress-Only Gateways",
            "anchor": "internet-gateways-nat-gateways-egress-gateways"
          },
          {
            "title": "Security Groups (Stateful) vs Network ACLs (Stateless)",
            "anchor": "security-groups-vs-network-acls"
          },
          {
            "title": "VPC Peering, Transit Gateway & Direct Connect Hybrid Networking",
            "anchor": "vpc-peering-transit-gateway-direct-connect"
          },
          {
            "title": "VPC Endpoints (Gateway vs Interface PrivateLink Endpoints)",
            "anchor": "vpc-endpoints-gateway-vs-privatelink"
          }
        ]
      },
      {
        "id": "aws-compute-ec2",
        "title": "AWS Compute: EC2, Elastic Load Balancing & Auto Scaling",
        "file": "aws-compute-ec2.md",
        "concepts": [
          {
            "title": "EC2 Architecture: Instance Types, AMIs & User Data Bootstrap Scripts",
            "anchor": "ec2-architecture-instance-types-amis-userdata"
          },
          {
            "title": "EC2 Pricing Models: On-Demand, Savings Plans, Reserved & Spot Instances",
            "anchor": "ec2-pricing-models-reserved-spot-instances"
          },
          {
            "title": "Elastic Load Balancers: ALB (Layer 7) vs NLB (Layer 4) Architecture",
            "anchor": "elastic-load-balancers-alb-vs-nlb"
          },
          {
            "title": "Target Groups, Health Checks & Cross-Zone Load Balancing",
            "anchor": "target-groups-health-checks-cross-zone-balancing"
          },
          {
            "title": "Auto Scaling Groups (ASG): Launch Templates & Dynamic Scaling Policies",
            "anchor": "auto-scaling-groups-launch-templates-scaling-policies"
          }
        ]
      },
      {
        "id": "aws-storage-s3-ebs",
        "title": "AWS Storage: S3 Object Storage, EBS Block Storage & EFS",
        "file": "aws-storage-s3-ebs.md",
        "concepts": [
          {
            "title": "Amazon S3 Architecture: Buckets, Keys & Consistency Guarantees",
            "anchor": "amazon-s3-architecture-buckets-keys-consistency"
          },
          {
            "title": "S3 Storage Classes: Standard, Intelligent-Tiering, Glacier & Lifecycle Rules",
            "anchor": "s3-storage-classes-glacier-lifecycle-rules"
          },
          {
            "title": "S3 Security: Bucket Policies, Pre-Signed URLs, CORS & KMS Encryption",
            "anchor": "s3-security-bucket-policies-presigned-urls-encryption"
          },
          {
            "title": "EBS Volume Types: gp3 vs io2 Block Express & Snapshot Snapshots",
            "anchor": "ebs-volume-types-gp3-io2-snapshots"
          },
          {
            "title": "Amazon EFS Distributed Network File System & Amazon FSx for High Performance",
            "anchor": "amazon-efs-distributed-file-system-fsx"
          }
        ]
      },
      {
        "id": "aws-databases-nosql",
        "title": "AWS Databases: RDS, Aurora & DynamoDB",
        "file": "aws-databases-nosql.md",
        "concepts": [
          {
            "title": "Amazon RDS: Multi-AZ Synchronous Deployments vs Asynchronous Read Replicas",
            "anchor": "amazon-rds-multiaz-vs-read-replicas"
          },
          {
            "title": "Amazon Aurora: Storage Engine Architecture & Serverless v2",
            "anchor": "amazon-aurora-storage-engine-serverless-v2"
          },
          {
            "title": "DynamoDB Data Modeling: Partition Keys, Sort Keys & Access Patterns",
            "anchor": "dynamodb-data-modeling-partition-sort-keys"
          },
          {
            "title": "DynamoDB Global Secondary Indexes (GSI) vs Local Secondary Indexes (LSI)",
            "anchor": "dynamodb-gsi-vs-lsi-indexes"
          },
          {
            "title": "DynamoDB Streams, TTL & DAX In-Memory Acceleration",
            "anchor": "dynamodb-streams-ttl-dax-acceleration"
          }
        ]
      },
      {
        "id": "aws-containers-serverless",
        "title": "AWS Containers & Serverless: ECS, EKS, Lambda & API Gateway",
        "file": "aws-containers-serverless.md",
        "concepts": [
          {
            "title": "Amazon ECS: Task Definitions, Tasks, Services & EC2 vs Fargate",
            "anchor": "amazon-ecs-task-definitions-services-fargate"
          },
          {
            "title": "Amazon EKS: Managed Control Plane, Managed Node Groups & IRSA",
            "anchor": "amazon-eks-control-plane-nodegroups-irsa"
          },
          {
            "title": "AWS Lambda: Execution Lifecycle, Cold Starts, Layers & Concurrency Limits",
            "anchor": "aws-lambda-execution-lifecycle-cold-starts-concurrency"
          },
          {
            "title": "Amazon API Gateway: REST vs HTTP APIs, Authorizers & WebSocket APIs",
            "anchor": "amazon-api-gateway-rest-http-authorizers-websockets"
          },
          {
            "title": "AWS Step Functions & EventBridge Event-Driven Serverless Workflows",
            "anchor": "aws-step-functions-eventbridge-serverless-workflows"
          }
        ]
      },
      {
        "id": "aws-messaging-observability",
        "title": "AWS Messaging & Observability: SQS, SNS, CloudWatch & Route 53",
        "file": "aws-messaging-observability.md",
        "concepts": [
          {
            "title": "Amazon SQS: Standard vs FIFO Queues, Visibility Timeout & Dead-Letter Queues (DLQ)",
            "anchor": "amazon-sqs-standard-fifo-visibility-dlq"
          },
          {
            "title": "Amazon SNS: Pub/Sub Topics, Fan-Out Patterns & SMS/Email Delivery",
            "anchor": "amazon-sns-pubsub-topics-fanout-delivery"
          },
          {
            "title": "Amazon CloudWatch: Custom Metrics, Metric Alarms & CloudWatch Logs Insights",
            "anchor": "amazon-cloudwatch-metrics-alarms-logs-insights"
          },
          {
            "title": "AWS CloudTrail & AWS X-Ray: Audit Logging & Distributed Tracing",
            "anchor": "aws-cloudtrail-xray-auditing-distributed-tracing"
          },
          {
            "title": "Amazon Route 53: Hosted Zones, DNS Routing Policies & Health Checks",
            "anchor": "amazon-route-53-hosted-zones-routing-policies-healthchecks"
          },
          {
            "title": "Amazon CloudFront: CDN Edge Caching, Origins, OAC & Lambda@Edge",
            "anchor": "amazon-cloudfront-cdn-edge-caching-oac-lambda-edge"
          }
        ]
      }
    ]
  },
  {
    "section": "2. Microsoft Azure Masterclass",
    "subsections": [
      {
        "id": "azure-foundations-entra",
        "title": "Azure Foundations, Resource Governance & Entra ID",
        "file": "azure-foundations-entra.md",
        "concepts": [
          {
            "title": "Azure Resource Hierarchy: Management Groups, Subscriptions & Resource Groups",
            "anchor": "azure-resource-hierarchy-management-groups-subscriptions"
          },
          {
            "title": "Azure Entra ID (Azure AD): Users, Groups, Service Principals & RBAC",
            "anchor": "azure-entra-id-users-groups-service-principals-rbac"
          },
          {
            "title": "Managed Identities: System-Assigned vs User-Assigned Identities",
            "anchor": "managed-identities-system-assigned-vs-user-assigned"
          },
          {
            "title": "Azure Policy, Blueprints & Resource Locks for Cloud Governance",
            "anchor": "azure-policy-blueprints-resource-locks"
          }
        ]
      },
      {
        "id": "azure-compute-networking",
        "title": "Azure Compute & Virtual Networks (VNets)",
        "file": "azure-compute-networking.md",
        "concepts": [
          {
            "title": "Azure Virtual Machines (VMs), Availability Sets & VM Scale Sets (VMSS)",
            "anchor": "azure-vms-availability-sets-vm-scale-sets"
          },
          {
            "title": "Azure Virtual Network (VNet) Architecture, Subnets & Peering",
            "anchor": "azure-vnet-architecture-subnets-peering"
          },
          {
            "title": "Network Security Groups (NSGs) & Application Security Groups (ASGs)",
            "anchor": "network-security-groups-nsgs-application-security-groups"
          },
          {
            "title": "Azure Load Balancer (Layer 4) vs Application Gateway (Layer 7 WAF)",
            "anchor": "azure-load-balancer-vs-application-gateway"
          },
          {
            "title": "Azure App Service, Consumption Plans & Azure Functions Serverless",
            "anchor": "azure-app-service-azure-functions-serverless"
          }
        ]
      },
      {
        "id": "azure-storage-databases",
        "title": "Azure Storage, Azure SQL & Cosmos DB",
        "file": "azure-storage-databases.md",
        "concepts": [
          {
            "title": "Azure Blob Storage: Hot, Cool, Cold, Archive Access Tiers & Lifecycle Management",
            "anchor": "azure-blob-storage-hot-cool-archive-tiers"
          },
          {
            "title": "Azure Data Lake Storage Gen2 (ADLS) & Hierarchical Namespaces",
            "anchor": "azure-data-lake-storage-gen2-adls"
          },
          {
            "title": "Azure SQL Database: Single DB, Elastic Pools & SQL Managed Instances",
            "anchor": "azure-sql-database-elastic-pools-managed-instances"
          },
          {
            "title": "Azure Cosmos DB: Multi-Model API & Global Data Distribution",
            "anchor": "azure-cosmos-db-multimodel-global-distribution"
          },
          {
            "title": "Cosmos DB Consistency Levels: Strong, Bounded Staleness, Session, Consistent Prefix & Eventual",
            "anchor": "cosmos-db-five-consistency-levels-explained"
          }
        ]
      },
      {
        "id": "azure-containers-monitoring",
        "title": "Azure Containers, Messaging & Observability",
        "file": "azure-containers-monitoring.md",
        "concepts": [
          {
            "title": "Azure Kubernetes Service (AKS): Architecture, Node Pools & Azure CNI",
            "anchor": "azure-kubernetes-service-aks-nodepools-cni"
          },
          {
            "title": "Azure Container Apps (ACA) & Microservices with KEDA Autoscaling",
            "anchor": "azure-container-apps-keda-microservices"
          },
          {
            "title": "Azure Service Bus: Queues, Topics, Subscriptions & Dead-Lettering",
            "anchor": "azure-service-bus-queues-topics-deadletter"
          },
          {
            "title": "Azure Event Grid & Event Hubs for Reactive Messaging and Streaming",
            "anchor": "azure-event-grid-event-hubs-streaming"
          },
          {
            "title": "Azure Monitor, Log Analytics (KQL) & Application Insights APM",
            "anchor": "azure-monitor-log-analytics-kql-application-insights"
          }
        ]
      }
    ]
  },
  {
    "section": "3. Google Cloud Platform (GCP) Masterclass",
    "subsections": [
      {
        "id": "gcp-foundations-iam-vpc",
        "title": "GCP Resource Hierarchy, Cloud IAM & Global VPC",
        "file": "gcp-foundations-iam-vpc.md",
        "concepts": [
          {
            "title": "GCP Resource Hierarchy: Organizations, Folders, Projects & Service Accounts",
            "anchor": "gcp-resource-hierarchy-organizations-folders-projects"
          },
          {
            "title": "GCP Cloud IAM: Predefined Roles, Custom Roles & Workload Identity Federation",
            "anchor": "gcp-cloud-iam-roles-workload-identity-federation"
          },
          {
            "title": "GCP Global VPC: Subnets, Shared VPC & VPC Network Peering",
            "anchor": "gcp-global-vpc-shared-vpc-network-peering"
          },
          {
            "title": "Cloud Load Balancing: Global HTTP(S) Load Balancing & Cloud CDN",
            "anchor": "gcp-cloud-load-balancing-global-https-cdn"
          }
        ]
      },
      {
        "id": "gcp-compute-containers",
        "title": "GCP Compute Engine, GKE & Cloud Run",
        "file": "gcp-compute-containers.md",
        "concepts": [
          {
            "title": "Compute Engine: VMs, Managed Instance Groups (MIGs) & Preemptible Spot VMs",
            "anchor": "gcp-compute-engine-vms-migs-spot-instances"
          },
          {
            "title": "Google Kubernetes Engine (GKE): Standard vs Autopilot Clusters",
            "anchor": "google-kubernetes-engine-gke-standard-vs-autopilot"
          },
          {
            "title": "Cloud Run: Fully Managed Serverless Containers with Scale-to-Zero",
            "anchor": "gcp-cloud-run-serverless-containers-scaletozero"
          },
          {
            "title": "Cloud Functions Gen 2 & Eventarc Event-Driven Architecture",
            "anchor": "gcp-cloud-functions-gen2-eventarc"
          }
        ]
      },
      {
        "id": "gcp-storage-databases",
        "title": "GCP Storage, Cloud Spanner & Big Data",
        "file": "gcp-storage-databases.md",
        "concepts": [
          {
            "title": "Google Cloud Storage (GCS): Standard, Nearline, Coldline, Archive Tiers",
            "anchor": "google-cloud-storage-gcs-storage-tiers"
          },
          {
            "title": "Cloud SQL (Managed Postgres/MySQL) vs Memorystore for Redis",
            "anchor": "gcp-cloud-sql-vs-memorystore-redis"
          },
          {
            "title": "Cloud Spanner: Globally Distributed Relational DB with TrueTime Atomic Clocks",
            "anchor": "gcp-cloud-spanner-distributed-relational-truetime"
          },
          {
            "title": "Cloud Bigtable: High-Throughput NoSQL Wide-Column Engine",
            "anchor": "gcp-cloud-bigtable-nosql-wide-column-engine"
          },
          {
            "title": "BigQuery: Serverless Columnar Data Warehouse & SQL Analytics",
            "anchor": "gcp-bigquery-serverless-columnar-warehouse-sql"
          },
          {
            "title": "Cloud Pub/Sub Distributed Messaging & Cloud Monitoring Observability",
            "anchor": "gcp-cloud-pubsub-messaging-cloud-monitoring"
          }
        ]
      }
    ]
  },
  {
    "section": "4. Linux & Terminal Power Engineering",
    "subsections": [
      {
        "id": "linux-filesystem-permissions",
        "title": "Linux Filesystem Hierarchy & Advanced Permissions",
        "file": "linux-filesystem-permissions.md",
        "concepts": [
          {
            "title": "Linux Filesystem Hierarchy Standard (FHS): /etc, /var, /proc, /sys & /dev",
            "anchor": "linux-filesystem-hierarchy-standard-fhs"
          },
          {
            "title": "File Permissions: Symbolic vs Octal chmod, chown, chgrp & umask",
            "anchor": "file-permissions-symbolic-octal-chmod-chown-umask"
          },
          {
            "title": "Special Permissions: SUID, SGID & Sticky Bit Implementation",
            "anchor": "special-permissions-suid-sgid-sticky-bit"
          },
          {
            "title": "POSIX Access Control Lists (ACLs): getfacl and setfacl Management",
            "anchor": "posix-access-control-lists-getfacl-setfacl"
          }
        ]
      },
      {
        "id": "linux-process-performance",
        "title": "Linux Process Management & System Diagnostics",
        "file": "linux-process-performance.md",
        "concepts": [
          {
            "title": "Process Lifecycle: ps, top, htop, pstree & Signals (SIGTERM, SIGKILL)",
            "anchor": "process-lifecycle-ps-top-htop-signals"
          },
          {
            "title": "CPU Diagnostics: Load Averages, uptime, vmstat & mpstat Analysis",
            "anchor": "cpu-diagnostics-load-averages-uptime-vmstat"
          },
          {
            "title": "Memory Diagnostics: free, Buffer vs Cache, Swapping & the OOM Killer",
            "anchor": "memory-diagnostics-free-buffer-cache-oom-killer"
          },
          {
            "title": "Disk I/O & Networking Diagnostics: iostat, df, du, ss, netstat, lsof & tcpdump",
            "anchor": "disk-io-networking-diagnostics-iostat-ss-lsof"
          }
        ]
      },
      {
        "id": "linux-text-bash-scripting",
        "title": "Text Processing, Pipelines & Bash Automation",
        "file": "linux-text-bash-scripting.md",
        "concepts": [
          {
            "title": "I/O Redirection, Pipes (|), tee, and xargs Command Processing",
            "anchor": "io-redirection-pipes-tee-xargs"
          },
          {
            "title": "Text Manipulation Powerhouses: grep, sed Regular Expressions & awk Field Processing",
            "anchor": "text-manipulation-grep-sed-awk"
          },
          {
            "title": "Robust Bash Scripting: Error Traps (set -euo pipefail), Functions & Conditionals",
            "anchor": "robust-bash-scripting-error-trapping-functions"
          },
          {
            "title": "Linux Service Management: systemd Units, systemctl & journalctl Logs",
            "anchor": "linux-service-management-systemd-systemctl-journalctl"
          }
        ]
      }
    ]
  },
  {
    "section": "5. Git & GitHub Architecture",
    "subsections": [
      {
        "id": "git-architecture-internals",
        "title": "Git Architecture & Internal Mechanics",
        "file": "git-architecture-internals.md",
        "concepts": [
          {
            "title": "Git Object Model: Blobs, Trees, Commits & Annotated Tags in .git/objects",
            "anchor": "git-object-model-blobs-trees-commits-tags"
          },
          {
            "title": "The Three Trees: Working Directory, Staging Area (Index) & Git Repository",
            "anchor": "the-three-trees-working-directory-index-repository"
          },
          {
            "title": "Git Diff Internals: Working vs Staging vs HEAD",
            "anchor": "git-diff-internals-working-staging-head"
          },
          {
            "title": "Atomic Commits, git add -p Patch Staging & Commit Hygiene",
            "anchor": "atomic-commits-git-add-patch-hygiene"
          }
        ]
      },
      {
        "id": "git-branching-rebasing",
        "title": "Branching Strategies, Merging & Interactive Rebasing",
        "file": "git-branching-rebasing.md",
        "concepts": [
          {
            "title": "Branching Workflows: Trunk-Based Development vs GitFlow",
            "anchor": "branching-workflows-trunk-based-vs-gitflow"
          },
          {
            "title": "Merge Mechanics: Fast-Forward Merges vs True 3-Way Merge Commits",
            "anchor": "merge-mechanics-fastforward-vs-3way-merges"
          },
          {
            "title": "Interactive Rebasing (git rebase -i): Squash, Reword, Edit & Drop",
            "anchor": "interactive-rebasing-squash-reword-drop"
          },
          {
            "title": "Merge vs Rebase Trade-Offs & Safe Force Pushing (git push --force-with-lease)",
            "anchor": "merge-vs-rebase-tradeoffs-force-with-lease"
          }
        ]
      },
      {
        "id": "git-advanced-reflog-bisect",
        "title": "Advanced Git: Reflog, Bisect, Cherry-Pick & Worktrees",
        "file": "git-advanced-reflog-bisect.md",
        "concepts": [
          {
            "title": "Git Reflog: Recovering 'Lost' Commits, Deleted Branches & Broken Rebases",
            "anchor": "git-reflog-recovering-lost-commits-deleted-branches"
          },
          {
            "title": "Git Reset (--soft, --mixed, --hard) vs Git Revert",
            "anchor": "git-reset-soft-mixed-hard-vs-revert"
          },
          {
            "title": "Git Bisect: Binary Searching History to Pinpoint Regressions",
            "anchor": "git-bisect-binary-search-bug-pinpointing"
          },
          {
            "title": "Git Cherry-Pick & Git Worktrees for Isolated Multi-Branch Working",
            "anchor": "git-cherry-pick-worktrees-multi-branch-isolation"
          },
          {
            "title": "Git Hooks: Client-Side (pre-commit, commit-msg) & Server-Side Enforcement",
            "anchor": "git-hooks-pre-commit-server-side-enforcement"
          }
        ]
      },
      {
        "id": "github-collaboration-actions",
        "title": "GitHub Enterprise Collaboration & CI/CD Actions",
        "file": "github-collaboration-actions.md",
        "concepts": [
          {
            "title": "Enterprise Pull Requests: Branch Protection Rules, Required Checks & CODEOWNERS",
            "anchor": "pull-requests-branch-protection-required-checks-codeowners"
          },
          {
            "title": "GitHub Actions Core: Workflows, Jobs, Steps, Matrix Strategy & Runners",
            "anchor": "github-actions-workflows-jobs-steps-matrix-runners"
          },
          {
            "title": "Security & Secrets: Encrypted Secrets, Environment Gates & OIDC Cloud Auth",
            "anchor": "github-actions-secrets-environments-oidc-cloud-auth"
          },
          {
            "title": "Artifacts & Dependency Caching (actions/cache, actions/upload-artifact)",
            "anchor": "github-actions-artifacts-dependency-caching"
          }
        ]
      }
    ]
  },
  {
    "section": "6. Docker & Containerization Deep-Dive",
    "subsections": [
      {
        "id": "docker-architecture-engine",
        "title": "Container Architecture & Linux Kernel Primitives",
        "file": "docker-architecture-engine.md",
        "concepts": [
          {
            "title": "Linux Kernel Primitives: Namespaces (PID, NET, MNT, IPC, UTS, USER) & cgroups",
            "anchor": "linux-kernel-primitives-namespaces-cgroups"
          },
          {
            "title": "Union File Systems & Copy-on-Write (OverlayFS Mechanics)",
            "anchor": "union-file-systems-overlayfs-copy-on-write"
          },
          {
            "title": "Docker Engine Architecture: dockerd, containerd, runc & OCI Specifications",
            "anchor": "docker-engine-dockerd-containerd-runc-oci"
          },
          {
            "title": "Containers vs Virtual Machines: Resource Isolation & Overhead Comparison",
            "anchor": "containers-vs-virtual-machines-isolation-overhead"
          }
        ]
      },
      {
        "id": "dockerfile-image-optimization",
        "title": "Dockerfile Optimization & Production Security",
        "file": "dockerfile-image-optimization.md",
        "concepts": [
          {
            "title": "Dockerfile Directives: ENTRYPOINT vs CMD, RUN vs COPY vs ADD",
            "anchor": "dockerfile-directives-entrypoint-cmd-run-copy"
          },
          {
            "title": "Multi-Stage Builds: Minimizing Final Image Attack Surface and Size",
            "anchor": "multi-stage-builds-image-size-attack-surface-reduction"
          },
          {
            "title": "Layer Caching Strategies & Ordering Directives for Instant Builds",
            "anchor": "layer-caching-strategies-command-ordering"
          },
          {
            "title": "Container Security: Non-Root Execution, Distroless Images & Vulnerability Scanning",
            "anchor": "container-security-non-root-distroless-vulnerability-scanning"
          }
        ]
      },
      {
        "id": "docker-networking-volumes",
        "title": "Docker Networking, Storage & Multi-Container Compose",
        "file": "docker-networking-volumes.md",
        "concepts": [
          {
            "title": "Docker Networking Drivers: Bridge, Host, Overlay & Macvlan",
            "anchor": "docker-networking-drivers-bridge-host-overlay"
          },
          {
            "title": "Docker Storage: Named Volumes, Bind Mounts, tmpfs & Volume Drivers",
            "anchor": "docker-storage-named-volumes-bind-mounts-tmpfs"
          },
          {
            "title": "Docker Compose: Service Orchestration, depends_on Conditions & Healthchecks",
            "anchor": "docker-compose-orchestration-healthchecks-networking"
          }
        ]
      }
    ]
  },
  {
    "section": "7. Kubernetes (K8s) Container Orchestration",
    "subsections": [
      {
        "id": "k8s-architecture-control-plane",
        "title": "Kubernetes Architecture & Control Plane Internals",
        "file": "k8s-architecture-control-plane.md",
        "concepts": [
          {
            "title": "Control Plane Architecture: kube-apiserver, etcd Quorum, kube-scheduler & Controllers",
            "anchor": "control-plane-architecture-apiserver-etcd-scheduler-controllers"
          },
          {
            "title": "Worker Node Architecture: Kubelet, kube-proxy & Container Runtime Interface (CRI)",
            "anchor": "worker-node-architecture-kubelet-kubeproxy-cri"
          },
          {
            "title": "Declarative Object Model: Desired State vs Actual State Reconciliation Loop",
            "anchor": "declarative-object-model-reconciliation-loop"
          },
          {
            "title": "kubectl Architecture, Contexts & Authentication Flow",
            "anchor": "kubectl-architecture-contexts-auth-flow"
          }
        ]
      },
      {
        "id": "k8s-workloads-pods-deployments",
        "title": "Workload Management: Pods, Deployments & Rollouts",
        "file": "k8s-workloads-pods-deployments.md",
        "concepts": [
          {
            "title": "Pod Lifecycle & Anatomy: Multi-Container Patterns (Sidecar, Init Containers)",
            "anchor": "pod-lifecycle-anatomy-sidecar-init-containers"
          },
          {
            "title": "Deployments & ReplicaSets: Managing Replicated Pod Workloads",
            "anchor": "deployments-replicasets-replicated-workloads"
          },
          {
            "title": "Rolling Updates, Rollbacks & Deployment Strategies (maxSurge, maxUnavailable)",
            "anchor": "rolling-updates-rollbacks-maxsurge-maxunavailable"
          },
          {
            "title": "Probes: Liveness, Readiness & Startup Probes Configuration",
            "anchor": "probes-liveness-readiness-startup-probes"
          }
        ]
      },
      {
        "id": "k8s-stateful-daemon-jobs",
        "title": "Advanced Workloads: StatefulSets, DaemonSets & Batch Jobs",
        "file": "k8s-stateful-daemon-jobs.md",
        "concepts": [
          {
            "title": "StatefulSets: Stable Network Identities, Ordered Deployment & Volume Claims",
            "anchor": "statefulsets-stable-network-identities-ordered-deployment"
          },
          {
            "title": "DaemonSets: Running Pods Across Every Node (Logging, Monitoring Agents)",
            "anchor": "daemonsets-node-level-agents-logging-monitoring"
          },
          {
            "title": "Batch Processing: Kubernetes Jobs & Scheduled CronJobs",
            "anchor": "batch-processing-kubernetes-jobs-cronjobs"
          }
        ]
      },
      {
        "id": "k8s-networking-services-ingress",
        "title": "Kubernetes Networking, Services & Ingress Controllers",
        "file": "k8s-networking-services-ingress.md",
        "concepts": [
          {
            "title": "Cluster Networking Model: Pod-to-Pod Flat Network & CNI Plugins (Calico, Cilium)",
            "anchor": "cluster-networking-model-cni-calico-cilium"
          },
          {
            "title": "Services: ClusterIP (Internal), NodePort, LoadBalancer & Headless Services",
            "anchor": "kubernetes-services-clusterip-nodeport-loadbalancer-headless"
          },
          {
            "title": "Ingress Controllers (Nginx Ingress, Traefik) & Path-Based Traffic Routing",
            "anchor": "ingress-controllers-nginx-traefik-path-routing"
          },
          {
            "title": "Kubernetes Gateway API: Modern HTTPRoute & GRPCRoute Architecture",
            "anchor": "kubernetes-gateway-api-httproute-grpcroute"
          }
        ]
      },
      {
        "id": "k8s-config-storage-helm",
        "title": "Configuration, Storage, Security & Helm Packaging",
        "file": "k8s-config-storage-helm.md",
        "concepts": [
          {
            "title": "ConfigMaps & Secrets: Environment Variables, Volume Projections & SealedSecrets",
            "anchor": "configmaps-secrets-projections-sealedsecrets"
          },
          {
            "title": "Storage: PersistentVolumes (PV), PersistentVolumeClaims (PVC) & StorageClasses (CSI)",
            "anchor": "kubernetes-storage-pv-pvc-storageclasses-csi"
          },
          {
            "title": "Resource Management: Requests, Limits, QoS Classes & Horizontal Pod Autoscaler (HPA)",
            "anchor": "resource-management-requests-limits-qos-hpa"
          },
          {
            "title": "Cluster Security: Namespaces, ResourceQuotas & RBAC (Roles, RoleBindings)",
            "anchor": "cluster-security-namespaces-resourcequotas-rbac"
          },
          {
            "title": "Helm Package Manager: Charts, Values, Templates & Release Lifecycle",
            "anchor": "helm-package-manager-charts-values-templates-releases"
          }
        ]
      }
    ]
  },
  {
    "section": "8. Infrastructure as Code (IaC) with Terraform",
    "subsections": [
      {
        "id": "terraform-hcl-syntax",
        "title": "Terraform Core, HCL Syntax & Workflow",
        "file": "terraform-hcl-syntax.md",
        "concepts": [
          {
            "title": "IaC Declarative Paradigm: Desired State vs Imperative Scripting",
            "anchor": "iac-declarative-paradigm-vs-imperative-scripting"
          },
          {
            "title": "HCL Syntax: Providers, Resources, Variables, Locals & Outputs",
            "anchor": "hcl-syntax-providers-resources-variables-locals-outputs"
          },
          {
            "title": "The Terraform Workflow: terraform init, plan, apply & destroy",
            "anchor": "terraform-workflow-init-plan-apply-destroy"
          },
          {
            "title": "Resource Dependencies: Implicit vs Explicit (depends_on) Dependency Graphs",
            "anchor": "resource-dependencies-implicit-vs-explicit-graphs"
          }
        ]
      },
      {
        "id": "terraform-state-management",
        "title": "Terraform State Management & Remote Backends",
        "file": "terraform-state-management.md",
        "concepts": [
          {
            "title": "Terraform State: terraform.tfstate Internal Structure & Drift Detection",
            "anchor": "terraform-state-internal-structure-drift-detection"
          },
          {
            "title": "Remote Backends: S3 Backend with DynamoDB Distributed State Locking",
            "anchor": "remote-backends-s3-dynamodb-state-locking"
          },
          {
            "title": "State Manipulation: terraform state list, show, mv, rm & import",
            "anchor": "state-manipulation-state-list-show-mv-import"
          },
          {
            "title": "Protecting Sensitive Data in Terraform State & Environment Workspaces",
            "anchor": "protecting-sensitive-data-state-workspaces"
          }
        ]
      },
      {
        "id": "terraform-modules-workspaces",
        "title": "Reusable Modules, Loops & Advanced IaC Patterns",
        "file": "terraform-modules-workspaces.md",
        "concepts": [
          {
            "title": "Terraform Modules: Root vs Child Modules, Input Variables & Output Contracts",
            "anchor": "terraform-modules-root-vs-child-contracts"
          },
          {
            "title": "Meta-Arguments: count vs for_each & Dynamic Blocks Construction",
            "anchor": "meta-arguments-count-vs-for-each-dynamic-blocks"
          },
          {
            "title": "Data Sources: Dynamically Querying Existing Infrastructure State",
            "anchor": "data-sources-dynamically-querying-existing-state"
          },
          {
            "title": "Resource Lifecycle Hooks: create_before_destroy, prevent_destroy & ignore_changes",
            "anchor": "resource-lifecycle-hooks-create-before-destroy-ignore-changes"
          }
        ]
      }
    ]
  },
  {
    "section": "9. CI/CD Pipelines & DevOps Automation",
    "subsections": [
      {
        "id": "cicd-principles-deployment",
        "title": "CI/CD Principles & Modern Deployment Strategies",
        "file": "cicd-principles-deployment.md",
        "concepts": [
          {
            "title": "Continuous Integration vs Continuous Delivery vs Continuous Deployment",
            "anchor": "ci-vs-cd-vs-continuous-deployment"
          },
          {
            "title": "Blue/Green Deployments: Zero-Downtime Environment Switching",
            "anchor": "blue-green-deployments-zerodowntime-switching"
          },
          {
            "title": "Canary Releases: Incremental Traffic Shifting & Automated Rollbacks",
            "anchor": "canary-releases-incremental-traffic-shifting"
          },
          {
            "title": "Rolling Deployments, Recreate Strategies & Feature Flag Driven Releases",
            "anchor": "rolling-deployments-recreate-strategies-feature-flags"
          }
        ]
      },
      {
        "id": "github-actions-enterprise",
        "title": "Enterprise GitHub Actions CI/CD Architecture",
        "file": "github-actions-enterprise.md",
        "concepts": [
          {
            "title": "Workflow Pipelines: Automated Linting, Unit Testing & Security Scans (SAST)",
            "anchor": "workflow-pipelines-linting-unit-testing-sast"
          },
          {
            "title": "Docker Multi-Stage Build & Push to Container Registries (GHCR / Docker Hub)",
            "anchor": "docker-build-push-container-registries-ghcr"
          },
          {
            "title": "Secretless Cloud Authentication: AWS/Azure OIDC Integration in GitHub Actions",
            "anchor": "secretless-cloud-auth-oidc-integration"
          },
          {
            "title": "Reusable Workflows, Composite Actions & Self-Hosted Runners",
            "anchor": "reusable-workflows-composite-actions-self-hosted-runners"
          }
        ]
      },
      {
        "id": "jenkins-pipelines",
        "title": "Jenkins Pipelines & GitOps Delivery",
        "file": "jenkins-pipelines.md",
        "concepts": [
          {
            "title": "Jenkins Architecture: Controller-Agent Topology & Distributed Builds",
            "anchor": "jenkins-architecture-controller-agent-topology"
          },
          {
            "title": "Declarative Jenkinsfile: Stages, Parallel Steps, Post Conditions & Agent Directives",
            "anchor": "declarative-jenkinsfile-stages-parallel-post-conditions"
          },
          {
            "title": "Artifact Management: Storing Releases in JFrog Artifactory & Nexus",
            "anchor": "artifact-management-jfrog-artifactory-nexus"
          },
          {
            "title": "GitOps with ArgoCD: Declarative Continuous Delivery for Kubernetes Clusters",
            "anchor": "gitops-with-argocd-declarative-continuous-delivery"
          }
        ]
      }
    ]
  },
  {
    "section": "10. Apache Kafka Distributed Streaming",
    "subsections": [
      {
        "id": "kafka-architecture-kraft",
        "title": "Kafka Architecture, Commit Log & KRaft Quorum",
        "file": "kafka-architecture-kraft.md",
        "concepts": [
          {
            "title": "Distributed Commit Log: Append-Only Immutable Records & Sequential Disk I/O",
            "anchor": "distributed-commit-log-append-only-records-sequential-io"
          },
          {
            "title": "Kafka Broker Architecture & Page Cache Zero-Copy Sendfile System Calls",
            "anchor": "kafka-broker-architecture-pagecache-zerocopy"
          },
          {
            "title": "ZooKeeper Elimination & KRaft (Kafka Raft Metadata Mode) Architecture",
            "anchor": "zookeeper-elimination-kraft-metadata-mode"
          }
        ]
      },
      {
        "id": "kafka-topics-partitions-producers",
        "title": "Topics, Partitions, Producers & Delivery Guarantees",
        "file": "kafka-topics-partitions-producers.md",
        "concepts": [
          {
            "title": "Topics & Partitions: Sharding, Concurrency & Strict Ordering Guarantees",
            "anchor": "topics-partitions-sharding-concurrency-ordering"
          },
          {
            "title": "Log Segments, Retention Policies (Time, Size) & Log Compaction",
            "anchor": "log-segments-retention-policies-log-compaction"
          },
          {
            "title": "Producer Mechanics: Partitioners, Batching (linger.ms), Compression & acks=all",
            "anchor": "producer-mechanics-partitioners-batching-acks"
          },
          {
            "title": "Idempotent Producers & Exactly-Once Semantics (EOS) with Transaction Coordinator",
            "anchor": "idempotent-producers-exactly-once-semantics-eos"
          }
        ]
      },
      {
        "id": "kafka-consumers-offset-management",
        "title": "Consumer Groups, Partition Rebalancing & Offsets",
        "file": "kafka-consumers-offset-management.md",
        "concepts": [
          {
            "title": "Consumer Groups: Scalable Parallel Processing & Partition Assignment Strategies",
            "anchor": "consumer-groups-parallel-processing-partition-assignment"
          },
          {
            "title": "Partition Rebalancing: Eager vs Cooperative Sticky Rebalance Protocols",
            "anchor": "partition-rebalancing-eager-vs-cooperative-sticky"
          },
          {
            "title": "Offset Commit Strategies: Automatic vs Manual (commitSync vs commitAsync)",
            "anchor": "offset-commit-strategies-automatic-vs-manual"
          },
          {
            "title": "Handling Poison Pills: Dead-Letter Queues (DLQ) & Consumer Retry Topics",
            "anchor": "poison-pills-dead-letter-queues-consumer-retry-topics"
          }
        ]
      },
      {
        "id": "kafka-ecosystem-connect-streams",
        "title": "Kafka Ecosystem: Schema Registry, Connect & Streams",
        "file": "kafka-ecosystem-connect-streams.md",
        "concepts": [
          {
            "title": "Schema Registry: Avro / Protobuf Data Serialization & Schema Evolution",
            "anchor": "schema-registry-avro-protobuf-schema-evolution"
          },
          {
            "title": "Kafka Connect: Source and Sink Connectors for Declarative Data Pipelines",
            "anchor": "kafka-connect-source-sink-declarative-pipelines"
          },
          {
            "title": "Kafka Streams: KStream, KTable, Stateful Processing, Windowing & RocksDB State",
            "anchor": "kafka-streams-kstream-ktable-stateful-processing-rocksdb"
          }
        ]
      }
    ]
  },
  {
    "section": "11. Apache Spark Big Data Engine",
    "subsections": [
      {
        "id": "spark-architecture-execution",
        "title": "Spark Architecture, Cluster Topologies & DAG Engine",
        "file": "spark-architecture-execution.md",
        "concepts": [
          {
            "title": "Spark Cluster Architecture: Driver Program, Cluster Manager (K8s/YARN) & Executors",
            "anchor": "spark-cluster-architecture-driver-executors"
          },
          {
            "title": "Job Execution Lifecycle: Jobs, Stages, Tasks & DAGScheduler Graph Construction",
            "anchor": "job-execution-lifecycle-stages-tasks-dagscheduler"
          },
          {
            "title": "Narrow vs Wide Dependencies & Shuffle Boundary Triggering",
            "anchor": "narrow-vs-wide-dependencies-shuffle-boundary"
          }
        ]
      },
      {
        "id": "spark-rdds-transformations-actions",
        "title": "Resilient Distributed Datasets (RDDs) & Lineage",
        "file": "spark-rdds-transformations-actions.md",
        "concepts": [
          {
            "title": "RDD Fundamentals: Immutability, Partitioning & Deterministic Lineage Graphs",
            "anchor": "rdd-fundamentals-immutability-partitioning-lineage"
          },
          {
            "title": "Transformations (Lazy) vs Actions (Eager): map, filter vs reduceByKey, collect",
            "anchor": "transformations-lazy-vs-actions-eager"
          },
          {
            "title": "Fault Tolerance: Lineage Graph Recomputation vs RDD Checkpointing",
            "anchor": "fault-tolerance-lineage-recomputation-checkpointing"
          }
        ]
      },
      {
        "id": "spark-dataframes-catalyst",
        "title": "Spark DataFrames, Datasets & Catalyst Optimization",
        "file": "spark-dataframes-catalyst.md",
        "concepts": [
          {
            "title": "DataFrames & Spark SQL: Schema Enforced Structured Big Data Processing",
            "anchor": "dataframes-spark-sql-structured-data-processing"
          },
          {
            "title": "Catalyst Optimizer: Analysis, Logical Optimization, Physical Planning & Code Gen",
            "anchor": "catalyst-optimizer-analysis-logical-physical-planning"
          },
          {
            "title": "Tungsten Execution Engine: Off-Heap Binary Memory Management & Whole-Stage Codegen",
            "anchor": "tungsten-engine-off-heap-binary-memory-whole-stage-codegen"
          }
        ]
      },
      {
        "id": "spark-streaming-performance",
        "title": "Shuffle Optimization, Memory Tuning & Structured Streaming",
        "file": "spark-streaming-performance.md",
        "concepts": [
          {
            "title": "Shuffle Optimization: Partition Tuning (spark.sql.shuffle.partitions) & Broadcast Joins",
            "anchor": "shuffle-optimization-partition-tuning-broadcast-joins"
          },
          {
            "title": "Spark Memory Management: Storage Memory vs Execution Memory & Spilling",
            "anchor": "spark-memory-management-storage-vs-execution-spilling"
          },
          {
            "title": "Handling Data Skew: Key Salting & Skew Join Hints",
            "anchor": "handling-data-skew-key-salting-skew-join-hints"
          },
          {
            "title": "Spark Structured Streaming: Event-Time Processing, Watermarking & Micro-Batching",
            "anchor": "spark-structured-streaming-event-time-watermarking"
          }
        ]
      }
    ]
  },
  {
    "section": "12. Database Engineering & PostgreSQL Internals",
    "subsections": [
      {
        "id": "postgresql-relational-normalization",
        "title": "Relational Theory, Normalization & Schema Design",
        "file": "postgresql-relational-normalization.md",
        "concepts": [
          {
            "title": "Relational Calculus & Data Integrity: Candidate Keys, Foreign Keys & Constraints",
            "anchor": "relational-calculus-data-integrity-keys-constraints"
          },
          {
            "title": "Functional Dependencies & Database Normalization (1NF, 2NF, 3NF, BCNF)",
            "anchor": "functional-dependencies-database-normalization-1nf-3nf-bcnf"
          },
          {
            "title": "Strategic Denormalization: Read Performance vs Write Anomaly Trade-Offs",
            "anchor": "strategic-denormalization-read-performance-write-anomalies"
          }
        ]
      },
      {
        "id": "postgresql-storage-mvcc-wal",
        "title": "PostgreSQL Internals: Storage, MVCC, WAL & Vacuuming",
        "file": "postgresql-storage-mvcc-wal.md",
        "concepts": [
          {
            "title": "PostgreSQL Physical Layout: Data Pages, Tuples, Shared Buffers & Buffer Pool",
            "anchor": "postgresql-physical-layout-pages-tuples-shared-buffers"
          },
          {
            "title": "Multi-Version Concurrency Control (MVCC): xmin, xmax, Snapshots & Isolation Levels",
            "anchor": "mvcc-xmin-xmax-snapshots-isolation-levels"
          },
          {
            "title": "Write-Ahead Logging (WAL): Checkpoints, LSNs & Crash Recovery",
            "anchor": "write-ahead-logging-wal-checkpoints-lsns-crash-recovery"
          },
          {
            "title": "VACUUM Mechanics: Dead Tuple Cleanup, Autovacuum Tuning & Anti-Wraparound Freeze",
            "anchor": "vacuum-mechanics-dead-tuples-autovacuum-tuning-freeze"
          }
        ]
      },
      {
        "id": "postgresql-indexing-optimization",
        "title": "PostgreSQL Index Architectures & Query Tuning",
        "file": "postgresql-indexing-optimization.md",
        "concepts": [
          {
            "title": "B-Tree Indexes: Node Layout, Search Traversal, Multi-Column & Covering Indexes (INCLUDE)",
            "anchor": "b-tree-indexes-node-layout-covering-indexes-include"
          },
          {
            "title": "Specialized Indexes: GIN (JSONB, Full-Text), GiST (Geospatial PostGIS) & BRIN (Timeseries)",
            "anchor": "specialized-indexes-gin-gist-brin-postgis"
          },
          {
            "title": "Query Lifecycle: Parser, Rewriter, Cost-Based Optimizer (CBO) & Executor",
            "anchor": "query-lifecycle-parser-rewriter-cbo-executor"
          },
          {
            "title": "Mastering EXPLAIN (ANALYZE, BUFFERS): Scan Types, Join Nodes & Cost Calculations",
            "anchor": "mastering-explain-analyze-buffers-scans-joins"
          }
        ]
      },
      {
        "id": "postgresql-replication-ha",
        "title": "Replication, Connection Pooling & High Availability",
        "file": "postgresql-replication-ha.md",
        "concepts": [
          {
            "title": "Physical Streaming Replication: Synchronous vs Asynchronous WAL Shipping",
            "anchor": "physical-streaming-replication-sync-vs-async-wal"
          },
          {
            "title": "Logical Replication: Publications, Subscriptions & Cross-Version Replication",
            "anchor": "logical-replication-publications-subscriptions"
          },
          {
            "title": "Connection Pooling with PgBouncer: Session, Transaction & Statement Pooling Modes",
            "anchor": "connection-pooling-pgbouncer-modes-tuning"
          },
          {
            "title": "High Availability Architectures: Patroni, Distributed Consensus (etcd) & Automated Failover",
            "anchor": "high-availability-architectures-patroni-etcd-failover"
          }
        ]
      }
    ]
  },
  {
    "section": "13. In-Memory Caching with Redis",
    "subsections": [
      {
        "id": "redis-architecture-datastructures",
        "title": "Redis Architecture & Data Structure Internals",
        "file": "redis-architecture-datastructures.md",
        "concepts": [
          {
            "title": "Redis Single-Threaded Event Loop: I/O Multiplexing (epoll/kqueue) Architecture",
            "anchor": "redis-event-loop-io-multiplexing-epoll-kqueue"
          },
          {
            "title": "Core Data Structures: Strings (SDS), Hashes (ZipList/Dict), Lists (QuickList)",
            "anchor": "core-data-structures-strings-hashes-lists"
          },
          {
            "title": "Advanced Structures: Sets (IntSet/Dict), Sorted Sets (SkipList), Bitmaps & HyperLogLog",
            "anchor": "advanced-structures-sets-sorted-sets-skiplist-hyperloglog"
          },
          {
            "title": "Redis Streams: Message Queuing with Consumer Groups and Pending Entries List (PEL)",
            "anchor": "redis-streams-consumer-groups-pending-entries-pel"
          }
        ]
      },
      {
        "id": "redis-caching-patterns-eviction",
        "title": "Caching Topologies, Invalidation & Eviction",
        "file": "redis-caching-patterns-eviction.md",
        "concepts": [
          {
            "title": "Caching Topologies: Cache-Aside (Lazy), Read-Through, Write-Through & Write-Behind",
            "anchor": "caching-topologies-cache-aside-read-through-write-through-write-behind"
          },
          {
            "title": "Cache Failure Modes: Cache Penetration, Cache Avalanche & Cache Stampede",
            "anchor": "cache-failure-modes-penetration-avalanche-stampede"
          },
          {
            "title": "Mitigation Patterns: Bloom Filters, Mutex Locks & Probabilistic Early Expiration (XFetch)",
            "anchor": "mitigation-patterns-bloom-filters-mutex-xfetch"
          },
          {
            "title": "Eviction Policies: allkeys-lru, volatile-lru, LFU & maxmemory Configuration",
            "anchor": "eviction-policies-lru-lfu-maxmemory-configuration"
          }
        ]
      },
      {
        "id": "redis-persistence-sentinel-cluster",
        "title": "Persistence, Sentinel High Availability & Redis Cluster",
        "file": "redis-persistence-sentinel-cluster.md",
        "concepts": [
          {
            "title": "Persistence Mechanics: RDB (Point-in-Time Snapshots) vs AOF (Append-Only File)",
            "anchor": "persistence-mechanics-rdb-snapshots-vs-aof-append-only"
          },
          {
            "title": "AOF Fsync Policies (always, everysec, no) & Background Log Rewriting (bgrewriteaof)",
            "anchor": "aof-fsync-policies-background-log-rewriting"
          },
          {
            "title": "Redis Sentinel: Quorum-Based Automatic Failover & Configuration Provider",
            "anchor": "redis-sentinel-quorum-failover-configuration-provider"
          },
          {
            "title": "Redis Cluster: Hash Slots (16,384), CRC16 Sharding, Multi-Key Limitations & Smart Clients",
            "anchor": "redis-cluster-hash-slots-sharding-smart-clients"
          }
        ]
      }
    ]
  },
  {
    "section": "14. Java & Spring Boot Microservices",
    "subsections": [
      {
        "id": "java-jvm-memory-concurrency",
        "title": "JVM Internals, Garbage Collection & Modern Concurrency",
        "file": "java-jvm-memory-concurrency.md",
        "concepts": [
          {
            "title": "JVM Runtime Data Areas: Heap, Stack, Metaspace & Program Counter Register",
            "anchor": "jvm-runtime-data-areas-heap-stack-metaspace"
          },
          {
            "title": "Garbage Collection Mechanics: Generational Hypothesis, G1 GC & ZGC Low Latency Collector",
            "anchor": "garbage-collection-mechanics-g1-gc-zgc-collector"
          },
          {
            "title": "Java Memory Model (JMM): synchronized, volatile, Happens-Before & Atomic References",
            "anchor": "java-memory-model-synchronized-volatile-atomics"
          },
          {
            "title": "Thread Pools, CompletableFuture & Project Loom Virtual Threads (Java 21)",
            "anchor": "thread-pools-completablefuture-virtual-threads"
          }
        ]
      },
      {
        "id": "spring-boot-core-di",
        "title": "Spring Boot Core Container & Dependency Injection",
        "file": "spring-boot-core-di.md",
        "concepts": [
          {
            "title": "Inversion of Control (IoC) & Dependency Injection: Constructor vs Field Injection",
            "anchor": "ioc-dependency-injection-constructor-vs-field"
          },
          {
            "title": "Bean Lifecycle: Instantiation, Dependency Population, Aware Interfaces, @PostConstruct & @PreDestroy",
            "anchor": "bean-lifecycle-postconstruct-predestroy"
          },
          {
            "title": "Spring Stereotypes & Configuration: @Component, @Service, @Repository & @Configuration",
            "anchor": "spring-stereotypes-component-service-repository-configuration"
          },
          {
            "title": "Spring Profiles, Externalized Configuration (@Value, @ConfigurationProperties) & Actuator",
            "anchor": "spring-profiles-configuration-properties-actuator"
          }
        ]
      },
      {
        "id": "spring-data-jpa-hibernate",
        "title": "Spring Data JPA, Hibernate & Transaction Management",
        "file": "spring-data-jpa-hibernate.md",
        "concepts": [
          {
            "title": "JPA & Hibernate Entity Lifecycle: Transient, Managed, Detached & Removed States",
            "anchor": "jpa-hibernate-entity-lifecycle-states"
          },
          {
            "title": "Entity Relationship Mappings: @OneToMany, @ManyToOne, Cascades & Orphan Removal",
            "anchor": "entity-relationship-mappings-onetomany-manytoone-cascades"
          },
          {
            "title": "Eliminating the N+1 Query Problem: JOIN FETCH, EntityGraphs & DTO Projections",
            "anchor": "eliminating-n-plus-1-query-problem-join-fetch-entitygraphs"
          },
          {
            "title": "Declarative Transaction Management (@Transactional): Propagation Levels & Isolation Guarantees",
            "anchor": "declarative-transaction-management-propagation-isolation"
          }
        ]
      },
      {
        "id": "spring-security-microservices",
        "title": "Spring Security & Microservice Resiliency",
        "file": "spring-security-microservices.md",
        "concepts": [
          {
            "title": "Spring Security Architecture: SecurityFilterChain, AuthenticationManager & OncePerRequestFilter",
            "anchor": "spring-security-architecture-filterchain-filters"
          },
          {
            "title": "Stateless JWT Authentication & Role-Based Access Control (RBAC) with Spring Security",
            "anchor": "stateless-jwt-authentication-rbac-spring-security"
          },
          {
            "title": "Microservices Communication: Feign Client, WebClient & API Gateway Routing",
            "anchor": "microservices-feign-webclient-api-gateway"
          },
          {
            "title": "Resiliency Patterns with Resilience4j: Circuit Breakers, Retries, Rate Limiters & Bulkheads",
            "anchor": "resiliency-patterns-resilience4j-circuit-breaker-retry"
          }
        ]
      }
    ]
  },
  {
    "section": "15. Python Backend Engineering with FastAPI",
    "subsections": [
      {
        "id": "python-async-fastapi-core",
        "title": "Asynchronous Python & FastAPI Framework Core",
        "file": "python-async-fastapi-core.md",
        "concepts": [
          {
            "title": "Async Python Mechanics: Event Loop, Coroutines (async/await) & asyncio Task Concurrency",
            "anchor": "async-python-event-loop-coroutines-asyncio-concurrency"
          },
          {
            "title": "WSGI vs ASGI: Starlette, Uvicorn & Non-Blocking Request Handling",
            "anchor": "wsgi-vs-asgi-starlette-uvicorn-nonblocking-handling"
          },
          {
            "title": "Pydantic v2: Strict Request Validation, Serialization & Custom Field Validators",
            "anchor": "pydantic-v2-request-validation-serialization-validators"
          },
          {
            "title": "FastAPI Dependency Injection System: Session Scoping, Security Dependencies & Reusable Logic",
            "anchor": "fastapi-dependency-injection-session-scoping-security"
          }
        ]
      },
      {
        "id": "fastapi-database-testing",
        "title": "SQLAlchemy 2.0 Async, Migrations & Production Testing",
        "file": "fastapi-database-testing.md",
        "concepts": [
          {
            "title": "SQLAlchemy 2.0 Async ORM: Async Engine, AsyncSession & Relationship Loading Strategies",
            "anchor": "sqlalchemy-async-orm-async-engine-session-loading"
          },
          {
            "title": "Database Schema Migrations with Alembic: Autogenerate, Version Control & Rollbacks",
            "anchor": "database-schema-migrations-alembic-autogenerate-rollbacks"
          },
          {
            "title": "JWT Authentication & Password Hashing with Passlib / Argon2 in FastAPI",
            "anchor": "jwt-authentication-password-hashing-fastapi"
          },
          {
            "title": "Automated Testing with Pytest: Async Fixtures, TestClient, Database Mocking & Testcontainers",
            "anchor": "automated-testing-pytest-async-fixtures-testcontainers"
          }
        ]
      }
    ]
  },
  {
    "section": "16. Production API Design & Architecture",
    "subsections": [
      {
        "id": "api-paradigms-http-grpc",
        "title": "API Styles: REST, GraphQL, gRPC & HTTP Protocols",
        "file": "api-paradigms-http-grpc.md",
        "concepts": [
          {
            "title": "HTTP Protocols: HTTP/1.1 Pipelining vs HTTP/2 Multiplexing vs HTTP/3 QUIC UDP",
            "anchor": "http-protocols-http1-http2-http3-quic-multiplexing"
          },
          {
            "title": "REST Architecture: Richardson Maturity Model, Resource URIs, Methods & HATEOAS",
            "anchor": "rest-architecture-richardson-maturity-model-uris-methods"
          },
          {
            "title": "GraphQL Architecture: Schema Definition Language (SDL), Queries, Mutations & Solving N+1 with DataLoader",
            "anchor": "graphql-architecture-sdl-queries-mutations-dataloader"
          },
          {
            "title": "gRPC & Protocol Buffers: Binary Serialization, HTTP/2 Transport, Unary vs Streaming RPCs",
            "anchor": "grpc-protocol-buffers-binary-serialization-streaming-rpcs"
          }
        ]
      },
      {
        "id": "api-security-resilience",
        "title": "API Security, Rate Limiting & Enterprise Governance",
        "file": "api-security-resilience.md",
        "concepts": [
          {
            "title": "OWASP API Security Top 10: Broken Object Level Authorization (BOLA), Mass Assignment & Mitigations",
            "anchor": "owasp-api-security-top-10-bola-mass-assignment"
          },
          {
            "title": "Rate Limiting Algorithms: Token Bucket, Leaky Bucket, Sliding Window Log & Sliding Window Counter",
            "anchor": "rate-limiting-algorithms-token-bucket-leaky-bucket-sliding-window"
          },
          {
            "title": "Idempotent API Design: Idempotency Keys, Unique Constraints & Distributed Locks",
            "anchor": "idempotent-api-design-idempotency-keys-distributed-locks"
          },
          {
            "title": "API Pagination Strategies: Offset/Limit vs Cursor-Based (Keyset) Pagination for Massive Datasets",
            "anchor": "api-pagination-strategies-offset-vs-cursor-keyset-pagination"
          }
        ]
      }
    ]
  }
];
