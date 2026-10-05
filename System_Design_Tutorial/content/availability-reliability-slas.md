# Availability, Reliability & SLAs

## Overview

In mission-critical enterprise engineering, system failure is not an anomaly; it is an inevitable statistical certainty. Hard drives experience mechanical fatigue, memory modules suffer cosmic-ray bit flips, power supplies burn out, fiber-optic backbones are severed by backhoes, and software deployments introduce latent race conditions.

Senior and staff software engineers do not attempt to construct "indestructible" components. Instead, we architect **fault-tolerant distributed topologies** that preserve continuous operational availability despite the ceaseless, concurrent failure of individual constituent nodes.

This masterclass establishes the mathematical, probabilistic, and operational engineering frameworks required to quantify, design, and guarantee High Availability (HA) across modern cloud infrastructure.

---

## SLI, SLO, and SLA Metrics

To engineer availability, you must first define it with mathematical precision. The Site Reliability Engineering (SRE) discipline pioneered by Google establishes three foundational tiers:

```
┌─────────────────────────────────────────────────────────────┐
│              SLA (Service Level Agreement)                  │
│       Legal contract with customers (Financial penalty)     │
│   e.g., "99.9% monthly availability or 15% bill credit"     │
├─────────────────────────────────────────────────────────────┤
│              SLO (Service Level Objective)                  │
│       Internal engineering target (Stricter than SLA)       │
│   e.g., "99.95% monthly availability target for on-call"    │
├─────────────────────────────────────────────────────────────┤
│              SLI (Service Level Indicator)                  │
│       Real-time measured metric (The ground truth)          │
│   e.g., Successful HTTP reqs (2xx/3xx < 250ms) / Total reqs │
└─────────────────────────────────────────────────────────────┘
```

### 1. Service Level Indicator (SLI)
An **SLI** is a quantifiable metric that directly measures the quality of service delivered to consumers.
$$\text{SLI} = \frac{\text{Count of Valid Events Meeting Good-Quality Criteria}}{\text{Total Count of Valid Events}} \times 100\%$$

*Examples of production SLIs:*
- **Latency SLI:** Percentage of successful `GET /v1/checkout` requests completed in $< 150\text{ ms}$ over a rolling 30-day window.
- **Availability SLI:** Ratio of non-5xx HTTP responses to total inbound HTTP transactions:
  $$\text{Availability SLI} = \frac{\sum (\text{HTTP Status} < 500)}{\sum \text{All HTTP Requests}} \times 100\%$$

### 2. Service Level Objective (SLO)
An **SLO** is the target reliability goal set by internal engineering and product leadership. It establishes the operational boundary between shipping new product features and freezing deployments to focus on technical debt.
- *Example:* "The payment service must achieve $\ge 99.95\%$ availability across every rolling 30-day window."

### 3. Service Level Agreement (SLA)
An **SLA** is the legally binding commercial contract negotiated with external customers or enterprise clients. It defines the explicit consequences (service credits, financial refunds, or contractual termination) if the provider fails to meet the promised service level.

> [!TIP]
> **The Golden Safety Buffer Rule:**
> $$\text{SLI (Observed)} \ge \text{SLO (Internal Target)} > \text{SLA (Legal Floor)}$$
> Never align your internal SLO with your external SLA. If your legal SLA is **99.9%**, your internal engineering SLO must be **99.95%** or **99.99%**. That delta represents your **safety buffer**, preventing customer-facing SLA breaches and financial penalties during unexpected outages.

### 4. Error Budgets and Burn Rates
The **Error Budget** is the exact mathematical inverse of your SLO:
$$\text{Error Budget} = 100\% - \text{SLO}$$
If your 30-day SLO is **99.9%**, your system is allowed **0.1% of failure** over that 30-day period.

- **1x Burn Rate:** Consumes exactly 100% of the error budget over 30 days (steady-state compliance).
- **14.4x Burn Rate:** Consumes 2% of the total monthly error budget in 1 hour. This triggers a high-severity pager alert to wake up on-call engineers.

---

## High Availability & Uptime Calculations (The Nines)

Availability is categorized by the number of "Nines" in its percentage uptime. You must memorize these exact operational downtime allowances:

| Nines | Availability | Downtime / Year | Downtime / Month (30d) | Downtime / Week | Downtime / Day | Typical Real-World Target |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Two 9s** | **99.0%** | 3.65 days | 7.20 hours | 1.68 hours | 14.40 minutes | Dev/staging environments, internal tools |
| **Three 9s** | **99.9%** | 8.76 hours | 43.80 minutes | 10.08 minutes | 1.44 minutes | Standard consumer web apps (Shopify, Medium) |
| **Four 9s** | **99.99%** | 52.56 minutes | 4.38 minutes | 1.01 minutes | 8.64 seconds | Tier-1 Cloud APIs, Stripe, AWS DynamoDB |
| **Five 9s** | **99.999%** | 5.26 minutes | 25.92 seconds | 6.05 seconds | 864 milliseconds | Telecommunications, financial ledgers, hospitals |
| **Six 9s** | **99.9999%** | 31.54 seconds | 2.59 seconds | 604 milliseconds | 86.4 milliseconds | Aerospace flight control, nuclear grids |

### The "Five Nines" Reality Check
Notice that **Five 9s** permits only **5 minutes and 15 seconds of total downtime across an entire calendar year**. 
- It is physically impossible to achieve Five 9s if recovery requires a human engineer to read an alert, log into a bastion host, and restart a crashed service (which takes 5–15 minutes minimum).
- Five 9s mandates **fully automated, zero-human-intervention self-healing**: automated health checks, automated load balancer fencing, sub-second consensus leader failovers, and redundant multi-region architectures.

### MTBF, MTTR, and MTTF Formulations
Engineers quantify hardware and component reliability using mean time statistics:

```
◄───────────────────────── MTBF (Mean Time Between Failures) ────────────────────────►
┌───────────────────────────────────────────────┬────────────────────────────────────┐
│         MTTF (Mean Time To Failure)           │    MTTR (Mean Time To Repair)      │
│          Component is operational             │  Failure occurs -> Restoration     │
└───────────────────────────────────────────────┴────────────────────────────────────┘
```

$$\text{Availability} = \frac{\text{MTTF}}{\text{MTTF} + \text{MTTR}} = \frac{\text{MTBF}}{\text{MTBF} + \text{MTTR}}$$

To increase availability, you have two independent engineering levers:
1. **Increase MTTF:** Build more resilient components (ECC memory, dual power supplies, automated testing).
2. **Decrease MTTR:** Accelerate recovery via automated failover, health probing, canary deployments, and hot standbys. In cloud software, reducing MTTR from 30 minutes to 300 milliseconds increases availability by two orders of magnitude!

---

## Cascading Availability in Series

When architectural components are connected in **series**, every component in the dependency chain must be operational for the overall user transaction to succeed.

```
[Client] ──► [API Gateway] ──► [Auth Service] ──► [Order Service] ──► [Database]
              (A₁ = 99.9%)      (A₂ = 99.9%)       (A₃ = 99.9%)      (A₄ = 99.9%)
```

### The Series Availability Theorem
For a synchronous system composed of $n$ independent components in series, overall availability $A_{\text{total}}$ is the mathematical product of the individual availabilities:
$$A_{\text{total}} = \prod_{i=1}^n A_i = A_1 \times A_2 \times \dots \times A_n$$

### The Cascading Degradation Example
Suppose an e-commerce checkout flow requires 4 services in series, each boasting a respectable **99.9% (Three 9s)** availability:
$$A_{\text{total}} = 0.999 \times 0.999 \times 0.999 \times 0.999 = (0.999)^4 \approx 0.9960 \text{ (99.60\%)}$$

**The Consequence:**
- A system of four 99.9% services drops to **99.6% overall availability**!
- Annual downtime increases from **8.76 hours** to **35.04 hours**—a 400% increase in customer-facing outages!

> [!WARNING]
> **Microservices Anti-Pattern:** A distributed architecture with deep, synchronous dependency chains (Service A calls B, which calls C, which calls D, which calls E) will inevitably suffer from catastrophic cascading fragility. Every synchronous hop mathematically degrades the system's theoretical uptime.

---

## Redundancy & Parallel Availability

To counteract the mathematical degradation of series chains, distributed systems introduce **Parallel Redundancy**.

```
                           ┌──► [Web Server 1 (A₁ = 99%)] ──┐
                           │                                │
[Client] ──► [Load Balancer]──► [Web Server 2 (A₂ = 99%)] ──┼──► [Response]
                           │                                │
                           └──► [Web Server 3 (A₃ = 99%)] ──┘
```

### The Parallel Availability Theorem
For a cluster of $n$ redundant, independent components operating in parallel, the entire subsystem fails **only if every single component fails simultaneously**.

Let $U_i = 1 - A_i$ denote the probability of failure (unavailability) for component $i$.
$$U_{\text{total}} = \prod_{i=1}^n (1 - A_i)$$
$$A_{\text{total}} = 1 - U_{\text{total}} = 1 - \prod_{i=1}^n (1 - A_i)$$

### The Redundancy Multiplication Effect
Consider three commodity web servers, each with poor reliability of only **99.0% (Two 9s)**:
- Probability of a single server failing: $1 - 0.99 = 0.01$ (1%).
- Probability of all 3 servers failing simultaneously:
  $$U_{\text{total}} = 0.01 \times 0.01 \times 0.01 = 0.000001 \text{ (0.0001\%)}$$
- Overall cluster availability:
  $$A_{\text{total}} = 1 - 0.000001 = 0.999999 \text{ (99.9999\% — Six 9s!)}$$

By placing three mediocre, inexpensive servers in parallel behind a load balancer, we mathematically synthesized a six-nines subsystem.

---

## Active-Active Failover Architecture

In an **Active-Active** topology, two or more instances, datacenters, or cloud availability zones process live client traffic simultaneously.

```
                          Client DNS Request
                                  │
                                  ▼
                   [ GeoDNS / Anycast BGP Routing ]
                       ┌──────────┴──────────┐
                       ▼ 50% Traffic         ▼ 50% Traffic
                 ┌───────────┐         ┌───────────┐
                 │ Region A  │         │ Region B  │
                 │ (Active)  │◄───────►│ (Active)  │
                 │           │  Async  │           │
                 │ Web & DB  │ Replic. │ Web & DB  │
                 └───────────┘         └───────────┘
```

### 1. Traffic Ingress & Routing
- **GeoDNS:** Directs clients to the nearest regional datacenter based on client IP geolocation.
- **Anycast BGP:** Announces identical IP addresses from multiple geographic locations; routers automatically steer packets along the shortest physical network path.

### 2. Advantages
- **Zero-Downtime Failover:** If Region A catches fire or loses network connectivity, health checkers instruct GeoDNS/Anycast to route 100% of traffic to Region B. No cold boots or service startups are required.
- **Full Hardware Utilization:** 100% of purchased computing capacity serves revenue-generating traffic during normal operations.

### 3. The "50% Headroom" Capacity Trap
Beginners assume that if two datacenters each run at 80% CPU utilization, the system is efficient. **This is a fatal production design flaw.**
- If Datacenter A crashes, its 50% of global traffic is instantaneously diverted to Datacenter B.
- Datacenter B was already at 80% CPU capacity. It is now hit with $80\% \times 2 = 160\%$ load.
- Datacenter B's CPUs peg at 100%, request queues fill up, memory exhausts, and Datacenter B crashes.
- **The Golden Rule:** In a 2-node Active-Active topology, neither node should ever exceed **40% to 50% steady-state capacity**.

---

## Active-Passive Failover Architecture

In an **Active-Passive** (Primary-Standby) topology, only the Primary node processes production read/write traffic. The Secondary node sits idle in standby mode, continuously replicating data from the Primary.

```
                           [ Virtual IP (VIP) ]
                                    │
                         ┌──────────┴──────────┐
                         ▼ Active Traffic      │ (Heartbeat Probe)
                  ┌─────────────┐              ▼
                  │   Primary   │─────────►┌─────────────┐
                  │  (Active)   │ Sync/Asy │  Secondary  │
                  │             │ Replic.  │  (Standby)  │
                  └─────────────┘          └─────────────┘
```

### 1. Failover Mechanics
1. **Heartbeat Probing:** The Standby node continuously sends sub-second heartbeat pings over a dedicated network interface to the Primary.
2. **Failure Detection:** If the Primary fails to respond to 3 consecutive heartbeats (e.g., 3 seconds of silence), the Standby declares the Primary dead.
3. **VIP Reassignment (GARP):** The Standby transmits a Gratuitous ARP (GARP) packet to the local network switch, remapping the Virtual IP (VIP) address to its own MAC address.
4. **Promotion:** The Standby transitions its local database engine from read-only replica mode to read-write primary mode.

### 2. Split-Brain Syndrome and Fencing (STONITH)
What if the Primary did not actually die, but a transient local network glitch merely severed the heartbeat wire between Primary and Standby?
- The Standby erroneously assumes the Primary is dead and promotes itself.
- **The Catastrophe (Split-Brain):** Both nodes now believe they are the legitimate Primary. Both accept writes from clients, and their underlying data diverges irreversibly.

#### The Solution: STONITH (Shoot The Other Node In The Head)
Before a Standby is legally allowed to promote itself to Primary, it must execute **Node Fencing**:
- **Hardware PDU / IPMI Cut:** The Standby sends a hardware command to the Primary's intelligent power strip to physically disconnect its power.
- **Consensus Quorum:** The Standby must acquire a distributed lease from an independent 3-node consensus cluster (`etcd` or ZooKeeper). If it cannot obtain the lease, it aborts promotion.

---

## RTO vs RPO: Disaster Recovery Metrics

When an catastrophic failure occurs, disaster recovery capabilities are measured along two orthogonal axes:

```
               Last Data Backup              System Outage               Service Restored
                     │                            │                             │
                     ▼                            ▼                             ▼
─────────────────────┴────────────────────────────┴─────────────────────────────┴────────► Time
                     ◄─────────── RPO ───────────► ◄──────────── RTO ───────────►
                           (Data Lost)                    (Downtime Duration)
```

### 1. Recovery Point Objective (RPO)
**RPO** quantifies the maximum acceptable volume of **data loss** measured in units of time.
- If RPO = 1 hour, your system can tolerate losing the last 60 minutes of committed transactions.
- **Zero RPO:** Mandates synchronous replication. A transaction is not confirmed until written to at least two physically independent locations.

### 2. Recovery Time Objective (RTO)
**RTO** quantifies the maximum acceptable duration of **system downtime** before business operations must be fully restored.
- If RTO = 5 minutes, your automated failover, health probing, and DNS convergence must bring the standby system online within 300 seconds.

---

> [!NOTE]
> ### Teacher FAQ & Common Beginner Doubts
>
> **Q: How does DNS TTL affect failover time in Active-Passive systems?**  
> **Teacher's Answer:** If you rely on public DNS changes to fail over traffic from a dead Primary IP to a Secondary IP, your actual failover time is dictated by DNS caching, not your database! Even if you set DNS TTL to 60 seconds, many consumer ISPs (Comcast, mobile carriers) deliberately ignore low TTLs and cache records for hours. Therefore, never use public DNS switching for sub-minute RTO. Use Anycast BGP, Cloud Load Balancers, or Virtual IP failovers.
>
> **Q: Is Active-Active always superior to Active-Passive?**  
> **Teacher's Answer:** No! Active-Active architectures introduce extreme complexity in state synchronization. If both nodes accept writes to the same database table, you must implement distributed multi-master conflict resolution (CRDTs, two-phase commits, or vector clocks). For transactional relational data (financial ledgers), Active-Passive with automated synchronous replication is almost universally preferred because it eliminates data corruption risks.
