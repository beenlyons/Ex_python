from collections import namedtuple

class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age
user = User(name="aaa", age=18)
print(user.name, user.age)

# namedtuple创建一个类，而不是一个对象,是tuple的子类
# 非常省空间,
Named_user = namedtuple("Named_user", ["name", "age", "height", "edu"])
#user = Named_user(name="bbb", age=17, height=111, "beijing")
# 等价
# user_tuple = ("bbb", 17, 111)
# user = Named_user(*user_tuple, "beijing")
user_dict = {
    "name": "bbb",
    "age": 17,
    "height": 111,
    "edu": "beijing"
}
user = Named_user(**user_dict)
print(user.age, user.name, user.height)
# 当成字典
user_order_dict = user._asdict()
name, age, *asd = user
print(asd)
print(user_order_dict)