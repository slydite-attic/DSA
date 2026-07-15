# Pattern 4: Advanced String DP

This pattern covers string-based DP problems that, while still often using a 2D DP table, have more complex recurrence relations or state transitions than the LCS family. These problems often require careful handling of multiple choices at each step or special characters.

---

### 1. Distinct Subsequences
`[HARD]` `#string-dp` `#count`

#### Problem Statement
Given two strings, `s` and `t`, count the number of distinct subsequences of `s` which equals `t`.

#### Recurrence Relation
Let `solve(i, j)` be the number of ways to form `t[0...j]` using `s[0...i]`.
- If `s[i] == t[j]`: We have two choices.
    1. Match `s[i]` with `t[j]`. The number of ways is `solve(i-1, j-1)`.
    2. Don't match `s[i]` with `t[j]`. The number of ways is `solve(i-1, j)`.
    Total ways = `solve(i-1, j-1) + solve(i-1, j)`.
- If `s[i] != t[j]`: We cannot match them. We must find `t[0...j]` in `s[0...i-1]`. The number of ways is `solve(i-1, j)`.

---
#### a) Memoization (Top-Down)
```python
def num_distinct_memo(s: str, t: str) -> int:
    n, m = len(s), len(t) # Get lengths of strings s and t.
    dp = [[-1] * m for _ in range(n)] # Initialize a memoization table.

    def solve(i, j): # Recursive helper function.
        if j < 0: return 1 # Base case: If t is empty, we found one valid subsequence.
        if i < 0: return 0 # Base case: If s is empty but t is not, no solution.
        if dp[i][j] != -1: return dp[i][j] # Return memoized result if available.

        if s[i] == t[j]: # If characters match,
            # We can either match s[i] with t[j] or not.
            dp[i][j] = solve(i - 1, j - 1) + solve(i - 1, j)
        else: # If characters don't match,
            # We must skip s[i] and find t in the rest of s.
            dp[i][j] = solve(i - 1, j)
        return dp[i][j] # Return the computed result.

    return solve(n - 1, m - 1) # Start recursion from the end of both strings.
```
- **Time Complexity:** O(n * m).
- **Space Complexity:** O(n * m) for DP table + O(n+m) for recursion stack.

---
#### b) Tabulation (Bottom-Up)
```python
def num_distinct_tab(s: str, t: str) -> int:
    n, m = len(s), len(t) # Get lengths of the strings.
    dp = [[0] * (m + 1) for _ in range(n + 1)] # Initialize a 2D DP table.

    # Base case: There's one way to form an empty t (by choosing no characters) from any prefix of s.
    for i in range(n + 1): # Iterate through all rows.
        dp[i][0] = 1 # Set the first column to 1.

    for i in range(1, n + 1): # Iterate through the characters of s.
        for j in range(1, m + 1): # Iterate through the characters of t.
            if s[i-1] == t[j-1]: # If characters match,
                # The number of ways is the sum of ways to form t[0...j-1] from s[0...i-1]
                # and the ways to form t[0...j] from s[0...i-1].
                dp[i][j] = dp[i-1][j-1] + dp[i-1][j]
            else: # If they don't match,
                # The number of ways is the same as forming t from the prefix of s without the current character.
                dp[i][j] = dp[i-1][j]

    return dp[n][m] # The result is in the bottom-right cell.
```
- **Time Complexity:** O(n * m).
- **Space Complexity:** O(n * m).

---
#### c) Space Optimization
```python
def num_distinct_optimized(s: str, t: str) -> int:
    n, m = len(s), len(t) # Get string lengths.
    prev_row = [0] * (m + 1) # Initialize a single DP array for space optimization.
    prev_row[0] = 1 # Base case: one way to form an empty string.

    for i in range(1, n + 1): # Iterate through string s.
        for j in range(m, 0, -1): # Iterate backwards through string t to use previous row's values correctly.
            if s[i-1] == t[j-1]: # If characters match,
                # Update the number of ways for the current position.
                prev_row[j] = prev_row[j-1] + prev_row[j]

    return prev_row[m] # The result is the last element of the DP array.
```
- **Time Complexity:** O(n * m).
- **Space Complexity:** O(m).

---

### 2. Edit Distance
`[MEDIUM]` `#string-dp` `#edit-distance`

#### Problem Statement
Given `word1` and `word2`, find the minimum operations (insert, delete, replace) to convert `word1` to `word2`.

#### Recurrence Relation
Let `solve(i, j)` be the min ops for `word1[0...i]` and `word2[0...j]`.
- If `word1[i] == word2[j]`: No operation needed. `solve(i-1, j-1)`.
- If they differ, take the minimum of the three choices:
    1. **Insert:** Convert `word1[0...i]` to `word2[0...j-1]` then insert `word2[j]`. Cost: `1 + solve(i, j-1)`.
    2. **Delete:** Delete `word1[i]` then convert `word1[0...i-1]` to `word2[0...j]`. Cost: `1 + solve(i-1, j)`.
    3. **Replace:** Replace `word1[i]` with `word2[j]`. Cost: `1 + solve(i-1, j-1)`.

---
#### a) Memoization (Top-Down)
```python
def min_distance_memo(word1: str, word2: str) -> int:
    n, m = len(word1), len(word2) # Get lengths of the words.
    dp = [[-1] * m for _ in range(n)] # Initialize a memoization table.

    def solve(i, j): # Recursive helper function.
        if i < 0: return j + 1 # Base case: If word1 is empty, must insert all of word2's characters.
        if j < 0: return i + 1 # Base case: If word2 is empty, must delete all of word1's characters.
        if dp[i][j] != -1: return dp[i][j] # Return memoized result.

        if word1[i] == word2[j]: # If characters match,
            dp[i][j] = solve(i - 1, j - 1) # No operation needed, move to the next characters.
        else: # If characters are different,
            insert_op = solve(i, j - 1) # Cost of insertion.
            delete_op = solve(i - 1, j) # Cost of deletion.
            replace_op = solve(i - 1, j - 1) # Cost of replacement.
            dp[i][j] = 1 + min(insert_op, delete_op, replace_op) # Take the minimum cost of the three operations and add 1.
        return dp[i][j] # Return the computed minimum distance.

    return solve(n - 1, m - 1) # Start the recursion from the end of both words.
```
- **Time Complexity:** O(n * m).
- **Space Complexity:** O(n * m) for the DP table + O(n + m) for recursion stack.

---
#### b) Tabulation (Bottom-Up)
```python
def min_distance_tab(word1: str, word2: str) -> int:
    n, m = len(word1), len(word2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    # Base cases
    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                insert_op = dp[i][j-1]
                delete_op = dp[i-1][j]
                replace_op = dp[i-1][j-1]
                dp[i][j] = 1 + min(insert_op, delete_op, replace_op)

    return dp[n][m]
```
- **Time/Space Complexity:** O(n * m).

---
#### c) Space Optimization
```python
def min_distance_optimized(word1: str, word2: str) -> int:
    n, m = len(word1), len(word2)
    prev_row = [j for j in range(m + 1)]

    for i in range(1, n + 1):
        curr_row = [0] * (m + 1)
        curr_row[0] = i
        for j in range(1, m + 1):
            if word1[i-1] == word2[j-1]:
                curr_row[j] = prev_row[j-1]
            else:
                insert_op = curr_row[j-1]
                delete_op = prev_row[j]
                replace_op = prev_row[j-1]
                curr_row[j] = 1 + min(insert_op, delete_op, replace_op)
        prev_row = curr_row

    return prev_row[m]
```
- **Time Complexity:** O(n * m).
- **Space Complexity:** O(m).

---

### 3. Wildcard Matching
`[HARD]` `#string-dp` `#wildcard`

#### Problem Statement
Given a string `s` and a pattern `p` with `?` and `*`, implement wildcard matching.
- `?` Matches any single character.
- `*` Matches any sequence of characters (including empty).

#### Recurrence Relation
Let `solve(i, j)` be true if `s[0...i]` matches `p[0...j]`.
- If `p[j] == '?'` or `p[j] == s[i]`: `solve(i-1, j-1)`.
- If `p[j] == '*'`: `*` can match empty (`solve(i, j-1)`) OR `*` can match `s[i]` (`solve(i-1, j)`). So, `solve(i, j-1) or solve(i-1, j)`.
- Otherwise: `False`.

---
#### a) Memoization (Top-Down)
```python
def is_match_wildcard_memo(s: str, p: str) -> bool:
    n, m = len(s), len(p)
    dp = [[-1] * m for _ in range(n)]

    def solve(i, j):
        # Base Cases
        if i < 0 and j < 0:
            return True
        if j < 0:
            return False
        if i < 0:
            # Pattern must only consist of '*' to match empty string
            for k in range(j + 1):
                if p[k] != '*':
                    return False
            return True

        if dp[i][j] != -1:
            return dp[i][j] == 1

        if p[j] == '?' or p[j] == s[i]:
            ans = solve(i - 1, j - 1)
        elif p[j] == '*':
            ans = solve(i, j - 1) or solve(i - 1, j)
        else:
            ans = False

        dp[i][j] = 1 if ans else 0
        return ans

    return solve(n - 1, m - 1)
```
- **Time Complexity:** O(n * m).
- **Space Complexity:** O(n * m) for the DP table + O(n + m) for the recursion stack.

---
#### b) Tabulation (Bottom-Up)
```python
def is_match_wildcard_tab(s: str, p: str) -> bool:
    n, m = len(s), len(p)
    dp = [[False] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = True

    for j in range(1, m + 1):
        if p[j-1] == '*':
            dp[0][j] = dp[0][j-1]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if p[j-1] == '?' or p[j-1] == s[i-1]:
                dp[i][j] = dp[i-1][j-1]
            elif p[j-1] == '*':
                dp[i][j] = dp[i][j-1] or dp[i-1][j]
            else:
                dp[i][j] = False

    return dp[n][m]
```
- **Time/Space Complexity:** O(n*m).

---
#### c) Space Optimization
```python
def is_match_wildcard_optimized(s: str, p: str) -> bool:
    n, m = len(s), len(p)
    prev = [False] * (m + 1)
    prev[0] = True

    for j in range(1, m + 1):
        if p[j-1] == '*':
            prev[j] = prev[j-1]

    for i in range(1, n + 1):
        curr = [False] * (m + 1)
        # Note: curr[0] is False because non-empty string cannot match empty pattern
        for j in range(1, m + 1):
            if p[j-1] == '?' or p[j-1] == s[i-1]:
                curr[j] = prev[j-1]
            elif p[j-1] == '*':
                curr[j] = curr[j-1] or prev[j]
        prev = curr

    return prev[m]
```
- **Time Complexity:** O(n * m).
- **Space Complexity:** O(m).
