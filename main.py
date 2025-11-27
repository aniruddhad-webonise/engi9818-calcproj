#!/usr/bin/env python3
"""
Command-Line Calculator with Symbolic Differentiation

This is the main entry point for our symbolic differentiation calculator.
It provides an interactive command-line interface that allows users to:
- Parse mathematical expressions
- Compute symbolic derivatives
- Evaluate expressions at specific points
- Simplify derivative expressions

PROJECT REQUIREMENTS ADDRESSED:
- Command-Line Calculator (interactive CLI interface)
- Symbolic Differentiation (complete differentiation pipeline)
- Basic Arithmetic (expression evaluation)
- Parse Mathematical Expressions (tokenization + parsing)
- Tree-based Representation (AST with node classes)
- Algorithms for Symbolic Manipulation (differentiation + simplification)

USAGE:
    python main.py                    # Interactive mode
    python main.py "2*x + 3"         # Single expression mode
    python main.py --help            # Show help
"""

import sys
import argparse
from typing import Dict, Optional

try:
    # Use the clean imports from the src module
    from src import parse_expression, simplify_expression, visualize_tree
except ImportError:
    # Fallback for direct execution (when running from src/ directory)
    from parser import parse_expression
    from simplifier import simplify_expression
    from tree_visualizer import visualize_tree


class Calculator:
    """
    Main calculator class that orchestrates the entire pipeline.
    
    This class provides the command-line interface and coordinates between
    the parser, differentiator, simplifier, and evaluator components.
    """
    
    def __init__(self):
        """Initialize the calculator."""
        self.variables: Dict[str, float] = {}
    
    def parse_and_differentiate(self, expression: str, variable: str = 'x') -> str:
        """
        Parse an expression and compute its derivative.
        
        Args:
            expression: Mathematical expression string
            variable: Variable to differentiate with respect to
            
        Returns:
            Simplified derivative as string
            
        Raises:
            ValueError: If expression is malformed
        """
        try:
            # Parse the expression
            tree = parse_expression(expression)
            
            # Compute derivative
            derivative = tree.differentiate(variable)
            
            # Simplify the result
            simplified = simplify_expression(derivative)
            
            return str(simplified)
        except Exception as e:
            raise ValueError(f"Error processing expression '{expression}': {e}")
    
    def evaluate_expression(self, expression: str, variables: Optional[Dict[str, float]] = None) -> float:
        """
        Evaluate an expression with given variable values.
        
        Args:
            expression: Mathematical expression string
            variables: Dictionary of variable values
            
        Returns:
            Numeric result
            
        Raises:
            ValueError: If expression is malformed or variables undefined
        """
        try:
            tree = parse_expression(expression)
            return tree.evaluate(variables or self.variables)
        except Exception as e:
            raise ValueError(f"Error evaluating expression '{expression}': {e}")
    
    def set_variable(self, name: str, value: float) -> None:
        """Set a variable value for evaluation."""
        self.variables[name] = value
    
    def get_variables(self) -> Dict[str, float]:
        """Get current variable values."""
        return self.variables.copy()
    
    def clear_variables(self) -> None:
        """Clear all variable values."""
        self.variables.clear()
    
    def visualize_expression(self, expression: str, style: str = "detailed") -> str:
        """
        Visualize an expression as a tree structure.
        
        Args:
            expression: Mathematical expression string
            style: Visualization style ("detailed" or "simple")
            
        Returns:
            Tree visualization string
            
        Raises:
            ValueError: If expression is malformed
        """
        try:
            tree = parse_expression(expression)
            return visualize_tree(tree, style=style)
        except Exception as e:
            raise ValueError(f"Error visualizing expression '{expression}': {e}")


def print_banner():
    """Print the calculator banner."""
    print("=" * 60)
    print("🧮 Command-Line Calculator with Symbolic Differentiation")
    print("=" * 60)
    print("Features:")
    print("  • Parse mathematical expressions")
    print("  • Compute symbolic derivatives")
    print("  • Evaluate expressions at specific points")
    print("  • Simplify derivative expressions")
    print("  • Visualize expression trees")
    print()
    print("Supported operations: +, -, *, /, ^ (exponentiation)")
    print("Supported functions: Variables (x, y, z, etc.)")
    print("Type 'help' for commands, 'quit' to exit")
    print("=" * 60)


def print_help():
    """Print help information."""
    print("\n Calculator Commands:")
    print("  help, h          - Show this help message")
    print("  quit, q, exit   - Exit the calculator")
    print("  clear           - Clear all variable values")
    print("  vars            - Show current variable values")
    print("  set <var> <val> - Set variable value (e.g., 'set x 5')")
    print()
    print(" Expression Commands:")
    print("  diff <expr>                     - Differentiate expression")
    print("  eval <expr>                     - Evaluate expression")
    print("  tree <expr>                     - Show expression tree structure")
    print()
    print("🔧 Advanced Usage:")
    print("  diff <expr> wrt <var>            - Differentiate with respect to variable")
    print("  eval <expr> at x=5               - Evaluate with specific values")
    print("  tree <expr> simple               - Show simple tree view")
    print()
    print(" Examples:")
    print("  diff 2*x + 3                    - Differentiate 2x + 3")
    print("  tree (x + 1)^2                  - Show tree for (x + 1)²")
    print("  eval x^2 + y^2 at x=3,y=4       - Evaluate x² + y² at x=3, y=4")


def interactive_mode():
    """Run the calculator in interactive mode."""
    print_banner()
    
    calc = Calculator()
    
    while True:
        try:
            # Get user input
            user_input = input("\ncalc> ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() in ['quit', 'q', 'exit']:
                print(" Goodbye!")
                break
            
            elif user_input.lower() in ['help', 'h']:
                print_help()
                continue
            
            elif user_input.lower() == 'clear':
                calc.clear_variables()
                print(" Variables cleared")
                continue
            
            elif user_input.lower() == 'vars':
                vars_dict = calc.get_variables()
                if vars_dict:
                    print(" Current variables:")
                    for var, val in vars_dict.items():
                        print(f"  {var} = {val}")
                else:
                    print(" No variables set")
                continue
            
            elif user_input.startswith('set '):
                parts = user_input.split()
                if len(parts) == 3:
                    try:
                        var_name = parts[1]
                        var_value = float(parts[2])
                        calc.set_variable(var_name, var_value)
                        print(f" Set {var_name} = {var_value}")
                    except ValueError:
                        print(" Error: Invalid variable value")
                else:
                    print(" Usage: set <variable> <value>")
                continue
            
            # Handle differentiation
            elif user_input.startswith('diff '):
                expr = user_input[5:].strip()
                
                # Check for "wrt" (with respect to)
                if ' wrt ' in expr:
                    expr, var = expr.split(' wrt ', 1)
                    expr = expr.strip()
                    var = var.strip()
                else:
                    var = 'x'  # Default variable
                
                try:
                    derivative = calc.parse_and_differentiate(expr, var)
                    print(f"📐 d/d{var}({expr}) = {derivative}")
                except ValueError as e:
                    print(f" {e}")
                continue
            
            # Handle evaluation
            elif user_input.startswith('eval '):
                expr = user_input[5:].strip()
                
                # Check for "at" clause
                if ' at ' in expr:
                    expr, at_clause = expr.split(' at ', 1)
                    expr = expr.strip()
                    
                    # Parse variable assignments
                    assignments = at_clause.split(',')
                    temp_vars = {}
                    for assignment in assignments:
                        if '=' in assignment:
                            var_name, var_value = assignment.split('=', 1)
                            try:
                                temp_vars[var_name.strip()] = float(var_value.strip())
                            except ValueError:
                                print(f" Error: Invalid value for {var_name.strip()}")
                                break
                    else:
                        try:
                            result = calc.evaluate_expression(expr, temp_vars)
                            print(f"🔢 {expr} = {result}")
                        except ValueError as e:
                            print(f" {e}")
                        continue
                
                # Use current variables
                try:
                    result = calc.evaluate_expression(expr)
                    print(f"🔢 {expr} = {result}")
                except ValueError as e:
                    print(f" {e}")
                continue
            
            # Handle tree visualization
            elif user_input.startswith('tree '):
                expr = user_input[5:].strip()
                
                # Check for style option
                style = "detailed"
                if expr.endswith(' simple'):
                    expr = expr[:-7].strip()
                    style = "simple"
                
                try:
                    tree_vis = calc.visualize_expression(expr, style)
                    print(f" Expression tree for '{expr}':")
                    print(tree_vis)
                except ValueError as e:
                    print(f" {e}")
                continue
            
            # Default: try to evaluate as expression
            else:
                try:
                    result = calc.evaluate_expression(user_input)
                    print(f" {user_input} = {result}")
                except ValueError as e:
                    print(f" {e}")
                    print(" Try 'help' for available commands")
                continue
        
        except KeyboardInterrupt:
            print("\n Goodbye!")
            break
        except EOFError:
            print("\n Goodbye!")
            break


def single_expression_mode(expression: str):
    """Run the calculator in single expression mode."""
    calc = Calculator()
    
    try:
        # Try differentiation first
        derivative = calc.parse_and_differentiate(expression)
        print(f"📐 d/dx({expression}) = {derivative}")
        
        # Try evaluation if possible
        try:
            result = calc.evaluate_expression(expression)
            print(f"🔢 {expression} = {result}")
        except ValueError:
            print("💡 Expression contains variables - use interactive mode to set values")
    
    except ValueError as e:
        print(f"❌ {e}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Command-Line Calculator with Symbolic Differentiation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Interactive mode
  python main.py "2*x + 3"         # Differentiate and evaluate 2x + 3
  python main.py "x^3 - 2*x"       # Differentiate and evaluate x³ - 2x
        """
    )
    
    parser.add_argument(
        'expression',
        nargs='?',
        help='Mathematical expression to process'
    )
    
    args = parser.parse_args()
    
    if args.expression:
        # Single expression mode
        single_expression_mode(args.expression)
    else:
        # Interactive mode
        interactive_mode()


if __name__ == "__main__":
    main()
