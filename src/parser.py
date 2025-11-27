"""
Parser - Converting Tokens into Expression Trees

This module implements the second step of our "robust parser" requirement.
It converts the token stream from the tokenizer into expression trees using
our node classes, handling operator precedence and parentheses correctly.

PROJECT REQUIREMENTS ADDRESSED:
- Robust parser (second component: parsing)
- Parse mathematical expressions (tokens → expression trees)
- Tree-based representation (creates AST using our node classes)
- Algorithms for symbolic manipulation (enables differentiation)

PARSING STRATEGY:
- Recursive descent parser with operator precedence
- Handles PEMDAS: Parentheses, Exponents, Multiplication/Division, Addition/Subtraction
- Left-to-right associativity for most operators
- Right-to-left associativity for exponentiation

EXAMPLES:
Tokens: [NUMBER(2), OPERATOR(*), VARIABLE(x), OPERATOR(+), NUMBER(3)]
Tree:   BinaryOp(+, BinaryOp(*, Number(2), Variable(x)), Number(3))

Tokens: [LPAREN, VARIABLE(x), OPERATOR(+), NUMBER(1), RPAREN, OPERATOR(^), NUMBER(2)]
Tree:   BinaryOp(^, BinaryOp(+, Variable(x), Number(1)), Number(2))
"""

from typing import List, Optional
try:
    from .tokenizer import Token, tokenize
    from .nodes import Node, Number, Variable, BinaryOp
except ImportError:
    # For testing when run directly
    from tokenizer import Token, tokenize
    from nodes import Node, Number, Variable, BinaryOp


class Parser:
    """
    Converts token streams into expression trees.
    
    This implements the parsing phase of our robust parser using recursive
    descent parsing with proper operator precedence handling. It creates
    expression trees that can be evaluated and differentiated.
    """
    
    def __init__(self, tokens: List[Token]):
        """
        Initialize parser with a list of tokens.
        
        Args:
            tokens: List of tokens from the tokenizer
        """
        self.tokens = tokens
        self.current_pos = 0
    
    def parse(self) -> Node:
        """
        Parse the token stream into an expression tree.
        
        This is the main entry point for parsing. It starts with the lowest
        precedence operations (addition/subtraction) and works its way up
        to higher precedence operations.
        
        Returns:
            Root node of the expression tree
            
        Raises:
            ValueError: If the expression is malformed
        """
        if not self.tokens:
            raise ValueError("No tokens to parse")
        
        # Start parsing from the lowest precedence level
        result = self._parse_addition()
        
        # Ensure we consumed all tokens except EOF
        if not self._is_at_end():
            raise ValueError(f"Unexpected token: {self._peek()}")
        
        return result
    
    def _parse_addition(self) -> Node:
        """
        Parse addition and subtraction (lowest precedence).
        
        This handles the '+' and '-' operators with left-to-right associativity.
        It calls _parse_multiplication() for higher precedence operations.
        
        Grammar: addition → multiplication (('+' | '-') multiplication)*
        """
        left = self._parse_multiplication()
        
        while self._match('OPERATOR', '+') or self._match('OPERATOR', '-'):
            operator = self._previous().value
            right = self._parse_multiplication()
            left = BinaryOp(left, operator, right)
        
        return left
    
    def _parse_multiplication(self) -> Node:
        """
        Parse multiplication and division (medium precedence).
        
        This handles the '*' and '/' operators with left-to-right associativity.
        It calls _parse_exponentiation() for higher precedence operations.
        
        Grammar: multiplication → exponentiation (('*' | '/') exponentiation)*
        """
        left = self._parse_exponentiation()
        
        while self._match('OPERATOR', '*') or self._match('OPERATOR', '/'):
            operator = self._previous().value
            right = self._parse_exponentiation()
            left = BinaryOp(left, operator, right)
        
        return left
    
    def _parse_exponentiation(self) -> Node:
        """
        Parse exponentiation (highest precedence, right-associative).
        
        This handles the '^' operator with right-to-left associativity.
        It calls _parse_primary() for the base cases.
        
        Grammar: exponentiation → primary ('^' exponentiation)?
        """
        left = self._parse_primary()
        
        if self._match('OPERATOR', '^'):
            right = self._parse_exponentiation()  # Right-associative
            left = BinaryOp(left, '^', right)
        
        return left
    
    def _parse_primary(self) -> Node:
        """
        Parse primary expressions (numbers, variables, parentheses).
        
        This handles the base cases of our grammar:
        - Numbers: 5, 3.14, -2
        - Variables: x, y, z
        - Parenthesized expressions: (x + 1)
        
        Grammar: primary → NUMBER | VARIABLE | '(' addition ')'
        """
        if self._match('NUMBER'):
            return Number(self._previous().value)
        
        if self._match('VARIABLE'):
            return Variable(self._previous().value)
        
        if self._match('LPAREN'):
            expr = self._parse_addition()  # Parse the expression inside parentheses
            if not self._match('RPAREN'):
                raise ValueError("Expected ')' after expression")
            return expr
        
        raise ValueError(f"Expected number, variable, or '(', got {self._peek()}")
    
    def _match(self, token_type: str, value: Optional[str] = None) -> bool:
        """
        Check if current token matches the expected type and value.
        
        If it matches, advance to the next token. This implements the
        lookahead mechanism for our recursive descent parser.
        
        Args:
            token_type: Expected token type
            value: Expected token value (optional)
            
        Returns:
            True if token matches and advances, False otherwise
        """
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
    
    def _peek(self) -> Token:
        """
        Look at the current token without advancing.
        
        Returns:
            Current token
            
        Raises:
            ValueError: If at end of input
        """
        if self._is_at_end():
            raise ValueError("Unexpected end of input")
        return self.tokens[self.current_pos]
    
    def _previous(self) -> Token:
        """
        Get the previous token.
        
        Returns:
            Previous token
            
        Raises:
            ValueError: If no previous token exists
        """
        if self.current_pos == 0:
            raise ValueError("No previous token")
        return self.tokens[self.current_pos - 1]
    
    def _is_at_end(self) -> bool:
        """
        Check if we've reached the end of the token stream.
        
        Returns:
            True if at EOF token, False otherwise
        """
        return (self.current_pos >= len(self.tokens) or 
                self.tokens[self.current_pos].type == 'EOF')


def parse_expression(text: str) -> Node:
    """
    Convenience function to parse a mathematical expression string.
    
    This combines tokenization and parsing into a single function,
    providing a simple interface for converting strings to expression trees.
    
    Args:
        text: Mathematical expression string
        
    Returns:
        Root node of the expression tree
        
    Raises:
        ValueError: If the expression is malformed
        
    Example:
        tree = parse_expression("2*x + 3")
        # Returns: BinaryOp(+, BinaryOp(*, Number(2), Variable(x)), Number(3))
    """
    tokens = tokenize(text)
    parser = Parser(tokens)
    return parser.parse()


# Example usage and testing
if __name__ == "__main__":
    # Test cases for parsing
    test_cases = [
        "2*x + 3",
        "(x + 1)^2",
        "x^3 - 2*x",
        "5.5 / 2.2",
        "x + y - z",
        "2^3^2",  # Right-associative: 2^(3^2) = 2^9 = 512
        "2*3 + 4*5",  # Left-associative: (2*3) + (4*5) = 6 + 20 = 26
    ]
    
    print("Parser Test Cases:")
    print("=" * 60)
    
    for test in test_cases:
        try:
            tree = parse_expression(test)
            print(f"Input: '{test}'")
            print(f"Tree:  {tree}")
            
            # Test evaluation if possible
            try:
                result = tree.evaluate({'x': 2, 'y': 3, 'z': 1})
                print(f"Eval:  {result}")
            except ValueError:
                print("Eval:  (requires variable values)")
            
            print()
        except ValueError as e:
            print(f"Error parsing '{test}': {e}")
            print()
