# -*- coding: utf-8 -*-
"""
Deep tutorials for Pattern 17: Prefix Sum & Difference Array Patterns.
Masterclass 12-step structured explanations with ASCII dry runs and complexity analyses.
"""

DEEP = {
325: '''<h2>🧭 How to think about it</h2>
<p>Given an integer array <code>nums</code> and an integer <code>k</code>, return the maximum length of a subarray that sums to <code>k</code>. If there isn't one, return 0 instead.</p>

<p>Let $prefix[i]$ be the cumulative running sum up to index $i$.
A subarray from $j + 1$ to $i$ has sum $prefix[i] - prefix[j] = k$.
Rearranging:
$$prefix[j] = prefix[i] - k$$
To <strong>maximize the length</strong> $i - j$, we want index $j$ to be as small (as early) as possible!
Therefore, maintain a hash map <code>first_seen[sum] -> index</code>:
- Only record the index the <strong>first time</strong> a prefix sum is encountered (never overwrite it)!
- Base case: <code>first_seen[0] = -1</code> (to handle subarrays starting at index 0).</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Checking all $O(n^2)$ subarrays takes $O(n^2)$ time. Hash map of earliest prefix occurrences finds the maximum length in a single linear pass $O(n)$ with $O(n)$ space.</p>

<div class="insight">💡 <strong>Key insight:</strong> Store earliest index of each prefix sum: <code>if curr_sum not in first_seen: first_seen[curr_sum] = i</code>. If <code>curr_sum - k</code> in map, update <code>max_len = max(max_len, i - first_seen[curr_sum - k])</code>.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def maxSubArrayLen(nums: list[int], k: int) -> int:
    first_seen = {0: -1}
    curr_sum = 0
    max_len = 0
    
    for i, x in enumerate(nums):
        curr_sum += x
        if curr_sum - k in first_seen:
            max_len = max(max_len, i - first_seen[curr_sum - k])
        if curr_sum not in first_seen:
            first_seen[curr_sum] = i
            
    return max_len
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n)$ — Single pass through array.<br>
<strong>Space:</strong> $O(n)$ — Hash map storing prefix sums.</p>
''',
523: '''<h2>🧭 How to think about it</h2>
<p>Given an integer array <code>nums</code> and an integer <code>k</code>, return <code>true</code> if <code>nums</code> has a continuous subarray of size at least two whose elements sum up to a multiple of <code>k</code>.</p>

<p><strong>Modulo Arithmetic on Prefix Sums:</strong>
If two prefix sums have the same remainder modulo $k$:
$$prefix[i] \\equiv prefix[j] \\pmod k \\implies (prefix[i] - prefix[j]) \\equiv 0 \\pmod k$$
which means the subarray sum between $j$ and $i$ is divisible by $k$!
Maintain <code>first_seen[remainder] -> index</code>:
- Base case: <code>first_seen[0] = -1</code>.
- If <code>curr_sum % k</code> has been seen before at index $j$ and $i - j \\ge 2$, return <code>True</code>!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Checking all subarrays takes $O(n^2)$. Modulo prefix map detects matching remainders in $O(n)$ time and $O(\\min(n, k))$ space.</p>

<div class="insight">💡 <strong>Key insight:</strong> Subarray sum is divisible by $k$ if two prefix sums share the same remainder: <code>rem = curr_sum % k</code>. Check if seen previously with index distance $\\ge 2$.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def checkSubarraySum(nums: list[int], k: int) -> bool:
    first_seen = {0: -1}
    curr_sum = 0
    
    for i, x in enumerate(nums):
        curr_sum += x
        rem = curr_sum % k
        if rem in first_seen:
            if i - first_seen[rem] >= 2:
                return True
        else:
            first_seen[rem] = i
            
    return False
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n)$ — Single pass.<br>
<strong>Space:</strong> $O(\\min(n, k))$ — Hash map storing remainders.</p>
''',
525: '''<h2>🧭 How to think about it</h2>
<p>Given a binary array <code>nums</code>, return the maximum length of a contiguous subarray with an equal number of 0 and 1.</p>

<p><strong>Transform 0 to -1 Trick:</strong>
If we treat <code>0</code> as <code>-1</code> and <code>1</code> as <code>+1</code>:
An equal number of 0s and 1s means the transformed subarray sums to <strong>0</strong>!
This reduces directly to <strong>LC 325 (Maximum Size Subarray Sum Equals 0)</strong>!
Maintain <code>first_seen[sum] -> index</code> with base case <code>first_seen[0] = -1</code>.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Counting 0s and 1s across all subarrays takes $O(n^2)$. Prefix transformation solves it in $O(n)$ time and $O(n)$ space.</p>

<div class="insight">💡 <strong>Key insight:</strong> Replace 0 with -1: <code>count += 1 if x == 1 else -1</code>. If <code>count</code> was seen before at index $j$, subarray from $j+1$ to $i$ has equal 0s and 1s!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def findMaxLength(nums: list[int]) -> int:
    first_seen = {0: -1}
    curr_sum = 0
    max_len = 0
    
    for i, x in enumerate(nums):
        curr_sum += 1 if x == 1 else -1
        if curr_sum in first_seen:
            max_len = max(max_len, i - first_seen[curr_sum])
        else:
            first_seen[curr_sum] = i
            
    return max_len
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n)$ — Linear pass over array.<br>
<strong>Space:</strong> $O(n)$ — Hash map storing running balance.</p>
''',
560: '''<h2>🧭 How to think about it</h2>
<p>Given an array of integers <code>nums</code> and an integer <code>k</code>, return the total number of subarrays whose sum equals to <code>k</code>.</p>

<p>A subarray sum from $j$ to $i$ equals $k$ if:
$$prefix[i] - prefix[j - 1] = k \\iff prefix[j - 1] = prefix[i] - k$$
Maintain a frequency map <code>prefix_counts</code> tracking how many times each prefix sum has occurred so far.
At each index $i$:
1. Add the number of times <code>prefix[i] - k</code> was seen to the answer:
   <code>total += prefix_counts.get(curr_sum - k, 0)</code>.
2. Increment frequency of the current prefix sum:
   <code>prefix_counts[curr_sum] = prefix_counts.get(curr_sum, 0) + 1</code>.
Base case: <code>prefix_counts[0] = 1</code> (a prefix itself equalling $k$).</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Evaluating all subarrays takes $O(n^2)$. Hash map frequency accumulation counts all valid subarrays in $O(n)$ time and $O(n)$ space.</p>

<div class="insight">💡 <strong>Key insight:</strong> Frequency map of prefix sums: <code>count += seen[curr_sum - k]</code>. Base case <code>seen[0] = 1</code>. Solves in $O(n)$ time!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">from collections import defaultdict

def subarraySum(nums: list[int], k: int) -> int:
    counts = defaultdict(int)
    counts[0] = 1
    curr_sum = 0
    total = 0
    
    for x in nums:
        curr_sum += x
        total += counts[curr_sum - k]
        counts[curr_sum] += 1
        
    return total
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n)$ — Single pass over <code>nums</code>.<br>
<strong>Space:</strong> $O(n)$ — Hash map of prefix sums.</p>
''',
930: '''<h2>🧭 How to think about it</h2>
<p>Given a binary array <code>nums</code> and an integer <code>goal</code>, return the number of non-empty subarrays with a sum <code>goal</code>.</p>

<p>Because all elements are non-negative ($0$ or $1$), we can use:
1. <strong>Prefix Sum Hash Map:</strong> Identical to <strong>LC 560</strong> in $O(n)$ time and $O(n)$ space.
2. <strong>Sliding Window (At Most Trick):</strong>
   $$\text{Exact}(goal) = \text{AtMost}(goal) - \text{AtMost}(goal - 1)$$
   The number of subarrays with sum $\\le goal$ can be computed using a two-pointer sliding window in $O(n)$ time and $O(1)$ space!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Hash map takes $O(n)$ space. Two-pass sliding window achieves $O(n)$ time with $O(1)$ auxiliary space.</p>

<div class="insight">💡 <strong>Key insight:</strong> $\text{Exact}(K) = \text{atMost}(K) - \text{atMost}(K - 1)$. Sliding window expands $r$, shrinks $l$ while sum exceeds target, adding $(r - l + 1)$ in $O(1)$ space.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def numSubarraysWithSum(nums: list[int], goal: int) -> int:
    def at_most(target):
        if target < 0:
            return 0
        l = 0
        curr_sum = 0
        count = 0
        for r in range(len(nums)):
            curr_sum += nums[r]
            while curr_sum > target:
                curr_sum -= nums[l]
                l += 1
            count += r - l + 1
        return count
        
    return at_most(goal) - at_most(goal - 1)
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n)$ — Two linear sliding window passes.<br>
<strong>Space:</strong> $O(1)$ — Constant pointers.</p>
''',
974: '''<h2>🧭 How to think about it</h2>
<p>Given an integer array <code>nums</code> and an integer <code>k</code>, return the number of non-empty subarrays that have a sum divisible by <code>k</code>.</p>

<p>Two prefix sums $prefix[i]$ and $prefix[j]$ produce a subarray divisible by $k$ if:
$$prefix[i] \\equiv prefix[j] \\pmod k$$
Count the frequency of each remainder $r = curr_sum % k$.
If a remainder $r$ has appeared $C$ times previously, the current prefix sum forms $C$ new valid subarrays!
Increment answer by $C$, then increment remainder frequency $C += 1$.
Base case: <code>remainder_counts[0] = 1</code>.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Modulo remainder hash table/array of size $k$ counts all matching pairs in $O(n)$ time and $O(k)$ space.</p>

<div class="insight">💡 <strong>Key insight:</strong> Frequency array of size $k$: <code>rem = curr_sum % k</code>. Add <code>counts[rem]</code> to answer, then increment <code>counts[rem] += 1</code>. Base case <code>counts[0] = 1</code>.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def subarraysDivByK(nums: list[int], k: int) -> int:
    counts = [0] * k
    counts[0] = 1
    curr_sum = 0
    total = 0
    
    for x in nums:
        curr_sum += x
        rem = curr_sum % k
        total += counts[rem]
        counts[rem] += 1
        
    return total
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n)$ — Single pass.<br>
<strong>Space:</strong> $O(k)$ — Remainder array of size $k$.</p>
''',
1248: '''<h2>🧭 How to think about it</h2>
<p>Given an array of integers <code>nums</code> and an integer <code>k</code>. A continuous subarray is called <strong>nice</strong> if there are <code>k</code> odd numbers on it. Return the number of nice sub-arrays.</p>

<p>Map each number to:
- <code>1</code> if odd (<code>x % 2 == 1</code>).
- <code>0</code> if even (<code>x % 2 == 0</code>).
The problem transforms identically to <strong>Binary Subarrays With Sum (LC 930)</strong> with <code>goal = k</code>!
$$\text{Exact}(k) = \text{atMost}(k) - \text{atMost}(k - 1)$$</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Sliding window with "at most" reduction executes in $O(n)$ time and $O(1)$ space.</p>

<div class="insight">💡 <strong>Key insight:</strong> Replace odd numbers with 1 and evens with 0. Subarrays with exactly $k$ odds $= \text{atMost}(k) - \text{atMost}(k - 1)$ in $O(1)$ space!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def numberOfSubarrays(nums: list[int], k: int) -> int:
    def at_most(target):
        if target < 0:
            return 0
        l = 0
        odds = 0
        count = 0
        for r in range(len(nums)):
            odds += nums[r] % 2
            while odds > target:
                odds -= nums[l] % 2
                l += 1
            count += r - l + 1
        return count
        
    return at_most(k) - at_most(k - 1)
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n)$ — Two linear scans.<br>
<strong>Space:</strong> $O(1)$ — Only pointer variables.</p>
''',
303: '''<h2>🧭 How to think about it</h2>
<p>Given an integer array <code>nums</code>, handle multiple queries of calculating the sum of elements between indices <code>left</code> and <code>right</code> inclusive where the array is immutable.</p>

<p>Precompute the <strong>Prefix Sum Array</strong> in the constructor:
$$prefix[0] = 0, \\quad prefix[i] = prefix[i - 1] + nums[i - 1]$$
Then any range sum is answered in strict $O(1)$ time:
$$\text{sumRange}(left, right) = prefix[right + 1] - prefix[left]$$</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Summing elements on every query takes $O(n)$ per call. Prefix sum array answers in $O(1)$ time with $O(n)$ precomputation.</p>

<div class="insight">💡 <strong>Key insight:</strong> Prefix sum array: <code>prefix[i] = prefix[i-1] + nums[i-1]</code>. Range sum $[l, r]$ is <code>prefix[r + 1] - prefix[l]</code> in $O(1)$!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">class NumArray:
    def __init__(self, nums: list[int]):
        self.prefix = [0]
        for x in nums:
            self.prefix.append(self.prefix[-1] + x)

    def sumRange(self, left: int, right: int) -> int:
        return self.prefix[right + 1] - self.prefix[left]
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> Constructor: $O(n)$. <code>sumRange</code>: $O(1)$ instant difference.<br>
<strong>Space:</strong> $O(n)$ — Prefix sum array.</p>
''',
304: '''<h2>🧭 How to think about it</h2>
<p>Given a 2D matrix <code>matrix</code>, handle multiple queries of calculating the sum of elements inside the rectangle defined by top-left $(row1, col1)$ and bottom-right $(row2, col2)$.</p>

<p><strong>2D Prefix Sum Formula (Inclusion-Exclusion):</strong>
Let $dp[r+1][c+1]$ be the sum of the submatrix from $(0, 0)$ to $(r, c)$:
$$dp[r+1][c+1] = matrix[r][c] + dp[r][c+1] + dp[r+1][c] - dp[r][c]$$
To query rectangle from $(r_1, c_1)$ to $(r_2, c_2)$:
$$\text{Sum} = dp[r_2+1][c_2+1] - dp[r_1][c_2+1] - dp[r_2+1][c_1] + dp[r_1][c_1]$$</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Traversing rectangle cells takes $O(m \times n)$ per query. 2D prefix sum answers queries in strictly $O(1)$ time!</p>

<div class="insight">💡 <strong>Key insight:</strong> 2D inclusion-exclusion: subtract top and left submatrices, add back the double-subtracted top-left overlap. Answers any rectangle in $O(1)$!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">class NumMatrix:
    def __init__(self, matrix: list[list[int]]):
        if not matrix or not matrix[0]:
            return
        m, n = len(matrix), len(matrix[0])
        self.dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for r in range(m):
            for c in range(n):
                self.dp[r + 1][c + 1] = (matrix[r][c] 
                                       + self.dp[r][c + 1] 
                                       + self.dp[r + 1][c] 
                                       - self.dp[r][c])

    def sumRegion(self, r1: int, c1: int, r2: int, c2: int) -> int:
        return (self.dp[r2 + 1][c2 + 1] 
              - self.dp[r1][c2 + 1] 
              - self.dp[r2 + 1][c1] 
              + self.dp[r1][c1])
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> Constructor: $O(m \times n)$. <code>sumRegion</code>: $O(1)$ arithmetic.<br>
<strong>Space:</strong> $O(m \times n)$ — 2D prefix table.</p>
''',
370: '''<h2>🧭 How to think about it</h2>
<p>You are given an integer <code>length</code> and an array <code>updates</code> where <code>updates[i] = [startIdx, endIdx, inc]</code>. Apply all updates to an initially zeroed array and return the final array.</p>

<p><strong>The Difference Array Technique:</strong>
Instead of modifying all elements from $start$ to $end$ ($O(length)$ per update):
Apply changes only at the boundaries in $O(1)$ time!
- <code>diff[start] += inc</code>: indicates values from $start$ onward increase by $inc$.
- <code>diff[end + 1] -= inc</code>: stops the increase from extending past $end$!</p>
<p>After all updates are recorded in $O(1)$ each, compute the running prefix sum of <code>diff</code> to reconstruct the final array in a single $O(n)$ pass!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Updating intervals directly takes $O(U \times N)$ time. Difference array executes updates in $O(1)$ and rebuilds in $O(N)$ time.</p>

<div class="insight">💡 <strong>Key insight:</strong> Difference array: <code>diff[start] += inc; diff[end + 1] -= inc</code>. Final array is the running cumulative prefix sum of <code>diff</code>. $O(U + N)$ total time!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def getModifiedArray(length: int, updates: list[list[int]]) -> list[int]:
    diff = [0] * (length + 1)
    
    # 1. Apply boundary markers in O(1)
    for start, end, inc in updates:
        diff[start] += inc
        diff[end + 1] -= inc
        
    # 2. Cumulative prefix sum in O(length)
    res = [0] * length
    curr = 0
    for i in range(length):
        curr += diff[i]
        res[i] = curr
        
    return res
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(U + N)$ where $U = \text{len}(updates)$ and $N = length$.<br>
<strong>Space:</strong> $O(N)$ — Difference buffer.</p>
''',
1094: '''<h2>🧭 How to think about it</h2>
<p>There is a car with <code>capacity</code> empty seats. The vehicle only drives east. Given integer <code>capacity</code> and array <code>trips = [numPassengers, from, to]</code>, return <code>true</code> if you can pick up and drop off all passengers without exceeding capacity.</p>

<p>This is range addition: passengers occupy the vehicle on half-open interval $[from, to)$!
Use a <strong>Difference Array</strong> over kilometers $0 \\dots 1000$:
- At departure $from$: passengers board $\to$ <code>diff[from] += passengers</code>.
- At arrival $to$: passengers get off $\to$ <code>diff[to] -= passengers</code>.</p>
<p>Sweep from kilometer 0 to 1000 tracking running passenger count:
If running passengers exceeds <code>capacity</code> at any kilometer, return <code>False</code>!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Difference array sweeps in $O(N + D)$ time where $D = 1001$ is the distance bound.</p>

<div class="insight">💡 <strong>Key insight:</strong> Difference array: <code>delta[from] += count; delta[to] -= count</code>. Running prefix sum tracks passengers aboard; reject if passenger count $> capacity$.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def carPooling(trips: list[list[int]], capacity: int) -> bool:
    # Max location is 1000
    timeline = [0] * 1001
    
    for passengers, start, end in trips:
        timeline[start] += passengers
        timeline[end] -= passengers
        
    curr_passengers = 0
    for count in timeline:
        curr_passengers += count
        if curr_passengers > capacity:
            return False
            
    return True
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(N + 1000)$ where $N$ is number of trips.<br>
<strong>Space:</strong> $O(1)$ — Fixed array of 1001 integers.</p>
''',
1109: '''<h2>🧭 How to think about it</h2>
<p>There are <code>n</code> flights that are labeled from <code>1</code> to <code>n</code>. You are given an array of flight bookings <code>bookings = [first, last, seats]</code>. Return an array <code>answer</code> of length <code>n</code> where <code>answer[i]</code> is the total number of seats reserved for flight <code>i</code>.</p>

<p>Standard <strong>Difference Array</strong> on 1-based indices $1 \\dots n$:
For each booking $[first, last, seats]$:
- <code>diff[first - 1] += seats</code>
- If $last < n$: <code>diff[last] -= seats</code>.</p>
<p>Running prefix sum of <code>diff</code> reconstructs total seats per flight in $O(n)$ time!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Adding seats to each flight range directly takes $O(B \times n)$ time. Difference array takes $O(B + n)$ linear time.</p>

<div class="insight">💡 <strong>Key insight:</strong> Difference array: <code>diff[first - 1] += seats; diff[last] -= seats</code>. Cumulative sum produces flight reservations in $O(B + n)$ time!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def corpFlightBookings(bookings: list[list[int]], n: int) -> list[int]:
    diff = [0] * (n + 1)
    
    for first, last, seats in bookings:
        diff[first - 1] += seats
        diff[last] -= seats
        
    res = [0] * n
    curr = 0
    for i in range(n):
        curr += diff[i]
        res[i] = curr
        
    return res
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(B + n)$ where $B$ is number of bookings.<br>
<strong>Space:</strong> $O(n)$ — Difference array of size $n+1$.</p>
''',
1310: '''<h2>🧭 How to think about it</h2>
<p>You are given an array <code>arr</code> of positive integers and an array <code>queries</code> where <code>queries[i] = [left_i, right_i]</code>. Return an array containing the XOR sum of all elements between $left_i$ and $right_i$ for each query.</p>

<p><strong>Prefix XOR Array:</strong>
Because XOR is its own inverse ($x \\oplus x = 0$):
$$\text{XOR}(arr[l \\dots r]) = \text{prefix_xor}[r + 1] \\oplus \text{prefix_xor}[l]$$
Everything from index $0$ to $l - 1$ cancels itself out to 0, leaving strictly the XOR sum of $arr[l \\dots r]$ in $O(1)$ time!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>XORing each query interval takes $O(Q \times n)$. Prefix XOR array answers each query in instant $O(1)$ time.</p>

<div class="insight">💡 <strong>Key insight:</strong> Prefix XOR: <code>pref[i] = pref[i-1] ^ arr[i-1]</code>. Range XOR $[l, r]$ is <code>pref[r + 1] ^ pref[l]</code> in strict $O(1)$!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def xorQueries(arr: list[int], queries: list[list[int]]) -> list[int]:
    prefix = [0]
    for x in arr:
        prefix.append(prefix[-1] ^ x)
        
    return [prefix[r + 1] ^ prefix[l] for l, r in queries]
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n + Q)$ — $O(n)$ prefix build, $O(1)$ per query.<br>
<strong>Space:</strong> $O(n)$ — Prefix XOR array.</p>
''',
}
