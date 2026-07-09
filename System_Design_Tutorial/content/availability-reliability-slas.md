# Availability, Reliability & SLAs

## Overview
What happens when your system goes down? You lose money, you lose trust, and engineers get paged at 3:00 AM. 

In System Design, we don't just hope the system stays up. We mathematically guarantee it through architecture. This masterclass covers the language of uptime (SLAs, 99.9%), the math behind redundant systems, and how to design failover mechanisms.

---

## SLI / SLO / SLA — indicator, objective, agreement

If you don't measure it, you can't guarantee it. The industry uses three acronyms to discuss uptime:

1. **SLI (Service Level Indicator):** The actual metric you are measuring. 
   - *Example:* "The percentage of HTTP GET requests that return a 200 OK status within 100ms."
2. **SLO (Service Level Objective):** Your internal goal for that metric.
   - *Example:* "We want 99.9% of requests to succeed."
3. **SLA (Service Level Agreement):** The legal contract with your customers. If you miss this, you owe them money.
   - *Example:* "If uptime drops below 99.9%, we will refund 10% of the customer's monthly bill."

> [!TIP]
> **Teacher's Secret:** Your SLO should always be stricter than your SLA! If you promise customers 99.9% (SLA), aim internally for 99.99% (SLO) so you have a buffer before you start losing money.

---

## 99.9% (8.76 hrs/yr) · 99.99% (52 min/yr) · 99.999% (5.25 min/yr)

When people talk about "High Availability," they measure it in "Nines." You must memorize how much downtime each "Nine" translates to.

| Nines | Percentage | Downtime per Year | Typical Use Case |
| :--- | :--- | :--- | :--- |
| **Two 9s** | 99% | 3.65 Days | Internal MVP, dev environments |
| **Three 9s** | 99.9% | 8.76 Hours | Standard SaaS product |
| **Four 9s** | 99.99% | 52.6 Minutes | Enterprise software, major APIs |
| **Five 9s** | 99.999% | 5.26 Minutes | Telecoms, aviation, heart monitors |

**The Reality Check:** Achieving Five 9s is incredibly expensive. It means you only have 5 minutes of downtime for the *entire year*. You cannot achieve this if a human has to manually intervene to fix a server. Failovers must be 100% automated.

---

## Availability in series: multiply (A1 × A2) — cascades

When you chain services together (Service A calls Service B), your overall availability **drops**.

Imagine a user logs in. The request hits the API Gateway (99.9%), which calls the Auth Service (99.9%), which queries the Database (99.9%).

**The Math (Series):**
`0.999 * 0.999 * 0.999 = 0.997` (99.7% Availability).

Because the request requires *all three* components to be alive, the system is less reliable than its weakest link. This is why microservice architectures can easily become brittle if they have deep, synchronous call chains.

---

## Availability in parallel: 1 - (1-A)^n — redundancy helps

If chaining components lowers availability, how do we increase it? We put components in **Parallel (Redundancy)**.

Instead of one database, you have two databases. The system only fails if **both** databases fail at the exact same time.

**The Math (Parallel):**
If a single server has 99% availability, its probability of failure is 1% (0.01).
If you have two servers, the probability they *both* fail is `0.01 * 0.01 = 0.0001` (0.01%).
Therefore, the availability is `1 - 0.0001 = 0.9999` (**99.99%**).

> [!NOTE]
> **Conclusion:** By taking two cheap, unreliable servers (99%) and placing them behind a Load Balancer, you magically created a highly available (99.99%) architecture. This is the entire foundation of distributed computing!

---

## Active-Active vs Active-Passive failover

When you have redundant systems (e.g., two Load Balancers or two Databases), how do they work together?

### Active-Passive (Warm Standby)
Only the Primary (Active) node handles traffic. The Secondary (Passive) node does absolutely nothing except receive data replications and wait for the Primary to die.
- **Pros:** Simple to reason about. No conflicts.
- **Cons:** You are paying for a server that does nothing. When the Primary dies, there is a delay (Recovery Time Objective - RTO) of maybe ~30-60 seconds while the Passive node takes over.

### Active-Active
Both nodes receive traffic simultaneously. If one dies, the other just takes on the extra load.
- **Pros:** Zero downtime failover. You get to utilize all the hardware you paid for.
- **Cons:** Very complex to keep data synchronized. You must ensure that neither node is running at >50% CPU, because if one dies, the survivor suddenly receives 100% of the traffic and might crash under the load (a cascading failure).
