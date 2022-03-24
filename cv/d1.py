import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import json
import random

ticArray=[]
channelArr=[]
dataArr=[]
with open('tic','r',encoding='utf8')as fp:
    ticArray = json.load(fp)
with open('channel','r',encoding='utf8')as fp:
    channelArr = json.load(fp) 
with open('data','r',encoding='utf8')as fp:
    dataArr = json.load(fp) 

print("TICTime len=", len(ticArray))
print("MZChannel len=", len(channelArr))
print("MZChannel len=", len(dataArr))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
x = ticArray
y = channelArr
X, Y = np.meshgrid(x, y)
zs = np.array(dataArr)

Z = zs.reshape(X.shape)

ax.plot_surface(X, Y, Z)

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()