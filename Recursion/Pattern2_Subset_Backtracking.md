### `[PATTERN] Recursion with Backtracking`

**Backtracking** is an algorithmic technique for solving problems recursively by trying to build a solution incrementally, one piece at a time. It removes those solutions that fail to satisfy the constraints of the problem at any point in time.

Think of it like navigating a maze. You explore one path. If you hit a dead end, you "backtrack" to the last junction and try a different path.

#### The Backtracking Template
Most backtracking problems can be solved using a common template:

```python
def backtrack(current_state, other_params):
    # Base Case: If the current state is a valid solution, add it to results.
    if is_a_solution(current_state):
        add_to_solutions(current_state)
        return

    # Iterate through all possible choices from the current state.
    for choice in all_possible_choices():
        # 1. Make a choice
        # Apply the choice to the current state.
        make_choice(choice)

        # 2. Recurse
        # Call the function with the updated state.
        backtrack(updated_state, other_params)

        # 3. Backtrack (Undo the choice)
        # Revert the state to what it was before making the choice.
        # This is the crucial step that allows exploring other paths.
        undo_choice(choice)
```

This pattern is powerful for solving problems related to permutations, combinations, subsets, and pathfinding.

---

### 1. Subsets (Power Set)
`[MEDIUM]` `#backtracking` `#subsets`

#### Problem Statement
Given an integer array `nums` of **unique** elements, return all possible subsets (the power set). The solution set must not contain duplicate subsets.

#### Implementation Overview
This is the canonical "pick / don't pick" backtracking problem. For each element in `nums`, we have two choices: either include it in our current subset or not include it.

- **Choice**: For each element, do we add it to the current subset?
- **State**: The current subset being built and the current index in `nums` we are considering.
- **Goal**: We have considered every element. Every state we reach is a valid subset.

#### Time and Space Complexity
- **Time Complexity:** $O(2^N \cdot N)$, where $N$ is the number of elements. There are $2^N$ subsets, and adding a subset to the result takes $O(N)$ time.
- **Space Complexity:** $O(N)$ for the recursion stack and current subset.

#### Python Code Snippet
```python
def subsets(nums: list[int]) -> list[list[int]]:
    result = []
    current_subset = []

    def backtrack(index):
        # Base Case: Add the current subset configuration to the result.
        # This is a valid subset at every step.
        result.append(list(current_subset))

        # Explore choices for the remaining elements.
        for i in range(index, len(nums)):
            # 1. Make a choice: Include nums[i]
            current_subset.append(nums[i])

            # 2. Recurse: Explore further with this choice
            backtrack(i + 1)

            # 3. Backtrack: Undo the choice (remove nums[i])
            current_subset.pop()

    backtrack(0)
    return result
```

---

### 2. Subsets II (Contains Duplicates)
`[MEDIUM]` `#backtracking` `#subsets`

#### Problem Statement
Given an integer array `nums` that **may contain duplicates**, return all possible subsets (the power set). The solution set must not contain duplicate subsets.

#### Implementation Overview
This is a variation of the Subsets problem. To avoid duplicate subsets, we must handle the duplicate numbers in the input.
1.  **Sort the input array**: Sorting `nums` brings all duplicate elements together.
2.  **Modify the loop**: In the backtracking function, when we iterate through our choices, we add a condition: if the current element is the same as the previous one, and we are not at the beginning of the choices for this level, we **skip** it. This ensures that for a group of identical elements, we only pick the first one to start a new path, preventing duplicate subsets.

#### Time and Space Complexity
- **Time Complexity:** $O(2^N \cdot N)$, similar to the basic subsets problem.
- **Space Complexity:** $O(N)$ for the recursion stack.

#### Python Code Snippet
```python
def subsets_with_dup(nums: list[int]) -> list[list[int]]:
    result = []
    current_subset = []
    nums.sort()  # Sort to handle duplicates

    def backtrack(index):
        result.append(list(current_subset))

        for i in range(index, len(nums)):
            # **The crucial part to avoid duplicates**
            # If the current element is the same as the previous one,
            # and we are not considering it for the first time in this level, skip it.
            if i > index and nums[i] == nums[i - 1]:
                continue

            current_subset.append(nums[i])
            backtrack(i + 1)
            current_subset.pop()

    backtrack(0)
    return result
```

---

### 3. Combination Sum
`[MEDIUM]` `#backtracking` `#combinations`

#### Problem Statement
Given an array of **distinct** integers `candidates` and a target integer `target`, return a list of all **unique combinations** of `candidates` where the chosen numbers sum to `target`. You may return the combinations in any order. The **same number may be chosen from `candidates` an unlimited number of times**.

#### Implementation Overview
This is a classic backtracking problem where we explore combinations that sum to a target.
- **Choice**: At each step, we can either choose the current candidate again (if the sum doesn't exceed the target) or move to the next candidate.
- **State**: The current combination, the current sum, and the index of the candidate we are considering.
- **Goal**: The current sum equals the `target`.

#### Time and Space Complexity
- **Time Complexity:** $O(K \cdot 2^T)$, where $T$ is the target value and $K$ is the average length of a combination. The number of combinations is loosely bounded by $2^T$ in the worst case (e.g., all candidates are 1).
- **Space Complexity:** $O(T)$ for the recursion stack (depth can go up to `target` if 1 is a candidate).

#### Python Code Snippet
```python
def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    result = []

    def backtrack(start_index, current_combination, current_sum):
        # Base Case: Successful solution
        if current_sum == target:
            result.append(list(current_combination))
            return

        # Base Case: Pruning - path is no longer viable
        if current_sum > target:
            return

        # Explore choices
        for i in range(start_index, len(candidates)):
            candidate = candidates[i]

            # 1. Make a choice
            current_combination.append(candidate)

            # 2. Recurse
            # We pass `i` instead of `i + 1` because we can reuse the same element.
            backtrack(i, current_combination, current_sum + candidate)

            # 3. Backtrack
            current_combination.pop()

    backtrack(0, [], 0)
    return result
```

---

### 4. Combination Sum II (No Duplicate Combinations)
`[MEDIUM]` `#backtracking` `#combinations`

#### Problem Statement
Given a collection of candidate numbers `candidates` (which **may contain duplicates**) and a target integer `target`, find all **unique combinations** in `candidates` where the candidate numbers sum to `target`. **Each number in `candidates` may only be used once** in the combination.

#### Implementation Overview
This problem has two key differences from Combination Sum I:
1.  Each candidate can be used only once.
2.  The input array can have duplicates, but the result should not have duplicate combinations.

This combination of constraints leads to a solution similar to Subsets II.
1.  **Sort the input**: Sort `candidates` to group duplicates.
2.  **Use each element once**: In the recursive call, pass `i + 1` as the next starting index, not `i`. This prevents reusing the same element.
3.  **Skip duplicates**: Just like in Subsets II, in the choice-making loop, if `i > start_index` and `candidates[i] == candidates[i - 1]`, we `continue`. This prevents creating duplicate combinations like `[1, 7]` and `[1, 7]` when the input is `[1, 1, 7]`.

#### Time and Space Complexity
- **Time Complexity:** $O(2^N \cdot N)$, similar to subsets.
- **Space Complexity:** $O(N)$ for recursion stack.

#### Python Code Snippet
```python
def combination_sum2(candidates: list[int], target: int) -> list[list[int]]:
    result = []
    candidates.sort()

    def backtrack(start_index, current_combination, current_sum):
        if current_sum == target:
            result.append(list(current_combination))
            return

        if current_sum > target:
            return

        for i in range(start_index, len(candidates)):
            # Skip duplicates to avoid duplicate combinations
            if i > start_index and candidates[i] == candidates[i - 1]:
                continue

            candidate = candidates[i]

            # Pruning: if the current candidate is too large, the rest will be too.
            if current_sum + candidate > target:
                break

            current_combination.append(candidate)
            # Recurse with `i + 1` because each number can be used only once.
            backtrack(i + 1, current_combination, current_sum + candidate)
            current_combination.pop()

    backtrack(0, [], 0)
    return result
```

---

### 5. Generate Parentheses
`[MEDIUM]` `#backtracking` `#string-generation`

#### Problem Statement
Given `n` pairs of parentheses, write a function to generate all combinations of well-formed parentheses.

#### Implementation Overview
We build the string character by character, and at each step, we have two choices: add a '(' or add a ')'. However, we must follow constraints.
- **State**: The current string being built, the number of open parentheses used (`open_count`), and the number of closed parentheses used (`close_count`).
- **Choices & Constraints**:
    1. We can add an open parenthesis `(` if `open_count < n`.
    2. We can add a closed parenthesis `)` if `close_count < open_count`. This is the key constraint that ensures the parentheses are well-formed.
- **Goal**: The length of the string is `2 * n`.

#### Time and Space Complexity
- **Time Complexity:** $O(\frac{4^n}{\sqrt{n}})$, which is related to the nth Catalan number.
- **Space Complexity:** $O(n)$ for the recursion stack.

#### Python Code Snippet
```python
def generate_parenthesis(n: int) -> list[str]:
    result = []

    def backtrack(current_string, open_count, close_count):
        # Base Case: A valid solution is found
        if len(current_string) == 2 * n:
            result.append(current_string)
            return

        # Choice 1: Add an open parenthesis
        if open_count < n:
            backtrack(current_string + "(", open_count + 1, close_count)

        # Choice 2: Add a closed parenthesis
        if close_count < open_count:
            backtrack(current_string + ")", open_count, close_count + 1)

    backtrack("", 0, 0)
    return result

---

### 10. Combination Sum III
`[MEDIUM]` `#recursion` `#backtracking` `#combinations`

#### Problem Statement
Find all valid combinations of `k` numbers that sum up to `n` such that:
- Only numbers from 1 to 9 are used.
- Each number is used at most once.

#### Implementation Overview
This is a highly constrained combination sum problem.
1.  **Recursive Function**: `find_combinations(start_num, k, n, current_combination)`
2.  **Base Case**:
    - If `len(current_combination) == k` and `n == 0`, we have found a valid combination.
    - Return if `n < 0` or `len(current_combination) == k`.
3.  **Recursive Step**:
    - Iterate from `start_num` to 9.
    - For each number `i`, add it to the combination and recurse with `find_combinations(i + 1, k, n - i, ...)`. We use `i + 1` as the next start because each number can be used at most once.
    - Backtrack by removing `i`.

#### Time and Space Complexity
- **Time Complexity:** $O(9^K \cdot K)$, effectively constant since the range of numbers (1-9) is small and fixed.
- **Space Complexity:** $O(K)$ for the recursion stack.

#### Python Code Snippet
```python
def combination_sum_3(k: int, n: int) -> list[list[int]]:
    result = []

    def backtrack(start_num, remaining_k, remaining_n, current_combo):
        if remaining_k == 0 and remaining_n == 0:
            result.append(list(current_combo))
            return

        if remaining_k == 0 or remaining_n < 0:
            return

        for i in range(start_num, 10):
            current_combo.append(i)
            backtrack(i + 1, remaining_k - 1, remaining_n - i, current_combo)
            current_combo.pop()

    backtrack(1, k, n, [])
    return result
```

---

### 9. Subset Sum I
`[EASY]` `#recursion` `#backtracking` `#subsequences`

#### Problem Statement
Given a list of `N` integers, find the sum of all the subsets in it.

#### Implementation Overview
This is a direct application of the "pick/don't-pick" pattern. We generate all subsets and record the sum of each one.
1.  **Recursive Function**: `find_sums(index, current_sum)`
2.  **Base Case**: When `index` reaches the end of the array, `current_sum` represents the sum of one complete subset. Add this sum to the result list.
3.  **Recursive Step**: At `index`:
    -   **Pick**: Make a recursive call for the next index with an updated sum: `find_sums(index + 1, current_sum + arr[index])`.
    -   **Don't-Pick**: Make a recursive call for the next index with the same sum: `find_sums(index + 1, current_sum)`.

#### Time and Space Complexity
- **Time Complexity:** $O(2^N)$.
- **Space Complexity:** $O(N)$ for recursion stack.

#### Python Code Snippet
```python
def subset_sums(arr: list[int]) -> list[int]:
    result = []
    def find_sums(index, current_sum):
        if index == len(arr):
            result.append(current_sum)
            return

        # Pick the element
        find_sums(index + 1, current_sum + arr[index])

        # Don't pick the element
        find_sums(index + 1, current_sum)

    find_sums(0, 0)
    return sorted(result)
```

---

### 8. Check if there exists a Subsequence with Sum K
`[MEDIUM]` `#recursion` `#backtracking` `#subsequences`

#### Problem Statement
Given an array of non-negative integers `arr` and a target sum `K`, determine if there is a subsequence of `arr` with a sum equal to `K`.

#### Implementation Overview
This is a decision-based version of the previous problem. We just need to find one valid subsequence. The recursive function can return a boolean.
1.  **Recursive Function**: `check_sum(index, target)`
2.  **Base Case**:
    - If `target == 0`, we have found a valid subsequence. Return `True`.
    - If `index` reaches the end of the array (and `target` is not 0), this path is a dead end. Return `False`.
3.  **Recursive Step**: At `index`:
    -   **Pick**: If `arr[index] <= target`, make a recursive call `check_sum(index + 1, target - arr[index])`. If this call returns `True`, return `True`.
    -   **Don't-Pick**: If the "pick" path didn't return `True`, explore the "don't-pick" path: `check_sum(index + 1, target)`.
    -   The result is `pick_result or dont_pick_result`.

#### Time and Space Complexity
- **Time Complexity:** $O(2^N)$ in the worst case (without memoization).
- **Space Complexity:** $O(N)$ for recursion stack.

#### Python Code Snippet
```python
def check_if_subsequence_sum_exists(arr: list[int], k: int) -> bool:
    def solve(index, target):
        if target == 0:
            return True
        if index == len(arr):
            return False

        # Don't pick
        dont_pick_result = solve(index + 1, target)
        if dont_pick_result:
            return True

        # Pick
        pick_result = False
        if arr[index] <= target:
            pick_result = solve(index + 1, target - arr[index])

        return pick_result

    return solve(0, k)
```

---

### 7. Count all Subsequences with Sum K
`[MEDIUM]` `#recursion` `#backtracking` `#subsequences`

#### Problem Statement
Given an array of integers `arr` and an integer `K`, count the total number of subsequences of `arr` that sum up to `K`.

#### Implementation Overview
This is a "pick/don't-pick" problem where the recursive function returns the count of valid subsequences found from its state.
1.  **Recursive Function**: `count_subsequences(index, current_sum)`
2.  **Base Case**: When `index` reaches the end of the array:
    - If `current_sum == K`, we have found one valid subsequence. Return 1.
    - Otherwise, return 0.
3.  **Recursive Step**: At `index`:
    -   **Pick**: Call `count_subsequences(index + 1, current_sum + arr[index])`.
    -   **Don't-Pick**: Call `count_subsequences(index + 1, current_sum)`.
    -   The total count is the sum of the results from both calls.

#### Time and Space Complexity
- **Time Complexity:** $O(2^N)$.
- **Space Complexity:** $O(N)$ for recursion stack.

#### Python Code Snippet
```python
def count_subsequences_with_sum_k(arr: list[int], k: int) -> int:
    def solve(index, current_sum):
        if index == len(arr):
            return 1 if current_sum == k else 0

        # Pick the element
        pick_count = solve(index + 1, current_sum + arr[index])

        # Don't pick the element
        dont_pick_count = solve(index + 1, current_sum)

        return pick_count + dont_pick_count

    return solve(0, 0)
```

---

### 6. Generate all Binary Strings
`[EASY]` `#recursion` `#backtracking`

#### Problem Statement
Given a positive integer `N`, generate all possible binary strings of length `N`.

#### Implementation Overview
For each position in the string, we have two choices: '0' or '1'. We can use recursion to explore these choices.
1.  **Recursive Function**: `generate(index, current_string)`
2.  **Base Case**: When `index == N`, a complete string has been formed. Add it to results.
3.  **Recursive Step**:
    -   Call `generate(index + 1, current_string + '0')`.
    -   Call `generate(index + 1, current_string + '1')`.

#### Time and Space Complexity
- **Time Complexity:** $O(2^N)$.
- **Space Complexity:** $O(N)$ for recursion stack.

#### Python Code Snippet
```python
def generate_binary_strings(N: int) -> list[str]:
    result = []
    def generate(index, current_string):
        if index == N:
            result.append(current_string)
            return

        generate(index + 1, current_string + '0')
        generate(index + 1, current_string + '1')

    generate(0, "")
    return result
```
```
