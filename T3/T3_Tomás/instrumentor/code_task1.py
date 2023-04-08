from classInstrumentor import ClassProfiler
from math import hypot

class Point:

    def __init__(self, x, y):
        ClassProfiler.record('method', 'None', '5', 'Point', '__init__')
        self.x = x
        self.y = y

    def distance(self, other):
        ClassProfiler.record('method', 'None', '9', 'Point', 'distance')
        dx = self.x - other.x
        dy = self.y - other.y
        return hypot(dx, dy)

    def __eq__(self, other):
        ClassProfiler.record('method', 'None', '14', 'Point', '__eq__')
        return self.x == other.x and self.y == other.y

    def __str__(self):
        ClassProfiler.record('method', 'None', '17', 'Point', '__str__')
        return 'Point (%s, %s)' % (self.x, self.y)

def test_str():
    ClassProfiler.record('function', 'test_str', 'None', 'None', 'None')
    point = Point(7, 10)
    assert point.__str__() == 'Point (7, 10)', 'Incorrect output'

def test_compare1():
    ClassProfiler.record('function', 'test_compare1', 'None', 'None', 'None')
    point1 = Point(5, 13)
    point2 = Point(19, 72)
    assert point1 != point2, 'Different points'

def test_compare2():
    ClassProfiler.record('function', 'test_compare2', 'None', 'None', 'None')
    point1 = Point(2, 3)
    point2 = Point(5, 3)
    assert point1 != point2, 'Different points'

def test_compare3():
    ClassProfiler.record('function', 'test_compare3', 'None', 'None', 'None')
    point1 = Point(22, 45)
    point2 = Point(22, 27)
    assert point1 != point2, 'Different points'

def test_compare_equal():
    ClassProfiler.record('function', 'test_compare_equal', 'None', 'None', 'None')
    point1 = Point(2, 5)
    point2 = Point(2, 5)
    assert point1 == point2, 'Equal points'
test_str()
test_compare1()