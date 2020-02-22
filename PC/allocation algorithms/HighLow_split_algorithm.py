import decimal
import serial
import sys
import pygame
import time
import math

# revise port's name for each PC after
ardu = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=0.1)

# define variables for GUI screen
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SIZE = 100

# color data (R,G,B)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
grey = (128, 128, 128)
yellow = (255, 204, 0)

# starts GUI screen
pygame.init()
pygame.display.set_caption("FBD:: Elevator Simulation")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# save the fonts and tests for GUI screen
font = pygame.font.Font('freesansbold.ttf', 30)
text_B1 = font.render("B1", True, black)
text_1 = font.render("1", True, black)
text_2 = font.render("2", True, black)
text_3 = font.render("3", True, black)
text_4 = font.render("4", True, black)
text_5 = font.render("5", True, black)
text_power = font.render("power:                     kWh", True, black)
text_time = font.render("waiting time:                 sec", True, black)
text_loop_count = font.render("loop count:                    sec", True, black)
text_button = font.render("E1  E2  down  up", True, black)
text_name = font.render("FBD2020 Project", True, black)


# function for drawing background
def print_background():
    screen.fill(white)
    pygame.draw.line(screen, black, [350, SIZE], [0, SIZE], 3)
    pygame.draw.line(screen, black, [350, 2 * SIZE], [0, 2 * SIZE], 3)
    pygame.draw.line(screen, black, [350, 3 * SIZE], [0, 3 * SIZE], 3)
    pygame.draw.line(screen, black, [350, 4 * SIZE], [0, 4 * SIZE], 3)
    pygame.draw.line(screen, black, [350, 5 * SIZE], [0, 5 * SIZE], 3)
    pygame.draw.line(screen, black, [350, 6 * SIZE], [0, 6 * SIZE], 3)
    screen.blit(text_B1, (300, 6 * SIZE - 30))
    screen.blit(text_1, (300, 5 * SIZE - 30))
    screen.blit(text_2, (300, 4 * SIZE - 30))
    screen.blit(text_3, (300, 3 * SIZE - 30))
    screen.blit(text_4, (300, 2 * SIZE - 30))
    screen.blit(text_5, (300, SIZE - 30))
    screen.blit(text_power, (800, SIZE - 30))
    screen.blit(text_time, (800, 2 * SIZE - 30))
    screen.blit(text_loop_count, (800, 3 * SIZE - 30))
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
    door_operating_time = 20  # loops that elevator should stay at arrived floor

    def __init__(self, id_num, floor):  # initialize instance
        self.id_num = id_num
        self.location = Building.floor_height * (floor - 1)
        self.v_direction = 0
        self.prev_destination = 0
        self.opening_sequence = 0
        self.destination_floor = floor
        self.destination = [self.location, "uncalled"]
        self.call_done = False

    def command(self, motion):
        if motion == 'u':
            if self.location == Building.highest_m:
                raise IndexError(
                    "Elevator%d is on the highest floor" % self.id_num)
            if self.opening_sequence > 0:
                raise ValueError(
                    "Elevator%d tries to moved with its door opened" % self.id_num)
            self.v_direction = 1
        elif motion == 'd':
            if self.location == Building.lowest_m:
                raise IndexError(
                    "Elevator%d is on the lowest floor" % self.id_num)
            if self.opening_sequence > 0:
                raise ValueError(
                    "Elevator%d tries to moved with its door opened" % self.id_num)
            self.v_direction = -1
        elif motion == 's':
            self.v_direction = 0
        self.location += Elevator.speed * self.v_direction

    def move_to_destination(self, floor, call_type):
        self.destination_floor = floor
        self.destination = [
            (floor - 1) * Building.floor_height, call_type]  # meter
        if self.location < self.destination[0]:
            self.command('u')
        elif self.location > self.destination[0]:
            self.command('d')
        elif self.destination[1] == "uncalled":
            self.command('s')
        # when elevator arrived
        else:
            self.prev_destination = self.v_direction
            self.command('s')
            self.door_open()
            self.call_done = True

    def door_open(self):
        self.opening_sequence = Elevator.door_operating_time

    def door_close(self):
        self.opening_sequence -= 1

    def __str__(self):
        return "Elevator{x} Location : {y}m, Direction : {z}, Opening Sequence : {r}, Destination(m) : {a}" \
            .format(x=self.id_num, y=self.location, z=self.v_direction, r=self.opening_sequence, a=self.destination)


# Global variables
# cc : Car Call      [floor(-1) <- [down, up], floor(1) <- [down, up], ... floor(5) <- [down, up]]
# lc : Landing Call  [ Ele(1) <- [0, 1, 2, 3, 4, 5, open], Ele(2) <- [0, 1, 2, 3, 4, 5, open]]
cc = [[False] * 2 for k in range(Building.whole_floor)]
lc = [[False] * (Building.whole_floor + 1) for i in range(2)]
cc_2 = [False, False, False, False]
cc_button_num = len(cc) * 2 - 2  # Except lowest down, highest up
run_main_algorithm = False
# calculate power consumption on watts, and waiting time on wtime
watts = 0
wtime = 0
count = 0
moved_distance = [[0, 0], [0, 0]]


# Function that converts button inputs to the Car Calls and the Landing Calls
# It modifies global variables
def input_to_call():

    data = ardu.readline()
    if data == b'\x00\r\n':
        data = b''

    # Convert to int starts from 0
    int_data = int.from_bytes(data, "little") - \
        int.from_bytes(b'A\r\n', "little")
    # If input data is None
    if int_data == int.from_bytes(bytes(), "little") - int.from_bytes(b'A\r\n', "little"):
        print("There is no button input")
    # If there is an input data, assign it to Landing Call or Car Call
    # If input data is NOT proper, raise assertion exception
    else:
        assert (0 <= int_data < 40), \
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
        elif int_data < 30:
            open_id = int_data - (cc_button_num + Building.whole_floor * 2)
            lc[open_id][Building.whole_floor] = bool(
                1 - lc[open_id][Building.whole_floor])
        else:
            cc_2[int_data-32]=True
        cc[0][1] = cc_2[0] or cc_2[1]
        cc[1][1] = cc_2[2] or cc_2[3]
        global run_main_algorithm
        run_main_algorithm = True
        print("Button Board says (", data, ") which means %dth button" % int_data)
    return 0


# Main algorithm that converts the Car Calls and the Landing Calls to the destination of each elevator
# It uses global variables as arguments
def call_to_command(e1, e2):
    print("Elevator1 location before command : %f" % e1.location)
    print("Elevator2 location before command : %f" % e2.location)
    # # # # # # # # # # # # # # # # # # # # # # # #
    # TO-DO LIST
    # # # # # # # # # # # # # # # # # # # # # # # #
    # MUST change call_type to "uncalled" after arrived

    calls = [[], []]
    e2_prev_dest = [e2.destination_floor, e2.destination[1]]

    for floor in range(Building.whole_floor):
        for call_type in range(2):
            if cc[floor][call_type]:
                if floor > 3:
                    calls[0].append([floor, "cc" + str(call_type)])
                elif floor > 1:
                    calls[1].append([floor, "cc" + str(call_type)])
                else:
                    if str(call_type) == '0':
                        calls[0].append([floor, "cc" + str(call_type)])
                        calls[1].append([floor, "cc" + str(call_type)])
                    else:
                        for i in range(4):
                            if cc_2[i]:
                                calls[i%2].append([floor, "cc1"])

    for id_num in range(2):
        for floor in range(Building.whole_floor):
            if lc[id_num][floor]:
                if id_num == 0:
                    if floor < 2 or floor > 3:
                        calls[id_num].append([floor, "lc"])
                    else:
                        lc[id_num][floor] = False
                else:
                    if floor < 4:
                        calls[id_num].append([floor, "lc"])
                    else:
                        lc[id_num][floor] = False

    if e1.destination[1] == e2.destination[1] == "uncalled":
        if len(calls[0]) == len(calls[1]) == 1:
            if calls[0][0][1][:2] == "cc":
                if calls[0] == calls[1]:
                    distance1 = abs(
                        e1.location / decimal.Decimal(2.5) + 1 - calls[0][0][0])
                    distance2 = abs(
                        e2.location / decimal.Decimal(2.5) + 1 - calls[0][0][0])
                    if (distance2 - distance1) > 0:
                        e1_destination_call = calls[0][0]
                        e2_destination_call = [
                            e2.destination_floor, "uncalled"]
                    else:
                        e2_destination_call = calls[1][0]
                        e1_destination_call = [
                            e1.destination_floor, "uncalled"]
                    destination_call = [e1_destination_call,
                                        e2_destination_call]  # example
                    print(destination_call)
                    return destination_call

    if e2.destination_floor < 2:
        if e2.destination[1] == "cc0":
            if calls[0].count(e2_prev_dest):
                calls[0].remove(e2_prev_dest)

    if len(calls[0]) == 0:
        e1_destination_call = [e1.destination_floor, "uncalled"]
    else:
        if e1.opening_sequence > 0:
            e1_destination_call = [e1.destination_floor, "uncalled"]
        else:
            if e1.v_direction == 0:
                if e1.prev_destination == 0:
                    e1_destination_call = calls[0][0]
                    check_d = 0
                else:
                    cur_floor = e1.location / decimal.Decimal(2.5)
                    if e1.prev_destination == 1:
                        check_d = -1
                        for i in range(len(calls[0])):
                            if(calls[0][i][0] > cur_floor):
                                check_d = 1
                    elif e1.prev_destination == -1:
                        check_d = 1
                        for i in range(len(calls[0])):
                            if(calls[0][i][0] < cur_floor):
                                check_d = -1
            elif e1.v_direction == 1:
                check_d = 1
            else:
                check_d = -1
            if check_d == 1:
                cur_floor = math.trunc(e1.location / decimal.Decimal(2.5))
                check = 1
                for index in range(5, cur_floor, -1):
                    if(calls[0].count([index, "lc"])):
                        e1_destination_call = [index, "lc"]
                        check = 0
                    if(calls[0].count([index, "cc1"])):
                        e1_destination_call = [index, "cc1"]
                        check = 0
                if check:
                    for index in range(cur_floor+1, 6):
                        if(calls[0].count([index, "cc0"])):
                            e1_destination_call = [index, "cc0"]
            elif check_d == -1:
                cur_floor = math.trunc(e1.location / decimal.Decimal(2.5)) + 1
                check = 1
                for index in range(cur_floor+1):
                    if(calls[0].count([index, "lc"])):
                        e1_destination_call = [index, "lc"]
                        check = 0
                    if(calls[0].count([index, "cc0"])):
                        e1_destination_call = [index, "cc0"]
                        check = 0
                if check:
                    for index in range(cur_floor, -1, -1):
                        if(calls[0].count([index, "cc1"])):
                            e1_destination_call = [index, "cc1"]

    if e1_destination_call[0] < 2:
        if e1_destination_call[1] == "cc0":
            if calls[1].count(e1_destination_call):
                calls[1].remove(e1_destination_call)

    if len(calls[1]) == 0:
        e2_destination_call = [e2.destination_floor, "uncalled"]
    else:
        if e2.opening_sequence > 0:
            e2_destination_call = [e2.destination_floor, "uncalled"]
        else:
            if e2.v_direction == 0:
                if e2.prev_destination == 0:
                    e2_destination_call = calls[1][0]
                    check_d = 0
                else:
                    cur_floor = e2.location / decimal.Decimal(2.5)
                    if e2.prev_destination == 1:
                        check_d = -1
                        for i in range(len(calls[1])):
                            if(calls[1][i][0] > cur_floor):
                                check_d = 1
                    elif e2.prev_destination == -1:
                        check_d = 1
                        for i in range(len(calls[1])):
                            if(calls[1][i][0] < cur_floor):
                                check_d = -1
            elif e2.v_direction == 1:
                check_d = 1
            else:
                check_d = -1
            if check_d == 1:
                cur_floor = math.trunc(e2.location / decimal.Decimal(2.5))
                check = 1
                for index in range(5, cur_floor, -1):
                    if(calls[1].count([index, "lc"])):
                        e2_destination_call = [index, "lc"]
                        check = 0
                    if(calls[1].count([index, "cc1"])):
                        e2_destination_call = [index, "cc1"]
                        check = 0
                if check:
                    for index in range(cur_floor+1, 6):
                        if(calls[1].count([index, "cc0"])):
                            e2_destination_call = [index, "cc0"]
            elif check_d == -1:
                cur_floor = math.trunc(e2.location / decimal.Decimal(2.5)) + 1
                check = 1
                for index in range(cur_floor+1):
                    if(calls[1].count([index, "lc"])):
                        e2_destination_call = [index, "lc"]
                        check = 0
                    if(calls[1].count([index, "cc0"])):
                        e2_destination_call = [index, "cc0"]
                        check = 0
                if check:
                    for index in range(cur_floor, -1, -1):
                        if(calls[1].count([index, "cc1"])):
                            e2_destination_call = [index, "cc1"]

    destination_call = [e1_destination_call, e2_destination_call]  # example
    print(destination_call)
    return destination_call


# Turn off calls if elevator arrived
def update_call(e):
    if e.call_done:
        if e.prev_destination == 1:
            if e.destination[1] == "cc1":
                if cc[e.destination_floor][int(e.destination[1][2])]:
                    cc[e.destination_floor][int(e.destination[1][2])] = False
                if lc[e.id_num - 1][e.destination_floor]:
                    lc[e.id_num-1][e.destination_floor] = False
            elif e.destination[1] == "lc":
                if lc[e.id_num - 1][e.destination_floor]:
                    lc[e.id_num-1][e.destination_floor] = False
                check = True
                for index in range(e.destination_floor + 1, 6):
                    if cc[index][0] or cc[index][1]:
                        check = False
                    if lc[e.id_num-1][index]:
                        check = False
                if check:
                    cc[e.destination_floor][0] = False
            elif e.destination[1] == "cc0":
                if cc[e.destination_floor][int(e.destination[1][2])]:
                    cc[e.destination_floor][int(e.destination[1][2])] = False
        elif e.prev_destination == -1:
            if e.destination[1] == "cc0":
                if cc[e.destination_floor][int(e.destination[1][2])]:
                    cc[e.destination_floor][int(e.destination[1][2])] = False
                if lc[e.id_num - 1][e.destination_floor]:
                    lc[e.id_num-1][e.destination_floor] = False
            elif e.destination[1] == "lc":
                if lc[e.id_num - 1][e.destination_floor]:
                    lc[e.id_num-1][e.destination_floor] = False
                check = False
                for index in range(e.destination_floor, -1, -1):
                    print(index)
                    if cc[index][0] or cc[index][1]:
                        check = True
                    if lc[e.id_num-1][index]:
                        check = True
                    if check:
                        cc[e.destination_floor][1] = False
            elif e.destination[1] == "cc1":
                if cc[e.destination_floor][int(e.destination[1][2])]:
                    cc[e.destination_floor][int(e.destination[1][2])] = False
        else:
            if e.destination[1][:2] == "cc":
                if cc[e.destination_floor][int(e.destination[1][2])]:
                    cc[e.destination_floor][int(e.destination[1][2])] = False
                else:
                    raise ValueError("Elevator%d arrived at %dth floor with vain call : " % (e.id_num, e.destination[0]),
                                     e.destination)
            elif e.destination[1][:2] == "lc":
                if lc[e.id_num - 1][e.destination_floor]:
                    lc[e.id_num - 1][e.destination_floor] = False
                else:
                    raise ValueError("Elevator%d arrived at %dth floor with vain call : " % (e.id_num, e.destination[0]),
                                     e.destination)
    global run_main_algorithm
    run_main_algorithm = True
    e.call_done = False


# Calculate evaluation factors : waiting time, power consumption
def update_evaluation_factor(e1, e2):
    cc_true_num = 0
    lc_true_num = [0, 0]
    for i in range(len(cc)):  # cc true
        for j in range(len(cc[i])):
            if cc[i][j]:
                cc_true_num += 1
    for i in range(len(lc)):  # lc true
        for j in range(len(lc[i])):
            if lc[i][j]:
                lc_true_num[i] += 1
    # Calculate waiting time
    wtime_per_loop = (cc_true_num + lc_true_num[0] + lc_true_num[1]) * 0.1
    # Calculate power consumption
    loop_time = decimal.Decimal(0.1)
    operating_power = 2
    e_direction = [e1.v_direction, e2.v_direction]
    power_per_loop = [0, 0]
    for i in range(2):
        ps_weight = lc_true_num[i] * 70
        power_constant = decimal.Decimal(15.5) * (1 - e_direction[i]) / 2 \
            + (decimal.Decimal((28 + 8) / 1350) * ps_weight - 8) * e1.v_direction
        if moved_distance[i][0]:
            if not moved_distance[i][1]:
                power_per_loop[i] = (Building.floor_height / Elevator.speed) * power_constant * loop_time
            elif moved_distance[i][1] > Building.floor_height:
                power_per_loop[i] = power_constant * loop_time
            else:
                power_per_loop[i] = operating_power * loop_time
        else:
            power_per_loop[i] = operating_power * loop_time
    return [wtime_per_loop, power_per_loop[0] + power_per_loop[1]]


# Make instances and initialize their id and initial position
# Elevator(id_num, floor)
elevator1 = Elevator(1, 1)
elevator2 = Elevator(2, 1)
command = [[elevator1.location / Building.floor_height + 1, "uncalled"],
           [elevator2.location / Building.floor_height + 1, "uncalled"]]
while True:
    input_to_call()
    if run_main_algorithm:
        command = call_to_command(elevator1, elevator2)
    run_main_algorithm = False
    # If elevator arrived, run main algorithm at next loop
    if elevator1.opening_sequence == 1:
        run_main_algorithm = True
    if elevator2.opening_sequence == 1:
        run_main_algorithm = True

    # Codes that actually operate the elevators
    # Close the door if it is opened.
    if elevator1.opening_sequence > 0:
        elevator1.door_close()
    if elevator2.opening_sequence > 0:
        elevator2.door_close()

    if lc[0][6]:
        elevator1.door_open()
    if lc[1][6]:
        elevator2.door_open()

    elevator1.move_to_destination(command[0][0], command[0][1])
    elevator2.move_to_destination(command[1][0], command[1][1])
    update_call(elevator1)

    if cc[0][1] == False:
        cc_2[0] = False
    if cc[1][1] == False:
        cc_2[2] = False
 
    cc[0][1] = cc_2[0] or cc_2[1]
    cc[1][1] = cc_2[2] or cc_2[3]
 
    update_call(elevator2)
    if cc[0][1] == False:
        cc_2[1] = False
    if cc[1][1] == False:
        cc_2[3] = False
 
    cc[0][1] = cc_2[0] or cc_2[1]
    cc[1][1] = cc_2[2] or cc_2[3]
    
    # Update evaluation factors : waiting time, power consumption
    if elevator1.v_direction == moved_distance[0][0]:
        moved_distance[0][1] += Elevator.speed
    else:
        moved_distance[0][0] = elevator1.v_direction
        moved_distance[0][1] = 0
    if elevator2.v_direction == moved_distance[1][0]:
        moved_distance[1][1] += Elevator.speed
    else:
        moved_distance[1][0] = elevator2.v_direction
        moved_distance[1][1] = Elevator.speed
    wtime = wtime + update_evaluation_factor(elevator1, elevator2)[0]
    watts = watts + update_evaluation_factor(elevator1, elevator2)[1]

    print(elevator1)
    print(elevator2)
    print("=" * 120)

    # GUI codes
    print_background()
    # Display variables(time & watt)
    watts_str = str(round(watts / 3600, 4))
    text_watts = font.render(watts_str, True, black)
    time_str = str(round(wtime, 3))
    text_wtime = font.render(time_str, True, black)
    count_str = str(count / 10)
    text_count = font.render(count_str, True, black)
    screen.blit(text_watts, (950, SIZE - 30))
    screen.blit(text_wtime, (1050, 2 * SIZE - 30))
    screen.blit(text_count, (1050, 3 * SIZE - 30))
    # Display two elevators

    pygame.draw.rect(screen, grey, [
                     30 - elevator1.opening_sequence, int(400 - elevator1.location * 40), 25, SIZE])
    pygame.draw.rect(screen, grey, [
                     55 + elevator1.opening_sequence, int(400 - elevator1.location * 40), 25, SIZE])
    pygame.draw.rect(screen, grey, [
                     170 - elevator2.opening_sequence, int(400 - elevator2.location * 40), 25, SIZE])
    pygame.draw.rect(screen, grey, [
                     195 + elevator2.opening_sequence, int(400 - elevator2.location * 40), 25, SIZE])

    # Display button inputs
    for i in range(len(lc)):
        for j in range(len(lc[i])):
            if lc[i][j]:
                if j == 6:
                    pygame.draw.circle(screen, yellow, (410 + i * 57, 700), 15)
                else:
                    pygame.draw.circle(
                        screen, yellow, (410 + i * 57, 600 - j * SIZE), 15)
            else:
                if j == 6:
                    pygame.draw.circle(
                        screen, black, (410 + i * 57, 700), 15, 5)
                else:
                    pygame.draw.circle(
                        screen, black, (410 + i * 57, 600 - j * SIZE), 15, 5)
    for i in range(len(cc)):
        for j in range(len(cc[i])):
            if cc[i][j]:
                pygame.draw.circle(
                    screen, yellow, (540 + j * 80, 600 - i * SIZE), 15)
            else:
                pygame.draw.circle(
                    screen, black, (540 + j * 80, 600 - i * SIZE), 15, 5)

    # If there's a key input "ESC", quit the displaying
    for event in pygame.event.get():
        key_event = pygame.key.get_pressed()
        if key_event[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    count = count + 1
