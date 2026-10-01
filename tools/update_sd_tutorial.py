# -*- coding: utf-8 -*-
"""
Updates System_Design_Tutorial/topics.js and markdown files in content/
to replace messy calculations, steps, and raw symbols with clean, professional titles.
"""
import os, json, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOPICS_FILE = os.path.join(ROOT, 'System_Design_Tutorial', 'topics.js')
CONTENT_DIR = os.path.join(ROOT, 'System_Design_Tutorial', 'content')

# Map of old anchor to (new_title, new_anchor, old_md_header_pattern, new_md_header)
REPLACEMENTS = {
    # 5-step framework
    'step-1-clarify-requirements-5-min-functional-non-functional-scale-constraints': (
        'Phase 1: Clarifying Requirements & Scope',
        'phase-1-clarifying-requirements-scope',
        r'## Step 1 [—–-].*',
        '## Phase 1: Clarifying Requirements & Scope'
    ),
    'step-2-back-of-envelope-estimates-qps-storage-yr-bandwidth': (
        'Phase 2: Scale & Capacity Estimation',
        'phase-2-scale-capacity-estimation',
        r'## Step 2 [—–-].*',
        '## Phase 2: Scale & Capacity Estimation'
    ),
    'step-3-high-level-design-draw-4-8-boxes-trace-key-request-flow': (
        'Phase 3: High-Level Architectural Design',
        'phase-3-high-level-architectural-design',
        r'## Step 3 [—–-].*',
        '## Phase 3: High-Level Architectural Design'
    ),
    'step-4-deep-dives-schema-bottlenecks-failure-modes-let-interviewer-steer': (
        'Phase 4: Component Deep Dives & Bottlenecks',
        'phase-4-component-deep-dives-bottlenecks',
        r'## Step 4 [—–-].*',
        '## Phase 4: Component Deep Dives & Bottlenecks'
    ),
    'step-5-trade-offs-what-breaks-at-10x-honest-about-limits-senior-signal': (
        'Phase 5: Failure Modes & Scalability Limits',
        'phase-5-failure-modes-scalability-limits',
        r'## Step 5 [—–-].*',
        '## Phase 5: Failure Modes & Scalability Limits'
    ),

    # Cheat sheet
    'powers-of-2-2-10-1k-2-20-1m-2-30-1b-2-40-1t': (
        'Powers of Two & Data Volume Units',
        'powers-of-two-data-volume-units',
        r'## Powers of 2:.*',
        '## Powers of Two & Data Volume Units'
    ),
    'read-latencies-l1-0-5ns-l2-7ns-ram-100ns-ssd-150-s-hdd-10ms-wan-150ms': (
        'Storage Hierarchy & Read Latencies',
        'storage-hierarchy-read-latencies',
        r'## Read latencies:.*',
        '## Storage Hierarchy & Read Latencies'
    ),
    '1b-users-10-dau-1-request-day-1157-qps': (
        'Daily Active Users to QPS Conversion',
        'daily-active-users-to-qps-conversion',
        r'## 1B users,.*',
        '## Daily Active Users to QPS Conversion'
    ),
    '100gb-day-data-3tb-month-36tb-year-can-a-single-machine-hold-it': (
        'Annual Data Growth & Storage Sizing',
        'annual-data-growth-storage-sizing',
        r'## 100GB/day data.*',
        '## Annual Data Growth & Storage Sizing'
    ),
    'text-tweet-280-chars-image-tweet-500kb-video-100mb': (
        'Payload & Media Storage Sizing',
        'payload-media-storage-sizing',
        r'## Text tweet:.*',
        '## Payload & Media Storage Sizing'
    ),

    # Latency & Throughput basics
    'l1-cache-0-5ns-ram-100ns-ssd-150-s-network-150ms': (
        'Latency vs Throughput Fundamentals',
        'latency-vs-throughput-fundamentals',
        r'## Latency vs Throughput.*',
        '## Latency vs Throughput Fundamentals'
    ),
    'p50-p95-p99-tail-latency-dominates-user-experience': (
        'Percentiles & Tail Latency (P50, P95, P99)',
        'percentiles-tail-latency-p50-p95-p99',
        r'## P50 / P95 / P99.*',
        '## Percentiles & Tail Latency (P50, P95, P99)'
    ),
    'vertical-scaling-scale-up-simpler-limited-by-hardware': (
        'Vertical Scaling (Scale-Up)',
        'vertical-scaling-scale-up',
        r'## Vertical scaling.*',
        '## Vertical Scaling (Scale-Up)'
    ),
    'horizontal-scaling-scale-out-stateless-apps-requires-lb': (
        'Horizontal Scaling (Scale-Out)',
        'horizontal-scaling-scale-out',
        r'## Horizontal scaling.*',
        '## Horizontal Scaling (Scale-Out)'
    ),
    'back-of-envelope-estimation-qps-storage-bandwidth': (
        'Back-of-Envelope Sizing Calculations',
        'back-of-envelope-sizing-calculations',
        r'## Back-of-envelope estimation.*',
        '## Back-of-Envelope Sizing Calculations'
    ),
    'batching-increases-throughput-at-the-cost-of-latency': (
        'Batching vs Streaming Trade-offs',
        'batching-vs-streaming-trade-offs',
        r'## Batching increases.*',
        '## Batching vs Streaming Trade-offs'
    ),

    # Availability & SLAs
    'sli-slo-sla-indicator-objective-agreement': (
        'SLI, SLO, and SLA Metrics',
        'sli-slo-and-sla-metrics',
        r'## SLI / SLO / SLA.*',
        '## SLI, SLO, and SLA Metrics'
    ),
    '99-9-8-76-hrs-yr-99-99-52-min-yr-99-999-5-25-min-yr': (
        'High Availability & Uptime Calculations (The Nines)',
        'high-availability-uptime-calculations-the-nines',
        r'## 99\.9%.*',
        '## High Availability & Uptime Calculations (The Nines)'
    ),
    'availability-in-series-multiply-a1-a2-cascades': (
        'Cascading Availability in Series',
        'cascading-availability-in-series',
        r'## Availability in series:.*',
        '## Cascading Availability in Series'
    ),
    'availability-in-parallel-1-1-a-n-redundancy-helps': (
        'Redundancy & Parallel Availability',
        'redundancy-parallel-availability',
        r'## Availability in parallel:.*',
        '## Redundancy & Parallel Availability'
    ),
    'active-active-failover-both-serve-traffic-fastest-failover': (
        'Active-Active Failover Architecture',
        'active-active-failover-architecture',
        r'## Active-Active failover.*',
        '## Active-Active Failover Architecture'
    ),
    'active-passive-failover-warm-standby-60s-rto': (
        'Active-Passive Failover Architecture',
        'active-passive-failover-architecture',
        r'## Active-Passive failover.*',
        '## Active-Passive Failover Architecture'
    ),

    # Circuit breakers
    'circuit-breaker-states-closed-normal-open-failing-half-open-testing': (
        'Circuit Breaker State Machine',
        'circuit-breaker-state-machine',
        r'## (?:4\.\s*)?Circuit breaker states:.*',
        '## Circuit Breaker State Machine'
    ),

    # DNS
    'dns-resolution-recursive-resolver-root-tld-authoritative': (
        'Hierarchical DNS Resolution Flow',
        'hierarchical-dns-resolution-flow',
        r'## DNS resolution:.*',
        '## Hierarchical DNS Resolution Flow'
    ),

    # HTTP Status codes
    'status-codes-2xx-success-3xx-redirect-4xx-client-5xx-server': (
        'HTTP Status Code Categories',
        'http-status-code-categories',
        r'## Status codes:.*',
        '## HTTP Status Code Categories'
    ),

    # SSE
    'sse-server-sent-events-http-based-server-client-only-auto-reconnect': (
        'Server-Sent Events (SSE)',
        'server-sent-events-sse',
        r'## SSE \(Server-Sent Events\).*',
        '## Server-Sent Events (SSE)'
    ),
}

def update_topics_js():
    with open(TOPICS_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    topics = json.loads(content[content.index('['):content.rindex(']')+1])
    
    updated_count = 0
    for sec in topics:
        for sub in sec.get('subsections', []):
            for c in sub.get('concepts', []):
                anchor = c.get('anchor')
                if anchor in REPLACEMENTS:
                    new_title, new_anchor, _, _ = REPLACEMENTS[anchor]
                    c['title'] = new_title
                    c['anchor'] = new_anchor
                    updated_count += 1
                    
    new_js = "window.topicsData = " + json.dumps(topics, ensure_ascii=False, indent=2) + ";\n"
    with open(TOPICS_FILE, 'w', encoding='utf-8') as f:
        f.write(new_js)
    print(f"Updated {updated_count} concepts in topics.js")

def update_markdown_files():
    for fpath in [os.path.join(CONTENT_DIR, f) for f in os.listdir(CONTENT_DIR) if f.endswith('.md')]:
        with open(fpath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        modified = False
        new_lines = []
        for line in lines:
            replaced_line = line
            for old_anchor, (new_title, new_anchor, pattern, new_header) in REPLACEMENTS.items():
                if line.startswith('## ') and re.match(f'^{pattern}$', line.strip()):
                    replaced_line = new_header + '\n'
                    modified = True
                    break
            new_lines.append(replaced_line)
        if modified:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            print(f"Updated headings in {os.path.basename(fpath)}")

if __name__ == '__main__':
    update_topics_js()
    update_markdown_files()
