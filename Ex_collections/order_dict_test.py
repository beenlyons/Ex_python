from collections import OrderedDict


user_dict = OrderedDict()
user_dict["asd"] = 0
user_dict["b"] = "2"
user_dict["c"] = "3"
user_dict["a"] = "1"
# 删除第一个
print(user_dict.popitem(last=False))
# 移动到最后
user_dict.move_to_end("b")
print(user_dict)