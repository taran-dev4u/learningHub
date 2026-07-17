# Metrics, Dashboards & Alerting

Welcome to this masterclass on **Metrics, Dashboards, and Alerting**. In modern distributed systems, you are operating essentially blind unless you have a robust observability pipeline. Imagine trying to drive a car on a highway with a blacked-out windshield and no dashboard to tell you your speed or fuel level. You might make it a few feet, but a crash is inevitable.

In this session, we are going to dive deep into exactly *why* we collect metrics, *what* specific metrics matter (spoiler: not all of them do), and *how* we build systems that proactively tell us when things are going wrong, without waking us up at 3 AM for issues that can wait.

## 4 Golden Signals: Latency, Traffic, Errors, Saturation

Google SREs coined the concept of the **Four Golden Signals**. If you can only measure four things in your user-facing system, these are the four you must measure. Why? Because they directly reflect the *user experience* and the *system's physical limits*.

### 1. Latency
**Latency** is the time it takes to service a request.
But here is a critical distinction: you must differentiate between the latency of *successful* requests and *failed* requests. If an error is returned instantly, it might artificially lower your overall average latency, tricking you into thinking the system is fast when it's actually just failing quickly.

- **Why it matters:** Users hate slow systems. A 500ms delay can drop e-commerce conversion rates by 20%.
- **Math/Metrics Rule:** Never rely solely on average (mean) latency. Averages hide outliers. You must measure percentiles: **p50 (median), p90, p95, and p99**. If your p99 latency is 2 seconds, it means 1 out of every 100 requests takes 2 seconds or longer.

### 2. Traffic
**Traffic** is a measure of how much demand is being placed on your system.
For a web API, this is usually **HTTP requests per second**. For a database, it's **transactions per second (TPS)**. For an audio streaming service, it might be **concurrent network I/O streams**.

- **Why it matters:** Traffic gives you the baseline context. If latency spikes, the first question is always: "Did traffic spike too?"

### 3. Errors
**Errors** represent the rate of requests that fail.
This includes explicit failures (e.g., HTTP 500), implicit failures (an HTTP 200 success response that contains a malformed JSON body), and policy failures (e.g., returning a response after a 3-second timeout when the SLA demands 1 second).

- **Why it matters:** Errors directly break the user journey.

### 4. Saturation
**Saturation** tells you how "full" your system is. It is a measure of the most constrained resource (e.g., CPU, memory, I/O, database connections).
- **Why it matters:** Many systems degrade in performance *long before* they reach 100% utilization. A database might start heavily queuing requests when its CPU hits 75%. Saturation helps you predict imminent failures before they manifest as errors or latency spikes.

> [!NOTE]
> **Teacher FAQ & Misconceptions**
> **Q: Why don't we just alert on CPU usage directly instead of latency?**
> A: This is a classic beginner mistake. High CPU usage is a symptom, not a user-facing problem. If CPU is at 95% but latency is totally fine and no errors are occurring, the user doesn't care. Your alerting should prioritize the user's pain (latency, errors). High CPU is something you look at on a dashboard *during* an investigation, but it shouldn't wake you up at night unless it threatens imminent failure (Saturation).

---

## The RED Method: Rate, Errors, Duration

While the Four Golden Signals apply broadly to whole systems, the **RED Method** is specifically tailored for **microservices architecture**. Coined by Tom Wilkie, RED stands for:

- **Rate:** The number of requests your service is serving per second. (Equivalent to Traffic).
- **Errors:** The number of failed requests per second.
- **Duration:** The time each request takes. (Equivalent to Latency).

### Why the RED Method?
In a microservice ecosystem with 500 distinct services, you need a standardized way to view the health of *any* service instantly. By forcing every single microservice to emit Rate, Errors, and Duration metrics, you can build unified dashboards. You don't need to know the inner workings of the `InventoryService` or the `PaymentService` to know they are broken—if `Errors` spike or `Duration` elongates, it's broken.

| Concept | Description | Analogy |
|---------|-------------|---------|
| **Rate** | Requests per second | Customers entering a coffee shop per minute. |
| **Errors** | Failure rate | Customers given the wrong coffee or walking out angry. |
| **Duration** | Latency/Time taken | How long a customer waits from order to receiving coffee. |

> [!TIP]
> Use the RED method for **Services** (things that take requests) and the USE method for **Resources** (things that do the processing).

---

## The USE Method: Utilization, Saturation, Errors

Created by Brendan Gregg, the **USE Method** is the standard approach for analyzing the performance of infrastructure and hardware resources (Nodes, Disks, Network interfaces).

For every resource, check:
1. **Utilization:** The average time the resource was busy servicing work (e.g., CPU usage is at 60%).
2. **Saturation:** The degree to which the resource has extra work which it can't service, often measured by queue length. (e.g., 5 threads waiting for a CPU core).
3. **Errors:** The count of error events (e.g., network interface dropping packets, disk read errors).

### Utilization vs. Saturation: The Highway Analogy
Think of a highway.
- **Utilization** is how much of the physical road is covered by cars. If it's 60% full, cars can still maneuver.
- **Saturation** is the traffic jam at the on-ramp because the highway is physically too full to accept more cars.

In computer systems, once a resource is saturated, latency increases exponentially as requests sit in queues waiting for their turn.

---

## Prometheus Scrape Model (Pull vs. Push)

When building an observability pipeline, a massive architectural decision is how metrics get from your servers to your monitoring database. There are two models: **Push** (services send data to a central server) and **Pull** (the central server asks services for data).

**Prometheus**, the industry standard for metrics, uses a **Pull model** (also known as a scrape model).

### How it Works
1. Your application exposes an HTTP endpoint, typically `/metrics`.
2. When this endpoint is hit, it returns the current state of all counters, gauges, and histograms in plain text.
3. The Prometheus server is configured with a list of IP addresses (targets).
4. Every `N` seconds (e.g., 15s), Prometheus makes an HTTP GET request to each target's `/metrics` endpoint, scraping the data and storing it in its Time Series Database (TSDB).

```text
# Example Prometheus /metrics output format
http_requests_total{method="GET", endpoint="/api/users", status="200"} 10452
http_requests_total{method="POST", endpoint="/api/users", status="500"} 13
cpu_usage_percent 42.5
```

### Why Pull over Push?
- **Simplified Architecture:** The microservices don't need to know where the metrics server is. They just blindly expose `/metrics`. The Prometheus server handles service discovery.
- **Overload Protection:** If the monitoring system is overwhelmed, a Push model results in services spamming the server, potentially causing a cascading failure or filling up network bandwidth. With a Pull model, if Prometheus is overloaded, it just scrapes slower. The applications are unharmed.
- **Easy Debugging:** You can manually `curl http://myservice:8080/metrics` from your laptop to verify metrics are working. You can't easily do that with a push model.

> [!WARNING]
> **Common Beginner Mistake**
> Using highly unbounded cardinality in Prometheus labels. If you label your `http_requests_total` with a `user_id` label, you will create a unique time-series for every single user in your database. If you have 10 million users, you just created 10 million time-series, which will instantly crash your Prometheus server with an Out-Of-Memory (OOM) error. Keep labels limited to finite, small sets (like HTTP status codes or endpoints).

---

## Alertmanager: Routing Alerts to PagerDuty, Slack, Email

Prometheus evaluates rules against its metric data (e.g., "Is the p99 latency > 1s for 5 minutes?"). When a rule evaluates to true, it generates an alert. But Prometheus doesn't send emails. It sends the alert to an ecosystem tool called **Alertmanager**.

Alertmanager's job is **Deduplication, Grouping, and Routing**.

### The Problem it Solves
Imagine a core database goes down.
Suddenly, 50 different microservices that depend on that database start failing. Your monitoring system fires 50 distinct alerts.
Without Alertmanager, your on-call engineer's phone would ring 50 times in 2 minutes. They would panic, overwhelmed by the noise.

### How Alertmanager Works
1. **Grouping:** It groups similar alerts. Instead of 50 Slack messages for 50 failing services, it sends *one* Slack message saying: "50 services are failing; common label: `datacenter=us-east-1`".
2. **Inhibition:** If Alertmanager receives a "Database Down" alert, it can systematically suppress all "Service X is failing" alerts, because it knows the database is the root cause.
3. **Routing:** It routes alerts based on severity and team ownership.
   - Severity: `CRITICAL` -> PagerDuty (wakes someone up).
   - Severity: `WARNING` -> Slack channel (engineer looks at it in the morning).
   - Label: `team=payments` -> Routes to the Payments Team's PagerDuty rotation.

> [!NOTE]
> **Teacher FAQ: The Reality of On-Call**
> **Q: Should we alert on everything to be safe?**
> A: Absolutely not. The fastest way to destroy engineering morale is "Alert Fatigue." If an alert does not require a human to take immediate action, it should not page. If a disk is at 70% capacity, send a Slack message. If a disk is at 99% capacity and will crash the database in 10 minutes, page them.

By mastering these concepts, you transition from building code that just runs on your laptop to building robust, observable platforms that teams can operate safely at global scale.
