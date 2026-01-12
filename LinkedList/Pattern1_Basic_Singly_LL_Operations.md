# Pattern 1: Basic Singly LL Operations

This pattern covers the foundational concepts and operations of a Singly Linked List. Understanding these is crucial before tackling more complex problems.

---

### 1. Introduction to LinkedList
`[FUNDAMENTAL]` `[EASY]` `#linked-list` `#data-structure`

#### Problem Statement
Understand the basic structure of a Singly Linked List. This includes the concept of a `Node`, which contains data and a pointer to the next node, and how these nodes link together to form a list.

#### Implementation Overview
A linked list is a linear data structure where elements are not stored at contiguous memory locations. They are linked using pointers.

- **Node Structure**: The fundamental unit of a linked list is a `Node`. Each node consists of two parts:
    1.  **Data**: The value stored in the node.
    2.  **Next Pointer**: A reference to the next node in the sequence. For the last node, this pointer is `null`.

- **Head Pointer**: The entry point to the linked list is a `HEAD` pointer, which points to the very first node. If the list is empty, `HEAD` is `null`.

This structure allows for dynamic memory allocation and efficient insertion and deletion operations at the beginning of the list.

- **Time Complexity:** Accessing an element is `O(N)`.
- **Space Complexity:** `O(N)` for storing N elements.

#### Python Code Snippet
```python
class Node:
    """A node in a singly linked list."""
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    """A singly linked list."""
    def __init__(self):
        self.head = None
```

---

### 2. Inserting a Node in LinkedList
`[FUNDAMENTAL]` `[EASY]` `#linked-list` `#insertion`

#### Problem Statement
Given a singly linked list, a value, and sometimes a position, insert a new node. Common variations include insertion at the beginning, at the end, or at a specific position `k`.

#### Implementation Overview
1.  **Insertion at Head**: Create a new node, point its `next` to the current `head`, and update `head` to be the new node.
2.  **Insertion at Tail**: Traverse to the last node (where `next` is `None`) and set its `next` pointer to the new node.
3.  **Insertion at Position `k`**: Traverse to the `(k-1)th` node. Let's call it `prev_node`. Set the new node's `next` to `prev_node.next`, and then set `prev_node.next` to the new node.

- **Time Complexity:** Insertion at head is `O(1)`. Insertion at tail or position `k` is `O(N)` due to traversal.
- **Space Complexity:** `O(1)`.

#### Python Code Snippet
```python
# Methods within the LinkedList class
def insert_at_beginning(self, data):
    new_node = Node(data)
    new_node.next = self.head
    self.head = new_node

def insert_at_end(self, data):
    new_node = Node(data)
    if not self.head:
        self.head = new_node
        return
    last = self.head
    while last.next:
        last = last.next
    last.next = new_node

def insert_at_position(self, data, position):
    if position < 1: return
    if position == 1:
        self.insert_at_beginning(data)
        return

    new_node = Node(data)
    temp = self.head
    # Traverse to the node just before the target position
    for _ in range(position - 2):
        if temp is None: return # Position out of bounds
        temp = temp.next

    if temp is None: return # Position out of bounds
    new_node.next = temp.next
    temp.next = new_node
```

---

### 3. Deleting a Node in LinkedList
`[FUNDAMENTAL]` `[EASY]` `#linked-list` `#deletion`

#### Problem Statement
Given a singly linked list and a key (value or position), delete the first occurrence of the node with that key.

#### Implementation Overview
1.  **Deletion of Head**: If the head node is the one to be deleted, update `head` to `head.next`.
2.  **Deletion by Value/Position**: Use two pointers, `prev` and `curr`, to traverse the list. When `curr` is the node to be deleted, "bypass" it by setting `prev.next = curr.next`.

- **Time Complexity:** `O(1)` for deleting head. `O(N)` for deleting by value or position.
- **Space Complexity:** `O(1)`.

#### Python Code Snippet
```python
# Method within the LinkedList class
def delete_node_by_value(self, key):
    temp = self.head
    # If head node itself holds the key
    if temp is not None and temp.data == key:
        self.head = temp.next
        return

    prev = None
    while temp is not None and temp.data != key:
        prev = temp
        temp = temp.next

    if temp is None: return # Key not found
    prev.next = temp.next # Unlink the node
```

---

### 4. Find the length of the linkedlist
`[FUNDAMENTAL]` `[EASY]` `#linked-list` `#traversal`

#### Problem Statement
Given the `head` of a singly linked list, find and return its length (the number of nodes).

#### Implementation Overview
1.  Initialize a `length` counter to 0.
2.  Initialize a `current` pointer to the `head`.
3.  Traverse the list, incrementing `length` for each node, until `current` is `None`.

- **Time Complexity:** `O(N)`.
- **Space Complexity:** `O(1)`.

#### Python Code Snippet
```python
# Method within the LinkedList class
def get_length(self):
    length = 0
    current = self.head
    while current:
        length += 1
        current = current.next
    return length
```

---

### 5. Search an element in the LL
`[FUNDAMENTAL]` `[EASY]` `#linked-list` `#traversal` `#search`

#### Problem Statement
Given the `head` of a singly linked list and a target value, determine if a node with that value exists in the list.

#### Implementation Overview
1.  Initialize a `current` pointer to the `head`.
2.  Traverse the list. At each node, compare its `data` with the target.
3.  If a match is found, return `True`.
4.  If the end of the list is reached, return `False`.

- **Time Complexity:** `O(N)`.
- **Space Complexity:** `O(1)`.

#### Python Code Snippet
```python
# Method within the LinkedList class
def search(self, target):
    current = self.head
    while current:
        if current.data == target:
            return True
        current = current.next
    return False
```
