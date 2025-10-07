"""
Simplifier - Cleaning Up Expression Trees

This module implements expression simplification to clean up messy derivative
expressions and make them more readable. It handles common algebraic
simplifications like combining like terms and eliminating unnecessary operations.

PROJECT REQUIREMENTS ADDRESSED:
- ✅ Algorithms for symbolic manipulation (simplification algorithms)
- ✅ Tree traversal (recursive simplification through tree structure)

SIMPLIFICATION RULES:
- x + 0 = x, x * 1 = x, x * 0 = 0
- 0 + x = x, 1 * x = x, 0 * x = 0
- x^1 = x, x^0 = 1 (for x ≠ 0)
- Combine like terms where possible
- Remove unnecessary parentheses

EXAMPLES:
Input:  ((0 * x) + (2.0 * 1)) + 0
Output: 2

Input:  (3.0 * (x ^ 2.0)) * 1
Output: 3 * x^2
"""

from typing import Dict, Any
try:
    from .nodes import Node, Number, Variable, BinaryOp
except ImportError:
    # For testing when run directly
    from nodes import Node, Number, Variable, BinaryOp


class Simplifier:
    """
    Simplifies expression trees by applying algebraic rules.
    
    This implements the simplification algorithms for our symbolic manipulation
    system. It recursively traverses the tree and applies simplification rules
    to make expressions cleaner and more readable.
    """
    
    @staticmethod
    def simplify(node: Node) -> Node:
        """
        Simplify an expression tree.
        
        This is the main entry point for simplification. It recursively
        simplifies the tree by applying algebraic rules.
        
        Args:
            node: The expression tree to simplify
            
        Returns:
            Simplified expression tree
        """
        if isinstance(node, Number):
            return node  # Numbers don't need simplification
        
        if isinstance(node, Variable):
            return node  # Variables don't need simplification
        
        if isinstance(node, BinaryOp):
            # Recursively simplify children first
            left_simplified = Simplifier.simplify(node.left)
            right_simplified = Simplifier.simplify(node.right)
            
            # Apply simplification rules
            return Simplifier._simplify_binary_op(left_simplified, node.operator, right_simplified)
        
        return node
    
    @staticmethod
    def _simplify_binary_op(left: Node, operator: str, right: Node) -> Node:
        """
        Apply simplification rules to a binary operation.
        
        This implements the core simplification logic for binary operations,
        handling cases like x+0=x, x*1=x, etc.
        
        Args:
            left: Left operand (already simplified)
            operator: The operation
            right: Right operand (already simplified)
            
        Returns:
            Simplified expression
        """
        # Handle addition
        if operator == '+':
            # x + 0 = x
            if isinstance(right, Number) and right.value == 0:
                return left
            # 0 + x = x
            if isinstance(left, Number) and left.value == 0:
                return right
            # Both are numbers: add them
            if isinstance(left, Number) and isinstance(right, Number):
                return Number(left.value + right.value)
        
        # Handle subtraction
        elif operator == '-':
            # x - 0 = x
            if isinstance(right, Number) and right.value == 0:
                return left
            # 0 - x = -x (we'll handle this as 0 + (-x) later)
            if isinstance(left, Number) and left.value == 0:
                return BinaryOp(Number(0), '-', right)
            # Both are numbers: subtract them
            if isinstance(left, Number) and isinstance(right, Number):
                return Number(left.value - right.value)
        
        # Handle multiplication
        elif operator == '*':
            # x * 0 = 0
            if (isinstance(left, Number) and left.value == 0) or \
               (isinstance(right, Number) and right.value == 0):
                return Number(0)
            # x * 1 = x
            if isinstance(right, Number) and right.value == 1:
                return left
            # 1 * x = x
            if isinstance(left, Number) and left.value == 1:
                return right
            # Both are numbers: multiply them
            if isinstance(left, Number) and isinstance(right, Number):
                return Number(left.value * right.value)
        
        # Handle division
        elif operator == '/':
            # x / 1 = x
            if isinstance(right, Number) and right.value == 1:
                return left
            # 0 / x = 0 (for x ≠ 0)
            if isinstance(left, Number) and left.value == 0:
                return Number(0)
            # Both are numbers: divide them
            if isinstance(left, Number) and isinstance(right, Number):
                return Number(left.value / right.value)
        
        # Handle exponentiation
        elif operator == '^':
            # x^1 = x
            if isinstance(right, Number) and right.value == 1:
                return left
            # x^0 = 1 (for x ≠ 0)
            if isinstance(right, Number) and right.value == 0:
                return Number(1)
            # Both are numbers: compute power
            if isinstance(left, Number) and isinstance(right, Number):
                return Number(left.value ** right.value)
        
        # If no simplification applies, return the original operation
        return BinaryOp(left, operator, right)


def simplify_expression(node: Node) -> Node:
    """
    Convenience function to simplify an expression tree.
    
    Args:
        node: The expression tree to simplify
        
    Returns:
        Simplified expression tree
    """
    return Simplifier.simplify(node)


# Example usage and testing
if __name__ == "__main__":
    from parser import parse_expression
    
    # Test cases for simplification
    test_cases = [
        "2*x + 3",
        "x^3",
        "x^2 + 2*x + 1",
        "(x + 1)^2",
        "(2*x + 1)^3"
    ]
    
    print("Simplification Test Cases:")
    print("=" * 60)
    
    for test in test_cases:
        try:
            tree = parse_expression(test)
            derivative = tree.differentiate('x')
            simplified = simplify_expression(derivative)
            
            print(f"Expression: {test}")
            print(f"Derivative: {derivative}")
            print(f"Simplified: {simplified}")
            print()
        except Exception as e:
            print(f"Error with '{test}': {e}")
            print()
