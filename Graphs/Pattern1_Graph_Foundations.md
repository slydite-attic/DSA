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

#### Complexity Analysis
- **Time Complexity:** $O(1)$ for concepts.
- **Space Complexity:** $O(1)$ for concepts.

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

#### Complexity Analysis
- **Time Complexity:** $O(V + E)$ to build the graph.
- **Space Complexity:** $O(V + E)$ to store the adjacency list.

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

#### Complexity Analysis
- **Time Complexity:** $O(V + E)$ since every vertex and every edge is visited at most once.
- **Space Complexity:** $O(V)$ for the queue, visited array, and traversal order list.

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

#### Complexity Analysis
- **Time Complexity:** $O(V + E)$ since every vertex and every edge is visited at most once.
- **Space Complexity:** $O(V)$ for the queue, visited array, and traversal order list.

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

#### Complexity Analysis
- **Time Complexity:** $O(V + E)$ because we do a standard DFS/BFS which visits all nodes and edges.
- **Space Complexity:** $O(V + E)$ for the adjacency list and $O(V)$ for the visited array and recursion stack.

---

### 6. Traversal Techniques (BFS)
`[FUNDAMENTAL]` `[EASY]` `#traversal` `#bfs`

#### Problem Statement
Given an undirected graph. Perform a Breadth-First Search (BFS) traversal of the graph starting from vertex 0 and return a list containing the BFS traversal.

#### Implementation Overview
This problem asks for a direct implementation of BFS starting from vertex 0. We will use a queue to keep track of the nodes to be visited and a `visited` array to ensure we don't process a node more than once. We dequeue a node, add it to our result list, and enqueue all its unvisited neighbors.

#### Python Code Snippet
```python
from collections import deque

def bfsOfGraph(V: int, adj: list[list[int]]) -> list[int]:
    visited = [False] * V
    q = deque([0])
    visited[0] = True
    traversal_order = []

    while q:
        u = q.popleft()
        traversal_order.append(u)

        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                q.append(v)

    return traversal_order
```

#### Complexity Analysis
- **Time Complexity:** $O(V + E)$ where $V$ is the number of vertices and $E$ is the number of edges. We visit each node once and examine each edge.
- **Space Complexity:** $O(V)$ for the queue and visited array.

---

### 7. DFS (Depth-First Search)
`[FUNDAMENTAL]` `[EASY]` `#traversal` `#dfs`

#### Problem Statement
Given a connected undirected graph. Perform a Depth-First Search (DFS) traversal of the graph starting from vertex 0 and return a list containing the DFS traversal.

#### Implementation Overview
This requires implementing the standard DFS algorithm starting at vertex 0. We use a recursive helper function that takes the current node, marks it as visited, adds it to the result list, and recursively visits all its unvisited neighbors.

#### Python Code Snippet
```python
def dfsOfGraph(V: int, adj: list[list[int]]) -> list[int]:
    visited = [False] * V
    traversal_order = []

    def dfs(node):
        visited[node] = True
        traversal_order.append(node)

        for neighbor in adj[node]:
            if not visited[neighbor]:
                dfs(neighbor)

    dfs(0)
    return traversal_order
```

#### Complexity Analysis
- **Time Complexity:** $O(V + E)$, as we visit each node exactly once and explore all its outgoing edges.
- **Space Complexity:** $O(V)$ for the visited array and recursion stack depth in the worst case.
