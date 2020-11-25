from pprint import pprint
from traffic import outer
from argparse import ArgumentParser
import util

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-s", "--show", type=bool, default=False)
    args = parser.parse_args()

    user_floor = 3
    elev_floor = 8
    total_floors = 15
    calls = [2, 5, 7]

    outer_traffic = outer.Outer(total_floors)

    # once per day
    for _ in range(3):
        outer_dummpy = util.generate_random_user_outer(total_floors, args.show)
        outer_traffic.update_table(outer_dummpy)

    time = 4
    print(f"TIME: {time}")
    outer_traffic_predict = outer_traffic.get_prediction(
        user_floor, elev_floor, time)
    pprint(outer_traffic_predict)
