### `[PATTERN] Advanced and Complex Problems`

This section covers advanced and complex linked list problems that often require combining multiple patterns, using auxiliary data structures like hash maps or heaps, or involve intricate pointer manipulation. These problems are common in technical interviews for senior roles as they test a deep understanding of data structures and algorithms.

---

### 1. Copy List with Random Pointer
`[MEDIUM]` `#hash-map` `#cloning` `#linked-list`

#### Problem Statement
A linked list of length `n` is given such that each node contains an additional `random` pointer, which could point to any node in the list, or `null`. Construct a **deep copy** of the list. The deep copy should consist of exactly `n` brand new nodes, where each new node has its value set to the value of its corresponding original node. Both the `next` and `random` pointers of the new nodes should point to new nodes in the copied list.

---

#### a) O(N) Space Approach using a Hash Map

This is the most intuitive approach. We use a hash map to store the mapping from an original node to its corresponding new node.

##### Implementation Overview
1.  **Initialize Hash Map**: Create a hash map `mapping = {None: None}`. The `None` entry handles cases where `random` pointers are null.
2.  **First Pass (Create Nodes)**: Iterate through the original list. For each node, create a new node with the same value and store the `(original_node, new_node)` pair in the hash map.
3.  **Second Pass (Assign Pointers)**: Iterate through the original list again. For each `original_node`:
    a. Get its corresponding `new_node` from the hash map.
    b. Assign the pointers:
       - `new_node.next = mapping[original_node.next]`
       - `new_node.random = mapping[original_node.random]`
4.  Return the head of the new list, which is `mapping[head]`.

##### Python Code Snippet
```python
class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random

def copy_random_list_with_map(head: 'Node') -> 'Node':
    if not head:
        return None

    mapping = {None: None}

    # 1. First pass: create all nodes and map old to new
    curr = head
    while curr:
        mapping[curr] = Node(curr.val)
        curr = curr.next

    # 2. Second pass: assign next and random pointers
    curr = head
    while curr:
        new_node = mapping[curr]
        new_node.next = mapping[curr.next]
        new_node.random = mapping[curr.random]
        curr = curr.next

    return mapping[head]
```

---

#### b) O(1) Space Approach (Interweaving)

This clever approach avoids using extra space for a hash map by modifying the original list structure temporarily.

##### Implementation Overview
1.  **First Pass (Interweave Nodes)**:
    -   Iterate through the original list.
    -   For each `original_node`, create its `copy_node`.
    -   Insert the `copy_node` immediately after the `original_node`.
    -   `original_node.next` should point to `copy_node`, and `copy_node.next` should point to the original `original_node.next`.
    -   After this pass, the list will be `A -> A' -> B -> B' -> C -> C' -> ...`

2.  **Second Pass (Assign Random Pointers)**:
    -   Iterate through the interweaved list (starting from the original head).
    -   For each `original_node` (`curr`), its copy is `curr.next`.
    -   The random pointer of the copy can be found via the original's random pointer: `curr.next.random = curr.random.next`.
    -   A check is needed: `if curr.random: curr.next.random = curr.random.next`.

3.  **Third Pass (Separate Lists)**:
    -   Iterate through the list again to restore the original list and extract the copied list.
    -   Use two pointers, `original_ptr` and `copy_ptr`, to manage the heads of the two lists being separated.
    -   Carefully rewire the `next` pointers to disentangle the lists.

##### Python Code Snippet
```python
def copy_random_list_optimized(head: 'Node') -> 'Node':
    if not head:
        return None

    # 1. Interweave new nodes
    curr = head
    while curr:
        new_node = Node(curr.val, curr.next)
        curr.next = new_node
        curr = new_node.next

    # 2. Assign random pointers
    curr = head
    while curr:
        if curr.random:
            curr.next.random = curr.random.next
        curr = curr.next.next # Move to the next original node

    # 3. Separate the lists
    original_head = head
    copy_head = head.next

    original_ptr = original_head
    copy_ptr = copy_head

    while original_ptr:
        original_ptr.next = original_ptr.next.next
        copy_ptr.next = copy_ptr.next.next if copy_ptr.next else None

        original_ptr = original_ptr.next
        copy_ptr = copy_ptr.next

    return copy_head
```

---

### 2. LRU Cache
`[MEDIUM]` `#design` `#hash-map` `#doubly-linked-list`

#### Problem Statement
Design a data structure that follows the constraints of a **Least Recently Used (LRU) Cache**. Implement the `LRUCache` class:
- `LRUCache(int capacity)`: Initializes the LRU cache with positive size `capacity`.
- `int get(int key)`: Returns the value of the `key` if it exists, otherwise returns -1.
- `void put(int key, int value)`: Updates the value of the `key` if it exists. Otherwise, adds the key-value pair to the cache. If the number of keys exceeds the capacity, **evict the least recently used key** before inserting the new item.

#### Implementation Overview
The key to an efficient LRU cache is performing both `get` and `put` operations in O(1) time. This is achieved by combining two data structures:
- **A Hash Map (Dictionary)**: Stores `(key, node)` pairs. This allows for O(1) lookup of any key to find its corresponding node in the linked list.
- **A Doubly Linked List**: Stores the nodes in order of use. The most recently used item is at one end (e.g., the head), and the least recently used item is at the other end (e.g., the tail). A doubly linked list is used because it allows for O(1) insertion and deletion of nodes from any position, given a reference to the node.

We use a `head` and `tail` dummy node to make list manipulation easier.
- **`get(key)`**:
  1. Check if `key` is in the hash map. If not, return -1.
  2. If it exists, retrieve the `node` from the map.
  3. This node is now the most recently used, so move it to the front of the linked list.
  4. Return the `node.value`.
- **`put(key, value)`**:
  1. Check if `key` is already in the hash map.
     - If yes, update its `value` and move the corresponding `node` to the front of the list.
     - If no:
       a. Check if the cache is at full capacity. If so, evict the least recently used item (the node at the tail of the list) and remove it from the hash map.
       b. Create a new `node` with the `key` and `value`.
       c. Add the new `node` to the front of the list.
       d. Add the `(key, new_node)` pair to the hash map.

#### Python Code Snippet
```python
class DLinkedNode:
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {} # Hash map: key -> node
        self.head = DLinkedNode() # Dummy head
        self.tail = DLinkedNode() # Dummy tail
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove_node(self, node):
        # Helper to remove a node from the list
        prev, nxt = node.prev, node.next
        prev.next = nxt
        nxt.prev = prev

    def _add_to_front(self, node):
        # Helper to add a node to the front (right after dummy head)
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1

        node = self.cache[key]
        self._remove_node(node)
        self._add_to_front(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            # Update existing key
            node = self.cache[key]
            node.value = value
            self._remove_node(node)
            self._add_to_front(node)
        else:
            # Add new key
            if len(self.cache) == self.capacity:
                # Evict the least recently used item (at the tail)
                lru = self.tail.prev
                self._remove_node(lru)
                del self.cache[lru.key]

            new_node = DLinkedNode(key, value)
            self.cache[key] = new_node
            self._add_to_front(new_node)
```

---

### 3. Flatten a Multilevel Doubly Linked List
`[MEDIUM]` `#doubly-linked-list` `#dfs` `#rearrangement`

#### Problem Statement
You are given a doubly linked list, which, in addition to the `next` and `prev` pointers, could have a `child` pointer, which may or may not point to a separate doubly linked list. These child lists may have one or more children of their own, and so on. Return the list as a single-level flattened list.

#### Implementation Overview (Iterative)
The goal is to traverse the list and, whenever we encounter a `child` list, splice it in immediately after the current node. An iterative approach using a stack (or just rewiring in place) is common.

1.  Initialize a `current` pointer to the `head`.
2.  Iterate while `current` is not `None`.
3.  If `current.child` is `None`, there's nothing to do, so just move to the next node: `current = current.next`.
4.  If `current.child` exists:
    a. We need to find the `tail` of the child list. Traverse the child list until `tail.next` is `None`.
    b. Store the original `next` of the current node: `original_next = current.next`.
    c. Splice the child list in:
       - `current.next = current.child`
       - `current.child.prev = current`
       - `current.child = None` (clear the child pointer)
    d. Connect the `tail` of the child list to the `original_next`:
       - `tail.next = original_next`
       - If `original_next` is not `None`, `original_next.prev = tail`.
5.  Continue the traversal from `current`.

#### Python Code Snippet
```python
class Node:
    # Definition for a Node.
    def __init__(self, val, prev, next, child):
        self.val = val
        self.prev = prev
        self.next = next
        self.child = child

def flatten(head: 'Node') -> 'Node':
    if not head:
        return None

    curr = head
    while curr:
        if not curr.child:
            curr = curr.next
            continue

        # Child exists, find its tail
        child_tail = curr.child
        while child_tail.next:
            child_tail = child_tail.next

        # Store original next
        original_next = curr.next

        # Splice in the child list
        curr.next = curr.child
        curr.child.prev = curr
        curr.child = None # Clear child pointer

        # Connect child tail to original next
        child_tail.next = original_next
        if original_next:
            original_next.prev = child_tail

        # Continue from the current node
        curr = curr.next

    return head
```

---

### 4. Merge K Sorted Lists
`[HARD]` `#heap` `#priority-queue` `#merging`

#### Problem Statement
You are given an array of `k` linked lists `lists`, where each linked list is sorted in ascending order. Merge all the linked lists into one sorted linked list and return it.

#### Implementation Overview
While you could merge lists one by one, this would be inefficient (O(N*k) where N is the total number of nodes). A much better approach uses a **Min-Heap** (Priority Queue) to efficiently find the smallest node among all the lists at any given time.

1.  **Initialize a Min-Heap**: The heap will store tuples of `(node.val, list_index, node)` to keep track of the smallest current element from each list. The `list_index` is needed to break ties in the heap if values are equal.
2.  **Populate the Heap**: Iterate through the `k` lists. If a list is not empty, push its head node (along with its value and index) onto the min-heap.
3.  **Initialize Result List**: Create a dummy `head` and a `tail` pointer for the merged list.
4.  **Process the Heap**:
    -   While the heap is not empty:
      a. Pop the smallest element: `(val, index, node) = heapq.heappop()`.
      b. Append this `node` to the `tail` of the result list and advance the `tail`.
      c. If the popped `node` has a `next` node in its original list, push that `next` node onto the heap.
5.  Return `dummy_head.next`.

This approach is efficient because heap operations (push and pop) take O(log k) time, and we do this for every node. The total time complexity is O(N log k).

#### Python Code Snippet
```python
import heapq

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    # Add a __lt__ method for heapq compatibility in Python 3
    # when values are equal.
    def __lt__(self, other):
        return self.val < other.val

def merge_k_lists(lists: list[ListNode]) -> ListNode:
    min_heap = []
    for i, l in enumerate(lists):
        if l:
            # Python's heapq can't compare nodes, so we use a tuple.
            # (value, node_object) is enough if values are unique.
            # Adding an index i makes the tuple unique if values are not.
            heapq.heappush(min_heap, (l.val, i, l))

    dummy_head = ListNode()
    tail = dummy_head

    while min_heap:
        val, i, node = heapq.heappop(min_heap)

        tail.next = node
        tail = tail.next

        if node.next:
            next_node = node.next
            heapq.heappush(min_heap, (next_node.val, i, next_node))

    return dummy_head.next

---

### 5. Sort List
`[MEDIUM]` `#divide-and-conquer` `#merge-sort` `#linked-list`

#### Problem Statement
Given the `head` of a linked list, return the list after sorting it in ascending order.

#### Implementation Overview
The most suitable sorting algorithm for linked lists is **Merge Sort**, due to its efficiency (O(N log N)) and the fact that it doesn't rely on random access. The process is a classic divide-and-conquer strategy.

1.  **Base Case**: If the list has 0 or 1 nodes, it is already sorted. Return `head`.
2.  **Divide**:
    -   Split the linked list into two halves. Find the middle of the list using the slow/fast pointer technique.
    -   Sever the link between the two halves to create two independent lists.
3.  **Conquer**:
    -   Recursively call `sortList()` on both the left half and the right half.
4.  **Merge**:
    -   Merge the two now-sorted halves into a single sorted list. This is done with a helper function that iteratively picks the smaller element from the two half-lists.

#### Python Code Snippet
```python
def sort_list(head: ListNode) -> ListNode:
    if not head or not head.next:
        return head

    # Find middle of the list
    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    # Split the list into two halves
    mid = slow.next
    slow.next = None

    # Recursively sort both halves
    left = sort_list(head)
    right = sort_list(mid)

    # Merge the sorted halves
    dummy = tail = ListNode()
    while left and right:
        if left.val < right.val:
            tail.next = left
            left = left.next
        else:
            tail.next = right
            right = right.next
        tail = tail.next

    tail.next = left or right
    return dummy.next
```
```

---

### 6. Flattening of LL
`[HARD]` `#linkedlist` `#merging`

#### Problem Statement
Given a Linked List where every node represents a sub-linked-list and contains two pointers:
1. `next`: Points to the next node in the main list.
2. `bottom`: Points to a sub-linked-list where all nodes are sorted.

Your task is to flatten the entire list into a single linked list sorted by bottom/child pointers, where all nodes are linked only via bottom/child pointers.

*Example:*
- **Input:**
  ```
  5 -> 10 -> 19 -> 28
  |    |     |     |
  7    20    22    35
  |          |     |
  8          50    40
  |                |
  30               45
  ```
- **Output:** `5 -> 7 -> 8 -> 10 -> 19 -> 20 -> 22 -> 28 -> 30 -> 35 -> 40 -> 45 -> 50`

#### Implementation Overview
We use a divide-and-conquer approach:
1. Recursively traverse to the end of the `next` pointer list.
2. Once at the end, merge the current list with the recursively flattened list on the right.
3. The merge operation is identical to merging two sorted linked lists using child/bottom pointers.

#### Python Code Snippet
```python
class Node:
    def __init__(self, data=0, next=None, bottom=None):
        self.data = data
        self.next = next
        self.bottom = bottom
        
def merge(a, b):
    if not a:
        return b
    if not b:
        return a
    if a.data < b.data:
        result = a
        result.bottom = merge(a.bottom, b)
    else:
        result = b
        result.bottom = merge(a, b.bottom)
    result.next = None
    return result
    
def flatten(root):
    if not root or not root.next:
        return root
    # Flatten the next list
    root.next = flatten(root.next)
    # Merge current list with flattened next list
    root = merge(root, root.next)
    return root
```
