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
}
