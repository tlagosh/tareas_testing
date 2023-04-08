from classInstrumentor import ClassProfiler

class Rectangle:

    def __init__(self, width, height):
        ClassProfiler.record('method', 'None', '3', 'Rectangle', '__init__')
        self.width = width
        self.height = height

    def get_area(self):
        ClassProfiler.record('method', 'None', '7', 'Rectangle', 'get_area')
        return self.width * self.height

    def get_perimeter(self):
        ClassProfiler.record('method', 'None', '10', 'Rectangle', 'get_perimeter')
        return self.width * 2 + self.height * 2

    def set_width(self, width):
        ClassProfiler.record('method', 'None', '13', 'Rectangle', 'set_width')
        self.width = width

    def set_height(self, height):
        ClassProfiler.record('method', 'None', '16', 'Rectangle', 'set_height')
        self.height = height

    def __eq__(self, other):
        ClassProfiler.record('method', 'None', '19', 'Rectangle', '__eq__')
        return self.width == other.width and self.height == other.height

def test_area():
    ClassProfiler.record('function', 'test_area', 'None', 'None', 'None')
    rectangle = Rectangle(2, 3)
    assert rectangle.get_area() == 6, 'Incorrect area'

def test_perimeter():
    ClassProfiler.record('function', 'test_perimeter', 'None', 'None', 'None')
    rectangle = Rectangle(5, 7)
    assert rectangle.get_perimeter() == 24, 'Incorrect perimeter'

def test_compare1():
    ClassProfiler.record('function', 'test_compare1', 'None', 'None', 'None')
    rectangle1 = Rectangle(2, 3)
    rectangle2 = Rectangle(5, 7)
    assert rectangle1 != rectangle2, 'Different rectangles'

def test_compare2():
    ClassProfiler.record('function', 'test_compare2', 'None', 'None', 'None')
    rectangle1 = Rectangle(2, 3)
    rectangle2 = Rectangle(5, 3)
    assert rectangle1 != rectangle2, 'Different rectangles'

def test_compare3():
    ClassProfiler.record('function', 'test_compare3', 'None', 'None', 'None')
    rectangle1 = Rectangle(2, 5)
    rectangle2 = Rectangle(2, 7)
    assert rectangle1 != rectangle2, 'Different rectangles'

def test_compare_equal():
    ClassProfiler.record('function', 'test_compare_equal', 'None', 'None', 'None')
    rectangle1 = Rectangle(2, 5)
    rectangle2 = Rectangle(2, 5)
    assert rectangle1 == rectangle2, 'Equal rectangles'
test_area()
test_perimeter()
test_compare1()
test_compare2()
test_compare3()
test_compare_equal()