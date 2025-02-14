﻿import pandas as pd
import numpy as np
import math
import time
import matplotlib.pyplot as plt
from PIL import Image
import math
import random


dataframe = pd.read_csv("./data.tsp",sep=" ",header=None)
v = dataframe.iloc[:,1:3]


train_v= np.array(v)
train_d=train_v
dist = np.zeros((train_v.shape[0],train_d.shape[0]))

#Tính toán ma trận khoảng cách
for i in range(train_v.shape[0]):
    for j in range(train_d.shape[0]):
        dist[i,j] = math.sqrt(np.sum((train_v[i,:]-train_d[j,:])**2))
"""
s: các thành phố đã đi qua
dist: ma trận khoảng cách giữa các thành phố
sumpath: tổng chiều dài đường dẫn tối thiểu hiện tại
Dtemp: khoảng cách tối thiểu hiện tại
flag: cờ truy cập
"""

i=1
n=train_v.shape[0]
j=0
sumpath=0
s=[]


s.append(0)
start = time.perf_counter()
while True:
    k=1
    Detemp=10000000
    while True:
        l=0
        flag=0
        if k in s:
            flag = 1
        if (flag==0) and (dist[k][s[i-1]] < Detemp):
            j = k;
            Detemp=dist[k][s[i - 1]];
        k+=1
        if k>=n:
            break;
    s.append(j)
    i+=1;
    sumpath+=Detemp
    if i>=n:
        break;
sumpath+=dist[0][j]
end = time.perf_counter()

print("Quảng đường đi = ",sumpath)
for m in range(n):
    print("%s "%(s[m]),end=' ')
print("\nThời gian thực hiện : %s"%(end-start))
