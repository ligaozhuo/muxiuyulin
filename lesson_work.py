# -*- coding:utf-8 -*-
__author__ = 'ligaozhuo'

import os
import pandas as pd
import numpy as np
import PySimpleGUI as sg 
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import csv
import re

class fengxiandimianguance:
    def __init__(self, filepath, sheetpath):
        self.filepath = filepath#用于实例化对象
        self.sheetpath=sheetpath
        self.df = self.parse()

    def parse(self):
        try:
            df = pd.read_excel(self.filepath, encoding="utf-8",sheet_name=self.sheetpath)
        except:
            df = pd.read_excel(self.filepath, encoding="GBK")
        """存在文件编码方式不同的情况,使用异常处理"""
        col = list(df.columns)
        col = [i.strip() for i in col]
        df.columns = col 
        
    def day_month(self,dayofmonth):
        if dayofmonth=='2009/02':
            x=list(pd.date_range(dayofmonth, periods=28, freq='d'))
        elif dayofmonth=='2009/11':
            x=list(pd.date_range(dayofmonth, periods=30, freq='d'))
        elif dayofmonth=='2009/04':
            x=list(pd.date_range(dayofmonth, periods=30, freq='d'))
        elif dayofmonth=='2009/06':
            x=list(pd.date_range(dayofmonth, periods=30, freq='d'))
        elif dayofmonth=='2009/09':
            x=list(pd.date_range(dayofmonth, periods=30, freq='d'))            
        else:
            x=list(pd.date_range(dayofmonth, periods=31, freq='d'))
        return x

    def plot_show(self, time, element,daymonth):

        io=self.filepath

        if element=='最大风风速（m/s）':
            df = pd.read_excel(io,sheet_name=self.sheetpath)
            
            """ df.replace('ppc', '0', inplace = True)
                data=df.loc[:,'2分钟平均风向（度）']
                print(data.head(40)) """
            col = list(df.columns)
            col = [i.strip() for i in col]
            df.columns = col 

            time_data=df.loc[:,'最大风出现时间']#获取全部的时间
            b=[t for t in time_data if t==t]
    
            onedaytime_data = list(filter(lambda x: re.match(time, x) != None, b))  
            data=[]
            for i in onedaytime_data:
                data.append(list(df.loc[df['最大风出现时间']==i,'最大风风速（m/s）']))
            a=np.asarray(data)
            c=a.ravel()#扁平化
            time1=np.asarray(daymonth)
            plt.plot(time1,c)
            plt.title("Line chart，min is:")
            plt.xlabel("time",fontsize=14)
            plt.ylabel("ph",fontsize=14)
            plt.show()
            #plt.savefig('one.png')
        else:
            df = pd.read_excel(io,sheet_name=self.sheetpath)
            col = list(df.columns)
            col = [i.strip() for i in col]
            df.columns = col 
            time_data=df.loc[:,'时间']#获取全部的时间
            onedaytime_data = list(filter(lambda x: re.match(time, x) != None, time_data))  # 正则表达式匹配时间，同时生成新列表(注意1号后面有空格，用以符合匹配)  
            data=[]
            for i in onedaytime_data:
                data.append(list(df.loc[df['时间']==i, element]))
            a=np.asarray(data)
            c=a.ravel()#扁平化
            b=[t for t in c if t==t]
        
            x=list(pd.date_range(time, periods=24, freq='H'))#不包括stop
            time2=np.asarray(x)

            if len(b)<24:
                plt.scatter(time2,c)
                plt.title("Line chart，min is:")
                plt.xlabel("time",fontsize=14)
                plt.ylabel("ph",fontsize=14)
                plt.show()

            else:    
                plt.plot(time2,c)
                plt.title("Line chart，min is:")
                plt.xlabel("time",fontsize=14)
                plt.ylabel("ph",fontsize=14)
                plt.show()#这里加上plt.savefig('one.png'),不加的话会再次显示之前的图片


    def show_image(self,one):
        sg.change_look_and_feel('Dark Blue 3')
        layout = [[sg.Image(r'.\one.png')]]#打开test.png
        window = sg.Window(f"{one}曲线图", layout)
        while True:
            event, values = window.read()#事件，获得的值为窗口的输入（或者是读取得到的）
            if event in (None, 'Cancel'):  # if user closes window or clicks cancel
                break            

if __name__ == '__main__':
    # m1 = fengxiandimianguance(r"C:/Users/Win7Dev1/Desktop/54511-AD-2018-07-05LV2.csv")
    # m1.plot_show(11, "2018/07/05 00:00")


    sg.change_look_and_feel('Dark Blue 3')  # Add a touch of color
    # All the stuff inside your window.
   
    layout = [[sg.Text('地面观测数据要素某天折线图')],
              [sg.Text('请选择文件',size=(15, 1)), sg.Input(), sg.FileBrowse()],#0,1,2,3
              [sg.Text('请选择类型',size=(15, 1)),sg.InputCombo(('气压', '气温','湿球温度','水气压','相对湿度','风','浅层地温'),size=(15, 1))],
              [sg.Text('请输入时间',size=(15, 1)), sg.InputText(tooltip='如：2009/01/1')],
              [sg.Text('请选择相关要素',size=(15, 1)),sg.InputCombo(('本站气压（hPa）', '气温（℃）','露点温度（℃）','水汽压（hPa）','相对湿度（%）','水气压',
              '相对湿度','2分钟平均风向（度）','2分钟平均风速（m/s）','10分钟平均风向（度）','10分钟平均风速（m/s）','最大风风速（m/s）'),size=(15, 1))],
              [sg.Ok(), sg.Cancel()]]

    # Create the Window
    window = sg.Window('创新实践', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event in ( None,'Cancel'):  # if user closes window or clicks cancel
            break
        
        m1 = fengxiandimianguance(values[0],values[1])
        t1=m1.day_month(values[2])#t1
        m1.plot_show(values[2],values[3],t1)
        #m1.show_image(values[3])#在这里就不用保存的图片进行显示，而是直接显示
        
    window.close()
