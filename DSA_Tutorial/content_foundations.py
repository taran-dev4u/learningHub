# Foundations pages — original tutorial content (v1 depth; deepened per MASTER_PROMPT sessions).

PAGES = [
# ============================================================ F01
{'id': 'f01-complexity', 'short': 'Complexity', 'title': 'F1 · Big-O: How We Measure “Fast”',
 'blurb': 'Time & space complexity from zero — the language every other page speaks.',
 'body': '''
<h2>The problem it solves</h2>
<p>“My code works” isn't enough — will it still work when the input has a million items? Big-O is how we predict that <em>without running the code</em>: it describes how work grows as input size <code>n</code> grows, ignoring constant factors and hardware.</p>

<h2>The growth ladder</h2>
<table>
<tr><th>Class</th><th>Name</th><th>n = 1,000,000 →</th><th>Typical source</th></tr>
<tr><td>O(1)</td><td>constant</td><td>1 step</td><td>hash lookup, array index, push/pop</td></tr>
<tr><td>O(log n)</td><td>logarithmic</td><td>~20 steps</td><td>binary search, balanced tree op, heap push/pop</td></tr>
<tr><td>O(n)</td><td>linear</td><td>10⁶</td><td>one pass over the data</td></tr>
<tr><td>O(n log n)</td><td>linearithmic</td><td>~2·10⁷</td><td>good sorting, n × heap ops</td></tr>
<tr><td>O(n²)</td><td>quadratic</td><td>10¹² — too slow</td><td>nested loops over the same data</td></tr>
<tr><td>O(2ⁿ)</td><td>exponential</td><td>astronomical</td><td>trying all subsets</td></tr>
<tr><td>O(n!)</td><td>factorial</td><td>worse</td><td>trying all orderings</td></tr>
</table>
<div class="insight"><strong>💡 Rule of thumb:</strong> a judge runs roughly 10⁷–10⁸ simple operations per second. n ≤ 10⁶ → you need O(n) or O(n log n). n ≤ 10³ → O(n²) is fine. n ≤ 20 → exponential/backtracking is intended.</div>

<h2>How to read code for its complexity</h2>
<pre><code>for x in nums:            # n iterations
    for y in nums:        #   × n iterations  → O(n²)
        ...

for x in nums:            # n iterations
    heapq.heappush(h, x)  #   × O(log n)      → O(n log n)

while lo < hi:            # halves the range each time → O(log n)
    mid = (lo + hi) // 2</code></pre>
<p>Rules: sequential blocks <strong>add</strong> (keep the biggest); nested blocks <strong>multiply</strong>; halving each step is log; drop constants (O(2n) = O(n)) and smaller terms (O(n² + n) = O(n²)).</p>

<h2>Space complexity</h2>
<p>Same idea, but for extra memory: an O(n) hash map, an O(h) recursion stack (h = tree height), O(1) for a few variables. The input itself usually doesn't count. Note: recursion always costs stack space — a DFS on a chain of n nodes is O(n) space even with no arrays.</p>

<h2>Amortized time</h2>
<p><code>list.append</code> occasionally copies the whole array to grow it (O(n) that once), but averaged over many appends it's O(1). That average-over-a-sequence cost is called <strong>amortized</strong>.</p>

<h2>Pitfalls</h2>
<ul>
<li>Big-O is worst case unless stated. Hash ops are O(1) <em>average</em>, O(n) pathological worst.</li>
<li>Two sequential loops are O(n), not O(n²) — nesting is what multiplies.</li>
<li>String concat in a loop and <code>list.pop(0)</code> are hidden O(n)s inside your loop.</li>
<li>Slicing (<code>a[i:j]</code>) copies — a "one-liner" can still be O(n).</li>
</ul>
'''},

# ============================================================ F02
{'id': 'f02-arrays-strings', 'short': 'Arrays & Strings', 'title': 'F2 · Arrays & Strings: Contiguous Memory',
 'blurb': 'Why index access is O(1), why inserting at the front is O(n), and the core techniques.',
 'body': '''
<h2>The problem it solves</h2>
<p>You need to store many items and jump straight to the i-th one. An array puts items side-by-side in memory, so the address of item i is just <code>start + i × item_size</code> — one multiplication, O(1), regardless of size.</p>

<h2>Visual</h2>
<pre class="viz">index:    0     1     2     3     4
        ┌─────┬─────┬─────┬─────┬─────┐
value:  │ 10  │ 20  │ 30  │ 40  │ 50  │   contiguous block
        └─────┴─────┴─────┴─────┴─────┘
insert 15 at index 1  →  20,30,40,50 ALL shift right → O(n)</code></pre>

<h2>Cost model (Python list = dynamic array)</h2>
<p>Access/assign O(1) · append/pop at end O(1) amortized · insert/delete anywhere else O(n) (shifting) · search unsorted O(n). Strings are immutable character arrays: same O(1) access, but every "modification" builds a new string.</p>

<h2>The three core array techniques (preview of patterns)</h2>
<ul>
<li><strong>Two pointers</strong> — two indices moving by rules; turns many O(n²) pair-scans into O(n). (Pattern P1)</li>
<li><strong>Sliding window</strong> — maintain a moving subarray and update its state incrementally. (Pattern P5)</li>
<li><strong>Prefix sums</strong> — precompute running totals once, answer any range-sum in O(1). (Pattern P17)</li>
</ul>
<pre><code># prefix sums in 3 lines
prefix = [0]
for x in nums: prefix.append(prefix[-1] + x)
# sum of nums[i..j] == prefix[j+1] - prefix[i]</code></pre>

<h2>In-place modification</h2>
<p>Many problems demand O(1) extra space. The trick is almost always the <strong>write-pointer</strong>: one pointer reads every element, another marks where the next "kept" element goes.</p>
<pre><code>write = 0
for read in range(len(nums)):
    if keep(nums[read]):
        nums[write] = nums[read]
        write += 1          # everything before write is the answer so far</code></pre>

<h2>Edge cases to always test</h2>
<ul><li>Empty array, single element</li><li>All duplicates</li><li>Already sorted / reverse sorted</li><li>Negative numbers and zeros</li><li>k larger than len (rotation problems: use <code>k %= n</code>)</li></ul>
'''},

# ============================================================ F03
{'id': 'f03-hashing', 'short': 'Hashing', 'title': 'F3 · Hashing: How dict and set Are O(1)',
 'blurb': 'Hash functions, buckets, collisions — and why "have I seen this?" is a constant-time question.',
 'body': '''
<h2>The problem it solves</h2>
<p>Searching a list is O(n). Hashing makes lookup O(1) by <em>computing where a value lives</em> instead of searching for it.</p>

<h2>Internal working</h2>
<p>A hash table is an array of <strong>buckets</strong>. A <strong>hash function</strong> turns any key into a number; <code>hash(key) % table_size</code> picks the bucket. Store the key (and value) there; to look up, hash again and jump straight to that bucket.</p>
<pre class="viz">hash("cat") = 738  →  738 % 8 = 2
buckets:  [0]      [1]      [2]────────┐  [3] ...
                            │"cat": 3  │
                            └──────────┘</code></pre>
<p><strong>Collisions</strong> — two keys landing in one bucket — are inevitable. Python resolves them by probing other slots (open addressing); when the table gets ~2/3 full it <strong>rehashes</strong> into a bigger array. That's why ops are O(1) <em>average</em>, and why only immutable (stable-hash) types can be keys.</p>

<h2>The three interview superpowers</h2>
<table>
<tr><th>Move</th><th>Idiom</th><th>Replaces</th></tr>
<tr><td>Seen before?</td><td><code>if x in seen</code> (set)</td><td>O(n) scan → O(1)</td></tr>
<tr><td>Complement lookup</td><td><code>if target - x in index_of</code></td><td>O(n²) Two Sum → O(n)</td></tr>
<tr><td>Group by signature</td><td><code>groups[key(x)].append(x)</code></td><td>O(n²) pairwise compare → O(n·k)</td></tr>
</table>
<pre><code># Two Sum — THE canonical hash trade: memory for speed
index_of = {}
for i, x in enumerate(nums):
    if target - x in index_of:       # O(1) average
        return [index_of[target - x], i]
    index_of[x] = i</code></pre>

<h2>Choosing a signature key</h2>
<p>Grouping problems reduce to "what makes two items equivalent?": anagrams → <code>tuple(sorted(word))</code> or 26-count tuple; shifted strings → tuple of letter gaps; grid diagonals → <code>r - c</code>. If you can name the invariant, a dict groups it in one pass.</p>

<h2>Pitfalls</h2>
<ul>
<li>Lists can't be keys (mutable) — convert to <code>tuple</code> first.</li>
<li>Hash map costs O(n) memory — mention the trade-off aloud in interviews.</li>
<li>Worst case O(n) per op exists in theory; say "average O(1)".</li>
<li>Dict preserves insertion order (3.7+) but a set does not guarantee any order.</li>
</ul>
'''},

# ============================================================ F04
{'id': 'f04-linked-lists', 'short': 'Linked Lists', 'title': 'F4 · Linked Lists: Chains of Nodes',
 'blurb': 'Nodes and pointers, the dummy-head trick, and the fast/slow pointer technique.',
 'body': '''
<h2>The problem it solves</h2>
<p>Arrays pay O(n) to insert/delete in the middle (shifting). A linked list stores each item in its own <strong>node</strong> with a pointer to the next node — rewiring two pointers inserts or deletes in O(1)… <em>if you're already standing there</em>. The trade: no O(1) index access; reaching position i costs O(i).</p>

<h2>Visual</h2>
<pre class="viz">head → [3 | •] → [7 | •] → [1 | •] → None

delete 7:  just rewire —   [3 | •] ─────────→ [1 | •] → None
insert 5 after 3:          [3 | •] → [5 | •] → [7 | •] → ...</code></pre>

<pre><code>class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next</code></pre>

<h2>Cost model</h2>
<p>insert/delete at a known node O(1) · access i-th O(n) · search O(n) · no cache friendliness (nodes scattered in memory). Use when you splice a lot and never index; otherwise arrays usually win.</p>

<h2>The three tools that solve 90% of list problems</h2>
<p><strong>1. Dummy head</strong> — a fake node before the real head so "delete the first node" isn't a special case:</p>
<pre><code>dummy = ListNode(0, head)
prev, cur = dummy, head
# ...delete: prev.next = cur.next
return dummy.next</code></pre>
<p><strong>2. Fast &amp; slow pointers</strong> — fast moves 2, slow moves 1. When fast hits the end, slow is at the middle; if there's a cycle, they must meet (Floyd's algorithm).</p>
<pre><code>slow = fast = head
while fast and fast.next:
    slow, fast = slow.next, fast.next.next
# slow == middle; add "if slow is fast: cycle!" inside for detection</code></pre>
<p><strong>3. In-place reversal</strong> — walk once, flipping each arrow:</p>
<pre><code>prev = None
while cur:
    cur.next, prev, cur = prev, cur, cur.next   # flip, advance
return prev    # new head</code></pre>
<pre class="viz">None ← 3   7 → 1        prev=3, cur=7
None ← 3 ← 7   1        prev=7, cur=1
None ← 3 ← 7 ← 1        prev=1, cur=None → done</code></pre>

<h2>Pitfalls</h2>
<ul>
<li>Losing the rest of the list: save <code>nxt = cur.next</code> <em>before</em> overwriting <code>cur.next</code>.</li>
<li>Null crashes: guard <code>while fast and fast.next</code> — order matters.</li>
<li>Off-by-one in "k-th from end": advance the lead pointer exactly k first, then move both.</li>
<li>Doubly-linked lists add a <code>prev</code> pointer — O(1) delete given the node; that's the engine of LRU Cache.</li>
</ul>
'''},

# ============================================================ F05
{'id': 'f05-stacks-queues', 'short': 'Stacks & Queues', 'title': 'F5 · Stacks & Queues: Order of Processing',
 'blurb': 'LIFO vs FIFO, implementations in Python, and where each shows up.',
 'body': '''
<h2>The problem they solve</h2>
<p>Often the algorithm's whole job is <em>processing things in the right order</em>. Two disciplines cover most needs: <strong>LIFO</strong> (last in, first out — a stack of plates) and <strong>FIFO</strong> (first in, first out — a checkout line).</p>

<h2>Stack — LIFO</h2>
<pre><code>stack = []
stack.append(x)     # push  O(1)
top = stack[-1]     # peek  O(1)
x = stack.pop()     # pop   O(1)
if not stack: ...   # empty check</code></pre>
<pre class="viz">push 1, push 2, push 3 →   │ 3 │ ← pop returns 3 first
                           │ 2 │
                           │ 1 │
                           └───┘</code></pre>
<p><strong>Where stacks appear:</strong> matching brackets (open → push, close → must match pop); undo history; DFS (explicit stack = recursion without recursion); <em>monotonic stacks</em> for "next greater element" (Pattern P6); expression evaluation (operators wait on a stack).</p>

<h2>Queue — FIFO</h2>
<pre><code>from collections import deque
q = deque()
q.append(x)         # enqueue O(1)
x = q.popleft()     # dequeue O(1)  ← list.pop(0) is O(n): never use a list as a queue</code></pre>
<p><strong>Where queues appear:</strong> BFS (process nodes in discovery order — this is why BFS finds shortest paths in unweighted graphs); level-order tree traversal; task scheduling; sliding-window maximum uses a <em>deque</em> variant (monotonic deque).</p>

<h2>Stack vs Queue vs Deque</h2>
<table>
<tr><th></th><th>Stack</th><th>Queue</th><th>Deque</th></tr>
<tr><td>Order</td><td>LIFO</td><td>FIFO</td><td>both ends</td></tr>
<tr><td>Python</td><td><code>list</code></td><td><code>deque</code></td><td><code>deque</code></td></tr>
<tr><td>Signature use</td><td>matching, DFS, monotonic</td><td>BFS, levels</td><td>window max/min</td></tr>
<tr><td>All ops</td><td>O(1)</td><td>O(1)</td><td>O(1)</td></tr>
</table>

<h2>Mini dry run — Valid Parentheses "([])"</h2>
<pre class="viz">read (  → push        stack: (
read [  → push        stack: ( [
read ]  → pop ( == [? yes → ok   stack: (
read )  → pop ( == (? yes → ok   stack: empty
end: stack empty → VALID</code></pre>

<h2>Pitfalls</h2>
<ul>
<li>Peeking/popping an empty stack — always check <code>if stack:</code> first.</li>
<li>Using <code>list.pop(0)</code> for a queue — silently turns O(n) total into O(n²).</li>
<li>For "next greater" problems, store <em>indices</em> on the stack, not values — you usually need distances.</li>
</ul>
'''},

# ============================================================ F06
{'id': 'f06-recursion', 'short': 'Recursion', 'title': 'F6 · Recursion: Functions That Call Themselves',
 'blurb': 'The call stack, base cases, the recursion leap of faith, and memoization.',
 'body': '''
<h2>The problem it solves</h2>
<p>Some problems are naturally "a smaller copy of themselves": a directory contains directories; a tree node's subtrees are trees; "ways to climb n stairs" depends on "ways to climb n−1 and n−2". Recursion lets the code mirror that structure.</p>

<h2>The two non-negotiable parts</h2>
<pre><code>def factorial(n):
    if n <= 1:                 # 1. BASE CASE — where recursion stops
        return 1
    return n * factorial(n-1)  # 2. RECURSIVE CASE — smaller subproblem</code></pre>
<p>No base case (or a recursive case that doesn't shrink the problem) = infinite recursion = <code>RecursionError</code>.</p>

<h2>Internal working: the call stack</h2>
<pre class="viz">factorial(3)
│ 3 * factorial(2)
│     │ 2 * factorial(1)
│     │     │ return 1        ← base case hit, stack unwinds
│     │ return 2 * 1 = 2
│ return 3 * 2 = 6</code></pre>
<p>Each call gets its own frame (its own local variables) on the <strong>call stack</strong>. Depth d ⇒ O(d) memory. Python caps depth (~1000); deep inputs need <code>sys.setrecursionlimit</code> or an iterative rewrite with an explicit stack.</p>

<h2>The leap of faith</h2>
<div class="insight"><strong>💡 How to write recursion without melting your brain:</strong> assume the recursive call <em>already works</em> for the smaller input, and only ask: (1) what's the smallest case I can answer directly? (2) if the sub-answer is correct, how do I combine it into my answer? Trace one small example to trust it — never mentally simulate 10 levels.</div>

<h2>Recursion trees &amp; complexity</h2>
<p><code>fib(n)</code> calling <code>fib(n-1)</code> and <code>fib(n-2)</code> makes a binary tree of calls ⇒ O(2ⁿ). Count complexity as (number of nodes in the call tree) × (work per node). The same subproblems repeat — <strong>memoization</strong> caches them:</p>
<pre><code>from functools import lru_cache
@lru_cache(None)
def fib(n):
    return n if n < 2 else fib(n-1) + fib(n-2)   # now O(n)</code></pre>
<p>That one decorator is the bridge from recursion to <strong>dynamic programming</strong> (Pattern P12).</p>

<h2>Recursion vs iteration</h2>
<table>
<tr><th>Prefer recursion</th><th>Prefer iteration</th></tr>
<tr><td>trees, nested structures, backtracking, divide &amp; conquer</td><td>simple counting loops, very deep linear chains (linked lists!), hot paths</td></tr>
</table>

<h2>Pitfalls</h2>
<ul>
<li>Mutable default args (<code>def f(path=[])</code>) persist across calls — pass explicitly.</li>
<li>Forgetting to <code>return</code> the recursive result (computing it and dropping it).</li>
<li>Sharing state across branches unintentionally — in backtracking, undo (pop) after each choice.</li>
</ul>
'''},

# ============================================================ F07
{'id': 'f07-trees', 'short': 'Trees', 'title': 'F7 · Trees & BSTs: Hierarchies',
 'blurb': 'Terminology, the four traversals, BST ordering, and height vs balance.',
 'body': '''
<h2>The problem it solves</h2>
<p>Lists are flat; lots of data is hierarchical (file systems, org charts, HTML). A <strong>tree</strong> is nodes with parent→child links, no cycles, one <strong>root</strong>. A <strong>binary tree</strong> allows ≤2 children (left, right).</p>
<pre><code>class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right</code></pre>
<pre class="viz">        4          depth of 4 = 0 (root)
      /   \\        height of tree = 2
     2     6       leaves: 1, 3, 5, 7
    / \\   / \\
   1   3 5   7</code></pre>

<h2>The four traversals (know these cold)</h2>
<table>
<tr><th>Traversal</th><th>Order</th><th>On the tree above</th><th>Superpower</th></tr>
<tr><td>Preorder</td><td>node, left, right</td><td>4 2 1 3 6 5 7</td><td>copy/serialize a tree</td></tr>
<tr><td>Inorder</td><td>left, node, right</td><td>1 2 3 4 5 6 7</td><td><strong>sorted order in a BST</strong></td></tr>
<tr><td>Postorder</td><td>left, right, node</td><td>1 3 2 5 7 6 4</td><td>children first: delete, subtree sums</td></tr>
<tr><td>Level-order</td><td>top→bottom, left→right</td><td>4 · 2 6 · 1 3 5 7</td><td>anything "per level" (BFS + deque)</td></tr>
</table>
<pre><code>def inorder(node):                 # DFS, O(n) time, O(h) stack
    if not node: return
    inorder(node.left)
    visit(node)
    inorder(node.right)

from collections import deque      # BFS
q = deque([root])
while q:
    for _ in range(len(q)):        # one level per outer iteration
        node = q.popleft()
        if node.left:  q.append(node.left)
        if node.right: q.append(node.right)</code></pre>

<h2>Binary Search Tree (BST)</h2>
<p>Ordering rule at <em>every</em> node: everything left &lt; node &lt; everything right. Search/insert/delete walk one root→leaf path: <strong>O(h)</strong>. Balanced ⇒ h = log n ⇒ O(log n); a sorted-order insert degenerates into a linked list ⇒ h = n. Self-balancing trees (AVL/Red-Black) keep h = O(log n) — know they exist and the guarantee, not the rotations.</p>
<div class="warn"><strong>Classic trap (Validate BST):</strong> checking only <code>left.val &lt; node.val &lt; right.val</code> is not enough — a grandchild can violate a grand-parent's bound. Pass down (lo, hi) limits, or check that inorder output is strictly increasing.</div>

<h2>Recursion mindset for trees</h2>
<p>Almost every tree problem is: "answer for node = combine(answer for left subtree, answer for right subtree)", with base case <code>None → 0/True/None</code>. Example — height: <code>1 + max(h(left), h(right))</code>.</p>

<h2>Pitfalls</h2>
<ul><li>Depth counts from root down; height from leaves up — define which you mean.</li>
<li>O(h) space isn't O(log n) unless the tree is balanced — say "O(h), log n if balanced".</li>
<li>"Complete" (filled left-to-right — heaps) ≠ "full" (0 or 2 children) ≠ "perfect" (all leaves same depth).</li></ul>
'''},

# ============================================================ F08
{'id': 'f08-heaps', 'short': 'Heaps', 'title': 'F8 · Heaps: Always Know the Minimum',
 'blurb': 'The array-as-tree trick, sift up/down, heapify, and the top-k playbook.',
 'body': '''
<h2>The problem it solves</h2>
<p>You repeatedly need the smallest (or largest) item from a changing collection. Keeping it sorted costs O(n) per insert; a <strong>heap</strong> gives insert O(log n) and pop-min O(log n), peek O(1) — by maintaining much weaker order than "sorted".</p>

<h2>Internal working</h2>
<p>A <strong>min-heap</strong> is a complete binary tree where each node ≤ its children (heap property). Only parent-child order matters — siblings are unordered. Because it's complete, it lives in a plain array with index math (no pointers): children of i are <code>2i+1, 2i+2</code>; parent is <code>(i−1)//2</code>.</p>
<pre class="viz">array: [1, 3, 2, 7, 4]        1            push 0:  put at end, "sift up":
                            /   \\          swap with parent while smaller
                           3     2         pop min: move last to root,
                          / \\              "sift down": swap with smaller
                         7   4             child while bigger — O(log n) each</code></pre>
<p><code>heapq.heapify</code> builds a heap in <strong>O(n)</strong> (bottom-up sift-down — most nodes are near the leaves and barely move; the costs sum to O(n), not O(n log n)).</p>

<h2>Python API + max-heap workaround</h2>
<pre><code>import heapq
heapq.heappush(h, x); x = heapq.heappop(h); h[0]      # min-heap
heapq.heappush(h, -x); biggest = -h[0]                # "max-heap"
heapq.heappush(h, (dist, node))                       # tuple = priority + payload</code></pre>

<h2>The top-k playbook (memorize)</h2>
<div class="insight"><strong>💡 k largest → keep a MIN-heap of size k</strong> (pop the smallest whenever size &gt; k; survivors are the k largest). k smallest → max-heap of size k. Cost O(n log k) — better than sorting when k ≪ n.</div>
<pre><code>h = []
for x in nums:
    heapq.heappush(h, x)
    if len(h) > k: heapq.heappop(h)   # h now holds the k largest</code></pre>

<h2>Where heaps appear</h2>
<ul><li>Top-k / k-th largest (P7)</li><li>Merge k sorted lists (heap of current heads)</li><li>Dijkstra's shortest path (always expand the closest node)</li><li>Two heaps: median of a stream (max-heap of lower half + min-heap of upper half)</li><li>Scheduling: always take the soonest deadline / most frequent task</li></ul>

<h2>Heap vs sorted vs BST</h2>
<table>
<tr><th></th><th>Heap</th><th>Sorted list</th><th>Balanced BST</th></tr>
<tr><td>peek min</td><td>O(1)</td><td>O(1)</td><td>O(log n)</td></tr>
<tr><td>insert</td><td>O(log n)</td><td>O(n)</td><td>O(log n)</td></tr>
<tr><td>find arbitrary</td><td>O(n)</td><td>O(log n)</td><td>O(log n)</td></tr>
</table>

<h2>Pitfalls</h2>
<ul><li>A heap array is NOT sorted — only h[0] is guaranteed.</li>
<li>Tuple ties: <code>(priority, item)</code> crashes if priorities tie and items aren't comparable — add a counter: <code>(priority, i, item)</code>.</li>
<li>No efficient "remove arbitrary element" — use lazy deletion (mark dead, skip when popped).</li></ul>
'''},

# ============================================================ F09
{'id': 'f09-graphs', 'short': 'Graphs', 'title': 'F9 · Graphs: Networks of Relationships',
 'blurb': 'Representations, BFS vs DFS, and the visited-set discipline.',
 'body': '''
<h2>The problem it solves</h2>
<p>Trees only model hierarchies. Friendships, maps, dependencies, grids — anything where items connect freely — need a <strong>graph</strong>: nodes (vertices) + connections (edges). Directed or undirected, weighted or unweighted, possibly cyclic, possibly disconnected.</p>

<h2>Representation: adjacency list (the default)</h2>
<pre><code>from collections import defaultdict
graph = defaultdict(list)
for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)      # drop this line for a directed graph</code></pre>
<p>O(V+E) space; iterating a node's neighbors is O(degree). An adjacency <em>matrix</em> is O(V²) space with O(1) edge lookup — only worth it for dense graphs. <strong>Grids are graphs too</strong>: cell (r,c) has neighbors in 4 directions — no need to build an explicit adjacency list.</p>

<h2>BFS vs DFS — the two engines</h2>
<pre><code>from collections import deque        # BFS: explore by distance rings
def bfs(start):
    q, seen = deque([start]), {start}
    while q:
        node = q.popleft()
        for nb in graph[node]:
            if nb not in seen:
                seen.add(nb)         # mark when ENQUEUED, not when popped
                q.append(nb)

def dfs(node, seen):                 # DFS: dive deep, backtrack
    for nb in graph[node]:
        if nb not in seen:
            seen.add(nb)
            dfs(nb, seen)</code></pre>
<table>
<tr><th></th><th>BFS</th><th>DFS</th></tr>
<tr><td>Structure</td><td>queue</td><td>recursion / stack</td></tr>
<tr><td>Explores</td><td>nearest first</td><td>one branch fully</td></tr>
<tr><td>Guarantees</td><td><strong>shortest path (unweighted)</strong></td><td>—</td></tr>
<tr><td>Best for</td><td>min steps, levels, nearest X</td><td>connectivity, islands, cycles, topological sort, backtracking</td></tr>
<tr><td>Complexity</td><td colspan="2">both O(V+E) time, O(V) space</td></tr>
</table>
<div class="warn"><strong>The #1 graph bug:</strong> forgetting the visited set (infinite loops on cycles) or marking visited at pop-time instead of enqueue-time in BFS (nodes enter the queue twice — wrong distances and blow-ups).</div>

<h2>The five recurring graph jobs</h2>
<ul>
<li><strong>Connected components / islands</strong> — loop all nodes, DFS/BFS from each unvisited one, count starts.</li>
<li><strong>Shortest path</strong> — unweighted: BFS. Weighted non-negative: Dijkstra (heap). Negative edges: Bellman-Ford.</li>
<li><strong>Cycle detection</strong> — undirected: DFS seeing a visited non-parent. Directed: three colors (white/gray/black); a gray→gray edge is a cycle.</li>
<li><strong>Topological sort</strong> — order a DAG so edges point forward: Kahn's algorithm (repeatedly remove indegree-0 nodes). Course Schedule is this.</li>
<li><strong>Union-Find</strong> — near-O(1) "same group?" queries under merging (F11).</li>
</ul>

<h2>Pitfalls</h2>
<ul><li>Disconnected graphs: one traversal from node 0 doesn't see everything — loop over all starts.</li>
<li>Grid DFS recursion can exceed Python's depth limit on big grids — use an explicit stack.</li>
<li>Don't mutate the input grid as your visited-marker unless allowed (though it's a classic O(1)-space trick — say it aloud).</li></ul>
'''},

# ============================================================ F10
{'id': 'f10-sorting', 'short': 'Sorting', 'title': 'F10 · Sorting: The Algorithms & When They Matter',
 'blurb': 'Merge sort, quicksort/quickselect, counting sort — and what interviews actually test.',
 'body': '''
<h2>What interviews actually test</h2>
<p>You'll rarely implement sorting from scratch — you'll be asked (1) to <em>explain</em> the classic algorithms and their trade-offs, (2) to use sorting as step 1 of a greedy/intervals solution, and (3) to know <strong>quickselect</strong> and <strong>counting sort</strong> for beating O(n log n) in special cases.</p>

<h2>The landscape</h2>
<table>
<tr><th>Algorithm</th><th>Time (avg)</th><th>Worst</th><th>Space</th><th>Stable?</th><th>One-line idea</th></tr>
<tr><td>Bubble/Insertion</td><td>O(n²)</td><td>O(n²)</td><td>O(1)</td><td>yes</td><td>swap neighbors / insert into sorted prefix (great when nearly sorted: O(n))</td></tr>
<tr><td>Merge sort</td><td>O(n log n)</td><td>O(n log n)</td><td>O(n)</td><td>yes</td><td>halve, sort halves, merge two sorted lists</td></tr>
<tr><td>Quicksort</td><td>O(n log n)</td><td>O(n²)</td><td>O(log n)</td><td>no</td><td>partition around a pivot, recurse on both sides</td></tr>
<tr><td>Heap sort</td><td>O(n log n)</td><td>O(n log n)</td><td>O(1)</td><td>no</td><td>heapify, pop n times</td></tr>
<tr><td>Counting sort</td><td>O(n+k)</td><td>O(n+k)</td><td>O(k)</td><td>yes</td><td>count occurrences of each of k possible values</td></tr>
<tr><td>Python's sort (Timsort)</td><td>O(n log n)</td><td>O(n log n)</td><td>O(n)</td><td>yes</td><td>merge sort + insertion-sort runs; exploits existing order</td></tr>
</table>

<h2>Merge — the step that powers everything</h2>
<pre><code>def merge(a, b):                  # two sorted lists → one sorted list, O(n)
    i = j = 0; out = []
    while i < len(a) and j < len(b):
        if a[i] <= b[j]: out.append(a[i]); i += 1
        else:            out.append(b[j]); j += 1
    return out + a[i:] + b[j:]    # one side has leftovers</code></pre>
<p>This two-pointer merge reappears in "merge sorted arrays", "merge k lists" (with a heap), and counting inversions.</p>

<h2>Partition &amp; quickselect — k-th element in O(n) average</h2>
<pre><code>import random
def quickselect(nums, k):               # k-th smallest, 0-indexed
    pivot = random.choice(nums)
    lo  = [x for x in nums if x < pivot]
    eq  = [x for x in nums if x == pivot]
    hi  = [x for x in nums if x > pivot]
    if k < len(lo):            return quickselect(lo, k)
    if k < len(lo) + len(eq):  return pivot
    return quickselect(hi, k - len(lo) - len(eq))</code></pre>
<p>Unlike quicksort, you recurse into <em>one</em> side: n + n/2 + n/4 + … = O(n) average. The answer to "k-th largest without sorting".</p>

<h2>Beating n log n</h2>
<p>Comparison sorts can't beat O(n log n) (information-theoretic bound). But if values live in a small known range — digits 0-9, letters a-z, ages 0-120 — <strong>counting sort</strong> is O(n+k). Sort Colors (3 values) is the famous special case, solvable one-pass with the Dutch National Flag three-pointer.</p>

<h2>Stability — why it matters</h2>
<p>Stable = equal keys keep their input order. Python's sort is stable, so you can sort by a secondary key first, then the primary — or just use a tuple key. Radix sort is repeated stable counting sort per digit.</p>

<h2>Pitfalls</h2>
<ul><li><code>a.sort()</code> returns <code>None</code> — don't write <code>a = a.sort()</code>.</li>
<li>Sorting costs O(n log n) up front — check whether a heap (O(n log k)) or one pass (counting) is cheaper for the actual question.</li>
<li>Custom comparators: prefer tuple keys; <code>functools.cmp_to_key</code> exists for genuine pairwise rules (e.g. Largest Number: compare <code>a+b</code> vs <code>b+a</code>).</li></ul>
'''},

# ============================================================ F11
{'id': 'f11-tries-dsu', 'short': 'Tries & Union-Find', 'title': 'F11 · Tries & Union-Find: Two Specialists',
 'blurb': 'Prefix trees for string sets; disjoint sets for dynamic connectivity.',
 'body': '''
<h2>Trie (prefix tree) — a dictionary organized by prefix</h2>
<p><strong>Problem it solves:</strong> a hash set answers "is <code>word</code> in the set?" but not "does anything start with <code>pre</code>?" A trie stores words as root→leaf paths where each edge is a letter, so all words sharing a prefix share a path — prefix queries cost O(len(prefix)), independent of how many words are stored.</p>
<pre class="viz">insert "car", "cat", "do":     root
                              /    \\
                             c      d
                             │      │
                             a      o ●        ● = end-of-word flag
                            / \\
                           r ●  t ●</code></pre>
<pre><code>class Trie:
    def __init__(self):
        self.root = {}                      # node = dict: letter → child node
    def insert(self, word):                 # O(len(word))
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node['$'] = True                    # end-of-word marker
    def search(self, word):                 # O(len(word))
        node = self._walk(word)
        return node is not None and '$' in node
    def starts_with(self, prefix):          # O(len(prefix))
        return self._walk(prefix) is not None
    def _walk(self, s):
        node = self.root
        for ch in s:
            if ch not in node: return None
            node = node[ch]
        return node</code></pre>
<p><strong>Use for:</strong> autocomplete, word search on boards (prune whole branches the moment a prefix doesn't exist — the Word Search II trick), wildcard matching (branch on '.'), XOR problems (bit-trie). Trade-off: much more memory than a set.</p>

<h2>Union-Find (Disjoint Set Union) — dynamic "same group?"</h2>
<p><strong>Problem it solves:</strong> edges keep arriving and you must repeatedly answer "are u and v connected?" Re-running BFS per query is O(V+E) each. DSU answers in near-O(1) by giving each group a representative <em>root</em>.</p>
<pre><code>parent = list(range(n))
rank   = [0] * n

def find(x):                         # walk to the root...
    while parent[x] != x:
        parent[x] = parent[parent[x]]   # path compression: point to grandparent
        x = parent[x]
    return x

def union(a, b):                     # returns False if already connected
    ra, rb = find(a), find(b)
    if ra == rb: return False
    if rank[ra] < rank[rb]: ra, rb = rb, ra
    parent[rb] = ra                  # attach shorter tree under taller (union by rank)
    rank[ra] += rank[ra] == rank[rb]
    return True</code></pre>
<p>Path compression + union by rank make each op effectively O(α(n)) ≈ O(1) — α is the inverse Ackermann function, ≤ 5 for any realistic n.</p>
<p><strong>Use for:</strong> counting components as edges arrive, cycle detection in undirected graphs (union returns False ⇒ cycle), Kruskal's MST, accounts-merge style grouping, "redundant connection".</p>

<h2>When which?</h2>
<table>
<tr><th>Question smells like…</th><th>Tool</th></tr>
<tr><td>prefixes, autocomplete, many string lookups</td><td>Trie</td></tr>
<tr><td>merging groups, connectivity under additions</td><td>Union-Find</td></tr>
<tr><td>connectivity of a FIXED graph, one-shot</td><td>plain BFS/DFS</td></tr>
</table>
'''},

# ============================================================ F12
{'id': 'f12-advanced-ds', 'short': 'Advanced Structures', 'title': 'F12 · Segment Trees, Fenwick Trees & Friends',
 'blurb': 'Range queries with point updates — and a map of the rarer structures.',
 'body': '''
<h2>The problem they solve</h2>
<p>Prefix sums answer range-sum queries in O(1) — but one array update forces rebuilding the prefixes in O(n). When you need <strong>both</strong> updates and range queries, interleaved, segment/Fenwick trees give O(log n) for each.</p>
<table>
<tr><th></th><th>update</th><th>range query</th><th>notes</th></tr>
<tr><td>plain array</td><td>O(1)</td><td>O(n)</td><td>fine if queries are rare</td></tr>
<tr><td>prefix sums</td><td>O(n)</td><td>O(1)</td><td>fine if updates are rare</td></tr>
<tr><td><strong>Fenwick / Segment tree</strong></td><td>O(log n)</td><td>O(log n)</td><td>fine when both are frequent</td></tr>
</table>

<h2>Segment tree — intervals halved recursively</h2>
<p>Each node covers a range and stores an aggregate (sum/min/max) of it; the root covers [0, n), children split the range in half. A query decomposes any [l, r) into O(log n) node ranges; an update fixes one leaf and its O(log n) ancestors. Works for <em>any associative operation</em> — that's its edge over Fenwick.</p>
<pre class="viz">              [0,8) sum=36
             /            \\
       [0,4)=10          [4,8)=26
       /     \\            /     \\
   [0,2)=3  [2,4)=7  [4,6)=11  [6,8)=15   ... leaves = single elements</code></pre>

<h2>Fenwick tree (BIT) — prefix sums, updatable</h2>
<p>A compressed cousin: an array where index i is responsible for a block whose size is i's lowest set bit (<code>i &amp; -i</code>). Shorter code, half the memory; supports prefix aggregates of invertible ops (sum yes, min no).</p>
<pre><code>tree = [0] * (n + 1)                  # 1-indexed
def update(i, delta):                 # add delta at position i
    while i <= n:
        tree[i] += delta
        i += i & (-i)                 # jump to next responsible block
def prefix(i):                        # sum of a[1..i]
    s = 0
    while i > 0:
        s += tree[i]
        i -= i & (-i)
    return s
# range sum l..r = prefix(r) - prefix(l-1)</code></pre>
<p>Classic uses: count of smaller elements to the right, range-sum with updates, counting inversions.</p>

<h2>Map of rarer structures (recognize, don't memorize)</h2>
<ul>
<li><strong>Monotonic stack/deque</strong> — next-greater-element, window max. (Really a technique — P6.)</li>
<li><strong>LRU structure</strong> — dict + doubly-linked list: O(1) get/put with eviction order. (P15/P18.)</li>
<li><strong>Intervals + sweep line</strong> — sort events, +1/−1 counter: meeting rooms, skyline. (P21.)</li>
<li><strong>Ordered multiset via <code>bisect</code>+list</strong> — Python's stand-in for a balanced BST; O(n) insert but often passes.</li>
<li><strong>Suffix arrays / KMP / Rabin-Karp</strong> — heavy string machinery. (P29.)</li>
</ul>

<div class="tip"><strong>Interview reality check:</strong> segment/Fenwick trees appear mainly in Hard problems. Recognize the trigger — "updates AND range queries, both frequent" — and know the API + complexity; fluent implementation is a bonus, not table stakes. Foundations complete → on to the patterns!</div>
'''},
]
