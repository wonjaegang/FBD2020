lowest = - 2.5
highest = 10.0


class Elevator:
    speed = 0.1  # 0.1m/loop

    def __init__(self, num, location):  # initialize instance
        self.num = num
        self.location = location

    def commend(self, commend):
        if commend == 'u':
            if self.location == highest:
                raise IndexError("It is the highest floor")
            self.location += Elevator.speed
        elif commend == 'd':
            if self.location == lowest:
                raise IndexError("It is the lowest floor")
            self.location -= Elevator.speed

    def __str__(self):
        return "Elevator{x} location : {y}m".format(x=self.num, y=self.location)


elevator1 = Elevator(1, 0)
elevator2 = Elevator(2, 0)
while True:
    a = input()
    if a == "s":
        break
    elevator1.commend(a)
    print(elevator1)
    print(elevator2)
    print(elevator2.__dict__)
