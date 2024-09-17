#!/usr/bin/env python3

import datetime

import VisualLog.LogParser as LogParser
import VisualLog.MatplotlibZoom as MatplotlibZoom

import matplotlib.pyplot as plot
from matplotlib.figure import Figure
from matplotlib.axes import Axes

class VisualLogPlot:
    """
    VisualLogPlot

    暂时不知道为什么Qt直接引用VisualLog、matplotlib会导致界面上的下拉框界面出问题，所以采用反射来处理解决
    """

    def __init__(self, kwargs):
        print("VisualLogPlot")

        # 清理matplotlib相关绘图，防止出现未知异常报错
        plot.close()

        MatplotlibZoom.Show(callback=VisualLogPlot.defaultShowCallback, rows = 1, cols = 1, args=kwargs)

    @classmethod
    def defaultShowCallback(clz, fig: Figure, index, args):
        """
        args:

        {
            'xAxis': [0],
            'dataIndex': [1],
            'lineInfosFiles': [
                [file data],
                [file data]
            ]
        }
        """

        # https://matplotlib.org/stable/api/
        ax: Axes = fig.get_axes()[index]
        ax.set_xlabel("X")
        ax.set_ylabel("Y")

        visualLogData = args

        if len(args["lineInfosFiles"]) == 0:
            return

        for fileInfo in args["lineInfosFiles"]:
            for lineInfos in fileInfo:
                if len(lineInfos) == 0:
                    continue

                # print(lineInfos[0])
                if len(visualLogData["xAxis"]) > 0:
                    # 迭代第一行数据，相当于绘制多少条线，每一列相当于一条线，一行数据中由x轴和y轴组成
                    #   1. i表示当前绘制第几条线
                    #   2. x表示当前当前x轴索引
                    for i in range(len(lineInfos[0])):
                        if i in visualLogData["dataIndex"]:
                            # 迭代x轴，主要是获取x轴索引，相当于用第j个x轴绘制第i个y轴
                            for j in range(len(visualLogData["xAxis"])):
                                x = visualLogData["xAxis"][j]                                               # 获取x索引
                                if (i == x) and (x in visualLogData["dataIndex"]):                          # 处理针对X轴绘图
                                    # i == x的会进入这个if，但是数组长度不同不会处理
                                    # datetime模式，只以日期为X轴，Y轴表示当前计数，正常的模式下X轴不处理
                                    # if isinstance(lineInfos[0][i], datetime.datetime) and len(visualLogData["xAxis"]) == len(lineInfos[0]):
                                    if isinstance(lineInfos[0][i], datetime.datetime) and len(visualLogData["dataIndex"]) == 1:
                                        pointCount = 0

                                        for s in lineInfos:
                                            pointCount += 1

                                            # 文字
                                            ax.text(s[x], pointCount + 0.2, str(pointCount), fontsize=9)
                                            # 圆点
                                            ax.plot(s[x], pointCount, 'o')
                                            # 虚线
                                            ax.plot([s[x], s[x]], [pointCount, 0], linestyle = 'dotted')
                                else:                                                                       # 用X轴索引数据绘制Y轴
                                    # dataIndex表示必须要绘制的图，不一定包括X轴
                                    if (i in visualLogData["dataIndex"]):
                                        # if
                                        #     绘制垂直线
                                        # else
                                        #     不绘制垂直线
                                        if isinstance(lineInfos[0][i], str):
                                            pointCount = 1

                                            for s in lineInfos:
                                                pointCount += 1

                                                # 文字
                                                ax.text(s[x], pointCount + 0.2, s[i], fontsize=9, rotation=90)
                                                # 圆点
                                                ax.plot(s[x], pointCount, 'o')
                                                # 虚线
                                                ax.plot([s[x], s[x]], [pointCount, 0], linestyle = 'dotted')
                                        else:
                                            ax.plot([s[x] for s in lineInfos], [s[i] for s in lineInfos])
                                            for s in lineInfos:
                                                ax.plot(s[x], s[i], 'o')

                                    # 处理针对X轴绘制垂直线
                                    if (x in visualLogData["dataIndex"]):
                                        for s in lineInfos:
                                            ax.plot([s[x], s[x]], [s[i], 0], linestyle = 'dotted')
                else:
                    # 迭代第一行数据，相当于绘制多少条线，每一列相当于一条线
                    for i in range(len(lineInfos[0])):
                        if i in visualLogData["dataIndex"]:
                            # ax.plot(range(len(lineInfos)), [s[i] for s in lineInfos], label = labels[i])
                            ax.plot(range(len(lineInfos)), [s[i] for s in lineInfos])

        ax.legend()

    def parseData(filePath, regex):
        print("parseData")
        
        return LogParser.logFileParser(
            [filePath],
            regex.split("\n")
        )
