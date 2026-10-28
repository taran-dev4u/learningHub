# AWS Foundations & Identity and Access Management (IAM): The Staff Engineer Masterclass

## Overview

Master AWS global infrastructure, core cloud computing models, the shared responsibility model, and production-grade IAM access controls.

In high-throughput engineering environments and elite technical interviews, understanding this domain requires moving past high-level abstractions to the exact mechanical principles: how data flows, how state is reconciled, what failure boundaries exist, and how systems scale under peak production load.

### Core Conceptual Framework

> [!TIP]
> **Real-World Analogy: Cloud Models**
> Think of IaaS as renting an empty lot of land where you build your own house; PaaS is renting a furnished apartment where plumbing and heating are managed; SaaS is staying in a full-service luxury hotel where everything is provided.

> [!TIP]
> **Real-World Analogy: IAM**
> Think of IAM like a high-security corporate headquarters: IAM Users are individual employees with ID badges, Groups are departments, Roles are temporary visitor passes or hazmat suits worn by authorized personnel to perform a specific task, and Policies are the security rulebook defining which doors the badge can unlock.


## Cloud Computing Models (IaaS, PaaS, SaaS) & Shared Responsibility

<!-- anchor: cloud-computing-models-iaas-paas-saas-shared-responsibility -->

To master **Cloud Computing Models (IaaS, PaaS, SaaS) & Shared Responsibility**, an engineer must understand both the design trade-offs and the runtime mechanics.

### Architecture & Engineering Mechanics

When implementing `cloud-computing-models-iaas-paas-saas-shared-responsibility`, production systems must balance latency, durability, and operational overhead:

- **State & Isolation**: How resources are partitioned, bounded, and monitored.
- **Failure Modes**: Network partitioning, hardware degradation, and automated health reconciliation.
- **Observability**: Key metrics, alarms, and tracing spans required to operate this component safely at scale.


### Architectural Trade-Off Analysis

| Attribute | Standard Configuration | High-Performance / Hardened Configuration |
| :--- | :--- | :--- |
| **Throughput / Latency** | Baseline single-node execution | Clustered / Distributed with multi-path routing |
| **Failure Recovery** | Automated restart / failover | Multi-AZ active-active with automated circuit breaking |
| **Operational Cost** | Standard tier resource allocation | Reserved / Optimized allocation with auto-scaling bounds |
| **Security Boundary** | Standard network isolation | Zero-trust authentication with least-privilege IAM / RBAC |


## AWS Global Infrastructure: Regions, Availability Zones & Edge Locations

<!-- anchor: aws-global-infrastructure-regions-azs-edge-locations -->

To master **AWS Global Infrastructure: Regions, Availability Zones & Edge Locations**, an engineer must understand both the design trade-offs and the runtime mechanics.

### Architecture & Engineering Mechanics

When implementing `aws-global-infrastructure-regions-azs-edge-locations`, production systems must balance latency, durability, and operational overhead:

- **State & Isolation**: How resources are partitioned, bounded, and monitored.
- **Failure Modes**: Network partitioning, hardware degradation, and automated health reconciliation.
- **Observability**: Key metrics, alarms, and tracing spans required to operate this component safely at scale.


### Architectural Trade-Off Analysis

| Attribute | Standard Configuration | High-Performance / Hardened Configuration |
| :--- | :--- | :--- |
| **Throughput / Latency** | Baseline single-node execution | Clustered / Distributed with multi-path routing |
| **Failure Recovery** | Automated restart / failover | Multi-AZ active-active with automated circuit breaking |
| **Operational Cost** | Standard tier resource allocation | Reserved / Optimized allocation with auto-scaling bounds |
| **Security Boundary** | Standard network isolation | Zero-trust authentication with least-privilege IAM / RBAC |


## IAM Fundamentals: Root User Security, IAM Users, Groups & Policies

<!-- anchor: iam-fundamentals-root-users-groups-policies -->

To master **IAM Fundamentals: Root User Security, IAM Users, Groups & Policies**, an engineer must understand both the design trade-offs and the runtime mechanics.

### Architecture & Engineering Mechanics

When implementing `iam-fundamentals-root-users-groups-policies`, production systems must balance latency, durability, and operational overhead:

- **State & Isolation**: How resources are partitioned, bounded, and monitored.
- **Failure Modes**: Network partitioning, hardware degradation, and automated health reconciliation.
- **Observability**: Key metrics, alarms, and tracing spans required to operate this component safely at scale.


### Architectural Trade-Off Analysis

| Attribute | Standard Configuration | High-Performance / Hardened Configuration |
| :--- | :--- | :--- |
| **Throughput / Latency** | Baseline single-node execution | Clustered / Distributed with multi-path routing |
| **Failure Recovery** | Automated restart / failover | Multi-AZ active-active with automated circuit breaking |
| **Operational Cost** | Standard tier resource allocation | Reserved / Optimized allocation with auto-scaling bounds |
| **Security Boundary** | Standard network isolation | Zero-trust authentication with least-privilege IAM / RBAC |


## IAM Roles, Instance Profiles & STS AssumeRole Delegation

<!-- anchor: iam-roles-instance-profiles-sts-assumerole -->

To master **IAM Roles, Instance Profiles & STS AssumeRole Delegation**, an engineer must understand both the design trade-offs and the runtime mechanics.

### Architecture & Engineering Mechanics

When implementing `iam-roles-instance-profiles-sts-assumerole`, production systems must balance latency, durability, and operational overhead:

- **State & Isolation**: How resources are partitioned, bounded, and monitored.
- **Failure Modes**: Network partitioning, hardware degradation, and automated health reconciliation.
- **Observability**: Key metrics, alarms, and tracing spans required to operate this component safely at scale.


### Architectural Trade-Off Analysis

| Attribute | Standard Configuration | High-Performance / Hardened Configuration |
| :--- | :--- | :--- |
| **Throughput / Latency** | Baseline single-node execution | Clustered / Distributed with multi-path routing |
| **Failure Recovery** | Automated restart / failover | Multi-AZ active-active with automated circuit breaking |
| **Operational Cost** | Standard tier resource allocation | Reserved / Optimized allocation with auto-scaling bounds |
| **Security Boundary** | Standard network isolation | Zero-trust authentication with least-privilege IAM / RBAC |


## Policy Evaluation Logic: Explicit Deny, SCPs & Permission Boundaries

<!-- anchor: policy-evaluation-logic-scps-permission-boundaries -->

To master **Policy Evaluation Logic: Explicit Deny, SCPs & Permission Boundaries**, an engineer must understand both the design trade-offs and the runtime mechanics.

### Architecture & Engineering Mechanics

When implementing `policy-evaluation-logic-scps-permission-boundaries`, production systems must balance latency, durability, and operational overhead:

- **State & Isolation**: How resources are partitioned, bounded, and monitored.
- **Failure Modes**: Network partitioning, hardware degradation, and automated health reconciliation.
- **Observability**: Key metrics, alarms, and tracing spans required to operate this component safely at scale.


### Architectural Trade-Off Analysis

| Attribute | Standard Configuration | High-Performance / Hardened Configuration |
| :--- | :--- | :--- |
| **Throughput / Latency** | Baseline single-node execution | Clustered / Distributed with multi-path routing |
| **Failure Recovery** | Automated restart / failover | Multi-AZ active-active with automated circuit breaking |
| **Operational Cost** | Standard tier resource allocation | Reserved / Optimized allocation with auto-scaling bounds |
| **Security Boundary** | Standard network isolation | Zero-trust authentication with least-privilege IAM / RBAC |


## Teacher FAQ & Common Production Doubts

> [!NOTE]
> **Question: When should I use an IAM Role vs an IAM User with static API keys?**
>
> **Teacher's Answer:** Never store static IAM User access keys on EC2 instances or in code. Always use IAM Roles attached via Instance Profiles or OIDC tokens for automated rotation and temporary STS credentials.

> [!NOTE]
> **Question: What is the difference between an SCP and an IAM Policy?**
>
> **Teacher's Answer:** SCPs (Service Control Policies) in AWS Organizations set the guardrail ceiling across an entire AWS account or OU. They never grant permissions; they only restrict the maximum permissions that IAM policies inside that account can grant.


## Production Readiness Checklist

1. **Idempotency & Retry Safety**: Are operations safe against duplicate delivery or retries?
2. **Least Privilege**: Are permissions strictly bounded to required resources?
3. **Metrics & Alarms**: Are error rate, latency P99, and saturation alarms configured?
4. **Disaster Recovery**: Is state replicated across independent fault domains with validated restore drills?
