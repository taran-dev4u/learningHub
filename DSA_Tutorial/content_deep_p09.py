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

}
