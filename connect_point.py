# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 17:27:48 2020

@author: jc-chen

用到的库及版本：
numpy:1.18.1
opencv:3.4.2
matplotlib:3.1.3
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt

def get_chain(points,left_point,right_point):
    # 根据横坐标排序，相同横坐标时纵坐标由大到小
    points_down = points.copy()
    points_down[:,1] = -1*points_down[:,1]
    points_down = points_down[np.lexsort(points_down[:,::-1].T)]
    points_down[:,1] = -1*points_down[:,1]
    # 更新上链
    temp_up_chain = []
    temp_down_chain = []
    for point in points:
        if not (point==left_point).all() and not (point==right_point).all():
            vector1 = point - left_point
            vector2 = point - right_point
            if np.cross(vector1,vector2)<0:
                temp_up_chain.append(point)
            else:
                temp_down_chain.append(point)
    up_chain = np.array(temp_up_chain).copy()
    # 更新下链 
    temp_up_chain = []
    temp_down_chain = []        
    for point in points_down:
        if not (point==left_point).all() and not (point==right_point).all():
            vector1 = point - left_point
            vector2 = point - right_point
            if np.cross(vector1,vector2)<0:
                temp_up_chain.append(point)
            else:
                temp_down_chain.append(point)
    down_chain = np.array(temp_down_chain).copy()

    up_x_set = up_chain[:,0]
    up_y_set = up_chain[:,1]
    down_x_set = down_chain[:,0]
    down_y_set = down_chain[:,1]
    return up_x_set,up_y_set,down_x_set,down_y_set
    
plt.close('all')
img = np.zeros((500, 500), np.uint8)
img1 = np.zeros((500, 500), np.uint8)
points = np.array([[215, 220], [460, 225], [300, 400], [235, 465],[460,460],[450,350],[270,94],[215,15],[460,26],[388,138]])#(x,y)
#points = np.array([[215, 220], [215, 100], [250, 220], [250, 100]])
# 根据横坐标排序，相同横坐标时纵坐标由小到大
points = points[np.lexsort(points[:,::-1].T)]
x_set = points[:,0]
y_set = points[:,1]

# 最左下方点
index = np.where(x_set==np.min(x_set))[0]
left_point = np.array([min(x_set),np.max(y_set[index[0]:index[-1]+1])])
# 最右上方点
index = np.where(x_set==np.max(x_set))[0]
right_point = np.array([max(x_set),np.min(y_set[index[0]:index[-1]+1])])

up_x_set,up_y_set,down_x_set,down_y_set = get_chain(points,left_point,right_point)
# 连接上链
last_point = (left_point[0],left_point[1])
for i in range(len(down_x_set)):  
    cv2.line(img,last_point,(down_x_set[i],down_y_set[i]),(255),2)
    last_point = (down_x_set[i],down_y_set[i])
cv2.line(img,last_point,(right_point[0],right_point[1]),(255),2)
# 连接下链
last_point = (left_point[0],left_point[1])
for i in range(len(up_x_set)):  
    cv2.line(img,last_point,(up_x_set[i],up_y_set[i]),(255),2)
    last_point = (up_x_set[i],up_y_set[i])
cv2.line(img,last_point,(right_point[0],right_point[1]),(255),2)

# cv2.line(img,(left_point[0],left_point[1]),(right_point[0],right_point[1]),(255),5)
for point in points:
    img1[point[1],point[0]] = 255
img, contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  
cv2.fillPoly(img, [contours[0].reshape(-1,2)], (255, 255, 255))

plt.subplot(121)
plt.imshow(img1,'gray')
plt.subplot(122)
plt.imshow(img,'gray')


