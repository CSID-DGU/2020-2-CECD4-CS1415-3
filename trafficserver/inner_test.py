from pprint import pprint
import json
from traffic import inner

total_floor = 8
test = inner.Inner(total_floor)


floor = 4
usage_info = {
    "enter_nums": 4,
    "exit_nums": 0
}
calls = [1, 3, 5, 6]

calls = [1, 3, 5, 6]

print("=============FIRST UPDATE===============")
print(f"User enters at floor {floor}")
print("Enter & Exit info")
print(f"  Enter num: {usage_info['enter_nums']}")
print(f"  Exit num: {usage_info['exit_nums']}")
print(f"Current calls: {calls}")

usage_info = json.dumps(usage_info)

print("*"*40)
test.update_table(floor, usage_info, calls)
pprint(test.get_lookup())

print("=============FIRST RESULT ===============")
pprint(test.get_prediction(floor))

floor = 5
usage_info = {
    "enter_nums": 1,
    "exit_nums": 3
}
calls = [1, 2, 3, 6]


print("=============SECOND UPDATE===============")
print(f"User enters at floor {floor}")
print("Enter & Exit info")
print(f"  Enter num: {usage_info['enter_nums']}")
print(f"  Exit num: {usage_info['exit_nums']}")
print(f"Current calls: {calls}")

usage_info = json.dumps(usage_info)

print("*"*40)
test.update_table(floor, usage_info, calls)
pprint(test.get_lookup())

print("=============SECOND RESULT ===============")
pprint(test.get_prediction(floor))
