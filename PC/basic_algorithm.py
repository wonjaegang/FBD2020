import decimal


# Class indicates specification of the building. Use decimal module to avoid floating point error
class Building:
        floor_height = decimal.Decimal('2.5')
        lowest_f = -1
        highest_f = 5
        lowest_m = floor_height * lowest_f
        highest_m = floor_height * highest_f
        whole_floor = abs(lowest_f) + highest_f


class Elevator:
    speed = decimal.Decimal('0.1')  # 0.1m/loop

    def __init__(self, num, location):  # initialize instance
        self.num = num
        self.location = location

    def commend(self, motion):
        if motion == 'u':
            if self.location == Building.highest_m:
                raise IndexError("Elevator%d is on the highest floor" % self.num)
            self.location += Elevator.speed
        elif motion == 'd':
            if self.location == Building.lowest_m:
                raise IndexError("Elevator%d is on the lowest floor" % self.num)
            self.location -= Elevator.speed

    def __str__(self):
        return "Elevator{x} location : {y}m".format(x=self.num, y=self.location)


# Global variables
lc = [[False] * (Building.whole_floor + 1) for i in range(2)]
cc = [[False] * 2 for k in range(Building.whole_floor)]


# Check serial input
def input():
    import serial
    ardu = serial.Serial(port='/dev/ttyUSB0',baudrate=9600)
    # revise port's name for each PC after
    if ardu.readable():
        data = ardu.readline()
        data = data.decode()
    else:
        data = '0'
    return data


# Function that converts button inputs to the Landing Calls and the Car Calls
# It modifies global variables
def input_to_call(button):

    # Need Algorithm

    return 0


# Main algorithm that converts the Landing Calls and the Car Calls to the motion of each elevator
# It uses global variables as arguments
def call_to_commend():

    # Need Algorithm

    motion = ['u', 'd']  # example
    return motion


# Make instances and initialize their id and initial position
elevator1 = Elevator(1, 0)
elevator2 = Elevator(2, 0)
while True:
    # Temporary input. Parsing code will replace it.
    button_input = input()
    if button_input == '0':
        break
    input_to_call(button_input)
    commend = call_to_commend()
    elevator1.commend(commend[0])
    elevator2.commend(commend[1])
    # Print with certain format -> sent to GUI algorithm
    print(elevator1)
    print(elevator2)
