# Command-Line Calculator with Symbolic Differentiation

A Python implementation of a command-line calculator that performs basic arithmetic and computes symbolic derivatives of mathematical expressions.

## Project Overview

This project implements a **Command-Line Calculator with Symbolic Differentiation** that addresses all the core requirements:

- **Robust Parser**: Tokenization + recursive descent parsing
- **Tree-Based Representation**: Abstract Syntax Tree (AST) with node classes
- **Symbolic Differentiation**: Complete calculus rules implementation
- **Algorithms for Symbolic Manipulation**: Differentiation + simplification
- **Data Structures**: Expression trees with traversal capabilities
- **Command-Line Interface**: Interactive and single-expression modes

## Features

### Core Functionality
- **Parse Mathematical Expressions**: Convert strings to expression trees
- **Symbolic Differentiation**: Compute derivatives using calculus rules
- **Expression Evaluation**: Evaluate expressions with variable substitution
- **Expression Simplification**: Clean up derivative expressions
- **Tree Visualization**: Display expression trees as ASCII art diagrams
- **Interactive CLI**: User-friendly command-line interface

### Supported Operations
- **Arithmetic**: `+`, `-`, `*`, `/`, `^` (exponentiation)
- **Variables**: Single-letter variables (`x`, `y`, `z`, etc.)
- **Parentheses**: Grouping expressions `(x + 1)^2`
- **Operator Precedence**: PEMDAS with proper associativity

### Differentiation Rules
- **Constant Rule**: `d/dx(c) = 0`
- **Variable Rule**: `d/dx(x) = 1`, `d/dx(y) = 0`
- **Sum Rule**: `d/dx(f + g) = f' + g'`
- **Product Rule**: `d/dx(f * g) = f'*g + f*g'`
- **Quotient Rule**: `d/dx(f/g) = (f'*g - f*g') / g^2`
- **Power Rule**: `d/dx(f^n) = n * f^(n-1) * f'`

## Project Structure

```
proj_calc/
├── main.py                 # Command-line interface
├── README.md              # Project documentation
├── src/
│   ├── __init__.py        # Package initialization with module metadata
│   ├── nodes.py           # Expression tree node classes
│   ├── tokenizer.py       # Tokenization logic
│   ├── parser.py          # Parsing logic
│   ├── simplifier.py      # Expression simplification
│   └── tree_visualizer.py  # Tree visualization utilities
└── tests/                 # Test files (future)
```

## Installation & Usage

### Prerequisites
- Python 3.7+

### Running the Calculator

#### Interactive Mode
```bash
python main.py
```

#### Single Expression Mode
```bash
python main.py "2*x + 3"
python main.py "x^3 - 2*x"
python main.py "(x + 1)^2"
```

### Interactive Commands

#### Basic Commands
- `help` - Show help information
- `quit` - Exit the calculator
- `clear` - Clear all variable values
- `vars` - Show current variable values

#### Expression Commands
- `diff <expression>` - Differentiate expression
- `eval <expression>` - Evaluate expression
- `tree <expression>` - Show expression tree structure
- `set <var> <value>` - Set variable value

#### Advanced Usage
- `diff <expr> wrt <var>` - Differentiate with respect to specific variable
- `eval <expr> at x=5` - Evaluate with specific variable values
- `tree <expr> simple` - Show simple tree view

## 📝 Examples

### Symbolic Differentiation
```
calc> diff 2*x + 3
d/dx(2*x + 3) = 2.0

calc> diff x^3 - 2*x
d/dx(x^3 - 2*x) = (3.0 * (x ^ 2.0)) - 2.0

calc> diff (x + 1)^2
d/dx((x + 1)^2) = 2.0 * (x + 1.0)
```

### Expression Evaluation
```
calc> set x 5
Set x = 5.0

calc> eval x^2 + 2*x + 1
x^2 + 2*x + 1 = 36.0

calc> eval x^2 + y^2 at y=3
x^2 + y^2 = 34.0
```

### Advanced Differentiation
```
calc> diff x^2 + y^2 wrt y
d/dy(x^2 + y^2) = (0 + (2.0 * y))
```

### Tree Visualization
```
calc> tree 2*x + 3
Expression tree for '2*x + 3':
                                      '+'                                       
                               ┌──────────────┐                                 
                                '*'   Number(3.0)                               
                             ┌──────────────────┐                               
                            Number(2.0) Variable(x)                             

calc> tree (x + 1)^2 simple
Expression tree for '(x + 1)^2':
((x + 1.0) ^ 2.0)
```

## Testing

Run individual component tests:
```bash
python src/tokenizer.py       # Test tokenization
python src/parser.py          # Test parsing
python src/simplifier.py      # Test simplification
python src/tree_visualizer.py # Test tree visualization
```

Test the complete module:
```bash
python -c "import src; print(src.get_module_info())"
```

## Architecture

### Design Patterns
- **Visitor Pattern**: Tree traversal for evaluation and differentiation
- **Recursive Descent Parser**: Clean, maintainable parsing logic
- **Immutable Trees**: Safe symbolic manipulation

### Key Components

1. **Tokenizer** (`tokenizer.py`): Converts strings to tokens
2. **Parser** (`parser.py`): Builds expression trees from tokens
3. **Nodes** (`nodes.py`): AST node classes with evaluation/differentiation
4. **Simplifier** (`simplifier.py`): Cleans up derivative expressions
5. **Tree Visualizer** (`tree_visualizer.py`): Displays expression trees as ASCII art
6. **CLI** (`main.py`): User interface and orchestration

### Data Flow
```
String → Tokenizer → Tokens → Parser → AST → Differentiator → Simplified AST → String
                                 ↓
                            Tree Visualizer → ASCII Art
```

## Technical Details

### Module Structure
The `src/` module provides a comprehensive API with:
- **Clean Imports**: `from src import parse_expression, simplify_expression, visualize_tree`
- **Module Introspection**: `src.get_module_info()`, `src.get_component_count()`
- **Self-Documenting**: Complete metadata about components, features, and capabilities
- **Easy Testing**: Individual component testing and full module validation

### Operator Precedence
- **Parentheses**: `()` (highest precedence)
- **Exponentiation**: `^` (right-associative)
- **Multiplication/Division**: `*`, `/` (left-associative)
- **Addition/Subtraction**: `+`, `-` (left-associative)

### Error Handling
- Invalid characters in expressions
- Malformed mathematical expressions
- Undefined variables during evaluation
- Division by zero detection
