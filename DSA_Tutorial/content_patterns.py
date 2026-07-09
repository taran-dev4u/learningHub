# Pattern page content, keyed by the exact pattern title from curriculum.json.
# Fields: slug, short, intuition(html), aha(html), signals[list of html], template(code str),
#         template_notes(html), complexity(html), mistakes[list of html]

PATTERNS = {

'Two Pointer Patterns': {
 'slug': 'two-pointers', 'short': 'Two indices moving by rules turn O(n²) pair scans into O(n).',
 'intuition': '<p>Many problems ask about <em>pairs</em> or <em>positions</em> in an array. Brute force tries every pair — O(n²). Two pointers replaces "try everything" with two indices that move by a rule, and the rule guarantees you never need to look back. Each pointer moves at most n steps, so the whole thing is O(n).</p>',
 'aha': 'On a <strong>sorted</strong> array, comparing <code>nums[left] + nums[right]</code> to the target tells you which pointer is safe to move: sum too small → only moving <code>left</code> up can help; too big → only moving <code>right</code> down can. Every comparison permanently eliminates a whole row of pair-candidates.',
 'signals': ['sorted array (or you may sort it) + find a pair/triplet',
             'palindrome or symmetric comparison (compare ends)',
             'do it <strong>in place</strong> with O(1) extra space (read/write pointers)',
             'linked list: middle, cycle, k-th from end (fast &amp; slow)',
             '"remove/keep elements" while preserving relative order'],
 'template': '''# Converging (opposite ends)
left, right = 0, len(nums) - 1
while left < right:
    cur = nums[left] + nums[right]      # ← state you compare
    if cur == target:
        return [left, right]
    elif cur < target:
        left += 1                        # too small: need a bigger left
    else:
        right -= 1                       # too big: need a smaller right

# Read/write (in-place filtering)
write = 0
for read in range(len(nums)):
    if keep(nums[read]):                 # ← condition changes per problem
        nums[write] = nums[read]
        write += 1''',
 'template_notes': 'Two shapes cover most problems: <strong>converging</strong> (ends → middle) and <strong>read/write</strong> (both start at 0, write lags). The third shape, <strong>fast &amp; slow</strong>, lives on linked lists: fast moves two steps per slow step.',
 'complexity': 'O(n) time — each pointer crosses the array once. O(1) space — just indices. If you must sort first, that dominates: O(n log n).',
 'mistakes': ['Using converging pointers on an <em>unsorted</em> array — the elimination logic only holds when sorted.',
              'Off-by-one: <code>while left &lt; right</code> vs <code>&lt;=</code> — decide whether pointers may meet.',
              'Forgetting to skip duplicates in 3Sum-style problems (advance past equal values).',
              'In fast/slow: writing <code>while fast.next and fast</code> — the null-check order crashes.']},

'Array/Matrix Manipulation Patterns': {
 'slug': 'array-matrix', 'short': 'In-place transforms: rotation, spiral walks, marking tricks.',
 'intuition': '<p>These problems hand you a grid or array and demand a transformation — rotate it, traverse it in a weird order, zero things out — usually <strong>in place</strong>. The skill is decomposing a scary transformation into simple safe steps, and using the structure itself (signs, first row/column) as scratch space.</p>',
 'aha': 'Hard transforms are compositions of easy ones. Rotating a matrix 90° clockwise = <strong>transpose, then reverse each row</strong> — two loops anyone can write, no index gymnastics. Similarly, rotating an array = three reversals.',
 'signals': ['"rotate / transpose / flip" a matrix or array',
             '"in place" / "O(1) extra space" on a grid problem',
             'traverse in an unusual order (spiral, diagonal, zigzag)',
             'mark/erase cells based on other cells (use the cells themselves as flags)'],
 'template': '''# Rotate matrix 90° clockwise, in place
n = len(matrix)
for r in range(n):                     # 1) transpose (swap across diagonal)
    for c in range(r + 1, n):
        matrix[r][c], matrix[c][r] = matrix[c][r], matrix[r][c]
for row in matrix:                     # 2) reverse each row
    row.reverse()

# Spiral walk: shrink four boundaries
top, bottom, left, right = 0, rows - 1, 0, cols - 1
while top <= bottom and left <= right:
    ...walk top row, right col, bottom row, left col...
    top += 1; bottom -= 1; left += 1; right -= 1''',
 'template_notes': 'For spiral/boundary walks, re-check <code>top &lt;= bottom</code> / <code>left &lt;= right</code> before the bottom row and left column — a single remaining row otherwise gets walked twice.',
 'complexity': 'Almost always O(m·n) time — every cell touched a constant number of times — and O(1) extra space; that constraint is the whole point.',
 'mistakes': ['Rotating by "moving elements one by one" with tangled indices instead of transpose+reverse.',
              'Spiral: forgetting the mid-loop boundary re-checks (duplicated row/column).',
              'Zeroing a matrix while scanning it — you erase the evidence; record first, apply second.',
              'Using O(m+n) marker arrays when the first row/column can be the markers.']},

'Linked List Manipulation Patterns': {
 'slug': 'linked-list', 'short': 'Pointer surgery: reversal, merging, dummy heads, fast/slow.',
 'intuition': '<p>Linked list problems are about <strong>rewiring pointers without losing pieces</strong>. There is no index access — only walking. Nearly every solution combines four moves: a dummy head (kills edge cases), fast &amp; slow pointers (find middles/cycles), in-place reversal, and splice/merge.</p>',
 'aha': 'You rarely need extra memory: the list itself can be re-linked. "Reorder list" = find middle (fast/slow) + reverse second half + merge two lists — three primitives you already know, glued together.',
 'signals': ['input is a linked list (that alone is the signal)',
             '"reverse", "reorder", "swap in pairs", "rotate" nodes',
             '"k-th from the end", "middle", "cycle" → fast &amp; slow',
             '"merge k sorted lists" → pairwise merge or heap of heads'],
 'template': '''dummy = ListNode(0, head)            # dummy head: prev of the real head
prev, cur = dummy, head

# In-place reversal core
p = None
while cur:
    cur.next, p, cur = p, cur, cur.next
# p is the new head

# Fast & slow
slow = fast = head
while fast and fast.next:
    slow, fast = slow.next, fast.next.next   # slow = middle when fast ends''',
 'template_notes': 'The one-line triple assignment reverses safely because Python evaluates the right side first — the old <code>cur.next</code> is read before being overwritten.',
 'complexity': 'O(n) time — constant passes. O(1) space is the standard expectation; recursion is allowed but costs O(n) stack.',
 'mistakes': ['Overwriting <code>cur.next</code> before saving it — half the list floats away.',
              'No dummy head → separate handling for "the answer is a new head", often buggy.',
              'Cycle problems: comparing <code>.val</code> instead of node identity (<code>is</code>).',
              'After splitting a list, forgetting to set the split point\'s <code>.next = None</code>.']},

'Tree Traversal Patterns (DFS & BFS)': {
 'slug': 'tree-traversal', 'short': 'DFS recursion & BFS levels — the grammar of every tree problem.',
 'intuition': '<p>Every tree problem is a traversal wearing a costume. The question is only: in what <em>order</em> do you visit nodes, and what do you <em>carry</em> — state passed down (path, bounds) or answers passed up (heights, sums)? DFS goes deep via recursion; BFS goes level-by-level via a queue.</p>',
 'aha': 'The recursive leap: <strong>solve the node, trust recursion for the subtrees</strong>. "Diameter" is not a path search — it is, at every node, <code>left_height + right_height</code>, maximized. Once you see each node asks one local question, hard problems become 5-liners.',
 'signals': ['"level", "depth", "nearest", "zigzag by rows" → BFS',
             '"path sum", "ancestor", "validate", "diameter" → DFS',
             'BST + "k-th smallest / sorted order" → inorder',
             '"serialize / reconstruct" → preorder'],
 'template': '''def dfs(node, state):                 # state flows DOWN (bounds, path...)
    if not node:
        return base                       # e.g. 0, True, None
    L = dfs(node.left,  new_state)
    R = dfs(node.right, new_state)
    return combine(node.val, L, R)        # answer flows UP

from collections import deque             # BFS by levels
q = deque([root])
while q:
    for _ in range(len(q)):               # freeze current level size
        node = q.popleft()
        if node.left:  q.append(node.left)
        if node.right: q.append(node.right)''',
 'template_notes': 'A global <code>self.best</code> updated inside DFS handles "best anywhere in the tree" answers (diameter, max path sum) while the function still returns the "usable by parent" value — that split is the key trick.',
 'complexity': 'O(n) time — each node visited once. Space: DFS O(h) recursion stack (h = height, log n balanced, n skewed); BFS O(w) queue (w = widest level, up to n/2).',
 'mistakes': ['Validate BST with only child comparisons — pass down (lo, hi) bounds instead.',
              'BFS levels without freezing <code>len(q)</code> — levels bleed together.',
              'Confusing "return value for parent" with "global answer" in diameter-style problems.',
              'Forgetting the <code>None</code> base case (crash) or returning the wrong neutral value.']},

'Sliding Window Patterns': {
 'slug': 'sliding-window', 'short': 'A moving subarray whose state updates incrementally — O(n²) → O(n).',
 'intuition': '<p>For "best contiguous chunk" problems, brute force recomputes every subarray from scratch. A sliding window keeps <strong>one</strong> chunk and slides it: when the right edge grows and the left edge shrinks, you update the running state (sum, counts) by ±1 item instead of recomputing.</p>',
 'aha': 'Neighboring windows differ by two elements only — one enters, one leaves. If the window state is updatable in O(1), the whole scan is O(n). And because <code>left</code> only ever moves right, the two pointers together take ≤ 2n steps — the inner while loop does NOT make it O(n²).',
 'signals': ['"contiguous subarray / substring" + longest/shortest/max/min/count',
             'fixed size k ("every window of size k")',
             'a constraint to maintain: "at most k distinct", "no repeats", "sum ≥ target"',
             'strings + character frequency ("anagram of", "contains all chars of")'],
 'template': '''# Variable-size window (the general form)
state = {}                              # counts / sum — whatever the constraint needs
left = 0
best = 0
for right in range(len(s)):
    add(s[right], state)                # 1) window grows
    while invalid(state):               # 2) shrink until constraint holds again
        remove(s[left], state)
        left += 1
    best = max(best, right - left + 1)  # 3) window is valid here''',
 'template_notes': 'Fixed-size windows are simpler: slide both edges together once size hits k. For "longest valid" the update happens <em>after</em> the shrink loop; for "shortest valid", inside a "while valid" loop instead — write which one you need before coding.',
 'complexity': 'O(n) time: right moves n times, left moves at most n times total (amortized). Space O(k) for the state (distinct chars / window size).',
 'mistakes': ['Recomputing window state from scratch each step — silently O(n²) again.',
              'Mixing up longest-vs-shortest template shape (where the answer update goes).',
              'Forgetting to delete keys whose count hits 0 — breaks "number of distinct" checks.',
              'Using it on non-contiguous ("subsequence") problems — wrong tool.']},

'Stack Patterns': {
 'slug': 'stack', 'short': 'Deferred decisions: matching, monotonic stacks, expression evaluation.',
 'intuition': '<p>A stack remembers <em>unfinished business</em> in exactly the order you must return to it. Open brackets wait for closers; operators wait for operands; in monotonic stacks, elements wait for their "next greater". Push when a decision can\'t be made yet, pop when today\'s element resolves it.</p>',
 'aha': 'The monotonic stack: keep the stack decreasing; when a bigger element arrives, it IS the "next greater element" for everything it pops. Each index pushes once, pops once — every "for each element find the next bigger/smaller" question drops from O(n²) to O(n).',
 'signals': ['brackets/tags to match or validate',
             '"next greater / next warmer / previous smaller" element',
             'histogram areas, trapped water, "can see over"',
             'evaluate/parse an expression, decode nested strings',
             'undo semantics or "remove adjacent pairs"'],
 'template': '''# Monotonic (decreasing) stack — next greater element
stack = []                              # holds INDICES of unresolved elements
res = [-1] * len(nums)
for i, x in enumerate(nums):
    while stack and nums[stack[-1]] < x:   # x resolves the waiting ones
        j = stack.pop()
        res[j] = x                          # x is j's next greater
    stack.append(i)

# Matching
for ch in s:
    if ch in pairs:  stack.append(ch)
    elif not stack or pairs[stack.pop()] != ch:
        return False
return not stack''',
 'template_notes': 'Store indices, not values — most problems (daily temperatures, spans, histogram) need distances or widths, which only indices give you.',
 'complexity': 'O(n) time — each element is pushed and popped at most once (the while loop is amortized). O(n) space worst case (fully decreasing input).',
 'mistakes': ['Returning True on matching problems without checking the stack is EMPTY at the end.',
              'Choosing the wrong monotonic direction — decreasing stack finds next <em>greater</em>; increasing finds next <em>smaller</em>. Dry-run 3 elements to check.',
              'Strict vs non-strict comparison (<code>&lt;</code> vs <code>&lt;=</code>) — decides how duplicates resolve.',
              'Histogram: forgetting the final flush (append a 0 bar or drain the stack after the loop).']},

'Heap (Priority Queue) Patterns': {
 'slug': 'heap', 'short': 'Always-know-the-extreme: top-k, k-way merge, two heaps, scheduling.',
 'intuition': '<p>When you repeatedly need "the current smallest/largest" from a changing pool, a heap keeps just enough order to answer in O(log n) per operation. The art is choosing <em>what</em> to put in the heap and <em>how big</em> to let it grow.</p>',
 'aha': 'For the k largest elements keep a <strong>min</strong>-heap capped at size k: anything smaller than the heap\'s minimum can never be top-k, so pop it. You process n items but the heap stays tiny — O(n log k) beats sorting whenever k ≪ n.',
 'signals': ['"k largest / k closest / k most frequent / k-th …"',
             'merge k sorted lists/streams',
             '"median of a stream" / balance two halves → two heaps',
             'scheduling: always take the earliest end / most frequent / cheapest next',
             'Dijkstra-style "expand the best frontier node"'],
 'template': '''import heapq
# Top-k largest: min-heap of size k
h = []
for x in nums:
    heapq.heappush(h, x)
    if len(h) > k:
        heapq.heappop(h)                 # evict the smallest of the k+1
# h holds the k largest; h[0] is the k-th largest

# k-way merge: heap of (value, which_list, index)
h = [(lst[0], i, 0) for i, lst in enumerate(lists) if lst]
heapq.heapify(h)
while h:
    val, i, j = heapq.heappop(h)
    out.append(val)
    if j + 1 < len(lists[i]):
        heapq.heappush(h, (lists[i][j+1], i, j+1))''',
 'template_notes': 'Python\'s heap is min-only: negate values for max behavior. Tuples give tie-breaking and payloads: <code>(priority, counter, item)</code> — the counter avoids comparing unorderable items.',
 'complexity': 'Push/pop O(log size), peek O(1), heapify O(n). Top-k: O(n log k) time, O(k) space. Two-heaps median: O(log n) insert, O(1) query.',
 'mistakes': ['Max-heap via negation, then forgetting to negate on the way out.',
              'k largest with a max-heap of ALL n items — works but O(n log n); the size-k min-heap is the intended answer.',
              'Lazy deletion forgotten: when items expire (window moved), skip stale heap tops on pop.',
              'Assuming the heap array is sorted — only index 0 is guaranteed.']},

'Binary Search Patterns': {
 'slug': 'binary-search', 'short': 'Halve a monotonic search space — indexes, answers, anything.',
 'intuition': '<p>Binary search needs only one property: a test that splits the space into "all False, then all True" (monotonic). Compare at the middle, discard the losing half, repeat — O(log n). The deep version: the array is optional. You can binary-search <em>the answer itself</em> ("can we do it with capacity c?") as long as feasibility is monotone.</p>',
 'aha': 'Reframe optimization as decision: "minimum ship capacity" is hard, but "can capacity c ship everything in d days?" is an easy O(n) check — and if c works, every bigger c works. Binary search over c: O(n log range).',
 'signals': ['sorted (or rotated-sorted) array + find/insert position',
             '"minimize the maximum" / "maximize the minimum"',
             'a feasibility check that flips once as a parameter grows',
             'O(log n) demanded explicitly',
             'find a peak / a boundary between regions'],
 'template': '''# Lower-bound shape: smallest index where check(i) is True
lo, hi = 0, n            # hi = n allows "no answer" result
while lo < hi:
    mid = (lo + hi) // 2
    if check(mid):        # True region is on the right side's left edge
        hi = mid          # mid might be the answer — keep it in range
    else:
        lo = mid + 1      # mid is definitely not — discard it
return lo                 # first True (or n if none)

# Binary search on the ANSWER
lo, hi = min_possible, max_possible
while lo < hi:
    mid = (lo + hi) // 2
    if feasible(mid): hi = mid
    else:             lo = mid + 1''',
 'template_notes': 'Learn ONE shape well. This half-open <code>[lo, hi)</code> lower-bound shape terminates cleanly (range shrinks every turn), never skips the answer, and expresses find-exact, insert-position, first/last occurrence, and answer-space searches with only <code>check</code> changing.',
 'complexity': 'O(log n) comparisons; answer-space version O(n log range) — n per feasibility check, log range checks.',
 'mistakes': ['Infinite loop from <code>hi = mid</code> with a closed-interval template — mixing conventions. Pick one, always.',
              'Rotated arrays: forgetting exactly one half is always sorted — test which, then decide.',
              'Using <code>mid = (lo+hi)//2</code> then eliminating mid from the wrong side.',
              'Answer-space search with a non-monotone check — verify feasibility really flips once.']},

'Graph Traversal Patterns (DFS & BFS)': {
 'slug': 'graph-traversal', 'short': 'Islands, shortest paths, topological sort — the traversal toolkit.',
 'intuition': '<p>Graph problems are traversal problems with bookkeeping: BFS explores in distance rings (shortest paths in unweighted graphs), DFS exhausts one region before the next (components, cycles, ordering). Grids are graphs where neighbors are the 4 adjacent cells. The visited set is the seatbelt — cycles loop forever without it.</p>',
 'aha': 'BFS visits nodes strictly in increasing distance order — the FIRST time you reach a node is via a shortest path, guaranteed, no comparisons needed. That single fact answers every unweighted "minimum steps" problem.',
 'signals': ['"islands", "connected", "regions", "provinces" → component DFS/BFS',
             '"minimum steps / moves / days to reach" → BFS',
             '"prerequisites", "build order", "course schedule" → topological sort',
             'states-and-moves puzzles (word ladder, locks) → BFS over implicit graph',
             '"can you finish / is there a cycle" → coloring or Kahn\'s'],
 'template': '''from collections import deque, defaultdict
# BFS shortest steps
q, seen = deque([(start, 0)]), {start}
while q:
    node, d = q.popleft()
    if node == goal: return d
    for nb in neighbors(node):
        if nb not in seen:
            seen.add(nb)                 # mark on ENQUEUE
            q.append((nb, d + 1))

# Topological sort (Kahn's)
indeg = defaultdict(int)
for u in graph:
    for v in graph[u]: indeg[v] += 1
q = deque([u for u in graph if indeg[u] == 0])
order = []
while q:
    u = q.popleft(); order.append(u)
    for v in graph[u]:
        indeg[v] -= 1
        if indeg[v] == 0: q.append(v)
# len(order) < number of nodes  ⇒  cycle exists''',
 'template_notes': 'For grids, <code>neighbors</code> is the 4-direction loop with a bounds check; the visited set holds <code>(r, c)</code> tuples (or mark the grid in place if mutation is allowed).',
 'complexity': 'O(V+E) time for BFS/DFS/topo-sort — every node and edge handled once. O(V) space for visited + queue/stack.',
 'mistakes': ['Marking visited when POPPED instead of when enqueued — duplicates flood the BFS queue.',
              'Missing disconnected pieces — wrap the traversal in a loop over all unvisited starts.',
              'Recursion-depth crash on big grids — iterative stack for deep DFS in Python.',
              'Word-ladder-style problems: generating neighbors by scanning the whole word list (O(n·L)) instead of trying all single-letter mutations (O(26·L)).']},

'Greedy Patterns': {
 'slug': 'greedy', 'short': 'One locally-best choice per step — when short-sighted is optimal.',
 'intuition': '<p>Greedy commits to the best-looking choice at each step and never reconsiders. It\'s the fastest pattern when valid — usually one sort + one pass — but correctness is never free: you owe an argument for why local best can\'t sabotage the future ("exchange argument": any optimal solution can be reshaped to start with the greedy choice without getting worse).</p>',
 'aha': 'The right <em>sort order</em> or <em>frontier metric</em> IS the solution. Interval scheduling: taking the meeting that <strong>ends earliest</strong> leaves maximal room for the rest — provably safe. Jump game: track the farthest reachable index; one pass settles reachability.',
 'signals': ['"maximum number of non-overlapping…" / "minimum number of intervals to remove"',
             '"minimum arrows/platforms/refuels" resource covering',
             'a swap/exchange argument feels available ("taking the smaller first is never worse")',
             'candidates can be sorted so that decisions never need revisiting',
             'DP feels right but n is 10⁵+ and the choice looks local'],
 'template': '''# Interval scheduling: max non-overlapping
intervals.sort(key=lambda iv: iv[1])     # sort by END time
count, free_at = 0, float('-inf')
for start, end in intervals:
    if start >= free_at:                 # doesn't clash with last taken
        count += 1
        free_at = end                    # commit — never look back

# Reachability sweep (jump game)
far = 0
for i, step in enumerate(nums):
    if i > far: return False             # gap we can never cross
    far = max(far, i + step)
return True''',
 'template_notes': 'When greedy fails (choices interact non-locally — e.g. unbounded knapsack), the fallback is DP. If you can\'t sketch the exchange argument in two sentences, be suspicious.',
 'complexity': 'Typically O(n log n) for the sort + O(n) for the pass; O(1) extra space. That efficiency is why interviewers accept greedy only WITH the correctness story.',
 'mistakes': ['Sorting intervals by start when the proof needs end (the classic).',
              'Asserting greedy works without an exchange argument — coin change with coins {1,3,4} breaks greedy: target 6 = 3+3, but greedy takes 4+1+1.',
              'Forgetting ties: define what happens when values are equal, it often matters.',
              'Missing the sweep-line reframe: "minimum platforms" is +1/−1 events sorted by time.']},

'Backtracking Patterns': {
 'slug': 'backtracking', 'short': 'Systematic try-everything with undo — subsets, permutations, boards.',
 'intuition': '<p>When the answer is "all ways to build something" (subsets, permutations, boards), you explore a <strong>decision tree</strong>: at each level make one choice, recurse, then <em>undo</em> the choice and try the next. The undo is what lets one shared <code>path</code> list serve every branch. Pruning — abandoning branches that can\'t succeed — is what makes it fast enough.</p>',
 'aha': 'Choose → explore → un-choose. The un-choose (<code>path.pop()</code>, unmark the cell) restores the world exactly, so sibling branches start clean. Forget it and branches contaminate each other — the single most common backtracking bug.',
 'signals': ['"all combinations / permutations / subsets / partitions"',
             '"generate all valid …" (parentheses, palindromes)',
             'board search: N-Queens, Sudoku, word paths in a grid',
             'n is small (≤ ~20) — exponential output is expected',
             '"count the ways" where DP doesn\'t fit because you need the actual objects'],
 'template': '''def backtrack(start, path):
    if is_complete(path):                 # base: record a snapshot
        res.append(path[:])               # COPY — path keeps mutating!
        return
    for i in range(start, len(choices)):
        if not valid(choices[i]):         # prune early
            continue
        path.append(choices[i])           # choose
        backtrack(i + 1, path)            # explore  (i+1: combinations;
        path.pop()                        # un-choose      i: reuse allowed)

res = []
backtrack(0, [])''',
 'template_notes': '<code>start</code> prevents duplicate combinations (only look forward). Permutations swap it for a <code>used</code> set. Duplicate elements: sort first, then <code>if i &gt; start and c[i] == c[i-1]: continue</code> — skip equal siblings at the same tree level.',
 'complexity': 'Output-bound: subsets O(2ⁿ · n), permutations O(n! · n), boards O(b^d) pre-pruning. State space size × cost of copying each answer — say it that way.',
 'mistakes': ['<code>res.append(path)</code> without copying — every saved answer mutates into garbage.',
              'Missing the un-choose (or unmarking grid cells) — sibling branches inherit dirty state.',
              'Duplicate handling at the wrong level — the skip must compare same-level siblings.',
              'Pruning too late: check validity before recursing, not at the bottom.']},

'Dynamic Programming (DP) Patterns': {
 'slug': 'dp', 'short': 'Overlapping subproblems + memory = exponential → polynomial.',
 'intuition': '<p>DP applies when the answer decomposes into <strong>smaller versions of the same question</strong> whose answers get reused. Brute-force recursion recomputes them exponentially many times; caching (memoization) or building bottom-up (tabulation) computes each once. The whole craft: define the state precisely — "dp[i] = best answer for the first i items" — and write the recurrence connecting states.</p>',
 'aha': 'Count the DISTINCT subproblems, not the calls. fib(n) recursion makes 2ⁿ calls but only n distinct inputs exist — cache them and exponential collapses to linear. If you can name the state, you can usually cache it.',
 'signals': ['"count the number of ways…"',
             '"minimum/maximum cost/value to reach…"',
             'choices at each step + overlapping futures (take/skip an item)',
             '"longest/shortest subsequence" (non-contiguous!)',
             'brute force is exponential and n ≤ a few thousand'],
 'template': '''# Top-down: brute-force recursion + cache
from functools import lru_cache
@lru_cache(None)
def dp(i):
    if i <= base: return base_value
    return best(dp(smaller_1), dp(smaller_2), ...)   # the recurrence

# Bottom-up: same recurrence, loop order = dependency order
dp = [0] * (n + 1)
dp[0] = base_value
for i in range(1, n + 1):
    dp[i] = best(dp[i-1] + ..., dp[i-2] + ...)
# often only last 2 values needed → two variables, O(1) space''',
 'template_notes': 'Recipe: 1) state — the minimal info describing a subproblem; 2) recurrence — how a state\'s answer combines smaller states; 3) base cases; 4) answer location. Write brute-force recursion first, add <code>@lru_cache</code>, then convert to a table if asked.',
 'complexity': '(number of states) × (work per state). 1-D like climbing stairs: O(n)·O(1). 2-D like edit distance: O(m·n)·O(1). Say it as that product.',
 'mistakes': ['A state that\'s missing information — if two different situations map to the same state, the recurrence lies. Add the missing dimension.',
              'Wrong loop order in tabulation — a state must be computed after everything it depends on.',
              '0/1 knapsack in 1-D: iterate capacity DESCENDING or items get reused (that ascending version is unbounded knapsack — know the difference!).',
              'Subsequence ≠ substring — using window logic on subsequence problems.']},

'String Manipulation Patterns': {
 'slug': 'string-manipulation', 'short': 'Frequency signatures, canonical forms, and building-not-concatenating.',
 'intuition': '<p>String problems reduce to a few moves: compare by <strong>frequency signature</strong> (anagrams), map to a <strong>canonical form</strong> so equivalent strings collide in a dict (grouping), scan with two pointers/windows, and always build output as a list joined once. The question behind most of them: <em>what makes two strings "the same" here?</em></p>',
 'aha': 'Design the key, and a dict does the rest. Anagrams → <code>tuple(sorted(w))</code> or a 26-count tuple; isomorphic strings → pattern of first-occurrence indices; shifted strings → tuple of letter-gaps mod 26. One pass, one dict, done.',
 'signals': ['"anagram", "permutation of", "rearrange"',
             '"group the strings that…" → canonical key + dict',
             'palindromes (two pointers or expand-from-center)',
             'parse/normalize (spaces, signs, overflow) — careful state machines',
             'version numbers, IPs, serialization — split + join'],
 'template': '''from collections import defaultdict, Counter
# Group by canonical signature
groups = defaultdict(list)
for w in words:
    key = tuple(sorted(w))        # or 26-tuple of counts: O(k) vs O(k log k)
    groups[key].append(w)

# Expand from center (palindromes)
def expand(s, l, r):
    while l >= 0 and r < len(s) and s[l] == s[r]:
        l -= 1; r += 1
    return s[l+1:r]               # overshoot by one on both sides
# try (i, i) and (i, i+1) for every center: odd + even lengths''',
 'template_notes': 'Anagram-in-window problems combine this with sliding window: keep a running count diff and a "how many letters currently match" counter for O(1) window checks.',
 'complexity': 'Signature grouping: O(n·k log k) with sorted keys, O(n·k) with count-tuples. Expand-from-center: O(n²) time, O(1) space — the accepted baseline for longest palindromic substring.',
 'mistakes': ['String += in a loop — O(n²); collect in a list, join once.',
              'Anagram keys as lists (unhashable) — must be tuple or joined string.',
              'Palindrome centers: forgetting the even-length (i, i+1) centers.',
              'Parsing problems: skipping the messy cases — leading spaces, signs, overflow clamp — they ARE the problem.']},

'Bit Manipulation Patterns': {
 'slug': 'bit-manipulation', 'short': 'XOR cancellation, bit tricks, and masks as sets.',
 'intuition': '<p>Integers are arrays of bits, and bitwise ops act on all 32/64 lanes at once — free parallelism. Three workhorses: <strong>XOR</strong> (pairs cancel: x^x=0), <strong>n &amp; (n−1)</strong> (clears the lowest set bit), and <strong>masks as sets</strong> (bit i = "element i included" — subsets become integers you can cache).</p>',
 'aha': 'XOR of everything makes duplicates vanish: XOR-ing a whole array where every number appears twice except one leaves exactly that one — O(n) time, O(1) space, no hash map. Order doesn\'t matter because XOR is commutative and associative.',
 'signals': ['"every element appears twice except…" → XOR',
             '"without using +/-" arithmetic → bit ops',
             'count/check/flip individual bits, powers of two',
             'n ≤ 20 with subset enumeration → bitmask (possibly + DP)',
             '"O(1) space" on a counting problem that smells impossible'],
 'template': '''x & 1            # is odd? (last bit)
x >> 1, x << 1   # halve / double
x & (x - 1)      # clear lowest set bit  → == 0 means power of two
x & (-x)         # isolate lowest set bit
x ^= y           # toggle by mask; pairs cancel
(x >> i) & 1     # read bit i
x | (1 << i)     # set bit i
x & ~(1 << i)    # clear bit i

# Bitmask subsets: iterate all 2^n subsets of n items
for mask in range(1 << n):
    if mask & (1 << i):  ...   # item i is in this subset''',
 'template_notes': 'Brian Kernighan\'s trick counts set bits in O(number of set bits): loop <code>x &amp;= x-1</code> until zero. Python ints are unbounded — simulate 32-bit wrap with <code>&amp; 0xFFFFFFFF</code> when a problem demands it.',
 'complexity': 'Single-number tricks: O(n) time, O(1) space. Bitmask enumeration: O(2ⁿ) subsets — fine only for n ≤ ~20 (and O(3ⁿ) for subset-of-subset loops).',
 'mistakes': ['Sign bugs porting negative-number logic — Python has no fixed width; mask explicitly.',
              'Operator precedence: <code>x &amp; 1 == 0</code> parses as <code>x &amp; (1 == 0)</code> — parenthesize!',
              'Confusing XOR-swap cleverness with clarity — just use tuple swap in Python.',
              'Missing that "appears 3 times except one" needs per-bit counting mod 3, not plain XOR.']},

'Design Patterns': {
 'slug': 'design', 'short': 'Compose structures to hit per-operation complexity targets.',
 'intuition': '<p>Design problems ("build LRU cache", "design Twitter") flip the script: you\'re given an API and per-operation complexity targets, and must <em>compose</em> structures — because no single one is fast at everything. The method: list the operations, write each one\'s target cost, and pick the minimal combination that covers all of them.</p>',
 'aha': 'Pair structures so each covers the other\'s weakness. LRU cache: dict gives O(1) lookup but no order; doubly-linked list gives O(1) reorder/evict but no lookup — dict-of-nodes gives both. O(1) insert/delete/getRandom: list for random, dict of value→index for delete (swap victim with last element, pop).',
 'signals': ['"Design/implement a class with operations X, Y, Z"',
             'explicit per-op complexity targets ("all in O(1)")',
             'eviction rules (LRU/LFU), recency, frequency',
             '"getRandom", "getMin", snapshots, iterators',
             'streaming data with rolling queries'],
 'template': '''# The composition method:
# 1. Ops:      get(k), put(k,v), evict_least_recent
# 2. Targets:  O(1),   O(1),     O(1)
# 3. Pick:     dict  → O(1) get/put by key
#              DLL   → O(1) move-to-front / evict-tail
#              glue: dict maps key → its DLL node

# In Python interviews, OrderedDict is the accepted shortcut:
from collections import OrderedDict
class LRUCache:
    def __init__(self, cap):
        self.d, self.cap = OrderedDict(), cap
    def get(self, k):
        if k not in self.d: return -1
        self.d.move_to_end(k)            # mark most-recent
        return self.d[k]
    def put(self, k, v):
        if k in self.d: self.d.move_to_end(k)
        self.d[k] = v
        if len(self.d) > self.cap:
            self.d.popitem(last=False)   # evict least-recent''',
 'template_notes': 'Say you know what OrderedDict hides (hash map + linked list) and offer to build the raw version — that\'s usually the actual test. Min-stack trick: store <code>(value, min_so_far)</code> pairs so getMin is a peek.',
 'complexity': 'Stated per operation, not overall: "get O(1), put O(1) amortized, space O(capacity)". Always give the space cost of the extra structures.',
 'mistakes': ['Optimizing one operation to the ruin of another — re-check every op against its target.',
              'LRU updated on put but not on GET — reads also refresh recency.',
              'Random-delete without the swap-with-last trick (list removal is O(n)).',
              'Forgetting edge ops: eviction at exactly capacity, get on missing key, duplicate put.']},

'Segment Tree & Fenwick Tree Patterns': {
 'slug': 'segment-tree', 'short': 'O(log n) range queries AND point updates, together.',
 'intuition': '<p>Prefix sums make range queries O(1) but updates O(n); a plain array is the reverse. When both are frequent, segment trees and Fenwick (BIT) trees balance the trade at O(log n) each, by storing aggregates over ranges arranged in a tree so any query/update touches only O(log n) nodes.</p>',
 'aha': 'Any range [l, r) decomposes into O(log n) pre-stored node ranges; any single update dirties only its O(log n) ancestors. You never re-aggregate more than a logarithmic slice of the structure.',
 'signals': ['interleaved "update element" + "query range sum/min/max"',
             '"count of smaller elements after self" (offline index counting)',
             'k-th smallest with insertions/deletions',
             'huge value range → coordinate-compress first',
             'range updates too → difference trick or lazy propagation'],
 'template': '''# Fenwick / BIT — shortest correct implementation (1-indexed)
tree = [0] * (n + 1)
def update(i, delta):            # a[i] += delta, O(log n)
    while i <= n:
        tree[i] += delta
        i += i & (-i)            # next block responsible for i
def prefix(i):                   # sum a[1..i], O(log n)
    s = 0
    while i > 0:
        s += tree[i]
        i -= i & (-i)
    return s
def range_sum(l, r):
    return prefix(r) - prefix(l - 1)''',
 'template_notes': 'Fenwick for sums (short, fast); segment tree when the operation isn\'t invertible (min/max/gcd) or you need lazy range-updates. "Count smaller after self" = walk the array right-to-left, BIT over value ranks.',
 'complexity': 'Build O(n) (segment) / O(n log n) naive BIT fills; update & query O(log n); space O(n) (segment tree arrays: 4n slots is the safe size).',
 'mistakes': ['Fenwick is 1-indexed — off-by-one on index 0 breaks the bit trick silently.',
              'Using BIT for min/max — prefix mins can\'t be subtracted; use a segment tree.',
              'Skipping coordinate compression when values reach 10⁹.',
              'Range-update + range-query without lazy propagation (or the two-BIT trick).']},

'Prefix Sum & Difference Array Patterns': {
 'slug': 'prefix-sum', 'short': 'Precompute running totals; answer any range in O(1).',
 'intuition': '<p>If you\'ll ask many range-sum questions, pay O(n) once to store running totals: <code>prefix[i]</code> = sum of the first i elements. Then any range sum is a subtraction. The same idea powers "subarray sums equal k" (via a hash map of seen prefixes) and its mirror twin, the <strong>difference array</strong>, which turns many range-updates into O(1) each.</p>',
 'aha': 'sum(i..j) = prefix[j+1] − prefix[i] — so "does any subarray sum to k?" becomes "have I already SEEN a prefix equal to current − k?" A dict of seen prefix-sums answers that in O(1) per step: the O(n²) subarray scan collapses to one pass.',
 'signals': ['many range-sum queries, immutable array',
             '"number of subarrays summing to k / divisible by k"',
             'many range UPDATES, values read once at the end → difference array',
             '2-D block sums → 2-D prefix (inclusion-exclusion)',
             '"equal 0s and 1s" → map to ±1 and find zero-sum ranges'],
 'template': '''# Prefix sums + hash map: count subarrays summing to k
from collections import defaultdict
count, cur = 0, 0
seen = defaultdict(int)
seen[0] = 1                      # empty prefix — subarrays starting at 0
for x in nums:
    cur += x
    count += seen[cur - k]       # each earlier prefix = one subarray ending here
    seen[cur] += 1

# Difference array: m range updates in O(1) each
diff = [0] * (n + 1)
for l, r, val in updates:
    diff[l] += val
    diff[r + 1] -= val           # effect ends after r
# final values = prefix sums of diff''',
 'template_notes': 'The trio to memorize: prefix + dict (counting), difference array (bulk updates), 2-D prefix <code>P[r][c] = A + P[r-1][c] + P[r][c-1] − P[r-1][c-1]</code> (block sums).',
 'complexity': 'Build O(n); each query/update O(1). Subarray counting: O(n) time, O(n) space for the dict.',
 'mistakes': ['Forgetting <code>seen[0] = 1</code> — misses every subarray that starts at index 0.',
              'Off-by-one between "prefix includes i" and "excludes i" — pick length-(n+1) prefixes.',
              'Negative numbers: sliding window fails but prefix+dict works — know when you\'re in which world.',
              'Difference array: writing −val at r instead of r+1.']},

'Hash Map & Cache Design Patterns': {
 'slug': 'hash-map', 'short': 'O(1) lookup as an engine for caches and composed structures.',
 'intuition': '<p>Beyond plain counting, this family builds <em>machinery</em> around O(1) lookup: caches with eviction (LRU/LFU), O(1)-everything sets, key-value stores with expiry or versions. The recurring shape: the dict finds things instantly, a second structure (linked list, heap, second dict) maintains whatever <em>order</em> the dict cannot.</p>',
 'aha': 'A dict pointing at linked-list NODES gives you both worlds at once: hash-speed access to an element AND O(1) splice-out/reorder of that element. That one composition is LRU, LFU (dict of frequency-buckets), and most "O(1) all operations" designs.',
 'signals': ['"O(1) average for every operation"',
             'eviction by recency/frequency, capacity limits',
             'time-versioned lookups (get value at timestamp)',
             'two-way mappings, consistent grouping',
             '"design a HashMap/HashSet" from primitives'],
 'template': '''# Frequency buckets (LFU core idea, also "O(1) inc/dec"):
# key → count, and count → set of keys with that count
counts = {}                       # key → its frequency
buckets = defaultdict(set)        # frequency → keys at that frequency
min_freq = tracked separately     # evict from buckets[min_freq]

# Timestamped values: dict of key → sorted list of (time, value)
import bisect
store = defaultdict(list)
def set_val(k, v, t): store[k].append((t, v))       # times arrive increasing
def get_val(k, t):
    arr = store[k]
    i = bisect.bisect_right(arr, (t, chr(0x10FFFF)))  # last entry ≤ t
    return arr[i-1][1] if i else ""''',
 'template_notes': 'Ask what each operation must cost <em>before</em> choosing structures. If eviction order matters → linked list or buckets; if "as of time t" → sorted list + bisect; if "min/max too" → add a heap or store pairs.',
 'complexity': 'The point is per-operation O(1) average (or O(log n) where bisect enters). State the space overhead — usually O(capacity) or O(total entries).',
 'mistakes': ['Iterating the dict to find an eviction victim — that\'s the O(n) you were hired to avoid.',
              'LFU without tracking min_freq — finding it on demand is O(n).',
              'Timestamp lookups with linear scan instead of bisect.',
              'Forgetting to clean empty buckets — stale min_freq pointers.']},

'Math, Number Theory & Geometry Patterns': {
 'slug': 'math', 'short': 'GCD, primes, modular arithmetic, and geometry with integer tricks.',
 'intuition': '<p>These problems trade data structures for facts: gcd via Euclid, primes via sieve, modular exponentiation, digit manipulation, coordinate geometry with cross products. There\'s usually a short insight that makes the code tiny — the risk is not knowing the fact, so this pattern is more "learn the toolbox" than "derive on the spot".</p>',
 'aha': 'Work smarter with structure: Euclid — gcd(a,b) = gcd(b, a mod b) collapses in O(log min); the sieve marks multiples instead of testing divisibility, giving all primes ≤ n in O(n log log n); pow(a, b, m) squares its way to the answer in O(log b).',
 'signals': ['divisibility, remainders, "answer modulo 10⁹+7"',
             'counting primes/factors/trailing zeros',
             'digit games: reverse, palindrome number, happy number',
             'geometry: overlaps of rectangles, points on a line, areas',
             'sequences with closed forms (sum formulas, cycle detection on digits)'],
 'template': '''import math
math.gcd(a, b)                      # Euclid, O(log min(a,b))
pow(a, b, MOD)                      # fast modular exponentiation, O(log b)

def sieve(n):                       # all primes ≤ n
    is_p = [True] * (n + 1)
    is_p[0] = is_p[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_p[i]:
            for j in range(i*i, n + 1, i):   # start at i² — smaller done
                is_p[j] = False
    return is_p

# Digits without strings
while n: n, d = divmod(n, 10)       # d = last digit

# Cross product: orientation of C vs line AB (0 = collinear)
cross = (bx-ax)*(cy-ay) - (by-ay)*(cx-ax)''',
 'template_notes': 'Rectangle overlap reads cleanest as "NOT disjoint": disjoint iff one is fully left/right/above/below the other. Slopes: never divide — compare via cross products to dodge division-by-zero and float error.',
 'complexity': 'Per-fact: Euclid O(log), sieve O(n log log n), fast pow O(log b). Mention overflow story: Python ints don\'t overflow, but mod keeps numbers small and matches other languages.',
 'mistakes': ['Applying MOD only at the end — apply after every multiply/add.',
              'Floating-point equality for geometry — integers and cross products instead.',
              'Sieve inner loop from 2·i instead of i·i — correct but slower; and forgetting 0,1 aren\'t prime.',
              'Negative mod surprises: Python\'s % is always non-negative, unlike C/Java — flag it.']},

'Trie / Prefix Tree Patterns': {
 'slug': 'trie', 'short': 'Share prefixes in a tree — search a whole dictionary in O(word).',
 'intuition': '<p>When one word is the query, a set suffices. When a <em>set of words</em> must be matched against prefixes, wildcards, or a letter grid, the trie shines: words sharing a prefix share a path, so a single walk simultaneously checks every word with that prefix — and a dead branch prunes all of them at once.</p>',
 'aha': 'In grid word-search, walk the trie WHILE you DFS the board: the moment the current path isn\'t a trie prefix, abandon the entire branch. Thousands of candidate words are eliminated in one comparison — that\'s Word Search II\'s whole trick.',
 'signals': ['"startsWith", autocomplete, longest common prefix over many strings',
             'wildcard search (\'.\' matches anything) → branch at the dot',
             'find many words in a letter grid simultaneously',
             'XOR maximization → binary trie over bits',
             '"replace words with shortest root"'],
 'template': '''class TrieNode:
    __slots__ = ('kids', 'end')
    def __init__(self):
        self.kids = {}                 # char → TrieNode
        self.end = False               # a word ends here

root = TrieNode()
def insert(word):                      # O(len)
    node = root
    for ch in word:
        node = node.kids.setdefault(ch, TrieNode())
    node.end = True

def search(word, node=None, i=0):      # supports '.' wildcard
    node = node or root
    for j in range(i, len(word)):
        ch = word[j]
        if ch == '.':
            return any(search(word, kid, j+1) for kid in node.kids.values())
        if ch not in node.kids: return False
        node = node.kids[ch]
    return node.end''',
 'template_notes': 'Store the full word on end-nodes in grid problems (no path reconstruction), and prune: delete leaf nodes after a word is found to shrink future searches.',
 'complexity': 'Insert/search O(L) per word — independent of dictionary size (a set can\'t say that for prefixes). Space O(total characters) worst case; shared prefixes compress it.',
 'mistakes': ['Marking end-of-word implicitly (leaf = word) — "car" inside "cart" needs an explicit flag.',
              'Wildcard search iteratively — the branching needs recursion.',
              'Grid search: checking word membership per path instead of walking the trie alongside.',
              'Not unmarking grid cells on backtrack (the usual backtracking sin).']},

'Intervals & Line Sweep Patterns': {
 'slug': 'intervals', 'short': 'Sort by start (or as events), then merge/count in one pass.',
 'intuition': '<p>Interval chaos becomes order the moment you sort. Sorted by start, overlap is a local question — each interval only interacts with the one before it. The other lens is the <strong>sweep line</strong>: convert intervals to +1/−1 <em>events</em>, sort events, and a running counter tells you how many intervals cover every moment.</p>',
 'aha': 'After sorting by start, "does interval i overlap anything?" reduces to <code>start_i ≤ end of the merged block so far</code>. One comparison per interval. And "max simultaneous meetings" is just the peak of the +1/−1 counter — no interval pairs ever compared.',
 'signals': ['"merge overlapping intervals" / "insert interval"',
             '"minimum meeting rooms / platforms / arrows"',
             '"remove fewest to make non-overlapping" (greedy by end)',
             'bookings, calendars, seat/resource occupancy over time',
             'skyline-style "what is the profile over time"'],
 'template': '''# Merge intervals
intervals.sort(key=lambda iv: iv[0])
merged = []
for s, e in intervals:
    if merged and s <= merged[-1][1]:            # overlaps the last block
        merged[-1][1] = max(merged[-1][1], e)    # extend it
    else:
        merged.append([s, e])

# Sweep line: max concurrent intervals
events = []
for s, e in intervals:
    events.append((s, 1))          # interval opens
    events.append((e, -1))         # interval closes
events.sort()                      # ties: -1 before +1 ⇒ [1,2],[2,3] don't stack
cur = peak = 0
for _, delta in events:
    cur += delta
    peak = max(peak, cur)''',
 'template_notes': 'Decide the tie rule consciously: does an interval ending at t overlap one starting at t? Closed intervals ⇒ yes (sort +1 before −1); half-open ⇒ no (−1 first, which plain tuple sort gives you).',
 'complexity': 'O(n log n) for the sort dominates; the pass is O(n). Meeting-rooms heap variant: O(n log n) too (heap of end times).',
 'mistakes': ['Not sorting first — nothing about intervals works unsorted.',
              'Tie-breaking at equal timestamps done by accident instead of by decision.',
              'Merging with <code>e &lt; merged[-1][1]</code> — forgetting to take the max of ends (nested intervals!).',
              '"Remove fewest overlapping" greedily by start instead of by END.']},

'Tree Dynamic Programming Patterns': {
 'slug': 'tree-dp', 'short': 'Postorder DFS returning tuples: DP where subproblems are subtrees.',
 'intuition': '<p>Tree DP = DP where the subproblems are <em>subtrees</em>. A postorder DFS computes children first, then combines their answers at the parent. The craft is deciding what each node reports upward — often a tuple of scenarios, like ("best if I\'m included", "best if I\'m excluded").</p>',
 'aha': 'When one number isn\'t enough, return a tuple of cases. House Robber III: each node returns (loot if robbed, loot if skipped); the parent combines them with its own choice. The exponential "try all subsets of nodes" collapses to one O(n) traversal.',
 'signals': ['optimize a value over a TREE (max path, max loot, longest chain)',
             'constraints between parent and child ("can\'t pick both")',
             '"count/size/best of subtrees" feeding a global answer',
             'the diameter shape: best-through-this-node vs best-for-parent differ',
             'rerooting: answer needed for EVERY node as root'],
 'template': '''def dfs(node):
    if not node:
        return NEUTRAL                     # e.g. (0, 0)
    L = dfs(node.left)                     # children first (postorder)
    R = dfs(node.right)
    include = node.val + L[1] + R[1]       # take node → children excluded
    exclude = max(L) + max(R)              # skip node → children free
    # global-answer problems also do:  best = max(best, through_node)
    return (include, exclude)

ans = max(dfs(root))''',
 'template_notes': 'The diameter/max-path-sum family has TWO quantities: the value <em>through</em> the node (may use both children — updates the global) and the value the node <em>offers its parent</em> (one child only — gets returned). Never conflate them.',
 'complexity': 'O(n) time — each node combined once; O(h) recursion stack. Rerooting technique: two passes, still O(n) for all n answers.',
 'mistakes': ['Returning the "through" value to the parent — a parent can\'t use a forked path.',
              'Clamping negatives forgotten: <code>max(0, child_gain)</code> in max-path-sum.',
              'Wrong neutral for None: (0,0) fine for sums; -inf needed for maxima of node values.',
              'Doing tree DP top-down without memo keyed by (node, state) — recompute explosion on shared logic.']},

'Advanced Dynamic Programming Patterns': {
 'slug': 'advanced-dp', 'short': 'Knapsack family, LIS, edit distance, intervals & bitmask DP.',
 'intuition': '<p>Same DP discipline, richer state spaces: two sequences (edit distance — 2-D grid of prefixes), capacity dimensions (knapsack), "last element matters" (LIS), ranges (burst balloons — interval DP), or subsets as bitmasks. Recognizing WHICH classic family a problem belongs to is most of the solve — the recurrences are standard once named.</p>',
 'aha': 'State design is compression: dp[i][j] for edit distance says "the answer for prefixes i and j" — you don\'t care HOW you got there, only the value. Whenever the future depends on a bounded summary of the past, that summary IS your state, however weird (capacity left, last index chosen, set of visited nodes).',
 'signals': ['two strings/sequences compared → 2-D prefix DP',
             'pick items under a budget → knapsack (0/1 vs unbounded!)',
             '"longest increasing …" → LIS (O(n log n) with patience trick)',
             'operations on ranges "burst/merge/remove" → interval DP over lengths',
             'n ≤ ~16 with "visit all" → bitmask DP'],
 'template': '''# 2-D sequence DP (edit distance shape)
dp = [[0]*(m+1) for _ in range(n+1)]
for i in range(n+1): dp[i][0] = i          # base: delete everything
for j in range(m+1): dp[0][j] = j
for i in range(1, n+1):
    for j in range(1, m+1):
        if a[i-1] == b[j-1]:
            dp[i][j] = dp[i-1][j-1]         # free match
        else:
            dp[i][j] = 1 + min(dp[i-1][j],      # delete
                               dp[i][j-1],      # insert
                               dp[i-1][j-1])    # replace

# 0/1 knapsack, 1-D
dp = [0] * (W + 1)
for wt, val in items:
    for w in range(W, wt - 1, -1):          # DESCENDING: item used once
        dp[w] = max(dp[w], dp[w - wt] + val)</code>''',
 'template_notes': 'LIS in O(n log n): keep <code>tails</code> where tails[k] = smallest tail of any increasing subsequence of length k+1; binary-search each element\'s slot. Interval DP: iterate by range LENGTH, and let the loop variable be "the LAST balloon burst" not the first — that\'s what makes subproblems independent.',
 'complexity': 'Sequence DP O(n·m); knapsack O(n·W) (pseudo-polynomial — W is a number, not a size!); LIS O(n log n); interval DP O(n³); bitmask DP O(2ⁿ·n).',
 'mistakes': ['Knapsack loop direction: ascending = unbounded, descending = 0/1. The #1 silent bug.',
              'LIS <code>tails</code> misread as an actual subsequence — it\'s not, only its length is meaningful.',
              'Interval DP anchored on the FIRST action instead of the last — subproblems overlap and the recurrence breaks.',
              'Bitmask DP beyond n≈20 — 2ⁿ states explode; check constraints first.']},

'Advanced Graph Algorithm Patterns': {
 'slug': 'advanced-graph', 'short': 'Dijkstra, Bellman-Ford, MST, bridges — weighted-world tools.',
 'intuition': '<p>Once edges have weights, BFS\'s guarantee dies. Dijkstra restores it for non-negative weights by expanding nodes in cost order (BFS with a heap). Bellman-Ford survives negative edges by brute relaxation. MST algorithms (Kruskal/Prim) connect everything cheaply. Tarjan-style DFS timestamps find the fragile edges (bridges). Pick by edge type + question type.</p>',
 'aha': 'Dijkstra is BFS where the queue became a min-heap keyed by total cost: when a node pops, its distance is FINAL (any other route must pass through something already ≥ as expensive — impossible to improve with non-negative edges). That greedy certainty is why one negative edge breaks it.',
 'signals': ['"cheapest / fastest path" with weights → Dijkstra (non-negative)',
             'negative weights or "at most k stops" → Bellman-Ford / k-round relaxation',
             '"minimum cost to connect all" → MST (Kruskal + DSU, or Prim)',
             '"critical connection" whose removal disconnects → bridges (Tarjan)',
             'all-pairs on small dense graphs → Floyd-Warshall O(V³)'],
 'template': '''import heapq
# Dijkstra
dist = {start: 0}
h = [(0, start)]
while h:
    d, u = heapq.heappop(h)
    if d > dist.get(u, float('inf')):    # stale heap entry — skip
        continue
    for v, w in graph[u]:
        nd = d + w
        if nd < dist.get(v, float('inf')):
            dist[v] = nd
            heapq.heappush(h, (nd, v))   # lazy: duplicates OK, skip stale

# Bellman-Ford core: V-1 rounds of relaxing every edge
for _ in range(V - 1):
    for u, v, w in edges:
        if dist[u] + w < dist[v]:
            dist[v] = dist[u] + w
# one more improving round ⇒ negative cycle''',
 'template_notes': 'Kruskal: sort edges by weight, add each unless DSU says it forms a cycle — MST in O(E log E). "K stops" flight problems: Bellman-Ford but only k+1 rounds, relaxing from a COPY of last round\'s distances.',
 'complexity': 'Dijkstra O((V+E) log V) with a heap; Bellman-Ford O(V·E); Kruskal O(E log E); Floyd-Warshall O(V³); bridges O(V+E).',
 'mistakes': ['Dijkstra with negative edges — silently wrong, not an error.',
              'Forgetting the stale-entry skip — correctness survives, performance dies.',
              'Bellman-Ford k-stops without the copy — paths use too many stops within one round.',
              'MST vs shortest path confusion: minimizing total wiring ≠ minimizing any route.']},

'Multi-Source BFS Patterns': {
 'slug': 'multi-source-bfs', 'short': 'Seed BFS with ALL sources at once — nearest-anything fields.',
 'intuition': '<p>"How far is each cell from the nearest X?" Running BFS from every X separately costs O(sources × V). Instead seed the queue with <em>all</em> X\'s at distance 0 and run ONE BFS: the wavefronts expand together, and whichever front reaches a cell first is, by BFS\'s order guarantee, the nearest source.</p>',
 'aha': 'Flip the direction: don\'t search FROM each cell FOR the nearest source — flood FROM all sources TO every cell simultaneously. It\'s equivalent to adding a virtual super-source connected to all real sources. One pass, O(V+E) total.',
 'signals': ['"distance to nearest 0/gate/land" for EVERY cell',
             'simultaneous spreading: rotting oranges, fire, infection + "how long until…"',
             '"highest cell / farthest from any coast" (max of min-distances)',
             'many starting points, one uniform spread speed'],
 'template': '''from collections import deque
q = deque()
dist = [[-1] * cols for _ in range(rows)]
for r in range(rows):                     # seed ALL sources at distance 0
    for c in range(cols):
        if grid[r][c] == SOURCE:
            dist[r][c] = 0
            q.append((r, c))
while q:
    r, c = q.popleft()
    for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and dist[nr][nc] == -1 \\
           and passable(grid[nr][nc]):
            dist[nr][nc] = dist[r][c] + 1
            q.append((nr, nc))
# "time until all infected" = max over dist; unreachable stay -1''',
 'template_notes': 'The dist grid doubles as the visited set (−1 = unseen). For "minutes until done" answers, either track the max distance or process level-by-level with the <code>len(q)</code> freeze and count rounds.',
 'complexity': 'O(V+E) = O(rows·cols) on grids — identical to single-source BFS; that\'s the entire win. Space O(V) for queue + distances.',
 'mistakes': ['Running per-source BFS loops — the exact O(S·V) trap this pattern deletes.',
              'Seeding sources with distance 0 but forgetting to mark them visited.',
              'Rotting oranges: not checking afterwards whether unreachable fresh cells remain (answer −1).',
              'Counting rounds off by one — an initially-done grid is 0 minutes.']},

'Iterator & Data-Stream Design Patterns': {
 'slug': 'iterators', 'short': 'Lazy evaluation: produce the next element on demand, O(1) state.',
 'intuition': '<p>Sometimes you must expose data <em>one element at a time</em> — flattening nested structures, peeking ahead, merging streams — without materializing everything. The discipline: keep just enough state (a stack of positions, a buffered element, running aggregates) to answer <code>next()</code> and <code>hasNext()</code> quickly, and do work lazily.</p>',
 'aha': 'Push the WORK into hasNext(): keep a stack of "places I still have to explore"; hasNext() digs until the top is a real element (or the stack dies). next() then just pops. This makes nested/lazy iteration correct even with empty sublists everywhere — and BST iterators O(h) memory instead of O(n).',
 'signals': ['"implement an iterator over…" (nested lists, BST, zigzag of k lists)',
             '"peek()" on top of an existing iterator → one-element buffer',
             'streaming: moving average, median, top-k of a live feed',
             'can\'t afford to flatten/materialize (memory bound)'],
 'template': '''# Nested-list iterator: stack of (list, index) frames
class Flattener:
    def __init__(self, nested):
        self.stack = [(nested, 0)]
    def hasNext(self):
        while self.stack:
            lst, i = self.stack[-1]
            if i == len(lst):
                self.stack.pop()                # frame exhausted
            elif isinstance(lst[i], list):
                self.stack[-1] = (lst, i + 1)   # consume slot,
                self.stack.append((lst[i], 0))  # descend into it
            else:
                return True                     # real element on top
        return False
    def next(self):
        lst, i = self.stack[-1]
        self.stack[-1] = (lst, i + 1)
        return lst[i]

# BST iterator: stack = path of left spines → O(h) memory inorder
# Moving average: deque(maxlen=k) + running sum''',
 'template_notes': 'peek() wraps any iterator: cache one element, serve it before advancing. Stream medians: the two-heap structure from the Heap pattern, maintained per arrival.',
 'complexity': 'Aim for amortized O(1) per next() (each element touched a constant number of times overall) and sublinear state — O(depth) or O(h) or O(k), never O(total).',
 'mistakes': ['Flattening everything in the constructor — legal, but it dodges the actual question; say the trade-off.',
              'next() without hasNext()\'s digging — breaks on empty nested lists.',
              'Iterator invalidation: mutating the underlying data mid-iteration.',
              'Moving average dividing by k before the window is full.']},

'Sorting Algorithms & Selection Patterns': {
 'slug': 'sorting-selection', 'short': 'Implement-the-sort problems + quickselect and counting tricks.',
 'intuition': '<p>Here the sort IS the problem: implement merge sort on a linked list, sort colors in one pass, find the k-th largest without full sorting. The leverage points: merge sort\'s merge step, quicksort\'s partition step (reusable alone as quickselect), and non-comparison counting when the value range is tiny.</p>',
 'aha': 'Partition does useful work even without sorting: after one partition, the pivot sits at its FINAL index, everything smaller is left, bigger is right. Recurse into just one side and you have quickselect — k-th element in O(n) average, no full sort.',
 'signals': ['"k-th largest/smallest" without needing full order → quickselect',
             '"sort colors / 0s,1s,2s in one pass" → Dutch national flag',
             'sort a LINKED list in O(n log n) O(1) space → merge sort',
             'values in a tiny known range → counting sort',
             '"sort by custom rule" (largest concatenation) → comparator thinking'],
 'template': '''# Dutch national flag: 3-way partition, one pass
lo, mid, hi = 0, 0, len(a) - 1
while mid <= hi:
    if a[mid] == 0:
        a[lo], a[mid] = a[mid], a[lo]; lo += 1; mid += 1
    elif a[mid] == 2:
        a[mid], a[hi] = a[hi], a[mid]; hi -= 1     # mid NOT advanced!
    else:
        mid += 1

# Quickselect skeleton (k-th smallest) — partition, recurse one side
import random
def quickselect(a, k):
    p = random.choice(a)
    lo  = [x for x in a if x < p]
    eq  = [x for x in a if x == p]
    if k < len(lo): return quickselect(lo, k)
    if k < len(lo) + len(eq): return p
    return quickselect([x for x in a if x > p], k - len(lo) - len(eq))''',
 'template_notes': 'Why mid doesn\'t advance after swapping with hi: the element that arrived from the right is unexamined. Random pivots make the O(n²) adversarial case vanish in practice; mention median-of-medians for guaranteed O(n).',
 'complexity': 'Quickselect O(n) average / O(n²) worst (random pivot ⇒ negligible); Dutch flag O(n)/O(1); linked-list merge sort O(n log n) with O(1) extra (bottom-up).',
 'mistakes': ['Advancing mid after the hi-swap in Dutch flag — skips elements.',
              'Quickselect without randomization on adversarial inputs.',
              'k-th LARGEST vs k-th smallest index conversion: k-th largest = (n−k)-th smallest.',
              'Linked-list sorting with array algorithms (random access doesn\'t exist).']},

'Randomized Algorithm Patterns': {
 'slug': 'randomized', 'short': 'Fisher-Yates, reservoir sampling, weighted picks — provable fairness.',
 'intuition': '<p>Randomness as a tool: shuffle uniformly, sample fairly from streams of unknown length, pick proportional to weights. Each has a short provably-correct recipe — and famous plausible-looking WRONG versions. The bar is being able to state why each element ends up equally (or proportionally) likely.</p>',
 'aha': 'Reservoir sampling: keep the i-th arriving item with probability 1/i, evicting a random incumbent. Induction shows every item seen so far ends at exactly 1/i — so you can sample uniformly from a stream without knowing its length, in O(1) memory.',
 'signals': ['"shuffle" / "random pick" with uniformity required',
             'stream or linked list of unknown length + "pick one uniformly"',
             'pick index proportional to weight → prefix sums + bisect',
             'O(1) getRandom in a set → array + swap-delete',
             '"random point in circle/rectangles" → geometric transforms'],
 'template': '''import random
# Fisher-Yates shuffle — uniform over all n! orders
for i in range(len(a) - 1, 0, -1):
    j = random.randint(0, i)          # j ∈ [0, i]  (inclusive!)
    a[i], a[j] = a[j], a[i]

# Reservoir sampling (k = 1) from a stream
choice, count = None, 0
for x in stream:
    count += 1
    if random.randint(1, count) == 1:   # prob 1/count
        choice = x

# Weighted random pick: prefix sums + binary search
import bisect, itertools
prefix = list(itertools.accumulate(weights))
def pick():
    r = random.uniform(0, prefix[-1])
    return bisect.bisect_left(prefix, r)    # first prefix ≥ r</code>''',
 'template_notes': 'The famous wrong shuffle draws j from the WHOLE range every step — it produces nⁿ equally-likely paths that can\'t map evenly onto n! orders, so it\'s biased. Know this story; it\'s the interview question behind the question.',
 'complexity': 'Shuffle O(n)/O(1). Reservoir O(n) stream pass, O(k) memory. Weighted pick O(n) build then O(log n) per query.',
 'mistakes': ['<code>randint(0, len(a)-1)</code> in Fisher-Yates instead of <code>(0, i)</code> — the biased classic.',
              'Weighted pick with bisect_right vs uniform float edge cases — trace a boundary.',
              'Reservoir with <code>random.random() &lt; 1/count</code> float form — fine, but be able to prove it.',
              'Testing randomness by eyeballing one run — check distributions over many runs.']},

'Advanced String Algorithm Patterns': {
 'slug': 'advanced-strings', 'short': 'KMP, Rabin-Karp, Manacher — pattern matching past the naive wall.',
 'intuition': '<p>Naive substring search re-compares up to O(n·m) characters because it forgets everything after each mismatch. The advanced algorithms all monetize memory of what already matched: KMP precomputes how much of a match survives a mismatch; Rabin-Karp compares rolling <em>hashes</em> in O(1); Manacher reuses palindrome symmetry. Total: O(n+m) where naive pays O(n·m).</p>',
 'aha': 'KMP\'s failure table answers one question: "after matching pattern[0..k] and failing, what is the LONGEST proper prefix of the pattern that is also a suffix of what matched?" Jump there instead of restarting — the text pointer never moves backwards, guaranteeing linear time.',
 'signals': ['find/count occurrences of a pattern in a long text',
             '"shortest palindrome by prepending", "longest prefix = suffix" → failure function',
             'many substring-equality checks → rolling hash',
             '"repeated substring pattern" / string periodicity',
             'longest palindromic substring in O(n) explicitly → Manacher'],
 'template': '''# KMP failure table: fail[i] = length of longest proper prefix of
# pat[0..i] that is also its suffix
def build_fail(pat):
    fail = [0] * len(pat)
    k = 0
    for i in range(1, len(pat)):
        while k and pat[i] != pat[k]:
            k = fail[k - 1]            # fall back to shorter border
        if pat[i] == pat[k]:
            k += 1
        fail[i] = k
    return fail

def kmp_search(text, pat):             # O(n + m)
    fail, k = build_fail(pat), 0
    for i, ch in enumerate(text):
        while k and ch != pat[k]:
            k = fail[k - 1]
        if ch == pat[k]:
            k += 1
        if k == len(pat):
            yield i - k + 1            # match start
            k = fail[k - 1]</code>''',
 'template_notes': 'Rabin-Karp rolling hash: <code>h = (h·B + new − old·Bᵐ) mod P</code> — O(1) per slide; verify hash hits by direct compare (collisions). Periodicity: s repeats iff <code>len(s) % (len(s) − fail[-1]) == 0</code> with fail[-1] &gt; 0.',
 'complexity': 'KMP O(n+m) time, O(m) space; Rabin-Karp O(n+m) average; Manacher O(n). Against naive O(n·m) — state the gap, it\'s the motivation.',
 'mistakes': ['Failure table "proper prefix" — the whole string never counts as its own border.',
              'Rabin-Karp trusting hash equality without verifying — collisions exist.',
              'Rolling hash without modular care — huge numbers or biased collisions.',
              'Reaching for KMP when <code>text.find(pat)</code> or a window suffices — know when it\'s overkill (then say why you know KMP anyway).']},
}
