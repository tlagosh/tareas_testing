from .rule import *
import ast

'''
LongVariableName - Se agregara un warning por cada variable que tenga un nombre que exceda de los 15 caracteres.
Se debe considerar dos casos: variables temporales y variables de instancia. Cada warning debe ser generado en base
al siguiente formato:
Warning("VariableLongName", <codeline-variable>,
"variable " + <var-name> + " has a long name")
'''

class LongVariableNameVisitor(WarningNodeVisitor):

    def __init__(self):
        super().__init__()
        self.threshold = 15
        self.currentClass = None

    def visit_Name(self, node: Name):
        if len(node.id) > self.threshold:
            self.addWarning('VariableLongName', node.lineno, 'variable ' + node.id + ' has a long name')
        self.generic_visit(node)
    
    # we also visit the self. variables
    def visit_Attribute(self, node: Attribute):
        if isinstance(node.value, Name):
            if node.value.id == 'self':
                if len(node.attr) > self.threshold:
                    self.addWarning('VariableLongName', node.lineno, 'variable ' + node.attr + ' has a long name')
        self.generic_visit(node)

class LongVariableNameRule(Rule):

    def analyze(self, ast):
        visitor = LongVariableNameVisitor()
        visitor.visit(ast)
        return visitor.warningsList()