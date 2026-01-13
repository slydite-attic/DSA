# Pattern 3: Breadth-First Search (BFS) Applications

Breadth-First Search explores a graph level by level, making it the perfect tool for finding the shortest path in unweighted graphs. It uses a queue to manage a "frontier" of nodes to visit. This pattern covers problems where BFS's level-order traversal is the key to an efficient solution, including multi-source and distance-finding problems.

---

### 1. Rotten Oranges
`[MEDIUM]` `#bfs` `#grid-traversal` `#multi-source-bfs`

#### Problem Statement
You are given an `m x n` grid where each cell can be `0` (empty), `1` (fresh orange), or `2` (rotten orange). Every minute, any fresh orange that is 4-directionally adjacent to a rotten orange becomes rotten. Return the minimum number of minutes that must elapse until no cell has a fresh orange. If this is impossible, return -1.

*Example:* `grid = [[2,1,1],[1,1,0],[0,1,1]]`. **Output:** `4`.

#### Implementation Overview
This is a classic multi-source BFS problem. The "levels" of the BFS correspond to minutes.
1.  Initialize a queue and add the coordinates and initial time `(r, c, 0)` of all rotten oranges.
2.  Count the total number of fresh oranges. If there are none, the answer is 0.
3.  Perform a level-order BFS. For each rotten orange dequeued, explore its 4-directional neighbors.
4.  If a neighbor is a fresh orange (`1`), turn it rotten (`2`), decrement the `fresh_oranges` count, and enqueue it with an incremented time.
5.  Keep track of the time elapsed. The time of the last orange to rot is the answer.
6.  After the BFS, if `fresh_oranges` is still greater than 0, it means some were unreachable. Return -1.

#### Python Code Snippet
```python
from collections import deque
def oranges_rotting(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    q = deque()
    fresh_oranges = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                fresh_oranges += 1
            elif grid[r][c] == 2:
                q.append((r, c, 0)) # (row, col, time)

    if fresh_oranges == 0: return 0

    max_time = 0
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    while q:
        r, c, time = q.popleft()
        max_time = max(max_time, time)

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                grid[nr][nc] = 2
                fresh_oranges -= 1
                q.append((nr, nc, time + 1))

    return max_time if fresh_oranges == 0 else -1
```
#### Time and Space Complexity
- **Time Complexity:** $O(M \times N)$, as each cell is processed at most once.
- **Space Complexity:** $O(M \times N)$ for the queue in the worst case (e.g., all rotten oranges).

---

### 2. 0/1 Matrix (Distance to Nearest 0)
`[MEDIUM]` `#bfs` `#grid-traversal` `#multi-source-bfs`

#### Problem Statement
Given an `m x n` binary matrix `mat`, return a new matrix of the same size where each cell contains the distance of the nearest `0`. The distance between two adjacent cells is 1.

*Example:* `mat = [[0,0,0],[0,1,0],[1,1,1]]`. **Output:** `[[0,0,0],[0,1,0],[1,2,1]]`.

#### Implementation Overview
This is another multi-source BFS. We find the shortest distance from every `0` to all other cells.
1.  Initialize a `distance` matrix, with `0` for `0`-cells and `-1` (or `inf`) for `1`-cells to mark them as unvisited.
2.  Initialize a queue and add the coordinates of all `0`-cells.
3.  Perform a standard multi-source BFS. For each cell `(r,c)` dequeued, explore its neighbors `(nr,nc)`.
4.  If a neighbor is unvisited (`distance[nr][nc] == -1`), update its distance `distance[nr][nc] = distance[r][c] + 1` and enqueue it.

#### Python Code Snippet
```python
from collections import deque
def update_matrix(mat: list[list[int]]) -> list[list[int]]:
    rows, cols = len(mat), len(mat[0])
    dist = [[-1] * cols for _ in range(rows)]
    q = deque()

    for r in range(rows):
        for c in range(cols):
            if mat[r][c] == 0:
                q.append((r, c))
                dist[r][c] = 0

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    while q:
        r, c = q.popleft()
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and dist[nr][nc] == -1:
                dist[nr][nc] = dist[r][c] + 1
                q.append((nr, nc))
    return dist
```
#### Time and Space Complexity
- **Time Complexity:** $O(M \times N)$, as each cell is enqueued and dequeued at most once.
- **Space Complexity:** $O(M \times N)$ for the distance matrix and queue.

---

### 3. Number of Enclaves
`[MEDIUM]` `#bfs` `#grid-traversal`

#### Problem Statement
You are given an `m x n` binary matrix `grid`, where `1` represents a land cell and `0` represents a water cell. An "enclave" is an island of land cells that cannot reach the boundary of the grid. Return the number of land cells in all enclaves.

*Example:* `grid = [[0,0,0,0],[1,0,1,0],[0,1,1,0],[0,0,0,0]]`. **Output:** `3`.

#### Implementation Overview
This is the same logic as "Surrounded Regions". We find all land cells that are *not* part of an enclave.
1.  Find all land cells (`1`s) on the four borders of the grid. Start a multi-source BFS from all of them.
2.  The BFS will visit and effectively mark all land cells that *can* reach the boundary.
3.  After the BFS, iterate through the grid and count the number of remaining `1`s. These are the enclaved cells.

#### Python Code Snippet
```python
from collections import deque
def num_enclaves(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    q = deque()

    # Start BFS from all border land cells
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1 and (r in [0, rows-1] or c in [0, cols-1]):
                q.append((r, c))
                visited[r][c] = True

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    while q:
        r, c = q.popleft()
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and grid[nr][nc] == 1:
                visited[nr][nc] = True
                q.append((nr, nc))

    # Count unvisited land cells
    enclave_count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1 and not visited[r][c]:
                enclave_count += 1

    return enclave_count
```
#### Time and Space Complexity
- **Time Complexity:** $O(M \times N)$.
- **Space Complexity:** $O(M \times N)$ for the visited array and queue.

---

### 4. Cycle Detection in Undirected Graph (BFS)
`[MEDIUM]` `#bfs` `#cycle-detection`

#### Problem Statement
Given an undirected graph, determine if it contains a cycle.

#### Implementation Overview
We can detect a cycle using BFS and tracking parent nodes.
1.  Use a `visited` array. The queue will store pairs: `(node, parent)`.
2.  Start a BFS from an unvisited node, adding `(start_node, -1)` to the queue.
3.  While the queue is not empty:
    - Dequeue `(node, parent)`.
    - For each `neighbor` of `node`:
        - If not visited, mark as visited and enqueue `(neighbor, node)`.
        - If visited, but it is *not* the `parent`, we have found an edge to an already visited node that is not the one we just came from. This forms a cycle. Return `true`.

#### Python Code Snippet
```python
from collections import deque
def has_cycle_undirected_bfs(n: int, adj: dict) -> bool:
    visited = [False] * n
    for i in range(n):
        if not visited[i]:
            q = deque([(i, -1)]) # (node, parent)
            visited[i] = True
            while q:
                node, parent = q.popleft()
                for neighbor in adj.get(node, []):
                    if not visited[neighbor]:
                        visited[neighbor] = True
                        q.append((neighbor, node))
                    elif neighbor != parent:
                        return True # Cycle detected
    return False
```
#### Time and Space Complexity
- **Time Complexity:** $O(V + E)$.
- **Space Complexity:** $O(V)$ for the visited array and queue.

---

### 5. Bipartite Graph (BFS)
`[MEDIUM]` `#bfs` `#graph-coloring`

#### Problem Statement
Determine if a graph is **bipartite** (can be colored with two colors, e.g., 0 and 1, so that no two adjacent nodes have the same color).

*Example:* `graph = [[1,3],[0,2],[1,3],[0,2]]`. **Output:** `true`.

#### Implementation Overview
1.  Create a `color` array, initialized to -1 (no color).
2.  Iterate through all vertices. If a vertex `i` is uncolored:
    - Start a BFS from `i`. Color `color[i] = 0` and add to queue.
    - While the queue is not empty:
        - Dequeue `node`.
        - For each `neighbor`:
            - If `neighbor` is uncolored, color it with the opposite color (`1 - color[node]`) and enqueue it.
            - If `neighbor` *is* colored and has the *same* color as `node`, there's a conflict. Return `false`.

#### Python Code Snippet
```python
from collections import deque
def is_bipartite_bfs(n: int, adj: dict) -> bool:
    color = {} # Using a dict as a sparse color array
    for i in range(n):
        if i not in color:
            q = deque([i])
            color[i] = 0
            while q:
                node = q.popleft()
                for neighbor in adj.get(node, []):
                    if neighbor not in color:
                        color[neighbor] = 1 - color[node]
                        q.append(neighbor)
                    elif color[neighbor] == color[node]:
                        return False
    return True
```
#### Time and Space Complexity
- **Time Complexity:** $O(V + E)$.
- **Space Complexity:** $O(V)$ for the color map and queue.
