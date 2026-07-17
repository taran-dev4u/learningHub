# Threat Modeling & Abuse Cases

Welcome to the masterclass on **Threat Modeling and Abuse Cases**. Building a secure system is not about blindly applying firewalls and encryption; it is about systematically identifying where your system is vulnerable and designing specific mitigations.

In this lecture, we will cover the professional frameworks used by security architects to break down complex architectures and identify threats *before* a single line of code is written.

---

## 1. The STRIDE Framework

**STRIDE** is an acronym developed by Microsoft. It is a systematic way to categorize different types of security threats during the design phase of a system. When you look at an architecture diagram, you apply STRIDE to every component and data flow.

**Analogy:** Imagine designing a physical bank vault. You don't just say "make it secure." You systematically ask: Can someone use a fake ID (Spoofing)? Can they alter the ledger (Tampering)? Can they deny making a withdrawal (Repudiation)? Can someone read the ledger (Information Disclosure)? Can they block the door (Denial of Service)? Can a teller give themselves manager keys (Elevation of Privilege)?

Let's break down STRIDE in software:

| Threat Category | Property Violated | Definition & Example | Mitigation |
| :--- | :--- | :--- | :--- |
| **S**poofing | Authenticity | Pretending to be someone else. *Ex: An attacker forging a JWT to act as another user.* | Strong AuthN, MFA, Signed Tokens. |
| **T**ampering | Integrity | Modifying data in transit or at rest. *Ex: Altering a product's price in an API request.* | TLS (HTTPS), Digital Signatures, Checksums. |
| **R**epudiation | Non-repudiability | Claiming you didn't perform an action. *Ex: A user deletes a database table but denies doing it.* | Immutable Audit Logs, Signed Transactions. |
| **I**nformation Disclosure | Confidentiality | Exposing private data. *Ex: An error message revealing database structure or PII leak.* | Encryption (At Rest & In Transit), Strict Access Control. |
| **D**enial of Service | Availability | Exhausting resources so the system fails. *Ex: A Botnet flooding a login endpoint.* | Rate Limiting, WAF, Autoscaling, CDNs. |
| **E**levation of Privilege | Authorization | Gaining permissions you shouldn't have. *Ex: A normal user exploiting an API to gain Admin rights.* | Strict RBAC/ABAC, Principle of Least Privilege. |

> [!TIP]
> **System Design Interview Tip:** When discussing a system's security, explicitly mention STRIDE. Say, *"To address Information Disclosure, we will encrypt data at rest using AES-256, and to prevent Tampering in transit, we enforce TLS 1.3."* This shows maturity and structured thinking.

---

## 2. Attack Surface Mapping

The **Attack Surface** is the sum of all points (the "vectors") where an unauthorized user can try to enter data to or extract data from an environment.

### How to Map an Attack Surface
1. **Identify Entry Points:** APIs, Web Forms, WebSocket connections, File Upload endpoints.
2. **Identify Trust Boundaries:** The imaginary line where data moves from an untrusted zone (e.g., the public Internet) to a trusted zone (e.g., your internal VPC).
3. **Map Dependencies:** Third-party libraries, NPM packages, external SaaS APIs. (A vulnerability in a logging library, like Log4j, expands your attack surface exponentially).

**Analogy:** A medieval castle. The attack surface includes the front gate, the postern door, the walls, the windows, and the moat. If you dig a secret tunnel for supplies, you just increased your attack surface. Every new feature you build is a new window in the castle.

**Reduction Strategy:**
- Shut down unused endpoints.
- Require VPNs for internal admin tools.
- Implement a WAF (Web Application Firewall) to inspect traffic before it hits the application logic.

---

## 3. Data Classification & Encryption Boundaries

Not all data is created equal. A system architect must classify data to apply the appropriate level of security. Protecting a public blog post with the same rigour as a credit card number is a waste of money and compute resources.

### Data Classification Tiers
1. **Public:** No harm if exposed. (e.g., Product catalog).
2. **Internal:** Mild harm. (e.g., Company org chart).
3. **Confidential:** Severe harm. (e.g., Financial records, Source Code).
4. **Restricted/PII:** Regulatory disaster if exposed. (e.g., Social Security Numbers, Passwords, Health Records).

### Encryption Boundaries
Once classified, you define where encryption begins and ends.
- **Encryption in Transit:** Data moving over a network. Handled by TLS (HTTPS).
- **Encryption at Rest:** Data sitting on a physical disk (e.g., AWS EBS volumes, S3 buckets). Handled by algorithms like AES-256.
- **Encryption in Use (Advanced):** Protecting data while it is in RAM, often using Secure Enclaves (e.g., AWS Nitro Enclaves) to process highly sensitive keys without exposing them to the OS.

> [!WARNING]
> **Common Beginner Mistake:** Assuming "Encryption at Rest" solves all database leaks. If an attacker gains SQL access via an SQL Injection vulnerability, the database will happily decrypt the data and serve it to them. Encryption at rest protects against someone stealing the *physical hard drives*, not application-layer vulnerabilities.

---

## 4. Abuse & Rate-Limit Threat Cases

Security isn't just about preventing hacks; it's about preventing **abuse of legitimate business logic**.

### The Scenarios

**1. Credential Stuffing & Account Takeover**
- *Threat:* Attackers take billions of leaked username/password pairs from other sites and automate login attempts on your site.
- *Mitigation:* Rate limit by IP. Rate limit by Username. Implement CAPTCHAs after 3 failed attempts. Force password resets if a credential matches a known breached database (e.g., HaveIBeenPwned).

**2. SMS Pumping (Toll Fraud)**
- *Threat:* You build a "Send OTP via SMS" feature. An attacker uses bots to trigger millions of SMS messages to premium-rate phone numbers they own, bankrupting your Twilio account while they collect the revenue.
- *Mitigation:* Extremely aggressive rate limiting on the SMS endpoint. Require a CAPTCHA before sending SMS. Geo-block SMS to high-risk countries if your business doesn't operate there.

**3. Scraping & Data Extraction**
- *Threat:* Competitors use bots to scrape your entire pricing catalog or user profiles.
- *Mitigation:* Implement behavioral rate limiting (e.g., if a user views 100 profiles in 60 seconds, block them). Serve data via APIs that require tokens, and use a CDN (like Cloudflare) with Bot Management to challenge headless browsers.

**4. Resource Exhaustion (Application DDoS)**
- *Threat:* An attacker doesn't try to hack you; they just try to make your AWS bill explode. They find an expensive API endpoint (e.g., `/generate-pdf` or `/search?query=wildcard`) and call it 10,000 times a second.
- *Mitigation:* Separate the processing of heavy tasks to an asynchronous queue (Message Queue + Worker Nodes). Limit the number of concurrent heavy requests a single user can enqueue.

---

**Summary:** System security requires structural thinking. Use STRIDE to find architectural flaws. Minimize your attack surface by exposing only what is necessary. Classify your data to apply encryption where it matters, and always design mitigations against the abuse of your business logic, not just technical exploits.
