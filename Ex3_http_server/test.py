

class Animal:

    animals_count = 0
    def __init__(self, name):
        print('New Animal')
        Animal.animals_count += 1
        self.name = name
    
    def talk(self):
        raise NotImplementedError("Generic animal can not talk")
    

class Dog(Animal):

    talk_count = 0

    def __init__(self, name, breed):
        super().__init__(name)
        self.breed = breed
    
    def talk(self):
        Dog.talk_count += 1
        print(f' {self.name}  count={Dog.talk_count} : Woof')

    def walk():
        print(f'Walking!! so far I know {Dog.talk_count} dogs talked')


class Cat(Animal):
    def __init__(self, name, color):
        super().__init__(name)
        self.color = color
    
    def talk(self):
        print('Meow')


a = Animal('A')
dog = Dog('clint', 'belguim')
dog2 = Dog('joey', 'good')
cat = Cat('Mizi', 'gray')


dog.talk()
dog2.talk()
cat.talk()

print(f'Animals count = {Animal.animals_count}')

Dog.walk()