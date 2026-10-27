"""Deep tutorials for Pattern 21: Intervals & Line Sweep Patterns."""
DEEP = {}
DEEP[56] = """<h3>Problem Overview</h3>
<p>Given an array of <code>intervals</code> where <code>intervals[i] = [start_i, end_i]</code>, merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.</p>

<h3>Key Insights</h3>
<p>Sorting by start time simplifies overlap detection. If intervals are sorted such that $start_1 \\le start_2 \\le \\dots$:
Interval $B$ overlaps with the current merged interval $A$ if and only if:
$$B.start \\le A.end$$
If they overlap, extend the merged interval's end: $A.end = \\max(A.end, B.end)$.
If they do not overlap ($B.start > A.end$), append $B$ as the new active interval.</p>

<details>
<summary><strong>Python 3 Solution (Sort + Single Scan)</strong></summary>
<div class="code-block">
<pre><code class="language-python">from typing import List

class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        intervals.sort(key=lambda x: x[0])
        merged = []
        
        for start, end in intervals:
            if not merged or start > merged[-1][1]:
                merged.append([start, end])
            else:
                merged[-1][1] = max(merged[-1][1], end)
                
        return merged
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> $O(N \\log N)$ for sorting + $O(N)$ linear pass.</li>
  <li><strong>Space Complexity:</strong> $O(N)$ for sorting space / output.</li>
  <li><strong>Edge Cases:</strong> Single interval, one interval completely enclosing another (e.g. <code>[1, 6], [2, 4]</code>), intervals touching at endpoints (e.g. <code>[1, 4], [4, 5]</code>).</li>
</ul>"""

DEEP[57] = """<h3>Problem Overview</h3>
<p>You are given an array of non-overlapping intervals sorted in ascending order by start time, and a new interval <code>newInterval = [start, end]</code>. Insert <code>newInterval</code> into <code>intervals</code> such that the list is still sorted in ascending order and non-overlapping (merge if necessary).</p>

<h3>Key Insights</h3>
<p>Because the input is already sorted, a three-phase linear scan solves it in $O(n)$ time:
<ol>
  <li><strong>Phase 1 (Before):</strong> Append all intervals that end strictly before <code>newInterval.start</code> ($end_i < newInterval.start$).</li>
  <li><strong>Phase 2 (Overlap & Merge):</strong> For all intervals that overlap with <code>newInterval</code> ($start_i \\le newInterval.end$):
      $$newInterval.start = \\min(newInterval.start, start_i)$$
      $$newInterval.end = \\max(newInterval.end, end_i)$$</li>
  <li><strong>Phase 3 (After):</strong> Append the merged <code>newInterval</code>, then append all remaining intervals that start after <code>newInterval.end</code>.</li>
</ol></p>

<details>
<summary><strong>Python 3 Solution (Three-Phase Linear Scan - O(N))</strong></summary>
<div class="code-block">
<pre><code class="language-python">from typing import List

class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        res = []
        i, n = 0, len(intervals)
        s, e = newInterval
        
        # 1. Add all intervals completely before newInterval
        while i < n and intervals[i][1] < s:
            res.append(intervals[i])
            i += 1
            
        # 2. Merge all overlapping intervals
        while i < n and intervals[i][0] <= e:
            s = min(s, intervals[i][0])
            e = max(e, intervals[i][1])
            i += 1
        res.append([s, e])
        
        # 3. Add all remaining intervals after newInterval
        while i < n:
            res.append(intervals[i])
            i += 1
            
        return res
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> $O(n)$ single linear scan.</li>
  <li><strong>Space Complexity:</strong> $O(n)$ for output array.</li>
  <li><strong>Edge Cases:</strong> Empty intervals list (returns <code>[newInterval]</code>), newInterval placed at very beginning or very end without overlap.</li>
</ul>"""

DEEP[218] = """<h3>Problem Overview</h3>
<p>A city's skyline is the outer contour of the silhouette formed by all the buildings. Given the locations and heights of all buildings <code>[left, right, height]</code>, return the key points that outline the skyline.</p>

<h3>Key Insights</h3>
<p><strong>Line Sweep with Max-Heap:</strong>
Convert each building into two events along the X-axis:
<ol>
  <li>Start of building at $x = left$: adds height $h$ (represented as $-h$ for max-heap).</li>
  <li>End of building at $x = right$: removes height $h$.</li>
</ol>
Sort events by X coordinate.
At each critical X position, maintain active building heights in a max-heap.
If the maximum height changes after processing all events at position X, record $[X, current_max_height]$ as a skyline keypoint!
Use lazy deletion to pop expired buildings from the heap top.</p>

<details>
<summary><strong>Python 3 Solution (Click to Expand)</strong></summary>
<div class="code-block">
<pre><code class="language-python">from typing import List
import heapq

class Solution:
    def getSkyline(self, buildings: List[List[int]]) -> List[List[int]]:
        # Events: (x, -h, right) for start, (right, 0, 0) for end
        events = []
        for l, r, h in buildings:
            events.append((l, -h, r))
            events.append((r, 0, 0))
        # Sort events: on tie, higher building first, start before end
        events.sort()
        
        # Max-heap storing (-h, right)
        heap = [(0, float('inf'))]
        skyline = []
        prev_h = 0
        
        for x, neg_h, r in events:
            if neg_h < 0:
                heapq.heappush(heap, (neg_h, r))
                
            # Pop expired buildings from heap top
            while heap[0][1] <= x:
                heapq.heappop(heap)
                
            curr_h = -heap[0][0]
            if curr_h != prev_h:
                skyline.append([x, curr_h])
                prev_h = curr_h
                
        return skyline
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> $O(N \\log N)$.</li>
  <li><strong>Space Complexity:</strong> $O(N)$.</li>
</ul>"""

DEEP[252] = """<h3>Problem Overview</h3>
<p>Given an array of meeting time intervals consisting of start and end times <code>[[s1, e1], [s2, e2], ...]</code>, determine if a person could attend all meetings without any conflicts.</p>

<h3>Key Insights</h3>
<p>Sort meetings by start time: <code>intervals.sort(key=lambda x: x[0])</code>.
A conflict exists if and only if any meeting starts before the previous meeting finishes:
$$intervals[i][0] < intervals[i - 1][1]$$
If any adjacent pair violates this, return <code>False</code>. If all finish before the next begins, return <code>True</code>.</p>

<details>
<summary><strong>Python 3 Solution (Click to Expand)</strong></summary>
<div class="code-block">
<pre><code class="language-python">from typing import List

class Solution:
    def canAttendMeetings(self, intervals: List[List[int]]) -> bool:
        intervals.sort(key=lambda x: x[0])
        for i in range(1, len(intervals)):
            if intervals[i][0] < intervals[i - 1][1]:
                return False
        return True
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> $O(N \\log N)$ sorting.</li>
  <li><strong>Space Complexity:</strong> $O(1)$.</li>
  <li><strong>Edge Cases:</strong> Empty intervals or 1 interval (always <code>True</code>), meetings touching at border ($[1, 5], [5, 10]$ do not conflict).</li>
</ul>"""

DEEP[253] = """<h3>Problem Overview</h3>
<p>Given an array of meeting time intervals consisting of start and end times, return the minimum number of conference rooms required.</p>

<h3>Key Insights</h3>
<p>This asks for the maximum number of concurrent overlapping meetings at any point in time. Two optimal techniques:
<ol>
  <li><strong>Min-Heap:</strong> Sort intervals by start time. Keep a min-heap of active meeting end times. If the earliest finishing meeting in the heap finishes before the current meeting starts ($heap[0] \\le start$), reuse that room (pop from heap). Push current meeting's end time. The heap size is the number of rooms needed: $O(N \\log N)$.</li>
  <li><strong>Line Sweep / Chronological Event Separation:</strong> Separate starts and ends into two sorted arrays. Track current active rooms: increment on start, decrement on end.</li>
</ol></p>

<details>
<summary><strong>Python 3 Solution (Min-Heap Simulation)</strong></summary>
<div class="code-block">
<pre><code class="language-python">from typing import List
import heapq

class Solution:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        if not intervals:
            return 0
            
        intervals.sort(key=lambda x: x[0])
        rooms = []  # stores end times
        
        for start, end in intervals:
            if rooms and rooms[0] <= start:
                heapq.heappop(rooms)  # reuse room
            heapq.heappush(rooms, end)
            
        return len(rooms)
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> $O(N \\log N)$.</li>
  <li><strong>Space Complexity:</strong> $O(N)$ for heap.</li>
</ul>"""

DEEP[352] = """<h3>Problem Overview</h3>
<p>Given a data stream input of non-negative integers $a_1, a_2, \\dots$, summarize the numbers seen so far as a list of disjoint intervals.</p>

<h3>Key Insights</h3>
<p>Store all unique numbers in a set or boolean array / sorted list.
When returning intervals:
Merge consecutive numbers $[start, end]$ where each adjacent pair differs by 1.
Using a sorted structure or binary search tree (or maintaining a balanced set in Python with <code>bisect</code>), adjacent intervals can be merged dynamically upon insertion.</p>

<details>
<summary><strong>Python 3 Solution (Click to Expand)</strong></summary>
<div class="code-block">
<pre><code class="language-python">from typing import List
import bisect

class SummaryRanges:
    def __init__(self):
        self.intervals = []  # list of [start, end]

    def addNum(self, value: int) -> None:
        # Find insertion position
        idx = bisect.bisect_right(self.intervals, [value, float('inf')])
        
        # Check if already covered by previous interval
        if idx > 0 and self.intervals[idx - 1][1] >= value:
            return
            
        left_merge = (idx > 0 and self.intervals[idx - 1][1] + 1 == value)
        right_merge = (idx < len(self.intervals) and self.intervals[idx][0] == value + 1)
        
        if left_merge and right_merge:
            self.intervals[idx - 1][1] = self.intervals[idx][1]
            self.intervals.pop(idx)
        elif left_merge:
            self.intervals[idx - 1][1] = value
        elif right_merge:
            self.intervals[idx][0] = value
        else:
            self.intervals.insert(idx, [value, value])

    def getIntervals(self) -> List[List[int]]:
        return self.intervals
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> <code>addNum</code> is $O(N)$ insertion in array, $O(\\log N)$ in balanced BST; <code>getIntervals</code> is $O(1)$.</li>
  <li><strong>Space Complexity:</strong> $O(N)$.</li>
</ul>"""

DEEP[729] = """<h3>Problem Overview</h3>
<p>Implement the <code>MyCalendar</code> class to store your events. A new event can be added if adding the event will not cause a double booking (two events have some non-empty intersection $[start, end)$).</p>

<h3>Key Insights</h3>
<p>Two intervals $[s_1, e_1)$ and $[s_2, e_2)$ overlap if and only if:
$$\\max(s_1, s_2) < \\min(e_1, e_2) \\iff s_1 < e_2 \\quad \text{and} \\quad s_2 < e_1$$
Maintain a sorted list of booked intervals using <code>bisect</code>.
When booking $[start, end)$:
Locate where $[start, end)$ would be inserted with binary search.
Check only the immediate predecessor and successor intervals for conflicts in $O(1)$!</p>

<details>
<summary><strong>Python 3 Solution (Binary Search Insertion)</strong></summary>
<div class="code-block">
<pre><code class="language-python">import bisect

class MyCalendar:
    def __init__(self):
        self.calendar = []  # sorted by start time

    def book(self, start: int, end: int) -> bool:
        idx = bisect.bisect_right(self.calendar, (start, end))
        
        # Check predecessor conflict
        if idx > 0 and self.calendar[idx - 1][1] > start:
            return False
            
        # Check successor conflict
        if idx < len(self.calendar) and self.calendar[idx][0] < end:
            return False
            
        self.calendar.insert(idx, (start, end))
        return True
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> $O(\\log N)$ binary search check + $O(N)$ list insertion.</li>
  <li><strong>Space Complexity:</strong> $O(N)$.</li>
</ul>"""

DEEP[731] = """<h3>Problem Overview</h3>
<p>Implement the <code>MyCalendarTwo</code> class such that no <strong>triple booking</strong> happens (three events have some non-empty intersection).</p>

<h3>Key Insights</h3>
<p>Maintain two lists:
<ol>
  <li><code>bookings</code>: All successfully booked single events $[s, e)$.</li>
  <li><code>overlaps</code>: All double-booked interval segments $[\\max(s_1, s_2), \\min(e_1, e_2))$.</li>
</ol>
When trying to book a new interval $[start, end)$:
<ol>
  <li>Check if $[start, end)$ overlaps with ANY interval in <code>overlaps</code>. If yes, it would cause a triple booking! Return <code>False</code> immediately.</li>
  <li>Otherwise, find all overlaps between $[start, end)$ and existing <code>bookings</code>, adding them to <code>overlaps</code>.</li>
  <li>Add $[start, end)$ to <code>bookings</code> and return <code>True</code>!</li>
</ol></p>

<details>
<summary><strong>Python 3 Solution (Double Booking Tracker)</strong></summary>
<div class="code-block">
<pre><code class="language-python">class MyCalendarTwo:
    def __init__(self):
        self.bookings = []
        self.overlaps = []

    def book(self, start: int, end: int) -> bool:
        # 1. Check if it causes triple booking
        for s, e in self.overlaps:
            if max(start, s) < min(end, e):
                return False
                
        # 2. Record new double-booked overlaps
        for s, e in self.bookings:
            os = max(start, s)
            oe = min(end, e)
            if os < oe:
                self.overlaps.append((os, oe))
                
        self.bookings.append((start, end))
        return True
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> $O(N)$ per booking call.</li>
  <li><strong>Space Complexity:</strong> $O(N)$ intervals stored.</li>
</ul>"""

DEEP[732] = """<h3>Problem Overview</h3>
<p>Implement the <code>MyCalendarThree</code> class. An event can always be added. Return an integer $k$ representing the largest integer such that there exists a $k$-booking in the calendar (the maximum number of concurrent overlapping events).</p>

<h3>Key Insights</h3>
<p><strong>Boundary Event Map / Line Sweep:</strong>
Each booking of $[start, end)$ introduces two timestamp events:
<ul>
  <li><code>events[start] += 1</code></li>
  <li><code>events[end] -= 1</code></li>
</ul>
Sweep through all events in chronological order, maintaining a running prefix sum of active concurrent events. The peak value reached is the answer $k$!</p>

<details>
<summary><strong>Python 3 Solution (Chronological Event Map)</strong></summary>
<div class="code-block">
<pre><code class="language-python">from collections import defaultdict

class MyCalendarThree:
    def __init__(self):
        self.events = defaultdict(int)

    def book(self, startTime: int, endTime: int) -> int:
        self.events[startTime] += 1
        self.events[endTime] -= 1
        
        max_k = curr = 0
        for t in sorted(self.events.keys()):
            curr += self.events[t]
            max_k = max(max_k, curr)
            
        return max_k
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> $O(N \\log N)$ sorting of event timestamps per booking.</li>
  <li><strong>Space Complexity:</strong> $O(N)$ event timestamps.</li>
</ul>"""

DEEP[759] = """<h3>Problem Overview</h3>
<p>Given a list <code>schedule</code> of employees, which represents the working time for each employee, return the list of finite intervals representing common, positive-length free time for all employees, sorted in order of time.</p>

<h3>Key Insights</h3>
<p>Flatten all employees' work intervals into a single global list.
Sort all intervals by start time.
Merge overlapping intervals just like LC 56!
Any gap between adjacent merged working intervals constitutes a common free time interval:
$$\text{Gap} = [merged[i-1].end, merged[i].start]$$</p>

<details>
<summary><strong>Python 3 Solution (Interval Merging + Gap Extraction)</strong></summary>
<div class="code-block">
<pre><code class="language-python"># Definition for an Interval:
# class Interval:
#     def __init__(self, start: int = None, end: int = None):
#         self.start = start
#         self.end = end

class Solution:
    def employeeFreeTime(self, schedule: '[[Interval]]') -> '[Interval]':
        all_intervals = []
        for emp in schedule:
            for iv in emp:
                all_intervals.append([iv.start, iv.end])
                
        all_intervals.sort(key=lambda x: x[0])
        
        merged = []
        for start, end in all_intervals:
            if not merged or start > merged[-1][1]:
                merged.append([start, end])
            else:
                merged[-1][1] = max(merged[-1][1], end)
                
        # Gaps between merged working intervals
        free_time = []
        for i in range(1, len(merged)):
            free_time.append(Interval(merged[i - 1][1], merged[i][0]))
            
        return free_time
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> $O(N \\log N)$ where $N$ is total intervals across all employees.</li>
  <li><strong>Space Complexity:</strong> $O(N)$.</li>
</ul>"""

DEEP[986] = """<h3>Problem Overview</h3>
<p>You are given two lists of closed intervals, <code>firstList</code> and <code>secondList</code>, where each list of intervals is pairwise disjoint and in sorted order. Return the intersection of these two interval lists.</p>

<h3>Key Insights</h3>
<p>Two-Pointer simulation:
For current intervals $A = [s_1, e_1]$ and $B = [s_2, e_2]$:
<ol>
  <li>The candidate intersection start is $\\max(s_1, s_2)$, and end is $\\min(e_1, e_2)$.</li>
  <li>They intersect if and only if $\\max(s_1, s_2) \\le \\min(e_1, e_2)$.</li>
  <li>Advance the pointer for whichever interval ends earlier ($\\min(e_1, e_2)$), because it cannot possibly intersect with any future interval!</li>
</ol></p>

<details>
<summary><strong>Python 3 Solution (Two-Pointer Scan)</strong></summary>
<div class="code-block">
<pre><code class="language-python">from typing import List

class Solution:
    def intervalIntersection(self, firstList: List[List[int]], secondList: List[List[int]]) -> List[List[int]]:
        i = j = 0
        res = []
        
        while i < len(firstList) and j < len(secondList):
            s1, e1 = firstList[i]
            s2, e2 = secondList[j]
            
            start = max(s1, s2)
            end = min(e1, e2)
            
            if start <= end:
                res.append([start, end])
                
            # Discard interval that finishes earlier
            if e1 < e2:
                i += 1
            else:
                j += 1
                
        return res
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> $O(M + N)$ where $M$ and $N$ are list lengths.</li>
  <li><strong>Space Complexity:</strong> $O(1)$ extra space excluding output.</li>
  <li><strong>Edge Cases:</strong> Either list empty, point intersection (e.g. <code>[1, 2]</code> and <code>[2, 3]</code> -> <code>[2, 2]</code>).</li>
</ul>"""

DEEP[1288] = """<h3>Problem Overview</h3>
<p>Given an array <code>intervals</code> where <code>intervals[i] = [li, ri]</code>, remove all intervals that are covered by another interval in the list. An interval $[a, b)$ is covered by $[c, d)$ if and only if $c \\le a$ and $b \\le d$. Return the number of remaining intervals.</p>

<h3>Key Insights</h3>
<p>Sort intervals by <strong>start ascending</strong>, and on tie by <strong>end descending</strong>:
<code>intervals.sort(key=lambda x: (x[0], -x[1]))</code>
With this sorting order:
Whenever an interval has $x[0] == prev[0]$, the wider one appears first!
We maintain <code>max_end</code> seen so far. For each interval $[s, e]$:
<ul>
  <li>If $e \\le max_end$: It is completely covered by an earlier interval with a smaller or equal start and larger end! We don't count it.</li>
  <li>If $e > max_end$: It is uncovered! Increment count and update $max_end = e$.</li>
</ul></p>

<details>
<summary><strong>Python 3 Solution (Click to Expand)</strong></summary>
<div class="code-block">
<pre><code class="language-python">from typing import List

class Solution:
    def removeCoveredIntervals(self, intervals: List[List[int]]) -> int:
        # Start ascending, end descending
        intervals.sort(key=lambda x: (x[0], -x[1]))
        
        count = 0
        max_end = 0
        
        for start, end in intervals:
            if end > max_end:
                count += 1
                max_end = end
                
        return count
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> $O(N \\log N)$ sorting + $O(N)$ scan.</li>
  <li><strong>Space Complexity:</strong> $O(1)$ extra space.</li>
</ul>"""

DEEP[1851] = """<h3>Problem Overview</h3>
<p>Given a 2D integer array <code>intervals</code> and an integer array <code>queries</code>, the size of interval $[l, r]$ is $r - l + 1$. For each query $q_j$, find the minimum size of an interval such that $l_i \\le q_j \\le r_i$. If no such interval exists, return -1.</p>

<h3>Key Insights</h3>
<p><strong>Offline Queries + Min-Heap:</strong>
Sort intervals by start time.
Sort queries in ascending order while keeping their original indices: <code>sorted_q = sorted(enumerate(queries), key=lambda x: x[1])</code>.
For each query $q$:
<ol>
  <li>Push all intervals with $start \\le q$ into a min-heap ordered by <strong>interval size</strong> $(r - l + 1, r)$.</li>
  <li>Pop any intervals from heap top whose $r < q$ (they cannot cover $q$ or any future larger query).</li>
  <li>The top of the heap is the minimum size interval covering $q$!</li>
</ol></p>

<details>
<summary><strong>Python 3 Solution (Offline Sorting + Min-Heap)</strong></summary>
<div class="code-block">
<pre><code class="language-python">from typing import List
import heapq

class Solution:
    def minInterval(self, intervals: List[List[int]], queries: List[int]) -> List[int]:
        intervals.sort(key=lambda x: x[0])
        q_sorted = sorted(enumerate(queries), key=lambda x: x[1])
        
        heap = []  # (size, right)
        ans = [-1] * len(queries)
        i = 0
        n = len(intervals)
        
        for orig_idx, q in q_sorted:
            # Add all intervals that start <= q
            while i < n and intervals[i][0] <= q:
                l, r = intervals[i]
                heapq.heappush(heap, (r - l + 1, r))
                i += 1
                
            # Discard intervals that end < q
            while heap and heap[0][1] < q:
                heapq.heappop(heap)
                
            if heap:
                ans[orig_idx] = heap[0][0]
                
        return ans
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> $O(N \\log N + Q \\log Q)$. Each interval is pushed and popped at most once.</li>
  <li><strong>Space Complexity:</strong> $O(N + Q)$.</li>
</ul>"""

DEEP[1854] = """<h3>Problem Overview</h3>
<p>Given a 2D integer array <code>logs</code> where <code>logs[i] = [birth_i, death_i]</code>, return the earliest year with the maximum population. A person is considered alive during the years in $[birth_i, death_i - 1]$.</p>

<h3>Key Insights</h3>
<p>The year range is small and fixed: $1950 \\le year \\le 2050$ (101 years).
Use a <strong>Difference Array</strong> of size 101:
For each person $[birth, death]$:
<ul>
  <li>Increment <code>delta[birth - 1950] += 1</code></li>
  <li>Decrement <code>delta[death - 1950] -= 1</code> (death year is not counted)</li>
</ul>
Prefix sum over the difference array reveals the maximum population year in $O(N + 101)$ time.</p>

<details>
<summary><strong>Python 3 Solution (Click to Expand)</strong></summary>
<div class="code-block">
<pre><code class="language-python">from typing import List

class Solution:
    def maximumPopulation(self, logs: List[List[int]]) -> int:
        delta = [0] * 102
        for b, d in logs:
            delta[b - 1950] += 1
            delta[d - 1950] -= 1
            
        max_pop = curr_pop = 0
        best_year = 1950
        
        for i in range(101):
            curr_pop += delta[i]
            if curr_pop > max_pop:
                max_pop = curr_pop
                best_year = 1950 + i
                
        return best_year
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> $O(N + Y)$ where $Y = 100$.</li>
  <li><strong>Space Complexity:</strong> $O(Y) = O(1)$.</li>
</ul>"""

DEEP[2402] = """<h3>Problem Overview</h3>
<p>You are given an integer $n$ (rooms numbered $0$ to $n - 1$) and a 2D integer array <code>meetings</code>. Meetings are allocated to the lowest numbered unused room. If all rooms are busy, the meeting is delayed until a room becomes free. Return the number of the room that held the most meetings.</p>

<h3>Key Insights</h3>
<p>Two Priority Queues:
<ol>
  <li><code>available_rooms</code>: Min-heap storing available room IDs (lowest ID on top). Initially contains $0, 1, \\dots, n - 1$.</li>
  <li><code>busy_rooms</code>: Min-heap storing tuples <code>(end_time, room_id)</code>.</li>
</ol>
Sort <code>meetings</code> by start time. For each meeting $(start, end)$:
<ol>
  <li>Free any rooms whose <code>end_time <= start</code>, returning them to <code>available_rooms</code>.</li>
  <li>If an available room exists, pop lowest room ID, assign meeting until $end$.</li>
  <li>If all rooms are busy, pop room with earliest <code>end_time</code>:
      The meeting starts at that room's <code>free_time</code> and runs for $duration = end - start$. Push back to <code>busy_rooms</code> with new end time <code>free_time + duration</code>.</li>
</ol></p>

<details>
<summary><strong>Python 3 Solution (Double Min-Heap Simulation)</strong></summary>
<div class="code-block">
<pre><code class="language-python">from typing import List
import heapq

class Solution:
    def mostBooked(self, n: int, meetings: List[List[int]]) -> int:
        meetings.sort(key=lambda x: x[0])
        
        available = list(range(n))
        heapq.heapify(available)
        busy = []  # (end_time, room_id)
        
        room_counts = [0] * n
        
        for start, end in meetings:
            duration = end - start
            # Free rooms
            while busy and busy[0][0] <= start:
                _, room = heapq.heappop(busy)
                heapq.heappush(available, room)
                
            if available:
                room = heapq.heappop(available)
                heapq.heappush(busy, (end, room))
            else:
                earliest_end, room = heapq.heappop(busy)
                heapq.heappush(busy, (earliest_end + duration, room))
                
            room_counts[room] += 1
            
        max_meetings = max(room_counts)
        return room_counts.index(max_meetings)
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> $O(M \\log M + M \\log n)$ where $M$ is number of meetings.</li>
  <li><strong>Space Complexity:</strong> $O(n)$ for room heaps.</li>
</ul>"""

DEEP[2406] = """<h3>Problem Overview</h3>
<p>Given an array <code>intervals</code>, divide the intervals into one or more groups such that each interval is in exactly one group, and no two intervals in the same group intersect. Return the minimum number of groups required.</p>

<h3>Key Insights</h3>
<p>By Dilworth's theorem and interval scheduling theory, the minimum number of non-overlapping groups required is equal to the <strong>maximum number of mutually overlapping intervals at any point in time</strong>!
This is mathematically identical to Meeting Rooms II (LC 253), except here intervals are inclusive $[left, right]$, so an interval ending at $t$ overlaps with one starting at $t$.
Events: $(start, +1)$ and $(end + 1, -1)$. Sort events and track running prefix sum!</p>

<details>
<summary><strong>Python 3 Solution (Line Sweep with Event Deltas)</strong></summary>
<div class="code-block">
<pre><code class="language-python">from typing import List
from collections import defaultdict

class Solution:
    def minGroups(self, intervals: List[List[int]]) -> int:
        events = defaultdict(int)
        for s, e in intervals:
            events[s] += 1
            events[e + 1] -= 1  # end is inclusive, freed at e + 1
            
        max_groups = curr = 0
        for t in sorted(events.keys()):
            curr += events[t]
            max_groups = max(max_groups, curr)
            
        return max_groups
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> $O(N \\log N)$ event sorting.</li>
  <li><strong>Space Complexity:</strong> $O(N)$ event map.</li>
</ul>"""
