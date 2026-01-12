# Pattern 2: Basic Doubly LL Operations

This pattern covers the foundational concepts and operations of a Doubly Linked List (DLL), highlighting the differences from a Singly Linked List due to the presence of the `previous` pointer.

---

### 1. Introduction to Doubly LinkedList
`[FUNDAMENTAL]` `[EASY]` `#linked-list` `#doubly-linked-list` `#data-structure`

#### Problem Statement
Understand the structure of a Doubly Linked List (DLL). This includes the `Node` structure, which now contains data, a pointer to the *next* node, and a pointer to the *previous* node.

#### Implementation Overview
A Doubly Linked List is a variation of a linked list where each node has a pointer to both its next and previous nodes. This bidirectional linkage provides advantages for certain operations.

- **Node Structure**: A DLL `Node` contains three parts:
    1.  **Data**: The value stored in the node.
    2.  **Next Pointer**: A reference to the next node in the sequence.
    3.  **Previous Pointer**: A reference to the previous node in the sequence. The `prev` pointer of the head is `null`.

- **Head and Tail**: A DLL is tracked with a `HEAD` pointer and often a `TAIL` pointer for O(1) appends.

- **Time Complexity:** Accessing an element is `O(N)`.
- **Space Complexity:** `O(N)` for storing N elements.

#### Python Code Snippet
```python
class Node:
    """A node in a doubly linked list."""
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None
```

---

### 2. Insert a node in DLL
`[FUNDAMENTAL]` `[EASY]` `#doubly-linked-list` `#insertion`

#### Problem Statement
Given a doubly linked list, a value, and a position, insert a new node with the given value.

#### Implementation Overview
1.  **Insertion at Head**: Create a new node. Set its `next` to the current `head`. If the list is not empty, set `head.prev` to `new_node`. Update `head` to `new_node`.
2.  **Insertion Before a Given Node (`next_node`)**:
    -   Set `new_node.next = next_node` and `new_node.prev = next_node.prev`.
    -   Update the `next` pointer of the node *before* `next_node` to point to `new_node`.
    -   Update `next_node.prev` to point to `new_node`.

- **Time Complexity:** `O(1)` for insertion if the reference to the node is given.
- **Space Complexity:** `O(1)`.

#### Python Code Snippet
```python
# Methods within a hypothetical LinkedList class
def insert_at_beginning(self, data):
    new_node = Node(data)
    if self.head is None:
        self.head = new_node
        return
    new_node.next = self.head
    self.head.prev = new_node
    self.head = new_node

def insert_before_node(self, next_node, data):
    if next_node is None: return
    new_node = Node(data)
    new_node.prev = next_node.prev
    new_node.next = next_node
    next_node.prev = new_node
    if new_node.prev is not None:
        new_node.prev.next = new_node
    else: # It's the new head
        self.head = new_node
```

---

### 3. Delete a node in DLL
`[FUNDAMENTAL]` `[EASY]` `#doubly-linked-list` `#deletion`

#### Problem Statement
Given a doubly linked list and a pointer to a node `del_node`, delete that node in O(1) time.

#### Implementation Overview
The key is to "bypass" `del_node` by linking its previous and next nodes directly to each other.
1.  If `del_node.prev` exists, set `del_node.prev.next = del_node.next`.
2.  If `del_node.next` exists, set `del_node.next.prev = del_node.prev`.
3.  Handle edge cases where `del_node` is the head or tail.

- **Time Complexity:** `O(1)` if the reference to the node to be deleted is given.
- **Space Complexity:** `O(1)`.

#### Python Code Snippet
```python
# Method within a hypothetical LinkedList class
def delete_node(self, del_node):
    if self.head is None or del_node is None:
        return

    # If node to be deleted is head node
    if self.head == del_node:
        self.head = del_node.next

    # Change next only if node to be deleted is NOT the last node
    if del_node.next is not None:
        del_node.next.prev = del_node.prev

    # Change prev only if node to be deleted is NOT the first node
    if del_node.prev is not None:
        del_node.prev.next = del_node.next
```

---

### 4. Reverse a DLL
`[EASY]` `#doubly-linked-list` `#reversal` `#two-pointers`

#### Problem Statement
Given a doubly linked list, reverse it in-place.

#### Implementation Overview
Reversing a DLL is simpler than a SLL. We iterate through the list and swap the `next` and `prev` pointers for each node.
1.  Initialize `current = head`.
2.  Traverse the list. In each iteration, swap `current.prev` and `current.next`.
3.  After swapping, the pointer to the *original* next node is now in `current.prev`. So, we advance our loop with `current = current.prev`.
4.  The last node visited becomes the new `head`.

- **Time Complexity:** `O(N)` as we traverse the list once.
- **Space Complexity:** `O(1)`.

#### Python Code Snippet
```python
# Method within a hypothetical LinkedList class
def reverse(self):
    temp = None
    current = self.head

    # Swap next and prev for all nodes
    while current is not None:
        temp = current.prev
        current.prev = current.next
        current.next = temp
        # The original next node is now in current.prev
        current = current.prev

    # After the loop, `temp` is the original head. Its `prev` pointer
    # now points to the new head of the reversed list.
    if temp is not None:
        self.head = temp.prev
```

---

### 5. Delete all occurrences of a key in DLL
`[EASY]` `#doubly-linked-list` `#deletion`

#### Problem Statement
Given a doubly linked list and a key, delete all nodes that have the given key.

#### Implementation Overview
Traverse the list and delete nodes that match the key. Care must be taken because deleting a node changes the links of its neighbors.
1.  Initialize a `current` pointer to the `head`.
2.  Traverse the list. If `current.data` matches the `key`:
    -   Store a reference to the next node: `next_node = current.next`.
    -   Perform the standard DLL deletion logic on `current`.
    -   Move to the next node to check: `current = next_node`.
3.  If `current.data` does not match, simply move to the next node: `current = current.next`.

- **Time Complexity:** `O(N)` to traverse the entire list.
- **Space Complexity:** `O(1)`.

#### Python Code Snippet
```python
# Method within a hypothetical LinkedList class
def delete_all_occurrences(self, key):
    current = self.head
    while current is not None:
        if current.data == key:
            next_node = current.next
            self.delete_node(current) # Use the helper from problem 3
            current = next_node
        else:
            current = current.next
```
