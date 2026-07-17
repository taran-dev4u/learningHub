# Deep tutorials — Pattern P2: Array / Matrix Manipulation (Session 3).
# Original teaching content written for this site. Keyed by LC number;
# content_problems.py merges this as (2, lc). build.py turns [[nn]] into links.

DEEP = {

# ============================================================ LC 48 — Rotate Image
48: '''
<h2>🧭 How to think about it</h2>
<p>Rotate an n×n matrix 90° clockwise, <em>in place</em>. Trying to move each element straight to its rotated spot means juggling four values at once — error-prone. The clean trick is to build the rotation out of two simple, well-understood moves you can each do in place: a <strong>transpose</strong> (flip across the main diagonal) followed by <strong>reversing every row</strong>.</p>

<h2>🐢 Brute force first</h2>
<p>Allocate a fresh n×n matrix and copy <code>new[j][n−1−i] = old[i][j]</code>. Simple, O(n²) time, but O(n²) extra space — the problem asks for in-place.</p>

<div class="insight">💡 <strong>Key insight:</strong> a 90° clockwise rotation equals <strong>transpose then reverse each row</strong>. Transpose swaps <code>(i,j)</code> with <code>(j,i)</code> — only the upper triangle, so no double-swaps. Reversing each row then slides the columns into rotated position. Both steps are in place.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Transpose: for <code>i</code> in 0..n−1, for <code>j</code> in <code>i+1</code>..n−1, swap <code>M[i][j]</code> and <code>M[j][i]</code>.</li>
<li>Reverse each row.</li>
</ol>

<h2>🎞️ Visual dry run — 3×3</h2>
<pre class="viz">start        transpose      reverse rows (→ 90° CW)
1 2 3        1 4 7          7 4 1
4 5 6   →    2 5 8    →     8 5 2
7 8 9        3 6 9          9 6 3</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def rotate(matrix):
    n = len(matrix)
    # 1) transpose: swap across the main diagonal (upper triangle only)
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    # 2) reverse each row in place
    for row in matrix:
        row.reverse()</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n²)</strong> — every cell is touched a constant number of times. <strong>Space O(1)</strong> — all swaps happen inside the matrix.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>n = 1 → nothing changes.</li>
<li>Even vs odd n → the transpose loop (<code>j &gt; i</code>) covers each pair exactly once either way.</li>
<li>Rotating counter-clockwise → reverse each row <em>first</em>, then transpose (or transpose then reverse columns).</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Transposing the whole matrix (both triangles) — you swap every pair twice and end up unchanged.</li>
<li>Reversing columns instead of rows (that gives counter-clockwise).</li>
<li>Allocating a new matrix and reassigning — not in place.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>180° → reverse rows and reverse each row (or rotate 90° twice).</li>
<li>Rectangular m×n rotation → must use O(m·n) extra space; the in-place trick needs a square.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[54]] · [[73]] · [[189]]</p>
''',

# ============================================================ LC 189 — Rotate Array
189: '''
<h2>🧭 How to think about it</h2>
<p>Shift every element <code>k</code> places to the right, wrapping around. The elegant in-place method is the <strong>triple reverse</strong>: reverse the whole array, then reverse the first <code>k</code> and the rest separately. Reversing flips order; doing it in the right three chunks lands everything in the rotated position.</p>

<h2>🐢 Brute force first</h2>
<p>Copy into a new array at <code>(i+k) % n</code> → O(n) space. Or rotate one step at a time k times → O(n·k), too slow. The triple reverse is O(n) time, O(1) space.</p>

<div class="insight">💡 <strong>Key insight:</strong> rotating right by <code>k</code> moves the last <code>k</code> elements to the front. Reverse the entire array (last k are now at the front but backwards), then reverse those first <code>k</code> and reverse the remaining <code>n−k</code> to fix their internal order. Always take <code>k %= n</code> first.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>k %= n</code> (rotating by n is a no-op).</li>
<li>Reverse the whole array.</li>
<li>Reverse the first <code>k</code> elements.</li>
<li>Reverse the last <code>n−k</code> elements.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [1,2,3,4,5,6,7], k = 3</h2>
<pre class="viz">reverse all      → 7 6 5 4 3 2 1
reverse first 3  → 5 6 7 4 3 2 1
reverse last 4   → 5 6 7 1 2 3 4  ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def rotate(nums, k):
    n = len(nums)
    k %= n                          # more than n wraps around
    def rev(i, j):
        while i &lt; j:
            nums[i], nums[j] = nums[j], nums[i]
            i += 1; j -= 1
    rev(0, n - 1)                   # whole array
    rev(0, k - 1)                   # first k
    rev(k, n - 1)                   # the rest</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — three linear reversals. <strong>Space O(1)</strong> — swaps in place.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li><code>k</code> a multiple of n → <code>k % n == 0</code>, array unchanged.</li>
<li><code>k &gt; n</code> → the modulo handles it.</li>
<li>Single element → no-op.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Forgetting <code>k %= n</code> → index errors or wrong rotation when <code>k ≥ n</code>.</li>
<li>Reversing the wrong two sub-ranges (mixing up <code>k</code> vs <code>n−k</code>).</li>
<li>Rotating left instead of right (the chunk sizes swap).</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Rotate left by k → same trick with reversed chunk order, or rotate right by <code>n−k</code>.</li>
<li>Cyclic-replacement method (juggling) → O(1) space too, but trickier with GCD cycles.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[48]] · [[344]] · [[61]]</p>
''',

# ============================================================ LC 54 — Spiral Matrix
54: '''
<h2>🧭 How to think about it</h2>
<p>Read a matrix in spiral order: top row left-to-right, right column top-to-bottom, bottom row right-to-left, left column bottom-to-top, then spiral inward. Track <strong>four boundaries</strong> — top, bottom, left, right — and shrink the relevant one after walking each side.</p>

<h2>🐢 Brute force first</h2>
<p>Simulate with a visited-matrix and turn right whenever you'd step off-grid or onto a visited cell — O(m·n) time and O(m·n) space. The four-boundary method needs no visited array.</p>

<div class="insight">💡 <strong>Key insight:</strong> keep <code>top, bottom, left, right</code>. Walk the top row then <code>top += 1</code>; the right column then <code>right -= 1</code>; the bottom row then <code>bottom -= 1</code>; the left column then <code>left += 1</code>. Re-check <code>top ≤ bottom</code> and <code>left ≤ right</code> before the bottom/left passes so a thin leftover strip isn't double-counted.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Set boundaries to the matrix edges; <code>res = []</code>.</li>
<li>While <code>top ≤ bottom</code> and <code>left ≤ right</code>: walk top row → shrink top; right col → shrink right; if still valid, bottom row → shrink bottom; left col → shrink left.</li>
</ol>

<h2>🎞️ Visual dry run — 3×3</h2>
<pre class="viz">1 2 3      top row: 1 2 3
4 5 6      right col: 6 9
7 8 9      bottom row: 8 7
           left col: 4
           inner: 5
Result: [1,2,3,6,9,8,7,4,5]</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def spiralOrder(matrix):
    if not matrix:
        return []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    res = []
    while top &lt;= bottom and left &lt;= right:
        for c in range(left, right + 1):     # top row →
            res.append(matrix[top][c])
        top += 1
        for r in range(top, bottom + 1):     # right col ↓
            res.append(matrix[r][right])
        right -= 1
        if top &lt;= bottom:                     # bottom row ← (guard thin strip)
            for c in range(right, left - 1, -1):
                res.append(matrix[bottom][c])
            bottom -= 1
        if left &lt;= right:                     # left col ↑
            for r in range(bottom, top - 1, -1):
                res.append(matrix[r][left])
            left += 1
    return res</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(m·n)</strong> — each cell appended once. <strong>Space O(1)</strong> beyond the output.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Single row or single column → the two guards prevent re-reading it.</li>
<li>Empty matrix → return empty.</li>
<li>Non-square → boundaries handle rectangles naturally.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Omitting the <code>top ≤ bottom</code> / <code>left ≤ right</code> guards → a middle row or column gets read twice.</li>
<li>Off-by-one in the reverse-direction ranges.</li>
<li>Forgetting to shrink a boundary after its pass → infinite loop.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Generate a spiral matrix (Spiral Matrix II) → same walk, writing values 1..n².</li>
<li>Spiral starting from an arbitrary cell ([[885]]) or filling from a list ([[2326]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[885]] · [[2326]] · [[48]]</p>
''',

# ============================================================ LC 885 — Spiral Matrix III
885: '''
<h2>🧭 How to think about it</h2>
<p>Start at a given cell and walk outward in a clockwise spiral, collecting cells that fall <em>inside</em> the grid, until you've collected them all. Here you don't track boundaries — you follow the spiral's natural rhythm: go 1 step, 1 step, 2 steps, 2 steps, 3 steps, 3 steps… turning right each time, and simply skip positions that land off the grid.</p>

<h2>🐢 Brute force first</h2>
<p>There's no simpler correct simulation — you must physically trace the spiral because the start is off-center. The trick is knowing the step-length pattern so you never wander aimlessly.</p>

<div class="insight">💡 <strong>Key insight:</strong> a spiral's segment lengths go <code>1,1,2,2,3,3,…</code>. Move in directions East, South, West, North, cycling; after every <em>two</em> direction changes the step length grows by 1. Record any position that's within bounds; stop once you've recorded <code>rows×cols</code> cells.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Directions in order: E(0,1), S(1,0), W(0,−1), N(−1,0). Start at <code>(r0,c0)</code>, record it.</li>
<li>Repeat: for two consecutive directions, walk <code>len</code> steps each, recording in-bounds cells; then <code>len += 1</code>.</li>
<li>Stop when all <code>rows·cols</code> cells are collected.</li>
</ol>

<h2>🎞️ Visual dry run — rows=1,cols=4,start=(0,0)</h2>
<pre class="viz">record (0,0)
E len1: (0,1) in → record
S len1: (1,1) out → skip
W len2: (1,0)out,(1,-1)out → skip
N len2: (0,-1)out,(-1,-1)out → skip
E len3: (-1,0)out,(-1,1)... (0,2) in → record; (0,3) in → record
collected 4 = 1×4 → done
Result: [[0,0],[0,1],[0,2],[0,3]]</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def spiralMatrixIII(rows, cols, rStart, cStart):
    res = [[rStart, cStart]]
    total = rows * cols
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]   # E, S, W, N
    r, c = rStart, cStart
    step, d = 1, 0
    while len(res) &lt; total:
        for _ in range(2):                       # two segments per length
            dr, dc = dirs[d % 4]
            for _ in range(step):
                r += dr; c += dc
                if 0 &lt;= r &lt; rows and 0 &lt;= c &lt; cols:
                    res.append([r, c])
            d += 1                                # turn right
        step += 1                                 # grow after every 2 turns
    return res</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(max(rows,cols)²)</strong> — the spiral may wander well outside the grid before filling it; work is bounded by the enclosing square. <strong>Space O(rows·cols)</strong> for the output.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Start in a corner → many early steps land out of bounds and are skipped.</li>
<li>Single cell grid → the initial record already completes it.</li>
<li>Very elongated grid → the spiral overshoots a lot; still correct.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Growing the step length every turn instead of every <em>two</em> turns.</li>
<li>Forgetting to record the starting cell before moving.</li>
<li>Stopping on step count rather than on collected-cell count.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Counter-clockwise → reverse the direction list.</li>
<li>Standard inward spiral read ([[54]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[54]] · [[2326]] · [[48]]</p>
''',

# ============================================================ LC 2326 — Spiral Matrix IV
2326: '''
<h2>🧭 How to think about it</h2>
<p>Fill an m×n matrix with the values of a linked list in spiral order, and put <code>−1</code> wherever the list runs out. This is the four-boundary spiral of [[54]], but instead of <em>reading</em> cells you <em>write</em> them — advancing the list pointer as you go and leaving the pre-filled <code>−1</code>s where the list ends.</p>

<h2>🐢 Brute force first</h2>
<p>No meaningfully different approach — you must traverse in spiral order. The only design choice is initializing the grid to <code>−1</code> so untouched cells are already correct.</p>

<div class="insight">💡 <strong>Key insight:</strong> pre-fill the matrix with <code>−1</code>. Run the exact four-boundary spiral walk; at each cell write <code>node.val</code> and advance <code>node</code> — but stop writing as soon as <code>node</code> is <code>None</code>. The leftover <code>−1</code>s need no special handling.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Create <code>grid = m×n</code> filled with <code>−1</code>; set boundaries.</li>
<li>Spiral-walk (top→right→bottom→left, shrinking each boundary).</li>
<li>At each visited cell, if <code>node</code> exists, write its value and move to <code>node.next</code>.</li>
<li>Stop early once the list is exhausted (or just let the writes become no-ops).</li>
</ol>

<h2>🎞️ Visual dry run — m=2,n=3, list = 3→0→2→6→8→1→7</h2>
<pre class="viz">grid starts all -1
top row →   : 3 0 2
right col ↓ : 6
bottom ←    : 8 1
left col ↑  : 7   (list ends here)
Result: [[3,0,2],[7,1,6]]  ... wait, order: [[3,0,2],[7,1,6]]</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def spiralMatrix(m, n, head):
    grid = [[-1] * n for _ in range(m)]
    top, bottom, left, right = 0, m - 1, 0, n - 1
    node = head
    while node and top &lt;= bottom and left &lt;= right:
        for c in range(left, right + 1):
            if node: grid[top][c] = node.val; node = node.next
        top += 1
        for r in range(top, bottom + 1):
            if node: grid[r][right] = node.val; node = node.next
        right -= 1
        if top &lt;= bottom:
            for c in range(right, left - 1, -1):
                if node: grid[bottom][c] = node.val; node = node.next
            bottom -= 1
        if left &lt;= right:
            for r in range(bottom, top - 1, -1):
                if node: grid[r][left] = node.val; node = node.next
            left += 1
    return grid</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(m·n)</strong> — every cell visited once. <strong>Space O(1)</strong> extra beyond the required grid.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>List shorter than m·n → remaining cells stay <code>−1</code>.</li>
<li>List longer than m·n → extra nodes are ignored (walk ends when the grid is full).</li>
<li>Single row/column → the two guards prevent overwrites.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Forgetting to initialize with <code>−1</code>, then trying to fill blanks afterward.</li>
<li>Advancing <code>node</code> even when it's <code>None</code> → crash.</li>
<li>Dropping the boundary guards → double-writing a thin strip.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Read a matrix into a list (inverse) → the [[54]] walk collecting values.</li>
<li>Fill with a different traversal (diagonal, zigzag) → swap the walk.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[54]] · [[885]] · [[206]]</p>
''',

# ============================================================ LC 73 — Set Matrix Zeroes
73: '''
<h2>🧭 How to think about it</h2>
<p>If a cell is 0, zero out its whole row and column — but do it <em>without</em> a separate copy. The problem is timing: if you zero a row immediately, those new zeros will wrongly trigger more rows/columns. The fix is to first <strong>mark</strong> which rows and columns need clearing, then clear them in a second pass. And to reach O(1) space, use the matrix's own first row and first column as the mark storage.</p>

<h2>🐢 Brute force first</h2>
<p>Record every original zero's (row, col), then clear — O(m·n) time, O(m+n) space with two sets. Using the first row/column as markers drops the extra space to O(1).</p>

<div class="insight">💡 <strong>Key insight:</strong> let <code>matrix[i][0]</code> and <code>matrix[0][j]</code> remember "row i / column j must be zeroed". Because the first row and first column overlap at <code>(0,0)</code>, track whether the first column itself needs zeroing in a single extra boolean. Then clear the interior using the marks, and finally clear the first row/column if flagged.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Scan for a zero in column 0 → remember with a boolean <code>col0</code>.</li>
<li>For every interior zero, set its row-marker <code>matrix[i][0]=0</code> and column-marker <code>matrix[0][j]=0</code>.</li>
<li>Second pass over the interior: zero <code>matrix[i][j]</code> if its row or column marker is 0.</li>
<li>Handle the first row (if <code>matrix[0][0]==0</code>) and first column (if <code>col0</code>) last.</li>
</ol>

<h2>🎞️ Visual dry run — [[1,1,1],[1,0,1],[1,1,1]]</h2>
<pre class="viz">zero at (1,1) → mark row1: M[1][0]=0 ; col1: M[0][1]=0
second pass: any cell whose M[i][0]==0 or M[0][j]==0 → 0
Result: [[1,0,1],[0,0,0],[1,0,1]]</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def setZeroes(matrix):
    m, n = len(matrix), len(matrix[0])
    col0 = any(matrix[i][0] == 0 for i in range(m))   # does column 0 need zeroing?
    for i in range(m):
        for j in range(1, n):
            if matrix[i][j] == 0:
                matrix[i][0] = 0        # mark this row
                matrix[0][j] = 0        # mark this column
    for i in range(m - 1, -1, -1):      # go bottom-up so row 0 markers survive
        for j in range(n - 1, 0, -1):
            if matrix[i][0] == 0 or matrix[0][j] == 0:
                matrix[i][j] = 0
        if col0:
            matrix[i][0] = 0
    return matrix</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(m·n)</strong> — two passes. <strong>Space O(1)</strong> — the matrix stores its own markers plus one boolean.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Zero already in the first row/column → captured by the markers and the <code>col0</code> flag.</li>
<li>All zeros → whole matrix zero.</li>
<li>No zeros → unchanged.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Clearing rows/columns during the first scan → cascades and zeros everything.</li>
<li>Forgetting the first-column overlap, so <code>(0,0)</code> can't encode both — hence the separate <code>col0</code> boolean.</li>
<li>Processing the interior top-down and wiping the row-0 markers before you use them (iterate bottom-up, or clear row 0 last).</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>O(m+n) space with two sets → the clear first answer to state before optimizing.</li>
<li>Set to a value other than zero → same marking idea.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[54]] · [[48]] · [[238]]</p>
''',

# ============================================================ LC 238 — Product of Array Except Self
238: '''
<h2>🧭 How to think about it</h2>
<p><code>answer[i]</code> is the product of everything <em>except</em> <code>nums[i]</code> — and you can't use division. Split the idea: the answer for position <code>i</code> is (product of all elements to its <strong>left</strong>) × (product of all elements to its <strong>right</strong>). Two sweeps compute those, and you can store both in the output array itself.</p>

<h2>🐢 Brute force first</h2>
<p>For each <code>i</code>, multiply all others → O(n²). Division would give O(n) but breaks on zeros and is banned. The two-sweep prefix/suffix method is O(n) with no division.</p>

<div class="insight">💡 <strong>Key insight:</strong> first pass left-to-right fills <code>answer[i]</code> with the running product of everything before <code>i</code>. Second pass right-to-left multiplies in a running product of everything after <code>i</code>. No extra arrays needed beyond the output and one scalar.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>answer[i] = product of nums[0..i-1]</code> via a left sweep (start prefix = 1).</li>
<li>Sweep right with a running <code>suffix</code> (start 1): <code>answer[i] *= suffix</code>, then <code>suffix *= nums[i]</code>.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [1,2,3,4]</h2>
<pre class="viz">left pass (prefix products):  answer = [1, 1, 2, 6]
right pass (suffix):
 i=3: ans[3]*=1 →6 ; suffix=4
 i=2: ans[2]*=4 →8 ; suffix=12
 i=1: ans[1]*=12→12; suffix=24
 i=0: ans[0]*=24→24; suffix=24
Result: [24,12,8,6]</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def productExceptSelf(nums):
    n = len(nums)
    answer = [1] * n
    prefix = 1
    for i in range(n):
        answer[i] = prefix          # product of everything left of i
        prefix *= nums[i]
    suffix = 1
    for i in range(n - 1, -1, -1):
        answer[i] *= suffix         # multiply in product of everything right of i
        suffix *= nums[i]
    return answer</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — two passes. <strong>Space O(1)</strong> extra (the output array doesn't count).</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>One zero → its position gets the product of the others; every other position is 0.</li>
<li>Two or more zeros → all positions are 0.</li>
<li>Negatives → signs handled by ordinary multiplication.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Using division — fails when any element is 0.</li>
<li>Storing the value at <code>i</code> after already multiplying by <code>nums[i]</code> (order of update matters in each sweep).</li>
<li>Allocating separate prefix and suffix arrays when a scalar suffices.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Allowed division + no zeros → total product ÷ nums[i].</li>
<li>Sum except self → prefix/suffix sums, same shape.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[303]] · [[152]] · [[560]]</p>
''',

# ============================================================ LC 66 — Plus One
66: '''
<h2>🧭 How to think about it</h2>
<p>The array is a big number, one digit per slot; add 1. Just do grade-school addition from the <strong>rightmost digit</strong>: add one, and if a digit becomes 10 it rolls to 0 and carries into the next. The only surprise case is all nines (<code>999</code>), where the carry runs off the front and the number grows a digit.</p>

<h2>🐢 Brute force first</h2>
<p>Convert to an int, add 1, convert back — works in Python but sidesteps the point and fails in fixed-width languages for huge inputs. The digit-by-digit carry is the intended O(n) method.</p>

<div class="insight">💡 <strong>Key insight:</strong> walk from the last digit. If it's less than 9, increment and you're done immediately. If it's 9, set it to 0 and carry left. If every digit was 9, you fall off the front — prepend a leading 1.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>For <code>i</code> from the last index down to 0: if <code>digits[i] &lt; 9</code>, increment it and return.</li>
<li>Otherwise set <code>digits[i] = 0</code> and continue (carry).</li>
<li>If the loop finishes, every digit was 9 → return <code>[1] + digits</code>.</li>
</ol>

<h2>🎞️ Visual dry run — digits = [1,2,9]  and  [9,9]</h2>
<pre class="viz">[1,2,9]: i=2 is 9 → 0, carry; i=1 is 2&lt;9 → 3, return → [1,3,0]
[9,9]:   i=1 → 0 carry; i=0 → 0 carry; loop ends → [1] + [0,0] = [1,0,0]</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def plusOne(digits):
    for i in range(len(digits) - 1, -1, -1):
        if digits[i] &lt; 9:
            digits[i] += 1          # no carry → done
            return digits
        digits[i] = 0               # 9 becomes 0, carry continues
    return [1] + digits             # all nines → new leading digit</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — at most one pass. <strong>Space O(1)</strong> in place (O(n) only in the all-nines case for the new array).</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>All nines → length grows by one.</li>
<li>Single digit (e.g., [9]) → becomes [1,0].</li>
<li>No carry (e.g., [1,2,3]) → returns after the first step.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Building the result left-to-right — carries propagate right-to-left.</li>
<li>Forgetting the all-nines case that adds a digit.</li>
<li>Relying on int conversion in a language where the number overflows.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Add two number-arrays → carry across both ([[2]] on linked lists).</li>
<li>Plus one on a linked list ([[369]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[2]] · [[369]] · [[88]]</p>
''',

# ============================================================ LC 88 — Merge Sorted Array
88: '''
<h2>🧭 How to think about it</h2>
<p>Merge <code>nums2</code> into <code>nums1</code>, which has extra space at the end. Merging front-to-back would overwrite values in <code>nums1</code> you haven't placed yet. The fix: fill <strong>from the back</strong>. The largest remaining element goes into the last empty slot, so you never clobber unread data.</p>

<h2>🐢 Brute force first</h2>
<p>Append and sort → O((m+n) log(m+n)). Correct but wasteful. The three-pointer back-merge is O(m+n) and in place.</p>

<div class="insight">💡 <strong>Key insight:</strong> three pointers — <code>i</code> at the last real element of <code>nums1</code>, <code>j</code> at the last of <code>nums2</code>, <code>k</code> at the very end of <code>nums1</code>. Copy the larger of <code>nums1[i]</code>, <code>nums2[j]</code> into <code>nums1[k]</code> and step inward. Writing backward means the slot you write was always going to be filled by something ≥ what's there.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>i = m−1</code>, <code>j = n−1</code>, <code>k = m+n−1</code>.</li>
<li>While <code>j ≥ 0</code>: place the larger of the two current values at <code>k</code>, decrement that pointer and <code>k</code>.</li>
<li>If <code>nums1</code> runs out first, remaining <code>nums2</code> values copy down; if <code>nums2</code> runs out, <code>nums1</code>'s are already in place.</li>
</ol>

<h2>🎞️ Visual dry run — nums1=[1,2,3,0,0,0] m=3, nums2=[2,5,6] n=3</h2>
<pre class="viz">i=2(3) j=2(6) k=5 → 6&gt;3 → nums1[5]=6; j=1,k=4
i=2(3) j=1(5) k=4 → 5&gt;3 → nums1[4]=5; j=0,k=3
i=2(3) j=0(2) k=3 → 3&gt;2 → nums1[3]=3; i=1,k=2
i=1(2) j=0(2) k=2 → 2≥2 → nums1[2]=2; j=-1 stop
Result: [1,2,2,3,5,6]</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def merge(nums1, m, nums2, n):
    i, j, k = m - 1, n - 1, m + n - 1
    while j &gt;= 0:                       # while nums2 has elements left
        if i &gt;= 0 and nums1[i] &gt; nums2[j]:
            nums1[k] = nums1[i]; i -= 1
        else:
            nums1[k] = nums2[j]; j -= 1
        k -= 1</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(m+n)</strong> — each element placed once. <strong>Space O(1)</strong> — merged in place.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li><code>n = 0</code> → nothing to merge; <code>nums1</code> already correct.</li>
<li><code>m = 0</code> → the loop copies all of <code>nums2</code> down.</li>
<li>Duplicates across arrays → the <code>≥</code>/<code>&gt;</code> choice keeps them stable enough (any order of equals is fine).</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Merging front-to-back and overwriting unprocessed <code>nums1</code> values.</li>
<li>Looping on <code>i ≥ 0</code> instead of <code>j ≥ 0</code> — leftover <code>nums2</code> elements would be dropped.</li>
<li>Forgetting the <code>i ≥ 0</code> guard in the comparison → index error.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Merge two lists into a new array → simple forward merge ([[21]] on linked lists).</li>
<li>Merge k arrays → heap-based k-way merge.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[21]] · [[977]] · [[189]]</p>
''',

# ============================================================ LC 41 — First Missing Positive
41: '''
<h2>🧭 How to think about it</h2>
<p>Find the smallest positive integer missing from the array, in O(n) time and O(1) space. The answer must be in <code>1..n+1</code> (with n elements you can't miss anything larger without missing something smaller). So use the array itself as a hash table: put each value <code>v</code> in <code>1..n</code> at its <strong>home index</strong> <code>v−1</code>. Then the first index whose value isn't right reveals the gap.</p>

<h2>🐢 Brute force first</h2>
<p>A set of the values then scan 1,2,3… → O(n) time but O(n) space. Sorting is O(n log n). Cyclic placement achieves O(n)/O(1).</p>

<div class="insight">💡 <strong>Key insight:</strong> repeatedly swap <code>nums[i]</code> to the slot where it belongs (<code>value v</code> → index <code>v−1</code>), as long as it's in range <code>1..n</code> and not already home. After this "cyclic sort", the first position <code>i</code> with <code>nums[i] != i+1</code> means <code>i+1</code> is missing; if all match, the answer is <code>n+1</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>For each <code>i</code>: while <code>1 ≤ nums[i] ≤ n</code> and <code>nums[nums[i]−1] != nums[i]</code>, swap <code>nums[i]</code> to its home.</li>
<li>Scan: the first <code>i</code> with <code>nums[i] != i+1</code> → return <code>i+1</code>.</li>
<li>If none, return <code>n+1</code>.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [3,4,-1,1]</h2>
<pre class="viz">place values into home indices:
[3,4,-1,1] → swap 3→idx2: [-1,4,3,1] → swap? nums[0]=-1 skip
 i=1: 4 out of range(n=4? idx3) → nums[3]=1, home idx0 → swap: [1,4,3,-1]... continue
final ~ [1,-1,3,4]  (1 home, idx1 should be 2 but is -1)
scan: idx1 has -1 != 2 → missing = 2</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def firstMissingPositive(nums):
    n = len(nums)
    for i in range(n):
        # send nums[i] to index nums[i]-1 until it's home or out of range
        while 1 &lt;= nums[i] &lt;= n and nums[nums[i] - 1] != nums[i]:
            j = nums[i] - 1
            nums[i], nums[j] = nums[j], nums[i]
    for i in range(n):
        if nums[i] != i + 1:
            return i + 1            # first gap
    return n + 1                    # 1..n all present</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — each value reaches its home in at most one successful swap, so total swaps are O(n). <strong>Space O(1)</strong> — rearranged in place.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>All negatives / all &gt; n → nothing placed → answer 1.</li>
<li><code>[1,2,3]</code> → all home → answer <code>n+1</code>.</li>
<li>Duplicates → the <code>nums[nums[i]-1] != nums[i]</code> guard stops infinite swapping.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Swapping without the "already home" check → infinite loop on duplicates.</li>
<li>Using <code>while</code> on <code>i</code> incorrectly — the inner loop must keep placing until the current slot is settled.</li>
<li>Off-by-one between value <code>v</code> and index <code>v−1</code>.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Find all missing ([[448]]) or all duplicates ([[442]]) → same home-index idea with sign-marking.</li>
<li>Missing number in 0..n ([[268]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[268]] · [[448]] · [[442]]</p>
''',

# ============================================================ LC 268 — Missing Number
268: '''
<h2>🧭 How to think about it</h2>
<p>The array holds <code>n</code> distinct numbers drawn from <code>0..n</code>, so exactly one is missing. Two clean tricks: the <strong>sum</strong> of <code>0..n</code> minus the actual sum is the missing number; or <strong>XOR</strong> all indices <code>0..n</code> with all values — every present number cancels itself, leaving the missing one.</p>

<h2>🐢 Brute force first</h2>
<p>Sort then find the gap → O(n log n). A boolean seen-array is O(n) space. Sum or XOR give O(n) time and O(1) space with no overflow worries (XOR) .</p>

<div class="insight">💡 <strong>Key insight (XOR):</strong> <code>x ^ x = 0</code> and XOR is commutative. XOR together every index 0..n and every array value; each number that appears both as an index and a value cancels, and the lone survivor is the missing number. The Gauss-sum version is equally valid: <code>n(n+1)/2 − sum(nums)</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Start <code>missing = n</code> (covers the top index that has no matching loop value).</li>
<li>For each <code>i</code>: <code>missing ^= i ^ nums[i]</code>.</li>
<li>Return <code>missing</code>.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [3,0,1] (n=3)</h2>
<pre class="viz">missing=3
i=0: 3 ^ 0 ^ 3 = 0
i=1: 0 ^ 1 ^ 0 = 1
i=2: 1 ^ 2 ^ 1 = 2
Answer: 2   (sum check: 0+1+2+3=6, sum(nums)=4, 6-4=2 ✓)</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def missingNumber(nums):
    n = len(nums)
    missing = n                    # start with the index n (no value pairs with it)
    for i, x in enumerate(nums):
        missing ^= i ^ x           # cancel index and value
    return missing

# Gauss-sum alternative:
# return n * (n + 1) // 2 - sum(nums)</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — one pass. <strong>Space O(1)</strong>. XOR avoids the (small) overflow risk the sum has in fixed-width languages.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Missing 0 → e.g. [1] → answer 0.</li>
<li>Missing n → e.g. [0,1] → answer 2.</li>
<li>Single-element array → returns whichever of 0/1 is absent.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Forgetting to seed <code>missing = n</code> (the top index never appears as a loop index otherwise).</li>
<li>Sum overflow in languages with fixed-width ints.</li>
<li>Assuming the array is sorted.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Cyclic-sort version → place each value at index = value, then find the mismatch ([[41]]).</li>
<li>Two missing numbers → XOR splits into two groups by a set bit.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[41]] · [[448]] · [[136]]</p>
''',

# ============================================================ LC 287 — Find the Duplicate Number
287: '''
<h2>🧭 How to think about it</h2>
<p>This problem lives in two pattern families. Under the <strong>cyclic-sort lens</strong> (this page), the values <code>1..n</code> want to live at home indices, and a duplicate is what blocks a slot. The catch: the official constraints forbid modifying the array and demand O(1) space — which is why the tournament answer is Floyd's cycle detection (taught in full on the Two Pointers version, [[287]]). Here we build the cyclic-sort intuition and note when it applies.</p>

<h2>🐢 Brute force first</h2>
<p>A seen-set finds the repeat in O(n) time / O(n) space. Sorting finds adjacent equals in O(n log n). Both are fine if the constraints are relaxed.</p>

<div class="insight">💡 <strong>Key insight:</strong> if you <em>are</em> allowed to mutate, index-marking works: walk the array, and for value <code>v</code> flip the sign at index <code>|v|−1</code>; the first index you find already negative points to the duplicate. To respect "no modification + O(1) space", read the array as a functional graph <code>i → nums[i]</code> and find the cycle entrance with slow/fast pointers.</div>

<h2>🪜 The approach, step by step (index-marking, if mutation allowed)</h2>
<ol>
<li>For each value <code>v = nums[i]</code>, let <code>idx = abs(v) − 1</code>.</li>
<li>If <code>nums[idx]</code> is already negative, <code>abs(v)</code> is the duplicate.</li>
<li>Otherwise negate <code>nums[idx]</code> to mark it seen.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [1,3,4,2,2] (index-marking)</h2>
<pre class="viz">v=1 → idx0: mark nums[0] neg
v=3 → idx2: mark nums[2] neg
v=4 → idx3: mark nums[3] neg
v=2 → idx1: mark nums[1] neg
v=2 → idx1: already negative → duplicate = 2</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code># Constraint-respecting answer (no mutation, O(1) space): Floyd's cycle detection.
def findDuplicate(nums):
    slow = fast = nums[0]
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
    return slow

# If mutation were allowed, index-marking is simpler:
# for x in nums:
#     idx = abs(x) - 1
#     if nums[idx] &lt; 0: return abs(x)
#     nums[idx] = -nums[idx]</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> for both methods. <strong>Space O(1)</strong>. Floyd also leaves the array untouched, satisfying the strict constraints.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Duplicate appears many times → still one repeated <em>value</em>; both methods return it.</li>
<li>Duplicate equals 1 or n → the functional-graph cycle still forms.</li>
<li>Smallest input (length 2) → the two equal values resolve immediately.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Using index-marking when the problem forbids modifying the array.</li>
<li>Starting Floyd's phase 2 from the meeting point rather than <code>nums[0]</code>.</li>
<li>Confusing "one duplicate value" with "exactly two copies" — it can repeat more.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Binary search on the value range (count ≤ mid) → O(n log n), O(1) space, no mutation.</li>
<li>Find <em>all</em> duplicates when mutation is allowed ([[442]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[442]] · [[448]] · [[41]]</p>
''',

# ============================================================ LC 442 — Find All Duplicates in an Array
442: '''
<h2>🧭 How to think about it</h2>
<p>Every value is in <code>1..n</code> and appears once or twice; return the ones appearing twice, in O(n) time and O(1) extra space. Use the array as its own bookkeeping: for value <code>v</code>, the sign of the slot at index <code>v−1</code> records "have I seen <code>v</code> before?" Flip it to mark; if it's already flipped, <code>v</code> is a duplicate.</p>

<h2>🐢 Brute force first</h2>
<p>A count dict is O(n) time but O(n) space. Sign-marking keeps it O(1) extra because the values fit the index range perfectly.</p>

<div class="insight">💡 <strong>Key insight:</strong> index <code>v−1</code> is <code>v</code>'s home. Negate <code>nums[v−1]</code> the first time you meet <code>v</code>. If you reach a <code>v</code> whose home is already negative, you've seen <code>v</code> before → it's a duplicate. Use <code>abs</code> when reading values, since earlier marks made some negative.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>For each <code>x</code>, let <code>idx = abs(x) − 1</code>.</li>
<li>If <code>nums[idx] &lt; 0</code>, append <code>abs(x)</code> to the result.</li>
<li>Otherwise negate <code>nums[idx]</code>.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [4,3,2,7,8,2,3,1]</h2>
<pre class="viz">x=4→idx3 mark; x=3→idx2 mark; x=2→idx1 mark; x=7→idx6 mark;
x=8→idx7 mark; x=2→idx1 already neg → dup 2;
x=3→idx2 already neg → dup 3; x=1→idx0 mark
Result: [2, 3]</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def findDuplicates(nums):
    res = []
    for x in nums:
        idx = abs(x) - 1           # home slot of value abs(x)
        if nums[idx] &lt; 0:
            res.append(abs(x))     # seen before → duplicate
        else:
            nums[idx] = -nums[idx] # mark as seen
    return res</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — one pass. <strong>Space O(1)</strong> extra (the output aside).</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>No duplicates → empty result; array signs flipped (restore with a second pass if needed).</li>
<li>Every value duplicated → all returned once.</li>
<li>Reading values after marks → always use <code>abs</code>.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Forgetting <code>abs()</code> when computing the index, after some slots turned negative.</li>
<li>Appending the index instead of the value.</li>
<li>Assuming input is sorted.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Find all <em>missing</em> numbers ([[448]]) → same marking, then report positive positions.</li>
<li>Single duplicate with no mutation ([[287]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[448]] · [[287]] · [[41]]</p>
''',

# ============================================================ LC 448 — Find All Numbers Disappeared in an Array
448: '''
<h2>🧭 How to think about it</h2>
<p>Values are in <code>1..n</code>; return those that never appear. Mirror of Find All Duplicates: mark each present value by negating its home slot, then any slot that stayed <strong>positive</strong> corresponds to a number nobody visited — that number is missing.</p>

<h2>🐢 Brute force first</h2>
<p>A set of present values, then scan 1..n → O(n) time, O(n) space. Sign-marking makes it O(1) extra.</p>

<div class="insight">💡 <strong>Key insight:</strong> for each value <code>v</code>, negate <code>nums[v−1]</code> to say "<code>v</code> is present". After the pass, index <code>i</code> still positive means <code>i+1</code> was never marked → <code>i+1</code> is missing.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>For each <code>x</code>, set <code>nums[abs(x)−1]</code> to its negative (if not already).</li>
<li>Scan: every index <code>i</code> with <code>nums[i] &gt; 0</code> → collect <code>i+1</code>.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [4,3,2,7,8,2,3,1]</h2>
<pre class="viz">mark homes of 4,3,2,7,8,2,3,1 → indices 3,2,1,6,7,0 negated
positive slots remain at idx4 and idx5
missing = [5, 6]</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def findDisappearedNumbers(nums):
    for x in nums:
        idx = abs(x) - 1
        if nums[idx] &gt; 0:
            nums[idx] = -nums[idx]     # mark value idx+1 as present
    return [i + 1 for i in range(len(nums)) if nums[i] &gt; 0]</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — two passes. <strong>Space O(1)</strong> extra.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>All numbers present → empty result.</li>
<li>Many duplicates → their extra copies re-negate an already-negative slot (guarded by the <code>&gt; 0</code> check).</li>
<li>Every number missing except one → the rest are reported.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Not guarding with <code>if nums[idx] &gt; 0</code> before negating → double-negation flips it back positive.</li>
<li>Forgetting <code>abs()</code> when indexing.</li>
<li>Reporting indices instead of <code>index+1</code> values.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>First missing positive with arbitrary values ([[41]]).</li>
<li>Find duplicates instead ([[442]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[442]] · [[41]] · [[268]]</p>
''',

# ============================================================ LC 74 — Search a 2D Matrix
74: '''
<h2>🧭 How to think about it</h2>
<p>The matrix is sorted row by row, and each row's first value is greater than the previous row's last — so reading it row after row gives one fully sorted sequence. That means you can run a single <strong>binary search over the m·n virtual array</strong>, converting a flat index back to (row, col) with division and modulo.</p>

<h2>🐢 Brute force first</h2>
<p>Scan every cell → O(m·n). Binary search per row → O(m log n). Treating it as one sorted array → O(log(m·n)), the best.</p>

<div class="insight">💡 <strong>Key insight:</strong> index <code>mid</code> in <code>0..m·n−1</code> maps to <code>matrix[mid // cols][mid % cols]</code>. Now it's a textbook binary search: compare, halve, repeat.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>lo = 0</code>, <code>hi = m·n − 1</code>.</li>
<li><code>mid</code> → value at <code>(mid // n, mid % n)</code>.</li>
<li>Equal → found; less → <code>lo = mid+1</code>; greater → <code>hi = mid−1</code>.</li>
</ol>

<h2>🎞️ Visual dry run — matrix=[[1,3,5,7],[10,11,16,20],[23,30,34,60]], target=3</h2>
<pre class="viz">m=3,n=4 → lo=0 hi=11
mid=5 → (1,1)=11 &gt; 3 → hi=4
mid=2 → (0,2)=5 &gt; 3 → hi=1
mid=0 → (0,0)=1 &lt; 3 → lo=1
mid=1 → (0,1)=3 == 3 → found</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def searchMatrix(matrix, target):
    m, n = len(matrix), len(matrix[0])
    lo, hi = 0, m * n - 1
    while lo &lt;= hi:
        mid = (lo + hi) // 2
        val = matrix[mid // n][mid % n]    # flat index → (row, col)
        if val == target:
            return True
        elif val &lt; target:
            lo = mid + 1
        else:
            hi = mid - 1
    return False</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(log(m·n))</strong> — one binary search. <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Target smaller than the first / larger than the last element → search converges to not-found.</li>
<li>Single row or single column → the index math still works.</li>
<li>Empty matrix → guard by checking dimensions.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Using <code>mid // m</code> / <code>mid % m</code> — must divide by the number of <em>columns</em> <code>n</code>.</li>
<li>Off-by-one in <code>hi = m·n − 1</code>.</li>
<li>Assuming the weaker row/column sorting of [[240]] (different algorithm).</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Rows sorted but not globally ([[240]]) → staircase search.</li>
<li>Count/insert position → lower-bound variant.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[240]] · [[378]] · [[35]]</p>
''',

# ============================================================ LC 240 — Search a 2D Matrix II
240: '''
<h2>🧭 How to think about it</h2>
<p>Here each row and each column is sorted, but there's no global order (a row can start below the previous row's end). Binary search on the flattened array no longer works. Instead, start at a <strong>corner where one direction increases and the other decreases</strong> — the top-right — so every comparison eliminates a whole row or column.</p>

<h2>🐢 Brute force first</h2>
<p>Scan all cells → O(m·n). Binary search each row → O(m log n). The staircase walk is O(m+n), simpler and often faster.</p>

<div class="insight">💡 <strong>Key insight:</strong> at the top-right cell, values to the left are smaller and values below are larger. If it's bigger than the target, the whole column can go (move left); if smaller, the whole row can go (move down). Each step removes a row or a column.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Start at <code>r = 0</code>, <code>c = n−1</code>.</li>
<li>If <code>matrix[r][c] == target</code> → found.</li>
<li>If it's greater than target → <code>c −= 1</code>; if less → <code>r += 1</code>.</li>
<li>Stop when you fall off the grid.</li>
</ol>

<h2>🎞️ Visual dry run — target = 5, matrix rows/cols sorted</h2>
<pre class="viz">start top-right (0, n-1) = large value
  &gt; 5 → move left (drop column)
  &gt; 5 → move left
  &lt; 5 → move down (drop row)
  == 5 → found</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def searchMatrix(matrix, target):
    if not matrix or not matrix[0]:
        return False
    r, c = 0, len(matrix[0]) - 1       # top-right corner
    while r &lt; len(matrix) and c &gt;= 0:
        val = matrix[r][c]
        if val == target:
            return True
        elif val &gt; target:
            c -= 1                      # eliminate this column
        else:
            r += 1                      # eliminate this row
    return False</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(m+n)</strong> — each step drops a row or column. <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Target absent → pointer walks off the grid.</li>
<li>Single row/column → degrades to ordinary linear/binary search behavior.</li>
<li>Empty matrix → early return.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Starting at top-left or bottom-right — those corners don't split the search (both neighbors move the same way).</li>
<li>Trying to reuse the flattened binary search from [[74]] (invalid here).</li>
<li>Boundary errors on <code>r</code>/<code>c</code>.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Count elements ≤ target → same staircase, counting as you go (used in [[378]]).</li>
<li>Start from bottom-left → symmetric alternative.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[74]] · [[378]] · [[240]]</p>
''',

# ============================================================ LC 378 — Kth Smallest Element in a Sorted Matrix
378: '''
<h2>🧭 How to think about it</h2>
<p>Each row and column is sorted; find the k-th smallest value overall. Rather than merging, <strong>binary search on the value range</strong> <code>[matrix[0][0], matrix[n−1][n−1]]</code>: for a candidate value <code>mid</code>, count how many matrix entries are ≤ <code>mid</code> (cheaply, with the staircase from [[240]]). Shrink the range until it collapses to the answer.</p>

<h2>🐢 Brute force first</h2>
<p>Flatten and sort → O(n² log n). A min-heap k-way merge → O(k log n). Binary-search-on-value is O(n log(max−min)), independent of k, and uses O(1) space.</p>

<div class="insight">💡 <strong>Key insight:</strong> "how many entries are ≤ x" is monotonic in x, so binary search the value. Counting is O(n): walk from the bottom-left, moving up when a value exceeds <code>mid</code> and right otherwise, tallying full columns. The smallest value whose count ≥ k is the k-th smallest.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>lo = matrix[0][0]</code>, <code>hi = matrix[n−1][n−1]</code>.</li>
<li><code>mid = (lo+hi)//2</code>; count entries ≤ <code>mid</code> via the staircase.</li>
<li>If count &lt; k → <code>lo = mid+1</code>; else <code>hi = mid</code>.</li>
<li>When <code>lo == hi</code>, that's the answer.</li>
</ol>

<h2>🎞️ Visual dry run — matrix=[[1,5,9],[10,11,13],[12,13,15]], k=8</h2>
<pre class="viz">lo=1 hi=15
mid=8: count(&lt;=8)=2 &lt; 8 → lo=9
mid=12: count(&lt;=12)=6 &lt; 8 → lo=13
mid=14: count(&lt;=14)=8 ≥ 8 → hi=14
mid=13: count(&lt;=13)=8 ≥ 8 → hi=13; lo==hi=13
Answer: 13</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def kthSmallest(matrix, k):
    n = len(matrix)
    def count_le(x):
        # count entries &lt;= x via staircase from bottom-left
        cnt, r, c = 0, n - 1, 0
        while r &gt;= 0 and c &lt; n:
            if matrix[r][c] &lt;= x:
                cnt += r + 1        # whole column up to r qualifies
                c += 1
            else:
                r -= 1
        return cnt

    lo, hi = matrix[0][0], matrix[n - 1][n - 1]
    while lo &lt; hi:
        mid = (lo + hi) // 2
        if count_le(mid) &lt; k:
            lo = mid + 1
        else:
            hi = mid
    return lo</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n · log(max−min))</strong> — each count is O(n), repeated for the value-range binary search. <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li><code>k = 1</code> → smallest = <code>matrix[0][0]</code>; <code>k = n²</code> → largest.</li>
<li>Duplicate values → the "smallest value with count ≥ k" rule still returns a value actually in the matrix.</li>
<li>1×1 matrix → returns its only element.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Using <code>lo = mid+1</code> when count ≥ k (must keep <code>hi = mid</code> to converge onto a real matrix value).</li>
<li>Counting with an O(n²) scan instead of the O(n) staircase.</li>
<li>Assuming the answer is <code>mid</code> — it's the converged <code>lo</code>.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>k-th smallest via a min-heap seeded with the first row → O(k log n).</li>
<li>k-th smallest pair distance / similar "search on the answer" problems.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[240]] · [[74]] · [[215]]</p>
''',

# ============================================================ LC 303 — Range Sum Query - Immutable
303: '''
<h2>🧭 How to think about it</h2>
<p>Many queries ask "sum of <code>nums[i..j]</code>" on an array that never changes. Recomputing each range is wasteful. Precompute a <strong>prefix-sum</strong> array once; then any range sum is a single subtraction — instant per query.</p>

<h2>🐢 Brute force first</h2>
<p>Each query loops <code>i..j</code> → O(n) per query, O(n·q) total. Prefix sums make each query O(1) after an O(n) setup.</p>

<div class="insight">💡 <strong>Key insight:</strong> let <code>prefix[k] = nums[0] + … + nums[k−1]</code> (with <code>prefix[0] = 0</code>). Then <code>sum(i..j) = prefix[j+1] − prefix[i]</code>. The extra leading zero removes all the <code>i == 0</code> special-casing.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>In the constructor, build <code>prefix</code> of length <code>n+1</code> with a running total.</li>
<li><code>sumRange(i, j)</code> returns <code>prefix[j+1] − prefix[i]</code>.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [-2,0,3,-5,2,-1]</h2>
<pre class="viz">prefix = [0, -2, -2, 1, -4, -2, -3]
sumRange(0,2) = prefix[3]-prefix[0] = 1-0 = 1
sumRange(2,5) = prefix[6]-prefix[2] = -3-(-2) = -1</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>class NumArray:
    def __init__(self, nums):
        self.prefix = [0] * (len(nums) + 1)
        for i, x in enumerate(nums):
            self.prefix[i + 1] = self.prefix[i] + x   # running total

    def sumRange(self, i, j):
        return self.prefix[j + 1] - self.prefix[i]    # O(1) range sum</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Build O(n)</strong>, <strong>query O(1)</strong>. <strong>Space O(n)</strong> for the prefix array.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li><code>i == j</code> → returns the single element.</li>
<li>Whole array → <code>prefix[n] − prefix[0]</code>.</li>
<li>Negatives → handled naturally.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Off-by-one: forgetting the leading zero and mixing up <code>prefix[j+1]</code> vs <code>prefix[j]</code>.</li>
<li>Rebuilding prefix sums on every query.</li>
<li>Confusing the inclusive query bounds.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>2-D range sums → 2-D prefix with inclusion-exclusion.</li>
<li>Mutable array (point updates) → Fenwick / segment tree.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[560]] · [[724]] · [[1480]]</p>
''',

# ============================================================ LC 560 — Subarray Sum Equals K
560: '''
<h2>🧭 How to think about it</h2>
<p>Count contiguous subarrays that sum to <code>k</code>. A subarray sum is a difference of two prefix sums: <code>sum(i..j) = prefix[j+1] − prefix[i]</code>. So a subarray ending at <code>j</code> with sum <code>k</code> exists once for every earlier prefix equal to <code>prefix[j+1] − k</code>. Keep a running prefix and a <strong>hash map of how many times each prefix value has occurred</strong>.</p>

<h2>🐢 Brute force first</h2>
<p>All O(n²) subarrays (with a running inner sum) → O(n²). The prefix-count map answers it in one pass, O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> as you sweep, maintain <code>running</code> = prefix sum so far and a dict <code>count[p]</code> = number of prefixes seen with value <code>p</code>. At each step add <code>count[running − k]</code> to the answer (each such earlier prefix starts a valid subarray), then record <code>running</code>. Seed <code>count[0] = 1</code> for subarrays starting at index 0.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>count = {0: 1}</code>, <code>running = 0</code>, <code>ans = 0</code>.</li>
<li>For each <code>x</code>: <code>running += x</code>; <code>ans += count.get(running − k, 0)</code>; then <code>count[running] += 1</code>.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [1,1,1], k = 2</h2>
<pre class="viz">count={0:1} running=0 ans=0
x=1: running=1; need -1 → 0; count={0:1,1:1}
x=1: running=2; need 0 → +1 (ans=1); count={0:1,1:1,2:1}
x=1: running=3; need 1 → +1 (ans=2); count[3]=1
Answer: 2</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>from collections import defaultdict
def subarraySum(nums, k):
    count = defaultdict(int)
    count[0] = 1                    # empty prefix, for subarrays from index 0
    running = 0
    ans = 0
    for x in nums:
        running += x
        ans += count[running - k]   # earlier prefixes that complete a sum of k
        count[running] += 1
    return ans</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — one pass, O(1) map ops. <strong>Space O(n)</strong> for the prefix-count map.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Negative numbers → sliding window fails here; the prefix-map handles them.</li>
<li><code>k = 0</code> → counts subarrays summing to zero.</li>
<li>Whole array equals k → counted via the seeded <code>count[0]=1</code>.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Forgetting <code>count[0] = 1</code> → misses subarrays that start at index 0.</li>
<li>Recording <code>running</code> <em>before</em> adding <code>count[running−k]</code> (over-counts zero-length).</li>
<li>Trying a sliding window with negatives present.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Sum divisible by k ([[974]]) → key on the remainder.</li>
<li>Count subarrays with a given XOR → same map on running XOR.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[974]] · [[930]] · [[303]]</p>
''',

# ============================================================ LC 724 — Find Pivot Index
724: '''
<h2>🧭 How to think about it</h2>
<p>Find an index where the sum to its left equals the sum to its right. Compute the <strong>total</strong> once; then sweep, tracking the running left sum. At each index the right sum is <code>total − left − nums[i]</code>, so you can test the pivot condition in O(1).</p>

<h2>🐢 Brute force first</h2>
<p>For each index sum both sides → O(n²). One prefix sweep with the total precomputed → O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> at index <code>i</code>, left sum is what you've accumulated before <code>i</code>; right sum is <code>total − left − nums[i]</code>. If they're equal, <code>i</code> is the pivot. Add <code>nums[i]</code> to <code>left</code> after the check.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>total = sum(nums)</code>, <code>left = 0</code>.</li>
<li>For each <code>i</code>: if <code>left == total − left − nums[i]</code>, return <code>i</code>.</li>
<li>Else <code>left += nums[i]</code>. If none found, return −1.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [1,7,3,6,5,6]</h2>
<pre class="viz">total=28
i=0 left=0 right=28-0-1=27 → no; left=1
i=1 left=1 right=28-1-7=20 → no; left=8
i=2 left=8 right=28-8-3=17 → no; left=11
i=3 left=11 right=28-11-6=11 → equal → pivot 3</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def pivotIndex(nums):
    total = sum(nums)
    left = 0
    for i, x in enumerate(nums):
        if left == total - left - x:   # right sum = total - left - current
            return i
        left += x
    return -1</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — one sum plus one sweep. <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Pivot at index 0 → left sum 0 must equal the sum of the rest.</li>
<li>Pivot at the last index → right sum 0.</li>
<li>Multiple pivots → return the leftmost.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Adding <code>nums[i]</code> to <code>left</code> before the comparison.</li>
<li>Including <code>nums[i]</code> in either side (the pivot itself belongs to neither).</li>
<li>Returning a boolean instead of the index / −1.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Find all pivots → don't return early.</li>
<li>Balance point by value/weight → weighted prefix sums.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[303]] · [[1480]] · [[560]]</p>
''',

# ============================================================ LC 930 — Binary Subarrays With Sum
930: '''
<h2>🧭 How to think about it</h2>
<p>Count subarrays of a 0/1 array whose sum equals <code>goal</code>. It's the same prefix-sum-count idea as [[560]] — for each running prefix, how many earlier prefixes equal <code>running − goal</code>? A hash map (or, since values are 0/1, a small array) tracks prefix frequencies.</p>

<h2>🐢 Brute force first</h2>
<p>All O(n²) subarrays → too slow for large n. Prefix-count map → O(n). A neat alternative is <em>atMost(goal) − atMost(goal−1)</em> with a sliding window (valid because entries are non-negative).</p>

<div class="insight">💡 <strong>Key insight:</strong> maintain <code>running</code> prefix and <code>count[p]</code> = how many prefixes had value <code>p</code>. Each step adds <code>count[running − goal]</code> to the answer. Seed <code>count[0] = 1</code>. Because entries are non-negative, the sliding-window "atMost" trick also works and uses O(1) space.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>count = {0: 1}</code>, <code>running = 0</code>, <code>ans = 0</code>.</li>
<li>For each <code>x</code>: <code>running += x</code>; <code>ans += count.get(running − goal, 0)</code>; <code>count[running] += 1</code>.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [1,0,1,0,1], goal = 2</h2>
<pre class="viz">count={0:1} running=0 ans=0
1→run1 need -1:0; count{0:1,1:1}
0→run1 need -1:0; count{0:1,1:2}
1→run2 need 0:+1(ans1); count{...,2:1}
0→run2 need 0:+1(ans2); count{...,2:2}
1→run3 need 1:+2(ans4)
Answer: 4</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>from collections import defaultdict
def numSubarraysWithSum(nums, goal):
    count = defaultdict(int)
    count[0] = 1
    running = ans = 0
    for x in nums:
        running += x
        ans += count[running - goal]
        count[running] += 1
    return ans</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — one pass. <strong>Space O(n)</strong> for the map (O(1) with the atMost sliding-window variant).</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li><code>goal = 0</code> → counts runs of consecutive zeros (the map handles it; a naive window would loop forever).</li>
<li>All ones with goal = length → exactly one subarray.</li>
<li>No qualifying subarray → 0.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Sliding window for <code>goal = 0</code> without the atMost subtraction → infinite/incorrect.</li>
<li>Forgetting <code>count[0] = 1</code>.</li>
<li>Ordering the update before the count read.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>atMost(goal) − atMost(goal−1) sliding window → O(1) space.</li>
<li>General integer arrays ([[560]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[560]] · [[974]] · [[303]]</p>
''',

# ============================================================ LC 974 — Subarray Sums Divisible by K
974: '''
<h2>🧭 How to think about it</h2>
<p>Count subarrays whose sum is divisible by <code>k</code>. A range sum is divisible by <code>k</code> exactly when its two prefix sums have the <strong>same remainder mod k</strong>. So track the running prefix's remainder and count how many earlier prefixes shared it — every pair forms a valid subarray.</p>

<h2>🐢 Brute force first</h2>
<p>All O(n²) subarrays → too slow. Counting equal remainders → O(n) with an array of size k.</p>

<div class="insight">💡 <strong>Key insight:</strong> if <code>prefix[j] ≡ prefix[i] (mod k)</code>, then <code>sum(i..j−1)</code> is a multiple of <code>k</code>. Keep <code>count[r]</code> = number of prefixes with remainder <code>r</code>; at each step add <code>count[r]</code> before incrementing it. Use Python's <code>%</code> which already returns a non-negative remainder for positive <code>k</code>, so negatives are handled.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>count = [0]*k</code>, <code>count[0] = 1</code>, <code>running = 0</code>, <code>ans = 0</code>.</li>
<li>For each <code>x</code>: <code>running = (running + x) % k</code>; <code>ans += count[running]</code>; <code>count[running] += 1</code>.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [4,5,0,-2,-3,1], k = 5</h2>
<pre class="viz">count[0]=1 running=0 ans=0
4→r4 ans+=count[4]=0; count[4]=1
5→r4 ans+=count[4]=1(ans1); count[4]=2
0→r4 ans+=2(ans3); count[4]=3
-2→r2 ans+=0; count[2]=1
-3→r4 ans+=3(ans6); count[4]=4
1→r0 ans+=count[0]=1(ans7)
Answer: 7</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def subarraysDivByK(nums, k):
    count = [0] * k
    count[0] = 1                    # empty prefix has remainder 0
    running = ans = 0
    for x in nums:
        running = (running + x) % k # Python % is non-negative for k &gt; 0
        ans += count[running]       # earlier prefixes with the same remainder
        count[running] += 1
    return ans</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — one pass. <strong>Space O(k)</strong> for the remainder counts.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Negative numbers → Python's <code>%</code> normalizes remainders (in other languages, add <code>k</code> then mod).</li>
<li>Zeros / subarrays that are already multiples → counted via matching remainders.</li>
<li><code>k = 1</code> → every subarray qualifies.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>In languages where <code>%</code> can be negative, forgetting to normalize with <code>((r % k) + k) % k</code>.</li>
<li>Omitting the seed <code>count[0] = 1</code>.</li>
<li>Incrementing the count before reading it.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Exact sum k ([[560]]) or 0/1 arrays ([[930]]).</li>
<li>Longest such subarray → store first-occurrence index instead of a count.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[560]] · [[930]] · [[523]]</p>
''',

# ============================================================ LC 1480 — Running Sum of 1d Array
1480: '''
<h2>🧭 How to think about it</h2>
<p>Return the running (cumulative) sum: <code>out[i] = nums[0] + … + nums[i]</code>. This is the prefix-sum idea in its simplest form, and you can build it <strong>in place</strong> — each element becomes itself plus the one before it.</p>

<h2>🐢 Brute force first</h2>
<p>For each <code>i</code> re-sum <code>0..i</code> → O(n²). One pass adding the previous cumulative value → O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> <code>nums[i] += nums[i−1]</code> for <code>i ≥ 1</code>. After the sweep, each slot already holds the running total — no extra array required.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>For <code>i</code> from 1 to n−1: <code>nums[i] += nums[i−1]</code>.</li>
<li>Return <code>nums</code>.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [1,2,3,4]</h2>
<pre class="viz">i=1: 2+1=3 → [1,3,3,4]
i=2: 3+3=6 → [1,3,6,4]
i=3: 4+6=10 → [1,3,6,10]
Result: [1,3,6,10]</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def runningSum(nums):
    for i in range(1, len(nums)):
        nums[i] += nums[i - 1]     # carry the cumulative total forward
    return nums</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — single pass. <strong>Space O(1)</strong> — computed in place.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Single element → returned unchanged.</li>
<li>Negatives → cumulative sum can dip and rise.</li>
<li>Empty array → returns empty.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Starting the loop at 0 → <code>nums[-1]</code> wraps to the last element in Python.</li>
<li>Allocating a new array unnecessarily.</li>
<li>Reading the un-updated previous value if you loop backwards.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Range-sum queries build on this ([[303]]).</li>
<li>2-D running sum / integral image.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[303]] · [[724]] · [[238]]</p>
''',

# ============================================================ LC 152 — Maximum Product Subarray
152: '''
<h2>🧭 How to think about it</h2>
<p>Find the contiguous subarray with the largest product. Unlike sums, products have a twist: a <strong>negative times a negative becomes positive</strong>, so a tiny (very negative) running product can suddenly become the largest. The fix is to track <em>both</em> the maximum and the minimum product ending at each position.</p>

<h2>🐢 Brute force first</h2>
<p>All O(n²) subarray products → too slow. Tracking running max/min gives a Kadane-style O(n) one-pass solution.</p>

<div class="insight">💡 <strong>Key insight:</strong> at each element keep <code>cur_max</code> and <code>cur_min</code> of products ending here. When the new value is negative, the roles swap (multiplying flips sign), so <strong>swap</strong> <code>cur_max</code> and <code>cur_min</code> before updating. Each is <code>max/min(x, x·prev)</code> — either start fresh at <code>x</code> or extend.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Init <code>cur_max = cur_min = best = nums[0]</code>.</li>
<li>For each later <code>x</code>: if <code>x &lt; 0</code>, swap <code>cur_max</code> and <code>cur_min</code>.</li>
<li><code>cur_max = max(x, cur_max·x)</code>; <code>cur_min = min(x, cur_min·x)</code>.</li>
<li><code>best = max(best, cur_max)</code>.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [2,3,-2,4]</h2>
<pre class="viz">start max=min=best=2
x=3: max=max(3,6)=6 min=min(3,6)=3 best=6
x=-2: swap→max=3,min=6; max=max(-2,-6)=-2 min=min(-2,-12)=-12 best=6
x=4: max=max(4,-8)=4 min=min(4,-48)=-48 best=6
Answer: 6</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def maxProduct(nums):
    cur_max = cur_min = best = nums[0]
    for x in nums[1:]:
        if x &lt; 0:                       # negative flips which is largest
            cur_max, cur_min = cur_min, cur_max
        cur_max = max(x, cur_max * x)   # start fresh or extend
        cur_min = min(x, cur_min * x)
        best = max(best, cur_max)
    return best</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — one pass. <strong>Space O(1)</strong> — two running values.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Zeros → reset both running products (the <code>max/min(x, …)</code> starts fresh at <code>x = 0</code>).</li>
<li>All negatives → an even count multiplies to a positive best.</li>
<li>Single element → returned directly.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Tracking only the max — a future negative can turn a stored min into the winner.</li>
<li>Forgetting to swap before the negative update.</li>
<li>Initializing <code>best = 0</code> instead of <code>nums[0]</code> (breaks all-negative inputs).</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Maximum sum subarray (Kadane, no min needed) — [[53]].</li>
<li>Product of array except self ([[238]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[238]] · [[53]] · [[560]]</p>
''',

}
