import unittest
from rules import *
from rewriter import *

"""
Template para los tests de las reglas y transformaciones adicionales propuestos por usted.
IMPORTANTE: 
    - Deben existir al menos 5 tests, uno por cada regla/transformador implementado.
    - Los codigos a ser analizados usados en los tests deben ser diferentes.
    - Los tests adicionales deben ser diferentes a los del archivo tests-tarea.py
    - Si usted implemento la tarea en un nuevo archivo dentro del folder rules o rewriter
    no olvide modificar el __init__.py de rules y rewriter para importar los archivos necesarios para su tarea.
    Caso contrario importe lo necesario en este archivo.
"""

class TestWarnings(unittest.TestCase):


    # Funcion que recibe un path del archivo a ser leido y retorna un AST en base al contenido del archivo
    def get_ast_from_file(self, filename):
        file = open(filename)
        fileContent = file.read()
        file.close()
        tree = parse(fileContent)

        return tree

    """ Nombre: test_long_variable_name
        Codigo a ser analizado: extra-test-code/longVariableName.py
        Descripcion: Test para evaluar LongVariableNameRule considerando los siguientes escenarios:
        - Linea 5: Uso de variable de instancia de nombre largo : intelligenceQuotient
        - Linea 6: Uso de variable de instancia de nombre largo : hasFoodUntilTomorrow
        - Linea 9: Uso de variable de nombre largo: isDogIntelligent
        - Linea 4 y 8: Uso de variables de nombre corto (<= 15)
        
        Resultado esperado:
        [Warning('VariableLongName', 5, 'variable intelligenceQuotient has a long name'),
        Warning('VariableLongName', 6, 'variable hasFoodUntilTomorrow has a long name'),
        Warning('VariableLongName', 9, 'variable isDogIntelligent has a long name')]
    """

    def test_long_variable_name(self):
        tree = self.get_ast_from_file('extra-test-code/longVariableName.py')

        longNameRule = LongVariableNameRule()
        result = longNameRule.analyze(tree)


        # Actualice el valor de expectedWarnings de acuerdo a su caso de prueba propuesto
        expectedWarnings = [
            Warning('VariableLongName', 5, 'variable intelligenceQuotient has a long name'),
            Warning('VariableLongName', 6, 'variable hasFoodUntilTomorrow has a long name'),
            Warning('VariableLongName', 9, 'variable isDogIntelligent has a long name')
        ]
        
        self.assertEqual(result, expectedWarnings)

    """ Nombre: test_unused_argument
        Codigo a ser analizado: extra-test-code/unusedArgument.py
        Descripcion: Test para evaluar UnusedArgumentRule considerando los siguientes escenarios:
        - Linea 1: En funcion listing1, argumento list2 no es utilizado
        - Linea 11: En funcion determineList, argumento isList no es utilizado
        
        Resultado esperado:
        [Warning('UnusedArgument', 1, 'argument list2 is not used'),
        Warning('UnusedArgument', 11, 'argument isList is not used')]
    """

    def test_unused_argument(self):
        tree = self.get_ast_from_file('extra-test-code/unusedArgument.py')

        unusedArgRule = UnusedArgumentRule()
        result = unusedArgRule.analyze(tree)

        # Actualice el valor de expectedWarnings de acuerdo a su caso de prueba propuesto
        expectedWarnings = [
            Warning('UnusedArgument', 1, 'argument list2 is not used'),
            Warning('UnusedArgument', 11, 'argument isList is not used')
        ]

        self.assertEqual(result, expectedWarnings)


    """ Nombre: test_super_init_not_called
        Codigo a ser analizado: extra-test-code/superInitNotCalled.py
        Descripcion: Test para evaluar SuperInitNotCalledRule considerando los siguientes escenarios:
        - Linea 11: Definicion de __init__ de Dog (subclase de Pet) con llamada a super().__init__
        - Linea 16: Definicion de __init__ de Cat (subclase de Pet) sin llamada a super().__init__
        
        Resultado esperado:
        [Warning('SuperInitNotCalled', 13, 'subclass Cat does not call to super().__init__()')]
    """

    def test_super_init_not_called(self):
        tree = self.get_ast_from_file('extra-test-code/superInitNotCalled.py')

        superInitRule = SuperInitNotCalledRule()
        result = superInitRule.analyze(tree)

        # Actualice el valor de expectedWarnings de acuerdo a su caso de prueba propuesto
        expectedWarnings = [
            Warning('SuperInitNotCalled', 13, 'subclass Cat does not call to super().__init__()')
        ]

        self.assertEqual(result, expectedWarnings)


    """ Nombre: test_minus_equal_rewriter
        Codigo a ser analizado: extra-test-code/minusEquals.py
        Descripcion: Test para evaluar transformador MinusEqualsRewriterCommand considerando los siguientes escenarios:
        - Linea 2: Asignación input = input - 10
        - Linea 6: Asignación input1 = input1 - input2
        
        Resultado esperado: expected-code/code-minus-equal.py
    """

    def test_minus_equal_rewriter(self):
        tree = self.get_ast_from_file('extra-test-code/minusEquals.py')

        command = MinusEqualsRewriterCommand()
        tree = command.apply(tree)

        expectedCode = self.get_ast_from_file('extra-test-code/expectedMinusEquals.py')
        self.assertEqual(dump(tree), dump(expectedCode))


    """ Nombre: test_simplified_if
        Codigo a ser analizado: extra-test-code/simplifiedIf.py
        Descripcion: Test para evaluar SimplifiedIfRewriterCommand considerando los siguientes escenarios:
        - Linea 2: Uso de la expresion if cuando puede ser reemplazada por el if.test
        - Linea 7: Uso de la expresion if cuando puede ser reemplazada por el not if.test
        
        Resultado esperado: expected-code/code-simplified-if.py
    """

    def test_simplified_if(self):
        tree = self.get_ast_from_file('extra-test-code/simplifiedIf.py')

        command = SimplifiedIfRewriterCommand()
        tree = command.apply(tree)

        expectedCode = self.get_ast_from_file('extra-test-code/expectedSimplifiedIf.py')
        
        self.assertEqual(dump(tree), dump(expectedCode))

if __name__ == '__main__':
    unittest.main()
