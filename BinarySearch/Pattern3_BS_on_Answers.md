# Pattern 3: Binary Search on the Answer Space

This is a powerful and often non-obvious application of binary search. Instead of searching on the array indices for a value, we define a search space for the **answer** itself and use binary search to find the most optimal answer.

The key is to find a **monotonic** property for the answer. For example, in a minimization problem, if we can achieve the goal with a value `k`, we can also achieve it with any value greater than `k`. This allows us to discard half of the search space.

The core structure is:
1.  Define a search space `[low, high]` for the possible answers. This range is determined by the problem's constraints.
2.  Write a predicate function `is_possible(value)` that returns `True` if an answer of `value` can satisfy the problem's constraints, and `False` otherwise.
3.  Use a standard binary search template on the `[low, high]` range.
    -   If `is_possible(mid)` is true, it means `mid` is a potential answer. We try for a "better" one (e.g., smaller for minimization, larger for maximization) by adjusting our search space.
    -   If `is_possible(mid)` is false, `mid` is not a valid answer, and we must search in the other half.

---

### 1. Find Square Root of a Number
`[EASY]` `#binary-search-on-answer`

#### Problem Statement
Given a non-negative integer `x`, compute and return the square root of `x`. Since the return type is an integer, the decimal digits are truncated, and only the integer part of the root is returned.

*Example:*
- **Input:** `x = 8`
- **Output:** `2` (The square root of 8 is 2.828..., and the integer part is 2).
- **Input:** `x = 16`
- **Output:** `4`

#### Implementation Overview
1.  **Search Space:** The square root of `x` must lie between `1` and `x`. So, `low = 1`, `high = x`.
2.  **Binary Search:** We search for the largest integer `mid` such that `mid * mid <= x`.
    -   If `mid * mid > x`, our guess `mid` is too high. We discard the right half: `high = mid - 1`.
    -   If `mid * mid <= x`, `mid` is a potential answer. We store it and try to find a larger root that also satisfies the condition: `ans = mid`, `low = mid + 1`.

#### Python Code Snippet
```python
def my_sqrt(x):
    if x == 0: return 0
    low, high = 1, x
    ans = 0
    while low <= high:
        mid = low + (high - low) // 2
        if mid * mid > x:
            high = mid - 1
        else:
            # mid is a potential answer, try for a larger one
            ans = mid
            low = mid + 1
    return ans
```

#### Tricks/Gotchas
- **Edge Cases:** Handle `x = 0` separately.
- **Integer Overflow:** `mid * mid` can overflow in some languages if `x` is very large. An alternative is to check `if mid > x / mid`.

---

### 2. Find the Nth Root of a Number
`[MEDIUM]` `#binary-search-on-answer`

#### Problem Statement
Given two positive integers `n` and `m`, find the `n`-th root of `m`. You need to return the integer part of the `n`-th root.

*Example:*
- **Input:** `n = 3`, `m = 27`
- **Output:** `3`
- **Input:** `n = 4`, `m = 69`
- **Output:** `2` (Since 2^4=16 and 3^4=81)

#### Implementation Overview
This is a direct extension of the square root problem.
1.  **Search Space:** The answer is between `1` and `m`. So, `low = 1`, `high = m`.
2.  **Binary Search:** We search for the largest integer `mid` such that `mid^n <= m`.
    -   If `mid^n > m`, the guess `mid` is too high (`high = mid - 1`).
    -   If `mid^n <= m`, `mid` is a potential answer, so we store it and search for a larger one (`ans = mid`, `low = mid + 1`).

#### Python Code Snippet
```python
def nth_root(n, m):
    low, high = 1, m
    ans = -1
    while low <= high:
        mid = low + (high - low) // 2
        # Using a helper to check for overflow is safer
        # For this example, we assume Python's arbitrary precision integers
        try:
            val = mid ** n
        except OverflowError:
            val = float('inf')

        if val > m:
            high = mid - 1
        else:
            ans = mid
            low = mid + 1
    return ans
```

---

### 3. Koko Eating Bananas
`[MEDIUM]` `#binary-search-on-answer` `#minimization`

#### Problem Statement
Koko loves to eat bananas. There are `n` piles of bananas, the `i`-th pile has `piles[i]` bananas. She can decide her bananas-per-hour eating speed of `k`. Each hour, she chooses some pile and eats `k` bananas. If the pile has less than `k` bananas, she eats all of them instead and will not eat any more bananas during that hour. Koko wants to finish all the bananas within `h` hours. Return the minimum integer eating speed `k` such that she can eat all the bananas within `h` hours.

*Example:*
- **Input:** `piles = [3,6,7,11]`, `h = 8`
- **Output:** `4`

#### Implementation Overview
1.  **Search Space:** The minimum possible speed is 1. The maximum possible speed is `max(piles)` (any higher speed is redundant). So, `low = 1`, `high = max(piles)`.
2.  **Predicate `is_possible(k)`:** Can Koko finish in `h` hours with speed `k`? Calculate the total hours needed: `total_hours = sum(math.ceil(pile / k) for pile in piles)`. Return `total_hours <= h`.
3.  **Binary Search:** We want to find the minimum `k`.
    -   If `is_possible(mid)` is true, `mid` is a valid speed. We store it and try for an even smaller speed: `ans = mid`, `high = mid - 1`.
    -   If `is_possible(mid)` is false, the speed `mid` is too slow. We must search for a higher speed: `low = mid + 1`.

#### Python Code Snippet
```python
import math
def koko_eating_bananas(piles, h):
    low, high = 1, max(piles)
    ans = high

    def is_possible(k):
        hours_needed = 0
        for pile in piles:
            hours_needed += math.ceil(pile / k)
        return hours_needed <= h

    while low <= high:
        mid = low + (high - low) // 2
        if is_possible(mid):
            ans = mid
            high = mid - 1
        else:
            low = mid + 1
    return ans
```

---

### 4. Minimum Days to Make M Bouquets
`[MEDIUM]` `#binary-search-on-answer` `#minimization`

#### Problem Statement
Given an integer array `bloomDay`, an integer `m` and an integer `k`. You want to make `m` bouquets. To make a bouquet, you need to use `k` **adjacent** flowers that have bloomed. The `i`-th flower will bloom on `bloomDay[i]`. Return the minimum number of days you have to wait to be able to make `m` bouquets. If it is impossible, return -1.

*Example:*
- **Input:** `bloomDay = [1,10,3,10,2]`, `m = 3`, `k = 1`
- **Output:** `3`

#### Implementation Overview
1.  **Search Space:** The minimum days we can wait is `min(bloomDay)`. The maximum is `max(bloomDay)`.
2.  **Predicate `is_possible(day)`:** On a given `day`, can we make `m` bouquets?
    -   Iterate through `bloomDay`. Keep a counter for adjacent flowers that have bloomed (`bloomDay[i] <= day`).
    -   If the adjacent counter reaches `k`, we can form a bouquet. Increment a `bouquets_made` counter and reset the adjacent flower counter.
    -   Return `bouquets_made >= m`.
3.  **Binary Search:** We want the minimum day.
    -   If `is_possible(mid)` is true, `mid` is a valid day. Store it and try for an earlier day: `ans = mid`, `high = mid - 1`.
    -   If false, `mid` is too early. We need to wait longer: `low = mid + 1`.

#### Python Code Snippet
```python
def min_days_for_bouquets(bloomDay, m, k):
    if m * k > len(bloomDay):
        return -1

    def is_possible(day):
        bouquets = 0
        flowers = 0
        for b_day in bloomDay:
            if b_day <= day:
                flowers += 1
                if flowers == k:
                    bouquets += 1
                    flowers = 0
            else:
                flowers = 0
        return bouquets >= m

    low, high = min(bloomDay), max(bloomDay)
    ans = -1
    while low <= high:
        mid = low + (high - low) // 2
        if is_possible(mid):
            ans = mid
            high = mid - 1
        else:
            low = mid + 1
    return ans
```

---

### 5. Find the Smallest Divisor
`[MEDIUM]` `#binary-search-on-answer` `#minimization`

#### Problem Statement
Given an array `nums` and a `threshold`, find the smallest positive integer divisor such that the sum of the divisions of all numbers in `nums` (rounded up to the nearest integer) is less than or equal to the threshold.

*Example:*
- **Input:** `nums = [1,2,5,9]`, `threshold = 6`
- **Output:** `5`

#### Implementation Overview
This problem is structurally identical to Koko Eating Bananas.
1.  **Search Space:** `low = 1`, `high = max(nums)`.
2.  **Predicate `is_possible(divisor)`:** Calculate `sum_of_divisions = sum(math.ceil(num / divisor) for num in nums)`. Return `sum_of_divisions <= threshold`.
3.  **Binary Search:** Search for the minimum possible divisor. If `is_possible(mid)` is true, try for a smaller one (`ans = mid`, `high = mid - 1`). Otherwise, `low = mid + 1`.

#### Python Code Snippet
```python
import math
def smallest_divisor(nums, threshold):
    low, high = 1, max(nums)
    ans = high

    def is_possible(divisor):
        total = sum(math.ceil(num / divisor) for num in nums)
        return total <= threshold

    while low <= high:
        mid = low + (high - low) // 2
        if is_possible(mid):
            ans = mid
            high = mid - 1
        else:
            low = mid + 1
    return ans
```

---

### 6. Capacity to Ship Packages within D Days
`[MEDIUM]` `#binary-search-on-answer` `#minimize-the-maximum`

#### Problem Statement
Given an array of package `weights` and `D` days, find the least weight capacity of a ship that can ship all packages within `D` days. You must ship packages in the given order.

*Example:*
- **Input:** `weights = [1,2,3,4,5,6,7,8,9,10]`, `days = 5`
- **Output:** `15`

#### Implementation Overview
This is a "minimize the maximum" problem. We are minimizing the maximum capacity.
1.  **Search Space:** The lowest possible capacity is `max(weights)` (to carry the heaviest single package). The highest possible capacity is `sum(weights)` (to carry everything in one day). So, `low = max(weights)`, `high = sum(weights)`.
2.  **Predicate `is_possible(capacity)`:** Can we ship all packages in `D` days with the given `capacity`?
    -   Greedily load packages. Keep a `current_weight` sum. For each package, if adding it exceeds `capacity`, we must ship the current load, which takes one day. Increment day count and start a new shipment with the current package.
    -   Return `days_needed <= D`.
3.  **Binary Search:** If `is_possible(mid)` is true, `mid` is a valid capacity. Try for a smaller capacity: `ans = mid`, `high = mid - 1`. Else, `low = mid + 1`.

#### Python Code Snippet
```python
def ship_within_days(weights, days):
    def is_possible(capacity):
        days_needed = 1
        current_weight = 0
        for w in weights:
            if current_weight + w > capacity:
                days_needed += 1
                current_weight = w
            else:
                current_weight += w
        return days_needed <= days

    low, high = max(weights), sum(weights)
    ans = high
    while low <= high:
        mid = low + (high - low) // 2
        if is_possible(mid):
            ans = mid
            high = mid - 1
        else:
            low = mid + 1
    return ans
```

---

### 7. Aggressive Cows
`[HARD]` `#binary-search-on-answer` `#maximize-the-minimum`

#### Problem Statement
You are given an array of `n` stall locations and an integer `k` representing the number of aggressive cows. You need to assign each cow to a stall such that the minimum distance between any two cows is maximized.

*Example:*
- **Input:** `stalls = [1, 2, 8, 4, 9]`, `k = 3`
- **Output:** `3` (Place cows at 1, 4, and 8 or 1, 4, and 9. Min distance is 3).

#### Implementation Overview
This is a classic "maximize the minimum" problem.
1.  **Sort:** The stall locations must be sorted first.
2.  **Search Space:** The answer (minimum distance) can range from `1` to `max(stalls) - min(stalls)`.
3.  **Predicate `is_possible(dist)`:** Can we place `k` cows with at least `dist` between them?
    -   Greedily place the first cow at `stalls[0]`.
    -   Iterate through the remaining stalls. Place the next cow only when the distance from the last placed cow is `>= dist`.
    -   Return `cows_placed >= k`.
4.  **Binary Search:** If `is_possible(mid)` is true, `mid` is a valid distance. We store it and try for an even larger distance: `ans = mid`, `low = mid + 1`. Otherwise, `mid` is too large: `high = mid - 1`.

#### Python Code Snippet
```python
def aggressive_cows(stalls, k):
    stalls.sort()

    def is_possible(dist):
        cows_placed = 1
        last_pos = stalls[0]
        for i in range(1, len(stalls)):
            if stalls[i] - last_pos >= dist:
                cows_placed += 1
                last_pos = stalls[i]
        return cows_placed >= k

    low, high = 1, stalls[-1] - stalls[0]
    ans = 0
    while low <= high:
        mid = low + (high - low) // 2
        if is_possible(mid):
            ans = mid
            low = mid + 1
        else:
            high = mid - 1
    return ans
```

---

### 8. Book Allocation Problem
`[HARD]` `#binary-search-on-answer` `#minimize-the-maximum`

#### Problem Statement
Given `n` books with `pages[i]` pages and `m` students, allocate the books consecutively to students. You have to minimize the maximum number of pages allocated to any single student.

*Example:*
- **Input:** `pages = [12, 34, 67, 90]`, `m = 2`
- **Output:** `113` (Student 1 gets [12, 34, 67] (sum 113), Student 2 gets [90]).

#### Implementation Overview
This is a "minimize the maximum" problem, identical in structure to `Capacity to Ship Packages`.
1.  **Search Space:** The answer (max pages for a student) ranges from `max(pages)` to `sum(pages)`.
2.  **Predicate `is_possible(max_pages)`:** Can we allocate books so no student has more than `max_pages`?
    -   Greedily assign books to a student until the page sum exceeds `max_pages`, then move to the next student.
    -   Return `students_needed <= m`.
3.  **Binary Search:** If `is_possible(mid)` is true, try for a smaller max page count: `ans = mid`, `high = mid - 1`. Else, `low = mid + 1`.

#### Python Code Snippet
```python
def allocate_books(pages, m):
    if m > len(pages): return -1

    def is_possible(max_pages_allowed):
        students_needed = 1
        current_pages = 0
        for p in pages:
            if current_pages + p > max_pages_allowed:
                students_needed += 1
                current_pages = p
            else:
                current_pages += p
        return students_needed <= m

    low, high = max(pages), sum(pages)
    ans = high
    while low <= high:
        mid = low + (high - low) // 2
        if is_possible(mid):
            ans = mid
            high = mid - 1
        else:
            low = mid + 1
    return ans
```

#### Related Problems
- `Split Array - Largest Sum`
- `Painter's Partition`
- `Capacity to Ship Packages`

---

### 9. Split Array - Largest Sum
`[MEDIUM]` `#binarysearch` `#searchspace`

#### Problem Statement
Given an integer array `nums` and an integer `k`, split the array into `k` non-empty contiguous subarrays such that the individual largest sum of these subarrays is minimized. Return the minimized largest sum of the split.

*Example:*
- **Input:** `nums = [7,2,5,10,8]`, `k = 2`
- **Output:** `18`
- **Explanation:** There are four ways to split nums into two subarrays. The best way is to split it into [7,2,5] and [10,8], where the largest sum is 18.

#### Implementation Overview
This is a direct application of the Binary Search on Answers pattern, mathematically identical to the Book Allocation Problem.
1. The search space is `[low, high]`, where `low = max(nums)` (the smallest possible maximum sum for a single element subarray) and `high = sum(nums)` (the sum if we only have 1 subarray).
2. For a candidate sum `mid`, we greedily group elements into subarrays.
3. If the number of subarrays needed is `<= k`, it means `mid` is feasible. We try to find a smaller maximum sum by searching in `[low, mid - 1]`.
4. Otherwise, we search in `[mid + 1, high]`.

#### Python Code Snippet
```python
def splitArray(nums, k):
    def canSplit(max_sum):
        current_sum = 0
        subarrays = 1
        for num in nums:
            if current_sum + num > max_sum:
                subarrays += 1
                current_sum = num
                if subarrays > k:
                    return False
            else:
                current_sum += num
        return True
        
    low = max(nums)
    high = sum(nums)
    ans = high
    while low <= high:
        mid = (low + high) // 2
        if canSplit(mid):
            ans = mid
            high = mid - 1
        else:
            low = mid + 1
    return ans
```

#### Tricks/Gotchas
- **Identical to Book Allocation:** The code logic is 100% equivalent; only the variable names and context differ.

---

### 10. Painter's Partition
`[MEDIUM]` `#binarysearch` `#searchspace`

#### Problem Statement
Given an array `boards` where each element represents the length of a board and an integer `k` representing the number of painters available. Each painter takes 1 unit of time to paint 1 unit of board. A board can only be painted by one painter and in a contiguous fashion. Find the minimum time to get the entire board painted.

*Example:*
- **Input:** `boards = [10, 20, 30, 40]`, `k = 2`
- **Output:** `60`

#### Implementation Overview
This is also mathematically identical to the Book Allocation and Split Array problems.
1. `low = max(boards)`, `high = sum(boards)`.
2. Binary search for the minimum maximum board length a single painter needs to paint.

#### Python Code Snippet
```python
def paintBoards(boards, k):
    def canPaint(max_time):
        current_time = 0
        painters = 1
        for board in boards:
            if current_time + board > max_time:
                painters += 1
                current_time = board
                if painters > k:
                    return False
            else:
                current_time += board
        return True
        
    low = max(boards)
    high = sum(boards)
    ans = high
    while low <= high:
        mid = (low + high) // 2
        if canPaint(mid):
            ans = mid
            high = mid - 1
        else:
            low = mid + 1
    return ans
```
