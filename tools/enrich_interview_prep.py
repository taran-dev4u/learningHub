#!/usr/bin/env python3
"""
Enriches interviewPrepSections in tools/build-learning-hub.mjs with:
1. High-yield, actionable frameworks and templates across existing sections 1-6.
2. Section 7: Company Preparation Tracks (Amazon Loop & Bar Raiser, Google GCA & Craft,
   Meta Speed & Autonomy, Staff & Principal Engineering).
Uses atomic file writing.
"""
import os, re, tempfile

BUILDER_PATH = os.path.join(os.path.dirname(__file__), "build-learning-hub.mjs")

NEW_SECTIONS_CODE = """const interviewPrepSections = [
  {
    title: "Answer Frameworks",
    tagline: "Reusable structures for clear, paced interview answers.",
    when: "Use this first so every answer has a beginning, middle, result, and reflection.",
    keyIdea: "Structure reduces anxiety. Pick the framework that fits the question, then fill it with evidence.",
    resources: [
      ["STAR Method Guide", "https://www.themuse.com/advice/star-interview-method"],
      ["MIT Behavioral Interviews", "https://capd.mit.edu/resources/behavioral-interviews/"],
      ["Google Interview Tips", "https://www.google.com/about/careers/applications/interview-tips/"],
    ],
    subsections: [
      ["Behavioral Story Methods", "How to turn experience into concise stories.", [
        ["STAR method", "Situation (context & stakes), Task (your explicit role), Action (60% of time: decisions, trade-offs, technical steps), Result (quantified business impact). Default for FAANG behavioral."],
        ["CARL method", "Context (the setup), Action (what you owned), Result (measured outcome), Learning (reflection on what you would do differently and how it matured your engineering judgment)."],
        ["SOAR method", "Situation, Obstacle (the unexpected blocker or failure), Action (mitigation & recovery steps), Result. Best for adversity, conflict, and post-mortem questions."],
        ["PAR method", "Problem, Action, Result. High-density 60-second format ideal for initial recruiter screens and lightning-round behavioral checks."],
        ["Result plus reflection", "Always conclude with dual results: 1. Quantitative metric (e.g. -45% p99 latency, +$1.2M GMV); 2. Systemic learning instituted to prevent recurrence."],
      ]],
      ["Direct Answer Methods", "How to answer open-ended and opinion questions without rambling.", [
        ["PREP method", "Point (direct conclusion), Reason (the underlying architectural principle), Example (concrete production scenario), Point (reiterating the takeaway)."],
        ["PEEL method", "Point (claim), Evidence (data/metrics), Explanation (why the evidence supports the point), Link (connecting back to the broader problem)."],
        ["Headline first", "State your bottom-line conclusion in the first 10 seconds before providing background; prevents losing the interviewer's attention."],
        ["Signposting", "Outline the 2-3 parts of your answer up front ('I approached this through 3 phases: root cause profiling, canary mitigation, and systemic linting')."],
        ["Time-boxing", "Calibrate story duration strictly: 30s elevator summary, 90s standard response, 3min project deep-dive; stop and check in with the interviewer."],
      ]],
      ["Answer Quality Checklist", "The standard every saved answer should meet.", [
        ["Specificity", "Anchor answers with concrete technologies, system scale, exact constraints, and real architectural trade-offs."],
        ["Ownership", "Distinguish personal contributions ('I designed', 'I implemented', 'I proposed') from collective team accomplishments ('We decided')."],
        ["Measurable impact", "Quantify outcomes with hard numbers: latency (ms), throughput (QPS), infrastructure cost ($/month), availability nines, or developer velocity."],
        ["Trade-off clarity", "Explicitly articulate what was sacrificed (e.g. accepted eventual consistency to guarantee high availability under network partitions)."],
        ["Learning loop", "Demonstrate that failures produced permanent structural improvements (automated CI checks, runbooks, architectural guardrails)."],
      ]],
    ],
  },
  {
    title: "Personal Pitch and Resume Walkthrough",
    tagline: "Answers for opening questions, resume discussion, and motivation.",
    when: "Use these in recruiter screens, hiring manager screens, and the first few minutes of technical interviews.",
    keyIdea: "Your pitch should connect your past work, target role, and proof that you can do the job.",
    resources: [
      ["Indeed Interview Questions", "https://www.indeed.com/career-advice/interviewing/top-interview-questions-and-answers"],
      ["Harvard Resume and Interview Resources", "https://careerservices.fas.harvard.edu/resources/"],
      ["LinkedIn Interview Prep", "https://www.linkedin.com/interview-prep/"],
    ],
    subsections: [
      ["Opening Questions", "The first answers that set the tone.", [
        ["Tell me about yourself", "Present, Past, Future framework: Current focus and standout accomplishments (30s) -> career trajectory & technical foundation (30s) -> why this role matches your growth path (30s)."],
        ["Walk me through your resume", "Highlight inflection points, expanding architectural scope, technical milestones, and leadership growth rather than reading line-by-line job descriptions."],
        ["What are you looking for next", "Connect your career trajectory to larger system scale, deeper domain specialization, technical mentorship, and high-impact business ownership."],
        ["Why this company", "Three pillars: 1. Specific product challenges and engineering scale; 2. Alignment with company engineering culture; 3. How your specific expertise directly addresses their current bottlenecks."],
        ["Why this role", "Map your unique technical strengths (distributed systems, performance optimization, cloud infrastructure) directly to the specific requirements of the team."],
        ["What makes you a strong fit", "Provide 3 crisp evidence points: proven domain mastery, track record of delivering under high ambiguity, and demonstrated ability to mentor and multiply peers."],
      ]],
      ["Experience and Projects", "How to explain work without sounding vague.", [
        ["Most impactful project", "Detail the problem, constraints, your personal architectural choices, and the measurable business outcome (e.g. scaled to 50k RPS, saved $480k/yr)."],
        ["Most complex project", "Articulate complexity across 4 vectors: technical scale (millions of records), distributed concurrency, organizational cross-team dependencies, and tight timeline constraints."],
        ["Project you are proud of", "Choose a project demonstrating technical craftsmanship, deep curiosity, and going beyond minimum requirements to solve a systemic problem."],
        ["Project that failed", "Choose a real technical or estimation failure; own it completely without blaming others; highlight the blameless post-mortem and automated prevention mechanism."],
        ["Favorite technical decision", "Explain the evaluated alternatives (Option A vs Option B), the critical deciding constraint, and how the choice proved correct over a multi-year horizon."],
      ]],
      ["Self-Awareness Questions", "Questions that test honesty and maturity.", [
        ["Biggest strength", "Name a genuine strength (e.g. diving deep into system performance bottlenecks) backed by a concrete production victory and peer recognition."],
        ["Biggest weakness", "Pick a real technical or organizational weakness with an active, demonstrable system for continuous improvement (e.g. tendency to over-engineer MVP prototypes; counteracted by strict time-boxed RFC reviews)."],
        ["How do you learn new things", "Describe an empirical learning loop: reading official specs/papers, building disposable working prototypes, benchmarking edge cases, and authoring team documentation."],
        ["Where do you see yourself in five years", "Focus on technical mastery, architectural leadership across multiple teams, multiplying engineering talent, and driving major technology roadmaps."],
        ["What motivates you", "Tie motivation to customer impact, solving non-trivial distributed systems problems, building reliable software craft, and collaborating with high-performing peers."],
      ]],
    ],
  },
  {
    title: "Behavioral Story Bank",
    tagline: "The personal story themes most interview loops repeatedly test.",
    when: "Use these to prepare one strong story per theme, then reuse them across different question wording.",
    keyIdea: "A small set of strong, flexible stories beats memorizing hundreds of one-off answers.",
    resources: [
      ["Amazon Leadership Principles", "https://www.amazon.jobs/content/en/our-workplace/leadership-principles"],
      ["MIT Behavioral Interviews", "https://capd.mit.edu/resources/behavioral-interviews/"],
      ["Yale Behavioral Interviewing", "https://ocs.yale.edu/channels/behavioral-interviewing/"],
    ],
    subsections: [
      ["Ownership and Impact", "Stories that show you take responsibility and move outcomes.", [
        ["Tell me about a time you owned a project end to end", "Lead through the full lifecycle: requirement scoping, RFC review, architecture design, parallel workstream tracking, canary rollout, and post-launch telemetry."],
        ["Tell me about a time you improved a process", "Identify an engineering drag (e.g. 45-minute manual releases), build an automated GitOps canary pipeline with automated rollback, and quantify velocity improvements."],
        ["Tell me about a time you went beyond your role", "Notice a critical blind spot outside your team's charter (e.g. data ingestion partition skew stalling ML models), step up to fix it, and establish monitoring alarms."],
        ["Tell me about a time you made a customer or user impact", "Translate customer friction (e.g. 22% auth abandonment on CLI) into technical overhaul (RFC 8628 Device Code flow), dropping drop-offs to under 1.5%."],
        ["Tell me about a time you delivered under pressure", "Maintain calm under tight deadlines by ruthlessly descoping non-essential P2 features, parallelizing frontend/backend mocks, and maintaining automated test rigor."],
      ]],
      ["Conflict and Communication", "Stories that show collaboration without defensiveness.", [
        ["Tell me about a conflict with a teammate", "Focus on depersonalizing the debate: conduct empirical benchmarks, analyze trade-offs against shared business goals, and align around data rather than seniority."],
        ["Tell me about a disagreement with your manager", "Disagree and commit: voice technical risks with data in private 1:1; propose low-risk fallback; once the decision is locked, execute with 100% commitment."],
        ["Tell me about a difficult stakeholder", "Align conflicting stakeholder incentives (e.g. Sales wanting instant features vs Security requiring audits) using an objective RICE scoring matrix and transparent phased delivery."],
        ["Tell me about feedback you received", "Receive critical feedback with humility (e.g. design docs too terse for junior engineers), demonstrate visible behavioral adaptation, and solicit follow-up feedback."],
        ["Tell me about giving difficult feedback", "Deliver timely, private, actionable feedback focusing on observable behaviors and business impacts rather than personal attributes, paired with a coaching path."],
      ]],
      ["Ambiguity, Failure, and Learning", "Stories that prove resilience and judgment.", [
        ["Tell me about a time requirements were unclear", "Structure chaos: decompose vague asks into concrete user personas, document core assumptions in an RFC, define explicit MVP boundaries, and establish feedback checkpoints."],
        ["Tell me about a failure", "Own a real technical mistake (e.g. overlooked database lock during migration); detail the immediate incident response, transparent stakeholder communication, and automated CI lock linting."],
        ["Tell me about a mistake in production", "Explain detection via metrics, immediate mitigation (traffic shedding/rollback), authoring a blameless post-mortem, and adding automated contract tests."],
        ["Tell me about learning a new technology quickly", "Demonstrate rapid technical immersion: self-taught eBPF over a weekend to isolate Linux CFS scheduler throttling, eliminating a persistent 40ms latency regression."],
        ["Tell me about a time you had to change direction", "Pivot gracefully when production telemetry or customer data disconfirms initial hypotheses; explain why staying attached to sunk costs hurts the business."],
      ]],
      ["Leadership and Mentoring", "Stories that show influence without relying on title.", [
        ["Tell me about leading without authority", "Influence cross-functional peers through clear technical design docs, proof-of-concept prototypes, empathetic listening, and shared ownership."],
        ["Tell me about mentoring someone", "Coach a struggling junior engineer through structured 1:1 whiteboarding, teach trade-off evaluation, delegate a meaty service project, and support their promotion to SDE-2."],
        ["Tell me about raising team standards", "Institute practical engineering hygiene: automated test coverage gates (minimum 80%), flaky test quarantine bots, and standardized RFC design templates."],
        ["Tell me about prioritizing competing work", "Evaluate competing sprint demands using an impact-effort matrix; make technical trade-offs visible to product leadership to prevent developer burnout."],
        ["Tell me about creating alignment", "Bridge conflicting architectural views across multiple teams by organizing a focused design review, compiling a side-by-side trade-off matrix, and driving decisive consensus."],
      ]],
    ],
  },
  {
    title: "HR and Recruiter Questions",
    tagline: "Common screening questions, logistics, negotiation, and professionalism.",
    when: "Use this before recruiter calls and final HR rounds.",
    keyIdea: "Be honest, calm, and concise. Do not over-explain sensitive topics.",
    resources: [
      ["Indeed HR Interview Questions", "https://www.indeed.com/career-advice/interviewing/hr-interview-questions"],
      ["HBR Negotiating Job Offers", "https://hbr.org/2014/04/15-rules-for-negotiating-a-job-offer"],
      ["Levels.fyi Salary Negotiation Guide", "https://www.levels.fyi/blog/salary-negotiation.html"],
    ],
    subsections: [
      ["Recruiter Screen Basics", "Questions that determine fit, timing, and communication quality.", [
        ["Why are you leaving your current role", "Frame positively around running TOWARDS greater challenges: seeking larger scale, deeper technical problems, and broader architectural ownership."],
        ["Why do you want to join us", "Demonstrate specific knowledge of their engineering challenges, recent product launches, and how your technical background directly helps solve their current bottlenecks."],
        ["What is your notice period", "State your contractual notice period directly, mention any accrued leave flexibility, and emphasize committing to a clean, professional handover."],
        ["Are you interviewing elsewhere", "Be transparent: state that you are actively exploring a select few high-caliber opportunities and are currently in intermediate/onsite interview stages."],
        ["What is your availability", "Provide clear, specific time windows and timezones for technical interviews; confirm your target start date window."],
        ["Do you need sponsorship", "Answer clearly and accurately regarding work authorization status and any future visa sponsorship requirements."],
      ]],
      ["Compensation and Offer Questions", "How to stay professional when money comes up.", [
        ["What are your salary expectations", "Research market rates on Levels.fyi; request the approved salary range for the role first; if pressed, provide a well-researched, realistic band."],
        ["What is your current compensation", "Redirect focus professionally to target compensation based on market value, role scope, and expectations: 'I am looking for a package competitive with market rates for this level.'"],
        ["Do you have competing offers", "State status truthfully; leverage competing timelines respectfully to accelerate scheduling without using ultimatums or burning bridges."],
        ["What matters besides salary", "Highlight total compensation components: equity (RSUs/options), role scope, engineering culture, direct manager, learning trajectory, and work-life flexibility."],
        ["How would you evaluate an offer", "Evaluate using a multi-factor rubric: role scope and impact, team caliber, compensation trajectory, equity upside, and long-term career growth."],
      ]],
      ["Risk and Fit Questions", "Questions that test maturity and alignment.", [
        ["Why is there a gap in your resume", "Be honest, brief, and factual (caregiving, travel, dedicated full-time technical upskilling); pivot immediately to your current readiness and enthusiasm."],
        ["Have you ever been fired or laid off", "Address calmly and factually without defensiveness or bitterness; explain company restructuring/macro conditions, take ownership of any learnings, and emphasize subsequent achievements."],
        ["How do you handle stress", "Explain a proactive operating system: ruthlessly prioritizing P0 deliverables, transparent communication with stakeholders, taking short cognitive breaks, and maintaining regular exercise."],
        ["What work environment helps you perform best", "Describe high-trust, collaborative environments with clear ownership, psychological safety to debate technical ideas, and high standards of craft."],
        ["What would make you decline an offer", "Stay values-focused: lack of team alignment on engineering quality, absence of growth opportunities, or misaligned ethical standards."],
      ]],
    ],
  },
  {
    title: "Technical Communication",
    tagline: "How to explain technical work, trade-offs, and debugging under interview pressure.",
    when: "Use this in system design, coding debriefs, project deep dives, and hiring manager rounds.",
    keyIdea: "Interviewers evaluate how you think, not only what you know. Make your reasoning visible.",
    resources: [
      ["Google Technical Interview Prep", "https://www.google.com/about/careers/applications/interview-tips/"],
      ["System Design Primer", "https://github.com/donnemartin/system-design-primer"],
      ["Martin Fowler Technical Leadership", "https://martinfowler.com/tags/leadership.html"],
    ],
    subsections: [
      ["Project Deep Dive Questions", "Explain technical depth with structure.", [
        ["Explain your architecture", "Structure top-down: start with user flow and ingress (CDN/API Gateway), then service breakdown and messaging, datastore selection, and caching/bottleneck mitigation."],
        ["What was the hardest technical problem", "State the unexpected technical anomaly, constraints, hypotheses tested, the root-cause diagnosis, and the permanent architectural resolution."],
        ["How did you measure success", "Provide quantitative pre-and-post metrics: throughput (QPS), latency percentiles (p50/p99), resource utilization, error budgets, and operational cost."],
        ["What would you redesign now", "Demonstrate mature hindsight: discuss earlier adoption of asynchronous event streams, investing in distributed tracing earlier, or decomposing large schemas earlier."],
        ["How did you test it", "Describe the complete testing pyramid: unit tests with mocking, integration tests with Docker/Testcontainers, load testing with k6/Locust, and canary verification."],
      ]],
      ["Trade-Off and Judgment Questions", "Show senior reasoning in simple language.", [
        ["Why did you choose this technology", "Name the evaluated alternatives (e.g. gRPC vs REST vs GraphQL), state the deciding constraint (serialization latency vs client flexibility), and justify the trade-off."],
        ["What did you optimize for", "State explicit priority ranking: Reliability > Security > Latency > Cost > Feature Velocity; explain why this ordering fit the business phase."],
        ["What broke at scale", "Describe the specific saturation bottleneck (e.g. database thread contention under 4x traffic), immediate mitigation (caching hot keys, shedding RPCs), and permanent sharding fix."],
        ["How do you handle incidents", "Five-step incident lifecycle: 1. Detect (alarms); 2. Mitigate (shed load/rollback); 3. Communicate (status page); 4. Root cause (thread dumps/logs); 5. Prevent (automated CI guards)."],
        ["How do you decide build vs buy", "Framework: Buy commodity capabilities (auth, billing, email, observability) to preserve focus; Build core differentiators (proprietary algorithms, business logic, core storage)."],
      ]],
      ["Coding Interview Communication", "What to say while solving.", [
        ["Restate the problem", "Repeat the problem in your own words, clarify input/output types, and walk through an example to confirm mutual understanding before typing any code."],
        ["Clarify edge cases", "Inquire proactively about nulls, empty inputs, single-element collections, duplicate values, negative numbers, integer overflow, and extreme scale constraints."],
        ["Explain brute force first", "State the naive brute force approach and its Big-O time/space complexity in 60 seconds; establish the baseline before optimizing."],
        ["Narrate the invariant", "Explain what condition remains true at each iteration of your loop or recursion, making your algorithmic logic transparent and easy for the interviewer to follow."],
        ["Close with complexity and tests", "Conclude by stating precise Big-O time and space complexity; manually trace your code through normal inputs and tricky boundary edge cases."],
      ]],
    ],
  },
  {
    title: "Transcript Practice Lab",
    tagline: "Read answers word by word, build pacing, and rehearse out loud.",
    when: "Use this after drafting an answer and before a mock interview.",
    keyIdea: "A strong answer sounds calm because it has rhythm. Practice with moving highlights until the structure feels natural.",
    resources: [
      ["Pramp Mock Interviews", "https://www.pramp.com/"],
      ["Interviewing.io", "https://interviewing.io/"],
      ["Exponent Interview Prep", "https://www.tryexponent.com/"],
    ],
    subsections: [
      ["Transcript Scripts", "Prepared scripts to read, personalize, and rehearse.", [
        ["Opening pitch transcript", "A 75-second structured answer for 'Tell me about yourself' connecting past experience, technical focus, and role fit."],
        ["Conflict story transcript", "A STAR script demonstrating calm technical disagreement, empirical benchmarking, and disagree-and-commit resolution."],
        ["Failure story transcript", "A CARL script owning a production testing oversight, immediate remediation, and instituting automated prevention."],
        ["Project deep dive transcript", "A 90-second technical walkthrough covering problem context, service architecture, key trade-offs, and quantified business impact."],
        ["Closing question transcript", "High-impact closing questions asking interviewers about team success metrics, current technical bottlenecks, and cultural expectations."],
      ]],
      ["Mock Interview Operating System", "How to run a complete prep session.", [
        ["Warm-up pass", "Read the prepared transcript out loud slowly, focusing on breath control, clear pronunciation, and eliminating verbal fillers ('um', 'like')."],
        ["Timed pass", "Rehearse the transcript against a 60-90 second timer to build intuitive pacing and time-budget awareness."],
        ["No-screen pass", "Deliver the answer from memory without looking at notes, verifying that core structural points and metrics remain intact."],
        ["Scorecard pass", "Self-evaluate against 4 objective criteria: Clarity of structure, Technical specificity, Ownership language ('I' vs 'we'), and Quantified impact."],
        ["Revision pass", "Cut unnecessary preamble, tighten technical explanations, and sharpen the opening sentence and closing takeaway."],
      ]],
    ],
  },
  {
    title: "Company Preparation Tracks",
    tagline: "Tailored interview blueprints for Amazon, Google, Meta, and Staff/Principal loops.",
    when: "Use these in the final 2-3 weeks before your onsite loop to align with company-specific evaluation rubrics.",
    keyIdea: "Each tech giant evaluates a distinct cultural and technical signature. Calibration to the company rubric is the differentiator.",
    resources: [
      ["Amazon Jobs: Leadership Principles", "https://www.amazon.jobs/content/en/our-workplace/leadership-principles"],
      ["Google Careers: How We Hire", "https://www.google.com/about/careers/applications/how-we-hire/"],
      ["Meta Careers: Interview Prep", "https://www.metacareers.com/swe-prep/"],
      ["StaffEng: Staff Engineering Archetypes", "https://staffeng.com/guides/staff-archetypes/"],
    ],
    subsections: [
      ["Amazon Loop & Bar Raiser Track", "Excel in Amazon SDE loops and navigate Bar Raiser evaluation.", [
        ["Bar Raiser role & veto authority", "Independent calibrated interviewer ensuring the candidate raises the 50th percentile bar across all LPs; probes highest-risk signals and tests depth."],
        ["Two LPs per round mapping", "Amazon loops allocate 2 specific LPs per 60-minute round; pace responses: crisp Situation/Task (20%), heavy technical Action (60%), quantitative Result (20%)."],
        ["Working backwards & PR/FAQ method", "Customer Obsession framework: start with customer press release, customer FAQ, internal architectural FAQ before writing code."],
        ["Flywheel and two-way doors", "Distinguish Type 1 irreversible architectural decisions from Type 2 reversible decisions favoring Bias for Action and calculated risk."],
        ["Amazon quantitative impact framing", "Frame results with hard metrics: p99 latency reduction, AWS cost savings ($), availability nines (99.99%), or team velocity."],
      ]],
      ["Google GCA & Craft Track", "Master General Cognitive Ability, Googleliness, and coding rigor.", [
        ["Googleliness & collaborative leadership", "Intellectual humility, doing the right thing, navigating ambiguity, psychological safety, and building team consensus."],
        ["General Cognitive Ability (GCA) framework", "Structure hypothetical open-ended problems: clarify constraints, state assumptions, propose framework, evaluate multiple approaches, analyze edge cases."],
        ["Google system design & SRE culture", "Design with SRE principles: error budgets, SLOs/SLIs, graceful degradation, blameless post-mortems, and distributed consensus."],
        ["Google coding signal & invariants", "Restate problem, analyze constraints, narrate loop invariants, write modular production code, and dry-run with targeted edge cases."],
      ]],
      ["Meta Engineering & Speed Track", "Optimize for execution velocity, pragmatic architecture, and ownership.", [
        ["Move fast & live in the future", "High execution velocity, pragmatism, shipping incrementally, short feedback loops, and balancing velocity against technical debt."],
        ["Meta behavioral & cross-functional signals", "Demonstrate high autonomy, driving cross-team consensus, rapid conflict resolution, and delivering measured business impact."],
        ["Meta coding round pacing", "Solve two medium/hard LeetCode problems in 40 minutes; requires instant pattern recognition, zero syntax stumbling, and optimal complexity."],
        ["Meta systems & product architecture", "Focus on client-server protocols, mobile offline caching, feed ranking fan-out, and high-concurrency event pub/sub."],
      ]],
      ["Staff & Principal Engineering Track", "Demonstrate organizational leverage, architectural vision, and mentorship.", [
        ["Architectural vision & ADRs", "Set multi-year technical strategy, author Architecture Decision Records (ADRs), and balance innovation tokens against proven technology."],
        ["Organizational influence without authority", "Align executive stakeholders and disparate teams around strategic technical roadmaps through RFCs and prototype spikes."],
        ["Systemic failure prevention & mechanisms", "Transform firefighting into permanent architectural mechanisms: chaos engineering, automated canary gates, and SLA observability."],
        ["Multiplying others & sponsorship", "Grow senior engineers into staff engineers; technical sponsorship, delegating high-visibility projects, and raising hiring standards."],
      ]],
    ],
  },
];"""

def update_builder():
    with open(BUILDER_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Find const interviewPrepSections = [ ... ];
    start_marker = "const interviewPrepSections = ["
    end_marker = "function read(file) {"
    
    start_pos = content.find(start_marker)
    end_pos = content.find(end_marker)
    
    if start_pos == -1 or end_pos == -1:
        raise ValueError("Could not locate interviewPrepSections block in builder script!")
    
    new_content = content[:start_pos] + NEW_SECTIONS_CODE + "\n\n" + content[end_pos:]

    dir_name = os.path.dirname(BUILDER_PATH)
    fd, temp_path = tempfile.mkstemp(dir=dir_name, text=True)
    with os.fdopen(fd, "w", encoding="utf-8") as tmp:
        tmp.write(new_content)
    os.replace(temp_path, BUILDER_PATH)
    print("Successfully replaced interviewPrepSections in tools/build-learning-hub.mjs!")

if __name__ == "__main__":
    update_builder()
