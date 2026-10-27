# -*- coding: utf-8 -*-
# Deep tutorials — Pattern P7: Heap (Priority Queue).
# Keyed by LC number; merged as (7, lc). [[nn]] -> links via build.py.

DEEP = {
# ============================================================ LC 215
215: '''<h2>🧭 How to think about it</h2>
<p>You need the <strong>kth largest</strong> element in an unsorted array. Sorting the entire array is O(n log n), which wastes work sorting the remaining n - k elements. Instead, think: <strong>what data structure can maintain the top k candidates dynamically?</strong> A min-heap of size k: the smallest of the top-k sits at the root. Any number bigger than the root replaces it.</p>

<h2>🐢 Brute force first</h2>
<p>Sort the array in descending order and return the element at index <code>k - 1</code>.</p>
<pre><code>def findKthLargest(nums, k):
    nums.sort(reverse=True)
    return nums[k - 1]</code></pre>
<p>Time O(n log n), Space O(1) or O(n) depending on sort implementation.</p>

<div class="insight">💡 <strong>Key insight:</strong> keep a <strong>min-heap of size k</strong>. As you scan, push each element; when the heap size exceeds k, pop the minimum. After processing all n elements, the heap contains the k largest elements, and the root is the kth largest. Alternatively, Quickselect achieves O(n) average time.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Initialize an empty min-heap <code>h = []</code>.</li>
<li>Iterate through each number <code>x</code> in <code>nums</code>:</li>
<li>Push <code>x</code> onto <code>h</code>. If <code>len(h) &gt; k</code>, pop the smallest element via <code>heappop(h)</code>.</li>
<li>At the end, return <code>h[0]</code> (the root of the min-heap).</li>
</ol>

<h2>🎞️ Visual dry run — nums = [3, 2, 1, 5, 6, 4], k = 2</h2>
<pre class="viz">x=3  → heap [3] (size 1 &lt;= 2)
x=2  → heap [2, 3] (size 2 &lt;= 2)
x=1  → push 1 → [1, 3, 2], size 3 &gt; 2 → pop 1 → heap [2, 3]
x=5  → push 5 → [2, 3, 5], size 3 &gt; 2 → pop 2 → heap [3, 5]
x=6  → push 6 → [3, 5, 6], size 3 &gt; 2 → pop 3 → heap [5, 6]
x=4  → push 4 → [4, 6, 5], size 3 &gt; 2 → pop 4 → heap [5, 6]
Result: h[0] = 5 ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>import heapq

def findKthLargest(nums, k):
    # Maintain a min-heap of the k largest elements seen so far
    heap = []
    for x in nums:
        heapq.heappush(heap, x)
        if len(heap) &gt; k:
            heapq.heappop(heap)   # discard the smallest among the top k+1
    return heap[0]                # the root is the kth largest element</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n log k)</strong> — processing n elements with heap operations of size at most k+1. <strong>Space O(k)</strong> — to store k elements in the heap.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li><code>k = 1</code>: returns the maximum element.</li>
<li><code>k = len(nums)</code>: returns the minimum element.</li>
<li>Duplicate elements: handled naturally since the heap allows duplicates.</li>
<li>Negative numbers: heap comparison operates directly on integer values.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Using a max-heap of size n instead of a min-heap of size k, which uses O(n) space and O(n + k log n) time.</li>
<li>Popping when <code>len(heap) == k</code> instead of after pushing the (k+1)th element.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Kth Smallest Element: maintain a max-heap of size k (or invert values in Python).</li>
<li>Streaming Kth Largest ([[703]]): where numbers arrive one by one.</li>
<li>Quickselect approach: partition around a pivot for O(n) average time complexity.</li>
</ul>''',

# ============================================================ LC 347
347: '''<h2>🧭 How to think about it</h2>
<p>Given an integer array, return the <code>k</code> most frequent elements. First, count frequencies using a hash map. Then we need the k largest counts. We can either use a min-heap of size k (O(n log k)) or bucket sort based on frequencies (O(n)).</p>

<h2>🐢 Brute force first</h2>
<p>Count frequencies with a hash map, sort the items by frequency descending, and take the first k elements.</p>
<pre><code>from collections import Counter
def topKFrequent(nums, k):
    counts = Counter(nums)
    sorted_items = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    return [item[0] for item in sorted_items[:k]]</code></pre>
<p>Time O(m log m) where m is the number of distinct elements (up to n). Space O(m).</p>

<div class="insight">💡 <strong>Key insight:</strong> frequency of any element cannot exceed <code>n</code>. We can use <strong>Bucket Sort</strong>: an array of lists where index <code>i</code> holds elements with frequency <code>i</code>. Scanning backwards from index n yields the top k frequent elements in O(n) linear time.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Count occurrences of each number using <code>Counter(nums)</code>.</li>
<li>Create <code>buckets</code> of size <code>len(nums) + 1</code>, where <code>buckets[f]</code> is a list of numbers appearing <code>f</code> times.</li>
<li>Populate buckets by mapping each <code>(num, count)</code> into <code>buckets[count].append(num)</code>.</li>
<li>Iterate backwards from frequency <code>len(nums)</code> down to 1, collecting numbers into <code>result</code> until <code>len(result) == k</code>.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [1,1,1,2,2,3], k = 2</h2>
<pre class="viz">Counts: {1: 3, 2: 2, 3: 1}
Buckets:
freq 1: [3]
freq 2: [2]
freq 3: [1]
freq 4..6: []
Scan from freq 6 down to 1:
- freq 3: take 1 → res = [1]
- freq 2: take 2 → res = [1, 2] (len == k == 2, done!)</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>from collections import Counter

def topKFrequent(nums, k):
    count = Counter(nums)
    # Bucket index = frequency, value = list of numbers with that frequency
    buckets = [[] for _ in range(len(nums) + 1)]
    for num, freq in count.items():
        buckets[freq].append(num)
        
    res = []
    # Collect from highest frequency bucket down to 1
    for freq in range(len(nums), 0, -1):
        for num in buckets[freq]:
            res.append(num)
            if len(res) == k:
                return res
    return res</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — O(n) to count frequencies, O(n) to populate buckets, and O(n) to gather top k. <strong>Space O(n)</strong> — for the hash map and the bucket array.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li><code>k = len(set(nums))</code>: all distinct elements returned.</li>
<li>All elements have frequency 1: any k elements are valid.</li>
<li>Array with a single unique element: returned immediately.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Using bucket size <code>n</code> instead of <code>n + 1</code>, resulting in an IndexError when an element appears n times.</li>
<li>Using O(n log n) sorting when interviewers specifically ask for better than O(n log n).</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Sort Characters By Frequency ([[451]]).</li>
<li>Top K Frequent Words (requires tie-breaking by lexicographical order).</li>
</ul>''',

# ============================================================ LC 451
451: '''<h2>🧭 How to think about it</h2>
<p>Sort characters in a string by decreasing frequency. Similar to [[347]], count each character's occurrences and sort or bucket-sort characters by frequency, then reconstruct the string multiplying each character by its frequency.</p>

<h2>🐢 Brute force first</h2>
<p>Count character frequencies with a dictionary, sort the unique characters by frequency descending, and build the string.</p>
<pre><code>from collections import Counter
def frequencySort(s):
    count = Counter(s)
    chars = sorted(count.keys(), key=lambda c: count[c], reverse=True)
    return "".join(c * count[c] for c in chars)</code></pre>
<p>Time O(n + k log k) where k is the number of distinct characters (at most 52 for ASCII letters, 128 for full ASCII). Space O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> since maximum frequency is <code>n = len(s)</code>, bucket sort groups characters by frequency in O(n) time and O(n) space without any comparison sorting.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Count character frequencies using <code>Counter(s)</code>.</li>
<li>Create bucket array of length <code>len(s) + 1</code>.</li>
<li>For each character and count, append character to <code>buckets[count]</code>.</li>
<li>Traverse buckets from <code>len(s)</code> down to 1, appending <code>c * count</code> to the result string.</li>
</ol>

<h2>🎞️ Visual dry run — s = "tree"</h2>
<pre class="viz">Counts: {'t': 1, 'r': 1, 'e': 2}
Buckets:
freq 2: ['e']
freq 1: ['t', 'r']
Scan from 4 down:
freq 2: 'e'*2 = "ee"
freq 1: 't'*1, 'r'*1 = "tr"
Result: "eert" (or "eetr") ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>from collections import Counter

def frequencySort(s):
    count = Counter(s)
    buckets = [[] for _ in range(len(s) + 1)]
    for char, freq in count.items():
        buckets[freq].append(char)
        
    res = []
    for freq in range(len(s), 0, -1):
        for char in buckets[freq]:
            res.append(char * freq)
    return "".join(res)</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — linear scan to count, bucket, and assemble. <strong>Space O(n)</strong> — for the buckets and reconstructed string.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>All characters unique (e.g. "abc"): any permutation is valid.</li>
<li>All characters identical (e.g. "aaaa"): string returned unchanged.</li>
<li>Case sensitivity: 'A' and 'a' are treated as distinct characters.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Concatenating strings inside a loop with <code>+=</code> (O(n^2) in some languages) instead of joining a list of string chunks.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Top K Frequent Elements ([[347]]).</li>
<li>Reorganize String ([[767]]): rearrange characters so no two adjacent characters are identical.</li>
</ul>''',

# ============================================================ LC 703
703: '''<h2>🧭 How to think about it</h2>
<p>You need to continuously find the kth largest element in a stream of numbers as new values arrive. If we keep only the <strong>k largest numbers</strong> in a min-heap, the smallest of these k numbers is at the root — which is exactly the kth largest element.</p>

<h2>🐢 Brute force first</h2>
<p>Append each incoming value to a list, sort the list descending, and return index <code>k - 1</code> on each <code>add()</code> call → O(n log n) per addition.</p>

<div class="insight">💡 <strong>Key insight:</strong> a <strong>min-heap of fixed size k</strong>. The heap root <code>heap[0]</code> is always the kth largest element. On adding <code>val</code>: if heap size &lt; k, push it; else if <code>val &gt; heap[0]</code>, push and pop via <code>heappushpop()</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Store <code>k</code> and convert the initial list into a heap using <code>heapify</code>.</li>
<li>While heap size exceeds <code>k</code>, pop the excess smaller elements.</li>
<li>In <code>add(val)</code>: if <code>len(heap) &lt; k</code>, push <code>val</code>; if <code>len(heap) == k</code> and <code>val &gt; heap[0]</code>, use <code>heapreplace(heap, val)</code>.</li>
<li>Return <code>heap[0]</code>.</li>
</ol>

<h2>🎞️ Visual dry run — k = 3, nums = [4, 5, 8, 2], add(3), add(5)</h2>
<pre class="viz">Init [4, 5, 8, 2] → heapify → pop min 2 → heap of size 3: [4, 5, 8]
add(3): 3 &lt; heap[0] (4) → 3 cannot enter top 3 → return 4
add(5): 5 &gt; heap[0] (4) → replace 4 with 5 → heap: [5, 5, 8] → return 5</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>import heapq

class KthLargest:
    def __init__(self, k: int, nums: list[int]):
        self.k = k
        self.heap = nums
        heapq.heapify(self.heap)
        # Trim heap down to size k
        while len(self.heap) &gt; k:
            heapq.heappop(self.heap)

    def add(self, val: int) -&gt; int:
        if len(self.heap) &lt; self.k:
            heapq.heappush(self.heap, val)
        elif val &gt; self.heap[0]:
            heapq.heapreplace(self.heap, val)   # pop root and push val in O(log k)
        return self.heap[0]</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(log k)</strong> per <code>add()</code> call; O(n log k) for initialization. <strong>Space O(k)</strong> for maintaining the heap.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Initial <code>nums</code> length is less than <code>k</code> (e.g. <code>k=3, nums=[1, 2]</code>): heap size grows to k upon subsequent <code>add()</code> calls.</li>
<li>Negative values: integer comparisons handle negatives correctly.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Using a max-heap: you would need to pop and restore k-1 elements on every query, making each <code>add()</code> O(k log n).</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Kth Largest Element in an Array ([[215]]).</li>
<li>Find Median from Data Stream ([[295]]): maintaining two balancing heaps.</li>
</ul>''',

# ============================================================ LC 973
973: '''<h2>🧭 How to think about it</h2>
<p>Given <code>points</code> in 2D space, return the <code>k</code> closest points to <code>(0, 0)</code>. Distance squared is <code>x^2 + y^2</code> (no need for square root since distance is monotonic). We need the k smallest distances, so maintain a <strong>max-heap of size k</strong>: the point with the largest distance among the top k is at the root. If a new point has a smaller distance, it replaces the root.</p>

<h2>🐢 Brute force first</h2>
<p>Compute distance for all points, sort by distance, and take the first k points → O(n log n) time.</p>

<div class="insight">💡 <strong>Key insight:</strong> use a <strong>max-heap of size k</strong> storing <code>(-dist, x, y)</code>. At any point, the heap holds the k closest points seen so far. If a new point is closer than the current worst in the heap, pop the worst and push the new one.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Initialize a max-heap <code>h = []</code>.</li>
<li>For each point <code>(x, y)</code>: calculate distance <code>d = x*x + y*y</code>.</li>
<li>Push <code>(-d, x, y)</code> to <code>h</code>.</li>
<li>If <code>len(h) &gt; k</code>, pop the root (which has the largest distance).</li>
<li>Return <code>[[x, y] for _, x, y in h]</code>.</li>
</ol>

<h2>🎞️ Visual dry run — points = [[1,3],[-2,2]], k = 1</h2>
<pre class="viz">[1, 3]  → dist = 1 + 9 = 10 → push (-10, 1, 3) → heap: [(-10, 1, 3)]
[-2, 2] → dist = 4 + 4 = 8  → push (-8, -2, 2) → heap size 2 &gt; 1
        → pop (-10, 1, 3) (largest distance discarded)
        → heap: [(-8, -2, 2)]
Result: [[-2, 2]] ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>import heapq

def kClosest(points, k):
    # Max-heap of size k: store negative distance so largest distance is popped first
    heap = []
    for x, y in points:
        dist = x * x + y * y
        heapq.heappush(heap, (-dist, x, y))
        if len(heap) &gt; k:
            heapq.heappop(heap)
            
    return [[x, y] for _, x, y in heap]</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n log k)</strong> — iterating through n points with heap of size at most k+1. <strong>Space O(k)</strong> — to store the k closest points.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li><code>k == len(points)</code>: returns all points.</li>
<li>Ties in distance: any order is accepted.</li>
<li>Coordinates with negative values: squaring removes negative signs.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Computing <code>math.sqrt()</code> for distance — floating point operations are slower and risk precision errors.</li>
<li>Using a min-heap of size n (O(n log n) space and time) instead of a max-heap of size k.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Quickselect approach: find the kth closest point in O(n) average time.</li>
<li>K Closest Elements ([[658]]).</li>
</ul>''',

# ============================================================ LC 1046
1046: '''<h2>🧭 How to think about it</h2>
<p>We are given stone weights. Each turn, pick the <strong>two heaviest stones</strong> <code>x</code> and <code>y</code> (with <code>x &lt;= y</code>). If <code>x == y</code>, both are destroyed; if <code>x != y</code>, stone <code>x</code> is destroyed and stone <code>y</code> has new weight <code>y - x</code>. Repeat until at most one stone remains. We need repeated maximum retrieval, which is the definition of a <strong>max-heap</strong>.</p>

<h2>🐢 Brute force first</h2>
<p>Sort the array descending every time after smashing two stones → O(n^2 log n).</p>

<div class="insight">💡 <strong>Key insight:</strong> invert all values to negative numbers and use Python's <code>heapq</code> as a <strong>max-heap</strong>. Popping twice gives the two largest stones in O(log n); pushing the difference back takes O(log n).</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Negate all elements in <code>stones</code> and heapify in O(n).</li>
<li>While <code>len(heap) &gt; 1</code>:</li>
<li>Pop the largest stone <code>y = -heappop(heap)</code>.</li>
<li>Pop the second largest stone <code>x = -heappop(heap)</code>.</li>
<li>If <code>y &gt; x</code>, push <code>-(y - x)</code> back onto the heap.</li>
<li>Return <code>-heap[0]</code> if heap is non-empty else <code>0</code>.</li>
</ol>

<h2>🎞️ Visual dry run — stones = [2, 7, 4, 1, 8, 1]</h2>
<pre class="viz">Heap: [-8, -7, -4, -1, -2, -1]
Pop 8 and 7: 8 != 7 → push 8 - 7 = 1 → Heap: [-4, -2, -1, -1, -1]
Pop 4 and 2: 4 != 2 → push 4 - 2 = 2 → Heap: [-2, -1, -1, -1]
Pop 2 and 1: 2 != 1 → push 2 - 1 = 1 → Heap: [-1, -1, -1]
Pop 1 and 1: 1 == 1 → both destroyed → Heap: [-1]
One stone left: 1 ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>import heapq

def lastStoneWeight(stones):
    # Python heapq is a min-heap; negate weights to simulate a max-heap
    heap = [-s for s in stones]
    heapq.heapify(heap)
    
    while len(heap) &gt; 1:
        y = -heapq.heappop(heap)   # heaviest stone
        x = -heapq.heappop(heap)   # second heaviest stone
        if y != x:
            heapq.heappush(heap, -(y - x))
            
    return -heap[0] if heap else 0</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n log n)</strong> — at most n-1 smashes, each doing O(log n) heap operations. <strong>Space O(n)</strong> — for the heap.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Single stone: immediately returned.</li>
<li>All stones pairwise equal: heap becomes empty, returns 0.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Take Gifts From the Richest Pile ([[2558]]).</li>
<li>Reorganize String ([[767]]).</li>
</ul>''',

# ============================================================ LC 295
295: '''<h2>🧭 How to think about it</h2>
<p>The median splits sorted numbers into two equal halves. Numbers arrive dynamically. We need fast access to the <strong>largest of the smaller half</strong> and the <strong>smallest of the larger half</strong>. This naturally calls for <strong>two heaps</strong>:</p>
<ul>
<li>A <strong>max-heap</strong> <code>small</code> for the lower half.</li>
<li>A <strong>min-heap</strong> <code>large</code> for the upper half.</li>
</ul>

<h2>🐢 Brute force first</h2>
<p>Insert each number into a sorted array via binary insertion (<code>bisect.insort</code>) in O(n) time per addition. Query median in O(1). Overall addition time is O(n^2) for n numbers.</p>

<div class="insight">💡 <strong>Key insight:</strong> balance two heaps such that <code>len(small) == len(large)</code> or <code>len(small) == len(large) + 1</code>, and every element in <code>small &lt;=</code> every element in <code>large</code>. Median is either <code>small[0]</code> (odd total) or <code>(small[0] + large[0]) / 2</code> (even total).</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Maintain max-heap <code>small</code> (stores negated values) and min-heap <code>large</code>.</li>
<li><code>addNum(num)</code>: push <code>num</code> to <code>small</code>, then pop maximum of <code>small</code> and push to <code>large</code> (ensures ordering).</li>
<li>If <code>len(large) &gt; len(small)</code>, pop minimum of <code>large</code> and push back to <code>small</code> (ensures <code>small</code> has >= elements).</li>
<li><code>findMedian()</code>: if total elements is odd, return <code>-small[0]</code>; if even, return <code>(-small[0] + large[0]) / 2.0</code>.</li>
</ol>

<h2>🎞️ Visual dry run — add(1), add(2), add(3)</h2>
<pre class="viz">add(1): small=[1], large=[] → median = 1
add(2): push 2 to small → move top to large → small=[1], large=[2] → median = (1+2)/2 = 1.5
add(3): push 3 to small → move top to large → large=[2,3], small=[1]
        balance: move 2 to small → small=[2,1], large=[3] → median = 2 ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>import heapq

class MedianFinder:
    def __init__(self):
        # small is a max-heap (negated values) for the lower half
        self.small = []
        # large is a min-heap for the upper half
        self.large = []

    def addNum(self, num: int) -&gt; None:
        # Step 1: Always route through small to maintain ordering
        heapq.heappush(self.small, -num)
        heapq.heappush(self.large, -heapq.heappop(self.small))
        
        # Step 2: Keep small holding equal or 1 more element than large
        if len(self.large) &gt; len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))

    def findMedian(self) -&gt; float:
        if len(self.small) &gt; len(self.large):
            return float(-self.small[0])
        return (-self.small[0] + self.large[0]) / 2.0</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(log n)</strong> for <code>addNum()</code>, <strong>O(1)</strong> for <code>findMedian()</code>. <strong>Space O(n)</strong> to store all stream elements.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Stream with duplicate values: heaps handle duplicates transparently.</li>
<li>Single element: <code>findMedian()</code> returns that element directly.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Pushing directly to <code>small</code> or <code>large</code> based on length rather than comparing values, violating the invariant that <code>max(small) &lt;= min(large)</code>.</li>
<li>Returning integer division instead of float division when length is even.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Sliding Window Median ([[480]]): remove outgoing window elements from two heaps (requires lazy deletion).</li>
<li>Finding MK Average ([[1825]]): maintaining three partitions (smallest k, middle, largest k).</li>
</ul>''',

# ============================================================ LC 23
23: '''<h2>🧭 How to think about it</h2>
<p>You have <code>k</code> sorted linked lists and want to merge them into one sorted list. At any step, the next node in the merged list must be the <strong>smallest current head</strong> among the k lists. A min-heap containing the current head of each list gives us the minimum in O(log k) time.</p>

<h2>🐢 Brute force first</h2>
<p>Traverse all nodes into an array, sort the array, and reconstruct a linked list → O(N log N) where N is total nodes. Doesn't leverage that lists are already sorted.</p>

<div class="insight">💡 <strong>Key insight:</strong> initialize a <strong>min-heap of size at most k</strong> with the head of each non-empty list. Repeatedly pop the smallest node, attach it to the result, and if that node has a <code>.next</code>, push <code>node.next</code> into the heap.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Create a dummy head <code>dummy = ListNode(0)</code> and <code>curr = dummy</code>.</li>
<li>Push a tuple <code>(node.val, i, node)</code> for each non-empty list head into the min-heap. (The index <code>i</code> acts as a unique tie-breaker to prevent Python from comparing <code>ListNode</code> objects).</li>
<li>While heap is non-empty:</li>
<li>Pop <code>(val, i, node)</code>. Attach <code>curr.next = node</code>, advance <code>curr</code>.</li>
<li>If <code>node.next</code> exists, push <code>(node.next.val, i, node.next)</code>.</li>
<li>Return <code>dummy.next</code>.</li>
</ol>

<h2>🎞️ Visual dry run — lists: [1-&gt;4, 1-&gt;3, 2-&gt;6]</h2>
<pre class="viz">Heap initialized: [(1, 0, n1), (1, 1, n1), (2, 2, n2)]
Pop (1, 0, n1) → append 1 → push (4, 0, n4)
Pop (1, 1, n1) → append 1 → push (3, 1, n3)
Pop (2, 2, n2) → append 2 → push (6, 2, n6)
Pop (3, 1, n3) → append 3
Pop (4, 0, n4) → append 4
Pop (6, 2, n6) → append 6
Result: 1 -&gt; 1 -&gt; 2 -&gt; 3 -&gt; 4 -&gt; 6 ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>import heapq

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def mergeKLists(lists):
    heap = []
    # Push (val, index, node) - index breaks ties when values are equal
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))
            
    dummy = ListNode(0)
    curr = dummy
    
    while heap:
        val, i, node = heapq.heappop(heap)
        curr.next = node
        curr = curr.next
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
            
    return dummy.next</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(N log k)</strong> — where N is the total number of nodes across all k lists. Each of the N nodes is pushed and popped from a heap of size at most k. <strong>Space O(k)</strong> — for the heap of size k.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li><code>lists = []</code>: returns <code>None</code>.</li>
<li><code>lists = [[]]</code>: list contains empty heads, returns <code>None</code>.</li>
<li><code>k = 1</code>: returns the single list directly.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Pushing <code>(node.val, node)</code> without a tiebreaker — Python throws <code>TypeError: '&lt;' not supported between instances of 'ListNode'</code> when two nodes have equal values.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Divide and Conquer approach: merge pairs of lists iteratively in O(N log k) time with O(1) extra space.</li>
<li>Find K Pairs with Smallest Sums ([[373]]).</li>
<li>Smallest Range Covering Elements from K Lists ([[632]]).</li>
</ul>''',

# ============================================================ LC 373
373: '''<h2>🧭 How to think about it</h2>
<p>Given two sorted arrays <code>nums1</code> and <code>nums2</code>, find the <code>k</code> pairs <code>(u, v)</code> with the smallest sums. Think of this as a matrix where cell <code>(i, j)</code> has sum <code>nums1[i] + nums2[j]</code>. Since both arrays are sorted, each row and column is sorted. This is identical to [[23]] Merge k Sorted Lists.</p>

<h2>🐢 Brute force first</h2>
<p>Generate all pairs, sort by sum, return the first k → O(n1 * n2 log(n1 * n2)). Infeasible when n1, n2 = 10^5.</p>

<div class="insight">💡 <strong>Key insight:</strong> start by pushing the first element of each row: <code>(nums1[i] + nums2[0], i, 0)</code> for <code>i &lt; min(k, len(nums1))</code> into a min-heap. When popping <code>(i, j)</code>, the next smallest candidate in that row is <code>(i, j + 1)</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Initialize min-heap with <code>(nums1[i] + nums2[0], i, 0)</code> for <code>i</code> up to <code>min(k, len(nums1))</code>.</li>
<li>While heap is not empty and <code>len(res) &lt; k</code>:</li>
<li>Pop <code>(sum, i, j)</code>, append <code>[nums1[i], nums2[j]]</code> to result.</li>
<li>If <code>j + 1 &lt; len(nums2)</code>, push <code>(nums1[i] + nums2[j+1], i, j + 1)</code>.</li>
<li>Return <code>res</code>.</li>
</ol>

<h2>🎞️ Visual dry run — nums1=[1,7,11], nums2=[2,4,6], k=3</h2>
<pre class="viz">Init heap with (nums1[i]+nums2[0], i, 0):
Heap: [(3, 0, 0), (9, 1, 0), (13, 2, 0)]
1. Pop (3, 0, 0) → pair [1, 2] → push (1+4=5, 0, 1)
Heap: [(5, 0, 1), (9, 1, 0), (13, 2, 0)]
2. Pop (5, 0, 1) → pair [1, 4] → push (1+6=7, 0, 2)
Heap: [(7, 0, 2), (9, 1, 0), (13, 2, 0)]
3. Pop (7, 0, 2) → pair [1, 6] (len == 3 == k, done!)
Result: [[1, 2], [1, 4], [1, 6]] ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>import heapq

def kSmallestPairs(nums1, nums2, k):
    if not nums1 or not nums2 or k &lt;= 0:
        return []
        
    heap = []
    # Seed the heap with the first column (at most k rows)
    for i in range(min(k, len(nums1))):
        heapq.heappush(heap, (nums1[i] + nums2[0], i, 0))
        
    res = []
    while heap and len(res) &lt; k:
        _, i, j = heapq.heappop(heap)
        res.append([nums1[i], nums2[j]])
        # Push the next element in the same row
        if j + 1 &lt; len(nums2):
            heapq.heappush(heap, (nums1[i] + nums2[j + 1], i, j + 1))
            
    return res</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(k log(min(n1, k)))</strong> — at most k elements popped and pushed from a heap of size at most min(n1, k). <strong>Space O(min(n1, k))</strong> — for the heap.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li><code>k &gt; n1 * n2</code>: returns all possible pairs.</li>
<li>Arrays with single elements.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Kth Smallest Element in a Sorted Matrix ([[378]]).</li>
<li>Smallest Range Covering Elements from K Lists ([[632]]).</li>
</ul>''',

# ============================================================ LC 378
378: '''<h2>🧭 How to think about it</h2>
<p>Given an <code>n x n</code> matrix where each row and column is sorted in ascending order, find the kth smallest element. Two optimal ways:</p>
<ol>
<li><strong>Min-Heap</strong>: treat each row as a sorted list, k-way merge until k elements popped (O(k log n)).</li>
<li><strong>Binary Search on Value Range</strong>: search between <code>matrix[0][0]</code> and <code>matrix[n-1][n-1]</code>, counting elements &lt;= mid in O(n) time (O(n log(max - min))).</li>
</ol>

<h2>🐢 Brute force first</h2>
<p>Flatten the matrix into a 1D array, sort it, and return index <code>k - 1</code> → O(n^2 log(n^2)).</p>

<div class="insight">💡 <strong>Key insight (Heap):</strong> push the first element of each row <code>(matrix[r][0], r, 0)</code> into a min-heap. Pop the minimum k-1 times, pushing the next element from that row. The kth popped element is the answer.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Push <code>(matrix[r][0], r, 0)</code> for <code>r</code> in <code>0..min(n, k) - 1</code>.</li>
<li>Loop <code>k - 1</code> times: pop <code>(val, r, c)</code>. If <code>c + 1 &lt; n</code>, push <code>(matrix[r][c + 1], r, c + 1)</code>.</li>
<li>The next popped element's value is the kth smallest.</li>
</ol>

<h2>🎞️ Visual dry run — matrix=[[1,5,9],[10,11,13],[12,13,15]], k=8</h2>
<pre class="viz">Heap init: [(1, 0, 0), (10, 1, 0), (12, 2, 0)]
Pop 1 → push 5 (0, 1)
Pop 5 → push 9 (0, 2)
Pop 9
Pop 10 → push 11 (1, 1)
Pop 11 → push 13 (1, 2)
Pop 12 → push 13 (2, 1)
Pop 13 (from row 1)
8th pop: 13 (from row 2) → result = 13 ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>import heapq

def kthSmallest(matrix, k):
    n = len(matrix)
    # Min-heap of size at most min(n, k)
    heap = []
    for r in range(min(n, k)):
        heapq.heappush(heap, (matrix[r][0], r, 0))
        
    val = 0
    for _ in range(k):
        val, r, c = heapq.heappop(heap)
        if c + 1 &lt; n:
            heapq.heappush(heap, (matrix[r][c + 1], r, c + 1))
            
    return val</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(k log n)</strong> using Min-Heap (or O(n log(max - min)) using Binary Search). <strong>Space O(n)</strong> for the heap.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li><code>k = 1</code>: returns <code>matrix[0][0]</code>.</li>
<li><code>k = n * n</code>: returns <code>matrix[n-1][n-1]</code>.</li>
<li>1x1 matrix.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Find K Pairs with Smallest Sums ([[373]]).</li>
<li>Kth Smallest Number in Multiplication Table ([[668]]).</li>
</ul>''',

# ============================================================ LC 253
253: '''<h2>🧭 How to think about it</h2>
<p>Given an array of meeting time intervals <code>[start, end]</code>, find the <strong>minimum number of conference rooms required</strong>. Two meetings can share a room if the earlier meeting ends before or at the time the next starts. When a new meeting starts, can we reuse a room that just freed up? We only care about the room with the <strong>earliest end time</strong>.</p>

<h2>🐢 Brute force first</h2>
<p>For every meeting, compare with all other rooms to find a conflict-free room; if none, allocate a new room → O(n^2).</p>

<div class="insight">💡 <strong>Key insight:</strong> sort meetings by <code>start_time</code>. Maintain a <strong>min-heap of active meeting end times</strong>. For each meeting, if <code>start &gt;= heap[0]</code>, the earliest room is free—pop it and reuse. Push the current meeting's <code>end_time</code>. The size of the heap is the number of rooms needed.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Sort intervals by <code>start</code> time.</li>
<li>Initialize min-heap <code>rooms = []</code>.</li>
<li>For each interval <code>[start, end]</code>:</li>
<li>If <code>rooms</code> is not empty and <code>start &gt;= rooms[0]</code>, pop the room (it is now free).</li>
<li>Push <code>end</code> onto <code>rooms</code>.</li>
<li>Return <code>len(rooms)</code>.</li>
</ol>

<h2>🎞️ Visual dry run — intervals = [[0,30],[5,10],[15,20]]</h2>
<pre class="viz">Sorted: [[0, 30], [5, 10], [15, 20]]
[0, 30]  → heap: [30] (1 room)
[5, 10]  → 5 &lt; 30 (conflict!) → push 10 → heap: [10, 30] (2 rooms)
[15, 20] → 15 &gt;= 10 (room freed!) → pop 10, push 20 → heap: [20, 30] (2 rooms)
Result: len(heap) = 2 rooms ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>import heapq

def minMeetingRooms(intervals):
    if not intervals:
        return 0
        
    # Sort meetings by start time
    intervals.sort(key=lambda x: x[0])
    
    # Min-heap stores end times of active meetings
    rooms = []
    
    for start, end in intervals:
        # If the earliest ending meeting has finished, reuse that room
        if rooms and start &gt;= rooms[0]:
            heapq.heappop(rooms)
            
        heapq.heappush(rooms, end)
        
    return len(rooms)</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n log n)</strong> — O(n log n) to sort intervals, plus n heap pushes/pops of size at most n. <strong>Space O(n)</strong> — to store end times in the heap.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Non-overlapping meetings: <code>len(rooms)</code> stays 1.</li>
<li>Simultaneous start times: sorted properly, multiple rooms allocated.</li>
<li>Meeting starts exactly when another ends: <code>start == end</code>, room successfully reused.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Two-pointer event sweep approach: separate starts and ends into two sorted arrays.</li>
<li>Meeting Rooms III ([[2402]]): tracking specific room numbers and meeting counts.</li>
</ul>''',

# ============================================================ LC 621
621: '''<h2>🧭 How to think about it</h2>
<p>You have CPU tasks represented by characters, and an idle cooldown <code>n</code> between identical tasks. Find the minimum intervals to complete all tasks. Greedy intuition: always execute the task with the <strong>highest remaining frequency</strong> first, because tasks with high counts require the most cooldown slots.</p>

<h2>🐢 Brute force first</h2>
<p>Simulate execution step by step with a queue tracking cooling tasks → O(total_intervals * log 26).</p>

<div class="insight">💡 <strong>Key insight:</strong> math formula solution. The most frequent task with count <code>max_freq</code> creates <code>max_freq - 1</code> empty chunks of size <code>n</code>. Total slots = <code>(max_freq - 1) * (n + 1) + count_of_max_freq_tasks</code>. The answer is <code>max(len(tasks), formula_result)</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Count frequencies of all tasks using <code>Counter(tasks)</code>.</li>
<li>Find <code>max_freq = max(counts.values())</code>.</li>
<li>Count how many tasks have frequency equal to <code>max_freq</code> (let this be <code>max_count</code>).</li>
<li>Calculate minimum time needed: <code>(max_freq - 1) * (n + 1) + max_count</code>.</li>
<li>Return <code>max(len(tasks), empty_slots_time)</code>.</li>
</ol>

<h2>🎞️ Visual dry run — tasks = ["A","A","A","B","B","B"], n = 2</h2>
<pre class="viz">max_freq = 3 ('A' and 'B' both appear 3 times). max_count = 2 ('A' and 'B').
Chunks:
Chunk 1: A B _ (size 3 = n + 1)
Chunk 2: A B _ (size 3 = n + 1)
Last chunk: A B (size 2 = max_count)
Total: (3 - 1) * (2 + 1) + 2 = 2 * 3 + 2 = 8 intervals: [A, B, idle, A, B, idle, A, B] ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>from collections import Counter

def leastInterval(tasks, n):
    count = Counter(tasks)
    max_freq = max(count.values())
    # Count how many tasks tie for the maximum frequency
    max_count = sum(1 for v in count.values() if v == max_freq)
    
    # Calculate required intervals based on the bottleneck task
    part_time = (max_freq - 1) * (n + 1) + max_count
    # Cannot be less than the total number of tasks
    return max(len(tasks), part_time)</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(N)</strong> — where N is the length of tasks, to count frequencies. <strong>Space O(1)</strong> — alphabet size is at most 26.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li><code>n = 0</code>: no cooldown needed, answer is simply <code>len(tasks)</code>.</li>
<li>Enough other tasks to fill all idle slots: returns <code>len(tasks)</code>.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Reorganize String ([[767]]): n = 1 with distinct adjacent characters.</li>
<li>Single-Threaded CPU ([[1834]]).</li>
</ul>''',

# ============================================================ LC 767
767: '''<h2>🧭 How to think about it</h2>
<p>Rearrange characters in string <code>s</code> so that <strong>no two adjacent characters are identical</strong>. Return "" if impossible. A character appearing more than <code>(len(s) + 1) // 2</code> times can never be separated. Greedily, always pick the character with the <strong>highest remaining frequency</strong> that differs from the previous character.</p>

<h2>🐢 Brute force first</h2>
<p>Backtracking through all permutations checking adjacency → O(n!).</p>

<div class="insight">💡 <strong>Key insight:</strong> use a <strong>max-heap of character frequencies</strong>. Pop the most frequent character. If it matches the previously placed character, pop the second most frequent character instead, place it, and push both back with decremented counts.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Count frequencies. If any <code>count &gt; (len(s) + 1) // 2</code>, return <code>""</code>.</li>
<li>Push <code>(-count, char)</code> into a max-heap.</li>
<li>Initialize <code>res = []</code> and <code>prev = (0, '')</code>.</li>
<li>While heap is not empty:</li>
<li>Pop <code>(cnt, char)</code>. Append <code>char</code> to <code>res</code>.</li>
<li>If <code>prev[0] &lt; 0</code> (still has remaining count), push <code>prev</code> back into the heap.</li>
<li>Set <code>prev = (cnt + 1, char)</code> (decremented count).</li>
<li>Return <code>"".join(res)</code>.</li>
</ol>

<h2>🎞️ Visual dry run — s = "aab"</h2>
<pre class="viz">Counts: {'a': 2, 'b': 1}. len=3, max allowed = (3+1)//2 = 2. Valid!
Heap: [(-2, 'a'), (-1, 'b')]
1. Pop (-2, 'a') → res=['a'] → prev=(-1, 'a')
2. Pop (-1, 'b') → res=['a', 'b'] → push prev (-1, 'a') → prev=(0, 'b')
3. Pop (-1, 'a') → res=['a', 'b', 'a'] → prev=(0, 'a')
Result: "aba" ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>import heapq
from collections import Counter

def reorganizeString(s):
    count = Counter(s)
    if max(count.values()) &gt; (len(s) + 1) // 2:
        return ""
        
    heap = [(-cnt, char) for char, cnt in count.items()]
    heapq.heapify(heap)
    
    res = []
    prev_cnt, prev_char = 0, ''
    
    while heap:
        cnt, char = heapq.heappop(heap)
        res.append(char)
        
        # If the previous character still has remaining count, re-add it to the heap
        if prev_cnt &lt; 0:
            heapq.heappush(heap, (prev_cnt, prev_char))
            
        # Store current character as the waiting previous character
        prev_cnt, prev_char = cnt + 1, char
        
    return "".join(res)</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n log A) = O(n)</strong> — where A is the alphabet size (at most 26), so heap ops are O(1). <strong>Space O(A) = O(1)</strong> for the heap.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Majority character count exceeds threshold: immediately returns <code>""</code>.</li>
<li>Already alternating string (e.g. "abab"): preserved.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Task Scheduler ([[621]]).</li>
<li>Rearrange String k Distance Apart ([[358]]).</li>
</ul>''',

# ============================================================ LC 1834
1834: '''<h2>🧭 How to think about it</h2>
<p>Given tasks with <code>[enqueueTime, processingTime]</code>, a single-threaded CPU picks available tasks. When idle, it takes the earliest arriving task. Among available tasks, it picks the one with the <strong>shortest processing time</strong> (tie-breaker: smallest index). This is the Shortest Job First (SJF) scheduling algorithm.</p>

<h2>🐢 Brute force first</h2>
<p>Scan all tasks at each CPU tick to find available ones and pick the minimum → O(total_time * n), infeasible.</p>

<div class="insight">💡 <strong>Key insight:</strong> sort tasks by <code>enqueueTime</code>. Maintain a <strong>min-heap of available tasks</strong> ordered by <code>(processingTime, originalIndex)</code>. Fast-forward current time <code>time</code> to the next task's enqueue time if the heap is empty.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Store tasks with original indices: <code>tasks = [(eq, proc, i) for i, (eq, proc) in enumerate(tasks)]</code>.</li>
<li>Sort tasks by <code>eq</code> time.</li>
<li>Initialize <code>heap = []</code>, <code>time = 0</code>, <code>i = 0</code>, <code>res = []</code>.</li>
<li>While <code>i &lt; n</code> or <code>heap</code>:</li>
<li>If heap is empty and <code>time &lt; tasks[i][0]</code>, jump <code>time = tasks[i][0]</code>.</li>
<li>Push all tasks with <code>eq &lt;= time</code> into heap as <code>(proc, index)</code>.</li>
<li>Pop <code>(proc, index)</code>, advance <code>time += proc</code>, append <code>index</code> to <code>res</code>.</li>
<li>Return <code>res</code>.</li>
</ol>

<h2>🎞️ Visual dry run — tasks = [[1,2],[2,4],[3,2],[4,1]]</h2>
<pre class="viz">Time=1: task 0 (proc 2) enqueues → heap: [(2, 0)]
Pop task 0 → finishes at time = 1 + 2 = 3. res = [0]
Time=3: tasks 1 (proc 4), 2 (proc 2) enqueued → heap: [(2, 2), (4, 1)]
Pop task 2 (proc 2) → finishes at time = 3 + 2 = 5. res = [0, 2]
Time=5: task 3 (proc 1) enqueued → heap: [(1, 3), (4, 1)]
Pop task 3 (proc 1) → finishes at time = 5 + 1 = 6. res = [0, 2, 3]
Pop task 1 (proc 4) → finishes at time = 6 + 4 = 10. res = [0, 2, 3, 1] ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>import heapq

def getOrder(tasks):
    # Decorate with original index and sort by enqueue time
    indexed_tasks = sorted([(eq, proc, i) for i, (eq, proc) in enumerate(tasks)])
    
    res = []
    heap = []   # stores (processing_time, original_index)
    time = 0
    i = 0
    n = len(tasks)
    
    while i &lt; n or heap:
        # If CPU is idle, advance time to next task arrival
        if not heap and time &lt; indexed_tasks[i][0]:
            time = indexed_tasks[i][0]
            
        # Enqueue all tasks that have arrived by current time
        while i &lt; n and indexed_tasks[i][0] &lt;= time:
            heapq.heappush(heap, (indexed_tasks[i][1], indexed_tasks[i][2]))
            i += 1
            
        # Process task with shortest duration
        proc, idx = heapq.heappop(heap)
        time += proc
        res.append(idx)
        
    return res</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n log n)</strong> — sorting tasks takes O(n log n), and each task is pushed/popped from the heap once in O(log n). <strong>Space O(n)</strong> — for indexed tasks and the heap.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Large gaps between task arrivals: time-jump logic prevents TLE.</li>
<li>Multiple tasks with equal processing times: tie-breaking by original index handled by Python tuple comparison.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Process Tasks Using Servers ([[1882]]).</li>
<li>Meeting Rooms III ([[2402]]).</li>
</ul>''',

# ============================================================ LC 2402
2402: '''<h2>🧭 How to think about it</h2>
<p>You have <code>n</code> rooms numbered <code>0</code> to <code>n - 1</code>. Meetings arrive with <code>[start, end]</code>. Each meeting gets the <strong>lowest-numbered unused room</strong>. If all rooms are busy, it waits for the earliest room to finish (preserving duration). Return the room that held the <strong>most meetings</strong>.</p>

<h2>🐢 Brute force first</h2>
<p>For each meeting, scan all n rooms to check availability; if none, find the room with minimal end time and delay → O(m * n).</p>

<div class="insight">💡 <strong>Key insight:</strong> use <strong>two min-heaps</strong>:</p>
<ul>
<li><code>unused</code>: contains available room numbers <code>0..n-1</code> (min-heap by room index).</li>
<li><code>busy</code>: contains <code>(endTime, roomNumber)</code> (min-heap by end time).</li>
</ul>
<p>For each meeting: free up all rooms whose <code>endTime &lt;= start</code> by popping from <code>busy</code> and pushing to <code>unused</code>. If <code>unused</code> is empty, take the earliest from <code>busy</code> and advance its end time by the meeting's duration.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Sort meetings by <code>start</code> time.</li>
<li>Initialize <code>unused = list(range(n))</code> (heapified) and <code>busy = []</code>. Track <code>counts = [0] * n</code>.</li>
<li>For each <code>start, end</code> in <code>meetings</code>:</li>
<li>While <code>busy</code> and <code>busy[0][0] &lt;= start</code>: pop <code>(_, room)</code> and push <code>room</code> to <code>unused</code>.</li>
<li>If <code>unused</code>: pop smallest room, push <code>(end, room)</code> to <code>busy</code>, increment <code>counts[room]</code>.</li>
<li>Else: pop earliest <code>(earliest_end, room)</code> from <code>busy</code>, push <code>(earliest_end + (end - start), room)</code>, increment <code>counts[room]</code>.</li>
<li>Return the room index with maximum count (tiebreaker: smallest index).</li>
</ol>

<h2>🎞️ Visual dry run — n=2, meetings=[[0,10],[1,5],[2,7],[3,4]]</h2>
<pre class="viz">unused=[0, 1], busy=[]
[0, 10] → room 0 gets it → busy=[(10, 0)], unused=[1]
[1, 5]  → room 1 gets it → busy=[(5, 1), (10, 0)], unused=[]
[2, 7]  → no unused room. Earliest busy finishes at 5 (room 1).
        → delayed to [5, 5+(7-2)=10] → busy=[(10, 0), (10, 1)]
[3, 4]  → no unused room. Earliest finishes at 10 (room 0 wins tiebreaker).
        → delayed to [10, 10+(4-3)=11] → busy=[(10, 1), (11, 0)]
Counts: room 0: 2 meetings, room 1: 2 meetings → tiebreaker room 0 ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>import heapq

def mostBooked(n, meetings):
    meetings.sort()
    
    unused = list(range(n))
    heapq.heapify(unused)
    
    busy = []   # (end_time, room_index)
    count = [0] * n
    
    for start, end in meetings:
        # Free rooms that finished before or at current start time
        while busy and busy[0][0] &lt;= start:
            _, room = heapq.heappop(busy)
            heapq.heappush(unused, room)
            
        duration = end - start
        if unused:
            room = heapq.heappop(unused)
            heapq.heappush(busy, (end, room))
        else:
            # Wait for the earliest room to become free
            earliest_end, room = heapq.heappop(busy)
            heapq.heappush(busy, (earliest_end + duration, room))
            
        count[room] += 1
        
    return count.index(max(count))</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(m log m + m log n)</strong> — where m is number of meetings. Sorting takes O(m log m); each meeting performs O(log n) heap operations. <strong>Space O(n)</strong> — for the two heaps.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Duration overflow if meeting delayed across large time spans: Python handles arbitrarily large integers.</li>
<li>Tiebreaker when multiple rooms have the exact same maximum count: <code>count.index(max(count))</code> naturally returns the smallest index.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Meeting Rooms II ([[253]]).</li>
<li>The Number of the Smallest Unoccupied Chair ([[1942]]).</li>
</ul>''',

# ============================================================ LC 506
506: '''<h2>🧭 How to think about it</h2>
<p>Given athlete scores, assign ranks: 1st is 'Gold Medal', 2nd is 'Silver Medal', 3rd is 'Bronze Medal', and 4th onwards are placement numbers ('4', '5'...). We need athletes sorted by score descending while placing ranks at their original indices. A <strong>max-heap</strong> of <code>(-score, originalIndex)</code> gives the top athletes in order.</p>

<h2>🐢 Brute force first</h2>
<p>Sort a copy of the array descending, look up the rank of each score using <code>score_copy.index(score) + 1</code> → O(n^2).</p>

<div class="insight">💡 <strong>Key insight:</strong> push <code>(-score[i], i)</code> to a max-heap (or sort pairs in O(n log n)). Pop one by one: the 1st gets 'Gold Medal', 2nd 'Silver Medal', 3rd 'Bronze Medal', and remaining get <code>str(rank)</code> placed directly at <code>result[i]</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Create result array <code>res = [""] * len(score)</code>.</li>
<li>Push <code>(-score[i], i)</code> into heap for each index.</li>
<li>Pop in order: track <code>rank = 1, 2, ...</code>.</li>
<li>Assign 'Gold Medal', 'Silver Medal', 'Bronze Medal', or <code>str(rank)</code> to <code>res[i]</code>.</li>
<li>Return <code>res</code>.</li>
</ol>

<h2>🎞️ Visual dry run — score = [10, 3, 8, 9, 4]</h2>
<pre class="viz">Heap: [(-10, 0), (-9, 3), (-8, 2), (-4, 4), (-3, 1)]
Rank 1: score 10 (idx 0) → res[0] = "Gold Medal"
Rank 2: score 9 (idx 3)  → res[3] = "Silver Medal"
Rank 3: score 8 (idx 2)  → res[2] = "Bronze Medal"
Rank 4: score 4 (idx 4)  → res[4] = "4"
Rank 5: score 3 (idx 1)  → res[1] = "5"
Result: ["Gold Medal", "5", "Bronze Medal", "Silver Medal", "4"] ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>import heapq

def findRelativeRanks(score):
    n = len(score)
    res = [""] * n
    heap = [(-s, i) for i, s in enumerate(score)]
    heapq.heapify(heap)
    
    medals = {1: "Gold Medal", 2: "Silver Medal", 3: "Bronze Medal"}
    rank = 1
    
    while heap:
        _, idx = heapq.heappop(heap)
        res[idx] = medals.get(rank, str(rank))
        rank += 1
        
    return res</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n log n)</strong> to heapify and pop all n elements. <strong>Space O(n)</strong> for the heap and result list.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li><code>len(score) &lt; 3</code>: only available medals are assigned.</li>
<li>Single athlete: returns <code>["Gold Medal"]</code>.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Kth Largest Element in an Array ([[215]]).</li>
</ul>''',

# ============================================================ LC 658
658: '''<h2>🧭 How to think about it</h2>
<p>Given a sorted integer array <code>arr</code>, find the <code>k</code> closest integers to <code>x</code>. Closeness is determined by <code>|a - x| &lt; |b - x|</code> (tiebreaker: smaller value). Since <code>arr</code> is sorted, the k closest elements form a <strong>contiguous subarray</strong>. We can use a max-heap of size k, or binary search for the left boundary of the window.</p>

<h2>🐢 Brute force first</h2>
<p>Compute <code>|num - x|</code> for all numbers, sort by distance, slice first k, sort again → O(n log n).</p>

<div class="insight">💡 <strong>Key insight:</strong> the k closest elements in a sorted array must be a contiguous subarray <code>arr[left:left+k]</code>. Binary search for the starting index <code>left</code> between <code>0</code> and <code>len(arr) - k</code> by comparing distances at <code>x - arr[mid]</code> and <code>arr[mid + k] - x</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Binary search range: <code>low = 0, high = len(arr) - k</code>.</li>
<li>While <code>low &lt; high</code>:</li>
<li><code>mid = (low + high) // 2</code>.</li>
<li>If <code>x - arr[mid] &gt; arr[mid + k] - x</code>, <code>arr[mid + k]</code> is closer than <code>arr[mid]</code>, so search right: <code>low = mid + 1</code>.</li>
<li>Else, <code>arr[mid]</code> is closer or tied, so search left: <code>high = mid</code>.</li>
<li>Return <code>arr[low:low + k]</code>.</li>
</ol>

<h2>🎞️ Visual dry run — arr = [1, 2, 3, 4, 5], k = 4, x = 3</h2>
<pre class="viz">Search range: low = 0, high = 5 - 4 = 1
mid = 0: compare x - arr[0] (3 - 1 = 2) vs arr[0 + 4] - x (5 - 3 = 2)
Distances equal (2 == 2) → tiebreaker prefers smaller value (left side) → high = 0
Exit loop: low = 0
Slice arr[0:4] = [1, 2, 3, 4] ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def findClosestElements(arr, k, x):
    # Binary search for the left boundary of the k-length window
    low, high = 0, len(arr) - k
    
    while low &lt; high:
        mid = (low + high) // 2
        # Compare distance of candidate left element vs candidate element right after the window
        if x - arr[mid] &gt; arr[mid + k] - x:
            low = mid + 1    # right side is strictly closer
        else:
            high = mid       # left side is closer or tied
            
    return arr[low:low + k]</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(log(n - k) + k)</strong> — binary search takes O(log(n - k)) and slicing takes O(k). <strong>Space O(1)</strong> extra space.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li><code>x &lt;= arr[0]</code>: returns the first k elements.</li>
<li><code>x &gt;= arr[-1]</code>: returns the last k elements.</li>
<li><code>k == len(arr)</code>: returns the entire array.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>K Closest Points to Origin ([[973]]).</li>
<li>Two-pointer shrink approach from both ends.</li>
</ul>''',

# ============================================================ LC 2558
2558: '''<h2>🧭 How to think about it</h2>
<p>You have gift piles. For <code>k</code> seconds: choose the pile with the <strong>maximum gifts</strong> and replace it with <code>floor(sqrt(gifts))</code>. Return the sum of remaining gifts. At every second, we need the maximum element, so maintain a <strong>max-heap</strong>.</p>

<h2>🐢 Brute force first</h2>
<p>Find the maximum element linearly k times, replace it with its square root → O(k * n). When n, k = 10^5, this results in TLE.</p>

<div class="insight">💡 <strong>Key insight:</strong> negate all pile values and push to a <strong>max-heap</strong>. Each second, pop the maximum <code>m</code>, compute <code>floor(sqrt(m))</code>, and push it back in O(log n). Total time is O(n + k log n).</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Negate elements in <code>gifts</code> and <code>heapify</code> in O(n).</li>
<li>Loop <code>k</code> times:</li>
<li>Pop largest pile <code>val = -heappop(heap)</code>.</li>
<li>Compute <code>remaining = math.isqrt(val)</code>.</li>
<li>Push <code>-remaining</code> into heap.</li>
<li>Return <code>-sum(heap)</code>.</li>
</ol>

<h2>🎞️ Visual dry run — gifts = [25, 64, 9, 4, 100], k = 4</h2>
<pre class="viz">1. Pop 100 → sqrt(100) = 10 → push 10
2. Pop 64  → sqrt(64) = 8   → push 8
3. Pop 25  → sqrt(25) = 5   → push 5
4. Pop 10  → sqrt(10) = 3   → push 3
Remaining: [3, 8, 5, 4, 9], sum = 29 ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>import heapq
import math

def pickGifts(gifts, k):
    # Store negated values to simulate a max-heap in Python
    heap = [-g for g in gifts]
    heapq.heapify(heap)
    
    for _ in range(k):
        max_gift = -heapq.heappop(heap)
        heapq.heappush(heap, -math.isqrt(max_gift))
        
    return -sum(heap)</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n + k log n)</strong> — O(n) to heapify, k heap replacements taking O(log n) each. <strong>Space O(n)</strong> for the heap.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Pile value is 1: <code>isqrt(1) = 1</code>, pile remains 1.</li>
<li><code>k &gt; sum(gifts)</code>: piles reduce to 1 and stay there.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Last Stone Weight ([[1046]]).</li>
<li>Reduce Array Size to The Half ([[1338]]).</li>
</ul>''',

# ============================================================ LC 1825
1825: '''<h2>🧭 How to think about it</h2>
<p>Maintain a stream of numbers. On request, compute the average of the <strong>last m elements after removing the k smallest and k largest</strong>. The window has size <code>m</code>. We need to split the window into three dynamically balanced groups: <code>left</code> (k smallest), <code>mid</code> (m - 2k middle elements), and <code>right</code> (k largest). We maintain a running sum of elements in <code>mid</code> for O(1) average computation.</p>

<h2>🐢 Brute force first</h2>
<p>Sort the last m elements, drop first k and last k, and compute average → O(m log m) per query.</p>

<div class="insight">💡 <strong>Key insight:</strong> use a balanced data structure (like <code>SortedList</code> from <code>sortedcontainers</code> or dual/triple heaps with lazy deletion). Keep <code>mid_sum</code> updated as elements migrate between left, mid, and right partitions. Average is <code>mid_sum // (m - 2k)</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Use a queue to track the last <code>m</code> incoming elements.</li>
<li>Maintain three sorted sets: <code>left</code> (size k), <code>mid</code> (size m - 2k), and <code>right</code> (size k).</li>
<li>Maintain <code>mid_sum</code> for all elements in <code>mid</code>.</li>
<li>On <code>addElement(num)</code>: insert into appropriate set, rebalance sizes, and update <code>mid_sum</code>. When queue size exceeds <code>m</code>, remove the oldest element.</li>
<li>On <code>calculateMKAverage()</code>: if queue length &lt; m, return -1; else return <code>mid_sum // (m - 2*k)</code>.</li>
</ol>

<h2>🎞️ Visual dry run — m = 3, k = 1, stream [3, 1, 10, 5]</h2>
<pre class="viz">Add 3, 1, 10:
Sorted window: [1, 3, 10]
left=[1], mid=[3], right=[10] → mid_sum = 3 → avg = 3 // 1 = 3
Add 5 (drops oldest 3):
Sorted window: [1, 5, 10]
left=[1], mid=[5], right=[10] → mid_sum = 5 → avg = 5 // 1 = 5 ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>from collections import deque
from bisect import insort, bisect_left

class MKAverage:
    def __init__(self, m: int, k: int):
        self.m = m
        self.k = k
        self.q = deque()
        self.sl = []          # sorted list of the m elements
        self.mid_sum = 0

    def addElement(self, num: int) -&gt; None:
        self.q.append(num)
        insort(self.sl, num)
        
        # If queue has reached window size m + 1, evict oldest
        if len(self.q) &gt; self.m:
            oldest = self.q.popleft()
            idx = bisect_left(self.sl, oldest)
            self.sl.pop(idx)
            
        # Recompute mid_sum when window is exactly m
        if len(self.q) == self.m:
            self.mid_sum = sum(self.sl[self.k : self.m - self.k])

    def calculateMKAverage(self) -&gt; int:
        if len(self.q) &lt; self.m:
            return -1
        return self.mid_sum // (self.m - 2 * self.k)</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(m)</strong> insertion with bisect (or O(log m) with balanced Fenwick tree / B-Tree). <strong>O(1)</strong> for <code>calculateMKAverage()</code>. <strong>Space O(m)</strong> to store window elements.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Fewer than <code>m</code> elements in the stream: returns -1.</li>
<li>Duplicate elements: binary search bisect finds correct occurrence.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Find Median from Data Stream ([[295]]).</li>
<li>Sliding Window Median ([[480]]).</li>
</ul>''',

# ============================================================ LC 632
632: '''<h2>🧭 How to think about it</h2>
<p>You have <code>k</code> sorted lists. Find the <strong>smallest range <code>[a, b]</code></strong> that includes at least one number from each of the k lists. Similar to [[23]] Merge k Sorted Lists: keep one pointer in each of the k lists. At any time, the range is <code>[min_val, max_val]</code> of the current k pointers. To shrink the range, the only option is to advance the pointer pointing to <code>min_val</code>.</p>

<h2>🐢 Brute force first</h2>
<p>Check every possible pair <code>[a, b]</code> and verify membership across all k lists → exponential.</p>

<div class="insight">💡 <strong>Key insight:</strong> maintain a <strong>min-heap of size k</strong> containing <code>(val, list_index, element_index)</code> and track the <code>current_max</code>. The current range is <code>[heap[0].val, current_max]</code>. Pop the minimum, record if it is a smaller range, and push the next element from that list. Stop when any list is exhausted.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Initialize min-heap with the first element of each list: <code>(nums[i][0], i, 0)</code>.</li>
<li>Track <code>cur_max = max(nums[i][0] for i in range(k))</code>.</li>
<li>Initialize best range <code>[-inf, inf]</code>.</li>
<li>While <code>len(heap) == k</code>:</li>
<li>Pop <code>min_val, r, c = heappop(heap)</code>.</li>
<li>If <code>cur_max - min_val &lt; best_end - best_start</code>, update best range.</li>
<li>If <code>c + 1 &lt; len(nums[r])</code>: next value is <code>next_val = nums[r][c+1]</code>, update <code>cur_max = max(cur_max, next_val)</code>, push <code>(next_val, r, c + 1)</code>.</li>
<li>Else: list <code>r</code> is exhausted, break loop.</li>
<li>Return <code>[best_start, best_end]</code>.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [[4,10,15],[0,9,12],[5,18,22]]</h2>
<pre class="viz">Init heap: (0, list1), (4, list0), (5, list2). cur_max = 5.
Range: [0, 5] (diff = 5)
Pop 0 → push 9 from list 1 → cur_max = 9. Heap min = 4. Range [4, 9] (diff = 5)
Pop 4 → push 10 from list 0 → cur_max = 10. Heap min = 5. Range [5, 10] (diff = 5)
Pop 5 → push 18 from list 2 → cur_max = 18. Heap min = 9.
Pop 9 → push 12 from list 1 → cur_max = 18. Heap min = 10.
Pop 10 → push 15 from list 0 → cur_max = 18.
Pop 12 → list 1 exhausted → stop!
Best range found: [20, 24] or [24, 28]... Best diff is [20, 24] (diff 4) ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>import heapq

def smallestRange(nums):
    heap = []
    cur_max = -float('inf')
    
    # Initialize heap with the first element from each list
    for r in range(len(nums)):
        val = nums[r][0]
        heapq.heappush(heap, (val, r, 0))
        cur_max = max(cur_max, val)
        
    best_range = [-float('inf'), float('inf')]
    
    while len(heap) == len(nums):
        min_val, r, c = heapq.heappop(heap)
        
        # Check if the current range [min_val, cur_max] is tighter
        if cur_max - min_val &lt; best_range[1] - best_range[0]:
            best_range = [min_val, cur_max]
            
        # Push the next element from the list whose element was just popped
        if c + 1 &lt; len(nums[r]):
            next_val = nums[r][c + 1]
            heapq.heappush(heap, (next_val, r, c + 1))
            cur_max = max(cur_max, next_val)
        else:
            break   # one list is exhausted; cannot form a valid range anymore
            
    return best_range</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(N log k)</strong> — where N is total elements across all lists and k is number of lists. <strong>Space O(k)</strong> — for the heap of size k.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li><code>k = 1</code>: returns <code>[nums[0][0], nums[0][0]]</code> (range of length 0).</li>
<li>Ties in range width: earlier range is preserved.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Merge k Sorted Lists ([[23]]).</li>
<li>Find K Pairs with Smallest Sums ([[373]]).</li>
</ul>''',

# ============================================================ LC 436
436: '''<h2>🧭 How to think about it</h2>
<p>For each interval <code>i</code>, find interval <code>j</code> such that <code>start_j &gt;= end_i</code> with <strong>minimum <code>start_j</code></strong>. Return the index of <code>j</code>, or -1 if none exists. Sorting intervals by their start times allows us to use <strong>binary search</strong> (<code>bisect_left</code>) on the start times in O(n log n) time.</p>

<h2>🐢 Brute force first</h2>
<p>For each interval, scan all other intervals to find the one with minimal valid start time → O(n^2).</p>

<div class="insight">💡 <strong>Key insight:</strong> store <code>(start, original_index)</code> for all intervals and sort them. For each interval's <code>end</code>, binary search the sorted starts for the first start &gt;= <code>end</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Create sorted array of pairs: <code>starts = sorted((it[0], i) for i, it in enumerate(intervals))</code>.</li>
<li>Extract just start times for binary search: <code>start_vals = [s[0] for s in starts]</code>.</li>
<li>For each interval <code>[start, end]</code>:</li>
<li>Use <code>bisect_left(start_vals, end)</code> to find the first start &gt;= <code>end</code>.</li>
<li>If index &lt; n, its original index is <code>starts[idx][1]</code>; else -1.</li>
<li>Return the collected indices.</li>
</ol>

<h2>🎞️ Visual dry run — intervals = [[3,4],[2,3],[1,2]]</h2>
<pre class="viz">starts sorted: [(1, 2), (2, 1), (3, 0)]
start_vals: [1, 2, 3]
interval [3, 4]: bisect(4) → idx 3 &gt;= len → -1
interval [2, 3]: bisect(3) → idx 2 → start=3 (orig idx 0) → 0
interval [1, 2]: bisect(2) → idx 1 → start=2 (orig idx 1) → 1
Result: [-1, 0, 1] ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>from bisect import bisect_left

def findRightInterval(intervals):
    n = len(intervals)
    starts = sorted((it[0], i) for i, it in enumerate(intervals))
    start_vals = [s[0] for s in starts]
    
    res = []
    for it in intervals:
        idx = bisect_left(start_vals, it[1])
        if idx &lt; n:
            res.append(starts[idx][1])
        else:
            res.append(-1)
            
    return res</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n log n)</strong> — sorting starts takes O(n log n), plus n binary searches of O(log n). <strong>Space O(n)</strong> for the starts array.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Interval is its own right interval (e.g. <code>[1, 1]</code>): valid because <code>start &gt;= end</code> (1 &gt;= 1).</li>
<li>No interval starts after an interval ends: returns -1.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Meeting Rooms II ([[253]]).</li>
<li>Non-overlapping Intervals ([[435]]).</li>
</ul>''',

# ============================================================ LC 502
502: '''<h2>🧭 How to think about it</h2>
<p>You have initial capital <code>w</code> and can complete at most <code>k</code> distinct projects. Each project <code>i</code> has pure profit <code>profits[i]</code> and requires minimum capital <code>capital[i]</code>. Greedily, among all projects we can afford (<code>capital &lt;= w</code>), we should always pick the one that gives the <strong>maximum profit</strong>.</p>

<h2>🐢 Brute force first</h2>
<p>In each of the k rounds, scan all projects to find affordable ones and pick the maximum profit → O(k * n).</p>

<div class="insight">💡 <strong>Key insight:</strong> sort projects by <code>capital</code> ascending. Maintain a <strong>max-heap of profits</strong> for all currently affordable projects. Each round, push all newly affordable projects into the heap, pop the maximum profit, and add it to capital <code>w</code>. Repeat k times.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Sort projects by capital: <code>projects = sorted(zip(capital, profits))</code>.</li>
<li>Initialize max-heap <code>available_profits = []</code>.</li>
<li>Track index <code>i = 0</code> in sorted projects.</li>
<li>For <code>_ in range(k)</code>:</li>
<li>While <code>i &lt; n</code> and <code>projects[i][0] &lt;= w</code>: push <code>-projects[i][1]</code> to heap, advance <code>i</code>.</li>
<li>If heap is empty (no affordable projects), break.</li>
<li><code>w += -heappop(available_profits)</code>.</li>
<li>Return <code>w</code>.</li>
</ol>

<h2>🎞️ Visual dry run — k = 2, w = 0, profits = [1,2,3], capital = [0,1,1]</h2>
<pre class="viz">Sorted projects (cap, profit): [(0, 1), (1, 2), (1, 3)]
Round 1 (w = 0):
- Cap 0 &lt;= 0: push profit 1 → heap: [-1]
- Pop 1 → w = 0 + 1 = 1
Round 2 (w = 1):
- Cap 1 &lt;= 1: push profit 2 → heap: [-2]
- Cap 1 &lt;= 1: push profit 3 → heap: [-3, -2]
- Pop 3 → w = 1 + 3 = 4
Result: w = 4 ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>import heapq

def findMaximizedCapital(k, w, profits, capital):
    n = len(profits)
    # Sort projects by required capital ascending
    projects = sorted(zip(capital, profits))
    
    available = []   # max-heap of profits for affordable projects
    i = 0
    
    for _ in range(k):
        # Add all newly affordable projects into the max-heap
        while i &lt; n and projects[i][0] &lt;= w:
            heapq.heappush(available, -projects[i][1])
            i += 1
            
        if not available:
            break    # cannot afford any more projects
            
        # Greedily choose the project with the highest profit
        w += -heapq.heappop(available)
        
    return w</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n log n + k log n)</strong> — sorting takes O(n log n); each project is pushed and popped at most once in O(log n). <strong>Space O(n)</strong> for the projects list and heap.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Capital never enough to start any project: returns initial <code>w</code>.</li>
<li><code>k &gt;= n</code>: all projects that can be afforded will be completed.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Maximum Performance of a Team ([[1383]]).</li>
<li>Course Schedule III ([[630]]).</li>
</ul>''',

# ============================================================ LC 857
857: '''<h2>🧭 How to think about it</h2>
<p>Hire <code>k</code> workers paid in proportion to their quality, satisfying each worker's minimum wage. If we pick a group of workers, the wage is set by the worker with the <strong>highest wage-to-quality ratio</strong> <code>R = max(wage[i] / quality[i])</code>. Total cost is <code>R * sum(qualities)</code>. To minimize cost, for a fixed ratio <code>R</code>, we want the <code>k</code> workers with the <strong>smallest qualities</strong>.</p>

<h2>🐢 Brute force first</h2>
<p>Try every combination of k workers, find max ratio, compute cost → exponential.</p>

<div class="insight">💡 <strong>Key insight:</strong> sort workers by <code>wage / quality</code> ratio ascending. Iterate through workers: maintain a <strong>max-heap of qualities of size k</strong>. When heap size reaches k, compute <code>cost = ratio * quality_sum</code> and keep the minimum. If heap exceeds k, pop the largest quality.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Calculate ratios and sort: <code>workers = sorted([(w / q, q) for w, q in zip(wage, quality)])</code>.</li>
<li>Initialize max-heap <code>qual_heap = []</code>, <code>qual_sum = 0</code>, <code>min_cost = inf</code>.</li>
<li>For each <code>ratio, q</code> in <code>workers</code>:</li>
<li>Push <code>-q</code> to heap, add <code>q</code> to <code>qual_sum</code>.</li>
<li>If <code>len(qual_heap) &gt; k</code>: <code>qual_sum += heappop(qual_heap)</code> (removes largest quality).</li>
<li>If <code>len(qual_heap) == k</code>: <code>min_cost = min(min_cost, ratio * qual_sum)</code>.</li>
<li>Return <code>min_cost</code>.</li>
</ol>

<h2>🎞️ Visual dry run — quality = [10, 20, 5], wage = [70, 50, 30], k = 2</h2>
<pre class="viz">Ratios: worker 0: 70/10 = 7.0, worker 1: 50/20 = 2.5, worker 2: 30/5 = 6.0
Sorted by ratio:
1. (2.5, 20): qual_sum = 20, heap = [20]
2. (6.0, 5):  qual_sum = 25, heap = [20, 5] (size == 2)
   cost = 6.0 * 25 = 150.0. min_cost = 150.0
3. (7.0, 10): push 10 → qual_sum = 35 → pop largest (20) → qual_sum = 15
   heap = [10, 5] (size == 2)
   cost = 7.0 * 15 = 105.0. min_cost = min(150, 105) = 105.0 ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>import heapq

def mincostToHireWorkers(quality, wage, k):
    # Sort workers by wage/quality ratio ascending
    workers = sorted([(w / q, q) for w, q in zip(wage, quality)])
    
    max_heap = []   # stores negative qualities to easily evict the largest
    qual_sum = 0
    min_cost = float('inf')
    
    for ratio, q in workers:
        heapq.heappush(max_heap, -q)
        qual_sum += q
        
        # Keep only k workers with the smallest qualities
        if len(max_heap) &gt; k:
            qual_sum += heapq.heappop(max_heap)   # heappop returns negative q
            
        if len(max_heap) == k:
            min_cost = min(min_cost, ratio * qual_sum)
            
    return min_cost</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n log n)</strong> — O(n log n) to sort workers, plus n heap operations of size k (O(n log k)). <strong>Space O(n)</strong> for sorted workers and heap.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li><code>k = 1</code>: simply pick the worker with minimal wage.</li>
<li><code>k = n</code>: all workers hired, cost is <code>max(ratios) * sum(qualities)</code>.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Maximum Performance of a Team ([[1383]]).</li>
<li>IPO ([[502]]).</li>
</ul>''',

# ============================================================ LC 1167
1167: '''<h2>🧭 How to think about it</h2>
<p>Connect sticks of lengths <code>sticks</code> into one. Cost to connect two sticks of lengths <code>x</code> and <code>y</code> is <code>x + y</code>. We want the <strong>minimum total cost</strong>. Notice that sticks connected earlier contribute repeatedly to future connection costs. Therefore, we should greedily connect the <strong>two smallest sticks</strong> first (classic Huffman Coding algorithm).</p>

<h2>🐢 Brute force first</h2>
<p>Try all possible pairing orders → exponential.</p>

<div class="insight">💡 <strong>Key insight:</strong> use a <strong>min-heap</strong>. Repeatedly pop the two smallest sticks <code>a</code> and <code>b</code>, add <code>a + b</code> to total cost, and push <code>a + b</code> back into the heap until one stick remains.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Heapify <code>sticks</code> in O(n).</li>
<li>Initialize <code>total_cost = 0</code>.</li>
<li>While <code>len(sticks) &gt; 1</code>:</li>
<li><code>a = heappop(sticks)</code>, <code>b = heappop(sticks)</code>.</li>
<li><code>cost = a + b</code>, <code>total_cost += cost</code>.</li>
<li><code>heappush(sticks, cost)</code>.</li>
<li>Return <code>total_cost</code>.</li>
</ol>

<h2>🎞️ Visual dry run — sticks = [2, 4, 3]</h2>
<pre class="viz">Heap: [2, 4, 3]
1. Pop 2 and 3 → cost = 5 → total_cost = 5 → push 5 → Heap: [4, 5]
2. Pop 4 and 5 → cost = 9 → total_cost = 5 + 9 = 14 → push 9 → Heap: [9]
One stick left. Result: 14 ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>import heapq

def connectSticks(sticks):
    heapq.heapify(sticks)
    total_cost = 0
    
    while len(sticks) &gt; 1:
        first = heapq.heappop(sticks)
        second = heapq.heappop(sticks)
        cost = first + second
        total_cost += cost
        heapq.heappush(sticks, cost)
        
    return total_cost</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n log n)</strong> — n - 1 connections, each performing O(log n) heap operations. <strong>Space O(1)</strong> auxiliary if heapified in-place.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Single stick: already connected, cost = 0.</li>
<li>All sticks equal length: pairs merge symmetrically.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Last Stone Weight ([[1046]]).</li>
<li>Huffman Coding algorithm.</li>
</ul>''',

# ============================================================ LC 1383
1383: '''<h2>🧭 How to think about it</h2>
<p>Given <code>n</code> engineers with speeds and efficiencies, choose at most <code>k</code> engineers to maximize performance: <code>sum(speed) * min(efficiency)</code>. Since performance is bounded by the minimum efficiency, if we fix an engineer as the bottleneck efficiency, we should greedily pick the fastest engineers whose efficiencies are &gt;= this bottleneck.</p>

<h2>🐢 Brute force first</h2>
<p>Examine all subsets of size up to k → combinatorial explosion.</p>

<div class="insight">💡 <strong>Key insight:</strong> sort engineers by <strong>efficiency descending</strong>. For each engineer, consider them as the minimum efficiency. Maintain a <strong>min-heap of speeds of size at most k</strong>. If heap exceeds k, pop the smallest speed. Track the maximum <code>speed_sum * efficiency</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Sort engineers by efficiency descending: <code>engineers = sorted(zip(efficiency, speed), reverse=True)</code>.</li>
<li>Initialize min-heap <code>speed_heap = []</code>, <code>speed_sum = 0</code>, <code>max_perf = 0</code>.</li>
<li>For each <code>eff, spd</code> in <code>engineers</code>:</li>
<li>Push <code>spd</code> to heap, add <code>spd</code> to <code>speed_sum</code>.</li>
<li>If <code>len(speed_heap) &gt; k</code>: <code>speed_sum -= heappop(speed_heap)</code>.</li>
<li>Update <code>max_perf = max(max_perf, speed_sum * eff)</code>.</li>
<li>Return <code>max_perf % (10^9 + 7)</code>.</li>
</ol>

<h2>🎞️ Visual dry run — n=6, speed=[2,10,3,1,5,8], efficiency=[5,4,3,9,7,2], k=2</h2>
<pre class="viz">Sorted (eff, spd): [(9, 1), (7, 5), (5, 2), (4, 10), (3, 3), (2, 8)]
1. (9, 1): heap=[1], sum=1 → perf = 1 * 9 = 9
2. (7, 5): heap=[1, 5], sum=6 → perf = 6 * 7 = 42
3. (5, 2): push 2 → pop 1 → heap=[2, 5], sum=7 → perf = 7 * 5 = 35
4. (4, 10): push 10 → pop 2 → heap=[5, 10], sum=15 → perf = 15 * 4 = 60 (max!)
5. (3, 3): push 3 → pop 3 → heap=[5, 10], sum=15 → perf = 15 * 3 = 45
6. (2, 8): push 8 → pop 5 → heap=[8, 10], sum=18 → perf = 18 * 2 = 36
Result: max = 60 ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>import heapq

def maxPerformance(n, speed, efficiency, k):
    # Sort engineers by efficiency descending
    engineers = sorted(zip(efficiency, speed), reverse=True)
    
    speed_heap = []   # min-heap storing speeds of chosen engineers
    speed_sum = 0
    max_perf = 0
    MOD = 10**9 + 7
    
    for eff, spd in engineers:
        heapq.heappush(speed_heap, spd)
        speed_sum += spd
        
        # Keep at most k engineers (discard the slowest)
        if len(speed_heap) &gt; k:
            speed_sum -= heapq.heappop(speed_heap)
            
        max_perf = max(max_perf, speed_sum * eff)
        
    return max_perf % MOD</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n log n)</strong> — sorting takes O(n log n), plus n heap operations of size k (O(n log k)). <strong>Space O(n)</strong> for sorted engineers and heap.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li><code>k = 1</code>: simply finds max <code>speed[i] * efficiency[i]</code>.</li>
<li>Modulo arithmetic: apply modulo only at the very end to prevent intermediate precision comparison bugs.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Minimum Cost to Hire K Workers ([[857]]).</li>
<li>IPO ([[502]]).</li>
</ul>''',

# ============================================================ LC 1642
1642: '''<h2>🧭 How to think about it</h2>
<p>You have buildings with heights, <code>bricks</code>, and <code>ladders</code>. Moving from building <code>i</code> to <code>i + 1</code>: if height decreases or stays same, 0 cost; if height increases by <code>diff</code>, use 1 ladder OR <code>diff</code> bricks. Ladders can cover ANY height difference, no matter how tall. Greedily, ladders should be reserved for the <strong>largest height climbs</strong>.</p>

<h2>🐢 Brute force first</h2>
<p>Backtracking DFS: at each climb, try either ladder or bricks → O(2^n).</p>

<div class="insight">💡 <strong>Key insight:</strong> use a <strong>min-heap of size at most ladders</strong>. For every climb, assume we use a ladder and push <code>diff</code> to the heap. When climbs exceed available ladders, pop the smallest climb from the heap and pay for it with bricks. If bricks drop below 0, we can go no further.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Initialize min-heap <code>ladder_climbs = []</code>.</li>
<li>For <code>i</code> from <code>0</code> to <code>len(heights) - 2</code>:</li>
<li><code>diff = heights[i + 1] - heights[i]</code>.</li>
<li>If <code>diff &gt; 0</code>: push <code>diff</code> to heap.</li>
<li>If <code>len(ladder_climbs) &gt; ladders</code>: pop smallest climb and deduct from <code>bricks</code>.</li>
<li>If <code>bricks &lt; 0</code>: return <code>i</code> (cannot make this climb).</li>
<li>If loop completes, return <code>len(heights) - 1</code>.</li>
</ol>

<h2>🎞️ Visual dry run — heights=[4,2,7,6,9,14,12], bricks=5, ladders=1</h2>
<pre class="viz">i=0: 4-&gt;2 (down)
i=1: 2-&gt;7 (diff 5): heap=[5] (size 1 &lt;= 1 ladder)
i=2: 7-&gt;6 (down)
i=3: 6-&gt;9 (diff 3): push 3 → heap=[3, 5] &gt; 1 ladder → pop 3 → bricks = 5 - 3 = 2. heap=[5]
i=4: 9-&gt;14 (diff 5): push 5 → heap=[5, 5] &gt; 1 ladder → pop 5 → bricks = 2 - 5 = -3 &lt; 0!
Stop at building 4 ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>import heapq

def furthestBuilding(heights, bricks, ladders):
    ladder_allocations = []   # min-heap tracking climbs covered by ladders
    
    for i in range(len(heights) - 1):
        diff = heights[i + 1] - heights[i]
        if diff &gt; 0:
            heapq.heappush(ladder_allocations, diff)
            # If we used more ladders than available, convert the smallest climb to bricks
            if len(ladder_allocations) &gt; ladders:
                bricks -= heapq.heappop(ladder_allocations)
            if bricks &lt; 0:
                return i
                
    return len(heights) - 1</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n log L)</strong> — where n is number of buildings and L is number of ladders. <strong>Space O(L)</strong> for the heap.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Decreasing heights throughout: reaches the final building with 0 resource usage.</li>
<li>0 ladders: all climbs paid with bricks.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Minimum Cost to Connect Sticks ([[1167]]).</li>
<li>Binary Search on furthest reachable building.</li>
</ul>''',

# ============================================================ LC 1792
1792: '''<h2>🧭 How to think about it</h2>
<p>You have classes with <code>[pass, total]</code> and <code>extraStudents</code> who always pass. Assign extra students to maximize the average pass ratio. Greedily, each extra student should be assigned to the class where they provide the <strong>greatest marginal increase</strong> in pass ratio: <code>gain = (pass + 1)/(total + 1) - pass/total</code>.</p>

<h2>🐢 Brute force first</h2>
<p>For each of the extra students, compute gains across all classes and pick maximum → O(extraStudents * n).</p>

<div class="insight">💡 <strong>Key insight:</strong> use a <strong>max-heap</strong> storing <code>(-gain, pass, total)</code>. Each student is assigned to the class at the root. Pop the class, increment <code>pass</code> and <code>total</code>, recalculate its new gain, and push it back.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Define gain helper: <code>gain(p, t) = (p + 1) / (t + 1) - p / t</code>.</li>
<li>Push <code>(-gain(p, t), p, t)</code> into heap for each class.</li>
<li>Repeat <code>extraStudents</code> times:</li>
<li>Pop <code>(-g, p, t)</code>.</li>
<li>Push <code>(-gain(p + 1, t + 1), p + 1, t + 1)</code>.</li>
<li>Return <code>sum(p / t for _, p, t in heap) / len(classes)</code>.</li>
</ol>

<h2>🎞️ Visual dry run — classes = [[1,2],[3,5],[2,2]], extra = 2</h2>
<pre class="viz">Gains:
[1, 2]: 2/3 - 1/2 = 0.1667
[3, 5]: 4/6 - 3/5 = 0.0667
[2, 2]: 3/3 - 2/2 = 0.0000
1. Assign to [1, 2] → becomes [2, 3] (new gain: 3/4 - 2/3 = 0.0833)
2. Highest gain is now [2, 3] (0.0833 &gt; 0.0667) → becomes [3, 4]
Final ratios: 3/4 (0.75), 3/5 (0.6), 2/2 (1.0)
Average = (0.75 + 0.6 + 1.0) / 3 = 0.78333 ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>import heapq

def maxAverageRatio(classes, extraStudents):
    def gain(p, t):
        return (p + 1) / (t + 1) - p / t
        
    heap = [(-gain(p, t), p, t) for p, t in classes]
    heapq.heapify(heap)
    
    for _ in range(extraStudents):
        g, p, t = heapq.heappop(heap)
        p, t = p + 1, t + 1
        heapq.heappush(heap, (-gain(p, t), p, t))
        
    return sum(p / t for _, p, t in heap) / len(classes)</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n + k log n)</strong> — where n is number of classes and k is extraStudents. <strong>Space O(n)</strong> for the heap.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Classes with 100% pass ratio (e.g. <code>[5, 5]</code>): gain is 0, pushed to bottom of heap.</li>
<li><code>extraStudents = 0</code>: returns current average.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Kth Largest Element in an Array ([[215]]).</li>
<li>Dijkstra's shortest path priority updates.</li>
</ul>''',

# ============================================================ LC 1845
1845: '''<h2>🧭 How to think about it</h2>
<p>Design a system that manages <code>n</code> seats numbered <code>1</code> to <code>n</code>. <code>reserve()</code> fetches the <strong>smallest-numbered unreserved seat</strong>. <code>unreserve(seatNumber)</code> releases a seat back to available. A <strong>min-heap</strong> provides instant O(log n) access to the smallest available seat.</p>

<h2>🐢 Brute force first</h2>
<p>Boolean array of reserved flags. Linear scan for the first <code>False</code> on <code>reserve()</code> → O(n) per reservation.</p>

<div class="insight">💡 <strong>Key insight:</strong> initialize a <strong>min-heap</strong> with numbers <code>1..n</code>. <code>reserve()</code> pops <code>heappop(heap)</code> in O(log n); <code>unreserve(seat)</code> pushes <code>heappush(heap, seat)</code> in O(log n).</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Initialize <code>heap = list(range(1, n + 1))</code> and heapify.</li>
<li><code>reserve()</code>: return <code>heappop(self.heap)</code>.</li>
<li><code>unreserve(seatNumber)</code>: <code>heappush(self.heap, seatNumber)</code>.</li>
</ol>

<h2>🎞️ Visual dry run — n = 5</h2>
<pre class="viz">Init heap: [1, 2, 3, 4, 5]
reserve()   → pops 1
reserve()   → pops 2
unreserve(2)→ pushes 2 → heap: [2, 3, 4, 5]
reserve()   → pops 2 (smallest available seat!)
reserve()   → pops 3 ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>import heapq

class SeatManager:
    def __init__(self, n: int):
        self.available = list(range(1, n + 1))
        heapq.heapify(self.available)

    def reserve(self) -> int:
        return heapq.heappop(self.available)

    def unreserve(self, seatNumber: int) -> None:
        heapq.heappush(self.available, seatNumber)</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> initialization; <strong>O(log n)</strong> per <code>reserve()</code> and <code>unreserve()</code> call. <strong>Space O(n)</strong> for the heap.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Repeated reserves and unreserves: heap guarantees monotonic smallest-seat extraction.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>The Number of the Smallest Unoccupied Chair ([[1942]]).</li>
<li>Meeting Rooms III ([[2402]]).</li>
</ul>''',

# ============================================================ LC 1882
1882: '''<h2>🧭 How to think about it</h2>
<p>You have <code>n</code> servers with weights and <code>m</code> tasks with execution times. At second <code>j</code>, task <code>j</code> arrives. Available servers are chosen by <strong>smallest weight</strong> (tiebreaker: smallest index). If no server is free, tasks wait in queue until a server frees up. We need two heaps: <strong>free servers</strong> (ordered by weight, index) and <strong>busy servers</strong> (ordered by finish time).</p>

<h2>🐢 Brute force first</h2>
<p>Scan all servers at each second to check availability and assign → O(total_time * n).</p>

<div class="insight">💡 <strong>Key insight:</strong> use <strong>two min-heaps</strong>: <code>free_servers</code> <code>(weight, index)</code> and <code>busy_servers</code> <code>(finish_time, weight, index)</code>. Fast-forward current time to the earliest finish time when no servers are available.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Initialize <code>free = [(servers[i], i) for i in range(n)]</code> and heapify.</li>
<li>Initialize <code>busy = []</code> (min-heap by finish time).</li>
<li>For each task <code>j</code> arriving at time <code>j</code>:</li>
<li>Time <code>cur_time = max(cur_time, j)</code>. If <code>free</code> is empty, fast-forward <code>cur_time = busy[0][0]</code>.</li>
<li>Move all servers from <code>busy</code> with <code>finish_time &lt;= cur_time</code> back to <code>free</code>.</li>
<li>Pop server <code>(w, i)</code> from <code>free</code>.</li>
<li>Push <code>(cur_time + tasks[j], w, i)</code> to <code>busy</code>.</li>
<li>Record <code>i</code> in result.</li>
<li>Return result.</li>
</ol>

<h2>🎞️ Visual dry run — servers = [3,3,2], tasks = [1,2,3,2,1,2]</h2>
<pre class="viz">free: [(2, 2), (3, 0), (3, 1)], busy: []
t=0, task 0 (dur 1): assign to (2, 2) → busy=[(1, 2, 2)]. res=[2]
t=1, task 1 (dur 2): server 2 frees up! free=[(2, 2), (3, 0), (3, 1)].
                     assign to (2, 2) → busy=[(3, 2, 2)]. res=[2, 2]
t=2, task 2 (dur 3): assign to (3, 0) → busy=[(3, 2, 2), (5, 3, 0)]. res=[2, 2, 0] ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>import heapq

def assignTasks(servers, tasks):
    # free: (weight, index)
    free = [(w, i) for i, w in enumerate(servers)]
    heapq.heapify(free)
    
    # busy: (finish_time, weight, index)
    busy = []
    
    res = []
    cur_time = 0
    
    for j, duration in enumerate(tasks):
        cur_time = max(cur_time, j)
        
        # If no servers are available, jump time forward to when the first server frees up
        if not free:
            cur_time = busy[0][0]
            
        # Free up all servers that have finished by cur_time
        while busy and busy[0][0] &lt;= cur_time:
            _, w, i = heapq.heappop(busy)
            heapq.heappush(free, (w, i))
            
        w, i = heapq.heappop(free)
        res.append(i)
        heapq.heappush(busy, (cur_time + duration, w, i))
        
    return res</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O((n + m) log n)</strong> — each task pushes and pops from the heaps in O(log n). <strong>Space O(n + m)</strong> for the heaps and result array.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>More tasks than servers: time fast-forward ensures no idle CPU spinning.</li>
<li>Equal weights: broken by original server index.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Single-Threaded CPU ([[1834]]).</li>
<li>Meeting Rooms III ([[2402]]).</li>
</ul>''',

# ============================================================ LC 1942
1942: '''<h2>🧭 How to think about it</h2>
<p>Friends arrive and leave at distinct times <code>[arrival, leaving]</code>. When a friend arrives, they sit in the <strong>smallest unoccupied chair</strong> (chairs numbered <code>0, 1, 2...</code>). Find which chair <code>targetFriend</code> sits on. We need to track available chairs (min-heap) and busy friends (min-heap by leaving time).</p>

<h2>🐢 Brute force first</h2>
<p>Simulate each second, linear scan for empty chair → O(max_time * n).</p>

<div class="insight">💡 <strong>Key insight:</strong> tag each friend with their index: <code>(arr, leave, i)</code> and sort by arrival time. Use <strong>two min-heaps</strong>: <code>free_chairs</code> (chair numbers <code>0..n-1</code>) and <code>busy</code> <code>(leaving_time, chair)</code>. When friend arrives, free all chairs of friends who left, and take the smallest available chair.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Tag friends with indices and sort by arrival: <code>events = sorted([(times[i][0], times[i][1], i) for i in range(len(times))])</code>.</li>
<li>Initialize <code>free_chairs = list(range(len(times)))</code> and heapify.</li>
<li>Initialize <code>busy = []</code> (min-heap of <code>(leaving_time, chair)</code>).</li>
<li>For each <code>arr, leave, idx</code>:</li>
<li>While <code>busy</code> and <code>busy[0][0] &lt;= arr</code>: pop <code>(_, chair)</code> and push <code>chair</code> to <code>free_chairs</code>.</li>
<li>Pop smallest <code>chair = heappop(free_chairs)</code>.</li>
<li>If <code>idx == targetFriend</code>: return <code>chair</code>.</li>
<li>Push <code>(leave, chair)</code> to <code>busy</code>.</li>
</ol>

<h2>🎞️ Visual dry run — times = [[1,4],[2,3],[4,6]], targetFriend = 1</h2>
<pre class="viz">Friends sorted by arrival: [1, 4] (idx 0), [2, 3] (idx 1), [4, 6] (idx 2)
free_chairs: [0, 1, 2]
Friend 0 arrives at 1: sits on chair 0 → busy=[(4, 0)]
Friend 1 arrives at 2: sits on chair 1 → busy=[(3, 1), (4, 0)]
Friend 1 is targetFriend! Return chair 1 ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>import heapq

def smallestChair(times, targetFriend):
    target_arrival = times[targetFriend][0]
    # Sort friends by arrival time
    events = sorted([(arr, leave, i) for i, (arr, leave) in enumerate(times)])
    
    free_chairs = list(range(len(times)))
    heapq.heapify(free_chairs)
    
    busy = []   # (leaving_time, chair)
    
    for arr, leave, i in events:
        # Free chairs of friends who have departed
        while busy and busy[0][0] &lt;= arr:
            _, chair = heapq.heappop(busy)
            heapq.heappush(free_chairs, chair)
            
        chair = heapq.heappop(free_chairs)
        if i == targetFriend:
            return chair
            
        heapq.heappush(busy, (leave, chair))
        
    return -1</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n log n)</strong> — sorting events takes O(n log n); each friend performs O(log n) heap operations. <strong>Space O(n)</strong> for the heaps.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Target friend is the first to arrive: returns chair 0.</li>
<li>Departure and arrival at the same time: departure happens first, so the chair is immediately available for the arriving friend.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Meeting Rooms II ([[253]]).</li>
<li>Meeting Rooms III ([[2402]]).</li>
</ul>''',

}
