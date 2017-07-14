""" 
**************************************************************************************
***    coding = utf-8                                                              ***
***    By JerCas                                                                   ***
***    2017-7-5~10                                                                    ***
***                                                                                ***
***    A typeical simulate example of conway life game which achieved by python    ***
**************************************************************************************
"""

# 导入numpy模块使用其数值操作
import numpy as np
# 导入matplotlib模块分别进行绘图和更新模拟
import matplotlib.pyplot as pyplot
import matplotlib.animation as animation

""" ***以下伪代码块部分已处理为运行以查看部分单块的功能操作*** """

""" 网格表示块
    # array()--生成一个二维数组x[][]
    example = np.array([[0,0,255],[255,255,0],[0,255,0]])
    # imshow()--显示出网格状态，将数字矩阵example表示为一张图像;参数interpolation给予nearest属性，以获得尖锐边缘效果（可理解为抗锯齿）
    pyplot.imshow(example,interpolation='nearest')
    # show()--输出图像
    pyplot.show()
"""

""" 随机初始化块
    # random.choice()--随机数生成；[0,255]-生成随机数范围、4*4-生成随机数个数、p=[0.1,0.9]-随机数生成概率，此处为p(0)=0.1,p(255)=0.9
    #                            最后将生成的含16个值的一维数组调用reshape()函数生成格式为4*4的二维数组
    example = np.random.choice([0,255],4*4,p=[0.1,0.9]).reshape(4*4)
    print("{}".format(example))
"""

""" 具象初始化块
    def addGlider(i,j,grid):
        #在网格块左上角的指定坐标(i,j)处，绘制添加一个滑翔机
        
        # 创建滑翔机外形的二维数组，存入图案数组glider
        glider = np.array([[0,0,255],[255,0,255],[0,255,255]])
        # 利用Numpy切片操作，将图案数组复制到模拟的二维网格中
        grid[i:i+3,j:j+3] = glider
        # 将处理完毕的二维数组传到制图函数imshow()随后绘图
        pyplot.imshow(grid)
        pyplot.show()
    # zero()--创建指定大小的零值数组；
    # reshape()--重构数组结构；此处为将 1维数组(1*25)———>2维数组(5*5)
    grid = np.zeros(5*5).reshape(5,5)
    addGlider(1,1,grid)
"""

""" 边界条件的处理
    # 生成一个3*3二维数组
    grids = np.array([[1,2,3],[4,5,6],[7,8,9]])
    print(grids)
    # 对于我们需要实现的环形边界,即对于grids[0][2]=3 要实现他的右边是1，上边是9
    # 定义getNeighbor来实现这个操作，通过传入需要获取邻居的网格具体坐标、二维数组的单向空间以及对应的操作数组，来输出各个邻居地址
    def getNeighbor(i,j,n,grid):
        right  = grid[i][(j+1)%n]
        left   = grid[i][(j-1)%n]
        top    = grid[(i-1)%n][j]
        bottom = grid[(i+1)%n][j]
        neighbor = [right,left,top,bottom]
        print('\nFor {0}\nright:{1[0]}\nleft:{1[1]}\ntop:{1[2]}\nbottom:{1[3]}\n'.format(grid[i][j],neighbor))
    i = input('Please input the row: ')
    j = input('Please input the col: ')
    getNeighbor(int(i),int(j),3,grids) 
"""

""" 命令行参数解析
    # 调用argparse模块自定义命令行参数解析
    descriptionStr = "Runs Conway's Game of Life simulation."
    parser = argparse.ArgumentParser(description = descriptionStr)
    # 添加参数解析
    parser.add_argument('--gridsize',dest='N',required=False)
    parser.add_argument('--movfile',dest='movfile',required=False)
    parser.add_argument('--interval',dest='interval',required=False)
    parser.add_argument('--glider',action='store_true',required=False)
    # 提交解析，返回前台具体输入命令
    args = parser.parse_args()
"""

import argparse
import sys
import matplotlib.pyplot
import numpy as np
import matplotlib.animation as animation

# 设置生命存活静态标识
ON = 255
OFF = 0
vals = [ON,OFF]

# 随机生成网格函数
def randomGrid(N):
    """随机返回一个N*N大小的随机值网格"""
    return np.random.choice(vals,N*N,p=[0.2,0.8]).reshape(N,N)

# 生成滑翔机图案函数
def addGlider(i,j,grid):
    """以指定(i,j)坐标为左上角，添加一个滑翔机图案"""
    glider = np.array([[0,0,255],[255,0,255],[0,255,255]])
    grid[i:i+3,j:j+3] = glider

# 生成高斯帕滑翔机枪图案函数
def addGosperGun(i, j, grid):
    """以指定(i,j)坐标为左上角，添加一个高斯帕滑翔机枪图案"""
    gun = np.zeros(11 * 38).reshape(11, 38)

    gun[5][1] = gun[5][2] = 255
    gun[6][1] = gun[6][2] = 255

    gun[3][13] = gun[3][14] = 255
    gun[4][12] = gun[4][16] = 255
    gun[5][11] = gun[5][17] = 255
    gun[6][11] = gun[6][15] = gun[6][17] = gun[6][18] = 255
    gun[7][11] = gun[7][17] = 255
    gun[8][12] = gun[8][16] = 255
    gun[9][13] = gun[9][14] = 255

    gun[1][25] = 255
    gun[2][23] = gun[2][25] = 255
    gun[3][21] = gun[3][22] = 255
    gun[4][21] = gun[4][22] = 255
    gun[5][21] = gun[5][22] = 255
    gun[6][23] = gun[6][25] = 255
    gun[7][25] = 255

    gun[3][35] = gun[3][36] = 255
    gun[4][35] = gun[4][36] = 255

    grid[i:i + 11, j:j + 38] = gun

# 刷新游戏图像
def update(frameNum,img,grid,N):
    # 复制网格进行遍历，根据每个'细胞'周遭邻居情况以对应法则判断其存活情况
    newGrid = grid.copy()
    # 遍历整个N*N网格，range(N) - 从0~N
    for i in range(N):
        for j in range(N):
            # 根据环形边界条件，模拟计算每个'细胞'周围邻居的存活数(通过计算八个相邻'细胞'的值总和除以生存标识255活动)
            total = int((
                        grid[i,(j-1)%N]       + grid[i,(j+1)%N]       + grid[(i-1)%N,j]       + grid[(i+1)%N,j] +
                        grid[(i-1)%N,(j-1)%N] + grid[(i+1)%N,(j-1)%N] + grid[(i-1)%N,(j+1)%N] + grid[(i+1)%N,(j+1)%N]
                        )/255)
            # 根据Conway's rules判断该'细胞'自身的存活情况
            if grid[i,j] == ON:
                if(total<2) or (total>3):
                    newGrid[i,j] = OFF
            else:
                if total == 3:
                    newGrid[i,j] = ON
    # 更新数据
    img.set_data(newGrid)
    # 以切片形式把更新网格结果存回原网格
    grid[:] = newGrid[:]
    return img

# 主函数流程
def main():
    # 调用argparse模块自定义命令行参数解析
    descriptionStr = "Runs Conway's Game of Life simulation."
    parser = argparse.ArgumentParser(description = descriptionStr)
    # 添加参数解析,dest属性代表参数别名.如N == gridsize
    parser.add_argument('--gridsize',dest='N',required=False)
    parser.add_argument('--interval', dest='interval', required=False)
    parser.add_argument('--glider', action='store_true', required=False)
    parser.add_argument('--movfile',dest='movfile',required=False)
    parser.add_argument('--gosperGun',action='store_true',required=False)
    # 提交解析，返回前台具体输入命令
    args = parser.parse_args()

    # 默认网格大小
    N = 100
    # 设置网格大小
    if args.N and int(args.N)>8:
        N = int(args.N)

    # 默认刷新间隔
    updateInterval = 50
    # 设置刷新间隔
    if args.interval:
        updateInterval = int(updateInterval)

    # 判断网格创建方式,首先先创建一个空的数组对象表示网格
    grid = np.array([])
    # 用户输入glider标识,添加滑翔机图像进入网格进行模拟
    if args.glider:
        grid = np.zeros(N*N).reshape(N,N)
        addGlider(1,1,grid)
    # 用户输入gosper标识,添加高斯帕滑翔机枪图像进入网格进行模拟
    elif args.gosperGun:
        grid = np.zeros(N*N).reshape(N,N)
        addGosperGun(1,1,grid)
    # 用户未输入,随机值创建网格进行模拟
    else:
        grid = randomGrid(N)

    # 创建图像
    # 调用subplots()创建子图
    fig,ax = pyplot.subplots()
    # 绘制网格图像
    img = ax.imshow(grid,interpolation='nearest')
    # 调用animation模块动态绘图
    ani = animation.FuncAnimation(fig,update,fargs=(img, grid, N, ),frames=10,interval=updateInterval,save_count=50)

    if args.movfile:
        ani.save(args.movfile,fps=30,extra_args=['-vcodec','libx264'])

    # 表示出图像
    pyplot.show()

# 调用主函数
if __name__ == '__main__':
    main()