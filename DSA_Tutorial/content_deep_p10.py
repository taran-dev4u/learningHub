# -*- coding: utf-8 -*-
"""
Deep tutorials for Pattern 10: Greedy Patterns.
Masterclass 12-step structured explanations with ASCII dry runs and complexity analyses.
"""

DEEP = {
# ============================================================ LC 56: Merge Intervals
56: '''<h2>🧭 How to think about it</h2>
<p>Given an array of <code>intervals</code> where <code>intervals[i] = [start_i, end_i]</code>, merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.</p>

<p>Two intervals <code>[a, b]</code> and <code>[c, d]</code> overlap if and only if <code>b &ge; c</code> (assuming <code>a &le; c</code>). To detect overlaps easily without quadratic comparisons, we sort all intervals by their <code>start</code> times.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Comparing every interval against all others to find overlaps takes <code>O(N^2)</code> or graph connected components. Sorting intervals by their start coordinates allows us to merge them in a single linear pass in <code>O(N log N)</code> time.</p>

<div class="insight">💡 <strong>Key insight:</strong> Sort by <code>start</code>. Once sorted, if the current interval starts after the last merged interval ends (<code>curr[0] > res[-1][1]</code>), they cannot possibly overlap—append <code>curr</code> as a new interval. Otherwise, they overlap—merge them by updating the end boundary: <code>res[-1][1] = max(res[-1][1], curr[1])</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Sort <code>intervals</code> in-place by start time: <code>intervals.sort(key=lambda x: x[0])</code>.</li>
<li>Initialize <code>merged = [intervals[0]]</code>.</li>
<li>For each <code>start, end</code> in <code>intervals[1:]</code>:
  <ul>
    <li>Let <code>last_start, last_end = merged[-1]</code>.</li>
    <li>If <code>start <= last_end</code>: overlap detected! Update <code>merged[-1][1] = max(last_end, end)</code>.</li>
    <li>Else: no overlap. Append <code>[start, end]</code> to <code>merged</code>.</li>
  </ul>
</li>
<li>Return <code>merged</code>.</li>
</ol>

<h2>🎞️ Visual dry run — intervals = [[1,3],[2,6],[8,10],[15,18]]:</h2>
<pre class="viz">1. Sorted: [[1,3], [2,6], [8,10], [15,18]]
2. merged = [[1,3]]
3. Process [2,6]: 2 <= 3 (overlap!) -> merged[-1][1] = max(3, 6) = 6.
   merged is now [[1,6]]
4. Process [8,10]: 8 > 6 (no overlap) -> append [8,10].
   merged is now [[1,6], [8,10]]
5. Process [15,18]: 15 > 10 (no overlap) -> append [15,18].
   merged is now [[1,6], [8,10], [15,18]]
Output: [[1,6], [8,10], [15,18]] ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def merge(intervals: list[list[int]]) -> list[list[int]]:
    """
    Merges overlapping intervals by sorting by start time.
    """
    if not intervals:
        return []
        
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
            
    return merged
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(N log N)</code> dominated by the sorting step. The linear scan takes <code>O(N)</code>.</li>
<li><strong>Space Complexity:</strong> <code>O(N)</code> to store the merged output intervals (or <code>O(log N)</code> for Python Timsort recursion stack).</li>
</ul>

<h2>🚨 Edge cases to watch out for</h2>
<ul>
<li><strong>One interval completely inside another:</strong> e.g. <code>[1, 10]</code> and <code>[2, 5]</code>. The <code>max(last_end, end)</code> correctly keeps <code>10</code>.</li>
<li><strong>Adjacent touching intervals:</strong> e.g. <code>[1, 4]</code> and <code>[4, 5]</code>. Since <code>4 <= 4</code>, they correctly merge into <code>[1, 5]</code>.</li>
</ul>''',

# ============================================================ LC 57: Insert Interval
57: '''<h2>🧭 How to think about it</h2>
<p>You are given an array of non-overlapping intervals <code>intervals</code> sorted by start time, and a <code>newInterval = [start, end]</code>. Insert <code>newInterval</code> into <code>intervals</code> such that the list is still sorted and non-overlapping (merging if necessary).</p>

<p>Because the input is already sorted, we can partition the problem into three linear phases:</p>
<ol>
  <li><strong>Left Part:</strong> Add all intervals that finish strictly before <code>newInterval</code> begins (<code>interval[1] < newInterval[0]</code>).</li>
  <li><strong>Overlap Part:</strong> Merge all intervals that overlap with <code>newInterval</code> (<code>interval[0] <= newInterval[1]</code>). Update <code>newInterval = [min(start), max(end)]</code>.</li>
  <li><strong>Right Part:</strong> Add all remaining intervals that start strictly after <code>newInterval</code> ends.</li>
</ol>

<h2>🐢 Brute force vs optimal</h2>
<p>Appending <code>newInterval</code> and calling <code>sort()</code> takes <code>O(N log N)</code>. By leveraging the existing sorted order, we achieve pure <code>O(N)</code> time in a single pass without sorting!</p>

<div class="insight">💡 <strong>Key insight:</strong> Loop through the sorted intervals. If <code>curr[1] < new[0]</code>, add <code>curr</code> to result. If <code>curr[0] > new[1]</code>, add <code>new</code> (if not added yet) and <code>curr</code>. Otherwise, they overlap—expand <code>new[0] = min(new[0], curr[0])</code> and <code>new[1] = max(new[1], curr[1])</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Initialize <code>result = []</code> and <code>i = 0, n = len(intervals)</code>.</li>
<li>Phase 1 (Before): While <code>i < n and intervals[i][1] < newInterval[0]</code>:
  <code>result.append(intervals[i]); i += 1</code>.</li>
<li>Phase 2 (Overlap): While <code>i < n and intervals[i][0] <= newInterval[1]</code>:
  <code>newInterval[0] = min(newInterval[0], intervals[i][0])</code>;
  <code>newInterval[1] = max(newInterval[1], intervals[i][1])</code>;
  <code>i += 1</code>.
  Append merged <code>newInterval</code> to <code>result</code>.</li>
<li>Phase 3 (After): While <code>i < n</code>:
  <code>result.append(intervals[i]); i += 1</code>.</li>
<li>Return <code>result</code>.</li>
</ol>

<h2>🎞️ Visual dry run — intervals = [[1,3],[6,9]], newInterval = [2,5]:</h2>
<pre class="viz">1. Phase 1: [1,3] has 3 >= 2 -> does not finish before newInterval. Phase 1 ends.
2. Phase 2 (Overlap):
   - [1,3]: 1 <= 5 (overlap!) -> newInterval = [min(2,1), max(5,3)] = [1,5]
   - [6,9]: 6 > 5 -> stops overlap!
   Append [1,5] to result: result = [[1,5]]
3. Phase 3 (After):
   Append [6,9]: result = [[1,5], [6,9]]
Output: [[1,5], [6,9]] ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def insert(intervals: list[list[int]], newInterval: list[int]) -> list[list[int]]:
    """
    Inserts and merges a new interval into sorted non-overlapping intervals in O(N) time.
    """
    res = []
    i = 0
    n = len(intervals)
    
    # 1. Add all intervals ending before newInterval starts
    while i < n and intervals[i][1] < newInterval[0]:
        res.append(intervals[i])
        i += 1
        
    # 2. Merge all overlapping intervals with newInterval
    while i < n and intervals[i][0] <= newInterval[1]:
        newInterval[0] = min(newInterval[0], intervals[i][0])
        newInterval[1] = max(newInterval[1], intervals[i][1])
        i += 1
    res.append(newInterval)
    
    # 3. Add all remaining intervals
    while i < n:
        res.append(intervals[i])
        i += 1
        
    return res
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(N)</code>. Each interval is examined and pushed to the result array exactly once.</li>
<li><strong>Space Complexity:</strong> <code>O(N)</code> to store the output array (or <code>O(1)</code> auxiliary space).</li>
</ul>

<h2>🚨 Edge cases to watch out for</h2>
<ul>
<li><code>intervals = []</code>: Returns <code>[newInterval]</code>.</li>
<li><code>newInterval</code> goes at the very beginning or very end without overlapping any interval.</li>
<li><code>newInterval</code> engulfs all existing intervals.</li>
</ul>''',

# ============================================================ LC 435: Non-overlapping Intervals
435: '''<h2>🧭 How to think about it</h2>
<p>Given an array of intervals, return the minimum number of intervals you need to remove to make the rest of the intervals non-overlapping.</p>

<p>Minimizing removals is mathematically equivalent to <strong>maximizing the number of mutually compatible intervals you keep</strong>. This is the classic <strong>Activity Selection Problem</strong>.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Dynamic programming takes <code>O(N^2)</code> (longest non-overlapping chain). Greedily sorting by <strong>end time</strong> solves this in <code>O(N log N)</code> time.</p>

<div class="insight">💡 <strong>Key insight:</strong> Always keep the interval that <strong>finishes earliest</strong>! Why? The earlier an interval finishes, the more available time is left on the timeline for subsequent intervals to fit in without conflict. If an interval overlaps with the last kept interval, it MUST be removed!</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Sort intervals by their end times: <code>intervals.sort(key=lambda x: x[1])</code>.</li>
<li>Initialize <code>removals = 0</code>, <code>prev_end = intervals[0][1]</code>.</li>
<li>For each <code>start, end</code> in <code>intervals[1:]</code>:
  <ul>
    <li>If <code>start < prev_end</code>: overlap detected! We must remove this interval to keep the earlier-ending one &rarr; <code>removals += 1</code>.</li>
    <li>Else: no overlap! We can safely keep this interval &rarr; update <code>prev_end = end</code>.</li>
  </ul>
</li>
<li>Return <code>removals</code>.</li>
</ol>

<h2>🎞️ Visual dry run — intervals = [[1,2],[2,3],[3,4],[1,3]]:</h2>
<pre class="viz">Sorted by end time:
[1,2] (end 2)
[2,3] (end 3)
[1,3] (end 3)
[3,4] (end 4)

1. Keep [1,2]. prev_end = 2.
2. [2,3]: start 2 >= 2 -> Keep! prev_end = 3.
3. [1,3]: start 1 < 3 -> Overlap! Remove! removals = 1.
4. [3,4]: start 3 >= 3 -> Keep! prev_end = 4.
Total removed = 1 ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def eraseOverlapIntervals(intervals: list[list[int]]) -> int:
    """
    Minimizes removals by greedily keeping intervals that finish earliest.
    """
    if not intervals:
        return 0
        
    # Sort by end time
    intervals.sort(key=lambda x: x[1])
    
    removals = 0
    prev_end = intervals[0][1]
    
    for start, end in intervals[1:]:
        if start < prev_end:
            removals += 1
        else:
            prev_end = end
            
    return removals
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(N log N)</code> for sorting. The linear scan is <code>O(N)</code>.</li>
<li><strong>Space Complexity:</strong> <code>O(1)</code> auxiliary space (excluding sort stack).</li>
</ul>''',

# ============================================================ LC 452: Minimum Number of Arrows to Burst Balloons
452: '''<h2>🧭 How to think about it</h2>
<p>There are spherical balloons taped to a flat wall. Each balloon is represented by a 2D integer array <code>points</code> where <code>points[i] = [x_start, x_end]</code>. An arrow shot vertically from <code>x</code> bursts all balloons with <code>x_start &le; x &le; x_end</code>. Find the minimum number of arrows that must be shot to burst all balloons.</p>

<p>Every arrow should burst as many overlapping balloons as possible. Like interval scheduling, we want to shoot our arrow at the <strong>earliest end coordinate</strong> among remaining balloons.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Sorting by <code>x_end</code> coordinates lets us greedily place an arrow at <code>x_end</code> of the first unburst balloon, guaranteeing that every balloon overlapping that coordinate is burst in <code>O(N log N)</code> time.</p>

<div class="insight">💡 <strong>Key insight:</strong> Sort by <code>x_end</code>. Shoot the first arrow at <code>points[0][1]</code>. For each subsequent balloon, if its <code>start <= arrow_pos</code>, it is already burst by the current arrow! If its <code>start > arrow_pos</code>, the current arrow cannot reach it &rarr; increment arrows by 1 and shoot a new arrow at this balloon's <code>end</code>!</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>If <code>not points</code>, return <code>0</code>.</li>
<li>Sort <code>points</code> by end coordinate: <code>points.sort(key=lambda x: x[1])</code>.</li>
<li>Initialize <code>arrows = 1</code>, <code>arrow_pos = points[0][1]</code>.</li>
<li>For each <code>start, end</code> in <code>points[1:]</code>:
  <ul>
    <li>If <code>start > arrow_pos</code>:
      <code>arrows += 1</code>; <code>arrow_pos = end</code>.</li>
  </ul>
</li>
<li>Return <code>arrows</code>.</li>
</ol>

<h2>🎞️ Visual dry run — points = [[10,16],[2,8],[1,6],[7,12]]:</h2>
<pre class="viz">Sorted by end:
[1,6]   (end 6)
[2,8]   (end 8)
[7,12]  (end 12)
[10,16] (end 16)

1. Shoot arrow 1 at pos = 6.
2. [2,8]: start 2 <= 6 -> Burst!
3. [7,12]: start 7 > 6 -> Cannot burst! Shoot arrow 2 at pos = 12. arrows = 2.
4. [10,16]: start 10 <= 12 -> Burst!
Total arrows = 2 ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def findMinArrowShots(points: list[list[int]]) -> int:
    """
    Finds minimum arrows to burst all balloons by sorting by end coordinate.
    """
    if not points:
        return 0
        
    points.sort(key=lambda x: x[1])
    arrows = 1
    arrow_pos = points[0][1]
    
    for start, end in points[1:]:
        if start > arrow_pos:
            arrows += 1
            arrow_pos = end
            
    return arrows
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(N log N)</code> for sorting.</li>
<li><strong>Space Complexity:</strong> <code>O(1)</code> auxiliary space.</li>
</ul>''',

# ============================================================ LC 55: Jump Game
55: '''<h2>🧭 How to think about it</h2>
<p>You are given an integer array <code>nums</code>. You are initially positioned at the array's first index, and each element in the array represents your maximum jump length at that position. Return <code>true</code> if you can reach the last index, or <code>false</code> otherwise.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Backtracking recursively explores all jump sizes: <code>O(2^N)</code>. Dynamic programming caches reachability in <code>O(N^2)</code>. The Greedy approach maintains the <strong>furthest reachable index</strong> in a single linear pass in <code>O(N)</code> time and <code>O(1)</code> space!</p>

<div class="insight">💡 <strong>Key insight:</strong> Maintain <code>max_reach</code>. Iterate index <code>i</code> from <code>0</code> to <code>n - 1</code>. If at any point <code>i > max_reach</code>, we have reached a position we could never have arrived at &rarr; return <code>False</code>! Otherwise, update <code>max_reach = max(max_reach, i + nums[i])</code>. If <code>max_reach >= n - 1</code>, return <code>True</code> immediately!</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Initialize <code>max_reach = 0</code>.</li>
<li>For index <code>i</code> and value <code>num</code> in <code>enumerate(nums)</code>:
  <ul>
    <li>If <code>i > max_reach</code>: return <code>False</code> (stranded!).</li>
    <li>Update <code>max_reach = max(max_reach, i + num)</code>.</li>
    <li>If <code>max_reach >= len(nums) - 1</code>: return <code>True</code>.</li>
  </ul>
</li>
<li>Return <code>True</code>.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [2,3,1,1,4]:</h2>
<pre class="viz">i=0: num=2 -> max_reach = max(0, 0+2) = 2
i=1: num=3 -> 1 <= 2 -> max_reach = max(2, 1+3) = 4 >= 4 (last index)!
Reachable! Return True ✓

Counterexample: nums = [3,2,1,0,4]:
i=0: max_reach = 3
i=1: max_reach = max(3, 1+2) = 3
i=2: max_reach = max(3, 2+1) = 3
i=3: max_reach = max(3, 3+0) = 3
i=4: 4 > 3! Stranded at index 3 (zero jump)! Return False ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def canJump(nums: list[int]) -> bool:
    """
    Determines if last index is reachable by tracking furthest boundary greedily.
    """
    max_reach = 0
    target = len(nums) - 1
    
    for i, jump in enumerate(nums):
        if i > max_reach:
            return False
        max_reach = max(max_reach, i + jump)
        if max_reach >= target:
            return True
            
    return True
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(N)</code>. Single pass over the array.</li>
<li><strong>Space Complexity:</strong> <code>O(1)</code>. Only one integer tracker variable.</li>
</ul>''',

# ============================================================ LC 45: Jump Game II
45: '''<h2>🧭 How to think about it</h2>
<p>You are given a 0-indexed array of integers <code>nums</code> of length <code>n</code>. You are initially positioned at <code>nums[0]</code>. Each element represents your maximum jump length. Return the <strong>minimum number of jumps</strong> to reach <code>nums[n - 1]</code> (guaranteed reachable).</p>

<h2>🐢 Brute force vs optimal</h2>
<p>DP takes <code>O(N^2)</code>. By viewing this problem through <strong>BFS levels</strong>, we can find the minimum jumps in pure <code>O(N)</code> time. Every jump moves us from the current level to the next level of reachable indices.</p>

<div class="insight">💡 <strong>Key insight:</strong> Maintain <code>cur_end</code> (the furthest boundary reachable with the current number of jumps) and <code>farthest</code> (the furthest index reachable by jumping from any point seen so far). When our scan reaches <code>cur_end</code>, we MUST jump! Increment <code>jumps += 1</code> and set <code>cur_end = farthest</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>If <code>len(nums) <= 1</code>, return <code>0</code>.</li>
<li>Initialize <code>jumps = 0</code>, <code>cur_end = 0</code>, <code>farthest = 0</code>.</li>
<li>Iterate <code>i</code> from <code>0</code> to <code>len(nums) - 2</code>:
  <ul>
    <li>Update <code>farthest = max(farthest, i + nums[i])</code>.</li>
    <li>If <code>i == cur_end</code>:
      <ul>
        <li><code>jumps += 1</code></li>
        <li><code>cur_end = farthest</code></li>
        <li>If <code>cur_end >= len(nums) - 1</code>, break early!</li>
      </ul>
    </li>
  </ul>
</li>
<li>Return <code>jumps</code>.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [2,3,1,1,4]:</h2>
<pre class="viz">i=0: num=2. farthest = max(0, 0+2) = 2.
     i == cur_end (0==0) -> Must jump! jumps = 1, cur_end = 2.

i=1: num=3. farthest = max(2, 1+3) = 4.
i=2: num=1. farthest = max(4, 2+1) = 4.
     i == cur_end (2==2) -> Must jump! jumps = 2, cur_end = 4.
cur_end >= 4 (target reached!). Stop!
Result = 2 jumps ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def jump(nums: list[int]) -> int:
    """
    Finds minimum jumps to reach end using level-by-level greedy BFS.
    """
    n = len(nums)
    if n <= 1:
        return 0
        
    jumps = 0
    cur_end = 0
    farthest = 0
    
    # We do not need to process the last element (n - 1)
    for i in range(n - 1):
        farthest = max(farthest, i + nums[i])
        if i == cur_end:
            jumps += 1
            cur_end = farthest
            if cur_end >= n - 1:
                break
                
    return jumps
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(N)</code>. Single linear scan.</li>
<li><strong>Space Complexity:</strong> <code>O(1)</code>. Constant extra space.</li>
</ul>''',

# ============================================================ LC 121: Best Time to Buy and Sell Stock
121: '''<h2>🧭 How to think about it</h2>
<p>You are given an array <code>prices</code> where <code>prices[i]</code> is the price of a given stock on the <code>i</code>-th day. You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock. Return the maximum profit you can achieve.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Testing all pairs of buy/sell days takes <code>O(N^2)</code>. Greedily tracking the lowest price seen so far allows computing maximum profit in a single linear pass in <code>O(N)</code> time and <code>O(1)</code> space.</p>

<div class="insight">💡 <strong>Key insight:</strong> If you sell on day <code>i</code>, your optimal buy day is simply the day with the minimum stock price among days <code>0</code> through <code>i - 1</code>! Maintain <code>min_price</code> and update <code>max_profit = max(max_profit, price - min_price)</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Initialize <code>min_price = float('inf')</code> and <code>max_profit = 0</code>.</li>
<li>For each <code>price</code> in <code>prices</code>:
  <ul>
    <li>Update <code>min_price = min(min_price, price)</code>.</li>
    <li>Update <code>max_profit = max(max_profit, price - min_price)</code>.</li>
  </ul>
</li>
<li>Return <code>max_profit</code>.</li>
</ol>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def maxProfit(prices: list[int]) -> int:
    """
    Finds maximum single-transaction stock profit in O(N) time and O(1) space.
    """
    min_price = float('inf')
    max_profit = 0
    
    for price in prices:
        if price < min_price:
            min_price = price
        elif price - min_price > max_profit:
            max_profit = price - min_price
            
    return max_profit
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(N)</code>.</li>
<li><strong>Space Complexity:</strong> <code>O(1)</code>.</li>
</ul>''',

# ============================================================ LC 122: Best Time to Buy and Sell Stock II
122: '''<h2>🧭 How to think about it</h2>
<p>You are given an integer array <code>prices</code> where <code>prices[i]</code> is the price of a given stock on the <code>i</code>-th day. On each day, you may decide to buy and/or sell the stock. You can only hold at most one share of the stock at any time. Find and return the maximum profit you can achieve.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Because you can make unlimited transactions, you can capture **every single price increase** from day to day!
If prices are <code>[1, 5, 8]</code>:
- Buying at 1 and selling at 8 gives profit: <code>8 - 1 = 7</code>.
- Capturing daily gains: <code>(5 - 1) + (8 - 5) = 4 + 3 = 7</code>!
The sum of all upward slopes equals the total gain from valley to peak!</p>

<div class="insight">💡 <strong>Key insight:</strong> Whenever <code>prices[i] > prices[i - 1]</code>, greedily add <code>prices[i] - prices[i - 1]</code> to profit! If tomorrow is higher than today, buy today and sell tomorrow.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def maxProfit(prices: list[int]) -> int:
    """
    Captures all positive price deltas across consecutive trading days.
    """
    profit = 0
    for i in range(1, len(prices)):
        if prices[i] > prices[i - 1]:
            profit += prices[i] - prices[i - 1]
    return profit
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(N)</code>.</li>
<li><strong>Space Complexity:</strong> <code>O(1)</code>.</li>
</ul>''',

# ============================================================ LC 134: Gas Station
134: '''<h2>🧭 How to think about it</h2>
<p>There are <code>n</code> gas stations along a circular route, where the amount of gas at the <code>i</code>-th station is <code>gas[i]</code>. It costs <code>cost[i]</code> of gas to travel from the <code>i</code>-th station to its next <code>(i + 1)</code>-th station. You begin the journey with an empty tank at one of the gas stations. Return the starting gas station's index if you can travel around the circuit once in the clockwise direction, otherwise return <code>-1</code>. If there exists a solution, it is guaranteed to be unique.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Simulating every possible starting station takes <code>O(N^2)</code>. The Greedy approach solves this in <code>O(N)</code> time using two core mathematical principles:</p>
<ol>
  <li>If <code>sum(gas) < sum(cost)</code>, the total gas in the system is insufficient to complete the circuit &rarr; return <code>-1</code> immediately.</li>
  <li>If <code>sum(gas) >= sum(cost)</code>, a valid starting station is <strong>guaranteed to exist</strong>! Furthermore, if starting at station <code>A</code> fails at station <code>B</code>, no station between <code>A</code> and <code>B</code> could possibly be the start! The next candidate must be <code>B + 1</code>.</li>
</ol>

<div class="insight">💡 <strong>Key insight:</strong> Maintain <code>total_tank</code> and <code>curr_tank</code>. Iterate <code>i</code> from <code>0</code> to <code>n - 1</code>. Add <code>gas[i] - cost[i]</code> to both. If <code>curr_tank < 0</code>, we cannot reach station <code>i + 1</code> from our current start &rarr; reset <code>start = i + 1</code> and <code>curr_tank = 0</code>!</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>If <code>sum(gas) < sum(cost)</code>, return <code>-1</code>.</li>
<li>Initialize <code>start = 0</code>, <code>curr_tank = 0</code>.</li>
<li>For <code>i</code> in range <code>len(gas)</code>:
  <ul>
    <li><code>curr_tank += gas[i] - cost[i]</code></li>
    <li>If <code>curr_tank < 0</code>:
      <code>start = i + 1</code>; <code>curr_tank = 0</code>.</li>
  </ul>
</li>
<li>Return <code>start</code>.</li>
</ol>

<h2>🎞️ Visual dry run — gas = [1,2,3,4,5], cost = [3,4,5,1,2]:</h2>
<pre class="viz">sum(gas) = 15, sum(cost) = 15. sum(gas) >= sum(cost) -> Solution exists!

i=0: net = 1 - 3 = -2. curr_tank = -2 < 0 -> start = 1, curr_tank = 0.
i=1: net = 2 - 4 = -2. curr_tank = -2 < 0 -> start = 2, curr_tank = 0.
i=2: net = 3 - 5 = -2. curr_tank = -2 < 0 -> start = 3, curr_tank = 0.
i=3: net = 4 - 1 = +3. curr_tank = 3 >= 0.
i=4: net = 5 - 2 = +3. curr_tank = 6 >= 0.
Loop finishes!
Valid start station: 3 (gas[3]=4, cost[3]=1) ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def canCompleteCircuit(gas: list[int], cost: list[int]) -> int:
    """
    Finds unique starting gas station to complete circuit in O(N) time and O(1) space.
    """
    if sum(gas) < sum(cost):
        return -1
        
    start = 0
    curr_tank = 0
    
    for i in range(len(gas)):
        curr_tank += gas[i] - cost[i]
        if curr_tank < 0:
            start = i + 1
            curr_tank = 0
            
    return start
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(N)</code>. Single pass to sum and single pass to find the starting index.</li>
<li><strong>Space Complexity:</strong> <code>O(1)</code>.</li>
</ul>''',

# ============================================================ LC 621: Task Scheduler
621: '''<h2>🧭 How to think about it</h2>
<p>Given a characters array <code>tasks</code> representing the tasks a CPU needs to do, where each letter represents a different task. Tasks could be done in any order. Each task is done in one unit of time. For each unit of time, the CPU could complete either one task or be idle. However, there is a non-negative integer <code>n</code> that represents the cooldown period between two <strong>same tasks</strong> (must be at least <code>n</code> intervals apart). Return the least number of units of times that the CPU will take to finish all the given tasks.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Simulating cooling queues with a max-heap takes <code>O(T log 26)</code>. The problem can be solved mathematically in <code>O(T)</code> time by analyzing the <strong>most frequent task</strong>!</p>

<div class="insight">💡 <strong>Key insight:</strong> The most frequent task dictates the minimum frame structure.
<br><br>
Let <code>max_freq</code> be the frequency of the most common task, and <code>count_max</code> be the number of tasks having this maximum frequency.
These tasks create <code>(max_freq - 1)</code> chunks, each requiring <code>(n + 1)</code> slots, plus <code>count_max</code> tasks in the final chunk:
$$\text{min\\_time} = (\text{max\\_freq} - 1) \times (n + 1) + \text{count\\_max}$$
If there are enough other tasks to fill all idle slots without needing any idling, the total time is simply <code>len(tasks)</code>!
Therefore, answer = <code>max(len(tasks), (max_freq - 1) * (n + 1) + count_max)</code>.</div>

<h2>🎞️ Visual dry run — tasks = ["A","A","A","B","B","B"], n = 2:</h2>
<pre class="viz">max_freq = 3 (A and B both appear 3 times). count_max = 2 (A and B).
Frame layout:
Chunk 1: A B (idle) -> length n + 1 = 3
Chunk 2: A B (idle) -> length n + 1 = 3
Last:    A B        -> length count_max = 2

Total slots = (3 - 1) * (2 + 1) + 2 = 2 * 3 + 2 = 8 slots:
[A, B, idle, A, B, idle, A, B]
Output: 8 ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">from collections import Counter

def leastInterval(tasks: list[str], n: int) -> int:
    """
    Computes minimum CPU intervals to execute tasks with cooling period n.
    """
    counts = Counter(tasks)
    max_freq = max(counts.values())
    count_max = sum(1 for val in counts.values() if val == max_freq)
    
    empty_slots_time = (max_freq - 1) * (n + 1) + count_max
    return max(len(tasks), empty_slots_time)
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(T)</code> where <code>T = len(tasks)</code> to count frequencies. The alphabet size is at most 26.</li>
<li><strong>Space Complexity:</strong> <code>O(1)</code> space (at most 26 uppercase letters in hash map).</li>
</ul>''',

# ============================================================ LC 763: Partition Labels
763: '''<h2>🧭 How to think about it</h2>
<p>You are given a string <code>s</code>. We want to partition the string into as many parts as possible so that each letter appears in at most one part. Return a list of integers representing the size of these parts.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>In a pre-pass, find the <strong>last occurrence index</strong> of each character. Then scan the string from left to right, maintaining an expanding boundary <code>end</code>. When our scan index reaches <code>end</code>, every character encountered so far will never appear again &rarr; close the partition!</p>

<div class="insight">💡 <strong>Key insight:</strong>
1. <code>last = {c: i for i, c in enumerate(s)}</code>.
2. Maintain <code>start = 0</code> and <code>end = 0</code>.
3. For index <code>i, c</code>: update <code>end = max(end, last[c])</code>.
4. If <code>i == end</code>: partition complete! Size is <code>end - start + 1</code>. Update <code>start = i + 1</code>.</div>

<h2>🎞️ Visual dry run — s = "ababcbacadefegdehijhklij":</h2>
<pre class="viz">Chars in first block: 'a', 'b', 'c'.
Last index of 'a' is 8, 'b' is 5, 'c' is 7 -> max end = 8.
At index 8: i == end (8==8)!
Partition 1 size = 8 - 0 + 1 = 9 ("ababcbaca"). start = 9.

Next block: 'd', 'e', 'f', 'g'.
Last of 'd' is 14, 'e' is 15 -> max end = 15.
At index 15: i == end (15==15)!
Partition 2 size = 15 - 9 + 1 = 7 ("defegde"). start = 16.

Final block: 'h'..'j'.
Partition 3 size = 8 ("hijhklij").
Output: [9, 7, 8] ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def partitionLabels(s: str) -> list[int]:
    """
    Partitions string such that each letter appears in at most one partition.
    """
    last = {c: i for i, c in enumerate(s)}
    res = []
    start = 0
    end = 0
    
    for i, c in enumerate(s):
        end = max(end, last[c])
        if i == end:
            res.append(end - start + 1)
            start = i + 1
            
    return res
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(N)</code>. Two linear passes over string.</li>
<li><strong>Space Complexity:</strong> <code>O(1)</code> space (at most 26 alphabet characters in hash map).</li>
</ul>''',

# ============================================================ LC 135: Candy
135: '''<h2>🧭 How to think about it</h2>
<p>There are <code>n</code> children standing in a line. Each child is assigned a rating value given in the integer array <code>ratings</code>. You are giving candies to these children subjected to the following requirements:
<ol>
  <li>Each child must have at least one candy.</li>
  <li>Children with a higher rating get more candies than their neighbors.</li>
</ol>
Return the minimum number of candies you need to have to distribute the candies to the children.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Each child has two neighbors: left neighbor and right neighbor. A two-pass greedy strategy satisfies both constraints independently:</p>
<ol>
  <li><strong>Left-to-Right Pass:</strong> If <code>ratings[i] > ratings[i - 1]</code>, child <code>i</code> must have more candies than child <code>i - 1</code>: <code>candies[i] = candies[i - 1] + 1</code>.</li>
  <li><strong>Right-to-Left Pass:</strong> If <code>ratings[i] > ratings[i + 1]</code>, child <code>i</code> must also have more candies than child <code>i + 1</code>: <code>candies[i] = max(candies[i], candies[i + 1] + 1)</code>.</li>
</ol>

<div class="insight">💡 <strong>Key insight:</strong> Two passes guarantee that both local conditions (left-neighbor and right-neighbor) are simultaneously satisfied while using the minimum possible candies.</div>

<h2>🎞️ Visual dry run — ratings = [1, 0, 2]:</h2>
<pre class="viz">1. Initialize: candies = [1, 1, 1]
2. Left-to-right:
   i=1: ratings[1]=0 <= ratings[0]=1 -> candies[1] stays 1
   i=2: ratings[2]=2 > ratings[1]=0 -> candies[2] = candies[1] + 1 = 2
   candies after L-to-R: [1, 1, 2]
3. Right-to-left:
   i=1: ratings[1]=0 <= ratings[2]=2 -> stays 1
   i=0: ratings[0]=1 > ratings[1]=0 -> candies[0] = max(1, candies[1] + 1) = 2!
   candies after R-to-L: [2, 1, 2]
Total candies = 2 + 1 + 2 = 5 ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def candy(ratings: list[int]) -> int:
    """
    Distributes minimum candies satisfying neighbor rating constraints via two passes.
    """
    n = len(ratings)
    candies = [1] * n
    
    # Left-to-right pass
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            candies[i] = candies[i - 1] + 1
            
    # Right-to-left pass
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i + 1]:
            candies[i] = max(candies[i], candies[i + 1] + 1)
            
    return sum(candies)
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(N)</code>. Two linear passes.</li>
<li><strong>Space Complexity:</strong> <code>O(N)</code> for the candies array.</li>
</ul>''',

# ============================================================ LC 678: Valid Parenthesis String
678: '''<h2>🧭 How to think about it</h2>
<p>Given a string <code>s</code> containing only three types of characters: <code>'('</code>, <code>')'</code>, and <code>'*'</code>, return <code>true</code> if <code>s</code> is valid. An <code>'*'</code> could be treated as a single right parenthesis <code>')'</code> or a single left parenthesis <code>'('</code> or an empty string <code>""</code>.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Because each <code>'*'</code> has 3 choices, branching recursion takes <code>O(3^N)</code>. Dynamic programming takes <code>O(N^2)</code>. The Greedy approach tracks the <strong>range of possible open parentheses count</strong> <code>[cmin, cmax]</code> in <code>O(N)</code> time and <code>O(1)</code> space!</p>

<div class="insight">💡 <strong>Key insight:</strong> Maintain <code>cmin</code> (minimum possible unclosed open parentheses) and <code>cmax</code> (maximum possible unclosed open parentheses):
<ul>
  <li><code>'('</code>: <code>cmin += 1</code>, <code>cmax += 1</code>.</li>
  <li><code>')'</code>: <code>cmin -= 1</code>, <code>cmax -= 1</code>.</li>
  <li><code>'*'</code>: Can act as <code>')'</code> (decrement), <code>'('</code> (increment), or <code>""</code> (unchanged) &rarr; <code>cmin -= 1</code>, <code>cmax += 1</code>.</li>
</ul>
If <code>cmax < 0</code>, we have more <code>')'</code> than could ever be matched &rarr; return <code>False</code>.
Clamp <code>cmin = max(cmin, 0)</code> (an <code>'*'</code> never forces open count below 0).
At the end, return <code>cmin == 0</code>!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def checkValidString(s: str) -> bool:
    """
    Validates parenthesis string with wildcards by tracking open count range [cmin, cmax].
    """
    cmin = 0  # Min possible open brackets
    cmax = 0  # Max possible open brackets
    
    for ch in s:
        if ch == '(':
            cmin += 1
            cmax += 1
        elif ch == ')':
            cmin -= 1
            cmax -= 1
        else:  # ch == '*'
            cmin -= 1
            cmax += 1
            
        if cmax < 0:
            return False  # Too many closing parentheses
        cmin = max(cmin, 0)
        
    return cmin == 0
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(N)</code>. Single pass.</li>
<li><strong>Space Complexity:</strong> <code>O(1)</code>. Two integer counters.</li>
</ul>''',

}
