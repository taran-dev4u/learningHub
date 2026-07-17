# Deep tutorials — Pattern P5: Sliding Window (Session 5).
# Keyed by LC number; merged as (5, lc). [[nn]] -> links via build.py.

DEEP = {

# ============================================================ LC 346 — Moving Average from Data Stream
346: '''
<h2>🧭 How to think about it</h2>
<p>Numbers arrive one at a time; each call returns the average of the <strong>last k</strong>. Keep a fixed-size window: a queue of the most recent values plus a running sum. When the window overflows, drop the oldest and subtract it — no re-summing.</p>

<h2>🐢 Brute force first</h2>
<p>Store every value and average the last k on each call → O(k) per call. A running sum makes each call O(1).</p>

<div class="insight">💡 <strong>Key insight:</strong> maintain <code>window_sum</code>. On <code>next(v)</code>: add <code>v</code>; if the queue exceeds <code>k</code>, pop the front and subtract it. The average is <code>window_sum / len(queue)</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Store <code>size = k</code>, a deque, and <code>window_sum = 0</code>.</li>
<li><code>next(v)</code>: append <code>v</code>, add to sum; if over capacity, pop-left and subtract.</li>
<li>Return <code>window_sum / len(deque)</code>.</li>
</ol>

<h2>🎞️ Visual dry run — k=3, stream 1,10,3,5</h2>
<pre class="viz">1 → [1] sum1 avg 1
10 → [1,10] sum11 avg 5.5
3 → [1,10,3] sum14 avg 4.667
5 → drop 1 → [10,3,5] sum18 avg 6</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>from collections import deque
class MovingAverage:
    def __init__(self, size):
        self.size = size
        self.q = deque()
        self.window_sum = 0

    def next(self, val):
        self.q.append(val)
        self.window_sum += val
        if len(self.q) &gt; self.size:
            self.window_sum -= self.q.popleft()   # evict the oldest
        return self.window_sum / len(self.q)</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(1)</strong> per call. <strong>Space O(k)</strong> for the window.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Fewer than k values so far → average over what's present.</li>
<li>k = 1 → returns the latest value.</li>
<li>Negative values → running sum still works.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Re-summing the window each call (O(k)).</li>
<li>Dividing by <code>k</code> instead of the current count before the window fills.</li>
<li>Forgetting to subtract the evicted value.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Moving median → two heaps.</li>
<li>Compressed/weighted mean over a window ([[2985]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[643]] · [[2985]] · [[239]]</p>
''',

# ============================================================ LC 643 — Maximum Average Subarray I
643: '''
<h2>🧭 How to think about it</h2>
<p>Find the length-<code>k</code> contiguous block with the largest average. Since every candidate has the same length <code>k</code>, maximizing the average is the same as maximizing the <strong>sum</strong>. Slide a fixed window of size <code>k</code>, updating the sum in O(1) per step.</p>

<h2>🐢 Brute force first</h2>
<p>Sum each window from scratch → O(n·k). The rolling sum (add the new element, drop the one that left) makes it O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> compute the first window's sum, then for each slide do <code>sum += nums[r] − nums[r−k]</code>. Track the maximum sum and divide by <code>k</code> at the end.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Sum the first <code>k</code> elements; set <code>best = that sum</code>.</li>
<li>For <code>r</code> from <code>k</code> to <code>n−1</code>: <code>sum += nums[r] − nums[r−k]</code>; update <code>best</code>.</li>
<li>Return <code>best / k</code>.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [1,12,-5,-6,50,3], k = 4</h2>
<pre class="viz">first 4: 1+12-5-6 = 2
slide: 2 -1 +50 = ... window[12,-5,-6,50]=51 (best)
window[-5,-6,50,3]=42
best sum 51 → avg 12.75</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def findMaxAverage(nums, k):
    window = sum(nums[:k])
    best = window
    for r in range(k, len(nums)):
        window += nums[r] - nums[r - k]     # add new, drop old
        best = max(best, window)
    return best / k</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — one pass after the initial sum. <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>k = n → one window, the whole array.</li>
<li>All negatives → the least-negative window wins.</li>
<li>k = 1 → the max element.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Comparing averages (float) instead of sums (int) — unnecessary and error-prone.</li>
<li>Off-by-one in <code>nums[r−k]</code>.</li>
<li>Initializing <code>best</code> to 0 and failing on all-negative input.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Variable-length max average → binary search on the answer.</li>
<li>Streaming moving average ([[346]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[346]] · [[2985]] · [[209]]</p>
''',

# ============================================================ LC 995 — Minimum Number of K Consecutive Bit Flips
995: '''
<h2>🧭 How to think about it</h2>
<p>Each move flips a fixed-length block of <code>k</code> consecutive bits; make the whole array all 1s with the fewest moves. Scan left to right: the leftmost 0 you meet <em>must</em> be fixed by a flip starting exactly there (nothing to its left can touch it anymore). Track the running effect of past flips so you know each bit's current value in O(1).</p>

<h2>🐢 Brute force first</h2>
<p>Actually flipping k bits per move is O(n·k) or worse. A <strong>difference array</strong> (or a queue of flip end-points) records how many flips are currently affecting the position, giving O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> keep a running <code>flips</code> parity. A position's real value is <code>nums[i] XOR (flips % 2)</code>. If it's 0, we must start a flip here — but only if <code>i + k ≤ n</code>; otherwise it's impossible (−1). Use a <code>diff</code> array to cancel a flip's effect once you pass its end.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Maintain <code>flips</code> (active flip parity) and a <code>diff</code> array.</li>
<li>At <code>i</code>: subtract <code>diff[i]</code> from <code>flips</code>. If <code>(nums[i] + flips) % 2 == 0</code>, flip here.</li>
<li>Flipping: if <code>i + k &gt; n</code> return −1; else <code>flips += 1</code>, count++, and mark <code>diff[i+k] += 1</code>.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [0,1,0], k = 1</h2>
<pre class="viz">i0 val0 → flip (count1) ; i1 val1 ok ; i2 val0 → flip (count2)
Answer: 2</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def minKBitFlips(nums, k):
    n = len(nums)
    diff = [0] * (n + 1)
    flips = 0                      # active flips affecting current index (parity)
    count = 0
    for i in range(n):
        flips += diff[i]
        if (nums[i] + flips) % 2 == 0:      # current effective bit is 0
            if i + k &gt; n:
                return -1                    # can't place a full flip
            count += 1
            flips += 1
            diff[i + k] -= 1                 # this flip stops affecting here
    return count</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — one pass. <strong>Space O(n)</strong> for the diff array (O(1) possible with a queue of endpoints).</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Already all 1s → 0 flips.</li>
<li>A trailing 0 within <code>k</code> of the end that needs flipping → −1.</li>
<li>k = n → at most one flip decides everything.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Literally flipping bits (too slow).</li>
<li>Forgetting the impossibility check <code>i + k &gt; n</code>.</li>
<li>Mismanaging the diff/parity so the running effect is wrong.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Bulb switcher / range-toggle problems use the same diff-parity idea.</li>
<li>Minimum flips with variable block size → harder.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[1004]] · [[239]] · [[1109]]</p>
''',

# ============================================================ LC 1004 — Max Consecutive Ones III
1004: '''
<h2>🧭 How to think about it</h2>
<p>You may flip at most <code>k</code> zeros to ones; find the longest run of 1s you can create. Reframed: find the <strong>longest window containing at most k zeros</strong>. Grow the window on the right; whenever it holds more than <code>k</code> zeros, shrink from the left until it's valid again.</p>

<h2>🐢 Brute force first</h2>
<p>Check every subarray's zero count → O(n²). The sliding window does it in O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> track <code>zeros</code> in the window. Expand <code>right</code>; if <code>zeros &gt; k</code>, advance <code>left</code> (decrementing <code>zeros</code> when it passes a zero). The window is always the longest valid one ending at <code>right</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>left = 0</code>, <code>zeros = 0</code>, <code>best = 0</code>.</li>
<li>For each <code>right</code>: if <code>nums[right] == 0</code>, <code>zeros += 1</code>.</li>
<li>While <code>zeros &gt; k</code>: if <code>nums[left] == 0</code> decrement; <code>left += 1</code>.</li>
<li><code>best = max(best, right − left + 1)</code>.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [1,1,0,0,1,1,1,0,1], k = 2</h2>
<pre class="viz">window grows to include two 0s ; a third 0 shrinks from left
longest valid window length = 6 (e.g., indices 2..7 with two flips)
Answer: 6</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def longestOnes(nums, k):
    left = zeros = best = 0
    for right in range(len(nums)):
        if nums[right] == 0:
            zeros += 1
        while zeros &gt; k:                 # too many zeros → shrink
            if nums[left] == 0:
                zeros -= 1
            left += 1
        best = max(best, right - left + 1)
    return best</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — each index enters and leaves the window once. <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>k ≥ number of zeros → the whole array.</li>
<li>k = 0 → longest existing run of 1s.</li>
<li>All zeros → answer is <code>min(k, n)</code>.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Shrinking with <code>if</code> instead of <code>while</code> (fine here since zeros grows by 1, but <code>while</code> is the safe habit).</li>
<li>Decrementing <code>zeros</code> for non-zero left elements.</li>
<li>Off-by-one in the window length.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Longest subarray of 1s after deleting exactly one element ([[1493]]).</li>
<li>Longest repeating character replacement ([[424]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[1493]] · [[424]] · [[3]]</p>
''',

# ============================================================ LC 2985 — Calculate Compressed Mean
2985: '''
<h2>🧭 How to think about it</h2>
<p>Order values stream in; each query wants the mean of the most recent <code>k</code> of them. This is the moving-average pattern: keep a fixed window of the last <code>k</code> values with a <strong>running sum</strong>, so each update and query is O(1).</p>

<h2>🐢 Brute force first</h2>
<p>Re-sum the last k on every query → O(k). A running sum plus a bounded queue makes it O(1) per update.</p>

<div class="insight">💡 <strong>Key insight:</strong> a deque capped at <code>k</code> holds the current window; adding a value that overflows evicts the oldest and subtracts it from the running sum. The compressed mean is <code>window_sum / count</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Keep a deque and <code>window_sum</code>.</li>
<li>On a new order value, push it and add to the sum; evict the front if over <code>k</code>.</li>
<li>Report <code>window_sum / len(window)</code>.</li>
</ol>

<h2>🎞️ Visual dry run — k=2, values 4,6,10</h2>
<pre class="viz">4 → [4] mean 4
6 → [4,6] mean 5
10 → drop 4 → [6,10] mean 8</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>from collections import deque
class CompressedMean:
    def __init__(self, k):
        self.k = k
        self.q = deque()
        self.total = 0

    def add(self, value):
        self.q.append(value)
        self.total += value
        if len(self.q) &gt; self.k:
            self.total -= self.q.popleft()
        return self.total / len(self.q)</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(1)</strong> per operation. <strong>Space O(k)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Fewer than k values → mean over what exists.</li>
<li>k = 1 → always the latest value.</li>
<li>Empty window queried → guard (or return 0).</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Recomputing the sum every query.</li>
<li>Dividing by k before the window fills.</li>
<li>Forgetting to subtract the evicted value.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Weight by quantity (true compressed/weighted mean) → track two running totals.</li>
<li>Moving average from a stream ([[346]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[346]] · [[643]] · [[239]]</p>
''',

# ============================================================ LC 3254 — Find the Power of K-Size Subarrays I
3254: '''
<h2>🧭 How to think about it</h2>
<p>For every window of size <code>k</code>, its "power" is the window's last value if the whole window is <strong>consecutive ascending</strong> (each element is exactly one more than the previous), otherwise <code>−1</code>. Track how long the current ascending-by-one run is; a window qualifies when that run covers the entire window.</p>

<h2>🐢 Brute force first</h2>
<p>Re-check each window for consecutiveness → O(n·k). Maintaining a run length makes it O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> keep <code>run</code> = the length of the current maximal streak where <code>nums[i] == nums[i−1] + 1</code>. At index <code>i</code> (the window's right end, for <code>i ≥ k−1</code>), the window is fully consecutive iff <code>run ≥ k</code>; then power is <code>nums[i]</code>, else <code>−1</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Walk the array tracking <code>run</code> (reset to 1 on a break, else +1).</li>
<li>Once <code>i ≥ k−1</code>, output <code>nums[i]</code> if <code>run ≥ k</code>, else <code>−1</code>.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [1,2,3,4,3,2,5], k = 3</h2>
<pre class="viz">runs: 1,2,3,4 then break at 3 (run1),2(run1? 2!=3+1)→1, 5(run? 5!=2+1)→1
windows(right idx 2..6): [1,2,3]run3→3 ; [2,3,4]run4→4 ; [3,4,3]run1→-1 ; [4,3,2]→-1 ; [3,2,5]→-1
Result: [3,4,-1,-1,-1]</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def resultsArray(nums, k):
    n = len(nums)
    res = []
    run = 1
    for i in range(n):
        if i &gt; 0 and nums[i] == nums[i - 1] + 1:
            run += 1
        else:
            run = 1                       # streak broken
        if i &gt;= k - 1:
            res.append(nums[i] if run &gt;= k else -1)
    return res</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — one pass. <strong>Space O(1)</strong> beyond the output.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>k = 1 → every window is trivially "consecutive"; power is the element itself.</li>
<li>Strictly ascending array → all powers are the window ends.</li>
<li>No consecutive run of length k → all <code>−1</code>.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Resetting <code>run</code> to 0 instead of 1 on a break.</li>
<li>Emitting before the first full window (<code>i ≥ k−1</code>).</li>
<li>Checking equality instead of "previous + 1".</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Any monotonic condition → track the corresponding run.</li>
<li>x-sum of windows ([[3318]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[3318]] · [[643]] · [[239]]</p>
''',

# ============================================================ LC 3318 — Find X-Sum of All K-Long Subarrays I
3318: '''
<h2>🧭 How to think about it</h2>
<p>For each window of size <code>k</code>, rank distinct values by <strong>frequency</strong> (ties broken by larger value), keep the top <code>x</code> of them, and sum each kept value times its count. The "I" variant has small limits, so you can honestly recompute each window's counts and pick the top <code>x</code>.</p>

<h2>🐢 Brute force first</h2>
<p>For every window, count values, sort by (frequency, value), take the top <code>x</code>, and sum. With small <code>n</code> and <code>k</code> that's acceptable — O(n · k log k).</p>

<div class="insight">💡 <strong>Key insight:</strong> the score of a value is <code>count × value</code>, but the <em>selection</em> is by <code>(count, value)</code>. Sort the window's distinct entries by that key descending, take <code>x</code>, and sum their <code>count × value</code>. If fewer than <code>x</code> distinct values exist, include them all.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>For each window, build a <code>Counter</code>.</li>
<li>Sort items by <code>(count, value)</code> descending; take the first <code>x</code>.</li>
<li>Sum <code>value × count</code> over those; append to the result.</li>
</ol>

<h2>🎞️ Visual dry run — window counts {1:3, 2:2, 3:1}, x=2</h2>
<pre class="viz">rank by (freq,value): (3,1)&gt;(2,2)&gt;(1,3)
top2: value1×3=3, value2×2=4 → x-sum 7</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>from collections import Counter
def findXSum(nums, k, x):
    res = []
    for i in range(len(nums) - k + 1):
        cnt = Counter(nums[i:i + k])
        # sort by frequency then value, both descending
        top = sorted(cnt.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)[:x]
        res.append(sum(val * c for val, c in top))
    return res</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n · k log k)</strong> — a fresh count and sort per window. <strong>Space O(k)</strong>. (The hard variant needs ordered multisets for O(n log k).)</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Distinct values in a window ≤ x → sum them all.</li>
<li>Ties in frequency → the larger value is preferred.</li>
<li>k = n → a single window.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Ranking by value only, ignoring frequency (or vice versa).</li>
<li>Summing selection keys instead of <code>value × count</code>.</li>
<li>Handling ties in the wrong direction.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Large limits → maintain two ordered multisets (top-x and the rest) across slides.</li>
<li>Top-k frequent elements ([[347]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[3254]] · [[239]] · [[347]]</p>
''',

# ============================================================ LC 3 — Longest Substring Without Repeating Characters
3: '''
<h2>🧭 How to think about it</h2>
<p>Find the longest substring with all-unique characters. Slide a window; when a character repeats, <strong>jump the left edge</strong> past the previous occurrence of that character so the window is valid again. A map of each character's last index makes the jump O(1).</p>

<h2>🐢 Brute force first</h2>
<p>Check every substring for uniqueness → O(n²) or worse. The sliding window with a last-seen map is O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> keep <code>last[c]</code> = the most recent index of character <code>c</code>. When <code>c</code> reappears inside the window, move <code>left</code> to <code>max(left, last[c] + 1)</code> — never backward. The best length is <code>right − left + 1</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>left = 0</code>, empty <code>last</code> map, <code>best = 0</code>.</li>
<li>For each <code>right</code>, if <code>s[right]</code> was seen at ≥ <code>left</code>, jump <code>left</code>.</li>
<li>Record <code>last[s[right]] = right</code>; update <code>best</code>.</li>
</ol>

<h2>🎞️ Visual dry run — s = "abcabcbb"</h2>
<pre class="viz">a,b,c window "abc" len3 ; next a → jump left past first a → "bca" ; ...
best length = 3</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def lengthOfLongestSubstring(s):
    last = {}
    left = best = 0
    for right, c in enumerate(s):
        if c in last and last[c] &gt;= left:
            left = last[c] + 1           # jump past the previous occurrence
        last[c] = right
        best = max(best, right - left + 1)
    return best</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — each index visited once. <strong>Space O(min(n, alphabet))</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Empty string → 0.</li>
<li>All identical → best length 1.</li>
<li>All distinct → the whole string.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Moving <code>left</code> backward — guard with <code>last[c] &gt;= left</code>.</li>
<li>Not updating <code>last[c]</code> every step.</li>
<li>Counting length as <code>right − left</code> (missing the +1).</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>At most k distinct characters ([[340]]).</li>
<li>Longest with at most two distinct → fruit baskets ([[904]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[340]] · [[904]] · [[76]]</p>
''',

# ============================================================ LC 76 — Minimum Window Substring
76: '''
<h2>🧭 How to think about it</h2>
<p>Find the shortest window of <code>s</code> that contains every character of <code>t</code> (with multiplicity). Grow the window until it's <strong>valid</strong> (covers all of <code>t</code>), then shrink from the left while it stays valid, recording the smallest. A <code>need</code>/<code>have</code> counting scheme tells you validity in O(1).</p>

<h2>🐢 Brute force first</h2>
<p>Check every window against <code>t</code> → O(n²·|t|). The expand-then-contract window with counts is O(n + m).</p>

<div class="insight">💡 <strong>Key insight:</strong> <code>need</code> = required counts from <code>t</code>; <code>formed</code> = how many distinct required characters are currently satisfied. Expand <code>right</code>, incrementing <code>formed</code> when a character's count reaches its need. When <code>formed == required</code>, contract <code>left</code>, recording the window, until it breaks validity.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Build <code>need</code> from <code>t</code>; track <code>window</code> counts, <code>formed</code>.</li>
<li>Expand <code>right</code>; when a char meets its need, <code>formed += 1</code>.</li>
<li>While valid, update the best window and shrink <code>left</code> (decrement <code>formed</code> when a need breaks).</li>
</ol>

<h2>🎞️ Visual dry run — s = "ADOBECODEBANC", t = "ABC"</h2>
<pre class="viz">first valid window "ADOBEC" → shrink to "BEC"? invalid ... eventually "BANC" (len4) is smallest
Answer: "BANC"</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>from collections import Counter
def minWindow(s, t):
    if not t or not s:
        return ""
    need = Counter(t)
    required = len(need)
    window = {}
    formed = 0
    left = 0
    best = (float('inf'), 0, 0)          # (length, l, r)
    for right, c in enumerate(s):
        window[c] = window.get(c, 0) + 1
        if c in need and window[c] == need[c]:
            formed += 1
        while formed == required:         # valid → try to shrink
            if right - left + 1 &lt; best[0]:
                best = (right - left + 1, left, right)
            lc = s[left]
            window[lc] -= 1
            if lc in need and window[lc] &lt; need[lc]:
                formed -= 1
            left += 1
    return "" if best[0] == float('inf') else s[best[1]:best[2] + 1]</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(|s| + |t|)</strong> — each character enters and leaves once. <strong>Space O(|alphabet|)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>No valid window → empty string.</li>
<li><code>t</code> longer than <code>s</code> → empty.</li>
<li>Duplicate characters in <code>t</code> → multiplicities matter.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Incrementing <code>formed</code> on every occurrence instead of only when the exact need is met.</li>
<li>Forgetting to shrink while still valid.</li>
<li>Comparing distinct-character coverage without counts.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Fixed-size anagram windows ([[438]], [[567]]).</li>
<li>Smallest window covering all distinct characters of <code>s</code> itself.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[438]] · [[567]] · [[3]]</p>
''',

# ============================================================ LC 209 — Minimum Size Subarray Sum
209: '''
<h2>🧭 How to think about it</h2>
<p>Find the shortest contiguous subarray whose sum is at least <code>target</code> (all values positive). Grow a window on the right, adding to a running sum; the moment the sum reaches <code>target</code>, <strong>shrink from the left</strong> as far as possible while still ≥ target, recording the length.</p>

<h2>🐢 Brute force first</h2>
<p>Try all subarrays → O(n²). Because values are positive, a sliding window is O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> positivity means adding elements only grows the sum and removing only shrinks it — so a two-pointer window monotonically finds the shortest valid length ending at each right edge.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>left = 0</code>, <code>total = 0</code>, <code>best = ∞</code>.</li>
<li>Add each <code>nums[right]</code>. While <code>total ≥ target</code>: update <code>best</code> and subtract <code>nums[left]</code>, advancing <code>left</code>.</li>
<li>Return <code>best</code> (0 if never reached).</li>
</ol>

<h2>🎞️ Visual dry run — nums = [2,3,1,2,4,3], target = 7</h2>
<pre class="viz">grow to [2,3,1,2] sum8 ≥7 → shrink [3,1,2]sum6 stop len4
… window [4,3] sum7 → len2 (best)
Answer: 2</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def minSubArrayLen(target, nums):
    left = total = 0
    best = float('inf')
    for right in range(len(nums)):
        total += nums[right]
        while total &gt;= target:            # shrink while still valid
            best = min(best, right - left + 1)
            total -= nums[left]
            left += 1
    return 0 if best == float('inf') else best</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — each element added and removed once. <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>No subarray reaches target → 0.</li>
<li>A single element ≥ target → length 1.</li>
<li>Whole array needed → length n.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Using a window when negatives are present (breaks monotonicity — use prefix sums / deque instead, [[862]]).</li>
<li>Recording the length after shrinking too far.</li>
<li>Returning ∞ instead of 0.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Negatives allowed → [[862]] (deque over prefix sums).</li>
<li>Exact sum → prefix-sum map ([[560]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[862]] · [[3]] · [[76]]</p>
''',

# ============================================================ LC 219 — Contains Duplicate II
219: '''
<h2>🧭 How to think about it</h2>
<p>Return true if some value repeats within a distance of <code>k</code> indices. Keep a <strong>sliding window of the last k</strong> values in a set; if the incoming value is already in that set, you've found a close duplicate.</p>

<h2>🐢 Brute force first</h2>
<p>Compare every pair within k → O(n·k). A window set makes each check O(1), total O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> maintain a set of the values at indices <code>[i−k, i−1]</code>. Before adding <code>nums[i]</code>, evict <code>nums[i−k−1]</code> so the set only holds the last <code>k</code>. A hit means a duplicate within range.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Iterate with index <code>i</code>, keeping a set <code>window</code>.</li>
<li>If <code>nums[i]</code> is in <code>window</code> → return True.</li>
<li>Add it; if <code>i ≥ k</code>, remove <code>nums[i−k]</code>.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [1,2,3,1], k = 3</h2>
<pre class="viz">i0 add1 ; i1 add2 ; i2 add3 ; i3 val1 in window → True</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def containsNearbyDuplicate(nums, k):
    window = set()
    for i, x in enumerate(nums):
        if x in window:
            return True                   # duplicate within k
        window.add(x)
        if i &gt;= k:
            window.remove(nums[i - k])     # keep only the last k
    return False</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong>, <strong>Space O(min(n, k))</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>k = 0 → no window; always false.</li>
<li>Duplicate exactly k apart → still within range (indices differ by ≤ k).</li>
<li>Large k → the set can hold up to k elements.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Evicting at the wrong time (must remove <code>nums[i−k]</code> after adding).</li>
<li>Using a dict of last indices and comparing distance incorrectly.</li>
<li>Off-by-one on the window size.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Value-difference version (Contains Duplicate III) → bucketing or ordered set.</li>
<li>Any duplicate anywhere (Contains Duplicate) → a plain set.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[3]] · [[340]] · [[567]]</p>
''',

# ============================================================ LC 340 — Longest Substring with At Most K Distinct Characters
340: '''
<h2>🧭 How to think about it</h2>
<p>Find the longest substring using at most <code>k</code> distinct characters. Slide a window with a <strong>count map</strong>; whenever the number of distinct characters exceeds <code>k</code>, shrink from the left until it's back to <code>k</code>.</p>

<h2>🐢 Brute force first</h2>
<p>Check every substring's distinct count → O(n²). The window with a frequency map is O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> the map's size is the current distinct count. Expand <code>right</code>; while <code>len(map) &gt; k</code>, decrement <code>s[left]</code> and delete it when its count hits 0, advancing <code>left</code>. Track the max window length.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Expand <code>right</code>, incrementing <code>count[s[right]]</code>.</li>
<li>While <code>len(count) &gt; k</code>: decrement <code>count[s[left]]</code>, drop it at 0, <code>left += 1</code>.</li>
<li>Update <code>best</code>.</li>
</ol>

<h2>🎞️ Visual dry run — s = "eceba", k = 2</h2>
<pre class="viz">"ece" 2 distinct len3 ; add b → 3 distinct → shrink to "ceb"? still 3 → "eb" 2 distinct
best length = 3</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def lengthOfLongestSubstringKDistinct(s, k):
    count = {}
    left = best = 0
    for right, c in enumerate(s):
        count[c] = count.get(c, 0) + 1
        while len(count) &gt; k:             # too many distinct
            lc = s[left]
            count[lc] -= 1
            if count[lc] == 0:
                del count[lc]
            left += 1
        best = max(best, right - left + 1)
    return best</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong>, <strong>Space O(k)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>k = 0 → 0.</li>
<li>k ≥ distinct characters → the whole string.</li>
<li>Empty string → 0.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Not deleting a key at count 0 (map size stays wrong).</li>
<li>Using <code>if</code> instead of <code>while</code> to shrink.</li>
<li>Off-by-one length.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Exactly k distinct → atMost(k) − atMost(k−1) ([[992]]).</li>
<li>At most two distinct → fruit baskets ([[904]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[904]] · [[992]] · [[3]]</p>
''',

# ============================================================ LC 424 — Longest Repeating Character Replacement
424: '''
<h2>🧭 How to think about it</h2>
<p>You may replace up to <code>k</code> characters; find the longest substring that can become all one letter. A window is achievable when the number of characters that <em>aren't</em> the window's most frequent letter is ≤ <code>k</code> — because those are the ones you'd replace.</p>

<h2>🐢 Brute force first</h2>
<p>Try each window and each target letter → O(n²·26). Tracking the window's max letter frequency gives O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> a window of length <code>L</code> is valid if <code>L − maxFreq ≤ k</code> (replace the non-majority letters). Grow <code>right</code>; if the window becomes invalid, slide <code>left</code> by one. Notably <code>maxFreq</code> never needs to decrease — the answer only grows when a genuinely better window appears.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Count letters in the window; track <code>maxFreq</code>.</li>
<li>If <code>(right − left + 1) − maxFreq &gt; k</code>, decrement <code>count[s[left]]</code> and advance <code>left</code>.</li>
<li>The answer is the largest window length seen.</li>
</ol>

<h2>🎞️ Visual dry run — s = "AABABBA", k = 1</h2>
<pre class="viz">window "AABA" maxFreq(A)=3, len4, 4-3=1 ≤1 valid
extend "AABAB" len5 maxFreq3 → 5-3=2 &gt;1 → slide left
best window length = 4</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def characterReplacement(s, k):
    count = {}
    left = maxFreq = best = 0
    for right, c in enumerate(s):
        count[c] = count.get(c, 0) + 1
        maxFreq = max(maxFreq, count[c])
        if (right - left + 1) - maxFreq &gt; k:   # too many to replace
            count[s[left]] -= 1
            left += 1
        best = max(best, right - left + 1)
    return best</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong>, <strong>Space O(26)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>k ≥ length → the whole string.</li>
<li>All same letter → length n (no replacements needed).</li>
<li>Empty string → 0.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Trying to recompute <code>maxFreq</code> exactly after shrinking (unnecessary; a stale-but-monotone max still yields the correct answer).</li>
<li>Shrinking with a <code>while</code> that recomputes max (over-engineering).</li>
<li>Off-by-one window length.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Max consecutive ones with k flips ([[1004]]).</li>
<li>Longest subarray after one deletion ([[1493]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[1004]] · [[1493]] · [[3]]</p>
''',

# ============================================================ LC 713 — Subarray Product Less Than K
713: '''
<h2>🧭 How to think about it</h2>
<p>Count contiguous subarrays whose product is strictly less than <code>k</code> (all values positive). Slide a window keeping the running <strong>product</strong>; whenever it reaches <code>k</code> or more, shrink from the left. Each valid right end contributes <code>right − left + 1</code> new subarrays.</p>

<h2>🐢 Brute force first</h2>
<p>All subarray products → O(n²). Positivity lets a sliding window count them in O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> for a window <code>[left, right]</code> with product &lt; k, every subarray ending at <code>right</code> and starting anywhere in <code>[left, right]</code> is valid — that's <code>right − left + 1</code> of them. Add that each step.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>If <code>k ≤ 1</code>, return 0 (no positive product is &lt; 1).</li>
<li>Multiply in <code>nums[right]</code>; while product ≥ k, divide out <code>nums[left]</code> and advance.</li>
<li>Add <code>right − left + 1</code> to the count.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [10,5,2,6], k = 100</h2>
<pre class="viz">10 → +1 ; 10*5=50 → +2 ; 50*2=100 ≥100 → shrink to [5,2] prod10 → +2 ; *6=60 → +3
total = 8</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def numSubarrayProductLessThanK(nums, k):
    if k &lt;= 1:
        return 0
    prod = 1
    left = count = 0
    for right, x in enumerate(nums):
        prod *= x
        while prod &gt;= k:                  # shrink until valid
            prod //= nums[left]
            left += 1
        count += right - left + 1         # subarrays ending at right
    return count</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong>, <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>k ≤ 1 → 0 (products of positives are ≥ 1).</li>
<li>Single element ≥ k → contributes nothing.</li>
<li>All products &lt; k → n(n+1)/2 subarrays.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Using <code>≤</code> instead of <code>&lt;</code> (strictly less than).</li>
<li>Forgetting the <code>k ≤ 1</code> guard (division/logic breaks).</li>
<li>Applying this to arrays with zeros or negatives (window logic fails).</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Sum less than k with positives → same counting shape.</li>
<li>Exactly k distinct integers ([[992]]) uses the atMost trick.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[209]] · [[992]] · [[3]]</p>
''',

# ============================================================ LC 904 — Fruit Into Baskets
904: '''
<h2>🧭 How to think about it</h2>
<p>You walk a row of fruit trees and can carry only <strong>two types</strong> total, picking one fruit per tree until you'd need a third type. This is exactly "longest subarray with at most 2 distinct values" — a sliding window with a count map capped at size 2.</p>

<h2>🐢 Brute force first</h2>
<p>Try every starting tree and walk until a third type → O(n²). The window solves it in O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> it's [[340]] with <code>k = 2</code>. Expand the window; when a third fruit type appears, shrink from the left until only two types remain. The answer is the longest such window.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Count fruit types in the window.</li>
<li>While more than 2 types, shrink from the left (drop a type at count 0).</li>
<li>Track the max window length.</li>
</ol>

<h2>🎞️ Visual dry run — fruits = [1,2,3,2,2]</h2>
<pre class="viz">[1,2] ok ; add 3 → 3 types → shrink past 1 → [2,3] ; extend [2,3,2,2] 2 types len4
Answer: 4</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def totalFruit(fruits):
    count = {}
    left = best = 0
    for right, f in enumerate(fruits):
        count[f] = count.get(f, 0) + 1
        while len(count) &gt; 2:             # only two baskets
            lf = fruits[left]
            count[lf] -= 1
            if count[lf] == 0:
                del count[lf]
            left += 1
        best = max(best, right - left + 1)
    return best</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong>, <strong>Space O(1)</strong> (at most 3 keys).</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>One fruit type → the whole row.</li>
<li>Two types → the whole row.</li>
<li>Alternating three types → short windows.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Not deleting a type when its count reaches 0.</li>
<li>Capping the count of fruits instead of the number of types.</li>
<li>Off-by-one window length.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>At most k types ([[340]]).</li>
<li>Longest without repeats ([[3]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[340]] · [[3]] · [[992]]</p>
''',

# ============================================================ LC 992 — Subarrays with K Different Integers
992: '''
<h2>🧭 How to think about it</h2>
<p>Count subarrays with <em>exactly</em> <code>k</code> distinct integers. "Exactly k" is awkward for a single window, but "<strong>at most k</strong>" is easy — so compute <code>atMost(k) − atMost(k−1)</code>. The difference leaves precisely the subarrays with exactly <code>k</code> distinct values.</p>

<h2>🐢 Brute force first</h2>
<p>Count distinct in every subarray → O(n²). Two at-most sliding windows give O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> <code>atMost(k)</code> counts subarrays with ≤ k distinct by a standard window: for each right end, add <code>right − left + 1</code> valid subarrays. Subtracting <code>atMost(k−1)</code> removes those with fewer than k, leaving exactly k.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Write <code>atMost(k)</code>: window with a count map, shrink while distinct &gt; k, add window length each step.</li>
<li>Return <code>atMost(k) − atMost(k−1)</code>.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [1,2,1,2,3], k = 2</h2>
<pre class="viz">atMost(2) = 12 ; atMost(1) = 5 ; exactly 2 = 12 − 5 = 7</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def subarraysWithKDistinct(nums, k):
    def at_most(m):
        count = {}
        left = res = 0
        for right, x in enumerate(nums):
            count[x] = count.get(x, 0) + 1
            while len(count) &gt; m:
                count[nums[left]] -= 1
                if count[nums[left]] == 0:
                    del count[nums[left]]
                left += 1
            res += right - left + 1        # subarrays ending at right
        return res
    return at_most(k) - at_most(k - 1)</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — two linear passes. <strong>Space O(k)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>k greater than the number of distinct values → 0.</li>
<li>k = 1 → count of single-value runs' subarrays.</li>
<li>All identical → only k = 1 yields results.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Trying to enforce "exactly k" in one window (hard); use the difference.</li>
<li>Off-by-one between <code>atMost(k)</code> and <code>atMost(k−1)</code>.</li>
<li>Not deleting zero-count keys.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Binary subarrays with sum ([[930]]) uses the same at-most trick.</li>
<li>At most k distinct ([[340]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[340]] · [[930]] · [[904]]</p>
''',

# ============================================================ LC 1438 — Longest Continuous Subarray With Absolute Diff <= Limit
1438: '''
<h2>🧭 How to think about it</h2>
<p>Find the longest subarray where the difference between its maximum and minimum is at most <code>limit</code>. A plain window can't cheaply know its current max and min — so maintain <strong>two monotonic deques</strong>: one giving the window max, one the window min. When <code>max − min</code> exceeds the limit, shrink from the left.</p>

<h2>🐢 Brute force first</h2>
<p>Recompute max/min per window → O(n²). Two monotonic deques keep both in O(1) amortized, so the whole thing is O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> a decreasing deque's front is the window max; an increasing deque's front is the window min. Push each new value (popping smaller/larger from the back). If <code>maxDeque.front − minDeque.front &gt; limit</code>, advance <code>left</code>, expiring indices that fall out of the window.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Maintain <code>maxd</code> (decreasing) and <code>mind</code> (increasing) deques of indices.</li>
<li>Push <code>right</code>; while the front difference &gt; limit, move <code>left</code> and pop expired fronts.</li>
<li>Track the best window length.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [8,2,4,7], limit = 4</h2>
<pre class="viz">[8] ok ; [8,2] max8 min2 diff6 &gt;4 → shrink to [2] ; [2,4] diff2 ; [2,4,7] max7 min2 diff5 &gt;4 → shrink to [4,7]
best length = 2</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>from collections import deque
def longestSubarray(nums, limit):
    maxd, mind = deque(), deque()     # indices; maxd decreasing, mind increasing
    left = best = 0
    for right, x in enumerate(nums):
        while maxd and nums[maxd[-1]] &lt;= x: maxd.pop()
        while mind and nums[mind[-1]] &gt;= x: mind.pop()
        maxd.append(right); mind.append(right)
        while nums[maxd[0]] - nums[mind[0]] &gt; limit:   # window invalid
            left += 1
            if maxd[0] &lt; left: maxd.popleft()
            if mind[0] &lt; left: mind.popleft()
        best = max(best, right - left + 1)
    return best</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — each index enters/leaves each deque once. <strong>Space O(n)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>All equal → whole array (diff 0).</li>
<li>limit = 0 → longest run of a single repeated value.</li>
<li>Single element → length 1.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Storing values instead of indices (can't expire by position).</li>
<li>Forgetting to pop expired fronts as <code>left</code> advances.</li>
<li>Wrong monotonic direction on a deque.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Count "continuous" subarrays with max−min ≤ 2 ([[2762]]).</li>
<li>Sliding window maximum ([[239]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[2762]] · [[239]] · [[3]]</p>
''',

# ============================================================ LC 1493 — Longest Subarray of 1's After Deleting One Element
1493: '''
<h2>🧭 How to think about it</h2>
<p>You must delete exactly one element; find the longest run of 1s afterward. Equivalently, find the <strong>longest window containing at most one 0</strong> — that 0 (or one element if the array is all 1s) is what you delete. The answer is the window length minus 1 (the deleted slot).</p>

<h2>🐢 Brute force first</h2>
<p>Try deleting each index and measure → O(n²). A window with at most one 0 is O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> slide a window allowing one 0. When a second 0 enters, shrink past the first 0. Every valid window contributes <code>length − 1</code> ones after the mandatory deletion.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Grow <code>right</code>, counting zeros.</li>
<li>While <code>zeros &gt; 1</code>, advance <code>left</code> (decrementing on a passed 0).</li>
<li>Track <code>best = max(best, right − left)</code> (length − 1).</li>
</ol>

<h2>🎞️ Visual dry run — nums = [1,1,0,1]</h2>
<pre class="viz">window [1,1,0,1] one 0 len4 → ones after delete = 3
Answer: 3</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def longestSubarray(nums):
    left = zeros = best = 0
    for right, x in enumerate(nums):
        if x == 0:
            zeros += 1
        while zeros &gt; 1:                  # at most one zero allowed
            if nums[left] == 0:
                zeros -= 1
            left += 1
        best = max(best, right - left)    # minus the deleted element
    return best</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong>, <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>All 1s → you must still delete one → <code>n − 1</code>.</li>
<li>All 0s → 0.</li>
<li>Single element → 0.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Returning the window length instead of <code>length − 1</code>.</li>
<li>Forgetting the mandatory deletion when the array is all 1s.</li>
<li>Allowing two zeros in the window.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Flip up to k zeros ([[1004]]).</li>
<li>Longest run with at most k of something ([[340]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[1004]] · [[424]] · [[3]]</p>
''',

# ============================================================ LC 1658 — Minimum Operations to Reduce X to Zero
1658: '''
<h2>🧭 How to think about it</h2>
<p>You remove elements from the two <em>ends</em> until their total is exactly <code>x</code>; minimize how many you remove. Flip it: the elements you <strong>keep</strong> form a contiguous middle subarray. So find the <strong>longest middle subarray whose sum equals <code>total − x</code></strong>; the answer is <code>n − (its length)</code>.</p>

<h2>🐢 Brute force first</h2>
<p>Trying all end-removal combinations is exponential. Reframing to a longest-subarray-with-target-sum is O(n) (positive values → sliding window).</p>

<div class="insight">💡 <strong>Key insight:</strong> removing a prefix and a suffix summing to <code>x</code> leaves a middle summing to <code>total − x</code>. Since values are positive, a sliding window finds the <em>longest</em> such middle; fewer removed ends = shorter total removal.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>need = total − x</code>. If <code>need &lt; 0</code>, impossible → −1.</li>
<li>Sliding window for the longest subarray summing to <code>need</code>.</li>
<li>Answer = <code>n − bestLen</code> (or −1 if none found).</li>
</ol>

<h2>🎞️ Visual dry run — nums = [1,1,4,2,3], x = 5, total = 11</h2>
<pre class="viz">need = 6 ; longest window summing 6: [1,1,4] len3
answer = 5 − 3 = 2 (remove the last two: 2+3=5)</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def minOperations(nums, x):
    need = sum(nums) - x
    if need &lt; 0:
        return -1
    if need == 0:
        return len(nums)                 # remove everything
    left = cur = 0
    best = -1
    for right, v in enumerate(nums):
        cur += v
        while cur &gt; need:                 # positive values → shrink
            cur -= nums[left]; left += 1
        if cur == need:
            best = max(best, right - left + 1)
    return -1 if best == -1 else len(nums) - best</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong>, <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li><code>total &lt; x</code> → −1.</li>
<li><code>total == x</code> → remove the whole array (<code>need = 0</code>).</li>
<li>No middle subarray sums to <code>need</code> → −1.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Trying to greedily peel from the ends directly.</li>
<li>Forgetting the <code>need == 0</code> and <code>need &lt; 0</code> cases.</li>
<li>Reporting the middle length instead of <code>n − length</code>.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Take from both ends to collect quotas ([[2516]]).</li>
<li>Shortest subarray with sum ≥ k ([[209]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[2516]] · [[209]] · [[560]]</p>
''',

# ============================================================ LC 1838 — Frequency of the Most Frequent Element
1838: '''
<h2>🧭 How to think about it</h2>
<p>You may add 1 to elements a total of <code>k</code> times; maximize the count of equal elements. If you <strong>sort</strong>, the cheapest way to make a group equal is to raise everyone up to the group's largest value. Slide a window over the sorted array; a window is affordable when the cost to lift all its elements to <code>nums[right]</code> is ≤ <code>k</code>.</p>

<h2>🐢 Brute force first</h2>
<p>Try each target value and count reachable elements → O(n²). Sort + sliding window with a running sum is O(n log n).</p>

<div class="insight">💡 <strong>Key insight:</strong> after sorting, the cost to make window <code>[left, right]</code> all equal to <code>nums[right]</code> is <code>nums[right] × windowLen − windowSum</code>. Grow <code>right</code>; while the cost exceeds <code>k</code>, shrink <code>left</code>. The largest affordable window is the answer.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Sort. Maintain a window sum.</li>
<li>Cost = <code>nums[right] × (right − left + 1) − windowSum</code>.</li>
<li>While cost &gt; k, subtract <code>nums[left]</code> and advance <code>left</code>.</li>
<li>Track the max window length.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [1,2,4], k = 5 → sorted [1,2,4]</h2>
<pre class="viz">right=2 (4): window[1,2,4] cost = 4*3 − 7 = 5 ≤5 → len3
Answer: 3</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def maxFrequency(nums, k):
    nums.sort()
    left = total = best = 0
    for right, x in enumerate(nums):
        total += x
        # cost to raise the whole window up to x
        while x * (right - left + 1) - total &gt; k:
            total -= nums[left]
            left += 1
        best = max(best, right - left + 1)
    return best</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n log n)</strong> — the sort dominates. <strong>Space O(1)</strong> (or O(n) for sorting).</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>k = 0 → the largest count of an already-equal value.</li>
<li>All equal → n.</li>
<li>Huge k → the whole array.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Forgetting to sort first.</li>
<li>Computing cost against the wrong target (must be <code>nums[right]</code>, the window max).</li>
<li>Integer overflow in fixed-width languages (<code>x × len</code> is large).</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Allow ± adjustments within k ([[3346]], [[3347]]).</li>
<li>Max beauty after ±k operations ([[2779]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[3346]] · [[2779]] · [[209]]</p>
''',

# ============================================================ LC 2461 — Maximum Sum of Distinct Subarrays With Length K
2461: '''
<h2>🧭 How to think about it</h2>
<p>Among all length-<code>k</code> windows whose elements are <strong>all distinct</strong>, return the maximum sum. Slide a fixed window of size <code>k</code> keeping a running sum and a count map; a window qualifies only when its map has exactly <code>k</code> keys (no repeats).</p>

<h2>🐢 Brute force first</h2>
<p>Check each window for distinctness and sum it → O(n·k). A rolling sum plus a count map is O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> maintain the window sum and a frequency map as you slide. The window is "distinct" exactly when <code>len(map) == k</code>. Update the best sum only then.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Add each element to the sum and map; once the window exceeds <code>k</code>, evict the leftmost.</li>
<li>When the window size is <code>k</code> and the map has <code>k</code> keys, update the best.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [1,5,4,2,9,9,9], k = 3</h2>
<pre class="viz">[1,5,4] distinct sum10 ; [5,4,2] 11 ; [4,2,9] 15 ; [2,9,9] repeat skip ; [9,9,9] skip
Answer: 15</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>from collections import defaultdict
def maximumSubarraySum(nums, k):
    count = defaultdict(int)
    total = best = 0
    left = 0
    for right, x in enumerate(nums):
        total += x
        count[x] += 1
        if right - left + 1 &gt; k:          # keep window size k
            y = nums[left]
            total -= y
            count[y] -= 1
            if count[y] == 0:
                del count[y]
            left += 1
        if right - left + 1 == k and len(count) == k:
            best = max(best, total)       # all distinct
    return best</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong>, <strong>Space O(k)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>No distinct window of size k → 0.</li>
<li>k = 1 → the max single element.</li>
<li>All distinct → the plain max-sum window.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Not deleting zero-count keys (map size wrong).</li>
<li>Comparing sums for non-distinct windows.</li>
<li>Off-by-one on window size.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Longest distinct substring ([[3]]).</li>
<li>Max average subarray ([[643]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[643]] · [[3]] · [[239]]</p>
''',

# ============================================================ LC 2516 — Take K of Each Character From Left and Right
2516: '''
<h2>🧭 How to think about it</h2>
<p>You take characters only from the two ends and must collect at least <code>k</code> each of <code>a</code>, <code>b</code>, <code>c</code>; minimize how many you take. Flip it: the characters you <strong>leave</strong> form a contiguous middle. So find the <strong>longest middle window</strong> whose removal still leaves ≥ <code>k</code> of each letter outside it; the answer is <code>n − thatLength</code>.</p>

<h2>🐢 Brute force first</h2>
<p>Enumerating end-take splits is O(n²). The complementary longest-window approach is O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> count the total of each letter. A middle window is allowed if, for every letter, <code>total − insideWindow ≥ k</code> (enough remain at the ends). Slide the largest such window; taking the rest from the ends is minimal.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>If any letter's total &lt; k → −1.</li>
<li>Window counts inside; it's valid when each letter still has ≥ k outside.</li>
<li>Maximize the window length; answer = <code>n − best</code>.</li>
</ol>

<h2>🎞️ Visual dry run — s = "aabaaaacaabc", k = 2</h2>
<pre class="viz">longest middle we can leave while keeping ≥2 of each at the ends → length 4 (example)
answer = n − 4 = 8</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>from collections import Counter
def takeCharacters(s, k):
    total = Counter(s)
    if any(total[c] &lt; k for c in "abc"):
        return -1
    inside = Counter()
    left = best = 0
    for right, ch in enumerate(s):
        inside[ch] += 1
        # shrink while removing this window would drop some letter below k
        while any(total[c] - inside[c] &lt; k for c in "abc"):
            inside[s[left]] -= 1
            left += 1
        best = max(best, right - left + 1)
    return len(s) - best</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — the "any over 3 letters" check is O(1). <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Some letter appears fewer than k times → −1.</li>
<li>k = 0 → take nothing (answer 0).</li>
<li>Need the entire string → best window 0.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Trying to directly simulate taking from both ends.</li>
<li>Checking counts inside the window instead of what remains outside.</li>
<li>Missing the impossibility check.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Reduce X to zero from ends ([[1658]]).</li>
<li>Minimum window substring ([[76]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[1658]] · [[76]] · [[209]]</p>
''',

# ============================================================ LC 2762 — Continuous Subarrays
2762: '''
<h2>🧭 How to think about it</h2>
<p>Count subarrays where the difference between the max and min is at most 2. Slide a window keeping its max and min via <strong>two monotonic deques</strong>; whenever <code>max − min &gt; 2</code>, shrink from the left. Each valid right end contributes <code>right − left + 1</code> subarrays.</p>

<h2>🐢 Brute force first</h2>
<p>Check every subarray's spread → O(n²). Deques keep max/min in O(1) amortized → O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> this is [[1438]]'s machinery used for <em>counting</em>. Maintain a decreasing deque (max) and increasing deque (min); after fixing the window at each <code>right</code>, add <code>right − left + 1</code> — every subarray ending at <code>right</code> and starting in <code>[left, right]</code> is continuous.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Push each index into the max and min deques.</li>
<li>While <code>maxFront − minFront &gt; 2</code>, advance <code>left</code>, expiring fronts.</li>
<li>Add <code>right − left + 1</code> to the count.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [5,4,2,4]</h2>
<pre class="viz">[5]→+1 ; [5,4]→+2 ; add 2: max5 min2 diff3&gt;2 → shrink to [4,2] → +2 ; [4,2,4] diff2 → +3
total = 8</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>from collections import deque
def continuousSubarrays(nums):
    maxd, mind = deque(), deque()
    left = 0
    total = 0
    for right, x in enumerate(nums):
        while maxd and nums[maxd[-1]] &lt;= x: maxd.pop()
        while mind and nums[mind[-1]] &gt;= x: mind.pop()
        maxd.append(right); mind.append(right)
        while nums[maxd[0]] - nums[mind[0]] &gt; 2:
            left += 1
            if maxd[0] &lt; left: maxd.popleft()
            if mind[0] &lt; left: mind.popleft()
        total += right - left + 1          # subarrays ending at right
    return total</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong>, <strong>Space O(n)</strong> for the deques.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>All within 2 → n(n+1)/2 subarrays.</li>
<li>Large jumps → many length-1 windows.</li>
<li>Single element → 1.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Counting length instead of adding <code>right − left + 1</code>.</li>
<li>Not expiring deque fronts as <code>left</code> moves.</li>
<li>Overflow on the total count in fixed-width languages.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Longest window with spread ≤ limit ([[1438]]).</li>
<li>Sliding window maximum ([[239]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[1438]] · [[239]] · [[713]]</p>
''',

# ============================================================ LC 2779 — Maximum Beauty of an Array After Applying Operation
2779: '''
<h2>🧭 How to think about it</h2>
<p>Each element may be changed once to any value in <code>[nums[i] − k, nums[i] + k]</code>; the "beauty" is the longest run of equal values you can make. Sort, and notice element <code>i</code> can cover any target within its ±k interval — so the answer is the <strong>largest set of intervals sharing a common point</strong>, which a sorted sliding window finds as the longest window with <code>nums[right] − nums[left] ≤ 2k</code>.</p>

<h2>🐢 Brute force first</h2>
<p>Try each target value and count coverers → O(n · range). Sort + window is O(n log n).</p>

<div class="insight">💡 <strong>Key insight:</strong> two elements can both become the same value iff their ±k intervals overlap, i.e. <code>|a − b| ≤ 2k</code>. On the sorted array, the longest window with <code>nums[right] − nums[left] ≤ 2k</code> is the max number of elements meetable at one value.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Sort the array.</li>
<li>Slide a window; while <code>nums[right] − nums[left] &gt; 2k</code>, advance <code>left</code>.</li>
<li>Track the longest window length.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [4,6,1,2], k = 2 → sorted [1,2,4,6]</h2>
<pre class="viz">2k=4 ; window [1,2,4] diff3 ≤4 len3 ; add 6 → 6−1=5 &gt;4 → shrink to [2,4,6] diff4 len3
Answer: 3</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def maximumBeauty(nums, k):
    nums.sort()
    left = best = 0
    for right in range(len(nums)):
        while nums[right] - nums[left] &gt; 2 * k:   # intervals no longer overlap
            left += 1
        best = max(best, right - left + 1)
    return best</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n log n)</strong> — the sort. <strong>Space O(1)</strong> extra.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>k = 0 → longest run of an already-equal value.</li>
<li>All within 2k → n.</li>
<li>Single element → 1.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Using <code>k</code> instead of <code>2k</code> for the overlap width.</li>
<li>Forgetting to sort.</li>
<li>Confusing beauty (count) with a subarray requirement (order doesn't matter here).</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Max frequency with +1 operations ([[1838]]).</li>
<li>Interval point-cover (max overlap) problems.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[1838]] · [[3346]] · [[209]]</p>
''',

# ============================================================ LC 2981 — Find Longest Special Substring That Occurs Thrice I
2981: '''
<h2>🧭 How to think about it</h2>
<p>A "special" substring is a run of a single repeated letter (like <code>"aaa"</code>). Find the longest length that occurs at least <strong>three times</strong> (overlaps allowed), or <code>−1</code>. Since specials are single-letter runs, group the run lengths per letter, then figure out the largest length that can be formed three times.</p>

<h2>🐢 Brute force first</h2>
<p>Enumerate all special substrings and count → O(n²). Using per-letter run lengths reduces the reasoning to a handful of candidates.</p>

<div class="insight">💡 <strong>Key insight:</strong> a run of length <code>L</code> contains a special of length <code>ell</code> in <code>L − ell + 1</code> positions. For each letter, take its run lengths; the best length appearing ≥ 3 times comes from the top runs: either the largest run minus 2 (three copies inside it), or combinations of the top three runs. Check candidate lengths and count occurrences.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Collect run lengths per letter.</li>
<li>For a candidate length <code>ell</code>, occurrences for a letter = <code>sum(max(0, run − ell + 1))</code>.</li>
<li>Find the largest <code>ell</code> (over all letters) with total occurrences ≥ 3.</li>
</ol>

<h2>🎞️ Visual dry run — s = "aaaa"</h2>
<pre class="viz">run of 'a' length4
ell=2 → occurrences 4−2+1 = 3 ≥3 ✓ ; ell=3 → 2 &lt;3
Answer: 2</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>from collections import defaultdict
def maximumLength(s):
    runs = defaultdict(list)
    i, n = 0, len(s)
    while i &lt; n:
        j = i
        while j &lt; n and s[j] == s[i]:
            j += 1
        runs[s[i]].append(j - i)          # run length for this letter
        i = j

    best = -1
    for lengths in runs.values():
        for ell in range(1, max(lengths) + 1):
            occ = sum(max(0, L - ell + 1) for L in lengths)
            if occ &gt;= 3:
                best = max(best, ell)
    return best</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n²)</strong> worst case for the "I" limits (candidate lengths × runs). <strong>Space O(n)</strong> for the runs. (A top-3-runs formula gives O(n).)</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>No length occurs three times → −1.</li>
<li>Three separate single letters (e.g., "aaa" as three overlapping "a") → length 1.</li>
<li>All distinct letters → −1.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Forgetting overlaps are allowed (a run of L gives multiple positions).</li>
<li>Only checking the single longest run and missing combinations across runs.</li>
<li>Off-by-one in <code>L − ell + 1</code>.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Occurs at least m times → change the threshold.</li>
<li>Larger limits → use the top-three-runs closed form.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[424]] · [[3]] · [[340]]</p>
''',

# ============================================================ LC 3026 — Maximum Good Subarray Sum
3026: '''
<h2>🧭 How to think about it</h2>
<p>A subarray is "good" if its first and last values differ by exactly <code>k</code>; maximize its sum. Using prefix sums, the sum of <code>[i, j]</code> is <code>prefix[j+1] − prefix[i]</code>. To maximize it for a fixed right end <code>j</code>, you want the <strong>smallest prefix</strong> at a start <code>i</code> whose value is <code>nums[j] + k</code> or <code>nums[j] − k</code>. Track that with a dictionary.</p>

<h2>🐢 Brute force first</h2>
<p>Check all pairs with the value constraint → O(n²). A value→min-prefix map makes it O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> keep <code>min_prefix[v]</code> = the smallest prefix sum seen just before an element with value <code>v</code>. At index <code>j</code>, the best good subarray ending here uses a start whose value is <code>nums[j] ± k</code>; its sum is <code>prefix[j+1] − min_prefix[nums[j]±k]</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Sweep, maintaining a running prefix sum.</li>
<li>For <code>nums[j]</code>, consider partners <code>nums[j] + k</code> and <code>nums[j] − k</code>; if present, update the best sum.</li>
<li>Record <code>min_prefix[nums[j]] = min(existing, prefix_before_j)</code>.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [1,2,3,4,5,6], k = 1</h2>
<pre class="viz">each adjacent pair differs by 1 → good subarrays are contiguous runs
best sum uses the smallest starting prefix for value nums[j]±1 → the whole array style max
Answer: the maximum such contiguous sum</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def maximumSubarraySum(nums, k):
    best = float('-inf')
    min_prefix = {}            # value -> smallest prefix sum before such a value
    prefix = 0
    for x in nums:
        # candidate starts whose value pairs with x
        for partner in (x - k, x + k):
            if partner in min_prefix:
                best = max(best, prefix + x - min_prefix[partner])
        # record smallest prefix seen before an element equal to x
        if x not in min_prefix or prefix &lt; min_prefix[x]:
            min_prefix[x] = prefix
        prefix += x
    return 0 if best == float('-inf') else best</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — O(1) work per element. <strong>Space O(n)</strong> for the map.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>No good subarray → return 0 (per the problem).</li>
<li>Negative values → prefix sums handle them.</li>
<li>Duplicate values → keep the smallest prefix.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Storing the prefix <em>after</em> adding <code>x</code> instead of before (breaks the subarray boundaries).</li>
<li>Keeping the latest prefix instead of the minimum.</li>
<li>Forgetting both <code>±k</code> partners.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Endpoints differ by at most k → range query over a sorted structure.</li>
<li>Subarray sum equals k ([[560]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[560]] · [[1658]] · [[209]]</p>
''',

# ============================================================ LC 3346 — Maximum Frequency of an Element After Performing Operations I
3346: '''
<h2>🧭 How to think about it</h2>
<p>You may adjust up to <code>numOperations</code> elements, each by at most ±<code>k</code> (each element once); maximize how many elements end up equal to some target <code>t</code>. For a target <code>t</code>, the elements that can <em>reach</em> it are those in <code>[t − k, t + k]</code>; the count you can make equal is limited by how many are already <code>t</code> plus <code>numOperations</code>. Sweep candidate targets and take the best.</p>

<h2>🐢 Brute force first</h2>
<p>For each possible target value scan the whole array → O(range · n). Sorting plus a sliding window over <code>[t − k, t + k]</code> makes it O(n log n).</p>

<div class="insight">💡 <strong>Key insight:</strong> good targets are the array's own values (or the boundaries). For target <code>t</code>: <code>reachable</code> = count of elements within <code>[t − k, t + k]</code> (a window on the sorted array); <code>alreadyEqual</code> = count of elements exactly <code>t</code>. The answer for <code>t</code> is <code>min(reachable, alreadyEqual + numOperations)</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Sort; also count exact frequencies.</li>
<li>For each candidate target <code>t</code> (each distinct value), window-count elements in <code>[t − k, t + k]</code>.</li>
<li>Best = <code>max(min(windowCount, freq[t] + numOperations))</code>.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [1,4,5], k = 1, ops = 2</h2>
<pre class="viz">t=4: reachable in [3,5] = {4,5} = 2 ; already 1 → min(2, 1+2)=2
t=5: reachable [4,6] = {4,5}=2 ; already1 → min(2,3)=2
Answer: 2</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>from collections import Counter
def maxFrequency(nums, k, numOperations):
    nums.sort()
    freq = Counter(nums)
    best = 0
    left = 0
    for right, t in enumerate(nums):        # candidate target = an existing value
        while nums[right] - nums[left] &gt; 2 * k:   # window of reachable-to-some-target
            left += 1
    # simpler: evaluate each distinct value as the target
    best = 0
    for t in set(nums):
        # count elements within [t-k, t+k] via bisect
        import bisect
        lo = bisect.bisect_left(nums, t - k)
        hi = bisect.bisect_right(nums, t + k)
        reachable = hi - lo
        best = max(best, min(reachable, freq[t] + numOperations))
    return best</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n log n)</strong> — sort plus a binary-search window per distinct target. <strong>Space O(n)</strong> for the frequency map.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li><code>numOperations = 0</code> → the plain max frequency.</li>
<li>k large enough to reach everything → limited only by <code>freq[t] + ops</code>.</li>
<li>All equal → n.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Forgetting the <code>min(reachable, alreadyEqual + ops)</code> cap — you can't create elements out of thin air.</li>
<li>Only trying existing values but missing that they are sufficient candidates.</li>
<li>Counting the same element for two different operations.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Larger constraints → [[3347]] (same idea, careful counting).</li>
<li>+1-only operations ([[1838]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[3347]] · [[1838]] · [[2779]]</p>
''',

# ============================================================ LC 3347 — Maximum Frequency of an Element After Performing Operations II
3347: '''
<h2>🧭 How to think about it</h2>
<p>Same problem as [[3346]] — adjust up to <code>numOperations</code> elements by ±<code>k</code> to maximize equal-element count — but with much larger value ranges, so you can't sweep raw values. Restrict candidate targets to the <strong>array's own values</strong> (and use binary search for the reachable window), which is enough to hit the optimum.</p>

<h2>🐢 Brute force first</h2>
<p>Sweeping every integer target is infeasible for wide ranges. Only the existing values (or their ±k boundaries) can be optimal targets — a finite, small set.</p>

<div class="insight">💡 <strong>Key insight:</strong> for target <code>t</code>, <code>reachable</code> = number of elements within <code>[t − k, t + k]</code> (found by binary search on the sorted array), and the answer is <code>min(reachable, freq[t] + numOperations)</code>. Evaluating every distinct value as <code>t</code> covers the optimum because moving the target off a value never increases both the exact count and the reachable count.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Sort; build exact-frequency counts.</li>
<li>For each distinct value <code>t</code>: binary-search the count in <code>[t − k, t + k]</code>.</li>
<li>Best = <code>max(min(reachable, freq[t] + numOperations))</code>.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [5,11,20,20], k = 5, ops = 1</h2>
<pre class="viz">t=20: reachable in [15,25] = {20,20} = 2 ; already 2 → min(2, 2+1)=2
t=11: reachable [6,16] = {11} =1 ; min(1,1+1)=1
Answer: 2</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>import bisect
from collections import Counter
def maxFrequency(nums, k, numOperations):
    nums.sort()
    freq = Counter(nums)
    best = 0
    for t in set(nums):
        lo = bisect.bisect_left(nums, t - k)     # first index ≥ t-k
        hi = bisect.bisect_right(nums, t + k)    # first index &gt; t+k
        reachable = hi - lo
        best = max(best, min(reachable, freq[t] + numOperations))
    return best</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n log n)</strong> — sort plus O(log n) per distinct target. <strong>Space O(n)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Huge values → binary search avoids scanning the range.</li>
<li><code>numOperations = 0</code> → plain max frequency.</li>
<li>Duplicates → counted in both <code>freq</code> and the window.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Trying to sweep every integer target (too many).</li>
<li>Dropping the <code>min(…, freq[t] + ops)</code> cap.</li>
<li>Off-by-one in <code>bisect_left</code>/<code>bisect_right</code> bounds.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Small-range version ([[3346]]).</li>
<li>Beauty after ±k ([[2779]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[3346]] · [[2779]] · [[1838]]</p>
''',

# ============================================================ LC 239 — Sliding Window Maximum
239: '''
<h2>🧭 How to think about it</h2>
<p>Report the maximum of every length-<code>k</code> window. A <strong>monotonic decreasing deque of indices</strong> keeps the current window's candidates so the front is always the max. Smaller values at the back are useless once a bigger value arrives, so they're discarded.</p>

<h2>🐢 Brute force first</h2>
<p>Max of each window from scratch → O(n·k). A heap is O(n log k). The monotonic deque is O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> before pushing index <code>i</code>, pop all back indices whose values are ≤ <code>nums[i]</code> (they can never be the max while <code>i</code> is around). Expire the front if it's left the window (<code>front ≤ i − k</code>). The front is the window max.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>For each <code>i</code>: pop smaller values from the back; append <code>i</code>.</li>
<li>Pop the front if it's out of the window.</li>
<li>Once <code>i ≥ k−1</code>, record <code>nums[front]</code>.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [1,3,-1,-3,5,3,6,7], k = 3</h2>
<pre class="viz">windows maxima: [1,3,-1]→3 ; [3,-1,-3]→3 ; [-1,-3,5]→5 ; [-3,5,3]→5 ; [5,3,6]→6 ; [3,6,7]→7
Result: [3,3,5,5,6,7]</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>from collections import deque
def maxSlidingWindow(nums, k):
    dq = deque()                         # indices, values decreasing
    res = []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] &lt;= x:   # pop smaller tail values
            dq.pop()
        dq.append(i)
        if dq[0] &lt;= i - k:               # front left the window
            dq.popleft()
        if i &gt;= k - 1:
            res.append(nums[dq[0]])       # front is the window max
    return res</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — each index pushed/popped once. <strong>Space O(k)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>k = 1 → the array itself.</li>
<li>k = n → one maximum.</li>
<li>Duplicates → <code>≤</code> keeps the deque tidy without dropping the true max.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Storing values instead of indices (can't expire by position).</li>
<li>Recording before the first full window.</li>
<li>Using <code>&lt;</code> vs <code>≤</code> incorrectly when values tie.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Window minimum → increasing deque.</li>
<li>Shortest subarray with sum ≥ k ([[862]]) uses a deque over prefix sums.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[862]] · [[1696]] · [[1438]]</p>
''',

# ============================================================ LC 862 — Shortest Subarray with Sum at Least K
862: '''
<h2>🧭 How to think about it</h2>
<p>Find the shortest subarray with sum ≥ <code>k</code>, but values may be <strong>negative</strong>, so the simple positive-only window ([[209]]) breaks. Work on <strong>prefix sums</strong> and keep a <strong>monotonic increasing deque</strong> of prefix indices; it lets you find, for each right end, the best (closest, smallest-prefix) start.</p>

<h2>🐢 Brute force first</h2>
<p>All subarrays → O(n²). The deque over prefix sums gives O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> with prefixes <code>P</code>, a subarray <code>(i, j]</code> has sum <code>P[j] − P[i] ≥ k</code>. For each <code>j</code>: (1) while <code>P[j] − P[front] ≥ k</code>, that front gives a valid subarray — record its length and pop it (a closer <code>j</code> can't do better with it). (2) Keep the deque increasing by popping back indices with <code>P ≥ P[j]</code> (a larger-or-equal earlier prefix is never a better start).</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Build prefix sums <code>P</code> of length <code>n+1</code>.</li>
<li>For each <code>j</code>: pop fronts satisfying <code>P[j] − P[front] ≥ k</code> (update best); pop backs with <code>P[back] ≥ P[j]</code>; push <code>j</code>.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [2,-1,2], k = 3</h2>
<pre class="viz">P = [0,2,1,3]
j=3 (P3=3): P3−P0=3 ≥3 → length 3 (best)
Answer: 3</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>from collections import deque
def shortestSubarray(nums, k):
    n = len(nums)
    P = [0] * (n + 1)
    for i in range(n):
        P[i + 1] = P[i] + nums[i]
    dq = deque()                          # indices with increasing prefix sums
    best = n + 1
    for j in range(n + 1):
        while dq and P[j] - P[dq[0]] &gt;= k:      # valid start → try it and drop it
            best = min(best, j - dq.popleft())
        while dq and P[dq[-1]] &gt;= P[j]:         # keep prefixes increasing
            dq.pop()
        dq.append(j)
    return best if best &lt;= n else -1</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — each index enters/leaves the deque once. <strong>Space O(n)</strong> for prefixes and the deque.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>No subarray reaches k → −1.</li>
<li>Negative values → handled by the prefix-deque (unlike [[209]]).</li>
<li>Single element ≥ k → length 1.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Applying the positive-only sliding window with negatives present.</li>
<li>Not popping the front after it yields a valid answer (a later <code>j</code> only makes it longer).</li>
<li>Wrong monotonic direction on the deque.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Positive-only shortest subarray ([[209]]).</li>
<li>Sliding window maximum ([[239]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[209]] · [[239]] · [[560]]</p>
''',

# ============================================================ LC 1696 — Jump Game VI
1696: '''
<h2>🧭 How to think about it</h2>
<p>Start at index 0; each move jumps forward 1..<code>k</code> steps, adding the landing value to your score; maximize the score at the last index. That's a DP where <code>dp[i]</code> = best score to reach <code>i</code> = <code>nums[i] +</code> the <strong>maximum of the previous k dp values</strong>. A sliding-window maximum (monotonic deque) supplies that max in O(1).</p>

<h2>🐢 Brute force first</h2>
<p>Plain DP scans back <code>k</code> per index → O(n·k). A monotonic deque over the dp window gives O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> <code>dp[i] = nums[i] + max(dp[i−k .. i−1])</code>. Maintain a decreasing deque of indices by dp value; the front is that window max. Expire indices older than <code>i − k</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>dp[0] = nums[0]</code>; deque holds index 0.</li>
<li>For each <code>i</code>: expire the front if <code>&lt; i − k</code>; <code>dp[i] = nums[i] + dp[front]</code>.</li>
<li>Pop back indices with dp ≤ <code>dp[i]</code>; push <code>i</code>.</li>
<li>Return <code>dp[n−1]</code>.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [1,-1,-2,4,-7,3], k = 2</h2>
<pre class="viz">dp0=1 ; dp1=1+(-1)=0 ; dp2=1+(-2)=-1 ; dp3=max(dp1,dp2)+4=0+4=4 ; dp4=max(dp2,dp3)-7=4-7=-3 ; dp5=max(dp3,dp4)+3=4+3=7
Answer: 7</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>from collections import deque
def maxResult(nums, k):
    n = len(nums)
    dp = [0] * n
    dp[0] = nums[0]
    dq = deque([0])                       # indices, dp values decreasing
    for i in range(1, n):
        while dq[0] &lt; i - k:              # out of the k-window
            dq.popleft()
        dp[i] = nums[i] + dp[dq[0]]       # best reachable predecessor
        while dq and dp[dq[-1]] &lt;= dp[i]:
            dq.pop()
        dq.append(i)
    return dp[-1]</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — each index enters/leaves the deque once. <strong>Space O(n)</strong> for dp (deque O(k)).</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>k ≥ n → one jump can reach the end from anywhere earlier.</li>
<li>All negatives → still must traverse; deque picks the least bad path.</li>
<li>Single element → <code>nums[0]</code>.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Recomputing the window max by scanning (O(n·k)).</li>
<li>Not expiring the deque front outside the window.</li>
<li>Reading the max before expiring stale indices.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Constrained subsequence sum → same deque-DP.</li>
<li>Sliding window maximum ([[239]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[239]] · [[862]] · [[1438]]</p>
''',

# ============================================================ LC 438 — Find All Anagrams in a String
438: '''
<h2>🧭 How to think about it</h2>
<p>Find every start index where a substring of <code>s</code> is an anagram of <code>p</code>. Use a <strong>fixed window of length |p|</strong> and compare letter counts. Instead of rebuilding counts each slide, keep a running difference and a "matched letters" counter for O(1) checks.</p>

<h2>🐢 Brute force first</h2>
<p>Sort or count each window and compare to <code>p</code> → O(n·|p|). The incremental count window is O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> maintain a 26-slot count of the current window versus <code>p</code>'s counts. Slide by adding the new right character and removing the left one; a window is an anagram exactly when all counts match — track a <code>matches</code> counter to avoid re-scanning 26 slots each step.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Build <code>need</code> counts for <code>p</code> and a running window count.</li>
<li>Slide a window of length <code>|p|</code>; add right, remove left.</li>
<li>When the window count equals <code>need</code>, record the start index.</li>
</ol>

<h2>🎞️ Visual dry run — s = "cbaebabacd", p = "abc"</h2>
<pre class="viz">window "cba" → anagram → index 0 ; ... "bac" → index 6
Result: [0, 6]</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>from collections import Counter
def findAnagrams(s, p):
    if len(p) &gt; len(s):
        return []
    need = Counter(p)
    window = Counter(s[:len(p)])
    res = []
    if window == need:
        res.append(0)
    for i in range(len(p), len(s)):
        window[s[i]] += 1                 # add new right char
        left = s[i - len(p)]
        window[left] -= 1                 # remove left char
        if window[left] == 0:
            del window[left]
        if window == need:
            res.append(i - len(p) + 1)
    return res</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — the <code>Counter</code> comparison is O(26). <strong>Space O(1)</strong> (fixed alphabet).</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li><code>p</code> longer than <code>s</code> → empty.</li>
<li>Repeated letters in <code>p</code> → multiplicities matter.</li>
<li>Whole string is one anagram → single index 0.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Not deleting zero-count keys, so <code>window == need</code> fails.</li>
<li>Off-by-one on the recorded start index.</li>
<li>Rebuilding counts from scratch each slide.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Return true if any permutation exists ([[567]]).</li>
<li>Minimum window substring ([[76]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[567]] · [[76]] · [[3]]</p>
''',

# ============================================================ LC 567 — Permutation in String
567: '''
<h2>🧭 How to think about it</h2>
<p>Return true if <code>s2</code> contains any permutation of <code>s1</code> as a contiguous substring. It's [[438]] with an early exit: slide a fixed window of length <code>|s1|</code> over <code>s2</code> comparing letter counts, and return <code>True</code> on the first exact match.</p>

<h2>🐢 Brute force first</h2>
<p>Check each window's sorted form against <code>s1</code> → O(n·|s1| log|s1|). The count-window is O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> a permutation match means identical letter counts. Keep a running 26-count window; slide by add-right/remove-left; the first time it equals <code>s1</code>'s counts, a permutation is present.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Build <code>need</code> counts for <code>s1</code>, plus the first window of <code>s2</code>.</li>
<li>Slide; on each step compare counts.</li>
<li>Return True at the first match; False if none.</li>
</ol>

<h2>🎞️ Visual dry run — s1 = "ab", s2 = "eidbaooo"</h2>
<pre class="viz">windows "ei","id","db","ba" → "ba" matches counts of "ab" → True</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>from collections import Counter
def checkInclusion(s1, s2):
    if len(s1) &gt; len(s2):
        return False
    need = Counter(s1)
    window = Counter(s2[:len(s1)])
    if window == need:
        return True
    for i in range(len(s1), len(s2)):
        window[s2[i]] += 1
        left = s2[i - len(s1)]
        window[left] -= 1
        if window[left] == 0:
            del window[left]
        if window == need:
            return True                   # first match is enough
    return False</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — O(26) comparisons. <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li><code>s1</code> longer than <code>s2</code> → False.</li>
<li>Immediate match at index 0 → checked before sliding.</li>
<li>Repeated letters → counts capture multiplicity.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Returning all matches instead of a boolean (that's [[438]]).</li>
<li>Forgetting to delete zero-count keys.</li>
<li>Not checking the very first window.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Return all start indices ([[438]]).</li>
<li>Minimum window substring ([[76]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[438]] · [[76]] · [[242]]</p>
''',
}
