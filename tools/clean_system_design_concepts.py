# -*- coding: utf-8 -*-
"""
Cleans up system_design.html concepts:
- Replaces long, description-stuffed titles with short, accurate, correct titles
- Puts the descriptive explanation underneath the title in a dedicated subtitle div
- Replaces generic/broken video queries with clean, targeted searches (and direct verified videos where available)
"""
import re, json, urllib.parse
from bs4 import BeautifulSoup

# Load verified concept videos from resources.js
sd_res_file = 'System_Design_Tutorial/resources.js'
data = open(sd_res_file, encoding='utf-8').read()
sd_data = json.loads(data[data.index('{'):data.rindex('}')+1])

concept_videos = {}
for k, v in sd_data.get('concepts', {}).items():
    if v.get('videos') and len(v['videos']) > 0:
        concept_videos[k] = v['videos'][0] # [id, title, channel]

# Mapping for 14.1-14.3 case studies to their concept keys in resources.js
CASE_STUDY_MAP = {
    '12.1.1': 'foundational-designs/url-shortener-tinyurl-bit-ly-hash-base62-collision-handling-analytics',
    '12.1.2': 'foundational-designs/distributed-cache-redis-cluster-consistent-hashing-eviction-replication',
    '12.1.3': 'foundational-designs/key-value-store-lsm-tree-compaction-range-queries',
    '12.1.4': 'foundational-designs/content-delivery-network-pull-vs-push-origin-shield-cache-invalidation',
    '12.1.5': 'foundational-designs/rate-limiter-distributed-token-bucket-in-redis-per-user-limits',
    '12.1.6': 'foundational-designs/distributed-job-scheduler-priority-queues-at-least-once-execution-dedup',
    '12.2.1': 'core-interview-designs/chat-whatsapp-slack-websockets-message-ordering-presence-fan-out',
    '12.2.2': 'core-interview-designs/twitter-x-fan-out-on-write-vs-read-hybrid-for-celebrities',
    '12.2.3': 'core-interview-designs/youtube-netflix-upload-pipeline-transcoding-adaptive-bitrate-streaming-cdn',
    '12.2.4': 'core-interview-designs/instagram-photo-sharing-media-upload-feed-generation-s3-cdn',
    '12.2.5': 'core-interview-designs/notification-system-multi-channel-push-email-sms-queues-templates-dedup',
    '12.2.6': 'core-interview-designs/ticketmaster-seat-booking-inventory-locks-payment-timeout-distributed-txns',
    '12.2.7': 'core-interview-designs/tinder-matching-geospatial-indexing-swiping-at-scale-recommendations',
    '12.2.8': 'core-interview-designs/tiktok-short-video-ml-powered-feed-cdn-video-encoding-pipeline',
    '12.2.9': 'core-interview-designs/airbnb-booking-double-booking-prevention-calendar-availability-search',
    '12.2.10': 'core-interview-designs/payment-system-idempotency-double-entry-bookkeeping-audit-logs-pci-dss',
    '12.2.11': 'core-interview-designs/distributed-message-queue-kafka-design-ordering-partitions-consumer-groups',
    '12.2.12': 'core-interview-designs/reddit-hn-voting-ranking-comment-threads-subreddit-feeds',
    '12.2.13': 'core-interview-designs/autocomplete-typeahead-trie-top-k-redis-sorted-sets-prefix-cache',
    '12.3.1': 'advanced-senior-level-designs/uber-rideshare-geospatial-indexing-quad-tree-geohash-matching-real-time-location',
    '12.3.2': 'advanced-senior-level-designs/google-search-crawling-indexing-ranking-pagerank-serving',
    '12.3.3': 'advanced-senior-level-designs/google-drive-dropbox-chunked-upload-dedup-hashing-sync-conflict-resolution',
    '12.3.4': 'advanced-senior-level-designs/google-maps-tile-generation-routing-dijkstra-at-scale-real-time-traffic',
    '12.3.5': 'advanced-senior-level-designs/google-docs-collaborative-editing-ot-operational-transform-or-crdts-conflict-resolution',
    '12.3.6': 'advanced-senior-level-designs/stock-exchange-ultra-low-latency-order-matching-engine-fifo-fairness',
    '12.3.7': 'advanced-senior-level-designs/facebook-news-feed-social-graph-ranking-fan-out-strategies-at-3b-users',
    '12.3.8': 'advanced-senior-level-designs/distributed-locking-service-like-chubby-consensus-lease-renewal-callbacks',
}

# Known verified videos for other core topics
EXTRA_VERIFIED_VIDEOS = {
    '8.2.1': ['Al2JNJBGG30', 'Distributed Consensus - Raft Leader Election', 'Jordan has no life'],
    '8.2.2': ['Al2JNJBGG30', 'Heartbeats and Failure Detection in Distributed Systems', 'Jordan has no life'],
    '8.1.1': ['Al2JNJBGG30', 'Consensus Algorithms: Raft and Paxos Explained', 'Jordan has no life'],
    '1.2.1': ['LAsMrghdFP0', 'Strong Consistency vs Eventual Consistency', 'ByteByteGo'],
    '1.2.2': ['LAsMrghdFP0', 'Eventual Consistency in Distributed Systems', 'ByteByteGo'],
    '1.1.1': ['k-K2FhP-14I', 'CAP Theorem Simplified', 'Gaurav Sen'],
    '3.3.1': ['YM_dEeXmnuY', 'Load Balancers: Algorithms and Design', 'ByteByteGo'],
    '3.5.1': ['mhUQe4BKZXs', 'Rate Limiting Algorithms Explained', 'Tech Dummies'],
    '3.6.1': ['1cFyfT0m3bA', 'WebSockets vs Polling vs Server-Sent Events', 'Hussein Nasser'],
    '4.6.1': ['L521gizea4s', 'Database Sharding and Partitioning', 'Hello Interview'],
    '4.7.1': ['zaRkONvyGr8', 'Consistent Hashing Explained', 'Gaurav Sen'],
    '6.2.1': ['iJLL-KPqBpM', 'Kafka Architecture Deep Dive', 'System Design Interview'],
    '8.1.2': ['26-pDkZpxxY', 'Raft Consensus Algorithm Visualization', 'SecretClub'],
}

def clean_title_and_desc(cid, raw_title, existing_desc):
    title = raw_title.strip()
    desc = existing_desc.strip()
    
    # Custom overrides for special cases
    CUSTOM = {
        '13.1.1': ('Phase 1: Clarifying Requirements & Scope', 'Extract functional & non-functional requirements, traffic scale, and edge constraints.'),
        '13.1.2': ('Phase 2: Scale & Capacity Estimation', 'Calculate QPS, peak multipliers, annual storage growth, and network bandwidth.'),
        '13.1.3': ('Phase 3: High-Level Architectural Design', 'Draw core functional blocks, request routing, and end-to-end data flow.'),
        '13.1.4': ('Phase 4: Component Deep Dives & Bottlenecks', 'Data schemas, partitioning keys, caching layers, and failure-mode analysis.'),
        '13.1.5': ('Phase 5: Failure Modes & Scalability Limits', 'Evaluate 10x scale limits, CAP trade-offs, and graceful degradation strategies.'),
        
        '13.2.1': ('Explicit Trade-off Articulation', 'Clearly explain trade-offs (e.g. strong consistency vs latency cost).'),
        '13.2.2': ('Metric Quantification & SLA Budgeting', 'Quantify scale: QPS, P99 latency budget, monthly egress, and storage tiers.'),
        '13.2.3': ('Failure-First Architectural Mindset', 'Analyze single points of failure and database crashes before the happy path.'),
        '13.2.4': ('Operational Awareness & Observability', 'Design for monitoring, canary deploys, on-call debugging, and safe rollbacks.'),
        '13.2.5': ('Interview Leadership & Pacing', 'Drive the conversation proactively and structure time across all 5 phases.'),
        
        '13.3.1': ('Powers of Two & Data Volume Units', '2^10=1KB, 2^20=1MB, 2^30=1GB, 2^40=1TB memory conversion rules.'),
        '13.3.2': ('Storage Hierarchy & Read Latencies', 'L1 (0.5ns), RAM (100ns), NVMe SSD (150µs), HDD seek (10ms), WAN (150ms).'),
        '13.3.3': ('Active Users to QPS Conversion', 'Convert MAU/DAU and actions per day into queries per second (100,000s shortcut).'),
        '13.3.4': ('Annual Data Growth & Storage Sizing', 'Calculate daily volume to monthly/annual storage to determine sharding needs.'),
        '13.3.5': ('Payload & Media Storage Sizing', 'Text tweet (280B), image thumbnail (500KB), video stream (5-10MB/min).'),
        
        '1.4.1': ('Latency vs Throughput', 'Round-trip time per request vs total request volume processed per second.'),
        '1.4.2': ('Percentiles & Tail Latency (P50, P95, P99)', 'P50 median, P95, and P99 tail latency; mitigating distributed fan-out amplification.'),
        '1.4.3': ('Vertical Scaling (Scale-Up)', 'Upgrading single-node CPU and RAM; hardware limits, cost curve, and SPOF.'),
        '1.4.4': ('Horizontal Scaling (Scale-Out)', 'Adding commodity nodes behind load balancers with stateless service tiers.'),
        '1.4.5': ('Back-of-Envelope Sizing', 'Translating high-level product scale into hardware, memory, and disk counts.'),
        '1.4.6': ('Batching vs Streaming', 'Amortizing network and disk I/O overhead for throughput at the expense of latency.'),
        
        '1.3.1': ('SLI, SLO, and SLA Metrics', 'Service Level Indicators (measured), Objectives (goals), and Agreements (contracts).'),
        '1.3.2': ('High Availability & Uptime (The Nines)', '99.9% (8.76 hrs/yr), 99.99% (52 min/yr), 99.999% (5.25 min/yr downtime).'),
        '1.3.3': ('Cascading Availability in Series', 'Multiplied component availability (A1 × A2); synchronous chains lower reliability.'),
        '1.3.4': ('Redundancy & Parallel Availability', '1 - (1-A)^n availability formula; hot standbys and active replicas increase uptime.'),
        '1.3.5': ('Active-Active Failover', 'All nodes serve live traffic across regions for instant zero-downtime failover.'),
        '1.3.6': ('Active-Passive Failover', 'Standby replica promoted on primary failure with short RTO (~60s).'),
        
        '1.2.1': ('Strong Consistency & Linearizability', 'Every read returns the latest write; requires synchronous coordination.'),
        '1.2.2': ('Eventual Consistency', 'Replicas converge given sufficient time; optimizes write latency and availability.'),
        '1.2.3': ('Read-Your-Writes Guarantee', 'A user always sees their own updates immediately across web and mobile clients.'),
        '1.2.4': ('Causal Consistency', 'Operations that are causally related are seen in the exact same order by all nodes.'),
        '1.2.5': ('Monotonic Reads Guarantee', 'A client never sees an older value after reading a newer value from the store.'),
        '1.2.6': ('Monotonic Writes Guarantee', 'Writes from the same client are serialized and executed in the order submitted.'),
        
        '8.2.1': ('Leader Election', 'Consensus-driven leader election using Raft, Bully algorithm, or ZooKeeper ephemeral nodes.'),
        '8.2.2': ('Heartbeats', 'Periodic health pings between nodes to detect failure, manage leases, and prevent false positive failovers.'),
        '8.2.3': ('Gossip Protocol', 'Nodes share cluster state probabilistically without a central coordinator (Cassandra, Dynamo).'),
        '8.2.4': ('Phi Accrual Failure Detector', 'Probabilistic failure detection measuring heartbeat arrival history to handle network jitter.'),
    }
    
    if cid in CUSTOM:
        return CUSTOM[cid]
        
    # Check for "Step X — Y: Z"
    step_m = re.match(r'^Step\s+(\d+)\s*[—–-]\s*([^:(]+)(?:\s*\(([^)]+)\))?(?::\s*(.+))?$', raw_title, re.IGNORECASE)
    if step_m:
        num, name, time_est, details = step_m.groups()
        step_names = {
            '1': 'Requirements Gathering & Scope',
            '2': 'Scale & Capacity Estimation',
            '3': 'High-Level Architecture Design',
            '4': 'Component Deep Dives & Bottlenecks',
            '5': 'Failure Modes & Scalability Limits'
        }
        title = f"Phase {num}: {step_names.get(num, name.strip())}"
        desc = (details or name).strip()
        if time_est:
            desc = f"({time_est}) {desc}"
        return title, desc
        
    if ' — ' in raw_title or ' – ' in raw_title:
        parts = re.split(r'\s+[—–]\s+', raw_title, maxsplit=1)
        title = parts[0].strip()
        if not desc:
            desc = parts[1].strip()
    elif ' - ' in raw_title:
        parts = raw_title.split(' - ', 1)
        title = parts[0].strip()
        if not desc:
            desc = parts[1].strip()
    elif ': ' in raw_title and not raw_title.lower().startswith('http'):
        parts = raw_title.split(': ', 1)
        if len(parts[0]) <= 40:
            title = parts[0].strip()
            if not desc:
                desc = parts[1].strip()

    # Clean up formatting
    if desc:
        desc = desc[0].upper() + desc[1:]
        if not desc.endswith('.'):
            desc += '.'

    return title, desc

def run():
    html_text = open('system_design.html', encoding='utf-8').read()
    soup = BeautifulSoup(html_text, 'html.parser')
    concepts = soup.find_all('li', attrs={'data-cid': True})
    
    print(f"Processing {len(concepts)} concepts in system_design.html...")
    updated_count = 0
    
    for c in concepts:
        cid = c.get('data-cid')
        cname_div = c.find('div', class_='cname')
        if not cname_div:
            continue
        raw_title = cname_div.text.strip()
        subdiv = c.find('div', style=lambda s: s and 'font-size:11.5px' in s)
        existing_desc = subdiv.text.strip() if subdiv else ''
        
        title, desc = clean_title_and_desc(cid, raw_title, existing_desc)
        
        # Update data-name
        c['data-name'] = title.lower()
        
        # Update or construct title + desc structure
        if subdiv:
            cname_div.string = title
            subdiv.string = desc
        else:
            # Wrap in parent div if not already
            parent = cname_div.parent
            if parent != c and len(parent.find_all(True, recursive=False)) > 1:
                cname_div.string = title
                # add or update desc
                new_sub = soup.new_tag('div')
                new_sub['style'] = 'font-size:11.5px;color:var(--text-faint);margin-top:2px'
                new_sub.string = desc
                parent.append(new_sub)
            else:
                # create container div
                wrapper = soup.new_tag('div')
                new_cname = soup.new_tag('div', attrs={'class': 'cname'})
                new_cname.string = title
                wrapper.append(new_cname)
                if desc:
                    new_sub = soup.new_tag('div')
                    new_sub['style'] = 'font-size:11.5px;color:var(--text-faint);margin-top:2px'
                    new_sub.string = desc
                    wrapper.append(new_sub)
                cname_div.replace_with(wrapper)
                
        # Update res-links
        res_links = c.find('div', class_='res-links')
        if res_links:
            # Check if verified video exists
            vid_info = None
            if cid in EXTRA_VERIFIED_VIDEOS:
                vid_info = EXTRA_VERIFIED_VIDEOS[cid]
            elif cid in CASE_STUDY_MAP and CASE_STUDY_MAP[cid] in concept_videos:
                vid_info = concept_videos[CASE_STUDY_MAP[cid]]
                
            q_term = urllib.parse.quote_plus(f"{title} system design")
            links = res_links.find_all('a')
            for a in links:
                href = a.get('href', '')
                if 'youtube.com' in href or 'video' in a.get('class', []):
                    if vid_info:
                        a['href'] = f"https://www.youtube.com/watch?v={vid_info[0]}"
                        a['title'] = f"{vid_info[1]} — {vid_info[2]}"
                        a.string = "🎬YT✓"
                        a['class'] = ['video', 'verified']
                    else:
                        a['href'] = f"https://www.youtube.com/results?search_query={q_term}"
                        a['title'] = f"YouTube search: {title} system design"
                        a.string = "🎬YT"
                        a['class'] = ['video']
                else:
                    a['href'] = f"https://www.google.com/search?q={q_term}"
                    a['title'] = f"Google search: {title} system design"
                    a.string = "🌐G"
                    a['class'] = []
                
        updated_count += 1
        
    out_html = str(soup)
    # Ensure UTF-8 HTML write
    with open('system_design.html', 'w', encoding='utf-8') as f:
        f.write(out_html)
    print(f"Successfully updated {updated_count} concepts in system_design.html")

if __name__ == '__main__':
    run()
