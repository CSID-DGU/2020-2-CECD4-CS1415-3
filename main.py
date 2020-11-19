from trafficserver import traffic_server

if __name__ == "__main__":
    user_floor = 3
    elev_floor = 8
    total_floors = 15
    calls = [2, 5, 7]
    time = 14
    UP = True
    DOWN = False
    traffic_server.initalize(4, 9)
    # print(traffic_server.traffic(user_floor,
    #                             elev_floor, total_floors, calls, time, UP))
