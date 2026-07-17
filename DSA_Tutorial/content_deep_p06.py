# Deep tutorials — Pattern P6: Stack (Session 5).
# Keyed by LC number; merged as (6, lc). [[nn]] -> links via build.py.

DEEP = {

# ============================================================ LC 20 — Valid Parentheses
20: '''
<h2>🧭 How to think about it</h2>
<p>Check that every bracket is closed by the correct type in the correct order. Brackets nest like a stack of plates: the <strong>most recently opened</strong> bracket must be the <strong>first</strong> to close. So push openers, and on each closer verify it matches the opener you pop.</p>

<h2>🐢 Brute force first</h2>
<p>Repeatedly deleting adjacent matched pairs like <code>()</code>/<code>[]</code>/<code>{}</code> until nothing changes → O(n²). A single stack pass is O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> a stack captures "last opened, first closed" exactly. Push each opener; on a closer, the top of the stack must be its matching opener — otherwise (or if the stack is empty) it's invalid. Valid iff the stack ends empty.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Map each closer to its opener.</li>
<li>For each char: opener → push; closer → the popped top must match (else invalid).</li>
<li>Valid iff the stack is empty at the end.</li>
</ol>

<h2>🎞️ Visual dry run — s = "([{}])"</h2>
<pre class="viz">( → [(] ; [ → [(,[] ; { → [(,[,{] ; } pop { ✓ ; ] pop [ ✓ ; ) pop ( ✓ → empty → valid</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def isValid(s):
    match = {')': '(', ']': '[', '}': '{'}
    stack = []
    for c in s:
        if c in match:                    # a closer
            if not stack or stack.pop() != match[c]:
                return False
        else:
            stack.append(c)               # an opener
    return not stack                      # nothing left unclosed</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong>, <strong>Space O(n)</strong> for the stack.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Empty string → valid.</li>
<li>Closer with an empty stack → invalid.</li>
<li>Leftover openers → invalid.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Forgetting the empty-stack check before popping.</li>
<li>Only counting brackets without checking types/order.</li>
<li>Not verifying the stack is empty at the end.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Longest valid substring ([[32]]).</li>
<li>Minimum insertions/removals to balance ([[921]], [[1249]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[32]] · [[921]] · [[1249]]</p>
''',

# ============================================================ LC 32 — Longest Valid Parentheses
32: '''
<h2>🧭 How to think about it</h2>
<p>Find the length of the longest run of correctly matched parentheses. A <strong>stack of indices</strong> with a "base" marker at the bottom lets you measure valid stretches: when you close a bracket, the length is the distance from the current index back to the last unmatched position.</p>

<h2>🐢 Brute force first</h2>
<p>Check every substring for validity → O(n³) or O(n²). The index-stack pass is O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> push <code>−1</code> as a base. Push <code>'('</code> indices. On <code>')'</code>, pop; if the stack becomes empty, push the current index as a new base; otherwise the valid length is <code>i − stack[-1]</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Stack starts with <code>[-1]</code>.</li>
<li><code>'('</code> → push its index. <code>')'</code> → pop.</li>
<li>If empty after pop, push <code>i</code> (new base); else update <code>best = i − stack[-1]</code>.</li>
</ol>

<h2>🎞️ Visual dry run — s = ")()())"</h2>
<pre class="viz">stack[-1] ; ) pop → empty → push0 ; ( push1 ; ) pop → top0 → len 2−0=2
( push3 ; ) pop → top0 → len 4−0=4 (best) ; ) pop0 → empty → push5
Answer: 4</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def longestValidParentheses(s):
    stack = [-1]                          # base marker
    best = 0
    for i, c in enumerate(s):
        if c == '(':
            stack.append(i)
        else:
            stack.pop()
            if not stack:
                stack.append(i)           # new base after an unmatched ')'
            else:
                best = max(best, i - stack[-1])
    return best</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong>, <strong>Space O(n)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>No valid pair → 0.</li>
<li>Whole string valid → n.</li>
<li>Leading unmatched closers → reset the base.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Forgetting the <code>−1</code> base marker.</li>
<li>Measuring length as a count of pops instead of an index distance.</li>
<li>Not pushing a new base after the stack empties.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>DP alternative: <code>dp[i]</code> from the previous match.</li>
<li>Count valid substrings, not just the longest.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[20]] · [[921]] · [[1249]]</p>
''',

# ============================================================ LC 71 — Simplify Path
71: '''
<h2>🧭 How to think about it</h2>
<p>Normalize a Unix-style absolute path: collapse <code>//</code>, drop <code>.</code>, and let <code>..</code> pop up one directory. Split on <code>/</code> and process components with a <strong>stack of directory names</strong>: names push, <code>..</code> pops, and <code>.</code>/empty are ignored.</p>

<h2>🐢 Brute force first</h2>
<p>String find/replace loops are fragile with edge cases. A stack over the split components handles everything cleanly in O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> the canonical path is exactly the stack contents joined by <code>/</code>. A real directory name pushes; <code>..</code> pops if possible; <code>.</code> and empty tokens (from <code>//</code>) are skipped.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Split the path on <code>'/'</code>.</li>
<li>For each token: <code>'..'</code> → pop if non-empty; <code>''</code> or <code>'.'</code> → skip; else push.</li>
<li>Return <code>'/' + '/'.join(stack)</code>.</li>
</ol>

<h2>🎞️ Visual dry run — "/a/./b/../../c/"</h2>
<pre class="viz">tokens: a . b .. .. c
a→[a] ; .→skip ; b→[a,b] ; ..→[a] ; ..→[] ; c→[c]
Result: "/c"</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def simplifyPath(path):
    stack = []
    for token in path.split('/'):
        if token == '' or token == '.':
            continue                      # redundant separators / current dir
        elif token == '..':
            if stack:
                stack.pop()               # go up one directory
        else:
            stack.append(token)
    return '/' + '/'.join(stack)</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong>, <strong>Space O(n)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Root only (<code>"/"</code>) → <code>"/"</code>.</li>
<li><code>..</code> at the root → stays at root.</li>
<li>Trailing slash → no trailing slash in output.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Popping on <code>..</code> when the stack is empty.</li>
<li>Not skipping empty tokens from <code>//</code>.</li>
<li>Forgetting the leading <code>/</code> in the result.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Relative paths → track a notion of current directory.</li>
<li>Windows-style paths → different separators/drive letters.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[20]] · [[155]] · [[394]]</p>
''',

# ============================================================ LC 921 — Minimum Add to Make Parentheses Valid
921: '''
<h2>🧭 How to think about it</h2>
<p>Count the fewest parentheses to insert so the string balances. You don't need a full stack — just track the running <strong>balance of open brackets</strong>. A <code>')'</code> with no open bracket needs an inserted <code>'('</code>; any opens left at the end each need a <code>')'</code>.</p>

<h2>🐢 Brute force first</h2>
<p>Repeatedly removing matched pairs and counting leftovers works but is clumsy. A single balance sweep is O(n), O(1) space.</p>

<div class="insight">💡 <strong>Key insight:</strong> keep <code>open</code> (unmatched <code>'('</code>) and <code>needed</code> (insertions so far). On <code>'('</code>, <code>open += 1</code>. On <code>')'</code>: if <code>open &gt; 0</code> match it (<code>open −= 1</code>), else <code>needed += 1</code> (an insert). Answer is <code>needed + open</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Sweep tracking <code>open</code> and <code>needed</code>.</li>
<li><code>')'</code> without an open → increment <code>needed</code>.</li>
<li>Return <code>needed + open</code>.</li>
</ol>

<h2>🎞️ Visual dry run — s = "())("</h2>
<pre class="viz">( open1 ; ) open0 ; ) needed1 ; ( open1
answer = needed1 + open1 = 2</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def minAddToMakeValid(s):
    open_count = 0
    needed = 0
    for c in s:
        if c == '(':
            open_count += 1
        else:                             # ')'
            if open_count &gt; 0:
                open_count -= 1           # match an existing '('
            else:
                needed += 1               # must insert a '('
    return needed + open_count            # leftover '(' each need a ')'</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong>, <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Already valid → 0.</li>
<li>All openers → <code>n</code> insertions.</li>
<li>All closers → <code>n</code> insertions.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Forgetting to add leftover <code>open</code> at the end.</li>
<li>Using a stack when a counter suffices.</li>
<li>Letting <code>open</code> go negative instead of counting a needed insert.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Minimum removals for validity ([[1249]]).</li>
<li>Minimum insertions with weighted brackets (LC 1541).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[1249]] · [[20]] · [[1963]]</p>
''',

# ============================================================ LC 1249 — Minimum Remove to Make Valid Parentheses
1249: '''
<h2>🧭 How to think about it</h2>
<p>Delete the fewest parentheses so the string is valid (letters stay). Use a <strong>stack of indices of unmatched <code>'('</code></strong>. A <code>')'</code> with no open partner is itself invalid — mark it for removal. Whatever <code>'('</code> indices remain on the stack at the end are also unmatched — remove them too.</p>

<h2>🐢 Brute force first</h2>
<p>Trying deletions combinatorially is exponential. One stack pass identifies exactly the indices to drop in O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> push each <code>'('</code>'s index; on <code>')'</code>, pop a matching <code>'('</code> if available, else record this <code>')'</code> as removable. Leftover <code>'('</code> indices are removable. Rebuild the string skipping all removable indices.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Scan; track a stack of <code>'('</code> indices and a set of indices to remove.</li>
<li>Unmatched <code>')'</code> → add to the remove set.</li>
<li>Add leftover stack indices to the remove set; build the result skipping them.</li>
</ol>

<h2>🎞️ Visual dry run — s = "a)b(c)d"</h2>
<pre class="viz">a ; ) unmatched → remove idx1 ; b ; ( push idx3 ; c ; ) match pop3 ; d
remove {1} → "ab(c)d"</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def minRemoveToMakeValid(s):
    s = list(s)
    stack = []                            # indices of unmatched '('
    for i, c in enumerate(s):
        if c == '(':
            stack.append(i)
        elif c == ')':
            if stack:
                stack.pop()               # matched
            else:
                s[i] = ''                 # unmatched ')' → delete
    for i in stack:                       # unmatched '(' → delete
        s[i] = ''
    return ''.join(s)</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong>, <strong>Space O(n)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>No parentheses → unchanged.</li>
<li>All unmatched → all removed.</li>
<li>Already valid → unchanged.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Removing letters by mistake.</li>
<li>Forgetting to delete leftover unmatched <code>'('</code>.</li>
<li>Editing the string while iterating by value (use indices).</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Minimum insertions instead ([[921]]).</li>
<li>Return the number removed, not the string.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[921]] · [[20]] · [[1963]]</p>
''',

# ============================================================ LC 1963 — Minimum Number of Swaps to Make the String Balanced
1963: '''
<h2>🧭 How to think about it</h2>
<p>The string has equal numbers of <code>'['</code> and <code>']'</code>; you may swap any two characters; minimize swaps to make it balanced. Track the running balance: the number of <strong>unmatched closing brackets</strong> at the worst point tells you how many swaps you need — each swap fixes two of them.</p>

<h2>🐢 Brute force first</h2>
<p>Simulating swaps is expensive. Counting the maximum unmatched-closer depth gives the answer directly in O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> sweep tracking <code>balance</code> (<code>+1</code> for <code>'['</code>, <code>−1</code> for <code>']'</code>). When <code>balance</code> goes negative, that's an unmatched <code>']'</code>; track the count of such unmatched closers. A single swap moves a <code>'['</code> to the front and fixes two unmatched closers, so the answer is <code>ceil(unmatched / 2)</code> = <code>(unmatched + 1) // 2</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Sweep; on <code>']'</code> that would make balance negative, count it as unmatched and reset balance to 0.</li>
<li>The answer is <code>(unmatched + 1) // 2</code>.</li>
</ol>

<h2>🎞️ Visual dry run — s = "]]][[[" </h2>
<pre class="viz">unmatched closers accumulate to 3 → swaps = (3+1)//2 = 2</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def minSwaps(s):
    balance = 0
    unmatched = 0
    for c in s:
        if c == '[':
            balance += 1
        else:                             # ']'
            if balance &gt; 0:
                balance -= 1              # matched an earlier '['
            else:
                unmatched += 1            # an unmatched ']'
    return (unmatched + 1) // 2           # each swap fixes two</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong>, <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Already balanced → 0.</li>
<li>Fully reversed → about <code>n/4</code> swaps.</li>
<li>Single pair out of order → 1 swap.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Returning <code>unmatched</code> instead of half of it.</li>
<li>Forgetting integer ceiling <code>(x + 1)//2</code>.</li>
<li>Simulating swaps directly.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Minimum insertions/removals ([[921]], [[1249]]).</li>
<li>Balanced with multiple bracket types → needs a stack.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[921]] · [[1249]] · [[20]]</p>
''',

# ============================================================ LC 85 — Maximal Rectangle
85: '''
<h2>🧭 How to think about it</h2>
<p>Find the largest all-<code>1</code> rectangle in a binary matrix. Process the matrix <strong>row by row</strong>, building a histogram where each column's bar height is the number of consecutive 1s ending at that row. Then the answer for each row reduces to <strong>Largest Rectangle in Histogram</strong> ([[84]]).</p>

<h2>🐢 Brute force first</h2>
<p>Enumerate all rectangles → O((mn)²) or worse. The row-histogram + monotonic-stack approach is O(m·n).</p>

<div class="insight">💡 <strong>Key insight:</strong> for each row, <code>height[c]</code> grows by 1 if the cell is 1, else resets to 0. The best rectangle whose bottom edge is on this row equals the largest rectangle in that histogram. Take the max over all rows.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Maintain a running <code>heights</code> array across rows.</li>
<li>For each row, update heights, then run the histogram routine.</li>
<li>Track the global maximum area.</li>
</ol>

<h2>🎞️ Visual dry run — rows build heights</h2>
<pre class="viz">row1 heights [1,0,1,0,0]
row2 heights [2,0,2,1,1]
row3 heights [3,1,3,2,2] → histogram max here is the answer region</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def maximalRectangle(matrix):
    if not matrix:
        return 0
    n = len(matrix[0])
    heights = [0] * n
    best = 0
    def largest_hist(h):
        stack, area = [], 0
        for i in range(len(h) + 1):
            cur = h[i] if i &lt; len(h) else 0
            while stack and h[stack[-1]] &gt;= cur:
                height = h[stack.pop()]
                width = i if not stack else i - stack[-1] - 1
                area = max(area, height * width)
            stack.append(i)
        return area
    for row in matrix:
        for c in range(n):
            heights[c] = heights[c] + 1 if row[c] == '1' else 0
        best = max(best, largest_hist(heights))
    return best</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(m·n)</strong> — each row's histogram is O(n). <strong>Space O(n)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>All zeros → 0.</li>
<li>Single row → plain histogram.</li>
<li>Values as chars <code>'0'/'1'</code> vs ints — match the input type.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Not resetting a column's height to 0 on a 0 cell.</li>
<li>Bugs in the histogram width calculation.</li>
<li>Mixing up string vs integer cell values.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Maximal square ([[221]]) → DP instead.</li>
<li>Largest rectangle in histogram ([[84]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[84]] · [[221]] · [[739]]</p>
''',

# ============================================================ LC 316 — Remove Duplicate Letters
316: '''
<h2>🧭 How to think about it</h2>
<p>Keep exactly one of each letter so the result is the <strong>lexicographically smallest</strong> and preserves relative order. Build the answer on a <strong>monotonic stack</strong>: before adding a letter, pop larger letters off the top <em>if they appear again later</em> (so removing them now is safe and makes the string smaller).</p>

<h2>🐢 Brute force first</h2>
<p>Trying all subsequences is exponential. The greedy stack with last-occurrence info is O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> maintain a stack that stays increasing where possible. For a new letter <code>c</code> not already in the stack: while the top is larger than <code>c</code> AND appears later, pop it. Skip letters already on the stack. Last-occurrence indices tell you whether a popped letter can be recovered later.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Record each letter's last index; keep an <code>in_stack</code> set.</li>
<li>For each <code>c</code>: skip if already present; else pop larger tops that occur later, then push <code>c</code>.</li>
<li>Join the stack.</li>
</ol>

<h2>🎞️ Visual dry run — s = "cbacdcbc"</h2>
<pre class="viz">c→[c] ; b&lt;c and c later → pop c, push b → [b] ; a&lt;b later → pop b, push a → [a] ; ...
Result: "acdb"</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def removeDuplicateLetters(s):
    last = {c: i for i, c in enumerate(s)}   # last occurrence
    stack = []
    seen = set()
    for i, c in enumerate(s):
        if c in seen:
            continue
        while stack and stack[-1] &gt; c and last[stack[-1]] &gt; i:
            seen.discard(stack.pop())         # safe: it appears again later
        stack.append(c)
        seen.add(c)
    return ''.join(stack)</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — each letter pushed/popped at most once. <strong>Space O(26)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Already unique and sorted → unchanged.</li>
<li>All same letter → one letter.</li>
<li>Reverse-sorted with repeats → heavy popping.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Popping a letter that doesn't appear again (loses it forever).</li>
<li>Re-adding a letter already on the stack.</li>
<li>Forgetting the <code>seen</code> set bookkeeping when popping.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Most competitive subsequence ([[1673]]).</li>
<li>Remove k digits ([[402]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[402]] · [[1673]] · [[456]]</p>
''',

# ============================================================ LC 402 — Remove K Digits
402: '''
<h2>🧭 How to think about it</h2>
<p>Remove <code>k</code> digits from a number string to make the <strong>smallest</strong> possible number. Scan left to right building a <strong>monotonic increasing stack</strong>: whenever a new digit is smaller than the top, popping the top makes the number smaller — do that up to <code>k</code> times.</p>

<h2>🐢 Brute force first</h2>
<p>Trying all digit-removal choices is combinatorial. The greedy stack is O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> a larger digit sitting before a smaller one hurts the value, so pop it (spending one removal). After processing, if removals remain, drop from the end (the largest remaining digits). Strip leading zeros; empty means <code>"0"</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>For each digit: while <code>k &gt; 0</code> and the top &gt; current, pop and <code>k −= 1</code>; push current.</li>
<li>Remove any remaining <code>k</code> from the end.</li>
<li>Strip leading zeros; return <code>"0"</code> if empty.</li>
</ol>

<h2>🎞️ Visual dry run — num = "1432219", k = 3</h2>
<pre class="viz">1 ; 4 ; 3&lt;4 pop4 → [1,3] k2 ; 2&lt;3 pop3 → [1,2] k1 ; 2 ; 1&lt;2 pop2 → [1,1] k0 ; 9
Result: "1219"</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def removeKdigits(num, k):
    stack = []
    for d in num:
        while k &gt; 0 and stack and stack[-1] &gt; d:
            stack.pop(); k -= 1           # dropping a bigger leading digit helps
        stack.append(d)
    stack = stack[:len(stack) - k] if k else stack   # remove leftovers from end
    return ''.join(stack).lstrip('0') or '0'</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong>, <strong>Space O(n)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>k = length → <code>"0"</code>.</li>
<li>Already increasing digits → remove from the end.</li>
<li>Leading zeros after removal → strip them.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Forgetting to remove leftover k from the end when the string was non-decreasing.</li>
<li>Not stripping leading zeros / returning empty.</li>
<li>Popping on <code>≥</code> instead of <code>&gt;</code> (removes equal digits needlessly).</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Largest number → pop on <code>&lt;</code>.</li>
<li>Most competitive subsequence of fixed length ([[1673]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[1673]] · [[316]] · [[321]]</p>
''',

# ============================================================ LC 456 — 132 Pattern
456: '''
<h2>🧭 How to think about it</h2>
<p>Detect indices <code>i &lt; j &lt; k</code> with <code>nums[i] &lt; nums[k] &lt; nums[j]</code> (a "1-3-2" shape). Scan from the <strong>right</strong> keeping a stack of candidate "3" values and tracking the best possible "2" — the largest value that was already popped (guaranteed to sit to the right and be smaller than some "3").</p>

<h2>🐢 Brute force first</h2>
<p>Check all triples → O(n³); fixing the middle → O(n²). The right-to-left monotonic stack is O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> traverse right to left. Maintain a decreasing stack and a value <code>third</code> = the largest number that has been popped (this is a valid "2", smaller than the "3" that popped it). If the current number is less than <code>third</code>, it can be the "1" → pattern found. Pop while the top is smaller than the current (those become new <code>third</code> candidates).</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>third = −∞</code>, empty stack.</li>
<li>For <code>x</code> from right to left: if <code>x &lt; third</code> → return True.</li>
<li>While the stack top <code>&lt; x</code>, pop and set <code>third = popped</code>; push <code>x</code>.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [3,1,4,2]</h2>
<pre class="viz">right→left: 2 push ; 4&gt;2 pop → third=2, push4 ; 1&lt;third2 → True (1,4,2)</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def find132pattern(nums):
    third = float('-inf')                 # best candidate for the "2"
    stack = []
    for x in reversed(nums):
        if x &lt; third:                     # x is the "1"
            return True
        while stack and stack[-1] &lt; x:
            third = stack.pop()           # popped value is a valid "2"
        stack.append(x)                   # x is a candidate "3"
    return False</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong>, <strong>Space O(n)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Fewer than 3 elements → False.</li>
<li>Strictly increasing or decreasing → no pattern.</li>
<li>Duplicates → strict inequalities keep it correct.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Scanning left to right (much harder to track the "2").</li>
<li>Updating <code>third</code> incorrectly (it must be the largest popped value).</li>
<li>Using <code>≤</code> where strictness is required.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>132 with returned indices → track positions.</li>
<li>Other order patterns → adapt the stack invariant.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[496]] · [[739]] · [[316]]</p>
''',

# ============================================================ LC 496 — Next Greater Element I
496: '''
<h2>🧭 How to think about it</h2>
<p>For each value in <code>nums1</code> (a subset of <code>nums2</code>), find the first greater value to its right in <code>nums2</code>. Precompute the "next greater" for every element of <code>nums2</code> with a <strong>monotonic decreasing stack</strong>, store the answers in a map, then look up each query.</p>

<h2>🐢 Brute force first</h2>
<p>For each element scan right for a bigger one → O(n·m). The monotonic stack computes all next-greaters in O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> sweep <code>nums2</code> keeping a stack of values still waiting for their next greater. When a value <code>x</code> arrives, every stack element smaller than <code>x</code> has found its answer (<code>x</code>) — pop and record them. Unresolved elements get <code>−1</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Walk <code>nums2</code>; while the stack top &lt; current, pop and map it to the current value.</li>
<li>Push the current value.</li>
<li>Answer each <code>nums1</code> query from the map (default −1).</li>
</ol>

<h2>🎞️ Visual dry run — nums2 = [1,3,4,2]</h2>
<pre class="viz">1 push ; 3&gt;1 pop→map[1]=3, push3 ; 4&gt;3 pop→map[3]=4, push4 ; 2 push
map: 1→3, 3→4, 4→-1, 2→-1</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def nextGreaterElement(nums1, nums2):
    nxt = {}
    stack = []
    for x in nums2:
        while stack and stack[-1] &lt; x:
            nxt[stack.pop()] = x          # x is the next greater
        stack.append(x)
    return [nxt.get(v, -1) for v in nums1]</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n + m)</strong>, <strong>Space O(n)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Largest element → −1.</li>
<li>Descending <code>nums2</code> → all −1.</li>
<li>All distinct (guaranteed) → clean map keys.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Recomputing per query instead of precomputing.</li>
<li>Pushing indices when values suffice (values are unique here).</li>
<li>Forgetting the −1 default.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Circular array ([[503]]).</li>
<li>Next greater as a permutation number ([[556]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[503]] · [[739]] · [[556]]</p>
''',

# ============================================================ LC 503 — Next Greater Element II
503: '''
<h2>🧭 How to think about it</h2>
<p>Same "next greater" question, but the array is <strong>circular</strong> — after the last element you wrap to the first. Simulate the wrap by iterating the indices <strong>twice</strong> (using modulo), running the usual monotonic-stack sweep.</p>

<h2>🐢 Brute force first</h2>
<p>For each element scan up to n−1 forward positions (with wrap) → O(n²). Two passes with a stack are O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> loop <code>i</code> from 0 to <code>2n − 1</code>, using <code>nums[i % n]</code>. Keep a stack of <em>indices</em>; when the current value exceeds the value at the stack's top index, record its answer. The second pass lets earlier elements find greater values that wrap around.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Initialize <code>res = [-1]*n</code>, empty stack.</li>
<li>For <code>i</code> in <code>0..2n−1</code>: while the top index's value &lt; <code>nums[i%n]</code>, pop and set its result.</li>
<li>Push <code>i % n</code> only during the first pass (or push always; results only set once).</li>
</ol>

<h2>🎞️ Visual dry run — nums = [1,2,1]</h2>
<pre class="viz">i0(1) push0 ; i1(2)&gt;1 pop0→res[0]=2, push1 ; i2(1) push2 ; i3(1) ; i4(2)&gt;1 pop2→res[2]=2
res = [2,-1,2]</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def nextGreaterElements(nums):
    n = len(nums)
    res = [-1] * n
    stack = []                            # indices
    for i in range(2 * n):
        cur = nums[i % n]
        while stack and nums[stack[-1]] &lt; cur:
            res[stack.pop()] = cur
        if i &lt; n:
            stack.append(i)               # only push originals once
    return res</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — 2n iterations, each index popped once. <strong>Space O(n)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>All equal → all −1 (strictly greater needed).</li>
<li>Single element → −1.</li>
<li>Global max → −1 even with wrap.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Pushing indices during the second pass (double answers).</li>
<li>Using values instead of indices (duplicates confuse results).</li>
<li>Forgetting the modulo wrap.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Non-circular ([[496]]).</li>
<li>Next greater element in a linked list ([[1019]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[496]] · [[739]] · [[556]]</p>
''',

# ============================================================ LC 556 — Next Greater Element III
556: '''
<h2>🧭 How to think about it</h2>
<p>Given an integer, find the smallest larger integer using the same digits (or −1 if none, or if it overflows 32 bits). This is the classic <strong>next permutation</strong> on the digit sequence: find the rightmost ascending step, swap it with the next-larger digit to its right, then sort the tail ascending.</p>

<h2>🐢 Brute force first</h2>
<p>Generating all permutations and picking the next is factorial. Next-permutation is O(d) over the digits.</p>

<div class="insight">💡 <strong>Key insight:</strong> scan from the right for the first digit smaller than the one after it (the "pivot"). Swap it with the smallest digit to its right that's still larger, then reverse (sort ascending) everything after the pivot — that's the minimal increase.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Find pivot <code>i</code> where <code>digits[i] &lt; digits[i+1]</code> (rightmost). None → −1.</li>
<li>Find the rightmost <code>j &gt; i</code> with <code>digits[j] &gt; digits[i]</code>; swap.</li>
<li>Reverse the suffix after <code>i</code>. Check the 32-bit bound.</li>
</ol>

<h2>🎞️ Visual dry run — n = 12443322</h2>
<pre class="viz">digits 1 2 4 4 3 3 2 2 ; pivot at index1 (2&lt;4)
swap 2 with rightmost bigger (3) → 1 3 4 4 3 2 2 2 ; reverse suffix → 1 3 2 2 2 3 4 4
Answer: 13222344</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def nextGreaterElement(n):
    digits = list(str(n))
    i = len(digits) - 2
    while i &gt;= 0 and digits[i] &gt;= digits[i + 1]:
        i -= 1                            # find the pivot
    if i &lt; 0:
        return -1                         # digits fully descending
    j = len(digits) - 1
    while digits[j] &lt;= digits[i]:
        j -= 1                            # smallest digit &gt; pivot on the right
    digits[i], digits[j] = digits[j], digits[i]
    digits[i + 1:] = reversed(digits[i + 1:])   # minimal suffix
    result = int(''.join(digits))
    return result if result &lt; 2**31 else -1</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(d)</strong> in the digit count. <strong>Space O(d)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Descending digits (e.g., 4321) → −1.</li>
<li>Overflows 32-bit → −1.</li>
<li>Single digit → −1.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Sorting the whole suffix instead of reversing (works but slower; reversing is enough after the swap).</li>
<li>Choosing the wrong swap partner (must be the smallest digit still larger than the pivot).</li>
<li>Forgetting the 32-bit overflow check.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Next permutation of an array (LC 31).</li>
<li>Previous smaller permutation → mirror the logic.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[496]] · [[503]] · [[31]]</p>
''',

# ============================================================ LC 735 — Asteroid Collision
735: '''
<h2>🧭 How to think about it</h2>
<p>Asteroids move right (positive) or left (negative); equal-size opposite movers destroy each other, a bigger one survives. Process left to right with a <strong>stack</strong> of surviving asteroids: a right-mover always survives for now, but a left-mover may collide with right-movers on top of the stack.</p>

<h2>🐢 Brute force first</h2>
<p>Repeatedly scanning for collisions until stable is O(n²). One stack pass resolves everything in O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> a collision happens only when the stack top is positive (moving right) and the new asteroid is negative (moving left). Resolve by comparing magnitudes: pop smaller right-movers; if equal, both vanish; if the top is bigger, the new one vanishes. Only if the new asteroid clears all opposing tops does it get pushed.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>For each asteroid, assume it survives.</li>
<li>While it's left-moving and the top is right-moving: compare sizes and destroy accordingly.</li>
<li>Push it if it survived the collisions.</li>
</ol>

<h2>🎞️ Visual dry run — [5,10,-5]</h2>
<pre class="viz">5 push ; 10 push [5,10] ; -5: top10&gt;5 → -5 destroyed
Result: [5,10]</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def asteroidCollision(asteroids):
    stack = []
    for a in asteroids:
        alive = True
        while alive and a &lt; 0 and stack and stack[-1] &gt; 0:
            top = stack[-1]
            if top &lt; -a:
                stack.pop()               # top (smaller) explodes; keep checking
            elif top == -a:
                stack.pop(); alive = False   # both explode
            else:
                alive = False             # incoming explodes
        if alive:
            stack.append(a)
    return stack</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — each asteroid pushed/popped once. <strong>Space O(n)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>All same direction → no collisions.</li>
<li>Equal opposite pair → both vanish.</li>
<li>Left-movers at the start → no right-mover to hit; they survive.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Colliding same-direction asteroids (only right-then-left collides).</li>
<li>Forgetting the equal-size mutual destruction.</li>
<li>Pushing an asteroid that was actually destroyed.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Report survivors' original indices.</li>
<li>Cars/particles collision simulations.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[739]] · [[853]] · [[20]]</p>
''',

# ============================================================ LC 739 — Daily Temperatures
739: '''
<h2>🧭 How to think about it</h2>
<p>For each day, how many days until a warmer temperature? Keep a <strong>monotonic decreasing stack of indices</strong> of days still waiting for a warmer day. When a warmer day arrives, it resolves all the cooler days on top of the stack, and the answer is the index distance.</p>

<h2>🐢 Brute force first</h2>
<p>For each day scan forward for a warmer one → O(n²). The monotonic stack is O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> the stack holds indices of days with strictly decreasing temperatures (unresolved). A day <code>i</code> warmer than the stack's top day resolves it: <code>answer[top] = i − top</code>. Pop until the top is warmer, then push <code>i</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>res = [0]*n</code>, empty stack of indices.</li>
<li>For each <code>i</code>: while the top day is cooler than <code>temps[i]</code>, pop and set <code>res[top] = i − top</code>.</li>
<li>Push <code>i</code>.</li>
</ol>

<h2>🎞️ Visual dry run — temps = [73,74,75,71,69,72,76,73]</h2>
<pre class="viz">73 push ; 74&gt;73 res[0]=1 ; 75&gt;74 res[1]=1 ; 71 push ; 69 push ; 72 resolves 69,71 → res[4]=1,res[3]=2 ; 76 resolves 72,75 → res[5]=1,res[2]=4 ; 73 push
Result: [1,1,4,2,1,1,0,0]</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def dailyTemperatures(temperatures):
    n = len(temperatures)
    res = [0] * n
    stack = []                            # indices of cooler, unresolved days
    for i, t in enumerate(temperatures):
        while stack and temperatures[stack[-1]] &lt; t:
            j = stack.pop()
            res[j] = i - j                # days until warmer
        stack.append(i)
    return res</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong>, <strong>Space O(n)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Monotonically decreasing → all 0.</li>
<li>Last day → 0 (no warmer day after).</li>
<li>Equal temperatures → not "warmer"; keep waiting.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Using <code>≤</code> (equal isn't warmer).</li>
<li>Storing temperatures instead of indices.</li>
<li>Forgetting to leave unresolved days at 0.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Next greater element ([[496]], [[503]]).</li>
<li>Online stock span ([[901]]) uses the mirror idea.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[496]] · [[901]] · [[84]]</p>
''',

# ============================================================ LC 853 — Car Fleet
853: '''
<h2>🧭 How to think about it</h2>
<p>Cars head to the same target; a faster car catching a slower one ahead forms a <strong>fleet</strong> (it can't pass, so it travels at the slower speed). Sort cars by <strong>starting position descending</strong> (closest to target first) and compute each car's arrival <em>time</em>. A car starts a new fleet only if it arrives <em>later</em> than the fleet ahead; otherwise it joins that fleet.</p>

<h2>🐢 Brute force first</h2>
<p>Simulating positions over time is messy. Sorting by position and comparing arrival times is O(n log n).</p>

<div class="insight">💡 <strong>Key insight:</strong> process cars from nearest the target to farthest. Track the arrival time of the current leading fleet. If a car's arrival time is greater than that lead, it can't catch up → it forms a new fleet and becomes the new lead; if ≤, it merges (arrives no later, so it's blocked).</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Pair positions with speeds; sort by position descending.</li>
<li>For each car, compute <code>time = (target − position) / speed</code>.</li>
<li>If <code>time &gt; lead</code>, count a new fleet and set <code>lead = time</code>.</li>
</ol>

<h2>🎞️ Visual dry run — target=12, pos=[10,8,0,5,3], speed=[2,4,1,1,3]</h2>
<pre class="viz">sorted by pos desc: 10(t1),8(t1),5(t7),3(t3),0(t12)
lead0 ; 1&gt;0 fleet1 lead1 ; 1 not&gt;1 merge ; 7&gt;1 fleet2 lead7 ; 3 merge ; 12&gt;7 fleet3
Answer: 3</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def carFleet(target, position, speed):
    cars = sorted(zip(position, speed), reverse=True)   # nearest target first
    fleets = 0
    lead = 0.0
    for pos, spd in cars:
        time = (target - pos) / spd
        if time &gt; lead:                   # can't catch the fleet ahead
            fleets += 1
            lead = time                    # this car leads a new fleet
    return fleets</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n log n)</strong> — the sort. <strong>Space O(n)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>One car → one fleet.</li>
<li>All merge into one → 1 fleet.</li>
<li>Ties in arrival time → merge (use <code>&gt;</code>, not <code>≥</code>).</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Sorting ascending and comparing the wrong direction.</li>
<li>Using <code>≥</code> and over-counting fleets on ties.</li>
<li>Integer division losing precision on times.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Two-direction traffic → separate the lanes.</li>
<li>Report fleet membership, not just the count.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[739]] · [[735]] · [[901]]</p>
''',

# ============================================================ LC 901 — Online Stock Span
901: '''
<h2>🧭 How to think about it</h2>
<p>For each new stock price, the "span" is how many consecutive previous days (including today) had a price ≤ today's. Keep a <strong>monotonic decreasing stack</strong> of <code>(price, span)</code> pairs: when a new price meets or exceeds earlier ones, absorb their spans.</p>

<h2>🐢 Brute force first</h2>
<p>Scan back each day counting ≤ prices → O(n²) overall. The stack makes each call O(1) amortized.</p>

<div class="insight">💡 <strong>Key insight:</strong> the current day's span starts at 1; while the stack top's price ≤ today's, pop it and add its span (those days are dominated by today). Push <code>(price, accumulated span)</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>On <code>next(price)</code>: <code>span = 1</code>.</li>
<li>While the top price ≤ <code>price</code>, pop and add its span.</li>
<li>Push <code>(price, span)</code>; return <code>span</code>.</li>
</ol>

<h2>🎞️ Visual dry run — prices 100,80,60,70,60,75,85</h2>
<pre class="viz">100→1 ; 80→1 ; 60→1 ; 70 absorbs 60 → 2 ; 60→1 ; 75 absorbs 60,70 → 4 ; 85 absorbs 75,80 → 6
Spans: [1,1,1,2,1,4,6]</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>class StockSpanner:
    def __init__(self):
        self.stack = []                   # (price, span), decreasing prices

    def next(self, price):
        span = 1
        while self.stack and self.stack[-1][0] &lt;= price:
            span += self.stack.pop()[1]   # absorb dominated spans
        self.stack.append((price, span))
        return span</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(1) amortized</strong> per call. <strong>Space O(n)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Strictly increasing prices → spans grow 1,2,3,…</li>
<li>Strictly decreasing → every span is 1.</li>
<li>Equal prices → counted (≤).</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Using <code>&lt;</code> instead of <code>≤</code> (equal prior days count).</li>
<li>Storing only prices and recomputing spans.</li>
<li>Forgetting to seed the span at 1.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Daily temperatures ([[739]]) is the "next greater" mirror.</li>
<li>Sliding-window max ([[239]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[739]] · [[496]] · [[84]]</p>
''',

# ============================================================ LC 907 — Sum of Subarray Minimums
907: '''
<h2>🧭 How to think about it</h2>
<p>Sum the minimum of every subarray. Rather than enumerate subarrays, count each element's <strong>contribution</strong>: <code>nums[i]</code> is the minimum of every subarray where it's the smallest. That count is (distance to the previous smaller element) × (distance to the next smaller element), found with a <strong>monotonic stack</strong>.</p>

<h2>🐢 Brute force first</h2>
<p>All O(n²) subarray minimums → too slow. The contribution technique is O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> for each <code>i</code>, let <code>left</code> = number of subarrays extending left where <code>nums[i]</code> stays the min (up to the previous strictly-smaller element), and <code>right</code> similarly. Then <code>nums[i]</code> contributes <code>nums[i] × left × right</code>. Use "previous less" and "next less-or-equal" to avoid double counting equal values.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Compute previous-smaller and next-smaller-or-equal distances via monotonic stacks.</li>
<li>Sum <code>nums[i] × left[i] × right[i]</code> modulo 1e9+7.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [3,1,2,4]</h2>
<pre class="viz">1 is min of subarrays spanning it → big contribution
sum of all subarray minimums = 17</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def sumSubarrayMins(arr):
    MOD = 10**9 + 7
    n = len(arr)
    prev_less = [-1] * n                  # index of previous strictly smaller
    next_less = [n] * n                   # index of next smaller-or-equal
    stack = []
    for i in range(n):
        while stack and arr[stack[-1]] &gt; arr[i]:
            stack.pop()
        prev_less[i] = stack[-1] if stack else -1
        stack.append(i)
    stack = []
    for i in range(n - 1, -1, -1):
        while stack and arr[stack[-1]] &gt;= arr[i]:
            stack.pop()
        next_less[i] = stack[-1] if stack else n
        stack.append(i)
    total = 0
    for i in range(n):
        left = i - prev_less[i]
        right = next_less[i] - i
        total = (total + arr[i] * left * right) % MOD
    return total</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — two stack passes. <strong>Space O(n)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Duplicate values → the strict/non-strict split prevents double counting.</li>
<li>Sorted ascending/descending → contributions skew but stay correct.</li>
<li>Single element → its own value.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Using the same inequality on both sides → duplicates counted twice.</li>
<li>Forgetting the modulus.</li>
<li>Off-by-one in the distance boundaries.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Sum of subarray maximums → mirror the inequalities.</li>
<li>Sum of subarray ranges ([[2104]]) = maxes − mins.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[2104]] · [[84]] · [[739]]</p>
''',

# ============================================================ LC 962 — Maximum Width Ramp
962: '''
<h2>🧭 How to think about it</h2>
<p>A "ramp" is a pair <code>i &lt; j</code> with <code>nums[i] ≤ nums[j]</code>; maximize <code>j − i</code>. Build a <strong>decreasing stack of candidate left ends</strong> (only indices where the value is smaller than everything before could ever be a useful <code>i</code>). Then scan <code>j</code> from the <strong>right</strong>, popping candidates that <code>nums[j]</code> can satisfy, recording the width.</p>

<h2>🐢 Brute force first</h2>
<p>All pairs → O(n²). The candidate-stack + right scan is O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> a good left end is a "prefix minimum" position — push indices where <code>nums</code> strictly decreases. Scanning <code>j</code> from the right, while <code>nums[stack top] ≤ nums[j]</code>, that top is a valid <code>i</code> giving the widest ramp for this <code>j</code> — pop it and update the best width.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Build a stack of indices with strictly decreasing values (left-to-right).</li>
<li>For <code>j</code> from right to left: while the top's value ≤ <code>nums[j]</code>, pop and update <code>best = max(best, j − top)</code>.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [6,0,8,2,1,5]</h2>
<pre class="viz">decreasing candidates: indices 0(6),1(0)
scan j from right: j=5(5)≥0 pop1 width4 ; ≥6? no → j=2(8)≥6 pop0 width2
best = 4</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def maxWidthRamp(nums):
    stack = []
    for i, x in enumerate(nums):
        if not stack or nums[stack[-1]] &gt; x:
            stack.append(i)               # decreasing candidate left ends
    best = 0
    for j in range(len(nums) - 1, -1, -1):
        while stack and nums[stack[-1]] &lt;= nums[j]:
            best = max(best, j - stack.pop())
        if not stack:
            break
    return best</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — build then a single right scan. <strong>Space O(n)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Strictly decreasing → no ramp → 0.</li>
<li>Equal values → valid (≤).</li>
<li>Sorted ascending → width <code>n − 1</code>.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Building candidate ends with <code>≥</code> (must be strictly decreasing).</li>
<li>Scanning <code>j</code> left-to-right (misses the widest match).</li>
<li>Not stopping when the stack empties.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Max width with strict inequality → adjust the comparison.</li>
<li>Largest rectangle uses related monotonic ideas ([[84]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[84]] · [[739]] · [[496]]</p>
''',

# ============================================================ LC 1475 — Final Prices With a Special Discount in a Shop
1475: '''
<h2>🧭 How to think about it</h2>
<p>Each item's price gets discounted by the price of the <strong>next item to its right that is ≤ it</strong>. That's a "next smaller-or-equal element" query for every position — a textbook <strong>monotonic stack</strong>.</p>

<h2>🐢 Brute force first</h2>
<p>For each item scan right for the first ≤ price → O(n²). The monotonic stack is O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> keep a stack of indices whose discount isn't decided yet, with increasing prices. When a new price <code>p</code> arrives, it discounts every stacked item with price ≥ <code>p</code> — pop them and subtract.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Copy prices into the answer.</li>
<li>For each <code>i</code>: while the top item's price ≥ <code>prices[i]</code>, pop it and subtract <code>prices[i]</code>.</li>
<li>Push <code>i</code>.</li>
</ol>

<h2>🎞️ Visual dry run — prices = [8,4,6,2,3]</h2>
<pre class="viz">8 push ; 4≤8 → discount 8 by 4 → 4 ; push4? 4 discounts nothing else ; 6 push ; 2 discounts 6→4 and 4? 4≥2 discount 4→2 ...
Result: [4,2,4,2,3]</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def finalPrices(prices):
    res = prices[:]                       # default: no discount
    stack = []                            # indices with undecided discounts
    for i, p in enumerate(prices):
        while stack and prices[stack[-1]] &gt;= p:
            res[stack.pop()] -= p         # p is the discount
        stack.append(i)
    return res</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong>, <strong>Space O(n)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Strictly increasing prices → no discounts.</li>
<li>Equal prices → discount applies (≥).</li>
<li>Last item → never discounted.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Using <code>&gt;</code> instead of <code>≥</code> (equal prices should discount).</li>
<li>Forgetting to default answers to the original prices.</li>
<li>Scanning naively (O(n²)).</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Next greater element ([[496]]).</li>
<li>Daily temperatures ([[739]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[739]] · [[496]] · [[907]]</p>
''',

# ============================================================ LC 1673 — Find the Most Competitive Subsequence
1673: '''
<h2>🧭 How to think about it</h2>
<p>Pick a subsequence of length <code>k</code> that is the <strong>smallest possible</strong> in lexicographic order. Build it on a <strong>monotonic increasing stack</strong>: pop larger trailing choices when a smaller value arrives, but only if enough elements remain to still reach length <code>k</code>.</p>

<h2>🐢 Brute force first</h2>
<p>All length-k subsequences is combinatorial. The greedy stack with a remaining-count guard is O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> a smaller earlier digit makes the subsequence more competitive. While the stack top &gt; current value AND there are enough remaining elements (<code>len(stack) − 1 + (n − i) ≥ k</code>) to still fill <code>k</code>, pop. Push while the stack has room. The answer is the first <code>k</code> stacked values.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>For each index <code>i</code> with value <code>x</code>: while the top &gt; <code>x</code> and dropping it still allows reaching length <code>k</code>, pop.</li>
<li>Push <code>x</code> if the stack has fewer than <code>k</code> elements.</li>
<li>Return the stack (length <code>k</code>).</li>
</ol>

<h2>🎞️ Visual dry run — nums = [3,5,2,6], k = 2</h2>
<pre class="viz">3 push ; 5 push [3,5] ; 2: pop5 (room), pop3 (room) → [2] ; 6 push [2,6]
Result: [2,6]</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def mostCompetitive(nums, k):
    n = len(nums)
    stack = []
    for i, x in enumerate(nums):
        # pop while bigger and enough elements remain to fill k
        while stack and stack[-1] &gt; x and len(stack) - 1 + (n - i) &gt;= k:
            stack.pop()
        if len(stack) &lt; k:
            stack.append(x)
    return stack</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong>, <strong>Space O(k)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>k = n → the whole array.</li>
<li>Already increasing → the first k elements.</li>
<li>Many duplicates → strict <code>&gt;</code> avoids needless pops.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Popping without the "enough remaining" guard → can't reach length k.</li>
<li>Pushing beyond k elements.</li>
<li>Using <code>≥</code> and dropping equal values unnecessarily.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Remove k digits for the smallest number ([[402]]).</li>
<li>Remove duplicate letters ([[316]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[402]] · [[316]] · [[456]]</p>
''',

# ============================================================ LC 1944 — Number of Visible People in a Queue
1944: '''
<h2>🧭 How to think about it</h2>
<p>Person <code>i</code> can see person <code>j</code> to their right if everyone strictly between them is shorter than both. Count, for each person, how many they can see. Scan from the <strong>right</strong> with a <strong>monotonic decreasing stack</strong> of heights: each shorter person on the stack is visible, and the first taller one is also visible (but blocks further view).</p>

<h2>🐢 Brute force first</h2>
<p>For each person scan right tracking the running max → O(n²). The stack does it in O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> processing right to left, the stack holds a decreasing sequence of heights (the currently visible people ahead). For person <code>i</code>: pop everyone shorter (each counts as visible); if a taller person remains, they're visible too (+1) but stop the view. Then push <code>i</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Traverse right to left with a decreasing stack.</li>
<li>For height <code>h</code>: while the top &lt; <code>h</code>, pop (count each). If the stack is still non-empty, add 1 more (the taller blocker).</li>
<li>Push <code>h</code>.</li>
</ol>

<h2>🎞️ Visual dry run — heights = [10,6,8,5,11,9]</h2>
<pre class="viz">from right: 9 ; 11 sees 9 → 1 ; 5 sees 11 → 1 ; 8 sees 5, then 11 → 2 ; 6 sees 8 → 1 ; 10 sees 6,8, then 11 → 3
Result: [3,1,2,1,1,0]</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def canSeePersonsCount(heights):
    n = len(heights)
    res = [0] * n
    stack = []                            # decreasing heights to the right
    for i in range(n - 1, -1, -1):
        h = heights[i]
        while stack and stack[-1] &lt; h:
            stack.pop()
            res[i] += 1                   # shorter person is visible
        if stack:
            res[i] += 1                   # the first taller person, then blocked
        stack.append(h)
    return res</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong>, <strong>Space O(n)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Increasing heights → each sees only the next.</li>
<li>Decreasing heights → each sees everyone to the right.</li>
<li>Last person → sees 0.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Forgetting the "+1 for the blocker" when a taller person remains.</li>
<li>Scanning left to right (harder to reason about visibility).</li>
<li>Off-by-one at the array end.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Buildings with a sunset view (LC 1762).</li>
<li>Daily temperatures ([[739]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[739]] · [[496]] · [[901]]</p>
''',

# ============================================================ LC 2104 — Sum of Subarray Ranges
2104: '''
<h2>🧭 How to think about it</h2>
<p>The "range" of a subarray is its max minus its min; sum ranges over all subarrays. Since <code>Σ range = Σ max − Σ min</code>, compute the <strong>sum of subarray maximums</strong> and the <strong>sum of subarray minimums</strong> separately, each with a monotonic-stack contribution technique ([[907]]).</p>

<h2>🐢 Brute force first</h2>
<p>All O(n²) subarrays tracking running max/min → O(n²) (fine for small n). The two contribution passes give O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> each element contributes to the max-sum over the subarrays where it's the maximum, and to the min-sum where it's the minimum. Compute both with previous/next boundary distances; the answer is <code>maxSum − minSum</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Sum of subarray maximums via monotonic stacks (previous/next greater).</li>
<li>Sum of subarray minimums via monotonic stacks (previous/next smaller).</li>
<li>Return the difference.</li>
</ol>

<h2>🎞️ Visual dry run — nums = [1,2,3]</h2>
<pre class="viz">subarray ranges: [1]0 [2]0 [3]0 [1,2]1 [2,3]1 [1,2,3]2 → sum 4</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def subArrayRanges(nums):
    n = len(nums)
    def sum_extreme(sign):
        # sign=+1 → sum of maxs ; sign=-1 → sum of mins (apply to -nums)
        a = [sign * x for x in nums]
        prev = [-1] * n; nxt = [n] * n; stack = []
        for i in range(n):
            while stack and a[stack[-1]] &lt; a[i]:
                stack.pop()
            prev[i] = stack[-1] if stack else -1
            stack.append(i)
        stack = []
        for i in range(n - 1, -1, -1):
            while stack and a[stack[-1]] &lt;= a[i]:
                stack.pop()
            nxt[i] = stack[-1] if stack else n
            stack.append(i)
        return sum(a[i] * (i - prev[i]) * (nxt[i] - i) for i in range(n))
    return sum_extreme(1) + sum_extreme(-1)   # maxSum - minSum (via -nums)</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — four stack passes. <strong>Space O(n)</strong>. (A simple O(n²) double loop is also accepted for small inputs.)</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Single element → range 0.</li>
<li>All equal → total 0.</li>
<li>Duplicates → strict/non-strict split avoids double counting.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Mixing strict and non-strict inequalities inconsistently between the two sums.</li>
<li>Forgetting that min-sum can be computed by negating and reusing the max-sum code.</li>
<li>Overflow in fixed-width languages.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Sum of subarray minimums alone ([[907]]).</li>
<li>Sum of subarray maximums alone.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[907]] · [[84]] · [[739]]</p>
''',

# ============================================================ LC 150 — Evaluate Reverse Polish Notation
150: '''
<h2>🧭 How to think about it</h2>
<p>Reverse Polish Notation (postfix) puts operators after their operands, so there are no parentheses. A <strong>stack of operands</strong> evaluates it directly: push numbers; on an operator, pop the top two, apply, and push the result.</p>

<h2>🐢 Brute force first</h2>
<p>Converting to infix and parsing is overkill. The single stack pass is O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> in postfix, when you hit an operator the two most recent values are its operands. Mind the order (<code>b</code> is on top, <code>a</code> below): compute <code>a op b</code>. Integer division must truncate toward zero.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>For each token: a number → push; an operator → pop <code>b</code>, pop <code>a</code>, push <code>a op b</code>.</li>
<li>The final stack value is the answer.</li>
</ol>

<h2>🎞️ Visual dry run — ["2","1","+","3","*"]</h2>
<pre class="viz">2 ; 1 ; + → pop1,2 push3 ; 3 ; * → pop3,3 push9
Answer: 9</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def evalRPN(tokens):
    stack = []
    ops = {'+', '-', '*', '/'}
    for t in tokens:
        if t in ops:
            b = stack.pop()
            a = stack.pop()
            if t == '+': stack.append(a + b)
            elif t == '-': stack.append(a - b)
            elif t == '*': stack.append(a * b)
            else: stack.append(int(a / b))    # truncate toward zero
        else:
            stack.append(int(t))
    return stack[0]</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong>, <strong>Space O(n)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Negative results from division → truncate toward zero (<code>int(a/b)</code>, not floor).</li>
<li>Single number token → that number.</li>
<li>Negative number tokens → parse with <code>int</code>.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Swapping operand order for <code>−</code> and <code>/</code>.</li>
<li>Using floor division for negatives (should truncate toward zero).</li>
<li>Treating negative-number tokens as operators.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Infix with parentheses ([[224]], [[227]], [[772]]).</li>
<li>Convert infix → postfix (shunting yard).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[224]] · [[227]] · [[772]]</p>
''',

# ============================================================ LC 224 — Basic Calculator
224: '''
<h2>🧭 How to think about it</h2>
<p>Evaluate an expression with <code>+</code>, <code>−</code>, and <strong>parentheses</strong> (no <code>×</code>/<code>÷</code>). Keep a running <code>result</code> and current <code>sign</code>; when you hit <code>'('</code>, push the state and start fresh; on <code>')'</code>, fold the sub-result back in. A single stack of saved <code>(result, sign)</code> handles arbitrary nesting.</p>

<h2>🐢 Brute force first</h2>
<p>Recursive descent parsing works but is heavier to write. The one-pass stack is O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> accumulate numbers digit by digit. On <code>+</code>/<code>−</code>, add <code>sign × number</code> to <code>result</code> and set the new sign. On <code>'('</code>, push <code>result</code> and <code>sign</code>, then reset. On <code>')'</code>, finish the inner number, then <code>result = result × savedSign + savedResult</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Track <code>result</code>, <code>sign</code>, and a current <code>number</code>.</li>
<li>Digit → build the number. <code>+/−</code> → fold it in, set sign. <code>(</code> → push (result, sign), reset. <code>)</code> → fold, then combine with the pushed state.</li>
</ol>

<h2>🎞️ Visual dry run — "(1+(4+5+2)-3)"</h2>
<pre class="viz">inner (4+5+2)=11 ; 1+11=12 ; 12-3=9
Answer: 9</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def calculate(s):
    result = 0
    number = 0
    sign = 1
    stack = []
    for c in s:
        if c.isdigit():
            number = number * 10 + int(c)
        elif c in '+-':
            result += sign * number       # commit the previous number
            number = 0
            sign = 1 if c == '+' else -1
        elif c == '(':
            stack.append(result); stack.append(sign)   # save state
            result = 0; sign = 1
        elif c == ')':
            result += sign * number
            number = 0
            result = result * stack.pop() + stack.pop() # sign then result
    return result + sign * number</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong>, <strong>Space O(n)</strong> for nesting.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Leading unary minus (e.g., <code>"-2+1"</code>) → sign starts handling it.</li>
<li>Spaces → skipped (non-digit, non-operator).</li>
<li>Deep nesting → the stack scales.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Popping sign and result in the wrong order.</li>
<li>Forgetting to commit the last number after the loop.</li>
<li>Not resetting <code>number</code> after committing.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Add <code>×</code>/<code>÷</code> ([[227]]) or both plus parens ([[772]]).</li>
<li>Postfix evaluation ([[150]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[227]] · [[772]] · [[150]]</p>
''',

# ============================================================ LC 227 — Basic Calculator II
227: '''
<h2>🧭 How to think about it</h2>
<p>Evaluate an expression with <code>+ − × ÷</code> and no parentheses, respecting precedence. Use a <strong>stack of terms</strong>: <code>+</code>/<code>−</code> push the (signed) number to be added later, while <code>×</code>/<code>÷</code> combine <em>immediately</em> with the top of the stack. The answer is the sum of the stack.</p>

<h2>🐢 Brute force first</h2>
<p>Two passes (handle ×/÷ first, then +/−) works. The single stack pass fuses them in O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> track the operator <em>before</em> the current number. When you finish a number: if the previous op was <code>+</code>/<code>−</code>, push <code>±number</code>; if it was <code>×</code>/<code>÷</code>, pop the top and push <code>top × number</code> or <code>int(top / number)</code>. Summing the stack respects precedence.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Iterate, building each number; remember the operator that preceded it (default <code>+</code>).</li>
<li>On an operator or end: apply the previous operator to the number against the stack.</li>
<li>Return <code>sum(stack)</code>.</li>
</ol>

<h2>🎞️ Visual dry run — "3+2*2"</h2>
<pre class="viz">3 → push3 ; op + ; 2 → op was + push2 ; op * ; 2 → op * pop2 push 2*2=4
stack [3,4] sum 7</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def calculate(s):
    stack = []
    number = 0
    op = '+'                              # operator preceding the current number
    for i, c in enumerate(s):
        if c.isdigit():
            number = number * 10 + int(c)
        if c in '+-*/' or i == len(s) - 1:
            if op == '+': stack.append(number)
            elif op == '-': stack.append(-number)
            elif op == '*': stack.append(stack.pop() * number)
            else: stack.append(int(stack.pop() / number))  # truncate toward zero
            op = c
            number = 0
    return sum(stack)</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong>, <strong>Space O(n)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Spaces → skipped (only digits/operators act).</li>
<li>Division truncates toward zero, including negatives.</li>
<li>Trailing number at the end → the <code>i == len−1</code> trigger commits it.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Not committing the final number (handle the last index).</li>
<li>Using floor division for negatives.</li>
<li>Applying precedence with two passes but mismanaging signs.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Add parentheses ([[772]]).</li>
<li>Only + − with parens ([[224]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[224]] · [[772]] · [[150]]</p>
''',

# ============================================================ LC 394 — Decode String
394: '''
<h2>🧭 How to think about it</h2>
<p>Decode strings like <code>3[a2[c]]</code> into <code>accaccacc</code>. Nested repeats call for a <strong>stack</strong>: push the current build state and repeat count when you hit <code>'['</code>, and on <code>']'</code> pop and append the just-built segment repeated.</p>

<h2>🐢 Brute force first</h2>
<p>Recursion mirrors the nesting and is equally valid. The explicit stack avoids deep call stacks and is O(total output).</p>

<div class="insight">💡 <strong>Key insight:</strong> keep a running <code>current</code> string and <code>num</code>. On <code>'['</code>, push <code>(current, num)</code> and reset. On <code>']'</code>, pop <code>(prev, k)</code> and set <code>current = prev + current × k</code>. Digits accumulate into <code>num</code>; letters append to <code>current</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Track <code>current</code> (string) and <code>num</code> (count).</li>
<li>Digit → build <code>num</code>. <code>'['</code> → push state, reset. <code>']'</code> → pop and expand. Letter → append.</li>
</ol>

<h2>🎞️ Visual dry run — "3[a2[c]]"</h2>
<pre class="viz">num3 ( push ("",3) ) ; a → "a" ; num2 ( push("a",2) ) ; c → "c" ; ] → "a"+"c"*2="acc" ; ] → ""+"acc"*3
Answer: "accaccacc"</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def decodeString(s):
    stack = []
    current = ""
    num = 0
    for c in s:
        if c.isdigit():
            num = num * 10 + int(c)
        elif c == '[':
            stack.append((current, num))  # save context
            current = ""; num = 0
        elif c == ']':
            prev, k = stack.pop()
            current = prev + current * k  # expand the segment
        else:
            current += c
    return current</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(total output length)</strong>. <strong>Space O(depth + output)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Multi-digit counts (e.g., <code>12[a]</code>).</li>
<li>Nested brackets → the stack handles arbitrary depth.</li>
<li>Plain letters without brackets → returned as-is.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Resetting <code>num</code> or <code>current</code> at the wrong moment.</li>
<li>Multiplying by the wrong saved count.</li>
<li>Only handling single-digit counts.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Encode a string with run-length + brackets.</li>
<li>Evaluate nested expressions ([[772]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[224]] · [[772]] · [[20]]</p>
''',

# ============================================================ LC 772 — Basic Calculator III
772: '''
<h2>🧭 How to think about it</h2>
<p>The full calculator: <code>+ − × ÷</code> <strong>and</strong> parentheses. Combine the ideas from [[227]] (precedence via a term stack) and [[224]] (parentheses). The cleanest structure is a <strong>recursive evaluator</strong> that processes a parenthesized group by recursing, returning both its value and where it ended.</p>

<h2>🐢 Brute force first</h2>
<p>Convert to postfix then evaluate is two steps. A single recursive/stack evaluator does it in one O(n) pass.</p>

<div class="insight">💡 <strong>Key insight:</strong> reuse the [[227]] term-stack for precedence within a level; when you meet <code>'('</code>, recurse to evaluate the inner expression and treat its result as a number; when you meet <code>')'</code>, finish the current level and return. Division truncates toward zero.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Parse with an index pointer; maintain a stack of terms and the pending operator.</li>
<li><code>'('</code> → recurse from the next index; use the returned value as the current number.</li>
<li><code>')'</code> or end → commit the last term and return <code>sum(stack)</code> with the position.</li>
</ol>

<h2>🎞️ Visual dry run — "2*(5+5*2)/3+(6/2+8)"</h2>
<pre class="viz">inner (5+5*2)=15 ; 2*15/3 = 10 ; inner (6/2+8)=11 ; 10+11 = 21
Answer: 21</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def calculate(s):
    def helper(i):
        stack = []
        num = 0
        op = '+'
        while i &lt; len(s):
            c = s[i]
            if c.isdigit():
                num = num * 10 + int(c)
            elif c == '(':
                num, i = helper(i + 1)     # evaluate the inner group
            if c in '+-*/)' or i == len(s) - 1:
                if op == '+': stack.append(num)
                elif op == '-': stack.append(-num)
                elif op == '*': stack.append(stack.pop() * num)
                elif op == '/': stack.append(int(stack.pop() / num))
                num = 0; op = c
                if c == ')':
                    return sum(stack), i    # return value and position
            i += 1
        return sum(stack), i
    return helper(0)[0]</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong>, <strong>Space O(n)</strong> for recursion/stack.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Nested parentheses → recursion handles depth.</li>
<li>Spaces → ignored.</li>
<li>Division truncates toward zero.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Not returning the updated index from the recursive group.</li>
<li>Mishandling the operator that follows a closing parenthesis.</li>
<li>Floor division on negatives.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Only +−() ([[224]]) or only +−×÷ ([[227]]).</li>
<li>Support exponentiation / functions.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[224]] · [[227]] · [[150]]</p>
''',

# ============================================================ LC 636 — Exclusive Time of Functions
636: '''
<h2>🧭 How to think about it</h2>
<p>Given function start/end logs for a single-threaded program, compute each function's <strong>exclusive</strong> run time (time spent in it but not in nested calls). The call structure is a stack: a "start" pushes a function; an "end" pops it. Track the <strong>previous timestamp</strong> to charge elapsed time to whatever's on top.</p>

<h2>🐢 Brute force first</h2>
<p>There's no simpler correct method than simulating the call stack; it's O(number of logs).</p>

<div class="insight">💡 <strong>Key insight:</strong> maintain a stack of active function IDs and <code>prev_time</code>. On a <code>start</code> at time <code>t</code>: add <code>t − prev</code> to the current top (it ran until now), push the new function, set <code>prev = t</code>. On an <code>end</code> at time <code>t</code>: add <code>t − prev + 1</code> to the popped function, set <code>prev = t + 1</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Parse each log into <code>(id, type, time)</code>.</li>
<li><code>start</code> → charge elapsed to the top, push id, update prev.</li>
<li><code>end</code> → charge elapsed (+1 inclusive) to the popped id, update prev to <code>time+1</code>.</li>
</ol>

<h2>🎞️ Visual dry run — logs: 0:start:0, 1:start:2, 1:end:5, 0:end:6</h2>
<pre class="viz">start0@0 prev0 ; start1@2 → f0 += 2-0=2, push1, prev2 ; end1@5 → f1 += 5-2+1=4, prev6 ; end0@6 → f0 += 6-6+1=1
f0=3, f1=4</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def exclusiveTime(n, logs):
    res = [0] * n
    stack = []
    prev = 0
    for log in logs:
        fid, typ, t = log.split(':')
        fid, t = int(fid), int(t)
        if typ == 'start':
            if stack:
                res[stack[-1]] += t - prev     # top ran until now
            stack.append(fid)
            prev = t
        else:  # end
            res[stack.pop()] += t - prev + 1   # inclusive of this tick
            prev = t + 1
    return res</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(number of logs)</strong>, <strong>Space O(depth)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Recursive calls (same id nested) → stack still tracks each activation.</li>
<li>Back-to-back calls → the <code>+1</code> and <code>prev = t + 1</code> keep ticks from double-counting.</li>
<li>Single function → its full span.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Off-by-one: end times are inclusive (<code>+1</code>), starts are not.</li>
<li>Forgetting to charge the top when a nested call starts.</li>
<li>Not updating <code>prev</code> to <code>t + 1</code> after an end.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Multi-threaded logs → per-thread stacks.</li>
<li>Inclusive time (with children) → simpler accounting.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[224]] · [[20]] · [[155]]</p>
''',

# ============================================================ LC 895 — Maximum Frequency Stack
895: '''
<h2>🧭 How to think about it</h2>
<p>Design a stack where <code>pop()</code> removes the <strong>most frequent</strong> element (ties broken by most recently pushed). Track each value's frequency, and keep a <strong>stack per frequency level</strong>: pushing a value adds it to the stack for its new frequency; popping takes from the highest non-empty frequency stack.</p>

<h2>🐢 Brute force first</h2>
<p>Scanning for the max frequency on each pop is O(n). The per-frequency stacks make push and pop O(1).</p>

<div class="insight">💡 <strong>Key insight:</strong> when you push <code>x</code> and its count becomes <code>f</code>, append <code>x</code> to <code>groups[f]</code>. The current maximum frequency <code>maxFreq</code> points at the stack to pop from; popping from <code>groups[maxFreq]</code> gives the most-frequent, most-recent value and naturally handles ties (recency within the group).</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>push(x)</code>: increment <code>freq[x]</code>; append <code>x</code> to <code>groups[freq[x]]</code>; bump <code>maxFreq</code>.</li>
<li><code>pop()</code>: take from <code>groups[maxFreq]</code>; decrement that value's freq; if the top group empties, lower <code>maxFreq</code>.</li>
</ol>

<h2>🎞️ Visual dry run — push 5,7,5,7,4,5 then pop×3</h2>
<pre class="viz">freq5=3 (groups[3]=[5]) ; pop → 5 (maxFreq2) ; pop → 7 (freq7 was 2, recent) ; pop → 5
Pops: 5, 7, 5</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>from collections import defaultdict
class FreqStack:
    def __init__(self):
        self.freq = defaultdict(int)
        self.groups = defaultdict(list)   # frequency -> stack of values
        self.max_freq = 0

    def push(self, val):
        self.freq[val] += 1
        f = self.freq[val]
        self.max_freq = max(self.max_freq, f)
        self.groups[f].append(val)

    def pop(self):
        val = self.groups[self.max_freq].pop()   # most frequent, most recent
        self.freq[val] -= 1
        if not self.groups[self.max_freq]:
            self.max_freq -= 1
        return val</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(1)</strong> per push/pop. <strong>Space O(n)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Ties in frequency → the group's top (most recent) wins.</li>
<li>Single element pushed many times → pops it repeatedly.</li>
<li>Interleaved pushes/pops → <code>max_freq</code> stays correct.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Forgetting to lower <code>max_freq</code> when the top group empties.</li>
<li>Not decrementing <code>freq[val]</code> on pop.</li>
<li>Using one global stack and re-sorting (O(n) pops).</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Least frequent element → track min frequency similarly.</li>
<li>LFU cache uses the same frequency-bucket idea.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[155]] · [[347]] · [[146]]</p>
''',

# ============================================================ LC 155 — Min Stack
155: '''
<h2>🧭 How to think about it</h2>
<p>Support push/pop/top plus <code>getMin</code>, all in O(1). The trick is to store, alongside each value, the <strong>minimum of the stack at that moment</strong>. Then the current minimum is always just the top's stored min.</p>

<h2>🐢 Brute force first</h2>
<p>Scanning for the min on each <code>getMin</code> is O(n). Pairing each element with its running min makes it O(1).</p>

<div class="insight">💡 <strong>Key insight:</strong> push <code>(val, min(val, currentMin))</code>. Popping restores the previous min automatically because it was stored with the element below. <code>getMin</code> reads the top's stored min.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>push(x)</code>: new min = <code>min(x, top's min)</code>; push <code>(x, newMin)</code>.</li>
<li><code>pop</code>/<code>top</code>: operate on the value component.</li>
<li><code>getMin</code>: return the top's min component.</li>
</ol>

<h2>🎞️ Visual dry run — push -2, 0, -3; getMin; pop; top; getMin</h2>
<pre class="viz">(-2,-2) (0,-2) (-3,-3) → getMin -3 ; pop → top 0 ; getMin -2</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>class MinStack:
    def __init__(self):
        self.stack = []                   # (value, min_so_far)

    def push(self, val):
        cur_min = val if not self.stack else min(val, self.stack[-1][1])
        self.stack.append((val, cur_min))

    def pop(self):
        self.stack.pop()

    def top(self):
        return self.stack[-1][0]

    def getMin(self):
        return self.stack[-1][1]</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(1)</strong> per operation. <strong>Space O(n)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Duplicate minimums → each element carries the correct running min.</li>
<li>Pop down to empty → the paired min disappears with the value.</li>
<li>Single element → its own min.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Keeping a single min variable that can't restore after popping the min.</li>
<li>Recomputing the min by scanning.</li>
<li>Mismatching value vs min components.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>O(1) space overhead trick storing encoded diffs.</li>
<li>Max stack, or a queue with min (monotonic deque).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[232]] · [[895]] · [[239]]</p>
''',

# ============================================================ LC 84 — Largest Rectangle in Histogram
84: '''
<h2>🧭 How to think about it</h2>
<p>Find the largest rectangle fitting under a histogram's bars. For each bar, the widest rectangle of its height stretches left and right until it hits a shorter bar. A <strong>monotonic increasing stack</strong> of indices lets you settle each bar's rectangle exactly when a shorter bar appears.</p>

<h2>🐢 Brute force first</h2>
<p>For each bar expand outward for the height limit → O(n²). The monotonic stack does it in O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> keep indices of bars in increasing height. When a shorter bar arrives, pop taller bars and "settle" each: its height is the popped bar's height, and its width spans from the new stack top (its previous smaller bar) to the current index. A sentinel 0 at the end flushes the stack.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Iterate with a stack of indices (increasing heights); append a virtual 0 at the end.</li>
<li>While the current bar is shorter than the stack top, pop and compute <code>height × width</code>.</li>
<li>Track the maximum area.</li>
</ol>

<h2>🎞️ Visual dry run — heights = [2,1,5,6,2,3]</h2>
<pre class="viz">bar 5,6 form 5×2=10 when 2 arrives ; overall best rectangle area = 10</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def largestRectangleArea(heights):
    stack = []                            # indices, increasing heights
    best = 0
    for i in range(len(heights) + 1):
        cur = heights[i] if i &lt; len(heights) else 0   # sentinel flushes stack
        while stack and heights[stack[-1]] &gt;= cur:
            height = heights[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            best = max(best, height * width)
        stack.append(i)
    return best</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — each index pushed/popped once. <strong>Space O(n)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Increasing heights → the sentinel settles everything at the end.</li>
<li>All equal → area = height × n.</li>
<li>Single bar → its own area.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Width formula off-by-one (use <code>i − stack[-1] − 1</code> after popping).</li>
<li>Forgetting the trailing sentinel to flush remaining bars.</li>
<li>Using <code>&gt;</code> vs <code>≥</code> inconsistently with equal heights.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Maximal rectangle in a binary matrix ([[85]]).</li>
<li>Largest square → DP ([[221]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[85]] · [[907]] · [[739]]</p>
''',
}
