from traffic import outer  # , inner
import util

if __name__ == "__main__":
    floors = 15
    # initiate traffics
    outer_traffic = outer.Outer(floors)
    # inner_traffic = inner.Inner()  # what args

    random_input = util.generate_random_user_outer(floors)
    # predict floors
    outer_traffic.get_prediction()  # [floor: estimated_time] , cur ~ target
    # inner_traffic.get_prediction()  # [floor: estimated_time]

    # predict time which will be returned to main
    # stop_floor = []
    # for outer, inner in zip(outer_traffic, inner_traffic):
    #     pass

    # deal with it in main file
    for _ in range(3):
        outer_traffic.update_table(random_input)  # per day
    # inner_traffic.update_table()  # per ??
