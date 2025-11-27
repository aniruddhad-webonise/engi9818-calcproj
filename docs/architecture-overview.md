# Core Components Overview - Technical Architecture

## Project Requirements Summary

Our **Command-Line Calculator with Symbolic Differentiation** addresses these core requirements:

> "Build a calculator that performs basic arithmetic and can also parse a mathematical expression and compute its symbolic derivative. The project requires a robust parser, a tree-based representation of the expression, and algorithms for symbolic manipulation. It will heavily involve data structures (expression trees) and algorithm development (traversal, simplification)."

## Architecture Overview

The system implements a **three-phase pipeline** that transforms mathematical expressions from strings to symbolic derivatives:

```
Input String → Tokenizer → Tokens → Parser → Expression Tree → Differentiator → Simplified Tree → Output
```

## Component Responsibilities

### 1. Tokenizer (`tokenizer.py`)
**Phase**: Lexical Analysis (String → Tokens)

**Responsibilities**:
- Break input strings into meaningful tokens
- Handle whitespace and invalid characters
- Parse numbers, variables, operators, and parentheses
- Provide structured input for parser

**Key Algorithms**:
- Character-by-character scanning
- Number parsing with decimal support
- Single-letter variable recognition
- Operator and parenthesis detection

**Project Requirements Addressed**:
-  **Robust Parser** (first component: lexical analysis)
-  **Parse Mathematical Expressions** (tokenization enables parsing)

### 2. Parser (`parser.py`)
**Phase**: Syntax Analysis (Tokens → Expression Tree)

**Responsibilities**:
- Convert token streams into expression trees
- Implement operator precedence (PEMDAS)
- Handle associativity (left-to-right, right-to-left)
- Detect syntax errors and malformed expressions

**Key Algorithms**:
- Recursive descent parsing
- Operator precedence handling
- Tree construction with proper hierarchy
- Lookahead token matching

**Project Requirements Addressed**:
-  **Robust Parser** (second component: syntax analysis)
-  **Parse Mathematical Expressions** (tokens → expression trees)
-  **Tree-Based Representation** (creates AST using node classes)

### 3. Nodes (`nodes.py`)
**Phase**: Symbolic Manipulation (Tree Operations)

**Responsibilities**:
- Define expression tree data structure
- Implement evaluation algorithms
- Implement differentiation algorithms
- Provide string representation

**Key Algorithms**:
- Tree traversal for evaluation
- Calculus rule implementation
- Recursive differentiation
- Immutable tree construction

**Project Requirements Addressed**:
-  **Tree-Based Representation** (AST with node classes)
-  **Algorithms for Symbolic Manipulation** (differentiation rules)
-  **Data Structures** (expression trees with traversal capabilities)
-  **Symbolic Derivative Computation** (each node knows its derivative)

## Data Flow Analysis

### Input Processing Pipeline

#### Phase 1: Tokenization
```
Input: "2*x + 3"
↓
Tokens: [NUMBER(2.0), OPERATOR(*), VARIABLE(x), OPERATOR(+), NUMBER(3.0), EOF]
```

**Algorithm**: Character-by-character scanning with state machine
**Complexity**: O(n) where n is input length
**Error Handling**: Invalid character detection

#### Phase 2: Parsing
```
Tokens: [NUMBER(2.0), OPERATOR(*), VARIABLE(x), OPERATOR(+), NUMBER(3.0), EOF]
↓
Tree: BinaryOp(+, BinaryOp(*, Number(2), Variable(x)), Number(3))
```

**Algorithm**: Recursive descent with operator precedence
**Complexity**: O(n) where n is number of tokens
**Error Handling**: Syntax error detection

#### Phase 3: Symbolic Manipulation
```
Tree: BinaryOp(+, BinaryOp(*, Number(2), Variable(x)), Number(3))
↓ Differentiate
Derivative: BinaryOp(+, BinaryOp(+, BinaryOp(Number(0), '*', Variable(x)), BinaryOp(Number(2), '*', Number(1))), Number(0))
↓ Simplify
Simplified: Number(2.0)
```

**Algorithm**: Recursive tree traversal with calculus rules
**Complexity**: O(n) where n is tree size
**Error Handling**: Division by zero, undefined variables

## Algorithm Complexity Analysis

### Time Complexity
- **Tokenizer**: O(n) - single pass through input
- **Parser**: O(n) - single pass through tokens
- **Differentiation**: O(n) - single traversal of tree
- **Overall**: O(n) linear in expression size

### Space Complexity
- **Tokenizer**: O(n) - token storage
- **Parser**: O(n) - tree storage
- **Differentiation**: O(n) - new tree creation
- **Overall**: O(n) linear in expression complexity

## Design Patterns Used

### 1. Visitor Pattern
**Implementation**: Tree traversal for evaluation and differentiation
**Benefits**: Clean separation of operations from data structure
**Usage**: Each node type handles its own operations

### 2. Recursive Descent Parsing
**Implementation**: Parser uses recursive methods for each precedence level
**Benefits**: Clean, maintainable parsing logic
**Usage**: Grammar rules map directly to method calls

### 3. Immutable Objects
**Implementation**: Expression trees are never modified after creation
**Benefits**: Safe for symbolic manipulation, thread-safe
**Usage**: Differentiation creates new trees

### 4. Polymorphism
**Implementation**: All nodes implement same interface
**Benefits**: Uniform operations across different node types
**Usage**: Evaluation and differentiation work on any node type

## Error Handling Strategy

### Lexical Errors (Tokenizer)
- **Invalid Characters**: Non-mathematical characters
- **Malformed Numbers**: Multiple decimal points, empty numbers
- **Detection**: Character-by-character validation

### Syntax Errors (Parser)
- **Unexpected Tokens**: Tokens that don't fit grammar
- **Missing Parentheses**: Unmatched opening/closing parentheses
- **Detection**: Grammar rule validation

### Runtime Errors (Nodes)
- **Undefined Variables**: Missing variable values
- **Division by Zero**: Zero denominators
- **Detection**: Runtime validation during evaluation

## Extensibility Design

### Adding New Operators
1. **Tokenizer**: Add operator to character classification
2. **Parser**: Add precedence level and parsing method
3. **Nodes**: Add operator handling in BinaryOp
4. **Testing**: Add test cases for new operator

### Adding New Node Types
1. **Inherit from Node**: Implement abstract methods
2. **Add Evaluation Logic**: Define numeric computation
3. **Add Differentiation Logic**: Define calculus rules
4. **Update Parser**: Add token type handling

### Adding New Functions
1. **Create Function Node**: New node type for functions
2. **Implement Calculus Rules**: Chain rule, etc.
3. **Update Tokenizer**: Add function name recognition
4. **Update Parser**: Add function call parsing

## Testing Strategy

### Unit Testing
- **Tokenizer**: Test token recognition and error handling
- **Parser**: Test precedence, associativity, and syntax errors
- **Nodes**: Test evaluation, differentiation, and string representation

### Integration Testing
- **End-to-End**: String → tokens → tree → derivative → simplified
- **Error Propagation**: Errors handled correctly through pipeline
- **Performance**: Large expressions processed efficiently

### Validation Testing
- **Mathematical Correctness**: Derivatives computed correctly
- **Edge Cases**: Empty expressions, single tokens, deep nesting
- **Error Cases**: Invalid input handled gracefully

## Performance Optimizations

### Memory Management
- **Immutable Trees**: No copying needed for safe manipulation
- **Token Reuse**: Tokens processed once, then discarded
- **Tree Sharing**: Common subexpressions could be shared (future)

### Algorithm Efficiency
- **Single Pass**: Each phase processes input once
- **Early Termination**: Errors detected as early as possible
- **Lazy Evaluation**: Trees built only when needed

## Future Enhancements

### Short Term
- **More Operators**: Modulo, factorial
- **Better Simplification**: More algebraic rules
- **Error Recovery**: Continue parsing after errors

### Medium Term
- **Trigonometric Functions**: sin, cos, tan
- **Logarithmic Functions**: ln, log
- **Multi-letter Variables**: Longer variable names

### Long Term
- **Integration**: Antiderivative computation
- **Graphical Interface**: Visual expression editing
- **Performance**: Parallel processing for large expressions

## Conclusion

The three core components (Tokenizer, Parser, Nodes) work together to fulfill all project requirements:

- **Robust Parser**: Two-phase lexical and syntax analysis
- **Tree-Based Representation**: Hierarchical AST with proper node classes
- **Algorithms for Symbolic Manipulation**: Complete differentiation rule implementation
- **Data Structures**: Expression trees with traversal capabilities
- **Symbolic Derivative Computation**: Each node knows how to differentiate itself

The architecture provides a solid foundation for a symbolic differentiation calculator that can be extended with additional mathematical functions and features while maintaining clean, maintainable code.
