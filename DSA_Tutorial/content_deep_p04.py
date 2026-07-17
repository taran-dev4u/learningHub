# Deep tutorials — Pattern P4: Tree Traversal (DFS & BFS) (Session 4).
# Original teaching content. Keyed by LC number; merged as (4, lc). [[nn]] -> links.
# Node convention: class TreeNode: val, left, right.

DEEP = {

# ============================================================ LC 102 — Binary Tree Level Order Traversal
102: '''
<h2>🧭 How to think about it</h2>
<p>Return the node values grouped level by level, top to bottom. "Level by level" is the signature of <strong>breadth-first search (BFS)</strong> with a queue. The one trick that makes levels come out cleanly: at the start of each round, <em>freeze the current queue size</em> — that many nodes are exactly one level.</p>

<h2>🐢 Brute force first</h2>
<p>You could find the height, then loop depth 0..h and DFS collecting nodes at each depth — O(n·h). A single BFS pass does it in O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> a queue naturally holds one level at a time if you drain exactly <code>len(queue)</code> nodes per round, enqueuing their children for the next round. Snapshot that length <em>before</em> the inner loop so newly added children don't bleed into the current level.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Put the root in a queue (skip if the tree is empty).</li>
<li>While the queue isn't empty: record <code>size = len(queue)</code>.</li>
<li>Pop <code>size</code> nodes, collect their values, enqueue their non-null children.</li>
<li>Append the collected values as one level.</li>
</ol>

<h2>🎞️ Visual dry run — tree [3,9,20,null,null,15,7]</h2>
<pre class="viz">queue=[3]  size1 → level [3]; enqueue 9,20
queue=[9,20] size2 → level [9,20]; enqueue 15,7
queue=[15,7] size2 → level [15,7]
Result: [[3],[9,20],[15,7]]</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>from collections import deque
def levelOrder(root):
    if not root:
        return []
    res, q = [], deque([root])
    while q:
        size = len(q)              # freeze this level's count
        level = []
        for _ in range(size):
            node = q.popleft()
            level.append(node.val)
            if node.left:  q.append(node.left)
            if node.right: q.append(node.right)
        res.append(level)
    return res</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — each node enqueued and dequeued once. <strong>Space O(n)</strong> — the queue holds up to a full level (up to n/2 nodes).</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Empty tree → return <code>[]</code>.</li>
<li>Single node → <code>[[val]]</code>.</li>
<li>Skewed tree → each level has one node.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Not snapshotting <code>len(q)</code> — children get mixed into the current level.</li>
<li>Enqueuing null children → crashes when popped.</li>
<li>Using a list with <code>pop(0)</code> (O(n)) instead of a deque.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Bottom-up order → reverse the result.</li>
<li>Zigzag order ([[103]]); right-side view ([[199]]); per-level max ([[515]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[103]] · [[199]] · [[515]]</p>
''',

# ============================================================ LC 103 — Binary Tree Zigzag Level Order Traversal
103: '''
<h2>🧭 How to think about it</h2>
<p>Same level-order BFS, but alternate direction: level 0 left-to-right, level 1 right-to-left, and so on. The cleanest way is to do a normal BFS and simply <strong>reverse every other level's list</strong> before appending it.</p>

<h2>🐢 Brute force first</h2>
<p>Full level-order then post-process reversals — that's essentially the answer. Trying to reverse the traversal order itself with a stack works too but is fiddlier.</p>

<div class="insight">💡 <strong>Key insight:</strong> BFS still visits left-to-right; keep a boolean <code>left_to_right</code> that flips each level. When it's false, reverse the collected level (or build it with <code>appendleft</code> into a deque) before adding it to the result.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Standard level-order BFS with a frozen level size.</li>
<li>Track a direction flag; append the level as-is or reversed.</li>
<li>Flip the flag each level.</li>
</ol>

<h2>🎞️ Visual dry run — [3,9,20,null,null,15,7]</h2>
<pre class="viz">level0 [3] (L→R)
level1 [9,20] → reversed [20,9] (R→L)
level2 [15,7] (L→R)
Result: [[3],[20,9],[15,7]]</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>from collections import deque
def zigzagLevelOrder(root):
    if not root:
        return []
    res, q, left_to_right = [], deque([root]), True
    while q:
        level = deque()
        for _ in range(len(q)):
            node = q.popleft()
            if left_to_right:
                level.append(node.val)
            else:
                level.appendleft(node.val)   # build reversed cheaply
            if node.left:  q.append(node.left)
            if node.right: q.append(node.right)
        res.append(list(level))
        left_to_right = not left_to_right
    return res</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — one BFS; <code>appendleft</code> keeps each level O(width). <strong>Space O(n)</strong> for the queue.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Empty tree → <code>[]</code>.</li>
<li>Single node → <code>[[val]]</code>.</li>
<li>Two levels → the second is reversed.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Reversing the traversal (visiting children right-first) and getting the child order wrong on the next level.</li>
<li>Forgetting to flip the direction flag.</li>
<li>Reversing with <code>list[::-1]</code> every level when <code>appendleft</code> is cleaner.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Spiral by column instead of row → vertical traversal ([[987]]).</li>
<li>Standard level order ([[102]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[102]] · [[199]] · [[515]]</p>
''',

# ============================================================ LC 116 — Populating Next Right Pointers in Each Node
116: '''
<h2>🧭 How to think about it</h2>
<p>The tree is <em>perfect</em> (every parent has two children, all leaves on the same level). Wire each node's <code>next</code> to the node on its right within the same level; the rightmost points to null. Because it's perfect, you can do this with <strong>O(1) extra space</strong> using the <code>next</code> pointers you're building as a same-level linked list.</p>

<h2>🐢 Brute force first</h2>
<p>BFS level by level, linking consecutive nodes — O(n) time but O(n) queue space. The pointer-threading trick removes the queue.</p>

<div class="insight">💡 <strong>Key insight:</strong> once a level is fully linked, you can walk it left-to-right via <code>next</code> and link the level below: for each node, <code>node.left.next = node.right</code>, and <code>node.right.next = node.next.left</code> (the next parent's left child). Perfectness guarantees those children exist.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Start <code>leftmost = root</code>.</li>
<li>While <code>leftmost.left</code> exists (there's a level below): walk the current level via <code>next</code>.</li>
<li>For each <code>node</code>: <code>node.left.next = node.right</code>; if <code>node.next</code>, <code>node.right.next = node.next.left</code>.</li>
<li>Drop to <code>leftmost = leftmost.left</code>.</li>
</ol>

<h2>🎞️ Visual dry run — perfect tree 1 / 2 3 / 4 5 6 7</h2>
<pre class="viz">level1: 1→null
link level2: 2.next=3, 3.next=null
link level3 via level2: 4→5 (2.left→2.right), 5→6 (2.right→3.left), 6→7
Result: each level threaded left→right</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def connect(root):
    leftmost = root
    while leftmost and leftmost.left:      # while a lower level exists
        node = leftmost
        while node:                        # walk current level via next
            node.left.next = node.right    # link the two children
            if node.next:
                node.right.next = node.next.left  # bridge across parents
            node = node.next
        leftmost = leftmost.left
    return root</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — each node visited once. <strong>Space O(1)</strong> — no queue; the <code>next</code> links are the scaffolding.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Empty tree → return null.</li>
<li>Single node → its <code>next</code> stays null.</li>
<li>Leaf level → the outer loop stops (<code>leftmost.left</code> is null).</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Assuming the general-tree version ([[117]]) is identical — here perfectness lets you dereference both children freely.</li>
<li>Forgetting the cross-parent link <code>node.right.next = node.next.left</code>.</li>
<li>Using a queue and losing the O(1)-space credit.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Any (non-perfect) binary tree ([[117]]) → track the next level's head/tail as you go.</li>
<li>Level-order traversal ([[102]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[117]] · [[102]] · [[199]]</p>
''',

# ============================================================ LC 117 — Populating Next Right Pointers in Each Node II
117: '''
<h2>🧭 How to think about it</h2>
<p>Same goal — thread each level with <code>next</code> — but now the tree can be <em>any</em> shape, so a node may have zero, one, or two children. You can't assume neighbors exist. The O(1)-space fix: as you walk the current (already-threaded) level, build the next level as a linked list using a <strong>dummy head</strong> and a moving <code>tail</code>.</p>

<h2>🐢 Brute force first</h2>
<p>Level-order BFS linking neighbors — O(n) time, O(n) space. The dummy-head threading keeps O(1) space.</p>

<div class="insight">💡 <strong>Key insight:</strong> a <code>dummy</code> node's <code>next</code> will point at the start of the level below; a <code>tail</code> pointer appends each child in order as you scan the current level via <code>next</code>. Whatever children exist get linked; gaps are handled automatically.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>cur = root</code> (head of the current level).</li>
<li>For each level: make a fresh <code>dummy</code>; <code>tail = dummy</code>.</li>
<li>Walk <code>cur</code> via <code>next</code>; append each existing child to <code>tail</code>.</li>
<li>Move down: <code>cur = dummy.next</code>.</li>
</ol>

<h2>🎞️ Visual dry run — 1 / 2 3 / 4 _ _ 7</h2>
<pre class="viz">level1: 1
build level2: tail links 2, then 3 → 2.next=3
build level3 from 2,3: 4 (2.left), then 7 (3.right) → 4.next=7
Result: 2→3, 4→7</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def connect(root):
    cur = root
    while cur:
        dummy = Node(0)            # sentinel before the next level
        tail = dummy
        while cur:                 # walk current level via next
            if cur.left:
                tail.next = cur.left; tail = tail.next
            if cur.right:
                tail.next = cur.right; tail = tail.next
            cur = cur.next
        cur = dummy.next           # descend to the level we just built
    return root</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — one visit per node. <strong>Space O(1)</strong> — a dummy and a tail pointer, no queue.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Empty tree → null.</li>
<li>Nodes with a single child → only that child is appended.</li>
<li>Last level → <code>dummy.next</code> becomes null, loop ends.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Reusing the [[116]] logic that assumes both children exist.</li>
<li>Forgetting to reset <code>dummy</code>/<code>tail</code> each level.</li>
<li>Not advancing <code>cur = cur.next</code> inside the inner loop.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Perfect tree special case ([[116]]).</li>
<li>Right-side view ([[199]]) is the last node of each threaded level.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[116]] · [[199]] · [[102]]</p>
''',

# ============================================================ LC 199 — Binary Tree Right Side View
199: '''
<h2>🧭 How to think about it</h2>
<p>Standing to the right of the tree, you see the <strong>last node of each level</strong>. So run level-order BFS and grab the final node of every level. (A right-first DFS that records the first node seen at each new depth works too.)</p>

<h2>🐢 Brute force first</h2>
<p>Collect all levels then take each level's last element — same cost as BFS. The direct approach just records the last node inline.</p>

<div class="insight">💡 <strong>Key insight:</strong> in level-order BFS, the node processed when the inner counter hits the last index of the level is the rightmost visible node. Append it and move on.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>BFS with a frozen level size.</li>
<li>Within the level loop, when <code>i == size − 1</code>, append that node's value.</li>
<li>Enqueue children as usual.</li>
</ol>

<h2>🎞️ Visual dry run — [1,2,3,null,5,null,4]</h2>
<pre class="viz">level0 [1] → see 1
level1 [2,3] → see 3
level2 [5,4] → see 4
Result: [1,3,4]</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>from collections import deque
def rightSideView(root):
    if not root:
        return []
    res, q = [], deque([root])
    while q:
        size = len(q)
        for i in range(size):
            node = q.popleft()
            if i == size - 1:          # rightmost of this level
                res.append(node.val)
            if node.left:  q.append(node.left)
            if node.right: q.append(node.right)
    return res</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong>, <strong>Space O(n)</strong> for the queue.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Empty tree → <code>[]</code>.</li>
<li>Left-only tree → every left node is the rightmost of its level.</li>
<li>Single node → <code>[val]</code>.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Taking <code>node.right</code> as the answer — a level's rightmost visible node may be a left child.</li>
<li>DFS that records the last (not first) node per depth when going right-first.</li>
<li>Off-by-one on <code>size − 1</code>.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Left side view → first node of each level.</li>
<li>Per-level max/sum ([[515]], [[1161]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[102]] · [[515]] · [[117]]</p>
''',

# ============================================================ LC 314 — Binary Tree Vertical Order Traversal
314: '''
<h2>🧭 How to think about it</h2>
<p>Group nodes by <strong>column</strong>: root is column 0, a left child is <code>col − 1</code>, a right child is <code>col + 1</code>. Within a column, nodes appear top-to-bottom, and (for ties at the same position) left-to-right — which is exactly what BFS gives you. Bucket node values by column, then read columns left to right.</p>

<h2>🐢 Brute force first</h2>
<p>DFS collecting (col, row) then sorting is possible, but BFS avoids a sort for this problem's tie rule: same column, same row ties keep left-before-right insertion order.</p>

<div class="insight">💡 <strong>Key insight:</strong> BFS carries a column index alongside each node. Append values into <code>columns[col]</code> in BFS order (top-down, left-right). Track the min and max column so you can output them in order without sorting keys.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Queue holds <code>(node, col)</code>, starting at <code>(root, 0)</code>.</li>
<li>Append <code>node.val</code> to <code>columns[col]</code>; enqueue <code>(left, col−1)</code>, <code>(right, col+1)</code>.</li>
<li>Track <code>min_col</code>/<code>max_col</code>; output columns from min to max.</li>
</ol>

<h2>🎞️ Visual dry run — [3,9,20,null,null,15,7]</h2>
<pre class="viz">3@0 ; 9@-1 ; 20@1 ; 15@0 ; 7@2
columns: -1:[9] 0:[3,15] 1:[20] 2:[7]
Result: [[9],[3,15],[20],[7]]</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>from collections import deque, defaultdict
def verticalOrder(root):
    if not root:
        return []
    columns = defaultdict(list)
    q = deque([(root, 0)])
    min_col = max_col = 0
    while q:
        node, col = q.popleft()
        columns[col].append(node.val)       # BFS order = top-down, left-right
        min_col = min(min_col, col)
        max_col = max(max_col, col)
        if node.left:  q.append((node.left, col - 1))
        if node.right: q.append((node.right, col + 1))
    return [columns[c] for c in range(min_col, max_col + 1)]</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — no sorting needed. <strong>Space O(n)</strong> for the queue and buckets.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Empty tree → <code>[]</code>.</li>
<li>All left children → columns spread negative.</li>
<li>Ties at same (col,row) → BFS keeps left-before-right.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Using DFS, which can violate the top-down order within a column.</li>
<li>Sorting by column value with a dict but forgetting negative indices.</li>
<li>Confusing this with [[987]], which additionally sorts same-position values.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Strict LeetCode 987 rule: sort ties by value ([[987]]).</li>
<li>Diagonal traversal → col = row − depth style indexing.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[987]] · [[102]] · [[103]]</p>
''',

# ============================================================ LC 515 — Find Largest Value in Each Tree Row
515: '''
<h2>🧭 How to think about it</h2>
<p>Report the maximum value on each level. Run level-order BFS and, for each level, keep a running max over the nodes you pop.</p>

<h2>🐢 Brute force first</h2>
<p>Collect every level's list then take <code>max</code> of each — the same work. Tracking the max inline avoids storing whole levels.</p>

<div class="insight">💡 <strong>Key insight:</strong> the level boundary (frozen <code>len(queue)</code>) lets you reduce each level to a single number as you go, so you never need the full level list.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>BFS with a frozen level size.</li>
<li>Start <code>level_max = −∞</code>; update it as you pop each node.</li>
<li>Append <code>level_max</code> after the level completes.</li>
</ol>

<h2>🎞️ Visual dry run — [1,3,2,5,3,null,9]</h2>
<pre class="viz">level0 [1] → 1
level1 [3,2] → 3
level2 [5,3,9] → 9
Result: [1,3,9]</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>from collections import deque
def largestValues(root):
    if not root:
        return []
    res, q = [], deque([root])
    while q:
        level_max = float('-inf')
        for _ in range(len(q)):
            node = q.popleft()
            level_max = max(level_max, node.val)
            if node.left:  q.append(node.left)
            if node.right: q.append(node.right)
        res.append(level_max)
    return res</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong>, <strong>Space O(n)</strong> for the queue.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Empty tree → <code>[]</code>.</li>
<li>Negative values → seed with <code>−∞</code>, not 0.</li>
<li>Single node → <code>[val]</code>.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Initializing <code>level_max = 0</code> and breaking on all-negative trees.</li>
<li>Not freezing the level size.</li>
<li>Storing whole levels unnecessarily.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Largest-sum level ([[1161]]).</li>
<li>Per-level average / min → swap the reducer.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[1161]] · [[102]] · [[199]]</p>
''',

# ============================================================ LC 545 — Boundary of Binary Tree
545: '''
<h2>🧭 How to think about it</h2>
<p>Walk the tree's outline counter-clockwise: the root, then the <strong>left boundary</strong> (top-down, excluding leaves), then <strong>all leaves</strong> left-to-right, then the <strong>right boundary</strong> (bottom-up, excluding leaves). Collecting these three pieces carefully — without double-counting leaves or the root — is the whole problem.</p>

<h2>🐢 Brute force first</h2>
<p>There's no shortcut; you must identify three groups. The care is in definitions: a leaf is neither a left- nor right-boundary node, and the root is added once.</p>

<div class="insight">💡 <strong>Key insight:</strong> split into three helper walks. Left boundary: follow left (or right if no left), adding non-leaf nodes top-down. Leaves: a DFS adding nodes with no children, left-to-right. Right boundary: follow right (or left), adding non-leaf nodes, then reverse for bottom-up order.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Add the root (if not a leaf).</li>
<li>Collect the left boundary (exclude leaves), top-down.</li>
<li>Collect all leaves left-to-right.</li>
<li>Collect the right boundary (exclude leaves), then reverse.</li>
</ol>

<h2>🎞️ Visual dry run — root 1, left spine 2→4, leaves 4,5,6, right spine 3</h2>
<pre class="viz">root: 1
left boundary (non-leaf): 2
leaves L→R: 4,5,6
right boundary (non-leaf, reversed): 3
Result: [1,2,4,5,6,3]</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def boundaryOfBinaryTree(root):
    if not root:
        return []
    def is_leaf(n): return not n.left and not n.right
    res = [root.val] if not is_leaf(root) else [root.val]

    # left boundary (exclude leaves)
    left = []
    n = root.left
    while n:
        if not is_leaf(n): left.append(n.val)
        n = n.left if n.left else n.right

    # leaves, left to right
    leaves = []
    def dfs(n):
        if not n: return
        if is_leaf(n): leaves.append(n.val); return
        dfs(n.left); dfs(n.right)
    if not is_leaf(root):
        dfs(root)

    # right boundary (exclude leaves), collected then reversed
    right = []
    n = root.right
    while n:
        if not is_leaf(n): right.append(n.val)
        n = n.right if n.right else n.left

    return res + left + leaves + right[::-1]</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — a few linear walks. <strong>Space O(h)</strong> recursion for the leaf DFS.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Single node → just the root.</li>
<li>Root with only one subtree → the missing side contributes nothing.</li>
<li>Avoid adding a leaf twice (it belongs only to the leaves group).</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Double-counting leaves that also sit on a boundary spine.</li>
<li>Forgetting to reverse the right boundary.</li>
<li>Adding the root inside the boundary walks too.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Clockwise boundary → mirror the piece order.</li>
<li>Perimeter of a grid island → analogous outline idea.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[199]] · [[257]] · [[102]]</p>
''',

# ============================================================ LC 662 — Maximum Width of Binary Tree
662: '''
<h2>🧭 How to think about it</h2>
<p>Width of a level = distance between its leftmost and rightmost <em>positions</em>, counting the null gaps in between as if the tree were a complete binary tree. Give each node a <strong>heap-style index</strong> (root = 0; left child = <code>2i</code>, right child = <code>2i+1</code>) and, per level, the width is <code>last_index − first_index + 1</code>.</p>

<h2>🐢 Brute force first</h2>
<p>Materializing a complete array with nulls blows up exponentially for skewed trees. Indexing only the real nodes keeps it O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> BFS carrying each node's positional index. The first node popped in a level gives <code>first</code>; the last gives <code>last</code>; width = <code>last − first + 1</code>. Normalize indices per level (subtract the level's first index) to avoid overflow in fixed-width languages.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Queue holds <code>(node, index)</code>, root at index 0.</li>
<li>Per level: record the first and last indices; update the best width.</li>
<li>Enqueue children with indices <code>2i</code> and <code>2i+1</code>.</li>
</ol>

<h2>🎞️ Visual dry run — [1,3,2,5,3,null,9]</h2>
<pre class="viz">level0: idx0 → width 1
level1: 3@0, 2@1 → width 2
level2: 5@0,3@1,9@3 → width 3-0+1 = 4
Answer: 4</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>from collections import deque
def widthOfBinaryTree(root):
    if not root:
        return 0
    best = 0
    q = deque([(root, 0)])
    while q:
        first = q[0][1]                 # leftmost index this level
        for _ in range(len(q)):
            node, idx = q.popleft()
            idx -= first                # normalize to prevent overflow
            best = max(best, idx + 1)
            if node.left:  q.append((node.left, 2 * idx))
            if node.right: q.append((node.right, 2 * idx + 1))
    return best</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — one BFS. <strong>Space O(n)</strong> for the queue.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Single node → width 1.</li>
<li>Skewed tree → each level width 1 (indices normalized).</li>
<li>Large deep trees → normalization prevents index blow-up.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Not normalizing indices → overflow / huge numbers in some languages.</li>
<li>Counting nodes instead of positions (nulls between count).</li>
<li>Computing width as <code>last − first</code> without the <code>+1</code>.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Max width by actual node count → different (and easier) metric.</li>
<li>Vertical width ([[987]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[102]] · [[199]] · [[987]]</p>
''',

# ============================================================ LC 987 — Vertical Order Traversal of a Binary Tree
987: '''
<h2>🧭 How to think about it</h2>
<p>Like vertical order ([[314]]), but with a stricter tie rule: order columns left→right, within a column top→bottom by row, and — crucially — when two nodes share the <em>same</em> (row, column), order them by <strong>value</strong>. That extra tiebreak means you must record <code>(col, row, val)</code> for every node and sort.</p>

<h2>🐢 Brute force first</h2>
<p>Plain BFS bucketing (as in 314) fails the same-cell value tiebreak. Collect all triples and sort — O(n log n), clean and correct.</p>

<div class="insight">💡 <strong>Key insight:</strong> DFS or BFS to gather <code>(col, row, val)</code> for each node (root at row 0, col 0; children at row+1 and col∓1). Sort by <code>(col, row, val)</code>; then group consecutive equal columns into output lists.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Traverse recording <code>(col, row, val)</code>.</li>
<li>Sort the list by <code>(col, row, val)</code>.</li>
<li>Group by <code>col</code>, emitting the values in sorted order.</li>
</ol>

<h2>🎞️ Visual dry run — [3,9,20,null,null,15,7]</h2>
<pre class="viz">triples: (0,0,3)(-1,1,9)(1,1,20)(0,2,15)(2,2,7)
sort by (col,row,val): col-1:[9] col0:[3,15] col1:[20] col2:[7]
Result: [[9],[3,15],[20],[7]]</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def verticalTraversal(root):
    nodes = []                                   # (col, row, val)
    def dfs(node, row, col):
        if not node: return
        nodes.append((col, row, node.val))
        dfs(node.left, row + 1, col - 1)
        dfs(node.right, row + 1, col + 1)
    dfs(root, 0, 0)
    nodes.sort()                                 # by col, then row, then val
    from itertools import groupby
    return [[v for _, _, v in group]
            for _, group in groupby(nodes, key=lambda t: t[0])]</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n log n)</strong> — dominated by the sort. <strong>Space O(n)</strong> for the triples.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Two nodes at the same (row, col) → smaller value first.</li>
<li>Single node → <code>[[val]]</code>.</li>
<li>Negative columns → handled by sorting.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Reusing the BFS-bucket approach from [[314]] and failing the value tiebreak.</li>
<li>Sorting by only (col, row) and leaving equal cells in traversal order.</li>
<li>Forgetting to group consecutive equal columns.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Looser tie rule → [[314]].</li>
<li>Diagonal traversal → different indexing.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[314]] · [[102]] · [[103]]</p>
''',

# ============================================================ LC 1161 — Maximum Level Sum of a Binary Tree
1161: '''
<h2>🧭 How to think about it</h2>
<p>Find the level (1-indexed, root = level 1) whose values sum to the most; ties go to the smallest level number. Level-order BFS, summing each level, tracking the best sum and the level that produced it.</p>

<h2>🐢 Brute force first</h2>
<p>Compute all level sums then take the argmax — same cost. Doing it inline avoids storing all sums.</p>

<div class="insight">💡 <strong>Key insight:</strong> because BFS processes levels top-down and you only update <code>best</code> on a <em>strictly greater</em> sum, the first (smallest-numbered) level wins ties automatically.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>BFS by level, counting the level number.</li>
<li>Sum each level; if it exceeds the current best, record the sum and level.</li>
<li>Return the best level number.</li>
</ol>

<h2>🎞️ Visual dry run — [1,7,0,7,-8]</h2>
<pre class="viz">level1: 1 → best=1 @L1
level2: 7+0=7 → best=7 @L2
level3: 7+(-8)=-1 → no change
Answer: 2</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>from collections import deque
def maxLevelSum(root):
    best_sum = float('-inf')
    best_level = 1
    level = 0
    q = deque([root])
    while q:
        level += 1
        s = 0
        for _ in range(len(q)):
            node = q.popleft()
            s += node.val
            if node.left:  q.append(node.left)
            if node.right: q.append(node.right)
        if s &gt; best_sum:                # strict &gt; keeps the earliest level on ties
            best_sum, best_level = s, level
    return best_level</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong>, <strong>Space O(n)</strong> for the queue.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>All negative values → seed best with <code>−∞</code>.</li>
<li>Single node → level 1.</li>
<li>Ties → the earlier level wins via strict <code>&gt;</code>.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Using <code>≥</code> and returning a later level on ties.</li>
<li>0-indexing levels when the problem is 1-indexed.</li>
<li>Initializing best sum to 0.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Max level by average → divide by level count.</li>
<li>Per-level max value ([[515]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[515]] · [[102]] · [[199]]</p>
''',

# ============================================================ LC 100 — Same Tree
100: '''
<h2>🧭 How to think about it</h2>
<p>Two trees are identical when their roots match <em>and</em> their left subtrees match <em>and</em> their right subtrees match. That self-referential definition is a textbook <strong>recursion</strong>: compare the current pair, then recurse on both child pairs.</p>

<h2>🐢 Brute force first</h2>
<p>Serialize both and compare strings — O(n) but allocates. Direct structural recursion is O(n) with no serialization.</p>

<div class="insight">💡 <strong>Key insight:</strong> base cases first — both null → equal; exactly one null or values differ → not equal. Otherwise the answer is <code>same(left, left) and same(right, right)</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>If both nodes are null → True.</li>
<li>If one is null or values differ → False.</li>
<li>Return the AND of the left-subtree and right-subtree comparisons.</li>
</ol>

<h2>🎞️ Visual dry run — p=[1,2,3], q=[1,2,3]</h2>
<pre class="viz">1==1 → compare (2,2) and (3,3)
2==2 → (null,null)✓ (null,null)✓ → True
3==3 → True
Overall True</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def isSameTree(p, q):
    if not p and not q:
        return True                 # both empty → identical
    if not p or not q or p.val != q.val:
        return False                # shape or value mismatch
    return isSameTree(p.left, q.left) and isSameTree(p.right, q.right)</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — visits each node pair once. <strong>Space O(h)</strong> recursion stack.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Both empty → True.</li>
<li>One empty → False.</li>
<li>Same values, different shapes → caught by the one-null check.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Checking values before the null cases → crashes on <code>None.val</code>.</li>
<li>Comparing only values and ignoring structure.</li>
<li>Using <code>==</code> on nodes instead of <code>.val</code>.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Symmetric (mirror) check ([[101]]).</li>
<li>Is one a subtree of another ([[572]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[101]] · [[572]] · [[226]]</p>
''',

# ============================================================ LC 101 — Symmetric Tree
101: '''
<h2>🧭 How to think about it</h2>
<p>A tree is a mirror of itself when its left subtree is the mirror image of its right subtree. So compare two nodes in <strong>mirror</strong>: outer with outer, inner with inner — <code>left.left</code> vs <code>right.right</code> and <code>left.right</code> vs <code>right.left</code>.</p>

<h2>🐢 Brute force first</h2>
<p>Do a level-order BFS and check each level reads as a palindrome (with null placeholders) — works but bookkeeping-heavy. The mirror recursion is cleaner.</p>

<div class="insight">💡 <strong>Key insight:</strong> write a helper <code>mirror(a, b)</code>: both null → True; one null or values differ → False; else <code>mirror(a.left, b.right) and mirror(a.right, b.left)</code>. Call it on the root's two children.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Empty tree → symmetric.</li>
<li>Call <code>mirror(root.left, root.right)</code>.</li>
<li>In <code>mirror</code>, compare outer and inner pairs recursively.</li>
</ol>

<h2>🎞️ Visual dry run — [1,2,2,3,4,4,3]</h2>
<pre class="viz">mirror(2,2): vals equal
  mirror(3,3) outer ✓
  mirror(4,4) inner ✓
→ symmetric True</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def isSymmetric(root):
    def mirror(a, b):
        if not a and not b:
            return True
        if not a or not b or a.val != b.val:
            return False
        return mirror(a.left, b.right) and mirror(a.right, b.left)
    return mirror(root.left, root.right) if root else True</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong>, <strong>Space O(h)</strong> recursion.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Empty tree → symmetric.</li>
<li>Single node → symmetric.</li>
<li>Same values but wrong shape → caught by the null mismatch.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Comparing <code>left.left</code> with <code>right.left</code> (that's the "same tree" check, not the mirror).</li>
<li>Dereferencing before null checks.</li>
<li>Forgetting the empty-tree case.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Iterative version with a queue of pairs.</li>
<li>Same tree ([[100]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[100]] · [[226]] · [[572]]</p>
''',

# ============================================================ LC 105 — Construct Binary Tree from Preorder and Inorder Traversal
105: '''
<h2>🧭 How to think about it</h2>
<p>Rebuild the tree from its preorder and inorder lists. <strong>Preorder's first element is always the root.</strong> Find that root inside inorder: everything to its left is the left subtree, everything to its right is the right subtree. Recurse on those slices.</p>

<h2>🐢 Brute force first</h2>
<p>Slicing arrays and doing <code>index()</code> each call is O(n²). A hash map from value→inorder-index plus a moving preorder pointer gives O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> consume preorder left-to-right (each call takes the next value as a root). Use a precomputed <code>value → inorder index</code> map to split in O(1), and pass inorder index bounds instead of slicing.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Map each value to its index in inorder.</li>
<li>Keep a global preorder pointer; each call pops the next root.</li>
<li>Build left subtree from the inorder range left of the root, then the right range.</li>
</ol>

<h2>🎞️ Visual dry run — preorder [3,9,20,15,7], inorder [9,3,15,20,7]</h2>
<pre class="viz">root 3 → inorder split: left [9] | right [15,20,7]
 left root 9 (leaf)
 right root 20 → left [15], right [7]
Reconstructed: 3(9, 20(15,7))</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def buildTree(preorder, inorder):
    idx = {v: i for i, v in enumerate(inorder)}   # value → inorder index
    self_pre = [0]                                 # preorder cursor
    def build(lo, hi):
        if lo &gt; hi:
            return None
        root_val = preorder[self_pre[0]]
        self_pre[0] += 1
        root = TreeNode(root_val)
        mid = idx[root_val]
        root.left = build(lo, mid - 1)             # left subtree first (preorder)
        root.right = build(mid + 1, hi)
        return root
    return build(0, len(inorder) - 1)</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — each node built once, O(1) split. <strong>Space O(n)</strong> for the map and recursion.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Empty input → empty tree.</li>
<li>Single node → root only.</li>
<li>All-left or all-right skew → still O(n) with the map.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Building the right subtree before the left (preorder demands left first, since the cursor advances).</li>
<li>Re-scanning inorder with <code>index()</code> each call → O(n²).</li>
<li>Off-by-one in the inorder bounds.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Inorder + postorder ([[106]]) — consume postorder from the right, build right subtree first.</li>
<li>Preorder + postorder → not always unique.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[106]] · [[94]] · [[114]]</p>
''',

# ============================================================ LC 110 — Balanced Binary Tree
110: '''
<h2>🧭 How to think about it</h2>
<p>A tree is height-balanced if, at <em>every</em> node, the left and right subtree heights differ by at most 1. Computing height separately at each node is wasteful; instead compute height <strong>bottom-up</strong> and let a special sentinel value signal "already unbalanced" so it bubbles straight to the top.</p>

<h2>🐢 Brute force first</h2>
<p>For each node call a height function on both subtrees and compare → O(n²) on skewed trees. A single postorder pass that returns height (or a poison value) is O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> a postorder helper returns the subtree height, but returns <code>−1</code> the moment it detects imbalance. Any parent seeing <code>−1</code> from a child immediately returns <code>−1</code> too, short-circuiting the rest.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Recurse to leaves; a null returns height 0.</li>
<li>Get left and right heights; if either is <code>−1</code> or they differ by &gt; 1, return <code>−1</code>.</li>
<li>Otherwise return <code>1 + max(left, right)</code>.</li>
<li>Balanced iff the root call isn't <code>−1</code>.</li>
</ol>

<h2>🎞️ Visual dry run — [3,9,20,null,null,15,7]</h2>
<pre class="viz">heights: 9→1, 15→1, 7→1, 20→2, root→3
no node has children differing by &gt;1 → balanced True</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def isBalanced(root):
    def height(node):
        if not node:
            return 0
        lh = height(node.left)
        if lh == -1: return -1          # left already unbalanced
        rh = height(node.right)
        if rh == -1: return -1
        if abs(lh - rh) &gt; 1:
            return -1                    # this node is unbalanced
        return 1 + max(lh, rh)
    return height(root) != -1</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — one postorder pass. <strong>Space O(h)</strong> recursion.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Empty tree → balanced.</li>
<li>Single node → balanced.</li>
<li>Long skew → detected as unbalanced early.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Recomputing height top-down → O(n²).</li>
<li>Forgetting to propagate the <code>−1</code> poison up.</li>
<li>Checking balance only at the root.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Return the height too → drop the sentinel and pass a mutable flag.</li>
<li>Diameter uses the same height recursion ([[543]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[104]] · [[543]] · [[124]]</p>
''',

# ============================================================ LC 112 — Path Sum
112: '''
<h2>🧭 How to think about it</h2>
<p>Is there a root-to-<em>leaf</em> path whose values add up to a target? Walk down, subtracting each node's value from the target you still need; at a <strong>leaf</strong>, success means the remaining target equals the leaf's value (i.e., it hits zero exactly).</p>

<h2>🐢 Brute force first</h2>
<p>Enumerate every root-to-leaf path and sum it → still O(n) here since each node is on paths, but carrying a running remainder is simplest and O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> subtract as you descend. The answer is True at a leaf when the remaining target is 0. Recurse into whichever children exist, OR-ing their results.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Null node → False.</li>
<li>Leaf → return <code>target − node.val == 0</code>.</li>
<li>Otherwise recurse left/right with <code>target − node.val</code>, returning their OR.</li>
</ol>

<h2>🎞️ Visual dry run — target 22, path 5→4→11→2</h2>
<pre class="viz">need 22 at 5 → 17 at 4 → 6 at 11 → 2 at leaf 2 ; 2==remaining 2 → True</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def hasPathSum(root, targetSum):
    if not root:
        return False
    if not root.left and not root.right:      # leaf
        return targetSum == root.val
    remaining = targetSum - root.val
    return (hasPathSum(root.left, remaining) or
            hasPathSum(root.right, remaining))</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — visits each node once. <strong>Space O(h)</strong> recursion.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Empty tree → False (even if target is 0 — there's no leaf).</li>
<li>Negative values → subtraction still works.</li>
<li>Single node → True iff it equals the target.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Treating a node with one child as a leaf → must have <em>no</em> children.</li>
<li>Returning True at an internal node when the running sum hits target early.</li>
<li>Returning True for an empty tree with target 0.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Return all such paths ([[113]]).</li>
<li>Count paths anywhere summing to target ([[437]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[113]] · [[437]] · [[129]]</p>
''',

# ============================================================ LC 113 — Path Sum II
113: '''
<h2>🧭 How to think about it</h2>
<p>Now return <em>every</em> root-to-leaf path that sums to the target. This is <strong>backtracking</strong>: carry the current path down, and when you reach a leaf that completes the target, snapshot the path. Undo (pop) as you return so siblings start clean.</p>

<h2>🐢 Brute force first</h2>
<p>Collect all root-to-leaf paths, then filter by sum — fine but stores everything. Backtracking prunes nothing extra here but records only completed paths.</p>

<div class="insight">💡 <strong>Key insight:</strong> append the node to <code>path</code>, subtract from the remaining target, recurse; at a leaf that hits zero, append a <em>copy</em> of <code>path</code> to the results. Always <code>path.pop()</code> before returning so the shared list stays correct for siblings.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>DFS carrying a mutable <code>path</code> and remaining target.</li>
<li>At a leaf with remaining == node.val, record <code>path + [node]</code>.</li>
<li>Recurse into children; pop the node on the way back.</li>
</ol>

<h2>🎞️ Visual dry run — target 22, tree with paths 5→4→11→2 (=22) and 5→8→4→5 (=22)</h2>
<pre class="viz">descend 5,4,11,2 → sum 22 → record [5,4,11,2]
backtrack, descend 5,8,4,5 → sum 22 → record [5,8,4,5]
Result: [[5,4,11,2],[5,8,4,5]]</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def pathSum(root, targetSum):
    res, path = [], []
    def dfs(node, remaining):
        if not node:
            return
        path.append(node.val)
        remaining -= node.val
        if not node.left and not node.right and remaining == 0:
            res.append(path[:])          # snapshot a copy
        else:
            dfs(node.left, remaining)
            dfs(node.right, remaining)
        path.pop()                        # backtrack
    dfs(root, targetSum)
    return res</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n²)</strong> worst case — copying paths of length up to <code>h</code> for many leaves. <strong>Space O(h)</strong> recursion plus output.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>No qualifying path → empty list.</li>
<li>Empty tree → empty list.</li>
<li>Negative values → still handled by subtraction.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Appending <code>path</code> itself instead of a copy — later pops mutate it.</li>
<li>Forgetting to backtrack (<code>path.pop()</code>).</li>
<li>Recording at non-leaf nodes.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Existence only ([[112]]).</li>
<li>Paths not required to start/end at root/leaf ([[437]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[112]] · [[437]] · [[257]]</p>
''',

# ============================================================ LC 114 — Flatten Binary Tree to Linked List
114: '''
<h2>🧭 How to think about it</h2>
<p>Flatten the tree into a right-leaning "linked list" that follows <strong>preorder</strong>: each node's <code>left</code> becomes null and <code>right</code> points to the next preorder node. The slick O(1)-space method rewires pointers using a Morris-like trick — attach the left subtree between a node and its right subtree.</p>

<h2>🐢 Brute force first</h2>
<p>Collect preorder into a list, then relink — O(n) time, O(n) space. The pointer-rewiring version is O(1) extra space.</p>

<div class="insight">💡 <strong>Key insight:</strong> for each node with a left child, find that left subtree's <strong>rightmost node</strong> (its preorder-last), attach the current right subtree there, move the left subtree to the right, and null the left. Advancing to <code>node.right</code> continues the process.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>cur = root</code>.</li>
<li>If <code>cur.left</code> exists: find the rightmost node of the left subtree.</li>
<li>Point that rightmost node's <code>right</code> to <code>cur.right</code>; set <code>cur.right = cur.left</code>; <code>cur.left = None</code>.</li>
<li>Advance <code>cur = cur.right</code>.</li>
</ol>

<h2>🎞️ Visual dry run — [1,2,5,3,4,null,6]</h2>
<pre class="viz">at 1: left=2..(rightmost 4) ; 4.right=5 ; 1.right=2 ; 1.left=None
→ 1→2→3→4→5→6 (all via right)
Result: 1,2,3,4,5,6</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def flatten(root):
    cur = root
    while cur:
        if cur.left:
            # rightmost node of the left subtree (preorder predecessor of cur.right)
            runner = cur.left
            while runner.right:
                runner = runner.right
            runner.right = cur.right     # splice current right subtree after it
            cur.right = cur.left         # move left subtree to the right
            cur.left = None
        cur = cur.right</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — each node visited O(1) amortized (the runner walks edges once overall). <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Empty tree → nothing to do.</li>
<li>Right-only tree → already flattened.</li>
<li>Left-only tree → becomes a right chain.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Forgetting to null out <code>cur.left</code> after moving it.</li>
<li>Attaching the right subtree at the wrong node (must be the left subtree's rightmost).</li>
<li>Losing the original right subtree before splicing.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Reverse-preorder recursion updating a <code>prev</code> pointer.</li>
<li>Flatten to a doubly linked list in inorder (BST → DLL).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[105]] · [[94]] · [[430]]</p>
''',

# ============================================================ LC 129 — Sum Root to Leaf Numbers
129: '''
<h2>🧭 How to think about it</h2>
<p>Each root-to-leaf path spells a number (e.g., 1→2→3 is 123); sum all of them. Carry the number built <strong>so far</strong> down the tree: at each step it becomes <code>current × 10 + node.val</code>. At a leaf, that value is one complete number to add.</p>

<h2>🐢 Brute force first</h2>
<p>Collect all paths as digit lists, convert, sum — works but stores paths. Threading the running number through the recursion is O(n), no extra storage beyond the stack.</p>

<div class="insight">💡 <strong>Key insight:</strong> pass an accumulator <code>cur</code>. Descending multiplies by 10 and adds the digit. Leaves return <code>cur</code>; internal nodes return the sum of their children's contributions.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>DFS with <code>cur = cur*10 + node.val</code>.</li>
<li>At a leaf, return <code>cur</code>.</li>
<li>Otherwise return the sum over existing children.</li>
</ol>

<h2>🎞️ Visual dry run — [1,2,3]</h2>
<pre class="viz">1 → left: cur=12 (leaf) → 12 ; right: cur=13 (leaf) → 13
sum = 25</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def sumNumbers(root):
    def dfs(node, cur):
        if not node:
            return 0
        cur = cur * 10 + node.val        # extend the number by one digit
        if not node.left and not node.right:
            return cur                    # completed number
        return dfs(node.left, cur) + dfs(node.right, cur)
    return dfs(root, 0)</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong>, <strong>Space O(h)</strong> recursion.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Single node → the node's value.</li>
<li>Empty tree → 0.</li>
<li>Nodes with one child → not leaves; keep descending.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Adding <code>cur</code> at internal nodes, double-counting.</li>
<li>Treating a one-child node as a leaf.</li>
<li>Resetting <code>cur</code> instead of threading it down.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Binary digits / other bases → change the multiplier.</li>
<li>Smallest string from leaf ([[988]]) is a string analog.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[112]] · [[988]] · [[257]]</p>
''',

# ============================================================ LC 226 — Invert Binary Tree
226: '''
<h2>🧭 How to think about it</h2>
<p>Mirror the tree: every node's left and right children swap. Because inverting a tree means inverting both subtrees and swapping them, it's a one-line <strong>recursion</strong> — swap children, recurse into each.</p>

<h2>🐢 Brute force first</h2>
<p>BFS/DFS swapping children iteratively works and is O(n); the recursive form is the shortest.</p>

<div class="insight">💡 <strong>Key insight:</strong> at each node, swap <code>left</code> and <code>right</code>, then invert both subtrees (order doesn't matter). Nulls return immediately.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Null node → return null.</li>
<li>Swap <code>node.left</code> and <code>node.right</code>.</li>
<li>Recurse into both children; return the node.</li>
</ol>

<h2>🎞️ Visual dry run — [4,2,7,1,3,6,9]</h2>
<pre class="viz">swap at 4 → (7,2) ; swap at 2 → (3,1) ; swap at 7 → (9,6)
Result: [4,7,2,9,6,3,1]</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def invertTree(root):
    if not root:
        return None
    root.left, root.right = root.right, root.left   # swap children
    invertTree(root.left)
    invertTree(root.right)
    return root</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong>, <strong>Space O(h)</strong> recursion.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Empty tree → null.</li>
<li>Single node → unchanged.</li>
<li>Skewed tree → becomes skewed the other way.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Recursing before swapping and swapping the already-inverted children back.</li>
<li>Returning the wrong node.</li>
<li>Forgetting the null base case.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Iterative with a stack/queue.</li>
<li>Symmetric check ([[101]]) uses the mirror idea without mutating.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[101]] · [[100]] · [[104]]</p>
''',

# ============================================================ LC 257 — Binary Tree Paths
257: '''
<h2>🧭 How to think about it</h2>
<p>List every root-to-leaf path as a string like <code>"1-&gt;2-&gt;5"</code>. This is a <strong>DFS with backtracking</strong>: build up the path of values as you descend and, at each leaf, join and record it.</p>

<h2>🐢 Brute force first</h2>
<p>There's no cheaper approach — you must enumerate paths. The choice is between passing an accumulating string (simple) or a list you join at leaves (avoids repeated string concatenation).</p>

<div class="insight">💡 <strong>Key insight:</strong> carry a list <code>path</code>; append the node, and at a leaf join with <code>"-&gt;"</code> and store it; pop on the way back so siblings reuse the prefix cleanly.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>DFS appending each node's value to <code>path</code>.</li>
<li>At a leaf, add <code>"-&gt;".join(path)</code> to results.</li>
<li>Recurse into children, then pop.</li>
</ol>

<h2>🎞️ Visual dry run — [1,2,3,null,5]</h2>
<pre class="viz">1→2→5 leaf → "1-&gt;2-&gt;5"
1→3 leaf → "1-&gt;3"
Result: ["1-&gt;2-&gt;5","1-&gt;3"]</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def binaryTreePaths(root):
    res, path = [], []
    def dfs(node):
        if not node:
            return
        path.append(str(node.val))
        if not node.left and not node.right:
            res.append("-&gt;".join(path))
        else:
            dfs(node.left)
            dfs(node.right)
        path.pop()                       # backtrack
    if root:
        dfs(root)
    return res</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n·h)</strong> — building strings of length up to <code>h</code>. <strong>Space O(h)</strong> recursion plus output.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Single node → one path with just that value.</li>
<li>Empty tree → empty list.</li>
<li>One-child nodes → included in the path (not leaves).</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Forgetting to backtrack (<code>path.pop()</code>).</li>
<li>Recording at internal nodes.</li>
<li>Building strings with <code>+</code> at every node (quadratic churn).</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Sum of the path numbers ([[129]]).</li>
<li>Return paths that meet a condition ([[113]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[113]] · [[129]] · [[988]]</p>
''',

# ============================================================ LC 572 — Subtree of Another Tree
572: '''
<h2>🧭 How to think about it</h2>
<p>Is <code>subRoot</code> an exact subtree of <code>root</code>? At every node of <code>root</code>, ask "does the tree rooted here <em>equal</em> subRoot?" using the Same-Tree check. If any node matches, yes.</p>

<h2>🐢 Brute force first</h2>
<p>The node-by-node Same-Tree test is O(m·n) worst case. A serialization trick (compare with null markers, then substring-search) reaches O(m+n).</p>

<div class="insight">💡 <strong>Key insight:</strong> combine two recursions — an outer walk over <code>root</code> and an inner <code>isSameTree</code>. Return True if the current node matches subRoot, or if either child subtree contains it.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>If <code>root</code> is null → False (a non-null subRoot can't fit).</li>
<li>If <code>isSameTree(root, subRoot)</code> → True.</li>
<li>Else recurse into left or right.</li>
</ol>

<h2>🎞️ Visual dry run — root [3,4,5,1,2], subRoot [4,1,2]</h2>
<pre class="viz">at 3: same? no → check children
at 4: same as [4,1,2]? yes → True</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def isSubtree(root, subRoot):
    def same(a, b):
        if not a and not b: return True
        if not a or not b or a.val != b.val: return False
        return same(a.left, b.left) and same(a.right, b.right)

    if not root:
        return False
    if same(root, subRoot):
        return True
    return isSubtree(root.left, subRoot) or isSubtree(root.right, subRoot)</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(m·n)</strong> worst case — Same-Tree at each of m nodes. <strong>Space O(h)</strong> recursion. (Serialization variant: O(m+n).)</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li><code>subRoot</code> equal to the whole tree → True at the root.</li>
<li>Single-node subRoot → matches any equal-valued leaf/subtree.</li>
<li>subRoot larger than root → never matches.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Requiring only value containment, not exact structure — must match shape too.</li>
<li>Substring serialization without null markers (e.g., "12" wrongly matching "123").</li>
<li>Missing the null base case.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Serialize with markers and use KMP for O(m+n).</li>
<li>Same tree ([[100]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[100]] · [[101]] · [[297]]</p>
''',

# ============================================================ LC 988 — Smallest String Starting From Leaf
988: '''
<h2>🧭 How to think about it</h2>
<p>Values 0–25 map to letters a–z. Among all leaf-to-root strings, return the lexicographically smallest. Since the string starts at a <em>leaf</em>, build the path root-to-leaf and <strong>reverse it</strong> at the leaf, then keep the smallest.</p>

<h2>🐢 Brute force first</h2>
<p>Collect every root-to-leaf path, reverse each, compare — O(n·h). A DFS that builds the reversed string incrementally and compares at leaves is the same order but cleaner.</p>

<div class="insight">💡 <strong>Key insight:</strong> prepend each node's letter as you descend (so the working string is already leaf-first from the current node up). At a leaf, that string is a full candidate — compare it to the best. Careful lexicographic comparison, not length, decides the winner.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>DFS carrying <code>cur = chr(val) + parent_string</code> (leaf-first order).</li>
<li>At a leaf, compare <code>cur</code> with the best-so-far and keep the smaller.</li>
<li>Return the best.</li>
</ol>

<h2>🎞️ Visual dry run — [0,1,2,3,4,3,4] (a at root)</h2>
<pre class="viz">paths reversed: "dba","eba","dca","eca"
smallest lexicographically: "dba"
Answer: "dba"</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def smallestFromLeaf(root):
    best = [None]
    def dfs(node, suffix):
        if not node:
            return
        cur = chr(ord('a') + node.val) + suffix   # prepend → leaf-first
        if not node.left and not node.right:
            if best[0] is None or cur &lt; best[0]:
                best[0] = cur
        else:
            dfs(node.left, cur)
            dfs(node.right, cur)
    dfs(root, "")
    return best[0] or ""</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n·h)</strong> — building/comparing strings up to length <code>h</code>. <strong>Space O(h)</strong> recursion.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Single node → its single letter.</li>
<li>Prefix ties (e.g., "ab" vs "aba") → shorter wins only if it's a strict prefix; Python's string <code>&lt;</code> handles it.</li>
<li>Empty tree → empty string.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Comparing by length instead of lexicographic order.</li>
<li>Building root-first and forgetting to reverse.</li>
<li>Recording candidates at internal nodes.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Largest string instead → flip the comparison.</li>
<li>Sum of root-to-leaf numbers ([[129]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[129]] · [[257]] · [[113]]</p>
''',

# ============================================================ LC 1448 — Count Good Nodes in Binary Tree
1448: '''
<h2>🧭 How to think about it</h2>
<p>A node is "good" if no node on the path from the root to it has a greater value — i.e., it's ≥ the <strong>maximum seen so far</strong> along that path. Carry that running max down the tree and count nodes that meet or beat it.</p>

<h2>🐢 Brute force first</h2>
<p>For each node, re-walk up to the root checking for a bigger ancestor → O(n·h). Threading the max down makes it a single O(n) pass.</p>

<div class="insight">💡 <strong>Key insight:</strong> a preorder DFS passes the maximum value on the path so far. A node counts if <code>node.val ≥ max_so_far</code>; then recurse with <code>max(max_so_far, node.val)</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>DFS with <code>max_so_far</code>, starting at <code>root.val</code> (or −∞).</li>
<li>Count 1 if <code>node.val ≥ max_so_far</code>.</li>
<li>Recurse into children with the updated max; sum the counts.</li>
</ol>

<h2>🎞️ Visual dry run — [3,1,4,3,null,1,5]</h2>
<pre class="viz">3 good (max3) ; 1 not (max3) ; 4 good (max4) ; 3 under 1: max3, 3≥3 good ; 1 not ; 5 good
good count = 4</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def goodNodes(root):
    def dfs(node, max_so_far):
        if not node:
            return 0
        good = 1 if node.val &gt;= max_so_far else 0
        new_max = max(max_so_far, node.val)
        return good + dfs(node.left, new_max) + dfs(node.right, new_max)
    return dfs(root, root.val)          # root is always good</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong>, <strong>Space O(h)</strong> recursion.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Root always counts (nothing above it).</li>
<li>Equal values along a path → still "good" (uses ≥).</li>
<li>Single node → 1.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Using strict <code>&gt;</code> and missing nodes equal to the running max.</li>
<li>Resetting the max instead of carrying it down.</li>
<li>Seeding the max above the root's value.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Count nodes that are a path minimum → track the running min.</li>
<li>Good-node style constraints appear in many DFS problems.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[112]] · [[129]] · [[104]]</p>
''',

# ============================================================ LC 94 — Binary Tree Inorder Traversal
94: '''
<h2>🧭 How to think about it</h2>
<p>Inorder means <strong>left, node, right</strong>. For a binary search tree that yields values in sorted order, which is why inorder is so useful. The recursive version is three lines; the iterative one uses an explicit stack to remember the chain of left-descendants.</p>

<h2>🐢 Brute force first</h2>
<p>Recursion is already O(n). The "follow-up" is doing it iteratively (no recursion) — same complexity, but you manage the stack yourself.</p>

<div class="insight">💡 <strong>Key insight (iterative):</strong> push the entire left spine onto a stack; then repeatedly pop (that node's left is done), visit it, and dive into its right child's left spine. The stack replaces the call stack.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>cur = root</code>, empty stack.</li>
<li>Push all left children while <code>cur</code> exists.</li>
<li>Pop a node, record it, then move to its right child and repeat.</li>
</ol>

<h2>🎞️ Visual dry run — [1,null,2,3]</h2>
<pre class="viz">push 1 ; cur=null → pop 1 visit ; cur=2 push 2, push 3 ; pop 3 visit ; pop 2 visit
Result: [1,3,2]</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def inorderTraversal(root):
    res, stack, cur = [], [], root
    while cur or stack:
        while cur:
            stack.append(cur)      # remember left spine
            cur = cur.left
        cur = stack.pop()          # leftmost unvisited
        res.append(cur.val)        # visit node
        cur = cur.right            # then its right subtree
    return res</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — each node pushed/popped once. <strong>Space O(h)</strong> for the stack.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Empty tree → <code>[]</code>.</li>
<li>Left-skewed → the stack grows to the full height.</li>
<li>Right-skewed → stack stays shallow.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Visiting a node before its left subtree.</li>
<li>Forgetting to move to <code>cur.right</code> after popping.</li>
<li>Looping only while <code>cur</code> (must also drain the stack).</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Morris traversal → O(1) space via temporary threads.</li>
<li>Preorder/postorder iterative variants ([[145]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[98]] · [[230]] · [[173]]</p>
''',

# ============================================================ LC 98 — Validate Binary Search Tree
98: '''
<h2>🧭 How to think about it</h2>
<p>Every node in a BST must be greater than <em>all</em> nodes in its left subtree and less than all in its right subtree — not just its immediate children. Enforce this by passing down an allowed <strong>(low, high) range</strong> that tightens as you descend.</p>

<h2>🐢 Brute force first</h2>
<p>Checking only <code>left.val &lt; node.val &lt; right.val</code> misses violations by distant ancestors. Two correct O(n) methods: range bounds, or an inorder traversal that must be strictly increasing.</p>

<div class="insight">💡 <strong>Key insight:</strong> a node is valid only if <code>low &lt; node.val &lt; high</code>. Going left tightens the upper bound to <code>node.val</code>; going right tightens the lower bound to <code>node.val</code>. Start with (−∞, +∞).</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Recurse with <code>(low, high)</code>, starting unbounded.</li>
<li>Null → valid. If <code>node.val</code> is outside <code>(low, high)</code> → invalid.</li>
<li>Recurse left with <code>(low, node.val)</code> and right with <code>(node.val, high)</code>.</li>
</ol>

<h2>🎞️ Visual dry run — [5,1,4,null,null,3,6]</h2>
<pre class="viz">5 in (−∞,∞) ✓ ; left 1 in (−∞,5) ✓ ; right 4 in (5,∞)? 4&gt;5 fails → invalid</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def isValidBST(root):
    def valid(node, low, high):
        if not node:
            return True
        if not (low &lt; node.val &lt; high):     # must fit inherited range
            return False
        return (valid(node.left, low, node.val) and
                valid(node.right, node.val, high))
    return valid(root, float('-inf'), float('inf'))</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong>, <strong>Space O(h)</strong> recursion.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Duplicate values → invalid (strict inequalities).</li>
<li>Single node → valid.</li>
<li>Extreme values → use ±∞ bounds, not fixed int limits.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Comparing only against immediate children.</li>
<li>Using <code>≤</code>/<code>≥</code> and accepting duplicates.</li>
<li>Hardcoding INT_MIN/MAX bounds that real values could hit.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Inorder-increasing check (track the previous value).</li>
<li>Recover a BST with two swapped nodes ([[99]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[99]] · [[94]] · [[230]]</p>
''',

# ============================================================ LC 99 — Recover Binary Search Tree
99: '''
<h2>🧭 How to think about it</h2>
<p>Exactly two nodes of a BST were swapped; fix them. Since an inorder traversal of a valid BST is strictly increasing, the swap creates one or two <strong>descents</strong> (a value bigger than the next). Spot the two offending nodes from those descents and swap their values back.</p>

<h2>🐢 Brute force first</h2>
<p>Inorder into a list, find the two misplaced values by comparing to a sorted copy, then fix — O(n) time and space. The in-traversal method uses O(h) space (or O(1) with Morris).</p>

<div class="insight">💡 <strong>Key insight:</strong> during inorder, whenever <code>prev.val &gt; cur.val</code> you found a descent. The <strong>first</strong> wrong node is the <code>prev</code> of the first descent; the <strong>second</strong> wrong node is the <code>cur</code> of the last descent. If the swapped nodes are adjacent there's only one descent (first and second come from it).</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Inorder-walk tracking <code>prev</code>.</li>
<li>On a descent, set <code>first</code> (once) to <code>prev</code> and always update <code>second</code> to <code>cur</code>.</li>
<li>Swap the values of <code>first</code> and <code>second</code>.</li>
</ol>

<h2>🎞️ Visual dry run — inorder 1,3,2,4 (3 and 2 swapped)</h2>
<pre class="viz">…3 then 2 → descent: first=3, second=2
no more descents → swap values → 1,2,3,4</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def recoverTree(root):
    first = second = prev = None
    stack, cur = [], root
    while cur or stack:
        while cur:
            stack.append(cur); cur = cur.left
        cur = stack.pop()
        if prev and prev.val &gt; cur.val:       # a descent
            if not first:
                first = prev                   # first wrong node
            second = cur                        # keep updating the second
        prev = cur
        cur = cur.right
    first.val, second.val = second.val, first.val   # swap back</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong>, <strong>Space O(h)</strong> (O(1) with Morris traversal).</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Adjacent swapped nodes → a single descent; <code>second</code> is that descent's <code>cur</code>.</li>
<li>Non-adjacent swap → two descents.</li>
<li>Minimum tree (two nodes) → one descent.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Setting <code>first</code> more than once (guard with "if not first").</li>
<li>Taking <code>second</code> from the first descent when swapped nodes aren't adjacent.</li>
<li>Swapping nodes (pointers) instead of just their values.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Morris inorder → true O(1) space.</li>
<li>Validate a BST ([[98]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[98]] · [[94]] · [[230]]</p>
''',

# ============================================================ LC 108 — Convert Sorted Array to Binary Search Tree
108: '''
<h2>🧭 How to think about it</h2>
<p>Turn a sorted array into a <em>height-balanced</em> BST. Pick the <strong>middle element as the root</strong> so the halves are equal-sized; recursively build the left subtree from the left half and the right subtree from the right half. Balance falls out of always splitting in the middle.</p>

<h2>🐢 Brute force first</h2>
<p>Inserting elements one by one gives a valid but possibly skewed BST. Choosing the middle each time guarantees minimal height.</p>

<div class="insight">💡 <strong>Key insight:</strong> the middle of a sorted range is the BST root that keeps both subtrees within one node of each other in size — the definition of balance. Recurse on <code>[lo, mid−1]</code> and <code>[mid+1, hi]</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Recurse on index range <code>[lo, hi]</code>.</li>
<li><code>mid = (lo + hi) // 2</code> becomes the current root.</li>
<li>Build left from <code>[lo, mid−1]</code>, right from <code>[mid+1, hi]</code>.</li>
</ol>

<h2>🎞️ Visual dry run — [-10,-3,0,5,9]</h2>
<pre class="viz">mid idx2 = 0 → root 0
 left [-10,-3] mid -3 → -3 with left -10
 right [5,9] mid 5 → 5 with right 9
Balanced BST rooted at 0</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def sortedArrayToBST(nums):
    def build(lo, hi):
        if lo &gt; hi:
            return None
        mid = (lo + hi) // 2           # middle keeps subtrees balanced
        node = TreeNode(nums[mid])
        node.left = build(lo, mid - 1)
        node.right = build(mid + 1, hi)
        return node
    return build(0, len(nums) - 1)</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — each element becomes one node. <strong>Space O(log n)</strong> recursion (balanced).</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Empty array → empty tree.</li>
<li>One element → single root.</li>
<li>Even length → either middle works; both are balanced.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Building from slices (O(n log n) space) instead of index bounds.</li>
<li>Off-by-one in the sub-ranges.</li>
<li>Not choosing the middle → an unbalanced tree.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Sorted linked list → BST (find middle with fast/slow).</li>
<li>Inorder reconstruction ([[105]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[105]] · [[98]] · [[938]]</p>
''',

# ============================================================ LC 173 — Binary Search Tree Iterator
173: '''
<h2>🧭 How to think about it</h2>
<p>Build an iterator that returns BST values in ascending order via <code>next()</code> and <code>hasNext()</code>, using only O(h) memory and O(1) amortized time per call. That's a <strong>paused inorder traversal</strong>: keep a stack holding the left spine, and advance it one node at a time.</p>

<h2>🐢 Brute force first</h2>
<p>Flatten the whole tree into a list up front → O(n) space, easy but violates the O(h) requirement. The controlled-stack iterator meets it.</p>

<div class="insight">💡 <strong>Key insight:</strong> the stack always contains the nodes whose left subtrees are fully processed but themselves aren't yet returned — the current left spine. <code>next()</code> pops the top (smallest remaining), then pushes the left spine of its right child.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Constructor: push the left spine from the root.</li>
<li><code>next()</code>: pop a node, then push the left spine of its right child; return the popped value.</li>
<li><code>hasNext()</code>: the stack is non-empty.</li>
</ol>

<h2>🎞️ Visual dry run — BST [7,3,15,null,null,9,20]</h2>
<pre class="viz">init stack: 7,3 → next→3 ; push right of 3 (none) → next→7 ; push spine of 15: 15,9 → next→9 → next→15 → next→20</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>class BSTIterator:
    def __init__(self, root):
        self.stack = []
        self._push_left(root)

    def _push_left(self, node):
        while node:
            self.stack.append(node)
            node = node.left

    def next(self):
        node = self.stack.pop()        # smallest remaining
        self._push_left(node.right)     # queue up its right subtree's spine
        return node.val

    def hasNext(self):
        return len(self.stack) &gt; 0</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(1) amortized</strong> per <code>next</code> (each node pushed/popped once overall). <strong>Space O(h)</strong> for the stack.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Empty tree → <code>hasNext</code> immediately false.</li>
<li>Right-skewed → stack stays shallow.</li>
<li>Left-skewed → constructor pushes the whole spine.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Flattening eagerly and using O(n) space.</li>
<li>Forgetting to push the right child's left spine in <code>next</code>.</li>
<li>Returning the node instead of its value.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Reverse iterator (descending) → mirror with right spines.</li>
<li>k-th smallest ([[230]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[94]] · [[230]] · [[285]]</p>
''',

# ============================================================ LC 230 — Kth Smallest Element in a BST
230: '''
<h2>🧭 How to think about it</h2>
<p>Inorder traversal of a BST produces values in ascending order, so the <code>k</code>-th value it emits is the answer. Walk inorder and stop as soon as you've counted <code>k</code> nodes — no need to traverse the whole tree.</p>

<h2>🐢 Brute force first</h2>
<p>Full inorder into a list, return index <code>k−1</code> → O(n). Early-stopping inorder returns after visiting only <code>k</code> nodes.</p>

<div class="insight">💡 <strong>Key insight:</strong> use the iterative inorder with a stack and a counter; decrement <code>k</code> each time you pop a node, and return that node's value when <code>k</code> hits 0.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Push the left spine; pop a node (next smallest).</li>
<li>Decrement <code>k</code>; if 0, return that value.</li>
<li>Otherwise descend into the right subtree and continue.</li>
</ol>

<h2>🎞️ Visual dry run — BST [3,1,4,null,2], k=1</h2>
<pre class="viz">inorder: 1,2,3,4 ; stop at 1st → 1</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def kthSmallest(root, k):
    stack, cur = [], root
    while cur or stack:
        while cur:
            stack.append(cur); cur = cur.left
        cur = stack.pop()
        k -= 1
        if k == 0:
            return cur.val             # k-th smallest reached
        cur = cur.right</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(h + k)</strong> — descend then pop k nodes. <strong>Space O(h)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li><code>k = 1</code> → the minimum (leftmost).</li>
<li><code>k = n</code> → the maximum.</li>
<li>Frequent modifications → keep subtree counts for faster repeated queries.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Traversing the whole tree instead of stopping at <code>k</code>.</li>
<li>Off-by-one on the counter (decrement then compare to 0).</li>
<li>Not exploiting the BST/inorder ordering.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>k-th largest → reverse inorder.</li>
<li>Many queries with updates → augment nodes with subtree sizes.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[94]] · [[173]] · [[230]]</p>
''',

# ============================================================ LC 285 — Inorder Successor in BST
285: '''
<h2>🧭 How to think about it</h2>
<p>Find the node that comes right after a given node <code>p</code> in inorder (the smallest value strictly greater than <code>p.val</code>). Use the BST property: walk from the root, and whenever you go <strong>left</strong> (because the current node is bigger than <code>p</code>), remember that node as a candidate successor.</p>

<h2>🐢 Brute force first</h2>
<p>Full inorder, find <code>p</code>, return the next node → O(n). The BST walk is O(h).</p>

<div class="insight">💡 <strong>Key insight:</strong> the successor is the deepest ancestor for which <code>p</code> is in the left subtree. Descend: if <code>root.val &gt; p.val</code>, this root could be the successor — record it and go left; otherwise go right (successor lies further right/up).</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>succ = None</code>, <code>cur = root</code>.</li>
<li>If <code>cur.val &gt; p.val</code>: <code>succ = cur</code>; go left.</li>
<li>Else go right.</li>
<li>Return <code>succ</code> when <code>cur</code> becomes null.</li>
</ol>

<h2>🎞️ Visual dry run — BST [2,1,3], p = 1</h2>
<pre class="viz">at 2: 2&gt;1 → succ=2, go left to 1 ; 1 not &gt;1 → go right null
Successor = 2</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def inorderSuccessor(root, p):
    succ = None
    cur = root
    while cur:
        if cur.val &gt; p.val:
            succ = cur                 # candidate; smaller ones may lie left
            cur = cur.left
        else:
            cur = cur.right            # need something bigger
    return succ</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(h)</strong> — one root-to-leaf descent. <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li><code>p</code> is the maximum → no successor, return null.</li>
<li><code>p</code> has a right subtree → successor is that subtree's minimum (the walk finds it).</li>
<li>Duplicates absent (BST assumption) → strict <code>&gt;</code>.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Only handling the "has right subtree" case and missing the ancestor case.</li>
<li>Recording candidates when going right (wrong direction).</li>
<li>Using ≥ and returning <code>p</code> itself.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Predecessor → mirror (go right, record when <code>root.val &lt; p.val</code>).</li>
<li>Successor with parent pointers → different formulation.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[230]] · [[173]] · [[98]]</p>
''',

# ============================================================ LC 450 — Delete Node in a BST
450: '''
<h2>🧭 How to think about it</h2>
<p>Delete a value from a BST and keep it valid. First <strong>find</strong> the node by BST navigation. Deleting a leaf or a one-child node is easy (return null or the single child). The tricky case — two children — is solved by replacing the node's value with its <strong>inorder successor</strong> (smallest in the right subtree), then deleting that successor.</p>

<h2>🐢 Brute force first</h2>
<p>Collect all values, remove one, rebuild a balanced BST → loses structure and is O(n). The recursive splice keeps it O(h).</p>

<div class="insight">💡 <strong>Key insight:</strong> recurse toward the target using BST order. When found: no left child → return right; no right child → return left; two children → copy the successor's value into this node and recursively delete the successor from the right subtree.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>If <code>key &lt; node.val</code> recurse left; if <code>&gt;</code> recurse right.</li>
<li>If equal: handle 0/1-child cases directly.</li>
<li>Two children: find the right subtree's min, copy its value up, delete it there.</li>
</ol>

<h2>🎞️ Visual dry run — delete 3 from [5,3,6,2,4,null,7]</h2>
<pre class="viz">find 3 (two children 2,4) → successor = 4 (min of right)
copy 4 up ; delete 4 from right subtree
Result: 3 replaced by 4, tree still a BST</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def deleteNode(root, key):
    if not root:
        return None
    if key &lt; root.val:
        root.left = deleteNode(root.left, key)
    elif key &gt; root.val:
        root.right = deleteNode(root.right, key)
    else:
        if not root.left:  return root.right     # 0 or 1 child
        if not root.right: return root.left
        succ = root.right                         # inorder successor
        while succ.left:
            succ = succ.left
        root.val = succ.val                       # copy value up
        root.right = deleteNode(root.right, succ.val)
    return root</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(h)</strong> — find plus a successor walk. <strong>Space O(h)</strong> recursion.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Key absent → tree unchanged.</li>
<li>Deleting the root → returns the restructured root.</li>
<li>Leaf deletion → simply drops to null.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Forgetting to reassign <code>root.left/right</code> to the recursive result.</li>
<li>Using the predecessor and successor inconsistently.</li>
<li>Not deleting the successor after copying its value.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Use the predecessor (max of left subtree) instead.</li>
<li>Insert into a BST → the mirror operation.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[98]] · [[285]] · [[669]]</p>
''',

# ============================================================ LC 501 — Find Mode in Binary Search Tree
501: '''
<h2>🧭 How to think about it</h2>
<p>Return the most frequent value(s) in a BST that may contain duplicates. Because inorder visits values in sorted order, <strong>equal values are consecutive</strong> — so you can count run lengths on the fly and track the maximum, using O(1) extra space (besides the output).</p>

<h2>🐢 Brute force first</h2>
<p>A hash-map count then filter by max → O(n) time and space. Inorder streak-counting avoids the map.</p>

<div class="insight">💡 <strong>Key insight:</strong> during inorder, maintain the current value's streak length. When the value changes, reset the streak. If a streak matches the best, add the value to the modes; if it exceeds the best, clear the list and start fresh.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Inorder walk with <code>prev</code>, <code>count</code>, <code>max_count</code>, and a <code>modes</code> list.</li>
<li>Same as <code>prev</code> → <code>count += 1</code>; else reset <code>count = 1</code>.</li>
<li>If <code>count == max_count</code> append; if <code>count &gt; max_count</code> reset the list to just this value.</li>
</ol>

<h2>🎞️ Visual dry run — inorder 1,2,2</h2>
<pre class="viz">1 (count1, max1, modes[1]) ; 2 (count1==max1 → modes[1,2]) ; 2 (count2&gt;1 → modes=[2], max2)
Answer: [2]</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def findMode(root):
    modes = []
    prev = None
    count = 0
    max_count = 0
    def visit(val):
        nonlocal prev, count, max_count, modes
        count = count + 1 if val == prev else 1
        if count &gt; max_count:
            max_count = count
            modes = [val]
        elif count == max_count:
            modes.append(val)
        prev = val
    stack, cur = [], root
    while cur or stack:
        while cur:
            stack.append(cur); cur = cur.left
        cur = stack.pop()
        visit(cur.val)
        cur = cur.right
    return modes</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong>, <strong>Space O(h)</strong> for the stack (O(1) extra beyond output with Morris).</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>All distinct → every value is a mode (count 1).</li>
<li>Single node → that value.</li>
<li>Multiple modes → all returned.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Not resetting the streak when the value changes.</li>
<li>Forgetting to clear the modes list when a new max appears.</li>
<li>Relying on a hash map when O(1) extra space is the goal.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Return only one mode → keep the first max.</li>
<li>Mode in a general (non-BST) tree → needs a counting map.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[94]] · [[530]] · [[230]]</p>
''',

# ============================================================ LC 530 — Minimum Absolute Difference in BST
530: '''
<h2>🧭 How to think about it</h2>
<p>Find the smallest absolute difference between any two node values. In a BST, the closest pair is always <strong>adjacent in inorder order</strong> — so walk inorder and compare each value only with the previous one.</p>

<h2>🐢 Brute force first</h2>
<p>Compare all pairs → O(n²). Sort the values (or inorder them) and check neighbors → O(n) after the traversal.</p>

<div class="insight">💡 <strong>Key insight:</strong> the minimum difference in a sorted sequence is between consecutive elements. Inorder gives sorted order for free, so track <code>prev</code> and minimize <code>cur − prev</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Inorder-walk keeping <code>prev</code>.</li>
<li>On each node, if <code>prev</code> exists, update <code>best = min(best, cur.val − prev)</code>.</li>
<li>Return <code>best</code>.</li>
</ol>

<h2>🎞️ Visual dry run — inorder 1,3,6</h2>
<pre class="viz">1→3: diff 2 (best 2) ; 3→6: diff 3 (best stays 2)
Answer: 2</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def getMinimumDifference(root):
    best = float('inf')
    prev = None
    stack, cur = [], root
    while cur or stack:
        while cur:
            stack.append(cur); cur = cur.left
        cur = stack.pop()
        if prev is not None:
            best = min(best, cur.val - prev)   # neighbors in sorted order
        prev = cur.val
        cur = cur.right
    return best</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong>, <strong>Space O(h)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Fewer than two nodes → no valid pair (problem guarantees at least two).</li>
<li>Values close together → still caught by neighbor comparison.</li>
<li>Duplicates (if present) → difference 0.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Comparing all pairs instead of using inorder adjacency.</li>
<li>Taking absolute value unnecessarily (inorder is increasing, so <code>cur − prev ≥ 0</code>).</li>
<li>Not initializing <code>prev</code> as "none".</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>General tree → collect values and sort.</li>
<li>Mode / k-th smallest use the same inorder ([[501]], [[230]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[501]] · [[230]] · [[94]]</p>
''',

# ============================================================ LC 669 — Trim a Binary Search Tree
669: '''
<h2>🧭 How to think about it</h2>
<p>Remove all nodes whose values fall outside <code>[low, high]</code>, keeping the tree a valid BST. Recurse: if a node is too small, the entire left subtree is also too small, so return the trimmed <strong>right</strong> subtree; if too big, return the trimmed <strong>left</strong> subtree; otherwise keep the node and trim both sides.</p>

<h2>🐢 Brute force first</h2>
<p>Collect valid values and rebuild → O(n) and loses structure. The recursive BST trim is O(n) and preserves shape where possible.</p>

<div class="insight">💡 <strong>Key insight:</strong> BST ordering lets you discard whole subtrees. If <code>node.val &lt; low</code>, everything in its left subtree is also &lt; low, so replace the node with the trim of its right child. Symmetrically for <code>&gt; high</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Null → null.</li>
<li><code>val &lt; low</code> → return <code>trim(right)</code>.</li>
<li><code>val &gt; high</code> → return <code>trim(left)</code>.</li>
<li>Else trim both children and keep the node.</li>
</ol>

<h2>🎞️ Visual dry run — [3,0,4,null,2,null,null,1], low=1, high=3</h2>
<pre class="viz">3 in range → trim left(0) and right(4)
 0&lt;1 → return trim(right of 0 = 2) → 2 in range → keep, trim its left 1
 4&gt;3 → return trim(left of 4 = null)
Result: 3→(2→1)</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def trimBST(root, low, high):
    if not root:
        return None
    if root.val &lt; low:
        return trimBST(root.right, low, high)   # whole left subtree too small
    if root.val &gt; high:
        return trimBST(root.left, low, high)    # whole right subtree too big
    root.left = trimBST(root.left, low, high)
    root.right = trimBST(root.right, low, high)
    return root</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> worst case. <strong>Space O(h)</strong> recursion.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>All nodes out of range → empty tree.</li>
<li>Root itself trimmed → the returned subtree becomes the new root.</li>
<li>Range covers everything → tree unchanged.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Trimming both children even when the node is out of range (must jump to the surviving subtree).</li>
<li>Forgetting to reassign <code>root.left/right</code>.</li>
<li>Using inclusive/exclusive bounds incorrectly.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Range sum within bounds ([[938]]).</li>
<li>Delete a single node ([[450]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[938]] · [[450]] · [[98]]</p>
''',

# ============================================================ LC 938 — Range Sum of BST
938: '''
<h2>🧭 How to think about it</h2>
<p>Sum the values in <code>[low, high]</code>. Use the BST property to <strong>prune</strong>: if a node is below <code>low</code>, skip its entire left subtree; if above <code>high</code>, skip its right subtree. Otherwise add the node and explore both sides.</p>

<h2>🐢 Brute force first</h2>
<p>Traverse every node and add those in range → O(n). Pruning skips whole subtrees for a faster average, still O(n) worst case.</p>

<div class="insight">💡 <strong>Key insight:</strong> ordering tells you where valid values can be. <code>node.val &lt; low</code> ⇒ only the right subtree can contain in-range values; <code>node.val &gt; high</code> ⇒ only the left. In range ⇒ count it and recurse both ways.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Null → 0.</li>
<li><code>val &lt; low</code> → recurse right only.</li>
<li><code>val &gt; high</code> → recurse left only.</li>
<li>Else add <code>val</code> and recurse both.</li>
</ol>

<h2>🎞️ Visual dry run — [10,5,15,3,7,null,18], low=7, high=15</h2>
<pre class="viz">10 in range → +10 ; left 5&lt;7 → right of 5 = 7 (+7) ; right 15 in range → +15 ; 18&gt;15 skip
Sum = 10+7+15 = 32</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def rangeSumBST(root, low, high):
    if not root:
        return 0
    if root.val &lt; low:
        return rangeSumBST(root.right, low, high)   # prune left
    if root.val &gt; high:
        return rangeSumBST(root.left, low, high)    # prune right
    return (root.val
            + rangeSumBST(root.left, low, high)
            + rangeSumBST(root.right, low, high))</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> worst case (fewer with pruning). <strong>Space O(h)</strong> recursion.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>No values in range → 0.</li>
<li>Whole tree in range → sums everything.</li>
<li>Inclusive bounds → both endpoints count.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Recursing both ways even when pruning is possible (correct but slower).</li>
<li>Excluding the endpoints (bounds are inclusive).</li>
<li>Missing the null base case.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Count nodes in range → return counts instead of sums.</li>
<li>Trim to the range ([[669]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[669]] · [[98]] · [[108]]</p>
''',

# ============================================================ LC 104 — Maximum Depth of Binary Tree
104: '''
<h2>🧭 How to think about it</h2>
<p>The depth of a tree is 1 plus the deeper of its two subtrees. That recursive definition is the whole solution: a <strong>postorder</strong> recursion where an empty subtree contributes 0.</p>

<h2>🐢 Brute force first</h2>
<p>BFS counting levels also works and is O(n). The recursive height is the shortest expression.</p>

<div class="insight">💡 <strong>Key insight:</strong> <code>depth(node) = 1 + max(depth(left), depth(right))</code>, with <code>depth(None) = 0</code>. Each node's answer depends only on its children — a clean bottom-up computation.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Null → 0.</li>
<li>Recurse into both children.</li>
<li>Return <code>1 + max(left, right)</code>.</li>
</ol>

<h2>🎞️ Visual dry run — [3,9,20,null,null,15,7]</h2>
<pre class="viz">9→1, 15→1, 7→1, 20→2, root→3
Answer: 3</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def maxDepth(root):
    if not root:
        return 0
    return 1 + max(maxDepth(root.left), maxDepth(root.right))</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong>, <strong>Space O(h)</strong> recursion.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Empty tree → 0.</li>
<li>Single node → 1.</li>
<li>Skewed tree → depth equals the node count.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Returning <code>max(left, right)</code> without the <code>+1</code>.</li>
<li>Counting edges vs nodes inconsistently.</li>
<li>Deep recursion overflow on huge skewed trees (use BFS then).</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Minimum depth → careful with one-sided nodes.</li>
<li>Balanced check builds on height ([[110]]); diameter too ([[543]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[110]] · [[543]] · [[111]]</p>
''',

# ============================================================ LC 106 — Construct Binary Tree from Inorder and Postorder Traversal
106: '''
<h2>🧭 How to think about it</h2>
<p>Postorder ends with the root (left, right, <strong>root</strong>). So read postorder from the <em>back</em>: the last element is the root; find it in inorder to split left/right subtrees. Because postorder is left-right-root, when consuming from the back you must build the <strong>right subtree before the left</strong>.</p>

<h2>🐢 Brute force first</h2>
<p>Slicing and <code>index()</code> each call is O(n²). A value→inorder-index map plus a postorder cursor makes it O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> mirror of [[105]]. Take roots off the end of postorder; split inorder at the root; recurse right first (since it was placed just before the root in postorder), then left.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Map value → inorder index.</li>
<li>Cursor at the end of postorder; each call pops a root.</li>
<li>Build right subtree first, then left.</li>
</ol>

<h2>🎞️ Visual dry run — inorder [9,3,15,20,7], postorder [9,15,7,20,3]</h2>
<pre class="viz">root 3 (last) → split inorder: left[9] | right[15,20,7]
next root 20 → right subtree: left[15] right[7]
Reconstructed: 3(9, 20(15,7))</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def buildTree(inorder, postorder):
    idx = {v: i for i, v in enumerate(inorder)}
    cur = [len(postorder) - 1]                 # postorder cursor (from the end)
    def build(lo, hi):
        if lo &gt; hi:
            return None
        root_val = postorder[cur[0]]
        cur[0] -= 1
        root = TreeNode(root_val)
        mid = idx[root_val]
        root.right = build(mid + 1, hi)        # RIGHT before LEFT
        root.left = build(lo, mid - 1)
        return root
    return build(0, len(inorder) - 1)</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong>, <strong>Space O(n)</strong> for the map and recursion.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Empty input → empty tree.</li>
<li>Single node → root only.</li>
<li>Skewed tree → still O(n) with the map.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Building the left subtree first (breaks the postorder-from-end order).</li>
<li>Re-scanning inorder with <code>index()</code>.</li>
<li>Off-by-one on the cursor or bounds.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Preorder + inorder ([[105]]).</li>
<li>Postorder + preorder → not unique in general.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[105]] · [[145]] · [[889]]</p>
''',

# ============================================================ LC 124 — Binary Tree Maximum Path Sum
124: '''
<h2>🧭 How to think about it</h2>
<p>A "path" can start and end at any nodes and bends at most once (goes up to some node, then down). At each node, the best path <em>through</em> it is the node's value plus the best downward gain from each side. The tricky part: what a node <strong>returns</strong> to its parent (a single downward branch) differs from what it <strong>contributes</strong> as a peak.</p>

<h2>🐢 Brute force first</h2>
<p>Trying all path pairs is exponential. A single postorder pass computing downward gains is O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> for each node compute <code>leftGain = max(0, dfs(left))</code> and <code>rightGain = max(0, dfs(right))</code> (clamp negatives to 0 — a losing branch is dropped). Update a global best with <code>node.val + leftGain + rightGain</code> (the bend), but return only <code>node.val + max(leftGain, rightGain)</code> to the parent (a straight branch).</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Postorder DFS; compute clamped left/right gains.</li>
<li>Update the global max with the through-node sum.</li>
<li>Return the best single-branch extension upward.</li>
</ol>

<h2>🎞️ Visual dry run — [-10,9,20,null,null,15,7]</h2>
<pre class="viz">at 20: gains 15,7 → through = 20+15+7 = 42 (global) ; returns 20+15 = 35
at -10: gains max(0,9)=9, max(0,35)=35 → through = -10+9+35 = 34 &lt; 42
Answer: 42</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def maxPathSum(root):
    best = float('-inf')
    def gain(node):
        nonlocal best
        if not node:
            return 0
        left = max(0, gain(node.left))     # drop negative branches
        right = max(0, gain(node.right))
        best = max(best, node.val + left + right)   # path bending here
        return node.val + max(left, right)          # extend one branch up
    gain(root)
    return best</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong>, <strong>Space O(h)</strong> recursion.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>All negative values → the max single node wins (clamping keeps branches out, but the node value can be negative — best still updates).</li>
<li>Single node → its value.</li>
<li>Long negative branch → dropped by the <code>max(0, …)</code>.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Returning the bent sum to the parent (a path can't fork upward).</li>
<li>Not clamping negative gains to 0.</li>
<li>Initializing <code>best = 0</code> and failing all-negative trees.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Diameter (count edges, ignore values) ([[543]]).</li>
<li>Max path sum with the path count constraint.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[543]] · [[104]] · [[687]]</p>
''',

# ============================================================ LC 145 — Binary Tree Postorder Traversal
145: '''
<h2>🧭 How to think about it</h2>
<p>Postorder is <strong>left, right, node</strong>. Recursively it's trivial; iteratively, a neat trick is to do a modified preorder (node, right, left) and <strong>reverse</strong> the result — that produces left, right, node.</p>

<h2>🐢 Brute force first</h2>
<p>Recursion is O(n). The iterative challenge is doing it without recursion; the reverse-preorder approach is the simplest correct method.</p>

<div class="insight">💡 <strong>Key insight:</strong> push root, then pop and record; push its <em>left</em> then <em>right</em> children (so right is processed first). This yields node-right-left order; reverse it to get postorder.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Stack with the root; output list.</li>
<li>Pop a node, append its value, push left then right.</li>
<li>Reverse the output at the end.</li>
</ol>

<h2>🎞️ Visual dry run — [1,null,2,3]</h2>
<pre class="viz">pop1 out[1] push2 ; pop2 out[1,2] push3 ; pop3 out[1,2,3]
reverse → [3,2,1]</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def postorderTraversal(root):
    if not root:
        return []
    stack, out = [root], []
    while stack:
        node = stack.pop()
        out.append(node.val)            # node, then (below) right, left
        if node.left:  stack.append(node.left)
        if node.right: stack.append(node.right)
    return out[::-1]                    # reverse node-right-left → left-right-node</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong>, <strong>Space O(n)</strong> for the stack and output.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Empty tree → <code>[]</code>.</li>
<li>Single node → <code>[val]</code>.</li>
<li>Skewed tree → linear stack usage.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Pushing right before left and forgetting the final reverse.</li>
<li>Trying a one-stack "true" postorder without tracking the last-visited node (harder to get right).</li>
<li>Reversing the tree instead of the output.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Inorder / preorder iterative ([[94]]).</li>
<li>Morris postorder → O(1) space, intricate.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[94]] · [[104]] · [[124]]</p>
''',

# ============================================================ LC 222 — Count Complete Tree Nodes
222: '''
<h2>🧭 How to think about it</h2>
<p>In a <em>complete</em> binary tree, every level is full except possibly the last, which fills left to right. You could count all nodes in O(n), but you can do better: compare the <strong>left height</strong> and <strong>right height</strong> at each node — if they're equal, the subtree is perfect and its size is <code>2^h − 1</code> (no recursion needed for that side).</p>

<h2>🐢 Brute force first</h2>
<p>A plain traversal counts all nodes in O(n). Exploiting completeness gives O(log²n).</p>

<div class="insight">💡 <strong>Key insight:</strong> walking only left gives the left height; only right gives the right height. If they match, the subtree is perfect → return <code>2^h − 1</code>. Otherwise recurse: <code>1 + count(left) + count(right)</code>. Only one branch recurses deeply at each level.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Measure left height (all left) and right height (all right).</li>
<li>Equal → return <code>2^height − 1</code>.</li>
<li>Else return <code>1 + count(left) + count(right)</code>.</li>
</ol>

<h2>🎞️ Visual dry run — perfect subtree of height 3</h2>
<pre class="viz">leftH == rightH == 3 → 2^3 − 1 = 7 nodes, no recursion
if unequal → recurse into children (one is perfect, computed instantly)</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def countNodes(root):
    if not root:
        return 0
    lh = rh = 0
    n = root
    while n: lh += 1; n = n.left       # height along the left edge
    n = root
    while n: rh += 1; n = n.right      # height along the right edge
    if lh == rh:
        return (1 &lt;&lt; lh) - 1            # perfect subtree
    return 1 + countNodes(root.left) + countNodes(root.right)</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(log²n)</strong> — O(log n) height checks at each of O(log n) levels. <strong>Space O(log n)</strong> recursion.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Empty tree → 0.</li>
<li>Perfect tree → answered by a single height comparison.</li>
<li>Last level partially filled → recursion narrows to the boundary.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Falling back to O(n) counting and ignoring completeness.</li>
<li>Off-by-one in the <code>2^h − 1</code> formula (heights counted in nodes, not edges).</li>
<li>Measuring left height on the right edge or vice versa.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Binary search on the last level's index → also O(log²n).</li>
<li>Max depth of a general tree ([[104]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[104]] · [[662]] · [[110]]</p>
''',

# ============================================================ LC 337 — House Robber III
337: '''
<h2>🧭 How to think about it</h2>
<p>Rob a binary tree of houses, but you can't rob a node and its direct child. At each node you have two choices, so return <strong>two numbers</strong> from every subtree: the best you can do if you rob this node, and the best if you don't. A parent combines its children's numbers.</p>

<h2>🐢 Brute force first</h2>
<p>Naive recursion recomputes grandchildren repeatedly → exponential. Returning a (rob, skip) pair per node makes it one O(n) pass (this is tree DP).</p>

<div class="insight">💡 <strong>Key insight:</strong> <code>rob = node.val + skipLeft + skipRight</code> (children must be skipped); <code>skip = max(robLeft, skipLeft) + max(robRight, skipRight)</code> (children free to choose). The answer is <code>max(rob, skip)</code> at the root.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Postorder DFS returning <code>(rob, skip)</code>.</li>
<li>Combine children's pairs into the node's pair.</li>
<li>Return <code>max</code> of the root's pair.</li>
</ol>

<h2>🎞️ Visual dry run — [3,2,3,null,3,null,1]</h2>
<pre class="viz">leaves 3,1: (3,0),(1,0)
node2: rob=2+0=2, skip=max(3,0)=3 → (2,3)
node3(right): rob=3+0=3, skip=1 → (3,1)
root3: rob=3+3+1=7, skip=max(2,3)+max(3,1)=3+3=6 → max 7</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def rob(root):
    def dfs(node):
        if not node:
            return (0, 0)              # (rob, skip)
        lr, ls = dfs(node.left)
        rr, rs = dfs(node.right)
        rob_here = node.val + ls + rs  # can't rob children
        skip_here = max(lr, ls) + max(rr, rs)
        return (rob_here, skip_here)
    return max(dfs(root))</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — one pass. <strong>Space O(h)</strong> recursion.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Single node → rob it.</li>
<li>All values equal → alternating levels chosen.</li>
<li>Empty tree → 0.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Returning a single number and losing the "skip" option.</li>
<li>Letting a robbed node's child also be robbed.</li>
<li>Memo-less naive recursion (exponential).</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Linear house robber (array) → the 1-D analog.</li>
<li>Max independent set on a tree → the same DP.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[124]] · [[543]] · [[104]]</p>
''',

# ============================================================ LC 366 — Find Leaves of Binary Tree
366: '''
<h2>🧭 How to think about it</h2>
<p>Repeatedly strip off all current leaves and group them, until the tree is empty. Instead of literally deleting layers, notice that a node's <strong>height from the bottom</strong> (leaf = 0) is exactly the round in which it gets removed. So group nodes by that height.</p>

<h2>🐢 Brute force first</h2>
<p>Actually removing leaves and re-scanning each round is O(n·layers). One postorder pass computing bottom-up heights buckets every node in O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> <code>height(node) = 1 + max(height(left), height(right))</code> with leaves at height 0. A node's height equals its removal round, so append its value to <code>result[height]</code> during the postorder.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Postorder DFS returning each node's bottom-up height.</li>
<li>Append the node's value to <code>result[height]</code> (grow the list as needed).</li>
<li>Return the list of layers.</li>
</ol>

<h2>🎞️ Visual dry run — [1,2,3,4,5]</h2>
<pre class="viz">heights: 4→0,5→0,3→0,2→1,1→2
layer0 [4,5,3] ; layer1 [2] ; layer2 [1]
Result: [[4,5,3],[2],[1]]</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def findLeaves(root):
    res = []
    def height(node):
        if not node:
            return -1                   # so a leaf gets height 0
        h = 1 + max(height(node.left), height(node.right))
        if h == len(res):
            res.append([])              # new layer
        res[h].append(node.val)
        return h
    height(root)
    return res</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — one pass. <strong>Space O(n)</strong> for output plus O(h) recursion.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Single node → <code>[[val]]</code>.</li>
<li>Skewed tree → each node in its own layer.</li>
<li>Empty tree → <code>[]</code>.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Actually deleting nodes and re-traversing (slow and mutating).</li>
<li>Using top-down depth instead of bottom-up height.</li>
<li>Off-by-one making leaves height 1 instead of 0.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Return heights instead of grouping.</li>
<li>Delete-and-return-forest style problems ([[1110]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[104]] · [[1110]] · [[543]]</p>
''',

# ============================================================ LC 437 — Path Sum III
437: '''
<h2>🧭 How to think about it</h2>
<p>Count paths that sum to a target, where a path goes <em>downward</em> (parent to child) but need not start at the root or end at a leaf. This is the tree version of "subarrays summing to k" — solved with a <strong>running prefix sum</strong> and a hash map of prefix counts along the current root-to-node path.</p>

<h2>🐢 Brute force first</h2>
<p>Start a downward sum from every node → O(n²) (or O(n·h)). The prefix-sum map answers it in O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> maintain <code>curr</code> = sum from root to the current node and a map <code>count[prefix]</code>. The number of valid paths ending here is <code>count[curr − target]</code> (an earlier prefix that leaves exactly <code>target</code>). Add the current prefix on the way down and <strong>remove it on the way back</strong> (backtrack) so sibling paths aren't polluted.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Seed <code>count = {0: 1}</code>, <code>curr = 0</code>.</li>
<li>At each node: <code>curr += val</code>; add <code>count[curr − target]</code> to the total; increment <code>count[curr]</code>.</li>
<li>Recurse into children, then decrement <code>count[curr]</code> (backtrack).</li>
</ol>

<h2>🎞️ Visual dry run — target 8, path 10→5→3</h2>
<pre class="viz">curr: 10 (need 2:0), 15 (need 7:0), 18 (need 10: count[10]=1 → +1)
found path 5→3? actually 10..: the 5→3 subpath sums 8 → counted via prefix 18−8=10</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>from collections import defaultdict
def pathSum(root, targetSum):
    count = defaultdict(int)
    count[0] = 1
    total = 0
    def dfs(node, curr):
        nonlocal total
        if not node:
            return
        curr += node.val
        total += count[curr - targetSum]   # paths ending here summing to target
        count[curr] += 1
        dfs(node.left, curr)
        dfs(node.right, curr)
        count[curr] -= 1                    # backtrack: leave this path
    dfs(root, 0)
    return total</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — each node processed once. <strong>Space O(h)</strong> for the map/recursion along a path.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Negative values → the prefix-sum method handles them (a sliding window would not).</li>
<li>Target 0 → counts zero-sum downward paths.</li>
<li>Single node equal to target → counts 1.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Forgetting to backtrack <code>count[curr] -= 1</code> → counts cross-branch paths.</li>
<li>Omitting the <code>count[0] = 1</code> seed.</li>
<li>Trying a sliding window with negative values.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Root-to-leaf only ([[112]], [[113]]).</li>
<li>Subarray sum equals k (array analog).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[112]] · [[113]] · [[124]]</p>
''',

# ============================================================ LC 543 — Diameter of Binary Tree
543: '''
<h2>🧭 How to think about it</h2>
<p>The diameter is the longest path (in edges) between any two nodes; it may not pass through the root. At each node, the longest path <em>through</em> it is <code>leftHeight + rightHeight</code>. Compute heights bottom-up and track the maximum such sum globally.</p>

<h2>🐢 Brute force first</h2>
<p>Computing height separately at each node to test its through-path is O(n²). One postorder pass updating a global gives O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> a height function that, as a side effect, updates <code>best = max(best, leftHeight + rightHeight)</code> at every node. The function returns <code>1 + max(left, right)</code> to its parent; the global holds the answer.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Postorder height with a global <code>best</code>.</li>
<li>At each node, update <code>best</code> with <code>left + right</code> (edges through it).</li>
<li>Return <code>1 + max(left, right)</code>.</li>
</ol>

<h2>🎞️ Visual dry run — [1,2,3,4,5]</h2>
<pre class="viz">at 2: left(4)=1,right(5)=1 → through 2 ; returns 2
at 1: left h(2)=2, right h(3)=1 → through = 3 (path 4-2-1-3)
Answer: 3</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def diameterOfBinaryTree(root):
    best = 0
    def height(node):
        nonlocal best
        if not node:
            return 0
        left = height(node.left)
        right = height(node.right)
        best = max(best, left + right)     # edges of the path through node
        return 1 + max(left, right)
    height(root)
    return best</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong>, <strong>Space O(h)</strong> recursion.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Single node → diameter 0 (no edges).</li>
<li>Path avoiding the root → captured because every node updates the global.</li>
<li>Skewed tree → diameter equals its height in edges.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Counting nodes instead of edges (off by one).</li>
<li>Assuming the diameter passes through the root.</li>
<li>Returning the through-sum to the parent instead of the height.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Weighted edges → add weights instead of counting 1.</li>
<li>Max path sum by value ([[124]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[124]] · [[104]] · [[110]]</p>
''',

# ============================================================ LC 863 — All Nodes Distance K in Binary Tree
863: '''
<h2>🧭 How to think about it</h2>
<p>Find every node exactly <code>k</code> edges from a target node. In a tree, "distance" can go up toward the parent too, but tree nodes only know their children. The fix: first build a <strong>parent map</strong> so every node can move in all three directions, then run a plain <strong>BFS</strong> outward from the target for <code>k</code> levels.</p>

<h2>🐢 Brute force first</h2>
<p>For each node compute its distance to the target via a path search → O(n²). Parent map + BFS is O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> converting the tree into an undirected graph (each node linked to left, right, and parent) turns "distance k" into a standard BFS that stops after <code>k</code> rounds. A visited set prevents walking back.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>DFS to record each node's parent.</li>
<li>BFS from the target, tracking visited nodes.</li>
<li>After exactly <code>k</code> rounds, the queue holds the answer.</li>
</ol>

<h2>🎞️ Visual dry run — target=5, k=2</h2>
<pre class="viz">round0: {5}
round1: neighbors of 5 (parent 3, children 6,2)
round2: their unvisited neighbors → the distance-2 nodes
Return the round-2 frontier</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>from collections import deque
def distanceK(root, target, k):
    parent = {}
    def dfs(node, par):
        if not node: return
        parent[node] = par
        dfs(node.left, node); dfs(node.right, node)
    dfs(root, None)

    visited = {target}
    q = deque([target])
    dist = 0
    while q and dist &lt; k:
        for _ in range(len(q)):
            node = q.popleft()
            for nxt in (node.left, node.right, parent[node]):
                if nxt and nxt not in visited:
                    visited.add(nxt); q.append(nxt)
        dist += 1
    return [n.val for n in q]</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — DFS plus BFS. <strong>Space O(n)</strong> for the parent map, visited set, and queue.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li><code>k = 0</code> → just the target.</li>
<li><code>k</code> larger than the tree's reach → empty (queue empties first).</li>
<li>Target is the root → only downward BFS matters.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Forgetting the parent direction → misses upward nodes.</li>
<li>No visited set → walks back and loops.</li>
<li>Stopping at the wrong round (off-by-one on <code>k</code>).</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Amount of time to infect a tree (BFS from a start) → same graph conversion.</li>
<li>Distance between two nodes → LCA-based path length.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[236]] · [[102]] · [[543]]</p>
''',

# ============================================================ LC 1110 — Delete Nodes And Return Forest
1110: '''
<h2>🧭 How to think about it</h2>
<p>Delete a set of values; the remaining nodes split into a <strong>forest</strong> of subtrees. Do a <strong>postorder</strong> pass: when a node is deleted, its surviving children become new tree roots. A node is a new root if it isn't deleted and its parent was deleted (or it's the original root).</p>

<h2>🐢 Brute force first</h2>
<p>Deleting one value at a time and re-scanning is wasteful. A single postorder with a "is my parent gone?" flag handles all deletions in O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> pass down whether the current node is a root candidate (parent deleted). Postorder returns the (possibly null) subtree after deletion. If a node is deleted, return null so the parent detaches it; if it survives and its parent is gone, add it to the forest.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>DFS with a flag <code>is_root</code> and a set of deletions.</li>
<li>Recurse into children first (postorder), reassigning them (deleted children become null).</li>
<li>If the node is deleted → return null; else if <code>is_root</code>, add it to the forest.</li>
</ol>

<h2>🎞️ Visual dry run — [1,2,3,4,5,6,7], delete {3,5}</h2>
<pre class="viz">delete 3 → its child 6,7 become roots
delete 5 → 2 loses right child (no new root, 5 had no kids kept)
Forest roots: 1, 6, 7</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def delNodes(root, to_delete):
    to_delete = set(to_delete)
    forest = []
    def dfs(node, is_root):
        if not node:
            return None
        deleted = node.val in to_delete
        if is_root and not deleted:
            forest.append(node)            # new tree root
        # children are roots only if this node is deleted
        node.left = dfs(node.left, deleted)
        node.right = dfs(node.right, deleted)
        return None if deleted else node
    dfs(root, True)
    return forest</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — one pass. <strong>Space O(h)</strong> recursion plus the forest output.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Root deleted → its surviving children are the first roots.</li>
<li>No deletions → the forest is just the original root.</li>
<li>Leaf deletions → simply detach, no new roots.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Adding a node to the forest before detaching deleted children.</li>
<li>Not reassigning <code>node.left/right</code> to the recursive result → keeps deleted nodes.</li>
<li>Treating survivors of non-deleted parents as new roots.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Return the count of trees instead of the forest.</li>
<li>Find leaves layer by layer ([[366]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[366]] · [[226]] · [[104]]</p>
''',

# ============================================================ LC 2458 — Height of Binary Tree After Subtree Removal Queries
2458: '''
<h2>🧭 How to think about it</h2>
<p>For each query node, imagine removing its entire subtree and report the remaining tree's height. Answering each query by rebuilding is far too slow. Precompute, in two passes, each node's <strong>depth</strong> and its subtree's deepest reach, then a single DFS computes, for every node, the best height achievable <em>without</em> entering that node's subtree.</p>

<h2>🐢 Brute force first</h2>
<p>Recompute the height for each of up to n queries → O(n²). Precomputing lets each query be answered in O(1).</p>

<div class="insight">💡 <strong>Key insight:</strong> let <code>deepest[node]</code> be the maximum node-depth within its subtree. Do a DFS passing down <code>rest</code> = the deepest depth reachable while avoiding the current subtree. When descending into one child, the value passed carries the other child's <code>deepest</code> (and the node's own depth). Then <code>answer[node] = rest</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Pass 1: compute <code>deepest[node]</code> = max absolute depth in its subtree.</li>
<li>Pass 2: DFS carrying <code>rest</code>; store <code>answer[node.val] = rest</code>.</li>
<li>When recursing into a child, combine <code>rest</code> with the sibling's <code>deepest</code>.</li>
<li>Return <code>[answer[q] for q in queries]</code>.</li>
</ol>

<h2>🎞️ Visual dry run — remove a leaf's subtree</h2>
<pre class="viz">deepest depths precomputed per node
descend left → rest = max(rest, deepest[right sibling], depth-of-node)
answer[node] = the best remaining depth avoiding node's subtree</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def treeQueries(root, queries):
    deepest = {}                          # node -> max absolute depth in its subtree
    def depth(node, d):
        if not node:
            return d - 1                  # so a null contributes nothing
        deepest[node] = max(depth(node.left, d + 1),
                            depth(node.right, d + 1))
        return deepest[node]
    depth(root, 0)

    answer = {}
    def dfs(node, d, rest):
        if not node:
            return
        answer[node.val] = rest
        left_deep  = deepest.get(node.left, d)   # depth of node if no left
        right_deep = deepest.get(node.right, d)
        # into left: exclude left subtree → best is rest or the right branch
        dfs(node.left, d + 1, max(rest, right_deep))
        dfs(node.right, d + 1, max(rest, left_deep))
    dfs(root, 0, 0)
    return [answer[q] for q in queries]</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n + q)</strong> — two DFS passes plus O(1) per query. <strong>Space O(n)</strong> for the maps.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Removing a leaf → height often unchanged (a sibling branch still reaches deep).</li>
<li>Removing a node on the unique deepest path → height drops to the next-deepest branch.</li>
<li>Query for a shallow node → answer reflects the rest of the tree.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Mixing up "depth" (from root) with "height" (from leaves).</li>
<li>Forgetting the node's own depth as a candidate when a child is missing.</li>
<li>Recomputing per query instead of precomputing.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Batch queries with rerooting techniques.</li>
<li>Simpler subtree-removal forest ([[1110]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[1110]] · [[543]] · [[104]]</p>
''',

# ============================================================ LC 235 — Lowest Common Ancestor of a Binary Search Tree
235: '''
<h2>🧭 How to think about it</h2>
<p>The lowest common ancestor (LCA) of two BST nodes is the first node where the two values <strong>split</strong> — one goes left and the other right (or one equals the node). BST ordering makes this a simple downward walk, no recursion into both sides needed.</p>

<h2>🐢 Brute force first</h2>
<p>The general-tree LCA ([[236]]) is O(n). The BST version exploits ordering for an O(h) walk.</p>

<div class="insight">💡 <strong>Key insight:</strong> from the root, if both values are smaller, the LCA is in the left subtree; if both are larger, it's in the right; otherwise the current node is where they diverge — that's the LCA.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>cur = root</code>.</li>
<li>Both values &lt; <code>cur.val</code> → go left; both &gt; → go right.</li>
<li>Otherwise return <code>cur</code>.</li>
</ol>

<h2>🎞️ Visual dry run — BST root 6, p=2, q=8</h2>
<pre class="viz">at 6: 2&lt;6 and 8&gt;6 → they split → LCA = 6</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def lowestCommonAncestor(root, p, q):
    cur = root
    while cur:
        if p.val &lt; cur.val and q.val &lt; cur.val:
            cur = cur.left            # both in the left subtree
        elif p.val &gt; cur.val and q.val &gt; cur.val:
            cur = cur.right           # both in the right subtree
        else:
            return cur                # they split here (or one is cur)
    return None</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(h)</strong> — one descent. <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>One node is an ancestor of the other → returned when the walk reaches it.</li>
<li>p and q on opposite sides of the root → root is the LCA.</li>
<li>Values equal to a node → that node splits the pair.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Ignoring the BST property and doing the O(n) general search.</li>
<li>Strict vs non-strict comparisons when one value equals the node.</li>
<li>Recursing unnecessarily (a loop suffices).</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>General binary tree LCA ([[236]]).</li>
<li>Distance between two BST nodes → depths from the LCA.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[236]] · [[98]] · [[285]]</p>
''',

# ============================================================ LC 236 — Lowest Common Ancestor of a Binary Tree
236: '''
<h2>🧭 How to think about it</h2>
<p>No BST ordering here, so search structurally. A node is the LCA if <code>p</code> and <code>q</code> lie in <strong>different subtrees</strong> of it — or the node itself is one of them. A <strong>postorder</strong> recursion that reports "did I find p or q below?" pinpoints exactly that node.</p>

<h2>🐢 Brute force first</h2>
<p>Find the root-to-<code>p</code> and root-to-<code>q</code> paths, then compare to find the last shared node → O(n) time and space. The postorder recursion is O(n) time, O(h) space and more elegant.</p>

<div class="insight">💡 <strong>Key insight:</strong> recurse; if a node <em>is</em> <code>p</code> or <code>q</code>, return it. If both left and right recursions return non-null, this node is the LCA. Otherwise bubble up whichever side found something.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Null or matching node → return it.</li>
<li>Recurse left and right.</li>
<li>Both non-null → current node is the LCA; else return the non-null side.</li>
</ol>

<h2>🎞️ Visual dry run — p and q in different subtrees of node X</h2>
<pre class="viz">left returns p, right returns q → both non-null → X is LCA
if only left non-null → LCA is up the left branch</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def lowestCommonAncestor(root, p, q):
    if not root or root is p or root is q:
        return root                    # found one, or dead end
    left = lowestCommonAncestor(root.left, p, q)
    right = lowestCommonAncestor(root.right, p, q)
    if left and right:
        return root                    # p and q split here → LCA
    return left or right               # bubble up the found side</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong>, <strong>Space O(h)</strong> recursion.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>One node is an ancestor of the other → that ancestor is returned early.</li>
<li>Both guaranteed present (per constraints) → always finds an LCA.</li>
<li>Root is the LCA → both sides return non-null.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Comparing values instead of node identity (there can be duplicate values in the general case; use <code>is</code>).</li>
<li>Returning too early and missing the split node.</li>
<li>Assuming BST ordering.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>With parent pointers → walk up like list-intersection.</li>
<li>LCA of deepest leaves ([[1123]]); step-by-step directions ([[2096]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[235]] · [[1123]] · [[2096]]</p>
''',

# ============================================================ LC 1123 — Lowest Common Ancestor of Deepest Leaves
1123: '''
<h2>🧭 How to think about it</h2>
<p>Find the LCA of all the <em>deepest</em> leaves. A node is that LCA when its left and right subtrees have the <strong>same height</strong> (both reach the deepest level); if one side is deeper, the answer lies on that side. Compute height and LCA together in one postorder pass, returning a <code>(depth, node)</code> pair.</p>

<h2>🐢 Brute force first</h2>
<p>Find the max depth, collect all deepest leaves, then compute their LCA separately → multiple passes. Combining depth and LCA into one return value does it in a single O(n) pass.</p>

<div class="insight">💡 <strong>Key insight:</strong> each call returns <code>(height, lca_of_deepest_below)</code>. If left height == right height, this node is the LCA of its deepest leaves. If left is deeper, propagate the left result; if right is deeper, the right.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Postorder returning <code>(depth, node)</code>.</li>
<li>Equal child depths → return <code>(depth+1, current node)</code>.</li>
<li>Otherwise return the deeper child's pair with depth incremented.</li>
</ol>

<h2>🎞️ Visual dry run — balanced deepest leaves under node X</h2>
<pre class="viz">left depth == right depth at X → X is the LCA
unequal → follow the deeper subtree</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def lcaDeepestLeaves(root):
    def dfs(node):
        if not node:
            return (0, None)           # (depth, lca)
        ld, lnode = dfs(node.left)
        rd, rnode = dfs(node.right)
        if ld == rd:
            return (ld + 1, node)      # balanced → this node is the LCA
        if ld &gt; rd:
            return (ld + 1, lnode)      # deeper on the left
        return (rd + 1, rnode)          # deeper on the right
    return dfs(root)[1]</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — one pass. <strong>Space O(h)</strong> recursion.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Single deepest leaf → the LCA is that leaf.</li>
<li>Perfectly balanced tree → the root is the answer.</li>
<li>Single node → itself.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Doing separate passes and re-deriving the LCA.</li>
<li>Returning the node without the depth (you need both to decide).</li>
<li>Mishandling the equal-depth case (that's exactly the LCA node).</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Same as LeetCode 865 (identical problem).</li>
<li>General LCA of two nodes ([[236]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[236]] · [[543]] · [[104]]</p>
''',

# ============================================================ LC 2096 — Step-By-Step Directions From a Binary Tree Node to Another
2096: '''
<h2>🧭 How to think about it</h2>
<p>Give the shortest path from node <code>startValue</code> to <code>destValue</code> as a string of <code>'U'</code> (up), <code>'L'</code>, <code>'R'</code>. Every path in a tree goes up to the <strong>lowest common ancestor</strong>, then down. So find the root-to-start and root-to-dest paths, drop their common prefix (that's the LCA), replace the start's remaining steps with <code>'U'</code>s, and append the dest's remaining steps.</p>

<h2>🐢 Brute force first</h2>
<p>BFS the whole tree as a graph → works but heavier. The path-and-LCA approach is O(n) and directly yields the directions.</p>

<div class="insight">💡 <strong>Key insight:</strong> record the root-to-node direction strings for both targets. Their shared prefix leads to the LCA. From start you go <code>'U'</code> once per remaining step up to the LCA; then follow dest's remaining <code>'L'/'R'</code> steps down.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>DFS to build the path string from root to <code>startValue</code> and to <code>destValue</code>.</li>
<li>Strip the common prefix.</li>
<li>Answer = <code>'U' × len(remaining start path)</code> + <code>remaining dest path</code>.</li>
</ol>

<h2>🎞️ Visual dry run — start path "LL", dest path "R"</h2>
<pre class="viz">common prefix "" → up 2 from start ("UU"), then dest "R"
Directions: "UUR"</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def getDirections(root, startValue, destValue):
    def find(node, value, path):
        if not node:
            return False
        if node.val == value:
            return True
        path.append('L')
        if find(node.left, value, path):
            return True
        path[-1] = 'R'
        if find(node.right, value, path):
            return True
        path.pop()                       # backtrack
        return False

    sp, dp = [], []
    find(root, startValue, sp)
    find(root, destValue, dp)
    # drop common prefix (path down to the LCA)
    i = 0
    while i &lt; len(sp) and i &lt; len(dp) and sp[i] == dp[i]:
        i += 1
    return 'U' * (len(sp) - i) + ''.join(dp[i:])</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — two path searches. <strong>Space O(n)</strong> for the paths/recursion.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Start is an ancestor of dest → all-down path (no <code>'U'</code>).</li>
<li>Dest is an ancestor of start → all-<code>'U'</code> path.</li>
<li>Start == dest is disallowed by constraints (paths differ).</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Forgetting to backtrack in the path search.</li>
<li>Not stripping the shared prefix (over-counting <code>'U'</code>s).</li>
<li>Using node identity when values are unique here (values are fine).</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Return the LCA node itself ([[236]]).</li>
<li>Distance (not directions) between nodes → sum of remaining lengths.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[236]] · [[863]] · [[257]]</p>
''',

# ============================================================ LC 297 — Serialize and Deserialize Binary Tree
297: '''
<h2>🧭 How to think about it</h2>
<p>Turn a tree into a string and back. A <strong>preorder</strong> walk that writes an explicit marker (like <code>"#"</code>) for every null child produces a string that reconstructs the tree <em>uniquely</em> — the nulls pin down the exact shape.</p>

<h2>🐢 Brute force first</h2>
<p>Storing inorder + preorder needs two arrays and assumes unique values. Preorder-with-null-markers is self-contained, handles duplicates, and is O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> serialize by preorder, emitting <code>node.val</code> or <code>"#"</code> for null. Deserialize by consuming tokens left-to-right with an iterator: a <code>"#"</code> is a null; otherwise create the node and recursively build its left then right children.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Serialize: preorder append <code>val</code> or <code>"#"</code>, joined by commas.</li>
<li>Deserialize: read tokens in order; <code>"#"</code> → null; else build node, recurse left, recurse right.</li>
</ol>

<h2>🎞️ Visual dry run — [1,2,3,null,null,4,5]</h2>
<pre class="viz">serialize → "1,2,#,#,3,4,#,#,5,#,#"
deserialize consumes tokens preorder → rebuilds the same tree</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>class Codec:
    def serialize(self, root):
        out = []
        def dfs(node):
            if not node:
                out.append('#'); return
            out.append(str(node.val))
            dfs(node.left); dfs(node.right)
        dfs(root)
        return ','.join(out)

    def deserialize(self, data):
        it = iter(data.split(','))
        def build():
            val = next(it)
            if val == '#':
                return None
            node = TreeNode(int(val))
            node.left = build()          # preorder: left then right
            node.right = build()
            return node
        return build()</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> for both directions. <strong>Space O(n)</strong> for the string and recursion.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Empty tree → serializes to just a marker; deserializes to null.</li>
<li>Negative values → handled as strings.</li>
<li>Skewed trees → many markers but still correct.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Omitting null markers → ambiguous, non-reconstructible strings.</li>
<li>Building right before left during deserialize (must mirror the serialize order).</li>
<li>Splitting the string incorrectly (delimiter collisions with values).</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>BST-specific serialization can skip markers using ranges.</li>
<li>Find duplicate subtrees via serialization ([[652]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[652]] · [[105]] · [[449]]</p>
''',

# ============================================================ LC 652 — Find Duplicate Subtrees
652: '''
<h2>🧭 How to think about it</h2>
<p>Return one representative root for each subtree shape+values that appears more than once. Give every subtree a <strong>canonical serialization</strong> (a string capturing its structure and values); identical subtrees produce identical strings. Count strings in a hash map and report those seen exactly twice.</p>

<h2>🐢 Brute force first</h2>
<p>Comparing every pair of subtrees is O(n²) comparisons, each O(n). Serializing each subtree once and hashing is O(n²) worst case for string sizes but conceptually clean; ID-based hashing reaches O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> a postorder serialization <code>"val,leftSerial,rightSerial"</code> uniquely identifies a subtree. Store counts in a dict; the first time a serialization's count hits 2, add that subtree's root to the answer (so each duplicate is reported once).</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Postorder build each subtree's serialization from its children's.</li>
<li>Increment a counter for that string.</li>
<li>When a string's count becomes exactly 2, record the current node.</li>
</ol>

<h2>🎞️ Visual dry run — subtree "2,4,#,#" appears twice</h2>
<pre class="viz">first "2,4,#,#" → count 1
second occurrence → count 2 → add its root to answer
Result: one node per duplicated subtree</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>from collections import defaultdict
def findDuplicateSubtrees(root):
    count = defaultdict(int)
    res = []
    def serialize(node):
        if not node:
            return '#'
        s = f"{node.val},{serialize(node.left)},{serialize(node.right)}"
        count[s] += 1
        if count[s] == 2:               # record once, on the second sighting
            res.append(node)
        return s
    serialize(root)
    return res</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n²)</strong> worst case — serialization strings can be O(n) long. <strong>Space O(n²)</strong> for the map (O(n) with subtree-ID encoding).</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>No duplicates → empty result.</li>
<li>A subtree appearing 3+ times → still reported once (count == 2 trigger).</li>
<li>Single node duplicates → matched by value with null children.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Ambiguous serialization without null markers or delimiters.</li>
<li>Reporting a subtree multiple times (guard on count == 2 exactly).</li>
<li>Comparing subtrees pairwise (too slow).</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Assign integer IDs to serializations for O(n) total.</li>
<li>Serialize/deserialize a whole tree ([[297]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[297]] · [[572]] · [[100]]</p>
''',
}
