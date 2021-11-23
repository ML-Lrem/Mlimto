# 模块名：ft
# 模块功能：对文件进行处理的若干函数
# 功能：
#   图片路径读取
#   图片存储

import os
import shutil
import re


# Name：getList
# Description: 获取指定文件夹内的图片路径，图片格式仅限jpg、png
# input：
#   foldPath：文件夹路径
#   fileType：指定文件类型，'all'-全部类型，默认fileType='all'，可选fileType=['jpg', 'png']
#   mode：输出文件列表类型，'name'-输出文件名列表;'path'-输出文件路径列表
#   subFold: 是否包含子文件夹
# Return：
#   fileList：指定文件夹下、制定文件类型的完整路径或名字
#
# process：done
def getList(foldPath=None, fileType='all', outMode='path', subFold=0):
    fileList = []
    fileDirs = []
    # 获得文件路径
    if subFold == 0:
        fileDirs = os.listdir(foldPath)
        for n, item in enumerate(fileDirs):
            fileDirs[n] = os.path.join(foldPath, item)
    else:
        for root, dirs, files in os.walk(foldPath, topdown=False):
            for name in files:
                fileDirs.append(os.path.join(root, name))
            for name in dirs:
                fileDirs.append(os.path.join(root, name))
    # 筛选文件类型
    if fileType == 'all':
        if outMode == 'path':
            fileList = fileDirs
        else:
            for item in fileDirs:
                fileList.append(getNames(item))
    else:
        for item in fileDirs:
            # 使用正则表达式匹配后缀名
            suffix = ''.join(re.findall(r'\.(\w+$)', item))
            if suffix in fileType:
                if outMode == 'path':
                    fileList.append(item)
                else:
                    fileList.append(getNames(item))
    return fileList


# Name：getNames
# Description: 获取指定文件路径的文件名
# input：
#   filePath：文件路径
# Return：
#   fileNames：指定文件路径的文件名
#
# process：done
def getNames(path=None, inSuffix=1):
    if inSuffix:
        fileName = ''.join(re.findall(r'[^\\]+\.\w+$', path))   # 重要的正则表达式
    else:
        fileName = ''.join(re.findall(r'([^\\]+)\.\w+$', path))  # 不保留后缀名，重要的正则表达式
    return fileName


# Name：getDesktop
# Description: 获取桌面地址
# input：
#   None
# Return：
#   Path：Desktop
#
# process：done
def getDesktop():
    return os.path.join(os.path.expanduser("~"), 'Desktop')


# Name：createFold
# Description: 新建文件夹
# input：
#   path：imgPath
# Return：
#   None
#
# process：done
def createFold(path=None):
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False


# Name：deleteFile
# Description: 删除指定路径的图片
# input：
#   path：filePath
# Return：
#   None
#
# process：done
def deleteFile(path=None):
    os.remove(path)


# Name：copyFile
# Description: 复制文件或文件夹
# input：
#   path：filePath or foldPath
# Return：
#   None
#
# process：done
def copyFile(filePath=None, foldPath=None, copyPath=None):
    if filePath is not None:
        createFold(copyPath)
        path, name = os.path.split(filePath)
        shutil.copy(filePath, copyPath + name)
    elif foldPath is not None:
        if os.path.exists(copyPath):
            shutil.rmtree(copyPath)
        shutil.copytree(foldPath, copyPath)     # 库自带文件夹创建功能
    else:
        print('Noting need to copy')
