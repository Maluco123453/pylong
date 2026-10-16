# EZ Programming Language Specification

## Overview
EZ is designed to be the most intuitive programming language possible - English-like, minimal syntax, easy to learn.

## Syntax Rules
1. **No braces `{}`** - use indentation like Python
2. **No semicolons `;`** - one statement per line
3. **English keywords only**: `let`, `print`, `if`, `else`, `while`, `input`
4. **Case-insensitive** - `LET` and `let` are the same

## Variable Assignment
```
let x = 10
let name = "Hello"
let active = true
```

## Print
```
print "Hello, World!"
print x
```

## Input
```
input name
```

## If Statement
```
if x > 5
    print "x is greater than 5"
else
    print "x is 5 or less"
end
```

## While Loop
```
while x < 10
    let x = x + 1
end
```

## Comments
```
# This is a comment
```

## Data Types
- **numbers**: integers and decimals
- **text**: strings in double quotes
- **boolean**: `true` or `false`

## Operators
- `=` (assignment)
- `==` (equal comparison)
- `!=` (not equal)
- `>` (greater than)
- `<` (less than)
- `+` (addition), `-` (subtraction), `*` (multiply), `/` (divide)

## Function Syntax (optional future feature)
Not in v1.0 - keeping it ultra-simple.