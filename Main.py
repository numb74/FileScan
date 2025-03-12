import tkinter as tk
from ttkbootstrap import ttk

import requests
from fake_user_agent import user_agent
from concurrent.futures import ThreadPoolExecutor


# 所有函数

# 处理每个URL的请求
def fetch_url(exp, Source_Url):

    headers = {
        'User-Agent': user_agent()
    }
    url = Source_Url + exp
    response = requests.get(url=url, headers=headers)
    if str(response.status_code) == '200':
        return url
    else:
        print("状态码不为200")

# 扫描函数
def Scan():

    tree.delete(*tree.get_children())

    with open('./payload.txt', 'r') as file:
        expressions = [line.strip() for line in file]


    Source_Url = [Text_Enter_Context.get()] * len(expressions)
    # 调用python内置多线程
    with ThreadPoolExecutor() as executor:
        results = executor.map(fetch_url, expressions , Source_Url)


    # 收集符合条件的URL
    urls_to_write = [url for url in results if url is not None]
    for url, status in zip(urls_to_write, ['200']*len(urls_to_write)):
        tree.insert("", tk.END, values=(url, status))

    # 写入给输出文本文件，Status_200.txt
    with open('Status_200.txt', 'w', encoding='utf-8') as file:
        for url in urls_to_write:
            file.write(url + '\n')





# 创建主窗口
a1 = tk.Tk()
a1.title('扫描工具')
a1.geometry('600x500')

# 输入区域
Text_Enter_Context = tk.StringVar()
Text_Enter = tk.Label(a1, font=('微软雅黑', 10), text='请输入url: ')
TextBox_Enter = tk.Entry(a1, font=('微软雅黑', 10), textvariable=Text_Enter_Context, width=30)
Button_Scan = tk.Button(a1, font=('微软雅黑', 10), text='开始扫描', width=10, height=1, command=Scan)

# 使用 grid 布局放置输入区域组件
# Text_Enter.grid(row=0, column=0, padx=10, pady=10, sticky="w")
Text_Enter.place(x=150,y=10)
TextBox_Enter.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
Button_Scan.grid(row=0, column=2, padx=10, pady=10, sticky="e")

# 创建 Treeview 展示区域
frame = ttk.Frame(a1)
frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

# 配置 grid 布局权重
a1.grid_rowconfigure(1, weight=1)
a1.grid_columnconfigure(0, weight=1)
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

# 创建 Treeview
tree = ttk.Treeview(frame, columns=("URL", "Status Code"), show="headings")
tree.heading("URL", text="URL")
tree.heading("Status Code", text="Status Code")

# 设置列的对齐方式为居中
tree.column("URL", anchor="center")
tree.column("Status Code", anchor="center")

# 创建垂直滚动条
v_scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=v_scrollbar.set)

# 创建水平滚动条
h_scrollbar = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=tree.xview)
tree.configure(xscroll=h_scrollbar.set)

# 使用 grid 布局放置 Treeview 和滚动条
tree.grid(row=0, column=0, sticky="nsew")
v_scrollbar.grid(row=0, column=1, sticky="ns")
h_scrollbar.grid(row=1, column=0, sticky="ew")

# 运行主循环
a1.mainloop()