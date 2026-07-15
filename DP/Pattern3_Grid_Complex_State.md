# Pattern 3: DP on Grids - Complex State & Choices

This pattern covers more advanced grid-based DP problems. The complexity arises from variations in movement (e.g., falling paths), state representation (e.g., needing to know the previous action), or having multiple interacting paths (e.g., two robots).

---

### 1. Ninja's Training
`[MEDIUM]` `#grid-dp` `#complex-state`

#### Problem Statement
A ninja trains for `N` days. Each day, he can choose one of three activities, earning points for it. He cannot perform the same activity on two consecutive days. Given the points for each activity on each day, find the maximum merit points he can earn.

#### Recurrence Relation
The state must include the day and the last activity performed.
- **`dp[day][last_activity]`**: Max points earned up to `day`, having done `last_activity` on `day`.
- **`dp[day][act] = points[day][act] + max(dp[day-1][other_act])`** for all `other_act != act`.
- The final answer is the max of `dp[N-1][0]`, `dp[N-1][1]`, and `dp[N-1][2]`.

---
#### a) Memoization (Top-Down)
```python
def ninja_training_memo(n: int, points: list[list[int]]) -> int:
    dp = [[-1] * 4 for _ in range(n)] # Using 4 for last_activity to avoid -1 issues

    def solve(day, last_activity):
        if day == 0:
            max_pts = 0
            for i in range(3):
                if i != last_activity:
                    max_pts = max(max_pts, points[0][i])
            return max_pts

        if dp[day][last_activity] != -1:
            return dp[day][last_activity]

        max_pts = 0
        for i in range(3):
            if i != last_activity:
                current_pts = points[day][i] + solve(day - 1, i)
                max_pts = max(max_pts, current_pts)

        dp[day][last_activity] = max_pts
        return max_pts

    return solve(n - 1, 3) # Start with a dummy last activity
```
- **Time Complexity:** O(N * 4 * 3) ~ O(N). Each state `dp[day][last_activity]` is computed once.
- **Space Complexity:** O(N * 4) for the DP table + O(N) for recursion stack.

---
#### b) Tabulation (Bottom-Up)
```python
def ninja_training_tab(n: int, points: list[list[int]]) -> int:
    dp = [[0] * 4 for _ in range(n)]

    # Base cases for day 0
    dp[0][0] = max(points[0][1], points[0][2])
    dp[0][1] = max(points[0][0], points[0][2])
    dp[0][2] = max(points[0][0], points[0][1])
    dp[0][3] = max(points[0][0], points[0][1], points[0][2])

    for day in range(1, n):
        for last_activity in range(4):
            max_pts = 0
            for task in range(3):
                if task != last_activity:
                    max_pts = max(max_pts, points[day][task] + dp[day-1][task])
            dp[day][last_activity] = max_pts

    return dp[n-1][3]
```
- **Time Complexity:** O(N * 4 * 3) ~ O(N).
- **Space Complexity:** O(N * 4) for the DP table.

---
#### c) Space Optimization
```python
def ninja_training_optimized(n: int, points: list[list[int]]) -> int:
    prev_day = [0] * 4
    prev_day[0] = max(points[0][1], points[0][2])
    prev_day[1] = max(points[0][0], points[0][2])
    prev_day[2] = max(points[0][0], points[0][1])
    prev_day[3] = max(points[0][0], points[0][1], points[0][2])

    for day in range(1, n):
        current_day = [0] * 4
        for last_activity in range(4):
            max_pts = 0
            for task in range(3):
                if task != last_activity:
                    max_pts = max(max_pts, points[day][task] + prev_day[task])
            current_day[last_activity] = max_pts
        prev_day = current_day

    return prev_day[3]
```
- **Time Complexity:** O(N).
- **Space Complexity:** O(1), as the `dp` array size is constant (4).

---

### 2. Minimum/Maximum Falling Path Sum
`[MEDIUM]` `#grid-dp` `#flexible-path`

#### Problem Statement
Given a square grid, find the minimum sum of a "falling path". A path starts at any element in the first row and moves to an adjacent cell in the row below (i.e., from `(r, c)` to `(r+1, c-1)`, `(r+1, c)`, or `(r+1, c+1)`).

#### Recurrence Relation
Let `dp[i][j]` be the minimum path sum ending at `(i, j)`.
- **`dp[i][j] = grid[i][j] + min(dp[i-1][j-1], dp[i-1][j], dp[i-1][j+1])`**
- **Base Cases:** The first row `dp[0]` is the same as `grid[0]`.
- **Final Answer:** The minimum value in the last row `dp[n-1]`.

---
#### a) Memoization (Top-Down)
```python
def min_falling_path_memo(matrix: list[list[int]]) -> int:
    n = len(matrix)
    dp = [[-1] * n for _ in range(n)]

    def solve(r, c):
        if c < 0 or c >= n:
            return float('inf')
        if r == 0:
            return matrix[0][c]
        if dp[r][c] != -1:
            return dp[r][c]

        up = solve(r - 1, c)
        up_left = solve(r - 1, c - 1)
        up_right = solve(r - 1, c + 1)

        dp[r][c] = matrix[r][c] + min(up, up_left, up_right)
        return dp[r][c]

    min_sum = float('inf')
    for j in range(n):
        min_sum = min(min_sum, solve(n - 1, j))
    return min_sum
```
- **Time Complexity:** O(n*n).
- **Space Complexity:** O(n*n) for DP table + O(n) for recursion stack.

#### b) Tabulation (Bottom-Up)
```python
def min_falling_path_tab(matrix: list[list[int]]) -> int:
    n = len(matrix)
    dp = [[0] * n for _ in range(n)]
    
    # Base case: first row
    for j in range(n):
        dp[0][j] = matrix[0][j]
        
    for i in range(1, n):
        for j in range(n):
            up = dp[i-1][j]
            up_left = dp[i-1][j-1] if j > 0 else float('inf')
            up_right = dp[i-1][j+1] if j < n - 1 else float('inf')
            dp[i][j] = matrix[i][j] + min(up, up_left, up_right)
            
    return min(dp[n-1])
```
- **Time Complexity:** O(n*n).
- **Space Complexity:** O(n*n).

---
#### c) Space Optimization
```python
def min_falling_path_optimized(matrix: list[list[int]]) -> int:
    n = len(matrix)
    prev_row = list(matrix[0])

    for i in range(1, n):
        current_row = [0] * n
        for j in range(n):
            up = prev_row[j]
            up_left = prev_row[j-1] if j > 0 else float('inf')
            up_right = prev_row[j+1] if j < n - 1 else float('inf')
            current_row[j] = matrix[i][j] + min(up, up_left, up_right)
        prev_row = current_row

    return min(prev_row)
```
- **Time Complexity:** O(n*n).
- **Space Complexity:** O(n).

---

### 3. Cherry Pickup II (3D DP)
`[HARD]` `#3d-dp` `#grid-dp` `#dual-path`

#### Problem Statement
Two robots, starting at `(0, 0)` and `(0, cols-1)`, move down to the last row. Find the maximum cherries they can collect together.

#### Recurrence Relation
Since both robots are always on the same row `i`, the state only needs to track their columns `j1` and `j2`.
- **`dp[i][j1][j2]`**: Max cherries collected up to row `i`, with robots at `(i, j1)` and `(i, j2)`.
- To find `dp[i][j1][j2]`, we look at the max value from all 9 possible previous states in row `i-1` and add the cherries at the current cells.

---
#### a) Memoization (Top-Down)
```python
def cherry_pickup_memo(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    dp = [[[-1] * cols for _ in range(cols)] for _ in range(rows)]

    def solve(r, c1, c2):
        if c1 < 0 or c1 >= cols or c2 < 0 or c2 >= cols:
            return float('-inf')
        if r == rows - 1:
            return grid[r][c1] if c1 == c2 else grid[r][c1] + grid[r][c2]
        if dp[r][c1][c2] != -1:
            return dp[r][c1][c2]

        max_future = 0
        for dc1 in [-1, 0, 1]:
            for dc2 in [-1, 0, 1]:
                max_future = max(max_future, solve(r + 1, c1 + dc1, c2 + dc2))

        cherries = grid[r][c1]
        if c1 != c2:
            cherries += grid[r][c2]

        dp[r][c1][c2] = cherries + max_future
        return dp[r][c1][c2]

    return solve(0, 0, cols - 1)
```
- **Time Complexity:** O(rows * cols * cols * 9) ~ O(R * C^2).
- **Space Complexity:** O(R * C^2) for DP table + O(R) for recursion stack.

---
#### b) Tabulation (Bottom-Up)
```python
def cherry_pickup_tab(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    dp = [[[0] * cols for _ in range(cols)] for _ in range(rows)]
    
    # Base case: last row
    for j1 in range(cols):
        for j2 in range(cols):
            dp[rows-1][j1][j2] = grid[rows-1][j1] if j1 == j2 else grid[rows-1][j1] + grid[rows-1][j2]
            
    # Iterate from second-to-last row up to the top
    for i in range(rows - 2, -1, -1):
        for j1 in range(cols):
            for j2 in range(cols):
                max_future = 0
                for dc1 in [-1, 0, 1]:
                    for dc2 in [-1, 0, 1]:
                        nj1, nj2 = j1 + dc1, j2 + dc2
                        if 0 <= nj1 < cols and 0 <= nj2 < cols:
                            max_future = max(max_future, dp[i+1][nj1][nj2])
                            
                cherries = grid[i][j1] + (grid[i][j2] if j1 != j2 else 0)
                dp[i][j1][j2] = cherries + max_future
                
    return dp[0][0][cols-1]
```
- **Time Complexity:** O(R * C^2).
- **Space Complexity:** O(R * C^2).

---
#### c) Space Optimization
```python
def cherry_pickup_optimized(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    front = [[0] * cols for _ in range(cols)]

    # Base case: last row
    for j1 in range(cols):
        for j2 in range(cols):
            front[j1][j2] = grid[rows-1][j1] if j1 == j2 else grid[rows-1][j1] + grid[rows-1][j2]

    # Iterate from second-to-last row up to the top
    for i in range(rows - 2, -1, -1):
        curr = [[0] * cols for _ in range(cols)]
        for j1 in range(cols):
            for j2 in range(cols):
                max_future = 0
                for dc1 in [-1, 0, 1]:
                    for dc2 in [-1, 0, 1]:
                        nj1, nj2 = j1 + dc1, j2 + dc2
                        if 0 <= nj1 < cols and 0 <= nj2 < cols:
                            max_future = max(max_future, front[nj1][nj2])

                cherries = grid[i][j1] + (grid[i][j2] if j1 != j2 else 0)
                curr[j1][j2] = cherries + max_future
        front = curr

    return front[0][cols-1]
```
- **Time Complexity:** O(R * C^2).
- **Space Complexity:** O(C^2) for the two DP tables.
