import json
from pprint import pprint
from typing import List

from traffic.trafficABC import Traffic
from typing import TypeVar

JSON = TypeVar("json")


class Inner(Traffic):
    def __init__(self, total_floor: int):
        self.lookup = dict()

        self.lookup["nums"] = 0
        self.lookup["users"] = dict()

        self.uid_set = set()
        self.total_floor = total_floor

    def get_prediction(self, user_floor: int, target_floor: int) -> dict:
        ret = dict()
        for floor in range(1, self.total_floor+1):
            ret[floor] = 0

        users = self.lookup["users"]
        for user, probs in users.items():
            for idx, prob in enumerate(probs):
                ret[idx+1] += prob

        return ret

    def _calculate_time(self, current, target):
        pass

    def _calculate_traffic(self):
        pass

    def _exit_handler(self, exit_nums: int, floor: int):
        def find_uids(nums, floor):
            users = self.lookup["users"]

            assert len(users) >= nums, print(
                "try to exit while there's not enough people")

            stack = []

            for uid, probs in users.items():
                prob = probs[floor]

                if not stack:
                    stack.append([prob, uid])
                    continue

                if prob > stack[0][0]:
                    if len(stack) >= nums:
                        stack.pop()
                        stack.append([prob, uid])
                    stack.append([prob, uid])

                stack.sort(key=lambda x: -x[0])

            for _, uid in stack:
                users.pop(uid, None)

            return stack

        def update_probs(floor: int, deleted_info: List[List]) -> None:
            THRESHOLD = 0.005
            users = self.lookup["users"]

            for user, probs in users.items():
                if probs[floor] > THRESHOLD:
                    for idx, prob in enumerate(probs):
                        if prob > THRESHOLD:
                            probs[idx] = 1/((1/prob) + 1)

            for user, probs in users.items():
                if sum(probs) > 1.0001 and sum(probs) < 0.9999999:
                    raise ValueError("Sum should be 1")

        floor -= 1
        deleted_info = find_uids(exit_nums, floor)

        for _, uid in deleted_info:
            self.uid_set.remove(uid)

        update_probs(floor, deleted_info)

    def _enter_handler(self, enter_nums, calls):
        used_uids = self.uid_set
        uid = 0

        while enter_nums:
            while uid in used_uids:
                uid += 1

            users = self.lookup["users"]
            used_uids.add(uid)
            users[uid] = [0 for _ in range(self.total_floor)]
            for call in calls:
                users[uid][call - 1] = 1 / len(calls)

            enter_nums -= 1

    def update_table(self, floor: int, elevator_user: JSON, calls: list):
        """ update lookup
        args:
            floor: current floor
            elevator_user: human after door closed {"enter_nums": num, "exit_nums": num}
            calls: [1, 3, 4, 5, 6]
        """

        elevator_user_dict = json.loads(elevator_user)

        enter_nums = elevator_user_dict["enter_nums"]
        exit_nums = elevator_user_dict["exit_nums"]

        self.lookup["nums"] += (enter_nums - exit_nums)

        if floor in calls:
            calls.remove(floor)
        self._exit_handler(exit_nums, floor)
        self._enter_handler(enter_nums, calls)

        assert self.lookup["nums"] == len(
            self.lookup["users"]), print("Update operates fail")

    def get_lookup(self):
        return self.lookup
