from collections import defaultdict
from collections import Counter

user_dict = {}
users = ["asd", "aaa", "bbb", "ccc", "aaa", "asd", "aaa", "bbb", "aaa"]
# 常规做法
# for user in users:
#     if user not in user_dict:
#         user_dict[user] = 1
#     else:
#         user_dict[user] += 1
# print(user_dict)

# setdefault做法
# for user in users:
#     user_dict.setdefault(user, 0)
#     user_dict[user] +=1
# print(user_dict)

# defaultdict
default_dict = defaultdict(int)
for user in users:
    default_dict[user] +=1
print(default_dict)

# 传递字典到defaudict
def gen_default():
    return {
        "name":"",
        "nums":0
    }
gen_dict = defaultdict(gen_default)
pass



