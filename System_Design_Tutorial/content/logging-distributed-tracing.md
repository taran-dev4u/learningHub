# Logging & Distributed Tracing

Welcome to the masterclass on **Logging & Distributed Tracing**. While metrics (dashboards, 4 Golden Signals) give you the *symptoms* of a problem ("We have a spike in 500s!"), logging and distributed tracing give you the *cause* ("Line 42 of the Payment Service threw a NullPointerException because the user's billing ID was missing").

In a monolith, debugging is easy: you open `app.log`, grep for the error, and you're done. In a microservices architecture, a single user request might touch 15 different services across 3 data centers. Without distributed tracing and structured logging, finding out exactly where that request failed is like finding a needle in 15 different haystacks, blindfolded.

Let's dive into how we solve this.

## Structured Logs: JSON over Plain Text

Historically, logs were just strings of text.

`[INFO] 2023-10-25 14:00:22 - User JohnDoe purchased item 456 in 240ms`

This is fine for a human reading a terminal, but it is a nightmare for a machine trying to parse, index, and query billions of logs. How do you query for all purchases that took longer than 200ms? You would need to write a complex regex to extract the time value from the string.

### The Solution: Structured Logging
Modern systems emit logs as **JSON objects** (Structured Logs).

```json
{
  "timestamp": "2023-10-25T14:00:22Z",
  "level": "INFO",
  "user_id": "JohnDoe",
  "item_id": 456,
  "action": "purchase",
  "latency_ms": 240,
  "trace_id": "abc123xyz"
}
```

- **Why it matters:** Log aggregators (like Elasticsearch, Splunk, or Datadog) can ingest JSON directly. You can instantly run a query like `SELECT * FROM logs WHERE action='purchase' AND latency_ms > 200`. No regex required.
- **Best Practice:** Every single log line should contain contextual keys: `trace_id`, `user_id`, `service_name`, and `latency_ms`.

> [!NOTE]
> **Common Beginner Mistake**
> Logging sensitive data (PII or passwords) in plain text logs. Logs are often replicated across multiple monitoring systems and visible to many engineers. **Never** log passwords, credit card numbers, or raw social security numbers. Mask them or hash them.

---

## Distributed Tracing & The `trace_id`

When a user clicks "Checkout", the UI calls the API Gateway, which calls the Order Service, which calls the Payment Service and the Inventory Service.

If the user gets a generic "Checkout Failed" error, how do you know which service dropped the ball?

This is where **Distributed Tracing** (popularized by Google's Dapper paper, and tools like Jaeger or Zipkin) comes in.

### How it Works
1. **Creation:** When a request enters the very first service (e.g., the API Gateway), the gateway generates a unique ID, called a **`trace_id`** (e.g., `8f8a2c1b`).
2. **Propagation:** The gateway passes this `trace_id` in the HTTP headers to the Order Service. The Order Service passes it to Payment and Inventory.
3. **Logging:** Every service includes this `trace_id` in every single structured log it emits.
4. **Spans:** Each step of the journey is recorded as a **Span** (which has a start time, end time, and the parent `trace_id`).

When an error occurs, you simply take the `trace_id` returned to the user, paste it into your tracing tool (like Jaeger), and you get a beautiful visual waterfall chart showing exactly how long each hop took and exactly which hop threw the 500 error.

### The Analogy: The FedEx Tracking Number
Think of a `trace_id` like a FedEx Tracking Number. Your package (the request) moves from a truck to a facility, to an airplane, to another truck. At every step, the worker scans the exact same tracking number. When the package gets lost, FedEx doesn't just guess where it is; they look up the tracking number and see exactly which facility scanned it last.

---

## W3C Trace Context Standard

For years, every observability vendor had their own proprietary way of passing the `trace_id` in HTTP headers. Zipkin used `X-B3-TraceId`, Datadog used `x-datadog-trace-id`, New Relic used something else.

This meant if you had a system where Service A used Datadog and Service B used Zipkin, the trace would break.

**W3C Trace Context** is the industry standard that solved this. It dictates exactly how trace information must be formatted in HTTP headers.

It defines two headers:
1. `traceparent`: Contains the globally unique `trace_id`, the `span_id` (the specific hop), and sampling flags. Example: `00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01`
2. `tracestate`: Vendor-specific data.

- **Why it matters:** By adhering to this standard, you can swap observability tools without changing your code, and requests can traverse boundaries (e.g., from your backend to a third-party payment provider) without losing the trace context.

---

## CloudTrail / Activity Logs

While standard application logs are for developers debugging code, **Audit Logs** (like AWS CloudTrail or an internal "Activity Log") are for security and compliance.

### The Difference
- **App Log:** `[INFO] Cache miss for item 123, falling back to DB.` (Used by engineering to debug performance).
- **Audit Log:** `[SECURITY] User admin_bob permanently deleted the production database at 3:00 AM from IP 192.168.1.50.` (Used by compliance to figure out who destroyed the company).

An Audit Trail must answer four questions definitively:
1. **Who** did it? (Identity/Role)
2. **What** did they do? (Action/API call)
3. **When** did they do it? (Timestamp)
4. **Where** did they do it from? (IP Address / Device)

Audit logs must be **immutable**. If a hacker breaches your system, the first thing they will try to do is delete the logs covering their tracks. Audit logs are often streamed directly to highly secured, write-once-read-many (WORM) storage buckets where even root administrators cannot delete them.

---

## Alert Fatigue

This is the psychological side of system design, but it is just as critical as the code.

**Alert Fatigue** occurs when an on-call engineer receives so many non-critical alerts that they become desensitized and start ignoring them. Eventually, a *critical* alert fires, the engineer assumes it's just more noise, goes back to sleep, and the company loses a million dollars.

### The Rules of Alerting
1. **Every Alert Must Be Actionable:** If an alert wakes me up, there must be a specific action I can take to fix it. If the alert is "CPU spiked for 2 seconds and recovered," I can't do anything about that at 3 AM. It should not be an alert.
2. **Symptom-Based Alerting:** Alert on symptoms that affect users (e.g., "Checkout latency is > 5s"). Do not alert on causes (e.g., "Database queue length > 10"). The user doesn't care about the queue length if checkout is still fast.
3. **Delete Noisy Alerts:** If an alert fires 10 times a week and the on-call engineer simply clicks "Resolve" without taking action, **delete the alert**. It is negative value.

> [!TIP]
> **Teacher FAQ & Misconceptions**
> **Q: Should we trace 100% of our requests?**
> A: No, that's too expensive. For high-throughput systems, generating a trace for every single request will cost more in storage than the actual database. You should use **Sampling**. Typically, you sample 1% to 10% of requests for tracing. However, you often employ **Tail-based Sampling**, where the system keeps the trace in memory, and only writes it to disk if the request ended in an error or took unusually long. This ensures you always have traces for the broken requests, but throw away the boring, successful ones.
