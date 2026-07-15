# Pattern 4: Topological Sort

A Topological Sort of a Directed Acyclic Graph (DAG) is a linear ordering of its vertices such that for every directed edge from vertex `u` to vertex `v`, `u` comes before `v` in the ordering. If the graph has a cycle, it does not have a topological sort. This pattern is fundamental for problems involving dependencies, scheduling, or prerequisites.

There are two main algorithms: a DFS-based approach and a BFS-based approach (Kahn's Algorithm).

---

### 1. Topological Sort (DFS-based)
`[MEDIUM]` `#dfs` `#topological-sort`

#### Problem Statement
Given a Directed Acyclic Graph (DAG) with `V` vertices and `E` edges, find any valid topological sort of the graph.

*Example:* `V = 4`, `edges = [[1,0],[2,0],[3,1],[3,2]]`. **Output:** `[3, 2, 1, 0]` or `[3, 1, 2, 0]`.

#### Implementation Overview
This approach uses DFS and a stack to record the "finish time" of each node. A node is "finished" after all its descendants have been visited.
1.  Initialize an empty `stack` and a `visited` array.
2.  Iterate through all vertices. For each unvisited vertex, call a recursive DFS helper.
3.  **`dfs(node)` function**:
    - Mark `node` as visited.
    - For each `neighbor` of `node`, if it's not visited, recursively call `dfs(neighbor)`.
    - After the recursive calls for all neighbors are complete, push the `node` onto the `stack`.
4.  The `stack`, when popped, gives the vertices in topologically sorted order.

#### Python Code Snippet
```python
def topo_sort_dfs(V: int, adj: dict) -> list[int]:
    visited = [False] * V
    stack = []

    def dfs(node):
        visited[node] = True
        for neighbor in adj.get(node, []):
            if not visited[neighbor]:
                dfs(neighbor)
        stack.append(node)

    for i in range(V):
        if not visited[i]:
            dfs(i)

    return stack[::-1] # Reverse the stack to get the correct order
```

#### Complexity Analysis
- **Time Complexity:** $O(V + E)$ where $V$ is vertices and $E$ is edges, because it is essentially a DFS traversal.
- **Space Complexity:** $O(V)$ for the stack and visited array.

---

### 2. Kahn's Algorithm (BFS-based Topological Sort)
`[MEDIUM]` `#bfs` `#topological-sort`

#### Problem Statement
Given a DAG, find a valid topological sort. This approach also naturally detects cycles.

#### Implementation Overview
Kahn's algorithm uses BFS and **in-degrees** (the number of incoming edges).
1.  **Compute In-degrees**: Create an array `in_degree` of size `V` and calculate the in-degree for every vertex by iterating through the adjacency list.
2.  **Initialize Queue**: Create a queue and add all vertices with an in-degree of `0`. These are the starting points with no prerequisites.
3.  **Process Queue**:
    - While the queue is not empty, dequeue `u`, add it to the `topo_order` list.
    - For each `neighbor` `v` of `u`, decrement its in-degree.
    - If a neighbor's in-degree becomes `0`, it means all its prerequisites are met, so enqueue it.
4.  **Cycle Detection**: If `len(topo_order) == V`, the sort is valid. Otherwise, a cycle exists.

#### Python Code Snippet
```python
from collections import deque
def topo_sort_kahns(V: int, adj: dict) -> list[int]:
    in_degree = [0] * V
    for i in range(V):
        for neighbor in adj.get(i, []):
            in_degree[neighbor] += 1

    q = deque([i for i in range(V) if in_degree[i] == 0])
    topo_order = []

    while q:
        u = q.popleft()
        topo_order.append(u)

        for v in adj.get(u, []):
            in_degree[v] -= 1
            if in_degree[v] == 0:
                q.append(v)

    if len(topo_order) == V:
        return topo_order
    else:
        return [] # Cycle detected
```

#### Complexity Analysis
- **Time Complexity:** $O(V + E)$ to compute in-degrees and traverse the graph.
- **Space Complexity:** $O(V)$ for the queue, in-degree array, and result array.

---

### 3. Course Schedule - I
`[MEDIUM]` `#topological-sort` `#cycle-detection`

#### Problem Statement
Given `numCourses` and a list of `prerequisites` `[ai, bi]` (to take `ai`, you must first take `bi`), return `true` if you can finish all courses.

*Example:* `numCourses = 2`, `prerequisites = [[1,0]]`. **Output:** `true`.

#### Implementation Overview
This is a cycle detection problem. If there is a cycle, it's impossible.
- **Graph Model**: Each course is a vertex. A prerequisite `[a, b]` is a directed edge `b -> a`.
- **Solution**: Use Kahn's algorithm. If the algorithm produces a topological sort of length `numCourses`, there was no cycle.

#### Python Code Snippet
```python
from collections import deque
def can_finish(numCourses: int, prerequisites: list[list[int]]) -> bool:
    adj = {i: [] for i in range(numCourses)}
    in_degree = [0] * numCourses
    for course, prereq in prerequisites:
        adj[prereq].append(course)
        in_degree[course] += 1

    q = deque([i for i in range(numCourses) if in_degree[i] == 0])
    count = 0
    while q:
        u = q.popleft()
        count += 1
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                q.append(v)

    return count == numCourses
```

#### Complexity Analysis
- **Time Complexity:** $O(V + E)$ where $V$ is `numCourses` and $E$ is the number of prerequisites.
- **Space Complexity:** $O(V + E)$ to store the adjacency list and $O(V)$ for the queue and in-degree array.

---

### 4. Course Schedule - II
`[MEDIUM]` `#topological-sort`

#### Problem Statement
Same as Course Schedule I, but return the ordering of courses to take. If impossible, return an empty array.

*Example:* `numCourses = 4`, `prerequisites = [[1,0],[2,0],[3,1],[3,2]]`. **Output:** `[0,1,2,3]` or `[0,2,1,3]`.

#### Implementation Overview
This is a direct application of topological sort.
- **Solution**: Perform a topological sort (Kahn's is natural here). If the sort is successful, return the ordering. Otherwise, return an empty array.

#### Python Code Snippet
```python
from collections import deque
def find_order(numCourses: int, prerequisites: list[list[int]]) -> list[int]:
    adj = {i: [] for i in range(numCourses)}
    in_degree = [0] * numCourses
    for course, prereq in prerequisites:
        adj[prereq].append(course)
        in_degree[course] += 1

    q = deque([i for i in range(numCourses) if in_degree[i] == 0])
    topo_order = []
    while q:
        u = q.popleft()
        topo_order.append(u)
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                q.append(v)

    return topo_order if len(topo_order) == numCourses else []
```

#### Complexity Analysis
- **Time Complexity:** $O(V + E)$ since we construct the graph and apply Kahn's algorithm.
- **Space Complexity:** $O(V + E)$ for the adjacency list and $O(V)$ for queue and in-degree structures.

---

### 5. Find Eventual Safe States
`[MEDIUM]` `#topological-sort` `#dfs`

#### Problem Statement
In a directed graph, a node is "safe" if every path starting from it leads to a "terminal" node (a node with no outgoing edges). Return all safe nodes, sorted.

*Example:* `graph = [[1,2],[2,3],[5],[0],[5],[],[]]`. **Output:** `[2,4,5,6]`.

#### Implementation Overview
A node is *unsafe* if it's part of a cycle or can reach a cycle.
- **Graph Reversal**: Reverse all edges. The problem becomes: find all nodes that can reach a terminal node in the original graph. In the reversed graph, original terminal nodes become new source nodes (in-degree 0).
- **Solution**: Perform a topological sort (Kahn's) on the **reversed graph**. The resulting sort gives all nodes reachable from the original terminal nodes. These are the safe nodes.

#### Python Code Snippet
```python
from collections import deque
def eventual_safe_nodes(graph: list[list[int]]) -> list[int]:
    n = len(graph)
    rev_adj = {i: [] for i in range(n)}
    out_degree = [0] * n
    for u in range(n):
        out_degree[u] = len(graph[u])
        for v in graph[u]:
            rev_adj[v].append(u)

    q = deque([i for i in range(n) if out_degree[i] == 0])
    safe_nodes = []
    while q:
        u = q.popleft()
        safe_nodes.append(u)
        for v in rev_adj[u]:
            out_degree[v] -= 1
            if out_degree[v] == 0:
                q.append(v)

    return sorted(safe_nodes)
```

#### Complexity Analysis
- **Time Complexity:** $O(V + E)$ to build the reversed graph and process it, plus $O(V \log V)$ for the final sort, making it $O(V \log V + E)$ overall.
- **Space Complexity:** $O(V + E)$ for the reversed graph and queue.

---

### 6. Alien Dictionary
`[HARD]` `#topological-sort`

#### Problem Statement
Given a list of `words` sorted lexicographically by an alien language's rules, derive the order of letters.

*Example:* `words = ["wrt","wrf","er","ett","rftt"]`. **Output:** `"wertf"`.

#### Implementation Overview
1.  **Build Graph**: Letters are vertices. Find dependencies by comparing adjacent words.
    - Compare `words[i]` and `words[i+1]`.
    - Find the first character where they differ. If `words[i] = "wrt"` and `words[i+1] = "wrf"`, then `t` must come before `f`. Add a directed edge `t -> f`.
2.  **Topological Sort**: Perform a topological sort on the graph of letter dependencies. The result is the alien alphabet.

#### Python Code Snippet
```python
from collections import deque
def alien_order(words: list[str]) -> str:
    adj = {c: set() for word in words for c in word}
    in_degree = {c: 0 for word in words for c in word}

    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i+1]
        min_len = min(len(w1), len(w2))
        # Handle invalid order like ["abc", "ab"]
        if len(w1) > len(w2) and w1[:min_len] == w2[:min_len]:
            return ""
        for j in range(min_len):
            if w1[j] != w2[j]:
                if w2[j] not in adj[w1[j]]:
                    adj[w1[j]].add(w2[j])
                    in_degree[w2[j]] += 1
                break

    q = deque([c for c in in_degree if in_degree[c] == 0])
    res = []
    while q:
        c = q.popleft()
        res.append(c)
        for neighbor in sorted(list(adj[c])): # sorted for deterministic output
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                q.append(neighbor)

    return "".join(res) if len(res) == len(in_degree) else ""
```

#### Complexity Analysis
- **Time Complexity:** $O(C)$ where $C$ is the total length of all words in the input array. We compare adjacent words. The BFS takes $O(U + \min(U^2, E))$ where $U$ is the number of unique characters.
- **Space Complexity:** $O(U + \min(U^2, E))$ for the adjacency list and queue.

---

### 7. Topo Sort
`[FUNDAMENTAL]` `[MEDIUM]` `#toposort` `#dag`

#### Problem Statement
Given a Directed Acyclic Graph (DAG) with V vertices and E edges, find any Topological Sort of that graph.

#### Implementation Overview
We can implement this using Kahn's Algorithm (BFS). We first compute the in-degrees of all vertices. We push all vertices with an in-degree of 0 into a queue. Then, we process the queue by appending the current vertex to the answer and decrementing the in-degree of its neighbors. If a neighbor's in-degree becomes 0, it's added to the queue.

#### Python Code Snippet
```python
from collections import deque

def topoSort(V: int, adj: list[list[int]]) -> list[int]:
    in_degree = [0] * V
    for u in range(V):
        for v in adj[u]:
            in_degree[v] += 1

    q = deque()
    for i in range(V):
        if in_degree[i] == 0:
            q.append(i)

    topo_order = []
    while q:
        node = q.popleft()
        topo_order.append(node)

        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                q.append(neighbor)

    return topo_order
```

#### Complexity Analysis
- **Time Complexity:** $O(V + E)$ where $V$ is vertices and $E$ is edges.
- **Space Complexity:** $O(V)$ for the queue and the in-degree array.

---

### 8. Detect a cycle in a directed graph
`[MEDIUM]` `#bfs` `#cycle-detection` `#toposort`

#### Problem Statement
Given a Directed Graph with V vertices and E edges, check whether it contains any cycle or not.

#### Implementation Overview
We can use Kahn's Algorithm (BFS based Topological Sort). A topological sort is only possible for a Directed Acyclic Graph (DAG). If we attempt Kahn's algorithm and the resulting topological sort does not contain all $V$ vertices, it means there is a cycle in the graph. We just keep a count of processed nodes, and if `count != V`, a cycle exists.

#### Python Code Snippet
```python
from collections import deque

def isCyclic(V: int, adj: list[list[int]]) -> bool:
    in_degree = [0] * V
    for u in range(V):
        for v in adj[u]:
            in_degree[v] += 1

    q = deque()
    for i in range(V):
        if in_degree[i] == 0:
            q.append(i)

    count = 0
    while q:
        node = q.popleft()
        count += 1

        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                q.append(neighbor)

    return count != V
```

#### Complexity Analysis
- **Time Complexity:** $O(V + E)$ where $V$ is vertices and $E$ is edges.
- **Space Complexity:** $O(V)$ for the queue and the in-degree array.
