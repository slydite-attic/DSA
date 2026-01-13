# Pattern 6: Advanced Data Structure Design

This pattern covers problems that require designing custom data structures, often by combining stacks, queues, linked lists, and hash maps. These problems test a deeper understanding of data structure trade-offs and are common in interviews for senior roles.

---

### 1. Implement Min Stack
`[EASY]` `#stack` `#design`

#### Problem Statement
Design a stack that supports `push`, `pop`, `top`, and `getMin` in constant time O(1). `getMin` should retrieve the minimum element currently in the stack.

*Example:*
```
minStack = MinStack()
minStack.push(-2)
minStack.push(0)
minStack.push(-3)
minStack.getMin() // return -3
minStack.pop()
minStack.top()    // return 0
minStack.getMin() // return -2
```

#### Implementation Overview
The challenge is retrieving the minimum element in O(1) time. The solution is to augment the stack to keep track of the minimum at every level.

**Method 1: Storing (value, current_min) pairs**
- Use a single stack that stores pairs: `(value, min_at_this_level)`.
- When pushing `x`, the new minimum is `min(x, current_min)`. Push the pair `(x, new_min)` onto the stack.
- This approach is clean and ensures that for any state of the stack, the minimum is available at the top.

**Method 2: Using a second stack**
- Use a main stack for values and a second "min stack".
- When pushing `x` to the main stack, if `x` is less than or equal to the top of the min stack (or if the min stack is empty), push `x` onto the min stack as well.
- When popping from the main stack, if the popped value is equal to the top of the min stack, pop from the min stack too.

#### Time and Space Complexity
- **Time Complexity:** $O(1)$ for all operations.
- **Space Complexity:** $O(N)$ for the stack.

#### Python Code Snippet (Method 1)
```python
class MinStack:
    def __init__(self):
        # Stack stores pairs of (value, current_minimum)
        self.stack = []

    def push(self, val: int) -> None:
        if not self.stack:
            # If stack is empty, the min is the value itself
            self.stack.append((val, val))
        else:
            # The new min is the smaller of the new value and the previous min
            current_min = self.stack[-1][1]
            new_min = min(val, current_min)
            self.stack.append((val, new_min))

    def pop(self) -> None:
        if self.stack:
            self.stack.pop()

    def top(self) -> int:
        if self.stack:
            return self.stack[-1][0] # Return the value
        return -1

    def getMin(self) -> int:
        if self.stack:
            return self.stack[-1][1] # Return the min
        return -1
```

---

### 2. The Celebrity Problem
`[MEDIUM]` `#stack` `#graph` `#two-pointers`

#### Problem Statement
In a party of `N` people, a celebrity is someone who is known by everyone but knows no one. You are given a function `knows(a, b)` which returns `true` if `a` knows `b`. Find the potential celebrity. If no celebrity exists, return -1.

#### Implementation Overview
This can be solved in O(N) time. The key insight is that if `knows(A, B)` is true, `A` cannot be a celebrity. If it's false, `B` cannot be a celebrity. We can use this to eliminate one person at each step.

**Method: Using a Stack (or just two pointers)**
1.  Push all people (indices `0` to `N-1`) onto a stack.
2.  While the stack has more than one person:
    - Pop two people, `A` and `B`.
    - If `knows(A, B)`, then `A` cannot be a celebrity. Push `B` back onto the stack as `B` is still a potential candidate.
    - If `!knows(A, B)`, then `B` cannot be a celebrity (since `A` doesn't know them). Push `A` back.
3.  The single person remaining in the stack is the *only potential candidate*.
4.  **Verify the candidate**: This candidate might not be a celebrity. We must iterate through all other people and confirm that:
    - The candidate knows no one.
    - Everyone knows the candidate.
    - If both conditions hold, return the candidate's index. Otherwise, return -1.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$ for finding the candidate and $O(N)$ for verification. Total $O(N)$.
- **Space Complexity:** $O(1)$ if using two pointers, $O(N)$ if using a stack.

#### Python Code Snippet
```python
# The knows API is already defined for you.
# def knows(a: int, b: int) -> bool:

class Solution:
    def findCelebrity(self, n: int) -> int:
        # Step 1 & 2: Find the single potential candidate
        candidate = 0
        for i in range(1, n):
            if knows(candidate, i):
                candidate = i # candidate cannot be a celebrity, i might be

        # Step 3: Verify the candidate
        for i in range(n):
            if i == candidate:
                continue
            # If candidate knows someone OR someone doesn't know the candidate
            if knows(candidate, i) or not knows(i, candidate):
                return -1

        return candidate
```

---

### 3. LRU Cache (Least Recently Used)
`[MEDIUM]` `#design` `#hash-map` `#doubly-linked-list`

#### Problem Statement
Design a data structure for an LRU cache. It should support `get(key)` and `put(key, value)` operations in O(1) time. When the cache is full, a `put` operation should evict the least recently used item.

#### Implementation Overview
This is a classic design problem that requires O(1) time complexity for both `get` and `put`. The optimal solution combines a hash map and a doubly linked list.
1.  **Hash Map (`dict` in Python)**: Stores `key -> Node` pairs. This provides O(1) access to any node in the list.
2.  **Doubly Linked List**: Stores the nodes themselves. The list is ordered by recency. The most recently used item is at the head, and the least recently used item is at the tail.

**Operations:**
- **`get(key)`**: Look up the node in the hash map. If found, move this node to the head of the linked list (to mark it as most recently used) and return its value.
- **`put(key, value)`**: If the key exists, update its value and move the node to the head. If it's a new key, create a new node. If the cache is full, remove the node at the tail of the list and also remove it from the hash map. Finally, add the new node to the head of the list and to the hash map.

#### Time and Space Complexity
- **Time Complexity:** $O(1)$ for both `get` and `put`.
- **Space Complexity:** $O(C)$ where $C$ is the capacity.

#### Python Code Snippet
```python
class Node:
    def __init__(self, key, val):
        self.key, self.val = key, val
        self.prev = self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.cache = {} # map key to node
        # Use dummy head and tail for cleaner code
        self.head, self.tail = Node(0, 0), Node(0, 0)
        self.head.next, self.tail.prev = self.tail, self.head

    # Removes a node from the list
    def _remove(self, node):
        prev, nxt = node.prev, node.next
        prev.next, nxt.prev = nxt, prev

    # Adds a node to the front of the list (head)
    def _add_to_head(self, node):
        node.prev, node.next = self.head, self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add_to_head(node)
            return node.val
        return -1

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self._remove(self.cache[key])

        node = Node(key, value)
        self.cache[key] = node
        self._add_to_head(node)

        if len(self.cache) > self.cap:
            # Remove from the tail of the list
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]
```

---

### 4. LFU Cache (Least Frequently Used)
`[HARD]` `#design` `#hash-map` `#doubly-linked-list`

#### Problem Statement
Design a data structure for an LFU cache. It supports `get` and `put`. When the cache is full, it evicts the least frequently used item. If there's a tie in frequency, the least *recently* used item among them is evicted.

#### Implementation Overview
This is significantly more complex than LRU. An optimal solution uses two hash maps and a doubly linked list structure.
1.  **A `key_to_node` hash map**: Maps a key to its node `(key, value, freq)`.
2.  **A `freq_to_dll` hash map**: Maps a frequency count to a Doubly Linked List (which acts as an LRU list for that specific frequency). All nodes in a given list have the same frequency.
3.  A variable `min_freq` to track the current lowest frequency, for O(1) eviction.

**Operations:**
- When a node is accessed (via `get` or `put`):
  - Its frequency increases by 1.
  - It must be moved from the DLL at `freq` to the head of the DLL at `freq + 1`.
  - Update `min_freq` if the list at the old `min_freq` becomes empty.
- **Eviction**: When the cache is full, use `min_freq` to find the correct DLL. Remove the node at the tail of that list (as it's the LRU for that frequency).

#### Time and Space Complexity
- **Time Complexity:** $O(1)$ for both `get` and `put`.
- **Space Complexity:** $O(C)$ where $C$ is the capacity.

#### Python Code Snippet
```python
class Node:
    def __init__(self, key, val):
        self.key, self.val = key, val
        self.freq = 1
        self.prev = self.next = None

class DLinkedList:
    def __init__(self):
        self.head, self.tail = Node(0, 0), Node(0, 0)
        self.head.next, self.tail.prev = self.tail, self.head
        self.size = 0

    def add_to_head(self, node):
        node.prev, node.next = self.head, self.head.next
        self.head.next.prev = node
        self.head.next = node
        self.size += 1

    def remove(self, node):
        prev, nxt = node.prev, node.next
        prev.next, nxt.prev = nxt, prev
        self.size -= 1

    def remove_tail(self):
        if self.size > 0:
            tail_node = self.tail.prev
            self.remove(tail_node)
            return tail_node
        return None

class LFUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.key_to_node = {}
        self.freq_to_dll = {}
        self.min_freq = 0

    def _update_node_freq(self, node):
        # Remove node from its old frequency list
        old_dll = self.freq_to_dll[node.freq]
        old_dll.remove(node)

        # If the old list was the min_freq list and is now empty, update min_freq
        if self.min_freq == node.freq and old_dll.size == 0:
            self.min_freq += 1

        # Increment frequency and add to new list
        node.freq += 1
        new_dll = self.freq_to_dll.get(node.freq, DLinkedList())
        new_dll.add_to_head(node)
        self.freq_to_dll[node.freq] = new_dll

    def get(self, key: int) -> int:
        if key not in self.key_to_node:
            return -1
        node = self.key_to_node[key]
        self._update_node_freq(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if self.cap == 0: return

        if key in self.key_to_node:
            node = self.key_to_node[key]
            node.val = value
            self._update_node_freq(node)
        else:
            if len(self.key_to_node) == self.cap:
                # Evict
                min_freq_dll = self.freq_to_dll[self.min_freq]
                lfu_node = min_freq_dll.remove_tail()
                del self.key_to_node[lfu_node.key]

            # Add new node
            new_node = Node(key, value)
            self.key_to_node[key] = new_node
            self.min_freq = 1
            dll = self.freq_to_dll.get(1, DLinkedList())
            dll.add_to_head(new_node)
            self.freq_to_dll[1] = dll
```
