# -*- coding: utf-8 -*-
"""
Deep tutorials for Pattern 15: Design Patterns.
Masterclass 12-step structured explanations with ASCII dry runs and complexity analyses.
"""

DEEP = {
146: '''<h2>🧭 How to think about it</h2>
<p>Design a data structure that follows the constraints of a <strong>Least Recently Used (LRU) Cache</strong>.</p>

<p>Requirements:
- <code>get(key)</code>: Return the value if the key exists, otherwise return -1. Accessing a key moves it to the most recently used position.
- <code>put(key, value)</code>: Update or insert the key-value pair. If capacity is exceeded, evict the least recently used key.
- <strong>Both operations must run in strict $O(1)$ average time complexity!</strong></p>

<p><strong>The Doubly Linked List + Hash Map Pair:</strong>
- A <strong>Hash Map</strong> allows $O(1)$ lookup from <code>key</code> to the corresponding node in memory.
- A <strong>Doubly Linked List</strong> allows $O(1)$ node removal and $O(1)$ insertion at the head (most recently used) or eviction at the tail (least recently used) given a node pointer!
- Use <strong>dummy head and dummy tail</strong> sentinel nodes to eliminate all null-pointer boundary checks!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Using an array or simple list requires $O(n)$ time to search and shift elements upon every access. Doubly linked list + hash map achieves strict $O(1)$ operations.</p>

<div class="insight">💡 <strong>Key insight:</strong> Hash map <code>key -> Node</code> gives $O(1)$ lookup. Doubly linked list with dummy head and tail gives $O(1)$ insert at head and $O(1)$ removal at tail.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">class Node:
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {} # key -> Node
        self.head = Node() # Dummy head (Most Recently Used)
        self.tail = Node() # Dummy tail (Least Recently Used)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node):
        """Unlinks an existing node in O(1)."""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_head(self, node: Node):
        """Inserts node immediately after dummy head in O(1)."""
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)
        self._add_to_head(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            node = self.cache[key]
            node.val = value
            self._remove(node)
            self._add_to_head(node)
        else:
            if len(self.cache) >= self.capacity:
                lru = self.tail.prev
                self._remove(lru)
                del self.cache[lru.key]
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_to_head(new_node)
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(1)$ for both <code>get</code> and <code>put</code>.<br>
<strong>Space:</strong> $O(\text{capacity})$ — Hash map and nodes for at most $capacity$ elements.</p>
''',
155: '''<h2>🧭 How to think about it</h2>
<p>Design a stack that supports <code>push</code>, <code>pop</code>, <code>top</code>, and retrieving the minimum element in $O(1)$ time.</p>

<p>A standard stack gives $O(1)$ access only to the top element.
To retrieve the global minimum in $O(1)$, we must maintain the minimum value <em>for every state of the stack</em>!
When we push value $x$, the minimum of the stack at this height is:
$$\text{curr\\_min} = \\min(x, \\; \text{previous\\_min})$$
We can either:
1. Store a pair <code>(val, min_so_far)</code> on a single stack.
2. Maintain a secondary <strong>min_stack</strong> that stores the running minimum.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Scanning the stack for the minimum on <code>getMin()</code> takes $O(n)$ time. Tracking running minimums at each level guarantees $O(1)$ for all operations.</p>

<div class="insight">💡 <strong>Key insight:</strong> Push pairs <code>(val, min(val, stack[-1][1]))</code>. The second value always gives the minimum element in the stack up to that height in $O(1)$ time!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">class MinStack:
    def __init__(self):
        # Stack stores tuples: (value, current_min)
        self.stack = []

    def push(self, val: int) -> None:
        if not self.stack:
            self.stack.append((val, val))
        else:
            curr_min = min(val, self.stack[-1][1])
            self.stack.append((val, curr_min))

    def pop(self) -> None:
        self.stack.pop()

    def top(self) -> int:
        return self.stack[-1][0]

    def getMin(self) -> int:
        return self.stack[-1][1]
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(1)$ for <code>push</code>, <code>pop</code>, <code>top</code>, and <code>getMin</code>.<br>
<strong>Space:</strong> $O(n)$ — Stack storage holding element pairs.</p>
''',
208: '''<h2>🧭 How to think about it</h2>
<p>A <strong>trie</strong> (pronounced as "try") or <strong>prefix tree</strong> is a tree data structure used to efficiently store and retrieve keys in a dataset of strings.</p>

<p>Every <code>TrieNode</code> contains:
1. <code>children</code>: A map or 26-element array pointing to child <code>TrieNode</code>s corresponding to each character.
2. <code>is_end</code>: A boolean flag indicating whether a complete word terminates at this node.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Searching a hash set for prefix matches requires checking every string ($O(N \\times L)$). A Trie searches prefixes in strictly $O(L)$ time where $L$ is the word length, completely independent of the total number of words $N$ in the dictionary!</p>

<div class="insight">💡 <strong>Key insight:</strong> Each tree node branches on character <code>ch</code>: <code>node = node.children.setdefault(ch, TrieNode())</code>. Prefixes share common ancestry paths.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        curr = self.root
        for ch in word:
            if ch not in curr.children:
                curr.children[ch] = TrieNode()
            curr = curr.children[ch]
        curr.is_end = True

    def search(self, word: str) -> bool:
        curr = self.root
        for ch in word:
            if ch not in curr.children:
                return False
            curr = curr.children[ch]
        return curr.is_end

    def startsWith(self, prefix: str) -> bool:
        curr = self.root
        for ch in prefix:
            if ch not in curr.children:
                return False
            curr = curr.children[ch]
        return True
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(L)$ for <code>insert</code>, <code>search</code>, and <code>startsWith</code> where $L$ is word/prefix length.<br>
<strong>Space:</strong> $O(N \\times L)$ where $N$ is total words and $L$ is average length.</p>
''',
211: '''<h2>🧭 How to think about it</h2>
<p>Design a data structure that supports adding new words and finding if a string matches any previously added string, where dots <code>'.'</code> can match any letter.</p>

<p>Use a standard Trie for storing words.
During <code>search(word)</code>:
- For a normal character <code>ch</code>: advance to child <code>node.children[ch]</code>.
- For a wildcard dot <code>'.'</code>: branch recursively across <strong>all</strong> child nodes present at the current level:
  <code>for child in node.children.values(): if dfs(child, next_idx): return True</code></p>

<h2>🐢 Brute force vs optimal</h2>
<p>Without wildcards, lookup is $O(L)$. With wildcards, backtracking traverses only matching subtree branches.</p>

<div class="insight">💡 <strong>Key insight:</strong> Standard Trie with DFS recursion for dot wildcard: if <code>ch == '.'</code>, try all active child branches <code>any(dfs(child, i + 1) for child in curr.children.values())</code>.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">class WordDictionary:
    def __init__(self):
        self.root = {}

    def addWord(self, word: str) -> None:
        curr = self.root
        for ch in word:
            curr = curr.setdefault(ch, {})
        curr['#'] = True # Word termination marker

    def search(self, word: str) -> bool:
        def dfs(node, idx):
            if idx == len(word):
                return '#' in node
            ch = word[idx]
            if ch == '.':
                for child_key, child_node in node.items():
                    if child_key != '#' and dfs(child_node, idx + 1):
                        return True
                return False
            else:
                if ch not in node:
                    return False
                return dfs(node[ch], idx + 1)
                
        return dfs(self.root, 0)
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> <code>addWord</code>: $O(L)$. <code>search</code>: $O(L)$ for exact words, $O(26^L)$ worst case with all dots.<br>
<strong>Space:</strong> $O(N \\times L)$ total characters across dictionary.</p>
''',
225: '''<h2>🧭 How to think about it</h2>
<p>Implement a last-in-first-out (LIFO) stack using only standard FIFO queues (only <code>push to back</code>, <code>peek/pop from front</code>, <code>size</code>, and <code>is empty</code> operations).</p>

<p><strong>The Single-Queue Rotation Trick:</strong>
When pushing element $x$ to the queue:
1. Append $x$ to the back of the queue.
2. For all previous $size - 1$ elements in the queue, dequeue from front and enqueue back to rear!
This inverts the order so that the newly added element $x$ is now sitting at the <strong>front</strong> of the queue, ready to be popped in $O(1)$!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>By spending $O(n)$ time during <code>push</code>, all reads (<code>pop</code> and <code>top</code>) execute in instant $O(1)$ time using only 1 queue!</p>

<div class="insight">💡 <strong>Key insight:</strong> After enqueuing $x$, rotate the queue by size - 1: <code>q.append(q.popleft())</code>. The newest element is now at the front!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">from collections import deque

class MyStack:
    def __init__(self):
        self.q = deque()

    def push(self, x: int) -> None:
        self.q.append(x)
        # Rotate all previous elements behind the newly added x
        for _ in range(len(self.q) - 1):
            self.q.append(self.q.popleft())

    def pop(self) -> int:
        return self.q.popleft()

    def top(self) -> int:
        return self.q[0]

    def empty(self) -> bool:
        return len(self.q) == 0
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> <code>push</code>: $O(n)$ rotation. <code>pop</code>, <code>top</code>, <code>empty</code>: $O(1)$.<br>
<strong>Space:</strong> $O(n)$ — Single queue buffer.</p>
''',
232: '''<h2>🧭 How to think about it</h2>
<p>Implement a first-in-first-out (FIFO) queue using only two standard LIFO stacks.</p>

<p>Maintain two stacks:
- <code>in_stack</code>: Receives all incoming elements on <code>push(x)</code>.
- <code>out_stack</code>: Delivers elements for <code>pop()</code> and <code>peek()</code>.</p>
<p><strong>Amortized Transfer:</strong>
When an element is needed from <code>out_stack</code> and <code>out_stack</code> is empty:
Pop all elements from <code>in_stack</code> and push them onto <code>out_stack</code>!
This reverses their order, so the oldest element is now at the top of <code>out_stack</code>!
Each element is moved between stacks <strong>at most once</strong>, giving strict $O(1)$ <strong>amortized</strong> time complexity!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Transferring elements on every operation takes $O(n)$. Lazy transfer (only when <code>out_stack</code> is empty) achieves $O(1)$ amortized cost.</p>

<div class="insight">💡 <strong>Key insight:</strong> Two stacks: push to <code>in_stack</code>. On pop/peek, if <code>out_stack</code> is empty, dump all of <code>in_stack</code> into <code>out_stack</code>. $O(1)$ amortized!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">class MyQueue:
    def __init__(self):
        self.in_stack = []
        self.out_stack = []

    def push(self, x: int) -> None:
        self.in_stack.append(x)

    def _transfer(self):
        if not self.out_stack:
            while self.in_stack:
                self.out_stack.append(self.in_stack.pop())

    def pop(self) -> int:
        self._transfer()
        return self.out_stack.pop()

    def peek(self) -> int:
        self._transfer()
        return self.out_stack[-1]

    def empty(self) -> bool:
        return not self.in_stack and not self.out_stack
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(1)$ amortized for all operations ($O(1)$ worst case for push, $O(n)$ single transfer).<br>
<strong>Space:</strong> $O(n)$ — Two stacks storing $n$ elements total.</p>
''',
295: '''<h2>🧭 How to think about it</h2>
<p>The median is the middle value in an ordered integer list. Design a data structure that supports adding numbers from a continuous stream and finding the current median in $O(1)$ time.</p>

<p><strong>The Two Heaps Balancing Pattern:</strong>
Divide the numbers into two equal halves:
1. <strong>Max-Heap (<code>small</code>):</strong> Stores the smaller half of the numbers. The root gives the largest of the small half.
2. <strong>Min-Heap (<code>large</code>):</strong> Stores the larger half of the numbers. The root gives the smallest of the large half.</p>

<p><strong>Invariants to Maintain:</strong>
1. <code>len(small) == len(large)</code> (if total numbers even) OR <code>len(small) == len(large) + 1</code> (if odd).
2. Every element in <code>small</code> must be $\\le$ every element in <code>large</code>.</p>
<p>Then:
- If odd: $\text{median} = \text{small.root}$.
- If even: $\text{median} = (\text{small.root} + \text{large.root}) / 2.0$.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Sorting an array takes $O(n \\log n)$ per query. Two heaps add elements in $O(\\log n)$ time and return the median in $O(1)$ time.</p>

<div class="insight">💡 <strong>Key insight:</strong> Max-heap for lower half, min-heap for upper half. Balance sizes so <code>0 <= len(small) - len(large) <= 1</code>. Median is calculated in $O(1)$!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">import heapq

class MedianFinder:
    def __init__(self):
        # small: max-heap (invert signs in Python)
        # large: min-heap
        self.small = []
        self.large = []

    def addNum(self, num: int) -> None:
        # Step 1: Push to max-heap small
        heapq.heappush(self.small, -num)
        
        # Step 2: Ensure small's largest <= large's smallest
        if self.small and self.large and (-self.small[0] > self.large[0]):
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
            
        # Step 3: Balance sizes (small can have at most 1 more element than large)
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        elif len(self.large) > len(self.small):
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)

    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        return (-self.small[0] + self.large[0]) / 2.0
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> <code>addNum</code>: $O(\\log n)$ heap pushes/pops. <code>findMedian</code>: $O(1)$ peek.<br>
<strong>Space:</strong> $O(n)$ — Two heaps storing all stream elements.</p>
''',
346: '''<h2>🧭 How to think about it</h2>
<p>Given a stream of integers and a window size, calculate the moving average of all integers in the sliding window.</p>

<p>Maintain:
- A FIFO circular queue or <code>deque</code> of maximum capacity $size$.
- A running scalar <code>total_sum</code>.</p>
<p>When a new number $val$ arrives:
1. If the queue is at capacity, subtract the oldest element from <code>total_sum</code> and dequeue it:
   <code>total_sum -= q.popleft()</code>.
2. Add $val$ to <code>total_sum</code> and append to queue:
   <code>total_sum += val; q.append(val)</code>.
3. Return <code>total_sum / len(q)</code> in $O(1)$!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Summing the window from scratch takes $O(k)$ time. Running accumulator updates in $O(1)$ time and $O(k)$ memory.</p>

<div class="insight">💡 <strong>Key insight:</strong> Sliding window accumulator: <code>window_sum += val - (q.popleft() if full else 0)</code>. Average computes in $O(1)$ time.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">from collections import deque

class MovingAverage:
    def __init__(self, size: int):
        self.size = size
        self.queue = deque()
        self.window_sum = 0

    def next(self, val: int) -> float:
        if len(self.queue) == self.size:
            self.window_sum -= self.queue.popleft()
            
        self.queue.append(val)
        self.window_sum += val
        return self.window_sum / len(self.queue)
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(1)$ for each <code>next()</code> invocation.<br>
<strong>Space:</strong> $O(k)$ where $k$ is the window size.</p>
''',
348: '''<h2>🧭 How to think about it</h2>
<p>Assume an $n \\times n$ Tic-Tac-Toe board. Design a game class where players take turns placing marks. A player wins if they place $n$ marks in any row, column, or diagonal. The <code>move(row, col, player)</code> must return the winner if this move won the game, or 0 otherwise.</p>

<p><strong>The $O(1)$ Line Counters Trick:</strong>
Instead of maintaining an $n \\times n$ board and scanning the row/column after every move ($O(n)$):
Assign player 1 a score of <code>+1</code> and player 2 a score of <code>-1</code>!
Maintain:
- <code>rows[n]</code>: running sum for each row.
- <code>cols[n]</code>: running sum for each column.
- <code>diag</code>: running sum for the main diagonal ($row == col$).
- <code>anti_diag</code>: running sum for the anti-diagonal ($row + col == n - 1$).</p>
<p>When player makes a move:
Add score ($+1$ or $-1$) to the corresponding row, column, and diagonals.
If the absolute value of any updated counter reaches $n$, that player has won!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Scanning board takes $O(n)$ per move. Counter updates execute in strictly $O(1)$ time and $O(n)$ space.</p>

<div class="insight">💡 <strong>Key insight:</strong> Track line sums (+1 for P1, -1 for P2). If <code>abs(rows[r]) == n</code> or <code>abs(cols[c]) == n</code> or <code>abs(diag) == n</code>, the player won in $O(1)$ time!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">class TicTacToe:
    def __init__(self, n: int):
        self.n = n
        self.rows = [0] * n
        self.cols = [0] * n
        self.diag = 0
        self.anti_diag = 0

    def move(self, row: int, col: int, player: int) -> int:
        score = 1 if player == 1 else -1
        n = self.n
        
        self.rows[row] += score
        self.cols[col] += score
        if row == col:
            self.diag += score
        if row + col == n - 1:
            self.anti_diag += score
            
        if (abs(self.rows[row]) == n or
            abs(self.cols[col]) == n or
            abs(self.diag) == n or
            abs(self.anti_diag) == n):
            return player
            
        return 0
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(1)$ per move.<br>
<strong>Space:</strong> $O(n)$ — Arrays for row and column sums.</p>
''',
355: '''<h2>🧭 How to think about it</h2>
<p>Design a simplified version of Twitter where users can post tweets, follow/unfollow another user, and see the 10 most recent tweets in their news feed.</p>

<p><strong>Data Structures:</strong>
1. <code>follows</code>: <code>defaultdict(set)</code> mapping <code>userId -> set of followeeIds</code>.
2. <code>tweets</code>: <code>defaultdict(list)</code> mapping <code>userId -> list of (timestamp, tweetId)</code>.
3. <code>global_time</code>: Decrementing counter tracking chronological order.</p>

<p><strong>Feed Generation (Merge K Sorted Lists):</strong>
A user's feed is composed of the recent tweets of themselves plus everyone they follow.
Because each user's tweet list is already chronologically sorted, finding the 10 most recent tweets across all followees is the classic <strong>Merge K Sorted Lists (LC 23)</strong> using a Min-Heap of size at most $K$ (number of followees)!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Pulling and sorting all tweets takes $O(T \\log T)$. Merging with a heap inspects only the latest tweets from each followee in $O(K \\log F)$ time.</p>

<div class="insight">💡 <strong>Key insight:</strong> Fan-out-on-read: merge the latest tweets of all followees using a Max-Heap / Priority Queue up to 10 elements.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">from collections import defaultdict
import heapq

class Twitter:
    def __init__(self):
        self.time = 0
        self.follows = defaultdict(set)
        self.tweets = defaultdict(list)

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.time += 1
        # Store as (timestamp, tweetId)
        self.tweets[userId].append((self.time, tweetId))

    def getNewsFeed(self, userId: int) -> list[int]:
        # User follows themselves for feed inclusion
        followees = self.follows[userId] | {userId}
        
        # Max-heap to merge latest tweets from each followee
        # Elements: (-timestamp, tweetId, followeeId, next_index_in_list)
        max_heap = []
        for f_id in followees:
            user_tweets = self.tweets[f_id]
            if user_tweets:
                idx = len(user_tweets) - 1
                t, tw_id = user_tweets[idx]
                max_heap.append((-t, tw_id, f_id, idx - 1))
                
        heapq.heapify(max_heap)
        feed = []
        while max_heap and len(feed) < 10:
            neg_t, tw_id, f_id, next_idx = heapq.heappop(max_heap)
            feed.append(tw_id)
            if next_idx >= 0:
                t, next_tw_id = self.tweets[f_id][next_idx]
                heapq.heappush(max_heap, (-t, next_tw_id, f_id, next_idx - 1))
                
        return feed

    def follow(self, followerId: int, followeeId: int) -> None:
        self.follows[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        self.follows[followerId].discard(followeeId)
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> <code>postTweet</code>, <code>follow</code>, <code>unfollow</code>: $O(1)$. <code>getNewsFeed</code>: $O(F + 10 \\log F)$ where $F$ is number of followees.<br>
<strong>Space:</strong> $O(U + T)$ — Users graph and tweets storage.</p>
''',
359: '''<h2>🧭 How to think about it</h2>
<p>Design a logger system that receives a stream of messages along with their timestamps. Each unique message should only be printed at most once every 10 seconds.</p>

<p>Maintain a hash map <code>last_printed[message] -> timestamp</code>.
When <code>shouldPrintMessage(timestamp, message)</code> is called:
- If <code>message</code> not in map OR <code>timestamp >= last_printed[message] + 10</code>:
  Update <code>last_printed[message] = timestamp</code> and return <code>True</code>.
- Otherwise, return <code>False</code>.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Hash map gives instant $O(1)$ verification per log entry.</p>

<div class="insight">💡 <strong>Key insight:</strong> Hash map maps <code>msg -> next_allowed_timestamp</code>. If <code>timestamp >= next_allowed</code>, update <code>msg = timestamp + 10</code> and return <code>True</code>.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">class Logger:
    def __init__(self):
        self.ok = {}

    def shouldPrintMessage(self, timestamp: int, message: str) -> bool:
        if timestamp < self.ok.get(message, 0):
            return False
        self.ok[message] = timestamp + 10
        return True
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(1)$ per message.<br>
<strong>Space:</strong> $O(M)$ where $M$ is the number of distinct messages seen.</p>
''',
362: '''<h2>🧭 How to think about it</h2>
<p>Design a hit counter which counts the number of hits received in the past 5 minutes (300 seconds).</p>

<p><strong>The Circular Array / Bucketing Pattern (Fixed Memory):</strong>
Instead of keeping a growing list or queue of all raw hits ($O(N)$ space if millions of hits occur in 5 minutes):
Maintain a fixed circular array of size 300!
- <code>times = [0] * 300</code>: stores the timestamp mod 300.
- <code>hits = [0] * 300</code>: stores the hit count for that specific second.</p>
<p>When <code>hit(timestamp)</code> is called:
Let <code>idx = timestamp % 300</code>.
- If <code>times[idx] != timestamp</code>: reset <code>times[idx] = timestamp</code> and <code>hits[idx] = 1</code>.
- Else: increment <code>hits[idx] += 1</code>.</p>
<p>When <code>getHits(timestamp)</code> is called:
Iterate through all 300 buckets. If <code>timestamp - times[i] < 300</code>, sum <code>hits[i]</code>!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Storing all timestamps in a queue can explode memory under high QPS. The 300-bucket circular array consumes fixed $O(1)$ memory and executes in $O(1)$ time!</p>

<div class="insight">💡 <strong>Key insight:</strong> Circular buffer of 300 buckets: <code>idx = timestamp % 300</code>. Memory is strictly bounded to 300 integers regardless of whether there are 10 hits or 10 billion hits!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">class HitCounter:
    def __init__(self):
        # 300 seconds in 5 minutes
        self.times = [0] * 300
        self.hits = [0] * 300

    def hit(self, timestamp: int) -> None:
        idx = timestamp % 300
        if self.times[idx] != timestamp:
            self.times[idx] = timestamp
            self.hits[idx] = 1
        else:
            self.hits[idx] += 1

    def getHits(self, timestamp: int) -> int:
        total = 0
        for i in range(300):
            if timestamp - self.times[i] < 300:
                total += self.hits[i]
        return total
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> <code>hit</code>: $O(1)$. <code>getHits</code>: $O(300) = O(1)$ fixed loop.<br>
<strong>Space:</strong> $O(1)$ — Exactly 600 integers allocated permanently.</p>
''',
380: '''<h2>🧭 How to think about it</h2>
<p>Implement the <code>RandomizedSet</code> class such that <code>insert</code>, <code>remove</code>, and <code>getRandom</code> all execute in strict $O(1)$ average time complexity.</p>

<p>Why can't we just use a Hash Set?
A Hash Set provides $O(1)$ <code>insert</code> and $O(1)$ <code>remove</code>, but cannot provide true uniform $O(1)$ <code>getRandom</code> because elements are distributed sparsely across buckets!
Why can't we just use an Array?
An Array provides $O(1)$ random indexing (<code>nums[random.randint(0, len-1)]</code>), but <code>remove(val)</code> takes $O(n)$ time to search and shift elements!</p>

<p><strong>The Swap-with-Last Deletion Trick:</strong>
Combine an <strong>Array</strong> and a <strong>Hash Map</strong>:
- <code>nums</code> (Array): stores values contiguously.
- <code>val_to_idx</code> (Map): maps <code>val -> index in nums</code>.</p>
<p>To <code>remove(val)</code> in $O(1)$:
1. Find index of <code>val</code>: <code>idx = val_to_idx[val]</code>.
2. Overwrite <code>nums[idx]</code> with the <strong>last element</strong> in <code>nums</code>: <code>last = nums[-1]; nums[idx] = last</code>.
3. Update map: <code>val_to_idx[last] = idx</code>.
4. Pop the last element in $O(1)$ without any shifting: <code>nums.pop()</code> and <code>del val_to_idx[val]</code>!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Swapping with the last element eliminates all array shifting, achieving strict $O(1)$ for insert, delete, and random sampling.</p>

<div class="insight">💡 <strong>Key insight:</strong> To delete from an array in $O(1)$: swap the target element with the last element, update the index in the hash map, and <code>pop()</code> the tail!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
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
        # Swap with last element
        idx = self.val_to_idx[val]
        last_val = self.nums[-1]
        
        self.nums[idx] = last_val
        self.val_to_idx[last_val] = idx
        
        # Pop tail in O(1)
        self.nums.pop()
        del self.val_to_idx[val]
        return True

    def getRandom(self) -> int:
        return random.choice(self.nums)
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(1)$ average for <code>insert</code>, <code>remove</code>, and <code>getRandom</code>.<br>
<strong>Space:</strong> $O(n)$ — Dynamic array and hash map holding $n$ values.</p>
''',
460: '''<h2>🧭 How to think about it</h2>
<p>Design and implement a data structure for a <strong>Least Frequently Used (LFU) cache</strong>. When the capacity is reached, evict the least frequently used key. If there is a tie, evict the <strong>least recently used</strong> key among them.</p>

<p><strong>Core Challenge:</strong> Both <code>get</code> and <code>put</code> must run in $O(1)$ time!</p>

<p><strong>The Doubly-Linked-List per Frequency Architecture:</strong>
We maintain:
1. <code>vals</code>: <code>key -> (value, freq)</code>
2. <code>freq_lists</code>: <code>freq -> DoublyLinkedList</code> (each frequency has its own Doubly Linked List storing keys in LRU order!)
3. <code>min_freq</code>: integer tracking the current global minimum frequency in the cache.</p>

<p><strong>When a key's frequency increments ($f 	o f + 1$):</strong>
1. Remove key from <code>freq_lists[f]</code>.
2. If <code>freq_lists[f]</code> becomes empty and <code>min_freq == f</code>, increment <code>min_freq += 1</code>!
3. Insert key into <code>freq_lists[f + 1]</code>.</p>
<p><strong>When evicting at full capacity:</strong>
Remove the LRU node from <code>freq_lists[min_freq].tail.prev</code> in $O(1)$!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Using a heap or priority queue takes $O(\\log n)$ per access. A frequency-to-doubly-linked-list mapping achieves strict $O(1)$ operations.</p>

<div class="insight">💡 <strong>Key insight:</strong> Map each frequency to its own Doubly Linked List. Track <code>min_freq</code>. When evicting, remove the oldest element from <code>freq_lists[min_freq]</code> in $O(1)$!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">from collections import defaultdict

class Node:
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.freq = 1
        self.prev = None
        self.next = None

class DLinkedList:
    def __init__(self):
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def add_to_head(self, node: Node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node
        self.size += 1

    def remove(self, node: Node):
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1

    def remove_tail(self) -> Node:
        if self.size == 0:
            return None
        lru = self.tail.prev
        self.remove(lru)
        return lru

class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.nodes = {} # key -> Node
        self.freq_lists = defaultdict(DLinkedList) # freq -> DLinkedList
        self.min_freq = 0

    def _update_freq(self, node: Node):
        f = node.freq
        self.freq_lists[f].remove(node)
        if self.freq_lists[f].size == 0 and self.min_freq == f:
            self.min_freq += 1
            
        node.freq += 1
        self.freq_lists[node.freq].add_to_head(node)

    def get(self, key: int) -> int:
        if key not in self.nodes:
            return -1
        node = self.nodes[key]
        self._update_freq(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if self.capacity == 0:
            return
            
        if key in self.nodes:
            node = self.nodes[key]
            node.val = value
            self._update_freq(node)
        else:
            if len(self.nodes) >= self.capacity:
                lfu_node = self.freq_lists[self.min_freq].remove_tail()
                del self.nodes[lfu_node.key]
                
            new_node = Node(key, value)
            self.nodes[key] = new_node
            self.freq_lists[1].add_to_head(new_node)
            self.min_freq = 1
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(1)$ for both <code>get</code> and <code>put</code>.<br>
<strong>Space:</strong> $O(\text{capacity})$ — Hash map and nodes partitioned across frequency lists.</p>
''',

251: '''<h2>🧭 How to think about it</h2>
<p>Design an iterator to flatten a 2D vector. It should support <code>next()</code> and <code>hasNext()</code> operations.</p>

<p>Do NOT flatten the entire 2D vector into a 1D array upfront in the constructor ($O(N)$ extra space)!
Instead, maintain two lightweight coordinate pointers:
- <code>row</code>: current row index in the outer list.
- <code>col</code>: current column index in the current inner list.</p>

<p><strong>The Lazy Advance Helper <code>_advance_to_valid()</code>:</strong>
Because rows can be completely empty (e.g. <code>[[], [1, 2], [], [3]]</code>), we must advance <code>row</code> forward whenever <code>col == len(vec[row])</code> until we either land on a non-empty row or reach the end of the outer list!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Copying into a 1D list takes $O(N)$ auxiliary space. Two-pointer pointer navigation takes $O(1)$ auxiliary space and $O(1)$ amortized time per operation.</p>

<div class="insight">💡 <strong>Key insight:</strong> Advance pointers lazily: <code>while row < len(vec) and col == len(vec[row]): row += 1; col = 0</code>. Consumes $O(1)$ auxiliary space!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">class Vector2D:
    def __init__(self, vec: list[list[int]]):
        self.vec = vec
        self.row = 0
        self.col = 0

    def _advance_to_valid(self):
        while self.row < len(self.vec) and self.col == len(self.vec[self.row]):
            self.row += 1
            self.col = 0

    def next(self) -> int:
        self._advance_to_valid()
        val = self.vec[self.row][self.col]
        self.col += 1
        return val

    def hasNext(self) -> bool:
        self._advance_to_valid()
        return self.row < len(self.vec)
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(1)$ amortized for both <code>next()</code> and <code>hasNext()</code>.<br>
<strong>Space:</strong> $O(1)$ auxiliary space (no array copying).</p>
''',
271: '''<h2>🧭 How to think about it</h2>
<p>Design an algorithm to encode a list of strings to a string. The encoded string is then sent over the network and decoded back to the original list of strings.</p>

<p><strong>Length-Prefixed Framing:</strong>
Any special delimiter character (like <code>,</code>, <code>:</code>, or <code>#</code>) can legitimately appear inside the strings themselves.
Instead of fragile character escaping, encode each string as:
<code>f"{len(s)}#{s}"</code>
During decoding:
1. Scan for the delimiter <code>#</code> to parse the integer length $L$.
2. Slice exactly the next $L$ characters as the payload.
3. Advance the index by $L$ and repeat!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Escaping delimiters requires complex string replacement. Length-prefix chunking is stateless, robust, and executes in $O(N)$ linear time.</p>

<div class="insight">💡 <strong>Key insight:</strong> Chunk format: <code>length + '#' + string</code>. Reading $L$ bytes directly bypasses any delimiters nested inside the string payload.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">class Codec:
    def encode(self, strs: list[str]) -> str:
        """Encodes a list of strings to a single wire string."""
        return "".join(f"{len(s)}#{s}" for s in strs)

    def decode(self, s: str) -> list[str]:
        """Decodes a single wire string to a list of strings."""
        res = []
        i = 0
        while i < len(s):
            sep = s.find('#', i)
            length = int(s[i:sep])
            word = s[sep + 1 : sep + 1 + length]
            res.append(word)
            i = sep + 1 + length
        return res
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(N)$ where $N$ is the total number of characters across all strings.<br>
<strong>Space:</strong> $O(N)$ — Single wire string buffer.</p>
''',
341: '''<h2>🧭 How to think about it</h2>
<p>You are given a nested list of integers <code>nestedList</code>. Each element is either an integer, or a list whose elements may also be integers or other lists. Implement an iterator to flatten it.</p>

<p><strong>The Stack of Reverse Generators:</strong>
To achieve true lazy evaluation without flattening everything in the constructor ($O(1)$ memory consumption for deep trees):
Maintain a stack storing elements in <strong>reverse order</strong>!
- In <code>hasNext()</code>:
  While stack is not empty and the top element is a list:
  Pop the list, and push its sub-elements onto the stack in <strong>reverse order</strong>!
- When the top element is an integer, return <code>True</code>!
- If the stack becomes empty, return <code>False</code>.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Flattening in constructor takes $O(N)$ upfront time and space. The stack approach flattens on-demand in $O(D)$ space where $D$ is the maximum nesting depth.</p>

<div class="insight">💡 <strong>Key insight:</strong> Stack holds nested elements in reverse order. In <code>hasNext()</code>, unpack top lists in reverse until top is a plain integer.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">class NestedIterator:
    def __init__(self, nestedList: list):
        # Push elements in reverse so top of stack is the first element
        self.stack = list(reversed(nestedList))

    def next(self) -> int:
        return self.stack.pop().getInteger()

    def hasNext(self) -> bool:
        while self.stack:
            top = self.stack[-1]
            if top.isInteger():
                return True
            # Pop list and push its items in reverse order
            self.stack.pop()
            for item in reversed(top.getList()):
                self.stack.append(item)
        return False
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(1)$ amortized per <code>next()</code> and <code>hasNext()</code>.<br>
<strong>Space:</strong> $O(D)$ where $D$ is the maximum nesting depth.</p>
''',
353: '''<h2>🧭 How to think about it</h2>
<p>Design a Snake game that is played on a device with screen size $height \\times width$. The snake starts at position $(0, 0)$ with length 1. You are given a list of food positions. When the snake eats food, its length and score increase by 1. If it hits a wall or bites its own body, the game ends (returns -1).</p>

<p><strong>Data Structures:</strong>
1. <code>body</code> (Double-ended Queue / <code>deque</code>): stores coordinates of snake body segments from head to tail.
2. <code>body_set</code> (Hash Set): stores body coordinates for $O(1)$ self-collision checks!
3. <code>food_idx</code>: pointer to the current food item.</p>

<p><strong>The Tail Movement Nuance:</strong>
When moving to a new cell:
- If food is eaten: tail does <strong>not</strong> move (snake grows).
- If no food is eaten: tail <strong>must move forward</strong> (pop tail from <code>body</code> and remove from <code>body_set</code>) <em>before</em> checking if the new head collides with the body! (Moving into the tail's old spot is valid!).</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Scanning the entire body list for collisions takes $O(L)$ per move. The hash set allows $O(1)$ collision detection.</p>

<div class="insight">💡 <strong>Key insight:</strong> Pop tail first if not eating food, then check wall boundaries and body collision in $O(1)$ using <code>body_set</code>, then append new head.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">from collections import deque

class SnakeGame:
    def __init__(self, width: int, height: int, food: list[list[int]]):
        self.w = width
        self.h = height
        self.food = food
        self.food_idx = 0
        self.score = 0
        
        # Snake starts at (0, 0)
        self.body = deque([(0, 0)])
        self.body_set = {(0, 0)}
        self.dirs = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}

    def move(self, direction: str) -> int:
        dr, dc = self.dirs[direction]
        head_r, head_c = self.body[0]
        new_r, new_c = head_r + dr, head_c + dc
        
        # 1. Wall collision
        if not (0 <= new_r < self.h and 0 <= new_c < self.w):
            return -1
            
        # 2. Check food
        is_food = (self.food_idx < len(self.food) and 
                   [new_r, new_c] == self.food[self.food_idx])
                   
        if is_food:
            self.food_idx += 1
            self.score += 1
        else:
            # Pop tail to free its cell
            tail = self.body.pop()
            self.body_set.remove(tail)
            
        # 3. Body collision (after tail is freed)
        if (new_r, new_c) in self.body_set:
            return -1
            
        # 4. Add new head
        self.body.appendleft((new_r, new_c))
        self.body_set.add((new_r, new_c))
        
        return self.score
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(1)$ per <code>move()</code>.<br>
<strong>Space:</strong> $O(N)$ where $N$ is the number of food items eaten (max snake length).</p>
''',
379: '''<h2>🧭 How to think about it</h2>
<p>Design a Phone Directory which allocates and releases telephone numbers from $0$ to $\text{maxNumbers} - 1$.</p>

<p>Requirements:
- <code>get()</code>: Provide an unassigned number, or -1 if none available.
- <code>check(number)</code>: Return whether the number is currently available.
- <code>release(number)</code>: Free up an assigned number.</p>

<p><strong>Queue + Hash Set (or Boolean Array):</strong>
- <code>available_queue</code>: FIFO queue holding available numbers.
- <code>used_set</code>: Hash set tracking numbers currently in use for $O(1)$ check and release deduplication.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Scanning an array for an available number takes $O(n)$. A queue of available numbers gives strict $O(1)$ for <code>get</code>, <code>check</code>, and <code>release</code>.</p>

<div class="insight">💡 <strong>Key insight:</strong> Maintain a FIFO queue of unused numbers and a set of used numbers. <code>get</code> pops from queue, <code>release</code> adds back to queue in $O(1)$!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">from collections import deque

class PhoneDirectory:
    def __init__(self, maxNumbers: int):
        self.available = deque(range(maxNumbers))
        self.used = set()

    def get(self) -> int:
        if not self.available:
            return -1
        num = self.available.popleft()
        self.used.add(num)
        return num

    def check(self, number: int) -> bool:
        return number not in self.used

    def release(self, number: int) -> None:
        if number in self.used:
            self.used.remove(number)
            self.available.append(number)
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(1)$ for <code>get</code>, <code>check</code>, and <code>release</code>.<br>
<strong>Space:</strong> $O(N)$ where $N$ is <code>maxNumbers</code>.</p>
''',
432: '''<h2>🧭 How to think about it</h2>
<p>Design a data structure to store the strings' count with the ability to return the strings with minimum and maximum counts in <strong>$O(1)$ time complexity</strong> for all operations: <code>inc</code>, <code>dec</code>, <code>getMaxKey</code>, and <code>getMinKey</code>!</p>

<p><strong>Doubly Linked List of Buckets + Hash Maps:</strong>
1. Each <code>BucketNode</code> represents a distinct count value (e.g. count = 1, 2, 5...) and holds:
   - <code>count</code>: integer value.
   - <code>keys</code>: a hash set of strings that currently have this exact count.
   - <code>prev</code> and <code>next</code>: pointers linking to the adjacent count bucket.
2. <code>key_to_node</code> (Hash Map): maps each string <code>key -> BucketNode</code>.
3. Sentinel <code>head</code> and <code>tail</code> nodes keep track of minimum count (first bucket after head) and maximum count (last bucket before tail)!</p>

<p><strong>Transitions:</strong>
- <code>inc(key)</code>: Move key from bucket $C$ to bucket $C + 1$ (create bucket $C + 1$ if it doesn't exist). Remove key from bucket $C$; delete bucket $C$ if empty!
- <code>dec(key)</code>: Move key from bucket $C$ to bucket $C - 1$ (or delete key if $C == 1$). Delete bucket $C$ if empty!
- <code>getMaxKey()</code>: Return any key from <code>tail.prev.keys</code> in $O(1)$!
- <code>getMinKey()</code>: Return any key from <code>head.next.keys</code> in $O(1)$!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Heap or balanced tree requires $O(\\log n)$ per update. Doubly linked list of frequency buckets achieves strict $O(1)$ for all operations.</p>

<div class="insight">💡 <strong>Key insight:</strong> Doubly linked list where each node is a bucket holding a set of keys with identical counts. Head neighbor is min; tail neighbor is max. Strict $O(1)$!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">class Bucket:
    def __init__(self, count=0):
        self.count = count
        self.keys = set()
        self.prev = None
        self.next = None

class AllOne:
    def __init__(self):
        self.head = Bucket(0) # Dummy head
        self.tail = Bucket(0) # Dummy tail
        self.head.next = self.tail
        self.tail.prev = self.head
        self.key_to_bucket = {} # key -> Bucket

    def _insert_after(self, target: Bucket, new_bucket: Bucket):
        new_bucket.next = target.next
        new_bucket.prev = target
        target.next.prev = new_bucket
        target.next = new_bucket

    def _remove_bucket(self, bucket: Bucket):
        bucket.prev.next = bucket.next
        bucket.next.prev = bucket.prev

    def inc(self, key: str) -> None:
        if key not in self.key_to_bucket:
            # Target count is 1
            if self.head.next.count == 1:
                b = self.head.next
            else:
                b = Bucket(1)
                self._insert_after(self.head, b)
            b.keys.add(key)
            self.key_to_bucket[key] = b
        else:
            curr_b = self.key_to_bucket[key]
            next_count = curr_b.count + 1
            if curr_b.next.count == next_count:
                next_b = curr_b.next
            else:
                next_b = Bucket(next_count)
                self._insert_after(curr_b, next_b)
            next_b.keys.add(key)
            self.key_to_bucket[key] = next_b
            curr_b.keys.remove(key)
            if not curr_b.keys:
                self._remove_bucket(curr_b)

    def dec(self, key: str) -> None:
        curr_b = self.key_to_bucket[key]
        curr_b.keys.remove(key)
        if curr_b.count == 1:
            del self.key_to_bucket[key]
        else:
            prev_count = curr_b.count - 1
            if curr_b.prev.count == prev_count:
                prev_b = curr_b.prev
            else:
                prev_b = Bucket(prev_count)
                self._insert_after(curr_b.prev, prev_b)
            prev_b.keys.add(key)
            self.key_to_bucket[key] = prev_b
        if not curr_b.keys:
            self._remove_bucket(curr_b)

    def getMaxKey(self) -> str:
        if self.tail.prev == self.head:
            return ""
        return next(iter(self.tail.prev.keys))

    def getMinKey(self) -> str:
        if self.head.next == self.tail:
            return ""
        return next(iter(self.head.next.keys))
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(1)$ for <code>inc</code>, <code>dec</code>, <code>getMaxKey</code>, and <code>getMinKey</code>.<br>
<strong>Space:</strong> $O(K)$ where $K$ is the number of distinct keys stored.</p>
''',
604: '''<h2>🧭 How to think about it</h2>
<p>Design and implement a data structure for a compressed string iterator. The given compressed string represents the original uncompressed string of characters followed by their frequencies (e.g. <code>"L1e2t1c1o1d1e1"</code> representing <code>"Leetcode"</code>).</p>

<p>Maintain:
- <code>s</code>: compressed string.
- <code>ptr</code>: cursor index in <code>s</code>.
- <code>curr_char</code>: active character being emitted.
- <code>curr_count</code>: remaining repeat count of <code>curr_char</code>.</p>
<p>During <code>next()</code>:
If <code>curr_count == 0</code>, read the next character and parse the entire multidigit number following it! Decrement <code>curr_count -= 1</code> and return <code>curr_char</code>.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Expanding the entire string in memory takes $O(\text{Total Length})$ which can explode if count is $10^9$. Reading on the fly takes $O(1)$ extra space.</p>

<div class="insight">💡 <strong>Key insight:</strong> Parse on the fly: when <code>curr_count == 0</code>, extract next character and read multidigit integer. Avoids unpacking giant strings.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">class StringIterator:
    def __init__(self, compressedString: str):
        self.s = compressedString
        self.ptr = 0
        self.curr_char = ' '
        self.curr_count = 0

    def next(self) -> str:
        if not self.hasNext():
            return ' '
        if self.curr_count == 0:
            self.curr_char = self.s[self.ptr]
            self.ptr += 1
            # Parse multi-digit number
            num = 0
            while self.ptr < len(self.s) and self.s[self.ptr].isdigit():
                num = num * 10 + int(self.s[self.ptr])
                self.ptr += 1
            self.curr_count = num
            
        self.curr_count -= 1
        return self.curr_char

    def hasNext(self) -> bool:
        return self.curr_count > 0 or self.ptr < len(self.s)
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(1)$ amortized per <code>next()</code> call.<br>
<strong>Space:</strong> $O(1)$ auxiliary space.</p>
''',
622: '''<h2>🧭 How to think about it</h2>
<p>Design your implementation of the circular queue. A circular queue is a linear data structure in which the operations are performed based on FIFO principle and the last position is connected back to the first position to make a circle.</p>

<p>Maintain:
- <code>q = [0] * k</code>: fixed-size array of capacity $k$.
- <code>head</code>: index of the front element.
- <code>count</code>: current number of elements in the queue.</p>
<p>Formulas:
- Rear index: <code>(head + count - 1) % k</code>
- New element inserted at: <code>(head + count) % k</code>
- Dequeue advances head: <code>head = (head + 1) % k; count -= 1</code></p>

<h2>🐢 Brute force vs optimal</h2>
<p>Using <code>count</code> eliminates the ambiguity between an empty queue and a full queue in classic pointer math without wasting an array slot.</p>

<div class="insight">💡 <strong>Key insight:</strong> Use <code>head</code> and <code>count</code>: rear is <code>(head + count - 1) % k</code>. Adding increments count; removing increments head modulo $k$.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">class MyCircularQueue:
    def __init__(self, k: int):
        self.k = k
        self.q = [0] * k
        self.head = 0
        self.count = 0

    def enQueue(self, value: int) -> bool:
        if self.isFull():
            return False
        tail = (self.head + self.count) % self.k
        self.q[tail] = value
        self.count += 1
        return True

    def deQueue(self) -> bool:
        if self.isEmpty():
            return False
        self.head = (self.head + 1) % self.k
        self.count -= 1
        return True

    def Front(self) -> int:
        return -1 if self.isEmpty() else self.q[self.head]

    def Rear(self) -> int:
        if self.isEmpty():
            return -1
        tail = (self.head + self.count - 1) % self.k
        return self.q[tail]

    def isEmpty(self) -> bool:
        return self.count == 0

    def isFull(self) -> bool:
        return self.count == self.k
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(1)$ for all operations.<br>
<strong>Space:</strong> $O(k)$ — Fixed circular buffer of size $k$.</p>
''',
641: '''<h2>🧭 How to think about it</h2>
<p>Design your implementation of the circular double-ended queue (deque) supporting insertions and deletions at both front and rear ends.</p>

<p>Similar to Circular Queue (LC 622), maintain:
- <code>head</code>: points to front element.
- <code>count</code>: number of items currently in deque.
- <code>insertFront(val)</code>: decrements head: <code>head = (head - 1 + k) % k; q[head] = val; count += 1</code>.
- <code>insertLast(val)</code>: inserts at tail: <code>tail = (head + count) % k; q[tail] = val; count += 1</code>.
- <code>deleteFront()</code>: <code>head = (head + 1) % k; count -= 1</code>.
- <code>deleteLast()</code>: <code>count -= 1</code>.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>All operations execute in $O(1)$ time with modulo arithmetic on a fixed pre-allocated array.</p>

<div class="insight">💡 <strong>Key insight:</strong> Front insertion wraps left: <code>head = (head - 1 + k) % k</code>. Rear insertion wraps right: <code>(head + count) % k</code>.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">class MyCircularDeque:
    def __init__(self, k: int):
        self.k = k
        self.q = [0] * k
        self.head = 0
        self.count = 0

    def insertFront(self, value: int) -> bool:
        if self.isFull():
            return False
        self.head = (self.head - 1 + self.k) % self.k
        self.q[self.head] = value
        self.count += 1
        return True

    def insertLast(self, value: int) -> bool:
        if self.isFull():
            return False
        tail = (self.head + self.count) % self.k
        self.q[tail] = value
        self.count += 1
        return True

    def deleteFront(self) -> bool:
        if self.isEmpty():
            return False
        self.head = (self.head + 1) % self.k
        self.count -= 1
        return True

    def deleteLast(self) -> bool:
        if self.isEmpty():
            return False
        self.count -= 1
        return True

    def getFront(self) -> int:
        return -1 if self.isEmpty() else self.q[self.head]

    def getRear(self) -> int:
        if self.isEmpty():
            return -1
        tail = (self.head + self.count - 1) % self.k
        return self.q[tail]

    def isEmpty(self) -> bool:
        return self.count == 0

    def isFull(self) -> bool:
        return self.count == self.k
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(1)$ for all 8 operations.<br>
<strong>Space:</strong> $O(k)$ — Fixed circular array.</p>
''',
642: '''<h2>🧭 How to think about it</h2>
<p>Design a search autocomplete system for a search engine. Users may input a sentence character by character. For each character typed (except <code>'#'</code> which terminates the sentence), return the top 3 historical hot sentences that have the same prefix as the sentence typed so far.</p>

<p><strong>Trie with Pre-sorted Top Suggestions:</strong>
Each <code>TrieNode</code> maintains:
- <code>children</code>: map of character to child node.
- <code>hotness</code>: a dictionary or list mapping <code>sentence -> total_frequency</code> across all sentences passing through this node.</p>
<p>When typing character <code>c</code>:
1. Advance cursor <code>curr = curr.children[c]</code>.
2. Sort candidate sentences in <code>curr.hotness</code> by <code>(-count, sentence)</code> and return top 3!
3. If <code>c == '#'</code>: record the full completed sentence into the Trie, increment count, and reset cursor to root!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Scanning all historical sentences on every keystroke takes $O(N \\log N)$. Storing sentence frequencies directly on Trie nodes provides rapid prefix retrieval.</p>

<div class="insight">💡 <strong>Key insight:</strong> Trie node caches sentence frequencies: <code>node.counts[sentence] += 1</code>. Top 3 suggestions are sorted by <code>(-frequency, ascii_sentence)</code>.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">class TrieNode:
    def __init__(self):
        self.children = {}
        self.counts = {} # sentence -> frequency

class AutocompleteSystem:
    def __init__(self, sentences: list[str], times: list[int]):
        self.root = TrieNode()
        self.curr_node = self.root
        self.curr_str = []
        
        for s, t in zip(sentences, times):
            self._insert(s, t)

    def _insert(self, sentence: str, count: int):
        curr = self.root
        for ch in sentence:
            if ch not in curr.children:
                curr.children[ch] = TrieNode()
            curr = curr.children[ch]
            curr.counts[sentence] = curr.counts.get(sentence, 0) + count

    def input(self, c: str) -> list[str]:
        if c == '#':
            sentence = "".join(self.curr_str)
            self._insert(sentence, 1)
            self.curr_str = []
            self.curr_node = self.root
            return []
            
        self.curr_str.append(c)
        if self.curr_node:
            self.curr_node = self.curr_node.children.get(c, None)
            
        if not self.curr_node:
            return []
            
        # Sort by: 1) frequency descending (-count), 2) ASCII ascending (s)
        candidates = sorted(self.curr_node.counts.items(), key=lambda x: (-x[1], x[0]))
        return [s for s, _ in candidates[:3]]
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> Typing a character: $O(K \\log K)$ where $K$ is number of candidate matches with this prefix. Adding sentence: $O(L)$ where $L$ is sentence length.<br>
<strong>Space:</strong> $O(N \\times L)$ — Trie nodes with sentence references.</p>
''',
705: '''<h2>🧭 How to think about it</h2>
<p>Design a HashSet without using any built-in hash table libraries.</p>

<p><strong>Separate Chaining with Prime Modulo:</strong>
Pick a large prime number for bucket count to minimize collision clustering (e.g. $B = 769$ or $B = 2069$).
Each bucket is a linked list or dynamic array.
- <code>hash(key) = key % B</code>
- <code>add(key)</code>: check if key exists in bucket; if not, append.
- <code>remove(key)</code>: remove key from bucket if present.
- <code>contains(key)</code>: linear scan inside bucket $key \\% B$.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Separate chaining with prime modulo ensures $O(1)$ average time per operation.</p>

<div class="insight">💡 <strong>Key insight:</strong> Array of buckets with prime length <code>769</code>: <code>bucket = buckets[key % 769]</code>. Append on add, remove on delete. Average $O(1)$!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">class MyHashSet:
    def __init__(self):
        self.buckets = 769
        self.table = [[] for _ in range(self.buckets)]

    def _hash(self, key: int) -> int:
        return key % self.buckets

    def add(self, key: int) -> None:
        idx = self._hash(key)
        if key not in self.table[idx]:
            self.table[idx].append(key)

    def remove(self, key: int) -> None:
        idx = self._hash(key)
        if key in self.table[idx]:
            self.table[idx].remove(key)

    def contains(self, key: int) -> bool:
        idx = self._hash(key)
        return key in self.table[idx]
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(1)$ average, $O(N / B)$ worst case with heavy collisions.<br>
<strong>Space:</strong> $O(K + B)$ where $K$ is total distinct keys and $B = 769$.</p>
''',
706: '''<h2>🧭 How to think about it</h2>
<p>Design a HashMap without using any built-in hash table libraries.</p>

<p>Similar to <code>MyHashSet</code> (LC 705), maintain $B = 769$ bucket lists storing <code>(key, value)</code> pairs.
- <code>put(key, value)</code>: hash to bucket. If key already exists in bucket, overwrite value. Otherwise, append <code>[key, value]</code>.
- <code>get(key)</code>: search bucket for key. Return value if found, else -1.
- <code>remove(key)</code>: remove <code>[key, value]</code> pair from bucket if present.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Separate chaining gives $O(1)$ amortized operations.</p>

<div class="insight">💡 <strong>Key insight:</strong> Bucket array storing <code>[key, val]</code> pairs: <code>idx = key % 769</code>. Overwrite on duplicate key, append on new key.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">class MyHashMap:
    def __init__(self):
        self.size = 769
        self.buckets = [[] for _ in range(self.size)]

    def _hash(self, key: int) -> int:
        return key % self.size

    def put(self, key: int, value: int) -> None:
        bucket = self.buckets[self._hash(key)]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))

    def get(self, key: int) -> int:
        bucket = self.buckets[self._hash(key)]
        for k, v in bucket:
            if k == key:
                return v
        return -1

    def remove(self, key: int) -> None:
        bucket = self.buckets[self._hash(key)]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                return
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(1)$ average for <code>put</code>, <code>get</code>, and <code>remove</code>.<br>
<strong>Space:</strong> $O(N + B)$ where $N$ is total pairs and $B = 769$.</p>
''',
715: '''<h2>🧭 How to think about it</h2>
<p>A Range Module is a module that tracks ranges of numbers. Design a data structure to add, query, and remove intervals in half-open intervals $[left, right)$.</p>

<p><strong>Disjoint Sorted Intervals:</strong>
Maintain intervals in sorted, non-overlapping order: <code>[[l1, r1], [l2, r2], ...]</code>.
- <code>addRange(left, right)</code>: Merge all intervals that overlap or touch $[left, right)$ into one expanded interval.
- <code>queryRange(left, right)</code>: Binary search for the interval covering $left$. If that interval also satisfies $interval.right \\ge right$, return <code>True</code>!
- <code>removeRange(left, right)</code>: Split and trim any intervals that intersect with $[left, right)$.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Using a sorted list with binary search (<code>bisect</code>) allows $O(\\log N)$ search and $O(N)$ interval slicing.</p>

<div class="insight">💡 <strong>Key insight:</strong> Disjoint intervals array: binary search finds overlapping candidates in $O(\\log N)$. Merge overlapping blocks on <code>addRange</code>; punch holes on <code>removeRange</code>.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">import bisect

class RangeModule:
    def __init__(self):
        # Flat list of alternating boundary points: [l0, r0, l1, r1, ...]
        # Represents disjoint intervals [l0, r0), [l1, r1)...
        self.track = []

    def addRange(self, left: int, right: int) -> None:
        l = bisect.bisect_left(self.track, left)
        r = bisect.bisect_right(self.track, right)
        sub = []
        if l % 2 == 0:
            sub.append(left)
        if r % 2 == 0:
            sub.append(right)
        self.track[l:r] = sub

    def queryRange(self, left: int, right: int) -> bool:
        l = bisect.bisect_right(self.track, left)
        r = bisect.bisect_left(self.track, right)
        return l % 2 == 1 and l == r

    def removeRange(self, left: int, right: int) -> None:
        l = bisect.bisect_left(self.track, left)
        r = bisect.bisect_right(self.track, right)
        sub = []
        if l % 2 == 1:
            sub.append(left)
        if r % 2 == 1:
            sub.append(right)
        self.track[l:r] = sub
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> <code>queryRange</code>: $O(\\log N)$ binary search. <code>addRange</code>, <code>removeRange</code>: $O(N)$ array slice.<br>
<strong>Space:</strong> $O(N)$ — Disjoint interval boundaries.</p>
''',

900: '''<h2>🧭 How to think about it</h2>
<p>We can use run-length encoding (RLE) to encode a sequence of integers. Design an iterator that iterates through a run-length encoded sequence given by <code>encoding</code> where even indices are counts and odd indices are values.</p>

<p>Maintain:
- <code>idx</code>: pointer to current count in <code>encoding</code>.
- During <code>next(n)</code>:
  While <code>idx < len(encoding)</code> and <code>n > 0</code>:
  - If <code>encoding[idx] >= n</code>: decrement <code>encoding[idx] -= n</code> and return <code>encoding[idx + 1]</code> (the value!).
  - If <code>encoding[idx] < n</code>: exhaust this entire run: <code>n -= encoding[idx]; idx += 2</code>.
  If we run out of elements, return -1!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Decompressing the entire sequence takes $O(\text{Total Counts})$ memory which exceeds 32-bit limits. The pointer consumes $O(1)$ auxiliary space and skips entire runs in $O(1)$!</p>

<div class="insight">💡 <strong>Key insight:</strong> Decrement counts directly in-place: subtract $n$ from <code>encoding[idx]</code>. If exhausted, advance <code>idx += 2</code>. Runs in $O(1)$ space!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">class RLEIterator:
    def __init__(self, encoding: list[int]):
        self.enc = encoding
        self.idx = 0

    def next(self, n: int) -> int:
        while self.idx < len(self.enc):
            if self.enc[self.idx] >= n:
                self.enc[self.idx] -= n
                return self.enc[self.idx + 1]
            else:
                n -= self.enc[self.idx]
                self.idx += 2
        return -1
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(1)$ amortized per <code>next()</code> call.<br>
<strong>Space:</strong> $O(1)$ auxiliary memory.</p>
''',
981: '''<h2>🧭 How to think about it</h2>
<p>Design a time-based key-value data structure that can store multiple values for the same key at different time stamps and retrieve the key's value at a certain timestamp.</p>

<p>Notice the critical constraint: <strong>All timestamps for <code>set</code> are strictly increasing!</strong>
Therefore, for each key, the list of <code>(timestamp, value)</code> pairs is <strong>already naturally sorted by timestamp</strong>!</p>
<p>To <code>get(key, timestamp)</code>:
1. Lookup the sorted list for <code>key</code> in a hash map: <code>history = data[key]</code>.
2. Use <strong>Binary Search (<code>bisect_right</code>)</strong> to find the largest timestamp $\\le \text{target timestamp}$ in $O(\\log N)$ time!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Linear scan of history takes $O(N)$ per query. Binary search evaluates in $O(\\log N)$ time.</p>

<div class="insight">💡 <strong>Key insight:</strong> Timestamps are monotonically increasing: store pairs <code>(timestamp, value)</code> in a list per key. Query with <code>bisect_right</code> in $O(\\log N)$!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">from collections import defaultdict
import bisect

class TimeMap:
    def __init__(self):
        # key -> list of (timestamp, value)
        self.data = defaultdict(list)

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.data[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        if key not in self.data:
            return ""
        history = self.data[key]
        # Binary search for rightmost timestamp <= query timestamp
        idx = bisect.bisect_right(history, (timestamp, chr(127))) - 1
        if idx >= 0:
            return history[idx][1]
        return ""
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> <code>set</code>: $O(1)$ append. <code>get</code>: $O(\\log N)$ binary search.<br>
<strong>Space:</strong> $O(Total \\; Sets)$ — List storage per key.</p>
''',
1146: '''<h2>🧭 How to think about it</h2>
<p>Implement a SnapshotArray that supports pre-allocating an array of length <code>length</code>, taking <code>snap()</code> which returns snapshot id, <code>set(index, val)</code>, and <code>get(index, snap_id)</code>.</p>

<p>Do NOT copy the entire array of size 50,000 on every snapshot ($O(N \\times S)$ would memory limit exceed!).
Instead, maintain history <strong>per index</strong>:
<code>history[index] = [(snap_id, val)]</code></p>
<p>- <code>snap()</code>: simply increments a global integer counter <code>curr_snap_id += 1</code> in $O(1)$!
- <code>set(index, val)</code>: append <code>(curr_snap_id, val)</code> to <code>history[index]</code>.
- <code>get(index, snap_id)</code>: run binary search (<code>bisect_right</code>) on <code>history[index]</code> to find the latest value recorded at or before <code>snap_id</code> in $O(\\log S)$!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Copying the array on snapshot takes $O(N)$ time and space per snapshot. Per-index version lists take $O(1)$ for <code>snap</code> and $O(\\log S)$ for <code>get</code>.</p>

<div class="insight">💡 <strong>Key insight:</strong> Version history per cell: <code>history[idx].append((snap_id, val))</code>. Binary search finds state at any past snapshot in $O(\\log S)$ time.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">import bisect

class SnapshotArray:
    def __init__(self, length: int):
        self.snap_id = 0
        # For each index: list of (snap_id, val)
        self.history = [[(0, 0)] for _ in range(length)]

    def set(self, index: int, val: int) -> None:
        if self.history[index][-1][0] == self.snap_id:
            # Overwrite value in current active snapshot
            self.history[index][-1] = (self.snap_id, val)
        else:
            self.history[index].append((self.snap_id, val))

    def snap(self) -> int:
        self.snap_id += 1
        return self.snap_id - 1

    def get(self, index: int, snap_id: int) -> int:
        hist = self.history[index]
        # Binary search for rightmost entry with recorded_snap <= query snap_id
        idx = bisect.bisect_right(hist, (snap_id, float('inf'))) - 1
        return hist[idx][1]
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> <code>set</code>: $O(1)$. <code>snap</code>: $O(1)$. <code>get</code>: $O(\\log S)$ where $S$ is mutations per index.<br>
<strong>Space:</strong> $O(N + \text{Total Sets})$ — Only modified cells consume memory.</p>
''',
1348: '''<h2>🧭 How to think about it</h2>
<p>A social media company wants to track frequency of tweets. Implement <code>recordTweet(tweetName, time)</code> and <code>getTweetCountsPerFrequency(freq, tweetName, startTime, endTime)</code> where <code>freq</code> is <code>"minute"</code> (60s), <code>"hour"</code> (3600s), or <code>"day"</code> (86400s).</p>

<p>For each <code>tweetName</code>, maintain a sorted list of tweet timestamps (or insert using <code>bisect.insort</code>).
During query:
1. Bucket interval length $\\Delta = 60, 3600, \text{or } 86400$.
2. Total chunks $k = (endTime - startTime) // \\Delta + 1$.
3. Binary search for timestamps in range $[startTime, endTime]$.
4. For each timestamp $t$, map it into chunk index: <code>chunk = (t - startTime) // delta</code> and increment <code>res[chunk] += 1</code>.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Sorting or maintaining binary search lists ensures queries inspect only relevant timestamps in $O(\\log N + M)$ time.</p>

<div class="insight">💡 <strong>Key insight:</strong> Sorted timestamps: binary search slice $[start, end]$, map each timestamp into bucket <code>(t - start) // delta</code> in $O(M)$ time.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">from collections import defaultdict
import bisect

class TweetCounts:
    def __init__(self):
        self.tweets = defaultdict(list)

    def recordTweet(self, tweetName: str, time: int) -> None:
        bisect.insort(self.tweets[tweetName], time)

    def getTweetCountsPerFrequency(self, freq: str, tweetName: str, startTime: int, endTime: int) -> list[int]:
        delta = 60 if freq == "minute" else (3600 if freq == "hour" else 86400)
        chunks = (endTime - startTime) // delta + 1
        res = [0] * chunks
        
        times = self.tweets[tweetName]
        l = bisect.bisect_left(times, startTime)
        r = bisect.bisect_right(times, endTime)
        
        for i in range(l, r):
            bucket = (times[i] - startTime) // delta
            res[bucket] += 1
            
        return res
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> <code>recordTweet</code>: $O(N)$ insertion. <code>getTweetCountsPerFrequency</code>: $O(\\log N + M)$ where $M$ is tweets in interval.<br>
<strong>Space:</strong> $O(N)$ timestamps stored per tweet.</p>
''',
1352: '''<h2>🧭 How to think about it</h2>
<p>Design an algorithm that accepts a stream of integers and retrieves the product of the last <code>k</code> integers of the stream in <strong>$O(1)$ time complexity</strong>!</p>

<p><strong>Prefix Product Array:</strong>
Let $prefix[i]$ be the cumulative product of all numbers up to index $i$.
The product of the last $k$ numbers is simply:
$$\text{Product} = \\frac{prefix[-1]}{prefix[-1 - k]}$$</p>

<p><strong>The Zero Reset Problem:</strong>
If a <code>0</code> is added to the stream:
Any product that includes that <code>0</code> will be 0! Any product that does NOT include that <code>0</code> will only look at numbers added <em>after</em> the 0!
Therefore, whenever <code>num == 0</code>:
Clear the prefix product array completely and reset <code>prefix = [1]</code>!
If a query requests $k \\ge \text{len}(prefix)$, it means the product spans across the zero, so return <code>0</code> immediately!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Multiplying last $k$ numbers takes $O(k)$ time. Prefix products calculate the quotient in strict $O(1)$ time.</p>

<div class="insight">💡 <strong>Key insight:</strong> Prefix products: <code>prefix.append(prefix[-1] * num)</code>. If $num == 0$, reset <code>prefix = [1]</code>. Product of last $k$ is <code>prefix[-1] // prefix[-1 - k]</code> in $O(1)$!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">class ProductOfNumbers:
    def __init__(self):
        self.prefix = [1]

    def add(self, num: int) -> None:
        if num == 0:
            # A zero invalidates all previous products
            self.prefix = [1]
        else:
            self.prefix.append(self.prefix[-1] * num)

    def getProduct(self, k: int) -> int:
        if k >= len(self.prefix):
            return 0
        return self.prefix[-1] // self.prefix[-1 - k]
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(1)$ for both <code>add</code> and <code>getProduct</code>.<br>
<strong>Space:</strong> $O(N)$ — Prefix product buffer.</p>
''',
1381: '''<h2>🧭 How to think about it</h2>
<p>Design a stack that supports <code>push</code>, <code>pop</code>, and incrementing the bottom <code>k</code> elements of the stack by <code>val</code> in <strong>$O(1)$ time complexity</strong>!</p>

<p>If we literally iterate through the bottom $k$ elements on every increment, <code>increment</code> takes $O(k)$ time.
<strong>The Lazy Propagation Array:</strong>
Maintain a parallel array <code>inc = [0] * maxSize</code>:
When <code>increment(k, val)</code> is called:
Only add <code>val</code> to the boundary element at index $idx = \\min(k, \text{len}(stack)) - 1$:
<code>inc[idx] += val</code>!</p>
<p>When <code>pop()</code> is called:
1. The popped element value is: <code>stack[-1] + inc[-1]</code>.
2. <strong>Pass the lazy increment down to the element beneath it</strong>:
   If index $> 0$: <code>inc[i - 1] += inc[i]</code>!
3. Pop from stack and reset <code>inc</code> entry!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Lazy propagation reduces <code>increment</code> from $O(k)$ to strict $O(1)$ time while maintaining $O(1)$ <code>push</code> and <code>pop</code>.</p>

<div class="insight">💡 <strong>Key insight:</strong> Lazy propagation: record increment only at index $k-1$. On <code>pop()</code>, propagate the lazy increment down to index $k-2$. Strict $O(1)$!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">class CustomStack:
    def __init__(self, maxSize: int):
        self.max_size = maxSize
        self.stack = []
        self.inc = []

    def push(self, x: int) -> None:
        if len(self.stack) < self.max_size:
            self.stack.append(x)
            self.inc.append(0)

    def pop(self) -> int:
        if not self.stack:
            return -1
        idx = len(self.stack) - 1
        val = self.stack.pop() + self.inc[idx]
        lazy = self.inc.pop()
        if idx > 0:
            self.inc[idx - 1] += lazy
        return val

    def increment(self, k: int, val: int) -> None:
        if self.stack:
            idx = min(k, len(self.stack)) - 1
            self.inc[idx] += val
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(1)$ for <code>push</code>, <code>pop</code>, and <code>increment</code>.<br>
<strong>Space:</strong> $O(\text{maxSize})$ — Pre-allocated stack buffers.</p>
''',
1396: '''<h2>🧭 How to think about it</h2>
<p>An underground railway system is keeping track of customer travel times between stations. Design a system to support <code>checkIn(id, stationName, t)</code>, <code>checkOut(id, stationName, t)</code>, and <code>getAverageTime(startStation, endStation)</code>.</p>

<p>Maintain two hash maps:
1. <code>check_ins</code>: <code>userId -> (startStation, checkInTime)</code>.
2. <code>routes</code>: <code>(startStation, endStation) -> [total_travel_time, trip_count]</code>.</p>
<p>- On <code>checkIn</code>: record passenger entry in <code>check_ins[id]</code>.
- On <code>checkOut</code>: retrieve start info, compute duration $t - t_{in}$, add to <code>routes[(start, end)]</code>, and remove passenger from <code>check_ins</code>.
- On <code>getAverageTime</code>: return <code>total_time / trip_count</code> in $O(1)$!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Both check-ins and average queries execute in constant $O(1)$ time with zero historical trip scanning.</p>

<div class="insight">💡 <strong>Key insight:</strong> Two maps: active passenger states in <code>check_ins[id]</code>; accumulated route metrics in <code>routes[(start, end)] = [total_time, count]</code>. $O(1)$ throughout.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">class UndergroundSystem:
    def __init__(self):
        # id -> (station, time)
        self.check_ins = {}
        # (start, end) -> [total_time, count]
        self.routes = {}

    def checkIn(self, id: int, stationName: str, t: int) -> None:
        self.check_ins[id] = (stationName, t)

    def checkOut(self, id: int, stationName: str, t: int) -> None:
        start_station, start_time = self.check_ins.pop(id)
        route_key = (start_station, stationName)
        duration = t - start_time
        
        if route_key not in self.routes:
            self.routes[route_key] = [duration, 1]
        else:
            self.routes[route_key][0] += duration
            self.routes[route_key][1] += 1

    def getAverageTime(self, startStation: str, endStation: str) -> float:
        total_time, count = self.routes[(startStation, endStation)]
        return total_time / count
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(1)$ for <code>checkIn</code>, <code>checkOut</code>, and <code>getAverageTime</code>.<br>
<strong>Space:</strong> $O(P + S^2)$ where $P$ is active passengers and $S$ is number of stations.</p>
''',
1472: '''<h2>🧭 How to think about it</h2>
<p>You have a browser of one tab where you start on the <code>homepage</code> and you can visit another url, get back in the history number of steps and move forward in the history number of steps.</p>

<p><strong>Dynamic Array with Two Pointers:</strong>
Instead of two stacks (back stack and forward stack):
Maintain a single dynamic array <code>history</code> and two integer pointers:
- <code>curr</code>: current page index.
- <code>max_bound</code>: rightmost reachable history index.</p>
<p>- <code>visit(url)</code>: advance <code>curr += 1</code>. If <code>curr == len(history)</code>, append; otherwise overwrite <code>history[curr] = url</code>. Set <code>max_bound = curr</code> (clears forward history!).
- <code>back(steps)</code>: <code>curr = max(0, curr - steps)</code>. Return <code>history[curr]</code>.
- <code>forward(steps)</code>: <code>curr = min(max_bound, curr + steps)</code>. Return <code>history[curr]</code>.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Two stacks require moving elements back and forth. A pointer on a single array executes all three operations in $O(1)$ time.</p>

<div class="insight">💡 <strong>Key insight:</strong> Single array with <code>curr</code> and <code>max_bound</code> pointers. <code>visit</code> overwrites forward history. <code>back</code> and <code>forward</code> are simple $O(1)$ integer clamping!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">class BrowserHistory:
    def __init__(self, homepage: str):
        self.history = [homepage]
        self.curr = 0
        self.max_bound = 0

    def visit(self, url: str) -> None:
        self.curr += 1
        if self.curr < len(self.history):
            self.history[self.curr] = url
        else:
            self.history.append(url)
        self.max_bound = self.curr

    def back(self, steps: int) -> str:
        self.curr = max(0, self.curr - steps)
        return self.history[self.curr]

    def forward(self, steps: int) -> str:
        self.curr = min(self.max_bound, self.curr + steps)
        return self.history[self.curr]
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(1)$ for <code>visit</code>, <code>back</code>, and <code>forward</code>.<br>
<strong>Space:</strong> $O(N)$ where $N$ is total visited URLs.</p>
''',
1756: '''<h2>🧭 How to think about it</h2>
<p>Design a queue-like data structure that moves the most recently used element to the end of the queue. Support <code>fetch(k)</code> which moves the $k$-th element (1-indexed) to the end and returns it.</p>

<p><strong>Square Root Decomposition (or Fenwick Tree / Balanced BST):</strong>
With $n = 2000$, a standard list <code>pop(k-1)</code> and <code>append()</code> takes $O(n)$ time.
Using <strong>$\\sqrt{N}$ Buckets</strong>:
Divide the $n$ elements into $pprox \\sqrt{N}$ small buckets of size $pprox \\sqrt{N}$.
To fetch the $k$-th element:
1. Locate which bucket contains $k$ in $O(\\sqrt{N})$ time.
2. Pop element from that bucket and append to the last bucket.
3. If necessary, rebalance bucket sizes in $O(\\sqrt{N})$ time.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Python's dynamic array <code>list.pop(k-1)</code> and <code>append()</code> is extremely optimized in C and passes within 50ms for $N = 2000$. For $N = 10^5$, $\\sqrt{N}$ decomposition guarantees $O(\\sqrt{N})$ per fetch.</p>

<div class="insight">💡 <strong>Key insight:</strong> $\\sqrt{N}$ bucket decomposition or dynamic list slicing: fetch locates target in $O(\\sqrt{N})$, extracts, and appends to rear.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">class MRUQueue:
    def __init__(self, n: int):
        self.q = list(range(1, n + 1))

    def fetch(self, k: int) -> int:
        val = self.q.pop(k - 1)
        self.q.append(val)
        return val
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(n)$ worst case, $O(\\sqrt{n})$ with block decomposition.<br>
<strong>Space:</strong> $O(n)$ — Queue storage.</p>
''',
2013: '''<h2>🧭 How to think about it</h2>
<p>Design a data structure that counts the number of ways to form axis-aligned squares with given points. Support <code>add(point)</code> and <code>count(point)</code>.</p>

<p>Let the query point be $P_1 = (x_1, y_1)$.
A square is uniquely determined by choosing its <strong>diagonal opposite point</strong> $P_3 = (x_3, y_3)$!
Iterate over all existing points $(x_3, y_3)$:
1. A valid diagonal must satisfy: $|x_1 - x_3| == |y_1 - y_3|$ and $x_1 \ne x_3$.
2. Once $P_1$ and $P_3$ are chosen, the other two corners are <strong>fixed and mandatory</strong>:
   $$P_2 = (x_1, y_3) \\quad \text{and} \\quad P_4 = (x_3, y_1)$$
3. The number of squares formed with diagonal $(P_1, P_3)$ is:
   $$\text{count}(P_3) \\times \text{count}(P_2) \\times \text{count}(P_4)$$</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Checking all 3-tuples takes $O(N^3)$. Iterating only over diagonal points takes $O(N)$ where $N$ is distinct points added.</p>

<div class="insight">💡 <strong>Key insight:</strong> For query point $(x_1, y_1)$, iterate over all points $(x_3, y_3)$. If $|x_1 - x_3| == |y_1 - y_3| > 0$, multiply frequencies of $(x_1, y_3)$ and $(x_3, y_1)$!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">from collections import Counter

class DetectSquares:
    def __init__(self):
        self.pts = Counter()

    def add(self, point: list[int]) -> None:
        self.pts[tuple(point)] += 1

    def count(self, point: list[int]) -> int:
        x1, y1 = point
        total = 0
        
        # Iterate over all registered points as potential diagonal opposites
        for (x3, y3), count3 in self.pts.items():
            # Must form non-zero square diagonal
            if abs(x1 - x3) == abs(y1 - y3) and x1 != x3:
                p2 = (x1, y3)
                p4 = (x3, y1)
                if p2 in self.pts and p4 in self.pts:
                    total += count3 * self.pts[p2] * self.pts[p4]
                    
        return total
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> <code>add</code>: $O(1)$. <code>count</code>: $O(N)$ where $N$ is distinct points.<br>
<strong>Space:</strong> $O(N)$ — Frequency map of points.</p>
''',
2034: '''<h2>🧭 How to think about it</h2>
<p>Design a stock price fluctuation system that can receive out-of-order price records, correct existing prices, and retrieve <code>current()</code>, <code>maximum()</code>, and <code>minimum()</code> stock prices in $O(\\log N)$ time.</p>

<p><strong>Hash Map + Min/Max Heaps with Lazy Deletion:</strong>
1. <code>prices</code>: <code>timestamp -> latest_price</code> (authoritative ground truth!).
2. <code>max_timestamp</code>: scalar tracking the latest timestamp seen so far (for <code>current()</code> in $O(1)$).
3. <code>max_heap</code>: stores <code>(-price, timestamp)</code>.
4. <code>min_heap</code>: stores <code>(price, timestamp)</code>.</p>

<p><strong>Lazy Deletion on Heap Reads:</strong>
When retrieving <code>maximum()</code>:
While <code>-max_heap[0][0] != prices[max_heap[0][1]]</code>:
The heap top price is stale (it was updated later)! Discard it with <code>heappop()</code>!
Return the first valid top element!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Scanning all prices for min/max takes $O(N)$ per query. Two heaps with lazy garbage collection execute in $O(\\log N)$ time.</p>

<div class="insight">💡 <strong>Key insight:</strong> Hash map holds true latest price per timestamp. Min/max heaps discard stale entries lazily: <code>while heap[0].price != map[heap[0].time]: heappop()</code>.</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">import heapq

class StockPrice:
    def __init__(self):
        self.prices = {} # timestamp -> price
        self.latest_time = 0
        self.max_heap = [] # (-price, timestamp)
        self.min_heap = [] # (price, timestamp)

    def update(self, timestamp: int, price: int) -> None:
        self.prices[timestamp] = price
        self.latest_time = max(self.latest_time, timestamp)
        heapq.heappush(self.max_heap, (-price, timestamp))
        heapq.heappush(self.min_heap, (price, timestamp))

    def current(self) -> int:
        return self.prices[self.latest_time]

    def maximum(self) -> int:
        while -self.max_heap[0][0] != self.prices[self.max_heap[0][1]]:
            heapq.heappop(self.max_heap) # Discard stale entry
        return -self.max_heap[0][0]

    def minimum(self) -> int:
        while self.min_heap[0][0] != self.prices[self.min_heap[0][1]]:
            heapq.heappop(self.min_heap) # Discard stale entry
        return self.min_heap[0][0]
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> <code>update</code>, <code>maximum</code>, <code>minimum</code>: $O(\\log N)$ amortized. <code>current</code>: $O(1)$.<br>
<strong>Space:</strong> $O(N)$ — Map and heaps storing price history.</p>
''',
2296: '''<h2>🧭 How to think about it</h2>
<p>Design a text editor with a cursor that supports:
- <code>addText(text)</code>: Insert text at cursor.
- <code>deleteText(k)</code>: Delete up to $k$ characters to the left of cursor.
- <code>cursorLeft(k)</code>: Move cursor left up to $k$ times and return last min(10, len) characters to the left.
- <code>cursorRight(k)</code>: Move cursor right up to $k$ times and return last min(10, len) characters to the left.</p>

<p><strong>The Two Stacks (Gap Buffer) Pattern:</strong>
Maintain two stacks of characters:
- <code>left</code>: characters strictly to the left of the cursor.
- <code>right</code>: characters strictly to the right of the cursor (in reverse order, top of stack is immediately right of cursor!).</p>
<p>Operations:
- <code>addText(text)</code>: append characters to <code>left</code>.
- <code>deleteText(k)</code>: pop up to $k$ characters from <code>left</code> in $O(1)$!
- <code>cursorLeft(k)</code>: pop from <code>left</code> and push to <code>right</code> up to $k$ times.
- <code>cursorRight(k)</code>: pop from <code>right</code> and push to <code>left</code> up to $k$ times.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Single string slicing takes $O(N)$ per edit. The two-stack gap buffer executes all character additions and deletions in $O(k)$ time without shifting arrays.</p>

<div class="insight">💡 <strong>Key insight:</strong> Two stacks representing text to left and right of cursor. Moving cursor transfers characters between stacks in $O(1)$ per step!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">class TextEditor:
    def __init__(self):
        self.left = []
        self.right = []

    def addText(self, text: str) -> None:
        self.left.extend(list(text))

    def deleteText(self, k: int) -> int:
        num_delete = min(k, len(self.left))
        for _ in range(num_delete):
            self.left.pop()
        return num_delete

    def cursorLeft(self, k: int) -> str:
        num_move = min(k, len(self.left))
        for _ in range(num_move):
            self.right.append(self.left.pop())
        return "".join(self.left[-10:])

    def cursorRight(self, k: int) -> str:
        num_move = min(k, len(self.right))
        for _ in range(num_move):
            self.left.append(self.right.pop())
        return "".join(self.left[-10:])
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(k)$ for all operations where $k$ is characters added/moved.<br>
<strong>Space:</strong> $O(N)$ where $N$ is total text characters.</p>
''',
2336: '''<h2>🧭 How to think about it</h2>
<p>You have a set which contains all positive integers <code>[1, 2, 3, 4, 5, ...]</code>. Implement the <code>SmallestInfiniteSet</code> class:
- <code>popSmallest()</code>: Removes and returns the smallest integer.
- <code>addBack(num)</code>: Adds positive integer back into set if not already present.</p>

<p>You cannot store an infinite set in memory!
Instead, notice that all integers from $1$ to $\\infty$ are naturally present in increasing order.
Maintain:
1. <code>curr_smallest = 1</code>: pointer tracking the next virgin integer that has never been popped yet.
2. <code>added_back_heap</code>: Min-Heap storing numbers smaller than <code>curr_smallest</code> that were popped and subsequently added back!
3. <code>added_back_set</code>: Hash set to prevent duplicates in the heap.</p>

<p>- <code>popSmallest()</code>: If <code>added_back_heap</code> is non-empty, pop its smallest element. Otherwise, return <code>curr_smallest</code> and increment <code>curr_smallest += 1</code>!
- <code>addBack(num)</code>: Only add if $num < curr\\_smallest$ and $num \\notin added\\_back\\_set$!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Heap + pointer simulates an infinite set in $O(\\log K)$ time where $K$ is the count of re-added numbers.</p>

<div class="insight">💡 <strong>Key insight:</strong> Pointer <code>curr_smallest</code> tracks the infinite frontier. Min-heap stores re-added numbers that fall below the frontier. $O(\\log K)$ operations!</div>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">import heapq

class SmallestInfiniteSet:
    def __init__(self):
        self.curr_smallest = 1
        self.added_heap = []
        self.added_set = set()

    def popSmallest(self) -> int:
        if self.added_heap:
            val = heapq.heappop(self.added_heap)
            self.added_set.remove(val)
            return val
        res = self.curr_smallest
        self.curr_smallest += 1
        return res

    def addBack(self, num: int) -> None:
        if num < self.curr_smallest and num not in self.added_set:
            self.added_set.add(num)
            heapq.heappush(self.added_heap, num)
</code></pre>
</details>

<h2>Complexity</h2>
<p><strong>Time:</strong> $O(\\log K)$ for <code>popSmallest</code> and <code>addBack</code> where $K$ is re-added numbers.<br>
<strong>Space:</strong> $O(K)$ — Only stores numbers currently added back.</p>
''',
}