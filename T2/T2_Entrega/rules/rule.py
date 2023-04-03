from ast import *

class Warning:

    def __init__(self, name, line, description):
        self.name = name
        self.lineNumber = line
        self.description = description

    # Sobreescribimos el metodo __str__ para dar una representacion de cadena de una instancia de Warning
    def __str__(self):
        return "[ Line " + str(self.lineNumber) + " ] " + self.name + " - " + self.description

    # Sobreescribimos el metodo __eq__ para personalizar como se comparan dos instancias
    def __eq__(self, other):
        if isinstance(other, Warning):
            return self.name == other.name and self.lineNumber == other.lineNumber and self.description == other.description
        else:
            return False

    # Sobreescribimos el metodo __gt__ para personalizar el comportamiento del operador >
    def __gt__(self, other):
        if self.lineNumber == other.lineNumber:
            return self.name > other.name
        return self.lineNumber > other.lineNumber
        

class Rule:

    def __init__(self):
        self.warningsList = []
    
    def analyze(self, ast):
        pass
    
    # Debe retornar una lista de objetos warnings
    def warnings(self):
        return self.warningsList


class WarningNodeVisitor(NodeVisitor):

    def __init__(self):
        self.warnings = []
    
    def addWarning(self, name, lineo, description):
        self.warnings.append(Warning(name, lineo, description))

    def warningsList(self):
        return self.warnings
    
# Desde aquí comienza el código de la entrega

# La siguiente clase debe seguir estas instrucciones:
'''
LongVariableName - Se agregar´a un warning por cada variable que tenga un nombre que exceda de los 15 caracteres.
Se debe considerar dos casos: variables temporales y variables de instancia. Cada warning debe ser generado en base
al siguiente formato:
Warning("VariableLongName", <codeline-variable>,
"variable " + <var-name> + " has a long name")

'''

class LongVariableNameRule(Rule):

    def __init__(self):
        super().__init__()

    def analyze(self, ast):
        visitor = LongVariableNameVisitor()
        visitor.visit(ast)
        self.warningsList = visitor.warningsList()
        return self.warningsList

class LongVariableNameVisitor(WarningNodeVisitor):

    def __init__(self):
        super().__init__()

    def visit_Assign(self, node: Assign):
        for target in node.targets:
            if isinstance(target, Name):
                if len(target.id) > 15:
                    self.addWarning("VariableLongName", node.lineno, "variable " + target.id + " has a long name")
        self.generic_visit(node)

    def visit_FunctionDef(self, node: FunctionDef):
        for arg in node.args.args:
            if len(arg.arg) > 15:
                self.addWarning("VariableLongName", node.lineno, "variable " + arg.arg + " has a long name")
        self.generic_visit(node)


'''
UnusedArgument - Se agregar´a un warning por cada argumento en la definici´on de un m´etodo que no es usado dentro
del mismo m´etodo. En el ejemplo, el argumento x no est´a
siendo usado. Cada warning debe ser generado en base al
siguiente formato:
Warning("UnusedArgument", <codeline-functionDef>,
"argument " + <unusedArg-name> + " is not used")
'''
    
class UnusedArgumentRule(Rule):

    def __init__(self):
        super().__init__()

    def analyze(self, ast):
        visitor = UnusedArgumentVisitor()
        visitor.visit(ast)
        self.warningsList = visitor.warningsList()
        return self.warningsList

class UnusedArgumentVisitor(WarningNodeVisitor):

    def __init__(self):
        super().__init__()

    def visit_FunctionDef(self, node: FunctionDef):
        usedArgs = []
        for arg in node.args.args:
            usedArgs.append(arg.arg)
        for stmt in node.body:
            if isinstance(stmt, Assign):
                for target in stmt.targets:
                    if isinstance(target, Name):
                        if target.id in usedArgs:
                            usedArgs.remove(target.id)
            elif isinstance(stmt, AugAssign):
                if isinstance(stmt.target, Name):
                    if stmt.target.id in usedArgs:
                        usedArgs.remove(stmt.target.id)
            elif isinstance(stmt, Return):
                if isinstance(stmt.value, Name):
                    if stmt.value.id in usedArgs:
                        usedArgs.remove(stmt.value.id)
            elif isinstance(stmt, Expr):
                if isinstance(stmt.value, Name):
                    if stmt.value.id in usedArgs:
                        usedArgs.remove(stmt.value.id)
        for arg in usedArgs:
            self.addWarning("UnusedArgument", node.lineno, "argument " + arg + " is not used")
        self.generic_visit(node)


'''
SuperInitNotCalled - Se agregar´a un warning cada vez
que en el m´etodo init de una subclase no se llame al
m´etodo init de su super clase. En el ejemplo, la clase
Circle es subclase de Shape y en el m´etodo init de
Circle no se llama al m´etodo init de Shape. Cada
warning debe ser generado en base al siguiente formato:
Warning("SuperInitNotCalled",
<codeline-subclassDef>,
"subclass " + <subclass-name> +
" does not call to super().__init__()")
'''

class SuperInitNotCalled(Rule):

    def __init__(self):
        super().__init__()

    def analyze(self, ast):
        visitor = SuperInitNotCalledVisitor()
        visitor.visit(ast)
        self.warningsList = visitor.warningsList()
        return self.warningsList

class SuperInitNotCalledVisitor(WarningNodeVisitor):

    def __init__(self):
        super().__init__()

    def visit_FunctionDef(self, node: FunctionDef):
        if node.name == "__init__":
            for stmt in node.body:
                if isinstance(stmt, Expr):
                    if isinstance(stmt.value, Call):
                        if isinstance(stmt.value.func, Attribute):
                            if stmt.value.func.attr == "__init__":
                                if isinstance(stmt.value.func.value, Name):
                                    if stmt.value.func.value.id == "super":
                                        return
        self.addWarning("SuperInitNotCalled", node.lineno, "subclass " + node.name + " does not call to super().__init__()")
        self.generic_visit(node)
