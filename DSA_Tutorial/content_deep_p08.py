# -*- coding: utf-8 -*-
"""
Deep tutorials for Pattern 8: Binary Search Patterns.
Masterclass 12-step structured explanations with ASCII dry runs and complexity analyses.
"""

DEEP = {
# ============================================================ LC 704
704: '''<h2>🧭 How to think about it</h2>
<p>Given an array of integers <code>nums</code> sorted in ascending order and a target value, find whether the target exists. If it exists, return its index; otherwise return <code>-1</code>. Because the array is sorted, comparing the middle element with the target immediately eliminates half the remaining search space.</p>

<h2>🐢 Brute force first</h2>
<p>Scan linearly from index <code>0</code> to <code>n-1</code> with a simple loop. Time: <strong>O(n)</strong>, Space: <strong>O(1)</strong>. Suboptimal because it ignores the sorted order property entirely.</p>

<div class="insight">💡 <strong>Key insight:</strong> Maintain a search window <code>[left, right]</code>. Compute mid <code>mid = left + (right - left) // 2</code>. If <code>nums[mid] == target</code>, we're done. If <code>nums[mid] < target</code>, target must lie in the right half, so <code>left = mid + 1</code>. If <code>nums[mid] > target</code>, target must lie in the left half, so <code>right = mid - 1</code>. Loop terminates when <code>left > right</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Initialize <code>left = 0</code> and <code>right = len(nums) - 1</code>.</li>
<li>While <code>left &lt;= right</code>:</li>
<li>Compute safe midpoint: <code>mid = left + (right - left) // 2</code> (avoids 32-bit integer overflow in languages like C++/Java).</li>
<li>If <code>nums[mid] == target</code>, return <code>mid</code>.</li>
<li>If <code>nums[mid] &lt; target</code>, eliminate left half: <code>left = mid + 1</code>.</li>
<li>Else, eliminate right half: <code>right = mid - 1</code>.</li>
<li>If the loop terminates without finding target, return <code>-1</code>.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [-1, 0, 3, 5, 9, 12], target = 9</h2>
<pre class="viz">Step 1: left = 0, right = 5
        mid = 0 + (5 - 0) // 2 = 2 → nums[2] = 3
        3 < 9 → search right → left = mid + 1 = 3

Step 2: left = 3, right = 5
        mid = 3 + (5 - 3) // 2 = 4 → nums[4] = 9
        nums[4] == target (9) → MATCH! Return 4. ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def search(nums, target):
    """
    Classic iterative binary search with closed interval [left, right].
    """
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
            
    return -1</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(log n)</strong> — The search space is halved every iteration. <strong>Space O(1)</strong> — Iterative implementation uses only two boundary pointers.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Array of size 1: target present or absent.</li>
<li>Target smaller than all elements or larger than all elements.</li>
<li>Negative values and zeros handled naturally without type casting.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Search Insert Position ([[35]]).</li>
<li>Find First and Last Position of Element in Sorted Array ([[34]]).</li>
</ul>''',

# ============================================================ LC 35
35: '''<h2>🧭 How to think about it</h2>
<p>Given a sorted array of distinct integers and a target value, return the index if the target is found. If not, return the index where it would be if it were inserted in order. The requirement is an algorithm with <strong>O(log n)</strong> runtime complexity.</p>

<h2>🐢 Brute force first</h2>
<p>Linear scan until finding an element <code>>= target</code>. Return that index, or <code>n</code> if target is greater than all elements. Time: O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> This is finding the <strong>lower bound</strong> (first element <code>>= target</code>). When the standard binary search terminates with <code>left > right</code>, <code>left</code> is exactly the insertion point where the target belongs!</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Initialize <code>left = 0</code>, <code>right = len(nums) - 1</code>.</li>
<li>While <code>left &lt;= right</code>:</li>
<li>Compute <code>mid = left + (right - left) // 2</code>.</li>
<li>If <code>nums[mid] == target</code>, target already exists, return <code>mid</code>.</li>
<li>If <code>nums[mid] &lt; target</code>, target belongs to the right, so <code>left = mid + 1</code>.</li>
<li>Else, target belongs to the left or at <code>mid</code>, so <code>right = mid - 1</code>.</li>
<li>When the loop exits, <code>left</code> points precisely to the correct insertion position. Return <code>left</code>.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [1, 3, 5, 6], target = 2</h2>
<pre class="viz">Initial: left = 0, right = 3
Iter 1: mid = 1, nums[1] = 3 > 2 → right = mid - 1 = 0
Iter 2: left = 0, right = 0
        mid = 0, nums[0] = 1 < 2 → left = mid + 1 = 1
Loop ends because left (1) > right (0).
Return left = 1.
Insert 2 at index 1 → [1, 2, 3, 5, 6] (sorted!). ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def searchInsert(nums, target):
    """
    Binary search lower bound: finds first index with nums[i] >= target.
    """
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
            
    # When loop ends, left points to insertion index
    return left</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(log n)</strong> — Binary search divides search space by 2 each step. <strong>Space O(1)</strong> — In-place pointer manipulation.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Target smaller than <code>nums[0]</code>: <code>left</code> ends at 0.</li>
<li>Target greater than <code>nums[-1]</code>: <code>left</code> ends at <code>len(nums)</code>.</li>
<li>Single element array matching target or not matching.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>C++ <code>std::lower_bound</code> and Python <code>bisect.bisect_left</code>.</li>
<li>Kth Missing Positive Number ([[1539]]).</li>
</ul>''',

# ============================================================ LC 69
69: '''<h2>🧭 How to think about it</h2>
<p>Given a non-negative integer <code>x</code>, compute and return the square root of <code>x</code> rounded down to the nearest integer. The returned integer should be non-negative as well. Do not use built-in exponent functions like <code>pow(x, 0.5)</code>.</p>

<h2>🐢 Brute force first</h2>
<p>Try every integer <code>i = 1, 2, 3...</code> and check if <code>i * i <= x</code>. Stop when <code>(i+1) * (i+1) > x</code>. Time: <strong>O(sqrt(x))</strong>. For <code>x = 2^31 - 1</code>, sqrt(x) ≈ 46,340 iterations.</p>

<div class="insight">💡 <strong>Key insight:</strong> The function <code>f(m) = m * m</code> is monotonically increasing for <code>m >= 0</code>. This is a binary search on the range <code>[0, x]</code> (or <code>[1, x // 2]</code> for <code>x >= 4</code>). We seek the largest integer <code>m</code> such that <code>m * m <= x</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>If <code>x &lt; 2</code>, return <code>x</code> (handles 0 and 1).</li>
<li>Set <code>left = 1</code>, <code>right = x // 2</code>.</li>
<li>While <code>left &lt;= right</code>:</li>
<li>Compute <code>mid = left + (right - left) // 2</code>.</li>
<li>Compute <code>sq = mid * mid</code>.</li>
<li>If <code>sq == x</code>, return <code>mid</code>.</li>
<li>If <code>sq &lt; x</code>, <code>mid</code> is a valid candidate for floor(sqrt(x)), but a larger one might exist: <code>ans = mid</code>, <code>left = mid + 1</code>.</li>
<li>Else (<code>sq &gt; x</code>), <code>mid</code> is too large: <code>right = mid - 1</code>.</li>
<li>Return <code>ans</code>.</li>
</ol>

<h2>🎞️ Visual dry run — x = 8</h2>
<pre class="viz">Range: left = 1, right = 4 (8 // 2)
Iter 1: mid = 2, sq = 4 <= 8 → ans = 2, left = 3
Iter 2: left = 3, right = 4, mid = 3, sq = 9 > 8 → right = 2
Loop ends because left (3) > right (2).
Return ans = 2. (Since 2^2 = 4 <= 8 < 3^2 = 9) ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def mySqrt(x):
    """
    Approach 1: Binary search on answer range [0, x // 2]
    """
    if x < 2:
        return x
        
    left, right = 1, x // 2
    ans = 1
    
    while left <= right:
        mid = left + (right - left) // 2
        if mid * mid <= x:
            ans = mid
            left = mid + 1
        else:
            right = mid - 1
            
    return ans

# Approach 2: Newton-Raphson method (super fast convergence)
def mySqrt_newton(x):
    if x < 2:
        return x
    r = x
    while r * r > x:
        r = (r + x // r) // 2
    return r</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(log x)</strong> for binary search (or O(log(log x)) for Newton's method). <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li><code>x = 0</code>: returns 0.</li>
<li><code>x = 1</code>: returns 1.</li>
<li>Large integers up to <code>2^31 - 1</code>: avoid overflow in languages with fixed integer sizes by using <code>mid <= x // mid</code>.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Valid Perfect Square ([[367]]).</li>
<li>Pow(x, n) ([[50]]).</li>
</ul>''',

# ============================================================ LC 74
74: '''<h2>🧭 How to think about it</h2>
<p>You are given an <code>m x n</code> integer matrix with two properties: each row is sorted in non-decreasing order, and the first integer of each row is greater than the last integer of the previous row. Determine if <code>target</code> exists in the matrix in <strong>O(log(m * n))</strong> time.</p>

<h2>🐢 Brute force first</h2>
<p>Linear scan over all <code>m * n</code> cells → O(m * n). Or binary search each row independently → O(m log n). Suboptimal because the matrix is globally sorted end-to-end!</p>

<div class="insight">💡 <strong>Key insight:</strong> The entire matrix can be treated as a single flattened 1D sorted array of length <code>m * n</code>! Any 1D index <code>idx</code> maps directly to 2D coordinates: <code>row = idx // n</code>, <code>col = idx % n</code>. Run standard binary search on <code>[0, m * n - 1]</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Let <code>m = len(matrix)</code>, <code>n = len(matrix[0])</code>.</li>
<li>Initialize <code>left = 0</code>, <code>right = m * n - 1</code>.</li>
<li>While <code>left &lt;= right</code>:</li>
<li>Compute <code>mid = left + (right - left) // 2</code>.</li>
<li>Convert <code>mid</code> to 2D coordinate: <code>val = matrix[mid // n][mid % n]</code>.</li>
<li>If <code>val == target</code>, return <code>True</code>.</li>
<li>If <code>val &lt; target</code>, <code>left = mid + 1</code>.</li>
<li>Else <code>right = mid - 1</code>.</li>
<li>If not found, return <code>False</code>.</li>
</ol>

<h2>🎞️ Visual dry run — matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3</h2>
<pre class="viz">m = 3, n = 4, total elements = 12. left = 0, right = 11.
Iter 1: mid = 5 → row = 5 // 4 = 1, col = 5 % 4 = 1
        matrix[1][1] = 11 > 3 → right = mid - 1 = 4
Iter 2: left = 0, right = 4, mid = 2 → row = 2 // 4 = 0, col = 2 % 4 = 2
        matrix[0][2] = 5 > 3 → right = mid - 1 = 1
Iter 3: left = 0, right = 1, mid = 0 → row = 0, col = 0
        matrix[0][0] = 1 < 3 → left = mid + 1 = 1
Iter 4: left = 1, right = 1, mid = 1 → row = 0, col = 1
        matrix[0][1] = 3 == 3 → MATCH! Return True. ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def searchMatrix(matrix, target):
    """
    Treat the m x n matrix as a single 1D virtual sorted array.
    """
    if not matrix or not matrix[0]:
        return False
        
    m, n = len(matrix), len(matrix[0])
    left, right = 0, m * n - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        # Coordinate mapping from 1D index to 2D row and col
        val = matrix[mid // n][mid % n]
        
        if val == target:
            return True
        elif val < target:
            left = mid + 1
        else:
            right = mid - 1
            
    return False</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(log(m * n))</strong> = O(log m + log n) — Performs binary search over <code>m * n</code> elements. <strong>Space O(1)</strong> — No flattened array created; coordinates computed via division/modulo on the fly.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>1x1 matrix: single cell comparison.</li>
<li>Single row or single column matrix: properly mapped by <code>mid // n</code> and <code>mid % n</code>.</li>
<li>Target smaller than matrix minimum (top-left) or larger than matrix maximum (bottom-right).</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Search a 2D Matrix II ([[240]]) — where rows and columns are sorted independently, but row 1 start is NOT greater than row 0 end.</li>
</ul>''',

# ============================================================ LC 240
240: '''<h2>🧭 How to think about it</h2>
<p>Write an efficient algorithm that searches for a value in an <code>m x n</code> matrix where integers in each row are sorted in ascending from left to right, and integers in each column are sorted in ascending from top to bottom. Unlike LC 74, the first element of row <code>i+1</code> is NOT necessarily greater than the last element of row <code>i</code>.</p>

<h2>🐢 Brute force first</h2>
<p>Linear scan of all cells takes O(m * n). Running binary search on each row takes O(m log n). Can we do O(m + n)?</p>

<div class="insight">💡 <strong>Key insight:</strong> Start at the <strong>top-right corner</strong> (or bottom-left). At position <code>(row, col) = (0, n-1)</code>: all elements in the same row to the left are smaller; all elements in the same column downward are larger! This creates a <strong>Binary Search Tree (BST)</strong> property rooted at the top-right corner. If <code>val > target</code>, decrement col; if <code>val < target</code>, increment row.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Start at <code>row = 0, col = n - 1</code> (top-right corner).</li>
<li>While <code>row &lt; m</code> and <code>col &gt;= 0</code>:</li>
<li>Let <code>val = matrix[row][col]</code>.</li>
<li>If <code>val == target</code>, return <code>True</code>.</li>
<li>If <code>val &gt; target</code>, target cannot be in column <code>col</code> (all elements below are even larger), so eliminate this column: <code>col -= 1</code>.</li>
<li>If <code>val &lt; target</code>, target cannot be in row <code>row</code> (all elements to the left are even smaller), so eliminate this row: <code>row += 1</code>.</li>
<li>If boundaries are crossed without finding target, return <code>False</code>.</li>
</ol>

<h2>🎞️ Visual dry run — target = 5</h2>
<pre class="viz">Matrix:
[ 1,  4,  7, 11, 15]
[ 2,  5,  8, 12, 19]
[ 3,  6,  9, 16, 22]

Start at (0, 4) = 15 > 5 → col--
Now at   (0, 3) = 11 > 5 → col--
Now at   (0, 2) =  7 > 5 → col--
Now at   (0, 1) =  4 < 5 → row++
Now at   (1, 1) =  5 == 5 → Found! Return True. ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def searchMatrix(matrix, target):
    """
    Z-search / Top-right corner traversal leveraging BST property.
    """
    if not matrix or not matrix[0]:
        return False
        
    m, n = len(matrix), len(matrix[0])
    row, col = 0, n - 1
    
    while row < m and col >= 0:
        val = matrix[row][col]
        if val == target:
            return True
        elif val > target:
            col -= 1  # eliminate column
        else:
            row += 1  # eliminate row
            
    return False</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(m + n)</strong> — Each step either decrements <code>col</code> or increments <code>row</code>. At most <code>m + n</code> steps. <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Empty matrix or row with 0 length.</li>
<li>Target smaller than top-left or larger than bottom-right.</li>
<li>Matrix of 1x1.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Search a 2D Matrix I ([[74]]).</li>
<li>Kth Smallest Element in a Sorted Matrix ([[378]]).</li>
</ul>''',

# ============================================================ LC 278
278: '''<h2>🧭 How to think about it</h2>
<p>Suppose you have <code>n</code> versions <code>[1, 2, ..., n]</code> and you want to find out the first bad one, which causes all following ones to be bad. You are given an API <code>isBadVersion(version)</code> which returns whether version is bad. Minimize calls to the API.</p>

<h2>🐢 Brute force first</h2>
<p>Call <code>isBadVersion(i)</code> for <code>i = 1, 2, ... n</code>. First one returning <code>True</code> is the answer. Takes O(n) API calls.</p>

<div class="insight">💡 <strong>Key insight:</strong> The versions form a monotonic predicate sequence: <code>[False, False, ..., False, True, True, ..., True]</code>. We need to find the boundary index where <code>isBadVersion</code> turns from <code>False</code> to <code>True</code>. This is a classic binary search on a condition function!</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Initialize <code>left = 1</code>, <code>right = n</code>.</li>
<li>While <code>left &lt; right</code>:</li>
<li>Compute <code>mid = left + (right - left) // 2</code>.</li>
<li>If <code>isBadVersion(mid) == True</code>: <code>mid</code> could be the first bad version or a later bad version. The first bad version must be at <code>mid</code> or to its left: <code>right = mid</code>.</li>
<li>Else (<code>False</code>): <code>mid</code> and all versions before it are good: <code>left = mid + 1</code>.</li>
<li>When <code>left == right</code>, the search space has converged to the exact first bad version. Return <code>left</code>.</li>
</ol>

<h2>🎞️ Visual dry run — n = 5, bad = 4</h2>
<pre class="viz">Versions: [1:F, 2:F, 3:F, 4:T, 5:T]
Iter 1: left = 1, right = 5 → mid = 3 → isBad(3) = False → left = 4
Iter 2: left = 4, right = 5 → mid = 4 → isBad(4) = True → right = 4
left == right == 4. Loop terminates.
Return 4. (Only 2 API calls instead of 4). ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def firstBadVersion(n):
    """
    Binary search for transition boundary: False -> True.
    Note the loop condition left < right and right = mid.
    """
    left, right = 1, n
    
    while left < right:
        mid = left + (right - left) // 2
        if isBadVersion(mid):
            right = mid      # mid could be first bad version
        else:
            left = mid + 1   # mid is definitely good
            
    return left</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(log n)</strong> — Halves the remaining versions each step. <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li><code>n = 1</code>: loop terminates immediately, returns 1 with 0 API calls.</li>
<li>First version is bad (<code>bad = 1</code>): <code>right</code> collapses down to 1.</li>
<li>Last version is bad (<code>bad = n</code>): <code>left</code> advances up to <code>n</code>.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Guess Number Higher or Lower ([[374]]).</li>
<li>Find Peak Element ([[162]]).</li>
</ul>''',

# ============================================================ LC 374
374: '''<h2>🧭 How to think about it</h2>
<p>We are playing the Guess Game. You pick a number from <code>1</code> to <code>n</code>. I have picked a number from <code>1</code> to <code>n</code>. You have to guess which number I picked. Call predefined API <code>guess(num)</code> which returns <code>-1</code> if your guess is higher than picked, <code>1</code> if your guess is lower, and <code>0</code> if your guess is equal.</p>

<h2>🐢 Brute force first</h2>
<p>Guess each number 1, 2, ..., n one by one. O(n) guesses.</p>

<div class="insight">💡 <strong>Key insight:</strong> Standard binary search on range <code>[1, n]</code> using feedback from <code>guess(mid)</code>. If <code>guess(mid) == 0</code>: return <code>mid</code>; if <code>guess(mid) == -1</code>: guess is too high, search left (<code>right = mid - 1</code>); if <code>guess(mid) == 1</code>: guess is too low, search right (<code>left = mid + 1</code>).</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Set <code>left = 1</code>, <code>right = n</code>.</li>
<li>While <code>left &lt;= right</code>:</li>
<li><code>mid = left + (right - left) // 2</code>.</li>
<li><code>res = guess(mid)</code>.</li>
<li>If <code>res == 0</code>, return <code>mid</code>.</li>
<li>If <code>res == -1</code>, <code>right = mid - 1</code>.</li>
<li>Else, <code>left = mid + 1</code>.</li>
</ol>

<h2>🎞️ Visual dry run — n = 10, pick = 6</h2>
<pre class="viz">Iter 1: left = 1, right = 10, mid = 5 → guess(5) = 1 (too low) → left = 6
Iter 2: left = 6, right = 10, mid = 8 → guess(8) = -1 (too high) → right = 7
Iter 3: left = 6, right = 7,  mid = 6 → guess(6) = 0 → MATCH! Return 6. ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def guessNumber(n):
    left, right = 1, n
    
    while left <= right:
        mid = left + (right - left) // 2
        res = guess(mid)
        
        if res == 0:
            return mid
        elif res == -1:
            right = mid - 1
        else:
            left = mid + 1
            
    return -1</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(log n)</strong> — Halves search space each query. <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li><code>n = 1</code>, pick = 1.</li>
<li>Pick is 1 or <code>n</code> (extreme bounds).</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Guess Number Higher or Lower II ([[375]]) — Minimax dynamic programming with cost.</li>
</ul>''',

# ============================================================ LC 540
540: '''<h2>🧭 How to think about it</h2>
<p>You are given a sorted array consisting of only integers where every element appears exactly twice, except for one element which appears exactly once. Find this single element that appears only once. Your solution must run in <strong>O(log n)</strong> time and <strong>O(1)</strong> space.</p>

<h2>🐢 Brute force first</h2>
<p>XOR all elements together: <code>x ^ x = 0</code> and <code>x ^ 0 = x</code>. Time: O(n), Space: O(1). Or linear scan checking adjacent pairs in O(n). To achieve O(log n), we must leverage the sorted structure with binary search.</p>

<div class="insight">💡 <strong>Key insight:</strong> Before the unique element, pairs always start at an <strong>even index</strong> and end at an <strong>odd index</strong>: <code>(0, 1), (2, 3), (4, 5)...</code>. After the unique element, every pair gets shifted right by 1, so pairs start at an <strong>odd index</strong> and end at an <strong>even index</strong>! Thus, if <code>mid</code>'s pair is correctly positioned, the unique element is to the right; otherwise it's at <code>mid</code> or to the left!</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Set <code>left = 0</code>, <code>right = len(nums) - 1</code>.</li>
<li>While <code>left &lt; right</code>:</li>
<li>Compute <code>mid = left + (right - left) // 2</code>.</li>
<li>If <code>mid % 2 == 1</code>, decrement <code>mid -= 1</code> so that <code>mid</code> is always the first element of an expected pair.</li>
<li>If <code>nums[mid] == nums[mid + 1]</code>: The pair is properly aligned! The single element has not disrupted pairing yet, so it lies strictly to the right: <code>left = mid + 2</code>.</li>
<li>Else: The alignment is broken! The single element is either at <code>mid</code> or to its left: <code>right = mid</code>.</li>
<li>When <code>left == right</code>, return <code>nums[left]</code>.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [1, 1, 2, 3, 3, 4, 4, 8, 8]</h2>
<pre class="viz">Indices:  0  1  2  3  4  5  6  7  8
Values:  [1, 1, 2, 3, 3, 4, 4, 8, 8]

Iter 1: left = 0, right = 8 → mid = 4 (even)
        nums[4] = 3, nums[5] = 4 → nums[4] != nums[5]!
        Alignment broken → right = mid = 4

Iter 2: left = 0, right = 4 → mid = 2 (even)
        nums[2] = 2, nums[3] = 3 → nums[2] != nums[3]!
        Alignment broken → right = mid = 2

Iter 3: left = 0, right = 2 → mid = 1 (odd) → mid = 0 (even)
        nums[0] = 1 == nums[1] → aligned!
        left = mid + 2 = 2

left == right == 2.
Return nums[2] = 2! ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def singleNonDuplicate(nums):
    """
    Binary search on even indices to find the parity disruption.
    """
    left, right = 0, len(nums) - 1
    
    while left < right:
        mid = left + (right - left) // 2
        # Ensure mid is even
        if mid % 2 == 1:
            mid -= 1
            
        if nums[mid] == nums[mid + 1]:
            # Pair is intact; anomaly is to the right
            left = mid + 2
        else:
            # Pair broken; anomaly is at mid or left
            right = mid
            
    return nums[left]</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(log n)</strong> — Standard binary search halving the search space each step. <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Single element array <code>[1]</code>: returns 1 immediately.</li>
<li>Single element at index 0 (first element unique): <code>nums[0] != nums[1]</code> collapses <code>right</code> to 0.</li>
<li>Single element at last index: <code>left</code> advances all the way to <code>len(nums) - 1</code>.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Find the Duplicate Number ([[287]]).</li>
<li>Single Number I, II, III ([[136]], [[137]], [[260]]).</li>
</ul>''',

# ============================================================ LC 1539
1539: '''<h2>🧭 How to think about it</h2>
<p>Given an array <code>arr</code> of positive integers sorted in strictly ascending order, and an integer <code>k</code>, return the <code>k-th</code> positive integer that is missing from this array.</p>

<h2>🐢 Brute force first</h2>
<p>Scan <code>num = 1, 2, 3...</code> using a pointer in <code>arr</code>. If <code>num == arr[i]</code>, advance <code>i</code>; otherwise decrement <code>k</code>. When <code>k == 0</code>, return <code>num</code>. Time: O(n + k), Space: O(1).</p>

<div class="insight">💡 <strong>Key insight:</strong> At index <code>i</code>, how many positive integers should precede it if none were missing? Exactly <code>arr[i] - (i + 1)</code>! Because the array is sorted, this missing count <code>arr[i] - (i + 1)</code> is <strong>monotonically non-decreasing</strong>! We can binary search for the largest index where missing count &lt; <code>k</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Set <code>left = 0</code>, <code>right = len(arr) - 1</code>.</li>
<li>While <code>left &lt;= right</code>:</li>
<li>Compute <code>mid = left + (right - left) // 2</code>.</li>
<li>Calculate missing before <code>mid</code>: <code>missing = arr[mid] - (mid + 1)</code>.</li>
<li>If <code>missing &lt; k</code>, we need to search further right: <code>left = mid + 1</code>.</li>
<li>Else, search left: <code>right = mid - 1</code>.</li>
<li>When the loop terminates, <code>left</code> is the number of elements in <code>arr</code> that are smaller than the kth missing number. The answer is simply <code>left + k</code>!</li>
</ol>

<h2>🎞️ Visual dry run — arr = [2, 3, 4, 7, 11], k = 5</h2>
<pre class="viz">Index i:       0   1   2   3   4
arr[i]:        2   3   4   7  11
Missing count: 1   1   1   3   6  (arr[i] - (i + 1))
k = 5.

Iter 1: left = 0, right = 4 → mid = 2
        missing = 4 - 3 = 1 < 5 → left = mid + 1 = 3
Iter 2: left = 3, right = 4 → mid = 3
        missing = 7 - 4 = 3 < 5 → left = mid + 1 = 4
Iter 3: left = 4, right = 4 → mid = 4
        missing = 11 - 5 = 6 >= 5 → right = mid - 1 = 3
Loop ends with left = 4.
Answer = left + k = 4 + 5 = 9!
Missing numbers: [1, 5, 6, 8, 9...] → 5th missing is 9. ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def findKthPositive(arr, k):
    """
    Binary search on the number of missing integers.
    arr[i] - (i + 1) gives missing count up to index i.
    """
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        missing = arr[mid] - (mid + 1)
        
        if missing < k:
            left = mid + 1
        else:
            right = mid - 1
            
    # At termination, missing count before index 'right' is < k.
    # The kth missing number = arr[right] + (k - missing_at_right)
    # = arr[right] + k - (arr[right] - (right + 1)) = right + 1 + k = left + k
    return left + k</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(log n)</strong> — Binary search over array length. <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>All missing numbers before <code>arr[0]</code> (e.g. <code>arr = [5, 6, 7], k = 2</code>): <code>left = 0</code>, returns <code>0 + 2 = 2</code>.</li>
<li>All missing numbers after array (e.g. <code>arr = [1, 2, 3], k = 2</code>): <code>left = 3</code>, returns <code>3 + 2 = 5</code>.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Missing Element in Sorted Array ([[1060]]).</li>
</ul>''',

# ============================================================ LC 33
33: '''<h2>🧭 How to think about it</h2>
<p>There is an integer array <code>nums</code> sorted in ascending order (with distinct values) that has been rotated at an unknown pivot index. Given the rotated array and a target, return its index if found, or <code>-1</code> if not. Must be <strong>O(log n)</strong> time.</p>

<h2>🐢 Brute force first</h2>
<p>Linear scan over all elements takes O(n). To achieve O(log n), we must identify which half of the array is sorted at any given step.</p>

<div class="insight">💡 <strong>Key insight:</strong> If you divide a rotated sorted array in half at <code>mid</code>, <strong>at least one half is always strictly sorted</strong>! Check if <code>nums[left] <= nums[mid]</code>. If yes, the left half is sorted; otherwise the right half is sorted. Once you know which half is sorted, you can check if <code>target</code> falls inside its range in O(1) and discard the other half!</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Set <code>left = 0, right = len(nums) - 1</code>.</li>
<li>While <code>left &lt;= right</code>:</li>
<li>Compute <code>mid = left + (right - left) // 2</code>.</li>
<li>If <code>nums[mid] == target</code>, return <code>mid</code>.</li>
<li><strong>Check if left half is sorted:</strong> <code>nums[left] &lt;= nums[mid]</code>:</li>
<li>&nbsp;&nbsp;If <code>nums[left] &lt;= target &lt; nums[mid]</code>: target is in the left half, so <code>right = mid - 1</code>.</li>
<li>&nbsp;&nbsp;Else: target must be in the right half, so <code>left = mid + 1</code>.</li>
<li><strong>Else (right half is sorted):</strong></li>
<li>&nbsp;&nbsp;If <code>nums[mid] &lt; target &lt;= nums[right]</code>: target is in the right half, so <code>left = mid + 1</code>.</li>
<li>&nbsp;&nbsp;Else: target must be in the left half, so <code>right = mid - 1</code>.</li>
<li>If not found, return <code>-1</code>.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [4, 5, 6, 7, 0, 1, 2], target = 0</h2>
<pre class="viz">Iter 1: left = 0, right = 6 → mid = 3, nums[mid] = 7
        nums[left] = 4 <= 7 → Left half [4, 5, 6, 7] is sorted!
        Is 4 <= target(0) < 7? No!
        Target must be in right half → left = mid + 1 = 4

Iter 2: left = 4, right = 6 → mid = 5, nums[mid] = 1
        nums[left] = 0 <= 1 → Left half [0, 1] is sorted!
        Is 0 <= target(0) < 1? Yes!
        Target is in left half → right = mid - 1 = 4

Iter 3: left = 4, right = 4 → mid = 4, nums[mid] = 0 == target!
        Match! Return 4. ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def search(nums, target):
    """
    Binary search in rotated sorted array.
    Determine sorted half and check if target is within bounds.
    """
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if nums[mid] == target:
            return mid
            
        # Left half is sorted
        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        # Right half is sorted
        else:
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
                
    return -1</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(log n)</strong> — Search space halved at each step. <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Array not rotated (standard sorted array): handled identically.</li>
<li>Array of size 1 or 2.</li>
<li>Target at rotation pivot boundary.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Search in Rotated Sorted Array II with duplicates ([[81]]).</li>
<li>Find Minimum in Rotated Sorted Array ([[153]]).</li>
</ul>''',

# ============================================================ LC 81
81: '''<h2>🧭 How to think about it</h2>
<p>Given the array <code>nums</code> after rotation, and an integer <code>target</code>, return <code>true</code> if target is in <code>nums</code>, or <code>false</code> if it is not. This problem differs from LC 33 because <strong><code>nums</code> may contain duplicate elements</strong>.</p>

<h2>🐢 Brute force first</h2>
<p>Linear scan O(n). Because duplicates can mask which half is sorted, the worst-case for binary search is actually O(n) too (e.g. <code>[1, 1, 1, 1, 2, 1, 1]</code>).</p>

<div class="insight">💡 <strong>Key insight:</strong> When duplicates exist, <code>nums[left] == nums[mid] == nums[right]</code> can happen! When this occurs, we cannot determine whether the left or right half is sorted. The remedy is simple: <strong>shrink both boundaries</strong> <code>left += 1</code> and <code>right -= 1</code>, shedding the ambiguity safely without losing a target that equals <code>mid</code>!</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Set <code>left = 0, right = len(nums) - 1</code>.</li>
<li>While <code>left &lt;= right</code>:</li>
<li>Compute <code>mid = left + (right - left) // 2</code>.</li>
<li>If <code>nums[mid] == target</code>, return <code>True</code>.</li>
<li><strong>Handle ambiguous duplicates:</strong> If <code>nums[left] == nums[mid] == nums[right]</code>: <code>left += 1; right -= 1; continue</code>.</li>
<li>If left half is sorted (<code>nums[left] &lt;= nums[mid]</code>):</li>
<li>&nbsp;&nbsp;If <code>nums[left] &lt;= target &lt; nums[mid]</code>: <code>right = mid - 1</code>, else <code>left = mid + 1</code>.</li>
<li>Else (right half is sorted):</li>
<li>&nbsp;&nbsp;If <code>nums[mid] &lt; target &lt;= nums[right]</code>: <code>left = mid + 1</code>, else <code>right = mid - 1</code>.</li>
<li>Return <code>False</code> if loop terminates.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [1, 0, 1, 1, 1], target = 0</h2>
<pre class="viz">Iter 1: left = 0, right = 4 → mid = 2
        nums[left]=1, nums[mid]=1, nums[right]=1
        All equal! Cannot tell which half is sorted.
        Shrink: left = 1, right = 3

Iter 2: left = 1, right = 3 → mid = 2, nums[mid] = 1 != target(0)
        nums[left]=0, nums[mid]=1 → left half sorted!
        0 <= target(0) < 1 → target in left half!
        right = mid - 1 = 1

Iter 3: left = 1, right = 1 → mid = 1, nums[mid] = 0 == 0! Match! Return True. ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def search(nums, target):
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if nums[mid] == target:
            return True
            
        # Ambiguous case: cannot determine sorted half
        if nums[left] == nums[mid] == nums[right]:
            left += 1
            right -= 1
            continue
            
        # Left half is sorted
        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        # Right half is sorted
        else:
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
                
    return False</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Average Time O(log n)</strong>; <strong>Worst-case Time O(n)</strong> when nearly all elements are identical. <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>All elements identical: e.g. <code>[2, 2, 2, 2]</code> searching for 3.</li>
<li>Target is the duplicate value itself.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Find Minimum in Rotated Sorted Array II ([[154]]).</li>
</ul>''',

# ============================================================ LC 153
153: '''<h2>🧭 How to think about it</h2>
<p>Suppose an array of length <code>n</code> sorted in ascending order is rotated between 1 and <code>n</code> times. Notice that all values are <strong>unique</strong>. Find the minimum element of this array in <strong>O(log n)</strong> time.</p>

<h2>🐢 Brute force first</h2>
<p>Scan array linearly to find <code>min(nums)</code> in O(n). To do O(log n), observe the inflection point.</p>

<div class="insight">💡 <strong>Key insight:</strong> Compare <code>nums[mid]</code> directly with <code>nums[right]</code>! If <code>nums[mid] > nums[right]</code>, the minimum element MUST be strictly to the right of <code>mid</code> (in <code>[mid + 1, right]</code>), because the rotation point broke ascending order. If <code>nums[mid] < nums[right]</code>, the minimum element is at <code>mid</code> or to its left (in <code>[left, mid]</code>)!</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Initialize <code>left = 0, right = len(nums) - 1</code>.</li>
<li>While <code>left &lt; right</code>:</li>
<li>Compute <code>mid = left + (right - left) // 2</code>.</li>
<li>If <code>nums[mid] &gt; nums[right]</code>: minimum must be to the right of <code>mid</code> → <code>left = mid + 1</code>.</li>
<li>Else: <code>nums[mid] &lt;= nums[right]</code>: <code>mid</code> could be the minimum itself or min is to the left → <code>right = mid</code>.</li>
<li>When <code>left == right</code>, the search window converges on the minimum element. Return <code>nums[left]</code>.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [4, 5, 6, 7, 0, 1, 2]</h2>
<pre class="viz">Iter 1: left = 0, right = 6 → mid = 3, nums[3] = 7
        nums[3] (7) > nums[6] (2) → minimum is right of mid!
        left = mid + 1 = 4

Iter 2: left = 4, right = 6 → mid = 5, nums[5] = 1
        nums[5] (1) < nums[6] (2) → minimum is at mid or left!
        right = mid = 5

Iter 3: left = 4, right = 5 → mid = 4, nums[4] = 0
        nums[4] (0) < nums[5] (1) → right = mid = 4

left == right == 4.
Return nums[4] = 0! ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def findMin(nums):
    """
    Binary search comparing with right boundary.
    Invariant: minimum element is always inside [left, right].
    """
    left, right = 0, len(nums) - 1
    
    while left < right:
        mid = left + (right - left) // 2
        
        if nums[mid] > nums[right]:
            # Min is in right portion
            left = mid + 1
        else:
            # Min is mid or in left portion
            right = mid
            
    return nums[left]</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(log n)</strong> — Binary search cuts interval in half each iteration. <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Array rotated 0 times (already fully sorted): <code>nums[mid] < nums[right]</code> immediately shrinks <code>right</code> to 0.</li>
<li>Single element array: loop terminates immediately, returns <code>nums[0]</code>.</li>
<li>Two element array: correctly chooses the smaller.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Find Minimum in Rotated Sorted Array II ([[154]]) with duplicates.</li>
<li>Search in Rotated Sorted Array ([[33]]).</li>
</ul>''',

# ============================================================ LC 162
162: '''<h2>🧭 How to think about it</h2>
<p>A peak element is an element that is strictly greater than its neighbors. Given a 0-indexed integer array <code>nums</code>, find a peak element, and return its index. If the array contains multiple peaks, return the index to <strong>any of the peaks</strong>. Imagine <code>nums[-1] = nums[n] = -inf</code>. Must run in <strong>O(log n)</strong> time.</p>

<h2>🐢 Brute force first</h2>
<p>Linear scan comparing <code>nums[i] > nums[i+1]</code>. First element that decreases is a peak. Time: O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> Even though the array is NOT sorted, binary search still works! Compare <code>nums[mid]</code> with <code>nums[mid + 1]</code>: if <code>nums[mid] < nums[mid + 1]</code>, we are on an <strong>upward slope</strong>, which guarantees at least one peak must exist to the right! If <code>nums[mid] > nums[mid + 1]</code>, we are on a <strong>downward slope</strong>, so a peak exists at <code>mid</code> or to the left.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Initialize <code>left = 0, right = len(nums) - 1</code>.</li>
<li>While <code>left &lt; right</code>:</li>
<li>Compute <code>mid = left + (right - left) // 2</code>.</li>
<li>If <code>nums[mid] &lt; nums[mid + 1]</code>: climb up to the right → <code>left = mid + 1</code>.</li>
<li>Else: <code>nums[mid] &gt; nums[mid + 1]</code>: peak must be at <code>mid</code> or to the left → <code>right = mid</code>.</li>
<li>When <code>left == right</code>, return <code>left</code>.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [1, 2, 1, 3, 5, 6, 4]</h2>
<pre class="viz">Iter 1: left = 0, right = 6 → mid = 3
        nums[3] = 3 < nums[4] = 5 → Upward slope! Search right.
        left = mid + 1 = 4

Iter 2: left = 4, right = 6 → mid = 5
        nums[5] = 6 > nums[6] = 4 → Downward slope! Search left / mid.
        right = mid = 5

Iter 3: left = 4, right = 5 → mid = 4
        nums[4] = 5 < nums[5] = 6 → Upward slope!
        left = mid + 1 = 5

left == right == 5.
nums[5] = 6 > 5 and 6 > 4. Peak found at index 5! ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def findPeakElement(nums):
    """
    Binary search following the upward slope.
    """
    left, right = 0, len(nums) - 1
    
    while left < right:
        mid = left + (right - left) // 2
        
        if nums[mid] < nums[mid + 1]:
            # Peak must be to the right
            left = mid + 1
        else:
            # Peak is at mid or to the left
            right = mid
            
    return left</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(log n)</strong> — Halves search window each step. <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Strictly increasing array: peak is at last index.</li>
<li>Strictly decreasing array: peak is at index 0.</li>
<li>Single element array: returns 0 immediately.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Peak Index in a Mountain Array ([[852]]).</li>
<li>Find in Mountain Array ([[1095]]).</li>
</ul>''',

# ============================================================ LC 852
852: '''<h2>🧭 How to think about it</h2>
<p>An array <code>arr</code> is a mountain if it increases to a single peak and then decreases. Given a mountain array, return the index <code>i</code> such that <code>arr[0] &lt; arr[1] &lt; ... arr[i-1] &lt; arr[i] &gt; arr[i+1] &gt; ... &gt; arr[arr.length - 1]</code>. Must be <strong>O(log(arr.length))</strong>.</p>

<h2>🐢 Brute force first</h2>
<p>Scan linearly until <code>arr[i] > arr[i+1]</code>. Return <code>i</code>. Time O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> The mountain array has two distinct phases: ascending (<code>arr[i] < arr[i+1]</code>) and descending (<code>arr[i] > arr[i+1]</code>). The peak is the unique transition point. Binary search easily identifies which slope <code>mid</code> lies on.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Initialize <code>left = 0, right = len(arr) - 1</code>.</li>
<li>While <code>left &lt; right</code>:</li>
<li>Compute <code>mid = left + (right - left) // 2</code>.</li>
<li>If <code>arr[mid] &lt; arr[mid + 1]</code>, we are ascending: <code>left = mid + 1</code>.</li>
<li>Else, we are descending or at the peak: <code>right = mid</code>.</li>
<li>Return <code>left</code> when <code>left == right</code>.</li>
</ol>

<h2>🎞️ Visual dry run — arr = [0, 10, 5, 2]</h2>
<pre class="viz">Iter 1: left = 0, right = 3 → mid = 1
        arr[1] = 10 > arr[2] = 5 → descending slope!
        right = mid = 1
Iter 2: left = 0, right = 1 → mid = 0
        arr[0] = 0 < arr[1] = 10 → ascending slope!
        left = mid + 1 = 1
left == right == 1.
Peak is at index 1 (val = 10). ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def peakIndexInMountainArray(arr):
    left, right = 0, len(arr) - 1
    
    while left < right:
        mid = left + (right - left) // 2
        if arr[mid] < arr[mid + 1]:
            left = mid + 1
        else:
            right = mid
            
    return left</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(log n)</strong>. <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Guaranteed to be a mountain array of length at least 3, so peak is never at index 0 or index n-1.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Find in Mountain Array ([[1095]]) — 3-phase binary search.</li>
</ul>''',

# ============================================================ LC 1095
1095: '''<h2>🧭 How to think about it</h2>
<p>Given a mountain array <code>mountainArr</code>, return the <strong>minimum index</strong> such that <code>mountainArr.get(index) == target</code>. If such an index does not exist, return <code>-1</code>. Access to the array is only through an interface <code>MountainArray.get(k)</code> and <code>MountainArray.length()</code>. Submissions making more than <strong>100 calls</strong> to <code>get</code> will be judged Wrong Answer.</p>

<h2>🐢 Brute force first</h2>
<p>Linear scan calling <code>get(i)</code> for all <code>i</code> will exceed 100 calls for arrays up to 10,000 elements.</p>

<div class="insight">💡 <strong>Key insight:</strong> A mountain array consists of two monotonic halves split by the peak: an ascending left half and a descending right half. Execute a <strong>3-phase binary search</strong>:
1. Find peak index using binary search (at most ~14 calls).
2. Binary search for target in the strictly increasing left half <code>[0, peak]</code> (~14 calls).
3. If not found in left half, binary search in strictly decreasing right half <code>[peak + 1, n - 1]</code> (~14 calls).
Total calls: ~42 &lt;&lt; 100 limit!</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><strong>Phase 1: Find Peak:</strong> <code>left = 0, right = n - 1</code>. While <code>left &lt; right</code>, if <code>get(mid) &lt; get(mid + 1)</code>: <code>left = mid + 1</code>, else <code>right = mid</code>. <code>peak = left</code>.</li>
<li><strong>Phase 2: Search Left Half (Ascending):</strong> <code>left = 0, right = peak</code>. Standard ascending binary search. If found, return index immediately (satisfies minimum index requirement).</li>
<li><strong>Phase 3: Search Right Half (Descending):</strong> <code>left = peak + 1, right = n - 1</code>. Note the comparison logic is inverted since values decrease as index increases.</li>
<li>If neither finds target, return <code>-1</code>.</li>
</ol>

<h2>🎞️ Visual dry run — array = [1, 2, 3, 4, 5, 3, 1], target = 3</h2>
<pre class="viz">1. Find peak: peak is index 4 (val = 5).
2. Search left [0, 4] for target 3:
   mid = 2, get(2) = 3 == 3 → Found at index 2!
   Return 2 immediately without needing to search the right half. ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def findInMountainArray(target, mountain_arr):
    n = mountain_arr.length()
    
    # Phase 1: Find peak index
    left, right = 0, n - 1
    while left < right:
        mid = left + (right - left) // 2
        if mountain_arr.get(mid) < mountain_arr.get(mid + 1):
            left = mid + 1
        else:
            right = mid
    peak = left
    
    # Phase 2: Binary search on ascending left slope [0, peak]
    left, right = 0, peak
    while left <= right:
        mid = left + (right - left) // 2
        val = mountain_arr.get(mid)
        if val == target:
            return mid
        elif val < target:
            left = mid + 1
        else:
            right = mid - 1
            
    # Phase 3: Binary search on descending right slope [peak + 1, n - 1]
    left, right = peak + 1, n - 1
    while left <= right:
        mid = left + (right - left) // 2
        val = mountain_arr.get(mid)
        if val == target:
            return mid
        elif val < target:
            # Decreasing slope: smaller values are to the right
            right = mid - 1
        else:
            left = mid + 1
            
    return -1</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(log n)</strong> — 3 binary searches each taking O(log n). Total API calls &lt;= 3 * log2(10000) ≈ 42 calls. <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Target exists on both slopes: algorithm returns left index first because left slope is searched first.</li>
<li>Target is at the peak: found during left slope search.</li>
<li>Target not in array: returns -1 after exhaustive search.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Search in Rotated Sorted Array ([[33]]).</li>
<li>Peak Index in a Mountain Array ([[852]]).</li>
</ul>''',

# ============================================================ LC 875
875: '''<h2>🧭 How to think about it</h2>
<p>Koko loves to eat bananas. There are <code>n</code> piles of bananas, where the <code>i-th</code> pile has <code>piles[i]</code> bananas. The guards will return in <code>h</code> hours. Koko can decide her eating speed <code>k</code> (bananas-per-hour). Each hour, she chooses a pile and eats <code>k</code> bananas from it. If the pile has less than <code>k</code> bananas, she eats all of them and will not eat any more bananas during this hour. Return the minimum integer <code>k</code> such that she can eat all bananas within <code>h</code> hours.</p>

<h2>🐢 Brute force first</h2>
<p>Test speeds <code>k = 1, 2, 3... max(piles)</code>. For each speed, calculate total hours needed: <code>sum(math.ceil(pile / k))</code>. The first speed where total hours &lt;= <code>h</code> is the answer. Time: O(max(piles) * n). When <code>max(piles) = 10^9</code>, this TLEs immediately.</p>

<div class="insight">💡 <strong>Key insight:</strong> Notice the <strong>monotonicity</strong>! If Koko can finish all bananas at speed <code>k</code>, she can certainly finish them at any speed <code>> k</code>. If she cannot finish at speed <code>k</code>, she cannot finish at any speed <code>< k</code>. This monotonic feasibility predicate <code>canFinish(k) -> bool</code> enables <strong>Binary Search on Answer</strong> in range <code>[1, max(piles)]</code>!</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Set search range: <code>left = 1</code> (minimum possible eating speed) and <code>right = max(piles)</code> (maximum needed eating speed).</li>
<li>Define helper <code>canFinish(k)</code>: calculates total hours spent across all piles: <code>sum((pile + k - 1) // k)</code> (integer ceil). Returns <code>True</code> if total hours &lt;= <code>h</code>.</li>
<li>While <code>left &lt; right</code>:</li>
<li>Compute <code>mid = left + (right - left) // 2</code>.</li>
<li>If <code>canFinish(mid)</code> is <code>True</code>: <code>mid</code> might be the minimum speed or a smaller speed might work → <code>right = mid</code>.</li>
<li>Else: <code>mid</code> is too slow → <code>left = mid + 1</code>.</li>
<li>When <code>left == right</code>, return <code>left</code>.</li>
</ol>

<h2>🎞️ Visual dry run — piles = [3, 6, 7, 11], h = 8</h2>
<pre class="viz">Range: [left = 1, right = 11]
Iter 1: mid = 6
  piles: 3(1h) + 6(1h) + 7(2h) + 11(2h) = 6 hours <= 8 → Possible!
  right = mid = 6

Iter 2: left = 1, right = 6 → mid = 3
  piles: 3(1h) + 6(2h) + 7(3h) + 11(4h) = 10 hours > 8 → Too slow!
  left = mid + 1 = 4

Iter 3: left = 4, right = 6 → mid = 5
  piles: 3(1h) + 6(2h) + 7(2h) + 11(3h) = 8 hours <= 8 → Possible!
  right = mid = 5

Iter 4: left = 4, right = 5 → mid = 4
  piles: 3(1h) + 6(2h) + 7(2h) + 11(3h) = 8 hours <= 8 → Possible!
  right = mid = 4

left == right == 4.
Return 4 bananas/hour! ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>import math

def minEatingSpeed(piles, h):
    """
    Binary search on answer range [1, max(piles)].
    """
    def canFinish(k):
        # (pile + k - 1) // k is fast integer ceiling for pile / k
        return sum((p + k - 1) // k for p in piles) <= h
        
    left, right = 1, max(piles)
    
    while left < right:
        mid = left + (right - left) // 2
        if canFinish(mid):
            right = mid
        else:
            left = mid + 1
            
    return left</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n * log(max(piles)))</strong> — Each binary search step takes O(n) to sum hours across all piles, and the search range shrinks by 2 each step. <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li><code>len(piles) == h</code>: Koko must eat each pile in 1 hour, so answer is <code>max(piles)</code>.</li>
<li><code>h</code> very large: answer will be 1.</li>
<li>Very large pile sizes up to <code>10^9</code>: binary search completes in ~30 iterations.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Capacity To Ship Packages Within D Days ([[1011]]).</li>
<li>Find the Smallest Divisor Given a Threshold ([[1283]]).</li>
<li>Minimum Number of Days to Make m Bouquets ([[1482]]).</li>
</ul>''',

# ============================================================ LC 1011
1011: '''<h2>🧭 How to think about it</h2>
<p>A conveyor belt has packages that must be shipped within <code>days</code> days. The <code>i-th</code> package has weight <code>weights[i]</code>. Each day, we load the conveyor belt with packages in the order given by <code>weights</code>, without exceeding the ship's maximum weight capacity. Return the least weight capacity of the ship that will result in all packages being shipped within <code>days</code> days.</p>

<h2>🐢 Brute force first</h2>
<p>Start capacity at <code>max(weights)</code> (since the ship must hold the heaviest single package). Increment capacity one by one until simulation finishes in <code><= days</code>. Time: O(sum(weights) * n) — unacceptable.</p>

<div class="insight">💡 <strong>Key insight:</strong> Feasibility is monotonic! If capacity <code>C</code> can ship all packages within <code>days</code>, any capacity <code>> C</code> can as well. Lower bound is <code>max(weights)</code> (cannot leave behind any single package), upper bound is <code>sum(weights)</code> (shipping everything in 1 day). Binary search the interval <code>[max(weights), sum(weights)]</code>!</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Lower bound: <code>left = max(weights)</code>. Upper bound: <code>right = sum(weights)</code>.</li>
<li>Condition function <code>feasible(cap)</code>: simulate greedy packing in linear order:
  <ul>
    <li>Accumulate current daily load.</li>
    <li>If adding <code>w</code> exceeds <code>cap</code>, increment day count and start new day with <code>w</code>.</li>
    <li>Return <code>True</code> if total days &lt;= <code>days</code>.</li>
  </ul>
</li>
<li>Binary search: if <code>feasible(mid)</code>, try smaller capacity: <code>right = mid</code>. Else: <code>left = mid + 1</code>.</li>
<li>Return <code>left</code>.</li>
</ol>

<h2>🎞️ Visual dry run — weights = [1,2,3,4,5,6,7,8,9,10], days = 5</h2>
<pre class="viz">left = max = 10, right = sum = 55
Iter 1: mid = 32 → days needed = 2 <= 5 → feasible! right = 32
Iter 2: mid = 21 → days needed = 3 <= 5 → feasible! right = 21
Iter 3: mid = 15 → days: [1..5]=15, [6,7]=13, [8]=8, [9]=9, [10]=10 → 5 days! feasible! right = 15
Iter 4: mid = 12 → days needed = 6 > 5 → not feasible! left = 13
Iter 5: mid = 14 → days needed = 5 <= 5 → feasible! right = 14
Iter 6: mid = 13 → days needed = 6 > 5 → not feasible! left = 14
left == right == 15. Capacity = 15! ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def shipWithinDays(weights, days):
    def feasible(capacity):
        day_count = 1
        current_load = 0
        for w in weights:
            if current_load + w > capacity:
                day_count += 1
                current_load = w
            else:
                current_load += w
        return day_count <= days

    left, right = max(weights), sum(weights)
    
    while left < right:
        mid = left + (right - left) // 2
        if feasible(mid):
            right = mid
        else:
            left = mid + 1
            
    return left</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n * log(sum(weights) - max(weights)))</strong> — Each feasibility check takes O(n). <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li><code>days == 1</code>: capacity must be <code>sum(weights)</code>.</li>
<li><code>days >= len(weights)</code>: capacity only needs to be <code>max(weights)</code>.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Split Array Largest Sum ([[410]]) — mathematically identical problem disguised as array partitioning!</li>
</ul>''',

# ============================================================ LC 1283
1283: '''<h2>🧭 How to think about it</h2>
<p>Given an array of integers <code>nums</code> and an integer <code>threshold</code>, we need to choose a positive integer <code>divisor</code>, divide all the array by it, and sum the division's result. Find the smallest <code>divisor</code> such that the result mentioned above is less than or equal to <code>threshold</code>. Each division result is rounded up to the nearest integer greater than or equal to that element (e.g. <code>7/3 = 3</code>).</p>

<h2>🐢 Brute force first</h2>
<p>Try divisors <code>d = 1, 2, ... max(nums)</code>. Stop at first <code>d</code> with sum &lt;= <code>threshold</code>. O(n * max(nums)) TLEs.</p>

<div class="insight">💡 <strong>Key insight:</strong> As <code>divisor</code> increases, <code>ceil(num / divisor)</code> monotonically decreases, so total sum monotonically decreases! Binary search in range <code>[1, max(nums)]</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>left = 1, right = max(nums)</code>.</li>
<li>Helper <code>computeSum(d)</code>: returns <code>sum((x + d - 1) // d for x in nums)</code>.</li>
<li>While <code>left &lt; right</code>:</li>
<li><code>mid = left + (right - left) // 2</code>.</li>
<li>If <code>computeSum(mid) &lt;= threshold</code>: <code>mid</code> works, search for smaller: <code>right = mid</code>.</li>
<li>Else: <code>mid</code> produces too large a sum, divisor must be larger: <code>left = mid + 1</code>.</li>
<li>Return <code>left</code>.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [1, 2, 5, 9], threshold = 6</h2>
<pre class="viz">Range: [1, 9]
Iter 1: mid = 5 → ceil(1/5)+ceil(2/5)+ceil(5/5)+ceil(9/5) = 1+1+1+2 = 5 <= 6 → right = 5
Iter 2: left = 1, right = 5 → mid = 3 → ceil: 1+1+2+3 = 7 > 6 → left = 4
Iter 3: left = 4, right = 5 → mid = 4 → ceil: 1+1+2+3 = 7 > 6 → left = 5
left == right == 5.
Smallest divisor = 5. ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def smallestDivisor(nums, threshold):
    left, right = 1, max(nums)
    
    while left < right:
        mid = left + (right - left) // 2
        total = sum((x + mid - 1) // mid for x in nums)
        
        if total <= threshold:
            right = mid
        else:
            left = mid + 1
            
    return left</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n * log(max(nums)))</strong>. <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li><code>threshold == len(nums)</code>: divisor must be <code>max(nums)</code> since minimum contribution of each element is 1.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Koko Eating Bananas ([[875]]).</li>
<li>Minimized Maximum of Products Distributed to Any Store ([[2064]]).</li>
</ul>''',

# ============================================================ LC 1482
1482: '''<h2>🧭 How to think about it</h2>
<p>You are given an integer array <code>bloomDay</code>, an integer <code>m</code> and an integer <code>k</code>. You want to make <code>m</code> bouquets. To make a bouquet, you need to use <code>k</code> <strong>adjacent</strong> flowers from the garden. The garden consists of <code>n</code> flowers, the <code>i-th</code> flower will bloom in the <code>bloomDay[i]</code>. Return the minimum number of days you need to wait to be able to make <code>m</code> bouquets from the garden. If it is impossible, return <code>-1</code>.</p>

<h2>🐢 Brute force first</h2>
<p>If <code>m * k > len(bloomDay)</code>, impossible, return -1. Otherwise try day 1, 2... up to <code>max(bloomDay)</code>. For each day, simulate flower availability and greedily count adjacent groups of size <code>k</code>. O(max(bloomDay) * n) TLE.</p>

<div class="insight">💡 <strong>Key insight:</strong> The number of bloomed flowers increases over time. More flowers can only make it easier to form bouquets. Monotonic predicate <code>canMake(day) -> bool</code> enables binary search on <code>[min(bloomDay), max(bloomDay)]</code>!</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>If <code>m * k &gt; len(bloomDay)</code>, return <code>-1</code>.</li>
<li><code>left = min(bloomDay), right = max(bloomDay)</code>.</li>
<li>Helper <code>canMake(day)</code>:
  <ul>
    <li>Iterate through <code>bloomDay</code>: if <code>b &lt;= day</code>, increment consecutive count. If consecutive == <code>k</code>, bouquet count += 1, reset consecutive = 0.</li>
    <li>If <code>b &gt; day</code>, reset consecutive = 0.</li>
    <li>Return <code>bouquets &gt;= m</code>.</li>
  </ul>
</li>
<li>While <code>left &lt; right</code>: if <code>canMake(mid)</code>: <code>right = mid</code>; else <code>left = mid + 1</code>.</li>
<li>Return <code>left</code>.</li>
</ol>

<h2>🎞️ Visual dry run — bloomDay = [1, 10, 3, 10, 2], m = 3, k = 1</h2>
<pre class="viz">m * k = 3 <= 5.
Range: [1, 10]
Iter 1: mid = 5 → bloomed: [1(T), 10(F), 3(T), 10(F), 2(T)] → 3 flowers >= 3 bouquets!
        right = mid = 5
Iter 2: left = 1, right = 5 → mid = 3 → bloomed: [T, F, T, F, T] → 3 bouquets!
        right = mid = 3
Iter 3: left = 1, right = 3 → mid = 2 → bloomed: [T, F, F, F, T] → 2 bouquets < 3!
        left = mid + 1 = 3
left == right == 3. Return 3 days! ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def minDays(bloomDay, m, k):
    if m * k > len(bloomDay):
        return -1
        
    def canMake(days):
        bouquets = 0
        flowers = 0
        for b in bloomDay:
            if b <= days:
                flowers += 1
                if flowers == k:
                    bouquets += 1
                    flowers = 0
            else:
                flowers = 0
        return bouquets >= m
        
    left, right = min(bloomDay), max(bloomDay)
    while left < right:
        mid = left + (right - left) // 2
        if canMake(mid):
            right = mid
        else:
            left = mid + 1
            
    return left</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n * log(max(bloomDay) - min(bloomDay)))</strong>. <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li><code>m * k > n</code>: impossible, return -1.</li>
<li><code>k = 1</code>: any bloomed flower forms a bouquet independently.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Magnetic Force Between Two Balls ([[1552]]).</li>
</ul>''',

# ============================================================ LC 1552
1552: '''<h2>🧭 How to think about it</h2>
<p>In the universe, there are <code>n</code> baskets at positions <code>position[i]</code>. We distribute <code>m</code> balls into the baskets such that the <strong>minimum magnetic force between any two balls is maximized</strong>. The magnetic force between two balls at <code>x</code> and <code>y</code> is <code>|x - y|</code>.</p>

<h2>🐢 Brute force first</h2>
<p>Generate all combinations of choosing <code>m</code> baskets from <code>n</code> baskets, find minimum distance for each, take the maximum. Combinatorial explosion O(C(n, m)).</p>

<div class="insight">💡 <strong>Key insight:</strong> Maximize the minimum! This is the signature pattern for <strong>Binary Search on Answer</strong>. If we can place <code>m</code> balls such that all pairwise distances are <code>>= D</code>, then we can also place them with any distance <code>< D</code>. Sort positions first, then greedily place the next ball at the first basket with distance <code>>= D</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Sort <code>position</code> array.</li>
<li>Range for answer: <code>left = 1</code> (minimum possible force), <code>right = position[-1] - position[0]</code> (maximum possible force).</li>
<li>Helper <code>canPlace(force)</code>:
  <ul>
    <li>Place 1st ball at <code>position[0]</code>.</li>
    <li>For subsequent baskets, if <code>position[i] - last_pos >= force</code>, place ball here, update <code>last_pos = position[i]</code>, count += 1.</li>
    <li>Return <code>count >= m</code>.</li>
  </ul>
</li>
<li>Binary search to find MAXIMUM feasible force:
  <ul>
    <li>If <code>canPlace(mid)</code>: <code>ans = mid, left = mid + 1</code> (try larger force!).</li>
    <li>Else: <code>right = mid - 1</code>.</li>
  </ul>
</li>
<li>Return <code>ans</code>.</li>
</ol>

<h2>🎞️ Visual dry run — position = [1, 2, 3, 4, 7], m = 3</h2>
<pre class="viz">Sorted: [1, 2, 3, 4, 7]
left = 1, right = 7 - 1 = 6
Iter 1: mid = 3
  Place ball 1 at 1. Next >= 1 + 3 = 4 (basket 4). Next >= 4 + 3 = 7 (basket 7).
  Placed 3 balls! Feasible. ans = 3, left = 4
Iter 2: left = 4, right = 6 → mid = 5
  Place at 1. Next >= 1 + 5 = 6 (basket 7). Placed 2 balls < 3. Infeasible!
  right = 4
Iter 3: left = 4, right = 4 → mid = 4
  Place at 1. Next >= 5 (basket 7). Placed 2 balls. Infeasible!
  right = 3
left (4) > right (3). Loop ends.
Return ans = 3! ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def maxDistance(position, m):
    position.sort()
    
    def canPlace(force):
        count = 1
        last_pos = position[0]
        for p in position[1:]:
            if p - last_pos >= force:
                count += 1
                last_pos = p
                if count == m:
                    return True
        return False
        
    left, right = 1, position[-1] - position[0]
    ans = 1
    
    while left <= right:
        mid = left + (right - left) // 2
        if canPlace(mid):
            ans = mid
            left = mid + 1   # Try for larger distance
        else:
            right = mid - 1
            
    return ans</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n log n + n * log(max_dist))</strong> — Sorting takes O(n log n); each greedy check takes O(n). <strong>Space O(1)</strong> (in-place sort).</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li><code>m = 2</code>: simply place at <code>position[0]</code> and <code>position[-1]</code>, answer is <code>position[-1] - position[0]</code>.</li>
<li>Consecutive positions <code>[1, 2, 3, 4, 5]</code>: handled smoothly.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Aggressive Cows (SPOJ classic).</li>
<li>Minimize Max Distance to Gas Station ([[774]]).</li>
</ul>''',

# ============================================================ LC 1760
1760: '''<h2>🧭 How to think about it</h2>
<p>You are given an integer array <code>nums</code> where <code>nums[i]</code> represents the number of balls in the <code>i-th</code> bag. You are also given an integer <code>maxOperations</code>. In one operation, you can take any bag and divide its balls into two new bags of positive sizes. Your penalty is the maximum number of balls in a bag. Return the <strong>minimum possible penalty</strong> after at most <code>maxOperations</code>.</p>

<h2>🐢 Brute force first</h2>
<p>Always split the largest bag using a max-heap: greedy split into two equal halves doesn't always yield the optimal penalty for future splits. Binary search on penalty is exact!</p>

<div class="insight">💡 <strong>Key insight:</strong> Can we achieve a maximum bag size of <code>P</code> (penalty)? For a bag of size <code>x</code>, to ensure no piece exceeds <code>P</code>, we must divide it into <code>ceil(x / P)</code> pieces, requiring <code>ceil(x / P) - 1 = (x - 1) // P</code> operations! If the sum of operations across all bags is &lt;= <code>maxOperations</code>, penalty <code>P</code> is feasible.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>left = 1</code> (minimum possible penalty), <code>right = max(nums)</code>.</li>
<li>Helper <code>canAchieve(P)</code>: calculate operations: <code>sum((x - 1) // P for x in nums) &lt;= maxOperations</code>.</li>
<li>While <code>left &lt; right</code>:</li>
<li><code>mid = left + (right - left) // 2</code>.</li>
<li>If <code>canAchieve(mid)</code>: <code>right = mid</code> (try smaller penalty).</li>
<li>Else: <code>left = mid + 1</code>.</li>
<li>Return <code>left</code>.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [9], maxOperations = 2</h2>
<pre class="viz">Range: [1, 9]
Iter 1: mid = 5 → (9 - 1) // 5 = 1 operation <= 2 → right = 5 (bag split into [5, 4])
Iter 2: left = 1, right = 5 → mid = 3 → (9 - 1) // 3 = 2 operations <= 2 → right = 3 (split into [3, 3, 3])
Iter 3: left = 1, right = 3 → mid = 2 → (9 - 1) // 2 = 4 operations > 2 → left = 3
left == right == 3. Penalty = 3! ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def minimumSize(nums, maxOperations):
    left, right = 1, max(nums)
    
    while left < right:
        mid = left + (right - left) // 2
        ops = sum((x - 1) // mid for x in nums)
        
        if ops <= maxOperations:
            right = mid
        else:
            left = mid + 1
            
    return left</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n * log(max(nums)))</strong>. <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li><code>maxOperations</code> very large: penalty can reach 1.</li>
<li>All numbers already small.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Koko Eating Bananas ([[875]]).</li>
<li>Maximum Candies Allocated to K Children ([[2226]]).</li>
</ul>''',

# ============================================================ LC 2064
2064: '''<h2>🧭 How to think about it</h2>
<p>You are given an integer <code>n</code> denoting the number of specialty retail stores, and an integer array <code>quantities</code> where <code>quantities[i]</code> represents the amount of the <code>i-th</code> product type. Distribute all products to stores such that each store receives at most one product type, but any amount of it. Minimize the maximum number of products given to any store.</p>

<h2>🐢 Brute force first</h2>
<p>Linear search through possible max store quantities from 1 to <code>max(quantities)</code>. O(n * max(quantities)) TLE.</p>

<div class="insight">💡 <strong>Key insight:</strong> If each store receives at most <code>x</code> items, product <code>quantities[i]</code> needs <code>ceil(quantities[i] / x)</code> stores. If the sum of required stores &lt;= <code>n</code>, distribution <code>x</code> is feasible! Binary search on <code>x in [1, max(quantities)]</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>left = 1, right = max(quantities)</code>.</li>
<li>While <code>left &lt; right</code>:</li>
<li><code>mid = left + (right - left) // 2</code>.</li>
<li>Stores needed: <code>sum((q + mid - 1) // mid for q in quantities)</code>.</li>
<li>If <code>stores &lt;= n</code>: <code>right = mid</code>.</li>
<li>Else: <code>left = mid + 1</code>.</li>
<li>Return <code>left</code>.</li>
</ol>

<h2>🎞️ Visual dry run — n = 6, quantities = [11, 6]</h2>
<pre class="viz">Range: [1, 11]
Iter 1: mid = 6 → stores = ceil(11/6) + ceil(6/6) = 2 + 1 = 3 <= 6 → right = 6
Iter 2: left = 1, right = 6 → mid = 3 → stores = ceil(11/3) + ceil(6/3) = 4 + 2 = 6 <= 6 → right = 3
Iter 3: left = 1, right = 3 → mid = 2 → stores = ceil(11/2) + ceil(6/2) = 6 + 3 = 9 > 6 → left = 3
left == right == 3. Return 3! ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def minimizedMaximum(n, quantities):
    left, right = 1, max(quantities)
    
    while left < right:
        mid = left + (right - left) // 2
        stores = sum((q + mid - 1) // mid for q in quantities)
        
        if stores <= n:
            right = mid
        else:
            left = mid + 1
            
    return left</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(m * log(max(quantities)))</strong> where <code>m = len(quantities)</code>. <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li><code>n == len(quantities)</code>: each store gets exactly one product type, answer is <code>max(quantities)</code>.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Koko Eating Bananas ([[875]]).</li>
</ul>''',

# ============================================================ LC 2226
2226: '''<h2>🧭 How to think about it</h2>
<p>You are given an integer array <code>candies</code> where each element is the number of candies in a pile. You are also given an integer <code>k</code>. You can divide each pile into any number of sub-piles, but you <strong>cannot merge two piles together</strong>. You want to allocate candies to <code>k</code> children such that each child gets the same number of candies. Find the <strong>maximum number of candies</strong> each child can get.</p>

<h2>🐢 Brute force first</h2>
<p>Total sum of candies must be &gt;= <code>k</code>, otherwise answer is 0. Try candy amounts <code>c = 1, 2, ... max(candies)</code>. For each <code>c</code>, count children satisfied: <code>sum(candy // c)</code>. Stop when count &lt; <code>k</code>.</p>

<div class="insight">💡 <strong>Key insight:</strong> Maximize candies per child! Monotonic feasibility: if each child can get <code>c</code> candies, they can also get any amount <code>< c</code>. Binary search in range <code>[1, max(candies)]</code>. Notice we want the MAXIMUM feasible value!</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>If <code>sum(candies) &lt; k</code>, return <code>0</code>.</li>
<li><code>left = 1, right = max(candies)</code>. <code>ans = 0</code>.</li>
<li>While <code>left &lt;= right</code>:</li>
<li><code>mid = left + (right - left) // 2</code>.</li>
<li>Children served: <code>sum(c // mid for c in candies)</code>.</li>
<li>If <code>served &gt;= k</code>: this amount is possible! Record <code>ans = mid</code>, search for larger: <code>left = mid + 1</code>.</li>
<li>Else: <code>right = mid - 1</code>.</li>
<li>Return <code>ans</code>.</li>
</ol>

<h2>🎞️ Visual dry run — candies = [5, 8, 6], k = 3</h2>
<pre class="viz">Total sum = 19 >= 3. Range [1, 8]
Iter 1: mid = 4 → served = 5//4 + 8//4 + 6//4 = 1 + 2 + 1 = 4 >= 3 → ans = 4, left = 5
Iter 2: left = 5, right = 8 → mid = 6 → served = 5//6 + 8//6 + 6//6 = 0 + 1 + 1 = 2 < 3 → right = 5
Iter 3: left = 5, right = 5 → mid = 5 → served = 1 + 1 + 1 = 3 >= 3 → ans = 5, left = 6
left > right. Return ans = 5! ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def maximumCandies(candies, k):
    left, right = 1, max(candies)
    ans = 0
    
    while left <= right:
        mid = left + (right - left) // 2
        children = sum(c // mid for c in candies)
        
        if children >= k:
            ans = mid
            left = mid + 1   # Try for even more candies
        else:
            right = mid - 1
            
    return ans</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n * log(max(candies)))</strong>. <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li><code>sum(candies) < k</code>: returns 0.</li>
<li><code>k = 1</code>: returns <code>max(candies)</code>.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Magnetic Force Between Two Balls ([[1552]]).</li>
</ul>''',

# ============================================================ LC 410
410: '''<h2>🧭 How to think about it</h2>
<p>Given an integer array <code>nums</code> and an integer <code>k</code>, split <code>nums</code> into <code>k</code> non-empty subarrays such that the <strong>largest sum of any subarray is minimized</strong>. Return the minimized largest sum of the split.</p>

<h2>🐢 Brute force first</h2>
<p>Dynamic programming: <code>dp[i][j]</code> = minimum largest sum splitting first <code>i</code> elements into <code>j</code> subarrays. Transitions take O(n^2 * k). Binary search reduces this to O(n log(sum)).</p>

<div class="insight">💡 <strong>Key insight:</strong> The answer must lie between <code>max(nums)</code> (each element in its own subarray) and <code>sum(nums)</code> (the whole array in 1 subarray). For any candidate max subarray sum <code>S</code>, we can greedily check if we can partition <code>nums</code> into &lt;= <code>k</code> subarrays where no subarray exceeds <code>S</code>!</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>left = max(nums), right = sum(nums)</code>.</li>
<li>Helper <code>canSplit(targetSum)</code>:
  <ul>
    <li>Iterate through <code>nums</code>: add to <code>current_sum</code>.</li>
    <li>If <code>current_sum + num > targetSum</code>: start new subarray, count += 1, <code>current_sum = num</code>.</li>
    <li>Return <code>count <= k</code>.</li>
  </ul>
</li>
<li>While <code>left < right</code>: if <code>canSplit(mid)</code>: <code>right = mid</code>; else <code>left = mid + 1</code>.</li>
<li>Return <code>left</code>.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [7, 2, 5, 10, 8], k = 2</h2>
<pre class="viz">left = 10, right = 32
Iter 1: mid = 21 → [7, 2, 5] (sum 14), [10, 8] (sum 18) → 2 subarrays <= 2 → right = 21
Iter 2: left = 10, right = 21 → mid = 15 → [7, 2, 5] (14), [10] (10), [8] (8) → 3 subarrays > 2 → left = 16
Iter 3: left = 16, right = 21 → mid = 18 → [7, 2, 5] (14), [10, 8] (18) → 2 subarrays <= 2 → right = 18
Iter 4: left = 16, right = 18 → mid = 17 → [7, 2, 5] (14), [10] (10), [8] (8) → 3 subarrays > 2 → left = 18
left == right == 18. Return 18! ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def splitArray(nums, k):
    def canSplit(max_sum):
        subarrays = 1
        current_sum = 0
        for num in nums:
            if current_sum + num > max_sum:
                subarrays += 1
                current_sum = num
            else:
                current_sum += num
        return subarrays <= k

    left, right = max(nums), sum(nums)
    while left < right:
        mid = left + (right - left) // 2
        if canSplit(mid):
            right = mid
        else:
            left = mid + 1
            
    return left</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n * log(sum(nums) - max(nums)))</strong>. <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li><code>k == len(nums)</code>: returns <code>max(nums)</code>.</li>
<li><code>k == 1</code>: returns <code>sum(nums)</code>.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Capacity To Ship Packages Within D Days ([[1011]]) — identical logic!</li>
<li>Painter's Partition Problem.</li>
</ul>''',

# ============================================================ LC 719
719: '''<h2>🧭 How to think about it</h2>
<p>The distance of a pair of integers <code>(a, b)</code> is defined as the absolute difference <code>|a - b|</code>. Given an integer array <code>nums</code> and an integer <code>k</code>, return the <code>k-th</code> smallest distance among all the pairs. The number of pairs is <code>n * (n - 1) // 2</code>.</p>

<h2>🐢 Brute force first</h2>
<p>Calculate all pair differences, put in a list or heap, and find the k-th smallest. O(n^2 log n) space and time. For <code>n = 10,000</code>, pair count is ~50 million → Memory Limit Exceeded.</p>

<div class="insight">💡 <strong>Key insight:</strong> The pair distance must fall in range <code>[0, max(nums) - min(nums)]</code>. If we sort <code>nums</code>, for any distance <code>D</code>, we can count how many pairs have difference <code><= D</code> in <strong>O(n)</strong> using a sliding window two-pointer! Binary search on the distance <code>D</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Sort <code>nums</code> ascending.</li>
<li><code>left = 0, right = nums[-1] - nums[0]</code>.</li>
<li>Helper <code>countPairs(dist)</code>:
  <ul>
    <li>Use two pointers <code>i</code> and <code>j</code>: for each <code>right_idx</code>, advance <code>left_idx</code> until <code>nums[right_idx] - nums[left_idx] &lt;= dist</code>.</li>
    <li>Number of valid pairs ending at <code>right_idx</code> is <code>right_idx - left_idx</code>.</li>
    <li>Return total pairs.</li>
  </ul>
</li>
<li>While <code>left &lt; right</code>: if <code>countPairs(mid) &gt;= k</code>: <code>right = mid</code>; else <code>left = mid + 1</code>.</li>
<li>Return <code>left</code>.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [1, 3, 1], k = 1</h2>
<pre class="viz">Sorted: [1, 1, 3]
Pairs: (1, 1) diff 0, (1, 3) diff 2, (1, 3) diff 2.
Range: [0, 2]
Iter 1: mid = 1
  Pairs with diff <= 1:
  right_idx = 1: nums[1]-nums[0] = 0 <= 1 → 1 pair (1,1)
  right_idx = 2: nums[2]-nums[0] = 2 > 1 → left_idx moves to 2 → 0 pairs
  Total = 1 >= k(1) → right = 1
Iter 2: left = 0, right = 1 → mid = 0
  Pairs with diff <= 0: (1,1) → 1 pair >= 1 → right = 0
left == right == 0.
Return 0! ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def smallestDistancePair(nums, k):
    nums.sort()
    
    def countPairsWithDistanceLessThanOrEqual(dist):
        count = 0
        left_idx = 0
        for right_idx in range(len(nums)):
            while nums[right_idx] - nums[left_idx] > dist:
                left_idx += 1
            count += right_idx - left_idx
        return count

    left, right = 0, nums[-1] - nums[0]
    
    while left < right:
        mid = left + (right - left) // 2
        if countPairsWithDistanceLessThanOrEqual(mid) >= k:
            right = mid
        else:
            left = mid + 1
            
    return left</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n log n + n * log(max_val - min_val))</strong> — Sorting takes O(n log n). Each binary search step runs two pointers in O(n). <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>All elements identical: distances are all 0, returns 0.</li>
<li><code>k = 1</code>: returns smallest adjacent difference.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Kth Smallest Element in a Sorted Matrix ([[378]]).</li>
<li>Median of Two Sorted Arrays ([[4]]).</li>
</ul>''',

# ============================================================ LC 774
774: '''<h2>🧭 How to think about it</h2>
<p>You are given an integer array <code>stations</code> that represents the positions of gas stations on the x-axis in sorted order. You are also given an integer <code>k</code>. You should add <code>k</code> new gas stations such that the maximum distance between adjacent gas stations is minimized. Return the smallest possible value of <code>D</code> (answer within <code>10^-6</code> of actual value).</p>

<h2>🐢 Brute force first</h2>
<p>Greedily place one station at a time into the currently largest interval using a max heap: O(k log n). When <code>k = 10^6</code>, heap operations timeout. Continuous binary search handles any <code>k</code>!</p>

<div class="insight">💡 <strong>Key insight:</strong> Can we achieve adjacent distance at most <code>D</code>? For an interval of length <code>diff = stations[i+1] - stations[i]</code>, we need <code>floor(diff / D)</code> additional stations! If the sum of stations needed &lt;= <code>k</code>, then <code>D</code> is achievable! Use floating-point binary search.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Floating binary search: <code>left = 0.0, right = stations[-1] - stations[0]</code>.</li>
<li>Loop while <code>right - left > 1e-6</code> (or fixed 60 iterations):</li>
<li><code>mid = (left + right) / 2.0</code>.</li>
<li>Count stations needed: <code>sum(int((stations[i+1] - stations[i]) / mid) for i in range(len(stations)-1))</code>.</li>
<li>If <code>count <= k</code>: <code>right = mid</code> (can achieve this max distance, try smaller).</li>
<li>Else: <code>left = mid</code>.</li>
<li>Return <code>left</code>.</li>
</ol>

<h2>🎞️ Visual dry run — stations = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], k = 9</h2>
<pre class="viz">Initial gaps: all 1.
With 9 stations added across 9 intervals, each interval splits in half:
Gap becomes 0.5!
Binary search converges smoothly to 0.500000. ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def minmaxGasDist(stations, k):
    left, right = 0.0, float(stations[-1] - stations[0])
    
    # 60 iterations gives precision (right - left) / 2^60 < 10^-10
    for _ in range(60):
        mid = (left + right) / 2.0
        needed = sum(int((stations[i+1] - stations[i]) / mid) for i in range(len(stations) - 1))
        
        if needed <= k:
            right = mid
        else:
            left = mid
            
    return left</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n * log((max_gap) / eps))</strong> ≈ 60 * O(n). <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Stations with uneven initial spacings.</li>
<li>Floating-point termination: running a fixed 60 or 70 iterations completely avoids infinite loops from precision loss.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Koko Eating Bananas ([[875]]).</li>
</ul>''',

# ============================================================ LC 34
34: '''<h2>🧭 How to think about it</h2>
<p>Given an array of integers <code>nums</code> sorted in non-decreasing order, find the starting and ending position of a given <code>target</code> value. If <code>target</code> is not found in the array, return <code>[-1, -1]</code>. You must write an algorithm with <strong>O(log n)</strong> runtime complexity.</p>

<h2>🐢 Brute force first</h2>
<p>Linear scan finding the first index where <code>nums[i] == target</code> and last index. O(n) runtime.</p>

<div class="insight">💡 <strong>Key insight:</strong> Standard binary search stops at *any* match. Here we need two specialized binary searches:
1. <strong>First Occurrence (Lower Bound):</strong> When <code>nums[mid] == target</code>, don't stop! Keep searching to the left: <code>right = mid - 1</code>.
2. <strong>Last Occurrence (Upper Bound):</strong> When <code>nums[mid] == target</code>, keep searching to the right: <code>left = mid + 1</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Helper <code>findBound(isFirst)</code>:
  <ul>
    <li><code>left = 0, right = len(nums) - 1, bound = -1</code>.</li>
    <li>While <code>left &lt;= right</code>:</li>
    <li><code>mid = left + (right - left) // 2</code>.</li>
    <li>If <code>nums[mid] == target</code>: <code>bound = mid</code>. If <code>isFirst</code>: <code>right = mid - 1</code>; else: <code>left = mid + 1</code>.</li>
    <li>Elif <code>nums[mid] &lt; target</code>: <code>left = mid + 1</code>.</li>
    <li>Else: <code>right = mid - 1</code>.</li>
  </ul>
</li>
<li>Return <code>[findBound(True), findBound(False)]</code>.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [5, 7, 7, 8, 8, 10], target = 8</h2>
<pre class="viz">1. Finding First (leftmost 8):
   left = 0, right = 5 → mid = 2, nums[2]=7 < 8 → left = 3
   left = 3, right = 5 → mid = 4, nums[4]=8 == 8 → bound = 4, right = 3
   left = 3, right = 3 → mid = 3, nums[3]=8 == 8 → bound = 3, right = 2
   left > right. First = 3.

2. Finding Last (rightmost 8):
   left = 0, right = 5 → mid = 2, nums[2]=7 < 8 → left = 3
   left = 3, right = 5 → mid = 4, nums[4]=8 == 8 → bound = 4, left = 5
   left = 5, right = 5 → mid = 5, nums[5]=10 > 8 → right = 4
   left > right. Last = 4.

Result: [3, 4] ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def searchRange(nums, target):
    def findBound(is_first):
        left, right = 0, len(nums) - 1
        bound = -1
        
        while left <= right:
            mid = left + (right - left) // 2
            
            if nums[mid] == target:
                bound = mid
                if is_first:
                    right = mid - 1  # keep searching left
                else:
                    left = mid + 1   # keep searching right
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
                
        return bound
        
    first = findBound(True)
    if first == -1:
        return [-1, -1]
    last = findBound(False)
    return [first, last]</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(log n)</strong> — Two binary searches of size n. <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Target not in array: returns <code>[-1, -1]</code>.</li>
<li>Array empty: returns <code>[-1, -1]</code>.</li>
<li>All elements equal target: returns <code>[0, n - 1]</code>.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Search Insert Position ([[35]]).</li>
<li>Count Occurrences of a Number in Sorted Array.</li>
</ul>''',

# ============================================================ LC 4
4: '''<h2>🧭 How to think about it</h2>
<p>Given two sorted arrays <code>nums1</code> and <code>nums2</code> of size <code>m</code> and <code>n</code> respectively, return the <strong>median</strong> of the two sorted arrays. The overall run time complexity should be <strong>O(log(m + n))</strong>.</p>

<h2>🐢 Brute force first</h2>
<p>Merge both arrays using two pointers into an array of size <code>m + n</code>, then pick the middle element. Time: O(m + n), Space: O(m + n). Violates the logarithmic constraint.</p>

<div class="insight">💡 <strong>Key insight:</strong> Partition both arrays simultaneously! A median partitions a combined set of <code>m + n</code> elements into two equal halves (left half and right half) where <strong>every element in the left half <= every element in the right half</strong>! If we take <code>i</code> elements from <code>nums1</code>, we must take <code>j = (m + n + 1) // 2 - i</code> elements from <code>nums2</code>. Binary search <code>i</code> on the <strong>shorter array</strong>!</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Ensure <code>nums1</code> is the shorter array (if not, swap <code>nums1, nums2</code>). This guarantees <code>O(log(min(m, n)))</code>.</li>
<li>Set <code>left = 0, right = m</code> (number of elements to take from <code>nums1</code> into left partition).</li>
<li>While <code>left &lt;= right</code>:</li>
<li><code>i = left + (right - left) // 2</code>.</li>
<li><code>j = (m + n + 1) // 2 - i</code>.</li>
<li>Border values:
  <ul>
    <li><code>maxLeft1 = nums1[i-1]</code> if <code>i > 0</code> else <code>-inf</code></li>
    <li><code>minRight1 = nums1[i]</code> if <code>i < m</code> else <code>+inf</code></li>
    <li><code>maxLeft2 = nums2[j-1]</code> if <code>j > 0</code> else <code>-inf</code></li>
    <li><code>minRight2 = nums2[j]</code> if <code>j < n</code> else <code>+inf</code></li>
  </ul>
</li>
<li>Check partition validity:
  <ul>
    <li>If <code>maxLeft1 <= minRight2</code> and <code>maxLeft2 <= minRight1</code>: Perfect partition!
      <ul>
        <li>If <code>(m + n) % 2 == 1</code>: return <code>max(maxLeft1, maxLeft2)</code>.</li>
        <li>Else: return <code>(max(maxLeft1, maxLeft2) + min(minRight1, minRight2)) / 2.0</code>.</li>
      </ul>
    </li>
    <li>If <code>maxLeft1 > minRight2</code>: too many elements from <code>nums1</code>, shift left: <code>right = i - 1</code>.</li>
    <li>Else: too few elements from <code>nums1</code>, shift right: <code>left = i + 1</code>.</li>
  </ul>
</li>
</ol>

<h2>🎞️ Visual dry run — nums1 = [1, 3], nums2 = [2]</h2>
<pre class="viz">m = 2, n = 1. Swap so nums1 = [2] (len 1), nums2 = [1, 3] (len 2).
Half size = (1 + 2 + 1) // 2 = 2.
left = 0, right = 1.
Iter 1: i = 0 → j = 2 - 0 = 2
  nums1 left: [], right: [2] → maxLeft1 = -inf, minRight1 = 2
  nums2 left: [1, 3], right: [] → maxLeft2 = 3, minRight2 = +inf
  Check: maxLeft2 (3) <= minRight1 (2)? NO! (3 > 2)
  nums1 took too few elements → left = i + 1 = 1

Iter 2: i = 1 → j = 2 - 1 = 1
  nums1 left: [2], right: [] → maxLeft1 = 2, minRight1 = +inf
  nums2 left: [1], right: [3] → maxLeft2 = 1, minRight2 = 3
  Check: maxLeft1 (2) <= minRight2 (3) AND maxLeft2 (1) <= minRight1 (+inf) → VALID!
  Total len = 3 (odd).
  Median = max(maxLeft1, maxLeft2) = max(2, 1) = 2.0. ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def findMedianSortedArrays(nums1, nums2):
    # Ensure nums1 is shorter to guarantee log(min(m, n))
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
        
    m, n = len(nums1), len(nums2)
    left, right = 0, m
    total_left = (m + n + 1) // 2
    
    while left <= right:
        i = left + (right - left) // 2
        j = total_left - i
        
        max_left1 = float('-inf') if i == 0 else nums1[i - 1]
        min_right1 = float('inf') if i == m else nums1[i]
        
        max_left2 = float('-inf') if j == 0 else nums2[j - 1]
        min_right2 = float('inf') if j == n else nums2[j]
        
        if max_left1 <= min_right2 and max_left2 <= min_right1:
            # Correct partition found
            if (m + n) % 2 == 1:
                return float(max(max_left1, max_left2))
            else:
                return (max(max_left1, max_left2) + min(min_right1, min_right2)) / 2.0
        elif max_left1 > min_right2:
            right = i - 1
        else:
            left = i + 1
            
    return 0.0</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(log(min(m, n)))</strong> — Binary search on the shorter array. <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>One array is empty: handled smoothly by <code>-inf</code> and <code>+inf</code> sentinels.</li>
<li>Arrays of different lengths (e.g. m=1, n=1000).</li>
<li>Combined length odd vs even.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Kth Element of Two Sorted Arrays.</li>
<li>Find K-th Smallest Pair Distance ([[719]]).</li>
</ul>''',


# ============================================================ LC 658 — Find K Closest Elements
658: '''<h2>🧭 How to think about it</h2>
<p>Given a sorted integer array <code>arr</code>, two integers <code>k</code> and <code>x</code>, return the <code>k</code> closest integers to <code>x</code> in the array. An integer <code>a</code> is closer to <code>x</code> than <code>b</code> if <code>|a - x| < |b - x|</code>, or <code>|a - x| == |b - x|</code> and <code>a < b</code>.</p>

<h2>🐢 Brute force first</h2>
<p>Sort the entire array by distance <code>abs(num - x)</code> and take first <code>k</code>, then sort those <code>k</code> elements. Time: O(n log n). Space: O(k).</p>

<div class="insight">💡 <strong>Key insight:</strong> The result is always a <strong>contiguous subarray of length k</strong> because the input array is already sorted! We simply need to find the optimal <strong>starting index</strong> <code>left</code> in range <code>[0, len(arr) - k]</code>. For any candidate start <code>mid</code>, compare the distance of element <code>arr[mid]</code> vs element <code>arr[mid + k]</code>: if <code>x - arr[mid] > arr[mid + k] - x</code>, <code>arr[mid + k]</code> is closer to <code>x</code> than <code>arr[mid]</code>, so the window must shift right!</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Set binary search range for starting index: <code>left = 0, right = len(arr) - k</code>.</li>
<li>While <code>left &lt; right</code>:</li>
<li><code>mid = left + (right - left) // 2</code>.</li>
<li>Compare distance of boundary elements: if <code>x - arr[mid] > arr[mid + k] - x</code>, <code>arr[mid]</code> is farther from <code>x</code> than <code>arr[mid + k]</code>, so shift right: <code>left = mid + 1</code>.</li>
<li>Else: <code>right = mid</code>.</li>
<li>Return <code>arr[left : left + k]</code>.</li>
</ol>

<h2>🎞️ Visual dry run — arr = [1, 2, 3, 4, 5], k = 4, x = 3</h2>
<pre class="viz">n = 5, k = 4. Search range for left bound: [0, 1]
mid = 0: compare arr[0]=1 vs arr[0+4]=arr[4]=5
dist to x(3): |3 - 1| = 2 vs |5 - 3| = 2
Tie broken by smaller value (1 < 5) → arr[0] is preferred!
right = mid = 0.
left == right == 0.
Subarray is arr[0:4] = [1, 2, 3, 4]. ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def findClosestElements(arr, k, x):
    left, right = 0, len(arr) - k
    
    while left < right:
        mid = left + (right - left) // 2
        # If arr[mid] is further from x than arr[mid + k], shift window right
        if x - arr[mid] > arr[mid + k] - x:
            left = mid + 1
        else:
            right = mid
            
    return arr[left : left + k]</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(log(n - k) + k)</strong> — Binary search takes O(log(n - k)) to find start index; slicing takes O(k). <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li><code>x <= arr[0]</code>: returns first <code>k</code> elements.</li>
<li><code>x >= arr[-1]</code>: returns last <code>k</code> elements.</li>
<li><code>k == len(arr)</code>: returns entire array.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Find K-th Smallest Pair Distance ([[719]]).</li>
</ul>
''',
}

