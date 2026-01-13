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
#### Time and Space Complexity
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
#### Time and Space Complexity
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
#### Time and Space Complexity
- **Time Complexity:** O(n * m).
- **Space Complexity:** O(m), where m is the length of the shorter string.

---

### 2. Longest Palindromic Subsequence
`[MEDIUM]` `#lps` `#lcs` `#string-dp`

#### Problem Statement
Given a string `s`, find the length of the longest palindromic subsequence.

#### Implementation Overview
- **Insight:** A palindrome reads the same forwards and backwards. Therefore, the longest palindromic subsequence of `s` is simply the **Longest Common Subsequence of `s` and `reverse(s)`**.
- **Algorithm:** Create a reversed copy of `s` and use any of the LCS implementations above to find the length.

#### Python Code Snippet
```python
def longest_palindromic_subsequence(s: str) -> int:
    # The longest palindromic subsequence is equivalent to the longest common subsequence
    # between the string and its reverse.
    return lcs_optimized(s, s[::-1]) # Call the LCS function with the string and its reverse.
```
#### Time and Space Complexity
- **Time Complexity:** Same as the underlying LCS implementation used ($O(N^2)$).
- **Space Complexity:** Same as the underlying LCS implementation used ($O(N)$ if optimized).

---

### 3. Minimum Insertions to Make a String Palindrome
`[HARD]` `#lps` `#lcs` `#string-dp`

#### Problem Statement
Given a string `s`, find the minimum number of insertions required to make it a palindrome.

#### Implementation Overview
- **Insight:** The characters that are already part of the Longest Palindromic Subsequence (LPS) form a "stable" core that doesn't need to be touched. The characters *not* in the LPS are the ones that are "unmatched" and each requires a corresponding character to be inserted to make the whole string a palindrome.
- **Algorithm:**
    1.  Find the length of the LPS (`len_lps`).
    2.  The number of insertions needed is `len(s) - len_lps`.

#### Python Code Snippet
```python
def min_insertions_to_palindrome(s: str) -> int:
    len_lps = longest_palindromic_subsequence(s) # First, find the length of the longest palindromic subsequence.
    # The number of insertions needed is the total length of the string minus the length of the LPS.
    return len(s) - len_lps
```
#### Time and Space Complexity
- **Time Complexity:** Dominated by the LPS calculation ($O(N^2)$).
- **Space Complexity:** Dominated by the LPS calculation ($O(N)$).

---

### 4. Minimum Deletions/Insertions to Convert String A to B
`[MEDIUM]` `#lcs` `#string-dp`

#### Problem Statement
Given `str1` and `str2`, find the minimum number of deletions and insertions to convert `str1` to `str2`.

#### Implementation Overview
- **Insight:** The Longest Common Subsequence is the part of `str1` that can be kept and reused to form `str2`.
    -   Characters in `str1` that are *not* in the LCS must be **deleted**.
    -   Characters in `str2` that are *not* in the LCS must be **inserted**.
- **Algorithm:**
    1.  Calculate `len_lcs = LCS(str1, str2)`.
    2.  Number of deletions = `len(str1) - len_lcs`.
    3.  Number of insertions = `len(str2) - len_lcs`.
    4.  Total operations = `deletions + insertions`.

#### Python Code Snippet
```python
def min_ops_to_convert(str1: str, str2: str) -> int:
    len_lcs = lcs_optimized(str1, str2) # Calculate the length of the Longest Common Subsequence.
    # Deletions = len(str1) - len_lcs. Insertions = len(str2) - len_lcs.
    # Total operations = (len(str1) - len_lcs) + (len(str2) - len_lcs)
    return len(str1) + len(str2) - 2 * len_lcs
```
#### Time and Space Complexity
- **Time Complexity:** Dominated by the LCS calculation ($O(NM)$).
- **Space Complexity:** Dominated by the LCS calculation ($O(min(N, M))$).

---

### 5. Shortest Common Supersequence
`[HARD]` `#lcs` `#string-dp` `#scs`

#### Problem Statement
Given `str1` and `str2`, return the shortest string that has both as subsequences.

#### Implementation Overview
- **Length Insight:** A naive supersequence is `str1 + str2`. To make it shortest, we should only include the common parts (the LCS) once. Thus, `len(SCS) = len(str1) + len(str2) - len(LCS)`.
- **Printing Algorithm:**
    1.  Compute the full LCS `dp` table.
    2.  Backtrack from `dp[n][m]` to build the SCS string.
        - If `str1[i-1] == str2[j-1]`, this character is common. Add it to the SCS once and move diagonally (`i--`, `j--`).
        - If they differ, find which subproblem gave the better LCS. If `dp[i-1][j]` was larger, it means `str1[i-1]` is unique to this path. Add it and move up (`i--`).
        - Otherwise, `str2[j-1]` is unique. Add it and move left (`j--`).
    3.  After the loop, append any remaining characters from the non-empty string.

#### Python Code Snippet
```python
def shortest_common_supersequence(str1: str, str2: str) -> str:
    n, m = len(str1), len(str2) # Get lengths of the strings.
    dp = [[0] * (m + 1) for _ in range(n + 1)] # Initialize DP table for LCS calculation.
    # Standard LCS table calculation to find the lengths of common subsequences.
    for i in range(1, n + 1): # Iterate through str1.
        for j in range(1, m + 1): # Iterate through str2.
            if str1[i-1] == str2[j-1]: # If characters match,
                dp[i][j] = 1 + dp[i-1][j-1] # Increment LCS length.
            else: # If they don't match,
                dp[i][j] = max(dp[i-1][j], dp[i][j-1]) # Take the max from top or left.

    # Backtrack from the end of the DP table to build the SCS string.
    res = [] # Result list to build the supersequence.
    i, j = n, m # Start from the bottom-right corner of the DP table.
    while i > 0 and j > 0: # Continue until one of the strings is fully processed.
        if str1[i-1] == str2[j-1]: # If characters are the same, they are part of the LCS.
            res.append(str1[i-1]) # Add the common character to the result.
            i -= 1; j -= 1 # Move diagonally up-left.
        elif dp[i-1][j] > dp[i][j-1]: # If the value from the top is greater,
            res.append(str1[i-1]) # Add the character from str1.
            i -= 1 # Move up.
        else: # Otherwise, the value from the left is greater or equal.
            res.append(str2[j-1]) # Add the character from str2.
            j -= 1 # Move left.

    # Append any remaining characters from str1 or str2.
    while i > 0: res.append(str1[i-1]); i -= 1 # If str1 has remaining characters.
    while j > 0: res.append(str2[j-1]); j -= 1 # If str2 has remaining characters.

    return "".join(reversed(res)) # Join the characters and reverse to get the final SCS.
```
#### Time and Space Complexity
- **Time Complexity:** O(n * m) to build the table.
- **Space Complexity:** O(n * m) for the DP table.
