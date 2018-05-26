# 不可变，iterable
name_tuple = ("body", "body2")
# name[0] = 3报错， tuple不可变
for name in name_tuple:
    print(name)
# 拆包
user_tuple = ("name", 29, 175, "beijing")
name, age, height ,*other= user_tuple
print(name, age, height)
name, *other= user_tuple
print(name, other)
# tuple 不是绝对不可变的,不建议将可变对象放入不可变对象中去
name_tuple = ("name", [29, 175])
name_tuple[1].append("beijng")
print(name_tuple)

user_info_dict = {}
user_info_dict[user_tuple] = "123"
print(user_info_dict)

# immutable的重要性，
# 1.性能优化，指出元素全部为immutable的tuple会作为常量在编译时确定，因此产生如此显著的速度差异
# 2.线程安全
# 3.可以作为dict的key
# 4.拆包特性
# 5.如果拿C语言类比，tuple就是struct，list是array