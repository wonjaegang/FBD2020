import decimal
import serial
import sys
import pygame
import time
import itertools

ardu = serial.Serial(port='COM10', baudrate=9600, timeout=0.1)  # revise port's name for each PC after
loop_time = decimal.Decimal(0.1)

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
text_time = font.render("waiting time:                  sec", True, black)
text_loop_count = font.render("loop count:                     sec", True, black)
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
    operating_power = 2  # kW

    def __init__(self, id_num, floor):  # initialize instance
        self.id_num = id_num
        self.location = Building.floor_height * (floor - 1)
        self.v_direction = 0
        self.opening_sequence = 0
        self.destination_floor = floor
        self.destination = [self.location, "uncalled"]
        self.call_done = False

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
        self.destination_floor = floor
        self.destination = [floor, call_type]
        if self.location < (floor - 1) * Building.floor_height:
            self.command('u')
        elif self.location > (floor - 1) * Building.floor_height:
            self.command('d')
        elif self.destination[1] == "uncalled":
            self.command('s')
        # when elevator arrived
        else:
            self.command('s')
            self.door_open()
            self.call_done = True

    def door_open(self):
        self.opening_sequence = Elevator.door_operating_time

    def door_close(self):
        self.opening_sequence -= 1

    def __str__(self):
        return "Elevator{x} Location : {y}m, Direction : {z}, Opening Sequence : {r}, Destination floor : {a}" \
            .format(x=self.id_num, y=self.location, z=self.v_direction, r=self.opening_sequence, a=self.destination)


# Global variables
# cc : Car Call      [floor(-1) <- [down, up], floor(1) <- [down, up], ... floor(5) <- [down, up]]
# lc : Landing Call  [ Ele(1) <- [0, 1, 2, 3, 4, 5, open], Ele(2) <- [0, 1, 2, 3, 4, 5, open]]
cc = [[False] * 2 for k in range(Building.whole_floor)]
lc = [[False] * (Building.whole_floor + 1) for i in range(2)]
cc_button_num = len(cc) * 2 - 2  # Except lowest down, highest up
run_main_algorithm = False
# calculate power consumption on watts, and waiting time on wtime
watts = 0
wtime = 0
count = 0
# moved distance with constant direction. [[e1 direction(1, 0, -1), e1 distance(m)], [e2~, e2~]]
moved_distance = [[0, 0], [0, 0]]


# Function that converts button inputs to the Car Calls and the Landing Calls
# It modifies global variables
def input_to_call():
    data = ardu.readline()
    if data == b'\x00\r\n':
        data = b''

    # Get to Work
    if count == 100:  # 1th -> destination: 4th, 5th
        data = b'C\r\n'
    if count == 150:  # 1th -> destination: 3th
        data = b'C\r\n'
    if count == 250:  # 5th -> destination: 1th
        data = b'J\r\n'
    if count == 260:  # 1th -> destination: 3th
        data = b'C\r\n'
    if count == 300:  # B1th -> destination: 2th
        data = b'A\r\n'

    # # Get off Work
    # if count == 100:  # 5th -> destination: 1th, B1th
    #     data = b'J\r\n'
    # if count == 120:  # 4th -> destination: 1th
    #     data = b'H\r\n'
    # if count == 200:  # 1th -> destination: 5th
    #     data = b'C\r\n'
    # if count == 240:  # 3th -> destination: 5th
    #     data = b'G\r\n'
    # if count == 300:  # 5th -> destination: 1th, B1th
    #     data = b'J\r\n'

    # # Lunch time
    # if count == 100:  # 5th -> destination: 1th
    #     data = b'J\r\n'
    # if count == 101:  # 2th -> destination: 1th
    #     data = b'D\r\n'
    # if count == 130:  # 1th -> destination: 3th
    #     data = b'C\r\n'
    # if count == 180:  # 3th -> destination: 1th
    #     data = b'F\r\n'
    # if count == 181:  # 1th -> destination: 5th
    #     data = b'C\r\n'
    # if count == 240:  # 1th -> destination: 4th
    #     data = b'C\r\n'
    # if count == 300:  # 4th -> destination: B1th
    #     data = b'H\r\n'

    # # Slack hours
    # if count == 100:  # destination: 1th
    #     data = b'J\r\n'
    # if count == 400:  # destination: 4th
    #     data = b'C\r\n'
    # if count == 700:  # destination: B1th
    #     data = b'D\r\n'
    # if count == 1000:  # destination: 1th
    #     data = b'F\r\n'
    # if count == 1300:  # destination: B1th
    #     data = b'C\r\n'

    int_data = int.from_bytes(data, "little") - int.from_bytes(b'A\r\n', "little")  # Convert to int starts from 0
    # If input data is None
    if int_data == int.from_bytes(bytes(), "little") - int.from_bytes(b'A\r\n', "little"):
        print("There is no button input")
    # If there is an input data, assign it to Landing Call or Car Call
    # If input data is NOT proper, raise assertion exception
    else:
        assert (0 <= int_data < cc_button_num + Building.whole_floor * 2 + 2), \
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
    #                                             #
    #         YOUR ALGORITHM STARTS HERE          #
    #                                             #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    # Cost comparing algorithm :
    #      Simulate every number of cases and calculate the cost of each case. Select the case that has lowest cost.
    #           cost_time :
    #           cost_power :
    #           cost_consistency :
    #           cost_total = cost_time * Wt + cost_power * Wp + cost_consistency * Wc
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Set weight values
    w_time = decimal.Decimal(1)
    w_power = decimal.Decimal(0)
    w_consistency = decimal.Decimal(0)
    # assert (round(w_time + w_power + w_consistency, 1) == 1), "Sum of weight values is not 1"

    # Put lc / cc values to car_calls and lc_calls list
    car_calls = []
    lc_calls = [[], []]
    cc_num = 0
    for floor in range(Building.whole_floor):
        for call_type in range(2):
            if cc[floor][call_type]:
                car_calls.append([floor, "cc" + str(call_type), cc_num])
                cc_num += 1
    for id_num in range(2):
        for floor in range(Building.whole_floor):
            if lc[id_num][floor]:
                lc_calls[id_num].append([floor, "lc"])

    # Slice car_calls list with number of all cases
    lowest_cost = decimal.Decimal(1000000.0)
    e1_destination_call = []
    e2_destination_call = []
    for slice_case in range(pow(2, len(car_calls))):
        calls = [[], []]
        # Change slice_case variable to binary number
        # Put car_calls & virtual landing calls to calls[[], []], referring to slice_case, using binary number
        for i in range(len(car_calls)):
            e_num = int(format(slice_case, 'b').zfill(len(car_calls))[i])
            calls[e_num].append(car_calls[i])
            calls[e_num].append([car_calls[i][0] + int(car_calls[i][1][2]) * 2 - 1, "virtual_lc", car_calls[i][2]])
        # Put lc_calls to calls[[], []]
        for id_num in range(2):
            calls[id_num] += lc_calls[id_num]
        print("Car-call slice of this loop : ", end='')
        print(calls)
        # Put every case of e1's move into whole_cases1, as tuple, using permutation iterator
        whole_cases1 = list(itertools.permutations(calls[0], len(calls[0])))
        for case_num1 in range(len(whole_cases1)):
            # Ignore the case in which virtual lc is ordered before corresponding car call.
            cc_list = [0 for i in range(cc_num)]  # array to check the order of cc / virtual_lc
            for order in range(len(whole_cases1[case_num1])):
                if len(whole_cases1[case_num1][order]) == 3:
                    if whole_cases1[case_num1][order][1] == "virtual_lc":
                        cc_list[whole_cases1[case_num1][order][2]] *= 0
                    else:
                        cc_list[whole_cases1[case_num1][order][2]] += 1
            if sum(cc_list):
                continue
            # Put every case of e2's move into whole_cases2, as tuple, using permutation iterator
            whole_cases2 = list(itertools.permutations(calls[1], len(calls[1])))
            for case_num2 in range(len(whole_cases2)):
                # Ignore the case in which virtual lc is ordered before corresponding car call.
                cc_list = [0 for i in range(cc_num)]  # array to check the order of cc / virtual_lc
                for order in range(len(whole_cases2[case_num2])):
                    if len(whole_cases2[case_num2][order]) == 3:
                        if whole_cases2[case_num2][order][1] == "virtual_lc":
                            cc_list[whole_cases2[case_num2][order][2]] *= 0
                        else:
                            cc_list[whole_cases2[case_num2][order][2]] += 1
                if sum(cc_list):
                    continue

                cost_time = 0
                cost_power = 0
                cost_consistency = 0

                # Calculate estimated waiting time of passengers in specific case
                # Bug : 층에 도착하여 문이 열려있는 상태에서, 동일한 층의 car call 이 들어오면
                #       현재의 opening sequence 를 무시해야하지만, 무시하지 않음
                # Be aware of increase rate of waiting time : more waiting passengers, faster it increases
                # The number of waiting passengers == the number of calls except cc (lc num + vlc num)
                def waiting_passengers(starting, target_list):
                    pss_num = 0
                    for n in range(starting, len(target_list)):
                        if not target_list[n][1][:2] == "cc":
                            pss_num += 1
                    return pss_num
                if len(whole_cases1[case_num1]):
                    # Waiting time from current location & opening sequence to first destination
                    cost_time += (abs(e1.location - (whole_cases1[case_num1][0][0] - 1) * Building.floor_height)
                                  + e1.opening_sequence * loop_time) * waiting_passengers(0, whole_cases1[case_num1])
                    # Waiting time from second destination to last destination
                    for i in range(len(whole_cases1[case_num1]) - 1):
                        cost_time += (abs(whole_cases1[case_num1][i][0] - whole_cases1[case_num1][i + 1][0])
                                      * Building.floor_height + Elevator.door_operating_time * loop_time) \
                                      * waiting_passengers(i + 1, whole_cases1[case_num1])
                # e2 : Just same with e1
                if len(whole_cases2[case_num2]):
                    cost_time += (abs(e2.location - (whole_cases2[case_num2][0][0] - 1) * Building.floor_height)
                                  + e2.opening_sequence * loop_time) * waiting_passengers(0, whole_cases2[case_num2])
                    for i in range(len(whole_cases2[case_num2]) - 1):
                        cost_time += (abs(whole_cases2[case_num2][i][0] - whole_cases2[case_num2][i + 1][0])
                                      * Building.floor_height + Elevator.door_operating_time * loop_time) \
                                      * waiting_passengers(i + 1, whole_cases2[case_num2])

                # Calculate estimated power consumption of e1 & e2 in specific case
                # Bug : 쉬고있는 엘리베이터의 가동전력을 계산하지 않음
                # 소비전력 예측 함수 : 전 단계 문 닫힌 상태 ~ 다음단계 문 닫힌 상태
                def calculate_p(h1, h2, journey, weight_check):
                    direction = (lambda f1, f2: 1 if (f2 > f1) else (-1 if (f1 > f2) else 0))(h1, h2)
                    weight = 0
                    # 승강기 무게 계산
                    for k in range(len(journey) - weight_check):
                        if journey[len(journey) - k - 1][1][:2] == "lc":
                            weight += 70
                    # 아래의 식은 update_evaluation_factor 함수 참고
                    k = decimal.Decimal(7.75) * (1 - direction) + (decimal.Decimal(2 / 75) * weight - 8) * direction
                    moved = abs(h1 - h2)
                    # 같은 층에서의 input 은 바로 처리되기에, 문이 닫히는 동안의 소비전력만 계산하면 됨
                    if direction:
                        return moved * Elevator.operating_power \
                            + (k - Elevator.operating_power) * (moved - Building.floor_height / 2) \
                            + Elevator.door_operating_time * loop_time * Elevator.operating_power
                    else:
                        return Elevator.door_operating_time * loop_time * Elevator.operating_power
                # Elevator 1 power consumption
                if len(whole_cases1[case_num1]):
                    # 현재 위치에서 첫 목적지까지 움직일 때의 소비전력 계산
                    cost_power += calculate_p(e1.location,
                                              (whole_cases1[case_num1][0][0] - 1) * Building.floor_height,
                                              whole_cases1[case_num1],
                                              0)
                    # 각 움직임에서 얼마나 전력이 소모될 지 계산
                    for trip in range(len(whole_cases1[case_num1]) - 1):
                        cost_power += calculate_p((whole_cases1[case_num1][trip][0] - 1) * Building.floor_height,
                                                  (whole_cases1[case_num1][trip + 1][0] - 1) * Building.floor_height,
                                                  whole_cases1[case_num1],
                                                  trip + 1)
                # Elevator 2 power consumption
                if len(whole_cases2[case_num2]):
                    # 현재 위치에서 첫 목적지까지 움직일 때의 소비전력 계산
                    cost_power += calculate_p(e2.location,
                                              (whole_cases2[case_num2][0][0] - 1) * Building.floor_height,
                                              whole_cases2[case_num2],
                                              0)
                    # 각 움직임에서 얼마나 전력이 소모될 지 계산
                    for trip in range(len(whole_cases2[case_num2]) - 1):
                        cost_power += calculate_p((whole_cases2[case_num2][trip][0] - 1) * Building.floor_height,
                                                  (whole_cases2[case_num2][trip + 1][0] - 1) * Building.floor_height,
                                                  whole_cases2[case_num2],
                                                  trip + 1)

                # Calculate Consistency of elevator
                # Elevator 1
                if len(whole_cases1[case_num1]):
                    location1 = e1.location
                    location2 = (whole_cases1[case_num1][0][0] - 1) * Building.floor_height
                    direction_next = (lambda f1, f2: 1 if (f2 > f1) else (-1 if (f1 > f2) else 0))(location1, location2)
                    direction_variation = abs(e1.v_direction - direction_next)
                    if direction_variation == 2:
                        cost_consistency += 1
                # Elevator 2
                if len(whole_cases2[case_num2]):
                    location1 = e2.location
                    location2 = (whole_cases2[case_num2][0][0] - 1) * Building.floor_height
                    direction_next = (lambda f1, f2: 1 if (f2 > f1) else (-1 if (f1 > f2) else 0))(location1, location2)
                    direction_variation = abs(e2.v_direction - direction_next)
                    if direction_variation == 2:
                        cost_consistency += 1

                # Main sentence of this algorithm. Calculate total cost with given weight-values
                cost_total = cost_time * w_time + cost_power * w_power + cost_consistency * w_consistency
                if cost_total < lowest_cost:
                    lowest_cost = cost_total
                    if len(whole_cases1[case_num1]) == 0:
                        e1_destination_call = [e1.destination_floor, "uncalled"]
                    elif e1.opening_sequence > 0:
                        if whole_cases1[case_num1][0][0] == e1.destination_floor:
                            e1_destination_call = whole_cases1[case_num1][0]
                        else:
                            e1_destination_call = [e1.destination_floor, "uncalled"]
                    else:
                        e1_destination_call = whole_cases1[case_num1][0]
                    if len(whole_cases2[case_num2]) == 0:
                        e2_destination_call = [e2.destination_floor, "uncalled"]
                    elif e2.opening_sequence > 0:
                        if whole_cases2[case_num2][0][0] == e2.destination_floor:
                            e2_destination_call = whole_cases2[case_num2][0]
                        else:
                            e2_destination_call = [e2.destination_floor, "uncalled"]
                    else:
                        e2_destination_call = whole_cases2[case_num2][0]
                print("case(%dth e1 case, %dth e2 case) : " % (case_num1, case_num2), end='')
                print(whole_cases1[case_num1], whole_cases2[case_num2], "-> ", end='')
                print("waiting time : %.2f, watts : %.2f, consistency : %0.2f, total cost : %.2f"
                      % (cost_time, cost_power, cost_consistency, cost_total))
        print("-" * 5)

    # [[elevator1 destination floor, elevator1 call type], [elevator2 destination floor, elevator2 call type]]
    # call type : "lc" : landing call, "cc0" : car call - down, "cc1" : car call - up, "uncalled" : command without call
    destination_call = [e1_destination_call, e2_destination_call]  # example
    print("selected destination :", destination_call)
    return destination_call


# Turn off calls if elevator arrived
def update_call(e):
    if e.call_done:
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
    e_direction = [e1.v_direction, e2.v_direction]
    power_per_loop = [0, 0]
    for i in range(2):
        ps_weight = lc_true_num[i] * 70
        power_constant = decimal.Decimal(15.5) * (1 - e_direction[i]) / 2 \
            + (decimal.Decimal((28 + 8) / 1350) * ps_weight - 8) * e1.v_direction
        if moved_distance[i][0]:
            if not moved_distance[i][1]:
                power_per_loop[i] = (Building.floor_height / Elevator.speed / 2) \
                                    * (power_constant - Elevator.operating_power) * loop_time
            elif moved_distance[i][1] > Building.floor_height:
                power_per_loop[i] = power_constant * loop_time
            else:
                power_per_loop[i] = Elevator.operating_power * loop_time
        else:
            power_per_loop[i] = Elevator.operating_power * loop_time
    return [wtime_per_loop, power_per_loop[0] + power_per_loop[1]]


# Make instances and initialize their id and initial position
# Elevator(id_num, floor)
elevator1 = Elevator(1, 1)
elevator2 = Elevator(2, 1)
command = [[elevator1.location / Building.floor_height + 1, "uncalled"],
           [elevator2.location / Building.floor_height + 1, "uncalled"]]
while True:
    print("loop count :", count)
    input_to_call()
    if run_main_algorithm:
        print("run allocation algorithm")
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
    elevator1.move_to_destination(command[0][0], command[0][1])
    elevator2.move_to_destination(command[1][0], command[1][1])

    # Turn off completed calls
    update_call(elevator1)
    update_call(elevator2)

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
    print("=" * 50)

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

    pygame.draw.rect(screen, grey, [30 - elevator1.opening_sequence, int(400 - elevator1.location * 40), 25, SIZE])
    pygame.draw.rect(screen, grey, [55 + elevator1.opening_sequence, int(400 - elevator1.location * 40), 25, SIZE])
    pygame.draw.rect(screen, grey, [170 - elevator2.opening_sequence, int(400 - elevator2.location * 40), 25, SIZE])
    pygame.draw.rect(screen, grey, [195 + elevator2.opening_sequence, int(400 - elevator2.location * 40), 25, SIZE])

    # Display button inputs
    for i in range(len(lc)):
        for j in range(len(lc[i])):
            if lc[i][j]:
                if j == 6:
                    pygame.draw.circle(screen, yellow, (410 + i * 57, 700), 15)
                else:
                    pygame.draw.circle(screen, yellow, (410 + i * 57, 600 - j * SIZE), 15)
            else:
                if j == 6:
                    pygame.draw.circle(screen, black, (410 + i * 57, 700), 15, 5)
                else:
                    pygame.draw.circle(screen, black, (410 + i * 57, 600 - j * SIZE), 15, 5)
    for i in range(len(cc)):
        for j in range(len(cc[i])):
            if cc[i][j]:
                pygame.draw.circle(screen, yellow, (540 + j * 80, 600 - i * SIZE), 15)
            else:
                pygame.draw.circle(screen, black, (540 + j * 80, 600 - i * SIZE), 15, 5)

    # If there's a key input "ESC", quit the displaying
    for event in pygame.event.get():
        key_event = pygame.key.get_pressed()
        if key_event[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    # time.sleep(0.01)
    count = count + 1
