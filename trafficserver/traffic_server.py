from traffic import outer, inner

if __name__ == "__main__":
    outer_traffic = outer.Outer(15, 4)
    inner_traffic = inner.Inner()  # what args

    """
    predict num_of_people
    """
    outer_traffic.get_prediction()  # [floor: estimated_time]
    inner_traffic.get_prediction()  # [floor: estimated_time]

    stop_floor = []
    for outer, inner in zip(outer_traffic, inner_traffic):
        pass

    outer_traffic.update_table()  # per day
    inner_traffic.update_table()  # per ??
