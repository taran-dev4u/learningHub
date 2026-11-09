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

DOCKER_SUBSECTIONS = [
    {
        "num": "6.1",
        "title": "Container Architecture, OCI Standards & Linux Kernel Primitives",
        "desc": "Operating system level virtualization, Linux kernel namespaces, control groups (cgroups v1/v2), union filesystems (OverlayFS), and OCI runtime specifications.",
        "concepts": [
            ("6.1.1", "Linux Kernel Primitives: Namespaces (PID, NET, MNT, IPC, UTS, USER) & cgroups v1/v2 Resource Accounting",
             "Isolation mechanics: PID namespace tree virtualization, mount propagation (rshared, rprivate), network interface sandbox, cgroups v2 unified hierarchy, CPU shares vs quota, and memory hard/soft limits.",
             "https://www.youtube.com/watch?v=3c-iBn73dDE&t=118s", "00:00", "TechWorld with Nana", "https://docs.docker.com/get-started/overview/"),
            ("6.1.2", "Union File Systems, Storage Drivers & Copy-on-Write (OverlayFS Mechanics)",
             "OverlayFS layer stacking: lowerdir (read-only image layers), upperdir (writable container layer), mergeddir (unified view), copy-on-write latency penalty on first write, and inode overhead.",
             "https://www.youtube.com/watch?v=3c-iBn73dDE&t=656s", "00:00", "TechWorld with Nana", "https://docs.docker.com/storage/storagedriver/overlayfs-driver/"),
            ("6.1.3", "OCI Specifications & Container Runtimes: OCI Runtime Spec, runc, containerd & CRI-O",
             "Container ecosystem standards: Open Container Initiative (OCI) image/runtime specifications, low-level runtimes (runc, crun), daemonless execution, containerd socket interfaces, and CRI abstraction.",
             "https://www.youtube.com/watch?v=3c-iBn73dDE&t=1180s", "00:00", "TechWorld with Nana", "https://opencontainers.org/"),
            ("6.1.4", "Containers vs Virtual Machines: Resource Isolation, Hypervisors & Overhead Comparison",
             "Architectural trade-offs: Type-1/Type-2 hypervisors with guest OS kernels vs shared host kernel with namespace boundaries; startup latency (milliseconds vs minutes), memory footprint, and kernel vulnerability isolation.",
             "https://www.youtube.com/watch?v=3c-iBn73dDE&t=1433s", "00:00", "TechWorld with Nana", "https://docs.docker.com/get-started/overview/")
        ]
    },
    {
        "num": "6.2",
        "title": "Dockerfile Engineering, Multi-Stage Builds & Image Optimization",
        "desc": "Production Dockerfile best practices, exec vs shell form execution semantics, multi-stage build minimization, and layer caching optimization.",
        "concepts": [
            ("6.2.1", "Dockerfile Directives & Execution Semantics: ENTRYPOINT vs CMD, RUN vs COPY vs ADD",
             "Exec vs Shell form JSON array semantics, ENTRYPOINT default executable with CMD arguments, RUN layer creation, COPY vs ADD tar auto-extraction, and ARG build-time vs ENV runtime environment variables.",
             "https://www.youtube.com/watch?v=3c-iBn73dDE&t=6122s", "00:00", "TechWorld with Nana", "https://docs.docker.com/develop/develop-images/dockerfile_best-practices/"),
            ("6.2.2", "Multi-Stage Builds: Build Arguments, Target Stages & Minimizing Attack Surface",
             "Stage inheritance (FROM ... AS builder), copying build artifacts into clean runtime stages (COPY --from=builder), reducing production image sizes by 90%+, and selective targets (--target test/prod).",
             "https://www.youtube.com/watch?v=3c-iBn73dDE&t=6480s", "00:00", "TechWorld with Nana", "https://docs.docker.com/build/building/multi-stage/"),
            ("6.2.3", "BuildKit Engine, Cache Mounts & Layer Optimization Strategies",
             "Next-generation BuildKit: parallel DAG execution, secret mounting (--mount=type=secret), persistent package cache mounts (--mount=type=cache), and ordering dependencies to maximize layer cache hits.",
             "https://www.youtube.com/watch?v=3c-iBn73dDE&t=6800s", "00:00", "TechWorld with Nana", "https://docs.docker.com/build/buildkit/"),
            ("6.2.4", "Multi-Architecture Images: Buildx, QEMU Emulation & OCI Manifest Lists",
             "Cross-compilation across amd64, arm64 (Apple Silicon/Graviton), buildx builder instances, binfmt_misc QEMU emulation, and creating unified multi-arch manifest lists with docker manifest inspect.",
             "https://www.youtube.com/watch?v=3c-iBn73dDE&t=7200s", "00:00", "TechWorld with Nana", "https://docs.docker.com/build/building/multi-platform/")
        ]
    },
    {
        "num": "6.3",
        "title": "Container Security, Hardening & Image Supply Chain",
        "desc": "Principle of least privilege, non-root users, security capabilities bounding, seccomp filters, minimal distroless base images, and vulnerability scanning.",
        "concepts": [
            ("6.3.1", "Principle of Least Privilege: Non-Root Users, USER Directive & Rootless Docker",
             "Preventing root escalation: dedicated non-root UID/GID creation, USER directive, rootless daemon configuration running under user namespaces, and read-only root filesystems (--read-only).",
             "https://www.youtube.com/watch?v=3c-iBn73dDE&t=7100s", "00:00", "TechWorld with Nana", "https://docs.docker.com/engine/security/rootless/"),
            ("6.3.2", "Linux Security Capabilities (cap-add/cap-drop), Seccomp Profiles & AppArmor",
             "Granular capability bounding: dropping default capabilities (CAP_DROP ALL, CAP_ADD NET_BIND_SERVICE), default seccomp syscall filtering filters (blocking ~44 dangerous syscalls), and AppArmor profile loading.",
             "https://www.youtube.com/watch?v=Gjnup-PuquQ", "00:00", "Fireship", "https://docs.docker.com/engine/security/seccomp/"),
            ("6.3.3", "Minimal Base Images: Distroless, Alpine vs Debian Slim & Stripping Compilers",
             "Attack surface reduction: Google Distroless runtime images containing only application binaries and dependencies (no shell, package manager, or glibc vulnerabilities), musl libc quirks in Alpine vs Debian Slim.",
             "https://www.youtube.com/watch?v=eGzB9xuiQtY", "00:00", "NetworkChuck", "https://github.com/GoogleContainerTools/distroless"),
            ("6.3.4", "Container Supply Chain Security: Trivy / Grype Vulnerability Scanning, SBOM & Cosign Signing",
             "CI/CD vulnerability scanning with Trivy/Grype, Software Bill of Materials (SBOM) generation (Syft, CycloneDX), cryptographic image signing with Sigstore Cosign, and provenance verification.",
             "https://www.youtube.com/watch?v=X48VuDVv0do&t=1000s", "00:00", "TechWorld with Nana", "https://docs.docker.com/scout/")
        ]
    },
    {
        "num": "6.4",
        "title": "Docker Networking Architecture & Traffic Routing",
        "desc": "Virtual Ethernet (veth) pairs, bridge networking, iptables NAT rules, embedded DNS resolver, and multi-host overlay networks.",
        "concepts": [
            ("6.4.1", "Docker Network Drivers: Bridge (docker0, veth pairs), Host, None & Macvlan",
             "Virtual Ethernet (veth) pair bridging, default bridge vs user-defined bridge networks, host driver bypassing network namespace for zero-overhead, none isolation, and direct L2 macvlan routing.",
             "https://www.youtube.com/watch?v=3c-iBn73dDE&t=2522s", "00:00", "TechWorld with Nana", "https://docs.docker.com/network/"),
            ("6.4.2", "Port Mapping, iptables NAT Rules & Embedded DNS Resolver (127.0.0.11)",
             "Port forwarding mechanics (-p 8080:80), docker0 iptables PREROUTING DNAT rules, container name resolution via embedded DNS server on 127.0.0.11, and automatic network alias routing.",
             "https://www.youtube.com/watch?v=bKFMS5C4CG0", "00:00", "Hussein Nasser", "https://docs.docker.com/network/packet-filtering-firewalls/"),
            ("6.4.3", "Multi-Host Overlay Networking, VXLAN Encapsulation & Distributed Service Discovery",
             "Cross-host container communication: VXLAN encapsulation on UDP port 4789, overlay network control plane, gossip protocols, and virtual IP (VIP) load balancing across distributed nodes.",
             "https://www.youtube.com/watch?v=3c-iBn73dDE&t=3200s", "00:00", "TechWorld with Nana", "https://docs.docker.com/network/drivers/overlay/"),
            ("6.4.4", "Network Debugging: Inspecting veth Interfaces, ip netns & tcpdump in Container Namespaces",
             "Troubleshooting connectivity: linking container network namespaces with nsenter / ip netns, tracing packet drops with iptables -L -n -v, and running tcpdump inside container network namespaces.",
             "https://www.youtube.com/watch?v=7bWzT_k98Ls", "00:00", "NetworkChuck", "https://docs.docker.com/network/troubleshoot/")
        ]
    },
    {
        "num": "6.5",
        "title": "Docker Storage, Volume Plugins & Persistent Data Management",
        "desc": "Named volumes, bind mounts, tmpfs in-memory storage, volume driver plugins, and database copy-on-write performance optimization.",
        "concepts": [
            ("6.5.1", "Storage Types: Named Volumes (/var/lib/docker/volumes), Bind Mounts & tmpfs",
             "Storage mechanics: Docker-managed named volumes outside UnionFS, host-managed bind mounts (-v /host:/container), tmpfs memory-backed ephemeral storage, and SELinux relabeling (:z, :Z flags).",
             "https://www.youtube.com/watch?v=3c-iBn73dDE&t=8846s", "00:00", "TechWorld with Nana", "https://docs.docker.com/storage/"),
            ("6.5.2", "Volume Driver Plugins: Cloud Storage Backends (NFS, EFS, AWS EBS) & Backup Strategies",
             "Remote volume plugins for shared multi-host persistence (NFS, AWS EFS, Ceph), automated volume backup containers using tar pipelines, and point-in-time snapshot strategies.",
             "https://www.youtube.com/watch?v=3c-iBn73dDE&t=9200s", "00:00", "TechWorld with Nana", "https://docs.docker.com/storage/volumes/"),
            ("6.5.3", "Copy-on-Write Performance: Database I/O Overhead on OverlayFS vs Volume Mounts",
             "High-throughput write penalties: why running databases (PostgreSQL, MySQL, Redis) on UnionFS leads to severe fragmentation and performance degradation; benchmark comparisons with raw volumes.",
             "https://www.youtube.com/watch?v=3c-iBn73dDE&t=9400s", "00:00", "TechWorld with Nana", "https://docs.docker.com/storage/storagedriver/"),
            ("6.5.4", "Data Migration, Volume Permissions (chown, UID/GID matching) & Orphan Cleanup",
             "Solving permission denied errors: matching container runtime UID/GID with host directory permissions, fixuid workarounds, volume data migration across hosts, and pruning orphan volumes.",
             "https://www.youtube.com/watch?v=0O6y_C_PZ4M", "00:00", "Jeff Geerling", "https://docs.docker.com/storage/volumes/#use-a-volume-to-initialize-data")
        ]
    },
    {
        "num": "6.6",
        "title": "Multi-Container Orchestration with Docker Compose & Operations",
        "desc": "Declarative multi-container orchestration, compose.yaml specification, service dependency sequencing, healthchecks, and production daemon operations.",
        "concepts": [
            ("6.6.1", "Docker Compose Specification: Services, Networks, Volumes & Environment Variables (.env)",
             "Declarative multi-container stacks: compose.yaml specification, service definitions, environment interpolation ($&#123;VAR:-default&#125;), volume definitions, and custom network topologies.",
             "https://www.youtube.com/watch?v=3c-iBn73dDE&t=9540s", "00:00", "TechWorld with Nana", "https://docs.docker.com/compose/"),
            ("6.6.2", "Service Dependencies & Startup Sequencing: depends_on, Condition Checks & Healthchecks",
             "Reliable boot ordering: depends_on with condition: service_healthy, configuring HEALTHCHECK intervals, retries, and start_period to eliminate race conditions between database and web services.",
             "https://www.youtube.com/watch?v=SXwC9fSwct8", "00:00", "TechWorld with Nana", "https://docs.docker.com/compose/startup-order/"),
            ("6.6.3", "Docker Daemon Operations: daemon.json Configuration, Live-Restore & Log Drivers",
             "Production daemon configuration: /etc/docker/daemon.json, live-restore (preventing container restarts on daemon upgrades), log rotation policies (max-size, max-file), and log forwarders (json-file, syslog, fluentd).",
             "https://www.youtube.com/watch?v=3c-iBn73dDE&t=10100s", "00:00", "TechWorld with Nana", "https://docs.docker.com/config/daemon/"),
            ("6.6.4", "Production Troubleshooting & Monitoring: docker stats, cAdvisor, docker inspect & Event Streams",
             "Telemetry and operational diagnostics: real-time CPU/memory utilization with docker stats, cAdvisor container profiling, deep JSON schema querying with docker inspect --format, and docker events audit logs.",
             "https://www.youtube.com/watch?v=3c-iBn73dDE&t=10500s", "00:00", "TechWorld with Nana", "https://docs.docker.com/engine/reference/commandline/stats/")
        ]
    }
]

K8S_SUBSECTIONS = [
    {
        "num": "7.1",
        "title": "Kubernetes Architecture, Control Plane & Core Components",
        "desc": "Master control plane internals (kube-apiserver, etcd Raft consensus, kube-scheduler, controller-manager), worker node daemons (kubelet, kube-proxy, CRI), and declarative reconciliation.",
        "concepts": [
            ("7.1.1", "Control Plane Architecture: kube-apiserver, etcd Distributed Consensus & Raft Quorum",
             "Master node internals: kube-apiserver REST API gateway, etcd distributed key-value store, Raft consensus quorum calculation (2N+1 nodes), etcd compaction, defragmentation, and encryption at rest.",
             "https://www.youtube.com/watch?v=X48VuDVv0do&t=1349s", "00:00", "TechWorld with Nana", "https://kubernetes.io/docs/concepts/overview/components/"),
            ("7.1.2", "Scheduling & Orchestration: kube-scheduler Decision Algorithm & Controller-Manager Reconciliation Loops",
             "Scheduling pipeline: filtering (predicates), scoring (priorities), node selection; and kube-controller-manager non-terminating reconciliation loops (NodeController, DeploymentController, EndpointSliceController).",
             "https://www.youtube.com/watch?v=X48VuDVv0do&t=1650s", "00:00", "TechWorld with Nana", "https://kubernetes.io/docs/concepts/scheduling-eviction/kube-scheduler/"),
            ("7.1.3", "Worker Node Architecture: Kubelet Lifecycle, CRI-O/containerd & kube-proxy (iptables vs IPVS)",
             "Worker node execution: Kubelet pod spec sync, cgroup driver (systemd vs cgroupfs), Container Runtime Interface (CRI), kube-proxy network routing (iptables O(N) linear chains vs IPVS O(1) hash tables).",
             "https://www.youtube.com/watch?v=X48VuDVv0do&t=1820s", "00:00", "TechWorld with Nana", "https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet/"),
            ("7.1.4", "Declarative Object Model: Desired State vs Actual State Reconciliation & kubectl Context Flow",
             "Declarative YAML specifications: apiVersion, kind, metadata, spec, status; client-side vs server-side apply (SSA), kubeconfig cluster/context/user configuration, and API request interceptor pipeline.",
             "https://www.youtube.com/watch?v=X48VuDVv0do&t=2692s", "00:00", "TechWorld with Nana", "https://kubernetes.io/docs/concepts/overview/working-with-objects/")
        ]
    },
    {
        "num": "7.2",
        "title": "Workload Management: Pod Lifecycle, Deployments & Rollouts",
        "desc": "Pod anatomy, multi-container patterns (Init, Sidecar, Ephemeral), health probes, Deployments, ReplicaSets, and zero-downtime rolling update strategies.",
        "concepts": [
            ("7.2.1", "Pod Anatomy & Lifecycle: Init Containers, Sidecar Containers & Ephemeral Containers",
             "Pod primitives: shared network/IPC namespace, Pod phases (Pending, Running, Succeeded, Failed, Unknown), ordered Init Container execution, native K8s 1.28+ Sidecar containers, and Ephemeral debug containers.",
             "https://www.youtube.com/watch?v=X48VuDVv0do&t=320s", "00:00", "TechWorld with Nana", "https://kubernetes.io/docs/concepts/workloads/pods/"),
            ("7.2.2", "Pod Health Diagnostics: Liveness, Readiness & Startup Probes Configuration & Mechanics",
             "Health check mechanics: HTTPGet, Exec, TCPSocket, gRPC probes; Startup probes protecting slow initialization, Liveness restarting failed containers, Readiness removing unhealthy pods from Service endpoints.",
             "https://www.youtube.com/watch?v=X48VuDVv0do&t=1500s", "00:00", "TechWorld with Nana", "https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/"),
            ("7.2.3", "Deployments & ReplicaSets: Managing Stateless Workloads & Rollout History",
             "Managing replicated workloads: Deployment controller supervising ReplicaSets, declarative replicas count, pod template hashes, zero-downtime rollouts, revision history, and rollback with kubectl rollout undo.",
             "https://www.youtube.com/watch?v=X48VuDVv0do&t=850s", "00:00", "TechWorld with Nana", "https://kubernetes.io/docs/concepts/workloads/controllers/deployment/"),
            ("7.2.4", "Rollout Strategies: RollingUpdate (maxSurge, maxUnavailable), Blue-Green & Canary Traffic Shifting",
             "Deployment update algorithms: RollingUpdate tuning (maxSurge, maxUnavailable percentages), Blue-Green manual selector switching, and automated Canary deployments with traffic splitting and progressive analysis.",
             "https://www.youtube.com/watch?v=X48VuDVv0do&t=1150s", "00:00", "TechWorld with Nana", "https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#strategy")
        ]
    },
    {
        "num": "7.3",
        "title": "Advanced Stateful & Batch Workload Controllers",
        "desc": "Managing stateful workloads with StatefulSets, node-level agent scheduling with DaemonSets, and batch processing with one-shot Jobs and scheduled CronJobs.",
        "concepts": [
            ("7.3.1", "StatefulSets: Stable Network IDs, Headless Services & VolumeClaimTemplates",
             "Managing stateful applications: deterministic zero-indexed pod identity (pod-0, pod-1), dedicated DNS subdomains via Headless Services (ClusterIP: None), and dynamic per-pod VolumeClaimTemplates.",
             "https://www.youtube.com/watch?v=pPQKAR1pA9U", "00:00", "TechWorld with Nana", "https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/"),
            ("7.3.2", "StatefulSet Operations: Ordered Graceful Termination, Scaling & Partitioned Updates",
             "Stateful operational lifecycle: ordered sequential provisioning (0 to N-1), reverse termination order (N-1 to 0), Parallel podManagementPolicy, and staged canary updates with updateStrategy.rollingUpdate.partition.",
             "https://www.youtube.com/watch?v=X48VuDVv0do&t=10718s", "00:00", "TechWorld with Nana", "https://kubernetes.io/docs/tasks/run-application/run-replicated-stateful-application/"),
            ("7.3.3", "DaemonSets: Node-Level Agent Scheduling (Logging, CNI, Monitoring) & Rolling Updates",
             "Running pods on all nodes: DaemonSet controller mechanics, ignoring node unschedulable taints, rolling update strategies, and real-world deployment of log forwarders (Fluentbit), CNI (Calico), and node-exporter.",
             "https://www.youtube.com/watch?v=X48VuDVv0do&t=11150s", "00:00", "TechWorld with Nana", "https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/"),
            ("7.3.4", "Batch Workloads: One-Shot Jobs, Parallelism, Completions & Scheduled CronJobs",
             "Batch processing patterns: Job controller restarting pods until completions reached, parallelism limits, backoffLimit retry counts, CronJob cron expressions, concurrencyPolicy (Allow, Forbid, Replace), and missed schedules.",
             "https://www.youtube.com/watch?v=X48VuDVv0do&t=11500s", "00:00", "TechWorld with Nana", "https://kubernetes.io/docs/concepts/workloads/controllers/job/")
        ]
    },
    {
        "num": "7.4",
        "title": "Kubernetes Networking Primitives, CNI & Service Topologies",
        "desc": "Flat pod-to-pod network model, CNI network plugins (Calico, Cilium, eBPF), Service discovery types, CoreDNS, Ingress controllers, and the modern Kubernetes Gateway API.",
        "concepts": [
            ("7.4.1", "Flat Pod-to-Pod Network Model & Container Network Interface (CNI: Calico, Cilium, eBPF)",
             "Cluster networking model: every pod gets a unique routable IP without NAT; CNI plugin comparison: Calico (BGP / VXLAN / WireGuard) vs Cilium (eBPF kernel bypass, XDP high-throughput packet processing).",
             "https://www.youtube.com/watch?v=6r_mZ4x_W2Y", "00:00", "Hussein Nasser", "https://kubernetes.io/docs/concepts/cluster-administration/networking/"),
            ("7.4.2", "Service Discovery & Types: ClusterIP (Internal), NodePort, LoadBalancer & Headless Services",
             "Stable Layer-4 virtual endpoints: ClusterIP internal routing, NodePort high-port exposure (30000-32767), cloud provider LoadBalancer provisioning, and Headless services for direct pod IP resolution.",
             "https://www.youtube.com/watch?v=X48VuDVv0do&t=4500s", "00:00", "TechWorld with Nana", "https://kubernetes.io/docs/concepts/services-networking/service/"),
            ("7.4.3", "CoreDNS Architecture: Internal DNS Records (.default.svc.cluster.local), Resolv.conf & ndots",
             "In-cluster name resolution: CoreDNS plugin chain, fully qualified domain names (service.namespace.svc.cluster.local), resolving SRV records for ports, and the ndots:5 DNS query amplification issue.",
             "https://www.youtube.com/watch?v=X48VuDVv0do&t=4800s", "00:00", "TechWorld with Nana", "https://kubernetes.io/docs/tasks/administer-cluster/dns-custom-nameservers/"),
            ("7.4.4", "Ingress Controllers (Nginx Ingress, Traefik) & Kubernetes Gateway API (HTTPRoute, GRPCRoute)",
             "Layer-7 routing: Ingress resources, IngressClass controllers (ingress-nginx, Traefik), SSL/TLS termination, and modern Gateway API role-oriented decoupling (GatewayClass, Gateway, HTTPRoute, GRPCRoute).",
             "https://www.youtube.com/watch?v=80Ew_fsV4rM", "00:00", "TechWorld with Nana", "https://gateway-api.sigs.k8s.io/")
        ]
    },
    {
        "num": "7.5",
        "title": "Configuration Management, Secrets & Storage (CSI)",
        "desc": "Decoupled configuration with ConfigMaps, secure Secrets management, Container Storage Interface (CSI), dynamic PersistentVolume provisioning, and volume snapshots.",
        "concepts": [
            ("7.5.1", "ConfigMaps & Environment Variables: Key-Value Stores, Volume Projections & Hot-Reloading",
             "Decoupling configuration from container images: ConfigMap creation from files/literals, injecting via env/envFrom, mounting as volume projections, and automatic symlink hot-reloading vs atomic restarts.",
             "https://www.youtube.com/watch?v=X48VuDVv0do&t=5200s", "00:00", "TechWorld with Nana", "https://kubernetes.io/docs/concepts/configuration/configmap/"),
            ("7.5.2", "Secrets Management: Base64 Encoding vs Encryption at Rest & HashiCorp Vault / External Secrets",
             "Securing sensitive data: Secret types (Opaque, TLS, docker-registry), why base64 is not encryption, KMS envelope encryption at rest, SealedSecrets, and External Secrets Operator integrating with Vault/AWS Secrets.",
             "https://www.youtube.com/watch?v=X48VuDVv0do&t=5600s", "00:00", "TechWorld with Nana", "https://kubernetes.io/docs/concepts/configuration/secret/"),
            ("7.5.3", "Container Storage Interface (CSI): StorageClasses, Dynamic Provisioning & PV / PVC Binding",
             "Storage decoupling: PersistentVolumes (PV) cluster resources, PersistentVolumeClaims (PVC) requests, StorageClasses defining dynamic provisioners (gp3, standard), reclaim policies (Retain, Delete), and CSI hooks.",
             "https://www.youtube.com/watch?v=X48VuDVv0do&t=8200s", "00:00", "TechWorld with Nana", "https://kubernetes.io/docs/concepts/storage/persistent-volumes/"),
            ("7.5.4", "Storage Access Modes (RWO, ROX, RWX) & Stateful Volume Expansion / Snapshots",
             "Volume capability matrix: ReadWriteOnce (single node), ReadOnlyMany, ReadWriteMany (shared NFS/EFS), online volume expansion (allowVolumeExpansion: true), and VolumeSnapshot custom resources.",
             "https://www.youtube.com/watch?v=X48VuDVv0do&t=8600s", "00:00", "TechWorld with Nana", "https://kubernetes.io/docs/concepts/storage/volume-snapshots/")
        ]
    },
    {
        "num": "7.6",
        "title": "Pod Scheduling, Node Affinity & Cluster Placement",
        "desc": "Fine-grained pod placement, nodeSelector, node affinity/anti-affinity, taints and tolerations, topology spread constraints, resource quotas, and PriorityClasses.",
        "concepts": [
            ("7.6.1", "Node Selection & Node Affinity / Anti-Affinity (Required vs Preferred During Scheduling)",
             "Constraining pod placement: nodeSelector label matching, nodeAffinity (requiredDuringSchedulingIgnoredDuringExecution hard rules vs preferredDuringScheduling soft rules), and matching expressions (In, NotIn, Exists).",
             "https://www.youtube.com/watch?v=X48VuDVv0do&t=9000s", "00:00", "TechWorld with Nana", "https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/"),
            ("7.6.2", "Taints and Tolerations: Dedicated Node Pools, Master Protection & NoSchedule/NoExecute",
             "Repelling pods from nodes: node taints (Key=Value:Effect), effects (NoSchedule, PreferNoSchedule, NoExecute eviction), pod tolerations, and dedicated GPU / compute node isolation.",
             "https://www.youtube.com/watch?v=X48VuDVv0do&t=9300s", "00:00", "TechWorld with Nana", "https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/"),
            ("7.6.3", "Pod Anti-Affinity & Pod Topology Spread Constraints: High Availability across Failure Zones",
             "Spreading pods across failure domains: podAntiAffinity preventing co-locating replicas on the same node/zone, and TopologySpreadConstraints (maxSkew, topologyKey: topology.kubernetes.io/zone, whenUnsatisfiable).",
             "https://www.youtube.com/watch?v=X48VuDVv0do&t=9600s", "00:00", "TechWorld with Nana", "https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/"),
            ("7.6.4", "Resource Quotas, LimitRanges, PriorityClasses & Preemption Eviction Logic",
             "Resource governance: LimitRanges enforcing default/max requests and limits per container, ResourceQuotas capping total CPU/memory/pods per namespace, and PriorityClasses with preemption eviction.",
             "https://www.youtube.com/watch?v=X48VuDVv0do&t=9800s", "00:00", "TechWorld with Nana", "https://kubernetes.io/docs/concepts/policy/resource-quotas/")
        ]
    },
    {
        "num": "7.7",
        "title": "Cluster Security, Access Control & Micro-Segmentation",
        "desc": "Zero-trust Kubernetes security: RBAC authorization, Pod Security Standards (PSS/PSA), NetworkPolicies micro-segmentation, and policy-as-code admission control.",
        "concepts": [
            ("7.7.1", "Authentication & Authorization: X.509 Client Certs, ServiceAccounts & Granular RBAC",
             "Identity and access control: X.509 client certificates, OIDC tokens, ServiceAccounts with bound tokens, and Role-Based Access Control (RBAC): Roles, ClusterRoles, RoleBindings, ClusterRoleBindings.",
             "https://www.youtube.com/watch?v=X48VuDVv0do&t=7500s", "00:00", "TechWorld with Nana", "https://kubernetes.io/docs/reference/access-authn-authz/rbac/"),
            ("7.7.2", "Pod Security Standards (PSS) & Admission (PSA): Privileged, Baseline, Restricted Profiles",
             "Replacing deprecated PSPs: built-in Pod Security Admission controller, three security standard profiles (Privileged, Baseline, Restricted), and namespace labeling modes (enforce, audit, warn).",
             "https://www.youtube.com/watch?v=PivpCKEiQOQ", "00:00", "Fireship", "https://kubernetes.io/docs/concepts/security/pod-security-standards/"),
            ("7.7.3", "NetworkPolicies: Pod-Level Micro-Segmentation, Ingress / Egress Rules & Default Deny",
             "East-west firewalling: NetworkPolicy resources, podSelector, ingress from / egress to CIDRs, namespaceSelectors, podSelectors, and establishing default-deny ingress and egress zero-trust profiles.",
             "https://www.youtube.com/watch?v=X48VuDVv0do&t=7800s", "00:00", "TechWorld with Nana", "https://kubernetes.io/docs/concepts/services-networking/network-policies/"),
            ("7.7.4", "Policy as Code & Security Auditing: OPA Gatekeeper / Kyverno, Kube-bench CIS Benchmarks",
             "Admission webhook governance: ValidatingWebhookConfiguration, MutatingWebhookConfiguration, Kyverno YAML policies vs OPA Rego constraint templates, and CIS benchmark auditing with kube-bench.",
             "https://www.youtube.com/watch?v=X48VuDVv0do&t=8000s", "00:00", "TechWorld with Nana", "https://open-policy-agent.github.io/gatekeeper/website/docs/")
        ]
    },
    {
        "num": "7.8",
        "title": "Cluster Auto-scaling, Observability & GitOps Operations",
        "desc": "Horizontal Pod Autoscaler (HPA v2 / KEDA), vertical autoscaling, Karpenter node provisioning, Prometheus/Grafana observability, and GitOps with ArgoCD.",
        "concepts": [
            ("7.8.1", "Horizontal Pod Autoscaler (HPA v2 Custom Metrics) & Vertical Pod Autoscaler (VPA)",
             "Dynamic scaling: HPA v2 querying metrics-server (CPU/Memory utilization) and custom Prometheus metrics via KEDA (event-driven scaling), and VPA profiling and resizing container requests in-place.",
             "https://www.youtube.com/watch?v=X48VuDVv0do&t=10100s", "00:00", "TechWorld with Nana", "https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/"),
            ("7.8.2", "Cluster Autoscaler & Next-Gen Node Provisioning with Karpenter",
             "Infrastructure scaling: legacy Cluster Autoscaler polling pending pods and resizing cloud node groups vs Karpenter directly evaluating unschedulable pod requirements and launching right-sized EC2 instances in seconds.",
             "https://www.youtube.com/watch?v=CqYQ4D9k6-4", "00:00", "DevOps Toolkit", "https://karpenter.sh/"),
            ("7.8.3", "Kubernetes Observability Stack: Prometheus Operator, ServiceMonitors, Grafana & cAdvisor",
             "Production observability: Prometheus Operator CRDs (Prometheus, ServiceMonitor, PodMonitor, PrometheusRule), cAdvisor node metrics, alert routing with Alertmanager, and Grafana cluster dashboards.",
             "https://www.youtube.com/watch?v=X48VuDVv0do&t=10400s", "00:00", "TechWorld with Nana", "https://prometheus-operator.dev/"),
            ("7.8.4", "Helm Package Manager & GitOps Continuous Delivery: Helm Charts & ArgoCD Reconciliation",
             "Enterprise application delivery: Helm chart templating, values.yaml overrides, dependencies, Helm release management; and GitOps continuous delivery with ArgoCD declarative Git-to-cluster reconciliation.",
             "https://www.youtube.com/watch?v=-ykwb1d0DXU", "00:00", "TechWorld with Nana", "https://helm.sh/docs/")
        ]
    }
]

def render_subsections_html(subs_list):
    out = []
    for sub in subs_list:
        num = sub["num"]
        title = sub["title"]
        desc = sub["desc"]
        concepts = sub["concepts"]
        out.append(f'''  <div class="subsection">
    <div class="subsection-head">
      <span class="subsection-tag">{num}</span>
      <h3>{html_lib.escape(title)}</h3>
      <span style="font-size:11px;color:var(--text-faint);">{len(concepts)} concepts</span>
    </div>
    <div class="subsection-desc">{html_lib.escape(desc)}</div>
    <ol class="concepts">''')
        for cid, cname, cdesc, vid, vtime, vchannel, doc in concepts:
            clean_name = re.sub(r'[^a-zA-Z0-9]+', ' ', cname).lower().strip()
            # Extract timestamp if present in vid
            t_match = re.search(r'[?&]t=(\d+)s?', vid)
            start_sec = t_match.group(1) if t_match else "0"
            out.append(f'''      <li data-cid="{cid}" data-name="{clean_name}">
        <div class="done-check" title="Mark as done"></div>
        <div class="bookmark-star" title="Bookmark">☆</div>
        <div>
          <div class="cname">{html_lib.escape(cname)}</div>
          <div style="font-size:11.5px;color:var(--text-faint);margin-top:2px">{html_lib.escape(cdesc)}</div>
        </div>
        <div class="res-links"><a class="video" href="{vid}" data-vtitle="{html_lib.escape(cname)}" data-vchannel="{html_lib.escape(vchannel)}" data-start="{start_sec}" data-vdur="" target="_blank" rel="noopener" title="Watch walkthrough: {html_lib.escape(cname)}">🎬YT</a><a href="{doc}" target="_blank" rel="noopener" title="Official Reference">🌐Doc</a></div>
      </li>''')
        out.append('    </ol>\n  </div>')
    return '\n'.join(out)

def expand_tech_docker_k8s():
    p = os.path.join(ROOT, 'tech_docker_k8s.html')
    with open(p, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update edition
    html = re.sub(
        r'<div class="edition">[^<]+</div>',
        '<div class="edition">Container Orchestration · Masterclass 04 · 14 Subsections · 56 Concepts</div>',
        html
    )

    # 2. Update subtitle
    html = re.sub(
        r'<p class="subtitle">[^<]+</p>',
        '<p class="subtitle">Complete container engineering: Linux cgroups &amp; namespaces, multi-stage Docker builds, image hardening, BuildKit, Compose, Kubernetes control plane, Pod lifecycle, Services, Ingress, StatefulSets, Scheduling, Security, Autoscaling, and GitOps.</p>',
        html
    )

    # 3. Update stats block
    old_stats_match = re.search(r'(<div class="stats">[\s\S]*?</div>\s*(?=<div class="overall-progress">))', html)
    if old_stats_match:
        new_stats = '''<div class="stats">
    <div class="stat"><div class="n">14</div><div class="l">Subsections</div></div>
    <div class="stat"><div class="n">56</div><div class="l">Concepts</div></div>
    <div class="stat"><div class="n">100%</div><div class="l">Curated</div></div>
    <div class="stat"><div class="n">40+</div><div class="l">Verified Docs &amp; Labs</div></div>
  </div>\n\n  '''
        html = html.replace(old_stats_match.group(1), new_stats, 1)

    # 4. Update overall progress pct & search placeholder
    html = re.sub(r'<span class="pct" id="overall-pct">[^<]+</span>', '<span class="pct" id="overall-pct">0 / 56</span>', html)
    html = re.sub(r'placeholder="Search [^"]+"', 'placeholder="Search 56 concepts…"', html)

    # 5. Update Section 6 (Docker) inside tech_docker_k8s
    sec6_match = re.search(r'(<section class="section domain-section"[^>]*id="section-6"[\s\S]*?</section>)', html)
    if sec6_match:
        sec6_text = sec6_match.group(1)
        sec6_new = re.sub(
            r'<span class="focus-bar-stats">[^<]+</span>',
            '<span class="focus-bar-stats">24 concepts &bull; 6 subsections</span>',
            sec6_text
        )
        sec6_new = re.sub(
            r'<div class="meta">[^<]+</div>',
            '<div class="meta">6 subsections · 24 concepts</div>',
            sec6_new
        )
        sec6_new = re.sub(
            r'<div class="pct-text" data-pp-text="6">[^<]+</div>',
            '<div class="pct-text" data-pp-text="6">0 / 24</div>',
            sec6_new
        )
        docker_subs_html = render_subsections_html(DOCKER_SUBSECTIONS)
        sub_start = sec6_new.find('<div class="subsection">')
        sub_end = sec6_new.rfind('</section>')
        if sub_start != -1 and sub_end != -1:
            sec6_new = sec6_new[:sub_start] + docker_subs_html + '\n' + sec6_new[sub_end:]
            html = html.replace(sec6_text, sec6_new, 1)
            print("Updated section-6 in tech_docker_k8s.html")
        else:
            raise ValueError("Could not find subsections in section-6 of tech_docker_k8s.html")
    else:
        raise ValueError("Could not find section-6 in tech_docker_k8s.html")

    # 6. Update Section 7 (Kubernetes) inside tech_docker_k8s
    sec7_match = re.search(r'(<section class="section domain-section"[^>]*id="section-7"[\s\S]*?</section>)', html)
    if sec7_match:
        sec7_text = sec7_match.group(1)
        sec7_new = re.sub(
            r'<span class="focus-bar-stats">[^<]+</span>',
            '<span class="focus-bar-stats">32 concepts &bull; 8 subsections</span>',
            sec7_text
        )
        sec7_new = re.sub(
            r'<div class="meta">[^<]+</div>',
            '<div class="meta">8 subsections · 32 concepts</div>',
            sec7_new
        )
        sec7_new = re.sub(
            r'<div class="pct-text" data-pp-text="7">[^<]+</div>',
            '<div class="pct-text" data-pp-text="7">0 / 32</div>',
            sec7_new
        )
        k8s_subs_html = render_subsections_html(K8S_SUBSECTIONS)
        sub_start = sec7_new.find('<div class="subsection">')
        sub_end = sec7_new.rfind('</section>')
        if sub_start != -1 and sub_end != -1:
            sec7_new = sec7_new[:sub_start] + k8s_subs_html + '\n' + sec7_new[sub_end:]
            html = html.replace(sec7_text, sec7_new, 1)
            print("Updated section-7 in tech_docker_k8s.html")
        else:
            raise ValueError("Could not find subsections in section-7 of tech_docker_k8s.html")
    else:
        raise ValueError("Could not find section-7 in tech_docker_k8s.html")

    atomic_write(p, html)
    print("Saved tech_docker_k8s.html successfully!")

def expand_all_tech():
    p = os.path.join(ROOT, 'all_tech.html')
    with open(p, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update edition & hero stats
    # 53 subsections -> 59 (+3 for Docker, +3 for K8s)
    # 209 concepts -> 234 (+13 for Docker: 11->24, +12 for K8s: 20->32)
    html = re.sub(
        r'<div class="edition">v4 &bull; All-in-One Tech &amp; Engineering Portal &bull; 13 Disciplines &bull; \d+ Subsections &bull; \d+ Concepts</div>',
        '<div class="edition">v4 &bull; All-in-One Tech &amp; Engineering Portal &bull; 13 Disciplines &bull; 59 Subsections &bull; 234 Concepts</div>',
        html
    )

    html = re.sub(
        r'(<div class="stat"><div class="n">)\d+(</div><div class="l">Subsections</div></div>)',
        r'\g<1>59\g<2>',
        html
    )
    html = re.sub(
        r'(<div class="stat"><div class="n">)\d+(</div><div class="l">Concepts</div></div>)',
        r'\g<1>234\g<2>',
        html
    )

    # 2. Update card-docker and card-k8s in domain deck
    card_docker_match = re.search(r'(<div class="domain-card[^"]*"[^>]*id="card-docker"[\s\S]*?</div>\s*</div>)', html)
    if card_docker_match:
        old_card = card_docker_match.group(1)
        new_card = re.sub(
            r'<div class="domain-card-chips">[\s\S]*?</div>',
            '''<div class="domain-card-chips">
<span class="domain-card-chip">6 Subsections</span>
<span class="domain-card-chip">24 Concepts</span>
<span class="domain-card-chip highlight">Kernel, Multi-Stage Builds, Security & Compose</span>
</div>''',
            old_card
        )
        html = html.replace(old_card, new_card, 1)
        print("Updated card-docker in all_tech.html")

    card_k8s_match = re.search(r'(<div class="domain-card[^"]*"[^>]*id="card-k8s"[\s\S]*?</div>\s*</div>)', html)
    if card_k8s_match:
        old_card = card_k8s_match.group(1)
        new_card = re.sub(
            r'<div class="domain-card-chips">[\s\S]*?</div>',
            '''<div class="domain-card-chips">
<span class="domain-card-chip">8 Subsections</span>
<span class="domain-card-chip">32 Concepts</span>
<span class="domain-card-chip highlight">Control Plane, Services, Ingress, Scheduling & GitOps</span>
</div>''',
            old_card
        )
        html = html.replace(old_card, new_card, 1)
        print("Updated card-k8s in all_tech.html")

    # 3. Update Section 6 (Docker) inside all_tech.html
    sec6_match = re.search(r'(<section class="section domain-section"[^>]*id="section-6"[\s\S]*?</section>)', html)
    if sec6_match:
        sec6_text = sec6_match.group(1)
        sec6_new = re.sub(
            r'<span class="focus-bar-stats">[^<]+</span>',
            '<span class="focus-bar-stats">24 concepts &bull; 6 subsections</span>',
            sec6_text
        )
        sec6_new = re.sub(
            r'<div class="meta">[^<]+</div>',
            '<div class="meta">6 subsections · 24 concepts</div>',
            sec6_new
        )
        sec6_new = re.sub(
            r'<div class="pct-text" data-pp-text="6">[^<]+</div>',
            '<div class="pct-text" data-pp-text="6">0 / 24</div>',
            sec6_new
        )
        docker_subs_html = render_subsections_html(DOCKER_SUBSECTIONS)
        sub_start = sec6_new.find('<div class="subsection">')
        sub_end = sec6_new.rfind('</section>')
        if sub_start != -1 and sub_end != -1:
            sec6_new = sec6_new[:sub_start] + docker_subs_html + '\n' + sec6_new[sub_end:]
            html = html.replace(sec6_text, sec6_new, 1)
            print("Updated section-6 in all_tech.html")
        else:
            raise ValueError("Could not find subsections in section-6 of all_tech.html")
    else:
        raise ValueError("Could not find section-6 in all_tech.html")

    # 4. Update Section 7 (Kubernetes) inside all_tech.html
    sec7_match = re.search(r'(<section class="section domain-section"[^>]*id="section-7"[\s\S]*?</section>)', html)
    if sec7_match:
        sec7_text = sec7_match.group(1)
        sec7_new = re.sub(
            r'<span class="focus-bar-stats">[^<]+</span>',
            '<span class="focus-bar-stats">32 concepts &bull; 8 subsections</span>',
            sec7_text
        )
        sec7_new = re.sub(
            r'<div class="meta">[^<]+</div>',
            '<div class="meta">8 subsections · 32 concepts</div>',
            sec7_new
        )
        sec7_new = re.sub(
            r'<div class="pct-text" data-pp-text="7">[^<]+</div>',
            '<div class="pct-text" data-pp-text="7">0 / 32</div>',
            sec7_new
        )
        k8s_subs_html = render_subsections_html(K8S_SUBSECTIONS)
        sub_start = sec7_new.find('<div class="subsection">')
        sub_end = sec7_new.rfind('</section>')
        if sub_start != -1 and sub_end != -1:
            sec7_new = sec7_new[:sub_start] + k8s_subs_html + '\n' + sec7_new[sub_end:]
            html = html.replace(sec7_text, sec7_new, 1)
            print("Updated section-7 in all_tech.html")
        else:
            raise ValueError("Could not find subsections in section-7 of all_tech.html")
    else:
        raise ValueError("Could not find section-7 in all_tech.html")

    atomic_write(p, html)
    print("Saved all_tech.html successfully!")

if __name__ == '__main__':
    expand_tech_docker_k8s()
    expand_all_tech()
    print("Finished expanding Docker & Kubernetes Masterclass!")
