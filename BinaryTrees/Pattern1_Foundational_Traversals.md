# Pattern 1: Foundational Traversals

This pattern covers the essential traversal algorithms for binary trees, which form the basis for solving a wide range of tree problems. It includes recursive and iterative approaches for Depth-First (Pre-order, In-order, Post-order) and Breadth-First (Level-order) traversals.

---

### 1. Binary Tree Traversals (Recursive)
`[EASY]` `#traversal` `#recursion`

#### Problem Statement
This is a foundational concept that covers the three primary ways to traverse a tree using Depth First Search (DFS):
- **In-order Traversal:** Visit the left subtree, then the current node, and finally the right subtree. (Mnemonic: **L**eft, **R**oot, **R**ight)
- **Pre-order Traversal:** Visit the current node, then the left subtree, and finally the right subtree. (Mnemonic: **R**oot, **L**eft, **R**ight)
- **Post-order Traversal:** Visit the left subtree, then the right subtree, and finally the current node. (Mnemonic: **L**eft, **R**ight, **R**oot)

Given the root of a binary tree, write recursive functions for all three traversal types.

**Example:**
For the tree: `[1, 2, 3, 4, 5]`
```
      1
     / \
    2   3
   / \
  4   5
```
- **In-order:** `4, 2, 5, 1, 3`
- **Pre-order:** `1, 2, 4, 5, 3`
- **Post-order:** `4, 5, 2, 3, 1`

#### Implementation Overview
The implementation for all three traversals is elegantly handled with recursion. A helper function is defined for each traversal, which takes the current node as an argument. The only difference is the order of the three key actions:
1.  **Base Case:** If the current node is `null` (or `None`), simply return.
2.  **Recursive Step:**
    - `traverse(node.left)`
    - `traverse(node.right)`
    - `process(node.val)`
The order of these three actions defines the traversal type.

#### Python Code Snippet
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def get_all_traversals(root):
    in_order, pre_order, post_order = [], [], []

    def traverse(node):
        if not node: return
        pre_order.append(node.val)
        traverse(node.left)
        in_order.append(node.val)
        traverse(node.right)
        post_order.append(node.val)

    traverse(root)
    return pre_order, in_order, post_order
```

---

### 2. Level Order Traversal (BFS)
`[MEDIUM]` `#traversal` `#level-order` `#bfs`

#### Problem Statement
Given the root of a binary tree, return the level order traversal of its nodes' values (i.e., from left to right, level by level).

**Example:**
Input: `root = [3,9,20,null,null,15,7]`
Output: `[[3],[9,20],[15,7]]`

#### Implementation Overview
Level order traversal is implemented using a queue, which is a hallmark of Breadth-First Search (BFS).
1.  Initialize a `result` list and a queue (e.g., `collections.deque`) with the root node.
2.  Loop while the queue is not empty.
3.  Inside the loop, get the `level_size` (number of nodes currently in the queue). This is key to processing one level at a time.
4.  Create a `current_level` list.
5.  Loop `level_size` times: dequeue a node, add its value to `current_level`, and enqueue its children (if they exist).
6.  Add `current_level` to the `result`.

#### Python Code Snippet
```python
from collections import deque
def levelOrder(root: TreeNode) -> list[list[int]]:
    if not root: return []
    result = []
    q = deque([root])
    while q:
        level_size = len(q)
        current_level = []
        for _ in range(level_size):
            node = q.popleft()
            current_level.append(node.val)
            if node.left: q.append(node.left)
            if node.right: q.append(node.right)
        result.append(current_level)
    return result
```

---

### 3. Iterative Preorder Traversal
`[EASY]` `#traversal` `#preorder` `#iterative` `#stack`

#### Problem Statement
Given the root of a binary tree, return the preorder traversal of its nodes' values using an iterative approach.

#### Implementation Overview
An iterative preorder traversal directly simulates recursion using a stack.
1.  Initialize an empty `result` list and a `stack` with the `root` node.
2.  Loop while the stack is not empty.
3.  Pop a node. Add its value to `result`.
4.  **Crucially, push the right child onto the stack first, then the left child.** A stack is LIFO, so pushing left last ensures it's processed first, maintaining the "Root, Left, Right" order.

#### Python Code Snippet
```python
def preorder_traversal_iterative(root: TreeNode) -> list[int]:
    if not root: return []
    result = []
    stack = [root]
    while stack:
        node = stack.pop()
        result.append(node.val)
        if node.right: stack.append(node.right)
        if node.left: stack.append(node.left)
    return result
```

---

### 4. Iterative Inorder Traversal
`[EASY]` `#traversal` `#inorder` `#iterative` `#stack`

#### Problem Statement
Given the root of a binary tree, return the inorder traversal of its nodes' values using an iterative approach.

#### Implementation Overview
Iterative inorder is more complex. We can't process a node just by popping it; we must wait until its entire left subtree has been visited.
1.  Initialize an empty `result` list, an empty `stack`, and a `current` pointer to the `root`.
2.  Loop while `current` is not null OR the `stack` is not empty.
3.  **Go Left:** While `current` is not null, push it onto the `stack` and move `current = current.left`.
4.  **Visit Node:** `current` is now null. Pop a node from the stack, add its value to `result`.
5.  **Go Right:** Set `current = popped_node.right` to explore the right subtree. The loop will then handle this new `current`.

#### Python Code Snippet
```python
def inorder_traversal_iterative(root: TreeNode) -> list[int]:
    result, stack = [], []
    current = root
    while current or stack:
        while current:
            stack.append(current)
            current = current.left
        current = stack.pop()
        result.append(current.val)
        current = current.right
    return result
```

---

### 5. Iterative Post-order Traversal (2 Stacks)
`[EASY]` `#traversal` `#postorder` `#iterative` `#stack`

#### Problem Statement
Given the root of a binary tree, return the postorder traversal of its nodes' values using an iterative approach with two stacks.

#### Implementation Overview
This method uses a clever trick: `Postorder (L, R, Root)` is the reverse of `(Root, R, L)`. We can generate the `(Root, R, L)` sequence easily and then reverse it.
1.  Use `stack1` for the main traversal and `stack2` to store the intermediate result. Push `root` to `stack1`.
2.  While `stack1` is not empty, pop a node. Push this node onto `stack2`.
3.  Push the popped node's left child, then its right child, to `stack1`.
4.  After the loop, `stack2` holds the `(Root, R, L)` sequence. Pop everything from `stack2` into the final `result` list to get the correct postorder sequence.

#### Python Code Snippet
```python
def postorder_traversal_2_stacks(root: TreeNode) -> list[int]:
    if not root: return []
    stack1, stack2 = [root], []
    while stack1:
        node = stack1.pop()
        stack2.append(node)
        if node.left: stack1.append(node.left)
        if node.right: stack1.append(node.right)

    result = []
    while stack2:
        result.append(stack2.pop().val)
    return result
```

---

### 6. Iterative Post-order Traversal (1 Stack)
`[MEDIUM]` `#traversal` `#postorder` `#iterative` `#stack`

#### Problem Statement
Given the root of a binary tree, return the postorder traversal of its nodes' values using an iterative approach with only one stack.

#### Implementation Overview
This is the trickiest of the iterative traversals. We need to ensure we only process a node after both its left and right children have been processed. We can track the `last_visited` node to achieve this.
1. Loop while `current` is not null or `stack` is not empty.
2. Go as far left as possible, pushing nodes to the stack.
3. Once `current` is null, `peek` at the stack top. If it has a right child that has **not** been visited yet, move `current` to that right child and continue.
4. Otherwise, we can visit the node at the top of the stack. Pop it, add its value to the result, and update `last_visited`.

#### Python Code Snippet
```python
def postorder_traversal_1_stack(root: TreeNode) -> list[int]:
    if not root: return []
    result, stack = [], []
    current, last_visited = root, None
    while current or stack:
        while current:
            stack.append(current)
            current = current.left
        peek_node = stack[-1]
        if peek_node.right and peek_node.right != last_visited:
            current = peek_node.right
        else:
            last_visited = stack.pop()
            result.append(last_visited.val)
    return result
```

---

### 7. Preorder Inorder Postorder Traversals in One Traversal
`[MEDIUM]` `#binarytree` `#traversal` `#stack`

#### Problem Statement
Given the root of a Binary Tree, return the Preorder, Inorder, and Postorder traversals of the tree computed in a single traversal (pass) of the tree.

*Example:*
- **Input:** `root = [1, null, 2, 3]`
- **Output:**
  - Preorder: `[1, 2, 3]`
  - Inorder: `[1, 3, 2]`
  - Postorder: `[3, 2, 1]`

#### Implementation Overview
We use a stack to simulate recursion. The stack stores pairs of `[node, state]`, where the state indicates which visit to the node we are on:
1. **State = 1 (Preorder)**: We push node value to Preorder list, change state to 2, and if a left child exists, push it onto stack with state 1.
2. **State = 2 (Inorder)**: We push node value to Inorder list, change state to 3, and if a right child exists, push it onto stack with state 1.
3. **State = 3 (Postorder)**: We push node value to Postorder list and pop the node from the stack.

#### Python Code Snippet
```python
def preInPostTraversal(root):
    if not root:
        return [], [], []
    pre, inorder, post = [], [], []
    stack = [[root, 1]]
    while stack:
        node, state = stack[-1]
        if state == 1:
            pre.append(node.val)
            stack[-1][1] = 2
            if node.left:
                stack.append([node.left, 1])
        elif state == 2:
            inorder.append(node.val)
            stack[-1][1] = 3
            if node.right:
                stack.append([node.right, 1])
        else:
            post.append(node.val)
            stack.pop()
    return pre, inorder, post
```
