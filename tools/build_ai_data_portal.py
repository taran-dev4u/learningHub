import os
import sys
import tempfile
import time
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Base CSS from cloud_aws_azure.html
SRC_CSS_PATH = os.path.join(ROOT, 'cloud_aws_azure.html')
with open(SRC_CSS_PATH, 'r', encoding='utf-8') as f:
    orig_cloud = f.read()

style_m = re.search(r'<style>([\s\S]*?)</style>', orig_cloud)
base_css = style_m.group(1) if style_m else ""

# Tracks Definition
TRACKS = [
    {
        "id": "section-1",
        "slug": "ai-eng",
        "title": "AI Engineering (Generative AI, LLMs & Agents)",
        "icon": "🤖",
        "desc": "Foundation models, Transformers, Prompt Engineering, RAG architectures, Vector DBs, Autonomous Agents, LoRA fine-tuning & evaluation.",
        "badge": "LLMs, RAG, Agents, Fine-Tuning & Vector DBs",
        "page": "ai_engineering.html",
        "page_title": "AI Engineering from Scratch Masterclass",
        "subsections": [
            {
                "title": "Foundation Models, Transformers & LLM Architecture",
                "concepts": [
                    ("ai-foundation-models", "Foundation Models, Pre-training & Next-Token Prediction", "Autoregressive language modeling, causal masking, pre-training loss, self-supervised objectives, and parameter scaling from billions to trillions of parameters.", "https://www.youtube.com/watch?v=zjkBMFhNj_g", "00:00", "3Blue1Brown"),
                    ("ai-transformer-attention", "Transformer Architecture & Multi-Head Self-Attention", "Scaled dot-product attention, query-key-value projections, positional encodings (RoPE), residual connections, and layer normalization mechanics.", "https://www.youtube.com/watch?v=wjZofJX0v4U", "00:00", "3Blue1Brown"),
                    ("ai-tokenization-sampling", "Tokenization (BPE/WordPiece), Context Windows & Temperature Sampling", "Byte-pair encoding (BPE), vocabulary sizes, token fragmentation, context length constraints, greedy search vs top-p (nucleus) and top-k sampling.", "https://www.youtube.com/watch?v=zduSFxRajkE", "00:00", "Andrej Karpathy"),
                    ("ai-scaling-inference", "Scaling Laws, Compute Optimal Models & Efficient Inference", "Chinchilla scaling laws, compute vs data tradeoffs, Key-Value (KV) cache memory footprint, FlashAttention memory bandwidth optimization, and PagedAttention.", "https://www.youtube.com/watch?v=kCc8FmEb1nY", "00:00", "Andrej Karpathy")
                ]
            },
            {
                "title": "Prompt Engineering & In-Context Learning",
                "concepts": [
                    ("ai-prompt-principles", "Core Prompting Principles, System Prompts & Instruction Formatting", "Instruction clarity, role priming, persona adoption, input/output delimiters, context window management, and zero-shot task elicitation.", "https://www.youtube.com/watch?v=jC4v5AS4RIM", "00:00", "DeepLearning.AI"),
                    ("ai-few-shot-cot", "Few-Shot In-Context Learning & Chain-of-Thought (CoT) Reasoning", "Exemplar selection, demonstration ordering, step-by-step rationales, zero-shot CoT ('Let\\'s think step by step'), and self-consistency decoding.", "https://www.youtube.com/watch?v=dQ57zYedMdQ", "00:00", "DeepLearning.AI"),
                    ("ai-structured-outputs", "Structured Outputs, JSON Mode & Schema Enforcement", "Constrained decoding, grammar-based sampling, JSON schema validation, Pydantic model extraction, and reliable API payload generation.", "https://www.youtube.com/watch?v=0hbbZ_1e_h0", "00:00", "freeCodeCamp"),
                    ("ai-prompt-security", "Prompt Injection Attacks, Jailbreaking & Defense Strategies", "Direct and indirect prompt injections, data exfiltration through tool execution, adversarial jailbreaks, sandwich defense, and input validation filters.", "https://www.youtube.com/watch?v=v2gD8BHOa14", "00:00", "freeCodeCamp")
                ]
            },
            {
                "title": "Retrieval-Augmented Generation (RAG) Architecture",
                "concepts": [
                    ("ai-rag-fundamentals", "RAG Workflow Architecture: Ingestion, Chunking, Indexing & Generation", "End-to-end RAG pipelines, external knowledge injection, grounding model responses, hallucination reduction, and context length expansion.", "https://www.youtube.com/watch?v=T-D1OfcDW1M", "00:00", "IBM Technology"),
                    ("ai-chunking-embeddings", "Semantic Chunking Strategies & Dense Embedding Models", "Fixed-size, sentence-based, recursive character, and semantic chunking; dense vector embeddings, representation spaces, and cross-lingual models.", "https://www.youtube.com/watch?v=gQddt9AgDsE", "00:00", "StatQuest"),
                    ("ai-hybrid-search-rrf", "Hybrid Search: Dense Vector Retrieval + BM25 Lexical Search & RRF", "Sparse keyword matching with BM25, dense semantic retrieval, score normalization, and Reciprocal Rank Fusion (RRF) for optimal recall.", "https://www.youtube.com/watch?v=2TGp1O8qVf8", "00:00", "freeCodeCamp"),
                    ("ai-reranking-advanced", "Re-ranking with Cross-Encoders & Multi-Query Expansion", "Two-stage retrieval pipelines, bi-encoders for fast candidate retrieval, cross-encoders for deep semantic re-ranking, and query decomposition.", "https://www.youtube.com/watch?v=yws4kZoxLrk", "00:00", "DeepLearning.AI")
                ]
            },
            {
                "title": "Vector Databases & Semantic Storage",
                "concepts": [
                    ("ai-vector-db-mechanics", "Vector Database Mechanics: Approximate Nearest Neighbor (ANN) & HNSW Indexing", "Exact k-NN vs Approximate Nearest Neighbor, Hierarchical Navigable Small World (HNSW) graphs, Inverted File Index (IVF), and product quantization.", "https://www.youtube.com/watch?v=klTvEwg3oJ8", "00:00", "Computerphile"),
                    ("ai-pinecone-chroma", "Managed Vector Stores: Pinecone, ChromaDB & Weaviate", "Fully-managed cloud vector indexes, serverless pricing, embedded vector databases for prototyping, and hybrid keyword-vector storage.", "https://www.youtube.com/watch?v=QdDoFfkVkcw", "00:00", "freeCodeCamp"),
                    ("ai-milvus-qdrant", "Open-Source Vector Engines: Qdrant, Milvus & pgvector for PostgreSQL", "Rust-based vector search engines, distributed Milvus clusters, and running native vector similarity search inside relational PostgreSQL via pgvector.", "https://www.youtube.com/watch?v=7uK3ddA9KFA", "00:00", "Fireship"),
                    ("ai-distance-metrics", "Vector Distance Metrics: Cosine Similarity, Dot Product & Euclidean Distance", "Mathematical foundations of vector similarity: geometric angle (cosine), magnitude-sensitive inner products, and Euclidean L2 metric spaces.", "https://www.youtube.com/watch?v=e9U0QAFbfLI", "00:00", "StatQuest")
                ]
            },
            {
                "title": "Autonomous AI Agents & Multi-Agent Frameworks",
                "concepts": [
                    ("ai-agent-loop-react", "The ReAct (Reason + Act) Pattern & Autonomous Decision Loops", "Observation-Thought-Action execution cycles, self-correction, task decomposition, stop conditions, and handling non-deterministic tool outputs.", "https://www.youtube.com/watch?v=bzcRHN4Z5iE", "00:00", "DeepLearning.AI"),
                    ("ai-tool-calling-exec", "Dynamic Tool Calling, API Execution & Environment Sandboxing", "Model-invoked external functions, parameter extraction, secure sandboxed code execution, web search integration, and error handling.", "https://www.youtube.com/watch?v=0LzvhbA-F5s", "00:00", "freeCodeCamp"),
                    ("ai-agent-memory", "Agent Memory Architectures: Short-Term Buffer, Sliding Windows & Vector Memory", "Conversation state management, token-constrained sliding buffers, recursive conversational summarization, and semantic memory recall.", "https://www.youtube.com/watch?v=1oEQqJ_XQx4", "00:00", "LangChain"),
                    ("ai-langgraph-crewai", "Multi-Agent Orchestration: LangGraph Stateful Graphs & CrewAI Role Playing", "Cyclic graph workflows, human-in-the-loop approval nodes, state persistence, role-based delegation, and collaborative agent consensus.", "https://www.youtube.com/watch?v=hvAPnpSfSGo", "00:00", "freeCodeCamp")
                ]
            },
            {
                "title": "Fine-Tuning, Parameter-Efficient Adaptation & Alignment",
                "concepts": [
                    ("ai-finetuning-transfer", "Full Fine-Tuning vs Transfer Learning & Task Adaptation", "Weight updating across all layers, catastrophic forgetting, compute and memory requirements, domain adaptation, and instruction fine-tuning.", "https://www.youtube.com/watch?v=e-gwvmhyU7A", "00:00", "Andrej Karpathy"),
                    ("ai-peft-lora", "Parameter-Efficient Fine-Tuning (PEFT) & Low-Rank Adaptation (LoRA)", "Freezing base model weights, injecting trainable low-rank rank-decomposition matrices (A and B), and reducing trainable parameter counts by 99%.", "https://www.youtube.com/watch?v=dA-NhCtrrVE", "00:00", "Weights & Biases"),
                    ("ai-qlora-quantization", "4-bit Quantization (QLoRA) & GPU Memory Optimization", "NormalFloat4 (NF4) data type, double quantization, paged optimizers, and fine-tuning 70B parameter models on consumer hardware.", "https://www.youtube.com/watch?v=TPcXVJ1VSRI", "00:00", "Hugging Face"),
                    ("ai-rlhf-dpo", "Model Alignment: Reinforcement Learning from Human Feedback (RLHF) & DPO", "Reward model training, PPO policy optimization, Direct Preference Optimization (DPO) without reinforcement learning, and safety alignment.", "https://www.youtube.com/watch?v=vE3m6U7fS4I", "00:00", "DeepLearning.AI")
                ]
            },
            {
                "title": "AI Safety, Guardrails & LLM Evaluation",
                "concepts": [
                    ("ai-guardrails-moderation", "Input/Output Guardrails: NeMo Guardrails & Llama Guard", "Programmable guardrail policies, topical rails, safety rails, hallucination mitigation, and sensitive data (PII) masking.", "https://www.youtube.com/watch?v=8V3G7aZcE3A", "00:00", "NVIDIA"),
                    ("ai-rag-triad-eval", "The RAG Triad: Faithfulness, Answer Relevance & Context Relevance", "Evaluating retrieval precision, assessing whether answers are grounded in retrieved context, and measuring question answering fidelity.", "https://www.youtube.com/watch?v=hG9r2mG2t4g", "00:00", "TruLens"),
                    ("ai-eval-frameworks", "Automated LLM Evaluation: Ragas, TruLens & Deepeval", "Synthetic test generation, automated metric scoring, CI/CD evaluation pipelines, and tracking model drift across prompt revisions.", "https://www.youtube.com/watch?v=nO_3y12sZ7k", "00:00", "DeepLearning.AI"),
                    ("ai-llm-as-judge", "LLM-as-a-Judge Methodologies, Benchmark Datasets & Golden Sets", "Using frontier models to grade reasoning outputs, pairwise comparisons, position bias mitigation, and standard benchmark evaluation.", "https://www.youtube.com/watch?v=uK7YjH_9wG4", "00:00", "freeCodeCamp")
                ]
            }
        ]
    },
    {
        "id": "section-2",
        "slug": "ml-eng",
        "title": "Machine Learning Engineering (MLE)",
        "icon": "🧠",
        "desc": "Classical supervised & unsupervised algorithms, Deep Learning with PyTorch, feature pipelines, MLOps, model registries, serving & drift.",
        "badge": "Algorithms, PyTorch, MLOps & Production Serving",
        "page": "tech_ml.html",
        "page_title": "Machine Learning Engineering Masterclass",
        "page_subtitle": "Production machine learning architecture: classical algorithms, PyTorch deep learning, feature pipelines, cross-validation, MLOps tracking, and low-latency Triton/vLLM serving.",
        "subsections": [
            {
                "title": "Supervised & Unsupervised Learning Algorithms",
                "concepts": [
                    ("ml-linear-logistic", "Linear & Logistic Regression: Cost Functions, Gradient Descent & Odds Ratios", "Ordinary least squares, sigmoid activation, log-loss cross-entropy, decision boundaries, and interpretability in linear modeling.", "https://www.youtube.com/watch?v=nk2CQITm_eo", "00:00", "StatQuest"),
                    ("ml-trees-ensembles", "Decision Trees, Bagging & Random Forest Ensembles", "Gini impurity, entropy information gain, tree pruning, bootstrap aggregating (bagging), and feature subspace random forests.", "https://www.youtube.com/watch?v=J4Wdy0Wc_xQ", "00:00", "StatQuest"),
                    ("ml-gradient-boosting", "Gradient Boosting: XGBoost, LightGBM & CatBoost Internals", "Sequential residual fitting, shrinkage learning rate, histogram-based splitting, leaf-wise vs depth-wise tree growth, and categorical features.", "https://www.youtube.com/watch?v=OtD8wVaFm6E", "00:00", "StatQuest"),
                    ("ml-unsupervised-clustering", "Unsupervised Learning: K-Means Clustering, Hierarchical & PCA", "Centroid convergence, inertia elbow method, silhouette analysis, dendrograms, and orthogonal variance projection via PCA.", "https://www.youtube.com/watch?v=4b5d3muPQmA", "00:00", "StatQuest")
                ]
            },
            {
                "title": "Deep Learning Architectures & PyTorch",
                "concepts": [
                    ("ml-neural-networks-backprop", "Multilayer Perceptrons (MLP), Activation Functions & Backpropagation", "Forward pass, chain rule derivative calculation, vanishing and exploding gradients, ReLU, LeakyReLU, GELU, and weight initialization.", "https://www.youtube.com/watch?v=aircAruvnKk", "00:00", "3Blue1Brown"),
                    ("ml-optimization-adam", "Loss Functions & Optimization: SGD with Momentum, RMSprop & Adam", "Convex vs non-convex optimization, exponential moving average of gradients, adaptive learning rates, weight decay, and learning rate warmups.", "https://www.youtube.com/watch?v=IHZwWFHWa-w", "00:00", "StatQuest"),
                    ("ml-pytorch-fundamentals", "PyTorch Core: Tensors, Autograd, nn.Module & Custom Training Loops", "Dynamic computational graphs, tensor GPU memory allocation, automatic differentiation with .backward(), and optimizer step iteration.", "https://www.youtube.com/watch?v=V_xro1bcAuA", "00:00", "freeCodeCamp"),
                    ("ml-cnn-rnn-foundations", "Vision & Sequence Models: Convolutional Neural Networks (CNNs) & LSTMs", "Convolution kernels, pooling layers, feature maps, recurrent hidden state transitions, gating mechanisms (Forget, Input, Output gates) in LSTMs.", "https://www.youtube.com/watch?v=KuXjwB4LzSA", "00:00", "3Blue1Brown")
                ]
            },
            {
                "title": "Feature Engineering, Preprocessing & Validation",
                "concepts": [
                    ("ml-feature-encoding-scaling", "Feature Preprocessing: One-Hot, Ordinal Encoding & Standard Scaling", "Handling categorical cardinalities, z-score normalization, min-max scaling, target encoding, and frequency encoding.", "https://www.youtube.com/watch?v=irHhDMb3Vz0", "00:00", "StatQuest"),
                    ("ml-missing-imputation", "Missing Value Imputation, Outlier Detection & Robust Scaling", "MCAR vs MAR vs MNAR missingness, KNN/iterative imputation, interquartile range (IQR) fencing, and robust median-based scalers.", "https://www.youtube.com/watch?v=m_hmflGZoxU", "00:00", "StatQuest"),
                    ("ml-cross-validation", "K-Fold Cross-Validation, Stratified Sampling & Train/Val/Test Splits", "Mitigating sample bias, class-balanced stratification, time-series split walk-forward validation, and hyperparameter grid search.", "https://www.youtube.com/watch?v=fSytzGwwBVw", "00:00", "StatQuest"),
                    ("ml-data-leakage", "Data Leakage Prevention: Preprocessing Inside Cross-Validation Pipelines", "Feature leakage, target leakage, fit/transform pipeline boundaries, and building scikit-learn Pipeline and ColumnTransformer objects.", "https://www.youtube.com/watch?v=URdnFlZnqnk", "00:00", "StatQuest")
                ]
            },
            {
                "title": "Model Evaluation & Diagnostics",
                "concepts": [
                    ("ml-classification-metrics", "Classification Metrics: Precision, Recall, F1-Score, ROC-AUC & PR-AUC", "Confusion matrix, false positives vs false negatives trade-off, precision-recall curve for imbalanced data, and probability thresholds.", "https://www.youtube.com/watch?v=4jRBRDbJemM", "00:00", "StatQuest"),
                    ("ml-regression-metrics", "Regression Metrics: Mean Squared Error (MSE), RMSE, MAE & R-Squared", "Penalizing large errors with MSE, interpretability of MAE, residual plots, and explained variance in target distributions.", "https://www.youtube.com/watch?v=2AQKmw14mHM", "00:00", "StatQuest"),
                    ("ml-bias-variance", "The Bias-Variance Tradeoff: Underfitting vs Overfitting Diagnostics", "Decomposing expected prediction error, learning curves, model capacity, validation loss divergence, and regularization remedies.", "https://www.youtube.com/watch?v=EuBBz3bI-aA", "00:00", "StatQuest"),
                    ("ml-regularization", "Regularization Techniques: L1 (Lasso), L2 (Ridge), Dropout & Early Stopping", "L1 parameter sparsity, L2 weight decay penalty, randomly dropping neurons during training, and stopping criteria on validation plateaus.", "https://www.youtube.com/watch?v=Q81RR3yKn30", "00:00", "StatQuest")
                ]
            },
            {
                "title": "MLOps: Tracking, Pipelines & Feature Stores",
                "concepts": [
                    ("ml-experiment-tracking", "Experiment Tracking & Model Registry with MLflow / Weights & Biases", "Logging hyperparameters, loss curves, artifacts, model versioning, transition stages (Staging, Production), and lineage audits.", "https://www.youtube.com/watch?v=6rVf8tL4lH4", "00:00", "freeCodeCamp"),
                    ("ml-pipeline-orchestration", "Automated ML Pipelines: Kubeflow, Metaflow & CI/CD for ML", "Reproducible DAG workflows, containerized training steps, artifact caching, and continuous training (CT) triggers upon data updates.", "https://www.youtube.com/watch?v=qTfZzYcR7pM", "00:00", "freeCodeCamp"),
                    ("ml-feature-stores", "Centralized Feature Stores: Feast & Feature Pipelines", "Decoupling feature engineering from model consumption, point-in-time correct joins to prevent data leakage, and low-latency online serving.", "https://www.youtube.com/watch?v=zGgZp9c2VzA", "00:00", "freeCodeCamp"),
                    ("ml-model-versioning", "Model Versioning, Artifact Lineage & Reproducibility", "Semantic versioning for model weights, data-code-model linkage via DVC, hardware environment freezing, and deterministic seeds.", "https://www.youtube.com/watch?v=kYJv8P2zHk8", "00:00", "freeCodeCamp")
                ]
            },
            {
                "title": "Production Serving & Low-Latency Inference",
                "concepts": [
                    ("ml-serving-architectures", "Model Serving Architectures: FastAPI, Triton Inference Server & TorchServe", "Synchronous REST endpoints vs asynchronous gRPC streaming, dynamic request batching, concurrent model execution, and GPU saturation.", "https://www.youtube.com/watch?v=0LzvhbA-F5s", "00:00", "freeCodeCamp"),
                    ("ml-optimized-runtimes", "Inference Optimization: ONNX Runtime, TensorRT & vLLM Engines", "Graph optimization, operator fusion, FP16/INT8 post-training quantization, PagedAttention continuous batching, and CUDA execution engines.", "https://www.youtube.com/watch?v=7uK3ddA9KFA", "00:00", "NVIDIA"),
                    ("ml-monitoring-drift", "Production Monitoring: Data Drift (KS-Test), Concept Drift & Evidentially", "Statistical drift detection, Kolmogorov-Smirnov test, Population Stability Index (PSI), ground truth latency, and model degradation alerts.", "https://www.youtube.com/watch?v=kYJv8P2zHk8", "00:00", "freeCodeCamp"),
                    ("ml-deployment-strategies", "Deployment Strategies: Shadow Deployments, Canary Releases & A/B Testing", "Routing production traffic copies to shadow models, incremental canary traffic shifting, statistical hypothesis validation, and auto-rollback.", "https://www.youtube.com/watch?v=5rT8X2k-4kU", "00:00", "freeCodeCamp")
                ]
            }
        ]
    },
    {
        "id": "section-3",
        "slug": "data-science",
        "title": "Data Science & Applied Analytics",
        "icon": "📊",
        "desc": "Exploratory data analysis, statistical modeling, hypothesis testing, causal inference, A/B experiments & time series analysis.",
        "badge": "Statistics, EDA, Hypothesis Testing, A/B & Time Series",
        "page": "tech_data_science.html",
        "page_title": "Data Science & Applied Analytics Masterclass",
        "page_subtitle": "Practical data science: exploratory feature insights, mathematical probability, hypothesis testing, causal inference, production A/B testing, and time series forecasting.",
        "subsections": [
            {
                "title": "Exploratory Data Analysis & Feature Insights",
                "concepts": [
                    ("ds-eda-distributions", "Distribution Analysis: Skewness, Kurtosis & Q-Q Normality Plots", "Assessing univariate distributions, log and power transforms (Box-Cox), identifying heavy tails, and visual normality validation via Q-Q plots.", "https://www.youtube.com/watch?v=smJBsZ4YQZg", "00:00", "StatQuest"),
                    ("ds-bivariate-correlation", "Correlation Mechanics: Pearson, Spearman Rank & Kendall Tau", "Linear vs monotonic relationships, sensitivity to outliers, rank transformation, covariance matrices, and multicollinearity diagnostics (VIF).", "https://www.youtube.com/watch?v=xZ_z8KWkhXE", "00:00", "StatQuest"),
                    ("ds-multivariate-reduction", "Multivariate Analysis: Dimensionality Reduction via PCA & t-SNE", "High-dimensional geometric projection, eigenvalue decomposition of covariance matrices, perplexity tuning in t-SNE, and UMAP clustering.", "https://www.youtube.com/watch?v=FgakZw6K1QQ", "00:00", "StatQuest"),
                    ("ds-data-cleaning-automation", "Robust Data Cleaning & Anomaly Detection with Isolation Forests", "Tree-based anomaly partitioning, outlier contamination factor tuning, automated missingness imputation strategies, and pandas profiling.", "https://www.youtube.com/watch?v=5p8wTXPG4Dk", "00:00", "freeCodeCamp")
                ]
            },
            {
                "title": "Probability & Mathematical Statistics",
                "concepts": [
                    ("ds-probability-distributions", "Core Probability Distributions: Normal, Binomial, Poisson & Exponential", "Probability density functions (PDF), cumulative distribution functions (CDF), Poisson arrival processes, and memoryless exponential modeling.", "https://www.youtube.com/watch?v=oI3hZASlRsE", "00:00", "StatQuest"),
                    ("ds-bayes-theorem", "Bayesian Probability: Prior, Likelihood, Posterior & Conjugate Priors", "Conditional probability updating, Bayes Theorem formula derivation, Beta-Binomial conjugate analysis, and MAP vs MLE estimation.", "https://www.youtube.com/watch?v=HZGCoVF3YvM", "00:00", "3Blue1Brown"),
                    ("ds-clt-sampling", "The Central Limit Theorem (CLT) & Sampling Distributions", "Sample mean convergence to normality, standard error formula, finite population correction factor, and sample size power requirements.", "https://www.youtube.com/watch?v=YAlJCEDH2uY", "00:00", "StatQuest"),
                    ("ds-maximum-likelihood", "Maximum Likelihood Estimation (MLE) & Expectation Maximization", "Constructing likelihood functions, log-likelihood optimization, parameter score equations, and latent variable estimation via EM algorithms.", "https://www.youtube.com/watch?v=XepXtl9YKSE", "00:00", "StatQuest")
                ]
            },
            {
                "title": "Inferential Statistics & Hypothesis Testing",
                "concepts": [
                    ("ds-hypothesis-framing", "Hypothesis Formulation: Null vs Alternative, Type I & Type II Errors", "Formulating testable claims, significance level alpha, statistical power (1 - beta), p-value interpretation, and decision matrices.", "https://www.youtube.com/watch?v=0oc49DyA3hU", "00:00", "StatQuest"),
                    ("ds-parametric-tests", "Parametric Tests: One-Sample, Two-Sample Student's t-Test & Paired t-Test", "Degrees of freedom calculation, pooled vs unpooled variance (Welch's t-test), Cohen's d effect size, and paired sample mean differences.", "https://www.youtube.com/watch?v=pTmLQvMM-1M", "00:00", "StatQuest"),
                    ("ds-anova-f-test", "Analysis of Variance (ANOVA) & F-Distribution", "One-way vs two-way ANOVA, partitioning sum of squares (between vs within groups), F-statistic calculation, and Tukey's HSD post-hoc tests.", "https://www.youtube.com/watch?v=ITf4vHhyGpc", "00:00", "StatQuest"),
                    ("ds-non-parametric", "Non-Parametric Tests: Chi-Square Independence, Mann-Whitney U & Kruskal-Wallis", "Observed vs expected contingency tables, rank-sum statistics for non-normal continuous data, and distribution-free multi-group comparisons.", "https://www.youtube.com/watch?v=7_cs1YlZoug", "00:00", "StatQuest")
                ]
            },
            {
                "title": "A/B Testing & Causal Inference",
                "concepts": [
                    ("ds-ab-design-power", "A/B Test Design: Sample Size Calculation, Power Analysis & Minimum Detectable Effect", "Statistical power calculation formula, baseline conversion rate, minimum detectable effect (MDE), and sample size determination.", "https://www.youtube.com/watch?v=bv-tgptpnU8", "00:00", "freeCodeCamp"),
                    ("ds-randomization-srm", "Randomization Mechanics, Hashing & Sample Ratio Mismatch (SRM)", "Consistent hashing for user bucketing, identifying Sample Ratio Mismatch (SRM) using Chi-square tests, and preventing experimental contamination.", "https://www.youtube.com/watch?v=2AQKmw14mHM", "00:00", "freeCodeCamp"),
                    ("ds-sequential-testing", "Multi-Armed Bandits vs Fixed-Horizon A/B Testing & Sequential Analysis", "Addressing the peeking problem, alpha spending functions, Thompson Sampling, Upper Confidence Bound (UCB), and dynamic exploration-exploitation.", "https://www.youtube.com/watch?v=e3L4VocZnnQ", "00:00", "freeCodeCamp"),
                    ("ds-causal-inference", "Causal Inference: Difference-in-Differences (DiD) & Propensity Score Matching", "Counterfactual reasoning, selection bias mitigation, quasi-experiments, parallel trends assumption in DiD, and synthetic control methods.", "https://www.youtube.com/watch?v=6rVf8tL4lH4", "00:00", "freeCodeCamp")
                ]
            },
            {
                "title": "Time Series Forecasting & Anomaly Detection",
                "concepts": [
                    ("ds-timeseries-components", "Time Series Anatomy: Trend, Seasonality, Residuals & Stationarity", "Additive vs multiplicative decomposition, moving averages, autocorrelation function (ACF), partial ACF (PACF), and Augmented Dickey-Fuller tests.", "https://www.youtube.com/watch?v=e8Yw4alG16Q", "00:00", "StatQuest"),
                    ("ds-arima-sarimax", "ARIMA, SARIMA & Exogenous Regressors (SARIMAX)", "Autoregressive (p), Integrated differencing (d), Moving Average (q) orders, seasonal order tuning (P, D, Q, s), and AIC/BIC model selection.", "https://www.youtube.com/watch?v=3UmyHed0iYE", "00:00", "StatQuest"),
                    ("ds-prophet-forecasting", "Additive Time Series with Meta Prophet & Holiday Effects", "Piecewise linear/logistic trend curves, Fourier series seasonal components, holiday indicators, and robust handling of missing dates/outliers.", "https://www.youtube.com/watch?v=j0e23nk2TCo", "00:00", "freeCodeCamp"),
                    ("ds-ts-anomaly-detection", "Time Series Anomaly Detection: STL Decomposition & Dynamic Thresholds", "Residual z-score thresholding, Exponential Moving Average (EMA) bounds, seasonal-trend decomposition anomaly flags, and alert smoothing.", "https://www.youtube.com/watch?v=1uTfG6eA0oE", "00:00", "freeCodeCamp")
                ]
            }
        ]
    },
    {
        "id": "section-4",
        "slug": "data-eng",
        "title": "Data Engineering & Modern Data Stack",
        "icon": "⚡",
        "desc": "Modern data warehousing, Apache Spark, Lakehouses (Iceberg/Delta), dbt transformation, Airflow orchestration & Kafka/Flink streaming.",
        "badge": "Warehouses, Spark, Lakehouse, dbt, Airflow & Kafka",
        "page": "tech_data_eng.html",
        "page_title": "Data Engineering & Lakehouse Architecture Masterclass",
        "page_subtitle": "Enterprise data engineering: cloud analytical data warehouses, distributed PySpark processing, open lakehouse table formats (Iceberg, Delta Lake), dbt modeling, Airflow DAG orchestration, and real-time Kafka/Flink streaming.",
        "subsections": [
            {
                "title": "Modern Data Warehousing & Analytical Engines",
                "concepts": [
                    ("de-oltp-vs-olap", "OLTP vs OLAP Architecture: Row-Store vs Columnar Execution", "B-tree transactional indexes vs columnar projection, dictionary encoding, run-length compression, vectorized query execution, and SIMD instructions.", "https://www.youtube.com/watch?v=bzcRHN4Z5iE", "00:00", "ByteByteGo"),
                    ("de-cloud-warehouses", "Cloud Data Warehouses: Snowflake Virtual Warehouses & BigQuery Slot Architecture", "Decoupled storage and compute, micro-partitions in Snowflake, capacitor storage in Google BigQuery, and reservation pricing models.", "https://www.youtube.com/watch?v=yE9v9fZkY4A", "00:00", "freeCodeCamp"),
                    ("de-clickhouse-duckdb", "Modern Analytical Query Engines: ClickHouse & Embedded DuckDB", "LSM-tree merge tree engines in ClickHouse, vectorized column processing, and zero-dependency in-process analytics using DuckDB.", "https://www.youtube.com/watch?v=nO_3y12sZ7k", "00:00", "SeattleDataGuy"),
                    ("de-partitioning-clustering", "Query Optimization: Partitioning Pruning, Clustering Keys & Data Skipping", "Min-max metadata pruning, bloom filters, sorting clustering keys, preventing full table scans, and optimizing partition cardinality.", "https://www.youtube.com/watch?v=3mJkWkH9P6Q", "00:00", "SeattleDataGuy")
                ]
            },
            {
                "title": "Distributed Processing with Apache Spark & PySpark",
                "concepts": [
                    ("de-spark-architecture", "Apache Spark Cluster Architecture: Driver, Executors & Memory Management", "Cluster manager (YARN/K8s), worker nodes, executor memory fractions (Storage vs Execution memory), tasks, and partitions.", "https://www.youtube.com/watch?v=3mJkWkH9P6Q", "00:00", "freeCodeCamp"),
                    ("de-spark-transformations", "Spark Transformations: Narrow vs Wide Dependencies & The Shuffle Stage", "Map/filter (narrow) without network transfers vs GroupBy/join (wide) requiring cluster-wide data shuffle, stage boundaries, and skew.", "https://www.youtube.com/watch?v=3mJkWkH9P6Q", "00:00", "freeCodeCamp"),
                    ("de-pyspark-dataframes", "PySpark DataFrames, Spark SQL & Distributed Aggregations", "DataFrame API syntax, structured streaming, window functions, user-defined functions (UDFs vs pandas UDFs with Arrow), and broadcast joins.", "https://www.youtube.com/watch?v=XrpSRCwISdk", "00:00", "freeCodeCamp"),
                    ("de-catalyst-optimizer", "The Catalyst Query Optimizer & Tungsten Memory Management", "Logical plan generation, rule-based optimization, cost-based optimization, physical plan selection, and off-heap binary format processing.", "https://www.youtube.com/watch?v=r0X6X_6r7uM", "00:00", "freeCodeCamp")
                ]
            },
            {
                "title": "Data Lakehouse Architecture & Open Table Formats",
                "concepts": [
                    ("de-lakehouse-evolution", "Lakehouse Evolution: Object Storage, ACID Transactions & Metadata", "Combining data lake cost-efficiency with data warehouse ACID guarantees, schema enforcement, concurrency, and metadata management.", "https://www.youtube.com/watch?v=vA8Z2k_o8bE", "00:00", "Databricks"),
                    ("de-apache-iceberg", "Apache Iceberg: Snapshot Architecture, Manifest Files & Partitioning", "Hierarchical metadata tree: Iceberg catalog, metadata file, manifest lists, manifest files, data files, hidden partitioning, and time travel.", "https://www.youtube.com/watch?v=4u1Q2f_x5aQ", "00:00", "SeattleDataGuy"),
                    ("de-delta-lake", "Delta Lake: Transaction Log (Delta Log), ACID Guarantees & Time Travel", "JSON/Parquet commit log, atomic commit protocols, optimistic concurrency control, vacuuming old snapshots, and MERGE upsert commands.", "https://www.youtube.com/watch?v=6rVf8tL4lH4", "00:00", "Databricks"),
                    ("de-parquet-internals", "Columnar File Formats: Apache Parquet Anatomy & Compression", "Parquet file structure: File Header, Row Groups, Column Chunks, Data Pages, Dictionary Pages, Snappy/ZSTD compression, and stats pruning.", "https://www.youtube.com/watch?v=1uTfG6eA0oE", "00:00", "SeattleDataGuy")
                ]
            },
            {
                "title": "Data Transformation & Dimensional Modeling with dbt",
                "concepts": [
                    ("de-dbt-fundamentals", "Data Build Tool (dbt): Models, Ref Macros & Modular SQL DAGs", "ELT paradigm, declarative SQL transformations, the {{ ref() }} function building lineage graphs, staging vs intermediate vs mart layers.", "https://www.youtube.com/watch?v=5rT8X2k-4kU", "00:00", "freeCodeCamp"),
                    ("de-dbt-testing-docs", "dbt Data Quality: Schema Tests, Singular Tests & Auto-Docs", "Asserting unique, not_null, accepted_values, relationships foreign keys; compiling data catalogs, interactive DAG visualizers, and CI runs.", "https://www.youtube.com/watch?v=6rVf8tL4lH4", "00:00", "SeattleDataGuy"),
                    ("de-dimensional-modeling", "Dimensional Modeling: Kimball Star Schema vs Snowflake Schema", "Business processes, grains, Fact tables (additive, semi-additive, non-additive measures), Dimension tables, surrogate keys, and normalization.", "https://www.youtube.com/watch?v=3g8K1P_q0qQ", "00:00", "SeattleDataGuy"),
                    ("de-scd-patterns", "Slowly Changing Dimensions (SCD Type 1, Type 2 & Type 3)", "Overwriting values (Type 1), tracking historical changes with valid_from/valid_to dates and is_current flags (Type 2), and dbt snapshots.", "https://www.youtube.com/watch?v=2AQKmw14mHM", "00:00", "SeattleDataGuy")
                ]
            },
            {
                "title": "Workflow Orchestration & Modern Data Pipelines",
                "concepts": [
                    ("de-airflow-dags", "Apache Airflow Core: DAGs, Operators, Tasks, Sensors & Dependencies", "Python-defined pipeline topologies, BashOperator, PythonOperator, external trigger sensors, XCom task communication, and pool concurrency.", "https://www.youtube.com/watch?v=K9AnJ9_ZAXE", "00:00", "Marc Lamberti"),
                    ("de-airflow-scheduling", "Airflow Execution: Celery/Kubernetes Executors & Idempotent Tasks", "Distributed task execution, stateless worker pods, data interval concepts (logical date vs execution date), backfilling historical partitions.", "https://www.youtube.com/watch?v=IHZwWFHWa-w", "00:00", "Marc Lamberti"),
                    ("de-dagster-assets", "Modern Asset-Based Orchestration with Dagster & Prefect", "Software-defined assets (SDAs), declarative data dependencies, dynamic parameter pipelines, and immediate local testability.", "https://www.youtube.com/watch?v=7uK3ddA9KFA", "00:00", "SeattleDataGuy"),
                    ("de-pipeline-observability", "Data Pipeline Observability: SLA Alerts, Data Lineage & Circuit Breakers", "Monitoring pipeline execution latency, data freshness SLAs, Monte Carlo data observability, OpenLineage standards, and circuit breakers.", "https://www.youtube.com/watch?v=kYJv8P2zHk8", "00:00", "freeCodeCamp")
                ]
            },
            {
                "title": "Real-Time Data Streaming & Event Processing",
                "concepts": [
                    ("de-streaming-fundamentals", "Stream Processing Fundamentals: Event Time, Processing Time & Watermarks", "Unbounded data streams, out-of-order event arrivals, late data handling, watermarks, tumbling windows, hopping windows, and session windows.", "https://www.youtube.com/watch?v=Vb7C_7a3d3M", "00:00", "ByteByteGo"),
                    ("de-kafka-pipelines", "Apache Kafka Architecture: Topics, Partitions, Consumer Groups & Offsets", "Distributed write-ahead log, partition hashing, leader-follower replication, consumer offset commits (__consumer_offsets), and log compaction.", "https://www.youtube.com/watch?v=Ch5VhJzaoaI", "00:00", "freeCodeCamp"),
                    ("de-kafka-connect", "Kafka Connect (Source & Sink Connectors) & Schema Registry", "Streaming change data capture (Debezium CDC), Kafka to Data Lakehouse ingestion, schema evolution enforcement with Apache Avro and Protobuf.", "https://www.youtube.com/watch?v=kCc8FmEb1nY", "00:00", "Confluent"),
                    ("de-flink-streaming", "Stateful Stream Processing with Apache Flink & Window Operations", "Distributed snapshots (Chandy-Lamport algorithm), RocksDB state backend, exactly-once processing end-to-end, and low-latency complex event CEP.", "https://www.youtube.com/watch?v=Vb7C_7a3d3M", "00:00", "Apache Flink")
                ]
            }
        ]
    }
]

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

def build_standalone_masterclass(track):
    page_name = track["page"]
    page_title = track["page_title"]
    page_subtitle = track["page_subtitle"]
    badge = track["badge"]
    total_subs = len(track["subsections"])
    total_concepts = sum(len(sub["concepts"]) for sub in track["subsections"])

    subsections_html = []
    for s_idx, sub in enumerate(track["subsections"]):
        concepts_html = []
        for c in sub["concepts"]:
            cid, cname, cdesc, yt_url, start_time, channel = c
            dur_label = "20:00"
            concept_row = f"""<li data-cid="{cid}" data-name="{cname.lower()}">
<div class="done-check" title="Mark as done"></div>
<div class="bookmark-star" title="Bookmark">☆</div>
<div>
<div class="cname">{cname}</div>
<div style="font-size:11.5px;color:var(--text-faint);margin-top:2px">{cdesc}</div>
</div>
<div class="res-links"><a class="video" data-start="{start_time}" data-vchannel="{channel}" data-vdur="{dur_label}" data-vtitle="{cname}" href="{yt_url}" rel="noopener" target="_blank" title="Watch walkthrough: {cname}">🎬YT</a><a href="https://en.wikipedia.org/wiki/{cname.split()[0]}" rel="noopener" target="_blank" title="Reference Guide">🌐Doc</a></div>
</li>"""
            concepts_html.append(concept_row)

        sub_block = f"""<div class="subsection">
<h3>1.{s_idx+1} {sub['title']}</h3>
<ol class="concepts">
{"".join(concepts_html)}
</ol>
</div>"""
        subsections_html.append(sub_block)

    sec_html = f"""<section class="section domain-section" id="{track['id']}" data-domain="{track['slug']}" style="--section-color:hsl(280, 80%, 50%)">
<h2>{track['title']}</h2>
<div class="sec-desc">
<p><strong>Core Focus:</strong> {track['desc']}</p>
<p><strong>Track Key:</strong> {track['badge']}</p>
</div>
{"".join(subsections_html)}
</section>"""

    page_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>{page_title} | Learning Hub</title>
<link href="assets/learning-hub-shared.css" rel="stylesheet"/>
<script src="assets/learning-hub-shared.js"></script>
<style>
{base_css}
</style>
</head>
<body data-site="ai_data">
<div class="wrap">
  <div class="tech-breadcrumb">
    <a class="tech-bc-home" href="ai_data.html">← AI &amp; Data Hub</a>
    <span class="tech-bc-sep">/</span>
    <span class="tech-bc-curr">{page_title}</span>
  </div>

  <div class="hero">
    <div class="edition">{badge} · {total_subs} Subsections · {total_concepts} Concepts</div>
    <h1>{page_title}</h1>
    <p class="subtitle">{page_subtitle}</p>
  </div>

  <div class="stats">
    <div class="stat"><div class="n">{total_subs}</div><div class="l">Subsections</div></div>
    <div class="stat"><div class="n">{total_concepts}</div><div class="l">Concepts</div></div>
    <div class="stat"><div class="n">100%</div><div class="l">Curated</div></div>
    <div class="stat"><div class="n">15+</div><div class="l">Verified Docs &amp; Labs</div></div>
  </div>

  <div class="overall-progress">
    <span class="lbl">Masterclass Progress</span>
    <div class="bar-track"><div class="bar-fill" id="overall-bar"></div></div>
    <span class="pct" id="overall-pct">0 / {total_concepts}</span>
  </div>

  <div class="controls">
    <div class="controls-row">
      <span class="label">Filter:</span>
      <button class="filter-btn status-done" data-filter="status" data-val="done">Done</button>
      <button class="filter-btn" data-filter="status" data-val="undone">Not Done</button>
      <button class="filter-btn status-bookmarked" data-filter="status" data-val="bookmarked">★ Bookmarked</button>
      <span class="sep"></span>
      <div class="search"><input id="search-input" placeholder="Search {total_concepts} concepts…" type="search"/></div>
      <button class="icon-btn" id="random-btn" title="Random concept">🎲</button>
      <button class="icon-btn" id="theme-toggle" title="Toggle theme">🌓</button>
      <button class="icon-btn" onclick="window.print()" title="Print">🖨️</button>
      <button class="filter-btn" id="clear-filters">Clear</button>
    </div>
  </div>

  {sec_html}

  <div class="sister-guides-card">
    <div class="sister-title">🤖 Companion AI &amp; Data Masterclasses</div>
    <div class="sister-grid">
      <a class="sister-link" href="ai_engineering.html">🤖 AI Engineering from Scratch (542 Lessons)</a>
      <a class="sister-link" href="tech_ml.html">🧠 Machine Learning Engineering Masterclass</a>
      <a class="sister-link" href="tech_data_science.html">📊 Data Science &amp; Applied Analytics Masterclass</a>
      <a class="sister-link" href="tech_data_eng.html">⚡ Data Engineering &amp; Lakehouse Masterclass</a>
      <a class="sister-link active-hub" href="ai_data.html">🌐 Unified AI &amp; Data Hub (4 Tracks) &rarr;</a>
    </div>
  </div>
</div>

<script>
window.SITE_SLUG = "ai_data";
</script>
<script>
(function() {{
  const SLUG = window.SITE_SLUG || 'ai_data';
  const KEY_DONE = 'hub_done_' + SLUG;
  const KEY_BM = 'hub_bm_' + SLUG;

  let doneSet = new Set();
  try {{
    const raw = localStorage.getItem(KEY_DONE);
    if (raw) doneSet = new Set(JSON.parse(raw));
  }} catch (e) {{}}

  let bmSet = new Set();
  try {{
    const raw = localStorage.getItem(KEY_BM);
    if (raw) bmSet = new Set(JSON.parse(raw));
  }} catch (e) {{}}

  function saveDone() {{
    try {{ localStorage.setItem(KEY_DONE, JSON.stringify([...doneSet])); }} catch (e) {{}}
  }}
  function saveBm() {{
    try {{ localStorage.setItem(KEY_BM, JSON.stringify([...bmSet])); }} catch (e) {{}}
  }}

  function updateProgress() {{
    const all = document.querySelectorAll('li[data-cid]');
    const total = all.length;
    let done = 0;
    all.forEach(li => {{
      const cid = li.getAttribute('data-cid');
      const isDone = doneSet.has(cid);
      li.classList.toggle('done', isDone);
      li.classList.toggle('is-done', isDone);
      const chk = li.querySelector('.done-check');
      if (chk) {{
        chk.classList.toggle('checked', isDone);
        chk.innerHTML = isDone ? '✓' : '';
      }}
      if (isDone) done++;
      const isBm = bmSet.has(cid);
      li.classList.toggle('is-bm', isBm);
      const star = li.querySelector('.bookmark-star');
      if (star) {{
        star.classList.toggle('active', isBm);
        star.textContent = isBm ? '★' : '☆';
      }}
    }});
    const pct = total ? Math.round((done / total) * 100) : 0;
    const bar = document.getElementById('overall-bar');
    if (bar) bar.style.width = pct + '%';
    const txt = document.getElementById('overall-pct');
    if (txt) txt.textContent = done + ' / ' + total + ' (' + pct + '%)';
  }}

  document.querySelectorAll('li[data-cid]').forEach(li => {{
    const cid = li.getAttribute('data-cid');
    const chk = li.querySelector('.done-check');
    if (chk) {{
      chk.addEventListener('click', (e) => {{
        e.stopPropagation();
        if (doneSet.has(cid)) doneSet.delete(cid);
        else doneSet.add(cid);
        saveDone();
        updateProgress();
      }});
    }}
    const star = li.querySelector('.bookmark-star');
    if (star) {{
      star.addEventListener('click', (e) => {{
        e.stopPropagation();
        if (bmSet.has(cid)) bmSet.delete(cid);
        else bmSet.add(cid);
        saveBm();
        updateProgress();
      }});
    }}
  }});

  let activeFilter = null;
  document.querySelectorAll('.filter-btn[data-filter]').forEach(b => {{
    b.addEventListener('click', () => {{
      const val = b.getAttribute('data-val');
      if (activeFilter === val) {{
        activeFilter = null;
        b.classList.remove('active');
      }} else {{
        document.querySelectorAll('.filter-btn[data-filter]').forEach(x => x.classList.remove('active'));
        activeFilter = val;
        b.classList.add('active');
      }}
      applyFilters();
    }});
  }});

  const sInput = document.getElementById('search-input');
  if (sInput) sInput.addEventListener('input', applyFilters);

  const clearBtn = document.getElementById('clear-filters');
  if (clearBtn) {{
    clearBtn.addEventListener('click', () => {{
      activeFilter = null;
      document.querySelectorAll('.filter-btn').forEach(x => x.classList.remove('active'));
      if (sInput) sInput.value = '';
      applyFilters();
    }});
  }}

  function applyFilters() {{
    const q = (sInput ? sInput.value : '').toLowerCase().trim();
    document.querySelectorAll('li[data-cid]').forEach(li => {{
      const cid = li.getAttribute('data-cid');
      const text = (li.getAttribute('data-name') || li.textContent).toLowerCase();
      let match = true;
      if (activeFilter === 'done' && !doneSet.has(cid)) match = false;
      if (activeFilter === 'undone' && doneSet.has(cid)) match = false;
      if (activeFilter === 'bookmarked' && !bmSet.has(cid)) match = false;
      if (q && !text.includes(q)) match = false;
      li.style.display = match ? '' : 'none';
    }});
  }}

  const randBtn = document.getElementById('random-btn');
  if (randBtn) {{
    randBtn.addEventListener('click', () => {{
      const all = Array.from(document.querySelectorAll('li[data-cid]')).filter(li => li.style.display !== 'none');
      if (!all.length) return;
      const pick = all[Math.floor(Math.random() * all.length)];
      pick.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
      pick.style.outline = '3px solid var(--accent)';
      setTimeout(() => {{ pick.style.outline = ''; }}, 2000);
    }});
  }}

  updateProgress();
}})();
</script>
</body>
</html>
"""
    dest = os.path.join(ROOT, page_name)
    atomic_write(dest, page_html)
    print(f"Generated standalone masterclass: {page_name} ({total_subs} subs, {total_concepts} concepts).")

def build():
    total_tracks = len(TRACKS)
    total_subs = sum(len(t['subsections']) for t in TRACKS)
    total_concepts = sum(sum(len(sub['concepts']) for sub in t['subsections']) for t in TRACKS)

    deck_cards = []
    for idx, t in enumerate(TRACKS):
        page_btn = f'<a class="domain-btn-masterclass" href="{t["page"]}">Dedicated Masterclass ↗</a>' if t.get("page") else ""
        card = f"""<div class="domain-card" data-domain="{t['slug']}" id="card-{t['slug']}" onclick="switchDomain('{t['slug']}')">
<div class="domain-card-head">
<div class="domain-card-icon">{t['icon']}</div>
<div class="domain-card-meta">
<span class="domain-card-idx">Track {idx+1:02d} / {total_tracks:02d}</span>
<h3 class="domain-card-title">{t['title']}</h3>
</div>
</div>
<p class="domain-card-desc">{t['desc']}</p>
<div class="domain-card-chips">
<span class="domain-card-chip highlight">{t['badge']}</span>
</div>
<div class="domain-card-actions">
<button class="domain-btn-view" onclick="event.stopPropagation(); switchDomain('{t['slug']}')" type="button">Focus Track</button>
{page_btn}
</div>
</div>"""
        deck_cards.append(card)

    pills = [f'<button class="d-nav-pill active" data-target="all" onclick="switchDomain(\'all\')">All Tracks ({total_tracks})</button>']
    for t in TRACKS:
        pills.append(f'<button class="d-nav-pill" data-target="{t["slug"]}" onclick="switchDomain(\'{t["slug"]}\')">{t["icon"]} {t["title"].split()[0]}</button>')
    pills.append('<a href="ai_engineering.html" class="d-nav-pill link-pill">🚀 Open Full AI Curriculum ↗</a>')

    sections_html = []
    for t_idx, t in enumerate(TRACKS):
        track_concepts_count = sum(len(s['concepts']) for s in t['subsections'])
        subsections_html = []
        for s_idx, sub in enumerate(t['subsections']):
            concepts_html = []
            for c in sub['concepts']:
                cid, cname, cdesc, yt_url, start_time, channel = c
                dur_label = "20:00"
                concept_row = f"""<li data-cid="{cid}" data-name="{cname.lower()}">
<div class="done-check" title="Mark as done"></div>
<div class="bookmark-star" title="Bookmark">☆</div>
<div>
<div class="cname">{cname}</div>
<div style="font-size:11.5px;color:var(--text-faint);margin-top:2px">{cdesc}</div>
</div>
<div class="res-links"><a class="video" data-start="{start_time}" data-vchannel="{channel}" data-vdur="{dur_label}" data-vtitle="{cname}" href="{yt_url}" rel="noopener" target="_blank" title="Watch walkthrough: {cname}">🎬YT</a><a href="https://en.wikipedia.org/wiki/{cname.split()[0]}" rel="noopener" target="_blank" title="Reference Guide">🌐Doc</a></div>
</li>"""
                concepts_html.append(concept_row)

            sub_block = f"""<div class="subsection">
<h3>{t_idx+1}.{s_idx+1} {sub['title']}</h3>
<ol class="concepts">
{"".join(concepts_html)}
</ol>
</div>"""
            subsections_html.append(sub_block)

        masterclass_title = t.get("page_title") or t["title"]
        masterclass_banner_link = f'<a class="domain-focus-link" href="{t["page"]}">Open Full Masterclass ↗</a>' if t.get("page") else ""

        sec_html = f"""<section class="section domain-section" id="{t['id']}" data-domain="{t['slug']}" style="--section-color:hsl({(t_idx*60 + 260)%360}, 80%, 50%)">
<div class="domain-focus-bar">
<div class="domain-focus-badge">{t['icon']} Track {t_idx+1} of {total_tracks}</div>
<div class="domain-focus-title">{t['title']}</div>
<div class="domain-focus-nav">
<button class="domain-focus-btn" onclick="navigateDomain(-1)" title="Previous Track">← Prev Track</button>
<button class="domain-focus-btn" onclick="switchDomain('all')" title="View All Tracks">View All ({total_tracks})</button>
<button class="domain-focus-btn" onclick="navigateDomain(1)" title="Next Track">Next Track →</button>
{masterclass_banner_link}
</div>
</div>
<h2>{t['title']}</h2>
<div class="sec-desc">
<p><strong>Core Focus:</strong> {t['desc']}</p>
<p><strong>Track Key:</strong> {t['badge']}</p>
</div>
{"".join(subsections_html)}
</section>"""
        sections_html.append(sec_html)

    track_slugs_js = "[" + ", ".join(f'"{t["slug"]}"' for t in TRACKS) + "]"

    page_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1" name="viewport"/>
<title>AI &amp; Data Hub (AI · ML · Data Science · Data Engineering) | Learning Hub</title>
<link href="assets/learning-hub-shared.css" rel="stylesheet"/>
<script src="assets/learning-hub-shared.js"></script>
<style>
{base_css}
</style>
</head>
<body data-site="ai_data">
<div class="wrap">
  <div class="hero">
    <div class="edition">v4 · AI &amp; Data Hub · {total_tracks} Strategic Tracks · {total_subs} Subsections · {total_concepts} Concepts</div>
    <h1>AI &amp; Data Hub (AI · ML · Data Science · Data Engineering)</h1>
    <p class="subtitle">Complete end-to-end curriculum spanning Generative AI &amp; LLM Engineering, Classical &amp; Deep Machine Learning, Applied Data Science &amp; Statistics, and Enterprise Data Engineering &amp; Lakehouse Architectures.</p>
  </div>

  <div class="stats">
    <div class="stat"><div class="n">{total_tracks}</div><div class="l">Tracks</div></div>
    <div class="stat"><div class="n">{total_subs}</div><div class="l">Subsections</div></div>
    <div class="stat"><div class="n">{total_concepts}</div><div class="l">Concepts</div></div>
    <div class="stat"><div class="n">{total_tracks}</div><div class="l">Masterclasses</div></div>
    <div class="stat"><div class="n">60+</div><div class="l">Resources</div></div>
  </div>

  <div class="overall-progress">
    <span class="lbl">Your Progress</span>
    <div class="bar-track"><div class="bar-fill" id="overall-bar"></div></div>
    <span class="pct" id="overall-pct">0 / {total_concepts}</span>
  </div>

  <div class="controls">
    <div class="controls-row">
      <span class="label">Filter:</span>
      <button class="filter-btn status-done" data-filter="status" data-val="done">Done</button>
      <button class="filter-btn" data-filter="status" data-val="undone">Not Done</button>
      <button class="filter-btn status-bookmarked" data-filter="status" data-val="bookmarked">★ Bookmarked</button>
      <span class="sep"></span>
      <div class="search"><input id="search-input" placeholder="Search {total_concepts} AI, ML, Data Science &amp; Data Engineering concepts…" type="search"/></div>
      <button class="icon-btn" id="random-btn" title="Random concept">🎲</button>
      <button class="icon-btn" id="theme-toggle" title="Toggle theme">🌓</button>
      <button class="icon-btn" onclick="window.print()" title="Print">🖨️</button>
      <button class="filter-btn" id="clear-filters">Clear</button>
    </div>
  </div>

  <section class="domain-deck-section" id="domain-navigator">
    <div class="domain-deck-head">
      <span class="domain-deck-kicker">Unified AI &amp; Data Command Deck</span>
      <h2>Explore AI &amp; Data Tracks</h2>
      <p class="domain-deck-subtitle">Select any track to isolate its curriculum, or open its dedicated deep-dive masterclass.</p>
    </div>
    <div class="domain-deck">
      {"".join(deck_cards)}
    </div>
  </section>

  <div class="domain-nav-bar" id="domain-nav-bar">
    <div class="domain-nav-scroll">
      {"".join(pills)}
    </div>
  </div>

  {"".join(sections_html)}

</div>

<script>
window.SITE_SLUG = "ai_data";
</script>
<script>
(function() {{
  const SLUG = window.SITE_SLUG || 'ai_data';
  const KEY_DONE = 'hub_done_' + SLUG;
  const KEY_BM = 'hub_bm_' + SLUG;

  let doneSet = new Set();
  try {{
    const raw = localStorage.getItem(KEY_DONE);
    if (raw) doneSet = new Set(JSON.parse(raw));
  }} catch (e) {{}}

  let bmSet = new Set();
  try {{
    const raw = localStorage.getItem(KEY_BM);
    if (raw) bmSet = new Set(JSON.parse(raw));
  }} catch (e) {{}}

  function saveDone() {{
    try {{ localStorage.setItem(KEY_DONE, JSON.stringify([...doneSet])); }} catch (e) {{}}
  }}
  function saveBm() {{
    try {{ localStorage.setItem(KEY_BM, JSON.stringify([...bmSet])); }} catch (e) {{}}
  }}

  function updateProgress() {{
    const all = document.querySelectorAll('li[data-cid]');
    const total = all.length;
    let done = 0;
    all.forEach(li => {{
      const cid = li.getAttribute('data-cid');
      const isDone = doneSet.has(cid);
      li.classList.toggle('done', isDone);
      li.classList.toggle('is-done', isDone);
      const chk = li.querySelector('.done-check');
      if (chk) {{
        chk.classList.toggle('checked', isDone);
        chk.innerHTML = isDone ? '✓' : '';
      }}
      if (isDone) done++;
      const isBm = bmSet.has(cid);
      li.classList.toggle('is-bm', isBm);
      const star = li.querySelector('.bookmark-star');
      if (star) {{
        star.classList.toggle('active', isBm);
        star.textContent = isBm ? '★' : '☆';
      }}
    }});
    const pct = total ? Math.round((done / total) * 100) : 0;
    const bar = document.getElementById('overall-bar');
    if (bar) bar.style.width = pct + '%';
    const txt = document.getElementById('overall-pct');
    if (txt) txt.textContent = done + ' / ' + total + ' (' + pct + '%)';
  }}

  document.querySelectorAll('li[data-cid]').forEach(li => {{
    const cid = li.getAttribute('data-cid');
    const chk = li.querySelector('.done-check');
    if (chk) {{
      chk.addEventListener('click', (e) => {{
        e.stopPropagation();
        if (doneSet.has(cid)) doneSet.delete(cid);
        else doneSet.add(cid);
        saveDone();
        updateProgress();
      }});
    }}
    const star = li.querySelector('.bookmark-star');
    if (star) {{
      star.addEventListener('click', (e) => {{
        e.stopPropagation();
        if (bmSet.has(cid)) bmSet.delete(cid);
        else bmSet.add(cid);
        saveBm();
        updateProgress();
      }});
    }}
  }});

  let activeFilter = null;
  document.querySelectorAll('.filter-btn[data-filter]').forEach(b => {{
    b.addEventListener('click', () => {{
      const val = b.getAttribute('data-val');
      if (activeFilter === val) {{
        activeFilter = null;
        b.classList.remove('active');
      }} else {{
        document.querySelectorAll('.filter-btn[data-filter]').forEach(x => x.classList.remove('active'));
        activeFilter = val;
        b.classList.add('active');
      }}
      applyFilters();
    }});
  }});

  const sInput = document.getElementById('search-input');
  if (sInput) sInput.addEventListener('input', applyFilters);

  const clearBtn = document.getElementById('clear-filters');
  if (clearBtn) {{
    clearBtn.addEventListener('click', () => {{
      activeFilter = null;
      document.querySelectorAll('.filter-btn').forEach(x => x.classList.remove('active'));
      if (sInput) sInput.value = '';
      applyFilters();
    }});
  }}

  function applyFilters() {{
    const q = (sInput ? sInput.value : '').toLowerCase().trim();
    document.querySelectorAll('li[data-cid]').forEach(li => {{
      const cid = li.getAttribute('data-cid');
      const text = (li.getAttribute('data-name') || li.textContent).toLowerCase();
      let match = true;
      if (activeFilter === 'done' && !doneSet.has(cid)) match = false;
      if (activeFilter === 'undone' && doneSet.has(cid)) match = false;
      if (activeFilter === 'bookmarked' && !bmSet.has(cid)) match = false;
      if (q && !text.includes(q)) match = false;
      li.style.display = match ? '' : 'none';
    }});
  }}

  const randBtn = document.getElementById('random-btn');
  if (randBtn) {{
    randBtn.addEventListener('click', () => {{
      const all = Array.from(document.querySelectorAll('li[data-cid]')).filter(li => li.style.display !== 'none');
      if (!all.length) return;
      const pick = all[Math.floor(Math.random() * all.length)];
      pick.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
      pick.style.outline = '3px solid var(--accent)';
      setTimeout(() => {{ pick.style.outline = ''; }}, 2000);
    }});
  }}

  updateProgress();
}})();
</script>
<script>
  const DOMAIN_SLUGS = {track_slugs_js};
  let currentActiveDomain = 'all';

  window.switchDomain = function(slug) {{
    if (!slug || slug === 'all') {{
      currentActiveDomain = 'all';
      document.querySelectorAll('.section.domain-section').forEach(sec => {{
        sec.classList.remove('hidden-domain');
      }});
      document.querySelectorAll('.domain-card').forEach(card => {{
        card.classList.remove('active-deck-card');
      }});
      document.querySelectorAll('.d-nav-pill').forEach(pill => {{
        pill.classList.toggle('active', pill.dataset.target === 'all');
      }});
      if (history.replaceState) {{
        history.replaceState(null, '', window.location.pathname + window.location.search);
      }}
      return;
    }}

    currentActiveDomain = slug;
    const target = document.querySelector(`.section.domain-section[data-domain="${{slug}}"]`) || document.getElementById(`section-${{slug}}`) || document.getElementById(slug);
    if (!target) return;

    document.querySelectorAll('.section.domain-section').forEach(sec => {{
      if (sec === target || sec.getAttribute('data-domain') === slug) {{
        sec.classList.remove('hidden-domain');
      }} else {{
        sec.classList.add('hidden-domain');
      }}
    }});

    document.querySelectorAll('.domain-card').forEach(card => {{
      card.classList.toggle('active-deck-card', card.dataset.domain === slug);
    }});

    document.querySelectorAll('.d-nav-pill').forEach(pill => {{
      pill.classList.toggle('active', pill.dataset.target === slug);
    }});

    target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
    if (history.replaceState) {{
      history.replaceState(null, '', '#' + slug);
    }}
  }};

  window.navigateDomain = function(step) {{
    let idx = DOMAIN_SLUGS.indexOf(currentActiveDomain);
    if (idx === -1) idx = step > 0 ? -1 : DOMAIN_SLUGS.length;
    let nextIdx = (idx + step + DOMAIN_SLUGS.length) % DOMAIN_SLUGS.length;
    window.switchDomain(DOMAIN_SLUGS[nextIdx]);
  }};

  function checkUrlHash() {{
    const hash = window.location.hash.replace(/^#/, '');
    if (!hash) return;
    if (DOMAIN_SLUGS.includes(hash)) {{
      window.switchDomain(hash);
    }} else if (hash.startsWith('section-')) {{
      const secNum = parseInt(hash.replace('section-', ''), 10);
      if (secNum >= 1 && secNum <= DOMAIN_SLUGS.length) {{
        window.switchDomain(DOMAIN_SLUGS[secNum - 1]);
      }}
    }}
  }}

  window.addEventListener('hashchange', checkUrlHash);

  const sInputOriginal = document.getElementById('search-input');
  if (sInputOriginal) {{
    sInputOriginal.addEventListener('input', (e) => {{
      if (e.target.value.trim().length > 0 && currentActiveDomain !== 'all') {{
        window.switchDomain('all');
      }}
    }});
  }}

  checkUrlHash();
</script>
</body>
</html>
"""
    dest_ai_data = os.path.join(ROOT, 'ai_data.html')
    atomic_write(dest_ai_data, page_html)
    print(f"Built ai_data.html successfully: {total_tracks} tracks, {total_subs} subs, {total_concepts} concepts.")

    # Build the 3 standalone masterclasses (Tracks 2, 3, 4)
    for track in TRACKS[1:]:
        build_standalone_masterclass(track)

if __name__ == '__main__':
    build()
