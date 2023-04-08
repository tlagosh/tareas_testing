from ast import *
import os
from profiler import Profiler
import ast

# Clase que permite inyectar codigo de tal forma que podamos reportar los metodos de alguna clase que se ejecutaron
class ClassInstrumentor(NodeTransformer):

    def __init__(self):
        self.visited_functions = []

    def visit_Module(self, node: Module):
        transformedNode = NodeTransformer.generic_visit(self, node)
        import_profile_injected = parse("from classInstrumentor import ClassProfiler")
        transformedNode.body.insert(0, import_profile_injected.body[0])
        fix_missing_locations(transformedNode)

        return transformedNode
    
    def visit_ClassDef(self, node: ClassDef):
        transformedNode = NodeTransformer.generic_visit(self, node)
        # For each method in the class we inject the profiler call at the beginning of the method
        for method in transformedNode.body:
            if isinstance(method, ast.FunctionDef):
                injectedCode = parse('ClassProfiler.record(\''+
                'method' + '\',\'' + 'None' + '\',\'' + str(method.lineno) + '\', \'' + str(transformedNode.name) + '\', \'' + str(method.name) + '\')')
                if isinstance(method.body, list):
                    method.body.insert(1, injectedCode.body[0])
                    #we erase the first line of the method body because it is the pass statement
                    method.body.pop(0)
                else:
                    method.body = [injectedCode.body[0], method.body]

        fix_missing_locations(method)
        return transformedNode


    def visit_FunctionDef(self, node: FunctionDef):
        transformedNode = NodeTransformer.generic_visit(self, node)
        # Inyectamos codigo para llamar al profiler en la primera linea de la definicion de una funcion
        injectedCode = parse('ClassProfiler.record(\''+
        'function' + '\',\'' + str(transformedNode.name) + '\',\'' + 'None' + '\', \'' + 'None' + '\', \'' + 'None' + '\')')
        if isinstance(transformedNode.body, list):
            transformedNode.body.insert(0, injectedCode.body[0])
        else:
            transformedNode.body = [injectedCode.body[0], node.body]
        fix_missing_locations(transformedNode)
        return transformedNode


class ClassProfiler(Profiler):

    @classmethod
    def record(cls, type, functionName, line, class_name, method_name):
        if type == 'function':
            cls.getInstance().change_function(functionName)
        else:
            cls.getInstance().ins_record(line, class_name, method_name)

    # Metodos de instancia
    def __init__(self):
        self.executed_methods = {}
        self.current_function = None

    def ins_record(self, line, class_name, method_name):
        if self.current_function not in self.executed_methods:
            self.executed_methods[self.current_function] = []
        if (method_name, int(line), class_name) not in self.executed_methods[self.current_function]:
            self.executed_methods[self.current_function].append((method_name, int(line), class_name))

    def change_function(self, functionName):
        self.current_function = functionName
    
    # report executed methods: Este metodo retorna una lista de tuplas que representan los metodos que fueron ejecutados (excluye las
    # funciones que fueron definidas fuera de alguna clase). La lista esta ordenada descendentemente en base al segundo elemento de la tupla
    # (t[1]) y cada tupla tiene el formato: (<method-name>,<codeline-methodDef>,<method-class>)

    def report_executed_methods(self):
        
        print("-- Executed methods --")

        executed_methods = []
        for fun in self.executed_methods:
            print("Function " + fun)
            for (method_name, line, class_name) in self.executed_methods[fun]:
                print("Method " + method_name + " from class " + class_name + " at line " + str(line))
                if (method_name, line, class_name) not in executed_methods:
                    executed_methods.append((method_name, line, class_name))
        
        # Ordenamos la lista de metodos ejecutados
        executed_methods.sort(key=lambda x: x[1], reverse=False)
        return executed_methods
    
    # report executed by: Este m´etodo recibe el nombre de una funci´on ejecutada (no pertenece a una clase) y retorna una lista de tuplas que
    # representan los m´etodos que fueron llamados por esa funci´on. La lista retornada esta ordenada descendentemente en base al segundo elemento de cada tupla (t[1]), donde cada tupla
    # sigue el formato: (<method-name>,<codeline-methodDef>, <method-class>)

    def report_executed_by(self, functionName):
        print("-- Executed by " + functionName + " --")
        executed_methods = []
        for (method_name, line, class_name) in self.executed_methods[functionName]:
            print("Method " + method_name + " from class " + class_name + " at line " + str(line))
            executed_methods.append((method_name, line, class_name))
        return executed_methods

def instrument(ast):
    visitor = ClassInstrumentor()
    return fix_missing_locations(visitor.visit(ast))


