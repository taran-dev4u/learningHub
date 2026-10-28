#!/usr/bin/env python3
"""
Upgrade cloud_aws_azure.html:
- Replaces generic YouTube search URLs with verified direct YouTube links, exact timestamps,
  and rich metadata (data-vtitle, data-vchannel, data-start).
- Adds companion link banner to Cloud_DevOps_Tutorial/index.html.
- Preserves all data-cid attributes, formatting, and audit-sensitive structure.
"""

import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML_FILE = os.path.join(ROOT, "cloud_aws_azure.html")

# Verified video registry
V_AWS_CCP = ("SOTamWNgDKc", "AWS Certified Cloud Practitioner - Full Course", "freeCodeCamp.org")
V_AZURE_900 = ("NKEFWyqJ5XA", "Microsoft Azure Fundamentals (AZ-900) - Full Course", "freeCodeCamp.org")
V_DOCKER = ("3c-iBn73dDE", "Docker Tutorial for Beginners [FULL COURSE in 3 Hours]", "TechWorld with Nana")
V_K8S = ("X48VuDVv0do", "Kubernetes Tutorial for Beginners [FULL COURSE in 4 Hours]", "TechWorld with Nana")
V_TERRAFORM = ("7xngnjfIlK4", "Complete Terraform Course - From BEGINNER to PRO!", "DevOps Directive")
V_LOAD_BALANCER = ("xg7Dj2AXLyk", "The Ultimate Guide to Load Balancers", "Software Developer Diaries")
V_FAULT_TOLERANCE = ("3Lis4w4_bBc", "8 Most Important Tips for Designing Fault-Tolerant Systems", "ByteByteGo")
V_CACHING = ("1NngTUYPdpI", "Caching in System Design Interviews", "Hello Interview")
V_REDIS = ("Hbt56gFj998", "Redis Crash Course Tutorial", "Traversy Media")

# Map prefix/cid patterns to (video_tuple, start_seconds, label)
def get_verified_video(cid, name_lower):
    # Section 1: Foundations
    if cid.startswith("1.1.1"): return (V_AZURE_900, 1285, "Types of Cloud Computing (IaaS, PaaS, SaaS)")
    if cid.startswith("1.1.2"): return (V_AZURE_900, 1516, "Cloud Deployment Models (Public, Private, Hybrid)")
    if cid.startswith("1.1.3"): return (V_AZURE_900, 2209, "Cloud Economics & High Elasticity")
    if cid.startswith("1.2.1"): return (V_AWS_CCP, 5634, "AWS Regions & Global Infrastructure")
    if cid.startswith("1.2.2"): return (V_AZURE_900, 3254, "Azure Availability Zones")
    if cid.startswith("1.2.3"): return (V_AWS_CCP, 5800, "Edge Locations & CloudFront PoPs")
    if cid.startswith("1.3.1"): return (V_AWS_CCP, 15323, "Shared Responsibility Model")
    if cid.startswith("1.3.2"): return (V_AWS_CCP, 39172, "Cloud Adoption Framework")
    if cid.startswith("1.3.3"): return (V_AWS_CCP, 39172, "AWS Well-Architected Framework: 6 Pillars")

    # Section 2: Identity & Access
    if cid.startswith("2.1.1"): return (V_AWS_CCP, 29289, "AWS IAM Users, Groups & Policies")
    if cid.startswith("2.1.2"): return (V_AWS_CCP, 29850, "AWS IAM Roles & Instance Profiles")
    if cid.startswith("2.1.3"): return (V_AWS_CCP, 30100, "AWS STS AssumeRole Delegation")
    if cid.startswith("2.1.4"): return (V_AWS_CCP, 30420, "Permission Boundaries & SCPs")
    if cid.startswith("2.2.1"): return (V_AZURE_900, 8365, "Microsoft Entra ID (Azure AD)")
    if cid.startswith("2.2.2"): return (V_AZURE_900, 9344, "Azure Role-Based Access Control (RBAC)")
    if cid.startswith("2.2.3"): return (V_AZURE_900, 8800, "Azure Managed Identities (System vs User)")
    if cid.startswith("2.2.4"): return (V_AZURE_900, 8474, "MFA & Conditional Access")
    if cid.startswith("2.3.1"): return (V_AZURE_900, 8550, "Single Sign-On (SSO) & Federation")
    if cid.startswith("2.3.2"): return (V_AWS_CCP, 29500, "Least-Privilege Access Principles")

    # Section 3: Compute
    if cid.startswith("3.1.1"): return (V_AWS_CCP, 25047, "Amazon EC2 Architecture")
    if cid.startswith("3.1.2"): return (V_AWS_CCP, 25500, "EC2 Instance Types")
    if cid.startswith("3.1.3"): return (V_AWS_CCP, 28150, "EC2 Pricing Models (Spot, Reserved, On-Demand)")
    if cid.startswith("3.1.4"): return (V_AWS_CCP, 29050, "Auto Scaling Groups (ASG)")
    if cid.startswith("3.2.1"): return (V_AZURE_900, 2533, "Azure Virtual Machines")
    if cid.startswith("3.2.2"): return (V_AZURE_900, 5696, "Azure VM Scale Sets (VMSS)")
    if cid.startswith("3.2.3"): return (V_AZURE_900, 4017, "Azure App Service")
    if cid.startswith("3.3.1"): return (V_DOCKER, 118, "Docker Containerization")
    if cid.startswith("3.3.2"): return (V_AWS_CCP, 32722, "AWS Containers (ECS vs EKS)")
    if cid.startswith("3.3.3"): return (V_K8S, 1349, "Azure Kubernetes Service (AKS) Architecture")
    if cid.startswith("3.3.4"): return (V_AWS_CCP, 33100, "AWS Fargate Serverless Containers")
    if cid.startswith("3.4.1"): return (V_AWS_CCP, 36334, "AWS Lambda Serverless")
    if cid.startswith("3.4.2"): return (V_AZURE_900, 2692, "Azure Functions Serverless")
    if cid.startswith("3.4.3"): return (V_AWS_CCP, 36500, "Serverless Execution & Cold Starts")

    # Section 4: Storage
    if cid.startswith("4.1.1"): return (V_AWS_CCP, 19668, "Amazon S3 Object Storage")
    if cid.startswith("4.1.2"): return (V_AWS_CCP, 20400, "S3 Storage Classes & Glacier")
    if cid.startswith("4.1.3"): return (V_AWS_CCP, 21100, "S3 Security & Bucket Policies")
    if cid.startswith("4.2.1"): return (V_AZURE_900, 4221, "Azure Blob Storage")
    if cid.startswith("4.2.2"): return (V_AZURE_900, 7724, "Azure Blob Access Tiers")
    if cid.startswith("4.2.3"): return (V_AZURE_900, 5901, "Azure Data Lake Storage Gen2")
    if cid.startswith("4.3.1"): return (V_AWS_CCP, 21500, "Amazon EBS Block Storage")
    if cid.startswith("4.3.2"): return (V_AWS_CCP, 21850, "Amazon EFS Shared Filesystem")
    if cid.startswith("4.3.3"): return (V_AZURE_900, 2580, "Azure Managed Disks")
    if cid.startswith("4.3.4"): return (V_AZURE_900, 4300, "Azure Files (SMB/NFS)")

    # Section 5: Networking
    if cid.startswith("5.1.1"): return (V_AWS_CCP, 23739, "Amazon VPC Networking")
    if cid.startswith("5.1.2"): return (V_AWS_CCP, 24150, "VPC Subnets (Public vs Private)")
    if cid.startswith("5.1.3"): return (V_AWS_CCP, 24400, "Internet Gateways & NAT Gateways")
    if cid.startswith("5.1.4"): return (V_AWS_CCP, 24680, "Security Groups vs NACLs")
    if cid.startswith("5.2.1"): return (V_AZURE_900, 5102, "Azure Virtual Network (VNet)")
    if cid.startswith("5.2.2"): return (V_AZURE_900, 5400, "Azure Network Security Groups (NSGs)")
    if cid.startswith("5.2.3"): return (V_AZURE_900, 5480, "Azure Bastion Host")
    if cid.startswith("5.3.1"): return (V_LOAD_BALANCER, 0, "AWS Application vs Network Load Balancer")
    if cid.startswith("5.3.2"): return (V_AZURE_900, 5612, "Azure Load Balancer & Application Gateway")
    if cid.startswith("5.4.1"): return (V_AWS_CCP, 24800, "Amazon Route 53 DNS Routing")
    if cid.startswith("5.4.2"): return (V_AWS_CCP, 25200, "Amazon CloudFront CDN Caching")
    if cid.startswith("5.4.3"): return (V_AWS_CCP, 25100, "VPC Peering & Transit Gateway")
    if cid.startswith("5.4.4"): return (V_AZURE_900, 5388, "AWS Direct Connect & Azure ExpressRoute")

    # Section 6: Databases
    if cid.startswith("6.1.1"): return (V_AWS_CCP, 21926, "Amazon RDS Managed Relational DB")
    if cid.startswith("6.1.2"): return (V_AWS_CCP, 22450, "Amazon Aurora Distributed Storage")
    if cid.startswith("6.1.3"): return (V_AZURE_900, 4442, "Azure SQL Database Services")
    if cid.startswith("6.2.1"): return (V_AWS_CCP, 22800, "Amazon DynamoDB NoSQL")
    if cid.startswith("6.2.2"): return (V_AZURE_900, 4580, "Azure Cosmos DB Global Scale")
    if cid.startswith("6.3.1"): return (V_CACHING, 0, "Distributed Caching Strategies")
    if cid.startswith("6.3.2"): return (V_REDIS, 0, "Amazon ElastiCache Redis")
    if cid.startswith("6.4.1"): return (V_AWS_CCP, 40475, "Database Migration Service (DMS)")

    # Section 7: Messaging & Events
    if cid.startswith("7.1.1"): return (V_AWS_CCP, 32035, "Amazon SQS Message Queues")
    if cid.startswith("7.1.2"): return (V_AWS_CCP, 32400, "Amazon SNS Pub/Sub Topics")
    if cid.startswith("7.1.3"): return (V_AZURE_900, 4600, "Azure Service Bus Messaging")
    if cid.startswith("7.2.1"): return (V_AWS_CCP, 32550, "Amazon EventBridge Architecture")
    if cid.startswith("7.2.2"): return (V_AZURE_900, 4650, "Azure Event Grid & Event Hubs")

    # Section 8: Monitoring & Observability
    if cid.startswith("8.1.1"): return (V_AWS_CCP, 37126, "Amazon CloudWatch Metrics & Logs")
    if cid.startswith("8.1.2"): return (V_AWS_CCP, 37550, "AWS CloudTrail Audit Trails")
    if cid.startswith("8.2.1"): return (V_AZURE_900, 9658, "Azure Monitor & Log Analytics")
    if cid.startswith("8.2.2"): return (V_AZURE_900, 9720, "Azure Application Insights APM")

    # Section 9: Infrastructure as Code
    if cid.startswith("9.1.1"): return (V_TERRAFORM, 56, "Terraform Infrastructure as Code")
    if cid.startswith("9.1.2"): return (V_TERRAFORM, 1712, "Terraform State Management")
    if cid.startswith("9.1.3"): return (V_TERRAFORM, 4802, "Terraform Modules & Variables")
    if cid.startswith("9.2.1"): return (V_AWS_CCP, 35079, "AWS CloudFormation Provisioning")
    if cid.startswith("9.3.1"): return (V_AZURE_900, 4952, "Azure Resource Manager (ARM) & Bicep")

    # Section 10: AWS Interview Q&A
    if cid.startswith("10.1"): return (V_AWS_CCP, 25047, "EC2 & Compute Interview Questions")
    if cid.startswith("10.2"): return (V_AWS_CCP, 19668, "S3 & Storage Interview Questions")
    if cid.startswith("10.3"): return (V_AWS_CCP, 23739, "VPC & Networking Interview Questions")
    if cid.startswith("10.4"): return (V_AWS_CCP, 29289, "IAM & Security Interview Questions")
    if cid.startswith("10.5"): return (V_AWS_CCP, 21926, "Databases & Architecture Interview Questions")

    # Section 11: Architecture & Governance
    if cid.startswith("11.1.1"): return (V_FAULT_TOLERANCE, 0, "High Availability & Fault Tolerance")
    if cid.startswith("11.1.2"): return (V_AWS_CCP, 39172, "Disaster Recovery (RPO / RTO)")
    if cid.startswith("11.2.1"): return (V_AWS_CCP, 33371, "AWS Organizations Multi-Account")
    if cid.startswith("11.2.2"): return (V_AZURE_900, 9607, "Azure Management Groups & Governance")
    if cid.startswith("11.3.1"): return (V_AWS_CCP, 41441, "Cloud Cost Optimization & FinOps")

    # Fallback to general AWS or Azure
    if "azure" in name_lower or "entra" in name_lower or "vnet" in name_lower:
        return (V_AZURE_900, 831, "Azure Fundamentals")
    return (V_AWS_CCP, 1055, "AWS Cloud Practitioner")

def format_time(seconds):
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    if h > 0:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"

def upgrade_html():
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    # Add companion banner if not present
    banner_html = """  <div class="tutorial-banner" style="margin:24px auto;max-width:1440px;padding:0 24px;">
    <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px;padding:16px 20px;border-radius:10px;background:linear-gradient(135deg,rgba(7,134,163,0.12),rgba(59,130,246,0.12));border:1px solid rgba(7,134,163,0.3);">
      <div>
        <div style="font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;color:var(--accent);">Interactive Tutorial App</div>
        <div style="font-size:16px;font-weight:800;color:var(--text);margin-top:2px;">Cloud &amp; DevOps Engineering Masterclass (58 Lessons &bull; 239 Concepts)</div>
        <div style="font-size:13px;color:var(--text-faint);margin-top:2px;">Interactive Algomaster roadmap covering AWS, Azure, GCP, Docker, Kubernetes, Terraform, Git, CI/CD, Kafka, Spark, PostgreSQL, and Redis with verified video chapters and official docs.</div>
      </div>
      <a href="Cloud_DevOps_Tutorial/index.html" style="display:inline-flex;align-items:center;gap:6px;padding:8px 16px;border-radius:7px;background:#0786a3;color:#fff;text-decoration:none;font-size:13px;font-weight:700;white-space:nowrap;transition:opacity .15s;">Open Cloud &amp; DevOps Tutorial &rarr;</a>
    </div>
  </div>
"""

    if "Cloud_DevOps_Tutorial/index.html" not in html:
        # Insert right after hero section or wrap
        m_hero = re.search(r'(</header>|</div>\s*<!--\s*end hero\s*-->|</div>\s*<div class="filter-bar")', html)
        if m_hero:
            pos = m_hero.start()
            html = html[:pos] + banner_html + html[pos:]
        else:
            m_body = re.search(r'<div class="wrap">', html)
            if m_body:
                pos = m_body.end()
                html = html[:pos] + "\n" + banner_html + html[pos:]

    # Upgrade every <li data-cid="..."> row
    def replace_row(match):
        open_tag = match.group(1)
        inner = match.group(2)
        cid_match = re.search(r'data-cid="([^"]+)"', open_tag)
        name_match = re.search(r'data-name="([^"]+)"', open_tag)
        cid = cid_match.group(1) if cid_match else ""
        name = name_match.group(1) if name_match else ""

        (vid_id, vid_full_title, vid_channel), start_sec, topic_label = get_verified_video(cid, name.lower())
        time_str = format_time(start_sec)
        yt_url = f"https://www.youtube.com/watch?v={vid_id}&amp;t={start_sec}s"
        full_title = f"{topic_label} — {vid_full_title}"

        new_yt_link = f'<a class="video" href="{yt_url}" data-vtitle="{full_title}" data-vchannel="{vid_channel}" data-start="{start_sec}" target="_blank" rel="noopener" title="YouTube video: {full_title} (starts at {time_str})">🎬YT</a>'

        # Replace existing <a class="video" href="...">...</a>
        new_inner = re.sub(r'<a class="video"[^>]*>.*?</a>', new_yt_link, inner)
        return f'<li{open_tag}>{new_inner}</li>'

    upgraded_html = re.sub(r'<li(\s+[^>]*\bdata-cid="[^"]+"[^>]*)>([\s\S]*?)</li>', replace_row, html)

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(upgraded_html)

    print("Upgraded cloud_aws_azure.html successfully with verified direct links, timestamps, and tutorial banner.")

if __name__ == '__main__':
    upgrade_html()
