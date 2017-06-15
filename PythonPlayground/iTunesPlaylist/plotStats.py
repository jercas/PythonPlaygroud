#coding=utf-8
#2017-6-14
#By JerCas

from matplotlib import pyplot
import plistlib
import numpy

def plotStats(fileName):
    """收集音轨的评分和时长"""
    # 将传入的p-list格式播放列表解析
    plist = plistlib.readPlist(fileName)
    # 获取tracks字典
    tracks = plist['Tracks']

    # 创建两个空列表，分别保存歌曲评分和音轨时长
    ratings = []
    durations = []
    # 遍历音轨字典
    for trackId,track in tracks.items():
        try:
            ratings.append(track["Album Rating"])
            durations.append(track["Total Time"])
        except:
            # 忽略未命名音轨
            pass

    # 检查上述数据是否收集完成
    if ratings == [] or durations == []:
        print("No valid Album Rating/Total Time data in "+ fileName +" ")
        return

    # 数据绘图部分
    # 调用numpy将音轨时长数据放到32位整数数组中
    x = numpy.array(durations,numpy.int32)
    y = numpy.array(ratings,numpy.int32)
    # 将音轨时长转换位毫秒到位，以整体数组进行操作运作到其中每个元素中
    x = x/60000.0

    # subplot(nrows, ncols, plot_number)参数定义为，所绘制图有  2行-1列-下一个点应绘制在第1行
    pyplot.subplot(2,1,1)
    # plot()以参数x,y位置创建一个点，并用o表示用圆圈来绘制数据
    pyplot.plot(x,y,'o')
    # axis()将x轴、y轴设置的略微大一点儿范围，以便在图和轴之间留一些空间
    pyplot.axis([0,1.05*numpy.max(x),-1,110])
    # xlabel()、ylabel()，为x轴、y轴设置说明文字
    pyplot.xlabel('Track duration')
    pyplot.ylabel('Track rating')

    # 绘制柱状图
    pyplot.subplot(2,1,2)
    # hist（)在同一张图中的第二行中，绘制时长直方图；其中bins参数设置数据分区个数，每个分区用于添加在整个范围内的计数
    pyplot.hist(x,bins=20)
    pyplot.xlabel('Track duration')
    pyplot.ylabel('Count')
    # 于窗口中绘制图形
    pyplot.show()