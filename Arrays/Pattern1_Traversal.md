# Pattern 1: Basic Traversal & Simple Manipulations

This pattern covers problems that can be solved by iterating through the array once or a fixed number of times. The logic inside the loop is typically simple, involving comparisons, assignments, or basic arithmetic. These problems form the foundation of array manipulation.

---

### 1. Largest Element in an Array
`[FUNDAMENTAL]` `[EASY]` `#traversal`

#### Problem Statement
Given an array of integers, find the largest element in it.

*Example:*
- **Input:** `arr = [2, 5, 1, 3, 0]`
- **Output:** `5`
- **Input:** `arr = [-1, -5, -2]`
- **Output:** `-1`

#### Implementation Overview
The logic is to maintain a variable, `max_element`, that stores the largest element found so far.
1. Initialize `max_element` with the first element of the array or negative infinity.
2. Iterate through the array from the second element (`i = 1` to `n-1`).
3. In each iteration, compare the current element `arr[i]` with `max_element`.
4. If `arr[i]` is greater than `max_element`, update `max_element` to `arr[i]`.
5. After the loop completes, `max_element` will hold the largest value in the array.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the number of elements in the array. We traverse the array exactly once.
- **Space Complexity:** $O(1)$, as we only use a single variable `max_element` for storage.

#### Python Code Snippet
```python
def find_largest_element(arr):
  if not arr:
    return None
  max_element = arr[0]
  for i in range(1, len(arr)):
    if arr[i] > max_element:
      max_element = arr[i]
  return max_element
```

#### Tricks/Gotchas
- **Edge Case:** Always consider an empty array. The code above handles it by returning `None`. A single-element array is also a valid case and is handled correctly.

#### Related Problems
- 2. Second Largest Element in an Array

---

### 2. Second Largest Element in an Array without sorting
`[EASY]` `#traversal`

#### Problem Statement
Given an array of integers, find the second largest element. If no second largest element exists, return -1.

*Example:*
- **Input:** `arr = [12, 35, 1, 10, 34, 1]`
- **Output:** `34`
- **Input:** `arr = [10, 10, 10]`
- **Output:** `-1`

#### Implementation Overview
We can find the second largest element in a single pass. The idea is to maintain two variables: `largest` and `second_largest`.
1. Initialize `largest` and `second_largest` to a very small number (like `float('-inf')`).
2. Iterate through the array.
3. For each element `num` in the array:
    - If `num` is greater than `largest`, it means we have found a new largest element. We update `second_largest` to the old `largest`, and `largest` to `num`.
    - Else, if `num` is smaller than `largest` but greater than `second_largest`, it becomes the new `second_largest`.
4. After the loop, if `second_largest` is still `float('-inf')`, it means no second largest element was found.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the size of the array. We iterate through the array once.
- **Space Complexity:** $O(1)$, as we only use two variables `largest` and `second_largest`.

#### Python Code Snippet
```python
def find_second_largest(arr):
  if len(arr) < 2:
    return -1

  largest = float('-inf')
  second_largest = float('-inf')

  for num in arr:
    if num > largest:
      # Found a new largest, the old largest is now the second largest
      second_largest = largest
      largest = num
    elif num > second_largest and num < largest:
      # Found a new second largest
      second_largest = num

  return second_largest if second_largest != float('-inf') else -1
```

#### Tricks/Gotchas
- **Distinctness:** The condition `num < largest` is important to correctly handle arrays with duplicate largest elements like `[10, 5, 10]`.
- **Initialization:** Initializing with `float('-inf')` simplifies the logic and correctly handles negative numbers in the array.
- **No Second Largest:** If all elements are the same (e.g., `[5, 5, 5]`), there is no second largest. The check at the end handles this.

#### Related Problems
- 1. Largest Element in an Array

---

### 3. Check if the array is sorted
`[EASY]` `#traversal`

#### Problem Statement
Given an array of integers, determine if the array is sorted in non-decreasing (ascending) order.

*Example:*
- **Input:** `arr = [1, 2, 2, 3, 4]`
- **Output:** `True`
- **Input:** `arr = [1, 3, 2, 4, 5]`
- **Output:** `False`

#### Implementation Overview
This can be checked with a single pass through the array.
1. Iterate from the first element up to the second-to-last element (`i = 0` to `n-2`).
2. In each iteration, compare the current element `arr[i]` with the next element `arr[i+1]`.
3. If you find any pair where `arr[i] > arr[i+1]`, the array is not sorted, and you can immediately return `False`.
4. If the loop completes without finding such a pair, the array is sorted, so you return `True`.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the size of the array. In the worst case, we traverse the entire array.
- **Space Complexity:** $O(1)$, as no extra space is used.

#### Python Code Snippet
```python
def is_sorted(arr):
  n = len(arr)
  if n <= 1:
    return True
  for i in range(n - 1):
    if arr[i] > arr[i+1]:
      return False
  return True
```

#### Tricks/Gotchas
- **Edge Cases:** Empty arrays and single-element arrays are considered sorted. The code handles this correctly.
- **Strictly Increasing vs. Non-decreasing:** The problem usually implies non-decreasing (i.e., `[1, 2, 2, 3]` is sorted). Be clear on this requirement. If strictly increasing is needed, the check becomes `arr[i] >= arr[i+1]`.

#### Related Problems
- None in this list.

---

### 5. Left Rotate an array by one place
`[EASY]` `#traversal` `#inplace`

#### Problem Statement
Given an array, rotate its elements to the left by one position. The first element moves to the last position. This should be done in-place.

*Example:*
- **Input:** `arr = [1, 2, 3, 4, 5]`
- **Output:** `[2, 3, 4, 5, 1]`

#### Implementation Overview
This is a simple in-place manipulation.
1. Store the first element (`arr[0]`) in a temporary variable.
2. Iterate from the first element to the second-to-last element (`i = 0` to `n-2`).
3. In each step, shift the element at `i+1` to position `i`. That is, `arr[i] = arr[i+1]`.
4. After the loop, assign the value from the temporary variable to the last element of the array (`arr[n-1]`).

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the number of elements in the array. We shift $N-1$ elements.
- **Space Complexity:** $O(1)$, as we perform the rotation in-place using only one temporary variable.

#### Python Code Snippet
```python
def left_rotate_by_one(arr):
  n = len(arr)
  if n <= 1:
    return arr

  temp = arr[0]
  for i in range(n - 1):
    arr[i] = arr[i+1]
  arr[n-1] = temp
  return arr
```

#### Tricks/Gotchas
- **In-place Modification:** The goal is usually to modify the array in-place to save memory, which this solution does.
- **Edge Case:** An array with 0 or 1 elements does not need rotation.

#### Related Problems
- 6. Left rotate an array by D places

---

### 8. Linear Search
`[FUNDAMENTAL]` `[EASY]` `#traversal` `#search`

#### Problem Statement
Given an array of integers and a target value, find the index of the first occurrence of the target in the array. If the target is not present, return -1.

*Example:*
- **Input:** `arr = [4, 5, 6, 7, 0, 1, 2]`, `target = 0`
- **Output:** `4`
- **Input:** `arr = [1, 2, 3]`, `target = 4`
- **Output:** `-1`

#### Implementation Overview
This is the most straightforward search algorithm.
1. Iterate through the array from the first element to the last (`i = 0` to `n-1`).
2. In each iteration, check if the current element `arr[i]` is equal to the `target`.
3. If a match is found, return the current index `i`.
4. If the loop completes without finding the target, it means the element is not in the array. Return -1.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the size of the array. In the worst case, we iterate through the entire array.
- **Space Complexity:** $O(1)$, as no extra data structures are used.

#### Python Code Snippet
```python
def linear_search(arr, target):
  for i in range(len(arr)):
    if arr[i] == target:
      return i
  return -1
```

#### Tricks/Gotchas
- **Simplicity:** Don't overthink it. Linear search is the brute-force approach and is efficient for small or unsorted arrays.
- **Return Value:** Be clear about what to return if the element is not found (commonly -1, but could be `None` or an exception depending on requirements).

#### Related Problems
- Binary Search (for sorted arrays)

---

### 10. Find missing number in an array
`[EASY]` `#traversal` `#math` `#summation` `#bitwise`

#### Problem Statement
Given an array containing `N-1` distinct integers from the range `[1, N]`, find the single missing number.

*Example:*
- **Input:** `arr = [1, 2, 4, 5]`, `N = 5`
- **Output:** `3`

#### Implementation Overview
There are two common and efficient approaches.

**1. Summation Method:**
1. Calculate the expected sum of the first `N` natural numbers using the formula: `expected_sum = N * (N + 1) // 2`.
2. Calculate the actual sum of all elements present in the input array.
3. The missing number is the difference between the `expected_sum` and the `actual_sum`.

**2. XOR Method:**
1. The XOR property `x ^ x = 0` is key.
2. XOR all numbers from 1 to `N`. Let this be `xor_all_N`.
3. XOR all elements in the given array. Let this be `xor_array`.
4. The result of `xor_all_N ^ xor_array` will be the missing number, as all other numbers will appear twice in the combined set and cancel each other out.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the given range. Both the summation and XOR methods iterate roughly $N$ times.
- **Space Complexity:** $O(1)$, as we only use a few variables for storage.

#### Python Code Snippet (Summation)
```python
def find_missing_number_sum(arr, N):
  expected_sum = N * (N + 1) // 2
  actual_sum = sum(arr)
  return expected_sum - actual_sum
```

#### Python Code Snippet (XOR)
```python
def find_missing_number_xor(arr, N):
    xor_all_N = 0
    for i in range(1, N + 1):
        xor_all_N ^= i

    xor_array = 0
    for num in arr:
        xor_array ^= num

    return xor_all_N ^ xor_array
```

#### Tricks/Gotchas
- **Integer Overflow:** For very large `N`, the summation method could potentially lead to an integer overflow if using fixed-size integers in other languages. The XOR method avoids this.
- **Range:** This solution assumes the range is `[1, N]`. If the range is `[0, N-1]`, the formulas must be adjusted.

#### Related Problems
- 37. Find the repeating and missing number
- 12. Find the number that appears once, and other numbers twice

---

### 11. Maximum Consecutive Ones
`[EASY]` `#traversal` `#counting`

#### Problem Statement
Given a binary array (containing only 0s and 1s), find the maximum number of consecutive 1s.

*Example:*
- **Input:** `arr = [1, 1, 0, 1, 1, 1, 0, 1, 1]`
- **Output:** `3` (The streak of three 1s is the longest).

#### Implementation Overview
This can be solved in a single pass.
1. Initialize two variables: `max_count = 0` (to store the final answer) and `current_count = 0` (to track the current streak of 1s).
2. Iterate through the array.
3. If the current element is `1`, increment `current_count`.
4. If the current element is `0`:
    - The streak is broken. Compare `current_count` with `max_count` and update `max_count` if `current_count` is larger.
    - Reset `current_count` to `0`.
5. After the loop, there's a final check: `max_count = max(max_count, current_count)`. This is crucial for cases where the longest streak of 1s is at the very end of the array.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the number of elements in the array. We iterate through the array once.
- **Space Complexity:** $O(1)$, as we use only two variables to track counts.

#### Python Code Snippet
```python
def max_consecutive_ones(arr):
  max_count = 0
  current_count = 0
  for num in arr:
    if num == 1:
      current_count += 1
    else:
      max_count = max(max_count, current_count)
      current_count = 0
  # Final check in case the array ends with a streak of ones
  max_count = max(max_count, current_count)
  return max_count
```

#### Tricks/Gotchas
- **Final Update:** Forgetting the final `max(max_count, current_count)` after the loop is a common mistake. It handles inputs like `[1, 1, 1]`.

#### Related Problems
- This is a simple form of a sliding window problem.

---

### 12. Find the number that appears once, and other numbers twice
`[MEDIUM]` `#traversal` `#bitwise` `#xor`

#### Problem Statement
Given a non-empty array of integers, every element appears twice except for one. Find that single one.

*Example:*
- **Input:** `arr = [4, 1, 2, 1, 2]`
- **Output:** `4`

#### Implementation Overview
This problem has a beautiful and highly efficient solution using the bitwise XOR operator.
- The XOR operation has two key properties: `A ^ A = 0` (XORing a number with itself results in zero) and `A ^ 0 = A` (XORing a number with zero results in the number itself).
- It is also commutative and associative, meaning the order of operations does not matter.
1. Initialize a variable, `result`, to 0.
2. Iterate through every number in the array.
3. In each iteration, XOR `result` with the current number: `result ^= num`.
4. Because all duplicate numbers will cancel each other out (`num ^ num = 0`), the final value of `result` will be the one number that did not have a pair.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the size of the array. We iterate through the array once.
- **Space Complexity:** $O(1)$, as we only use a single variable for the result.

#### Python Code Snippet
```python
def find_single_number(arr):
  result = 0
  for num in arr:
    result ^= num
  return result
```

#### Tricks/Gotchas
- **The XOR Trick:** This is the core of the problem. While a hashmap could also solve it in O(N) time, it would use O(N) space. The XOR solution is optimal with O(N) time and O(1) space.
- **Problem Constraints:** This trick only works if all other numbers appear exactly twice. If they appear, say, three times, a different bitwise approach is needed.

#### Related Problems
- 10. Find missing number in an array
- Find the two numbers that appear once

---

### 20. Stock Buy and Sell
`[EASY]` `#traversal` `#greedy`

#### Problem Statement
You are given an array `prices` where `prices[i]` is the price of a given stock on the `i`-th day. You want to maximize your profit by choosing a **single day** to buy one stock and choosing a **different day in the future** to sell that stock. Return the maximum profit you can achieve. If you cannot achieve any profit, return 0.

*Example:*
- **Input:** `prices = [7, 1, 5, 3, 6, 4]`
- **Output:** `5` (Buy on day 2 (price=1) and sell on day 5 (price=6), profit = 6-1=5).
- **Input:** `prices = [7, 6, 4, 3, 1]`
- **Output:** `0` (No profitable transaction is possible).

#### Implementation Overview (Buy Once, Sell Once)
This is a classic problem that can be solved in a single pass. The key is to keep track of the minimum price seen so far and the maximum profit found.
1. Initialize `min_price` to a very large number (or `prices[0]`).
2. Initialize `max_profit` to 0.
3. Iterate through the `prices` array.
4. For each `price`:
    - If `price` is less than `min_price`, update `min_price` to `price`. This is a new best day to buy.
    - Otherwise, calculate the potential profit if we were to sell today: `profit = price - min_price`.
    - If this `profit` is greater than `max_profit`, update `max_profit`.
5. After the loop, `max_profit` holds the answer.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the number of days (prices). We make a single pass through the prices.
- **Space Complexity:** $O(1)$, as we only store the minimum price and maximum profit.

#### Python Code Snippet
```python
def max_profit_single(prices):
  if not prices:
    return 0

  min_price = float('inf')
  max_profit = 0

  for price in prices:
    if price < min_price:
      min_price = price
    else:
      profit = price - min_price
      if profit > max_profit:
        max_profit = profit

  return max_profit
```

#### Tricks/Gotchas
- **Problem Variation:** This is the "buy once, sell once" version. A different version allows multiple transactions, which has a different greedy solution. Always clarify which version is being asked.
- **Logic Flow:** The logic works because we always update our `min_price` to the lowest point. Any subsequent higher price is a candidate for a sale, and we just need to track the best one.

#### Related Problems
- 18. Kadane's Algorithm (Maximum Subarray Sum) - This problem can be transformed into Kadane's by looking at the array of daily price differences.

---

### 23. Leaders in an Array problem
`[EASY]` `#traversal` `#suffix-max`

#### Problem Statement
Given an integer array, find all the "leaders". An element is a leader if it is greater than or equal to all the elements to its right side. The rightmost element is always a leader.

*Example:*
- **Input:** `arr = [16, 17, 4, 3, 5, 2]`
- **Output:** `[17, 5, 2]`

#### Implementation Overview
A naive solution would be O(N^2) (for each element, scan its right side). The optimal solution is O(N) by traversing from right to left.
1. Initialize an empty list `leaders` to store the result.
2. The rightmost element `arr[n-1]` is always a leader, so we start there.
3. Initialize a variable `max_from_right` with the value of the rightmost element. Add this element to the `leaders` list.
4. Iterate through the array from the second-to-last element down to the first (`i = n-2` down to `0`).
5. For each element `arr[i]`, if it is greater than `max_from_right`, it is a leader because it's greater than the largest element to its right.
    - If it's a leader, add `arr[i]` to the `leaders` list.
    - Update `max_from_right = arr[i]` to reflect the new maximum.
6. Since we traversed from the right, the `leaders` list is in reverse order of their appearance in the original array. Reverse it before returning.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the number of elements in the array. We scan the array once.
- **Space Complexity:** $O(N)$ to store the result, or $O(1)$ if we exclude the space for the output list.

#### Python Code Snippet
```python
def find_leaders(arr):
  n = len(arr)
  if n == 0:
    return []

  leaders = []
  # The rightmost element is always a leader
  max_from_right = arr[n-1]
  leaders.append(max_from_right)

  # Traverse from right to left
  for i in range(n - 2, -1, -1):
    # If current element is greater than or equal to the max found so far from the right
    if arr[i] >= max_from_right:
      max_from_right = arr[i]
      leaders.append(max_from_right)

  # The leaders were added in reverse order, so we reverse the list
  return leaders[::-1]
```

#### Tricks/Gotchas
- **Traversal Direction:** Right-to-left is the key insight for an O(N) solution.
- **Output Order:** The problem statement doesn't always specify the required order of leaders. Reversing at the end is common to match the original array's relative order.

#### Related Problems
- None in this list.
