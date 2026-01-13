# Pattern 3: Recursive Properties & Path Sums

This pattern focuses on a common recursive strategy for solving binary tree problems. The core idea is to perform a post-order traversal (or a variation) where each node's recursive call returns a value (or set of values) to its parent. The parent then uses these values from its left and right children to compute a property for its own subtree. This "pass-up" information flow is key.

---

### 1. Height of a Binary Tree
`[EASY]` `#recursion` `#height-balanced`

#### Problem Statement
Given the root of a binary tree, find its maximum depth (or height). The maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.

**Example:**
Input: `root = [3,9,20,null,null,15,7]`
Output: `3`

#### Implementation Overview
This is a classic recursion problem that perfectly demonstrates the post-order traversal pattern. The height of a tree is defined by the height of its subtrees.

1.  **Base Case:** If the current node is `null`, its height is `0`. This is the termination condition for the recursion.
2.  **Recursive Step:**
    a. Recursively calculate the height of the left subtree: `left_height = height(node.left)`.
    b. Recursively calculate the height of the right subtree: `right_height = height(node.right)`.
3.  **Combine Results:** The height of the tree rooted at the current node is `1 + max(left_height, right_height)`. The `+1` accounts for the current node itself.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the number of nodes. We visit each node once.
- **Space Complexity:** $O(H)$, where $H$ is the height of the tree, due to recursion stack depth.

#### Python Code Snippet
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def maxDepth(root: TreeNode) -> int:
    if not root:
        return 0
    left_depth = maxDepth(root.left)
    right_depth = maxDepth(root.right)
    return 1 + max(left_depth, right_depth)
```

#### Tricks/Gotchas
- Be clear about the definition of height/depth. LeetCode and most platforms define it as the number of nodes, hence the `1 + ...`.
- The time complexity is O(N) because we visit every node once. The space complexity is O(H) due to the recursion stack.

#### Related Problems
- `[Pattern 3]` Check if the Binary tree is height-balanced or not
- `[Pattern 3]` Diameter of Binary Tree

---

### 2. Check if the Binary tree is height-balanced or not
`[EASY]` `#recursion` `#height-balanced`

#### Problem Statement
Given a binary tree, determine if it is height-balanced. A height-balanced binary tree is a binary tree in which the depth of the two subtrees of every node never differs by more than one.

#### Implementation Overview
The key insight is to modify the standard height-finding function. Instead of just returning the height, we can make it return a special value (like `-1`) to signal that an imbalance has been detected somewhere in its subtree.

1.  Create a recursive helper function `check_height(node)`.
2.  **Base Case:** If `node` is null, it's balanced and has a height of `0`. Return `0`.
3.  **Recursive Step:**
    a. Recursively call on the left child: `left_height = check_height(node.left)`.
    b. If `left_height` is `-1`, the left subtree is already unbalanced. Propagate this up by immediately returning `-1`.
    c. Do the same for the right subtree.
4.  **Check Current Node:** After getting valid heights, check if `abs(left_height - right_height) > 1`. If so, the current node is unbalanced; return `-1`.
5.  **Return Height:** If balanced, return its height as usual: `1 + max(left_height, right_height)`.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the number of nodes. We visit each node once.
- **Space Complexity:** $O(H)$, where $H$ is the height of the tree, due to recursion stack depth.

#### Python Code Snippet
```python
class Solution:
    def isBalanced(self, root: TreeNode) -> bool:
        def check_height(node):
            if not node: return 0
            left_height = check_height(node.left)
            if left_height == -1: return -1
            right_height = check_height(node.right)
            if right_height == -1: return -1
            if abs(left_height - right_height) > 1: return -1
            return 1 + max(left_height, right_height)
        return check_height(root) != -1
```

#### Tricks/Gotchas
- This O(N) solution is efficient because it combines the height calculation and the balance check into a single post-order traversal.

---

### 3. Diameter of Binary Tree
`[EASY]` `#recursion` `#diameter`

#### Problem Statement
Given the root of a binary tree, return the length of the diameter of the tree. The diameter is the length of the longest path between any two nodes. This path may or may not pass through the root.

#### Implementation Overview
The longest path might not pass through the root. A recursive function must do two things:
1.  **Return** the height (max depth) of the subtree it's called on.
2.  **Update** a global `max_diameter` variable as a side effect.

**Algorithm:**
1.  Initialize `max_diameter = 0`.
2.  Create a recursive helper `height(node)`.
3.  **Recursive Step:** For the current node, the longest path passing through it has a length of `left_height + right_height`. We compare this with our global `max_diameter`.
4.  **Return Value:** The function must still return the height of the current subtree to its parent, which is `1 + max(left_height, right_height)`.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the number of nodes. We visit each node once.
- **Space Complexity:** $O(H)$, where $H$ is the height of the tree, due to recursion stack depth.

#### Python Code Snippet
```python
class Solution:
    def diameterOfBinaryTree(self, root: TreeNode) -> int:
        self.max_diameter = 0
        def height(node):
            if not node: return 0
            left_height = height(node.left)
            right_height = height(node.right)
            self.max_diameter = max(self.max_diameter, left_height + right_height)
            return 1 + max(left_height, right_height)
        height(root)
        return self.max_diameter
```

---

### 4. Maximum Path Sum
`[HARD]` `#recursion` `#path-sum`

#### Problem Statement
A path in a binary tree is a sequence of nodes where each pair of adjacent nodes has an edge connecting them. A node can only appear in the sequence at most once. The path sum is the sum of the node's values in the path. Given the root of a binary tree, return the maximum path sum of any non-empty path.

#### Implementation Overview
This follows the same pattern as Diameter. The recursive function `max_path_down(node)` will compute the maximum path sum starting at `node` and going downwards into *one* of its subtrees.
1.  Initialize a global `max_sum` to `-infinity`.
2.  **Recursive Step:** Get `left_path = max(0, max_path_down(node.left))` and `right_path = max(0, max_path_down(node.right))`. We use `max(0, ...)` because we don't want to include paths with negative sums.
3.  **Update Global Maximum:** The maximum path that "turns" at the current node is `node.val + left_path + right_path`. We update our global `max_sum` with this value.
4.  **Return Value:** The function must return the maximum path sum going *straight down* from the current node: `node.val + max(left_path, right_path)`.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the number of nodes. We visit each node once.
- **Space Complexity:** $O(H)$, where $H$ is the height of the tree, due to recursion stack depth.

#### Python Code Snippet
```python
class Solution:
    def maxPathSum(self, root: TreeNode) -> int:
        self.max_sum = float('-inf')
        def max_path_down(node):
            if not node: return 0
            left_path = max(0, max_path_down(node.left))
            right_path = max(0, max_path_down(node.right))
            self.max_sum = max(self.max_sum, node.val + left_path + right_path)
            return node.val + max(left_path, right_path)
        max_path_down(root)
        return self.max_sum
```

---

### 5. Check if two trees are identical or not
`[EASY]` `#recursion` `#tree-comparison`

#### Problem Statement
Given the roots of two binary trees, `p` and `q`, write a function to check if they are the same or not. Two binary trees are the same if they are structurally identical and the nodes have the same value.

#### Implementation Overview
A straightforward parallel recursion.
1.  **Base Cases:** If both nodes are `null`, they are identical. If one is `null` but the other isn't, or if their values differ, they are not identical.
2.  **Recursive Step:** Return `isSameTree(p.left, q.left) AND isSameTree(p.right, q.right)`.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the minimum number of nodes in the two trees.
- **Space Complexity:** $O(H)$, where $H$ is the height of the shorter tree, due to recursion stack depth.

#### Python Code Snippet
```python
class Solution:
    def isSameTree(self, p: TreeNode, q: TreeNode) -> bool:
        if not p and not q: return True
        if not p or not q or p.val != q.val: return False
        return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)
```

---

### 6. Symmetric Binary Tree
`[EASY]` `#recursion` `#tree-comparison` `#symmetry`

#### Problem Statement
Given the root of a binary tree, check whether it is a mirror of itself (i.e., symmetric around its center).

#### Implementation Overview
A tree is symmetric if the root's left subtree is a mirror image of the root's right subtree. We write a recursive helper `isMirror(node1, node2)`.
1.  **Base Cases:** Same as `isSameTree`.
2.  **Recursive Step:** The key difference. We must check if `node1.left` is a mirror of `node2.right` AND `node1.right` is a mirror of `node2.left`.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the number of nodes.
- **Space Complexity:** $O(H)$, where $H$ is the height of the tree, due to recursion stack depth.

#### Python Code Snippet
```python
class Solution:
    def isSymmetric(self, root: TreeNode) -> bool:
        if not root: return True
        def isMirror(node1, node2):
            if not node1 and not node2: return True
            if not node1 or not node2 or node1.val != node2.val: return False
            return isMirror(node1.left, node2.right) and isMirror(node1.right, node2.left)
        return isMirror(root.left, root.right)

---

### 7. Check for Children Sum Property
`[EASY]` `#recursion` `#properties`

#### Problem Statement
Given the root of a binary tree, check if the tree satisfies the "Children Sum Property". The property states that for every node in the tree, its value must be equal to the sum of the values of its left and right children. For a leaf node, this property is trivially true. If a child is null, its value is considered 0.

**Example:**
Input:
```
      10
     /  \
    8    2
   / \  /
  3  5 2
```
Output: `True` (10=8+2, 8=3+5, 2=2+0)

#### Implementation Overview
This can be solved with a straightforward recursive traversal. For each node, we check if it satisfies the property and then verify that its left and right subtrees also satisfy the property.

1.  **Base Case:** If the current `node` is `null` or it is a leaf node, it trivially satisfies the property. Return `True`.
2.  **Calculate Children Sum:** Get the values of the left and right children. If a child is `null`, treat its value as `0`.
3.  **Check Current Node:** Compare `node.val` with the sum of its children's values.
4.  **Recurse:** If the current node is valid, recursively call the function on its left and right children. The overall result is true only if the current node is valid AND both recursive calls return true.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the number of nodes.
- **Space Complexity:** $O(H)$, where $H$ is the height of the tree, due to recursion stack depth.

#### Python Code Snippet
```python
class Solution:
    def isChildrenSum(self, root: TreeNode) -> bool:
        if not root or (not root.left and not root.right):
            return True

        # Calculate sum of children's values
        child_sum = 0
        if root.left:
            child_sum += root.left.val
        if root.right:
            child_sum += root.right.val

        # Check current node and recurse
        return (root.val == child_sum and
                self.isChildrenSum(root.left) and
                self.isChildrenSum(root.right))
```

#### Tricks/Gotchas
- **Leaf Nodes:** Correctly identifying the base case for leaf nodes is important. A leaf node has no children to sum, so the property is considered true for it.
- **Complete Traversal:** You must check the property for all nodes in the tree, not just the root. The recursion ensures this.
```
