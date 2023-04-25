from src.clock_factory import *
from src.clock_display import *
from src.display_number import *
from unittest import TestCase

class TestClockFactory(TestCase):
    def test_create(self):
        factory = ClockFactory()
        clock = factory.create("hh:mm")
        self.assertEqual(clock.str(), "00:00")

class TestClockDisplay(TestCase):
    def test_str(self):
        clock = ClockDisplay([24,60])
        self.assertEqual(clock.str(), "00:00")

    def test_increment(self):
        clock = ClockDisplay([24,60])
        clock.increment()
        self.assertEqual(clock.str(), "00:01")
    
    def test_increment2(self):
        clock = ClockDisplay([24,60])
        for i in range(60):
            clock.increment()
        self.assertEqual(clock.str(), "01:00")

    def test_clone(self):
        clock = ClockDisplay([24,60])
        clock.increment()
        clock2 = clock.clone()
        self.assertEqual(clock2.str(), "00:01")

    def test_invariant(self):
        clock = ClockDisplay([24,60])
        self.assertTrue(clock.invariant())
    
class TestNumberDisplay(TestCase):
    def test_str(self):
        number = NumberDisplay(0, 60)
        self.assertEqual(number.str(), "00")

    def test_invariant(self):
        number = NumberDisplay(0, 60)
        self.assertTrue(number.invariant())

    def test_increase(self):
        number = NumberDisplay(0, 60)
        self.assertFalse(number.increase())
        self.assertEqual(number.str(), "01")

    def test_reset(self):
        number = NumberDisplay(0, 60)
        number.increase()
        number.reset()
        self.assertEqual(number.str(), "00")

    def test_clone(self):
        number = NumberDisplay(0, 60)
        number.increase()
        number2 = number.clone()
        self.assertEqual(number2.str(), "01")
    