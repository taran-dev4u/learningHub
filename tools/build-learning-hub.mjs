import fs from "node:fs";
import path from "node:path";
import { gapSections, resourceLibraries } from "./gap-content.mjs";
import { simpleHubHtml } from "./hub-page.mjs";
// build: generates hub pages, gap sections, resource libraries, and search index.

const root = process.cwd();

const sourceDefs = [
  {
    key: "dsa",
    title: "DSA Ultimate Index",
    file: "DSA_Ultimate_Index.html",
    kind: "problem",
    label: "DSA",
    color: "#2f6fdd",
    storage: { done: "dsa_index_solved_v1", bookmark: "dsa_index_bookmark_v1" },
    summary: "Pattern-first LeetCode prep with company tags, lists, notes, and a 14-week plan.",
  },
  {
    key: "sd",
    title: "System Design",
    file: "system_design.html",
    kind: "concept",
    label: "Systems",
    color: "#d84f86",
    storage: { done: "hub_done_sd", bookmark: "hub_bm_sd" },
    summary: "Distributed systems, architecture patterns, reliability, security, and classic designs.",
  },
  {
    key: "cs",
    title: "CS Fundamentals",
    file: "cs_fundamentals.html",
    kind: "concept",
    label: "CS",
    color: "#15875f",
    storage: { done: "hub_done_cs", bookmark: "hub_bm_cs" },
    summary: "Operating systems, networking, databases, concurrency, security, and architecture.",
  },
  {
    key: "bh",
    title: "Behavioral and Leadership",
    file: "behavioral.html",
    kind: "concept",
    label: "Behavioral",
    color: "#c9692d",
    storage: { done: "hub_done_bh", bookmark: "hub_bm_bh" },
    summary: "STAR stories, leadership principles, question categories, and mock strategy.",
  },
  {
    key: "ai",
    title: "AI Engineering",
    file: "ai_engineering.html",
    kind: "concept",
    label: "AI",
    color: "#7b61d8",
    storage: { done: "hub_done_ai", bookmark: "hub_bm_ai" },
    summary: "LLM fundamentals, RAG, agents, evals, fine-tuning, ML, deep learning, and MLOps.",
  },
  {
    key: "cloud",
    title: "Cloud - AWS and Azure",
    file: "cloud_aws_azure.html",
    kind: "concept",
    label: "Cloud",
    color: "#0786a3",
    storage: { done: "hub_done_cloud", bookmark: "hub_bm_cloud" },
    summary: "AWS and Azure service mapping, cloud foundations, IaC, observability, and interview Q&A.",
  },
];

const roadmap = [
  {
    phase: "Weeks 1-2",
    title: "Baseline and tooling",
    focus: "Git, CLI fluency, language syntax, Big-O, debugging, and test hygiene.",
    domains: ["DSA", "CS"],
  },
  {
    phase: "Weeks 3-8",
    title: "Core coding interviews",
    focus: "Arrays, strings, two pointers, sliding window, stacks, queues, trees, graphs, and recursion.",
    domains: ["DSA"],
  },
  {
    phase: "Weeks 9-11",
    title: "Advanced problem solving",
    focus: "Dynamic programming, heaps, binary search, tries, intervals, greedy, and graph variants.",
    domains: ["DSA", "CS"],
  },
  {
    phase: "Weeks 10-13",
    title: "Systems foundation",
    focus: "HTTP, DNS, load balancers, databases, caching, queues, sharding, consistency, and reliability.",
    domains: ["System Design", "CS"],
  },
  {
    phase: "Weeks 12-14",
    title: "Cloud and production",
    focus: "IAM, networking, storage, compute, serverless, observability, IaC, and deployment trade-offs.",
    domains: ["Cloud", "System Design"],
  },
  {
    phase: "Weeks 13-15",
    title: "Role specialization",
    focus: "AI engineering, RAG, agents, evals, MLOps, or deeper backend/frontend tracks based on target roles.",
    domains: ["AI", "Cloud"],
  },
  {
    phase: "Every week",
    title: "Behavioral and mocks",
    focus: "Prepare STAR stories, leadership examples, failure stories, conflict stories, and live mock interviews.",
    domains: ["Behavioral"],
  },
];

const additions = [
  {
    area: "Web and frontend fundamentals",
    why: "Useful for full-stack roles and missing from the original folder as a dedicated track.",
    topics: ["HTML semantics", "CSS layout", "JavaScript runtime", "accessibility", "React fundamentals", "browser performance"],
    resources: [
      ["MDN Web Docs", "https://developer.mozilla.org/en-US/docs/Learn"],
      ["web.dev Learn", "https://web.dev/learn"],
      ["React Learn", "https://react.dev/learn"],
    ],
  },
  {
    area: "Backend API engineering",
    why: "Bridges DSA/system design with real implementation work.",
    topics: ["REST", "GraphQL", "auth sessions", "pagination", "idempotency", "validation", "testing APIs"],
    resources: [
      ["Microsoft REST API Guidelines", "https://github.com/microsoft/api-guidelines"],
      ["Google API Design Guide", "https://cloud.google.com/apis/design"],
      ["FastAPI Tutorial", "https://fastapi.tiangolo.com/tutorial/"],
    ],
  },
  {
    area: "Testing and quality",
    why: "Interviewers increasingly ask how you ship safely, not just how you code.",
    topics: ["unit tests", "integration tests", "contract tests", "test doubles", "CI", "observability-driven debugging"],
    resources: [
      ["Google Testing Blog", "https://testing.googleblog.com/"],
      ["Martin Fowler - Testing", "https://martinfowler.com/testing/"],
      ["Playwright Docs", "https://playwright.dev/docs/intro"],
    ],
  },
  {
    area: "Security and identity depth",
    why: "Security appears in system design, cloud, and backend interviews.",
    topics: ["OAuth2", "OIDC", "JWT", "CSRF", "XSS", "SSRF", "secrets", "threat modeling"],
    resources: [
      ["OWASP Top 10", "https://owasp.org/www-project-top-ten/"],
      ["OAuth 2.0 Simplified", "https://www.oauth.com/"],
      ["PortSwigger Web Security Academy", "https://portswigger.net/web-security"],
    ],
  },
  {
    area: "Portfolio projects",
    why: "A project converts the roadmap into something you can explain with ownership.",
    topics: ["one CRUD app", "one distributed feature", "one cloud deployment", "one AI/RAG feature", "one postmortem"],
    resources: [
      ["GitHub Skills", "https://skills.github.com/"],
      ["12 Factor App", "https://12factor.net/"],
      ["OpenTelemetry Docs", "https://opentelemetry.io/docs/"],
    ],
  },
];

const coverageBySource = {
  dsa: {
    title: "DSA Coverage Check",
    source: "NeetCode / Striver-style pattern coverage",
    notes: [
      "Keep the 609-problem pattern index as the primary practice map.",
      "Revisit duplicate placements intentionally; duplicated problems should teach multiple patterns.",
      "Prioritize core patterns before advanced/niche patterns unless a target company requires them.",
    ],
    topics: [
      "Pattern recognition drills",
      "Complexity trade-offs",
      "Edge-case checklist",
      "Mock interview communication",
      "Re-solving weak bookmarked problems",
    ],
    resources: [
      ["NeetCode Roadmap", "https://neetcode.io/roadmap"],
      ["Striver A2Z DSA Sheet", "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/"],
      ["CP-Algorithms", "https://cp-algorithms.com/"],
    ],
  },
  sd: {
    title: "System Design Coverage Check",
    source: "roadmap.sh System Design + System Design Primer + GeeksforGeeks System Design Tutorial",
    notes: [
      "Make trade-offs explicit: consistency, latency, cost, availability, and operability.",
      "Use classic designs as integration practice, not memorized templates.",
      "Add security, observability, and failure-mode reasoning to every design.",
    ],
    topics: [
      "Capacity estimation",
      "HLD vs LLD boundaries",
      "Functional and non-functional requirements",
      "UML and HLD diagrams",
      "CDNs and edge caching",
      "Proxies and API gateways",
      "Testing and CI/CD",
      "Cost estimation",
      "Search systems",
      "Observability and SLOs",
      "Threat modeling",
    ],
    resources: [
      ["roadmap.sh System Design", "https://roadmap.sh/system-design"],
      ["System Design Primer", "https://github.com/donnemartin/system-design-primer"],
      ["GeeksforGeeks System Design Tutorial", "https://www.geeksforgeeks.org/system-design/system-design-tutorial/"],
      ["Google SRE Book", "https://sre.google/sre-book/table-of-contents/"],
    ],
  },
  cs: {
    title: "CS Fundamentals Coverage Check",
    source: "roadmap.sh Computer Science + standard interview foundations",
    notes: [
      "Keep OS, networking, DB, concurrency, security, and architecture as the required core.",
      "Add compiler/runtime and distributed-systems prerequisites as review topics.",
      "Treat CS fundamentals as support for system design and debugging interviews.",
    ],
    topics: [
      "Compilers and interpreters",
      "Runtime and garbage collection",
      "Serialization formats",
      "Distributed systems basics",
      "Testing fundamentals",
      "Performance profiling",
    ],
    resources: [
      ["roadmap.sh Computer Science", "https://roadmap.sh/computer-science"],
      ["MIT 6.828 Operating Systems", "https://pdos.csail.mit.edu/6.828/"],
      ["Beej's Guide to Network Programming", "https://beej.us/guide/bgnet/"],
    ],
  },
  bh: {
    title: "Behavioral Coverage Check",
    source: "STAR interview prep + leadership story coverage",
    notes: [
      "Prepare reusable stories that can flex across companies and question wording.",
      "Every story should include stakes, action, measurable result, and reflection.",
      "Keep a short answer and a deeper version for each major story.",
    ],
    topics: [
      "Ambiguity",
      "Ownership",
      "Conflict",
      "Failure",
      "Mentoring",
      "Prioritization",
      "Customer impact",
      "Technical judgment",
    ],
    resources: [
      ["Amazon Leadership Principles", "https://www.amazon.jobs/content/en/our-workplace/leadership-principles"],
      ["Google Interview Prep", "https://www.google.com/about/careers/applications/interview-tips/"],
      ["STAR Method Guide", "https://www.themuse.com/advice/star-interview-method"],
    ],
  },
  ai: {
    title: "AI Engineering Coverage Check",
    source: "roadmap.sh AI Engineer + OpenAI Cookbook + production LLM practice",
    notes: [
      "Focus on building reliable AI systems with existing models before training from scratch.",
      "Pair every RAG/agent technique with evals, observability, and failure analysis.",
      "Track safety, cost, latency, and quality as production constraints.",
    ],
    topics: [
      "Structured outputs",
      "Function/tool calling",
      "RAG evaluation",
      "Agent reliability",
      "Prompt/version management",
      "LLM observability",
      "Safety and guardrails",
      "Cost and latency optimization",
    ],
    resources: [
      ["roadmap.sh AI Engineer", "https://roadmap.sh/ai-engineer"],
      ["OpenAI Cookbook", "https://cookbook.openai.com/"],
      ["Hugging Face NLP Course", "https://huggingface.co/learn/nlp-course"],
    ],
  },
  cloud: {
    title: "Cloud Coverage Check",
    source: "roadmap.sh AWS + AWS/Azure Well-Architected guidance",
    notes: [
      "Keep AWS and Azure mappings side-by-side for interview recall.",
      "Add reliability, security, cost, and operational excellence to each service family.",
      "Practice explaining why a managed service is chosen, not only what it is called.",
    ],
    topics: [
      "Well-Architected pillars",
      "Landing zones",
      "Cost governance",
      "Backup and disaster recovery",
      "Secrets management",
      "Container platforms",
      "Zero-trust networking",
      "Cloud migration patterns",
    ],
    resources: [
      ["roadmap.sh AWS", "https://roadmap.sh/aws"],
      ["AWS Well-Architected Framework", "https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html"],
      ["Azure Well-Architected Framework", "https://learn.microsoft.com/en-us/azure/well-architected/"],
    ],
  },
};

const gfgSystemDesignOutline = [
  {
    group: "Basics and Requirements",
    status: "Strengthen",
    topics: [
      "System design introduction",
      "High-level design vs low-level design",
      "Functional requirements",
      "Non-functional requirements",
      "Requirements gathering",
      "System life cycle / SDLC",
      "System analysis vs system design",
      "Core terminology and objectives",
    ],
  },
  {
    group: "High-Level Design",
    status: "Covered plus diagrams",
    topics: [
      "HLD components and interactions",
      "HLD diagrams",
      "Activity diagrams",
      "Monolithic architecture",
      "Microservices architecture",
      "Event-driven architecture",
      "Serverless architecture",
      "Stateful vs stateless systems",
      "Pub/Sub architecture",
    ],
  },
  {
    group: "Scalability and Capacity",
    status: "Covered",
    topics: [
      "Horizontal scaling",
      "Vertical scaling",
      "Choosing a scaling approach",
      "Scalability bottlenecks",
      "Highly scalable system design",
      "Capacity estimation",
    ],
  },
  {
    group: "Databases and Storage",
    status: "Covered",
    topics: [
      "Database design",
      "SQL vs NoSQL selection",
      "File vs database storage",
      "Block storage",
      "Object storage",
      "File storage",
      "Database replication",
      "Replication types",
      "Database sharding",
      "Data partitioning",
      "Normalization",
      "Denormalization",
      "SQL query optimization",
      "Redis",
    ],
  },
  {
    group: "Reliability Qualities",
    status: "Covered",
    topics: [
      "Availability",
      "High availability",
      "Consistency",
      "Consistency patterns",
      "CAP theorem",
      "Reliability",
      "Fault tolerance",
      "Maintainability",
    ],
  },
  {
    group: "Traffic and Performance",
    status: "Covered",
    topics: [
      "Load balancers",
      "Load balancer types",
      "Load balancing algorithms",
      "Concurrency and parallelism",
      "Stateful vs stateless load balancing",
      "Load balancing vs failover",
      "Consistent hashing",
      "Latency and throughput",
      "Caching",
      "Distributed cache",
      "Cache eviction policies",
      "Cold and warm cache",
      "Edge caching",
      "CDN vs edge server",
    ],
  },
  {
    group: "Communication and Integration",
    status: "Covered",
    topics: [
      "API gateway",
      "Message queues",
      "Rate limiting",
      "Rate limiting algorithms",
      "Communication protocols",
      "DNS",
      "DNS caching",
      "TTL",
      "CDN",
      "Proxies",
      "Forward proxy vs reverse proxy",
      "Web server vs application server",
      "Short polling",
      "Long polling",
      "WebSockets",
    ],
  },
  {
    group: "Event-Driven Systems",
    status: "Covered",
    topics: [
      "Event sourcing",
      "Event sourcing vs event streaming",
      "Event-driven APIs",
      "Event-driven error handling",
      "State restore after message-driven failure",
      "Cloud-native event-driven patterns",
      "Request-driven vs event-driven microservices",
      "Message-driven vs event-driven architecture",
    ],
  },
  {
    group: "Testing and Delivery",
    status: "Add",
    topics: [
      "Unit testing",
      "Integration testing",
      "Load testing",
      "Stress testing",
      "CI/CD pipelines",
      "Release safety checks",
    ],
  },
  {
    group: "Security and Recovery",
    status: "Strengthen",
    topics: [
      "Security measures",
      "Authentication",
      "Authorization",
      "SSL/TLS",
      "Secure SDLC",
      "Data backup",
      "Disaster recovery",
      "Secure distributed communication",
    ],
  },
  {
    group: "Distributed Systems",
    status: "Covered",
    topics: [
      "Distributed system introduction",
      "Consensus algorithms",
      "Distributed tracing",
      "Distributed design issues",
      "Secure communication in distributed systems",
    ],
  },
  {
    group: "Cost and Optimization",
    status: "Add",
    topics: [
      "Software cost estimation",
      "Performance optimization techniques",
      "Cost vs performance trade-offs",
    ],
  },
  {
    group: "Low-Level Design",
    status: "Add",
    topics: [
      "OOP concepts",
      "OOAD",
      "Modularity and interfaces",
      "HLD vs LLD differences",
      "SOLID",
      "DRY",
      "KISS",
      "YAGNI",
      "UML diagrams",
      "Creational design patterns",
      "Structural design patterns",
      "Behavioral design patterns",
    ],
  },
  {
    group: "Interview Practice",
    status: "Strengthen",
    topics: [
      "Cracking the system design round",
      "LLD interview approach",
      "Common system design concepts",
      "Object-oriented design interview steps",
      "Common design interview questions",
      "Design Dropbox / Google Drive",
      "Design Twitter / X",
      "Design Netflix / YouTube",
      "Design Uber / rideshare",
      "Design BookMyShow / ticketing",
      "Design Facebook Messenger / chat",
    ],
  },
];

const gfgSystemDesignPriorityGaps = [
  "HLD vs LLD distinction and when to switch levels",
  "Functional vs non-functional requirement checklist",
  "System life cycle / SDLC and requirements gathering",
  "HLD diagrams, activity diagrams, and UML diagram practice",
  "LLD foundations: OOP, OOAD, interfaces, SOLID, DRY, KISS, YAGNI",
  "Testing and delivery: unit, integration, load, stress, CI/CD",
  "Cost estimation and cost-vs-performance trade-offs",
  "Backup and disaster recovery planning",
  "Ticket booking / BookMyShow and Messenger-style design prompts",
];

const gfgSystemDesignResources = [
  ["GFG System Design Tutorial", "https://www.geeksforgeeks.org/system-design/system-design-tutorial/"],
  ["GFG HLD", "https://www.geeksforgeeks.org/system-design/what-is-high-level-design-learn-system-design/"],
  ["GFG LLD", "https://www.geeksforgeeks.org/system-design/what-is-low-level-design-or-lld-learn-system-design/"],
  ["GFG Functional vs Non-Functional Requirements", "https://www.geeksforgeeks.org/software-engineering/functional-vs-non-functional-requirements/"],
  ["GFG UML Diagrams", "https://www.geeksforgeeks.org/system-design/unified-modeling-language-uml-introduction/"],
  ["GFG System Design Interview Guide", "https://www.geeksforgeeks.org/interview-experiences/how-to-crack-system-design-round-in-interviews/"],
];

const gfgSystemDesignLinks = [
  ["System Design Tutorial", "https://www.geeksforgeeks.org/system-design/system-design-tutorial/"],
  ["HLD", "https://www.geeksforgeeks.org/system-design/what-is-high-level-design-learn-system-design/"],
  ["LLD", "https://www.geeksforgeeks.org/system-design/what-is-low-level-design-or-lld-learn-system-design/"],
  ["Functional and Non Functional", "https://www.geeksforgeeks.org/software-engineering/functional-vs-non-functional-requirements/"],
  ["Life Cycle", "https://www.geeksforgeeks.org/system-design/system-design-life-cycle-phases-models-and-use-cases/"],
  ["Design Patterns", "https://www.geeksforgeeks.org/system-design/software-design-patterns/"],
  ["UML Diagrams", "https://www.geeksforgeeks.org/system-design/unified-modeling-language-uml-introduction/"],
  ["System Design Interview Guide", "https://www.geeksforgeeks.org/interview-experiences/how-to-crack-system-design-round-in-interviews/"],
  ["Scalability", "https://www.geeksforgeeks.org/system-design/what-is-scalability/"],
  ["Databases", "https://www.geeksforgeeks.org/system-design/complete-reference-to-databases-in-designing-systems/"],
  ["Software Engineering", "https://www.geeksforgeeks.org/software-engineering/software-engineering/"],
  ["System Design Introduction - HLD & LLD", "https://www.geeksforgeeks.org/system-design/getting-started-with-system-design/"],
  ["High Level Design Diagram", "https://www.geeksforgeeks.org/system-design/how-to-draw-high-level-design-diagram/"],
  ["Monolithic Architecture", "https://www.geeksforgeeks.org/system-design/monolithic-architecture-system-design/"],
  ["Microservices", "https://www.geeksforgeeks.org/system-design/microservices/"],
  ["Monolithic Vs Microservices Architecture", "https://www.geeksforgeeks.org/software-engineering/monolithic-vs-microservices-architecture/"],
  ["Event-Driven Architecture", "https://www.geeksforgeeks.org/system-design/event-driven-architecture-system-design/"],
  ["Event-Driven Architecture in an E-commerce System", "https://www.geeksforgeeks.org/system-design/event-driven-architecture-in-an-e-commerce-system/"],
  ["Serverless Architecture", "https://www.geeksforgeeks.org/system-design/serverless-architectures/"],
  ["Stateless and Stateful Systems", "https://www.geeksforgeeks.org/system-design/stateless-and-stateful-systems-in-system-design/"],
  ["Stateful Vs Stateless Architecture", "https://www.geeksforgeeks.org/system-design/stateful-vs-stateless-architecture/"],
  ["Pub/Sub Architecture", "https://www.geeksforgeeks.org/system-design/what-is-pub-sub/"],
  ["Horizontal and Vertical Scaling", "https://www.geeksforgeeks.org/system-design/system-design-horizontal-and-vertical-scaling/"],
  ["Choosing the Right Scalability Approach", "https://www.geeksforgeeks.org/system-design/which-scalability-approach-is-right-for-our-application-system-design/"],
  ["Designing Highly Scalable Systems", "https://www.geeksforgeeks.org/system-design/guide-for-designing-highly-scalable-systems/"],
  ["Primary Scalability Bottlenecks", "https://www.geeksforgeeks.org/system-design/primary-bottlenecks-that-hurt-the-scalability-of-an-application-system-design/"],
  ["Types of Database", "https://www.geeksforgeeks.org/system-design/types-of-databases-in-system-design/"],
  ["Choosing a Database - SQL or NoSQL", "https://www.geeksforgeeks.org/system-design/which-database-to-choose-while-designing-a-system-sql-or-nosql/"],
  ["File and Database Storage Systems", "https://www.geeksforgeeks.org/system-design/file-and-database-storage-systems-in-system-design/"],
  ["Database Replication", "https://www.geeksforgeeks.org/system-design/database-replication-and-their-types-in-system-design/"],
  ["Types of Database Replication", "https://www.geeksforgeeks.org/system-design/types-of-database-replication-system-design/"],
  ["Database Sharding", "https://www.geeksforgeeks.org/system-design/database-sharding-a-system-design-concept/"],
  ["Data Partitioning", "https://www.geeksforgeeks.org/system-design/data-partitioning-techniques/"],
  ["Block, Object, and File Storage", "https://www.geeksforgeeks.org/system-design/block-object-and-file-storage-in-cloud-with-difference/"],
  ["Intro to Redis", "https://www.geeksforgeeks.org/system-design/introduction-to-redis-server/"],
  ["Availability", "https://www.geeksforgeeks.org/system-design/availability-in-system-design/"],
  ["High Availability", "https://www.geeksforgeeks.org/system-design/what-is-high-availability-in-system-design/"],
  ["Consistency", "https://www.geeksforgeeks.org/system-design/consistency-in-system-design/"],
  ["Consistency Patterns", "https://www.geeksforgeeks.org/system-design/consistency-patterns/"],
  ["CAP Theorem", "https://www.geeksforgeeks.org/system-design/cap-theorem-in-system-design/"],
  ["Reliability", "https://www.geeksforgeeks.org/system-design/reliability-in-system-design/"],
  ["Fault Tolerance", "https://www.geeksforgeeks.org/system-design/fault-tolerance-in-system-design/"],
  ["Maintainability", "https://www.geeksforgeeks.org/system-design/maintainability-in-system-design/"],
  ["Load Balancer", "https://www.geeksforgeeks.org/system-design/what-is-load-balancer-system-design/"],
  ["Types of Load Balancer", "https://www.geeksforgeeks.org/system-design/types-of-load-balancer/"],
  ["Load Balancing Algorithms", "https://www.geeksforgeeks.org/system-design/load-balancing-algorithms/"],
  ["Stateless Vs Stateful Load Balancing", "https://www.geeksforgeeks.org/system-design/stateless-vs-stateful-load-balancing/"],
  ["Load Balancing Vs Failover", "https://www.geeksforgeeks.org/system-design/load-balancing-vs-failover/"],
  ["Consistent Hashing", "https://www.geeksforgeeks.org/system-design/consistent-hashing/"],
  ["Latency and Throughput", "https://www.geeksforgeeks.org/system-design/latency-in-system-design/"],
  ["Caching", "https://www.geeksforgeeks.org/system-design/caching-system-design-concept-for-beginners/"],
  ["Distributed Cache", "https://www.geeksforgeeks.org/system-design/what-is-a-distributed-cache/"],
  ["Design Distributed Cache", "https://www.geeksforgeeks.org/system-design/design-distributed-cache-system-design/"],
  ["Edge Caching", "https://www.geeksforgeeks.org/system-design/edge-caching-system-design/"],
  ["CDN Vs Edge Server", "https://www.geeksforgeeks.org/system-design/cdn-vs-edge-server-system-design/"],
  ["Cache Eviction Policies", "https://www.geeksforgeeks.org/system-design/cache-eviction-policies-system-design/"],
  ["Cold and Warm Cache", "https://www.geeksforgeeks.org/system-design/cold-and-warm-cache-in-system-design/"],
  ["API Gateway", "https://www.geeksforgeeks.org/system-design/what-is-api-gateway-system-design/"],
  ["Message Queues", "https://www.geeksforgeeks.org/system-design/message-queues-system-design/"],
  ["Rate Limiting", "https://www.geeksforgeeks.org/system-design/rate-limiting-in-system-design/"],
  ["Rate Limiting Algorithm", "https://www.geeksforgeeks.org/system-design/rate-limiting-algorithms-system-design/"],
  ["Communication Protocols", "https://www.geeksforgeeks.org/system-design/communication-protocols-in-system-design/"],
  ["Content Delivery Network", "https://www.geeksforgeeks.org/system-design/what-is-content-delivery-networkcdn-in-system-design/"],
  ["Proxies", "https://www.geeksforgeeks.org/system-design/network-protocols-and-proxies-in-system-design/"],
  ["Forward Proxy vs Reverse Proxy", "https://www.geeksforgeeks.org/system-design/difference-between-forward-proxy-and-reverse-proxy/"],
  ["Web and Application Server", "https://www.geeksforgeeks.org/system-design/web-server-proxies-and-their-role-in-designing-systems/"],
  ["Event Sourcing Pattern", "https://www.geeksforgeeks.org/system-design/event-sourcing-pattern/"],
  ["Event Sourcing Vs Event Streaming", "https://www.geeksforgeeks.org/system-design/event-sourcing-vs-event-streaming-in-system-design/"],
  ["Event-Driven APIs", "https://www.geeksforgeeks.org/system-design/event-driven-apis-in-microservice-architectures/"],
  ["Event-Driven Error Handling", "https://www.geeksforgeeks.org/system-design/error-handling-in-event-driven-architecture/"],
  ["Restore State After Event Failure", "https://www.geeksforgeeks.org/system-design/how-to-restore-state-in-an-event-based-message-driven-microservice-architecture-on-failure-scenario/"],
  ["Cloud-Native Event Patterns", "https://www.geeksforgeeks.org/system-design/event-driven-architecture-patterns-in-cloud-native-applications/"],
  ["Request-driven Vs Event-driven Microservices", "https://www.geeksforgeeks.org/system-design/request-driven-vs-event-driven-microservices/"],
  ["Event-Driven Vs Microservices", "https://www.geeksforgeeks.org/system-design/event-driven-architecture-vs-microservices-architecture/"],
  ["Message-Driven Vs Event-Driven", "https://www.geeksforgeeks.org/system-design/message-driven-architecture-vs-event-driven-architecture/"],
  ["CI/CD Pipeline", "https://www.geeksforgeeks.org/system-design/cicd-pipeline-system-design/"],
  ["Security Measures", "https://www.geeksforgeeks.org/system-design/essential-security-measures-in-system-design/"],
  ["Distributed Tracing", "https://www.geeksforgeeks.org/system-design/distributed-tracing-system-design/"],
  ["Distributed System Design Issues", "https://www.geeksforgeeks.org/system-design/design-issues-of-distributed-system/"],
  ["Software Cost Estimation", "https://www.geeksforgeeks.org/software-engineering/software-cost-estimation/"],
  ["Performance Optimization Techniques", "https://www.geeksforgeeks.org/system-design/optimization-techniques-for-system-design/"],
  ["Cost Vs Performance", "https://www.geeksforgeeks.org/system-design/cost-vs-performance/"],
  ["OOP Concepts", "https://www.geeksforgeeks.org/system-design/object-oriented-programingoop-concepts-for-designing-sytems/"],
  ["Modularity and Interfaces", "https://www.geeksforgeeks.org/system-design/inroduction-to-modularity-and-interfaces-in-system-design/"],
  ["HLD vs LLD Difference", "https://www.geeksforgeeks.org/system-design/difference-between-high-level-design-and-low-level-design/"],
  ["SOLID Principles", "https://www.geeksforgeeks.org/system-design/solid-principle-in-programming-understand-with-real-life-examples/"],
  ["DRY Principle", "https://www.geeksforgeeks.org/software-engineering/dont-repeat-yourselfdry-in-software-development/"],
  ["KISS Principle", "https://www.geeksforgeeks.org/software-engineering/kiss-principle-in-software-development/"],
  ["YAGNI Principle", "https://www.geeksforgeeks.org/software-engineering/what-is-yagni-principle-you-arent-gonna-need-it/"],
  ["Common Design Interview Questions", "https://www.geeksforgeeks.org/system-design/most-commonly-asked-system-design-interview-problems-questions/"],
  ["Cracking System Design Round", "https://www.geeksforgeeks.org/system-design/how-to-crack-system-design-round-in-interviews/"],
  ["Low-Level Design Interview Tips", "https://www.geeksforgeeks.org/system-design/5-tips-to-crack-low-level-system-design-interviews/"],
  ["Common System Design Concepts", "https://www.geeksforgeeks.org/system-design/5-common-system-design-concepts-for-interview-preparation/"],
  ["Object-Oriented Design Interview Steps", "https://www.geeksforgeeks.org/interview-experiences/steps-to-approach-object-oriented-design-questions-in-interview/"],
  ["Components", "https://www.geeksforgeeks.org/system-design/what-are-the-components-of-system-design/"],
  ["Goals and Objectives", "https://www.geeksforgeeks.org/system-design/goals-and-objectives-of-system-design/"],
  ["Importance of System Design", "https://www.geeksforgeeks.org/system-design/why-is-it-important-to-learn-system-design/"],
  ["Key Concepts and Terminologies", "https://www.geeksforgeeks.org/system-design/important-key-concepts-and-terminologies-learn-system-design/"],
  ["Advantages", "https://www.geeksforgeeks.org/system-design/advantages-of-system-design/"],
  ["Monolithic vs Distributed Systems", "https://www.geeksforgeeks.org/system-design/analysis-of-monolithic-and-distributed-systems-learn-system-design/"],
  ["Requirements Gathering", "https://www.geeksforgeeks.org/system-design/what-is-requirements-gathering-process/"],
  ["System Analysis vs System Design", "https://www.geeksforgeeks.org/system-design/system-analysis-vs-system-design/"],
  ["Capacity Estimation", "https://www.geeksforgeeks.org/system-design/capacity-estimation-in-systems-design/"],
  ["Answering System Design Problems", "https://www.geeksforgeeks.org/system-design/how-to-answer-a-system-design-interview-problem/"],
  ["Activity Diagrams", "https://www.geeksforgeeks.org/system-design/unified-modeling-language-uml-activity-diagrams/"],
  ["Authentication vs Authorization", "https://www.geeksforgeeks.org/system-design/difference-between-authentication-and-authorization-in-lld-system-design/"],
  ["OOAD", "https://www.geeksforgeeks.org/software-engineering/object-oriented-analysis-and-design/"],
  ["DSA for System Design", "https://www.geeksforgeeks.org/system-design/data-structures-and-algorithms-for-system-design/"],
  ["Containerization Architecture", "https://www.geeksforgeeks.org/system-design/containerization-architecture-in-system-design/"],
  ["Prepare for LLD Interviews", "https://www.geeksforgeeks.org/system-design/how-to-prepare-for-low-level-design-interviews/"],
  ["Creational Design Patterns", "https://www.geeksforgeeks.org/system-design/creational-design-pattern/"],
  ["Structural Design Patterns", "https://www.geeksforgeeks.org/system-design/structural-design-patterns/"],
  ["Behavioral Design Patterns", "https://www.geeksforgeeks.org/system-design/behavioral-design-patterns/"],
  ["Design Patterns Cheat Sheet", "https://www.geeksforgeeks.org/system-design/design-patterns-cheat-sheet-when-to-use-which-design-pattern/"],
  ["Interview Q&A", "https://www.geeksforgeeks.org/system-design/top-10-system-design-interview-questions-and-answers/"],
];

const designGurusSystemDesignLinks = [
  ["Course home", "https://www.designgurus.io/course/grokking-the-system-design-interview"],
  ["What is a system design interview?", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/what-is-a-system-design-interview"],
  ["Functional vs non-functional requirements", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/functional-vs-nonfunctional-requirements"],
  ["Back-of-the-envelope estimations", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/what-are-backoftheenvelope-estimations"],
  ["System design basics", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/system-design-basics"],
  ["Distributed system characteristics", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/key-characteristics-of-distributed-systems"],
  ["Load balancing", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/load-balancing"],
  ["Load balancing algorithms", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/load-balancing-algorithms"],
  ["Caching", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/caching"],
  ["Data partitioning", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/data-partitioning"],
  ["Indexes", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/indexes"],
  ["Proxies", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/proxies"],
  ["Redundancy and replication", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/redundancy-and-replication"],
  ["SQL vs NoSQL", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/sql-vs-nosql"],
  ["CAP theorem", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/cap-theorem"],
  ["PACELC theorem", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/pacelc-theorem-new"],
  ["Consistent hashing", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/consistent-hashing-new"],
  ["Long polling vs WebSockets vs SSE", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/longpolling-vs-websockets-vs-serversent-events"],
  ["Bloom filters", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/bloom-filters"],
  ["Quorum", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/quorum-new"],
  ["Leader and follower", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/leader-and-follower-new"],
  ["Heartbeat", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/heartbeat-new"],
  ["Checksum", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/checksum-new"],
  ["Trade-offs", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/importance-of-discussing-tradeoffs"],
  ["Strong vs eventual consistency", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/strong-vs-eventual-consistency"],
  ["Latency vs throughput", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/latency-vs-throughput"],
  ["ACID vs BASE", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/acid-vs-base-properties-in-databases"],
  ["Read-through vs write-through cache", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/readthrough-vs-writethrough-cache"],
  ["Batch vs stream processing", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/batch-processing-vs-stream-processing"],
  ["Load balancer vs API gateway", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/load-balancer-vs-api-gateway"],
  ["Proxy vs reverse proxy", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/proxy-vs-reverse-proxy"],
  ["REST vs RPC", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/rest-vs-rpc"],
  ["Polling vs long polling vs webhooks", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/polling-vs-longpolling-vs-webhooks"],
  ["CDN vs direct serving", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/cdn-usage-vs-direct-server-serving"],
  ["Serverless vs server-based", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/serverless-architecture-vs-traditional-serverbased"],
  ["Stateful vs stateless architecture", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/stateful-vs-stateless-architecture"],
  ["Token bucket vs leaky bucket", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/token-bucket-vs-leaky-bucket"],
  ["Read-heavy vs write-heavy systems", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/read-heavy-vs-write-heavy-system"],
  ["Step-by-step interview guide", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/system-design-interviews-a-step-by-step-guide"],
  ["System design master template", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/system-design-master-template"],
  ["Design URL shortener", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/designing-a-url-shortening-service-like-tinyurl"],
  ["Design Pastebin", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/designing-pastebin"],
  ["Design Instagram", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/designing-instagram"],
  ["Design Dropbox", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/designing-dropbox"],
  ["Design Facebook Messenger", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/designing-facebook-messenger"],
  ["Design Twitter", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/designing-twitter"],
  ["Design YouTube or Netflix", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/designing-youtube-or-netflix"],
  ["Design Typeahead", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/designing-typeahead-suggestion"],
  ["Design API rate limiter", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/designing-an-api-rate-limiter"],
  ["Design Twitter search", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/designing-twitter-search"],
  ["Design web crawler", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/designing-a-web-crawler"],
  ["Design Facebook newsfeed", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/designing-facebooks-newsfeed"],
  ["Design Yelp / Nearby Friends", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/designing-yelp-or-nearby-friends"],
  ["Design Uber backend", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/designing-uber-backend"],
  ["Design Ticketmaster", "https://www.designgurus.io/course-play/grokking-the-system-design-interview/doc/designing-ticketmaster"],
];

const thitaHldOutline = [
  "Foundations: 45-minute framework, estimation, CAP and consistency, availability and SLAs",
  "Networking and APIs: protocols, API design, gRPC, advanced API patterns, chat design",
  "Databases: SQL vs NoSQL, replication, sharding, indexing, storage, LSM trees, WAL",
  "Caching: cache strategy, cache failure modes, multi-layer caching, rate limiter and distributed cache designs",
  "Queues and async: queue fundamentals, delivery guarantees, idempotency, event-driven patterns, job scheduler design",
  "Scalability: consistent hashing, scaling reads vs writes, service architecture, feed design",
  "Coordination and transactions: consensus, locks, distributed transactions, Raft, gossip, quorum, stock exchange design",
  "Search, geo and aggregation: search, geospatial systems, real-time aggregation, Elasticsearch, maps and leaderboard designs",
];

const thitaLldOutline = [
  "OOP foundations and class design",
  "Strategy and factory patterns",
  "State pattern and state machines",
  "Observer, decorator and behavioral patterns",
  "Concurrency patterns",
  "Machine coding and interview execution",
  "Foundational case studies",
  "Applied case studies",
];

const thitaBehavioralPatterns = [
  ["STAR Method", ["Situation Examples", "Task Breakdown", "Action Planning", "Result Measurement"]],
  ["Conflict Resolution", ["Identifying Issues", "Stakeholder Management", "Negotiation Tactics", "Resolution Follow-up"]],
  ["Team Leadership", ["Team Building", "Motivation Techniques", "Delegation Skills", "Performance Management"]],
  ["Project Management", ["Planning & Scoping", "Risk Management", "Timeline Management", "Cross-functional Coordination"]],
  ["Communication", ["Stakeholder Communication", "Technical Explanation", "Active Listening", "Feedback Delivery"]],
  ["Problem Solving", ["Root Cause Analysis", "Creative Solutions", "Data-Driven Decisions", "Implementation Strategy"]],
  ["Adaptability", ["Change Management", "Learning Agility", "Resilience Building", "Flexibility in Approach"]],
  ["Cultural Fit", ["Company Values Alignment", "Team Dynamics", "Work Style Preferences", "Growth Mindset"]],
];

const thitaDataScienceOutline = [
  "Business Analytics and Metrics",
  "Data Manipulation and Preprocessing",
  "Deep Learning Fundamentals",
  "Exploratory Data Analysis",
  "Feature Selection and Dimensionality Reduction",
  "Full Pattern Problem Practice",
  "Model Selection and Validation",
  "Natural Language Processing",
  "Statistics and Probability Fundamentals",
  "Supervised Learning - Classification",
  "Supervised Learning - Regression",
  "Time Series Analysis",
  "Unsupervised Learning",
];

const dataScienceDirectResources = [
  ["Thita Data Science Learning Path", "https://thita.ai/dashboard/learning-path/data-science"],
  ["Kaggle Learn Python", "https://www.kaggle.com/learn/python"],
  ["Kaggle Learn Pandas", "https://www.kaggle.com/learn/pandas"],
  ["Kaggle Learn Data Visualization", "https://www.kaggle.com/learn/data-visualization"],
  ["Kaggle Intro to Machine Learning", "https://www.kaggle.com/learn/intro-to-machine-learning"],
  ["Google Machine Learning Crash Course", "https://developers.google.com/machine-learning/crash-course"],
  ["scikit-learn User Guide", "https://scikit-learn.org/stable/user_guide.html"],
  ["TensorFlow Tutorials", "https://www.tensorflow.org/tutorials"],
  ["Hugging Face NLP Course", "https://huggingface.co/learn/nlp-course"],
];

function read(file) {
  return fs.readFileSync(path.join(root, file), "utf8");
}

function write(file, content) {
  fs.mkdirSync(path.dirname(path.join(root, file)), { recursive: true });
  fs.writeFileSync(path.join(root, file), content, "utf8");
}

function decodeEntities(value = "") {
  const named = {
    amp: "&",
    lt: "<",
    gt: ">",
    quot: "\"",
    apos: "'",
    nbsp: " ",
    mdash: "-",
    ndash: "-",
  };
  return value.replace(/&(#x?[0-9a-fA-F]+|[a-zA-Z]+);/g, (_m, ent) => {
    if (ent[0] === "#") {
      const isHex = ent[1]?.toLowerCase() === "x";
      const num = Number.parseInt(ent.slice(isHex ? 2 : 1), isHex ? 16 : 10);
      return Number.isFinite(num) ? String.fromCodePoint(num) : _m;
    }
    return named[ent] ?? _m;
  });
}

function stripTags(html = "") {
  return decodeEntities(
    html
      .replace(/<script[\s\S]*?<\/script>/gi, " ")
      .replace(/<style[\s\S]*?<\/style>/gi, " ")
      .replace(/<[^>]+>/g, " ")
      .replace(/\s+/g, " ")
      .trim(),
  );
}

function clean(value = "") {
  return stripTags(value)
    .replace(/\s+([,.;:!?])/g, "$1")
    .replace(/\s+/g, " ")
    .trim();
}

function attr(html = "", name) {
  const re = new RegExp(`${name}\\s*=\\s*["']([^"']*)["']`, "i");
  const match = html.match(re);
  return match ? decodeEntities(match[1]).trim() : "";
}

function first(block, re) {
  const match = block.match(re);
  return match ? clean(match[1]) : "";
}

function rawFirst(block, re) {
  const match = block.match(re);
  return match ? match[1] : "";
}

function slugify(value) {
  return value
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 80);
}

function blockStarts(html, re) {
  return [...html.matchAll(re)].map((match) => ({
    index: match.index ?? 0,
    id: match[1],
  }));
}

function sliceByStarts(html, starts, endIndex = html.length) {
  return starts.map((start, idx) => {
    const end = starts[idx + 1]?.index ?? endIndex;
    return {
      id: start.id,
      block: html.slice(start.index, end),
    };
  });
}

function extractRows(block) {
  return [...block.matchAll(/<div class="row">([\s\S]*?)<\/div>/gi)]
    .slice(0, 4)
    .map((m) => clean(m[1]))
    .filter(Boolean);
}

function extractResources(block, context = {}) {
  const resources = [];
  const re = /<a\b([^>]*class=["'][^"']*(?:res-link|sub-res-link)[^"']*["'][^>]*)>([\s\S]*?)<\/a>/gi;
  for (const match of block.matchAll(re)) {
    const open = match[1];
    const body = match[2];
    const url = attr(open, "href");
    if (!url || url.startsWith("#")) continue;
    const title = first(body, /<span class="res-title">([\s\S]*?)<\/span>/i) || clean(body);
    const source =
      first(body, /<span class="res-source">([\s\S]*?)<\/span>/i) ||
      first(body, /<span class="src">([\s\S]*?)<\/span>/i) ||
      "";
    resources.push({
      id: `${context.domain || "site"}:${slugify(title)}:${slugify(url)}`,
      title,
      url,
      source,
      domain: context.domain,
      domainTitle: context.domainTitle,
      section: context.section,
      subsection: context.subsection,
    });
  }
  return resources;
}

function extractProblemLinks(block) {
  const links = [];
  const re = /<a\b([^>]*class=["'][^"']*sol-link[^"']*["'][^>]*)>([\s\S]*?)<\/a>/gi;
  for (const match of block.matchAll(re)) {
    const url = attr(match[1], "href");
    if (!url) continue;
    links.push({ title: clean(match[2]) || "Resource", url });
  }
  return links.slice(0, 4);
}

function extractConceptLinks(block) {
  const links = [];
  const resLinks = rawFirst(block, /<div class="res-links">([\s\S]*?)<\/div>/i);
  const re = /<a\b([^>]*)>([\s\S]*?)<\/a>/gi;
  for (const match of resLinks.matchAll(re)) {
    const url = attr(match[1], "href");
    if (!url) continue;
    links.push({ title: clean(match[2]) || "Resource", url });
  }
  return links.slice(0, 4);
}

function parseConceptPage(source, html) {
  const starts = blockStarts(html, /<section class="section" id="([^"]+)"/gi);
  const sections = [];
  const items = [];
  const resources = extractResources(html, { domain: source.key, domainTitle: source.title });

  for (const section of sliceByStarts(html, starts)) {
    const title = first(section.block, /<h2>([\s\S]*?)<\/h2>/i) || section.id;
    const meta = first(section.block, /<div class="meta">([\s\S]*?)<\/div>/i);
    const tagline = first(section.block, /<div class="tagline">([\s\S]*?)<\/div>/i);
    const secResources = extractResources(section.block, {
      domain: source.key,
      domainTitle: source.title,
      section: title,
    });
    const subStarts = blockStarts(section.block, /<div class="subsection">/gi).map((s, idx) => ({
      ...s,
      id: `sub-${idx + 1}`,
    }));
    const subsections = [];

    for (const sub of sliceByStarts(section.block, subStarts)) {
      const subTitle = first(sub.block, /<h3>([\s\S]*?)<\/h3>/i) || title;
      const subDesc = first(sub.block, /<div class="subsection-desc">([\s\S]*?)<\/div>/i);
      const subResources = extractResources(sub.block, {
        domain: source.key,
        domainTitle: source.title,
        section: title,
        subsection: subTitle,
      });
      const conceptMatches = [...sub.block.matchAll(/<li\b([^>]*data-cid=["'][^"']+["'][^>]*)>([\s\S]*?)<\/li>/gi)];
      const subItemIds = [];

      for (const match of conceptMatches) {
        const open = match[1];
        const body = match[2];
        const cid = attr(open, "data-cid");
        const itemTitle =
          first(body, /<div class="cname">([\s\S]*?)<\/div>/i) ||
          decodeEntities(attr(open, "data-name")) ||
          cid;
        const descCandidates = [...body.matchAll(/<div style=["'][^"']*margin-top:2px[^"']*["']>([\s\S]*?)<\/div>/gi)]
          .map((m) => clean(m[1]))
          .filter(Boolean);
        const description = descCandidates[0] || subDesc || tagline;
        const id = `${source.key}:${cid}`;
        subItemIds.push(id);
        items.push({
          id,
          key: cid,
          type: "concept",
          domain: source.key,
          domainTitle: source.title,
          title: itemTitle,
          description,
          section: title,
          subsection: subTitle,
          url: "",
          link: `${source.file}#${section.id}`,
          resources: extractConceptLinks(body),
          search: [itemTitle, description, source.title, title, subTitle, cid].join(" ").toLowerCase(),
        });
      }

      subsections.push({
        title: subTitle,
        description: subDesc,
        itemCount: subItemIds.length,
        resourceCount: subResources.length,
      });
    }

    const sectionItemCount = subsections.reduce((sum, s) => sum + s.itemCount, 0);
    sections.push({
      id: section.id,
      title,
      meta,
      tagline,
      rows: extractRows(section.block),
      link: `${source.file}#${section.id}`,
      itemCount: sectionItemCount,
      resourceCount: secResources.length,
      subsections,
    });
  }

  return { sections, items, resources };
}

function parseDsaPage(source, html) {
  const starts = blockStarts(html, /<section class="pattern" id="([^"]+)"/gi);
  const end = html.search(/<section class="sources">/i);
  const sections = [];
  const resources = extractResources(html, { domain: source.key, domainTitle: source.title });
  const byLc = new Map();

  for (const pattern of sliceByStarts(html, starts, end > -1 ? end : html.length)) {
    const title = first(pattern.block, /<h2>([\s\S]*?)<\/h2>/i) || pattern.id;
    const meta = first(pattern.block, /<div class="meta">([\s\S]*?)<\/div>/i);
    const tagline = first(pattern.block, /<div class="tagline">([\s\S]*?)<\/div>/i);
    const patternResources = extractResources(pattern.block, {
      domain: source.key,
      domainTitle: source.title,
      section: title,
    });
    const subStarts = blockStarts(pattern.block, /<div class="subpattern">/gi).map((s, idx) => ({
      ...s,
      id: `sub-${idx + 1}`,
    }));
    const subsections = [];
    let patternProblemCount = 0;

    for (const sub of sliceByStarts(pattern.block, subStarts)) {
      const subTitle = first(sub.block, /<h3>([\s\S]*?)<\/h3>/i) || title;
      const subDesc = first(sub.block, /<div class="subpattern-desc">([\s\S]*?)<\/div>/i);
      const subResources = extractResources(sub.block, {
        domain: source.key,
        domainTitle: source.title,
        section: title,
        subsection: subTitle,
      });
      const problemMatches = [...sub.block.matchAll(/<li\b([^>]*data-lc=["'][^"']+["'][^>]*)>([\s\S]*?)<\/li>/gi)];
      patternProblemCount += problemMatches.length;

      for (const match of problemMatches) {
        const open = match[1];
        const body = match[2];
        const lc = attr(open, "data-lc");
        if (!lc) continue;
        const problemTitle =
          first(body, /<a class="pname"[^>]*>([\s\S]*?)<\/a>/i) ||
          decodeEntities(attr(open, "data-name")) ||
          `LeetCode ${lc}`;
        const href = attr(rawFirst(body, /(<a class="pname"[^>]*>[\s\S]*?<\/a>)/i), "href");
        const diff = attr(open, "data-diff");
        const companies = attr(open, "data-companies")
          .split(",")
          .map((c) => c.trim())
          .filter(Boolean);
        const lists = [
          attr(open, "data-blind75") ? "Blind 75" : "",
          attr(open, "data-neetcode") ? "NeetCode 150" : "",
          attr(open, "data-grind") ? "Grind 75" : "",
        ].filter(Boolean);
        const existing = byLc.get(lc);
        const placement = {
          section: title,
          subsection: subTitle,
          description: subDesc,
          link: `${source.file}#${pattern.id}`,
        };
        if (existing) {
          existing.placements.push(placement);
          existing.search += ` ${title} ${subTitle} ${subDesc}`.toLowerCase();
        } else {
          byLc.set(lc, {
            id: `${source.key}:${lc}`,
            key: lc,
            type: "problem",
            domain: source.key,
            domainTitle: source.title,
            title: problemTitle,
            description: subDesc || tagline,
            section: title,
            subsection: subTitle,
            url: href,
            link: `${source.file}#${pattern.id}`,
            diff,
            companies,
            lists,
            placements: [placement],
            resources: extractProblemLinks(body),
            search: [problemTitle, lc, diff, companies.join(" "), lists.join(" "), source.title, title, subTitle, subDesc]
              .join(" ")
              .toLowerCase(),
          });
        }
      }

      subsections.push({
        title: subTitle,
        description: subDesc,
        itemCount: problemMatches.length,
        resourceCount: subResources.length,
      });
    }

    sections.push({
      id: pattern.id,
      title,
      meta,
      tagline,
      rows: extractRows(pattern.block),
      link: `${source.file}#${pattern.id}`,
      itemCount: patternProblemCount,
      resourceCount: patternResources.length,
      subsections,
    });
  }

  return { sections, items: [...byLc.values()], resources };
}

function uniqueBy(items, fn) {
  const seen = new Set();
  const out = [];
  for (const item of items) {
    const key = fn(item);
    if (seen.has(key)) continue;
    seen.add(key);
    out.push(item);
  }
  return out;
}

function buildData() {
  const parsedSources = [];
  let allItems = [];
  let allResources = [];

  for (const source of sourceDefs) {
    const html = read(source.file);
    const parsed = source.key === "dsa" ? parseDsaPage(source, html) : parseConceptPage(source, html);
    const itemCount = parsed.items.length;
    const resourceCount = uniqueBy(parsed.resources, (r) => `${r.title}|${r.url}`).length;
    const sourceRecord = {
      ...source,
      sections: parsed.sections,
      itemCount,
      resourceCount,
      progressLabel: source.kind === "problem" ? "problems" : "concepts",
      coverage: coverageBySource[source.key],
    };
    parsedSources.push(sourceRecord);
    allItems = allItems.concat(parsed.items);
    allResources = allResources.concat(parsed.resources);
  }

  allResources = uniqueBy(allResources, (r) => `${r.title}|${r.url}|${r.domain}|${r.section || ""}`);

  const stats = {
    domains: parsedSources.length,
    sections: parsedSources.reduce((sum, s) => sum + s.sections.length, 0),
    subsections: parsedSources.reduce(
      (sum, s) => sum + s.sections.reduce((inner, sec) => inner + sec.subsections.length, 0),
      0,
    ),
    items: allItems.length,
    problems: allItems.filter((i) => i.type === "problem").length,
    concepts: allItems.filter((i) => i.type === "concept").length,
    resources: allResources.length,
    additions: additions.length,
  };

  return {
    generatedAt: new Date().toISOString(),
    stats,
    sources: parsedSources,
    items: allItems,
    resources: allResources,
    roadmap,
    additions,
    coverage: coverageBySource,
  };
}

function escHtml(value = "") {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function hubHtml(data) {
  const json = JSON.stringify(data).replace(/</g, "\\u003c");
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="A unified learning hub for DSA, system design, CS fundamentals, behavioral interviews, AI engineering, and cloud.">
<title>Learning Hub</title>
<style>
:root {
  --bg: #f7f8fb;
  --surface: #ffffff;
  --surface-2: #eef2f7;
  --text: #171b24;
  --muted: #5d6575;
  --faint: #8a93a3;
  --border: #dce2eb;
  --strong: #253044;
  --accent: #2459d6;
  --accent-2: #0d8b78;
  --shadow: 0 10px 28px rgba(21, 30, 50, .08);
  --radius: 8px;
}
html.dark {
  --bg: #111318;
  --surface: #191d26;
  --surface-2: #222836;
  --text: #edf0f6;
  --muted: #a6adbb;
  --faint: #727b8c;
  --border: #303747;
  --strong: #f5f7fb;
  --accent: #7ca2ff;
  --accent-2: #50d1bd;
  --shadow: 0 12px 30px rgba(0, 0, 0, .25);
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--text);
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
  line-height: 1.5;
}
a { color: inherit; }
button, input, select { font: inherit; }
.appbar {
  position: sticky;
  top: 0;
  z-index: 20;
  border-bottom: 1px solid var(--border);
  background: color-mix(in srgb, var(--surface) 88%, transparent);
  backdrop-filter: blur(16px);
}
.appbar-inner {
  max-width: 1480px;
  margin: 0 auto;
  padding: 12px 18px;
  display: grid;
  grid-template-columns: minmax(160px, 220px) minmax(260px, 1fr) auto;
  gap: 12px;
  align-items: center;
}
.brand { min-width: 0; }
.brand-title {
  font-size: 18px;
  font-weight: 800;
  letter-spacing: 0;
  color: var(--strong);
}
.brand-sub {
  font-size: 11px;
  color: var(--muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.searchbox {
  display: grid;
  grid-template-columns: 28px 1fr;
  align-items: center;
  border: 1px solid var(--border);
  background: var(--surface-2);
  border-radius: var(--radius);
  padding: 0 10px;
  min-height: 42px;
}
.searchbox span { color: var(--faint); font-weight: 800; }
.searchbox input {
  border: 0;
  outline: 0;
  background: transparent;
  color: var(--text);
  width: 100%;
  min-width: 0;
}
.bar-actions { display: flex; gap: 8px; align-items: center; justify-content: end; }
.btn, .select {
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--text);
  min-height: 38px;
  border-radius: var(--radius);
  padding: 0 12px;
  cursor: pointer;
}
.btn:hover, .select:hover { border-color: var(--accent); }
.btn.primary {
  background: var(--strong);
  color: var(--bg);
  border-color: var(--strong);
}
.wrap {
  max-width: 1480px;
  margin: 0 auto;
  padding: 20px 18px 70px;
}
.metrics {
  display: grid;
  grid-template-columns: repeat(6, minmax(120px, 1fr));
  gap: 10px;
  margin-bottom: 16px;
}
.metric, .domain-card, .panel, .result, .section-row, .resource-row {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
}
.metric { padding: 12px; min-height: 78px; }
.metric .num { font-size: 24px; font-weight: 850; color: var(--strong); font-variant-numeric: tabular-nums; }
.metric .label { font-size: 11px; color: var(--muted); text-transform: uppercase; letter-spacing: .08em; }
.domain-grid {
  display: grid;
  grid-template-columns: repeat(6, minmax(150px, 1fr));
  gap: 10px;
  margin-bottom: 16px;
}
.domain-card {
  padding: 12px;
  min-height: 156px;
  cursor: pointer;
  border-top: 4px solid var(--domain-color);
}
.domain-card.active { outline: 2px solid color-mix(in srgb, var(--domain-color) 65%, transparent); }
.domain-card h2 { margin: 0 0 6px; font-size: 16px; letter-spacing: 0; }
.domain-card p { margin: 0; color: var(--muted); font-size: 12px; }
.domain-card .counts { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 10px; }
.pill {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 3px 7px;
  min-height: 24px;
  border-radius: 999px;
  background: var(--surface-2);
  color: var(--muted);
  font-size: 11px;
  font-weight: 700;
}
.progress {
  margin-top: 10px;
  height: 8px;
  border: 1px solid var(--border);
  border-radius: 999px;
  overflow: hidden;
  background: var(--surface-2);
}
.progress span { display: block; height: 100%; width: 0; background: var(--domain-color, var(--accent)); }
.workspace {
  display: grid;
  grid-template-columns: 340px minmax(0, 1fr);
  gap: 16px;
  align-items: start;
}
.sidebar {
  position: sticky;
  top: 82px;
  display: grid;
  gap: 12px;
}
.panel { padding: 14px; }
.panel h2, .main-title h2 {
  margin: 0;
  font-size: 15px;
  letter-spacing: 0;
}
.panel-head, .main-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}
.roadmap-list { display: grid; gap: 8px; }
.roadmap-step {
  border-left: 3px solid var(--accent-2);
  padding: 4px 0 4px 10px;
}
.roadmap-step .phase { color: var(--faint); font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: .06em; }
.roadmap-step .title { font-size: 13px; font-weight: 800; }
.roadmap-step .focus { font-size: 12px; color: var(--muted); margin-top: 2px; }
.additions { display: grid; gap: 8px; }
.addition {
  padding: 9px;
  background: var(--surface-2);
  border-radius: var(--radius);
}
.addition strong { font-size: 13px; }
.addition p { margin: 4px 0 0; color: var(--muted); font-size: 12px; }
.mainpane { min-width: 0; display: grid; gap: 12px; }
.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 10px;
}
.filter-group { display: flex; flex-wrap: wrap; gap: 6px; }
.chip {
  border: 1px solid var(--border);
  background: var(--surface-2);
  color: var(--muted);
  border-radius: 999px;
  padding: 7px 10px;
  min-height: 34px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 800;
}
.chip.active {
  background: var(--strong);
  color: var(--bg);
  border-color: var(--strong);
}
.results, .sections, .resources { display: grid; gap: 10px; }
.result {
  padding: 12px;
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 10px;
  border-left: 4px solid var(--domain-color, var(--accent));
}
.result h3 { margin: 0 0 5px; font-size: 15px; letter-spacing: 0; }
.result p { margin: 0; color: var(--muted); font-size: 13px; }
.result-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 8px;
}
.result-actions {
  display: grid;
  grid-template-columns: 1fr;
  align-content: start;
  gap: 6px;
  min-width: 104px;
}
.mini-btn {
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--surface-2);
  color: var(--text);
  padding: 6px 8px;
  min-height: 32px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 800;
  text-decoration: none;
  text-align: center;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.mini-btn.done, .mini-btn.bookmarked { background: var(--strong); color: var(--bg); border-color: var(--strong); }
.section-row {
  padding: 11px 12px;
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 8px;
  border-left: 4px solid var(--domain-color, var(--accent));
}
.section-row h3 { margin: 0; font-size: 14px; }
.section-row p { margin: 4px 0 0; color: var(--muted); font-size: 12px; }
.resource-row {
  padding: 11px 12px;
  display: grid;
  gap: 6px;
}
.resource-row a { font-weight: 800; text-decoration: none; }
.empty {
  padding: 28px;
  text-align: center;
  color: var(--muted);
  border: 1px dashed var(--border);
  border-radius: var(--radius);
}
.load-row { display: flex; justify-content: center; padding: 8px 0 4px; }
.hidden { display: none !important; }
@media (max-width: 1180px) {
  .metrics { grid-template-columns: repeat(3, minmax(120px, 1fr)); }
  .domain-grid { grid-template-columns: repeat(3, minmax(150px, 1fr)); }
  .workspace { grid-template-columns: 1fr; }
  .sidebar { position: static; grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
@media (max-width: 760px) {
  .appbar-inner { grid-template-columns: 1fr; }
  .bar-actions {
    display: grid;
    grid-template-columns: minmax(0, 1fr) minmax(72px, 80px) minmax(82px, 92px);
    justify-content: stretch;
  }
  .bar-actions .btn, .bar-actions .select { width: 100%; min-width: 0; padding-left: 8px; padding-right: 8px; }
  .metrics, .domain-grid, .sidebar { grid-template-columns: 1fr; }
  .result, .section-row { grid-template-columns: 1fr; }
  .result-actions { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
</style>
</head>
<body>
<script id="hub-data" type="application/json">${json}</script>
<header class="appbar">
  <div class="appbar-inner">
    <div class="brand">
      <div class="brand-title">Learning Hub</div>
      <div class="brand-sub">One index across DSA, systems, CS, behavioral, AI, and cloud</div>
    </div>
    <label class="searchbox">
      <span>/</span>
      <input id="search" autocomplete="off" placeholder="Search concepts, problems, companies, resources, sections">
    </label>
    <div class="bar-actions">
      <select id="quick-jump" class="select" title="Open source site">
        <option value="">Open site</option>
      </select>
      <button class="btn" id="theme">Theme</button>
      <button class="btn primary" id="random">Random</button>
    </div>
  </div>
</header>
<main class="wrap">
  <section class="metrics" id="metrics"></section>
  <section class="domain-grid" id="domains"></section>
  <div class="workspace">
    <aside class="sidebar">
      <section class="panel">
        <div class="panel-head"><h2>Roadmap</h2><span class="pill" id="roadmap-count"></span></div>
        <div class="roadmap-list" id="roadmap"></div>
      </section>
      <section class="panel">
        <div class="panel-head"><h2>Added Lanes</h2><span class="pill">gap fill</span></div>
        <div class="additions" id="additions"></div>
      </section>
    </aside>
    <section class="mainpane">
      <div class="filters">
        <div class="filter-group" id="type-filter"></div>
        <div class="filter-group" id="status-filter"></div>
        <div class="filter-group" id="difficulty-filter"></div>
        <button class="chip" id="clear">Clear</button>
      </div>
      <section>
        <div class="main-title"><h2 id="results-title">Catalog</h2><span class="pill" id="result-count"></span></div>
        <div class="results" id="results"></div>
        <div class="load-row"><button class="btn hidden" id="load-more">Load more</button></div>
      </section>
      <section>
        <div class="main-title"><h2>Section Map</h2><span class="pill" id="section-count"></span></div>
        <div class="sections" id="sections"></div>
      </section>
      <section>
        <div class="main-title"><h2>Resource Library</h2><span class="pill" id="resource-count"></span></div>
        <div class="resources" id="resources"></div>
      </section>
    </section>
  </div>
</main>
<script>
(function () {
  const data = JSON.parse(document.getElementById("hub-data").textContent);
  const byDomain = Object.fromEntries(data.sources.map(function (s) { return [s.key, s]; }));
  const state = { domain: "all", type: "all", status: "all", diff: "all", q: "", shown: 80 };
  const themeKey = "learning_hub_theme_v1";

  function qs(id) { return document.getElementById(id); }
  function esc(value) {
    return String(value || "").replace(/[&<>"']/g, function (ch) {
      return ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[ch];
    });
  }
  function readSet(key) {
    try { return new Set(JSON.parse(localStorage.getItem(key) || "[]")); }
    catch (_e) { return new Set(); }
  }
  function writeSet(key, set) { localStorage.setItem(key, JSON.stringify(Array.from(set))); }
  function storage(item) { return byDomain[item.domain].storage; }
  function isDone(item) { return readSet(storage(item).done).has(item.key); }
  function isBookmarked(item) { return readSet(storage(item).bookmark).has(item.key); }
  function toggleSet(key, value) {
    const set = readSet(key);
    if (set.has(value)) set.delete(value); else set.add(value);
    writeSet(key, set);
  }
  function pct(done, total) { return total ? Math.round((done / total) * 100) : 0; }
  function domainDone(source) {
    const set = readSet(source.storage.done);
    const valid = new Set(data.items.filter(function (i) { return i.domain === source.key; }).map(function (i) { return i.key; }));
    return Array.from(set).filter(function (key) { return valid.has(key); }).length;
  }
  function currentItems() {
    const q = state.q.toLowerCase();
    return data.items.filter(function (item) {
      if (state.domain !== "all" && item.domain !== state.domain) return false;
      if (state.type !== "all" && item.type !== state.type) return false;
      if (state.status === "done" && !isDone(item)) return false;
      if (state.status === "open" && isDone(item)) return false;
      if (state.status === "bookmarked" && !isBookmarked(item)) return false;
      if (state.diff !== "all" && item.diff !== state.diff) return false;
      if (q && !item.search.includes(q)) return false;
      return true;
    });
  }
  function currentResources() {
    const q = state.q.toLowerCase();
    return data.resources.filter(function (res) {
      if (state.domain !== "all" && res.domain !== state.domain) return false;
      if (!q) return true;
      return [res.title, res.source, res.domainTitle, res.section, res.subsection].join(" ").toLowerCase().includes(q);
    });
  }
  function renderMetrics() {
    const done = data.sources.reduce(function (sum, s) { return sum + domainDone(s); }, 0);
    const metrics = [
      [data.stats.domains, "source sites"],
      [data.stats.sections, "sections"],
      [data.stats.subsections, "subsections"],
      [data.stats.problems, "unique problems"],
      [data.stats.concepts, "concepts"],
      [done + " / " + data.stats.items, "completed"],
    ];
    qs("metrics").innerHTML = metrics.map(function (m) {
      return '<article class="metric"><div class="num">' + esc(m[0]) + '</div><div class="label">' + esc(m[1]) + '</div></article>';
    }).join("");
  }
  function renderDomains() {
    qs("domains").innerHTML = data.sources.map(function (source) {
      const done = domainDone(source);
      const percent = pct(done, source.itemCount);
      return '<article class="domain-card ' + (state.domain === source.key ? "active" : "") + '" data-domain="' + esc(source.key) + '" style="--domain-color:' + esc(source.color) + '">' +
        '<h2>' + esc(source.title) + '</h2>' +
        '<p>' + esc(source.summary) + '</p>' +
        '<div class="counts"><span class="pill">' + source.sections.length + ' sections</span><span class="pill">' + source.itemCount + ' ' + esc(source.progressLabel) + '</span><span class="pill">' + source.resourceCount + ' resources</span></div>' +
        '<div class="progress" title="' + percent + '% complete"><span style="width:' + percent + '%"></span></div>' +
      '</article>';
    }).join("");
    document.querySelectorAll(".domain-card").forEach(function (card) {
      card.addEventListener("click", function () {
        state.domain = state.domain === card.dataset.domain ? "all" : card.dataset.domain;
        state.shown = 80;
        render();
      });
    });
  }
  function makeChip(group, value, label, active) {
    return '<button class="chip ' + (active ? "active" : "") + '" data-group="' + group + '" data-value="' + value + '">' + esc(label) + '</button>';
  }
  function renderFilters() {
    qs("type-filter").innerHTML =
      makeChip("type", "all", "All", state.type === "all") +
      makeChip("type", "problem", "Problems", state.type === "problem") +
      makeChip("type", "concept", "Concepts", state.type === "concept");
    qs("status-filter").innerHTML =
      makeChip("status", "all", "Any status", state.status === "all") +
      makeChip("status", "open", "Open", state.status === "open") +
      makeChip("status", "done", "Done", state.status === "done") +
      makeChip("status", "bookmarked", "Bookmarked", state.status === "bookmarked");
    qs("difficulty-filter").innerHTML =
      makeChip("diff", "all", "Any difficulty", state.diff === "all") +
      makeChip("diff", "E", "Easy", state.diff === "E") +
      makeChip("diff", "M", "Medium", state.diff === "M") +
      makeChip("diff", "H", "Hard", state.diff === "H");
    document.querySelectorAll(".chip[data-group]").forEach(function (chip) {
      chip.addEventListener("click", function () {
        state[chip.dataset.group] = chip.dataset.value;
        state.shown = 80;
        render();
      });
    });
  }
  function itemHtml(item) {
    const source = byDomain[item.domain];
    const done = isDone(item);
    const bookmarked = isBookmarked(item);
    const tags = [
      source.label,
      item.type === "problem" ? "LC " + item.key : item.key,
      item.diff ? ({ E: "Easy", M: "Medium", H: "Hard" }[item.diff] || item.diff) : "",
      item.section,
      item.subsection,
    ].filter(Boolean);
    const resources = (item.resources || []).slice(0, 2).map(function (r) {
      return '<a class="mini-btn" href="' + esc(r.url) + '" target="_blank" rel="noopener">' + esc(r.title) + '</a>';
    }).join("");
    const external = item.url ? '<a class="mini-btn" href="' + esc(item.url) + '" target="_blank" rel="noopener">External</a>' : "";
    return '<article class="result" style="--domain-color:' + esc(source.color) + '">' +
      '<div><h3>' + esc(item.title) + '</h3><p>' + esc(item.description || "") + '</p>' +
      '<div class="result-meta">' + tags.map(function (t) { return '<span class="pill">' + esc(t) + '</span>'; }).join("") + '</div></div>' +
      '<div class="result-actions">' +
        '<button class="mini-btn ' + (done ? "done" : "") + '" data-done="' + esc(item.id) + '">' + (done ? "Done" : "Mark done") + '</button>' +
        '<button class="mini-btn ' + (bookmarked ? "bookmarked" : "") + '" data-bookmark="' + esc(item.id) + '">' + (bookmarked ? "Saved" : "Save") + '</button>' +
        '<a class="mini-btn" href="' + esc(item.link) + '">Open page</a>' + external + resources +
      '</div></article>';
  }
  function renderResults() {
    const items = currentItems();
    qs("result-count").textContent = items.length + " matches";
    qs("results-title").textContent = state.domain === "all" ? "Catalog" : byDomain[state.domain].title + " Catalog";
    const visible = items.slice(0, state.shown);
    qs("results").innerHTML = visible.length ? visible.map(itemHtml).join("") : '<div class="empty">No catalog items match the current filters.</div>';
    qs("load-more").classList.toggle("hidden", items.length <= state.shown);
    document.querySelectorAll("[data-done]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        const item = data.items.find(function (i) { return i.id === btn.dataset.done; });
        toggleSet(storage(item).done, item.key);
        render();
      });
    });
    document.querySelectorAll("[data-bookmark]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        const item = data.items.find(function (i) { return i.id === btn.dataset.bookmark; });
        toggleSet(storage(item).bookmark, item.key);
        render();
      });
    });
  }
  function renderSections() {
    const sources = state.domain === "all" ? data.sources : [byDomain[state.domain]];
    const rows = [];
    sources.forEach(function (source) {
      source.sections.forEach(function (section) {
        if (state.q) {
          const hay = [source.title, section.title, section.tagline, section.rows.join(" ")].join(" ").toLowerCase();
          if (!hay.includes(state.q.toLowerCase())) return;
        }
        rows.push({ source: source, section: section });
      });
    });
    qs("section-count").textContent = rows.length + " shown";
    qs("sections").innerHTML = rows.slice(0, 60).map(function (row) {
      return '<article class="section-row" style="--domain-color:' + esc(row.source.color) + '">' +
        '<div><h3>' + esc(row.source.label) + ' / ' + esc(row.section.title) + '</h3><p>' + esc(row.section.tagline || row.section.meta || "") + '</p>' +
        '<div class="result-meta"><span class="pill">' + row.section.itemCount + ' items</span><span class="pill">' + row.section.subsections.length + ' subsections</span><span class="pill">' + row.section.resourceCount + ' resources</span></div></div>' +
        '<a class="mini-btn" href="' + esc(row.section.link) + '">Open</a></article>';
    }).join("") || '<div class="empty">No sections match the current filters.</div>';
  }
  function renderResources() {
    const resources = currentResources();
    qs("resource-count").textContent = resources.length + " resources";
    qs("resources").innerHTML = resources.slice(0, 80).map(function (res) {
      const source = byDomain[res.domain];
      return '<article class="resource-row" style="--domain-color:' + esc(source.color) + '">' +
        '<a href="' + esc(res.url) + '" target="_blank" rel="noopener">' + esc(res.title) + '</a>' +
        '<div class="result-meta"><span class="pill">' + esc(source.label) + '</span>' +
        (res.section ? '<span class="pill">' + esc(res.section) + '</span>' : '') +
        (res.source ? '<span class="pill">' + esc(res.source) + '</span>' : '') +
        '</div></article>';
    }).join("") || '<div class="empty">No resources match the current filters.</div>';
  }
  function renderRoadmap() {
    qs("roadmap-count").textContent = data.roadmap.length + " phases";
    qs("roadmap").innerHTML = data.roadmap.map(function (step) {
      return '<div class="roadmap-step"><div class="phase">' + esc(step.phase) + '</div><div class="title">' + esc(step.title) + '</div><div class="focus">' + esc(step.focus) + '</div><div class="result-meta">' + step.domains.map(function (d) { return '<span class="pill">' + esc(d) + '</span>'; }).join("") + '</div></div>';
    }).join("");
    qs("additions").innerHTML = data.additions.map(function (add) {
      return '<div class="addition"><strong>' + esc(add.area) + '</strong><p>' + esc(add.why) + '</p><div class="result-meta">' + add.topics.slice(0, 4).map(function (t) { return '<span class="pill">' + esc(t) + '</span>'; }).join("") + '</div></div>';
    }).join("");
  }
  function renderJump() {
    qs("quick-jump").innerHTML = '<option value="">Open site</option>' + data.sources.map(function (source) {
      return '<option value="' + esc(source.file) + '">' + esc(source.title) + '</option>';
    }).join("");
  }
  function render() {
    renderMetrics();
    renderDomains();
    renderFilters();
    renderResults();
    renderSections();
    renderResources();
  }

  const savedTheme = localStorage.getItem(themeKey);
  if (savedTheme === "dark" || (!savedTheme && window.matchMedia("(prefers-color-scheme: dark)").matches)) {
    document.documentElement.classList.add("dark");
  }
  qs("theme").addEventListener("click", function () {
    const isDark = document.documentElement.classList.toggle("dark");
    localStorage.setItem(themeKey, isDark ? "dark" : "light");
  });
  qs("search").addEventListener("input", function (event) {
    state.q = event.target.value.trim().toLowerCase();
    state.shown = 80;
    render();
  });
  qs("clear").addEventListener("click", function () {
    state.domain = "all"; state.type = "all"; state.status = "all"; state.diff = "all"; state.q = ""; state.shown = 80;
    qs("search").value = "";
    render();
  });
  qs("load-more").addEventListener("click", function () {
    state.shown += 80;
    renderResults();
  });
  qs("random").addEventListener("click", function () {
    const items = currentItems();
    if (!items.length) return;
    const pick = items[Math.floor(Math.random() * items.length)];
    window.location.href = pick.link;
  });
  qs("quick-jump").addEventListener("change", function (event) {
    if (event.target.value) window.location.href = event.target.value;
  });

  renderJump();
  renderRoadmap();
  render();
})();
</script>
</body>
</html>
`;
}

function siteNavStyle() {
  return `<style id="site-nav-style">
.site-nav {
  position: sticky; top: 0; z-index: 80;
  display: flex; align-items: center; gap: 12px; flex-wrap: wrap;
  margin: 0 0 14px; padding: 10px 12px;
  border: 1px solid var(--border); border-radius: 10px;
  background: color-mix(in srgb, var(--bg-elev, var(--bg-card, #fff)) 92%, transparent);
  backdrop-filter: blur(14px); box-shadow: var(--shadow-card, 0 1px 3px rgba(0,0,0,.12));
}
.site-brand { display: grid; gap: 1px; color: var(--text); text-decoration: none; min-width: 180px; }
.site-brand strong { font-size: 14px; letter-spacing: 0; }
.site-brand span { font-size: 11px; color: var(--text-faint, var(--text-dim)); }
.site-nav-toggle { position: absolute; opacity: 0; pointer-events: none; }
.site-nav-menu {
  display: none; min-height: 34px; padding: 0 10px; border-radius: 7px;
  border: 1px solid var(--border); background: var(--bg-card); color: var(--text);
  align-items: center; cursor: pointer; font-size: 12px; font-weight: 800;
}
.site-links { display: flex; flex: 1; min-width: 260px; gap: 6px; flex-wrap: wrap; align-items: center; }
.site-links a, .site-theme-button {
  display: inline-flex; align-items: center; justify-content: center; min-height: 32px;
  padding: 5px 9px; border-radius: 7px; border: 1px solid var(--border);
  background: var(--bg-card); color: var(--text-dim); text-decoration: none;
  font-size: 12px; font-weight: 800; white-space: nowrap; cursor: pointer;
}
.site-links a, .site-theme-button { transition: border-color .15s ease, color .15s ease, transform .15s ease; }
.site-links a:hover, .site-theme-button:hover { border-color: var(--accent); color: var(--text); transform: translateY(-1px); }
.site-links a.current { background: var(--accent); border-color: var(--accent); color: white; }
.site-theme-button { margin-left: auto; font-family: inherit; }
.site-progress { color: var(--text-faint, var(--text-dim)); font-size: 11px; font-weight: 800; margin-left: 2px; }
.learning-coverage {
  background: var(--bg-elev); border: 1px solid var(--border); border-radius: 12px;
  padding: 14px 18px; margin: 16px 0 22px; box-shadow: var(--shadow-card);
}
.learning-coverage h2 { margin: 0 0 6px; font-size: 16px; letter-spacing: 0; }
.learning-coverage p { margin: 0; color: var(--text-dim); font-size: 13px; }
.coverage-pills { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 10px; }
.coverage-pills span, .coverage-links a {
  display: inline-flex; align-items: center; min-height: 25px; padding: 3px 8px;
  border-radius: 999px; background: var(--bg-card); border: 1px solid var(--border);
  color: var(--text-dim); font-size: 11px; font-weight: 800; text-decoration: none;
}
.coverage-links { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 10px; }
.source-extract {
  background: var(--bg-elev); border: 1px solid var(--border); border-radius: 10px;
  padding: 16px 18px; margin: 16px 0 22px; box-shadow: var(--shadow-card);
  transition: box-shadow .2s ease;
}
.source-extract h2 { margin: 0 0 6px; font-size: 17px; letter-spacing: 0; }
.source-extract p { margin: 0; color: var(--text-dim); font-size: 13px; }
.source-extract-grid {
  display: grid; gap: 10px; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
  margin-top: 12px;
}
.source-extract-card {
  border: 1px solid var(--border); border-radius: 8px; background: var(--bg-card); padding: 12px;
}
.source-extract-card h3 { margin: 0 0 6px; font-size: 14px; letter-spacing: 0; }
.source-extract-card ul { margin: 0; padding-left: 18px; color: var(--text-dim); font-size: 12px; }
.source-extract-card li { margin: 3px 0; }
.source-status {
  display: inline-flex; margin-bottom: 7px; min-height: 22px; align-items: center;
  padding: 2px 7px; border-radius: 999px; border: 1px solid var(--border);
  color: var(--accent); font-size: 10px; font-weight: 900; text-transform: uppercase;
}
.source-direct-links { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 12px; }
.source-direct-links a {
  display: inline-flex; align-items: center; min-height: 25px; padding: 3px 8px;
  border-radius: 999px; background: var(--bg-card); border: 1px solid var(--border);
  color: var(--text-dim); font-size: 11px; font-weight: 800; text-decoration: none;
}
.source-direct-links a:hover { border-color: var(--accent); color: var(--text); }
.qa-name { display: grid; gap: 3px; }
.qa-question { font-weight: 800; color: var(--text); }
.qa-answer { color: var(--text-dim); font-size: 12px; font-weight: 500; }
@media (max-width: 760px) {
  .site-nav { align-items: stretch; }
  .site-brand { flex: 1; min-width: 0; }
  .site-nav-menu { display: inline-flex; }
  .site-links { display: none; flex-basis: 100%; min-width: 0; grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .site-nav-toggle:checked ~ .site-links { display: grid; }
  .site-links a, .site-theme-button { width: 100%; }
  .site-theme-button { margin-left: 0; }
}
</style>`;
}

function siteNavHtml(source) {
  const links = sourceDefs.map((target) => {
    const currentAttrs = target.key === source.key ? ' class="current" aria-current="page"' : "";
    return `<a${currentAttrs} href="${escHtml(target.file)}">${escHtml(target.label)}</a>`;
  }).join("");
  return `<nav class="site-nav" aria-label="Learning site navigation">
  <a class="site-brand" href="index.html"><strong>Taran's Learning Hub</strong><span>${escHtml(source.title)}</span></a>
  <input class="site-nav-toggle" id="site-nav-toggle" type="checkbox" aria-label="Toggle site menu">
  <label class="site-nav-menu" for="site-nav-toggle">Menu</label>
  <div class="site-links">
    <a${source.key === "hub" ? ' class="current" aria-current="page"' : ""} href="index.html">Hub</a>
    ${links}
    <button class="site-theme-button" type="button" data-site-theme-toggle>Theme</button>
    <span class="site-progress">Progress: <span data-site-nav-progress>saved locally</span></span>
  </div>
</nav>`;
}

function siteNavScript() {
  return `<script id="site-nav-script">
(function () {
  const progress = document.querySelector("[data-site-nav-progress]");
  function refreshProgress() {
    const pageProgress = document.getElementById("overall-pct");
    if (progress && pageProgress) progress.textContent = pageProgress.textContent.trim();
  }
  refreshProgress();
  const pageProgress = document.getElementById("overall-pct");
  if (progress && pageProgress && "MutationObserver" in window) {
    new MutationObserver(refreshProgress).observe(pageProgress, {
      childList: true,
      characterData: true,
      subtree: true
    });
  }
  setTimeout(refreshProgress, 120);
  document.addEventListener("click", function (event) {
    if (event.target.closest(".done-check, .solve-check, .bookmark-star")) setTimeout(refreshProgress, 80);
  });
  const themeButton = document.querySelector("[data-site-theme-toggle]");
  if (themeButton) {
    themeButton.addEventListener("click", function () {
      const pageThemeButton = document.getElementById("theme-toggle");
      if (pageThemeButton) pageThemeButton.click();
      else document.documentElement.classList.toggle("light");
    });
  }
})();
</script>`;
}

function coveragePanelHtml(source) {
  const coverage = coverageBySource[source.key];
  if (!coverage) return "";
  const topics = coverage.topics.map((topic) => `<span>${escHtml(topic)}</span>`).join("");
  const links = coverage.resources.map(([title, url]) => `<a href="${escHtml(url)}" target="_blank" rel="noopener">${escHtml(title)}</a>`).join("");
  return `<section class="learning-coverage" id="coverage-check">
  <h2>${escHtml(coverage.title)}</h2>
  <p>${escHtml(coverage.notes[0])}</p>
  <div class="coverage-pills">${topics}</div>
  <div class="coverage-links">${links}</div>
</section>`;
}

function linkChips(links, limit = links.length) {
  return links
    .slice(0, limit)
    .map(([title, url]) => `<a href="${escHtml(url)}" target="_blank" rel="noopener">${escHtml(title)}</a>`)
    .join("");
}

function listItems(items) {
  return items.map((item) => `<li>${escHtml(item)}</li>`).join("");
}

function tutoringLink(pattern, subpattern) {
  const base = "https://thita.ai/dashboard/tutoring";
  const params = new URLSearchParams({
    category: "Behavioral",
    pattern,
    subpattern,
    teaching_mode: "feynman",
    persona: "samuel-brooks",
  });
  return `${base}?${params.toString()}`;
}

function systemDesignSourceExtractHtml() {
  const gfgCards = gfgSystemDesignOutline.map((group) => `<article class="source-extract-card">
    <span class="source-status">${escHtml(group.status)}</span>
    <h3>${escHtml(group.group)}</h3>
    <ul>${listItems(group.topics)}</ul>
  </article>`).join("");
  const priority = `<article class="source-extract-card">
    <span class="source-status">Priority gaps</span>
    <h3>Add / strengthen next</h3>
    <ul>${listItems(gfgSystemDesignPriorityGaps)}</ul>
  </article>`;
  const thitaCards = [
    `<article class="source-extract-card"><span class="source-status">Thita HLD</span><h3>20-hour HLD path</h3><ul>${listItems(thitaHldOutline)}</ul></article>`,
    `<article class="source-extract-card"><span class="source-status">Thita LLD</span><h3>LLD learning path</h3><ul>${listItems(thitaLldOutline)}</ul></article>`,
  ].join("");
  return `<aside class="source-extract" id="system-design-source-extracts">
  <h2>Extracted Source Map: GFG, DesignGurus and Thita</h2>
  <p>Topic outline extracted from the provided URL and uploaded course pages. This is organized as a gap map so I can study missing pieces without copying course/article text verbatim.</p>
  <div class="source-direct-links">${linkChips(gfgSystemDesignResources)}${linkChips([
    ["DesignGurus Grokking Course", "https://www.designgurus.io/course/grokking-the-system-design-interview"],
    ["Thita System Design HLD", "https://www.thita.ai/system-design"],
    ["Thita LLD Path", "https://www.thita.ai/dashboard/learning-path/lld"],
  ])}</div>
  <div class="source-extract-grid">${priority}${gfgCards}${thitaCards}</div>
  <h2 style="margin-top:16px">Direct GFG Topic Links</h2>
  <p>Direct topic links extracted from the GeeksforGeeks System Design tutorial page.</p>
  <div class="source-direct-links">${linkChips(gfgSystemDesignLinks)}</div>
  <h2 style="margin-top:16px">Direct DesignGurus Lesson Links</h2>
  <p>Direct topic links from the uploaded Grokking System Design course file.</p>
  <div class="source-direct-links">${linkChips(designGurusSystemDesignLinks)}</div>
</aside>`;
}

function behavioralSourceExtractHtml() {
  const cards = thitaBehavioralPatterns.map(([pattern, subs]) => `<article class="source-extract-card">
    <span class="source-status">Thita</span>
    <h3>${escHtml(pattern)}</h3>
    <ul>${subs.map((sub) => `<li><a href="${escHtml(tutoringLink(pattern, sub))}" target="_blank" rel="noopener">${escHtml(sub)}</a></li>`).join("")}</ul>
  </article>`).join("");
  return `<aside class="source-extract" id="behavioral-source-extracts">
  <h2>Extracted Source Map: Thita Behavioral Sheet</h2>
  <p>8 behavioral patterns and 32 subpatterns extracted from the uploaded Thita STAR sheet, with direct practice links for each subtopic.</p>
  <div class="source-direct-links">${linkChips([["Thita Behavioral Sheet", "https://www.thita.ai/behavioral-sheet"]])}</div>
  <div class="source-extract-grid">${cards}</div>
</aside>`;
}

function aiSourceExtractHtml() {
  const cards = thitaDataScienceOutline.map((topic) => `<article class="source-extract-card">
    <span class="source-status">Data science</span>
    <h3>${escHtml(topic)}</h3>
    <ul><li>Use this as the ML/statistics foundation bridge for AI engineering interviews.</li></ul>
  </article>`).join("");
  return `<aside class="source-extract" id="ai-source-extracts">
  <h2>Extracted Source Map: Thita Data Science Path</h2>
  <p>13 data science and analytics patterns extracted from the uploaded Thita learning path. I added direct resource links for the topics that support AI engineering.</p>
  <div class="source-direct-links">${linkChips(dataScienceDirectResources)}</div>
  <div class="source-extract-grid">${cards}</div>
</aside>`;
}

function gapSearchContext(key) {
  return {
    sd: "system design",
    cs: "computer science",
    bh: "behavioral interview",
    ai: "AI engineering",
    cloud: "AWS Azure cloud",
  }[key] || "";
}

function gapConceptLi(cid, name, desc, context) {
  const topic = normalizeSearchTopic(name);
  const yt = `https://www.youtube.com/results?search_query=${queryEncode(`${topic} ${context} explained`)}`;
  const google = `https://www.google.com/search?q=${queryEncode(`${topic} ${context} tutorial`)}`;
  return `<li data-cid="${cid}" data-name="${escHtml(name.toLowerCase())}"><div class="done-check" title="Mark as done"></div><div class="bookmark-star" title="Bookmark">☆</div><div><div class="cname">${escHtml(name)}</div><div style="font-size:11.5px;color:var(--text-faint);margin-top:2px">${escHtml(desc)}</div></div><div class="res-links"><a class="video" href="${yt}" target="_blank" rel="noopener">🔍YT</a><a class="" href="${google}" target="_blank" rel="noopener">🔍G</a></div></li>`;
}

function gapSectionHtml(source) {
  const gap = gapSections[source.key];
  if (!gap) return "";
  const context = gapSearchContext(source.key);
  const total = gap.subsections.reduce((sum, [, , concepts]) => sum + concepts.length, 0);
  const resLinks = gap.resources
    .map(([icon, title, src, url]) => `<a class="res-link" href="${escHtml(url)}" target="_blank" rel="noopener"><span class="res-icon">${icon}</span><span class="res-title">${escHtml(title)}</span><span class="res-source">${escHtml(src)}</span></a>`)
    .join("");
  const subs = gap.subsections
    .map(([subTitle, subDesc, concepts], subIndex) => {
      const tag = `${gap.num}.${subIndex + 1}`;
      const lis = concepts
        .map(([name, desc], conceptIndex) => gapConceptLi(`${tag}.${conceptIndex + 1}`, name, desc, context))
        .join("");
      return `<div class="subsection"><div class="subsection-head"><span class="subsection-tag">${tag}</span><h3>${escHtml(subTitle)}</h3><span style="font-size:11px;color:var(--text-faint);">${concepts.length} concepts</span></div><div class="subsection-desc">${escHtml(subDesc)}</div><ol class="concepts">${lis}</ol></div>`;
    })
    .join("\n");
  return `<!--gen-gap-start-->
<section class="section" id="section-${gap.num}" style="--section-color:hsl(${gap.hue}, 60%, 55%)">
<div class="section-banner" style="background:linear-gradient(135deg, hsl(${gap.hue}, 65%, 48%), hsl(${gap.hue + 30}, 70%, 55%))">
<div class="num">${gap.num}</div>
<div class="info">
<div class="label">Section ${gap.num} · Gap coverage</div>
<h2>${escHtml(gap.title)}</h2>
<div class="meta">${gap.subsections.length} subsections · ${total} concepts</div>
</div>
<div class="ppg">
<div class="pct-text" data-pp-text="${gap.num}">0 / ${total}</div>
<div class="pp-track"><div class="pp-fill" data-pp-fill="${gap.num}"></div></div>
</div>
</div>
<div class="section-desc">
<div class="tagline">${escHtml(gap.tagline)}</div>
<div class="row"><b>When.</b> ${escHtml(gap.when)}</div>
<div class="row"><b>Key idea.</b> ${escHtml(gap.keyIdea)}</div>
</div>
<div class="resources-section"><div class="head" onclick="this.parentElement.classList.toggle('open')"><h4>📚 Learn this domain</h4><div><span class="count">${gap.resources.length} resources</span><span class="chevron">▶</span></div></div><div class="resources-body"><div class="res-grid">${resLinks}</div></div></div>
${subs}
</section>
<!--gen-gap-end-->`;
}

function gapTocEntryHtml(source) {
  const gap = gapSections[source.key];
  if (!gap) return "";
  const total = gap.subsections.reduce((sum, [, , concepts]) => sum + concepts.length, 0);
  return `<!--gen-toc-start--><a href="#section-${gap.num}"><span class="roman">${gap.num}</span><span class="name">${escHtml(gap.title)}</span><span class="cnt">${gap.subsections.length}sec · ${total}</span></a><!--gen-toc-end-->`;
}

function resourceLibraryHtml(source) {
  const lib = resourceLibraries[source.key];
  if (!lib) return "";
  const links = lib.links
    .map(([title, url]) => `<a class="res-link" href="${escHtml(url)}" target="_blank" rel="noopener"><span class="res-icon">🔗</span><span class="res-title">${escHtml(title)}</span><span class="res-source">${escHtml(new URL(url).hostname.replace(/^www\./, ""))}</span></a>`)
    .join("");
  const drills = lib.drills
    ? `<div class="source-extract-grid"><article class="source-extract-card"><span class="source-status">Weekly drills</span><h3>Practice operating system</h3><ul>${listItems(lib.drills)}</ul></article></div>`
    : "";
  return `<aside class="source-extract" id="resource-library-${escHtml(source.key)}">
  <h2>${escHtml(lib.title)}</h2>
  <p>${escHtml(lib.blurb)}</p>
  ${drills}
  <div class="res-grid" style="margin-top:10px">${links}</div>
</aside>`;
}

function sourceExtractHtml(source) {
  const parts = [];
  if (source.key === "sd") parts.push(systemDesignSourceExtractHtml());
  if (source.key === "bh") parts.push(behavioralSourceExtractHtml());
  if (source.key === "ai") parts.push(aiSourceExtractHtml());
  const library = resourceLibraryHtml(source);
  if (library) parts.push(library);
  return parts.join("\n");
}

function stripLeadingDecor(value = "") {
  return clean(value)
    .replace(/^[\p{Extended_Pictographic}\uFE0F\s]+/gu, "")
    .replace(/\s+/g, " ")
    .trim();
}

function queryEncode(value) {
  return encodeURIComponent(value).replace(/%20/g, "+");
}

function normalizeSearchTopic(value = "") {
  let text = stripLeadingDecor(value)
    .replace(/&#x27;/g, "'")
    .replace(/&amp;/g, "and")
    .replace(/[“”]/g, '"')
    .replace(/[’]/g, "'")
    .replace(/\s+/g, " ")
    .trim();
  const qMatch = text.match(/^q:\s*(.*?)(?:\s+[—-]\s*a:|\s+a:|$)/i);
  if (qMatch) text = qMatch[1];
  text = text
    .replace(/^a:\s*/i, "")
    .replace(/\bq:\s*/gi, "")
    .replace(/\ba:\s*/gi, "")
    .replace(/[^\w\s+#./-]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
  const words = text.split(" ");
  const deduped = [];
  for (const word of words) {
    if (word.toLowerCase() !== deduped[deduped.length - 1]?.toLowerCase()) deduped.push(word);
  }
  return deduped.join(" ").trim();
}

function rewriteProblemSearchLinks(html) {
  return html.replace(/<li\b([^>]*\bdata-lc=["'][^"']+["'][^>]*)>([\s\S]*?)<\/li>/gi, (full, open, body) => {
    const lc = attr(open, "data-lc");
    if (!lc) return full;
    const title = normalizeSearchTopic(first(body, /<a class="pname"[^>]*>([\s\S]*?)<\/a>/i) || attr(open, "data-name"));
    const yt = `https://www.youtube.com/results?search_query=${queryEncode(`leetcode ${lc} ${title} solution`)}`;
    const google = `https://www.google.com/search?q=${queryEncode(`site:geeksforgeeks.org ${title} leetcode`)}`;
    const nextBody = body
      .replace(/https:\/\/www\.youtube\.com\/results\?search_query=[^"']*/gi, yt)
      .replace(/https:\/\/www\.google\.com\/search\?q=[^"']*/gi, google);
    return `<li${open}>${nextBody}</li>`;
  });
}

function rewriteConceptSearchLinks(html, source) {
  const context = {
    sd: "system design",
    cs: "computer science",
    bh: "behavioral interview",
    ai: "AI engineering",
    cloud: "AWS Azure cloud",
  }[source.key] || source.title;
  return html.replace(/<li\b([^>]*\bdata-cid=["'][^"']+["'][^>]*)>([\s\S]*?)<\/li>/gi, (full, open, body) => {
    const topic = normalizeSearchTopic(attr(open, "data-name") || first(body, /<div class="cname[^"]*">([\s\S]*?)<\/div>/i));
    if (!topic) return full;
    const yt = `https://www.youtube.com/results?search_query=${queryEncode(`${topic} ${context} explained`)}`;
    const google = `https://www.google.com/search?q=${queryEncode(`${topic} ${context} tutorial`)}`;
    const nextBody = body
      .replace(/https:\/\/www\.youtube\.com\/results\?search_query=[^"']*/gi, yt)
      .replace(/https:\/\/www\.google\.com\/search\?q=[^"']*/gi, google);
    return `<li${open}>${nextBody}</li>`;
  });
}

function formatCloudQa(html) {
  return html.replace(/<div class="cname">Q:\s*([\s\S]*?)\s+[—-]\s*A:\s*([\s\S]*?)<\/div>/gi, (_full, question, answer) => {
    return `<div class="cname qa-name"><span class="qa-question">Q: ${clean(question)}</span><span class="qa-answer">A: ${clean(answer)}</span></div>`;
  });
}

function removeGeneratedPageChrome(html) {
  return html
    .replace(/<style id="site-nav-style">[\s\S]*?<\/style>\s*/g, "")
    .replace(/<script id="site-nav-script">[\s\S]*?<\/script>\s*/g, "")
    .replace(/<nav class="site-nav"[\s\S]*?<\/nav>\s*/g, "")
    .replace(/<section class="learning-coverage" id="coverage-check">[\s\S]*?<\/section>\s*/g, "")
    .replace(/<aside class="source-extract"[\s\S]*?<\/aside>\s*/g, "")
    .replace(/<nav class="nav-bar">[\s\S]*?<\/nav>\s*/g, "")
    .replace(/<div class="home-strip">[\s\S]*?<\/div>\s*/g, "")
    .replace(/<!--gen-gap-start-->[\s\S]*?<!--gen-gap-end-->\s*/g, "")
    .replace(/<!--gen-toc-start-->[\s\S]*?<!--gen-toc-end-->\s*/g, "");
}

function transformSourcePage(source) {
  const filePath = path.join(root, source.file);
  let html = fs.readFileSync(filePath, "utf8");
  html = removeGeneratedPageChrome(html);
  const gapHtml = gapSectionHtml(source);
  if (gapHtml) {
    html = html.replace(/<script>window\.SITE_SLUG/, `${gapHtml}\n<script>window.SITE_SLUG`);
    const tocEntry = gapTocEntryHtml(source);
    html = html.replace(/(<nav class="toc">[\s\S]*?)(<\/div>\s*<\/nav>)/, (_m, head, tail) => `${head}${tocEntry}${tail}`);
  }
  html = html.replace(/href=["']hub\.html["']/g, 'href="index.html"');
  html = html.replace(/\bclass=(["'])resources-section\s+open\1/g, 'class=$1resources-section$1');
  html = html.replace(/\bclass=(["'])resources-section\s+open\s+([^"']*)\1/g, 'class=$1resources-section $2$1');
  html = html.replace(/<h1>([\s\S]*?)<\/h1>/i, (_m, title) => `<h1>${escHtml(stripLeadingDecor(title))}</h1>`);
  html = rewriteProblemSearchLinks(html);
  html = rewriteConceptSearchLinks(html, source);
  if (source.key === "cloud") html = formatCloudQa(html);
  html = html.replace("</head>", `${siteNavStyle()}\n</head>`);
  html = html.replace('<div class="wrap">', `<div class="wrap">\n${siteNavHtml(source)}\n`);
  html = html.replace(/(<nav class="toc">)/, `${coveragePanelHtml(source)}\n${sourceExtractHtml(source)}\n$1`);
  html = html.replace("</body>", `${siteNavScript()}\n</body>`);
  fs.writeFileSync(filePath, html, "utf8");
}

function duplicateTitles(values) {
  const counts = new Map();
  for (const value of values.filter(Boolean)) counts.set(value, (counts.get(value) || 0) + 1);
  return [...counts.entries()].filter(([, count]) => count > 1).map(([value, count]) => `${value} (${count})`);
}

function buildContentAudit(data) {
  const lines = [
    "# Taran's Learning Hub Content Audit",
    "",
    `Generated: ${data.generatedAt}`,
    "",
    "## Research References",
    "",
    "- roadmap.sh System Design: https://roadmap.sh/system-design",
    "- roadmap.sh Computer Science: https://roadmap.sh/computer-science",
    "- roadmap.sh AI Engineer: https://roadmap.sh/ai-engineer",
    "- roadmap.sh AWS: https://roadmap.sh/aws",
    "- OpenAI Cookbook: https://cookbook.openai.com/",
    "- AWS Well-Architected Framework: https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html",
    "- Azure Well-Architected Framework: https://learn.microsoft.com/en-us/azure/well-architected/",
    "- OWASP Top 10: https://owasp.org/www-project-top-ten/",
    "- System Design Primer: https://github.com/donnemartin/system-design-primer",
    "- GeeksforGeeks System Design Tutorial: https://www.geeksforgeeks.org/system-design/system-design-tutorial/",
    "- DesignGurus Grokking System Design Interview: https://www.designgurus.io/course/grokking-the-system-design-interview",
    "- Thita Behavioral Sheet: https://www.thita.ai/behavioral-sheet",
    "- Thita System Design HLD: https://www.thita.ai/system-design",
    "- Thita Data Science Learning Path: https://thita.ai/dashboard/learning-path/data-science",
    "- Thita LLD Learning Path: https://thita.ai/dashboard/learning-path/lld",
    "",
    "## Global Actions Applied",
    "",
    "- Rebuilt the hub as six page cards only; no global catalog, roadmap, or resource library on the landing page.",
    "- Added a shared cross-site navigation bar to every source page.",
    "- Closed resource dropdown panels by default while preserving click-to-expand behavior.",
    "- Rewrote generated YouTube and Google fallback URLs with cleaner topic-specific query rules.",
    "- Added per-page coverage check panels based on trusted roadmap and official documentation sources.",
    "",
  ];

  for (const source of data.sources) {
    const subsectionTitles = source.sections.flatMap((section) => section.subsections.map((sub) => sub.title));
    const weak = subsectionTitles.filter((title) => /^(misc|general|other|basics?)$/i.test(title) || title.length < 4);
    const dupes = duplicateTitles(subsectionTitles);
    const coverage = coverageBySource[source.key];
    lines.push(`## ${source.title}`);
    lines.push("");
    lines.push(`- Inventory: ${source.sections.length} sections, ${source.sections.reduce((sum, s) => sum + s.subsections.length, 0)} subsections, ${source.itemCount} ${source.progressLabel}, ${source.resourceCount} resources.`);
    lines.push(`- Formatting focus: consistent navigation, closed resources, clean headings, and better fallback search links.`);
    lines.push(`- Duplicate subsection names to review: ${dupes.length ? dupes.slice(0, 8).join(", ") : "none found by title."}`);
    lines.push(`- Weak/generic subsection names to review: ${weak.length ? weak.slice(0, 8).join(", ") : "none found by heuristic."}`);
    if (coverage) {
      lines.push(`- Coverage source: ${coverage.source}.`);
      lines.push(`- Missing/priority candidates: ${coverage.topics.join(", ")}.`);
      lines.push(`- Recommended next resources: ${coverage.resources.map(([title]) => title).join(", ")}.`);
    }
    if (source.key === "sd") {
      lines.push("- Uploaded/source extracts added to page: GeeksforGeeks topic map, DesignGurus direct lesson links, Thita HLD outline, and Thita LLD outline.");
      lines.push(`- GFG priority gaps: ${gfgSystemDesignPriorityGaps.join(", ")}.`);
      lines.push(`- GFG direct topic links included: ${gfgSystemDesignLinks.length}.`);
      lines.push(`- DesignGurus direct links included: ${designGurusSystemDesignLinks.length}.`);
      lines.push("- GFG extracted outline:");
      for (const group of gfgSystemDesignOutline) lines.push(`  - ${group.group} [${group.status}]: ${group.topics.join(", ")}.`);
      lines.push("- GFG direct topic links:");
      for (const [title, url] of gfgSystemDesignLinks) lines.push(`  - ${title}: ${url}`);
      lines.push("- Thita HLD extracted outline:");
      for (const item of thitaHldOutline) lines.push(`  - ${item}.`);
      lines.push("- Thita LLD extracted outline:");
      for (const item of thitaLldOutline) lines.push(`  - ${item}.`);
      lines.push("- DesignGurus direct lesson links:");
      for (const [title, url] of designGurusSystemDesignLinks) lines.push(`  - ${title}: ${url}`);
    }
    if (source.key === "bh") {
      lines.push("- Uploaded/source extract added to page: Thita Behavioral Sheet with direct STAR/pattern practice links.");
      lines.push("- Thita behavioral extracted outline:");
      for (const [pattern, subs] of thitaBehavioralPatterns) lines.push(`  - ${pattern}: ${subs.join(", ")}.`);
    }
    if (source.key === "ai") {
      lines.push("- Uploaded/source extract added to page: Thita Data Science path as an AI/ML foundations bridge.");
      lines.push(`- Data Science extracted topics: ${thitaDataScienceOutline.join(", ")}.`);
      lines.push("- Data Science direct resources:");
      for (const [title, url] of dataScienceDirectResources) lines.push(`  - ${title}: ${url}`);
    }
    lines.push("");
    lines.push("Sections:");
    for (const section of source.sections) {
      lines.push(`- ${section.title}: ${section.itemCount} items, ${section.subsections.length} subsections, ${section.resourceCount} resources.`);
    }
    lines.push("");
  }
  return `${lines.join("\n")}\n`;
}

function pagesWorkflow() {
  return `name: Deploy static learning hub

on:
  push:
    branches: ["main"]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  deploy:
    environment:
      name: github-pages
      url: \${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Configure Pages
        uses: actions/configure-pages@v5
      - name: Upload static site
        uses: actions/upload-pages-artifact@v3
        with:
          path: .
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
`;
}

function readme(data) {
  return `# Taran's Learning Hub

A personal static learning hub generated from the HTML sites in this folder.

## Included sites

${data.sources.map((s) => `- ${s.title}: ${s.itemCount} ${s.progressLabel}, ${s.sections.length} sections, ${s.resourceCount} resources`).join("\n")}

## Current UI

- \`index.html\` and \`hub.html\` show only the six page entry cards.
- Each source page has shared cross-site navigation.
- Resource panels start closed by default.
- Progress and bookmarks are stored locally in the browser.

## Local preview

Open \`index.html\` directly, or serve the folder with any static file server.

## GitHub Pages

This repo includes a GitHub Actions workflow at \`.github/workflows/pages.yml\`.
After pushing to the \`main\` branch, GitHub Pages deploys the static site.
The default public URL format is:

\`https://<github-user-or-org>.github.io/<repo-name>/\`
`;
}

function updateSourceNavs() {
  for (const source of sourceDefs) {
    const filePath = path.join(root, source.file);
    const html = fs.readFileSync(filePath, "utf8");
    fs.writeFileSync(filePath, html.replace(/href=["']hub\.html["']/g, 'href="index.html"'), "utf8");
  }
}

const data = buildData();
write("learning-hub-data.json", `${JSON.stringify(data, null, 2)}\n`);
write(
  "search-index.json",
  `${JSON.stringify(
    data.items.map((item) => ({
      k: item.domain,
      c: item.key,
      t: item.title,
      s: item.section,
      a: item.link,
    })),
  )}\n`,
);
write("index.html", simpleHubHtml(data));
write("hub.html", simpleHubHtml(data));
write("content-audit.md", buildContentAudit(data));
write(".nojekyll", "");
write(".github/workflows/pages.yml", pagesWorkflow());
write("README.md", readme(data));
for (const source of sourceDefs) transformSourcePage(source);

console.log(`Learning hub generated: ${data.stats.domains} sites, ${data.stats.sections} sections, ${data.stats.items} items, ${data.stats.resources} resources.`);
