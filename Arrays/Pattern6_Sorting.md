# Pattern 6: Sorting & Divide and Conquer

This pattern addresses problems that are either simplified immensely by an initial sorting step or are classic examples of the divide-and-conquer paradigm. Sorting-based solutions often have a time complexity of at least O(N log N). Divide and conquer solutions break a problem into smaller, similar subproblems, solve them recursively, and then combine the results. The Merge Sort algorithm is a frequent foundation for these types of problems.

---

### 35. Merge Overlapping Subintervals
`[MEDIUM]` `#sorting` `#intervals`

#### Problem Statement
Given a collection of intervals, merge all overlapping intervals.

*Example:*
- **Input:** `intervals = [[1,3],[2,6],[8,10],[15,18]]`
- **Output:** `[[1,6],[8,10],[15,18]]`
- **Explanation:** Since intervals `[1,3]` and `[2,6]` overlap, they are merged into `[1,6]`.

#### Implementation Overview
This is a classic interval problem solved with a greedy approach after sorting.
1.  **Sort:** The crucial first step is to sort the intervals based on their starting points. This ensures we can process them in a linear fashion.
2.  **Initialize:** Create a `merged` list and initialize it with the first interval from the sorted list.
3.  **Iterate and Merge:** Iterate through the sorted intervals, starting from the second one. For each `current_interval`:
    -   Let `last_merged` be the last interval in our `merged` list.
    -   Check for an overlap: `if current_interval.start <= last_merged.end`.
    -   If they overlap, we merge them by updating the end of `last_merged`. The new end will be the maximum of the two intervals' ends: `last_merged.end = max(last_merged.end, current_interval.end)`.
    -   If they do not overlap, the `current_interval` is a new, distinct interval, so we simply append it to the `merged` list.
4.  The `merged` list is the result.

- **Time Complexity:** `O(N log N)` due to the sorting step. The iteration itself is `O(N)`.
- **Space Complexity:** `O(N)` to store the merged intervals.

#### Python Code Snippet
```python
def merge_intervals(intervals):
    if not intervals:
        return []

    # Sort intervals based on the start time
    intervals.sort(key=lambda x: x[0])

    merged = [intervals[0]]

    for i in range(1, len(intervals)):
        current_interval = intervals[i]
        last_merged = merged[-1]

        # Check for overlap
        if current_interval[0] <= last_merged[1]:
            # Merge
            last_merged[1] = max(last_merged[1], current_interval[1])
        else:
            # No overlap, add new interval
            merged.append(current_interval)

    return merged
```

#### Tricks/Gotchas
- **Sorting is Key:** The entire greedy strategy depends on the intervals being sorted by their start points.
- **In-place Merge:** The code snippet shows an in-place merge where the last element of the result list is modified, which is an efficient approach.

#### Related Problems
- Insert Interval
- Non-overlapping Intervals

---

### 38. Count Inversions
`[HARD]` `#divide-and-conquer` `#merge-sort`

#### Problem Statement
An "inversion" in an array is a pair of indices `(i, j)` such that `i < j` and `arr[i] > arr[j]`. Given an array, count the total number of inversions.

*Example:*
- **Input:** `arr = [8, 4, 2, 1]`
- **Output:** `6`
- **Explanation:** The inversions are `(8,4), (8,2), (8,1), (4,2), (4,1), (2,1)`.

#### Implementation Overview
A brute-force O(N^2) solution is trivial. The optimal O(N log N) solution uses a modified **Merge Sort** algorithm.
1.  The core idea is to count inversions while merging. When we merge two sorted halves, `left` and `right`, some elements in `left` might be greater than elements in `right`, creating "split inversions".
2.  The recursive function `merge_sort_and_count` will do the following:
    -   Base case: If the array has one or zero elements, the inversion count is 0.
    -   Recursively call on the left half to get `left_inversions`.
    -   Recursively call on the right half to get `right_inversions`.
    -   Call a `merge_and_count_split` function that merges the two halves and counts the split inversions.
3.  **Counting Split Inversions:** Inside the `merge` function, while comparing `left[i]` and `right[j]`:
    -   If `left[i] <= right[j]`, there is no inversion with `right[j]`. Place `left[i]` in the merged array and move to the next element in `left`.
    -   If `left[i] > right[j]`, then `right[j]` is smaller than `left[i]` and all subsequent elements in the `left` subarray (because `left` is sorted). The number of such inversions is `len(left) - i`. Add this to the split inversion count, place `right[j]` in the merged array, and move to the next element in `right`.
4.  The total count is `left_inversions + right_inversions + split_inversions`.

- **Time Complexity:** `O(N log N)` because it follows the merge sort algorithm.
- **Space Complexity:** `O(N)` for the temporary merged arrays during the process.

#### Python Code Snippet
```python
def count_inversions(arr):

    def merge_sort(sub_arr):
        if len(sub_arr) <= 1:
            return sub_arr, 0

        mid = len(sub_arr) // 2
        left, inv_left = merge_sort(sub_arr[:mid])
        right, inv_right = merge_sort(sub_arr[mid:])
        merged, inv_split = merge(left, right)

        return merged, inv_left + inv_right + inv_split

    def merge(left, right):
        merged_arr = []
        inversions = 0
        i, j = 0, 0

        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged_arr.append(left[i])
                i += 1
            else:
                merged_arr.append(right[j])
                inversions += (len(left) - i)
                j += 1

        merged_arr.extend(left[i:])
        merged_arr.extend(right[j:])

        return merged_arr, inversions

    _, total_inversions = merge_sort(arr)
    return total_inversions
```

#### Tricks/Gotchas
- **The Core Logic:** The most important part is realizing that when `left[i] > right[j]`, you have found `len(left) - i` inversions at once.
- **Time Complexity:** The algorithm runs in O(N log N) time because it follows the structure of Merge Sort.

#### Related Problems
- 39. Reverse Pairs

---

### 39. Reverse Pairs
`[HARD]` `#divide-and-conquer` `#merge-sort`

#### Problem Statement
A "reverse pair" is a pair of indices `(i, j)` such that `i < j` and `arr[i] > 2 * arr[j]`. Given an array, count the number of reverse pairs.

*Example:*
- **Input:** `nums = [1, 3, 2, 3, 1]`
- **Output:** `2` (The pairs are `(3, 1)` at indices (1, 4) and `(3, 1)` at indices (3, 4))

#### Implementation Overview
This problem is very similar to Count Inversions and is also solved optimally with a modified Merge Sort. The structure is nearly identical, but the counting step is different.
1.  The recursive `merge_sort` structure remains the same.
2.  The modification comes in the `merge` function. Before performing the standard merge-and-sort, we must first count the reverse pairs where one element is in the left half and the other is in the right half.
3.  **Counting Reverse Pairs:**
    -   Use two pointers, `i` for the left half and `j` for the right half.
    -   For each element `left[i]`, iterate `j` through the right half as long as `left[i] > 2 * right[j]`.
    -   The number of elements `j` has advanced gives the number of reverse pairs for that specific `left[i]`. Add this to the total count.
    -   This counting loop is optimized: As `i` increments, `j` does not need to be reset to 0, because `left[i+1] >= left[i]`, so any `j` that formed a pair with `left[i]` will also form one with `left[i+1]`.
4.  **Merge:** After counting is complete, perform a standard merge of the two sorted halves to prepare the array for the next level of recursion.

- **Time Complexity:** `O(N log N)` due to the merge sort structure.
- **Space Complexity:** `O(N)` for the temporary arrays.

#### Python Code Snippet
```python
def reverse_pairs(nums):

    def merge_sort_and_count(arr):
        if len(arr) <= 1:
            return arr, 0

        mid = len(arr) // 2
        left, count_left = merge_sort_and_count(arr[:mid])
        right, count_right = merge_sort_and_count(arr[mid:])

        # Count pairs between halves
        count_split = 0
        j = 0
        for i in range(len(left)):
            while j < len(right) and left[i] > 2 * right[j]:
                j += 1
            count_split += j

        # Merge halves (standard merge logic)
        merged = []
        i, j = 0, 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])

        return merged, count_left + count_right + count_split

    _, total_count = merge_sort_and_count(nums)
    return total_count
```

#### Tricks/Gotchas
- **Count Before Merge:** The counting of reverse pairs must happen *before* the two halves are merged into a single sorted array, as the merge operation changes the element positions.
- **Separate Loops:** It's cleaner and less error-prone to have one loop for counting pairs and a separate, standard loop for merging the arrays.

#### Related Problems
- 38. Count Inversions
