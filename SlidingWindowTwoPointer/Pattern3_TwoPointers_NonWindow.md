### `[PATTERN] Two Pointers (Non-Window)`

While the Sliding Window technique uses two pointers to define a contiguous "window", the **Two Pointers** pattern is more general. It involves using two pointers to iterate through a data structure, but they don't necessarily form a window. Their movement is based on the properties of the data and the problem's constraints.

Common variations include:
- **Opposite Ends Converging**: One pointer starts at the beginning of a sorted array, and the other starts at the end. They move towards each other.
- **Slow and Fast Pointers**: Pointers move through a sequence at different speeds. This is extremely common for linked list cycle detection and is covered in the Linked List section.
- **Two-Sequence Iteration**: Each pointer iterates over a different array or string, and their movement is synchronized based on comparisons between the elements they point to.

---

### 1. Two Sum II - Input Array Is Sorted
`[EASY]` `#two-pointers` `#sorted-array`

#### Problem Statement
Given a 1-indexed array of integers `numbers` that is already sorted in non-decreasing order, find two numbers such that they add up to a specific `target` number. Return the indices of the two numbers (added by one) as an integer array `[index1, index2]`.

#### Implementation Overview
This is the canonical example of the "opposite ends converging" pattern.
1.  Initialize two pointers: `left = 0` and `right = len(numbers) - 1`.
2.  Loop as long as `left < right`.
3.  Calculate the `current_sum = numbers[left] + numbers[right]`.
4.  **Compare and Move**:
    - If `current_sum == target`, we have found the solution.
    - If `current_sum < target`, we need a larger sum, so we move the `left` pointer to the right (`left += 1`).
    - If `current_sum > target`, we need a smaller sum, so we move the `right` pointer to the left (`right -= 1`).

This works because the array is sorted. Moving `left` right always increases the sum, and moving `right` left always decreases it.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(1)$.

#### Python Code Snippet
```python
def two_sum_sorted(numbers: list[int], target: int) -> list[int]:
    left, right = 0, len(numbers) - 1

    while left < right:
        current_sum = numbers[left] + numbers[right]
        if current_sum == target:
            # Return 1-based indices
            return [left + 1, right + 1]
        elif current_sum < target:
            left += 1
        else: # current_sum > target
            right -= 1
```

---

### 2. 3Sum
`[MEDIUM]` `#two-pointers` `#sorting`

#### Problem Statement
Given an integer array `nums`, return all the triplets `[nums[i], nums[j], nums[k]]` such that `i != j`, `i != k`, and `j != k`, and `nums[i] + nums[j] + nums[k] == 0`. Notice that the solution set must not contain duplicate triplets.

#### Implementation Overview
This problem is a great example of building upon the "Two Sum II" pattern.
1.  **Sort the array**: Sorting is crucial for both the two-pointer approach and for handling duplicates.
2.  **Outer Loop**: Iterate through the array with a pointer `i`. `nums[i]` will be the first element of a potential triplet.
3.  **Handle Duplicates**: In the outer loop, if `i > 0` and `nums[i] == nums[i-1]`, we `continue`. This prevents generating duplicate triplets starting with the same number.
4.  **Inner Two-Pointer Problem**: For each `nums[i]`, the problem reduces to finding two numbers in the rest of the array (`nums[i+1:]`) that sum up to `-nums[i]`.
    - Set up `left = i + 1` and `right = len(nums) - 1`.
    - Use the "opposite ends converging" two-pointer logic to find pairs that sum to `target = -nums[i]`.
    - When a valid triplet is found, add it to the results.
    - **Handle Inner Duplicates**: After finding a valid triplet, move the `left` and `right` pointers inward, but also add logic to skip any duplicate elements to avoid duplicate triplets.

#### Time and Space Complexity
- **Time Complexity:** $O(N^2)$. Sorting takes $O(N \log N)$ and the nested loops take $O(N^2)$.
- **Space Complexity:** $O(1)$ (or $O(N)$ for sorting depending on implementation).

#### Python Code Snippet
```python
def three_sum(nums: list[int]) -> list[list[int]]:
    result = []
    nums.sort()

    for i in range(len(nums) - 2):
        # Skip duplicate first elements
        if i > 0 and nums[i] == nums[i-1]:
            continue

        left, right = i + 1, len(nums) - 1
        target = -nums[i]

        while left < right:
            current_sum = nums[left] + nums[right]
            if current_sum == target:
                result.append([nums[i], nums[left], nums[right]])
                # Skip duplicate second and third elements
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                left += 1
                right -= 1
            elif current_sum < target:
                left += 1
            else:
                right -= 1

    return result
```

---

### 3. Container With Most Water
`[MEDIUM]` `#two-pointers` `#greedy`

#### Problem Statement
You are given an integer array `height` of length `n`. There are `n` vertical lines drawn such that the two endpoints of the `i`-th line are `(i, 0)` and `(i, height[i])`. Find two lines that together with the x-axis form a container, such that the container contains the most water.

#### Implementation Overview
This is another "opposite ends converging" problem. The area of the container is determined by the shorter of the two lines (the height) and the distance between them (the width).
1.  Initialize `left = 0`, `right = len(height) - 1`, and `max_area = 0`.
2.  Loop while `left < right`.
3.  Calculate the current area: `width = right - left`, `h = min(height[left], height[right])`, `area = width * h`. Update `max_area`.
4.  **Move the Pointer**: To maximize the area, we need to find a greater height. The current height is limited by the shorter of the two lines. Moving the pointer of the *taller* line can't possibly increase the height, it will only decrease the width. Therefore, we should always move the pointer of the *shorter* line inward, in the hope of finding a taller line.
    - If `height[left] < height[right]`, move `left += 1`.
    - Otherwise, move `right -= 1`.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(1)$.

#### Python Code Snippet
```python
def max_area(height: list[int]) -> int:
    left, right = 0, len(height) - 1
    max_area = 0

    while left < right:
        h = min(height[left], height[right])
        width = right - left
        max_area = max(max_area, h * width)

        if height[left] < height[right]:
            left += 1
        else:
            right -= 1

    return max_area
```

---

### 4. Minimum Window Subsequence
`[HARD]` `#two-pointers` `#subsequence` `#dynamic-programming`

#### Problem Statement
Given strings `s1` and `s2`, return the minimum contiguous window (substring) in `s1` which contains `s2` as a **subsequence**.

#### Implementation Overview
This is a complex two-pointer problem because we are matching a subsequence, not a substring. A standard sliding window won't work. The core idea is to find a match for the subsequence, and then work backward to find the start of the minimal window containing that match.

1.  **Outer Loop (Forward Pass)**: Use a pointer `i` for `s1` and `j` for `s2`. Iterate `i` through `s1`. If `s1[i] == s2[j]`, we've found the next character of `s2`, so increment `j`.
2.  **Window Found**: Once `j` reaches `len(s2)`, we have found a valid subsequence ending at `s1[i]`. Let this be `end_of_window = i`.
3.  **Inner Loop (Backward Pass)**: Now, we must find the start of this window. Reset `j` to `len(s2) - 1` and use another pointer, `start_of_window`, initialized to `end_of_window`. Move `start_of_window` to the left. If `s1[start_of_window] == s2[j]`, we've found the previous character of the subsequence, so decrement `j`.
4.  **Minimal Window**: When the inner loop finishes (`j < 0`), `start_of_window` will be at the index of the first character of the subsequence match. The window is `s1[start_of_window : end_of_window + 1]`. Compare its length to the minimum found so far.
5.  **Continue Search**: To find other potential windows, reset `j=0` and continue the outer loop by setting `i = start_of_window + 1`.

#### Time and Space Complexity
- **Time Complexity:** $O(S \cdot T)$, where $S$ and $T$ are string lengths. In worst case we might rescan parts of $S$.
- **Space Complexity:** $O(1)$.

#### Python Code Snippet
```python
def min_window_subsequence(s1: str, s2: str) -> str:
    i, j = 0, 0
    min_len = float('inf')
    result = ""

    while i < len(s1):
        # Forward pass to find the end of a potential window
        if s1[i] == s2[j]:
            j += 1

        # If we've found all of s2 as a subsequence
        if j == len(s2):
            end = i

            # Backward pass to find the start of this specific window
            j -= 1
            while j >= 0:
                if s1[end] == s2[j]:
                    j -= 1
                end -= 1
            start = end + 1

            # Check if this window is the new minimum
            if (i - start + 1) < min_len:
                min_len = i - start + 1
                result = s1[start : i + 1]

            # Reset for the next search
            i = start # Continue search from the character after our window started
            j = 0

        i += 1

    return result
```
