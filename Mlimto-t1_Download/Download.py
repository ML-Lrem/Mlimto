# coding=utf-8
# author: Lrem
# conputer: 32926
# time: 2020/8/13 22:32
# FileName: Tool_GUI

# tool: PyCharm

import os
import requests
import winsound
from tkinter import *
import tkinter.font as tf
from tkinter.filedialog import askdirectory


class Application(Frame):  # 继承Frame框架
    def __init__(self, master=None):  # Application类的构造函数,self-自身；master-操作控件；**kw-控件的各种特性
        super().__init__(master)  # super在python3中支持，super()代表的是父类(Frame)的定义，这里必须主动调用父类构造器
        self.master = master  # 创建类的属性(master)
        self.pack()  # 布局管理器pack()
        self.createMenu()  # 创建菜单组件
        self.creatInit()  # 创建基础配置栏
        self.creatWindows()  # 创建进程窗口

    def createMenu(self):
        # print("GUI")
        # 创建主菜单栏
        menu_bar = Menu(root)
        # 创建菜单项
        menu_Set = Menu(menu_bar, tearoff=False)  # tear_off去除横线
        menu_Help = Menu(menu_bar, tearoff=False)
        menu_about = Menu(menu_bar, tearoff=False)
        # 主菜单设置，并将菜单项绑定到主菜单中
        menu_bar.add_cascade(label="设置(S)", menu=menu_Set)
        menu_bar.add_cascade(label="帮助(H)", menu=menu_Help)
        menu_bar.add_cascade(label="关于(A)", menu=menu_about)
        # 增加子菜单项
        for item in ['默认下载地址']:
            menu_Set.add_command(label=item, accelerator="ctrl+d", command=self.test)  # accelerator快捷键显示
        # 将主菜单加到根窗口
        root["menu"] = menu_bar
        # 创建快捷菜单
        self.contextMenu = Menu(root)  # 不建议再子def内创建类成员
        self.contextMenu.add_command(label='打开图片路径', command=self.test)
        root.bind("<Button-3>", self.createcontextMenu)


    def createcontextMenu(self, event):
        self.contextMenu.post(event.x_root, event.y_root)

    def test(self):
        pass

    def creatInit(self):
        ft = tf.Font(family='宋体', size=12, weight=tf.BOLD)  # 设置字体
        # 引导标签
        label_Init = Label(self, text='基础配置', font=ft, fg='black', bg='#D9D9D9', height=2)
        label_Init.grid(row=0, column=0, padx=3, ipadx=15)
        label_line = Label(self, text='▮  ▮  ▮  ▮  ▮  ▮  ▮  ▮  ▮  ▮  ▮  ▮  ▮  ▮  ▮  ▮',
                           font=('宋体', 20), fg='#BFBFBF', relief='groove')  # relief：设置边框样式
        label_line.grid(row=0, column=1, sticky=W + N + S, columnspan=8, ipadx=6)
        # 下载按钮
        button_Download = Button(self, text='开始下载', font=('宋体', 18),
                                 fg='white', bg='#C55A11', command=start_download)
        button_Download.grid(row=0, column=9, sticky=W + N, rowspan=2, padx=8, ipadx=10, ipady=17)

        # 用户输入
        # @选项卡-下载模式
        label_DModel = Label(self, text=' 下载模式:', font=ft, height=2)
        label_DModel.grid(row=1, column=0, pady=4)
        global str_rad1
        str_rad1 = StringVar()  # 用以存储按钮获取到的字符
        str_rad1.set('S')  # 设置默认值
        rad_d_b1 = Radiobutton(self, text='单页', value='S', variable=str_rad1)
        rad_d_b2 = Radiobutton(self, text='图集', value='G', variable=str_rad1)
        rad_d_b1.grid(row=1, column=1)  # 布局
        rad_d_b2.grid(row=1, column=2)
        # @选项卡-提取规则
        label_RModel = Label(self, text='| 提取规则:', font=ft, height=2)
        label_RModel.grid(row=1, column=3, sticky=W)
        global str_rad2
        str_rad2 = StringVar()  # 用以存储按钮获取到的字符
        str_rad2.set('N')  # 设置默认值
        rad_r_b1 = Radiobutton(self, text='通用', value='N', variable=str_rad2)
        rad_r_b2 = Radiobutton(self, text='专家', value='E', variable=str_rad2)
        rad_r_b1.grid(row=1, column=4, sticky=W)  # 布局
        rad_r_b2.grid(row=1, column=5, sticky=W)
        # @文件导入
        label_address = Label(self, text='| 下载地址:', font=ft, height=2)
        label_address.grid(row=1, column=6, sticky=W)
        global str_address
        str_address = StringVar()  # 单行文本框entry接收字符
        file_entry = Entry(self, textvariable=str_address, relief='groove', state='disabled', width=10)
        file_entry.grid(row=1, column=7, sticky=W + E, ipadx=60, ipady=4)
        file_button = Button(self, text='...', bg='#D9D9D9', command=self.open_fold)
        file_button.grid(row=1, column=8, ipadx=5)
        # @目标网址
        label_url1 = Label(self, text=' 目标网址:', font=ft, height=2)
        label_url1.grid(row=2, column=0)
        global str_url1
        str_url1 = StringVar()  # 单行文本框entry接收字符
        entry_url1 = Entry(self, textvariable=str_url1, relief='groove')
        entry_url1.grid(row=2, column=1, columnspan=5, sticky=W, ipadx=82, ipady=4)
        # @图片特征符
        label_Img_key = Label(self, text=' 图片特征符:', font=ft, height=2)
        label_Img_key.grid(row=2, column=6)
        global str_key
        str_key = StringVar()  # 单行文本框entry接收字符
        str_key.set("(选填)")
        key_entry = Entry(self, textvariable=str_key, relief='groove')
        key_entry.grid(row=2, column=7, columnspan=2, sticky=W + E, ipadx=43, ipady=4)
        # @预览保存文件夹
        view_button = Button(self, text='预览图片文件夹', font=('宋体', 12),
                             bg='#D9D9D9', command=self.explorer_fold)
        view_button.grid(row=2, column=9, ipadx=5, )
        # @图集末尾
        label_url2 = Label(self, text=' 图集末尾:', font=ft, height=2)
        label_url2.grid(row=3, column=0)
        global str_url2
        str_url2 = StringVar()  # 单行文本框entry接收字符
        str_url2.set("PS：单页模式下无需填写此栏")
        entry_url2 = Entry(self, textvariable=str_url2, relief='groove')
        entry_url2.grid(row=3, column=1, columnspan=5, sticky=W, ipadx=82, ipady=4)
        # @正则表达式
        label_re_word = Label(self, text=' 正则表达式:', font=ft, height=2)
        label_re_word.grid(row=3, column=6)
        global str_re
        str_re = StringVar()  # 单行文本框entry接收字符
        str_re.set("PS：通用模式下无需填写此栏")
        entry_re = Entry(self, textvariable=str_re, relief='groove')
        entry_re.grid(row=3, column=7, columnspan=3, sticky=W, ipadx=114, ipady=4)

    def open_fold(self):
        str_address.set(askdirectory(title="选择下载地址", initialdir="C:\\Users\\32926\\Desktop"))

    def explorer_fold(self):
        address = str_address.get()
        if address == '':
            pass
        else:
            address = re.sub('/', '\\\\', address)
            print('lml:', address)
            os.system('explorer.exe /n,' + address)

    def creatWindows(self):
        ft = tf.Font(family='宋体', size=12, weight=tf.BOLD)  # 设置字体
        label_progress = Label(self, text='下载进程', font=ft, fg='black', bg='#D9D9D9', height=2)
        label_progress.grid(row=4, column=0, padx=3, ipadx=15)
        label_line = Label(self, text='▮  ▮  ▮  ▮  ▮  ▮  ▮  ▮  ▮  ▮  ▮  ▮  ▮  ▮  ▮  ▮  ▮  ▮  ▮ ',
                           font=('宋体', 20), fg='#BFBFBF', relief='groove')  # relief：设置边框样式
        label_line.grid(row=4, column=1, sticky=W + N + S, columnspan=9, ipadx=8)


def init_address(_address):
    if _address == '':
        _address = r"C:/Users/32926/Desktop/新建文件夹"
        folder = os.path.exists(_address)  # 判断地址是否存在
        if not folder:
            os.makedirs(_address)  # 新建地址
    _address += '/'
    return _address


# @ 功能1：从url中获取源代码（字符串）
def get_data(_url):
    # 获取源代码: .text是Unicode型数据，.content是二进制的数据
    # 设置http报头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/84.0.4147.105 Safari/537.36 '

    }
    _data = ''  # 初始化
    n = 0
    while n < 3:  # 重连
        try:
            html = requests.get(_url, headers=headers, timeout=5).text  # 这里使用text模式，以确保带有中文地址的图片获取成功
            _data = str(html)
            n = 3
        except requests.exceptions.RequestException as e:
            n += 1
    return _data


# @ 功能2：使用正则表达式，从源代码中获取图片信息
def get_list(_data, _const, _mode):
    if _mode == 'N':
        _list = re.findall(r'(https?[:][/].{0,150})(jpg|png|webp)(?![a-zA-Z0-9])', _data)
        new_list = []
        for n in range(len(_list)):
            num = 0
            # 对图片网址进行二次处理，过滤不必要的信息
            _list[n] = "".join(_list[n])
            _list[n] = re.sub(r'[\"\'].*', '', _list[n])
            # 第二次不同类型的图片筛选正则（re1)，可在“jpg|png|webp”中补充其他图片格式
            temp_list = re.findall('(https?[:](?!.*?http).*?)(jpg|png|webp)(?![a-zA-Z0-9])', _list[n])
            if temp_list:  # 判断地址是否合法
                temp_url = "".join(temp_list[0])
                # 在待定图片url中查找关键字，如果没有，则不保存此图片
                if _const == '':
                    new_list.append(temp_url)
                    num += 1
                elif re.search(_const, temp_url):
                    # 将列变转换为字符串并存储到新列表中,使用.append方法添加数据
                    new_list.append(temp_url)
                    num += 1
    else:
        re_word = str_re.get()
        _list = re.findall(re_word, _data)
        new_list = []
        for n in range(len(_list)):
            num = 0
            temp_url = _list[n]
            if _const == '':
                new_list.append(temp_url)
                num += 1
            elif re.search(_const, temp_url):
                # 将列变转换为字符串并存储到新列表中,使用.append方法添加数据
                new_list.append(temp_url)
                num += 1
    return new_list


# @ 功能3：从图片url列表中下载图片到指定路径
def Image_write(_list, _file_name):
    for i in range(len(_list)):
        # 获取单张图片，添加随机休眠避免访问频繁导致的错误
        n = 0
        # 处理缩略图
        _list[i] = re.sub('.md', '', _list[i])
        while n < 3:  # 重连
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/84.0.4147.105 Safari/537.36 '

                }
                picture = requests.get(_list[i], headers=headers, timeout=10).content
                # 从图片url中获取适合的文件名，使用图片地址命名可以排除重复图片
                p_name = re.sub(r'[\\\/\*\.\|\<\>]|jpg|png|webp', '', _list[i][-20:])
                suffix = "".join(re.findall(r"(.jpg|.png|.webp)$", _list[i]))  # 获取后缀名
                if suffix == '':
                    suffix = '.jpg'
                # with open *** as f方法用于文件的读写
                with open(_file_name + p_name + suffix, 'wb') as f:
                    f.write(picture)
                n = 3
            except requests.exceptions.RequestException as e:
                n += 1


# @ 功能5：多网址的图集滚动
def rolling_url(_url, _n):
    new_url = re.sub(r'\d{1,3}(?!.*\d)', str(_n), _url)
    return new_url


def start_download():
    root.iconify()
    url = str_url1.get()
    mode_flag = str_rad1.get()
    mode_search = str_rad2.get()
    if str_key.get() == '(选填)':
        const_word = ''
    else:
        const_word = str_key.get()
    address = init_address(str_address.get())
    if mode_flag == 'S':
        code_data = get_data(url)  # 获取源代码
        # print('源代码获取成功，下载中:\t')     # 可视化
        Image_list = get_list(code_data, const_word, mode_search)  # 获取图片列表
        Image_write(Image_list, address)  # 下载图片到文件夹
    else:
        Image_list = []
        url_fina = str_url2.get()
        page_num = int("".join(re.findall(r'\d{1,3}(?!.*\d)', url_fina)))  # 获取总页数
        # print('正在获取源代码，请稍后:')   # 可视化
        for page in range(page_num):
            code_data = get_data(url)  # 获取源代码
            Image_list.extend(get_list(code_data, const_word, mode_search))  # 获取图片列表，使用列表extend方法添加新列
            # Image_write(Image_list, address)  # 下载图片到文件夹
            url = rolling_url(url_fina, page + 2)  # 滚动图集下载地址
        # print('源代码获取成功，下载中:')   # 可视化
        Image_write(Image_list, address)  # 下载图片到文件夹
    winsound.Beep(300, 300)
    root.deiconify()


if __name__ == '__main__':
    root = Tk()
    root.title("Download_Image 网页图片下载器")
    root.iconbitmap("favicon.ico")
    root.geometry("920x700+200+150")  # 学习：如何让窗口记住上一次操作
    root.resizable(0, 0)
    app = Application(master=root)
    root.mainloop()
