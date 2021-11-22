import ft
import imt
import gc
import re
# import time

from tqdm import tqdm

# 主函数
if __name__ == '__main__':
    # start = time.time()

    # 预设值
    # galleyFold = input("输入图集素材的文件夹地址：")
    # targetFold = input("输入目标图集的文件夹地址：")
    # sourceFold = input("源图片保存到（默认桌面地址）："）
    # saveFold = input("输出结果保存到？(默认桌面地址）：")
    galleyFold = r'.\gallery'
    targetFold = r'.\target'
    sourceFold = r'.\source'
    saveFold = r'.\save'

    pixel = input("输入源图片的像素大小n,n（默认100*100)：")
    block = input("输入目标图标的预分块数20-300(默认100）：")
    acc = input("设置源图片单色阈值1-10（单色阈值越高输出图像的色彩还原度越好，默认2）：")
    if pixel == '':
        pixel = [20, 20]  # 源图片的尺寸【像素】
    else:
        pixel = list(map(int, (re.findall(r'(\d+)', pixel))))
    if block == '':
        block = 300  # 目标图片的分块(按横向切块)
    else:
        block = list(map(int, (re.findall(r'(\d+)', block))))
        block = block[0]
    if acc == '':
        acc = 0.2  # 设置准确度，0-1
    else:
        acc = list(map(int, (re.findall(r'(\d+)', acc))))
        acc = acc[0]/10
    # hsvSpl = [6, 5, 8]

    # 获取图集素材的地址，图片类型：”jpg、png“；输出模式：文件路径；是否包含子文件：是
    galleyPaths = ft.getList(foldPath=galleyFold, fileType=['jpg', 'png', 'jpeg'], outMode='path', subFold=1)
    # 获取源图片主色调-用于拼图的若干小图片
    sourcePT = []  # 小图片路径+色调
    toneList = []
    for imgPath in tqdm(galleyPaths):
        img = imt.crop(path=imgPath, wh=pixel[0] / pixel[1])  # 按比例裁剪图片
        img = imt.compress(img=img, mode='width', wid=pixel[0])  # 等宽度缩放图片，作为拼图用的源图片
        imgTone = imt.getTone(img=img, SA=0.2, PCT=acc)  # 获取图片的主色调，预设
        if imgTone == 'NT':  # 图片不能提取出主色调
            pass
        else:
            # 存储满足条件的小图片到指定路径
            toneList.append(imgTone)
            numTone = toneList.count(imgTone)
            if numTone <= 400:  # 同一色调图片最多存放400张
                sourcePath = sourceFold + '\\' + str(imgTone) + '_' + ft.getNames(path=imgPath)
                imt.write(path=sourcePath, img=img, suffix='origin')
                sourcePT.append([sourcePath, imgTone])
            else:
                pass
    # 清除不需要再使用的变量内存
    del galleyPaths
    gc.collect()

    # 生成所有色调的各个图片
    allPT = imt.createAllTone(foldPath=sourceFold, pixel=pixel)
    sourcePT.extend(allPT)

    # 获取目标图集的地址，图片类型：”jpg、png“；输出模式：文件路径；是否包含子文件：否
    targetPaths = ft.getList(foldPath=targetFold, fileType=['jpg', 'png', 'jpeg'], outMode='path', subFold=0)
    # # 批处理目标图片-被拼合的大图片
    for n, imgPath in enumerate(targetPaths):
        img = imt.compress(path=imgPath, mode='width', wid=block * 5)  # 用于切块的图片，尺寸=Block*10
        imgBloPost = imt.getSubPost(img=img, mPix=pixel, Blo=block)  # 切图函数，返回值为每个块的位置信息
        imgLevel = []
        imgOut = []
        imgBloTone = []
        for level, postI in enumerate(tqdm(imgBloPost)):
            for vert, post in enumerate(postI):
                imgBlo = imt.getSubImg(img=img, post=post)
                imgBloTone = imt.getTone(img=imgBlo, SA=0.8, PCT=0)
                imgSource = imt.getSourceImg(pToneList=sourcePT, tone=imgBloTone)  # 随机
                if vert == 0:
                    imgLevel = imgSource
                else:
                    imgLevel = imt.split(img1=imgLevel, img2=imgSource, doa='level')
            if level == 0:
                imgOut = imgLevel
            else:
                imgOut = imt.split(img1=imgOut, img2=imgLevel, doa='vert')
        savePath = saveFold + '\\' + str(n) + '.jpg'
        imt.write(path=savePath, img=imgOut, suffix='jpg')
        del imgLevel, imgOut, imgBloTone
        gc.collect()
    # 清除内存
    del targetPaths, imgBloPost
    gc.collect()

    # end = time.time()
    # print("循环运行时间:%.2f秒" % (end - start), '\n')
