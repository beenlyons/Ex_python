from copy import deepcopy
import numpy as np


a = [[1, 2, 1, 1],
     [1, 1, 4, 1],
     [1, 3, 1, 6],
     [1, 7, 2, 5]
]

inner_list = []
res_list = []
for i in range(len(a)):
    for j in range(len(a)):
        inner_list.append(a[j][i])
    copy_list = deepcopy(inner_list)
    res_list.append(copy_list)
    inner_list.clear()
print(res_list)


for i in zip(*a):
    print(i)

print(list(map(list,(zip(*a))))
)

a = np.array(a).T
print(a)
'''
(1, 1, 1, 1)
(2, 1, 3, 7)
(1, 4, 1, 2)
(1, 1, 6, 5)'''