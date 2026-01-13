# Pattern 3: Hashing & Prefix Aggregates

This pattern leverages hash-based data structures (Hashmaps/Dictionaries and Hash Sets) to solve problems, typically in O(N) time. The two main uses are:
1.  **Lookups and Frequency Counting:** Using a hashmap or hash set to store information about elements (e.g., their counts, indices, or just existence) for quick O(1) average time lookups.
2.  **Prefix Aggregates:** Using a hashmap to store the cumulative sum (or XOR, product, etc.) calculated from the start of the array up to a certain index. This is extremely powerful for solving subarray problems. If the prefix sum up to index `i` is `P[i]` and up to `j` is `P[j]`, the sum of the subarray between `i` and `j` is `P[j] - P[i]`. Hashing allows us to instantly look up if a required complementary prefix sum exists.

---

### 14. Longest subarray with sum K (Positives + Negatives)
`[MEDIUM]` `#hashing` `#prefix-sum`

#### Problem Statement
Given an array of integers (which can be positive, negative, or zero) and an integer `K`, find the length of the longest subarray with a sum equal to `K`.

*Example:*
- **Input:** `arr = [10, 5, 2, 7, 1, 9]`, `K = 15`
- **Output:** `4` (The subarray is `[5, 2, 7, 1]`)
- **Input:** `arr = [-1, 1, 1]`, `K = 1`
- **Output:** `2` (The subarray is `[1, 1]`)

#### Implementation Overview
The sliding window technique fails here because negative numbers disrupt the monotonic nature of the sum. The optimal solution uses a hashmap to store prefix sums.
1.  Initialize `current_sum = 0`, `max_len = 0`.
2.  Create a hashmap `prefix_sum_map` to store `{prefix_sum: index}`.
3.  Iterate through the array with index `i`:
    -   Update `current_sum += arr[i]`.
    -   If `current_sum == K`, we have a subarray from the start to `i`, so `max_len = max(max_len, i + 1)`.
    -   We are looking for a subarray that ends at `i` with sum `K`. This means we need to find a prior prefix sum, `required_sum`, such that `current_sum - required_sum = K`. This rearranges to `required_sum = current_sum - K`.
    -   Check if `required_sum` exists in `prefix_sum_map`. If it does, we've found a subarray. The length is `i - prefix_sum_map[required_sum]`. Update `max_len` with this length if it's greater.
    -   If the `current_sum` is not already in the map, add it: `prefix_sum_map[current_sum] = i`. We only add it if it's new because we want the *earliest* index for a given prefix sum to maximize the subarray length.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the size of the array. We iterate through the array once.
- **Space Complexity:** $O(N)$, as we use a hashmap to store prefix sums. In the worst case, all prefix sums are distinct.

#### Python Code Snippet
```python
def longest_subarray_with_sum_k_negatives(arr, k):
    prefix_sum_map = {0: -1} # Initialize with sum 0 at index -1 to handle subarrays starting from index 0
    current_sum = 0
    max_len = 0

    for i, num in enumerate(arr):
        current_sum += num

        required_sum = current_sum - k
        if required_sum in prefix_sum_map:
            max_len = max(max_len, i - prefix_sum_map[required_sum])

        # Store the current prefix sum if it's not already there
        # We don't update it if it exists because we want the longest subarray,
        # which means we need the earliest possible start index.
        if current_sum not in prefix_sum_map:
            prefix_sum_map[current_sum] = i

    return max_len
```

#### Tricks/Gotchas
- **Zero Sum Initialization:** Initializing the map with `{0: -1}` elegantly handles cases where the subarray with sum `K` starts from index 0.
- **Why not update map entry?** For the *longest* subarray, we need the prefix sum that occurred the furthest back in the array, so we never update an existing entry in the map.

#### Related Problems
- 13. Longest subarray with given sum K (positives)
- 28. Count subarrays with given sum
- 33. Largest Subarray with 0 Sum

---

### 24. Longest Consecutive Sequence in an Array
`[MEDIUM]` `#hashing` `#hash-set`

#### Problem Statement
Given an unsorted array of integers, find the length of the longest consecutive elements sequence. The sequence can be in any order in the input array.

*Example:*
- **Input:** `nums = [100, 4, 200, 1, 3, 2]`
- **Output:** `4` (The longest consecutive sequence is `[1, 2, 3, 4]`)

#### Implementation Overview
A naive solution is to sort the array (O(N log N)) and then iterate. The optimal O(N) solution uses a hash set for fast lookups.
1.  Insert all elements of the array into a hash set for O(1) average time lookups.
2.  Initialize `max_length = 0`.
3.  Iterate through each number `num` in the set.
4.  For each `num`, check if `num - 1` exists in the hash set.
    -   If `num - 1` **is** in the set, it means `num` is not the start of a consecutive sequence, so we can skip it. This is the key optimization.
    -   If `num - 1` **is not** in the set, then `num` is the potential start of a sequence.
5.  If we've found a start, we begin counting. Initialize `current_length = 1` and `current_num = num`.
6.  In a `while` loop, check if `current_num + 1` exists in the set. If it does, increment `current_length` and `current_num`.
7.  After the inner loop, update `max_length = max(max_length, current_length)`.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the number of elements in the array. Although there is a `while` loop inside the `for` loop, each number is visited at most twice.
- **Space Complexity:** $O(N)$, as we store the elements in a hash set.

#### Python Code Snippet
```python
def longest_consecutive_sequence(nums):
    if not nums:
        return 0

    num_set = set(nums)
    max_length = 0

    for num in num_set:
        # Check if it's the start of a sequence
        if num - 1 not in num_set:
            current_num = num
            current_length = 1

            while current_num + 1 in num_set:
                current_num += 1
                current_length += 1

            max_length = max(max_length, current_length)

    return max_length
```

#### Tricks/Gotchas
- **O(N) Complexity:** This algorithm is O(N) because each number is effectively processed at most twice (once by the outer `for` loop, and at most once by the inner `while` loop across the entire execution). The `if num - 1 not in num_set` check ensures we only start counting from the absolute beginning of any sequence.

#### Related Problems
- None in this list.

---

### 28. Count subarrays with given sum
`[MEDIUM]` `#hashing` `#prefix-sum`

#### Problem Statement
Given an array of integers and an integer `K`, find the total number of continuous subarrays whose sum equals `K`.

*Example:*
- **Input:** `nums = [1, 1, 1]`, `k = 2`
- **Output:** `2` (The subarrays are `[1, 1]` starting at index 0 and `[1, 1]` starting at index 1)

#### Implementation Overview
This is a classic variation of the prefix sum pattern. Instead of finding the max length, we count all occurrences.
1.  Initialize `count = 0`, `current_sum = 0`.
2.  Create a hashmap `prefix_sum_map` to store `{prefix_sum: frequency}`.
3.  **Crucial Initialization:** Put `prefix_sum_map[0] = 1`. This handles cases where a subarray with sum `K` starts from index 0.
4.  Iterate through the array:
    -   Update `current_sum += num`.
    -   We need to find how many times a `prefix_sum` equal to `current_sum - K` has occurred before. Let this be `required_sum`.
    -   Add the frequency of `required_sum` from the map to our `count`: `count += prefix_sum_map.get(required_sum, 0)`.
    -   Update the frequency of the `current_sum` in the map: `prefix_sum_map[current_sum] = prefix_sum_map.get(current_sum, 0) + 1`.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the size of the array. We traverse the array once.
- **Space Complexity:** $O(N)$, as we use a hashmap to store prefix sum frequencies.

#### Python Code Snippet
```python
def subarray_sum_count(nums, k):
    count = 0
    current_sum = 0
    prefix_sum_map = {0: 1}  # {prefix_sum: frequency}

    for num in nums:
        current_sum += num
        required_sum = current_sum - k

        count += prefix_sum_map.get(required_sum, 0)

        prefix_sum_map[current_sum] = prefix_sum_map.get(current_sum, 0) + 1

    return count
```

#### Tricks/Gotchas
- **`{0: 1}` Initialization:** Forgetting to initialize the map with a prefix sum of 0 having a frequency of 1 is the most common mistake. It correctly counts subarrays that start from the beginning of the array whose sum is exactly `K`.

#### Related Problems
- 14. Longest subarray with sum K (Positives + Negatives)
- 33. Largest Subarray with 0 Sum
- 34. Count number of subarrays with given xor K

---

### 33. Largest Subarray with 0 Sum
`[MEDIUM]` `#hashing` `#prefix-sum`

#### Problem Statement
Given an array of integers, find the length of the longest subarray with a sum of 0.

*Example:*
- **Input:** `arr = [15, -2, 2, -8, 1, 7, 10, 23]`
- **Output:** `5` (The subarray is `[-2, 2, -8, 1, 7]`)

#### Implementation Overview
This is a direct application of the "Longest subarray with sum K" pattern, where `K` is specifically 0.
1.  The logic is that if we encounter the same prefix sum twice, say at index `i` and `j` (`j > i`), then the sum of the elements in the subarray `(i, j]` must be 0.
2.  Initialize `max_len = 0`, `current_sum = 0`.
3.  Create a hashmap `prefix_sum_map` to store `{prefix_sum: index}`.
4.  Iterate through the array with index `i`:
    -   Update `current_sum += arr[i]`.
    -   If `current_sum == 0`, the subarray from the start `[0...i]` has a sum of 0. Update `max_len = i + 1`.
    -   If `current_sum` is already in `prefix_sum_map`, it means the subarray between the previous occurrence and the current one has a sum of 0. Calculate its length `i - prefix_sum_map[current_sum]` and update `max_len`.
    -   If `current_sum` is not in the map, store its first occurrence: `prefix_sum_map[current_sum] = i`.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the size of the array. We traverse the array once.
- **Space Complexity:** $O(N)$, as we use a hashmap to store prefix sums.

#### Python Code Snippet
```python
def largest_subarray_with_zero_sum(arr):
    prefix_sum_map = {0: -1} # Initialize with sum 0 at index -1
    current_sum = 0
    max_len = 0

    for i, num in enumerate(arr):
        current_sum += num

        if current_sum in prefix_sum_map:
            max_len = max(max_len, i - prefix_sum_map[current_sum])
        else:
            # Store the first time we see this prefix sum
            prefix_sum_map[current_sum] = i

    return max_len
```

#### Tricks/Gotchas
- **Identical Logic:** This is exactly problem #14 with `K=0`. Recognizing this pattern is key. The `{0: -1}` initialization handles cases where the longest zero-sum subarray starts from index 0.

#### Related Problems
- 14. Longest subarray with sum K (Positives + Negatives)
- 28. Count subarrays with given sum

---

### 34. Count number of subarrays with given xor K
`[MEDIUM]` `#hashing` `#prefix-xor`

#### Problem Statement
Given an array of integers and an integer `K`, find the total number of subarrays with a bitwise XOR of all elements equal to `K`.

*Example:*
- **Input:** `arr = [4, 2, 2, 6, 4]`, `K = 6`
- **Output:** `4` (Subarrays are `[6]`, `[4, 2]`, `[2, 2, 6]`, and `[4, 2, 2, 6, 4]`)

#### Implementation Overview
This problem is analogous to "Count subarrays with given sum," but it uses the properties of XOR instead of arithmetic sum.
- The key property is: if `prefix_xor[j] ^ prefix_xor[i] = K`, then `prefix_xor[j] ^ K = prefix_xor[i]`.
1.  Initialize `count = 0`, `current_xor = 0`.
2.  Create a hashmap `prefix_xor_map` to store `{prefix_xor: frequency}`.
3.  Initialize `prefix_xor_map[0] = 1` to handle subarrays starting at index 0 whose XOR is `K`.
4.  Iterate through the array:
    -   Update `current_xor ^= num`.
    -   We need to find a previous `prefix_xor` that satisfies the property. Let this be `required_xor = current_xor ^ K`.
    -   Look up `required_xor` in the map and add its frequency to `count`.
    -   Update the frequency of `current_xor` in the map.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the size of the array. We traverse the array once.
- **Space Complexity:** $O(N)$, as we use a hashmap to store prefix XOR frequencies.

#### Python Code Snippet
```python
def subarrays_with_xor_k(arr, k):
    count = 0
    current_xor = 0
    prefix_xor_map = {0: 1}  # {prefix_xor: frequency}

    for num in arr:
        current_xor ^= num
        required_xor = current_xor ^ k

        count += prefix_xor_map.get(required_xor, 0)

        prefix_xor_map[current_xor] = prefix_xor_map.get(current_xor, 0) + 1

    return count
```

#### Tricks/Gotchas
- **XOR Properties:** Understanding the properties of XOR is essential. The logic is a direct parallel to the prefix sum version.
- **`{0: 1}` Initialization:** Just like the sum version, this initialization is critical.

#### Related Problems
- 28. Count subarrays with given sum

---

### 37. Find the repeating and missing number
`[MEDIUM]` `#hashing` `#math` `#bitwise`

#### Problem Statement
You are given a read-only array of `N` integers from 1 to `N`. One number is repeated twice, and one number is missing. Find these two numbers.

*Example:*
- **Input:** `arr = [3, 1, 2, 5, 3]` (`N=5`)
- **Output:** Repeating = `3`, Missing = `4`

#### Implementation Overview
There are several ways to solve this (math equations, XOR), but a hash-based approach is straightforward and intuitive.
1.  **Frequency Counting:** Use a hashmap or a frequency array to count the occurrences of each number in the input array.
2.  Iterate through the input `arr`. For each `num`, increment its count in the frequency map.
3.  After populating the map, iterate from `1` to `N`.
4.  Check the frequency of each number `i` in this range:
    -   If the frequency of `i` is `2`, then `i` is the repeating number.
    -   If `i` is not in the map, then `i` is the missing number.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the size of the array. We iterate through the array once and then through the range $1$ to $N$.
- **Space Complexity:** $O(N)$, as we use a hashmap (or frequency array) to store counts.

#### Python Code Snippet
```python
def find_repeating_and_missing(arr):
    n = len(arr)
    counts = {}
    for num in arr:
        counts[num] = counts.get(num, 0) + 1

    repeating, missing = -1, -1
    for i in range(1, n + 1):
        count = counts.get(i, 0)
        if count == 2:
            repeating = i
        elif count == 0:
            missing = i

    return repeating, missing
```

#### Tricks/Gotchas
- **Multiple Solutions:** This problem is famous for having multiple solutions with different trade-offs.
    - **Math Approach (O(N) time, O(1) space):** Involves setting up two equations based on the sum of numbers and the sum of squares of numbers from 1 to N. It can be prone to integer overflow.
    - **XOR Approach (O(N) time, O(1) space):** A clever but complex method involving XORing all array elements and numbers from 1 to N, then partitioning the numbers based on a set bit to isolate the repeating and missing values.
- **Constraints:** The hash-based solution is excellent unless there's a strict O(1) space constraint.

#### Related Problems
- 10. Find missing number in an array
- 12. Find the number that appears once, and other numbers twice.
