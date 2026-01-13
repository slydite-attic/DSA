# Pattern 2: Tree Views & Boundary Traversals

This pattern groups problems that require viewing or traversing the binary tree in a specific, non-standard order. These problems often build upon foundational traversals (like Level-order) but add extra logic to track coordinates, levels, or boundaries.

---

### 1. Zig Zag Traversal of Binary Tree
`[EASY]` `#traversal` `#level-order` `#bfs` `#queue` `#deque`

#### Problem Statement
Given the root of a binary tree, return the zigzag level order traversal of its nodes' values. This means for the first level, the order is left-to-right, for the second level it's right-to-left, and so on, alternating between levels.

**Example:**
Input: `root = [3,9,20,null,null,15,7]`
```
    3
   / \
  9  20
    /  \
   15   7
```
Output: `[[3],[20,9],[15,7]]`

#### Implementation Overview
This is a modification of the standard Level Order Traversal. We use a queue for BFS, but we need to handle the alternating traversal direction for each level.

1.  Initialize a `result` list, a `queue` with the root, and a `left_to_right` boolean flag, initially `True`.
2.  Loop while the queue is not empty.
3.  Get the `level_size` to know how many nodes are on the current level.
4.  Initialize a `current_level` list (or a `deque` for efficient appends at both ends).
5.  Loop `level_size` times:
    a. Dequeue a `node`.
    b. Based on the `left_to_right` flag, either append the node's value to the end of `current_level` (for left-to-right) or append it to the beginning (for right-to-left).
    c. Enqueue the node's children (`left` then `right`) as usual.
6.  After the inner loop, add the `current_level` to the `result`.
7.  **Flip the flag:** `left_to_right = not left_to_right`.
8.  Return the `result`.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the number of nodes. Each node is processed once.
- **Space Complexity:** $O(W)$, where $W$ is the max width of the tree, for the queue and `current_level` deque.

#### Python Code Snippet
```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from typing import List, Optional
import collections

class Solution:
    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []

        result = []
        queue = collections.deque([root])
        left_to_right = True

        while queue:
            level_size = len(queue)
            # Using a deque for efficient appends to both ends
            current_level = collections.deque()

            for _ in range(level_size):
                node = queue.popleft()

                if left_to_right:
                    current_level.append(node.val)
                else:
                    current_level.appendleft(node.val)

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            result.append(list(current_level))
            left_to_right = not left_to_right # Flip direction for the next level

        return result
```

#### Tricks/Gotchas
- The core logic is standard level order traversal. The main trick is how to handle the reversal. Using a `deque` for `current_level` and `appendleft()` is a clean and efficient way to do this.
- Another common approach is to collect the level's values in a normal list and then reverse it if `left_to_right` is false. This can be slightly less efficient for very wide trees but is often more intuitive.
- Forgetting to flip the `left_to_right` boolean after each level is a common bug.

#### Related Problems
- `[Pattern 1]` Level Order Traversal (the basis for this problem).
- `[Pattern 2]` Binary Tree Right Side View (another level-order variant).

---

### 7. Maximum Width of Binary Tree
`[MEDIUM]` `#traversal` `#level-order` `#bfs`

#### Problem Statement
Given the root of a binary tree, return the maximum width of the tree. The width of one level is defined as the length between the end-nodes (the leftmost and rightmost non-null nodes), where the null nodes between the end-nodes that would be present in a complete binary tree are also counted into the length calculation.

**Example:**
Input: `root = [1,3,2,5,3,null,9]`
```
      1
     / \
    3   2
   / \   \
  5   3   9
```
Output: `4` (The maximum width is at level 3, between nodes 5 and 9, with nodes (5,6,7,8) giving a width of 4).

#### Implementation Overview
This problem is solved using a level-order traversal (BFS). The key is to assign an index to each node as if it were in a complete binary tree.
- If a node has index `i`, its left child will have index `2*i + 1` and its right child will have index `2*i + 2`.
- For each level, the width is `(index of rightmost node) - (index of leftmost node) + 1`. We track the maximum width found across all levels.

**Algorithm:**
1.  Initialize `max_width = 0` and a queue for BFS.
2.  The queue will store `(node, index)` pairs. Add `(root, 0)` to the queue.
3.  In each level of the BFS:
    a. Get the `level_size`.
    b. Record the index of the first node in the level (`level_start_index`).
    c. Loop `level_size` times, dequeueing `(node, index)`.
    d. The `index` of the last node in the level will be our `level_end_index`.
    e. Enqueue the children with their calculated indices: `(node.left, 2*index + 1)` and `(node.right, 2*index + 2)`.
    f. After the level is processed, calculate the width: `max_width = max(max_width, level_end_index - level_start_index + 1)`.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the number of nodes.
- **Space Complexity:** $O(W)$, where $W$ is the maximum width of the tree, for the queue.

#### Python Code Snippet
```python
from collections import deque

class Solution:
    def widthOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0

        max_width = 0
        queue = deque([(root, 0)]) # (node, index)

        while queue:
            level_size = len(queue)
            # Get the index of the first node at this level
            level_start_index = queue[0][1]

            for i in range(level_size):
                node, index = queue.popleft()

                # The index of the last node at this level
                if i == level_size - 1:
                    level_end_index = index

                if node.left:
                    queue.append((node.left, 2 * index + 1))
                if node.right:
                    queue.append((node.right, 2 * index + 2))

            max_width = max(max_width, level_end_index - level_start_index + 1)

        return max_width
```

#### Tricks/Gotchas
- **Index Normalization:** The indices can become very large. A common optimization is to normalize them at each level by subtracting the `level_start_index`. The new index for a node would be `index - level_start_index`, and its children would be `2 * (index - level_start_index) + 1` and `+ 2`. This keeps the numbers smaller.

---

### 2. Boundary Traversal of Binary Tree
`[MEDIUM]` `#traversal` `#boundary`

#### Problem Statement
Given a binary tree, return its boundary traversal in an anti-clockwise direction. The traversal should consist of the left boundary (top-down), all leaf nodes (left-to-right), and the right boundary (bottom-up).

**Example:**
Input:
```
      1
     / \
    2   3
   / \ / \
  4  5 6  7
```
Output: `[1, 2, 4, 5, 6, 7, 3]`
Left Boundary: `1, 2`
Leaves: `4, 5, 6, 7`
Right Boundary (reversed): `3`

#### Implementation Overview
This problem is solved by breaking it down into three distinct parts and combining the results, being careful to avoid duplicates.

1.  **Add the Left Boundary:** Traverse down the left side of the tree. Add each node's value to the result as long as it is **not a leaf node**. Prioritize going left; if a left child doesn't exist, move to the right child.
2.  **Add the Leaf Nodes:** Perform a standard traversal (like preorder) on the entire tree. Inside the traversal, if a node is a leaf (i.e., it has no left and no right child), add its value to the result.
3.  **Add the Right Boundary (in reverse):** Traverse down the right side of the tree. Store the node values in a temporary list. After the traversal is complete, add the values from the temporary list to the result in reverse order. Again, only add nodes that are **not leaves**.

The root is handled as part of the initial call.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, as we visit each node a constant number of times (at most 3 times, once for each phase).
- **Space Complexity:** $O(H)$ for the recursion stack during leaf traversal and to store the right boundary before reversing. $H$ is the height of the tree.

#### Python Code Snippet
```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from typing import List

def is_leaf(node):
    return not node.left and not node.right

class Solution:
    def boundaryOfBinaryTree(self, root: TreeNode) -> List[int]:
        if not root:
            return []

        result = []
        if not is_leaf(root):
            result.append(root.val)

        # 1. Add left boundary (excluding leaves)
        curr = root.left
        while curr:
            if not is_leaf(curr):
                result.append(curr.val)
            if curr.left:
                curr = curr.left
            else:
                curr = curr.right

        # 2. Add all leaf nodes
        def add_leaves(node):
            if not node:
                return
            if is_leaf(node):
                result.append(node.val)
            add_leaves(node.left)
            add_leaves(node.right)

        # We start the leaf traversal from the root to get all leaves
        add_leaves(root)

        # 3. Add right boundary (in reverse, excluding leaves)
        right_boundary = []
        curr = root.right
        while curr:
            if not is_leaf(curr):
                right_boundary.append(curr.val)
            if curr.right:
                curr = curr.right
            else:
                curr = curr.left

        result.extend(right_boundary[::-1])

        return result
```

#### Tricks/Gotchas
- The main complexity is handling the duplicates and edge cases. The root should only be added if it's not a leaf. Leaf nodes must only be added during the dedicated leaf traversal part.
- The condition `if not is_leaf(curr):` is crucial in the left and right boundary traversals to prevent adding leaf nodes, which would cause duplicates.
- The right boundary must be collected and then reversed to achieve the anti-clockwise traversal.

#### Related Problems
- This problem combines ideas from simple traversals but requires careful case analysis. It's a unique pattern.

---

### 3. Vertical Order Traversal of Binary Tree
`[EASY]` `#traversal` `#level-order` `#coordinates` `#hashmap`

#### Problem Statement
Given the root of a binary tree, return the vertical order traversal of its nodes' values. For each vertical line (column), the nodes should be ordered from top to bottom. If two nodes are in the same row and column, they should be ordered by their value.

**Example:**
Input: `root = [3,9,20,null,null,15,7]`
```
      3 (0,0)
     / \
    9(-1,1) 20(1,1)
          /  \
         15(1,2) 7(2,2)
```
Output: `[[9],[3,15],[20],[7]]` (Note: At column 1, 15 is below 20, so it comes after)

#### Implementation Overview
This problem requires us to know the `(column, row)` coordinate of each node. We can use a traversal (BFS is natural for top-to-bottom order) to visit each node and store it in a data structure that groups nodes by their vertical column.

1.  Initialize a hash map (`vertical_map`) to store nodes, where keys are column indices and values are lists of `(row, value)` tuples.
2.  Create a queue for level-order traversal. The queue will store tuples of `(node, column, row)`.
3.  Start by pushing `(root, 0, 0)` into the queue.
4.  While the queue is not empty, dequeue an element `(node, col, row)`.
5.  Add the `(row, node.val)` tuple to the list associated with `col` in the `vertical_map`.
6.  If the node has a left child, enqueue `(node.left, col - 1, row + 1)`.
7.  If the node has a right child, enqueue `(node.right, col + 1, row + 1)`.
8.  After the traversal, the `vertical_map` contains all nodes grouped by column.
9.  Iterate through the columns of the map in sorted order.
10. For each column, sort the list of `(row, value)` tuples. This ensures top-to-bottom order, and for ties in row, it sorts by value as required.
11. Extract just the node values and build the final result.

#### Time and Space Complexity
- **Time Complexity:** $O(N \log N)$. The traversal is $O(N)$, but sorting the nodes in each column can take $O(N \log N)$ in the worst case (e.g., all nodes in one vertical line).
- **Space Complexity:** $O(N)$ to store the nodes in the map and the queue.

#### Python Code Snippet
```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from typing import List, Optional
import collections

class Solution:
    def verticalTraversal(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []

        vertical_map = collections.defaultdict(list)
        queue = collections.deque([(root, 0, 0)]) # (node, col, row)

        while queue:
            # Using BFS ensures we process top-to-bottom
            node, col, row = queue.popleft()
            vertical_map[col].append((row, node.val))

            if node.left:
                queue.append((node.left, col - 1, row + 1))
            if node.right:
                queue.append((node.right, col + 1, row + 1))

        result = []
        # Sort columns to get the final left-to-right order
        for col in sorted(vertical_map.keys()):
            # Sort by row first, then by value if rows are the same
            sorted_nodes = sorted(vertical_map[col])
            result.append([val for row, val in sorted_nodes])

        return result
```

#### Tricks/Gotchas
- The key is associating each node with its coordinates. BFS is a natural fit because it automatically visits nodes from top to bottom, level by level.
- The sorting requirement is crucial. The problem statement specifies sorting by value if coordinates are the same. Storing `(row, val)` tuples and sorting them handles this perfectly.
- Using `sorted(vertical_map.keys())` is a clean way to ensure the final result has columns in the correct left-to-right order.

#### Related Problems
- `[Pattern 2]` Top View of Binary Tree
- `[Pattern 2]` Bottom View of Binary Tree

---

### 4. Top View of Binary Tree
`[EASY]` `#traversal` `#view` `#coordinates` `#hashmap`

#### Problem Statement
Given the root of a binary tree, return the top view of its nodes' values. The top view is the set of nodes visible when the tree is viewed from the top. Nodes are ordered from left to right. If multiple nodes are in the same vertical line, only the first one encountered (the topmost one) is visible.

**Example:**
Input:
```
      1
     / \
    2   3
     \
      4
       \
        5
```
Output: `[2, 1, 3, 5]`

#### Implementation Overview
This problem is a simplification of the Vertical Order Traversal. We still need to associate nodes with their vertical column index, but we only care about the *first* node we encounter for each column. A level-order (BFS) traversal is perfect for this, as it guarantees we see top nodes before bottom nodes.

1.  Initialize a hash map (`top_view_map`) to store the first node value seen for each column index.
2.  Initialize a queue for BFS, storing tuples of `(node, column_index)`.
3.  Add `(root, 0)` to the queue.
4.  Loop while the queue is not empty:
    a. Dequeue a `(node, col)` pair.
    b. **Check the map:** If the `col` is **not** already a key in `top_view_map`, it means this is the first time we are visiting this column. Add the node's value to the map: `top_view_map[col] = node.val`.
    c. Enqueue the children: `(node.left, col - 1)` and `(node.right, col + 1)`.
5.  After the traversal, the `top_view_map` contains the top-most node for each column.
6.  Sort the map by its keys (the column indices) and extract the values to get the final left-to-right ordered result.

#### Time and Space Complexity
- **Time Complexity:** $O(N \log N)$ due to sorting the columns at the end. The traversal itself is $O(N)$.
- **Space Complexity:** $O(N)$ to store the map and the queue.

#### Python Code Snippet
```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from typing import List, Optional
import collections

class Solution:
    def topSideView(self, root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []

        top_view_map = {}
        queue = collections.deque([(root, 0)]) # (node, column)

        while queue:
            node, col = queue.popleft()

            # If this column has not been seen before, add the node
            if col not in top_view_map:
                top_view_map[col] = node.val

            if node.left:
                queue.append((node.left, col - 1))
            if node.right:
                queue.append((node.right, col + 1))

        # Sort by column index and return the values
        sorted_columns = sorted(top_view_map.keys())
        return [top_view_map[col] for col in sorted_columns]
```

#### Tricks/Gotchas
- The logic `if col not in top_view_map:` is the core of the algorithm. It leverages the top-to-bottom nature of BFS to ensure only the first-encountered node in any column is recorded.
- Unlike Vertical Order Traversal, we don't need to store row information or do complex sorting at the end; we just sort the final keys.

#### Related Problems
- `[Pattern 2]` Vertical Order Traversal (a more complex version of this problem).
- `[Pattern 2]` Bottom View of Binary Tree (a slight variation of this problem).
- `[Pattern 2]` Binary Tree Right Side View (shares the idea of "seeing" only one node per level).

---

### 5. Bottom View of Binary Tree
`[MEDIUM]` `#traversal` `#view` `#coordinates` `#hashmap`

#### Problem Statement
Given the root of a binary tree, return the bottom view of its nodes' values. The bottom view is the set of nodes visible when the tree is viewed from the bottom. Nodes are ordered from left to right. If multiple nodes are in the same vertical line, only the last one encountered is visible.

**Example:**
Input:
```
      1
     / \
    2   3
   /   /
  4   5
```
Output: `[4, 2, 5, 3]`

#### Implementation Overview
The logic is nearly identical to the Top View problem. We use a level-order (BFS) traversal to visit nodes from top to bottom. The key difference is that for any given vertical column, we want the *last* node we see, not the first.

1.  Initialize a hash map (`bottom_view_map`) to store the last node value seen for each column index.
2.  Initialize a queue for BFS, storing tuples of `(node, column_index)`.
3.  Add `(root, 0)` to the queue.
4.  Loop while the queue is not empty:
    a. Dequeue a `(node, col)` pair.
    b. **Update the map:** Unconditionally update the value for the current column with the current node's value: `bottom_view_map[col] = node.val`. Since we are traversing level by level, a later node at the same column will always be below a previous one, so simply overwriting the value works perfectly.
    c. Enqueue the children: `(node.left, col - 1)` and `(node.right, col + 1)`.
5.  After the traversal, the `bottom_view_map` contains the bottom-most node for each column.
6.  Sort the map by its keys (the column indices) and extract the values to get the final left-to-right ordered result.

#### Time and Space Complexity
- **Time Complexity:** $O(N \log N)$ due to sorting the columns at the end. The traversal itself is $O(N)$.
- **Space Complexity:** $O(N)$ to store the map and the queue.

#### Python Code Snippet
```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from typing import List, Optional
import collections

class Solution:
    def bottomView(self, root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []

        bottom_view_map = {}
        queue = collections.deque([(root, 0)]) # (node, column)

        while queue:
            node, col = queue.popleft()

            # Always update the map for the column. The last one seen wins.
            bottom_view_map[col] = node.val

            if node.left:
                queue.append((node.left, col - 1))
            if node.right:
                queue.append((node.right, col + 1))

        # Sort by column index and return the values
        sorted_columns = sorted(bottom_view_map.keys())
        return [bottom_view_map[col] for col in sorted_columns]
```

#### Tricks/Gotchas
- The only change from Top View is removing the `if col not in map` check. By always overwriting the value for a column, the last node visited in that column (which is the lowest, thanks to BFS) will be the one that remains in the map.
- This elegant solution highlights the power of choosing the right traversal (BFS) for the problem.

#### Related Problems
- `[Pattern 2]` Top View of Binary Tree (the inverse of this problem).
- `[Pattern 2]` Vertical Order Traversal (a more general version).

---

### 6. Right/Left View of Binary Tree
`[MEDIUM]` `#traversal` `#view` `#level-order`

#### Problem Statement
Given the root of a binary tree, imagine yourself standing on the right side of it. Return the values of the nodes you can see ordered from top to bottom.

**Example:**
Input: `root = [1,2,3,null,5,null,4]`
```
   1   <---
 /   \
2     3  <---
 \     \
  5     4  <---
```
Output: `[1, 3, 4]`

#### Implementation Overview
There are two common approaches: Level-Order (BFS) and Reverse Preorder (DFS).

**1. Level-Order (BFS) Approach:**
This is the most intuitive method. We perform a standard level-order traversal. For each level, the last node we process is the one visible from the right.
1.  Initialize a `result` list and a `queue` for BFS.
2.  Loop while the queue is not empty.
3.  Get the `level_size`.
4.  Loop `level_size` times:
    a. Dequeue a `node`.
    b. **Check if it's the last node:** If this is the last iteration of the inner loop (`i == level_size - 1`), it's the rightmost node. Add its value to `result`.
    c. Enqueue children as usual.
5.  Return `result`.

**2. Recursive (DFS) Approach:**
This is a clever approach that uses a reverse preorder traversal (`Root, Right, Left`). We pass the current `level` as a parameter.
1.  Initialize a `result` list.
2.  Call a recursive helper `dfs(node, level)`.
3.  Inside `dfs`:
    a. If `node` is null, return.
    b. **Check level:** If the current `level` is equal to the current size of the `result` list, it means this is the first time we are visiting this level. Since we are traversing `Root, Right, Left`, the first node we see at any level is the rightmost one. Add `node.val` to `result`.
    c. Recurse on the right child: `dfs(node.right, level + 1)`.
    d. Recurse on the left child: `dfs(node.left, level + 1)`.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the number of nodes.
- **Space Complexity:** $O(H)$ for recursion stack (DFS) or $O(W)$ for queue (BFS).

#### Python Code Snippet (Recursive DFS):
```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from typing import List, Optional

class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        result = []

        def dfs(node, level):
            if not node:
                return

            # If this level is being visited for the first time,
            # this node is the rightmost one.
            if level == len(result):
                result.append(node.val)

            # Recurse right first to ensure we process rightmost nodes first
            dfs(node.right, level + 1)
            dfs(node.left, level + 1)

        dfs(root, 0)
        return result
```

#### Tricks/Gotchas
- For the **Left Side View**, you can use the exact same recursive logic but swap the order of the recursive calls: `dfs(node.left, ...)` then `dfs(node.right, ...)`. The first node encountered at each level will now be the leftmost one.
- The condition `level == len(result)` is a clever way to track whether a node for a given level has already been added, without needing an extra set or map.

#### Related Problems
- `[Pattern 1]` Level Order Traversal (the basis for the BFS solution).
