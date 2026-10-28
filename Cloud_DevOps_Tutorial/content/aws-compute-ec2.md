# AWS Compute: EC2, Elastic Load Balancing & Auto Scaling: The Staff Engineer Masterclass

## Overview

Engineer scalable compute clusters with EC2 instance types, launch templates, elastic load balancing (ALB/NLB), and dynamic autoscaling.

In high-throughput engineering environments and elite technical interviews, understanding this domain requires moving past high-level abstractions to the exact mechanical principles: how data flows, how state is reconciled, what failure boundaries exist, and how systems scale under peak production load.

### Core Conceptual Framework

> [!TIP]
> **Real-World Analogy: Load Balancers**
> Think of an Application Load Balancer (ALB) like a smart restaurant maître d' who reads the customer's reservation ticket (URL path, HTTP headers) and escorts them to the specific sushi, pasta, or dessert chef. A Network Load Balancer (NLB) is like an ultra-high-speed highway toll plaza directing millions of vehicles purely by lane number (TCP/UDP port) in microsecond latency.


## EC2 Architecture: Instance Types, AMIs & User Data Bootstrap Scripts

<!-- anchor: ec2-architecture-instance-types-amis-userdata -->

To master **EC2 Architecture: Instance Types, AMIs & User Data Bootstrap Scripts**, an engineer must understand both the design trade-offs and the runtime mechanics.

### Architecture & Engineering Mechanics

When implementing `ec2-architecture-instance-types-amis-userdata`, production systems must balance latency, durability, and operational overhead:

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


## EC2 Pricing Models: On-Demand, Savings Plans, Reserved & Spot Instances

<!-- anchor: ec2-pricing-models-reserved-spot-instances -->

To master **EC2 Pricing Models: On-Demand, Savings Plans, Reserved & Spot Instances**, an engineer must understand both the design trade-offs and the runtime mechanics.

### Architecture & Engineering Mechanics

When implementing `ec2-pricing-models-reserved-spot-instances`, production systems must balance latency, durability, and operational overhead:

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


## Elastic Load Balancers: ALB (Layer 7) vs NLB (Layer 4) Architecture

<!-- anchor: elastic-load-balancers-alb-vs-nlb -->

To master **Elastic Load Balancers: ALB (Layer 7) vs NLB (Layer 4) Architecture**, an engineer must understand both the design trade-offs and the runtime mechanics.

### Architecture & Engineering Mechanics

When implementing `elastic-load-balancers-alb-vs-nlb`, production systems must balance latency, durability, and operational overhead:

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


## Target Groups, Health Checks & Cross-Zone Load Balancing

<!-- anchor: target-groups-health-checks-cross-zone-balancing -->

To master **Target Groups, Health Checks & Cross-Zone Load Balancing**, an engineer must understand both the design trade-offs and the runtime mechanics.

### Architecture & Engineering Mechanics

When implementing `target-groups-health-checks-cross-zone-balancing`, production systems must balance latency, durability, and operational overhead:

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


## Auto Scaling Groups (ASG): Launch Templates & Dynamic Scaling Policies

<!-- anchor: auto-scaling-groups-launch-templates-scaling-policies -->

To master **Auto Scaling Groups (ASG): Launch Templates & Dynamic Scaling Policies**, an engineer must understand both the design trade-offs and the runtime mechanics.

### Architecture & Engineering Mechanics

When implementing `auto-scaling-groups-launch-templates-scaling-policies`, production systems must balance latency, durability, and operational overhead:

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
> **Question: When should I choose Spot Instances over On-Demand or Reserved Instances?**
>
> **Teacher's Answer:** Spot Instances offer up to 90% cost savings and are ideal for fault-tolerant, stateless batch workloads, CI/CD runners, and big data workers that can withstand a 2-minute termination notice.

> [!NOTE]
> **Question: What is the difference between ALB and NLB?**
>
> **Teacher's Answer:** ALB operates at Layer 7 (HTTP/HTTPS) and can inspect URLs, query parameters, and cookies. NLB operates at Layer 4 (TCP/UDP/TLS) and is optimized for ultra-high throughput, static IP requirements, and extreme low latency (microseconds).


## Production Readiness Checklist

1. **Idempotency & Retry Safety**: Are operations safe against duplicate delivery or retries?
2. **Least Privilege**: Are permissions strictly bounded to required resources?
3. **Metrics & Alarms**: Are error rate, latency P99, and saturation alarms configured?
4. **Disaster Recovery**: Is state replicated across independent fault domains with validated restore drills?
