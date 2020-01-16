# should download pyserial
# example code for kmkim
# 시리얼 입력 받은 데이터를 출력하는 코드
import serial
from time import sleep
num = 1
# revise port's name for each PC after
ardu = serial.Serial(port='/dev/ttyUSB0', baudrate=9600)

# ardu = serial.Serial(port='/dev/ttyUSB0',baudrate=9600)
# port의 ttyUSB0은 연결된 시리얼 포트의 이름으로 수정할 것
# baudrate는 9600 고정


def input_to_call():
    check = False
    data = ardu.readline()
    print(data)
    if data == b'A\r\n':
        print('A')
        check = True
    elif data == b'B\r\n':
        print('B')
        check = True
    elif data == b'W\r\n':
        print('W')
        check = True
    return check


while True:
    print(num)
    num = num+1
    call_change = input_to_call()
    if call_change:
        print("hi")
    sleep(0.1)
