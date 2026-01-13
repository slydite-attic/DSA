### `[PATTERN] Direct Recursion & Divide and Conquer`

Recursion is a fundamental programming technique where a function calls itself to solve a problem. This pattern focuses on "direct" recursion, where the problem is broken down into smaller, self-similar subproblems. **Divide and Conquer** is a powerful algorithmic paradigm that is a classic application of this recursive pattern.

#### The Core of Recursion
Every recursive function has two essential parts:
1.  **Base Case**: A condition under which the function stops calling itself and returns a simple, known value. This prevents infinite loops.
2.  **Recursive Step**: The part of the function that breaks the problem down into a smaller version of itself and calls the function again on the smaller piece.

---

### The Divide and Conquer Paradigm

This strategy involves three steps:
1.  **Divide**: Break the given problem into subproblems of the same type.
2.  **Conquer**: Recursively solve these subproblems. If the subproblems are small enough, solve them directly (the base case).
3.  **Combine**: Combine the solutions of the subproblems to create the solution for the original problem.

---

### 1. Fibonacci Number
`[EASY]` `#recursion` `#divide-and-conquer`

#### Problem Statement
The Fibonacci numbers, commonly denoted `F(n)`, form a sequence such that each number is the sum of the two preceding ones, starting from 0 and 1. That is, `F(0) = 0`, `F(1) = 1`, and `F(n) = F(n - 1) + F(n - 2)` for `n > 1`. Given `n`, calculate `F(n)`.

#### Implementation Overview
This is a direct translation of the mathematical definition into a recursive function.
- **Base Case**: If `n` is 0 or 1, return `n`.
- **Recursive Step (Divide & Combine)**: The problem `F(n)` is "divided" into two subproblems, `F(n-1)` and `F(n-2)`. The results are "combined" by adding them together.

#### Time and Space Complexity
- **Time Complexity:** $O(2^n)$ for the naive recursive solution.
- **Space Complexity:** $O(n)$ for the recursion stack.

#### Python Code Snippet
```python
def fibonacci(n: int) -> int:
    """
    Calculates the Nth Fibonacci number using a naive recursive approach.
    """
    # Base Case
    if n <= 1:
        return n

    # Recursive Step (Divide and Conquer)
    return fibonacci(n - 1) + fibonacci(n - 2)
```

#### Tricks/Gotchas
- **Inefficiency**: This naive recursive solution is extremely inefficient for larger `n` (O(2^n) time complexity) because it re-computes the same Fibonacci numbers many times (e.g., `fib(5)` calls `fib(3)` twice). This problem of "overlapping subproblems" is the primary motivation for **Dynamic Programming**, which stores the results of subproblems to avoid re-computation.

---

### 2. Binary Search (Recursive)
`[EASY]` `#recursion` `#divide-and-conquer`

#### Problem Statement
Given a sorted array of integers `nums` and an integer `target`, write a function to search for `target` in `nums`. If `target` exists, then return its index. Otherwise, return -1.

#### Implementation Overview
Binary search is a perfect example of Divide and Conquer.
- **Divide**: The "division" step is finding the middle element of the current search space. This divides the array into two halves.
- **Conquer**: Compare the middle element with the `target`.
    - If they are equal, the problem is solved (the base case).
    - If the `target` is smaller, recursively search the *left* half.
    - If the `target` is larger, recursively search the *right* half.
- **Combine**: There is no "combine" step, as the result from the recursive call is the final answer.

#### Time and Space Complexity
- **Time Complexity:** $O(\log n)$.
- **Space Complexity:** $O(\log n)$ for the recursion stack.

#### Python Code Snippet
```python
def binary_search_recursive(nums: list[int], target: int, left: int, right: int) -> int:
    """
    Performs a binary search recursively on a sorted array.
    """
    if left > right:
        return -1 # Base case: search space is empty

    mid = left + (right - left) // 2

    if nums[mid] == target:
        return mid # Base case: target found
    elif nums[mid] > target:
        # Conquer the left half
        return binary_search_recursive(nums, target, left, mid - 1)
    else:
        # Conquer the right half
        return binary_search_recursive(nums, target, mid + 1, right)

# Wrapper function for initial call
def search(nums: list[int], target: int) -> int:
    return binary_search_recursive(nums, target, 0, len(nums) - 1)
```

---

### 3. Pow(x, n)
`[MEDIUM]` `#recursion` `#divide-and-conquer`

#### Problem Statement
Implement `pow(x, n)`, which calculates `x` raised to the power `n`.

#### Implementation Overview
A naive solution would multiply `x` by itself `n` times (O(n)). A much faster approach uses Divide and Conquer. The key idea is that `x^n = x^(n/2) * x^(n/2)`. If `n` is odd, `x^n = x * x^((n-1)/2) * x^((n-1)/2)`.

- **Base Case**: If `n` is 0, `x^0 = 1`. Return 1.
- **Divide**: The problem `pow(x, n)` is divided into the subproblem `pow(x, n/2)`.
- **Conquer**: Recursively call the function to compute `pow(x, n/2)`.
- **Combine**:
    - Square the result of the subproblem.
    - If `n` was odd, multiply by an extra `x`.
- **Negative `n`**: If `n` is negative, the result is `1 / pow(x, -n)`.

#### Time and Space Complexity
- **Time Complexity:** $O(\log n)$.
- **Space Complexity:** $O(\log n)$ for the recursion stack.

#### Python Code Snippet
```python
def my_pow(x: float, n: int) -> float:
    """
    Calculates x^n using a fast recursive (divide and conquer) approach.
    """
    if n == 0:
        return 1.0

    # Handle negative exponent
    if n < 0:
        return 1.0 / my_pow(x, -n)

    # Recursive step (Conquer)
    half = my_pow(x, n // 2)

    # Combine
    result = half * half
    if n % 2 == 1:
        result *= x

    return result
```
#### Tricks/Gotchas
- **Time Complexity**: This approach has a time complexity of O(log n), which is a massive improvement over the naive O(n) solution.

---

### 4. Merge Sort
`[MEDIUM]` `#sorting` `#divide-and-conquer`

#### Problem Statement
Given an array of integers `nums`, sort the array in ascending order using Merge Sort.

#### Implementation Overview
Merge Sort is the canonical example of the Divide and Conquer paradigm.
1.  **Divide**: Find the middle index of the array and split it into two halves: a left subarray and a right subarray.
2.  **Conquer**: Recursively call `merge_sort` on both the left and right subarrays. This continues until the subarrays have a size of 1 or 0, which are by definition sorted (the base case).
3.  **Combine**: Merge the two sorted subarrays back into a single, sorted array. This is done with a helper function, `merge`, which iterates through both subarrays with two pointers, picking the smaller element at each step to build the new sorted array.

#### Time and Space Complexity
- **Time Complexity:** $O(N \log N)$.
- **Space Complexity:** $O(N)$ for the temporary merge arrays and recursion stack.

#### Python Code Snippet
```python
def merge_sort(nums: list[int]) -> list[int]:
    """
    Sorts an array using the Merge Sort algorithm.
    """
    # Base case: an array with 0 or 1 elements is already sorted
    if len(nums) <= 1:
        return nums

    # 1. Divide
    mid = len(nums) // 2
    left_half = nums[:mid]
    right_half = nums[mid:]

    # 2. Conquer
    sorted_left = merge_sort(left_half)
    sorted_right = merge_sort(right_half)

    # 3. Combine
    return merge(sorted_left, sorted_right)

def merge(left: list[int], right: list[int]) -> list[int]:
    """
    Merges two sorted arrays into a single sorted array.
    """
    merged = []
    i, j = 0, 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    # Append any remaining elements
    merged.extend(left[i:])
    merged.extend(right[j:])

    return merged
```

---

### 5. Quick Sort
`[MEDIUM]` `#sorting` `#divide-and-conquer`

#### Problem Statement
Given an array of integers `nums`, sort the array in ascending order using Quick Sort.

#### Implementation Overview
Quick Sort is another famous Divide and Conquer sorting algorithm.
1.  **Divide**: Pick an element from the array, called the **pivot**. Reorder the array so that all elements with values less than the pivot come before it, while all elements with values greater than the pivot come after it. This step is called **partitioning**. After partitioning, the pivot is in its final sorted position.
2.  **Conquer**: Recursively call `quick_sort` on the sub-array of elements to the left of the pivot and on the sub-array of elements to the right of the pivot.
3.  **Combine**: No "combine" step is needed. Because the partitioning places the pivot in its correct final position, the recursive calls on the subarrays handle the rest. The array is sorted in-place.

#### Time and Space Complexity
- **Time Complexity:** $O(N \log N)$ on average, $O(N^2)$ worst case.
- **Space Complexity:** $O(\log N)$ for recursion stack.

#### Python Code Snippet
```python
def quick_sort(nums: list[int], low: int, high: int):
    """
    Sorts an array in-place using the Quick Sort algorithm.
    """
    if low < high:
        # 1. Divide: Find the partition index
        pi = partition(nums, low, high)

        # 2. Conquer: Recursively sort the two halves
        quick_sort(nums, low, pi - 1)
        quick_sort(nums, pi + 1, high)

def partition(nums: list[int], low: int, high: int) -> int:
    """
    Partitions the array using the last element as the pivot.
    Places the pivot element at its correct position in the sorted array.
    """
    pivot = nums[high]
    i = low - 1  # Index of smaller element

    for j in range(low, high):
        if nums[j] <= pivot:
            i += 1
            nums[i], nums[j] = nums[j], nums[i]

    # Place pivot in correct position
    nums[i + 1], nums[high] = nums[high], nums[i + 1]
    return i + 1

# Wrapper function for initial call
def sort_array(nums: list[int]) -> list[int]:
    quick_sort(nums, 0, len(nums) - 1)
    return nums

---

### 9. Reverse a Stack using Recursion
`[EASY]` `#recursion` `#stack`

#### Problem Statement
Given a stack, reverse its elements using only recursion and the standard stack operations. You are not allowed to use any explicit loops.

#### Implementation Overview
This solution is structurally similar to sorting a stack. It uses a main recursive function to peel off the top element and a helper function to insert that element at the bottom of the reversed smaller stack.
1.  **`reverse(stack)`:** The main function.
    - **Base Case:** If the stack is empty, there is nothing to reverse.
    - **Recursive Step:** Pop the top element (`temp`). Recursively call `reverse` on the rest of the stack. After the smaller stack is fully reversed, insert `temp` at the very bottom of it using a helper.
2.  **`insertAtBottom(stack, element)`:** This helper function inserts an element at the bottom of a stack.
    - **Base Case:** If the stack is empty, just push the `element`.
    - **Recursive Step:** Pop the top element (`top`), recursively call `insertAtBottom`, and then push `top` back onto the stack. This ensures `element` ends up at the bottom.

#### Time and Space Complexity
- **Time Complexity:** $O(N^2)$, where $N$ is the stack size.
- **Space Complexity:** $O(N)$ for recursion stack.

#### Python Code Snippet
```python
def reverse_stack(stack: list):
    if not stack:
        return

    temp = stack.pop()
    reverse_stack(stack)
    insert_at_bottom(stack, temp)

def insert_at_bottom(stack: list, element: int):
    if not stack:
        stack.append(element)
        return

    temp = stack.pop()
    insert_at_bottom(stack, element)
    stack.append(temp)
```

---

### 8. Sort a Stack using Recursion
`[MEDIUM]` `#recursion` `#stack`

#### Problem Statement
Given a stack, sort it using only recursion and the standard stack operations (`push`, `pop`, `isEmpty`). You are not allowed to use any explicit loops.

#### Implementation Overview
The solution involves two recursive functions, demonstrating a powerful way to use the call stack for storage.
1.  **`sortStack(stack)`:** The main function.
    - **Base Case:** If the stack is empty, it's sorted.
    - **Recursive Step:** Pop the top element (`temp`). Recursively call `sortStack` on the rest of the stack. After the smaller stack is sorted, insert `temp` back into its correct sorted position using a helper function.
2.  **`sortedInsert(stack, element)`:** This helper inserts an element into a sorted stack.
    - **Base Case:** If the stack is empty or the `element` is greater than the top, push `element`.
    - **Recursive Step:** If `element` is smaller than the top, pop the top element (`top`), recursively call `sortedInsert`, and then push `top` back.

#### Time and Space Complexity
- **Time Complexity:** $O(N^2)$.
- **Space Complexity:** $O(N)$ for recursion stack.

#### Python Code Snippet
```python
def sort_stack(stack: list):
    if not stack:
        return

    # Pop the top element
    temp = stack.pop()

    # Recursively sort the remaining stack
    sort_stack(stack)

    # Insert the popped element back in sorted order
    sorted_insert(stack, temp)

def sorted_insert(stack: list, element: int):
    # Base case: if stack is empty or element is greater than top
    if not stack or element > stack[-1]:
        stack.append(element)
        return

    # Pop elements until we find the right spot
    temp = stack.pop()
    sorted_insert(stack, element)

    # Push the popped elements back
    stack.append(temp)
```

---

### 7. Count Good Numbers
`[MEDIUM]` `#recursion` `#modular-arithmetic`

#### Problem Statement
A digit string is "good" if digits at even indices are even (0, 2, 4, 6, 8) and digits at odd indices are prime (2, 3, 5, 7). Given `n`, return the total number of good digit strings of length `n`, modulo 10^9 + 7.

#### Implementation Overview
This is a combinatorial problem that requires modular exponentiation for an efficient solution.
-   Number of choices for even indices: 5 (0, 2, 4, 6, 8)
-   Number of choices for odd indices: 4 (2, 3, 5, 7)
-   Number of even indices: `(n + 1) // 2`
-   Number of odd indices: `n // 2`
-   Total count = `(5 ^ num_even_indices) * (4 ^ num_odd_indices) % mod`.
-   We must use a recursive function for modular exponentiation (similar to `Pow(x, n)`) to handle large `n`.

#### Time and Space Complexity
- **Time Complexity:** $O(\log n)$ due to modular exponentiation.
- **Space Complexity:** $O(\log n)$ for recursion stack.

#### Python Code Snippet
```python
def count_good_numbers(n: int) -> int:
    MOD = 10**9 + 7

    def power(base, exp):
        if exp == 0:
            return 1
        half = power(base, exp // 2)
        half_sq = (half * half) % MOD
        if exp % 2 == 1:
            return (base * half_sq) % MOD
        else:
            return half_sq

    num_even_indices = (n + 1) // 2
    num_odd_indices = n // 2

    return (power(5, num_even_indices) * power(4, num_odd_indices)) % MOD
```

---

### 6. Recursive Implementation of atoi()
`[MEDIUM]` `#recursion` `#string-manipulation`

#### Problem Statement
Implement the `atoi()` function, which converts a string to an integer, handling whitespace, signs, and non-digit characters, while also checking for overflow. Implement the core logic recursively.

#### Implementation Overview
A recursive solution processes the string one character at a time. The main recursive function takes the current index, sign, and accumulated result as parameters.
1.  **Base Case:** The recursion stops when the index reaches the end of the string or a non-digit character is found.
2.  **Recursive Step:**
    - The function is called with the next index (`index + 1`).
    - The current character is converted to a digit.
    - Before adding the digit, check for potential overflow.
    - The digit is added to the accumulated result: `result = result * 10 + digit`.
3.  **Initial Call:** A non-recursive wrapper handles leading whitespace and the sign.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the string length.
- **Space Complexity:** $O(N)$ for recursion stack (iterative is better for this reason).

#### Python Code Snippet
```python
def myAtoi_recursive(s: str) -> int:
    INT_MAX, INT_MIN = 2**31 - 1, -2**31

    def solve(index, sign, result):
        if index >= len(s) or not s[index].isdigit():
            return sign * result

        digit = int(s[index])

        # Overflow check
        if result > INT_MAX // 10 or (result == INT_MAX // 10 and digit > 7):
            return INT_MAX if sign == 1 else INT_MIN

        return solve(index + 1, sign, result * 10 + digit)

    i, n = 0, len(s)
    while i < n and s[i] == ' ': i += 1

    sign = 1
    if i < n and s[i] in ['+', '-']:
        if s[i] == '-': sign = -1
        i += 1

    return solve(i, sign, 0)
```
```
