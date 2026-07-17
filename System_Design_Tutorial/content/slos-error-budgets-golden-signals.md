# SLOs, Error Budgets & Golden Signals

Welcome to this masterclass on **Service Level Objectives (SLOs), Error Budgets, and Golden Signals**.

In system design, reliability is often considered the most important feature of any product. A system with a perfect UI, brilliant features, and lightning-fast algorithms is absolutely worthless if it's constantly crashing when users try to use it.

But here is the million-dollar realization: **100% reliability is the wrong target.**

Aiming for 100% reliability stalls innovation, costs an exorbitant amount of money, and frankly, users won't even notice the difference between 99.99% and 100% because their own internet connections and devices are inherently unreliable.

In this session, we'll explore how modern engineering organizations define, measure, and govern reliability using SLOs and Error Budgets.

## SLI, SLO, and SLA: The Definitions

These three acronyms are often thrown around interchangeably, but they have precise, distinct meanings. Let's break them down.

### SLI (Service Level Indicator)
An SLI is a **direct measurement** of a specific aspect of your service's behavior. It is a fact. It tells you what is happening right now.
- **Example:** "The percentage of HTTP GET requests to `/checkout` that return a 200 OK status code."
- **Example:** "The latency of the 95th percentile (p95) database read query over a 5-minute window."

An SLI is just a metric, usually expressed as a percentage of successful events out of total events.

### SLO (Service Level Objective)
An SLO is your **internal target** for the SLI. It is the line in the sand you draw to say, "If we stay above this line, our users are happy. If we drop below it, our users are feeling pain."
- **Example:** "99.9% of all HTTP GET requests to `/checkout` will succeed in a given month."
- **Example:** "The p95 latency for database reads will be under 200ms over a trailing 30-day window."

SLOs are internal goals. They drive engineering behavior.

### SLA (Service Level Agreement)
An SLA is a **legal and financial contract** with your customers. It says, "If we fail to meet our SLO, we will pay you money."
- **Example:** "If uptime drops below 99.9% in a calendar month, the customer will receive a 10% credit on their next bill."

Engineers rarely deal directly with SLAs—that's for lawyers and sales teams. Engineers build systems to protect the **SLO**, knowing that the SLA is the worst-case consequence. Usually, the internal SLO is stricter than the external SLA (e.g., SLO = 99.95%, SLA = 99.9%) to give a buffer.

| Concept | Definition | Analogy |
|---------|------------|---------|
| **SLI** | The measurement | Your current speed on the highway (65 mph). |
| **SLO** | The goal/target | Your personal goal to arrive in under 2 hours. |
| **SLA** | The contract | A guarantee to the client that if you arrive late, the delivery is free. |

---

## Error Budgets: The Currency of Reliability

If your SLO is 99.9% availability, that implies you are *allowed* to be unavailable for 0.1% of the time.
That 0.1% is your **Error Budget**.

In a 30-day month, 0.1% equates to roughly **43 minutes** of allowable downtime.

### Why Error Budgets Change Engineering Culture
Historically, there was a war between Development (who want to ship new features fast) and Operations (who want to block all changes to keep the system stable).

Error Budgets align these teams using math:
1. Every time a request fails, you spend some of your error budget.
2. If the budget is **positive** (e.g., you have 30 minutes left this month), developers are free to push code rapidly, experiment, and take risks.
3. If the budget is **exhausted** (you've used all 43 minutes), you pull the emergency brake. **All feature launches are frozen.** The entire team pivots to fixing technical debt, adding tests, and improving reliability until the rolling 30-day window restores the budget.

> [!IMPORTANT]
> The Error Budget is not just a nice idea; it requires organizational discipline. If an executive overrides the feature freeze when the budget is blown, the entire system collapses into meaninglessness.

---

## Golden Signals

We touched on this in observability, but let's reinforce it in the context of SLOs. When defining your SLIs, you shouldn't measure arbitrary things like "CPU utilization." You should measure the **Four Golden Signals**:

1. **Latency:** How long it takes to return a response.
2. **Traffic:** How much demand is on the system.
3. **Errors:** The rate of requests that fail.
4. **Saturation:** How "full" the system is.

When writing an SLO, you almost always write it against **Latency** or **Errors**.
- *Error SLO:* "99.99% of requests will not result in a 5xx error."
- *Latency SLO:* "99% of successful requests will return in under 300ms."

---

## Distributed Tracing in SLOs

How do you debug an exhausted error budget? If your overall system SLO is failing, you need to know *which* component is eating the budget.

**Distributed Tracing** (e.g., injecting a `trace_id` at the gateway and passing it to every downstream microservice) allows you to map the critical path.

If the API Gateway SLA is failing because latency is too high, tracing allows you to see:
- Gateway: 500ms
  - Auth Service: 10ms
  - User Service: 20ms
  - **Inventory DB Query: 450ms**

Tracing points the finger exactly at the bottleneck, allowing you to invest your engineering effort (and error budget recovery time) exactly where it's needed.

> [!NOTE]
> **Teacher FAQ & Misconceptions**
> **Q: What is the "Nines" calculation? I hear people talk about "Four Nines" or "Five Nines".**
> A: This refers to the number of 9s in the percentage, and it dictates exactly how much downtime you are allowed in a year. You must memorize these magnitudes:
> - **2 Nines (99%)**: ~3.6 days of downtime per year. (Startup MVP).
> - **3 Nines (99.9%)**: ~8.7 hours per year. (Standard commercial service).
> - **4 Nines (99.99%)**: ~52 minutes per year. (Enterprise critical).
> - **5 Nines (99.999%)**: ~5 minutes per year. (Telecom/Pacemakers. Incredibly expensive to achieve).
>
> **Q: If my system goes down for maintenance at midnight, does that hurt my SLO?**
> A: If you defined your SLO as "available 24/7", yes. If you defined it as "available excluding scheduled maintenance windows," no. It all depends on how you define the SLI!
