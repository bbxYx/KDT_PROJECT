def plus(num1,num2):
    return num1+num2
def minus(num1,num2):
    return num1-num2
def multi(num1,num2):
    return num1*num2
def divide(num1, num2):
    return num1/num2
def guide(fp):
        print('''------<사칙연산계산기 프로그램>------
           -기호 가이드-
덧셈(+), 뺄셈(-), 곱셈(*), 나눗셈(/)
           -연산 가이드-
0으로 나눈 경우 연산자를 다시 확인합니다.
숫자를 잘못 입력한 경우 숫자를 다시 확인합니다.
              
              ''')
        print('''------<사칙연산계산기 프로그램>------
           -기호 가이드-
덧셈(+), 뺄셈(-), 곱셈(*), 나눗셈(/)
           -연산 가이드-
0으로 나눈 경우 연산자를 다시 확인합니다.
숫자를 잘못 입력한 경우 숫자를 다시 확인합니다.
              
              ''',file=fp)



def four_calculation(fp):
    pre_num=0
    a=1
    while a!=0:
        try:
            number_initial=float(input('숫자 : ').strip())
            a=0
        except ValueError :
            a=1
            print('숫자만 입력하세요.')
            print(f'숫자만 입력하세요.\n',file=fp)
            

    sign = input('원하는 연산자의 기호를 입력하세요(q입력시 종료) : ')
    if sign== 'q': 
        print('계산이 종료됩니다')
        print('계산이 종료됩니다\n',file=fp)
    else:
        if sign in ('+', '-', '*', '/'):
            b=1
            while b!=0:
                try:
                    number1_1=input('숫자 : ')
                    number1=float(number1_1.strip())
                    b=0
                except ValueError :
                    b=1
                    print('숫자만 입력하세요.')
                    print(f'입력값 : {number1_1}, 숫자만 입력하세요. \n',file=fp)
                
            try:
                if sign=='+': 
                    print(f'{number_initial}+{number1}={plus(number_initial, number1)}')
                    print(f'{number_initial}+{number1}={plus(number_initial, number1)}\n',file=fp)
                    pre_num+=plus(number_initial, number1)
                elif sign=='-': 
                    print(f'{number_initial}-{number1}={minus(number_initial, number1)}')
                    print(f'{number_initial}-{number1}={minus(number_initial, number1)}\n',file=fp)
                    pre_num+=minus(number_initial, number1)
                elif sign=='*': 
                    print(f'{number_initial}*{number1}={multi(number_initial, number1)}')
                    print(f'{number_initial}*{number1}={multi(number_initial, number1)}\n',file=fp)
                    pre_num+=multi(number_initial, number1)
                elif sign=='/': 
                    print(f'{number_initial}/{number1}={divide(number_initial, number1)}')
                    print(f'{number_initial}/{number1}={divide(number_initial, number1)}\n',file=fp)
                    pre_num+=divide(number_initial, number1)
            except ZeroDivisionError :
                print('숫자가 0인 경우 나눗셈을 할 수 없습니다.')
                print()
                print(f'입력된 식 : {number_initial}/{number1}\n숫자가 0인 경우 나눗셈을 할 수 없습니다.\n0이 아닌 다를 숫자 혹은 나눗셈이 아닌 다른 연산을 입력해주세요\n',file=fp)
        else : 
            print('연산자가 잘못 입력되었습니다.')
            print(f'입력한 연산자 : {sign}\n, 연산자가 잘못 입력되었습니다.',file=fp)
            pass


        while True :
            cont_calc=input('원하는 연산자의 기호를 입력하세요(q입력시 종료, g입력시 guide) : ')
            if cont_calc in 'q': 
                print('계산이 종료됩니다')
                print('계산이 종료됩니다\n',file=fp)
                break
            if cont_calc=='g':
                guide(fp)
                continue
            else : 
                if cont_calc in ('+', '-', '*', '/'):
                    c=1
                    while c !=0:
                        try:
                            number_1=input('숫자 : ')
                            number=float(number_1.strip())
                            c=0
                        except ValueError :
                            c=1
                            print('숫자만 입력하세요.')
                            print(f'입력값 : {number_1}, 숫자만 입력하세요.\n',file=fp)

                    try:
                        if cont_calc=='+': 
                            print(f'{pre_num}+{number}={plus(pre_num, number)}')
                            print(f'{pre_num}+{number}={plus(pre_num, number)}\n',file=fp)
                            pre_num+=number
                        elif cont_calc=='-': 
                            print(f'{pre_num}-{number}={minus(pre_num, number)}')
                            print(f'{pre_num}-{number}={minus(pre_num, number)}\n',file=fp)
                            pre_num-=number
                        elif cont_calc=='*': 
                            print(f'{pre_num}*{number}={multi(pre_num, number)}')
                            print(f'{pre_num}*{number}={multi(pre_num, number)}\n',file=fp)
                            pre_num*=number
                        elif cont_calc=='/': 
                            print(f'{pre_num}/{number}={divide(pre_num, number)}')
                            print(f'{pre_num}/{number}={divide(pre_num, number)}\n',file=fp)
                            pre_num/=number
                    except ZeroDivisionError :
                        print('숫자가 0인 경우 나눗셈을 할 수 없습니다.')
                        print(f'입력된 식 : {pre_num}/{number}\n숫자가 0인 경우 나눗셈을 할 수 없습니다.\n0이 아닌 다를 숫자 혹은 나눗셈이 아닌 다른 연산을 입력해주세요\n',file=fp)
                        continue

                else : 
                    print('연산자의 기호를 확인 후 다시 입력하세요')
                    print(f'입력된 연산자 : {cont_calc}, 연산자의 기호를 확인 후 다시 입력하세요.\n',file=fp)

filename='four_calcul.txt'
fp=open(filename, mode='w',encoding='utf-8')
guide(fp)
four_calculation(fp)
fp.close()