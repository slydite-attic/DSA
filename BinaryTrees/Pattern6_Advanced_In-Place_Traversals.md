# Pattern 6: Advanced & In-Place Traversals (Morris)

This pattern is dedicated to the Morris Traversal, a sophisticated and space-efficient way to traverse a binary tree without using recursion or a stack, achieving O(1) extra space. It works by temporarily modifying the tree structure to create "threads" or links to navigate back up the tree after visiting a subtree.

---

### 1. Morris Preorder Traversal of a Binary Tree
`[MEDIUM]` `#traversal` `#morris-traversal` `#preorder` `#in-place`

#### Problem Statement
Given the root of a binary tree, return the preorder traversal of its nodes' values using Morris Traversal, which uses O(1) extra space.

#### Implementation Overview
Morris Traversal works by creating temporary "threads" (links) from a node's inorder predecessor back to the node itself. This allows us to return to the node after visiting its left subtree, all without using a stack. The algorithm for **preorder** is a slight modification of the inorder version.

1.  Initialize `current = root`.
2.  While `current` is not null:
    a. If `current` has no left child, visit it (`result.append(current.val)`) and move right (`current = current.right`).
    b. If `current` has a left child:
        i. Find the inorder predecessor (the rightmost node in the left subtree).
        ii. **If no thread exists** (`predecessor.right` is null):
            - **Visit the current node** (this is the key preorder step).
            - Create the thread: `predecessor.right = current`.
            - Move left to process the left subtree: `current = current.left`.
        iii. **If a thread already exists** (`predecessor.right == current`):
            - We have returned from the left subtree.
            - Remove the thread: `predecessor.right = None`.
            - Move to the right child: `current = current.right`.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$. While some edges are traversed more than once, amortized time is linear.
- **Space Complexity:** $O(1)$, as it does not use a stack or recursion.

#### Python Code Snippet
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def preorder_morris_traversal(root: TreeNode) -> list[int]:
    result = []
    current = root
    while current:
        if not current.left:
            result.append(current.val)
            current = current.right
        else:
            predecessor = current.left
            while predecessor.right and predecessor.right != current:
                predecessor = predecessor.right
            if not predecessor.right:
                result.append(current.val) # Visit before going left
                predecessor.right = current
                current = current.left
            else:
                predecessor.right = None # Remove thread
                current = current.right
    return result
```

#### Tricks/Gotchas
- The only difference between Morris Inorder and Preorder is *when* you visit the node. In Preorder, you visit the node right before you create the thread. In Inorder, you visit it after you return via an existing thread.

#### Related Problems
- `[Pattern 6]` Morris Inorder Traversal of a Binary Tree.

---

### 2. Morris Inorder Traversal of a Binary Tree
`[MEDIUM]` `#traversal` `#morris-traversal` `#inorder` `#in-place`

#### Problem Statement
Given the root of a binary tree, return the inorder traversal of its nodes' values using Morris Traversal, which uses O(1) extra space.

#### Implementation Overview
The Morris Inorder Traversal is the canonical version of this algorithm.
1.  Initialize `current = root`.
2.  While `current` is not null:
    a. If `current` has no left child, visit it (`result.append(current.val)`) and move right (`current = current.right`).
    b. If `current` has a left child:
        i. Find the inorder predecessor.
        ii. **If no thread exists** (`predecessor.right` is null):
            - Create the thread: `predecessor.right = current`.
            - Move left: `current = current.left`.
        iii. **If a thread already exists** (`predecessor.right == current`):
            - This means we have finished the left subtree.
            - **Visit the current node**.
            - Remove the thread: `predecessor.right = None`.
            - Move right: `current = current.right`.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(1)$.

#### Python Code Snippet
```python
def inorder_morris_traversal(root: TreeNode) -> list[int]:
    result = []
    current = root
    while current:
        if not current.left:
            result.append(current.val)
            current = current.right
        else:
            predecessor = current.left
            while predecessor.right and predecessor.right != current:
                predecessor = predecessor.right
            if not predecessor.right:
                predecessor.right = current
                current = current.left
            else:
                predecessor.right = None # Remove thread
                result.append(current.val) # Visit node
                current = current.right
    return result
```

#### Tricks/Gotchas
- **Thread Removal:** It is absolutely crucial to remove the thread (`predecessor.right = None`) after using it. Forgetting this will leave the tree in a modified state with cycles.
- **Postorder Traversal:** A Morris Postorder traversal also exists but is significantly more complex. It involves creating the threads like an inorder traversal, but upon returning via a thread, it requires traversing the path from the left child to the predecessor again *in reverse* to add the nodes to the result. It's rarely asked in interviews due to its complexity.
- **Complexity:** While the space complexity is O(1), the time complexity is still O(N). Although some edges are traversed multiple times, it can be shown that the total number of operations is still proportional to N.
