import json
from pprint import pprint

from traffic.trafficABC import Traffic
from typing import TypeVar

JSON = TypeVar("json")


class Outer(Traffic):
    def __init__(self, total_floor: int, num_of_elevs: int):
        self.dates = 0
        self.lookup = dict()

        for elev_id in range(num_of_elevs):
            self.lookup[elev_id] = dict()
            self.lookup[elev_id][Traffic.UP] = dict()
            self.lookup[elev_id][Traffic.DOWN] = dict()

            for floor_id in range(1, total_floor+1):
                self.lookup[elev_id][Traffic.UP][floor_id] = 0
                self.lookup[elev_id][Traffic.DOWN][floor_id] = 0

    def get_prediction(self, current_floor: int, target_floor: int) -> JSON:
        self._calculate_time()
        self._calculate_traffic()
        pass

    def _calculate_time(self):
        pass

    def _calculate_traffic(self):
        pass

    def update_table(self, time_user: JSON, elev_id: int):
        """ update look up table
        args:
            time_user, JSON: one day logged data that has average number of people per hour
            {time: [direction:bool, floor:int, num_of_enter:float]
            {0 :[[UP, 3, 13.5]], 1: [[DOWN, 5, 2.3]] ...}
        """
        time_user_dict = json.loads(time_user)

        for time, info in time_user_dict.items():
            direction, floor, num_of_enter = info
            cur_traffic = self.lookup[elev_id][direction][floor]
            cur_traffic = (cur_traffic * self.dates +
                           num_of_enter) / (self.dates + 1)
            self.lookup[elev_id][direction][floor] = cur_traffic

        self.dates += 1
