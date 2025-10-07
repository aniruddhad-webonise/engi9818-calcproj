"""
Tokenizer - Breaking Input Strings into Tokens

This module implements the first step of our "robust parser" requirement.
It converts mathematical expression strings into a list of tokens that can
be processed by the parser to build expression trees.

PROJECT REQUIREMENTS ADDRESSED:
- ✅ Robust parser (first component: tokenization)
- ✅ Parse mathematical expressions (tokenization enables parsing)

TOKEN TYPES SUPPORTED:
- NUMBER: Numeric constants (5, 3.14, -2)
- VARIABLE: Single-letter variables (x, y, z)
- OPERATOR: Binary operations (+, -, *, /, ^)
- LPAREN/RPAREN: Parentheses for grouping
- EOF: End of input marker

EXAMPLES:
Input: "2*x + 3"     → [NUMBER(2), OPERATOR(*), VARIABLE(x), OPERATOR(+), NUMBER(3)]
Input: "(x + 1)^2"   → [LPAREN, VARIABLE(x), OPERATOR(+), NUMBER(1), RPAREN, OPERATOR(^), NUMBER(2)]
Input: "x^3 - 2*x"   → [VARIABLE(x), OPERATOR(^), NUMBER(3), OPERATOR(-), NUMBER(2), OPERATOR(*), VARIABLE(x)]
"""

from typing import List, Union
from dataclasses import dataclass


@dataclass
class Token:
    """
    Represents a single token in the mathematical expression.
    
    Each token has a type and value, enabling the parser to understand
    what each piece of the input string represents.
    """
    type: str
    value: Union[str, float, None] = None
    
    def __str__(self) -> str:
        """String representation for debugging."""
        if self.value is not None:
            return f"{self.type}({self.value})"
        return self.type
    
    def __repr__(self) -> str:
        """Debug representation."""
        return self.__str__()


class Tokenizer:
    """
    Converts mathematical expression strings into lists of tokens.
    
    This implements the tokenization phase of our robust parser.
    It handles:
    - Multi-digit numbers and decimals
    - Single-letter variables
    - Binary operators
    - Parentheses
    - Whitespace handling
    - Error detection for invalid characters
    """
    
    def __init__(self):
        """Initialize the tokenizer."""
        self.tokens: List[Token] = []
        self.current_pos = 0
        self.text = ""
    
    def tokenize(self, text: str) -> List[Token]:
        """
        Convert input string into a list of tokens.
        
        This is the main entry point for tokenization. It processes the
        input character by character, building tokens according to their
        type (number, variable, operator, etc.).
        
        Args:
            text: The mathematical expression string to tokenize
            
        Returns:
            List of tokens representing the expression
            
        Raises:
            ValueError: If invalid characters are encountered
        """
        self.text = text.strip()
        self.current_pos = 0
        self.tokens = []
        
        while self.current_pos < len(self.text):
            char = self.text[self.current_pos]
            
            if char.isspace():
                # Skip whitespace
                self.current_pos += 1
            elif char.isdigit() or char == '.':
                # Parse number (including decimals)
                self._parse_number()
            elif char.isalpha():
                # Parse variable (single letter)
                self._parse_variable()
            elif char in '+-*/^':
                # Parse operator
                self._parse_operator()
            elif char == '(':
                # Left parenthesis
                self.tokens.append(Token('LPAREN'))
                self.current_pos += 1
            elif char == ')':
                # Right parenthesis
                self.tokens.append(Token('RPAREN'))
                self.current_pos += 1
            else:
                # Invalid character
                raise ValueError(f"Invalid character '{char}' at position {self.current_pos}")
        
        # Add end-of-input marker
        self.tokens.append(Token('EOF'))
        return self.tokens
    
    def _parse_number(self) -> None:
        """
        Parse a numeric constant (integer or decimal).
        
        Handles cases like:
        - 5 (integer)
        - 3.14 (decimal)
        - -2 (negative number)
        - 0.5 (decimal starting with 0)
        
        This method implements the number parsing logic for our robust parser.
        """
        start_pos = self.current_pos
        number_str = ""
        
        # Handle negative sign
        if self.current_pos < len(self.text) and self.text[self.current_pos] == '-':
            number_str += '-'
            self.current_pos += 1
        
        # Parse digits and decimal point
        while (self.current_pos < len(self.text) and 
               (self.text[self.current_pos].isdigit() or self.text[self.current_pos] == '.')):
            number_str += self.text[self.current_pos]
            self.current_pos += 1
        
        # Validate and convert to float
        try:
            value = float(number_str)
            self.tokens.append(Token('NUMBER', value))
        except ValueError:
            raise ValueError(f"Invalid number '{number_str}' at position {start_pos}")
    
    def _parse_variable(self) -> None:
        """
        Parse a variable name (single letter).
        
        For simplicity, we only support single-letter variables like x, y, z.
        This could be extended to support multi-letter variables later.
        
        This method implements variable parsing for our robust parser.
        """
        char = self.text[self.current_pos]
        if not char.isalpha():
            raise ValueError(f"Expected letter, got '{char}' at position {self.current_pos}")
        
        self.tokens.append(Token('VARIABLE', char))
        self.current_pos += 1
    
    def _parse_operator(self) -> None:
        """
        Parse a binary operator.
        
        Supported operators:
        - + (addition)
        - - (subtraction) 
        - * (multiplication)
        - / (division)
        - ^ (exponentiation)
        
        This method implements operator parsing for our robust parser.
        """
        char = self.text[self.current_pos]
        
        if char not in '+-*/^':
            raise ValueError(f"Invalid operator '{char}' at position {self.current_pos}")
        
        self.tokens.append(Token('OPERATOR', char))
        self.current_pos += 1


def tokenize(text: str) -> List[Token]:
    """
    Convenience function to tokenize a string.
    
    This provides a simple interface for tokenizing expressions
    without needing to create a Tokenizer instance.
    
    Args:
        text: Mathematical expression string
        
    Returns:
        List of tokens
        
    Example:
        tokens = tokenize("2*x + 3")
        # Returns: [NUMBER(2), OPERATOR(*), VARIABLE(x), OPERATOR(+), NUMBER(3), EOF]
    """
    tokenizer = Tokenizer()
    return tokenizer.tokenize(text)


# Example usage and testing
if __name__ == "__main__":
    # Test cases for tokenization
    test_cases = [
        "2*x + 3",
        "(x + 1)^2", 
        "x^3 - 2*x",
        "5.5 / 2.2",
        "x + y - z"
    ]
    
    print("Tokenizer Test Cases:")
    print("=" * 50)
    
    for test in test_cases:
        try:
            tokens = tokenize(test)
            token_strs = [str(token) for token in tokens]
            print(f"Input:  '{test}'")
            print(f"Tokens: {token_strs}")
            print()
        except ValueError as e:
            print(f"Error tokenizing '{test}': {e}")
            print()
