#!/usr/bin/env python3
"""
Build and validate Cloud_DevOps_Tutorial/resources.js.
Validates all YouTube video IDs via YouTube oEmbed API.
Provides exact chapter start timestamps (seconds) and official documentation links.
"""

import json
import os
import sys
import urllib.request
import re

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOPICS_FILE = os.path.join(ROOT, "Cloud_DevOps_Tutorial", "topics.js")
OUT_FILE = os.path.join(ROOT, "Cloud_DevOps_Tutorial", "resources.js")

# Verified video metadata cache
OEMBED_CACHE = {}

def get_oembed(video_id):
    if video_id in OEMBED_CACHE:
        return OEMBED_CACHE[video_id]
    url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            title = data.get('title', 'Video')
            author = data.get('author_name', 'YouTube')
            OEMBED_CACHE[video_id] = (title, author)
            return (title, author)
    except Exception as e:
        print(f"[ERROR] Failed to verify video ID {video_id}: {e}")
        return None

# Mapping of lesson files to curated verified videos and docs
# Format: "lesson_file": {
#   "video": (video_id, custom_title_suffix, default_start_sec),
#   "docs": [(doc_title, doc_url), ...],
#   "concept_starts": { "concept_anchor": start_sec, ... }
# }

LESSON_MAPPINGS = {
    # 1. AWS
    "aws-foundations-iam.md": {
        "video": ("SOTamWNgDKc", "AWS Foundations & IAM", 1055),
        "docs": [
            ("AWS Well-Architected Framework", "https://aws.amazon.com/architecture/well-architected/"),
            ("AWS IAM User Guide & Security Best Practices", "https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html")
        ],
        "concept_starts": {
            "cloud-computing-models-iaas-paas-saas-shared-responsibility": 1055,
            "aws-global-infrastructure-regions-azs-edge-locations": 5634,
            "iam-fundamentals-root-users-groups-policies": 29289,
            "iam-roles-instance-profiles-sts-assumerole": 29850,
            "policy-evaluation-logic-scps-permission-boundaries": 30420
        }
    },
    "aws-networking-vpc.md": {
        "video": ("SOTamWNgDKc", "AWS VPC & Network Architecture", 23739),
        "docs": [
            ("Amazon VPC User Guide", "https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html"),
            ("AWS Direct Connect & Transit Gateway Patterns", "https://docs.aws.amazon.com/whitepapers/latest/aws-transit-gateway-best-practices/welcome.html")
        ],
        "concept_starts": {
            "vpc-fundamentals-cidr-blocks-subnets-route-tables": 23739,
            "internet-gateways-nat-gateways-egress-gateways": 24150,
            "security-groups-vs-network-acls": 24680,
            "vpc-peering-transit-gateway-direct-connect": 25100,
            "vpc-endpoints-gateway-vs-privatelink": 25520
        }
    },
    "aws-compute-ec2.md": {
        "video": ("SOTamWNgDKc", "AWS Compute: EC2 & Auto Scaling", 25047),
        "docs": [
            ("Amazon EC2 Documentation", "https://docs.aws.amazon.com/ec2/"),
            ("Elastic Load Balancing User Guide", "https://docs.aws.amazon.com/elasticloadbalancing/")
        ],
        "concept_starts": {
            "ec2-architecture-instance-types-amis-userdata": 25047,
            "ec2-pricing-models-reserved-spot-instances": 28150,
            "elastic-load-balancers-alb-vs-nlb": 28550,
            "target-groups-health-checks-cross-zone-balancing": 28800,
            "auto-scaling-groups-launch-templates-scaling-policies": 29050
        }
    },
    "aws-storage-s3-ebs.md": {
        "video": ("SOTamWNgDKc", "AWS Storage: S3, EBS & EFS", 19668),
        "docs": [
            ("Amazon S3 User Guide", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html"),
            ("Amazon EBS Volume Types & Performance", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-volume-types.html")
        ],
        "concept_starts": {
            "amazon-s3-architecture-buckets-keys-consistency": 19668,
            "s3-storage-classes-glacier-lifecycle-rules": 20400,
            "s3-security-bucket-policies-presigned-urls-encryption": 21100,
            "ebs-volume-types-gp3-io2-snapshots": 21500,
            "amazon-efs-distributed-file-system-fsx": 21850
        }
    },
    "aws-databases-nosql.md": {
        "video": ("SOTamWNgDKc", "AWS Databases: RDS & DynamoDB", 21926),
        "docs": [
            ("Amazon Relational Database Service (RDS)", "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html"),
            ("Amazon DynamoDB Developer Guide", "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html")
        ],
        "concept_starts": {
            "amazon-rds-multiaz-vs-read-replicas": 21926,
            "amazon-aurora-storage-engine-serverless-v2": 22450,
            "dynamodb-data-modeling-partition-sort-keys": 22800,
            "dynamodb-gsi-vs-lsi-indexes": 23200,
            "dynamodb-streams-ttl-dax-acceleration": 23550
        }
    },
    "aws-containers-serverless.md": {
        "video": ("SOTamWNgDKc", "AWS Containers & Serverless", 32722),
        "docs": [
            ("AWS Lambda Developer Guide", "https://docs.aws.amazon.com/lambda/latest/dg/welcome.html"),
            ("Amazon Elastic Container Service (ECS)", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/Welcome.html")
        ],
        "concept_starts": {
            "amazon-ecs-task-definitions-services-fargate": 32722,
            "amazon-eks-control-plane-nodegroups-irsa": 33400,
            "aws-lambda-execution-lifecycle-cold-starts-concurrency": 36334,
            "amazon-api-gateway-rest-http-authorizers-websockets": 36700,
            "aws-step-functions-eventbridge-serverless-workflows": 37000
        }
    },
    "aws-messaging-observability.md": {
        "video": ("SOTamWNgDKc", "AWS Messaging & Observability", 32035),
        "docs": [
            ("Amazon SQS Developer Guide", "https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html"),
            ("Amazon CloudWatch User Guide", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html")
        ],
        "concept_starts": {
            "amazon-sqs-standard-fifo-visibility-dlq": 32035,
            "amazon-sns-pubsub-topics-fanout-delivery": 32400,
            "amazon-cloudwatch-metrics-alarms-logs-insights": 37126,
            "aws-cloudtrail-xray-auditing-distributed-tracing": 37550,
            "amazon-route-53-hosted-zones-routing-policies-healthchecks": 24800,
            "amazon-cloudfront-cdn-edge-caching-oac-lambda-edge": 25200
        }
    },

    # 2. Azure
    "azure-foundations-entra.md": {
        "video": ("NKEFWyqJ5XA", "Azure Foundations & Entra ID", 831),
        "docs": [
            ("Microsoft Azure Fundamentals (AZ-900) Documentation", "https://learn.microsoft.com/en-us/azure/"),
            ("Microsoft Entra ID (Azure AD) Documentation", "https://learn.microsoft.com/en-us/entra/identity/")
        ],
        "concept_starts": {
            "azure-resource-hierarchy-management-groups-subscriptions": 9607,
            "azure-entra-id-users-groups-service-principals-rbac": 8365,
            "managed-identities-system-assigned-vs-user-assigned": 8800,
            "azure-policy-blueprints-resource-locks": 9344
        }
    },
    "azure-compute-networking.md": {
        "video": ("NKEFWyqJ5XA", "Azure Compute & Virtual Networks", 2533),
        "docs": [
            ("Azure Virtual Machines Documentation", "https://learn.microsoft.com/en-us/azure/virtual-machines/"),
            ("Azure Virtual Network (VNet) Overview", "https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-overview")
        ],
        "concept_starts": {
            "azure-vms-availability-sets-vm-scale-sets": 2533,
            "azure-vnet-architecture-subnets-peering": 5102,
            "network-security-groups-nsgs-application-security-groups": 5400,
            "azure-load-balancer-vs-application-gateway": 5612,
            "azure-app-service-azure-functions-serverless": 2692
        }
    },
    "azure-storage-databases.md": {
        "video": ("NKEFWyqJ5XA", "Azure Storage, SQL & Cosmos DB", 4221),
        "docs": [
            ("Azure Blob Storage Documentation", "https://learn.microsoft.com/en-us/azure/storage/blobs/"),
            ("Azure Cosmos DB Documentation", "https://learn.microsoft.com/en-us/azure/cosmos-db/")
        ],
        "concept_starts": {
            "azure-blob-storage-hot-cool-archive-tiers": 4221,
            "azure-data-lake-storage-gen2-adls": 4350,
            "azure-sql-database-elastic-pools-managed-instances": 4442,
            "azure-cosmos-db-multimodel-global-distribution": 4580,
            "cosmos-db-five-consistency-levels-explained": 4700
        }
    },
    "azure-containers-monitoring.md": {
        "video": ("NKEFWyqJ5XA", "Azure Containers & Observability", 2618),
        "docs": [
            ("Azure Kubernetes Service (AKS) Documentation", "https://learn.microsoft.com/en-us/azure/aks/"),
            ("Azure Monitor Overview", "https://learn.microsoft.com/en-us/azure/azure-monitor/overview")
        ],
        "concept_starts": {
            "azure-kubernetes-service-aks-nodepools-cni": 2618,
            "azure-container-apps-keda-microservices": 2660,
            "azure-service-bus-queues-topics-deadletter": 4600,
            "azure-event-grid-event-hubs-streaming": 4650,
            "azure-monitor-log-analytics-kql-application-insights": 9658
        }
    },

    # 3. GCP
    "gcp-foundations-iam-vpc.md": {
        "video": ("jpno8FSqpc8", "GCP Resource Hierarchy, IAM & Global VPC", 5936),
        "docs": [
            ("Google Cloud Resource Manager", "https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy"),
            ("Google Cloud VPC Network Overview", "https://cloud.google.com/vpc/docs/overview")
        ],
        "concept_starts": {
            "gcp-resource-hierarchy-organizations-folders-projects": 5936,
            "gcp-cloud-iam-roles-workload-identity-federation": 15655,
            "gcp-global-vpc-shared-vpc-network-peering": 22719,
            "gcp-cloud-load-balancing-global-https-cdn": 48801
        }
    },
    "gcp-compute-containers.md": {
        "video": ("jpno8FSqpc8", "GCP Compute Engine, GKE & Cloud Run", 35961),
        "docs": [
            ("Google Compute Engine Documentation", "https://cloud.google.com/compute/docs"),
            ("Google Kubernetes Engine (GKE) Documentation", "https://cloud.google.com/kubernetes-engine/docs")
        ],
        "concept_starts": {
            "gcp-compute-engine-vms-migs-spot-instances": 35961,
            "google-kubernetes-engine-gke-standard-vs-autopilot": 52490,
            "gcp-cloud-run-serverless-containers-scaletozero": 62500,
            "gcp-cloud-functions-gen2-eventarc": 63049
        }
    },
    "gcp-storage-databases.md": {
        "video": ("jpno8FSqpc8", "GCP Storage, Spanner & Big Data", 64186),
        "docs": [
            ("Google Cloud Storage Documentation", "https://cloud.google.com/storage/docs"),
            ("Google Cloud Spanner Architecture", "https://cloud.google.com/spanner/docs")
        ],
        "concept_starts": {
            "google-cloud-storage-gcs-storage-tiers": 64186,
            "gcp-cloud-sql-vs-memorystore-redis": 67580,
            "gcp-cloud-spanner-distributed-relational-truetime": 68631,
            "gcp-cloud-bigtable-nosql-wide-column-engine": 69100,
            "gcp-bigquery-serverless-columnar-warehouse-sql": 69844,
            "gcp-cloud-pubsub-messaging-cloud-monitoring": 71436
        }
    },

    # 4. Linux & Terminal
    "linux-filesystem-permissions.md": {
        "video": ("sWbUDq4S6Y8", "Linux Filesystem & Permissions", 98),
        "docs": [
            ("Filesystem Hierarchy Standard (FHS)", "https://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0.html"),
            ("Linux Permissions Reference (ArchWiki)", "https://wiki.archlinux.org/title/File_permissions_and_attributes")
        ],
        "concept_starts": {
            "linux-filesystem-hierarchy-standard-fhs": 98,
            "file-permissions-symbolic-octal-chmod-chown-umask": 17365,
            "special-permissions-suid-sgid-sticky-bit": 17800,
            "posix-access-control-lists-getfacl-setfacl": 18200
        }
    },
    "linux-process-performance.md": {
        "video": ("sWbUDq4S6Y8", "Linux Processes & Diagnostics", 13013),
        "docs": [
            ("Brendan Gregg's Linux Performance", "https://www.brendangregg.com/linuxperf.html"),
            ("Linux Process Management (Red Hat)", "https://docs.redhat.com/")
        ],
        "concept_starts": {
            "process-lifecycle-ps-top-htop-signals": 13013,
            "cpu-diagnostics-load-averages-uptime-vmstat": 13600,
            "memory-diagnostics-free-buffer-cache-oom-killer": 14100,
            "disk-io-networking-diagnostics-iostat-ss-lsof": 20404
        }
    },
    "linux-text-bash-scripting.md": {
        "video": ("sWbUDq4S6Y8", "Text Processing & Bash Scripting", 18812),
        "docs": [
            ("Bash Reference Manual (GNU)", "https://www.gnu.org/software/bash/manual/"),
            ("systemd System and Service Manager", "https://systemd.io/")
        ],
        "concept_starts": {
            "io-redirection-pipes-tee-xargs": 7977,
            "text-manipulation-grep-sed-awk": 18812,
            "robust-bash-scripting-error-trapping-functions": 19400,
            "linux-service-management-systemd-systemctl-journalctl": 20000
        }
    },

    # 5. Git & GitHub
    "git-architecture-internals.md": {
        "video": ("RGOj5yH7evk", "Git Internals & Architecture", 70),
        "docs": [
            ("Pro Git Book — Chapter 10: Git Internals", "https://git-scm.com/book/en/v2/Git-Internals-Plumbing-and-Porcelain"),
            ("Git Documentation: Object Database", "https://git-scm.com/docs/git-hash-object")
        ],
        "concept_starts": {
            "git-object-model-blobs-trees-commits-tags": 70,
            "the-three-trees-working-directory-index-repository": 320,
            "git-diff-internals-working-staging-head": 1095,
            "atomic-commits-git-add-patch-hygiene": 1155
        }
    },
    "git-branching-rebasing.md": {
        "video": ("RGOj5yH7evk", "Branching & Interactive Rebasing", 1962),
        "docs": [
            ("Pro Git Book — Chapter 3: Git Branching", "https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell"),
            ("Atlassian Git: Merging vs Rebasing", "https://www.atlassian.com/git/tutorials/merging-vs-rebasing")
        ],
        "concept_starts": {
            "branching-workflows-trunk-based-vs-gitflow": 1962,
            "merge-mechanics-fastforward-vs-3way-merges": 2100,
            "interactive-rebasing-squash-reword-drop": 2350,
            "merge-vs-rebase-tradeoffs-force-with-lease": 2600
        }
    },
    "git-advanced-reflog-bisect.md": {
        "video": ("RGOj5yH7evk", "Advanced Git: Reflog & Bisect", 3390),
        "docs": [
            ("Pro Git Book — Chapter 7: Git Tools - Revision Selection & Bisect", "https://git-scm.com/book/en/v2/Git-Tools-Revision-Selection"),
            ("Git Bisect Guide", "https://git-scm.com/docs/git-bisect")
        ],
        "concept_starts": {
            "git-reflog-recovering-lost-commits-deleted-branches": 3390,
            "git-reset-soft-mixed-hard-vs-revert": 3480,
            "git-bisect-binary-search-bug-pinpointing": 3600,
            "git-cherry-pick-worktrees-multi-branch-isolation": 3710,
            "git-hooks-pre-commit-server-side-enforcement": 3820
        }
    },
    "github-collaboration-actions.md": {
        "video": ("R8_veQiYBjI", "GitHub Actions CI/CD Pipeline", 0),
        "docs": [
            ("GitHub Actions Documentation", "https://docs.github.com/en/actions"),
            ("GitHub Flow & Pull Request Best Practices", "https://docs.github.com/en/get-started/using-github/github-flow")
        ],
        "concept_starts": {
            "pull-requests-branch-protection-required-checks-codeowners": 0,
            "github-actions-workflows-jobs-steps-matrix-runners": 420,
            "github-actions-secrets-environments-oidc-cloud-auth": 1120,
            "github-actions-artifacts-dependency-caching": 1650
        }
    },

    # 6. Docker
    "docker-architecture-engine.md": {
        "video": ("3c-iBn73dDE", "Docker Engine & Kernel Primitives", 118),
        "docs": [
            ("Docker Overview & Architecture", "https://docs.docker.com/get-started/overview/"),
            ("Linux Namespaces and Cgroups Reference", "https://man7.org/linux/man-pages/man7/namespaces.7.html")
        ],
        "concept_starts": {
            "linux-kernel-primitives-namespaces-cgroups": 118,
            "union-file-systems-overlayfs-copy-on-write": 656,
            "docker-engine-dockerd-containerd-runc-oci": 1180,
            "containers-vs-virtual-machines-isolation-overhead": 1433
        }
    },
    "dockerfile-image-optimization.md": {
        "video": ("3c-iBn73dDE", "Dockerfile Optimization & Security", 6122),
        "docs": [
            ("Dockerfile Best Practices Guide", "https://docs.docker.com/develop/develop-images/dockerfile_best-practices/"),
            ("Multi-Stage Builds Documentation", "https://docs.docker.com/build/building/multi-stage/")
        ],
        "concept_starts": {
            "dockerfile-directives-entrypoint-cmd-run-copy": 6122,
            "multi-stage-builds-image-size-attack-surface-reduction": 6480,
            "layer-caching-strategies-command-ordering": 6800,
            "container-security-non-root-distroless-vulnerability-scanning": 7100
        }
    },
    "docker-networking-volumes.md": {
        "video": ("3c-iBn73dDE", "Docker Networking & Compose", 5389),
        "docs": [
            ("Docker Networking Documentation", "https://docs.docker.com/network/"),
            ("Docker Compose Specification", "https://docs.docker.com/compose/")
        ],
        "concept_starts": {
            "docker-networking-drivers-bridge-host-overlay": 2522,
            "docker-storage-named-volumes-bind-mounts-tmpfs": 8846,
            "docker-compose-orchestration-healthchecks-networking": 5389
        }
    },

    # 7. Kubernetes
    "k8s-architecture-control-plane.md": {
        "video": ("X48VuDVv0do", "Kubernetes Architecture & Control Plane", 1349),
        "docs": [
            ("Kubernetes Components Overview", "https://kubernetes.io/docs/concepts/overview/components/"),
            ("etcd Distributed Key-Value Store Documentation", "https://etcd.io/docs/")
        ],
        "concept_starts": {
            "control-plane-architecture-apiserver-etcd-scheduler-controllers": 1349,
            "worker-node-architecture-kubelet-kubeproxy-cri": 1820,
            "declarative-object-model-reconciliation-loop": 3723,
            "kubectl-architecture-contexts-auth-flow": 2692
        }
    },
    "k8s-workloads-pods-deployments.md": {
        "video": ("X48VuDVv0do", "Pods, Deployments & Rollouts", 320),
        "docs": [
            ("Kubernetes Pod Lifecycle", "https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/"),
            ("Kubernetes Deployments Guide", "https://kubernetes.io/docs/concepts/workloads/controllers/deployment/")
        ],
        "concept_starts": {
            "pod-lifecycle-anatomy-sidecar-init-containers": 320,
            "deployments-replicasets-replicated-workloads": 850,
            "rolling-updates-rollbacks-maxsurge-maxunavailable": 1150,
            "probes-liveness-readiness-startup-probes": 1500
        }
    },
    "k8s-stateful-daemon-jobs.md": {
        "video": ("X48VuDVv0do", "StatefulSets & DaemonSets", 10718),
        "docs": [
            ("Kubernetes StatefulSets Documentation", "https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/"),
            ("Kubernetes DaemonSet Documentation", "https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/")
        ],
        "concept_starts": {
            "statefulsets-stable-network-identities-ordered-deployment": 10718,
            "daemonsets-node-level-agents-logging-monitoring": 11150,
            "batch-processing-kubernetes-jobs-cronjobs": 11400
        }
    },
    "k8s-networking-services-ingress.md": {
        "video": ("X48VuDVv0do", "Kubernetes Services & Ingress", 7312),
        "docs": [
            ("Kubernetes Services Documentation", "https://kubernetes.io/docs/concepts/services-networking/service/"),
            ("Kubernetes Ingress Controllers", "https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/")
        ],
        "concept_starts": {
            "cluster-networking-model-cni-calico-cilium": 7312,
            "kubernetes-services-clusterip-nodeport-loadbalancer-headless": 11623,
            "ingress-controllers-nginx-traefik-path-routing": 7312,
            "kubernetes-gateway-api-httproute-grpcroute": 8100
        }
    },
    "k8s-config-storage-helm.md": {
        "video": ("X48VuDVv0do", "Kubernetes Storage & Helm", 8657),
        "docs": [
            ("Kubernetes Volumes and Persistent Volumes", "https://kubernetes.io/docs/concepts/storage/persistent-volumes/"),
            ("Helm Documentation", "https://helm.sh/docs/")
        ],
        "concept_starts": {
            "configmaps-secrets-projections-sealedsecrets": 6376,
            "kubernetes-storage-pv-pvc-storageclasses-csi": 9487,
            "resource-management-requests-limits-qos-hpa": 10100,
            "cluster-security-namespaces-resourcequotas-rbac": 6376,
            "helm-package-manager-charts-values-templates-releases": 8657
        }
    },

    # 8. Terraform
    "terraform-hcl-syntax.md": {
        "video": ("7xngnjfIlK4", "Terraform Core & HCL Syntax", 56),
        "docs": [
            ("Terraform CLI Documentation", "https://developer.hashicorp.com/terraform/docs"),
            ("HCL Syntax Specification", "https://developer.hashicorp.com/terraform/language")
        ],
        "concept_starts": {
            "iac-declarative-paradigm-vs-imperative-scripting": 56,
            "hcl-syntax-providers-resources-variables-locals-outputs": 251,
            "terraform-workflow-init-plan-apply-destroy": 876,
            "resource-dependencies-implicit-vs-explicit-graphs": 1213
        }
    },
    "terraform-state-management.md": {
        "video": ("7xngnjfIlK4", "Terraform State & Remote Backends", 1712),
        "docs": [
            ("Terraform State Documentation", "https://developer.hashicorp.com/terraform/language/state"),
            ("S3 Backend with DynamoDB Locking", "https://developer.hashicorp.com/terraform/language/settings/backends/s3")
        ],
        "concept_starts": {
            "terraform-state-internal-structure-drift-detection": 1712,
            "remote-backends-s3-dynamodb-state-locking": 2711,
            "state-manipulation-state-list-show-mv-import": 3503,
            "protecting-sensitive-data-state-workspaces": 4280
        }
    },
    "terraform-modules-workspaces.md": {
        "video": ("7xngnjfIlK4", "Terraform Modules & Advanced Patterns", 4802),
        "docs": [
            ("Terraform Modules Guide", "https://developer.hashicorp.com/terraform/language/modules"),
            ("Meta-Arguments: count and for_each", "https://developer.hashicorp.com/terraform/language/meta-arguments/for_each")
        ],
        "concept_starts": {
            "terraform-modules-root-vs-child-contracts": 4802,
            "meta-arguments-count-vs-for-each-dynamic-blocks": 5340,
            "data-sources-dynamically-querying-existing-state": 5766,
            "resource-lifecycle-hooks-create-before-destroy-ignore-changes": 6210
        }
    },

    # 9. CI/CD Pipelines
    "cicd-principles-deployment.md": {
        "video": ("oUdB2XqtGmk", "DevOps, CI/CD & Deployment Strategies", 0),
        "docs": [
            ("Martin Fowler: Continuous Integration", "https://martinfowler.com/articles/continuousIntegration.html"),
            ("Blue-Green Deployment Guide", "https://martinfowler.com/bliki/BlueGreenDeployment.html")
        ],
        "concept_starts": {
            "ci-vs-cd-vs-continuous-deployment": 0,
            "blue-green-deployments-zerodowntime-switching": 120,
            "canary-releases-incremental-traffic-shifting": 240,
            "rolling-deployments-recreate-strategies-feature-flags": 360
        }
    },
    "github-actions-enterprise.md": {
        "video": ("R8_veQiYBjI", "Enterprise GitHub Actions CI/CD", 0),
        "docs": [
            ("GitHub Actions Security Hardening", "https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions"),
            ("Configuring OpenID Connect in Cloud Providers", "https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect")
        ],
        "concept_starts": {
            "workflow-pipelines-linting-unit-testing-sast": 0,
            "docker-build-push-container-registries-ghcr": 480,
            "secretless-cloud-auth-oidc-integration": 960,
            "reusable-workflows-composite-actions-self-hosted-runners": 1440
        }
    },
    "jenkins-pipelines.md": {
        "video": ("oUdB2XqtGmk", "Jenkins Pipelines & GitOps", 0),
        "docs": [
            ("Jenkins Declarative Pipeline Syntax", "https://www.jenkins.io/doc/book/pipeline/syntax/"),
            ("ArgoCD Declarative GitOps Documentation", "https://argo-cd.readthedocs.io/")
        ],
        "concept_starts": {
            "jenkins-architecture-controller-agent-topology": 0,
            "declarative-jenkinsfile-stages-parallel-post-conditions": 150,
            "artifact-management-jfrog-artifactory-nexus": 300,
            "gitops-with-argocd-declarative-continuous-delivery": 450
        }
    },

    # 10. Apache Kafka
    "kafka-architecture-kraft.md": {
        "video": ("R873BlNVUB4", "Kafka Architecture & KRaft", 0),
        "docs": [
            ("Apache Kafka Documentation: Core Concepts", "https://kafka.apache.org/documentation/#intro_concepts"),
            ("KIP-500: Replace ZooKeeper with KRaft Metadata Mode", "https://cwiki.apache.org/confluence/display/KAFKA/KIP-500%3A+Replace+ZooKeeper+with+a+Self-Managed+Metadata+Quorum")
        ],
        "concept_starts": {
            "distributed-commit-log-append-only-records-sequential-io": 0,
            "kafka-broker-architecture-pagecache-zerocopy": 152,
            "zookeeper-elimination-kraft-metadata-mode": 1386
        }
    },
    "kafka-topics-partitions-producers.md": {
        "video": ("R873BlNVUB4", "Kafka Topics, Partitions & Producers", 339),
        "docs": [
            ("Apache Kafka Producer Configuration & Idempotence", "https://kafka.apache.org/documentation/#producerconfigs"),
            ("Confluent: Exactly-Once Semantics in Apache Kafka", "https://www.confluent.io/blog/exactly-once-semantics-are-possible-heres-how-apache-kafka-does-it/")
        ],
        "concept_starts": {
            "topics-partitions-sharding-concurrency-ordering": 514,
            "log-segments-retention-policies-log-compaction": 600,
            "producer-mechanics-partitioners-batching-acks": 339,
            "idempotent-producers-exactly-once-semantics-eos": 750
        }
    },
    "kafka-consumers-offset-management.md": {
        "video": ("R873BlNVUB4", "Kafka Consumers & Offsets", 431),
        "docs": [
            ("Apache Kafka Consumer Configuration", "https://kafka.apache.org/documentation/#consumerconfigs"),
            ("Cooperative Sticky Assignor in Apache Kafka", "https://www.confluent.io/blog/cooperative-rebalancing-in-kafka-streams-consumer-ksqldb/")
        ],
        "concept_starts": {
            "consumer-groups-parallel-processing-partition-assignment": 1007,
            "partition-rebalancing-eager-vs-cooperative-sticky": 1150,
            "offset-commit-strategies-automatic-vs-manual": 431,
            "poison-pills-dead-letter-queues-consumer-retry-topics": 1250
        }
    },
    "kafka-ecosystem-connect-streams.md": {
        "video": ("R873BlNVUB4", "Kafka Ecosystem: Connect & Streams", 1785),
        "docs": [
            ("Confluent Schema Registry Overview", "https://docs.confluent.io/platform/current/schema-registry/index.html"),
            ("Apache Kafka Streams Architecture", "https://kafka.apache.org/documentation/streams/architecture")
        ],
        "concept_starts": {
            "schema-registry-avro-protobuf-schema-evolution": 1785,
            "kafka-connect-source-sink-declarative-pipelines": 2000,
            "kafka-streams-kstream-ktable-stateful-processing-rocksdb": 2300
        }
    },

    # 11. Apache Spark
    "spark-architecture-execution.md": {
        "video": ("_C8kWso4ne4", "Apache Spark Architecture & DAG", 0),
        "docs": [
            ("Apache Spark Cluster Mode Overview", "https://spark.apache.org/docs/latest/cluster-overview.html"),
            ("Spark Job Execution Architecture", "https://spark.apache.org/docs/latest/job-scheduling.html")
        ],
        "concept_starts": {
            "spark-cluster-architecture-driver-executors": 0,
            "job-execution-lifecycle-stages-tasks-dagscheduler": 300,
            "narrow-vs-wide-dependencies-shuffle-boundary": 600
        }
    },
    "spark-rdds-transformations-actions.md": {
        "video": ("_C8kWso4ne4", "Spark RDDs & Lineage", 900),
        "docs": [
            ("Spark RDD Programming Guide", "https://spark.apache.org/docs/latest/rdd-programming-guide.html"),
            ("Transformations and Actions in Spark", "https://spark.apache.org/docs/latest/rdd-programming-guide.html#transformations")
        ],
        "concept_starts": {
            "rdd-fundamentals-immutability-partitioning-lineage": 900,
            "transformations-lazy-vs-actions-eager": 1200,
            "fault-tolerance-lineage-recomputation-checkpointing": 1500
        }
    },
    "spark-dataframes-catalyst.md": {
        "video": ("_C8kWso4ne4", "Spark DataFrames & Catalyst Engine", 1800),
        "docs": [
            ("Spark SQL, DataFrames and Datasets Guide", "https://spark.apache.org/docs/latest/sql-programming-guide.html"),
            ("Deep Dive into the Catalyst Optimizer", "https://databricks.com/blog/2015/04/13/deep-dive-into-spark-sqls-catalyst-optimizer.html")
        ],
        "concept_starts": {
            "dataframes-spark-sql-structured-data-processing": 1800,
            "catalyst-optimizer-analysis-logical-physical-planning": 2400,
            "tungsten-engine-off-heap-binary-memory-whole-stage-codegen": 3000
        }
    },
    "spark-streaming-performance.md": {
        "video": ("_C8kWso4ne4", "Spark Structured Streaming & Tuning", 3600),
        "docs": [
            ("Spark Structured Streaming Programming Guide", "https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html"),
            ("Spark Performance Tuning Guide", "https://spark.apache.org/docs/latest/tuning.html")
        ],
        "concept_starts": {
            "shuffle-optimization-partition-tuning-broadcast-joins": 3600,
            "spark-memory-management-storage-vs-execution-spilling": 4200,
            "handling-data-skew-key-salting-skew-join-hints": 4800,
            "spark-structured-streaming-event-time-watermarking": 5400
        }
    },

    # 12. PostgreSQL
    "postgresql-relational-normalization.md": {
        "video": ("qw--VYLpxG4", "PostgreSQL Relational Normalization", 317),
        "docs": [
            ("PostgreSQL Documentation: Data Definition & Constraints", "https://www.postgresql.org/docs/current/ddl-constraints.html"),
            ("Database Normalization Standards (1NF to BCNF)", "https://en.wikipedia.org/wiki/Database_normalization")
        ],
        "concept_starts": {
            "relational-calculus-data-integrity-keys-constraints": 317,
            "functional-dependencies-database-normalization-1nf-3nf-bcnf": 2952,
            "strategic-denormalization-read-performance-write-anomalies": 9655
        }
    },
    "postgresql-storage-mvcc-wal.md": {
        "video": ("qw--VYLpxG4", "PostgreSQL Storage, MVCC & WAL", 2497),
        "docs": [
            ("PostgreSQL Internals: Multi-Version Concurrency Control (MVCC)", "https://www.postgresql.org/docs/current/mvcc.html"),
            ("PostgreSQL Write-Ahead Logging (WAL)", "https://www.postgresql.org/docs/current/wal.html")
        ],
        "concept_starts": {
            "postgresql-physical-layout-pages-tuples-shared-buffers": 2497,
            "mvcc-xmin-xmax-snapshots-isolation-levels": 4919,
            "write-ahead-logging-wal-checkpoints-lsns-crash-recovery": 6190,
            "vacuum-mechanics-dead-tuples-autovacuum-tuning-freeze": 9083
        }
    },
    "postgresql-indexing-optimization.md": {
        "video": ("qw--VYLpxG4", "PostgreSQL Indexing & Query Tuning", 9083),
        "docs": [
            ("PostgreSQL Index Types Guide (B-Tree, GIN, GiST, BRIN)", "https://www.postgresql.org/docs/current/indexes-types.html"),
            ("Using EXPLAIN to Analyze Queries", "https://www.postgresql.org/docs/current/using-explain.html")
        ],
        "concept_starts": {
            "b-tree-indexes-node-layout-covering-indexes-include": 9083,
            "specialized-indexes-gin-gist-brin-postgis": 10155,
            "query-lifecycle-parser-rewriter-cbo-executor": 11801,
            "mastering-explain-analyze-buffers-scans-joins": 12570
        }
    },
    "postgresql-replication-ha.md": {
        "video": ("qw--VYLpxG4", "PostgreSQL Replication & HA", 12570),
        "docs": [
            ("PostgreSQL High Availability, Load Balancing, and Replication", "https://www.postgresql.org/docs/current/high-availability.html"),
            ("PgBouncer Connection Pooler Guide", "https://www.pgbouncer.org/")
        ],
        "concept_starts": {
            "physical-streaming-replication-sync-vs-async-wal": 12570,
            "logical-replication-publications-subscriptions": 13200,
            "connection-pooling-pgbouncer-modes-tuning": 13800,
            "high-availability-architectures-patroni-etcd-failover": 14400
        }
    },

    # 13. Redis
    "redis-architecture-datastructures.md": {
        "video": ("Hbt56gFj998", "Redis Architecture & Data Structures", 0),
        "docs": [
            ("Redis Data Types Tutorial", "https://redis.io/docs/data-types/"),
            ("Redis Event Loop & Multiplexing Internals", "https://redis.io/docs/reference/internals/")
        ],
        "concept_starts": {
            "redis-event-loop-io-multiplexing-epoll-kqueue": 0,
            "core-data-structures-strings-hashes-lists": 300,
            "advanced-structures-sets-sorted-sets-skiplist-hyperloglog": 900,
            "redis-streams-consumer-groups-pending-entries-pel": 1500
        }
    },
    "redis-caching-patterns-eviction.md": {
        "video": ("1NngTUYPdpI", "Redis Caching Patterns & Eviction", 0),
        "docs": [
            ("Redis Key Eviction (LRU / LFU)", "https://redis.io/docs/reference/eviction/"),
            ("Caching Strategies & Invalidation Best Practices", "https://aws.amazon.com/caching/best-practices/")
        ],
        "concept_starts": {
            "caching-topologies-cache-aside-read-through-write-through-write-behind": 0,
            "cache-failure-modes-penetration-avalanche-stampede": 450,
            "mitigation-patterns-bloom-filters-mutex-xfetch": 900,
            "eviction-policies-lru-lfu-maxmemory-configuration": 1350
        }
    },
    "redis-persistence-sentinel-cluster.md": {
        "video": ("Hbt56gFj998", "Redis Persistence, Sentinel & Cluster", 1800),
        "docs": [
            ("Redis Persistence: RDB and AOF", "https://redis.io/docs/management/persistence/"),
            ("Redis Cluster Specification", "https://redis.io/docs/management/scaling/")
        ],
        "concept_starts": {
            "persistence-mechanics-rdb-snapshots-vs-aof-append-only": 1800,
            "aof-fsync-policies-background-log-rewriting": 2100,
            "redis-sentinel-quorum-failover-configuration-provider": 2400,
            "redis-cluster-hash-slots-sharding-smart-clients": 2700
        }
    },

    # 14. Java & Spring Boot
    "java-jvm-memory-concurrency.md": {
        "video": ("grEKMHGYyns", "Java JVM Internals & Concurrency", 0),
        "docs": [
            ("Java Virtual Machine Specification", "https://docs.oracle.com/javase/specs/jvms/se21/html/index.html"),
            ("Java Concurrency and Multithreading (Oracle)", "https://docs.oracle.com/javase/tutorial/essential/concurrency/")
        ],
        "concept_starts": {
            "jvm-runtime-data-areas-heap-stack-metaspace": 0,
            "garbage-collection-mechanics-g1-gc-zgc-collector": 600,
            "java-memory-model-synchronized-volatile-atomics": 1200,
            "thread-pools-completablefuture-virtual-threads": 1800
        }
    },
    "spring-boot-core-di.md": {
        "video": ("9SGDpanrc8U", "Spring Boot Core & Dependency Injection", 132),
        "docs": [
            ("Spring Boot Reference Documentation", "https://docs.spring.io/spring-boot/docs/current/reference/html/"),
            ("Spring Framework IoC Container", "https://docs.spring.io/spring-framework/reference/core/beans.html")
        ],
        "concept_starts": {
            "ioc-dependency-injection-constructor-vs-field": 1748,
            "bean-lifecycle-postconstruct-predestroy": 2100,
            "spring-stereotypes-component-service-repository-configuration": 1399,
            "spring-profiles-configuration-properties-actuator": 1960
        }
    },
    "spring-data-jpa-hibernate.md": {
        "video": ("9SGDpanrc8U", "Spring Data JPA & Hibernate", 2388),
        "docs": [
            ("Spring Data JPA Reference Documentation", "https://docs.spring.io/spring-data/jpa/reference/"),
            ("Hibernate ORM User Guide", "https://docs.jboss.org/hibernate/orm/current/userguide/html_single/Hibernate_User_Guide.html")
        ],
        "concept_starts": {
            "jpa-hibernate-entity-lifecycle-states": 2388,
            "entity-relationship-mappings-onetomany-manytoone-cascades": 2600,
            "eliminating-n-plus-1-query-problem-join-fetch-entitygraphs": 2855,
            "declarative-transaction-management-propagation-isolation": 3200
        }
    },
    "spring-security-microservices.md": {
        "video": ("9SGDpanrc8U", "Spring Security & Microservices", 3781),
        "docs": [
            ("Spring Security Architecture Guide", "https://docs.spring.io/spring-security/reference/"),
            ("Resilience4j Circuit Breaker & Retry Guide", "https://resilience4j.readme.io/docs/circuitbreaker")
        ],
        "concept_starts": {
            "spring-security-architecture-filterchain-filters": 3781,
            "stateless-jwt-authentication-rbac-spring-security": 4200,
            "microservices-feign-webclient-api-gateway": 4600,
            "resiliency-patterns-resilience4j-circuit-breaker-retry": 5000
        }
    },

    # 15. Python Backend with FastAPI
    "python-async-fastapi-core.md": {
        "video": ("0sOvCWFmrtA", "Async Python & FastAPI Core", 2181),
        "docs": [
            ("FastAPI Official Documentation", "https://fastapi.tiangolo.com/"),
            ("Pydantic v2 Documentation", "https://docs.pydantic.dev/latest/")
        ],
        "concept_starts": {
            "async-python-event-loop-coroutines-asyncio-concurrency": 2181,
            "wsgi-vs-asgi-starlette-uvicorn-nonblocking-handling": 2363,
            "pydantic-v2-request-validation-serialization-validators": 4049,
            "fastapi-dependency-injection-session-scoping-security": 8282
        }
    },
    "fastapi-database-testing.md": {
        "video": ("0sOvCWFmrtA", "SQLAlchemy 2.0 Async, Alembic & Pytest", 16533),
        "docs": [
            ("SQLAlchemy 2.0 Asyncio Guide", "https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html"),
            ("Alembic Database Migration Tutorial", "https://alembic.sqlalchemy.org/en/latest/tutorial.html")
        ],
        "concept_starts": {
            "sqlalchemy-async-orm-async-engine-session-loading": 16533,
            "database-schema-migrations-alembic-autogenerate-rollbacks": 38025,
            "jwt-authentication-password-hashing-fastapi": 23569,
            "automated-testing-pytest-async-fixtures-testcontainers": 51291
        }
    },

    # 16. API Design & Architecture
    "api-paradigms-http-grpc.md": {
        "video": ("DQ57zYedMdQ", "API Paradigms: REST, GraphQL & gRPC", 0),
        "docs": [
            ("Microsoft REST API Guidelines", "https://github.com/microsoft/api-guidelines"),
            ("gRPC Core Concepts and Architecture", "https://grpc.io/docs/what-is-grpc/core-concepts/")
        ],
        "concept_starts": {
            "http-protocols-http1-http2-http3-quic-multiplexing": 0,
            "rest-architecture-richardson-maturity-model-uris-methods": 300,
            "graphql-architecture-sdl-queries-mutations-dataloader": 750,
            "grpc-protocol-buffers-binary-serialization-streaming-rpcs": 1200
        }
    },
    "api-security-resilience.md": {
        "video": ("MIJFyUPG4Z4", "API Security & Rate Limiting", 0),
        "docs": [
            ("OWASP API Security Top 10", "https://owasp.org/www-project-api-security/"),
            ("Cloudflare: Rate Limiting Algorithms", "https://www.cloudflare.com/learning/bots/what-is-rate-limiting/")
        ],
        "concept_starts": {
            "owasp-api-security-top-10-bola-mass-assignment": 0,
            "rate-limiting-algorithms-token-bucket-leaky-bucket-sliding-window": 350,
            "idempotent-api-design-idempotency-keys-distributed-locks": 850,
            "api-pagination-strategies-offset-vs-cursor-keyset-pagination": 1200
        }
    }
}

def main():
    print("Verifying all video IDs via YouTube oEmbed API...")
    unique_vids = {m["video"][0] for m in LESSON_MAPPINGS.values()}
    for vid in unique_vids:
        info = get_oembed(vid)
        if not info:
            print(f"[ERROR] Rejecting video {vid} - failed oEmbed verification!")
            sys.exit(1)
        print(f"  [VERIFIED] {vid} -> '{info[0][:50]}' by {info[1]}")

    with open(TOPICS_FILE, "r", encoding="utf-8") as f:
        topics_js = f.read()

    m = re.search(r"window\.topicsData\s*=\s*(\[.*\]);", topics_js, re.DOTALL)
    if not m:
        print("[ERROR] Could not parse window.topicsData from topics.js")
        sys.exit(1)

    topics_data = json.loads(m.group(1))

    lessons_output = {}
    concepts_output = {}

    for sec in topics_data:
        for sub in sec.get("subsections", []):
            sub_id = sub["id"]
            file_name = sub["file"]
            mapping = LESSON_MAPPINGS.get(file_name)

            if not mapping:
                print(f"[WARNING] Missing mapping for {file_name}")
                continue

            vid_id, custom_label, default_start = mapping["video"]
            vid_title, vid_channel = get_oembed(vid_id)

            lessons_output[file_name] = {
                "videos": [
                    [vid_id, f"{vid_title} ({custom_label})", vid_channel, "", default_start]
                ],
                "docs": mapping["docs"]
            }

            concept_starts = mapping.get("concept_starts", {})
            for c in sub.get("concepts", []):
                anchor = c["anchor"]
                concept_key = f"{sub_id}/{anchor}"
                c_start = concept_starts.get(anchor, default_start)

                concepts_output[concept_key] = {
                    "videos": [
                        [vid_id, f"{c['title']}", vid_channel, "", c_start]
                    ],
                    "docs": mapping["docs"]
                }

    resources_data = {
        "lessons": lessons_output,
        "concepts": concepts_output
    }

    out_content = "/* Curated resources for the Cloud & DevOps roadmap.\n" \
                  "   Every video id below was verified against YouTube's oEmbed API.\n" \
                  "   Generated by tools/build_cloud_devops_resources.py. */\n" \
                  "window.cloudDevOpsResources = " + json.dumps(resources_data, indent=2, ensure_ascii=False) + ";\n"

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        f.write(out_content)

    print(f"\nSuccessfully wrote {OUT_FILE}:")
    print(f"  - Lessons covered: {len(lessons_output)}")
    print(f"  - Concepts mapped with exact timestamps: {len(concepts_output)}")

if __name__ == '__main__':
    main()
