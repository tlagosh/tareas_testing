from .rule import *
import ast

'''
SuperInitNotCalled - Se agregara un warning cada vez
que en el metodo init de una subclase no se llame al
metodo init de su super clase. En el ejemplo, la clase
Circle es subclase de Shape y en el metodo init de
Circle no se llama al metodo init de Shape. Cada
warning debe ser generado en base al siguiente formato:
Warning("SuperInitNotCalled",
<codeline-subclassDef>,
"subclass " + <subclass-name> +
" does not call to super().__init__()")
'''

# Clases que permiten detectar clases que no llaman al metodo init de su super clase en su metodo init

class SuperInitNotCalledVisitor(WarningNodeVisitor):

    def __init__(self):
        super().__init__()
        self.currentClass = None
    
    # visitamos las clases, si es que son subclases, vemos si llaman al metodo init de su super clase, si no lo hacen, agregamos un warning
    def visit_ClassDef(self, node: ClassDef):
        if node.bases:
            self.currentClass = node.name
            for stmt in node.body:
                if isinstance(stmt, FunctionDef):
                    if stmt.name == '__init__':
                        if not self.checkInit(stmt):
                            self.addWarning('SuperInitNotCalled', node.lineno, 'subclass ' + self.currentClass + ' does not call to super().__init__()')
        self.generic_visit(node)
    
    # revisamos si el metodo init de la subclase llama al metodo init de su super clase
    def checkInit(self, node: FunctionDef):
        for stmt in node.body:
            if isinstance(stmt, Expr):
                if isinstance(stmt.value, Call):
                    if isinstance(stmt.value.func, Attribute):
                        if stmt.value.func.attr == '__init__':
                            if isinstance(stmt.value.func.value, Call):
                                if isinstance(stmt.value.func.value.func, Name):
                                    if stmt.value.func.value.func.id == 'super':
                                        return True
        return False
                
            

class SuperInitNotCalledRule(Rule):

    def analyze(self, ast):
        visitor = SuperInitNotCalledVisitor()
        visitor.visit(ast)
        return visitor.warningsList()