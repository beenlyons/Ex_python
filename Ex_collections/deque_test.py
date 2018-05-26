from collections import deque
# 双端队列 deque是线程安全的，由GIL保证的，list是线程不安全的

# user_list = ["boddy", "boddy2"]
# user_list.pop()
# print(user_list)

# 可以使用可迭代对象初始化
# 尽量用来保存相同类型的数据
# user_list = deque({
#     "De": 12,
#     "dd": 14,
# })

# 浅拷贝只拷贝元素，可变对象的索引没有变
user_list = deque(["bbb", ["bbb1", "bbb2"], "bbb3"])
user_list2 = user_list.copy()
print(user_list, user_list2)
print(id(user_list), id(user_list2))
user_list[1].append("asd")
print(user_list, user_list2)
print(id(user_list), id(user_list2))
# 在原deque上修改，不返回
user_list2.extendleft(user_list)
print(user_list2)







