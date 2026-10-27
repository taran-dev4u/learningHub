# -*- coding: utf-8 -*-
"""
Deep tutorials for Pattern 11: Backtracking Patterns.
Masterclass 12-step structured explanations with ASCII dry runs and complexity analyses.
"""

DEEP = {
# ============================================================ LC 78: Subsets
78: '''<h2>🧭 How to think about it</h2>
<p>Given an integer array <code>nums</code> of unique elements, return all possible subsets (the power set). The solution set must not contain duplicate subsets and can be returned in any order.</p>

<p>For an array of length <code>n</code>, every element has exactly two choices: either <strong>include</strong> it in the current subset, or <strong>exclude</strong> it. The total number of subsets is mathematically <code>2^n</code>. A state-space tree where nodes represent candidate subsets is traversed using <strong>Backtracking</strong>.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Since the output itself requires <code>O(N &times; 2^N)</code> time to write <code>2^N</code> subsets of average length <code>N/2</code>, any optimal algorithm must operate in <code>O(N &times; 2^N)</code> time.</p>

<div class="insight">💡 <strong>Key insight:</strong> At each level of the recursion tree, the current <code>path</code> is a valid subset! Add a copy of <code>path</code> to <code>result</code> immediately. Then iterate index <code>i</code> from <code>start</code> to <code>n - 1</code>:
<ol>
  <li><strong>Choose:</strong> <code>path.append(nums[i])</code></li>
  <li><strong>Explore:</strong> <code>backtrack(i + 1, path)</code></li>
  <li><strong>Un-choose:</strong> <code>path.pop()</code></li>
</ol></div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Initialize <code>result = []</code>.</li>
<li>Define <code>backtrack(start, path)</code>:
  <ul>
    <li>Append <code>list(path)</code> to <code>result</code>.</li>
    <li>For <code>i</code> from <code>start</code> to <code>len(nums) - 1</code>:
      <ul>
        <li><code>path.append(nums[i])</code></li>
        <li><code>backtrack(i + 1, path)</code></li>
        <li><code>path.pop()</code></li>
      </ul>
    </li>
  </ul>
</li>
<li>Call <code>backtrack(0, [])</code>. Return <code>result</code>.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [1, 2, 3]:</h2>
<pre class="viz">backtrack(0, []) -> record []
  i=0: path=[1] -> record [1]
    i=1: path=[1,2] -> record [1,2]
      i=2: path=[1,2,3] -> record [1,2,3]
    i=2: path=[1,3] -> record [1,3]
  i=1: path=[2] -> record [2]
    i=2: path=[2,3] -> record [2,3]
  i=2: path=[3] -> record [3]

Result: [[], [1], [1,2], [1,2,3], [1,3], [2], [2,3], [3]] (8 subsets) ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def subsets(nums: list[int]) -> list[list[int]]:
    """
    Generates all subsets (power set) of distinct integers via backtracking.
    """
    res = []
    path = []
    n = len(nums)
    
    def backtrack(start):
        # Every node in the recursion tree represents a valid subset
        res.append(list(path))
        
        for i in range(start, n):
            path.append(nums[i])      # Choose
            backtrack(i + 1)          # Explore
            path.pop()                # Un-choose (Backtrack)
            
    backtrack(0)
    return res
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(N &times; 2^N)</code>. There are <code>2^N</code> subsets, and copying each subset takes on average <code>O(N)</code> time.</li>
<li><strong>Space Complexity:</strong> <code>O(N)</code> recursion stack depth and path storage (excluding output array).</li>
</ul>''',

# ============================================================ LC 90: Subsets II
90: '''<h2>🧭 How to think about it</h2>
<p>Given an integer array <code>nums</code> that may contain <strong>duplicates</strong>, return all possible subsets (the power set). The solution set must not contain duplicate subsets.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Generating all subsets and converting to a <code>set(tuple(x))</code> wastes computation on duplicate branches. By <strong>sorting</strong> the input and pruning identical sibling choices at the same recursion depth, we generate only unique subsets in <code>O(N &times; 2^N)</code> time.</p>

<div class="insight">💡 <strong>Key insight:</strong> Sort <code>nums</code>. In the loop <code>for i in range(start, n)</code>:
If <code>i > start and nums[i] == nums[i - 1]</code>: <strong>continue</strong>!
<br><br>
Why <code>i > start</code>? Because if <code>i == start</code>, this is the first time we are picking this duplicate element for the current position (e.g. picking the second <code>'2'</code> to make <code>[2, 2]</code>). But if <code>i > start</code>, we have already explored all subsets starting with an identical element at this level—picking it again would generate a duplicate branch!</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Sort <code>nums.sort()</code>.</li>
<li>Initialize <code>res = []</code>, <code>path = []</code>.</li>
<li>In <code>backtrack(start)</code>:
  <ul>
    <li>Append <code>list(path)</code> to <code>res</code>.</li>
    <li>For <code>i</code> from <code>start</code> to <code>len(nums) - 1</code>:
      <ul>
        <li>If <code>i > start and nums[i] == nums[i - 1]</code>: continue (prune duplicate sibling!).</li>
        <li><code>path.append(nums[i])</code></li>
        <li><code>backtrack(i + 1)</code></li>
        <li><code>path.pop()</code></li>
      </ul>
    </li>
  </ul>
</li>
</ol>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def subsetsWithDup(nums: list[int]) -> list[list[int]]:
    """
    Generates all unique subsets from array with duplicates using sorting and sibling pruning.
    """
    nums.sort()
    res = []
    path = []
    n = len(nums)
    
    def backtrack(start):
        res.append(list(path))
        
        for i in range(start, n):
            # Prune duplicate choices at the same recursion depth
            if i > start and nums[i] == nums[i - 1]:
                continue
                
            path.append(nums[i])
            backtrack(i + 1)
            path.pop()
            
    backtrack(0)
    return res
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(N &times; 2^N)</code>. Sorting takes <code>O(N log N)</code>.</li>
<li><strong>Space Complexity:</strong> <code>O(N)</code> recursion stack.</li>
</ul>''',

# ============================================================ LC 77: Combinations
77: '''<h2>🧭 How to think about it</h2>
<p>Given two integers <code>n</code> and <code>k</code>, return all possible combinations of <code>k</code> numbers chosen from the range <code>[1, n]</code>.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>We can optimize the search by <strong>pruning</strong> the loop range: if the number of remaining elements in the range is strictly less than the number of elements we still need to complete <code>k</code>, stop looping!</p>

<div class="insight">💡 <strong>Key insight:</strong> Number of slots remaining = <code>k - len(path)</code>. If we pick number <code>i</code>, there are <code>n - i + 1</code> numbers available. Thus we only need to iterate <code>i</code> while <code>n - i + 1 >= k - len(path)</code> &rarr; <code>i <= n - (k - len(path)) + 1</code>! This avoids exploring dead-end branches.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def combine(n: int, k: int) -> list[list[int]]:
    """
    Generates all combinations of k numbers from 1 to n with loop boundary pruning.
    """
    res = []
    path = []
    
    def backtrack(start):
        if len(path) == k:
            res.append(list(path))
            return
            
        # Pruned upper bound: no need to search if remaining elements < needed
        needed = k - len(path)
        upper_bound = n - needed + 1
        
        for i in range(start, upper_bound + 1):
            path.append(i)
            backtrack(i + 1)
            path.pop()
            
    backtrack(1)
    return res
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(k &times; C(n, k))</code> where <code>C(n, k) = n! / (k!(n-k)!)</code>.</li>
<li><strong>Space Complexity:</strong> <code>O(k)</code> for the recursion stack.</li>
</ul>''',

# ============================================================ LC 17: Letter Combinations of a Phone Number
17: '''<h2>🧭 How to think about it</h2>
<p>Given a string containing digits from <code>2-9</code> inclusive, return all possible letter combinations that the number could represent according to telephone keypad mappings.</p>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Define mapping <code>PHONE = {'2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl', '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'}</code>.</li>
<li>If <code>not digits</code>, return <code>[]</code>.</li>
<li>Backtracking state <code>(index, path)</code>:
  <ul>
    <li>If <code>index == len(digits)</code>: append <code>"".join(path)</code> to <code>res</code>; return.</li>
    <li>For letter in <code>PHONE[digits[index]]</code>:
      <ul>
        <li><code>path.append(letter)</code>; <code>backtrack(index + 1)</code>; <code>path.pop()</code>.</li>
      </ul>
    </li>
  </ul>
</li>
</ol>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def letterCombinations(digits: str) -> list[str]:
    """
    Generates phone keypad letter combinations in O(4^N * N) time.
    """
    if not digits:
        return []
        
    phone = {
        '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
        '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
    }
    
    res = []
    path = []
    
    def backtrack(idx):
        if idx == len(digits):
            res.append("".join(path))
            return
            
        for char in phone[digits[idx]]:
            path.append(char)
            backtrack(idx + 1)
            path.pop()
            
    backtrack(0)
    return res
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(4^N &times; N)</code> where <code>N = len(digits)</code>. In the worst case (digits 7 and 9), each digit maps to 4 letters.</li>
<li><strong>Space Complexity:</strong> <code>O(N)</code> recursion stack.</li>
</ul>''',

# ============================================================ LC 46: Permutations
46: '''<h2>🧭 How to think about it</h2>
<p>Given an array <code>nums</code> of distinct integers, return all the possible <strong>permutations</strong> in any order.</p>

<p>For an array of length <code>n</code>, there are exactly <code>n!</code> permutations. At each step of the recursion tree, any element not yet used in the current prefix can be placed next.</p>

<div class="insight">💡 <strong>Key insight:</strong> Two standard approaches:
<ol>
  <li><strong>Visited Boolean Array:</strong> Maintain <code>visited = [False] * n</code>. Loop <code>i</code> from <code>0</code> to <code>n - 1</code>: if not visited, mark visited, push to path, recurse, pop and unmark.</li>
  <li><strong>In-place Swapping:</strong> In <code>backtrack(first)</code>, swap <code>nums[first]</code> with <code>nums[i]</code> for <code>i &isin; [first, n-1]</code>. Requires zero auxiliary visited set!</li>
</ol></div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def permute(nums: list[int]) -> list[list[int]]:
    """
    Generates all permutations using backtracking with a visited tracking array.
    """
    n = len(nums)
    res = []
    path = []
    used = [False] * n
    
    def backtrack():
        if len(path) == n:
            res.append(list(path))
            return
            
        for i in range(n):
            if not used[i]:
                used[i] = True
                path.append(nums[i])
                backtrack()
                path.pop()
                used[i] = False
                
    backtrack()
    return res
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(N &times; N!)</code>. There are <code>N!</code> permutations, and each takes <code>O(N)</code> to copy into the result.</li>
<li><strong>Space Complexity:</strong> <code>O(N)</code> for the recursion stack and <code>used</code> array.</li>
</ul>''',

# ============================================================ LC 47: Permutations II
47: '''<h2>🧭 How to think about it</h2>
<p>Given a collection of numbers, <code>nums</code>, that might contain <strong>duplicates</strong>, return all possible unique permutations in any order.</p>

<div class="insight">💡 <strong>Key insight:</strong> Sort <code>nums</code>. When iterating through candidate elements at index <code>i</code>:
If <code>used[i]</code> is True: continue.
If <code>i > 0 and nums[i] == nums[i - 1] and not used[i - 1]</code>: <strong>continue</strong>!
<br><br>
Why <code>not used[i - 1]</code>?
Because if <code>used[i - 1] == False</code>, it means <code>nums[i - 1]</code> was just un-chosen during backtracking at the exact same depth! Picking the identical duplicate <code>nums[i]</code> now would generate a duplicate permutation subtree!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def permuteUnique(nums: list[int]) -> list[list[int]]:
    """
    Generates unique permutations of array with duplicates via sorting and used-flag pruning.
    """
    nums.sort()
    n = len(nums)
    res = []
    path = []
    used = [False] * n
    
    def backtrack():
        if len(path) == n:
            res.append(list(path))
            return
            
        for i in range(n):
            if used[i]:
                continue
            # Prune duplicate siblings at the same recursion depth
            if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                continue
                
            used[i] = True
            path.append(nums[i])
            backtrack()
            path.pop()
            used[i] = False
            
    backtrack()
    return res
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(N &times; N!)</code>.</li>
<li><strong>Space Complexity:</strong> <code>O(N)</code>.</li>
</ul>''',

# ============================================================ LC 31: Next Permutation
31: '''<h2>🧭 How to think about it</h2>
<p>A permutation of an array of integers is an arrangement of its members into a sequence or linear order. The <strong>next permutation</strong> is the next lexicographically greater permutation. Rearrange <code>nums</code> into the lexicographically next greater permutation of numbers in-place with <code>O(1)</code> extra memory. If no greater permutation is possible, rearrange it to the lowest possible order (sorted ascending).</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Generating all permutations takes <code>O(N!)</code>. The single-pass greedy scan operates in <code>O(N)</code> time and <code>O(1)</code> space!</p>

<div class="insight">💡 <strong>Key insight:</strong> 4-step algorithm:
<ol>
  <li><strong>Find Pivot:</strong> Scan from right to left to find the first decreasing element: <code>nums[i] < nums[i + 1]</code>. The suffix <code>nums[i + 1:]</code> is descending.</li>
  <li><strong>Find Successor:</strong> If such index <code>i</code> exists, scan from right to left to find the smallest number greater than <code>nums[i]</code>: <code>nums[j] > nums[i]</code>.</li>
  <li><strong>Swap:</strong> Swap <code>nums[i]</code> and <code>nums[j]</code>.</li>
  <li><strong>Reverse Suffix:</strong> Reverse the suffix <code>nums[i + 1:]</code> to turn it into ascending order (smallest possible value).</li>
</ol></div>

<h2>🎞️ Visual dry run — nums = [1, 2, 7, 4, 3, 1]:</h2>
<pre class="viz">1. Suffix 7, 4, 3, 1 is descending. First decreasing element from right is 2 (index 1).
2. Smallest element in suffix larger than 2 is 3 (index 4).
3. Swap 2 and 3 -> [1, 3, 7, 4, 2, 1].
4. Reverse suffix [7, 4, 2, 1] -> [1, 2, 4, 7].
Result: [1, 3, 1, 2, 4, 7] ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def nextPermutation(nums: list[int]) -> None:
    """
    Rearranges numbers into lexicographically next greater permutation in-place.
    """
    n = len(nums)
    i = n - 2
    
    # 1. Find first index i from right where nums[i] < nums[i + 1]
    while i >= 0 and nums[i] >= nums[i + 1]:
        i -= 1
        
    if i >= 0:
        # 2. Find index j from right where nums[j] > nums[i]
        j = n - 1
        while nums[j] <= nums[i]:
            j -= 1
        # 3. Swap
        nums[i], nums[j] = nums[j], nums[i]
        
    # 4. Reverse suffix from i + 1 to end
    left, right = i + 1, n - 1
    while left < right:
        nums[left], nums[right] = nums[right], nums[left]
        left += 1
        right -= 1
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(N)</code>. Two linear scans from right and one reverse.</li>
<li><strong>Space Complexity:</strong> <code>O(1)</code> strictly in-place.</li>
</ul>''',

# ============================================================ LC 39: Combination Sum
39: '''<h2>🧭 How to think about it</h2>
<p>Given an array of distinct integers <code>candidates</code> and a <code>target</code> integer, return a list of all unique combinations of <code>candidates</code> where the chosen numbers sum to <code>target</code>. The same number may be chosen from <code>candidates</code> an <strong>unlimited number of times</strong>.</p>

<div class="insight">💡 <strong>Key insight:</strong> Sort <code>candidates</code>. At index <code>i</code>, if <code>candidates[i] > remaining_target</code>, break immediately (pruning!). When exploring, pass index <code>i</code> (NOT <code>i + 1</code>) to allow reusing the current candidate.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def combinationSum(candidates: list[int], target: int) -> list[list[int]]:
    """
    Finds combinations summing to target with unlimited element reuse.
    """
    candidates.sort()
    res = []
    path = []
    n = len(candidates)
    
    def backtrack(start, remain):
        if remain == 0:
            res.append(list(path))
            return
            
        for i in range(start, n):
            if candidates[i] > remain:
                break  # Pruning: all subsequent candidates are larger!
                
            path.append(candidates[i])
            backtrack(i, remain - candidates[i])  # Reuse candidate by passing i
            path.pop()
            
    backtrack(0, target)
    return res
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(N^(T/M))</code> where <code>T = target</code> and <code>M = min(candidates)</code>.</li>
<li><strong>Space Complexity:</strong> <code>O(T/M)</code> for maximum recursion tree depth.</li>
</ul>''',

# ============================================================ LC 40: Combination Sum II
40: '''<h2>🧭 How to think about it</h2>
<p>Given a collection of candidate numbers <code>candidates</code> (which may contain duplicates) and a <code>target</code>, find all unique combinations where candidate numbers sum to <code>target</code>. Each number in <code>candidates</code> may only be used <strong>once</strong> in the combination.</p>

<div class="insight">💡 <strong>Key insight:</strong> Sort <code>candidates</code>. Pass <code>i + 1</code> into recursive call (each number used once). Prune duplicate sibling branches: <code>if i > start and candidates[i] == candidates[i - 1]: continue</code>.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def combinationSum2(candidates: list[int], target: int) -> list[list[int]]:
    """
    Finds unique combinations summing to target with single-use candidates and duplicates.
    """
    candidates.sort()
    res = []
    path = []
    n = len(candidates)
    
    def backtrack(start, remain):
        if remain == 0:
            res.append(list(path))
            return
            
        for i in range(start, n):
            if candidates[i] > remain:
                break
            if i > start and candidates[i] == candidates[i - 1]:
                continue  # Skip duplicate elements at same depth
                
            path.append(candidates[i])
            backtrack(i + 1, remain - candidates[i])
            path.pop()
            
    backtrack(0, target)
    return res
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(2^N)</code> in worst case.</li>
<li><strong>Space Complexity:</strong> <code>O(N)</code>.</li>
</ul>''',

# ============================================================ LC 22: Generate Parentheses
22: '''<h2>🧭 How to think about it</h2>
<p>Given <code>n</code> pairs of parentheses, write a function to generate all combinations of well-formed parentheses.</p>

<div class="insight">💡 <strong>Key insight:</strong> Maintain <code>open_count</code> and <code>close_count</code>:
<ul>
  <li>Can add <code>'('</code> if <code>open_count < n</code>.</li>
  <li>Can add <code>')'</code> if <code>close_count < open_count</code>.</li>
</ul>
Base case: when <code>len(path) == 2 * n</code>, append <code>"".join(path)</code>!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def generateParenthesis(n: int) -> list[str]:
    """
    Generates well-formed parentheses strings via open/close bounded backtracking.
    """
    res = []
    path = []
    
    def backtrack(open_count, close_count):
        if len(path) == 2 * n:
            res.append("".join(path))
            return
            
        if open_count < n:
            path.append('(')
            backtrack(open_count + 1, close_count)
            path.pop()
            
        if close_count < open_count:
            path.append(')')
            backtrack(open_count, close_count + 1)
            path.pop()
            
    backtrack(0, 0)
    return res
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(4^N / sqrt(N))</code> governed by the n-th Catalan number $C_n = rac{1}{n+1}inom{2n}{n}$.</li>
<li><strong>Space Complexity:</strong> <code>O(N)</code> stack depth.</li>
</ul>''',

# ============================================================ LC 79: Word Search
79: '''<h2>🧭 How to think about it</h2>
<p>Given an <code>m x n</code> grid of characters <code>board</code> and a string <code>word</code>, return <code>true</code> if <code>word</code> exists in the grid. The word can be constructed from letters of sequentially adjacent cells (horizontally or vertically).</p>

<div class="insight">💡 <strong>Key insight:</strong>
1. <strong>In-Place Visited:</strong> Temporarily set <code>board[r][c] = '#'</code> to avoid an extra 2D visited array. Restore on backtrack: <code>board[r][c] = temp</code>.
2. <strong>Pruning Shortcut:</strong> If character count in <code>word</code> exceeds frequency in <code>board</code>, return <code>False</code> immediately. If <code>word[-1]</code> is rarer than <code>word[0]</code>, reverse <code>word</code> to search from the rarer end!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">from collections import Counter

def exist(board: list[list[str]], word: str) -> bool:
    """
    Finds word in grid via in-place cell masking DFS with frequency pruning.
    """
    m, n = len(board), len(board[0])
    if len(word) > m * n:
        return False
        
    # Frequency check optimization
    board_counts = Counter(c for row in board for c in row)
    word_counts = Counter(word)
    for c, count in word_counts.items():
        if board_counts[c] < count:
            return False
            
    # Reverse word if last letter is rarer than first letter
    if board_counts[word[0]] > board_counts[word[-1]]:
        word = word[::-1]
        
    def dfs(r, c, k):
        if k == len(word):
            return True
        if r < 0 or r >= m or c < 0 or c >= n or board[r][c] != word[k]:
            return False
            
        temp = board[r][c]
        board[r][c] = '#'  # Mark visited in-place
        
        found = (dfs(r + 1, c, k + 1) or
                 dfs(r - 1, c, k + 1) or
                 dfs(r, c + 1, k + 1) or
                 dfs(r, c - 1, k + 1))
                 
        board[r][c] = temp  # Backtrack
        return found
        
    for r in range(m):
        for c in range(n):
            if board[r][c] == word[0] and dfs(r, c, 0):
                return True
                
    return False
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(M &times; N &times; 3^L)</code> where <code>L = len(word)</code> (3 choices per step after the first).</li>
<li><strong>Space Complexity:</strong> <code>O(L)</code> recursion stack.</li>
</ul>''',

# ============================================================ LC 212: Word Search II
212: '''<h2>🧭 How to think about it</h2>
<p>Given an <code>m x n</code> <code>board</code> of characters and a list of strings <code>words</code>, return all words on the board.</p>

<div class="insight">💡 <strong>Key insight:</strong> Running Word Search I for each word independently takes <code>O(W &times; M &times; N &times; 3^L)</code>, which TLEs. Instead, insert all words into a <strong>Prefix Tree (Trie)</strong>. A single 2D DFS walks the grid while simultaneously walking down the Trie! When <code>node.word</code> is found, append it and set <code>node.word = None</code> (preventing duplicate results).</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">class TrieNode:
    def __init__(self):
        self.children = {}
        self.word = None

def findWords(board: list[list[str]], words: list[str]) -> list[str]:
    """
    Finds all dictionary words in grid simultaneously via Trie-guided 2D backtracking.
    """
    root = TrieNode()
    for w in words:
        curr = root
        for c in w:
            if c not in curr.children:
                curr.children[c] = TrieNode()
            curr = curr.children[c]
        curr.word = w
        
    m, n = len(board) , len(board[0])
    res = []
    
    def dfs(r, c, node):
        char = board[r][c]
        curr_node = node.children[char]
        
        if curr_node.word:
            res.append(curr_node.word)
            curr_node.word = None  # Prevent duplicate insertions
            
        board[r][c] = '#'  # Mark visited
        
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and board[nr][nc] in curr_node.children:
                dfs(nr, nc, curr_node)
                
        board[r][c] = char  # Backtrack
        
        # Optimization: prune leaf nodes to speed up subsequent searches
        if not curr_node.children:
            del node.children[char]
            
    for r in range(m):
        for c in range(n):
            if board[r][c] in root.children:
                dfs(r, c, root)
                
    return res
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(M &times; N &times; 4 &times; 3^(L-1))</code> where <code>L</code> is max word length.</li>
<li><strong>Space Complexity:</strong> <code>O(Total letters in words)</code> for the Trie.</li>
</ul>''',

# ============================================================ LC 51: N-Queens
51: '''<h2>🧭 How to think about it</h2>
<p>The n-queens puzzle is the problem of placing <code>n</code> queens on an <code>n x n</code> chessboard such that no two queens attack each other. Return all distinct solutions.</p>

<div class="insight">💡 <strong>Key insight:</strong> Place one queen per row! Queens attack if they share the same column <code>c</code>, same positive diagonal (where <code>r + c</code> is constant), or same negative diagonal (where <code>r - c</code> is constant). Maintain three hash sets: <code>cols</code>, <code>pos_diag</code>, <code>neg_diag</code> for <code>O(1)</code> safety checks.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def solveNQueens(n: int) -> list[list[str]]:
    """
    Solves N-Queens using row-by-row backtracking with O(1) diagonal attack sets.
    """
    cols = set()
    pos_diag = set()  # r + c
    neg_diag = set()  # r - c
    res = []
    board = [['.'] * n for _ in range(n)]
    
    def backtrack(r):
        if r == n:
            res.append(["".join(row) for row in board])
            return
            
        for c in range(n):
            if c in cols or (r + c) in pos_diag or (r - c) in neg_diag:
                continue
                
            cols.add(c)
            pos_diag.add(r + c)
            neg_diag.add(r - c)
            board[r][c] = 'Q'
            
            backtrack(r + 1)
            
            cols.remove(c)
            pos_diag.remove(r + c)
            neg_diag.remove(r - c)
            board[r][c] = '.'
            
    backtrack(0)
    return res
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(N!)</code>.</li>
<li><strong>Space Complexity:</strong> <code>O(N^2)</code> for board and sets.</li>
</ul>''',

# ============================================================ LC 37: Sudoku Solver
37: '''<h2>🧭 How to think about it</h2>
<p>Write a program to solve a Sudoku puzzle by filling the empty cells (represented by <code>'.'</code>). Each of the digits <code>1-9</code> must occur exactly once in each row, each column, and each of the nine <code>3x3</code> sub-boxes.</p>

<div class="insight">💡 <strong>Key insight:</strong> Iterate to find the next empty cell <code>(r, c)</code>. Try placing digits <code>'1'</code> through <code>'9'</code>. If placing digit <code>d</code> is valid (not in row <code>r</code>, not in col <code>c</code>, not in sub-box), set <code>board[r][c] = d</code> and recurse. If the recursive call returns <code>True</code>, return <code>True</code> immediately! If no digit works, reset <code>board[r][c] = '.'</code> and return <code>False</code>.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def solveSudoku(board: list[list[str]]) -> None:
    """
    Solves 9x9 Sudoku board in-place via backtracking.
    """
    def is_valid(r, c, ch):
        for i in range(9):
            if board[r][i] == ch:
                return False
            if board[i][c] == ch:
                return False
            # Check 3x3 sub-box
            br, bc = 3 * (r // 3) + i // 3, 3 * (c // 3) + i % 3
            if board[br][bc] == ch:
                return False
        return True
        
    def solve():
        for r in range(9):
            for c in range(9):
                if board[r][c] == '.':
                    for d in "123456789":
                        if is_valid(r, c, d):
                            board[r][c] = d
                            if solve():
                                return True
                            board[r][c] = '.'  # Backtrack
                    return False
        return True
        
    solve()
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(9^(empty_cells))</code> bounded by <code>O(9^81) = O(1)</code> for a fixed 9x9 board.</li>
<li><strong>Space Complexity:</strong> <code>O(81) = O(1)</code> recursion stack.</li>
</ul>''',

# ============================================================ LC 93: Restore IP Addresses
93: '''<h2>🧭 How to think about it</h2>
<p>Given a string <code>s</code> containing only digits, return all possible valid IPv4 addresses that can be formed by inserting dots into <code>s</code>.</p>

<div class="insight">💡 <strong>Key insight:</strong> Partition <code>s</code> into 4 parts. At each step, take 1 to 3 digits. Valid segment conditions:
1. Integer value &le; 255.
2. No leading zeros: <code>segment == "0" or not segment.startswith("0")</code>.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def restoreIpAddresses(s: str) -> list[str]:
    """
    Generates all valid IPv4 address strings via 4-segment backtracking.
    """
    if len(s) < 4 or len(s) > 12:
        return []
        
    res = []
    path = []
    
    def backtrack(start):
        if len(path) == 4:
            if start == len(s):
                res.append(".".join(path))
            return
            
        for length in range(1, 4):
            if start + length > len(s):
                break
                
            seg = s[start:start + length]
            # No leading zeros unless single digit 0
            if (len(seg) > 1 and seg[0] == '0') or int(seg) > 255:
                continue
                
            path.append(seg)
            backtrack(start + length)
            path.pop()
            
    backtrack(0)
    return res
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(3^4) = O(1)</code> constant time (at most 81 partitions).</li>
<li><strong>Space Complexity:</strong> <code>O(1)</code> space.</li>
</ul>''',

# ============================================================ LC 131: Palindrome Partitioning
131: '''<h2>🧭 How to think about it</h2>
<p>Given a string <code>s</code>, partition <code>s</code> such that every substring of the partition is a <strong>palindrome</strong>. Return all possible palindrome partitionings of <code>s</code>.</p>

<div class="insight">💡 <strong>Key insight:</strong> Backtracking explores split points. For <code>i</code> from <code>start</code> to <code>len(s) - 1</code>: check if prefix <code>s[start:i+1]</code> is a palindrome (<code>sub == sub[::-1]</code>). If it is, append to <code>path</code> and recurse on <code>i + 1</code>. When <code>start == len(s)</code>, append <code>list(path)</code>!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def partition(s: str) -> list[list[str]]:
    """
    Finds all palindrome partitions using backtracking with substring verification.
    """
    res = []
    path = []
    n = len(s)
    
    def is_palindrome(left, right):
        while left < right:
            if s[left] != s[right]:
                return False
            left += 1
            right -= 1
        return True
        
    def backtrack(start):
        if start == n:
            res.append(list(path))
            return
            
        for end in range(start, n):
            if is_palindrome(start, end):
                path.append(s[start:end + 1])
                backtrack(end + 1)
                path.pop()
                
    backtrack(0)
    return res
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(N &times; 2^N)</code>. There are <code>2^(N-1)</code> possible partitions, and verifying palindromes takes <code>O(N)</code>.</li>
<li><strong>Space Complexity:</strong> <code>O(N)</code> recursion stack.</li>
</ul>''',

}
