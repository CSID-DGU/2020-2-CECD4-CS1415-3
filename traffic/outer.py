from traffic.trafficABC import Traffic
from typing import TypeVar

JSON = TypeVar("json")


class Outer(Traffic):
    def __init__(self):
        print("outer init")

    def get_prediction(self, current_floor: int, target_floor: int) -> JSON:
        pass

    def _calculate_time(**kwargs):
        pass

    def _calculate_traffic(**kwargs):
        pass

    def get_traffic(**kwargs):
        pass

    def get_time(**kwargs):
        pass

    def update_table(**kwargs):
        pass
