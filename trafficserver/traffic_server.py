from traffic import outer, inner
import util

if __name__ == "__main__":
    floors = 15
    # initiate traffics
    outer_traffic = outer.Outer(floors)
    # inner_traffic = inner.Inner()

    # create dummy data for test
    random_input = util.generate_random_user_outer(floors)
    for _ in range(3):
        outer_traffic.update_table(random_input)  # per day

    # predict floors
    outer_traffic_dict = outer_traffic.get_prediction(3, 8)
    # inner -> {eid: {floor: estimated_time}}
    inner_traffic_dict = outer_traffic_dict
    # inner_traffic.get_prediction()  # [floor: estimated_time]

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
