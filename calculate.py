import numpy as np
import math
from scipy.optimize import root
y_c, z_c, area = 0, 0, 0        # 中点为坐标原点，形心坐标与面积
y_len, z_len, d_a = 0, 0, 0     # 图形的像素与微元面积
img = [0]


def get_centroid(img_mat, scale):
    # 计算并返回形心坐标和面积、图形大小和微元大小
    global y_c, z_c, area
    global y_len, z_len, d_a
    global img

    img = img_mat

    # 确定图形大小
    y_len = img_mat.shape[0]
    z_len = img_mat.shape[1]
    d_a = scale ** 2        # 微元面积大小

    # 计算面积与静矩
    area, s_y, s_z = 0, 0, 0
    for i in range(y_len):
        for j in range(z_len):
            if img_mat[i, j] == 1:
                y = 0.5 * y_len - i
                z = j - 0.5 * z_len
                area += d_a
                s_y = s_y + y * d_a
                s_z = s_z + z * d_a

    # 计算形心坐标
    y_c = s_y / area
    z_c = s_z / area


def moi_origin(img_mat):
    # 计算原始坐标轴的惯性矩与惯性积
    i_y, i_z, i_yz = 0, 0, 0

    # 计算相对于原坐标轴的惯性积与惯性矩
    for i in range(y_len):
        for j in range(z_len):
            if img_mat[i, j] == 1:
                y = 0.5 * y_len - i
                z = j - 0.5 * z_len
                i_y += (pow(z, 2) * d_a)
                i_z += (pow(y, 2) * d_a)
                i_yz += (y * z * d_a)

    # 计算相对于新坐标轴的惯性积与惯性矩
    i_y = i_y - pow(z_c, 2) * area
    i_z = i_z - pow(y_c, 2) * area
    i_yz = i_yz - y_c * z_c * area

    return i_y, i_z, i_yz


def fun(x):
    i_y, i_z, i_yz = moi_origin(img)
    return math.sin(2 * x) * 0.5 * (i_z - i_y) + math.cos(2 * x) * i_yz


def get_theta():
    theta = root(fun, np.array([1.68])).x
    return theta
