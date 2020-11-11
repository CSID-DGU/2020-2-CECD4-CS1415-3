from pprint import pprint
import util
import json
from traffic import inner

total_floor = 8
test = inner.Inner(total_floor)


floor = 4
usage_info = {
    "enter_nums": 4,
    "exit_nums": 0
}

calls = [1, 3, 4, 5, 6]
print(f"User enters at floor {floor}")
print("Enter & Exit info")
print(f"Enter num: {usage_info['enter_nums']}")
print(f"Exit num: {usage_info['exit_nums']}")
print(f"Current calls: {calls}")

usage_info = json.dumps(usage_info)

test.update_table(floor, usage_info, calls)
pprint(test.get_lookup())
