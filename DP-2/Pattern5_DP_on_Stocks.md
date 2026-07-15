# Pattern 5: DP on Stocks

The "DP on Stocks" pattern is a series of problems that involve maximizing profit from buying and selling stocks under various constraints. The core idea is to define a state at each day `i` based on whether we are holding a stock or not (`can_buy`). This state can be extended to include transaction counts, cooldowns, etc.

**General Recurrence Relation:**
Let `solve(index, can_buy)` be the max profit from `index` onwards.
- If `can_buy`:
    - **Choice 1 (Buy):** `-prices[index] + solve(index + 1, cannot_buy)`
    - **Choice 2 (Skip):** `0 + solve(index + 1, can_buy)`
    - We take `max(Choice1, Choice2)`.
- If `cannot_buy`:
    - **Choice 1 (Sell):** `prices[index] + solve(index + 1, can_buy)` (plus any fees/cooldowns)
    - **Choice 2 (Skip):** `0 + solve(index + 1, cannot_buy)`
    - We take `max(Choice1, Choice2)`.

---

### 1. Best Time to Buy and Sell Stock
`[EASY]` `#dp-on-stocks` `#greedy`

#### Problem Statement
Maximize profit with a **single transaction** (one buy, one sell).

#### Implementation Overview
While a simple greedy approach is most efficient (O(n) time, O(1) space), this problem can be framed with DP to show the foundational thinking. However, the greedy solution is standard and preferred.

```python
# Greedy Solution
def max_profit_one_transaction(prices: list[int]) -> int:
    min_price = float('inf') # Initialize the minimum price seen so far to infinity.
    max_profit = 0 # Initialize the maximum profit to 0.
    for price in prices: # Iterate through each price in the list.
        min_price = min(min_price, price) # Update the minimum price if the current price is lower.
        max_profit = max(max_profit, price - min_price) # Calculate the potential profit if selling today and update max_profit.
    return max_profit # Return the maximum profit found.
```
- **Time Complexity:** O(n).
- **Space Complexity:** O(1).

---

### 2. Best Time to Buy and Sell Stock II
`[MEDIUM]` `#dp-on-stocks` `#greedy`

#### Problem Statement
Maximize profit with **infinite transactions**.

#### Recurrence Relation
`solve(index, can_buy)`:
- `can_buy`: `max(-prices[index] + solve(index+1, 0), solve(index+1, 1))`
- `!can_buy`: `max(prices[index] + solve(index+1, 1), solve(index+1, 0))`

---
#### a) Memoization (Top-Down)
```python
def max_profit_infinite_memo(prices: list[int]) -> int:
    n = len(prices) # Get the number of days.
    dp = [[-1] * 2 for _ in range(n)] # DP table to store results: dp[day][can_buy_flag].

    def solve(index, can_buy): # Recursive helper function.
        if index == n: return 0 # Base case: If past the last day, no more profit can be made.
        if dp[index][can_buy] != -1: return dp[index][can_buy] # Return memoized result.

        if can_buy: # If we are allowed to buy on this day,
            buy_profit = -prices[index] + solve(index + 1, 0) # Profit if we buy today.
            skip_profit = solve(index + 1, 1) # Profit if we skip buying today.
            dp[index][can_buy] = max(buy_profit, skip_profit) # Store the max of the two choices.
        else: # If we must sell (or hold),
            sell_profit = prices[index] + solve(index + 1, 1) # Profit if we sell today.
            skip_profit = solve(index + 1, 0) # Profit if we skip selling today.
            dp[index][can_buy] = max(sell_profit, skip_profit) # Store the max of the two choices.

        return dp[index][can_buy] # Return the computed profit.

    return solve(0, 1) # Start recursion from day 0 with the ability to buy.
```
- **Time Complexity:** O(n * 2) ~ O(n).
- **Space Complexity:** O(n * 2) for the DP table + O(n) for recursion stack.

---
#### b) Tabulation (Bottom-Up)
```python
def max_profit_infinite_tab(prices: list[int]) -> int:
    n = len(prices)
    dp = [[0] * 2 for _ in range(n + 1)]

    # Base case: dp[n][0] = dp[n][1] = 0 (automatically 0)

    for index in range(n - 1, -1, -1):
        for can_buy in range(2):
            if can_buy:
                dp[index][can_buy] = max(-prices[index] + dp[index+1][0], dp[index+1][1])
            else:
                dp[index][can_buy] = max(prices[index] + dp[index+1][1], dp[index+1][0])

    return dp[0][1]
```
- **Time/Space Complexity:** O(n).

---
#### c) Space Optimization
```python
def max_profit_infinite_optimized(prices: list[int]) -> int:
    n = len(prices) # Get the number of days.
    ahead_can_buy, ahead_cannot_buy = 0, 0 # Initialize variables to store the profits for the next day.

    for i in range(n - 1, -1, -1): # Iterate backwards from the second to last day.
        # Calculate the max profit for the current day if we can buy.
        curr_can_buy = max(-prices[i] + ahead_cannot_buy, ahead_can_buy)
        # Calculate the max profit for the current day if we cannot buy (must sell or hold).
        curr_cannot_buy = max(prices[i] + ahead_can_buy, ahead_cannot_buy)

        ahead_can_buy = curr_can_buy # Update the 'ahead' variables for the next iteration.
        ahead_cannot_buy = curr_cannot_buy

    return ahead_can_buy # The final result is the max profit if we can buy on day 0.
```
- **Time Complexity:** O(n).
- **Space Complexity:** O(1).

---

### 3. Best Time to Buy and Sell Stock III
`[HARD]` `#dp-on-stocks`

#### Problem Statement
Maximize profit with **at most two transactions**.

#### Recurrence Relation
The state must now include the transaction count.
`solve(index, can_buy, transactions_left)`

---
#### a) Memoization (Top-Down)
```python
def max_profit_two_transactions_memo(prices: list[int]) -> int:
    n = len(prices)
    # Memo table: dp[index][can_buy][transactions_left]
    # transactions_left can be 0, 1, 2. can_buy can be 0, 1.
    dp = [[[-1] * 3 for _ in range(2)] for _ in range(n)]

    def solve(index, can_buy, cap):
        if index == n or cap == 0:
            return 0
        if dp[index][can_buy][cap] != -1:
            return dp[index][can_buy][cap]

        if can_buy:
            buy = -prices[index] + solve(index + 1, 0, cap)
            skip = solve(index + 1, 1, cap)
            dp[index][can_buy][cap] = max(buy, skip)
        else:
            sell = prices[index] + solve(index + 1, 1, cap - 1)
            skip = solve(index + 1, 0, cap)
            dp[index][can_buy][cap] = max(sell, skip)

        return dp[index][can_buy][cap]

    return solve(0, 1, 2)
```
- **Time Complexity:** O(n * 2 * 3) ~ O(n).
- **Space Complexity:** O(n * 2 * 3) ~ O(n) for the DP table + O(n) for the recursion stack.

---
#### b) Tabulation (Bottom-Up)
A 3D DP table `dp[index][can_buy][transactions]` can be used, or a 2D table tracking the four explicit states (buy1, sell1, buy2, sell2). Below is the 4-state version:

```python
def max_profit_two_transactions_tab(prices: list[int]) -> int:
    n = len(prices) # Get the number of days.
    # dp[day][transaction_state] where states are 0:buy1, 1:sell1, 2:buy2, 3:sell2.
    dp = [[0] * 4 for _ in range(n)] # Initialize a 2D DP table.

    dp[0][0] = -prices[0] # Initialize the first buy on day 0.
    dp[0][2] = -prices[0] # Initialize the second buy on day 0 (after an imaginary first transaction).

    for i in range(1, n): # Iterate through the days starting from the second day.
        # State 0: Max profit after the first buy.
        dp[i][0] = max(dp[i-1][0], -prices[i])
        # State 1: Max profit after the first sell.
        dp[i][1] = max(dp[i-1][1], dp[i-1][0] + prices[i])
        # State 2: Max profit after the second buy.
        dp[i][2] = max(dp[i-1][2], dp[i-1][1] - prices[i])
        # State 3: Max profit after the second sell.
        dp[i][3] = max(dp[i-1][3], dp[i-1][2] + prices[i])

    return dp[n-1][3] # The result is the max profit after the second sell on the last day.
```
- **Time Complexity:** O(n * 4) ~ O(n).
- **Space Complexity:** O(n * 4) ~ O(n).

---
#### b) Space Optimization
```python
def max_profit_two_transactions_optimized(prices: list[int]) -> int:
    buy1, sell1 = float('-inf'), 0 # Initialize profits for the first transaction.
    buy2, sell2 = float('-inf'), 0 # Initialize profits for the second transaction.

    for price in prices: # Iterate through each day's price.
        buy1 = max(buy1, -price) # Update the max profit after the first buy.
        sell1 = max(sell1, buy1 + price) # Update the max profit after the first sell.
        buy2 = max(buy2, sell1 - price) # Update the max profit after the second buy.
        sell2 = max(sell2, buy2 + price) # Update the max profit after the second sell.

    return sell2 # The final result is the max profit after the second sell.
```
- **Time Complexity:** O(n).
- **Space Complexity:** O(1).

---

### 4. Best Time to Buy and Sell Stock IV
`[HARD]` `#dp-on-stocks`

#### Problem Statement
Maximize profit with **at most k transactions** (one transaction = one buy and one sell).

#### Recurrence Relation & Alternative DP Formulations
This problem generalizes Stock III. There are two main ways to formulate the DP states:

##### Formulation A: 3D DP State `dp[index][can_buy][transactions_left]`
- **`dp[i][1][cap] = max(-prices[i] + dp[i+1][0][cap], dp[i+1][1][cap])`**
- **`dp[i][0][cap] = max(prices[i] + dp[i+1][1][cap-1], dp[i+1][0][cap])`**

##### Formulation B: 2D DP State `dp[index][transaction_state]` (State Machine)
We can map the $k$ transactions to $2k$ states:
- Even states ($0, 2, \dots, 2k-2$) represent buying.
- Odd states ($1, 3, \dots, 2k-1$) represent selling.
- **For buying state `s`**: `dp[i][s] = max(dp[i-1][s], dp[i-1][s-1] - prices[i])` (where `dp[i-1][-1]` is 0).
- **For selling state `s`**: `dp[i][s] = max(dp[i-1][s], dp[i-1][s-1] + prices[i])`.

---
#### a) Memoization (Top-Down - Formulation A)
```python
def max_profit_k_transactions_memo(k: int, prices: list[int]) -> int:
    n = len(prices)
    dp = [[[-1] * (k + 1) for _ in range(2)] for _ in range(n)]

    def solve(index, can_buy, cap):
        if index == n or cap == 0:
            return 0
        if dp[index][can_buy][cap] != -1:
            return dp[index][can_buy][cap]

        if can_buy:
            buy = -prices[index] + solve(index + 1, 0, cap)
            skip = solve(index + 1, 1, cap)
            dp[index][can_buy][cap] = max(buy, skip)
        else:
            sell = prices[index] + solve(index + 1, 1, cap - 1)
            skip = solve(index + 1, 0, cap)
            dp[index][can_buy][cap] = max(sell, skip)

        return dp[index][can_buy][cap]

    return solve(0, 1, k)
```
- **Time Complexity:** O(n * 2 * k) ~ O(n * k).
- **Space Complexity:** O(n * k) for the DP table + O(n) for the recursion stack.

---
#### b) Tabulation (Bottom-Up - Formulation A)
```python
def max_profit_k_transactions_tab(k: int, prices: list[int]) -> int:
    n = len(prices)
    dp = [[[0] * (k + 1) for _ in range(2)] for _ in range(n + 1)]

    for index in range(n - 1, -1, -1):
        for can_buy in range(2):
            for cap in range(1, k + 1):
                if can_buy:
                    dp[index][can_buy][cap] = max(-prices[index] + dp[index+1][0][cap], dp[index+1][1][cap])
                else:
                    dp[index][can_buy][cap] = max(prices[index] + dp[index+1][1][cap - 1], dp[index+1][0][cap])

    return dp[0][1][k]
```
- **Time Complexity:** O(n * k).
- **Space Complexity:** O(n * k).

---
#### c) Alternative 2D Tabulation (Formulation B)
By treating the problem as a state machine of $2k$ transaction states, we reduce the dimensions from 3D to 2D.
```python
def max_profit_k_transactions_alternative_tab(k: int, prices: list[int]) -> int:
    n = len(prices)
    if n == 0 or k == 0:
        return 0
    
    # dp[day][state] where states are 0 to 2k-1
    dp = [[0] * (2 * k) for _ in range(n)]
    
    # Initial state on day 0
    for s in range(2 * k):
        if s % 2 == 0:
            dp[0][s] = -prices[0]  # Buy state
            
    for i in range(1, n):
        for s in range(2 * k):
            if s == 0:
                # First buy
                dp[i][s] = max(dp[i-1][s], -prices[i])
            elif s % 2 == 0:
                # Subsequent buys
                dp[i][s] = max(dp[i-1][s], dp[i-1][s-1] - prices[i])
            else:
                # Sells
                dp[i][s] = max(dp[i-1][s], dp[i-1][s-1] + prices[i])
                
    return dp[n-1][2*k - 1]
```
- **Time Complexity:** O(n * k).
- **Space Complexity:** O(n * k).

---
#### d) Space Optimization (Formulation B)
Using the state machine formulation, we only need to keep track of the current values of the $2k$ states.
```python
def max_profit_k_transactions_optimized(k: int, prices: list[int]) -> int:
    if not prices or k == 0:
        return 0
        
    # Initialize states: buy states to -infinity, sell states to 0
    states = [float('-inf') if i % 2 == 0 else 0 for i in range(2 * k)]

    for price in prices:
        for s in range(2 * k):
            if s == 0:
                states[s] = max(states[s], -price)
            elif s % 2 == 0:
                states[s] = max(states[s], states[s-1] - price)
            else:
                states[s] = max(states[s], states[s-1] + price)

    return states[2 * k - 1]
```
- **Time Complexity:** O(n * k).
- **Space Complexity:** O(k) space.

---

### 4. Best Time to Buy and Sell Stock with Cooldown
`[MEDIUM]` `#dp-on-stocks` `#cooldown`

#### Problem Statement
Maximize profit with infinite transactions, but with a one-day cooldown after selling.

#### Recurrence Relation
`solve(index, can_buy)`:
- `can_buy`: `max(-prices[index] + solve(index+1, 0), solve(index+1, 1))`
- `!can_buy`: The sell choice now forces a cooldown. `max(prices[index] + solve(index+2, 1), solve(index+1, 0))`. `index+2` skips one day.

---
#### a) Memoization (Top-Down)
```python
def max_profit_cooldown_memo(prices: list[int]) -> int:
    n = len(prices) # Get the number of days.
    dp = [[-1] * 2 for _ in range(n)] # Initialize a DP table for memoization.

    def solve(index, can_buy): # Recursive helper function.
        if index >= n: return 0 # Base case: If past the last day, profit is 0.
        if dp[index][can_buy] != -1: return dp[index][can_buy] # Return memoized result.

        if can_buy: # If we can buy today,
            # Choose between buying (and then not being able to buy tomorrow) or skipping.
            profit = max(-prices[index] + solve(index + 1, 0), solve(index + 1, 1))
        else: # If we must sell or hold,
            # Choose between selling (and then having a cooldown, so jumping to index+2) or skipping.
            profit = max(prices[index] + solve(index + 2, 1), solve(index + 1, 0))

        dp[index][can_buy] = profit # Memoize the result.
        return profit # Return the computed profit.

    return solve(0, 1) # Start from day 0 with the ability to buy.
```
- **Time Complexity:** O(n).
- **Space Complexity:** O(n) for the DP table + O(n) for recursion stack.

---
#### b) Tabulation (Bottom-Up)
```python
def max_profit_cooldown_tab(prices: list[int]) -> int:
    n = len(prices)
    # dp[index][can_buy]
    # base case: index >= n is 0, so we size n+2 to avoid out of bound on index+2
    dp = [[0] * 2 for _ in range(n + 2)]

    for index in range(n - 1, -1, -1):
        for can_buy in range(2):
            if can_buy:
                dp[index][can_buy] = max(-prices[index] + dp[index+1][0], dp[index+1][1])
            else:
                dp[index][can_buy] = max(prices[index] + dp[index+2][1], dp[index+1][0])

    return dp[0][1]
```
- **Time/Space Complexity:** O(n).

---
#### c) Space Optimization
The state machine approach is cleanest here.
- `held`: Max profit ending today holding a stock.
- `rest`: Max profit ending today being able to buy.
- `sold`: Max profit ending today having just sold.

```python
def max_profit_cooldown_optimized(prices: list[int]) -> int:
    held, rest, sold = float('-inf'), 0, 0

    for price in prices:
        prev_sold = sold
        sold = held + price
        held = max(held, rest - price)
        rest = max(rest, prev_sold)

    return max(sold, rest)
```
- **Time Complexity:** O(n).
- **Space Complexity:** O(1).

---

### 5. Best Time to Buy and Sell Stock with Transaction Fee
`[MEDIUM]` `#dp-on-stocks` `#fee`

#### Problem Statement
Maximize profit with infinite transactions, but pay a transaction `fee` for each completed transaction.

#### Recurrence Relation
`solve(index, can_buy)`:
- `can_buy`: `max(-prices[index] + solve(index+1, 0), solve(index+1, 1))`
- `!can_buy`: `max(prices[index] - fee + solve(index+1, 1), solve(index+1, 0))`. The fee is subtracted upon selling.

---
#### a) Memoization (Top-Down)
```python
def max_profit_fee_memo(prices: list[int], fee: int) -> int:
    n = len(prices)
    dp = [[-1] * 2 for _ in range(n)]

    def solve(index, can_buy):
        if index == n: return 0
        if dp[index][can_buy] != -1: return dp[index][can_buy]

        if can_buy:
            profit = max(-prices[index] + solve(index + 1, 0), solve(index + 1, 1))
        else:
            profit = max(prices[index] - fee + solve(index + 1, 1), solve(index + 1, 0))

        dp[index][can_buy] = profit
        return profit

    return solve(0, 1)
```
- **Time Complexity:** O(n).
- **Space Complexity:** O(n) for the DP table + O(n) for recursion stack.

---
#### b) Tabulation (Bottom-Up)
```python
def max_profit_fee_tab(prices: list[int], fee: int) -> int:
    n = len(prices)
    dp = [[0] * 2 for _ in range(n + 1)]

    for index in range(n - 1, -1, -1):
        for can_buy in range(2):
            if can_buy:
                dp[index][can_buy] = max(-prices[index] + dp[index+1][0], dp[index+1][1])
            else:
                dp[index][can_buy] = max(prices[index] - fee + dp[index+1][1], dp[index+1][0])

    return dp[0][1]
```
- **Time/Space Complexity:** O(n).

---
#### c) Space Optimization
```python
def max_profit_fee_optimized(prices: list[int], fee: int) -> int:
    n = len(prices)
    ahead_can_buy, ahead_cannot_buy = 0, 0

    for i in range(n - 1, -1, -1):
        curr_can_buy = max(-prices[i] + ahead_cannot_buy, ahead_can_buy)
        curr_cannot_buy = max(prices[i] - fee + ahead_can_buy, ahead_cannot_buy)

        ahead_can_buy = curr_can_buy
        ahead_cannot_buy = curr_cannot_buy

    return ahead_can_buy
```
- **Time Complexity:** O(n).
- **Space Complexity:** O(1).
