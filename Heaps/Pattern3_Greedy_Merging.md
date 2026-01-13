# Pattern 3: Heaps for Greedy Algorithms & Merging

This pattern explores two powerful applications of heaps: as a core component in greedy algorithms and as the primary tool for K-way merging. In greedy problems, a heap helps in efficiently selecting the best local choice at each step. In merging, a heap keeps track of the smallest (or largest) items from multiple sorted sources.

---

### 1. Connect n ropes with minimal cost
`[MEDIUM]` `#greedy` `#min-heap`

#### Problem Statement
You are given `n` ropes of different lengths. The cost to connect two ropes is equal to their sum. Your task is to connect the ropes into a single rope with the minimum possible cost.

*Example:* `ropes = [4, 3, 2, 6]`. **Output:** `29`.
(Connect 2+3=5. Ropes: [4,5,6]. Cost so far: 5.
Connect 4+5=9. Ropes: [6,9]. Cost so far: 5+9=14.
Connect 6+9=15. Ropes: [15]. Cost so far: 14+15=29)

#### Implementation Overview
To minimize total cost, always connect the two shortest available ropes. A **Min-Heap** is perfect for this.
1.  Add all rope lengths to a min-heap.
2.  Loop until only one rope remains in the heap:
    a. Extract the two smallest ropes.
    b. Calculate the cost to connect them and add this to the total cost.
    c. Add the new, combined rope length back into the min-heap.

#### Time and Space Complexity
- **Time Complexity:** $O(N \log N)$. Building the heap takes $O(N)$, and we perform $N-1$ extraction and insertion pairs, each taking $O(\log N)$.
- **Space Complexity:** $O(N)$ for the heap.

#### Python Code Snippet
```python
import heapq
def min_cost_to_connect_ropes(ropes: list[int]) -> int:
    heapq.heapify(ropes) # Turn the list into a min-heap in-place
    total_cost = 0

    while len(ropes) > 1:
        rope1 = heapq.heappop(ropes)
        rope2 = heapq.heappop(ropes)

        cost = rope1 + rope2
        total_cost += cost

        heapq.heappush(ropes, cost)

    return total_cost
```

---

### 2. Task Scheduler
`[MEDIUM]` `#greedy` `#max-heap` `#frequency`

#### Problem Statement
Given a list of tasks and a non-negative integer `n` representing the cooldown period between two same tasks, find the least number of CPU intervals required to complete all tasks.

*Example:* `tasks = ["A","A","A","B","B","B"]`, `n = 2`. **Output:** `8` (A -> B -> idle -> A -> B -> idle -> A -> B).

#### Implementation Overview
The greedy strategy is to execute the most frequent task first. A **Max-Heap** keeps track of task frequencies.
1.  Count task frequencies using a hash map.
2.  Push all frequencies into a max-heap.
3.  The main loop processes tasks in chunks. In each chunk:
    a. Pop up to `n+1` tasks from the heap and store them temporarily.
    b. Decrement their frequencies.
    c. Push tasks with remaining frequency > 0 back onto the max-heap.
    d. Add `n+1` to the total time (or the number of tasks processed if the heap is now empty).

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the number of tasks. The heap operations are constant because there are at most 26 distinct tasks (or a fixed constant).
- **Space Complexity:** $O(1)$ (since heap size is limited by the alphabet size).

#### Python Code Snippet
```python
import heapq
from collections import Counter, deque
def least_interval(tasks: list[str], n: int) -> int:
    counts = Counter(tasks)
    max_heap = [-count for count in counts.values()]
    heapq.heapify(max_heap)

    time = 0
    q = deque() # Stores pairs of [-count, ready_time]

    while max_heap or q:
        time += 1

        if max_heap:
            count = heapq.heappop(max_heap)
            if count + 1 < 0: # If there are remaining tasks
                q.append((count + 1, time + n))

        if q and q[0][1] == time:
            heapq.heappush(max_heap, q.popleft()[0])

    return time
```

---

### 3. Hand of Straights
`[MEDIUM]` `#greedy` `#hashmap`

#### Problem Statement
Given an array of integers `hand` and an integer `groupSize`, return `true` if the `hand` can be rearranged into groups of `groupSize` consecutive cards.

*Example:* `hand = [1,2,3,6,2,3,4,7,8]`, `groupSize = 3`. **Output:** `true` ([1,2,3], [2,3,4], [6,7,8]).

#### Implementation Overview
A greedy approach works. Always try to form a sequence starting with the smallest available card.
1.  Check if `len(hand) % groupSize != 0`. If so, return `false`.
2.  Count card frequencies in a hash map.
3.  Push all unique card numbers into a min-heap.
4.  While the heap is not empty:
    a. Pop the smallest card (`start_card`).
    b. If its count is zero (used by a previous group), continue.
    c. For `groupSize` cards starting from `start_card`, check if each consecutive card exists with a positive count.
    d. If not, return `false`. If yes, decrement their counts.

#### Time and Space Complexity
- **Time Complexity:** $O(N \log N)$ or $O(N \log M)$ where $M$ is unique cards.
- **Space Complexity:** $O(N)$ for the frequency map and heap.

#### Python Code Snippet
```python
import heapq
from collections import Counter
def is_n_straight_hand(hand: list[int], groupSize: int) -> bool:
    if len(hand) % groupSize != 0:
        return False

    counts = Counter(hand)
    min_heap = list(counts.keys())
    heapq.heapify(min_heap)

    while min_heap:
        start_card = min_heap[0]

        # Check if we can form a group starting with start_card
        for i in range(groupSize):
            card = start_card + i
            if counts.get(card, 0) == 0:
                return False
            counts[card] -= 1
            if counts[card] == 0:
                # Ensure the card we are removing is the smallest one
                if card != heapq.heappop(min_heap):
                    return False
    return True
```

---

### 4. Merge K Sorted Lists
`[MEDIUM]` `#k-way-merge` `#min-heap`

#### Problem Statement
You are given `k` sorted linked lists. Merge them into a single sorted linked list.

#### Implementation Overview
This is the canonical **K-way Merge** problem. A Min-Heap efficiently tracks the smallest element across all `k` lists.
1.  Initialize a min-heap.
2.  Push the head node from each of the `k` lists onto the heap. Store `(value, list_index, node)`.
3.  Create a dummy head for the result list.
4.  While the heap is not empty:
    a. Pop the smallest element tuple.
    b. Add the node to the result list.
    c. If the popped node has a `next` node, push it onto the heap.

#### Time and Space Complexity
- **Time Complexity:** $O(N \log K)$, where $N$ is the total number of elements across all lists and $K$ is the number of lists.
- **Space Complexity:** $O(K)$ for the heap.

#### Python Code Snippet
```python
import heapq
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
def merge_k_lists(lists: list) -> list:
    min_heap = []
    for i, l in enumerate(lists):
        if l:
            # Add a tie-breaker (list index i) for nodes with same value
            heapq.heappush(min_heap, (l.val, i, l))

    dummy = current = ListNode()
    while min_heap:
        val, i, node = heapq.heappop(min_heap)
        current.next = node
        current = current.next
        if node.next:
            heapq.heappush(min_heap, (node.next.val, i, node.next))

    return dummy.next
```

---

### 5. Design Twitter
`[MEDIUM]` `#system-design` `#k-way-merge` `#max-heap`

#### Problem Statement
Design a simplified Twitter where users can post tweets, follow/unfollow, and get the 10 most recent tweets in their news feed.

#### Implementation Overview
The most complex part is `getNewsFeed`. It's a K-way merge of sorted lists (the tweet lists of the user and their followed users).
-   **Data Structures:**
    -   `user_tweets`: map `userId -> list[(timestamp, tweetId)]`.
    -   `user_follows`: map `userId -> set[userId]`.
-   **`getNewsFeed(userId)` Logic:**
    1.  Get all relevant users (self + followed).
    2.  Use a **Max-Heap** to find the 10 most recent tweets. For each relevant user, get their most recent tweet.
    3.  Push `(timestamp, tweetId, user_id, tweet_index)` for the latest tweet from each user onto the max-heap.
    4.  Loop 10 times: Pop the max, add to result, and push the next tweet from the same user onto the heap.

#### Time and Space Complexity
- **Time Complexity:** $O(F)$, where $F$ is the number of followees, to build the heap. Retrieving the feed takes $O(10 \cdot \log F)$.
- **Space Complexity:** $O(F)$ for the heap.

#### Python Code Snippet
```python
import heapq
from collections import defaultdict, deque
class Twitter:
    def __init__(self):
        self.time = 0
        self.user_tweets = defaultdict(deque) # userId -> deque of (time, tweetId)
        self.user_follows = defaultdict(set) # followerId -> set of followeeId

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.time += 1
        self.user_tweets[userId].appendleft((self.time, tweetId))
        if len(self.user_tweets[userId]) > 10:
            self.user_tweets[userId].pop()

    def getNewsFeed(self, userId: int) -> list[int]:
        users_to_follow = self.user_follows[userId] | {userId}
        min_heap = []

        for user in users_to_follow:
            for tweet in self.user_tweets[user]:
                heapq.heappush(min_heap, tweet)
                if len(min_heap) > 10:
                    heapq.heappop(min_heap)

        feed = []
        while min_heap:
            feed.append(heapq.heappop(min_heap)[1])
        return feed[::-1]

    def follow(self, followerId: int, followeeId: int) -> None:
        self.user_follows[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        self.user_follows[followerId].discard(followeeId)

---

### 6. Sort a K-Sorted Array
`[MEDIUM]` `#k-way-merge` `#min-heap` `#sorting`

#### Problem Statement
You are given a "K-Sorted" array, where each element is at most `k` positions away from its sorted position. Sort the array efficiently.

*Example:* `arr = [6, 5, 3, 2, 8, 10, 9]`, `k = 3`. **Output:** `[2, 3, 5, 6, 8, 9, 10]`.

#### Implementation Overview
A naive sort would be O(N log N). We can do better by using a min-heap of size `k+1`, which leverages the "nearly sorted" property.
1.  Create a min-heap and populate it with the first `k+1` elements from the array.
2.  Initialize a `result` array and an `index` for placing sorted elements.
3.  Iterate through the rest of the array (from index `k+1` onwards):
    a. Extract the minimum element from the heap and place it at the current `index` in the result array.
    b. Push the current element from the input array (`arr[i]`) into the heap.
4.  After the loop, the heap will still contain `k+1` elements. Pop them one by one and add them to the result array.

#### Time and Space Complexity
- **Time Complexity:** $O(N \log K)$.
- **Space Complexity:** $O(K)$ for the heap.

#### Python Code Snippet
```python
import heapq

def sort_k_sorted_array(arr: list[int], k: int) -> list[int]:
    n = len(arr)
    # Create a min-heap with the first k+1 elements
    min_heap = arr[:k+1]
    heapq.heapify(min_heap)

    result_idx = 0

    # Iterate through the rest of the elements
    for i in range(k + 1, n):
        # The smallest element in the heap is the next sorted element
        arr[result_idx] = heapq.heappop(min_heap)
        result_idx += 1
        # Add the new element to the heap
        heapq.heappush(min_heap, arr[i])

    # Empty the remaining elements from the heap
    while min_heap:
        arr[result_idx] = heapq.heappop(min_heap)
        result_idx += 1

    return arr
```
```
