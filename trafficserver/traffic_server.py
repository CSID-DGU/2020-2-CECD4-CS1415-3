import pickle
import os
from pathlib import Path
import json
from pprint import pprint
from traffic import outer, inner
import util


def update_traffic():
    pass


def initialize(e_num, total_floors):
    nums = list(range(e_num))

    outers = dict()
    inners = dict()
    pwd = Path(os.path.dirname(__file__)).absolute()
    pwd.mkdir(parents=True, exist_ok=True)

    for eid in nums:
        outers[eid], inners[eid] = initialize_traffic(eid, total_floors)

    with open(pwd/"data/outer.pickle", "wb") as f:
        pickle.dump(outers, f)

    with open(pwd/"data/inner.pickle", "wb") as f:
        pickle.dump(inners, f)


def traffics(e_num, total_floors):
    traffics = []

    while True:
        for eid in nums:
            traffics.append(each_traffic(user_floor, elev_floor, total_floors,
                                         calls, time, UP, outers[eid], inners[eid], eid))


def initialize_traffic(eid, total_floors):
    return outer.Outer(total_floors), inner.Inner(total_floors)


def update_outer():
    pwd = Path(os.path.dirname(__file__)).absolute()
    outer_traffics = None
    with open(pwd/"data/outer.pickle", "rb") as f:
        outer_traffics = pickle.load(f)

    outers = dict()
    enums = len(outer_traffics)
    for enum in range(enums):
        outer_traffic = outer_traffics[enum]
        outer_dummy = util.generate_random_user_outer(total_floors)
        outer_traffic.update_table(outer_dummy)
        outers[enum] = outer_traffic

    with open(pwd / "data/outer.pickle", "wb") as f:
        pickle.dump(outers, f)


def predict(user_floor, elev_floor, total_floors, calls, time, direction):
    outer_traffics = None
    inner_traffics = None

    pwd = Path(os.path.dirname(__file__)).absolute()

    outer_traffic = None
    inner_traffics = None

    with open(pwd/"data/outer.pickle", "rb") as f:
        outer_traffics = pickle.load(f)
    enums = len(outer_traffics)
    eids = list(range(enums))

    with open(pwd/"data/inner.pickle", "rb") as f:
        inner_traffics = pickle.load(f)

    usage_info = json.dumps({
        "enter_nums": 4,
        "exit_nums": 0
    })

    rets = dict()

    for eid in eids:
        outer_traffic = outer_traffics[eid]
        inner_traffic = inner_traffics[eid]

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

        time = 0
        cur_floor = bottom_floor
        while cur_floor < above_floor:
            time = traffic_predict[cur_floor]
            cur_floor += 1

        estimated_traffic = 3

        ret = dict()
        ret["estimated_time"] = time
        ret["estimated_traffic"] = estimated_traffic
        #ret = json.dumps(ret)
        rets[eid+1] = ret
    ret_dic = dict()
    for k, v in sorted(rets.items(), key=lambda x: x[0]):
        ret_dic[k] = v
    return ret_dic


if __name__ == "__main__":
    user_floor = 3
    elev_floor = 8
    total_floors = 15
    calls = [2, 5, 7]
    time = 14
    UP = True
    DOWN = False
    e_num = 4
    initialize(e_num, total_floors)
    update_outer()
    print(predict(user_floor, elev_floor, total_floors, calls, time, UP))
