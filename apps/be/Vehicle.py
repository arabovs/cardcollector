class Vehicle():

    def __init__(self, model="hey", year=200):
        self.model = model
        self.year = year
    def __str__(self):
        return "hey"

v = Vehicle("Mazda","1995")

print(str(v))
