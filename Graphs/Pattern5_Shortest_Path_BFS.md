# Pattern 5: Shortest Path in Unweighted Graphs via BFS

A fundamental property of Breadth-First Search (BFS) is that it explores a graph level by level. This makes it the ideal algorithm for finding the shortest path between two nodes in an **unweighted graph**. The first time BFS reaches a target node, it is guaranteed to have done so via a shortest possible path.

This pattern focuses on problems where the graph is not given explicitly but must be inferred from the input. The "nodes" and "edges" represent relationships between data points (like words differing by one letter).

---

### 1. Word Ladder I
`[HARD]` `#bfs` `#shortest-path` `#implicit-graph`

#### Problem Statement
Given a `beginWord`, an `endWord`, and a `wordList`, return the length of the shortest transformation sequence from `beginWord` to `endWord`, where each transformation consists of changing a single letter. Each transformed word must exist in the `wordList`. If no such sequence exists, return 0.

*Example:* `beginWord = "hit"`, `endWord = "cog"`, `wordList = ["hot","dot","dog","lot","log","cog"]`. **Output:** `5` ("hit" -> "hot" -> "dot" -> "dog" -> "cog").

#### Implementation Overview
This is a shortest path problem on an implicit graph.
- **Nodes**: The words in the `wordList` (plus `beginWord`).
- **Edges**: An edge exists between two words if they differ by exactly one letter.

A brute-force graph construction would be too slow. Instead, we generate neighbors on the fly during the BFS.
1.  Add the `wordList` to a `Set` for O(1) lookups.
2.  Initialize a queue for BFS and add `(beginWord, 1)` where 1 is the path length.
3.  Use a `visited` set (or remove words from the `wordSet`) to avoid cycles.
4.  **BFS Loop**:
    - Dequeue `(current_word, length)`.
    - If `current_word` is the `endWord`, return `length`.
    - **Generate Neighbors**: For each character in `current_word`, try substituting it with every letter from 'a' to 'z'.
    - For each `new_word` generated, if it's in the `wordSet`, it's a valid neighbor. Add it to the queue and mark as visited.

#### Python Code Snippet
```python
from collections import deque
def ladder_length(beginWord: str, endWord: str, wordList: list[str]) -> int:
    wordSet = set(wordList)
    if endWord not in wordSet:
        return 0

    q = deque([(beginWord, 1)])
    # Removing from the set is an efficient way to mark as visited
    if beginWord in wordSet:
        wordSet.remove(beginWord)

    while q:
        word, length = q.popleft()
        if word == endWord:
            return length

        for i in range(len(word)):
            for char_code in range(ord('a'), ord('z') + 1):
                new_char = chr(char_code)
                new_word = word[:i] + new_char + word[i+1:]

                if new_word in wordSet:
                    wordSet.remove(new_word)
                    q.append((new_word, length + 1))
    return 0
```
#### Time and Space Complexity
- **Time Complexity:** $O(M^2 \times N)$, where $M$ is the word length and $N$ is the number of words. Generating neighbors takes $M \times 26$, and string operations take $O(M)$.
- **Space Complexity:** $O(M \times N)$ for the word set and queue.

---

### 2. Word Ladder II
`[HARD]` `#bfs` `#shortest-path` `#implicit-graph` `#backtracking`

#### Problem Statement
Given a `beginWord`, an `endWord`, and a `wordList`, return *all* the shortest transformation sequences from `beginWord` to `endWord`.

*Example:* `beginWord = "hit"`, `endWord = "cog"`, `wordList = ["hot","dot","dog","lot","log","cog"]`.
**Output:** `[["hit","hot","dot","dog","cog"], ["hit","hot","lot","log","cog"]]`

#### Implementation Overview
This is much harder because we need to reconstruct all shortest paths. A simple BFS isn't enough. A common approach is a two-phase process:
1.  **Phase 1: BFS to find shortest path distances.**
    - Perform a BFS starting from `beginWord`.
    - Use a `distance_map` to store the shortest distance from `beginWord` to every reachable word.
    - We only add a word to the queue if we find a path to it that is shorter than any previously found path.
2.  **Phase 2: DFS with Backtracking to reconstruct paths.**
    - Once we have the `distance_map`, we can find all valid paths by starting a DFS from the `endWord` and working backwards.
    - `dfs(word, current_path)`:
        - Add `word` to `current_path`.
        - If `word` is `beginWord`, a valid path has been found. Reverse it and add to results.
        - For each neighbor of `word`, if `distance_map[neighbor] == distance_map[word] - 1`, it's on a shortest path. Recurse.
        - Backtrack by removing `word` from `current_path`.

#### Python Code Snippet
```python
from collections import deque, defaultdict
def find_ladders(beginWord: str, endWord: str, wordList: list[str]) -> list[list[str]]:
    wordSet = set(wordList)
    if endWord not in wordSet:
        return []

    # Phase 1: BFS to find shortest path distances
    distance = {beginWord: 0}
    q = deque([beginWord])

    while q:
        word = q.popleft()
        if word == endWord:
            break # Found shortest path length, no need to go further

        for i in range(len(word)):
            for char_code in range(ord('a'), ord('z') + 1):
                new_word = word[:i] + chr(char_code) + word[i+1:]
                if new_word in wordSet and new_word not in distance:
                    distance[new_word] = distance[word] + 1
                    q.append(new_word)

    # Phase 2: DFS to reconstruct paths
    results = []
    if endWord in distance: # Check if endWord is reachable
        def dfs(word, path):
            if word == beginWord:
                results.append(path[::-1])
                return

            for i in range(len(word)):
                for char_code in range(ord('a'), ord('z') + 1):
                    prev_word = word[:i] + chr(char_code) + word[i+1:]
                    # Check if prev_word is part of a shortest path
                    if distance.get(prev_word) == distance[word] - 1:
                        path.append(prev_word)
                        dfs(prev_word, path)
                        path.pop() # Backtrack

        dfs(endWord, [endWord])

    return results
```
#### Time and Space Complexity
- **Time Complexity:** $O(M^2 \times N)$ for BFS + DFS overhead (can be exponential in worst case due to many paths).
- **Space Complexity:** $O(M \times N)$ for storing paths and graph structures.
