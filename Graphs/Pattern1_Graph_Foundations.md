# Pattern 1: Graph Foundations & Core Traversal Algorithms

This pattern covers the absolute fundamentals of graph theory. Before solving any problem, it's essential to understand what a graph is, its types, how to represent it in code, and the two primary methods for exploring it: Breadth-First Search (BFS) and Depth-First Search (DFS).

---

### 1. Graph and Types
`[EASY]` `[FUNDAMENTAL]` `#theory`

#### Description
A graph is a non-linear data structure consisting of **nodes** (or **vertices**) and **edges**. The edges connect pairs of nodes.

**Key Types of Graphs:**
1.  **Undirected Graph:** Edges have no orientation. An edge `(u, v)` is the same as `(v, u)`. Think of a two-way street.
2.  **Directed Graph (Digraph):** Edges have a direction. An edge `(u, v)` goes from `u` to `v`, but not necessarily the other way. Think of a one-way street.
3.  **Weighted Graph:** Each edge has a numerical weight or cost associated with it. This is used to represent concepts like distance, time, or cost.
4.  **Unweighted Graph:** Edges have no weight.
5.  **Cyclic Graph:** Contains at least one path that starts and ends at the same vertex.
6.  **Acyclic Graph:** Contains no cycles. A directed acyclic graph is called a **DAG**.

---

### 2. Graph Representation
`[EASY]` `[FUNDAMENTAL]` `#implementation`

#### Overview
How we store a graph in memory is crucial for performance. The two most common methods are the Adjacency Matrix and the Adjacency List.

1.  **Adjacency Matrix:**
    - A 2D array of size `V x V` where `V` is the number of vertices.
    - `matrix[i][j] = 1` (or a weight) if there is an edge from vertex `i` to `j`. Otherwise, `0`.
    - **Pros:** Fast to check for an edge between two vertices (O(1)).
    - **Cons:** Uses O(V^2) space, which is inefficient for **sparse graphs**.

2.  **Adjacency List:**
    - An array of lists. The size of the array is `V`.
    - `adj[i]` contains a list of all vertices that are adjacent to vertex `i`.
    - **Pros:** Space-efficient for sparse graphs (O(V + E)). Easy to iterate over all neighbors.
    - **Cons:** Slower to check for a specific edge `(u, v)` (O(degree(u))).

**Adjacency List is the most common representation in interviews.**

#### Python Code Snippet (Adjacency List)
```python
from collections import defaultdict

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        # Using a defaultdict to represent the adjacency list
        self.adj = defaultdict(list)

    # For an undirected graph
    def add_edge(self, u, v):
        self.adj[u].append(v)
        self.adj[v].append(u)

    # For a directed graph
    def add_edge_directed(self, u, v):
        self.adj[u].append(v)
```
#### Time and Space Complexity
- **Space Complexity:** $O(V + E)$ to store the vertices and edges.
- **Time Complexity:** $O(1)$ to add an edge.

---

### 3. Breadth-First Search (BFS)
`[MEDIUM]` `[FUNDAMENTAL]` `#traversal` `#queue`

#### Problem Statement
Given a graph and a starting vertex, traverse the graph level by level from the starting vertex. Return a list of all vertices in the order they were visited.

*Example:* A graph with edges `(0,1), (0,2), (1,2), (2,3)`. Start at vertex 0.
**Output:** `[0, 1, 2, 3]`

#### Implementation Overview
BFS explores a graph level by level, using a **queue** to manage the order of nodes to visit. It's ideal for finding the shortest path in an unweighted graph.
1.  Create a `visited` array/set to avoid cycles.
2.  Create a queue and add the starting `source` vertex. Mark `source` as visited.
3.  While the queue is not empty:
    - Dequeue a vertex `u`. Add it to the result list.
    - For every neighbor `v` of `u`:
        - If `v` has not been visited, mark it as visited and enqueue it.

#### Python Code Snippet
```python
from collections import deque
def bfs_traversal(adj: dict, start_node: int, num_nodes: int) -> list[int]:
    visited = [False] * num_nodes
    q = deque([start_node])
    visited[start_node] = True
    traversal_order = []

    while q:
        u = q.popleft()
        traversal_order.append(u)

        for v in adj.get(u, []):
            if not visited[v]:
                visited[v] = True
                q.append(v)

    return traversal_order
```
#### Time and Space Complexity
- **Time Complexity:** $O(V + E)$, where $V$ is the number of vertices and $E$ is the number of edges. We visit every vertex and edge at most once.
- **Space Complexity:** $O(V)$ for the queue and visited array.

---

### 4. Depth-First Search (DFS)
`[MEDIUM]` `[FUNDAMENTAL]` `#traversal` `#stack` `#recursion`

#### Problem Statement
Given a graph and a starting vertex, traverse the graph by exploring as far as possible along each branch before backtracking. Return a list of all vertices in the order they were visited.

*Example:* A graph with edges `(0,1), (0,2), (1,2), (2,3)`. Start at vertex 0.
**Output:** `[0, 1, 2, 3]`

#### Implementation Overview
DFS is typically implemented with **recursion** (which uses the call stack).
1.  Create a `visited` array/set.
2.  Define a recursive function `dfs(u, visited, result)`:
    - Mark the current vertex `u` as visited and add it to the `result`.
    - For every neighbor `v` of `u`:
        - If `v` has not been visited, recursively call `dfs(v, ...)`.

#### Python Code Snippet
```python
def dfs_traversal(adj: dict, start_node: int, num_nodes: int) -> list[int]:
    visited = [False] * num_nodes
    traversal_order = []

    def dfs(u):
        visited[u] = True
        traversal_order.append(u)
        for v in adj.get(u, []):
            if not visited[v]:
                dfs(v)

    dfs(start_node)
    return traversal_order
```
#### Time and Space Complexity
- **Time Complexity:** $O(V + E)$, as we visit every vertex and traverse every edge once.
- **Space Complexity:** $O(V)$ for the recursion stack and visited array.

---

### 5. Number of Connected Components
`[MEDIUM]` `#traversal` `#bfs` `#dfs`

#### Problem Statement
Given an undirected graph, find and count the number of disconnected subgraphs (components).

*Example:* `V = 5`, `edges = [[0,1], [1,2], [3,4]]`. **Output:** `2`.

#### Implementation Overview
This is a direct application of BFS or DFS to count the number of times we have to start a new traversal.
1.  Initialize a `visited` array of size `V` to all `false`.
2.  Initialize a `component_count` to 0.
3.  Iterate through all vertices from `i = 0` to `V-1`:
    - If `visited[i]` is `false`:
        - This means we've found a new, unvisited component.
        - Increment `component_count`.
        - Start a traversal (either BFS or DFS) from vertex `i`. The traversal will automatically visit every node in the current component and mark them as visited.
4.  The final `component_count` is the answer.

#### Python Code Snippet
```python
def count_components(n: int, edges: list[list[int]]) -> int:
    adj = {i: [] for i in range(n)}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    visited = [False] * n
    component_count = 0

    def dfs(u):
        visited[u] = True
        for v in adj[u]:
            if not visited[v]:
                dfs(v)

    for i in range(n):
        if not visited[i]:
            component_count += 1
            dfs(i)

    return component_count
```
#### Time and Space Complexity
- **Time Complexity:** $O(V + E)$, as we iterate over all nodes and edges to build the graph and traverse it.
- **Space Complexity:** $O(V + E)$ for the adjacency list and $O(V)$ for the recursion stack and visited array.
