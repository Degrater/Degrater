import math
print('ДЕЙСТВИЯ :')
print('косинус числа - cos')
print('синус числа - sin')
print('тангенс числа - tan')
print('вывод из корня - корень')
a1=input('Выберите действие:')
if a1 == "cos":
    cus=float(input('Введите число : '))
    cus1= math.cos (cus)
    print(cus1)
else:
 if a1 == "sin":
  ui=float(input("Введите число : "))
  ui1 = math.sin (ui)
  print(ui1)
 if a1 =="корень":
  kor=float(input('Введите число : '))
  kor1 = math.sqrt (kor)
  print(kor1)
 if a1 == "tan":
  tg=float(input('Введите число : '))
  tg1 = math.tan (tg)
  print(tg1)
