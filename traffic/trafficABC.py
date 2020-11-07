from abc import ABC, abstractmethod


class Traffic(ABC):
    UP = True
    DOWN = False

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
    def get_time():
        pass

    @abstractmethod
    def update_table():
        pass
