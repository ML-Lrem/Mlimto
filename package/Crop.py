# coding=utf-8
# author: L rem
# computer: 32926
# time: 2020/8/13 15:28
# FileName: Tool
# tool: PyCharm

# 接口：
#   galleyFold：预处理文件夹
#   targetFold：目标文件夹
#   targetName：0-原名，1-更改文件名
#   pixel：保存图片的像素（图片质量）

import ft
import imt
from tqdm import tqdm


if __name__ == '__main__':
    galleyFold = input("请输入预处理文件夹：")
    targetFold = input("请输入保存文件夹(默认保存在根目录中):")
    targetName = input("输入保存文件名：")
    pixel = input("输入图片像素大小（默认2K分辨率)：")
    if pixel == '':
        pixel = [3840, 2160]
    if targetFold == '':
        targetFold = galleyFold + '\\' + 'target'  # 默认目标文件位置    pixel = input("输入源图片的像素大小（默认2K分辨率)：")
    else:
        ft.createFold(targetFold)
    galleyPaths = ft.getList(foldPath=galleyFold, fileType=['jpg', 'png', 'jpeg'])
    print(galleyPaths)

    for n, imgPath in enumerate(tqdm(galleyPaths)):
        img = imt.crop(path=imgPath, pl=pixel)      # 按比例裁剪图片
        img = imt.compress(img=img, mode='width', wid=pixel[0])    # 等宽度缩放图片
        # 存储满足条件的小图片到指定路径
        targetPath = targetFold + '\\' + targetName + '_' + str(n) + '.jpg'
        imt.write(path=targetPath, img=img)
