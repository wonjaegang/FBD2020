# should download pyserial
# 해당 파일은 참고용
# 시리얼 입력 받은 데이터를 출력하는 코드
import serial
ardu = serial.Serial(port='/dev/ttyUSB0',baudrate=9600)
# port의 ttyUSB0은 연결된 시리얼 포트의 이름으로 수정할 것
# baudrate는 9600 고정
while True:
    data = ardu.readline()
    data = data.decode()
    print(data)
