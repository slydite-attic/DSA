### `[PATTERN] Two Pointers`

The **Two Pointers** technique is a powerful pattern for solving problems involving sorted arrays, linked lists, or strings. It involves using two pointers to iterate through the data structure until they meet or satisfy a certain condition. For linked lists, this pattern is particularly effective for cycle detection, finding middle elements, and solving problems that require looking at two parts of the list simultaneously.

A common variation is the **slow and fast pointer** (or "tortoise and hare") method, where one pointer moves faster than the other.

---

### 1. Middle of a LinkedList
`[EASY]` `#two-pointers` `#slow-fast-pointers` `#linked-list`

#### Problem Statement
Given the `head` of a non-empty singly linked list, return the middle node of the linked list. If there are two middle nodes (in case of an even number of nodes), return the second middle node.

#### Implementation Overview
This is a classic application of the **slow and fast pointer** (or "tortoise and hare") technique.
1.  Initialize two pointers, `slow` and `fast`, both starting at the `head` of the list.
2.  Traverse the list with these pointers, but move `slow` by one step and `fast` by two steps in each iteration.
3.  The loop continues as long as `fast` and `fast.next` are not `None`.
4.  When the `fast` pointer reaches the end of the list, the `slow` pointer will be at the middle.
    -   If the list has an odd number of nodes (e.g., 5), `fast` will end up on the last node (node 5). `slow` will be at node 3.
    -   If the list has an even number of nodes (e.g., 6), `fast` will become `None` (it was at node 5, `fast.next` is node 6, `fast.next.next` is `None`). `slow` will be at node 4, which is the second middle node.
    -   In both cases, `slow` points to the desired middle node.

- **Time Complexity:** `O(N)` because we traverse the list once.
- **Space Complexity:** `O(1)`.

#### Python Code Snippet
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def find_middle(head: ListNode) -> ListNode:
    """
    Finds the middle node of a linked list using the tortoise and hare method.
    If the list has an even number of nodes, it returns the second middle node.
    """
    slow = head
    fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    return slow
```

#### Tricks/Gotchas
- **Loop Condition**: The condition `while fast and fast.next` is crucial. It correctly handles both even and odd length lists and prevents errors from trying to access `fast.next.next` when `fast` or `fast.next` is `None`.
- **Edge Cases**: The code works correctly for a single-node list (returns the node itself).

#### Related Problems
- [Delete the middle node of LL](#6-delete-the-middle-node-of-ll)
- [Check if LL is palindrome or not](Pattern4_Advanced_Problems.md#1-check-if-ll-is-palindrome-or-not)

---

### 2. Detect a loop in LL (Floyd's Cycle-Finding)
`[EASY]` `#two-pointers` `#floyd-cycle-detection` `#linked-list`

#### Problem Statement
Given the `head` of a linked list, determine if the linked list has a cycle in it. A cycle exists if some node in the list can be reached again by continuously following the `next` pointer.

#### Implementation Overview
This is the canonical problem for **Floyd's Cycle-Finding Algorithm**, which uses a slow and fast pointer.
1.  Initialize `slow` and `fast` pointers to the `head`.
2.  Move `slow` one step at a time and `fast` two steps at a time.
3.  If the list has no cycle, the `fast` pointer (or `fast.next`) will eventually become `None`, and the function can return `False`.
4.  If the list *does* have a cycle, the `fast` pointer will eventually lap the `slow` pointer. At some point, `slow` and `fast` will point to the same node.
5.  If a meeting occurs (`slow == fast`), you have detected a loop, and the function should return `True`.

- **Time Complexity:** `O(N)`.
- **Space Complexity:** `O(1)`.

#### Python Code Snippet
```python
def has_cycle(head: ListNode) -> bool:
    """
    Determines if a linked list contains a cycle using Floyd's algorithm.
    """
    slow, fast = head, head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

        if slow == fast:
            return True  # Cycle detected

    return False  # No cycle
```

#### Tricks/Gotchas
- **Proof of Correctness**: The reason this works is that the relative speed between the pointers is 1. If there is a cycle, the fast pointer enters it first, and the slow pointer follows. The "gap" between them decreases by one at each step within the cycle, guaranteeing they will eventually meet.
- **Initialization**: Both pointers must start at the same location for the standard algorithm to work correctly, especially for follow-up problems like finding the cycle's start.

#### Related Problems
- [Find the starting point in LL](#3-find-the-starting-point-of-the-cycle-in-ll)
- [Length of Loop in LL](#4-length-of-loop-in-ll)

---

### 3. Find the starting point of the Cycle in LL
`[MEDIUM]` `#two-pointers` `#floyd-cycle-detection` `#linked-list`

#### Problem Statement
Given the `head` of a linked list that may contain a cycle, return the node where the cycle begins. If there is no cycle, return `null`.

#### Implementation Overview
This is an extension of Floyd's Cycle-Finding Algorithm.
1.  **Phase 1: Detect the Cycle**: First, use the slow/fast pointer approach described above to find a meeting point (`meet`) inside the cycle. If they don't meet (i.e., `fast` becomes `None`), there is no cycle, so return `None`.
2.  **Phase 2: Find the Start Node**: If a meeting point (`meet`) is found, reset one of the pointers (e.g., `slow`) back to the `head` of the list. Keep the other pointer (`fast`) at the `meet` point.
3.  **Move in Unison**: Now, move both `slow` and `fast` one step at a time.
4.  The node where they meet again is the starting node of the cycle.

**Proof Intuition**: Let `L` be the distance from the head to the cycle start. Let `C` be the length of the cycle. Let `m` be the distance from the cycle start to the meeting point. When the pointers meet, `slow` has traveled `L + m`, and `fast` has traveled `L + m + k*C` for some integer `k`. Since `fast` travels twice as fast, `2 * dist(slow) = dist(fast)`.
`2 * (L + m) = L + m + k*C`
`L + m = k*C`
`L = k*C - m`
This equation tells us that the distance from the head to the cycle start (`L`) is equal to `k` full cycles minus the distance from the start to the meeting point (`m`). This is why, if we place one pointer at the head and another at the meeting point and move them at the same speed, they will meet at the cycle's start.

- **Time Complexity:** `O(N)`.
- **Space Complexity:** `O(1)`.

#### Python Code Snippet
```python
def detect_cycle_start(head: ListNode) -> ListNode:
    """
    Finds the starting node of a cycle in a linked list.
    """
    slow, fast = head, head

    # Phase 1: Find the meeting point
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            break  # Meeting point found
    else:
        return None # No cycle

    # Phase 2: Find the start of the cycle
    slow = head
    while slow != fast:
        slow = slow.next
        fast = fast.next

    return slow
```

#### Tricks/Gotchas
- **No Cycle Case**: Ensure you handle the case where no cycle exists (the first loop terminates naturally because `fast` reaches `None`).
- **Two-Phase Process**: Don't confuse the two phases. The first finds *any* meeting point; the second finds the cycle's *start*.

---

### 4. Length of Loop in LL
`[MEDIUM]` `#two-pointers` `#floyd-cycle-detection` `#linked-list`

#### Problem Statement
Given a linked list that is guaranteed to have a cycle, find the length of the cycle.

#### Implementation Overview
1.  **Find Meeting Point**: First, use the standard slow/fast pointer approach to find any node within the cycle. Let's call this `meet_node`.
2.  **Count Nodes in Cycle**: Once you have a node inside the cycle (`meet_node`), keep a pointer fixed at this node.
3.  Start traversing from the *next* node (`meet_node.next`) with another pointer and count the steps until you get back to the `meet_node`.
4.  The final count is the length of the loop.

- **Time Complexity:** `O(N)`.
- **Space Complexity:** `O(1)`.

#### Python Code Snippet
```python
def length_of_cycle(head: ListNode) -> int:
    """
    Calculates the length of the cycle in a linked list.
    Assumes a cycle exists.
    """
    slow, fast = head, head

    # 1. Find the meeting point inside the cycle
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            break
    else:
        return 0 # Should not happen based on problem statement, but good practice

    # 2. Count the length of the loop
    # Keep one pointer at the meeting point, and move another until it comes back.
    count = 1
    temp = slow.next
    while temp != slow:
        count += 1
        temp = temp.next

    return count
```

#### Tricks/Gotchas
- **Starting the Count**: After finding a meeting point (`slow`), initialize the count to 1 and start the counting traversal from the *next* node (`slow.next`). If you start from `slow` itself and the count at 0, the loop `while temp != slow` will not execute, giving a wrong answer of 0.

#### Related Problems
- [Detect a loop in LL](#2-detect-a-loop-in-ll-floyds-cycle-finding)

---

### 5. Remove Nth node from the back of the LL
`[MEDIUM]` `#two-pointers` `#linked-list`

#### Problem Statement
Given the `head` of a linked list, remove the `n`-th node from the end of the list and return its head.

#### Implementation Overview
The most efficient way to do this in a single pass is with two pointers, creating a "gap" between them.
1.  **Use a Dummy Node**: Create a `dummy` node that points to the `head`. This simplifies edge cases, particularly removing the head node itself.
2.  Initialize two pointers, `fast` and `slow`, both at the `dummy` node.
3.  Move the `fast` pointer `n + 1` steps ahead. This creates a gap of `n` nodes between `slow` and `fast`.
4.  Now, move both `fast` and `slow` one step at a time until `fast` reaches the end of the list (`fast` is `None`).
5.  At this point, `slow` will be pointing to the node *just before* the one we want to delete.
6.  To delete the target node, set `slow.next = slow.next.next`.
7.  Return `dummy.next`, which is the new head of the list.

- **Time Complexity:** `O(N)`.
- **Space Complexity:** `O(1)`.

#### Python Code Snippet
```python
def remove_nth_from_end(head: ListNode, n: int) -> ListNode:
    """
    Removes the Nth node from the end of the list in a single pass.
    """
    # Use a dummy node to handle edge case of removing the head
    dummy = ListNode(0, head)
    slow = dummy
    fast = dummy

    # Move fast pointer n+1 steps ahead to create the gap
    for _ in range(n + 1):
        fast = fast.next

    # Move both until fast reaches the end
    while fast is not None:
        slow = slow.next
        fast = fast.next

    # slow is now at the node before the target. Delete the Nth node.
    slow.next = slow.next.next

    return dummy.next
```

#### Tricks/Gotchas
- **Dummy Node**: The dummy node is the key to simplifying the logic. Without it, you would need separate code to handle the case where the head node is removed. By starting `slow` and `fast` at `dummy` and moving `fast` `n+1` steps, `slow` naturally lands on the predecessor of the target node.
- **Off-by-one Errors**: Be careful with pointer positioning. The goal is to have `slow` point to the node *before* the target. The `n+1` gap is crucial for this.

#### Related Problems
- [Middle of a LinkedList](#1-middle-of-a-linkedlist)

---

### 6. Delete the middle node of LL
`[MEDIUM]` `#two-pointers` `#linked-list`

#### Problem Statement
Given the `head` of a singly linked list, delete the middle node and return the `head` of the modified list. The middle node is determined using the same rules as the "Middle of a LinkedList" problem (if two middle nodes, the second is chosen).

#### Implementation Overview
This problem combines finding the middle node with deletion. The key is to find the node *before* the middle node.
1.  **Handle Edge Cases**: If the list is empty or has only one node, deleting the middle results in an empty list, so return `None`.
2.  **Find Node Before Middle**: Use the slow and fast pointer technique. To find the predecessor of the middle node, we can keep a `prev` pointer that trails the `slow` pointer.
3.  Initialize `slow`, `fast`, and `prev_to_slow = None`.
4.  In the standard two-pointer loop, update `prev_to_slow` to be `slow` *before* `slow` moves forward.
5.  When the loop terminates, `slow` is at the middle node, and `prev_to_slow` is at the node just before it.
6.  Delete the middle node by linking `prev_to_slow.next` to `slow.next`.

- **Time Complexity:** `O(N)`.
- **Space Complexity:** `O(1)`.

#### Python Code Snippet
```python
def delete_middle_node(head: ListNode) -> ListNode:
    """
    Deletes the middle node of a linked list.
    """
    if not head or not head.next:
        return None

    # We need a pointer to the node *before* the middle node
    slow, fast = head, head
    prev_to_slow = None

    while fast and fast.next:
        prev_to_slow = slow
        slow = slow.next
        fast = fast.next.next

    # slow is now the middle node, prev_to_slow is the node before it
    # Delete the middle node
    prev_to_slow.next = slow.next

    return head
```

#### Tricks/Gotchas
- **Finding the Predecessor**: The main challenge is not just to find the middle node, but its predecessor, which is required for deletion. A dedicated `prev_to_slow` pointer is a straightforward way to track it.
- **Two-Node Case**: In a two-node list `[1, 2]`, `slow` becomes `2` and `prev_to_slow` becomes `1`. The code correctly sets `1.next = 2.next` (which is `None`), resulting in `[1]`.

#### Related Problems
- [Middle of a LinkedList](#1-middle-of-a-linkedlist)

---

### 7. Find the intersection point of Y LL
`[MEDIUM]` `#two-pointers` `#linked-list`

#### Problem Statement
Given the heads of two singly linked-lists `headA` and `headB`, return the node at which the two lists intersect. If the two linked lists have no intersection at all, return `null`. The lists are guaranteed to have no cycles.

#### Implementation Overview
A clever two-pointer approach solves this efficiently without needing to calculate list lengths.
1.  Initialize two pointers, `ptrA = headA` and `ptrB = headB`.
2.  Traverse with both pointers simultaneously.
3.  If `ptrA` reaches the end of list A (`None`), redirect it to the head of list B.
4.  Similarly, if `ptrB` reaches the end of list B, redirect it to the head of list A.
5.  Continue this process. If the lists intersect, the pointers are guaranteed to meet at the intersection node. If they don't intersect, they will both become `None` at the same time after traversing both lists completely.

This works because by switching heads, both pointers travel the same total distance (`lenA + lenB`) before the loop terminates. Any difference in path length before a potential intersection is canceled out after the switch.

- **Time Complexity:** `O(N + M)` where N and M are the lengths of the two lists.
- **Space Complexity:** `O(1)`.

#### Python Code Snippet
```python
def get_intersection_node(headA: ListNode, headB: ListNode) -> ListNode:
    """
    Finds the intersection node of two linked lists.
    """
    if not headA or not headB:
        return None

    ptrA = headA
    ptrB = headB

    while ptrA != ptrB:
        # If a pointer reaches the end of its list, redirect it to the head of the other list
        ptrA = headB if ptrA is None else ptrA.next
        ptrB = headA if ptrB is None else ptrB.next

    # The loop terminates when ptrA == ptrB.
    # This is either the intersection node or None (if they both reached the end).
    return ptrA
```

#### Tricks/Gotchas
- **Termination Condition**: The loop condition `while ptrA != ptrB` elegantly handles both intersection and no-intersection cases. If there's no intersection, both pointers become `None` after traversing `lenA + lenB` nodes. Since `None == None`, the loop terminates, correctly returning `None`.
- **Alternative Method**: A less efficient but valid method is to find the lengths of both lists (`lenA`, `lenB`), calculate the difference `d`, move the pointer of the longer list `d` steps forward, and then traverse both lists in unison until the pointers meet.

---

### 8. Find pairs with given sum in a sorted Doubly LL
`[MEDIUM]` `#two-pointers` `#doubly-linked-list`

#### Problem Statement
Given a *sorted* doubly linked list of distinct elements, find all pairs of nodes whose sum is equal to a given value `x`.

#### Implementation Overview
This problem is a classic two-pointer pattern, adapted for a doubly linked list. Because the list is sorted and we can traverse backward using the `prev` pointer, we can solve this efficiently.
1.  **Initialize Pointers**:
    -   Create a `left` pointer and initialize it to the `head` of the list.
    -   Create a `right` pointer and initialize it to the `tail` of the list. (To find the tail, you must traverse the list once).
2.  **Traverse Inward**:
    -   Loop as long as the `left` pointer is not the same as the `right` pointer and they haven't crossed.
    -   Calculate the `current_sum = left.data + right.data`.
    -   **Case 1: `current_sum == x`**: A pair is found. Record it. Move both pointers inward (`left = left.next`, `right = right.prev`).
    -   **Case 2: `current_sum < x`**: The sum is too small. We need a larger value, so move the `left` pointer forward (`left = left.next`).
    -   **Case 3: `current_sum > x`**: The sum is too large. We need a smaller value, so move the `right` pointer backward (`right = right.prev`).
3.  The loop terminates when the pointers meet or cross, meaning all possible pairs have been checked.

- **Time Complexity:** `O(N)` to find the tail and traverse the list.
- **Space Complexity:** `O(1)`.

#### Python Code Snippet
```python
class DoublyListNode:
    def __init__(self, data, next=None, prev=None):
        self.data = data
        self.next = next
        self.prev = prev

def find_pairs_with_sum(head: DoublyListNode, x: int) -> list:
    """
    Finds all pairs in a sorted doubly linked list that sum up to x.
    """
    if not head or not head.next:
        return []

    # Find the tail of the list
    right = head
    while right.next:
        right = right.next

    left = head
    pairs = []

    # Pointers move towards each other
    while left != right and right.next != left:
        current_sum = left.data + right.data

        if current_sum == x:
            pairs.append((left.data, right.data))
            left = left.next
            right = right.prev
        elif current_sum < x:
            left = left.next
        else: # current_sum > x
            right = right.prev

    return pairs
```

#### Tricks/Gotchas
- **Finding the Tail**: An initial O(N) traversal is required to find the tail pointer before the two-pointer traversal can begin.
- **Pointer Crossing Condition**: The loop must terminate correctly. `left != right` handles the odd-length case, and `right.next != left` handles the even-length case, preventing pointers from overlapping and re-checking pairs.
- **Sorted List**: This approach fundamentally relies on the list being sorted.

#### Related Problems
- Two Sum (in an array)
