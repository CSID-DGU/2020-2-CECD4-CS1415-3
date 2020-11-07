from abc import ABC, abstractmethod


class Traffic(ABC):
    UP = True
    DOWN = False
    OPEN_TIME = 0.5
    CLOSE_TIME = 0.5
    TIME_PER_PERSON = 0.3

    def __init__():
        pass

    @abstractmethod
    def get_prediction():
        pass

    @abstractmethod
    def _calculate_time():
        pass

    @abstractmethod
    def _calculate_traffic():
        pass

    @abstractmethod
    def get_traffic():
        pass

    @abstractmethod
    def update_table():
        pass
