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

}
