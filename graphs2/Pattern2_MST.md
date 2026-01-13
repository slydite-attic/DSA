# Pattern 2: Minimum Spanning Tree (MST)

A **Spanning Tree** of a connected, undirected graph is a subgraph that connects all the vertices together with the minimum possible number of edges (`V-1`), without forming a cycle. Think of it as the "skeleton" of the graph.

A **Minimum Spanning Tree (MST)** is a spanning tree for a *weighted* graph that has the minimum possible total edge weight. It represents the "cheapest" possible way to connect all vertices. For example, finding the cheapest way to lay cable to connect a set of cities.

There are two famous greedy algorithms for finding the MST: **Prim's Algorithm** and **Kruskal's Algorithm**.

---

### 1. Prim's Algorithm
- **Core Idea**: Grows a single tree from an arbitrary starting vertex. At each step, it greedily adds the cheapest edge that connects a vertex *in the growing tree* to a vertex *outside* the tree.
- **Analogy**: Start with one city. Find the cheapest road that connects your city to a new city. Now you have two cities. Find the cheapest road connecting *either* of your two cities to a new, unconnected city. Repeat until all cities are connected.
- **Best For**: Dense graphs, or when the graph is represented by an adjacency list.

#### Implementation
Prim's is very similar to Dijkstra's algorithm. It uses a priority queue to efficiently find the next cheapest edge to an unvisited node.
1.  **Initialize**:
    -   A `visited` array to track vertices already in the MST.
    -   A min-priority queue to store `(weight, vertex)` tuples, prioritized by `weight`.
    -   `mst_weight = 0`.
2.  **Start**: Pick an arbitrary starting vertex `s` (e.g., 0). Push `(0, s)` to the priority queue.
3.  **Loop**: While the priority queue is not empty:
    a. Pop the edge with the minimum weight `(w, u)` from the PQ.
    b. If vertex `u` has already been visited, skip it (this prevents cycles).
    c. Mark `u` as visited and add its edge weight `w` to `mst_weight`.
    d. For each neighbor `v` of `u`, if `v` is not yet visited, push the edge `(edge_weight, v)` to the priority queue.
4.  The loop ends when all reachable vertices have been visited.

#### Time and Space Complexity
- **Time Complexity:** $O(E \log V)$ with a priority queue.
- **Space Complexity:** $O(V + E)$ for the adjacency list and priority queue.

#### Python Code Snippet
```python
import heapq

def prims_algorithm(adj: list[list[tuple[int, int]]], V: int) -> int:
    """
    Calculates the weight of the MST using Prim's algorithm.
    adj is an adjacency list: adj[u] = [(v, weight), ...]
    V is the number of vertices.
    """
    # The priority queue stores (weight, vertex)
    # We don't need to store the parent, as we only need the total weight.
    pq = [(0, 0)]  # Start with vertex 0 with a weight of 0
    visited = [False] * V
    mst_weight = 0

    while pq:
        weight, u = heapq.heappop(pq)

        # If the node is already visited, this edge would form a cycle
        if visited[u]:
            continue

        # Include the new vertex in the MST
        visited[u] = True
        mst_weight += weight

        # Add all adjacent edges of the new vertex to the PQ
        for v, edge_weight in adj[u]:
            if not visited[v]:
                heapq.heappush(pq, (edge_weight, v))

    return mst_weight
```

---

### 2. Kruskal's Algorithm
- **Core Idea**: Builds a "forest" of trees that gradually merge. It considers all edges in the graph, from cheapest to most expensive, and adds an edge to the MST if and only if it does not form a cycle with the edges already added.
- **Analogy**: Look at a list of all possible roads between cities, sorted by cost. Start building the cheapest roads first. Only skip building a road if it would create a redundant loop between cities that are already connected.
- **Best For**: Sparse graphs, or when the graph is just given as a list of edges.

#### Implementation
Kruskal's algorithm relies on an efficient way to check if adding an edge will form a cycle. This is the perfect use case for a **Disjoint Set Union (DSU)** data structure (also known as Union-Find).
1.  **Initialize**:
    -   Create a list of all edges in the graph as `(weight, u, v)` tuples.
    -   **Sort all edges** by weight in non-decreasing order.
    -   Initialize a DSU structure where each of the `V` vertices is in its own set.
    -   `mst_weight = 0`.
2.  **Loop**: Iterate through the sorted edges `(w, u, v)`:
    a. Check if vertices `u` and `v` are already in the same component using `dsu.find(u) != dsu.find(v)`.
    b. If they are in different components, the edge will not form a cycle.
        - Add the edge to the MST by adding its weight `w` to `mst_weight`.
        - **Merge** the two components using `dsu.union(u, v)`.
3.  Stop when `V-1` edges have been added or all edges have been considered.

#### Time and Space Complexity
- **Time Complexity:** $O(E \log E)$ due to sorting the edges. The DSU operations are nearly constant time on average ($O(\alpha(V))$).
- **Space Complexity:** $O(V)$ for the DSU data structure.

#### Python Code Snippet (with DSU)
```python
class DSU:
    """Disjoint Set Union data structure with Path Compression and Union by Size."""
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, i):
        # Path compression
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            # Union by size
            if self.size[root_i] < self.size[root_j]:
                root_i, root_j = root_j, root_i
            self.parent[root_j] = root_i
            self.size[root_i] += self.size[root_j]
            return True # Union was performed
        return False # Already in the same set

def kruskals_algorithm(edges: list[tuple[int, int, int]], V: int) -> int:
    """
    Calculates the weight of the MST using Kruskal's algorithm.
    edges is a list of (u, v, weight) tuples.
    """
    # Sort all edges by weight
    edges.sort(key=lambda item: item[2])

    dsu = DSU(V)
    mst_weight = 0
    edges_count = 0

    for u, v, weight in edges:
        # If u and v are not already connected (i.e., adding this edge won't form a cycle)
        if dsu.find(u) != dsu.find(v):
            dsu.union(u, v)
            mst_weight += weight
            edges_count += 1
            # Stop if we have V-1 edges in the MST
            if edges_count == V - 1:
                break

    return mst_weight
```
