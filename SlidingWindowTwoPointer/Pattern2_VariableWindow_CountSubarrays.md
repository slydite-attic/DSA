### `[PATTERN] Variable-Size Sliding Window (Counting Subarrays)`

This advanced pattern is used for problems that require **counting the total number of subarrays/substrings** that satisfy a condition. It often applies to problems asking for a property to be *exactly* `K` (e.g., exactly `K` distinct integers, or a sum of *exactly* `K`).

#### The "At Most K" Conversion
Directly counting subarrays that match a condition *exactly* is difficult with a sliding window. The trick is to convert the problem into one that is easier to solve. The key identity is:

**`count(exactly K) = count(at most K) - count(at most K - 1)`**

The "at most K" version is much easier because it has a **monotonic property**: if a window `[left, right]` is valid (has at most `K` distinct elements), then all of its sub-windows (e.g., `[left+1, right]`) are also valid. This allows for a simple and efficient counting method within the sliding window loop.

#### The "At Most K" Template
This template is the building block for solving problems in this pattern.

```python
def at_most_k_template(arr, k):
    left = 0
    count = 0
    # State variables (e.g., hash map) to track the window's properties

    for right in range(len(arr)):
        # 1. EXPAND the window by including arr[right]
        # Update state...

        # 2. SHRINK the window while the "at most k" condition is invalid
        while not is_at_most_k_valid(state):
            # Update state by removing arr[left]
            left += 1

        # 3. COUNT: The window [left, right] is now valid.
        # All subarrays ending at `right` are also valid.
        # e.g., [left...right], [left+1...right], ..., [right...right]
        # The number of such subarrays is (right - left + 1).
        count += (right - left + 1)

    return count
```

---

### 1. Subarrays with K Different Integers
`[HARD]` `#sliding-window` `#counting` `#hash-map`

#### Problem Statement
Given an integer array `nums` and an integer `k`, return the number of "good" subarrays of `nums`. A good subarray is a contiguous subarray that has **exactly `k` different integers**.

#### Implementation Overview
This is the quintessential problem for the `exactly K = at most K - at most K-1` strategy.

1.  Implement a helper function, `atMostK(k_val)`, that solves the "at most k distinct integers" version of the problem using the template above.
2.  The main function simply returns `atMostK(k) - atMostK(k - 1)`.
3.  **Inside `atMostK(k_val)`**:
    - Use a hash map to track the frequencies of numbers in the window.
    - The window is invalid if `len(counts) > k_val`.
    - When the window is valid, add `right - left + 1` to the total count.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(N)$ for the hash map in worst case, but typically limited by $K$ distinct elements.

#### Python Code Snippet
```python
import collections

def subarrays_with_k_distinct(nums: list[int], k: int) -> int:
    def atMostK(k_val: int) -> int:
        left = 0
        count = 0
        counts = collections.defaultdict(int)
        for right in range(len(nums)):
            # Expand window
            if counts[nums[right]] == 0:
                k_val -= 1
            counts[nums[right]] += 1

            # Shrink window if it's invalid
            while k_val < 0:
                counts[nums[left]] -= 1
                if counts[nums[left]] == 0:
                    k_val += 1
                left += 1

            # Count valid subarrays
            count += right - left + 1
        return count

    return atMostK(k) - atMostK(k - 1)
```

---

### 2. Binary Subarray with Sum
`[MEDIUM]` `#sliding-window` `#prefix-sum` `#counting`

#### Problem Statement
Given a binary array `nums` and an integer `goal`, return the number of non-empty subarrays with a sum **exactly** equal to `goal`.

#### Implementation Overview
This is another "exactly K" problem, where `K` is the `goal` sum. We apply the same conversion.

1.  Define a helper function, `atMost(k)`, that counts subarrays with a sum of *at most* `k`.
2.  Return `atMost(goal) - atMost(goal - 1)`.
3.  **Inside `atMost(k)`**:
    - The state is just the `current_sum` of the window.
    - The window is invalid if `current_sum > k`.
    - When valid, add `right - left + 1` to the count.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(1)$.

#### Python Code Snippet
```python
def num_subarrays_with_sum(nums: list[int], goal: int) -> int:
    def atMost(k: int) -> int:
        if k < 0:
            return 0
        left = 0
        current_sum = 0
        count = 0
        for right in range(len(nums)):
            current_sum += nums[right]
            while current_sum > k:
                current_sum -= nums[left]
                left += 1
            count += right - left + 1
        return count

    return atMost(goal) - atMost(goal - 1)
```

---

### 3. Count Number of Nice Subarrays
`[MEDIUM]` `#sliding-window` `#counting` `#problem-reduction`

#### Problem Statement
Given an array of integers `nums` and an integer `k`, a "nice" subarray is one with **exactly `k` odd numbers**. Return the number of nice subarrays.

#### Implementation Overview
This problem is a great example of **problem reduction**. The actual values don't matter, only their parity.
1.  **Reduce**: Transform `nums` into a binary array where odd numbers are `1` and even numbers are `0`.
2.  The problem is now: "Find the number of subarrays in the binary array with a sum of exactly `k`."
3.  This is identical to the "Binary Subarray with Sum" problem. Apply the `atMost(k) - atMost(k - 1)` strategy.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(N)$ for the binary array (can be optimized to $O(1)$ by processing on the fly).

#### Python Code Snippet
```python
def number_of_subarrays(nums: list[int], k: int) -> int:
    # Reduce the problem by converting odd/even to 1/0
    binary_nums = [1 if num % 2 != 0 else 0 for num in nums]

    def atMost(goal: int) -> int:
        if goal < 0:
            return 0
        left = 0
        current_sum = 0
        count = 0
        for right in range(len(binary_nums)):
            current_sum += binary_nums[right]
            while current_sum > goal:
                current_sum -= binary_nums[left]
                left += 1
            count += right - left + 1
        return count

    return atMost(k) - atMost(k - 1)
```

---

### 4. Number of Substrings Containing All Three Characters
`[MEDIUM]` `#sliding-window` `#counting`

#### Problem Statement
Given a string `s` of 'a', 'b', and 'c', return the number of substrings that contain **at least one** of each character.

#### Implementation Overview
This problem uses a different but related counting insight. Instead of the `atMostK` conversion, we can count directly.
The key idea: if the window `[left, right]` is the *first* valid window ending at `right`, then any superstring that starts at or before `left` and ends at or after `right` is also valid. We can count these efficiently.

1.  **State**: `left` pointer and a frequency map `counts` for 'a', 'b', 'c'.
2.  **Expand**: Move `right` pointer and update `counts`.
3.  **Check Validity**: Use a `while` loop to check if the window `[left, right]` is valid (i.e., `counts` for 'a', 'b', 'c' are all > 0).
4.  **Count and Shrink**:
    - If the window is valid, it means the minimal valid window starting at `left` ends at `right`. Any substring starting *before* `left` and ending at `right` would also be valid. There are `left + 1` such substrings.
    - A simpler way to count: any substring ending at `right` or later that contains this valid window is also valid. The number of such substrings is `len(s) - right`.
    - After counting, we must shrink the window from the left (`counts[s[left]] -= 1; left += 1`) to find the next possible valid window.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(1)$.

#### Python Code Snippet
```python
def number_of_substrings(s: str) -> int:
    left = 0
    count = 0
    counts = {'a': 0, 'b': 0, 'c': 0}

    for right in range(len(s)):
        counts[s[right]] += 1

        # Once the window is valid, we can count all superstrings.
        while all(c > 0 for c in counts.values()):
            # The minimal window is [left, right].
            # Any substring starting at or before `left` and ending at `right` or later is valid.
            # A simpler insight: any substring that starts at `left` and ends at `right` or later is valid.
            # Number of such substrings = len(s) - right.
            count += len(s) - right

            # Shrink the window from the left to find the next valid minimal window.
            counts[s[left]] -= 1
            left += 1

    return count
```
