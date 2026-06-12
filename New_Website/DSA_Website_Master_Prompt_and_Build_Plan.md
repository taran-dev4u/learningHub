# DSA Learning Website — Master Prompt + Complete Build Plan

This document has three parts. Use them together across multiple chat sessions, because the content (29 patterns, 158 subpatterns, 609 problems, plus foundations) is far too large for one generation.

- **PART A — The Master Prompt.** Paste this at the start of every build session. It locks in the teaching style, the lesson template, and the site architecture so every session produces consistent content.
- **PART B — The Phased Build Plan.** The exact order of build sessions, with a ready-to-paste session prompt for each phase.
- **PART C — The Complete Coverage Checklist.** Every module, pattern, and subpattern enumerated. Tick items off as they're built so nothing is ever skipped.

---

# PART A — THE MASTER PROMPT

Copy everything between the lines below and paste it as the first message of each build session, followed by the specific phase prompt from Part B.

---

You are building one section of **"DSA Academy"** — a complete, self-contained learning website that teaches Data Structures & Algorithms to an absolute beginner and takes them to advanced interview level. I will tell you which module/pattern to build in this session. Follow every rule below exactly.

## 1. Who you are teaching
A complete beginner. Assume they know basic programming syntax (variables, loops, functions in Python) and **nothing else**. Never use a term before defining it. Never say "obviously" or "simply." Every concept must be built from zero.

## 2. Your teaching persona
You are a world-class instructor. For every concept you must follow this teaching sequence — never skip a step:

1. **Real-world analogy first.** (A queue is a line at a movie theater; a stack is a pile of plates; a heap is a tournament bracket where the winner is always on top.)
2. **The problem it solves.** Why does this thing exist? What goes wrong without it?
3. **Plain-English definition.** One or two sentences, no jargon.
4. **Visual representation.** ASCII/diagram showing the structure and how it changes during operations.
5. **Step-by-step dry run.** Walk through a tiny example by hand, state-by-state (show the array/pointers/tree at every step).
6. **Code.** Clean, commented Python (primary). Every line that does something non-obvious gets a comment explaining *why*, not *what*.
7. **Complexity.** Time and space for each operation, with one-line intuition for *why* (not just the answer).
8. **Edge cases & pitfalls.** Empty input, single element, duplicates, overflow, off-by-one — list the classic mistakes beginners make.
9. **Differences & comparisons.** Compare against the closest sibling concept in a table (e.g., stack vs queue, BFS vs DFS, Dijkstra vs Bellman-Ford, segment tree vs Fenwick tree, memoization vs tabulation).
10. **When to use / when NOT to use.** Recognition signals — what words in a problem statement hint at this tool.

## 3. Data structure coverage rule (non-negotiable)
When a module covers a data structure, you must cover **every operation** from scratch:
- **Create / initialize**
- **Insert / add** (all variants: front, back, middle, by priority…)
- **Delete / remove** (all variants)
- **Update / modify**
- **Access / search / peek**
- **Traverse** (all orders that apply)
- Plus structure-specific operations (heapify, rotate, rehash, balance, union, find, etc.)

Each operation gets: analogy → diagram → dry run → code → complexity → edge cases. No operation is "left as exercise."

## 4. Pattern lesson template (for the 29 pattern modules)
Every **pattern** page must contain, in this order:
1. **One-paragraph intuition** — the core mental model in plain English.
2. **The "aha" insight** — what makes this pattern collapse a brute force into something efficient (show the brute force first, then the optimization).
3. **Recognition signals** — bullet list: "if the problem says X, Y, Z → think of this pattern."
4. **Master template code** — the reusable skeleton in Python with comments marking the parts that change per problem.
5. **Visual dry run** of the template on a small example.
6. **Complexity** of the template.
7. **Subpattern sections** — one per subpattern (listed in Part C). Each subpattern gets: how it differs from the base pattern, its own mini-template if the code changes, and its full problem list.
8. **Comparison table** vs related patterns (e.g., Sliding Window vs Two Pointers vs Prefix Sum).
9. **Common mistakes** in this pattern.
10. **Pattern quiz** — 3–5 "which pattern is this?" mini-prompts with answers hidden in a collapsible.

## 5. Problem coverage rule (non-negotiable)
Every problem listed for a subpattern must appear with:
- LeetCode number, name, difficulty pill (E/M/H), and list badges (Blind 75 / NeetCode 150 / Grind 75) when applicable
- **Problem restated in plain English** (one or two sentences, beginner-friendly)
- **Key insight** — the one realization that unlocks it (1–3 sentences)
- **Approach walkthrough** — numbered steps from brute force → optimal, with the intuition for each leap
- **Full commented Python solution**
- **Complexity** with reasoning
- **Edge cases** specific to this problem
- **Variations / follow-ups** interviewers commonly ask
- Link to the LeetCode problem page

Do not skip problems. If a session would exceed output limits, say so and split the subpattern across continuation messages — never silently omit a problem.

## 6. Website technical specification
- **Single-file HTML pages** (HTML + CSS + JS inline), no build tools, no external dependencies except optional CDN for syntax highlighting (highlight.js from cdnjs).
- **Multi-page architecture**: one `index.html` hub + one HTML file per module (e.g., `m0-1-arrays.html`, `p05-sliding-window.html`). Hub links to all pages; every page links back to the hub and to prev/next module.
- **Dark/light theme toggle** (persisted in a JS variable per session; do NOT use localStorage — use in-memory state).
- **Collapsible sections** (`<details>/<summary>`) for solutions and quiz answers — beginners should attempt before revealing.
- **Progress checkboxes** next to every problem and every subpattern (in-memory state).
- **Copy buttons** on every code block.
- **Search/filter bar** on the hub page (filter by topic name).
- **Responsive** — must read well on a phone.
- Consistent visual identity across all pages: same CSS variables, same header/nav, same component styles. (Define them once in this session's first file and reuse verbatim.)

## 7. Quality bar
- No placeholder content, no "TODO," no "explanation goes here."
- No hand-waving: every claim about complexity gets a one-line justification.
- Code must be correct and runnable. Dry-run your own code mentally before output.
- Tone: encouraging, precise, zero fluff. Like the best teacher the student ever had.

---
*(End of Master Prompt)*

---

# PART B — THE PHASED BUILD PLAN

Run these sessions **in order**. Foundations come first because the pattern index assumes you already know the data structures. Each session: paste the Master Prompt (Part A), then the session prompt below, then attach or paste the relevant subpattern + problem list from the checklist in Part C (so the model knows the exact problems to include).

Estimated total: **~40 build sessions**. Heavy modules (Trees, Graphs, DP) are split.

## PHASE 0 — Site skeleton (1 session)
> **Session prompt:** "Build `index.html` — the DSA Academy hub. Include: hero, search/filter bar, and a card grid linking to every module listed below (use the exact module list and file names from my checklist — Module 0.1 through 0.12 and Patterns P1 through P29). Each card shows module number, title, subpattern count, problem count, and a progress bar placeholder. Also define the shared CSS design system (variables, components) that all future pages will copy. Include the Pattern Recognition Cheat Sheet table, the Big-O Reference tables, and the 14-Week Study Plan as three collapsible sections on the hub (I will paste their content)."

## PHASE 1 — Foundations: Module 0 (12 sessions, one per sub-module)
These teach the raw data structures and prerequisite skills with EVERY operation, before any pattern.

| Session | File | Content |
|---|---|---|
| 0.1 | `m0-1-complexity.html` | Big-O from scratch: what counting steps means, best/avg/worst, amortized, space complexity, log intuition, comparing growth rates, how to analyze loops/recursion (recursion tree + master theorem intuition) |
| 0.2 | `m0-2-arrays-strings.html` | Arrays & dynamic arrays: memory layout, indexing, insert/delete/update/search/traverse, resizing & amortized O(1), 2D arrays/matrices; strings: immutability, building, slicing |
| 0.3 | `m0-3-hashing.html` | Hash maps & sets from scratch: hash functions, collisions (chaining vs open addressing), load factor & rehashing, all operations, why O(1) average, when it degrades |
| 0.4 | `m0-4-linked-lists.html` | Singly/doubly/circular: node anatomy, insert (head/tail/middle), delete, update, search, traverse, dummy-node trick, vs arrays comparison |
| 0.5 | `m0-5-stacks-queues.html` | Stack: push/pop/peek/isEmpty, array vs linked implementation. Queue: enqueue/dequeue/peek, circular queue, deque — every operation. Stack vs queue table |
| 0.6 | `m0-6-recursion.html` | Recursion from zero: call stack visualized, base/recursive case, tree of calls, recursion→iteration conversion, tail recursion, classic exercises (factorial, fib, power, reverse) |
| 0.7 | `m0-7-trees.html` | Tree vocabulary (root/leaf/height/depth), binary trees, BST: insert/search/delete (all 3 delete cases)/update/min/max/successor, traversals (pre/in/post/level) each dry-run, balanced-tree concept (why AVL/Red-Black exist, rotations conceptually) |
| 0.8 | `m0-8-heaps.html` | Binary heap from scratch: array representation, parent/child index math, insert (sift-up), extract-min/max (sift-down), peek, heapify O(n) proof intuition, update-key, delete-arbitrary, heap sort, Python `heapq` mapping |
| 0.9 | `m0-9-graphs.html` | Graph vocabulary (vertex/edge/directed/weighted/cycle), representations (adjacency list/matrix/edge list + conversion), add/remove vertex & edge, degree, BFS and DFS mechanics dry-run (visited sets, queue vs stack) |
| 0.10 | `m0-10-sorting.html` | Bubble, selection, insertion, merge, quick, heap, counting, radix, bucket — each with full mechanics, dry run, code, stability, complexity table, when to use which |
| 0.11 | `m0-11-tries-dsu.html` | Trie: node structure, insert/search/startsWith/delete. Union-Find: parent array, find, union, path compression, union by rank, α(N) intuition |
| 0.12 | `m0-12-advanced-ds.html` | Segment tree (build/query/update, lazy concept), Fenwick/BIT (the lowbit trick, prefix query, point update), ordered maps/TreeMap concept, monotonic stack/queue as reusable tools |

> **Session prompt template (Phase 1):** "Build `[file]` covering [content row]. Follow the Master Prompt teaching sequence for EVERY operation listed. This is a Foundations page — no LeetCode problems yet, but end with a 'Where you'll use this' box linking to the relevant pattern pages."

## PHASE 2 — Core linear patterns (sessions, in study-plan order)
| Session | File | Pattern | Size |
|---|---|---|---|
| 2.1 | `p01-two-pointers.html` | P1: Two Pointers — 7 subpatterns, 37 problems | split into 2 sessions if needed |
| 2.2 | `p02-array-matrix.html` | P2: Array/Matrix Manipulation — 10 subpatterns, 24 problems | 1–2 sessions |
| 2.3 | `p05-sliding-window.html` | P5: Sliding Window — 4 subpatterns, 33 problems | 2 sessions |
| 2.4 | `p17-prefix-sum.html` | P17: Prefix Sum & Difference Array — 4 subpatterns, 13 problems | 1 session |

## PHASE 3 — Linear data structure patterns
| Session | File | Pattern |
|---|---|---|
| 3.1 | `p03-linked-list.html` | P3: Linked List Manipulation — 5 subpatterns, 22 problems |
| 3.2 | `p06-stack.html` | P6: Stack Patterns — 6 subpatterns, 32 problems (2 sessions; Monotonic Stack alone has 17) |
| 3.3 | `p07-heap.html` | P7: Heap Patterns — 4 subpatterns, 30 problems (2 sessions) |

## PHASE 4 — Search & hashing patterns
| Session | File | Pattern |
|---|---|---|
| 4.1 | `p08-binary-search.html` | P8: Binary Search — 5 subpatterns, 29 problems (2 sessions) |
| 4.2 | `p18-hashmap-cache.html` | P18: Hash Map & Cache Design — 5 subpatterns, 10 problems |
| 4.3 | `p14-bit-manipulation.html` | P14: Bit Manipulation — 4 subpatterns, 16 problems |

## PHASE 5 — Trees
| Session | File | Pattern |
|---|---|---|
| 5.1 | `p04-tree-traversal.html` | P4: Tree Traversal — 6 subpatterns, 54 problems (3 sessions: BFS+preorder / inorder+postorder / LCA+serialization) |
| 5.2 | `p22-tree-dp.html` | P22: Tree DP — 4 subpatterns, 8 problems |

## PHASE 6 — Graphs
| Session | File | Pattern |
|---|---|---|
| 6.1 | `p09-graph-traversal.html` | P9: Graph Traversal — 11 subpatterns, 69 problems (3–4 sessions: DFS/BFS islands / topo+cycle / Dijkstra+Bellman / DSU+bipartite+MST+state-space) |
| 6.2 | `p25-multi-source-bfs.html` | P25: Multi-Source BFS — 1 subpattern, 6 problems |
| 6.3 | `p24-advanced-graph.html` | P24: Advanced Graph — 9 subpatterns, 27 problems (2 sessions) |

## PHASE 7 — Dynamic Programming
| Session | File | Pattern |
|---|---|---|
| 7.1 | `p12-dp.html` | P12: DP — 12 subpatterns, 50 problems (3 sessions: 1D styles / 2D styles / interval+Catalan+LIS+palindrome). Begin with a DP-from-zero primer: what is a state, memoization vs tabulation, how to derive a recurrence |
| 7.2 | `p23-advanced-dp.html` | P23: Advanced DP — 5 subpatterns, 30 problems (2 sessions) |

## PHASE 8 — Greedy & Backtracking
| Session | File | Pattern |
|---|---|---|
| 8.1 | `p10-greedy.html` | P10: Greedy — 7 subpatterns, 25 problems. Include the "how to argue a greedy is correct" exchange-argument primer |
| 8.2 | `p11-backtracking.html` | P11: Backtracking — 7 subpatterns, 27 problems |

## PHASE 9 — Strings
| Session | File | Pattern |
|---|---|---|
| 9.1 | `p13-string-manipulation.html` | P13: String Manipulation — 7 subpatterns, 23 problems (KMP/Rabin-Karp taught fully from scratch) |
| 9.2 | `p29-advanced-strings.html` | P29: Advanced String — 3 subpatterns, 7 problems (Manacher, Z-algorithm from scratch) |

## PHASE 10 — Specialized structures & design
| Session | File | Pattern |
|---|---|---|
| 10.1 | `p15-design.html` | P15: Design — 2 subpatterns, 43 problems (2–3 sessions; the General Design subpattern alone has 40) |
| 10.2 | `p16-segment-fenwick.html` | P16: Segment & Fenwick Tree — 2 subpatterns, 12 problems |
| 10.3 | `p20-trie.html` | P20: Trie — 5 subpatterns, 17 problems |
| 10.4 | `p21-intervals-sweep.html` | P21: Intervals & Line Sweep — 4 subpatterns, 16 problems |
| 10.5 | `p26-iterators-streams.html` | P26: Iterator & Data-Stream Design — 6 subpatterns, 13 problems |

## PHASE 11 — Math, sorting, randomized
| Session | File | Pattern |
|---|---|---|
| 11.1 | `p19-math.html` | P19: Math, Number Theory & Geometry — 5 subpatterns, 20 problems |
| 11.2 | `p27-sorting-selection.html` | P27: Sorting & Selection — 4 subpatterns, 8 problems |
| 11.3 | `p28-randomized.html` | P28: Randomized Algorithms — 4 subpatterns, 6 problems |

## PHASE 12 — Final integration (1 session)
> "Update `index.html`: verify every module file is linked, add the cross-referenced-problems section, add a final 'Am I ready?' self-assessment checklist (pattern recognition drills, complexity trade-offs, edge-case checklist, mock interview communication, re-solving weak problems), and a prev/next chain across all pages in study-plan order."

### Rules to enforce in every session
1. Paste Part A first, then the phase prompt, then the exact subpattern/problem list from Part C for that module.
2. At the end of each session, ask: *"List every subpattern and problem you just covered."* Diff it against Part C. Anything missing → "Continue, you omitted: …"
3. If output gets cut, say "continue exactly where you stopped" — never restart the file.
4. Keep all generated files; the design system from Phase 0 is copied verbatim into every page.

---

# PART C — COMPLETE COVERAGE CHECKLIST

Every pattern and subpattern from your index, with problem counts. Tick each when its page is built AND its problem list is verified complete. (Problem-by-problem lists live in your original `DSA_Ultimate_Index.html` — keep it open and paste the relevant problem list into each session.)

## Module 0 — Foundations (new, prerequisite layer)
- [ ] 0.1 Complexity Analysis & Big-O
- [ ] 0.2 Arrays, Dynamic Arrays, Strings, Matrices
- [ ] 0.3 Hash Maps & Hash Sets (internals)
- [ ] 0.4 Linked Lists (singly/doubly/circular)
- [ ] 0.5 Stacks, Queues, Deques, Circular Queues
- [ ] 0.6 Recursion & the Call Stack
- [ ] 0.7 Trees & BSTs (all operations, balance concept)
- [ ] 0.8 Heaps / Priority Queues (all operations)
- [ ] 0.9 Graph Representations + BFS/DFS mechanics
- [ ] 0.10 All Sorting Algorithms
- [ ] 0.11 Tries & Union-Find
- [ ] 0.12 Segment Tree, Fenwick Tree, TreeMap, Monotonic structures

## P1 Two Pointer Patterns — 7 sp · 37 problems
- [ ] 1.1 Converging (12)
- [ ] 1.2 String Reversal (4)
- [ ] 1.3 In-place Array Modification (11)
- [ ] 1.4 Fast and Slow (4)
- [ ] 1.5 Fixed Separation (3)
- [ ] 1.6 String Comparison with Special Characters (1)
- [ ] 1.7 Expanding From Center (2)

## P2 Array/Matrix Manipulation — 10 sp · 24 problems
- [ ] 2.1 In-place Rotation (2)
- [ ] 2.2 Spiral Traversal (3)
- [ ] 2.3 Set Matrix Zeroes / In-place Marking (1)
- [ ] 2.4 Product Except Self / Prefix-Suffix Products (1)
- [ ] 2.5 Plus One / Handling Carry (1)
- [ ] 2.6 Merge Sorted Array / In-place from End (1)
- [ ] 2.7 Cyclic Sort (5)
- [ ] 2.8 Matrix Search / Sorted Matrix (3)
- [ ] 2.9 Prefix Sum / Running Sum (6)
- [ ] 2.10 Kadane Variant for Maximum Product (1)

## P3 Linked List Manipulation — 5 sp · 22 problems
- [ ] 3.1 In-place Reversal (7)
- [ ] 3.2 Merging Two Sorted Lists (1)
- [ ] 3.3 Addition of Numbers (2)
- [ ] 3.4 Intersection Detection (1)
- [ ] 3.5 Reordering / Partitioning (11)

## P4 Tree Traversal (DFS & BFS) — 6 sp · 54 problems
- [ ] 4.1 BFS — Level Order Traversal (11)
- [ ] 4.2 DFS — Recursive Preorder (13)
- [ ] 4.3 DFS — Recursive Inorder (12)
- [ ] 4.4 DFS — Recursive Postorder (12)
- [ ] 4.5 Lowest Common Ancestor (4)
- [ ] 4.6 Serialization & Deserialization (2)

## P5 Sliding Window — 4 sp · 33 problems
- [ ] 5.1 Fixed Size / Subarray Calculation (7)
- [ ] 5.2 Variable Size / Condition-Based (21)
- [ ] 5.3 Monotonic Queue for Max/Min (3)
- [ ] 5.4 Character Frequency Matching (2)

## P6 Stack Patterns — 6 sp · 32 problems
- [ ] 6.1 Valid Parentheses Matching (6)
- [ ] 6.2 Monotonic Stack (17)
- [ ] 6.3 Expression Evaluation / RPN / Infix (5)
- [ ] 6.4 Simulation / Backtracking Helper (2)
- [ ] 6.5 Min Stack Design (1)
- [ ] 6.6 Largest Rectangle in Histogram (1)

## P7 Heap (Priority Queue) — 4 sp · 30 problems
- [ ] 7.1 Top K Elements / Selection / Frequency (9)
- [ ] 7.2 Two Heaps for Median Finding (2)
- [ ] 7.3 K-way Merge (4)
- [ ] 7.4 Scheduling / Min Cost with PQ (15)

## P8 Binary Search — 5 sp · 29 problems
- [ ] 8.1 On Sorted Array/List (9)
- [ ] 8.2 Min/Max in Rotated Sorted Array (6)
- [ ] 8.3 On Answer / Condition Function (11)
- [ ] 8.4 First/Last Occurrence (2)
- [ ] 8.5 Median of Two Sorted Arrays (1)

## P9 Graph Traversal (DFS & BFS) — 11 sp · 69 problems
- [ ] 9.1 DFS — Connected Components / Islands (11)
- [ ] 9.2 BFS — Connected Components / Islands (5)
- [ ] 9.3 DFS — Cycle Detection, Directed (4)
- [ ] 9.4 BFS — Topological Sort (Kahn's) (10)
- [ ] 9.5 Deep Copy / Cloning (1)
- [ ] 9.6 Shortest Path — Dijkstra (10)
- [ ] 9.7 Shortest Path — Bellman-Ford / BFS+K (1)
- [ ] 9.8 Union-Find / DSU (19)
- [ ] 9.9 Bipartite Coloring (2)
- [ ] 9.10 Minimum Spanning Tree (3)
- [ ] 9.11 BFS on State Space (3)

## P10 Greedy — 7 sp · 25 problems
- [ ] 10.1 Interval Merging / Scheduling (7)
- [ ] 10.2 Jump Game Reachability / Minimization (2)
- [ ] 10.3 Buy/Sell Stock (5)
- [ ] 10.4 Gas Station Circuit (1)
- [ ] 10.5 Task Scheduling / Frequency Based (3)
- [ ] 10.6 Partition / Labels (1)
- [ ] 10.7 Assign / Resource Allocation (6)

## P11 Backtracking — 7 sp · 27 problems
- [ ] 11.1 Subsets / Include-Exclude (4)
- [ ] 11.2 Permutations (6)
- [ ] 11.3 Combination Sum (3)
- [ ] 11.4 Parentheses Generation (2)
- [ ] 11.5 Word Search / Grid Path Finding (5)
- [ ] 11.6 N-Queens / Constraint Satisfaction (6)
- [ ] 11.7 Palindrome Partitioning (1)

## P12 Dynamic Programming — 12 sp · 50 problems
- [ ] 12.1 1D / Fibonacci Style (9)
- [ ] 12.2 1D / Kadane's Max-Min Subarray (1)
- [ ] 12.3 1D / Coin Change / Unbounded Knapsack (4)
- [ ] 12.4 1D / 0-1 Knapsack Subset Sum (2)
- [ ] 12.5 1D / Word Break Style (2)
- [ ] 12.6 2D / Longest Common Subsequence (5)
- [ ] 12.7 2D / Edit Distance (3)
- [ ] 12.8 2D / Unique Paths on Grid (7)
- [ ] 12.9 Interval DP (2)
- [ ] 12.10 Catalan Numbers (3)
- [ ] 12.11 Longest Increasing Subsequence (7)
- [ ] 12.12 Palindrome DP (5)

## P13 String Manipulation — 7 sp · 23 problems
- [ ] 13.1 Palindrome Check / Two Pointers / Reverse (3)
- [ ] 13.2 Anagram Check / Frequency / Sort (2)
- [ ] 13.3 Roman to Integer (1)
- [ ] 13.4 String to Integer (atoi) (1)
- [ ] 13.5 Multiply Strings / Manual Simulation (3)
- [ ] 13.6 String Matching / Naive / KMP / Rabin-Karp (12)
- [ ] 13.7 Repeated Substring Pattern Detection (1)

## P14 Bit Manipulation — 4 sp · 16 problems
- [ ] 14.1 XOR / Single or Missing Number (5)
- [ ] 14.2 AND / Counting Set Bits (3)
- [ ] 14.3 Bitwise DP / Counting Bits (2)
- [ ] 14.4 Power of Two or Four Check (6)

## P15 Design — 2 sp · 43 problems
- [ ] 15.1 General / Specific Data Structure Design (40)
- [ ] 15.2 Trie / Prefix Tree Design (3)

## P16 Segment Tree & Fenwick Tree — 2 sp · 12 problems
- [ ] 16.1 Segment Tree / Range Query with Updates (8)
- [ ] 16.2 Fenwick Tree / BIT / Coordinate Compression (4)

## P17 Prefix Sum & Difference Array — 4 sp · 13 problems
- [ ] 17.1 Subarray Sum with Hashmap (7)
- [ ] 17.2 Range Sum Query, Static (2)
- [ ] 17.3 Difference Array / Range Update (3)
- [ ] 17.4 Prefix XOR / Prefix Product (1)

## P18 Hash Map & Cache Design — 5 sp · 10 problems
- [ ] 18.1 Grouping / Frequency (4)
- [ ] 18.2 LRU Cache Design (1)
- [ ] 18.3 LFU Cache Design (2)
- [ ] 18.4 Time-Based / Snapshot Storage (1)
- [ ] 18.5 Hashmap + Random Access O(1) (2)

## P19 Math, Number Theory & Geometry — 5 sp · 20 problems
- [ ] 19.1 Powers, Logs, Roots (3)
- [ ] 19.2 Number Representation Conversion (3)
- [ ] 19.3 Primes & Sieve (4)
- [ ] 19.4 Geometry & Points (6)
- [ ] 19.5 GCD, LCM & Combinatorics (4)

## P20 Trie / Prefix Tree — 5 sp · 17 problems
- [ ] 20.1 Trie Core, Insert/Search (3)
- [ ] 20.2 Trie with Wildcards (1)
- [ ] 20.3 Trie + DFS on Grid / Strings (2)
- [ ] 20.4 Streaming / Autocomplete / Suffix Trie (9)
- [ ] 20.5 XOR Trie / Binary Trie (2)

## P21 Intervals & Line Sweep — 4 sp · 16 problems
- [ ] 21.1 Interval Merging / Insertion (4)
- [ ] 21.2 Meeting Rooms & Scheduling (5)
- [ ] 21.3 Line Sweep with Events (3)
- [ ] 21.4 Calendar / Booking (TreeMap) (4)

## P22 Tree DP — 4 sp · 8 problems
- [ ] 22.1 Include/Exclude on Tree — Tree Robber (1)
- [ ] 22.2 Tree Diameter & Longest Path (3)
- [ ] 22.3 Tree Max Path Sum / Tilt (2)
- [ ] 22.4 Subtree Summary DP (2)

## P23 Advanced DP — 5 sp · 30 problems
- [ ] 23.1 Bitmask / Subset DP / TSP-style (8)
- [ ] 23.2 Digit DP (4)
- [ ] 23.3 State-Machine DP, Stock & Beyond (4)
- [ ] 23.4 Interval / Partition DP (6)
- [ ] 23.5 Grid-Cost DP, Paint House / Cherry Pickup (8)

## P24 Advanced Graph — 9 sp · 27 problems
- [ ] 24.1 Tarjan: Bridges, Articulation, SCC (1)
- [ ] 24.2 Eulerian Path, Hierholzer (2)
- [ ] 24.3 All-Pairs Shortest Path, Floyd-Warshall (1)
- [ ] 24.4 Bellman-Ford / BFS with K Steps (2)
- [ ] 24.5 Dijkstra Variants on Weighted Grids (6)
- [ ] 24.6 0-1 BFS, Deque Variant (1)
- [ ] 24.7 Bidirectional BFS / State-Space BFS (5)
- [ ] 24.8 Topological-Sort Applications (7)
- [ ] 24.9 Functional Graph / Safe-State Analysis (2)

## P25 Multi-Source BFS — 1 sp · 6 problems
- [ ] 25.1 Multi-Source Distance BFS (6)

## P26 Iterator & Data-Stream Design — 6 sp · 13 problems
- [ ] 26.1 BST Iterator (1)
- [ ] 26.2 Peeking / Wrapping Iterators (1)
- [ ] 26.3 Multi-Source Iterators (2)
- [ ] 26.4 Nested List / 2D Iterator (2)
- [ ] 26.5 Streaming Statistics (3)
- [ ] 26.6 Stack / Queue Conversion (4)

## P27 Sorting Algorithms & Selection — 4 sp · 8 problems
- [ ] 27.1 Quickselect, Kth Element (2)
- [ ] 27.2 Merge-Sort Applications (1)
- [ ] 27.3 Bucket / Counting / Radix Sort (3)
- [ ] 27.4 Custom-Comparator Sort (2)

## P28 Randomized Algorithms — 4 sp · 6 problems
- [ ] 28.1 Reservoir Sampling (2)
- [ ] 28.2 Weighted Random, Prefix Sum + Binary Search (1)
- [ ] 28.3 Fisher-Yates Shuffle (1)
- [ ] 28.4 Random Pick with Blacklist (2)

## P29 Advanced String Algorithms — 3 sp · 7 problems
- [ ] 29.1 Manacher's Algorithm, Linear Palindrome (1)
- [ ] 29.2 Z-Algorithm / KMP Failure-Function Applications (3)
- [ ] 29.3 Rolling Hash Beyond Rabin-Karp (3)

## Hub extras (from your index — include on `index.html`)
- [ ] Pattern Recognition Cheat Sheet (problem-signal → pattern table)
- [ ] Big-O Reference (data structures, sorting, graph, string algorithm tables)
- [ ] 14-Week Study Plan
- [ ] Cross-Referenced Problems section
- [ ] DSA Coverage Check / self-assessment

**Totals: 29 patterns · 158 subpatterns · 609 unique problems (707 listed slots) + 12 foundation modules.**

---

## How to verify nothing was missed (final audit)
1. After all phases, open each generated page and count its subpattern headers against this checklist.
2. For each subpattern, count problems on the page vs the count in parentheses above.
3. For an exact problem-name diff, paste a page's problem list and the corresponding section of your original `DSA_Ultimate_Index.html` into a session and ask: "Diff these two lists; report any problem in the index missing from the page."
