from graph_reader import *
from calculate import *


if __name__ == '__main__':
    # 向用户请求数据
    img_matrix, scale, length, force_pos, force_dir = get_info()

    # 计算面积与形心，定义为全局变量，可随意调用
    get_centroid(img_matrix, scale)

