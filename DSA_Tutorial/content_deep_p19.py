"""Deep tutorials for Pattern 19: Math, Number Theory & Geometry Patterns."""
DEEP = {}
DEEP[8] = """<h3>Problem Overview</h3>
<p>Implement the <code>myAtoi(string s)</code> function, which converts a string to a 32-bit signed integer. Must parse leading whitespace, handle optional sign <code>'+'</code> or <code>'-'</code>, read digits until a non-digit character, and clamp values to the 32-bit signed range <code>{2, 3, 5}</code>[-2^{31}, 2^{31} - 1]<code>{2, 3, 5}</code>.</p>

<h3>Key Insights</h3>
<p>State machine traversal:
<ol>
  <li>Skip leading spaces with index pointer.</li>
  <li>Check optional sign at current pointer.</li>
  <li>Accumulate digits: <code>val = val * 10 + digit</code>. Check for 32-bit overflow before multiplication.</li>
  <li>Clamp to <code>{2, 3, 5}</code>-2^{31} = -2147483648<code>{2, 3, 5}</code> and <code>{2, 3, 5}</code>2^{31} - 1 = 2147483647<code>{2, 3, 5}</code>.</li>
</ol></p>

<details>
<summary><strong>Python 3 Solution (Deterministic Parsing)</strong></summary>
<div class="code-block">
<pre><code class="language-python">class Solution:
    def myAtoi(self, s: str) -> int:
        INT_MAX = 2**31 - 1
        INT_MIN = -2**31
        
        i, n = 0, len(s)
        while i < n and s[i] == ' ':
            i += 1
            
        if i == n:
            return 0
            
        sign = 1
        if s[i] == '+':
            i += 1
        elif s[i] == '-':
            sign = -1
            i += 1
            
        val = 0
        while i < n and s[i].isdigit():
            digit = ord(s[i]) - ord('0')
            val = val * 10 + digit
            if sign * val > INT_MAX:
                return INT_MAX
            if sign * val < INT_MIN:
                return INT_MIN
            i += 1
            
        return sign * val
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> <code>{2, 3, 5}</code>O(N)<code>{2, 3, 5}</code> single pass over characters.</li>
  <li><strong>Space Complexity:</strong> <code>{2, 3, 5}</code>O(1)<code>{2, 3, 5}</code>.</li>
  <li><strong>Edge Cases:</strong> Whitespace only, sign without digits (<code>"+"</code>), words preceding numbers (<code>"words and 987"</code> returns 0), numbers exceeding 64 bits.</li>
</ul>"""

DEEP[50] = """<h3>Problem Overview</h3>
<p>Implement <code>pow(x, n)</code>, which calculates <code>{2, 3, 5}</code>x<code>{2, 3, 5}</code> raised to the power <code>{2, 3, 5}</code>n<code>{2, 3, 5}</code> (<code>{2, 3, 5}</code>x^n<code>{2, 3, 5}</code>). Must handle negative exponents and large values of <code>{2, 3, 5}</code>n<code>{2, 3, 5}</code> efficiently without exceeding time limits.</p>

<h3>Key Insights</h3>
<p>A naive loop multiplying <code>{2, 3, 5}</code>x<code>{2, 3, 5}</code>, <code>{2, 3, 5}</code>n<code>{2, 3, 5}</code> times takes <code>{2, 3, 5}</code>O(n)<code>{2, 3, 5}</code> time, which will Time Out for <code>{2, 3, 5}</code>n = 2^{31} - 1 \\approx 2.14 \times 10^9<code>{2, 3, 5}</code>.</p>
<p>Instead, we use <strong>Binary Exponentiation (Fast Powering)</strong>:
<code>{2, 3, 5}</code><code>{2, 3, 5}</code>x^n = \\begin{cases} (x^2)^{n / 2} & \text{if } n \text{ is even} \\ x \\cdot (x^2)^{(n - 1) / 2} & \text{if } n \text{ is odd} \\end{cases}<code>{2, 3, 5}</code><code>{2, 3, 5}</code>
This cuts the exponent in half at each step, reducing time complexity to <code>{2, 3, 5}</code>O(\\log n)<code>{2, 3, 5}</code>.</p>

<details>
<summary><strong>Python 3 Solution (Iterative Binary Exponentiation)</strong></summary>
<div class="code-block">
<pre><code class="language-python">class Solution:
    def myPow(self, x: float, n: int) -> float:
        if n == 0:
            return 1.0
        if n < 0:
            x = 1.0 / x
            n = -n
            
        res = 1.0
        curr_power = x
        
        while n > 0:
            if n & 1:
                res *= curr_power
            curr_power *= curr_power
            n >>= 1
            
        return res
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> <code>{2, 3, 5}</code>O(\\log n)<code>{2, 3, 5}</code> because <code>{2, 3, 5}</code>n<code>{2, 3, 5}</code> is halved at every bit shift.</li>
  <li><strong>Space Complexity:</strong> <code>{2, 3, 5}</code>O(1)<code>{2, 3, 5}</code> iterative memory.</li>
  <li><strong>Edge Cases:</strong> <code>{2, 3, 5}</code>n = -2^{31}<code>{2, 3, 5}</code> (in 32-bit systems, taking <code>{2, 3, 5}</code>-n<code>{2, 3, 5}</code> overflows if not handled with 64-bit/Python arbitrary precision), <code>{2, 3, 5}</code>x = 0<code>{2, 3, 5}</code>, <code>{2, 3, 5}</code>n = 0<code>{2, 3, 5}</code>.</li>
</ul>"""

DEEP[62] = """<h3>Problem Overview</h3>
<p>A robot is located at the top-left corner of an <code>{2, 3, 5}</code>m \times n<code>{2, 3, 5}</code> grid. The robot can only move either down or right at any point. How many possible unique paths are there to reach the bottom-right corner?</p>

<h3>Key Insights</h3>
<p>To reach cell <code>{2, 3, 5}</code>(m-1, n-1)<code>{2, 3, 5}</code> from <code>{2, 3, 5}</code>(0, 0)<code>{2, 3, 5}</code>, the robot must make exactly:
<ul>
  <li><code>{2, 3, 5}</code>m - 1<code>{2, 3, 5}</code> steps Down</li>
  <li><code>{2, 3, 5}</code>n - 1<code>{2, 3, 5}</code> steps Right</li>
</ul>
Total steps = <code>{2, 3, 5}</code>(m - 1) + (n - 1) = m + n - 2<code>{2, 3, 5}</code>.
Any path is determined by choosing which <code>{2, 3, 5}</code>m - 1<code>{2, 3, 5}</code> steps are Down out of the total <code>{2, 3, 5}</code>m + n - 2<code>{2, 3, 5}</code> steps. This is a closed-form combinatorics formula:
<code>{2, 3, 5}</code><code>{2, 3, 5}</code>\\binom{m + n - 2}{m - 1} = \\frac{(m + n - 2)!}{(m - 1)! \\cdot (n - 1)!}<code>{2, 3, 5}</code><code>{2, 3, 5}</code></p>

<details>
<summary><strong>Python 3 Solution (Combinatorics - O(min(m, n)))</strong></summary>
<div class="code-block">
<pre><code class="language-python">import math

class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        # Combination: C(m + n - 2, min(m - 1, n - 1))
        return math.comb(m + n - 2, m - 1)
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> <code>{2, 3, 5}</code>O(\\min(m, n))<code>{2, 3, 5}</code> multiplicative steps.</li>
  <li><strong>Space Complexity:</strong> <code>{2, 3, 5}</code>O(1)<code>{2, 3, 5}</code>.</li>
  <li><strong>Edge Cases:</strong> <code>{2, 3, 5}</code>m = 1<code>{2, 3, 5}</code> or <code>{2, 3, 5}</code>n = 1<code>{2, 3, 5}</code> (returns 1).</li>
</ul>"""

DEEP[69] = """<h3>Problem Overview</h3>
<p>Given a non-negative integer <code>{2, 3, 5}</code>x<code>{2, 3, 5}</code>, compute and return the square root of <code>{2, 3, 5}</code>x<code>{2, 3, 5}</code> rounded down to the nearest integer. Do not use any built-in exponent functions or operators like <code>pow(x, 0.5)</code> or <code>x ** 0.5</code>.</p>

<h3>Key Insights</h3>
<p>For <code>{2, 3, 5}</code>x \\ge 1<code>{2, 3, 5}</code>, <code>{2, 3, 5}</code>\\lfloor \\sqrt{x} \rfloor<code>{2, 3, 5}</code> is an integer in the range <code>{2, 3, 5}</code>[1, x // 2 + 1]<code>{2, 3, 5}</code>. Because the sequence <code>{2, 3, 5}</code>1^2, 2^2, 3^2, \\dots<code>{2, 3, 5}</code> is monotonically increasing, we can use <strong>Binary Search</strong> to find the largest integer <code>{2, 3, 5}</code>m<code>{2, 3, 5}</code> such that <code>{2, 3, 5}</code>m^2 \\le x<code>{2, 3, 5}</code>.</p>

<details>
<summary><strong>Python 3 Solution (Binary Search)</strong></summary>
<div class="code-block">
<pre><code class="language-python">class Solution:
    def mySqrt(self, x: int) -> int:
        if x < 2:
            return x
        
        left, right = 1, x // 2
        ans = 1
        
        while left <= right:
            mid = (left + right) // 2
            sq = mid * mid
            if sq == x:
                return mid
            elif sq < x:
                ans = mid  # mid is a valid candidate
                left = mid + 1
            else:
                right = mid - 1
                
        return ans
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> <code>{2, 3, 5}</code>O(\\log x)<code>{2, 3, 5}</code> operations.</li>
  <li><strong>Space Complexity:</strong> <code>{2, 3, 5}</code>O(1)<code>{2, 3, 5}</code>.</li>
  <li><strong>Edge Cases:</strong> <code>{2, 3, 5}</code>x = 0<code>{2, 3, 5}</code> (returns 0), <code>{2, 3, 5}</code>x = 1<code>{2, 3, 5}</code> (returns 1), large values like <code>{2, 3, 5}</code>x = 2^{31} - 1<code>{2, 3, 5}</code>.</li>
</ul>"""

DEEP[118] = """<h3>Problem Overview</h3>
<p>Given an integer <code>numRows</code>, return the first <code>numRows</code> of Pascal's triangle, where each number is the sum of the two numbers directly above it.</p>

<h3>Key Insights</h3>
<p>Row <code>{2, 3, 5}</code>r<code>{2, 3, 5}</code> has <code>{2, 3, 5}</code>r + 1<code>{2, 3, 5}</code> elements. The first and last elements are always 1: <code>row[0] = row[-1] = 1</code>.
Every intermediate element satisfies:
<code>{2, 3, 5}</code><code>{2, 3, 5}</code>row[c] = prev_row[c - 1] + prev_row[c]<code>{2, 3, 5}</code><code>{2, 3, 5}</code></p>

<details>
<summary><strong>Python 3 Solution (Click to Expand)</strong></summary>
<div class="code-block">
<pre><code class="language-python">from typing import List

class Solution:
    def generate(self, numRows: int) -> List[List[int]]:
        triangle = []
        for r in range(numRows):
            row = [1] * (r + 1)
            for c in range(1, r):
                row[c] = triangle[r - 1][c - 1] + triangle[r - 1][c]
            triangle.append(row)
        return triangle
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> <code>{2, 3, 5}</code>O(\text{numRows}^2)<code>{2, 3, 5}</code> total numbers computed.</li>
  <li><strong>Space Complexity:</strong> <code>{2, 3, 5}</code>O(\text{numRows}^2)<code>{2, 3, 5}</code> to store the output triangle.</li>
</ul>"""

DEEP[119] = """<h3>Problem Overview</h3>
<p>Given an integer <code>rowIndex</code>, return the <code>{2, 3, 5}</code>\text{rowIndex}^{\text{th}}<code>{2, 3, 5}</code> (0-indexed) row of Pascal's triangle using only <code>{2, 3, 5}</code>O(\text{rowIndex})<code>{2, 3, 5}</code> extra space.</p>

<h3>Key Insights</h3>
<p>Notice the relationship between adjacent elements in row <code>{2, 3, 5}</code>n<code>{2, 3, 5}</code>:
<code>{2, 3, 5}</code><code>{2, 3, 5}</code>\\binom{n}{k} = \\binom{n}{k - 1} \times \\frac{n - k + 1}{k}<code>{2, 3, 5}</code><code>{2, 3, 5}</code>
Starting from <code>{2, 3, 5}</code>row[0] = 1<code>{2, 3, 5}</code>, each subsequent element <code>{2, 3, 5}</code>k<code>{2, 3, 5}</code> can be computed from element <code>{2, 3, 5}</code>k - 1<code>{2, 3, 5}</code> in <code>{2, 3, 5}</code>O(1)<code>{2, 3, 5}</code> time and <code>{2, 3, 5}</code>O(1)<code>{2, 3, 5}</code> extra space!</p>

<details>
<summary><strong>Python 3 Solution (Linear Time O(k) Space)</strong></summary>
<div class="code-block">
<pre><code class="language-python">from typing import List

class Solution:
    def getRow(self, rowIndex: int) -> List[int]:
        row = [1] * (rowIndex + 1)
        for k in range(1, rowIndex):
            row[k] = row[k - 1] * (rowIndex - k + 1) // k
        return row
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> <code>{2, 3, 5}</code>O(k)<code>{2, 3, 5}</code> where <code>{2, 3, 5}</code>k = \text{rowIndex}<code>{2, 3, 5}</code>.</li>
  <li><strong>Space Complexity:</strong> <code>{2, 3, 5}</code>O(k)<code>{2, 3, 5}</code> for the output row.</li>
  <li><strong>Edge Cases:</strong> <code>{2, 3, 5}</code>\text{rowIndex} = 0<code>{2, 3, 5}</code> (returns <code>[1]</code>).</li>
</ul>"""

DEEP[149] = """<h3>Problem Overview</h3>
<p>Given an array of <code>points</code> where <code>points[i] = [xi, yi]</code> represents a point on the X-Y plane, return the maximum number of points that lie on the same straight line.</p>

<h3>Key Insights</h3>
<p>Two points <code>{2, 3, 5}</code>A<code>{2, 3, 5}</code> and <code>{2, 3, 5}</code>B<code>{2, 3, 5}</code> define a unique line slope: <code>{2, 3, 5}</code>\text{slope} = \\frac{y_2 - y_1}{x_2 - x_1}<code>{2, 3, 5}</code>.
Floating-point division suffers from precision errors. To maintain exactness, represent each slope as a reduced coprime pair <code>{2, 3, 5}</code>\\left(\\frac{\\Delta y}{\\gcd(\\Delta x, \\Delta y)}, \\frac{\\Delta x}{\\gcd(\\Delta x, \\Delta y)}\right)<code>{2, 3, 5}</code>.
For each point <code>{2, 3, 5}</code>i<code>{2, 3, 5}</code>, calculate the slope to every other point <code>{2, 3, 5}</code>j > i<code>{2, 3, 5}</code> and find the maximum frequency in a hash map.</p>

<details>
<summary><strong>Python 3 Solution (Exact Coprime Slope Hashing)</strong></summary>
<div class="code-block">
<pre><code class="language-python">from typing import List
from collections import defaultdict
import math

class Solution:
    def maxPoints(self, points: List[List[int]]) -> int:
        n = len(points)
        if n <= 2:
            return n
            
        max_pts = 1
        for i in range(n):
            slopes = defaultdict(int)
            x1, y1 = points[i]
            for j in range(i + 1, n):
                x2, y2 = points[j]
                dx = x2 - x1
                dy = y2 - y1
                g = math.gcd(dx, dy)
                dx //= g
                dy //= g
                # Ensure canonical orientation
                if dx < 0 or (dx == 0 and dy < 0):
                    dx, dy = -dx, -dy
                slopes[(dx, dy)] += 1
                
            if slopes:
                max_pts = max(max_pts, max(slopes.values()) + 1)
                
        return max_pts
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> <code>{2, 3, 5}</code>O(n^2)<code>{2, 3, 5}</code> pairs evaluated with <code>{2, 3, 5}</code>O(\\log(\\min(\\Delta x, \\Delta y)))<code>{2, 3, 5}</code> GCD calculations.</li>
  <li><strong>Space Complexity:</strong> <code>{2, 3, 5}</code>O(n)<code>{2, 3, 5}</code> hash map per outer point.</li>
  <li><strong>Edge Cases:</strong> Vertical lines (<code>{2, 3, 5}</code>dx = 0<code>{2, 3, 5}</code>), horizontal lines (<code>{2, 3, 5}</code>dy = 0<code>{2, 3, 5}</code>).</li>
</ul>"""

DEEP[168] = """<h3>Problem Overview</h3>
<p>Given an integer <code>columnNumber</code>, return its corresponding column title as it appears in an Excel sheet (1 -> A, 2 -> B, ..., 26 -> Z, 27 -> AA, 28 -> AB, ...).</p>

<h3>Key Insights</h3>
<p>This is a <strong>bijective base-26 numeral system</strong> without a 0 digit (digits range from 1 to 26 rather than 0 to 25). To adapt standard base conversion: decrement <code>columnNumber</code> by 1 at each iteration before taking modulo 26!</p>
<div class="code-block">
<pre><code>rem = (columnNumber - 1) % 26
char = chr(ord('A') + rem)
columnNumber = (columnNumber - 1) // 26</code></pre>
</div>

<details>
<summary><strong>Python 3 Solution (Click to Expand)</strong></summary>
<div class="code-block">
<pre><code class="language-python">class Solution:
    def convertToTitle(self, columnNumber: int) -> str:
        res = []
        while columnNumber > 0:
            columnNumber -= 1
            rem = columnNumber % 26
            res.append(chr(ord('A') + rem))
            columnNumber //= 26
        return "".join(reversed(res))
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> <code>{2, 3, 5}</code>O(\\log_{26}(\text{columnNumber}))<code>{2, 3, 5}</code>.</li>
  <li><strong>Space Complexity:</strong> <code>{2, 3, 5}</code>O(1)<code>{2, 3, 5}</code> auxiliary space.</li>
  <li><strong>Edge Cases:</strong> Exact multiples of 26 (e.g. 26 -> <code>"Z"</code>, 52 -> <code>"AZ"</code>, 702 -> <code>"ZZ"</code>).</li>
</ul>"""

DEEP[171] = """<h3>Problem Overview</h3>
<p>Given a string <code>columnTitle</code> that represents the column title as appears in an Excel sheet, return its corresponding column number (A -> 1, B -> 2, ..., Z -> 26, AA -> 27).</p>

<h3>Key Insights</h3>
<p>Polynomial evaluation in base 26: For a string <code>{2, 3, 5}</code>c_0 c_1 \\dots c_{k-1}<code>{2, 3, 5}</code>, each character contributes <code>{2, 3, 5}</code>(ord(c_i) - ord('A') + 1) \times 26^{k - 1 - i}<code>{2, 3, 5}</code>.
Accumulate from left to right: <code>res = res * 26 + (ord(ch) - ord('A') + 1)</code>.</p>

<details>
<summary><strong>Python 3 Solution (Click to Expand)</strong></summary>
<div class="code-block">
<pre><code class="language-python">class Solution:
    def titleToNumber(self, columnTitle: str) -> int:
        res = 0
        for ch in columnTitle:
            digit = ord(ch) - ord('A') + 1
            res = res * 26 + digit
        return res
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> <code>{2, 3, 5}</code>O(L)<code>{2, 3, 5}</code> where <code>{2, 3, 5}</code>L<code>{2, 3, 5}</code> is length of string (<code>{2, 3, 5}</code>L \\le 7<code>{2, 3, 5}</code>).</li>
  <li><strong>Space Complexity:</strong> <code>{2, 3, 5}</code>O(1)<code>{2, 3, 5}</code>.</li>
  <li><strong>Edge Cases:</strong> Single character <code>"A"</code> (1), multi-character <code>"FXSHRXW"</code> (<code>{2, 3, 5}</code>2^{31} - 1<code>{2, 3, 5}</code>).</li>
</ul>"""

DEEP[204] = """<h3>Problem Overview</h3>
<p>Given an integer <code>{2, 3, 5}</code>n<code>{2, 3, 5}</code>, return the number of prime numbers strictly less than <code>{2, 3, 5}</code>n<code>{2, 3, 5}</code>.</p>

<h3>Key Insights</h3>
<p>Checking each number up to <code>{2, 3, 5}</code>n<code>{2, 3, 5}</code> individually with trial division takes <code>{2, 3, 5}</code>O(n \\sqrt{n})<code>{2, 3, 5}</code> time, which will TLE for <code>{2, 3, 5}</code>n = 5 \times 10^6<code>{2, 3, 5}</code>.</p>
<p>The optimal algorithm is the <strong>Sieve of Eratosthenes</strong>:
<ol>
  <li>Initialize a boolean array <code>is_prime</code> of size <code>{2, 3, 5}</code>n<code>{2, 3, 5}</code> with <code>True</code>. Set indices 0 and 1 to <code>False</code>.</li>
  <li>For each <code>{2, 3, 5}</code>i<code>{2, 3, 5}</code> from 2 up to <code>{2, 3, 5}</code>\\lfloor \\sqrt{n} \rfloor<code>{2, 3, 5}</code>:
    <ul>
      <li>If <code>is_prime[i]</code> is true, mark all multiples of <code>{2, 3, 5}</code>i<code>{2, 3, 5}</code> starting from <code>{2, 3, 5}</code>i^2<code>{2, 3, 5}</code> (step size <code>{2, 3, 5}</code>i<code>{2, 3, 5}</code>) as <code>False</code>.</li>
    </ul>
  </li>
  <li>Return <code>sum(is_prime)</code>.</li>
</ol></p>

<details>
<summary><strong>Python 3 Solution (Sieve of Eratosthenes - O(N log log N))</strong></summary>
<div class="code-block">
<pre><code class="language-python">class Solution:
    def countPrimes(self, n: int) -> int:
        if n < 3:
            return 0
            
        is_prime = [True] * n
        is_prime[0] = is_prime[1] = False
        
        limit = int(n**0.5)
        for i in range(2, limit + 1):
            if is_prime[i]:
                # Mark multiples starting from i*i
                is_prime[i*i:n:i] = [False] * len(is_prime[i*i:n:i])
                
        return sum(is_prime)
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> <code>{2, 3, 5}</code>O(n \\log \\log n)<code>{2, 3, 5}</code> by the Prime Number Theorem.</li>
  <li><strong>Space Complexity:</strong> <code>{2, 3, 5}</code>O(n)<code>{2, 3, 5}</code> boolean array.</li>
  <li><strong>Edge Cases:</strong> <code>{2, 3, 5}</code>n = 0, 1, 2<code>{2, 3, 5}</code> (returns 0).</li>
</ul>"""

DEEP[223] = """<h3>Problem Overview</h3>
<p>Given the coordinates of two rectilinear rectangles in a 2D plane: rectangle 1 <code>{2, 3, 5}</code>(ax1, ay1)<code>{2, 3, 5}</code> to <code>{2, 3, 5}</code>(ax2, ay2)<code>{2, 3, 5}</code> and rectangle 2 <code>{2, 3, 5}</code>(bx1, by1)<code>{2, 3, 5}</code> to <code>{2, 3, 5}</code>(bx2, by2)<code>{2, 3, 5}</code>, return the total area covered by the two rectangles.</p>

<h3>Key Insights</h3>
<p>By the <strong>Principle of Inclusion-Exclusion</strong>:
<code>{2, 3, 5}</code><code>{2, 3, 5}</code>\text{Total Area} = \text{Area}_1 + \text{Area}_2 - \text{Overlap Area}<code>{2, 3, 5}</code><code>{2, 3, 5}</code>
The overlap rectangle's boundaries are:
<ul>
  <li><code>{2, 3, 5}</code>\text{overlap_width} = \\max(0, \\min(ax2, bx2) - \\max(ax1, bx1))<code>{2, 3, 5}</code></li>
  <li><code>{2, 3, 5}</code>\text{overlap_height} = \\max(0, \\min(ay2, by2) - \\max(ay1, by1))<code>{2, 3, 5}</code></li>
</ul>
If either overlap width or height <code>{2, 3, 5}</code>\\le 0<code>{2, 3, 5}</code>, the rectangles do not intersect, and overlap area is 0.</p>

<details>
<summary><strong>Python 3 Solution (Click to Expand)</strong></summary>
<div class="code-block">
<pre><code class="language-python">class Solution:
    def computeArea(self, ax1: int, ay1: int, ax2: int, ay2: int, bx1: int, by1: int, bx2: int, by2: int) -> int:
        area1 = (ax2 - ax1) * (ay2 - ay1)
        area2 = (bx2 - bx1) * (by2 - by1)
        
        # Calculate intersection width and height
        overlap_width = max(0, min(ax2, bx2) - max(ax1, bx1))
        overlap_height = max(0, min(ay2, by2) - max(ay1, by1))
        overlap_area = overlap_width * overlap_height
        
        return area1 + area2 - overlap_area
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> <code>{2, 3, 5}</code>O(1)<code>{2, 3, 5}</code>.</li>
  <li><strong>Space Complexity:</strong> <code>{2, 3, 5}</code>O(1)<code>{2, 3, 5}</code>.</li>
  <li><strong>Edge Cases:</strong> One rectangle fully inside another, non-overlapping rectangles separated by distance.</li>
</ul>"""

DEEP[263] = """<h3>Problem Overview</h3>
<p>An ugly number is a positive integer whose prime factors are limited to 2, 3, and 5. Given an integer <code>{2, 3, 5}</code>n<code>{2, 3, 5}</code>, return <code>true</code> if <code>{2, 3, 5}</code>n<code>{2, 3, 5}</code> is an ugly number, and <code>false</code> otherwise.</p>

<h3>Key Insights</h3>
<p>If <code>{2, 3, 5}</code>n \\le 0<code>{2, 3, 5}</code>, it cannot be ugly (ugly numbers are positive by definition). Repeatedly divide <code>{2, 3, 5}</code>n<code>{2, 3, 5}</code> by 2, 3, and 5 while it is divisible. If the resulting value is 1, all prime factors were in <code>{2, 3, 5}</code>{2, 3, 5}<code>{2, 3, 5}</code>.</p>

<details>
<summary><strong>Python 3 Solution (Click to Expand)</strong></summary>
<div class="code-block">
<pre><code class="language-python">class Solution:
    def isUgly(self, n: int) -> bool:
        if n <= 0:
            return False
            
        for factor in (2, 3, 5):
            while n % factor == 0:
                n //= factor
                
        return n == 1
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> <code>{2, 3, 5}</code>O(\\log n)<code>{2, 3, 5}</code>.</li>
  <li><strong>Space Complexity:</strong> <code>{2, 3, 5}</code>O(1)<code>{2, 3, 5}</code>.</li>
  <li><strong>Edge Cases:</strong> <code>{2, 3, 5}</code>n \\le 0<code>{2, 3, 5}</code> (negative and zero return <code>False</code>), <code>{2, 3, 5}</code>n = 1<code>{2, 3, 5}</code> (returns <code>True</code>).</li>
</ul>"""

DEEP[264] = """<h3>Problem Overview</h3>
<p>Given an integer <code>{2, 3, 5}</code>n<code>{2, 3, 5}</code>, return the <code>{2, 3, 5}</code>n^{\text{th}}<code>{2, 3, 5}</code> ugly number. Ugly numbers are positive integers whose prime factors are limited to 2, 3, and 5.</p>

<h3>Key Insights</h3>
<p>Every ugly number after 1 must be formed by multiplying a previously generated ugly number by 2, 3, or 5.
We maintain three pointers <code>{2, 3, 5}</code>p_2, p_3, p_5<code>{2, 3, 5}</code>, each pointing to the candidate index in the sorted list of ugly numbers:
<code>{2, 3, 5}</code><code>{2, 3, 5}</code>next_ugly = \\min(ugly[p_2] \times 2, ugly[p_3] \times 3, ugly[p_5] \times 5)<code>{2, 3, 5}</code><code>{2, 3, 5}</code>
Whenever the chosen candidate matches <code>{2, 3, 5}</code>ugly[p_k] \times k<code>{2, 3, 5}</code>, advance <code>{2, 3, 5}</code>p_k<code>{2, 3, 5}</code>. (Handling duplicates like <code>{2, 3, 5}</code>2 \times 3 = 6<code>{2, 3, 5}</code> and <code>{2, 3, 5}</code>3 \times 2 = 6<code>{2, 3, 5}</code> naturally by advancing both pointers).</p>

<details>
<summary><strong>Python 3 Solution (Three-Pointer DP - O(N))</strong></summary>
<div class="code-block">
<pre><code class="language-python">class Solution:
    def nthUglyNumber(self, n: int) -> int:
        ugly = [1] * n
        p2 = p3 = p5 = 0
        
        for i in range(1, n):
            c2, c3, c5 = ugly[p2] * 2, ugly[p3] * 3, ugly[p5] * 5
            nxt = min(c2, c3, c5)
            ugly[i] = nxt
            
            if nxt == c2:
                p2 += 1
            if nxt == c3:
                p3 += 1
            if nxt == c5:
                p5 += 1
                
        return ugly[-1]
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> <code>{2, 3, 5}</code>O(n)<code>{2, 3, 5}</code> strictly linear time.</li>
  <li><strong>Space Complexity:</strong> <code>{2, 3, 5}</code>O(n)<code>{2, 3, 5}</code> array to store <code>{2, 3, 5}</code>n<code>{2, 3, 5}</code> ugly numbers.</li>
</ul>"""

DEEP[279] = """<h3>Problem Overview</h3>
<p>Given an integer <code>{2, 3, 5}</code>n<code>{2, 3, 5}</code>, return the least number of perfect square numbers that sum to <code>{2, 3, 5}</code>n<code>{2, 3, 5}</code>.</p>

<h3>Key Insights</h3>
<p>By <strong>Lagrange's Four-Square Theorem</strong>, every natural number can be represented as the sum of at most four integer squares!
Furthermore, by <strong>Legendre's Three-Square Theorem</strong>, a number can be expressed as the sum of three squares if and only if it is <em>not</em> of the form <code>{2, 3, 5}</code>4^k(8m + 7)<code>{2, 3, 5}</code>.
Hence, the answer is always strictly 1, 2, 3, or 4:
<ol>
  <li><strong>Answer 1:</strong> If <code>{2, 3, 5}</code>n<code>{2, 3, 5}</code> is a perfect square (<code>{2, 3, 5}</code>s^2 == n<code>{2, 3, 5}</code>).</li>
  <li><strong>Answer 4:</strong> While <code>{2, 3, 5}</code>n % 4 == 0<code>{2, 3, 5}</code>, <code>{2, 3, 5}</code>n //= 4<code>{2, 3, 5}</code>. If <code>{2, 3, 5}</code>n % 8 == 7<code>{2, 3, 5}</code>, answer is 4.</li>
  <li><strong>Answer 2:</strong> Check if <code>{2, 3, 5}</code>n = a^2 + b^2<code>{2, 3, 5}</code> for some integer <code>{2, 3, 5}</code>a<code>{2, 3, 5}</code>.</li>
  <li><strong>Answer 3:</strong> Otherwise, the answer is 3.</li>
</ol></p>

<details>
<summary><strong>Python 3 Solution (Number Theoretic O(sqrt(N)))</strong></summary>
<div class="code-block">
<pre><code class="language-python">class Solution:
    def numSquares(self, n: int) -> int:
        def is_square(x: int) -> bool:
            s = int(x**0.5)
            return s * s == x
            
        if is_square(n):
            return 1
            
        # Check Legendre's 4-square condition: 4^k * (8m + 7)
        temp = n
        while temp % 4 == 0:
            temp //= 4
        if temp % 8 == 7:
            return 4
            
        # Check if sum of two squares: n = a^2 + b^2
        for a in range(1, int(n**0.5) + 1):
            if is_square(n - a * a):
                return 2
                
        return 3
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> <code>{2, 3, 5}</code>O(\\sqrt{n})<code>{2, 3, 5}</code> time due to the 2-square search loop. Drastically faster than DP (<code>{2, 3, 5}</code>O(n \\sqrt{n})<code>{2, 3, 5}</code>).</li>
  <li><strong>Space Complexity:</strong> <code>{2, 3, 5}</code>O(1)<code>{2, 3, 5}</code>.</li>
</ul>"""

DEEP[335] = """<h3>Problem Overview</h3>
<p>Given an array of integers <code>distance</code>, where you start at <code>{2, 3, 5}</code>(0,0)<code>{2, 3, 5}</code> and move North, West, South, and East cyclically. Return <code>true</code> if your path crosses itself, and <code>false</code> otherwise.</p>

<h3>Key Insights</h3>
<p>There are only 3 fundamental geometric self-crossing configurations in this 4-directional spiral:
<ol>
  <li><strong>Crossing 4th line (Self-intersection with 3 steps ago):</strong>
      <code>{2, 3, 5}</code><code>{2, 3, 5}</code>d[i] \\ge d[i-2] \\quad \text{and} \\quad d[i-1] \\le d[i-3]<code>{2, 3, 5}</code><code>{2, 3, 5}</code></li>
  <li><strong>Overlapping 5th line (Self-intersection with 4 steps ago):</strong>
      <code>{2, 3, 5}</code><code>{2, 3, 5}</code>d[i-1] == d[i-3] \\quad \text{and} \\quad d[i] + d[i-4] \\ge d[i-2]<code>{2, 3, 5}</code><code>{2, 3, 5}</code></li>
  <li><strong>Crossing 6th line (Self-intersection with 5 steps ago):</strong>
      <code>{2, 3, 5}</code><code>{2, 3, 5}</code>d[i-2] \\ge d[i-4], \\quad d[i] + d[i-4] \\ge d[i-2], \\quad d[i-1] \\le d[i-3], \\quad d[i-1] + d[i-5] \\ge d[i-3]<code>{2, 3, 5}</code><code>{2, 3, 5}</code></li>
</ol></p>

<details>
<summary><strong>Python 3 Solution (Click to Expand)</strong></summary>
<div class="code-block">
<pre><code class="language-python">from typing import List

class Solution:
    def isSelfCrossing(self, distance: List[int]) -> bool:
        d = distance
        n = len(d)
        if n < 4:
            return False
            
        for i in range(3, n):
            # Case 1: crosses line i - 3
            if d[i] >= d[i - 2] and d[i - 1] <= d[i - 3]:
                return True
            # Case 2: overlaps line i - 4
            if i >= 4 and d[i - 1] == d[i - 3] and d[i] + d[i - 4] >= d[i - 2]:
                return True
            # Case 3: crosses line i - 5
            if i >= 5 and d[i - 2] >= d[i - 4] and d[i] + d[i - 4] >= d[i - 2] and d[i - 1] <= d[i - 3] and d[i - 1] + d[i - 5] >= d[i - 3]:
                return True
                
        return False
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> <code>{2, 3, 5}</code>O(N)<code>{2, 3, 5}</code> single linear scan.</li>
  <li><strong>Space Complexity:</strong> <code>{2, 3, 5}</code>O(1)<code>{2, 3, 5}</code>.</li>
</ul>"""

DEEP[372] = """<h3>Problem Overview</h3>
<p>Calculate <code>{2, 3, 5}</code>a^b \\pmod{1337}<code>{2, 3, 5}</code> where <code>{2, 3, 5}</code>a<code>{2, 3, 5}</code> is a positive integer and <code>{2, 3, 5}</code>b<code>{2, 3, 5}</code> is an extremely large positive integer given as an array of digits (e.g., <code>{2, 3, 5}</code>b = [1, 0]<code>{2, 3, 5}</code> represents <code>{2, 3, 5}</code>10<code>{2, 3, 5}</code>).</p>

<h3>Key Insights</h3>
<p>By mathematical induction on the base-10 representation:
<code>{2, 3, 5}</code><code>{2, 3, 5}</code>a^{[d_0, d_1, \\dots, d_{k-1}, d_k]} = \\left( a^{[d_0, \\dots, d_{k-1}]} \right)^{10} \\cdot a^{d_k} \\pmod{1337}<code>{2, 3, 5}</code><code>{2, 3, 5}</code>
This recurrence allows us to pop digits from right to left, combining modular exponentiation:
<code>{2, 3, 5}</code><code>{2, 3, 5}</code>\text{superPow}(a, b) = \text{pow}(\text{superPow}(a, b[:-1]), 10) \\cdot \text{pow}(a, b[-1]) \\pmod{1337}<code>{2, 3, 5}</code><code>{2, 3, 5}</code></p>

<details>
<summary><strong>Python 3 Solution (Recursive Modular Exponentiation)</strong></summary>
<div class="code-block">
<pre><code class="language-python">from typing import List

class Solution:
    MOD = 1337
    
    def qpow(self, base: int, exp: int) -> int:
        res = 1
        base %= self.MOD
        while exp > 0:
            if exp & 1:
                res = (res * base) % self.MOD
            base = (base * base) % self.MOD
            exp >>= 1
        return res

    def superPow(self, a: int, b: List[int]) -> int:
        if not b:
            return 1
        last_digit = b.pop()
        part1 = self.qpow(self.superPow(a, b), 10)
        part2 = self.qpow(a, last_digit)
        return (part1 * part2) % self.MOD
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> <code>{2, 3, 5}</code>O(L)<code>{2, 3, 5}</code> where <code>{2, 3, 5}</code>L<code>{2, 3, 5}</code> is the number of digits in <code>{2, 3, 5}</code>b<code>{2, 3, 5}</code>, since each digit requires <code>{2, 3, 5}</code>O(\\log 10) = O(1)<code>{2, 3, 5}</code> modular operations.</li>
  <li><strong>Space Complexity:</strong> <code>{2, 3, 5}</code>O(L)<code>{2, 3, 5}</code> recursion call stack.</li>
</ul>"""

DEEP[836] = """<h3>Problem Overview</h3>
<p>An axis-aligned rectangle is represented by <code>[x1, y1, x2, y2]</code>. Two rectangles overlap if the area of their intersection is positive. Return <code>true</code> if they overlap, else <code>false</code>.</p>

<h3>Key Insights</h3>
<p>Two 1D intervals <code>{2, 3, 5}</code>[x_1, x_2]<code>{2, 3, 5}</code> and <code>{2, 3, 5}</code>[x_3, x_4]<code>{2, 3, 5}</code> overlap if and only if:
<code>{2, 3, 5}</code><code>{2, 3, 5}</code>\\max(x_1, x_3) < \\min(x_2, x_4)<code>{2, 3, 5}</code><code>{2, 3, 5}</code>
For 2D rectangles to have positive overlapping area, their projections onto BOTH the X-axis and Y-axis must overlap simultaneously.</p>

<details>
<summary><strong>Python 3 Solution (Click to Expand)</strong></summary>
<div class="code-block">
<pre><code class="language-python">from typing import List

class Solution:
    def isRectangleOverlap(self, rec1: List[int], rec2: List[int]) -> bool:
        # Check X-projection overlap and Y-projection overlap
        x_overlap = max(rec1[0], rec2[0]) < min(rec1[2], rec2[2])
        y_overlap = max(rec1[1], rec2[1]) < min(rec1[3], rec2[3])
        return x_overlap and y_overlap
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> <code>{2, 3, 5}</code>O(1)<code>{2, 3, 5}</code>.</li>
  <li><strong>Space Complexity:</strong> <code>{2, 3, 5}</code>O(1)<code>{2, 3, 5}</code>.</li>
  <li><strong>Edge Cases:</strong> Line contact or point contact (perimeter touching is not positive area overlap, correctly handled by strict inequality <code><</code>).</li>
</ul>"""

DEEP[973] = """<h3>Problem Overview</h3>
<p>Given an array of <code>points</code> where <code>points[i] = [xi, yi]</code> represents a point on the X-Y plane and an integer <code>{2, 3, 5}</code>k<code>{2, 3, 5}</code>, return the <code>{2, 3, 5}</code>k<code>{2, 3, 5}</code> closest points to the origin <code>{2, 3, 5}</code>(0, 0)<code>{2, 3, 5}</code>.</p>

<h3>Key Insights</h3>
<p>Squared Euclidean distance: <code>{2, 3, 5}</code>dist^2 = x^2 + y^2<code>{2, 3, 5}</code>.
Because square root is monotonic, comparing <code>{2, 3, 5}</code>x^2 + y^2<code>{2, 3, 5}</code> preserves order without floating-point computations.
Two optimal strategies:
<ol>
  <li><strong>Max-Heap of size <code>{2, 3, 5}</code>k<code>{2, 3, 5}</code>:</strong> Maintain the <code>{2, 3, 5}</code>k<code>{2, 3, 5}</code> closest points. If a new point is closer than the heap root, pop and push: <code>{2, 3, 5}</code>O(n \\log k)<code>{2, 3, 5}</code> time, <code>{2, 3, 5}</code>O(k)<code>{2, 3, 5}</code> space.</li>
  <li><strong>QuickSelect (Optimal):</strong> Average <code>{2, 3, 5}</code>O(n)<code>{2, 3, 5}</code> time, partitioning in-place around pivot distances.</li>
</ol></p>

<details>
<summary><strong>Python 3 Solution (Max-Heap - O(N log K))</strong></summary>
<div class="code-block">
<pre><code class="language-python">from typing import List
import heapq

class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        # Max-heap storing (-dist_sq, x, y)
        heap = []
        for x, y in points:
            dist_sq = x * x + y * y
            if len(heap) < k:
                heapq.heappush(heap, (-dist_sq, x, y))
            else:
                if dist_sq < -heap[0][0]:
                    heapq.heapreplace(heap, (-dist_sq, x, y))
                    
        return [[x, y] for _, x, y in heap]
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> <code>{2, 3, 5}</code>O(n \\log k)<code>{2, 3, 5}</code>.</li>
  <li><strong>Space Complexity:</strong> <code>{2, 3, 5}</code>O(k)<code>{2, 3, 5}</code> to store the heap.</li>
  <li><strong>Edge Cases:</strong> <code>{2, 3, 5}</code>k == n<code>{2, 3, 5}</code>, multiple points having identical distances.</li>
</ul>"""

DEEP[1071] = """<h3>Problem Overview</h3>
<p>For two strings <code>{2, 3, 5}</code>s<code>{2, 3, 5}</code> and <code>{2, 3, 5}</code>t<code>{2, 3, 5}</code>, we say "<code>{2, 3, 5}</code>t<code>{2, 3, 5}</code> divides <code>{2, 3, 5}</code>s<code>{2, 3, 5}</code>" if and only if <code>{2, 3, 5}</code>s = t + t + \\dots + t<code>{2, 3, 5}</code> (i.e. <code>{2, 3, 5}</code>t<code>{2, 3, 5}</code> is concatenated with itself one or more times). Given two strings <code>str1</code> and <code>str2</code>, return the largest string <code>{2, 3, 5}</code>x<code>{2, 3, 5}</code> such that <code>{2, 3, 5}</code>x<code>{2, 3, 5}</code> divides both <code>str1</code> and <code>str2</code>.</p>

<h3>Key Insights</h3>
<p>A common divisor string exists if and only if:
<code>{2, 3, 5}</code><code>{2, 3, 5}</code>str1 + str2 == str2 + str1<code>{2, 3, 5}</code><code>{2, 3, 5}</code>
If this commutative concatenation condition fails, no common base string can ever exist (return <code>""</code>).
If it holds, the length of the GCD string is simply the numeric <code>{2, 3, 5}</code>\\gcd(\text{len}(str1), \text{len}(str2))<code>{2, 3, 5}</code>!
<code>{2, 3, 5}</code><code>{2, 3, 5}</code>\text{GCD string} = str1[0 : \\gcd(|str1|, |str2|)]<code>{2, 3, 5}</code><code>{2, 3, 5}</code></p>

<details>
<summary><strong>Python 3 Solution (Click to Expand)</strong></summary>
<div class="code-block">
<pre><code class="language-python">import math

class Solution:
    def gcdOfStrings(self, str1: str, str2: str) -> str:
        if str1 + str2 != str2 + str1:
            return ""
        g = math.gcd(len(str1), len(str2))
        return str1[:g]
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> <code>{2, 3, 5}</code>O(L_1 + L_2)<code>{2, 3, 5}</code> string equality check + <code>{2, 3, 5}</code>O(\\log(\\min(L_1, L_2)))<code>{2, 3, 5}</code> GCD.</li>
  <li><strong>Space Complexity:</strong> <code>{2, 3, 5}</code>O(L_1 + L_2)<code>{2, 3, 5}</code> for concatenation check.</li>
  <li><strong>Edge Cases:</strong> No common divisor (e.g. <code>"LEET"</code> and <code>"CODE"</code>), one string multiple of the other (<code>"ABCABC"</code> and <code>"ABC"</code>).</li>
</ul>"""

DEEP[2013] = """<h3>Problem Overview</h3>
<p>Implement the <code>DetectSquares</code> class to add 2D points from a stream and count the number of ways to choose three existing points that, together with a query point, form an axis-aligned square with positive area.</p>

<h3>Key Insights</h3>
<p>An axis-aligned square has four vertices: query point <code>{2, 3, 5}</code>(qx, qy)<code>{2, 3, 5}</code>, diagonal point <code>{2, 3, 5}</code>(x, y)<code>{2, 3, 5}</code>, and two anti-diagonal points <code>{2, 3, 5}</code>(qx, y)<code>{2, 3, 5}</code> and <code>{2, 3, 5}</code>(x, qy)<code>{2, 3, 5}</code>.
A point <code>{2, 3, 5}</code>(x, y)<code>{2, 3, 5}</code> can form a square with <code>{2, 3, 5}</code>(qx, qy)<code>{2, 3, 5}</code> if and only if:
<code>{2, 3, 5}</code><code>{2, 3, 5}</code>|x - qx| == |y - qy| > 0<code>{2, 3, 5}</code><code>{2, 3, 5}</code>
Once a valid diagonal point <code>{2, 3, 5}</code>(x, y)<code>{2, 3, 5}</code> is found, the number of valid squares formed is:
<code>{2, 3, 5}</code><code>{2, 3, 5}</code>\text{count}(x, y) \times \text{count}(qx, y) \times \text{count}(x, qy)<code>{2, 3, 5}</code><code>{2, 3, 5}</code>
We store point frequencies in a hash map <code>point_counts[(x, y)]</code> and iterate over distinct points.</p>

<details>
<summary><strong>Python 3 Solution (Click to Expand)</strong></summary>
<div class="code-block">
<pre><code class="language-python">from typing import List
from collections import defaultdict

class DetectSquares:
    def __init__(self):
        self.pts = defaultdict(int)

    def add(self, point: List[int]) -> None:
        self.pts[tuple(point)] += 1

    def count(self, point: List[int]) -> int:
        qx, qy = point
        total = 0
        
        # Iterate over all registered points as candidate diagonal points
        for (x, y), count_diag in self.pts.items():
            dx = abs(x - qx)
            dy = abs(y - qy)
            if dx > 0 and dx == dy:
                # Valid square diagonal candidate
                c1 = self.pts.get((qx, y), 0)
                c2 = self.pts.get((x, qy), 0)
                total += count_diag * c1 * c2
                
        return total
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> <code>add</code> is <code>{2, 3, 5}</code>O(1)<code>{2, 3, 5}</code>; <code>count</code> is <code>{2, 3, 5}</code>O(P)<code>{2, 3, 5}</code> where <code>{2, 3, 5}</code>P<code>{2, 3, 5}</code> is the number of distinct points added.</li>
  <li><strong>Space Complexity:</strong> <code>{2, 3, 5}</code>O(P)<code>{2, 3, 5}</code> hash map entries.</li>
  <li><strong>Edge Cases:</strong> Duplicate points at same coordinate (handled by multiplicative counting), points with same coordinate as query point (<code>{2, 3, 5}</code>dx = 0<code>{2, 3, 5}</code>, ignored).</li>
</ul>"""
