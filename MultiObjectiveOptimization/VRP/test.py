# TODO 500*1000的数组
import numpy as np

arr = [1, 2, 3, 5, 6, 7, 8, 5, 9, 10, 11, 12, 13, 14, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 111, 1, 1, 1, 1, 1, 1, 1, 1, ]
# 最后返回
result = []
population_size = 5
temp = []
for i in range(len(arr)):
    if i != 0 and i % population_size == 0:
        result.append(temp)
        temp = []

    temp.append(arr[i])
# 这里是1000个值（interaion数量）
result.append(temp)
mean_list = []
for aa in result:
    mean_list.append(np.mean(aa))



print(result)
