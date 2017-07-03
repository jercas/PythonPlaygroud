#coding=utf-8
#2017-6-15
#By JerCas

import re,argparse
import sys
from findDuplicates import findDuplicates
from findCommonTracks import findCommonTrakcs
from plotStats import plotStats

def main():
    # 创建解析对象说明
    descStr = """This program analyzes playlist files (.xml) exported from iTunes."""
    # 创建解析对象
    parser = argparse.ArgumentParser(description=descStr)
    # 添加互斥（mutually exclusive）参数分组
    group = parser.add_mutually_exclusive_group()

    # 添加存入解析值的参数变量名
    # 分别键入三个处理函数的解析值参数
    # 该部分详见evernote/jercas0618@163.com
    # nargs表示该参数可处理（？——'1个/不需要'、+——'多余一个'、*——'任意个'、n——'指定个数'）键入值
    # dest相当于把 该参数关联到一个特点名词，可理解为 common=plFiles,stats=plFile,dup=plFileD
    # 故下文选择参数判断时，所用的是arg.plFiles而非arg.common
    group.add_argument('--common',nargs='*',dest='plFiles',required=False)
    group.add_argument('--stats',dest='plFile',required=False)
    group.add_argument('--dup',dest='plFileD',required=False)

    # 实际解析操作，将用户传入的指令进行解析，获取具体操作函数进行判别操作
    args = parser.parse_args()

    # 判别调用函数
    if args.plFiles:
        # find common tracks
        findCommonTrakcs(args.plFiles)
    elif args.plFile:
        # plot stats
        plotStats(args.plFile)
    elif args.plFileD:
        # find duplicate tracks
        findDuplicates(args.plFileD)
    else:
        print("These are not the tracks you are looking for!")

if __name__ == '__main__':
    main()