import json
from pprint import pprint
from collections import defaultdict

from traffic.trafficABC import Traffic
from typing import TypeVar

JSON = TypeVar("json")


class Outer(Traffic):
    def __init__(self, total_floor: int):
        self.dates = 0
        self.total_floor = total_floor
        self.lookup = dict()

        for time in range(0, 24):
            self.lookup[time] = dict()
            self.lookup[time][Traffic.UP] = dict()
            self.lookup[time][Traffic.DOWN] = dict()

            for floor in range(1, total_floor+1):
                self.lookup[time][Traffic.UP][floor] = 0.0
                self.lookup[time][Traffic.DOWN][floor] = 0.0

    def get_prediction(self, elev_floor: int, user_floor: int, time: int) -> dict:
        def is_above(elev_floor, user_floor):
            return elev_floor > user_floor

        move_time = Traffic.TIME_PER_PERSON
        above = is_above(elev_floor, user_floor)

        ret = dict()
        direction = Traffic.UP if above else Traffic.DOWN
        calculated_floors = set()

        for floor in range(min(user_floor, elev_floor), max(user_floor, elev_floor)):
            calculated_floors.add(floor)
            ret[floor] = self.lookup[time][direction][floor] * move_time

        for floor in range(1, self.total_floor+1):
            if floor in calculated_floors:
                continue

            for direction in [Traffic.UP, Traffic.DOWN]:
                if floor not in ret:
                    ret[floor] = self.lookup[time][direction][floor] * move_time
                else:
                    ret[floor] += self.lookup[time][direction][floor] * move_time
        return ret

    def _calculate_time(self):
        pass

    def _calculate_traffic(self):
        pass

    def get_traffic():
        pass

    def update_table(self, time_user: JSON):
        """ update look up table
        args:
            time_user, JSON: one day logged data that has average number of people per hour
            {time: [direction:bool, floor:int, num_of_enter:float]}
            {0 :[[UP, 3, 13.5], [...]], 1: [[DOWN, 5, 2.3], [...]] ...}
        """
        time_user_dict = json.loads(time_user)

        for time, infos in time_user_dict.items():
            time = int(time)
            for info in infos:
                direction, floor, num_of_enter = info
                cur_traffic = self.lookup[time][direction][floor]
                cur_traffic = (cur_traffic * self.dates +
                               num_of_enter) / (self.dates + 1)
                self.lookup[time][direction][floor] = cur_traffic

        self.dates += 1
