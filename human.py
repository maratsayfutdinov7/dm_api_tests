class Human:
    def __init__(self, name, sex, years, height, weight ):
        self.name = name
        self.sex = sex
        self.years = years
        self.height = height
        self.weight = weight

    def walk(self):
        print(f'{self.name} walk!')

julia = Human(name = 'Julia', sex = 'female', years = 23, height = 165, weight = 65)

print(julia.sex)