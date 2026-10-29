import os
import sys
import tempfile
import time
import re
import html as html_lib

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def atomic_write(filepath, content):
    d = os.path.dirname(os.path.abspath(filepath))
    with tempfile.NamedTemporaryFile('w', dir=d, delete=False, encoding='utf-8') as tf:
        tf.write(content)
        temp_name = tf.name
    for attempt in range(4):
        try:
            os.replace(temp_name, filepath)
            break
        except OSError:
            if attempt == 3: raise
            time.sleep(0.1 * (attempt + 1))
    if os.path.exists(temp_name):
        try: os.unlink(temp_name)
        except OSError: pass

# 24 Concepts across 6 Subsections
API_SUBSECTIONS = [
    {
        "num": "16.1",
        "title": "API Architectural Paradigms, Protocols & Wire Formats",
        "desc": "Foundational transport protocols, architectural styles, and wire formats from REST to gRPC and full-duplex streaming.",
        "concepts": [
            ("16.1.1", "REST & Resource-Oriented Architecture (ROA)",
             "Richardson Maturity Model (Level 0 to Level 3 HATEOAS), HTTP verb semantics (safe vs idempotent: GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS), standard status code taxonomies (200, 201, 204, 304, 400, 401, 403, 404, 409, 422, 429, 500, 502, 503), noun-based URI path hierarchies, and content negotiation via Accept and Content-Type.",
             "https://www.youtube.com/watch?v=-mN3VyJuCjM", "00:00", "Traversy Media", "https://github.com/microsoft/api-guidelines"),
            ("16.1.2", "GraphQL Schemas, Execution & Apollo Federation",
             "Schema Definition Language (SDL), Queries, Mutations, Subscriptions, AST parsing and execution resolvers, the N+1 problem and DataLoader batching/memoization, Schema Stitching vs Apollo Federation (subgraphs, router, @key, @shareable), and query depth/cost analysis for security.",
             "https://www.youtube.com/watch?v=yWzKJPw_VzM", "00:00", "Fireship", "https://graphql.org/learn/"),
            ("16.1.3", "gRPC & Protocol Buffers (Protobuf v3)",
             "HTTP/2 multiplexed framing, binary wire encoding (varints, zigzag, length-delimited), proto3 interface definition, communication patterns (Unary, Server Streaming, Client Streaming, Bidirectional Streaming), gRPC-Web bridging, deadlines/cancellations, and metadata interceptors.",
             "https://www.youtube.com/watch?v=gnchfOoj9Ec", "00:00", "Hussein Nasser", "https://grpc.io/docs/what-is-grpc/core-concepts/"),
            ("16.1.4", "Real-Time & Streaming APIs: WebSockets, SSE & Webhooks",
             "WebSockets full-duplex persistent TCP frames (ws://, wss://), Server-Sent Events (SSE) unidirectional HTTP streaming (text/event-stream), Webhook outbound delivery patterns (HMAC-SHA256 signature verification, idempotency, exponential backoff retries, and dead-letter queues), and long polling fallback mechanics.",
             "https://www.youtube.com/watch?v=1BfCnjr_Vjg", "00:00", "Fireship", "https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events")
        ]
    },
    {
        "num": "16.2",
        "title": "API Specifications, Schema Governance & Evolution",
        "desc": "Machine-readable contract definitions, schema validation engines, versioning hygiene, and consumer-driven contract testing.",
        "concepts": [
            ("16.2.1", "OpenAPI Specification (OAS 3.0 & 3.1) & Swagger Ecosystem",
             "Contract-first design, YAML/JSON schemas, paths, operations, request bodies, reusable components, discriminators, automated client/server SDK code generation (OpenAPI Generator), and interactive documentation (Swagger UI, Redoc, Stoplight).",
             "https://www.youtube.com/watch?v=7PrxUe7vL5k", "00:00", "freeCodeCamp.org", "https://spec.openapis.org/oas/v3.1.0"),
            ("16.2.2", "AsyncAPI & Event-Driven Message Contracts",
             "Machine-readable specifications for asynchronous event architectures (Kafka topics, RabbitMQ queues, MQTT channels, WebSocket messages), channels, operations (send/receive), payload schemas, and protocol bindings.",
             "https://www.youtube.com/watch?v=nN40NqQfKx8", "00:00", "IBM Technology", "https://www.asyncapi.com/docs/concepts/overview"),
            ("16.2.3", "JSON Schema Validation & Consumer-Driven Contract Testing (Pact)",
             "Draft 2020-12 / Draft-07 schema validation engines (ajv, pydantic), consumer-driven contract testing with Pact, broker verification, preventing breaking schema regressions, and CI/CD contract validation gates.",
             "https://www.youtube.com/watch?v=sAAX4W_G_1Q", "00:00", "Continuous Delivery", "https://json-schema.org/learn/getting-started-step-by-step"),
            ("16.2.4", "API Versioning Strategies & Schema Evolution",
             "URI path versioning (/v1/), custom header versioning (Accept: application/vnd.company.v1+json), query parameter versioning, backward and forward compatibility rules (Additive Changes, Deprecation workflows via Sunset and Deprecation RFC headers, breaking change policies).",
             "https://www.youtube.com/watch?v=XhIq6V4Xh2M", "00:00", "ByteByteGo", "https://restfulapi.net/versioning/")
        ]
    },
    {
        "num": "16.3",
        "title": "Data Handling, Querying & Transport Optimization",
        "desc": "Scalable dataset traversal, conditional caching, compound filtering, and high-efficiency binary transport.",
        "concepts": [
            ("16.3.1", "Pagination Patterns: Offset-Limit vs Keyset (Cursor-Based)",
             "Performance degradation of SQL OFFSET on large datasets, keyset/cursor pagination using indexed sort keys (created_at, id), encoding opaque cursors (Base64), RFC 5988 Link navigation headers, and infinite scrolling data contracts.",
             "https://www.youtube.com/watch?v=zwBXIdn_3qI", "00:00", "Hussein Nasser", "https://jsonapi.org/format/#fetching-pagination"),
            ("16.3.2", "Advanced Filtering, Multi-Field Sorting & Sparse Fieldsets",
             "JSON:API style compound filtering (?filter[status]=active&filter[price_gte]=100), dynamic multi-column ordering (?sort=-created_at,price), sparse fieldsets (?fields=id,title,author), and GraphQL field selection comparison.",
             "https://www.youtube.com/watch?v=u18N7rZ-xL8", "00:00", "Web Dev Simplified", "https://jsonapi.org/format/#fetching-filtering"),
            ("16.3.3", "HTTP Caching, Conditional Requests & CDN Edge Validation",
             "Cache-Control directives (max-age, s-maxage, no-cache, no-store, must-revalidate, stale-while-revalidate), validator headers (Strong ETag vs Weak W/..., Last-Modified), conditional requests (If-None-Match -> 304 Not Modified, If-Match optimistic concurrency), and CDN edge caching.",
             "https://www.youtube.com/watch?v=HiBdZskyv2A", "00:00", "Computerphile", "https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching"),
            ("16.3.4", "Payload Compression, Streaming & Binary Encodings",
             "HTTP payload compression algorithms (Gzip, Brotli br), Content-Encoding vs Transfer-Encoding: chunked, newline-delimited JSON (NDJSON) streaming for large tabular exports, and binary payload serialization (MessagePack, CBOR, Avro).",
             "https://www.youtube.com/watch?v=4b4MUYve_U8", "00:00", "Computerphile", "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Encoding")
        ]
    },
    {
        "num": "16.4",
        "title": "API Resilience, Traffic Management & Fault Tolerance",
        "desc": "Mitigating thundering herds, preventing duplicate billing, handling cascading downstream outages, and standardized error envelopes.",
        "concepts": [
            ("16.4.1", "Rate Limiting & Throttling Algorithms",
             "Token Bucket, Leaky Bucket, Fixed Window Counter, Sliding Window Log, Sliding Window Counter; distributed atomic token enforcement with Redis Lua scripts; HTTP 429 Too Many Requests response standards (Retry-After, RateLimit-Limit, RateLimit-Remaining, RateLimit-Reset).",
             "https://www.youtube.com/watch?v=MIJFyUPG4Z4", "00:00", "Hello Interview", "https://cloud.google.com/architecture/rate-limiting-strategies-techniques"),
            ("16.4.2", "Idempotency Mechanisms & Duplicate Request Prevention",
             "Enterprise idempotency keys (Idempotency-Key / X-Idempotency-Key headers), distributed atomic deduplication locks (Redis, DynamoDB conditional writes), caching and replaying execution responses for retried mutating operations (payments, order processing).",
             "https://www.youtube.com/watch?v=DQ57zYedMdQ", "00:00", "Hello Interview", "https://stripe.com/docs/api/idempotent_requests"),
            ("16.4.3", "Circuit Breakers, Exponential Backoff & Timeout Budgets",
             "Distributed circuit breaker finite state machines (Closed, Open, Half-Open), failure threshold triggers, recovery probes, exponential backoff with full jitter formulas, deadline propagation across microservice call graphs, and graceful degradation fallbacks.",
             "https://www.youtube.com/watch?v=ADHcBxEXvFA", "00:00", "ByteByteGo", "https://martinfowler.com/bliki/CircuitBreaker.html"),
            ("16.4.4", "RFC 7807 / RFC 9457 Problem Details & Standardized Errors",
             "Structured machine-readable error representations (application/problem+json), standard fields (type, title, status, detail, instance, invalid_params), correlation/request trace IDs, suppressing internal stack traces, and developer-friendly error taxonomies.",
             "https://www.youtube.com/watch?v=2n3xS8eR2J8", "00:00", "IBM Technology", "https://datatracker.ietf.org/doc/html/rfc7807")
        ]
    },
    {
        "num": "16.5",
        "title": "API Security, Identity Federation & OWASP API Top 10",
        "desc": "Cryptographic authentication, zero-trust mTLS, delegated authorization tokens, and vulnerability defense against the OWASP API Top 10.",
        "concepts": [
            ("16.5.1", "API Authentication Mechanics: API Keys, Bearer Tokens & mTLS",
             "API Key rotation and hashing (never raw in URLs), HTTP Bearer Authorization headers, Mutual TLS (mTLS) zero-trust bidirectional certificate validation for service-to-service communication, and client certificate thumbprint binding.",
             "https://www.youtube.com/watch?v=7Q17ubqLfaM", "00:00", "Hussein Nasser", "https://owasp.org/www-project-api-security/"),
            ("16.5.2", "OAuth 2.0 Framework & OpenID Connect (OIDC)",
             "Authorization Code Grant with Proof Key for Code Exchange (PKCE) for public clients/SPAs, Client Credentials grant for machine-to-machine, Refresh Token rotation strategies, JSON Web Tokens (JWT: Header, Payload, Signature), asymmetric signing (RS256, ES256), and JWKS (.well-known/jwks.json) key verification.",
             "https://www.youtube.com/watch?v=CPbvxxslDTU", "00:00", "ByteByteGo", "https://oauth.net/2/"),
            ("16.5.3", "Fine-Grained Authorization: RBAC, ABAC & Policy as Code",
             "Role-Based Access Control (RBAC), Attribute-Based Access Control (ABAC) evaluating user/resource/environment attributes, OAuth scopes vs JWT claims, and Policy-as-Code engines (Open Policy Agent OPA / Rego, AWS Cedar, Zanzibar relationship-based access control ReBAC).",
             "https://www.youtube.com/watch?v=R6tUNpR4flk", "00:00", "IBM Technology", "https://www.openpolicyagent.org/docs/latest/"),
            ("16.5.4", "OWASP API Security Top 10 Vulnerabilities & Defense in Depth",
             "Broken Object Level Authorization (BOLA/IDOR) mitigations, Broken Function Level Authorization (BFLA), Unrestricted Resource Consumption, Mass Assignment / Object Property Level Authorization, Server-Side Request Forgery (SSRF) in webhook dispatchers, CORS policy (Access-Control-Allow-Origin, preflight OPTIONS), and input sanitization.",
             "https://www.youtube.com/watch?v=4sE1a4Yk9_o", "00:00", "freeCodeCamp.org", "https://owasp.org/API-Security/editions/2023/en/0x11-t10/")
        ]
    },
    {
        "num": "16.6",
        "title": "API Gateway Architecture, Service Mesh & Observability",
        "desc": "Edge routing topologies, east-west microservice traffic management, OpenTelemetry distributed tracing, and developer self-service.",
        "concepts": [
            ("16.6.1", "API Gateway Architectural Patterns & Topologies",
             "Edge gateway vs internal microgateway, reverse proxy routing, SSL/TLS termination, protocol translation (REST-to-gRPC, JSON-to-Kafka), request transformation, and top modern gateways (Kong Gateway, Apache APISIX, Traefik, AWS API Gateway, Envoy Proxy).",
             "https://www.youtube.com/watch?v=hRP5VvC9r0I", "00:00", "ByteByteGo", "https://docs.konghq.com/gateway/latest/"),
            ("16.6.2", "Service Mesh & Microservice East-West Traffic",
             "Envoy data plane sidecars, Istio / Linkerd control planes, mTLS automatic encryption, traffic management (canary deployments, percentage traffic splitting, fault injection), and circuit breaking at the infrastructure mesh layer.",
             "https://www.youtube.com/watch?v=16fgzklcF7Y", "00:00", "IBM Technology", "https://istio.io/latest/about/service-mesh/"),
            ("16.6.3", "Distributed Tracing, Metrics & Observability (OpenTelemetry)",
             "W3C Trace Context standards (traceparent, tracestate), OpenTelemetry (OTel) instrumentation, distributed trace context propagation across HTTP/gRPC boundaries, Jaeger and Zipkin visualization, and API Golden Signals (Latency, Traffic, Errors, Saturation).",
             "https://www.youtube.com/watch?v=l_tQ_h6_ZlE", "00:00", "ByteByteGo", "https://opentelemetry.io/docs/concepts/what-is-opentelemetry/"),
            ("16.6.4", "API Developer Experience (DX), Mocking & Governance",
             "Developer self-service onboarding portals, interactive API documentation, sandbox environments and mock servers (Prism, Mockoon), API monetization and quota tiers, SDK maintenance automation, and enterprise schema linters (Spectral).",
             "https://www.youtube.com/watch?v=rTmyJkZk37g", "00:00", "Continuous Delivery", "https://stoplight.io/open-source/spectral")
        ]
    }
]

def render_subsections_html():
    out = []
    for sub in API_SUBSECTIONS:
        num = sub["num"]
        title = sub["title"]
        desc = sub["desc"]
        concepts = sub["concepts"]
        out.append(f'''<div class="subsection">
<div class="subsection-head">
<span class="subsection-tag">{num}</span>
<h3>{html_lib.escape(title)}</h3>
<span style="font-size:11px;color:var(--text-faint);">{len(concepts)} concepts</span>
</div>
<div class="subsection-desc">{html_lib.escape(desc)}</div>
<ol class="concepts">''')
        for cid, cname, cdesc, vid, vtime, vchannel, doc in concepts:
            clean_name = re.sub(r'[^a-zA-Z0-9]+', ' ', cname).lower().strip()
            out.append(f'''<li data-cid="{cid}" data-name="{clean_name}">
<div class="done-check" title="Mark as done"></div>
<div class="bookmark-star" title="Bookmark">☆</div>
<div>
<div class="cname">{html_lib.escape(cname)}</div>
<div style="font-size:11.5px;color:var(--text-faint);margin-top:2px">{html_lib.escape(cdesc)}</div>
</div>
<div class="res-links"><a class="video" data-start="0" data-vchannel="{html_lib.escape(vchannel)}" data-vdur="" data-vtitle="{html_lib.escape(cname)}" href="{vid}" rel="noopener" target="_blank" title="Watch walkthrough: {html_lib.escape(cname)}">🎬YT</a><a href="{doc}" rel="noopener" target="_blank" title="Official Reference">🌐Doc</a></div>
</li>''')
        out.append('</ol>\n</div>')
    return '\n'.join(out)

def expand_tech_apis():
    p = os.path.join(ROOT, 'tech_apis.html')
    with open(p, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update edition & stats
    html = re.sub(
        r'<div class="edition">[^<]+</div>',
        '<div class="edition">API Architecture · Masterclass 12 · 6 Subsections · 24 Concepts</div>',
        html
    )

    old_stats = '''<div class="stats">
    <div class="stat"><div class="n">2</div><div class="l">Subsections</div></div>
    <div class="stat"><div class="n">8</div><div class="l">Concepts</div></div>
    <div class="stat"><div class="n">100%</div><div class="l">Curated</div></div>
    <div class="stat"><div class="n">15+</div><div class="l">Verified Docs &amp; Labs</div></div>
  </div>'''

    new_stats = '''<div class="stats">
    <div class="stat"><div class="n">6</div><div class="l">Subsections</div></div>
    <div class="stat"><div class="n">24</div><div class="l">Concepts</div></div>
    <div class="stat"><div class="n">100%</div><div class="l">Curated</div></div>
    <div class="stat"><div class="n">25+</div><div class="l">Verified Docs &amp; Labs</div></div>
  </div>'''
    if old_stats in html:
        html = html.replace(old_stats, new_stats, 1)
    else:
        # Regex replacement matching up to </div>\n\n  <div class="overall-progress">
        html = re.sub(r'<div class="stats">[\s\S]*?</div>\s*(?=<div class="overall-progress">)', new_stats + '\n\n  ', html, count=1)

    # 2. Update overall progress pct & search placeholder
    html = re.sub(r'<span class="pct" id="overall-pct">[^<]+</span>', '<span class="pct" id="overall-pct">0 / 24</span>', html)
    html = re.sub(r'placeholder="Search [^"]+"', 'placeholder="Search 24 concepts…"', html)

    # 3. Update focus bar & section banner
    html = re.sub(
        r'<span class="focus-bar-stats">[^<]+</span>',
        '<span class="focus-bar-stats">24 concepts &bull; 6 subsections</span>',
        html
    )
    html = re.sub(
        r'<div class="meta">[^<]+</div>',
        '<div class="meta">6 subsections · 24 concepts</div>',
        html,
        count=1
    )
    html = re.sub(
        r'<div class="pct-text" data-pp-text="16">[^<]+</div>',
        '<div class="pct-text" data-pp-text="16">0 / 24</div>',
        html
    )

    # 4. Replace subsections inside section-16
    subs_html = render_subsections_html()
    sub_start = html.find('<div class="subsection">')
    sub_end = html.find('</section>', sub_start)
    if sub_start != -1 and sub_end != -1:
        html = html[:sub_start] + subs_html + '\n' + html[sub_end:]
        print("Updated subsections in tech_apis.html")
    else:
        raise ValueError("Could not find subsections in tech_apis.html")

    atomic_write(p, html)
    print("Saved tech_apis.html successfully!")

def expand_all_tech():
    p = os.path.join(ROOT, 'all_tech.html')
    with open(p, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update edition and hero stats
    html = re.sub(
        r'<div class="edition">v4 &bull; All-in-One Tech &amp; Engineering Portal &bull; 13 Disciplines &bull; \d+ Subsections &bull; \d+ Concepts</div>',
        '<div class="edition">v4 &bull; All-in-One Tech &amp; Engineering Portal &bull; 13 Disciplines &bull; 50 Subsections &bull; 197 Concepts</div>',
        html
    )

    html = re.sub(
        r'(<div class="stat"><div class="n">)\d+(</div><div class="l">Subsections</div></div>)',
        r'\g<1>50\g<2>',
        html
    )
    html = re.sub(
        r'(<div class="stat"><div class="n">)\d+(</div><div class="l">Concepts</div></div>)',
        r'\g<1>197\g<2>',
        html
    )

    # 2. Update card-apis in domain deck
    card_apis_old = re.search(r'(<div class="domain-card[^"]*"[^>]*id="card-apis"[\s\S]*?</div>\s*</div>)', html)
    if card_apis_old:
        old_card = card_apis_old.group(1)
        new_card = re.sub(
            r'<div class="domain-card-chips">[\s\S]*?</div>',
            '''<div class="domain-card-chips">
<span class="domain-card-chip">6 Subsections</span>
<span class="domain-card-chip">24 Concepts</span>
<span class="domain-card-chip highlight">API Governance, Idempotency & Rate Limiting</span>
</div>''',
            old_card
        )
        html = html.replace(old_card, new_card, 1)
        print("Updated card-apis in all_tech.html")

    # 3. Update Section 16 header, stats, and subsections
    sec16_match = re.search(r'(<section class="section domain-section"[^>]*id="section-16"[\s\S]*?</section>)', html)
    if sec16_match:
        sec16_text = sec16_match.group(1)
        
        sec16_new = re.sub(
            r'<span class="focus-bar-stats">[^<]+</span>',
            '<span class="focus-bar-stats">24 concepts &bull; 6 subsections</span>',
            sec16_text
        )
        sec16_new = re.sub(
            r'<div class="meta">[^<]+</div>',
            '<div class="meta">6 subsections · 24 concepts</div>',
            sec16_new
        )
        sec16_new = re.sub(
            r'<div class="pct-text" data-pp-text="16">[^<]+</div>',
            '<div class="pct-text" data-pp-text="16">0 / 24</div>',
            sec16_new
        )

        subs_html = render_subsections_html()
        sub_start = sec16_new.find('<div class="subsection">')
        sub_end = sec16_new.rfind('</section>')
        if sub_start != -1 and sub_end != -1:
            sec16_new = sec16_new[:sub_start] + subs_html + '\n' + sec16_new[sub_end:]
            html = html.replace(sec16_text, sec16_new, 1)
            print("Updated section-16 in all_tech.html")
        else:
            raise ValueError("Could not find subsections in section-16 of all_tech.html")
    else:
        raise ValueError("Could not find section-16 in all_tech.html")

    atomic_write(p, html)
    print("Saved all_tech.html successfully!")

if __name__ == '__main__':
    expand_tech_apis()
    expand_all_tech()
    print("Finished expanding API Masterclass!")
