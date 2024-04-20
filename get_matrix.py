import cv2
import numpy as np
import matplotlib.pyplot as plt

cross_section_matrix = np.zeros((100, 100))  # 这里应该是 np.zeros((100, 100)) 或者 np.zeros((100, 100))
for i in range(25, 75):  # 将矩阵中部元素赋值为1，代表截面所在区域
    for j in range(25, 75):
        cross_section_matrix[i, j] = 1

intensity_list1 = np.arange(1, 10001)  # 代表应力范围
real_intensity_matrix = np.reshape(intensity_list1, (100, 100))  # 生成100×100的应力矩阵

# 根据应力矩阵元素大小赋予对应Hue值
H_matrix = real_intensity_matrix / 10000 * 255
H_matrix_unit8 = H_matrix.astype(np.uint8)  # 确保数据类型是uint8

# 根据元素值，使用cv2.applyColorMap给矩阵上色
colored_image_bgr = cv2.applyColorMap(H_matrix_unit8, cv2.COLORMAP_JET)
#  将红色与蓝色对调，使得应力大的区域显示红色，应力小的区域显示蓝色
colored_image_rgb = cv2.cvtColor(colored_image_bgr, cv2.COLOR_BGR2RGB)

#  使截面之外的区域显示为白色
for i in range(0, 100):
    for j in range(0, 100):
        if cross_section_matrix[i, j] == 0:
            colored_image_rgb[i, j] = (255, 255, 255)

# 设定截面形心
ctr_y = 50
ctr_z = 50

plt.text(ctr_y, ctr_z, 'O', fontsize=16, color='Black')  # 在形心处添加字母 '0'，表示原点
plt.text(ctr_y, ctr_z - 40, 'Y', fontsize=16, color='Black')  # 在形心处添加字母 'Y'，表示Y坐标
plt.text(ctr_y - 40, ctr_z, 'Z', fontsize=16, color='Black')  # 在形心处添加字母 'Z'，表示Z坐标

plt.plot([ctr_y, ctr_y], [ctr_z - 40, ctr_z + 40], color='black', linewidth=1)  # 在原图上添加Y轴
plt.plot([ctr_y - 40, ctr_y + 40], [ctr_z, ctr_z], color='black', linewidth=1)  # 在原图上添加Z轴




