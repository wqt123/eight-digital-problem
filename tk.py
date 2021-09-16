'''
    通过tkinter库，实现程序可视化
'''
import time
import datetime
import tkinter as tk
from tkinter import messagebox
import numpy as np
from A_star import A_star,Node,end_array,start_array
import globalvar as gl

gl.set_value('algorithm',int(1))#使'algorithm'成为可跨文件的变量

isChoose = False #是否选择了估价函数
isFirst = True   #是否是第一次进行A*搜索
isStart = False  #是否按下'Go'开始键
step = 0   #A*搜索步数 
result_node = Node(np.zeros((3,3),dtype = int),0,None) #最终结果结点

window = tk.Tk()
window.title('eight-digital-problem')
window.geometry('670x350')     #定义窗口长宽

#起始和目标矩阵
frm_start = tk.Frame(window)
tk.Label(frm_start,text = 'start_state').place(x = 20,y = 0)

start = [] 
end = []
matrix = {1:start,2:end}

frm_start = tk.Frame(window)
frm_end = tk.Frame(window)
frm = {1:frm_start,2:frm_end}

for i in range(1,3):
    for j in range(9):
        temp_entry = tk.Entry(frm[i])
        matrix[i].append(temp_entry)
for k in range(1,3):
    for i in range(3):
        for j in range(3):
            matrix[k][i*3+j].place(x = i*40,y = j*40 + 30,width = 40,height = 40)

label = {1:'start',2:'end'}
for i in range(1,3):
    tk.Label(frm[i],text = label[i]).place(x = 50,y = 15,anchor = 'center')
    frm[i].place(x = 30 + (i + 1)% 2 * 150,y = (i > 2)*160,width = 450,height = 450)

#过程展示
frm_process = tk.Frame(window)
canvas_process = tk.Canvas(frm_process,height = 117,width = 117)
#初始化展示组件
def init_process():
    for i in range(3):
        for j in range(3):
                    canvas_process.delete(tk.ALL)#去除上一帧图像
    for i in range(3):
        for j in range(3):
            canvas_process.create_text(20+i*39,20+j*39,text = '*',font = 40,tags = str(i*3+j))
    canvas_process.place(x = 0,y = 32)
    tk.Label(frm_process,text = 'process').place(x = 60,y = 15,anchor = 'center')
    frm_process.place(x = 30,y = 160,width = 450,height = 450)
    frm_process.update()
init_process()

#开始按钮
#初始化起始和目标矩阵          
def init_array():
    global isStart
    #初始化起始矩阵
    for i in range(3):
        for j in range(3):
            try:
                int(matrix[1][i*3+j].get())
            except:
                messagebox.showwarning('警告','请输入0-8的整数')
                isStart = False
                return
            if 0 <= int(matrix[1][i*3+j].get()) <= 8 :
                start_array[j][i] = int(matrix[1][i*3+j].get())
            else:
                messagebox.showwarning('警告','请输入0-8的整数')  
                isStart = False  
                return           
    #初始化目标矩阵
    for i in range(3):
        for j in range(3):
            try:
                int(matrix[2][i*3+j].get())
            except:
                messagebox.showwarning('警告','请输入0-8的整数')
                isStart = False
                return
            
            if 0 <= int(matrix[2][i*3+j].get()) <= 8 :
                end_array[j][i] = int(matrix[2][i*3+j].get())
            else:
                messagebox.showwarning('警告','请输入0-8的整数') 
                isStart = False   
                return
    start_status = 0
    end_status = 0
    for i in range(9):
        for j in range(i):
            if start_array[int(j / 3)][int(j % 3)] != 0 and start_array[int(j / 3)][int(j % 3)]  < start_array[int(i / 3)][int(i % 3)]:
                start_status += 1
            if end_array[int(j / 3)][int(j % 3)] != 0 and end_array[int(j / 3)][int(j % 3)]  < end_array[int(i / 3)][int(i % 3)]:
                end_status += 1
    if start_status % 2 != end_status % 2:
        messagebox.showwarning('警告','本次输入无解，请重新输入') 
        isStart = False
#搜索路径结点列表
def node_list(node):
    node.inPath = True
    allnode = [node]
    for i in range(node.deepth):
        allnode.insert(0,node.parent)
        node = node.parent
        node.inPath = True
    
    return allnode
#显示搜索过程
def show_process(all_node):
    for node in all_node:
        for i in range(3):
            for j in range(3):
                    canvas_process.delete(tk.ALL)#去除上一帧图像
        for i in range(3):
            for j in range(3):
                if end_array[j][i] == node.array[j][i]:
                    canvas_process.create_text(20+i*39,20+j*39,text = str(node.array[j][i]),font = 40,fill = 'green',tags = str(i*3+j))
                else:
                    canvas_process.create_text(20+i*39,20+j*39,text = str(node.array[j][i]),font = 40,fill = 'black',tags = str(i*3+j))      
        time.sleep(1)
        canvas_process.update() #更新
#初始化A*算法相关细节
def init_detail(all_node):
    global text,scroll,canvas_detail,time
    str1 = ''
    str2 = ''
    
    #显示每一步状态
    text = tk.Text(window,width=20,height=17)
    scroll = tk.Scrollbar()

    # 两个控件关联
    scroll.config(command=text.yview)
    text.config(yscrollcommand=scroll.set)

    step = 0
    for node in all_node:
        if step != 0:
            str1 = str1 + 'step ——> ' + str(step) + '\n'
        for i in range(3):
            for j in range(3):
               str1 = str1 + str(node.array[i][j]) + ' '
            str1 = str1 + '\n' 
        str1 += '\n' 
        step += 1
    text.insert(tk.INSERT,str1)
    
    #显示步数和和时间
    str2 = str2 + 'step：' + str(step) + '\n' + 'time：' + str(time_Astar) + 's'
    canvas_detail.create_text(50,20,text = str2)

def start(result_node):
    global isChoose,all_node,step,isFirst,isStart,time_Astar,press_times
    press_times = 0
    isStart = True
    if isChoose:
        if isFirst == False: #不是第一次运行时需要对之前创建、显示的组件进行处理
            init_process()
            time.sleep(0.5)
            canvas_curtain.place(x = 350,y = 30)
            canvas_detail.place_forget() 
            canvas_detail.delete(tk.ALL) 
            tree_button.place_forget()
            scroll.place_forget()
            text.destroy()  

        init_array()
        if isStart == False:
            return
        start = datetime.datetime.now()
        result_node = A_star()
        end = datetime.datetime.now()
        time_Astar = (end - start).microseconds / 1000 #A*搜索时间
        step = result_node.deepth + 1
        all_node = node_list(result_node)
        show_process(all_node)
        init_detail(all_node)
        isChoose = False
        isFirst = False
    else:
        messagebox.showwarning('警告','请先选择估价函数')

start_button = tk.Button(window,text = 'Go',width = 5,height = 1,command = lambda : start(result_node))
start_button.place(x = 205, y = 240)

#细节展示
press_times = 0 #点击展示按钮的次数
image_file = tk.PhotoImage(file = 'figure/image1.png')
canvas_curtain = tk.Canvas(window,height = 300,width = 300)
canvas_curtain.create_image(0,0,anchor = 'nw',image = image_file)
canvas_curtain.place(x = 350,y = 30)
canvas_detail = tk.Canvas(window,height = 200,width = 200)

#绘制搜索树
def draw(node,n):
    global dic
    global canvas
    canvas.create_rectangle(5+60*dic[n],5+60*n,55+60*dic[n],55+60*n)

    if node.inPath:
        str_color = 'red'
    else:
        str_color = 'black'
    for i in range(3):
        for j in range(3):
            canvas.create_text(5+60*dic[n]+5+i*20,5+60*n+5+j*20,text = str(node.array[j][i]),fill = str_color)
    if len(node.child) == 0:
        dic[n] += 1
        canvas.pack()
        return
    for child in node.child:
        canvas.create_line(30+60*dic[n],55+60*n,30+60*dic[n + 1],65+60*(n))
        draw(child,n+1)  
    dic[n] += 1
def show_tree():
    global all_node
    global canvas
    global step
    global dic
    dic = dict.fromkeys(range(step),0)
    w = tk.Toplevel() #新窗口
    w.title('Tree')
    canvas = tk.Canvas(w,height = 60*step + 20,width = 60*step + 20)
    draw(all_node[0],0)
tree_button = tk.Button(window,text = 'show tree',width = 10,height = 1,command = show_tree)
#细节展示按钮
def show_detail():
    global image_file,canvas_curtain,press_times,frm_detail,text,scroll,isStart
    if isStart:
        if press_times % 2:
            press_times += 1
            scroll.place_forget()
            text.place_forget()
            tree_button.place_forget()
            canvas_detail.place_forget()
            canvas_curtain.place(x = 350,y = 30)  
        else:
            press_times += 1
            canvas_curtain.place_forget()
            text.place(x =350,y = 30)
            scroll.place(x = 500,y = 30)
            tree_button.place(x =540,y = 250)
            canvas_detail.place(x = 540,y =100)
    else:
        messagebox.showwarning('警告','请先进行A*搜索')

show_button = tk.Button(window,text = 'Show Detail',width = 10,height = 1,command = show_detail)
show_button.place(x = 185, y = 280)

#估计代价函数选择
def choose(i):
    gl.set_value('algorithm',i) 
    global isChoose,isStart
    isChoose = True
    isStart = False #更换估计代价函数后需要重新运行程序

choice_button = tk.Menubutton(window,text = ' Choose h(n) ',width = 10,height = 1,relief = 'raised')
choice_button.place(x = 200, y = 200)   
algorithm_menu = tk.Menu(choice_button, tearoff=False)
algorithm_menu.add_command(label = 'h1(n)',command = lambda :choose(1))
algorithm_menu.add_command(label = 'h2(n)',command = lambda :choose(2))
algorithm_menu.add_command(label = 'h3(n)',command = lambda :choose(3))
choice_button.config(menu = algorithm_menu)

window.mainloop()
