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
    galleyFold = input('请输入图片批处理文件夹\n')
    targetFold = galleyFold
    targetName = 'fox'
    backFold = galleyFold + r'\old'
    # maskRan = input('遮罩范围？以百分比形式输入0.2\n')
    # maskDir = input('遮罩类型？1-上下;2-下上;3-左右;4-右左; 5-左上右下;6-左下右上;7-右上左下;8-右下左上\n')  # 1
    # maskTra = input('遮罩透明度？以百分比形式输入0-1,1-完全透明\n')
    # maskCol = input('遮罩颜色？默认取图片\'主色调\'\n')

    ''' handle data '''
    maskRan = 0.4  # 默认遮罩范围
    maskMode = '7'  # 默认遮罩类型
    maskTra = [0.4, 0]  # 默认遮罩透明样式(起始透明度,终止透明的度)
    maskCol = [0, 0, 0]  # 由于色调提取算法未完成，遮罩色彩固定为黑色

    pixel = [3840, 2160]

    ''' get file '''
    ft.copyFile(foldPath=galleyFold, copyPath=backFold)
    galleyPaths = ft.getList(foldPath=galleyFold, fileType=['jpg', 'png', 'jpeg'], outMode='path', subFold=0)

    ''' 遮盖图片初始化 '''
    imgMask = 0
    for n, imgPath in enumerate(tqdm(galleyPaths)):
        ''' read the image and add a alphaChannel'''
        # img = imt.read(imgPath)
        img = imt.crop(path=imgPath, pl=pixel)  # 按比例裁剪图片
        img = imt.compress(img=img, mode='force', pl=pixel)  # 强制缩放图片模式，保证长宽一定一致

        ''' get mask color '''
        # # 缩放100倍，一定会取一个色调最多的出来(色调提取算法有待优化：参考edge项目收藏，由于该项目必须要这个算法的支持，故暂时停滞)
        # tone = imt.getTone(img=img, SA=0.01, PCT=0)
        # rgb = col.ctgTran(ctg=tone, out='rgb')
        if n < 1:  # 遮罩只需要生成一次
            ''' create mask img '''
            hig, wid = img.shape[0:2]
            # 根据渐变类型、遮罩方向、遮罩范围，更新能被遮罩的区域，优先实现所需类型的遮罩
            # 1. 基于maskCol生成一张遮罩图片imgMask
            imgMask = np.zeros((hig, wid, 3), np.uint8)
            imgMask[:, :] = (maskCol[2], maskCol[1], maskCol[0])
            bChannel, gChannel, rChannel = cv.split(imgMask)  # 切分imgMask通道，用于后续计算

            # 2. 基于maskRan, maskTra修改imgMask的透明样式
            if maskMode in ['1', '2', '3', '4']:  # 竖直或水平渐变, 其实可以统一到对角遮盖模式下
                pass
            else:
                # 方法1：基于函数计算。 算法更复杂, 其实也可以设计得很通用 ,渐变的关键是根据预设参数找到渐变线alphaLine
                # 生成imgMask的透明通道
                alphaChannel = np.ones(bChannel.shape, dtype=bChannel.dtype) * 0
                # 计算参考线方程 　line: A,B,C
                A = hig / wid
                B = 1
                C = 0
                D = abs(A * wid + B * hig + C) / (math.sqrt(A * A + B * B))
                for y in range(hig):
                    for x in range(wid):
                        d = abs(A * x + B * y + C) / (math.sqrt(A * A + B * B))
                        dD = d / (D * maskRan)
                        if dD > 1:  # 渐变终止
                            break
                        else:
                            alphaChannel[y, x] = int(255 * ((maskTra[1] - maskTra[0]) * dD + maskTra[0]))
                imgMask = cv.merge((bChannel, gChannel, rChannel, alphaChannel))
                # 方法2：基于图片旋转。可适用与任何角度, 通用性更好

                # 3. 基于maskMode修改遮盖方向
                if maskMode == '5':
                    pass
                elif maskMode == '7':
                    imgMask = cv.flip(imgMask, 1)

        ''' add mask '''
        imgOut = imt.addOrigin(img, imgMask)

        ''' save new img '''
        # 存储图片到指定路径
        targetPath = targetFold + '\\' + targetName + '_' + str(n) + '.jpg'
        imt.write(path=targetPath, img=img)

        ''' delete old img '''
        if imgPath == targetPath:
            pass
        else:
            ft.deleteFile(imgPath)
