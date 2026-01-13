# Pattern 2: DP on Grids - Pathfinding

This pattern covers fundamental Dynamic Programming problems on 2D grids. The core idea is to treat the grid itself as the DP table (or use a separate one of the same dimensions). Each cell `dp[i][j]` stores the solution to a subproblem ending at that cell, typically by combining solutions from adjacent cells.

---

### 1. Grid Unique Paths
`[MEDIUM]` `#grid-dp` `#pathfinding`

#### Problem Statement
You are on a `m x n` grid, starting at `(0, 0)` and want to reach `(m-1, n-1)`. You can only move either down or right. Find the total number of unique paths.

#### Recurrence Relation
Let `dp[i][j]` be the number of unique paths to reach cell `(i, j)`. To reach `(i, j)`, you must have come from `(i-1, j)` (above) or `(i, j-1)` (left).
- **`dp[i][j] = dp[i-1][j] + dp[i][j-1]`**
- **Base Case:** `dp[0][0] = 1`. Any cell in the first row or first column can only be reached in one way.

---
#### a) Memoization (Top-Down)
```python
def unique_paths_memo(m: int, n: int) -> int:
    dp = [[-1] * n for _ in range(m)]

    def solve(r, c):
        if r == 0 and c == 0:
            return 1
        if r < 0 or c < 0:
            return 0
        if dp[r][c] != -1:
            return dp[r][c]

        up = solve(r - 1, c)
        left = solve(r, c - 1)
        dp[r][c] = up + left
        return dp[r][c]

    return solve(m - 1, n - 1)
```
#### Time and Space Complexity
- **Time Complexity:** O(m * n). Each state `(r, c)` is computed once.
- **Space Complexity:** O(m * n) for the `dp` table + O(m+n) for recursion stack depth.

---
#### b) Tabulation (Bottom-Up)
```python
def unique_paths_tab(m: int, n: int) -> int:
    dp = [[0] * n for _ in range(m)]
    dp[0][0] = 1

    for r in range(m):
        for c in range(n):
            if r == 0 and c == 0: continue
            up = dp[r-1][c] if r > 0 else 0
            left = dp[r][c-1] if c > 0 else 0
            dp[r][c] = up + left

    return dp[m-1][n-1]
```
#### Time and Space Complexity
- **Time Complexity:** O(m * n) for the nested loops.
- **Space Complexity:** O(m * n) for the DP table.

---
#### c) Space Optimization
We only need the previous row to compute the current row.

```python
def unique_paths_optimized(m: int, n: int) -> int:
    prev_row = [0] * n

    for r in range(m):
        current_row = [0] * n
        for c in range(n):
            if r == 0 and c == 0:
                current_row[c] = 1
                continue
            up = prev_row[c]
            left = current_row[c-1] if c > 0 else 0
            current_row[c] = up + left
        prev_row = current_row

    return prev_row[n-1]
```
#### Time and Space Complexity
- **Time Complexity:** O(m * n).
- **Space Complexity:** O(n) for storing one row.
*Note: This problem also has a more efficient O(min(m,n)) time combinatorial solution: `(m+n-2) choose (m-1)`.*

---

### 2. Grid Unique Paths II (With Obstacles)
`[MEDIUM]` `#grid-dp` `#pathfinding` `#obstacles`

#### Problem Statement
A follow-up to the above, the grid now contains obstacles (marked as `1`) that cannot be passed through.

#### Recurrence Relation
- If `grid[i][j] == 1` (obstacle), `dp[i][j] = 0`.
- Otherwise, `dp[i][j] = dp[i-1][j] + dp[i][j-1]`.

---
#### a) Memoization (Top-Down)
```python
def unique_paths_obstacles_memo(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    dp = [[-1] * n for _ in range(m)]

    def solve(r, c):
        if r < 0 or c < 0 or grid[r][c] == 1:
            return 0
        if r == 0 and c == 0:
            return 1
        if dp[r][c] != -1:
            return dp[r][c]

        up = solve(r - 1, c)
        left = solve(r, c - 1)
        dp[r][c] = up + left
        return dp[r][c]

    return solve(m - 1, n - 1)
```
#### Time and Space Complexity
- **Time Complexity:** O(m * n).
- **Space Complexity:** O(m * n) for the `dp` table + O(m+n) for recursion stack depth.

---
#### b) Space Optimization
```python
def unique_paths_obstacles_optimized(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    if grid[0][0] == 1: return 0

    prev_row = [0] * n
    for r in range(m):
        current_row = [0] * n
        for c in range(n):
            if grid[r][c] == 1:
                current_row[c] = 0
                continue
            if r == 0 and c == 0:
                current_row[c] = 1
                continue

            up = prev_row[c] if r > 0 else 0
            left = current_row[c-1] if c > 0 else 0
            current_row[c] = up + left
        prev_row = current_row

    return prev_row[n-1]
```
#### Time and Space Complexity
- **Time Complexity:** O(m * n).
- **Space Complexity:** O(n).

---

### 3. Minimum Path Sum in Grid
`[MEDIUM]` `#grid-dp` `#pathfinding` `#min-cost`

#### Problem Statement
Given a grid of non-negative numbers, find a path from top-left to bottom-right which minimizes the sum of all numbers along its path. You can only move down or right.

#### Recurrence Relation
Let `dp[i][j]` be the minimum path sum to reach cell `(i, j)`.
- **`dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])`**

---
#### a) Memoization (Top-Down)
```python
def min_path_sum_memo(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    dp = [[-1] * n for _ in range(m)]

    def solve(r, c):
        if r < 0 or c < 0:
            return float('inf')
        if r == 0 and c == 0:
            return grid[0][0]
        if dp[r][c] != -1:
            return dp[r][c]

        up = solve(r - 1, c)
        left = solve(r, c - 1)
        dp[r][c] = grid[r][c] + min(up, left)
        return dp[r][c]

    return solve(m - 1, n - 1)
```
#### Time and Space Complexity
- **Time Complexity:** O(m * n).
- **Space Complexity:** O(m * n) for the `dp` table + O(m+n) for recursion stack depth.

---
#### b) Space Optimization
```python
def min_path_sum_optimized(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    prev_row = [float('inf')] * n

    for r in range(m):
        current_row = [float('inf')] * n
        for c in range(n):
            if r == 0 and c == 0:
                current_row[c] = grid[r][c]
            else:
                up = prev_row[c]
                left = current_row[c-1]
                current_row[c] = grid[r][c] + min(up, left)
        prev_row = current_row

    return prev_row[n-1]
```
#### Time and Space Complexity
- **Time Complexity:** O(m * n).
- **Space Complexity:** O(n).

---

### 4. Minimum Path Sum in Triangular Grid
`[MEDIUM]` `#grid-dp` `#pathfinding` `#triangle`

#### Problem Statement
Given a triangle array, find the minimum path sum from top to bottom. From index `j` on row `i`, you can move to index `j` or `j+1` on row `i+1`.

#### Recurrence Relation
Let `dp[i][j]` be the min path sum starting from cell `(i, j)` to the bottom. Working bottom-up is most intuitive.
- **`dp[i][j] = grid[i][j] + min(dp[i+1][j], dp[i+1][j+1])`**
- **Base Cases:** The last row of `dp` is the last row of the triangle.

---
#### a) Tabulation (Bottom-Up, Space Optimized)
We only need the "next" row to compute the "current" row. We can use a 1D `dp` array and iterate upwards from the bottom.

```python
def minimum_total_triangle(triangle: list[list[int]]) -> int:
    n = len(triangle)
    # dp array initialized with the last row
    next_row = list(triangle[n-1])

    # Iterate from the second-to-last row up to the top
    for r in range(n - 2, -1, -1):
        current_row = [0] * (r + 1)
        for c in range(r + 1):
            down = next_row[c]
            diagonal = next_row[c+1]
            current_row[c] = triangle[r][c] + min(down, diagonal)
        next_row = current_row

    return next_row[0]
```
#### Time and Space Complexity
- **Time Complexity:** O(n^2), where n is the number of rows.
- **Space Complexity:** O(n) for storing one row.
