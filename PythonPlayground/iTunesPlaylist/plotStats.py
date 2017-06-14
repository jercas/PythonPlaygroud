#coding=utf-8
#2017-6-14
#By JerCas

import plistlib

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