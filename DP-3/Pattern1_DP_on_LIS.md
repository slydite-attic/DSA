# Pattern 1: DP on LIS (Longest Increasing Subsequence)

The Longest Increasing Subsequence (LIS) pattern is a fundamental DP concept used to find the longest subsequence of a given sequence where the elements are sorted in increasing order. A wide variety of problems can be solved by reducing them to LIS.

---

### 1. Longest Increasing Subsequence
`[MEDIUM]` `#lis` `#dp` `#binary-search`

#### Problem Statement
Given an integer array `nums`, return the length of the longest strictly increasing subsequence.

#### Recurrence Relation
Let `solve(index, prev_index)` be the length of the LIS from `nums[index...]` where the previous element chosen was at `prev_index`.
- **Choice 1 (Pick):** If `nums[index] > nums[prev_index]`, we can pick it. Length is `1 + solve(index + 1, index)`.
- **Choice 2 (Don't Pick):** We skip `nums[index]`. Length is `solve(index + 1, prev_index)`.
- We take the max of these choices. The state is `(index, prev_index)`, leading to an O(n^2) DP table.

---
#### a) Memoization (Top-Down O(n^2))
```python
def length_of_lis_memo(nums: list[int]) -> int:
    n = len(nums) # Get the number of elements.
    # DP table to store results. `prev_index + 1` is used to handle the -1 case.
    dp = [[-1] * (n + 1) for _ in range(n)]

    def solve(index, prev_index): # Recursive helper function.
        if index == n: # Base case: If we've considered all elements.
            return 0
        if dp[index][prev_index + 1] != -1: # If the result is memoized.
            return dp[index][prev_index + 1]

        # Case 1: Don't pick the current element.
        length = solve(index + 1, prev_index)

        # Case 2: Pick the current element (if it's greater than the previous).
        if prev_index == -1 or nums[index] > nums[prev_index]:
            length = max(length, 1 + solve(index + 1, index))

        dp[index][prev_index + 1] = length # Memoize the result.
        return length

    return solve(0, -1) # Start the recursion from the first element with no previous element.
```
- **Time Complexity:** O(n^2). Each state `dp[i][j]` is computed once.
- **Space Complexity:** O(n^2) for DP table + O(n) for recursion stack.

---
#### b) Tabulation (Bottom-Up O(n^2))
A more intuitive tabulation approach uses `dp[i]` to store the length of the LIS ending at index `i`.

```python
def length_of_lis_tab(nums: list[int]) -> int:
    n = len(nums) # Get the number of elements.
    if n == 0: return 0 # If the array is empty, the LIS length is 0.
    dp = [1] * n # Initialize a DP array where dp[i] stores the length of the LIS ending at index i.

    for i in range(n): # Iterate through each element as a potential end of a subsequence.
        for prev in range(i): # Iterate through all previous elements.
            if nums[i] > nums[prev]: # If the current element can extend the subsequence from the previous element,
                dp[i] = max(dp[i], 1 + dp[prev]) # Update the LIS length for the current element.

    return max(dp) # The result is the maximum value in the DP array.
```
- **Time Complexity:** O(n^2) for the nested loops.
- **Space Complexity:** O(n) for the DP array.

---
#### c) Advanced Solution (O(n log n) with Binary Search)
This approach maintains an auxiliary array `sub` which stores the smallest tail of all increasing subsequences of a given length.

```python
import bisect
def length_of_lis_optimized(nums: list[int]) -> int:
    sub = [] # This list stores the smallest tail of all increasing subsequences of a given length.
    for num in nums: # Iterate through each number in the input array.
        idx = bisect.bisect_left(sub, num) # Find the insertion point for 'num' to maintain sorted order.
        if idx == len(sub): # If 'num' is greater than all elements in 'sub',
            sub.append(num) # It extends the LIS, so we append it.
        else: # Otherwise, 'num' can replace an existing element
            sub[idx] = num # to form a new subsequence of the same length but with a smaller tail.
    return len(sub) # The length of 'sub' is the length of the LIS.
```
- **Time Complexity:** O(n log n). The loop runs n times, and each binary search (`bisect_left`) takes O(log n).
- **Space Complexity:** O(n) for the `sub` array.

---

### 2. Printing Longest Increasing Subsequence
`[MEDIUM]` `#lis` `#dp` `#backtracking`

#### Problem Statement
Given an integer array `nums`, find and print one of its longest increasing subsequences.

---
#### a) Memoization (Top-Down with Path Tracking)
We recursively compute the LIS paths and cache the lists of elements for each state `(index, prev_idx)`.
```python
def print_lis_memo(nums: list[int]) -> list[int]:
    n = len(nums)
    memo = {}

    def solve(index, prev_idx):
        if index == n:
            return []
        if (index, prev_idx) in memo:
            return memo[(index, prev_idx)]

        # Option 1: Skip nums[index]
        res = solve(index + 1, prev_idx)

        # Option 2: Pick nums[index] (if it extends the increasing subsequence)
        if prev_idx == -1 or nums[index] > nums[prev_idx]:
            picked = [nums[index]] + solve(index + 1, index)
            if len(picked) > len(res):
                res = picked

        memo[(index, prev_idx)] = res
        return res

    return solve(0, -1)
```
- **Time/Space Complexity:** O(n^2) states, but each state can store a list of size up to O(n), giving O(n^3) time/space.

---
#### b) Tabulation & Backtracking (Bottom-Up)
This is the standard approach, using a `parent` array to backtrack and reconstruct the LIS in O(n^2) time and O(n) space.
```python
def print_lis_tab(nums: list[int]) -> list[int]:
    n = len(nums)
    if n == 0: return []

    dp = [1] * n
    parent = [-1] * n
    max_len, last_idx = 0, 0

    for i in range(n):
        for j in range(i):
            if nums[i] > nums[j] and dp[i] < 1 + dp[j]:
                dp[i] = 1 + dp[j]
                parent[i] = j
        if dp[i] > max_len:
            max_len = dp[i]
            last_idx = i

    lis = []
    while last_idx != -1:
        lis.append(nums[last_idx])
        last_idx = parent[last_idx]

    return lis[::-1]
```
- **Time Complexity:** O(n^2) to compute and O(n) to backtrack.
- **Space Complexity:** O(n) for DP and parent tracking.

> **Note on Space Optimization:** Printing the LIS requires the `parent` array for backtracking — this is already O(n), which is the minimum required. The `dp` array is also O(n). No further space reduction is possible without losing the ability to reconstruct the path.

---

### 3. Largest Divisible Subset
`[MEDIUM]` `#lis-variant` `#dp`

#### Problem Statement
Given a set of distinct positive integers `nums`, return the largest subset where for every pair `(a, b)`, either `a % b == 0` or `b % a == 0`.

#### Recurrence Relation
By sorting the array first, the divisibility constraint simplifies: `nums[i]` only needs to be divisible by `nums[prev]`. This reduces the problem to an LIS variant.

---
#### a) Memoization (Top-Down with Path Tracking)
```python
def largest_divisible_subset_memo(nums: list[int]) -> list[int]:
    nums.sort()
    n = len(nums)
    memo = {}

    def solve(index, prev_idx):
        if index == n:
            return []
        if (index, prev_idx) in memo:
            return memo[(index, prev_idx)]

        # Option 1: Skip nums[index]
        res = solve(index + 1, prev_idx)

        # Option 2: Pick nums[index]
        if prev_idx == -1 or nums[index] % nums[prev_idx] == 0:
            picked = [nums[index]] + solve(index + 1, index)
            if len(picked) > len(res):
                res = picked

        memo[(index, prev_idx)] = res
        return res

    return solve(0, -1)
```
- **Time/Space Complexity:** O(n^3) due to storing lists in cache.

---
#### b) Tabulation & Backtracking (Bottom-Up)
```python
def largest_divisible_subset_tab(nums: list[int]) -> list[int]:
    n = len(nums)
    if n == 0: return []
    nums.sort()

    dp = [1] * n
    parent = [-1] * n
    max_len, last_idx = 1, 0

    for i in range(n):
        for j in range(i):
            if nums[i] % nums[j] == 0 and dp[i] < 1 + dp[j]:
                dp[i] = 1 + dp[j]
                parent[i] = j
        if dp[i] > max_len:
            max_len = dp[i]
            last_idx = i

    lds = []
    while last_idx != -1:
        lds.append(nums[last_idx])
        last_idx = parent[last_idx]

    return lds[::-1]
```
- **Time Complexity:** O(n^2).
- **Space Complexity:** O(n).

> **Note on Space Optimization:** This problem requires reconstructing the actual subset (not just its length), which necessitates the `parent` array for backtracking. The `dp` and `parent` arrays are both already O(n) — the minimum required. No further reduction is possible.

---

### 4. Longest String Chain
`[MEDIUM]` `#lis-variant` `#dp` `#string`

#### Problem Statement
Given `words`, find the length of the longest "word chain," where `word_i` is a predecessor of `word_{i+1}` (formed by deleting exactly one letter).

---
#### a) Memoization (Top-Down)
```python
def longest_str_chain_memo(words: list[str]) -> int:
    word_set = set(words)
    memo = {}

    def solve(word):
        if word in memo:
            return memo[word]

        max_chain = 1
        for i in range(len(word)):
            predecessor = word[:i] + word[i+1:]
            if predecessor in word_set:
                max_chain = max(max_chain, 1 + solve(predecessor))

        memo[word] = max_chain
        return max_chain

    return max(solve(word) for word in words) if words else 0
```
- **Time Complexity:** O(N * L^2) where N is the number of words and L is the max length of a word.
- **Space Complexity:** O(N * L) for recursion and cache.

---
#### b) Tabulation (Bottom-Up)
```python
def longest_str_chain_tab(words: list[str]) -> int:
    words.sort(key=len) # Sort by length so predecessors are computed first
    dp = {}
    max_chain = 0

    for word in words:
        current_len = 1
        for i in range(len(word)):
            predecessor = word[:i] + word[i+1:]
            if predecessor in dp:
                current_len = max(current_len, dp[predecessor] + 1)
        dp[word] = current_len
        max_chain = max(max_chain, current_len)

    return max_chain
```
- **Time Complexity:** O(N log N + N * L^2).
- **Space Complexity:** O(N * L) for the hash map.

> **Note on Space Optimization:** The tabulation naturally uses a hash map keyed by word string — each word is only needed once its shorter predecessors are computed (sorted by length). The space usage is already the minimum required: O(N) word entries. No further reduction is possible since we need all previously computed values.

---

### 5. Longest Bitonic Subsequence
`[MEDIUM]` `#lis-variant` `#dp`

#### Problem Statement
Find the length of the longest bitonic subsequence (first increasing, then decreasing).

---
#### a) Memoization (Top-Down LIS + LDS)
```python
def longest_bitonic_subsequence_memo(nums: list[int]) -> int:
    n = len(nums)
    if n == 0: return 0
    lis_memo = {}
    lds_memo = {}

    def get_lis(i):
        if i in lis_memo: return lis_memo[i]
        ans = 1
        for j in range(i):
            if nums[i] > nums[j]:
                ans = max(ans, 1 + get_lis(j))
        lis_memo[i] = ans
        return ans

    def get_lds(i):
        if i in lds_memo: return lds_memo[i]
        ans = 1
        for j in range(i + 1, n):
            if nums[i] > nums[j]:
                ans = max(ans, 1 + get_lds(j))
        lds_memo[i] = ans
        return ans

    max_bitonic = 0
    for i in range(n):
        max_bitonic = max(max_bitonic, get_lis(i) + get_lds(i) - 1)
    return max_bitonic
```
- **Time/Space Complexity:** O(n^2) time, O(n) space.

---
#### b) Tabulation (Bottom-Up LIS + LDS)
```python
def longest_bitonic_subsequence_tab(nums: list[int]) -> int:
    n = len(nums)
    if n == 0: return 0

    # dp1[i] = length of LIS ending at index i
    dp1 = [1] * n
    for i in range(n):
        for j in range(i):
            if nums[i] > nums[j]:
                dp1[i] = max(dp1[i], 1 + dp1[j])

    # dp2[i] = length of LDS (LIS from right) starting at index i
    dp2 = [1] * n
    for i in range(n - 1, -1, -1):
        for j in range(n - 1, i, -1):
            if nums[i] > nums[j]:
                dp2[i] = max(dp2[i], 1 + dp2[j])

    max_val = 0
    for i in range(n):
        # A valid bitonic point must have both an increasing and decreasing part
        if dp1[i] > 1 and dp2[i] > 1:
            max_val = max(max_val, dp1[i] + dp2[i] - 1)

    return max_val
```
- **Time Complexity:** O(n^2).
- **Space Complexity:** O(n).

> **Note on Space Optimization:** Both the LIS (`dp1`) and LDS (`dp2`) arrays of size n are required simultaneously to compute the final answer. There is no way to reduce below O(n) space — this tabulation already achieves the theoretical optimum for this approach.

---

### 6. Number of Longest Increasing Subsequences
`[MEDIUM]` `#lis-variant` `#dp` `#count`

#### Problem Statement
Given an array, return the number of longest increasing subsequences.

---
#### a) Memoization (Top-Down)
```python
def find_number_of_lis_memo(nums: list[int]) -> int:
    n = len(nums)
    if n <= 1: return n
    memo_len = {}
    memo_count = {}

    def solve(i):
        if i in memo_len:
            return memo_len[i], memo_count[i]

        max_l = 1
        max_c = 1
        for j in range(i):
            if nums[i] > nums[j]:
                length, count = solve(j)
                if length + 1 > max_l:
                    max_l = length + 1
                    max_c = count
                elif length + 1 == max_l:
                    max_c += count

        memo_len[i] = max_l
        memo_count[i] = max_c
        return max_l, max_c

    overall_max = 1
    for i in range(n):
        length, _ = solve(i)
        overall_max = max(overall_max, length)

    total_count = 0
    for i in range(n):
        length, count = solve(i)
        if length == overall_max:
            total_count += count

    return total_count
```
- **Time/Space Complexity:** O(n^2) time, O(n) space.

---
#### b) Tabulation (Bottom-Up)
```python
def find_number_of_lis_tab(nums: list[int]) -> int:
    n = len(nums)
    if n <= 1: return n

    length = [1] * n  # length[i] = length of LIS ending at i
    count = [1] * n   # count[i] = number of LIS of that length ending at i

    for i in range(n):
        for j in range(i):
            if nums[i] > nums[j]:
                if length[j] + 1 > length[i]:
                    length[i] = length[j] + 1
                    count[i] = count[j]
                elif length[j] + 1 == length[i]:
                    count[i] += count[j]

    max_len = max(length)
    result = 0
    for i in range(n):
        if length[i] == max_len:
            result += count[i]

    return result
```
- **Time Complexity:** O(n^2).
- **Space Complexity:** O(n).

> **Note on Space Optimization:** Both the `length` and `count` arrays (each O(n)) are needed simultaneously — `count[i]` depends on `count[j]` for all `j < i` with the same LIS length. There is no way to reduce below O(n) space. This tabulation already achieves the optimum.
