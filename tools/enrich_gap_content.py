#!/usr/bin/env python3
"""
Enriches tools/gap-content.mjs for bh, ai, and cloud with staff-level depth,
actionable frameworks, concrete metrics, and architectural trade-offs.
"""
import os, re, tempfile

GAP_PATH = os.path.join(os.path.dirname(__file__), "gap-content.mjs")

def update_gap_content():
    with open(GAP_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Behavioral updates
    bh_replacements = {
        "Acting with incomplete information": "Framework: Quantify confidence threshold (Jeff Bezos 70% rule), bound blast radius via feature flags and canary deployments, and establish explicit metrics for automated rollback.",
        "Defining scope when none is given": "Framework: Deconstruct ambiguity into personas, core user stories, non-functional latency/throughput constraints, and an iterative phased milestone roadmap.",
        "Communicating assumptions": "Framework: State assumptions and risk vectors explicitly in an RFC/Architecture Decision Record (ADR); schedule weekly alignment checkpoints to validate against real data.",
        "Going beyond your role": "Story: Stepped outside team boundaries to investigate cross-team latency spikes, diagnosing upstream partition skew and authoring an automated pipeline fix.",
        "Long-term thinking vs quick wins": "Story: Pushed back against fragile hardcoded routing patches; delivered an extensible metadata-driven dynamic routing layer that scaled to 200+ enterprise tenants.",
        "Owning outcomes after handoff": "Story: Monitored telemetry, error rates, and on-call runbooks for 60 days post-launch; mentored client operations team to ensure sustained SLA adherence.",
        "Disagreeing with a manager": "Story: Disagree and commit. Voiced technical risks of NoSQL migration with empirical ACID transaction benchmark data in private 1:1; once decided, committed 100% to flawless execution.",
        "Influencing without authority": "Story: Built a working end-to-end prototype and automated performance benchmark suite to align two deadlocked engineering teams around gRPC adoption.",
        "Driving alignment across teams": "Story: Brokered an enterprise search unification agreement between 4 independent product divisions by presenting a unified multi-tenant architecture with 60% cost reduction.",
        "Telling a real failure story": "Story: Errant migration script triggered an 11-minute production auth outage. Took 100% personal ownership, published transparent status updates, and added CI lock analysis.",
        "Post-mortems and prevention": "Story: Facilitated a blameless post-mortem analyzing the five whys of an outage; implemented permanent automated guards, canary gates, and runbook playbooks.",
        "Receiving hard feedback": "Story: Received feedback on overly abrasive code review comments. Transitioned to inquisitive coaching ('What failure modes occur if X fails?'), improving team trust.",
        "Onboarding and coaching juniors": "Story: Mentored an SDE-1 through weekly system design pairing, guided their delivery of a critical payment webhook gateway, and supported their promotion to SDE-2.",
        "Delegation and trust": "Story: Delegated architectural ownership of a mission-critical billing refactor to a mid-level engineer, providing strategic scaffolding while trusting their execution.",
        "Raising the bar in reviews": "Story: Instituted structured RFC review templates and automated linting/coverage gates in CI, uplifting engineering velocity and reducing regression bugs by 64%.",
        "Saying no with data": "Story: Declined an executive request to add un-cached real-time dashboard analytics by showing load test data proving it would degrade core checkout latency.",
        "Tech debt vs features": "Story: Negotiated a dedicated 20% sprint budget for tech debt remediation by quantifying that flaky tests and brittle legacy code cost 35 engineering hours per week.",
        "Deadline triage": "Story: 6 weeks before contractual deadline, descoped non-essential P2 features and parallelized workstreams to ship core payment capabilities with 100% financial accuracy.",
        "Working backwards from the customer": "Story: Started with user friction logs showing 22% authentication drop-offs; replaced legacy OAuth flow with RFC 8628 device flow, slashing drop-offs to 1.5%.",
        "Quantifying customer outcomes": "Story: Solved high-latency mobile API waterfalls in Latin America, dropping p99 latency from 4.8s to 340ms and driving a 22% increase in user retention.",
        "Handling customer escalations": "Story: Personally debugged intermittent webhook dropouts for an enterprise customer, diagnosing TCP window exhaustion and authoring an adaptive backoff client SDK.",
        "Choosing boring technology": "Story: Chose proven PostgreSQL over trendy NoSQL for a high-throughput ledger; avoided distributed transaction complexity and met all SLA targets easily.",
        "Architecture decision records": "Story: Established repository-tracked ADRs detailing context, evaluated alternatives, and trade-offs, enabling architectural decisions to endure team rotations.",
        "Estimating and de-risking projects": "Story: Identified third-party integration latency as the biggest project risk; built a proof-of-concept spike in sprint 1 to de-risk timeline estimates."
    }

    # AI updates
    ai_replacements = {
        "JSON mode and schema-constrained decoding": "CFG / Regex logit masking at each token step guarantees 100% valid JSON schema compliance at generation time with zero parsing errors.",
        "Function calling APIs": "Model emits tool name and JSON args matching OpenAPI schemas; client runtime executes and returns results as tool-role messages for final synthesis.",
        "Tool selection and routing": "Keep tool definitions minimal and discriminative; tool descriptions are prompts guiding the model on boundaries, inputs, and operational side effects.",
        "Parallel tool calls": "Independent tool calls batched in a single turn reduce multi-turn roundtrip latency by up to 75% for read-heavy agent workflows.",
        "Validating and repairing output": "Pydantic validation with automated repair loops feeding execution tracebacks and validation errors back to the model for iterative correction.",
        "Retrieval metrics (recall@k, MRR)": "Recall@K measures chunk presence in top-K; Mean Reciprocal Rank (MRR) evaluates ranking position of first relevant chunk across evaluation queries.",
        "Faithfulness and groundedness": "Evaluates whether claims in generated answer are mathematically supported by retrieved context via LLM-as-a-judge (Ragas framework).",
        "Golden datasets and synthetic evals": "Curate 50-200 ground-truth Q-A-Context triples; bootstrap adversarial edge cases with synthetic question generation across diverse document domains.",
        "End-to-end RAG eval pipelines": "Decouple retrieval evaluation (Hit Rate, MRR, Context Relevance) from generation evaluation (Faithfulness, Groundedness) to isolate pipeline failures.",
        "Agent failure modes": "Infinite tool calling loops, hallucinated arguments, context window overflow, and goal drift. Mitigate with hard step caps, timeouts, and state checkpoints.",
        "Guardrails on actions and budgets": "Step limits (max 10 iterations), per-session token/spend budgets, strict tool allowlists, and dry-run execution modes for mutations.",
        "Human-in-the-loop checkpoints": "Mandatory human review and approval gates before executing high-blast-radius actions (database writes, refunds, customer communications).",
        "Tracing agent decisions": "OpenTelemetry-compatible step-by-step tracing (Langfuse, LangSmith) capturing thoughts, tool calls, return values, latency, and token cost.",
        "Prompt registries and versioning": "Version control prompts with semantic versioning and metadata outside the application hot path; track prompt lineage across releases.",
        "A/B testing prompts": "Route live traffic between prompt variants; measure statistical significance on downstream completion rates, user retention, and token cost.",
        "Regression testing on prompt change": "Automated CI/CD gates running regression eval suites on golden datasets before merging any prompt modification.",
        "Templates and variable hygiene": "Strict XML/JSON input escaping; never concatenate raw untrusted user input directly into system prompts or developer instructions.",
        "Token, cost and latency dashboards": "Granular real-time telemetry attributing input/output token usage, prompt cache hits, and dollar cost down to individual features and tenants.",
        "Logging completions safely": "Automated PII scrubbing (Presidio) before logging; sample full execution traces to data lakes with strict retention policies.",
        "Quality drift detection": "Continuous sampling of production interactions; run automated LLM judges to detect sudden drops in groundedness or user satisfaction.",
        "User feedback loops": "Explicit (thumbs up/down, corrections) and implicit (copy-paste, dwell time) user telemetry feeding future evaluation and fine-tuning datasets.",
        "Input and output content filtering": "Multi-layered guardrail classifiers (Llama Guard, NeMo Guardrails) evaluating safety and toxicity before model call and before returning response.",
        "Prompt injection defenses": "Enforce privilege separation: delimit untrusted external text in isolated XML tags; instruct model to treat retrieved data purely as passive text.",
        "Jailbreak detection": "Detect adversarial prefix injection, role-play exploits, and Base64-encoded payloads; log and apply aggressive rate limits to offending tenants.",
        "PII redaction": "Mask credit card numbers, SSNs, and personal credentials on client side prior to egressing data outside the organizational perimeter.",
        "Model routing and cascades": "Route incoming requests to smaller cheap models (GPT-4o-mini, Haiku); escalate to frontier models only on low confidence or high complexity.",
        "Caching (exact and semantic)": "Exact hash caching for identical prompt strings; vector embedding semantic caching (>=0.95 cosine similarity) for common queries.",
        "Batching and streaming": "Server-Sent Events (SSE) for low TTFT online queries; asynchronous batch API processing for offline jobs at 50% discount.",
        "Quantization and distillation": "AWQ / GPTQ 4-bit weight quantization and knowledge distillation from frontier models into specialized 8B/70B models for on-prem serving.",
        "Context window budgeting": "Dynamic context truncation, hierarchical summarization, and vector retrieval filtering to prevent prompt bloat and 'Lost in the Middle' degradation."
    }

    # Cloud updates
    cloud_replacements = {
        "Operational excellence": "Manage infrastructure as code, make frequent small reversible changes, anticipate failures, and conduct blameless post-mortems.",
        "Security pillar": "Identity-centric defense in depth, zero-trust network boundaries, ubiquitous encryption at rest and in transit, and automated incident response.",
        "Reliability pillar": "Multi-AZ and multi-region deployment topologies, automated failure recovery, horizontal elasticity, distributed rate limiting, and regular DR drills.",
        "Performance efficiency": "Right-size compute instance families, leverage serverless event-driven architectures, deploy edge caching globally, and benchmark continuously.",
        "Cost optimization": "Implement FinOps governance, eliminate idle resources, leverage Reserved Instances and Savings Plans, and optimize storage lifecycle tiering.",
        "Sustainability": "Maximize hardware utilization, adopt energy-efficient ARM-based AWS Graviton processors, and scale down non-production workloads during off-peak hours.",
        "AWS Organizations and Control Tower": "Automated account factory, centralized IAM Identity Center SSO, consolidated billing, and continuous compliance monitoring.",
        "Azure management groups and subscriptions": "Hierarchical management structure providing unified policy inheritance, role assignments, and cost boundaries across hundreds of subscriptions.",
        "Account/subscription isolation strategy": "Isolate environments into dedicated accounts (Prod, Staging, Dev, Shared Services, Security Tooling) to strictly bound blast radiuses.",
        "Guardrails: SCPs and Azure Policy": "Enforce mandatory preventive guardrails (e.g. restrict regions, mandate encryption, deny public S3 buckets) that account administrators cannot disable.",
        "Tagging and cost allocation": "Enforce mandatory resource tagging (CostCenter, Environment, Owner) to enable granular cost allocation showback and chargeback accounting.",
        "Budgets and anomaly alerts": "AWS Budgets and Azure Cost Management with automated ML anomaly detection alerting teams before cloud overruns occur.",
        "Savings plans and reserved capacity": "Analyze 90-day compute baseline usage; commit to 1-3 year Compute Savings Plans for up to 72% discount while keeping burst on-demand.",
        "FinOps practice": "Cross-functional Inform -> Optimize -> Operate framework aligning engineering, finance, and product teams on unit economics (cost per transaction).",
        "RTO and RPO targets": "Recovery Time Objective (maximum tolerable downtime) and Recovery Point Objective (maximum tolerable data loss) determine architecture and budget.",
        "Backup vs snapshot vs replication": "Point-in-time snapshots (S3-backed EBS snapshots) vs continuous block-level or database streaming replication (Aurora Global Database).",
        "DR strategies": "Backup & Restore (high RTO/RPO, lowest cost) -> Pilot Light (minimal core running) -> Warm Standby (scaled-down replica) -> Multi-Site Active-Active (zero RTO/RPO).",
        "Cross-region failover testing": "Scheduled Game Day disaster simulation drills injecting regional partition failures (Chaos Engineering) to validate DNS failover and database promotion.",
        "Secrets Manager vs Key Vault": "Centralized, encrypted secret storage providing automated password rotation via Lambda/Functions, fine-grained IAM access, and audit logging.",
        "KMS envelope encryption": "Two-tier key hierarchy: customer master keys (KMS CMK) protect data encryption keys (DEK); data is encrypted locally using the DEK.",
        "Secret rotation": "Automated continuous rotation of database credentials and API tokens every 30-90 days with zero application downtime using dual-credential buffering.",
        "IAM roles vs static credentials": "Workload Identity (AWS IAM Roles for Service Accounts - IRSA, Azure Workload Identity) eliminating static API keys and service principal secrets.",
        "ECS vs EKS vs AKS": "AWS ECS provides simplified native container management; AWS EKS and Azure AKS provide managed CNCF-compliant Kubernetes for complex cloud-native architectures.",
        "Fargate and serverless containers": "Run containers without managing virtual machine node instances; AWS and Azure handle OS patching, security hardening, and compute capacity.",
        "Cluster autoscaling": "Horizontal Pod Autoscaler (HPA) scales replica counts on metrics; Karpenter or Cluster Autoscaler provisions optimal EC2 instance types dynamically in seconds.",
        "Service discovery and ingress": "Kubernetes Service abstractions, AWS Cloud Map, and Ingress Controllers (AWS ALB Ingress Controller) managing external L7 traffic routing.",
        "Image registries and scanning": "Amazon ECR and Azure ACR with automated vulnerability scanning (CVE checks on push), immutable image tags, and cross-region replication.",
        "Identity-based access vs network perimeter": "Authenticate and authorize every transaction explicitly; never trust requests based solely on origin IP or internal network location.",
        "PrivateLink and private endpoints": "Secure private connectivity between VPCs/VNets and cloud services over internal backbones without traversing the public internet or requiring NAT gateways.",
        "mTLS service-to-service": "Mutual Transport Layer Security (mTLS) with cryptographically verified identity certificates between all internal microservice calls using a service mesh (Istio, Linkerd).",
        "Microsegmentation": "Granular host-level and subnet-level security groups enforcing least-privilege traffic flow between individual workload tiers (east-west traffic control).",
        "The 6 Rs of migration": "Rehost (lift-and-shift), Replatform (lift-tinker-and-shift to managed DB), Repurchase (drop-and-shop to SaaS), Refactor (cloud-native rewrite), Retire, Retain.",
        "Strangler fig pattern": "Incrementally replace legacy monolith components by routing specific API endpoints to newly deployed cloud microservices via an API Gateway.",
        "Database migration (DMS)": "AWS Database Migration Service with Change Data Capture (CDC) replicating ongoing transactions to minimize cutover downtime to seconds.",
        "Hybrid connectivity": "Dual-redundant AWS Direct Connect / Azure ExpressRoute circuits paired with backup IPSec VPN tunnels for high-availability corporate datacenter interconnect."
    }

    all_replacements = {**bh_replacements, **ai_replacements, **cloud_replacements}
    total_replaced = 0

    for title, desc in all_replacements.items():
        # Match `["Title", "OldDesc"]`
        escaped_title = re.escape(title)
        pattern = re.compile(rf'(\[\s*"{escaped_title}"\s*,\s*)"[^"]*"\s*(\])')
        # We need to escape any backslashes or quotes in desc
        escaped_desc = desc.replace('\\', '\\\\').replace('"', '\\"')
        content, n = pattern.subn(rf'\1"{escaped_desc}"\2', content)
        total_replaced += n

    dir_name = os.path.dirname(GAP_PATH)
    fd, temp_path = tempfile.mkstemp(dir=dir_name, text=True)
    with os.fdopen(fd, "w", encoding="utf-8") as tmp:
        tmp.write(content)
    os.replace(temp_path, GAP_PATH)
    print(f"Updated {total_replaced} gap content items in tools/gap-content.mjs!")

if __name__ == "__main__":
    update_gap_content()
