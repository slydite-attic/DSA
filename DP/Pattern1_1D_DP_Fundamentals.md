# Pattern 1: 1D DP Fundamentals

This pattern introduces the core concepts of Dynamic Programming (DP) and applies them to problems that can be solved using a one-dimensional state. These problems are foundational for understanding how to identify DP patterns, formulate recurrence relations, and apply optimization techniques.

---

### 1. Dynamic Programming Introduction
`[FUNDAMENTAL]` `[EASY]` `#concept` `#memoization` `#tabulation`

#### Concept Overview
**Dynamic Programming** is an algorithmic technique for solving optimization problems by breaking them down into simpler, overlapping subproblems. By solving each subproblem only once and storing its result, DP avoids redundant computations.

A problem is suitable for DP if it has two key attributes:
1.  **Optimal Substructure:** An optimal solution to the problem can be constructed from optimal solutions to its subproblems.
2.  **Overlapping Subproblems:** The problem can be broken down into subproblems that are reused several times.

**Two Main DP Techniques:**
1.  **Memoization (Top-Down):** This approach uses recursion. The function is written as a standard recursive solution, but the results of each subproblem are stored in a cache (e.g., a hash map or an array, often called `dp`). Before computing, the function checks the cache. If the result exists, it's returned immediately. Otherwise, the result is computed, stored in the cache, and then returned. It solves subproblems as they are needed.

2.  **Tabulation (Bottom-Up):** This approach is iterative. It solves the problem by filling a DP table, starting with the smallest possible subproblems and building up to the solution for the original problem. This avoids recursion and the potential for stack overflow errors.

---

### 2. Climbing Stairs
`[EASY]` `#1D-DP` `#fibonacci`

#### Problem Statement
You are climbing a staircase that takes `n` steps to reach the top. Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?

#### Recurrence Relation
Let `ways(i)` be the number of ways to reach step `i`. To get to step `i`, you must have come from either step `i-1` or step `i-2`.
- **`ways(i) = ways(i-1) + ways(i-2)`**
- **Base Cases:** `ways(0) = 1` (one way to be at the start), `ways(1) = 1` (one way to take one step).

This is the Fibonacci sequence.

---
#### a) Memoization (Top-Down)
We create a recursive function that uses a `dp` array to store the results for each step `n`.

```python
def climb_stairs_memo(n: int) -> int:
    dp = [-1] * (n + 1)

    def solve(step):
        if step <= 1:
            return 1
        if dp[step] != -1:
            return dp[step]

        dp[step] = solve(step - 1) + solve(step - 2)
        return dp[step]

    return solve(n)
```
- **Time Complexity:** O(n). Each state `dp[i]` is computed only once.
- **Space Complexity:** O(n) for the `dp` array + O(n) for the recursion stack depth.

---
#### b) Tabulation (Bottom-Up)
We fill a `dp` array from the base cases up to `n`.

```python
def climb_stairs_tab(n: int) -> int:
    if n <= 1:
        return 1
    dp = [0] * (n + 1)
    dp[0] = 1
    dp[1] = 1

    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]

    return dp[n]
```
- **Time Complexity:** O(n) due to the single loop.
- **Space Complexity:** O(n) for the `dp` array.

---
#### c) Space Optimization
Since the calculation for `dp[i]` only depends on `dp[i-1]` and `dp[i-2]`, we only need to store the two previous results.

```python
def climb_stairs_optimized(n: int) -> int:
    if n <= 1:
        return 1

    prev2 = 1  # ways to reach step 0
    prev1 = 1  # ways to reach step 1

    for i in range(2, n + 1):
        current = prev1 + prev2
        prev2 = prev1
        prev1 = current

    return prev1
```
- **Time Complexity:** O(n).
- **Space Complexity:** O(1).

---

### 3. Frog Jump
`[EASY]` `#1D-DP`

#### Problem Statement
A frog must jump from stone 0 to `N-1`. The cost of a jump from stone `i` to `j` is `abs(heights[i] - heights[j])`. The frog can jump from `i` to `i+1` or `i+2`. Find the minimum energy cost.

#### Recurrence Relation
Let `dp[i]` be the minimum energy to reach stone `i`.
- **`dp[i] = min(dp[i-1] + abs(h[i]-h[i-1]), dp[i-2] + abs(h[i]-h[i-2]))`**
- **Base Case:** `dp[0] = 0`.

---
#### a) Memoization (Top-Down)
```python
def frog_jump_memo(heights: list[int]) -> int:
    n = len(heights)
    dp = [-1] * n

    def solve(index):
        if index == 0:
            return 0
        if dp[index] != -1:
            return dp[index]

        jump1 = solve(index - 1) + abs(heights[index] - heights[index - 1])
        jump2 = float('inf')
        if index > 1:
            jump2 = solve(index - 2) + abs(heights[index] - heights[index - 2])

        dp[index] = min(jump1, jump2)
        return dp[index]

    return solve(n - 1)
```
- **Time Complexity:** O(n).
- **Space Complexity:** O(n) for `dp` array + O(n) for recursion stack.

---
#### b) Tabulation (Bottom-Up)
```python
def frog_jump_tab(heights: list[int]) -> int:
    n = len(heights)
    dp = [0] * n

    for i in range(1, n):
        jump1 = dp[i-1] + abs(heights[i] - heights[i-1])
        jump2 = float('inf')
        if i > 1:
            jump2 = dp[i-2] + abs(heights[i] - heights[i-2])
        dp[i] = min(jump1, jump2)

    return dp[n-1]
```
- **Time Complexity:** O(n).
- **Space Complexity:** O(n).

---
#### c) Space Optimization
```python
def frog_jump_optimized(heights: list[int]) -> int:
    n = len(heights)
    prev2 = 0
    prev1 = 0

    for i in range(1, n):
        jump1 = prev1 + abs(heights[i] - heights[i-1])
        jump2 = float('inf')
        if i > 1:
            jump2 = prev2 + abs(heights[i] - heights[i-2])

        current = min(jump1, jump2)
        prev2 = prev1
        prev1 = current

    return prev1
```
- **Time Complexity:** O(n).
- **Space Complexity:** O(1).

---

### 4. Frog Jump with K Distances
`[MEDIUM]` `#1D-DP` `#k-jumps`

#### Problem Statement
A frog must jump from stone 0 to `N-1`. The cost of a jump from stone `i` to `j` is `abs(heights[i] - heights[j])`. The frog can jump from `i` to any stone up to `i+k` (i.e. `i+1, i+2, ..., i+k`). Find the minimum energy cost.

#### Recurrence Relation
Let `dp[i]` be the minimum energy to reach stone `i`.
- **`dp[i] = min(dp[i-j] + abs(heights[i] - heights[i-j]))`** for all `1 <= j <= k` such that `i-j >= 0`.
- **Base Case:** `dp[0] = 0`.

---
#### a) Memoization (Top-Down)
```python
def frog_jump_k_memo(heights: list[int], k: int) -> int:
    n = len(heights)
    dp = [-1] * n

    def solve(index):
        if index == 0:
            return 0
        if dp[index] != -1:
            return dp[index]

        min_energy = float('inf')
        for j in range(1, k + 1):
            if index - j >= 0:
                jump = solve(index - j) + abs(heights[index] - heights[index - j])
                min_energy = min(min_energy, jump)
        dp[index] = min_energy
        return dp[index]

    return solve(n - 1)
```
- **Time Complexity:** O(n * k).
- **Space Complexity:** O(n) for the `dp` table + O(n) for recursion stack.

---
#### b) Tabulation (Bottom-Up)
```python
def frog_jump_k_tab(heights: list[int], k: int) -> int:
    n = len(heights)
    dp = [0] * n

    for i in range(1, n):
        min_energy = float('inf')
        for j in range(1, k + 1):
            if i - j >= 0:
                jump = dp[i - j] + abs(heights[i] - heights[i - j])
                min_energy = min(min_energy, jump)
        dp[i] = min_energy

    return dp[n - 1]
```
- **Time Complexity:** O(n * k).
- **Space Complexity:** O(n).

---
#### c) Space Optimization
We only need to store the DP values of the last `k` stones using a circular buffer.
```python
def frog_jump_k_optimized(heights: list[int], k: int) -> int:
    n = len(heights)
    dp_window = [0] * min(n, k)
    
    for i in range(1, n):
        min_energy = float('inf')
        for j in range(1, k + 1):
            if i - j >= 0:
                jump = dp_window[(i - j) % k] + abs(heights[i] - heights[i - j])
                min_energy = min(min_energy, jump)
        
        if len(dp_window) < k:
            dp_window.append(min_energy)
        else:
            dp_window[i % k] = min_energy

    return dp_window[(n - 1) % k] if n > 1 else 0
```
- **Time Complexity:** O(n * k).
- **Space Complexity:** O(k) for the circular buffer.

---

### 5. House Robber (Max Sum of Non-Adjacent Elements)
`[MEDIUM]` `#1D-DP`

#### Problem Statement
Given an array `nums` representing money in houses, find the max amount you can rob without robbing two adjacent houses.

#### Recurrence Relation
Let `dp[i]` be the max money robbed up to house `i`.
- **Choice 1: Rob house `i`**. Profit is `nums[i] + dp[i-2]`.
- **Choice 2: Skip house `i`**. Profit is `dp[i-1]`.
- **`dp[i] = max(nums[i] + dp[i-2], dp[i-1])`**

---
#### a) Memoization (Top-Down)
```python
def house_robber_memo(nums: list[int]) -> int:
    n = len(nums)
    dp = [-1] * n

    def solve(index):
        if index < 0:
            return 0
        if dp[index] != -1:
            return dp[index]

        pick = nums[index] + solve(index - 2)
        not_pick = solve(index - 1)

        dp[index] = max(pick, not_pick)
        return dp[index]

    return solve(n - 1)
```
- **Time Complexity:** O(n).
- **Space Complexity:** O(n) for `dp` array + O(n) for recursion stack.

---
#### b) Tabulation (Bottom-Up)
```python
def house_robber_tab(nums: list[int]) -> int:
    n = len(nums)
    if n == 0: return 0
    dp = [0] * n
    dp[0] = nums[0]

    for i in range(1, n):
        pick = nums[i]
        if i > 1:
            pick += dp[i-2]
        not_pick = dp[i-1]
        dp[i] = max(pick, not_pick)

    return dp[n-1]
```
- **Time Complexity:** O(n).
- **Space Complexity:** O(n).

---
#### c) Space Optimization
```python
def house_robber_optimized(nums: list[int]) -> int:
    prev2 = 0
    prev1 = 0
    for num in nums:
        current = max(prev1, num + prev2)
        prev2 = prev1
        prev1 = current
    return prev1
```
- **Time Complexity:** O(n).
- **Space Complexity:** O(1).

---

### 6. House Robber II (Circular Houses)

`[MEDIUM]` `#1D-DP` `#circular`

#### Problem Statement
Same as House Robber, but the houses are in a circle (the first and last are adjacent).

#### Implementation Overview
The circular constraint means we cannot rob both the first and last house. This breaks the problem into two independent, non-circular subproblems:
1.  Solve House Robber for the array excluding the last house (`nums[0...n-2]`).
2.  Solve House Robber for the array excluding the first house (`nums[1...n-1]`).
The final answer is the maximum of these two results. We can reuse our linear house robber function.

#### a) Memoization (Top-Down)
```python
def house_robber_ii_memo(nums: list[int]) -> int:
    if not nums: return 0
    if len(nums) == 1: return nums[0]

    def rob_linear_memo(sub_nums):
        n = len(sub_nums)
        dp = [-1] * n
        
        def solve(index):
            if index < 0:
                return 0
            if dp[index] != -1:
                return dp[index]
            
            pick = sub_nums[index] + solve(index - 2)
            not_pick = solve(index - 1)
            dp[index] = max(pick, not_pick)
            return dp[index]
            
        return solve(n - 1)

    return max(rob_linear_memo(nums[:-1]), rob_linear_memo(nums[1:]))
```
- **Time Complexity:** O(n).
- **Space Complexity:** O(n) for the DP array + O(n) for the recursion stack.

---
#### b) Tabulation (Bottom-Up)
```python
def house_robber_ii_tab(nums: list[int]) -> int:
    if not nums: return 0
    if len(nums) == 1: return nums[0]

    def rob_linear_tab(sub_nums):
        n = len(sub_nums)
        if n == 0: return 0
        dp = [0] * n
        dp[0] = sub_nums[0]
        
        for i in range(1, n):
            pick = sub_nums[i]
            if i > 1:
                pick += dp[i-2]
            not_pick = dp[i-1]
            dp[i] = max(pick, not_pick)
            
        return dp[n-1]

    return max(rob_linear_tab(nums[:-1]), rob_linear_tab(nums[1:]))
```
- **Time Complexity:** O(n).
- **Space Complexity:** O(n) for the DP array.

---
#### c) Space Optimization
```python
def house_robber_ii_optimized(nums: list[int]) -> int:
    if not nums: return 0
    if len(nums) == 1: return nums[0]

    def rob_linear_optimized(sub_nums):
        prev2, prev1 = 0, 0
        for num in sub_nums:
            current = max(prev1, num + prev2)
            prev2 = prev1
            prev1 = current
        return prev1

    return max(rob_linear_optimized(nums[:-1]), rob_linear_optimized(nums[1:]))
```
- **Time Complexity:** O(n).
- **Space Complexity:** O(1).
