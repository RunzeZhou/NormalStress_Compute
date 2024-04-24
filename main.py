from graph_reader import *
from calculate import *
from project_UI import *
from gif_generator import *
import os


def m2point(y, z):
    # 将尺寸参数转换为像素
    center_y = int(0.5 * y_len)
    center_z = int(0.5 * z_len)
    delta_y, delta_z = y / scale, z / scale
    y_point = int(center_y - delta_y)
    z_point = int(center_z - delta_z)
    return y_point, z_point


def get_max_min(img_mat, n_mat):
    # 计算截面上的最大正应力与最小正应力
    max_s = 0
    min_s = 0
    state_check = 0
    for i in range(img_mat.shape[0]):
        for j in range(img_mat.shape[1]):
            if img_mat[i, j] == 1:
                if state_check == 0:
                    state_check = 1
                    max_s = n_mat[i, j]
                    min_s = n_mat[i, j]
                else:
                    if n_mat[i, j] > max_s:
                        max_s = n_mat[i, j]
                    elif n_mat[i ,j] < min_s:
                        min_s = n_mat[i, j]
    return max_s, min_s


if __name__ == '__main__':
    # 向用户请求数据
    img_matrix, scale, length, force_pos, force_dir = get_info()

    # 计算面积与形心、形心主矩，定义为全局变量，可随意调用
    y_c, z_c, area, y_len, z_len, d_a = get_centroid(img_matrix, scale)
    theta, i_yp, i_zp = get_theta_moip(img_matrix, scale)

    req = input("A:计算特定截面正应力\nB:计算全部截面正应力")
    if req == 'a' or req == 'A':
        # 返回一个包含平面内各个点的正应力的矩阵，但是并未对截面的内外进行区分
        n_stress_mat = normal_stress_calculate(scale, length, force_pos, force_dir)
        max_str, min_str = get_max_min(img_matrix, n_stress_mat)

        # trial
        y_p, z_p = m2point(y_c, z_c)
        show_image(z_p, y_p, theta, 40, scale, max_str, min_str, n_stress_mat, img_matrix)

    elif req == 'b' or req == 'B':
        many_n_mat = normal_stress_calculate_all(scale, length, force_pos, force_dir)
        max_stress, min_stress = many_n_mat.max(), many_n_mat.min()
        gif_generator(length, theta, scale, max_stress, min_stress, img_matrix, many_n_mat)
        os.system("pause")
