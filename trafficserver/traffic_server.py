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
    outer_dummpy = util.generate_random_user_outer(floors)
    for _ in range(3):
        outer_traffic.update_table(outer_dummpy)  # per day

    # predict floors
    outer_traffic_dict = outer_traffic.get_prediction(user_floor, elev_floor)
    inner_traffic_dict = inner_traffic.get_prediction(
        user_floor, elev_floor, calls)

    traffic_dict = dict()
    for floor, outer_time in outer_traffic_dict.items():
        inner_time = inner_traffic_dict[floor]
        traffic_dict[floor] = inner_time + outer_time

    # util.calc_total(traffic_dict)

    # predict time which will be returned to main
    # stop_floor = []
    # for outer, inner in zip(outer_traffic, inner_traffic):
    #     pass

    # deal with it in main file
    # inner_traffic.update_table()  # per ??
