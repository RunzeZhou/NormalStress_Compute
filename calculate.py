import numpy as np
from math import sin, cos, atan, sqrt
y_c, z_c, area = 0, 0, 0        # 中点为坐标原点，形心坐标与面积
y_len, z_len, d_a = 0, 0, 0     # 图形的像素与微元面积
theta, i_yp, i_zp = 0, 0, 0     # 惯性主轴的旋转角与相对于惯性主轴的惯性矩


def get_centroid(img_mat, scale):
    # 计算并返回形心坐标和面积、图形大小和微元大小
    global y_c, z_c, area
    global y_len, z_len, d_a

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
                z = 0.5 * z_len - j
                area += d_a
                s_y += y * d_a * scale
                s_z += z * d_a * scale

    # 计算形心坐标
    y_c = s_y / area
    z_c = s_z / area

    return y_c, z_c, area, y_len, z_len, d_a


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


def get_theta_moip(img_mat):
    # 计算形心主轴的转动角度与形心主矩
    global theta, i_yp, i_zp

    i_y, i_z, i_yz = moi_origin(img_mat)
    theta = 0.5 * (atan(-(i_yz / i_z - i_y)))
    i_yp = 0.5 * (i_y + i_z) + 0.5 * sqrt(pow((i_y - i_z), 2) + 4 * pow(i_yz, 2))
    i_zp = 0.5 * (i_y - i_z) - 0.5 * sqrt(pow((i_y - i_z), 2) + 4 * pow(i_yz, 2))
    return theta, i_yp, i_zp


def force_normalize(force_pos, force_dir):
    # 获得作用力在其作用截面上，相对于形心主轴的三个力的分量与两个力矩分量
    x_o, y_o, z_o = force_pos[0], force_pos[1], force_pos[2]
    fx_o, fy_o, fz_o = force_dir[0], force_dir[1], force_dir[2]
    x = x_o
    y = (y_o - y_c) * cos(theta) - (z_o - z_c) * sin(theta)
    z = (y_o - y_c) * sin(theta) - (z_o - z_c) * cos(theta)
    fx = fx_o
    fy = fy_o * cos(theta) - fz_o * sin(theta)
    fz = fz_o * cos(theta) + fy_o * sin(theta)
    my = - fy * z + fx * y
    mz = fz * y - fx * z
    return x, [fx, fy, fz], [my, mz]


def get_coordinate(i, j, scale):
    # 计算某一点相对于惯性主轴的坐标
    y = (0.5 * y_len - i) * scale
    z = (j - 0.5 * z_len) * scale
    y1 = (y - y_c) * cos(theta) - (z - z_c) * sin(theta)
    z1 = (y - y_c) * sin(theta) - (z - z_c) * cos(theta)
    return y1, z1


def single_n_stress(fx, my, mz, i, j, scale):
    # 计算截面上某一点的正应力
    y, z = get_coordinate(i, j, scale)
    ns = fx / area - (mz * y / i_zp) + (my * z / i_yp)
    return ns


def calculate_stress_distribute(x, force, moment, cal_x, scale):
    # 计算截面的正应力分布
    n_stress_mat = np.zeros((y_len, z_len))
    fx, fy, fz = force[0], force[1], force[2]
    my, mz = moment[0], moment[1]

    if cal_x > x:
        return n_stress_mat         # 如果研究的截面在作用力作用范围之外，那么返回一个全零的矩阵
    else:
        my = my - fz * (x - cal_x)  # 将作用力和力矩简化到所研究的截面
        mz = mz + fy * (x - cal_x)
        # 逐一计算每一个小格子的正应力
        for i in range(y_len):
            for j in range(z_len):
                n_stress_mat[i, j] = single_n_stress(fx, my, mz, i, j, scale)

    return n_stress_mat


def normal_stress_calculate(scale, length, force_pos, force_dir):
    # 获取力的作用截面上的分力与力矩
    x, force, moment = force_normalize(force_pos, force_dir)

    # 获取所研究的截面的位置
    cal_x = x
    while True:
        c = input("请输入所研究的截面的坐标(mm)(输入q以退出)：")
        if c == 'q' or c == 'Q':
            break
        cal_x = float(c) / 1000
        # 研究的截面在梁之外，使用户重新输入
        if (cal_x > length) or (cal_x < 0):
            print("错误：截面不在梁上")
            continue
        else:
            break

    # 返回截面正应力分布矩阵
    return calculate_stress_distribute(x, force, moment, cal_x, scale)


def normal_stress_calculate_all(scale, length, force_pos, force_dir):
    # 计算所有截面的应力分布
    # 获取力的作用截面上的分力与力矩
    x, force, moment = force_normalize(force_pos, force_dir)

    # 获取所研究的截面的位置
    step = 100
    x_list = np.linspace(0, length, step)
    n_mat = calculate_stress_distribute(x, force, moment, x_list[0], scale)
    for cal_x in x_list[1:]:
        mat = calculate_stress_distribute(x, force, moment, cal_x, scale)
        np.array([n_mat, mat])

    # 返回截面正应力分布矩阵
    return n_mat
