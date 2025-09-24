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

#### Implementation Overview
This requires the O(n^2) tabulation approach, augmented with a `parent` array to reconstruct the path.
1.  Use the O(n^2) tabulation to fill a `dp` array (`dp[i]` = LIS length ending at `i`).
2.  While filling `dp`, also fill a `parent` array. When `dp[i]` is updated by `1 + dp[j]`, set `parent[i] = j`.
3.  Find the index `last_idx` where the maximum value in `dp` occurs. This is the end of an LIS.
4.  Backtrack from `last_idx` using the `parent` array to reconstruct the LIS.

#### Python Code Snippet
```python
def print_lis(nums: list[int]) -> list[int]:
    n = len(nums) # Get the number of elements.
    if n == 0: return [] # Return empty list for empty input.

    dp = [1] * n # dp[i] will store the length of the LIS ending at index i.
    parent = [-1] * n # parent[i] will store the index of the previous element in the LIS ending at i.
    max_len, last_idx = 0, 0 # To track the length and the last index of the overall LIS.

    for i in range(n): # Iterate through each element.
        for j in range(i): # Iterate through previous elements.
            if nums[i] > nums[j] and dp[i] < 1 + dp[j]: # If we can extend a subsequence,
                dp[i] = 1 + dp[j] # Update the length.
                parent[i] = j # And set the parent to reconstruct the path later.
        if dp[i] > max_len: # If we've found a new longest subsequence,
            max_len = dp[i] # Update the max length.
            last_idx = i # And store its last index.

    lis = [] # The list to store the reconstructed LIS.
    while last_idx != -1: # Backtrack from the last index of the LIS.
        lis.append(nums[last_idx]) # Add the element to our list.
        last_idx = parent[last_idx] # Move to the parent element.

    return lis[::-1] # Reverse the list to get the correct order.
```
- **Time Complexity:** O(n^2).
- **Space Complexity:** O(n).

---

### 3. Largest Divisible Subset
`[MEDIUM]` `#lis-variant` `#dp`

#### Problem Statement
Given a set of distinct positive integers `nums`, return the largest subset where for every pair `(a, b)`, either `a % b == 0` or `b % a == 0`.

#### Implementation Overview
This is an LIS variation. The "increasing" property is replaced by a "divisibility" property.
1.  **Sort `nums`**. This is crucial. Now we only need to check `nums[i] % nums[j] == 0` for `j < i`.
2.  The problem becomes finding the longest subsequence where each element is divisible by the previous one.
3.  This is structurally identical to "Printing LIS". Use the same O(n^2) DP approach with the parent tracking.

#### Python Code Snippet
```python
def largest_divisible_subset(nums: list[int]) -> list[int]:
    n = len(nums) # Get the number of elements.
    if n == 0: return [] # Return empty list for empty input.
    nums.sort() # Sort the array to ensure that if `nums[i]` is divisible by `nums[j]`, then `j < i`.

    dp = [1] * n # dp[i] stores the size of the largest divisible subset ending with nums[i].
    parent = [-1] * n # To reconstruct the subset.
    max_len, last_idx = 1, 0 # To track the size and end of the largest subset.

    for i in range(n): # For each element,
        for j in range(i): # Check all previous elements.
            # If nums[i] is divisible by nums[j] and we can form a larger subset,
            if nums[i] % nums[j] == 0 and dp[i] < 1 + dp[j]:
                dp[i] = 1 + dp[j] # Update the size.
                parent[i] = j # Set the parent.
        if dp[i] > max_len: # If we found a new largest subset,
            max_len = dp[i] # Update the max length.
            last_idx = i # And its last index.

    lds = [] # List to store the result.
    while last_idx != -1: # Backtrack from the end of the largest subset.
        lds.append(nums[last_idx]) # Add the element.
        last_idx = parent[last_idx] # Move to the parent.

    return lds[::-1] # Reverse to get the correct order.
```
- **Time Complexity:** O(n^2).
- **Space Complexity:** O(n).

---

### 4. Longest String Chain
`[MEDIUM]` `#lis-variant` `#dp` `#string`

#### Problem Statement
Given `words`, find the length of the longest "word chain," where `word_i` is a predecessor of `word_{i+1}` (formed by deleting one letter).

#### Implementation Overview
1.  **Sort `words` by length**. This ensures we process potential predecessors before their successors.
2.  **DP State:** `dp[word]` = length of the longest chain ending with `word`. A hash map is ideal for this.
3.  **Recurrence:** For each `word`, generate all its possible predecessors by deleting one character. The longest chain for `word` is `1 + max(dp[predecessor])` over all valid predecessors found in the map.

#### Python Code Snippet
```python
def longest_str_chain(words: list[str]) -> int:
    words.sort(key=len) # Sort words by length to ensure we process predecessors before their successors.
    dp = {} # A dictionary to store the length of the longest chain ending with a particular word.
    max_chain = 0 # To keep track of the overall maximum chain length found.

    for word in words: # Iterate through each word in the sorted list.
        current_len = 1 # The minimum chain length for any word is 1 (the word itself).
        # Generate all possible predecessors by deleting one character at a time.
        for i in range(len(word)):
            predecessor = word[:i] + word[i+1:] # Create a potential predecessor.
            if predecessor in dp: # If this predecessor exists in our DP map,
                # Update the current word's chain length if we found a longer chain through this predecessor.
                current_len = max(current_len, dp[predecessor] + 1)
        dp[word] = current_len # Store the calculated max chain length for the current word.
        max_chain = max(max_chain, current_len) # Update the overall max chain length.

    return max_chain # Return the final result.
```
- **Time Complexity:** O(N * L^2), where N is the number of words and L is the max word length. Sorting is O(N log N).
- **Space Complexity:** O(N * L) to store the DP map.

---

### 5. Longest Bitonic Subsequence
`[MEDIUM]` `#lis-variant` `#dp`

#### Problem Statement
Find the length of the longest bitonic subsequence (first increasing, then decreasing).

#### Implementation Overview
A bitonic subsequence has a "peak". We can find the longest one by considering every element as a potential peak.
1.  **`dp1[i]`**: Length of the LIS ending at `i` (calculated from left-to-right).
2.  **`dp2[i]`**: Length of the Longest Decreasing Subsequence (LDS) starting at `i` (or LIS from right-to-left).
3.  For each `i`, a bitonic sequence with `nums[i]` as the peak has length `dp1[i] + dp2[i] - 1`. The `-1` is because `nums[i]` is counted in both.
4.  The answer is the maximum of this value over all `i`.

#### Python Code Snippet
```python
def longest_bitonic_subsequence(nums: list[int]) -> int:
    n = len(nums) # Get the number of elements.
    if n == 0: return 0 # Return 0 for an empty array.

    # dp1[i] stores the length of the Longest Increasing Subsequence ending at index i.
    dp1 = [1] * n
    for i in range(n): # Iterate from left to right.
        for j in range(i):
            if nums[i] > nums[j]:
                dp1[i] = max(dp1[i], 1 + dp1[j])

    # dp2[i] stores the length of the Longest Increasing Subsequence starting from index i (or LDS ending at i).
    dp2 = [1] * n
    for i in range(n - 1, -1, -1): # Iterate from right to left.
        for j in range(n - 1, i, -1):
            if nums[i] > nums[j]:
                dp2[i] = max(dp2[i], 1 + dp2[j])

    max_val = 0 # To store the maximum length of the bitonic subsequence.
    for i in range(n): # Iterate through all possible peaks.
        # The length of the bitonic subsequence with peak at i is the sum of the increasing part
        # and the decreasing part, with the peak counted once.
        max_val = max(max_val, dp1[i] + dp2[i] - 1)

    return max_val # Return the overall maximum length found.
```
- **Time Complexity:** O(n^2) due to the two nested loops for calculating `dp1` and `dp2`.
- **Space Complexity:** O(n) for the two DP arrays.

---

### 6. Number of Longest Increasing Subsequences
`[MEDIUM]` `#lis-variant` `#dp` `#count`

#### Problem Statement
Given an array, return the number of longest increasing subsequences.

#### Implementation Overview
We need to track not just the length of LIS ending at `i`, but also the count of such subsequences.
- **DP State:**
    - `length[i]`: The length of the LIS ending at `nums[i]`.
    - `count[i]`: The number of distinct LIS that end at `nums[i]`.
- **Recurrence:** For each `i`, iterate `j` from `0` to `i-1`:
    - If `nums[i] > nums[j]`:
        - If `length[j] + 1 > length[i]`: We've found a new, longer LIS. Update `length[i]` and reset the count: `count[i] = count[j]`.
        - If `length[j] + 1 == length[i]`: We've found another LIS of the same max length. Add its ways: `count[i] += count[j]`.
- **Final Answer:** Find the `max_len` across the `length` array. The answer is the sum of `count[k]` for all `k` where `length[k] == max_len`.

#### Python Code Snippet
```python
def find_number_of_lis(nums: list[int]) -> int:
    n = len(nums) # Get the number of elements.
    if n <= 1: return n # If there's 0 or 1 element, the number of LIS is n.

    length = [1] * n # `length[i]` stores the length of the LIS ending at index `i`.
    count = [1] * n  # `count[i]` stores the number of LIS ending at index `i`.

    for i in range(n): # Iterate through each element as the end of a potential LIS.
        for j in range(i): # Iterate through all previous elements.
            if nums[i] > nums[j]: # If the current element can extend the subsequence from the previous one.
                if length[j] + 1 > length[i]: # If we found a longer LIS.
                    length[i] = length[j] + 1 # Update the length.
                    count[i] = count[j] # The count is inherited from the previous subsequence.
                elif length[j] + 1 == length[i]: # If we found another LIS of the same length.
                    count[i] += count[j] # Add the number of ways from the previous subsequence.

    max_len = max(length) # Find the maximum length of any LIS.
    result = 0 # To store the total count of all LIS.
    for i in range(n): # Iterate through the length and count arrays.
        if length[i] == max_len: # If an LIS ending at index `i` has the maximum length,
            result += count[i] # Add its count to the total result.

    return result # Return the total count.
```
- **Time Complexity:** O(n^2).
- **Space Complexity:** O(n).
