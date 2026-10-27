"""Deep tutorials for Pattern 18: Hash Map & Cache Design Patterns."""
DEEP = {}
DEEP[49] = """<h3>Problem Overview</h3>
<p>Given an array of strings <code>strs</code>, group the anagrams together in any order. An anagram is a word formed by rearranging the letters of a different word, using all the original letters exactly once.</p>

<h3>Key Insights</h3>
<p>Two strings are anagrams if and only if their sorted versions are identical, or equivalently, their character frequency counts across the 26 lowercase English letters are identical. We can use a hash map where the key is the canonical representation of an anagram class and the value is a list of strings belonging to that class.</p>

<div class="table-wrap">
<table>
  <thead>
    <tr><th>Approach</th><th>Time Complexity</th><th>Space Complexity</th><th>Pros & Cons</th></tr>
  </thead>
  <tbody>
    <tr><td>Sorted String as Key</td><td>$O(N \\cdot K \\log K)$</td><td>$O(N \\cdot K)$</td><td>Simple to write; slower for long words.</td></tr>
    <tr><td>26-Count Tuple as Key (Optimal)</td><td>$O(N \\cdot K)$</td><td>$O(N \\cdot K)$</td><td>Linear in total characters; optimal for large inputs.</td></tr>
  </tbody>
</table>
</div>

<h3>Step-by-Step Algorithm (Optimal 26-Count Tuple)</h3>
<ol>
  <li>Initialize <code>groups = collections.defaultdict(list)</code>.</li>
  <li>For each word in <code>strs</code>:
    <ul>
      <li>Initialize a count array of size 26 with zeros.</li>
      <li>For each character $c$ in the word, increment <code>count[ord(c) - ord('a')]</code>.</li>
      <li>Convert the mutable list <code>count</code> into an immutable tuple <code>tuple(count)</code> to use as a hashable dictionary key.</li>
      <li>Append the original word to <code>groups[tuple(count)]</code>.</li>
    </ul>
  </li>
  <li>Return <code>list(groups.values())</code>.</li>
</ol>

<div class="code-block">
<pre><code># ASCII Dry Run for ["eat", "tea", "tan", "ate", "nat", "bat"]
# "eat" -> count: (1,0,0,0,1,...,1,0...) -> key_1 -> ["eat"]
# "tea" -> count: (1,0,0,0,1,...,1,0...) -> key_1 -> ["eat", "tea"]
# "tan" -> count: (1,0,0,0,0,...,1,1...) -> key_2 -> ["tan"]
# "ate" -> count: (1,0,0,0,1,...,1,0...) -> key_1 -> ["eat", "tea", "ate"]
# "nat" -> count: (1,0,0,0,0,...,1,1...) -> key_2 -> ["tan", "nat"]
# "bat" -> count: (1,1,0,0,0,...,0,1...) -> key_3 -> ["bat"]</code></pre>
</div>

<details>
<summary><strong>Python 3 Solution (Click to Expand)</strong></summary>
<div class="code-block">
<pre><code class="language-python">from typing import List
from collections import defaultdict

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        groups = defaultdict(list)
        
        for s in strs:
            count = [0] * 26
            for ch in s:
                count[ord(ch) - ord('a')] += 1
            # Tuples are hashable in Python
            groups[tuple(count)].append(s)
            
        return list(groups.values())
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> $O(N \\cdot K)$ where $N$ is the number of strings and $K$ is the maximum length of a string. Counting frequencies takes $O(K)$, and hashing a 26-element tuple is $O(26) = O(1)$.</li>
  <li><strong>Space Complexity:</strong> $O(N \\cdot K)$ to store the grouped strings in the hash map.</li>
  <li><strong>Edge Cases:</strong> Single character words, empty strings <code>[""]</code>, words with identical letters (e.g. <code>"aaaa"</code>).</li>
</ul>"""

DEEP[128] = """<h3>Problem Overview</h3>
<p>Given an unsorted array of integers <code>nums</code>, return the length of the longest consecutive elements sequence. The algorithm must run in $O(n)$ time.</p>

<h3>Key Insights</h3>
<p>A sorting solution takes $O(n \\log n)$, which violates the linear time requirement. To achieve $O(n)$, we use a <strong>Hash Set</strong> for $O(1)$ average lookups.</p>
<p>Crucial realization: A number $x$ can only be the <em>start</em> of a consecutive streak if $x - 1$ is <strong>not</strong> in the set! If $x - 1$ is present, $x$ cannot be the beginning of a maximal streak, so we skip it immediately. This ensures each number is visited at most twice (once in the outer loop, and once during sequence extension).</p>

<div class="table-wrap">
<table>
  <thead>
    <tr><th>Approach</th><th>Time Complexity</th><th>Space Complexity</th><th>Notes</th></tr>
  </thead>
  <tbody>
    <tr><td>Brute Force / Sorting</td><td>$O(n \\log n)$</td><td>$O(1)$ or $O(n)$</td><td>Sort and scan consecutive deltas.</td></tr>
    <tr><td>HashSet Streak Search (Optimal)</td><td>$O(n)$</td><td>$O(n)$</td><td>Only expand streaks from genuine sequence roots ($x - 1 \notin set$).</td></tr>
  </tbody>
</table>
</div>

<h3>Step-by-Step Algorithm</h3>
<ol>
  <li>Convert <code>nums</code> to a set <code>num_set = set(nums)</code>. This handles duplicates and provides $O(1)$ lookups.</li>
  <li>Initialize <code>max_streak = 0</code>.</li>
  <li>Iterate through each number $x$ in <code>num_set</code>:
    <ul>
      <li>Check if $x - 1 \notin num_set$. If false, continue to the next number (not a sequence start).</li>
      <li>If true, $x$ starts a streak: set <code>current_num = x</code> and <code>current_streak = 1</code>.</li>
      <li>While <code>current_num + 1 \\in num_set</code>, increment <code>current_num += 1</code> and <code>current_streak += 1</code>.</li>
      <li>Update <code>max_streak = max(max_streak, current_streak)</code>.</li>
    </ul>
  </li>
  <li>Return <code>max_streak</code>.</li>
</ol>

<details>
<summary><strong>Python 3 Solution (Click to Expand)</strong></summary>
<div class="code-block">
<pre><code class="language-python">from typing import List

class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        num_set = set(nums)
        longest = 0
        
        for num in num_set:
            # Only start counting if num is the beginning of a sequence
            if num - 1 not in num_set:
                curr = num
                streak = 1
                
                while curr + 1 in num_set:
                    curr += 1
                    streak += 1
                    
                longest = max(longest, streak)
                
        return longest
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> $O(n)$. Each number is checked as a start element in $O(1)$. The inner <code>while</code> loop only runs when $x$ is the head of a sequence, traversing each consecutive chain once across the entire algorithm.</li>
  <li><strong>Space Complexity:</strong> $O(n)$ to store unique elements in the HashSet.</li>
  <li><strong>Edge Cases:</strong> Empty array (returns 0), duplicate elements (e.g. <code>[0, 1, 1, 2]</code>), negative numbers.</li>
</ul>"""

DEEP[146] = """<h3>Problem Overview</h3>
<p>Design a data structure that follows the constraints of a <strong>Least Recently Used (LRU) cache</strong>. Implement <code>get(key)</code> and <code>put(key, value)</code> in $O(1)$ average time complexity.</p>

<h3>Core Data Structure: Doubly Linked List + Hash Map</h3>
<p>To achieve $O(1)$ access, we need a <strong>Hash Map</strong> mapping <code>key -> Node</code>. To achieve $O(1)$ removal and re-ordering upon access, we use a <strong>Doubly Linked List</strong> with dummy <code>head</code> (most recently used) and <code>tail</code> (least recently used) sentinel nodes.</p>

<div class="code-block">
<pre><code>[Head Sentinel] <-> [MRU Node] <-> ... <-> [LRU Node] <-> [Tail Sentinel]
       ^                                         ^
       |                                         |
Newly accessed nodes inserted here       Evictions happen right before Tail</code></pre>
</div>

<details>
<summary><strong>Python 3 Solution (Click to Expand)</strong></summary>
<div class="code-block">
<pre><code class="language-python">class Node:
    __slots__ = ('key', 'val', 'prev', 'next')
    def __init__(self, key: int = 0, val: int = 0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # key -> Node
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node) -> None:
        p, n = node.prev, node.next
        p.next = n
        n.prev = p

    def _add_to_front(self, node: Node) -> None:
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)
        self._add_to_front(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            node = self.cache[key]
            node.val = value
            self._remove(node)
            self._add_to_front(node)
        else:
            if len(self.cache) >= self.capacity:
                lru = self.tail.prev
                self._remove(lru)
                del self.cache[lru.key]
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_to_front(new_node)
</code></pre>
</div>
</details>

<h3>Complexity & Invariants</h3>
<ul>
  <li><strong>Time Complexity:</strong> $O(1)$ for both <code>get</code> and <code>put</code>. Hash map lookup is $O(1)$, pointer updates in a doubly linked list are $O(1)$.</li>
  <li><strong>Space Complexity:</strong> $O(\text{capacity})$ to store up to capacity nodes.</li>
</ul>"""

DEEP[249] = """<h3>Problem Overview</h3>
<p>Given an array of strings <code>strings</code>, group all strings that belong to the same shifting sequence. Two strings $s_1$ and $s_2$ belong to the same shifting sequence if $s_1$ can be converted into $s_2$ by shifting each character of $s_1$ forward by the same number of positions cyclically around the alphabet.</p>

<h3>Key Insights</h3>
<p>A string's shifting identity is invariant under cyclical character differences! For example, for <code>"az"</code>: <code>('z' - 'a') % 26 = 25</code>. For <code>"ba"</code>: <code>('a' - 'b') % 26 = (-1) % 26 = 25</code>.</p>
<p>Thus, any string can be represented by a canonical key: the tuple of cyclic differences between consecutive adjacent characters:
$$key = \\left( (s[i] - s[i - 1]) \\pmod{26} \right)_{i=1}^{L-1}$$
Strings of length 1 all share the empty tuple <code>()</code> as key.</p>

<details>
<summary><strong>Python 3 Solution (Click to Expand)</strong></summary>
<div class="code-block">
<pre><code class="language-python">from typing import List
from collections import defaultdict

class Solution:
    def groupStrings(self, strings: List[str]) -> List[List[str]]:
        groups = defaultdict(list)
        
        for s in strings:
            # Compute canonical key of cyclical diffs
            diff_key = []
            for i in range(1, len(s)):
                diff = (ord(s[i]) - ord(s[i - 1])) % 26
                diff_key.append(diff)
            groups[tuple(diff_key)].append(s)
            
        return list(groups.values())
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> $O(N \\cdot L)$ where $N$ is the number of strings and $L$ is the maximum length of a string.</li>
  <li><strong>Space Complexity:</strong> $O(N \\cdot L)$ to store all grouped strings in the hash map.</li>
  <li><strong>Edge Cases:</strong> Single character strings (e.g. <code>["a", "z"]</code> both map to <code>()</code>), wraps around <code>'z' -> 'a'</code>.</li>
</ul>"""

DEEP[347] = """<h3>Problem Overview</h3>
<p>Given an integer array <code>nums</code> and an integer $k$, return the $k$ most frequent elements. The algorithm must be better than $O(n \\log n)$.</p>

<h3>Key Insights</h3>
<p>We can count frequencies using a hash map in $O(n)$ time. To extract the top $k$ without sorting all distinct keys in $O(u \\log u)$, we have two optimal approaches:</p>
<ol>
  <li><strong>Min-Heap:</strong> Keep a min-heap of size $k$ based on frequency: $O(n \\log k)$ time, $O(n)$ space.</li>
  <li><strong>Bucket Sort (Optimal Linear Time):</strong> Frequencies can range only from $1$ to $n$. We create a list of buckets where <code>buckets[f]</code> contains all elements that appear with frequency $f$. We iterate backwards from bucket $n$ down to $1$ to collect $k$ elements in $O(n)$ time!</li>
</ol>

<details>
<summary><strong>Python 3 Solution (Bucket Sort - O(N))</strong></summary>
<div class="code-block">
<pre><code class="language-python">from typing import List
from collections import Counter

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        counts = Counter(nums)
        n = len(nums)
        # buckets[i] will store list of elements with frequency i
        buckets = [[] for _ in range(n + 1)]
        
        for num, freq in counts.items():
            buckets[freq].append(num)
            
        res = []
        for freq in range(n, 0, -1):
            for num in buckets[freq]:
                res.append(num)
                if len(res) == k:
                    return res
        return res
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> $O(n)$ total. Counter generation takes $O(n)$, bucket population takes $O(u) \\le O(n)$, and iterating backwards takes at most $O(n)$ steps.</li>
  <li><strong>Space Complexity:</strong> $O(n)$ for the frequency map and buckets.</li>
  <li><strong>Edge Cases:</strong> $k$ equals number of unique elements, all elements identical ($freq = n$), negative values.</li>
</ul>"""

DEEP[380] = """<h3>Problem Overview</h3>
<p>Implement the <code>RandomizedSet</code> class such that <code>insert</code>, <code>remove</code>, and <code>getRandom</code> operate in $O(1)$ average time.</p>

<h3>Key Insights</h3>
<ul>
  <li>A <strong>Hash Map</strong> allows $O(1)$ search and deletion, but does not support picking a uniform random element in $O(1)$ because hash keys cannot be indexed by an integer in $[0, n-1]$.</li>
  <li>A <strong>Dynamic Array (List)</strong> supports $O(1)$ uniform random access via index, but deletion of an arbitrary element takes $O(n)$ because elements must shift.</li>
  <li><strong>Combination (The Swap Trick):</strong> Use an array <code>nums</code> and a hash map <code>val_to_idx</code>. To delete an element in $O(1)$ without shifting:
    <ol>
      <li>Swap the target element with the <strong>last element</strong> in the array.</li>
      <li>Update the index of the swapped last element in the hash map.</li>
      <li>Pop the last element from the array in $O(1)$!</li>
    </ol>
  </li>
</ul>

<details>
<summary><strong>Python 3 Solution (Click to Expand)</strong></summary>
<div class="code-block">
<pre><code class="language-python">import random

class RandomizedSet:
    def __init__(self):
        self.nums = []
        self.val_to_idx = {}

    def insert(self, val: int) -> bool:
        if val in self.val_to_idx:
            return False
        self.val_to_idx[val] = len(self.nums)
        self.nums.append(val)
        return True

    def remove(self, val: int) -> bool:
        if val not in self.val_to_idx:
            return False
        idx = self.val_to_idx[val]
        last_val = self.nums[-1]
        
        # Move last element to the slot of the element to delete
        self.nums[idx] = last_val
        self.val_to_idx[last_val] = idx
        
        # Pop last element
        self.nums.pop()
        del self.val_to_idx[val]
        return True

    def getRandom(self) -> int:
        return random.choice(self.nums)
</code></pre>
</div>
</details>

<h3>Complexity & Invariants</h3>
<ul>
  <li><strong>Time Complexity:</strong> $O(1)$ average for <code>insert</code>, <code>remove</code>, and <code>getRandom</code>.</li>
  <li><strong>Space Complexity:</strong> $O(N)$ to store $N$ elements.</li>
</ul>"""

DEEP[381] = """<h3>Problem Overview</h3>
<p>Implement the <code>RandomizedCollection</code> class with support for duplicate elements, such that <code>insert</code>, <code>remove</code>, and <code>getRandom</code> operate in $O(1)$ average time.</p>

<h3>Key Insights</h3>
<p>Because duplicates are allowed, a value can appear at multiple indices in the array. Therefore, the hash map must map each value to a <strong>set of indices</strong>: <code>val_to_indices = defaultdict(set)</code>.</p>
<p>When removing <code>val</code>:
<ol>
  <li>Take any index <code>remove_idx</code> from <code>val_to_indices[val]</code>.</li>
  <li>Let <code>last_idx = len(nums) - 1</code> and <code>last_val = nums[-1]</code>.</li>
  <li>Overwrite <code>nums[remove_idx] = last_val</code>.</li>
  <li>Update <code>val_to_indices[last_val]</code>: remove <code>last_idx</code> and add <code>remove_idx</code>.</li>
  <li>Remove <code>remove_idx</code> from <code>val_to_indices[val]</code>.</li>
  <li>Pop from <code>nums</code> in $O(1)$.</li>
</ol>
Careful with the edge case where <code>remove_idx == last_idx</code>: perform set modifications appropriately so indices remain consistent!</p>

<details>
<summary><strong>Python 3 Solution (Click to Expand)</strong></summary>
<div class="code-block">
<pre><code class="language-python">from collections import defaultdict
import random

class RandomizedCollection:
    def __init__(self):
        self.nums = []
        self.indices = defaultdict(set)

    def insert(self, val: int) -> bool:
        has_val = len(self.indices[val]) > 0
        self.indices[val].add(len(self.nums))
        self.nums.append(val)
        return not has_val

    def remove(self, val: int) -> bool:
        if not self.indices[val]:
            return False
        
        # Pick any index of val to remove
        remove_idx = self.indices[val].pop()
        last_idx = len(self.nums) - 1
        last_val = self.nums[-1]
        
        if remove_idx != last_idx:
            self.nums[remove_idx] = last_val
            self.indices[last_val].remove(last_idx)
            self.indices[last_val].add(remove_idx)
            
        self.nums.pop()
        return True

    def getRandom(self) -> int:
        return random.choice(self.nums)
</code></pre>
</div>
</details>

<h3>Complexity & Invariants</h3>
<ul>
  <li><strong>Time Complexity:</strong> $O(1)$ average for <code>insert</code>, <code>remove</code>, and <code>getRandom</code>. Set operations on integer indices run in $O(1)$.</li>
  <li><strong>Space Complexity:</strong> $O(N)$ for array and set of indices.</li>
  <li><strong>Edge Cases:</strong> Removing the very last element in the array (<code>remove_idx == last_idx</code>).</li>
</ul>"""

DEEP[432] = """<h3>Problem Overview</h3>
<p>Design a data structure to store the strings' count with the ability to return the strings with minimum and maximum counts in $O(1)$ time complexity for all operations: <code>inc(key)</code>, <code>dec(key)</code>, <code>getMaxKey()</code>, and <code>getMinKey()</code>.</p>

<h3>Key Insights</h3>
<p>Multiple strings can have the same frequency. If we maintain individual nodes per string, finding min/max in $O(1)$ is difficult. Instead, maintain a <strong>Doubly Linked List of Frequency Buckets</strong>, where each bucket holds a frequency count and a <code>set()</code> of all strings having that exact frequency!</p>
<ul>
  <li><code>head</code> sentinel points to the lowest frequency bucket; <code>tail</code> sentinel points to the highest.</li>
  <li><code>key_to_bucket</code> hash map maps each <code>key</code> to its containing <code>BucketNode</code>.</li>
  <li><code>inc(key)</code>: Move key from bucket $f$ to bucket $f+1$. If bucket $f+1$ doesn't exist, insert it immediately after bucket $f$. If bucket $f$ becomes empty, remove it.</li>
  <li><code>dec(key)</code>: Move key from bucket $f$ to bucket $f-1$. If $f-1 == 0$, delete key entirely.</li>
  <li><code>getMaxKey()</code>: Return any key from <code>tail.prev.keys</code> (or <code>""</code> if empty).</li>
  <li><code>getMinKey()</code>: Return any key from <code>head.next.keys</code> (or <code>""</code> if empty).</li>
</ul>

<details>
<summary><strong>Python 3 Solution (Click to Expand)</strong></summary>
<div class="code-block">
<pre><code class="language-python">class Bucket:
    def __init__(self, freq: int):
        self.freq = freq
        self.keys = set()
        self.prev = None
        self.next = None

class AllOne:
    def __init__(self):
        self.head = Bucket(0)  # Min sentinel
        self.tail = Bucket(0)  # Max sentinel
        self.head.next = self.tail
        self.tail.prev = self.head
        self.key_bucket = {}   # key -> Bucket

    def _insert_after(self, prev_bucket: Bucket, new_bucket: Bucket) -> None:
        new_bucket.next = prev_bucket.next
        new_bucket.prev = prev_bucket
        prev_bucket.next.prev = new_bucket
        prev_bucket.next = new_bucket

    def _remove_bucket(self, bucket: Bucket) -> None:
        bucket.prev.next = bucket.next
        bucket.next.prev = bucket.prev

    def inc(self, key: str) -> None:
        if key not in self.key_bucket:
            # Insert key into freq 1 bucket
            if self.head.next.freq == 1:
                target = self.head.next
            else:
                target = Bucket(1)
                self._insert_after(self.head, target)
            target.keys.add(key)
            self.key_bucket[key] = target
        else:
            curr = self.key_bucket[key]
            curr.keys.remove(key)
            if curr.next.freq == curr.freq + 1:
                target = curr.next
            else:
                target = Bucket(curr.freq + 1)
                self._insert_after(curr, target)
            target.keys.add(key)
            self.key_bucket[key] = target
            if not curr.keys:
                self._remove_bucket(curr)

    def dec(self, key: str) -> None:
        if key not in self.key_bucket:
            return
        curr = self.key_bucket[key]
        curr.keys.remove(key)
        if curr.freq == 1:
            del self.key_bucket[key]
        else:
            if curr.prev.freq == curr.freq - 1:
                target = curr.prev
            else:
                target = Bucket(curr.freq - 1)
                self._insert_after(curr.prev, target)
            target.keys.add(key)
            self.key_bucket[key] = target
        if not curr.keys:
            self._remove_bucket(curr)

    def getMaxKey(self) -> str:
        if self.tail.prev == self.head:
            return ""
        return next(iter(self.tail.prev.keys))

    def getMinKey(self) -> str:
        if self.head.next == self.tail:
            return ""
        return next(iter(self.head.next.keys))
</code></pre>
</div>
</details>

<h3>Complexity & Invariants</h3>
<ul>
  <li><strong>Time Complexity:</strong> Strictly $O(1)$ for all operations (<code>inc</code>, <code>dec</code>, <code>getMaxKey</code>, <code>getMinKey</code>).</li>
  <li><strong>Space Complexity:</strong> $O(N)$ where $N$ is the number of distinct string keys.</li>
</ul>"""

DEEP[460] = """<h3>Problem Overview</h3>
<p>Design and implement an <strong>LFU (Least Frequently Used) cache</strong> with $O(1)$ runtime for <code>get</code> and <code>put</code>. When the cache reaches its capacity, it should invalidate and evict the least frequently used key. If there is a tie in frequency, the least recently used key among them should be evicted.</p>

<h3>Core Data Structures</h3>
<ol>
  <li><code>key_to_node</code>: maps <code>key -> Node(key, val, freq)</code>.</li>
  <li><code>freq_to_dll</code>: maps <code>freq -> DoublyLinkedList</code>. Each DLL maintains LRU order for all items with that frequency.</li>
  <li><code>min_freq</code>: an integer tracking the lowest frequency currently present in the cache. When evicting, we pop from <code>freq_to_dll[min_freq].pop_lru()</code>.</li>
</ol>

<details>
<summary><strong>Python 3 Solution (Click to Expand)</strong></summary>
<div class="code-block">
<pre><code class="language-python">from collections import defaultdict

class Node:
    __slots__ = ('key', 'val', 'freq', 'prev', 'next')
    def __init__(self, key: int = 0, val: int = 0, freq: int = 1):
        self.key = key
        self.val = val
        self.freq = freq
        self.prev = None
        self.next = None

class DLinkedList:
    def __init__(self):
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def add_node(self, node: Node) -> None:
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node
        self.size += 1

    def remove_node(self, node: Node) -> None:
        p, n = node.prev, node.next
        p.next = n
        n.prev = p
        self.size -= 1

    def pop_tail(self) -> Node:
        if self.size == 0:
            return None
        lru = self.tail.prev
        self.remove_node(lru)
        return lru

class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.key_to_node = {}
        self.freq_to_dll = defaultdict(DLinkedList)
        self.min_freq = 0

    def _update_freq(self, node: Node) -> None:
        freq = node.freq
        self.freq_to_dll[freq].remove_node(node)
        if freq == self.min_freq and self.freq_to_dll[freq].size == 0:
            self.min_freq += 1
        node.freq += 1
        self.freq_to_dll[node.freq].add_node(node)

    def get(self, key: int) -> int:
        if key not in self.key_to_node:
            return -1
        node = self.key_to_node[key]
        self._update_freq(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return
        if key in self.key_to_node:
            node = self.key_to_node[key]
            node.val = value
            self._update_freq(node)
        else:
            if len(self.key_to_node) >= self.capacity:
                lru = self.freq_to_dll[self.min_freq].pop_tail()
                del self.key_to_node[lru.key]
            new_node = Node(key, value, 1)
            self.key_to_node[key] = new_node
            self.freq_to_dll[1].add_node(new_node)
            self.min_freq = 1
</code></pre>
</div>
</details>

<h3>Complexity & Invariants</h3>
<ul>
  <li><strong>Time Complexity:</strong> $O(1)$ for both <code>get</code> and <code>put</code>.</li>
  <li><strong>Space Complexity:</strong> $O(\text{capacity})$ to store elements and frequency lists.</li>
</ul>"""

DEEP[981] = """<h3>Problem Overview</h3>
<p>Design a time-based key-value data structure that can store multiple values for the same key at different time stamps and retrieve the key's value at a certain timestamp.</p>
<ul>
  <li><code>set(key, value, timestamp)</code>: Stores the key and value along with the given timestamp. Timestamps are strictly increasing.</li>
  <li><code>get(key, timestamp)</code>: Returns a value such that <code>set</code> was called previously with <code>timestamp_prev &lt;= timestamp</code>. If multiple, return the largest timestamp; if none, return <code>""</code>.</li>
</ul>

<h3>Key Insights</h3>
<p>Because timestamps for each key are added in strictly increasing order, the list of <code>(timestamp, value)</code> pairs for any key is already sorted! We can use <strong>Binary Search (bisect_right)</strong> to find the rightmost timestamp $\\le$ the requested query timestamp in $O(\\log N)$ time.</p>

<details>
<summary><strong>Python 3 Solution (Click to Expand)</strong></summary>
<div class="code-block">
<pre><code class="language-python">from collections import defaultdict
import bisect

class TimeMap:
    def __init__(self):
        # key -> list of (timestamp, value)
        self.store = defaultdict(list)

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.store[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        if key not in self.store:
            return ""
        entries = self.store[key]
        # Binary search for rightmost entry with entry[0] <= timestamp
        idx = bisect.bisect_right(entries, (timestamp, chr(127)))
        if idx == 0:
            return ""
        return entries[idx - 1][1]
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong>
    <ul>
      <li><code>set</code>: $O(1)$ append.</li>
      <li><code>get</code>: $O(\\log M)$ where $M$ is the number of timestamps for the given key.</li>
    </ul>
  </li>
  <li><strong>Space Complexity:</strong> $O(N)$ total elements stored across all keys.</li>
  <li><strong>Edge Cases:</strong> Query timestamp smaller than any stored timestamp for the key (returns <code>""</code>).</li>
</ul>"""
