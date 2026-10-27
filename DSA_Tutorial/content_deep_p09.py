# -*- coding: utf-8 -*-
"""
Deep tutorials for Pattern 9: Graph Traversal Patterns (DFS & BFS).
Masterclass 12-step structured explanations with ASCII dry runs and complexity analyses.
"""

DEEP = {
# ============================================================ LC 200
200: '''<h2>🧭 How to think about it</h2>
<p>Given an <code>m x n</code> 2D binary grid <code>grid</code> representing a map of <code>'1'</code>s (land) and <code>'0'</code>s (water), return the number of islands. An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically.</p>

<h2>🐢 Brute force first</h2>
<p>Checking every pair of land cells for path connectivity via pairwise BFS takes O((m*n)^2). Suboptimal because connected components can be traversed in a single pass.</p>

<div class="insight">💡 <strong>Key insight:</strong> Iterate over every cell in the grid. When you encounter an unvisited land cell <code>'1'</code>, you have discovered a <strong>new island</strong>! Increment the island count, then immediately launch a DFS or BFS traversal from that cell to visit and "sink" (or mark visited) the entire connected component of land. Every cell is visited at most a constant number of times.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Initialize <code>islands = 0</code>. Let <code>m = len(grid), n = len(grid[0])</code>.</li>
<li>Iterate through row <code>r</code> from <code>0</code> to <code>m-1</code> and col <code>c</code> from <code>0</code> to <code>n-1</code>:</li>
<li>If <code>grid[r][c] == '1'</code>:
  <ul>
    <li>Increment <code>islands += 1</code>.</li>
    <li>Trigger <code>dfs(r, c)</code> to sink the island.</li>
  </ul>
</li>
<li>In <code>dfs(r, c)</code>:
  <ul>
    <li>Base case: if out of bounds (<code>r < 0 or r >= m or c < 0 or c >= n</code>) or <code>grid[r][c] != '1'</code>, return.</li>
    <li>Mark cell as visited: <code>grid[r][c] = '0'</code> (in-place modification avoids an extra visited set).</li>
    <li>Recursively call <code>dfs</code> on 4 neighbors: <code>(r+1, c), (r-1, c), (r, c+1), (r, c-1)</code>.</li>
  </ul>
</li>
<li>Return <code>islands</code>.</li>
</ol>

<h2>🎞️ Visual dry run — grid:</h2>
<pre class="viz">1 1 0 0
1 1 0 0
0 0 1 0
0 0 0 1

1. At (0,0)='1': islands=1. DFS sinks (0,0), (0,1), (1,0), (1,1) to '0'.
   Grid becomes:
   0 0 0 0
   0 0 0 0
   0 0 1 0
   0 0 0 1

2. Scan advances to (2,2)='1': islands=2. DFS sinks (2,2) to '0'.
3. Scan advances to (3,3)='1': islands=3. DFS sinks (3,3) to '0'.
Total islands = 3! ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def numIslands(grid):
    """
    Connected components count via in-place DFS flood fill.
    """
    if not grid or not grid[0]:
        return 0
        
    m, n = len(grid), len(grid[0])
    islands = 0
    
    def dfs(r, c):
        if r < 0 or r >= m or c < 0 or c >= n or grid[r][c] != '1':
            return
            
        # Sink the land cell to mark as visited
        grid[r][c] = '0'
        
        # Explore 4 orthogonal directions
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)
        
    for r in range(m):
        for c in range(n):
            if grid[r][c] == '1':
                islands += 1
                dfs(r, c)
                
    return islands</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(m * n)</strong> — Every cell is visited at most twice (once by nested loops, once by DFS). <strong>Space O(m * n)</strong> in worst-case recursion stack (e.g., grid full of land).</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Grid containing only water: returns 0.</li>
<li>Grid containing only land: returns 1 (sunk in first DFS).</li>
<li>1x1 grid with '0' or '1'.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Max Area of Island ([[695]]).</li>
<li>Number of Closed Islands ([[1254]]).</li>
<li>Surrounded Regions ([[130]]).</li>
</ul>''',

# ============================================================ LC 695
695: '''<h2>🧭 How to think about it</h2>
<p>You are given an <code>m x n</code> binary matrix <code>grid</code>. An island is a group of <code>1</code>'s connected 4-directionally. The area of an island is the number of cells with a value <code>1</code> in the island. Return the <strong>maximum area</strong> of an island in <code>grid</code>. If there is no island, return <code>0</code>.</p>

<h2>🐢 Brute force first</h2>
<p>Run full BFS from every cell tracking set of reachable cells → O((m*n)^2). Instead, DFS with in-place sinking counts each island's size in O(m * n) total time.</p>

<div class="insight">💡 <strong>Key insight:</strong> Modify the island-sinking DFS to return an integer: <code>1 + dfs(up) + dfs(down) + dfs(left) + dfs(right)</code>. When a new unvisited land cell is found, sink it and take the max area seen across all connected components!</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Initialize <code>max_area = 0</code>.</li>
<li>Define <code>dfs(r, c)</code>:
  <ul>
    <li>If <code>r, c</code> out of bounds or <code>grid[r][c] == 0</code>, return 0.</li>
    <li>Sink cell: <code>grid[r][c] = 0</code>.</li>
    <li>Return <code>1 + dfs(r+1, c) + dfs(r-1, c) + dfs(r, c+1) + dfs(r, c-1)</code>.</li>
  </ul>
</li>
<li>Iterate through every cell <code>(r, c)</code>: if <code>grid[r][c] == 1</code>, <code>max_area = max(max_area, dfs(r, c))</code>.</li>
<li>Return <code>max_area</code>.</li>
</ol>

<h2>🎞️ Visual dry run — grid:</h2>
<pre class="viz">0 1 1 0
0 1 0 0
0 0 0 1

Island 1 at (0,1):
  (0,1) -> sinks, adds 1
  (0,2) -> sinks, adds 1
  (1,1) -> sinks, adds 1
  Total area = 3. max_area = 3.

Island 2 at (2,3):
  (2,3) -> sinks, adds 1
  Total area = 1.

max_area = max(3, 1) = 3! ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def maxAreaOfIsland(grid):
    m, n = len(grid), len(grid[0])
    max_area = 0
    
    def dfs(r, c):
        if r < 0 or r >= m or c < 0 or c >= n or grid[r][c] == 0:
            return 0
            
        grid[r][c] = 0  # sink to avoid revisits
        
        return (1 + dfs(r + 1, c) + 
                    dfs(r - 1, c) + 
                    dfs(r, c + 1) + 
                    dfs(r, c - 1))
                    
    for r in range(m):
        for c in range(n):
            if grid[r][c] == 1:
                max_area = max(max_area, dfs(r, c))
                
    return max_area</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(m * n)</strong> — Each cell is visited at most once by DFS. <strong>Space O(m * n)</strong> for recursion call stack in worst case.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Grid with no land (all 0s): returns 0.</li>
<li>Grid completely filled with land: returns <code>m * n</code>.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Number of Islands ([[200]]).</li>
<li>Count Sub Islands ([[1905]]).</li>
</ul>''',

# ============================================================ LC 733
733: '''<h2>🧭 How to think about it</h2>
<p>An image is represented by an <code>m x n</code> integer grid <code>image</code> where <code>image[i][j]</code> represents the pixel value. You are given <code>sr, sc</code> and <code>color</code>. Perform a flood fill on the image starting from pixel <code>image[sr][sc]</code>: change the color of the starting pixel and all 4-directionally connected pixels with the same initial color to <code>color</code>.</p>

<h2>🐢 Brute force first</h2>
<p>Standard BFS/DFS traversal. The critical trap is an <strong>infinite loop</strong> when the target <code>color</code> is already equal to the starting cell's color (<code>image[sr][sc] == color</code>)!</p>

<div class="insight">💡 <strong>Key insight:</strong> If <code>image[sr][sc] == color</code>, return <code>image</code> immediately without any traversal! Otherwise, record <code>original_color = image[sr][sc]</code> and run DFS from <code>(sr, sc)</code>, replacing any neighboring cell with <code>original_color</code> with <code>color</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Let <code>orig = image[sr][sc]</code>.</li>
<li>If <code>orig == color</code>, return <code>image</code> immediately (prevents infinite recursion).</li>
<li>Define <code>dfs(r, c)</code>:
  <ul>
    <li>If <code>r, c</code> out of bounds or <code>image[r][c] != orig</code>, return.</li>
    <li>Change color: <code>image[r][c] = color</code>.</li>
    <li>Recurse 4 directions: <code>(r+1, c), (r-1, c), (r, c+1), (r, c-1)</code>.</li>
  </ul>
</li>
<li>Call <code>dfs(sr, sc)</code> and return <code>image</code>.</li>
</ol>

<h2>🎞️ Visual dry run — image = [[1,1,1],[1,1,0],[1,0,1]], sr=1, sc=1, color=2</h2>
<pre class="viz">orig = image[1][1] = 1. color = 2.
DFS starts at (1,1):
  (1,1) -> 2
  (0,1) -> 2, (0,0) -> 2, (0,2) -> 2
  (1,0) -> 2, (2,0) -> 2
  (2,2) remains 1 because it's separated by 0!
Result:
[[2, 2, 2],
 [2, 2, 0],
 [2, 0, 1]] ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def floodFill(image, sr, sc, color):
    orig = image[sr][sc]
    if orig == color:
        return image
        
    m, n = len(image), len(image[0])
    
    def dfs(r, c):
        if r < 0 or r >= m or c < 0 or c >= n or image[r][c] != orig:
            return
            
        image[r][c] = color
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)
        
    dfs(sr, sc)
    return image</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(m * n)</strong>. <strong>Space O(m * n)</strong> call stack.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li><code>orig == color</code>: handled immediately by upfront check.</li>
<li>1x1 image.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Number of Islands ([[200]]).</li>
<li>Coloring A Border ([[1034]]).</li>
</ul>''',

# ============================================================ LC 130
130: '''<h2>🧭 How to think about it</h2>
<p>Given an <code>m x n</code> matrix <code>board</code> containing <code>'X'</code> and <code>'O'</code>, capture all regions that are 4-directionally surrounded by <code>'X'</code>. A region is captured by flipping all <code>'O'</code>s into <code>'X'</code>s in that surrounded region.</p>

<h2>🐢 Brute force first</h2>
<p>Checking each 'O' to see if it can reach the boundary takes O((m*n)^2). Invert the perspective: which 'O's CANNOT be captured?</p>

<div class="insight">💡 <strong>Key insight:</strong> Any <code>'O'</code> on the <strong>border</strong> (or connected to a border <code>'O'</code>) can NEVER be surrounded! Therefore, reverse the logic:
1. Start DFS from all <code>'O'</code>s located on the 4 borders of the matrix. Mark them and all connected <code>'O'</code>s with a temporary marker (e.g. <code>'E'</code> for Escaped).
2. Now, all remaining <code>'O'</code>s are completely surrounded! Flip them to <code>'X'</code>.
3. Finally, restore the escaped <code>'E'</code> cells back to <code>'O'</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Identify all boundary cells: first row, last row, first col, last col.</li>
<li>For each boundary cell where <code>board[r][c] == 'O'</code>, run DFS to mark all connected <code>'O'</code>s as <code>'E'</code>.</li>
<li>Iterate through the entire board:
  <ul>
    <li>If <code>board[r][c] == 'O'</code>: flip to <code>'X'</code> (it was truly surrounded).</li>
    <li>If <code>board[r][c] == 'E'</code>: restore to <code>'O'</code> (it was connected to border).</li>
  </ul>
</li>
</ol>

<h2>🎞️ Visual dry run — board:</h2>
<pre class="viz">X X X X       Phase 1 (Border DFS):     Phase 2 (Flip & Restore):
X O O X  -->  (1,1) & (1,2) are not --> X X X X
X X O X       connected to border.      X X X X
X O X X       (3,1) is on border -> E   X X X X
                                        X O X X ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def solve(board):
    """
    Do not return anything, modify board in-place instead.
    """
    if not board or not board[0]:
        return
        
    m, n = len(board), len(board[0])
    
    def dfs(r, c):
        if r < 0 or r >= m or c < 0 or c >= n or board[r][c] != 'O':
            return
        board[r][c] = 'E'  # Mark as escaped / border-connected
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)
        
    # Step 1: Run DFS from all border 'O's
    for r in range(m):
        for c in (0, n - 1):
            if board[r][c] == 'O':
                dfs(r, c)
    for c in range(n):
        for r in (0, m - 1):
            if board[r][c] == 'O':
                dfs(r, c)
                
    # Step 2: Flip captured 'O' -> 'X', and restore 'E' -> 'O'
    for r in range(m):
        for c in range(n):
            if board[r][c] == 'O':
                board[r][c] = 'X'
            elif board[r][c] == 'E':
                board[r][c] = 'O'</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(m * n)</strong>. <strong>Space O(m * n)</strong> recursion stack.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Grid of size &lt;= 2: no inner cell can be surrounded; all cells are on the border.</li>
<li>Board containing only 'X' or only 'O'.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Pacific Atlantic Water Flow ([[417]]).</li>
<li>Number of Enclaves ([[1020]]).</li>
</ul>''',

# ============================================================ LC 417
417: '''<h2>🧭 How to think about it</h2>
<p>There is an <code>m x n</code> rectangular island bordered by the Pacific Ocean (top and left edges) and the Atlantic Ocean (bottom and right edges). Water flows from cell to neighbor if the neighbor's height is <strong>less than or equal</strong> to the current cell's height. Find all grid coordinates where rain water can flow to <strong>both</strong> the Pacific and Atlantic oceans.</p>

<h2>🐢 Brute force first</h2>
<p>Run DFS from every cell to see if it can reach both oceans: O((m*n)^2). Flowing downhill from every cell causes massive duplicate work.</p>

<div class="insight">💡 <strong>Key insight:</strong> Reverse the flow! Instead of simulating water flowing downhill from every internal cell to the oceans, simulate water flowing <strong>uphill</strong> from the oceans into the island!
1. Start BFS/DFS from all Pacific boundary cells moving to neighbors with <code>height >= current_height</code>. Mark reachable in <code>pacific</code> set.
2. Start BFS/DFS from all Atlantic boundary cells moving uphill. Mark in <code>atlantic</code> set.
3. The intersection <code>pacific & atlantic</code> is the exact set of coordinates that can reach both oceans!</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Create two boolean sets: <code>pacific = set()</code> and <code>atlantic = set()</code>.</li>
<li>Helper <code>dfs(r, c, visited)</code>:
  <ul>
    <li>Add <code>(r, c)</code> to <code>visited</code>.</li>
    <li>For 4 neighbors <code>(nr, nc)</code>: if in bounds, not in <code>visited</code>, and <code>heights[nr][nc] >= heights[r][c]</code> (uphill!), recurse <code>dfs(nr, nc, visited)</code>.</li>
  </ul>
</li>
<li>Run DFS for all Pacific border cells: top row <code>r=0</code> and left col <code>c=0</code>.</li>
<li>Run DFS for all Atlantic border cells: bottom row <code>r=m-1</code> and right col <code>c=n-1</code>.</li>
<li>Return <code>list(pacific & atlantic)</code>.</li>
</ol>

<h2>🎞️ Visual dry run:</h2>
<pre class="viz">Pacific is top/left. Atlantic is bottom/right.
Heights:
[1, 2, 2, 3, 5]
[3, 2, 3, 4, 4]
[2, 4, 5, 3, 1]
[6, 7, 1, 4, 5]
[5, 1, 1, 2, 4]

Cells reached by Pacific (flowing uphill from top & left).
Cells reached by Atlantic (flowing uphill from bottom & right).
Intersection: [[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]] ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def pacificAtlantic(heights):
    if not heights or not heights[0]:
        return []
        
    m, n = len(heights), len(heights[0])
    pacific = set()
    atlantic = set()
    
    def dfs(r, c, visited):
        visited.add((r, c))
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and (nr, nc) not in visited:
                # Water flows uphill: neighbor must be >= current cell
                if heights[nr][nc] >= heights[r][c]:
                    dfs(nr, nc, visited)
                    
    # Pacific border: row 0 and col 0
    for r in range(m):
        dfs(r, 0, pacific)
    for c in range(n):
        dfs(0, c, pacific)
        
    # Atlantic border: row m-1 and col n-1
    for r in range(m):
        dfs(r, n - 1, atlantic)
    for c in range(n):
        dfs(m - 1, c, atlantic)
        
    return [list(coord) for coord in (pacific & atlantic)]</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(m * n)</strong> — Each cell is visited at most twice per ocean. <strong>Space O(m * n)</strong> for the two visited sets.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>1x1 grid: cell touches both Pacific and Atlantic, returns <code>[[0, 0]]</code>.</li>
<li>All cells equal height: every cell can reach both oceans.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Surrounded Regions ([[130]]).</li>
<li>Swim in Rising Water ([[778]]).</li>
</ul>''',

# ============================================================ LC 547
547: '''<h2>🧭 How to think about it</h2>
<p>There are <code>n</code> cities. Some are connected, some are not. If city <code>a</code> is connected to <code>b</code>, and <code>b</code> is connected to <code>c</code>, then <code>a</code> is connected indirectly to <code>c</code>. A province is a group of directly or indirectly connected cities. Given an <code>n x n</code> adjacency matrix <code>isConnected</code> where <code>isConnected[i][j] = 1</code> if connected, return the total number of provinces.</p>

<h2>🐢 Brute force first</h2>
<p>Standard connected component counting on an undirected graph with <code>n</code> nodes. Can be solved with DFS, BFS, or Union-Find.</p>

<div class="insight">💡 <strong>Key insight:</strong> Maintain a <code>visited</code> set. Loop through each city <code>i</code> from <code>0</code> to <code>n-1</code>: if <code>i</code> is not visited, we found a new province! Increment count, and run DFS from <code>i</code> to visit all cities connected to <code>i</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Let <code>n = len(isConnected)</code>, <code>visited = set()</code>, <code>provinces = 0</code>.</li>
<li>For city <code>i</code> in <code>0 .. n-1</code>:</li>
<li>If <code>i not in visited</code>:
  <ul>
    <li><code>provinces += 1</code>.</li>
    <li>Run <code>dfs(i)</code>: mark <code>i</code> visited; for each neighbor <code>j</code>, if <code>isConnected[i][j] == 1</code> and <code>j not in visited</code>, recurse <code>dfs(j)</code>.</li>
  </ul>
</li>
<li>Return <code>provinces</code>.</li>
</ol>

<h2>🎞️ Visual dry run — isConnected = [[1,1,0],[1,1,0],[0,0,1]]</h2>
<pre class="viz">City 0: unvisited -> provinces = 1.
  DFS(0): visits 0, sees connection to 1 -> visits 1.
City 1: already visited.
City 2: unvisited -> provinces = 2.
  DFS(2): visits 2.
Total provinces = 2! ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def findCircleNum(isConnected):
    n = len(isConnected)
    visited = set()
    provinces = 0
    
    def dfs(city):
        visited.add(city)
        for neighbor in range(n):
            if isConnected[city][neighbor] == 1 and neighbor not in visited:
                dfs(neighbor)
                
    for i in range(n):
        if i not in visited:
            provinces += 1
            dfs(i)
            
    return provinces</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n^2)</strong> — Traverses the <code>n x n</code> adjacency matrix. <strong>Space O(n)</strong> for <code>visited</code> set and recursion stack.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>All cities disconnected (identity matrix): <code>n</code> provinces.</li>
<li>All cities connected: 1 province.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Number of Connected Components in an Undirected Graph ([[323]]).</li>
<li>Redundant Connection ([[684]]) via Union-Find.</li>
</ul>''',

# ============================================================ LC 841
841: '''<h2>🧭 How to think about it</h2>
<p>There are <code>n</code> rooms labeled <code>0</code> to <code>n - 1</code>, and all the rooms are locked except for room <code>0</code>. Each room has a list of keys <code>rooms[i]</code> to other rooms. Return <code>true</code> if you can visit <strong>all</strong> the rooms, or <code>false</code> otherwise.</p>

<h2>🐢 Brute force first</h2>
<p>This is standard graph reachability starting from source node 0. Traverse all reachable nodes via BFS/DFS; check if <code>len(visited) == n</code>.</p>

<div class="insight">💡 <strong>Key insight:</strong> Standard BFS/DFS traversal with a <code>visited</code> set starting at <code>0</code>. When traversal completes, if <code>len(visited) == len(rooms)</code>, all rooms were unlocked!</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><code>visited = {0}</code>, stack = <code>[0]</code>.</li>
<li>While stack is not empty:
  <ul>
    <li>Pop <code>room = stack.pop()</code>.</li>
    <li>For key in <code>rooms[room]</code>: if <code>key not in visited</code>: add to <code>visited</code>, push to stack.</li>
  </ul>
</li>
<li>Return <code>len(visited) == len(rooms)</code>.</li>
</ol>

<h2>🎞️ Visual dry run — rooms = [[1],[2],[3],[]]</h2>
<pre class="viz">Start at 0: visited = {0}, keys: [1]
Visit 1: visited = {0, 1}, keys: [2]
Visit 2: visited = {0, 1, 2}, keys: [3]
Visit 3: visited = {0, 1, 2, 3}, keys: []
len(visited) == 4 == len(rooms) -> True! ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def canVisitAllRooms(rooms):
    visited = {0}
    stack = [0]
    
    while stack:
        room = stack.pop()
        for key in rooms[room]:
            if key not in visited:
                visited.add(key)
                stack.append(key)
                
    return len(visited) == len(rooms)</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(V + E)</strong> where <code>V = len(rooms)</code> and <code>E = total keys</code>. <strong>Space O(V)</strong> for visited set.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Cycles in keys (e.g. room 0 has key 1, room 1 has key 0): handled cleanly by <code>visited</code> set.</li>
<li>Isolated room with no incoming keys: returns False.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Course Schedule ([[207]]).</li>
</ul>''',

# ============================================================ LC 1020
1020: '''<h2>🧭 How to think about it</h2>
<p>You are given an <code>m x n</code> binary matrix <code>grid</code>, where <code>0</code> represents a sea cell and <code>1</code> represents a land cell. A move consists of walking from one land cell to another adjacent land cell or walking off the boundary of the grid. Return the number of land cells in <code>grid</code> for which we <strong>cannot walk off the boundary</strong> of the grid in any number of moves.</p>

<h2>🐢 Brute force first</h2>
<p>Count how many 1s are strictly trapped inside surrounded components. Similar to LC 130 Surrounded Regions!</p>

<div class="insight">💡 <strong>Key insight:</strong> Reverse thinking! Run DFS/BFS starting from all land cells on the <strong>boundary</strong> of the grid and sink them to <code>0</code> (or mark them as reached). Once all boundary-connected land is eliminated, count the remaining <code>1</code>s in the grid! Those remaining <code>1</code>s are the enclaves.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>For all cells on the 4 borders: if <code>grid[r][c] == 1</code>, run <code>dfs(r, c)</code> to sink all reachable land to <code>0</code>.</li>
<li>Count remaining <code>1</code>s: <code>sum(row.count(1) for row in grid)</code>.</li>
<li>Return the count.</li>
</ol>

<h2>🎞️ Visual dry run — grid:</h2>
<pre class="viz">0 0 0 0
1 0 1 0
0 1 1 0
0 0 0 0

Border land at (1,0) is sunk to 0.
Inner land cells at (1,2), (2,1), (2,2) cannot reach border.
Count remaining 1s = 3! ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def numEnclaves(grid):
    m, n = len(grid), len(grid[0])
    
    def dfs(r, c):
        if r < 0 or r >= m or c < 0 or c >= n or grid[r][c] == 0:
            return
        grid[r][c] = 0  # Sink boundary-connected land
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)
        
    # Sink all boundary land
    for r in range(m):
        if grid[r][0] == 1: dfs(r, 0)
        if grid[r][n - 1] == 1: dfs(r, n - 1)
    for c in range(n):
        if grid[0][c] == 1: dfs(0, c)
        if grid[m - 1][c] == 1: dfs(m - 1, c)
        
    # Count remaining trapped enclaves
    return sum(row.count(1) for row in grid)</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(m * n)</strong>. <strong>Space O(m * n)</strong> recursion stack.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>All land touches the boundary: returns 0.</li>
<li>No land: returns 0.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Surrounded Regions ([[130]]).</li>
<li>Number of Closed Islands ([[1254]]).</li>
</ul>''',

# ============================================================ LC 1254
1254: '''<h2>🧭 How to think about it</h2>
<p>Given a 2D grid consists of <code>0</code>s (land) and <code>1</code>s (water). An island is a maximal 4-directionally connected group of <code>0</code>s and a <strong>closed island</strong> is totally surrounded by <code>1</code>s (i.e. does not touch the boundary of the grid). Return the number of closed islands.</p>

<h2>🐢 Brute force first</h2>
<p>Notice the inverted notation: <code>0</code> is land, <code>1</code> is water! Any land component that touches the boundary is not closed.</p>

<div class="insight">💡 <strong>Key insight:</strong> First, eliminate all land (<code>0</code>s) connected to the grid boundary by running DFS from the 4 borders and turning them into water (<code>1</code>s). Then, standard island counting: any remaining <code>0</code> is guaranteed to be a closed island!</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Iterate borders: if <code>grid[r][c] == 0</code>, run <code>dfs(r, c)</code> to turn into <code>1</code>.</li>
<li>Now scan interior: if <code>grid[r][c] == 0</code>, <code>closed_islands += 1</code>, run <code>dfs(r, c)</code> to sink the island.</li>
<li>Return <code>closed_islands</code>.</li>
</ol>

<h2>🎞️ Visual dry run:</h2>
<pre class="viz">1 1 1 1
1 0 0 1  <-- Land 0s completely surrounded by 1s!
1 0 0 1
1 1 1 1
Closed island count = 1! ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def closedIsland(grid):
    m, n = len(grid), len(grid[0])
    
    def dfs(r, c):
        if r < 0 or r >= m or c < 0 or c >= n or grid[r][c] == 1:
            return
        grid[r][c] = 1  # Turn land into water
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)
        
    # Step 1: Sink boundary-connected land
    for r in range(m):
        for c in (0, n - 1):
            if grid[r][c] == 0: dfs(r, c)
    for c in range(n):
        for r in (0, m - 1):
            if grid[r][c] == 0: dfs(r, c)
            
    # Step 2: Count closed islands
    closed = 0
    for r in range(1, m - 1):
        for c in range(1, n - 1):
            if grid[r][c] == 0:
                closed += 1
                dfs(r, c)
                
    return closed</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(m * n)</strong>. <strong>Space O(m * n)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Grid of size &lt;= 2: no closed islands possible, returns 0.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Number of Islands ([[200]]).</li>
<li>Number of Enclaves ([[1020]]).</li>
</ul>''',

# ============================================================ LC 994
994: '''<h2>🧭 How to think about it</h2>
<p>You are given an <code>m x n</code> grid where <code>0</code> represents an empty cell, <code>1</code> represents a fresh orange, and <code>2</code> represents a rotten orange. Every minute, any fresh orange that is 4-directionally adjacent to a rotten orange becomes rotten. Return the minimum number of minutes that must elapse until no cell has a fresh orange. If this is impossible, return <code>-1</code>.</p>

<h2>🐢 Brute force first</h2>
<p>Simulate minute-by-minute with full grid scans: O((m*n)^2). Multi-source BFS simulates simultaneous propagation in a single pass.</p>

<div class="insight">💡 <strong>Key insight:</strong> All rotten oranges rot their neighbors <strong>simultaneously</strong>! This is the signature textbook problem for <strong>Multi-Source BFS</strong>.
1. Add all initially rotten oranges <code>(r, c)</code> into a FIFO queue at time 0.
2. Count initial <code>fresh</code> oranges.
3. Pop level-by-level (by minutes): for each rotten orange, infect adjacent fresh oranges, decrement <code>fresh</code>, and append newly infected oranges to queue.
4. When queue is empty, if <code>fresh == 0</code> return minutes; else return <code>-1</code> (some fresh oranges were unreachable).</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Initialize <code>queue = deque()</code> and <code>fresh = 0</code>.</li>
<li>Scan grid: if cell == 2, <code>queue.append((r, c))</code>; if cell == 1, <code>fresh += 1</code>.</li>
<li>If <code>fresh == 0</code>, return 0 immediately.</li>
<li><code>minutes = 0</code>. While queue and fresh > 0:
  <ul>
    <li>For _ in range(len(queue)):</li>
    <li>Pop <code>(r, c)</code>. For 4 neighbors: if in bounds and cell == 1: turn to 2, <code>fresh -= 1</code>, <code>queue.append((nr, nc))</code>.</li>
    <li><code>minutes += 1</code>.</li>
  </ul>
</li>
<li>Return <code>minutes</code> if <code>fresh == 0</code> else <code>-1</code>.</li>
</ol>

<h2>🎞️ Visual dry run — grid = [[2,1,1],[1,1,0],[0,1,1]]</h2>
<pre class="viz">Initial: Queue = [(0,0)], fresh = 6.
Minute 1: (0,0) rots (0,1) and (1,0). fresh = 4. Queue = [(0,1), (1,0)]
Minute 2: (0,1) rots (0,2); (1,0) rots (1,1). fresh = 2. Queue = [(0,2), (1,1)]
Minute 3: (1,1) rots (2,1). fresh = 1. Queue = [(2,1)]
Minute 4: (2,1) rots (2,2). fresh = 0.
fresh == 0! Return 4 minutes. ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>from collections import deque

def orangesRotting(grid):
    m, n = len(grid), len(grid[0])
    queue = deque()
    fresh = 0
    
    # 1. Enqueue all rotten oranges & count fresh ones
    for r in range(m):
        for c in range(n):
            if grid[r][c] == 2:
                queue.append((r, c))
            elif grid[r][c] == 1:
                fresh += 1
                
    if fresh == 0:
        return 0
        
    minutes = 0
    # 2. Multi-source BFS level-by-level
    while queue and fresh > 0:
        minutes += 1
        for _ in range(len(queue)):
            r, c = queue.popleft()
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    queue.append((nr, nc))
                    
    return minutes if fresh == 0 else -1</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(m * n)</strong> — Each cell is processed at most once. <strong>Space O(m * n)</strong> for the BFS queue.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>No fresh oranges at start: returns 0.</li>
<li>Fresh orange isolated by empty cells: cannot be reached, returns -1.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>01 Matrix ([[542]]).</li>
<li>Shortest Path in Binary Matrix ([[1091]]).</li>
<li>Walls and Gates ([[286]]).</li>
</ul>''',

# ============================================================ LC 542
542: '''<h2>🧭 How to think about it</h2>
<p>Given an <code>m x n</code> binary matrix <code>mat</code>, return the distance of the nearest <code>0</code> for each cell. The distance between two adjacent cells is <code>1</code>.</p>

<h2>🐢 Brute force first</h2>
<p>For every <code>1</code>, run BFS to find the closest <code>0</code>: O((m*n)^2). Reverse the thinking: run multi-source BFS starting from all <code>0</code>s simultaneously!</p>

<div class="insight">💡 <strong>Key insight:</strong> <strong>Multi-Source BFS from all 0s!</strong>
1. Initialize distance matrix <code>dist</code> with <code>-1</code>.
2. Enqueue all cells containing <code>0</code> with distance <code>0</code>.
3. As BFS expands outwards, the first time you reach a cell <code>(nr, nc)</code>, the distance <code>dist[r][c] + 1</code> is guaranteed to be its shortest distance to ANY <code>0</code>!</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Initialize <code>dist = [[-1]*n for _ in range(m)]</code> and <code>queue = deque()</code>.</li>
<li>Add all <code>(r, c)</code> where <code>mat[r][c] == 0</code> to queue, setting <code>dist[r][c] = 0</code>.</li>
<li>While queue:
  <ul>
    <li><code>r, c = queue.popleft()</code>.</li>
    <li>For 4 neighbors: if in bounds and <code>dist[nr][nc] == -1</code>: <code>dist[nr][nc] = dist[r][c] + 1</code>, <code>queue.append((nr, nc))</code>.</li>
  </ul>
</li>
<li>Return <code>dist</code>.</li>
</ol>

<h2>🎞️ Visual dry run — mat = [[0,0,0],[0,1,0],[1,1,1]]</h2>
<pre class="viz">Queue starts with all 0 cells (dist 0):
Dist after queue init:
[ 0,  0,  0]
[ 0, -1,  0]
[-1, -1, -1]

BFS expansion:
dist[1][1] = 1 (reached from (0,1))
dist[2][0] = 1 (reached from (1,0))
dist[2][2] = 1 (reached from (1,2))
dist[2][1] = 2 (reached from (1,1) or (2,0))
Result:
[[0, 0, 0],
 [0, 1, 0],
 [1, 2, 1]] ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>from collections import deque

def updateMatrix(mat):
    m, n = len(mat), len(mat[0])
    dist = [[-1] * n for _ in range(m)]
    queue = deque()
    
    # Enqueue all 0s as multi-source origins
    for r in range(m):
        for c in range(n):
            if mat[r][c] == 0:
                dist[r][c] = 0
                queue.append((r, c))
                
    while queue:
        r, c = queue.popleft()
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and dist[nr][nc] == -1:
                dist[nr][nc] = dist[r][c] + 1
                queue.append((nr, nc))
                
    return dist</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(m * n)</strong> — Each cell is queued and dequeued exactly once. <strong>Space O(m * n)</strong> for distance matrix and queue.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>All 0s: returns all 0s.</li>
<li>Single 0 in corner.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Rotting Oranges ([[994]]).</li>
<li>As Far from Land as Possible ([[1162]]).</li>
</ul>''',

# ============================================================ LC 1091
1091: '''<h2>🧭 How to think about it</h2>
<p>Given an <code>n x n</code> binary matrix <code>grid</code>, return the length of the shortest clear path in the matrix. A clear path connects the top-left cell <code>(0, 0)</code> and the bottom-right cell <code>(n - 1, n - 1)</code> such that all visited cells are <code>0</code>, and all adjacent cells of the path are <strong>8-directionally connected</strong>. If no such path exists, return <code>-1</code>.</p>

<h2>🐢 Brute force first</h2>
<p>DFS can explore exponential paths. In an unweighted graph, BFS is mathematically guaranteed to find the shortest path!</p>

<div class="insight">💡 <strong>Key insight:</strong> Standard BFS using <strong>8 directional vectors</strong>. Mark visited by mutating <code>grid[r][c] = 1</code> in-place as soon as a cell is enqueued to prevent duplicate additions. Return path length as soon as destination <code>(n-1, n-1)</code> is reached!</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>If <code>grid[0][0] != 0 or grid[n-1][n-1] != 0</code>, return <code>-1</code>.</li>
<li><code>queue = deque([(0, 0, 1)])</code> (row, col, distance). Mark <code>grid[0][0] = 1</code>.</li>
<li>While queue:
  <ul>
    <li><code>r, c, d = queue.popleft()</code>.</li>
    <li>If <code>r == n - 1 and c == n - 1</code>, return <code>d</code>.</li>
    <li>For all 8 directional deltas <code>(dr, dc)</code>:</li>
    <li>If neighbor in bounds and <code>grid[nr][nc] == 0</code>: mark <code>grid[nr][nc] = 1</code>, <code>queue.append((nr, nc, d + 1))</code>.</li>
  </ul>
</li>
<li>Return <code>-1</code>.</li>
</ol>

<h2>🎞️ Visual dry run — grid = [[0,1],[1,0]]</h2>
<pre class="viz">Start at (0,0) dist 1.
8 directions includes diagonal (1,1)!
From (0,0), neighbor (1,1) is valid and clear (0).
(1,1) == (n-1, n-1) destination!
Returns distance = 2! ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>from collections import deque

def shortestPathBinaryMatrix(grid):
    n = len(grid)
    if grid[0][0] != 0 or grid[n - 1][n - 1] != 0:
        return -1
        
    queue = deque([(0, 0, 1)])  # (r, c, path_len)
    grid[0][0] = 1  # mark visited
    
    # 8 directional movements
    directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    
    while queue:
        r, c, d = queue.popleft()
        if r == n - 1 and c == n - 1:
            return d
            
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0:
                grid[nr][nc] = 1
                queue.append((nr, nc, d + 1))
                
    return -1</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(n^2)</strong> — Each cell visited at most once. <strong>Space O(n^2)</strong> for queue.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Start <code>(0,0)</code> or end <code>(n-1, n-1)</code> blocked (equals 1): returns -1.</li>
<li>1x1 grid with <code>0</code>: returns 1.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Word Ladder ([[127]]).</li>
<li>Cheapest Flights Within K Stops ([[787]]).</li>
</ul>''',

# ============================================================ LC 127
127: '''<h2>🧭 How to think about it</h2>
<p>A transformation sequence from <code>beginWord</code> to <code>endWord</code> using a dictionary <code>wordList</code> is a sequence of words where every adjacent pair of words differs by exactly one letter, and every word in the sequence exists in <code>wordList</code>. Given <code>beginWord</code>, <code>endWord</code>, and <code>wordList</code>, return the <strong>number of words in the shortest transformation sequence</strong> from <code>beginWord</code> to <code>endWord</code>, or <code>0</code> if no such sequence exists.</p>

<h2>🐢 Brute force first</h2>
<p>Testing all pairs of words for 1-letter difference takes O(N^2 * L) to build an adjacency graph. When N = 5,000, N^2 = 25,000,000 operations.</p>

<div class="insight">💡 <strong>Key insight:</strong> Treat each word as a graph node. An edge exists between words that differ by 1 letter. To find the shortest path, use BFS!
Instead of comparing word-to-word (O(N)), generate all <code>26 * L</code> possible single-character mutations of the current word and check set membership in O(1)! Even faster: <strong>Bidirectional BFS</strong>, expanding from both <code>beginWord</code> and <code>endWord</code> simultaneously, reducing the search space from $b^d$ to $2 	imes b^{d/2}$!</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Convert <code>wordList</code> into a hash set for O(1) lookups. If <code>endWord not in wordList</code>, return 0.</li>
<li>Initialize two sets: <code>begin_set = {beginWord}</code>, <code>end_set = {endWord}</code>.</li>
<li><code>step = 1</code>.</li>
<li>While <code>begin_set</code> and <code>end_set</code> are non-empty:
  <ul>
    <li>Always expand the <strong>smaller set</strong> to minimize branching factor: if <code>len(begin_set) > len(end_set)</code>, swap them.</li>
    <li><code>next_set = set()</code>.</li>
    <li>For each word in <code>begin_set</code>:</li>
    <li>Try all 26 character substitutions at each of the <code>L</code> positions.</li>
    <li>If mutated word is in <code>end_set</code>: return <code>step + 1</code> (search frontiers met!).</li>
    <li>If mutated word in <code>word_set</code>: add to <code>next_set</code>, remove from <code>word_set</code> to prevent cycles.</li>
    <li><code>begin_set = next_set; step += 1</code>.</li>
  </ul>
</li>
<li>Return 0.</li>
</ol>

<h2>🎞️ Visual dry run — beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log","cog"]</h2>
<pre class="viz">Step 1: begin_set = {"hit"}, end_set = {"cog"}
  Expand "hit" -> "hot" (valid).
  next_set = {"hot"}. step = 2.

Step 2: begin_set = {"hot"} (len 1), end_set = {"cog"} (len 1).
  Expand "hot" -> "dot", "lot".
  next_set = {"dot", "lot"}. step = 3.

Step 3: Swap so begin_set = {"cog"} (len 1), end_set = {"dot", "lot"} (len 2).
  Expand "cog" -> "dog", "log".
  next_set = {"dog", "log"}. step = 4.

Step 4: Expand "dog" -> matches "dot" in end_set!
Frontiers meet! Return step + 1 = 4 + 1 = 5 words!
("hit" -> "hot" -> "dot" -> "dog" -> "cog") ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def ladderLength(beginWord, endWord, wordList):
    word_set = set(wordList)
    if endWord not in word_set:
        return 0
        
    begin_set = {beginWord}
    end_set = {endWord}
    step = 1
    L = len(beginWord)
    
    while begin_set and end_set:
        # Always expand the smaller frontier
        if len(begin_set) > len(end_set):
            begin_set, end_set = end_set, begin_set
            
        next_set = set()
        for word in begin_set:
            word_chars = list(word)
            for i in range(L):
                orig_char = word_chars[i]
                for c in 'abcdefghijklmnopqrstuvwxyz':
                    if c == orig_char:
                        continue
                    word_chars[i] = c
                    mutated = ''.join(word_chars)
                    
                    if mutated in end_set:
                        return step + 1
                    if mutated in word_set:
                        next_set.add(mutated)
                        word_set.remove(mutated)  # Mark visited
                word_chars[i] = orig_char
                
        begin_set = next_set
        step += 1
        
    return 0</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(M * N * 26)</strong> = O(M * N) where <code>M</code> is length of words and <code>N</code> is total words in dictionary. <strong>Space O(N)</strong> for word sets.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li><code>endWord</code> not in wordList: returns 0 immediately.</li>
<li>No valid transformation path exists.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Word Ladder II ([[126]]) — return all shortest transformation sequences.</li>
<li>Minimum Genetic Mutation ([[433]]).</li>
<li>Open the Lock ([[752]]).</li>
</ul>''',

# ============================================================ LC 207
207: '''<h2>🧭 How to think about it</h2>
<p>There are a total of <code>numCourses</code> courses you have to take, labeled from <code>0</code> to <code>numCourses - 1</code>. You are given an array <code>prerequisites</code> where <code>prerequisites[i] = [a_i, b_i]</code> indicates that you must take course <code>b_i</code> first if you want to take course <code>a_i</code>. Return <code>true</code> if you can finish all courses, or <code>false</code> otherwise.</p>

<h2>🐢 Brute force first</h2>
<p>Attempting all permutations of course orders is factorial O(n!).</p>

<div class="insight">💡 <strong>Key insight:</strong> Can you complete all courses? Only if there is <strong>NO CYCLE in the directed prerequisite graph</strong>! A directed graph without cycles is a DAG (Directed Acyclic Graph). We can detect cycles using either:
1. <strong>Kahn's Algorithm (BFS with In-degrees)</strong>: Count in-degrees (prerequisites needed). Courses with 0 in-degrees can be taken immediately. Decrement in-degrees of their dependent courses. If total taken courses == <code>numCourses</code>, no cycle exists!
2. <strong>DFS 3-State Coloring</strong>: 0 = unvisited, 1 = visiting (in current recursion stack), 2 = visited. If a neighbor is in state 1, a back-edge (cycle) exists!</div>

<h2>🪜 The approach, step by step (Kahn's Algorithm)</h2>
<ol>
<li>Build adjacency list <code>graph = {i: []}</code> and compute <code>in_degree = [0] * numCourses</code>.</li>
<li>For <code>dest, src in prerequisites</code>: <code>graph[src].append(dest)</code>, <code>in_degree[dest] += 1</code>.</li>
<li>Add all courses with <code>in_degree[i] == 0</code> to a queue (courses with no prerequisites).</li>
<li><code>taken = 0</code>.</li>
<li>While queue:
  <ul>
    <li><code>course = queue.popleft()</code>; <code>taken += 1</code>.</li>
    <li>For neighbor in <code>graph[course]</code>:
      <ul>
        <li><code>in_degree[neighbor] -= 1</code>.</li>
        <li>If <code>in_degree[neighbor] == 0</code>: <code>queue.append(neighbor)</code>.</li>
      </ul>
    </li>
  </ul>
</li>
<li>Return <code>taken == numCourses</code>.</li>
</ol>

<h2>🎞️ Visual dry run — prerequisites = [[1, 0], [0, 1]] (Cycle!)</h2>
<pre class="viz">Edge 0 -> 1 (to take 1, need 0)
Edge 1 -> 0 (to take 0, need 1)
in_degrees: 0: 1, 1: 1
Queue: empty! No course has in_degree == 0.
Loop terminates immediately.
taken = 0 != 2.
Return False (Deadlock/Cycle detected!). ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>from collections import deque, defaultdict

def canFinish(numCourses, prerequisites):
    """
    Kahn's Algorithm for Topological Sort / Cycle Detection.
    """
    graph = defaultdict(list)
    in_degree = [0] * numCourses
    
    for dest, src in prerequisites:
        graph[src].append(dest)
        in_degree[dest] += 1
        
    queue = deque([i for i in range(numCourses) if in_degree[i] == 0])
    taken = 0
    
    while queue:
        course = queue.popleft()
        taken += 1
        
        for neighbor in graph[course]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
                
    return taken == numCourses</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(V + E)</strong> where <code>V = numCourses</code> and <code>E = len(prerequisites)</code>. <strong>Space O(V + E)</strong> for graph and queue.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>No prerequisites: all courses have in-degree 0, returns True.</li>
<li>Self-dependency <code>[0, 0]</code>: in-degree never reaches 0, returns False.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Course Schedule II ([[210]]) — return the topological ordering.</li>
<li>Alien Dictionary ([[269]]).</li>
<li>Parallel Courses ([[1136]]).</li>
</ul>''',

# ============================================================ LC 210
210: '''<h2>🧭 How to think about it</h2>
<p>Given <code>numCourses</code> and array <code>prerequisites</code>, return the <strong>ordering of courses</strong> you should take to finish all courses. If there are many valid answers, return any of them. If it is impossible to finish all courses, return an <strong>empty array</strong>.</p>

<h2>🐢 Brute force first</h2>
<p>Kahn's algorithm produces the exact valid topological ordering as courses are dequeued!</p>

<div class="insight">💡 <strong>Key insight:</strong> Extend Kahn's algorithm: as each course with <code>in_degree == 0</code> is popped from the queue, append it to an <code>order</code> list. If <code>len(order) == numCourses</code>, return <code>order</code>; otherwise a cycle exists, return <code>[]</code>!</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Construct <code>graph</code> and <code>in_degree</code> array.</li>
<li>Enqueue all nodes with <code>in_degree == 0</code>.</li>
<li>Initialize <code>order = []</code>.</li>
<li>While queue:
  <ul>
    <li><code>u = queue.popleft()</code>.</li>
    <li><code>order.append(u)</code>.</li>
    <li>For <code>v in graph[u]</code>: <code>in_degree[v] -= 1</code>; if <code>in_degree[v] == 0</code>, <code>queue.append(v)</code>.</li>
  </ul>
</li>
<li>Return <code>order</code> if <code>len(order) == numCourses</code> else <code>[]</code>.</li>
</ol>

<h2>🎞️ Visual dry run — numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]</h2>
<pre class="viz">Graph: 0 -> 1, 0 -> 2, 1 -> 3, 2 -> 3
in_degrees: 0: 0, 1: 1, 2: 1, 3: 2
Queue: [0]
Pop 0 -> order = [0], in_degrees: 1: 0, 2: 0 -> Queue = [1, 2]
Pop 1 -> order = [0, 1], in_degrees: 3: 1
Pop 2 -> order = [0, 1, 2], in_degrees: 3: 0 -> Queue = [3]
Pop 3 -> order = [0, 1, 2, 3]
Valid topological order: [0, 1, 2, 3]! ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>from collections import deque, defaultdict

def findOrder(numCourses, prerequisites):
    graph = defaultdict(list)
    in_degree = [0] * numCourses
    
    for dest, src in prerequisites:
        graph[src].append(dest)
        in_degree[dest] += 1
        
    queue = deque([i for i in range(numCourses) if in_degree[i] == 0])
    order = []
    
    while queue:
        course = queue.popleft()
        order.append(course)
        
        for neighbor in graph[course]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
                
    return order if len(order) == numCourses else []</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(V + E)</strong>. <strong>Space O(V + E)</strong>.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li>Cycle exists: returns empty list <code>[]</code>.</li>
<li>Disconnected components: processes all independent subgraphs correctly.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Course Schedule I ([[207]]).</li>
<li>Alien Dictionary ([[269]]).</li>
</ul>''',

# ============================================================ LC 133
133: '''<h2>🧭 How to think about it</h2>
<p>Given a reference of a node in a connected undirected graph, return a <strong>deep copy</strong> (clone) of the graph. Each node in the graph contains a value (<code>int</code>) and a list of its neighbors (<code>List[Node]</code>).</p>

<h2>🐢 Brute force first</h2>
<p>Traversing without tracking visited clones causes an infinite loop because undirected graphs contain bidirectional cycles!</p>

<div class="insight">💡 <strong>Key insight:</strong> Use a hash map <code>cloned = {original_node: new_cloned_node}</code>.
When visiting <code>node</code>:
1. If <code>node</code> is already in <code>cloned</code>, return <code>cloned[node]</code>.
2. Create clone: <code>copy = Node(node.val)</code> and store in <code>cloned[node] = copy</code>.
3. For each neighbor in <code>node.neighbors</code>: recursively clone it and append to <code>copy.neighbors</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>If <code>node is None</code>, return <code>None</code>.</li>
<li><code>cloned = {}</code>.</li>
<li>Define <code>dfs(curr)</code>:
  <ul>
    <li>If <code>curr in cloned</code>, return <code>cloned[curr]</code>.</li>
    <li><code>copy = Node(curr.val)</code>; <code>cloned[curr] = copy</code>.</li>
    <li>For neighbor in <code>curr.neighbors</code>: <code>copy.neighbors.append(dfs(neighbor))</code>.</li>
    <li>Return <code>copy</code>.</li>
  </ul>
</li>
<li>Return <code>dfs(node)</code>.</li>
</ol>

<h2>🎞️ Visual dry run:</h2>
<pre class="viz">Graph: 1 -- 2
       |    |
       4 -- 3

dfs(1): creates clone(1), cloned={1: c1}
  neighbor 2 -> dfs(2): creates clone(2), cloned={1: c1, 2: c2}
    neighbor 3 -> dfs(3): creates clone(3)
      neighbor 4 -> dfs(4): creates clone(4)
        neighbor 1 -> 1 in cloned! Returns c1 immediately without looping!
Graph deep cloned successfully! ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code>def cloneGraph(node):
    if not node:
        return None
        
    cloned = {}
    
    def dfs(curr):
        if curr in cloned:
            return cloned[curr]
            
        copy = Node(curr.val)
        cloned[curr] = copy
        
        for neighbor in curr.neighbors:
            copy.neighbors.append(dfs(neighbor))
            
        return copy
        
    return dfs(node)</code></pre>
</details>

<h2>⏱️ Complexity</h2>
<p><strong>Time O(V + E)</strong> — Visits each node and edge once. <strong>Space O(V)</strong> for hash map and recursion stack.</p>

<h2>⚠️ Edge cases</h2>
<ul>
<li><code>node is None</code>: returns <code>None</code>.</li>
<li>Single node with no neighbors: returns copy with empty neighbors list.</li>
</ul>

<h2>🔁 Variations &amp; follow-ups</h2>
<ul>
<li>Copy List with Random Pointer ([[138]]).</li>
<li>Clone Binary Tree with Random Pointer ([[1485]]).</li>
</ul>''',

# ============================================================ LC 743
743: '''<h2>🧭 How to think about it</h2>
<p>You have a network of <code>n</code> nodes labeled <code>1</code> to <code>n</code>, and a list of directed edges <code>times[i] = (u, v, w)</code> where <code>w</code> is the signal travel time from <code>u</code> to <code>v</code>. A signal is sent from source node <code>k</code>. Return the minimum time for all nodes to receive the signal. If it is impossible for all nodes to receive it, return <code>-1</code>.</p>

<p>Because all edge weights are non-negative (<code>w &ge; 0</code>), this is the classic <strong>Single-Source Shortest Path (SSSP)</strong> problem, solved optimally by <strong>Dijkstra's Algorithm</strong>. Once we find the shortest travel time from <code>k</code> to every node, the network delay is simply the maximum time among all reached nodes (since signals propagate concurrently).</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Bellman-Ford relaxes all edges <code>V - 1</code> times, taking <code>O(V &times; E)</code>. Floyd-Warshall computes all-pairs in <code>O(V<sup>3</sup>)</code>. Dijkstra with a min-priority queue computes the optimal distances in <code>O((V + E) log V)</code>, which is standard for interview graphs.</p>

<div class="insight">💡 <strong>Key insight:</strong> Dijkstra greedily processes nodes in increasing order of their accumulated distance from source <code>k</code>. Because all weights are non-negative, once a node is popped from the min-heap, its shortest distance is finalized and will never be improved. When the min-heap empties, if we have visited all <code>n</code> nodes, the answer is <code>max(distances.values())</code>; otherwise some node was unreachable, so return <code>-1</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><strong>Build graph adjacency list:</strong> <code>graph = defaultdict(list)</code> mapping <code>u &rarr; (v, w)</code>.</li>
<li><strong>Initialize Dijkstra state:</strong>
  <ul>
    <li>Min-heap <code>pq = [(0, k)]</code> storing pairs of <code>(distance_so_far, node)</code>.</li>
    <li>Visited/shortest distance hash map <code>dist = {}</code>.</li>
  </ul>
</li>
<li><strong>Extract-min loop:</strong>
  <ul>
    <li>Pop <code>(d, u)</code> from <code>pq</code>.</li>
    <li>If <code>u</code> is already in <code>dist</code>, skip it (a stale, longer path was pushed earlier).</li>
    <li>Record <code>dist[u] = d</code>.</li>
    <li>If <code>len(dist) == n</code>, we can stop early—all nodes have their shortest paths!</li>
    <li>For each outgoing neighbor <code>(v, weight)</code> of <code>u</code>: if <code>v</code> not in <code>dist</code>, push <code>(d + weight, v)</code> into <code>pq</code>.</li>
  </ul>
</li>
<li><strong>Evaluate result:</strong> If <code>len(dist) == n</code>, return <code>max(dist.values())</code>; otherwise return <code>-1</code>.</li>
</ol>

<h2>🎞️ Visual dry run — nodes=4, k=2, edges=[(2,1,1), (2,3,1), (3,4,1)]:</h2>
<pre class="viz">Graph topology:
   (1) &larr;[1]&mdash; (2) &mdash;[1]&rarr; (3) &mdash;[1]&rarr; (4)
              ^source

1. pq = [(0, 2)], dist = {}
2. Pop (0, 2): dist[2] = 0. Neighbors: push (1, 1), push (1, 3).
   pq = [(1, 1), (1, 3)]
3. Pop (1, 1): dist[1] = 1. No outgoing edges.
   pq = [(1, 3)]
4. Pop (1, 3): dist[3] = 1. Neighbor: push (1+1, 4) = (2, 4).
   pq = [(2, 4)]
5. Pop (2, 4): dist[4] = 2.
   dist = {2: 0, 1: 1, 3: 1, 4: 2}. len(dist) == 4 == n.
6. Max time = max(0, 1, 1, 2) = 2. Output: 2 ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Python 3 — Clean Dijkstra with Min-Heap</summary>
<pre><code class="language-python">import heapq
from collections import defaultdict

def networkDelayTime(times: list[list[int]], n: int, k: int) -> int:
    """
    Finds maximum time for signal to reach all n nodes from source k using Dijkstra's Algorithm.
    """
    # 1. Build adjacency list: u -> list of (v, weight)
    graph = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))
        
    # 2. Priority queue: stores (distance, node). Start at k with dist 0.
    pq = [(0, k)]
    dist = {}
    
    # 3. Dijkstra relaxation loop
    while pq:
        d, u = heapq.heappop(pq)
        
        # If node u already finalized, ignore duplicate queue entry
        if u in dist:
            continue
            
        dist[u] = d
        if len(dist) == n:
            break
            
        for v, weight in graph[u]:
            if v not in dist:
                heapq.heappush(pq, (d + weight, v))
                
    # 4. Check if all n nodes received the signal
    return max(dist.values()) if len(dist) == n else -1
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(E log V)</code>. In the worst case, every directed edge is pushed into the priority queue once. Inserting into and extracting from a binary heap of size up to <code>E</code> takes <code>O(log E) = O(log V)</code> time.</li>
<li><strong>Space Complexity:</strong> <code>O(V + E)</code> to store the adjacency list graph and up to <code>O(E)</code> elements in the priority queue.</li>
</ul>

<h2>🚨 Edge cases to watch out for</h2>
<ul>
<li><strong>Unreachable nodes / Disconnected graph:</strong> If a component has no incoming edges from <code>k</code>, <code>len(dist) < n</code>; must return <code>-1</code>.</li>
<li><strong>Graph with cycles:</strong> The <code>if u in dist: continue</code> check prevents infinite loops in cyclic graphs.</li>
<li><strong>Single node graph (n=1):</strong> Loop pops source, <code>len(dist) == 1 == n</code>, returns <code>0</code> immediately.</li>
</ul>

<h2>🧗 Follow-ups &amp; variations</h2>
<ul>
<li><strong>Path with Maximum Probability ([[1514]]):</strong> Negate probabilities or use max-heap with multiplicative weights.</li>
<li><strong>Cheapest Flights Within K Stops ([[787]]):</strong> Constrained shortest paths where edge count is bounded; use Bellman-Ford or BFS with step tracking.</li>
</ul>''',

# ============================================================ LC 1631
1631: '''<h2>🧭 How to think about it</h2>
<p>You are given a 2D grid <code>heights</code> of size <code>rows x cols</code>. A path's <strong>effort</strong> is the <em>maximum absolute difference</em> in heights between two consecutive cells of the route. You need to find the minimum effort required to travel from <code>(0, 0)</code> to <code>(rows - 1, cols - 1)</code>.</p>

<p>Notice the bottleneck property: we want to find a route whose peak edge difference is minimized. This can be viewed through two lens:</p>
<ol>
  <li><strong>Modified Dijkstra's Algorithm:</strong> Treat each cell as a graph vertex. The distance to a cell is the maximum effort seen along the path to it. A min-heap always expands the path with the smallest peak effort.</li>
  <li><strong>Binary Search on Answer + BFS:</strong> Since effort is bounded in <code>[0, 10^6]</code>, binary search the effort threshold and run a simple BFS/DFS checking if <code>(rows-1, cols-1)</code> is reachable using only step differences &le; mid.</li>
</ol>

<h2>🐢 Brute force vs optimal</h2>
<p>Exploring all simple paths with DFS/backtracking takes <code>O(4^(m &times; n))</code> exponential time. Modified Dijkstra operates in <code>O((m &times; n) log(m &times; n))</code>, which runs comfortably within 100ms.</p>

<div class="insight">💡 <strong>Key insight:</strong> In standard Dijkstra, new path cost is <code>dist + edge_weight</code>. In Minimum Effort, new path cost is <code>max(effort_so_far, abs(heights[r][c] - heights[nr][nc]))</code>. The min-heap guarantees that the first time we pop destination <code>(rows - 1, cols - 1)</code>, its recorded effort is globally minimal!</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Let <code>m = len(heights)</code> and <code>n = len(heights[0])</code>.</li>
<li>Initialize distance table <code>dist = [[float('inf')] * n for _ in range(m)]</code>. Set <code>dist[0][0] = 0</code>.</li>
<li>Min-heap <code>pq = [(0, 0, 0)]</code> containing tuples <code>(effort, r, c)</code>.</li>
<li>While <code>pq</code> is not empty:
  <ul>
    <li>Pop <code>(effort, r, c)</code>.</li>
    <li>If <code>(r, c) == (m - 1, n - 1)</code>, return <code>effort</code> immediately!</li>
    <li>If <code>effort > dist[r][c]</code>, continue (stale entry).</li>
    <li>For each of the 4 cardinal neighbors <code>(nr, nc)</code>:
      <ul>
        <li>Calculate step effort: <code>next_effort = max(effort, abs(heights[r][c] - heights[nr][nc]))</code>.</li>
        <li>If <code>next_effort < dist[nr][nc]</code>: update <code>dist[nr][nc] = next_effort</code> and push <code>(next_effort, nr, nc)</code> into <code>pq</code>.</li>
      </ul>
    </li>
  </ul>
</li>
</ol>

<h2>🎞️ Visual dry run:</h2>
<pre class="viz">Grid:
[1, 2, 2]
[3, 8, 2]
[5, 3, 5]

Path 1: (0,0)->(0,1)->(0,2)->(1,2)->(2,2)
  Heights: 1 -> 2 -> 2 -> 2 -> 5
  Diffs:   |1-2|=1, |2-2|=0, |2-2|=0, |2-5|=3 -> Max effort = 3

Path 2: (0,0)->(1,0)->(2,0)->(2,1)->(2,2)
  Heights: 1 -> 3 -> 5 -> 3 -> 5
  Diffs:   |1-3|=2, |3-5|=2, |5-3|=2, |3-5|=2 -> Max effort = 2!

Dijkstra pops (2, 2) with effort 2 before ever popping effort 3.
Output: 2 ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Python 3 — Modified Dijkstra (Min-Heap)</summary>
<pre><code class="language-python">import heapq

def minimumEffortPath(heights: list[list[int]]) -> int:
    """
    Finds path from (0,0) to bottom-right cell with minimum peak consecutive elevation difference.
    """
    m, n = len(heights), len(heights[0])
    # dist[r][c] stores minimum effort to reach cell (r, c)
    dist = [[float('inf')] * n for _ in range(m)]
    dist[0][0] = 0
    
    # Priority queue stores (effort, row, col)
    pq = [(0, 0, 0)]
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    
    while pq:
        effort, r, c = heapq.heappop(pq)
        
        # Reached destination: first pop is guaranteed minimum
        if r == m - 1 and c == n - 1:
            return effort
            
        if effort > dist[r][c]:
            continue
            
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n:
                step_effort = abs(heights[r][c] - heights[nr][nc])
                new_effort = max(effort, step_effort)
                
                if new_effort < dist[nr][nc]:
                    dist[nr][nc] = new_effort
                    heapq.heappush(pq, (new_effort, nr, nc))
                    
    return 0
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O((m &times; n) log(m &times; n))</code>. There are <code>V = m &times; n</code> cells and at most <code>E = 4 &times; m &times; n</code> edges. Heap operations take <code>O(log(m &times; n))</code>.</li>
<li><strong>Space Complexity:</strong> <code>O(m &times; n)</code> to store the <code>dist</code> matrix and priority queue.</li>
</ul>

<h2>🚨 Edge cases to watch out for</h2>
<ul>
<li><strong>1&times;1 grid:</strong> Start cell is the destination; while loop immediately hits <code>r == 0 and c == 0</code> and returns <code>0</code> effort.</li>
<li><strong>Flat grid (all heights equal):</strong> Effort is <code>0</code> across all transitions.</li>
</ul>

<h2>🧗 Follow-ups &amp; variations</h2>
<ul>
<li><strong>Swim in Rising Water ([[778]]):</strong> Identical concept where cost is <code>max(current_time, grid[nr][nc])</code>.</li>
<li><strong>Minimum Obstacle Removal to Reach Corner ([[2290]]):</strong> 0-1 BFS / Dijkstra on binary obstacle grid.</li>
</ul>''',

# ============================================================ LC 778
778: '''<h2>🧭 How to think about it</h2>
<p>You are given an <code>n x n</code> integer matrix <code>grid</code> where each value represents the elevation at <code>(i, j)</code>. At time <code>t</code>, water level everywhere is <code>t</code>. You can swim from cell to adjacent cell if the elevation of both cells is at most <code>t</code>. Return the minimum time <code>t</code> until you can reach <code>(n - 1, n - 1)</code> starting from <code>(0, 0)</code>.</p>

<p>This is a shortest path problem on a grid where the cost to enter any cell <code>(r, c)</code> along a path is <code>max(time_so_far, grid[r][c])</code>. We want to find a path that minimizes the peak elevation encountered.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Backtracking is exponential. Binary searching the answer <code>t &isin; [0, n^2 - 1]</code> with BFS reachability takes <code>O(n^2 log n)</code>. Modified Dijkstra with a min-heap directly finds the optimal path in <code>O(n^2 log n)</code> with less code.</p>

<div class="insight">💡 <strong>Key insight:</strong> Min-priority queue stores <code>(current_time, r, c)</code>. At each step, pop the cell with the smallest water level needed to reach it. When we pop <code>(n-1, n-1)</code>, that water level is guaranteed to be the minimum time required!</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Initialize min-heap <code>pq = [(grid[0][0], 0, 0)]</code> and a 2D boolean <code>visited</code> array.</li>
<li>Mark <code>visited[0][0] = True</code>.</li>
<li>While <code>pq</code> is not empty:
  <ul>
    <li>Pop <code>(t, r, c)</code>.</li>
    <li>If <code>r == n - 1 and c == n - 1</code>, return <code>t</code>!</li>
    <li>For each of the 4 neighbors <code>(nr, nc)</code>:
      <ul>
        <li>If inside grid and not visited:</li>
        <li>Mark <code>visited[nr][nc] = True</code>.</li>
        <li>Push <code>(max(t, grid[nr][nc]), nr, nc)</code> into <code>pq</code>.</li>
      </ul>
    </li>
  </ul>
</li>
</ol>

<h2>🎞️ Visual dry run:</h2>
<pre class="viz">Grid:
[ 0,  2]
[ 1,  3]

1. Push (grid[0][0], 0, 0) = (0, 0, 0). visited = {(0,0)}
2. Pop (0, 0, 0).
   Neighbors:
   - (0, 1): elevation 2 -> push (max(0, 2), 0, 1) = (2, 0, 1)
   - (1, 0): elevation 1 -> push (max(0, 1), 1, 0) = (1, 1, 0)
   pq = [(1, 1, 0), (2, 0, 1)]
3. Pop (1, 1, 0).
   Neighbor (1, 1): elevation 3 -> push (max(1, 3), 1, 1) = (3, 1, 1)
   pq = [(2, 0, 1), (3, 1, 1)]
4. Pop (2, 0, 1).
   Neighbor (1, 1) already visited.
5. Pop (3, 1, 1): Destination reached! Return 3 ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Python 3 — Dijkstra via Min-Heap</summary>
<pre><code class="language-python">import heapq

def swimInWater(grid: list[list[int]]) -> int:
    """
    Returns minimum time to swim from (0,0) to (n-1, n-1) using modified Dijkstra.
    """
    n = len(grid)
    visited = [[False] * n for _ in range(n)]
    visited[0][0] = True
    
    # Priority queue stores (time_required, row, col)
    pq = [(grid[0][0], 0, 0)]
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    
    while pq:
        t, r, c = heapq.heappop(pq)
        
        if r == n - 1 and c == n - 1:
            return t
            
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and not visited[nr][nc]:
                visited[nr][nc] = True
                heapq.heappush(pq, (max(t, grid[nr][nc]), nr, nc))
                
    return 0
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(n<sup>2</sup> log n)</code>. Each cell is pushed and popped from the priority queue at most once. Priority queue contains at most <code>n^2</code> elements, making heap operations <code>O(log n^2) = O(log n)</code>.</li>
<li><strong>Space Complexity:</strong> <code>O(n<sup>2</sup>)</code> for the visited matrix and priority queue.</li>
</ul>

<h2>🚨 Edge cases to watch out for</h2>
<ul>
<li><strong>1&times;1 grid:</strong> Returns <code>grid[0][0]</code> directly on first pop.</li>
<li><strong>Start cell elevation high:</strong> If <code>grid[0][0]</code> is large, time must be at least <code>grid[0][0]</code> because you must wait for water to cover the start cell before you can even begin swimming!</li>
</ul>''',

# ============================================================ LC 261
261: '''<h2>🧭 How to think about it</h2>
<p>You have a graph of <code>n</code> nodes labeled from <code>0</code> to <code>n - 1</code> and a list of undirected edges. Determine if these edges form a <strong>valid tree</strong>.</p>

<p>By mathematical definition, an undirected graph of <code>n</code> nodes is a tree if and only if:</p>
<ol>
  <li>It contains <strong>no cycles</strong>.</li>
  <li>It is <strong>fully connected</strong> (all nodes belong to a single connected component).</li>
  <li>It has exactly <code>n - 1</code> edges.</li>
</ol>

<h2>🐢 Brute force vs optimal</h2>
<p>If <code>len(edges) != n - 1</code>, it cannot possibly be a tree!
<ul>
  <li>If <code>len(edges) < n - 1</code>, the graph is disconnected.</li>
  <li>If <code>len(edges) > n - 1</code>, by the Pigeonhole Principle the graph must contain at least one cycle.</li>
</ul>
Thus, we can instantly return <code>False</code> if <code>len(edges) != n - 1</code>. Then, we only need to verify either connectivity or cycle freedom using <strong>Disjoint Set Union (DSU)</strong> or <strong>BFS/DFS</strong>.</p>

<div class="insight">💡 <strong>Key insight:</strong> Using Disjoint Set Union (Union-Find) with path compression: Start with <code>n</code> disjoint components. For each edge <code>(u, v)</code>: find the representatives of <code>u</code> and <code>v</code>. If <code>find(u) == find(v)</code>, they are already connected, so adding this edge creates a cycle &rarr; return <code>False</code>! Otherwise union them and decrement component count. At the end, must have exactly 1 component!</div>

<h2>🪜 The approach, step by step (DSU)</h2>
<ol>
<li>Check base condition: if <code>len(edges) != n - 1</code>, return <code>False</code> immediately.</li>
<li>Initialize <code>parent = list(range(n))</code> and <code>rank = [1] * n</code>.</li>
<li>Define <code>find(i)</code> with recursive path compression: <code>parent[i] = find(parent[i])</code>.</li>
<li>Define <code>union(u, v)</code>:
  <ul>
    <li>Find roots <code>root_u = find(u)</code> and <code>root_v = find(v)</code>.</li>
    <li>If <code>root_u == root_v</code>, return <code>False</code> (cycle detected!).</li>
    <li>Attach smaller rank tree under larger rank tree. Return <code>True</code>.</li>
  </ul>
</li>
<li>Iterate through every edge: if <code>not union(u, v)</code>, return <code>False</code>.</li>
<li>Return <code>True</code> (since <code>len(edges) == n - 1</code> and no cycles were found, it must be connected).</li>
</ol>

<h2>🎞️ Visual dry run — n=5, edges=[(0,1), (0,2), (0,3), (1,4)]:</h2>
<pre class="viz">1. len(edges) = 4 == n - 1 (5 - 1). Check passed!
2. union(0, 1): merged. components = 4
3. union(0, 2): merged. components = 3
4. union(0, 3): merged. components = 2
5. union(1, 4): merged. components = 1
All 4 edges processed with zero cycles.
Result: True (Valid tree) ✓

Counterexample: n=5, edges=[(0,1),(1,2),(2,3),(1,3),(1,4)]
len(edges) = 5 != 4 -> Immediately False! ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Python 3 — Union-Find with Path Compression &amp; Rank</summary>
<pre><code class="language-python">def validTree(n: int, edges: list[list[int]]) -> bool:
    """
    Checks if n nodes and undirected edges form a single acyclic connected tree.
    """
    # A valid tree with n nodes must have exactly n - 1 edges
    if len(edges) != n - 1:
        return False
        
    parent = list(range(n))
    rank = [1] * n
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])  # Path compression
        return parent[x]
        
    def union(x, y):
        rx, ry = find(x), find(y)
        if rx == ry:
            return False  # Cycle detected: x and y already in same component!
            
        # Union by rank
        if rank[rx] < rank[ry]:
            parent[rx] = ry
        elif rank[rx] > rank[ry]:
            parent[ry] = rx
        else:
            parent[ry] = rx
            rank[rx] += 1
        return True
        
    for u, v in edges:
        if not union(u, v):
            return False
            
    return True
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(N &times; &alpha;(N)) &approx; O(N)</code>, where <code>&alpha;</code> is the Inverse Ackermann function (less than 5 for all practical input sizes). Checking edge count is <code>O(1)</code>, and processing <code>n - 1</code> edges with path compression runs in near-linear time.</li>
<li><strong>Space Complexity:</strong> <code>O(N)</code> for the parent and rank arrays.</li>
</ul>

<h2>🚨 Edge cases to watch out for</h2>
<ul>
<li><code>n = 1, edges = []</code>: <code>len(edges) == 0 == n - 1</code>, returns <code>True</code>. A single isolated node is a valid tree.</li>
<li><strong>Disconnected components with cycle:</strong> e.g. a triangle of 3 nodes and 2 isolated nodes with 4 edges total. Handled because DSU catches the triangle cycle.</li>
</ul>

<h2>🧗 Follow-ups &amp; variations</h2>
<ul>
<li><strong>Number of Connected Components ([[323]]):</strong> Count distinct tree roots.</li>
<li><strong>Redundant Connection ([[684]]):</strong> Return the exact edge that closes the cycle.</li>
</ul>''',

# ============================================================ LC 323
323: '''<h2>🧭 How to think about it</h2>
<p>Given <code>n</code> nodes labeled <code>0</code> to <code>n - 1</code> and a list of undirected edges, return the total number of connected components in the graph.</p>

<p>Every node starts as its own independent component (total <code>n</code> components). Every time an edge connects two previously disconnected components, the total component count decreases by 1.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Standard DFS or BFS explores each component in <code>O(V + E)</code> time. Disjoint Set Union (DSU) solves this interactively in <code>O(E &times; &alpha;(V))</code> time with clean, concise code.</p>

<div class="insight">💡 <strong>Key insight:</strong> Initialize <code>count = n</code>. For each edge <code>(u, v)</code>, attempt <code>union(u, v)</code>. If <code>u</code> and <code>v</code> were in different sets, decrement <code>count -= 1</code>. When all edges are processed, <code>count</code> is the exact number of connected components!</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Initialize <code>count = n</code>.</li>
<li>Initialize <code>parent = list(range(n))</code>.</li>
<li>Implement <code>find(x)</code> with path compression.</li>
<li>Implement <code>union(u, v)</code>:
  <ul>
    <li>If <code>find(u) != find(v)</code>: set <code>parent[find(u)] = find(v)</code> and decrement <code>count -= 1</code>.</li>
  </ul>
</li>
<li>Process all edges, return final <code>count</code>.</li>
</ol>

<h2>🎞️ Visual dry run — n=5, edges=[(0,1), (1,2), (3,4)]:</h2>
<pre class="viz">Initial components: {0}, {1}, {2}, {3}, {4} -> count = 5

1. Edge (0, 1): union(0, 1) -> {0, 1}, {2}, {3}, {4} -> count = 4
2. Edge (1, 2): union(1, 2) -> {0, 1, 2}, {3}, {4} -> count = 3
3. Edge (3, 4): union(3, 4) -> {0, 1, 2}, {3, 4} -> count = 2
Finished edges! Return count = 2 ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Python 3 — Union-Find</summary>
<pre><code class="language-python">def countComponents(n: int, edges: list[list[int]]) -> int:
    """
    Returns the number of connected components in an undirected graph using DSU.
    """
    parent = list(range(n))
    count = n
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
        
    for u, v in edges:
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv
            count -= 1
            
    return count
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(V + E &times; &alpha;(V)) &approx; O(V + E)</code>.</li>
<li><strong>Space Complexity:</strong> <code>O(V)</code> for the parent array.</li>
</ul>

<h2>🚨 Edge cases to watch out for</h2>
<ul>
<li><code>edges = []</code>: Returns <code>n</code> (every node is an isolated component).</li>
<li><strong>Multiple edges connecting same components:</strong> Duplicate edges have <code>ru == rv</code>, which safely leaves <code>count</code> unchanged.</li>
</ul>''',

# ============================================================ LC 684
684: '''<h2>🧭 How to think about it</h2>
<p>A tree is an undirected graph that is connected and has no cycles. You are given a graph that started as a tree with <code>n</code> nodes labeled <code>1</code> to <code>n</code>, but one extra edge was added. Find the edge that can be removed so that the resulting graph is a tree. If there are multiple answers, return the one that occurs last in the input.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>For each edge, temporarily remove it and check if remaining graph is a tree via DFS: <code>O(E &times; (V + E)) = O(N^2)</code>. With Union-Find, we can find the cycle in a single pass in <code>O(N &times; &alpha;(N)) &approx; O(N)</code>!</p>

<div class="insight">💡 <strong>Key insight:</strong> Iterate through <code>edges</code> in order. For each edge <code>(u, v)</code>: check if <code>find(u) == find(v)</code>. If they already share the same root, they are already connected through some path in the tree. Therefore, adding <code>(u, v)</code> directly creates a cycle! Since we iterate in order, the first edge that connects two already-connected nodes is our answer!</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Initialize <code>parent = list(range(n + 1))</code> (1-indexed).</li>
<li>Define <code>find(x)</code> with path compression.</li>
<li>For each <code>u, v</code> in <code>edges</code>:
  <ul>
    <li><code>ru = find(u), rv = find(v)</code>.</li>
    <li>If <code>ru == rv</code>: return <code>[u, v]</code> immediately!</li>
    <li>Otherwise, union them: <code>parent[ru] = rv</code>.</li>
  </ul>
</li>
</ol>

<h2>🎞️ Visual dry run — edges=[(1,2), (1,3), (2,3)]:</h2>
<pre class="viz">1. Edge (1, 2): find(1)=1, find(2)=2. Union -> parent[1]=2.
2. Edge (1, 3): find(1)=2, find(3)=3. Union -> parent[2]=3.
   Now 1, 2, 3 all belong to component 3.
3. Edge (2, 3): find(2)=3, find(3)=3.
   find(2) == find(3)! Cycle detected!
   Return [2, 3] ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Python 3 — DSU</summary>
<pre><code class="language-python">def findRedundantConnection(edges: list[list[int]]) -> list[int]:
    """
    Finds the redundant edge that creates a cycle in an undirected graph.
    """
    n = len(edges)
    parent = list(range(n + 1))
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
        
    for u, v in edges:
        ru, rv = find(u), find(v)
        if ru == rv:
            return [u, v]
        parent[ru] = rv
        
    return []
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(N &times; &alpha;(N)) &approx; O(N)</code>.</li>
<li><strong>Space Complexity:</strong> <code>O(N)</code> for parent array.</li>
</ul>

<h2>🧗 Follow-ups &amp; variations</h2>
<ul>
<li><strong>Redundant Connection II ([[685]]):</strong> Directed graph variant where nodes can have indegree 2 or cycles.</li>
</ul>''',

# ============================================================ LC 721
721: '''<h2>🧭 How to think about it</h2>
<p>Given a list of accounts where each element <code>accounts[i]</code> is a list of strings: the first element is a name, and the remaining elements are emails. If two accounts share a common email, both accounts belong to the same person. Merge the accounts and return the list of merged accounts where emails are sorted lexicographically.</p>

<p>This is a <strong>connected components</strong> problem on a graph. The nodes of the graph are individual emails! If an account contains emails <code>[e1, e2, e3]</code>, there are edges between <code>e1 &mdash; e2</code> and <code>e1 &mdash; e3</code>. All emails in the same connected component belong to the same person.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Iteratively checking pairs of accounts for email intersections takes <code>O(A<sup>2</sup> &times; E)</code>, which is too slow. Using <strong>Disjoint Set Union (DSU)</strong> or <strong>DFS</strong> on an email adjacency graph merges all accounts in <code>O(N &times; E log(N &times; E))</code>, dominated only by the final sorting of emails.</p>

<div class="insight">💡 <strong>Key insight:</strong> Map each email to its owner's name. Within each account <code>[name, e1, e2, ...]</code>, union the first email <code>e1</code> with every other email <code>e_i</code>. After processing all accounts, group all emails by their DSU root representative: <code>components[find(email)].append(email)</code>. Finally, format each component as <code>[email_to_name[root]] + sorted(emails)</code>.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li><strong>Union-Find Data Structure:</strong> Initialize <code>parent = {}</code>. If an email is seen for the first time, set <code>parent[email] = email</code>.</li>
<li><strong>Record Name &amp; Union Emails:</strong>
  <ul>
    <li>Maintain <code>email_to_name = {}</code>.</li>
    <li>For each account <code>name, *emails</code>:</li>
    <li>First email <code>first_email = emails[0]</code>.</li>
    <li>For every email in <code>emails</code>:
      <ul>
        <li>Record <code>email_to_name[email] = name</code>.</li>
        <li><code>union(first_email, email)</code>.</li>
      </ul>
    </li>
  </ul>
</li>
<li><strong>Group by Root:</strong>
  <ul>
    <li>Create <code>groups = defaultdict(list)</code>.</li>
    <li>For every email: <code>groups[find(email)].append(email)</code>.</li>
  </ul>
</li>
<li><strong>Sort &amp; Assemble:</strong>
  <ul>
    <li>For each group: <code>result.append([email_to_name[root]] + sorted(emails))</code>.</li>
    <li>Return <code>result</code>.</li>
  </ul>
</li>
</ol>

<h2>🎞️ Visual dry run:</h2>
<pre class="viz">Account 1: ["John", "johnsmith@mail.com", "john00@mail.com"]
Account 2: ["John", "johnnybravo@mail.com"]
Account 3: ["John", "johnsmith@mail.com", "john_newyork@mail.com"]

1. Account 1: union("johnsmith", "john00")
2. Account 2: "johnnybravo" is isolated component.
3. Account 3: union("johnsmith", "john_newyork")
   "johnsmith" links Account 1 and Account 3!

Groups after find():
- Root "john00": ["johnsmith@mail.com", "john00@mail.com", "john_newyork@mail.com"]
- Root "johnnybravo": ["johnnybravo@mail.com"]

Output:
[["John", "john00@mail.com", "john_newyork@mail.com", "johnsmith@mail.com"],
 ["John", "johnnybravo@mail.com"]] ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Python 3 — DSU by Email Strings</summary>
<pre><code class="language-python">from collections import defaultdict

def accountsMerge(accounts: list[list[str]]) -> list[list[str]]:
    """
    Merges accounts belonging to the same person using Disjoint Set Union on emails.
    """
    parent = {}
    email_to_name = {}
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
        
    def union(x, y):
        rx, ry = find(x), find(y)
        if rx != ry:
            parent[rx] = ry

    # 1. Initialize parents and union emails within each account
    for account in accounts:
        name = account[0]
        first_email = account[1]
        
        for email in account[1:]:
            if email not in parent:
                parent[email] = email
            email_to_name[email] = name
            union(first_email, email)
            
    # 2. Group emails by their root representative
    groups = defaultdict(list)
    for email in parent:
        root = find(email)
        groups[root].append(email)
        
    # 3. Format result: [name] + sorted(emails)
    res = []
    for root, emails in groups.items():
        res.append([email_to_name[root]] + sorted(emails))
        
    return res
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(N &times; K log(N &times; K))</code> where <code>N</code> is the number of accounts and <code>K</code> is the maximum number of emails per account. Union-Find operations take <code>O(N &times; K &times; &alpha;(N &times; K))</code>, and sorting the merged email lists takes <code>O(total_emails log(total_emails))</code>.</li>
<li><strong>Space Complexity:</strong> <code>O(N &times; K)</code> to store parents, names, and groups.</li>
</ul>

<h2>🚨 Edge cases to watch out for</h2>
<ul>
<li><strong>Same person name, different people:</strong> Two different people named "John" with completely different emails must NOT be merged. Since we only union by email connectivity, they naturally stay in separate components.</li>
<li><strong>Duplicate emails inside a single account:</strong> Handled seamlessly by the hash map representation.</li>
</ul>''',

# ============================================================ LC 269
269: '''<h2>🧭 How to think about it</h2>
<p>There is a new alien language that uses the English alphabet. However, the order of the letters is unknown to you. You are given a list of strings <code>words</code> from the alien language dictionary, where the words are claimed to be sorted lexicographically by the rules of this language. Derive the order of letters in this language. If the order is invalid, return <code>""</code>. If there are multiple valid orders, return any of them.</p>

<p>This is the definitive interview problem for <strong>Topological Sort</strong> on a Directed Acyclic Graph (DAG) using <strong>Kahn's Algorithm</strong>.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Each pair of adjacent words provides a relative ordering constraint between two characters. Comparing every word with every other word takes <code>O(W^2)</code>, but because the dictionary is already sorted, we only need to compare adjacent words <code>words[i]</code> and <code>words[i+1]</code> in <code>O(W &times; L)</code> where <code>L</code> is maximum word length.</p>

<div class="insight">💡 <strong>Key insight:</strong>
<ol>
  <li><strong>Edge Extraction:</strong> For adjacent words <code>w1</code> and <code>w2</code>: find the first index <code>j</code> where <code>w1[j] != w2[j]</code>. This tells us <code>w1[j]</code> must come before <code>w2[j]</code> &rarr; directed edge <code>w1[j] &rarr; w2[j]</code>, and increment <code>in_degree[w2[j]] += 1</code>.</li>
  <li><strong>Prefix Invalidity Trap:</strong> If <code>len(w1) > len(w2)</code> and <code>w1.startswith(w2)</code> (e.g. <code>["apple", "app"]</code>), the dictionary is invalid! In any valid lexicographical order, a prefix must come before its longer version. Return <code>""</code> immediately!</li>
  <li><strong>Topological BFS:</strong> Push all characters with <code>in_degree == 0</code> into a queue. Pop and append to result string, decrementing neighbors' in-degrees. If the final string length equals the number of unique characters, return it; otherwise a cycle exists (e.g. <code>a &rarr; b &rarr; a</code>), so return <code>""</code>.</li>
</ol></div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Initialize <code>adj = {c: set() for word in words for c in word}</code> and <code>in_degree = {c: 0 for c in adj}</code>.</li>
<li>For <code>i</code> from <code>0</code> to <code>len(words) - 2</code>:
  <ul>
    <li><code>w1, w2 = words[i], words[i+1]</code>.</li>
    <li>If <code>len(w1) > len(w2) and w1.startswith(w2)</code>: return <code>""</code>.</li>
    <li>Find first differing index <code>j</code>:
      <ul>
        <li>If <code>w2[j] not in adj[w1[j]]</code>: add <code>w2[j]</code> to <code>adj[w1[j]]</code> and increment <code>in_degree[w2[j]] += 1</code>.</li>
        <li>Break (subsequent characters give no ordering information).</li>
      </ul>
    </li>
  </ul>
</li>
<li>Queue <code>q = deque([c for c, deg in in_degree.items() if deg == 0])</code>.</li>
<li>While <code>q</code>:
  <ul>
    <li>Pop <code>c</code>, append to <code>order</code>.</li>
    <li>For neighbor <code>nxt in adj[c]</code>:
      <ul>
        <li><code>in_degree[nxt] -= 1</code>.</li>
        <li>If <code>in_degree[nxt] == 0</code>: push <code>nxt</code> to <code>q</code>.</li>
      </ul>
    </li>
  </ul>
</li>
<li>Return <code>"".join(order)</code> if <code>len(order) == len(in_degree)</code> else <code>""</code>.</li>
</ol>

<h2>🎞️ Visual dry run — words = ["wrt","wrf","er","ett","rftt"]:</h2>
<pre class="viz">Compare adjacent words:
1. "wrt" vs "wrf": 't' != 'f' -> Edge: t -> f
2. "wrf" vs "er":  'w' != 'e' -> Edge: w -> e
3. "er"  vs "ett": 'r' != 't' -> Edge: r -> t
4. "ett" vs "rftt":'e' != 'r' -> Edge: e -> r

Graph:
w -> e -> r -> t -> f
In-degrees: {w:0, e:1, r:1, t:1, f:1}

Kahn's BFS:
1. Pop 'w' (deg 0): order = ['w'], e's deg becomes 0
2. Pop 'e' (deg 0): order = ['w', 'e'], r's deg becomes 0
3. Pop 'r' (deg 0): order = ['w', 'e', 'r'], t's deg becomes 0
4. Pop 't' (deg 0): order = ['w', 'e', 'r', 't'], f's deg becomes 0
5. Pop 'f' (deg 0): order = ['w', 'e', 'r', 't', 'f']

Length matches 5 unique chars!
Output: "wertf" ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Python 3 — Kahn's Algorithm (Topological Sort)</summary>
<pre><code class="language-python">from collections import deque

def alienOrder(words: list[str]) -> str:
    """
    Derives alien alphabet ordering using Kahn's topological sort algorithm.
    """
    # 1. Initialize graph and in-degree maps for all unique characters
    adj = {c: set() for word in words for c in word}
    in_degree = {c: 0 for c in adj}
    
    # 2. Build graph from adjacent word comparisons
    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i + 1]
        min_len = min(len(w1), len(w2))
        
        # Check invalid prefix case: e.g. ["apple", "app"]
        if len(w1) > len(w2) and w1[:min_len] == w2[:min_len]:
            return ""
            
        for j in range(min_len):
            if w1[j] != w2[j]:
                if w2[j] not in adj[w1[j]]:
                    adj[w1[j]].add(w2[j])
                    in_degree[w2[j]] += 1
                break  # Only first differing character determines order
                
    # 3. BFS with queue of characters with in-degree == 0
    q = deque([c for c, deg in in_degree.items() if deg == 0])
    order = []
    
    while q:
        c = q.popleft()
        order.append(c)
        for neighbor in adj[c]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                q.append(neighbor)
                
    # 4. If order length equals unique characters, valid DAG; else cycle exists
    return "".join(order) if len(order) == len(in_degree) else ""
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(C)</code> where <code>C</code> is the total length of all words in the input. Extracting edges examines each character at most once. Topological sort visits at most 26 vertices and edges.</li>
<li><strong>Space Complexity:</strong> <code>O(1)</code> or <code>O(U + min(U^2, N))</code> where <code>U &le; 26</code> is the alphabet size. Storage is bounded by at most 26 nodes.</li>
</ul>

<h2>🚨 Edge cases to watch out for</h2>
<ul>
<li><strong>Prefix anomaly:</strong> <code>["abc", "ab"]</code> &rarr; must return <code>""</code>.</li>
<li><strong>Cycles:</strong> <code>["z", "x", "z"]</code> &rarr; <code>z &rarr; x</code> and <code>x &rarr; z</code> &rarr; cycle detected, returns <code>""</code>.</li>
<li><strong>Single character or single word:</strong> Returns the character(s) in any valid order.</li>
</ul>''',

# ============================================================ LC 310
310: '''<h2>🧭 How to think about it</h2>
<p>A tree is an undirected graph in which any two vertices are connected by exactly one path. The <strong>height</strong> of a rooted tree is the number of edges on the longest downward path between the root and a leaf. Given <code>n</code> nodes labeled <code>0</code> to <code>n - 1</code> and a tree of <code>n - 1</code> edges, find all nodes that, when chosen as root, produce a tree with <strong>minimum height</strong>. Return a list of all such roots (Minimum Height Trees, or MHTs).</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Running BFS from every single node to compute its height takes <code>O(N &times; (V + E)) = O(N^2)</code>, which TLEs on <code>n = 20,000</code>.</p>

<div class="insight">💡 <strong>Key insight:</strong> The roots that minimize tree height are the <strong>centroids</strong> of the tree! In graph theory, any tree has either <strong>1 or 2 centroids</strong>.
<br><br>
Think of this like <strong>peeling an onion</strong> from the outside in: repeatedly trim all current leaf nodes (nodes with <code>degree == 1</code>) layer by layer. The last remaining 1 or 2 nodes in the core are guaranteed to be the centroids!</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Base cases: if <code>n &le; 2</code>, all nodes are already MHT roots; return <code>list(range(n))</code>.</li>
<li>Build adjacency sets: <code>adj = defaultdict(set)</code>.</li>
<li>Find all initial leaves: <code>leaves = [i for i in range(n) if len(adj[i]) == 1]</code>.</li>
<li>Maintain remaining node count: <code>remaining_nodes = n</code>.</li>
<li>While <code>remaining_nodes > 2</code>:
  <ul>
    <li>Subtract current leaves: <code>remaining_nodes -= len(leaves)</code>.</li>
    <li>New leaves list <code>new_leaves = []</code>.</li>
    <li>For each leaf in <code>leaves</code>:
      <ul>
        <li>Find its only neighbor: <code>neighbor = adj[leaf].pop()</code>.</li>
        <li>Remove leaf from neighbor: <code>adj[neighbor].remove(leaf)</code>.</li>
        <li>If neighbor now has <code>len(adj[neighbor]) == 1</code>: append neighbor to <code>new_leaves</code>.</li>
      </ul>
    </li>
    <li><code>leaves = new_leaves</code>.</li>
  </ul>
</li>
<li>Return <code>leaves</code> (contains either 1 or 2 nodes).</li>
</ol>

<h2>🎞️ Visual dry run — n=6, edges=[(3,0),(3,1),(3,2),(3,4),(5,4)]:</h2>
<pre class="viz">Tree structure:
0 1 -- 3 -- 4 -- 5
2 /

1. Initial leaves (degree 1): [0, 1, 2, 5]. remaining = 6.
2. Trim leaves [0, 1, 2, 5]:
   - Removing 0, 1, 2 leaves node 3 with only neighbor 4 (degree 1).
   - Removing 5 leaves node 4 with only neighbor 3 (degree 1).
   remaining = 6 - 4 = 2 nodes left.
3. remaining <= 2 -> Stop!
Remaining centroids: [3, 4]
Output: [3, 4] ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Python 3 — Leaf Trimming (Topological Onion Peeling)</summary>
<pre><code class="language-python">from collections import defaultdict

def findMinHeightTrees(n: int, edges: list[list[int]]) -> list[int]:
    """
    Finds centroids of tree by iteratively trimming leaf nodes layer by layer.
    """
    if n <= 2:
        return list(range(n))
        
    # 1. Build adjacency list using sets for O(1) edge removal
    adj = defaultdict(set)
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
        
    # 2. Collect initial leaves
    leaves = [i for i in range(n) if len(adj[i]) == 1]
    
    # 3. Trim leaves until 1 or 2 centroids remain
    remaining_nodes = n
    while remaining_nodes > 2:
        remaining_nodes -= len(leaves)
        new_leaves = []
        for leaf in leaves:
            # The only neighbor of this leaf
            neighbor = adj[leaf].pop()
            adj[neighbor].remove(leaf)
            if len(adj[neighbor]) == 1:
                new_leaves.append(neighbor)
        leaves = new_leaves
        
    return leaves
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(N)</code>. Each node and edge is examined and removed at most once during the leaf-trimming process.</li>
<li><strong>Space Complexity:</strong> <code>O(N)</code> to store the adjacency sets and leaf lists.</li>
</ul>

<h2>🚨 Edge cases to watch out for</h2>
<ul>
<li><code>n = 1</code>: Returns <code>[0]</code> immediately.</li>
<li><code>n = 2</code>: Returns <code>[0, 1]</code>.</li>
<li><strong>Linear line graph:</strong> Centroids are the exact middle node (if odd length) or middle two nodes (if even length).</li>
</ul>''',

# ============================================================ LC 785
785: '''<h2>🧭 How to think about it</h2>
<p>An undirected graph is <strong>bipartite</strong> if we can split its set of nodes into two independent subsets <code>A</code> and <code>B</code> such that every edge in the graph connects a node in <code>A</code> and a node in <code>B</code>.</p>

<p>In graph theory, this is identical to <strong>2-Coloring</strong>: can we color every vertex with one of two colors (e.g. Red and Blue, or <code>1</code> and <code>-1</code>) such that no two adjacent vertices have the same color?</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Trying all 2^n coloring combinations is exponential. BFS or DFS 2-coloring checks the graph in <code>O(V + E)</code> time.</p>

<div class="insight">💡 <strong>Key insight:</strong> An undirected graph is bipartite <strong>if and only if it contains NO odd-length cycles</strong>.
<br><br>
Iterate through all nodes <code>0</code> to <code>n - 1</code>. If a node is uncolored, start a BFS/DFS from it with color <code>1</code>. For every neighbor:
<ul>
  <li>If uncolored: assign it <code>-color</code> and recurse.</li>
  <li>If already colored: it MUST have color <code>-color</code>. If it has the SAME color, a conflict (odd cycle) is detected &rarr; return <code>False</code>!</li>
</ul></div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Initialize <code>color = {}</code>.</li>
<li>For each node <code>i</code> from <code>0</code> to <code>n - 1</code>:
  <ul>
    <li>If <code>i</code> not in <code>color</code>:
      <ul>
        <li>Launch <code>bfs(i)</code>: queue <code>q = deque([i])</code>, set <code>color[i] = 1</code>.</li>
        <li>While <code>q</code>:
          <ul>
            <li>Pop <code>u</code>.</li>
            <li>For neighbor <code>v in graph[u]</code>:
              <ul>
                <li>If <code>v not in color</code>: set <code>color[v] = -color[u]</code>, push <code>v</code>.</li>
                <li>Else if <code>color[v] == color[u]</code>: return <code>False</code>!</li>
              </ul>
            </li>
          </ul>
        </li>
      </ul>
    </li>
  </ul>
</li>
<li>Return <code>True</code>.</li>
</ol>

<h2>🎞️ Visual dry run:</h2>
<pre class="viz">Graph: 0 -- 1
       |    |
       3 -- 2

1. color[0] = 1 (Blue)
2. Neighbors of 0: 1 and 3 -> color[1] = -1 (Red), color[3] = -1 (Red)
3. Neighbor of 1: 2 -> color[2] = 1 (Blue)
4. Check 3's neighbor 2: color[3]=-1 != color[2]=1. Valid!
Result: True (Bipartite) ✓

Odd cycle counterexample: Triangle 0-1-2
0 (Blue) -> 1 (Red) -> 2 (Blue)
Edge 2-0 connects Blue to Blue! Conflict! Output: False ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Python 3 — BFS 2-Coloring</summary>
<pre><code class="language-python">from collections import deque

def isBipartite(graph: list[list[int]]) -> bool:
    """
    Determines if graph is 2-colorable using BFS traversal across all components.
    """
    n = len(graph)
    color = {}  # node -> 1 or -1
    
    for i in range(n):
        if i not in color:
            color[i] = 1
            q = deque([i])
            
            while q:
                u = q.popleft()
                for v in graph[u]:
                    if v not in color:
                        color[v] = -color[u]
                        q.append(v)
                    elif color[v] == color[u]:
                        return False  # Odd cycle found
                        
    return True
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(V + E)</code>. Each node is colored once and each edge is inspected twice.</li>
<li><strong>Space Complexity:</strong> <code>O(V)</code> for the color dictionary and BFS queue.</li>
</ul>

<h2>🧗 Follow-ups &amp; variations</h2>
<ul>
<li><strong>Possible Bipartition ([[886]]):</strong> Split people into two groups based on dislikes; same 2-coloring problem.</li>
</ul>''',

# ============================================================ LC 787
787: '''<h2>🧭 How to think about it</h2>
<p>There are <code>n</code> cities connected by flights with prices. Given <code>src</code>, <code>dst</code>, and an integer <code>k</code>, return the cheapest price from <code>src</code> to <code>dst</code> with <strong>at most <code>k</code> stops</strong> (i.e. at most <code>k + 1</code> flight legs). If no such route exists, return <code>-1</code>.</p>

<p>Because the number of edges is explicitly bounded by <code>k + 1</code>, standard Dijkstra's algorithm fails if it greedily explores a cheap path that consumes too many stops. Instead, this problem is custom-built for <strong>Bellman-Ford Algorithm</strong> run for exactly <code>k + 1</code> rounds, or <strong>BFS level-by-level</strong>.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>DFS backtracking is exponential. Bellman-Ford runs in <code>O((K + 1) &times; E)</code> time and takes <code>O(V)</code> auxiliary space.</p>

<div class="insight">💡 <strong>Key insight:</strong>
In Bellman-Ford, iteration <code>i</code> calculates the shortest distance to all vertices using <strong>at most <code>i</code> edges</strong>!
<br><br>
CRITICAL TRICK: At the start of each iteration, copy <code>prices</code> to <code>temp_prices</code>. Relax edges using values from the <em>previous</em> iteration: <code>temp_prices[v] = min(temp_prices[v], prices[u] + weight)</code>. This ensures an iteration uses at most ONE additional flight and prevents a single iteration from cascading through multiple flights!</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Initialize <code>prices = [float('inf')] * n</code>. Set <code>prices[src] = 0</code>.</li>
<li>Loop <code>k + 1</code> times (allowing at most <code>k + 1</code> flights):
  <ul>
    <li>Create a copy: <code>temp = list(prices)</code>.</li>
    <li>For each flight <code>(u, v, cost)</code> in <code>flights</code>:
      <ul>
        <li>If <code>prices[u] != float('inf')</code> and <code>prices[u] + cost < temp[v]</code>:
          <code>temp[v] = prices[u] + cost</code>.</li>
      </ul>
    </li>
    <li>Update <code>prices = temp</code>.</li>
  </ul>
</li>
<li>Return <code>prices[dst]</code> if <code>prices[dst] != float('inf')</code> else <code>-1</code>.</li>
</ol>

<h2>🎞️ Visual dry run — n=3, flights=[(0,1,100),(1,2,100),(0,2,500)], src=0, dst=2, k=1:</h2>
<pre class="viz">Initial prices: [0, inf, inf]

Round 1 (1 flight / 0 stops):
  Edge 0->1 (100): temp[1] = min(inf, 0 + 100) = 100
  Edge 0->2 (500): temp[2] = min(inf, 0 + 500) = 500
  prices after round 1: [0, 100, 500]

Round 2 (2 flights / 1 stop):
  Edge 1->2 (100): temp[2] = min(500, prices[1] + 100) = min(500, 100 + 100) = 200!
  prices after round 2: [0, 100, 200]

Stop count k=1 reached. Output = 200 ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Python 3 — Bellman-Ford with Copy Array</summary>
<pre><code class="language-python">def findCheapestPrice(n: int, flights: list[list[int]], src: int, dst: int, k: int) -> int:
    """
    Computes cheapest flight price from src to dst with at most k stops using Bellman-Ford.
    """
    prices = [float('inf')] * n
    prices[src] = 0
    
    # Run Bellman-Ford for at most k + 1 flights
    for _ in range(k + 1):
        temp = list(prices)
        for u, v, cost in flights:
            if prices[u] != float('inf') and prices[u] + cost < temp[v]:
                temp[v] = prices[u] + cost
        prices = temp
        
    return prices[dst] if prices[dst] != float('inf') else -1
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O((K + 1) &times; E)</code>. There are <code>k + 1</code> rounds, and each round scans all <code>E</code> flights.</li>
<li><strong>Space Complexity:</strong> <code>O(V)</code> to store the prices and temp arrays.</li>
</ul>

<h2>🚨 Edge cases to watch out for</h2>
<ul>
<li><code>src == dst</code>: Cost is 0.</li>
<li><strong>Destination unreachable within k stops:</strong> Returns <code>-1</code> correctly.</li>
<li><strong>Direct flight exists but is more expensive:</strong> The algorithm correctly considers the multi-hop cheaper route if within <code>k</code> stops.</li>
</ul>''',

# ============================================================ LC 752
752: '''<h2>🧭 How to think about it</h2>
<p>You have a 4-wheel lock starting at <code>"0000"</code>. Each wheel has digits <code>'0'</code> through <code>'9'</code> and can rotate forward (<code>9 &rarr; 0</code>) or backward (<code>0 &rarr; 9</code>). You are given a list of <code>deadends</code>: if the lock displays any deadend combination, the wheels lock and you cannot turn them anymore. Return the minimum number of total turns required to reach <code>target</code>, or <code>-1</code> if impossible.</p>

<p>Every combination is a vertex in an unweighted graph. Each combination has <strong>8 neighbors</strong> (4 wheels &times; 2 rotation directions). Since each move has unit cost 1, the shortest path from <code>"0000"</code> to <code>target</code> is solved using <strong>Breadth-First Search (BFS)</strong>.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Standard BFS explores level by level. To make it blaze fast, <strong>Bidirectional BFS</strong> searches from both <code>"0000"</code> and <code>target</code> simultaneously, meeting in the middle!</p>

<div class="insight">💡 <strong>Key insight:</strong> Bidirectional BFS reduces branching volume. If search tree has branching factor <code>b = 8</code> and depth <code>d</code>, single-ended BFS explores <code>O(b<sup>d</sup>)</code> states, whereas bidirectional BFS explores <code>2 &times; O(b<sup>d/2</sup>)</code> states—a massive speedup! Always expand the smaller frontier set at each step.</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Deadend check: if <code>"0000" in deadends</code> or <code>target in deadends</code>, return <code>-1</code> immediately.</li>
<li>Initialize two frontier sets: <code>begin_set = {"0000"}</code> and <code>end_set = {target}</code>.</li>
<li>Initialize <code>visited = set(deadends)</code> and <code>turns = 0</code>.</li>
<li>While <code>begin_set</code> and <code>end_set</code>:
  <ul>
    <li>Always expand the smaller set: if <code>len(begin_set) > len(end_set)</code>, swap them.</li>
    <li>Create <code>next_level = set()</code>.</li>
    <li>For each code in <code>begin_set</code>:
      <ul>
        <li>For each digit position <code>i &isin; [0, 3]</code>:
          <ul>
            <li>Try turning forward (<code>(d + 1) % 10</code>) and backward (<code>(d - 1) % 10</code>).</li>
            <li>If neighbor in <code>end_set</code>: return <code>turns + 1</code> (the two frontiers met!).</li>
            <li>If neighbor not in <code>visited</code>: add to <code>visited</code> and <code>next_level</code>.</li>
          </ul>
        </li>
      </ul>
    </li>
    <li><code>begin_set = next_level</code>, <code>turns += 1</code>.</li>
  </ul>
</li>
<li>Return <code>-1</code>.</li>
</ol>

<h2>🎞️ Visual dry run — start="0000", target="0009":</h2>
<pre class="viz">1. begin = {"0000"}, end = {"0009"}, turns = 0
2. Expand "0000" -> neighbors include:
   wheel 3 backward: (0 - 1) % 10 = 9 -> "0009"!
   "0009" is directly in end_set!
3. Frontiers met! Return turns + 1 = 1 ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Python 3 — Bidirectional BFS</summary>
<pre><code class="language-python">def openLock(deadends: list[str], target: str) -> int:
    """
    Finds minimum turns to open lock avoiding deadends using Bidirectional BFS.
    """
    dead_set = set(deadends)
    if "0000" in dead_set or target in dead_set:
        return -1
    if target == "0000":
        return 0
        
    begin_set = {"0000"}
    end_set = {target}
    visited = set(deadends)
    visited.add("0000")
    visited.add(target)
    turns = 0
    
    while begin_set and end_set:
        # Always expand the smaller frontier set
        if len(begin_set) > len(end_set):
            begin_set, end_set = end_set, begin_set
            
        next_level = set()
        for code in begin_set:
            for i in range(4):
                digit = int(code[i])
                # Generate 2 turns: +1 and -1
                for diff in (-1, 1):
                    new_digit = (digit + diff) % 10
                    neighbor = code[:i] + str(new_digit) + code[i+1:]
                    
                    if neighbor in end_set:
                        return turns + 1
                    if neighbor not in visited:
                        visited.add(neighbor)
                        next_level.add(neighbor)
                        
        turns += 1
        begin_set = next_level
        
    return -1
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(8 &times; 10<sup>4</sup>) = O(1)</code>. The state space is bounded by 10,000 combinations (0000 to 9999), and each state has 8 transitions.</li>
<li><strong>Space Complexity:</strong> <code>O(10<sup>4</sup>) = O(1)</code> for sets and visited storage.</li>
</ul>

<h2>🚨 Edge cases to watch out for</h2>
<ul>
<li><code>"0000"</code> is in <code>deadends</code>: Returns <code>-1</code>.</li>
<li><code>target == "0000"</code>: Returns <code>0</code> immediately.</li>
</ul>''',

# ============================================================ LC 1584
1584: '''<h2>🧭 How to think about it</h2>
<p>You are given an array <code>points</code> representing integer coordinates of <code>n</code> points on a 2D plane, where <code>points[i] = [xi, yi]</code>. The cost of connecting two points <code>[xi, yi]</code> and <code>[xj, yj]</code> is the Manhattan distance: <code>|xi - xj| + |yi - yj|</code>. Return the minimum cost to make all points connected such that there is exactly one simple path between any pair of points.</p>

<p>Connecting all <code>n</code> points with minimum total cost and zero cycles is the textbook definition of a <strong>Minimum Spanning Tree (MST)</strong>. Because every pair of points can be connected, the graph is a <strong>dense complete graph</strong> with <code>V = n</code> vertices and <code>E = n(n - 1) / 2</code> edges.</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Testing all spanning trees is exponential. For finding an MST on a dense graph where <code>E &approx; V^2</code>:
<ul>
  <li><strong>Kruskal's Algorithm:</strong> Requires creating and sorting all <code>O(V^2)</code> edges &rarr; <code>O(V^2 log V)</code> time and <code>O(V^2)</code> memory.</li>
  <li><strong>Prim's Algorithm (Dense Array Variant):</strong> Maintains <code>min_cost[i]</code> for each node. At each step, finds the node outside the tree with smallest cost in <code>O(V)</code> time. Repeating <code>V</code> times takes <code>O(V^2)</code> time and only <code>O(V)</code> space!</li>
</ul></p>

<div class="insight">💡 <strong>Key insight:</strong> Dense Prim's algorithm starts with point 0 in the tree. We maintain <code>min_dist = [inf] * n</code>. At each iteration, pick the unvisited node <code>u</code> with the smallest distance, mark it visited, add its distance to the total cost, and update all other unvisited nodes <code>v</code>: <code>min_dist[v] = min(min_dist[v], manhattan_dist(u, v))</code>. No heap needed! Runs in pure O(N^2) time with zero allocation overhead.</div>

<h2>🪜 The approach, step by step (Dense Prim's)</h2>
<ol>
<li>Let <code>n = len(points)</code>. If <code>n &le; 1</code>, return <code>0</code>.</li>
<li>Initialize <code>min_dist = [float('inf')] * n</code> with <code>min_dist[0] = 0</code>.</li>
<li>Initialize <code>visited = [False] * n</code>, <code>total_cost = 0</code>.</li>
<li>Loop <code>n</code> times (to add all <code>n</code> nodes to the tree):
  <ul>
    <li>Find unvisited node <code>u</code> with minimum <code>min_dist[u]</code>.</li>
    <li>Mark <code>visited[u] = True</code>.</li>
    <li>Add <code>total_cost += min_dist[u]</code>.</li>
    <li>For every unvisited node <code>v</code> from <code>0</code> to <code>n - 1</code>:
      <ul>
        <li>Calculate Manhattan distance: <code>d = abs(points[u][0] - points[v][0]) + abs(points[u][1] - points[v][1])</code>.</li>
        <li>Update <code>min_dist[v] = min(min_dist[v], d)</code>.</li>
      </ul>
    </li>
  </ul>
</li>
<li>Return <code>total_cost</code>.</li>
</ol>

<h2>🎞️ Visual dry run — points = [[0,0],[2,2],[3,10],[5,2],[7,0]]:</h2>
<pre class="viz">1. Start at node 0 [0,0]: cost = 0.
   Distances from 0: node 1(2,2)=4, node 2(3,10)=13, node 3(5,2)=7, node 4(7,0)=7.
2. Pick min unvisited: node 1 (dist 4). total_cost = 0 + 4 = 4.
   Update distances using node 1:
   node 2: min(13, |2-3|+|2-10|=9) = 9
   node 3: min(7, |2-5|+|2-2|=3) = 3!
   node 4: min(7, |2-7|+|2-0|=7) = 7
3. Pick min unvisited: node 3 (dist 3). total_cost = 4 + 3 = 7.
   Update distances using node 3:
   node 2: min(9, |5-3|+|2-10|=10) = 9
   node 4: min(7, |5-7|+|2-0|=4) = 4!
4. Pick min unvisited: node 4 (dist 4). total_cost = 7 + 4 = 11.
   node 2: min(9, |7-3|+|0-10|=14) = 9
5. Pick last unvisited: node 2 (dist 9). total_cost = 11 + 9 = 20.
All 5 points connected into MST! Total cost = 20 ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def minCostConnectPoints(points: list[list[int]]) -> int:
    """
    Computes Minimum Spanning Tree on complete Euclidean point graph using Dense Prim's.
    """
    n = len(points)
    if n <= 1:
        return 0
        
    min_dist = [float('inf')] * n
    min_dist[0] = 0
    visited = [False] * n
    total_cost = 0
    
    for _ in range(n):
        # 1. Pick unvisited vertex with smallest connecting distance
        curr = -1
        curr_dist = float('inf')
        for i in range(n):
            if not visited[i] and min_dist[i] < curr_dist:
                curr_dist = min_dist[i]
                curr = i
                
        # 2. Add vertex to tree
        visited[curr] = True
        total_cost += curr_dist
        x1, y1 = points[curr]
        
        # 3. Update minimum distance to remaining unvisited vertices
        for nxt in range(n):
            if not visited[nxt]:
                x2, y2 = points[nxt]
                dist = abs(x1 - x2) + abs(y1 - y2)
                if dist < min_dist[nxt]:
                    min_dist[nxt] = dist
                    
    return total_cost
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(N^2)</code>. There are <code>N</code> outer iterations; each iteration scans <code>N</code> nodes to find the minimum and another <code>N</code> nodes to update distances. For a dense graph with <code>N(N-1)/2</code> edges, <code>O(N^2)</code> is strictly optimal and beats heap Prim's / Kruskal's <code>O(N^2 log N)</code>.</li>
<li><strong>Space Complexity:</strong> <code>O(N)</code> to store <code>min_dist</code> and <code>visited</code> arrays. Zero storage needed for explicit edges!</li>
</ul>

<h2>🚨 Edge cases to watch out for</h2>
<ul>
<li><code>n = 1</code>: Cost is 0 (a single point is already connected).</li>
<li><strong>Coincident points:</strong> Distance is 0; correctly handled.</li>
</ul>''',

# ============================================================ LC 1135
1135: '''<h2>🧭 How to think about it</h2>
<p>There are <code>n</code> cities labeled <code>1</code> to <code>n</code>. You are given an array <code>connections</code> where <code>connections[i] = [city1, city2, cost]</code> represents the cost to build a bidirectional road between two cities. Return the minimum cost to connect all <code>n</code> cities such that there is a path between any pair of cities. If it is impossible, return <code>-1</code>.</p>

<p>This is a classic <strong>Minimum Spanning Tree</strong> problem on a sparse graph with explicit edge costs, solved directly by <strong>Kruskal's Algorithm</strong> using Disjoint Set Union (DSU).</p>

<h2>🐢 Brute force vs optimal</h2>
<p>Kruskal's algorithm greedily considers edges in increasing order of weight. If the edge connects two cities that are not yet in the same connected component, we add it to the spanning tree. If all <code>n</code> cities are connected using exactly <code>n - 1</code> edges, the sum of weights is guaranteed to be minimal!</p>

<div class="insight">💡 <strong>Key insight:</strong> Sort edges by cost in ascending order. Process each edge: if <code>union(city1, city2)</code> successfully merges two previously disjoint components, increment our edge counter and accumulate the cost. If we place <code>n - 1</code> edges, return total cost; if edges run out before reaching <code>n - 1</code> edges, the graph is disconnected &rarr; return <code>-1</code>!</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>If <code>len(connections) < n - 1</code>, return <code>-1</code> immediately (impossible to connect <code>n</code> nodes).</li>
<li>Sort <code>connections</code> by cost: <code>connections.sort(key=lambda x: x[2])</code>.</li>
<li>Initialize DSU with <code>parent = list(range(n + 1))</code> (1-indexed) and <code>rank = [1] * (n + 1)</code>.</li>
<li>Initialize <code>total_cost = 0</code>, <code>edges_used = 0</code>.</li>
<li>For each <code>u, v, cost</code> in sorted connections:
  <ul>
    <li>If <code>union(u, v)</code> succeeds:
      <ul>
        <li><code>total_cost += cost</code></li>
        <li><code>edges_used += 1</code></li>
        <li>If <code>edges_used == n - 1</code>, break early!</li>
      </ul>
    </li>
  </ul>
</li>
<li>Return <code>total_cost</code> if <code>edges_used == n - 1</code> else <code>-1</code>.</li>
</ol>

<h2>🎞️ Visual dry run — n=3, connections=[[1,2,5],[1,3,6],[2,3,1]]:</h2>
<pre class="viz">1. Sort by cost: [[2,3,1], [1,2,5], [1,3,6]]
2. Edge [2,3,1]: union(2,3) -> success! cost = 1, edges_used = 1.
3. Edge [1,2,5]: union(1,2) -> success! cost = 1 + 5 = 6, edges_used = 2.
4. edges_used == n - 1 (3 - 1 = 2) -> Done!
Result: 6 ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def minimumCost(n: int, connections: list[list[int]]) -> int:
    """
    Computes minimum cost to connect n cities via Kruskal's MST algorithm.
    """
    if len(connections) < n - 1:
        return -1
        
    # 1. Sort edges by weight
    connections.sort(key=lambda x: x[2])
    
    parent = list(range(n + 1))
    rank = [1] * (n + 1)
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
        
    def union(x, y):
        rx, ry = find(x), find(y)
        if rx == ry:
            return False
        if rank[rx] < rank[ry]:
            parent[rx] = ry
        elif rank[rx] > rank[ry]:
            parent[ry] = rx
        else:
            parent[ry] = rx
            rank[rx] += 1
        return True
        
    total_cost = 0
    edges_count = 0
    
    for u, v, cost in connections:
        if union(u, v):
            total_cost += cost
            edges_count += 1
            if edges_count == n - 1:
                return total_cost
                
    return -1
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(E log E)</code> to sort the edges, where <code>E = len(connections)</code>. The DSU operations take near-linear <code>O(E &times; &alpha;(V))</code> time.</li>
<li><strong>Space Complexity:</strong> <code>O(V)</code> for the parent and rank arrays.</li>
</ul>

<h2>🚨 Edge cases to watch out for</h2>
<ul>
<li><strong>Fewer than n-1 edges:</strong> Handled by upfront check <code>len(connections) < n - 1</code>.</li>
<li><strong>Disconnected components:</strong> If edge count never reaches <code>n - 1</code>, returns <code>-1</code>.</li>
</ul>''',

# ============================================================ LC 1293
1293: '''<h2>🧭 How to think about it</h2>
<p>You are given an <code>m x n</code> integer matrix <code>grid</code> where each cell is either <code>0</code> (empty) or <code>1</code> (obstacle). You can move up, down, left, or right. You can eliminate at most <code>k</code> obstacles. Return the minimum number of steps to walk from <code>(0, 0)</code> to <code>(m - 1, n - 1)</code>, or <code>-1</code> if no such walk exists.</p>

<p>Because each step has unit cost 1, the shortest path is solved with <strong>Breadth-First Search (BFS)</strong>. However, this is not a standard 2D grid BFS—it is a <strong>3D State Space BFS</strong> where a state is defined by <code>(row, col, remaining_eliminations)</code>!</p>

<h2>🐢 Brute force vs optimal</h2>
<p>DFS explores all exponential branching paths. In BFS, each layer represents 1 additional step. If we track visited states as <code>(r, c, k_remaining)</code>, the first time we pop destination <code>(m - 1, n - 1)</code>, its step count is guaranteed to be globally minimal!</p>

<div class="insight">💡 <strong>Key insight:</strong>
<ol>
  <li><strong>Manhattan Distance Shortcut:</strong> The shortest possible path from <code>(0,0)</code> to <code>(m-1, n-1)</code> without any obstacles is <code>m + n - 2</code>. If <code>k >= m + n - 2</code>, we have enough eliminations to blast straight through every single obstacle along the Manhattan path! Return <code>m + n - 2</code> immediately in O(1)!</li>
  <li><strong>State Pruning:</strong> If we have already visited cell <code>(r, c)</code> with <code>rem_k</code> eliminations remaining, visiting it later with &le; <code>rem_k</code> eliminations is strictly worse and can be pruned! Maintain <code>visited[r][c] = max_k_remaining_seen</code>.</li>
</ol></div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>Let <code>m = len(grid), n = len(grid[0])</code>.</li>
<li>If <code>k >= m + n - 2</code>, return <code>m + n - 2</code>.</li>
<li>Initialize queue: <code>q = deque([(0, 0, k, 0)])</code> representing <code>(r, c, k_rem, steps)</code>.</li>
<li>Initialize <code>visited = {(0, 0): k}</code> mapping <code>(r, c) &rarr; max_k_remaining</code>.</li>
<li>While <code>q</code>:
  <ul>
    <li>Pop <code>(r, c, k_rem, steps)</code>.</li>
    <li>If <code>r == m - 1 and c == n - 1</code>, return <code>steps</code>!</li>
    <li>For each neighbor <code>(nr, nc)</code>:
      <ul>
        <li>If inside grid:
          <ul>
            <li>Calculate new eliminations: <code>next_k = k_rem - grid[nr][nc]</code>.</li>
            <li>If <code>next_k >= 0</code> and <code>next_k > visited.get((nr, nc), -1)</code>:
              <ul>
                <li>Record <code>visited[(nr, nc)] = next_k</code>.</li>
                <li>Push <code>(nr, nc, next_k, steps + 1)</code> into <code>q</code>.</li>
              </ul>
            </li>
          </ul>
        </li>
      </ul>
    </li>
  </ul>
</li>
<li>Return <code>-1</code>.</li>
</ol>

<h2>🎞️ Visual dry run:</h2>
<pre class="viz">grid = [[0,1,1],[1,1,0],[1,0,0]], k = 1

(0,0) [k=1, step 0]
 -> step 1: (0,1) obstacle! k=0. steps=1.
    -> step 2: (0,2) obstacle! k=-1 (Invalid!)
    -> step 2: (1,1) obstacle! k=-1 (Invalid!)
 -> step 1: (1,0) obstacle! k=0. steps=1.
    -> step 2: (2,0) obstacle! k=-1 (Invalid!)
    -> step 2: (1,1) obstacle! k=-1 (Invalid!)
Obstacle wall blocks all paths with k=1! Returns -1 ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">from collections import deque

def shortestPath(grid: list[list[int]], k: int) -> int:
    """
    Finds shortest path in grid with at most k obstacle eliminations using 3D State BFS.
    """
    m, n = len(grid)
    if m == 1 and n == 1:
        return 0
        
    # Manhattan shortcut: if k is large enough, walk direct shortest path
    if k >= m + n - 2:
        return m + n - 2
        
    # Queue stores: (row, col, k_remaining, steps)
    q = deque([(0, 0, k, 0)])
    # visited maps (row, col) -> max k_remaining seen so far
    visited = {(0, 0): k}
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    
    while q:
        r, c, k_rem, steps = q.popleft()
        
        if r == m - 1 and c == n - 1:
            return steps
            
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n:
                next_k = k_rem - grid[nr][nc]
                if next_k >= 0 and next_k > visited.get((nr, nc), -1):
                    visited[(nr, nc)] = next_k
                    q.append((nr, nc, next_k, steps + 1))
                    
    return -1
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(M &times; N &times; K)</code>. Each state <code>(r, c, k_remaining)</code> is enqueued at most once. Transitions take <code>O(1)</code> across 4 directions.</li>
<li><strong>Space Complexity:</strong> <code>O(M &times; N &times; K)</code> for the visited dictionary and BFS queue.</li>
</ul>

<h2>🚨 Edge cases to watch out for</h2>
<ul>
<li><code>m = 1, n = 1</code>: Returns <code>0</code> immediately.</li>
<li><code>grid[0][0] == 1</code>: If start cell has obstacle, handled by decrementing initial <code>k</code>.</li>
</ul>''',

# ============================================================ LC 1319
1319: '''<h2>🧭 How to think about it</h2>
<p>There are <code>n</code> computers numbered from <code>0</code> to <code>n - 1</code> connected by ethernet cables <code>connections</code>. You can extract redundant cables from connected computers and reconnect them to unconnected computers. Return the minimum number of times you need to do this to make all computers connected. If it is impossible, return <code>-1</code>.</p>

<p>To connect <code>n</code> nodes into a single connected component, we mathematically need <strong>at least <code>n - 1</code> cables</strong>.
<ul>
  <li>If <code>len(connections) < n - 1</code>: Impossible! Even if we rearrange every cable optimally, there simply aren't enough edges. Return <code>-1</code>.</li>
  <li>If <code>len(connections) >= n - 1</code>: By Graph Theory, any connected graph with <code>C</code> separate components can be linked together into a single component using exactly <code>C - 1</code> edges! Since we know there are surplus redundant edges, the answer is simply <code>components - 1</code>!</li>
</ul></p>

<h2>🐢 Brute force vs optimal</h2>
<p>We only need to count the number of connected components in the graph using <strong>Disjoint Set Union (DSU)</strong> or <strong>DFS</strong> in <code>O(V + E)</code> time!</p>

<div class="insight">💡 <strong>Key insight:</strong>
Check <code>len(connections) < n - 1</code> first. Then count the number of disjoint components <code>components</code>. Every successful union reduces component count. The answer is <code>components - 1</code>!</div>

<h2>🪜 The approach, step by step</h2>
<ol>
<li>If <code>len(connections) < n - 1</code>, return <code>-1</code>.</li>
<li>Initialize <code>parent = list(range(n))</code>, <code>components = n</code>.</li>
<li>Define <code>find(x)</code> with path compression.</li>
<li>For each <code>u, v</code> in <code>connections</code>:
  <ul>
    <li><code>ru, rv = find(u), find(v)</code>.</li>
    <li>If <code>ru != rv</code>: <code>parent[ru] = rv</code>, <code>components -= 1</code>.</li>
  </ul>
</li>
<li>Return <code>components - 1</code>.</li>
</ol>

<h2>🎞️ Visual dry run — n=4, connections=[[0,1],[0,2],[1,2]]:</h2>
<pre class="viz">1. len(connections) = 3 >= 4 - 1 = 3. Possible!
2. Initial components = 4: {0}, {1}, {2}, {3}
3. Edge (0, 1): components = 3 ({0, 1}, {2}, {3})
4. Edge (0, 2): components = 2 ({0, 1, 2}, {3})
5. Edge (1, 2): find(1)==find(2). Redundant edge! components stays 2.
Final components = 2.
Operations needed = components - 1 = 2 - 1 = 1 ✓</pre>

<h2>✅ The solution</h2>
<details><summary>Reveal the commented solution (attempt it first!)</summary>
<pre><code class="language-python">def makeConnected(n: int, connections: list[list[int]]) -> int:
    """
    Computes minimum cable rewirings to connect all computers via DSU.
    """
    if len(connections) < n - 1:
        return -1
        
    parent = list(range(n))
    components = n
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
        
    for u, v in connections:
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv
            components -= 1
            
    return components - 1
</code></pre>
</details>

<h2>⚡ Complexity analysis</h2>
<ul>
<li><strong>Time Complexity:</strong> <code>O(N + E &times; &alpha;(N)) &approx; O(N + E)</code>. Initial check is <code>O(1)</code>, and DSU runs in near-linear time.</li>
<li><strong>Space Complexity:</strong> <code>O(N)</code> for the parent array.</li>
</ul>

<h2>🚨 Edge cases to watch out for</h2>
<ul>
<li><code>len(connections) < n - 1</code>: Returns <code>-1</code> immediately.</li>
<li><code>n = 1</code>: <code>components = 1</code>, returns <code>0</code> (already connected).</li>
</ul>''',

}
