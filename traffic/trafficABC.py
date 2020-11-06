from abc import ABC, abstractmethod


class Traffic(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_prediction(**kwargs):
        pass

    @abstractmethod
    def _calculate_time(**kwargs):
        pass

    @abstractmethod
    def _calculate_traffic(**kwargs):
        pass

    @abstractmethod
    def get_traffic(**kwargs):
        pass

    @abstractmethod
    def get_time(**kwargs):
        pass

    @abstractmethod
    def update_table(**kwargs):
        pass
