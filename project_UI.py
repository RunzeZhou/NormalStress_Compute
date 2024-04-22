import cv2
import numpy as np
import matplotlib.pyplot as plt
import math


def get_image(real_intensity_matrix, cross_section_matrix, max_stress):  # 获取正应力图像
    # 根据应力矩阵元素大小赋予对应Hue值
    H_matrix = real_intensity_matrix / max_stress * 255
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

    return colored_image_rgb


def add_axis(ctr_y, ctr_z, angle_I, axis_length):  # 在图像上添加主轴坐标
    plt.text(ctr_y, ctr_z, 'O', fontsize=16, color='Black')  # 在形心处添加字母 '0'，表示原点

    angle_I = -1 * angle_I
    # 获取用于添加坐标轴及注释的点的位置
    y1 = ctr_y - axis_length * math.cos(angle_I)
    z1 = ctr_z - axis_length * math.sin(angle_I)
    y2 = ctr_y + axis_length * math.sin(angle_I)
    z2 = ctr_z - axis_length * math.cos(angle_I)
    y3 = ctr_y + axis_length * math.cos(angle_I)
    z3 = ctr_z + axis_length * math.sin(angle_I)
    y4 = ctr_y - axis_length * math.sin(angle_I)
    z4 = ctr_z + axis_length * math.cos(angle_I)

    plt.text(y1, z1, 'Z', fontsize=16, color='Black')  # 标注Z轴
    plt.text(y2, z2, 'Y', fontsize=16, color='Black')  # 标注Y轴

    plt.plot([y2, y4], [z2, z4], color='black', linewidth=1)  # 在原图上添加Y轴
    plt.plot([y1, y3], [z1, z3], color='black', linewidth=1)  # 在原图上添加Z轴


def add_label(scale, pull_max, push_max, angle_I):
    plt.xlabel(f"scale: {scale}\nmax pulling stress: {pull_max}\n"
               f"max pushing stress: {push_max}", fontsize=16)
    # 设置标题显示图像的序号
    plt.title(f'angle = {angle_I}')


def show_image(ctr_y, ctr_z, theta, axis_length, scale, pull_max, push_max,real_intensity_matrix, cross_section_matrix):
    plt.figure(figsize=(10, 10))
    colored_image_rgb = get_image(real_intensity_matrix, cross_section_matrix, max(push_max, pull_max))
    add_axis(ctr_y, ctr_z, theta, axis_length)
    add_label(scale, pull_max, push_max, theta)

    plt.imshow(colored_image_rgb)
    plt.axis('on')  # 不显示坐标轴
    plt.show()


"""
# 设定一系列转角用于测试
theta = [i * (math.pi / 6) for i in range(3)]

for i in theta:
    # 显示图像
    show_image(50, 50, i, 40, '10 mm/mm', 50, 30)
    # 切换间隔
    plt.pause(0.5)  # 暂停0.5秒
"""