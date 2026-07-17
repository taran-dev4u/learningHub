# Deep tutorials — Pattern P3: Linked List Manipulation (Session 3).
# Original teaching content written for this site. Keyed by LC number;
# content_problems.py merges this as (3, lc). build.py turns [[nn]] into links.
# Node convention: class ListNode: def __init__(self, val=0, next=None): ...

DEEP = {

# ============================================================ LC 24 — Swap Nodes in Pairs
24: '''
<h2>🧭 How to think about it</h2>
<p>Swap every two adjacent nodes: <code>1→2→3→4</code> becomes <code>2→1→4→3</code>. You're rewiring pointers, not values. The safe way to rewire linked-list edges near the front is a <strong>dummy node</strong> in front of the head, plus a <code>prev</code> pointer that always sits just before the pair being swapped.</p>

<h2>🐢 Brute force first</h2>
<p>You could copy values into a list, swap pairs, and write them back — but the problem is really about pointer surgery, and doing it in place is the point. One pass, O(1) space.</p>

<div class="insight">💡 <strong>Key insight:</strong> to swap nodes <code>a → b</code> into <code>b → a</code>, set <code>prev.next = b</code>, <code>a.next = b.next</code>, <code>b.next = a</code>. Then advance <code>prev</code> to <code>a</code> (now the second of the pair) and repeat.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Create <code>dummy → head</code>; <code>prev = dummy</code>.</li>
<li>While there are two nodes ahead (<code>prev.next</code> and <code>prev.next.next</code>): name them <code>a</code>, <code>b</code>.</li>
<li>Rewire <code>prev→b→a→(rest)</code>.</li>
<li>Advance <code>prev = a</code>.</li>
</ol>

<h2>🎞️ Visual dry run — 1→2→3→4</h2>
<pre class="viz">dummy→1→2→3→4 ; prev=dummy, a=1 b=2
rewire: dummy→2→1→3→4 ; prev=1
a=3 b=4 → 1→4→3 ; dummy→2→1→4→3
Result: 2→1→4→3</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def swapPairs(head):
    dummy = ListNode(0, head)
    prev = dummy
    while prev.next and prev.next.next:
        a = prev.next
        b = a.next
        a.next = b.next     # a points past b
        b.next = a          # b points back to a
        prev.next = b       # prev points to b (new first)
        prev = a            # a is now the tail of this pair
    return dummy.next</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — each node touched once. <strong>Space O(1)</strong> — pointer rewiring only.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Empty list or single node → the while condition is false; return unchanged.</li>
<li>Odd length → the last lonely node stays put.</li>
<li>Exactly two nodes → one swap.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Forgetting the dummy → head swap needs special-casing and gets messy.</li>
<li>Rewiring in the wrong order and losing the rest of the list (save <code>b.next</code> first).</li>
<li>Advancing <code>prev</code> by only one node.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Reverse in groups of k ([[25]]) generalizes this.</li>
<li>Swap by value instead of node → different (and usually discouraged).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[25]] · [[206]] · [[92]]</p>
''',

# ============================================================ LC 25 — Reverse Nodes in k-Group
25: '''
<h2>🧭 How to think about it</h2>
<p>Reverse the list in chunks of <code>k</code>; if the final chunk has fewer than <code>k</code> nodes, leave it as-is. Do it by first <strong>checking</strong> that <code>k</code> nodes remain, then reversing exactly those <code>k</code>, and reconnecting the reversed block to the pieces before and after.</p>

<h2>🐢 Brute force first</h2>
<p>Copy values into an array, reverse each k-block, write back — O(n) time and O(n) space, and it dodges the pointer work. The in-place version is the intended O(1)-space answer.</p>

<div class="insight">💡 <strong>Key insight:</strong> keep a <code>group_prev</code> before each block. Walk k nodes to confirm a full group exists and to find the node <em>after</em> the group (<code>kth.next</code>). Reverse the k nodes with the standard prev/cur loop, then splice: <code>group_prev.next</code> becomes the new head, and the old first node becomes the next <code>group_prev</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>dummy → head</code>; <code>group_prev = dummy</code>.</li>
<li>Find the k-th node from <code>group_prev</code>; if fewer than k remain, stop.</li>
<li>Reverse the k nodes; reconnect the block between the previous and next segments.</li>
<li>Move <code>group_prev</code> to the block's new tail.</li>
</ol>

<h2>🎞️ Visual dry run — 1→2→3→4→5, k = 2</h2>
<pre class="viz">group1 [1,2] reversed → 2→1 ; dummy→2→1→3→4→5 ; group_prev=1
group2 [3,4] reversed → 4→3 ; ...→1→4→3→5 ; group_prev=3
group3 [5] &lt; k → leave
Result: 2→1→4→3→5</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def reverseKGroup(head, k):
    dummy = ListNode(0, head)
    group_prev = dummy
    while True:
        # find the k-th node ahead of group_prev
        kth = group_prev
        for _ in range(k):
            kth = kth.next
            if not kth:
                return dummy.next        # fewer than k left → done
        group_next = kth.next
        # reverse the k nodes [group_prev.next .. kth]
        prev, cur = group_next, group_prev.next
        while cur != group_next:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt
        # reconnect: old first node is the new tail
        new_tail = group_prev.next
        group_prev.next = kth            # kth is the new head of the block
        group_prev = new_tail</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — each node is visited a constant number of times. <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li><code>k = 1</code> → no change.</li>
<li>Length not divisible by k → the short tail is left untouched.</li>
<li>Length &lt; k → whole list unchanged.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Reversing before confirming a full group of k exists.</li>
<li>Losing the connection to <code>group_next</code> — reverse toward it as the sentinel.</li>
<li>Forgetting to update <code>group_prev</code> to the block's new tail.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Swap pairs is k = 2 ([[24]]).</li>
<li>Reverse the leftover tail too → drop the "full group" check.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[24]] · [[206]] · [[92]]</p>
''',

# ============================================================ LC 82 — Remove Duplicates from Sorted List II
82: '''
<h2>🧭 How to think about it</h2>
<p>The list is sorted; remove <em>every</em> node that has a duplicate, leaving only values that appeared exactly once (<code>1→2→3→3→4→4→5</code> → <code>1→2→5</code>). Because the head itself can be deleted, use a <strong>dummy</strong> before it, and a <code>prev</code> pointing at the last confirmed-unique node.</p>

<h2>🐢 Brute force first</h2>
<p>Count values with a dict, then rebuild keeping count-1 values → O(n) time, O(n) space. Since the list is sorted, a single in-place pass with O(1) space works.</p>

<div class="insight">💡 <strong>Key insight:</strong> when <code>cur</code> starts a run of equal values, skip the whole run, then link <code>prev.next</code> past it. If <code>cur</code> had no duplicate, just advance <code>prev</code>. The dummy lets <code>prev</code> start "before the head" so deleting the first node is uniform.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>dummy → head</code>; <code>prev = dummy</code>, <code>cur = head</code>.</li>
<li>If <code>cur</code> and <code>cur.next</code> have equal values, advance <code>cur</code> past the entire run, then <code>prev.next = cur.next</code>.</li>
<li>Otherwise <code>prev = cur</code>.</li>
<li>Advance <code>cur</code>.</li>
</ol>

<h2>🎞️ Visual dry run — 1→2→3→3→4→4→5</h2>
<pre class="viz">prev=dummy cur=1 (unique) → prev=1
cur=2 (unique) → prev=2
cur=3, 3==3 → skip run to last 3 → prev.next = 4 ; cur=4
cur=4, 4==4 → skip run → prev.next = 5 ; cur=5
cur=5 unique → prev=5
Result: 1→2→5</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def deleteDuplicates(head):
    dummy = ListNode(0, head)
    prev, cur = dummy, head
    while cur:
        if cur.next and cur.val == cur.next.val:
            while cur.next and cur.val == cur.next.val:
                cur = cur.next          # walk to the end of the run
            prev.next = cur.next        # cut the whole run out
        else:
            prev = cur                  # cur is unique → keep it
        cur = cur.next
    return dummy.next</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — one pass. <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>All duplicates → empty list.</li>
<li>Duplicates at the head → the dummy handles deletion cleanly.</li>
<li>No duplicates → unchanged.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Advancing <code>prev</code> into a duplicate run (it must stay before the run).</li>
<li>Forgetting the dummy → head-deletion bugs.</li>
<li>Confusing this with [[83]], which keeps one copy of each value.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Keep one copy of each ([[83]]).</li>
<li>Unsorted input → count with a dict first.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[83]] · [[26]] · [[203]]</p>
''',

# ============================================================ LC 83 — Remove Duplicates from Sorted List
83: '''
<h2>🧭 How to think about it</h2>
<p>The list is sorted; collapse each run of equal values to a single node (<code>1→1→2→3→3</code> → <code>1→2→3</code>). Because you always keep the first of each value, no dummy is needed — just walk with one pointer and skip a node whenever it equals the next.</p>

<h2>🐢 Brute force first</h2>
<p>A set plus rebuild is O(n) space. Sorted order lets you compare neighbors and do it in place, O(1) space.</p>

<div class="insight">💡 <strong>Key insight:</strong> keep a single <code>cur</code>. If <code>cur.val == cur.next.val</code>, bypass the next node (<code>cur.next = cur.next.next</code>) without advancing <code>cur</code>, so a run of three-plus collapses. Otherwise move <code>cur</code> forward.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>cur = head</code>.</li>
<li>While <code>cur</code> and <code>cur.next</code>: if equal values, <code>cur.next = cur.next.next</code>; else <code>cur = cur.next</code>.</li>
</ol>

<h2>🎞️ Visual dry run — 1→1→2→3→3</h2>
<pre class="viz">cur=1, next=1 equal → skip → 1→2→3→3 (cur stays at 1)
cur=1, next=2 → advance cur=2
cur=2, next=3 → advance cur=3
cur=3, next=3 equal → skip → 1→2→3
Result: 1→2→3</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def deleteDuplicates(head):
    cur = head
    while cur and cur.next:
        if cur.val == cur.next.val:
            cur.next = cur.next.next    # drop the duplicate; keep cur
        else:
            cur = cur.next
    return head</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — one pass. <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Empty or single node → returned as-is.</li>
<li>All equal → collapses to one node.</li>
<li>No duplicates → unchanged.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Advancing <code>cur</code> after skipping — a run of 3+ then keeps a duplicate.</li>
<li>Confusing with [[82]], which removes all copies of duplicated values.</li>
<li>Null-dereference by not checking <code>cur.next</code>.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Remove all duplicated values entirely ([[82]]).</li>
<li>Array version ([[26]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[82]] · [[26]] · [[203]]</p>
''',

# ============================================================ LC 92 — Reverse Linked List II
92: '''
<h2>🧭 How to think about it</h2>
<p>Reverse only the sublist between positions <code>left</code> and <code>right</code> (1-indexed), leaving the rest intact. Walk to the node just before <code>left</code>, then repeatedly <strong>pull the node after the current one to the front of the sublist</strong> (head-insertion) until the sublist is flipped.</p>

<h2>🐢 Brute force first</h2>
<p>Collect the sublist values, reverse, and write back → O(n) time, O(n) space. The head-insertion method does it in one pass, O(1) space.</p>

<div class="insight">💡 <strong>Key insight:</strong> let <code>prev</code> be the node before position <code>left</code> and <code>cur</code> the first node of the sublist. Each step, take <code>cur.next</code> and splice it right after <code>prev</code>. After <code>right − left</code> such moves, the sublist is reversed and still stitched to both ends. A dummy keeps <code>left = 1</code> uniform.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>dummy → head</code>; walk <code>prev</code> to position <code>left−1</code>.</li>
<li><code>cur = prev.next</code>. Repeat <code>right − left</code> times: <code>move = cur.next</code>; <code>cur.next = move.next</code>; <code>move.next = prev.next</code>; <code>prev.next = move</code>.</li>
</ol>

<h2>🎞️ Visual dry run — 1→2→3→4→5, left=2, right=4</h2>
<pre class="viz">prev=1, cur=2
move 3 to front: 1→3→2→4→5 ; cur still 2
move 4 to front: 1→4→3→2→5
Result: 1→4→3→2→5</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def reverseBetween(head, left, right):
    dummy = ListNode(0, head)
    prev = dummy
    for _ in range(left - 1):
        prev = prev.next            # node before the sublist
    cur = prev.next                 # first node of the sublist
    for _ in range(right - left):
        move = cur.next             # node to hoist to the front
        cur.next = move.next
        move.next = prev.next
        prev.next = move
    return dummy.next</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — walk plus the reversals. <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li><code>left == right</code> → no reversal needed (loop runs zero times).</li>
<li>Reversing from the head (<code>left = 1</code>) → the dummy handles it.</li>
<li>Reversing to the tail → still correct.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Off-by-one walking <code>prev</code> (it must land at <code>left−1</code>).</li>
<li>Reversing <code>right − left + 1</code> times instead of <code>right − left</code>.</li>
<li>Not using a dummy and mishandling <code>left = 1</code>.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Reverse the whole list ([[206]]).</li>
<li>Reverse in k-groups ([[25]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[206]] · [[25]] · [[24]]</p>
''',

# ============================================================ LC 206 — Reverse Linked List
206: '''
<h2>🧭 How to think about it</h2>
<p>The fundamental linked-list move: flip every <code>.next</code> pointer to face backward. Walk the list once with two pointers, <code>prev</code> and <code>cur</code>; at each node, remember the next node, point <code>cur</code> back at <code>prev</code>, then slide both forward. When <code>cur</code> falls off the end, <code>prev</code> is the new head.</p>

<h2>🐢 Brute force first</h2>
<p>Push all nodes to a stack and rebuild, or collect values and rewrite → O(n) space. The in-place pointer flip is O(1) space and is the move you'll reuse everywhere.</p>

<div class="insight">💡 <strong>Key insight:</strong> before overwriting <code>cur.next</code>, save it in <code>nxt</code> so you don't lose the rest of the list. Then <code>cur.next = prev</code>; advance <code>prev = cur</code>, <code>cur = nxt</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>prev = None</code>, <code>cur = head</code>.</li>
<li>While <code>cur</code>: <code>nxt = cur.next</code>; <code>cur.next = prev</code>; <code>prev = cur</code>; <code>cur = nxt</code>.</li>
<li>Return <code>prev</code>.</li>
</ol>

<h2>🎞️ Visual dry run — 1→2→3</h2>
<pre class="viz">prev=None cur=1 : 1.next=None ; prev=1 cur=2
prev=1 cur=2    : 2.next=1    ; prev=2 cur=3
prev=2 cur=3    : 3.next=2    ; prev=3 cur=None
Return 3 → 3→2→1</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def reverseList(head):
    prev, cur = None, head
    while cur:
        nxt = cur.next      # save the rest before we overwrite
        cur.next = prev     # flip this pointer backward
        prev = cur          # advance prev
        cur = nxt           # advance cur
    return prev             # new head</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — one pass. <strong>Space O(1)</strong> (recursive version is O(n) call stack).</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Empty list → <code>prev</code> stays <code>None</code>.</li>
<li>Single node → returned unchanged.</li>
<li>Two nodes → one flip.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Overwriting <code>cur.next</code> before saving it → you lose the tail.</li>
<li>Returning <code>cur</code> (which is <code>None</code>) instead of <code>prev</code>.</li>
<li>Forgetting to advance both pointers.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Reverse a sublist ([[92]]) or k-groups ([[25]]).</li>
<li>Recursive reversal → elegant but O(n) stack.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[92]] · [[25]] · [[234]]</p>
''',

# ============================================================ LC 234 — Palindrome Linked List
234: '''
<h2>🧭 How to think about it</h2>
<p>Check whether the list reads the same forwards and backwards, ideally in O(1) space. Combine three primitives you already know: <strong>find the middle</strong> (fast/slow), <strong>reverse the second half</strong>, then <strong>walk the two halves in step</strong> comparing values.</p>

<h2>🐢 Brute force first</h2>
<p>Copy values into a list and check <code>vals == vals[::-1]</code> → O(n) time, O(n) space. The three-primitive method gets O(1) space.</p>

<div class="insight">💡 <strong>Key insight:</strong> a slow/fast pass lands <code>slow</code> at the middle; reverse everything from there. Now the first half and the reversed second half start at both ends — compare node by node. (Optionally restore the list by reversing back.)</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Fast/slow to reach the middle.</li>
<li>Reverse the second half starting at <code>slow</code>.</li>
<li>Compare the front half with the reversed back half value by value.</li>
</ol>

<h2>🎞️ Visual dry run — 1→2→2→1</h2>
<pre class="viz">middle: slow lands at second 2
reverse second half: 1→2 | 1→2  (back half now 1→2 reversed)
compare front 1,2 with back 1,2 → all equal → True</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def isPalindrome(head):
    # 1) find middle
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    # 2) reverse second half
    prev = None
    while slow:
        nxt = slow.next
        slow.next = prev
        prev = slow
        slow = nxt
    # 3) compare halves
    left, right = head, prev
    while right:                 # right half is shorter or equal
        if left.val != right.val:
            return False
        left = left.next
        right = right.next
    return True</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — find + reverse + compare are each linear. <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Empty or single node → palindrome.</li>
<li>Odd length → the middle node belongs to neither half; comparing until the shorter (<code>right</code>) ends handles it.</li>
<li>Restoring the list → reverse the second half back if the caller needs it intact.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Comparing until <code>left</code> ends (it may be longer for odd lengths) — loop on <code>right</code>.</li>
<li>Off-by-one in the middle for even vs odd lengths.</li>
<li>Falling back to O(n) space when O(1) was requested.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Reorder list uses the same middle+reverse ([[143]]).</li>
<li>Doubly linked list → compare from both ends directly.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[206]] · [[876]] · [[143]]</p>
''',

# ============================================================ LC 21 — Merge Two Sorted Lists
21: '''
<h2>🧭 How to think about it</h2>
<p>Weave two sorted lists into one sorted list. Use a <strong>dummy head</strong> to collect the result and a <code>tail</code> pointer; at each step attach whichever list's current node is smaller, and advance that list. When one runs out, attach the entire remaining tail of the other.</p>

<h2>🐢 Brute force first</h2>
<p>Concatenate and sort → O((m+n) log(m+n)). Since both inputs are already sorted, a single merge pass is O(m+n).</p>

<div class="insight">💡 <strong>Key insight:</strong> a dummy node removes the "which list starts the result" special case. Splice nodes (don't copy values), so it's O(1) extra space. The leftover of the non-empty list is already sorted — attach it wholesale.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>dummy</code>; <code>tail = dummy</code>.</li>
<li>While both lists non-empty: attach the smaller head to <code>tail</code>, advance that list and <code>tail</code>.</li>
<li>Attach whichever list remains.</li>
</ol>

<h2>🎞️ Visual dry run — l1=1→2→4, l2=1→3→4</h2>
<pre class="viz">1(l1)≤1(l2) → take l1 1 ; 1(l2)≤2 → take l2 1 ; 2≤3 → 2 ; 3≤4 → 3 ; 4≤4 → 4(l1) ; attach l2 tail 4
Result: 1→1→2→3→4→4</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def mergeTwoLists(l1, l2):
    dummy = ListNode()
    tail = dummy
    while l1 and l2:
        if l1.val &lt;= l2.val:
            tail.next = l1; l1 = l1.next
        else:
            tail.next = l2; l2 = l2.next
        tail = tail.next
    tail.next = l1 or l2        # attach the non-empty remainder
    return dummy.next</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(m+n)</strong> — each node spliced once. <strong>Space O(1)</strong> — no new nodes.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>One list empty → return the other.</li>
<li>Both empty → return <code>None</code>.</li>
<li>Equal values → <code>≤</code> keeps the merge stable.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Forgetting to attach the leftover tail.</li>
<li>Creating new nodes instead of splicing (wastes space).</li>
<li>Not advancing <code>tail</code>.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Merge k sorted lists ([[23]]) → heap or pairwise merge.</li>
<li>Merge sorted arrays ([[88]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[23]] · [[88]] · [[148]]</p>
''',

# ============================================================ LC 2 — Add Two Numbers
2: '''
<h2>🧭 How to think about it</h2>
<p>Two numbers are stored as linked lists with digits in <strong>reverse order</strong> (ones digit first). That's actually convenient: walk both lists together, adding digit by digit and carrying, exactly like grade-school addition — and the reversed order means you start where the carry starts.</p>

<h2>🐢 Brute force first</h2>
<p>Convert each list to an integer, add, convert back — works in Python but overflows in fixed-width languages and misses the point. The digit-by-digit merge is O(max(m,n)) and universal.</p>

<div class="insight">💡 <strong>Key insight:</strong> a <code>dummy</code> collects result nodes; a running <code>carry</code> spans steps. At each position add the two current digits (0 if a list ended) plus carry; the new digit is <code>total % 10</code>, the new carry is <code>total // 10</code>. Don't forget a final carry node.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>dummy</code>, <code>tail = dummy</code>, <code>carry = 0</code>.</li>
<li>While either list has nodes or <code>carry</code>: <code>total = a + b + carry</code>; append <code>total % 10</code>; <code>carry = total // 10</code>.</li>
<li>Advance whichever lists remain.</li>
</ol>

<h2>🎞️ Visual dry run — 2→4→3 (342) + 5→6→4 (465)</h2>
<pre class="viz">2+5=7 c0 → 7
4+6=10 → 0 c1
3+4+1=8 → 8
Result: 7→0→8  (807 = 342+465)</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def addTwoNumbers(l1, l2):
    dummy = ListNode()
    tail = dummy
    carry = 0
    while l1 or l2 or carry:
        a = l1.val if l1 else 0
        b = l2.val if l2 else 0
        total = a + b + carry
        carry, digit = divmod(total, 10)
        tail.next = ListNode(digit)
        tail = tail.next
        l1 = l1.next if l1 else None
        l2 = l2.next if l2 else None
    return dummy.next</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(max(m,n))</strong> — one pass over the longer list. <strong>Space O(max(m,n))</strong> for the result.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Different lengths → the shorter contributes 0 once exhausted.</li>
<li>Final carry (e.g., 5 + 5 = 10) → the <code>or carry</code> in the loop adds the leading 1.</li>
<li>One list is a single 0 → handled naturally.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Ending the loop before flushing a leftover carry.</li>
<li>Assuming equal lengths.</li>
<li>Converting to int in languages where it overflows.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Digits in forward order (Add Two Numbers II) → reverse first or use stacks.</li>
<li>Plus one on a list ([[369]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[369]] · [[66]] · [[21]]</p>
''',

# ============================================================ LC 369 — Plus One Linked List
369: '''
<h2>🧭 How to think about it</h2>
<p>The number's digits are in <strong>forward order</strong> (most significant first) and you must add 1. The carry, though, flows from the <em>last</em> digit backward — the opposite of the list's direction. The simplest robust approach: <strong>reverse</strong> the list, add one with a carry from the front, then reverse back.</p>

<h2>🐢 Brute force first</h2>
<p>Convert to int, add 1, rebuild — fine in Python but fragile elsewhere. The reverse-add-reverse (or a one-pass recursion) is the clean pointer solution.</p>

<div class="insight">💡 <strong>Key insight:</strong> after reversing, the least significant digit is first, so adding 1 and carrying is a straightforward forward walk (just like [[2]]). Reverse back to restore most-significant-first order. If a carry survives the end, append a new leading 1 (after the second reverse it becomes the head).</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Reverse the list.</li>
<li>Walk it adding <code>carry</code> (start 1); a digit &lt; 9 absorbs the carry and stops it; a 9 becomes 0 and carries on.</li>
<li>If carry remains at the end, append a node with value 1.</li>
<li>Reverse back and return.</li>
</ol>

<h2>🎞️ Visual dry run — 1→2→3  (123 + 1)</h2>
<pre class="viz">reverse → 3→2→1
add 1: 3→4 (carry gone) → 4→2→1
reverse back → 1→2→4
(9→9→9 → reversed 9→9→9 → all roll to 0 with carry → 0→0→0→1 → reverse → 1→0→0→0)</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def plusOne(head):
    def reverse(node):
        prev = None
        while node:
            nxt = node.next
            node.next = prev
            prev = node
            node = nxt
        return prev

    head = reverse(head)
    cur, carry = head, 1
    prev = None
    while cur:
        total = cur.val + carry
        cur.val = total % 10
        carry = total // 10
        prev = cur
        cur = cur.next
    if carry:
        prev.next = ListNode(1)     # new most-significant digit (still reversed)
    return reverse(head)</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — two reversals and one add pass. <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>All nines → grows a leading digit (999 → 1000).</li>
<li>Single node → 9 → 1→0.</li>
<li>No carry beyond the first digit → stops early logically (loop still finishes, carry 0).</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Trying to carry forward without reversing (carry direction fights the list).</li>
<li>Forgetting the all-nines new leading node.</li>
<li>Not reversing back before returning.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Recursive one-pass (carry returned up the stack) avoids reversing.</li>
<li>Array version ([[66]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[66]] · [[2]] · [[206]]</p>
''',

# ============================================================ LC 160 — Intersection of Two Linked Lists
160: '''
<h2>🧭 How to think about it</h2>
<p>Two lists may share a common tail; find the node where they first merge. The lengths before the join differ, so a naive lockstep walk misidentifies the meeting point. The elegant trick: send a pointer down each list, and when it reaches the end, <strong>redirect it to the other list's head</strong>. Both pointers then travel the same total distance and meet exactly at the intersection.</p>

<h2>🐢 Brute force first</h2>
<p>Put all nodes of one list in a set, then scan the other for the first shared node → O(m+n) time, O(m) space. The two-pointer switch achieves O(1) space.</p>

<div class="insight">💡 <strong>Key insight:</strong> pointer A walks <code>lenA</code> then <code>lenB</code>; pointer B walks <code>lenB</code> then <code>lenA</code>. Both cover <code>lenA + lenB</code> steps, so they arrive at the intersection simultaneously. If there's no intersection, they reach <code>None</code> together.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>a = headA</code>, <code>b = headB</code>.</li>
<li>While <code>a != b</code>: <code>a = a.next if a else headB</code>; <code>b = b.next if b else headA</code>.</li>
<li>Return <code>a</code> (the shared node, or <code>None</code>).</li>
</ol>

<h2>🎞️ Visual dry run — A: a1→a2→c1→c2, B: b1→b2→b3→c1→c2</h2>
<pre class="viz">a walks A then B; b walks B then A
after each covers lenA+lenB, both land on c1
Return c1</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def getIntersectionNode(headA, headB):
    a, b = headA, headB
    while a is not b:               # compare node identity, not value
        a = a.next if a else headB  # switch to the other list at the end
        b = b.next if b else headA
    return a                        # intersection node, or None</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(m+n)</strong> — at most two passes each. <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>No intersection → both become <code>None</code> at the same time; loop ends, returns <code>None</code>.</li>
<li>Intersection at the head of one list → still found.</li>
<li>Equal-length lists → they meet without needing the switch trick, but it still works.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Switching to your own head instead of the <em>other</em> list's head.</li>
<li>Comparing values instead of node identity (<code>is</code>).</li>
<li>Infinite loop if you forget the "no intersection → both hit None" termination.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Length-difference method → advance the longer list by the difference first.</li>
<li>Cycle-based questions ([[141]], [[142]]) share the two-pointer spirit.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[141]] · [[142]] · [[206]]</p>
''',

# ============================================================ LC 61 — Rotate List
61: '''
<h2>🧭 How to think about it</h2>
<p>Rotate the list right by <code>k</code> places. The clean trick: connect the tail to the head to form a <strong>ring</strong>, figure out where the new head should be, then break the ring there. Because rotating by the length is a no-op, reduce <code>k</code> modulo the length first.</p>

<h2>🐢 Brute force first</h2>
<p>Move the last node to the front, <code>k</code> times → O(n·k). Forming a ring and cutting once is O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> find the length <code>n</code> and the tail. Link <code>tail.next = head</code> (a ring). The new tail is <code>n − (k % n) − 1</code> steps from the old head; the node after it is the new head. Cut the ring there.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Count length <code>n</code> and reach the tail. If <code>k % n == 0</code>, return unchanged.</li>
<li>Make it circular: <code>tail.next = head</code>.</li>
<li>Walk <code>n − k%n − 1</code> steps to the new tail; new head is its <code>.next</code>.</li>
<li>Break: set new tail's <code>.next = None</code>.</li>
</ol>

<h2>🎞️ Visual dry run — 1→2→3→4→5, k = 2</h2>
<pre class="viz">n=5, k%n=2 ; ring: ...5→1...
new tail = n-k-1 = 2 steps from head → node 3
new head = 4 ; break after 3
Result: 4→5→1→2→3</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def rotateRight(head, k):
    if not head or not head.next:
        return head
    # length + tail
    n, tail = 1, head
    while tail.next:
        tail = tail.next
        n += 1
    k %= n
    if k == 0:
        return head
    tail.next = head                 # form a ring
    steps = n - k                     # new tail is steps-1 from head
    new_tail = head
    for _ in range(steps - 1):
        new_tail = new_tail.next
    new_head = new_tail.next
    new_tail.next = None              # cut the ring
    return new_head</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — count plus one walk. <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li><code>k</code> a multiple of n → unchanged.</li>
<li>Empty or single node → unchanged.</li>
<li><code>k &gt; n</code> → the modulo reduces it.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Forgetting <code>k %= n</code> → huge, wrong walks.</li>
<li>Off-by-one on the new-tail step count.</li>
<li>Not breaking the ring → an infinite list.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Rotate left by k → new tail is <code>k−1</code> from head.</li>
<li>Array rotation ([[189]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[189]] · [[206]] · [[143]]</p>
''',

# ============================================================ LC 86 — Partition List
86: '''
<h2>🧭 How to think about it</h2>
<p>Reorder so every node less than <code>x</code> comes before every node ≥ <code>x</code>, keeping the original relative order within each group. Build <strong>two separate chains</strong> — a "less" list and a "greater-or-equal" list — as you scan, then join them.</p>

<h2>🐢 Brute force first</h2>
<p>Collect values, stable-partition, rebuild → O(n) space. Two dummy-headed chains do it in place with O(1) extra.</p>

<div class="insight">💡 <strong>Key insight:</strong> keep two builder tails, <code>less</code> and <code>greater</code>, each starting at its own dummy. Append each node to the appropriate chain in order (that preserves stability). Finally link <code>less</code>'s tail to <code>greater</code>'s head and terminate the greater chain.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Two dummies: <code>less_head</code>, <code>greater_head</code>; tails point at them.</li>
<li>For each node: if <code>val &lt; x</code> append to <code>less</code>, else append to <code>greater</code>.</li>
<li><code>greater_tail.next = None</code>; <code>less_tail.next = greater_head.next</code>; return <code>less_head.next</code>.</li>
</ol>

<h2>🎞️ Visual dry run — 1→4→3→2→5→2, x = 3</h2>
<pre class="viz">less:    1 → 2 → 2
greater: 4 → 3 → 5
join → 1→2→2→4→3→5</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def partition(head, x):
    less_head = less = ListNode()
    greater_head = greater = ListNode()
    while head:
        if head.val &lt; x:
            less.next = head; less = less.next
        else:
            greater.next = head; greater = greater.next
        head = head.next
    greater.next = None                 # terminate the greater chain
    less.next = greater_head.next       # stitch less → greater
    return less_head.next</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — one pass. <strong>Space O(1)</strong> — nodes are relinked, not copied.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>All nodes on one side → the other chain is empty (dummy handles it).</li>
<li>Empty list → returns <code>None</code>.</li>
<li>Values equal to <code>x</code> → go to the "greater-or-equal" chain.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Forgetting <code>greater.next = None</code> → a cycle or trailing junk.</li>
<li>Breaking the stable order by inserting at heads instead of tails.</li>
<li>Using <code>≤</code> vs <code>&lt;</code> incorrectly for the pivot.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Three-way partition (Dutch flag on a list) → three chains.</li>
<li>Odd/even index split ([[328]]) is the same two-chain idea by position.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[328]] · [[21]] · [[75]]</p>
''',

# ============================================================ LC 138 — Copy List with Random Pointer
138: '''
<h2>🧭 How to think about it</h2>
<p>Deep-copy a list where each node has a <code>next</code> and a <code>random</code> pointer to any node (or null). The challenge is the random pointers: when you clone a node, the target of its random may not be cloned yet. Two clean solutions: a hash map from original→clone, or the <strong>interleaving</strong> trick that needs no extra map.</p>

<h2>🐢 Brute force first</h2>
<p>Hash map <code>old → new</code>: first pass creates clones, second pass wires <code>next</code> and <code>random</code> using the map → O(n) time, O(n) space. The interleave method gets O(1) extra space.</p>

<div class="insight">💡 <strong>Key insight (interleave):</strong> insert each clone right after its original (<code>A → A' → B → B' → …</code>). Now a clone's random is simply <code>original.random.next</code> — the copy sits next to the node it should point to. Finally unzip the two lists apart.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Pass 1: after each node, splice in a clone with the same value.</li>
<li>Pass 2: set each clone's <code>random = original.random.next</code> (if the original's random exists).</li>
<li>Pass 3: unzip — restore the originals' <code>next</code> and extract the clones' <code>next</code>.</li>
</ol>

<h2>🎞️ Visual dry run — A→B, A.random=B, B.random=B</h2>
<pre class="viz">interleave: A→A'→B→B'
randoms: A'.random = A.random.next = B'  ; B'.random = B.random.next = B'
unzip: originals A→B ; clones A'→B'</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def copyRandomList(head):
    if not head:
        return None
    # 1) interleave clones
    cur = head
    while cur:
        clone = Node(cur.val, cur.next, None)
        cur.next = clone
        cur = clone.next
    # 2) assign randoms
    cur = head
    while cur:
        if cur.random:
            cur.next.random = cur.random.next
        cur = cur.next.next
    # 3) unzip
    cur = head
    copy_head = head.next
    while cur:
        clone = cur.next
        cur.next = clone.next
        clone.next = clone.next.next if clone.next else None
        cur = cur.next
    return copy_head</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — three linear passes. <strong>Space O(1)</strong> extra (interleave) versus O(n) for the hash-map version.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Empty list → return <code>None</code>.</li>
<li>Random pointing to null → leave the clone's random null.</li>
<li>Random pointing to self → handled: <code>cur.random.next</code> is the clone of self.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Wiring randoms before all clones are interleaved.</li>
<li>Not fully restoring the original list's <code>next</code> during the unzip.</li>
<li>Forgetting the null check on <code>cur.random</code>.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Hash-map version → simpler to explain, O(n) space.</li>
<li>Clone a graph ([[133]]) uses the map idea generally.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[133]] · [[206]] · [[430]]</p>
''',

# ============================================================ LC 143 — Reorder List
143: '''
<h2>🧭 How to think about it</h2>
<p>Reorder <code>L0→L1→…→Ln</code> into <code>L0→Ln→L1→Ln−1→…</code> in place. It decomposes into three familiar primitives: <strong>find the middle</strong>, <strong>reverse the second half</strong>, and <strong>merge the two halves alternately</strong>.</p>

<h2>🐢 Brute force first</h2>
<p>Store nodes in an array and rewire by index from both ends → O(n) space. The three-primitive method is O(1) space.</p>

<div class="insight">💡 <strong>Key insight:</strong> after splitting at the middle and reversing the back half, you have two lists; zip them together taking one node from each in turn. Because the back half is reversed, alternating gives exactly the front-back-front-back pattern.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Fast/slow to find the middle; split into two halves.</li>
<li>Reverse the second half.</li>
<li>Merge the two halves alternately.</li>
</ol>

<h2>🎞️ Visual dry run — 1→2→3→4</h2>
<pre class="viz">middle split: 1→2 | 3→4
reverse back: 4→3
merge: 1→4→2→3
Result: 1→4→2→3</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def reorderList(head):
    if not head or not head.next:
        return
    # 1) middle (slow ends at first-half end)
    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    second = slow.next
    slow.next = None                # cut into two halves
    # 2) reverse second half
    prev = None
    while second:
        nxt = second.next
        second.next = prev
        prev = second
        second = nxt
    # 3) merge alternately
    first, second = head, prev
    while second:
        f_next, s_next = first.next, second.next
        first.next = second
        second.next = f_next
        first, second = f_next, s_next</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — each primitive is linear. <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>0/1/2 nodes → already reordered (early return or trivial).</li>
<li>Odd length → the middle node stays in the first half; merge ends cleanly.</li>
<li>Cutting the halves → must null-terminate the first half.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Not splitting the list (leaving both halves linked) → a cycle.</li>
<li>Off-by-one middle causing an unbalanced merge.</li>
<li>Losing <code>next</code> pointers during the alternate merge (save them first).</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Palindrome check reuses middle+reverse ([[234]]).</li>
<li>Fold from both ends by value → different problem.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[234]] · [[876]] · [[206]]</p>
''',

# ============================================================ LC 148 — Sort List
148: '''
<h2>🧭 How to think about it</h2>
<p>Sort a linked list in O(n log n). <strong>Merge sort</strong> is the natural fit: splitting a list is cheap (find the middle with fast/slow) and merging two sorted lists is the [[21]] routine you already know. Quicksort on lists is awkward because you can't index; merge sort wins.</p>

<h2>🐢 Brute force first</h2>
<p>Dump values into an array, sort, rebuild → O(n log n) time but O(n) space and it ignores the list structure. Top-down merge sort is O(n log n) with O(log n) stack; bottom-up reaches O(1) space.</p>

<div class="insight">💡 <strong>Key insight:</strong> recursively split the list in half (slow/fast finds the midpoint; cut it), sort each half, then merge. The merge is exactly Merge Two Sorted Lists.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Base case: 0 or 1 node → already sorted.</li>
<li>Find the middle, split into two halves.</li>
<li>Recursively sort both halves.</li>
<li>Merge the two sorted halves.</li>
</ol>

<h2>🎞️ Visual dry run — 4→2→1→3</h2>
<pre class="viz">split → [4→2] [1→3]
sort → [2→4] [1→3]
merge → 1→2→3→4</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def sortList(head):
    if not head or not head.next:
        return head
    # split at the middle
    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    mid = slow.next
    slow.next = None
    left = sortList(head)
    right = sortList(mid)
    # merge two sorted halves
    dummy = tail = ListNode()
    while left and right:
        if left.val &lt;= right.val:
            tail.next = left; left = left.next
        else:
            tail.next = right; right = right.next
        tail = tail.next
    tail.next = left or right
    return dummy.next</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n log n)</strong> — log n levels, O(n) merge each. <strong>Space O(log n)</strong> recursion stack (O(1) for the bottom-up iterative version).</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Empty or single node → returned directly.</li>
<li>Already sorted → still O(n log n) but merges are cheap.</li>
<li>Duplicates → the <code>≤</code> merge keeps them together.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Not cutting the list at the middle (<code>slow.next = None</code>) → infinite recursion.</li>
<li>Using <code>fast = head</code> instead of <code>head.next</code> can mis-split a 2-node list into an infinite loop.</li>
<li>Reaching for quicksort and struggling with partitioning a list.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Bottom-up merge sort → true O(1) space.</li>
<li>Merge k sorted lists ([[23]]).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[21]] · [[23]] · [[876]]</p>
''',

# ============================================================ LC 328 — Odd Even Linked List
328: '''
<h2>🧭 How to think about it</h2>
<p>Group nodes at odd <em>positions</em> before nodes at even positions, preserving order (this is about index parity, not value). Weave two chains as you walk: an <strong>odd</strong> chain and an <strong>even</strong> chain, then attach the even chain after the odd one.</p>

<h2>🐢 Brute force first</h2>
<p>Collect nodes into two lists by index and rebuild → O(n) space. Splicing in place with two moving tails is O(1) extra.</p>

<div class="insight">💡 <strong>Key insight:</strong> keep <code>odd</code> and <code>even</code> tails, with <code>even_head</code> remembered. Each iteration links <code>odd.next = even.next</code> (skip one) and advances, then <code>even.next = odd.next</code> and advances. When the even chain ends, point <code>odd.next</code> to <code>even_head</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>odd = head</code>, <code>even = head.next</code>, <code>even_head = even</code>.</li>
<li>While <code>even</code> and <code>even.next</code>: <code>odd.next = even.next</code>; <code>odd = odd.next</code>; <code>even.next = odd.next</code>; <code>even = even.next</code>.</li>
<li><code>odd.next = even_head</code>.</li>
</ol>

<h2>🎞️ Visual dry run — 1→2→3→4→5</h2>
<pre class="viz">odd chain: 1→3→5
even chain: 2→4
join → 1→3→5→2→4</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def oddEvenList(head):
    if not head or not head.next:
        return head
    odd = head
    even = even_head = head.next
    while even and even.next:
        odd.next = even.next        # next odd-position node
        odd = odd.next
        even.next = odd.next        # next even-position node
        even = even.next
    odd.next = even_head            # append evens after odds
    return head</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — one pass. <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>0/1/2 nodes → returned as-is or trivially split.</li>
<li>Odd vs even total length → the loop condition covers both.</li>
<li>Preserving order within each group → guaranteed by tail-appending.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Losing <code>even_head</code> before the join.</li>
<li>Interleaving by value instead of by position.</li>
<li>Null errors when <code>even</code> or <code>even.next</code> is missing.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Partition by a pivot value ([[86]]) is the same two-chain idea.</li>
<li>Group by index mod 3 → three chains.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[86]] · [[206]] · [[24]]</p>
''',

# ============================================================ LC 430 — Flatten a Multilevel Doubly Linked List
430: '''
<h2>🧭 How to think about it</h2>
<p>A doubly linked list where nodes may have a <code>child</code> list; flatten everything into one level, splicing each child list in <strong>right after its parent</strong> and before the parent's original <code>next</code>. It's a depth-first traversal with careful <code>prev</code>/<code>next</code>/<code>child</code> rewiring.</p>

<h2>🐢 Brute force first</h2>
<p>Recursively collect all values into a list and rebuild → loses the in-place requirement and O(1) space. A stack-based DFS splices in place.</p>

<div class="insight">💡 <strong>Key insight:</strong> walk the list; when a node has a child, remember its <code>next</code> (push it or hold it), splice the child list in (fix <code>next</code>/<code>prev</code>), and null out <code>child</code>. A stack naturally resumes the saved <code>next</code> when a branch ends.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Walk with <code>cur</code>. If <code>cur.child</code> exists: push <code>cur.next</code> (if any) to a stack.</li>
<li>Link <code>cur.next = cur.child</code>, <code>cur.child.prev = cur</code>, clear <code>cur.child</code>.</li>
<li>When <code>cur.next</code> is null and the stack is non-empty, pop and attach it (fixing <code>prev</code>).</li>
</ol>

<h2>🎞️ Visual dry run — 1↔2(child: 3↔4)↔5</h2>
<pre class="viz">at 2: child 3→4 ; push 5
splice: 1↔2↔3↔4 ; 2.child=None
reach 4 (next null), pop 5 → 4↔5
Result: 1↔2↔3↔4↔5</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def flatten(head):
    if not head:
        return None
    stack = []
    cur = head
    while cur:
        if cur.child:
            if cur.next:
                stack.append(cur.next)      # resume this later
            cur.next = cur.child            # splice child in
            cur.child.prev = cur
            cur.child = None
        if not cur.next and stack:
            nxt = stack.pop()               # branch ended → resume
            cur.next = nxt
            nxt.prev = cur
        cur = cur.next
    return head</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — each node visited once. <strong>Space O(d)</strong> for the stack, where <code>d</code> is the nesting depth.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Empty list → return <code>None</code>.</li>
<li>Child at the tail (no <code>next</code> to save) → nothing pushed.</li>
<li>Deeply nested children → the stack handles arbitrary depth.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Forgetting to set <code>child = None</code> after splicing.</li>
<li>Not fixing <code>prev</code> pointers (it's a doubly linked list).</li>
<li>Losing the parent's original <code>next</code> when there's a child.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Recursive DFS instead of an explicit stack.</li>
<li>Flatten a nested list iterator ([[341]]) is a cousin.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[138]] · [[206]] · [[143]]</p>
''',

# ============================================================ LC 707 — Design Linked List
707: '''
<h2>🧭 How to think about it</h2>
<p>Implement a linked list supporting <code>get</code>, <code>addAtHead</code>, <code>addAtTail</code>, <code>addAtIndex</code>, and <code>deleteAtIndex</code>. The single design decision that removes almost all edge cases is a <strong>dummy head</strong> plus a maintained <code>size</code> counter — then head, tail, and middle operations all become "walk to index and splice".</p>

<h2>🐢 Brute force first</h2>
<p>Backing it with a Python list makes <code>get</code> O(1) but insert/delete O(n) shifts. A genuine singly linked list gives O(1) head insert and clean pointer operations — and it's what the exercise wants you to practice.</p>

<div class="insight">💡 <strong>Key insight:</strong> a dummy node before the real head means "insert before index i" is uniform for i = 0 too: walk <code>pred</code> to the node before index i (starting at the dummy), then splice. Track <code>size</code> to validate indices in O(1).</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Keep <code>dummy</code> and <code>size</code>.</li>
<li><code>get(i)</code>: bounds-check, walk i+1 steps from dummy, return value.</li>
<li><code>addAtIndex(i, v)</code>: if <code>0 ≤ i ≤ size</code>, walk <code>pred</code> to index i−1 (dummy for i=0), splice a new node, <code>size += 1</code>.</li>
<li><code>deleteAtIndex(i)</code>: bounds-check, walk <code>pred</code>, bypass, <code>size −= 1</code>.</li>
</ol>

<h2>🎞️ Visual dry run — addAtHead(1), addAtTail(3), addAtIndex(1,2), get(1)</h2>
<pre class="viz">dummy→1 ; dummy→1→3 ; insert 2 at idx1 → dummy→1→2→3 ; get(1)=2</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>class MyLinkedList:
    def __init__(self):
        self.dummy = ListNode(0)
        self.size = 0

    def get(self, index):
        if index &lt; 0 or index &gt;= self.size:
            return -1
        cur = self.dummy.next
        for _ in range(index):
            cur = cur.next
        return cur.val

    def addAtIndex(self, index, val):
        if index &lt; 0 or index &gt; self.size:
            return
        pred = self.dummy
        for _ in range(index):
            pred = pred.next
        pred.next = ListNode(val, pred.next)
        self.size += 1

    def addAtHead(self, val): self.addAtIndex(0, val)
    def addAtTail(self, val): self.addAtIndex(self.size, val)

    def deleteAtIndex(self, index):
        if index &lt; 0 or index &gt;= self.size:
            return
        pred = self.dummy
        for _ in range(index):
            pred = pred.next
        pred.next = pred.next.next
        self.size -= 1</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time:</strong> <code>get</code>, <code>addAtIndex</code>, <code>deleteAtIndex</code> are O(index); <code>addAtHead</code> O(1). <strong>Space O(n)</strong> for the nodes.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li><code>addAtIndex(size, …)</code> → appends at the tail (allowed: <code>index == size</code>).</li>
<li>Out-of-range indices → <code>get</code> returns −1; add/delete no-op.</li>
<li>Empty list operations → the dummy keeps them safe.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Allowing <code>addAtIndex</code> only for <code>index &lt; size</code> — appending needs <code>index == size</code>.</li>
<li>Forgetting to update <code>size</code>.</li>
<li>Not using a dummy → head/tail special-casing bugs.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Doubly linked list with a tail pointer → O(1) tail insert, faster middle access.</li>
<li>LRU cache ([[146]]) builds on a doubly linked list + map.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[146]] · [[708]] · [[206]]</p>
''',

# ============================================================ LC 708 — Insert into a Sorted Circular Linked List
708: '''
<h2>🧭 How to think about it</h2>
<p>Insert a value into a sorted <strong>circular</strong> list so it stays sorted. Walk with <code>prev</code>/<code>cur</code> around the ring once, watching for the right gap: either between two ascending neighbors that bracket the value, or at the "seam" where the list wraps from its maximum back to its minimum.</p>

<h2>🐢 Brute force first</h2>
<p>Collect values, sort, rebuild the ring → O(n) space and destroys the structure. A single pointer walk splices in O(n) time, O(1) space.</p>

<div class="insight">💡 <strong>Key insight:</strong> as you traverse, insert when one of three things holds: (1) <code>prev.val ≤ value ≤ cur.val</code> (normal slot); (2) at the seam <code>prev.val &gt; cur.val</code> and the value is ≥ the max or ≤ the min (a new extreme); (3) you've looped all the way around (all values equal) — insert anywhere.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Empty list → make a single self-pointing node.</li>
<li>Walk <code>prev = head</code>, <code>cur = head.next</code>; check the three insert conditions.</li>
<li>Splice <code>prev.next = new</code>, <code>new.next = cur</code>; stop.</li>
<li>If a full loop passes with no slot, insert before returning to head.</li>
</ol>

<h2>🎞️ Visual dry run — ring 3→4→1 (sorted circular), insert 2</h2>
<pre class="viz">prev=3 cur=4: 3≤2≤4? no ; seam? 3&gt;4? no
prev=4 cur=1: seam 4&gt;1 ; 2≥max(4)? no ; 2≤min(1)? no → skip
prev=1 cur=3: 1≤2≤3 yes → insert between 1 and 3
Result: 3→4→1→2 (circular, sorted)</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def insert(head, insertVal):
    node = Node(insertVal)
    if not head:                       # empty → self-loop
        node.next = node
        return node
    prev, cur = head, head.next
    while True:
        if prev.val &lt;= insertVal &lt;= cur.val:
            break                       # normal in-between slot
        if prev.val &gt; cur.val:          # seam (max → min)
            if insertVal &gt;= prev.val or insertVal &lt;= cur.val:
                break                   # new max or new min
        if cur is head:                 # looped fully (all equal) → insert here
            break
        prev, cur = cur, cur.next
    prev.next = node
    node.next = cur
    return head</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — at most one full loop. <strong>Space O(1)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Empty list → create a self-referential node.</li>
<li>All values equal → the "looped fully" condition inserts after one lap.</li>
<li>New min or new max → inserted at the seam.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Infinite loop when all values are equal — needs the <code>cur is head</code> stop.</li>
<li>Mishandling the seam (max→min) insert for extremes.</li>
<li>Forgetting the empty-list self-loop.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Delete from a sorted circular list → similar seam care.</li>
<li>Insert into a non-circular sorted list → simpler (no seam).</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[707]] · [[21]] · [[86]]</p>
''',

# ============================================================ LC 1019 — Next Greater Node In Linked List
1019: '''
<h2>🧭 How to think about it</h2>
<p>For each node, find the value of the first later node that is strictly greater; 0 if none. "Next greater to the right" is the classic <strong>monotonic stack</strong> pattern — but it's on a list, so first turn the values into an array (or process while collecting), then use a decreasing stack of indices.</p>

<h2>🐢 Brute force first</h2>
<p>For each node scan all later nodes → O(n²). A monotonic stack resolves each node once → O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> keep a stack of indices whose "next greater" is still unknown, with their values decreasing down the stack. When a bigger value arrives, it is the answer for everything on top of the stack that's smaller — pop and fill them in.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Copy list values into an array <code>vals</code>; <code>res = [0]*n</code>.</li>
<li>For each index <code>i</code>: while the stack's top value &lt; <code>vals[i]</code>, pop and set its answer to <code>vals[i]</code>.</li>
<li>Push <code>i</code>. Leftover stack entries keep 0.</li>
</ol>

<h2>🎞️ Visual dry run — 2→1→5</h2>
<pre class="viz">vals=[2,1,5]
i=0 push0 (stack[0])
i=1 top val2&gt;1 → push1 (stack[0,1])
i=2 val5: pop1(val1)→res[1]=5 ; pop0(val2)→res[0]=5 ; push2
res=[5,5,0]</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def nextLargerNodes(head):
    vals = []
    while head:
        vals.append(head.val)
        head = head.next
    res = [0] * len(vals)
    stack = []                         # indices with unresolved next-greater
    for i, v in enumerate(vals):
        while stack and vals[stack[-1]] &lt; v:
            res[stack.pop()] = v        # v is the next greater for that index
        stack.append(i)
    return res</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — each index pushed and popped once. <strong>Space O(n)</strong> for the values array, result, and stack.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Strictly increasing list → everyone's next greater is the following node (stack empties each step).</li>
<li>Strictly decreasing → all answers 0.</li>
<li>Single node → [0].</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Using <code>≤</code> instead of <code>&lt;</code> — "greater" is strict.</li>
<li>Storing values instead of indices on the stack (you need to know which slot to fill).</li>
<li>Forgetting leftover indices default to 0.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Next greater in an array ([[496]], [[739]]).</li>
<li>Previous greater → scan the other direction.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[739]] · [[496]] · [[206]]</p>
''',

# ============================================================ LC 2487 — Remove Nodes From Linked List
2487: '''
<h2>🧭 How to think about it</h2>
<p>Remove every node that has a strictly greater value somewhere to its right. What survives is a <strong>non-increasing</strong> chain. The cleanest way: reverse the list, then keep a running maximum — drop any node below it — which is a monotonic-stack idea done in place; reverse back at the end.</p>

<h2>🐢 Brute force first</h2>
<p>For each node scan the rest for a larger value → O(n²). Reverse + running-max (or a monotonic stack) is O(n).</p>

<div class="insight">💡 <strong>Key insight:</strong> reversing makes "is there a bigger value to the right?" become "is there a bigger value already seen?" Walk the reversed list keeping the max so far; keep a node only if it's ≥ that max (and update the max). The kept nodes, reversed back, are the answer.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Reverse the list.</li>
<li>Walk it; keep a node if its value ≥ the running max, else drop it; update the max on keeps.</li>
<li>Reverse the kept chain back and return it.</li>
</ol>

<h2>🎞️ Visual dry run — 5→2→13→3→8</h2>
<pre class="viz">reverse → 8→3→13→2→5
walk keeping ≥ max: 8(max8) ; 3&lt;8 drop ; 13(max13) ; 2&lt;13 drop ; 5&lt;13 drop
kept reversed: 13→8 ... plus 5? no. kept = 8,13 → reverse → 13→8
Result: 13→8</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def removeNodes(head):
    def reverse(node):
        prev = None
        while node:
            nxt = node.next
            node.next = prev
            prev = node
            node = nxt
        return prev

    head = reverse(head)
    cur = head
    max_so_far = cur.val
    while cur.next:
        if cur.next.val &lt; max_so_far:
            cur.next = cur.next.next     # drop a smaller node
        else:
            cur = cur.next
            max_so_far = cur.val         # new running max
    return reverse(head)</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n)</strong> — two reversals and one filter pass. <strong>Space O(1)</strong> (an explicit monotonic stack would be O(n)).</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Strictly increasing list → only the last (largest) node survives.</li>
<li>Non-increasing already → nothing removed.</li>
<li>Single node → unchanged.</li>
</ul>

<h2>🐛 Common mistakes</h2>
<ul>
<li>Comparing with <code>≤</code> and dropping equal values (equal ones stay — "strictly greater" triggers removal).</li>
<li>Forgetting to reverse back.</li>
<li>Updating the running max on dropped nodes.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Monotonic-stack version without reversing (build the answer forward).</li>
<li>Next greater node ([[1019]]) uses the same monotonic idea.</li>
</ul>

<h2>🔗 Related problems</h2>
<p>[[1019]] · [[206]] · [[739]]</p>
''',

}
