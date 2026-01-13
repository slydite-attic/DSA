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
#### Time and Space Complexity
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
#### Time and Space Complexity
- **Time Complexity:** O(m * n).
- **Space Complexity:** O(m * n).
- **Note:** This can be space-optimized to O(n) or even O(1) by modifying the input matrix in-place, as the original values at `(i-1,j)`, etc., are no longer needed after `dp[i][j]` is computed.

---

### 2. Maximal Rectangle
`[HARD]` `#dp-on-squares` `#grid-dp` `#histogram` `#stack`

#### Problem Statement
Given a `m x n` binary matrix filled with 0s and 1s, find the largest rectangle containing only 1s and return its area.

#### Implementation Overview
This is a famous problem that is solved by reducing it to a series of "Largest Rectangle in Histogram" problems. The DP aspect is in how we build the histogram for each row.

1.  **DP State (Implicit):** We process the matrix row by row. For each row `i`, we create a `heights` array where `heights[j]` represents the number of consecutive `1`s above `matrix[i][j]` (including the cell itself).
2.  **DP Transition:**
    - `for row in matrix:`
    - `for j in range(n):`
    - `heights[j] = heights[j] + 1 if row[j] == '1' else 0`
3.  **Subproblem:** After computing the `heights` array for a row, it represents a histogram. We then solve the "Largest Rectangle in Histogram" problem for this histogram. This subproblem is typically solved in O(n) using a monotonic stack.
4.  **Combine:** The final answer is the maximum area found across all rows.

#### Python Code Snippet
```python
def maximal_rectangle(matrix: list[list[str]]) -> int:
    if not matrix or not matrix[0]: # Handle empty matrix case.
        return 0

    m, n = len(matrix), len(matrix[0]) # Get matrix dimensions.
    # DP state: heights[j] stores the number of consecutive '1's above the current cell in column j.
    heights = [0] * n
    max_area = 0 # To store the overall maximum area.

    def largest_rectangle_in_histogram(h: list[int]) -> int: # Helper function to solve the histogram problem.
        stack = [-1] # A monotonic stack to keep track of indices of the bars. Sentinel value -1.
        max_h_area = 0 # To store the max area for the current histogram.
        for i, height in enumerate(h): # Iterate through the histogram bars.
            while stack[-1] != -1 and h[stack[-1]] >= height: # While the stack is not empty and the current bar is smaller than the top of the stack.
                h_pop = h[stack.pop()] # Pop the stack.
                w = i - stack[-1] - 1 # Calculate the width of the rectangle.
                max_h_area = max(max_h_area, h_pop * w) # Update the max area.
            stack.append(i) # Push the current bar's index onto the stack.

        while stack[-1] != -1: # Process any remaining bars in the stack.
            h_pop = h[stack.pop()]
            w = len(h) - stack[-1] - 1
            max_h_area = max(max_h_area, h_pop * w)
        return max_h_area

    # Iterate through each row of the matrix.
    for i in range(m):
        # Build the histogram heights for the current row based on the previous row's heights.
        for j in range(n):
            heights[j] = heights[j] + 1 if matrix[i][j] == '1' else 0

        # Calculate the max area for the histogram formed by the current row and update the overall max.
        max_area = max(max_area, largest_rectangle_in_histogram(heights))

    return max_area # Return the final maximum area.
```
#### Time and Space Complexity
- **Time Complexity:** O(m * n). We iterate through each cell once to build the histogram, and the histogram calculation for each row is O(n).
- **Space Complexity:** O(n) to store the `heights` array and the stack for the subproblem.
