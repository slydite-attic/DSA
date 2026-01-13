# Pattern 3: In-order Traversal Applications

A defining property of a Binary Search Tree is that a standard in-order traversal (Left, Root, Right) visits the nodes in ascending sorted order. This pattern covers a wide range of problems that are solved by leveraging this property. The solution often involves performing an in-order traversal and either analyzing the sequence of nodes as they are visited or processing the resulting sorted list.

---

### 8. Find K-th smallest/largest element in BST
`[MEDIUM]` `#bst` `#inorder-traversal`

#### Problem Statement
Given the root of a BST and an integer `k`, find the `k`-th smallest element in the tree.

*Example:*
- **Input:** `root = [3,1,4,null,2]`, `k = 1`
- **Output:** `1`

#### Implementation Overview
Since an in-order traversal visits nodes in sorted order, the `k`-th node visited will be the `k`-th smallest element.

**Method 1: Recursive In-order Traversal**
1.  Use a counter variable, initialized to `k`.
2.  In the traversal, after visiting the left subtree but before visiting the root, decrement the counter.
3.  If the counter becomes `0`, the current node is the `k`-th smallest. Store this value.

**Method 2: Iterative In-order Traversal with a Stack**
This is often preferred to avoid deep recursion.
1. Use a stack to simulate the in-order traversal.
2. Go left as far as possible, pushing nodes onto the stack.
3. Once you can't go left anymore, pop a node. This is the next node in the in-order sequence. Decrement `k`. If `k` is now 0, this is your answer.
4. Move to the right child of the popped node and repeat the process.

To find the **k-th largest** element, you can find the `(N-k+1)`-th smallest element or perform a reverse in-order traversal (Right, Root, Left).

#### Time and Space Complexity
- **Time Complexity:** $O(H + k)$, where $H$ is the height of the tree. We need to reach the leftmost node ($O(H)$) and then pop $k$ elements.
- **Space Complexity:** $O(H)$ for the stack.

#### Python Code Snippet (Iterative)
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def kth_smallest(root: TreeNode, k: int) -> int:
    stack = []
    current = root

    while current or stack:
        # Go left as far as possible
        while current:
            stack.append(current)
            current = current.left

        # Process the node
        current = stack.pop()
        k -= 1
        if k == 0:
            return current.val

        # Go right
        current = current.right
```

---

### 9. Check if a tree is a BST or BT
`[MEDIUM]` `#bst` `#inorder-traversal` `#validation`

#### Problem Statement
Given the root of a binary tree, determine if it is a valid Binary Search Tree (BST).

#### Implementation Overview
**Method 1: Recursive with Valid Range (Min/Max)**
A robust method is a recursive approach that validates each node against a `(lower_bound, upper_bound)` range.
1.  The initial call is `is_valid(root, -infinity, +infinity)`.
2.  For a `node` to be valid, its value must be strictly between its `lower_bound` and `upper_bound`.
3.  When recurring left, the valid range becomes `(lower_bound, node.val)`.
4.  When recurring right, the valid range becomes `(node.val, upper_bound)`.

**Method 2: In-order Traversal**
Since an in-order traversal of a valid BST yields a sorted sequence, we can check this property.
1. Perform an in-order traversal.
2. Keep track of the value of the previously visited node.
3. At each current node, check if its value is strictly greater than the previous node's value. If not, the tree is not a valid BST.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the number of nodes in the tree, as we visit each node once.
- **Space Complexity:** $O(N)$ for the recursion stack (worst case skewed tree).

#### Python Code Snippet (In-order Traversal)
```python
class Solution:
    def isValidBST(self, root: TreeNode) -> bool:
        # Use a class member to store the previous value
        self.prev_val = float('-inf')

        def inorder(node):
            if not node:
                return True

            # Check left subtree
            if not inorder(node.left):
                return False

            # Check current node against previous
            if node.val <= self.prev_val:
                return False
            self.prev_val = node.val

            # Check right subtree
            return inorder(node.right)

        return inorder(root)
```

---

### 12. Inorder Successor/Predecessor in BST
`[MEDIUM]` `#bst` `#inorder-traversal`

#### Problem Statement
Given a node `p` in a BST, find its in-order successor. The successor is the node with the smallest key greater than `p.val`.

#### Implementation Overview
The solution depends on whether the given node `p` has a right subtree.
1.  **If `p` has a right subtree:** The in-order successor is the node with the minimum value in that right subtree. To find this, we simply traverse as far left as possible from `p.right`.
2.  **If `p` has no right subtree:** The successor is an ancestor. We must find the lowest ancestor of `p` for which `p` is in its left subtree. We can find this by traversing down from the `root` of the entire tree.
    -   While traversing towards `p`: if we move left (`p.val < current.val`), the `current` node is a potential successor. If we move right, it is not.

#### Time and Space Complexity
- **Time Complexity:** $O(H)$, where $H$ is the height of the tree.
- **Space Complexity:** $O(1)$, as we use constant extra space for traversal.

#### Python Code Snippet (Successor)
```python
def inorder_successor(root: TreeNode, p: TreeNode) -> TreeNode:
    # Case 1: Node has a right subtree
    if p.right:
        current = p.right
        while current.left:
            current = current.left
        return current

    # Case 2: Node has no right subtree
    successor = None
    current = root
    while current:
        if p.val < current.val:
            successor = current # Potential successor
            current = current.left
        elif p.val > current.val:
            current = current.right
        else: # We found p
            break
    return successor
```

---

### 14. Two Sum In BST
`[EASY]` `#bst` `#inorder-traversal` `#two-pointers` `#hash-set`

#### Problem Statement
Given the root of a BST and a target number `k`, return `true` if there exist two elements in the BST such that their sum is equal to `k`, or `false` otherwise.

#### Implementation Overview
**Approach 1: In-order Traversal + Two Pointers (O(N) time, O(N) space)**
1.  Perform an in-order traversal of the BST to get a sorted list of its node values.
2.  Use the standard two-pointer technique on this sorted list to find if a pair sums to `k`.

**Approach 2: Hashing (O(N) time, O(N) space)**
1.  Traverse the tree (any order works).
2.  For each node with value `v`, check if `k - v` exists in a hash set.
3.  If it exists, return `true`.
4.  If not, add `v` to the hash set.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the number of nodes.
- **Space Complexity:** $O(N)$ to store the hash set or the inorder traversal list.

#### Python Code Snippet (Hashing)
```python
def find_target_bst(root: TreeNode, k: int) -> bool:
    if not root:
        return False

    seen = set()
    stack = [root]

    while stack:
        node = stack.pop()
        if k - node.val in seen:
            return True
        seen.add(node.val)

        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)

    return False
```

---

### 15. Recover BST | Correct BST with two nodes swapped
`[MEDIUM]` `#bst` `#inorder-traversal` `#modification`

#### Problem Statement
You are given the `root` of a BST where the values of exactly two nodes have been swapped by mistake. Recover the tree without changing its structure.

*Example:*
- **Input:** `root = [3,1,4,null,null,2]` (3 and 2 are swapped)
- **Output:** `root = [2,1,4,null,null,3]`

#### Implementation Overview
The core insight is that an in-order traversal of the corrupted BST will reveal the swapped nodes. In a correct in-order traversal, `prev.val < current.val` always holds. A swap will create one or two violations of this rule.
1.  Initialize three pointers: `first = None`, `middle = None`, `last = None`, and `prev = TreeNode(float('-inf'))`.
2.  Perform an in-order traversal. At each node, compare `current.val` with `prev.val`.
3.  If `prev.val > current.val`, we've found a "dip" or violation.
    -   If this is the **first violation** (`first` is `None`), it means `prev` is the first out-of-place node. So, `first = prev`. `middle` is set to the `current` node, as it might be the second swapped node (in case the swapped nodes are adjacent).
    -   If this is the **second violation** (`first` is not `None`), it means the `current` node is the second out-of-place node. So, `last = current`.
4.  After the traversal, if `last` is not `None`, it means the swapped nodes were non-adjacent. Swap `first` and `last`.
5.  If `last` is `None`, it means the swapped nodes were adjacent. Swap `first` and `middle`.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the number of nodes.
- **Space Complexity:** $O(N)$ for recursion stack (worst case). Can be optimized to $O(1)$ using Morris Traversal.

#### Python Code Snippet
```python
class Solution:
    def recoverTree(self, root: TreeNode) -> None:
        self.first = None
        self.middle = None
        self.last = None
        self.prev = TreeNode(float('-inf'))

        def inorder(node):
            if not node: return
            inorder(node.left)

            if self.prev.val > node.val:
                if not self.first:
                    self.first = self.prev
                    self.middle = node
                else:
                    self.last = node
            self.prev = node

            inorder(node.right)

        inorder(root)

        if self.last:
            self.first.val, self.last.val = self.last.val, self.first.val
        else:
            self.first.val, self.middle.val = self.middle.val, self.first.val
```
