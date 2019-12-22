# -*- coding:utf-8 -*-
__author__ = 'ligaozhuo'

import os
import pandas as pd
import numpy as np
import PySimpleGUI as sg 
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt#从包中导入item（可以是模块、子包、函数、类、变量）
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
        return df.columns ,df  
        
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
        #注意比较老的版本excel（如2003版）应该使用.xls。比较新的用.xlsx
        io=self.filepath
        
        if element=='最大风风速（m/s）':
            df = pd.read_excel(io,sheet_name=self.sheetpath)
            #以下语句是筛选掉ppc的（ppc用0代替，以方便画图），但是不知道为什么无法作用
            """ df.replace('ppc', '0', inplace = True)
                data=df.loc[:,'2分钟平均风向（度）']
                print(data.head(40)) """
            col = list(df.columns)#df.colums显示列名，list(df.colums)把列名做成一个列表赋给col
            #strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列
            col = [i.strip() for i in col]
            df.columns = col 
            #pandas的dropna()能够找到DataFrame类型数据的空值（缺失值），将空值所在的行/列删除后，将新的DataFrame作为返回值返回
            #dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)
            #inplace原地修改
            #df.dropna(inplace=True)


            #data=df.loc[[2,4]]#取2，4两行数据
            #data=df.loc[2:4,'2分钟平均风向（度）']#做切片处理也可以得到相关数据
            time_data=df.loc[:,'最大风出现时间']#获取全部的时间
            b=[t for t in time_data if t==t]
            ####获取某天气压的最大值lambda定义了一个匿名函数
            #filter() 函数用于过滤序列，过滤掉不符合条件的元素，返回由符合条件元素组成的新列表
            #filter(function, iterable)
            onedaytime_data = list(filter(lambda x: re.match(time, x) != None, b))  # 正则表达式匹配时间（这里匹配一个月的时间（在窗口输入2009/01）），同时生成新列表(注意1号后面有空格，用以符合匹配)  
            #print(onedaytime_data)

            data=[]
            for i in onedaytime_data:
                data.append(list(df.loc[df['最大风出现时间']==i,'最大风风速（m/s）']))
            a=np.asarray(data)#把list转换为数组。（注意data是一个list的list,即有[[],[],[]]的结构）#获取某一天的要素的全部数据
            c=a.ravel()#扁平化
            #print(c)
            #x=list(pd.date_range(values[2], periods=31, freq='d'))#不包括stop
            time1=np.asarray(daymonth)
            plt.figure(1)
            plt.plot(time1,c)
            plt.title("Line chart，min is:")
            plt.xlabel("time",fontsize=14)
            plt.ylabel("ph",fontsize=14)
            plt.show()
            #plt.savefig('one.png')
            """ elif element=='最大风风速（m/s）':
                    pass
                elif element=='极大风风向（度）':#需要注意这里是：time_data=df.loc[:,'极大风出现时间']#获取全部的时间
                    pass
                elif element=='极大风风速（m/s）':
                    pass
                else:
                pass """    
        else:
            df = pd.read_excel(io,sheet_name=self.sheetpath)
            col = list(df.columns)#df.colums显示列名，list(df.colums)把列名做成一个列表赋给col
            #strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列
            col = [i.strip() for i in col]
            df.columns = col 
            #pandas的dropna()能够找到DataFrame类型数据的空值（缺失值），将空值所在的行/列删除后，将新的DataFrame作为返回值返回
            #dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)
            #inplace原地修改
            #df.dropna(inplace=True)


            #data=df.loc[[2,4]]#取2，4两行数据
            #data=df.loc[2:4,'2分钟平均风向（度）']#做切片处理也可以得到相关数据
            time_data=df.loc[:,'时间']#获取全部的时间

            ####获取某天气压的最大值lambda定义了一个匿名函数
            #filter() 函数用于过滤序列，过滤掉不符合条件的元素，返回由符合条件元素组成的新列表
            #filter(function, iterable)
            onedaytime_data = list(filter(lambda x: re.match(time, x) != None, time_data))  # 正则表达式匹配时间，同时生成新列表(注意1号后面有空格，用以符合匹配)  
            #print(onedaytime_data)

            data=[]
            for i in onedaytime_data:
                data.append(list(df.loc[df['时间']==i, element]))
            a=np.asarray(data)#把list转换为数组。（注意data是一个list的list,即有[[],[],[]]的结构）#获取某一天的要素的全部数据
            c=a.ravel()#扁平化
            #print(c)
            #判断里面是不是有nan (not a number)
            b=[t for t in c if t==t]#nan不和任何值相等，包括本身#python中可以用math.isinf()与math.isnan()来判断数据是否为inf或nan。
        
            x=list(pd.date_range(time, periods=24, freq='H'))#不包括stop
            daytime2=np.asarray(x)
                

            if len(b)<24:
                plt.figure(1)
                plt.scatter(daytime2,c)
         
                plt.title("Line chart，min is:")
                plt.xlabel("time",fontsize=14)
                plt.ylabel("ph",fontsize=14)
                plt.show()

            else:    
                plt.figure(1)
                plt.plot(daytime2,c)
         
                plt.title("Line chart，min is:")
                plt.xlabel("time",fontsize=14)
                plt.ylabel("ph",fontsize=14)
                plt.show()#这里加上plt.savefig('one.png'),不加的话会再次显示之前的图片


    def plot_show_compare(self, time, element,daymonth,time1,daymonth1):
            #注意比较老的版本excel（如2003版）应该使用.xls。比较新的用.xlsx
            io=self.filepath
            
            if element=='最大风风速（m/s）':
                df = pd.read_excel(io,sheet_name=self.sheetpath)
                
                col = list(df.columns)#df.colums显示列名，list(df.colums)把列名做成一个列表赋给col
                #strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列
                col = [i.strip() for i in col]
                df.columns = col 
                
                time_data=df.loc[:,'最大风出现时间']#获取全部的时间
                b=[t for t in time_data if t==t]
                ####获取某天气压的最大值lambda定义了一个匿名函数
                #filter() 函数用于过滤序列，过滤掉不符合条件的元素，返回由符合条件元素组成的新列表
                #filter(function, iterable)
                onemonth_time_data = list(filter(lambda x: re.match(time, x) != None, b))  # 正则表达式匹配时间（这里匹配一个月的时间（在窗口输入2009/01）），同时生成新列表(注意1号后面有空格，用以符合匹配)  
        
                data=[]
                for i in onemonth_time_data:
                    data.append(list(df.loc[df['最大风出现时间']==i,'最大风风速（m/s）']))
                a=np.asarray(data)#把list转换为数组。（注意data是一个list的list,即有[[],[],[]]的结构）#获取某一天的要素的全部数据
                c=a.ravel()#扁平化



                onemonth_time_data1 = list(filter(lambda x: re.match(time1, x) != None, b))  # 正则表达式匹配时间（这里匹配一个月的时间（在窗口输入2009/01）），同时生成新列表(注意1号后面有空格，用以符合匹配)  
                #print(onedaytime_data)

                data1=[]
                for i in onemonth_time_data1:
                    data1.append(list(df.loc[df['最大风出现时间']==i,'最大风风速（m/s）']))
                a1=np.asarray(data1)#把list转换为数组。（注意data是一个list的list,即有[[],[],[]]的结构）#获取某一天的要素的全部数据
                c1=a1.ravel()#扁平化
                
                x1=np.asarray(daymonth)
                x2=np.asarray(daymonth1)
                plt.figure(2)
                plt.subplot(211)
                plt.plot(x1,c)
                plt.title("Line chart，min is:")
                plt.xlabel("time",fontsize=14)
                plt.ylabel("ph",fontsize=14)
                plt.subplot(212)
                plt.plot(x2,c1)
                plt.title("Line chart，min is:")
                plt.xlabel("time1",fontsize=14)
                plt.ylabel("ph",fontsize=14)
                plt.show()
                #plt.savefig('one.png')
               
                       
            else:
                df = pd.read_excel(io,sheet_name=self.sheetpath)
                col = list(df.columns)#
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

                onedaytime_data1 = list(filter(lambda x: re.match(time1, x) != None, time_data))  # 正则表达式匹配时间，同时生成新列表(注意1号后面有空格，用以符合匹配)  
                data1=[]
                for i in onedaytime_data1:
                    data1.append(list(df.loc[df['时间']==i, element]))
                a1=np.asarray(data1)
                c1=a1.ravel()#扁平化
                #b1=[t for t in c1 if t==t]
            

                x=list(pd.date_range(time, periods=24, freq='H'))#不包括stop
                daytime2=np.asarray(x)
                x1=list(pd.date_range(time1, periods=24, freq='H'))#不包括stop
                daytime3=np.asarray(x1)
                    

                if len(b)<24:
                    plt.figure(2)
                    plt.subplot(211)
                    plt.scatter(daytime2,c)
                    plt.title("Line chart，min is:")
                    plt.xlabel("time",fontsize=14)
                    plt.ylabel("ph",fontsize=14)

                    plt.subplot(212)
                    plt.scatter(daytime3,c1)
                    plt.title("Line chart，min is:")
                    plt.xlabel("time",fontsize=14)
                    plt.ylabel("ph",fontsize=14)
                    plt.show()

                else:    
                    plt.figure(2)
                    plt.subplot(211)
                    plt.plot(daytime2,c)
                    plt.title("Line chart，min is:")
                    plt.xlabel("time",fontsize=14)
                    plt.ylabel("ph",fontsize=14)
                    plt.subplot(212)
                    plt.plot(daytime3,c1)
                    plt.title("Line chart，min is:")
                    plt.xlabel("time",fontsize=14)
                    plt.ylabel("ph",fontsize=14)
                    plt.show()#这里加上plt.savefig('one.png'),不加的话会再次显示之前的图片


if __name__ == '__main__':
    # m1 = fengxiandimianguance(r"C:/Users/Win7Dev1/Desktop/54511-AD-2018-07-05LV2.csv")
    # m1.plot_show(11, "2018/07/05 00:00")


    sg.change_look_and_feel('Dark Blue 3')  # Add a touch of color
    # All the stuff inside your window.
    #0,1,2,3
    layout = [[sg.Text('地面观测数据要素某天(月)折线图')],
              [sg.Text('请选择文件',size=(15, 1)), sg.Input(), sg.FileBrowse()],
              [sg.Text('请选择类型',size=(15, 1)),sg.InputCombo(('气压', '气温','湿球温度','水汽压','相对湿度','风','浅层地温'),size=(15, 1))],
              [sg.Text('请输入时间',size=(15, 1)), sg.InputText(tooltip='如：2009/01，显示风相关要素的月变化。如2009/01/1 ，日的数字后有空格，显示相关要素日变化。还有显示日最高相关要素时是显示后一天的')],
              [sg.Text('请选择相关要素',size=(15, 1)),sg.InputCombo(('本站气压（hPa）','日最高气压（hPa）' ,'日最高气压出现时间','日最低气压（hPa）','日最低气压出现时间'
              '气温（℃）','日最高气温（℃）','日最高气温出现时间','日最低气温（℃）','日最低气温出现时间',
              '露点温度（℃）','水汽压（hPa）','相对湿度（%）','日最低相对湿度（%）','日最低相对湿度时间',
              '2分钟平均风向（度）','2分钟平均风速（m/s）','10分钟平均风向（度）','10分钟平均风速（m/s）','最大风风速（m/s）',
              '0cm段地温（℃）','5cm段地温（℃）','10cm段地温（℃）','15cm段地温（℃）','20cm段地温（℃）'),size=(15, 1))],
              [sg.Text('请输入比较时间',size=(15, 1)), sg.InputText(tooltip='如：2009/01，显示风相关要素的月变化。如2009/01/1 ，日的数字后有空格，显示相关要素日变化。还有显示日最高相关要素时是显示后一天的')],
              [sg.Ok(), sg.Cancel()]]
    #湿球温度选项不可用，但是可以把时间那一列复制到第一列可以。当然也可以再做一个类似于'最大风风速'时判断，具体见lot_show()
    #还有浅地层温度表格中，0cm段最高地温（℃），0cm段最低地温（℃）匹配不正确。应该是前面是温度，后面是日期。如有需要显示，可在表格把这两个调换一下名称即可
    #做月或者是日数据对比，画在在一个图里面展示对比（目前想到的方法）。
    # Create the Window
    window = sg.Window('地面观测', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event in ( None,'Cancel'):  # if user closes window or clicks cancel
            break
        """ if values[4]==None:
            m1 = fengxiandimianguance(values[0],values[1])# class 创建类的对象，创建类对象的过程又称为类的实例化。语法：类名(参数)

            #获取文件值（values其实就是一个list）#其实就是把参数传给用于实例化的_init_函数（方法）
            t1=m1.day_month(values[2])#t1
            t2=m1.day_month(values[4])
        
            m1.plot_show(values[2],values[3],t1)
           
        else: 
            m1 = fengxiandimianguance(values[0],values[1])# class 创建类的对象，创建类对象的过程又称为类的实例化。语法：类名(参数)
            t1=m1.day_month(values[2])#t1
            t2=m1.day_month(values[4])
            m1.plot_show_compare(values[2],values[3],t1,values[4],t2)
        #m1.show_image(values[3])#在这里就不用保存的图片进行显示，而是直接显示 """
        m1 = fengxiandimianguance(values[0],values[1])# class 创建类的对象，创建类对象的过程又称为类的实例化。语法：类名(参数)
        t1=m1.day_month(values[2])#t1
        t2=m1.day_month(values[4])
        m1.plot_show(values[2],values[3],t1)
        m1.plot_show_compare(values[2],values[3],t1,values[4],t2)
    window.close()
