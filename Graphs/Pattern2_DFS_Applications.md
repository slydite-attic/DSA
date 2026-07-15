# Pattern 2: Depth-First Search (DFS) Applications

Depth-First Search is a powerful graph traversal algorithm that explores as far as possible along each branch before backtracking. Its recursive nature makes it particularly well-suited for a variety of problems involving connectivity, path-finding, and cycle detection. This pattern covers common problems that are naturally solved using DFS.

---

### 1. Number of Provinces
`[MEDIUM]` `#dfs` `#grid-traversal` `#connectivity`

#### Problem Statement
Given an `n x n` matrix `isConnected` where `isConnected[i][j] = 1` if the `i`th city and the `j`th city are directly connected, return the total number of **provinces**. A province is a group of directly or indirectly connected cities.

*Example:* `isConnected = [[1,1,0],[1,1,0],[0,0,1]]`. **Output:** `2`.

#### Implementation Overview
This is a "Connected Components" problem on a graph represented by an adjacency matrix.
1.  Create a `visited` array of size `n`.
2.  Initialize a `provinces` count to 0.
3.  Iterate through each city `i` from `0` to `n-1`.
4.  If city `i` has not been visited:
    - Increment `provinces` count (we've found a new component).
    - Start a DFS traversal from city `i`. The DFS will explore all connected cities, marking them as visited.
5.  The final `provinces` count is the answer.

#### Python Code Snippet
```python
def find_circle_num(isConnected: list[list[int]]) -> int:
    n = len(isConnected)
    visited = [False] * n
    provinces = 0

    def dfs(city):
        visited[city] = True
        for neighbor in range(n):
            if isConnected[city][neighbor] == 1 and not visited[neighbor]:
                dfs(neighbor)

    for i in range(n):
        if not visited[i]:
            provinces += 1
            dfs(i)

    return provinces
```

#### Complexity Analysis
- **Time Complexity:** $O(V^2)$ where $V$ is the number of cities, because we traverse the $V \times V$ adjacency matrix.
- **Space Complexity:** $O(V)$ for the visited array and recursion stack.

---

### 2. Flood Fill
`[EASY]` `#dfs` `#grid-traversal`

#### Problem Statement
Given an `m x n` grid `image`, a starting pixel `(sr, sc)`, and a `newColor`, "flood fill" the image by changing the color of the starting pixel and all connected pixels of the same original color to the `newColor`.

*Example:* `image = [[1,1,1],[1,1,0],[1,0,1]]`, `sr = 1, sc = 1, newColor = 2`. **Output:** `[[2,2,2],[2,2,0],[2,0,1]]`.

#### Implementation Overview
1.  Store the `startColor` of the pixel `image[sr][sc]`. If `startColor` is already `newColor`, do nothing.
2.  Start a DFS from `(sr, sc)`. The DFS function `dfs(r, c)` will:
    - Check for boundary conditions and if the current pixel has the `startColor`.
    - If valid, change the pixel's color to `newColor` to mark it as visited.
    - Recursively call DFS for its 4-directional neighbors.

#### Python Code Snippet
```python
def flood_fill(image: list[list[int]], sr: int, sc: int, newColor: int) -> list[list[int]]:
    rows, cols = len(image), len(image[0])
    start_color = image[sr][sc]
    if start_color == newColor:
        return image

    def dfs(r, c):
        if not (0 <= r < rows and 0 <= c < cols): return
        if image[r][c] != start_color: return

        image[r][c] = newColor

        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    dfs(sr, sc)
    return image
```

#### Complexity Analysis
- **Time Complexity:** $O(N \times M)$ where $N$ and $M$ are the dimensions of the grid, as we might visit every cell.
- **Space Complexity:** $O(N \times M)$ in the worst case for the recursion stack.

---

### 3. Surrounded Regions (O's and X's)
`[MEDIUM]` `#dfs` `#grid-traversal`

#### Problem Statement
Given an `m x n` matrix `board` containing `'X'` and `'O'`, capture all regions of `'O'`s that are surrounded by `'X'`s. An `'O'` is *not* surrounded if it is on the border or connected to an `'O'` on the border.

*Example:* `board = [["X","X","X","X"],["X","O","O","X"],["X","X","O","X"],["X","O","X","X"]]`. **Output:** `[["X","X","X","X"],["X","X","X","X"],["X","X","X","X"],["X","O","X","X"]]`.

#### Implementation Overview
The trick is to find the `'O'`s that should *not* be captured.
1.  Any `'O'` on the border, and any `'O'` connected to a border `'O'`, cannot be captured.
2.  Iterate through the four borders. If you find an `'O'`, start a DFS from there.
3.  This DFS finds all connected `'O'`s and marks them with a temporary character (e.g., `'E'` for "escaped").
4.  After checking all borders, iterate through the entire grid:
    - If a cell is `'O'`, it's surrounded. Flip it to `'X'`.
    - If a cell is `'E'`, it's un-surrounded. Flip it back to `'O'`.

#### Python Code Snippet
```python
def solve_surrounded_regions(board: list[list[str]]) -> None:
    if not board: return
    rows, cols = len(board), len(board[0])

    def dfs(r, c):
        if not (0 <= r < rows and 0 <= c < cols and board[r][c] == 'O'):
            return
        board[r][c] = 'E' # Mark as escaped
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    # Capture escaped 'O's on the borders
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == 'O' and (r in [0, rows-1] or c in [0, cols-1]):
                dfs(r, c)

    # Flip 'O' to 'X' and 'E' back to 'O'
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == 'O':
                board[r][c] = 'X'
            elif board[r][c] == 'E':
                board[r][c] = 'O'
```

#### Complexity Analysis
- **Time Complexity:** $O(N \times M)$ because we traverse the grid cells and perform DFS which visits each cell at most once.
- **Space Complexity:** $O(N \times M)$ for the recursion stack in the worst case.

---

### 4. Number of Distinct Islands
`[MEDIUM]` `#dfs` `#grid-traversal` `#hash-set`

#### Problem Statement
Given a binary matrix `grid`, return the number of *distinct* islands. Two islands are distinct if their shapes are different, regardless of their position on the grid.

*Example:* `grid = [[1,1,0],[0,1,1],[0,0,0],[1,1,1],[0,1,0]]`. **Output:** `2`.

#### Implementation Overview
We need a canonical representation ("signature") for each island's shape.
1.  Create a `set` to store the signatures of unique islands.
2.  Iterate through the grid. When you find an unvisited `1`:
    - Start a DFS. The DFS will record the path taken relative to the starting cell `(r0, c0)`.
    - `dfs(r, c, path)`: The path is a sequence of moves ('U', 'D', 'L', 'R', 'B' for backtrack).
3.  After an island is traversed, add the resulting path string (the signature) to the set.
4.  The final answer is the size of the set.

#### Python Code Snippet
```python
def number_of_distinct_islands(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    visited = set()
    unique_islands = set()

    def dfs(r, c, r0, c0, path):
        if not (0 <= r < rows and 0 <= c < cols and
                grid[r][c] == 1 and (r, c) not in visited):
            return

        visited.add((r, c))
        path.append((r - r0, c - c0)) # Store relative path

        dfs(r + 1, c, r0, c0, path)
        dfs(r - 1, c, r0, c0, path)
        dfs(r, c + 1, r0, c0, path)
        dfs(r, c - 1, r0, c0, path)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1 and (r, c) not in visited:
                path = []
                dfs(r, c, r, c, path)
                unique_islands.add(frozenset(path))

    return len(unique_islands)
```

#### Complexity Analysis
- **Time Complexity:** $O(N \times M)$ where $N$ and $M$ are the dimensions of the grid. We visit each cell at most once.
- **Space Complexity:** $O(N \times M)$ for the recursion stack, `visited` set, and storing the paths of distinct islands.

---

### 5. Cycle Detection in Undirected Graph (DFS)
`[MEDIUM]` `#dfs` `#cycle-detection`

#### Problem Statement
Given an undirected graph, determine if it contains a cycle.

#### Implementation Overview
For an undirected graph, a cycle exists if a DFS traversal encounters a visited node that is not its immediate parent.
1.  The DFS function takes the current `node` and its `parent`. `dfs(node, parent)`.
2.  Mark `node` as visited.
3.  For each `neighbor` of `node`:
    - If `neighbor` is not visited, recursively call `dfs(neighbor, node)`. If it returns `true`, a cycle was found.
    - If `neighbor` *is* visited, but it is *not* the `parent`, we have found a back edge to an ancestor. This is a cycle. Return `true`.

#### Python Code Snippet
```python
def has_cycle_undirected(n: int, adj: dict) -> bool:
    visited = [False] * n
    for i in range(n):
        if not visited[i]:
            if dfs(i, -1, visited, adj):
                return True
    return False

def dfs(node, parent, visited, adj):
    visited[node] = True
    for neighbor in adj.get(node, []):
        if not visited[neighbor]:
            if dfs(neighbor, node, visited, adj):
                return True
        elif neighbor != parent:
            return True # Cycle detected
    return False
```

#### Complexity Analysis
- **Time Complexity:** $O(V + E)$ where $V$ is vertices and $E$ is edges, as we do a standard DFS.
- **Space Complexity:** $O(V)$ for the visited array and recursion stack.

---

### 6. Bipartite Graph (DFS)
`[MEDIUM]` `#dfs` `#graph-coloring`

#### Problem Statement
Determine if a graph is **bipartite** (can be colored with two colors so that no two adjacent nodes have the same color).

#### Implementation Overview
1.  Create a `color` array, initialized to -1 (no color).
2.  Iterate through all vertices. If a vertex is uncolored, start a DFS.
3.  `dfs(node, c)`:
    - Color `node` with color `c`.
    - For each `neighbor`:
        - If `neighbor` is uncolored, recursively call `dfs(neighbor, 1 - c)`. If this returns `false`, propagate failure.
        - If `neighbor` *is* colored and its color is the *same* as `c`, there is a conflict. Return `false`.

#### Python Code Snippet
```python
def is_bipartite_dfs(n: int, adj: dict) -> bool:
    color = {} # Using a dict as a sparse color array
    for i in range(n):
        if i not in color:
            if not dfs_color(i, 0, color, adj):
                return False
    return True

def dfs_color(node, c, color, adj):
    color[node] = c
    for neighbor in adj.get(node, []):
        if neighbor not in color:
            if not dfs_color(neighbor, 1 - c, color, adj):
                return False
        elif color[neighbor] == c:
            return False
    return True
```

#### Complexity Analysis
- **Time Complexity:** $O(V + E)$ to traverse all nodes and edges.
- **Space Complexity:** $O(V)$ for the recursion stack and the color tracking.

---

### 7. Cycle Detection in Directed Graph (DFS)
`[MEDIUM]` `#dfs` `#cycle-detection`

#### Problem Statement
Given a directed graph, determine if it contains a cycle.

#### Implementation Overview
For a directed graph, we must track nodes in the *current recursion path*.
1.  Use two boolean arrays: `visited` (global) and `path_visited` (for the current recursion stack).
2.  `dfs(node)`:
    - Mark `node` as `visited` and `path_visited` as `true`.
    - For each `neighbor`:
        - If `neighbor` is not `visited`, recursively call `dfs(neighbor)`. If it returns `true`, propagate `true`.
        - If `neighbor` *is* in the `path_visited`, we have found a back edge to a node in the current path. This is a cycle. Return `true`.
3.  Before returning, mark `path_visited` for `node` as `false` (backtracking).

#### Python Code Snippet
```python
def has_cycle_directed(n: int, adj: dict) -> bool:
    visited = [False] * n
    path_visited = [False] * n
    for i in range(n):
        if not visited[i]:
            if dfs_cycle(i, visited, path_visited, adj):
                return True
    return False

def dfs_cycle(node, visited, path_visited, adj):
    visited[node] = True
    path_visited[node] = True

    for neighbor in adj.get(node, []):
        if not visited[neighbor]:
            if dfs_cycle(neighbor, visited, path_visited, adj):
                return True
        elif path_visited[neighbor]:
            return True # Cycle detected

    path_visited[node] = False # Backtrack
    return False
```

#### Complexity Analysis
- **Time Complexity:** $O(V + E)$ to visit each node and its edges.
- **Space Complexity:** $O(V)$ for the recursion stack, `visited`, and `path_visited` arrays.

---

### 8. Connected Components Problem in Matrix (Number of Islands)
`[MEDIUM]` `#dfs` `#connectedcomponents`

#### Problem Statement
Given a 2D grid of '1's (land) and '0's (water), count the number of islands. An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically or diagonally.

#### Implementation Overview
This is a standard connected components problem on a grid. We iterate through every cell in the grid. When we find an unvisited '1', we increment our island count and launch a DFS to visit all adjacent '1's (in all 8 directions, as specified by horizontal, vertical, or diagonal). We mark visited cells by changing them to '0' (or using a visited set) to avoid revisiting.

#### Python Code Snippet
```python
def numIslands(grid: list[list[str]]) -> int:
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    islands = 0

    def dfs(r, c):
        if not (0 <= r < rows and 0 <= c < cols and grid[r][c] == '1'):
            return

        # Mark as visited by mutating the grid
        grid[r][c] = '0'

        # 8 directions
        directions = [
            (0, 1), (0, -1), (1, 0), (-1, 0),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]

        for dr, dc in directions:
            dfs(r + dr, c + dc)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                islands += 1
                dfs(r, c)

    return islands
```

#### Complexity Analysis
- **Time Complexity:** $O(N \times M)$ where $N$ is the number of rows and $M$ is the number of columns. Each cell is visited a constant number of times.
- **Space Complexity:** $O(N \times M)$ in the worst case for the recursion stack (if the entire grid is one island).

---
