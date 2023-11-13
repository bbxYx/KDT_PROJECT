'''
[숫자 야구 게임]
- 수비(컴퓨터) : 각 자리가 서로 다른 세 자리의 숫자
- 공격(사용자) : 세 자리의 숫자 입력
수비가 정한 다른 세 자리 숫자를 공격이 맞추는 게임입니다.

공격에서 입력한 세 자리 숫자가 수비가 지정한 숫자와 동일 여부를 아래와 같은 형식
으로 제공하여 공격자에게 힌트가 될 수 있도록 합니다.

* 스트라이크 : 숫자와 자리 위치가 일치할 경우
*  볼 : 숫자는 맞지만 자리 위치가 틀린 경우
* 아웃 : 일치하는 숫자가 하나도 없는 경우
------------------------------------------------------------------------------------------------------
[ 예시 ] 
수비 – 827 

공격 – 123   2가 일치하기 때문에 1 스트라이크

공격 – 456	일치하는 숫자가 없기 때문에 아웃

공격 – 789	7과 8이 존재하지만 둘 다 자리가 틀리기 때문에 2볼

공격 – 928	1스트라이크, 1볼

공격자는 수비가 제공하는 출력 정보에 따라 숫자 조합을 찾아가는 게임입니다.
'''



import random

# 수비숫자
initial_number=[]
while len(initial_number)<3:
    number=random.randint(0,9)
    if number not in initial_number:
        initial_number.append(number)
user_number=[]

#게임진행
# 공격숫자
a=0
x=0
while True:
    if x !=0:
        print('종료합니다')
        break
    else:
        user_number=[]
        n=1
        print(f'{a+1}번째 시도')
        while n<=3:
            num=input(f'{n}번째 숫자를 입력해주세요(종료:"q") :' ).strip()
            if num != 'q':
                try : 
                    num=int(num)
                    if num not in range(0,10):
                        print('0~9사이의 숫자를 입력해주세요')
                    elif num in user_number:
                        print(f'중복되는 숫자입니다. {num}이 아닌 다른 숫자를 입력해주세요')
                    else : 
                        user_number.append(num)
                        n+=1
                except : print('0~9사이의 숫자만 입력해주세요.')
                
                # 횟수 확인을 위해서
                if n==3 : a+=1
            else : 
                x=1
                break
                
        # 게임진행
        if x ==0:
            if initial_number == user_number:   
                print(f'정답!! {a}번째 시도에서 성공하셨습니다!')
                re=input('게임을 다시 진행 하시겠습니까?(y/n) : ')
                # 다시 진행 했을 때 이니셜 넘버 재지정
                if re=='y': 
                    a=0
                    initial_number=[]
                    while len(initial_number)<3:
                        number=random.randint(0,9)
                        if number not in initial_number:
                            initial_number.append(number)
                    user_number=[]
                    pass
                elif re=='n': 
                    print('게임을 종료합니다')
                    break
                else : print('y와 n중 하나를 선택해주세요')
            else:
                strike=0
                ball=0
                for n in range(0,3):
                    if user_number[n]==initial_number[n]:strike+=1
                    elif user_number[n] in initial_number: ball+=1
                print(f'{a}번째 공격 = {strike=}, {ball=}')