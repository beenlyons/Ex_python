from collections import Counter
# 可用任何可迭代对象进行统计
users = ["asd", "aaa", "bbb", "ccc", "aaa", "asd", "aaa", "bbb", "aaa"]
user_counter = Counter(users)
print(user_counter)
# 也是传递可迭代对象
user_counter.update(user_counter)
print(user_counter)
# top n,用的是堆的数据结构
print(user_counter.most_common(3))

prime_factors = Counter({2: 2, 3: 3, 17: 1})
for i in prime_factors.elements():
    print(i)