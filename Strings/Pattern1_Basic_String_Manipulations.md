### `[PATTERN] Basic String Manipulations`

This pattern covers fundamental string operations that form the building blocks for more complex problems. Common techniques include:
- **Reversal**: Reversing entire strings or parts of a string.
- **Two Pointers**: Using pointers from opposite ends to check for properties like palindromes.
- **Frequency Counting**: Using a hash map or an array to count character occurrences (e.g., for anagrams).
- **Parsing**: Iterating through a string to convert it into another format (e.g., Roman numerals, integers).

---

### 1. Reverse Words in a String
`[MEDIUM]` `#string` `#two-pointers`

#### Problem Statement
Given an input string `s`, reverse the order of the words. A word is a sequence of non-space characters. The returned string should have only a single space separating words and no leading/trailing spaces.

#### Implementation Overview
A straightforward approach uses built-in functions to deconstruct and reconstruct the string.
1.  **Trim and Split**: Use a built-in `split` method to break the string into a list of words. This method usually handles multiple spaces between words and leading/trailing spaces gracefully.
2.  **Reverse**: Reverse the resulting list of words.
3.  **Join**: Join the words back into a string with a single space as a separator.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the length of the string.
- **Space Complexity:** $O(N)$ to store the list of words and the result string.

#### Python Code Snippet
```python
def reverse_words(s: str) -> str:
    """
    Reverses the order of words in a string.
    """
    # 1. Split the string into words, handling multiple spaces
    words = s.split()

    # 2. Reverse the list of words
    # 3. Join them back with a single space
    return " ".join(reversed(words))
```

#### Tricks/Gotchas
- **In-place Solution (O(1) space)**: A common follow-up is to solve this in-place. This involves:
    1. Reversing the entire string. (`"the sky is blue"` -> `"eulb si yks eht"`)
    2. Reversing each word in the reversed string. (`"eulb si yks eht"` -> `"blue is sky the"`)

---

### 2. Palindrome Check
`[EASY]` `#string` `#two-pointers`

#### Problem Statement
Given a string `s`, return `true` if it is a palindrome, or `false` otherwise. A string is a palindrome if it reads the same forward and backward, after converting all uppercase letters into lowercase and removing all non-alphanumeric characters.

#### Implementation Overview
The most efficient method uses two pointers starting from opposite ends of the string.
1.  **Setup**: Initialize `left = 0` and `right = len(s) - 1`.
2.  **Iterate and Compare**: Loop while `left < right`.
    a. Move `left` forward until it points to an alphanumeric character.
    b. Move `right` backward until it points to an alphanumeric character.
    c. Compare the lowercase versions of the characters at `left` and `right`. If they don't match, it's not a palindrome.
    d. If they match, move both pointers inward (`left += 1`, `right -= 1`).
3.  If the loop completes, the string is a palindrome.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the length of the string. We traverse the string once.
- **Space Complexity:** $O(1)$.

#### Python Code Snippet
```python
def is_palindrome(s: str) -> bool:
    left, right = 0, len(s) - 1
    while left < right:
        # Move pointers past non-alphanumeric characters
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1

        # Compare characters
        if s[left].lower() != s[right].lower():
            return False

        left += 1
        right -= 1

    return True
```

---

### 3. Valid Anagram
`[EASY]` `#string` `#hash-map` `#sorting`

#### Problem Statement
Given two strings `s` and `t`, return `true` if `t` is an anagram of `s`, and `false` otherwise. An anagram is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.

#### Implementation Overview
There are two common solutions.

**a) Sorting:**
If two strings are anagrams, their sorted versions will be identical.
1. Check if the lengths are equal. If not, they can't be anagrams.
2. Sort both strings and compare the results.

**b) Frequency Counting:**
Anagrams must have the same frequency of each character.
1. Check for equal length.
2. Use a hash map (or an array of size 26 for lowercase English letters) to count character frequencies in `s`.
3. Iterate through `t`, decrementing the count for each character. If a character is not in the map or its count is already zero, they are not anagrams.
4. If the loop completes, they are anagrams.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$ for frequency counting, $O(N \log N)$ for sorting.
- **Space Complexity:** $O(1)$ (constant alphabet size) for frequency counting, $O(N)$ for sorting.

#### Python Code Snippet (Frequency Counting)
```python
import collections

def is_anagram(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False

    counts = collections.Counter(s)

    for char in t:
        if counts[char] == 0:
            return False
        counts[char] -= 1

    return True
```

---

### 4. String to Integer (atoi)
`[MEDIUM]` `#string` `#parsing`

#### Problem Statement
Implement the `myAtoi(string s)` function, which converts a string to a 32-bit signed integer. The algorithm is:
1. Read in and ignore any leading whitespace.
2. Check if the next character is `'-'` or `'+'`. Read this character in if it is either.
3. Read in the next characters until the next non-digit character or the end of the input is reached.
4. Convert these digits into an integer.
5. If the integer is out of the 32-bit signed integer range `[-2^31, 2^31 - 1]`, then clamp the integer.
6. Return the integer as the final result.

#### Implementation Overview
This is a state-based parsing problem. We must carefully process the string character by character.
1.  **Initialize**: `i = 0` (pointer), `sign = 1`, `result = 0`.
2.  **Whitespace**: Skip all leading spaces.
3.  **Sign**: Check for `'+'` or `'-'`. If found, update `sign` and advance `i`.
4.  **Digits**: Loop while the current character is a digit.
    a. Convert the character to an integer `digit`.
    b. **Check for Overflow**: Before updating `result`, check if `result * 10 + digit` will exceed the integer limits. Let `INT_MAX = 2**31 - 1` and `INT_MIN = -2**31`. The check is `if result > INT_MAX // 10 or (result == INT_MAX // 10 and digit > 7)`.
    c. If overflow, return `INT_MAX` or `INT_MIN` based on the `sign`.
    d. Update `result = result * 10 + digit`.
5.  Return `sign * result`.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(1)$.

#### Python Code Snippet
```python
def my_atoi(s: str) -> int:
    i, n = 0, len(s)
    INT_MAX, INT_MIN = 2**31 - 1, -2**31

    # 1. Skip whitespace
    while i < n and s[i] == ' ':
        i += 1

    # 2. Check for sign
    sign = 1
    if i < n and (s[i] == '+' or s[i] == '-'):
        if s[i] == '-':
            sign = -1
        i += 1

    # 3. Read digits and handle overflow
    result = 0
    while i < n and s[i].isdigit():
        digit = int(s[i])
        # Overflow check
        if result > INT_MAX // 10 or (result == INT_MAX // 10 and digit > 7):
            return INT_MAX if sign == 1 else INT_MIN

        result = result * 10 + digit
        i += 1

    return sign * result
```

---

### 5. Roman to Integer
`[EASY]` `#string` `#parsing` `#hash-map`

#### Problem Statement
Given a roman numeral, convert it to an integer. Roman numerals are represented by seven different symbols: `I, V, X, L, C, D, M`.

#### Implementation Overview
The key is to handle the subtractive cases (e.g., `IV` is 4, `IX` is 9). A character's value might be subtracted from the next if it's smaller.
1.  Create a mapping from Roman symbols to their integer values.
2.  Iterate through the string from left to right.
3.  For each character `s[i]`, check the value of the next character `s[i+1]`.
    - If `value(s[i]) < value(s[i+1])`, it's a subtractive case. Subtract `value(s[i])` from the total.
    - Otherwise, it's an additive case. Add `value(s[i])` to the total.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(1)$.

#### Python Code Snippet
```python
def roman_to_int(s: str) -> int:
    roman_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    result = 0

    for i in range(len(s)):
        # Check for subtractive case
        if i + 1 < len(s) and roman_map[s[i]] < roman_map[s[i+1]]:
            result -= roman_map[s[i]]
        else:
            result += roman_map[s[i]]

    return result
```

---

### 6. Integer to Roman
`[MEDIUM]` `#string` `#greedy`

#### Problem Statement
Given an integer, convert it to a roman numeral.

#### Implementation Overview
A greedy approach works best here. We process the number from largest values to smallest.
1.  Create a list of `(value, symbol)` pairs, sorted from largest to smallest (e.g., `(1000, "M")`, `(900, "CM")`, `(500, "D")`, ...). Including the subtractive cases (`CM`, `CD`, `XC`, `XL`, `IX`, `IV`) makes the logic much simpler.
2.  Iterate through this list. For each `(value, symbol)` pair:
    - While the input `num` is greater than or equal to `value`, append the `symbol` to the result string and subtract `value` from `num`.
3.  Continue until `num` becomes 0.

#### Time and Space Complexity
- **Time Complexity:** $O(1)$ because the input number is bounded (typically < 4000).
- **Space Complexity:** $O(1)$.

#### Python Code Snippet
```python
def int_to_roman(num: int) -> str:
    # List of values and symbols, sorted from largest to smallest
    val_syms = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"),
        (1, "I")
    ]

    result = []
    for val, sym in val_syms:
        while num >= val:
            result.append(sym)
            num -= val

    return "".join(result)

---

### 9. Reverse Every Word in a String
`[EASY]` `#string` `#reversal`

#### Problem Statement
Given a string `s`, reverse each word in the string. The order of the words and the whitespace should be preserved.

#### Implementation Overview
This is a direct application of string manipulation.
1.  **Split the String**: Split the input string `s` into a list of words.
2.  **Reverse Each Word**: Iterate through the list of words. For each word, reverse it.
3.  **Join the Words**: Join the list of reversed words back into a single string, using a space as the separator.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(N)$.

#### Python Code Snippet
```python
def reverse_each_word(s: str) -> str:
    words = s.split(' ')
    reversed_words = [word[::-1] for word in words]
    return " ".join(reversed_words)
```

---

### 8. Check if One String is a Rotation of Another
`[EASY]` `#string` `#concatenation`

#### Problem Statement
Given two strings, `s1` and `s2`, return `true` if `s2` is a rotation of `s1`, and `false` otherwise. For example, `"waterbottle"` is a rotation of `"erbottlewat"`.

#### Implementation Overview
This problem has a famously clever and simple solution.
1.  **Length Check**: If `s1` and `s2` have different lengths, `s2` cannot be a rotation of `s1`.
2.  **Concatenation**: Create a new string by concatenating `s1` with itself (`s1 + s1`).
3.  **Substring Check**: If `s2` is a rotation of `s1`, then `s2` must be a substring of the new concatenated string. Check if `s2` exists within `s1 + s1`.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(N)$ for the concatenated string.

#### Python Code Snippet
```python
def is_rotation(s1: str, s2: str) -> bool:
    if len(s1) != len(s2) or not s1:
        return False

    concatenated_s1 = s1 + s1
    return s2 in concatenated_s1
```

---

### 7. Largest Odd Number in String
`[EASY]` `#string` `#greedy`

#### Problem Statement
You are given a string `num`, representing a large integer. Return the largest-valued odd integer (as a string) that is a non-empty substring of `num`, or an empty string `""` if no odd integer exists.

#### Implementation Overview
A greedy approach is most effective. The largest odd number will be the longest possible prefix of the original number that ends in an odd digit.
1.  **Iterate from the End**: Traverse the string `num` from right to left.
2.  **Find First Odd Digit**: The first digit you encounter that is odd will be the last digit of the largest possible odd number substring.
3.  **Return the Prefix**: Once you find the first odd digit from the right at index `i`, the substring `num[:i+1]` is the answer.
4.  **No Odd Digits**: If the loop finishes, no odd digits were found. Return `""`.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(1)$ (or $O(N)$ if slicing creates a new string).

#### Python Code Snippet
```python
def largest_odd_number(num: str) -> str:
    for i in range(len(num) - 1, -1, -1):
        if int(num[i]) % 2 != 0:
            return num[:i+1]
    return ""
```
```
