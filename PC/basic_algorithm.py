import decimal
import serial
ardu = serial.Serial(port='COM6', baudrate=9600, timeout=0.1)    # revise port's name for each PC after


# Class indicates specification of the building. Use decimal module to avoid floating point error
# 0th floor is a basement floor
class Building:
        floor_height = decimal.Decimal('2.5')
        lowest_f = 0
        highest_f = 5
        lowest_m = floor_height * (lowest_f - 1)
        highest_m = floor_height * (highest_f - 1)
        whole_floor = highest_f - lowest_f + 1


class Elevator:
    speed = decimal.Decimal('0.1')  # 0.1m/loop

    def __init__(self, id_num, location):  # initialize instance
        self.id_num = id_num
        self.location = location

    def commend(self, motion):
        if motion == 'u':
            if self.location == Building.highest_m:
                raise IndexError("Elevator%d is on the highest floor" % self.id_num)
            self.location += Elevator.speed
        elif motion == 'd':
            if self.location == Building.lowest_m:
                raise IndexError("Elevator%d is on the lowest floor" % self.id_num)
            self.location -= Elevator.speed

    def __str__(self):
        return "Elevator{x} location : {y}m".format(x=self.id_num, y=self.location)


# Global variables
# cc : Car Call      [floor(-1) <- [down, up], floor(1) <- [down, up], ... floor(5) <- [down, up]]
# lc : Landing Call  [ Ele(1) <- [0, 1, 2, 3, 4, 5, open], Ele(2) <- [0, 1, 2, 3, 4, 5, open]]
cc = [[False] * 2 for k in range(Building.whole_floor)]
lc = [[False] * (Building.whole_floor + 1) for i in range(2)]
cc_button_num = len(cc) * 2 - 2  # Except lowest down, highest up


# Function that converts button inputs to the Car Calls and the Landing Calls
# It modifies global variables
def input_to_call():
    check = False
    data = ardu.readline()
    int_data = int.from_bytes(data, "little") - int.from_bytes(b'A\r\n', "little")  # Convert to int starts from 0
    if int_data < 0:
        print("there's a no input")
    else:
        check = True
        if int_data < cc_button_num:
            cc_floor = (int_data + 1) // 2
            cc_direction = (int_data + 1) % 2
            cc[cc_floor][cc_direction] = True
        elif int_data < cc_button_num + Building.whole_floor * 2:
            lc_id = (int_data - cc_button_num) // Building.whole_floor
            lc_floor = (int_data - cc_button_num) % Building.whole_floor
            lc[lc_id][lc_floor] = True
        elif int_data < cc_button_num + Building.whole_floor * 2 + 2:
            open_id = int_data - (cc_button_num + Building.whole_floor * 2)
            lc[open_id][Building.whole_floor] = bool(1 - lc[open_id][Building.whole_floor])
        print("Button Board says (", data, ") which means", int_data, "th button")
    # if elevator completes a work :
        # using whatever such as location or other variable
        # changes global input 
        # check = True
    return check


# Main algorithm that converts the Car Calls and the Landing Calls to the motion of each elevator
# It uses global variables as arguments
def call_to_commend(e1, e2):
    print("Elevator1 location before commend : %f" % e1.location)
    print("Elevator2 location before commend : %f" % e2.location)

    # Need Algorithm

    motion = ['d', 'u']  # example
    return motion


# Make instances and initialize their id and initial position
elevator1 = Elevator(1, 0)
elevator2 = Elevator(2, 0)
commend = ['s', 's']
while True:
    call_change = input_to_call()
    if call_change:
        commend = call_to_commend(elevator1, elevator2)
    elevator1.commend(commend[0])
    elevator2.commend(commend[1])
    # Print with certain format -> sent to GUI algorithm
    print("Car call : ", cc)
    print("Elevator1 Landing call : ", lc[0])
    print("Elevator2 Landing call : ", lc[1])
    print(elevator1)
    print(elevator2)
    print("=======================================")
