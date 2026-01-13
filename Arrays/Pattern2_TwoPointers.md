# Pattern 2: Two Pointers & Sliding Window

The Two Pointers technique is one of the most versatile patterns for solving array and string problems. It involves using two integer pointers to iterate through a data structure, tracking different indices or positions. The pointers can move in the same direction, opposite directions, or a combination, depending on the problem.

The Sliding Window is a specific application of this pattern where the pointers (`left` and `right`) define a "window" or a subarray. The window size can be fixed or dynamic, and it slides over the array to find a solution.

---

### 4. Remove duplicates from Sorted array
`[EASY]` `#two-pointers` `#inplace`

#### Problem Statement
Given a sorted array of integers, remove the duplicates in-place such that each unique element appears only once. The relative order of the elements should be kept the same. Return the number of unique elements.

*Example:*
- **Input:** `arr = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]`
- **Output:** `5` (and `arr` is modified to `[0, 1, 2, 3, 4, _, _, _, _, _]`)

#### Implementation Overview
This is a classic application of the "fast and slow pointer" approach.
1. Use a "slow" pointer `i` that points to the last known unique element's position. Initialize `i = 0`.
2. Use a "fast" pointer `j` to iterate through the entire array, starting from the second element (`j = 1`).
3. As `j` iterates, if `arr[j]` is different from `arr[i]`, it means we've found a new unique element.
4. To record this new unique element, we increment `i` first, and then assign `arr[j]` to `arr[i]`.
5. The fast pointer `j` always moves forward. The slow pointer `i` only moves when a new unique element is found.
6. The number of unique elements is `i + 1`.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the size of the array. The fast pointer traverses the array once.
- **Space Complexity:** $O(1)$, as we are modifying the array in-place without using extra space.

#### Python Code Snippet
```python
def remove_duplicates(arr):
  if not arr:
    return 0

  i = 0 # Slow pointer indicates the position for the next unique element
  for j in range(1, len(arr)): # Fast pointer scans the array
    if arr[j] != arr[i]:
      i += 1
      arr[i] = arr[j]

  return i + 1
```

#### Tricks/Gotchas
- **In-place Modification:** The key is to modify the array directly without using extra space. The problem is judged on the first `k` (returned value) elements.
- **Sorted Array:** This algorithm relies on the array being sorted, as duplicates will be adjacent.

#### Related Problems
- 7. Move Zeros to end

---

### 6. Left rotate an array by D places
`[EASY]` `#two-pointers` `#reversal-algorithm`

#### Problem Statement
Given an array, rotate it to the left by `D` places. `D` can be greater than the size of the array. This should be done in-place.

*Example:*
- **Input:** `arr = [1, 2, 3, 4, 5, 6, 7]`, `D = 3`
- **Output:** `[4, 5, 6, 7, 1, 2, 3]`

#### Implementation Overview
While using a temporary array is straightforward, the "Reversal Algorithm" is an elegant in-place solution.
1. First, handle `D` being larger than array length `n` by taking `D = D % n`.
2. **Step 1:** Reverse the first `D` elements of the array. (e.g., `[1, 2, 3]` becomes `[3, 2, 1]`).
3. **Step 2:** Reverse the remaining `n-D` elements. (e.g., `[4, 5, 6, 7]` becomes `[7, 6, 5, 4]`).
4. **Step 3:** Reverse the entire array. (e.g., `[3, 2, 1, 7, 6, 5, 4]` becomes `[4, 5, 6, 7, 1, 2, 3]`).
Each reversal is a standard two-pointer operation (swapping elements from start and end, moving inwards).

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the number of elements in the array. Each element is swapped a constant number of times.
- **Space Complexity:** $O(1)$, as the reversal is done in-place.

#### Python Code Snippet
```python
def reverse(arr, start, end):
  while start < end:
    arr[start], arr[end] = arr[end], arr[start]
    start += 1
    end -= 1

def rotate_left(arr, d):
  n = len(arr)
  if n == 0:
    return
  d = d % n # Handle d > n
  if d == 0:
    return

  reverse(arr, 0, d - 1)
  reverse(arr, d, n - 1)
  reverse(arr, 0, n - 1)
```

#### Tricks/Gotchas
- **Modulus for D:** Always take `D % n` to handle cases where `D` is larger than the array length.
- **In-place:** The reversal algorithm is O(N) time and O(1) space.

#### Related Problems
- 5. Left Rotate an array by one place

---

### 7. Move Zeros to end
`[EASY]` `#two-pointers` `#inplace`

#### Problem Statement
Given an array of integers, move all the zeros to the end of it while maintaining the relative order of the non-zero elements.

*Example:*
- **Input:** `arr = [0, 1, 0, 3, 12]`
- **Output:** `[1, 3, 12, 0, 0]`

#### Implementation Overview
A highly effective method uses two pointers.
1. Use a pointer `j` to mark the position where the next non-zero element should be placed. Initialize `j = 0`.
2. Iterate through the array with a pointer `i` from `0` to `n-1`.
3. If `arr[i]` is a non-zero element, we swap it with the element at `arr[j]`. This effectively moves the non-zero element to the front part of the array.
4. We then increment `j`.
5. This process ensures that non-zero elements are moved to the front in the same relative order they appeared, because the `i` pointer always moves forward, and we only swap when `arr[i]` is non-zero.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the size of the array. We traverse the array once.
- **Space Complexity:** $O(1)$, as we perform the swaps in-place.

#### Python Code Snippet
```python
def move_zeros(arr):
  j = 0 # Pointer for the next non-zero element's position
  for i in range(len(arr)):
    if arr[i] != 0:
      arr[j], arr[i] = arr[i], arr[j] # Swap non-zero element to the front
      j += 1
```

#### Tricks/Gotchas
- **Relative Order:** The solution must preserve the original order of non-zero elements. The single-pass swap method shown above achieves this efficiently.

#### Related Problems
- 4. Remove duplicates from Sorted array
- 21. Rearrange array in alternating positive and negative items

---

### 9. Find the Union of two sorted arrays
`[EASY]` `#two-pointers` `#hash-set`

#### Problem Statement
Given two sorted arrays, find their union. The union should contain each element only once.

*Example:*
- **Input:** `arr1 = [1, 2, 3, 4, 5]`, `arr2 = [1, 2, 3, 6, 7]`
- **Output:** `[1, 2, 3, 4, 5, 6, 7]`

#### Implementation Overview
For sorted arrays, a two-pointer approach is very efficient.
1. Use a pointer `i` for `arr1` and `j` for `arr2`.
2. Create a `union` list to store the results.
3. While `i` and `j` are within their array bounds:
    - If `arr1[i] < arr2[j]`, add `arr1[i]` to the union (if it's not a duplicate) and increment `i`.
    - If `arr1[i] > arr2[j]`, add `arr2[j]` to the union (if it's not a duplicate) and increment `j`.
    - If `arr1[i] == arr2[j]`, add one of them to the union (if it's not a duplicate) and increment both `i` and `j`.
4. After the main loop, add any remaining elements from `arr1` or `arr2`.

#### Time and Space Complexity
- **Time Complexity:** $O(N + M)$, where $N$ and $M$ are the sizes of the two arrays. We iterate through both arrays once.
- **Space Complexity:** $O(N + M)$ to store the union list. If we don't count the output space, it's $O(1)$.

#### Python Code Snippet
```python
def find_union(arr1, arr2):
    i, j = 0, 0
    union = []

    while i < len(arr1) and j < len(arr2):
        val1, val2 = arr1[i], arr2[j]
        if val1 <= val2:
            if not union or union[-1] != val1:
                union.append(val1)
            i += 1
            if val1 == val2: # Move j pointer as well if elements are same
                j += 1
        else:
            if not union or union[-1] != val2:
                union.append(val2)
            j += 1

    # Add remaining elements from arr1
    while i < len(arr1):
        if not union or union[-1] != arr1[i]:
            union.append(arr1[i])
        i += 1

    # Add remaining elements from arr2
    while j < len(arr2):
        if not union or union[-1] != arr2[j]:
            union.append(arr2[j])
        j += 1

    return union
```

#### Tricks/Gotchas
- **Sorted Input:** This optimal approach assumes the input arrays are sorted. If not, using a `set` is easier: `sorted(list(set(arr1) | set(arr2)))`.
- **Handling Duplicates:** The check `if not union or union[-1] != ...` is crucial for ensuring the final union list has unique elements.

#### Related Problems
- 36. Merge two sorted arrays without extra space

---

### 13. Longest subarray with given sum K (positives)
`[MEDIUM]` `#two-pointers` `#sliding-window`

#### Problem Statement
Given an array of positive integers and an integer `K`, find the length of the longest subarray with a sum equal to `K`.

*Example:*
- **Input:** `arr = [4, 1, 1, 1, 2, 3, 5]`, `K = 5`
- **Output:** `4` (for subarray `[1, 1, 1, 2]`)

#### Implementation Overview
This is a classic sliding window problem. The window is a subarray defined by a `left` and `right` pointer.
1. Initialize `left = 0`, `right = 0`, `current_sum = 0`, `max_len = 0`.
2. Use the `right` pointer to expand the window by iterating through the array. In each step, add `arr[right]` to `current_sum`.
3. After expanding, check if the `current_sum` exceeds `K`. If so, shrink the window from the left by subtracting `arr[left]` and incrementing `left` until the sum is valid again.
4. If `current_sum == K`, we have a candidate subarray. Update `max_len = max(max_len, right - left + 1)`.
5. Repeat until `right` reaches the end of the array.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the size of the array. Each element is added and removed from the window at most once.
- **Space Complexity:** $O(1)$, as we use only a few variables.

#### Python Code Snippet
```python
def longest_subarray_with_sum_k(arr, k):
    left = 0
    current_sum = 0
    max_len = 0

    for right in range(len(arr)):
        current_sum += arr[right]

        while current_sum > k:
            current_sum -= arr[left]
            left += 1

        if current_sum == k:
            max_len = max(max_len, right - left + 1)

    return max_len
```

#### Tricks/Gotchas
- **Positive Numbers Only:** This sliding window approach works because the numbers are all positive. This guarantees that shrinking the window from the left will decrease the sum. This logic fails for arrays with negative numbers.
- **Time Complexity:** This solution is O(N) because each element is visited at most twice (once by the `right` pointer and once by the `left` pointer).

#### Related Problems
- 14. Longest subarray with sum K (Positives + Negatives) (requires hashmaps)
- 28. Count subarrays with given sum

---

### 15. 2Sum Problem
`[MEDIUM]` `#two-pointers` `#hashing`

#### Problem Statement
Given an array of integers `nums` and an integer `target`, return **indices** of the two numbers such that they add up to `target`. Assume that each input would have exactly one solution, and you may not use the same element twice.

*Example:*
- **Input:** `nums = [2, 7, 11, 15]`, `target = 9`
- **Output:** `[0, 1]`

#### Implementation Overview

**Method 1: Hashing (Most Common)**
This is the preferred method when indices are required, as it avoids sorting.
1. Create a hashmap `num_to_index` to store numbers and their indices.
2. Iterate through the array. For each number `num` at index `i`:
3. Calculate the required complement: `complement = target - num`.
4. Check if `complement` exists in the hashmap. If so, you've found the solution. Return `[num_to_index[complement], i]`.
5. If not, add the current `num` and its index `i` to the hashmap.

**Method 2: Two Pointers (If returning values or if sorting is allowed)**
1. This method requires the array to be sorted. If you need to return original indices, you must store them before sorting, e.g., `[(value, index), ...]`.
2. Initialize `left = 0` and `right = len(arr) - 1`.
3. Loop while `left < right`. If `arr[left] + arr[right]` equals the target, you've found the pair. If the sum is too small, increment `left`. If too large, decrement `right`.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$ for hashing (one pass), or $O(N \log N)$ for two pointers (due to sorting).
- **Space Complexity:** $O(N)$ for hashing (hashmap stores up to $N$ elements), or $O(1)$ for two pointers (if sorting is in-place and output is not counted).

#### Python Code Snippet (Hashing)
```python
def two_sum_hashing(nums, target):
    num_to_index = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_to_index:
            return [num_to_index[complement], i]
        num_to_index[num] = i
    return None
```

#### Tricks/Gotchas
- **Indices vs. Values:** Be clear about what the problem asks for. For original indices, the hashmap approach is far more direct. The two-pointer approach is great for variants where you just need to find if a pair exists or return their values.

#### Related Problems
- 31. 3-Sum Problem
- 32. 4-Sum Problem

---

### 16. Sort an array of 0's 1's and 2's
`[MEDIUM]` `#two-pointers` `#dutch-national-flag`

#### Problem Statement
Given an array containing only 0s, 1s, and 2s, sort it in-place. This is known as the Dutch National Flag problem.

*Example:*
- **Input:** `arr = [2, 0, 2, 1, 1, 0]`
- **Output:** `[0, 0, 1, 1, 2, 2]`

#### Implementation Overview
This is solved efficiently using three pointers that partition the array.
1. Initialize three pointers:
    - `low = 0`: Marks the end of the `0`'s section.
    - `mid = 0`: The current element being processed.
    - `high = len(arr) - 1`: Marks the beginning of the `2`'s section.
2. The array is partitioned into four sections: `0s | 1s | unsorted | 2s`.
3. Iterate while `mid <= high`:
    - If `arr[mid] == 0`: Swap `arr[low]` with `arr[mid]`. Increment both `low` and `mid`.
    - If `arr[mid] == 1`: The element is in its correct potential place. Just increment `mid`.
    - If `arr[mid] == 2`: Swap `arr[high]` with `arr[mid]`. Decrement `high`. **Do not** increment `mid`, as the new `arr[mid]` hasn't been processed yet.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the size of the array. We process each element at most once.
- **Space Complexity:** $O(1)$, as we perform the sorting in-place.

#### Python Code Snippet
```python
def sort_colors(arr):
    low, mid, high = 0, 0, len(arr) - 1

    while mid <= high:
        if arr[mid] == 0:
            arr[low], arr[mid] = arr[mid], arr[low]
            low += 1
            mid += 1
        elif arr[mid] == 1:
            mid += 1
        else: # arr[mid] == 2
            arr[high], arr[mid] = arr[mid], arr[high]
            high -= 1
```

#### Tricks/Gotchas
- **`mid` pointer logic:** The most subtle part is not incrementing `mid` when a 2 is found and swapped. This is because the element brought to `mid` from the `high` position has not yet been inspected and must be processed in the next iteration.

#### Related Problems
- 7. Move Zeros to end (a simpler, two-way partition)

---

### 21. Rearrange array in alternating positive and negative items
`[MEDIUM]` `#two-pointers`

#### Problem Statement
You are given an array of an equal number of positive and negative numbers. Rearrange the array so that positive and negative numbers appear alternatively, starting with a positive number. The relative order of positive numbers and negative numbers should be maintained.

*Example:*
- **Input:** `arr = [3, 1, -2, -5, 2, -4]`
- **Output:** `[3, -2, 1, -5, 2, -4]`

#### Implementation Overview
Since relative order must be preserved, we can't just partition. A simpler approach is to use extra space.
1. Create two separate lists, one for positive numbers (`pos`) and one for negative numbers (`neg`), by iterating through the original array. This preserves their relative order.
2. Create a new result array. Iterate from `0` to `n/2 - 1`. In each iteration, append one element from the `pos` list and one from the `neg` list.

*Note: There are O(1) space solutions but they are much more complex, involving rotations.*

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the size of the array. We iterate through the array a couple of times.
- **Space Complexity:** $O(N)$ to store the positive and negative lists and the result.

#### Python Code Snippet (O(N) space)
```python
def rearrange_alternating(arr):
    pos = [n for n in arr if n > 0]
    neg = [n for n in arr if n < 0]

    result = []
    for i in range(len(pos)):
        result.append(pos[i])
        result.append(neg[i])

    return result
```

#### Tricks/Gotchas
- **Problem Variation:** There are many variations of this problem. Some have unequal numbers of positives/negatives, some don't require order preservation. The version with equal numbers and order preservation is a common one.
- **In-place vs Extra Space:** The O(N) space solution is simple and intuitive. An O(1) space solution is a much harder problem.

#### Related Problems
- 7. Move Zeros to end

---

### 31. 3-Sum Problem
`[MEDIUM]` `#two-pointers` `#sorting`

#### Problem Statement
Given an integer array, return all the triplets `[arr[i], arr[j], arr[k]]` such that `i != j`, `i != k`, and `j != k`, and `arr[i] + arr[j] + arr[k] == 0`. The solution set must not contain duplicate triplets.

*Example:*
- **Input:** `nums = [-1, 0, 1, 2, -1, -4]`
- **Output:** `[[-1, -1, 2], [-1, 0, 1]]`

#### Implementation Overview
This problem builds on the 2-Sum problem.
1. **Sort the array.** This is essential for the two-pointer approach and for handling duplicates.
2. Iterate through the array with a pointer `i` from `0` to `n-3`.
3. **Handle duplicates for `i`:** If `i > 0` and `arr[i] == arr[i-1]`, `continue` to the next iteration to avoid processing the same starting number.
4. For each `arr[i]`, use the two-pointer technique on the rest of the array:
    - Set `left = i + 1` and `right = n - 1`. The target for the two-pointer sum is `target = -arr[i]`.
    - While `left < right`:
        - If `arr[left] + arr[right] == target`, you've found a triplet. Add it to the results.
        - **Handle duplicates for `left` and `right`:** After finding a valid triplet, move `left` and `right` inward while they are pointing to duplicate values to avoid duplicate triplets.
        - If the sum is less than the target, increment `left`.
        - If the sum is greater than the target, decrement `right`.

#### Time and Space Complexity
- **Time Complexity:** $O(N^2)$, where $N$ is the size of the array. Sorting takes $O(N \log N)$, and the two-pointer approach within the loop takes $O(N^2)$.
- **Space Complexity:** $O(1)$ (or $O(N)$ depending on sorting implementation), not counting the space for the output list.

#### Python Code Snippet
```python
def three_sum(nums):
    nums.sort()
    result = []
    n = len(nums)
    for i in range(n - 2):
        if i > 0 and nums[i] == nums[i-1]: # Skip duplicates for the first element
            continue

        left, right = i + 1, n - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total == 0:
                result.append([nums[i], nums[left], nums[right]])
                # Skip duplicates for the second and third elements
                while left < right and nums[left] == nums[left+1]:
                    left += 1
                while left < right and nums[right] == nums[right-1]:
                    right -= 1
                left += 1
                right -= 1
            elif total < 0:
                left += 1
            else:
                right -= 1
    return result
```

#### Tricks/Gotchas
- **Duplicate Handling:** This is the trickiest part. Sorting is the first step, followed by explicit checks to skip duplicate elements for all three positions in the triplet.

#### Related Problems
- 15. 2Sum Problem
- 32. 4-Sum Problem

---

### 32. 4-Sum Problem
`[HARD]` `#two-pointers` `#sorting`

#### Problem Statement
Given an array of `n` integers, return an array of all the unique quadruplets `[nums[a], nums[b], nums[c], nums[d]]` such that they sum up to a given `target`.

*Example:*
- **Input:** `nums = [1, 0, -1, 0, -2, 2]`, `target = 0`
- **Output:** `[[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]]`

#### Implementation Overview
This is a direct extension of the 3-Sum problem, solved by adding another layer of iteration.
1. **Sort the array.**
2. Use a nested loop structure. The outer loop iterates with pointer `i` from `0` to `n-4`. The inner loop iterates with `j` from `i+1` to `n-3`.
3. **Handle duplicates for `i` and `j`** similar to 3-Sum to avoid processing the same starting pairs.
4. For each pair `(arr[i], arr[j])`, solve the 2-Sum problem for the rest of the array (`arr[j+1]` to `arr[n-1]`).
    - The new target is `new_target = target - arr[i] - arr[j]`.
    - Set `left = j + 1` and `right = n - 1`.
    - Use the standard two-pointer approach to find pairs that sum to `new_target`, including duplicate handling for `left` and `right`.

#### Time and Space Complexity
- **Time Complexity:** $O(N^3)$, where $N$ is the size of the array. Sorting takes $O(N \log N)$, and the triply nested structure (two loops + one two-pointer scan) dominates.
- **Space Complexity:** $O(1)$ (or $O(N)$), not counting the output space.

#### Python Code Snippet
```python
def four_sum(nums, target):
    nums.sort()
    result = []
    n = len(nums)
    for i in range(n - 3):
        if i > 0 and nums[i] == nums[i-1]:
            continue
        for j in range(i + 1, n - 2):
            if j > i + 1 and nums[j] == nums[j-1]:
                continue

            left, right = j + 1, n - 1
            while left < right:
                total = nums[i] + nums[j] + nums[left] + nums[right]
                if total == target:
                    result.append([nums[i], nums[j], nums[left], nums[right]])
                    while left < right and nums[left] == nums[left+1]:
                        left += 1
                    while left < right and nums[right] == nums[right-1]:
                        right -= 1
                    left += 1
                    right -= 1
                elif total < target:
                    left += 1
                else:
                    right -= 1
    return result
```

#### Tricks/Gotchas
- **Complexity:** The time complexity is O(N^3) due to the nested loops and the two-pointer scan.
- **Extensive Duplicate Checks:** Duplicate handling is even more critical here and must be done at every level of the nested loops.

#### Related Problems
- 15. 2Sum Problem
- 31. 3-Sum Problem

---

### 36. Merge two sorted arrays without extra space
`[HARD]` `#two-pointers` `#gap-algorithm`

#### Problem Statement
Given two sorted arrays, `arr1` of size `n` and `arr2` of size `m`, merge them into a single sorted array without using any extra space. The final result should be that the first `n` elements (the smallest `n` of the combined set) are in `arr1` and the next `m` elements are in `arr2`.

*Example:*
- **Input:** `arr1 = [1, 4, 8, 10]`, `arr2 = [2, 3, 9]`
- **Output:** `arr1 = [1, 2, 3, 4]`, `arr2 = [8, 9, 10]`

#### Implementation Overview
This is a complex problem. The "Gap Algorithm" (based on Shell Sort) is one of the most efficient O((n+m)log(n+m)) solutions. A simpler, but less optimal O(n*m), method is also common.

**Method 1: Insertion Sort-based approach (O(n*m))**
1. Iterate through `arr1` with pointer `i`.
2. For each `arr1[i]`, compare it with the first element of `arr2`, `arr2[0]`.
3. If `arr1[i] > arr2[0]`, swap them.
4. After swapping, `arr2` is no longer sorted. The new element `arr1[i]` needs to be placed in its correct position in `arr2`. Use insertion sort to place `arr2[0]` correctly.
5. Repeat for all elements in `arr1`.

**Method 2: Gap Algorithm (O((n+m)log(n+m)))**
1. The core idea is to compare elements that are a certain `gap` distance apart and swap them if they are in the wrong order, considering both arrays as a single conceptual array.
2. The initial `gap` is `ceil((n + m) / 2)`.
3. The algorithm proceeds in a loop, reducing the `gap` by half in each iteration (`gap = ceil(gap / 2)`), until `gap` is 0.
4. Inside the loop, use two pointers to traverse the conceptual array and swap elements if out of order. The pointer logic is complex to handle moving between `arr1` and `arr2`.

#### Time and Space Complexity
- **Time Complexity:** $O(N \cdot M)$ for the insertion sort-based approach, or $O((N+M) \log (N+M))$ for the Gap Algorithm.
- **Space Complexity:** $O(1)$, as we merge in-place without using extra space (other than a few variables).

#### Python Code Snippet (Insertion-based)
```python
def merge_no_extra_space(arr1, arr2):
    n, m = len(arr1), len(arr2)
    for i in range(n):
        # Compare current element of arr1 with first element of arr2
        if arr1[i] > arr2[0]:
            arr1[i], arr2[0] = arr2[0], arr1[i]

            # arr2 is now unsorted, place the new element (old arr2[0]) in its correct spot
            first = arr2[0]
            k = 1
            while k < m and arr2[k] < first:
                arr2[k-1] = arr2[k]
                k += 1
            arr2[k-1] = first
```

#### Tricks/Gotchas
- **Complexity Trade-offs:** The O(n*m) approach is easier to understand and implement, but inefficient for large arrays. The Gap Algorithm is much faster but significantly harder to get right.
- **Problem Constraints:** The constraints on `n` and `m` will determine which approach is feasible.

#### Related Problems
- 9. Find the Union of two sorted arrays
- Merge Sort Algorithm
