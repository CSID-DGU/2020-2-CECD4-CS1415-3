from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.http import JsonResponse
import json
import sys
sys.path.append('/Users/uknow/Desktop/종설/2020-1-CECD2-CS1415-1/trafficserver')
import traffic_server as ts
import random
# Create your views here.
# 여러 엘리베이터의 현재 정보를 JSON에 담아 IOS로 보내줌
class elevatorView(APIView):
    renderer_classes = (JSONRenderer, )
    def get(self, request):
        user_floor = 3
        elev_floor = 8
        total_floors = 15
        calls = [2, 5, 7]
        time = 14
        UP = True
        DOWN = False
        e_num = 4
        ts.initialize(e_num, total_floors)
        ts.update_outer(total_floors)
        res = ts.predict(user_floor, elev_floor, total_floors, calls, time, UP)
        print(res)        
        return JsonResponse(res, safe=False)

    def post(self, request):
        request = json.loads(request.body)
        loc = int(request["l"])
        dest = int(request["d"])
        total_floors = 15
        calls = [2, 5, 7]
        time = 14
        UP = True
        DOWN = False
        e_num = 4
        ts.initialize(e_num, total_floors)
        ts.update_outer(total_floors)
        print(loc, dest)
        res = ts.predict(loc, dest, total_floors, calls, time, UP)
        return JsonResponse(res, safe=False)
