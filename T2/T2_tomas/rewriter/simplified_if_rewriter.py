from .rewriter import *
import ast
import astor

# Clases que permiten transformar codigo que contiene expresiones de la forma:
# def example(x, y):
#     return True if <condicion> else False
# por:
# def example(x, y):
#     return <condicion>
#y
# def example(x, y):
#     return False if <condicion> else True
# por:
# def example(x, y):
#     return not <condicion>

class SimplifiedIfTransformer(NodeTransformer):

   def visit_Return(self, node):
        if isinstance(node.value, ast.IfExp):
            if isinstance(node.value.body, ast.NameConstant) and node.value.body.value is True and isinstance(node.value.orelse, ast.NameConstant) and node.value.orelse.value is False:
                return ast.Return(value=node.value.test)
            elif isinstance(node.value.body, ast.NameConstant) and node.value.body.value is False and isinstance(node.value.orelse, ast.NameConstant) and node.value.orelse.value is True:
                return ast.Return(value=ast.UnaryOp(op=ast.Not(), operand=node.value.test))
        return node
   

class SimplifiedIfRewriterCommand(RewriterCommand):
    
    def apply(self, ast):
        # La funcion fix_missing_locations se utiliza para recorrer los nodos del AST y actualizar ciertos atributos (e.g., numero de linea) considerando ahora la modificacion
        new_tree = fix_missing_locations(SimplifiedIfTransformer().visit(ast))
        return new_tree