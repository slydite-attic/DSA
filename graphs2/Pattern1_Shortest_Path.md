### `[PATTERN] Shortest Path Algorithms`

Finding the shortest path between nodes in a graph is a classic problem with several well-established solutions. The key is to choose the right algorithm based on the properties of the graph.

#### How to Choose the Right Algorithm

| Graph Type                                | Algorithm                               | Time Complexity |
| ----------------------------------------- | --------------------------------------- | --------------- |
| **Unweighted** (all edges have same weight) | Breadth-First Search (BFS)              | O(V + E)        |
| **Weighted, No Negative Edges**           | Dijkstra's Algorithm                    | O(E log V)      |
| **Weighted, Directed Acyclic (DAG)**      | Topological Sort + Path Relaxation      | O(V + E)        |
| **Weighted, Has Negative Edges**          | Bellman-Ford Algorithm                  | O(V * E)        |
| **All-Pairs Shortest Path**               | Floyd-Warshall Algorithm                | O(V^3)          |

---

### 1. Breadth-First Search (BFS) for Unweighted Graphs
- **Use Case**: Finding the shortest path in an unweighted graph. The "length" of the path is the number of edges.
- **Core Idea**: Explores the graph layer by layer, guaranteeing that when it first reaches a node, it has done so via the shortest possible path.

#### Implementation
1. Use a queue and add the `(source, distance)` pair, e.g., `(src, 0)`.
2. Use a `distance` array, initialized to infinity, to store shortest paths and act as a visited set. Set `distance[src] = 0`.
3. While the queue is not empty, dequeue a `(node, dist)`:
4. For each `neighbor` of `node`, if `distance[neighbor]` is still infinity, it means we haven't visited it. Update its distance to `dist + 1`, and enqueue `(neighbor, dist + 1)`.

#### Python Code Snippet
```python
from collections import deque

def bfs_shortest_path(adj: list[list[int]], src: int, n: int) -> list[int]:
    """
    Finds the shortest path from a source to all other nodes in an unweighted graph.
    Returns a list of distances.
    """
    distance = [-1] * n  # Using -1 to indicate unreachability
    queue = deque([(src, 0)])
    distance[src] = 0

    while queue:
        node, dist = queue.popleft()

        for neighbor in adj[node]:
            if distance[neighbor] == -1:  # If not visited
                distance[neighbor] = dist + 1
                queue.append((neighbor, dist + 1))

    return distance
```

---

### 2. Dijkstra's Algorithm
- **Use Case**: Finding the shortest path from a single source in a **weighted graph with no negative edge weights**.
- **Core Idea**: A greedy algorithm that maintains a set of visited vertices and, at each step, selects the unvisited vertex with the smallest known distance from the source to visit next. A **min-priority queue** is used to efficiently select this vertex.

#### Implementation
1. Initialize a `dist` array to infinity, with `dist[src] = 0`.
2. Use a priority queue to store `(distance, vertex)` tuples. Push `(0, src)`.
3. While the priority queue is not empty:
    a. Pop the vertex `u` with the smallest distance.
    b. If this `u` has already been processed with a shorter path, skip it.
    c. For each neighbor `v` of `u` with edge weight `w`:
        - If `dist[u] + w < dist[v]`, a shorter path to `v` is found.
        - Update `dist[v] = dist[u] + w`.
        - Push the new `(dist[v], v)` to the priority queue.

#### Python Code Snippet
```python
import heapq

def dijkstra(adj: list[list[tuple[int, int]]], src: int, n: int) -> list[int]:
    """
    Finds the shortest path from a source using Dijkstra's algorithm.
    adj is a list of lists of (neighbor, weight) tuples.
    """
    pq = [(0, src)]  # (distance, node)
    dist = [float('inf')] * n
    dist[src] = 0

    while pq:
        d, u = heapq.heappop(pq)

        # Skip if we've found a shorter path already
        if d > dist[u]:
            continue

        for v, weight in adj[u]:
            if dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                heapq.heappush(pq, (dist[v], v))

    return dist
```
- **Common Applications**: Network Delay Time, Path with Minimum Effort, Number of Ways to Arrive at Destination (with modifications).

---

### 3. Bellman-Ford Algorithm
- **Use Case**: Finding the shortest path from a single source in a weighted graph that **may contain negative edge weights**.
- **Core Idea**: A dynamic programming approach that relaxes every edge in the graph `V-1` times. A shortest path can have at most `V-1` edges.

#### Implementation
1. Initialize `dist` array to infinity, `dist[src] = 0`.
2. **Relaxation Loop**: Repeat `V-1` times:
   - For every edge `(u, v)` with weight `w`, update the distance if a shorter path is found: `dist[v] = min(dist[v], dist[u] + w)`.
3. **Negative Cycle Detection**: After `V-1` iterations, perform one more relaxation pass. If any distance gets updated during this `V`-th pass, it means a negative-weight cycle reachable from the source exists.

#### Python Code Snippet
```python
def bellman_ford(edges: list[tuple[int, int, int]], src: int, n: int) -> list[int]:
    """
    Finds the shortest path using Bellman-Ford. Also detects negative cycles.
    edges is a list of (u, v, weight) tuples.
    """
    dist = [float('inf')] * n
    dist[src] = 0

    # Relax edges V-1 times
    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    # V-th relaxation to detect negative cycles
    for u, v, w in edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            # Negative cycle detected. Can't find shortest path.
            # Depending on problem, return error or handle as needed.
            return [-1] # Example: indicates negative cycle

    return dist
```
- **Common Applications**: Cheapest Flights Within K Stops (run relaxation loop `K+1` times instead of `V-1`).

---

### 4. Shortest Path in a Directed Acyclic Graph (DAG)
- **Use Case**: Finding the shortest path in a **weighted DAG**. This is more efficient than Dijkstra's for DAGs and works even with negative edge weights.
- **Core Idea**: If we process nodes in topological order, we know that by the time we process a node `u`, we have already found the shortest path to it. We can then relax its outgoing edges.

#### Implementation
1. Find a **topological sort** of the graph's vertices.
2. Initialize `dist` array to infinity, `dist[src] = 0`.
3. For each vertex `u` in topological order:
   - For each neighbor `v` of `u`:
     - Relax the edge: `dist[v] = min(dist[v], dist[u] + weight(u, v))`.

#### Python Code Snippet
```python
# Assumes a 'topological_sort' function is available
# (e.g., using Kahn's algorithm (BFS) or DFS)

def shortest_path_dag(adj: list[list[tuple[int, int]]], src: int, n: int) -> list[int]:
    """
    Finds shortest path in a DAG.
    """
    topo_order = topological_sort(adj, n) # You need to implement this
    dist = [float('inf')] * n
    dist[src] = 0

    for u in topo_order:
        if dist[u] != float('inf'):
            for v, weight in adj[u]:
                if dist[u] + weight < dist[v]:
                    dist[v] = dist[u] + weight

    return dist
```

---

### 5. Floyd-Warshall Algorithm
- **Use Case**: Finding the shortest paths between **all pairs** of vertices (All-Pairs Shortest Path).
- **Core Idea**: A dynamic programming algorithm that considers all possible intermediate nodes for each pair of vertices.

#### Implementation
1. Initialize a 2D `dist` matrix where `dist[i][j]` is the weight of the direct edge from `i` to `j`, or infinity if no direct edge exists. `dist[i][i]` is 0.
2. Use three nested loops (`k`, `i`, `j`):
   - `for k from 0 to V-1`: (the intermediate vertex)
   - `for i from 0 to V-1`: (the source vertex)
   - `for j from 0 to V-1`: (the destination vertex)
     - `dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])`
3. The final `dist` matrix contains all-pairs shortest paths.

#### Python Code Snippet
```python
def floyd_warshall(n: int, edges: list[tuple[int, int, int]]) -> list[list[int]]:
    """
    Finds all-pairs shortest paths.
    """
    # Initialize distance matrix
    dist = [[float('inf')] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for u, v, w in edges:
        dist[u][v] = w

    # Main algorithm
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] != float('inf') and dist[k][j] != float('inf'):
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

    return dist

---

### 6. Minimum Steps to Reach End
`[MEDIUM]` `#dijkstra` `#implicit-graph`

#### Problem Statement
Given an array `arr` and two numbers `start` and `end`, find the minimum steps to reach `end` from `start` by performing multiplication and modulo operations. In one step, you can go from `x` to `(x * arr[i]) % 100000`.

#### Implementation Overview
This is a shortest path problem on an implicit graph where nodes are numbers from 0 to 99999.
-   **Nodes**: Numbers from 0 to 99999.
-   **Edges**: An edge exists from `x` to `y` if `y = (x * arr[i]) % 100000` for some `arr[i]`. Each edge has a weight of 1.
-   **Algorithm**: Since edge weights are uniform (1), this is a shortest path on an unweighted graph problem. However, because we are looking for the shortest path from a single source, Dijkstra's algorithm is a very natural fit (and would work even if weights weren't uniform).

#### Python Code Snippet
```python
import heapq

def minimum_steps(arr: list[int], start: int, end: int) -> int:
    mod = 100000
    dist = {i: float('inf') for i in range(mod)}
    dist[start] = 0

    pq = [(0, start)] # (steps, number)

    while pq:
        steps, u = heapq.heappop(pq)

        if u == end:
            return steps

        if steps > dist[u]:
            continue

        for num in arr:
            v = (u * num) % mod
            if dist[u] + 1 < dist[v]:
                dist[v] = dist[u] + 1
                heapq.heappush(pq, (dist[v], v))

    return -1
```
```
- **Common Applications**: Find the City With the Smallest Number of Neighbors at a Threshold Distance. After running Floyd-Warshall, you can easily check the distance from any city to any other city.

---

### 7. Shortest Distance in a Binary Maze
`[MEDIUM]` `#shortestpath` `#bfs`

#### Problem Statement
Given an `n x n` binary matrix grid where each cell is either 0 or 1, find the length of the shortest clear path from top-left (0,0) to bottom-right (n-1,n-1). If no path exists, return -1.

#### Python Code Snippet
```python
# TODO: Implement Shortest Distance in a Binary Maze
def shortestPathBinaryMatrix(grid):
    pass
```

---

### 8. Path with minimum effort
`[MEDIUM]` `#shortestpath` `#dijkstra`

#### Problem Statement
You are a hiker preparing for an upcoming hike. You are given `heights`, a 2D array of size `rows x columns`, where `heights[row][col]` represents the height of cell `(row, col)`. Find the minimum effort required to travel from top-left to bottom-right. The effort of a path is the maximum absolute difference in heights between two consecutive cells.

#### Python Code Snippet
```python
# TODO: Implement Path with Minimum Effort
def minimumEffortPath(heights):
    pass
```

---

### 9. Cheapest flight within K stops
`[MEDIUM]` `#shortestpath` `#dijkstra` `#bfs`

#### Problem Statement
There are `n` cities connected by some number of flights. You are given an array `flights` where `flights[i] = [from_i, to_i, price_i]`. Also given three integers `src`, `dst`, and `k`, return the cheapest price from `src` to `dst` with at most `k` stops. If no such route exists, return -1.

#### Python Code Snippet
```python
# TODO: Implement Cheapest Flights Within K Stops
def findCheapestPrice(n, flights, src, dst, k):
    pass
```

---

### 10. Network Delay Time
`[MEDIUM]` `#shortestpath` `#dijkstra`

#### Problem Statement
You are given a network of `n` nodes, labeled from 1 to `n`. You are also given `times`, a list of travel times as directed edges `times[i] = [u_i, v_i, w_i]`. We will send a signal from a given node `k`. Return the minimum time it takes for all the `n` nodes to receive the signal. If it is impossible for all nodes to receive the signal, return -1.

#### Python Code Snippet
```python
# TODO: Implement Network Delay Time
def networkDelayTime(times, n, k):
    pass
```

---

### 11. Number of ways to arrive at destination
`[MEDIUM]` `#shortestpath` `#dijkstra` `#dynamicprogramming`

#### Problem Statement
You are in a city that consists of `n` intersections numbered from 0 to `n - 1`. You are given a 2D integer array `roads` where `roads[i] = [u_i, v_i, time_i]`. Find the number of ways you can go from intersection 0 to intersection `n - 1` in the minimum amount of time.

#### Python Code Snippet
```python
# TODO: Implement Number of Ways to Arrive at Destination
def countPaths(n, roads):
    pass
```

---

### 12. Find the city with the smallest number of neighbors
`[MEDIUM]` `#shortestpath` `#floydwarshall`

#### Problem Statement
There are `n` cities numbered from 0 to `n-1`. Given the array `edges` where `edges[i] = [from_i, to_i, weight_i]`. Return the city with the smallest number of cities that are reachable through some path and whose distance is at most `distanceThreshold`.

#### Python Code Snippet
```python
# TODO: Implement Find the City with the Smallest Number of Neighbors
def findTheCity(n, edges, distanceThreshold):
    pass
```
