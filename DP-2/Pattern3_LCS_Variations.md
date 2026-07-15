# Pattern 3: Longest Common Subsequence (LCS) & Variations

The Longest Common Subsequence (LCS) is a fundamental DP pattern for problems involving two strings. The core idea is to build a 2D DP table where `dp[i][j]` represents the solution for the prefixes of the strings. Many string problems can be solved by applying the LCS algorithm directly or by slightly modifying its recurrence relation.

---

### 1. Longest Common Subsequence
`[MEDIUM]` `#lcs` `#string-dp`

#### Problem Statement
Given two strings, `text1` and `text2`, return the length of their longest common subsequence.

#### Recurrence Relation
Let `solve(i, j)` be the LCS length for `text1[0...i]` and `text2[0...j]`.
- If `text1[i] == text2[j]`: The characters match. The LCS length is `1 + solve(i-1, j-1)`.
- If `text1[i] != text2[j]`: The characters don't match. We have two choices:
    - Ignore the character from `text1`: `solve(i-1, j)`.
    - Ignore the character from `text2`: `solve(i, j-1)`.
    We take the maximum of these two choices.

---
#### a) Memoization (Top-Down)
```python
def lcs_memo(text1: str, text2: str) -> int:
    n, m = len(text1), len(text2) # Get the lengths of the two input strings.
    dp = [[-1] * m for _ in range(n)] # Initialize a memoization table with -1.

    def solve(i, j): # Recursive helper function to compute LCS length for text1[0..i] and text2[0..j].
        if i < 0 or j < 0: # Base case: If either string is empty, the LCS is 0.
            return 0
        if dp[i][j] != -1: # If the result for this state is already computed, return it.
            return dp[i][j]

        if text1[i] == text2[j]: # If the characters at the current indices match,
            dp[i][j] = 1 + solve(i - 1, j - 1) # The LCS length is 1 + LCS of the preceding substrings.
        else: # If the characters do not match,
            dp[i][j] = max(solve(i - 1, j), solve(i, j - 1)) # Take the maximum LCS from the two possible subproblems.
        return dp[i][j] # Return the computed value.

    return solve(n - 1, m - 1) # Start the recursion from the end of both strings.
```
- **Time Complexity:** O(n * m).
- **Space Complexity:** O(n * m) for DP table + O(n+m) for recursion stack.

---
#### b) Tabulation (Bottom-Up)
```python
def lcs_tab(text1: str, text2: str) -> int:
    n, m = len(text1), len(text2) # Get the lengths of the two strings.
    dp = [[0] * (m + 1) for _ in range(n + 1)] # Initialize a 2D DP table with zeros. The +1 is for the base case of empty strings.

    for i in range(1, n + 1): # Iterate through text1.
        for j in range(1, m + 1): # Iterate through text2.
            if text1[i-1] == text2[j-1]: # If the characters match,
                dp[i][j] = 1 + dp[i-1][j-1] # The LCS length is 1 + the LCS of the strings without these characters.
            else: # If they don't match,
                dp[i][j] = max(dp[i-1][j], dp[i][j-1]) # Take the maximum LCS from the previous states.

    return dp[n][m] # The result is in the bottom-right cell of the DP table.
```
- **Time Complexity:** O(n * m).
- **Space Complexity:** O(n * m).

---
#### c) Space Optimization
```python
def lcs_optimized(text1: str, text2: str) -> int:
    n, m = len(text1), len(text2) # Get the lengths of the two strings.
    prev_row = [0] * (m + 1) # Initialize a DP array for the previous row.

    for i in range(1, n + 1): # Iterate through text1.
        curr_row = [0] * (m + 1) # Initialize a DP array for the current row.
        for j in range(1, m + 1): # Iterate through text2.
            if text1[i-1] == text2[j-1]: # If characters match,
                curr_row[j] = 1 + prev_row[j-1] # The value is 1 + the diagonal value from the previous row.
            else: # If they don't match,
                curr_row[j] = max(prev_row[j], curr_row[j-1]) # Take the max from the value above or the value to the left.
        prev_row = curr_row # The current row becomes the previous row for the next iteration.

    return prev_row[m] # The result is the last element of the final row.
```
- **Time Complexity:** O(n * m).
- **Space Complexity:** O(m), where m is the length of the shorter string.

---
#### d) Alternative Formulation: LCS to LIS Reduction (O(n log n))
If one of the strings has **all unique characters** (e.g. a permutation of numbers or distinct characters), we can map the LCS problem to a **Longest Increasing Subsequence (LIS)** problem.
1. Create a hash map `pos` that maps each character of `text1` to its index.
2. Iterate through `text2`. If a character is in `pos`, replace it with its mapped index. If it isn't, discard it.
3. Find the LIS of the resulting index list. Since LIS can be solved in $O(n \log n)$ using binary search (patience sorting), this solves LCS in $O(n \log n)$ time.

```python
import bisect

def lcs_via_lis(text1: str, text2: str) -> int:
    # Build map from character to index in text1
    # Assumes text1 has unique characters (or we track positions list for duplicates)
    pos = {char: idx for idx, char in enumerate(text1)}
    
    # Map text2 characters to their indices in text1
    mapped_indices = []
    for char in text2:
        if char in pos:
            mapped_indices.append(pos[char])
            
    # Find LIS of mapped_indices in O(N log N)
    sub = []
    for num in mapped_indices:
        idx = bisect.bisect_left(sub, num)
        if idx == len(sub):
            sub.append(num)
        else:
            sub[idx] = num
            
    return len(sub)
```
- **Time Complexity:** O(n + m log m).
- **Space Complexity:** O(n + m) to store map and mapped list.

---

#### 2. Longest Palindromic Subsequence
`[MEDIUM]` `#lps` `#lcs` `#string-dp`

#### Problem Statement
Given a string `s`, find the length of the longest palindromic subsequence.

#### Recurrence Relation
Let `dp[i][j]` be the length of the longest palindromic subsequence in `s[i...j]`.
- If `s[i] == s[j]`: `dp[i][j] = 2 + dp[i+1][j-1]` (with base cases handled).
- If `s[i] != s[j]`: `dp[i][j] = max(dp[i+1][j], dp[i][j-1])`.
- **Alternative Insight:** The LPS of `s` is equivalent to the LCS of `s` and `reverse(s)`.

---
#### a) Memoization (Top-Down Interval DP)
```python
def lps_memo(s: str) -> int:
    n = len(s)
    dp = [[-1] * n for _ in range(n)]

    def solve(i, j):
        if i > j:
            return 0
        if i == j:
            return 1
        if dp[i][j] != -1:
            return dp[i][j]

        if s[i] == s[j]:
            dp[i][j] = 2 + solve(i + 1, j - 1)
        else:
            dp[i][j] = max(solve(i + 1, j), solve(i, j - 1))
        return dp[i][j]

    return solve(0, n - 1)
```
- **Time Complexity:** O(n^2).
- **Space Complexity:** O(n^2) for the DP table + O(n) recursion stack.

---
#### b) Tabulation (Bottom-Up)
```python
def lps_tab(s: str) -> int:
    n = len(s)
    dp = [[0] * n for _ in range(n)]
    
    # Base cases: Single character substrings are palindromes of length 1
    for i in range(n):
        dp[i][i] = 1

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                dp[i][j] = 2 + (dp[i+1][j-1] if i+1 <= j-1 else 0)
            else:
                dp[i][j] = max(dp[i+1][j], dp[i][j-1])

    return dp[0][n-1]
```
- **Time Complexity:** O(n^2).
- **Space Complexity:** O(n^2).

---
#### c) Space Optimization
```python
def lps_optimized(s: str) -> int:
    n = len(s)
    dp = [0] * n # Represents the row below the current row

    for i in range(n - 1, -1, -1):
        new_dp = [0] * n
        new_dp[i] = 1 # Base case: single character
        for j in range(i + 1, n):
            if s[i] == s[j]:
                new_dp[j] = 2 + (dp[j-1] if i+1 <= j-1 else 0)
            else:
                new_dp[j] = max(dp[j], new_dp[j-1])
        dp = new_dp

    return dp[n-1]
```
- **Time Complexity:** O(n^2).
- **Space Complexity:** O(n).

---

### 3. Minimum Insertions to Make a String Palindrome
`[HARD]` `#lps` `#lcs` `#string-dp`

#### Problem Statement
Given a string `s`, find the minimum number of insertions required to make it a palindrome.

#### Recurrence Relation
- The minimum insertions to make a string a palindrome is `len(s) - LPS(s)`. The longest palindromic subsequence remains untouched, and we insert matching characters for the remainder.

---
#### a) Memoization (Top-Down)
```python
def min_insertions_to_palindrome_memo(s: str) -> int:
    return len(s) - lps_memo(s)
```
- **Time/Space Complexity:** Same as `lps_memo`, O(n^2).

---
#### b) Tabulation (Bottom-Up)
```python
def min_insertions_to_palindrome_tab(s: str) -> int:
    return len(s) - lps_tab(s)
```
- **Time/Space Complexity:** Same as `lps_tab`, O(n^2).

---
#### c) Space Optimization
```python
def min_insertions_to_palindrome_optimized(s: str) -> int:
    return len(s) - lps_optimized(s)
```
- **Time Complexity:** O(n^2).
- **Space Complexity:** O(n).

---

### 4. Minimum Deletions/Insertions to Convert String A to B
`[MEDIUM]` `#lcs` `#string-dp`

#### Problem Statement
Given `str1` and `str2`, find the minimum number of deletions and insertions to convert `str1` to `str2`.

#### Recurrence Relation
- Keep the LCS intact. Delete the remaining characters of `str1`, and insert the remaining characters of `str2`.
- `deletions = len(str1) - LCS`
- `insertions = len(str2) - LCS`
- `total_operations = len(str1) + len(str2) - 2 * LCS`

---
#### a) Memoization (Top-Down)
```python
def min_ops_to_convert_memo(str1: str, str2: str) -> int:
    return len(str1) + len(str2) - 2 * lcs_memo(str1, str2)
```
- **Time/Space Complexity:** Same as `lcs_memo`, O(n * m).

---
#### b) Tabulation (Bottom-Up)
```python
def min_ops_to_convert_tab(str1: str, str2: str) -> int:
    return len(str1) + len(str2) - 2 * lcs_tab(str1, str2)
```
- **Time/Space Complexity:** Same as `lcs_tab`, O(n * m).

---
#### c) Space Optimization
```python
def min_ops_to_convert_optimized(str1: str, str2: str) -> int:
    return len(str1) + len(str2) - 2 * lcs_optimized(str1, str2)
```
- **Time Complexity:** O(n * m).
- **Space Complexity:** O(min(n, m)).

---

### 5. Shortest Common Supersequence
`[HARD]` `#lcs` `#string-dp` `#scs`

#### Problem Statement
Given `str1` and `str2`, return the shortest string that has both as subsequences.

#### Recurrence/Printing Algorithm
- `len(SCS) = len(str1) + len(str2) - len(LCS)`.
- To print the string, we backtrack on the LCS `dp` table.

---
#### a) Memoization (Top-Down Length)
```python
def shortest_common_supersequence_len_memo(str1: str, str2: str) -> int:
    return len(str1) + len(str2) - lcs_memo(str1, str2)
```
- **Time/Space Complexity:** O(n * m).

---
#### b) Tabulation & Printing (Bottom-Up)
```python
def shortest_common_supersequence_print(str1: str, str2: str) -> str:
    n, m = len(str1), len(str2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if str1[i-1] == str2[j-1]:
                dp[i][j] = 1 + dp[i-1][j-1]
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    # Backtrack to build the SCS
    res = []
    i, j = n, m
    while i > 0 and j > 0:
        if str1[i-1] == str2[j-1]:
            res.append(str1[i-1])
            i -= 1
            j -= 1
        elif dp[i-1][j] > dp[i][j-1]:
            res.append(str1[i-1])
            i -= 1
        else:
            res.append(str2[j-1])
            j -= 1

    while i > 0:
        res.append(str1[i-1])
        i -= 1
    while j > 0:
        res.append(str2[j-1])
        j -= 1

    return "".join(reversed(res))
```
- **Time/Space Complexity:** O(n * m).

---
#### c) Space Optimization (Length Only)
```python
def shortest_common_supersequence_len_optimized(str1: str, str2: str) -> int:
    return len(str1) + len(str2) - lcs_optimized(str1, str2)
```
- **Time Complexity:** O(n * m).
- **Space Complexity:** O(min(n, m)).

---

### 6. Print Longest Common Subsequence
`[MEDIUM]` `#lcs` `#string-dp`

#### Problem Statement
Given two strings `text1` and `text2`, find and return their longest common subsequence as a string.

---
#### a) Memoization (Top-Down String DP)
```python
def print_lcs_memo(text1: str, text2: str) -> str:
    memo = {}

    def solve(i, j):
        if i < 0 or j < 0:
            return ""
        if (i, j) in memo:
            return memo[(i, j)]

        if text1[i] == text2[j]:
            memo[(i, j)] = solve(i - 1, j - 1) + text1[i]
        else:
            s1 = solve(i - 1, j)
            s2 = solve(i, j - 1)
            memo[(i, j)] = s1 if len(s1) > len(s2) else s2
        return memo[(i, j)]

    return solve(len(text1) - 1, len(text2) - 1)
```
- **Time Complexity:** O(n * m * min(n, m)) due to string concatenations.
- **Space Complexity:** O(n * m * min(n, m)) for storing strings in memo cache.

---
#### b) Tabulation & Backtracking (Bottom-Up)
```python
def print_lcs_tab(text1: str, text2: str) -> str:
    n, m = len(text1), len(text2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = 1 + dp[i-1][j-1]
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    # Backtrack
    i, j = n, m
    res = []
    while i > 0 and j > 0:
        if text1[i-1] == text2[j-1]:
            res.append(text1[i-1])
            i -= 1
            j -= 1
        elif dp[i-1][j] > dp[i][j-1]:
            i -= 1
        else:
            j -= 1
    return "".join(reversed(res))
```
- **Time Complexity:** O(n * m) to build the table, O(n+m) to backtrack.
- **Space Complexity:** O(n * m) to store the table.

> **Note on Space Optimization:** Printing the LCS requires backtracking through the `dp` table from `dp[n][m]` to `dp[0][0]`. At each backtracking step, the algorithm compares `dp[i-1][j]` vs `dp[i][j-1]`, requiring simultaneous access to multiple rows. Reducing to a 1D rolling array overwrites previously needed row values, making path reconstruction impossible. The full O(n * m) table is therefore **required** for printing. If only the **length** is needed, use `lcs_optimized` from Problem 1 for O(m) space.

---

### 7. Longest Common Substring
`[MEDIUM]` `#lcs` `#substring`

#### Problem Statement
Given two strings `text1` and `text2`, find the length of their longest common substring.

#### Recurrence Relation
Let `dp[i][j]` be the length of the common substring ending at `text1[i-1]` and `text2[j-1]`.
- If `text1[i-1] == text2[j-1]`: `dp[i][j] = 1 + dp[i-1][j-1]`
- If `text1[i-1] != text2[j-1]`: `dp[i][j] = 0`
- **Result:** Max value in the entire `dp` table.

---
#### a) Memoization (Top-Down)
```python
def longest_common_substring_memo(text1: str, text2: str) -> int:
    n, m = len(text1), len(text2)
    dp = [[-1] * m for _ in range(n)]
    max_len = 0

    def solve(i, j):
        nonlocal max_len
        if i < 0 or j < 0:
            return 0
        if dp[i][j] != -1:
            return dp[i][j]

        # Recurse for all subproblems to ensure all states are computed
        solve(i - 1, j)
        solve(i, j - 1)

        if text1[i] == text2[j]:
            dp[i][j] = 1 + solve(i - 1, j - 1)
            max_len = max(max_len, dp[i][j])
        else:
            dp[i][j] = 0
        return dp[i][j]

    solve(n - 1, m - 1)
    return max_len
```
- **Time Complexity:** O(n * m).
- **Space Complexity:** O(n * m) + O(n + m) recursion stack.

---
#### b) Tabulation (Bottom-Up)
```python
def longest_common_substring_tab(text1: str, text2: str) -> int:
    n, m = len(text1), len(text2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    max_len = 0

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = 1 + dp[i-1][j-1]
                max_len = max(max_len, dp[i][j])
            else:
                dp[i][j] = 0

    return max_len
```
- **Time Complexity:** O(n * m).
- **Space Complexity:** O(n * m).

---
#### c) Space Optimization
```python
def longest_common_substring_optimized(text1: str, text2: str) -> int:
    n, m = len(text1), len(text2)
    prev_row = [0] * (m + 1)
    max_len = 0

    for i in range(1, n + 1):
        curr_row = [0] * (m + 1)
        for j in range(1, m + 1):
            if text1[i-1] == text2[j-1]:
                curr_row[j] = 1 + prev_row[j-1]
                max_len = max(max_len, curr_row[j])
        prev_row = curr_row

    return max_len
```
- **Time Complexity:** O(n * m).
- **Space Complexity:** O(m).
