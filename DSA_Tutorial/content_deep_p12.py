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

97: '''<h2>🧭 How to think about it</h2>
<p>Given strings <code>s1</code>, <code>s2</code>, and <code>s3</code>, determine whether <code>s3</code> is formed by an interleaving of <code>s1</code> and <code>s2</code>.</p>

<p>First, check the lengths: if $\\text{len}(s1) + \\text{len}(s2) \ne \\text{len}(s3)$, return <code>False</code> immediately.
Let $dp[i][j]$ be a boolean indicating whether the prefix $s3[0 \\dots i+j-1]$ can be formed by interleaving $s1[0 \\dots i-1]$ and $s2[0 \\dots j-1]$.</p>

<p>At position $(i, j)$ corresponding to character $s3[i + j - 1]$:
1. If $s1[i - 1] == s3[i + j - 1]$ and $dp[i - 1][j]$ is true, then $dp[i][j] = \\text{True}$.
2. If $s2[j - 1] == s3[i + j - 1]$ and $dp[i][j - 1]$ is true, then $dp[i][j] = \\text{True}$.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Naive recursion explores branching paths in $O(2^{m+n})$. Dynamic programming caches intermediate prefixes in an $(m+1) \\times (n+1)$ table in $O(m \\times n)$ time and can be compressed to $O(n)$ space.</p>

<div class="insight">💡 <strong>Key insight:</strong> Rolling 1D array of size $n+1$: <code>dp[j] = (dp[j] and s1[i-1] == s3[i+j-1]) or (dp[j-1] and s2[j-1] == s3[i+j-1])</code>.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def isInterleave(s1: str, s2: str, s3: str) -> bool:
    m, n, l = len(s1), len(s2), len(s3)
    if m + n != l:
        return False
        
    dp = [False] * (n + 1)
    dp[0] = True
    
    # Base row: using only s2
    for j in range(1, n + 1):
        dp[j] = dp[j - 1] and s2[j - 1] == s3[j - 1]
        
    for i in range(1, m + 1):
        dp[0] = dp[0] and s1[i - 1] == s3[i - 1]
        for j in range(1, n + 1):
            char_s3 = s3[i + j - 1]
            from_s1 = dp[j] and s1[i - 1] == char_s3
            from_s2 = dp[j - 1] and s2[j - 1] == char_s3
            dp[j] = from_s1 or from_s2
            
    return dp[n]
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(m \\times n)$ where $m = \\text{len}(s1), n = \\text{len}(s2)$.<br>
<strong>Space:</strong> $O(n)$ — Rolling 1D boolean array.</p>
''',
115: '''<h2>🧭 How to think about it</h2>
<p>Given two strings <code>s</code> and <code>t</code>, return the number of distinct subsequences of <code>s</code> which equals <code>t</code>.</p>

<p>Let $dp[i][j]$ be the number of distinct subsequences of $s[0 \\dots i-1]$ that equal $t[0 \\dots j-1]$.
- If $s[i - 1] == t[j - 1]$, we have two choices:
  1. <strong>Match this character:</strong> add $dp[i - 1][j - 1]$ (match $s[i-1]$ with $t[j-1]$).
  2. <strong>Skip this character:</strong> add $dp[i - 1][j]$ (look for $t[0 \\dots j-1]$ earlier in $s$).
  $$dp[i][j] = dp[i - 1][j - 1] + dp[i - 1][j]$$
- If $s[i - 1] \ne t[j - 1]$, we cannot match, so:
  $$dp[i][j] = dp[i - 1][j]$$</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Generating all $2^{|s|}$ subsequences is impossibly slow. 2D DP computes the answer in $O(|s| \\times |t|)$ time. Traversing <code>j</code> backwards optimizes space to $O(|t|)$!</p>

<div class="insight">💡 <strong>Key insight:</strong> 1D array backwards: if $s[i-1] == t[j-1]$, <code>dp[j] += dp[j - 1]</code> with base case <code>dp[0] = 1</code> (empty string $t$ has 1 subsequence in any prefix of $s$).</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def numDistinct(s: str, t: str) -> int:
    m, n = len(s), len(t)
    if m < n:
        return 0
        
    dp = [0] * (n + 1)
    dp[0] = 1
    
    for char_s in s:
        for j in range(n, 0, -1):
            if char_s == t[j - 1]:
                dp[j] += dp[j - 1]
                
    return dp[n]
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(m \\times n)$ — Nested string traversal.<br>
<strong>Space:</strong> $O(n)$ — 1D space traversing right-to-left.</p>
''',
583: '''<h2>🧭 How to think about it</h2>
<p>Given two strings <code>word1</code> and <code>word2</code>, return the minimum number of steps required to make <code>word1</code> and <code>word2</code> the same. In one step, you can delete exactly one character in either string.</p>

<p>To make both strings equal with minimum deletions, we should preserve the <strong>Longest Common Subsequence (LCS)</strong> of the two strings!
Let $L = \\text{LCS}(word1, word2)$.
Every character not in the LCS must be deleted.
$$\\text{Min Deletions} = (\\text{len}(word1) - L) + (\\text{len}(word2) - L) = \\text{len}(word1) + \\text{len}(word2) - 2L$$</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Computing all common subsequences takes exponential time. Standard 2D LCS DP runs in $O(m \\times n)$ time and $O(n)$ space.</p>

<div class="insight">💡 <strong>Key insight:</strong> Min deletions $= m + n - 2 \\times \\text{LCS}(s1, s2)$. Reduces directly to Longest Common Subsequence!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def minDistance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    dp = [0] * (n + 1)
    
    for i in range(1, m + 1):
        prev_diag = 0
        for j in range(1, n + 1):
            temp = dp[j]
            if word1[i - 1] == word2[j - 1]:
                dp[j] = prev_diag + 1
            else:
                dp[j] = max(dp[j], dp[j - 1])
            prev_diag = temp
            
    lcs = dp[n]
    return m + n - 2 * lcs
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(m \\times n)$ — Standard LCS calculation.<br>
<strong>Space:</strong> $O(n)$ — 1D rolling array.</p>
''',
10: '''<h2>🧭 How to think about it</h2>
<p>Given an input string <code>s</code> and a pattern <code>p</code>, implement regular expression matching with support for <code>'.'</code> and <code>'*'</code>:
- <code>'.'</code> Matches any single character.
- <code>'*'</code> Matches zero or more of the preceding element.</p>

<p>Let $dp[i][j]$ be whether $s[0 \\dots i-1]$ matches $p[0 \\dots j-1]$.
1. <strong>Exact match or '.' :</strong>
   If $p[j - 1] == s[i - 1]$ or $p[j - 1] == \\text{'.'}$, then $dp[i][j] = dp[i - 1][j - 1]$.
2. <strong>Star '*' :</strong>
   If $p[j - 1] == \\text{'*'}$, look at the preceding element $p[j - 2]$:
   - <strong>Zero occurrences:</strong> ignore the star and preceding char: $dp[i][j] = dp[i][j - 2]$.
   - <strong>One or more occurrences:</strong> if $s[i - 1]$ matches $p[j - 2]$ (or $p[j-2] == \\text{'.'}$, then $dp[i][j] = dp[i][j] \\lor dp[i - 1][j]$.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Star wildcards create recursive trees of depth $O(2^{m+n})$. Memoizing subproblems on the $(m+1) \\times (n+1)$ state grid solves it in $O(m \\times n)$ time.</p>

<div class="insight">💡 <strong>Key insight:</strong> For '*': <code>dp[i][j] = dp[i][j - 2]</code> (zero occurrences) or <code>(matches(s[i-1], p[j-2]) and dp[i - 1][j])</code> (consume one more char from s).</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def isMatch(s: str, p: str) -> bool:
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True
    
    # Handle patterns like a*, a*b*, a*b*c* matching empty string s
    for j in range(2, n + 1):
        if p[j - 1] == '*':
            dp[0][j] = dp[0][j - 2]
            
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j - 1] == '*':
                # Case 1: zero occurrences of preceding element
                dp[i][j] = dp[i][j - 2]
                # Case 2: one or more occurrences
                if p[j - 2] == '.' or p[j - 2] == s[i - 1]:
                    dp[i][j] = dp[i][j] or dp[i - 1][j]
            elif p[j - 1] == '.' or p[j - 1] == s[i - 1]:
                dp[i][j] = dp[i - 1][j - 1]
                
    return dp[m][n]
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(m \\times n)$ — Grid filled cell by cell.<br>
<strong>Space:</strong> $O(m \\times n)$ — 2D DP matrix (can be optimized to $O(n)$).</p>
''',
44: '''<h2>🧭 How to think about it</h2>
<p>Given an input string <code>s</code> and a pattern <code>p</code>, implement wildcard pattern matching with support for <code>'?'</code> and <code>'*'</code>:
- <code>'?'</code> Matches any single character.
- <code>'*'</code> Matches any sequence of characters (including the empty sequence).</p>

<p>Notice the critical difference from Regex (LC 10): in Wildcard, <code>'*'</code> stands by itself and matches any sequence, without needing a preceding character!
- If $p[j - 1] == \\text{'?'}$ or $p[j - 1] == s[i - 1]$: $dp[i][j] = dp[i - 1][j - 1]$.
- If $p[j - 1] == \\text{'*'}'$: $dp[i][j] = dp[i][j - 1] \\lor dp[i - 1][j]$
  - $dp[i][j - 1]$ means '*' matches empty string.
  - $dp[i - 1][j]$ means '*' matches at least one character (consumes $s[i-1]$).</p>

<h2>🐢 Brute force vs optimal</h2>
<p>2D DP takes $O(m \\times n)$ time. Alternatively, a greedy two-pointer approach tracking the last seen '*' and match index runs in $O(m)$ average time with $O(1)$ space!</p>

<div class="insight">💡 <strong>Key insight:</strong> Greedy two-pointer: record <code>star_idx</code> and <code>match_idx</code>. When mismatch occurs, backtrack to <code>star_idx</code>, expand match length by 1, and resume.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def isMatch(s: str, p: str) -> bool:
    s_idx, p_idx = 0, 0
    star_idx = -1
    match_idx = 0
    
    while s_idx < len(s):
        # 1. Characters match or pattern has '?'
        if p_idx < len(p) and (p[p_idx] == '?' or p[p_idx] == s[s_idx]):
            s_idx += 1
            p_idx += 1
        # 2. Pattern has '*'
        elif p_idx < len(p) and p[p_idx] == '*':
            star_idx = p_idx
            match_idx = s_idx
            p_idx += 1
        # 3. Last pattern char was '*' - backtrack and match one more char in s
        elif star_idx != -1:
            p_idx = star_idx + 1
            match_idx += 1
            s_idx = match_idx
        # 4. Mismatch and no '*' to fall back on
        else:
            return False
            
    # Check remaining chars in pattern (must all be '*')
    while p_idx < len(p) and p[p_idx] == '*':
        p_idx += 1
        
    return p_idx == len(p)
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(m)$ average, $O(m \\times n)$ worst case (e.g. <code>s="aaaa", p="*a"</code>).<br>
<strong>Space:</strong> $O(1)$ — Only a few pointer variables.</p>
''',
87: '''<h2>🧭 How to think about it</h2>
<p>We can scramble a string <code>s</code> to get a string <code>t</code> using the following algorithm:
1. If the length of the string is 1, stop.
2. Split string into two non-empty substrings at any index.
3. Randomly choose whether to swap the two substrings or leave them as is.
4. Apply the algorithm recursively on each substring.</p>

<p>Given <code>s1</code> and <code>s2</code> of length $n$, can <code>s2</code> be formed by scrambling <code>s1</code>?</p>

<p>For any split index $k \\in [1, n-1]$:
1. <strong>Without Swap:</strong> $s1[0 \\dots k]$ scrambles to $s2[0 \\dots k]$ AND $s1[k \\dots n]$ scrambles to $s2[k \\dots n]$.
2. <strong>With Swap:</strong> $s1[0 \\dots k]$ scrambles to $s2[n-k \\dots n]$ AND $s1[k \\dots n]$ scrambles to $s2[0 \\dots n-k]$.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Top-down memoized recursion with a frequency character pruning check. If <code>sorted(s1) != sorted(s2)</code>, return <code>False</code> immediately without branching!</p>

<div class="insight">💡 <strong>Key insight:</strong> Memoize <code>(s1, s2)</code>. Prune early using <code>Counter(s1) != Counter(s2)</code>. For each split $k$, check (no_swap) or (swap).</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">from collections import Counter
from functools import lru_cache

def isScramble(s1: str, s2: str) -> bool:
    @lru_cache(maxsize=None)
    def dfs(a: str, b: str) -> bool:
        if a == b:
            return True
        if Counter(a) != Counter(b):
            return False
            
        n = len(a)
        for k in range(1, n):
            # Case 1: no swap
            if dfs(a[:k], b[:k]) and dfs(a[k:], b[k:]):
                return True
            # Case 2: swapped
            if dfs(a[:k], b[n - k:]) and dfs(a[k:], b[:n - k]):
                return True
                
        return False
        
    return dfs(s1, s2)
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n^4)$ states with memoization.<br>
<strong>Space:</strong> $O(n^3)$ memoization cache and recursion stack.</p>
''',
95: '''<h2>🧭 How to think about it</h2>
<p>Given an integer <code>n</code>, return all structurally unique BST's (binary search trees) which has exactly <code>n</code> nodes of unique values from <code>1</code> to <code>n</code>.</p>

<p>Every number $i \\in [1, n]$ can serve as the root node.
Because of BST properties:
- All values $< i$ (i.e. $[1 \\dots i-1]$) must go into the <strong>left subtree</strong>.
- All values $> i$ (i.e. $[i+1 \\dots n]$) must go into the <strong>right subtree</strong>.</p>
<p>Use divide and conquer: generate all possible left subtrees for $[start, i-1]$ and all possible right subtrees for $[i+1, end]$, then form Cartesian product combinations with root $i$.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>The total number of structurally unique BSTs is the $n$-th Catalan number $C_n = \\frac{1}{n+1}\\binom{2n}{n}$. Memoizing intervals <code>(start, end)</code> prevents re-generating identical subtrees.</p>

<div class="insight">💡 <strong>Key insight:</strong> <code>generate(start, end)</code>: for root $i \\in [start, end]$, Cartesian product of <code>left_trees</code> and <code>right_trees</code> attached to <code>TreeNode(i)</code>.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def generateTrees(n: int) -> list[TreeNode]:
    if n == 0:
        return []
        
    memo = {}
    
    def build(start: int, end: int) -> list[TreeNode]:
        if start > end:
            return [None]
        if (start, end) in memo:
            return memo[(start, end)]
            
        all_trees = []
        for root_val in range(start, end + 1):
            left_trees = build(start, root_val - 1)
            right_trees = build(root_val + 1, end)
            
            for l in left_trees:
                for r in right_trees:
                    root = TreeNode(root_val, l, r)
                    all_trees.append(root)
                    
        memo[(start, end)] = all_trees
        return all_trees
        
    return build(1, n)
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(4^n / n^{3/2})$ — Governed by Catalan number generation.<br>
<strong>Space:</strong> $O(4^n / n^{3/2})$ — Space to store all unique tree structures.</p>
''',
96: '''<h2>🧭 How to think about it</h2>
<p>Given an integer <code>n</code>, return the number of structurally unique BST's (binary search trees) which has exactly <code>n</code> nodes of unique values from <code>1</code> to <code>n</code>.</p>

<p>Let $G(n)$ be the number of unique BSTs for sequence of length $n$.
For each root $i \\in [1, n]$, there are $i - 1$ nodes in the left subtree and $n - i$ nodes in the right subtree:
$$G(n) = \\sum_{i=1}^n G(i - 1) \\times G(n - i)$$
with base cases $G(0) = 1, G(1) = 1$. This is the mathematical recurrence for <strong>Catalan Numbers</strong>!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>1D DP tabulates $G(0) \\dots G(n)$ in $O(n^2)$ time. Alternatively, Catalan closed form $C_n = \\frac{1}{n+1}\\binom{2n}{n} = \\frac{(2n)!}{(n+1)!n!}$ computes in $O(n)$ time and $O(1)$ space.</p>

<div class="insight">💡 <strong>Key insight:</strong> Closed-form iterative Catalan computation: $C_{i} = C_{i-1} \\times \\frac{2(2i - 1)}{i + 1}$ computes the exact answer in $O(n)$ time!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def numTrees(n: int) -> int:
    """
    Computes nth Catalan number in O(n) time and O(1) space.
    """
    c = 1
    for i in range(1, n + 1):
        c = c * 2 * (2 * i - 1) // (i + 1)
    return c
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n)$ — Single linear mathematical iteration.<br>
<strong>Space:</strong> $O(1)$ — Single scalar accumulator.</p>
''',
241: '''<h2>🧭 How to think about it</h2>
<p>Given a string <code>expression</code> of numbers and operators, return all possible results from computing all the different possible ways to group numbers and operators (with parentheses).</p>

<p>This is divide and conquer / Catalan structure:
Every operator (<code>+</code>, <code>-</code>, <code>*</code>) splits the expression into a left subexpression and a right subexpression:
$$\\text{diffWaysToCompute}(\\text{left}) \\quad \\text{op} \\quad \\text{diffWaysToCompute}(\\text{right})$$
Evaluate Cartesian product of all results from left and right operands.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Memoizing on the string slice <code>memo[expression]</code> prevents re-evaluating identical subexpressions.</p>

<div class="insight">💡 <strong>Key insight:</strong> For each operator at index $i$: split into <code>expr[:i]</code> and <code>expr[i+1:]</code>, recurse with memoization, and combine pairwise results.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def diffWaysToCompute(expression: str) -> list[int]:
    memo = {}
    
    def dfs(expr: str) -> list[int]:
        if expr in memo:
            return memo[expr]
            
        res = []
        for i, ch in enumerate(expr):
            if ch in '+-*':
                left_results = dfs(expr[:i])
                right_results = dfs(expr[i + 1:])
                
                for l in left_results:
                    for r in right_results:
                        if ch == '+':
                            res.append(l + r)
                        elif ch == '-':
                            res.append(l - r)
                        elif ch == '*':
                            res.append(l * r)
                            
        # Base case: pure number
        if not res:
            res.append(int(expr))
            
        memo[expr] = res
        return res
        
    return dfs(expression)
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(4^n / \\sqrt{n})$ — Bound by Catalan number of parenthesizations.<br>
<strong>Space:</strong> $O(4^n / \\sqrt{n})$ — Memoization dictionary storing all subexpression evaluation lists.</p>
''',
312: '''<h2>🧭 How to think about it</h2>
<p>You are given <code>n</code> balloons, indexed from <code>0</code> to <code>n - 1</code>. Each balloon is painted with a number on it represented by an array <code>nums</code>. You are asked to burst all the balloons. If you burst balloon <code>i</code> you will get <code>nums[i - 1] * nums[i] * nums[i + 1]</code> coins. Return the maximum coins you can collect.</p>

<p>Pad boundaries with virtual balloons: <code>nums = [1] + nums + [1]</code>.
If you think about which balloon to burst <em>first</em>, the left and right subproblems become coupled and dependent because bursting a balloon changes the neighbors for subsequent pops!</p>

<p><strong>The Reverse Trick:</strong> Think about which balloon is burst <strong>LAST</strong> in the interval $(left, right)$!
If balloon $k$ ($left < k < right$) is the last balloon burst in interval $(left, right)$, then balloons $left$ and $right$ are guaranteed to still be present right next to $k$:
$$dp[l][r] = \\max_{l < k < r} (dp[l][k] + dp[k][r] + nums[l] \\times nums[k] \\times nums[r])$$
Now the two subproblems $(l, k)$ and $(k, r)$ are completely independent!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Thinking forward creates intractable dependencies. Thinking backwards (last balloon to pop) yields clean <strong>Interval DP</strong> with states $O(n^2)$ and transition $O(n)$, running in $O(n^3)$ time.</p>

<div class="insight">💡 <strong>Key insight:</strong> Reverse your thinking: choose the <strong>last</strong> balloon $k$ to burst in $(l, r)$. Coins gained $= nums[l] \\times nums[k] \\times nums[r] + dp[l][k] + dp[k][r]$.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def maxCoins(nums: list[int]) -> int:
    padded = [1] + nums + [1]
    n = len(padded)
    dp = [[0] * n for _ in range(n)]
    
    # length of interval from 2 (no balloons inside) to n - 1
    for length in range(2, n):
        for left in range(0, n - length):
            right = left + length
            for k in range(left + 1, right):
                coins = padded[left] * padded[k] * padded[right] + dp[left][k] + dp[k][right]
                if coins > dp[left][right]:
                    dp[left][right] = coins
                    
    return dp[0][n - 1]
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n^3)$ — Lengths $2 \\dots n$, left bounds $O(n)$, split points $k \\in (l, r)$.<br>
<strong>Space:</strong> $O(n^2)$ — 2D table for interval $(left, right)$.</p>
''',
546: '''<h2>🧭 How to think about it</h2>
<p>You are given several boxes with different colors represented by positive integers <code>boxes</code>. You may experience several rounds to remove boxes until there is no box left. Each time you can choose some continuous boxes with the same color (i.e. length <code>k >= 1</code>), remove them and get <code>k * k</code> points. Return the maximum points you can get.</p>

<p>This is one of the most famous 3D Interval DP problems in competitive programming!
A standard 2D interval $dp[l][r]$ is insufficient because boxes to the left of $l$ with the same color as $boxes[l]$ can be accumulated and merged together after clearing intermediate boxes!</p>

<p><strong>3D State Formulation:</strong>
Let $dp[l][r][k]$ be the maximum score for subarray $boxes[l \\dots r]$ given that there are already $k$ boxes adjacent to $boxes[l]$ on the left with the same color $boxes[l]$!
1. <strong>Option 1:</strong> Remove $boxes[l]$ together with the $k$ accumulated identical boxes:
   $$\\text{gain} = (k + 1)^2 + dp[l + 1][r][0]$$
2. <strong>Option 2:</strong> Keep $boxes[l]$ and the $k$ boxes, find another box $m \\in [l+1, r]$ where $boxes[m] == boxes[l]$, clear the intermediate segment $boxes[l+1 \\dots m-1]$, and merge:
   $$\\text{gain} = dp[l + 1][m - 1][0] + dp[m][r][k + 1]$$</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Brute force search is factorial. 3D memoization bounds distinct subproblems to $O(n^4)$ states and transitions, executing smoothly within typical constraints ($n \\le 100$).</p>

<div class="insight">💡 <strong>Key insight:</strong> State includes $k$: <code>dfs(l, r, k)</code> = max score on <code>boxes[l..r]</code> with $k$ matching boxes attached to <code>boxes[l]</code> from the left.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">from functools import lru_cache

def removeBoxes(boxes: list[int]) -> int:
    @lru_cache(maxsize=None)
    def dfs(l: int, r: int, k: int) -> int:
        if l > r:
            return 0
            
        # Optimization: group consecutive matching boxes at the start
        while l + 1 <= r and boxes[l] == boxes[l + 1]:
            l += 1
            k += 1
            
        # Option 1: burst boxes[l] and the k accumulated identical boxes
        res = (k + 1) * (k + 1) + dfs(l + 1, r, 0)
        
        # Option 2: find another matching box m in (l+1..r)
        for m in range(l + 1, r + 1):
            if boxes[m] == boxes[l]:
                res = max(res, dfs(l + 1, m - 1, 0) + dfs(m, r, k + 1))
                
        return res
        
    return dfs(0, len(boxes) - 1, 0)
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n^4)$ — $n^3$ states, each taking $O(n)$ transition scan.<br>
<strong>Space:</strong> $O(n^3)$ — 3D memoization cache.</p>
''',

5: '''<h2>🧭 How to think about it</h2>
<p>Given a string <code>s</code>, return the longest palindromic substring in <code>s</code>.</p>

<p>Every palindrome mirrors around its center. A string of length $n$ has exactly $2n - 1$ potential centers:
1. $n$ odd-length centers: centered at character $s[i]$ ($i \\in [0, n-1]$).
2. $n - 1$ even-length centers: centered between $s[i]$ and $s[i+1]$ ($i \\in [0, n-2]$).</p>
<p>Expanding outward from each center until characters mismatch finds the longest palindrome in $O(n^2)$ time with $O(1)$ space. For $O(n)$ linear time, Manacher's Algorithm mirrors palindromic lengths using previously computed boundaries.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Testing all $O(n^2)$ substrings for palindromicity takes $O(n^3)$ time. Expand-around-center reduces time to $O(n^2)$ and space to $O(1)$ without allocating any DP table!</p>

<div class="insight">💡 <strong>Key insight:</strong> Expand outward from $2n-1$ centers. For center $(l, r)$, decrement $l$ and increment $r$ while $s[l] == s[r]$. Track the maximum $(r - l - 1)$ interval.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def longestPalindrome(s: str) -> str:
    if not s or len(s) == 1:
        return s
        
    start, max_len = 0, 1
    
    def expand(l: int, r: int):
        nonlocal start, max_len
        while l >= 0 and r < len(s) and s[l] == s[r]:
            curr_len = r - l + 1
            if curr_len > max_len:
                max_len = curr_len
                start = l
            l -= 1
            r += 1
            
    for i in range(len(s)):
        expand(i, i)       # Odd length palindrome
        expand(i, i + 1)   # Even length palindrome
        
    return s[start : start + max_len]
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n^2)$ — $2n - 1$ centers, expanding at most $n$ times.<br>
<strong>Space:</strong> $O(1)$ — Constant scalar variables (pointers).</p>
''',
647: '''<h2>🧭 How to think about it</h2>
<p>Given a string <code>s</code>, return the number of palindromic substrings in it.</p>

<p>A substring is a palindrome if it reads the same forward and backward. Like <strong>LC 5</strong>, every palindromic substring must have a center.
Expanding around each of the $2n - 1$ centers, every successful match $s[l] == s[r]$ contributes exactly <strong>one</strong> valid palindrome!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Brute force generation of all substrings takes $O(n^3)$. Expand-around-center checks all centers in $O(n^2)$ time and $O(1)$ auxiliary space.</p>

<div class="insight">💡 <strong>Key insight:</strong> As you expand from center $(l, r)$, increment <code>count += 1</code> on every matching step <code>s[l] == s[r]</code>.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def countSubstrings(s: str) -> int:
    n = len(s)
    total = 0
    
    def count_palindromes(l: int, r: int) -> int:
        c = 0
        while l >= 0 and r < n and s[l] == s[r]:
            c += 1
            l -= 1
            r += 1
        return c
        
    for i in range(n):
        total += count_palindromes(i, i)     # Odd centers
        total += count_palindromes(i, i + 1) # Even centers
        
    return total
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n^2)$ — Each expansion runs at most $O(n)$.<br>
<strong>Space:</strong> $O(1)$ — Only count accumulators.</p>
''',
132: '''<h2>🧭 How to think about it</h2>
<p>Given a string <code>s</code>, partition <code>s</code> such that every substring of the partition is a palindrome. Return the minimum cuts needed for a palindrome partitioning of <code>s</code>.</p>

<p>Let $cuts[i]$ be the minimum cuts needed for prefix $s[0 \\dots i]$.
To find $cuts[i]$, consider all possible palindromic suffixes $s[j \\dots i]$ ($0 \\le j \\le i$):
- If $s[0 \\dots i]$ is already a palindrome ($j = 0$), then $cuts[i] = 0$.
- If $s[j \\dots i]$ is a palindrome for $j > 0$, then $cuts[i] = \\min(cuts[i], \\; cuts[j - 1] + 1)$.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Precomputing or simultaneously updating palindrome intervals with expand-around-center optimizes the solution to $O(n^2)$ time and $O(n)$ space.</p>

<div class="insight">💡 <strong>Key insight:</strong> Maintain <code>cuts[i] = i</code> (worst case: cut every char). While expanding palindrome $(l, r)$, transition <code>cuts[r] = min(cuts[r], (cuts[l - 1] + 1) if l > 0 else 0)</code>.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def minCut(s: str) -> int:
    n = len(s)
    cuts = list(range(n)) # cuts[i] initialized to i (max possible cuts)
    
    for mid in range(n):
        # Odd-length palindromes centered at mid
        l, r = mid, mid
        while l >= 0 and r < n and s[l] == s[r]:
            new_cut = 0 if l == 0 else cuts[l - 1] + 1
            cuts[r] = min(cuts[r], new_cut)
            l -= 1
            r += 1
            
        # Even-length palindromes centered between mid and mid + 1
        l, r = mid, mid + 1
        while l >= 0 and r < n and s[l] == s[r]:
            new_cut = 0 if l == 0 else cuts[l - 1] + 1
            cuts[r] = min(cuts[r], new_cut)
            l -= 1
            r += 1
            
    return cuts[-1]
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n^2)$ — Each character center expanded in $O(n)$ time.<br>
<strong>Space:</strong> $O(n)$ — 1D cuts array of length $n$.</p>
''',
1312: '''<h2>🧭 How to think about it</h2>
<p>Given a string <code>s</code>. In one step you can insert any character at any position of the string. Return the minimum number of steps to make <code>s</code> a palindrome.</p>

<p>Any character that is already part of the <strong>Longest Palindromic Subsequence (LPS)</strong> does NOT need to be paired by insertion—it is already mirrored!
Every character outside the LPS requires exactly one matching insertion on the opposite side.
$$\\text{Min Insertions} = \\text{len}(s) - \\text{LPS}(s)$$
Recall: $\\text{LPS}(s) = \\text{LCS}(s, \\text{reverse}(s))$!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>This problem reduces directly to finding the Longest Palindromic Subsequence (LC 516) or LCS with the reversed string in $O(n^2)$ time and $O(n)$ space.</p>

<div class="insight">💡 <strong>Key insight:</strong> Min Insertions $= n - \\text{LPS}(s)$. Compute LPS bottom-up on intervals $[l, r]$ or via LCS with reversed string.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def minInsertions(s: str) -> int:
    n = len(s)
    dp = [0] * n
    
    # Bottom-up interval DP for Longest Palindromic Subsequence
    for l in range(n - 1, -1, -1):
        prev_diag = 0
        dp[l] = 1 # Single character is palindrome of length 1
        for r in range(l + 1, n):
            temp = dp[r]
            if s[l] == s[r]:
                dp[r] = prev_diag + 2
            else:
                dp[r] = max(dp[r], dp[r - 1])
            prev_diag = temp
            
    lps = dp[n - 1]
    return n - lps
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n^2)$ — Nested interval loops.<br>
<strong>Space:</strong> $O(n)$ — 1D rolling array for LPS.</p>
''',
354: '''<h2>🧭 How to think about it</h2>
<p>You are given a 2D array of integers <code>envelopes</code> where <code>envelopes[i] = [w_i, h_i]</code> represents the width and the height of an envelope. One envelope can fit into another if and only if both the width and height of one envelope are strictly greater than the other envelope. Return the maximum number of envelopes you can Russian doll (put inside one another).</p>

<p>This is a 2D variation of <strong>Longest Increasing Subsequence (LIS)</strong>.
If we sort envelopes by width ascending, we reduce one dimension!
<strong>The Clever Sorting Trick:</strong>
- Sort width <strong>ascending</strong>: <code>w1 < w2</code> ensures width is non-decreasing.
- If widths are equal, sort height <strong>descending</strong>: <code>h1 > h2</code>!</p>
<p>Why descending on height for identical widths? Because an envelope cannot contain another envelope of the <em>same</em> width! By sorting height descending, when we run standard 1D LIS on heights, we can never pick two envelopes with the same width!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Standard $O(n^2)$ LIS DP gets TLE ($n = 10^5$). With the sorting trick, binary search LIS (Patience Sorting / <code>bisect_left</code>) solves it in $O(n \\log n)$ time!</p>

<div class="insight">💡 <strong>Key insight:</strong> Sort by <code>(width, -height)</code>, then extract heights and run $O(n \\log n)$ Patience Sorting LIS with binary search.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">import bisect

def maxEnvelopes(envelopes: list[list[int]]) -> int:
    # Sort width ascending, height descending
    envelopes.sort(key=lambda x: (x[0], -x[1]))
    
    # Run O(n log n) LIS on heights
    tails = []
    for _, h in envelopes:
        idx = bisect.bisect_left(tails, h)
        if idx == len(tails):
            tails.append(h)
        else:
            tails[idx] = h
            
    return len(tails)
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n \\log n)$ — Sorting takes $O(n \\log n)$ and binary search LIS takes $O(n \\log n)$.<br>
<strong>Space:</strong> $O(n)$ — <code>tails</code> array storing active increasing subsequence tails.</p>
''',
673: '''<h2>🧭 How to think about it</h2>
<p>Given an integer array <code>nums</code>, return the number of longest increasing subsequences.</p>

<p>We maintain two arrays:
- $length[i]$: the length of the longest increasing subsequence ending at index $i$.
- $count[i]$: the number of longest increasing subsequences of length $length[i]$ ending at index $i$.</p>

<p>For each pair $j < i$ with $nums[j] < nums[i]$:
1. If $length[j] + 1 > length[i]$: we found a strictly longer LIS! Set $length[i] = length[j] + 1$ and reset $count[i] = count[j]$.
2. If $length[j] + 1 == length[i]$: we found another way to achieve this maximum length! Add $count[i] += count[j]$.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>$O(n^2)$ DP tracks both length and counts simultaneously. At the end, find global max length $M = \\max(length)$ and sum all $count[i]$ where $length[i] == M$.</p>

<div class="insight">💡 <strong>Key insight:</strong> Two DP arrays: <code>length[i]</code> and <code>count[i]</code>. When <code>length[j] + 1 == length[i]</code>, accumulate <code>count[i] += count[j]</code>.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def findNumberOfLIS(nums: list[int]) -> int:
    if not nums:
        return 0
    n = len(nums)
    length = [1] * n
    count = [1] * n
    
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                if length[j] + 1 > length[i]:
                    length[i] = length[j] + 1
                    count[i] = count[j]
                elif length[j] + 1 == length[i]:
                    count[i] += count[j]
                    
    max_len = max(length)
    return sum(c for l, c in zip(length, count) if l == max_len)
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n^2)$ — Nested loops over all pairs $(j, i)$.<br>
<strong>Space:</strong> $O(n)$ — Two linear arrays <code>length</code> and <code>count</code>.</p>
''',
1027: '''<h2>🧭 How to think about it</h2>
<p>Given an array <code>nums</code> of integers, return the length of the longest arithmetic subsequence in <code>nums</code>. A subsequence is arithmetic if $nums[i_{k+1}] - nums[i_k]$ is constant for all $k$.</p>

<p>An arithmetic sequence is determined by its common difference $d = nums[i] - nums[j]$.
Let $dp[i][d]$ be the length of the arithmetic subsequence ending at index $i$ with difference $d$.
For each $j < i$:
$$d = nums[i] - nums[j]$$
$$dp[i][d] = dp[j].get(d, 1) + 1$$
Global answer is $\\max_{i, d} dp[i][d]$.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Using a list of hash maps $dp[i]$ where each map keys differences to subsequence lengths runs in $O(n^2)$ time and $O(n^2)$ space.</p>

<div class="insight">💡 <strong>Key insight:</strong> Maintain <code>dp[i][diff]</code> as the length of arithmetic subsequence ending at <code>i</code> with common difference <code>diff</code>. Transition: <code>dp[i][diff] = dp[j].get(diff, 1) + 1</code>.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def longestArithSeqLength(nums: list[int]) -> int:
    n = len(nums)
    dp = [{} for _ in range(n)]
    max_len = 2
    
    for i in range(n):
        for j in range(i):
            diff = nums[i] - nums[j]
            prev_len = dp[j].get(diff, 1)
            curr_len = prev_len + 1
            dp[i][diff] = curr_len
            if curr_len > max_len:
                max_len = curr_len
                
    return max_len
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n^2)$ — Double nested iteration over all index pairs $(j, i)$.<br>
<strong>Space:</strong> $O(n^2)$ — Dictionary states across $n$ indices.</p>
''',
1187: '''<h2>🧭 How to think about it</h2>
<p>Given two integer arrays <code>arr1</code> and <code>arr2</code>, return the minimum number of operations needed to make <code>arr1</code> strictly increasing. In one operation, you can choose any index in <code>arr1</code> and replace the value with any element from <code>arr2</code>. If not possible, return -1.</p>

<p>Pre-sort and deduplicate <code>arr2</code> so we can use binary search (<code>bisect_right</code>) to find the smallest element strictly greater than a threshold.</p>
<p>Let $dp$ be a dictionary mapping the current valid ending value to the minimum replacements used so far.
For each element $x \\in arr1$:
1. <strong>Keep $x$ (no operation):</strong> if $x > prev$, we can transition to $x$ with $ops$ operations.
2. <strong>Replace $x$ with smallest valid element from $arr2$:</strong> find smallest $y \\in arr2$ with $y > prev$ using <code>bisect_right</code>. Transition to $y$ with $ops + 1$ operations.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>DP state compression keeping only the minimum operations for each reachable value bounds state space to $O(n \\times \\min(m, n))$, executing within milliseconds.</p>

<div class="insight">💡 <strong>Key insight:</strong> Maintain map <code>dp[last_value] = min_ops</code>. For each position, greedily try either keeping <code>arr1[i]</code> or replacing it with the smallest strictly larger element in <code>arr2</code> via binary search.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">import bisect

def makeArrayIncreasing(arr1: list[int], arr2: list[int]) -> int:
    arr2 = sorted(set(arr2))
    # dp maps: last_value_in_arr1 -> min_operations
    dp = {-1: 0}
    
    for x in arr1:
        new_dp = {}
        for prev_val, ops in dp.items():
            # Option 1: Keep x if strictly greater than prev_val
            if x > prev_val:
                if x not in new_dp or ops < new_dp[x]:
                    new_dp[x] = ops
                    
            # Option 2: Replace x with smallest element in arr2 > prev_val
            idx = bisect.bisect_right(arr2, prev_val)
            if idx < len(arr2):
                y = arr2[idx]
                if y not in new_dp or ops + 1 < new_dp[y]:
                    new_dp[y] = ops + 1
                    
        dp = new_dp
        if not dp:
            return -1
            
    return min(dp.values())
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n \\times \\min(n, m) \\log m)$ — At each index, binary search into sorted <code>arr2</code>.<br>
<strong>Space:</strong> $O(\\min(n, m))$ — State map holding active branch endpoints.</p>
''',
1671: '''<h2>🧭 How to think about it</h2>
<p>You may recall that an array <code>arr</code> is a mountain array if and only if:
- $\\text{len}(arr) \\ge 3$
- There exists some index $i$ ($0 < i < \\text{len}(arr) - 1$) such that $arr[0] < arr[1] < \\dots < arr[i]$ and $arr[i] > arr[i+1] > \\dots > arr[-1]$.</p>
<p>Given an integer array <code>nums</code>, return the minimum number of elements to remove to make <code>nums</code> a mountain array.</p>

<p>Minimizing removals is equivalent to <strong>maximizing the length of the mountain array</strong>!
For every valid peak index $i$:
$$\\text{Mountain Length} = LIS_{left}[i] + LIS_{right}[i] - 1$$
where:
- $LIS_{left}[i]$ is the Longest Increasing Subsequence in $nums[0 \\dots i]$ ending at $i$.
- $LIS_{right}[i]$ is the Longest Decreasing Subsequence starting at $i$ (i.e. LIS in reversed array ending at $i$).</p>
<p>A peak is valid only if $LIS_{left}[i] \\ge 2$ and $LIS_{right}[i] \\ge 2$ (must have at least one element strictly climbing up and one climbing down!).</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Compute $LIS_{left}$ and $LIS_{right}$ using $O(n \\log n)$ Patience Sorting. Maximize valid mountain length in $O(n \\log n)$ time total!</p>

<div class="insight">💡 <strong>Key insight:</strong> Compute forward LIS and backward LIS in $O(n \\log n)$. For every peak with $left \\ge 2$ and $right \\ge 2$, removals $= n - (left + right - 1)$.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">import bisect

def minimumMountainRemovals(nums: list[int]) -> int:
    n = len(nums)
    
    # 1. Forward LIS ending at i
    lis_left = [1] * n
    tails = []
    for i in range(n):
        idx = bisect.bisect_left(tails, nums[i])
        if idx == len(tails):
            tails.append(nums[i])
        else:
            tails[idx] = nums[i]
        lis_left[i] = idx + 1
        
    # 2. Backward LIS starting at i
    lis_right = [1] * n
    tails = []
    for i in range(n - 1, -1, -1):
        idx = bisect.bisect_left(tails, nums[i])
        if idx == len(tails):
            tails.append(nums[i])
        else:
            tails[idx] = nums[i]
        lis_right[i] = idx + 1
        
    # 3. Find max mountain length
    max_mountain = 0
    for i in range(1, n - 1):
        if lis_left[i] >= 2 and lis_right[i] >= 2:
            max_mountain = max(max_mountain, lis_left[i] + lis_right[i] - 1)
            
    return n - max_mountain
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n \\log n)$ — Two binary search LIS passes.<br>
<strong>Space:</strong> $O(n)$ — Arrays storing <code>lis_left</code> and <code>lis_right</code>.</p>
''',
2407: '''<h2>🧭 How to think about it</h2>
<p>You are given an integer array <code>nums</code> and an integer <code>k</code>. Find the longest subsequence of <code>nums</code> that meets the following requirements:
1. The subsequence is strictly increasing.
2. The difference between adjacent elements in the subsequence is at most <code>k</code> (i.e. $nums[i+1] - nums[i] \\le k$).</p>

<p>For each number $x \\in nums$, we can extend any previous subsequence ending at value $v \\in [\\max(1, x - k), x - 1]$.
$$dp[x] = 1 + \\max_{v \\in [\\max(1, x - k), x - 1]} dp[v]$$
This requires a dynamic point-update and range-maximum query over the value domain $[1, \\max(nums)]$!
A <strong>Segment Tree</strong> or <strong>Fenwick Tree</strong> over the value range executes both query and update in $O(\\log M)$ time!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Checking all previous values takes $O(n \\times k)$ or $O(n^2)$. Using a Segment Tree on value range $M = \\max(nums)$ solves it in $O(n \\log M)$ time!</p>

<div class="insight">💡 <strong>Key insight:</strong> Segment tree over value domain $[1, M]$: query range $\\max$ on $[\\max(1, x-k), x-1]$, add 1, and update point $x$ with new max length.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">class SegmentTree:
    def __init__(self, size):
        self.n = size
        self.tree = [0] * (4 * size)
        
    def query(self, node, start, end, l, r):
        if r < start or end < l:
            return 0
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        p1 = self.query(2 * node, start, mid, l, r)
        p2 = self.query(2 * node + 1, mid + 1, end, l, r)
        return max(p1, p2)
        
    def update(self, node, start, end, idx, val):
        if start == end:
            self.tree[node] = max(self.tree[node], val)
            return
        mid = (start + end) // 2
        if idx <= mid:
            self.update(2 * node, start, mid, idx, val)
        else:
            self.update(2 * node + 1, mid + 1, end, idx, val)
        self.tree[node] = max(self.tree[2 * node], self.tree[2 * node + 1])

def lengthOfLIS(nums: list[int], k: int) -> int:
    max_val = max(nums)
    st = SegmentTree(max_val)
    
    for x in nums:
        left_bound = max(1, x - k)
        right_bound = x - 1
        best_prev = 0
        if left_bound <= right_bound:
            best_prev = st.query(1, 1, max_val, left_bound, right_bound)
        st.update(1, 1, max_val, x, best_prev + 1)
        
    return st.tree[1]
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n \\log M)$ where $M = \\max(nums)$. $n$ range queries and point updates.<br>
<strong>Space:</strong> $O(M)$ — Segment tree nodes for value domain.</p>
''',
}