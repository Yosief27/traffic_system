
from statistics import mean, median
from time import sleep
import destinations as des
import trafficComponents as tc
from trafficComponents import Vehicle


class TrafficSystem:
    """Defines a traffic system"""

    def __init__(self):
        self.time = 0
        self.lane1 = tc.Lane(5)
        self.lane2 = tc.Lane(5)
        self.des = des.Destinations()
        self.light = tc.Light(10, 8)
        self.wait_vehicle = []

    def snapshot(self):

        print(f'{self.lane1}{self.light}{self.lane2}{self.wait_vehicle}')

    def step(self):
        self.time += 1

        self.lane1.remove_first()
        self.lane1.step()
        if self.light.is_green():
            # removing a vehicle from the second lane
            v = self.lane2.remove_first()
            # add to the first line if there is a care
            self.lane1.enter(v if v is not None else '.')
        # step the light and lean 2
        self.light.step()
        self.lane2.step()

        new_des = self.des.step()
        # if there is a destination to go then create new vehicle and go on the road
        if new_des is not None:
            # new vehicle in the queue
            self.wait_vehicle.append(tc.Vehicle(new_des, self.time))

            if self.lane2.last_free():
                if len(self.wait_vehicle) != 0:
                    self.lane2.enter(self.wait_vehicle.pop(0))
        # if there is not destination ,then check if there are vehicles in the queue
        else:
            if self.lane2.last_free():
                if len(self.wait_vehicle) != 0:
                    self.lane2.enter(self.wait_vehicle.pop(0))

    def in_system(self):
        pass

    def print_statistics(self):
        pass


def main():
    ts = TrafficSystem()
    for i in range(100):
        ts.snapshot()
        ts.step()
        sleep(0.1)
    print('\nFinal state:')
    ts.snapshot()
    print()
    ts.print_statistics()


if __name__ == '__main__':
    main()
