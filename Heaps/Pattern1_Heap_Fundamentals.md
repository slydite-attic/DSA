# Pattern 1: Heap Fundamentals

This pattern covers the essential concepts and implementations of heaps (specifically binary heaps), which are the most common underlying structure for Priority Queues. Understanding these fundamentals is crucial before tackling more complex heap-based problems.

---

### 1. Introduction to Priority Queues using Binary Heaps
`[FUNDAMENTAL]` `[EASY]` `#concept` `#data-structure`

#### Concept Overview
A **Priority Queue** is an abstract data type that operates like a regular queue but with an added "priority" for each element. When you dequeue an element, the one with the highest priority is removed first.

While several data structures can implement a priority queue, the most efficient and common choice is a **Binary Heap**. A Binary Heap is a complete binary tree that satisfies the heap property:
1.  **Min-Heap Property:** The value of each parent node is less than or equal to the value of its children. The root always holds the minimum value.
2.  **Max-Heap Property:** The value of each parent node is greater than or equal to the value of its children. The root always holds the maximum value.

Heaps provide an excellent balance of performance for the main priority queue operations:
-   **Insertion (Enqueue):** O(log n)
-   **Deletion (Dequeue):** O(log n)
-   **Peek (Get Max/Min):** O(1)

Heaps are typically represented using an array. For a node at index `i`:
-   Its left child is at `2*i + 1`.
-   Its right child is at `2*i + 2`.
-   Its parent is at `floor((i-1)/2)`.

---

### 2. Min Heap and Max Heap Implementation
`[FUNDAMENTAL]` `[EASY]` `#implementation` `#min-heap` `#max-heap`

#### Problem Statement
Implement both a Min-Heap and a Max-Heap data structure that support insertion and extraction of the root element.

#### Implementation Overview
In Python, the `heapq` module provides a direct implementation of a Min-Heap.
-   **Min-Heap:** Use `heapq.heappush` to insert and `heapq.heappop` to extract the minimum element.
-   **Max-Heap:** The standard trick is to **insert the negation** of the values. When you extract a value, you negate it again to get the original maximum value.

#### Python Code Snippet
```python
import heapq

# --- Min-Heap Example ---
min_heap = []
heapq.heappush(min_heap, 3)  # Heap is [3]
heapq.heappush(min_heap, 1)  # Heap is [1, 3]
heapq.heappush(min_heap, 4)  # Heap is [1, 3, 4]
print(f"Min-heap: {min_heap}")

# To peek at the smallest element:
print(f"Smallest element: {min_heap[0]}") # -> 1

# To extract the smallest element:
smallest = heapq.heappop(min_heap) # smallest is 1
print(f"Popped: {smallest}, Heap is now: {min_heap}") # -> [3, 4]

# --- Max-Heap Example (using negation) ---
max_heap = []
heapq.heappush(max_heap, -3) # Store -3 for 3. Heap: [-3]
heapq.heappush(max_heap, -1) # Store -1 for 1. Heap: [-3, -1]
heapq.heappush(max_heap, -4) # Store -4 for 4. Heap: [-4, -1, -3]
print(f"Max-heap (internal): {max_heap}")

# To peek at the largest element:
print(f"Largest element: {-max_heap[0]}") # -> 4

# To extract the largest element:
largest = -heapq.heappop(max_heap) # largest is 4
print(f"Popped: {largest}, Heap is now: {max_heap}") # -> [-3, -1] (represents [3, 1])
```

---

### 3. Check if an array represents a min-heap
`[EASY]` `#heap-property` `#validation`

#### Problem Statement
Given an array, determine if it represents a valid Min-Heap.

*Example:* `arr = [1, 2, 3, 4, 5]`. **Output:** `True`.
*Example:* `arr = [1, 3, 2, 4, 5]`. **Output:** `False` (3 > 2).

#### Implementation Overview
The core idea is to iterate through all **non-leaf nodes** and check if they satisfy the Min-Heap property. A node at index `i` is non-leaf if `2*i + 1 < n`.

For each parent node at index `i`:
1.  Calculate indices of its left (`2*i + 1`) and right (`2*i + 2`) children.
2.  If the left child exists and its value is smaller than the parent's, it's not a min-heap.
3.  If the right child exists and its value is smaller than the parent's, it's not a min-heap.
4.  If all parent nodes satisfy the property, the array is a valid min-heap.

#### Python Code Snippet
```python
def is_min_heap(arr: list[int]) -> bool:
    n = len(arr)
    # Iterate through all non-leaf nodes
    for i in range(n // 2):
        left_child_idx = 2 * i + 1
        right_child_idx = 2 * i + 2

        # Check left child
        if left_child_idx < n and arr[i] > arr[left_child_idx]:
            return False

        # Check right child
        if right_child_idx < n and arr[i] > arr[right_child_idx]:
            return False

    return True
```

---

### 4. Convert Min-Heap to Max-Heap
`[MEDIUM]` `#heapify` `#conversion`

#### Problem Statement
Given an array representing a Min-Heap, convert it in-place to a Max-Heap.

*Example:* `min_heap = [3, 5, 9, 6, 8, 20, 10, 12, 18, 9]`. The task is to reorder it into a valid max-heap.

#### Implementation Overview
A Min-Heap does not satisfy the Max-Heap property. Converting it requires rebuilding the heap structure. The standard O(n) algorithm to build a heap from an arbitrary array is to run a `heapify` process on all non-leaf nodes in reverse order.
1.  Identify the last non-leaf node. Its index is `(n // 2) - 1`.
2.  Iterate from this node backwards up to the root (index 0).
3.  In each iteration, call a `max_heapify_down` function on the current node. This function ensures the subtree rooted at the given node is a max-heap by "sifting down" the node to its correct position.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, because building a heap from an unordered array takes linear time.
- **Space Complexity:** $O(1)$ (iterative heapify) or $O(\log N)$ (recursive heapify due to stack).

#### Python Code Snippet
```python
def max_heapify_down(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    # See if left child exists and is greater than root
    if left < n and arr[i] < arr[left]:
        largest = left

    # See if right child exists and is greater than the largest so far
    if right < n and arr[largest] < arr[right]:
        largest = right

    # Change root, if needed
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        # Heapify the root of the affected sub-tree
        max_heapify_down(arr, n, largest)

def convert_min_to_max_heap(arr: list[int]):
    n = len(arr)
    # Start from the last non-leaf node and heapify each node
    for i in range((n // 2) - 1, -1, -1):
        max_heapify_down(arr, n, i)
    # The array is now a max-heap
    return arr
```
