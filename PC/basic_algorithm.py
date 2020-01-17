import decimal
import time
import copy
import serial
import sys
import pygame

ardu = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=0.1)    # revise port's name for each PC after

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SIZE = 100

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

pygame.init()
pygame.display.set_caption("Pygame Test")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

font = pygame.font.Font('freesansbold.ttf', 30)
text_B1 = font.render("B1", True, white)
text_1 = font.render("1", True, white)
text_2 = font.render("2", True, white)
text_3 = font.render("3", True, white)
text_4 = font.render("4", True, white)
text_5 = font.render("5", True, white)
text_power = font.render("power: ", True, white)
text_time = font.render("waiting time: ", True, white)
text_button = font.render("E1  E2  up  down", True, white)
text_name = font.render("FBD2020 Project", True, white)
text_check = font.render("O", True, red)

def print_background():
    screen.fill(black)
    pygame.draw.line(screen, white, [350, SIZE], [0, SIZE], 3)
    pygame.draw.line(screen, white, [350, 2*SIZE], [0, 2*SIZE], 3)
    pygame.draw.line(screen, white, [350, 3*SIZE], [0, 3*SIZE], 3)
    pygame.draw.line(screen, white, [350, 4*SIZE], [0, 4*SIZE], 3)
    pygame.draw.line(screen, white, [350, 5*SIZE], [0, 5*SIZE], 3)
    pygame.draw.line(screen, white, [350, 6*SIZE], [0, 6*SIZE], 3)
    screen.blit(text_B1, (300, 6*SIZE-30))
    screen.blit(text_1, (300, 5*SIZE-30))
    screen.blit(text_2, (300, 4*SIZE-30))
    screen.blit(text_3, (300, 3*SIZE-30))
    screen.blit(text_4, (300, 2*SIZE-30))
    screen.blit(text_5, (300, SIZE-30))
    screen.blit(text_power, (800, SIZE-30))
    screen.blit(text_time, (800, 2*SIZE-30))
    screen.blit(text_button, (400, 10))
    screen.blit(text_name, (50, 750))


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
    door_operating_time = 10  # loops that elevator should stay at arrived floor

    def __init__(self, id_num, location, v_direction):  # initialize instance
        self.id_num = id_num
        self.location = location
        self.v_direction = v_direction
        self.opening_sequence = 0
        self.destination = [location, "uncalled"]

    def command(self, motion):
        if motion == 'u':
            if self.location == Building.highest_m:
                raise IndexError("Elevator%d is on the highest floor" % self.id_num)
            if self.opening_sequence > 0:
                raise ValueError("Elevator%d tries to moved with its door opened" % self.id_num)
            self.v_direction = 1
        elif motion == 'd':
            if self.location == Building.lowest_m:
                raise IndexError("Elevator%d is on the lowest floor" % self.id_num)
            if self.opening_sequence > 0:
                raise ValueError("Elevator%d tries to moved with its door opened" % self.id_num)
            self.v_direction = -1
        elif motion == 's':
            self.v_direction = 0
        self.location += Elevator.speed * self.v_direction

    def move_to_destination(self, floor, call_type):
        self.destination = [(floor - 1) * Building.floor_height, call_type]  # meter
        if self.location < self.destination[0]:
            self.command('u')
        elif self.location > self.destination[0]:
            self.command('d')
        elif self.destination[1] == "uncalled":
            self.command('s')
        else:
            self.command('s')
            self.door_open()

    def door_open(self):
        self.opening_sequence = Elevator.door_operating_time

    def door_close(self):
        self.opening_sequence -= 1

    def __str__(self):
        return "Elevator{x} Location : {y}m, Direction : {z}, Opening Sequence : {r}, Destination(m) : {a}"\
            .format(x=self.id_num, y=self.location, z=self.v_direction, r=self.opening_sequence, a=self.destination)


# Global variables
# cc : Car Call      [floor(-1) <- [down, up], floor(1) <- [down, up], ... floor(5) <- [down, up]]
# lc : Landing Call  [ Ele(1) <- [0, 1, 2, 3, 4, 5, open], Ele(2) <- [0, 1, 2, 3, 4, 5, open]]
cc = [[False] * 2 for k in range(Building.whole_floor)]
lc = [[False] * (Building.whole_floor + 1) for i in range(2)]
cc_button_num = len(cc) * 2 - 2  # Except lowest down, highest up
cc_before = copy.deepcopy(cc)
lc_before = copy.deepcopy(lc)
# calcute power consumption on watts, and waiting time on wtime
watts=0
wtime=0

# Function that converts button inputs to the Car Calls and the Landing Calls
# It modifies global variables
def input_to_call():
    data = ardu.readline()
    int_data = int.from_bytes(data, "little") - int.from_bytes(b'A\r\n', "little")  # Convert to int starts from 0
    # If input data is None
    if int_data == int.from_bytes(bytes(), "little") - int.from_bytes(b'A\r\n', "little"):
        print("There is no button input")
    # If there is an input data, assign it to Landing Call or Car Call
    # If input data is NOT proper, raise assertion exception
    else:
        assert (0 <= int_data < cc_button_num + Building.whole_floor * 2 + 2),\
            "Input data is NOT proper. Input data(int) : %d" % int_data
        # If input data is Car Call
        if int_data < cc_button_num:
            cc_floor = (int_data + 1) // 2
            cc_direction = (int_data + 1) % 2
            cc[cc_floor][cc_direction] = True
        # If input data is Landing Call : floor
        elif int_data < cc_button_num + Building.whole_floor * 2:
            lc_id = (int_data - cc_button_num) // Building.whole_floor
            lc_floor = (int_data - cc_button_num) % Building.whole_floor
            lc[lc_id][lc_floor] = True
        # If input data is Landing Call : door open
        else:
            open_id = int_data - (cc_button_num + Building.whole_floor * 2)
            lc[open_id][Building.whole_floor] = bool(1 - lc[open_id][Building.whole_floor])
        print("Button Board says (", data, ") which means %dth button" % int_data)
    return 0


# Main algorithm that converts the Car Calls and the Landing Calls to the destination of each elevator
# It uses global variables as arguments
def call_to_command(e1, e2):
    print("Elevator1 location before command : %f" % e1.location)
    print("Elevator2 location before command : %f" % e2.location)

    # Need Algorithm

    # MUST change call_type to "uncalled" after arrived
    destination_call = [[2, "cc+"], [5, "lc"]]  # example
    return destination_call


# Turn off calls if elevator arrived
def update_call(e1, e2):
    print(e1.location, e2.location)


# Make instances and initialize their id and initial position
elevator1 = Elevator(1, 0, 0)
elevator2 = Elevator(2, 0, 0)
command = [[elevator1.location / Building.floor_height + 1, 0], [elevator2.location / Building.floor_height + 1, 0]]
while True:
    input_to_call()
    if not(cc_before == cc and lc_before == lc):
        command = call_to_command(elevator1, elevator2)
    cc_before = copy.deepcopy(cc)
    lc_before = copy.deepcopy(lc)
    # Codes that actually operate elevators
    print(command[0][0], command[1][0])
    elevator1.move_to_destination(command[0][0], command[0][1])
    elevator2.move_to_destination(command[1][0], command[1][1])
    if elevator1.opening_sequence > 0:
        elevator1.door_close()
    if elevator2.opening_sequence > 0:
        elevator2.door_close()
    update_call(elevator1, elevator2)

    # GUI code
    print_background()
    watts_str=str(watts)
    text_watts = font.render(watts_str, True, white)
    time_str=str(wtime)
    text_wtime = font.render(time_str, True, white)
    screen.blit(text_watts, (950, SIZE-30))
    screen.blit(text_wtime, (1050, 2*SIZE-30))
    pygame.draw.rect(screen, red, [50, 400 - elevator1.location * 40, 40, SIZE], 5)
    pygame.draw.rect(screen, red, [150, 400 - elevator2.location * 40, 40, SIZE], 5)
    for i in range(len(lc)):
        for j in range(len(lc[i])):
            if lc[i][j]==True:
                 screen.blit(text_check, (400 + i*57, 600 - j*SIZE-40))
    for i in range(len(cc)):
        for j in range(len(cc[i])):
            if cc[i][j]==True:
                 screen.blit(text_check, (514 + j*57, 600 - i*SIZE-40))
    pygame.display.update()

