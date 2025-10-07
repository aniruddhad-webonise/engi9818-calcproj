# Technical Documentation Index

## Overview

This directory contains detailed technical documentation for the core components of our **Command-Line Calculator with Symbolic Differentiation**. Each document explains how the code works and how it fulfills the project requirements.

## Documentation Files

### Core Components

1. **[tokenizer.md](tokenizer.md)** - Lexical Analysis Module
   - Character-by-character input processing
   - Token recognition and classification
   - Error detection and handling
   - Integration with parser

2. **[parser.md](parser.md)** - Syntax Analysis Module
   - Recursive descent parsing algorithm
   - Operator precedence implementation (PEMDAS)
   - Expression tree construction
   - Syntax error detection

3. **[nodes.md](nodes.md)** - Expression Tree Data Structure
   - Abstract Syntax Tree (AST) implementation
   - Node classes (Number, Variable, BinaryOp)
   - Evaluation algorithms
   - Differentiation algorithms with calculus rules

### Architecture

4. **[architecture-overview.md](architecture-overview.md)** - System Architecture
   - Overall system design and data flow
   - Component integration and responsibilities
   - Design patterns and algorithms used
   - Performance analysis and extensibility

5. **[data-structures.md](data-structures.md)** - Data Structures Deep Dive
   - Expression trees (AST) as core data structure
   - Tree construction and traversal algorithms
   - Memory management and performance analysis
   - Design decisions and extensibility patterns

6. **[algorithms.md](algorithms.md)** - Algorithm Development
   - Tree traversal algorithms (post-order, pre-order, in-order)
   - Simplification algorithms and algebraic rules
   - Parsing algorithms and operator precedence
   - Performance analysis and optimization strategies

## Project Requirements Mapping

Each component addresses specific requirements from the project specification:

> "Build a calculator that performs basic arithmetic and can also parse a mathematical expression and compute its symbolic derivative. The project requires a robust parser, a tree-based representation of the expression, and algorithms for symbolic manipulation. It will heavily involve data structures (expression trees) and algorithm development (traversal, simplification)."

### Requirements Coverage

- ✅ **Robust Parser**: Tokenizer + Parser modules
- ✅ **Tree-Based Representation**: Nodes module with AST
- ✅ **Algorithms for Symbolic Manipulation**: Differentiation rules in Nodes
- ✅ **Data Structures**: Expression trees with traversal capabilities
- ✅ **Algorithm Development**: Tree traversal, evaluation, differentiation

## Quick Reference

### Key Algorithms
- **Tokenization**: Character scanning with state machine
- **Parsing**: Recursive descent with operator precedence
- **Evaluation**: Post-order tree traversal
- **Differentiation**: Recursive calculus rule application

### Key Data Structures
- **Token**: Type-value pairs for lexical units
- **Expression Tree**: Hierarchical AST with node classes
- **Node Types**: Number (leaf), Variable (leaf), BinaryOp (internal)

### Key Design Patterns
- **Visitor Pattern**: Tree traversal for operations
- **Recursive Descent**: Grammar-driven parsing
- **Immutable Objects**: Safe symbolic manipulation
- **Polymorphism**: Uniform interface across node types

## Usage

Each document is self-contained and can be read independently, but they build upon each other:

1. Start with **architecture-overview.md** for the big picture
2. Read **tokenizer.md** to understand lexical analysis
3. Read **parser.md** to understand syntax analysis
4. Read **nodes.md** to understand symbolic manipulation

## Code Examples

Each document includes:
- Detailed code explanations
- Algorithm walkthroughs
- Performance analysis
- Error handling strategies
- Extensibility guidelines
- Test cases and validation

## Contributing

When modifying the core components:
1. Update the relevant documentation
2. Add new test cases
3. Update the architecture overview if needed
4. Ensure all requirements are still addressed
