'''
    A*算法解决八数码问题
    f(n) = g(n) + h(n)
    g(n):深度
    h(n):估计价值函数
'''

import numpy as np 
import queue 
import globalvar as gl

start_array = np.zeros((3,3),dtype = int) #起始矩阵
end_array = np.zeros((3,3),dtype = int)   #目标矩阵
opened = queue.Queue() #open表，存储遍历的结点
closed = {}            #close表，标记结点状态是否被遍历

# 不在位元素个数
def h1(array):
    count = 0
    for i in range(3):
        for j in range(3):
            temp_elem = array[i][j]
            comp_elem = end_array[i][j]
            count += temp_elem != comp_elem
    return count
# 曼哈顿距离
def h2(array):
    count = 0
    for i in range(3):
        for j in range(3):
            for m in range(3):
                for n in range(3):
                    if(array[i][j] == end_array[m][n]):
                        count += abs(i - m) + abs(j - n)
    return count
# 欧几里德距离
def h3(array):
    count = 0
    for i in range(3):
        for j in range(3):
            for m in range(3):
                for n in range(3):
                    if(array[i][j] == end_array[m][n]):
                        count += ((i - m) ** 2 + (j - n) ** 2) ** 0.5
    return count
#估价函数字典
h = {1:h1,2:h2,3:h3}
class Node:
    f = -1   #启发值
    deepth = 0 #从开始到现在经历的步数
    parent = None #父结点
    child = []      #子结点
    child_num = 0     #子结点个数
    array = np.array([[0,0,0],[0,0,0],[0,0,0]]) 
    inPath = False #结点是否在找到的路径中

    def __init__(self,array,deepth,parent):
        self.array = array
        self.deepth = deepth
        self.parent = parent
#将矩阵映射成整数  
def index(array):
    a = 0
    for i in array:
        for j in i:
            a = a*10 + j
    return a
#移动‘0’
def move(now_array,dir):
    temp_x,temp_y = np.where(now_array == 0)
    x = temp_x[0]
    y = temp_y[0]
    array = np.copy(now_array)

    if dir == 'left':
        if y == 0:
            return array 
        array[x][y] = array[x][y - 1]
        array[x][y - 1] = 0
        return array
    
    if dir == 'right':
        if y == 2:
            return array 
        array[x][y] = array[x][y + 1]
        array[x][y + 1] = 0
        return array

    if dir == 'up':
        if x == 0:
            return array 
        array[x][y] = array[x - 1][y]
        array[x - 1][y] = 0
        return array

    if dir == 'down':
        if x == 2:
            return array 
        array[x][y] = array[x + 1][y]
        array[x + 1][y] = 0
        return array
#更新open表
def update_opened(node):
    array = node.array
    temp_opened = opened.queue.copy()
    for i in range(len(temp_opened)):
        if (temp_opened[i] == array).all():
            if temp_opened[i].f <= node.f:
                return False
            else:
                temp_opened[i] = node 
                opened.queue = temp_opened
                return True
    temp_opened.append(node)
    opened.queue = temp_opened
    return True
#以启发值为标准对open表进行排序
def sort():
    tmp_open = opened.queue.copy()
    length = len(tmp_open)
    for i in range(length):
        for j in range(length):
            if tmp_open[i].f < tmp_open[j].f:
                tmp = tmp_open[i]
                tmp_open[i] = tmp_open[j]
                tmp_open[j] = tmp
            if tmp_open[i].f == tmp_open[j].f:
                if tmp_open[i].deepth > tmp_open[j].deepth:
                    tmp = tmp_open[i]
                    tmp_open[i] = tmp_open[j]
                    tmp_open[j] = tmp
    opened.queue = tmp_open
#A*算法
def A_star():
    #选择估价函数
    global h
    algorithm = gl.get_value('algorithm')
    #初始化open表
    first_node = Node(start_array,0,None)
    first_node.f = h[algorithm](first_node.array) + first_node.deepth
    opened.queue.clear()
    closed.clear()
    opened.put(first_node)

    while len(opened.queue) != 0:
        node = opened.get()
        #当结点的矩阵与目标矩阵相同时，程序结束返回该结点
        if(node.array == end_array).all():
            return node
        #将结点加入到close表中，表示已经遍历了该状态
        closed[index(node.array)] = 1
        #对结点进行扩展
        for dir in ['left','right','up','down']:
            temp_array = node.array
            child_node = Node(move(temp_array,dir),node.deepth + 1,node)
            child_node.f = h[algorithm](child_node.array) + child_node.deepth
            #如没有遍历过，则加入open表中
            if index(child_node.array) not in closed:
                update_opened(child_node)
                node.child = node.child + [child_node]
                node.child_num += 1
        #对open表进行排序
        sort()












        
