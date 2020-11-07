import json
from pprint import pprint
from collections import defaultdict

from traffic.trafficABC import Traffic
from typing import TypeVar

JSON = TypeVar("json")


class Outer(Traffic):
    def __init__(self, total_floor: int):
        self.dates = 0
        self.lookup = dict()

        self.lookup[Traffic.UP] = dict()
        self.lookup[Traffic.DOWN] = dict()

        for floor_id in range(1, total_floor+1):
            self.lookup[Traffic.UP][floor_id] = 0.0
            self.lookup[Traffic.DOWN][floor_id] = 0.0

    def get_prediction(self, elev_floor: int, user_floor: int) -> JSON:
        def is_up(elev_floor, user_floor):
            return elev_floor > user_floor

        open_time, close_time, move_time = Traffic.OPEN_TIME, Traffic.OPEN_TIME, Traffic.TIME_PER_PERSON
        direction = Traffic.UP if is_up(
            elev_floor, user_floor) else Traffic.DOWN
        ret = defaultdict(dict)
        for direction, info in self.lookup.items():
            ret[direction] = info

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
            {time: [direction:bool, floor:int, num_of_enter:float]
            {0 :[[UP, 3, 13.5], [...], 1: [[DOWN, 5, 2.3], [...]] ...}
        """
        time_user_dict = json.loads(time_user)

        for time, infos in time_user_dict.items():
            for info in infos:
                direction, floor, num_of_enter = info
                cur_traffic = self.lookup[direction][floor]
                cur_traffic = (cur_traffic * self.dates +
                               num_of_enter) / (self.dates + 1)
                self.lookup[direction][floor] = cur_traffic

        self.dates += 1
