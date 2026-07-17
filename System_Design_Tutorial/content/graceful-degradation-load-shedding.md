# Graceful Degradation & Load Shedding: The Masterclass

Welcome, architects. When a system is pushed beyond its limits, it will break. However, *how* it breaks is entirely up to you. A poorly designed system fails catastrophically, taking down everything and presenting users with endless loading screens or ugly 500 server errors. A well-designed system bends without breaking, shedding non-essential weight to ensure core functionalities survive.

In this masterclass, we will cover the advanced survival tactics of distributed systems: **Graceful Degradation** and **Load Shedding**. We will explore how to use fallbacks, kill switches, and priority queues to keep your system afloat during a Category 5 traffic hurricane.

---

## 1. Graceful Degradation: The Art of Failing Elegantly

### The "Why": User Experience Over Perfection
Imagine you are browsing Netflix. The homepage usually shows personalized recommendations driven by a heavy, complex machine learning backend. Now, imagine that ML service goes down.

A fragile system would crash the entire homepage, preventing you from watching anything. A system built with **Graceful Degradation** realizes the ML service is down, swallows the error, and instead shows you a hardcoded list of "Top 10 Trending Movies." The user experience is slightly degraded (not personalized), but the core functionality (finding a movie to watch) remains perfectly intact.

### Fallback Responses
When an upstream service or database fails, your system should have a pre-planned **fallback**.

There are three main types of fallbacks:
1. **Stale Cache:** If the live database is down, return the data you cached 5 minutes ago. Stale data is almost always better than an error.
2. **Default/Hardcoded Values:** If you can't fetch a user's custom avatar, serve a generic placeholder silhouette.
3. **Empty Responses:** If a secondary feature (like a "Suggested Friends" sidebar) fails, just render the page without that sidebar.

> [!TIP]
> Always ask yourself during system design: *"If this microservice completely explodes, what should the user see?"* If the answer is an error page, you have a hard dependency that needs a fallback.

---

## 2. Feature Flags & Kill Switches: Jettisoning the Cargo

When a ship is sinking, the crew throws heavy, non-essential cargo overboard to stay afloat.

In software, certain features are incredibly expensive to compute. For example, a heavy search aggregation, a complex recommendation engine, or generating PDF reports. Under normal conditions, these features are great. Under extreme load, they are the anchors dragging your database to the bottom of the ocean.

### Feature Flags
Feature flags are configuration toggles that allow you to turn parts of your application on or off dynamically, *without deploying new code*.

### Kill Switches
A kill switch is a specific type of feature flag designed for emergencies. If your monitoring dashboard shows CPU utilization hitting 95%, you flip the kill switch for the expensive "PDF Generation" feature.
Instantly, the UI hides the "Download PDF" button, and the backend stops accepting those requests. CPU utilization drops to 60%. The site stays online.

| Strategy | Speed of execution | Primary Use Case |
| :--- | :--- | :--- |
| **Code Rollback** | Slow (minutes to hours) | Reverting a bug that was just deployed. |
| **Kill Switch** | Instant (milliseconds) | Shedding expensive system load instantly during traffic spikes. |

---

## 3. Load Shedding: The Last Line of Defense

If rate limiting is the bouncer at the club door, **Load Shedding** is the bouncer tossing people out when a fire starts.

Rate limiting generally applies evenly to all users based on a quota. Load shedding is a survival mechanism that kicks in when the server itself realizes it is dying.

### How Load Shedding Works
When a server’s internal metrics (e.g., CPU, memory, active threads, request queue depth) cross a critical threshold, it stops accepting new work entirely, returning an immediate HTTP 503 (Service Unavailable).

1. **CPU hits 90%.**
2. The load shedder activates.
3. It intercepts all incoming requests at the very edge of the application framework.
4. It instantly returns a 503 before the request even reaches the business logic or database.
5. CPU drops. Once it stabilizes below 80%, the load shedder deactivates.

### Rejecting Low-Priority Requests First
Not all requests are created equal. A "Process Payment" request is infinitely more important than a "Record Analytics Click" request.

Advanced load shedding inspects the headers or URL of a request. If the system is under stress, it will shed the analytics requests *first*. If the system is still dying, it will shed read requests. It will only shed payment requests if the server is literally seconds away from a hard crash.

> [!WARNING]
> Do not attempt to process a request and *then* decide to shed load. Load shedding must happen in microseconds. If you parse the JSON body before rejecting the request, you've already wasted the CPU cycles you were trying to save.

---

## 4. Priority Queues: Protecting Critical Work

In asynchronous systems, work is often dropped into a message queue (like RabbitMQ or SQS) to be processed by background workers.

If a flood of low-priority events fills up the queue, your background workers will spend all day processing garbage while critical tasks wait for hours.

### The Solution: Multiple Queues
Instead of one massive queue, you implement **Priority Queues**.

1. **Queue A (High Priority):** Payment processing, password resets.
2. **Queue B (Standard Priority):** Sending welcome emails.
3. **Queue C (Low Priority):** Image resizing, analytics aggregation.

Your worker nodes are configured to *always* pull from Queue A first. They only look at Queue B if Queue A is empty.

Under extreme load, Queue C might back up and delay image resizing by 6 hours. That is a graceful degradation. But password resets and payments will continue to process instantly, completely unaffected by the flood.

---

## Teacher FAQ & Common Beginner Mistakes

> [!NOTE]
> **Question:** Isn't returning stale data via a fallback dangerous? What if they see the wrong bank balance?
> **Answer:** Context is everything! You never use stale cache fallbacks for transactional data (money, inventory). Fallbacks are for read-heavy, eventually consistent data (comments, recommendations, profile pictures, social feeds).

> [!NOTE]
> **Question:** How do I know when to trigger Load Shedding?
> **Answer:** The most reliable metric is usually **Concurrency** (number of active requests in flight) or **Queue Depth**. CPU can be a lagging indicator. If your server can normally handle 500 concurrent requests, and you suddenly see 2,000, start shedding immediately.

> [!NOTE]
> **Misconception:** "Load Shedding and Rate Limiting are the same thing."
> **Correction:** Rate Limiting protects the system from a *specific greedy user* exceeding their quota. Load Shedding protects the system from *itself* when total global capacity is breached, regardless of who is making the request.
