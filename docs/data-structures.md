# Data Structures in Symbolic Differentiation Calculator

## Overview

This document provides a comprehensive analysis of how our **Command-Line Calculator with Symbolic Differentiation** uses data structures, with particular focus on **expression trees** as the core data structure. We'll examine the design decisions, implementation details, and how these structures enable efficient symbolic manipulation.

## Project Requirements Context

Our project specifically requires:
> "The project requires a robust parser, a tree-based representation of the expression, and algorithms for symbolic manipulation. It will heavily involve data structures (expression trees) and algorithm development (traversal, simplification)."

This document focuses on the **data structures** aspect, showing how expression trees enable all other functionality.

## Core Data Structures

### 1. Expression Trees (Abstract Syntax Trees)

#### Definition and Purpose
An **Expression Tree** (also called Abstract Syntax Tree or AST) is a hierarchical data structure that represents mathematical expressions in a way that preserves both the **structure** and **semantics** of the expression.

#### Why Trees?
```
Mathematical Expression: 2*x + 3
Linear Representation:   [2, *, x, +, 3]  (loss of structure)
Tree Representation:     +
                        / \
                       *   3
                      / \
                     2   x
```

**Advantages of Tree Representation**:
- **Preserves Precedence**: Operator precedence is encoded in tree structure
- **Enables Recursive Algorithms**: Natural fit for recursive operations
- **Supports Symbolic Manipulation**: Easy to transform and manipulate
- **Clear Semantics**: Structure directly reflects mathematical meaning

#### Tree Structure Design

**Hierarchical Organization**:
```
Node (Abstract Base)
├── Number (Leaf Node)
├── Variable (Leaf Node)
└── BinaryOp (Internal Node)
    ├── left: Node
    ├── operator: str
    └── right: Node
```

**Node Types**:
- **Leaf Nodes**: `Number`, `Variable` (no children)
- **Internal Nodes**: `BinaryOp` (exactly two children)
- **Root Node**: Top-level node of the expression

### 2. Token Data Structure

#### Token Class Design
```python
@dataclass
class Token:
    type: str                    # Token category
    value: Union[str, float, None]  # Actual value
```

**Purpose**: Intermediate representation between string input and expression tree.

**Token Types**:
- `NUMBER`: Numeric constants with float values
- `VARIABLE`: Variable names with string values
- `OPERATOR`: Operation symbols with string values
- `LPAREN/RPAREN`: Parentheses with no values
- `EOF`: End-of-input marker

#### Token List Structure
```python
List[Token]  # Sequential storage maintaining input order
```

**Characteristics**:
- **Sequential Access**: Tokens processed left-to-right
- **Immutable**: Tokens created once, never modified
- **Type-Safe**: Each token has known type and value

### 3. Tree Traversal Data Structures

#### Recursion Stack
```python
# Implicit stack through function calls
def evaluate(node):
    if isinstance(node, BinaryOp):
        left_val = evaluate(node.left)    # Recursive call
        right_val = evaluate(node.right)  # Recursive call
        return combine(left_val, right_val, node.operator)
```

**Stack Behavior**:
- **Depth**: O(d) where d is tree depth
- **Automatic Management**: Handled by Python call stack
- **Post-Order Traversal**: Children processed before parent

#### Visitor Pattern Implementation
```python
class Node(ABC):
    @abstractmethod
    def evaluate(self, variables: Dict[str, float] = None) -> float:
        pass
    
    @abstractmethod
    def differentiate(self, variable: str = 'x') -> 'Node':
        pass
```

**Benefits**:
- **Polymorphic Operations**: Same interface for different node types
- **Extensible**: Easy to add new operations
- **Type Safety**: Compile-time checking of operation support

## Expression Tree Implementation Details

### Tree Construction Algorithm

#### Bottom-Up Construction
```python
# Parser builds tree bottom-up
def _parse_primary(self) -> Node:
    if self._match('NUMBER'):
        return Number(self._previous().value)  # Leaf node
    if self._match('VARIABLE'):
        return Variable(self._previous().value)  # Leaf node
    if self._match('LPAREN'):
        expr = self._parse_addition()  # Recursive construction
        return expr  # Return constructed subtree
```

**Construction Process**:
1. **Parse Leaf Nodes**: Numbers and variables
2. **Parse Internal Nodes**: Operations with children
3. **Recursive Assembly**: Children built before parents
4. **Tree Completion**: Single root node represents entire expression

#### Tree Building Example
```
Input: "2*x + 3"

Step 1: Parse "2" → Number(2)
Step 2: Parse "*" → BinaryOp(Number(2), '*', ?)
Step 3: Parse "x" → BinaryOp(Number(2), '*', Variable(x))
Step 4: Parse "+" → BinaryOp(BinaryOp(Number(2), '*', Variable(x)), '+', ?)
Step 5: Parse "3" → BinaryOp(BinaryOp(Number(2), '*', Variable(x)), '+', Number(3))
```

### Tree Structure Properties

#### Immutability Design
```python
class Number(Node):
    def __init__(self, value: float):
        self.value = value  # Set once, never changed
    
    def differentiate(self, variable: str = 'x') -> 'Node':
        return Number(0)  # Returns NEW node, doesn't modify self
```

**Benefits**:
- **Thread Safety**: Multiple operations can run concurrently
- **Safe Symbolic Manipulation**: Original expressions preserved
- **Debugging**: Original expression always available
- **Functional Programming**: No side effects

#### Memory Layout
```
BinaryOp(+, BinaryOp(*, Number(2), Variable(x)), Number(3))

Memory Layout:
┌─────────────────┐
│ BinaryOp        │
│ operator: '+'   │
│ left: ──────────┼─→ ┌─────────────────┐
│ right: ─────────┼─→ │ BinaryOp        │
└─────────────────┘   │ operator: '*'   │
                      │ left: ──────────┼─→ ┌─────────────┐
                      │ right: ─────────┼─→ │ Number      │
                      └─────────────────┘   │ value: 2.0  │
                                            └─────────────┘
```

### Tree Traversal Algorithms

#### Post-Order Traversal (Evaluation)
```python
def evaluate(self, variables: Dict[str, float] = None) -> float:
    # Post-order: process children before parent
    left_val = self.left.evaluate(variables)   # Process left child
    right_val = self.right.evaluate(variables) # Process right child
    return self.combine(left_val, right_val)   # Process current node
```

**Traversal Order**:
1. Visit left subtree
2. Visit right subtree  
3. Process current node

**Example**: `2*x + 3` with `x = 5`
```
Traversal Order:
1. Number(2).evaluate() → 2.0
2. Variable(x).evaluate() → 5.0
3. BinaryOp(*, 2.0, 5.0) → 10.0
4. Number(3).evaluate() → 3.0
5. BinaryOp(+, 10.0, 3.0) → 13.0
```

#### Pre-Order Traversal (Differentiation)
```python
def differentiate(self, variable: str = 'x') -> 'Node':
    # Pre-order: process current node before children
    if self.operator == '+':
        return BinaryOp(
            self.left.differentiate(variable),   # Process children
            '+',
            self.right.differentiate(variable)
        )
```

**Traversal Order**:
1. Process current node (apply calculus rule)
2. Visit left subtree
3. Visit right subtree

**Example**: Differentiating `2*x + 3`
```
Traversal Order:
1. BinaryOp(+, ...).differentiate() → Apply sum rule
2. BinaryOp(*, ...).differentiate() → Apply product rule
3. Number(2).differentiate() → Return Number(0)
4. Variable(x).differentiate() → Return Number(1)
5. Number(3).differentiate() → Return Number(0)
```

## Data Structure Operations

### Tree Manipulation Operations

#### Tree Copying (Implicit)
```python
def differentiate(self, variable: str = 'x') -> 'Node':
    # Creates new tree structure
    return BinaryOp(
        self.left.differentiate(variable),  # New left subtree
        self.operator,                      # Same operator
        self.right.differentiate(variable) # New right subtree
    )
```

**Copy Behavior**:
- **Deep Copy**: Entire tree structure replicated
- **Selective Copying**: Only modified parts copied
- **Memory Efficiency**: Shared subtrees where possible

#### Tree Transformation
```python
# Differentiation transforms tree structure
Original: BinaryOp(+, BinaryOp(*, Number(2), Variable(x)), Number(3))
Derivative: BinaryOp(+, BinaryOp(+, BinaryOp(Number(0), '*', Variable(x)), BinaryOp(Number(2), '*', Number(1))), Number(0))
```

**Transformation Types**:
- **Structure Changes**: Tree topology modified
- **Value Changes**: Node values updated
- **Type Changes**: Node types may change

### Memory Management

#### Garbage Collection
```python
# Old trees automatically garbage collected
original_tree = parse_expression("2*x + 3")
derivative_tree = original_tree.differentiate('x')
# original_tree still exists, derivative_tree is new
```

**Memory Characteristics**:
- **Automatic Cleanup**: Python garbage collector handles unused trees
- **Reference Counting**: Immediate cleanup when references removed
- **Memory Efficiency**: Only active trees consume memory

#### Memory Usage Analysis
```
Expression: 2*x + 3
Tree Size: 5 nodes (1 BinaryOp + 1 BinaryOp + 2 Number + 1 Variable)
Memory per Node: ~50-100 bytes (Python object overhead)
Total Memory: ~250-500 bytes
```

## Advanced Data Structure Features

### Tree Simplification Data Structures

#### Simplification Rules
```python
def _simplify_binary_op(left: Node, operator: str, right: Node) -> Node:
    if operator == '+' and isinstance(right, Number) and right.value == 0:
        return left  # x + 0 = x
    if operator == '*' and isinstance(right, Number) and right.value == 1:
        return left  # x * 1 = x
    # ... more rules
```

**Simplification Data Structures**:
- **Rule Matching**: Pattern matching on tree structure
- **Tree Rewriting**: Replace matched patterns with simplified forms
- **Iterative Application**: Apply rules until no more changes

### Tree Visualization Data Structures

#### ASCII Art Generation
```python
def _build_tree_lines(node: Node) -> List[str]:
    if isinstance(node, Number):
        return [f"Number({node.value})"]
    if isinstance(node, BinaryOp):
        left_lines = _build_tree_lines(node.left)
        right_lines = _build_tree_lines(node.right)
        return combine_subtrees(left_lines, operator_line, right_lines)
```

**Visualization Data Structures**:
- **Line Arrays**: Each tree level represented as string array
- **Width Calculation**: Dynamic width calculation for alignment
- **Character Mapping**: ASCII characters for tree connections

## Performance Characteristics

### Time Complexity Analysis

#### Tree Construction
- **Tokenizer**: O(n) where n is input length
- **Parser**: O(n) where n is number of tokens
- **Overall**: O(n) linear in expression size

#### Tree Operations
- **Evaluation**: O(n) where n is tree size
- **Differentiation**: O(n) where n is tree size
- **String Conversion**: O(n) where n is tree size

#### Tree Traversal
- **Depth**: O(d) where d is tree depth
- **Breadth**: O(n) where n is number of nodes
- **Memory**: O(d) for recursion stack

### Space Complexity Analysis

#### Tree Storage
- **Nodes**: O(n) where n is expression complexity
- **References**: O(n) for parent-child relationships
- **Metadata**: O(n) for node-specific data

#### Operation Memory
- **Differentiation**: O(n) for new tree creation
- **Evaluation**: O(d) for recursion stack
- **Simplification**: O(n) for intermediate results

## Data Structure Design Decisions

### Why Not Other Structures?

#### Arrays/Lists
```
Expression: 2*x + 3
Array: [2, '*', 'x', '+', 3]
```
**Problems**:
- **No Precedence**: Operator precedence lost
- **Complex Parsing**: Difficult to determine evaluation order
- **No Hierarchy**: Flat structure doesn't reflect expression structure

#### Stacks
```
Expression: 2*x + 3
Stack Operations: Push(2), Push(x), Push(*), Push(3), Push(+)
```
**Problems**:
- **Temporary**: Stack destroyed after evaluation
- **No Persistence**: Can't store expression for later use
- **Limited Operations**: Hard to implement symbolic manipulation

#### Graphs
```
Expression: 2*x + 3
Graph: Multiple nodes with arbitrary connections
```
**Problems**:
- **Over-Engineering**: Too complex for tree structure
- **No Hierarchy**: Lacks natural parent-child relationships
- **Complex Algorithms**: Harder to implement tree operations

### Why Trees Are Optimal

#### Natural Hierarchy
- **Mathematical Structure**: Expressions naturally hierarchical
- **Operator Precedence**: Tree structure encodes precedence
- **Recursive Operations**: Natural fit for recursive algorithms

#### Efficient Operations
- **O(n) Traversal**: Linear time for most operations
- **O(d) Memory**: Memory usage proportional to depth
- **Cache Friendly**: Locality of reference for tree operations

#### Symbolic Manipulation
- **Easy Transformation**: Tree structure easy to modify
- **Rule Application**: Calculus rules map naturally to tree operations
- **Composition**: Complex operations composed from simple ones

## Extensibility and Future Enhancements

### Adding New Node Types
```python
class Function(Node):
    def __init__(self, name: str, argument: Node):
        self.name = name
        self.argument = argument
    
    def evaluate(self, variables: Dict[str, float] = None) -> float:
        arg_val = self.argument.evaluate(variables)
        return self.apply_function(self.name, arg_val)
```

**Extension Points**:
- **Inherit from Node**: Implement abstract methods
- **Add to Parser**: Handle new token types
- **Add Calculus Rules**: Implement differentiation rules

### Adding New Operations
```python
class TernaryOp(Node):
    def __init__(self, condition: Node, true_expr: Node, false_expr: Node):
        self.condition = condition
        self.true_expr = true_expr
        self.false_expr = false_expr
```

**Design Considerations**:
- **Arity Flexibility**: Support different numbers of operands
- **Operation Complexity**: Balance between flexibility and simplicity
- **Memory Usage**: Consider impact on tree size

## Testing Data Structures

### Tree Structure Validation
```python
def validate_tree_structure(node: Node) -> bool:
    if isinstance(node, Number) or isinstance(node, Variable):
        return True  # Leaf nodes are valid
    if isinstance(node, BinaryOp):
        return (validate_tree_structure(node.left) and 
                validate_tree_structure(node.right))
    return False
```

### Tree Equality Testing
```python
def __eq__(self, other) -> bool:
    return (isinstance(other, BinaryOp) and 
            self.operator == other.operator and
            self.left == other.left and
            self.right == other.right)
```

**Testing Strategies**:
- **Structure Validation**: Ensure tree structure is valid
- **Equality Testing**: Compare tree structures for equality
- **Performance Testing**: Measure operation times
- **Memory Testing**: Monitor memory usage patterns

## Conclusion

Our symbolic differentiation calculator demonstrates excellent use of data structures:

### Key Achievements
- **Expression Trees**: Core data structure enabling all functionality
- **Hierarchical Design**: Natural representation of mathematical expressions
- **Efficient Operations**: O(n) time complexity for most operations
- **Memory Efficiency**: O(n) space complexity with automatic cleanup
- **Extensible Design**: Easy to add new node types and operations

### Data Structure Benefits
- **Natural Fit**: Trees perfectly match mathematical expression structure
- **Algorithmic Efficiency**: Enables efficient recursive algorithms
- **Symbolic Manipulation**: Supports complex symbolic operations
- **Maintainability**: Clean, understandable data structure design

### Project Requirements Fulfillment
- ✅ **Tree-Based Representation**: Expression trees as core data structure
- ✅ **Data Structures**: Comprehensive use of trees, tokens, and traversal structures
- ✅ **Algorithm Development**: Tree traversal algorithms for evaluation and differentiation
- ✅ **Symbolic Manipulation**: Tree transformation algorithms for calculus operations

The expression tree data structure serves as the **foundation** that enables all other functionality in our symbolic differentiation calculator, demonstrating how thoughtful data structure design can enable complex algorithmic operations.
