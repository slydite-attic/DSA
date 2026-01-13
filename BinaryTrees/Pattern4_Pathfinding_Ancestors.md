# Pattern 4: Pathfinding & Ancestors

This pattern deals with problems that require finding a path between nodes, identifying common ancestors (like the Lowest Common Ancestor), or finding nodes based on their relationship or distance to another node. These solutions often involve a traversal to find the target node(s) and then another mechanism (like backtracking or a parent-pointer map) to solve the actual problem.

---

### 1. Root to Node Path in Binary Tree
`[MEDIUM]` `#recursion` `#pathfinding` `#backtracking`

#### Problem Statement
Given the root of a binary tree and an integer `B`, find and return the path from the root to the node with value `B`. If no such node exists, return an empty path.

**Example:**
Input: `B = 5` in tree `[1,2,3,4,5,6,7]`
```
      1
     / \
    2   3
   / \ / \
  4  5 6  7
```
Output: `[1, 2, 5]`

#### Implementation Overview
This is a classic backtracking problem that can be solved with a recursive DFS. We need a function that not only traverses the tree but also keeps track of the path taken so far.

1.  Create a recursive helper function `getPath(node, target, current_path)`. This function will return `True` if the `target` is found in the subtree rooted at `node`, and `False` otherwise.
2.  **Base Case:** If `node` is null, the target cannot be here. Return `False`.
3.  **Add to Path:** Add the current `node.val` to the `current_path`.
4.  **Check for Target:** If `node.val` equals `target`, we have found the path. Return `True`.
5.  **Recurse:**
    a. Call `getPath(node.left, target, current_path)`. If it returns `True`, it means the path was found in the left subtree, so we propagate `True` up.
    b. If not found in the left subtree, call `getPath(node.right, target, current_path)`. If it returns `True`, propagate `True` up.
6.  **Backtrack:** If the target was not found in either the left or right subtree of the current node, it means this node is not on the correct path. We must remove it from `current_path` before returning. This is the backtracking step. Return `False`.

The main function will initialize an empty list and call the helper. The list will contain the correct path after the call.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the number of nodes. We might visit every node in the worst case.
- **Space Complexity:** $O(H)$, where $H$ is the height of the tree, for the recursion stack and the path list.

#### Python Code Snippet
```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from typing import List

class Solution:
    def solve(self, root: TreeNode, B: int) -> List[int]:
        path = []
        self.getPath(root, B, path)
        return path

    def getPath(self, node: TreeNode, target: int, path: List[int]) -> bool:
        # Base case: node is null
        if not node:
            return False

        # Add current node to the path
        path.append(node.val)

        # If we found the target, we are done with this path
        if node.val == target:
            return True

        # Recurse on left or right subtree
        if self.getPath(node.left, target, path) or self.getPath(node.right, target, path):
            return True

        # If target not found in either subtree, this node is not on the path. Backtrack.
        path.pop()
        return False
```

#### Tricks/Gotchas
- The backtracking step (`path.pop()`) is the most crucial part of the algorithm. Without it, the `path` list would contain nodes from incorrect branches.
- The function's boolean return value is essential for signaling when to stop and when to backtrack.
- This approach finds only one path. If multiple nodes could have the target value, it would find the first one encountered in a preorder traversal.

#### Related Problems
- `[Pattern 4]` LCA in Binary Tree (can use this as a first step).

---

### 2. LCA in Binary Tree
`[MEDIUM]` `#recursion` `#lca`

#### Problem Statement
Given a binary tree, find the lowest common ancestor (LCA) of two given nodes in the tree. The lowest common ancestor is defined between two nodes `p` and `q` as the lowest node in the tree that has both `p` and `q` as descendants (where we allow a node to be a descendant of itself).

**Example:**
Input: `root = [3,5,1,6,2,0,8,null,null,7,4]`, `p = 5`, `q = 1`
Output: `3` (Node 3 is the LCA of nodes 5 and 1).

#### Implementation Overview
The classic recursive solution is extremely elegant. The function `lca(node, p, q)` has a clear purpose:
- It returns the LCA if it's found in the subtree of `node`.
- It returns one of `p` or `q` if that node is found.
- It returns `null` if neither is found.

**Algorithm:**
1.  **Base Case:** If the current `node` is `null`, or if its value matches `p` or `q`, we have found a potential ancestor or one of the nodes itself. Return `node`.
2.  **Recursive Step:**
    a. Recursively search for the LCA in the left subtree: `left_lca = lca(node.left, p, q)`.
    b. Recursively search for the LCA in the right subtree: `right_lca = lca(node.right, p, q)`.
3.  **Combine Results:**
    a. If `left_lca` and `right_lca` are **both non-null**, it means `p` was found in one subtree and `q` in the other. Therefore, the current `node` is their lowest common ancestor. Return `node`.
    b. If only one of them is non-null (e.g., `left_lca`), it means both `p` and `q` were found in the left subtree, and `left_lca` is already their LCA. Propagate this result up by returning `left_lca`. The same logic applies if only `right_lca` is non-null.
    c. If both are `null`, neither `p` nor `q` was found in this subtree. Return `null`.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the number of nodes. We visit each node once.
- **Space Complexity:** $O(H)$, where $H$ is the height of the tree, due to recursion stack depth.

#### Python Code Snippet
```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        # Base case: if we find p, q, or hit a null node
        if not root or root == p or root == q:
            return root

        # Search in left and right subtrees
        left_lca = self.lowestCommonAncestor(root.left, p, q)
        right_lca = self.lowestCommonAncestor(root.right, p, q)

        # If both subtrees returned a non-null value, this means
        # p and q were found on different sides, so this root is the LCA.
        if left_lca and right_lca:
            return root

        # Otherwise, the LCA (or p/q) must be in one of the subtrees.
        # If one is null, this returns the other. If both are null, it returns null.
        return left_lca or right_lca
```

#### Tricks/Gotchas
- This solution beautifully handles the case where one node is an ancestor of the other. For example, if `p` is an ancestor of `q`, the search will find `p` first and return it. The recursive calls starting from `p`'s other branches will return `null`, so `p` will be correctly propagated up as the LCA.
- The logic relies on the function returning a meaningful value (`p`, `q`, the LCA, or `null`) at every step.

#### Related Problems
- `[Pattern 4]` Root to Node Path (An alternative, less efficient approach is to find the path to `p` and `q` and then find the last common node in the two paths).
- Lowest Common Ancestor of a Binary Search Tree (a simpler version with the BST property).

---

### 3. Print all the Nodes at a distance of K in a Binary Tree
`[MEDIUM]` `#traversal` `#pathfinding` `#distance-k`

#### Problem Statement
Given the `root` of a binary tree, a `target` node, and an integer `k`, return a list of the values of all nodes that have a distance `k` from the `target` node.

**Example:**
Input: `root = [3,5,1,6,2,0,8,null,null,7,4]`, `target = 5`, `k = 2`
Output: `[7, 4, 1]`

#### Implementation Overview
To solve this, we need to find nodes that are `k` distance away, which can be in three directions from the target:
1.  Downwards in the target's own subtree.
2.  Upwards towards the root.
3.  Downwards into other subtrees (via an ancestor).

The most common approach is to convert the tree into a graph-like structure so we can traverse in any direction. We can do this by creating a map of parent pointers.

1.  **Annotate Parents:** Perform a traversal (like BFS or DFS) to create a hash map `parent_map` where `parent_map[child] = parent`.
2.  **BFS from Target:** Once we have the parent pointers, we can treat the tree as a graph and perform a standard Breadth-First Search (BFS) starting from the `target` node.
3.  Initialize a queue with `(target, 0)` representing `(node, distance)` and a `visited` set to avoid cycles.
4.  Loop while the queue is not empty.
    a. Dequeue a `(node, distance)` pair.
    b. If `distance == k`, we have found a valid node. Add its value to our result list.
    c. Explore neighbors: For the current node's `left`, `right`, and `parent` (from the map), if the neighbor exists and has not been visited, add it to the queue with `distance + 1` and mark it as visited.
5.  After the BFS completes, the result list will contain all nodes at distance `k`.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the number of nodes. We traverse the tree once to build the parent map and once more for the BFS.
- **Space Complexity:** $O(N)$ to store the `parent_map`, `queue`, and `visited` set.

#### Python Code Snippet
```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None
import collections
from typing import List

class Solution:
    def distanceK(self, root: TreeNode, target: TreeNode, k: int) -> List[int]:
        if not root:
            return []

        # 1. Annotate parents to create a graph
        parent_map = {}
        q = collections.deque([root])
        while q:
            node = q.popleft()
            if node.left:
                parent_map[node.left] = node
                q.append(node.left)
            if node.right:
                parent_map[node.right] = node
                q.append(node.right)

        # 2. BFS from target
        queue = collections.deque([(target, 0)]) # (node, distance)
        visited = {target}
        result = []

        while queue:
            node, distance = queue.popleft()

            if distance == k:
                result.append(node.val)

            if distance > k: # Optimization
                continue

            # Add neighbors (children and parent) to the queue
            for neighbor in [node.left, node.right, parent_map.get(node)]:
                if neighbor and neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, distance + 1))

        return result
```

#### Tricks/Gotchas
- The key is to realize this is a graph problem on a tree structure. The parent pointers are what turn the directed tree into an undirected graph, allowing upward traversal.
- A `visited` set is crucial to prevent infinite loops (e.g., going from a child to a parent and immediately back to the child).
- The BFS approach naturally finds nodes in layers of distance, making it a perfect fit for this problem.

#### Related Problems
- `[Pattern 4]` Minimum time taken to BURN the Binary Tree from a Node (uses a very similar pattern).

---

### 4. Minimum time taken to BURN the Binary Tree from a Node
`[HARD]` `#traversal` `#bfs` `#burn-tree`

#### Problem Statement
You are given the root of a binary tree and an integer `start` representing the value of a node where a fire starts. At each time step, the fire spreads from a burning node to all its adjacent unburnt nodes. Return the minimum time required for the entire tree to burn.

**Example:**
Input: `root = [1,5,3,null,4,10,6]`, `start = 3`
Output: `4`

#### Implementation Overview
This problem is almost identical in structure to "Nodes at Distance K". It asks for the "maximum distance" from the `start` node to any other node in the tree, which is just the total time taken for the fire to spread everywhere.

1.  **Find the Start Node & Annotate Parents:** We need to do two things in our first traversal: find the node object that corresponds to the `start` value, and create the `parent_map` to build our graph. A single DFS or BFS can accomplish both.
2.  **BFS from Start Node:** Once we have the `start_node` and the `parent_map`, we can perform a BFS to find the time taken to burn the whole tree.
3.  Initialize a queue with the `(start_node, 0)` representing `(node, time)` and a `visited` set.
4.  Keep track of `max_time = 0`.
5.  Loop while the queue is not empty.
    a. Dequeue a `(node, time)` pair.
    b. Update `max_time = max(max_time, time)`.
    c. Explore neighbors: For the current node's `left`, `right`, and `parent`, if the neighbor exists and has not been visited, add it to the queue with `time + 1` and mark it as visited.
6.  After the BFS is complete, `max_time` will hold the time it took for the fire to reach the farthest node, which is the time for the whole tree to burn. Return `max_time`.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the number of nodes.
- **Space Complexity:** $O(N)$ to store the `parent_map`, `queue`, and `visited` set.

#### Python Code Snippet
```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
import collections
from typing import Optional

class Solution:
    def amountOfTime(self, root: Optional[TreeNode], start: int) -> int:
        if not root:
            return 0

        # 1. Annotate parents and find the start node
        parent_map = {}
        start_node = None
        q = collections.deque([root])
        while q:
            node = q.popleft()
            if node.val == start:
                start_node = node
            if node.left:
                parent_map[node.left] = node
                q.append(node.left)
            if node.right:
                parent_map[node.right] = node
                q.append(node.right)

        if not start_node:
             return 0

        # 2. BFS from the start node to find max time
        queue = collections.deque([(start_node, 0)]) # (node, time)
        visited = {start_node}
        max_time = 0

        while queue:
            node, time = queue.popleft()
            max_time = max(max_time, time)

            # Add neighbors (children and parent) to the queue
            for neighbor in [node.left, node.right, parent_map.get(node)]:
                if neighbor and neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, time + 1))

        return max_time
```

#### Tricks/Gotchas
- This problem is a great example of re-framing a question. "Minimum time to burn the whole tree" is just another way of asking "what is the maximum distance from the start node to any other node in the graph?"
- The setup (annotating parents, performing BFS) is identical to the "Nodes at Distance K" problem.

#### Related Problems
- `[Pattern 4]` Print all the Nodes at a distance of K in a Binary Tree (the basis for this problem).
