# Pattern 1: Basic Data Structure Implementation

This pattern covers the foundational implementation of stacks and queues using basic data structures like arrays and linked lists. Understanding these is crucial before tackling more complex problems. A key distinction is their access pattern:
- **Stack**: LIFO (Last-In, First-Out). Like a stack of plates.
- **Queue**: FIFO (First-In, First-Out). Like a checkout line.

---

### 1. Implement Stack using Arrays
`[EASY]` `[FUNDAMENTAL]` `#implementation` `#array`

#### Problem Statement
Implement a Stack class using an array. It should support the following operations in amortized O(1) time:
- `push(x)`: Pushes element x onto the stack.
- `pop()`: Removes the element on the top of the stack and returns it.
- `top()`: Gets the top element of the stack without removing it.
- `size()`: Returns the number of elements in the stack.
- `isEmpty()`: Returns true if the stack is empty.

*Example Usage:*
```
myStack = Stack()
myStack.push(1)
myStack.push(2)
myStack.top()    // returns 2
myStack.pop()    // returns 2
myStack.isEmpty()// returns false
```

#### Implementation Overview
We use a dynamic array (a `list` in Python) to store the stack elements. The "top" of the stack is the end of the list.
- **Push**: Append the element to the end of the array (`list.append()`). This is an amortized O(1) operation.
- **Pop**: Remove the element from the end of the array (`list.pop()`). This is an O(1) operation.
- **Top**: Return the last element of the array (`arr[-1]`) without removing it.
- **Edge Cases**: Always check for stack underflow (calling `pop` or `top` on an empty stack).

#### Time and Space Complexity
- **Time Complexity:** Amortized $O(1)$ for push, $O(1)$ for pop, top, size, and isEmpty.
- **Space Complexity:** $O(N)$ to store the elements.

#### Python Code Snippet
```python
class Stack:
    def __init__(self):
        self.arr = []

    def push(self, x: int) -> None:
        self.arr.append(x)

    def pop(self) -> int:
        if self.isEmpty():
            # In a real-world scenario, raising an exception is often preferred.
            # raise IndexError("pop from empty stack")
            return -1
        return self.arr.pop()

    def top(self) -> int:
        if self.isEmpty():
            return -1
        return self.arr[-1]

    def size(self) -> int:
        return len(self.arr)

    def isEmpty(self) -> bool:
        return len(self.arr) == 0
```

---

### 2. Implement Queue using Arrays
`[EASY]` `[FUNDAMENTAL]` `#implementation` `#array`

#### Problem Statement
Implement a Queue class using an array. It should support:
- `enqueue(x)`: Pushes element x to the back of the queue.
- `dequeue()`: Removes the element from the front of the queue and returns it.
- `front()`: Gets the front element of the queue.
- `size()`: Returns the number of elements in the queue.
- `isEmpty()`: Returns true if the queue is empty.

#### Implementation Overview
A naive implementation using a dynamic array for a queue is inefficient for dequeues because removing from the front (`list.pop(0)`) is an O(N) operation. For efficient queue operations in Python, `collections.deque` is the standard tool as it is implemented with a doubly-linked list, providing O(1) appends and pops from both ends.

- **Enqueue (Naive)**: Add element to the end of the list (O(1)).
- **Dequeue (Naive)**: Remove element from the beginning of the list (O(N)).

#### Time and Space Complexity
- **Time Complexity:** $O(1)$ for enqueue, $O(N)$ for dequeue (naive array implementation). With `deque`, both are $O(1)$.
- **Space Complexity:** $O(N)$ to store the elements.

#### Python Code Snippet (Naive)
```python
# Note: This is a simple but inefficient implementation.
# In Python, collections.deque is strongly preferred for queues.
class Queue:
    def __init__(self):
        self.arr = []

    def enqueue(self, x: int) -> None:
        self.arr.append(x)

    def dequeue(self) -> int:
        if self.isEmpty():
            return -1
        return self.arr.pop(0) # This is an O(N) operation

    def front(self) -> int:
        if self.isEmpty():
            return -1
        return self.arr[0]

    def size(self) -> int:
        return len(self.arr)

    def isEmpty(self) -> bool:
        return len(self.arr) == 0
```

#### The Pythonic Way: `collections.deque`
```python
from collections import deque

# Create a new queue
q = deque()

# Enqueue
q.append(1)
q.append(5)

# Dequeue
val = q.popleft() # val is 1, q is now deque([5])
```

---

### 3. Implement Stack using LinkedList
`[EASY]` `[FUNDAMENTAL]` `#implementation` `#linked-list`

#### Problem Statement
Implement a Stack class using a singly linked list. All operations should be O(1).

#### Implementation Overview
The LIFO (Last-In, First-Out) property of a stack is efficiently implemented by adding and removing nodes from the **head** of a linked list. We only need to maintain a `head` pointer and a size counter.
- **Push**: Create a new node. Set its `next` pointer to the current `head`, and then update `head` to be the new node.
- **Pop**: The element to pop is the `head`. To remove it, store its data, and then update `head` to point to `head.next`.
- All core operations (push, pop, top) are O(1).

#### Time and Space Complexity
- **Time Complexity:** $O(1)$ for all operations.
- **Space Complexity:** $O(N)$ to store the nodes.

#### Python Code Snippet
```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Stack:
    def __init__(self):
        self.head = None
        self.stack_size = 0

    def push(self, x: int) -> None:
        new_node = Node(x)
        new_node.next = self.head
        self.head = new_node
        self.stack_size += 1

    def pop(self) -> int:
        if self.isEmpty():
            return -1
        popped_node_data = self.head.data
        self.head = self.head.next
        self.stack_size -= 1
        return popped_node_data

    def top(self) -> int:
        if self.isEmpty():
            return -1
        return self.head.data

    def size(self) -> int:
        return self.stack_size

    def isEmpty(self) -> bool:
        return self.stack_size == 0
```

---

### 4. Implement Queue using LinkedList
`[EASY]` `[FUNDAMENTAL]` `#implementation` `#linked-list`

#### Problem Statement
Implement a Queue class using a singly linked list. All operations should be O(1).

#### Implementation Overview
The FIFO (First-In, First-Out) property requires adding to one end (rear) and removing from the other (front). We maintain two pointers: `head` (for the front) and `tail` (for the rear).
- **Enqueue**: Create a new node. If the queue is empty, set both `head` and `tail` to this new node. Otherwise, set the current `tail.next` to the new node, and then update `tail` to point to the new node.
- **Dequeue**: The element to dequeue is at the `head`. To remove it, simply advance the `head` pointer to `head.next`. If the queue becomes empty after this operation (i.e., `head` becomes `None`), the `tail` pointer must also be set to `None`.
- All core operations are O(1).

#### Time and Space Complexity
- **Time Complexity:** $O(1)$ for all operations.
- **Space Complexity:** $O(N)$ to store the nodes.

#### Python Code Snippet
```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Queue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.queue_size = 0

    def enqueue(self, x: int) -> None:
        new_node = Node(x)
        if self.isEmpty():
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.queue_size += 1

    def dequeue(self) -> int:
        if self.isEmpty():
            return -1
        popped_node_data = self.head.data
        self.head = self.head.next
        if self.head is None: # The queue is now empty
            self.tail = None
        self.queue_size -= 1
        return popped_node_data

    def front(self) -> int:
        if self.isEmpty():
            return -1
        return self.head.data

    def size(self) -> int:
        return self.queue_size

    def isEmpty(self) -> bool:
        return self.queue_size == 0
```
