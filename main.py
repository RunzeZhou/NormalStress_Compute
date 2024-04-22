from graph_reader import *
from calculate import *
from project_UI import *


if __name__ == '__main__':
    # 向用户请求数据
    img_matrix, scale, length, force_pos, force_dir = get_info()

    # 计算面积与形心、形心主矩，定义为全局变量，可随意调用
    y_c, z_c, area, y_len, z_len, d_a = get_centroid(img_matrix, scale)
    get_theta_moip(img_matrix)

    # 返回一个包含平面内各个点的正应力的矩阵，但是并未对截面的内外进行区分
    n_stress_mat = normal_stress_calculate(scale, length, force_pos, force_dir)

    # trial
    show_image(y_c, z_c, theta, 40, scale, n_stress_mat.max(), n_stress_mat.min(), n_stress_mat, img_matrix)
