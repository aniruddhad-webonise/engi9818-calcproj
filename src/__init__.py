"""
Symbolic Differentiation Calculator - Core Module

This module provides the core functionality for a command-line calculator that performs 
basic arithmetic and computes symbolic derivatives of mathematical expressions.

The module implements a complete pipeline for symbolic differentiation:
1. Tokenization: Convert input strings into tokens
2. Parsing: Build expression trees from tokens using recursive descent parsing
3. Tree Representation: Abstract Syntax Tree (AST) with node classes
4. Differentiation: Symbolic derivative computation using calculus rules
5. Simplification: Clean up derivative expressions for readability
6. Visualization: Display expression trees as text diagrams

Usage:
    from src import parse_expression, simplify_expression, visualize_tree
    tree = parse_expression("2*x + 3")
    derivative = tree.differentiate('x')
    simplified = simplify_expression(derivative)
    print(visualize_tree(tree))

Core Components:
- nodes.py: Expression tree node classes (Number, Variable, BinaryOp)
- tokenizer.py: Tokenization logic for parsing mathematical expressions
- parser.py: Recursive descent parser with operator precedence
- simplifier.py: Expression simplification algorithms
- tree_visualizer.py: Tree visualization utilities

Features:
- Robust parser with proper operator precedence (PEMDAS)
- Complete symbolic differentiation rules (sum, product, quotient, power)
- Expression simplification (x+0=x, x*1=x, etc.)
- Tree visualization with ASCII art
- Support for variables, constants, and all basic operations
- Error handling for malformed expressions
"""

__version__ = "0.1.0"

# Import key functions for easy access
try:
    from .parser import parse_expression
    from .simplifier import simplify_expression
    from .tree_visualizer import visualize_tree
    from .tokenizer import tokenize
    from .nodes import Number, Variable, BinaryOp
except ImportError:
    # Handle cases where relative imports fail
    pass

# Module metadata
MODULE_INFO = {
    "name": "Symbolic Differentiation Calculator Core",
    "version": __version__,
    "description": "Core module for symbolic differentiation calculator",
    "components": {
        "nodes": "Expression tree node classes (Number, Variable, BinaryOp)",
        "tokenizer": "Tokenization logic for parsing mathematical expressions", 
        "parser": "Recursive descent parser with operator precedence",
        "simplifier": "Expression simplification algorithms",
        "tree_visualizer": "Tree visualization utilities"
    },
    "features": [
        "Robust parser with PEMDAS operator precedence",
        "Complete symbolic differentiation rules",
        "Expression simplification algorithms", 
        "Tree visualization with ASCII art",
        "Support for variables and basic operations",
        "Comprehensive error handling"
    ],
    "supported_operations": ["+", "-", "*", "/", "^"],
    "differentiation_rules": [
        "Constant rule: d/dx(c) = 0",
        "Variable rule: d/dx(x) = 1", 
        "Sum rule: d/dx(f + g) = f' + g'",
        "Product rule: d/dx(f * g) = f'*g + f*g'",
        "Quotient rule: d/dx(f/g) = (f'*g - f*g') / g^2",
        "Power rule: d/dx(f^n) = n * f^(n-1) * f'"
    ]
}


def get_module_info():
    """Return comprehensive information about this module."""
    return MODULE_INFO


def get_component_count():
    """Return the number of core components in this module."""
    return len(MODULE_INFO["components"])


def get_feature_count():
    """Return the number of implemented features."""
    return len(MODULE_INFO["features"])


def get_supported_operations():
    """Return list of supported mathematical operations."""
    return MODULE_INFO["supported_operations"]


def get_differentiation_rules():
    """Return list of implemented differentiation rules."""
    return MODULE_INFO["differentiation_rules"]


# Export key functions and data for easy access
__all__ = [
    # Core functions
    "parse_expression",
    "simplify_expression", 
    "visualize_tree",
    "tokenize",
    
    # Node classes
    "Number",
    "Variable", 
    "BinaryOp",
    
    # Module information
    "get_module_info",
    "get_component_count",
    "get_feature_count", 
    "get_supported_operations",
    "get_differentiation_rules",
    "MODULE_INFO",
    
    # Version
    "__version__"
]
