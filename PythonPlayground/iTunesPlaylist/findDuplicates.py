#coding=utf-8
#2017.6.13
#By JerCas

# 导入plist文件解析模块
import plistlib

def findDuplicates(fileName):
    """查找重复曲目"""
    print("Finding duplicate tracks in "+ fileName +" ...")
    # 读取播放列表
    # P-list文件将对象表示为字典，而列表文件使用的是一个字典的字典（值仍为一个字典）;readPlist读入一个P-list文件作为输入，返回一个顶层字典
    plist = plistlib.readPlist(fileName)
    # 从播放列表字典中获取Tracks健的值——声轨字典存为tracks
    tracks = plist['Tracks']
    # 创建存储重复声轨的空字典
    trackNames = {}
    # 循环迭代声轨字典，获取声轨名、声轨长度，trackId-key track-value（tracks是一个字典字典，而其value是一个字典）
    for trackId,track in tracks.items():
        try:
            # 获取声轨字典中声轨名和声轨长度，这两个key的value
            name = track['Name']
            duration = track['Total Time']
            # 在存储重复声轨字典中查找该声轨名是否已在其中
            if name in trackNames:
                # 如已在其中，则对声轨长度做二次比较，若也符合则证明重复
                # //整除，将音轨长度除以1000，将秒转换为毫秒
                if duration//1000 == trackNames[name][0]//1000:
                    # 获取重复计数count（trackNames value中的存储顺序为0：duration,1:count）
                    # 故用trackNames[key][index]获取对应位置的值
                    count = trackNames[name][1]
                    # 将重复次数+1,修改重复音轨字典中对应的key的value——音轨重复次数
                    trackNames[name] = (duration,count+1)
                else:
                    # 第一次遇到该音轨，将（duration,count）作为元祖值存入重复声轨字典的对应key-name中
                    trackNames[name] = (duration,1)
        except:
            # 忽略没有定义名称的音轨
            pass

    # 将重复音轨作为一个（name，count）元祖存储在列表中
    dups = []
    # 循环迭代重复声轨字典
    for key,value in trackNames.items():
        # 重复次数大于1，说明有重复
        if value[1]>1:
            # 加入重复声轨列表中
            dups.append((value[1],key))
        # 将重复声轨信息存储到文本信息中(有重复信息的情况下)
    if len(dups)>0:
        print("Found "+str(len(dups))+" duplicates. Track names saved to dup.txt")
    else:
        print("No duplicate tracks found!")
    f = open("dups.txt","w")
    for val in dups:
        f.write("[" + val[0] + "]" + + val[1] + "\n")
    f.close()