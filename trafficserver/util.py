from pprint import pprint
import json
from random import randint
from typing import TypeVar

import matplotlib.pyplot as plt

JSON = TypeVar("json")


def generate_random_user_outer(floors: int, show: bool) -> JSON:
    PATTERNS = [11, 5, 4, 5, 15, 18, 12, 39, 51, 37, 31,
                30, 40, 48, 48, 47, 50, 60, 59, 50, 39, 37, 30, 21]
    ret = dict()
    ys = []
    for time in range(0, 24):
        infos = []
        cur_pattern = PATTERNS[time]
        total_people = 0
        for floor in range(1, floors+1):
            for is_up in [True, False]:
                people = randint(-cur_pattern, cur_pattern)
                people /= 10
                info = [is_up, floor, cur_pattern + people]
                infos.append(info)
                total_people += (cur_pattern + people)
        avg_people = total_people / (floors * 2)
        ys.append(avg_people)
        ret[time] = infos

    plt.plot(list(range(1, 25)), ys)
    if show:
        plt.show()

    return json.dumps(ret)


def calc_total(traffic, user_floor, elev_floor,):
    ret = 0
    floor_cache = set()

    # inbound calc
    for floor in (min(elev_floor, user_floor), max(elev_floor, user_floor)):
        floor_cache.add(floor)
        ret += traffic[floor]

    # outbound calc
    for floor in range(1, len(traffic)+1):
        if floor in floor_cache:
            continue
