class Dog:

    def __init__(self, firstName, intelligence):
        self.name = firstName
        self.intelligenceQuotient = intelligence
        self.hasFoodUntilTomorrow = False

dog = Dog('Luca', 100)
isDogIntelligent = dog.intelligenceQuotient

