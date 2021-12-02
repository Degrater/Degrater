import random

class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        #print('Ишак создан')

    def sit(self):
        print(self.name.title + ' сел ')
    
    def jump(self):
        print(self.name.title + ' прыгнул ')
    
    def death(self):
        print(self.name.title + ' Ваш помер ')

    def fight(self):
        print('На вас напали'+ '' +  str(random.randint(2 , 12)) + '' +'живодеров')


angryM = Dog(' Злой  пес Миша' , 18)
chechenM = Dog(' Миша Чеченец ' , 31)
kolM =  Dog(' Сын Колесниковича и Миши' , 7)

print('Cимулятор Миши')
print('1 ' + angryM.name)
print('2 ' + chechenM.name)
print('3 ' + kolM.name)
operation=input('Выберите персонажа:')

if operation == '1':
    print('Вы выбрали' + angryM.name)
    ang=input('продолжайте бегать ...')
    if ang == '1':
        print(angryM.fight())





       