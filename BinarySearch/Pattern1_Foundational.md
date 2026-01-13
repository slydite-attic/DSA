# Pattern 1: Foundational Binary Search

This pattern covers the core binary search algorithm and its direct variations. These are the fundamental building blocks for all other binary search problems. The key is always a sorted search space and shrinking the problem by half in each step. A standard binary search template is used to find an element, or the position for an element, in a sorted array.

The core logic revolves around three pointers: `low`, `high`, and `mid`.
- `low`: The start of the search space.
- `high`: The end of the search space.
- `mid = low + (high - low) // 2`: The middle element, calculated this way to prevent integer overflow.

The loop continues as long as `low <= high`. Based on the comparison between `arr[mid]` and the `target`, we discard either the left or right half of the search space.

---

### 1. Binary Search to Find X
`[FUNDAMENTAL]` `[EASY]` `#binary-search` `#core-logic`

#### Problem Statement
Given a sorted array of `n` elements and a target element `t`, find the index of `t` in the array. Return -1 if the target is not found.

*Example:*
- **Input:** `arr = [2, 3, 5, 7, 9]`, `target = 7`
- **Output:** `3`
- **Input:** `arr = [1, 4, 5, 8]`, `target = 6`
- **Output:** `-1`

#### Implementation Overview
This is the standard binary search algorithm.
1.  Initialize `low = 0` and `high = n - 1`.
2.  While `low <= high`:
    -   Calculate `mid`.
    -   If `arr[mid] == target`, we have found the element, return `mid`.
    -   If `arr[mid] < target`, the target must be in the right half, so we discard the left half by setting `low = mid + 1`.
    -   If `arr[mid] > target`, the target must be in the left half, so we discard the right half by setting `high = mid - 1`.
3.  If the loop finishes, the target was not found, so return -1.

#### Time and Space Complexity
- **Time Complexity:** $O(\log N)$, where $N$ is the size of the array. The search space is halved in each step.
- **Space Complexity:** $O(1)$, as we use only a few variables.

#### Python Code Snippet
```python
def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = low + (high - low) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1
```

#### Tricks/Gotchas
- **Loop Condition:** The `low <= high` condition is important. If it were `low < high`, the loop would terminate one element too early, failing to check the last remaining element.
- **Integer Overflow:** `mid = low + (high - low) // 2` is preferred over `mid = (low + high) // 2` in languages with fixed-size integers to prevent potential overflow if `low` and `high` are very large.

---

### 2. Implement Lower Bound
`[FUNDAMENTAL]` `[MEDIUM]` `#binary-search` `#lower-bound`

#### Problem Statement
Given a sorted array and a value `x`, find the index of the first element in the array that is **greater than or equal to `x`**. This is also known as the "lower bound" of `x`. If no such element exists, return the length of the array.

*Example:*
- **Input:** `arr = [1, 2, 2, 3, 4, 5]`, `x = 2`
- **Output:** `1` (The first element >= 2 is at index 1)
- **Input:** `arr = [1, 2, 3, 4, 5]`, `x = 6`
- **Output:** `5` (No element is >= 6, so we return the length of the array)

#### Implementation Overview
1.  Initialize `low = 0`, `high = n - 1`.
2.  Initialize `ans = n` (the default answer if no element is found).
3.  Loop while `low <= high`.
4.  If `arr[mid] >= x`: This element is a potential answer. We store it (`ans = mid`) and then try to find an even earlier one by searching in the left half (`high = mid - 1`).
5.  If `arr[mid] < x`: The element is too small. We must search in the right half (`low = mid + 1`).
6.  Return `ans`.

#### Time and Space Complexity
- **Time Complexity:** $O(\log N)$, where $N$ is the size of the array.
- **Space Complexity:** $O(1)$.

#### Python Code Snippet
```python
def lower_bound(arr, x):
    low, high = 0, len(arr) - 1
    ans = len(arr)
    while low <= high:
        mid = low + (high - low) // 2
        if arr[mid] >= x:
            ans = mid
            high = mid - 1
        else:
            low = mid + 1
    return ans
```

#### Tricks/Gotchas
- **The "Potential Answer" Logic:** The key is to realize that when `arr[mid] >= x`, `mid` is a *candidate* for the answer, but there might be a better one to its left. That's why we store it and continue searching left.

---

### 3. Implement Upper Bound
`[FUNDAMENTAL]` `[MEDIUM]` `#binary-search` `#upper-bound`

#### Problem Statement
Given a sorted array and a value `x`, find the index of the first element in the array that is **strictly greater than `x`**. This is the "upper bound" of `x`.

*Example:*
- **Input:** `arr = [1, 2, 2, 3, 4, 5]`, `x = 2`
- **Output:** `3` (The first element > 2 is `3` at index 3)
- **Input:** `arr = [1, 2, 3]`, `x = 3`
- **Output:** `3` (No element is > 3, so we return the length of the array)

#### Implementation Overview
The implementation is nearly identical to `lower_bound`, with a small change in the comparison.
1.  Initialize `low = 0`, `high = n - 1`, and `ans = n`.
2.  Loop while `low <= high`.
3.  If `arr[mid] > x`: This is a potential answer. Store it (`ans = mid`) and search for a better one in the left half (`high = mid - 1`).
4.  If `arr[mid] <= x`: The element is too small or equal. We must search in the right half (`low = mid + 1`).
5.  Return `ans`.

#### Time and Space Complexity
- **Time Complexity:** $O(\log N)$, where $N$ is the size of the array.
- **Space Complexity:** $O(1)$.

#### Python Code Snippet
```python
def upper_bound(arr, x):
    low, high = 0, len(arr) - 1
    ans = len(arr)
    while low <= high:
        mid = low + (high - low) // 2
        if arr[mid] > x:
            ans = mid
            high = mid - 1
        else:
            low = mid + 1
    return ans
```

#### Tricks/Gotchas
- **Strict vs. Non-Strict:** The only difference from `lower_bound` is the strict inequality (`>`) instead of (`>=`).

---

### 4. Search Insert Position
`[EASY]` `#binary-search` `#lower-bound`

#### Problem Statement
Given a sorted array of distinct integers and a target value, return the index if the target is found. If not, return the index where it would be if it were inserted in order.

*Example:*
- **Input:** `nums = [1, 3, 5, 6]`, `target = 5`
- **Output:** `2`
- **Input:** `nums = [1, 3, 5, 6]`, `target = 2`
- **Output:** `1`

#### Implementation Overview
This problem is a direct application of **Lower Bound**. The definition of `lower_bound` (the first element greater than or equal to x) is exactly the index where the element should be inserted to maintain the sorted order. The implementation is identical to `lower_bound`.

#### Time and Space Complexity
- **Time Complexity:** $O(\log N)$, where $N$ is the size of the array.
- **Space Complexity:** $O(1)$.

#### Python Code Snippet
```python
def search_insert_position(nums, target):
    low, high = 0, len(nums) - 1
    ans = len(nums)
    while low <= high:
        mid = low + (high - low) // 2
        if nums[mid] >= target:
            ans = mid
            high = mid - 1
        else:
            low = mid + 1
    return ans
```

#### Related Problems
- `Implement Lower Bound`

---

### 5. Find the First and Last Occurrence of a Number
`[MEDIUM]` `#binary-search` `#lower-bound` `#upper-bound`

#### Problem Statement
Given a sorted array with duplicate elements, find the first and last occurrences of a given number `x`. If the number is not found, return `[-1, -1]`.

*Example:*
- **Input:** `nums = [5, 7, 7, 8, 8, 10]`, `target = 8`
- **Output:** `[3, 4]`

#### Implementation Overview
This problem can be solved by using `lower_bound` and `upper_bound`.
1.  **First Occurrence:** The first occurrence of `x` is simply the `lower_bound(arr, x)`.
2.  **Last Occurrence:** The last occurrence of `x` is one position to the left of the `upper_bound(arr, x)`. So, `last = upper_bound(arr, x) - 1`.
3.  We must check if the found indices are valid and if they actually point to the target element.

#### Time and Space Complexity
- **Time Complexity:** $O(\log N)$, where $N$ is the size of the array. We perform two binary searches.
- **Space Complexity:** $O(1)$.

#### Python Code Snippet
```python
def find_first_and_last(arr, target):
    def lower_bound(arr, x):
        low, high = 0, len(arr) - 1
        ans = len(arr)
        while low <= high:
            mid = low + (high - low) // 2
            if arr[mid] >= x:
                ans = mid
                high = mid - 1
            else:
                low = mid + 1
        return ans

    def upper_bound(arr, x):
        low, high = 0, len(arr) - 1
        ans = len(arr)
        while low <= high:
            mid = low + (high - low) // 2
            if arr[mid] > x:
                ans = mid
                high = mid - 1
            else:
                low = mid + 1
        return ans

    first = lower_bound(arr, target)
    if first == len(arr) or arr[first] != target:
        return [-1, -1]

    last = upper_bound(arr, target) - 1

    return [first, last]
```

#### Tricks/Gotchas
- **Validation:** After finding the lower bound, you must check if it's a valid index and if the element at that index is indeed the target. If not, the target doesn't exist in the array.

#### Related Problems
- `Count Occurrences of a Number`

---

### 6. Count Occurrences of a Number
`[EASY]` `#binary-search`

#### Problem Statement
Given a sorted array with duplicates, count the number of occurrences of a number `x`.

*Example:*
- **Input:** `nums = [5, 7, 7, 8, 8, 10]`, `target = 8`
- **Output:** `2`

#### Implementation Overview
This is a direct application of the previous problem.
1.  Find the index of the first occurrence of `x` using `lower_bound(x)`.
2.  Find the index of the first element strictly greater than `x` using `upper_bound(x)`.
3.  The count is the difference between these two indices: `count = upper_bound(x) - lower_bound(x)`.

#### Time and Space Complexity
- **Time Complexity:** $O(\log N)$, where $N$ is the size of the array.
- **Space Complexity:** $O(1)$.

#### Python Code Snippet
```python
def count_occurrences(arr, target):
    def lower_bound(arr, x):
        low, high = 0, len(arr) - 1
        ans = len(arr)
        while low <= high:
            mid = low + (high - low) // 2
            if arr[mid] >= x:
                ans = mid
                high = mid - 1
            else:
                low = mid + 1
        return ans

    def upper_bound(arr, x):
        low, high = 0, len(arr) - 1
        ans = len(arr)
        while low <= high:
            mid = low + (high - low) // 2
            if arr[mid] > x:
                ans = mid
                high = mid - 1
            else:
                low = mid + 1
        return ans

    first = lower_bound(arr, target)
    if first == len(arr) or arr[first] != target:
        return 0

    last_exclusive = upper_bound(arr, target)
    return last_exclusive - first
```

#### Related Problems
- `Find the First or Last Occurrence of a Number`

---

### 7. Floor and Ceil in Sorted Array
`[MEDIUM]` `#binary-search`

#### Problem Statement
Given a sorted array and a value `x`:
- **Floor:** Find the largest number in the array that is less than or equal to `x`.
- **Ceil:** Find the smallest number in the array that is greater than or equal to `x`.

*Example:*
- **Input:** `arr = [3, 4, 7, 8, 10]`, `x = 5`
- **Output:** Floor = `4`, Ceil = `7`

#### Implementation Overview
- **Ceil:** The ceiling of `x` is exactly what `lower_bound(x)` finds. We just need to return the element at the found index (if the index is valid).
- **Floor:** The floor requires a slight modification to the binary search logic to find the largest number `<= x`.

#### Time and Space Complexity
- **Time Complexity:** $O(\log N)$, where $N$ is the size of the array.
- **Space Complexity:** $O(1)$.

#### Python Code Snippet (Floor)
```python
def find_floor(arr, x):
    low, high = 0, len(arr) - 1
    ans = -1
    while low <= high:
        mid = low + (high - low) // 2
        if arr[mid] <= x:
            # This is a potential answer for the floor
            ans = arr[mid]
            # Try to find a larger one in the right half
            low = mid + 1
        else:
            # Element is too large, search in the left half
            high = mid - 1
    return ans
```
#### Python Code Snippet (Ceil)
```python
def find_ceil(arr, x):
    low, high = 0, len(arr) - 1
    ans = -1
    while low <= high:
        mid = low + (high - low) // 2
        if arr[mid] >= x:
            # This is a potential answer for the ceiling
            ans = arr[mid]
            # Try to find a smaller one in the left half
            high = mid - 1
        else:
            # Element is too small, search in the right half
            low = mid + 1
    return ans
```

#### Tricks/Gotchas
- **Return Value:** Be clear on what to return if the floor or ceil doesn't exist (e.g., finding the floor of 2 in `[3, 4, 5]`). The code above returns -1 in such cases.
