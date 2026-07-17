# Authentication & Authorization

Welcome to the masterclass on **Authentication & Authorization**. In system design, you can build the most scalable, highly available system in the world, but if your security is fundamentally flawed, the system is completely compromised.

As a system architect, you must deeply understand the difference between *Authentication* (AuthN - "Who are you?") and *Authorization* (AuthZ - "What are you allowed to do?"). In this lecture, we are going to dive deep into the most critical concepts you must master for designing secure systems.

---

## 1. Sessions (Server-Side State) vs JWT (Stateless Signed Tokens)

When a user logs in, how does the server remember them on subsequent requests? HTTP is naturally a stateless protocol, meaning it forgets who you are the moment a request is completed.

### The Session-Based Approach (Stateful)
In the traditional session-based approach, when a user logs in, the server generates a unique string (the `Session ID`), stores it in a database or an in-memory cache like Redis, and sends it back to the client as a Cookie.

**Analogy:** Think of a Session ID like a VIP guest list at a nightclub. When you arrive, the bouncer checks your ID, finds your name on his clipboard, and lets you in. Every time you go to the bar, they have to check the clipboard again.

**The "Why":** We store this state on the server so that we have absolute control. If a user's account is compromised, we simply delete their Session ID from our Redis cache, and they are instantly logged out.

**The Problem:** Scaling. If you have 10 million active users, you need to store 10 million session records. Furthermore, if you have 100 backend servers behind a Load Balancer, every server needs access to the centralized session store (e.g., a Redis cluster).

### The JWT Approach (Stateless)
A **JSON Web Token (JWT)** flips this paradigm. Instead of storing a record on the server, the server cryptographically *signs* a JSON payload containing the user's details (like `user_id` and `role`) and sends this token to the client. The client sends it back on every request.

**Analogy:** Think of a JWT like a stamped wristband at a music festival. The security guard at the gate checks your ticket and gives you a wristband with a holographic seal. For the rest of the day, the bartender doesn't need to check a master list; they just look at your wristband and verify the holographic seal (the cryptographic signature).

**The "Why":** This is highly scalable. The server doesn't need to look up a database on every request. It merely verifies the cryptographic signature (using a secret key or a public/private key pair) to trust the contents of the token.

### Trade-offs: Sessions vs JWT

| Feature | Session IDs (Stateful) | JWT (Stateless) |
| :--- | :--- | :--- |
| **Where is state kept?** | Server (DB/Redis) | Client (Browser/App) |
| **Revocability** | Immediate. Just delete from DB. | Hard. Token is valid until it expires. |
| **Scalability** | Requires central cache (bottleneck at massive scale). | Highly scalable. CPU-bound (signature verification). |
| **Payload Size** | Tiny (just a random string, e.g., 32 bytes). | Large (Base64 encoded JSON + Signature). |
| **Best Used For** | Web apps needing tight security & instant logout. | Microservices, Server-to-Server, short-lived API access. |

> [!WARNING]
> **Common Beginner Mistake:** Putting sensitive data (like passwords or PII) inside a JWT payload. JWTs are encoded in Base64, **not encrypted**. Anyone who intercepts the token can read the JSON payload. They just can't tamper with it without invalidating the signature.

---

## 2. OAuth 2.0 — Delegated Authorization

**OAuth 2.0** is an open standard for *delegated authorization*. Notice I said authorization, not authentication.

**Analogy:** You go to a fancy hotel and give the valet your car keys. But you don't give them your master key that opens the trunk and the glovebox. You give them a special "valet key" that only turns on the ignition and drives the car for a maximum of 2 miles. That is delegated authorization.

In the digital world, this happens when an application (like a third-party analytics tool) wants to read your Google Contacts. You don't give that tool your Google password. Instead, Google asks you: *"Do you authorize this app to read your contacts?"* If you say yes, Google issues an **Access Token** (the valet key) to the app.

### The Key Flows (Grant Types)

1. **Authorization Code Flow (Standard for Web Apps):**
   - The user is redirected to the Authorization Server (e.g., Google).
   - They log in and consent.
   - Google redirects back to your server with a short-lived `auth_code`.
   - Your backend server securely exchanges the `auth_code` for an `access_token` and `refresh_token` using a Client Secret.
   - **Why?** Because the `access_token` is never exposed to the user's browser, keeping it safe from malicious browser extensions.

2. **Authorization Code with PKCE (Proof Key for Code Exchange):**
   - Used for Single Page Apps (SPAs) like React or Mobile Apps where you cannot safely store a Client Secret on the device.
   - It dynamically generates a cryptographic secret (code verifier) for every single authorization request, proving that the app asking for the token is the exact same app that initiated the request.

3. **Client Credentials Flow:**
   - Used for Machine-to-Machine (M2M) communication. There is no user involved.
   - Example: Your backend billing service needs to talk to your backend email service. It just sends its Client ID and Client Secret to the Auth server to get a token.

> [!NOTE]
> **Teacher FAQ:** "Why do we need a Refresh Token?"
> Access tokens are purposefully short-lived (e.g., 15 minutes) to limit the blast radius if they are stolen. Once expired, the client uses the long-lived Refresh Token (stored securely) to get a new Access Token without asking the user to log in again. If a user revokes access, you simply invalidate the Refresh Token.

---

## 3. OpenID Connect (OIDC)

If OAuth 2.0 is for authorization, how do we handle authentication (verifying *who* the user is)? For a long time, developers abused OAuth 2.0 to do authentication by making a request to an `/about_me` endpoint using the access token. This was non-standard and messy.

Enter **OpenID Connect (OIDC)**. OIDC is a thin identity layer built *on top of* OAuth 2.0.

When you use OIDC, the Authorization Server doesn't just return an Access Token; it also returns an **ID Token**.
- The ID Token is a JWT.
- It contains standard claims about the user: `sub` (subject identifier), `name`, `email`, and when they authenticated.

When you see a "Log in with Google" or "Log in with Apple" button, 99% of the time, this is powered by OpenID Connect.

---

## 4. SAML — XML-Based SSO

**SAML (Security Assertion Markup Language)** is the grandparent of enterprise Single Sign-On (SSO). While startups and consumer apps use OAuth/OIDC, legacy enterprises, banks, and healthcare companies heavily rely on SAML.

**Analogy:** Imagine working at a giant corporation. You are issued an RFID badge by HR (the Identity Provider). That single badge lets you into the main lobby, the cafeteria, and the IT server room (the Service Providers).

### How SAML Works
1. You try to access an internal HR app (Service Provider).
2. The app redirects you to Okta/Ping Identity (Identity Provider) with a SAML Request.
3. You log in to Okta.
4. Okta generates a heavily structured **XML document** called a SAML Assertion, signs it cryptographically, and redirects your browser back to the HR app.
5. The HR app parses the XML, verifies the signature, and lets you in.

**Why is it still used?** It is incredibly robust, highly standardized in the corporate world, and allows for extremely granular security policies baked straight into the XML.

| Feature | OIDC | SAML |
| :--- | :--- | :--- |
| **Data Format** | JSON (JWT) | XML |
| **Primary Use Case** | Consumer Web, Mobile, Modern APIs | Enterprise SSO (Okta, Active Directory) |
| **Complexity** | Lightweight and easy to parse | Heavy, verbose, requires XML parsers |

---

## 5. MFA / WebAuthn & FIDO2

Passwords are fundamentally broken. Users reuse them, they get leaked in data breaches, and they are susceptible to phishing.

**Multi-Factor Authentication (MFA)** requires something you *know* (password) and something you *have* (a device).

However, SMS-based MFA and Time-based One-Time Passwords (TOTP via Google Authenticator) are still vulnerable to **Man-in-the-Middle (MitM) Phishing**. If a user goes to a fake website (`g00gle.com`), the attacker can proxy the password AND the 6-digit code in real-time.

### WebAuthn and FIDO2
To solve this, the industry created **WebAuthn** (Web Authentication API) under the FIDO2 standard.
This utilizes hardware-backed security:
- YubiKeys (USB security keys)
- TouchID / FaceID on your Macbook or iPhone (Platform Authenticators)

**How it stops phishing:**
When you register a WebAuthn device, it generates a Public/Private key pair bound *specifically* to the domain name (e.g., `google.com`).
If you are tricked into visiting `g00gle.com`, the browser looks at the domain, realizes it doesn't match the origin the key was registered for, and **refuses to sign the challenge**. The phishing attack fails instantly.

> [!TIP]
> **System Design Interview Tip:** If asked to design a highly secure internal system (like an admin portal for a bank), always mention enforcing hardware-backed MFA (WebAuthn/YubiKeys) for all employees to completely eliminate credential-stuffing and phishing risks.

---

## 6. RBAC vs ABAC Access Control

Once a user is authenticated, how do we determine what they can do?

### RBAC (Role-Based Access Control)
Users are assigned **Roles** (e.g., `Admin`, `Editor`, `Viewer`). Roles are assigned **Permissions** (e.g., `delete_post`, `edit_post`, `read_post`).

**Analogy:** A restaurant manager. By nature of having the "Manager" role, they have the keys to the safe, the freezer, and the cash register.
- **Pros:** Very easy to reason about, implement, and audit.
- **Cons:** Suffers from "Role Explosion." What if you want a Manager who can only open the safe on Tuesdays? You have to create a new role: `Manager_Tuesday_Safe`.

### ABAC (Attribute-Based Access Control)
Access is granted dynamically based on **Attributes** of the User, the Resource, and the Environment.
- **User Attributes:** Department, Clearance Level.
- **Resource Attributes:** Sensitivity of the document, owner of the document.
- **Environment Attributes:** Time of day, IP Address.

**Policy Example:** *"Allow access IF User.Department == 'Finance' AND Resource.Classification == 'Confidential' AND Environment.Time == '9am-5pm' AND Environment.IP_Range == 'Internal_VPN'."*

- **Pros:** Infinitely flexible and granular.
- **Cons:** Extremely complex to engineer. Evaluating these rules requires a dedicated Policy Engine (like OPA - Open Policy Agent) which adds latency to every request.

**When to use which?** Start with RBAC. Only move to ABAC when your business rules become so complex that RBAC leads to an unmanageable explosion of hundreds of hyper-specific roles.

---

**Summary:** You must understand AuthN vs AuthZ. Use JWTs for stateless microservices, OIDC for modern user login, SAML for enterprise SSO, and WebAuthn for phishing-resistant security. Start with RBAC for permissions, and graduate to ABAC only when absolute granularity is required.
