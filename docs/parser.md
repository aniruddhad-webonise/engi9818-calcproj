# Parser Module - Detailed Technical Documentation

## Overview

The `parser.py` module implements the **second phase of our robust parser** requirement. It converts the token stream from the tokenizer into expression trees using recursive descent parsing with proper operator precedence handling.

## Project Requirements Addressed

### Robust Parser (Second Component)
- **Syntax Analysis**: Converts tokens into structured expression trees
- **Operator Precedence**: Implements PEMDAS correctly
- **Associativity**: Handles left-to-right and right-to-left associativity
- **Error Handling**: Detects malformed expressions

### Parse Mathematical Expressions
- **Token → Tree Conversion**: Transforms token streams into AST
- **Grammar Implementation**: Implements mathematical expression grammar
- **Tree Construction**: Creates hierarchical expression representations

### Tree-Based Representation
- **AST Creation**: Builds Abstract Syntax Trees using node classes
- **Hierarchical Structure**: Maintains parent-child relationships
- **Immutable Design**: Safe for symbolic manipulation

## Code Architecture

### Core Classes

#### `Parser` Class
```python
class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current_pos = 0
```

**Purpose**: Main parsing engine that processes token streams.

**State Management**:
- `tokens`: List of tokens from tokenizer
- `current_pos`: Current position in token stream
- **Lookahead**: Single token lookahead for parsing decisions

### Parsing Strategy: Recursive Descent

The parser uses **recursive descent parsing** with **operator precedence** handling:

```
Grammar Hierarchy (Precedence Order):
1. addition → multiplication (('+' | '-') multiplication)*
2. multiplication → exponentiation (('*' | '/') exponentiation)*  
3. exponentiation → primary ('^' exponentiation)?
4. primary → NUMBER | VARIABLE | '(' addition ')'
```

## Algorithm Implementation

### Main Parsing Entry Point
```python
def parse(self) -> Node:
    result = self._parse_addition()  # Start with lowest precedence
    
    if not self._is_at_end():
        raise ValueError(f"Unexpected token: {self._peek()}")
    
    return result
```

**Design Principles**:
- **Top-Down**: Starts with lowest precedence (addition)
- **Complete Consumption**: Ensures all tokens are processed
- **Error Detection**: Catches unexpected tokens

### Addition/Subtraction Parsing (Lowest Precedence)
```python
def _parse_addition(self) -> Node:
    left = self._parse_multiplication()
    
    while self._match('OPERATOR', '+') or self._match('OPERATOR', '-'):
        operator = self._previous().value
        right = self._parse_multiplication()
        left = BinaryOp(left, operator, right)
    
    return left
```

**Algorithm Characteristics**:
- **Left Associative**: `a + b + c` → `(a + b) + c`
- **Recursive**: Calls higher precedence parser
- **Loop Structure**: Handles multiple consecutive operations
- **Tree Building**: Creates BinaryOp nodes

**Example**: `2 + 3 - 1`
```
Step 1: left = 2 (from multiplication)
Step 2: Match '+', right = 3, left = BinaryOp(2, '+', 3)
Step 3: Match '-', right = 1, left = BinaryOp(BinaryOp(2, '+', 3), '-', 1)
```

### Multiplication/Division Parsing (Medium Precedence)
```python
def _parse_multiplication(self) -> Node:
    left = self._parse_exponentiation()
    
    while self._match('OPERATOR', '*') or self._match('OPERATOR', '/'):
        operator = self._previous().value
        right = self._parse_exponentiation()
        left = BinaryOp(left, operator, right)
    
    return left
```

**Same Pattern as Addition**:
- **Left Associative**: `a * b * c` → `(a * b) * c`
- **Higher Precedence**: Called by addition parser
- **Consistent Structure**: Same loop-based approach

### Exponentiation Parsing (Highest Precedence, Right-Associative)
```python
def _parse_exponentiation(self) -> Node:
    left = self._parse_primary()
    
    if self._match('OPERATOR', '^'):
        right = self._parse_exponentiation()  # Right-associative!
        left = BinaryOp(left, '^', right)
    
    return left
```

**Key Difference - Right Associativity**:
- **Recursive Call**: Calls itself for right operand
- **Right Associative**: `a^b^c` → `a^(b^c)`
- **Single Match**: Only handles one exponentiation per call

**Example**: `2^3^2`
```
Step 1: left = 2 (from primary)
Step 2: Match '^', right = 3^2 (recursive call)
Step 3: Result = BinaryOp(2, '^', BinaryOp(3, '^', 2))
```

### Primary Expression Parsing (Base Cases)
```python
def _parse_primary(self) -> Node:
    if self._match('NUMBER'):
        return Number(self._previous().value)
    
    if self._match('VARIABLE'):
        return Variable(self._previous().value)
    
    if self._match('LPAREN'):
        expr = self._parse_addition()  # Parse nested expression
        if not self._match('RPAREN'):
            raise ValueError("Expected ')' after expression")
        return expr
    
    raise ValueError(f"Expected number, variable, or '(', got {self._peek()}")
```

**Handles Base Cases**:
- **Numbers**: `5`, `3.14`, `-2`
- **Variables**: `x`, `y`, `z`
- **Parentheses**: `(expression)` with proper nesting

## Lookahead and Matching

### Token Matching Algorithm
```python
def _match(self, token_type: str, value: Optional[str] = None) -> bool:
    if self._is_at_end():
        return False
    
    current = self._peek()
    
    if value is not None:
        if current.type == token_type and current.value == value:
            self.current_pos += 1
            return True
    else:
        if current.type == token_type:
            self.current_pos += 1
            return True
    
    return False
```

**Lookahead Mechanism**:
- **Non-Destructive**: `peek()` doesn't advance position
- **Conditional Advance**: `match()` advances only on success
- **Type and Value**: Can match by type alone or type+value

### Position Management
```python
def _peek(self) -> Token:
    if self._is_at_end():
        raise ValueError("Unexpected end of input")
    return self.tokens[self.current_pos]

def _is_at_end(self) -> bool:
    return (self.current_pos >= len(self.tokens) or 
            self.tokens[self.current_pos].type == 'EOF')
```

**Safe Access**:
- **Bounds Checking**: Prevents out-of-bounds access
- **EOF Handling**: Properly detects end of input
- **Error Messages**: Clear error reporting

## Operator Precedence Implementation

### PEMDAS Compliance
```
Precedence (High to Low):
1. Parentheses: ()           (handled in primary)
2. Exponents: ^              (right-associative)
3. Multiplication/Division: *, /  (left-associative)
4. Addition/Subtraction: +, -     (left-associative)
```

### Associativity Handling

#### Left Associative Operations
```python
# For +, -, *, /
left = parse_higher_precedence()
while match_operator():
    operator = get_operator()
    right = parse_higher_precedence()
    left = BinaryOp(left, operator, right)
```

**Result**: `a + b + c` → `(a + b) + c`

#### Right Associative Operations
```python
# For ^
left = parse_higher_precedence()
if match_operator('^'):
    right = parse_exponentiation()  # Recursive!
    left = BinaryOp(left, '^', right)
```

**Result**: `a^b^c` → `a^(b^c)`

## Tree Construction

### Node Creation
```python
# From primary parsing
return Number(token.value)        # For numbers
return Variable(token.value)      # For variables

# From binary operations
return BinaryOp(left, operator, right)
```

### Tree Structure Examples

#### Simple Expression: `2*x + 3`
```
BinaryOp(+, 
  BinaryOp(*, Number(2), Variable(x)),
  Number(3)
)
```

#### Complex Expression: `(x + 1)^2`
```
BinaryOp(^,
  BinaryOp(+, Variable(x), Number(1)),
  Number(2)
)
```

#### Right Associative: `2^3^2`
```
BinaryOp(^,
  Number(2),
  BinaryOp(^, Number(3), Number(2))
)
```

## Error Handling Strategy

### Syntax Error Detection
```python
# Unexpected tokens
if not self._is_at_end():
    raise ValueError(f"Unexpected token: {self._peek()}")

# Missing closing parenthesis
if not self._match('RPAREN'):
    raise ValueError("Expected ')' after expression")

# Invalid primary expressions
raise ValueError(f"Expected number, variable, or '(', got {self._peek()}")
```

### Error Recovery
- **Fail Fast**: Stops at first syntax error
- **Clear Messages**: Describes what was expected
- **Context**: Shows what token caused the error

## Data Structures Used

### Token Stream
- **Type**: `List[Token]`
- **Access Pattern**: Sequential with lookahead
- **Modification**: Read-only, position tracking only

### Expression Trees
- **Root Type**: `Node` (abstract base class)
- **Leaf Types**: `Number`, `Variable`
- **Internal Types**: `BinaryOp`
- **Structure**: Hierarchical, immutable

## Performance Characteristics

### Time Complexity
- **Overall**: O(n) where n is number of tokens
- **Per Expression**: Linear in expression size
- **Memory**: O(n) for tree storage

### Space Complexity
- **Tree Storage**: O(n) where n is expression complexity
- **Stack Depth**: O(d) where d is nesting depth
- **Working Memory**: O(1) for position tracking

## Integration Points

### Tokenizer Integration
```python
def parse_expression(text: str) -> Node:
    tokens = tokenize(text)      # From tokenizer
    parser = Parser(tokens)      # Create parser
    return parser.parse()        # Build tree
```

### Node Integration
- **Creates Node Instances**: Uses Number, Variable, BinaryOp
- **Tree Structure**: Builds hierarchical relationships
- **Method Calls**: Nodes handle evaluation and differentiation

## Testing and Validation

### Test Cases
```python
test_cases = [
    "2*x + 3",        # Basic precedence
    "(x + 1)^2",      # Parentheses
    "x^3 - 2*x",      # Mixed operations
    "2^3^2",          # Right associativity
    "2*3 + 4*5",      # Left associativity
]
```

### Validation Points
- **Precedence**: Correct operator precedence
- **Associativity**: Proper left/right associativity
- **Parentheses**: Correct nesting and matching
- **Error Handling**: Invalid syntax detection

## Extensibility

### Adding New Operators
1. **Update Tokenizer**: Add operator to tokenizer
2. **Add Precedence Level**: Create new parsing method
3. **Update Grammar**: Modify precedence hierarchy
4. **Add Node Support**: Update BinaryOp handling

### Adding New Primary Types
1. **Extend Primary Parser**: Add new token type handling
2. **Create Node Class**: Implement new node type
3. **Update Grammar**: Add to primary expression rules

## Code Quality Features

### Design Patterns
- **Recursive Descent**: Clean, maintainable parsing logic
- **Visitor Pattern**: Tree traversal for operations
- **Immutable Trees**: Safe symbolic manipulation

### Error Handling
- **Comprehensive**: Covers all syntax error cases
- **Informative**: Clear error messages with context
- **Consistent**: Uniform error handling approach

### Documentation
- **Method Documentation**: Every method documented
- **Algorithm Explanation**: Detailed parsing logic
- **Examples**: Usage examples and test cases

## Conclusion

The parser module successfully implements the **syntax analysis phase** of our robust parser requirement. It provides:

- **Correct Precedence**: Implements PEMDAS accurately
- **Proper Associativity**: Handles left and right associativity
- **Tree Construction**: Creates structured expression trees
- **Error Detection**: Catches syntax errors early
- **Clean Integration**: Works seamlessly with tokenizer and nodes

This module fulfills the core requirements for **parsing mathematical expressions** and **tree-based representation**, enabling the symbolic differentiation system to operate on properly structured expression trees.
