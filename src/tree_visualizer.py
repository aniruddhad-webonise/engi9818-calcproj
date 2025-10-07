"""
Tree Visualizer - Display Expression Trees as Text

This module provides visualization capabilities for expression trees,
showing the hierarchical structure in a readable text format.

PROJECT REQUIREMENTS ADDRESSED:
- ✅ Tree-based representation (visualization of AST structure)
- ✅ Data structures (tree traversal for visualization)
- ✅ Algorithms for symbolic manipulation (tree display algorithms)

VISUALIZATION FEATURES:
- Text-based tree display with ASCII art
- Hierarchical structure showing parent-child relationships
- Node type and value information
- Configurable display options

EXAMPLES:
Input:  BinaryOp(+, BinaryOp(*, Number(2), Variable(x)), Number(3))
Output: 
    +
   / \
  *   3
 / \
2   x
"""

from typing import List, Optional, Tuple
try:
    from .nodes import Node, Number, Variable, BinaryOp
except ImportError:
    # For testing when run directly
    from nodes import Node, Number, Variable, BinaryOp


class TreeVisualizer:
    """
    Visualizes expression trees as text-based diagrams.
    
    This implements tree visualization algorithms that convert the
    hierarchical structure of expression trees into readable text
    representations using ASCII art.
    """
    
    @staticmethod
    def visualize(node: Node, show_values: bool = True, max_width: int = 80) -> str:
        """
        Create a text visualization of an expression tree.
        
        Args:
            node: The root node of the expression tree
            show_values: Whether to show node values in the visualization
            max_width: Maximum width for the visualization
            
        Returns:
            Multi-line string representing the tree structure
        """
        lines = TreeVisualizer._build_tree_lines(node, show_values)
        
        # Center the tree if it's not too wide
        if lines:
            max_line_width = max(len(line.rstrip()) for line in lines)
            if max_line_width <= max_width:
                lines = [line.center(max_width) for line in lines]
        
        return '\n'.join(lines)
    
    @staticmethod
    def _build_tree_lines(node: Node, show_values: bool) -> List[str]:
        """
        Build the lines for tree visualization recursively.
        
        Args:
            node: Current node to visualize
            show_values: Whether to show node values
            
        Returns:
            List of strings representing the tree lines
        """
        if isinstance(node, Number):
            return [f"Number({node.value})" if show_values else "Number"]
        
        if isinstance(node, Variable):
            return [f"Variable({node.name})" if show_values else "Variable"]
        
        if isinstance(node, BinaryOp):
            # Get child visualizations
            left_lines = TreeVisualizer._build_tree_lines(node.left, show_values)
            right_lines = TreeVisualizer._build_tree_lines(node.right, show_values)
            
            # Create the operator line
            operator_text = f"'{node.operator}'" if show_values else "Op"
            operator_line = f"  {operator_text}  "
            
            # Combine left and right subtrees
            return TreeVisualizer._combine_subtrees(left_lines, operator_line, right_lines)
        
        return ["Unknown"]
    
    @staticmethod
    def _combine_subtrees(left_lines: List[str], operator_line: str, right_lines: List[str]) -> List[str]:
        """
        Combine left and right subtree visualizations with an operator.
        
        Args:
            left_lines: Lines for left subtree
            operator_line: Line containing the operator
            right_lines: Lines for right subtree
            
        Returns:
            Combined tree visualization lines
        """
        # Ensure both subtrees have the same height
        max_height = max(len(left_lines), len(right_lines))
        left_lines = TreeVisualizer._pad_lines(left_lines, max_height)
        right_lines = TreeVisualizer._pad_lines(right_lines, max_height)
        
        # Create the combined visualization
        result = []
        
        # Add the operator line
        result.append(operator_line)
        
        # Add connection lines
        if left_lines or right_lines:
            left_width = len(left_lines[0]) if left_lines else 0
            right_width = len(right_lines[0]) if right_lines else 0
            
            # Create connection lines
            left_conn = "┌" + "─" * (left_width - 2) if left_width > 2 else "┌"
            right_conn = "─" * (right_width - 2) + "┐" if right_width > 2 else "┐"
            
            # Center the connections under the operator
            total_width = left_width + len(operator_line) + right_width
            left_padding = (total_width - len(left_conn) - len(right_conn)) // 2
            right_padding = total_width - len(left_conn) - len(right_conn) - left_padding
            
            conn_line = " " * left_padding + left_conn + right_conn + " " * right_padding
            result.append(conn_line)
        
        # Add the subtree lines
        for i in range(max_height):
            left_line = left_lines[i] if i < len(left_lines) else ""
            right_line = right_lines[i] if i < len(right_lines) else ""
            
            # Combine left and right lines
            combined_line = left_line + " " + right_line
            result.append(combined_line)
        
        return result
    
    @staticmethod
    def _pad_lines(lines: List[str], target_height: int) -> List[str]:
        """
        Pad lines to a target height with empty strings.
        
        Args:
            lines: List of lines to pad
            target_height: Target number of lines
            
        Returns:
            Padded list of lines
        """
        while len(lines) < target_height:
            lines.append("")
        return lines
    
    @staticmethod
    def visualize_simple(node: Node) -> str:
        """
        Create a simple one-line representation of the tree.
        
        Args:
            node: The root node of the expression tree
            
        Returns:
            Simple string representation
        """
        if isinstance(node, Number):
            return str(node.value)
        
        if isinstance(node, Variable):
            return node.name
        
        if isinstance(node, BinaryOp):
            left_str = TreeVisualizer.visualize_simple(node.left)
            right_str = TreeVisualizer.visualize_simple(node.right)
            return f"({left_str} {node.operator} {right_str})"
        
        return "Unknown"


def visualize_tree(node: Node, style: str = "detailed", **kwargs) -> str:
    """
    Convenience function to visualize an expression tree.
    
    Args:
        node: The expression tree to visualize
        style: Visualization style ("detailed" or "simple")
        **kwargs: Additional options for visualization
        
    Returns:
        String representation of the tree
    """
    if style == "simple":
        return TreeVisualizer.visualize_simple(node)
    else:
        return TreeVisualizer.visualize(node, **kwargs)


# Example usage and testing
if __name__ == "__main__":
    from parser import parse_expression
    
    # Test cases for tree visualization
    test_cases = [
        "2*x + 3",
        "x^3",
        "(x + 1)^2",
        "x^2 + 2*x + 1",
        "2^3^2"
    ]
    
    print("Tree Visualization Test Cases:")
    print("=" * 60)
    
    for test in test_cases:
        try:
            tree = parse_expression(test)
            
            print(f"\nExpression: {test}")
            print("Simple view:", visualize_tree(tree, style="simple"))
            print("\nDetailed tree structure:")
            print(visualize_tree(tree, style="detailed"))
            print("-" * 40)
            
        except Exception as e:
            print(f"Error visualizing '{test}': {e}")
            print("-" * 40)
