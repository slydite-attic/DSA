# Pattern 1: Subset Sum & Partition DP

This pattern is a cornerstone of Dynamic Programming, often called **0/1 Knapsack** style problems. The fundamental idea is, for each element, we have two choices: either **include it** in our subset or **not include it**. This binary choice structure forms the basis of the recurrence relation. These problems typically ask for the existence of a subset with a certain property, the count of such subsets, or the optimal partition of a set.

---

### 1. Subset Sum Equal to Target
`[MEDIUM]` `#subset-sum` `#0-1-knapsack`

#### Problem Statement
Given a set of non-negative integers `nums` and a value `k`, determine if there is a subset of the given set with a sum equal to `k`.

#### Recurrence Relation
Let `solve(index, target)` be a function that returns true if a subset summing to `target` can be formed using elements from `nums[0...index]`.
- **Choice 1 (Don't Pick):** If we don't pick `nums[index]`, we need to see if the target can be formed from the remaining elements: `solve(index - 1, target)`.
- **Choice 2 (Pick):** If we pick `nums[index]`, we need to see if `target - nums[index]` can be formed from the remaining elements: `solve(index - 1, target - nums[index])`.
- **`solve(index, target) = solve(index-1, target) OR solve(index-1, target - nums[index])`**
- **Base Case:** `target == 0` is always true. `index < 0` is false if target isn't 0.

---
#### a) Memoization (Top-Down)
```python
def subset_sum_memo(nums: list[int], k: int) -> bool:
    n = len(nums) # Get the number of elements in the input list.
    dp = [[-1] * (k + 1) for _ in range(n)] # Initialize a memoization table with -1 to store results of subproblems.

    def solve(index, target): # Recursive helper function to solve the problem for a given index and target sum.
        if target == 0: # Base case: If the target sum is 0, we've found a valid subset.
            return True
        if index == 0: # Base case: If we're at the first element, check if it equals the target.
            return nums[0] == target
        if dp[index][target] != -1: # If the result for this state is already computed, return it.
            return dp[index][target]

        not_pick = solve(index - 1, target) # Case 1: Don't include the current element in the subset.
        pick = False # Initialize the 'pick' case to False.
        if nums[index] <= target: # If the current element is not greater than the target,
            pick = solve(index - 1, target - nums[index]) # Case 2: Include the current element.

        dp[index][target] = not_pick or pick # Store the result of the current state in the memoization table.
        return dp[index][target] # Return the computed result.

    return solve(n - 1, k) # Start the recursion from the last element with the initial target sum.
```
- **Time Complexity:** O(n * k). Each state `dp[i][j]` is computed once.
- **Space Complexity:** O(n * k) for the DP table + O(n) for recursion stack.

---
#### b) Tabulation (Bottom-Up)
```python
def subset_sum_tab(nums: list[int], k: int) -> bool:
    n = len(nums) # Get the number of elements in the list.
    dp = [[False] * (k + 1) for _ in range(n)] # Initialize a 2D DP table to store boolean values.

    # Base case: A target sum of 0 is always possible (by choosing no elements).
    for i in range(n): # Iterate through each row (representing each item).
        dp[i][0] = True # Set the first column to True.

    if nums[0] <= k: # If the first element is within the target bound,
        dp[0][nums[0]] = True # Mark it as achievable in the first row.

    for i in range(1, n): # Iterate through the elements of the list, starting from the second one.
        for target in range(1, k + 1): # Iterate through all possible target sums.
            not_pick = dp[i-1][target] # The result if we don't pick the current element is the same as the result from the previous element.
            pick = False # Initialize the 'pick' case to False.
            if nums[i] <= target: # If the current element is not greater than the target,
                pick = dp[i-1][target - nums[i]] # Check if the remaining target was achievable with the previous elements.
            dp[i][target] = not_pick or pick # The current state is true if either 'pick' or 'not_pick' is true.

    return dp[n-1][k] # Return the result for the last element and the initial target sum.
```
- **Time Complexity:** O(n * k).
- **Space Complexity:** O(n * k).

---
#### c) Space Optimization
```python
def subset_sum_optimized(nums: list[int], k: int) -> bool:
    n = len(nums) # Get the number of elements in the list.
    prev_row = [False] * (k + 1) # Initialize a single row to store the results of the previous row in the DP table.
    prev_row[0] = True # Base case: A target sum of 0 is always possible.

    if nums[0] <= k: # If the first element is within the target bound,
        prev_row[nums[0]] = True # Mark it as achievable.

    for i in range(1, n): # Iterate through the elements of the list, starting from the second one.
        # Iterate backwards to use the results from the 'previous' row (i-1)
        # before they are overwritten in this pass.
        for target in range(k, nums[i] - 1, -1): # Iterate backwards from the target sum down to the current number.
            not_pick = prev_row[target] # The result if we don't pick the current element.
            pick = prev_row[target - nums[i]] # The result if we pick the current element.
            prev_row[target] = not_pick or pick # Update the current target's status.

    return prev_row[k] # Return the result for the initial target sum.
```
- **Time Complexity:** O(n * k).
- **Space Complexity:** O(k).

---

### 2. Partition Equal Subset Sum
`[MEDIUM]` `#subset-sum` `#partition`

#### Problem Statement
Given an array `nums`, find if it can be partitioned into two subsets with equal sums.

#### Implementation Overview
This is a direct application of Subset Sum. If the array can be partitioned into two equal sum subsets, the sum of each subset must be `total_sum / 2`.
1.  Calculate `total_sum`. If it's odd, return `False`.
2.  The problem becomes: find if there is a subset with sum equal to `target = total_sum / 2`.
3.  Use any of the Subset Sum solutions above.

#### Python Code Snippet (using optimized Subset Sum)
```python
def can_partition(nums: list[int]) -> bool:
    total_sum = sum(nums) # Calculate the total sum of the elements in the list.
    if total_sum % 2 != 0: # If the total sum is odd, it's impossible to partition it into two equal halves.
        return False # So, return False.

    return subset_sum_optimized(nums, total_sum // 2) # The problem is now reduced to finding if a subset sums up to half of the total sum.
```
- **Time Complexity:** O(n * total_sum).
- **Space Complexity:** O(total_sum).

---

### 3. Count Partitions with Given Difference
`[MEDIUM]` `#subset-sum` `#partition` `#count`

#### Problem Statement
Given an array and a difference `diff`, count the ways to partition it into two subsets `S1` and `S2` such that `sum(S1) - sum(S2) = diff`.

#### Implementation Overview
This problem reduces to **Count Subsets with Sum K**.
1.  We have two equations:
    - `sum(S1) - sum(S2) = diff`
    - `sum(S1) + sum(S2) = totalSum`
2.  Adding them gives `2 * sum(S1) = totalSum + diff`, so `sum(S1) = (totalSum + diff) / 2`.
3.  The problem is now to count the number of subsets that sum to this `target = (totalSum + diff) / 2`.
4.  This requires a counting version of the subset sum DP. Let `dp[j]` be the number of ways to make sum `j`. The recurrence is `dp[j] = dp[j] + dp[j - num]`.

#### Python Code Snippet
```python
def count_partitions_with_diff(nums: list[int], diff: int) -> int:
    total_sum = sum(nums) # Calculate the total sum of all numbers in the list.

    # Edge cases: if the target sum is not an integer or is negative, no solution exists.
    if (total_sum + diff) % 2 != 0 or (total_sum + diff) < 0:
        return 0 # Return 0 as no such partitions are possible.

    target = (total_sum + diff) // 2 # Calculate the target sum for one of the subsets.

    # Count subsets with sum = target
    dp = [0] * (target + 1) # Initialize a DP array to store the number of ways to achieve each sum.
    dp[0] = 1 # Base case: there is one way to make a sum of 0 (by choosing an empty set).
    for num in nums: # Iterate through each number in the input list.
        for j in range(target, num - 1, -1): # Iterate backwards from the target down to the current number.
            dp[j] += dp[j - num] # Update the number of ways to form sum 'j' by adding the ways to form 'j - num'.

    return dp[target] # The result is the number of ways to form the target sum.
```
- **Time Complexity:** O(n * target).
- **Space Complexity:** O(target).
- **Related Problem:** The **Target Sum** problem is an identical variation.

---

### 4. Partition a set into two subsets with minimum absolute sum difference
`[HARD]` `#dynamicprogramming` `#subsetsum`

#### Problem Statement
Given an array of integers `arr`, partition it into two subsets `S1` and `S2` such that the absolute difference of their sums, i.e., `|sum(S1) - sum(S2)|`, is minimized. Return the minimum absolute sum difference.

*Example:*
- **Input:** `arr = [1, 6, 11, 5]`
- **Output:** `1`
- **Explanation:** Subset 1 = [1, 5, 6], sum = 12; Subset 2 = [11], sum = 11. Difference = |12-11| = 1.

#### Implementation Overview
We use the subset sum DP logic.
1. Compute `total_sum = sum(arr)`. Our goal is to find if any subset sum in range `[0, total_sum // 2]` is possible.
2. Find the largest sum `s1 <= total_sum // 2` which is possible.
3. The other subset sum will be `s2 = total_sum - s1`.
4. The minimum difference is `s2 - s1 = total_sum - 2*s1`.

#### Python Code Snippet
```python
def minSubsetSumDifference(arr):
    n = len(arr)
    total_sum = sum(arr)
    target = total_sum // 2
    dp = [False] * (target + 1)
    dp[0] = True
    for num in arr:
        for j in range(target, num - 1, -1):
            dp[j] = dp[j] or dp[j - num]
            
    s1 = 0
    for j in range(target, -1, -1):
        if dp[j]:
            s1 = j
            break
    return total_sum - 2 * s1
```

---

### 5. Count Subsets with Sum K
`[MEDIUM]` `#dynamicprogramming` `#subsetsum`

#### Problem Statement
Given an array `arr` of size `n` and a target sum `k`, count the number of subsets whose sum is equal to `k`.

*Example:*
- **Input:** `arr = [1, 2, 2, 3]`, `k = 3`
- **Output:** `3`
- **Explanation:** The subsets are [1, 2], [1, 2], and [3].

#### Python Code Snippet
```python
def findWays(arr, k):
    dp = [0] * (k + 1)
    dp[0] = 1
    for num in arr:
        for j in range(k, num - 1, -1):
            dp[j] = (dp[j] + dp[j - num])
    return dp[k]
```
