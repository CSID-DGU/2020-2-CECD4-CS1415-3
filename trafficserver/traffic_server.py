import json
from pprint import pprint
from traffic import outer, inner
import util

"""
Input:
    [user_floor, elev_cur_floor, elev_info(calls,direction)]
"""


def update_traffic():
    pass


def main(user_floor, elev_floor, total_floors, calls, time, direction):
    outer_traffic = outer.Outer(total_floors)
    inner_traffic = inner.Inner(total_floors)

    for _ in range(3):
        outer_dummy = util.generate_random_user_outer(total_floors)
        outer_traffic.update_table(outer_dummy)  # per day

    usage_info = json.dumps({
        "enter_nums": 4,
        "exit_nums": 0
    })
    calls = [1, 3, 5, 6]
    inner_dummy = util.generate_random_user_inner(total_floors)
    inner_traffic.update_table(elev_floor, usage_info, calls)

    # predict floors
    outer_traffic_predict = outer_traffic.get_prediction(
        elev_floor, user_floor, time)
    inner_traffic_predict = inner_traffic.get_prediction(
        user_floor)

    traffic_predict = dict()
    for floor, time in outer_traffic_predict.items():
        traffic_predict[floor] = time + inner_traffic_predict[floor]

    bottom_floor = min(user_floor, elev_floor)
    above_floor = max(user_floor, elev_floor)

    estimated_time = 0
    cur_floor = bottom_floor
    while cur_floor < above_floor:
        estimated_time = traffic_predict[cur_floor]
        cur_floor += 1

    estimated_traffic = 3

    ret = dict()
    ret["estimated_time"] = estimated_time
    ret["estimated_traffic"] = estimated_traffic

    ret_json = json.dumps(ret)
    return ret_json


if __name__ == "__main__":
    user_floor = 3
    elev_floor = 8
    total_floors = 15
    calls = [2, 5, 7]
    time = 14
    UP = True
    DOWN = False
    print(main(user_floor, elev_floor, total_floors, calls, time, UP))