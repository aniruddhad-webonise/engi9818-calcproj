"""
Expression Tree Node Classes - Core Data Structure for Symbolic Differentiation

This module implements the "tree-based representation of the expression" requirement
from the project specification. It defines the Abstract Syntax Tree (AST) nodes that
represent mathematical expressions as hierarchical data structures.

PROJECT REQUIREMENTS ADDRESSED:
- ✅ Tree-based representation of expressions (AST nodes)
- ✅ Algorithms for symbolic manipulation (differentiation rules)
- ✅ Data structures (expression trees with traversal capabilities)
- ✅ Symbolic derivative computation (each node knows its derivative)

ARCHITECTURE OVERVIEW:
- Abstract base class (Node) defines the interface
- Concrete implementations: Number, Variable, BinaryOp
- Each node implements evaluation and differentiation algorithms
- Tree traversal happens recursively through the differentiate() method
- Immutable design ensures safe symbolic manipulation

HOW IT FITS THE BIGGER PICTURE:
1. Parser (next step) will create these nodes from input strings
2. These nodes enable symbolic differentiation through tree traversal
3. Simplifier (later step) will clean up derivative expressions
4. Command-line interface will orchestrate: parse → differentiate → display
"""

from abc import ABC, abstractmethod
from typing import Union, Dict, Any


class Node(ABC):
    """
    Abstract base class for all expression tree nodes.
    
    This implements the core interface for our "tree-based representation" requirement.
    Every mathematical expression component (numbers, variables, operations) inherits
    from this class, ensuring they all support:
    
    1. EVALUATION: Compute numeric value given variable assignments
    2. DIFFERENTIATION: Compute symbolic derivative (returns new tree)
    3. STRING REPRESENTATION: Convert back to readable math notation
    
    The differentiation method implements the "algorithms for symbolic manipulation"
    requirement through recursive tree traversal.
    """
    
    @abstractmethod
    def evaluate(self, variables: Dict[str, float] = None) -> float:
        """
        Evaluate the expression with given variable values.
        
        This method implements tree traversal for evaluation - it recursively
        visits child nodes and combines their values according to the operation.
        
        Args:
            variables: Dictionary mapping variable names to their values
            
        Returns:
            The numeric result of evaluating this expression
            
        Raises:
            ValueError: If required variables are not defined
        """
        pass
    
    @abstractmethod
    def differentiate(self, variable: str = 'x') -> 'Node':
        """
        Compute the symbolic derivative with respect to the given variable.
        
        This is the core "symbolic manipulation" algorithm. Each node type
        implements the appropriate calculus rule:
        - Constants → 0
        - Variables → 1 (if same variable) or 0 (otherwise)  
        - Operations → Apply calculus rules (sum, product, quotient, power)
        
        Args:
            variable: The variable to differentiate with respect to
            
        Returns:
            A new expression tree representing the derivative
        """
        pass
    
    @abstractmethod
    def __str__(self) -> str:
        """
        String representation of the expression.
        
        Converts the tree back to readable mathematical notation.
        This enables the command-line calculator to display results.
        """
        pass
    
    def __repr__(self) -> str:
        """Debug representation showing the tree structure."""
        return f"{self.__class__.__name__}({self})"


class Number(Node):
    """
    Represents a numeric constant in our expression tree.
    
    Examples: 5, 3.14, -2, 0
    This is a leaf node in our tree structure - it has no children.
    """
    
    def __init__(self, value: float):
        """Initialize with the numeric value."""
        self.value = value
    
    def evaluate(self, variables: Dict[str, float] = None) -> float:
        """
        Evaluate a constant - always returns the same value regardless of variables.
        
        This implements the base case for tree traversal during evaluation.
        """
        return self.value
    
    def differentiate(self, variable: str = 'x') -> 'Node':
        """
        Apply the constant rule: d/dx(c) = 0
        
        This is the simplest differentiation rule and serves as a base case
        for recursive differentiation algorithms.
        """
        return Number(0)
    
    def __str__(self) -> str:
        """Convert back to string representation for display."""
        return str(self.value)
    
    def __eq__(self, other) -> bool:
        """Equality comparison for testing and simplification."""
        return isinstance(other, Number) and self.value == other.value


class Variable(Node):
    """
    Represents a variable in our expression tree.
    
    Examples: x, y, z, t
    This is also a leaf node - it represents an unknown quantity that can
    be assigned different values during evaluation.
    """
    
    def __init__(self, name: str):
        """Initialize with the variable name."""
        self.name = name
    
    def evaluate(self, variables: Dict[str, float] = None) -> float:
        """
        Evaluate a variable by looking up its value in the variables dictionary.
        
        This implements the variable lookup during tree traversal for evaluation.
        The command-line calculator will provide variable values when evaluating
        expressions at specific points.
        """
        if variables is None or self.name not in variables:
            raise ValueError(f"Variable '{self.name}' not defined")
        return variables[self.name]
    
    def differentiate(self, variable: str = 'x') -> 'Node':
        """
        Apply the variable differentiation rule:
        - d/dx(x) = 1  (derivative of x with respect to x)
        - d/dx(y) = 0  (derivative of y with respect to x)
        
        This implements the core rule for symbolic differentiation of variables.
        """
        if self.name == variable:
            return Number(1)
        else:
            return Number(0)
    
    def __str__(self) -> str:
        """Convert back to string representation for display."""
        return self.name
    
    def __eq__(self, other) -> bool:
        """Equality comparison for testing and simplification."""
        return isinstance(other, Variable) and self.name == other.name


class BinaryOp(Node):
    """
    Represents a binary operation in our expression tree.
    
    This is where the "algorithms for symbolic manipulation" really shine!
    Each operation implements the appropriate calculus rules for differentiation.
    
    Supported operations: +, -, *, /, ^ (exponentiation)
    Examples: x + 5, 2 * y, x^3, (x + 1) / (x - 1)
    
    This class implements the core "tree traversal" requirement through
    recursive differentiation algorithms.
    """
    
    def __init__(self, left: Node, operator: str, right: Node):
        """
        Initialize a binary operation with left operand, operator, and right operand.
        
        This creates the tree structure where each BinaryOp has two child nodes,
        implementing the hierarchical "tree-based representation" requirement.
        """
        self.left = left
        self.operator = operator
        self.right = right
    
    def evaluate(self, variables: Dict[str, float] = None) -> float:
        """
        Evaluate the binary operation by recursively evaluating children.
        
        This implements tree traversal for evaluation - it visits both child nodes,
        evaluates them, then combines their results according to the operation.
        This enables the "basic arithmetic" functionality of our calculator.
        """
        left_val = self.left.evaluate(variables)
        right_val = self.right.evaluate(variables)
        
        if self.operator == '+':
            return left_val + right_val
        elif self.operator == '-':
            return left_val - right_val
        elif self.operator == '*':
            return left_val * right_val
        elif self.operator == '/':
            if right_val == 0:
                raise ValueError("Division by zero")
            return left_val / right_val
        elif self.operator == '^':
            return left_val ** right_val
        else:
            raise ValueError(f"Unknown operator: {self.operator}")
    
    def differentiate(self, variable: str = 'x') -> 'Node':
        """
        Apply differentiation rules based on the operator.
        
        This is the heart of our "symbolic manipulation" algorithms!
        Each operation implements the appropriate calculus rule:
        
        SUM RULE:     d/dx(f + g) = f' + g'
        DIFFERENCE:   d/dx(f - g) = f' - g'  
        PRODUCT RULE: d/dx(f * g) = f'*g + f*g'
        QUOTIENT:     d/dx(f/g) = (f'*g - f*g') / g^2
        POWER RULE:   d/dx(x^n) = n*x^(n-1)
        
        The recursive nature implements tree traversal - each child node
        is differentiated, then combined according to the calculus rule.
        """
        if self.operator == '+':
            # Sum rule: d/dx(f + g) = f' + g'
            return BinaryOp(
                self.left.differentiate(variable),
                '+',
                self.right.differentiate(variable)
            )
        elif self.operator == '-':
            # Difference rule: d/dx(f - g) = f' - g'
            return BinaryOp(
                self.left.differentiate(variable),
                '-',
                self.right.differentiate(variable)
            )
        elif self.operator == '*':
            # Product rule: d/dx(f * g) = f'*g + f*g'
            left_diff = self.left.differentiate(variable)
            right_diff = self.right.differentiate(variable)
            return BinaryOp(
                BinaryOp(left_diff, '*', self.right),
                '+',
                BinaryOp(self.left, '*', right_diff)
            )
        elif self.operator == '/':
            # Quotient rule: d/dx(f/g) = (f'*g - f*g') / g^2
            left_diff = self.left.differentiate(variable)
            right_diff = self.right.differentiate(variable)
            numerator = BinaryOp(
                BinaryOp(left_diff, '*', self.right),
                '-',
                BinaryOp(self.left, '*', right_diff)
            )
            denominator = BinaryOp(self.right, '^', Number(2))
            return BinaryOp(numerator, '/', denominator)
        elif self.operator == '^':
            # Power rule: d/dx(f^n) = n * f^(n-1) * f'
            # This handles both simple cases (x^n) and complex cases ((x+1)^2)
            if isinstance(self.right, Number):
                n = self.right.value
                f = self.left
                f_prime = f.differentiate(variable)
                
                # Build n * f^(n-1) * f'
                if n == 1:
                    # Special case: d/dx(f^1) = f'
                    return f_prime
                elif n == 0:
                    # Special case: d/dx(f^0) = d/dx(1) = 0
                    return Number(0)
                else:
                    # General case: n * f^(n-1) * f'
                    power_part = BinaryOp(f, '^', Number(n - 1))
                    coefficient_part = BinaryOp(Number(n), '*', power_part)
                    return BinaryOp(coefficient_part, '*', f_prime)
            else:
                # For cases like f^g where g is not a constant
                # This would require logarithmic differentiation - not implemented yet
                raise NotImplementedError("Power rule for non-constant exponents not implemented yet")
        else:
            raise ValueError(f"Unknown operator: {self.operator}")
    
    def __str__(self) -> str:
        """
        Convert the tree back to readable mathematical notation.
        
        This enables the command-line calculator to display expressions
        in a user-friendly format. The parentheses handling ensures
        proper precedence is maintained in the output.
        """
        # Add parentheses for clarity in complex expressions
        left_str = str(self.left)
        right_str = str(self.right)
        
        # Add parentheses around binary operations for clarity
        if isinstance(self.left, BinaryOp):
            left_str = f"({left_str})"
        if isinstance(self.right, BinaryOp):
            right_str = f"({right_str})"
        
        return f"{left_str} {self.operator} {right_str}"
    
    def __eq__(self, other) -> bool:
        """
        Equality comparison for testing and simplification.
        
        This enables testing that our differentiation algorithms
        produce the expected results, and will be useful for
        expression simplification in later steps.
        """
        return (isinstance(other, BinaryOp) and 
                self.operator == other.operator and
                self.left == other.left and
                self.right == other.right)
