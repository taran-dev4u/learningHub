# Search Indexing, Ranking & Typeahead

Welcome to this masterclass module on **Search Systems & Discovery**. Whether you are building the next Google, an e-commerce search engine like Amazon, or simply adding a search bar to a SaaS product, understanding search architecture is absolutely non-negotiable for a senior engineer.

Search is rarely just about string matching; it is about *understanding intent* and doing so with blazing speed across millions or billions of documents. Think of a modern search system as an ultra-efficient, encyclopedic librarian. This librarian hasn't just read every book—they have meticulously mapped out exactly on which page, in which paragraph, every single word appears, and they can retrieve the exact book you want in milliseconds.

In this deep dive, we are going to explore the core mechanics of search engines, dissect the architecture of tools like Elasticsearch, break down the mathematical formulas used to rank results, and finally, design the "magic" autocomplete systems that predict what you're typing before you even finish your sentence. Let's dive in.

---

## Inverted Index Fundamentals

If you take away only one concept from this entire module, let it be the **Inverted Index**. It is the beating heart of almost every text search engine on the planet, including Lucene (which powers Elasticsearch and Solr).

### What is an Inverted Index?

To understand the inverted index, we first must understand the **Forward Index**.

A forward index maps a document to the words it contains.
- **Doc 1:** "The quick brown fox"
- **Doc 2:** "The fast brown fox"

If I ask a forward index, *"Which documents contain the word 'fox'?"*, the system has to scan Doc 1, check for 'fox', then scan Doc 2, check for 'fox'. This is an $O(N)$ operation where $N$ is the number of documents. If you have 10 billion documents, scanning them all sequentially for every search query is computationally impossible.

An **Inverted Index** flips this relationship. It maps **words (terms)** to the **documents** that contain them.

| Term | Document IDs (Postings List) |
|---|---|
| the | Doc 1, Doc 2 |
| quick | Doc 1 |
| brown | Doc 1, Doc 2 |
| fast | Doc 2 |
| fox | Doc 1, Doc 2 |

Now, if I search for "fox", the engine looks up the term "fox" in a highly optimized hash map or B-Tree, and immediately returns the list `[Doc 1, Doc 2]`. This changes the time complexity from $O(N)$ (scanning all documents) to $O(1)$ or $O(\log M)$ (finding the term in the dictionary), where $M$ is the number of unique words.

> [!NOTE]
> **Analogy Time:** Think of a forward index as the *Table of Contents* in a book (Chapter 1 contains these topics). Think of an inverted index as the *Index at the back of the book* (The word "Database" appears on pages 14, 82, and 105). When you need to find a specific word, you always use the index at the back.

### The Indexing Pipeline (Text Analysis)

You can't just take raw text and dump it into an inverted index. Human language is messy. If a user searches for "Running", they probably also want documents containing "Run" or "Ran".

Before text is indexed, it goes through an **Analyzer Pipeline**:
1. **Character Filtering:** Strip out HTML tags (`<b>`, `<i>`) or convert special characters.
2. **Tokenization:** Split the sentence into individual words (tokens). "The quick fox!" becomes `["The", "quick", "fox!"]`.
3. **Token Filtering:**
   - **Lowercasing:** "The" becomes "the".
   - **Stop Words Removal:** Remove extremely common, low-value words ("the", "is", "a").
   - **Stemming/Lemmatization:** Reduce words to their root form. "Running", "Ran", "Runs" all become "run".

Only after this rigorous normalization process are the terms added to the inverted index. This ensures that the search is resilient to typos, casing differences, and verb tenses.

> [!WARNING]
> **Common Beginner Mistake:** Over-stemming. If you stem aggressively, "Universal" and "University" might both reduce to "Univers". Now, a search for a university returns results about the universe. Always tune your analyzers to your specific business domain!

---

## Elasticsearch Architecture

Now that we know *how* text is stored, let's talk about the systems that manage it. **Elasticsearch (ES)** is the industry standard for distributed search. It is built on top of Apache Lucene (a Java-based search library) but adds a massive distributed system wrapper around it.

### The Core Components of Elasticsearch

Elasticsearch is designed to scale horizontally. Let's break down its topology:

1. **Cluster:** A collection of one or more servers (nodes) that together hold your entire data and provide federated indexing and search capabilities.
2. **Node:** A single server running an instance of Elasticsearch.
3. **Index:** A logical namespace that maps to one or more primary shards. (Think of it like a "Database" in SQL).
4. **Shard:** A single, self-contained instance of Apache Lucene. **This is the actual worker.**

### Why do we need Shards?

If you have 10 Terabytes of product data, you cannot fit it all on one 1TB hard drive. Furthermore, searching 10TB of data on a single CPU would take ages.

Elasticsearch solves this by **Sharding** the data. When you create an index, you tell ES to split it into, say, 5 primary shards. ES will distribute these 5 shards across the nodes in your cluster.

When a user executes a search query:
1. The request hits a **Coordinating Node**.
2. The coordinating node broadcasts the search query to *all 5 shards*.
3. Every shard executes the search locally on its subset of data in parallel.
4. Each shard returns its top 10 results to the coordinating node.
5. The coordinating node merges these 50 results, sorts them, and returns the absolute top 10 to the user.

This is known as the **Scatter-Gather** pattern. It allows Elasticsearch to provide millisecond latency even over Petabytes of data, because the workload is heavily parallelized.

### High Availability: Replicas

What if the server holding Shard 1 catches fire? You lose 20% of your search index. To prevent this, Elasticsearch uses **Replica Shards**.
For every primary shard, you can define $N$ replicas. ES guarantees that a primary shard and its replica will *never* live on the same physical node. Replicas not only provide failover redundancy but also increase read throughput, because search queries can be routed to replicas!

| Feature | Primary Shard | Replica Shard |
|---|---|---|
| **Handles Writes?** | Yes. All new documents go here first. | Yes, asynchronously copies from Primary. |
| **Handles Reads?** | Yes. | Yes. Great for scaling read-heavy workloads. |
| **Can it be changed?** | **NO.** You cannot change the number of primary shards after index creation (without a full re-index). | **YES.** You can add or remove replicas on the fly. |

> [!TIP]
> **Teacher FAQ:** *"Why can't I change the number of primary shards later?"*
> Because Elasticsearch uses a routing formula to decide which shard a document belongs to: `shard = hash(routing_id) % number_of_primary_shards`. If you change the denominator (number of primary shards), the entire math breaks, and ES wouldn't know where to find existing documents!

---

## Relevance Scoring (TF-IDF, BM25)

Finding the documents is only half the battle. If a search for "Apple" returns 10 million documents, how do we decide which 10 documents show up on Page 1? We need a mathematical way to score **Relevance**.

### The Legacy Standard: TF-IDF

For decades, the standard algorithm for text relevance was **TF-IDF (Term Frequency - Inverse Document Frequency)**. It consists of two opposing forces:

**1. Term Frequency (TF):** How many times does the search term appear in the document?
- If Document A says "Apple" once, and Document B says "Apple" 50 times, Document B is probably more relevant.
- *Rule: More occurrences = Higher Score.*

**2. Inverse Document Frequency (IDF):** How rare is the search term across the *entire* index?
- If you search for "The Apple", the word "The" appears in 99% of documents. It is virtually useless for identifying relevance. The word "Apple" might only appear in 1% of documents. It carries massive signal weight.
- *Rule: Rarer words globally = Higher Score.*

**The Formula:** `Score = TF * IDF`

> [!NOTE]
> **Analogy Time:** Imagine you are in a crowded room. TF is how loud a specific person is shouting a word. IDF evaluates how many other people are shouting the same word. If everyone is shouting "THE!" (Low IDF), it's just noise. If only one person is shouting "APPLE!" (High IDF), you immediately know exactly who to look at.

### The Modern Standard: BM25 (Best Matching 25)

TF-IDF is great, but it has a fatal flaw: **Term Frequency Saturation**.
Under pure TF-IDF, if a document contains "Apple" 1,000 times, its TF score shoots through the roof. This allows spammers to game the system by creating invisible text blocks repeating keywords (keyword stuffing).

**BM25**, which is the default in modern Elasticsearch, fixes this by introducing an asymptotic curve to Term Frequency.
- The first time a word appears, the score jumps up significantly.
- The 5th time, it goes up a bit more.
- By the 20th time, the score flattens out. Repeating the word 1,000 times gives almost no extra score compared to 20 times.

BM25 also factors in **Document Length**. If "Apple" appears 5 times in a 10-word tweet, that tweet is heavily about Apples. If "Apple" appears 5 times in a 1,000-page book, the book is probably not about Apples. BM25 penalizes overly long documents to level the playing field.

---

## Autocomplete / Typeahead Design

One of the most magical experiences in software is when a system finishes your sentence. When you type "Sys", Google immediately suggests "System Design Interview". How do you build a system that responds within 50 milliseconds while typing?

You cannot use a standard SQL database or even a standard inverted index for this. The queries are too frequent (firing on every keystroke) and require prefix matching.

### The Data Structure: The Trie (Prefix Tree)

The foundation of any autocomplete system is a tree data structure called a **Trie** (pronounced "try", from re**trie**val).

In a Trie, every node represents a character. The root node is empty.
If we insert the words "car", "cat", and "cart", the tree looks like this:

```text
       (root)
         |
         c
         |
         a
        / \
       r   t
      /
     t
```

When a user types "ca", we simply traverse down the tree: `root -> c -> a`. From the `a` node, we can perform a Depth-First Search (DFS) to find all valid words branching from there ("car", "cart", "cat").

### Scaling the Trie

While a Trie is elegant, it presents massive scaling challenges for a system like Google with billions of queries.

**Challenge 1: DFS is too slow for real-time.**
Running a full DFS on the tree for every keystroke takes too long.
*Solution:* **Pre-computation.** We store a cached list of the top 5 most popular search terms *directly on the prefix node*.
For the node `a` in `c -> a`, we don't do a DFS. We just read the cached list stored at node `a`: `[{term: "cat", weight: 99}, {term: "car", weight: 85}]`. This reduces retrieval to an $O(1)$ lookup!

**Challenge 2: The Trie is too big for memory.**
A global search Trie might be hundreds of gigabytes.
*Solution:* **Sharding / Partitioning.** We can partition the Trie across multiple cache servers (like Redis) based on the prefix.
- Server 1 handles prefixes starting with `a` through `m`.
- Server 2 handles prefixes starting with `n` through `z`.

### The Data Pipeline: How does the Trie update?

We cannot update the Trie synchronously every time a user searches for a new phrase; the write load would crush the system. Instead, we use an asynchronous pipeline:

1. **Log aggregation:** Every user search query is logged into an event streaming platform like **Apache Kafka**.
2. **Stream Processing / MapReduce:** A batch job (like Apache Spark or Hadoop) runs every hour. It aggregates the frequencies of all search terms. (e.g., "System Design" was searched 50,000 times this hour).
3. **Trie Builder:** A backend service consumes this aggregated data, builds a completely new, mathematically weighted Trie in memory.
4. **Swap:** The new Trie is serialized and pushed to the distributed cache (Redis/Memcached). The web servers swap their pointers to the new Trie seamlessly.

> [!TIP]
> **Teacher FAQ:** *"If the Trie is only updated every hour, how do trending topics (like breaking news) show up in autocomplete instantly?"*
> Excellent question! Massive scale systems actually run *two* Tries.
> 1. A **Historical Trie** (updated daily/hourly) holding long-term trends.
> 2. A **Real-Time Trending Trie** (updated via stream processors like Flink every few seconds).
> The application queries both Tries simultaneously, merges the results, and applies a heavy multiplier to the trending keywords so they surface to the top immediately.

---

### Summary Checklist for Interviews

If you are asked to design a Search or Autocomplete system in a System Design interview, make sure you hit these critical architectural pillars:
- Mention the **Inverted Index** and how it achieves $O(1)$ lookup time.
- Discuss **Scatter-Gather** architecture across Shards to prove you understand distributed search.
- Mention **BM25** to show you understand modern relevance scoring vs legacy TF-IDF.
- Use a **Trie (Prefix Tree)** for typeahead, and immediately mention caching the top results at the node level to avoid real-time DFS traversals.

Keep these concepts in your back pocket, and you'll ace any search-related system design discussion.
