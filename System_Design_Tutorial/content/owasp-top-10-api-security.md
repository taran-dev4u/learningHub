# OWASP Top 10 & API Security

Welcome to the masterclass on **OWASP Top 10 & API Security**. As a system architect, you cannot just design for the "happy path" where users act perfectly. You must assume that every input is malicious, every endpoint will be probed, and every unpatched vulnerability will be exploited.

The **OWASP Top 10** is the gold standard awareness document for web application security. In this lecture, we will dive deep into the most critical vulnerabilities, how they fundamentally work, and exactly how to architect your systems to prevent them.

---

## 1. Injection (SQL, NoSQL, OS)

Injection vulnerabilities occur when a system takes untrusted user input and sends it to an interpreter as part of a command or query.

**Analogy:** Imagine giving a delivery driver an address: "123 Main Street". But instead, you write: "123 Main Street, and while you are there, please empty the cash register and give it to me." If the driver blindly follows all instructions written on the paper, they will commit a robbery. The driver (interpreter) failed to distinguish between *data* (the address) and *code* (the command to rob).

### SQL Injection (SQLi)
If your backend does string concatenation for queries:
```sql
SELECT * FROM users WHERE username = 'admin' AND password = '" + user_input_password + "';
```
An attacker inputs `' OR '1'='1`. The resulting query becomes:
```sql
SELECT * FROM users WHERE username = 'admin' AND password = '' OR '1'='1';
```
Because `1=1` is always true, the attacker bypasses authentication completely.

### The Fix: Parameterized Queries (Prepared Statements)
Never use string concatenation. Use parameterized queries.
When you use a prepared statement, the database pre-compiles the SQL query structure *before* the data is inserted. When the malicious string `' OR '1'='1` arrives, the database treats it strictly as a literal string for the password field, not as executable SQL logic.

---

## 2. XSS (Cross-Site Scripting)

XSS occurs when an application includes untrusted data in a web page without proper validation or escaping. This allows attackers to execute malicious JavaScript in the victim's browser.

**Analogy:** Think of XSS like a Trojan Horse hidden in a legitimate package. You think you are opening a nice greeting card (a normal webpage), but inside the card is a tiny robot (malicious JavaScript) that steals your wallet (session cookies) and runs away.

### Types of XSS
- **Stored XSS:** The malicious payload is saved to the database (e.g., in a blog comment) and served to every user who views the page.
- **Reflected XSS:** The payload is embedded in a malicious URL and reflected off the web server (e.g., via a search parameter).

### The Fix
1. **Context-Aware Output Escaping:** Before rendering user input into HTML, escape special characters. Convert `<script>` to `&lt;script&gt;`. Modern frameworks like React and Angular do this automatically by default.
2. **Content Security Policy (CSP):** A powerful HTTP response header that restricts which scripts the browser is allowed to execute. For example, you can tell the browser: *"Only execute scripts loaded from my domain, and absolutely no inline scripts."*

---

## 3. CSRF (Cross-Site Request Forgery)

CSRF forces a logged-on victim's browser to send a forged HTTP request to a vulnerable web application.

**Analogy:** You leave your bank app open in one tab. In another tab, you click a sketchy link. The sketchy website contains a hidden form that POSTs to `bank.com/transfer?amount=10000&to=Attacker`. Because your browser automatically attaches your Bank Session Cookie to any request to `bank.com`, the bank thinks *you* made the transfer.

### The Fix
1. **Anti-CSRF Tokens:** The server generates a unique, cryptographically strong token for the user's session and embeds it in the UI (e.g., in a hidden form field). When a POST request is made, the server validates this token. A malicious third-party site cannot read this token due to the Same-Origin Policy.
2. **SameSite Cookie Attribute:** Set your session cookies to `SameSite=Lax` or `SameSite=Strict`. This instructs the browser: *"Do not send this cookie if the request originated from a different domain."* This practically eliminates CSRF.

---

## 4. SSRF (Server-Side Request Forgery)

In SSRF, the attacker abuses the server's functionality to read or update internal resources.

**The Scenario:** You build a feature where a user can input an image URL (e.g., `http://example.com/avatar.jpg`), and your backend server fetches it to save as their profile picture.

**The Exploit:** The attacker provides an internal URL instead:
- `http://localhost:8080/admin` (accessing internal admin panels).
- `http://169.254.169.254/latest/meta-data/` (The AWS/Cloud metadata service).

If the attacker hits the AWS metadata service via your server, they can extract the temporary IAM credentials assigned to the EC2 instance and take full control of your cloud infrastructure!

### The Fix
- Never trust user-provided URLs.
- Use an explicit **allowlist** of domains if possible.
- Deny requests to private IP ranges (e.g., `127.0.0.1`, `10.0.0.0/8`, `169.254.169.254`).
- Disable following redirects when fetching user-provided URLs.

---

## 5. Broken Authentication

Authentication systems are often built incorrectly, allowing attackers to compromise passwords, keys, or session tokens.

### Common Pitfalls:
- Allowing weak passwords (`Password123!`).
- Not rate-limiting login attempts (enabling brute-force and credential stuffing).
- Exposing Session IDs in the URL (`?session_id=12345`).
- Not enforcing Multi-Factor Authentication (MFA).

### The Fix
- Implement robust password policies. Use modern hashing algorithms like **Argon2** or **Bcrypt** with salt.
- Enforce MFA, preferably WebAuthn/FIDO2.
- Implement rate limiting and account lockouts after multiple failed attempts.

---

## 6. API Security Core Principles

When designing APIs, security must be implemented at multiple layers (Defense in Depth).

1. **Always Authenticate:** Never assume an endpoint is "internal only." If it is reachable over the network, it must require authentication.
2. **Validate Input:** Enforce strict schemas for incoming JSON payloads. If you expect an integer, reject strings. If you expect a max length of 100, reject 101.
3. **Log All Calls:** Maintain an unalterable audit log. You cannot detect a breach or investigate an incident if you have no logs of who called what API, when, and with what parameters (excluding PII/passwords).
4. **Rate Limit:** APIs are highly susceptible to Denial of Service (DoS) attacks and scraping. Use a distributed rate limiter (like a Token Bucket algorithm in Redis) to restrict requests per IP or per API Key.

> [!NOTE]
> **Teacher FAQ:** "Why do we rate limit authenticated users? Aren't they trusted?"
> Even trusted users can write a bad script that goes into an infinite loop and accidentally DDoS-es your system. Rate limiting protects your system's stability against both malice and sheer incompetence.

---

**Summary:** Assume all input is hostile. Use parameterized queries for SQL, CSP and escaping for XSS, SameSite cookies for CSRF, and block internal IPs for SSRF. Secure your APIs with strict rate limits, input validation, and comprehensive logging.
