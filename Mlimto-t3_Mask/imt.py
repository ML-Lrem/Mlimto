# 模块名：imt
# 模块功能：各类处理图片的函数
# 功能：
#   裁剪图片
#   缩放图片：按比例缩放、按大小缩放
#   提取图片主色调
#   将图片切割成若干块(n*m块)


import cv2 as cv
import numpy as np
import re
import random

import col


# def autoCrop():


# Name：read
# Description: 读图片到img
# input：
#   path：图片路径
# Return：图片矩阵
#
# process：done
def read(path=None):
    img = cv.imdecode(np.fromfile(path, dtype=np.uint8), cv.IMREAD_COLOR)
    return img


# Name：write
# Description: 写图片到指定路径
# input：
#   path：图片路径
#   img： 图片矩阵
# Return：0
#
# process：done
def write(path=None, img=None, suffix='origin'):
    if suffix == 'origin':
        cv.imencode(path, img)[1].tofile(path)
    else:
        suffix = r'.' + suffix
        cv.imencode(suffix, img)[1].tofile(re.sub(r'.\w+$', suffix, path))
    return 0


# Name：Crop
# Description: 裁剪图片
# input：
#   path：图片路径
#   img： 图片矩阵
#   mode：裁剪模式，‘right’，居右；‘left'，居左；'center'，居中；'auto'，智能模式【默认居中】
#   wh：裁剪宽高比
# Return：
#   img：缩放后的图片矩阵
#
# process：done
def crop(path=None, img=None, mode='center', pl=None):
    wh = pl[0] / pl[1]
    if path is None:
        pass
    else:
        # 处理中文编码
        img = read(path)
    # 获取长宽
    hig, wid = img.shape[0:2]
    if mode == 'center':
        if wid / hig <= wh:
            newH = int(wid / wh)
            cropH1 = hig / 2 - newH / 2
            cropH2 = hig / 2 + newH / 2
            if cropH1 - int(cropH1) != 0:
                cropH1 = cropH1 - 0.5
            if cropH2 - int(cropH2) != 0:
                cropH2 = cropH2 - 0.5
            cropH1 = int(cropH1)
            cropH2 = int(cropH2)
            img = img[cropH1:cropH2, 0:wid]
        elif wid / hig == wh:
            pass
        else:
            newW = int(hig * wh)
            cropW1 = wid / 2 - newW / 2
            cropW2 = wid / 2 + newW / 2
            if cropW1 - int(cropW1) != 0:
                cropW1 = cropW1 - 0.5
            if cropW2 - int(cropW2) != 0:
                cropW2 = cropW2 - 0.5
            cropW1 = int(cropW1)
            cropW2 = int(cropW2)
            img = img[0:hig, cropW1:cropW2]
    elif mode == 'right':
        if wid / hig < wh:
            newH = int(wid / wh)
            img = img[0:hig - newH, 0:wid]
        else:
            newW = int(hig * wh)
            img = img[0:hig, wid - newW:wid]
    elif mode == 'left':
        if wid / hig < wh:
            newH = int(wid / wh)
            img = img[0:newH, 0:wid]
        else:
            newW = int(hig * wh)
            img = img[0:hig, 0:newW]
    elif mode == 'auto':
        pass
        # img = autoCrop(img)
    else:
        print('crop parameter error')
    return img


# Name：compress
# Description: 缩放图片
# input：
#   path：图片路径
#   mode：缩放模式，prop，等比例缩放；width，等宽缩放；
#   wid：锁定宽度
#   pro：缩放比例
# Return：
#   img：缩放后的图片矩阵
#
# process：done
def compress(path=None, img=None, mode='width', pl=None, pro=None):
    if path is None:
        pass
    else:
        img = read(path)
    h, w = img.shape[0:2]
    if mode == 'width':
        img = cv.resize(img, (pl[0], int(h * pl[0] / w)))
    elif mode == 'prop':
        img = cv.resize(img, (int(w * pro), int(h * pro)))
    elif mode == 'force':
        img = cv.resize(img, (pl[0], pl[1]))
    else:
        print('zip parameter error')
    return img


# Name：getTone  【可优化：返回主色调与某一固定ctg的偏离程度】
# Description: 获取图片的主色调
# input：
#   path：图片路径
#   img： 图片矩阵
#   SA: 采样精度-图片缩放倍数, SA越大，获取的主色调能更能够代表实际值，默认SA=0.2(SA=0-1)
#   PCT: 主色阈值-当一张图片中某一颜色的量在总量中的占比不小于PCT，则认为这种颜色为主色，PCT越高，得到图片的色彩更单一（更适合作为源图片），默认PCT=0.2,PCT=0~1，
# Return：
#   tone: 图片主色调
#   '000'：无法提取主色调
#
# process：done
def getTone(path=None, img=None, SA=0.2, PCT=0.15):
    if path is None:
        pass
    else:
        img = read(path)
    # print('压缩前：', img.shape[0:2])
    # 压缩图片以提高计算速度
    img = compress(img=img, mode='prop', pro=SA)
    # print('压缩后：', img.shape[0:2])
    # 统计图片中各个颜色的量
    ctgList = []
    for hig in range(img.shape[0]):
        for wid in range(img.shape[1]):
            bgr = img[hig, wid]
            rgb = [bgr[2], bgr[1], bgr[0]]
            ctg = col.getCate(rgb=rgb, SAH=5, SAS=5, SAV=8)
            ctgList.append(ctg)
    # 统计最多的色调
    tone = max(ctgList, key=lambda v: ctgList.count(v))
    if ctgList.count(tone) >= len(ctgList) * PCT:
        return tone
        # 将‘516’转为[5,1,6]
        # return list(map(eval, list(tone)))
    else:
        return 'NT'


# Name：getSubPost
# Description: 将图片切成若干块,得到每一块的坐标位置
# input：
#   path：图片路径
#   img： 图片矩阵
#   mPix：最小像素点的像素
#   wBlo：约束横向的块总数
# Return：imgBloPost：所有块在原图中的位置
#
# process：done
def getSubPost(path=None, img=None, mPix=None, Blo=None):
    if path is None:
        pass
    else:
        img = read(path)
    hig, wid = img.shape[0:2]
    if hig >= wid:
        hBlo = Blo
        higStep = round(hig / hBlo)
        widStep = round(higStep * mPix[0] / mPix[1])
        wBlo = int(wid / widStep)
        hBlo = int(hig / higStep)
    else:
        wBlo = Blo
        widStep = int(wid / wBlo)
        higStep = int(widStep * mPix[1] / mPix[0])
        hBlo = int(hig / higStep)  # 注意这里为防止溢出，不能四舍五入，而要舍掉小数项
        wBlo = int(wid / widStep)
    imgBloPost = [[] for _ in range(hBlo)]
    # imgBloPost = []
    for j in range(hBlo):
        for i in range(wBlo):
            pX1 = str(i * widStep)
            pX2 = str((i + 1) * widStep)
            pY1 = str(j * higStep)
            pY2 = str((j + 1) * higStep)
            post = ','.join([pY1, pY2, pX1, pX2])
            imgBloPost[j].append(post)
    return imgBloPost


# Name：getSubImg
# Description: 根据坐标位置获得子图
# input：
#   path：图片路径
#   img： 图片矩阵
#   post：子图坐标位置，两种输入方式:1.'_X1_X2_Y1_Y2'; 2.[X1,X2,Y1,Y2]
# Return：imgSub：对应坐标位置的子图
#
# process：done
def getSubImg(path=None, img=None, post=None):
    if path is None:
        pass
    else:
        img = read(path)
    if isinstance(post, str):
        post = re.findall(r'\d+', post)
    else:
        pass
    img = img[int(post[0]):int(post[1]), int(post[2]):int(post[3])]
    return img


# Name：getSourceImg     【随机法】
# Description: 获得对应色调的源图片矩阵
# input：
#   toneList：图源
#   tone：当前色调
# Return：img：拼接结果
#
# process：done
def getSourceImg(pToneList=None, tone=None):
    tempPT = []
    for n, PT in enumerate(pToneList):
        if PT[1] == tone:
            tempPT.append(PT)
    if not tempPT:
        print('lack tone:', tone)
    P = random.randint(0, len(tempPT) - 1)
    imgPath = tempPT[P][0]
    img = read(path=imgPath)
    return img


# Name：split
# Description: 智能拼接两张图片
# input：
#   img1：第一张图片矩阵
#   img2：第二张图片矩阵
#   path1：第一张图片路径
#   path2： 第二张图片路径
#   doa：两张图片的拼接关系，level，水平，vert，垂直
# Return：img：拼接结果
#
# process：done
def split(img1=None, img2=None, doa='level'):
    if doa == 'level':
        img = cv.hconcat([img1, img2])
    else:
        img = cv.vconcat([img1, img2])
    return img


# Name：createAllTone
# Description: 创建所有色调的图片
# input：
#   foldPath：创建文件夹
#   pixel：图片尺寸
# Return：
#
# process：done
def createAllTone(foldPath=None, pixel=None):
    height = pixel[1]
    width = pixel[0]
    allPT = []
    img = np.zeros((height, width, 3), np.uint8)
    for ctg0 in range(6):
        for ctg1 in range(5):
            for ctg2 in range(8):
                # ctg = ''.join([str(ctg0), str(ctg1), str(ctg2)])
                # rgb = col.ctgTran(ctg=ctg, out='rgb')
                # tone = col.getCate(rgb=rgb)         # 由于算法，有些tone是等价的，比如000 = 010
                # if ctg == '305':
                #     print('ctg:', ctg, 'rgb', rgb, 'tone:', tone)
                # if tone != ctg:
                #     # print('tone:', tone, 'ctg:', ctg)
                #     pass
                # else:
                #     img[:, :] = (rgb[0], rgb[1], rgb[2])    # (B, G, R)
                #     imgPath = foldPath + '\\' + tone + '.jpg'
                #     write(path=imgPath, img=img)
                #     allPT.append([imgPath, tone])
                tone = ''.join([str(ctg0), str(ctg1), str(ctg2)])
                rgb = col.ctgTran(ctg=tone, out='rgb')
                img[:, :] = (rgb[2], rgb[1], rgb[0])  # (B, G, R)
                imgPath = foldPath + '\\' + tone + '.jpg'
                write(path=imgPath, img=img)
                allPT.append([imgPath, tone])
    # ctg = '147'
    # rgb = col.ctgTran(ctg=ctg, out='rgb')
    # print('ctg:', ctg, 'rgb:', rgb)
    # img[:, :] = (rgb[2], rgb[1], rgb[0])    # (B, G, R)
    # imgPath = foldPath + '\\' + ctg + '.jpg'
    # write(path=imgPath, img=img)
    return allPT


# Name：addOrigin
# Description: 图片原样重叠
# input：
#   img1：底图
#   img2：顶图
# Return：img
#
# process：done

def addOrigin(img1, img2):
    if img2.shape[2] == 3:
        img = cv.add(img1, img2)
    else:
        alphaImg2 = img2[:, :, 3] / 255
        alphaImg1 = 1 - alphaImg2
        for c in range(0, 3):
            img1[:, :, c] = (alphaImg1 * img1[:, :, c] + (alphaImg2 * img2[:, :, c]))
        img = img1
    return img
