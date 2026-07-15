# Pattern 3: DP on Squares

This is a mini-pattern that deals with problems on a 2D grid where the goal is to find or count square or rectangular submatrices with a specific property (e.g., all ones). The DP state `dp[i][j]` typically stores information about a shape ending at cell `(i, j)`.

---

### 1. Count Square Submatrices with All Ones
`[MEDIUM]` `#dp-on-squares` `#grid-dp`

#### Problem Statement
Given a `m x n` matrix of ones and zeros, return how many square submatrices have all ones.

#### Recurrence Relation
Let `dp[i][j]` be the side length of the largest square of all ones whose **bottom-right corner** is at `(i, j)`.
- If `matrix[i][j] == 0`, no square can end here, so `dp[i][j] = 0`.
- If `matrix[i][j] == 1`, the size of the square ending here is limited by the squares ending at its top, left, and top-left neighbors.
- **`dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])`**
- **Counting Insight:** A `dp[i][j]` value of `k` means there is a `k x k` square, a `(k-1) x (k-1)` square, ..., and a `1 x 1` square all ending at this corner. Therefore, the total number of squares is the sum of all values in the `dp` table.

---
#### a) Memoization (Top-Down)
This approach is less intuitive for this problem. We define `solve(i, j)` which computes `dp[i][j]` and adds it to a total.

```python
def count_squares_memo(matrix: list[list[int]]) -> int:
    m, n = len(matrix), len(matrix[0]) # Get matrix dimensions.
    dp = [[-1] * n for _ in range(m)] # Memoization table.

    def solve(r, c): # Function to find the size of the largest square ending at (r, c).
        # Base case: If out of bounds or the cell is 0, no square can end here.
        if r < 0 or c < 0 or matrix[r][c] == 0:
            return 0
        if dp[r][c] != -1: # Return memoized result.
            return dp[r][c]

        # Recursively find the size of squares ending at the top, left, and diagonal neighbors.
        top = solve(r - 1, c)
        left = solve(r, c - 1)
        diag = solve(r - 1, c - 1)

        # The size of the square ending at (r, c) is 1 + the minimum of its neighbors.
        dp[r][c] = 1 + min(top, left, diag)
        return dp[r][c]

    total_squares = 0 # Initialize total count.
    for i in range(m): # Iterate through each cell.
        for j in range(n):
            # The value returned by solve(i, j) is the number of squares with (i, j) as the bottom-right corner.
            total_squares += solve(i, j)

    return total_squares # Return the accumulated total.
```
- **Time Complexity:** O(m * n). Each state `dp[i][j]` is computed once.
- **Space Complexity:** O(m * n) for DP table + O(m+n) for recursion stack.

---
#### b) Tabulation (Bottom-Up)
This is the most natural approach. We build the `dp` table and sum its values.

```python
def count_squares_tab(matrix: list[list[int]]) -> int:
    m, n = len(matrix), len(matrix[0]) # Get matrix dimensions.
    dp = [[0] * n for _ in range(m)] # DP table to store the size of the largest square ending at (i, j).
    total_squares = 0 # Initialize the total count of squares.

    for i in range(m): # Iterate through each row.
        for j in range(n): # Iterate through each column.
            if matrix[i][j] == 1: # If the current cell is 1,
                if i == 0 or j == 0: # For the first row or column, the largest square is of size 1.
                    dp[i][j] = 1
                else: # For other cells,
                    # The size of the square is 1 + the minimum of its top, left, and diagonal neighbors.
                    dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
                # A dp value of k means a kxk square, a (k-1)x(k-1) square, etc., all end here.
                total_squares += dp[i][j]

    return total_squares # Return the final count.
```
- **Time Complexity:** O(m * n).
- **Space Complexity:** O(m * n).

---
#### c) Space Optimization (O(n) Space)
Since computing `dp[i][j]` only requires values from the current and the previous row, we can optimize the space to O(n) using a single 1D array of size `n` representing the previous row.

```python
def count_squares_optimized(matrix: list[list[int]]) -> int:
    m, n = len(matrix), len(matrix[0])
    prev_row = [0] * n
    total_squares = 0

    for i in range(m):
        curr_row = [0] * n
        for j in range(n):
            if matrix[i][j] == 1:
                if i == 0 or j == 0:
                    curr_row[j] = 1
                else:
                    curr_row[j] = 1 + min(prev_row[j], curr_row[j-1], prev_row[j-1])
                total_squares += curr_row[j]
        prev_row = curr_row

    return total_squares
```
- **Time Complexity:** O(m * n).
- **Space Complexity:** O(n) to store one row.

---

### 2. Maximal Rectangle
`[HARD]` `#dp-on-squares` `#grid-dp` `#histogram` `#stack`

#### Problem Statement
Given a `m x n` binary matrix filled with 0s and 1s, find the largest rectangle containing only 1s and return its area.

#### Implementation Overview
This problem reduces to solving the "Largest Rectangle in Histogram" problem for each row. The heights of the histogram columns are determined by the consecutive number of `1`s ending at the current row.

---
#### a) Memoization (Top-Down heights + Histogram solver)
We use a top-down function to recursively calculate the height of consecutive `1`s at any given cell.
```python
def maximal_rectangle_memo(matrix: list[list[str]]) -> int:
    if not matrix or not matrix[0]: return 0
    m, n = len(matrix), len(matrix[0])
    dp = [[-1] * n for _ in range(m)]

    def get_height(r, c):
        if r < 0: return 0
        if matrix[r][c] == '0': return 0
        if dp[r][c] != -1: return dp[r][c]
        dp[r][c] = 1 + get_height(r - 1, c)
        return dp[r][c]

    def largest_rectangle_in_histogram(h: list[int]) -> int:
        stack = [-1]
        max_area = 0
        for i, height in enumerate(h):
            while stack[-1] != -1 and h[stack[-1]] >= height:
                h_pop = h[stack.pop()]
                w = i - stack[-1] - 1
                max_area = max(max_area, h_pop * w)
            stack.append(i)
        while stack[-1] != -1:
            h_pop = h[stack.pop()]
            w = len(h) - stack[-1] - 1
            max_area = max(max_area, h_pop * w)
        return max_area

    max_rect = 0
    for i in range(m):
        h = [get_height(i, j) for j in range(n)]
        max_rect = max(max_rect, largest_rectangle_in_histogram(h))
    return max_rect
```
- **Time Complexity:** O(m * n).
- **Space Complexity:** O(m * n) to cache the heights + O(m) recursion stack.

---
#### b) Tabulation (Bottom-Up 2D Table + Histogram solver)
We precompute a 2D table representing heights of consecutive `1`s at each cell bottom-up.
```python
def maximal_rectangle_tab(matrix: list[list[str]]) -> int:
    if not matrix or not matrix[0]: return 0
    m, n = len(matrix), len(matrix[0])
    
    # 2D DP Table to store consecutive 1s heights
    dp = [[0] * n for _ in range(m)]
    for j in range(n):
        dp[0][j] = 1 if matrix[0][j] == '1' else 0
    for i in range(1, m):
        for j in range(n):
            dp[i][j] = dp[i-1][j] + 1 if matrix[i][j] == '1' else 0

    def largest_rectangle_in_histogram(h: list[int]) -> int:
        stack = [-1]
        max_area = 0
        for i, height in enumerate(h):
            while stack[-1] != -1 and h[stack[-1]] >= height:
                h_pop = h[stack.pop()]
                w = i - stack[-1] - 1
                max_area = max(max_area, h_pop * w)
            stack.append(i)
        while stack[-1] != -1:
            h_pop = h[stack.pop()]
            w = len(h) - stack[-1] - 1
            max_area = max(max_area, h_pop * w)
        return max_area

    max_rect = 0
    for i in range(m):
        max_rect = max(max_rect, largest_rectangle_in_histogram(dp[i]))
    return max_rect
```
- **Time Complexity:** O(m * n).
- **Space Complexity:** O(m * n) to store the 2D heights table.

---
#### c) Space Optimization (1D Array + Histogram solver)
Since computing heights for row `i` only requires the heights of row `i-1`, we can optimize space to a single 1D array of size `n` representing the running column heights.
```python
def maximal_rectangle_optimized(matrix: list[list[str]]) -> int:
    if not matrix or not matrix[0]: return 0
    m, n = len(matrix), len(matrix[0])
    heights = [0] * n
    max_area = 0

    def largest_rectangle_in_histogram(h: list[int]) -> int:
        stack = [-1]
        max_h_area = 0
        for i, height in enumerate(h):
            while stack[-1] != -1 and h[stack[-1]] >= height:
                h_pop = h[stack.pop()]
                w = i - stack[-1] - 1
                max_h_area = max(max_h_area, h_pop * w)
            stack.append(i)
        while stack[-1] != -1:
            h_pop = h[stack.pop()]
            w = len(h) - stack[-1] - 1
            max_h_area = max(max_h_area, h_pop * w)
        return max_h_area

    for i in range(m):
        for j in range(n):
            heights[j] = heights[j] + 1 if matrix[i][j] == '1' else 0
        max_area = max(max_area, largest_rectangle_in_histogram(heights))

    return max_area
```
- **Time Complexity:** O(m * n).
- **Space Complexity:** O(n) to store the 1D heights array.
