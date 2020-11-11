import json
from random import randint
from typing import TypeVar

JSON = TypeVar("json")


def generate_random_user_inner(total_floor: int) -> JSON:
    ret = dict()
    return json.dumps(ret)


def generate_random_user_outer(floors: int) -> JSON:
    ret = dict()
    for time in range(0, 24):
        infos = []
        for floor in range(1, floors+1):
            for is_up in [True, False]:
                people = randint(0, 80)
                people /= 10
                info = [is_up, floor, people]
                infos.append(info)
        ret[time] = infos

    return json.dumps(ret)


def calc_total(traffic, target_floor, elev_floor, user_floor):
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
