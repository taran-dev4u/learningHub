# Testing, Chaos & Safe Deployment

Welcome to the masterclass on **Testing, Chaos Engineering, and Safe Deployment**.

You've designed a brilliant distributed system on the whiteboard. You've written the code. Now comes the scariest part of software engineering: putting it into production where actual users will touch it.

In a distributed environment, you cannot just click "deploy" and hope for the best. Systems fail in unpredictable, non-deterministic ways. Network packets drop, databases stall, disks fill up.

In this session, we will cover how we test systems under extreme duress, how we intentionally break them in production to build resilience, and how we deploy new code so that if it is broken, almost nobody notices.

## 1. Load, Stress, and Soak Testing

Writing unit tests verifies your logic, but it tells you nothing about how your system behaves when 10,000 users log in simultaneously. For that, we need performance testing.

### Load Testing
Load testing answers the question: **"Can the system handle the expected peak traffic?"**
If your Black Friday projection is 5,000 requests per second (RPS), you run a load test at 5,000 RPS. You verify that latency stays within your SLO and that no errors are thrown. It validates your architecture against known expectations.

### Stress Testing
Stress testing answers the question: **"What happens when the system is pushed past its limits?"**
Instead of stopping at 5,000 RPS, you ramp the traffic to 10,000, 20,000, 50,000 RPS until the system physically breaks.
- **Why it matters:** You want to see *how* it dies. Does it degrade gracefully by dropping excess requests (Load Shedding)? Or does the database lock up completely, causing a cascading failure that takes hours to recover from? Stress testing finds the weakest link in your architecture.

### Soak Testing
Soak testing answers the question: **"Can the system run stably for a long period of time?"**
Instead of a massive spike, you run a moderate, steady load (e.g., 1,000 RPS) for 48 hours straight.
- **Why it matters:** Soak tests are designed to catch **memory leaks**, unclosed database connections, and disk-space exhaustion. A system might survive a 10-minute stress test perfectly, but crash on day 3 because a temporary file directory wasn't being purged.

| Test Type | Goal | Duration | Traffic Level |
|-----------|------|----------|---------------|
| **Load** | Verify expected capacity | Short (hours) | Expected Peak |
| **Stress**| Find the breaking point | Short (minutes/hours)| Beyond limit (until death) |
| **Soak** | Catch leaks over time | Long (days) | Moderate/Normal |

---

## 2. Chaos Engineering

Originally pioneered by Netflix with their famous tool "Chaos Monkey", **Chaos Engineering** is the discipline of intentionally injecting failures into a production system to prove that the system can survive them.

In a distributed system, you must assume that nodes will die. If you wait for a natural disaster to test your failover mechanisms, you will fail.

### How it Works
You define a steady state (e.g., "Video playback success rate is 99.9%"). Then, you introduce a variable:
- Terminate a random virtual machine.
- Inject 500ms of latency into the network between the API and the Database.
- Simulate a full AWS availability zone going offline.

You then observe if the steady state holds. If the video playback rate drops, you halt the experiment, fix the redundancy issue, and try again.

### The Analogy: Fire Drills
Chaos engineering is exactly like a fire drill in a school. You pull the alarm when there is no fire, intentionally interrupting the day, to ensure that when a real fire happens, everyone knows the exact path to safety and panic is minimized.

---

## 3. CI/CD Pipeline Design

Continuous Integration and Continuous Deployment (CI/CD) is the automated factory line for your code.

### Continuous Integration (CI)
When a developer pushes code to the repository, the CI server (like Jenkins, GitHub Actions, or GitLab CI) immediately takes over.
1. It compiles the code.
2. It runs unit tests and integration tests.
3. It runs static analysis and security scans (linting, vulnerability checks).
If any step fails, the build turns red, and the code cannot be merged. This ensures the main branch is always in a deployable state.

### Continuous Deployment (CD)
Once the code passes CI, CD takes the compiled artifact (like a Docker image) and automatically pushes it through various environments (Dev -> Staging -> Production).
The goal of CD is to remove human error from deployments and make shipping code a boring, push-button event.

---

## 4. Canary and Blue-Green Deployments

If you have a bug in your code that passed all tests, and you deploy it to 100% of your servers at once, 100% of your users will experience an outage. We mitigate this risk using advanced deployment strategies.

### Blue-Green Deployment
In a Blue-Green deployment, you maintain two identical production environments.
- **Blue** is currently live and taking 100% of user traffic.
- **Green** is idle.
When you deploy a new version, you deploy it completely to the **Green** environment. You run internal tests against Green. Once satisfied, you flip the router/load balancer to instantly send 100% of traffic to Green. Blue becomes idle.
- **Pros:** Zero-downtime deployment. Instant rollback (just flip the router back to Blue if Green fails).
- **Cons:** Very expensive, as you have to pay for 2x the infrastructure.

### Canary Deployment
Named after the "canary in the coal mine," this strategy rolls out the new code to a very small subset of users first.
1. You deploy the new version to just **1%** of your servers.
2. The load balancer sends 1% of live user traffic to the new version.
3. You monitor the Golden Signals (Latency, Errors) for that 1% over a period (e.g., 30 minutes).
4. If errors spike, the load balancer automatically rolls back the 1%. Only 1% of users had a bad experience.
5. If it's stable, you slowly ramp up: 10%, 25%, 50%, 100%.

- **Pros:** Highly limits the blast radius of a bad deployment. Cheaper than Blue-Green.
- **Cons:** Slows down the deployment process.

> [!CAUTION]
> **Teacher FAQ: The Database Schema Problem**
> **Q: How do you do a Blue-Green or Canary deployment if the new code requires a database schema change (like dropping a column)?**
> A: This is the hardest problem in deployments. You cannot make breaking database changes in a single step, because the old code (which is still running on the other servers) will crash.
> You must use the **Expand and Contract pattern**:
> 1. **Phase 1 (Expand):** Add the new column. Deploy code that writes to both the old and new columns, but reads from the old.
> 2. **Phase 2 (Migrate):** Run a script to backfill data into the new column.
> 3. **Phase 3 (Switch):** Deploy code that reads from the new column.
> 4. **Phase 4 (Contract):** Deploy code that stops writing to the old column, and finally drop the old column from the DB.
> Never drop a column while old code is still capable of running!
