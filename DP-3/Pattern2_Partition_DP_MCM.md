# Pattern 2: Partition DP & MCM

Partition DP is a powerful pattern for problems where the objective is to find an optimal way to solve a problem by partitioning a sequence. The core idea is to define a state `dp[i][j]` representing the optimal solution for the subproblem on the range `arr[i...j]`. To compute `dp[i][j]`, we iterate through all possible partition points `k` between `i` and `j`, recursively solving the subproblems and combining their results. Matrix Chain Multiplication (MCM) is the most famous example.

---

### 1. Matrix Chain Multiplication (MCM)
`[HARD]` `#partition-dp` `#mcm`

#### Problem Statement
Given an array `arr` where `arr[i-1] x arr[i]` is the dimension of the `i`-th matrix, find the minimum number of scalar multiplications needed to multiply the chain of matrices.

#### Recurrence Relation
Let `solve(i, j)` be the min cost to multiply matrices `A[i]` through `A[j]`.
The dimensions of matrix `A[k]` are `arr[k-1] x arr[k]`.
To find `solve(i, j)`, we can split the chain at any point `k` between `i` and `j-1`.
- **`cost = solve(i, k) + solve(k+1, j) + cost_of_final_multiplication`**
- The final multiplication is between the resulting matrix from `(i..k)` (size `arr[i-1] x arr[k]`) and `(k+1..j)` (size `arr[k] x arr[j]`). The cost is `arr[i-1] * arr[k] * arr[j]`.
- **`solve(i, j) = min(solve(i,k) + solve(k+1,j) + arr[i-1]*arr[k]*arr[j])`** for `k` in `i..j-1`.
- **Base Case:** `solve(i, i) = 0` (a single matrix requires no multiplications).

---
#### a) Memoization (Top-Down)
```python
def mcm_memo(arr: list[int]) -> int:
    n = len(arr) # The number of matrices is n-1. arr[i-1]xarr[i] is the dimension of matrix i.
    dp = [[-1] * n for _ in range(n)] # Memoization table.

    def solve(i, j): # Function to find the min cost for matrices from i to j.
        if i == j: # Base case: a single matrix has 0 multiplication cost.
            return 0
        if dp[i][j] != -1: # If already computed, return the result.
            return dp[i][j]

        min_cost = float('inf') # Initialize min_cost to infinity.
        for k in range(i, j): # Iterate through all possible partition points.
            # Cost = cost of left part + cost of right part + cost of multiplying the two results.
            cost = solve(i, k) + solve(k + 1, j) + arr[i-1] * arr[k] * arr[j]
            min_cost = min(min_cost, cost) # Update the minimum cost.

        dp[i][j] = min_cost # Memoize the result.
        return dp[i][j]

    return solve(1, n - 1) # Solve for the entire chain of matrices from 1 to n-1.
```
#### Time and Space Complexity
- **Time Complexity:** O(n^3). There are O(n^2) states, and each state takes O(n) time for the loop over `k`.
- **Space Complexity:** O(n^2) for DP table + O(n) for recursion stack.

---
#### b) Tabulation (Bottom-Up)
```python
def mcm_tab(arr: list[int]) -> int:
    n = len(arr) # Number of matrices is n-1.
    dp = [[0] * n for _ in range(n)] # DP table to store costs.

    # l is the length of the matrix chain.
    for l in range(2, n): # Iterate over chain lengths from 2 to n-1.
        for i in range(1, n - l + 1): # i is the starting index of the chain.
            j = i + l - 1 # j is the ending index of the chain.
            dp[i][j] = float('inf') # Initialize the cost for this subproblem to infinity.
            for k in range(i, j): # k is the partition point.
                # Calculate the cost for this partition.
                cost = dp[i][k] + dp[k+1][j] + arr[i-1] * arr[k] * arr[j]
                dp[i][j] = min(dp[i][j], cost) # Update with the minimum cost found.

    return dp[1][n-1] # The result is the min cost for the entire chain from matrix 1 to n-1.
```
#### Time and Space Complexity
- **Time Complexity:** O(n^3).
- **Space Complexity:** O(n^2).

---

### 2. Minimum Cost to Cut the Stick
`[HARD]` `#partition-dp`

#### Problem Statement
Given a stick of length `n` and an array `cuts` of positions, find the minimum cost to make all cuts. The cost of a cut is the length of the stick segment it's on.

#### Recurrence Relation
1. Add `0` and `n` to `cuts` and sort it. This gives us the boundaries of all segments.
2. Let `solve(i, j)` be the min cost to cut the stick segment defined by `cuts[i]` and `cuts[j]`.
3. To find `solve(i, j)`, we try making the first cut at each possible position `k` between `i` and `j`.
- **Cost:** `(cuts[j] - cuts[i])` (cost of the current cut) `+ solve(i, k) + solve(k, j)`.
- **`solve(i, j) = (cuts[j] - cuts[i]) + min(solve(i,k) + solve(k,j))`** for `k` in `i+1..j-1`.
- **Base Case:** If `j <= i + 1`, there are no cuts to be made, so cost is 0.

---
#### a) Memoization (Top-Down)
```python
def min_cost_cut_stick_memo(n: int, cuts: list[int]) -> int:
    cuts = sorted([0] + cuts + [n]) # Add boundaries 0 and n, then sort.
    m = len(cuts) # The number of points in the augmented cuts array.
    dp = [[-1] * m for _ in range(m)] # Memoization table.

    def solve(i, j): # Function to find the min cost for the segment between cuts[i] and cuts[j].
        if j <= i + 1: # Base case: If there are no cuts to be made between i and j.
            return 0
        if dp[i][j] != -1: # Return memoized result if available.
            return dp[i][j]

        min_cost = float('inf') # Initialize min_cost.
        for k in range(i + 1, j): # Iterate through all possible cut positions k between i and j.
            # Cost = cost of the current cut + cost of the left subproblem + cost of the right subproblem.
            cost = (cuts[j] - cuts[i]) + solve(i, k) + solve(k, j)
            min_cost = min(min_cost, cost) # Update the minimum cost.

        dp[i][j] = min_cost # Memoize the result.
        return dp[i][j]

    return solve(0, m - 1) # Solve for the entire stick from 0 to n.
```
#### Time and Space Complexity
- **Time Complexity:** O(m^3), where m is the number of cuts.
- **Space Complexity:** O(m^2) for DP table.

---
#### b) Tabulation (Bottom-Up)
```python
def min_cost_cut_stick_tab(n: int, cuts: list[int]) -> int:
    cuts = sorted([0] + cuts + [n]) # Add boundaries and sort the cuts.
    m = len(cuts) # Get the size of the augmented cuts array.
    dp = [[0] * m for _ in range(m)] # Initialize a 2D DP table.

    # Iterate through the segments by decreasing start index 'i'.
    for i in range(m - 2, -1, -1):
        # And increasing end index 'j'. This ensures smaller subproblems are solved first.
        for j in range(i + 2, m):
            min_cost = float('inf') # Initialize min_cost for the current segment.
            for k in range(i + 1, j): # Iterate through all possible first cuts 'k'.
                # Calculate the cost for this choice of k.
                cost = (cuts[j] - cuts[i]) + dp[i][k] + dp[k][j]
                min_cost = min(min_cost, cost) # Update the minimum cost.
            dp[i][j] = min_cost # Store the result in the DP table.

    return dp[0][m-1] # The result is the min cost for the whole stick (from cuts[0] to cuts[m-1]).
```
#### Time and Space Complexity
- **Time Complexity:** O(m^3).
- **Space Complexity:** O(m^2).

---

### 3. Burst Balloons
`[HARD]` `#partition-dp`

#### Problem Statement
Given `n` balloons with values `nums[i]`, bursting balloon `i` gives `nums[left] * nums[i] * nums[right]` coins. Find the maximum coins.

#### Recurrence Relation
The key is to think in reverse: which balloon do we burst **last** in a given range `(i, j)`?
1. Add `1` to the beginning and end of `nums` to handle boundaries.
2. Let `solve(i, j)` be the max coins from bursting balloons in the open interval `(i, j)`.
3. Let `k` be the *last* balloon burst in `(i, j)`. Its neighbors will be `i` and `j`.
- **`coins = solve(i,k) + solve(k,j) + nums[i]*nums[k]*nums[j]`**.
- **`solve(i, j) = max(coins)`** over all `k` from `i+1` to `j-1`.
- **Base Case:** If `j <= i + 1`, no balloons to burst, cost is 0.

---
#### a) Memoization (Top-Down)
```python
def max_coins_memo(nums: list[int]) -> int:
    nums = [1] + nums + [1] # Add boundary balloons with value 1.
    n = len(nums) # Get the new length of the array.
    dp = [[-1] * n for _ in range(n)] # Memoization table.

    def solve(i, j): # Function to find max coins in the interval (i, j).
        if i >= j - 1: return 0 # Base case: If there are no balloons to burst.
        if dp[i][j] != -1: return dp[i][j] # Return memoized result.

        max_c = 0 # Initialize max coins for this subproblem.
        # k is the last balloon to be burst in the interval (i, j).
        for k in range(i + 1, j):
            # Coins = coins from left part + coins from right part + coins from bursting k last.
            coins = solve(i, k) + solve(k, j) + nums[i] * nums[k] * nums[j]
            max_c = max(max_c, coins) # Update max coins.
        dp[i][j] = max_c # Memoize the result.
        return dp[i][j]

    return solve(0, n - 1) # Solve for the entire range of balloons.
```
#### Time and Space Complexity
- **Time Complexity:** O(n^3).
- **Space Complexity:** O(n^2) for DP table.

---
#### b) Tabulation (Bottom-Up)
```python
def max_coins_tab(nums: list[int]) -> int:
    nums = [1] + nums + [1] # Add boundary balloons.
    n = len(nums) # Get the new length.
    dp = [[0] * n for _ in range(n)] # Initialize a 2D DP table.

    for i in range(n - 2, -1, -1): # Iterate backwards for the start of the interval.
        for j in range(i + 2, n): # Iterate forwards for the end of the interval.
            max_c = 0 # Initialize max coins for this subproblem.
            # k is the last balloon to be burst in the interval (i, j).
            for k in range(i + 1, j):
                # Calculate the coins gained for this choice of k.
                coins = dp[i][k] + dp[k][j] + nums[i] * nums[k] * nums[j]
                max_c = max(max_c, coins) # Update the max coins.
            dp[i][j] = max_c # Store the result in the DP table.

    return dp[0][n-1] # The result is the max coins for the entire range.
```
#### Time and Space Complexity
- **Time Complexity:** O(n^3).
- **Space Complexity:** O(n^2) for DP table.

---

### 4. Partition Array for Maximum Sum
`[MEDIUM]` `#partition-dp`

#### Problem Statement
Partition an array `arr` into contiguous subarrays of length at most `k`. After partitioning, each subarray's values are changed to become the max value of that subarray. Return the largest sum of the array after partitioning.

#### Recurrence Relation
This is a 1D DP problem, but with a partition-like thought process.
- **`dp[i]`**: max sum for the prefix `arr[0...i-1]`.
- To compute `dp[i]`, we consider the last subarray ending at `i-1`. It can have length `j` from 1 to `k`.
- **`dp[i] = max(dp[i-j] + max_in_last_partition * j)`** for `j` from 1 to `k`.

---
#### a) Memoization (Top-Down)
```python
def max_sum_after_partitioning_memo(arr: list[int], k: int) -> int:
    n = len(arr) # Get the length of the array.
    dp = [-1] * n # Memoization table for the subproblems starting at each index.

    def solve(index): # Function to find the max sum for the subarray arr[index:].
        if index == n: return 0 # Base case: If we are at the end of the array, sum is 0.
        if dp[index] != -1: return dp[index] # Return memoized result.

        max_ans = 0 # Initialize max answer for this state.
        max_val_in_partition = 0 # Track the max value in the current potential partition.
        # Iterate through all possible partition end points 'j'.
        for j in range(index, min(n, index + k)):
            max_val_in_partition = max(max_val_in_partition, arr[j]) # Update the max value in the partition.
            partition_len = j - index + 1 # Calculate the length of the current partition.
            # Sum = (value of the partition) + (result of the rest of the array).
            current_sum = (max_val_in_partition * partition_len) + solve(j + 1)
            max_ans = max(max_ans, current_sum) # Update the max answer.

        dp[index] = max_ans # Memoize the result.
        return dp[index]

    return solve(0) # Start the process from the beginning of the array.
```
#### Time and Space Complexity
- **Time Complexity:** O(n * k).
- **Space Complexity:** O(n) for DP table + O(n) for recursion stack.

---
#### b) Tabulation (Bottom-Up)
```python
def max_sum_after_partitioning_tab(arr: list[int], k: int) -> int:
    n = len(arr) # Get the length of the array.
    dp = [0] * (n + 1) # DP table where dp[i] stores the max sum for the prefix of length i.

    for i in range(1, n + 1): # Iterate through all possible prefix lengths.
        max_val_in_partition = 0 # To track the max value in the last partition.
        # j is the length of the last partition.
        for j in range(1, k + 1):
            if i - j >= 0: # Ensure we don't go out of bounds.
                # The element at arr[i-j] is the next one to consider for the last partition.
                max_val_in_partition = max(max_val_in_partition, arr[i-j])
                # Calculate the sum for this partition choice.
                current_sum = dp[i-j] + max_val_in_partition * j
                dp[i] = max(dp[i], current_sum) # Update dp[i] with the max sum found so far.

    return dp[n] # The result is the max sum for the entire array.
```
#### Time and Space Complexity
- **Time Complexity:** O(n * k).
- **Space Complexity:** O(n).
