print('Выход - 0')
print('Определение типа числа - 1')
print('Расчеты - 2')
print('Сопромат - 3')
print('Коэффициенты и т.д. - 4')
operation1=input('Введите необходимую операцию : ')
if operation1 == '2':
    print('Сложение - 1')
    print('Вычисление - 2')
    print('Возведение в квадрат - 3')
    print ('Умножение - 4')
    oper1=input('Выберите операцию : ')
    if oper1 == ('1'):
        sum=input('Введите первое число : ')
        sum1=input('Введите второе число : ')
        sum3 = sum + sum1
        print(sum3)
    if oper1 == ('2'):
        vich=int(input('Введите первое число : '))
        vich1=int(input('Введите второе число : '))
        vich2 = vich - vich1
        print(vich2)    
    if oper1 == ('4'):
        umn=int(input('Введите первое число : '))
        umn1=int(input('Введите второе число : '))
        umn2 = umn * umn1
        print(umn2)
    if oper1 == ('3'):
        step=int(input('Введите первое число : '))
        step1=int(input('Введите второе число : '))
        step2 = step ** step1
        print(step2)            
if operation1 == '1':
    numbet=input('Введите число : ')
    if numbet <= ('99999999999'):
        print('Натуральное число')