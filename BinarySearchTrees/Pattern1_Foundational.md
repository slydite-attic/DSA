# Pattern 1: Foundational Operations & Traversal

This pattern covers the fundamental properties and traversal algorithms of a Binary Search Tree (BST). Understanding these core concepts is essential, as nearly all other BST problems are built upon them. The key idea in this pattern is leveraging the BST property—left subtree nodes are smaller, right subtree nodes are larger—to efficiently navigate and search the tree in O(H) time, where H is the height of the tree.

---

### 1. Introduction to Binary Search Tree
`[FUNDAMENTAL]` `[EASY]` `#bst` `#theory`

#### Problem Statement
Understand and define the properties of a Binary Search Tree.

#### Implementation Overview
A Binary Search Tree is a node-based binary tree data structure which has the following properties:
1.  **Left Subtree Property:** The value of every node in a node's left subtree is strictly less than the node's value.
2.  **Right Subtree Property:** The value of every node in a node's right subtree is strictly greater than the node's value.
3.  **Recursive Structure:** Both the left and right subtrees must also be binary search trees.
4.  **No Duplicates:** Typically, BSTs do not contain duplicate values. (This can vary by implementation, but is a common assumption).

These properties ensure that an in-order traversal of a BST will yield its values in sorted order.

#### Time and Space Complexity
- **Time Complexity:**
    -   **Balanced BST:** In a balanced BST (like an AVL or Red-Black Tree), the height `H` is proportional to `log(N)`, where `N` is the number of nodes. Operations like search, insert, and delete have an average and worst-case time complexity of **O(log N)**.
    -   **Unbalanced BST:** In the worst case (e.g., a skewed tree where each node has only one child), the tree degenerates into a linked list. The height `H` becomes `N`. Operations in this case have a worst-case time complexity of **O(N)**.
- **Space Complexity:** $O(H)$, where $H$ is the height of the tree, for recursive operations (due to stack space). Iterative operations use $O(1)$ auxiliary space.

#### Related Problems
- All other problems in this topic.

---

### 2. Search in a Binary Search Tree
`[FUNDAMENTAL]` `[EASY]` `#bst` `#traversal`

#### Problem Statement
Given the root of a BST and a target value, find the node in the tree that has the given value. If such a node does not exist, return `null`.

*Example:*
- **Input:** `root = [4,2,7,1,3]`, `val = 2`
- **Output:** The node with value 2.

#### Implementation Overview
The search operation efficiently uses the BST property to discard half of the tree at each step.
1.  Start with the `root` node.
2.  Compare the `target` value with the current node's value.
3.  - If `target == current.val`, the node is found. Return the current node.
    - If `target < current.val`, the target must be in the left subtree. Move to the left child: `current = current.left`.
    - If `target > current.val`, the target must be in the right subtree. Move to the right child: `current = current.right`.
4.  Repeat this process. If `current` becomes `null`, it means the value is not in the tree.

#### Time and Space Complexity
- **Time Complexity:** $O(H)$, where $H$ is the height of the tree. In the worst case (skewed tree), $H=N$. In the average case (balanced tree), $H = \log N$.
- **Space Complexity:** $O(1)$ for the iterative approach.

#### Python Code Snippet (Iterative)
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def search_bst(root: TreeNode, val: int) -> TreeNode:
    current = root
    while current:
        if val == current.val:
            return current
        elif val < current.val:
            current = current.left
        else:
            current = current.right
    return None
```

---

### 3. Find Min/Max in BST
`[FUNDAMENTAL]` `[EASY]` `#bst` `#traversal`

#### Problem Statement
Given the root of a BST, find the minimum and maximum value nodes in the tree.

#### Implementation Overview
-   **Minimum Value:** The smallest value is always the terminal node of the path that goes left from the root as much as possible. To find it, start at the root and repeatedly move to the left child until you reach a node with no left child.
-   **Maximum Value:** Symmetrically, the largest value is the rightmost node. To find it, start at the root and repeatedly move to the right child until you reach a node with no right child.

#### Time and Space Complexity
- **Time Complexity:** $O(H)$, where $H$ is the height of the tree.
- **Space Complexity:** $O(1)$ for the iterative approach.

#### Python Code Snippet
```python
def find_min(root: TreeNode) -> TreeNode:
    if not root: return None
    current = root
    while current.left:
        current = current.left
    return current

def find_max(root: TreeNode) -> TreeNode:
    if not root: return None
    current = root
    while current.right:
        current = current.right
    return current
```

---

### 4. Ceil in a Binary Search Tree
`[EASY]` `#bst` `#traversal`

#### Problem Statement
Given the root of a BST and a key, find the "ceil" of the key. The ceil is the smallest value in the tree that is greater than or equal to the key.

#### Implementation Overview
This is a modified search. We traverse the tree, keeping track of the best possible `ceil` value found so far.
1.  Initialize `ceil = -1`.
2.  If `current.val == key`, return `key`.
3.  If `key < current.val`, the current node is a *potential* answer. Record it (`ceil = current.val`) and move left to find an even better (smaller) ceil.
4.  If `key > current.val`, the current node is too small. The ceil must be in the right subtree.

#### Time and Space Complexity
- **Time Complexity:** $O(H)$, where $H$ is the height of the tree.
- **Space Complexity:** $O(1)$ for the iterative approach.

#### Python Code Snippet
```python
def find_ceil(root: TreeNode, key: int) -> int:
    ceil = -1
    current = root
    while current:
        if current.val == key:
            return key
        if key < current.val:
            ceil = current.val
            current = current.left
        else:
            current = current.right
    return ceil
```

---

### 5. Floor in a Binary Search Tree
`[EASY]` `#bst` `#traversal`

#### Problem Statement
Given the root of a BST and a key, find the "floor" of the key. The floor is the largest value in the tree that is less than or equal to the key.

#### Implementation Overview
The logic is symmetric to finding the ceil.
1. Initialize `floor = -1`.
2. If `current.val == key`, return `key`.
3. If `key > current.val`, the current node is a *potential* answer. Record it (`floor = current.val`) and move right to find an even better (larger) floor.
4. If `key < current.val`, the current node is too large. The floor must be in the left subtree.

#### Time and Space Complexity
- **Time Complexity:** $O(H)$, where $H$ is the height of the tree.
- **Space Complexity:** $O(1)$ for the iterative approach.

#### Python Code Snippet
```python
def find_floor(root: TreeNode, key: int) -> int:
    floor = -1
    current = root
    while current:
        if current.val == key:
            return key
        if key > current.val:
            floor = current.val
            current = current.right
        else:
            current = current.left
    return floor
```

---

### 6. Insert a given Node in Binary Search Tree
`[FUNDAMENTAL]` `[EASY]` `#bst` `#modification`

#### Problem Statement
Given the root of a BST and a value to insert, insert the value into the BST. Return the root of the BST after the insertion. The structure of the tree must be maintained.

#### Implementation Overview
We traverse the tree to find the correct empty spot for the new node.
1. Start at the root. If the tree is empty, the new node becomes the root.
2. Loop until we find an empty spot:
   - If `val < current.val`, the new node belongs in the left subtree. If `current.left` is null, insert it there. Otherwise, move `current = current.left`.
   - If `val > current.val`, the new node belongs in the right subtree. If `current.right` is null, insert it there. Otherwise, move `current = current.right`.

#### Time and Space Complexity
- **Time Complexity:** $O(H)$, where $H$ is the height of the tree.
- **Space Complexity:** $O(1)$ for the iterative approach.

#### Python Code Snippet
```python
def insert_into_bst(root: TreeNode, val: int) -> TreeNode:
    if not root:
        return TreeNode(val)

    current = root
    while True:
        if val < current.val:
            if not current.left:
                current.left = TreeNode(val)
                break
            current = current.left
        else: # val > current.val (assuming no duplicates)
            if not current.right:
                current.right = TreeNode(val)
                break
            current = current.right

    return root
```

---

### 7. Delete a Node in Binary Search Tree
`[FUNDAMENTAL]` `[MEDIUM]` `#bst` `#modification`

#### Problem Statement
Given a root node of a BST and a key, delete the node with the given key in the BST. Return the root of the BST after the deletion.

#### Implementation Overview
This is the most complex foundational operation. First, find the node to delete. Once found, there are three cases:
1.  **Case 1: Node has 0 children (leaf node).** Simply remove the node by setting its parent's corresponding child pointer to `null`.
2.  **Case 2: Node has 1 child.** Replace the node with its child by linking the node's parent directly to the node's child.
3.  **Case 3: Node has 2 children.** This is the tricky case. To maintain the BST property, we must replace the node's value with its **in-order successor** (the smallest value in its right subtree) or its **in-order predecessor** (the largest value in its left subtree).
    - Find the in-order successor (the minimum value in the right subtree).
    - Copy the successor's value to the node we want to delete.
    - Now, the problem is reduced to deleting the successor node from the right subtree (which will fall into Case 1 or 2).

#### Time and Space Complexity
- **Time Complexity:** $O(H)$, where $H$ is the height of the tree.
- **Space Complexity:** $O(H)$ due to recursion stack depth.

#### Python Code Snippet
```python
def delete_node(root: TreeNode, key: int) -> TreeNode:
    if not root:
        return None

    if key < root.val:
        root.left = delete_node(root.left, key)
    elif key > root.val:
        root.right = delete_node(root.right, key)
    else: # key == root.val, this is the node to delete
        # Case 1 & 2: 0 or 1 child
        if not root.left:
            return root.right
        if not root.right:
            return root.left

        # Case 3: 2 children
        # Find the in-order successor (smallest in the right subtree)
        successor = find_min(root.right)
        root.val = successor.val
        # Delete the successor from the right subtree
        root.right = delete_node(root.right, successor.val)

    return root

# Helper to find the minimum node (in-order successor)
def find_min(node: TreeNode) -> TreeNode:
    current = node
    while current.left:
        current = current.left
    return current
```

---

### 10. LCA in Binary Search Tree
`[EASY]` `#bst` `#traversal` `#lca`

#### Problem Statement
Given a Binary Search Tree and two nodes `p` and `q`, find the Lowest Common Ancestor (LCA) of the two nodes. The LCA is defined as the lowest node in the tree that has both `p` and `q` as descendants.

#### Implementation Overview
Unlike in a regular binary tree, we can find the LCA in a BST very efficiently in O(H) time.
1.  Start a traversal from the `root`.
2.  At each `current` node, compare its value with `p.val` and `q.val`.
    -   If both `p.val` and `q.val` are greater than `current.val`, the LCA must be in the right subtree. Move right.
    -   If both `p.val` and `q.val` are less than `current.val`, the LCA must be in the left subtree. Move left.
    -   If neither of the above is true, it means the `current` node is the "split point" where the paths to `p` and `q` diverge. This node is the LCA.

#### Time and Space Complexity
- **Time Complexity:** $O(H)$, where $H$ is the height of the tree.
- **Space Complexity:** $O(1)$ for the iterative approach.

#### Python Code Snippet
```python
def lowest_common_ancestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    current = root
    while current:
        if p.val > current.val and q.val > current.val:
            current = current.right
        elif p.val < current.val and q.val < current.val:
            current = current.left
        else:
            # Found the split point or one of the nodes, this is the LCA
            return current
    return None
```
