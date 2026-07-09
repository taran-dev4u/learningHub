# Deep tutorials — Pattern P1: Two Pointers (Session 2).
# Original teaching content written for this site. Keyed by LC number;
# build.py shows these bodies instead of the light outline.

DEEP = {

# ============================================================ LC 1 — Two Sum
1: '''
<h2>🧭 How to think about it</h2>
<p>You need a <em>pair</em> with a property (sums to target). Whenever you see "find two things that combine to X", ask: <strong>as I look at each element, what would its partner have to be?</strong> For element <code>x</code>, the partner is exactly <code>target − x</code>. That turns "search for a pair" into "search for one known value" — and searching for one known value fast is what hash maps do.</p>

<h2>🐢 Brute force first</h2>
<p>Try every pair: two nested loops, check <code>nums[i] + nums[j] == target</code>.</p>
<pre><code>for i in range(len(nums)):
    for j in range(i + 1, len(nums)):
        if nums[i] + nums[j] == target:
            return [i, j]</code></pre>
<p>O(n²) time — n(n−1)/2 pairs. Fine for n=100, hopeless for n=10⁵.</p>

<div class="insight">💡 <strong>Key insight:</strong> one pass with a dict of <em>value → index</em>. For each element, ask in O(1): "has my partner already walked past?" If yes, done; if no, register myself and move on. Checking <em>before</em> inserting also means an element can never pair with itself.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Create an empty dict <code>seen</code> mapping value → index.</li>
<li>Walk the array once with <code>enumerate</code>.</li>
<li>For each <code>x</code>, compute <code>need = target − x</code>.</li>
<li>If <code>need</code> is in <code>seen</code>, return <code>[seen[need], i]</code>.</li>
<li>Otherwise store <code>seen[x] = i</code> and continue.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [2, 7, 11, 15], target = 9</h2>
<pre class="viz">i=0  x=2   need=7   seen={}          → 7 not seen → store {2:0}
i=1  x=7   need=2   seen={2:0}       → 2 IS seen at index 0 → return [0, 1] ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def twoSum(nums, target):
    seen = {}                        # value -&gt; index of where we saw it
    for i, x in enumerate(nums):
        need = target - x            # what my partner must be
        if need in seen:             # O(1) average lookup
            return [seen[need], i]   # partner's index first (it came earlier)
        seen[x] = i                  # register AFTER checking: no self-pairing
    # problem guarantees an answer exists, so we never fall through</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — one pass, O(1) dict work per element. <strong>Space O(n)</strong> — the dict may hold nearly every element before the pair appears.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Duplicates that pair with themselves (<code>[3,3]</code>, target 6): works because we check before inserting — the first 3 is found in <code>seen</code> when the second arrives.</li>
<li>Negative numbers and zero: nothing special, arithmetic just works.</li>
<li>Same element twice is forbidden: the check-then-insert order enforces this automatically.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Inserting into the dict <em>before</em> checking — a value equal to half the target pairs with itself and returns <code>[i, i]</code>.</li>
<li>Returning values instead of indices (read the ask!).</li>
<li>Sorting first to use converging pointers — works for values but destroys the original indices; you'd need to carry index pairs around.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li><em>"The array is sorted"</em> → converging two pointers, O(1) space ([[167]]).</li>
<li><em>"Count the pairs"</em> instead of returning one — keep counting, don't return early.</li>
<li><em>"Three numbers"</em> → sort + fix one + converge ([[15]]).</li>
<li><em>"Data arrives as a stream"</em> → keep the dict; answer per arrival.</li>
</ul>

<h2>🔗 Related problems</h2>
<p><a href="0007-lc167-two-sum-ii-input-array-is-sorted.html">#167 Two Sum II</a> · <a href="0003-lc15-3sum.html">#15 3Sum</a> · <a href="0005-lc18-4sum.html">#18 4Sum</a> · <a href="0004-lc16-3sum-closest.html">#16 3Sum Closest</a></p>
''',

# ============================================================ LC 11 — Container With Most Water
11: '''
<h2>🧭 How to think about it</h2>
<p>Area between lines i and j is <code>min(h[i], h[j]) × (j − i)</code>: the shorter line is the bottleneck, the distance is the width. We want the best trade-off between <em>width</em> and <em>the shorter height</em>. Start with maximum width (both ends) and ask: which end is ever worth giving up?</p>

<h2>🐢 Brute force first</h2>
<p>Check all pairs: O(n²). For each pair compute the min-height × width. Works, but n = 10⁵ kills it.</p>

<div class="insight">💡 <strong>Key insight:</strong> from the widest container, moving the <em>taller</em> pointer inward can never help — the width shrinks and the height is still capped by the same shorter line. Only moving the <strong>shorter</strong> pointer has any chance of finding a taller bottleneck. So each step discards one end <em>safely</em>, and O(n²) pairs collapse into n steps.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>left = 0</code>, <code>right = n−1</code>, <code>best = 0</code>.</li>
<li>Compute the current area; update <code>best</code>.</li>
<li>Move the pointer at the <em>shorter</em> line inward (ties: either).</li>
<li>Repeat until the pointers meet.</li>
</ol>

<h2>🎞️ Visual dry run — h = [1, 8, 6, 2, 5, 4, 8, 3, 7]</h2>
<pre class="viz">L=0(h=1) R=8(h=7)  area=min(1,7)×8= 8   best=8    h[L]&lt;h[R] → L→1
L=1(h=8) R=8(h=7)  area=min(8,7)×7=49   best=49   h[R]&lt;h[L] → R→7
L=1(h=8) R=7(h=3)  area=min(8,3)×6=18   best=49   R→6
L=1(h=8) R=6(h=8)  area=min(8,8)×5=40   best=49   tie → move either …
…pointers close in; nothing beats 49 → answer 49</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def maxArea(height):
    left, right = 0, len(height) - 1
    best = 0
    while left &lt; right:
        h = min(height[left], height[right])   # bottleneck height
        best = max(best, h * (right - left))   # width = distance
        if height[left] &lt; height[right]:
            left += 1                          # only the shorter end can improve
        else:
            right -= 1
    return best</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — every step retires one index for good. <strong>Space O(1)</strong> — two indices and a best.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Exactly two lines: one area, returned directly.</li>
<li>All equal heights: still correct — every move keeps area shrinking with width, first computation was the max.</li>
<li>Zero heights at the ends: fine, area 0 just never wins.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Moving the taller pointer, or both — breaks the "never discard a possible winner" guarantee.</li>
<li>Using the taller line for the area (water spills over the short one).</li>
<li>Confusing this with Trapping Rain Water ([[42]]) — here only TWO lines form the container; there, every bar matters.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Return the indices, not the area — track them when best updates.</li>
<li>Interviewer asks "why is skipping the taller one safe?" — be ready to prove it: the skipped pairs all have area ≤ current (same bottleneck, less width).</li>
</ul>

<h2>🔗 Related problems</h2>
<p><a href="0006-lc42-trapping-rain-water.html">#42 Trapping Rain Water</a> · <a href="0011-lc881-boats-to-save-people.html">#881 Boats to Save People</a> · <a href="0007-lc167-two-sum-ii-input-array-is-sorted.html">#167 Two Sum II</a></p>
''',

# ============================================================ LC 15 — 3Sum
15: '''
<h2>🧭 How to think about it</h2>
<p>Three numbers summing to zero = <strong>fix one number <code>a</code></strong>, then find a pair summing to <code>−a</code> — which is exactly Two Sum on the rest. On a <em>sorted</em> array that pair-search is converging two pointers in O(n). The real difficulty of 3Sum isn't the search — it's returning <em>unique</em> triplets. Sorting solves that too: duplicates sit next to each other, so you can skip them.</p>

<h2>🐢 Brute force first</h2>
<p>Three nested loops, O(n³), plus a set of sorted triplets to dedupe. n = 3000 → 4.5 billion checks. No.</p>

<div class="insight">💡 <strong>Key insight:</strong> sort once. For each anchor index <code>i</code>, converge <code>lo/hi</code> on the suffix: sum too small → <code>lo += 1</code>, too big → <code>hi −= 1</code>. After every hit AND at the anchor level, <strong>skip equal neighbors</strong> — that's what makes results unique without a set.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Sort the array (O(n log n)).</li>
<li>For each <code>i</code> from 0 to n−3:
  <ul><li>if <code>nums[i] &gt; 0</code>, stop — a positive anchor can't reach zero with larger numbers;</li>
  <li>if <code>nums[i] == nums[i−1]</code>, skip — same anchor was already handled.</li></ul></li>
<li>Converge <code>lo = i+1</code>, <code>hi = n−1</code> looking for <code>−nums[i]</code>.</li>
<li>On a hit: record, then advance <code>lo</code> past duplicates and retreat <code>hi</code> past duplicates.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [−1, 0, 1, 2, −1, −4] → sorted [−4, −1, −1, 0, 1, 2]</h2>
<pre class="viz">i=0 a=−4  need 4:  lo=1(−1) hi=5(2)  sum=1&lt;4 →lo  … no pair (max is 3)
i=1 a=−1  need 1:  lo=2(−1) hi=5(2)  sum=1 ✓ → [−1,−1,2]; skip dups; lo=3(0) hi=4(1) sum=1 ✓ → [−1,0,1]
i=2 a=−1  = nums[1] → SKIP (anchor duplicate)
i=3 a=0   need 0:  lo=4(1) hi=5(2)  sum=3&gt;0 →hi; pointers meet. Done.
Result: [[−1,−1,2], [−1,0,1]]</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def threeSum(nums):
    nums.sort()
    res = []
    n = len(nums)
    for i in range(n - 2):
        if nums[i] &gt; 0:                    # anchors beyond 0 can't work
            break
        if i &gt; 0 and nums[i] == nums[i-1]: # duplicate anchor → same triplets
            continue
        lo, hi = i + 1, n - 1
        while lo &lt; hi:
            s = nums[i] + nums[lo] + nums[hi]
            if s &lt; 0:
                lo += 1                    # need a bigger sum
            elif s &gt; 0:
                hi -= 1                    # need a smaller sum
            else:
                res.append([nums[i], nums[lo], nums[hi]])
                while lo &lt; hi and nums[lo] == nums[lo+1]:  # skip dup pairs
                    lo += 1
                while lo &lt; hi and nums[hi] == nums[hi-1]:
                    hi -= 1
                lo += 1; hi -= 1           # move BOTH past the used values
    return res</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n²)</strong> — n anchors × O(n) converge each (sort's n log n is dominated). <strong>Space O(1)</strong> extra beyond the output (sorting in place).</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Fewer than 3 elements → empty result.</li>
<li>All zeros <code>[0,0,0,0]</code> → exactly one triplet [0,0,0]; the dup-skips guarantee it appears once.</li>
<li>All positive or all negative → the <code>nums[i] &gt; 0</code> break / natural convergence returns [].</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Skipping duplicates at the wrong moment — anchor skip uses <code>nums[i] == nums[i−1]</code> (compare <em>backwards</em>); comparing forward skips valid first-uses.</li>
<li>After a hit, moving only one pointer — you'll record the same pair again.</li>
<li>Using a set of triplets instead of skip logic — accepted, but the interviewer wants the O(1)-space dedupe.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Target ≠ 0: replace 0 with target everywhere (drop the <code>&gt; 0</code> break unless values are known non-negative).</li>
<li>Closest instead of exact → track the best gap ([[16]]).</li>
<li>Four numbers → one more anchor loop ([[18]]); k numbers → recursion peeling one anchor per level.</li>
<li>Count triplets with sum &lt; target → ([[259]]) — the counting trick <code>hi − lo</code>.</li>
</ul>

<h2>🔗 Related problems</h2>
<p><a href="0001-lc1-two-sum.html">#1 Two Sum</a> · <a href="0004-lc16-3sum-closest.html">#16 3Sum Closest</a> · <a href="0005-lc18-4sum.html">#18 4Sum</a> · <a href="0008-lc259-3sum-smaller.html">#259 3Sum Smaller</a></p>
''',

# ============================================================ LC 16 — 3Sum Closest
16: '''
<h2>🧭 How to think about it</h2>
<p>Same skeleton as 3Sum — sort, anchor, converge — but there's no exact hit to find. Instead every candidate sum is a <em>contestant</em>: keep whichever lands nearest the target. The pointers still move by the same logic (sum too small → need bigger → <code>lo += 1</code>), because sorted order still tells you which direction improves.</p>

<h2>🐢 Brute force first</h2>
<p>All triplets O(n³), track the closest. The sorted converge cuts it to O(n²) exactly like 3Sum.</p>

<div class="insight">💡 <strong>Key insight:</strong> convergence doesn't need equality to work — it needs <em>monotonicity</em>. Sum &lt; target means every pair with this <code>lo</code> and a smaller <code>hi</code> is even further below; so <code>lo += 1</code> is the only sensible move. Track <code>best</code> on every step and you can't miss the optimum.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Sort. Initialize <code>best</code> to the sum of the first three values.</li>
<li>Anchor <code>i</code>; converge <code>lo/hi</code> on the suffix.</li>
<li>Each step: if <code>|sum − target| &lt; |best − target|</code>, update best.</li>
<li>Exact hit? Return immediately — can't beat distance 0.</li>
<li>Move <code>lo</code> or <code>hi</code> by comparing sum to target.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [−1, 2, 1, −4], target = 1 → sorted [−4, −1, 1, 2]</h2>
<pre class="viz">i=0 a=−4: lo=1(−1) hi=3(2) sum=−3 |−3−1|=4 → best=−3;  −3&lt;1 → lo
          lo=2(1)  hi=3(2) sum=−1 |−1−1|=2 → best=−1;  −1&lt;1 → lo → meet
i=1 a=−1: lo=2(1)  hi=3(2) sum=2  |2−1|=1  → best=2;    2&gt;1 → hi → meet
Answer: 2</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def threeSumClosest(nums, target):
    nums.sort()
    n = len(nums)
    best = nums[0] + nums[1] + nums[2]
    for i in range(n - 2):
        if i &gt; 0 and nums[i] == nums[i-1]:
            continue                          # duplicate anchors add nothing
        lo, hi = i + 1, n - 1
        while lo &lt; hi:
            s = nums[i] + nums[lo] + nums[hi]
            if abs(s - target) &lt; abs(best - target):
                best = s                      # closer contestant wins
            if s == target:
                return s                      # distance 0: unbeatable
            elif s &lt; target:
                lo += 1
            else:
                hi -= 1
    return best</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n²)</strong>, <strong>space O(1)</strong> — same shape as 3Sum, one extra comparison per step.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Exactly three elements — their sum is the answer (initialization handles it).</li>
<li>Target far outside the value range — best converges to the min or max triple sum.</li>
<li>Several sums equally close — any is accepted; the strict <code>&lt;</code> keeps the first found.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Initializing <code>best = 0</code> or <code>inf</code> — 0 is a <em>sum</em>, not a distance; compare distances, seed with a real triplet sum.</li>
<li>Comparing <code>abs(s − target)</code> against <code>best</code> instead of <code>abs(best − target)</code>.</li>
<li>Forgetting the early return on exact match (correct but slower, and interviewers notice).</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Return the triplet itself — store indices/values when best updates.</li>
<li>Closest <em>pair</em> sum (2Sum closest) — same converge without the anchor loop.</li>
</ul>

<h2>🔗 Related problems</h2>
<p><a href="0003-lc15-3sum.html">#15 3Sum</a> · <a href="0008-lc259-3sum-smaller.html">#259 3Sum Smaller</a> · <a href="0001-lc1-two-sum.html">#1 Two Sum</a></p>
''',

# ============================================================ LC 18 — 4Sum
18: '''
<h2>🧭 How to think about it</h2>
<p>The kSum ladder: 2Sum on sorted input = converge in O(n); 3Sum = anchor × 2Sum; 4Sum = anchor × anchor × 2Sum. Every extra number is one more outer loop with the <em>same</em> duplicate-skipping discipline. If you truly own 3Sum, 4Sum is bookkeeping.</p>

<h2>🐢 Brute force first</h2>
<p>Four loops = O(n⁴). Even a hash-assisted O(n³)-pairs approach struggles with dedupe. The sorted double-anchor + converge is the clean O(n³).</p>

<div class="insight">💡 <strong>Key insight:</strong> generalize, don't specialize: <code>kSum(nums, target, k)</code> recursively fixes one anchor and calls <code>kSum(rest, target − anchor, k−1)</code> until k == 2, which converges. One function solves 2/3/4/5-Sum — this is the answer interviewers hope to see for "and now 5Sum?"</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Sort.</li>
<li>Loop anchor <code>a</code> (skip duplicates); loop anchor <code>b &gt; a</code> (skip duplicates).</li>
<li>Converge <code>lo/hi</code> on the remainder toward <code>target − nums[a] − nums[b]</code>.</li>
<li>On hits: record and skip duplicates on both pointers.</li>
<li>Optional pruning per anchor level: smallest possible sum &gt; target → break; largest possible &lt; target → continue.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [1, 0, −1, 0, −2, 2], target = 0 → sorted [−2, −1, 0, 0, 1, 2]</h2>
<pre class="viz">a=−2: b=−1: need 3:  lo(0)+hi(2)=2&lt;3 →lo; 0+2=2&lt;3 →lo; 1+2=3 ✓ [−2,−1,1,2]
      b=0 : need 2:  0+2=2 ✓ [−2,0,0,2]; skip dups; 1+? meet
a=−1: b=0 : need 1:  0+2=2&gt;1 →hi; 0+1=1 ✓ [−1,0,0,1]
a=0 (dup of previous 0 as first anchor? no—first 0 anchor) … no further hits
Result: [[−2,−1,1,2], [−2,0,0,2], [−1,0,0,1]]</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def fourSum(nums, target):
    nums.sort()
    n, res = len(nums), []
    for a in range(n - 3):
        if a &gt; 0 and nums[a] == nums[a-1]:
            continue                              # dup anchor 1
        for b in range(a + 1, n - 2):
            if b &gt; a + 1 and nums[b] == nums[b-1]:
                continue                          # dup anchor 2
            lo, hi = b + 1, n - 1
            need = target - nums[a] - nums[b]
            while lo &lt; hi:
                s = nums[lo] + nums[hi]
                if s &lt; need:
                    lo += 1
                elif s &gt; need:
                    hi -= 1
                else:
                    res.append([nums[a], nums[b], nums[lo], nums[hi]])
                    while lo &lt; hi and nums[lo] == nums[lo+1]: lo += 1
                    while lo &lt; hi and nums[hi] == nums[hi-1]: hi -= 1
                    lo += 1; hi -= 1
    return res</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n³)</strong> — n² anchor pairs × O(n) converge. <strong>Space O(1)</strong> beyond output.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li><strong>Overflow warning for other languages:</strong> sums of four 10⁹-scale values overflow 32-bit ints; Python is safe, but say it aloud.</li>
<li>Massive duplicate runs (<code>[2,2,2,2,2]</code>, target 8) → exactly one quadruplet.</li>
<li>n &lt; 4 → empty.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Second anchor's dup-skip condition: must be <code>b &gt; a + 1</code>, not <code>b &gt; 0</code> — otherwise you skip legitimate quadruplets where <code>nums[b] == nums[a]</code>.</li>
<li>Forgetting that four numbers can legally repeat values across positions — dedupe per <em>position level</em>, never globally.</li>
<li>Rebuilding 3Sum logic inline with subtle differences instead of reusing the discipline.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>kSum generic recursion (the follow-up interviewers love).</li>
<li>4Sum-II (count tuples from four separate arrays) — different tool: meet-in-the-middle hash of pair sums, O(n²).</li>
</ul>

<h2>🔗 Related problems</h2>
<p><a href="0003-lc15-3sum.html">#15 3Sum</a> · <a href="0001-lc1-two-sum.html">#1 Two Sum</a> · <a href="0004-lc16-3sum-closest.html">#16 3Sum Closest</a></p>
''',

# ============================================================ LC 42 — Trapping Rain Water
42: '''
<h2>🧭 How to think about it</h2>
<p>Stop thinking about "pools". Think about <strong>one column at a time</strong>: how much water stands on top of bar i? Water is held by the tallest wall to the left and the tallest wall to the right; the level is the <em>lower</em> of those two, and the water above bar i is <code>min(maxL, maxR) − h[i]</code> (never negative). Sum that over all bars and the problem is solved — the rest is how cheaply you can know <code>maxL</code> and <code>maxR</code>.</p>

<h2>🐢 Brute force first</h2>
<p>For each bar, scan left for the max and right for the max: O(n²). Better: precompute prefix-max and suffix-max arrays → O(n) time, O(n) space. The two-pointer version removes even that space.</p>

<div class="insight">💡 <strong>Key insight:</strong> walk pointers from both ends carrying <code>maxL</code> and <code>maxR</code>. If <code>maxL &lt; maxR</code>, then for the left bar the binding wall is <em>certainly</em> <code>maxL</code> — some unseen wall in the middle can only make the right side taller, never lower than <code>maxR</code>. So the left column's water is decided <em>now</em>, without ever seeing the middle. Process it, step inward.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>l = 0, r = n−1, maxL = maxR = 0, water = 0</code>.</li>
<li>If <code>h[l] &lt; h[r]</code>: the left side is the shorter frontier —
  <ul><li>if <code>h[l] ≥ maxL</code>, it's a new wall: update <code>maxL</code>;</li>
  <li>else it holds <code>maxL − h[l]</code> water. Then <code>l += 1</code>.</li></ul></li>
<li>Otherwise do the mirror step on the right.</li>
<li>Stop when pointers cross.</li>
</ol>

<h2>🎞️ Visual dry run — h = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]</h2>
<pre class="viz">              █
      █░░░░░░ █ █░░█
  █░░ █ █░░ █ █ █ █ █ █        ░ = trapped water
  0 1 0 2 1 0 1 3 2 1 2 1
l walks while its frontier is shorter: bar2 gets 1−0=1, bar4 gets 2−1=1,
bar5 gets 2−0=2, bar6 gets 2−1=1 … right side: bar9 gets 2−1=1 … total = 6</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def trap(height):
    l, r = 0, len(height) - 1
    maxL = maxR = water = 0
    while l &lt; r:
        if height[l] &lt; height[r]:
            # left frontier is shorter → its ceiling is maxL, final
            if height[l] &gt;= maxL:
                maxL = height[l]          # new left wall, holds nothing
            else:
                water += maxL - height[l] # stands under the left wall
            l += 1
        else:
            if height[r] &gt;= maxR:
                maxR = height[r]
            else:
                water += maxR - height[r]
            r -= 1
    return water</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — each bar processed once from one side. <strong>Space O(1)</strong> — two maxima, two pointers. (The prefix/suffix-array version is O(n)/O(n) and a fine first answer.)</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Fewer than 3 bars → 0 (no basin possible).</li>
<li>Monotonic ascending or descending → 0 (every bar is its own max on one side).</li>
<li>Plateaus of equal heights — the ≥ in the wall update handles them without double-counting.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Comparing <code>maxL</code> vs <code>maxR</code> to decide which side to step (compare the <em>current bars</em> <code>h[l]</code> vs <code>h[r]</code>; the maxima update after).</li>
<li>Trying to detect "pools" as shapes — per-column accounting is the whole trick.</li>
<li>Confusing with Container With Most Water ([[11]]): there you pick 2 lines and ignore the middle; here every middle bar displaces water.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>2-D version (Trapping Rain Water II, LC 407) — becomes a heap/BFS from the border, not two pointers.</li>
<li>"Explain why the shorter-side decision is safe" — rehearse the argument; it's the interview.</li>
<li>Prefix/suffix arrays version — know both; offer the O(1)-space upgrade.</li>
</ul>

<h2>🔗 Related problems</h2>
<p><a href="0002-lc11-container-with-most-water.html">#11 Container With Most Water</a> · <a href="0012-lc977-squares-of-a-sorted-array.html">#977 Squares of a Sorted Array</a></p>
''',

# ============================================================ LC 167 — Two Sum II (sorted)
167: '''
<h2>🧭 How to think about it</h2>
<p>This is Two Sum, but the array is <strong>already sorted</strong> — and sorted order is a gift. When a list is sorted, the sum of the two ends tells you which way to move: too small means you need more, so raise the low end; too big means you need less, so lower the high end. No hash map needed, no extra memory.</p>

<h2>🐢 Brute force first</h2>
<p>Every pair, O(n²). Or reuse the hash-map Two Sum for O(n) time and O(n) space. But sorted input lets us do O(n) time with <em>O(1)</em> space — strictly better.</p>

<div class="insight">💡 <strong>Key insight:</strong> put one pointer at each end. Their sum is the largest-plus-smallest available. If it's below target, the only way to grow is <code>left += 1</code>; if above, the only way to shrink is <code>right -= 1</code>. Each move safely discards a value that can never be part of the answer.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>left = 0</code>, <code>right = n − 1</code>.</li>
<li>Compute <code>s = nums[left] + nums[right]</code>.</li>
<li>If <code>s == target</code>, return the 1-indexed pair <code>[left+1, right+1]</code>.</li>
<li>If <code>s &lt; target</code>, <code>left += 1</code>; if <code>s &gt; target</code>, <code>right -= 1</code>.</li>
</ol>

<h2>🎞️ Visual dry run — numbers = [2, 7, 11, 15], target = 9</h2>
<pre class="viz">L=0(2) R=3(15)  sum=17 &gt; 9 → R−−
L=0(2) R=2(11)  sum=13 &gt; 9 → R−−
L=0(2) R=1(7)   sum=9  = 9 → return [1, 2] ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def twoSum(numbers, target):
    left, right = 0, len(numbers) - 1
    while left &lt; right:
        s = numbers[left] + numbers[right]
        if s == target:
            return [left + 1, right + 1]   # problem uses 1-based indices
        elif s &lt; target:
            left += 1                       # need a bigger sum
        else:
            right -= 1                      # need a smaller sum
    return []                               # guaranteed not reached</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — each step retires one index; pointers meet after ≤ n moves. <strong>Space O(1)</strong> — two indices, nothing else.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Exactly two elements — the first comparison settles it.</li>
<li>Negatives and zeros — arithmetic is unaffected; sorted order is all that matters.</li>
<li>The 1-based indexing — a classic off-by-one; add 1 to both.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Returning 0-based indices — this problem is 1-based.</li>
<li>Using <code>left &lt;= right</code> — an element can't pair with itself here; keep <code>&lt;</code>.</li>
<li>Reaching for a hash map — correct but wastes the O(1)-space opportunity the sorting hands you.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Unsorted input → hash-map Two Sum ([[1]]).</li>
<li>Count all pairs summing to target → keep moving both ends after each hit, skipping duplicates.</li>
<li>Three numbers → sort + anchor + this converge ([[15]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[1]] · [[15]] · [[977]] · [[611]]</p>
''',

# ============================================================ LC 259 — 3Sum Smaller
259: '''
<h2>🧭 How to think about it</h2>
<p>We don't want exact triples — we want to <em>count</em> how many triples sum to <strong>less than</strong> target. The magic is a counting shortcut: on a sorted array, if <code>nums[i] + nums[lo] + nums[hi] &lt; target</code>, then keeping <code>lo</code> fixed and using <em>any</em> <code>hi</code> between <code>lo+1</code> and the current <code>hi</code> also works — because those middle values are all smaller. That's <code>hi − lo</code> triples counted in one shot.</p>

<h2>🐢 Brute force first</h2>
<p>Three nested loops testing each triple, O(n³). For n up to a few thousand that is far too slow. Sorting plus the converge trick brings it to O(n²).</p>

<div class="insight">💡 <strong>Key insight:</strong> sort, then for each anchor converge <code>lo/hi</code>. When the sum is below target, every element strictly between <code>lo</code> and <code>hi</code> also forms a valid triple with <code>lo</code> — add <code>hi − lo</code> at once and bump <code>lo</code>. When the sum is ≥ target, drop <code>hi</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Sort the array.</li>
<li>For each anchor <code>i</code>, set <code>lo = i+1</code>, <code>hi = n−1</code>.</li>
<li>If <code>nums[i] + nums[lo] + nums[hi] &lt; target</code>: add <code>hi − lo</code> to the count, then <code>lo += 1</code>.</li>
<li>Otherwise <code>hi -= 1</code>.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [−2, 0, 1, 3], target = 2 → sorted [−2, 0, 1, 3]</h2>
<pre class="viz">i=0 a=−2: lo=1(0) hi=3(3) sum=1 &lt; 2 → count += hi−lo = 2 (pairs (0,1),(0,3)); lo→2
          lo=2(1) hi=3(3) sum=2 not &lt; 2 → hi→2 ; lo==hi stop
i=1 a=0 : lo=2(1) hi=3(3) sum=4 ≥ 2 → hi→2 ; stop
i=2 a=1 : lo=3    hi=3     stop
Total count = 2</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def threeSumSmaller(nums, target):
    nums.sort()
    n, count = len(nums), 0
    for i in range(n - 2):
        lo, hi = i + 1, n - 1
        while lo &lt; hi:
            if nums[i] + nums[lo] + nums[hi] &lt; target:
                count += hi - lo        # all hi's between lo+1..hi also qualify
                lo += 1
            else:
                hi -= 1                 # sum too big; shrink from the top
    return count</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n²)</strong> — n anchors × O(n) converge (sorting's n log n is dominated). <strong>Space O(1)</strong> beyond the sort.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Fewer than 3 elements → 0.</li>
<li>All triples already below target → the <code>hi − lo</code> shortcut still counts them correctly.</li>
<li>No valid triple → count stays 0.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Counting 1 instead of <code>hi − lo</code> — you'd re-walk each pair and lose the O(n²) win.</li>
<li>Using <code>≤</code> when the problem says strictly <em>less than</em> (or vice-versa) — read the comparison carefully.</li>
<li>Forgetting to move <code>lo</code> after adding the batch — infinite loop.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Count triples with sum ≤ target → change <code>&lt;</code> to <code>&lt;=</code>.</li>
<li>Exact-sum triples → [[15]]; closest → [[16]].</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[15]] · [[16]] · [[611]] · [[167]]</p>
''',

# ============================================================ LC 349 — Intersection of Two Arrays
349: '''
<h2>🧭 How to think about it</h2>
<p>Return the <em>unique</em> values that appear in both arrays. The one-line answer is <code>set(a) &amp; set(b)</code>. But the two-pointer version is worth knowing: sort both arrays, then walk a pointer through each — when they point at equal values, that's a shared element; otherwise advance whichever points at the smaller value, because it can never catch up.</p>

<h2>🐢 Brute force first</h2>
<p>For each element of <code>a</code>, scan all of <code>b</code>: O(n·m), plus a set to dedupe. Sets alone give O(n+m). The two-pointer method gives O(n log n + m log m) and shines when the inputs are already sorted or memory is tight.</p>

<div class="insight">💡 <strong>Key insight:</strong> on two sorted arrays, matching values line up. Equal → record and step both past duplicates. Unequal → the smaller value has no partner ahead of it, so step it forward.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Sort both arrays.</li>
<li><code>i = j = 0</code>. While both in range: compare <code>a[i]</code>, <code>b[j]</code>.</li>
<li>Equal → append (if not just appended), advance both.</li>
<li><code>a[i] &lt; b[j]</code> → <code>i += 1</code>; else <code>j += 1</code>.</li>
</ol>

<h2>🎞️ Visual dry run — a = [4,9,5], b = [9,4,9,8,4] → sorted a=[4,5,9] b=[4,4,8,9,9]</h2>
<pre class="viz">i=0(4) j=0(4)  equal → out=[4]; i→1, j→1
i=1(5) j=1(4)  5&gt;4 → j→2
i=1(5) j=2(8)  5&lt;8 → i→2
i=2(9) j=2(8)  9&gt;8 → j→3
i=2(9) j=3(9)  equal → out=[4,9]; i→3 (end)
Result: [4, 9]</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def intersection(nums1, nums2):
    nums1.sort(); nums2.sort()
    i = j = 0
    res = []
    while i &lt; len(nums1) and j &lt; len(nums2):
        if nums1[i] == nums2[j]:
            if not res or res[-1] != nums1[i]:  # keep results unique
                res.append(nums1[i])
            i += 1; j += 1
        elif nums1[i] &lt; nums2[j]:
            i += 1                              # smaller value can't match ahead
        else:
            j += 1
    return res

# One-liner alternative:  return list(set(nums1) &amp; set(nums2))</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n log n + m log m)</strong> — dominated by the two sorts; the merge walk is O(n+m). <strong>Space O(1)</strong> beyond the output (the set version is O(n+m) space, O(n+m) time).</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Either array empty → empty result.</li>
<li>Heavy duplicates → the "don't repeat the last appended" guard keeps the output unique.</li>
<li>No overlap → one pointer runs off the end, loop stops, result empty.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Forgetting to dedupe — the result must contain each shared value once.</li>
<li>Advancing only one pointer on a match — you'd re-report duplicates.</li>
<li>Not sorting before the two-pointer walk — the whole method depends on order.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Keep multiplicity (Intersection II, LC 350) → append on every match, don't dedupe.</li>
<li>One array is huge and on disk → sort + stream the two-pointer merge.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[167]] · [[977]] · [[15]]</p>
''',

# ============================================================ LC 611 — Valid Triangle Number
611: '''
<h2>🧭 How to think about it</h2>
<p>Three lengths form a triangle iff the two shortest add up to more than the longest (the other two triangle inequalities are automatic once that holds). So <strong>sort</strong>, fix the <em>largest</em> side, and count how many pairs of smaller sides beat it. Sorting turns "check three inequalities" into "check one".</p>

<h2>🐢 Brute force first</h2>
<p>Test every triple against the triangle inequality: O(n³). Sorting plus a converge collapses it to O(n²).</p>

<div class="insight">💡 <strong>Key insight:</strong> after sorting, fix the largest side at index <code>k</code> and converge <code>lo/hi</code> below it. If <code>nums[lo] + nums[hi] &gt; nums[k]</code>, then every element from <code>lo</code> up to <code>hi−1</code> also works with <code>hi</code> — add <code>hi − lo</code> at once and drop <code>hi</code>. Otherwise <code>lo += 1</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Sort ascending.</li>
<li>For <code>k</code> from <code>n−1</code> down to 2 (the largest side): set <code>lo = 0</code>, <code>hi = k−1</code>.</li>
<li>If <code>nums[lo] + nums[hi] &gt; nums[k]</code>: count += <code>hi − lo</code>, then <code>hi -= 1</code>.</li>
<li>Else <code>lo += 1</code>.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [2, 2, 3, 4] (sorted)</h2>
<pre class="viz">k=3 (side 4): lo=0(2) hi=2(3)  2+3=5 &gt; 4 → count += hi−lo = 2; hi→1
              lo=0(2) hi=1(2)  2+2=4 not &gt; 4 → lo→1 ; lo==hi stop
k=2 (side 3): lo=0(2) hi=1(2)  2+2=4 &gt; 3 → count += 1 (total 3); hi→0 stop
Total = 3 triangles</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def triangleNumber(nums):
    nums.sort()
    n, count = len(nums), 0
    for k in range(n - 1, 1, -1):        # k = index of the longest side
        lo, hi = 0, k - 1
        while lo &lt; hi:
            if nums[lo] + nums[hi] &gt; nums[k]:
                count += hi - lo         # lo..hi-1 all pair with hi
                hi -= 1
            else:
                lo += 1                  # shortest side too small; grow it
    return count</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n²)</strong> — n choices of longest side × O(n) converge. <strong>Space O(1)</strong> beyond the sort.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Fewer than 3 elements → 0.</li>
<li>Zeros — a side of length 0 never satisfies <code>a + b &gt; c</code> when it's one of the shorter sides, and the strict <code>&gt;</code> handles it.</li>
<li>Many equal lengths → counted correctly by the batch add.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Fixing the <em>smallest</em> side instead of the largest — you'd need all three inequalities again.</li>
<li>Using <code>≥</code> — degenerate (flat) triangles don't count; the inequality is strict.</li>
<li>Adding 1 instead of <code>hi − lo</code>.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Count degenerate triangles too → switch to <code>≥</code>.</li>
<li>Return the triangles, not the count → record the ranges instead of summing.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[259]] · [[15]] · [[167]]</p>
''',

# ============================================================ LC 881 — Boats to Save People
881: '''
<h2>🧭 How to think about it</h2>
<p>Every boat holds at most two people and a weight limit. To use the fewest boats, pair the <strong>heaviest remaining person with the lightest</strong>: if they fit together, great, one boat for two; if not, the heavy one rides alone. Sorting makes "heaviest" and "lightest" the two ends of the array.</p>

<h2>🐢 Brute force first</h2>
<p>Trying all pairings is exponential. The greedy "heaviest + lightest" is provably optimal and runs in O(n log n) (just the sort).</p>

<div class="insight">💡 <strong>Key insight:</strong> after sorting, point <code>lo</code> at the lightest and <code>hi</code> at the heaviest. The heaviest person must leave on <em>some</em> boat now; give them a seat and check if the lightest can squeeze in too. Either way <code>hi</code> boards, so <code>hi</code> always moves left; <code>lo</code> moves only when they share.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Sort ascending. <code>lo = 0</code>, <code>hi = n−1</code>, <code>boats = 0</code>.</li>
<li>While <code>lo &lt;= hi</code>: this boat carries person <code>hi</code>.</li>
<li>If <code>people[lo] + people[hi] &lt;= limit</code>, the lightest joins → <code>lo += 1</code>.</li>
<li>Always <code>hi -= 1</code> and <code>boats += 1</code>.</li>
</ol>

<h2>🎞️ Visual dry run — people = [3,2,2,1], limit = 3 → sorted [1,2,2,3]</h2>
<pre class="viz">lo=0(1) hi=3(3)  1+3=4 &gt; 3 → 3 rides alone; hi→2, boats=1
lo=0(1) hi=2(2)  1+2=3 ≤ 3 → pair; lo→1, hi→1, boats=2
lo=1(2) hi=1(2)  same person; 2 rides alone; hi→0, boats=3
Answer: 3 boats</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def numRescueBoats(people, limit):
    people.sort()
    lo, hi = 0, len(people) - 1
    boats = 0
    while lo &lt;= hi:
        if people[lo] + people[hi] &lt;= limit:
            lo += 1                 # lightest fits alongside the heaviest
        hi -= 1                     # heaviest always boards this boat
        boats += 1
    return boats</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n log n)</strong> — the sort dominates; the walk is O(n). <strong>Space O(1)</strong> (in-place sort).</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li><code>lo == hi</code> — one person left, boards alone; the <code>&lt;=</code> loop condition includes this.</li>
<li>Everyone at the limit → each rides alone, <code>n</code> boats.</li>
<li>All very light → every boat carries two, <code>⌈n/2⌉</code> boats.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Using <code>lo &lt; hi</code> — the last solo passenger gets dropped from the count.</li>
<li>Trying to pair the two heaviest — a boat holds at most two people <em>and</em> the limit; pairing heavy+light is what's optimal.</li>
<li>Forgetting the problem caps each boat at two people, not just a weight.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Boats hold three people → greedy breaks; needs different reasoning.</li>
<li>Minimize total weight per boat rather than count → a different objective.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[11]] · [[167]] · [[977]]</p>
''',

# ============================================================ LC 977 — Squares of a Sorted Array
977: '''
<h2>🧭 How to think about it</h2>
<p>Squaring a sorted array scrambles the order because negatives flip: <code>[−4,−1,0,3]</code> squared is <code>[16,1,0,9]</code>. But notice — the <em>largest</em> square always sits at one of the two ends (the most negative or the most positive value). So compare the ends, take the bigger square, and fill the answer <strong>from the back</strong>.</p>

<h2>🐢 Brute force first</h2>
<p>Square everything then sort: O(n log n). Correct, but we can do O(n) because the input is already sorted — we just need to merge two runs.</p>

<div class="insight">💡 <strong>Key insight:</strong> the array is two sorted runs in disguise — negatives (descending in magnitude) and non-negatives (ascending). The biggest magnitude is at one end or the other. Two pointers at the ends pick the larger square each step and place it at the current tail of the result.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>lo = 0</code>, <code>hi = n−1</code>, result array of size n, write index <code>pos = n−1</code>.</li>
<li>Compare <code>|nums[lo]|</code> and <code>|nums[hi]|</code> via their squares.</li>
<li>Place the larger square at <code>result[pos]</code>, move that pointer inward, <code>pos -= 1</code>.</li>
<li>Repeat until the pointers cross.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [−4, −1, 0, 3, 10]</h2>
<pre class="viz">lo=0(−4→16) hi=4(10→100)  100&gt;16 → res[4]=100; hi→3, pos=3
lo=0(−4→16) hi=3(3→9)     16&gt;9  → res[3]=16 ; lo→1, pos=2
lo=1(−1→1)  hi=3(3→9)     9&gt;1   → res[2]=9  ; hi→2, pos=1
lo=1(−1→1)  hi=2(0→0)     1&gt;0   → res[1]=1  ; lo→2, pos=0
lo=2(0)     hi=2(0)       res[0]=0
Result: [0, 1, 9, 16, 100]</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def sortedSquares(nums):
    n = len(nums)
    res = [0] * n
    lo, hi = 0, n - 1
    for pos in range(n - 1, -1, -1):    # fill from the back
        if nums[lo] * nums[lo] &gt; nums[hi] * nums[hi]:
            res[pos] = nums[lo] * nums[lo]
            lo += 1
        else:
            res[pos] = nums[hi] * nums[hi]
            hi -= 1
    return res</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — one pass, each index placed once. <strong>Space O(n)</strong> for the output (unavoidable; the input can't be safely overwritten while reading both ends).</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>All non-negative → the <code>hi</code> pointer feeds everything; already-sorted squares.</li>
<li>All negative → the <code>lo</code> pointer feeds everything.</li>
<li>Contains 0 → its square 0 lands first (at the front).</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Filling the result from the front — you'd need the <em>smallest</em> square, which is in the middle and hard to find.</li>
<li>Comparing raw values instead of magnitudes/squares — <code>−4 &lt; 3</code> but <code>16 &gt; 9</code>.</li>
<li>Off-by-one on <code>pos</code> or the crossing condition.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Cubes of a sorted array → cubes preserve sign/order, so just map — no merge needed.</li>
<li>Merge two sorted arrays generally → same back-to-front idea ([[88]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[167]] · [[349]] · [[11]]</p>
''',

# ============================================================ LC 151 — Reverse Words in a String
151: '''
<h2>🧭 How to think about it</h2>
<p>Reverse the <em>order of words</em>, not the letters, and collapse any messy spacing to single spaces. The clean Python answer is split-reverse-join. But interviewers often want the in-place, O(1)-extra-space version done on a character array: reverse the whole thing, then reverse each word back.</p>

<h2>🐢 Brute force first</h2>
<p>Split on whitespace, drop empties, reverse the list, join with single spaces. That's O(n) time and O(n) space — perfectly good and the expected first answer.</p>

<div class="insight">💡 <strong>Key insight:</strong> reversing the entire string flips both the word order <em>and</em> each word's letters. A second pass that reverses each individual word fixes the letters, leaving the words in reversed order. Two reversals = the answer, no extra array.</div>

<h2>🪜 The approach, step by step (in-place variant)</h2>
<ol>
<li>Trim and normalize spaces (or handle them while scanning).</li>
<li>Reverse the whole character array.</li>
<li>Walk with two pointers to find each word's bounds and reverse it back.</li>
</ol>

<h2>🎞️ Visual dry run — s = "the sky is blue"</h2>
<pre class="viz">split → ["the","sky","is","blue"]
reverse list → ["blue","is","sky","the"]
join → "blue is sky the"

in-place idea: "the sky is blue"
reverse all → "eulb si yks eht"
reverse each word → "blue is sky the" ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def reverseWords(s):
    # Pythonic: split() drops all runs of whitespace automatically
    return " ".join(reversed(s.split()))

# In-place style on a list of chars (interview version):
def reverseWordsInPlace(chars):
    def rev(a, i, j):
        while i &lt; j:
            a[i], a[j] = a[j], a[i]
            i += 1; j -= 1
    rev(chars, 0, len(chars) - 1)          # reverse everything
    start = 0
    for i in range(len(chars) + 1):
        if i == len(chars) or chars[i] == ' ':
            rev(chars, start, i - 1)        # reverse this word back
            start = i + 1
    return chars</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — a constant number of linear passes. <strong>Space O(1)</strong> for the in-place char-array version (Python's <code>split</code>/<code>join</code> version is O(n) space because strings are immutable).</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Leading/trailing spaces and multiple spaces between words → <code>split()</code> normalizes them; the in-place version must skip empty gaps.</li>
<li>Single word → returned unchanged.</li>
<li>All spaces → empty string.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Reversing the characters of each word instead of the word order (the double-reverse trick prevents this).</li>
<li>Leaving double spaces in the output.</li>
<li>Forgetting to reverse the final word when the string doesn't end in a space (loop to <code>len+1</code> to flush it).</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Reverse letters within each word but keep word order (LC 557) → just the second pass.</li>
<li>Do it truly in place in a language with mutable strings → the two-reversal method is the answer.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[344]] · [[345]] · [[541]]</p>
''',

# ============================================================ LC 344 — Reverse String
344: '''
<h2>🧭 How to think about it</h2>
<p>Reverse a character array <em>in place</em>. The whole trick is one image: a pointer at each end swap their characters, then step toward the middle. When they meet, every pair has been swapped exactly once.</p>

<h2>🐢 Brute force first</h2>
<p>Building a new reversed array is O(n) space; the problem explicitly forbids that. Two converging pointers do it with O(1) extra space.</p>

<div class="insight">💡 <strong>Key insight:</strong> element <code>i</code> from the front must trade places with element <code>i</code> from the back. Swap <code>left</code> and <code>right</code>, move both inward, stop when they cross. This is the canonical two-variable swap <code>a, b = b, a</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>left = 0</code>, <code>right = n−1</code>.</li>
<li>While <code>left &lt; right</code>: swap <code>s[left]</code> and <code>s[right]</code>.</li>
<li><code>left += 1</code>, <code>right -= 1</code>.</li>
</ol>

<h2>🎞️ Visual dry run — s = ['h','e','l','l','o']</h2>
<pre class="viz">L=0 R=4  swap h↔o → ['o','e','l','l','h'] ; L→1 R→3
L=1 R=3  swap e↔l → ['o','l','l','e','h'] ; L→2 R→2
L==R → stop.  Result: ['o','l','l','e','h']</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def reverseString(s):
    left, right = 0, len(s) - 1
    while left &lt; right:
        s[left], s[right] = s[right], s[left]   # in-place swap
        left += 1
        right -= 1</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — n/2 swaps. <strong>Space O(1)</strong> — swaps happen in place.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Empty or single character → loop body never runs; already reversed.</li>
<li>Even length → pointers cross without meeting; every element swapped.</li>
<li>Odd length → the middle element stays put (correct).</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Using <code>left &lt;= right</code> — the middle element would swap with itself (harmless) but it signals a misunderstanding.</li>
<li>Creating a new list and returning it — the problem wants an in-place mutation.</li>
<li>Forgetting to advance both pointers → infinite loop.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Reverse only vowels ([[345]]) → same walk, skip non-vowels.</li>
<li>Reverse in blocks of k ([[541]]).</li>
<li>Reverse a linked list ([[206]]) → pointer rewiring, same spirit.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[345]] · [[541]] · [[151]]</p>
''',

# ============================================================ LC 345 — Reverse Vowels of a String
345: '''
<h2>🧭 How to think about it</h2>
<p>Reverse only the vowels, leaving every other character exactly where it is. That's the two-pointer swap from Reverse String, but each pointer first <strong>skips forward until it lands on a vowel</strong>. Only vowels ever get swapped; consonants are frozen.</p>

<h2>🐢 Brute force first</h2>
<p>Collect the vowels, reverse that list, then splice them back into their original positions: O(n) time, O(n) space. The two-pointer method does it in place.</p>

<div class="insight">💡 <strong>Key insight:</strong> a left pointer walks right until it finds a vowel; a right pointer walks left until it finds a vowel; swap those two vowels, then continue. Non-vowels are stepped over and never touched.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Put the string in a list (Python strings are immutable). <code>left = 0</code>, <code>right = n−1</code>, define a vowel set.</li>
<li>Advance <code>left</code> while <code>s[left]</code> isn't a vowel; retreat <code>right</code> while <code>s[right]</code> isn't a vowel.</li>
<li>If <code>left &lt; right</code>, swap them, then step both inward.</li>
</ol>

<h2>🎞️ Visual dry run — s = "leetcode"</h2>
<pre class="viz">l e e t c o d e     vowels = {e,e,o,e}
L finds 'e'(1), R finds 'e'(7) → swap (both 'e', no visible change); L→2 R→6
L finds 'e'(2), R finds 'o'(5) → swap e↔o → "leotcede"; L→3 R→4
L skips t,c to 4; R at 4 → cross → stop
Result: "leotcede"</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def reverseVowels(s):
    vowels = set("aeiouAEIOU")
    chars = list(s)                       # strings are immutable
    left, right = 0, len(chars) - 1
    while left &lt; right:
        if chars[left] not in vowels:
            left += 1                     # skip consonant on the left
        elif chars[right] not in vowels:
            right -= 1                    # skip consonant on the right
        else:
            chars[left], chars[right] = chars[right], chars[left]
            left += 1; right -= 1
    return "".join(chars)</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — each pointer crosses the string once. <strong>Space O(n)</strong> only because Python needs a mutable list; the algorithm itself is O(1) extra.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>No vowels → nothing swaps; string unchanged.</li>
<li>Uppercase vowels — include them in the vowel set.</li>
<li>All vowels → behaves exactly like full reversal.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Forgetting uppercase vowels.</li>
<li>Swapping before both pointers actually sit on vowels (structure the if/elif/else so a swap only happens when both are vowels).</li>
<li>Re-checking <code>left &lt; right</code> after skips — the loop condition handles it each iteration.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Reverse only letters, skipping punctuation (LC 917) → same skip-and-swap.</li>
<li>Reverse consonants instead → flip the membership test.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[344]] · [[125]] · [[541]]</p>
''',

# ============================================================ LC 541 — Reverse String II
541: '''
<h2>🧭 How to think about it</h2>
<p>March through the string in blocks of <code>2k</code> characters. In each block, reverse the <em>first</em> <code>k</code>; leave the rest alone. The two-pointer reversal is the same as before — the only new idea is stepping the start index by <code>2k</code> each time and clamping the reversal when fewer than <code>k</code> characters remain.</p>

<h2>🐢 Brute force first</h2>
<p>There isn't really a slower approach worth naming — the direct block walk is already O(n). The subtlety is entirely in the boundary rules.</p>

<div class="insight">💡 <strong>Key insight:</strong> iterate the start index <code>i</code> in steps of <code>2k</code>. Reverse <code>s[i : i+k]</code>. If fewer than <code>k</code> characters are left, reverse whatever remains; if between <code>k</code> and <code>2k</code>, reverse exactly the first <code>k</code>. Python slicing with a clamped end handles both cases for free.</p></div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Convert to a list. Loop <code>i = 0, 2k, 4k, …</code> up to the length.</li>
<li>Reverse the sub-range from <code>i</code> to <code>min(i+k, n)</code>.</li>
<li>Leave the next <code>k</code> (or the tail) untouched.</li>
</ol>

<h2>🎞️ Visual dry run — s = "abcdefg", k = 2 (so 2k = 4)</h2>
<pre class="viz">i=0: reverse s[0:2] "ab"→"ba"  → "bacdefg"   (leave s[2:4] "cd")
i=4: reverse s[4:6] "ef"→"fe"  → "bacdfeg"   (leave s[6:] "g")
i=8: past end → stop
Result: "bacdfeg"</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def reverseStr(s, k):
    chars = list(s)
    for i in range(0, len(chars), 2 * k):     # start of each 2k block
        left, right = i, min(i + k, len(chars)) - 1
        while left &lt; right:                   # reverse the first k (clamped)
            chars[left], chars[right] = chars[right], chars[left]
            left += 1; right -= 1
    return "".join(chars)</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — every character is touched at most once. <strong>Space O(n)</strong> for the mutable list (O(1) extra logic).</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Fewer than <code>k</code> chars total → reverse them all.</li>
<li>Between <code>k</code> and <code>2k</code> left → reverse exactly the first <code>k</code>.</li>
<li><code>k</code> larger than the string → whole string reversed.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Stepping by <code>k</code> instead of <code>2k</code> — you'd reverse everything.</li>
<li>Not clamping <code>i+k</code> to the length → index errors on the last block.</li>
<li>Reversing the wrong half of each block.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Reverse the <em>second</em> k of each block → shift the range.</li>
<li>Reverse nodes in k-groups on a linked list ([[25]]) — same block idea, pointer rewiring.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[344]] · [[345]] · [[151]]</p>
''',

# ============================================================ LC 26 — Remove Duplicates from Sorted Array
26: '''
<h2>🧭 How to think about it</h2>
<p>The array is sorted, so duplicates are neighbors. Keep a <strong>write pointer</strong> marking where the next unique value goes; a read pointer scans ahead. Whenever the read value differs from the last kept value, it's new — copy it to the write slot and advance. The front of the array becomes the deduplicated answer.</p>

<h2>🐢 Brute force first</h2>
<p>Build a new list of uniques, or use a set — both O(n) space. The problem demands in-place with O(1) extra space, which the write-pointer delivers.</p>

<div class="insight">💡 <strong>Key insight:</strong> a slow "write" index trails behind a fast "read" index. <code>write</code> always points just past the last unique value. Copy forward only when <code>nums[read] != nums[write-1]</code>. The count of uniques is the final <code>write</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>If empty, return 0. Else <code>write = 1</code> (first element is always kept).</li>
<li>For <code>read</code> from 1 to n−1: if <code>nums[read] != nums[write-1]</code>, set <code>nums[write] = nums[read]</code>, <code>write += 1</code>.</li>
<li>Return <code>write</code> — the length of the unique prefix.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [0, 0, 1, 1, 1, 2]</h2>
<pre class="viz">write=1
read=1 (0) == nums[0](0) → skip
read=2 (1) != nums[0](0) → nums[1]=1; write=2 → [0,1,1,1,1,2]
read=3 (1) == nums[1](1) → skip
read=4 (1) == nums[1](1) → skip
read=5 (2) != nums[1](1) → nums[2]=2; write=3 → [0,1,2,1,1,2]
Return 3; first 3 = [0,1,2]</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def removeDuplicates(nums):
    if not nums:
        return 0
    write = 1                        # index where the next unique goes
    for read in range(1, len(nums)):
        if nums[read] != nums[write - 1]:   # new value (sorted ⇒ compare last kept)
            nums[write] = nums[read]
            write += 1
    return write                     # length of the unique prefix</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — one scan. <strong>Space O(1)</strong> — writes happen inside the same array.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Empty array → return 0.</li>
<li>All identical → <code>write</code> stays 1.</li>
<li>All unique → every element copies onto itself; <code>write</code> ends at n.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Comparing <code>nums[read]</code> to <code>nums[read-1]</code> instead of <code>nums[write-1]</code> — usually equivalent here, but the "last kept" framing generalizes to the keep-two variant.</li>
<li>Starting <code>write</code> at 0 and forgetting the first element is always unique.</li>
<li>Returning the modified array instead of the count.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Allow each value at most twice ([[80]]) → compare against <code>nums[write-2]</code>.</li>
<li>Unsorted input → sort first, or use a set (loses O(1) space).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[80]] · [[27]] · [[283]]</p>
''',

# ============================================================ LC 27 — Remove Element
27: '''
<h2>🧭 How to think about it</h2>
<p>Delete every occurrence of a given value, in place. Use a <strong>write pointer</strong>: scan the array, and each time you meet a value you want to <em>keep</em>, write it at the write index and advance. Everything equal to <code>val</code> is simply skipped, so it gets overwritten.</p>

<h2>🐢 Brute force first</h2>
<p>Filtering into a new list is O(n) space. The write-pointer compaction does it in place with O(1) extra space.</p>

<div class="insight">💡 <strong>Key insight:</strong> <code>write</code> counts how many keepers we've placed. For each element, keep-or-drop: if it isn't <code>val</code>, place it at <code>nums[write]</code> and bump <code>write</code>. The first <code>write</code> entries are the survivors, in original order.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>write = 0</code>.</li>
<li>For each <code>read</code>: if <code>nums[read] != val</code>, set <code>nums[write] = nums[read]</code>, <code>write += 1</code>.</li>
<li>Return <code>write</code>.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [3, 2, 2, 3], val = 3</h2>
<pre class="viz">write=0
read=0 (3) == val → skip
read=1 (2) != val → nums[0]=2; write=1 → [2,2,2,3]
read=2 (2) != val → nums[1]=2; write=2 → [2,2,2,3]
read=3 (3) == val → skip
Return 2; first 2 = [2,2]</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def removeElement(nums, val):
    write = 0
    for read in range(len(nums)):
        if nums[read] != val:        # a keeper
            nums[write] = nums[read]
            write += 1
    return write                     # number of kept elements</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — single pass. <strong>Space O(1)</strong> — in-place writes.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Empty array → return 0.</li>
<li><code>val</code> absent → every element copies onto itself; return n.</li>
<li>All elements equal <code>val</code> → return 0.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Trying to preserve the elements beyond <code>write</code> — they may be leftover garbage and the problem says they don't matter.</li>
<li>Returning the array instead of the new length.</li>
<li>Using an extra list, defeating the in-place requirement.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>When removals are rare, swap the victim with the last element and shrink — fewer writes.</li>
<li>Remove duplicates instead of a specific value ([[26]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[26]] · [[283]] · [[905]]</p>
''',

# ============================================================ LC 75 — Sort Colors
75: '''
<h2>🧭 How to think about it</h2>
<p>Only three values exist — 0, 1, 2 (red, white, blue). Sorting them is really <em>partitioning</em> into three regions in one pass. The Dutch National Flag algorithm uses three pointers to grow a "0s" region on the left, a "2s" region on the right, and leave "1s" in the middle.</p>

<h2>🐢 Brute force first</h2>
<p>Counting sort: tally how many 0s, 1s, 2s, then overwrite — two passes, O(n). The one-pass three-pointer version is the classic follow-up.</p>

<div class="insight">💡 <strong>Key insight:</strong> keep <code>low</code> (end of the 0s), <code>mid</code> (current element), <code>high</code> (start of the 2s). If <code>nums[mid]==0</code> swap it down to <code>low</code>; if <code>==2</code> swap it up to <code>high</code> (and don't advance <code>mid</code>, since the swapped-in value is unexamined); if <code>==1</code> just advance <code>mid</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>low = 0</code>, <code>mid = 0</code>, <code>high = n−1</code>.</li>
<li>While <code>mid &lt;= high</code>: inspect <code>nums[mid]</code>.</li>
<li>0 → swap <code>mid</code>,<code>low</code>; <code>low += 1</code>, <code>mid += 1</code>.</li>
<li>1 → <code>mid += 1</code>.</li>
<li>2 → swap <code>mid</code>,<code>high</code>; <code>high -= 1</code> (leave <code>mid</code> — re-examine the new value).</li>
</ol>

<h2>🎞️ Visual dry run — nums = [2, 0, 2, 1, 1, 0]</h2>
<pre class="viz">low=0 mid=0 high=5 : nums[0]=2 → swap(0,5) → [0,0,2,1,1,2]; high=4
low=0 mid=0 high=4 : nums[0]=0 → swap(0,0); low=1, mid=1
low=1 mid=1 high=4 : nums[1]=0 → swap(1,1); low=2, mid=2
low=2 mid=2 high=4 : nums[2]=2 → swap(2,4) → [0,0,1,1,2,2]; high=3
low=2 mid=2 high=3 : nums[2]=1 → mid=3
low=2 mid=3 high=3 : nums[3]=1 → mid=4 &gt; high → stop
Result: [0,0,1,1,2,2]</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def sortColors(nums):
    low, mid, high = 0, 0, len(nums) - 1
    while mid &lt;= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1; mid += 1          # value swapped down is a 1 already seen
        elif nums[mid] == 1:
            mid += 1
        else:  # nums[mid] == 2
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1                    # DON'T advance mid: new value unknown</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — <code>mid</code> and <code>high</code> together cover the array once. <strong>Space O(1)</strong> — in-place swaps.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Already sorted → swaps become no-ops, pointers slide through.</li>
<li>Single value throughout → trivially handled.</li>
<li>Two colors only → the missing region stays empty.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Advancing <code>mid</code> after a 2-swap — the value pulled from <code>high</code> hasn't been checked yet.</li>
<li>Using <code>mid &lt; high</code> instead of <code>&lt;=</code> — the final element goes unprocessed.</li>
<li>Overcomplicating with counting when the one-pass version was requested.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Sort by parity ([[905]]) → a two-region version of the same idea.</li>
<li>k colors → counting sort, or repeated partitioning.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[905]] · [[27]] · [[283]]</p>
''',

# ============================================================ LC 80 — Remove Duplicates from Sorted Array II
80: '''
<h2>🧭 How to think about it</h2>
<p>Same as Remove Duplicates, but each value may stay <strong>up to twice</strong>. The write-pointer trick generalizes with one clever comparison: an incoming value is allowed only if it differs from the element <em>two slots back</em> in the kept region — that guarantees at most two copies survive.</p>

<h2>🐢 Brute force first</h2>
<p>Count occurrences with a dict and rebuild → O(n) space. The two-back comparison keeps it in place, O(1) extra.</p>

<div class="insight">💡 <strong>Key insight:</strong> keep a value <code>x</code> if <code>write &lt; 2</code> (the first two always survive) OR <code>x != nums[write-2]</code>. Because the array is sorted, <code>nums[write-2] == x</code> means two copies of <code>x</code> are already kept, so a third must be dropped.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>write = 0</code>.</li>
<li>For each <code>x = nums[read]</code>: if <code>write &lt; 2</code> or <code>x != nums[write-2]</code>, place <code>nums[write] = x</code>, <code>write += 1</code>.</li>
<li>Return <code>write</code>.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [1, 1, 1, 2, 2, 3]</h2>
<pre class="viz">write=0
x=1: write&lt;2 → nums[0]=1; write=1
x=1: write&lt;2 → nums[1]=1; write=2
x=1: nums[write-2]=nums[0]=1 == x → DROP
x=2: nums[0]=1 != 2 → nums[2]=2; write=3
x=2: nums[1]=1 != 2 → nums[3]=2; write=4
x=3: nums[2]=2 != 3 → nums[4]=3; write=5
Return 5; first 5 = [1,1,2,2,3]</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def removeDuplicates(nums):
    write = 0
    for x in nums:
        if write &lt; 2 or x != nums[write - 2]:   # allow at most two copies
            nums[write] = x
            write += 1
    return write</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — single scan. <strong>Space O(1)</strong> — in-place.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Length ≤ 2 → everything kept (the <code>write &lt; 2</code> guard).</li>
<li>All identical → exactly two survive.</li>
<li>All distinct → all kept.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Comparing to <code>nums[read-2]</code> instead of <code>nums[write-2]</code> — the read side still has un-compacted duplicates.</li>
<li>Hard-coding "at most 2" logic with counters instead of the elegant two-back check.</li>
<li>Forgetting the <code>write &lt; 2</code> base case → index error.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>At most <code>k</code> copies → compare against <code>nums[write-k]</code> — the same one-liner generalizes.</li>
<li>At most one copy ([[26]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[26]] · [[27]] · [[283]]</p>
''',

# ============================================================ LC 283 — Move Zeroes
283: '''
<h2>🧭 How to think about it</h2>
<p>Push all zeros to the end while keeping the non-zeros in their original order. A <strong>write pointer</strong> compacts the non-zeros to the front; then the remaining slots are filled with zeros. A tidy variant swaps as it goes so it's a single pass with no cleanup.</p>

<h2>🐢 Brute force first</h2>
<p>Build a new list of non-zeros padded with zeros → O(n) space. The write-pointer method is in place, O(1) extra.</p>

<div class="insight">💡 <strong>Key insight:</strong> <code>write</code> marks the next spot for a non-zero. Each time <code>nums[read]</code> is non-zero, <em>swap</em> it into <code>nums[write]</code> and advance <code>write</code>. Zeros naturally drift to the back because they're the values left behind.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>write = 0</code>.</li>
<li>For each <code>read</code>: if <code>nums[read] != 0</code>, swap <code>nums[write]</code> and <code>nums[read]</code>, then <code>write += 1</code>.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [0, 1, 0, 3, 12]</h2>
<pre class="viz">write=0
read=0 (0) → skip
read=1 (1) → swap(0,1) → [1,0,0,3,12]; write=1
read=2 (0) → skip
read=3 (3) → swap(1,3) → [1,3,0,0,12]; write=2
read=4 (12)→ swap(2,4) → [1,3,12,0,0]; write=3
Result: [1,3,12,0,0]</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def moveZeroes(nums):
    write = 0
    for read in range(len(nums)):
        if nums[read] != 0:
            nums[write], nums[read] = nums[read], nums[write]  # swap non-zero forward
            write += 1</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — one pass. <strong>Space O(1)</strong> — in-place swaps.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>No zeros → every element swaps with itself; order preserved.</li>
<li>All zeros → <code>write</code> never moves; array unchanged.</li>
<li>Zeros already at the end → no-op swaps.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Copying non-zeros forward and then forgetting to zero-fill the tail (if you use the copy variant instead of swapping).</li>
<li>Not preserving the relative order of non-zeros (some naive swaps scramble it).</li>
<li>Using extra storage.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Move a specific value to the end → replace the <code>!= 0</code> test.</li>
<li>Minimize the number of writes → skip self-swaps when <code>write == read</code>.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[27]] · [[26]] · [[905]]</p>
''',

# ============================================================ LC 443 — String Compression
443: '''
<h2>🧭 How to think about it</h2>
<p>Compress runs of the same character in place: <code>aaab</code> becomes <code>a3b</code>. You need <strong>two pointers</strong> — a <em>read</em> pointer that counts each run, and a <em>write</em> pointer that lays down the character followed by its count's digits (only when the count is &gt; 1). The answer's length is where <code>write</code> ends up.</p>

<h2>🐢 Brute force first</h2>
<p>Building the compressed string separately is O(n) space; the problem wants in-place with O(1) extra. Because the compressed form is never longer than the input, the write pointer safely trails the read pointer.</p>

<div class="insight">💡 <strong>Key insight:</strong> a run never expands — one char plus its count digits is at most as long as the run itself. So <code>write</code> can never overtake <code>read</code>. Scan each run, write the char, then write the count's digits (skip the digits when the count is 1).</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>read = 0</code>, <code>write = 0</code>.</li>
<li>At each run start, remember the char; advance <code>read</code> while it stays the same, counting length.</li>
<li>Write the char at <code>write</code>; if count &gt; 1, write each digit of the count.</li>
<li>Return <code>write</code>.</li>
</ol>

<h2>🎞️ Visual dry run — chars = ['a','a','b','b','c','c','c']</h2>
<pre class="viz">run 'a' ×2 → write 'a','2' → [a,2,...] write=2
run 'b' ×2 → write 'b','2' → [a,2,b,2,...] write=4
run 'c' ×3 → write 'c','3' → [a,2,b,2,c,3,...] write=6
Return 6; first 6 = ['a','2','b','2','c','3']</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def compress(chars):
    write = read = 0
    n = len(chars)
    while read &lt; n:
        ch = chars[read]
        count = 0
        while read &lt; n and chars[read] == ch:   # measure the run
            read += 1; count += 1
        chars[write] = ch; write += 1           # write the character
        if count &gt; 1:                            # write digits only if needed
            for d in str(count):
                chars[write] = d; write += 1
    return write</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — each character read once, each output slot written once. <strong>Space O(1)</strong> — writes stay inside the array (the <code>str(count)</code> is at most a few digits).</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Run length 1 → write only the char, no digit.</li>
<li>Counts ≥ 10 → written as multiple digit characters (e.g., "12").</li>
<li>Single character input → returns 1.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Writing the count as a number instead of individual digit characters.</li>
<li>Writing "1" for singleton runs.</li>
<li>Letting <code>write</code> pass <code>read</code> (can't happen if you follow the run structure, but sloppy indexing breaks it).</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Decompress the run-length encoding → inverse two-pointer walk.</li>
<li>Return a new string instead of in-place → simpler, O(n) space.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[26]] · [[27]] · [[283]]</p>
''',

# ============================================================ LC 905 — Sort Array By Parity
905: '''
<h2>🧭 How to think about it</h2>
<p>Put all even numbers before all odd numbers (any order within each group). This is a two-way partition, exactly like the first step of quicksort: one pointer at each end, swap an out-of-place pair, and close in.</p>

<h2>🐢 Brute force first</h2>
<p>Two lists (evens, odds) concatenated → O(n) space. The two-pointer swap does it in place, O(1) extra.</p>

<div class="insight">💡 <strong>Key insight:</strong> <code>left</code> looks for an odd on the left side (which shouldn't be there); <code>right</code> looks for an even on the right side. When both find a misplaced value, swap them. Repeat until the pointers cross — evens end up left, odds right.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>left = 0</code>, <code>right = n−1</code>.</li>
<li>Advance <code>left</code> while <code>nums[left]</code> is even; retreat <code>right</code> while <code>nums[right]</code> is odd.</li>
<li>If <code>left &lt; right</code>, swap them, then step both.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [3, 1, 2, 4]</h2>
<pre class="viz">L=0(3 odd) stops; R=3(4 even) stops → swap → [4,1,2,3]; L→1 R→2
L=1(1 odd) stops; R=2(2 even) stops → swap → [4,2,1,3]; L→2 R→1 cross
Result: [4,2,1,3] (evens first)</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def sortArrayByParity(nums):
    left, right = 0, len(nums) - 1
    while left &lt; right:
        if nums[left] % 2 == 0:
            left += 1                    # even is already on the correct side
        elif nums[right] % 2 == 1:
            right -= 1                   # odd is already on the correct side
        else:                            # nums[left] odd, nums[right] even
            nums[left], nums[right] = nums[right], nums[left]
            left += 1; right -= 1
    return nums</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — pointers cross once. <strong>Space O(1)</strong> — in-place swaps.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Already partitioned → pointers slide, no swaps.</li>
<li>All even or all odd → one pointer runs to the other; no swaps.</li>
<li>Single element → loop doesn't run.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Swapping before confirming <em>both</em> ends are misplaced (structure the if/elif/else).</li>
<li>Assuming a required order within the even/odd groups — any order is accepted.</li>
<li>Off-by-one at the crossing.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Even at even indices, odd at odd indices ([[922]]).</li>
<li>Stable partition (preserve order) → needs the write-pointer approach with a second pass.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[922]] · [[75]] · [[283]]</p>
''',

# ============================================================ LC 922 — Sort Array By Parity II
922: '''
<h2>🧭 How to think about it</h2>
<p>Now the parity must match the <em>index</em>: even numbers at even indices, odd numbers at odd indices. Run <strong>two pointers</strong> — one over even positions (0, 2, 4, …) and one over odd positions (1, 3, 5, …). Whenever both point at a wrongly-placed number, swap them into place.</p>

<h2>🐢 Brute force first</h2>
<p>Separate evens and odds into two lists, then interleave → O(n) space. The two-index-pointer swap is in place, O(1) extra.</p>

<div class="insight">💡 <strong>Key insight:</strong> the count of evens equals the count of even indices, so a misplaced even at an odd index is always matched by a misplaced odd at an even index. Advance <code>even</code> until it finds an odd value sitting at an even index; advance <code>odd</code> until it finds an even value at an odd index; swap the pair.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>even = 0</code>, <code>odd = 1</code>.</li>
<li>Advance <code>even</code> by 2 while <code>nums[even]</code> is even (correctly placed).</li>
<li>Advance <code>odd</code> by 2 while <code>nums[odd]</code> is odd (correctly placed).</li>
<li>If both are in range, swap the mismatched pair; repeat.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [4, 2, 5, 7]</h2>
<pre class="viz">even=0(4 even) ok → even=2(5 odd) STOP (odd value at even index)
odd=1(2 even) STOP (even value at odd index)
swap idx2,idx1 → [4,5,2,7]; even→4 (out) → done
Result: [4,5,2,7]  (even idx: 4,2 ; odd idx: 5,7)</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def sortArrayByParityII(nums):
    n = len(nums)
    even, odd = 0, 1
    while even &lt; n and odd &lt; n:
        if nums[even] % 2 == 0:
            even += 2                    # correctly placed even
        elif nums[odd] % 2 == 1:
            odd += 2                     # correctly placed odd
        else:                            # both misplaced → fix together
            nums[even], nums[odd] = nums[odd], nums[even]
            even += 2; odd += 2
    return nums</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — each index visited once. <strong>Space O(1)</strong> — in-place.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Already valid → pointers slide, no swaps.</li>
<li>Every even slot wrong → each fixed exactly once against its odd counterpart.</li>
<li>Length 2 → at most one swap.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Stepping by 1 instead of 2 — you'd revisit already-correct positions.</li>
<li>Swapping when only one side is misplaced (impossible to be alone, but bad structure can force a wrong swap).</li>
<li>Using two separate output lists when in-place is requested.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Simple parity partition without index constraint ([[905]]).</li>
<li>Three-way by index-mod-3 → generalized bucket placement.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[905]] · [[75]] · [[283]]</p>
''',

# ============================================================ LC 925 — Long Pressed Name
925: '''
<h2>🧭 How to think about it</h2>
<p>Someone typed your name but a key may have been held down, repeating letters. Decide whether <code>typed</code> could be your <code>name</code> with some characters long-pressed. Walk <strong>two pointers</strong> — one on <code>name</code>, one on <code>typed</code> — matching letter by letter; extra repeats in <code>typed</code> are allowed only if they repeat the character you just matched.</p>

<h2>🐢 Brute force first</h2>
<p>Run-length encode both strings and compare characters with counts (typed's count must be ≥ name's for each run). The two-pointer walk does the same check without building the encodings.</p>

<div class="insight">💡 <strong>Key insight:</strong> pointer <code>i</code> on name, <code>j</code> on typed. If <code>name[i] == typed[j]</code>, both advance. Otherwise <code>typed[j]</code> must equal the <em>previous</em> matched character (a long-press) — advance only <code>j</code>. If neither holds, it's not a match. At the end, <code>i</code> must have consumed all of name.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>i = j = 0</code>.</li>
<li>If <code>name[i] == typed[j]</code>: <code>i += 1</code>, <code>j += 1</code>.</li>
<li>Else if <code>j &gt; 0</code> and <code>typed[j] == typed[j−1]</code>: <code>j += 1</code> (long-press).</li>
<li>Else return False.</li>
<li>After the loop, return <code>i == len(name)</code> (all of name matched; trailing typed repeats are fine).</li>
</ol>

<h2>🎞️ Visual dry run — name = "alex", typed = "aaleex"</h2>
<pre class="viz">i0=a j0=a match → i1 j1
i1=l j1=a  a==typed[0]a long-press → j2
i1=l j2=l match → i2 j3
i2=e j3=e match → i3 j4
i3=x j4=e  e==typed[3]e long-press → j5
i3=x j5=x match → i4 j6 (end)
i==len(name)=4 → True</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def isLongPressedName(name, typed):
    i, j = 0, 0
    while j &lt; len(typed):
        if i &lt; len(name) and name[i] == typed[j]:
            i += 1; j += 1               # normal match
        elif j &gt; 0 and typed[j] == typed[j - 1]:
            j += 1                        # long-press of the previous char
        else:
            return False
    return i == len(name)                 # every name char consumed</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n + m)</strong> — each pointer advances through its string once. <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>First characters differ → immediate False (no previous char to long-press).</li>
<li><code>typed</code> shorter than <code>name</code> → <code>i</code> can't finish → False.</li>
<li>Extra trailing repeats in typed → fine, as long as name is fully matched.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Forgetting the final <code>i == len(name)</code> check — typed may end before name is consumed.</li>
<li>Allowing a long-press against the wrong (not-just-matched) character.</li>
<li>Index errors when <code>j == 0</code> and the first chars mismatch.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Is one string a subsequence of another ([[392]]) — related pointer walk.</li>
<li>Allow bounded press counts → track run lengths explicitly.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[392]] · [[844]] · [[443]]</p>
''',

# ============================================================ LC 2337 — Move Pieces to Obtain a String
2337: '''
<h2>🧭 How to think about it</h2>
<p>Two boards of <code>'L'</code>, <code>'R'</code>, and <code>'_'</code> (blank). An <code>'L'</code> can only slide left, an <code>'R'</code> only right; blanks are free space. Can <code>start</code> become <code>target</code>? Ignore the blanks and compare the <strong>sequence of pieces</strong>: it must be identical. Then use two pointers to check each piece can physically reach its target position given its allowed direction.</p>

<h2>🐢 Brute force first</h2>
<p>Simulating every possible move is exponential. The insight-based two-pointer check is O(n): the relative order of non-blank pieces never changes, so it's a positional feasibility test.</p>

<div class="insight">💡 <strong>Key insight:</strong> compare only non-blank characters, in order — they must match exactly (same L/R sequence). For each matched piece, an <code>'L'</code> in start must be at an index <strong>≥</strong> its target index (it moves left), and an <code>'R'</code> must be at an index <strong>≤</strong> its target index (it moves right).</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Two pointers <code>i</code> (start) and <code>j</code> (target); skip blanks in each.</li>
<li>When both point at pieces, they must be the same letter; else return False.</li>
<li>For <code>'L'</code>: require <code>i &gt;= j</code>. For <code>'R'</code>: require <code>i &lt;= j</code>.</li>
<li>Advance both. At the end both pointers must have reached the end together.</li>
</ol>

<h2>🎞️ Visual dry run — start = "_L__", target = "L___"</h2>
<pre class="viz">i skips '_' to 1 ('L'); j at 0 ('L')  → same letter, 'L' needs i≥j: 1≥0 ✓
advance: i→2 (skip blanks to end), j→1 (skip to end)
both reach end together → True  (the L slid left from index1 to index0)</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def canChange(start, target):
    n = len(start)
    i = j = 0
    while i &lt; n or j &lt; n:
        while i &lt; n and start[i] == '_':  i += 1   # skip blanks
        while j &lt; n and target[j] == '_': j += 1
        if i == n or j == n:                        # one ran out of pieces
            return i == n and j == n                # both must end together
        if start[i] != target[j]:
            return False                            # different piece order
        if start[i] == 'L' and i &lt; j:
            return False                            # 'L' can't move right
        if start[i] == 'R' and i &gt; j:
            return False                            # 'R' can't move left
        i += 1; j += 1
    return True</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — each pointer scans once. <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Different piece counts → one pointer finishes first → False.</li>
<li>Same string → trivially True.</li>
<li>Piece order differs → caught by the letter-mismatch check.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Forgetting that L moves left (needs <code>i ≥ j</code>) and R moves right (needs <code>i ≤ j</code>) — mixing them up.</li>
<li>Not verifying both pointers end simultaneously.</li>
<li>Comparing including blanks.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Report the sequence of moves → harder; needs a queue of positions.</li>
<li>Pieces that move both directions → the positional constraints relax.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[2938]] · [[844]] · [[925]]</p>
''',

# ============================================================ LC 2938 — Separate Black and White Balls
2938: '''
<h2>🧭 How to think about it</h2>
<p>A string of <code>'0'</code> (white) and <code>'1'</code> (black); you may swap adjacent balls, and want all whites on the left and blacks on the right with the <em>minimum</em> number of adjacent swaps. Think of each white ball: it must "pass" every black ball currently to its left. Count those crossings and you have the answer.</p>

<h2>🐢 Brute force first</h2>
<p>Bubble-sort style adjacent swaps simulate the process but are O(n²). Counting crossings in one pass is O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> sweep left to right counting the blacks seen so far. Every time you hit a white ball, it needs exactly <code>(number of blacks already passed)</code> adjacent swaps to move past them. Sum that over all whites. Equivalently: a pointer tracks the destination for the next white; the gap is the swaps needed.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>ones = 0</code> (blacks seen), <code>swaps = 0</code>.</li>
<li>For each character: if <code>'1'</code>, increment <code>ones</code>.</li>
<li>If <code>'0'</code>, it must cross all current blacks → <code>swaps += ones</code>.</li>
<li>Return <code>swaps</code>.</li>
</ol>

<h2>🎞️ Visual dry run — s = "100"</h2>
<pre class="viz">ch='1' → ones=1
ch='0' → swaps += 1 (this white passes the one black) → swaps=1
ch='0' → swaps += 1 → swaps=2
Answer: 2   ("100" → "010" → "001")</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def minimumSteps(s):
    ones = 0        # black balls ('1') seen so far
    swaps = 0
    for ch in s:
        if ch == '1':
            ones += 1
        else:                       # a white ball must cross every black to its left
            swaps += ones
    return swaps</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — single pass. <strong>Space O(1)</strong>. (Use a 64-bit-safe integer type in other languages; Python ints are unbounded.)</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Already sorted ("0…01…1") → 0 swaps.</li>
<li>All same color → 0 swaps.</li>
<li>Reverse sorted ("1…10…0") → the maximum, counted correctly.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Simulating adjacent swaps → O(n²) and too slow for large inputs.</li>
<li>Integer overflow in languages with fixed-width ints (the count can be ~n²/4).</li>
<li>Counting whites-before-blacks instead of blacks-before-whites — pick one consistent framing.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>All blacks on the left instead → mirror the count.</li>
<li>Three colors → reduces toward the Dutch-flag idea ([[75]]) for placement, but swap-counting differs.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[75]] · [[905]] · [[2337]]</p>
''',

# ============================================================ LC 141 — Linked List Cycle
141: '''
<h2>🧭 How to think about it</h2>
<p>Does the linked list loop back on itself? Picture two runners on a track: a slow one taking one step, a fast one taking two. On a straight track the fast runner reaches the end. On a <em>circular</em> track the fast runner keeps lapping and must eventually collide with the slow one. That collision is the signal for a cycle — and it needs no extra memory.</p>

<h2>🐢 Brute force first</h2>
<p>Store every visited node in a set; if you revisit one, there's a cycle — O(n) time, O(n) space. Floyd's two-pointer method gets O(1) space.</p>

<div class="insight">💡 <strong>Key insight:</strong> move <code>slow</code> by 1 and <code>fast</code> by 2. If there's no cycle, <code>fast</code> hits <code>None</code>. If there is, <code>fast</code> gains one step on <code>slow</code> each iteration inside the loop and inevitably lands on it. (Tortoise and hare.)</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>slow = fast = head</code>.</li>
<li>While <code>fast</code> and <code>fast.next</code> exist: <code>slow = slow.next</code>, <code>fast = fast.next.next</code>.</li>
<li>If <code>slow is fast</code>, return True.</li>
<li>If the loop exits, return False.</li>
</ol>

<h2>🎞️ Visual dry run — 3 → 2 → 0 → −4 ↺ back to 2</h2>
<pre class="viz">slow=3 fast=3
step: slow=2 fast=0
step: slow=0 fast=2   (fast looped)
step: slow=-4 fast=-4 → slow is fast → cycle! True</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def hasCycle(head):
    slow = fast = head
    while fast and fast.next:        # fast needs two steps available
        slow = slow.next
        fast = fast.next.next
        if slow is fast:            # they collided → cycle
            return True
    return False                    # fast fell off the end → no cycle</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — before meeting, the pointers traverse O(n) nodes. <strong>Space O(1)</strong> — two pointers.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Empty list or single node with no self-loop → loop never triggers → False.</li>
<li>Single node pointing to itself → detected on the first step.</li>
<li>Cycle at the very end → still caught.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Checking <code>slow == fast</code> before moving them — they start equal at <code>head</code>, giving a false positive.</li>
<li>Forgetting the <code>fast.next</code> guard → <code>None.next</code> crash.</li>
<li>Comparing values instead of node identity (use <code>is</code>).</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Return the cycle's entry node ([[142]]) → after meeting, restart one pointer at head.</li>
<li>Cycle length → keep moving one pointer after the meeting until it returns.</li>
<li>Happy Number ([[202]]) applies the same trick to a number sequence.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[142]] · [[202]] · [[287]]</p>
''',

# ============================================================ LC 202 — Happy Number
202: '''
<h2>🧭 How to think about it</h2>
<p>Repeatedly replace a number by the sum of the squares of its digits. If you reach 1, it's "happy"; otherwise you fall into a loop that never hits 1. "A sequence that either reaches a target or cycles forever" is exactly a <strong>cycle-detection</strong> problem — the same tortoise-and-hare from Linked List Cycle, but the "next node" is computed arithmetically.</p>

<h2>🐢 Brute force first</h2>
<p>Track seen numbers in a set; if a value repeats before reaching 1, it's unhappy — O(1)-ish space bounded by how many distinct values appear. Floyd's two-pointer version uses truly O(1) space.</p>

<div class="insight">💡 <strong>Key insight:</strong> define <code>next(n)</code> = sum of squares of digits. Run <code>slow = next(n)</code> and <code>fast = next(next(n))</code>. If they meet at 1 → happy; if they meet anywhere else → a cycle that never reaches 1 → not happy.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Write a helper that squares and sums digits.</li>
<li><code>slow</code> steps once, <code>fast</code> steps twice per iteration.</li>
<li>Stop when they meet. Return whether the meeting value is 1.</li>
</ol>

<h2>🎞️ Visual dry run — n = 19</h2>
<pre class="viz">next(19)=1²+9²=82, next(82)=68, next(68)=100, next(100)=1
slow: 82, 68, 1 ...
fast: 68, 1, 1 ...
they converge on 1 → Happy → True</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def isHappy(n):
    def nxt(x):
        total = 0
        while x:
            x, d = divmod(x, 10)   # peel last digit
            total += d * d
        return total

    slow, fast = n, nxt(n)
    while fast != 1 and slow != fast:
        slow = nxt(slow)           # one step
        fast = nxt(nxt(fast))      # two steps
    return fast == 1               # reached 1 ⇒ happy; else stuck in a cycle</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(log n)</strong> per step and a bounded number of steps (values quickly collapse below 1000), so effectively O(log n) overall. <strong>Space O(1)</strong> with the two-pointer method.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li><code>n = 1</code> → already happy.</li>
<li>Known unhappy cycle contains 4 → the pointers meet at a non-1 value.</li>
<li>Large <code>n</code> → the digit-square-sum shrinks it fast.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Looping <code>while fast != 1</code> only — you also need <code>slow != fast</code> to break out of unhappy cycles.</li>
<li>Off-by-one in initializing <code>fast = nxt(n)</code> vs <code>n</code>.</li>
<li>Recomputing digit sums inefficiently.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Use a set instead of Floyd → simpler, slightly more memory.</li>
<li>Other digit functions (cubes, etc.) → same detection framework.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[141]] · [[287]] · [[142]]</p>
''',

# ============================================================ LC 287 — Find the Duplicate Number
287: '''
<h2>🧭 How to think about it</h2>
<p>An array of <code>n+1</code> numbers, each in <code>1..n</code>, has exactly one repeated value. The elegant O(1)-space trick reads the array as a <strong>linked list</strong>: from index <code>i</code>, "follow" to index <code>nums[i]</code>. Because some value repeats, two indices point to the same place — creating a cycle. Floyd's tortoise-and-hare finds the cycle's entrance, which is the duplicate.</p>

<h2>🐢 Brute force first</h2>
<p>A set of seen values is O(n) space; sorting mutates the array; both are disallowed by the "no modification, O(1) space" constraints. Cycle detection satisfies both.</p>

<div class="insight">💡 <strong>Key insight:</strong> treat <code>nums[i]</code> as "next index". The duplicate value is the index that two others jump to, so the functional graph has a cycle whose <em>entry node</em> equals the duplicate. Phase 1: find a meeting point with slow/fast. Phase 2: walk one pointer from the start until they meet again — that's the entrance.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>slow = fast = nums[0]</code>.</li>
<li>Advance <code>slow = nums[slow]</code>, <code>fast = nums[nums[fast]]</code> until they meet.</li>
<li>Reset <code>slow = nums[0]</code>; step both by one until they meet — the meeting value is the duplicate.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [1, 3, 4, 2, 2]</h2>
<pre class="viz">Phase 1 (find meeting):
slow: 1 → nums[1]=3 → nums[3]=2 → nums[2]=4 ...
fast: 1 → nums[nums[1]]=nums[3]=2 → nums[nums[2]]=nums[4]=2 → ...
they meet at value 4 (inside the cycle)
Phase 2 (find entrance):
slow=nums[0]=1, other=4 → step: 3 vs 2 → 2 vs 4 → 4 vs 2 → 2 vs 2 meet at 2
Duplicate = 2</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def findDuplicate(nums):
    slow = fast = nums[0]
    # Phase 1: find a point inside the cycle
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
    # Phase 2: entrance of the cycle == duplicate
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
    return slow</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — both phases are linear. <strong>Space O(1)</strong> — array untouched, just indices.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>The duplicate appears more than twice → still exactly one repeated <em>value</em>, still works.</li>
<li>Duplicate is the first or last value → the graph still has a cycle.</li>
<li>Minimum size (n=1, array length 2) → the two equal entries meet immediately.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Starting phase 2 from the meeting point rather than <code>nums[0]</code>.</li>
<li>Advancing <code>fast</code> by only one step in phase 2 (it must slow to one step there).</li>
<li>Modifying the array (e.g., marking visited) when the problem forbids it.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>If modification were allowed → index-as-marker or cyclic sort ([[442]], [[448]]).</li>
<li>Binary search on the value range (count ≤ mid) → O(n log n), also O(1) space.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[141]] · [[142]] · [[202]]</p>
''',

# ============================================================ LC 392 — Is Subsequence
392: '''
<h2>🧭 How to think about it</h2>
<p>Is <code>s</code> a subsequence of <code>t</code> — can you get <code>s</code> by deleting some characters of <code>t</code> without reordering? Walk <strong>two pointers</strong>: one over <code>s</code>, one over <code>t</code>. Advance through <code>t</code>, and every time its character matches the current character of <code>s</code>, tick <code>s</code> forward. If you consume all of <code>s</code>, it's a subsequence.</p>

<h2>🐢 Brute force first</h2>
<p>There's no meaningfully slower natural approach; the greedy two-pointer scan is already O(n). The interesting complexity is in the follow-up (many queries).</p>

<div class="insight">💡 <strong>Key insight:</strong> greedily match each character of <code>s</code> to the <em>earliest</em> possible position in <code>t</code>. A single pointer over <code>s</code> only advances on a match; a pointer over <code>t</code> always advances. If <code>s</code>'s pointer reaches its end, every character was found in order.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>i = 0</code> (into s), <code>j = 0</code> (into t).</li>
<li>While both in range: if <code>s[i] == t[j]</code>, <code>i += 1</code>. Always <code>j += 1</code>.</li>
<li>Return <code>i == len(s)</code>.</li>
</ol>

<h2>🎞️ Visual dry run — s = "abc", t = "ahbgdc"</h2>
<pre class="viz">i0=a j0=a match → i1 j1
i1=b j1=h no  → j2
i1=b j2=b match → i2 j3
i2=c j3=g no  → j4
i2=c j4=d no  → j5
i2=c j5=c match → i3 (end of s)
i==len(s)=3 → True</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def isSubsequence(s, t):
    i, j = 0, 0
    while i &lt; len(s) and j &lt; len(t):
        if s[i] == t[j]:
            i += 1                 # matched one char of s
        j += 1                     # always move through t
    return i == len(s)             # consumed all of s?</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(|t|)</strong> — one scan of <code>t</code>. <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li><code>s</code> empty → vacuously True.</li>
<li><code>s</code> longer than <code>t</code> → can't finish → False.</li>
<li>Identical strings → True.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Advancing <code>i</code> even on a mismatch.</li>
<li>Returning based on <code>j</code> instead of whether all of <code>s</code> was matched.</li>
<li>Assuming contiguous substring rather than subsequence.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li><strong>Many</strong> <code>s</code> queries against one <code>t</code> → preprocess <code>t</code> into lists of positions per character and binary-search each — O(|s| log |t|) per query.</li>
<li>Longest common subsequence ([[1143]]) generalizes the matching to DP.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[925]] · [[844]] · [[1143]]</p>
''',

# ============================================================ LC 19 — Remove Nth Node From End of List
19: '''
<h2>🧭 How to think about it</h2>
<p>Delete the n-th node counting from the end, in a single pass. The trick is a <strong>fixed gap</strong> between two pointers: move a lead pointer <code>n</code> steps ahead, then advance both together. When the lead reaches the end, the trailing pointer sits exactly on the node just before the one to remove.</p>

<h2>🐢 Brute force first</h2>
<p>Two passes: count the length L, then walk to node <code>L−n</code> and unlink. Correct and simple. The two-pointer version does it in one pass.</p>

<div class="insight">💡 <strong>Key insight:</strong> a gap of <code>n</code> between <code>lead</code> and <code>lag</code> is preserved as both advance. Start them off a <em>dummy</em> node so that even removing the head is handled uniformly; when <code>lead</code> falls off the end, <code>lag.next</code> is the target.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Create a <code>dummy</code> pointing to head; <code>lead = lag = dummy</code>.</li>
<li>Advance <code>lead</code> by <code>n+1</code> steps (so the gap spans the node before the target).</li>
<li>Advance both until <code>lead</code> is <code>None</code>.</li>
<li><code>lag.next = lag.next.next</code>; return <code>dummy.next</code>.</li>
</ol>

<h2>🎞️ Visual dry run — list 1→2→3→4→5, n = 2</h2>
<pre class="viz">dummy→1→2→3→4→5 ; move lead 3 steps: lead=3, lag=dummy
advance both: lead=4 lag=1 ; lead=5 lag=2 ; lead=None lag=3
lag.next (=4) skipped → lag.next = 5
Result: 1→2→3→5</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def removeNthFromEnd(head, n):
    dummy = ListNode(0, head)      # handles removing the head uniformly
    lead = lag = dummy
    for _ in range(n + 1):         # open a gap of n between lag and lead
        lead = lead.next
    while lead:                    # advance together
        lead = lead.next
        lag = lag.next
    lag.next = lag.next.next       # unlink the target
    return dummy.next</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(L)</strong> — one traversal. <strong>Space O(1)</strong> — a few pointers.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Removing the head (<code>n == L</code>) → the dummy makes <code>lag</code> land on dummy, so <code>dummy.next</code> updates correctly.</li>
<li>Single-node list, <code>n = 1</code> → returns empty list.</li>
<li><code>n</code> equal to length → head removed.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Advancing <code>lead</code> by <code>n</code> instead of <code>n+1</code> — you'd land <code>lag</code> on the target, not before it.</li>
<li>Not using a dummy → special-casing head removal and risking null errors.</li>
<li>Off-by-one in the gap.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Return the n-th node from the end without deleting → same gap, no unlink.</li>
<li>Find the middle ([[876]]) → a different fixed-ratio pointer setup.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[876]] · [[2095]] · [[141]]</p>
''',

# ============================================================ LC 876 — Middle of the Linked List
876: '''
<h2>🧭 How to think about it</h2>
<p>Find the middle node in one pass, without knowing the length up front. Send a <strong>fast pointer at double speed</strong>: when it reaches the end, the slow pointer — moving half as fast — is exactly at the middle.</p>

<h2>🐢 Brute force first</h2>
<p>Count the length, then walk to index <code>length // 2</code> — two passes. Fast/slow does it in one.</p>

<div class="insight">💡 <strong>Key insight:</strong> if <code>fast</code> covers two nodes for every one that <code>slow</code> covers, then when <code>fast</code> has gone the full length, <code>slow</code> has gone halfway. The loop condition <code>fast and fast.next</code> makes <code>slow</code> land on the <em>second</em> middle for even lengths (as the problem asks).</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>slow = fast = head</code>.</li>
<li>While <code>fast</code> and <code>fast.next</code>: <code>slow = slow.next</code>, <code>fast = fast.next.next</code>.</li>
<li>Return <code>slow</code>.</li>
</ol>

<h2>🎞️ Visual dry run — 1→2→3→4→5</h2>
<pre class="viz">slow=1 fast=1
slow=2 fast=3
slow=3 fast=5  (fast.next is None → stop)
Middle = node 3 ✓
(For 1→2→3→4→5→6, slow ends on 4 — the second middle.)</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def middleNode(head):
    slow = fast = head
    while fast and fast.next:      # fast moves two, slow one
        slow = slow.next
        fast = fast.next.next
    return slow                    # halfway when fast reached the end</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — fast traverses the whole list. <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Single node → returns it.</li>
<li>Two nodes → returns the second (the second middle).</li>
<li>Odd vs even length → the loop condition selects the intended middle.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Using <code>while fast.next and fast.next.next</code> → returns the first middle for even lengths (wrong for this problem).</li>
<li>Forgetting the <code>fast</code> null check → crash on even lengths.</li>
<li>Returning <code>slow.next</code> by mistake.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Return the <em>first</em> middle → adjust the loop condition.</li>
<li>Split the list in half (used in merge sort / reorder, [[143]]) → stop one before the middle.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[2095]] · [[19]] · [[141]]</p>
''',

# ============================================================ LC 2095 — Delete the Middle Node of a Linked List
2095: '''
<h2>🧭 How to think about it</h2>
<p>Delete the middle node (index <code>⌊n/2⌋</code>). Finding the middle is the fast/slow trick again — but to <em>delete</em> it you must stop the slow pointer <strong>one node before</strong> the middle so you can relink around it. A dummy head keeps the single-node case clean.</p>

<h2>🐢 Brute force first</h2>
<p>Count length, walk to the predecessor, unlink — two passes. Fast/slow with a trailing <code>prev</code> does it in one.</p>

<div class="insight">💡 <strong>Key insight:</strong> run <code>fast</code> two steps and <code>slow</code> one, but keep a <code>prev</code> pointer chasing <code>slow</code>. When <code>fast</code> reaches the end, <code>slow</code> is on the middle and <code>prev</code> is right before it → <code>prev.next = slow.next</code> removes the middle.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>If the list has one node, return <code>None</code>.</li>
<li><code>slow = head</code>, <code>fast = head</code>, <code>prev = None</code>.</li>
<li>While <code>fast</code> and <code>fast.next</code>: <code>prev = slow</code>; <code>slow = slow.next</code>; <code>fast = fast.next.next</code>.</li>
<li><code>prev.next = slow.next</code>; return <code>head</code>.</li>
</ol>

<h2>🎞️ Visual dry run — 1→3→4→7→1→2→6 (n=7, middle index 3 = node 7)</h2>
<pre class="viz">prev=None slow=1 fast=1
prev=1 slow=3 fast=4
prev=3 slow=4 fast=1(idx4)
prev=4 slow=7 fast=6 (fast.next None → stop)
prev.next (=7) skipped → 4→1(idx4)
Result: 1→3→4→1→2→6</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def deleteMiddle(head):
    if head.next is None:          # single node → nothing remains
        return None
    slow, fast, prev = head, head, None
    while fast and fast.next:
        prev = slow                # trail one behind slow
        slow = slow.next
        fast = fast.next.next
    prev.next = slow.next          # unlink the middle (slow)
    return head</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — one traversal. <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Single node → return <code>None</code> (handled up front).</li>
<li>Two nodes → middle is the second; <code>prev</code> = first, relinks to <code>None</code>.</li>
<li>Even vs odd length → <code>⌊n/2⌋</code> falls out of the same loop condition.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Not tracking <code>prev</code> → you find the middle but can't unlink it.</li>
<li>Forgetting the single-node guard → <code>prev</code> stays <code>None</code> and crashes.</li>
<li>Deleting the wrong middle for even lengths (verify with a small even case).</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Return the middle instead of deleting ([[876]]).</li>
<li>Delete the n-th from the end ([[19]]) — same fixed-gap family.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[876]] · [[19]] · [[141]]</p>
''',

# ============================================================ LC 844 — Backspace String Compare
844: '''
<h2>🧭 How to think about it</h2>
<p>Two strings contain <code>'#'</code> characters meaning "backspace". Do they type out equal? The clean O(1)-space way is to scan <strong>from the right</strong>: a <code>'#'</code> tells you to skip the next real character, so you can figure out each string's next "surviving" character without building the result.</p>

<h2>🐢 Brute force first</h2>
<p>Rebuild each string with a stack (push letters, pop on <code>'#'</code>), then compare — O(n) time, O(n) space. The reverse two-pointer walk drops the space to O(1).</p>

<div class="insight">💡 <strong>Key insight:</strong> walking backwards, keep a <em>skip</em> counter. Each <code>'#'</code> increases skip; each real character either is skipped (skip &gt; 0, decrement) or is the next surviving character. Advance both strings to their next survivors and compare; repeat.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Pointers <code>i</code>, <code>j</code> at the ends of <code>s</code>, <code>t</code>.</li>
<li>A helper walks a pointer left past skipped characters to the next real, surviving character.</li>
<li>Compare the two survivors; if they differ (or one runs out), decide the answer; else step both inward.</li>
</ol>

<h2>🎞️ Visual dry run — s = "ab#c", t = "ad#c"</h2>
<pre class="viz">s survivors from right: c, (b then # cancels), a → "ac"
t survivors from right: c, (d then # cancels), a → "ac"
compare c==c, a==a → equal → True</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def backspaceCompare(s, t):
    def next_valid(string, i):
        skip = 0
        while i &gt;= 0:
            if string[i] == '#':
                skip += 1; i -= 1        # a backspace to apply
            elif skip &gt; 0:
                skip -= 1; i -= 1        # this char is erased
            else:
                break                    # i is a surviving character
        return i

    i, j = len(s) - 1, len(t) - 1
    while i &gt;= 0 or j &gt;= 0:
        i = next_valid(s, i)
        j = next_valid(t, j)
        if i &gt;= 0 and j &gt;= 0:
            if s[i] != t[j]:
                return False
        elif i &gt;= 0 or j &gt;= 0:            # one has a leftover character
            return False
        i -= 1; j -= 1
    return True</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n + m)</strong> — each character visited once. <strong>Space O(1)</strong> — just counters and indices.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Backspace on an empty result (leading <code>'#'</code>) → harmless, skip counter just idles.</li>
<li>Strings that reduce to empty → equal.</li>
<li>Different surviving lengths → the "one leftover" check returns False.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Comparing lengths of the raw strings rather than the typed results.</li>
<li>Mishandling the case where one pointer is exhausted but the other still has a survivor.</li>
<li>Forgetting to decrement both pointers after a successful comparison.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Build with a stack for clarity if O(n) space is fine.</li>
<li>Multiple special commands (e.g., caps-lock) → extend the survivor logic.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[925]] · [[392]] · [[443]]</p>
''',

# ============================================================ LC 5 — Longest Palindromic Substring
5: '''
<h2>🧭 How to think about it</h2>
<p>A palindrome reads the same both ways, so it has a <strong>center</strong> and is symmetric around it. Instead of checking every substring, sit at each possible center and let two pointers <em>expand outward</em> while the characters match. There are <code>2n−1</code> centers (each character, and each gap between characters), covering odd- and even-length palindromes.</p>

<h2>🐢 Brute force first</h2>
<p>Check all O(n²) substrings, each palindrome-tested in O(n) → O(n³). Expand-around-center is O(n²) time and O(1) space; the advanced Manacher's algorithm reaches O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> every palindrome grows symmetrically from its center. For each center, push <code>left</code> and <code>right</code> apart while <code>s[left] == s[right]</code>. Track the longest span found. Two center types — <code>(i, i)</code> for odd length and <code>(i, i+1)</code> for even — cover them all.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>For each index <code>i</code>, expand around center <code>(i, i)</code> and around <code>(i, i+1)</code>.</li>
<li>Each expansion returns the palindrome's bounds; keep the longest.</li>
<li>Return the substring for those bounds.</li>
</ol>

<h2>🎞️ Visual dry run — s = "babad"</h2>
<pre class="viz">center i=1 (a): expand b[a]b → "bab" length 3
center i=2 (b): expand a[b]a → "aba" length 3
even centers give length ≤ 1 here
Longest = "bab" (or "aba"; either is accepted)</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def longestPalindrome(s):
    def expand(left, right):
        while left &gt;= 0 and right &lt; len(s) and s[left] == s[right]:
            left -= 1; right += 1
        return left + 1, right - 1        # last valid (inclusive) bounds

    start, end = 0, 0
    for i in range(len(s)):
        l1, r1 = expand(i, i)             # odd-length center
        if r1 - l1 &gt; end - start:
            start, end = l1, r1
        l2, r2 = expand(i, i + 1)         # even-length center
        if r2 - l2 &gt; end - start:
            start, end = l2, r2
    return s[start:end + 1]</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n²)</strong> — n centers, each expands up to O(n). <strong>Space O(1)</strong> — just index bookkeeping.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Empty string → returns empty.</li>
<li>All identical characters → the whole string is the palindrome.</li>
<li>No palindrome longer than 1 → any single character is returned.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Handling only odd centers → misses even-length palindromes like "abba".</li>
<li>Off-by-one when converting the expanded pointers back to inclusive bounds.</li>
<li>Comparing lengths with the wrong bound arithmetic.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Count all palindromic substrings ([[647]]) → same expansion, add up counts.</li>
<li>Manacher's algorithm → O(n), the ultimate follow-up.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[647]] · [[345]] · [[125]]</p>
''',

# ============================================================ LC 647 — Palindromic Substrings
647: '''
<h2>🧭 How to think about it</h2>
<p>Count how many substrings are palindromes. Same engine as Longest Palindromic Substring: expand around every center. The only change is that instead of tracking the longest, you <strong>count each successful expansion</strong> — every time the two pointers still match, that's one more palindrome.</p>

<h2>🐢 Brute force first</h2>
<p>Test all O(n²) substrings for palindrome-ness in O(n) each → O(n³). Expand-around-center counts them in O(n²) with O(1) space.</p>

<div class="insight">💡 <strong>Key insight:</strong> each time an expansion step succeeds (<code>s[left] == s[right]</code>), it reveals exactly one new palindrome centered there. Sum those successes across all <code>2n−1</code> centers.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>For each index <code>i</code>: expand around <code>(i, i)</code> and <code>(i, i+1)</code>.</li>
<li>Each successful match while expanding adds 1 to the count.</li>
<li>Return the total.</li>
</ol>

<h2>🎞️ Visual dry run — s = "aaa"</h2>
<pre class="viz">odd centers:  (0)→"a"; (1)→"a" then "aaa"; (2)→"a"  → 4 counts
even centers: (0,1)→"aa"; (1,2)→"aa"                → 2 counts
Total = 6 palindromic substrings</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def countSubstrings(s):
    def count_from(left, right):
        c = 0
        while left &gt;= 0 and right &lt; len(s) and s[left] == s[right]:
            c += 1                        # one more palindrome centered here
            left -= 1; right += 1
        return c

    total = 0
    for i in range(len(s)):
        total += count_from(i, i)         # odd length
        total += count_from(i, i + 1)     # even length
    return total</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n²)</strong> — n centers, each expands up to O(n). <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Single character → count 1.</li>
<li>All identical → n(n+1)/2 palindromes (every substring qualifies).</li>
<li>No repeats → exactly n (each single character).</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Counting only maximal palindromes instead of every centered one.</li>
<li>Skipping even-length centers.</li>
<li>Double-counting by mixing up the two center loops.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Return the longest instead of the count ([[5]]).</li>
<li>Count distinct palindromic substrings → needs hashing or a palindromic tree.</li>
<li>Manacher's → O(n) counting.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[5]] · [[345]] · [[125]]</p>
''',
}
