
from statistics import mean, median
from time import sleep
import destinations as des
import trafficComponents as tc
from trafficComponents import Vehicle
from statistics import median


class TrafficSystem:
    """Defines a traffic system"""

    def __init__(self):
        self.time = 0
        self.lane = tc.Lane(11)
        self.lane_w = tc.Lane(8)
        self.lane_s = tc.Lane(8)
        self.des = des.Destinations()
        self.light_w = tc.Light(14, 6)
        self.light_s = tc.Light(14, 4)
        self.wait_vehicle = []
        self.block_w = 0
        self.block_s = 0

        self.time = 0
        self.new_vehicle = 0
        self.vehicle_w = 0
        self.vehicle_s = 0
        self.count = 0
        self.queue_count = 0
        self.vehicle_pass_s = []
        self.vehicle_pass_w = []
    block_set = ''

    def snapshot(self):

        print(
            f'{self.light_w}{self.lane_w}{self.block_set}{self.lane}{self.wait_vehicle}\n{self.light_s}{self.lane_s}\n')

    def step(self):
        self.time += 1
        # check if south light is green
        if self.light_s.is_green():
            if self.lane_s.get_first() is not None:
                lift_s = self.lane_s.remove_first()
                # calculate creation and passing time of the vehicle
                self.vehicle_pass_s.append(self.time-lift_s.borntime)
                # count the vehicle heading to south
                self.vehicle_s += 1
        # check if west light is green
        if self.light_w.is_green():
            if self.lane_w.get_first() is not None:
                lift_w = self.lane_w.remove_first()
                self.vehicle_pass_w.append(self.time-lift_w.borntime)
                self.vehicle_w += 1
                self.count += 1

        # step lane
        self.lane_s.step()
        self.lane_w.step()

        # stepping vehicle from lane to south or west depending to their destination
        if self.lane.get_first() is 'S':
            # check the destination lane is free
            if self.lane_s.last_free():
                # clear if here is any block
                self.block_set = ''
                # move the vehicle
                self.lane_s.enter(self.lane.remove_first())

            else:
                # count the block and block the lane
                self.block_s += 1
                self.block_set = '*'

        elif self.lane.get_first() is 'W':
            if self.lane_w.last_free():
                self.block_set = ''
                self.lane_w.enter(self.lane.remove_first())

            else:
                self.block_w += 1
                self.block_set = '*'
        self.lane.step()
        # check if there is a destination to go and  create new vehicle and add to back of the lane
        new_des = self.des.step()
        if new_des is not None:
            # new vehicle to be created
            self.new_vehicle += 1
            # check if the last space of the line is free and insert the new vehicle
            if self.lane.last_free():
                self.lane.enter(tc.Vehicle(new_des, self.time))
            # but if the last space of the lane is not free add the newly created vehicle into the  waiting queue
            else:
                self.wait_vehicle.append(tc.Vehicle(new_des, self.time))

        # No destination then   check the queue if there is already a vehicle on the waiting queue
        elif self.lane.last_free():
            if len(self.wait_vehicle) != 0:
                self.lane.enter(self.wait_vehicle.pop(0))
        if len(self.wait_vehicle) != 0:
            self.queue_count += 1

        # step light
        self.light_s.step()
        self.light_w.step()

    def in_system(self):

        pass

    def statistics(self):
        # print((self.block_s + self.block_w), self.time,
        #       self.new_vehicle, self.vehicle_s, self.vehicle_w, self.queue_count)
        """Print statistics about the run."""
        print('Statistics after 100 timesteps:')
        print(f'Created vehicles:\t{self.new_vehicle}')
        print(
            f'In system\t:\t{self.lane_s.number_in_lane() + self.lane_w.number_in_lane() + self.lane.number_in_lane() +len(self.wait_vehicle)}')
        print()
        print(f'At exit\t\t west\t South')
        print(f'Vehicles out\t{self.vehicle_w}\t{self.vehicle_s}')

        print(
            f'Minimal time:\t{min(self.vehicle_pass_w)}\t{min(self.vehicle_pass_s)}')
        print(
            f'Maximal time:\t{max(self.vehicle_pass_w)}\t{max(self.vehicle_pass_s)}')
        print(
            f'Mean time\t{round(mean(self.vehicle_pass_w),1)}\t{round(mean(self.vehicle_pass_s),1)}')
        print(
            f'Median time\t{median(self.vehicle_pass_w)}\t{median(self.vehicle_pass_s)}')

        print()
        print(f'Blocked\t:{self.block_s + self.block_w}%')
        print(f'Queue\t:{self.queue_count}%')


def main():
    ts = TrafficSystem()
    for i in range(100):
        ts.snapshot()
        ts.step()
        sleep(0.1)
    print('\nFinal state:')
    ts.snapshot()
    print()
    ts.statistics()


if __name__ == '__main__':
    main()
