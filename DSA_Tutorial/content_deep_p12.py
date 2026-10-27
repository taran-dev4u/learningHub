# -*- coding: utf-8 -*-
"""
Deep tutorials for Pattern 12: Dynamic Programming (DP) Patterns.
Masterclass 12-step structured explanations with ASCII dry runs and complexity analyses.
"""

DEEP = {
# ============================================================ LC 70: Climbing Stairs
70: '''<h2>🧭 How to think about it</h2>
<p>You are climbing a staircase. It takes <code>n</code> steps to reach the top. Each time you can either climb <code>1</code> or <code>2</code> steps. In how many distinct ways can you climb to the top?</p>

<p>To reach step <code>i</code>, you must take either a 1-step from step <code>i - 1</code> or a 2-step from step <code>i - 2</code>.
Therefore, the number of distinct ways to reach step <code>i</code> is the sum of ways to reach step <code>i - 1</code> and step <code>i - 2</code>:
$$dp[i] = dp[i - 1] + dp[i - 2]$$
This is the famous <strong>Fibonacci sequence</strong> with base cases <code>dp[1] = 1</code> and <code>dp[2] = 2</code>.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Naive recursion calculates overlapping subproblems exponentially: <code>O(2^N)</code>. Dynamic programming caches subproblems in <code>O(N)</code> time. Because each state only depends on the previous two values, we can reduce space to <code>O(1)</code> using two variables!</p>

<div class="insight">💡 <strong>Key insight:</strong> Maintain <code>prev1</code> (ways to reach step i - 1) and <code>prev2</code> (ways to reach step i - 2). At each step: <code>curr = prev1 + prev2; prev2 = prev1; prev1 = curr</code>. Runs in O(N) time with O(1) memory!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def climbStairs(n: int) -> int:
    """
    Computes distinct ways to reach step n using O(1) space Fibonacci DP.
    """
    if n <= 2:
        return n
        
    prev2, prev1 = 1, 2
    for _ in range(3, n + 1):
        curr = prev1 + prev2
        prev2 = prev1
        prev1 = curr
        
    return prev1
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(N)</code>. Single loop of N - 2 iterations.</li>
<li><strong>Space Complexity:</strong> <code>O(1)</code> constant extra space.</li>
</ul>''',

# ============================================================ LC 198: House Robber
198: '''<h2>🧭 How to think about it</h2>
<p>You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed. Adjacent houses have security systems connected: it will automatically contact the police if two adjacent houses were broken into on the same night. Return the maximum amount of money you can rob tonight without alerting the police.</p>

<p>At each house <code>i</code>, you have two mutually exclusive choices:
<ol>
  <li><strong>Rob house i:</strong> You earn <code>nums[i]</code>, but you cannot rob house <code>i - 1</code>. Thus your total is <code>nums[i] + max_loot_at(i - 2)</code>.</li>
  <li><strong>Skip house i:</strong> You keep the maximum loot possible up to house <code>i - 1</code>: <code>max_loot_at(i - 1)</code>.</li>
</ol>
The recurrence relation is:
$$dp[i] = \\max(dp[i - 1], dp[i - 2] + nums[i])$$</p>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def rob(nums: list[int]) -> int:
    """
    Finds maximum loot without robbing adjacent houses in O(N) time and O(1) space.
    """
    rob1, rob2 = 0, 0
    # rob1: max money robbed up to i - 2
    # rob2: max money robbed up to i - 1
    for num in nums:
        curr = max(rob2, rob1 + num)
        rob1 = rob2
        rob2 = curr
        
    return rob2
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(N)</code>. Single pass.</li>
<li><strong>Space Complexity:</strong> <code>O(1)</code>.</li>
</ul>''',

# ============================================================ LC 213: House Robber II
213: '''<h2>🧭 How to think about it</h2>
<p>All houses at this place are <strong>arranged in a circle</strong>. That means the first house is the neighbor of the last one. Meanwhile, adjacent houses have a security system connected. Return the maximum amount of money you can rob tonight without alerting the police.</p>

<div class="insight">💡 <strong>Key insight:</strong> Because house 0 and house <code>n - 1</code> are adjacent, you can NEVER rob both in the same night! This splits the circular problem into two linear subproblems:
<ol>
  <li>Rob houses from index <code>0</code> to <code>n - 2</code> (exclude last house).</li>
  <li>Rob houses from index <code>1</code> to <code>n - 1</code> (exclude first house).</li>
</ol>
The answer is simply <code>max(nums[0], rob_linear(nums[:-1]), rob_linear(nums[1:]))</code>!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def rob(nums: list[int]) -> int:
    """
    Solves circular house robber by taking maximum of two linear slices.
    """
    if len(nums) == 1:
        return nums[0]
        
    def rob_linear(houses):
        rob1, rob2 = 0, 0
        for h in houses:
            curr = max(rob2, rob1 + h)
            rob1 = rob2
            rob2 = curr
        return rob2
        
    return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(N)</code>. Two linear passes.</li>
<li><strong>Space Complexity:</strong> <code>O(1)</code>.</li>
</ul>''',

# ============================================================ LC 91: Decode Ways
91: '''<h2>🧭 How to think about it</h2>
<p>A message containing letters from <code>A-Z</code> can be encoded into numbers using the mapping <code>'A' &rarr; "1", 'B' &rarr; "2", ..., 'Z' &rarr; "26"</code>. Given a string <code>s</code> containing only digits, return the number of ways to decode it.</p>

<div class="insight">💡 <strong>Key insight:</strong> Let <code>dp[i]</code> be the number of ways to decode prefix <code>s[:i]</code>.
<ol>
  <li><strong>Single Digit:</strong> If <code>s[i - 1] != '0'</code>, the single digit <code>s[i-1]</code> is valid ('1'-'9') &rarr; <code>dp[i] += dp[i - 1]</code>.</li>
  <li><strong>Two Digits:</strong> If the two-digit substring <code>s[i-2:i]</code> is between <code>"10"</code> and <code>"26"</code> &rarr; <code>dp[i] += dp[i - 2]</code>.</li>
</ol></div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def numDecodings(s: str) -> int:
    """
    Computes decode ways via 1D DP with single and double digit transitions.
    """
    if not s or s[0] == '0':
        return 0
        
    n = len(s)
    dp = [0] * (n + 1)
    dp[0] = 1  # Base case: empty string has 1 way
    dp[1] = 1
    
    for i in range(2, n + 1):
        # 1. Single digit decode
        if s[i - 1] != '0':
            dp[i] += dp[i - 1]
            
        # 2. Two digit decode
        two_digit = int(s[i - 2:i])
        if 10 <= two_digit <= 26:
            dp[i] += dp[i - 2]
            
    return dp[n]
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(N)</code>. Single pass.</li>
<li><strong>Space Complexity:</strong> <code>O(N)</code> (can be reduced to <code>O(1)</code> using two variables).</li>
</ul>''',

# ============================================================ LC 53: Maximum Subarray
53: '''<h2>🧭 How to think about it</h2>
<p>Given an integer array <code>nums</code>, find the subarray with the largest sum, and return its sum.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Testing all subarrays takes <code>O(N^2)</code>. <strong>Kadane's Algorithm</strong> computes the global maximum subarray in a single linear pass in <code>O(N)</code> time and <code>O(1)</code> space!</p>

<div class="insight">💡 <strong>Key insight:</strong> At element <code>nums[i]</code>, we have two choices:
<ol>
  <li>Extend the existing subarray: <code>curr_sum + nums[i]</code>.</li>
  <li>Discard previous sum (if it was negative) and start a new subarray at <code>nums[i]</code>.</li>
</ol>
Thus: <code>curr_sum = max(nums[i], curr_sum + nums[i])</code>. Update <code>max_sum = max(max_sum, curr_sum)</code>.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def maxSubArray(nums: list[int]) -> int:
    """
    Kadane's algorithm for maximum subarray sum in O(N) time and O(1) space.
    """
    max_sum = nums[0]
    curr_sum = 0
    
    for x in nums:
        if curr_sum < 0:
            curr_sum = 0
        curr_sum += x
        if curr_sum > max_sum:
            max_sum = curr_sum
            
    return max_sum
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(N)</code>. Single pass.</li>
<li><strong>Space Complexity:</strong> <code>O(1)</code>.</li>
</ul>''',

# ============================================================ LC 322: Coin Change
322: '''<h2>🧭 How to think about it</h2>
<p>You are given an integer array <code>coins</code> representing coins of different denominations and an integer <code>amount</code>. Return the fewest number of coins that you need to make up that amount. If that amount cannot be made up by any combination, return <code>-1</code>. Each coin can be used an <strong>unlimited number of times</strong> (Unbounded Knapsack).</p>

<div class="insight">💡 <strong>Key insight:</strong> Let <code>dp[a]</code> be the minimum coins to form amount <code>a</code>.
For each amount <code>a</code> from <code>1</code> to <code>amount</code>:
$$dp[a] = \\min_{c \\in coins, c \\le a} (dp[a - c] + 1)$$
Initialize <code>dp = [inf] * (amount + 1)</code> with <code>dp[0] = 0</code>.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def coinChange(coins: list[int], amount: int) -> int:
    """
    Computes minimum coins to make amount using Unbounded Knapsack DP.
    """
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for a in range(1, amount + 1):
        for c in coins:
            if a >= c:
                dp[a] = min(dp[a], dp[a - c] + 1)
                
    return dp[amount] if dp[amount] != float('inf') else -1
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(amount &times; len(coins))</code>.</li>
<li><strong>Space Complexity:</strong> <code>O(amount)</code> for the DP array.</li>
</ul>''',

# ============================================================ LC 518: Coin Change II
518: '''<h2>🧭 How to think about it</h2>
<p>You are given an integer array <code>coins</code> and an integer <code>amount</code>. Return the number of combinations that make up that amount. Each coin may be used an unlimited number of times.</p>

<div class="insight">💡 <strong>Key insight: Combinations vs Permutations!</strong>
To count <strong>combinations</strong> (where <code>[1, 2]</code> and <code>[2, 1]</code> are the same combination):
The <strong>outer loop must iterate over coins</strong>, and the <strong>inner loop iterates over amounts</strong>!
<br><br>
If you iterate amounts in the outer loop, you would count permutations instead of combinations.
Recurrence: <code>dp[a] += dp[a - coin]</code>.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def change(amount: int, coins: list[int]) -> int:
    """
    Computes number of unique coin combinations to form amount.
    """
    dp = [0] * (amount + 1)
    dp[0] = 1
    
    # Outer loop over coins guarantees combination order
    for coin in coins:
        for a in range(coin, amount + 1):
            dp[a] += dp[a - coin]
            
    return dp[amount]
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(amount &times; len(coins))</code>.</li>
<li><strong>Space Complexity:</strong> <code>O(amount)</code>.</li>
</ul>''',

# ============================================================ LC 416: Partition Equal Subset Sum
416: '''<h2>🧭 How to think about it</h2>
<p>Given an integer array <code>nums</code>, return <code>true</code> if you can partition the array into two subsets such that the sum of the elements in both subsets is equal or <code>false</code> otherwise.</p>

<div class="insight">💡 <strong>Key insight:</strong>
1. Total sum must be even! If <code>sum(nums) % 2 != 0</code>, return <code>False</code>.
2. Target sum is <code>target = sum(nums) // 2</code>.
3. This is pure <strong>0-1 Knapsack Subset Sum</strong>: can we pick a subset of elements that sums exactly to <code>target</code>?
4. Space optimization: 1D boolean array <code>dp[j]</code>. Iterate <code>j</code> <strong>backwards from target down to num</strong> so that each number is used at most once!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def canPartition(nums: list[int]) -> bool:
    """
    Determines if array can be partitioned into two equal sum subsets via 0-1 Knapsack DP.
    """
    total = sum(nums)
    if total % 2 != 0:
        return False
        
    target = total // 2
    dp = [False] * (target + 1)
    dp[0] = True
    
    for num in nums:
        # Loop backwards to prevent reusing the same element
        for j in range(target, num - 1, -1):
            dp[j] = dp[j] or dp[j - num]
            
    return dp[target]
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(N &times; Target)</code> pseudo-polynomial time where <code>Target = sum(nums) / 2</code>.</li>
<li><strong>Space Complexity:</strong> <code>O(Target)</code>.</li>
</ul>''',

# ============================================================ LC 139: Word Break
139: '''<h2>🧭 How to think about it</h2>
<p>Given a string <code>s</code> and a dictionary of strings <code>wordDict</code>, return <code>true</code> if <code>s</code> can be segmented into a space-separated sequence of one or more dictionary words.</p>

<div class="insight">💡 <strong>Key insight:</strong> Let <code>dp[i]</code> be True if prefix <code>s[:i]</code> can be segmented into dictionary words.
<code>dp[0] = True</code> (empty string is always valid).
For <code>i</code> from <code>1</code> to <code>n</code>:
For <code>j</code> from <code>0</code> to <code>i</code>:
If <code>dp[j] == True</code> and substring <code>s[j:i]</code> is in <code>word_set</code> &rarr; set <code>dp[i] = True</code> and break!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def wordBreak(s: str, wordDict: list[str]) -> bool:
    """
    Validates if string can be segmented into dictionary words via 1D boolean DP.
    """
    word_set = set(wordDict)
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True
    
    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break
                
    return dp[n]
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(N^2 &times; K)</code> where <code>K</code> is average word length for string slicing and hashing.</li>
<li><strong>Space Complexity:</strong> <code>O(N)</code> for the DP array.</li>
</ul>''',

# ============================================================ LC 1143: Longest Common Subsequence
1143: '''<h2>🧭 How to think about it</h2>
<p>Given two strings <code>text1</code> and <code>text2</code>, return the length of their longest common subsequence. If there is no common subsequence, return <code>0</code>.</p>

<div class="insight">💡 <strong>Key insight:</strong> 2D Dynamic Programming table <code>dp[i][j]</code> representing LCS of prefixes <code>text1[:i]</code> and <code>text2[:j]</code>:
<ul>
  <li>If <code>text1[i - 1] == text2[j - 1]</code>: characters match! <code>dp[i][j] = 1 + dp[i - 1][j - 1]</code>.</li>
  <li>Else: characters differ! Skip one character from either string: <code>dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])</code>.</li>
</ul></div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def longestCommonSubsequence(text1: str, text2: str) -> int:
    """
    Computes length of LCS between two strings in O(M * N) time.
    """
    m, n = len(text1), len(text2)
    # dp[i][j] stores LCS length of text1[:i] and text2[:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = 1 + dp[i - 1][j - 1]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
                
    return dp[m][n]
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(M &times; N)</code> where <code>M = len(text1), N = len(text2)</code>.</li>
<li><strong>Space Complexity:</strong> <code>O(M &times; N)</code> (can be optimized to <code>O(min(M, N))</code> using a 1D rolling array).</li>
</ul>''',

# ============================================================ LC 72: Edit Distance
72: '''<h2>🧭 How to think about it</h2>
<p>Given two strings <code>word1</code> and <code>word2</code>, return the minimum number of operations required to convert <code>word1</code> to <code>word2</code>. You have three operations: Insert a character, Delete a character, Replace a character.</p>

<div class="insight">💡 <strong>Key insight:</strong> Let <code>dp[i][j]</code> be the edit distance between <code>word1[:i]</code> and <code>word2[:j]</code>:
<ul>
  <li>If <code>word1[i - 1] == word2[j - 1]</code>: no operation needed &rarr; <code>dp[i][j] = dp[i - 1][j - 1]</code>.</li>
  <li>Else: take 1 + minimum of the three operations:
    <ul>
      <li>Insert: <code>dp[i][j - 1]</code></li>
      <li>Delete: <code>dp[i - 1][j]</code></li>
      <li>Replace: <code>dp[i - 1][j - 1]</code></li>
    </ul>
    $$dp[i][j] = 1 + \\min(dp[i][j - 1], dp[i - 1][j], dp[i - 1][j - 1])$$
  </li>
</ul></div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def minDistance(word1: str, word2: str) -> int:
    """
    Computes Levenshtein edit distance between two strings in O(M * N) time.
    """
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Base cases: converting to/from empty string
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
        
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i][j - 1],     # Insert
                    dp[i - 1][j],     # Delete
                    dp[i - 1][j - 1]  # Replace
                )
                
    return dp[m][n]
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(M &times; N)</code>.</li>
<li><strong>Space Complexity:</strong> <code>O(M &times; N)</code>.</li>
</ul>''',

# ============================================================ LC 62: Unique Paths
62: '''<h2>🧭 How to think about it</h2>
<p>There is a robot on an <code>m x n</code> grid. The robot is initially located at the top-left corner <code>(0, 0)</code> and tries to move to the bottom-right corner <code>(m - 1, n - 1)</code>. The robot can only move either down or right at any point in time. How many possible unique paths are there?</p>

<div class="insight">💡 <strong>Key insight:</strong> To reach cell <code>(r, c)</code>, the robot must come from either <code>(r - 1, c)</code> (from above) or <code>(r, c - 1)</code> (from left).
Recurrence: <code>dp[r][c] = dp[r - 1][c] + dp[r][c - 1]</code>.
Using a 1D array of size <code>n</code>: <code>row[c] += row[c - 1]</code>.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def uniquePaths(m: int, n: int) -> int:
    """
    Computes unique grid paths using 1D space optimized DP in O(M * N) time and O(N) space.
    """
    row = [1] * n
    for _ in range(m - 1):
        for c in range(1, n):
            row[c] += row[c - 1]
    return row[-1]
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(M &times; N)</code>.</li>
<li><strong>Space Complexity:</strong> <code>O(N)</code>.</li>
</ul>''',

# ============================================================ LC 300: Longest Increasing Subsequence
300: '''<h2>🧭 How to think about it</h2>
<p>Given an integer array <code>nums</code>, return the length of the longest strictly increasing subsequence.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Traditional DP takes <code>O(N^2)</code>: <code>dp[i] = max(dp[j] + 1) for j < i if nums[j] < nums[i]</code>.
<strong>Patience Sorting with Binary Search</strong> finds the LIS in <code>O(N log N)</code> time!</p>

<div class="insight">💡 <strong>Key insight (Patience Sorting):</strong>
Maintain an array <code>tails</code> where <code>tails[i]</code> is the smallest tail element of all increasing subsequences of length <code>i + 1</code> found so far.
For each <code>x</code> in <code>nums</code>:
Binary search for the first element &ge; <code>x</code> in <code>tails</code> (using <code>bisect_left</code>):
<ul>
  <li>If <code>x</code> is larger than all elements in <code>tails</code>: append <code>x</code> to <code>tails</code> (extends LIS length!).</li>
  <li>Else: replace the element at index <code>idx</code> with <code>x</code> (lowers the tail value, making future extensions easier!).</li>
</ul>
At the end, <code>len(tails)</code> is the exact length of the LIS!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">from bisect import bisect_left

def lengthOfLIS(nums: list[int]) -> int:
    """
    Computes LIS length via Patience Sorting & Binary Search in O(N log N) time and O(N) space.
    """
    tails = []
    for x in nums:
        idx = bisect_left(tails, x)
        if idx == len(tails):
            tails.append(x)
        else:
            tails[idx] = x
            
    return len(tails)
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(N log N)</code>. For each of the N numbers, binary search takes <code>O(log N)</code>.</li>
<li><strong>Space Complexity:</strong> <code>O(N)</code> for the tails array.</li>
</ul>''',

# ============================================================ LC 516: Longest Palindromic Subsequence
516: '''<h2>🧭 How to think about it</h2>
<p>Given a string <code>s</code>, find the longest palindromic subsequence's length in <code>s</code>. A subsequence is a sequence that can be derived from another sequence by deleting some or no elements without changing the order of the remaining elements.</p>

<div class="insight">💡 <strong>Key insight:</strong>
Two equivalent approaches:
1. <strong>LCS with Reverse:</strong> The Longest Palindromic Subsequence of <code>s</code> is mathematically identical to the <strong>Longest Common Subsequence</strong> of <code>s</code> and its reverse <code>s[::-1]</code>!
2. <strong>Interval DP:</strong> Let <code>dp[i][j]</code> be LPS length in substring <code>s[i..j]</code>:
   - If <code>s[i] == s[j]</code>: <code>dp[i][j] = 2 + dp[i + 1][j - 1]</code>.
   - Else: <code>dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])</code>.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def longestPalindromeSubseq(s: str) -> int:
    """
    Computes LPS length via Interval DP in O(N^2) time and O(N) space.
    """
    n = len(s)
    # dp[j] stores LPS length for substring ending at j
    dp = [0] * n
    
    for i in range(n - 1, -1, -1):
        new_dp = [0] * n
        new_dp[i] = 1  # Single character palindrome
        for j in range(i + 1, n):
            if s[i] == s[j]:
                new_dp[j] = 2 + dp[j - 1]
            else:
                new_dp[j] = max(dp[j], new_dp[j - 1])
        dp = new_dp
        
    return dp[n - 1]
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(N^2)</code>.</li>
<li><strong>Space Complexity:</strong> <code>O(N)</code> rolling array space.</li>
</ul>''',


509: '''<h2>🧭 How to think about it</h2>
<p>The Fibonacci numbers form a sequence where each number is the sum of the two preceding ones, starting from <code>0</code> and <code>1</code>:</p>
<p>$$F(0) = 0, \\quad F(1) = 1, \\quad F(n) = F(n - 1) + F(n - 2) \\quad \\text{for } n \\ge 2$$</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Naive recursion computes the recurrence tree with branching factor 2, leading to exponential $O(2^n)$ time and $O(n)$ call stack depth. By recognizing that we only ever need the previous two terms ($F(i-1)$ and $F(i-2)$), we can iterate linearly with two variables, reducing time to $O(n)$ and space to $O(1)$.</p>

<div class="insight">💡 <strong>Key insight:</strong> Rolling state update with two scalar registers <code>a, b = b, a + b</code> computes the nth term in $O(n)$ time and $O(1)$ space. For astronomical $n$, Matrix Exponentiation or Binet's Formula solves it in $O(\\log n)$.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def fib(n: int) -> int:
    """
    Computes F(n) in O(n) time and O(1) space.
    """
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n)$ — Single linear pass from 2 to n.<br>
<strong>Space:</strong> $O(1)$ — Only two integer variables maintained.</p>
''',
746: '''<h2>🧭 How to think about it</h2>
<p>You are given an integer array <code>cost</code> where <code>cost[i]</code> is the cost of <code>i</code>-th step on a staircase. Once you pay the cost, you can either climb one or two steps. You can start from step <code>0</code> or step <code>1</code>. Return the minimum cost to reach the top floor (index <code>n</code>).</p>

<p>To stand on step <code>i</code>, you must have stepped from either <code>i - 1</code> or <code>i - 2</code>.
Therefore, the cost to reach step <code>i</code> is:
$$dp[i] = \\min(dp[i - 1] + cost[i - 1], \\; dp[i - 2] + cost[i - 2])$$</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Exploring both 1-step and 2-step choices recursively yields an $O(2^n)$ recurrence tree. Since subproblems overlap, we memoize or tabulate. Moreover, step <code>i</code> only depends on <code>dp[i - 1]</code> and <code>dp[i - 2]</code>, so two variables suffice for $O(1)$ auxiliary space.</p>

<div class="insight">💡 <strong>Key insight:</strong> Define <code>dp1</code> and <code>dp2</code> as the minimum cost to arrive at the current and previous steps. At each index, transition via <code>curr = min(dp1 + cost[i - 1], dp2 + cost[i - 2])</code>.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def minCostClimbingStairs(cost: list[int]) -> int:
    """
    Computes min cost to reach top floor using rolling DP.
    """
    # dp1: cost to reach step 1, dp2: cost to reach step 0
    dp2, dp1 = 0, 0
    for i in range(2, len(cost) + 1):
        curr = min(dp1 + cost[i - 1], dp2 + cost[i - 2])
        dp2, dp1 = dp1, curr
    return dp1
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n)$ — Single pass through the array.<br>
<strong>Space:</strong> $O(1)$ — Only two rolling variables.</p>
''',
1137: '''<h2>🧭 How to think about it</h2>
<p>The Tribonacci sequence $T_n$ is defined as:</p>
<p>$$T_0 = 0, \\quad T_1 = 1, \\quad T_2 = 1$$
$$T_{n+3} = T_n + T_{n+1} + T_{n+2} \\quad \\text{for } n \\ge 0$$</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Recursive branching of 3 yields $O(3^n)$ time. Rolling three registers ($t_0, t_1, t_2$) allows $O(n)$ computation in $O(1)$ extra memory.</p>

<div class="insight">💡 <strong>Key insight:</strong> Shift three scalar values on each step: <code>t0, t1, t2 = t1, t2, t0 + t1 + t2</code>.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def tribonacci(n: int) -> int:
    if n == 0:
        return 0
    if n <= 2:
        return 1
    t0, t1, t2 = 0, 1, 1
    for _ in range(3, n + 1):
        t0, t1, t2 = t1, t2, t0 + t1 + t2
    return t2
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n)$ — Linear iterative progression.<br>
<strong>Space:</strong> $O(1)$ — Three rolling variables.</p>
''',
740: '''<h2>🧭 How to think about it</h2>
<p>You are given an integer array <code>nums</code>. You want to maximize points earned. If you pick <code>nums[i]</code>, you earn <code>nums[i]</code> points, but must delete every element equal to <code>nums[i] - 1</code> and <code>nums[i] + 1</code>.</p>

<p>Notice the conflict: picking value <code>x</code> deletes all instances of <code>x - 1</code> and <code>x + 1</code>. But if you decide to take value <code>x</code>, you should take <strong>all</strong> occurrences of <code>x</code>, earning <code>x * count[x]</code> total points!</p>
<p>This transforms the problem exactly into <strong>House Robber (LC 198)</strong> over bucket values $0 \\dots \\max(nums)$. You cannot rob adjacent value buckets!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Trying all subsets of numbers is exponential. By aggregating total points per value into a frequency bucket array <code>points[v] = v * count[v]</code>, the recurrence is:
$$dp[v] = \\max(dp[v - 1], \\; dp[v - 2] + points[v])$$
which runs in $O(M)$ time where $M = \\max(nums)$.</p>

<div class="insight">💡 <strong>Key insight:</strong> Pre-aggregate into value buckets: <code>points[v] = v * frequency</code>. Then run standard House Robber <code>rob, skip = max(skip + points[v], rob), rob</code>.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">from collections import Counter

def deleteAndEarn(nums: list[int]) -> int:
    if not nums:
        return 0
    counts = Counter(nums)
    max_val = max(nums)
    
    prev2 = 0
    prev1 = 0
    
    for v in range(max_val + 1):
        gain = v * counts.get(v, 0)
        curr = max(prev1, prev2 + gain)
        prev2 = prev1
        prev1 = curr
        
    return prev1
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n + M)$ where $n = \\text{len}(nums)$ and $M = \\max(nums)$.<br>
<strong>Space:</strong> $O(n)$ for the frequency map, $O(1)$ DP registers.</p>
''',
337: '''<h2>🧭 How to think about it</h2>
<p>The thief has found himself in a new neighborhood where houses form a binary tree. If two directly-linked houses are broken into on the same night, the alarm automatically alerts the police. Find the maximum amount of money the thief can rob without alerting the police.</p>

<p>For any subtree rooted at <code>node</code>, the thief has two mutual exclusive choices:
1. <strong>Rob this node:</strong> We gain <code>node.val</code>, but we <strong>cannot</strong> rob either of its immediate children. We must take the optimal "not robbed" values from both children.
2. <strong>Do not rob this node:</strong> We are free to either rob or not rob each child independently (taking $\\max(\\text{rob}, \\text{not\\_rob})$ for each).</p>

<h2>🐢 Brute force vs optimal</h2>
<p>A naive recursive approach checking grandparents causes exponential recomputations. Instead, post-order DFS returns a tuple <code>(rob_node, not_rob_node)</code> for each subtree in a single bottom-up pass in $O(n)$ time.</p>

<div class="insight">💡 <strong>Key insight:</strong> Post-order traversal returns <code>(rob, not_rob)</code>:
<br><code>rob = node.val + left_not_rob + right_not_rob</code>
<br><code>not_rob = max(left_rob, left_not_rob) + max(right_rob, right_not_rob)</code>.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def rob(root) -> int:
    def dfs(node):
        if not node:
            return (0, 0) # (rob_this, skip_this)
            
        left_rob, left_skip = dfs(node.left)
        right_rob, right_skip = dfs(node.right)
        
        # If we rob this node, we cannot rob left or right children
        rob_curr = node.val + left_skip + right_skip
        
        # If we skip this node, children can either be robbed or skipped
        skip_curr = max(left_rob, left_skip) + max(right_rob, right_skip)
        
        return (rob_curr, skip_curr)
        
    return max(dfs(root))
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n)$ — Every tree node is visited exactly once.<br>
<strong>Space:</strong> $O(h)$ — Call stack height where $h$ is tree height ($O(\\log n)$ balanced, $O(n)$ skewed).</p>
''',
279: '''<h2>🧭 How to think about it</h2>
<p>Given an integer <code>n</code>, return the least number of perfect square numbers that sum to <code>n</code>. A perfect square is an integer that is the square of an integer (e.g., 1, 4, 9, 16...).</p>

<p>This is an <strong>unbounded knapsack</strong> problem where coin values are squares $1, 4, 9, \\dots, s^2 \\le n$.
Let $dp[i]$ be the minimum number of square numbers summing to $i$:
$$dp[i] = 1 + \\min_{j \\times j \\le i} dp[i - j \\times j]$$</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Exhaustive search is exponential. Dynamic programming tabulates bottom-up in $O(n \\sqrt{n})$ time. Alternatively, Legendre's Three-Square Theorem classifies answers into 1, 2, 3, or 4 in $O(\\sqrt{n})$ time.</p>

<div class="insight">💡 <strong>Key insight:</strong> Standard 1D DP: initialize $dp[0]=0, dp[i]=\\infty$. For each $i$ from 1 to $n$, iterate over all $j \\times j \\le i$ and minimize $1 + dp[i - j^2]$.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def numSquares(n: int) -> int:
    dp = [float('inf')] * (n + 1)
    dp[0] = 0
    
    # Precompute squares <= n
    squares = [j * j for j in range(1, int(n**0.5) + 1)]
    
    for i in range(1, n + 1):
        for sq in squares:
            if sq > i:
                break
            if dp[i - sq] + 1 < dp[i]:
                dp[i] = dp[i - sq] + 1
                
    return dp[n]
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n \\sqrt{n})$ — Outer loop runs $n$ times; inner loop runs $\\sqrt{n}$ times.<br>
<strong>Space:</strong> $O(n)$ — 1D array of size $n+1$.</p>
''',
377: '''<h2>🧭 How to think about it</h2>
<p>Given an array of distinct integers <code>nums</code> and a target integer <code>target</code>, return the number of possible combinations that add up to <code>target</code>. Note that different sequences (order matters, e.g., <code>[1, 2]</code> and <code>[2, 1]</code>) are counted as different permutations.</p>

<p>Because order matters, this is counting permutations! To reach target sum <code>i</code>, the last number chosen could be any <code>num \\in nums</code> where <code>num <= i</code>:
$$dp[i] = \\sum_{num \\in nums, num \\le i} dp[i - num]$$
with base case $dp[0] = 1$ (one way to form sum 0: empty set).</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Notice the loop order:
- In <strong>Coin Change II (LC 518)</strong> (combinations, order does NOT matter), outer loop is coins, inner loop is amounts.
- In <strong>Combination Sum IV (LC 377)</strong> (permutations, order DOES matter), outer loop is target amounts $1 \\dots \\text{target}$, inner loop is numbers!</p>

<div class="insight">💡 <strong>Key insight:</strong> Loop targets outer, coins inner: <code>for i in range(1, target + 1): for x in nums: dp[i] += dp[i - x]</code>.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def combinationSum4(nums: list[int], target: int) -> int:
    dp = [0] * (target + 1)
    dp[0] = 1
    
    for i in range(1, target + 1):
        for num in nums:
            if i >= num:
                dp[i] += dp[i - num]
                
    return dp[target]
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(\\text{target} \\times |nums|)$ — Nested iterations.<br>
<strong>Space:</strong> $O(\\text{target})$ — 1D DP table.</p>
''',
494: '''<h2>🧭 How to think about it</h2>
<p>You are given an integer array <code>nums</code> and an integer <code>target</code>. Build an expression by adding <code>+</code> or <code>-</code> before each integer in <code>nums</code>. Return the number of different expressions that evaluate to <code>target</code>.</p>

<p>Divide <code>nums</code> into two disjoint subsets: $P$ (elements assigned <code>+</code>) and $N$ (elements assigned <code>-</code>).
$$\\sum P - \\sum N = \\text{target}$$
Adding $\\sum P + \\sum N = \\text{total\\_sum}$ to both sides:
$$2 \\times \\sum P = \\text{target} + \\text{total\\_sum} \\implies \\sum P = \\frac{\\text{target} + \\text{total\\_sum}}{2}$$</p>
<p>This transforms Target Sum into finding the number of subsets with sum $S = (\\text{target} + \\text{total\\_sum}) / 2$ — standard <strong>0-1 Knapsack Subset Sum</strong>!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Trying all $2^n$ sign assignments is $O(2^n)$. The subset sum reduction solves it in $O(n \\times S)$ time with 1D space rolling backwards!</p>

<div class="insight">💡 <strong>Key insight:</strong> Check parity: if <code>target + total_sum</code> is odd or <code>abs(target) > total_sum</code>, return 0. Otherwise, count subsets with target sum $S$ traversing backward to prevent reusing elements.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def findTargetSumWays(nums: list[int], target: int) -> int:
    total = sum(nums)
    if (target + total) % 2 != 0 or abs(target) > total:
        return 0
        
    s = (target + total) // 2
    dp = [0] * (s + 1)
    dp[0] = 1
    
    for num in nums:
        for j in range(s, num - 1, -1):
            dp[j] += dp[j - num]
            
    return dp[s]
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n \\times S)$ where $S = (\\text{target} + \\text{total}) / 2$.<br>
<strong>Space:</strong> $O(S)$ — 1D space optimized backward traversal.</p>
''',
140: '''<h2>🧭 How to think about it</h2>
<p>Given a string <code>s</code> and a dictionary of strings <code>wordDict</code>, add spaces in <code>s</code> to construct a sentence where each word is a valid dictionary word. Return all such possible sentences in any order.</p>

<p>Unlike <strong>Word Break I (LC 139)</strong> which asks for a boolean existence, Word Break II asks to construct <em>all</em> sentences. If every partition is valid, the number of outputs can be exponential (e.g. <code>s = "aaaaa", wordDict = ["a", "aa"]</code>). We use <strong>memoized backtracking (top-down DP)</strong> to cache results for subproblems <code>dfs(i)</code> returning all valid suffixes starting at index <code>i</code>.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Plain backtracking explores overlapping suffixes multiple times. Memoizing <code>memo[i] = list of valid sentences for s[i:]</code> ensures each unique suffix is computed only once, skipping doomed branches instantly.</p>

<div class="insight">💡 <strong>Key insight:</strong> Top-down DFS with memoization: <code>memo[start]</code> stores all valid sentences formable from suffix <code>s[start:]</code>. Prunes dead ends immediately.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def wordBreak(s: str, wordDict: list[str]) -> list[str]:
    word_set = set(wordDict)
    memo = {}
    
    def dfs(start: int) -> list[str]:
        if start in memo:
            return memo[start]
        if start == len(s):
            return [""]
            
        res = []
        for end in range(start + 1, len(s) + 1):
            word = s[start:end]
            if word in word_set:
                sub_sentences = dfs(end)
                for sub in sub_sentences:
                    res.append(word + ("" if not sub else " " + sub))
                    
        memo[start] = res
        return res
        
    return dfs(0)
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n^2 + 2^n)$ in worst-case dense matchings, but heavily pruned in practice.<br>
<strong>Space:</strong> $O(n \\times 2^n)$ to store all reconstructed paths and recursion stack.</p>
''',
63: '''<h2>🧭 How to think about it</h2>
<p>You are given an <code>m x n</code> integer array <code>obstacleGrid</code>. A <code>1</code> represents an obstacle and <code>0</code> represents an empty space. A robot starts at the top-left corner and moves only down or right. Return the number of unique paths to the bottom-right corner.</p>

<p>Transition rule:
- If <code>obstacleGrid[i][j] == 1</code>, $dp[i][j] = 0$ (impassable!).
- If <code>obstacleGrid[i][j] == 0</code>, $dp[i][j] = dp[i - 1][j] + dp[i][j - 1]$.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Instead of an $m \\times n$ 2D matrix, we only need the current row and the row above. We can reduce space to $O(n)$ using a 1D rolling array!</p>

<div class="insight">💡 <strong>Key insight:</strong> 1D DP: <code>dp[j]</code> represents paths to cell $(i, j)$. If cell has obstacle, set <code>dp[j] = 0</code>. Otherwise add left neighbor: <code>dp[j] += dp[j - 1]</code>.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def uniquePathsWithObstacles(obstacleGrid: list[list[int]]) -> int:
    if not obstacleGrid or obstacleGrid[0][0] == 1:
        return 0
        
    m, n = len(obstacleGrid), len(obstacleGrid[0])
    dp = [0] * n
    dp[0] = 1
    
    for r in range(m):
        for c in range(n):
            if obstacleGrid[r][c] == 1:
                dp[c] = 0
            elif c > 0:
                dp[c] += dp[c - 1]
                
    return dp[n - 1]
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(m \\times n)$ — Every cell evaluated once.<br>
<strong>Space:</strong> $O(n)$ — Single 1D array of width $n$.</p>
''',
64: '''<h2>🧭 How to think about it</h2>
<p>Given an <code>m x n</code> grid filled with non-negative numbers, find a path from top left to bottom right which minimizes the sum of all numbers along its path. You can only move down or right.</p>

<p>At cell $(i, j)$, you arrived from either $(i - 1, j)$ or $(i, j - 1)$:
$$dp[i][j] = grid[i][j] + \\min(dp[i - 1][j], \\; dp[i][j - 1])$$</p>

<h2>🐢 Brute force vs optimal</h2>
<p>We can solve this with $O(n)$ extra space using a 1D array, or even $O(1)$ extra space by updating <code>grid</code> in place.</p>

<div class="insight">💡 <strong>Key insight:</strong> Maintain 1D array: <code>dp[c] = grid[r][c] + min(dp[c], dp[c - 1])</code>.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def minPathSum(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    dp = [float('inf')] * n
    dp[0] = 0
    
    for r in range(m):
        dp[0] += grid[r][0]
        for c in range(1, n):
            dp[c] = grid[r][c] + min(dp[c], dp[c - 1])
            
    return dp[-1]
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(m \\times n)$ — Grid traversed cell by cell.<br>
<strong>Space:</strong> $O(n)$ — 1D array of width $n$.</p>
''',
120: '''<h2>🧭 How to think about it</h2>
<p>Given a <code>triangle</code> array, return the minimum path sum from top to bottom. For each step, you may move to an adjacent number on the row below (i.e. from index <code>i</code> on current row to index <code>i</code> or <code>i + 1</code> on the next row).</p>

<p>Top-down DP requires handling boundary conditions. <strong>Bottom-up DP</strong> starting from the base of the triangle is vastly cleaner and eliminates all edge cases!</p>
<p>$$dp[j] = \\text{triangle}[r][j] + \\min(dp[j], \\; dp[j + 1])$$</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Starting from the bottom row, collapse upwards row by row. At the top, <code>dp[0]</code> contains the global minimum path sum!</p>

<div class="insight">💡 <strong>Key insight:</strong> Initialize <code>dp = triangle[-1][:]</code>. Iterate from row $n-2$ down to 0, updating <code>dp[c] = triangle[r][c] + min(dp[c], dp[c + 1])</code>.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def minimumTotal(triangle: list[list[int]]) -> int:
    dp = triangle[-1][:]
    
    for r in range(len(triangle) - 2, -1, -1):
        for c in range(len(triangle[r])):
            dp[c] = triangle[r][c] + min(dp[c], dp[c + 1])
            
    return dp[0]
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(N)$ where $N$ is total number of cells in triangle ($n(n+1)/2$).<br>
<strong>Space:</strong> $O(n)$ — 1D buffer the length of the bottom row.</p>
''',
221: '''<h2>🧭 How to think about it</h2>
<p>Given an <code>m x n</code> binary matrix filled with <code>'0'</code>s and <code>'1'</code>s, find the largest square containing only <code>'1'</code>s and return its area.</p>

<p>Let $dp[i][j]$ be the side length of the largest square whose <strong>bottom-right corner</strong> is at $(i, j)$.
If <code>matrix[i][j] == '1'</code>, $(i, j)$ can extend a square only if its top, left, and top-left diagonal neighbors can also form squares:
$$dp[i][j] = 1 + \\min(dp[i - 1][j], \\; dp[i][j - 1], \\; dp[i - 1][j - 1])$$
If <code>matrix[i][j] == '0'</code>, $dp[i][j] = 0$.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Checking every possible square of size $k \\times k$ takes $O(m \\times n \\times \\min(m, n)^2)$ which is $O((m \\cdot n)^2)$. DP reduces this to a single pass $O(m \\cdot n)$ with $O(n)$ space.</p>

<div class="insight">💡 <strong>Key insight:</strong> The bottom-right corner of a square of size $k$ requires size $k-1$ from top, left, and top-left diagonal simultaneously.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def maximalSquare(matrix: list[list[str]]) -> int:
    if not matrix:
        return 0
    m, n = len(matrix), len(matrix[0])
    dp = [0] * (n + 1)
    max_side = 0
    prev_diag = 0
    
    for r in range(m):
        prev_diag = 0
        for c in range(n):
            temp = dp[c + 1]
            if matrix[r][c] == '1':
                dp[c + 1] = 1 + min(dp[c], dp[c + 1], prev_diag)
                max_side = max(max_side, dp[c + 1])
            else:
                dp[c + 1] = 0
            prev_diag = temp
            
    return max_side * max_side
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(m \\times n)$ — Each cell visited once.<br>
<strong>Space:</strong> $O(n)$ — Single 1D row array.</p>
''',
931: '''<h2>🧭 How to think about it</h2>
<p>Given an <code>n x n</code> array of integers <code>matrix</code>, return the minimum sum of any falling path through <code>matrix</code>. A falling path starts at any element in the first row and chooses the element in the next row that is either directly below or diagonally left/right.</p>

<p>$$dp[r][c] = matrix[r][c] + \\min(dp[r - 1][c - 1], \\; dp[r - 1][c], \\; dp[r - 1][c + 1])$$</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Branching factor 3 at each row yields $O(3^n)$ recursion. Standard DP computes row by row in $O(n^2)$ time and $O(n)$ memory.</p>

<div class="insight">💡 <strong>Key insight:</strong> Rolling 1D array: <code>dp[c] = matrix[r][c] + min(prev[max(0, c-1) : min(n, c+2)])</code>.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def minFallingPathSum(matrix: list[list[int]]) -> int:
    n = len(matrix)
    dp = matrix[0][:]
    
    for r in range(1, n):
        new_dp = [0] * n
        for c in range(n):
            best_prev = dp[c]
            if c > 0:
                best_prev = min(best_prev, dp[c - 1])
            if c < n - 1:
                best_prev = min(best_prev, dp[c + 1])
            new_dp[c] = matrix[r][c] + best_prev
        dp = new_dp
        
    return min(dp)
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n^2)$ — $n \\times n$ matrix cells.<br>
<strong>Space:</strong> $O(n)$ — Single row of size $n$.</p>
''',
1277: '''<h2>🧭 How to think about it</h2>
<p>Given a <code>m * n</code> matrix of ones and zeros, return how many square submatrices have all ones.</p>

<p>Recall <strong>Maximal Square (LC 221)</strong>: if $dp[i][j] = k$, it means the largest square ending at $(i, j)$ has side length $k$. That automatically implies there are squares of side length $1, 2, \\dots, k$ all sharing $(i, j)$ as their bottom-right corner!
Therefore, the number of square submatrices with bottom-right corner at $(i, j)$ is exactly $dp[i][j]$!</p>
<p>$$\\text{Total Squares} = \\sum_{i, j} dp[i][j]$$</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Iterating all submatrices takes $O(m \\cdot n \\cdot \\min(m, n))$. With DP, each cell is $O(1)$, so total time is $O(m \\cdot n)$!</p>

<div class="insight">💡 <strong>Key insight:</strong> <code>dp[i][j]</code> is both the maximum side length AND the exact count of squares whose bottom-right corner is at $(i, j)$. Simply sum all <code>dp[i][j]</code>!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def countSquares(matrix: list[list[int]]) -> int:
    m, n = len(matrix), len(matrix[0])
    total = 0
    
    for r in range(m):
        for c in range(n):
            if matrix[r][c] == 1:
                if r > 0 and c > 0:
                    matrix[r][c] = 1 + min(matrix[r - 1][c], matrix[r][c - 1], matrix[r - 1][c - 1])
                total += matrix[r][c]
                
    return total
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(m \\times n)$ — Single pass in place.<br>
<strong>Space:</strong> $O(1)$ — Modified in place (or $O(n)$ if matrix immutable).</p>
''',
}