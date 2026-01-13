# Pattern 4: Advanced Graph Algorithms

This pattern covers advanced algorithms for analyzing the connectivity and structure of graphs. These algorithms are typically based on nuanced applications of **Depth-First Search (DFS)** and are used to find critical connections (bridges), critical nodes (articulation points), and tightly-knit clusters (Strongly Connected Components).

---

### 1. Bridges in a Graph (Tarjan's Bridge-Finding Algorithm)
`[HARD]` `#dfs` `#bridges`

A **bridge** (or cut-edge) is an edge in a graph that, if removed, would increase the number of connected components. Finding bridges is crucial for identifying single points of failure in a network.

#### Implementation Overview
This algorithm uses a single DFS traversal. During the traversal, we track two key pieces of information for each vertex `u`:
- **Discovery Time (`disc[u]`):** The "time" (or step number) at which `u` is first visited during the DFS.
- **Low-Link Value (`low[u]`):** The lowest discovery time reachable from `u` (including itself) by traversing its DFS subtree and using at most **one back-edge** to an ancestor.

**The Bridge Condition:**
An edge `(u, v)` (where `v` is a child of `u` in the DFS tree) is a bridge if and only if `low[v] > disc[u]`.
- **Intuition**: This condition means that the earliest node the subtree at `v` can reach is `v` itself. It has no back-edges that can "escape" up to `u` or any of `u`'s ancestors. Therefore, the edge `(u, v)` is the only connection from `v`'s subtree to the rest of the graph.

#### Algorithm Steps
1.  Initialize `disc` and `low` arrays to -1, a `time` counter to 0, and a `parent` array/map.
2.  Start a DFS from an arbitrary source.
3.  Inside `dfs(u)`:
    a. Mark `u` as visited. Set `disc[u] = low[u] = time` and increment `time`.
    b. For each neighbor `v` of `u`:
        - If `v` is the direct parent of `u` in the DFS tree, ignore it.
        - If `v` is already visited (and not the parent), it's a back-edge. This means we've found a path to an ancestor. Update `low[u] = min(low[u], disc[v])`.
        - If `v` is not visited:
            - Recursively call `dfs(v)`.
            - After the recursive call returns, update `low[u] = min(low[u], low[v])`. This propagates the lowest-reachable ancestor info up the tree.
            - Check the bridge condition: If `low[v] > disc[u]`, add the edge `(u, v)` to the list of bridges.

#### Time and Space Complexity
- **Time Complexity:** $O(V + E)$, where $V$ is vertices and $E$ is edges. We perform a single DFS traversal.
- **Space Complexity:** $O(V + E)$ to build the adjacency list and $O(V)$ for the recursion stack and auxiliary arrays (`disc`, `low`, `parent`).

#### Python Code Snippet
```python
def find_bridges(n: int, connections: list[list[int]]) -> list[list[int]]:
    adj = [[] for _ in range(n)]
    for u, v in connections:
        adj[u].append(v)
        adj[v].append(u)

    disc = [-1] * n
    low = [-1] * n
    parent = [-1] * n
    bridges = []
    time = 0

    def dfs(u):
        nonlocal time
        disc[u] = low[u] = time
        time += 1

        for v in adj[u]:
            if v == parent[u]:
                continue
            if disc[v] != -1: # Visited, back-edge
                low[u] = min(low[u], disc[v])
            else: # Not visited
                parent[v] = u
                dfs(v)
                low[u] = min(low[u], low[v])
                if low[v] > disc[u]:
                    bridges.append([u, v])

    for i in range(n):
        if disc[i] == -1:
            dfs(i)

    return bridges
```

---

### 2. Articulation Points in a Graph
`[HARD]` `#dfs` `#articulation-points`

An **articulation point** (or cut vertex) is a vertex that, if removed, would increase the number of connected components. They represent critical single points of failure in a network node.

#### Implementation Overview
The algorithm is nearly identical to bridge-finding, using `disc` and `low` values. The conditions for identifying an articulation point are slightly different.

**Articulation Point Conditions:**
A vertex `u` is an articulation point if:
1.  **`u` is the root of the DFS tree and has at least two children.** The root's children's subtrees are disconnected from each other except through the root itself.
2.  **`u` is not the root**, and it has a child `v` such that `low[v] >= disc[u]`.
    - **Intuition**: This means the subtree at `v` cannot reach any ancestor of `u` via a back-edge. Its "highest" possible connection is to `u` itself. Therefore, removing `u` disconnects the subtree of `v` from the rest of the graph.

#### Time and Space Complexity
- **Time Complexity:** $O(V + E)$, as it uses a single DFS.
- **Space Complexity:** $O(V + E)$ for the adjacency list and $O(V)$ for auxiliary structures.

#### Python Code Snippet
```python
def find_articulation_points(n: int, connections: list[list[int]]) -> list[int]:
    adj = [[] for _ in range(n)]
    for u, v in connections:
        adj[u].append(v)
        adj[v].append(u)

    disc = [-1] * n
    low = [-1] * n
    parent = [-1] * n
    articulation_points = [False] * n
    time = 0

    def dfs(u):
        nonlocal time
        disc[u] = low[u] = time
        time += 1
        children = 0

        for v in adj[u]:
            if v == parent[u]:
                continue
            if disc[v] != -1:
                low[u] = min(low[u], disc[v])
            else:
                children += 1
                parent[v] = u
                dfs(v)
                low[u] = min(low[u], low[v])

                # Check for articulation point
                if parent[u] == -1 and children > 1: # Case 1: Root with >1 child
                    articulation_points[u] = True
                if parent[u] != -1 and low[v] >= disc[u]: # Case 2: Non-root
                    articulation_points[u] = True

    for i in range(n):
        if disc[i] == -1:
            dfs(i)

    return [i for i, is_ap in enumerate(articulation_points) if is_ap]
```

---

### 3. Strongly Connected Components (Kosaraju's Algorithm)
`[HARD]` `#dfs` `#kosaraju` `#scc`

In a **directed graph**, a **Strongly Connected Component (SCC)** is a maximal subgraph where for every pair of vertices `u, v` in the subgraph, there is a path from `u` to `v` and a path from `v` to `u`.

#### Implementation Overview
Kosaraju's algorithm cleverly uses two DFS passes to find all SCCs.
1.  **Step 1: First DFS (Order by Finish Time)**
    - Perform a DFS on the original graph `G`.
    - As each vertex finishes (i.e., all its descendants have been fully explored), push it onto a stack. This effectively orders the vertices by decreasing finish time, similar to a topological sort.

2.  **Step 2: Transpose the Graph**
    - Create the transpose graph `G_T` by reversing the direction of every edge in `G`.

3.  **Step 3: Second DFS (Find Components)**
    - Pop vertices one by one from the stack created in Step 1.
    - If a popped vertex `u` has not yet been visited (in this second pass), it marks the start of a new SCC.
    - Start a DFS on the **transpose graph `G_T`** from `u`. All vertices reachable from `u` in `G_T` form a single SCC. Collect them and mark them as visited.
    - Repeat until the stack is empty.

#### Time and Space Complexity
- **Time Complexity:** $O(V + E)$, as we perform DFS twice and transpose the graph once.
- **Space Complexity:** $O(V + E)$ to store the graph and its transpose, plus $O(V)$ for the stack and visited array.

#### Python Code Snippet
```python
def kosaraju_scc(n: int, adj: list[list[int]]) -> list[list[int]]:
    # Step 1: First DFS to get nodes in order of finishing time
    stack = []
    visited = [False] * n
    def dfs1(u):
        visited[u] = True
        for v in adj[u]:
            if not visited[v]:
                dfs1(v)
        stack.append(u)

    for i in range(n):
        if not visited[i]:
            dfs1(i)

    # Step 2: Transpose the graph
    adj_rev = [[] for _ in range(n)]
    for i in range(n):
        for neighbor in adj[i]:
            adj_rev[neighbor].append(i)

    # Step 3: Second DFS on the transposed graph
    scc_list = []
    visited = [False] * n
    def dfs2(u, current_scc):
        visited[u] = True
        current_scc.append(u)
        for v in adj_rev[u]:
            if not visited[v]:
                dfs2(v, current_scc)

    while stack:
        u = stack.pop()
        if not visited[u]:
            current_scc = []
            dfs2(u, current_scc)
            scc_list.append(current_scc)

    return scc_list
```
