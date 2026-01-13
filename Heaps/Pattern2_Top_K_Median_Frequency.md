# Pattern 2: Top 'K' / Median / Frequency Problems

This pattern focuses on using heaps to solve problems related to finding the "Kth" element, tracking elements based on frequency, or maintaining the median of a dataset. The core idea is that a heap is extremely efficient at keeping track of the smallest or largest elements in a collection without needing to fully sort it.

---

### 1. Kth Largest Element in an Array
`[MEDIUM]` `#top-k` `#min-heap`

#### Problem Statement
Find the Kth largest element in an unsorted array. Note that it is the Kth largest element in the sorted order, not the Kth distinct element.

*Example:* `nums = [3,2,1,5,6,4]`, `k = 2`. **Output:** `5`.

#### Implementation Overview
The most efficient heap-based solution uses a **Min-Heap** of size K.
1.  Iterate through the elements of the array.
2.  For each element, push it onto the min-heap.
3.  If the heap's size exceeds K, pop the smallest element. This ensures the heap always maintains the K largest elements seen so far.
4.  After iterating, the root of the min-heap is the Kth largest element.

#### Time and Space Complexity
- **Time Complexity:** $O(N \log K)$.
- **Space Complexity:** $O(K)$ for the heap.

#### Python Code Snippet
```python
import heapq
def find_kth_largest(nums: list[int], k: int) -> int:
    min_heap = []
    for num in nums:
        heapq.heappush(min_heap, num)
        if len(min_heap) > k:
            heapq.heappop(min_heap)
    return min_heap[0]
```

---

### 2. Kth Smallest Element in an Array
`[MEDIUM]` `#top-k` `#max-heap`

#### Problem Statement
Find the Kth smallest element in an unsorted array.

*Example:* `nums = [3,2,1,5,6,4]`, `k = 2`. **Output:** `2`.

#### Implementation Overview
This is the mirror image of finding the Kth largest. The optimal heap-based solution uses a **Max-Heap** of size K. In Python, this is simulated by pushing negative values onto a min-heap.
1.  Iterate through the elements.
2.  Push the negation of each element onto the min-heap.
3.  If the heap's size exceeds K, pop.
4.  The root of the heap is the negation of the Kth smallest element.

#### Time and Space Complexity
- **Time Complexity:** $O(N \log K)$.
- **Space Complexity:** $O(K)$.

#### Python Code Snippet
```python
import heapq
def find_kth_smallest(nums: list[int], k: int) -> int:
    max_heap = []
    for num in nums:
        heapq.heappush(max_heap, -num)
        if len(max_heap) > k:
            heapq.heappop(max_heap)
    return -max_heap[0]
```

---

### 3. Kth Largest Element in a Stream
`[EASY]` `#top-k` `#stream`

#### Problem Statement
Design a class to find the Kth largest element in a stream of numbers.

#### Implementation Overview
This is a direct application of the "Kth Largest" pattern. The class maintains a **Min-Heap** of size K internally.
-   **Constructor:** Initialize the min-heap with the initial numbers, ensuring the heap size is trimmed to K.
-   **`add(val)` method:** Push the new value `val`. If the heap size is now greater than K, pop. The root is the current Kth largest.

#### Time and Space Complexity
- **Time Complexity:** $O(N \log K)$ for constructor, $O(\log K)$ for `add`.
- **Space Complexity:** $O(K)$.

#### Python Code Snippet
```python
import heapq
class KthLargest:
    def __init__(self, k: int, nums: list[int]):
        self.k = k
        self.min_heap = nums
        heapq.heapify(self.min_heap)
        while len(self.min_heap) > k:
            heapq.heappop(self.min_heap)

    def add(self, val: int) -> int:
        heapq.heappush(self.min_heap, val)
        if len(self.min_heap) > self.k:
            heapq.heappop(self.min_heap)
        return self.min_heap[0]
```

---

### 4. Find Median from Data Stream
`[HARD]` `#two-heaps` `#median` `#stream`

#### Problem Statement
Design a data structure that supports adding numbers from a data stream and finding the median of all elements seen so far.

#### Implementation Overview
The key is to use **two heaps**:
1.  A **Max-Heap (`small_half`)** to store the smaller half of the numbers.
2.  A **Min-Heap (`large_half`)** to store the larger half.
The heaps are balanced such that `len(small_half)` is either equal to or one greater than `len(large_half)`.

**Median Calculation:**
-   If sizes are equal, median is `(top(small) + top(large)) / 2`.
-   If `small_half` is larger, median is `top(small)`.

#### Time and Space Complexity
- **Time Complexity:** $O(\log N)$ for `addNum`, $O(1)$ for `findMedian`.
- **Space Complexity:** $O(N)$ to store elements.

#### Python Code Snippet
```python
import heapq
class MedianFinder:
    def __init__(self):
        self.small_half = []  # Max-heap (stores negative values)
        self.large_half = []  # Min-heap

    def addNum(self, num: int) -> None:
        # Add to max-heap, then move largest to min-heap
        heapq.heappush(self.small_half, -num)
        heapq.heappush(self.large_half, -heapq.heappop(self.small_half))

        # Balance the heaps
        if len(self.large_half) > len(self.small_half):
            heapq.heappush(self.small_half, -heapq.heappop(self.large_half))

    def findMedian(self) -> float:
        if len(self.small_half) > len(self.large_half):
            return -self.small_half[0]
        else:
            return (-self.small_half[0] + self.large_half[0]) / 2.0
```

---

### 5. K Most Frequent Elements
`[MEDIUM]` `#top-k` `#frequency` `#hashmap`

#### Problem Statement
Given an array of integers `nums` and an integer `k`, return the `k` most frequent elements.

*Example:* `nums = [1,1,1,2,2,3]`, `k = 2`. **Output:** `[1,2]`

#### Implementation Overview
1.  **Frequency Counting:** Use a Hash Map to count the frequency of each number (O(N)).
2.  **Finding Top K:** Use a **Min-Heap** of size K to find the K elements with the highest frequencies.
    -   Iterate through the `(element, frequency)` pairs.
    -   Push `(frequency, element)` tuples onto the min-heap.
    -   If heap size exceeds K, pop.
    -   After iterating, the heap contains the K most frequent elements.

#### Time and Space Complexity
- **Time Complexity:** $O(N \log K)$.
- **Space Complexity:** $O(N)$ for the hash map + $O(K)$ for the heap.

#### Python Code Snippet
```python
import heapq
from collections import Counter
def top_k_frequent(nums: list[int], k: int) -> list[int]:
    if k == len(nums):
        return nums

    counts = Counter(nums)
    min_heap = []
    for num, freq in counts.items():
        heapq.heappush(min_heap, (freq, num))
        if len(min_heap) > k:
            heapq.heappop(min_heap)

    return [num for freq, num in min_heap]
```

---

### 6. Maximum Sum Combination
`[HARD]` `#top-k` `#merging`

#### Problem Statement
Given two arrays `A` and `B` of equal size, find the `k` largest sum combinations, where a sum combination is `A[i] + B[j]`.

*Example:* `A = [1, 4, 2, 3]`, `B = [2, 5, 1, 6]`, `k = 4`. **Output:** `[10, 9, 9, 8]`.

#### Implementation Overview
A brute-force O(N^2) approach is too slow. A better way uses a heap.
1.  Sort both arrays `A` and `B` in descending order.
2.  The largest possible sum is `A[0] + B[0]`.
3.  Use a **Max-Heap** to store tuples of `(sum, index_A, index_B)`.
4.  Initialize the heap with `(A[0] + B[0], 0, 0)`.
5.  Use a `visited` set to avoid duplicate `(index_A, index_B)` pairs.
6.  Loop `k` times: Pop the max sum, add it to the result, and push its neighbors `(i+1, j)` and `(i, j+1)` if not visited.

#### Time and Space Complexity
- **Time Complexity:** $O(N \log N)$ for sorting + $O(K \log K)$ for heap operations.
- **Space Complexity:** $O(K)$ for the heap and visited set.

#### Python Code Snippet
```python
import heapq
def k_max_sum_combinations(a: list[int], b: list[int], k: int) -> list[int]:
    a.sort(reverse=True)
    b.sort(reverse=True)
    n = len(a)

    max_heap = [(-(a[0] + b[0]), 0, 0)] # (negative_sum, i, j)
    visited = {(0, 0)}
    result = []

    for _ in range(k):
        if not max_heap: break

        neg_s, i, j = heapq.heappop(max_heap)
        result.append(-neg_s)

        # Add neighbor (i+1, j)
        if i + 1 < n and (i + 1, j) not in visited:
            heapq.heappush(max_heap, (-(a[i+1] + b[j]), i + 1, j))
            visited.add((i + 1, j))

        # Add neighbor (i, j+1)
        if j + 1 < n and (i, j + 1) not in visited:
            heapq.heappush(max_heap, (-(a[i] + b[j+1]), i, j + 1))
            visited.add((i, j + 1))

    return result
```

---

### 7. Replace each array element by its corresponding rank
`[EASY]` `#ranking` `#sorting`

#### Problem Statement
Given an array of integers, replace each element with its rank. Rank is 1-based. Ties have the same rank.

*Example:* `arr = [40,10,20,30,20]`. **Output:** `[4,1,2,3,2]`.

#### Implementation Overview
The most direct solution involves sorting.
1.  Get the unique elements from the array and sort them.
2.  Create a hash map (`rank_map`) to store the rank of each unique element.
3.  Iterate through the sorted unique elements and assign ranks: `rank_map[element] = rank`.
4.  Iterate through the original array and use the map to build the result.

#### Time and Space Complexity
- **Time Complexity:** $O(N \log N)$ for sorting unique elements.
- **Space Complexity:** $O(N)$ for storing unique elements and rank map.

#### Python Code Snippet
```python
def array_rank_transform(arr: list[int]) -> list[int]:
    # Get unique elements and sort them
    sorted_unique_elements = sorted(list(set(arr)))

    # Create a map from value to rank
    rank_map = {val: i + 1 for i, val in enumerate(sorted_unique_elements)}

    # Build the result array
    return [rank_map[val] for val in arr]
```
