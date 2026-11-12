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

TERRAFORM_SUBSECTIONS = [
    {
        "num": "8.1",
        "title": "Terraform Core Architecture, HCL2 Syntax & Execution Lifecycle",
        "desc": "Declarative infrastructure paradigms, HCL2 syntax constructs, input variable validation, execution graph generation, and provider plugin architectures.",
        "concepts": [
            ("8.1.1", "IaC Declarative Paradigm: Desired State vs Imperative Scripting",
             "Declarative state models vs imperative scripts, idempotency, convergence, immutable infrastructure principles, avoiding manual configuration drift, and infrastructure reproducibility across environments.",
             "https://www.youtube.com/watch?v=7xngnjfIlK4&t=56s", "00:56", "DevOps Directive", "https://developer.hashicorp.com/terraform/intro"),
            ("8.1.2", "HCL2 Syntax Foundations: Blocks, Arguments, Types & Variable Validation",
             "HashiCorp Configuration Language (HCL2) block types (terraform, provider, resource, variable, output, locals), strict type constraints (string, number, bool, list, map, object, tuple), custom validation blocks with regex and condition rules, and sensitive output masking.",
             "https://www.youtube.com/watch?v=7xngnjfIlK4&t=251s", "04:11", "DevOps Directive", "https://developer.hashicorp.com/terraform/language/syntax/configuration"),
            ("8.1.3", "The Core Terraform Lifecycle: init, validate, plan, apply & destroy",
             "Provider plugin resolution, .terraform.lock.hcl dependency lockfiles, static configuration validation, execution plan computation (terraform plan -out=tfplan), spec-driven atomic applies, targeted destroys, and CI/CD exit codes (-detailed-exitcode).",
             "https://www.youtube.com/watch?v=7xngnjfIlK4&t=876s", "14:36", "DevOps Directive", "https://developer.hashicorp.com/terraform/cli/commands"),
            ("8.1.4", "Resource Dependency Graph Engine: Implicit vs Explicit (depends_on) Execution Graphs",
             "Directed Acyclic Graph (DAG) construction, topological sorting, implicit references via attribute interpolation, explicit ordering via depends_on, parallel resource walking, cycle detection algorithms, and graph export (terraform graph | dot -Tsvg).",
             "https://www.youtube.com/watch?v=7xngnjfIlK4&t=1213s", "20:13", "DevOps Directive", "https://developer.hashicorp.com/terraform/language/resources/behavior#dependencies")
        ]
    },
    {
        "num": "8.2",
        "title": "State Management, Remote Backends & Distributed Concurrency",
        "desc": "State file schema internals, centralized remote backends, distributed lock acquisition, sensitive value protections, and environment state isolation.",
        "concepts": [
            ("8.2.1", "Terraform State Internals: terraform.tfstate Schema, Lineage & Serial",
             "Mapping declarative HCL blocks to real cloud provider resource IDs, state metadata schema v4, cryptographic checksums, serial version increments, lineage UUID tracking, and out-of-band drift discovery during refresh phases.",
             "https://www.youtube.com/watch?v=7xngnjfIlK4&t=1712s", "28:32", "DevOps Directive", "https://developer.hashicorp.com/terraform/language/state"),
            ("8.2.2", "Remote Backends & Distributed State Locking: S3 + DynamoDB, Azure Blob & GCS",
             "Centralized remote state architectures, server-side encryption (KMS / customer-managed keys), distributed mutual exclusion locking with DynamoDB LockID / Azure blob leases, preventing catastrophic concurrent apply collisions in multi-engineer teams.",
             "https://www.youtube.com/watch?v=7xngnjfIlK4&t=2711s", "45:11", "DevOps Directive", "https://developer.hashicorp.com/terraform/language/settings/backends/configuration"),
            ("8.2.3", "Sensitive Data in State & Backend Security Hardening",
             "Risks of plaintext secrets (database passwords, private keys, API tokens) stored inside state files, ephemeral values, KMS envelope encryption at rest, IAM least-privilege backend bucket policies, and decoupling secrets via HashiCorp Vault.",
             "https://www.youtube.com/watch?v=7xngnjfIlK4&t=4280s", "01:11:20", "DevOps Directive", "https://developer.hashicorp.com/terraform/language/state/sensitive-data"),
            ("8.2.4", "Environment Isolation: Workspaces vs Directory-Isolated Root Modules",
             "State isolation trade-offs: terraform workspace single-backend branch switching vs directory-isolated environment roots (environments/dev, environments/prod), blast radius containment, and preventing accidental cross-environment destruction.",
             "https://www.youtube.com/watch?v=SLB_c_ayRMo&t=2820s", "47:00", "freeCodeCamp.org", "https://developer.hashicorp.com/terraform/language/state/workspaces")
        ]
    },
    {
        "num": "8.3",
        "title": "Dynamic Configuration, Meta-Arguments & Reusable Module Engineering",
        "desc": "Standard module composition, count vs for_each iteration semantics, dynamic nested blocks, HCL collection comprehensions, and data source lookups.",
        "concepts": [
            ("8.3.1", "Reusable Module Architecture: Root vs Child Modules & Clean Interface Contracts",
             "Standard module structure (main.tf, variables.tf, outputs.tf, versions.tf), input variable defaults and descriptions, output encapsulation, public registry vs private Git/HTTP module sourcing, and semantic version pinning (~> 2.0).",
             "https://www.youtube.com/watch?v=7xngnjfIlK4&t=4802s", "01:20:02", "DevOps Directive", "https://developer.hashicorp.com/terraform/language/modules"),
            ("8.3.2", "Meta-Arguments: count vs for_each & Dynamic Nested Blocks",
             "Conditional resource instantiation (count = var.enabled ? 1 : 0), map/set iteration with for_each avoiding index shifting bugs, dynamic nested configuration blocks (dynamic tag { for_each = ... content { ... } }), and iterator variables.",
             "https://www.youtube.com/watch?v=7xngnjfIlK4&t=5340s", "01:29:00", "DevOps Directive", "https://developer.hashicorp.com/terraform/language/meta-arguments/for_each"),
            ("8.3.3", "HCL Advanced Functions, Expressions & Collection Comprehensions",
             "Built-in collection transformations: merge(), flatten(), lookup(), slice(), zipmap(); conditional ternary operators, for list and map comprehensions with filtering ([for k, v in var.map : v if v.active]), and splat expressions (aws_subnet.public[*].id).",
             "https://www.youtube.com/watch?v=SLB_c_ayRMo&t=4500s", "01:15:00", "freeCodeCamp.org", "https://developer.hashicorp.com/terraform/language/functions"),
            ("8.3.4", "Data Sources & Cross-Stack State Sharing: terraform_remote_state",
             "Reading existing cloud infrastructure metadata without managing its lifecycle (data aws_ami, data aws_vpc), cross-layer state sharing via terraform_remote_state data sources, and loosely coupled alternatives (SSM Parameter Store, AWS Cloud Map).",
             "https://www.youtube.com/watch?v=7xngnjfIlK4&t=5766s", "01:36:06", "DevOps Directive", "https://developer.hashicorp.com/terraform/language/data-sources")
        ]
    },
    {
        "num": "8.4",
        "title": "Resource Lifecycle Hooks, Refactoring & Advanced State Operations",
        "desc": "Lifecycle meta-arguments, surgical state modifications, brownfield import automation, and zero-downtime declarative refactoring using moved blocks.",
        "concepts": [
            ("8.4.1", "Resource Lifecycle Meta-Arguments: create_before_destroy, prevent_destroy & ignore_changes",
             "Zero-downtime resource replacement semantics (create_before_destroy = true), safety guards preventing accidental destruction of mission-critical databases (prevent_destroy = true), and ignoring auto-scaled or externally mutated attributes (ignore_changes = [tags, desired_count]).",
             "https://www.youtube.com/watch?v=7xngnjfIlK4&t=6210s", "01:43:30", "DevOps Directive", "https://developer.hashicorp.com/terraform/language/meta-arguments/lifecycle"),
            ("8.4.2", "State Inspection & Surgical CLI Manipulation: state list, show, mv, rm & replace",
             "Targeted debugging with terraform state list and terraform state show, safe resource address renaming with terraform state mv, unbinding resources with terraform state rm, and forcing targeted rebuilds via terraform apply -replace=....",
             "https://www.youtube.com/watch?v=7xngnjfIlK4&t=3503s", "58:23", "DevOps Directive", "https://developer.hashicorp.com/terraform/cli/commands/state"),
            ("8.4.3", "Declarative Resource Import & Code Generation: import Blocks (Terraform 1.5+)",
             "Adopting brownfield infrastructure: interactive terraform import CLI command vs modern declarative import { to = ... id = ... } blocks, automatic HCL code generation with terraform plan -generate-config-out=generated.tf, and bringing unmanaged cloud assets under IaC control.",
             "https://www.youtube.com/watch?v=SLB_c_ayRMo&t=6200s", "01:43:20", "freeCodeCamp.org", "https://developer.hashicorp.com/terraform/language/import"),
            ("8.4.4", "Declarative Architecture Refactoring: moved Blocks (Terraform 1.1+)",
             "Refactoring legacy monolithic codebases into modular architectures without resource destruction: declarative moved { from = ... to = ... } blocks, recording rename history in version control, and eliminating hazardous manual state mv commands across distributed teams.",
             "https://www.youtube.com/watch?v=Yc53L_V39-Q", "00:00", "Christian Lempa", "https://developer.hashicorp.com/terraform/language/modules/develop/refactoring")
        ]
    },
    {
        "num": "8.5",
        "title": "Multi-Environment Orchestration, Terragrunt & CI/CD GitOps",
        "desc": "Terragrunt DRY orchestration, automated PR plan reviews with GitHub Actions, Terraform Cloud / Enterprise workflows, and multi-region / multi-account provider patterns.",
        "concepts": [
            ("8.5.1", "DRY Architecture with Terragrunt: Remote State Inheritance & Dependency Blocks",
             "Terragrunt orchestration layer for keeping Terraform configurations DRY, automated S3/DynamoDB remote state backend generation, hierarchical variable inheritance (find_in_parent_folders()), and DAG-directed multi-module execution (terragrunt run-all apply).",
             "https://www.youtube.com/watch?v=u3O28tB0D70", "00:00", "TechWorld with Nana", "https://terragrunt.gruntwork.io/docs/"),
            ("8.5.2", "Automated CI/CD Pipelines: GitHub Actions, GitLab CI & Speculative PR Plans",
             "Enterprise IaC CI/CD delivery: automated linting, security scanning, generating speculative plan diffs posted as PR comments, branch protection rules, OIDC token authentication for AWS/Azure/GCP (eliminating long-lived cloud keys), and automated gated apply on main branch merge.",
             "https://www.youtube.com/watch?v=GpzPzM5xLp0", "00:00", "Abhishek Veeramalla", "https://developer.hashicorp.com/terraform/tutorials/automation/github-actions"),
            ("8.5.3", "Terraform Cloud (HCP Terraform) & Terraform Enterprise Architecture",
             "Hosted remote execution environments, team access controls (RBAC), private module registries, automated plan execution on Git push, Cost Estimation engines, Sentinel policy enforcement, audit logs, and self-hosted private agent pools.",
             "https://www.youtube.com/watch?v=Vl0v_6N4Kk8", "00:00", "TechWorld with Nana", "https://developer.hashicorp.com/terraform/cloud-docs"),
            ("8.5.4", "Multi-Provider & Multi-Region Orchestration: Provider Aliases & AssumeRole Delegation",
             "Managing multi-region cloud architectures with provider aliases (provider aws { alias = us_west }), cross-account infrastructure provisioning using AWS STS assume_role blocks, and multi-cloud orchestration combining AWS, Cloudflare, Datadog, and Kubernetes providers in a single deployment graph.",
             "https://www.youtube.com/watch?v=SLB_c_ayRMo&t=7800s", "02:10:00", "freeCodeCamp.org", "https://developer.hashicorp.com/terraform/language/providers/configuration#alias-multiple-provider-configurations")
        ]
    },
    {
        "num": "8.6",
        "title": "IaC Security, Policy as Code, Testing & Drift Automation",
        "desc": "Shift-left security scanning, Sentinel and OPA policy guardrails, native HCL test frameworks, and automated continuous drift detection.",
        "concepts": [
            ("8.6.1", "Static Code Analysis, Linting & Security Scanning: TFLint, tfsec & Checkov",
             "Shift-left IaC security: pre-commit static analysis, catching syntax errors and deprecated cloud arguments with TFLint, scanning Abstract Syntax Trees (AST) for insecure defaults (unencrypted S3 buckets, open 0.0.0.0/0 security groups) using Checkov and tfsec/Trivy.",
             "https://www.youtube.com/watch?v=f_VpP3Wj85w", "00:00", "Christian Lempa", "https://www.checkov.io/"),
            ("8.6.2", "Policy as Code & Guardrails: HashiCorp Sentinel & Open Policy Agent (OPA / Rego)",
             "Enforcing enterprise compliance before provisioning: Sentinel advisory/soft-mandatory/hard-mandatory policies, OPA Rego evaluation over terraform show -json plan outputs, enforcing mandatory tagging, CIDR restrictions, approved instance types, and cost guardrails.",
             "https://www.youtube.com/watch?v=q6gI6A6Y2l4", "00:00", "TechWorld with Nana", "https://developer.hashicorp.com/sentinel/docs"),
            ("8.6.3", "Native Integration Testing: The terraform test Framework (Terraform 1.6+)",
             "First-class HCL-native unit and integration testing: .tftest.hcl test files, run blocks for execution phases, mock providers for zero-cost testing, assertions on output values and resource attributes, and validating module edge cases without deploying actual cloud infrastructure.",
             "https://www.youtube.com/watch?v=uX37F2xS_aM", "00:00", "Christian Lempa", "https://developer.hashicorp.com/terraform/language/tests"),
            ("8.6.4", "Continuous Drift Detection & Automated Self-Healing Workflows",
             "Mitigating out-of-band manual changes made via cloud web consoles: scheduled cron-triggered terraform plan -detailed-exitcode jobs, drift alerting to Slack and PagerDuty, automated remediation via GitOps controllers (Weave TF-Controller, Flux, ArgoCD), and human-in-the-loop review strategies.",
             "https://www.youtube.com/watch?v=jWd7vK4_f44", "00:00", "TechWorld with Nana", "https://developer.hashicorp.com/terraform/tutorials/state/drift-detection")
        ]
    }
]

def render_subsections_html(subsections):
    out = []
    for sub in subsections:
        num = sub["num"]
        title = sub["title"]
        desc = sub["desc"]
        concepts = sub["concepts"]
        
        out.append(f'  <div class="subsection">')
        out.append(f'    <div class="subsection-head">')
        out.append(f'      <span class="subsection-tag">{num}</span>')
        out.append(f'      <h3>{html_lib.escape(title)}</h3>')
        out.append(f'      <span style="font-size:11px;color:var(--text-faint);">{len(concepts)} concepts</span>')
        out.append(f'    </div>')
        out.append(f'    <div class="subsection-desc">{html_lib.escape(desc)}</div>')
        out.append(f'    <ol class="concepts">')
        
        for cid, cname, cdesc, yurl, ytime, ychan, docurl in concepts:
            norm_name = re.sub(r'[^a-z0-9]+', ' ', cname.lower()).strip()
            
            # extract start seconds
            start_s = "0"
            m = re.search(r'[?&]t=(\d+)s?', yurl)
            if m:
                start_s = m.group(1)
            
            out.append(f'      <li data-cid="{cid}" data-name="{html_lib.escape(norm_name)}">')
            out.append(f'        <div class="done-check" title="Mark as done"></div>')
            out.append(f'        <div class="bookmark-star" title="Bookmark">☆</div>')
            out.append(f'        <div>')
            out.append(f'          <div class="cname">{html_lib.escape(cname)}</div>')
            out.append(f'          <div style="font-size:11.5px;color:var(--text-faint);margin-top:2px">{html_lib.escape(cdesc)}</div>')
            out.append(f'        </div>')
            out.append(f'        <div class="res-links"><a class="video" href="{html_lib.escape(yurl)}" data-vtitle="{html_lib.escape(cname)}" data-vchannel="{html_lib.escape(ychan)}" data-start="{start_s}" data-vdur="" target="_blank" rel="noopener" title="Watch walkthrough: {html_lib.escape(cname)}">🎬YT</a><a href="{html_lib.escape(docurl)}" target="_blank" rel="noopener" title="Official Documentation">🌐Doc</a></div>')
            out.append(f'      </li>')
            
        out.append(f'    </ol>')
        out.append(f'  </div>')
    return '\n'.join(out)

def expand_tech_terraform():
    p = os.path.join(ROOT, 'tech_terraform.html')
    with open(p, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update hero edition & subtitle
    html = re.sub(
        r'<div class="edition">[^<]+</div>',
        '<div class="edition">Infrastructure as Code &middot; Masterclass 06 &middot; 6 Subsections &middot; 24 Concepts</div>',
        html
    )

    # 2. Update stats cards
    html = re.sub(
        r'<div class="stats">[\s\S]*?</div>\s*</div>\s*</div>',
        '''<div class="stats">
    <div class="stat"><div class="n">6</div><div class="l">Subsections</div></div>
    <div class="stat"><div class="n">24</div><div class="l">Concepts</div></div>
    <div class="stat"><div class="n">100%</div><div class="l">Curated</div></div>
    <div class="stat"><div class="n">25+</div><div class="l">Verified Docs &amp; Labs</div></div>
  </div>''',
        html
    )

    # 3. Update overall progress pct & search placeholder
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

    # 4. Update section 8 inside tech_terraform.html
    sec8_match = re.search(r'(<section class="section domain-section"[^>]*id="section-8"[\s\S]*?</section>)', html)
    if not sec8_match:
        raise ValueError("Could not find section-8 in tech_terraform.html")

    sec8_text = sec8_match.group(1)
    sec8_new = re.sub(
        r'<span class="focus-bar-stats">[^<]+</span>',
        '<span class="focus-bar-stats">24 concepts &bull; 6 subsections</span>',
        sec8_text
    )
    sec8_new = re.sub(
        r'<div class="meta">[^<]+</div>',
        '<div class="meta">6 subsections · 24 concepts</div>',
        sec8_new
    )
    sec8_new = re.sub(
        r'<div class="pct-text" data-pp-text="8">[^<]+</div>',
        '<div class="pct-text" data-pp-text="8">0 / 24</div>',
        sec8_new
    )

    subs_html = render_subsections_html(TERRAFORM_SUBSECTIONS)
    sub_start = sec8_new.find('<div class="subsection">')
    sub_end = sec8_new.rfind('</section>')
    if sub_start != -1 and sub_end != -1:
        sec8_new = sec8_new[:sub_start] + subs_html + '\n' + sec8_new[sub_end:]
        html = html.replace(sec8_text, sec8_new, 1)
        print("Updated section-8 in tech_terraform.html")
    else:
        raise ValueError("Could not locate subsection boundaries in section-8")

    atomic_write(p, html)
    print("Saved tech_terraform.html successfully!")

def expand_all_tech():
    p = os.path.join(ROOT, 'all_tech.html')
    with open(p, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update edition & hero stats
    # 59 subsections -> 62 (+3 for Terraform)
    # 234 concepts -> 246 (+12 for Terraform: 12->24)
    html = re.sub(
        r'<div class="edition">v4 &bull; All-in-One Tech &amp; Engineering Portal &bull; 13 Disciplines &bull; \d+ Subsections &bull; \d+ Concepts</div>',
        '<div class="edition">v4 &bull; All-in-One Tech &amp; Engineering Portal &bull; 13 Disciplines &bull; 62 Subsections &bull; 246 Concepts</div>',
        html
    )

    html = re.sub(
        r'(<div class="stat"><div class="n">)\d+(</div><div class="l">Subsections</div></div>)',
        r'\g<1>62\g<2>',
        html
    )
    html = re.sub(
        r'(<div class="stat"><div class="n">)\d+(</div><div class="l">Concepts</div></div>)',
        r'\g<1>246\g<2>',
        html
    )

    # 2. Update card-terraform in domain deck
    card_tf_match = re.search(r'(<div class="domain-card[^"]*"[^>]*id="card-terraform"[\s\S]*?</div>\s*</div>)', html)
    if card_tf_match:
        old_card = card_tf_match.group(1)
        new_card = re.sub(
            r'<div class="domain-card-chips">[\s\S]*?</div>',
            '''<div class="domain-card-chips">
<span class="domain-card-chip">6 Subsections</span>
<span class="domain-card-chip">24 Concepts</span>
<span class="domain-card-chip highlight">HCL2, State Locking, Refactoring, Terragrunt & Policy as Code</span>
</div>''',
            old_card
        )
        html = html.replace(old_card, new_card, 1)
        print("Updated card-terraform in all_tech.html")

    # 3. Update Section 8 (Terraform) inside all_tech.html
    sec8_match = re.search(r'(<section class="section domain-section"[^>]*id="section-8"[\s\S]*?</section>)', html)
    if sec8_match:
        sec8_text = sec8_match.group(1)
        sec8_new = re.sub(
            r'<span class="focus-bar-stats">[^<]+</span>',
            '<span class="focus-bar-stats">24 concepts &bull; 6 subsections</span>',
            sec8_text
        )
        sec8_new = re.sub(
            r'<div class="meta">[^<]+</div>',
            '<div class="meta">6 subsections · 24 concepts</div>',
            sec8_new
        )
        sec8_new = re.sub(
            r'<div class="pct-text" data-pp-text="8">[^<]+</div>',
            '<div class="pct-text" data-pp-text="8">0 / 24</div>',
            sec8_new
        )
        subs_html = render_subsections_html(TERRAFORM_SUBSECTIONS)
        sub_start = sec8_new.find('<div class="subsection">')
        sub_end = sec8_new.rfind('</section>')
        if sub_start != -1 and sub_end != -1:
            sec8_new = sec8_new[:sub_start] + subs_html + '\n' + sec8_new[sub_end:]
            html = html.replace(sec8_text, sec8_new, 1)
            print("Updated section-8 in all_tech.html")
        else:
            raise ValueError("Could not find subsections in section-8 of all_tech.html")
    else:
        raise ValueError("Could not find section-8 in all_tech.html")

    atomic_write(p, html)
    print("Saved all_tech.html successfully!")

if __name__ == '__main__':
    expand_tech_terraform()
    expand_all_tech()
    print("Finished expanding Terraform Masterclass!")
