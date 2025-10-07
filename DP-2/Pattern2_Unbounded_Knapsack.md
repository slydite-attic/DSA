# Pattern 2: Unbounded Knapsack

The Unbounded Knapsack pattern is a variation of 0/1 Knapsack. The key difference is that you can use each item an **unlimited** number of times. This changes the recurrence relation, as the choice for an item does not remove it from the set of future choices.

---

### 1. Unbounded Knapsack
`[MEDIUM]` `#unbounded-knapsack`

#### Problem Statement
Given items with weights and values, and a knapsack of capacity `W`, find the maximum value of items that can be put into the knapsack. You can use any item an unlimited number of times.

#### Recurrence Relation
Let `solve(index, capacity)` be the max value from items `0..index` with a given `capacity`.
- **Choice 1 (Don't Pick):** If we don't pick `nums[index]`, the value is `solve(index - 1, capacity)`.
- **Choice 2 (Pick):** If we pick `nums[index]`, the value is `values[index] + solve(index, capacity - weights[index])`. Note that we stay at the same `index` because we can pick the item again.
- **`solve(index, capacity) = max(choice1, choice2)`**

---
#### a) Memoization (Top-Down)
```python
def unbounded_knapsack_memo(W, values, weights):
    n = len(values) # Get the number of items.
    dp = [[-1] * (W + 1) for _ in range(n)] # Initialize a memoization table with -1.

    def solve(index, capacity): # Recursive helper function.
        if index == 0: # Base case: If only the first item is considered.
            return (capacity // weights[0]) * values[0] # It can be picked as many times as the capacity allows.
        if dp[index][capacity] != -1: # If the state is already computed, return the stored value.
            return dp[index][capacity]

        not_pick = solve(index - 1, capacity) # Case 1: Don't pick the current item.
        pick = -1 # Initialize the 'pick' value to -1 (or any indicator for not possible).
        if weights[index] <= capacity: # If the current item's weight is within the capacity.
            pick = values[index] + solve(index, capacity - weights[index]) # Case 2: Pick the item and solve for the remaining capacity.

        dp[index][capacity] = max(pick, not_pick) # Store the maximum value of picking or not picking.
        return dp[index][capacity] # Return the result for the current state.

    return solve(n - 1, W) # Start the recursion from the last item with the full knapsack capacity.
```
- **Time Complexity:** O(n * W).
- **Space Complexity:** O(n * W) for DP table + O(n) for recursion stack.

---
#### b) Tabulation (Bottom-Up)
```python
def unbounded_knapsack_tab(W, values, weights):
    n = len(values) # Get the number of items.
    dp = [[0] * (W + 1) for _ in range(n)] # Initialize a 2D DP table with zeros.

    # Base case for the first item: calculate the value for all capacities.
    for w in range(W + 1): # Iterate through all capacities from 0 to W.
        dp[0][w] = (w // weights[0]) * values[0] # The value is how many times the first item fits, times its value.

    for i in range(1, n): # Iterate through each item starting from the second one.
        for w in range(W + 1): # Iterate through each capacity.
            not_pick = dp[i-1][w] # The value if the current item is not picked.
            pick = -1 # Initialize the 'pick' value.
            if weights[i] <= w: # If the current item's weight is within the capacity.
                pick = values[i] + dp[i][w - weights[i]] # The value is the current item's value plus the value for the remaining capacity with the same item.
            dp[i][w] = max(pick, not_pick) # Store the maximum of the two choices.

    return dp[n-1][W] # The result is in the last row and column of the DP table.
```
- **Time Complexity:** O(n * W).
- **Space Complexity:** O(n * W).

---
#### c) Space Optimization (1D Array)
The tabulation can be optimized to a single 1D array. The key difference from 0/1 knapsack is that the inner loop for `w` runs from left to right. This allows the current item `i` to be considered multiple times for a given capacity `w`.

```python
def unbounded_knapsack_optimized(W, values, weights):
    n = len(values) # Get the number of items.
    dp = [0] * (W + 1) # Initialize a 1D DP array to store the maximum value for each capacity.

    for i in range(n): # Iterate through each item.
        for w in range(weights[i], W + 1): # Iterate through capacities from the current item's weight up to W.
            # The forward iteration allows using the same item multiple times.
            dp[w] = max(dp[w], values[i] + dp[w - weights[i]]) # Update the max value for capacity 'w'.

    return dp[W] # The result is the value stored for the full capacity W.
```
- **Time Complexity:** O(n * W).
- **Space Complexity:** O(W).

---

### 2. Coin Change (Minimum Coins)
`[MEDIUM]` `#unbounded-knapsack` `#coin-change`

#### Problem Statement
Given coins of different denominations and a total `amount`, find the fewest coins needed to make up that amount. If impossible, return -1.

#### Recurrence Relation
Let `dp[i]` be the min coins for amount `i`.
- **`dp[i] = 1 + min(dp[i - coin])`** for every `coin` denomination.
- **Base Case:** `dp[0] = 0`.

---
#### a) Memoization (Top-Down)
```python
def coin_change_min_memo(coins: list[int], amount: int) -> int:
    dp = {} # Use a dictionary for memoization.
    def solve(rem_amount): # Recursive helper function to find the minimum coins for a remaining amount.
        if rem_amount == 0: return 0 # Base case: If remaining amount is 0, no coins are needed.
        if rem_amount < 0: return float('inf') # Base case: If amount is negative, this path is invalid.
        if rem_amount in dp: return dp[rem_amount] # If the result is already memoized, return it.

        min_coins = float('inf') # Initialize min_coins to infinity.
        for coin in coins: # Iterate through each available coin denomination.
            res = solve(rem_amount - coin) # Recursively call for the amount after using the current coin.
            if res != float('inf'): # If a valid solution was found for the subproblem,
                min_coins = min(min_coins, 1 + res) # Update min_coins with the smaller value.

        dp[rem_amount] = min_coins # Memoize the result for the current remaining amount.
        return min_coins # Return the computed minimum coins.

    result = solve(amount) # Start the recursion with the initial amount.
    return result if result != float('inf') else -1 # If a solution was found, return it; otherwise, return -1.
```
- **Time Complexity:** O(amount * len(coins)).
- **Space Complexity:** O(amount) for DP table + O(amount) for recursion stack.

---
#### b) Tabulation (Bottom-Up)
```python
def coin_change_min_tab(coins: list[int], amount: int) -> int:
    dp = [float('inf')] * (amount + 1) # Initialize a DP array with infinity, representing min coins for each amount.
    dp[0] = 0 # Base case: 0 coins are needed to make an amount of 0.

    for i in range(1, amount + 1): # Iterate through all amounts from 1 to the target amount.
        for coin in coins: # Iterate through each coin denomination.
            if i >= coin: # If the current amount is greater than or equal to the coin value,
                dp[i] = min(dp[i], 1 + dp[i - coin]) # Update the min coins needed for amount 'i'.

    return dp[amount] if dp[amount] != float('inf') else -1 # Return the result for the target amount, or -1 if not possible.
```
- **Time Complexity:** O(amount * len(coins)).
- **Space Complexity:** O(amount).

---

### 3. Coin Change II (Number of Combinations)
`[MEDIUM]` `#unbounded-knapsack` `#coin-change` `#count-combinations`

#### Problem Statement
Given coins and an `amount`, find the number of **combinations** of coins that make up that amount.

#### Recurrence Relation
Let `dp[i]` = number of ways to make sum `i`. To avoid counting permutations, we process one coin at a time.
- For each `coin`, we update the `dp` array: **`dp[j] = dp[j] + dp[j - coin]`**.

---
#### a) Tabulation (Bottom-Up)
The tabulation approach is the most natural for this problem. The order of loops is crucial for counting combinations instead of permutations.

```python
def coin_change_combinations_tab(amount: int, coins: list[int]) -> int:
    dp = [0] * (amount + 1) # Initialize a DP array to store the number of combinations for each amount.
    dp[0] = 1 # Base case: there is one way to make an amount of 0 (by choosing no coins).

    # The outer loop iterates through coins to ensure we count combinations, not permutations.
    for coin in coins: # For each coin,
        for j in range(coin, amount + 1): # Iterate from the coin's value up to the target amount.
            dp[j] += dp[j - coin] # The number of ways to make amount 'j' is increased by the number of ways to make 'j - coin'.

    return dp[amount] # The result is the number of combinations for the target amount.
```
- **Time Complexity:** O(amount * len(coins)).
- **Space Complexity:** O(amount).

---

### 4. Rod Cutting Problem
`[MEDIUM]` `#unbounded-knapsack`

#### Problem Statement
Given a rod of length `n` and prices for pieces of different lengths, find the maximum value obtainable by cutting the rod.

#### Implementation Overview
This is an unbounded knapsack problem where rod length is capacity, piece lengths are weights, and prices are values.
- **DP State:** `dp[i]` = max profit from a rod of length `i`.
- **Recurrence:** `dp[i] = max(prices[j-1] + dp[i-j])` for all cut lengths `j` from 1 to `i`.

---
#### a) Tabulation (Bottom-Up)
```python
def rod_cutting_tab(prices: list[int], n: int) -> int:
    # Let lengths be 1-based for easier mapping.
    lengths = [i + 1 for i in range(len(prices))] # Create a list of possible rod lengths.
    dp = [0] * (n + 1) # Initialize a DP array to store the maximum profit for each rod length.

    for i in range(1, n + 1): # Iterate through all rod lengths from 1 to n.
        for j in range(len(lengths)): # Iterate through all available piece lengths.
            if lengths[j] <= i: # If the piece length is not more than the current rod length,
                dp[i] = max(dp[i], prices[j] + dp[i - lengths[j]]) # Update the maximum profit for length 'i'.

    return dp[n] # The result is the maximum profit for a rod of length n.
```
- **Time Complexity:** O(n * len(prices)).
- **Space Complexity:** O(n).
