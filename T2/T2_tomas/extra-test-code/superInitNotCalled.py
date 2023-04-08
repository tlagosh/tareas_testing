class Pet:

	def __init__(self, name, type):
		self.name = name
		self.type = type
		print("Soy un " + self.type + " y me llamo " + self.name)

class Dog(Pet):

	def __init__(self):
		super(Dog, self).__init__("luca", "perro")

class Cat(Pet):

	def __init__(self):
		print("Soy una gato")
