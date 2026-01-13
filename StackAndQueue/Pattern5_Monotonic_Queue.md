# Pattern 5: Monotonic Queue (Sliding Window Maximum/Minimum)

A Monotonic Queue (or Deque) is a specialized data structure that maintains its elements in a sorted order. It's the go-to pattern for solving problems that involve finding the maximum or minimum value within a sliding window of a fixed size. By cleverly adding and removing elements from both ends of a deque, we can ensure that the maximum/minimum element in the current window is always at the front of the deque, allowing for O(1) access.

The overall time complexity for processing an entire array is O(n) because each element is added to and removed from the deque at most once.

---

### 1. Sliding Window Maximum
`[HARD]` `#monotonic-queue` `#deque` `#sliding-window`

#### Problem Statement
You are given an array of integers `nums` and an integer `k` representing the size of the sliding window. There is a sliding window which moves from the very left of the array to the very right. You can only see the `k` numbers in the window. Each time the sliding window moves right by one position, return the maximum value in the current window.

*Example:*
- **Input:** `nums = [1, 3, -1, -3, 5, 3, 6, 7]`, `k = 3`
- **Output:** `[3, 3, 5, 5, 6, 7]`
- **Explanation:**
  - Window `[1, 3, -1]`: max is 3
  - Window `[3, -1, -3]`: max is 3
  - Window `[-1, -3, 5]`: max is 5
  - Window `[-3, 5, 3]`: max is 5
  - Window `[5, 3, 6]`: max is 6
  - Window `[3, 6, 7]`: max is 7

#### Implementation Overview
We use a deque (double-ended queue) to store **indices** of elements in the current window. The deque will be kept in decreasing order of the values at those indices, meaning `nums[dq[0]]` is always the largest.

1.  Initialize an empty deque and a result array.
2.  Iterate through the array `nums` from left to right with index `i`.
3.  **Maintain the Monotonic Property**: Before adding the new element's index, remove all indices from the **rear** of the deque that correspond to values smaller than `nums[i]`. This ensures that the largest value's index is always moving towards the front.
4.  **Add New Element**: Add the current index `i` to the rear of the deque.
5.  **Remove Out-of-Bounds Elements**: If the index at the **front** of the deque is no longer in the current window (i.e., `dq[0] <= i - k`), remove it. This is because it's too old to be part of the current window.
6.  **Record Result**: Once the window is full (i.e., `i >= k - 1`), the maximum element for the current window is `nums[dq[0]]`. Append this to the result array.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$. Each element is added and removed from the deque at most once.
- **Space Complexity:** $O(K)$ for the deque, where $K$ is the window size.

#### Python Code Snippet
```python
from collections import deque

def max_sliding_window(nums, k):
    if not nums or k == 0:
        return []

    result = []
    dq = deque() # Stores indices of elements

    for i in range(len(nums)):
        # 1. Remove indices from the front that are out of the current window's bounds
        if dq and dq[0] <= i - k:
            dq.popleft()

        # 2. Maintain monotonic decreasing property by removing smaller elements from the back
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()

        # 3. Add current element's index to the back
        dq.append(i)

        # 4. The front of the deque is the max of the current window.
        #    Start adding to results once the first full window is formed.
        if i >= k - 1:
            result.append(nums[dq[0]])

    return result
```

#### Tricks/Gotchas
- **Indices vs. Values**: The deque must store **indices**, not values. Storing indices is the only reliable way to know when an element has fallen out of the sliding window's range.
- **Monotonic Direction**: For "Sliding Window Maximum", we maintain a monotonically *decreasing* queue (largest values at the front). For "Sliding Window Minimum", we would maintain a monotonically *increasing* queue (smallest values at the front).
- **Time Complexity**: The O(N) complexity can be confusing. Although there is a `while` loop inside the `for` loop, each element is pushed onto and popped from the deque at most once over the entire iteration, leading to an amortized O(1) time for each step.
