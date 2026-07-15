# Pattern 2: Unbounded Knapsack

The Unbounded Knapsack pattern is a variation of 0/1 Knapsack. The key difference is that you can use each item an **unlimited** number of times.

### Alternative DP Formulations: Item-Centric vs. Capacity-Centric
Unbounded knapsack problems can be modeled using two fundamentally different DP state representations:

1. **Item-Centric Formulation (Formulation A):**
   - **State:** `dp[index][capacity]`
   - **Transition:** For each item, decide whether to skip it or stay at the same index and pick it again.
   - **Recurrence:** `dp[i][c] = max(dp[i-1][c], value[i] + dp[i][c - weight[i]])`
   - *This formulation is highly structured and mirrors 0/1 Knapsack, but requires 2D state space (which can then be space-optimized to 1D).*

2. **Capacity-Centric Formulation (Formulation B):**
   - **State:** `dp[capacity]`
   - **Transition:** For a given capacity `c`, iterate through all items and find the best item to place "last".
   - **Recurrence:** `dp[c] = max(value[i] + dp[c - weight[i]])` for all items `i`.
   - *This formulation natively reduces the DP state to a 1D array from the start, making it highly intuitive for capacity-only dependencies (like Coin Change or Rod Cutting).*

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
#### d) Capacity-Centric Formulation (Formulation B - 1D State)
Instead of keeping track of the item index, we calculate the max value for each capacity `w` by trying to place each of the `n` items at the end.
```python
def unbounded_knapsack_capacity_centric(W, values, weights):
    n = len(values)
    dp = [0] * (W + 1)

    for w in range(1, W + 1):
        for i in range(n):
            if weights[i] <= w:
                dp[w] = max(dp[w], values[i] + dp[w - weights[i]])

    return dp[W]
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
#### c) Space Optimization (Item-Centric 1D Array)
We can also solve this in an item-centric manner, iterating through the coins and updating the minimum coins needed for each amount. This uses a single 1D array of size `amount + 1`.

```python
def coin_change_min_optimized(coins: list[int], amount: int) -> int:
    n = len(coins)
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    for i in range(n):
        for j in range(coins[i], amount + 1):
            dp[j] = min(dp[j], 1 + dp[j - coins[i]])

    return dp[amount] if dp[amount] != float('inf') else -1
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
#### a) Memoization (Top-Down)
```python
def coin_change_combinations_memo(amount: int, coins: list[int]) -> int:
    n = len(coins)
    dp = [[-1] * (amount + 1) for _ in range(n)]

    def solve(index, target):
        if target == 0:
            return 1
        if index < 0 or target < 0:
            return 0
        if dp[index][target] != -1:
            return dp[index][target]

        not_pick = solve(index - 1, target)
        pick = 0
        if coins[index] <= target:
            pick = solve(index, target - coins[index])

        dp[index][target] = not_pick + pick
        return dp[index][target]

    return solve(n - 1, amount)
```
- **Time Complexity:** O(n * amount).
- **Space Complexity:** O(n * amount) + O(n + amount) recursion stack.

---
#### b) Tabulation (Bottom-Up)
```python
def coin_change_combinations_tab(amount: int, coins: list[int]) -> int:
    n = len(coins)
    dp = [[0] * (amount + 1) for _ in range(n)]
    
    for i in range(n):
        dp[i][0] = 1

    for i in range(n):
        for j in range(1, amount + 1):
            not_pick = dp[i-1][j] if i > 0 else 0
            pick = dp[i][j - coins[i]] if j >= coins[i] else 0
            dp[i][j] = not_pick + pick

    return dp[n-1][amount]
```
- **Time Complexity:** O(n * amount).
- **Space Complexity:** O(n * amount).

---
#### c) Space Optimization
```python
def coin_change_combinations_optimized(amount: int, coins: list[int]) -> int:
    dp = [0] * (amount + 1)
    dp[0] = 1

    for coin in coins:
        for j in range(coin, amount + 1):
            dp[j] += dp[j - coin]

    return dp[amount]
```
- **Time Complexity:** O(n * amount).
- **Space Complexity:** O(amount).

---

### 4. Rod Cutting Problem
`[MEDIUM]` `#unbounded-knapsack`

#### Problem Statement
Given a rod of length `n` and prices for pieces of different lengths, find the maximum value obtainable by cutting the rod.

#### Implementation Overview
This is an unbounded knapsack problem where rod length is capacity, piece lengths are weights, and prices are values.
- **DP State:** `dp[i][j]` = max profit considering pieces up to size `i` for a rod of length `j`.
- **Recurrence:** `dp[i][j] = max(dp[i-1][j], prices[i-1] + dp[i][j - i])` if piece length `i` <= `j`.

---
#### a) Memoization (Top-Down)
```python
def rod_cutting_memo(prices: list[int], n: int) -> int:
    m = len(prices)
    dp = [[-1] * (n + 1) for _ in range(m)]

    def solve(index, length):
        if index == 0:
            return length * prices[0] # length // 1 * prices[0]
        if dp[index][length] != -1:
            return dp[index][length]

        not_pick = solve(index - 1, length)
        pick = float('-inf')
        piece_len = index + 1
        if piece_len <= length:
            pick = prices[index] + solve(index, length - piece_len)

        dp[index][length] = max(pick, not_pick)
        return dp[index][length]

    return solve(m - 1, n)
```
- **Time Complexity:** O(n * len(prices)).
- **Space Complexity:** O(n * len(prices)) + O(n) recursion stack.

---
#### b) Tabulation (Bottom-Up)
```python
def rod_cutting_tab(prices: list[int], n: int) -> int:
    m = len(prices)
    dp = [[0] * (n + 1) for _ in range(m)]

    # Base case: first piece of length 1
    for length in range(n + 1):
        dp[0][length] = length * prices[0]

    for i in range(1, m):
        piece_len = i + 1
        for length in range(n + 1):
            not_pick = dp[i-1][length]
            pick = float('-inf')
            if piece_len <= length:
                pick = prices[i] + dp[i][length - piece_len]
            dp[i][length] = max(pick, not_pick)

    return dp[m-1][n]
```
- **Time/Space Complexity:** O(n * len(prices)).

---
#### c) Space Optimization
```python
def rod_cutting_optimized(prices: list[int], n: int) -> int:
    dp = [0] * (n + 1)
    # Base case for length 1 pieces
    for length in range(n + 1):
        dp[length] = length * prices[0]

    for i in range(1, len(prices)):
        piece_len = i + 1
        for length in range(piece_len, n + 1):
            dp[length] = max(dp[length], prices[i] + dp[length - piece_len])

    return dp[n]
```
- **Time Complexity:** O(n * len(prices)).
- **Space Complexity:** O(n).
