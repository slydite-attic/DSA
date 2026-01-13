### `[PATTERN] Advanced Parsing and Special Cases`

This pattern covers more complex string parsing problems. These often involve intricate rules, state management, and the use of a **stack** to handle nested structures like parentheses or to reverse evaluation order.

---
### Parentheses-Based Problems

These problems use counters or stacks to validate, manipulate, or measure properties of strings containing parentheses.

---

### 1. Valid Parentheses
`[EASY]` `#stack` `#parentheses`

#### Problem Statement
Given a string `s` containing just the characters `(`, `)`, `{`, `}`, `[` and `]`, determine if the input string is valid. An input string is valid if:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.

#### Implementation Overview
This is the classic problem for demonstrating the utility of a stack.
1.  **Initialize a Stack**: Use a list or deque as a stack.
2.  **Initialize a Mapping**: A hash map is useful to store the matching pairs (e.g., `map = {')': '(', '}': '{', ']': '['}`).
3.  **Iterate Through String**:
    -   If the current character is an **opening** bracket (`(`, `{`, `[`), push it onto the stack.
    -   If the current character is a **closing** bracket (`)`, `}`, `]`):
        a. Check if the stack is empty. If it is, there's no matching open bracket, so it's invalid.
        b. Pop the top element from the stack.
        c. Check if the popped element is the corresponding opening bracket for the current closing bracket (using the map). If not, it's invalid.
4.  **Final Check**: After the loop, if the stack is **empty**, it means every open bracket had a matching closing bracket. If it's not empty, it means there are unclosed opening brackets.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(N)$ for the stack.

#### Python Code Snippet
```python
def is_valid(s: str) -> bool:
    stack = []
    mapping = {")": "(", "}": "{", "]": "["}

    for char in s:
        if char in mapping: # It's a closing bracket
            top_element = stack.pop() if stack else '#'
            if mapping[char] != top_element:
                return False
        else: # It's an opening bracket
            stack.append(char)

    return not stack # Stack must be empty for a valid string
```

---

### 2. Maximum Nesting Depth of the Parentheses
`[EASY]` `#parentheses`

#### Problem Statement
Given a valid parentheses string `s`, return its maximum nesting depth.

#### Implementation Overview
Because the string is guaranteed to be valid, we don't need a stack to check for mismatches. A simple counter is sufficient to track the depth.
1.  Initialize `max_depth = 0` and `current_depth = 0`.
2.  Iterate through the string:
    - If `char == '('`: Increment `current_depth` and update `max_depth = max(max_depth, current_depth)`.
    - If `char == ')`: Decrement `current_depth`.
3.  Return `max_depth`.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(1)$.

#### Python Code Snippet
```python
def max_depth(s: str) -> int:
    max_d = 0
    current_d = 0
    for char in s:
        if char == '(':
            current_d += 1
            max_d = max(max_d, current_d)
        elif char == ')':
            current_d -= 1
    return max_d
```

---

### 3. Remove Outermost Parentheses
`[EASY]` `#parentheses`

#### Problem Statement
Given a valid parentheses string `s` which consists of primitive valid parentheses strings concatenated, remove the outermost parentheses of every primitive string.

#### Implementation Overview
We can identify the primitive parts by tracking the balance of open/closed parentheses.
1.  Initialize a result list and a `balance` counter to 0.
2.  Iterate through the string:
    - If `char == '('`: If `balance > 0` (meaning this is not the first `(` of a primitive part), append it to the result. Then, increment `balance`.
    - If `char == ')`: Decrement `balance`. If `balance > 0` (meaning this is not the last `)` of a primitive part), append it to the result.
3.  Join the result list into a string.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(N)$ for the result string.

#### Python Code Snippet
```python
def remove_outer_parentheses(s: str) -> str:
    result = []
    balance = 0
    for char in s:
        if char == '(':
            if balance > 0:
                result.append(char)
            balance += 1
        else: # char == ')'
            balance -= 1
            if balance > 0:
                result.append(char)
    return "".join(result)
```

---
### Advanced Parsing and Conversion

These problems involve more complex logic for converting between formats or parsing according to specific, non-trivial rules.

---

### 4. Simplify Path
`[MEDIUM]` `#stack` `#parsing`

#### Problem Statement
Given a string `path`, which is an absolute path (starting with a `/`) to a file or directory in a Unix-style file system, convert it to the simplified canonical path. (e.g., `/a/./b/../../c/` -> `/c`).

#### Implementation Overview
A stack is the perfect data structure for this problem. It naturally handles the directory hierarchy.
1.  **Split the Path**: Split the input `path` by the `/` delimiter. This will create a list of components.
2.  **Initialize Stack**: Create a list to use as a stack.
3.  **Process Components**: Iterate through the components from the split:
    - If the component is `.` or empty (`""`), ignore it.
    - If the component is `..`, pop from the stack if it's not empty. This handles moving up a directory.
    - Otherwise, the component is a directory name. Push it onto the stack.
4.  **Build Result**: Join the components remaining in the stack with `/` and prepend a `/` to the front to form the final canonical path.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(N)$ for the stack and splitting the string.

#### Python Code Snippet
```python
def simplify_path(path: str) -> str:
    stack = []
    components = path.split('/')

    for comp in components:
        if comp == "" or comp == ".":
            continue
        elif comp == "..":
            if stack:
                stack.pop()
        else:
            stack.append(comp)

    return "/" + "/".join(stack)
```

---

### 5. Basic Calculator
`[HARD]` `#stack` `#parsing`

#### Problem Statement
Given a string `s` representing a valid expression, implement a basic calculator to evaluate it and return the result. The expression string may contain `(`, `)`, `+`, `-`, non-negative integers, and empty spaces.

#### Implementation Overview
This problem requires a stack to handle the precedence introduced by parentheses.
1.  **Initialize**: `stack`, `result = 0`, `number = 0`, `sign = 1` (for `+` or `-`).
2.  **Iterate**: Loop through each character of the string `s`.
    - If `char` is a **digit**: Build the `number`.
    - If `char` is `'+'` or `'-'`:
        - Add the `number` processed so far to the `result` (with the current `sign`).
        - Reset `number = 0` and update `sign` to `1` or `-1`.
    - If `char` is `'('`:
        - This is the start of a sub-expression. Push the current `result` and `sign` onto the stack.
        - Reset `result = 0` and `sign = 1` for the new sub-expression.
    - If `char` is `')'`:
        - Add the last `number` of the sub-expression to its `result`.
        - Now, "close" the sub-expression. Pop the `prev_sign` and `prev_result` from the stack.
        - The `result` of the sub-expression is multiplied by `prev_sign` and added to `prev_result`.
3.  Add the very last `number` to the `result` after the loop finishes.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(N)$ for the stack.

#### Python Code Snippet
```python
def calculate(s: str) -> int:
    stack = []
    result = 0
    number = 0
    sign = 1  # 1 for +, -1 for -

    for char in s:
        if char.isdigit():
            number = number * 10 + int(char)
        elif char == '+':
            result += sign * number
            number = 0
            sign = 1
        elif char == '-':
            result += sign * number
            number = 0
            sign = -1
        elif char == '(':
            # Push the result and sign onto the stack for later
            stack.append(result)
            stack.append(sign)
            # Reset for the new sub-expression
            result = 0
            sign = 1
        elif char == ')':
            result += sign * number
            number = 0
            # Pop sign and result from stack
            result *= stack.pop()  # Pop sign
            result += stack.pop()  # Pop result

    return result + sign * number
```

---

### 6. Integer to English Words
`[HARD]` `#parsing` `#mapping`

#### Problem Statement
Convert a non-negative integer `num` to its English words representation.

#### Implementation Overview
This is a complex mapping problem that is best solved by breaking the number down into chunks of three (hundreds, tens, ones) and using helper functions.
1.  **Define Mappings**: Create maps for single digits (1-9), teens (10-19), and tens (20, 30, ...).
2.  **Main Logic**:
    - Handle the zero case.
    - Process the number in chunks of thousands, millions, billions, etc.
    - For each chunk, use a helper function to convert the 3-digit number (0-999) to words.
    - Append the appropriate "place" word (e.g., "Thousand", "Million") if the 3-digit chunk is non-zero.
3.  **Helper Function `three_digit_to_words(n)`**:
    - If `n >= 100`, handle the hundreds part (e.g., "One Hundred") and recurse on `n % 100`.
    - If `n >= 20`, handle the tens part (e.g., "Twenty") and recurse on `n % 10`.
    - If `n >= 10`, handle the teens part (e.g., "Fifteen").
    - If `n > 0`, handle the ones part (e.g., "Five").
4.  **Combine and Clean**: Join the parts and clean up any extra spaces.

#### Time and Space Complexity
- **Time Complexity:** $O(1)$ (number of digits is small).
- **Space Complexity:** $O(1)$.

#### Python Code Snippet
```python
def number_to_words(num: int) -> str:
    if num == 0:
        return "Zero"

    to_19 = 'One Two Three Four Five Six Seven Eight Nine Ten Eleven Twelve ' \
            'Thirteen Fourteen Fifteen Sixteen Seventeen Eighteen Nineteen'.split()
    tens = 'Twenty Thirty Forty Fifty Sixty Seventy Eighty Ninety'.split()

    def words(n):
        if n < 20:
            return to_19[n-1:n]
        if n < 100:
            return [tens[n//10-2]] + words(n%10)
        if n < 1000:
            return [to_19[n//100-1], 'Hundred'] + words(n%100)

        for p, w in enumerate(('Thousand', 'Million', 'Billion'), 1):
            if n < 1000**(p+1):
                return words(n//1000**p) + [w] + words(n%1000**p)

    return " ".join(words(num)) or ""
```
