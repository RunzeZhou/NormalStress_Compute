from PIL import Image
import numpy as np


def image2matrix(img, y_range):
    # 将灰度图片二值化并转化为矩阵并计算比例尺

    # 获得二值化矩阵
    img = img.convert('L')
    im = np.array(img)
    state = 0
    max_y, min_y = 0, 0
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            if im[i, j] < 128:
                im[i, j] = 1
                if state == 0:
                    state = 1
                    min_y = i
                elif (state == 1) and (i > min_y):
                    max_y = i
            else:
                im[i, j] = 0

    # 计算图形比例尺，即每像素多少米
    y_range /= 1000
    scale = y_range / (max_y - min_y)

    return im, scale


def get_info():
    # 获得相关参数
    direction = input("请输入图像路径")
    img = Image.open(direction)
    y_range = float(input("请输入截面y方向高度(mm)：")) / 1000
    img_matrix, scale = image2matrix(img, y_range)
    length = float(input("请输入梁的长度(mm)：")) / 1000

    # 力的相关参数
    force_pos = list(map(float, input("请输入力的作用点的x、y、z坐标(mm)，(x,y,z)：").split(',')))
    for i in force_pos:
        i /= 1000
    force_dir = list(map(float, input("请输入力的作用点的x、y、z分量(N)，(x,y,z)：").split(',')))

    return img_matrix, scale, length, force_pos, force_dir
