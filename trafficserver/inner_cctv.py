from pprint import pprint
from count.run import run
from traffic import inner

total_floor = 8
test = inner.Inner(total_floor)


floor = 4
usage_info = run("1.mp4")
calls = [1, 3]

print("=============FIRST UPDATE===============")
print(f"User enters at floor {floor}")
print("Enter & Exit info")
print(f"  Enter num: {usage_info['enter']}")
print(f"  Exit num: {usage_info['exit']}")
print(f"Current calls: {calls}")

print("*"*40)
test.update_table(floor, usage_info, calls)
pprint(test.get_lookup())

print("=============FIRST RESULT ===============")
pprint(test.get_prediction(floor))

floor = 3
usage_info = run("2.mp4")
calls = [1]


print("=============SECOND UPDATE===============")
print(f"User enters at floor {floor}")
print("Enter & Exit info")
print(f"  Enter num: {usage_info['enter']}")
print(f"  Exit num: {usage_info['exit']}")
print(f"Current calls: {calls}")


print(usage_info)
print("*"*40)
test.update_table(floor, usage_info, calls)
pprint(test.get_lookup())

print("=============SECOND RESULT ===============")
pprint(test.get_prediction(floor))

floor = 1
usage_info = run("3.mp4")
calls = [2, 3]


print("=============THIRD UPDATE===============")
print(f"User enters at floor {floor}")
print("Enter & Exit info")
print(f"  Enter num: {usage_info['enter']}")
print(f"  Exit num: {usage_info['exit']}")
print(f"Current calls: {calls}")


print(usage_info)
print("*"*40)
test.update_table(floor, usage_info, calls)
pprint(test.get_lookup())

print("=============THIRD RESULT ===============")
pprint(test.get_prediction(floor))

floor = 2
usage_info = run("4.mp4")
calls = [3]


print("=============FOURTH UPDATE===============")
print(f"User enters at floor {floor}")
print("Enter & Exit info")
print(f"  Enter num: {usage_info['enter']}")
print(f"  Exit num: {usage_info['exit']}")
print(f"Current calls: {calls}")


print(usage_info)
print("*"*40)
test.update_table(floor, usage_info, calls)
pprint(test.get_lookup())

print("=============FOURTH RESULT ===============")
pprint(test.get_prediction(floor))

floor = 3
usage_info = run("5.mp4")
calls = []


print("=============FOURTH UPDATE===============")
print(f"User enters at floor {floor}")
print("Enter & Exit info")
print(f"  Enter num: {usage_info['enter']}")
print(f"  Exit num: {usage_info['exit']}")
print(f"Current calls: {calls}")


print(usage_info)
print("*"*40)
test.update_table(floor, usage_info, calls)
pprint(test.get_lookup())

print("=============FOURTH RESULT ===============")
pprint(test.get_prediction(floor))
