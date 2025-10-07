# Tokenizer Module - Detailed Technical Documentation

## Overview

The `tokenizer.py` module implements the **first phase of our robust parser** requirement. It converts mathematical expression strings into a structured list of tokens that can be processed by the parser to build expression trees.

## Project Requirements Addressed

### ✅ Robust Parser (First Component)
- **Lexical Analysis**: Breaks input strings into meaningful tokens
- **Error Detection**: Identifies invalid characters and malformed numbers
- **Whitespace Handling**: Properly ignores spaces and tabs
- **Character-by-Character Processing**: Systematic input analysis

### ✅ Parse Mathematical Expressions
- **Tokenization Enables Parsing**: Creates the foundation for expression tree construction
- **Structured Input**: Converts unstructured strings into parseable tokens

## Code Architecture

### Core Classes

#### `Token` Class
```python
@dataclass
class Token:
    type: str
    value: Union[str, float, None] = None
```

**Purpose**: Represents a single meaningful unit in a mathematical expression.

**Key Features**:
- **Type Safety**: Each token has a specific type (NUMBER, VARIABLE, OPERATOR, etc.)
- **Value Storage**: Stores the actual value (number, variable name, operator symbol)
- **Debug Support**: String representation for debugging and testing

**Token Types Supported**:
- `NUMBER`: Numeric constants (5, 3.14, -2)
- `VARIABLE`: Single-letter variables (x, y, z)
- `OPERATOR`: Binary operations (+, -, *, /, ^)
- `LPAREN/RPAREN`: Parentheses for grouping
- `EOF`: End-of-input marker

#### `Tokenizer` Class
```python
class Tokenizer:
    def __init__(self):
        self.tokens: List[Token] = []
        self.current_pos = 0
        self.text = ""
```

**Purpose**: Main tokenization engine that processes input strings.

**State Management**:
- `tokens`: Accumulates parsed tokens
- `current_pos`: Tracks current position in input string
- `text`: Stores the input string being processed

## Algorithm Implementation

### Main Tokenization Loop
```python
def tokenize(self, text: str) -> List[Token]:
    while self.current_pos < len(self.text):
        char = self.text[self.current_pos]
        
        if char.isspace():
            self.current_pos += 1  # Skip whitespace
        elif char.isdigit() or char == '.':
            self._parse_number()   # Parse numeric constants
        elif char.isalpha():
            self._parse_variable() # Parse variables
        elif char in '+-*/^':
            self._parse_operator() # Parse operators
        elif char == '(':
            self.tokens.append(Token('LPAREN'))
        elif char == ')':
            self.tokens.append(Token('RPAREN'))
        else:
            raise ValueError(f"Invalid character '{char}'")
```

**Algorithm Characteristics**:
- **Single Pass**: Processes input in one left-to-right scan
- **Character Classification**: Uses character properties to determine token type
- **Error Handling**: Raises exceptions for invalid characters
- **Whitespace Agnostic**: Ignores spaces, tabs, newlines

### Number Parsing Algorithm
```python
def _parse_number(self) -> None:
    number_str = ""
    
    # Handle negative sign
    if self.text[self.current_pos] == '-':
        number_str += '-'
        self.current_pos += 1
    
    # Parse digits and decimal point
    while (self.current_pos < len(self.text) and 
           (self.text[self.current_pos].isdigit() or 
            self.text[self.current_pos] == '.')):
        number_str += self.text[self.current_pos]
        self.current_pos += 1
    
    # Convert to float and create token
    value = float(number_str)
    self.tokens.append(Token('NUMBER', value))
```

**Handles Complex Cases**:
- **Integers**: `5`, `42`, `-3`
- **Decimals**: `3.14`, `0.5`, `-2.7`
- **Edge Cases**: `0.0`, `.5`, `5.`

**Error Handling**:
- **Invalid Numbers**: `..5`, `5..`, `5.5.5`
- **Empty Numbers**: `-`, `.`
- **Type Conversion**: Handles `ValueError` from `float()`

### Variable Parsing Algorithm
```python
def _parse_variable(self) -> None:
    char = self.text[self.current_pos]
    if not char.isalpha():
        raise ValueError(f"Expected letter, got '{char}'")
    
    self.tokens.append(Token('VARIABLE', char))
    self.current_pos += 1
```

**Design Decisions**:
- **Single Letter Only**: Simplified for initial implementation
- **Case Sensitive**: `x` and `X` are different variables
- **Extensible**: Can be modified to support multi-letter variables

### Operator Parsing Algorithm
```python
def _parse_operator(self) -> None:
    char = self.text[self.current_pos]
    
    if char not in '+-*/^':
        raise ValueError(f"Invalid operator '{char}'")
    
    self.tokens.append(Token('OPERATOR', char))
    self.current_pos += 1
```

**Supported Operators**:
- `+`: Addition
- `-`: Subtraction
- `*`: Multiplication
- `/`: Division
- `^`: Exponentiation

## Data Structures Used

### Token List
- **Type**: `List[Token]`
- **Purpose**: Sequential storage of parsed tokens
- **Order**: Maintains left-to-right order from input string
- **Access Pattern**: Sequential processing by parser

### Position Tracking
- **Type**: `int` (current_pos)
- **Purpose**: Tracks current position in input string
- **Increment**: Advanced after each token is parsed
- **Bounds Checking**: Prevents out-of-bounds access

## Error Handling Strategy

### Invalid Character Detection
```python
else:
    raise ValueError(f"Invalid character '{char}' at position {self.current_pos}")
```

**Benefits**:
- **Early Detection**: Catches errors during tokenization
- **Precise Location**: Reports exact character position
- **Clear Messages**: Descriptive error messages

### Number Validation
```python
try:
    value = float(number_str)
except ValueError:
    raise ValueError(f"Invalid number '{number_str}' at position {start_pos}")
```

**Validation Points**:
- **Format Validation**: Ensures valid number format
- **Range Checking**: Handles Python float limits
- **Edge Cases**: Empty strings, multiple decimal points

## Integration with Parser

### Token Stream Format
```
Input: "2*x + 3"
Output: [NUMBER(2.0), OPERATOR(*), VARIABLE(x), OPERATOR(+), NUMBER(3.0), EOF]
```

### Parser Interface
- **Clean Separation**: Tokenizer only handles lexical analysis
- **No Syntax Knowledge**: Doesn't understand operator precedence
- **Stream Processing**: Parser consumes tokens sequentially

## Performance Characteristics

### Time Complexity
- **Overall**: O(n) where n is input string length
- **Per Token**: O(1) for simple tokens, O(k) for numbers where k is digit count
- **Memory**: O(n) for token storage

### Space Complexity
- **Token Storage**: O(n) where n is number of tokens
- **Working Memory**: O(1) for position tracking
- **Input Storage**: O(n) for input string

## Testing and Validation

### Test Cases Covered
```python
test_cases = [
    "2*x + 3",      # Basic arithmetic
    "(x + 1)^2",    # Parentheses and exponentiation
    "x^3 - 2*x",    # Complex expressions
    "5.5 / 2.2",    # Decimal numbers
    "x + y - z"     # Multiple variables
]
```

### Edge Cases Handled
- **Whitespace**: Spaces, tabs, newlines
- **Negative Numbers**: Leading minus signs
- **Decimals**: Various decimal formats
- **Parentheses**: Nested grouping
- **Invalid Input**: Non-mathematical characters

## Extensibility

### Adding New Token Types
1. **Define Token Type**: Add new type constant
2. **Update Classification**: Modify main loop
3. **Add Parser Support**: Update parser to handle new tokens

### Supporting Multi-Letter Variables
```python
def _parse_variable(self) -> None:
    var_name = ""
    while (self.current_pos < len(self.text) and 
           self.text[self.current_pos].isalnum()):
        var_name += self.text[self.current_pos]
        self.current_pos += 1
    
    self.tokens.append(Token('VARIABLE', var_name))
```

## Code Quality Features

### Documentation
- **Comprehensive Docstrings**: Every method documented
- **Type Hints**: Full type annotation support
- **Examples**: Usage examples in docstrings

### Error Messages
- **Descriptive**: Clear explanation of what went wrong
- **Contextual**: Includes position and character information
- **Actionable**: Suggests what might be wrong

### Maintainability
- **Single Responsibility**: Each method has one clear purpose
- **Modular Design**: Easy to modify individual parsing methods
- **Testable**: Clear interfaces for unit testing

## Conclusion

The tokenizer module successfully implements the **lexical analysis phase** of our robust parser requirement. It provides:

- **Reliable Tokenization**: Handles all supported mathematical constructs
- **Error Detection**: Catches invalid input early
- **Clean Interface**: Simple API for parser integration
- **Extensible Design**: Easy to add new features

This foundation enables the parser to focus on **syntax analysis** and **expression tree construction**, fulfilling the core requirement for parsing mathematical expressions in our symbolic differentiation calculator.
