# Traffic system components
from destinations import *


class Vehicle:
    """Represents vehicles in traffic simulations"""

    def __init__(self, destination, borntime):
        self.destination = destination
        self.borntime = borntime

    def __repr__(self):
        return f'{self.destination}'


class Lane:
    "Represents a lane with (possible) vehicles"

    def __init__(self, length):
        self.length = length
        self.lane = ["." for i in range(length)]
        self.vehicle = ''

    def enter(self, vehicle):
        self.vehicle = vehicle
        if self.last_free():
            self.lane[self.length-1] = self.vehicle

    def last_free(self):
        return True if self.lane[self.length-1] == '.' else False

    def step(self):

        for i, v in enumerate(self.lane):
            if i == 0 and v != '.':
                pass

            elif v != '.':
                if self.lane[i-1] == '.':
                    self.lane[i-1] = self.lane[i]
                    self.lane[i] = '.'

    def get_first(self):
        return self.lane[0].destination if self.lane[0] != '.' else None

    def remove_first(self):
        if self.lane[0] != '.':
            v = self.lane[0]
            self.lane[0] = '.'
            return v
        else:
            return None

    def number_in_lane(self):

        return sum(map(lambda v: v != '.', self.lane))

    def __repr__(self):
        list_lane = [vehicle.destination if vehicle !=
                     '.' else '.' for vehicle in self.lane]
        return f'[{list_lane}]'

    def __str__(self):
        list_lane = [vehicle.destination if vehicle !=
                     '.' else '.' for vehicle in self.lane]
        test = '{}'*(len(list_lane)-1)+'{}'

        return f'[{test.format(*list_lane)}]'


def demo_lane():
    """For demonstration of the class Lane"""
    a_lane = Lane(10)
    print(a_lane)

    des = Destinations()
    v = Vehicle('N', 34)

    a_lane.enter(v)
    print(a_lane)
    a_lane.step()
    print(a_lane)

    for i in range(20):
        if i % 2 == 0:
            #u = Vehicle(des.step(), i)
            u = Vehicle('S', i)
            a_lane.enter(u)
        a_lane.step()
        print(a_lane)
        if i % 3 == 0:
            print('  out: ', a_lane.get_first(),
                  a_lane.remove_first())
    print('Number in lane:',
          a_lane.number_in_lane(), a_lane.length)


class Light:
    """Represents a traffic light"""
    cur = 0

    def __init__(self, period, green_period):
        self.period = period
        self.green_period = green_period
        self.light = {}
        self.cur = 0
        for i in range(self.period):
            if i < self.green_period:
                self.light[i] = 'G'
            else:
                self.light[i] = 'R'

    def __str__(self):
        return "(%s)" % (self.light[self.cur])

    def __repr__(self):
        pass

    def step(self):
        if self.cur == self.period-1:
            self.cur = 0
        else:
            self.cur += 1

    def is_green(self):
        if self.light[self.cur] == 'G':
            return True
        else:
            return False


def demo_light():
    """Demonstrats the Light class"""
    a_light = Light(10, 8)

    for i in range(20):
        print(i, a_light,
              a_light.is_green())
        a_light.step()
    pass


def main():
    """Demonstrates the classes"""
    # print('\nLight demonstration\n')
    # demo_light()
    # print('\nLane demonstration')
    demo_lane()
    # v1 = Vehicle('N', 1)
    # print(v1)
    pass


if __name__ == '__main__':
    main()
