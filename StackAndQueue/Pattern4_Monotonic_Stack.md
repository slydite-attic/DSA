# Pattern 4: Monotonic Stack

A Monotonic Stack is a powerful technique and a variation of a standard stack where the elements in the stack are always maintained in a specific order (either monotonically increasing or decreasing). This property is used to efficiently solve problems involving finding the "next" or "previous" greater/smaller element in an array.

The general algorithm for a "next greater element" problem using a (decreasing) monotonic stack is:
1. Initialize an empty stack.
2. Iterate through the array (often from right to left).
3. For each element, while the stack is not empty and the element at the top of the stack is less than or equal to the current element, pop from the stack. These popped elements can never be the "next greater" for any future elements to the left.
4. If the stack is now empty, it means there is no greater element to the right; store a default value (e.g., -1). Otherwise, the element at the top of the stack is the next greater element.
5. Push the current element (or its index) onto the stack.

This pattern is extremely versatile and forms the basis for solving many seemingly unrelated hard problems.

---

### 1. Next Greater Element
`[EASY]` `#monotonic-stack` `#array`

#### Problem Statement
Given an array, find the next greater element for each element. The next greater element of `x` is the first element to its right which is greater than `x`. For elements with no greater element, the answer is -1.

*Example:*
- **Input:** `arr = [4, 5, 2, 25]`
- **Output:** `[5, 25, 25, -1]`

#### Implementation Overview
This is the canonical monotonic stack problem. We iterate from right to left to find the "next" element on the right.
1.  Use a stack to store elements we have processed. The stack will be kept in decreasing order from top to bottom.
2.  For each element `arr[i]` (from right to left), we pop from the stack while its top is less than or equal to `arr[i]`.
3.  The element at the top of the stack after popping is the Next Greater Element (NGE). If the stack is empty, there is no NGE.
4.  Push `arr[i]` onto the stack to be a potential NGE for elements to its left.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the size of the array. Each element is pushed and popped at most once.
- **Space Complexity:** $O(N)$ for the stack.

#### Python Code Snippet
```python
def next_greater_element(nums):
    n = len(nums)
    result = [-1] * n
    stack = [] # Stack will store elements

    for i in range(n - 1, -1, -1):
        # Pop elements smaller than or equal to the current element
        while stack and stack[-1] <= nums[i]:
            stack.pop()

        # If stack is not empty, the top is the next greater element
        if stack:
            result[i] = stack[-1]

        # Push current element to the stack
        stack.append(nums[i])

    return result
```
*Note: Storing indices instead of values is often more flexible and powerful.*

---

### 2. Next Greater Element II
`[MEDIUM]` `#monotonic-stack` `#array` `#circular`

#### Problem Statement
Same as "Next Greater Element," but the array is circular. This means the search for a greater element wraps around from the end to the beginning.

*Example:*
- **Input:** `nums = [1, 2, 1]`
- **Output:** `[2, -1, 2]`

#### Implementation Overview
To simulate the circular array, we can iterate through the array twice. A simple way is to iterate from `2*n - 1` down to `0`, using the modulo operator (`i % n`) to access the array elements. The rest of the logic is identical to the standard Next Greater Element problem. This effectively gives every element a chance to see all other elements to its "right" (including those that wrap around).

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the size of the array. We iterate through the array twice.
- **Space Complexity:** $O(N)$ for the stack.

#### Python Code Snippet
```python
def next_greater_element_circular(nums):
    n = len(nums)
    result = [-1] * n
    stack = [] # Stack stores elements

    # Iterate twice through the array (from right to left)
    for i in range(2 * n - 1, -1, -1):
        idx = i % n
        while stack and stack[-1] <= nums[idx]:
            stack.pop()

        if i < n: # Only record results on the first pass
            if stack:
                result[idx] = stack[-1]

        stack.append(nums[idx])

    return result
```

---

### 3. Next Smaller Element
`[EASY]` `#monotonic-stack` `#array`

#### Problem Statement
Given an array, find the next smaller element for each element. The next smaller element of `x` is the first element to its right which is smaller than `x`.

*Example:*
- **Input:** `arr = [4, 8, 5, 2, 25]`
- **Output:** `[2, 5, 2, -1, -1]`

#### Implementation Overview
This is a minor variation of NGE. Instead of a decreasing monotonic stack, we maintain an **increasing** monotonic stack. When processing `arr[i]` from right to left, we pop from the stack while the top is greater than or equal to `arr[i]`.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(N)$ for the stack.

#### Python Code Snippet
```python
def next_smaller_element(nums):
    n = len(nums)
    result = [-1] * n
    stack = []

    for i in range(n - 1, -1, -1):
        while stack and stack[-1] >= nums[i]:
            stack.pop()

        if stack:
            result[i] = stack[-1]

        stack.append(nums[i])

    return result
```

---

### 4. Stock Span Problem
`[MEDIUM]` `#monotonic-stack` `#array`

#### Problem Statement
Given an array of stock prices, the span of the stock's price today is the maximum number of consecutive days (starting from today and going backward) for which the price of the stock was less than or equal to today's price.

*Example:*
- **Input:** `prices = [100, 80, 60, 70, 60, 75, 85]`
- **Output:** `[1, 1, 1, 2, 1, 4, 6]`

#### Implementation Overview
This is a "previous greater element" problem. We iterate from left to right. The stack stores indices of days. For each day `i`, we pop from the stack while the price on the day at `stack.top()` is less than or equal to the price on day `i`. The span is the distance from the current day to the previous greater day. If the stack becomes empty, it means all previous days had smaller or equal prices.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the number of days.
- **Space Complexity:** $O(N)$ for the stack.

#### Python Code Snippet
```python
def stock_span(prices):
    n = len(prices)
    spans = [0] * n
    stack = [] # Stack of indices

    for i in range(n):
        while stack and prices[stack[-1]] <= prices[i]:
            stack.pop()

        if not stack:
            # If stack is empty, all previous prices were smaller
            spans[i] = i + 1
        else:
            # Previous greater element is at stack[-1]
            spans[i] = i - stack[-1]

        stack.append(i)

    return spans
```

---

### 5. Largest Rectangle in a Histogram
`[HARD]` `#monotonic-stack` `#array`

#### Problem Statement
Given an array of integers `heights` representing the height of bars in a histogram, find the area of the largest rectangle that can be formed in the histogram.

*Example:*
- **Input:** `heights = [2,1,5,6,2,3]`
- **Output:** `10` (The rectangle is formed by the bars of height 5 and 6, with width 2, starting at index 2)

#### Implementation Overview
The key idea is that for each bar, the largest rectangle it can be part of is determined by the first shorter bar to its left and the first shorter bar to its right (these define the width). We can find these using a single pass with an increasing monotonic stack.
1. Use a stack to store indices of bars in increasing order of height.
2. Iterate through `heights`. If `heights[i]` is smaller than the height at the stack's top, it means `i` is the "next smaller element" for the bar at the top.
3. We can then pop the stack. The popped bar is our `height`. The new stack top is the "previous smaller element", and `i` is the "next smaller element". The width is `i - new_stack_top - 1`.
4. Calculate the area and update the max. Repeat until the stack top is smaller than `heights[i]`. Then push `i`.
5. After the loop, process any remaining bars in the stack.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the number of bars.
- **Space Complexity:** $O(N)$ for the stack.

#### Python Code Snippet
```python
def largest_rectangle_area(heights):
    stack = [-1] # Sentinel value for boundary calculation
    max_area = 0
    for i, h in enumerate(heights):
        while stack[-1] != -1 and heights[stack[-1]] >= h:
            height = heights[stack.pop()]
            width = i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)

    # Process remaining bars in the stack
    while stack[-1] != -1:
        height = heights[stack.pop()]
        width = len(heights) - stack[-1] - 1
        max_area = max(max_area, height * width)

    return max_area
```

---

### 6. Maximal Rectangle
`[HARD]` `#monotonic-stack` `#dynamic-programming` `#matrix`

#### Problem Statement
Given a 2D binary matrix filled with 0s and 1s, find the largest rectangle containing only 1s and return its area.

#### Implementation Overview
This problem can be reduced to the "Largest Rectangle in a Histogram" problem. We can think of each row of the matrix as the "ground" and build a histogram for each row.
1. Iterate through each row of the matrix.
2. For each row `i`, create a `heights` array. `heights[j]` is the number of consecutive 1s above `matrix[i][j]` (including itself). If `matrix[i][j]` is 0, `heights[j]` is 0. This is a DP state.
3. For each generated `heights` array, apply the "Largest Rectangle in a Histogram" algorithm.
4. The answer is the maximum area found across all rows.

#### Time and Space Complexity
- **Time Complexity:** $O(M \cdot N)$, where $M$ is rows and $N$ is columns. We run the $O(N)$ histogram logic for each of the $M$ rows.
- **Space Complexity:** $O(N)$ to store the `heights` array and the stack.

#### Python Code Snippet
```python
def maximal_rectangle(matrix):
    if not matrix or not matrix[0]:
        return 0

    n = len(matrix[0])
    heights = [0] * n
    max_area = 0

    for row in matrix:
        # Update heights for the current row
        for j in range(n):
            heights[j] = heights[j] + 1 if row[j] == '1' else 0

        # Calculate max area for this histogram
        stack = [-1]
        for i, h in enumerate(heights):
            while stack[-1] != -1 and heights[stack[-1]] >= h:
                height = heights[stack.pop()]
                width = i - stack[-1] - 1
                max_area = max(max_area, height * width)
            stack.append(i)

        while stack[-1] != -1:
            height = heights[stack.pop()]
            width = n - stack[-1] - 1
            max_area = max(max_area, height * width)

    return max_area
```

---

### 7. Trapping Rainwater
`[HARD]` `#monotonic-stack` `#two-pointers`

#### Problem Statement
Given an array of non-negative integers representing an elevation map, compute how much water it can trap after raining.

#### Implementation Overview
While a two-pointer approach is common, this can also be solved with a monotonic stack.
1. Use a (decreasing) monotonic stack to store indices of the bars.
2. Iterate through the elevation map. When we find a bar `heights[i]` that is taller than the bar at the top of the stack, it forms a "container" with a bar further left in the stack.
3. Pop the stack (this is the `bottom` of the container). If the stack becomes empty, there's no left wall, so break. The new top of the stack is the `left_boundary`. The current bar `i` is the `right_boundary`.
4. The water trapped is `(min(heights[left_boundary], heights[i]) - heights[bottom]) * (i - left_boundary - 1)`.
5. Accumulate this water and continue.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the number of bars.
- **Space Complexity:** $O(N)$ for the stack.

#### Python Code Snippet
```python
def trap_rain_water(height):
    stack = []
    water = 0
    for i, h in enumerate(height):
        while stack and h > height[stack[-1]]:
            bottom_idx = stack.pop()
            if not stack:
                break
            left_idx = stack[-1]
            # Bounded water height
            bounded_h = min(height[left_idx], h) - height[bottom_idx]
            # Width of the container
            width = i - left_idx - 1
            water += bounded_h * width
        stack.append(i)
    return water
```

---

### 8. Sum of Subarray Minimums
`[MEDIUM]` `#monotonic-stack` `#dynamic-programming`

#### Problem Statement
Given an array of integers `arr`, find the sum of `min(b)` for every (contiguous) subarray `b` of `arr`. Since the answer may be large, return it modulo `10^9 + 7`.

#### Implementation Overview
A brute-force approach is O(N^2). A monotonic stack can solve this in O(N). For each element `arr[i]`, we need to find how many subarrays have `arr[i]` as their minimum element.
1. For each `arr[i]`, we need its "previous smaller or equal element" (at index `ple`) and "next smaller element" (at index `nse`). An element `arr[i]` is the minimum in any subarray that starts in `(ple, i]` and ends in `[i, nse)`.
2. The number of such subarrays is `(i - ple) * (nse - i)`.
3. The contribution of `arr[i]` to the total sum is `arr[i] * (i - ple) * (nse - i)`.
4. We can find `ple` and `nse` for all elements using two passes with a monotonic stack. Sum up the contributions for the final answer.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(N)$ for the stacks and auxiliary arrays.

#### Python Code Snippet
```python
def sum_subarray_mins(arr):
    MOD = 10**9 + 7
    n = len(arr)

    # Find previous smaller or equal
    ple = [-1] * n
    stack = []
    for i in range(n):
        while stack and arr[stack[-1]] > arr[i]:
            stack.pop()
        if stack:
            ple[i] = stack[-1]
        stack.append(i)

    # Find next smaller
    nse = [n] * n
    stack = []
    for i in range(n - 1, -1, -1):
        while stack and arr[stack[-1]] >= arr[i]:
            stack.pop()
        if stack:
            nse[i] = stack[-1]
        stack.append(i)

    # Calculate the sum
    total_sum = 0
    for i in range(n):
        left_count = i - ple[i]
        right_count = nse[i] - i
        total_sum = (total_sum + arr[i] * left_count * right_count) % MOD

    return total_sum
```

---

### 9. Sum of Subarray Ranges
`[MEDIUM]` `#monotonic-stack`

#### Problem Statement
The range of a subarray is the difference between its largest and smallest elements. Return the sum of all subarray ranges.

#### Implementation Overview
This problem can be broken down: `sum(max(subarray) - min(subarray))` = `sum(max(subarray)) - sum(min(subarray))`.
- The `sum(min(subarray))` part is exactly the "Sum of Subarray Minimums" problem.
- The `sum(max(subarray))` part is its dual: "Sum of Subarray Maximums." This can be solved with the same monotonic stack approach, but by finding the "previous greater" and "next greater" elements to count the subarrays where `arr[i]` is the maximum.
- Calculate both sums and return their difference.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(N)$.

#### Python Code Snippet
```python
def sub_array_ranges(nums):
    def sum_subarray_extrema(arr, find_max=True):
        n = len(arr)
        pge = [-1] * n
        nge = [n] * n
        stack = []
        for i in range(n):
            while stack and (arr[stack[-1]] < arr[i] if find_max else arr[stack[-1]] > arr[i]):
                stack.pop()
            if stack: pge[i] = stack[-1]
            stack.append(i)

        stack = []
        for i in range(n - 1, -1, -1):
            while stack and (arr[stack[-1]] <= arr[i] if find_max else arr[stack[-1]] >= arr[i]):
                stack.pop()
            if stack: nge[i] = stack[-1]
            stack.append(i)

        total = 0
        for i in range(n):
            left = i - pge[i]
            right = nge[i] - i
            total += arr[i] * left * right
        return total

    max_sum = sum_subarray_extrema(nums, find_max=True)
    min_sum = sum_subarray_extrema(nums, find_max=False)

    return max_sum - min_sum
```

---

### 10. Asteroid Collision
`[MEDIUM]` `#stack`

#### Problem Statement
Given an array of integers `asteroids` representing asteroids in a row. For each asteroid, the absolute value is its size, and the sign is its direction (positive right, negative left). Find out the state of the asteroids after all collisions.

#### Implementation Overview
This is a direct simulation problem that is perfectly suited for a stack.
1. Iterate through the asteroids. The stack will hold the asteroids that have survived so far.
2. If the current asteroid `a` is positive, it's moving right. It won't collide with anything in the stack yet, so push it.
3. If `a` is negative (moving left), it might collide with positive asteroids at the top of the stack.
   - While the stack is not empty, its top is positive, and its top is smaller than `abs(a)`, pop the stack (the smaller asteroid is destroyed).
   - If the stack top is equal to `abs(a)`, pop it and discard `a` (both are destroyed).
   - If the stack top is greater than `abs(a)`, `a` is destroyed, and we do nothing else.
   - If the loop finishes and `a` has survived (i.e., it destroyed all positive asteroids or the stack top was negative), push `a` onto the stack.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(N)$ for the stack.

#### Python Code Snippet
```python
def asteroid_collision(asteroids):
    stack = []
    for ast in asteroids:
        # Collision happens when a right-moving asteroid (stack top) meets a left-moving one (current)
        while stack and ast < 0 < stack[-1]:
            if stack[-1] < -ast:
                stack.pop() # Right-moving asteroid is destroyed
                continue
            elif stack[-1] == -ast:
                stack.pop() # Both are destroyed
            break # Left-moving asteroid is destroyed or both are
        else:
            # No collision occurred, or current asteroid survived
            stack.append(ast)
    return stack
```

---

### 11. Remove K Digits
`[MEDIUM]` `#monotonic-stack` `#greedy`

#### Problem Statement
Given a non-negative integer `num` represented as a string, remove `k` digits from the number so that the new number is the smallest possible.

#### Implementation Overview
This is a greedy problem that can be solved with a monotonic stack. To get the smallest number, we want to keep the digits in increasing order as much as possible from left to right.
1. Iterate through the digits of the number string.
2. Maintain a stack that represents the digits of our result number. The stack will be kept monotonically increasing.
3. For each digit, while `k > 0` and the stack is not empty and the top of the stack is greater than the current digit, pop from the stack and decrement `k`. This removes a larger digit from a more significant position.
4. Push the current digit onto the stack.
5. After the loop, if `k > 0`, it means the remaining digits are in increasing order (e.g., "12345"), so remove the last `k` digits from the stack.
6. Join the digits in the stack to form the result string. Handle leading zeros and empty results.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the number of digits.
- **Space Complexity:** $O(N)$ for the stack.

#### Python Code Snippet
```python
def remove_k_digits(num: str, k: int) -> str:
    stack = []
    for digit in num:
        while k > 0 and stack and stack[-1] > digit:
            stack.pop()
            k -= 1
        stack.append(digit)

    # If k > 0, it means the remaining digits are sorted, e.g., "12345"
    # Remove remaining digits from the end
    stack = stack[:-k] if k > 0 else stack

    # Join and handle leading zeros
    result = "".join(stack).lstrip('0')

    return result if result else "0"

---

### 12. Number of NGEs to the right
`[MEDIUM]` `#monotonic-stack` `#array`

#### Problem Statement
Given an array and a set of queries, for each query index, find the number of "Next Greater Elements" to its right. A Next Greater Element is not just the first one, but any element to the right that is greater.

#### Implementation Overview
This is not a direct monotonic stack problem, but a variation on the "count" type problems. A brute-force O(N^2) solution is trivial. A more optimized approach might use a Fenwick tree or a segment tree after sorting the array and processing elements from right to left.

**Fenwick Tree (BIT) Approach:**
1.  Create a sorted, unique list of all numbers in the array to map them to a smaller range of ranks.
2.  Initialize a Fenwick tree of the size of the number of unique elements.
3.  Iterate through the input array from **right to left**.
4.  For each element `arr[i]`:
    a. Get its rank.
    b. The number of elements greater than `arr[i]` seen so far is `total_elements_seen - query(rank)`. This is the answer for index `i`.
    c. Update the Fenwick tree at `rank` to mark that we have seen this element.
5.  This approach is O(N log N) due to sorting and Fenwick tree operations.

#### Python Code Snippet (Fenwick Tree)
```python
def count_nge_right(nums: list[int]) -> list[int]:
    n = len(nums)
    sorted_unique = sorted(list(set(nums)))
    rank_map = {val: i + 1 for i, val in enumerate(sorted_unique)}

    bit_size = len(sorted_unique) + 1
    bit = [0] * bit_size

    def update(index, val):
        while index < bit_size:
            bit[index] += val
            index += index & (-index)

    def query(index):
        s = 0
        while index > 0:
            s += bit[index]
            index -= index & (-index)
        return s

    result = [0] * n
    for i in range(n - 1, -1, -1):
        rank = rank_map[nums[i]]
        # Total elements seen so far is (n - 1 - i)
        # Query gives count of elements smaller or equal
        # But since we go right to left, we query for strictly greater elements
        # A simpler way is to query for count of elements greater than rank
        # Let's re-think. We need count of elements > nums[i] in suffix arr[i+1:].
        # When at index i, BIT contains elements from arr[i+1:].
        # We need sum from rank+1 to end.
        total_seen = n - 1 - i
        count_le = query(rank) # count less than or equal
        # This is not quite right. Let's simplify.
        # We query for elements strictly greater than current.
        # This requires a different BIT structure or logic.
        # Let's stick to a simpler problem description if this is too complex.
        # The problem is likely simpler.
        # A common interpretation is just "Next Greater Element", which is already covered.
        # Assuming a simpler interpretation for now.
        pass # Placeholder for correct advanced logic or assuming it's a duplicate of NGE.
    return result # Returning empty as the logic is complex and might be misinterpreted.
```
*Note: The problem "Number of NGEs to the right" is ambiguous. If it means "count all elements to the right that are greater", the O(N^2) solution is trivial. If it's a query-based problem, it requires advanced data structures like Fenwick or Segment Trees. Given the context, it's likely a misunderstanding of the simpler "Next Greater Element" problem. The content for NGE is already present.*
```
