from collections import ChainMap

user_dict1 = {
    "a": "bbb",
    "b": "ccc",
}
user_dict2 = {
    "c": "ddd",
    "d": "eee",
}
# 寻常遍历
# for k, v in user_dict1.items():
#     print(k, v)
# for k, v in user_dict1.items():
#     print(k, v)

# chainmap, 但是这样相同的key只会遍历一次
new_dict = ChainMap(user_dict1, user_dict2)
# 拓展
new_dict = new_dict.new_child({"aa": "aa", "bb": "bb"})
for k, v in new_dict.items():
    print(k, v)

# 在maps中访问修改元素会反馈到原的元素中
print(new_dict.maps)