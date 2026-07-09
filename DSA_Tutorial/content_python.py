# Python Primer pages — original tutorial content. body is HTML injected into the page shell.

PAGES = [
# ============================================================ PY-1
{'id': 'py-1-how-python-thinks', 'short': 'How Python Thinks', 'title': 'PY-1 · How Python Thinks: Variables, Truthiness & Loops',
 'blurb': 'References, mutability, truthiness, and the loop idioms every solution uses.',
 'body': '''
<p>Before any data structure, you need to know what Python is actually doing when you write a line of code. Three ideas explain 90% of beginner bugs: <strong>everything is a reference</strong>, <strong>some objects can change and some cannot</strong>, and <strong>every value is secretly True or False</strong>.</p>

<h2>1. Variables are name-tags, not boxes</h2>
<p>In Python a variable does not "contain" a value. It is a name-tag tied onto an object. Two names can point at the <em>same</em> object:</p>
<pre><code>a = [1, 2, 3]
b = a          # b is another name for the SAME list, not a copy
b.append(4)
print(a)       # [1, 2, 3, 4]  ← a changed too!</code></pre>
<div class="warn"><strong>Classic interview bug:</strong> building a 2-D grid with <code>grid = [[0]*3]*3</code>. All three rows are the <em>same</em> list, so writing <code>grid[0][0]=1</code> changes every row. Correct: <code>grid = [[0]*3 for _ in range(3)]</code>.</div>
<p>To copy a list: <code>b = a[:]</code> or <code>b = list(a)</code> (shallow) or <code>copy.deepcopy(a)</code> (nested structures).</p>

<h2>2. Mutable vs immutable</h2>
<table><tr><th>Immutable (cannot change)</th><th>Mutable (can change in place)</th></tr>
<tr><td><code>int, float, str, tuple, frozenset, bool</code></td><td><code>list, dict, set, deque, custom objects</code></td></tr></table>
<p>Why it matters: only <strong>immutable</strong> things can be dictionary keys or set members (they must have a stable hash). Strings being immutable means <code>s += ch</code> in a loop copies the whole string every time — O(n²) total. Build a list and <code>''.join()</code> it instead.</p>

<h2>3. Truthiness — the hidden if</h2>
<p>Every value converts to True/False. These are False: <code>0, 0.0, "", [], {{}}, set(), None, False</code>. Everything else is True. That's why Pythonic code says:</p>
<pre><code>if not stack:          # stack is empty
if node:               # node is not None
while queue:           # keep going until queue is empty</code></pre>
<div class="warn"><code>if not x</code> is True for BOTH <code>x = None</code> and <code>x = 0</code>. When 0 is a legal value (e.g. index or count), test explicitly: <code>if x is None</code>.</div>

<h2>4. Loop idioms you will use constantly</h2>
<pre><code>for i in range(n):            # 0, 1, ..., n-1
for i in range(n-1, -1, -1):  # n-1, ..., 1, 0  (backwards)
for i, v in enumerate(nums):  # index AND value together
for a, b in zip(xs, ys):      # walk two lists in lockstep
for k, v in d.items():        # dict keys and values

# swap without a temp variable — used in every two-pointer problem
nums[i], nums[j] = nums[j], nums[i]

# multiple assignment — used in Fibonacci/DP all the time
prev, curr = curr, prev + curr</code></pre>

<h2>5. Integer behavior (no overflow!)</h2>
<p>Python ints grow without limit — no 32-bit overflow like Java/C++. Interviewers may still ask about overflow; know that <code>2**31 - 1</code> is the classic INT_MAX. Division: <code>7 / 2 == 3.5</code> (true division), <code>7 // 2 == 3</code> (floor), <code>7 % 2 == 1</code> (modulo). Careful: <code>-7 // 2 == -4</code> (floors toward negative infinity, not toward zero). <code>divmod(7, 2)</code> returns <code>(3, 1)</code>.</p>

<h2>6. Comparison chaining &amp; conditional expression</h2>
<pre><code>if 0 <= i < n:                 # bounds check in one shot
best = a if a > b else b       # ternary
x = y or default               # y if y is truthy, else default</code></pre>

<div class="tip"><strong>Self-check:</strong> Why does <code>a = b = []</code> then <code>a.append(1)</code> make <code>b == [1]</code>? (Answer: both names tag the same list object.)</div>
'''},

# ============================================================ PY-2
{'id': 'py-2-builtin-functions', 'short': 'Built-in Functions', 'title': 'PY-2 · The Built-in Functions That Solve Problems',
 'blurb': 'len, sorted, min/max, sum, any/all, map/filter, enumerate, zip — with complexities.',
 'body': '''
<p>These functions are pre-loaded — no import needed. Knowing them cold is the difference between a 5-line solution and a 25-line one. Complexities matter: interviewers expect you to know that <code>sorted</code> is O(n log n) and <code>len</code> is O(1).</p>

<h2>The core table</h2>
<table>
<tr><th>Function</th><th>What it does</th><th>Complexity</th><th>Interview use</th></tr>
<tr><td><code>len(x)</code></td><td>number of items</td><td>O(1) — stored, not counted</td><td>everywhere</td></tr>
<tr><td><code>sorted(x)</code></td><td>NEW sorted list (any iterable)</td><td>O(n log n)</td><td>intervals, greedy</td></tr>
<tr><td><code>x.sort()</code></td><td>sorts list in place, returns None</td><td>O(n log n)</td><td>when original order not needed</td></tr>
<tr><td><code>min(x) / max(x)</code></td><td>smallest / largest</td><td>O(n)</td><td>with <code>key=</code>, very powerful</td></tr>
<tr><td><code>sum(x)</code></td><td>total</td><td>O(n)</td><td>prefix sums, averages</td></tr>
<tr><td><code>abs(x)</code></td><td>absolute value</td><td>O(1)</td><td>distances</td></tr>
<tr><td><code>any(it)</code></td><td>True if ANY element truthy (stops early)</td><td>O(n) worst</td><td>existence checks</td></tr>
<tr><td><code>all(it)</code></td><td>True if ALL truthy (stops early)</td><td>O(n) worst</td><td>validation</td></tr>
<tr><td><code>enumerate(x)</code></td><td>yields (index, value)</td><td>O(1) per step</td><td>replaces manual counters</td></tr>
<tr><td><code>zip(a, b)</code></td><td>pairs items up, stops at shorter</td><td>O(1) per step</td><td>compare two sequences</td></tr>
<tr><td><code>reversed(x)</code></td><td>iterator over x backwards</td><td>O(1) to create</td><td>palindromes</td></tr>
<tr><td><code>range(a, b, s)</code></td><td>lazy number sequence</td><td>O(1) memory</td><td>all loops</td></tr>
<tr><td><code>map(f, x)</code></td><td>lazily apply f to each</td><td>O(1) per step</td><td>parsing input</td></tr>
<tr><td><code>filter(f, x)</code></td><td>lazily keep items where f is True</td><td>O(1) per step</td><td>cleaning data</td></tr>
<tr><td><code>round(x, d)</code></td><td>round to d decimals</td><td>O(1)</td><td>output formatting</td></tr>
<tr><td><code>pow(a, b, m)</code></td><td>aᵇ mod m, FAST</td><td>O(log b)</td><td>number theory</td></tr>
<tr><td><code>ord(c) / chr(i)</code></td><td>char ↔ unicode number</td><td>O(1)</td><td>letter math: <code>ord(c)-ord('a')</code></td></tr>
<tr><td><code>bin(x) / hex(x)</code></td><td>binary/hex string of x</td><td>O(log x)</td><td>bit manipulation</td></tr>
<tr><td><code>isinstance(x, T)</code></td><td>type check</td><td>O(1)</td><td>nested structures</td></tr>
<tr><td><code>id(x)</code></td><td>object identity</td><td>O(1)</td><td>debugging references</td></tr>
</table>

<h2>The <code>key=</code> superpower</h2>
<p><code>sorted</code>, <code>min</code>, and <code>max</code> all accept a <code>key</code> function — "judge each item by this value instead":</p>
<pre><code>sorted(words, key=len)                     # shortest → longest
sorted(points, key=lambda p: p[0]**2 + p[1]**2)   # by distance from origin
sorted(intervals, key=lambda iv: iv[0])    # intervals by start — the #1 intervals move
max(freq, key=freq.get)                    # dict key with the highest value
sorted(s)                                  # chars of a string, sorted → anagram signature</code></pre>
<p>Sort descending: <code>sorted(x, reverse=True)</code>. Sort by two criteria: return a tuple — <code>key=lambda w: (-count[w], w)</code> means "count descending, then alphabetical". Python's sort is <strong>stable</strong>: equal keys keep their original order.</p>

<h2>Building collections from iterables</h2>
<pre><code>list("abc")      # ['a', 'b', 'c']
set(nums)        # dedupe in O(n)
dict(pairs)      # from [(k, v), ...]
tuple(nums)      # hashable version of a list (usable as dict key!)
''.join(chars)   # list of strings → one string, O(total length)
str(123), int("42"), int("ff", 16)         # conversions</code></pre>

<h2>Input parsing one-liners (for non-LeetCode judges)</h2>
<pre><code>n = int(input())
nums = list(map(int, input().split()))
a, b = map(int, input().split())</code></pre>

<div class="tip"><strong>Rule of thumb:</strong> if you are writing a manual loop to find a max, a sum, a count, or a check — a built-in probably does it in one readable line with the same complexity.</div>
'''},

# ============================================================ PY-3
{'id': 'py-3-data-structures', 'short': 'Core Data Structures', 'title': 'PY-3 · list, tuple, dict, set — Every Operation & Its Cost',
 'blurb': 'The four built-in structures with the complexity of every operation.',
 'body': '''
<p>Four structures cover most interview code. For each, you must know every operation <em>and its cost</em> — choosing the wrong structure is the most common reason a correct algorithm times out.</p>

<h2>1. list — dynamic array</h2>
<p>A resizable array. Fast at the <strong>end</strong>, slow at the <strong>front</strong> (everything must shift).</p>
<table>
<tr><th>Operation</th><th>Code</th><th>Cost</th></tr>
<tr><td>index / assign</td><td><code>a[i]</code>, <code>a[i]=v</code></td><td>O(1)</td></tr>
<tr><td>append at end</td><td><code>a.append(v)</code></td><td>O(1) amortized</td></tr>
<tr><td>pop end</td><td><code>a.pop()</code></td><td>O(1)</td></tr>
<tr><td>pop front / insert front</td><td><code>a.pop(0)</code>, <code>a.insert(0,v)</code></td><td><strong>O(n) — avoid! use deque</strong></td></tr>
<tr><td>insert middle / delete</td><td><code>a.insert(i,v)</code>, <code>del a[i]</code>, <code>a.remove(v)</code></td><td>O(n)</td></tr>
<tr><td>membership</td><td><code>v in a</code></td><td><strong>O(n) — use a set if repeated</strong></td></tr>
<tr><td>slice</td><td><code>a[i:j]</code></td><td>O(j−i), makes a copy</td></tr>
<tr><td>reverse / sort</td><td><code>a.reverse()</code>, <code>a.sort()</code></td><td>O(n) / O(n log n)</td></tr>
<tr><td>extend, count, index</td><td><code>a.extend(b)</code>, <code>a.count(v)</code>, <code>a.index(v)</code></td><td>O(len b) / O(n) / O(n)</td></tr>
</table>
<p>Slicing tricks: <code>a[::-1]</code> reversed copy · <code>a[:k]</code> first k · <code>a[-k:]</code> last k · <code>a[::2]</code> every 2nd.</p>

<h2>2. tuple — frozen list</h2>
<p>Immutable, hashable. Use as dict/set keys (<code>seen[(r, c)]</code> for grid cells), for multiple return values, and for sort keys. Same O(1) indexing as list.</p>

<h2>3. dict — hash map (the interview MVP)</h2>
<table>
<tr><th>Operation</th><th>Code</th><th>Cost</th></tr>
<tr><td>get / set / delete</td><td><code>d[k]</code>, <code>d[k]=v</code>, <code>del d[k]</code></td><td>O(1) average</td></tr>
<tr><td>membership</td><td><code>k in d</code></td><td>O(1) average</td></tr>
<tr><td>safe get</td><td><code>d.get(k, default)</code></td><td>O(1) — no KeyError</td></tr>
<tr><td>get-or-insert</td><td><code>d.setdefault(k, []).append(v)</code></td><td>O(1)</td></tr>
<tr><td>remove &amp; return</td><td><code>d.pop(k, None)</code></td><td>O(1)</td></tr>
<tr><td>iterate</td><td><code>d.keys() / d.values() / d.items()</code></td><td>O(n)</td></tr>
</table>
<p>Since Python 3.7 dicts remember <strong>insertion order</strong> — that's what makes an LRU cache buildable with a plain dict. Counting idiom without imports: <code>freq[x] = freq.get(x, 0) + 1</code>.</p>
<div class="warn">Never add/remove dict keys while looping over the dict — iterate over <code>list(d)</code> if you must modify.</div>

<h2>4. set — dict without values</h2>
<table>
<tr><th>Operation</th><th>Code</th><th>Cost</th></tr>
<tr><td>add / remove / contains</td><td><code>s.add(v)</code>, <code>s.discard(v)</code>, <code>v in s</code></td><td>O(1) average</td></tr>
<tr><td>union / intersection / difference</td><td><code>a | b</code>, <code>a &amp; b</code>, <code>a - b</code></td><td>O(len a + len b)</td></tr>
<tr><td>subset</td><td><code>a <= b</code></td><td>O(len a)</td></tr>
</table>
<p><code>s.remove(v)</code> raises if missing; <code>s.discard(v)</code> doesn't. Dedupe: <code>list(set(a))</code> (order lost). The one-line "have I seen this before?" tool for cycle detection, duplicates, visited cells.</p>

<h2>Which structure? Decision table</h2>
<table>
<tr><th>You need…</th><th>Use</th></tr>
<tr><td>ordered items, index access, stack</td><td><code>list</code></td></tr>
<tr><td>key → value lookup, counting, grouping</td><td><code>dict</code></td></tr>
<tr><td>fast "seen it?" membership, dedupe</td><td><code>set</code></td></tr>
<tr><td>hashable composite key, fixed record</td><td><code>tuple</code></td></tr>
<tr><td>fast pops from BOTH ends (queue)</td><td><code>collections.deque</code> (next page)</td></tr>
</table>
'''},

# ============================================================ PY-4
{'id': 'py-4-strings', 'short': 'String Methods', 'title': 'PY-4 · Strings: Every Method You Need',
 'blurb': 'Immutability, the full method toolkit, formatting, and the classic string idioms.',
 'body': '''
<p>Strings appear in a third of all interview problems. Two facts drive everything: strings are <strong>immutable</strong> (every "change" creates a new string) and they are <strong>sequences</strong> (everything from lists — indexing, slicing, <code>len</code>, <code>in</code>, loops — works on them).</p>

<h2>1. The immutability tax</h2>
<pre><code># BAD: O(n²) — each += copies the whole string so far
res = ""
for ch in parts: res += ch

# GOOD: O(n) — collect then join once
res = []
for ch in parts: res.append(ch)
answer = "".join(res)</code></pre>

<h2>2. Method toolkit</h2>
<table>
<tr><th>Method</th><th>What it does</th><th>Notes</th></tr>
<tr><td><code>s.split(sep)</code></td><td>string → list</td><td><code>s.split()</code> splits on ANY whitespace, drops empties</td></tr>
<tr><td><code>sep.join(lst)</code></td><td>list → string</td><td>O(total length); items must be strings</td></tr>
<tr><td><code>s.strip() / lstrip / rstrip</code></td><td>trim whitespace (or given chars)</td><td>parsing</td></tr>
<tr><td><code>s.lower() / s.upper()</code></td><td>case change</td><td>case-insensitive compare</td></tr>
<tr><td><code>s.replace(old, new)</code></td><td>replace all occurrences</td><td>returns new string</td></tr>
<tr><td><code>s.find(t) / s.index(t)</code></td><td>first position of t</td><td>find returns −1, index raises</td></tr>
<tr><td><code>s.count(t)</code></td><td>non-overlapping occurrences</td><td>O(n·m)</td></tr>
<tr><td><code>s.startswith(t) / endswith(t)</code></td><td>prefix/suffix test</td><td>accepts tuple of options</td></tr>
<tr><td><code>s.isdigit() / isalpha() / isalnum()</code></td><td>character-class tests</td><td>whole string must match</td></tr>
<tr><td><code>s.zfill(w)</code></td><td>left-pad with zeros</td><td>binary addition problems</td></tr>
</table>

<h2>3. f-strings</h2>
<pre><code>f"{name} scored {score:.2f}"     # 2 decimals
f"{n:05d}"                        # zero-padded width 5
f"{ratio:.1%}"                    # percentage</code></pre>

<h2>4. Classic string idioms</h2>
<pre><code>s == s[::-1]                          # palindrome check
sorted(a) == sorted(b)                # anagram check, O(n log n)
"".join(sorted(s))                    # canonical anagram key for grouping
ord(c) - ord('a')                     # letter → 0..25 (frequency arrays)
s.split() and " ".join(words[::-1])   # reverse word order
c.isalnum()                           # skip punctuation in palindrome problems</code></pre>

<h2>5. Character frequency — three ways</h2>
<pre><code>from collections import Counter
freq = Counter(s)                       # the usual way

freq = {}                               # manual
for c in s: freq[c] = freq.get(c, 0) + 1

arr = [0] * 26                          # fastest, lowercase only
for c in s: arr[ord(c) - ord('a')] += 1</code></pre>
<p>The 26-length array trick makes the frequency itself hashable (<code>tuple(arr)</code>) — the key to Group Anagrams in O(n·k).</p>

<div class="tip"><strong>Mental model:</strong> to "edit" a string, convert to list, edit, join back: <code>lst = list(s); lst[i] = 'x'; s = "".join(lst)</code>.</div>
'''},

# ============================================================ PY-5
{'id': 'py-5-power-modules', 'short': 'Power Modules', 'title': 'PY-5 · The Power Modules: collections, heapq, bisect, itertools, math, functools',
 'blurb': 'deque, Counter, defaultdict, heaps, binary search, caching — the interview standard library.',
 'body': '''
<p>Six standard-library modules turn Python into an interview machine. All are allowed in interviews and on LeetCode.</p>

<h2>1. collections.deque — the real queue</h2>
<p>Double-ended queue: O(1) push/pop at <em>both</em> ends (a list is O(n) at the front). This is the queue for every BFS.</p>
<pre><code>from collections import deque
q = deque([start])
while q:
    node = q.popleft()      # O(1) — list.pop(0) would be O(n)
    q.append(neighbor)      # O(1)
# also: q.appendleft(x), q.pop(), deque(maxlen=k) auto-evicts old items</code></pre>

<h2>2. collections.Counter — counting, solved</h2>
<pre><code>from collections import Counter
c = Counter("banana")        # {'a':3, 'n':2, 'b':1}
c.most_common(2)             # [('a',3), ('n',2)]
c['z']                       # 0 — missing keys are 0, never KeyError
Counter(a) == Counter(b)     # anagram check in O(n)
c1 - c2, c1 & c2             # subtract counts / min of counts</code></pre>

<h2>3. collections.defaultdict — no more key-exists checks</h2>
<pre><code>from collections import defaultdict
graph = defaultdict(list)            # adjacency list
for u, v in edges: graph[u].append(v)   # missing key → [] automatically
groups = defaultdict(list)           # grouping (e.g. anagrams)
groups["".join(sorted(w))].append(w)</code></pre>

<h2>4. heapq — priority queue (min-heap)</h2>
<pre><code>import heapq
heap = []
heapq.heappush(heap, item)     # O(log n)
smallest = heapq.heappop(heap) # O(log n)
heap[0]                        # peek min, O(1)
heapq.heapify(lst)             # list → heap in O(n)
heapq.nlargest(k, nums)        # top-k in O(n log k)</code></pre>
<div class="warn">Python has NO max-heap. Push <strong>negated</strong> values: <code>heappush(h, -x)</code>, read <code>-h[0]</code>. Tie-break by pushing tuples: <code>(priority, count, item)</code> — tuples compare element by element.</div>

<h2>5. bisect — binary search, pre-written</h2>
<pre><code>import bisect
i = bisect.bisect_left(a, x)   # first index where x could go (a sorted)
j = bisect.bisect_right(a, x)  # after any equal elements
bisect.insort(a, x)            # insert keeping sorted, O(n) shift
# count of x in sorted list: bisect_right - bisect_left
# "first element >= x": a[bisect_left(a, x)]</code></pre>

<h2>6. itertools, math, functools — the utility belt</h2>
<pre><code>from itertools import permutations, combinations, product, accumulate
permutations([1,2,3])        # all orderings (n!)
combinations(nums, 2)        # all pairs, order-free
product(range(3), repeat=2)  # (0,0),(0,1)...(2,2) — grid coordinates
list(accumulate(nums))       # prefix sums in one line

import math
math.inf, -math.inf          # sentinels for min/max searches
math.gcd(a, b), math.lcm(a, b)
math.ceil(a / b)  or  -(-a // b)   # ceiling division trick
math.sqrt(x), math.log2(x), math.comb(n, k)

from functools import lru_cache
@lru_cache(None)             # memoize: dict of args → result
def fib(n):
    return n if n < 2 else fib(n-1) + fib(n-2)</code></pre>
<p><code>@lru_cache</code> turns any brute-force recursion into top-down DP in one line — arguments must be hashable.</p>

<h2>Cheat table — problem → tool</h2>
<table>
<tr><th>Problem smell</th><th>Reach for</th></tr>
<tr><td>BFS / process in arrival order</td><td><code>deque</code></td></tr>
<tr><td>count things / top frequent</td><td><code>Counter</code></td></tr>
<tr><td>group by key / adjacency list</td><td><code>defaultdict(list)</code></td></tr>
<tr><td>k-th smallest, merge streams, "top k"</td><td><code>heapq</code></td></tr>
<tr><td>sorted array lookups / insertion point</td><td><code>bisect</code></td></tr>
<tr><td>overlapping subproblems in recursion</td><td><code>@lru_cache</code></td></tr>
<tr><td>need all subsets/orderings (n ≤ ~10)</td><td><code>itertools</code></td></tr>
</table>
'''},

# ============================================================ PY-6
{'id': 'py-6-idioms-shortcuts', 'short': 'Idioms & Shortcuts', 'title': 'PY-6 · Comprehensions, Lambdas & the Shortcuts Pythonistas Use',
 'blurb': 'List/dict/set comprehensions, generator expressions, unpacking, and interview-speed idioms.',
 'body': '''
<p>This page is the "why does their solution look so short?" page — the compression tools of fluent Python, each with the long version next to it so you always know what's happening underneath.</p>

<h2>1. List comprehensions</h2>
<pre><code>squares = [x*x for x in nums]              # map
evens   = [x for x in nums if x % 2 == 0]  # filter
pairs   = [(i, j) for i in range(3) for j in range(3) if i != j]  # nested
matrix_col = [row[0] for row in grid]      # extract a column</code></pre>
<p>Long version of the first: <code>squares = []</code> then <code>for x in nums: squares.append(x*x)</code>. Same speed class, half the code, no off-by-one room.</p>

<h2>2. Dict &amp; set comprehensions, generators</h2>
<pre><code>index_of = {v: i for i, v in enumerate(nums)}   # value → index map (Two Sum!)
seen     = {x % 10 for x in nums}               # set comprehension
total    = sum(x*x for x in nums)               # generator: no list built, O(1) memory
first    = next((x for x in nums if x < 0), None)  # first match or None</code></pre>

<h2>3. Unpacking &amp; star syntax</h2>
<pre><code>a, b = b, a                    # swap
first, *rest = nums            # head / tail
x, y = point                   # tuple unpack
def f(*args, **kwargs): ...    # variadic
merged = [*list1, *list2]      # concatenate
print(*nums)                   # spread as arguments</code></pre>

<h2>4. Lambdas — tiny throwaway functions</h2>
<pre><code>sorted(people, key=lambda p: (p[1], p[0]))   # sort by 2nd field, then 1st
max(words, key=lambda w: len(set(w)))         # most distinct letters
intervals.sort(key=lambda iv: iv[0])          # THE intervals opener</code></pre>
<p>A lambda is just <code>def f(p): return (p[1], p[0])</code> without the name. If it needs more than one expression, write a real function.</p>

<h2>5. Idioms that save minutes in interviews</h2>
<pre><code>float('inf'), float('-inf')         # best-so-far sentinels
dp = [[0]*cols for _ in range(rows)]  # 2-D array (NOT [[0]*c]*r !)
for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):   # 4-direction grid walk
    r, c = row+dr, col+dc
    if 0 <= r < R and 0 <= c < C: ...
k = (lo + hi) // 2                  # binary search mid (no overflow in Python)
seen = set(); seen.add((r, c))      # visited cells as tuples
res.append(path[:])                 # SNAPSHOT the path in backtracking (copy!)
matrix[:] = zip(*matrix[::-1])      # rotate matrix 90° clockwise
val = d.get(key, 0) + 1             # count without Counter
if x in (a, b, c):                  # membership instead of 3 ors</code></pre>
<div class="warn"><strong>Backtracking bug #1:</strong> <code>res.append(path)</code> appends a <em>reference</em>; when you later pop from <code>path</code>, your saved answer mutates too. Always append a copy: <code>path[:]</code> or <code>list(path)</code>.</div>

<h2>6. Reading "clever" one-liners</h2>
<pre><code># Longest string in list:
max(strs, key=len)
# Sum of digits:
sum(int(d) for d in str(n))
# Transpose:
list(zip(*grid))
# Check if all rows same length:
len({len(r) for r in grid}) == 1
# Frequency of most common element:
max(Counter(nums).values())</code></pre>

<h2>7. What NOT to do in interviews</h2>
<ul>
<li>Don't nest comprehensions three levels deep — clarity beats cleverness; you'll be asked to explain it.</li>
<li>Don't shadow built-ins: naming a variable <code>list</code>, <code>dict</code>, <code>sum</code>, <code>min</code>, or <code>max</code> breaks them for the rest of the function.</li>
<li>Don't use recursion depth &gt; ~1000 without <code>sys.setrecursionlimit</code> — Python's default limit will crash deep DFS on big inputs; know the iterative rewrite.</li>
<li>Don't mutate a list while iterating over it — iterate over a copy or build a new list.</li>
</ul>

<div class="tip">You now have the full Python toolkit. Next stop: <strong>Foundations</strong> — how these tools are built and when each data structure wins.</div>
'''},
]
