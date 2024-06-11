# Abstract Method Implementation

from abc import ABC, abstractmethod


class Parents(ABC):
    @abstractmethod
    def health_card(self):
        pass
    @abstractmethod
    def kids(self):
        pass

class GrandParents(Parents):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def health_card(self):
        print(f'Age is {self.age} years and need weekly checkup')

    def kids(self):
        print(f'Have 5 kids')


gp = GrandParents("YSR", 60)
print(gp.name)
gp.kids()
gp.health_card()


# Encpasulation
