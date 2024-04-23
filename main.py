from graph_reader import *
from calculate import *
from project_UI import *


def m2point(y, z):
    # 将尺寸参数转换为像素
    center_y = int(0.5 * y_len)
    center_z = int(0.5 * z_len)
    delta_y, delta_z = y / scale, z / scale
    y_point = int(center_y - delta_y)
    z_point = int(center_z - delta_z)
    return y_point, z_point


if __name__ == '__main__':
    # 向用户请求数据
    img_matrix, scale, length, force_pos, force_dir = get_info()

    # 计算面积与形心、形心主矩，定义为全局变量，可随意调用
    y_c, z_c, area, y_len, z_len, d_a = get_centroid(img_matrix, scale)
    theta, i_yp, i_zp = get_theta_moip(img_matrix)

    # 返回一个包含平面内各个点的正应力的矩阵，但是并未对截面的内外进行区分
    n_stress_mat = normal_stress_calculate(scale, length, force_pos, force_dir)

    # trial
    y_p, z_p = m2point(y_c, z_c)
    show_image(z_p, y_p, theta, 40, scale, n_stress_mat.max(), n_stress_mat.min(), n_stress_mat, img_matrix)
