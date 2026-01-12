### `[PATTERN] Reversal and Rearrangement`

This pattern focuses on techniques to alter the structure of a linked list, primarily through reversal and reordering of its nodes. Mastering list reversal is fundamental, as it's a subroutine in many more complex problems. These problems often require a combination of pointer manipulations, including the two-pointer technique, to achieve the desired new structure.

---

### 1. Reverse a LinkedList (Iterative and Recursive)
`[EASY]` `#reversal` `#linked-list`

#### Problem Statement
Given the `head` of a singly linked list, reverse the list, and return the new head.

---

#### a) Iterative Approach

The iterative approach is generally preferred due to its O(1) space complexity. It involves using three pointers to traverse the list and reverse the links between nodes.

##### Implementation Overview
1.  Initialize three pointers: `prev = None`, `current = head`, and `next_node = None`.
2.  Iterate through the list as long as `current` is not `None`.
3.  In each iteration:
    a.  Store the next node: `next_node = current.next`.
    b.  Reverse the link: `current.next = prev`.
    c.  Move the pointers one step forward: `prev = current`, `current = next_node`.
4.  When the loop ends, `prev` will be pointing to the new head of the reversed list.

- **Time Complexity:** `O(N)`.
- **Space Complexity:** `O(1)`.

##### Python Code Snippet
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_list_iterative(head: ListNode) -> ListNode:
    """
    Reverses a singly linked list iteratively.
    """
    prev = None
    current = head
    while current:
        next_node = current.next  # Store next node
        current.next = prev       # Reverse the link
        prev = current            # Move prev to current
        current = next_node       # Move to the original next node
    return prev # prev is the new head
```

---

#### b) Recursive Approach

The recursive approach provides a more concise but less space-efficient (O(N) stack space) solution.

##### Implementation Overview
1.  **Base Case**: If the list is empty (`head is None`) or has only one node (`head.next is None`), it's already reversed, so return `head`.
2.  **Recursive Step**:
    a.  Recursively call the function on the rest of the list (`head.next`). This will reverse the sub-list and return its new head (`new_head`).
    b.  The `head` node is still pointing to the *last node* of the original sub-list (which is now the second node of the reversed sub-list). Let this be `head.next`.
    c.  To connect `head` to the end of the reversed sub-list, set `head.next.next = head`.
    d.  Break the original forward link: `head.next = None`.
3.  Return `new_head`.

- **Time Complexity:** `O(N)`.
- **Space Complexity:** `O(N)` for the recursion stack.

##### Python Code Snippet
```python
def reverse_list_recursive(head: ListNode) -> ListNode:
    """
    Reverses a singly linked list recursively.
    """
    # Base case: empty list or a single node
    if not head or not head.next:
        return head

    # Recursively reverse the rest of the list
    new_head = reverse_list_recursive(head.next)

    # head.next is the last node of the original list, which should point back to head
    head.next.next = head
    head.next = None # Break the original link

    return new_head
```

---

### 2. Reverse Nodes in k-Group
`[HARD]` `#reversal` `#recursion` `#linked-list`

#### Problem Statement
Given the `head` of a linked list, reverse the nodes of the list `k` at a time, and return the modified list. `k` is a positive integer and is less than or equal to the length of the linked list. If the number of nodes is not a multiple of `k`, then the left-out nodes, in the end, should remain as they are.

#### Implementation Overview (Recursive)
This is a classic recursion problem. The main idea is to reverse the first `k` nodes and then recursively call the function on the rest of the list.

1.  **Base Case**: If there are fewer than `k` nodes left, do nothing and return the `head`.
2.  **Check for `k` nodes**: First, traverse `k` nodes to ensure there are enough nodes to reverse. If not, return `head`.
3.  **Reverse the `k`-group**:
    a. Use the iterative reversal method to reverse the first `k` nodes of the current segment. The `head` of this segment will become the tail, and the `k`-th node will become the new head (`new_head`).
    b. The original `head` of this segment (which is now the tail of the reversed group) needs to point to the result of the recursive call on the rest of the list.
4.  **Recursive Link**: The `head` of the original list (which is now the tail of the first reversed group) should have its `next` pointer set to the head of the *next* reversed group, which is obtained by `reverse_k_group(next_segment_head, k)`.

- **Time Complexity:** `O(N)`.
- **Space Complexity:** `O(N/k)` for the recursion stack.

#### Python Code Snippet
```python
def reverse_k_group(head: ListNode, k: int) -> ListNode:
    """
    Reverses nodes of a linked list k at a time.
    """
    # 1. Check if there are at least k nodes left
    curr = head
    for _ in range(k):
        if not curr:
            return head # Not enough nodes, return as is
        curr = curr.next

    # 2. Reverse the first k nodes
    prev = None
    curr = head
    for _ in range(k):
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node

    # 3. Recursively call for the rest of the list
    # head is now the tail of the reversed group.
    # curr is the head of the next segment.
    # prev is the new head of the current reversed group.
    if curr:
        head.next = reverse_k_group(curr, k)

    return prev # prev is the new head of this segment
```

---

### 3. Rotate List
`[MEDIUM]` `#rearrangement` `#two-pointers` `#linked-list`

#### Problem Statement
Given the `head` of a linked list, rotate the list to the right by `k` places.

#### Implementation Overview
A right rotation by `k` means the last `k` nodes become the first `k` nodes.
1.  **Handle Edge Cases**: If the list is empty, has one node, or `k=0`, return `head`.
2.  **Find Length and Connect to Tail**: Traverse the list to find its length (`L`) and the last node. Connect the last node's `next` to the `head`, forming a cycle.
3.  **Handle Large `k`**: The number of effective rotations is `k % L`.
4.  **Find the New Tail**: The new tail of the list will be at position `L - (k % L) - 1` from the original head. The node *after* this new tail will be the new head.
5.  **Break the Cycle**: Traverse `L - (k % L) - 1` steps from the head to find the new tail. The next node is the `new_head`. Set `new_tail.next = None` to break the cycle.
6.  Return `new_head`.

- **Time Complexity:** `O(N)`.
- **Space Complexity:** `O(1)`.

#### Python Code Snippet
```python
def rotate_right(head: ListNode, k: int) -> ListNode:
    if not head or not head.next or k == 0:
        return head

    # 1. Find length and last node
    last_node = head
    length = 1
    while last_node.next:
        last_node = last_node.next
        length += 1

    # 2. Connect to form a cycle
    last_node.next = head

    # 3. Reduce k
    k = k % length

    # 4. Find the new tail (node before the new head)
    # The new head is at index length - k
    steps_to_new_tail = length - k - 1
    new_tail = head
    for _ in range(steps_to_new_tail):
        new_tail = new_tail.next

    # 5. Find new head and break the cycle
    new_head = new_tail.next
    new_tail.next = None

    return new_head
```

---

### 4. Reorder List
`[MEDIUM]` `#rearrangement` `#two-pointers` `#reversal` `#linked-list`

#### Problem Statement
Given the `head` of a singly linked list, reorder it in-place such that the new order is `L0 → Ln → L1 → Ln-1 → L2 → Ln-2 → …`.

#### Implementation Overview
This is a multi-step problem that combines several patterns.
1.  **Find the Middle**: Use the slow/fast pointer method to find the middle of the list. This will split the list into two halves.
2.  **Reverse the Second Half**: Reverse the second half of the list starting from `slow.next`. After reversal, set `slow.next = None` to break the link between the two halves.
3.  **Merge the Two Halves**: Merge the first half (`head`) and the reversed second half (`reversed_head`) by interleaving their nodes. Use two pointers, one for each half, and carefully rewire their `next` pointers.

- **Time Complexity:** `O(N)`.
- **Space Complexity:** `O(1)`.

#### Python Code Snippet
```python
def reorder_list(head: ListNode) -> None:
    """
    Reorders the list in-place.
    """
    if not head or not head.next:
        return

    # 1. Find the middle of the list
    slow, fast = head, head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next

    # 2. Reverse the second half
    # slow.next is the head of the second half
    prev, curr = None, slow.next
    while curr:
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node
    slow.next = None # Split the list into two

    # 3. Merge the two halves
    # head1 is the first half, head2 is the reversed second half (prev)
    head1, head2 = head, prev
    while head2:
        # Store next nodes
        next1 = head1.next
        next2 = head2.next

        # Interleave
        head1.next = head2
        head2.next = next1

        # Move pointers
        head1 = next1
        head2 = next2
```

---

### 5. Palindrome Linked List
`[EASY]` `#reversal` `#two-pointers` `#linked-list`

#### Problem Statement
Given the `head` of a singly linked list, return `true` if it is a palindrome.

#### Implementation Overview
An efficient O(1) space solution follows a similar pattern to "Reorder List".
1.  **Find the Middle**: Use the slow/fast pointer method to find the middle.
2.  **Reverse the Second Half**: Reverse the list from the middle node onwards.
3.  **Compare Halves**: Compare the first half with the reversed second half. Initialize one pointer at the `head` and another at the head of the reversed second half. Traverse both. If any data values don't match, it's not a palindrome.
4.  **(Optional) Restore List**: If required, reverse the second half again to restore the original list structure.

- **Time Complexity:** `O(N)`.
- **Space Complexity:** `O(1)`.

#### Python Code Snippet
```python
def is_palindrome(head: ListNode) -> bool:
    if not head or not head.next:
        return True

    # 1. Find the middle
    slow, fast = head, head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    # 2. Reverse the second half (from slow pointer)
    prev = None
    curr = slow
    while curr:
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node

    # 3. Compare the first half and the reversed second half
    left, right = head, prev # prev is the head of reversed second half
    while right: # Only need to check up to the end of the shorter (reversed) half
        if left.val != right.val:
            return False
        left = left.next
        right = right.next

    return True

---

### 6. Segregate Odd and Even Nodes
`[MEDIUM]` `#rearrangement` `#linked-list`

#### Problem Statement
Given the `head` of a singly linked list, group all the nodes with odd indices together followed by the nodes with even indices, and return the reordered list. The relative order within the odd and even groups should remain the same.

#### Implementation Overview
The goal is to create two separate lists—one for odd-indexed nodes and one for even-indexed nodes—and then link them.
1.  **Handle Edge Cases**: If the list has 0, 1, or 2 nodes, it's already segregated.
2.  **Initialize Pointers**:
    -   `odd = head` (points to the tail of the odd-indexed list)
    -   `even_head = head.next` (a fixed pointer to the head of the even list)
    -   `even = even_head` (points to the tail of the even-indexed list)
3.  **Traverse and Relink**:
    -   Iterate as long as `even` and `even.next` are valid.
    -   Link the next odd node: `odd.next = even.next`. Move `odd` forward.
    -   Link the next even node: `even.next = odd.next`. Move `even` forward.
4.  **Connect the Lists**: After the loop, the `odd` pointer is at the tail of the odd list. Connect it to the head of the even list: `odd.next = even_head`.

- **Time Complexity:** `O(N)`.
- **Space Complexity:** `O(1)`.

#### Python Code Snippet
```python
def odd_even_list(head: ListNode) -> ListNode:
    if not head or not head.next:
        return head

    odd = head
    even_head = head.next
    even = even_head

    while even and even.next:
        odd.next = even.next
        odd = odd.next

        even.next = odd.next
        even = even.next

    # Connect the odd list to the even list
    odd.next = even_head

    return head

---

### 10. Remove Duplicates from Sorted DLL
`[EASY]` `#doubly-linked-list` `#deletion`

#### Problem Statement
Given a doubly linked list sorted in ascending order, delete all duplicate nodes.

#### Implementation Overview
Since the list is sorted, all duplicate nodes will be adjacent. We can solve this by traversing the list and checking if the current node's data is the same as the next node's data.

1.  Initialize a `current` pointer to the `head`.
2.  Traverse the list as long as `current` and `current.next` are not `None`.
3.  If `current.val == current.next.val`, a duplicate is found.
    -   The node `current.next` needs to be deleted.
    -   Store a reference to the node *after* the duplicate: `next_node = current.next.next`.
    -   Bypass the duplicate node: `current.next = next_node`.
    -   If `next_node` is not `None`, update its `prev` pointer to `current`.
4.  If the data is not the same, no duplicate is found at this position, so just move to the next node: `current = current.next`.

- **Time Complexity:** `O(N)`.
- **Space Complexity:** `O(1)`.

#### Python Code Snippet
```python
def remove_duplicates_sorted_dll(head: ListNode) -> ListNode:
    if not head or not head.next:
        return head

    current = head
    while current and current.next:
        if current.val == current.next.val:
            # Duplicate found, bypass the next node
            duplicate_node = current.next
            current.next = duplicate_node.next
            if duplicate_node.next:
                duplicate_node.next.prev = current
            # The 'current' pointer stays in place to check for more duplicates (e.g., 1->1->1)
        else:
            # No duplicate, move to the next node
            current = current.next

    return head
```

---

### 9. Add Two Numbers
`[MEDIUM]` `#reversal` `#linked-list` `#math`

#### Problem Statement
You are given two non-empty linked lists representing two non-negative integers. The digits are stored in **reverse order**, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list. (This is the easier version). A harder version has digits stored in forward order.

#### Implementation Overview (Reverse Order)
Since the digits are already in reverse order (least significant digit first), we can iterate through both lists simultaneously.
1.  **Initialize**: Create a dummy `head` for the result list and a `current` pointer. Initialize `carry = 0`.
2.  **Iterate and Add**:
    -   Loop as long as there are nodes in `l1`, `l2`, or there is a remaining `carry`.
    -   Get the values from the current nodes of `l1` and `l2` (if a list is exhausted, its value is `0`).
    -   Calculate `sum = val1 + val2 + carry`.
    -   Update `carry = sum // 10`.
    -   Create a new node with `sum % 10` and append it to the result list.
3.  **Return Result**: The final sum list is `dummy_head.next`.

- **Time Complexity:** `O(max(N, M))` where N and M are the lengths of the two lists.
- **Space Complexity:** `O(max(N, M))` for the result list.

#### Python Code Snippet
```python
def add_two_numbers(l1: ListNode, l2: ListNode) -> ListNode:
    dummy_head = ListNode(0)
    current = dummy_head
    carry = 0

    while l1 or l2 or carry:
        val1 = l1.val if l1 else 0
        val2 = l2.val if l2 else 0

        sum_val = val1 + val2 + carry
        carry = sum_val // 10
        digit = sum_val % 10

        current.next = ListNode(digit)
        current = current.next

        l1 = l1.next if l1 else None
        l2 = l2.next if l2 else None

    return dummy_head.next
```

---

### 8. Add 1 to a Number Represented by LL
`[MEDIUM]` `#reversal` `#linked-list` `#math`

#### Problem Statement
A non-negative integer is represented by a singly linked list of digits, where the head is the most significant digit. Add one to the number.

#### Implementation Overview
The main challenge is that addition starts from the least significant digit (the tail), but we only have access to the head. A common approach is to reverse the list.
1.  **Reverse the List**: Reverse the linked list first. This makes the tail node the head, which is where addition begins.
2.  **Add with Carry**:
    -   Traverse the reversed list. Start with a `carry` of `1`.
    -   For each node, calculate `sum = node.val + carry`.
    -   Update the node's value: `node.val = sum % 10`.
    -   Update the carry: `carry = sum // 10`. If `carry` becomes `0`, you can stop early.
3.  **Handle Final Carry**: If after the loop there is still a `carry`, create a new node with the carry value and append it to the end of the reversed list.
4.  **Reverse Back**: Reverse the list again to restore the original order.

- **Time Complexity:** `O(N)`.
- **Space Complexity:** `O(1)`.

#### Python Code Snippet
```python
def add_one(head: ListNode) -> ListNode:
    # 1. Reverse the list
    head = reverse_list_iterative(head) # Assume reverse_list_iterative is defined

    # 2. Add with carry
    current = head
    carry = 1
    while current and carry > 0:
        sum_val = current.val + carry
        current.val = sum_val % 10
        carry = sum_val // 10

        # If no more carry, we can stop
        if carry == 0:
            break

        # Move to next node, but handle final carry if it's the last node
        if not current.next and carry > 0:
            current.next = ListNode(carry)
            carry = 0 # End loop

        current = current.next

    # 4. Reverse back
    return reverse_list_iterative(head)
```

---

### 7. Sort a LL of 0s, 1s and 2s
`[MEDIUM]` `#rearrangement` `#linked-list`

#### Problem Statement
Given a linked list of `0`s, `1`s, and `2`s, sort it by modifying the links, not by swapping data.

#### Implementation Overview
This is similar to the Dutch National Flag problem for arrays. The idea is to create three separate lists for `0`s, `1`s, and `2`s, and then concatenate them.
1.  **Create Dummy Heads**: Create three dummy nodes (`zero_head`, `one_head`, `two_head`) to serve as the starting points for the three new lists. This simplifies handling empty sublists.
2.  **Create Tail Pointers**: Create three tail pointers (`zero_tail`, `one_tail`, `two_tail`) initialized to the dummy heads.
3.  **Iterate and Segregate**: Traverse the original list. For each node, append it to the appropriate tail pointer based on its value and advance that tail pointer.
4.  **Concatenate the Lists**:
    -   Connect the `zero` list to the `one` list (or the `two` list if the `one` list is empty).
    -   Connect the `one` list to the `two` list.
5.  **Terminate the Final List**: Set the `next` of the final tail (`two_tail`) to `None`.
6.  Return the head of the combined list, which is `zero_head.next`.

- **Time Complexity:** `O(N)`.
- **Space Complexity:** `O(1)` as we re-use existing nodes.

#### Python Code Snippet
```python
def sort_list_of_012(head: ListNode) -> ListNode:
    if not head or not head.next:
        return head

    zero_head = ListNode(0)
    one_head = ListNode(0)
    two_head = ListNode(0)
    zero_tail, one_tail, two_tail = zero_head, one_head, two_head

    curr = head
    while curr:
        if curr.val == 0:
            zero_tail.next = curr
            zero_tail = zero_tail.next
        elif curr.val == 1:
            one_tail.next = curr
            one_tail = one_tail.next
        else:
            two_tail.next = curr
            two_tail = two_tail.next
        curr = curr.next

    # Concatenate lists
    one_tail.next = two_head.next
    zero_tail.next = one_head.next if one_head.next else two_head.next
    two_tail.next = None

    return zero_head.next
```
```
```
