import ast
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class ASTPatcher(ast.NodeTransformer):
    """
    Modifies Python code safely using Abstract Syntax Trees (AST).
    Inherits from NodeTransformer to allow targeted modifications.
    """

    @staticmethod
    def read_ast(file_path: str) -> Optional[ast.Module]:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                source = f.read()
            return ast.parse(source)
        except Exception as e:
            logger.error(f"Error reading AST from {file_path}: {e}")
            return None

    @staticmethod
    def write_ast(tree: ast.Module, file_path: str) -> bool:
        try:
            ast.fix_missing_locations(tree)
            # unparse requires Python 3.9+
            source = ast.unparse(tree)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(source)
            return True
        except Exception as e:
            logger.error(f"Error writing AST to {file_path}: {e}")
            return False

    @classmethod
    def apply_patch(cls, file_path: str, patcher_instance: ast.NodeTransformer) -> bool:
        """
        Applies a specific NodeTransformer to a file and saves it.
        """
        tree = cls.read_ast(file_path)
        if tree is None:
            return False
        
        patched_tree = patcher_instance.visit(tree)
        return cls.write_ast(patched_tree, file_path)

# Example usage for Mechanic:
# class TargetModifier(ASTPatcher):
#     def visit_FunctionDef(self, node):
#         if node.name == 'target_func':
#             # Modify node.body or arguments
#             pass
#         return self.generic_visit(node)
# 
# ASTPatcher.apply_patch("some_file.py", TargetModifier())
