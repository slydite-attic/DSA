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

##### a) Memoization (Top-Down)
```python
def can_partition_memo(nums: list[int]) -> bool:
    total_sum = sum(nums)
    if total_sum % 2 != 0:
        return False
    target = total_sum // 2
    n = len(nums)
    dp = [[-1] * (target + 1) for _ in range(n)]

    def solve(index, t):
        if t == 0:
            return True
        if index == 0:
            return nums[0] == t
        if dp[index][t] != -1:
            return dp[index][t]

        not_pick = solve(index - 1, t)
        pick = False
        if nums[index] <= t:
            pick = solve(index - 1, t - nums[index])

        dp[index][t] = not_pick or pick
        return dp[index][t]

    return solve(n - 1, target)
```
- **Time Complexity:** O(n * total_sum).
- **Space Complexity:** O(n * total_sum) + O(n) recursion stack.

---
#### b) Tabulation (Bottom-Up)
```python
def can_partition_tab(nums: list[int]) -> bool:
    total_sum = sum(nums)
    if total_sum % 2 != 0:
        return False
    target = total_sum // 2
    n = len(nums)
    dp = [[False] * (target + 1) for _ in range(n)]

    for i in range(n):
        dp[i][0] = True

    if nums[0] <= target:
        dp[0][nums[0]] = True

    for i in range(1, n):
        for t in range(1, target + 1):
            not_pick = dp[i-1][t]
            pick = False
            if nums[i] <= t:
                pick = dp[i-1][t - nums[i]]
            dp[i][t] = not_pick or pick

    return dp[n-1][target]
```
- **Time/Space Complexity:** O(n * total_sum).

---
#### c) Space Optimization
```python
def can_partition_optimized(nums: list[int]) -> bool:
    total_sum = sum(nums)
    if total_sum % 2 != 0:
        return False
    target = total_sum // 2
    return subset_sum_optimized(nums, target)
```
- **Time Complexity:** O(n * total_sum).
- **Space Complexity:** O(total_sum).

---

### 3. Count Partitions with Given Difference
`[MEDIUM]` `#subset-sum` `#partition` `#count`

#### Problem Statement
Given an array and a difference `diff`, count the ways to partition it into two subsets `S1` and `S2` such that `sum(S1) - sum(S2) = diff`.

#### Recurrence Relation
This problem reduces to **Count Subsets with Sum K**.
- `sum(S1) - sum(S2) = diff` and `sum(S1) + sum(S2) = totalSum`
- Adding them gives `sum(S1) = (totalSum + diff) / 2`.
- Let `solve(index, target)` be the number of ways to form `target` using first `index` items.
- **`solve(index, target) = solve(index-1, target) + solve(index-1, target - nums[index])`**

---
#### a) Memoization (Top-Down)
```python
def count_partitions_memo(nums: list[int], diff: int) -> int:
    total_sum = sum(nums)
    if (total_sum + diff) % 2 != 0 or (total_sum + diff) < 0:
        return 0
    target = (total_sum + diff) // 2
    n = len(nums)
    dp = [[-1] * (target + 1) for _ in range(n)]

    def solve(index, t):
        if index == 0:
            if t == 0 and nums[0] == 0:
                return 2  # Pick or not pick the 0
            if t == 0 or nums[0] == t:
                return 1
            return 0
        if dp[index][t] != -1:
            return dp[index][t]

        not_pick = solve(index - 1, t)
        pick = 0
        if nums[index] <= t:
            pick = solve(index - 1, t - nums[index])

        dp[index][t] = not_pick + pick
        return dp[index][t]

    return solve(n - 1, target)
```
- **Time Complexity:** O(n * target).
- **Space Complexity:** O(n * target) + O(n) recursion stack.

---
#### b) Tabulation (Bottom-Up)
```python
def count_partitions_tab(nums: list[int], diff: int) -> int:
    total_sum = sum(nums)
    if (total_sum + diff) % 2 != 0 or (total_sum + diff) < 0:
        return 0
    target = (total_sum + diff) // 2
    n = len(nums)
    dp = [[0] * (target + 1) for _ in range(n)]

    # Base case for first element
    if nums[0] == 0:
        dp[0][0] = 2
    else:
        dp[0][0] = 1
        if nums[0] <= target:
            dp[0][nums[0]] = 1

    for i in range(1, n):
        for t in range(target + 1):
            not_pick = dp[i-1][t]
            pick = 0
            if nums[i] <= t:
                pick = dp[i-1][t - nums[i]]
            dp[i][t] = not_pick + pick

    return dp[n-1][target]
```
- **Time/Space Complexity:** O(n * target).

---
#### c) Space Optimization
```python
def count_partitions_optimized(nums: list[int], diff: int) -> int:
    total_sum = sum(nums)
    if (total_sum + diff) % 2 != 0 or (total_sum + diff) < 0:
        return 0
    target = (total_sum + diff) // 2
    dp = [0] * (target + 1)
    dp[0] = 1
    if nums[0] != 0 and nums[0] <= target:
        dp[nums[0]] = 1
    elif nums[0] == 0:
        dp[0] = 2

    for i in range(1, len(nums)):
        for t in range(target, nums[i] - 1, -1):
            dp[t] += dp[t - nums[i]]
    return dp[target]
```
- **Time Complexity:** O(n * target).
- **Space Complexity:** O(target).

---

### 4. Partition a set into two subsets with minimum absolute sum difference
`[HARD]` `#dynamicprogramming` `#subsetsum`

#### Problem Statement
Given an array of integers `arr`, partition it into two subsets `S1` and `S2` such that the absolute difference of their sums, i.e., `|sum(S1) - sum(S2)|`, is minimized. Return the minimum absolute sum difference.

---
#### a) Memoization (Top-Down)
```python
def min_subset_sum_difference_memo(arr: list[int]) -> int:
    n = len(arr)
    total_sum = sum(arr)
    target = total_sum // 2
    dp = [[-1] * (target + 1) for _ in range(n)]

    def solve(index, t):
        if t == 0:
            return True
        if index == 0:
            return arr[0] == t
        if dp[index][t] != -1:
            return dp[index][t]

        not_pick = solve(index - 1, t)
        pick = False
        if arr[index] <= t:
            pick = solve(index - 1, t - arr[index])

        dp[index][t] = not_pick or pick
        return dp[index][t]

    # Find the largest subset sum achievable <= total_sum // 2
    s1 = 0
    for t in range(target, -1, -1):
        if solve(n - 1, t):
            s1 = t
            break

    return total_sum - 2 * s1
```
- **Time Complexity:** O(n * total_sum).
- **Space Complexity:** O(n * total_sum) + O(n) recursion stack.

---
#### b) Tabulation (Bottom-Up)
```python
def min_subset_sum_difference_tab(arr: list[int]) -> int:
    n = len(arr)
    total_sum = sum(arr)
    target = total_sum // 2
    dp = [[False] * (target + 1) for _ in range(n)]

    for i in range(n):
        dp[i][0] = True
    if arr[0] <= target:
        dp[0][arr[0]] = True

    for i in range(1, n):
        for t in range(1, target + 1):
            not_pick = dp[i-1][t]
            pick = False
            if arr[i] <= t:
                pick = dp[i-1][t - arr[i]]
            dp[i][t] = not_pick or pick

    s1 = 0
    for t in range(target, -1, -1):
        if dp[n-1][t]:
            s1 = t
            break

    return total_sum - 2 * s1
```
- **Time/Space Complexity:** O(n * total_sum).

---
#### c) Space Optimization
```python
def min_subset_sum_difference_optimized(arr: list[int]) -> int:
    n = len(arr)
    total_sum = sum(arr)
    target = total_sum // 2
    dp = [False] * (target + 1)
    dp[0] = True
    if arr[0] <= target:
        dp[arr[0]] = True

    for i in range(1, n):
        for j in range(target, arr[i] - 1, -1):
            dp[j] = dp[j] or dp[j - arr[i]]

    s1 = 0
    for j in range(target, -1, -1):
        if dp[j]:
            s1 = j
            break
    return total_sum - 2 * s1
```
- **Time Complexity:** O(n * total_sum).
- **Space Complexity:** O(total_sum).

---

### 5. Count Subsets with Sum K
`[MEDIUM]` `#dynamicprogramming` `#subsetsum`

#### Problem Statement
Given an array `arr` of size `n` and a target sum `k`, count the number of subsets whose sum is equal to `k`.

---
#### a) Memoization (Top-Down)
```python
def find_ways_memo(arr: list[int], k: int) -> int:
    n = len(arr)
    dp = [[-1] * (k + 1) for _ in range(n)]

    def solve(index, t):
        if index == 0:
            if t == 0 and arr[0] == 0:
                return 2
            if t == 0 or arr[0] == t:
                return 1
            return 0
        if dp[index][t] != -1:
            return dp[index][t]

        not_pick = solve(index - 1, t)
        pick = 0
        if arr[index] <= t:
            pick = solve(index - 1, t - arr[index])

        dp[index][t] = not_pick + pick
        return dp[index][t]

    return solve(n - 1, k)
```
- **Time Complexity:** O(n * k).
- **Space Complexity:** O(n * k) + O(n) recursion stack.

---
#### b) Tabulation (Bottom-Up)
```python
def find_ways_tab(arr: list[int], k: int) -> int:
    n = len(arr)
    dp = [[0] * (k + 1) for _ in range(n)]

    if arr[0] == 0:
        dp[0][0] = 2
    else:
        dp[0][0] = 1
        if arr[0] <= k:
            dp[0][arr[0]] = 1

    for i in range(1, n):
        for t in range(k + 1):
            not_pick = dp[i-1][t]
            pick = 0
            if arr[i] <= t:
                pick = dp[i-1][t - arr[i]]
            dp[i][t] = not_pick + pick

    return dp[n-1][k]
```
- **Time/Space Complexity:** O(n * k).

---
#### c) Space Optimization
```python
def find_ways_optimized(arr: list[int], k: int) -> int:
    dp = [0] * (k + 1)
    dp[0] = 1
    if arr[0] != 0 and arr[0] <= k:
        dp[arr[0]] = 1
    elif arr[0] == 0:
        dp[0] = 2

    for i in range(1, len(arr)):
        for j in range(k, arr[i] - 1, -1):
            dp[j] = dp[j] + dp[j - arr[i]]
    return dp[k]
```
- **Time Complexity:** O(n * k).
- **Space Complexity:** O(k).

---

### 6. Target Sum
`[MEDIUM]` `#dynamicprogramming` `#subsetsum` `#partition` `#target-sum`

#### Problem Statement
Given an array of integers `arr` and a target integer `target`, count the number of ways to assign `+` and `-` signs to each integer to make the expression evaluate to `target`.

#### Recurrence Relation
This is equivalent to dividing the array into two subsets `S1` (positive elements) and `S2` (negative elements) such that `sum(S1) - sum(S2) = target`.
- `sum(S1) - sum(S2) = target` and `sum(S1) + sum(S2) = total_sum`
- Subtracting them gives `2 * sum(S2) = total_sum - target`, or `sum(S2) = (total_sum - target) / 2`.
- Let `k = (total_sum - target) / 2`. If `total_sum - target < 0` or is odd, return 0.
- The problem reduces to finding the number of subsets with sum `k`.

---
#### a) Memoization (Top-Down)
```python
def target_sum_memo(arr: list[int], target: int) -> int:
    total_sum = sum(arr)
    if (total_sum - target) % 2 != 0 or (total_sum - target) < 0:
        return 0
    k = (total_sum - target) // 2
    n = len(arr)
    dp = [[-1] * (k + 1) for _ in range(n)]

    def solve(index, t):
        if index == 0:
            if t == 0 and arr[0] == 0:
                return 2
            if t == 0 or arr[0] == t:
                return 1
            return 0
        if dp[index][t] != -1:
            return dp[index][t]

        not_pick = solve(index - 1, t)
        pick = 0
        if arr[index] <= t:
            pick = solve(index - 1, t - arr[index])

        dp[index][t] = not_pick + pick
        return dp[index][t]

    return solve(n - 1, k)
```
- **Time Complexity:** O(n * k).
- **Space Complexity:** O(n * k) + O(n) recursion stack.

---
#### b) Tabulation (Bottom-Up)
```python
def target_sum_tab(arr: list[int], target: int) -> int:
    total_sum = sum(arr)
    if (total_sum - target) % 2 != 0 or (total_sum - target) < 0:
        return 0
    k = (total_sum - target) // 2
    n = len(arr)
    dp = [[0] * (k + 1) for _ in range(n)]

    if arr[0] == 0:
        dp[0][0] = 2
    else:
        dp[0][0] = 1
        if arr[0] <= k:
            dp[0][arr[0]] = 1

    for i in range(1, n):
        for t in range(k + 1):
            not_pick = dp[i-1][t]
            pick = 0
            if arr[i] <= t:
                pick = dp[i-1][t - arr[i]]
            dp[i][t] = not_pick + pick

    return dp[n-1][k]
```
- **Time/Space Complexity:** O(n * k).

---
#### c) Space Optimization
```python
def target_sum_optimized(arr: list[int], target: int) -> int:
    total_sum = sum(arr)
    if (total_sum - target) % 2 != 0 or (total_sum - target) < 0:
        return 0
    k = (total_sum - target) // 2
    dp = [0] * (k + 1)
    dp[0] = 1
    if arr[0] != 0 and arr[0] <= k:
        dp[arr[0]] = 1
    elif arr[0] == 0:
        dp[0] = 2

    for i in range(1, len(arr)):
        for j in range(k, arr[i] - 1, -1):
            dp[j] = dp[j] + dp[j - arr[i]]
    return dp[k]
```
- **Time Complexity:** O(n * k).
- **Space Complexity:** O(k).
