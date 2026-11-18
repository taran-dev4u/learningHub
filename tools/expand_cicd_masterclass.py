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


CICD_SUBSECTIONS = [
    {
        "num": "9.1",
        "title": "CI/CD Foundations, Branching Workflows & Build Pipelines",
        "desc": "Core continuous integration and delivery paradigms, trunk-based branching models, hermetic build caching, and fast-feedback test pyramid architectures.",
        "concepts": [
            ("9.1.1", "Continuous Integration vs Continuous Delivery vs Continuous Deployment",
             "Distinguishing automated merge verification (CI), always-releasable artifact pipelines with manual approval gates (Continuous Delivery), and fully automated production releases (Continuous Deployment), including feedback-loop latency and blast-radius trade-offs.",
             "https://www.youtube.com/watch?v=LNLKZ4Rvk8w", "00:00", "IBM Technology", "https://martinfowler.com/articles/continuousIntegration.html"),
            ("9.1.2", "Trunk-Based Development, Short-Lived Feature Branches & Merge Queues",
             "Eliminating long-lived branch merge hell through daily mainline integration, short-lived pull requests, GitHub/GitLab Merge Queues for serialized CI validation on high-velocity monorepos, and branch protection policies.",
             "https://www.youtube.com/watch?v=C1SXUjG7T9Q", "00:00", "Octopus Deploy", "https://trunkbaseddevelopment.com/"),
            ("9.1.3", "Deterministic Builds, Dependency Caching, Hermetic Environments & Bazel/Nix",
             "Reproducible artifact compilation using lockfiles, layered dependency caches, remote build caches (Bazel Remote Execution, Turborepo, Nix derivations), isolated build sandboxes, and eliminating 'works on my machine' drift.",
             "https://www.youtube.com/watch?v=t3OJn4LseY4", "00:00", "The Automation Stack", "https://bazel.build/basics"),
            ("9.1.4", "Automated Testing Pyramid in CI: Unit, Integration, Contract, E2E & Flaky Test Quarantine",
             "Balancing fast unit suites, Testcontainers-backed integration tests, Pact consumer-driven contract verification, selective End-to-End smoke tests, test sharding/parallelism, and automated flaky test detection and quarantine.",
             "https://www.youtube.com/watch?v=jKQs1s4ygxI", "00:00", "BazAI", "https://martinfowler.com/articles/practical-test-pyramid.html"),
        ],
    },
    {
        "num": "9.2",
        "title": "Progressive Delivery, Zero-Downtime Deployments & Release Engineering",
        "desc": "Production rollout topologies, stateful database schema compatibility, automated canary metric analysis, and decoupled feature flag releases.",
        "concepts": [
            ("9.2.1", "Rolling Updates & Recreate Strategies: Readiness Gates & PodDisruptionBudgets",
             "Incremental instance replacement with maxSurge and maxUnavailable tuning, graceful SIGTERM connection draining (preStop hooks), readiness probe gating, PodDisruptionBudgets (PDB), and when Recreate is required for exclusive locks.",
             "https://www.youtube.com/watch?v=e2HjRrmXMDw", "00:00", "Anton Putra", "https://kubernetes.io/docs/concepts/workloads/pods/disruptions/"),
            ("9.2.2", "Blue/Green Deployments: Traffic Cutover, Instant Rollbacks & Database Schema Compatibility",
             "Parallel idle/active production environments, instant load-balancer or Service selector cutover, zero-downtime Expand-and-Contract database schema migrations so Blue and Green code versions coexist safely, and instant rollback mechanics.",
             "https://www.youtube.com/watch?v=AWVTKBUnoIg", "00:00", "ByteByteGo", "https://martinfowler.com/bliki/BlueGreenDeployment.html"),
            ("9.2.3", "Canary Releases & Traffic Splitting: Argo Rollouts, Flagger & Automated Metric Rollbacks",
             "Weighted Layer 7 traffic shifting (1% -> 5% -> 25% -> 100%) via Ingress/Gateway API or Istio, automated canary analysis (ACA) querying Prometheus error rates and p99 latency, and deterministic auto-rollback on SLO breach.",
             "https://www.youtube.com/watch?v=Z3E9newfGSw", "00:00", "Cloud + AI Architect", "https://argo-rollouts.readthedocs.io/en/stable/"),
            ("9.2.4", "Feature Flags, Dark Launches, Shadow Traffic & Decoupling Deploy from Release",
             "Separating binary deployment from user-facing feature activation, runtime targeting rules, percentage rollouts, dark-launching backend code paths, traffic mirroring/shadowing for load verification, and kill-switch hygiene.",
             "https://www.youtube.com/watch?v=uPCSrWi9IV8", "00:00", "LaunchDarkly", "https://martinfowler.com/articles/feature-toggles.html"),
        ],
    },
    {
        "num": "9.3",
        "title": "GitHub Actions Architecture, Workflows & Enterprise Scale",
        "desc": "Event-driven workflow execution, modular reusable pipelines, SHA-pinned third-party actions, OIDC secretless cloud federation, and autoscaling Kubernetes runners.",
        "concepts": [
            ("9.3.1", "GitHub Actions Core: Events, Triggers, Jobs, Matrix Strategies & Concurrency Controls",
             "Workflow YAML anatomy (on, push, pull_request, workflow_dispatch), job dependency DAGs (needs), cross-platform matrix builds with fail-fast controls, concurrency groups with cancel-in-progress, and least-privilege GITHUB_TOKEN scopes.",
             "https://www.youtube.com/watch?v=R8_veQiYBjI", "00:00", "TechWorld with Nana", "https://docs.github.com/en/actions/writing-workflows/quickstart"),
            ("9.3.2", "Reusable Workflows, Composite Actions & Marketplace Action Version Pinning (SHA Pinning)",
             "Eliminating YAML sprawl across microservices using centralized workflow_call templates, composite step actions, passing secrets/outputs safely, and pinning third-party actions to immutable 40-char commit SHAs against tag-hijacking.",
             "https://www.youtube.com/watch?v=lRypYtmbKMs", "00:00", "CoderDave", "https://docs.github.com/en/actions/sharing-automations/reusing-workflows"),
            ("9.3.3", "Secretless Cloud Auth: OIDC Federation with AWS IAM, Azure & GCP Workload Identity",
             "Replacing static long-lived cloud access keys with ephemeral OpenID Connect (OIDC) JWT tokens (id-token: write), strict subject claim trust policies (repo, branch, environment), and short-lived STS AssumeRoleWithWebIdentity credentials.",
             "https://www.youtube.com/watch?v=Io5UFJlEJKc", "00:00", "GitHub", "https://docs.github.com/en/actions/concepts/security/openid-connect"),
            ("9.3.4", "Runners & Build Optimization: Ephemeral Self-Hosted Runners, ARC & BuildKit Cache",
             "Deploying autoscaling ephemeral self-hosted runners on Kubernetes with Actions Runner Controller (ARC), avoiding persistent runner state contamination, private VPC access, and accelerating Docker builds with BuildKit GitHub Actions cache (type=gha).",
             "https://www.youtube.com/watch?v=lD0t-UgKfEo", "00:00", "Anton Putra", "https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners-with-actions-runner-controller/about-actions-runner-controller"),
        ],
    },
    {
        "num": "9.4",
        "title": "Enterprise CI Engines: Jenkins, GitLab CI & Cloud-Native Pipelines",
        "desc": "Distributed Jenkins controller-agent architectures, GitLab DAG pipelines with review environments, and Kubernetes-native Tekton and Dagger engines.",
        "concepts": [
            ("9.4.1", "Jenkins Architecture: Controller-Agent Topology, Ephemeral Kubernetes Agents & JCasC",
             "Decoupling the Jenkins Controller from workload execution, dynamic ephemeral Pod agents via the Kubernetes plugin, Jenkins Configuration as Code (JCasC) for reproducible controller state, and securing controller credentials.",
             "https://www.youtube.com/watch?v=N52Bg-JcKKg", "00:00", "BECOME A TECH PRO", "https://www.jenkins.io/doc/book/architecting-for-scale/"),
            ("9.4.2", "Declarative vs Scripted Jenkinsfiles: Stages, Parallel Execution, Shared Libraries & Post Blocks",
             "Multibranch pipeline discovery, Declarative pipeline blocks (agent, environment, stages, parallel, when, post), Groovy Shared Libraries for enterprise governance, and credential binding isolation.",
             "https://www.youtube.com/watch?v=7KCS70sCoK0", "00:00", "TechWorld with Nana", "https://www.jenkins.io/doc/book/pipeline/syntax/"),
            ("9.4.3", "GitLab CI/CD Architecture: .gitlab-ci.yml DAG (needs:), Environments, Review Apps & Runners",
             "Stage-based vs Directed Acyclic Graph (needs:) job execution, dynamic ephemeral Review Apps per merge request, GitLab Runner executors (Docker, Kubernetes), parent-child pipelines, and rules/workflow conditional logic.",
             "https://www.youtube.com/watch?v=qP8kir2GUgo", "00:00", "TechWorld with Nana", "https://docs.gitlab.com/ee/ci/"),
            ("9.4.4", "Cloud-Native & Code-Native CI: Tekton Pipelines (Kubernetes CRDs) & Dagger Engines",
             "Running serverless CI natively inside Kubernetes using Tekton Tasks, Pipelines, Workspaces, and Triggers CRDs, alongside portable container-native Dagger pipelines authored in Go/Python/TypeScript that run identically locally and in CI.",
             "https://www.youtube.com/watch?v=7mvrpxz_BfE", "00:00", "DevOps & AI Toolkit", "https://tekton.dev/docs/"),
        ],
    },
    {
        "num": "9.5",
        "title": "Artifact Management, Container Supply Chain Security & DevSecOps",
        "desc": "Immutable artifact registries, shift-left SAST/DAST/SCA scanning, SBOM & SLSA cryptographic provenance, and dynamic secret injection.",
        "concepts": [
            ("9.5.1", "Artifact Repositories & Semantic Versioning: JFrog Artifactory, Sonatype Nexus, GHCR & Immutable Tags",
             "Build-once-promote-everywhere lifecycle, immutable OCI image digests (@sha256) vs mutable tags, SemVer release tagging, proxy/remote dependency caching against upstream outages, and artifact retention policies.",
             "https://www.youtube.com/watch?v=W8eBHd3BlOc", "00:00", "Sonatype", "https://help.sonatype.com/en/sonatype-nexus-repository.html"),
            ("9.5.2", "Shift-Left Security Scanning: SAST (Semgrep/CodeQL), DAST, SCA Dependency Audits & Secret Detection",
             "Automated PR security gates: Static Application Security Testing (CodeQL, Semgrep), Software Composition Analysis (Dependabot, Snyk, Trivy) for CVEs and licenses, Gitleaks secret scanning, and Dynamic Application Security Testing against staging.",
             "https://www.youtube.com/watch?v=C5HH90H0Rg0", "00:00", "AppSec Decoded", "https://owasp.org/www-project-devsecops-guideline/"),
            ("9.5.3", "Software Supply Chain Integrity: SBOM Generation (Syft), SLSA Provenance & Sigstore Cosign Verification",
             "Generating CycloneDX/SPDX Software Bills of Materials (Syft/Trivy), SLSA build provenance attestations, keyless OIDC artifact signing with Sigstore Cosign and Rekor transparency log, and Kubernetes admission verification (Kyverno/Policy Controller).",
             "https://www.youtube.com/watch?v=hF95PiItWtM", "00:00", "NDC Conferences", "https://slsa.dev/spec/v1.0/"),
            ("9.5.4", "Dynamic Secrets & Environment Promotion Gates: HashiCorp Vault, OIDC Secrets & Manual Approvals",
             "Fetching short-lived dynamic database and cloud credentials from HashiCorp Vault via AppRole or JWT/OIDC auth inside CI jobs, protected deployment environments with required human reviewers, and secret masking in pipeline logs.",
             "https://www.youtube.com/watch?v=ZPL3_mrIm6Y", "00:00", "Bryan Krausen", "https://developer.hashicorp.com/vault/docs"),
        ],
    },
    {
        "num": "9.6",
        "title": "GitOps Continuous Delivery, DORA Metrics & Pipeline Observability",
        "desc": "Pull-based declarative reconciliation, ArgoCD and Flux CD production topologies, and measuring engineering velocity and stability via DORA metrics.",
        "concepts": [
            ("9.6.1", "Push vs Pull Deployment Models: GitOps Principles, State Reconciliation & Drift Prevention",
             "Why pull-based GitOps agents inside clusters eliminate exposing kubeconfig admin credentials to external CI systems, continuous desired-vs-live state reconciliation loops, immutable Git audit trails, and self-healing drift correction.",
             "https://www.youtube.com/watch?v=f5EpcWp0THw", "00:00", "TechWorld with Nana", "https://opengitops.dev/"),
            ("9.6.2", "ArgoCD Architecture: Application CRDs, ApplicationSets, Sync Waves, Hooks & Multi-Cluster Delivery",
             "Repo-server manifest generation (Helm/Kustomize), Application controller reconciliation, ordered Sync Waves and PreSync/PostSync schema migration hooks, ApplicationSet generators for multi-cluster fleet delivery, and App-of-Apps patterns.",
             "https://www.youtube.com/watch?v=MeU5_k9ssrs", "00:00", "TechWorld with Nana", "https://argo-cd.readthedocs.io/en/stable/"),
            ("9.6.3", "Flux CD Architecture: GitRepository/Kustomization Controllers, Image Automation & Helm Releases",
             "Composable GitOps Toolkit micro-controllers (source-controller, kustomize-controller, helm-controller), automated container tag polling and Git commit write-back (image-reflector/automation), and SOPS/Age encrypted secrets in Git.",
             "https://www.youtube.com/watch?v=PFLimPh5-wo", "00:00", "Techno Tim", "https://fluxcd.io/flux/"),
            ("9.6.4", "Release Observability & DORA Metrics: Deployment Frequency, Lead Time, CFR, MTTR & OTel CI Traces",
             "Instrumenting the four DORA key metrics (Deployment Frequency, Lead Time for Changes, Change Failure Rate, Mean Time to Recovery), OpenTelemetry pipeline span tracing to pinpoint slow CI stages, and continuous post-deploy SLO verification.",
             "https://www.youtube.com/watch?v=lqsENcje41w", "00:00", "Harness", "https://dora.dev/guides/dora-metrics-four-keys/"),
        ],
    },
]

CICD_RESOURCES_HTML = '''  <div class="resources-section">
    <div class="head" onclick="this.parentElement.classList.toggle('open')">
      <h4>📚 Learn this domain</h4>
      <div><span class="count">6 curated resources</span><span class="chevron">▶</span></div>
    </div>
    <div class="resources-body">
      <div class="res-grid">
        <a class="res-link" href="https://www.youtube.com/watch?v=R8_veQiYBjI" target="_blank" rel="noopener"><span class="res-icon">🎥</span><span class="res-title">GitHub Actions CI/CD Complete Tutorial (Nana)</span><span class="res-source">TechWorld with Nana</span></a>
        <a class="res-link" href="https://www.jenkins.io/doc/book/" target="_blank" rel="noopener"><span class="res-icon">📖</span><span class="res-title">Jenkins User Handbook</span><span class="res-source">Jenkins</span></a>
        <a class="res-link" href="https://argo-cd.readthedocs.io/en/stable/" target="_blank" rel="noopener"><span class="res-icon">🚀</span><span class="res-title">ArgoCD: Declarative GitOps for Kubernetes</span><span class="res-source">CNCF</span></a>
        <a class="res-link" href="https://martinfowler.com/articles/continuousIntegration.html" target="_blank" rel="noopener"><span class="res-icon">📝</span><span class="res-title">Martin Fowler: Continuous Integration &amp; Delivery</span><span class="res-source">Martin Fowler</span></a>
        <a class="res-link" href="https://slsa.dev/spec/v1.0/" target="_blank" rel="noopener"><span class="res-icon">🛡️</span><span class="res-title">SLSA Supply Chain Security Specification v1.0</span><span class="res-source">OpenSSF</span></a>
        <a class="res-link" href="https://dora.dev/guides/dora-metrics-four-keys/" target="_blank" rel="noopener"><span class="res-icon">📊</span><span class="res-title">DORA Four Keys Engineering Metrics Guide</span><span class="res-source">DORA</span></a>
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


def update_section_9(sec9_text):
    sec9_new = re.sub(
        r'<span class="focus-bar-stats">[^<]+</span>',
        '<span class="focus-bar-stats">24 concepts &bull; 6 subsections</span>',
        sec9_text
    )
    sec9_new = re.sub(
        r'<div class="meta">[^<]+</div>',
        '<div class="meta">6 subsections · 24 concepts</div>',
        sec9_new
    )
    sec9_new = re.sub(
        r'<div class="pct-text" data-pp-text="9">[^<]+</div>',
        '<div class="pct-text" data-pp-text="9">0 / 24</div>',
        sec9_new
    )
    sec9_new = re.sub(
        r'<div class="section-desc">[\s\S]*?</div>\s*(?=<div class="resources-section">)',
        '''<div class="section-desc">
    <div class="tagline">Trunk-based workflows, automated quality gates, zero-downtime progressive delivery, supply-chain DevSecOps, and GitOps reconciliation.</div>
    <div class="row"><b>Core Focus:</b> GitHub Actions OIDC &amp; reusable workflows, Blue/Green &amp; Canary rollouts, Jenkins/GitLab/Tekton pipelines, SBOM/SLSA/Cosign, and ArgoCD/Flux GitOps.</div>
    <div class="row"><b>Production Trade-offs:</b> Fast deploy cadence vs comprehensive security &amp; contract gates, ephemeral Kubernetes runners vs pre-warmed build caches, push CI vs pull GitOps.</div>
  </div>
''',
        sec9_new,
        count=1
    )
    sec9_new = re.sub(
        r'<div class="resources-section">[\s\S]*?</div>\s*</div>\s*</div>\s*(?=<div class="subsection">)',
        CICD_RESOURCES_HTML + '\n',
        sec9_new,
        count=1
    )
    subs_html = render_subsections_html(CICD_SUBSECTIONS)
    sub_start = sec9_new.find('<div class="subsection">')
    sub_end = sec9_new.rfind('</section>')
    if sub_start == -1 or sub_end == -1:
        raise ValueError("Could not locate subsection boundaries in section-9")
    return sec9_new[:sub_start] + subs_html + '\n' + sec9_new[sub_end:]


def expand_tech_cicd():
    p = os.path.join(ROOT, 'tech_cicd.html')
    with open(p, 'r', encoding='utf-8') as f:
        html = f.read()

    html = re.sub(
        r'<div class="edition">[^<]+</div>',
        '<div class="edition">DevOps Automation &middot; Masterclass 05 &middot; 6 Subsections &middot; 24 Concepts</div>',
        html
    )
    html = re.sub(
        r'<p class="subtitle">[^<]+</p>',
        '<p class="subtitle">Enterprise continuous integration &amp; delivery: trunk-based workflows, GitHub Actions OIDC, Jenkins/GitLab/Tekton, Blue/Green &amp; Canary rollouts, DevSecOps supply chain, and GitOps.</p>',
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

    sec9_match = re.search(r'(<section class="section domain-section"[^>]*id="section-9"[\s\S]*?</section>)', html)
    if not sec9_match:
        raise ValueError("Could not find section-9 in tech_cicd.html")

    sec9_text = sec9_match.group(1)
    sec9_new = update_section_9(sec9_text)
    html = html.replace(sec9_text, sec9_new, 1)

    atomic_write(p, html)
    print("Saved tech_cicd.html successfully!")


def expand_all_tech():
    p = os.path.join(ROOT, 'all_tech.html')
    with open(p, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update card-cicd in domain deck
    card_match = re.search(r'(<div class="domain-card[^"]*"[^>]*id="card-cicd"[\s\S]*?</div>\s*</div>\s*</div>)', html)
    if not card_match:
        raise ValueError("Could not find card-cicd in all_tech.html")
    old_card = card_match.group(1)
    new_card = re.sub(
        r'<p class="domain-card-desc">[\s\S]*?</p>',
        '<p class="domain-card-desc">Trunk-based CI, GitHub Actions OIDC, Jenkins &amp; GitLab DAGs, Blue/Green &amp; Canary rollouts, SBOM/SLSA DevSecOps, ArgoCD/Flux GitOps &amp; DORA metrics.</p>',
        old_card,
        count=1
    )
    new_card = re.sub(
        r'<div class="domain-card-chips">[\s\S]*?</div>',
        '''<div class="domain-card-chips">
<span class="domain-card-chip">6 Subsections</span>
<span class="domain-card-chip">24 Concepts</span>
<span class="domain-card-chip highlight">GitHub Actions, Canary, DevSecOps, GitOps &amp; DORA</span>
</div>''',
        new_card,
        count=1
    )
    html = html.replace(old_card, new_card, 1)
    print("Updated card-cicd in all_tech.html")

    # 2. Update Section 9 (CI/CD) inside all_tech.html
    sec9_match = re.search(r'(<section class="section domain-section"[^>]*id="section-9"[\s\S]*?</section>)', html)
    if not sec9_match:
        raise ValueError("Could not find section-9 in all_tech.html")
    sec9_text = sec9_match.group(1)
    sec9_new = update_section_9(sec9_text)
    html = html.replace(sec9_text, sec9_new, 1)
    print("Updated section-9 in all_tech.html")

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
    expand_tech_cicd()
    expand_all_tech()
    print("Finished expanding CI/CD Masterclass!")
