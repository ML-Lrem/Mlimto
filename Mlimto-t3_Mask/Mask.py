# coding=utf-8
# author: ML-L rem
# computer: L rem
# Start time: 2021/11/22

# import sys
# sys.path.append('../package')

import imt
import math
import ft  # Need to read and create folders
import cv2 as cv
import numpy as np
from tqdm import tqdm

if __name__ == '__main__':
    ''' input '''
    sources_folder = input('请输入图片批处理文件夹\n')
    img_new_name = input('请输入新的图集名')
    save_folder = sources_folder
    backup_fold = sources_folder + r'\old'
    # maskRan = input('遮罩范围？以百分比形式输入0.2\n')
    # maskDir = input('遮罩类型？1-上下;2-下上;3-左右;4-右左; 5-左上右下;6-左下右上;7-右上左下;8-右下左上\n')  # 1
    # maskTra = input('遮罩透明度？以百分比形式输入0-1,1-完全透明\n')
    # maskCol = input('遮罩颜色？默认取图片\'主色调\'\n')

    ''' handle data '''
    mask_range = 0.4  # 默认遮罩范围
    mask_mode = '7'  # 默认遮罩类型
    mask_alpha = [0.4, 0]  # 默认遮罩透明样式(起始透明度,终止透明的度)
    mask_color = [0, 0, 0]  # 由于色调提取算法未完成，遮罩色彩固定为黑色

    img_pixel = [3840, 2160]
    # img_new_name = 'fox'

    ''' get img path '''
    ft.copyFile(foldPath=sources_folder, copyPath=backup_fold)
    img_sources_path = ft.getList(foldPath=sources_folder, fileType=['jpg', 'png', 'jpeg'], outMode='path', subFold=0)

    ''' 遮盖图片初始化 '''
    img_mask = 0
    for n, img_path in enumerate(tqdm(img_sources_path)):
        ''' read the image and add a alphaChannel'''
        img = imt.crop(path=img_path, pl=img_pixel)  # 按比例裁剪图片
        img = imt.compress(img=img, mode='force', pl=img_pixel)  # 强制缩放图片模式，保证长宽一定一致

        ''' get mask color '''
        # # 缩放100倍，一定会取一个色调最多的出来(色调提取算法有待优化：参考edge项目收藏，由于该项目必须要这个算法的支持，故暂时停滞)
        if n < 1:  # 遮罩只需要生成一次
            ''' create mask img '''
            img_height, img_width = img.shape[0:2]
            # 根据渐变类型、遮罩方向、遮罩范围，更新能被遮罩的区域，优先实现所需类型的遮罩
            # 1. 基于mask_col生成一张遮罩图片imgMask
            img_mask = np.zeros((img_height, img_width, 3), np.uint8)
            img_mask[:, :] = (mask_color[2], mask_color[1], mask_color[0])
            b_channel, g_channel, r_channel = cv.split(img_mask)  # 切分imgMask通道，用于后续计算

            # 2. 基于maskRan, maskTra修改imgMask的透明样式
            if mask_mode in ['1', '2', '3', '4']:  # 竖直或水平渐变, 其实可以统一到对角遮盖模式下
                pass
            else:
                # 方法1：基于函数计算。 算法更复杂, 其实也可以设计得很通用 ,渐变的关键是根据预设参数找到渐变线alphaLine
                # 生成img_mask的透明通道
                alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 0
                # 计算参考线方程 　line: A,B,C
                A = img_height / img_width
                B = 1
                C = 0
                max_distance = abs(A * img_width + B * img_height + C) / (math.sqrt(A * A + B * B))
                for y in range(img_height):
                    for x in range(img_width):
                        distance = abs(A * x + B * y + C) / (math.sqrt(A * A + B * B))
                        dD = distance / (max_distance * mask_range)
                        if dD > 1:  # 渐变终止
                            break
                        else:
                            alpha_channel[y, x] = int(255 * ((mask_alpha[1] - mask_alpha[0]) * dD + mask_alpha[0]))
                img_mask = cv.merge((b_channel, g_channel, r_channel, alpha_channel))
                # 方法2：基于图片旋转。可适用与任何角度, 通用性更好

                # 3. 基于maskMode修改遮盖方向
                if mask_mode == '5':
                    pass
                elif mask_mode == '7':
                    img_mask = cv.flip(img_mask, 1)

        ''' add mask '''
        img_out = imt.addOrigin(img, img_mask)

        ''' save new img '''
        # 存储图片到指定路径
        img_save_path = sources_folder + '\\' + img_new_name + '_' + str(n) + '.jpg'
        imt.write(path=img_save_path, img=img_out)

        ''' delete old img '''
        if img_path == img_save_path:
            pass
        else:
            ft.deleteFile(img_path)
