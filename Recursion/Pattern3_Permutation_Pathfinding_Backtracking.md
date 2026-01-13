### `[PATTERN] Backtracking for Permutations and Pathfinding`

This pattern extends the core backtracking concept to solve two common classes of problems:
1.  **Permutations**: Generating all possible orderings of a set of elements.
2.  **Pathfinding / Maze Problems**: Finding all valid paths through a constrained space, such as a grid, graph, or decision tree, while adhering to a set of rules.

The core template of "choose, recurse, backtrack" remains the same, but the state and choices become more complex.

---

### 1. Permutations
`[MEDIUM]` `#backtracking` `#permutations`

#### Problem Statement
Given an array `nums` of distinct integers, return all the possible permutations. You can return the answer in any order.

#### Implementation Overview
To generate permutations, we need to ensure that each element is used exactly once in each permutation.
- **Choice**: At each step, which of the *unused* numbers should we place next in our permutation?
- **Constraint**: A number cannot be used if it's already in the current permutation.
- **Goal**: The length of the permutation equals the length of `nums`.

A common way to track used elements is with a boolean `visited` array.

#### Time and Space Complexity
- **Time Complexity:** $O(N \cdot N!)$, where $N$ is the number of elements. There are $N!$ permutations, and each takes $O(N)$ to build.
- **Space Complexity:** $O(N)$ for the recursion stack and visited array.

#### Python Code Snippet
```python
def permute(nums: list[int]) -> list[list[int]]:
    result = []
    current_permutation = []
    visited = [False] * len(nums)

    def backtrack():
        # Base Case: A full permutation is found
        if len(current_permutation) == len(nums):
            result.append(list(current_permutation))
            return

        # Explore choices
        for i in range(len(nums)):
            # Constraint: Only use numbers that haven't been visited
            if not visited[i]:
                # 1. Make a choice
                visited[i] = True
                current_permutation.append(nums[i])

                # 2. Recurse
                backtrack()

                # 3. Backtrack
                current_permutation.pop()
                visited[i] = False

    backtrack()
    return result
```
#### Variation: Permutations II (with duplicates)
If the input array contains duplicates, the above approach will generate duplicate permutations. To fix this, first **sort the input `nums`**. Then, add a condition inside the loop: `if i > 0 and nums[i] == nums[i-1] and not visited[i-1]: continue`. This ensures that for a block of identical numbers, we only pick them in one specific order.

---

### 2. Letter Combinations of a Phone Number
`[MEDIUM]` `#backtracking` `#string-generation`

#### Problem Statement
Given a string containing digits from 2-9, return all possible letter combinations that the number could represent.

#### Implementation Overview
This is a variation of a permutation/combination problem where the choices for each position are defined by a mapping.
- **State**: The current index in the input `digits` string and the combination string built so far.
- **Choice**: For the digit at the current index, which letter should we append to our combination?
- **Goal**: The length of our combination string equals the length of the input `digits` string.

#### Time and Space Complexity
- **Time Complexity:** $O(4^N \cdot N)$, where $N$ is the length of digits. Each digit maps to at most 4 letters.
- **Space Complexity:** $O(N)$ for the recursion stack.

#### Python Code Snippet
```python
def letter_combinations(digits: str) -> list[str]:
    if not digits:
        return []

    mapping = {
        '2': "abc", '3': "def", '4': "ghi", '5': "jkl",
        '6': "mno", '7': "pqrs", '8': "tuv", '9': "wxyz"
    }
    result = []

    def backtrack(index, current_combination):
        # Base Case: Reached the end of the digits string
        if index == len(digits):
            result.append("".join(current_combination))
            return

        # Get letters for the current digit
        possible_letters = mapping[digits[index]]

        # Explore choices
        for letter in possible_letters:
            # 1. Choose
            current_combination.append(letter)
            # 2. Recurse
            backtrack(index + 1, current_combination)
            # 3. Backtrack
            current_combination.pop()

    backtrack(0, [])
    return result
```

---

### 3. Word Search
`[MEDIUM]` `#backtracking` `#pathfinding` `#matrix`

#### Problem Statement
Given an `m x n` grid of characters `board` and a string `word`, return `true` if `word` exists in the grid. The word can be constructed from letters of sequentially adjacent cells (horizontally or vertically). The same letter cell may not be used more than once.

#### Implementation Overview
This is a classic pathfinding problem on a grid. We perform a Depth First Search (DFS) from every cell that could be a potential start of the word.
- **State**: The current position `(row, col)` on the board and the current index `k` in the `word` we are trying to match.
- **Choice**: Which of the four adjacent cells (up, down, left, right) should we move to next?
- **Constraint**: The move must be within the grid boundaries, the cell must match `word[k]`, and the cell must not have been visited before in the current path.
- **Goal**: We have successfully matched all characters in the word (`k == len(word)`).

#### Time and Space Complexity
- **Time Complexity:** $O(M \cdot N \cdot 4^L)$, where $M \times N$ is the board size and $L$ is the word length.
- **Space Complexity:** $O(L)$ for the recursion stack.

#### Python Code Snippet
```python
def exist(board: list[list[str]], word: str) -> bool:
    rows, cols = len(board), len(board[0])

    def backtrack(r, c, k):
        # Goal: Successfully found the entire word
        if k == len(word):
            return True

        # Constraints: Check for out-of-bounds or mismatch
        if r < 0 or c < 0 or r >= rows or c >= cols or board[r][c] != word[k]:
            return False

        # 1. Make a choice (and mark as visited)
        original_char = board[r][c]
        board[r][c] = '#' # Mark the cell as visited for this path

        # 2. Recurse on neighbors
        found = (backtrack(r + 1, c, k + 1) or
                 backtrack(r - 1, c, k + 1) or
                 backtrack(r, c + 1, k + 1) or
                 backtrack(r, c - 1, k + 1))

        # 3. Backtrack (undo the choice)
        board[r][c] = original_char # Restore the cell

        return found

    # Try starting the search from every cell
    for r in range(rows):
        for c in range(cols):
            if backtrack(r, c, 0):
                return True

    return False
```

---

### 4. N-Queens
`[HARD]` `#backtracking` `#pathfinding`

#### Problem Statement
The N-Queens puzzle is the problem of placing `N` chess queens on an `N x N` chessboard such that no two queens threaten each other. Given `n`, return all distinct solutions.

#### Implementation Overview
We place one queen per column, ensuring each new placement is safe from all previously placed queens.
- **State**: The current column `col` we are trying to place a queen in, and the `board` configuration.
- **Choice**: In which row `r` of the current column `col` should we place a queen?
- **Constraint**: The chosen cell `(r, col)` must not be under attack by any queen in previous columns.
- **Goal**: We have successfully placed a queen in every column (`col == n`).

#### Time and Space Complexity
- **Time Complexity:** $O(N!)$, as we place queens row by row.
- **Space Complexity:** $O(N)$ for the recursion stack and sets.

#### Python Code Snippet (Optimized)
This version uses sets for an O(1) safety check.
```python
def solve_n_queens(n: int) -> list[list[str]]:
    result = []
    board = [['.' for _ in range(n)] for _ in range(n)]

    # Sets to track attacked columns and diagonals
    attacked_cols = set()
    attacked_pos_diagonals = set() # (r + c) is constant
    attacked_neg_diagonals = set() # (r - c) is constant

    def backtrack(r):
        # Goal: All queens have been placed (one in each row)
        if r == n:
            # Format the board for the result
            copy = ["".join(row) for row in board]
            result.append(copy)
            return

        # Explore choices for the current row `r`
        for c in range(n):
            # Constraints
            if c in attacked_cols or (r + c) in attacked_pos_diagonals or (r - c) in attacked_neg_diagonals:
                continue

            # 1. Make a choice
            board[r][c] = 'Q'
            attacked_cols.add(c)
            attacked_pos_diagonals.add(r + c)
            attacked_neg_diagonals.add(r - c)

            # 2. Recurse
            backtrack(r + 1)

            # 3. Backtrack
            board[r][c] = '.'
            attacked_cols.remove(c)
            attacked_pos_diagonals.remove(r + c)
            attacked_neg_diagonals.remove(r - c)

    backtrack(0)
    return result
```

---

### 5. Sudoku Solver
`[HARD]` `#backtracking` `#pathfinding` `#matrix`

#### Problem Statement
Write a program to solve a Sudoku puzzle by filling the empty cells ('.').

#### Implementation Overview
We find the next empty cell and try placing digits from 1 to 9. If a digit is valid according to Sudoku rules, we place it and recurse. If the recursive call fails, we backtrack.
- **State**: The entire `board`. The search for the next empty cell is part of the function logic.
- **Choice**: For the next empty cell `(r, c)`, which digit from '1' to '9' should we place?
- **Constraint**: The chosen digit must not already exist in the same row, column, or 3x3 sub-grid.
- **Goal**: There are no more empty cells on the board.

#### Time and Space Complexity
- **Time Complexity:** $O(9^M)$, where $M$ is the number of empty cells. In the worst case (empty board), this is huge, but constraints make it feasible.
- **Space Complexity:** $O(1)$ effectively, or $O(M)$ for recursion stack.

#### Python Code Snippet
```python
def solve_sudoku(board: list[list[str]]) -> None:
    """
    Solves the Sudoku puzzle in-place.
    """
    def is_valid(r, c, digit):
        for i in range(9):
            # Check row and column
            if board[r][i] == digit or board[i][c] == digit:
                return False
            # Check 3x3 sub-grid
            box_r, box_c = 3 * (r // 3), 3 * (c // 3)
            if board[box_r + i // 3][box_c + i % 3] == digit:
                return False
        return True

    def backtrack():
        # Find the next empty cell
        for r in range(9):
            for c in range(9):
                if board[r][c] == '.':
                    # Try placing digits 1-9
                    for digit in "123456789":
                        if is_valid(r, c, digit):
                            # 1. Choose
                            board[r][c] = digit

                            # 2. Recurse
                            if backtrack():
                                return True # Solution found

                            # 3. Backtrack
                            board[r][c] = '.'

                    return False # No valid digit found for this cell

        return True # Goal: No empty cells left, puzzle solved

    backtrack()

---

### 10. Expression Add Operators
`[HARD]` `#recursion` `#backtracking` `#string-manipulation`

#### Problem Statement
Given a string `num` that contains only digits and an integer `target`, return all possibilities to add binary operators `+`, `-`, or `*` between the digits of `num` so that the resultant expression evaluates to `target`.

#### Implementation Overview
This is a complex backtracking problem where we build the expression string and evaluate it on the fly. The main difficulty is handling multiplication's higher precedence.
1.  **Recursive Function**: `dfs(index, path, current_val, prev_operand)`
    - `prev_operand` is the value of the last operand. This is the key to handling multiplication correctly.
2.  **Base Case**: If `index` reaches the end of `num`, check if `current_val == target`.
3.  **Recursive Step**:
    - Loop `i` from `index` to generate the current number operand.
    - For each number `s`:
        - **'+'**: Recurse with `current_val + s` and `prev_operand = s`.
        - **'-'**: Recurse with `current_val - s` and `prev_operand = -s`.
        - **'*'**: The new value is `(current_val - prev_operand) + (prev_operand * s)`. The new `prev_operand` becomes `prev_operand * s`.

#### Time and Space Complexity
- **Time Complexity:** $O(4^N)$, where $N$ is the length of the string (3 operators + no operator).
- **Space Complexity:** $O(N)$ for recursion stack.

#### Python Code Snippet
```python
def add_operators(num: str, target: int) -> list[str]:
    result = []

    def backtrack(index, path, current_val, prev_operand):
        if index == len(num):
            if current_val == target:
                result.append(path)
            return

        for i in range(index, len(num)):
            # Handle numbers with leading zeros
            if i > index and num[index] == '0':
                break

            current_str = num[index:i+1]
            current_num = int(current_str)

            if index == 0:
                # First number
                backtrack(i + 1, current_str, current_num, current_num)
            else:
                # Addition
                backtrack(i + 1, path + "+" + current_str, current_val + current_num, current_num)
                # Subtraction
                backtrack(i + 1, path + "-" + current_str, current_val - current_num, -current_num)
                # Multiplication
                backtrack(i + 1, path + "*" + current_str,
                          current_val - prev_operand + (prev_operand * current_num),
                          prev_operand * current_num)

    backtrack(0, "", 0, 0)
    return result
```

---

### 9. M-Coloring Problem
`[HARD]` `#recursion` `#backtracking` `#graph`

#### Problem Statement
Given an undirected graph and an integer `M`, determine if the graph can be colored with at most `M` colors such that no two adjacent vertices have the same color.

#### Implementation Overview
We attempt to color the graph's vertices one by one, from vertex 0 to N-1.
1.  **Recursive Function**: `solve(node_index, colors_array)`
2.  **Base Case**: If `node_index == N`, all vertices have been successfully colored. Return `true`.
3.  **Recursive Step**: For vertex `node_index`:
    - Loop through each color `c` from 1 to `M`.
    - Check if it is `isSafe` to assign color `c`. This involves checking all of its neighbors to see if any are already assigned color `c`.
    - If safe, assign the color, and recurse: `solve(node_index + 1, ...)`.
    - If the recursive call is true, a solution was found. Propagate `true`.
    - If not, backtrack by resetting the color and try the next color.
4. If no color works, return `false`.

#### Time and Space Complexity
- **Time Complexity:** $O(M^V)$, where $V$ is vertices and $M$ is colors.
- **Space Complexity:** $O(V)$ for colors array and recursion stack.

#### Python Code Snippet
```python
def can_m_color(graph: list[list[int]], m: int, n: int) -> bool:
    colors = [0] * n # 0 means no color

    def is_safe(node, color):
        for neighbor in graph[node]:
            if colors[neighbor] == color:
                return False
        return True

    def solve(node_idx):
        if node_idx == n:
            return True

        for c in range(1, m + 1):
            if is_safe(node_idx, c):
                colors[node_idx] = c
                if solve(node_idx + 1):
                    return True
                colors[node_idx] = 0 # Backtrack

        return False

    return solve(0)
```

---

### 8. Word Break
`[MEDIUM]` `#recursion` `#backtracking` `#dynamic-programming`

#### Problem Statement
Given a string `s` and a dictionary of strings `wordDict`, return `true` if `s` can be segmented into a space-separated sequence of one or more dictionary words.

#### Implementation Overview
This is a partitioning problem where we check if any prefix of the string is a valid word. If it is, we recursively check if the remaining suffix can also be broken down.
1.  **Recursive Function**: `can_break(substring)`
2.  **Base Case**: If `substring` is empty, the original string has been successfully segmented. Return `true`.
3.  **Recursive Step**:
    - Iterate `i` from 1 to `len(substring)`.
    - Check if the `prefix` (`substring[0...i]`) is in the `wordDict`.
    - If it is, recurse on the `suffix`: `can_break(substring[i...])`.
    - If the recursive call is true, we have a valid path. Return `true`.
4.  If the loop finishes, no valid segmentation was found. Return `false`.
5.  **Optimization**: This has overlapping subproblems and can be optimized with memoization (DP).

#### Time and Space Complexity
- **Time Complexity:** $O(N^3)$ (with memoization) due to substring slicing in the loop.
- **Space Complexity:** $O(N)$ for the recursion stack and memoization.

#### Python Code Snippet
```python
def word_break(s: str, wordDict: list[str]) -> bool:
    word_set = set(wordDict)
    memo = {}

    def solve(substring):
        if not substring:
            return True
        if substring in memo:
            return memo[substring]

        for i in range(1, len(substring) + 1):
            prefix = substring[:i]
            if prefix in word_set and solve(substring[i:]):
                memo[substring] = True
                return True

        memo[substring] = False
        return False

    return solve(s)
```

---

### 7. Rat in a Maze
`[MEDIUM]` `#recursion` `#backtracking` `#matrix`

#### Problem Statement
Given a square maze `m` of size `N x N` where `1` means the block is open and `0` is a wall. A rat starts at `(0, 0)` and wants to reach `(N-1, N-1)`. Find all possible paths.

#### Implementation Overview
This is a DFS on a grid problem. We explore all possible paths, backtracking when we hit a wall or a visited cell.
1.  **Recursive Function**: `find_paths(row, col, maze, current_path, visited)`
2.  **Base Case**: If the rat is at the destination, add `current_path` to results.
3.  **Recursive Step & Constraints**:
    - Mark current cell as visited.
    - Explore all 4 directions (D, L, R, U).
    - For each valid move (in-bounds, not a wall, not visited), recurse.
    - Backtrack by un-marking the current cell as visited.

#### Time and Space Complexity
- **Time Complexity:** $O(4^{N^2})$, worst case exponential.
- **Space Complexity:** $O(N^2)$ for visited array and recursion stack.

#### Python Code Snippet
```python
def find_rat_maze_paths(m: list[list[int]]) -> list[str]:
    n = len(m)
    if m[0][0] == 0 or m[n-1][n-1] == 0:
        return []

    result = []
    visited = [[False for _ in range(n)] for _ in range(n)]

    def solve(r, c, current_path):
        if r == n - 1 and c == n - 1:
            result.append(current_path)
            return

        # D, L, R, U order
        # Down
        if r + 1 < n and not visited[r+1][c] and m[r+1][c] == 1:
            visited[r][c] = True
            solve(r + 1, c, current_path + 'D')
            visited[r][c] = False
        # Left
        if c - 1 >= 0 and not visited[r][c-1] and m[r][c-1] == 1:
            visited[r][c] = True
            solve(r, c - 1, current_path + 'L')
            visited[r][c] = False
        # Right
        if c + 1 < n and not visited[r][c+1] and m[r][c+1] == 1:
            visited[r][c] = True
            solve(r, c + 1, current_path + 'R')
            visited[r][c] = False
        # Up
        if r - 1 >= 0 and not visited[r-1][c] and m[r-1][c] == 1:
            visited[r][c] = True
            solve(r - 1, c, current_path + 'U')
            visited[r][c] = False

    solve(0, 0, "")
    return result
```

---

### 6. Palindrome Partitioning
`[MEDIUM]` `#recursion` `#backtracking`

#### Problem Statement
Given a string `s`, partition `s` such that every substring of the partition is a palindrome. Return all possible palindrome partitionings of `s`.

#### Implementation Overview
The strategy is to iterate through all possible prefixes of the current string. If a prefix is a palindrome, we add it to our current partition and recursively solve for the rest of the string.
1.  **Recursive Function**: `partition_helper(start_index, current_partition)`
2.  **Base Case**: If `start_index` reaches the end of the string, a valid partition is found.
3.  **Recursive Step**:
    - Loop `i` from `start_index` to the end of the string.
    - The substring `s[start_index...i]` is a potential first piece of the partition.
    - If this substring is a palindrome, add it to `current_partition` and recurse on the rest: `partition_helper(i + 1, ...)`.
    - Backtrack by removing the substring from `current_partition`.

#### Time and Space Complexity
- **Time Complexity:** $O(N \cdot 2^N)$, as there are $2^N$ possible partitions and checking palindrome takes $O(N)$.
- **Space Complexity:** $O(N)$ for recursion stack.

#### Python Code Snippet
```python
def partition_palindrome(s: str) -> list[list[str]]:
    result = []
    current_partition = []

    def is_palindrome(sub: str) -> bool:
        return sub == sub[::-1]

    def backtrack(start_index):
        if start_index == len(s):
            result.append(list(current_partition))
            return

        for i in range(start_index, len(s)):
            prefix = s[start_index : i + 1]
            if is_palindrome(prefix):
                current_partition.append(prefix)
                backtrack(i + 1)
                current_partition.pop()

    backtrack(0)
    return result
```
```
