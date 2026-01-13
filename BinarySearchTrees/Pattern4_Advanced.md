# Pattern 4: Advanced & Multi-Step Problems

This pattern covers the most challenging problems in the BST topic. These problems often require combining several concepts from other patterns, such as traversal, modification, and validation, or they involve complex recursive solutions that pass rich state between function calls. They test a deep understanding of tree properties and algorithms.

---

### 13. Merge 2 BST's
`[MEDIUM]` `#bst` `#inorder-traversal` `#construction`

#### Problem Statement
Given two Binary Search Trees, merge them into a single balanced BST.

*Example:*
- **Input:**
  - BST 1: `root1 = [2,1,3]`
  - BST 2: `root2 = [5,4,6]`
- **Output:** A balanced BST like `[3,1,5,null,2,4,6]`

#### Implementation Overview
A straightforward and practical approach involves breaking the problem down into three distinct steps:
1.  **Flatten to Sorted Lists:** Perform an in-order traversal on both BSTs. Since an in-order traversal of a BST produces a sorted sequence, this will give us two sorted lists of all the elements from each tree.
2.  **Merge Sorted Lists:** Merge the two sorted lists into a single, combined sorted list. This is a standard O(N+M) operation, where N and M are the number of nodes in the two trees.
3.  **Construct Balanced BST from Sorted List:** Convert the final merged, sorted list into a balanced BST. This is a classic problem solved recursively:
    -   The middle element of the current list segment becomes the root of the (sub)tree.
    -   The left half of the list is used to recursively construct the left subtree.
    -   The right half of the list is used to recursively construct the right subtree.
    -   This process ensures the resulting tree is height-balanced.

This approach is easy to reason about but has a space complexity of O(N+M) to store the lists.

#### Time and Space Complexity
- **Time Complexity:** $O(M + N)$, where $M$ and $N$ are the number of nodes in each tree.
- **Space Complexity:** $O(M + N)$ to store the lists and the recursion stack.

#### Python Code Snippet
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def merge_bsts(root1: TreeNode, root2: TreeNode) -> TreeNode:

    # Step 1: Flatten BSTs to sorted lists
    def inorder_traversal(root):
        if not root:
            return []
        return inorder_traversal(root.left) + [root.val] + inorder_traversal(root.right)

    list1 = inorder_traversal(root1)
    list2 = inorder_traversal(root2)

    # Step 2: Merge the two sorted lists
    merged_list = []
    i, j = 0, 0
    while i < len(list1) and j < len(list2):
        if list1[i] <= list2[j]:
            merged_list.append(list1[i])
            i += 1
        else:
            merged_list.append(list2[j])
            j += 1
    merged_list.extend(list1[i:])
    merged_list.extend(list2[j:])

    # Step 3: Construct a balanced BST from the sorted list
    def sorted_list_to_bst(arr):
        if not arr:
            return None

        mid = len(arr) // 2
        root = TreeNode(arr[mid])

        root.left = sorted_list_to_bst(arr[:mid])
        root.right = sorted_list_to_bst(arr[mid+1:])

        return root

    return sorted_list_to_bst(merged_list)

```

#### Tricks/Gotchas
- **Space Complexity:** The main drawback of this method is its O(N+M) space requirement. More complex in-place solutions exist but are much harder to implement correctly (e.g., converting BSTs to doubly linked lists, merging the lists, and then converting back).
- **Balanced Tree Requirement:** Simply inserting all elements from one tree into the other can lead to a skewed, unbalanced tree. The construction from a sorted list ensures balance.

#### Related Problems
- (Arrays) 36. Merge two sorted arrays without extra space

---

### 16. Largest BST in Binary Tree
`[MEDIUM]` `#bst` `#binary-tree` `#postorder-traversal` `#dp-on-trees`

#### Problem Statement
Given a binary tree, find the size (number of nodes) of the largest subtree that is also a valid Binary Search Tree.

*Example:*
- **Input:** `root = [10,5,15,1,8,null,7]`
- **Output:** `3` (The largest BST is the subtree rooted at 5: `[5,1,8]`)

#### Implementation Overview
This is a classic "DP on Trees" problem. A simple top-down approach of checking `isValidBST` for every node would be very inefficient (O(N^2)). The optimal O(N) solution involves a single traversal (post-order is natural) where each node returns a bundle of information about its subtree to its parent.

1.  Define a custom data structure or tuple to hold the information returned from each recursive call. This info should include:
    -   `is_bst`: A boolean, `True` if the subtree is a BST.
    -   `size`: The number of nodes in the subtree.
    -   `min_val`: The minimum value in the subtree.
    -   `max_val`: The maximum value in the subtree.
2.  Use a post-order traversal (`Left, Right, Root`) so that information about children is available before processing the parent.
3.  **Recursive Step:** For a `current` node:
    a. Recursively call on the left and right children.
    b. The `current` node can be the root of a valid BST only if:
        -   Its left child's subtree is a BST.
        -   Its right child's subtree is a BST.
        -   `current.val` is greater than the `max_val` from the left child's info.
        -   `current.val` is less than the `min_val` from the right child's info.
    c. **If it is a valid BST:** The new size is `1 + left_info.size + right_info.size`. Update a global `max_size` tracker. Return the new, combined info bundle upwards.
    d. **If it is not a valid BST:** The chain is broken. Return info indicating this (e.g., `is_bst=False`, `size=...`) so that all ancestors also know they cannot form a BST with this subtree.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the number of nodes in the tree. We visit each node once.
- **Space Complexity:** $O(N)$ for the recursion stack in the worst case (skewed tree).

#### Python Code Snippet
```python
class NodeInfo:
    def __init__(self, is_bst, size, min_val, max_val):
        self.is_bst = is_bst
        self.size = size
        self.min_val = min_val
        self.max_val = max_val

class Solution:
    def largestBSTSubtree(self, root: TreeNode) -> int:
        self.max_bst_size = 0
        self.postorder(root)
        return self.max_bst_size

    def postorder(self, node: TreeNode) -> NodeInfo:
        if not node:
            # Base case: an empty node is a valid BST of size 0
            return NodeInfo(True, 0, float('inf'), float('-inf'))

        left_info = self.postorder(node.left)
        right_info = self.postorder(node.right)

        # Check if the current subtree is a valid BST
        if (left_info.is_bst and right_info.is_bst and
            left_info.max_val < node.val < right_info.min_val):

            # It is a valid BST
            current_size = 1 + left_info.size + right_info.size
            self.max_bst_size = max(self.max_bst_size, current_size)

            # The min of this new BST is the min of the left subtree (or node.val if no left)
            # The max of this new BST is the max of the right subtree (or node.val if no right)
            current_min = min(node.val, left_info.min_val)
            current_max = max(node.val, right_info.max_val)

            return NodeInfo(True, current_size, current_min, current_max)
        else:
            # It is not a valid BST, so propagate this info up
            # We don't care about the size or values if it's not a BST
            return NodeInfo(False, 0, 0, 0)
```

#### Tricks/Gotchas
- **Post-order Traversal:** This is essential. You must have information about the children before you can make a decision about the parent.
- **Rich State:** The key is passing a rich state object (like the `NodeInfo` class) up the recursion, not just a simple value.

#### Related Problems
- 9. Check if a tree is a BST or BT
