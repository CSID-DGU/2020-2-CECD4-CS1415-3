import json
from pprint import pprint

from traffic.trafficABC import Traffic
from typing import TypeVar

JSON = TypeVar("json")


class Inner(Traffic):
    def __init__(self, total_floor: int, num_of_elevs: int):
        self.lookup = dict()

        self.lookup["num"] = 0
        self.lookup["users"] = dict()
        self.uid_set = set()

    def get_prediction(self, user_floor: int, target_floor: int) -> dict:
        pass

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

        def update_probs(floor: int, deleted_info: list[list]) -> None:
            probs = sorted(
                list(map(lambda x: x[0], deleted_info)), reverse=True)

            users = self.lookup["users"]

            for prob in probs:
                need_to_change = int(1/prob) - 1
                for user, prob_table in user.items():
                    if not need_to_chage:
                        break
                    if prob_table[floor] == prob:
                        users[user][floor] = 1 / ((1/prob) + 1)

        deleted_info = find_uids(exit_nums, floor-1)

        for _, uid in deleted_info:
            self.uid_set.remove(uid)

        update_probs(floor-1, deleted_info)

    def update_table(self, floor: int, elevetor_user: JSON):
        """ update lookup
        args:
            elevator_user, JSON: human after door closed
            {"enter_nums": num, "exit_nums": num}
        """

        elevator_user_dict = json.loads(elevator_user)

        enter_nums = elevator_user_dict["enter_nums"]
        exit_nums = elevator_user_dict["exit_nums"]

        self.lookup["nums"] += (enter_nums - exit_nums)

        self._exit_handler(exit_nums, floor)

        assert lookup["nums"] == len(
            self.lookup["users"]), print("Update operates fail")
