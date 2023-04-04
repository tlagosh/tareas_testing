from .rewriter import *
import ast

# Clases que permiten transformar codigo que contiene expresiones de la forma a = a - b por a -= b.

class MinusEqualsTransformer(NodeTransformer):

    def visit_Assign(self, node: Assign):
        if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            target_name = node.targets[0].id
            for value_node in ast.walk(node.value):
                if isinstance(value_node, ast.BinOp) and isinstance(value_node.op, ast.Sub) and isinstance(value_node.left, ast.Name) and value_node.left.id == target_name:
                    return ast.AugAssign(target=node.targets[0], op=ast.Sub(), value=value_node.right)
        return node


class MinusEqualsRewriterCommand(RewriterCommand):
    
    def apply(self, ast):
        # La funcion fix_missing_locations se utiliza para recorrer los nodos del AST y actualizar ciertos atributos (e.g., numero de linea) considerando ahora la modificacion
        new_tree = fix_missing_locations(MinusEqualsTransformer().visit(ast))
        return new_tree