from .rule import *
import ast

'''
UnusedArgument - Se agregara un warning por cada argumento en la definicion de un metodo que no es usado dentro
del mismo metodo. En el ejemplo, el argumento x no est´a
siendo usado. Cada warning debe ser generado en base al
siguiente formato:
Warning("UnusedArgument", <codeline-functionDef>,
"argument " + <unusedArg-name> + " is not used")
'''

# Clases que permiten detectar argumentos que no son usados en una funcion, por ejemplo:
# def example(x, y, z):
#    return y + z

class UnusedArgumentVisitor(WarningNodeVisitor):

    def __init__(self):
        super().__init__()

    def visit_FunctionDef(self, node: FunctionDef):
        arg_names = [arg.arg for arg in node.args.args]
        for stmt in node.body:
            for name in ast.walk(stmt):
                if isinstance(name, ast.Name) and name.id in arg_names:
                    arg_names.remove(name.id)
        if arg_names:
            for arg_name in arg_names:
                self.addWarning("UnusedArgument", node.lineno, "argument " + arg_name + " is not used")
        self.generic_visit(node)
                    

  
class UnusedArgumentRule(Rule):

    def analyze(self, ast):
        visitor = UnusedArgumentVisitor()
        visitor.visit(ast)
        return visitor.warningsList()