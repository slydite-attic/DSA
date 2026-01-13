# Pattern 3: Classic Stack Applications

This pattern covers problems where the Last-In, First-Out (LIFO) property of a stack is used directly to solve problems related to parsing, validation, and expression evaluation.

---

### 1. Check for balanced parenthesis
`[EASY]` `#stack` `#validation`

#### Problem Statement
Given a string `s` containing just the characters `(`, `)`, `{`, `}`, `[` and `]`, determine if the input string is valid. An input string is valid if:
1.  Open brackets must be closed by the same type of brackets.
2.  Open brackets must be closed in the correct order.
3.  Every close bracket has a corresponding open bracket of the same type.

*Example:*
- **Input:** `s = "()[]{}"`
- **Output:** `true`
- **Input:** `s = "(]"`
- **Output:** `false`

#### Implementation Overview
This is a canonical problem for stack usage. We iterate through the string:
- If we see an opening bracket (`(`, `{`, `[`), we push it onto the stack. This means we expect a corresponding closing bracket later.
- If we see a closing bracket (`)`, `}`, `]`), we check the top of the stack.
  - If the stack is empty or the top element is not the corresponding opening bracket, the string is invalid.
  - If it is the correct opening bracket, we have found a valid pair, so we pop the stack.
- After iterating through the entire string, if the stack is empty, all brackets were correctly matched and closed. If the stack is not empty, it means there are unclosed opening brackets, so the string is invalid.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the length of the string.
- **Space Complexity:** $O(N)$ for the stack.

#### Python Code Snippet
```python
def is_valid_parentheses(s: str) -> bool:
    stack = []
    bracket_map = {')': '(', '}': '{', ']': '['}

    for char in s:
        if char in bracket_map: # It's a closing bracket
            if not stack:
                return False # Closing bracket with no open one
            top_element = stack.pop()
            if bracket_map[char] != top_element:
                return False # Mismatched brackets
        else: # It's an opening bracket
            stack.append(char)

    return not stack # True if stack is empty, False otherwise
```

---

### 2. Infix to Postfix Conversion
`[MEDIUM]` `#stack` `#expression-parsing`

#### Problem Statement
Given an infix expression string, convert it to a postfix expression. Infix notation is the common mathematical form (e.g., `a+b*c`). Postfix notation (or Reverse Polish Notation) places operators after their operands (e.g., `abc*+`).

*Example:*
- **Input:** `a+b*(c^d-e)^(f+g*h)-i`
- **Output:** `abcd^e-fgh*+^*+i-`

#### Implementation Overview
We use a stack to hold operators. We iterate through the infix expression:
1.  **Operand**: If the character is an operand (a letter or number), append it to the result string.
2.  **Opening Parenthesis `(`**: Push it onto the stack.
3.  **Closing Parenthesis `)`**: Pop operators from the stack and append them to the result until an opening parenthesis `(` is encountered. Pop and discard the `(`.
4.  **Operator**: If the character is an operator:
    - While the stack is not empty, the top is not `(`, and the precedence of the current operator is less than or equal to the precedence of the operator at the top of the stack, pop operators from the stack and append them to the result.
    - After the loop, push the current operator onto the stack.
5. After iterating through the expression, pop any remaining operators from the stack and append them to the result.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$, where $N$ is the length of the string.
- **Space Complexity:** $O(N)$ for the stack and result.

#### Python Code Snippet
```python
def infix_to_postfix(expression):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    stack = []
    postfix = []

    for char in expression:
        if char.isalnum():
            postfix.append(char)
        elif char == '(':
            stack.append(char)
        elif char == ')':
            while stack and stack[-1] != '(':
                postfix.append(stack.pop())
            if stack and stack[-1] == '(':
                stack.pop() # Pop '('
        else: # Operator
            # Note: For '^', associativity is right-to-left, so we use <
            while (stack and stack[-1] != '(' and
                   (precedence.get(char, 0) < precedence.get(stack[-1], 0) or
                    (precedence.get(char, 0) == precedence.get(stack[-1], 0) and char != '^'))):
                postfix.append(stack.pop())
            stack.append(char)

    while stack:
        postfix.append(stack.pop())

    return "".join(postfix)
```

---

### 3. Postfix to Infix Conversion
`[MEDIUM]` `#stack` `#expression-parsing`

#### Problem Statement
Given a postfix expression, convert it to a fully parenthesized infix expression.

*Example:*
- **Input:** `ab+c*`
- **Output:** `((a+b)*c)`

#### Implementation Overview
Iterate through the postfix expression:
- If the character is an operand, push it onto a stack.
- If the character is an operator, pop two operands from the stack (`op2` then `op1`). Form a string `(op1 operator op2)` and push this new string back onto the stack.
- The final result is the single string remaining on the stack.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(N)$.

#### Python Code Snippet
```python
def postfix_to_infix(expression):
    stack = []
    for char in expression:
        if char.isalnum():
            stack.append(char)
        else: # Operator
            op2 = stack.pop()
            op1 = stack.pop()
            stack.append(f"({op1}{char}{op2})")
    return stack.pop()
```

---

### 4. Prefix to Infix Conversion
`[MEDIUM]` `#stack` `#expression-parsing`

#### Problem Statement
Given a prefix expression, convert it to a fully parenthesized infix expression.

*Example:*
- **Input:** `*+ab/cd`
- **Output:** `((a+b)*(c/d))`

#### Implementation Overview
This is similar to postfix-to-infix, but we iterate through the prefix expression in **reverse**.
- If the character is an operand, push it onto a stack.
- If the character is an operator, pop two operands from the stack (`op1` then `op2`). Form a string `(op1 operator op2)` and push it back.
- The final result is the single string on the stack.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(N)$.

#### Python Code Snippet
```python
def prefix_to_infix(expression):
    stack = []
    # Iterate in reverse
    for char in reversed(expression):
        if char.isalnum():
            stack.append(char)
        else: # Operator
            op1 = stack.pop()
            op2 = stack.pop()
            stack.append(f"({op1}{char}{op2})")
    return stack.pop()
```

---

### 5. Prefix to Postfix Conversion
`[MEDIUM]` `#stack` `#expression-parsing`

#### Problem Statement
Given a prefix expression, convert it to a postfix expression.

*Example:*
- **Input:** `*+ab-cd`
- **Output:** `ab+cd-*`

#### Implementation Overview
Iterate through the prefix expression in **reverse**.
- If the character is an operand, push it onto a stack.
- If the character is an operator, pop two operands (`op1`, `op2`) from the stack. Form a new string `op1 + op2 + operator` and push it back.
- The final result is the single string on the stack.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(N)$.

#### Python Code Snippet
```python
def prefix_to_postfix(expression):
    stack = []
    for char in reversed(expression):
        if char.isalnum():
            stack.append(char)
        else: # Operator
            op1 = stack.pop()
            op2 = stack.pop()
            stack.append(f"{op1}{op2}{char}")
    return stack.pop()
```

---

### 6. Postfix to Prefix Conversion
`[MEDIUM]` `#stack` `#expression-parsing`

#### Problem Statement
Given a postfix expression, convert it to a prefix expression.

*Example:*
- **Input:** `ab+cd-*`
- **Output:** `*+ab-cd`

#### Implementation Overview
Iterate through the postfix expression.
- If the character is an operand, push it onto a stack.
- If the character is an operator, pop two operands (`op2` then `op1`) from the stack. Form a new string `operator + op1 + op2` and push it back.
- The final result is the single string on the stack.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(N)$.

#### Python Code Snippet
```python
def postfix_to_prefix(expression):
    stack = []
    for char in expression:
        if char.isalnum():
            stack.append(char)
        else: # Operator
            op2 = stack.pop()
            op1 = stack.pop()
            stack.append(f"{char}{op1}{op2}")
    return stack.pop()
```

---

### 7. Convert Infix To Prefix Notation
`[MEDIUM]` `#stack` `#expression-parsing`

#### Problem Statement
Given an infix expression, convert it to a prefix expression.

*Example:*
- **Input:** `x+y*z/w+u`
- **Output:** `++x/*yzwu`

#### Implementation Overview
This is a variation of Infix to Postfix that reuses the same logic with a clever trick.
1.  **Reverse** the infix expression.
2.  While reversing, swap every `(` with `)` and every `)` with `(`.
3.  Find the **postfix** expression of this new modified string using the standard algorithm.
4.  **Reverse** the resulting postfix expression. This gives the final prefix expression.

#### Time and Space Complexity
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(N)$.

#### Python Code Snippet
```python
def infix_to_prefix(expression):
    # Step 1 & 2: Reverse and swap parentheses
    rev_expr = ""
    for char in reversed(expression):
        if char == '(':
            rev_expr += ')'
        elif char == ')':
            rev_expr += '('
        else:
            rev_expr += char

    # Step 3: Find postfix of the reversed expression
    # Using the same logic from infix_to_postfix
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    stack = []
    postfix = []
    for char in rev_expr:
        if char.isalnum():
            postfix.append(char)
        elif char == '(':
            stack.append(char)
        elif char == ')':
            while stack and stack[-1] != '(':
                postfix.append(stack.pop())
            if stack: stack.pop()
        else:
            while (stack and stack[-1] != '(' and
                   precedence.get(char, 0) < precedence.get(stack[-1], 0)):
                postfix.append(stack.pop())
            stack.append(char)

    while stack:
        postfix.append(stack.pop())

    # Step 4: Reverse the result
    return "".join(reversed(postfix))
```
