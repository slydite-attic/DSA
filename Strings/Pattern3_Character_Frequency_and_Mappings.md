### `[PATTERN] Character Frequency and Mappings`

This pattern is fundamental for solving a wide range of string problems. The core idea is to use a data structure, typically a **hash map** (or a simple array of size 26/128/256 if the character set is known and small), to store the frequencies of characters or to establish mappings between characters.

This approach is highly efficient for:
- Checking for anagrams.
- Verifying isomorphic relationships.
- Grouping or sorting strings based on their character composition.
- Tracking the state of a sliding window.

---

### 1. Isomorphic Strings
`[EASY]` `#hash-map` `#mapping`

#### Problem Statement
Given two strings `s` and `t`, determine if they are isomorphic. Two strings are isomorphic if the characters in `s` can be replaced to get `t`. All occurrences of a character must be replaced with the same character, and no two characters may map to the same target character.

#### Implementation Overview
To be isomorphic, the mapping from `s` to `t` must be **bijective** (one-to-one and onto).
1.  A character in `s` must map to exactly one character in `t`.
2.  A character in `t` must be mapped to by exactly one character in `s`.

We can enforce this by using two hash maps.

1.  **Length Check**: If `len(s) != len(t)`, they can't be isomorphic.
2.  **Initialize Maps**: `s_to_t_map` and `t_to_s_map`.
3.  **Iterate**: Loop through the strings using `zip`. For each pair `(char_s, char_t)`:
    a. Check if `char_s` is already mapped to a different character in `t`.
    b. Check if `char_t` is already mapped to by a different character in `s`.
    c. If either check fails, return `False`.
    d. Otherwise, establish the mapping in both directions.
4.  If the loop completes, the mapping is valid. Return `True`.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the string length.
- **Space Complexity:** $O(1)$ (limited by the character set size).

#### Python Code Snippet
```python
def is_isomorphic(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False

    s_to_t_map = {}
    t_to_s_map = {}

    for char_s, char_t in zip(s, t):
        # Check forward mapping (s -> t)
        if char_s in s_to_t_map and s_to_t_map[char_s] != char_t:
            return False
        # Check backward mapping (t -> s)
        if char_t in t_to_s_map and t_to_s_map[char_t] != char_s:
            return False

        s_to_t_map[char_s] = char_t
        t_to_s_map[char_t] = char_s

    return True
```

---

### 2. Valid Anagram
`[EASY]` `#hash-map` `#sorting` `#frequency-counting`

#### Problem Statement
Given two strings `s` and `t`, return `true` if `t` is an anagram of `s`. An anagram is formed by rearranging the letters of another word, using all original letters exactly once.

#### Implementation Overview
**a) Frequency Counting (Optimal):** Anagrams must have identical character frequencies.
1. Check for equal length.
2. Use a hash map (or an array of size 26) to count character frequencies in `s`.
3. Iterate through `t`, decrementing the count for each character. If a character is not in the map or its count is already zero, they are not anagrams.

**b) Sorting:** If two strings are anagrams, their sorted versions will be identical. This is often simpler to write but less performant (O(N log N)).

#### Time and Space Complexity
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(1)$ (constant alphabet size).

#### Python Code Snippet (Frequency Counting)
```python
from collections import Counter

def is_anagram(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False
    # Counter creates a hash map of frequencies.
    # Comparing two Counter objects is a clean way to check for equality.
    return Counter(s) == Counter(t)

# Alternative: Manual frequency counting
def is_anagram_manual(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False

    counts = {}
    for char in s:
        counts[char] = counts.get(char, 0) + 1

    for char in t:
        if counts.get(char, 0) == 0:
            return False
        counts[char] -= 1

    return True
```

---

### 3. Group Anagrams
`[MEDIUM]` `#hash-map` `#grouping`

#### Problem Statement
Given an array of strings `strs`, group the anagrams together. You can return the answer in any order.

#### Implementation Overview
The core idea is to find a **canonical representation** for each anagram group. All strings in an anagram group will have the same canonical form. We can use a hash map where the key is this canonical form and the value is a list of strings belonging to that group.

Two common choices for the canonical key:
1.  **Sorted String**: Sort the characters of the string (e.g., "eat", "tea", "ate" all become "aet").
2.  **Character Count Tuple**: Create a frequency array (e.g., of size 26) for each string and convert it to a tuple, which is hashable and can be used as a dictionary key.

#### Time and Space Complexity
- **Time Complexity:** $O(N \cdot K \log K)$, where $N$ is the number of strings and $K$ is the max length of a string (sorting each string).
- **Space Complexity:** $O(N \cdot K)$ to store the grouped strings.

#### Python Code Snippet (Sorted String Key)
```python
import collections

def group_anagrams(strs: list[str]) -> list[list[str]]:
    # A dictionary where keys are the canonical form (sorted string)
    # and values are lists of anagrams.
    anagram_groups = collections.defaultdict(list)

    for s in strs:
        # The sorted string is the key
        key = "".join(sorted(s))
        anagram_groups[key].append(s)

    return list(anagram_groups.values())
```

---

### 4. Sort Characters by Frequency
`[MEDIUM]` `#hash-map` `#sorting` `#frequency-counting`

#### Problem Statement
Given a string `s`, sort it in decreasing order based on the frequency of its characters.

#### Implementation Overview
This combines frequency counting with a custom sort.
1.  **Count Frequencies**: Use a hash map (`collections.Counter`) to get the frequency of each character.
2.  **Sort by Frequency**: Sort the characters based on their frequencies in descending order.
3.  **Build Result**: Create the final string by appending each character a number of times equal to its frequency.

A **Bucket Sort** approach is often more efficient (O(N) time).
1. Count frequencies.
2. Create `n+1` buckets (arrays/lists).
3. For each character with frequency `f`, add it to `buckets[f]`.
4. Build the result string by iterating through the buckets from `n` down to `1`.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$ with bucket sort.
- **Space Complexity:** $O(N)$ to store the buckets and result.

#### Python Code Snippet (Bucket Sort)
```python
from collections import Counter

def frequency_sort(s: str) -> str:
    counts = Counter(s)
    max_freq = max(counts.values(), default=0)

    # Create buckets for each frequency
    buckets = [[] for _ in range(max_freq + 1)]
    for char, freq in counts.items():
        buckets[freq].append(char)

    # Build string from buckets, from highest frequency to lowest
    result = []
    for i in range(max_freq, 0, -1):
        for char in buckets[i]:
            result.append(char * i)

    return "".join(result)
```

---

### 5. Find All Anagrams in a String
`[MEDIUM]` `#sliding-window` `#hash-map`

#### Problem Statement
Given two strings `s` and `p`, return an array of all the start indices of `p`'s anagrams in `s`.

#### Implementation Overview
This is a perfect blend of the Sliding Window and Frequency Map patterns. We slide a window of size `len(p)` across `s` and, at each step, check if the window's character frequencies match the frequencies of `p`.

1.  **Setup**: Get frequency maps for the pattern `p` (`p_counts`) and for the initial window in `s` (`s_counts`).
2.  **Initial Check**: Compare the initial `p_counts` and `s_counts`. If they match, index 0 is a solution.
3.  **Slide the Window**: Iterate from `len(p)` to the end of `s`.
    a. **Expand**: Add the new character `s[right]` to the window by incrementing its count in `s_counts`.
    b. **Shrink**: Remove the character `s[left]` that just left the window by decrementing its count. If its count becomes 0, remove it from the map.
    c. **Compare**: After each slide, compare `s_counts` with `p_counts`. If they are equal, the current `left` index marks the start of an anagram.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(1)$ (constant alphabet size).

#### Python Code Snippet
```python
from collections import Counter

def find_anagrams(s: str, p: str) -> list[int]:
    ns, np = len(s), len(p)
    if ns < np:
        return []

    p_counts = Counter(p)
    s_counts = Counter()

    result = []

    # Initialize the first window
    for i in range(np):
        s_counts[s[i]] += 1

    if s_counts == p_counts:
        result.append(0)

    # Slide the window across the rest of the string
    for i in range(np, ns):
        # Add the new character (at right of window)
        s_counts[s[i]] += 1

        # Remove the old character (at left of window)
        left_char = s[i - np]
        if s_counts[left_char] == 1:
            del s_counts[left_char]
        else:
            s_counts[left_char] -= 1

        # Compare and add result
        if s_counts == p_counts:
            result.append(i - np + 1)

    return result
```
