### `[PATTERN] Variable-Size Sliding Window (Finding Length)`

This pattern is used for problems that ask for the **longest** or **shortest** subarray/substring that satisfies a certain condition. The key feature is that the window size is not fixed; it expands and shrinks based on the constraints of the problem.

#### The General Template
A common template for finding the **maximum** length involves expanding the window and only shrinking it when a condition is violated.

```python
def variable_window_template(arr):
    left = 0
    max_len = 0
    # State variables (e.g., hash map, count) to track the window's properties

    for right in range(len(arr)):
        # 1. EXPAND the window by including the element at `right`
        # Update state variables based on arr[right]

        # 2. SHRINK the window from the left while the condition is invalid
        while not is_window_valid(state):
            # Update state variables by removing arr[left]
            left += 1

        # 3. UPDATE RESULT: The window is now valid.
        # Calculate the current length and update max_len.
        max_len = max(max_len, right - left + 1)

    return max_len
```

---

### 1. Longest Substring Without Repeating Characters
`[MEDIUM]` `#sliding-window` `#hash-map`

#### Problem Statement
Given a string `s`, find the length of the longest substring that does not contain repeating characters.

#### Implementation Overview
We use a sliding window that maintains the property of having no repeated characters. A hash set is perfect for tracking the characters currently in the window.

1.  **State**: A hash set `char_set` stores the unique characters in the current window `[left, right]`.
2.  **Expand**: Move the `right` pointer, considering `s[right]`.
3.  **Shrink Condition**: The window is invalid if `s[right]` is already in `char_set`.
4.  **Shrink Logic**: While the window is invalid, remove `s[left]` from the `char_set` and increment `left`.
5.  **Update Result**: After the shrinking phase (if any), the window is guaranteed to be valid. Add `s[right]` to the set and update `max_len`.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$. Each character is added to and removed from the set at most once.
- **Space Complexity:** $O(\min(N, A))$, where $A$ is the alphabet size (e.g., 26 for lowercase English letters).

#### Python Code Snippet
```python
def length_of_longest_substring(s: str) -> int:
    char_set = set()
    left = 0
    max_len = 0

    for right in range(len(s)):
        # Shrink the window while s[right] is already in the set
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1

        # Expand the window
        char_set.add(s[right])

        # Update the result
        max_len = max(max_len, right - left + 1)

    return max_len
```

---

### 2. Longest Substring with At Most K Distinct Characters
`[MEDIUM]` `#sliding-window` `#hash-map`

#### Problem Statement
Given a string `s` and an integer `k`, find the length of the longest substring of `s` that contains at most `k` distinct characters.

#### Implementation Overview
This is a template problem for this pattern. The window is valid as long as it contains no more than `k` unique characters. A hash map is used to track the frequency of characters in the window.

1.  **State**: A hash map `char_counts` stores the frequency of each character in the window.
2.  **Expand**: Move `right` pointer and increment the count of `s[right]` in `char_counts`.
3.  **Shrink Condition**: The window is invalid if the number of unique characters (`len(char_counts)`) is greater than `k`.
4.  **Shrink Logic**: While invalid, decrement the count of `s[left]`. If a character's count drops to 0, remove it from the map. Increment `left`.
5.  **Update Result**: The window is now valid. Update `max_len`.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(K)$ to store character frequencies.

#### Python Code Snippet
```python
import collections

def length_of_longest_substring_k_distinct(s: str, k: int) -> int:
    if k == 0:
        return 0

    left = 0
    max_len = 0
    char_counts = collections.defaultdict(int)

    for right in range(len(s)):
        char_counts[s[right]] += 1

        while len(char_counts) > k:
            char_counts[s[left]] -= 1
            if char_counts[s[left]] == 0:
                del char_counts[s[left]]
            left += 1

        max_len = max(max_len, right - left + 1)

    return max_len
```

#### Related Problems
- **Fruit Into Baskets**: This is the same problem with `k=2`.

---

### 3. Longest Repeating Character Replacement
`[MEDIUM]` `#sliding-window` `#hash-map`

#### Problem Statement
You are given a string `s` and an integer `k`. You can change any character to any other character at most `k` times. Return the length of the longest substring containing the same letter you can get.

#### Implementation Overview
The key is to define the window's validity condition. A window is valid if the number of characters we need to change to make them all the same is at most `k`. This can be expressed as: `window_length - count_of_most_frequent_char <= k`.

1.  **State**: A hash map `char_counts` for frequencies and a variable `max_freq` to track the frequency of the most common character in the current window.
2.  **Expand**: Move `right` pointer, update `char_counts[s[right]]`, and update `max_freq`.
3.  **Shrink Condition**: The window is invalid if `(right - left + 1) - max_freq > k`.
4.  **Shrink Logic**: If invalid, decrement the count of `s[left]` and increment `left`. (Note: We don't need to re-calculate `max_freq` when shrinking, as the window size can only grow if we find a *new* `max_freq`).
5.  **Update Result**: The window size `right - left + 1` is always the candidate for the maximum length.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(26)$ or $O(1)$, as the alphabet size is constant.

#### Python Code Snippet
```python
import collections

def character_replacement(s: str, k: int) -> int:
    left = 0
    max_freq = 0
    char_counts = collections.defaultdict(int)

    for right in range(len(s)):
        char_counts[s[right]] += 1
        max_freq = max(max_freq, char_counts[s[right]])

        # Check if the window is invalid
        if (right - left + 1) - max_freq > k:
            char_counts[s[left]] -= 1
            left += 1

    # The result is the size of the final, largest valid window.
    return right - left + 1

---

### 4. Max Consecutive Ones III
`[MEDIUM]` `#sliding-window`

#### Problem Statement
Given a binary array `nums` and an integer `k`, return the maximum number of consecutive 1s in the array if you can flip at most `k` 0s.

#### Implementation Overview
This problem can be rephrased as "find the longest subarray containing at most `k` zeros". This makes it a classic variable-size sliding window problem.
1.  Initialize `left = 0`, `max_len = 0`, and `zero_count = 0`.
2.  Iterate through the array with the `right` pointer, expanding the window.
3.  If `nums[right]` is a `0`, increment `zero_count`.
4.  If `zero_count` becomes greater than `k`, the window is invalid. Shrink it from the left until it becomes valid again.
5.  After each potential shrink, the window `[left, right]` is valid. Calculate its length and update `max_len`.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(1)$.

#### Python Code Snippet
```python
def longest_ones(nums: list[int], k: int) -> int:
    left = 0
    zero_count = 0
    max_len = 0
    for right in range(len(nums)):
        if nums[right] == 0:
            zero_count += 1

        while zero_count > k:
            if nums[left] == 0:
                zero_count -= 1
            left += 1

        max_len = max(max_len, right - left + 1)

    return max_len
```
```

---

### 4. Minimum Window Substring
`[HARD]` `#sliding-window` `#hash-map`

#### Problem Statement
Given two strings, `s` (search string) and `t` (target), find the **minimum-length** substring of `s` that contains all the characters of `t` (including duplicates).

#### Implementation Overview
This problem asks for the *minimum* length, so the template is slightly different. We expand the window until it's valid, and then we shrink it as much as possible while it *remains* valid, updating our result at each step of the shrink phase.

1.  **State**: `t_counts` (a frequency map of `t`), `window_counts` (a frequency map of the current window), `have` (count of characters in the window that meet `t`'s frequency requirements), and `need` (total unique characters in `t`).
2.  **Expand**: Move `right` pointer. Update `window_counts`. If a character's count in the window now matches its required count in `t`, increment `have`.
3.  **Shrink Condition**: The window is ready to be shrunk once it becomes valid (`have == need`).
4.  **Shrink Logic**: While `have == need`:
    a. **Update Result**: The current window is a candidate for the minimum. Update the result if this window is smaller than the best one found so far.
    b. **Shrink from left**: Increment `left`. As `s[left]` is removed, update `window_counts`. If `s[left]` was a required character and its count now drops below what's needed, decrement `have`. This will eventually break the shrink loop.
5.  Continue until `right` reaches the end.

#### Time and Space Complexity
- **Time Complexity:** $O(N + M)$, where $N$ is the length of `s` and $M$ is the length of `t`.
- **Space Complexity:** $O(1)$ (constant alphabet size).

#### Python Code Snippet
```python
import collections

def min_window(s: str, t: str) -> str:
    if not t or not s:
        return ""

    t_counts = collections.Counter(t)
    need = len(t_counts)
    have = 0

    window_counts = {}
    res_indices, res_len = [-1, -1], float('inf')
    left = 0

    for right, char in enumerate(s):
        window_counts[char] = window_counts.get(char, 0) + 1

        if char in t_counts and window_counts[char] == t_counts[char]:
            have += 1

        # Shrink phase
        while have == need:
            # Update result
            if (right - left + 1) < res_len:
                res_indices = [left, right]
                res_len = right - left + 1

            # Shrink window from the left
            window_counts[s[left]] -= 1
            if s[left] in t_counts and window_counts[s[left]] < t_counts[s[left]]:
                have -= 1
            left += 1

    l, r = res_indices
    return s[l:r+1] if res_len != float('inf') else ""
```

---
### 5. Maximum Points You Can Obtain from Cards
`[MEDIUM]` `#sliding-window` `#prefix-sum`

#### Problem Statement
You must take exactly `k` cards from a row, either from the beginning or the end. Return the maximum possible score.

#### Implementation Overview
This problem can be cleverly transformed into a standard sliding window problem. Taking `k` cards from the ends is equivalent to *not taking* a contiguous subarray of size `n-k` from the middle. To maximize the sum of the cards taken, we must **minimize the sum of the subarray left behind**.

**Note:** This solution uses a **fixed-size** sliding window, not a variable one, but is included here due to its common association with windowing problems.

1.  **Rephrase**: Find the minimum sum subarray of size `n - k`.
2.  Calculate the `total_sum` of `cardPoints`.
3.  Use a fixed-size sliding window of size `window_size = n - k` to find the `min_window_sum`.
4.  The final answer is `total_sum - min_window_sum`.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the number of cards.
- **Space Complexity:** $O(1)$.

#### Python Code Snippet
```python
def max_score(cardPoints: list[int], k: int) -> int:
    n = len(cardPoints)
    window_size = n - k
    total_sum = sum(cardPoints)

    # If we must take all cards
    if window_size == 0:
        return total_sum

    # Calculate sum of the initial window of elements to be left behind
    current_window_sum = sum(cardPoints[:window_size])
    min_window_sum = current_window_sum

    # Slide the fixed-size window to find the minimum sum subarray
    for i in range(window_size, n):
        # Add the new element and remove the old one
        current_window_sum += cardPoints[i] - cardPoints[i - window_size]
        min_window_sum = min(min_window_sum, current_window_sum)

    return total_sum - min_window_sum
```
