from traffic import outer, inner  # , inner

if __name__ == "__main__":
    # initiate traffics
    outer_traffic = outer.Outer(15, 4)
    # inner_traffic = inner.Inner()  # what args

    # predict floors
    # outer_traffic.get_prediction()  # [floor: estimated_time]
    # inner_traffic.get_prediction()  # [floor: estimated_time]

    # predict time which will be returned to main
    # stop_floor = []
    # for outer, inner in zip(outer_traffic, inner_traffic):
    #     pass

    # deal with it in main file
    # outer_traffic.update_table()  # per day
    # inner_traffic.update_table()  # per ??
