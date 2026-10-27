# -*- coding: utf-8 -*-
L2 = {
"kafka-architecture.md": {"videos": [["2pioVWPblXs", "Apache Kafka Architecture: overview of Kafka's internal components", "Confluent"]], "docs": [
  ["Kafka — Design (official docs)", "https://kafka.apache.org/documentation/#design"],
  ["Kafka: a distributed messaging system for log processing (paper)", "https://notes.stephenholiday.com/Kafka.pdf"],
  ["Confluent — Kafka internals course", "https://developer.confluent.io/courses/architecture/get-started/"]]},

"delivery-semantics-reliability.md": {"videos": [["oUJbuFMyBDk", "What is a MESSAGE QUEUE and Where is it used?", "Gaurav Sen"]], "docs": [
  ["Confluent — Exactly-once semantics in Kafka", "https://www.confluent.io/blog/exactly-once-semantics-are-possible-heres-how-apache-kafka-does-it/"],
  ["AWS Builders' Library — Timeouts, retries and backoff with jitter", "https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/"],
  ["AlgoMaster — Idempotency", "https://algomaster.io/learn/system-design/idempotency"]]},

"event-driven-architecture.md": {"videos": [["YZNX4p4uYPU", "#40 Publish/Subscribe Pattern | System Design Fundamentals", "Software Interviews Prep"]], "docs": [
  ["Martin Fowler — What do you mean by event-driven?", "https://martinfowler.com/articles/201701-event-driven.html"],
  ["Confluent — Event-driven architecture", "https://www.confluent.io/learn/event-driven-architecture/"],
  ["microservices.io — Event sourcing", "https://microservices.io/patterns/data/event-sourcing.html"],
  ["AlgoMaster — Change data capture (CDC)", "https://algomaster.io/learn/system-design/change-data-capture-cdc"]]},

"monolith-vs-microservices-vs-serverless.md": {"videos": [["lTAcCNbJ7KE", "What Are Microservices Really All About? (And When Not To Use It)", "ByteByteGo"]], "docs": [
  ["Martin Fowler — Microservices", "https://martinfowler.com/articles/microservices.html"],
  ["Martin Fowler — MonolithFirst", "https://martinfowler.com/bliki/MonolithFirst.html"],
  ["AlgoMaster — Serverless architecture", "https://blog.algomaster.io/p/2edeb23b-cfa5-4b24-845e-3f6f7a39d162"],
  ["microservices.io — Microservice architecture pattern", "https://microservices.io/patterns/microservices.html"]]},

"microservices-patterns.md": {"videos": [["RqfaTIWc3LQ", "Reverse Proxy vs API Gateway vs Load Balancer", "ByteByteGo"]], "docs": [
  ["microservices.io — Pattern catalogue", "https://microservices.io/patterns/index.html"],
  ["microservices.io — Database per service", "https://microservices.io/patterns/data/database-per-service.html"],
  ["Martin Fowler — CQRS", "https://martinfowler.com/bliki/CQRS.html"],
  ["Martin Fowler — Strangler fig application", "https://martinfowler.com/bliki/StranglerFigApplication.html"]]},

"clean-layered-hexagonal-architecture.md": {"videos": [["G08FxxwPjXE", "Clean Architecture – Robert (Uncle Bob) Martin", "DevTernity Conference"]], "docs": [
  ["Uncle Bob — The clean architecture", "https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html"],
  ["Alistair Cockburn — Hexagonal architecture", "https://alistair.cockburn.us/hexagonal-architecture/"],
  ["Martin Fowler — PresentationDomainDataLayering", "https://martinfowler.com/bliki/PresentationDomainDataLayering.html"]]},

"circuit-breakers-bulkheads-timeouts.md": {"videos": [["ADHcBxEXvFA", "Circuit Breaker Pattern - Fault Tolerant Microservices", "Defog Tech"]], "docs": [
  ["Martin Fowler — Circuit breaker", "https://martinfowler.com/bliki/CircuitBreaker.html"],
  ["AWS Builders' Library — Timeouts, retries and backoff with jitter", "https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/"],
  ["microservices.io — Circuit breaker pattern", "https://microservices.io/patterns/reliability/circuit-breaker.html"],
  ["Google SRE Book — Addressing cascading failures", "https://sre.google/sre-book/addressing-cascading-failures/"]]},

"backpressure-throttling-load-protection.md": {"videos": [["YXkOdWBwqaA", "Rate Limiter System Design: Token Bucket, Leaky Bucket, Scaling", "ByteByteGo"]], "docs": [
  ["Apply back pressure when overloaded (Mechanical Sympathy)", "http://mechanical-sympathy.blogspot.com/2012/05/apply-back-pressure-when-overloaded.html"],
  ["AWS Builders' Library — Using load shedding to avoid overload", "https://aws.amazon.com/builders-library/using-load-shedding-to-avoid-overload/"],
  ["Google SRE Book — Handling overload", "https://sre.google/sre-book/handling-overload/"]]},

"graceful-degradation-load-shedding.md": {"videos": [["TmNiHbh-6Wg", "AWS re:Invent 2021 - Keeping Netflix reliable using prioritized load shedding", "AWS Events"]], "docs": [
  ["Google SRE Book — Handling overload", "https://sre.google/sre-book/handling-overload/"],
  ["AWS Builders' Library — Avoiding fallback in distributed systems", "https://aws.amazon.com/builders-library/avoiding-fallback-in-distributed-systems/"],
  ["AWS Builders' Library — Workload isolation using shuffle sharding", "https://aws.amazon.com/builders-library/workload-isolation-using-shuffle-sharding/"]]},

"distributed-locking-idempotency-safe-retries.md": {"videos": [["v7x75aN9liM", "Distributed locks — system design basics", "Tech Dummies - Narendra Lakshmana Gowda"]], "docs": [
  ["Kleppmann — How to do distributed locking", "https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html"],
  ["Redis — Distributed locks (Redlock)", "https://redis.io/docs/latest/develop/clients/patterns/distributed-locks/"],
  ["Stripe — Designing robust and predictable APIs with idempotency", "https://stripe.com/blog/idempotency"]]},

"consensus-algorithms-raft-paxos.md": {"videos": [["Ry2fIFIThP8", "The hardest problem in databases: consensus", "Ben Dicken"]], "docs": [
  ["The Secret Lives of Data — Raft, visualised", "https://thesecretlivesofdata.com/raft/"],
  ["Raft — the consensus algorithm (official site)", "https://raft.github.io/"],
  ["Paxos: the part-time parliament (paper)", "https://lamport.azurewebsites.net/pubs/lamport-paxos.pdf"],
  ["Google SRE Book — Managing critical state: distributed consensus", "https://sre.google/sre-book/managing-critical-state/"]]},

"leader-election-heartbeats-failure-detection.md": {"videos": [["vYp4LYbnnW8", "Designing for Understandability: The Raft Consensus Algorithm", "Diego Ongaro"]], "docs": [
  ["AlgoMaster — Heartbeats in distributed systems", "https://blog.algomaster.io/p/heartbeats-in-distributed-systems"],
  ["ZooKeeper: wait-free coordination (paper)", "https://www.usenix.org/legacy/event/usenix10/tech/full_papers/Hunt.pdf"],
  ["The Chubby lock service (paper)", "https://static.googleusercontent.com/media/research.google.com/en//archive/chubby-osdi06.pdf"]]},

"distributed-transactions-sagas.md": {"videos": [["rO9BXsl4AMQ", "Sagas: Event Choreography & Orchestration (NServiceBus)", "CodeOpinion"]], "docs": [
  ["microservices.io — Saga pattern", "https://microservices.io/patterns/data/saga.html"],
  ["Airbnb — Avoiding double payments in a distributed payments system", "https://medium.com/airbnb-engineering/avoiding-double-payments-in-a-distributed-payments-system-2981f6b070bb"],
  ["Two-phase commit protocol", "https://en.wikipedia.org/wiki/Two-phase_commit_protocol"]]},

"search-indexing-ranking-typeahead.md": {"videos": [["CeGtqouT8eA", "How Google searches one document among billions quickly", "Tech Dummies - Narendra Lakshmana Gowda"]], "docs": [
  ["Elasticsearch — Inverted index and relevance", "https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules.html"],
  ["Introduction to Information Retrieval (free book)", "https://nlp.stanford.edu/IR-book/information-retrieval-book.html"],
  ["Redis — Sorted sets (for top-K and typeahead)", "https://redis.io/docs/latest/develop/data-types/sorted-sets/"]]},

"metrics-dashboards-alerting.md": {"videos": [["kIcq1_pBQSY", "Design an analytics platform (metrics & logging) — mock interview", "Exponent"]], "docs": [
  ["Google SRE Book — Monitoring distributed systems", "https://sre.google/sre-book/monitoring-distributed-systems/"],
  ["Prometheus — Instrumentation best practices", "https://prometheus.io/docs/practices/instrumentation/"],
  ["Prometheus — Alerting best practices", "https://prometheus.io/docs/practices/alerting/"]]},

"logging-distributed-tracing.md": {"videos": [["AZhIjNHzURQ", "Google Dapper, a Large-Scale Distributed Systems Tracing Infrastructure", "Gaurav Sen"]], "docs": [
  ["OpenTelemetry — Observability primer", "https://opentelemetry.io/docs/concepts/observability-primer/"],
  ["Dapper, a large-scale distributed systems tracing infrastructure (paper)", "https://static.googleusercontent.com/media/research.google.com/en//archive/papers/dapper-2010-1.pdf"],
  ["Dynatrace — What is distributed tracing?", "https://www.dynatrace.com/news/blog/what-is-distributed-tracing/"]]},

"slos-error-budgets-golden-signals.md": {"videos": [["U53wC2A75Is", "Getting started with SLOs", "Google Cloud Tech"]], "docs": [
  ["Google SRE Book — Service level objectives", "https://sre.google/sre-book/service-level-objectives/"],
  ["Google SRE Workbook — Implementing SLOs", "https://sre.google/workbook/implementing-slos/"],
  ["Google SRE Book — Monitoring: the four golden signals", "https://sre.google/sre-book/monitoring-distributed-systems/"]]},

"testing-chaos-safe-deployment.md": {"videos": [["Q4nniyAarbs", "Chaos & Intuition Engineering at Netflix • Casey Rosenthal", "GOTO Conferences"]], "docs": [
  ["Principles of chaos engineering", "https://principlesofchaos.org/"],
  ["Martin Fowler — The practical test pyramid", "https://martinfowler.com/articles/practical-test-pyramid.html"],
  ["Martin Fowler — Blue-green deployment", "https://martinfowler.com/bliki/BlueGreenDeployment.html"],
  ["Google SRE Book — Release engineering", "https://sre.google/sre-book/release-engineering/"]]},

"authentication-authorization.md": {"videos": [["uj_4vxm9u90", "Design a simple authentication system — interview prep", "Interview Pen"]], "docs": [
  ["OAuth 2.0 — official site", "https://oauth.net/2/"],
  ["JWT — Introduction", "https://jwt.io/introduction"],
  ["OWASP — Authentication cheat sheet", "https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html"],
  ["Auth0 — Authentication and authorization flows", "https://auth0.com/docs/get-started/authentication-and-authorization-flow"]]},

"owasp-top-10-api-security.md": {"videos": [["YYe0FdfdgDU", "OWASP API Security Top 10 Course Secure Your Web Apps", "freeCodeCamp.org"]], "docs": [
  ["OWASP API Security Top 10 (2023)", "https://owasp.org/API-Security/editions/2023/en/0x11-t10/"],
  ["OWASP Top 10", "https://owasp.org/www-project-top-ten/"],
  ["API security checklist", "https://github.com/shieldfy/API-Security-Checklist"]]},

"threat-modeling-abuse-cases.md": {"videos": [["rEnJYNkUde0", "STRIDE Threat Modeling for Beginners - In 20 Minutes", "Netsec Explained"]], "docs": [
  ["OWASP — Threat modeling cheat sheet", "https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html"],
  ["Microsoft — STRIDE threat model", "https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats"],
  ["OWASP — Abuse case cheat sheet", "https://cheatsheetseries.owasp.org/cheatsheets/Abuse_Case_Cheat_Sheet.html"]]},

"cost-estimation-build-vs-buy-trade-offs.md": {"videos": [["8HaKO0Lw6Us", "A FinOps guide to re:Invent 2025 | The Keys to AWS Optimization", "AWS Events"]], "docs": [
  ["AWS Well-Architected — Cost optimization pillar", "https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/welcome.html"],
  ["AWS pricing calculator", "https://calculator.aws/"],
  ["AlgoMaster — Top 15 system design trade-offs", "https://blog.algomaster.io/p/system-design-top-15-trade-offs"]]},

"hld-vs-lld-boundaries.md": {"videos": [["ASPL5E0AIJw", "HLD Vs LLD | System Design Essentials", "Algorithms Made Easy"]], "docs": [
  ["Hello Interview — System design in a hurry", "https://www.hellointerview.com/learn/system-design/in-a-hurry/introduction"],
  ["Martin Fowler — Software architecture guide", "https://martinfowler.com/architecture/"],
  ["Refactoring Guru — Design patterns catalogue", "https://refactoring.guru/design-patterns/catalog"]]},

"object-oriented-foundations.md": {"videos": [["pTB0EiLXUC8", "Object-Oriented Programming, Simplified", "Programming with Mosh"]], "docs": [
  ["Refactoring Guru — OOP basics", "https://refactoring.guru/design-patterns/what-is-pattern"],
  ["Java design patterns — principles", "https://java-design-patterns.com/principles/"],
  ["SOLID principles explained", "https://en.wikipedia.org/wiki/SOLID"]]},

"design-principles.md": {"videos": [["pTB30aXS77U", "Uncle Bob's SOLID Principles Made Easy - In Python!", "ArjanCodes"]], "docs": [
  ["Java design patterns — principles", "https://java-design-patterns.com/principles/"],
  ["Uncle Bob — The principles of OOD", "http://butunclebob.com/ArticleS.UncleBob.PrinciplesOfOod"],
  ["Refactoring Guru — Design principles", "https://refactoring.guru/design-patterns/what-is-pattern"]]},

"uml-interaction-modeling.md": {"videos": [["6XrL5jXmTwM", "UML class diagrams", "Lucid Software"]], "docs": [
  ["UML class diagrams reference", "https://www.uml-diagrams.org/class-diagrams-overview.html"],
  ["PlantUML — Sequence diagram syntax", "https://plantuml.com/sequence-diagram"],
  ["Mermaid — Class diagram syntax", "https://mermaid.js.org/syntax/classDiagram.html"]]},

"design-patterns-for-lld.md": {"videos": [["vNHpsC5ng_E", "Design Patterns Video Tutorial", "Derek Banas"]], "docs": [
  ["Refactoring Guru — Design patterns catalogue", "https://refactoring.guru/design-patterns/catalog"],
  ["Java design patterns — full catalogue", "https://java-design-patterns.com/patterns/"],
  ["SourceMaking — Design patterns", "https://sourcemaking.com/design_patterns"]]},

"machine-coding-lld-case-studies.md": {"videos": [["NtMvNh0WFVM", "Amazon system design interview: design a parking garage", "Exponent"], ["D0kDMUgo27c", "System design mock interview: design a vending machine", "Exponent"]], "docs": [
  ["Refactoring Guru — Design patterns catalogue", "https://refactoring.guru/design-patterns/catalog"],
  ["Awesome low-level design (GitHub)", "https://github.com/ashishps1/awesome-low-level-design"]]},

"foundational-designs.md": {"videos": [["HHUi8F_qAXM", "How Does a URL Shortener Work?", "ByteByteGo"]], "docs": [
  ["AlgoMaster — Design a URL shortener", "https://algomaster.io/learn/system-design-interviews/design-url-shortener"],
  ["AlgoMaster — Design a load balancer", "https://algomaster.io/learn/system-design-interviews/design-load-balancer"],
  ["AlgoMaster — Design a distributed job scheduler", "https://blog.algomaster.io/p/design-a-distributed-job-scheduler"]]},

"core-interview-designs.md": {"videos": [["vvhC64hQZMk", "WHATSAPP System Design: Chat Messaging Systems for Interviews", "Gaurav Sen"]], "docs": [
  ["AlgoMaster — Design WhatsApp", "https://algomaster.io/learn/system-design-interviews/design-whatsapp"],
  ["AlgoMaster — Design Instagram", "https://algomaster.io/learn/system-design-interviews/design-instagram"],
  ["AlgoMaster — Design a notification service", "https://algomaster.io/learn/system-design-interviews/design-notification-service"]]},

"advanced-senior-level-designs.md": {"videos": [["_UZ1ngy-kOI", "Design Dropbox or Google Drive w/ a Ex-Meta Staff Engineer", "Hello Interview"]], "docs": [
  ["Discord — How Discord stores trillions of messages", "https://discord.com/blog/how-discord-stores-trillions-of-messages"],
  ["Slack — Real-time messaging", "https://slack.engineering/real-time-messaging/"],
  ["Spanner: Google's globally distributed database (paper)", "https://static.googleusercontent.com/media/research.google.com/en//archive/spanner-osdi2012.pdf"]]},
}
