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
- **Space Complexity:** O(n * 2) for DP table + O(n) for recursion stack.

---
#### b) Space Optimization
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
#### a) Tabulation (Bottom-Up)
A 3D DP table `dp[index][can_buy][transactions]` can be used. A more common and intuitive tabulation uses a 2D array `dp[k][day]` or tracks the 4 states (buy1, sell1, buy2, sell2).

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
- **Time/Space Complexity:** O(n).

---
#### b) Space Optimization
The state machine approach is cleanest here.
- `held`: Max profit ending today holding a stock.
- `sold`: Max profit ending today having just sold.
- `rest`: Max profit ending today being able to buy.

```python
def max_profit_cooldown_optimized(prices: list[int]) -> int:
    held, sold, rest = float('-inf'), 0, 0 # Initialize the three states: holding a stock, just sold, and resting.

    for price in prices: # Iterate through each day's price.
        prev_sold = sold # Store the previous 'sold' state before updating it.
        # The max profit if we sell today is the profit from holding yesterday plus today's price.
        sold = held + price
        # The max profit if we hold a stock today is either holding from yesterday or buying today (from a resting state).
        held = max(held, rest - price)
        # The max profit if we are resting today is either resting from yesterday or having sold previously.
        rest = max(rest, prev_sold)

    return max(sold, rest) # The final max profit is the max of the 'sold' and 'rest' states.
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
    n = len(prices) # Get the number of days.
    dp = [[-1] * 2 for _ in range(n)] # Initialize a DP table for memoization.

    def solve(index, can_buy): # Recursive helper function.
        if index == n: return 0 # Base case: No more profit to be made after the last day.
        if dp[index][can_buy] != -1: return dp[index][can_buy] # Return memoized result.

        if can_buy: # If we are allowed to buy today,
            # Choose between buying (and not being able to buy tomorrow) or skipping.
            profit = max(-prices[index] + solve(index + 1, 0), solve(index + 1, 1))
        else: # If we must sell or hold,
            # Choose between selling (and paying the fee) or skipping.
            profit = max(prices[index] - fee + solve(index + 1, 1), solve(index + 1, 0))

        dp[index][can_buy] = profit # Memoize the result.
        return profit # Return the computed profit.

    return solve(0, 1) # Start from day 0 with the ability to buy.
```
- **Time/Space Complexity:** O(n).

---
#### b) Space Optimization
```python
def max_profit_fee_optimized(prices: list[int], fee: int) -> int:
    n = len(prices) # Get the number of days.
    ahead_can_buy, ahead_cannot_buy = 0, 0 # Initialize profits for the day ahead.

    for i in range(n - 1, -1, -1): # Iterate backwards from the second to last day.
        # Max profit if I can buy today: either buy now or skip.
        curr_can_buy = max(-prices[i] + ahead_cannot_buy, ahead_can_buy)
        # Max profit if I can sell today: either sell now (and pay the fee) or skip.
        curr_cannot_buy = max(prices[i] - fee + ahead_can_buy, ahead_cannot_buy)

        ahead_can_buy = curr_can_buy # Update the 'ahead' profits for the next iteration.
        ahead_cannot_buy = curr_cannot_buy

    return ahead_can_buy # The final result is the max profit if we can buy on day 0.
```
- **Time Complexity:** O(n).
- **Space Complexity:** O(1).
