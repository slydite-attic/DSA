# Pattern 5: Tree Construction & Manipulation

This pattern covers problems where the primary goal is to construct a binary tree from a given representation (like traversal arrays) or to fundamentally manipulate its structure (like flattening it into a linked list). These problems test understanding of how traversals uniquely define a tree's structure.

---

### 1. Count total Nodes in a COMPLETE Binary Tree
`[MEDIUM]` `#recursion` `#complete-tree` `#properties`

#### Problem Statement
Given the root of a complete binary tree, return the number of the nodes in the tree. A complete binary tree is a binary tree in which every level, except possibly the last, is completely filled, and all nodes in the last level are as far left as possible. The solution should be more efficient than a simple O(N) traversal.

**Example:**
Input: `root = [1,2,3,4,5,6]`
Output: `6`

#### Implementation Overview
The brute-force O(N) traversal is trivial. The challenge is to find a sub-linear solution by exploiting the properties of a complete binary tree. The key idea is to compare the height of the tree as seen from the leftmost path versus the rightmost path.
1.  Calculate the height by only traversing left children from the root (`left_height`).
2.  Calculate the height by only traversing right children from the root (`right_height`).
3.  **Case 1: `left_height == right_height`**. This means the tree is a **full binary tree**. The number of nodes is simply `2^height - 1`. We can calculate this and return immediately.
4.  **Case 2: `left_height != right_height`**. This means the tree is complete but not full. We cannot use the formula for the whole tree. Instead, we fall back to the standard recursive definition: `1 + countNodes(root.left) + countNodes(root.right)`.

This approach is O((log N)^2) because at each level of recursion, we do an O(log N) height calculation.

#### Python Code Snippet
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def countNodes(self, root: TreeNode) -> int:
        if not root:
            return 0

        def get_left_height(node):
            h = 0
            while node:
                h += 1
                node = node.left
            return h

        def get_right_height(node):
            h = 0
            while node:
                h += 1
                node = node.right
            return h

        lh = get_left_height(root)
        rh = get_right_height(root)

        if lh == rh:
            return (1 << lh) - 1
        else:
            return 1 + self.countNodes(root.left) + self.countNodes(root.right)
```

---

### 2. Construct Binary Tree from Preorder and Inorder Traversal
`[MEDIUM]` `#recursion` `#construction` `#inorder` `#preorder`

#### Problem Statement
Given two integer arrays, `preorder` and `inorder`, where `preorder` is the preorder traversal of a binary tree and `inorder` is the inorder traversal of the same tree, construct and return the binary tree.

**Example:**
Input: `preorder = [3,9,20,15,7]`, `inorder = [9,3,15,20,7]`
Output: `[3,9,20,null,null,15,7]`

#### Implementation Overview
- The **first** element of `preorder` is always the **root** of the current subtree.
- The `inorder` traversal shows the root's left subtree elements to its left and the right subtree elements to its right.

**Algorithm:**
1.  Build a hash map `inorder_map` from value to index for O(1) lookups.
2.  Create a recursive `build(in_start, in_end)` function. Use a global `preorder_idx` to track our position in `preorder`.
3.  The root of the current subtree is `preorder[preorder_idx]`. Increment `preorder_idx`.
4.  Find the root's index `in_root_idx` in the `inorder_map` to split the `inorder` array into left and right subtrees.
5.  Recursively build the left subtree: `build(in_start, in_root_idx - 1)`.
6.  Recursively build the right subtree: `build(in_root_idx + 1, in_end)`.
7.  Return the `root`.

#### Python Code Snippet
```python
class Solution:
    def buildTree(self, preorder: list[int], inorder: list[int]) -> TreeNode:
        inorder_map = {val: i for i, val in enumerate(inorder)}
        self.preorder_idx = 0

        def build(in_start, in_end):
            if in_start > in_end:
                return None

            root_val = preorder[self.preorder_idx]
            self.preorder_idx += 1
            root = TreeNode(root_val)
            in_root_idx = inorder_map[root_val]

            # Build left subtree first
            root.left = build(in_start, in_root_idx - 1)
            root.right = build(in_root_idx + 1, in_end)
            return root

        return build(0, len(inorder) - 1)
```

---

### 3. Construct Binary Tree from Inorder and Postorder Traversal
`[MEDIUM]` `#recursion` `#construction` `#inorder` `#postorder`

#### Problem Statement
Given two integer arrays, `inorder` and `postorder`, construct and return the binary tree.

**Example:**
Input: `inorder = [9,3,15,20,7]`, `postorder = [9,15,7,20,3]`
Output: `[3,9,20,null,null,15,7]`

#### Implementation Overview
This is very similar to the preorder/inorder version. The key difference is:
- The **last** element of `postorder` is always the **root** of the current subtree.

**Algorithm:**
1.  Build the `inorder_map`.
2.  Use a global `postorder_idx` starting at the *end* of the `postorder` array.
3.  The root is `postorder[postorder_idx]`. Decrement `postorder_idx`.
4.  Find the root's index in `inorder` to find the split point.
5.  **Crucially, build the right subtree first**, then the left. This is because we are processing the `postorder` array backwards (`Root, Right, Left`).

#### Python Code Snippet
```python
class Solution:
    def buildTree(self, inorder: list[int], postorder: list[int]) -> TreeNode:
        inorder_map = {val: i for i, val in enumerate(inorder)}
        self.postorder_idx = len(postorder) - 1

        def build(in_start, in_end):
            if in_start > in_end:
                return None

            root_val = postorder[self.postorder_idx]
            self.postorder_idx -= 1
            root = TreeNode(root_val)
            in_root_idx = inorder_map[root_val]

            # Build right subtree first
            root.right = build(in_root_idx + 1, in_end)
            root.left = build(in_start, in_root_idx - 1)
            return root

        return build(0, len(inorder) - 1)
```

---

### 4. Serialize and Deserialize Binary Tree
`[HARD]` `#serialization` `#traversal`

#### Problem Statement
Design an algorithm to serialize a binary tree to a string and deserialize it back to the tree.

#### Implementation Overview
A common and effective way to solve this is to use a **preorder traversal**.
**Serialization:**
1.  Perform a preorder traversal.
2.  Append the node's value to a list. If a node is `null`, append a special marker (e.g., `"N"`). This is crucial for structure.
3.  Join the list to form the final string.

**Deserialization:**
1.  Split the string into a list of values. Use a `deque` for efficient `popleft` operations.
2.  Create a recursive `build()` function.
3.  Inside `build()`, get the next value. If it's the null marker, return `None`.
4.  Otherwise, create a `TreeNode` and recursively call `build()` to construct its left and right children.

#### Python Code Snippet
```python
from collections import deque
class Codec:
    def serialize(self, root):
        res = []
        def dfs(node):
            if not node:
                res.append("N")
                return
            res.append(str(node.val))
            dfs(node.left)
            dfs(node.right)
        dfs(root)
        return ",".join(res)

    def deserialize(self, data):
        vals = deque(data.split(','))
        def build():
            val = vals.popleft()
            if val == "N":
                return None
            node = TreeNode(int(val))
            node.left = build()
            node.right = build()
            return node
        return build()
```

---

### 5. Flatten Binary Tree to LinkedList
`[MEDIUM]` `#manipulation` `#recursion`

#### Problem Statement
Given the `root` of a binary tree, flatten the tree into a "linked list" in-place. The list should use the `right` child pointer, and the `left` child pointer should always be `null`. The order should be the same as a **pre-order traversal**.

#### Implementation Overview
A very clever solution uses a modified, reversed pre-order traversal (`Right, Left, Root`). This allows us to "build" the list backwards.
1.  Maintain a `prev` pointer (as a class member or passed by reference) to track the previously visited node.
2.  Create a recursive function `flatten(node)`.
3.  Recurse right: `flatten(node.right)`.
4.  Recurse left: `flatten(node.left)`.
5.  After the children are processed, `prev` will hold the node that should come *after* the current `node`. Rewire the pointers:
    a. `node.right = prev`
    b. `node.left = None`
    c. Update `prev = node` for the next call up the stack.

#### Python Code Snippet
```python
class Solution:
    def __init__(self):
        self.prev = None

    def flatten(self, root: TreeNode) -> None:
        if not root:
            return
        self.flatten(root.right)
        self.flatten(root.left)
        root.right = self.prev
        root.left = None
        self.prev = root
```

---

### 6. Requirements needed to construct a unique BT
`[EASY]` `#binarytree` `#concept`

#### Problem Statement
Given two integers representing traversals (1: Preorder, 2: Inorder, 3: Postorder), check if a unique binary tree can be constructed.

*Example:*
- **Input:** `traversal1 = 2`, `traversal2 = 1` (Inorder and Preorder)
- **Output:** `True`
- **Input:** `traversal1 = 1`, `traversal2 = 3` (Preorder and Postorder)
- **Output:** `False`

#### Implementation Overview
A unique binary tree can be constructed if and only if one of the traversals is **Inorder** (2) and the other is either **Preorder** (1) or **Postorder** (3).
If we only have Preorder and Postorder, we can construct multiple structures that are structurally different but share the same preorder and postorder.

#### Python Code Snippet
```python
def isUniqueBTPossible(traversal1, traversal2):
    # 1: Preorder, 2: Inorder, 3: Postorder
    if traversal1 == 2 or traversal2 == 2:
        if (traversal1 == 1 or traversal2 == 1) or (traversal1 == 3 or traversal2 == 3):
            return True
    return False
```
