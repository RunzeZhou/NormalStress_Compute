import numpy as np
import matplotlib.pyplot as plt
import imageio
from io import BytesIO
import math
import calculate
import cv2


def get_image(real_intensity_matrix, cross_section_matrix, pull_max, push_max):  # 获取正应力图像
    # 根据应力矩阵元素大小赋予对应Hue值
    H_matrix = (real_intensity_matrix - push_max) / (pull_max - push_max) * 255
    H_matrix_unit8 = H_matrix.astype(np.uint8)  # 确保数据类型是uint8

    # 根据元素值，使用cv2.applyColorMap给矩阵上色
    colored_image_bgr = cv2.applyColorMap(H_matrix_unit8, cv2.COLORMAP_JET)
    #  将红色与蓝色对调，使得应力大的区域显示红色，应力小的区域显示蓝色
    colored_image_rgb = cv2.cvtColor(colored_image_bgr, cv2.COLOR_BGR2RGB)

    #  使截面之外的区域显示为白色
    for i in range(0, calculate.y_len):
        for j in range(0, calculate.z_len):
            if cross_section_matrix[i, j] == 0:
                colored_image_rgb[i, j] = (255, 255, 255)

    return colored_image_rgb


def add_axis(ax, ctr_y, ctr_z, angle_I, axis_length):  # 在图像上添加主轴坐标
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

    plt.text(y1, z1, 'Z', fontsize=8, color='Black')  # 标注Z轴
    plt.text(y2, z2, 'Y', fontsize=8, color='Black')  # 标注Y轴

    plt.plot([y2, y4], [z2, z4], color='black', linewidth=1)  # 在原图上添加Y轴
    plt.plot([y1, y3], [z1, z3], color='black', linewidth=1)  # 在原图上添加Z轴


# 定义一个函数来在图像上添加注释并返回图像数据
def image_with_annotation(image_data, annotation_text, annotation_position, ctr_y, ctr_z, angle_I, axis_length):
    # 生成应力图像
    fig, ax = plt.subplots(figsize=(2, 2), dpi=80)  # dpi参数用于设置图像分辨率
    ax.imshow(image_data)

    # 添加坐标轴
    add_axis(ax, ctr_y, ctr_z, angle_I, axis_length)
    # 添加标注
    ax.text(*annotation_position, annotation_text, fontsize=6, color='black',
            bbox=dict(facecolor='red', alpha=0.5))
    ax.axis('off')
    fig.canvas.draw()

    # 使用BytesIO捕获图像数据
    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    buf.seek(0)
    image = imageio.imread(buf)
    plt.close(fig)
    return image


def save_images_to_gif(images, filename, fps):
    imageio.mimsave(filename, [img for img in images], fps=fps)


def img_generator():
    # 生成一个100x100的全0矩阵
    matrix = np.zeros((100, 100))

    # 获取中间50x50的区域的索引
    start_row, end_row = 25, 75
    start_col, end_col = 25, 75

    # 将中间50x50的区域替换为0到50的随机数
    matrix[start_row:end_row, start_col:end_col] = np.random.randint(0, 51, (50, 50))

    return matrix


def gif_generator(x_len, theta, scale, max_pull, max_push, binary_matrix, stress_matrix_list):
    x_list = [i * x_len / 100 for i in range(100)]

    image_data_list = get_image(stress_matrix_list, binary_matrix, max_pull, max_push)
    height, width = image_data_list[0].shape
    label_list = [f"x = {x}mm\nscale = {scale}px/1mm"
                  for x, max_pull, max_push in zip(image_data_list)]
    position_list = [(width, height) for i in range(60)]  # 假设所有图像的注释位置相同

    # 对每组图像数据和注释调用image_with_annotation函数
    annotated_images = [image_with_annotation(img, label, pos, height / 2, width / 2, theta, 39)
                        for img, label, pos in zip(image_data_list, label_list, position_list)]

    # 将图像列表保存为GIF
    save_images_to_gif(annotated_images, 'my_images.gif', fps=10)

