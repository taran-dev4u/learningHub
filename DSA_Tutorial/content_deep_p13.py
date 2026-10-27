# -*- coding: utf-8 -*-
"""
Deep tutorials for Pattern 13: String Manipulation Patterns.
Masterclass 12-step structured explanations with ASCII dry runs and complexity analyses.
"""

DEEP = {
9: '''<h2>🧭 How to think about it</h2>
<p>Given an integer <code>x</code>, return <code>true</code> if <code>x</code> is a palindrome, and <code>false</code> otherwise.</p>

<p>Negative numbers cannot be palindromes (e.g. <code>-121</code> reversed is <code>121-</code>).
Also, any positive number ending in <code>0</code> (except <code>0</code> itself) cannot be a palindrome (leading digit cannot be <code>0</code>).</p>
<p><strong>The O(1) Space Half-Reversal Trick:</strong>
Instead of converting to string (which takes $O(\\log_{10} x)$ memory) or reversing the entire integer (which risks 32-bit overflow), reverse only the <strong>second half</strong> of the number!
When <code>x <= reversed_num</code>, we have reached the midpoint:
- For even digits (e.g. 1221): <code>x == reversed_num</code> (12 == 12).
- For odd digits (e.g. 12321): <code>x == reversed_num // 10</code> (12 == 123 // 10).</p>

<h2>🐢 Brute force vs optimal</h2>
<p>String conversion uses heap allocation and $O(n)$ space. Half-number arithmetic reversal runs in $O(\\log_{10} n)$ time with zero string allocations and zero overflow risk.</p>

<div class="insight">💡 <strong>Key insight:</strong> Reverse digits from the right into <code>rev = rev * 10 + x % 10; x //= 10</code> until <code>x <= rev</code>. Check <code>x == rev or x == rev // 10</code>.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def isPalindrome(x: int) -> bool:
    # Negative numbers and non-zero multiples of 10 cannot be palindromes
    if x < 0 or (x % 10 == 0 and x != 0):
        return False
        
    rev = 0
    while x > rev:
        rev = rev * 10 + (x % 10)
        x //= 10
        
    # When length is odd, discard middle digit via rev // 10
    return x == rev or x == rev // 10
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(\\log_{10} n)$ — Divide by 10 at each step; takes at most $\\approx 5$ iterations for 32-bit int.<br>
<strong>Space:</strong> $O(1)$ — Only arithmetic scalar variables.</p>
''',
125: '''<h2>🧭 How to think about it</h2>
<p>A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward.</p>

<p>Use two pointers: <code>left = 0</code> and <code>right = len(s) - 1</code>.
Advance <code>left</code> past non-alphanumeric characters (<code>not s[left].isalnum()</code>).
Advance <code>right</code> past non-alphanumeric characters (<code>not s[right].isalnum()</code>).
Compare lowercased characters: if <code>s[left].lower() != s[right].lower()</code>, return <code>False</code> immediately.
Repeat until pointers cross!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Creating a cleaned filtered string takes $O(n)$ extra memory. Converging two pointers runs in-place with $O(1)$ auxiliary space.</p>

<div class="insight">💡 <strong>Key insight:</strong> Converge two pointers skipping non-alphanumerics via <code>isalnum()</code>. Compare <code>s[l].lower() == s[r].lower()</code> in $O(1)$ space.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def isPalindrome(s: str) -> bool:
    l, r = 0, len(s) - 1
    
    while l < r:
        while l < r and not s[l].isalnum():
            l += 1
        while l < r and not s[r].isalnum():
            r -= 1
            
        if s[l].lower() != s[r].lower():
            return False
            
        l += 1
        r -= 1
        
    return True
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n)$ — Single pass inward.<br>
<strong>Space:</strong> $O(1)$ — Two integer index pointers.</p>
''',
680: '''<h2>🧭 How to think about it</h2>
<p>Given a string <code>s</code>, return <code>true</code> if the <code>s</code> can be palindrome after deleting at most one character from it.</p>

<p>Run standard two pointers from ends: <code>l = 0, r = len(s) - 1</code>.
The moment we encounter a mismatch <code>s[l] != s[r]</code>, we have reached the fork in the road! We are allowed exactly one deletion:
1. <strong>Delete character at $l$:</strong> check if substring $s[l+1 \\dots r]$ is a palindrome.
2. <strong>Delete character at $r$:</strong> check if substring $s[l \\dots r-1]$ is a palindrome.
If either subproblem is a valid palindrome, return <code>True</code>; otherwise return <code>False</code>!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Trying all $n$ single deletions takes $O(n^2)$. Checking the first mismatch with two substring checks takes $O(n)$ time and $O(1)$ space.</p>

<div class="insight">💡 <strong>Key insight:</strong> At the first mismatch <code>s[l] != s[r]</code>, test if <code>s[l+1:r+1]</code> or <code>s[l:r]</code> is palindromic. Greedily terminates in $O(n)$ time.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def validPalindrome(s: str) -> bool:
    def is_pali_range(i: int, j: int) -> bool:
        while i < j:
            if s[i] != s[j]:
                return False
            i += 1
            j -= 1
        return True
        
    l, r = 0, len(s) - 1
    while l < r:
        if s[l] != s[r]:
            return is_pali_range(l + 1, r) or is_pali_range(l, r - 1)
        l += 1
        r -= 1
        
    return True
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n)$ — At most two linear scans.<br>
<strong>Space:</strong> $O(1)$ — Constant pointers.</p>
''',
49: '''<h2>🧭 How to think about it</h2>
<p>Given an array of strings <code>strs</code>, group the anagrams together. You can return the answer in any order.</p>

<p>Two strings are anagrams if and only if they contain the exact same characters with identical frequencies.
We can map each word to a canonical key in a hash table:
1. <strong>Sorting Key:</strong> <code>tuple(sorted(word))</code>. Time per word: $O(L \\log L)$.
2. <strong>Character Count Tuple Key:</strong> a 26-element tuple of counts for <code>'a'</code> through <code>'z'</code>. Time per word: $O(L)$.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Comparing every pair takes $O(n^2 \\cdot L)$. Hash map grouping with character count or sorted tuple runs in $O(n \\cdot L)$ or $O(n \\cdot L \\log L)$.</p>

<div class="insight">💡 <strong>Key insight:</strong> Group in a hash map using the 26-character frequency tuple <code>tuple(count)</code> as the dictionary key. Appends anagrams in $O(n \\cdot L)$ time!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">from collections import defaultdict

def groupAnagrams(strs: list[str]) -> list[list[str]]:
    groups = defaultdict(list)
    
    for s in strs:
        count = [0] * 26
        for ch in s:
            count[ord(ch) - ord('a')] += 1
        groups[tuple(count)].append(s)
        
    return list(groups.values())
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n \\cdot L)$ where $n = \text{len}(strs)$ and $L$ is max word length.<br>
<strong>Space:</strong> $O(n \\cdot L)$ to store grouped strings in the hash map.</p>
''',
242: '''<h2>🧭 How to think about it</h2>
<p>Given two strings <code>s</code> and <code>t</code>, return <code>true</code> if <code>t</code> is an anagram of <code>s</code>, and <code>false</code> otherwise.</p>

<p>If $\text{len}(s) \ne \text{len}(t)$, they cannot be anagrams.
Maintain a single frequency table of size 26:
- Increment count for each character in $s$: <code>table[ord(c) - 97] += 1</code>.
- Decrement count for each character in $t$: <code>table[ord(c) - 97] -= 1</code>.
- If any count drops below 0, return <code>False</code> immediately!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Sorting both strings takes $O(n \\log n)$ time and $O(n)$ space. A fixed 26-int frequency array runs in $O(n)$ time with $O(1)$ constant space.</p>

<div class="insight">💡 <strong>Key insight:</strong> Fixed 26-element integer array. One pass increments from $s$ and decrements from $t$. If all frequencies balance to 0, they are anagrams.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def isAnagram(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False
        
    counts = [0] * 26
    for c1, c2 in zip(s, t):
        counts[ord(c1) - ord('a')] += 1
        counts[ord(c2) - ord('a')] -= 1
        
    return all(c == 0 for c in counts)
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n)$ — Single linear pass over length $n$.<br>
<strong>Space:</strong> $O(1)$ — Exactly 26 integers allocated.</p>
''',
13: '''<h2>🧭 How to think about it</h2>
<p>Roman numerals are represented by seven symbols: <code>I(1), V(5), X(10), L(50), C(100), D(500), M(1000)</code>.</p>

<p>Roman numerals are usually written largest to smallest from left to right.
<strong>The Subtraction Rule:</strong> If a smaller numeral appears immediately <em>before</em> a larger numeral (e.g. <code>IV = 4</code>, <code>IX = 9</code>, <code>XL = 40</code>), it is subtracted instead of added!
Therefore:
- If <code>val[s[i]] < val[s[i + 1]]</code>: subtract <code>val[s[i]]</code>.
- Otherwise: add <code>val[s[i]]</code>.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Linear scan from left to right with a simple one-character lookahead runs in $O(n)$ time and $O(1)$ space.</p>

<div class="insight">💡 <strong>Key insight:</strong> Lookahead comparison: if current symbol value is strictly less than next symbol value, subtract it; else add it.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def romanToInt(s: str) -> int:
    values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    n = len(s)
    
    for i in range(n):
        curr = values[s[i]]
        if i + 1 < n and curr < values[s[i + 1]]:
            total -= curr
        else:
            total += curr
            
    return total
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n)$ — Single pass through the string (max length 15).<br>
<strong>Space:</strong> $O(1)$ — Fixed dictionary of 7 symbols.</p>
''',
12: '''<h2>🧭 How to think about it</h2>
<p>Seven different symbols represent Roman numerals. Given an integer <code>num</code>, convert it to a Roman numeral.</p>

<p>We greedily subtract the largest possible Roman symbol value!
To handle the subtraction cases (like <code>4 = IV</code>, <code>9 = IX</code>, <code>40 = XL</code>, <code>900 = CM</code>), we simply treat those six subtraction combinations as their own distinct denominations in our lookup table!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Greedy subtraction from 1000 down to 1. Because integers are bounded ($1 \\le num \\le 3999$), loop runs at most 13 steps.</p>

<div class="insight">💡 <strong>Key insight:</strong> Ordered denominations list including subtraction pairs: <code>[(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"), (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]</code>. Greedily append!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def intToRoman(num: int) -> str:
    denominations = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")
    ]
    res = []
    for val, sym in denominations:
        if num == 0:
            break
        count, num = divmod(num, val)
        res.append(sym * count)
        
    return "".join(res)
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(1)$ — Finite number of denominations (at most 13 operations).<br>
<strong>Space:</strong> $O(1)$ — Constant output string buffer.</p>
''',
8: '''<h2>🧭 How to think about it</h2>
<p>Implement the <code>myAtoi(string s)</code> function, which converts a string to a 32-bit signed integer (similar to C/C++'s <code>atoi</code> function).</p>

<p>The 4-step state machine:
1. <strong>Whitespace:</strong> Discard leading whitespace (<code>s.lstrip()</code>).
2. <strong>Sign:</strong> Check if next character is <code>'+'</code> or <code>'-'</code>. Set <code>sign = -1</code> or <code>1</code>.
3. <strong>Digits:</strong> Read consecutive digits until a non-digit character or end of string.
4. <strong>Clamping:</strong> Clamp integer into 32-bit signed range: $[-2^{31}, 2^{31} - 1]$.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Linear scan with arithmetic overflow clamping. Prevents 64-bit integer overflow if in languages without arbitrary precision.</p>

<div class="insight">💡 <strong>Key insight:</strong> Accumulate <code>num = num * 10 + digit</code>. Clamp with <code>max(-2**31, min(2**31 - 1, sign * num))</code>.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def myAtoi(s: str) -> int:
    s = s.lstrip()
    if not s:
        return 0
        
    sign = 1
    idx = 0
    if s[0] == '-':
        sign = -1
        idx = 1
    elif s[0] == '+':
        idx = 1
        
    res = 0
    INT_MAX = 2**31 - 1
    INT_MIN = -2**31
    
    while idx < len(s) and s[idx].isdigit():
        digit = int(s[idx])
        # Check overflow
        if res > (INT_MAX - digit) // 10:
            return INT_MAX if sign == 1 else INT_MIN
        res = res * 10 + digit
        idx += 1
        
    res *= sign
    return max(INT_MIN, min(INT_MAX, res))
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n)$ — Single linear pass.<br>
<strong>Space:</strong> $O(1)$ — Scalar variables only.</p>
''',
43: '''<h2>🧭 How to think about it</h2>
<p>Given two non-negative integers <code>num1</code> and <code>num2</code> represented as strings, return the product of <code>num1</code> and <code>num2</code>, also represented as a string. Note: You must not use any built-in BigInteger library or convert the inputs to integer directly.</p>

<p>Elementary school multiplication simulation!
A number of length $m$ multiplied by a number of length $n$ will have at most $m + n$ digits (e.g. $99 \\times 99 = 9801$, length 2 + 2 = 4).
Let <code>res</code> be an array of size $m + n$ initialized to zeros.
When multiplying digit $num1[i]$ and $num2[j]$:
- The product <code>mul = int(num1[i]) * int(num2[j])</code> contributes to indices <code>p1 = i + j</code> and <code>p2 = i + j + 1</code>.
- <code>total = mul + res[p2]</code>
- <code>res[p2] = total % 10</code>
- <code>res[p1] += total // 10</code></p>

<h2>🐢 Brute force vs optimal</h2>
<p>Simulating digit by digit in an array of size $m + n$ executes in $O(m \\times n)$ time and $O(m + n)$ space without any library cheat.</p>

<div class="insight">💡 <strong>Key insight:</strong> The product of digit at index $i$ and index $j$ lands at indices $i + j$ (carry) and $i + j + 1$ (digit) in the output array.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def multiply(num1: str, num2: str) -> str:
    if num1 == "0" or num2 == "0":
        return "0"
        
    m, n = len(num1), len(num2)
    res = [0] * (m + n)
    
    for i in range(m - 1, -1, -1):
        d1 = ord(num1[i]) - ord('0')
        for j in range(n - 1, -1, -1):
            d2 = ord(num2[j]) - ord('0')
            mul = d1 * d2
            p1, p2 = i + j, i + j + 1
            
            total = mul + res[p2]
            res[p2] = total % 10
            res[p1] += total // 10
            
    # Skip leading zeros
    start = 0
    while start < len(res) and res[start] == 0:
        start += 1
        
    return "".join(map(str, res[start:]))
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(m \\times n)$ — Each digit pair multiplied once.<br>
<strong>Space:</strong> $O(m + n)$ — Digits array of size $m + n$.</p>
''',
273: '''<h2>🧭 How to think about it</h2>
<p>Convert a non-negative integer <code>num</code> to its English words representation.</p>

<p>Every group of 3 digits is named in the exact same way with a thousands-magnitude suffix:
- <code>10^9</code>: "Billion"
- <code>10^6</code>: "Million"
- <code>10^3</code>: "Thousand"
- <code>10^0</code>: ""</p>
<p>Write a helper function <code>words_under_1000(n)</code> that converts any number from 1 to 999:
- If $n \\ge 100$: <code>BELOW_20[n // 100] + " Hundred"</code>
- Remainder $< 20$: lookup in <code>BELOW_20</code>
- Remainder $\\ge 20$: <code>TENS[rem // 10] + " " + BELOW_20[rem % 10]</code></p>

<h2>🐢 Brute force vs optimal</h2>
<p>Chunk by 1,000 using division and modulo. Runs in $O(1)$ time because 32-bit integers are bounded by 2 Billion ($2^{31} - 1$).</p>

<div class="insight">💡 <strong>Key insight:</strong> Process chunks of 1,000 using triplets <code>("Billion", "Million", "Thousand", "")</code>. Format 3-digit numbers with <code>Hundreds + Tens + Ones</code> lookup arrays.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def numberToWords(num: int) -> str:
    if num == 0:
        return "Zero"
        
    LESS_THAN_20 = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten",
                    "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
    TENS = ["", "Ten", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
    THOUSANDS = ["", "Thousand", "Million", "Billion"]
    
    def helper(n):
        if n == 0:
            return ""
        elif n < 20:
            return LESS_THAN_20[n] + " "
        elif n < 100:
            return TENS[n // 10] + " " + helper(n % 10)
        else:
            return LESS_THAN_20[n // 100] + " Hundred " + helper(n % 100)
            
    res = ""
    for i, unit in enumerate(THOUSANDS):
        if num % 1000 != 0:
            res = helper(num % 1000) + unit + " " + res
        num //= 1000
        
    return res.strip()
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(1)$ — At most 4 chunks of 3 digits.<br>
<strong>Space:</strong> $O(1)$ — Constant size lookup tables.</p>
''',
6: '''<h2>🧭 How to think about it</h2>
<p>The string <code>"PAYPALISHIRING"</code> is written in a zigzag pattern on a given number of rows like this:
<pre>
P   A   H   N
A P L S I I G
Y   I   R
</pre>
And then read line by line: <code>"PAHNAPLSIIGYIR"</code>.</p>

<p>Track the current row <code>curr_row</code> and direction <code>step = 1</code> (moving down) or <code>step = -1</code> (moving up diagonally).
- Whenever <code>curr_row == 0</code>, set <code>step = 1</code>.
- Whenever <code>curr_row == numRows - 1</code>, set <code>step = -1</code>.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Instead of creating an entire 2D matrix with empty spaces, maintain a list of <code>numRows</code> string buffers! Append each character to <code>rows[curr_row]</code>, then join all rows at the end.</p>

<div class="insight">💡 <strong>Key insight:</strong> Bouncing pointer: <code>curr_row += step</code>. Reverse step direction (<code>step = -step</code>) when hitting row 0 or row <code>numRows - 1</code>.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def convert(s: str, numRows: int) -> str:
    if numRows == 1 or numRows >= len(s):
        return s
        
    rows = [[] for _ in range(numRows)]
    curr_row = 0
    step = -1
    
    for ch in s:
        rows[curr_row].append(ch)
        if curr_row == 0 or curr_row == numRows - 1:
            step = -step
        curr_row += step
        
    return "".join("".join(row) for row in rows)
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n)$ — Single pass over string $s$.<br>
<strong>Space:</strong> $O(n)$ — String buffers holding characters.</p>
''',
14: '''<h2>🧭 How to think about it</h2>
<p>Write a function to find the longest common prefix string amongst an array of strings. If there is no common prefix, return an empty string <code>""</code>.</p>

<p><strong>Vertical Scanning:</strong>
Look at index <code>i</code> across all strings simultaneously.
If index <code>i</code> exceeds any string's length or <code>strs[j][i] != strs[0][i]</code>, the common prefix ends right before index <code>i</code>!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Vertical scanning stops at the earliest mismatch point. Worst-case time is $O(S)$ where $S$ is total characters across all strings; best case takes only $O(n \\times \text{min\\_len})$ operations.</p>

<div class="insight">💡 <strong>Key insight:</strong> Vertical scanning: check character at column $i$ for all strings. Stop at the very first mismatch or end-of-string.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def longestCommonPrefix(strs: list[str]) -> str:
    if not strs:
        return ""
        
    for i in range(len(strs[0])):
        ch = strs[0][i]
        for s in strs[1:]:
            if i >= len(s) or s[i] != ch:
                return strs[0][:i]
                
    return strs[0]
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(S)$ where $S$ is sum of all characters in all strings.<br>
<strong>Space:</strong> $O(1)$ — No extra space allocated.</p>
''',

28: '''<h2>🧭 How to think about it</h2>
<p>Given two strings <code>needle</code> and <code>haystack</code>, return the index of the first occurrence of <code>needle</code> in <code>haystack</code>, or <code>-1</code> if <code>needle</code> is not part of <code>haystack</code>.</p>

<p>The standard benchmark algorithm for string searching is the <strong>Knuth-Morris-Pratt (KMP) Algorithm</strong>.
Instead of resetting the search pointer all the way back upon a mismatch ($O(n \\times m)$ worst case), KMP utilizes a precomputed <strong>LPS (Longest Proper Prefix which is also Suffix)</strong> table of the needle to skip redundant character comparisons!</p>

<p><strong>LPS Array Construction:</strong>
<code>lps[i]</code> stores the length of the longest proper prefix of <code>needle[0..i]</code> that is also a suffix of <code>needle[0..i]</code>.
When a mismatch occurs at <code>needle[j]</code> against <code>haystack[i]</code>, we don't back up <code>i</code>; we simply update <code>j = lps[j - 1]</code> and continue!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Naive sliding window takes $O((n - m + 1) \\times m)$ time. KMP guarantees strict $O(n + m)$ linear time with $O(m)$ space.</p>

<div class="insight">💡 <strong>Key insight:</strong> KMP failure function: precompute <code>lps</code> array in $O(m)$. On mismatch at <code>needle[j]</code>, roll back <code>j = lps[j - 1]</code> without ever rewinding pointer <code>i</code> in haystack!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def strStr(haystack: str, needle: str) -> int:
    if not needle:
        return 0
    m, n = len(needle), len(haystack)
    if m > n:
        return -1
        
    # 1. Build KMP LPS array
    lps = [0] * m
    prev_lps = 0
    i = 1
    while i < m:
        if needle[i] == needle[prev_lps]:
            prev_lps += 1
            lps[i] = prev_lps
            i += 1
        elif prev_lps > 0:
            prev_lps = lps[prev_lps - 1]
        else:
            lps[i] = 0
            i += 1
            
    # 2. Search needle in haystack
    i = 0 # pointer for haystack
    j = 0 # pointer for needle
    while i < n:
        if haystack[i] == needle[j]:
            i += 1
            j += 1
            if j == m:
                return i - m # Match found!
        elif j > 0:
            j = lps[j - 1]
        else:
            i += 1
            
    return -1
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n + m)$ — $O(m)$ for LPS preprocessing, $O(n)$ for search pass.<br>
<strong>Space:</strong> $O(m)$ — LPS array for needle of length $m$.</p>
''',
38: '''<h2>🧭 How to think about it</h2>
<p>The count-and-say sequence is a sequence of digit strings defined by the recursive formula:
- <code>countAndSay(1) = "1"</code>
- <code>countAndSay(n)</code> is the run-length encoding of <code>countAndSay(n - 1)</code>.</p>

<p>For example, to generate term <code>n = 4</code> from term <code>n = 3 ("21")</code>:
- Read <code>"2"</code>: one 2 $\\to$ <code>"12"</code>
- Read <code>"1"</code>: one 1 $\\to$ <code>"11"</code>
- Result: <code>"1211"</code>.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Iteratively apply two-pointer run-length encoding $n - 1$ times. Group identical consecutive characters with pointer $j$, append <code>str(count) + char</code>, and advance.</p>

<div class="insight">💡 <strong>Key insight:</strong> Two pointers group consecutive identical digits: count occurrences while <code>s[j] == s[i]</code>, append <code>f"{count}{s[i]}"</code>, and advance <code>i = j</code>.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def countAndSay(n: int) -> str:
    curr = "1"
    for _ in range(n - 1):
        res = []
        i = 0
        while i < len(curr):
            j = i
            while j < len(curr) and curr[j] == curr[i]:
                j += 1
            res.append(str(j - i))
            res.append(curr[i])
            i = j
        curr = "".join(res)
    return curr
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n \\times L)$ where $L$ is length of the generated string.<br>
<strong>Space:</strong> $O(L)$ — Output buffer for the current string.</p>
''',
68: '''<h2>🧭 How to think about it</h2>
<p>Given an array of strings <code>words</code> and a width <code>maxWidth</code>, format the text such that each line has exactly <code>maxWidth</code> characters and is fully (left and right) justified.</p>

<p>Rules to handle:
1. <strong>Pack as many words as possible:</strong> a line can hold words if $\\sum \text{len}(w) + (k - 1) \\le \text{maxWidth}$.
2. <strong>Evenly distribute extra spaces:</strong>
   - Let <code>total_spaces = maxWidth - sum_len_words</code>.
   - If line has $k > 1$ words, there are $k - 1$ slots.
   - Base spaces per slot: <code>base = total_spaces // (k - 1)</code>.
   - Extra spaces assigned to leftmost slots: <code>extra = total_spaces % (k - 1)</code>.
3. <strong>Edge cases (Single word line OR Last line):</strong>
   - Left-justify! Words separated by exactly single space <code>" "</code>, and pad remaining spaces to the right until <code>maxWidth</code>.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Single linear pass over <code>words</code> collecting lines greedily, then applying formatting rules in $O(N)$ time.</p>

<div class="insight">💡 <strong>Key insight:</strong> Greedily pack words per line. If $k=1$ or last line: left justify (join with <code>" "</code> and <code>ljust(maxWidth)</code>). Otherwise: distribute <code>total_spaces // (k-1)</code> with <code>total_spaces % (k-1)</code> extra to left slots.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def fullJustify(words: list[str], maxWidth: int) -> list[str]:
    res = []
    i = 0
    n = len(words)
    
    while i < n:
        # 1. Determine which words fit on current line
        line_words = [words[i]]
        line_len = len(words[i])
        j = i + 1
        while j < n and line_len + 1 + len(words[j]) <= maxWidth:
            line_words.append(words[j])
            line_len += 1 + len(words[j])
            j += 1
            
        k = len(line_words)
        total_word_len = sum(len(w) for w in line_words)
        total_spaces = maxWidth - total_word_len
        
        # 2. Case: Last line OR single word line -> Left justify
        if j == n or k == 1:
            line = " ".join(line_words).ljust(maxWidth)
        else:
            # 3. Fully justify
            base_spaces = total_spaces // (k - 1)
            extra_spaces = total_spaces % (k - 1)
            line_parts = []
            for idx in range(k - 1):
                line_parts.append(line_words[idx])
                spaces = base_spaces + (1 if idx < extra_spaces else 0)
                line_parts.append(" " * spaces)
            line_parts.append(line_words[-1])
            line = "".join(line_parts)
            
        res.append(line)
        i = j
        
    return res
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(N)$ where $N$ is total length of all characters.<br>
<strong>Space:</strong> $O(N)$ — Justified text result array.</p>
''',
151: '''<h2>🧭 How to think about it</h2>
<p>Given an input string <code>s</code>, reverse the order of the words. A word is defined as a sequence of non-space characters. The words in <code>s</code> will be separated by at least one space. Return a string of the words in reverse order concatenated by a single space.</p>

<p>To solve in $O(1)$ auxiliary space (in mutable char arrays / C++ / Java):
1. Reverse the entire string.
2. Reverse each individual word in place.
3. Clean up multiple consecutive spaces and trim edges.</p>
<p>In Python: <code>" ".join(reversed(s.split()))</code> handles multi-spaces and edge whitespaces naturally.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Splitting on whitespace skips all multiple spaces and reverses words in $O(n)$ time.</p>

<div class="insight">💡 <strong>Key insight:</strong> <code>s.split()</code> in Python automatically strips leading/trailing spaces and groups runs of spaces. Reverse the word list and join with a single space.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def reverseWords(s: str) -> str:
    """
    Reverses words in string, cleaning excess whitespace in O(n) time.
    """
    return " ".join(reversed(s.split()))
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n)$ — Single pass to split, reverse, and join.<br>
<strong>Space:</strong> $O(n)$ — Words list buffer.</p>
''',
214: '''<h2>🧭 How to think about it</h2>
<p>You are given a string <code>s</code>. You can convert <code>s</code> to a palindrome by adding characters in front of it. Return the shortest palindrome you can find by performing this transformation.</p>

<p>To minimize characters added to the front, we must find the <strong>longest palindromic prefix</strong> of <code>s</code>!
Once we find the longest palindromic prefix of length $L$, the remaining suffix $s[L:]$ reversed and prepended to $s$ forms the shortest palindrome:
$$\text{Result} = \text{reverse}(s[L:]) + s$$</p>

<p><strong>The KMP Prefix Function Trick:</strong>
Form a combined string $T = s + \text{"#"} + \text{reverse}(s)$.
The value of $LPS[-1]$ (longest prefix of $T$ that is also suffix) is <strong>exactly</strong> the length of the longest palindromic prefix of $s$!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Checking palindromes from $n$ down to 1 takes $O(n^2)$. KMP LPS table computes the longest palindromic prefix in $O(n)$ linear time!</p>

<div class="insight">💡 <strong>Key insight:</strong> Build $T = s + \text{'#'} + \text{reverse}(s)$. Run KMP failure function. $l = LPS[-1]$ is the longest palindromic prefix! Prepend $s[l:][::-1]$.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def shortestPalindrome(s: str) -> str:
    if not s:
        return ""
        
    rev_s = s[::-1]
    temp = s + "#" + rev_s
    
    # Compute KMP LPS table
    lps = [0] * len(temp)
    prev = 0
    i = 1
    while i < len(temp):
        if temp[i] == temp[prev]:
            prev += 1
            lps[i] = prev
            i += 1
        elif prev > 0:
            prev = lps[prev - 1]
        else:
            lps[i] = 0
            i += 1
            
    # Length of longest palindromic prefix in s
    pal_len = lps[-1]
    
    # Suffix not included in palindrome must be reversed and prepended
    add_on = rev_s[:len(s) - pal_len]
    return add_on + s
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n)$ — Linear KMP LPS computation on string of length $2n + 1$.<br>
<strong>Space:</strong> $O(n)$ — LPS array and concatenated string.</p>
''',
271: '''<h2>🧭 How to think about it</h2>
<p>Design an algorithm to encode a list of strings to a string. The encoded string is then sent over the network and decoded back to the original list of strings.</p>

<p>Why can't we just use a delimiter like <code>','</code> or <code>'#'</code>?
Because any arbitrary delimiter character can appear <em>inside</em> the strings themselves (e.g. <code>["hello#world", "foo,bar"]</code>)!</p>

<p><strong>The Length-Prefixed Protocol (Chunking):</strong>
Prefix each word with its length, followed by a separator: <code>f"{len(word)}#{word}"</code>.
When decoding:
1. Read digits until encountering <code>'#'</code> to get integer $L$.
2. The next $L$ characters are guaranteed to be the exact content of the original string, regardless of what characters appear inside!
3. Advance pointer past $L$ and repeat.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Escaping delimiters requires parsing escape sequences. Length-prefix chunking is stateless, foolproof, and executes in $O(N)$ linear time.</p>

<div class="insight">💡 <strong>Key insight:</strong> Length-prefixed framing: encode each string as <code>f"{len(s)}#{s}"</code>. Decode reads length until <code>'#'</code>, then slices exactly $L$ bytes.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">class Codec:
    def encode(self, strs: list[str]) -> str:
        """Encodes a list of strings to a single string."""
        res = []
        for s in strs:
            res.append(f"{len(s)}#{s}")
        return "".join(res)

    def decode(self, s: str) -> list[str]:
        """Decodes a single string to a list of strings."""
        res = []
        i = 0
        while i < len(s):
            # Find delimiter '#'
            j = s.find('#', i)
            length = int(s[i:j])
            word = s[j + 1 : j + 1 + length]
            res.append(word)
            i = j + 1 + length
        return res
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(N)$ — Single pass encode and decode where $N$ is total character count.<br>
<strong>Space:</strong> $O(N)$ — Single contiguous string wire format.</p>
''',
686: '''<h2>🧭 How to think about it</h2>
<p>Given two strings <code>a</code> and <code>b</code>, return the minimum number of times you should repeat string <code>a</code> so that string <code>b</code> is a substring of it. If it is impossible, return <code>-1</code>.</p>

<p>How many repetitions could possibly be required?
To even have length $\\ge \text{len}(b)$, we need at least $k = \\lceil \text{len}(b) / \text{len}(a) \\rceil$ repetitions.
Because $b$ could start near the end of the first copy of $a$ and spill over, it might require at most <strong>one extra copy</strong>: $k + 1$!
Any repetitions beyond $k + 1$ are completely redundant: if $b$ is not in $a \\times k$ and not in $a \\times (k + 1)$, it will never be in $a \\times (k + 2)$!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Test $a \\times k$; if $b$ is inside, return $k$.
Else test $a \\times (k + 1)$; if $b$ is inside, return $k + 1$.
Otherwise, return -1! Can use KMP or Rabin-Karp substring search.</p>

<div class="insight">💡 <strong>Key insight:</strong> Lower bound repetitions $k = -(-\text{len}(b) // \text{len}(a))$. Only test $k$ and $k + 1$; if neither contains $b$, return -1.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def repeatedStringMatch(a: str, b: str) -> int:
    # Ceiling division for minimum repeats
    k = -(-len(b) // len(a))
    
    repeated = a * k
    if b in repeated:
        return k
    if b in (repeated + a):
        return k + 1
        
    return -1
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(|a| + |b|)$ with KMP or built-in Boyer-Moore-Horspool search.<br>
<strong>Space:</strong> $O(|a| \\times k)$ — Buffer for repeated string.</p>
''',
791: '''<h2>🧭 How to think about it</h2>
<p>You are given two strings <code>order</code> and <code>s</code>. All the characters of <code>order</code> are unique and were sorted in some custom order previously. Permute the characters of <code>s</code> so that they match the order that <code>order</code> was sorted.</p>

<p>Count frequencies of all characters in $s$ using a frequency map / <code>Counter</code>.
1. Iterate through characters $c$ in <code>order</code> in their specified sequence. If $c \\in s$, append $c \\times count[c]$ to result and delete from map.
2. Append all remaining characters not mentioned in <code>order</code> at the end (their order does not matter!).</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Custom sorting with comparator takes $O(n \\log n)$. Frequency counting (bucket sort) runs in $O(|order| + |s|)$ linear time with $O(1)$ space (26 lowercase letters).</p>

<div class="insight">💡 <strong>Key insight:</strong> Bucket sort: count frequencies in $s$. Append characters in sequence of <code>order</code>, then dump remaining unlisted characters. Runs in $O(n)$ time!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">from collections import Counter

def customSortString(order: str, s: str) -> str:
    counts = Counter(s)
    res = []
    
    # 1. Append characters in custom order
    for ch in order:
        if ch in counts:
            res.append(ch * counts[ch])
            del counts[ch]
            
    # 2. Append all remaining characters
    for ch, count in counts.items():
        res.append(ch * count)
        
    return "".join(res)
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(|order| + |s|)$ — Linear traversal.<br>
<strong>Space:</strong> $O(1)$ — 26 lowercase English letters frequency map.</p>
''',
796: '''<h2>🧭 How to think about it</h2>
<p>Given two strings <code>s</code> and <code>goal</code>, return <code>true</code> if and only if <code>s</code> can become <code>goal</code> after some number of shifts on <code>s</code>. A shift on <code>s</code> consists of moving the leftmost character of <code>s</code> to the rightmost position.</p>

<p><strong>The Concatenation Invariance:</strong>
Any cyclic rotation of string <code>s</code> of length $n$ must be a substring of <code>s + s</code>!
For example: <code>s = "abcde"</code> $\\to$ <code>s + s = "abcdeabcde"</code>.
All rotations (<code>"bcdea"</code>, <code>"cdeab"</code>, <code>"deabc"</code>, <code>"eabcd"</code>) are present inside <code>s + s</code>!</p>
<p>Therefore, <code>goal</code> is a rotation of <code>s</code> if and only if:
1. $\text{len}(s) == \text{len}(goal)$
2. <code>goal in (s + s)</code></p>

<h2>🐢 Brute force vs optimal</h2>
<p>Simulating all $n$ shifts takes $O(n^2)$. String containment check in <code>s + s</code> runs in $O(n)$ time with KMP.</p>

<div class="insight">💡 <strong>Key insight:</strong> Return <code>len(s) == len(goal) and goal in (s + s)</code>. Every valid cyclic shift is a substring of the doubled string.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def rotateString(s: str, goal: str) -> bool:
    """
    Checks if goal is a rotation of s in O(n) time.
    """
    return len(s) == len(goal) and goal in (s + s)
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n)$ — Substring search in string of length $2n$.<br>
<strong>Space:</strong> $O(n)$ — Concatenated string <code>s + s</code>.</p>
''',
3008: '''<h2>🧭 How to think about it</h2>
<p>You are given a 0-indexed string <code>s</code>, two strings <code>a</code> and <code>b</code>, and an integer <code>k</code>. An index $i$ is beautiful if:
1. $0 \\le i \\le \text{len}(s) - \text{len}(a)$ and $s[i \\dots i + \text{len}(a) - 1] == a$.
2. There exists some index $j$ such that $0 \\le j \\le \text{len}(s) - \text{len}(b)$ and $s[j \\dots j + \text{len}(b) - 1] == b$ with $|j - i| \\le k$.</p>

<p><strong>3-Step Efficient Pipeline:</strong>
1. <strong>Find all match indices of $a$ in $s$:</strong> Run KMP algorithm to find all starting indices <code>indices_a</code> in $O(n)$ time.
2. <strong>Find all match indices of $b$ in $s$:</strong> Run KMP algorithm to find all starting indices <code>indices_b</code> in $O(n)$ time.
3. <strong>Filter with Binary Search:</strong>
   For each index $i \\in indices\\_a$, we need to check if there is any $j \\in indices\\_b$ such that $i - k \\le j \\le i + k$.
   Use <code>bisect_left(indices_b, i - k)</code>. If the found index has $j \\le i + k$, then $i$ is beautiful!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Pairwise check takes $O(|indices\\_a| \\times |indices\\_b|)$. KMP pattern matching + binary search runs in $O(|s| + |indices\\_a| \\log |indices\\_b|)$.</p>

<div class="insight">💡 <strong>Key insight:</strong> KMP finds all match positions of $a$ and $b$ in $O(n)$. Binary search (<code>bisect_left</code>) on <code>indices_b</code> verifies $|j - i| \\le k$ in $O(\\log |b\\_matches|)$ per candidate!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">import bisect

def beautifulIndices(s: str, a: str, b: str, k: int) -> list[int]:
    def kmp_search(pattern: str) -> list[int]:
        m = len(pattern)
        if m == 0 or m > len(s):
            return []
            
        # LPS
        lps = [0] * m
        prev, i = 0, 1
        while i < m:
            if pattern[i] == pattern[prev]:
                prev += 1
                lps[i] = prev
                i += 1
            elif prev > 0:
                prev = lps[prev - 1]
            else:
                lps[i] = 0
                i += 1
                
        matches = []
        i, j = 0, 0
        while i < len(s):
            if s[i] == pattern[j]:
                i += 1
                j += 1
                if j == m:
                    matches.append(i - m)
                    j = lps[j - 1]
            elif j > 0:
                j = lps[j - 1]
            else:
                i += 1
        return matches

    indices_a = kmp_search(a)
    indices_b = kmp_search(b)
    
    res = []
    for i in indices_a:
        idx = bisect.bisect_left(indices_b, i - k)
        if idx < len(indices_b) and indices_b[idx] <= i + k:
            res.append(i)
            
    return res
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(|s| + |indices\\_a| \\log |indices\\_b|)$ — Linear KMP matchings followed by binary search.<br>
<strong>Space:</strong> $O(|s|)$ — Arrays of matching index coordinates.</p>
''',
459: '''<h2>🧭 How to think about it</h2>
<p>Given a string <code>s</code>, check if it can be constructed by taking a substring of it and appending one or more copies of the substring together.</p>

<p><strong>Approach 1: The Doubled String Theorem:</strong>
If a string $s$ is composed of repeated sub-patterns, then shifting $s$ cyclically will produce $s$ again!
Therefore, $s$ is periodic if and only if $s$ appears as a substring inside $(s + s)[1:-1]$ (stripping the first and last character so we don't match the original copies at indices $0$ and $n$).</p>

<p><strong>Approach 2: KMP LPS Property:</strong>
Let $L = lps[-1]$ be the longest prefix that is also a suffix of $s$.
The remaining characters $P = n - L$ represent the length of the candidate repeating unit!
If $L > 0$ and $n \\pmod{n - L} == 0$, then $s$ is periodically constructed from the prefix of length $n - L$!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Both the Doubled String trick <code>s in (s + s)[1:-1]</code> and KMP LPS check run in $O(n)$ time.</p>

<div class="insight">💡 <strong>Key insight:</strong> KMP LPS: let $L = lps[-1]$. If $L > 0$ and $n \\% (n - L) == 0$, $s$ is periodic! Or simply return <code>s in (s + s)[1:-1]</code>.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def repeatedSubstringPattern(s: str) -> bool:
    """
    Checks if string is periodic in O(n) time.
    """
    return s in (s + s)[1:-1]
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n)$ — Linear substring search in string of length $2n - 2$.<br>
<strong>Space:</strong> $O(n)$ — Sliced string buffer.</p>
''',
}