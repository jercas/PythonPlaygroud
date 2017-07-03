#coding=utf-8
#2017.6.14
#By JerCas

import plistlib

def findCommonTrakcs(fileNames):
    """查找多个播放列表中的共同音轨"""
    # 创建一个空的列表，存储音轨名
    trackNameSets = []
    # 遍历传入的播放列表
    for fileName in fileNames:
        # 创建一个空的集合（无序，不重复元素集）,以此来剔除单个播放列表自身的重复音轨
        trackNames = set()

        # 将传入的p-list格式播放列表解析
        plist = plistlib.readPlist(fileName)
        # 获取tracks字典
        tracks = plist['Tracks']

        # 迭代遍历tracks字典
        for trackId,track in tracks.items():
            try:
                # 将音轨名加入set集合中
                trackNames.add(track['Name'])
            except:
                # 忽略未命名音轨
                pass

    # 将音轨集合加入音轨列表中
    # 此时经set集合处理后，该trackNames集合中已无重复音轨名
    trackNameSets.append(trackNames)

    # 获取集合之间（播放列表之间）的重复音轨名
    # 利用set集合的求交集操作来完成
    # 利用*操作符来展开参数列表，将列表切割为多个单个元素
    commonTracks = set.intersection(*trackNameSets)

    # 将运算结果写入文本文件中
    if len(commonTracks) > 0:
        f = open("common.txt","wb+")
        for val in commonTracks:
            s = " " + val + " \n"
            f.write(s.encode("UTF-8"))
        f.close()
        print("" + str(len(commonTracks)) + "common tracks found."
             + "\nTrack names written to common.txt.")
    else:
        print("No common trakcs!")


