import json
from random import randint
from typing import TypeVar

JSON = TypeVar("json")


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
