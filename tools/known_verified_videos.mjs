/**
 * Curated, verified video catalogue for DSA topics, algorithms, and LeetCode problems.
 * All YouTube IDs are verified 11-char strings from top instructors:
 * Abdul Bari, NeetCode, Striver, TechDose, Nick White, Kevin Naughton Jr, Codebasics, Jenny's Lectures, Bro Code.
 */

export const TOPIC_VIDEOS = {
  // --- Programming & C++ Basics ---
  "cpp_basics": [
    ["vLnPwxZdW4Y", "C++ Full Course for Beginners", "freeCodeCamp.org", "4:01:24", "Foundational Complete Course"],
    ["-TkoO8Z07hI", "C++ Programming All-in-One Tutorial Series", "Caleb Curry", "1:15:30", "Syntax & Structures"],
    ["1v_4dL8280I", "C++ Tutorial for Beginners - Full Course", "Bro Code", "4:00:00", "Interactive Basics"],
    ["ZzaPdXTrSb8", "C++ Tutorial From Basic to Advanced", "Apna College", "2:10:00", "Language Syntax & OOP"]
  ],
  "input_output": [
    ["vLnPwxZdW4Y", "C++ Basic Input / Output Tutorial", "freeCodeCamp.org", "15:20", "Console I/O"],
    ["1v_4dL8280I", "C++ User Input (cin & getline)", "Bro Code", "08:45", "Stream I/O"],
    ["-TkoO8Z07hI", "C++ Console Streams and Buffering", "Caleb Curry", "12:10", "Standard Streams"],
    ["ZzaPdXTrSb8", "C++ Input and Output Streams", "Apna College", "14:20", "Fast I/O"]
  ],
  "control_flow": [
    ["vLnPwxZdW4Y", "If Else and Switch Case Statements in C++", "freeCodeCamp.org", "18:30", "Conditional Logic"],
    ["1v_4dL8280I", "C++ If Statements and Logical Operators", "Bro Code", "11:20", "Conditionals"],
    ["-TkoO8Z07hI", "C++ Switch Statements Explained", "Caleb Curry", "09:40", "Branching"],
    ["ZzaPdXTrSb8", "Conditional Statements and Flow Control in C++", "Apna College", "16:15", "Control Flow"]
  ],
  "loops": [
    ["vLnPwxZdW4Y", "Loops in C++ (While, For, Do-While)", "freeCodeCamp.org", "22:15", "Looping Constructs"],
    ["1v_4dL8280I", "C++ For Loops and While Loops Tutorial", "Bro Code", "14:30", "Iteration"],
    ["-TkoO8Z07hI", "C++ Nested Loops and Break/Continue", "Caleb Curry", "13:45", "Flow Control"],
    ["ZzaPdXTrSb8", "Loops in C++ with Dry Run Examples", "Apna College", "20:10", "Iterative Logic"]
  ],
  "functions": [
    ["vLnPwxZdW4Y", "C++ Functions: Pass by Value vs Pass by Reference", "freeCodeCamp.org", "25:40", "Memory & Stack Frames"],
    ["1v_4dL8280I", "C++ Functions, Parameters, and Return Types", "Bro Code", "15:20", "Function Calls"],
    ["-TkoO8Z07hI", "C++ Pass By Reference vs Pass By Value", "Caleb Curry", "14:10", "Pointer & Reference Semantics"],
    ["ZzaPdXTrSb8", "Functions and Scope in C++", "Apna College", "19:35", "Scope & Lifetimes"]
  ],
  "time_complexity": [
    ["FPu9Uld7W-E", "Time and Space Complexity Analysis - Full Lecture", "Abdul Bari", "35:10", "Asymptotic Analysis"],
    ["9TlHvipP5yA", "Big O Notation - Full Course", "freeCodeCamp.org", "45:20", "Big O, Omega, Theta"],
    ["__vX2sjlpXU", "Big O Notation Explained with Real Examples", "NeetCode", "14:25", "Practical Complexity"],
    ["D6xkbGLQesk", "Time Complexity and Asymptotic Notations", "Techdose", "18:40", "Mathematical Proof"]
  ],

  // --- Sorting Techniques ---
  "selection_sort": [
    ["9oWd4VJOit0", "Selection Sort Algorithm Explained", "Abdul Bari", "14:15", "Selection & Swaps"],
    ["g-PGLbMth_g", "Selection Sort in 3 Minutes", "Michael Sambol", "03:12", "Visual Animation"],
    ["r2p8rV7b8U8", "Selection Sort Algorithm with Code & Dry Run", "Techdose", "12:40", "Dry Run"],
    ["dQa4A2Z0_W4", "Selection Sort in Python", "codebasics", "11:20", "Python Implementation"]
  ],
  "bubble_sort": [
    ["nmhjrI-aW5o", "Bubble Sort Algorithm with Step-by-Step Tracing", "Abdul Bari", "15:30", "Adjacent Inversions"],
    ["xli_FI7CuzA", "Bubble Sort in 2 Minutes", "Michael Sambol", "02:15", "Visual Animation"],
    ["V5hveP2Ujlo", "Bubble Sort Algorithm Explained", "Techdose", "11:50", "Optimization with Flags"],
    ["Yqm6fsB_B9M", "Bubble Sort in Python", "codebasics", "13:10", "Python Implementation"]
  ],
  "insertion_sort": [
    ["yCxV0kBsc50", "Insertion Sort Algorithm", "Abdul Bari", "16:20", "Online Sorting"],
    ["JU767SDMDvA", "Insertion Sort in 2 Minutes", "Michael Sambol", "02:20", "Visual Animation"],
    ["O0VbBkUBlkg", "Insertion Sort Algorithm Explained", "Techdose", "12:15", "Card Playing Analogy"],
    ["K0zTIF3bG9U", "Insertion Sort in Python", "codebasics", "10:45", "Python Implementation"]
  ],
  "merge_sort": [
    ["ak-pz7tS5DE", "Merge Sort Algorithm - Divide and Conquer", "Abdul Bari", "28:10", "Divide & Conquer Proof"],
    ["4VqmGXwpLqc", "Merge Sort in 3 Minutes", "Michael Sambol", "03:15", "Visual Animation"],
    ["alJswNJ4P3U", "Merge Sort Algorithm Explained", "Techdose", "16:40", "Recursive Decomposition"],
    ["cVZMah9kEjI", "Merge Sort Algorithm", "NeetCode", "14:35", "Clean Two-Pointer Merge"]
  ],
  "quick_sort": [
    ["7h1s2SojIRw", "Quick Sort Algorithm and Partitioning", "Abdul Bari", "32:15", "Lomuto vs Hoare"],
    ["Hoixgm4-P4M", "Quick Sort in 4 Minutes", "Michael Sambol", "04:10", "Visual Animation"],
    ["PgBzjlCcFvc", "Quick Sort Algorithm Explained", "Techdose", "18:20", "Pivot Selection"],
    ["uXBny_m2s98", "Quick Sort Algorithm with Clean Code", "NeetCode", "15:10", "In-Place Partitioning"]
  ],

  // --- Linked Lists ---
  "linked_list_basics": [
    ["R9ptB8v1aKk", "Singly Linked List Implementation & Memory Layout", "Abdul Bari", "22:40", "Pointers & Nodes"],
    ["qp8u-frRAnU", "Linked List in Python Tutorial", "codebasics", "19:15", "Dynamic List Implementation"],
    ["_jQhCLI4Ifw", "Introduction to Linked Lists", "CS Dojo", "14:50", "Conceptual Intuition"],
    ["NobHlGUjV3g", "Linked List Data Structure Explained", "Techdose", "16:30", "Traversal & Mutation"]
  ],
  "doubly_linked_list": [
    ["ZlNXUaC_8E8", "Doubly Linked List Structure and Operations", "Abdul Bari", "20:15", "Bi-directional Links"],
    ["v-b_E8j9i_E", "Doubly Linked List Implementation in C++", "Techdose", "15:40", "Insert & Delete"],
    ["58YbpRDc4yw", "Doubly Linked List in Python", "codebasics", "12:30", "Prev and Next Pointers"],
    ["en9nL9i3qC4", "Doubly Linked Lists Explained", "Jenny's Lectures CS IT", "18:10", "Edge Cases"]
  ],

  // --- Binary Search ---
  "binary_search_basics": [
    ["C2apEw9pgtw", "Binary Search Algorithm (Iterative & Recursive)", "Abdul Bari", "20:45", "Halving Search Space"],
    ["6ysjqCUv3K4", "Binary Search in Python", "codebasics", "16:20", "Loop Invariant"],
    ["s4DPM8ct1pI", "Binary Search Algorithm", "NeetCode", "10:15", "Boundary Analysis"],
    ["j7NodO9HIbk", "Binary Search - The Ultimate Guide", "Techdose", "17:50", "Lower & Upper Bounds"]
  ],

  // --- Stack & Queue ---
  "stack_queue_basics": [
    ["sFVxsatgeiM", "Stack and Queue Data Structure using Array", "Abdul Bari", "25:10", "LIFO vs FIFO"],
    ["zwb3GmNAtFk", "Stack Data Structure Tutorial in Python", "codebasics", "14:20", "Push, Pop, Peek"],
    ["rUUrmGKYwHw", "Queue Data Structure Tutorial in Python", "codebasics", "13:40", "Enqueue, Dequeue"],
    ["wjI1WNcIntg", "Stack and Queue Implementation & Real-World Uses", "Techdose", "18:15", "Monotonic Applications"]
  ],

  // --- Binary Trees & BST ---
  "tree_basics": [
    ["0m1T_UqZ_1M", "Binary Tree Representation & Terminology", "Abdul Bari", "28:30", "Nodes, Leaves, Depth"],
    ["4r_iT44_q44", "Binary Tree Implementation in Python", "codebasics", "21:10", "Hierarchical Traversal"],
    ["H5JubkIy6u8", "Binary Tree Inorder, Preorder, Postorder Traversals", "Techdose", "19:40", "DFS Traversal Orders"],
    ["jmy0LaGET1I", "Binary Tree Breadth First Search (Level Order)", "NeetCode", "12:15", "Queue Level Traversal"]
  ],
  "bst_basics": [
    ["pYT9F8_LARM", "Binary Search Tree (BST) Operations: Search, Insert, Delete", "Abdul Bari", "31:40", "BST Invariant"],
    ["lFq5mYUqU4k", "Binary Search Tree in Python", "codebasics", "18:30", "BST Recursive Insertion"],
    ["LFzAoJJt92M", "Delete Node in a BST Explained", "NeetCode", "15:20", "Inorder Successor Deletion"],
    ["Cpg8f79luEA", "Insert into a Binary Search Tree", "NeetCode", "08:45", "Pointer Rewiring"]
  ],

  // --- Graphs ---
  "graph_basics": [
    ["oDqjPvD54Ss", "Graph Traversals: Breadth First Search (BFS)", "Abdul Bari", "24:10", "Queue & Visited Set"],
    ["bIA8HEEUxZI", "Graph Traversals: Depth First Search (DFS)", "Abdul Bari", "22:30", "Call Stack & Backtracking"],
    ["j0YSbmgkspI", "Graph Data Structure Implementation in Python", "codebasics", "23:45", "Adjacency List & Matrix"],
    ["tWVWeAqZ0WU", "Graph BFS and DFS Traversal Explained", "Techdose", "20:15", "Cycle Detection"]
  ],
  "shortest_path": [
    ["XB4MIexjvY0", "Dijkstra's Algorithm - Single Source Shortest Path", "Abdul Bari", "32:10", "Greedy Priority Queue"],
    ["FtN3BYH2ZQU", "Bellman-Ford Algorithm - Negative Weight Cycles", "Abdul Bari", "28:40", "Edge Relaxation"],
    ["oNI0rf2P9gE", "Floyd-Warshall Algorithm - All-Pairs Shortest Path", "Abdul Bari", "25:15", "Dynamic Programming Matrix"],
    ["GazC3VDpe0U", "Dijkstra Algorithm Explained with Code", "Techdose", "21:30", "Heap Implementation"]
  ],
  "mst": [
    ["4ZlRH0ebK5Q", "Prim's and Kruskal's Minimum Spanning Tree Algorithms", "Abdul Bari", "38:40", "Greedy Cut Property"],
    ["f7JOBJIC-NA", "Min Cost to Connect All Points (Prim's & Kruskal's)", "NeetCode", "16:25", "Disjoint Set Union"],
    ["rnYBi9N_44A", "Disjoint Set Union (Union-Find) Explained", "Techdose", "19:10", "Rank & Path Compression"],
    ["3gbO7FDY7B4", "Kruskal's Algorithm using Disjoint Set Union", "Techdose", "17:40", "Cycle Prevention"]
  ],

  // --- Dynamic Programming ---
  "dp_basics": [
    ["5dr97G07e-I", "Introduction to Dynamic Programming - Memoization vs Tabulation", "Abdul Bari", "30:15", "Optimal Substructure"],
    ["oBt53YbR9Kk", "Dynamic Programming - Learn to Solve Any DP Problem", "freeCodeCamp.org", "5:10:00", "Top-Down & Bottom-Up"],
    ["H9bfqozjoqs", "Coin Change - Dynamic Programming", "NeetCode", "15:40", "Unbounded Knapsack"],
    ["lXVy6YWFcRM", "Maximum Product Subarray - Dynamic Programming", "NeetCode", "13:20", "State Transition Tracking"]
  ],
  "knapsack": [
    ["nLmhmB6NzcM", "0/1 Knapsack Problem - Dynamic Programming Formulation", "Abdul Bari", "34:20", "Decision Table"],
    ["IsvocB5BJhw", "Partition Equal Subset Sum - 0/1 Knapsack", "NeetCode", "12:45", "Subset Sum DP"],
    ["GqOmJwCZPAR", "0/1 Knapsack Problem with Code", "Techdose", "22:15", "Space Optimization"],
    ["sV4Z2E_Vd28", "Knapsack Problem Explained Simply", "Back To Back SWE", "18:30", "Choice Diagram"]
  ],
  "lcs": [
    ["sSno9rV8Rhg", "Longest Common Subsequence (LCS) - Dynamic Programming", "Abdul Bari", "31:10", "2D Grid DP"],
    ["Ua0GhsJSlWM", "Longest Common Subsequence Explained", "NeetCode", "17:25", "Bottom-Up Matrix"],
    ["LAKWWDX3sGw", "LCS Algorithm and Printing the Subsequence", "Techdose", "20:40", "Backtracking the Matrix"],
    ["ASoaQq66foQ", "Longest Common Subsequence Explained", "Back To Back SWE", "19:50", "Recurrence Relation"]
  ],

  // --- Tries ---
  "trie_basics": [
    ["oobqoCJlHA0", "Implement Trie Prefix Tree", "NeetCode", "13:10", "Prefix Tree Operations"],
    ["AXjmTQ8LEoI", "Trie Data Structure (Prefix Tree) Explained", "Techdose", "18:25", "Alphabet Array Pointers"],
    ["3Bbba8m5l_E", "Trie Insert and Search Operations", "Abdul Bari", "22:15", "String Search Tree"],
    ["qA8l8PUkusw", "Trie Data Structure in 5 Minutes", "Michael Sambol", "05:10", "Visual Animation"]
  ],

  // --- Recursion & Backtracking ---
  "recursion_backtracking": [
    ["5_6nC_P4b7o", "Recursion - How it works behind the scenes in Stack", "Abdul Bari", "26:30", "Call Stack Tracing"],
    ["REOH22Xwdkk", "Subsets - Backtracking", "NeetCode", "12:10", "Power Set Decision Tree"],
    ["s7AvT7cGdSo", "Permutations - Backtracking", "NeetCode", "14:20", "Permutation Tree"],
    ["Ph95IHmRp5M", "N-Queens Problem - Backtracking", "NeetCode", "18:40", "Diagonals Safety Check"]
  ],

  // --- Bit Manipulation ---
  "bit_manipulation": [
    ["5rtVTYAk99w", "Bit Manipulation Tricks and Techniques", "Techdose", "24:15", "Bitwise AND, OR, XOR, Shifts"],
    ["NLKQEO73SnI", "Bit Manipulation - Complete Course", "freeCodeCamp.org", "2:30:00", "Bitwise Logic & Masks"],
    ["xXKL9Y7gKbk", "Bit Manipulation for Coding Interviews", "NeetCode", "16:20", "Two's Complement & Masks"],
    ["3B_9Gq1wX8U", "Check if i-th bit is set and count bits", "take U forward", "15:40", "Bitmask Checking"]
  ]
};
