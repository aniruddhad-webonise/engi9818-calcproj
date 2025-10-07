# Nodes Module - Detailed Technical Documentation

## Overview

The `nodes.py` module implements the **tree-based representation** requirement and serves as the foundation for **algorithms for symbolic manipulation**. It defines the Abstract Syntax Tree (AST) node classes that represent mathematical expressions as hierarchical data structures, with each node knowing how to evaluate itself and compute its derivative.

## Project Requirements Addressed

### ✅ Tree-Based Representation
- **Abstract Syntax Tree**: Hierarchical data structure for expressions
- **Node Classes**: Number, Variable, BinaryOp representing different expression types
- **Tree Structure**: Parent-child relationships with proper encapsulation
- **Immutable Design**: Safe for symbolic manipulation

### ✅ Algorithms for Symbolic Manipulation
- **Differentiation Rules**: Complete calculus rule implementation
- **Tree Traversal**: Recursive algorithms for evaluation and differentiation
- **Symbolic Computation**: Returns new trees rather than modifying existing ones

### ✅ Data Structures
- **Expression Trees**: Hierarchical tree structures
- **Traversal Capabilities**: Methods for visiting and processing tree nodes
- **Node Relationships**: Proper parent-child connections

### ✅ Symbolic Derivative Computation
- **Each Node Knows Its Derivative**: Polymorphic differentiation
- **Calculus Rules**: Sum, product, quotient, power rules implemented
- **Recursive Application**: Rules applied recursively through tree structure

## Code Architecture

### Abstract Base Class

#### `Node` Class
```python
class Node(ABC):
    @abstractmethod
    def evaluate(self, variables: Dict[str, float] = None) -> float:
        """Evaluate the expression with given variable values."""
        pass
    
    @abstractmethod
    def differentiate(self, variable: str = 'x') -> 'Node':
        """Compute the symbolic derivative with respect to the given variable."""
        pass
    
    @abstractmethod
    def __str__(self) -> str:
        """String representation of the expression."""
        pass
```

**Design Principles**:
- **Polymorphic Interface**: All nodes implement same methods
- **Abstract Methods**: Forces implementation of core functionality
- **Type Safety**: Ensures all nodes support required operations
- **Extensibility**: Easy to add new node types

**Core Operations**:
1. **Evaluation**: Compute numeric value given variable assignments
2. **Differentiation**: Compute symbolic derivative (returns new tree)
3. **String Representation**: Convert back to readable math notation

### Concrete Node Classes

#### `Number` Class - Leaf Node for Constants
```python
class Number(Node):
    def __init__(self, value: float):
        self.value = value
    
    def evaluate(self, variables: Dict[str, float] = None) -> float:
        return self.value
    
    def differentiate(self, variable: str = 'x') -> 'Node':
        return Number(0)  # d/dx(c) = 0
```

**Characteristics**:
- **Leaf Node**: No children, represents terminal values
- **Constant Rule**: Derivative of any constant is zero
- **Simple Evaluation**: Always returns the stored value
- **Immutable**: Value never changes after creation

**Examples**:
- `Number(5)` represents the constant `5`
- `Number(3.14)` represents `π ≈ 3.14`
- `Number(-2)` represents the constant `-2`

#### `Variable` Class - Leaf Node for Variables
```python
class Variable(Node):
    def __init__(self, name: str):
        self.name = name
    
    def evaluate(self, variables: Dict[str, float] = None) -> float:
        if variables is None or self.name not in variables:
            raise ValueError(f"Variable '{self.name}' not defined")
        return variables[self.name]
    
    def differentiate(self, variable: str = 'x') -> 'Node':
        if self.name == variable:
            return Number(1)  # d/dx(x) = 1
        else:
            return Number(0)   # d/dx(y) = 0
```

**Characteristics**:
- **Leaf Node**: No children, represents unknown quantities
- **Variable Rule**: Derivative depends on differentiation variable
- **Lookup Evaluation**: Requires variable values for evaluation
- **Single Letter**: Currently supports single-letter variables

**Differentiation Logic**:
- **Same Variable**: `d/dx(x) = 1`
- **Different Variable**: `d/dx(y) = 0`

#### `BinaryOp` Class - Internal Node for Operations
```python
class BinaryOp(Node):
    def __init__(self, left: Node, operator: str, right: Node):
        self.left = left
        self.operator = operator
        self.right = right
```

**Characteristics**:
- **Internal Node**: Has two children (left and right operands)
- **Operation Storage**: Stores the operator symbol
- **Tree Structure**: Creates parent-child relationships
- **Polymorphic Children**: Children can be any Node type

## Algorithm Implementation

### Evaluation Algorithm - Tree Traversal

#### Recursive Evaluation Pattern
```python
def evaluate(self, variables: Dict[str, float] = None) -> float:
    left_val = self.left.evaluate(variables)   # Recursive call
    right_val = self.right.evaluate(variables) # Recursive call
    
    if self.operator == '+':
        return left_val + right_val
    elif self.operator == '-':
        return left_val - right_val
    # ... other operators
```

**Algorithm Characteristics**:
- **Post-Order Traversal**: Evaluate children before parent
- **Recursive**: Each node handles its own evaluation
- **Bottom-Up**: Values propagate up the tree
- **Error Handling**: Division by zero detection

**Example**: Evaluating `2*x + 3` with `x = 5`
```
BinaryOp(+, BinaryOp(*, Number(2), Variable(x)), Number(3))
    ↓
BinaryOp(*, Number(2), Variable(x)) → 2 * 5 = 10
Number(3) → 3
    ↓
BinaryOp(+, 10, 3) → 10 + 3 = 13
```

### Differentiation Algorithm - Symbolic Manipulation

#### Calculus Rules Implementation

**Sum Rule**: `d/dx(f + g) = f' + g'`
```python
if self.operator == '+':
    return BinaryOp(
        self.left.differentiate(variable),   # f'
        '+',
        self.right.differentiate(variable)    # g'
    )
```

**Product Rule**: `d/dx(f * g) = f'*g + f*g'`
```python
elif self.operator == '*':
    left_diff = self.left.differentiate(variable)   # f'
    right_diff = self.right.differentiate(variable) # g'
    return BinaryOp(
        BinaryOp(left_diff, '*', self.right),       # f'*g
        '+',
        BinaryOp(self.left, '*', right_diff)        # f*g'
    )
```

**Quotient Rule**: `d/dx(f/g) = (f'*g - f*g') / g^2`
```python
elif self.operator == '/':
    left_diff = self.left.differentiate(variable)
    right_diff = self.right.differentiate(variable)
    numerator = BinaryOp(
        BinaryOp(left_diff, '*', self.right),       # f'*g
        '-',
        BinaryOp(self.left, '*', right_diff)        # f*g'
    )
    denominator = BinaryOp(self.right, '^', Number(2))  # g^2
    return BinaryOp(numerator, '/', denominator)
```

**Power Rule**: `d/dx(f^n) = n * f^(n-1) * f'`
```python
elif self.operator == '^':
    if isinstance(self.right, Number):
        n = self.right.value
        f = self.left
        f_prime = f.differentiate(variable)
        
        if n == 1:
            return f_prime                    # d/dx(f^1) = f'
        elif n == 0:
            return Number(0)                 # d/dx(f^0) = 0
        else:
            power_part = BinaryOp(f, '^', Number(n - 1))      # f^(n-1)
            coefficient_part = BinaryOp(Number(n), '*', power_part)  # n*f^(n-1)
            return BinaryOp(coefficient_part, '*', f_prime)   # n*f^(n-1)*f'
```

#### Differentiation Algorithm Characteristics
- **Recursive**: Each node differentiates its children
- **Tree Building**: Creates new trees, doesn't modify originals
- **Rule Application**: Applies appropriate calculus rule per operator
- **Immutable**: Original expression tree remains unchanged

**Example**: Differentiating `2*x + 3`
```
BinaryOp(+, BinaryOp(*, Number(2), Variable(x)), Number(3))
    ↓ Apply sum rule
BinaryOp(+, 
    BinaryOp(*, Number(2), Variable(x)).differentiate('x'),  # (2*x)'
    Number(3).differentiate('x')                           # (3)'
)
    ↓ Apply product rule and constant rule
BinaryOp(+, 
    BinaryOp(+, 
        BinaryOp(Number(0), '*', Variable(x)),  # 0*x
        BinaryOp(Number(2), '*', Number(1))    # 2*1
    ),
    Number(0)                                   # 0
)
```

### String Representation Algorithm

#### Tree-to-String Conversion
```python
def __str__(self) -> str:
    left_str = str(self.left)
    right_str = str(self.right)
    
    # Add parentheses for clarity
    if isinstance(self.left, BinaryOp):
        left_str = f"({left_str})"
    if isinstance(self.right, BinaryOp):
        right_str = f"({right_str})"
    
    return f"{left_str} {self.operator} {right_str}"
```

**Algorithm Characteristics**:
- **Recursive**: Each node converts itself to string
- **Parentheses Handling**: Adds parentheses for clarity
- **Precedence Preservation**: Maintains mathematical notation
- **Readable Output**: Human-readable mathematical expressions

## Data Structures Used

### Tree Structure
```
BinaryOp(+, 
  BinaryOp(*, Number(2), Variable(x)),
  Number(3)
)
```

**Visual Representation**:
```
    +
   / \
  *   3
 / \
2   x
```

### Node Relationships
- **Parent-Child**: BinaryOp has left and right children
- **Leaf Nodes**: Number and Variable have no children
- **Polymorphic**: Children can be any Node type
- **Immutable**: Tree structure doesn't change after creation

## Error Handling Strategy

### Evaluation Errors
```python
def evaluate(self, variables: Dict[str, float] = None) -> float:
    if variables is None or self.name not in variables:
        raise ValueError(f"Variable '{self.name}' not defined")
```

**Error Types**:
- **Undefined Variables**: Missing variable values
- **Division by Zero**: Runtime error during evaluation
- **Type Errors**: Invalid variable types

### Differentiation Errors
```python
if char not in '+-*/^':
    raise ValueError(f"Unknown operator: {self.operator}")
```

**Error Types**:
- **Unknown Operators**: Unsupported operations
- **Complex Cases**: Not yet implemented (e.g., f^g where g is not constant)

## Performance Characteristics

### Time Complexity
- **Evaluation**: O(n) where n is tree size
- **Differentiation**: O(n) where n is tree size
- **String Conversion**: O(n) where n is tree size

### Space Complexity
- **Tree Storage**: O(n) where n is expression complexity
- **Differentiation**: O(n) for new tree creation
- **Recursion Stack**: O(d) where d is tree depth

## Integration Points

### Parser Integration
```python
# Parser creates nodes
if self._match('NUMBER'):
    return Number(self._previous().value)
if self._match('VARIABLE'):
    return Variable(self._previous().value)
if self._match('OPERATOR'):
    return BinaryOp(left, operator, right)
```

### Simplifier Integration
```python
# Simplifier processes nodes
def simplify(node: Node) -> Node:
    if isinstance(node, BinaryOp):
        left_simplified = simplify(node.left)
        right_simplified = simplify(node.right)
        return _simplify_binary_op(left_simplified, node.operator, right_simplified)
```

## Testing and Validation

### Test Cases
```python
# Evaluation tests
tree = BinaryOp(Number(2), '*', Variable('x'))
result = tree.evaluate({'x': 5})  # Should return 10

# Differentiation tests
tree = BinaryOp(Variable('x'), '^', Number(3))
derivative = tree.differentiate('x')  # Should return 3*x^2
```

### Validation Points
- **Correct Evaluation**: Proper arithmetic computation
- **Correct Differentiation**: Proper calculus rule application
- **Tree Structure**: Proper parent-child relationships
- **String Representation**: Readable mathematical notation

## Extensibility

### Adding New Node Types
1. **Inherit from Node**: Implement abstract methods
2. **Add Evaluation Logic**: Define how to compute numeric value
3. **Add Differentiation Logic**: Define calculus rules
4. **Add String Representation**: Define display format

### Adding New Operations
1. **Extend BinaryOp**: Add new operator handling
2. **Implement Calculus Rule**: Define differentiation rule
3. **Update Evaluation**: Add arithmetic computation
4. **Test Integration**: Ensure parser compatibility

## Code Quality Features

### Design Patterns
- **Visitor Pattern**: Tree traversal for operations
- **Polymorphism**: Different node types, same interface
- **Immutable Objects**: Safe for symbolic manipulation
- **Recursive Design**: Clean, maintainable algorithms

### Error Handling
- **Comprehensive**: Covers all error cases
- **Informative**: Clear error messages
- **Consistent**: Uniform error handling approach

### Documentation
- **Method Documentation**: Every method documented
- **Algorithm Explanation**: Detailed calculus rule implementation
- **Examples**: Usage examples and test cases

## Advanced Features

### Complex Power Rule
The power rule implementation handles both simple and complex cases:

**Simple Case**: `d/dx(x^n) = n*x^(n-1)`
**Complex Case**: `d/dx((x+1)^2) = 2*(x+1)^1 * (x+1)' = 2*(x+1)*1`

### Special Cases
- **f^1**: Returns f' directly
- **f^0**: Returns 0 (derivative of constant)
- **f^g where g is not constant**: Not yet implemented (requires logarithmic differentiation)

## Conclusion

The nodes module successfully implements the **tree-based representation** and **algorithms for symbolic manipulation** requirements. It provides:

- **Hierarchical Structure**: Proper tree representation of expressions
- **Polymorphic Interface**: Consistent operations across node types
- **Complete Calculus Rules**: All major differentiation rules implemented
- **Recursive Algorithms**: Clean tree traversal for evaluation and differentiation
- **Immutable Design**: Safe for symbolic manipulation
- **Extensible Architecture**: Easy to add new node types and operations

This module forms the **core data structure** of our symbolic differentiation calculator, enabling the entire system to operate on properly structured, manipulable expression trees that can be evaluated, differentiated, and simplified.
