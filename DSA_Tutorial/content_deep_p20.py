"""Deep tutorials for Pattern 20: Trie / Prefix Tree Patterns."""
DEEP = {}
DEEP[140] = """<h3>Problem Overview</h3>
<p>Given a string <code>s</code> and a dictionary of strings <code>wordDict</code>, add spaces in <code>s</code> to construct a sentence where each word is a valid dictionary word. Return all such possible sentences.</p>

<h3>Key Insights</h3>
<p>Store <code>wordDict</code> in a Trie (or HashSet) for $O(1)$ prefix matches. Use <strong>DFS with Memoization</strong>:
<code>memo[start_idx]</code> stores all valid sentence tails from index <code>start_idx</code> to end of string $s$.
At index $i$, match prefixes of $s[i:]$ against the Trie. For every matching word ending at $j$, recursively obtain sentences for $s[j:]$, prepending the matched word.</p>

<details>
<summary><strong>Python 3 Solution (DFS with Memoization)</strong></summary>
<div class="code-block">
<pre><code class="language-python">from typing import List

class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> List[str]:
        words = set(wordDict)
        memo = {}
        
        def dfs(start: int) -> List[str]:
            if start == len(s):
                return [""]
            if start in memo:
                return memo[start]
                
            res = []
            for end in range(start + 1, len(s) + 1):
                word = s[start:end]
                if word in words:
                    sub_sentences = dfs(end)
                    for sub in sub_sentences:
                        if sub:
                            res.append(word + " " + sub)
                        else:
                            res.append(word)
                            
            memo[start] = res
            return res
            
        return dfs(0)
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> $O(2^N)$ worst-case output sentences, bounded by memoization on non-matching subproblems.</li>
  <li><strong>Space Complexity:</strong> $O(N \times 2^N)$ to store sentences.</li>
</ul>"""

DEEP[208] = """<h3>Problem Overview</h3>
<p>Implement a trie with <code>insert</code>, <code>search</code>, and <code>startsWith</code> methods. A trie (pronounced "try") or prefix tree is a tree data structure used to efficiently store and retrieve keys in a dataset of strings.</p>

<h3>Key Insights</h3>
<p>Each <code>TrieNode</code> contains:
<ol>
  <li><code>children</code>: A dictionary or fixed-size array of size 26 mapping each character to its child <code>TrieNode</code>.</li>
  <li><code>is_end_of_word</code>: A boolean flag indicating whether the path from root to this node constitutes a complete stored word.</li>
</ol>
<ul>
  <li><code>insert(word)</code>: Traverse or create nodes character by character; mark final node as <code>is_end = True</code>.</li>
  <li><code>search(word)</code>: Traverse characters; return <code>True</code> if path exists and final node has <code>is_end == True</code>.</li>
  <li><code>startsWith(prefix)</code>: Traverse characters; return <code>True</code> if the entire prefix path exists (regardless of <code>is_end</code>).</li>
</ul></p>

<details>
<summary><strong>Python 3 Solution (Click to Expand)</strong></summary>
<div class="code-block">
<pre><code class="language-python">class TrieNode:
    __slots__ = ('children', 'is_end')
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
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> $O(L)$ for all operations (<code>insert</code>, <code>search</code>, <code>startsWith</code>), where $L$ is the length of the string.</li>
  <li><strong>Space Complexity:</strong> $O(N \times L)$ total nodes where $N$ is number of inserted words and $L$ is average word length.</li>
  <li><strong>Edge Cases:</strong> Single character strings, prefixes identical to existing words.</li>
</ul>"""

DEEP[211] = """<h3>Problem Overview</h3>
<p>Design a data structure that supports adding new words and finding if a string matches any previously added string, where <code>'.'</code> can match any letter.</p>

<h3>Key Insights</h3>
<p>Standard trie for insertion. For searching:
<ul>
  <li>If character is <code>'a' - 'z'</code>: Normal trie branch lookup.</li>
  <li>If character is <code>'.'</code>: Wildcard! Recursively branch DFS into <strong>all existing children</strong> of current node. If any child returns <code>True</code>, the search succeeds!</li>
</ul></p>

<details>
<summary><strong>Python 3 Solution (Trie + DFS Backtracking)</strong></summary>
<div class="code-block">
<pre><code class="language-python">class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class WordDictionary:
    def __init__(self):
        self.root = TrieNode()

    def addWord(self, word: str) -> None:
        curr = self.root
        for ch in word:
            if ch not in curr.children:
                curr.children[ch] = TrieNode()
            curr = curr.children[ch]
        curr.is_end = True

    def search(self, word: str) -> bool:
        def dfs(node: TrieNode, idx: int) -> bool:
            if idx == len(word):
                return node.is_end
            ch = word[idx]
            if ch == '.':
                for child in node.children.values():
                    if dfs(child, idx + 1):
                        return True
                return False
            else:
                if ch not in node.children:
                    return False
                return dfs(node.children[ch], idx + 1)
                
        return dfs(self.root, 0)
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> <code>addWord</code>: $O(L)$. <code>search</code>: $O(L)$ without wildcards, worst-case $O(26^L)$ if all characters are <code>'.'</code>.</li>
  <li><strong>Space Complexity:</strong> $O(N \times L)$ for trie.</li>
</ul>"""

DEEP[212] = """<h3>Problem Overview</h3>
<p>Given an $m \times n$ <code>board</code> of characters and a list of strings <code>words</code>, return all words on the board. Each word must be constructed from letters of sequentially adjacent cells (horizontally or vertically neighboring). The same letter cell may not be used more than once in a word.</p>

<h3>Key Insights</h3>
<p>Running individual DFS for each word from every cell takes $O(W \times M \times N \times 4^L)$, which will TLE.</p>
<p><strong>Optimal Trie + Simultaneous DFS Backtracking:</strong>
<ol>
  <li>Build a Trie containing all words. Store the entire word string <code>node.word = word</code> at the terminal node for $O(1)$ result collection.</li>
  <li>Start DFS from every cell $(r, c)$. As we walk the grid, walk the Trie simultaneously!</li>
  <li><strong>Pruning (Crucial optimization):</strong> When a word is found, set <code>node.word = None</code> so it is not added again. If a node has no remaining children, prune it from its parent's <code>children</code> dict to prevent re-traversing dead branches!</li>
</ol></p>

<details>
<summary><strong>Python 3 Solution (Trie + In-Place Backtracking + Pruning)</strong></summary>
<div class="code-block">
<pre><code class="language-python">from typing import List

class TrieNode:
    def __init__(self):
        self.children = {}
        self.word = None

class Solution:
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        root = TrieNode()
        for w in words:
            curr = root
            for ch in w:
                if ch not in curr.children:
                    curr.children[ch] = TrieNode()
                curr = curr.children[ch]
            curr.word = w

        R, C = len(board), len(board[0])
        result = []

        def dfs(r: int, c: int, parent: TrieNode):
            ch = board[r][c]
            curr = parent.children.get(ch)
            if not curr:
                return

            if curr.word:
                result.append(curr.word)
                curr.word = None  # Avoid duplicates

            # Backtrack marker
            board[r][c] = '#'
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < R and 0 <= nc < C and board[nr][nc] != '#':
                    dfs(nr, nc, curr)
            board[r][c] = ch

            # Trie leaf pruning
            if not curr.children:
                del parent.children[ch]

        for r in range(R):
            for c in range(C):
                if board[r][c] in root.children:
                    dfs(r, c, root)

        return result
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> $O(M \times N \times 4^L)$ bounded heavily by Trie pruning.</li>
  <li><strong>Space Complexity:</strong> $O(\\sum |w|)$ for Trie nodes.</li>
</ul>"""

DEEP[336] = """<h3>Problem Overview</h3>
<p>Given a list of unique words, return all pairs of distinct indices <code>(i, j)</code> such that the concatenation <code>words[i] + words[j]</code> is a palindrome.</p>

<h3>Key Insights</h3>
<p>Checking every pair takes $O(N^2 \times L)$ (TLE).
Notice: For $w_1 + w_2$ to be a palindrome:
<ol>
  <li>If $|w_1| == |w_2|$, $w_2$ must be the exact reverse of $w_1$.</li>
  <li>If $|w_1| > |w_2|$, $w_1$ can be split into prefix + suffix:
    <ul>
      <li>If prefix is a palindrome, $w_2$ must be the reverse of suffix!</li>
      <li>If suffix is a palindrome, $w_2$ must be the reverse of prefix!</li>
    </ul>
  </li>
</ol>
We insert words into a hash map <code>{word: index}</code>. For each word, check all valid split points $k$ where one half is a palindrome and the reverse of the other half exists in our dictionary.</p>

<details>
<summary><strong>Python 3 Solution (Prefix/Suffix Palindrome Decomposition)</strong></summary>
<div class="code-block">
<pre><code class="language-python">from typing import List

class Solution:
    def palindromePairs(self, words: List[str]) -> List[List[int]]:
        def is_pal(s: str) -> bool:
            return s == s[::-1]
            
        word_to_idx = {w: i for i, w in enumerate(words)}
        res = []
        
        for i, w in enumerate(words):
            L = len(w)
            for j in range(L + 1):
                pref, suff = w[:j], w[j:]
                
                # Case 1: pref is palindrome -> need rev(suff) + pref + suff
                if is_pal(pref):
                    rev_suff = suff[::-1]
                    if rev_suff in word_to_idx and word_to_idx[rev_suff] != i:
                        res.append([word_to_idx[rev_suff], i])
                        
                # Case 2: suff is palindrome -> need pref + suff + rev(pref)
                # j < L avoids duplicate when j == L (already covered when j == 0)
                if j < L and is_pal(suff):
                    rev_pref = pref[::-1]
                    if rev_pref in word_to_idx and word_to_idx[rev_pref] != i:
                        res.append([i, word_to_idx[rev_pref]])
                        
        return res
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> $O(N \times L^2)$ where $N$ is number of words and $L$ is word length.</li>
  <li><strong>Space Complexity:</strong> $O(N \times L)$ hash map.</li>
  <li><strong>Edge Cases:</strong> Empty string <code>""</code> paired with any palindrome word.</li>
</ul>"""

DEEP[421] = """<h3>Problem Overview</h3>
<p>Given an integer array <code>nums</code>, return the maximum result of <code>nums[i] XOR nums[j]</code> where $0 \\le i \\le j < n$. Must run in $O(n)$ time.</p>

<h3>Key Insights</h3>
<p>A <strong>Binary Bitwise Trie</strong>:
Each number has 31 bits ($0 \\dots 30$). Insert all numbers into a Trie where branches are only $0$ and $1$.
To maximize $x \\oplus y$, for each bit of $x$ (from most significant bit 30 down to 0):
We greedily want the opposite bit $1 - bit$ to exist in the Trie!
If $1 - bit$ exists, we move to that branch and set the corresponding bit in XOR sum to 1. Otherwise, we are forced to take the matching bit.</p>

<details>
<summary><strong>Python 3 Solution (Binary Trie - O(31 * N))</strong></summary>
<div class="code-block">
<pre><code class="language-python">from typing import List

class TrieNode:
    __slots__ = ('children',)
    def __init__(self):
        self.children = [None, None]

class Solution:
    def findMaximumXOR(self, nums: List[int]) -> int:
        root = TrieNode()
        
        # 1. Insert all numbers into 31-bit Trie
        for num in nums:
            curr = root
            for bit_pos in range(30, -1, -1):
                bit = (num >> bit_pos) & 1
                if not curr.children[bit]:
                    curr.children[bit] = TrieNode()
                curr = curr.children[bit]
                
        # 2. Greedily find max XOR partner
        max_xor = 0
        for num in nums:
            curr = root
            curr_xor = 0
            for bit_pos in range(30, -1, -1):
                bit = (num >> bit_pos) & 1
                opp_bit = 1 - bit
                if curr.children[opp_bit]:
                    curr_xor |= (1 << bit_pos)
                    curr = curr.children[opp_bit]
                else:
                    curr = curr.children[bit]
            max_xor = max(max_xor, curr_xor)
            
        return max_xor
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> $O(31 \times N) = O(N)$ strictly linear time.</li>
  <li><strong>Space Complexity:</strong> $O(31 \times N)$ nodes.</li>
</ul>"""

DEEP[472] = """<h3>Problem Overview</h3>
<p>Given an array of strings <code>words</code> (without duplicates), return all the concatenated words in the given list of words. A concatenated word is a word that can be formed entirely by concatenating at least two shorter words of the given array.</p>

<h3>Key Insights</h3>
<p>Sort words by length ascending: <code>words.sort(key=len)</code>.
This guarantees that when evaluating word $w$, any shorter constituent word has already been processed and placed into our dictionary set <code>word_set</code>!
For each word, check if it can be partitioned into words in <code>word_set</code> using standard 1D Word Break DP:
$$dp[j] = \text{true if } \\exists i < j \text{ s.t. } dp[i] \text{ is true and } w[i:j] \\in word_set$$</p>

<details>
<summary><strong>Python 3 Solution (Click to Expand)</strong></summary>
<div class="code-block">
<pre><code class="language-python">from typing import List

class Solution:
    def findAllConcatenatedWordsInADict(self, words: List[str]) -> List[str]:
        words.sort(key=len)
        word_set = set()
        res = []
        
        def can_form(w: str) -> bool:
            if not word_set:
                return False
            n = len(w)
            dp = [False] * (n + 1)
            dp[0] = True
            for i in range(n):
                if not dp[i]:
                    continue
                for j in range(i + 1, n + 1):
                    if w[i:j] in word_set:
                        dp[j] = True
                if dp[n]:
                    return True
            return dp[n]
            
        for w in words:
            if can_form(w):
                res.append(w)
            word_set.add(w)
            
        return res
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> $O(N \\log N + N \times L^2)$.</li>
  <li><strong>Space Complexity:</strong> $O(N \times L)$.</li>
</ul>"""

DEEP[642] = """<h3>Problem Overview</h3>
<p>Design a search autocomplete system for a search engine. Users enter sentences character by character ending with <code>'#'</code>. Return the top 3 historical hot sentences that have prefix equal to the typed sentence so far, sorted by frequency descending, then lexicographical order ascending.</p>

<h3>Key Insights</h3>
<p>Each <code>TrieNode</code> stores a dictionary of sentence frequencies: <code>counts = defaultdict(int)</code>.
When typing character $c$:
<ul>
  <li>If <code>c == '#'</code>: Insert/increment full typed query in the trie, reset search pointer to root.</li>
  <li>If <code>c != '#'</code>: Walk to child node. The node directly contains all candidate sentences passing through it! Sort candidates with custom key <code>(-freq, sentence)</code> and return top 3.</li>
</ul></p>

<details>
<summary><strong>Python 3 Solution (Click to Expand)</strong></summary>
<div class="code-block">
<pre><code class="language-python">from typing import List
from collections import defaultdict
import heapq

class TrieNode:
    def __init__(self):
        self.children = {}
        self.counts = defaultdict(int)

class AutocompleteSystem:
    def __init__(self, sentences: List[str], times: List[int]):
        self.root = TrieNode()
        self.curr_node = self.root
        self.curr_input = []
        self.dead_end = False
        
        for s, t in zip(sentences, times):
            self._add(s, t)

    def _add(self, sentence: str, count: int) -> None:
        curr = self.root
        for ch in sentence:
            if ch not in curr.children:
                curr.children[ch] = TrieNode()
            curr = curr.children[ch]
            curr.counts[sentence] += count

    def input(self, c: str) -> List[str]:
        if c == '#':
            sentence = "".join(self.curr_input)
            self._add(sentence, 1)
            self.curr_node = self.root
            self.curr_input = []
            self.dead_end = False
            return []
            
        self.curr_input.append(c)
        if self.dead_end or c not in self.curr_node.children:
            self.dead_end = True
            return []
            
        self.curr_node = self.curr_node.children[c]
        # Extract top 3 candidates
        candidates = sorted(self.curr_node.counts.items(), key=lambda x: (-x[1], x[0]))
        return [sent for sent, _ in candidates[:3]]
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> $O(K \\log K)$ where $K$ is number of candidate sentences sharing the prefix.</li>
  <li><strong>Space Complexity:</strong> $O(N \times L)$ nodes and inverted index entries.</li>
</ul>"""

DEEP[648] = """<h3>Problem Overview</h3>
<p>Given a dictionary of root words and a sentence, replace all derivative words in the sentence with their shortest matching root word in the dictionary.</p>

<h3>Key Insights</h3>
<p>Store all roots in a Trie. For each word in the sentence:
Walk through its characters in the Trie. As soon as we encounter a node with <code>is_end == True</code>, we have found the shortest root prefix! Replace the word with this prefix immediately. If path terminates without finding an end, keep the original word.</p>

<details>
<summary><strong>Python 3 Solution (Click to Expand)</strong></summary>
<div class="code-block">
<pre><code class="language-python">from typing import List

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Solution:
    def replaceWords(self, dictionary: List[str], sentence: str) -> str:
        root = TrieNode()
        for word in dictionary:
            curr = root
            for ch in word:
                if ch not in curr.children:
                    curr.children[ch] = TrieNode()
                curr = curr.children[ch]
            curr.is_end = True
            
        def find_root(w: str) -> str:
            curr = root
            for i, ch in enumerate(w):
                if ch not in curr.children:
                    return w
                curr = curr.children[ch]
                if curr.is_end:
                    return w[:i + 1]
            return w
            
        return " ".join(find_root(w) for w in sentence.split())
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> $O(D \times L + S \times L)$ where $D$ is dictionary size, $S$ is number of sentence words.</li>
  <li><strong>Space Complexity:</strong> $O(D \times L)$ for Trie.</li>
</ul>"""

DEEP[677] = """<h3>Problem Overview</h3>
<p>Design a map that allows inserting a <code>(key, val)</code> pair (overwriting if key exists) and returning the sum of all values whose keys start with a given <code>prefix</code>.</p>

<h3>Key Insights</h3>
<p>Store a <code>sum_val</code> attribute on each <code>TrieNode</code> representing the total sum of all words passing through this node.
When inserting <code>(key, val)</code>:
<ol>
  <li>Find the difference $\\Delta = val - \text{old_val}$ (where $\text{old_val} = 0$ if key is new).</li>
  <li>Update the record in a hash map: <code>key_map[key] = val</code>.</li>
  <li>Traverse the trie path for <code>key</code>, adding $\\Delta$ to <code>curr.sum_val</code> at each node!</li>
</ol>
For <code>sum(prefix)</code>: Simply traverse to the prefix node and return its <code>sum_val</code> in $O(L)$ time!</p>

<details>
<summary><strong>Python 3 Solution (Prefix Sum Tracking on Nodes)</strong></summary>
<div class="code-block">
<pre><code class="language-python">class TrieNode:
    def __init__(self):
        self.children = {}
        self.sum_val = 0

class MapSum:
    def __init__(self):
        self.root = TrieNode()
        self.values = {}

    def insert(self, key: str, val: int) -> None:
        delta = val - self.values.get(key, 0)
        self.values[key] = val
        
        curr = self.root
        curr.sum_val += delta
        for ch in key:
            if ch not in curr.children:
                curr.children[ch] = TrieNode()
            curr = curr.children[ch]
            curr.sum_val += delta

    def sum(self, prefix: str) -> int:
        curr = self.root
        for ch in prefix:
            if ch not in curr.children:
                return 0
            curr = curr.children[ch]
        return curr.sum_val
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> $O(L)$ for both <code>insert</code> and <code>sum</code>.</li>
  <li><strong>Space Complexity:</strong> $O(N \times L)$ nodes.</li>
</ul>"""

DEEP[1032] = """<h3>Problem Overview</h3>
<p>Design an algorithm that accepts a stream of characters and checks if a suffix of these characters is a string of a given array of words.</p>

<h3>Key Insights</h3>
<p>A forward Trie requires maintaining a set of all active search pointers for every character in history, which explodes in size.
<strong>Reversed Word Trie:</strong>
Insert all dictionary words in <strong>reverse order</strong> into the Trie!
Keep a running stream history array <code>history</code>. When <code>query(letter)</code> is called, append letter to <code>history</code>, then walk backward from the end of <code>history</code> through the reversed Trie!
If we hit <code>node.is_end == True</code> at any point, a valid suffix match is found in $O(L)$ time.</p>

<details>
<summary><strong>Python 3 Solution (Reversed Suffix Trie)</strong></summary>
<div class="code-block">
<pre><code class="language-python">from typing import List

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class StreamChecker:
    def __init__(self, words: List[str]):
        self.root = TrieNode()
        self.history = []
        self.max_len = 0
        
        for w in words:
            self.max_len = max(self.max_len, len(w))
            curr = self.root
            for ch in reversed(w):
                if ch not in curr.children:
                    curr.children[ch] = TrieNode()
                curr = curr.children[ch]
            curr.is_end = True

    def query(self, letter: str) -> bool:
        self.history.append(letter)
        curr = self.root
        
        # Walk backward through history
        for i in range(len(self.history) - 1, -1, -1):
            ch = self.history[i]
            if ch not in curr.children:
                return False
            curr = curr.children[ch]
            if curr.is_end:
                return True
            if len(self.history) - i > self.max_len:
                break
                
        return False
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> $O(L)$ per query, where $L$ is max word length.</li>
  <li><strong>Space Complexity:</strong> $O(N \times L)$ nodes.</li>
</ul>"""

DEEP[1233] = """<h3>Problem Overview</h3>
<p>Given a list of folders, return the folders after removing all sub-folders in those folders. If a folder <code>folder[i]</code> is located within another <code>folder[j]</code>, it is called a sub-folder of it.</p>

<h3>Key Insights</h3>
<p>Sort the folders lexicographically: <code>folder.sort()</code>.
When sorted, any subfolder must appear immediately after its parent folder!
We only need to track the <code>last_added</code> folder. If current folder starts with <code>last_added + '/'</code>, it is a subfolder and we skip it. Otherwise, add it to result!</p>

<details>
<summary><strong>Python 3 Solution (Lexicographical Prefix Pruning)</strong></summary>
<div class="code-block">
<pre><code class="language-python">from typing import List

class Solution:
    def removeSubfolders(self, folder: List[str]) -> List[str]:
        folder.sort()
        res = []
        
        for f in folder:
            if not res or not f.startswith(res[-1] + '/'):
                res.append(f)
                
        return res
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> $O(N \\log N \times L)$ sorting + $O(N \times L)$ scan.</li>
  <li><strong>Space Complexity:</strong> $O(N \times L)$ for sorted list and results.</li>
</ul>"""

DEEP[1707] = """<h3>Problem Overview</h3>
<p>Given an array <code>nums</code> and <code>queries</code> where <code>queries[i] = [xi, mi]</code>, the answer is the maximum bitwise XOR of $x_i$ with any element in <code>nums</code> that is $\\le m_i$. If no such element exists, answer is -1.</p>

<h3>Key Insights</h3>
<p><strong>Offline Query Processing + Binary Trie:</strong>
Sort <code>nums</code> ascending.
Sort queries by $m_i$ ascending while preserving original query indices: <code>queries_sorted = sorted(enumerate(queries), key=lambda q: q[1][1])</code>.
As we process queries in increasing order of $m_i$, insert elements from <code>nums</code> that are $\\le m_i$ into the Binary Trie incrementally!
Query the Trie greedily using the standard $O(31)$ max XOR lookup.</p>

<details>
<summary><strong>Python 3 Solution (Offline Queries + Binary Trie)</strong></summary>
<div class="code-block">
<pre><code class="language-python">from typing import List

class TrieNode:
    __slots__ = ('children',)
    def __init__(self):
        self.children = [None, None]

class Solution:
    def maximizeXor(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        nums.sort()
        # queries with original index: (orig_idx, x, m)
        q_sorted = sorted([(i, q[0], q[1]) for i, q in enumerate(queries)], key=lambda item: item[2])
        
        root = TrieNode()
        ans = [-1] * len(queries)
        num_idx = 0
        n = len(nums)
        
        def insert(val: int):
            curr = root
            for bit_pos in range(30, -1, -1):
                bit = (val >> bit_pos) & 1
                if not curr.children[bit]:
                    curr.children[bit] = TrieNode()
                curr = curr.children[bit]
                
        def query_max_xor(x: int) -> int:
            if not root.children[0] and not root.children[1]:
                return -1
            curr = root
            res = 0
            for bit_pos in range(30, -1, -1):
                bit = (x >> bit_pos) & 1
                opp_bit = 1 - bit
                if curr.children[opp_bit]:
                    res |= (1 << bit_pos)
                    curr = curr.children[opp_bit]
                else:
                    curr = curr.children[bit]
            return res

        for orig_idx, x, m in q_sorted:
            while num_idx < n and nums[num_idx] <= m:
                insert(nums[num_idx])
                num_idx += 1
            ans[orig_idx] = query_max_xor(x)
            
        return ans
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> $O(N \\log N + Q \\log Q + 31 \times (N + Q))$.</li>
  <li><strong>Space Complexity:</strong> $O(31 \times N)$ Trie nodes + $O(Q)$ results.</li>
  <li><strong>Edge Cases:</strong> No elements $\\le m_i$ in <code>nums</code> (returns -1).</li>
</ul>"""

DEEP[1804] = """<h3>Problem Overview</h3>
<p>Extend the standard Trie to support:
<ul>
  <li><code>insert(word)</code>: Insert string <code>word</code> into trie.</li>
  <li><code>countWordsEqualTo(word)</code>: Return number of instances of <code>word</code> in trie.</li>
  <li><code>countWordsStartingWith(prefix)</code>: Return number of words that have <code>prefix</code> as prefix.</li>
  <li><code>erase(word)</code>: Erase one instance of <code>word</code> from trie.</li>
</ul></p>

<h3>Key Insights</h3>
<p>Each node maintains two counters:
<ol>
  <li><code>pass_count</code>: Incremented when inserting, decremented when erasing. Tells how many words pass through this node.</li>
  <li><code>end_count</code>: Incremented at the final character node when inserting, decremented when erasing. Tells how many exact words end here.</li>
</ol></p>

<details>
<summary><strong>Python 3 Solution (Click to Expand)</strong></summary>
<div class="code-block">
<pre><code class="language-python">class TrieNode:
    def __init__(self):
        self.children = {}
        self.pass_count = 0
        self.end_count = 0

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        curr = self.root
        curr.pass_count += 1
        for ch in word:
            if ch not in curr.children:
                curr.children[ch] = TrieNode()
            curr = curr.children[ch]
            curr.pass_count += 1
        curr.end_count += 1

    def countWordsEqualTo(self, word: str) -> int:
        curr = self.root
        for ch in word:
            if ch not in curr.children:
                return 0
            curr = curr.children[ch]
        return curr.end_count

    def countWordsStartingWith(self, prefix: str) -> int:
        curr = self.root
        for ch in prefix:
            if ch not in curr.children:
                return 0
            curr = curr.children[ch]
        return curr.pass_count

    def erase(self, word: str) -> None:
        curr = self.root
        curr.pass_count -= 1
        for ch in word:
            curr = curr.children[ch]
            curr.pass_count -= 1
        curr.end_count -= 1
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> $O(L)$ for all four operations.</li>
  <li><strong>Space Complexity:</strong> $O(N \times L)$.</li>
</ul>"""

DEEP[2185] = """<h3>Problem Overview</h3>
<p>Given an array of strings <code>words</code> and a string <code>pref</code>, return the number of strings in <code>words</code> that contain <code>pref</code> as a prefix.</p>

<h3>Key Insights</h3>
<p>Iterate through words and count how many start with <code>pref</code> using Python's <code>str.startswith(pref)</code>.</p>

<details>
<summary><strong>Python 3 Solution (Click to Expand)</strong></summary>
<div class="code-block">
<pre><code class="language-python">from typing import List

class Solution:
    def prefixCount(self, words: List[str], pref: str) -> int:
        return sum(1 for w in words if w.startswith(pref))
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> $O(N \times L)$ where $L = \text{len}(pref)$.</li>
  <li><strong>Space Complexity:</strong> $O(1)$.</li>
</ul>"""

DEEP[2416] = """<h3>Problem Overview</h3>
<p>The score of a string is the number of strings in <code>words</code> that have this string as a prefix. Given an array <code>words</code>, return an array <code>answer</code> where <code>answer[i]</code> is the sum of scores of every non-empty prefix of <code>words[i]</code>.</p>

<h3>Key Insights</h3>
<p>Build a Trie where each node records <code>count</code> (the number of words passing through it).
For each word:
Traverse its characters in the Trie; at each step, add <code>node.count</code> to the total sum of prefix scores for that word!</p>

<details>
<summary><strong>Python 3 Solution (Trie Prefix Frequency Accumulation)</strong></summary>
<div class="code-block">
<pre><code class="language-python">from typing import List

class TrieNode:
    __slots__ = ('children', 'count')
    def __init__(self):
        self.children = {}
        self.count = 0

class Solution:
    def sumPrefixScores(self, words: List[str]) -> List[int]:
        root = TrieNode()
        
        # 1. Insert and count prefix frequencies
        for w in words:
            curr = root
            for ch in w:
                if ch not in curr.children:
                    curr.children[ch] = TrieNode()
                curr = curr.children[ch]
                curr.count += 1
                
        # 2. Query prefix score sum
        ans = []
        for w in words:
            curr = root
            score = 0
            for ch in w:
                curr = curr.children[ch]
                score += curr.count
            ans.append(score)
            
        return ans
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> $O(N \times L)$ strictly linear in total characters.</li>
  <li><strong>Space Complexity:</strong> $O(N \times L)$ Trie nodes.</li>
</ul>"""

DEEP[2707] = """<h3>Problem Overview</h3>
<p>Given a 0-indexed string <code>s</code> and a dictionary of words <code>dictionary</code>, break <code>s</code> into one or more non-overlapping substrings such that each substring is in <code>dictionary</code>. Return the minimum number of extra characters left over.</p>

<h3>Key Insights</h3>
<p>1D Dynamic Programming:
Let $dp[i]$ be the minimum extra characters for the prefix $s[:i]$.
Base case: $dp[0] = 0$.
For index $i$ from 1 to $n$:
<ol>
  <li>Default option: Treat $s[i-1]$ as an extra character: $dp[i] = dp[i-1] + 1$.</li>
  <li>Try matching any dictionary word ending at $i$: If $s[j:i] \\in \text{dict}$, $dp[i] = \\min(dp[i], dp[j])$.</li>
</ol></p>

<details>
<summary><strong>Python 3 Solution (Click to Expand)</strong></summary>
<div class="code-block">
<pre><code class="language-python">from typing import List

class Solution:
    def minExtraChar(self, s: str, dictionary: List[str]) -> int:
        words = set(dictionary)
        n = len(s)
        dp = [0] * (n + 1)
        
        for i in range(1, n + 1):
            dp[i] = dp[i - 1] + 1
            for j in range(i):
                if s[j:i] in words:
                    dp[i] = min(dp[i], dp[j])
                    
        return dp[n]
</code></pre>
</div>
</details>

<h3>Complexity & Edge Cases</h3>
<ul>
  <li><strong>Time Complexity:</strong> $O(n^2)$ time with HashSet lookups.</li>
  <li><strong>Space Complexity:</strong> $O(n + D \times L)$.</li>
</ul>"""
