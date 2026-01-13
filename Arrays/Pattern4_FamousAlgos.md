# Pattern 4: Famous Algorithms

This pattern covers problems whose optimal solutions are specific, named algorithms. Recognizing the problem as an instance of one of these patterns is the key to solving it efficiently. This category includes algorithms like Kadane's for maximum subarray sum, Moore's Voting Algorithm for majority elements, and the standard algorithm for finding the next permutation.

---

### 17. Majority Element (>n/2 times)
`[EASY]` `#voting-algorithm` `#moores-algorithm`

#### Problem Statement
Given an array of size `N`, find the element that appears more than `N/2` times. You may assume that the majority element always exists in the array.

*Example:*
- **Input:** `nums = [2, 2, 1, 1, 1, 2, 2]`
- **Output:** `2`

#### Implementation Overview
While a hashmap can solve this in O(N) time and space, **Boyer-Moore's Voting Algorithm** provides an elegant O(N) time and O(1) space solution.
1.  Initialize two variables: `candidate` to store the potential majority element and `count` to track its "votes".
2.  Iterate through the array.
3.  If `count` is 0, we set the current element `num` as the new `candidate` and set its `count` to 1.
4.  If the current `num` is the same as our `candidate`, we increment `count`.
5.  If the current `num` is different from our `candidate`, we decrement `count`. This is like a non-candidate canceling out a vote for the candidate.
6.  The element remaining as the `candidate` at the end of the loop is the majority element. Since the problem guarantees a majority element exists, a second pass to verify its count is not strictly necessary.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the size of the array. We iterate through the array once.
- **Space Complexity:** $O(1)$, as we use only two variables.

#### Python Code Snippet
```python
def majority_element_n2(nums):
    candidate = None
    count = 0
    for num in nums:
        if count == 0:
            candidate = num

        if num == candidate:
            count += 1
        else:
            count -= 1

    return candidate
```

#### Tricks/Gotchas
- **Guaranteed Existence:** The simple version of the algorithm relies on the guarantee that a majority element always exists. If it might not, a second pass is required to count the final candidate's frequency and verify it's > N/2.

#### Related Problems
- 30. Majority Element (n/3 times)

---

### 18. Kadane's Algorithm, maximum subarray sum
`[MEDIUM]` `#dynamic-programming` `#kadanes-algorithm`

#### Problem Statement
Given an integer array, find the contiguous subarray (containing at least one number) which has the largest sum and return its sum.

*Example:*
- **Input:** `nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]`
- **Output:** `6` (The subarray is `[4, -1, 2, 1]`)

#### Implementation Overview
This is the classic application of **Kadane's Algorithm**. It's a dynamic programming approach that solves the problem in O(N) time and O(1) space.
1.  Initialize two variables:
    -   `max_so_far`: Stores the maximum sum found for any subarray yet. Initialize it to the first element of the array.
    -   `current_sum`: Stores the sum of the subarray ending at the current position. Initialize to 0.
2.  Iterate through the array. For each element `num`:
    -   Add the current `num` to `current_sum`.
    -   Update `max_so_far = max(max_so_far, current_sum)`.
    -   If `current_sum` becomes negative, it means the subarray ending here is a "burden" to any future subarray. We are better off starting a new subarray from the next element. So, if `current_sum < 0`, we reset it to `0`.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the size of the array. We iterate through the array once.
- **Space Complexity:** $O(1)$, as we use only a few variables.

#### Python Code Snippet
```python
def max_subarray_sum(nums):
    max_so_far = nums[0]
    current_sum = 0

    for num in nums:
        current_sum += num
        if current_sum > max_so_far:
            max_so_far = current_sum

        if current_sum < 0:
            current_sum = 0

    return max_so_far
```

#### Tricks/Gotchas
- **Initialization:** Initializing `max_so_far` with the first element is crucial for handling arrays where all numbers are negative. In that case, the answer is the largest (least negative) number.
- **Order of Operations:** It's important to update `max_so_far` *before* resetting `current_sum`. This ensures that even if the array contains only one negative number, it is captured correctly.

#### Related Problems
- 19. Print subarray with maximum subarray sum
- 40. Maximum Product Subarray
- 20. Stock Buy and Sell (Buy once, sell once)

---

### 19. Print subarray with maximum subarray sum
`[MEDIUM]` `#dynamic-programming` `#kadanes-algorithm`

#### Problem Statement
An extension of Kadane's algorithm, where you also need to print the subarray that corresponds to the maximum sum.

*Example:*
- **Input:** `nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]`
- **Output:** `[4, -1, 2, 1]`

#### Implementation Overview
We augment the standard Kadane's algorithm by adding pointers to track the start and end of the maximum subarray found so far.
1.  Initialize `max_so_far`, `current_sum` as before.
2.  Initialize `start_index = 0`, `end_index = 0` to store the bounds of the final answer.
3.  Initialize `current_start = 0` to track the beginning of the subarray corresponding to `current_sum`.
4.  Iterate through the array with index `i`.
    -   Add `nums[i]` to `current_sum`.
    -   If `current_sum > max_so_far`:
        -   Update `max_so_far = current_sum`.
        -   Update the final pointers: `start_index = current_start`, `end_index = i`.
    -   If `current_sum < 0`:
        -   Reset `current_sum = 0`.
        -   A new potential subarray will start from the next element, so update `current_start = i + 1`.
5.  After the loop, the subarray is `nums[start_index : end_index + 1]`.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the size of the array. We iterate through the array once.
- **Space Complexity:** $O(1)$ (or $O(N)$ if the output subarray is considered extra space), as we use only a few variables to track indices.

#### Python Code Snippet
```python
def max_subarray_print(nums):
    max_so_far = nums[0]
    current_sum = 0
    start_index = 0
    end_index = 0
    current_start = 0

    for i, num in enumerate(nums):
        current_sum += num

        if current_sum > max_so_far:
            max_so_far = current_sum
            start_index = current_start
            end_index = i

        if current_sum < 0:
            current_sum = 0
            current_start = i + 1

    return nums[start_index : end_index + 1]
```

#### Tricks/Gotchas
- **Index Tracking:** The logic for updating `current_start` is the key addition. It must be updated only when the current subarray's sum becomes negative, indicating it's time to start fresh.

#### Related Problems
- 18. Kadane's Algorithm, maximum subarray sum

---

### 22. Next Permutation
`[MEDIUM]` `#array-manipulation`

#### Problem Statement
Implement the "next permutation" function, which rearranges numbers into the lexicographically next greater permutation of numbers. If such an arrangement is not possible, it must rearrange it as the lowest possible order (i.e., sorted in ascending order). The replacement must be in-place and use only constant extra memory.

*Example:*
- **Input:** `nums = [1, 2, 3]` -> **Output:** `[1, 3, 2]`
- **Input:** `nums = [3, 2, 1]` -> **Output:** `[1, 2, 3]`

#### Implementation Overview
This problem is solved by a specific, multi-step algorithm.
1.  **Find the pivot:** Traverse the array from right to left. Find the first element `nums[i]` which is smaller than the element to its right `nums[i+1]`. This `nums[i]` is our "pivot".
2.  **Handle the last permutation:** If no such pivot is found (i.e., the entire array is in descending order), it means we are at the last possible permutation. The "next" permutation is the very first one, so we just reverse the whole array.
3.  **Find the successor:** If a pivot is found at index `i`, traverse from right to left again. Find the first element `nums[j]` that is greater than the pivot `nums[i]`. This is the pivot's successor.
4.  **Swap:** Swap the pivot `nums[i]` with its successor `nums[j]`.
5.  **Reverse the suffix:** Reverse the part of the array to the right of the original pivot's position (from `i + 1` to the end). This ensures the suffix is in its smallest possible order.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the size of the array. In the worst case, we scan the array three times (find pivot, find successor, reverse).
- **Space Complexity:** $O(1)$, as we perform all operations in-place.

#### Python Code Snippet
```python
def next_permutation(nums):
    n = len(nums)
    pivot_index = -1
    # Step 1: Find the pivot (the first element from right that is smaller than its right neighbor)
    for i in range(n - 2, -1, -1):
        if nums[i] < nums[i+1]:
            pivot_index = i
            break

    # Step 2: If no pivot exists, the array is in descending order, reverse it
    if pivot_index == -1:
        nums.reverse()
        return

    # Step 3: Find the successor to the pivot (the smallest element to the right of pivot that is larger than pivot)
    for i in range(n - 1, pivot_index, -1):
        if nums[i] > nums[pivot_index]:
            # Step 4: Swap pivot and successor
            nums[i], nums[pivot_index] = nums[pivot_index], nums[i]
            break

    # Step 5: Reverse the suffix to the right of the pivot
    left, right = pivot_index + 1, n - 1
    while left < right:
        nums[left], nums[right] = nums[right], nums[left]
        left += 1
        right -= 1
```

#### Tricks/Gotchas
- **Edge Cases:** An empty or single-element array needs no changes.
- **In-place:** The algorithm must modify the array in-place.

#### Related Problems
- Previous Permutation

---

### 30. Majority Element (n/3 times)
`[MEDIUM]` `#voting-algorithm` `#moores-algorithm`

#### Problem Statement
Given an integer array of size `N`, find all elements that appear more than `N/3` times.

*Example:*
- **Input:** `nums = [3, 2, 3]` -> **Output:** `[3]`
- **Input:** `nums = [1, 1, 1, 3, 3, 2, 2, 2]` -> **Output:** `[1, 2]`

#### Implementation Overview
This is an extension of Boyer-Moore's Voting Algorithm. The key insight is that there can be at most two elements that appear more than `N/3` times.
1.  Initialize two candidates (`candidate1`, `candidate2`) and two counters (`count1`, `count2`).
2.  **First Pass (Finding Candidates):** Iterate through the array to find the two potential candidates.
    -   If `num` matches `candidate1`, increment `count1`.
    -   Else if `num` matches `candidate2`, increment `count2`.
    -   Else if `count1` is 0, set `candidate1 = num` and `count1 = 1`.
    -   Else if `count2` is 0, set `candidate2 = num` and `count2 = 1`.
    -   Else, decrement both `count1` and `count2`.
3.  **Second Pass (Verification):** The first pass gives us two *potential* candidates. We must verify their counts.
    -   Reset `count1` and `count2` to 0.
    -   Iterate through the array again, counting the actual occurrences of `candidate1` and `candidate2`.
4.  **Final Check:** Check if `count1 > N/3` and `count2 > N/3`. Add the qualifying candidates to the result list, ensuring not to add duplicates if `candidate1 == candidate2`.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the size of the array. We iterate through the array twice.
- **Space Complexity:** $O(1)$, as we use a constant number of variables.

#### Python Code Snippet
```python
def majority_element_n3(nums):
    if not nums:
        return []

    candidate1, count1 = None, 0
    candidate2, count2 = None, 0

    for num in nums:
        if num == candidate1:
            count1 += 1
        elif num == candidate2:
            count2 += 1
        elif count1 == 0:
            candidate1, count1 = num, 1
        elif count2 == 0:
            candidate2, count2 = num, 1
        else:
            count1 -= 1
            count2 -= 1

    # Second pass for verification
    result = []
    count1, count2 = 0, 0
    for num in nums:
        if num == candidate1:
            count1 += 1
        elif num == candidate2:
            count2 += 1

    n = len(nums)
    if count1 > n / 3:
        result.append(candidate1)
    if count2 > n / 3 and candidate1 != candidate2:
        result.append(candidate2)

    return result
```

#### Tricks/Gotchas
- **Verification Pass:** The second pass is not optional. The first pass only identifies candidates, not guarantees.
- **Distinct Candidates:** The check `candidate1 != candidate2` is important to avoid adding the same number to the result list twice if both candidates happen to be the same number.

#### Related Problems
- 17. Majority Element (>n/2 times)

---

### 40. Maximum Product Subarray
`[MEDIUM]` `#dynamic-programming` `#kadanes-algorithm`

#### Problem Statement
Given an integer array, find a contiguous non-empty subarray within the array that has the largest product, and return the product.

*Example:*
- **Input:** `nums = [2, 3, -2, 4]`
- **Output:** `6` (The subarray is `[2, 3]`)
- **Input:** `nums = [-2, 0, -1]`
- **Output:** `0`

#### Implementation Overview
This is a variation of Kadane's algorithm. The standard approach doesn't work directly because multiplying by a negative number can flip the largest product to the smallest and vice-versa.
1.  The key is to track both the maximum product and the minimum product ending at the current position.
2.  Initialize `max_so_far` (global max product), `max_ending_here`, and `min_ending_here` to the first element of the array.
3.  Iterate from the second element. For each `num`:
    -   Calculate the potential new max and min. The new max can be `num`, `num * old_max`, or `num * old_min`.
    -   Store the old `max_ending_here` in a temp variable because it's needed for the `min_ending_here` calculation.
    -   `max_ending_here = max(num, num * max_ending_here, num * min_ending_here)`
    -   `min_ending_here = min(num, num * temp_max, num * min_ending_here)`
    -   Update the overall `max_so_far` with the new `max_ending_here`.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the size of the array. We iterate through the array once.
- **Space Complexity:** $O(1)$, as we use only a few variables.

#### Python Code Snippet
```python
def max_product_subarray(nums):
    if not nums:
        return 0

    max_so_far = nums[0]
    max_ending_here = nums[0]
    min_ending_here = nums[0]

    for i in range(1, len(nums)):
        num = nums[i]

        # We need to store the old max_ending_here to calculate the new min_ending_here
        temp_max = max_ending_here

        max_ending_here = max(num, num * temp_max, num * min_ending_here)
        min_ending_here = min(num, num * temp_max, num * min_ending_here)

        max_so_far = max(max_so_far, max_ending_here)

    return max_so_far
```

#### Tricks/Gotchas
- **Zeroes:** A zero will reset the product chain. The logic `max(num, ...)` handles this correctly by allowing a new subarray to start at `num`.
- **Tracking Min Product:** The core insight is that a large negative number (the minimum product) is valuable, as it can become the maximum product if another negative number appears.

#### Related Problems
- 18. Kadane's Algorithm, maximum subarray sum
