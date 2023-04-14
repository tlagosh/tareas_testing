import sys
import ast
import traceback
from types import *
from stackInspector import StackInspector

""" Clase para rastrear funciones que fueron ejecutadas. Para su uso, considere:
with CoverageTracer() as coverage:
    function_to_be_traced()

coverage.report_executed_lines()
"""

# Este tracer identifica que lıneas de codigo fueron ejecutadas y cuantas veces.

class CoverageTracer(StackInspector):

    def __init__(self):
        self.original_trace_function = None
        self.executed_lines = []

    def traceit(self, frame, event: str, arg):
        if event == "line":
            line = frame.f_lineno
            function_name = frame.f_code.co_name

            # Evitamos rastrearnos a nosotros
            if not self.our_frame(frame) and not self.problematic_frame(frame):
                self.executed_lines.append((function_name, line))

        return self.traceit
    
    # We return a sorted list of tuples (function_name, line_number), sorted by line_number, with no duplicates.
    def report_executed_lines(self):
        return sorted(set(self.executed_lines), key=lambda t: t[1], reverse=False)
    
    # We return a sorted list of tuples (function_name, line_number, execution_count), sorted by line_number, with no duplicates.
    def report_execution_count(self):
        result = []
        for fun_name, line in self.executed_lines:
            count = 0
            for fun_name2, line2 in self.executed_lines:
                if fun_name == fun_name2 and line == line2:
                    count += 1
            result.append((fun_name, line, count))
        print(sorted(set(result), key=lambda t: t[1], reverse=False))
        return sorted(set(result), key=lambda t: t[1], reverse=False)
    
    # Esta funcion se llama al comienzo de un bloque 'with' y comienza con el rastreo
    def __enter__(self):
        self.original_trace_function = sys.gettrace()
        sys.settrace(self.traceit)

        return self

    # Esta funcion se llama al final de un bloque 'with' y termina el rastreo.
    # Retorna 'None' si _todo funciona bien y si retorna 'False' significa que hubo un error interno (por nuestra clase Tracer o subclases).
    def __exit__(self, exc_tp, exc_value, exc_traceback: TracebackType):
        sys.settrace(self.original_trace_function)

        # Note que debemos retornar un valor 'False' para indicar que hubo un error interno y levantar las excepciones correspondientes.
        if self.is_internal_error(exc_tp, exc_value, exc_traceback):
            return False
        else:
            # Significa que _todo funciona bien
            return None

