# Pattern 5: Matrix Manipulations

This pattern focuses on problems involving 2D arrays, or matrices. These problems often require specialized traversal strategies (like spiral traversal) or clever in-place modification techniques to meet space complexity constraints. The core data structure is a list of lists, and the logic involves manipulating row and column indices.

---

### 25. Set Matrix Zeros
`[MEDIUM]` `#matrix` `#inplace-manipulation`

#### Problem Statement
Given an `m x n` integer matrix, if an element is 0, set its entire row and column to 0s. You must do this in-place.

*Example:*
- **Input:** `matrix = [[1,1,1],[1,0,1],[1,1,1]]`
- **Output:** `[[1,0,1],[0,0,0],[1,0,1]]`

#### Implementation Overview
A naive solution using an auxiliary matrix would take O(M*N) space. A better solution using two auxiliary arrays for rows and columns takes O(M+N) space. The optimal O(1) space solution uses the first row and first column of the matrix itself as markers.

1.  **Check the first row/col:** First, determine if the original first row or first column contains a zero. Store this information in two boolean variables, e.g., `first_row_has_zero` and `first_col_has_zero`.
2.  **Mark the first row/col:** Iterate through the *rest* of the matrix (from `matrix[1][1]`). If you find `matrix[i][j] == 0`, use the first row and column as markers by setting `matrix[i][0] = 0` and `matrix[0][j] = 0`.
3.  **Set zeros based on markers:** Iterate through the rest of the matrix again (from `matrix[1][1]`). If the marker for that row or column is set (i.e., `matrix[i][0] == 0` or `matrix[0][j] == 0`), then set `matrix[i][j] = 0`.
4.  **Set the first row/col:** Finally, use the boolean flags from step 1 to determine whether the first row and first column themselves need to be entirely zeroed out.

#### Time and Space Complexity
- **Time Complexity:** $O(M \cdot N)$, where $M$ is the number of rows and $N$ is the number of columns. We traverse the matrix twice.
- **Space Complexity:** $O(1)$, as we use the matrix itself for storage and a constant amount of extra space.

#### Python Code Snippet
```python
def set_matrix_zeros(matrix):
    if not matrix:
        return
    m, n = len(matrix), len(matrix[0])
    first_row_has_zero = any(matrix[0][j] == 0 for j in range(n))
    first_col_has_zero = any(matrix[i][0] == 0 for i in range(m))

    # Use first row/col as markers for the rest of the matrix
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][j] == 0:
                matrix[i][0] = 0
                matrix[0][j] = 0

    # Set zeros for the rest of the matrix based on markers
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][0] == 0 or matrix[0][j] == 0:
                matrix[i][j] = 0

    # Set zeros for the first row and col if needed
    if first_row_has_zero:
        for j in range(n):
            matrix[0][j] = 0

    if first_col_has_zero:
        for i in range(m):
            matrix[i][0] = 0
```

#### Tricks/Gotchas
- **O(1) Space Constraint:** The main challenge is achieving O(1) extra space. Using the matrix's own first row/column is the key trick.
- **Order of Operations:** You must process the first row/column's status *before* using them as markers, otherwise you lose information when you start overwriting them.

#### Related Problems
- None in this list.

---

### 26. Rotate Matrix by 90 degrees
`[MEDIUM]` `#matrix` `#inplace-manipulation`

#### Problem Statement
You are given an `n x n` 2D matrix representing an image. Rotate the image by 90 degrees clockwise. You have to rotate the image in-place.

*Example:*
- **Input:** `matrix = [[1,2,3],[4,5,6],[7,8,9]]`
- **Output:** `[[7,4,1],[8,5,2],[9,6,3]]`

#### Implementation Overview
The most intuitive in-place solution involves a two-step process:
1.  **Transpose the matrix:** A transpose operation flips a matrix over its main diagonal. This is achieved by swapping `matrix[i][j]` with `matrix[j][i]`. You only need to iterate through the upper triangle of the matrix (where `j > i`) to do this.
    - After transpose: `[[1,4,7],[2,5,8],[3,6,9]]`
2.  **Reverse each row:** After transposing, iterate through each row of the matrix and reverse it.
    - Reversing the first row `[1,4,7]` gives `[7,4,1]`.
    - This yields the final rotated matrix.

#### Time and Space Complexity
- **Time Complexity:** $O(N^2)$, where $N$ is the dimension of the matrix. We iterate through the matrix roughly twice (once for transpose, once for row reversal).
- **Space Complexity:** $O(1)$, as the rotation is performed in-place.

#### Python Code Snippet
```python
def rotate_matrix(matrix):
    n = len(matrix)

    # Step 1: Transpose the matrix
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

    # Step 2: Reverse each row
    for i in range(n):
        matrix[i].reverse()
```

#### Tricks/Gotchas
- **Clockwise vs. Counter-Clockwise:**
    - **Clockwise (current solution):** Transpose, then reverse each row.
    - **Counter-Clockwise:** Reverse each row, then transpose. Or, transpose then reverse each column.
- **In-place:** The solution modifies the matrix directly without creating a new one.

#### Related Problems
- None in this list.

---

### 27. Print the matrix in spiral manner
`[MEDIUM]` `#matrix` `#traversal` `#simulation`

#### Problem Statement
Given an `m x n` matrix, return all elements of the matrix in spiral order.

*Example:*
- **Input:** `matrix = [[1,2,3],[4,5,6],[7,8,9]]`
- **Output:** `[1,2,3,6,9,8,7,4,5]`

#### Implementation Overview
This problem is a simulation of a spiral path. We can solve it by keeping track of the boundaries of the layer we are currently printing.
1.  Initialize four boundary pointers: `top = 0`, `bottom = m-1`, `left = 0`, `right = n-1`.
2.  Initialize an empty list `result` to store the output.
3.  Loop as long as the boundaries haven't crossed (`top <= bottom` and `left <= right`).
4.  **Traverse Right:** Print the top row from `left` to `right`. After this, the top boundary moves down: `top += 1`.
5.  **Traverse Down:** Print the rightmost column from `top` to `bottom`. The right boundary moves in: `right -= 1`.
6.  **Traverse Left:** Before traversing, check if `top <= bottom`. If so, print the bottom row from `right` to `left` (backwards). The bottom boundary moves up: `bottom -= 1`.
7.  **Traverse Up:** Before traversing, check if `left <= right`. If so, print the leftmost column from `bottom` to `top` (backwards). The left boundary moves out: `left += 1`.
8.  Repeat until the loop condition is false.

#### Time and Space Complexity
- **Time Complexity:** $O(M \cdot N)$, where $M$ is the number of rows and $N$ is the number of columns. We visit each element exactly once.
- **Space Complexity:** $O(1)$ (or $O(M \cdot N)$ if the output list is considered extra space).

#### Python Code Snippet
```python
def spiral_order(matrix):
    if not matrix:
        return []

    m, n = len(matrix), len(matrix[0])
    top, bottom, left, right = 0, m - 1, 0, n - 1
    result = []

    while top <= bottom and left <= right:
        # Traverse Right
        for j in range(left, right + 1):
            result.append(matrix[top][j])
        top += 1

        # Traverse Down
        for i in range(top, bottom + 1):
            result.append(matrix[i][right])
        right -= 1

        # Traverse Left (check boundaries to handle non-square matrices)
        if top <= bottom:
            for j in range(right, left - 1, -1):
                result.append(matrix[bottom][j])
            bottom -= 1

        # Traverse Up (check boundaries to handle non-square matrices)
        if left <= right:
            for i in range(bottom, top - 1, -1):
                result.append(matrix[i][left])
            left += 1

    return result
```

#### Tricks/Gotchas
- **Boundary Checks:** The checks `if top <= bottom` and `if left <= right` before the last two traversals are crucial for non-square matrices (e.g., a single row or column) to prevent duplicate printing.

#### Related Problems
- Spiral Matrix II

---

### 29. Pascal's Triangle
`[EASY]` `#matrix` `#dp` `#simulation`

#### Problem Statement
Given an integer `numRows`, generate the first `numRows` of Pascal's Triangle. In Pascal's triangle, each number is the sum of the two numbers directly above it.

*Example:*
- **Input:** `numRows = 5`
- **Output:** `[[1],[1,1],[1,2,1],[1,3,3,1],[1,4,6,4,1]]`

#### Implementation Overview
This is a generative, simulation-style problem. We can build the triangle row by row.
1.  If `numRows` is 0, return an empty list.
2.  Initialize the result with the first row: `triangle = [[1]]`.
3.  Loop from `i = 1` up to `numRows - 1` to generate the remaining rows.
4.  In each iteration, get the `previous_row` from `triangle[-1]`.
5.  Create a `new_row` that starts with `1`.
6.  Calculate the middle elements of the `new_row`. Each element `new_row[j]` is the sum of `previous_row[j-1]` and `previous_row[j]`.
7.  Append a `1` to the end of the `new_row`.
8.  Append the completed `new_row` to the `triangle`.
9.  Return the `triangle`.

#### Time and Space Complexity
- **Time Complexity:** $O(N^2)$, where $N$ is the number of rows. We generate roughly $N^2/2$ elements.
- **Space Complexity:** $O(N^2)$ to store the entire triangle.

#### Python Code Snippet
```python
def generate_pascal_triangle(numRows):
    if numRows == 0:
        return []

    triangle = [[1]]

    for i in range(1, numRows):
        prev_row = triangle[-1]
        new_row = [1]

        for j in range(len(prev_row) - 1):
            new_row.append(prev_row[j] + prev_row[j+1])

        new_row.append(1)
        triangle.append(new_row)

    return triangle
```

#### Tricks/Gotchas
- **Problem Variations:** A common variation is "Pascal's Triangle II," which asks for *only* the `k`-th row. This can be solved with O(k) space by only storing the previous row to generate the current one.
- **Off-by-one errors:** Indexing into the `previous_row` requires care. The loop for middle elements runs `len(prev_row) - 1` times.

#### Related Problems
- Pascal's Triangle II
