

# 내부 트래픽 정보 : 인원, 눌려있는 층
# 
# 각 호기에 대해 눌려있는지 여부를 정보로 담고 있어야 함(True, False)
# 
# estimated_time : get_prediction함수 통해서 눌려있는 각 층 정보 계산 후 current부터 target floor까지 멈춰있을 시간 계산

import json
from pprint import pprint

from traffic.trafficABC import Traffic
from typing import TypeVar

JSON = TypeVar("json")


class Inner(Traffic):
    def __init__(self, total_floor: int, num_of_elevs: int):
        self.elevatorStatus = dict()

        for elev_id in range(1, num_of_elevs+1):
            self.elevatorStatus[elev_id] = dict()
            self.elevatorStatus[elev_id][Traffic.UP] = dict()
            self.elevatorStatus[elev_id][Traffic.DOWN] = dict()

            for floor_id in range(1, total_floor+1):
                self.elevatorStatus[elev_id][Traffic.UP][floor_id] = 0
                self.elevatorStatus[elev_id][Traffic.DOWN][floor_id] = 0

    def get_prediction(self, current_floor: int, target_floor: int) -> JSON:
        self._calculate_time()      # 멈춰있을 시간 계산
        self._calculate_traffic()   # 탈 수 있는지 여부에 대해 알려주기 위해 traffic 정보 계산해야함
        pass

    def _calculate_time(self, current, target):
        '''
        ret = dict()
        request_json = json.loads(calc_request)

        for i in range(1, num_of_elevs+1):
            stopped_time = 0
            # 엘리베이터가 상승 중

            # 엘리베이터가 하강 중
            for floor in range()
        '''
        pass

    def _calculate_traffic(self):
        pass

    def get_traffic():
        pass

    def get_time():
        pass

    def update_table(self, target_call: JSON):#When call occurs(in elevator)
        """ update elevatorTable
        args:
            direction => False : Going Down, True : Going Up
            time_user, JSON: target_call data which occurs by passengers in Elevator(target_floor, elev_id)
            {elev_id: [direction:bool, current_floor:int, target_floor:int]}
            {1 :[False, 3], 2: [True, 5] ...}
        """
        call_json = json.loads(target_call)
        for elev_id, info in call_json.items():
            direction, target_floor = info
            print(elev_id)
            pprint(self.elevatorStatus[2])
            exit()   
            #self.elevatorStatus[elev_id][direction][target_floor] += 1
        
        pprint(self.elevatorStatus)