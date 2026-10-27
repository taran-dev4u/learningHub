# -*- coding: utf-8 -*-
"""
Deep tutorials for Pattern 14: Bit Manipulation Patterns.
Masterclass 12-step structured explanations with ASCII dry runs and complexity analyses.
"""

DEEP = {
136: '''<h2>🧭 How to think about it</h2>
<p>Given a non-empty array of integers <code>nums</code>, every element appears twice except for one. Find that single one. You must implement a solution with a linear runtime complexity and use only constant extra space.</p>

<p>The mathematical properties of the <strong>XOR ($\\oplus$) operation</strong>:
1. Identity: $x \\oplus 0 = x$
2. Self-Inverse: $x \\oplus x = 0$
3. Commutative and Associative: order of XORing does not matter ($a \\oplus b \\oplus a = (a \\oplus a) \\oplus b = 0 \\oplus b = b$).</p>
<p>If we XOR all elements in <code>nums</code> together, every pair cancels itself out to 0, leaving only the unique single number!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Hash set or frequency map takes $O(n)$ space. XOR reduction accumulates in $O(n)$ time with $O(1)$ constant memory.</p>

<div class="insight">💡 <strong>Key insight:</strong> XOR all numbers: <code>res = 0; for x in nums: res ^= x</code>. Paired duplicates cancel to 0; single element remains!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def singleNumber(nums: list[int]) -> int:
    res = 0
    for x in nums:
        res ^= x
    return res
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n)$ — Single linear pass over array.<br>
<strong>Space:</strong> $O(1)$ — Single scalar variable.</p>
''',
137: '''<h2>🧭 How to think about it</h2>
<p>Given an integer array <code>nums</code> where every element appears three times except for one, which appears exactly once. Find the single element and return it.</p>

<p><strong>Bit-Counting Modulo 3:</strong>
Consider each of the 32 bit positions independently.
For any bit position $i$, if every number appeared three times, the sum of bits at position $i$ across all numbers would be a multiple of 3 ($0 \\pmod 3$).
Because one number appears exactly once, if the sum of bits at position $i$ is not a multiple of 3, the unique number must have a <code>1</code> at bit $i$!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Counting bits position by position takes $32 \\times n = O(n)$ time and $O(1)$ space. Alternatively, a two-register digital logic circuit using <code>ones</code> and <code>twos</code> tracks modulo-3 states in a single pass.</p>

<div class="insight">💡 <strong>Key insight:</strong> Digital logic state machine: <code>ones = (ones ^ x) & ~twos</code> and <code>twos = (twos ^ x) & ~ones</code>. Tracks bits appearing 1 or 2 times modulo 3 in $O(n)$ time and $O(1)$ space.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def singleNumber(nums: list[int]) -> int:
    ones, twos = 0, 0
    for x in nums:
        # ones holds bits that appeared 1st time (and not 2nd time)
        ones = (ones ^ x) & ~twos
        # twos holds bits that appeared 2nd time (and not 3rd time)
        twos = (twos ^ x) & ~ones
    return ones
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n)$ — Single pass through array.<br>
<strong>Space:</strong> $O(1)$ — Two integer variables.</p>
''',
260: '''<h2>🧭 How to think about it</h2>
<p>Given an integer array <code>nums</code>, in which exactly two elements appear once and all other elements appear twice. Find the two elements that appear only once.</p>

<p>Let the two unique numbers be $A$ and $B$.
1. XOR all numbers in <code>nums</code>:
   $$\text{diff} = A \\oplus B$$
   Since $A \ne B$, $\text{diff} \ne 0$. There must be at least one bit position where $A$ and $B$ differ (one has <code>1</code>, the other has <code>0</code>)!
2. <strong>Isolate lowest set bit:</strong>
   $$\text{mask} = \text{diff} \\;\\&\\; (-\text{diff})$$
3. <strong>Partition into two groups:</strong>
   - Group 1: numbers where bit <code>mask</code> is 1 (contains $A$ and pairs).
   - Group 2: numbers where bit <code>mask</code> is 0 (contains $B$ and pairs).
XORing each group independently isolates $A$ and $B$!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Hash map requires $O(n)$ auxiliary space. Two-pass XOR partitioning isolates both elements in $O(n)$ time and $O(1)$ memory.</p>

<div class="insight">💡 <strong>Key insight:</strong> <code>diff = xor_all</code>. Isolate lowest set bit <code>diff & (-diff)</code>. Partition array into two buckets based on this bit; XOR each bucket to find the two unique numbers!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def singleNumber(nums: list[int]) -> list[int]:
    diff = 0
    for x in nums:
        diff ^= x
        
    # Isolate lowest set bit
    mask = diff & (-diff)
    
    a, b = 0, 0
    for x in nums:
        if x & mask:
            a ^= x
        else:
            b ^= x
            
    return [a, b]
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n)$ — Two passes over array.<br>
<strong>Space:</strong> $O(1)$ — Constant scalar variables.</p>
''',
268: '''<h2>🧭 How to think about it</h2>
<p>Given an array <code>nums</code> containing <code>n</code> distinct numbers in the range <code>[0, n]</code>, return the only number in the range that is missing from the array.</p>

<p><strong>XOR Invariance:</strong>
XOR all numbers in <code>nums</code> and all indices from $0$ to $n$:
$$\text{missing} = n \\oplus \\left( \\bigoplus_{i=0}^{n-1} (i \\oplus nums[i]) \\right)$$
Every number that is present appears twice (once in range $[0, n]$, once in <code>nums</code>) and cancels out to 0. The missing number appears only once!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Gauss sum $\frac{n(n+1)}{2} - \\sum nums$ can suffer integer overflow in 32-bit fixed integer types. XOR avoids all arithmetic overflow completely in $O(n)$ time and $O(1)$ space.</p>

<div class="insight">💡 <strong>Key insight:</strong> <code>res = len(nums); for i, x in enumerate(nums): res ^= i ^ x</code>. Returns the missing number in $O(n)$ time and $O(1)$ space.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def missingNumber(nums: list[int]) -> int:
    res = len(nums)
    for i, x in enumerate(nums):
        res ^= i ^ x
    return res
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n)$ — Single linear loop.<br>
<strong>Space:</strong> $O(1)$ — Single accumulator variable.</p>
''',
389: '''<h2>🧭 How to think about it</h2>
<p>You are given two strings <code>s</code> and <code>t</code>. String <code>t</code> is generated by random shuffling string <code>s</code> and then adding one more letter at a random position. Return the letter that was added to <code>t</code>.</p>

<p>XOR all character codes in string $s$ and string $t$.
Every character that appears in both $s$ and $t$ will cancel itself to 0. The single added character is left over!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Frequency map or sorting takes $O(n)$ or $O(n \\log n)$ time with extra memory. Running XOR runs in $O(n)$ time with $O(1)$ space.</p>

<div class="insight">💡 <strong>Key insight:</strong> XOR character ASCII codes: <code>res = 0; for c in s + t: res ^= ord(c)</code>. Return <code>chr(res)</code>.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def findTheDifference(s: str, t: str) -> str:
    res = 0
    for c in s:
        res ^= ord(c)
    for c in t:
        res ^= ord(c)
    return chr(res)
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n)$ — Linear pass over strings.<br>
<strong>Space:</strong> $O(1)$ — Constant integer register.</p>
''',
191: '''<h2>🧭 How to think about it</h2>
<p>Write a function that takes the binary representation of a positive integer and returns the number of set bits it has (also known as the Hamming weight).</p>

<p><strong>Brian Kernighan's Algorithm:</strong>
The bitwise operation:
$$n \\;\\&\\; (n - 1)$$
always clears the <strong>lowest set bit</strong> of $n$!
- If $n = 12$ (<code>1100</code>): $n - 1 = 11$ (<code>1011</code>) $\to n \\;\\&\\; (n - 1) = 8$ (<code>1000</code>).
- If $n = 8$ (<code>1000</code>): $n - 1 = 7$ (<code>0111</code>) $\to n \\;\\&\\; (n - 1) = 0$ (<code>0000</code>).</p>
<p>By repeatedly executing $n = n \\;\\&\\; (n - 1)$ until $n == 0$, the loop runs in <strong>strictly $O(k)$ iterations</strong> where $k$ is the number of <code>1</code> bits, skipping all <code>0</code> bits entirely!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Testing all 32 bits takes 32 iterations. Brian Kernighan's algorithm takes only as many iterations as there are set bits.</p>

<div class="insight">💡 <strong>Key insight:</strong> <code>while n: n &= (n - 1); count += 1</code>. Clears one set bit per loop iteration.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def hammingWeight(n: int) -> int:
    count = 0
    while n:
        n &= (n - 1)
        count += 1
    return count
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(k)$ where $k \\le 32$ is the number of set bits.<br>
<strong>Space:</strong> $O(1)$ — Single counter.</p>
''',
201: '''<h2>🧭 How to think about it</h2>
<p>Given two integers <code>left</code> and <code>right</code> that represent the range <code>[left, right]</code>, return the bitwise AND of all numbers in this range, inclusive.</p>

<p>If $left < right$, there is at least one even and one odd number in the range, which means the lowest bit (LSB) will alternate between <code>0</code> and <code>1</code>, making the LSB of the cumulative AND <strong>guaranteed to be 0</strong>!</p>
<p>In fact, as numbers increment from $left$ to $right$, all bits after the <strong>common prefix</strong> will toggle between 0 and 1 at least once.
Therefore, the bitwise AND of $[left, right]$ is simply the <strong>longest common binary prefix</strong> of $left$ and $right$, followed by trailing zeros!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Iterating $left \\dots right$ is $O(right - left)$ and TLEs for $2^{31}$. Shifting right until $left == right$ takes at most 32 operations ($O(1)$ time).</p>

<div class="insight">💡 <strong>Key insight:</strong> Find the common binary prefix of <code>left</code> and <code>right</code>: <code>while left < right: right &= (right - 1)</code>. Clears non-matching suffix bits instantly!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def rangeBitwiseAnd(left: int, right: int) -> int:
    while left < right:
        right &= (right - 1)
    return right
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(1)$ — At most 32 bit-clearing operations.<br>
<strong>Space:</strong> $O(1)$ — Modifies integer registers.</p>
''',
477: '''<h2>🧭 How to think about it</h2>
<p>The Hamming distance between two integers is the number of positions at which the corresponding bits are different. Given an integer array <code>nums</code>, return the sum of Hamming distances between all pairs of integers in <code>nums</code>.</p>

<p>Instead of comparing pairs $(i, j)$ ($O(n^2)$ time), calculate the contribution of each bit position $0 \\dots 31$ independently across all numbers!
For any bit position $b$:
- Let $k$ be the count of numbers in <code>nums</code> that have the $b$-th bit set to <code>1</code>.
- Then $n - k$ numbers have the $b$-th bit set to <code>0</code>.
Each pairing between a number with bit <code>1</code> and a number with bit <code>0</code> contributes exactly 1 to the Hamming distance!
$$\text{Hamming Contribution at bit } b = k \\times (n - k)$$
Total Hamming distance is simply $\\sum_{b=0}^{31} k_b \\times (n - k_b)$!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Comparing all $n(n-1)/2$ pairs takes $O(n^2)$ time. Column-wise bit counting runs in $32 \\times n = O(n)$ linear time and $O(1)$ space.</p>

<div class="insight">💡 <strong>Key insight:</strong> At bit $b$, if $k$ numbers have <code>1</code> and $n-k$ numbers have <code>0</code>, they form $k \\times (n - k)$ differing pairs. Sum over 32 bit positions!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def totalHammingDistance(nums: list[int]) -> int:
    n = len(nums)
    total = 0
    
    for b in range(32):
        ones = sum((x >> b) & 1 for x in nums)
        zeros = n - ones
        total += ones * zeros
        
    return total
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(32 \\times n) = O(n)$ — 32 passes over array.<br>
<strong>Space:</strong> $O(1)$ — Constant scalar variables.</p>
''',
338: '''<h2>🧭 How to think about it</h2>
<p>Given an integer <code>n</code>, return an array <code>ans</code> of length <code>n + 1</code> such that for each <code>i</code> ($0 \\le i \\le n$), <code>ans[i]</code> is the number of <code>1</code>'s in the binary representation of <code>i</code>.</p>

<p><strong>Bit DP Recurrence:</strong>
Notice that shifting right by 1 (<code>i >> 1</code>) divides $i$ by 2 and drops the lowest bit:
$$dp[i] = dp[i >> 1] + (i \\;\\&\\; 1)$$
Alternatively, using Brian Kernighan's lowest bit clear:
$$dp[i] = dp[i \\;\\&\\; (i - 1)] + 1$$
Both relations allow computing $dp[i]$ in $O(1)$ time using previously computed entries!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Counting bits independently for each number takes $O(n \\log n)$. Bit DP computes the entire array in $O(n)$ linear time.</p>

<div class="insight">💡 <strong>Key insight:</strong> <code>dp[i] = dp[i >> 1] + (i & 1)</code>. The bit count of $i$ is the bit count of $i // 2$ plus the lowest bit!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def countBits(n: int) -> list[int]:
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i >> 1] + (i & 1)
    return dp
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n)$ — Single pass from 1 to $n$.<br>
<strong>Space:</strong> $O(n)$ — Output array of size $n+1$.</p>
''',
1863: '''<h2>🧭 How to think about it</h2>
<p>The XOR total of an array is the bitwise XOR of all its elements. Given an array <code>nums</code>, return the sum of all XOR totals for every subset of <code>nums</code>.</p>

<p><strong>The Symmetry of Bits:</strong>
Consider any bit position $b$.
If at least one element in <code>nums</code> has bit $b$ set to 1, then exactly <strong>half</strong> of all $2^n$ subsets will have bit $b$ set in their subset XOR!
Why? Because choosing or omitting that element flips bit $b$ from 0 to 1 or 1 to 0 across all subset combinations!</p>
<p>Therefore, if bit $b$ is present in <strong>bitwise OR of all elements</strong>, it will contribute to exactly $2^{n-1}$ subsets:
$$\text{Total Sum} = (\text{OR of all elements in nums}) \\times 2^{n - 1}$$</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Backtracking through all $2^n$ subsets takes $O(2^n)$ time. The bitwise OR insight solves it in $O(n)$ linear time and $O(1)$ space!</p>

<div class="insight">💡 <strong>Key insight:</strong> Every bit set in <code>reduce(OR, nums)</code> appears in exactly $2^{n-1}$ subsets. Total sum $= (\text{OR\\_all}) \\ll (n - 1)$!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def subsetXORSum(nums: list[int]) -> int:
    or_all = 0
    for x in nums:
        or_all |= x
    return or_all << (len(nums) - 1)
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n)$ — Single linear OR reduction.<br>
<strong>Space:</strong> $O(1)$ — Constant memory.</p>
''',
190: '''<h2>🧭 How to think about it</h2>
<p>Reverse bits of a given 32 bits unsigned integer.</p>

<p>Iterate 32 times:
1. Shift result left by 1: <code>res = (res << 1)</code>.
2. Extract the lowest bit of $n$: <code>res |= (n & 1)</code>.
3. Shift $n$ right by 1: <code>n >>= 1</code>.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>32-step bit-by-bit reversal runs in $O(1)$ time. For frequent calls, precomputing a 256-entry lookup table reverses 8 bits per step (4 table lookups total).</p>

<div class="insight">💡 <strong>Key insight:</strong> 32-bit shift register: <code>res = (res << 1) | (n & 1); n >>= 1</code> for 32 iterations.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def reverseBits(n: int) -> int:
    res = 0
    for _ in range(32):
        res = (res << 1) | (n & 1)
        n >>= 1
    return res
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(1)$ — Exactly 32 operations.<br>
<strong>Space:</strong> $O(1)$ — Single 32-bit register.</p>
''',
231: '''<h2>🧭 How to think about it</h2>
<p>Given an integer <code>n</code>, return <code>true</code> if it is a power of two. Otherwise, return <code>false</code>.</p>

<p>A power of two in binary has <strong>exactly one set bit</strong> (e.g. $1=2^0=1_2, 2=2^1=10_2, 4=2^2=100_2, 8=2^3=1000_2$).
Recall Brian Kernighan's bit trick:
$$n \\;\\&\\; (n - 1)$$
clears the lowest set bit!
If $n$ has only one set bit, clearing it leaves <strong>0</strong>:
$$n > 0 \\quad \text{and} \\quad (n \\;\\&\\; (n - 1)) == 0$$</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Repeated division by 2 takes $O(\\log n)$. The single bitwise check runs in $O(1)$ constant time.</p>

<div class="insight">💡 <strong>Key insight:</strong> Power of two check: <code>n > 0 and (n & (n - 1)) == 0</code>. Executes in a single CPU cycle!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def isPowerOfTwo(n: int) -> bool:
    """
    Checks power of two in O(1) time and space.
    """
    return n > 0 and (n & (n - 1)) == 0
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(1)$ — Single bitwise operation.<br>
<strong>Space:</strong> $O(1)$ — No memory allocated.</p>
''',
342: '''<h2>🧭 How to think about it</h2>
<p>Given an integer <code>n</code>, return <code>true</code> if it is a power of four. Otherwise, return <code>false</code>.</p>

<p>Powers of four ($4^0=1, 4^1=4, 4^2=16, 4^3=64$) must satisfy two properties:
1. <strong>Must be a power of two:</strong> $n > 0$ and $(n \\;\\&\\; (n - 1)) == 0$.
2. <strong>The single set bit must be at an even bit position (0, 2, 4, 6...):</strong>
   In 32-bit binary, the mask with bits at all even positions is <code>0x55555555</code> (binary <code>01010101010101010101010101010101</code>)!
   $$n \\;\\&\\; \text{0x55555555} \ne 0$$
   Alternatively: $n \\pmod 3 == 1$!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Bitmask check runs in $O(1)$ time with zero loops.</p>

<div class="insight">💡 <strong>Key insight:</strong> Must be power of 2 AND single bit must be at even index: <code>n > 0 and (n & (n - 1)) == 0 and (n & 0x55555555) != 0</code>.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def isPowerOfFour(n: int) -> bool:
    return n > 0 and (n & (n - 1)) == 0 and (n & 0x55555555) != 0
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(1)$ — Instant bitmask verification.<br>
<strong>Space:</strong> $O(1)$ — Constant memory.</p>
''',
371: '''<h2>🧭 How to think about it</h2>
<p>Given two integers <code>a</code> and <code>b</code>, return the sum of the two integers without using the operators <code>+</code> and <code>-</code>.</p>

<p><strong>Half Adder Circuit:</strong>
- Bitwise XOR (<code>a ^ b</code>) performs addition <strong>without carry</strong> ($0+0=0, 1+0=1, 0+1=1, 1+1=0$).
- Bitwise AND (<code>a & b</code>) identifies where carries occur ($1+1$ generates carry). Shifted left by 1 (<code>(a & b) << 1</code>), it becomes the carry input for the next position!</p>
<p>Repeat until carry becomes 0:
- <code>sum = a ^ b</code>
- <code>carry = (a & b) << 1</code></p>
<p>In Python, integers have arbitrary precision, so mask with <code>0xFFFFFFFF</code> to simulate 32-bit signed two's complement integer arithmetic!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Simulates hardware ALU adder in $O(1)$ (at most 32 carry propagations).</p>

<div class="insight">💡 <strong>Key insight:</strong> Half adder: <code>while b: carry = (a & b) << 1; a = a ^ b; b = carry</code>. In Python, mask with <code>0xFFFFFFFF</code> to enforce 32-bit limits.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def getSum(a: int, b: int) -> int:
    mask = 0xFFFFFFFF
    
    while (b & mask) > 0:
        carry = (a & b) << 1
        a = a ^ b
        b = carry
        
    # If a is a negative 32-bit number, sign-extend it in Python
    return (a & mask) if b > 0 else a
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(1)$ — Carries propagate at most 32 times.<br>
<strong>Space:</strong> $O(1)$ — Two integer registers.</p>
''',
393: '''<h2>🧭 How to think about it</h2>
<p>Given an integer array <code>data</code> representing the data, return whether it is a valid UTF-8 encoding.</p>

<p>UTF-8 encoding rules:
1. <strong>1-byte character:</strong> starts with bit <code>0</code> (<code>0xxxxxxx</code>).
2. <strong>n-byte character ($2 \\le n \\le 4$):</strong>
   - First byte has $n$ leading <code>1</code>s followed by a <code>0</code> (e.g. <code>110xxxxx</code> for 2 bytes, <code>1110xxxx</code> for 3 bytes, <code>11110xxx</code> for 4 bytes).
   - Followed by $n - 1$ continuation bytes, each strictly starting with <code>10xxxxxx</code>.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Track <code>n_bytes</code> remaining.
For each byte:
- If <code>n_bytes == 0</code>: count leading 1s. If 0, it's 1-byte char; if 2, 3, or 4, set <code>n_bytes = count - 1</code>. If 1 or $> 4$, invalid!
- If <code>n_bytes > 0</code>: verify byte starts with <code>10xxxxxx</code> (<code>(byte >> 6) == 0b10</code>) and decrement <code>n_bytes -= 1</code>.
At end, verify <code>n_bytes == 0</code>.</p>

<div class="insight">💡 <strong>Key insight:</strong> State machine tracking continuation bytes: inspect top bits via right-shifts. First byte dictates expected continuation count.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def validUtf8(data: list[int]) -> bool:
    n_bytes = 0
    
    for num in data:
        byte = num & 0xFF
        if n_bytes == 0:
            if (byte >> 7) == 0:
                continue
            elif (byte >> 5) == 0b110:
                n_bytes = 1
            elif (byte >> 4) == 0b1110:
                n_bytes = 2
            elif (byte >> 3) == 0b11110:
                n_bytes = 3
            else:
                return False
        else:
            if (byte >> 6) != 0b10:
                return False
            n_bytes -= 1
            
    return n_bytes == 0
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n)$ — Single linear pass over bytes.<br>
<strong>Space:</strong> $O(1)$ — Single state tracker.</p>
''',
1318: '''<h2>🧭 How to think about it</h2>
<p>Given 3 positives numbers <code>a</code>, <code>b</code> and <code>c</code>. Return the minimum flips to make <code>(a OR b == c)</code>. In one flip, you can change any single bit (from 1 to 0, or 0 to 1) in <code>a</code> or <code>b</code>.</p>

<p>Inspect bit by bit from $0$ to $31$:
- Let $bit_a = (a >> i) \\& 1$, $bit_b = (b >> i) \\& 1$, $bit_c = (c >> i) \\& 1$.
- <strong>Case 1 ($bit_c == 1$):</strong>
  We need $(bit_a \\lor bit_b) == 1$.
  If both $bit_a == 0$ and $bit_b == 0$, we need <strong>1 flip</strong> (flip either $a$ or $b$ to 1).
- <strong>Case 2 ($bit_c == 0$):</strong>
  We need $(bit_a \\lor bit_b) == 0$.
  Both bits must be 0!
  If $bit_a == 1$, add 1 flip. If $bit_b == 1$, add 1 flip (up to <strong>2 flips</strong>).</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Loop runs exactly 32 times ($O(1)$ time and space).</p>

<div class="insight">💡 <strong>Key insight:</strong> If $c_i = 1$: flip $= 1$ only if both $a_i=0$ and $b_i=0$. If $c_i = 0$: flip $= a_i + b_i$ (both must be turned off).</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def minFlips(a: int, b: int, c: int) -> int:
    flips = 0
    for i in range(32):
        bit_a = (a >> i) & 1
        bit_b = (b >> i) & 1
        bit_c = (c >> i) & 1
        
        if bit_c == 1:
            if bit_a == 0 and bit_b == 0:
                flips += 1
        else:
            flips += bit_a + bit_b
            
    return flips
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(1)$ — 32 bit comparisons.<br>
<strong>Space:</strong> $O(1)$ — Scalar counter.</p>
''',
}
