import json
from pprint import pprint
from traffic import outer, inner
import util

"""
Input:
    [user_floor, elev_cur_floor, elev_info(calls,direction)]
"""


def main():
    user_floor = 3
    elev_floor = 8
    total_floors = 15
    calls = [2, 5, 7]

    outer_traffic = outer.Outer(total_floors)
    inner_traffic = inner.Inner(total_floors)

    for _ in range(3):
        outer_dummy = util.generate_random_user_outer(total_floors)
        outer_traffic.update_table(outer_dummpy)  # per day

    usage_info = json.dumps({
        "enter_nums": 4,
        "exit_nums": 0
    })
    calls = [1, 3, 5, 6]
    inner_dummy = util.generate_random_user_inner()
    inner_traffic.update_table(floor, usage_info, calls)

    # predict floors
    outer_traffic_predict = outer_traffic.get_prediction(
        user_floor, elev_floor)
    inner_traffic_predict = inner_traffic.get_prediction(
        user_floor, elev_floor)


if __name__ == "__main__":
    main()
