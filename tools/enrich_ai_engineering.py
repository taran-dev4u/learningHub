#!/usr/bin/env python3
"""
Enriches ai_engineering.html with staff-level engineering depth across all 10 core sections:
- Transformers & Attention (math, MHA/MQA/GQA, RoPE, Pre-LN vs RMSNorm, KV-cache dynamics)
- Prompt Engineering & In-Context Learning (Few-shot, CoT, Self-consistency, Constrained decoding)
- RAG Pipelines (Layout parsing, HNSW/IVF/PQ, BM25+dense hybrid RRF, Cross-encoder rerankers, HyDE, Contextual retrieval)
- Agents & Tool Calling (ReAct, Plan-and-Solve, MCP standard, multi-agent frameworks)
- Evaluation & Benchmarking (Evals pyramid, LLM-as-judge, deterministic assertions, CI/CD)
- Fine-Tuning (LoRA rank decomposition, QLoRA 4-bit NF4, DPO preference loss, data efficiency)
- Production Engineering (SSE streaming, prompt caching, speculative decoding, guardrails)
- ML Fundamentals (OLS vs Gradient Descent, XGBoost/LightGBM, SVM RBF kernels, Bias-variance, data leakage)
- Deep Learning Fundamentals (Backpropagation chain rule, GELU/Swish, AdamW, CNN/ViT, MoE routing)
- MLOps & Infrastructure (Feature stores, Shadow/Canary deploys, KS-test/PSI drift, Triton/vLLM)
"""
import os, re, tempfile

AI_HTML_PATH = os.path.join(os.path.dirname(__file__), "..", "ai_engineering.html")

ENRICHMENTS = {
    # 1.1 Transformers & Attention
    "1.1.1": "<b>Mechanism:</b> Computes dynamic token alignment via Scaled Dot-Product Attention: <code>Attention(Q,K,V) = softmax(QK^T / &radic;d_k)V</code>. Scaling by <code>&radic;d_k</code> prevents the dot products from growing excessively large for high dimensions, which would push softmax into regions with vanishingly small gradients. <b>Complexity:</b> O(N&sup2;) time and memory complexity with sequence length N.",
    "1.1.2": "<b>Architecture:</b> Linearly projects queries, keys, and values into <code>h</code> distinct subspace representations: <code>MultiHead(Q,K,V) = Concat(head_1, ..., head_h)W^O</code>. <b>Trade-off:</b> Multi-Head Attention (MHA) allocates separate K/V heads per Q head; Multi-Query Attention (MQA) shares 1 K/V head across all Q heads (drastic KV-cache memory reduction); Grouped-Query Attention (GQA, e.g. LLaMA 3) groups Q heads into G subsets per K/V head, striking the optimal balance between inference throughput and modeling expressivity.",
    "1.1.3": "<b>Mechanics:</b> Inject sequence position into permutation-invariant self-attention. <b>Absolute Sinusoidal:</b> Adds fixed trigonometric frequencies <code>PE(pos, 2i) = sin(pos/10000^(2i/d))</code>. <b>Rotary Position Embedding (RoPE):</b> Multiplies Q and K representations by an orthogonal rotation matrix in 2D complex conjugate planes, ensuring dot-product depends purely on relative distance <code>m - n</code>. Enables length extrapolation via NTK-aware scaling and YaRN.",
    "1.1.4": "<b>Taxonomy:</b> <b>Encoder-only (BERT):</b> Full bidirectional attention over all tokens; optimal for classification and dense embeddings. <b>Decoder-only (GPT, LLaMA):</b> Causal autoregressive triangular masking preventing future token visibility; standard for text generation. <b>Encoder-Decoder (T5, BART):</b> Bidirectional encoder with cross-attention decoder; specialized for translation and summarization.",
    "1.1.5": "<b>Stability:</b> <b>Residuals:</b> Skip connections <code>x + SubLayer(x)</code> provide identity gradient paths, mitigating vanishing gradients in deep networks. <b>LayerNorm:</b> Pre-LN (normalizing before attention/FFN) provides stable gradient flow without warmup schedules, replacing legacy Post-LN. Modern LLMs favor <b>RMSNorm</b> (Root Mean Square Normalization), dropping mean-centering for 10-15% compute speedup.",

    # 1.2 Tokens & Tokenization
    "1.2.1": "<b>Algorithm:</b> Subword tokenization starting with raw bytes and iteratively merging the most frequent adjacent character/token pairs into a fixed vocabulary (e.g. 32k to 128k tokens). Balances vocabulary size against sequence length, eliminating out-of-vocabulary (OOV) tokens while compressing text to ~4 chars/token in English.",
    "1.2.2": "<b>Gotchas:</b> Leading whitespace (' apple' vs 'apple') produces completely different token IDs and embeddings; non-Latin Unicode scripts (Devanagari, Cyrillic, Chinese) suffer token bloat (3-8x more tokens per word than English), directly multiplying inference latency and API costs. Always inspect tokenizer output for whitespace and casing artifacts.",
    "1.2.3": "<b>Memory Dynamics:</b> KV-cache memory scales linearly with context length: <code>Bytes = 2 * 2 * n_layers * n_kv_heads * d_head * seq_len * batch_size</code>. At 128k context, a single batch KV cache consumes tens of gigabytes of VRAM. Requires vLLM PagedAttention (virtual paging eliminating fragmentation) and attention kernel optimizations (FlashAttention-2/3) to execute efficiently.",
    "1.2.4": "<b>Optimization:</b> Minimize token consumption via prompt compression (LLMLingua pruning low-perplexity tokens), prefix caching (reusing KV states across calls sharing identical system prompts), and schema minimization (abbreviated keys in JSON or using compact TOML/YAML schemas).",

    # 1.3 Training & Inference
    "1.3.1": "<b>Pretraining:</b> Unsupervised self-supervised learning predicting next token over trillions of tokens using Cross-Entropy loss. Governed by Chinchilla Scaling Laws: compute-optimal training requires scaling tokens and parameters equally (ratio ~20:1 tokens per parameter).",
    "1.3.2": "<b>Supervised Fine-Tuning:</b> Teaches conversational format and task execution using curated high-quality (prompt, response) pairs. Masked cross-entropy loss applied exclusively to target response tokens, preserving the base model's general knowledge while aligning output behavior.",
    "1.3.3": "<b>RLHF:</b> Trains an explicit scalar Reward Model on pairwise human preference comparisons (Bradley-Terry model). Updates the LLM policy using Proximal Policy Optimization (PPO) with a per-token KL-divergence penalty against the reference model to prevent reward hacking and model collapse.",
    "1.3.4": "<b>DPO Mechanics:</b> Mathematically derives the optimal policy loss directly from the Bradley-Terry preference objective: <code>L_DPO = -E[log &sigma;(&beta; log(&pi;_&theta;(y_w|x)/&pi;_ref(y_w|x)) - &beta; log(&pi;_&theta;(y_l|x)/&pi;_ref(y_l|x)))]</code>. Completely bypasses training a separate reward model and eliminates unstable PPO reinforcement learning loops.",
    "1.3.5": "<b>Inference Sampling:</b> <b>Temperature:</b> Scales logits <code>z_i / T</code> before softmax; T &rarr; 0 yields deterministic greedy argmax, while higher T flattens distribution. <b>Top-p (Nucleus):</b> Restricts sampling to the smallest cumulative probability mass &ge; p (typically 0.8-0.95). <b>Top-k:</b> Hard cutoff to top k candidate tokens. Combine low T with Top-p for reliable factual extraction.",
    "1.3.6": "<b>Search Strategies:</b> <b>Greedy Search:</b> Picks argmax token at each step (fast, prone to repetitive loops). <b>Beam Search:</b> Maintains B most probable candidate sequences (standard in translation, detrimental for open-ended creative generation). <b>Speculative Sampling:</b> Small draft model generates K speculative tokens; target model validates all K in a single forward pass, achieving 2-3x speedup.",

    # 2.1 Prompt Engineering & In-Context Learning
    "2.1.1": "<b>Technique:</b> Providing task instructions directly in natural language without input-output exemplars. Effective with modern frontier models for standard reasoning, classification, and summarization tasks where explicit zero-shot transfer suffices.",
    "2.1.2": "<b>In-Context Learning:</b> Providing 2-5 representative (input, output) demonstrations. Drastically improves structural adherence, domain-specific formatting, and edge-case handling. Dynamic few-shot uses vector similarity search to pull the most semantically relevant exemplars for each incoming query.",
    "2.1.3": "<b>Reasoning Chains:</b> Elicits multi-step intermediate reasoning before emitting the final answer ('Think step-by-step'). Allocates additional computational budget (tokens) to reasoning, overcoming feed-forward depth limitations on complex arithmetic, logic, and multi-hop planning.",
    "2.1.4": "<b>Ensemble Reasoning:</b> Samples N independent reasoning paths from the model at temperature &gt; 0.5 using Chain-of-Thought, then aggregates the final answers via majority voting. Substantially improves accuracy on mathematical and symbolic reasoning tasks by filtering random reasoning errors.",
    "2.1.5": "<b>Tree of Thoughts:</b> Generalizes CoT by exploring reasoning as an explicit tree where nodes represent intermediate thoughts. Uses heuristic evaluation prompts or lookahead search (BFS/DFS) to explore, backtrack, and evaluate multiple candidate reasoning trajectories.",
    "2.1.7": "<b>Prompt Hierarchy:</b> <b>System Prompt:</b> Out-of-band persistent developer instructions defining persona, behavioral boundaries, response schemas, and guardrails; privileged over user input. <b>User Prompt:</b> Dynamic task request containing untrusted user inputs. Always isolate user input using XML delimiters to prevent prompt injection.",

    # 2.2 Structured Output
    "2.2.1": "<b>Constrained Decoding:</b> Enforces strict JSON grammar at the token generation layer by masking non-compliant vocabulary logits at each decoding step. Guarantees 100% syntactically valid JSON matching target schemas without post-processing failures.",
    "2.2.2": "<b>Function/Tool Calling:</b> Model outputs structured JSON specifying tool name and arguments conforming to an OpenAPI/JSON-Schema specification. Execution happens on the client/application side; returned results are appended as tool-role messages for final synthesis.",
    "2.2.3": "<b>XML Delimiters:</b> Claude and Anthropic models are trained to parse and generate hierarchical XML tags (e.g. <code>&lt;context&gt;</code>, <code>&lt;scratchpad&gt;</code>, <code>&lt;response&gt;</code>). Drastically reduces cross-talk between instructions, retrieved context, and user inputs.",
    "2.2.4": "<b>Validation Frameworks:</b> Libraries (Instructor, Pydantic) that wrap LLM structured outputs with schema validation, type coercion, and automated self-correction loops (feeding validation exception tracebacks back into the model for iterative repair).",

    # 2.3 Advanced Patterns
    "2.3.1": "<b>Decomposition:</b> Deconstructs a monolithic complex prompt into a sequential Directed Acyclic Graph (DAG) of isolated single-responsibility prompts. Prevents context degradation and enables unit testing and caching of intermediate prompt stages.",
    "2.3.2": "<b>Refinement:</b> Two-pass generation pattern: Generator model produces initial output; Critic model (or generator with rubrics) evaluates against constraints (correctness, style, safety); Refiner model patches identified defects. Boosts code generation and drafting accuracy.",

    # 3.1 RAG Pipeline Stages
    "3.1.1": "<b>Ingestion:</b> Document conversion from heterogeneous formats (PDFs, DOCX, HTML, audio transcripts) into clean structured text. Layout-aware parsers (unstructured, OCR, vision LLMs) preserve tables, headers, and document hierarchy vital for semantic coherence.",
    "3.1.2": "<b>Chunking:</b> <b>Fixed-size:</b> Sliding window with token overlap (e.g. 512 tokens with 50-token overlap). <b>Recursive:</b> Splits by natural structural boundaries (paragraphs &rarr; sentences &rarr; words). <b>Semantic:</b> Computes moving embedding distance between consecutive sentences, splitting where distance spikes exceed a threshold. <b>Parent-Child:</b> Indexes small child chunks for vector search, retrieves larger parent chunk for generation.",
    "3.1.3": "<b>Dense Representations:</b> Bi-encoder models (e.g. text-embedding-3, BGE, E5) map text chunks to d-dimensional vectors (e.g. 768 or 1536 dims). Semantic similarity measured via Cosine Similarity <code>(u &middot; v) / (||u|| ||v||)</code> or Dot Product on normalized embeddings.",
    "3.1.4": "<b>ANN Indexing:</b> Approximate Nearest Neighbor algorithms: <b>HNSW:</b> Multi-layer navigable graph (skip-list on graphs); fast sub-10ms search with high recall, memory-heavy. <b>IVF (Inverted File):</b> Clusters space into Voronoi cells; searches only centroids nearest to query. <b>PQ (Product Quantization):</b> Compresses vectors into compact byte codes for 4-16x RAM savings.",
    "3.1.5": "<b>Hybrid Retrieval:</b> Combines dense semantic retrieval (captures conceptual meaning, misses rare keywords/IDs) with sparse lexical retrieval (BM25, inverted index matching exact keywords). Merged using Reciprocal Rank Fusion: <code>RRF_score(d) = &Sigma; 1 / (60 + rank_i(d))</code>.",
    "3.1.6": "<b>Cross-Encoder Reranking:</b> Re-scores top-k candidates (e.g. top 50) using a cross-encoder model (Cohere Rerank, BGE-Reranker) that performs full all-to-all attention across query and document jointly. Drastically improves precision over bi-encoder cosine ranking at modest latency cost (~20-50ms).",
    "3.1.7": "<b>Prompt Synthesis:</b> Formats retrieved chunks into the prompt context with source attribution markers, temporal metadata, and explicit grounding instructions ('Answer ONLY using retrieved context; if insufficient, state unknown') to prevent hallucinations.",

    # 3.2 Vector Databases
    "3.2.1": "<b>Managed SaaS:</b> Serverless, fully managed vector database with decoupled compute/storage and native metadata filtering. Optimized for turnkey cloud operations with zero index tuning overhead.",
    "3.2.2": "<b>Multi-Modal DB:</b> Open-source vector engine supporting graph-like cross-references, hybrid vector-BM25 search, and pluggable vectorizer modules. Written in Go, supports horizontal clustering.",
    "3.2.3": "<b>High-Performance Engine:</b> Open-source vector database written in Rust. Features payload-based pre-filtering, quantized vector storage in RAM/mmap, and rapid HNSW index updates with sub-millisecond p99 latencies.",
    "3.2.4": "<b>Embedded Store:</b> Lightweight, in-process or local client-server vector store. Excellent for local prototyping, unit tests, and single-host applications without distributed infrastructure.",
    "3.2.5": "<b>Relational Extension:</b> Open-source vector extension for PostgreSQL. Adds <code>vector</code> data type with HNSW and IVFFlat indexing. Ideal for existing Postgres stacks serving up to 10-20M vectors; enables transactional ACID joins between relational data and vector embeddings.",
    "3.2.6": "<b>In-Memory C++ Library:</b> Facebook AI's low-level library for dense vector similarity search and clustering. Provides GPU-accelerated index construction, PQ compression, and highly optimized CPU SIMD vector operations.",

    # 3.3 Advanced RAG
    "3.3.1": "<b>Query Transformation:</b> Uses an LLM to rewrite ambiguous or conversational user queries into standalone, search-optimized search terms, or decomposes complex multi-intent questions into parallel sub-queries.",
    "3.3.2": "<b>HyDE:</b> Hypothetical Document Embeddings: Prompts an LLM to generate a hypothetical answer to the query, then embeds the generated answer. Shifts query vector from the question manifold into the document manifold, boosting zero-shot recall.",
    "3.3.3": "<b>Contextual Retrieval:</b> Anthropic technique: Prepends a concise document-level context blurb to each individual chunk prior to embedding and indexing. Resolves pronoun ambiguity and isolated domain references, improving retrieval recall by up to 35-49%.",
    "3.3.4": "<b>Multi-Hop Retrieval:</b> Iterative retrieve-read-reason loop for complex questions requiring information across disparate documents. Intermediate retrieved facts generate follow-up search queries until the answer can be fully synthesized.",
    "3.3.5": "<b>RAG Triad Metrics:</b> Evaluates RAG quality across 3 orthogonal dimensions: <b>Context Relevance:</b> Are retrieved chunks focused on the query? <b>Groundedness / Faithfulness:</b> Is the answer mathematically derived from the context? <b>Answer Relevance:</b> Does the answer directly address the user's prompt?",
    "3.3.6": "<b>Context vs RAG:</b> Long-context LLMs (1M+ tokens) allow dumping entire document corpora directly into context, but suffer from high latency, linear cost scaling, and 'Lost in the Middle' attention degradation. Hybrid RAG (filtering 10k relevant tokens via vector search) remains 10x faster and cheaper.",

    # 4.1 Agent Patterns
    "4.1.1": "<b>Basic Tool Loop:</b> Simplest agent loop: System prompt defines tools &rarr; model emits tool call &rarr; runtime executes tool &rarr; tool output appended &rarr; model generates final response or triggers next tool call until termination.",
    "4.1.2": "<b>ReAct Pattern:</b> Interleaves Reasoning ('Thought') and Action ('Act' + 'Observation') steps. Explicit thoughts allow the agent to decompose tasks, track goal progress, handle exceptions, and formulate informed tool queries.",
    "4.1.3": "<b>Plan-and-Solve:</b> Decouples planning from execution: Planner model generates a structured list of subtasks; Executor agent iterates through subtasks sequentially, updating state. Reduces wandering and token costs on long-horizon workflows.",
    "4.1.4": "<b>Intent Routing:</b> Lightweight classifier (small model, embeddings, or regex) categorizes incoming user input and routes to specialized downstream prompts, agents, or RAG collections, minimizing latency and cost.",
    "4.1.5": "<b>Fan-Out Execution:</b> Orchestrator decomposes independent subtasks (e.g. searching 5 distinct sources), executes tool invocations in parallel async workers, and joins results in an aggregator prompt for final synthesis.",
    "4.1.6": "<b>Hierarchical Multi-Agent:</b> Supervisor agent delegates sub-problems to specialized worker agents (e.g. ResearchAgent, CodingAgent, ReviewAgent). Each worker maintains its own isolated context, preventing context contamination.",
    "4.1.7": "<b>Self-Correction Loop:</b> Generator agent produces artifact; Critic/Evaluator agent runs unit tests or checks criteria; if failed, feedback is returned to Generator for iterative refinement until passing or max retry budget reached.",

    # 4.2 Tool Design
    "4.2.1": "<b>Schema Definition:</b> Precise JSON Schema definitions for function inputs and outputs. Specify required fields, type constraints, enums, and clear docstrings. Avoid overly broad or nested input structures.",
    "4.2.2": "<b>Description Engineering:</b> The tool description is a prompt instructing the LLM when, why, and how to use the tool. Include clear guidance on tool boundaries, parameter semantics, and sample inputs.",
    "4.2.3": "<b>Defensive Execution:</b> Tools must catch runtime exceptions and return structured, human-readable error messages ('Error: Table users does not exist. Did you mean user_accounts?') enabling the agent to self-correct rather than crashing.",
    "4.2.4": "<b>Model Context Protocol:</b> Open standard protocol created by Anthropic in 2024 defining a standardized JSON-RPC 2.0 communication layer between LLM clients and local/remote tool, prompt, and resource providers.",

    # 4.3 Agent Frameworks
    "4.3.1": "<b>Stateful Workflow Graph:</b> LangChain's graph-based orchestration framework (LangGraph). Models agent state as a cyclical state machine with explicit persistence, checkpoints, human-in-the-loop approvals, and time-travel debugging.",
    "4.3.2": "<b>Data Framework:</b> Specialized for ingestion, indexing, and querying private data. Offers hierarchical indices, query routing engines, and document agents optimized for data retrieval pipelines.",
    "4.3.3": "<b>Programmatic Prompts:</b> Replaces manual prompt strings with declarative Python modules. Uses teleprompters (optimizers) to automatically compile and optimize prompt demonstrations and few-shot exemplars against an objective metric.",
    "4.3.4": "<b>Collaborative Agents:</b> Multi-agent orchestration frameworks (CrewAI, AutoGen) simulating conversational interactions between autonomous role-playing agents. Prone to token explosion and non-deterministic loops; requires strict guardrails.",
    "4.3.5": "<b>Production Architecture:</b> Industry consensus for production agents: avoid monolithic abstraction frameworks in favor of raw provider SDKs (OpenAI, Anthropic) wrapped in clean, deterministic Python/Go loops with explicit state management.",

    # 5.1 Evaluation Approaches
    "5.1.1": "<b>Lexical Metrics:</b> <b>BLEU:</b> Precision of n-gram overlaps (standard in machine translation). <b>ROUGE:</b> Recall of n-gram overlaps (standard in summarization). Brittle for open-ended LLM outputs because they penalize valid semantic paraphrasing.",
    "5.1.2": "<b>Model-Based Scoring:</b> <b>Perplexity:</b> Exponential of cross-entropy loss, measures how surprised a language model is by text. <b>Embedding Distance:</b> Cosine distance between candidate and reference embeddings. Fast, reference-free, but blind to factual contradictions.",
    "5.1.3": "<b>Automated Judge:</b> Prompts a frontier model (GPT-4o, Claude 3.5 Sonnet) with a detailed grading rubric to score candidate answers. <b>Mitigations:</b> Mitigate position bias by swapping candidate order; use chain-of-thought grading; calibrate against human judgements.",
    "5.1.4": "<b>Gold Standard:</b> Double-blind Side-by-Side (SxS) human ratings or Likert-scale evaluations. Crucial for establishing baseline ground truth and calibrating automated LLM judges, but slow and expensive.",
    "5.1.5": "<b>Deterministic Assertions:</b> Programmatic unit checks: JSON schema validation, regex pattern matching, Python code execution in sandboxes, and SQL execution assertions against test databases. Fast, reliable, and free.",

    # 5.2 Build an Eval Pipeline
    "5.2.1": "<b>Curated Golden Dataset:</b> Assemble 50-200 representative, hard test cases covering core user journeys, adversarial prompts, and production edge cases. Treat the dataset as living code updated upon every production regression.",
    "5.2.2": "<b>CI/CD Gateways:</b> Run automated evaluation suites on every prompt or pipeline pull request. Block merges if composite accuracy drops below threshold or if critical safety assertions fail.",
    "5.2.3": "<b>Production Experiments:</b> Route a percentage of live production traffic between prompt variants (A/B testing). Measure downstream business metrics (click-through, completion rates, thumbs up/down, session retention).",
    "5.2.4": "<b>Observability Platforms:</b> Dedicated LLM monitoring tools (Langfuse, LangSmith, Phoenix) tracking complete execution traces, token costs, latency breakdowns, and user feedback in production.",
    "5.2.5": "<b>Adversarial Red-Teaming:</b> Systematic testing against OWASP Top 10 for LLMs: prompt injection, jailbreaks, data exfiltration, and unsafe tool execution. Automated fuzzing with adversarial prompt generators.",

    # 6.1 Fine-Tuning Approaches
    "6.1.1": "<b>Soft Prompts:</b> Prepends learnable continuous embedding vectors to frozen model inputs. Requires negligible training memory, but exhibits lower expressivity and cannot generalize across distinct task paradigms.",
    "6.1.2": "<b>LoRA & QLoRA:</b> <b>LoRA:</b> Freezes base weights W0 &isin; R^(d&times;k) and injects trainable rank decomposition matrices: <code>&Delta;W = (B &times; A) * (&alpha; / r)</code>, where r &ll; min(d,k), cutting trainable parameters by 99%. <b>QLoRA:</b> Quantizes base model to 4-bit NormalFloat (NF4), adds Double Quantization and Paged Optimizers, enabling fine-tuning of 70B models on a single 48GB GPU.",
    "6.1.3": "<b>Full Parameter Updates:</b> Modifies 100% of network weights using distributed backpropagation (DeepSpeed ZeRO-3, FSDP). Highly resource-intensive, risks catastrophic forgetting of general reasoning, and requires high learning rate warmup schedules.",
    "6.1.4": "<b>Instruction Alignment:</b> Fine-tunes a pretrained base model on conversational (instruction, response) datasets. Transforms raw next-token completion engines into steerable assistant models that adhere to safety and system guidelines.",
    "6.1.5": "<b>Preference Optimization:</b> Aligns model outputs with human preference pairs (chosen vs rejected) using DPO, KTO (Kahneman-Tversky Optimization), or ORPO. Eliminates the complex reinforcement learning reward models of legacy PPO pipelines.",
    "6.1.6": "<b>Decision Matrix:</b> <b>Prompting:</b> First choice for 80% of tasks; instant iteration. <b>RAG:</b> Required for dynamic, private, or real-time factual knowledge. <b>Fine-Tuning:</b> Best for teaching style, tone, rigid output schemas, specialized syntax, or latency reduction via distillation into smaller models. Never fine-tune solely to inject factual data.",

    # 6.2 Data + Training Infrastructure
    "6.2.1": "<b>Data Quality over Volume:</b> The LIMA paper demonstrated that 1,000 meticulously curated, high-diversity training examples produce superior conversational alignment compared to 100,000 noisy, scraped examples. Deduplicate and filter rigorously.",
    "6.2.2": "<b>Hyperparameters:</b> Learning rate: 1e-4 to 2e-4 for LoRA, 1e-5 to 5e-6 for full fine-tuning with cosine decay schedule; Batch size: 32-128; Epochs: 2-4 (avoid overfitting); LoRA rank r=8-64, alpha=16-128 (typically alpha = 2 * r).",
    "6.2.3": "<b>Distributed Training:</b> <b>FSDP (Fully Sharded Data Parallel):</b> Shards model weights, gradients, and optimizer states across GPUs. <b>ZeRO (Zero Redundancy Optimizer):</b> ZeRO-1 shards optimizer states, ZeRO-2 adds gradients, ZeRO-3 shards model parameters, eliminating memory duplication.",
    "6.2.4": "<b>Quantization Formats:</b> <b>GGUF:</b> CPU/GPU format for llama.cpp. <b>AWQ / GPTQ:</b> 4-bit weight-only quantization algorithms with activation-aware outlier protection, preserving near FP16 perplexity with 3x faster memory bandwidth.",

    # 7.1 Performance
    "7.1.1": "<b>Streaming (SSE):</b> Server-Sent Events stream generated tokens chunk-by-chunk over HTTP/2, reducing perceived Time-to-First-Token (TTFT) from several seconds to 200-400ms, drastically improving user experience.",
    "7.1.2": "<b>Prefix Caching:</b> Caches precomputed KV-cache states for shared prompt prefixes (e.g. system instructions, static RAG context). Reduces Time-to-First-Token by up to 80% and cuts API input token costs by 50-90% on OpenAI and Anthropic.",
    "7.1.3": "<b>Tiered Cascades:</b> Evaluates incoming queries with a fast, cheap model (e.g. GPT-4o-mini, Claude 3.5 Haiku); inspects output confidence or perplexity; escalates complex or uncertain queries to a flagship frontier model. Saves 60-80% of operational inference spend.",
    "7.1.4": "<b>Batching & Dynamic Batching:</b> <b>Offline Batching:</b> Non-interactive tasks submitted via batch APIs for 50% discount. <b>Continuous Batching (vLLM, TGI):</b> Iteration-level scheduling that inserts new requests and evicts finished sequences dynamically at each token step, maximizing GPU saturation.",
    "7.1.5": "<b>Speculative Decoding:</b> A small draft model speculatively generates K tokens autoregressively; the large target model evaluates all K tokens in a single parallel forward pass using causal masking. Yields 2x-3x speedup with zero degradation in mathematical output distribution.",

    # 7.2 Reliability
    "7.2.1": "<b>Exponential Backoff with Jitter:</b> Standard retry algorithm for HTTP 429 (Rate Limit) and 503 errors: <code>sleep = min(cap, base * 2^attempt) + uniform(0, jitter)</code>. Full jitter prevents synchronized thundering herd retries against upstream LLM gateways.",
    "7.2.2": "<b>Multi-Provider Redundancy:</b> Gateway layer (LiteLLM, Portkey) that routes requests across diverse LLM providers (AWS Bedrock, Azure OpenAI, GCP Vertex) with automated health checks, circuit breakers, and automatic failover.",
    "7.2.3": "<b>Timeout & Cancellation:</b> Enforce strict connection and read timeouts. If streaming tokens stall or if generation exceeds target SLAs, immediately abort the downstream request to conserve server resources and notify the client.",
    "7.2.4": "<b>Input/Output Guardrails:</b> Synchronous inspection layers (NeMo Guardrails, Llama Guard): filters toxic prompts, jailbreak patterns, and off-topic queries before model invocation; validates model responses against safety policies before returning.",

    # 7.3 Observability
    "7.3.1": "<b>Full-Stack Tracing:</b> OpenTelemetry-compatible tracing across all agent hops, tool executions, vector searches, and model calls. Captures exact prompt payloads, token counts, latency breakdowns, and system errors.",
    "7.3.2": "<b>FinOps Cost Tracking:</b> Attributing token consumption, cache hits, and infrastructure spend down to individual users, organizations, and application features. Sets automated spend alerts and budget circuit breakers.",
    "7.3.3": "<b>Production Quality Drift:</b> Continuous offline evaluation sampling production traces. Measures drift in user satisfaction, response length, topic distribution, and LLM-as-a-judge quality scores over time.",

    # 7.4 Security
    "7.4.1": "<b>Prompt Injection Defense:</b> Mitigates Direct (jailbreaks) and Indirect (malicious content in retrieved web pages/documents) injection. Enforces strict privilege separation: user/document data placed in isolated XML/JSON tags; system prompts instruct model to treat tagged data strictly as passive data, never executable instructions.",
    "7.4.2": "<b>Output Sanitization:</b> Never execute raw LLM outputs directly. Generated SQL must run with read-only scoped database credentials with query timeouts; generated Python code must execute in isolated ephemeral sandboxes (Docker, Firecracker microVMs, gVisor); generated HTML must be sanitized against XSS.",
    "7.4.3": "<b>PII & Compliance:</b> Client-side PII scrubbing (Presidio, regex) masking credit card numbers, SSNs, and email addresses before payloads leave the network perimeter. Enforce Data Processing Agreements (DPAs) with zero data-retention guarantees.",

    # 8.1 Supervised Learning
    "8.1.1": "<b>Foundations:</b> <b>Linear Regression:</b> Solves OLS closed-form normal equation <code>&beta; = (X^T X)^(-1) X^T y</code> or minimizes MSE via gradient descent; assumes linearity, homoscedasticity, and normal residuals. <b>Logistic Regression:</b> Models log-odds via sigmoid link <code>&sigma;(z) = 1 / (1 + e^(-z))</code>; optimized via Maximum Likelihood Estimation with binary cross-entropy loss.",
    "8.1.2": "<b>Greedy Partitioning:</b> Non-parametric recursive binary splitting selecting feature and split threshold maximizing Information Gain (Entropy reduction) or minimizing Gini Impurity: <code>Gini = 1 - &Sigma; p_i&sup2;</code>. Highly interpretable; prone to high variance and overfitting unless constrained by max depth, min samples per leaf, or cost-complexity pruning.",
    "8.1.3": "<b>Bagging Ensemble:</b> Bootstrap Aggregation: Trains B independent deep decision trees on random bootstrap subsets of data with random feature subsampling (typically &radic;p features). Drastically reduces prediction variance without increasing bias; Out-Of-Bag (OOB) samples provide unbiased validation without explicit holdout sets.",
    "8.1.4": "<b>Boosting Frameworks:</b> Trains an additive sequence of shallow decision trees, where each tree fits the negative gradient (pseudo-residuals) of the loss function. <b>XGBoost:</b> Second-order Taylor expansion with exact Hessian weighting and tree regularization. <b>LightGBM:</b> Histogram binning and Gradient-based One-Side Sampling (GOSS). <b>CatBoost:</b> Symmetric oblivious trees and target statistics.",
    "8.1.5": "<b>Max-Margin Separation:</b> Finds optimal separating hyperplane maximizing geometric margin <code>2 / ||w||</code> subject to correct classification constraints. Soft-margin introduces slack variables &xi;_i with penalty C. <b>Kernel Trick:</b> Implicitly maps data into infinite-dimensional Hilbert space via RBF kernel <code>K(x, x') = exp(-&gamma; ||x - x'||&sup2;)</code>.",
    "8.1.6": "<b>Instance-Based Learning:</b> Non-parametric lazy learner storing training instances directly; classifies new queries based on majority label of k nearest neighbors in Euclidean or Manhattan distance. Inefficient at inference (O(N &times; D)); severely degraded by the curse of dimensionality in high dimensions without PCA.",
    "8.1.7": "<b>Probabilistic Classifier:</b> Computes posterior probability via Bayes' Rule: <code>P(C|X) &prop; P(C) &Pi; P(x_i|C)</code>, assuming conditional independence of features given the class. Extremely fast, robust to irrelevant features, and provides a strong baseline for high-dimensional text classification and spam detection.",

    # 8.2 Unsupervised Learning
    "8.2.1": "<b>Centroid Clustering:</b> Iterative Lloyd's algorithm: 1. Assign points to nearest centroid in Euclidean space; 2. Recalculate centroids as the arithmetic mean of assigned points. Sensitive to initialization (mitigated by k-means++ distance-weighted seeding); finds spherical clusters, requires pre-specifying k via Elbow method or Silhouette score.",
    "8.2.2": "<b>Hierarchical Dendrograms:</b> Agglomerative (bottom-up) clustering starting with individual points as clusters, iteratively merging closest pairs based on linkage criteria (Ward's minimum variance, complete linkage, single linkage). Produces an interpretable dendrogram tree without pre-specifying cluster counts.",
    "8.2.3": "<b>Density-Based Clustering:</b> Groups dense core points with &ge; MinPts within an &epsilon;-neighborhood; expands clusters along density-connected paths. Automatically identifies arbitrary non-convex cluster shapes and isolates low-density points as explicit noise outliers.",
    "8.2.4": "<b>Linear Dimensionality Reduction:</b> Orthogonal linear projection onto directions of maximum variance. Mathematically equivalent to computing eigenvectors of the feature covariance matrix <code>X^T X</code>. Preserves global variance structure while compressing feature dimensionality.",
    "8.2.5": "<b>Non-Linear Manifold Projection:</b> <b>t-SNE:</b> Minimizes KL divergence between student-t distribution in low dimensions and Gaussian distribution in high dimensions; preserves local neighborhoods for visualization. <b>UMAP:</b> Fuzzy simplicial sets based on Riemannian geometry; faster runtime and preserves both local and global topological structure.",

    # 8.3 Model Evaluation
    "8.3.1": "<b>Data Partitioning:</b> Train / Validation / Test holdouts (e.g. 70/15/15). Stratified splits ensure identical target class proportions across folds. For time-series, temporal walk-forward splitting is mandatory to prevent future lookahead leakage.",
    "8.3.2": "<b>Cross-Validation:</b> Partitions dataset into K equal disjoint folds. Iteratively trains on K-1 folds and evaluates on the remaining fold, rotating K times. Averages metric across iterations to produce an unbiased estimate of generalization performance with variance confidence intervals.",
    "8.3.3": "<b>Classification Metrics:</b> Accuracy is misleading under class imbalance. <b>Precision:</b> TP / (TP + FP) (minimizes false alarms). <b>Recall:</b> TP / (TP + FN) (minimizes missed detections). <b>F1:</b> Harmonic mean. <b>ROC-AUC:</b> Threshold-independent ranking ability. <b>PR-AUC:</b> Critical when positive class is rare (&lt;1%).",
    "8.3.4": "<b>Regression Metrics:</b> <b>MAE:</b> Mean Absolute Error (L1 loss: predicts median, robust to extreme outliers). <b>RMSE:</b> Root Mean Squared Error (L2 loss: predicts mean, heavily penalizes large errors). <b>R&sup2;:</b> Coefficient of determination measuring proportion of target variance explained by model.",
    "8.3.5": "<b>Error Decomposition:</b> <code>Expected Error = Bias&sup2; + Variance + Irreducible Noise</code>. High Bias (underfitting) fails to capture underlying patterns; addressed by adding model complexity. High Variance (overfitting) models training noise; addressed by regularization, pruning, or bagging ensembles.",
    "8.3.6": "<b>Data Leakage Prevention:</b> Information from target or test split inadvertently contaminating the training feature pipeline. <b>Golden Rule:</b> All transformations (StandardScaler, Imputer, Target Encoding) MUST fit strictly on the training partition and only transform the test partition. Never scale before splitting.",

    # 8.4 Feature Engineering
    "8.4.1": "<b>Continuous Transformations:</b> <b>StandardScaler:</b> Zero mean, unit variance <code>(x - &mu;) / &sigma;</code> (for gradient-based models). <b>MinMaxScaler:</b> Bounds to [0,1]. <b>Log1p:</b> Compresses long-tailed right-skewed distributions. <b>Quantile Binning:</b> Discretizes non-linear continuous features into equal-frequency ordinal buckets.",
    "8.4.2": "<b>Categorical Transformations:</b> <b>One-Hot:</b> Binary dummy indicators for low cardinality (&lt;10). <b>Target Encoding:</b> Replaces category with target mean smoothed by empirical Bayes prior (prevents overfitting high-cardinality IDs). <b>Entity Embeddings:</b> Learns dense d-dimensional vectors in neural networks.",
    "8.4.3": "<b>Text Representations:</b> <b>TF-IDF:</b> <code>TF(t, d) &times; log(N / DF(t))</code> discounts frequent stopwords while highlighting discriminative domain keywords. <b>Sentence Embeddings:</b> Pretrained bi-encoders mapping phrases into semantic vector spaces.",
    "8.4.4": "<b>Imputation Mechanics:</b> Characterize missingness (MCAR vs MAR). Simple: Mean/median imputation paired with an explicit binary missingness indicator column (<code>is_missing</code>). Advanced: Iterative chained equations (MICE) or kNN imputation. Tree models (XGBoost) learn default split directions for missing values natively.",
    "8.4.5": "<b>Selection Methods:</b> <b>Filter:</b> Pearson/Spearman correlation or mutual information ranking. <b>Wrapper:</b> Recursive Feature Elimination (RFE) pruning weakest features iteratively. <b>Embedded:</b> L1 Lasso penalty driving coefficients to zero, performing intrinsic feature selection.",

    # 9.1 Deep Learning Core Concepts
    "9.1.1": "<b>Reverse-Mode Differentiation:</b> Computes exact partial derivatives <code>&part;L / &part;W</code> using the multivariable chain rule on directed acyclic computational graphs. Forward pass computes intermediate activations; backward pass propagates adjoint gradient vectors from loss to parameters.",
    "9.1.2": "<b>Non-Linear Mappings:</b> Introduces representational capacity to multi-layer networks. <b>ReLU:</b> <code>max(0, x)</code> (fast, mitigates vanishing gradients, suffers from dying ReLU). <b>GELU:</b> <code>x &Phi;(x)</code> (smooth Gaussian error gating, standard in BERT and GPT). <b>Swish/SiLU:</b> <code>x &sigma;(&beta;x)</code> (used in LLaMA architectures).",
    "9.1.3": "<b>Optimization Objectives:</b> <b>Cross-Entropy:</b> <code>-&Sigma; y_i log(p_i)</code> for classification (minimizes KL-divergence between empirical and predicted distributions). <b>MSE / Huber Loss:</b> For continuous regression. <b>InfoNCE / Contrastive:</b> Maximizes similarity of positive pairs against negative batches in metric embedding learning.",
    "9.1.4": "<b>Adaptive Optimization:</b> <b>SGD with Momentum:</b> Accelerates through ravines by accumulating past velocity. <b>Adam:</b> Combines first-moment momentum and second-moment uncentered variance estimation. <b>AdamW:</b> Decouples L2 weight decay from gradient updates, resolving weight magnitude decay issues in Transformers.",
    "9.1.5": "<b>Generalization Guards:</b> <b>Dropout:</b> Randomly zeroes activations with probability p during training, simulating an exponential ensemble of sub-networks. <b>Weight Decay:</b> Penalizes large L2 weight norms <code>0.5 &lambda; ||W||&sup2;</code>. <b>Data Augmentation:</b> Mixup and CutMix forcing invariant representations.",
    "9.1.6": "<b>Normalization Mechanics:</b> <b>Batch Normalization:</b> Normalizes across mini-batch dimension; unstable with small batches and autoregressive sequences. <b>Layer Normalization:</b> Normalizes across feature channels for each token independently: <code>(x - &mu;) / &radic;(&sigma;&sup2; + &epsilon;) &times; &gamma; + &beta;</code>. Indispensable for sequence stability.",

    # 9.2 Architectures
    "9.2.1": "<b>Spatial Feature Extraction:</b> Leverages discrete 2D convolutions with weight sharing and local receptive fields to encode translation-invariant patterns. <b>ResNet:</b> Introduced identity shortcut connections <code>F(x) + x</code>, enabling training of 100+ layer networks without gradient degradation.",
    "9.2.2": "<b>Recurrent State Updates:</b> Processes sequences sequentially: <code>h_t = tanh(W_h h_(t-1) + W_x x_t)</code>. <b>LSTM:</b> Introduces constant error carousel cell states governed by Forget, Input, and Output gates, mitigating vanishing gradients but constrained by non-parallelizable sequential execution.",
    "9.2.3": "<b>Attention Supremacy:</b> Replaces recurrence with parallel self-attention mechanisms. Modern Vision Transformers (ViT) divide images into 16x16 flattened patches, projecting them into transformer token embeddings to outperform CNNs on large datasets without spatial inductive bias.",
    "9.2.4": "<b>Iterative Denoising:</b> Generative models formulating generation as reversing a thermodynamic diffusion process. Forward process incrementally injects Gaussian noise into data; reverse process trains a U-Net or DiT (Diffusion Transformer) to predict and subtract noise at timestep t (DDPM, Flow Matching).",
    "9.2.5": "<b>Sparse Activation:</b> Replaces dense feed-forward blocks with E parallel expert networks. A parameterized gating router computes a softmax distribution over experts, routing each token to only the top-k experts (e.g. Mixtral 8x7B activates 2 of 8 experts per token), scaling capacity with constant FLOPs.",

    # 10.1 Model Lifecycle
    "10.1.1": "<b>Experiment Tracking:</b> Platforms (MLflow, Weights & Biases) that log git commit hash, hyperparameters, dataset version, loss curves, and artifact checkpoints across distributed training runs, enabling perfect scientific reproducibility.",
    "10.1.2": "<b>Dataset Versioning:</b> Tools (DVC, LakeFS) treating large binary datasets, feature matrices, and model weights with Git-like immutability, branching, and content-addressed storage pointers backed by S3/GCS buckets.",
    "10.1.3": "<b>Central Governance:</b> Model registry managing artifact metadata, lineage graphs, input/output tensor signature contracts, and promotion lifecycle stages (Development &rarr; Staging &rarr; Production) with cryptographic digest validation.",
    "10.1.4": "<b>Unified Feature Stores:</b> Systems (Feast, Tecton) bridging offline analytical feature extraction (Snowflake, Spark) and low-latency online inference lookups (Redis, DynamoDB). Guarantees point-in-time correctness to eliminate train-serve feature skew.",

    # 10.2 Deployment Patterns
    "10.2.1": "<b>Offline Scoring:</b> High-throughput asynchronous batch inference scheduled on Spark or Ray; scores millions of records offline and writes precomputed embeddings or predictions to distributed key-value stores for sub-millisecond retrieval.",
    "10.2.2": "<b>Low-Latency Serving:</b> Synchronous microservices (FastAPI, Triton Inference Server, TorchServe) executing model forward passes on incoming requests. Uses dynamic request batching, model concurrency, and TensorRT compilation to meet sub-50ms p99 SLAs.",
    "10.2.3": "<b>Event-Driven Prediction:</b> Real-time inference pipelines consuming event streams directly from Kafka or AWS Kinesis using stateful stream processors (Apache Flink), emitting enriched prediction events downstream with minimal latency.",
    "10.2.4": "<b>Dark Launch:</b> Clones live production request traffic and asynchronously forwards payloads to a shadow model without returning predictions to end clients. Measures real-world inference latency, memory pressure, and output variance with zero user impact.",
    "10.2.5": "<b>Progressive Traffic Shifting:</b> Deploys candidate model behind an API gateway/service mesh (Envoy, Istio); shifts traffic incrementally (1% &rarr; 5% &rarr; 25% &rarr; 100%) while continuously comparing error rates, p99 latency, and business metrics against production baseline.",

    # 10.3 Monitoring
    "10.3.1": "<b>Input Distribution Shift:</b> Detects when inference feature distributions drift from training data <code>P(X)</code>. Employs statistical tests: Kolmogorov-Smirnov (KS) test for numerical variables, Population Stability Index (PSI &gt; 0.2 flags severe drift), and Earth Mover's Distance.",
    "10.3.2": "<b>Relationship Shift:</b> Detects shifts in the relationship between input features and target labels <code>P(Y|X)</code> (e.g. macro changes in user purchasing habits). Requires delayed ground truth labels; tracked via rolling accuracy/F1 windows.",
    "10.3.3": "<b>Inference Telemetry:</b> Real-time observability tracking model throughput (QPS), p50/p95/p99 inference latency, GPU memory/utilization, token consumption rates, and prediction distribution entropy via Prometheus and Grafana.",
    "10.3.4": "<b>Data Flywheel:</b> Asynchronous logging of production inference payloads (features, predictions, latency) with PII redaction to data lakes. Samples low-confidence predictions to feed active learning and fine-tuning pipelines.",

    # 10.4 Infrastructure
    "10.4.1": "<b>ML Orchestration on K8s:</b> Kubernetes-native ML platforms (Kubeflow, KServe) providing declarative custom resource definitions (PyTorchJob, InferenceService) for autoscaling inference pods based on GPU metrics and queue depth.",
    "10.4.2": "<b>Hardware Utilization:</b> Maximizing GPU ROI via Multi-Instance GPU (MIG) slicing, NVIDIA Triton dynamic batching, vLLM continuous batching, and spot/preemptible GPU instance autoscaling with checkpoint recovery.",
    "10.4.3": "<b>Automated ML Pipelines:</b> Automated CI/CD pipelines executing on code or data triggers: runs data validation suites, trains baseline models, evaluates against regression benchmarks, checks model bias, and deploys canaries."
}

def enrich_ai_html():
    with open(AI_HTML_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    count = 0
    for cid, text in ENRICHMENTS.items():
        pattern = re.compile(
            rf'(<li\b[^>]*data-cid="{re.escape(cid)}"[^>]*>[\s\S]*?<div class="cname">[\s\S]*?<\/div>)\s*<div style="font-size:11.5px;color:var\(--text-faint\);margin-top:2px">([\s\S]*?)<\/div>',
            re.IGNORECASE
        )
        content, n = pattern.subn(
            rf'\1<div style="font-size:11.5px;color:var(--text-faint);margin-top:2px">{text}</div>',
            content
        )
        count += n

    dir_name = os.path.dirname(AI_HTML_PATH)
    fd, temp_path = tempfile.mkstemp(dir=dir_name, text=True)
    with os.fdopen(fd, "w", encoding="utf-8") as tmp:
        tmp.write(content)
    os.replace(temp_path, AI_HTML_PATH)
    print(f"Enriched {count} concepts in ai_engineering.html!")

if __name__ == "__main__":
    enrich_ai_html()
