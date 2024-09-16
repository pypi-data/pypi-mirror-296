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

        self.visualLogData = kwargs
        self.lineInfosOfFiles = kwargs["lineInfosFiles"]

        MatplotlibZoom.Show(callback=self.defaultShowCallback, rows = 1, cols = 1)

    def defaultShowCallback(self, fig: Figure, index):
        # https://matplotlib.org/stable/api/
        ax: Axes = fig.get_axes()[index]
        ax.set_xlabel("X")
        ax.set_ylabel("Y")

        print(self.visualLogData)

        for self.lineInfos in self.lineInfosOfFiles:
            if len(self.lineInfos) == 0:
                continue

            print(self.lineInfos[0])
            if len(self.visualLogData["xAxis"]) > 0:
                # 迭代第一行数据，相当于绘制多少条线，每一列相当于一条线，一行数据中由x轴和y轴组成
                #   1. i表示当前绘制第几条线
                #   2. x表示当前当前x轴索引
                for i in range(len(self.lineInfos[0])):
                    if i in self.visualLogData["dataIndex"]:
                        # 迭代x轴，主要是获取x轴索引，相当于用第j个x轴绘制第i个y轴
                        for j in range(len(self.visualLogData["xAxis"])):
                            x = self.visualLogData["xAxis"][j]                                               # 获取x索引
                            if (i == x) and (x in self.visualLogData["dataIndex"]):                          # 处理针对X轴绘图
                                # i == x的会进入这个if，但是数组长度不同不会处理
                                # datetime模式，只以日期为X轴，Y轴表示当前计数，正常的模式下X轴不处理
                                # if isinstance(self.lineInfos[0][i], datetime.datetime) and len(self.visualLogData["xAxis"]) == len(self.lineInfos[0]):
                                if isinstance(self.lineInfos[0][i], datetime.datetime) and len(self.visualLogData["dataIndex"]) == 1:
                                    pointCount = 0

                                    for s in self.lineInfos:
                                        pointCount += 1

                                        # 文字
                                        ax.text(s[x], pointCount + 0.2, str(pointCount), fontsize=9)
                                        # 圆点
                                        ax.plot(s[x], pointCount, 'o')
                                        # 虚线
                                        ax.plot([s[x], s[x]], [pointCount, 0], linestyle = 'dotted')
                            else:                                                                       # 用X轴索引数据绘制Y轴
                                # dataIndex表示必须要绘制的图，不一定包括X轴
                                if (i in self.visualLogData["dataIndex"]):
                                    # if
                                    #     绘制垂直线
                                    # else
                                    #     不绘制垂直线
                                    if isinstance(self.lineInfos[0][i], str):
                                        pointCount = 1

                                        for s in self.lineInfos:
                                            pointCount += 1

                                            # 文字
                                            ax.text(s[x], pointCount + 0.2, s[i], fontsize=9, rotation=90)
                                            # 圆点
                                            ax.plot(s[x], pointCount, 'o')
                                            # 虚线
                                            ax.plot([s[x], s[x]], [pointCount, 0], linestyle = 'dotted')
                                    else:
                                        ax.plot([s[x] for s in self.lineInfos], [s[i] for s in self.lineInfos])
                                        for s in self.lineInfos:
                                            ax.plot(s[x], s[i], 'o')

                                # 处理针对X轴绘制垂直线
                                if (x in self.visualLogData["dataIndex"]):
                                    for s in self.lineInfos:
                                        ax.plot([s[x], s[x]], [s[i], 0], linestyle = 'dotted')
            else:
                # 迭代第一行数据，相当于绘制多少条线，每一列相当于一条线
                for i in range(len(self.lineInfos[0])):
                    if i in self.visualLogData["dataIndex"]:
                        # ax.plot(range(len(self.lineInfos)), [s[i] for s in self.lineInfos], label = self.labels[i])
                        ax.plot(range(len(self.lineInfos)), [s[i] for s in self.lineInfos])

        ax.legend()

    def parseData(filePath, regex):
        print("parseData")
        
        return LogParser.logFileParser(
            filePath,
            regex.split("\n")
        )
