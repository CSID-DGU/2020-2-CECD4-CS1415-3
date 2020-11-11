from pprint import pprint
from traffic import outer, inner
import util

"""
Input:
    [user_floor, elev_cur_floor, elev_info(calls,direction)]
"""
if __name__ == "__main__":
    user_floor = 3
    elev_floor = 8
    total_floors = 15
    calls = [2, 5, 7]

    # initiate
    outer_traffic = outer.Outer(total_floors)
    inner_traffic = inner.Inner(total_floors)

    # create dummy data for test
    outer_dummpy = util.generate_random_user_outer(total_floors)
    for _ in range(3):
        outer_traffic.update_table(outer_dummpy)  # per day

    # INNER TEST

    util.generate_random_user_inner()
    ###

    # predict floors
    outer_traffic_predict = outer_traffic.get_prediction(
        user_floor, elev_floor)
    inner_traffic_predict = inner_traffic.get_prediction(
        user_floor, elev_floor)

    # traffic_dict = dict()
    # for floor, outer_time in outer_traffic_dict.items():
    #     inner_time = inner_traffic_dict[floor]
    #     traffic_dict[floor] = inner_time + outer_time
