from pprint import pprint
from traffic import outer
import util

if __name__ == "__main__":
    user_floor = 3
    elev_floor = 8
    total_floors = 15
    calls = [2, 5, 7]

    outer_traffic = outer.Outer(total_floors)

    for _ in range(3):
        outer_dummpy = util.generate_random_user_outer(total_floors)
        outer_traffic.update_table(outer_dummpy)

    outer_traffic_predict = outer_traffic.get_prediction(
        user_floor, elev_floor)
    pprint(outer_traffic_predict)
