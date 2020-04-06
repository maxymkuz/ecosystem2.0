from random import random


class Animal:
    """
    Represents an animal
    """
    def __init__(self, name):
        self.name = name
        self.male = True if random() > 0.5 else False
        self.power = 10 * random()
        self.age = 0

    def __str__(self):
        return f"{self.name}{round(self.power, 2)}" \
               f"{'ч' if self.male else 'ж'}{self.age} "

    def __repr__(self):
        return self.name


class Bear(Animal):
    def __init__(self):
        super().__init__('B')


class Fish(Animal):
    def __init__(self):
        super().__init__('F')


class Otter(Animal):
    def __init__(self):
        super().__init__('O')
