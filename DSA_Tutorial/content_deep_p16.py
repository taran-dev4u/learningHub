# -*- coding: utf-8 -*-
"""
Deep tutorials for Pattern 16: Segment Tree & Fenwick Tree Patterns.
Masterclass 12-step structured explanations with ASCII dry runs and complexity analyses.
"""

DEEP = {
218: '''<h2>🧭 How to think about it</h2>
<p>A city's skyline is the outer contour of the silhouette formed by all the buildings. Given <code>buildings = [left, right, height]</code>, output the key points that characterize the skyline.</p>

<p><strong>The Event-Driven Line Sweep Pattern:</strong>
Every building creates two discrete events:
1. <strong>Start of building at $x = left$:</strong> pushes height $h$ into active buildings.
2. <strong>End of building at $x = right$:</strong> removes height $h$ from active buildings.</p>

<p>Sort all event boundaries along the x-axis:
- For equal $x$ coordinates:
  - If both are starts: higher building comes first (process height descending).
  - If both are ends: lower building comes first (process height ascending).
  - If one is start and one is end: start comes first!</p>
<p>Maintain a <strong>Max-Heap of active heights</strong> (with lazy deletion).
At each event $x$:
- If current max height changes from previous max height:
  $$(x, \\; \text{new\\_max\\_height})$$
  is a critical key point on the skyline!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Evaluating height at every integer coordinate takes $O(W \\times N)$ where $W$ is width. Line sweep with max-heap evaluates in $O(N \\log N)$ time and $O(N)$ space.</p>

<div class="insight">💡 <strong>Key insight:</strong> Sweep vertical line left to right. Maintain active building heights in a Max-Heap with lazy deletion. Whenever the maximum height changes, record a keypoint $(x, max\\_h)$!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">import heapq
from collections import defaultdict

def getSkyline(buildings: list[list[int]]) -> list[list[int]]:
    # Events: (x, -height) for start, (x, height) for end
    events = []
    for l, r, h in buildings:
        events.append((l, -h, r)) # start event (stores end time r)
        events.append((r, 0, 0))   # end boundary trigger
        
    events.sort()
    
    # max_heap stores (-height, end_x)
    max_heap = [(0, float('inf'))]
    res = []
    prev_max_h = 0
    
    for x, neg_h, r in events:
        if neg_h < 0:
            heapq.heappush(max_heap, (neg_h, r))
            
        # Lazy garbage collection: pop buildings whose right boundary <= current x
        while max_heap and max_heap[0][1] <= x:
            heapq.heappop(max_heap)
            
        curr_max_h = -max_heap[0][0]
        if curr_max_h != prev_max_h:
            res.append([x, curr_max_h])
            prev_max_h = curr_max_h
            
    return res
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(N \\log N)$ — Sorting events and heap operations.<br>
<strong>Space:</strong> $O(N)$ — Events list and max heap.</p>
''',
307: '''<h2>🧭 How to think about it</h2>
<p>Given an integer array <code>nums</code>, handle multiple queries of the following types:
1. <code>update(index, val)</code>: Update the value of <code>nums[index]</code>.
2. <code>sumRange(left, right)</code>: Return the sum of elements between $left$ and $right$ inclusive.</p>

<p><strong>Binary Indexed Tree (Fenwick Tree) / Segment Tree:</strong>
- A plain array has $O(1)$ update but $O(N)$ query.
- A prefix sum array has $O(1)$ query but $O(N)$ update.
- A <strong>Fenwick Tree (BIT)</strong> or <strong>Segment Tree</strong> balances both operations to <strong>$O(\\log N)$ time</strong>!</p>

<p><strong>Fenwick Tree Mechanics:</strong>
Using 1-based indexing:
- <code>add(i, delta)</code>: Add $delta$ to index $i$, then advance $i += (i \\;\\&\\; (-i))$ (adding lowest set bit).
- <code>query(i)</code>: Accumulate sum at index $i$, then step $i -= (i \\;\\&\\; (-i))$ (clearing lowest set bit).
- <code>sumRange(l, r) = query(r + 1) - query(l)</code>.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Fenwick tree achieves $O(\\log N)$ updates and queries in strictly $O(N)$ memory with zero tree node pointers.</p>

<div class="insight">💡 <strong>Key insight:</strong> Fenwick tree: <code>i += (i & -i)</code> for point updates, <code>i -= (i & -i)</code> for prefix sums. Both execute in $O(\\log N)$!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">class NumArray:
    def __init__(self, nums: list[int]):
        self.n = len(nums)
        self.nums = nums[:]
        self.bit = [0] * (self.n + 1)
        for i, val in enumerate(nums):
            self._add(i + 1, val)

    def _add(self, i: int, delta: int):
        while i <= self.n:
            self.bit[i] += delta
            i += i & (-i)

    def _query(self, i: int) -> int:
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & (-i)
        return s

    def update(self, index: int, val: int) -> None:
        delta = val - self.nums[index]
        self.nums[index] = val
        self._add(index + 1, delta)

    def sumRange(self, left: int, right: int) -> int:
        return self._query(right + 1) - self._query(left)
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(\\log N)$ for both <code>update</code> and <code>sumRange</code>. $O(N \\log N)$ (or $O(N)$) build.<br>
<strong>Space:</strong> $O(N)$ — 1D Fenwick tree array.</p>
''',
308: '''<h2>🧭 How to think about it</h2>
<p>Given a 2D matrix <code>matrix</code>, handle multiple queries of updating a cell $(row, col)$ and retrieving the sum of elements inside a submatrix defined by $[row1, col1]$ to $[row2, col2]$.</p>

<p><strong>2D Fenwick Tree (Binary Indexed Tree):</strong>
Extend the 1D Fenwick tree to two dimensions:
- <code>bit[m + 1][n + 1]</code>
- <code>update(r, c, delta)</code>: Nested loops running $r += (r \\;\\&\\; (-r))$ and $c += (c \\;\\&\\; (-c))$.
- <code>query(r, c)</code>: Returns sum in rectangle $[1, 1]$ to $[r, c]$.
- Submatrix sum by 2D Inclusion-Exclusion:
  $$\text{Sum} = Q(r_2, c_2) - Q(r_1 - 1, c_2) - Q(r_2, c_1 - 1) + Q(r_1 - 1, c_1 - 1)$$</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Scanning submatrix takes $O(m \\times n)$. 2D Fenwick Tree updates and queries in strictly $O(\\log m \\times \\log n)$ time!</p>

<div class="insight">💡 <strong>Key insight:</strong> 2D Fenwick tree: nested $(r \\;\\&\\; -r)$ and $(c \\;\\&\\; -c)$ loops. Inclusion-exclusion evaluates 2D range sum in $O(\\log m \\log n)$.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">class NumMatrix:
    def __init__(self, matrix: list[list[int]]):
        if not matrix or not matrix[0]:
            return
        self.m, self.n = len(matrix), len(matrix[0])
        self.matrix = [[0] * self.n for _ in range(self.m)]
        self.bit = [[0] * (self.n + 1) for _ in range(self.m + 1)]
        
        for r in range(self.m):
            for c in range(self.n):
                self.update(r, c, matrix[r][c])

    def update(self, row: int, col: int, val: int) -> None:
        delta = val - self.matrix[row][col]
        self.matrix[row][col] = val
        r = row + 1
        while r <= self.m:
            c = col + 1
            while c <= self.n:
                self.bit[r][c] += delta
                c += c & (-c)
            r += r & (-r)

    def _query(self, row: int, col: int) -> int:
        s = 0
        r = row
        while r > 0:
            c = col
            while c > 0:
                s += self.bit[r][c]
                c -= c & (-c)
            r -= r & (-r)
        return s

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        return (self._query(row2 + 1, col2 + 1)
              - self._query(row1, col2 + 1)
              - self._query(row2 + 1, col1)
              + self._query(row1, col1))
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(\\log m \\times \\log n)$ for <code>update</code> and <code>sumRegion</code>.<br>
<strong>Space:</strong> $O(m \\times n)$ — 2D Fenwick tree array.</p>
''',
699: '''<h2>🧭 How to think about it</h2>
<p>There are several squares being dropped onto an X-axis. Each square is given by <code>positions[i] = [left, side_length]</code>. When a square falls, it drops until it lands on the top edge of another square or on the X-axis. Return a list of heights after each square falls.</p>

<p>For each newly dropped square with interval $[left, left + side)$:
The landing height is:
$$h_{land} = side + \\max_{j < i, \\; [l_j, r_j) \text{ overlaps } [l, r)} height[j]$$</p>

<h2>🐢 Brute force vs optimal</h2>
<p>With $N \\le 1000$, checking previously dropped squares takes $O(N)$ per square, totaling $O(N^2)$ time. For $N = 10^5$, a Segment Tree with Lazy Propagation and Coordinate Compression solves it in $O(N \\log N)$ time.</p>

<div class="insight">💡 <strong>Key insight:</strong> For current square $[l, r)$, find maximum height of all overlapping previous intervals, add $side$, and record. $O(N^2)$ interval check is optimal and clean for $N=1000$.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def fallingSquares(positions: list[list[int]]) -> list[int]:
    intervals = [] # stores (left, right, height)
    res = []
    max_h = 0
    
    for left, side in positions:
        right = left + side
        base_h = 0
        # Check all previous intervals for overlap
        for prev_l, prev_r, prev_h in intervals:
            # Overlap condition: max(left, prev_l) < min(right, prev_r)
            if left < prev_r and right > prev_l:
                base_h = max(base_h, prev_h)
                
        curr_h = base_h + side
        intervals.append((left, right, curr_h))
        max_h = max(max_h, curr_h)
        res.append(max_h)
        
    return res
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(N^2)$ — Compares each square against previous intervals.<br>
<strong>Space:</strong> $O(N)$ — Stores active intervals and results.</p>
''',
715: '''<h2>🧭 How to think about it</h2>
<p>A Range Module is a module that tracks ranges of numbers. Design a data structure to add, query, and remove intervals in half-open intervals $[left, right)$.</p>

<p><strong>Disjoint Sorted Intervals with Binary Search:</strong>
Maintain a 1D flat list of boundary coordinates: <code>[l0, r0, l1, r1, ...]</code>.
Every pair <code>track[2*i]</code> and <code>track[2*i + 1]</code> forms a valid half-open interval $[l_i, r_i)$.
- <code>bisect_left</code> and <code>bisect_right</code> identify the exact overlapping insertion range in $O(\\log N)$ time.
- Slice replacement merges or punches holes cleanly.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Interval list with binary search provides $O(\\log N)$ query time and $O(N)$ modification time.</p>

<div class="insight">💡 <strong>Key insight:</strong> Flat boundary list with parity indexing: odd index indicates inside an active interval; even index indicates outside. Binary search determines state in $O(\\log N)$.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">import bisect

class RangeModule:
    def __init__(self):
        self.track = []

    def addRange(self, left: int, right: int) -> None:
        l = bisect.bisect_left(self.track, left)
        r = bisect.bisect_right(self.track, right)
        sub = []
        if l % 2 == 0:
            sub.append(left)
        if r % 2 == 0:
            sub.append(right)
        self.track[l:r] = sub

    def queryRange(self, left: int, right: int) -> bool:
        l = bisect.bisect_right(self.track, left)
        r = bisect.bisect_left(self.track, right)
        return l % 2 == 1 and l == r

    def removeRange(self, left: int, right: int) -> None:
        l = bisect.bisect_left(self.track, left)
        r = bisect.bisect_right(self.track, right)
        sub = []
        if l % 2 == 1:
            sub.append(left)
        if r % 2 == 1:
            sub.append(right)
        self.track[l:r] = sub
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> <code>queryRange</code>: $O(\\log N)$. <code>addRange</code>, <code>removeRange</code>: $O(N)$ array slice.<br>
<strong>Space:</strong> $O(N)$ — Boundary list.</p>
''',
729: '''<h2>🧭 How to think about it</h2>
<p>You are implementing a program to use as your calendar. We can add a new event if adding the event will not cause a <strong>double booking</strong> (two events having some non-empty intersection $[start, end)$).</p>

<p>Maintain booked events in sorted order of start times:
Use binary search (<code>bisect_right</code>) to locate where the new interval $[start, end)$ should be inserted.
Check only two neighbors:
1. The preceding interval $[prev_s, prev_e)$: must have $prev_e \\le start$.
2. The succeeding interval $[next_s, next_e)$: must have $end \\le next_s$.
If both checks pass, insert the interval and return <code>True</code>!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Linear check of all intervals takes $O(N)$. Binary search checks in $O(\\log N)$ time and inserts in $O(N)$ time.</p>

<div class="insight">💡 <strong>Key insight:</strong> Sorted intervals: binary search finds insertion index in $O(\\log N)$. Only verify non-overlap with immediate left neighbor (<code>prev_end <= start</code>) and right neighbor (<code>end <= next_start</code>).</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">import bisect

class MyCalendar:
    def __init__(self):
        self.calendar = [] # sorted list of (start, end)

    def book(self, start: int, end: int) -> bool:
        idx = bisect.bisect_right(self.calendar, (start, end))
        
        # Check left neighbor
        if idx > 0 and self.calendar[idx - 1][1] > start:
            return False
            
        # Check right neighbor
        if idx < len(self.calendar) and self.calendar[idx][0] < end:
            return False
            
        self.calendar.insert(idx, (start, end))
        return True
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(\\log N)$ search + $O(N)$ insertion.<br>
<strong>Space:</strong> $O(N)$ — Sorted calendar intervals.</p>
''',
731: '''<h2>🧭 How to think about it</h2>
<p>A triple booking happens when three events have some non-empty intersection. Implement a MyCalendarTwo class that allows events that do not cause a <strong>triple booking</strong> (double booking is allowed!).</p>

<p>Maintain two lists:
1. <code>calendar</code>: All booked single events.
2. <code>overlaps</code>: All double-booked interval intersections!</p>
<p>When booking $[start, end)$:
1. First, check if $[start, end)$ intersects with <strong>any interval in <code>overlaps</code></strong>. If yes, it would cause a triple booking! Return <code>False</code> immediately!
2. If no conflict:
   Find all intersections between $[start, end)$ and existing intervals in <code>calendar</code>, and add those intersection intervals to <code>overlaps</code>!
   Add $[start, end)$ to <code>calendar</code> and return <code>True</code>.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Explicitly tracking the overlap intersections guarantees $O(N)$ check per booking.</p>

<div class="insight">💡 <strong>Key insight:</strong> Maintain <code>overlaps</code> list. Reject if new event touches any double-booking. Otherwise, compute new pairwise overlaps with <code>calendar</code> and accept.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">class MyCalendarTwo:
    def __init__(self):
        self.calendar = []
        self.overlaps = []

    def book(self, start: int, end: int) -> bool:
        # Check against existing double-booked intervals
        for s, e in self.overlaps:
            if max(start, s) < min(end, e):
                return False # Would create triple booking!
                
        # Record new double-booked intervals
        for s, e in self.calendar:
            if max(start, s) < min(end, e):
                self.overlaps.append((max(start, s), min(end, e)))
                
        self.calendar.append((start, end))
        return True
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(N)$ per booking call where $N$ is total booked events.<br>
<strong>Space:</strong> $O(N)$ — Stores intervals and overlap segments.</p>
''',
732: '''<h2>🧭 How to think about it</h2>
<p>A $k$-booking happens when $k$ events have some non-empty intersection. Implement <code>MyCalendarThree</code> which returns the largest integer $k$ such that there exists a $k$-booking in the calendar.</p>

<p><strong>Line Sweep with Coordinate Delta Map:</strong>
Use a sorted difference map (or dictionary of boundary points):
- When an event starts at $start$: increment active events: <code>delta[start] += 1</code>.
- When an event ends at $end$: decrement active events: <code>delta[end] -= 1</code>.</p>
<p>To find the maximum concurrent overlapping events:
Iterate through all boundary timestamps in sorted order, maintaining a running sum:
$$\text{curr\\_active} += \text{delta}[t]$$
$$\text{max\\_k} = \\max(\text{max\\_k}, \\; \text{curr\\_active})$$</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Sorted coordinate delta map computes the global maximum overlap in $O(N)$ per booking.</p>

<div class="insight">💡 <strong>Key insight:</strong> Line sweep: <code>delta[start] += 1; delta[end] -= 1</code>. Sweep through sorted timestamps accumulating active events; track global max!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">from collections import defaultdict

class MyCalendarThree:
    def __init__(self):
        self.delta = defaultdict(int)

    def book(self, startTime: int, endTime: int) -> int:
        self.delta[startTime] += 1
        self.delta[endTime] -= 1
        
        curr_active = 0
        max_k = 0
        for t in sorted(self.delta.keys()):
            curr_active += self.delta[t]
            if curr_active > max_k:
                max_k = curr_active
                
        return max_k
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(N \\log N)$ per booking to sort unique timestamps.<br>
<strong>Space:</strong> $O(N)$ — Timestamp dictionary.</p>
''',
315: '''<h2>🧭 How to think about it</h2>
<p>Given an integer array <code>nums</code>, return an integer array <code>counts</code> where <code>counts[i]</code> is the number of smaller elements to the right of <code>nums[i]</code>.</p>

<p>Scan <code>nums</code> in <strong>reverse order</strong> (from right to left)!
When we are at index $i$:
Every element to the right of index $i$ has already been processed and inserted into our tracking data structure!
We need to count how many inserted elements are strictly less than $nums[i]$.</p>

<p><strong>Fenwick Tree (BIT) with Coordinate Compression:</strong>
1. Coordinate compression maps arbitrary integer values to ranked indices $1 \\dots M$ ($M \\le N$).
2. For each number $x$ from right to left:
   - Query prefix sum in Fenwick tree up to rank $rank(x) - 1$:
     <code>count = query(rank - 1)</code>
   - Insert $x$ into Fenwick tree:
     <code>add(rank, 1)</code></p>

<h2>🐢 Brute force vs optimal</h2>
<p>Comparing every pair takes $O(N^2)$ time. Fenwick tree with coordinate compression evaluates in $O(N \\log N)$ time and $O(N)$ space.</p>

<div class="insight">💡 <strong>Key insight:</strong> Traverse right-to-left. Query Fenwick tree for <code>query(rank - 1)</code>, then <code>add(rank, 1)</code>. Executes in $O(N \\log N)$ time!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def countSmaller(nums: list[int]) -> list[int]:
    # Coordinate compression
    ranks = {val: i + 1 for i, val in enumerate(sorted(set(nums)))}
    m = len(ranks)
    bit = [0] * (m + 1)
    
    def add(i, delta):
        while i <= m:
            bit[i] += delta
            i += i & (-i)
            
    def query(i):
        s = 0
        while i > 0:
            s += bit[i]
            i -= i & (-i)
        return s
        
    res = []
    # Traverse from right to left
    for x in reversed(nums):
        r = ranks[x]
        res.append(query(r - 1))
        add(r, 1)
        
    return res[::-1]
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(N \\log N)$ — Sorting for coordinate compression + $N$ Fenwick queries.<br>
<strong>Space:</strong> $O(N)$ — Fenwick tree array and ranks map.</p>
''',
327: '''<h2>🧭 How to think about it</h2>
<p>Given an integer array <code>nums</code> and two integers <code>lower</code> and <code>upper</code>, return the number of range sums that lie in <code>[lower, upper]</code> inclusive.</p>

<p>Let $prefix[i] = \\sum_{k=0}^{i-1} nums[k]$.
A subsegment sum $nums[i \\dots j] = prefix[j + 1] - prefix[i]$.
We need:
$$lower \\le prefix[j + 1] - prefix[i] \\le upper$$
Rearranging for $prefix[i]$:
$$prefix[j + 1] - upper \\le prefix[i] \\le prefix[j + 1] - lower$$</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Merge sort divide-and-conquer on prefix sums solves this in $O(N \\log N)$ time!</p>

<div class="insight">💡 <strong>Key insight:</strong> Modified merge sort on prefix sums: for each element in right half, two pointers find the valid window in sorted left half in $O(N)$ per merge step!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def countRangeSum(nums: list[int], lower: int, upper: int) -> int:
    prefix = [0]
    for x in nums:
        prefix.append(prefix[-1] + x)
        
    def merge_sort(l, r):
        if l >= r:
            return 0
        mid = (l + r) // 2
        count = merge_sort(l, mid) + merge_sort(mid + 1, r)
        
        # Count pairs across left and right halves
        j = k = mid + 1
        for i in range(l, mid + 1):
            while k <= r and prefix[k] - prefix[i] < lower:
                k += 1
            while j <= r and prefix[j] - prefix[i] <= upper:
                j += 1
            count += j - k
            
        # Merge sorted halves
        prefix[l:r + 1] = sorted(prefix[l:r + 1])
        return count
        
    return merge_sort(0, len(prefix) - 1)
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(N \\log N)$ — Divide and conquer with linear two-pointer range checks.<br>
<strong>Space:</strong> $O(N)$ — Prefix sum buffer and recursion stack.</p>
''',
493: '''<h2>🧭 How to think about it</h2>
<p>Given an integer array <code>nums</code>, return the number of <strong>reverse pairs</strong> in the array. A reverse pair is a pair $(i, j)$ where $0 \\le i < j < len(nums)$ and $nums[i] > 2 \\times nums[j]$.</p>

<p>This is a variation of counting inversions!
Use <strong>Merge Sort Divide-and-Conquer</strong>:
When merging two sorted halves $nums[l \\dots mid]$ and $nums[mid+1 \\dots r]$:
Both halves are already sorted!
For each element $nums[i]$ in the left half, advance pointer $j$ in the right half while:
$$nums[i] > 2 \\times nums[j]$$
Because $nums[i]$ is increasing, pointer $j$ only moves forward (two pointers in $O(N)$)!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Nested loops take $O(N^2)$. Merge sort divide-and-conquer counts all reverse pairs in $O(N \\log N)$ time.</p>

<div class="insight">💡 <strong>Key insight:</strong> Merge sort: count pairs before merging. Two pointers advance $j$ while $nums[i] > 2 \\times nums[j]$, accumulating $(j - (mid + 1))$ in $O(N)$ time per level.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def reversePairs(nums: list[int]) -> int:
    def merge_sort(l, r):
        if l >= r:
            return 0
        mid = (l + r) // 2
        count = merge_sort(l, mid) + merge_sort(mid + 1, r)
        
        # Count reverse pairs
        j = mid + 1
        for i in range(l, mid + 1):
            while j <= r and nums[i] > 2 * nums[j]:
                j += 1
            count += j - (mid + 1)
            
        # Merge sorted halves in place
        nums[l:r + 1] = sorted(nums[l:r + 1])
        return count
        
    return merge_sort(0, len(nums) - 1)
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(N \\log N)$ — Standard merge sort recurrence with $O(N)$ two-pointer scan.<br>
<strong>Space:</strong> $O(N)$ — Temporary merge buffers and recursion stack.</p>
''',
}
