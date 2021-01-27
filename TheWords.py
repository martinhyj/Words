#-*- coding:utf-8 -*-
'''
Author: martin
Date: 2020-10-06 15:32:25
LastEditTime: 2021-01-21 23:17:12
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /py/practice/TheWords.py
'''



import json
import os
import random
import sqlite3
from datetime import timedelta,datetime
from sqlite3 import *

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

wordtables=["WORD_KAOYAN","WORD_CET4","WORD_CET6"] #单词表
word_content=["KaoYan_3.json","CET4_3.json","CET6_3.json"]

class word:
    '''
        单词类
    '''
    def __init__(self, name, c_name,master_index=0,review_times=0):
        self.name=name  #单词名
        self.c_name=c_name #单词释义
        # master->(0,5) 
        self.master_index=master_index
        self.review_times=review_times
    
    def storage(self,wordbase_id):
        '''
        将单词信息存储到数据库
        '''
        #连接 本地数据库mysql
        mydb=connect_sqlite()
        print("连接成功-储存单词")

        #插入单词信息
        cursor=mydb.cursor()
        sql_insert="INSERT INTO "+wordtables[wordbase_id]+"(\
            word, explain, master_index, times,last_time)\
            VALUES ('%s', '%s', %s, %s,'%s')" %(self.name, self.c_name, self.master_index, self.review_times,gettime())
        try:
            cursor.execute(sql_insert)
            mydb.commit()
            print("保存成功")
        except IntegrityError as error:
            mydb.rollback()
            print(error)
        
        cursor.close()
        mydb.close()
    
    
    def findword(a_word,wordbase_id):
        '''
        查询一个单词是否在数据库中
        '''
        mydb=connect_sqlite()
        print("连接成功-search单词")
        cursor=mydb.cursor()

        sql = "SELECT * FROM "+wordtables[wordbase_id]+\
        "WHERE word = '%s' " %(a_word)
        try:
         # 执行SQL语句
          cursor.execute(sql)
         # 获取一条记录
          if cursor.fetchone():
              return True
        except OperationalError as error:
           print (error)
        
        mydb.close()
        return False

    
    def getword_index(wordbase_id):
        '''
        根据index属性，随机从词库中抽取index<3的单词
        '''
        
        #连接 本地数据库mysql
        word=[]
        mydb=connect_sqlite()
        print("连接成功-抽取单词")
        cursor=mydb.cursor()
        sql_select="SELECT * FROM "+self.wordtables[wordbase_id]+\
            "WHERE master_index < %s"%(3)
        try:
            cursor.execute(sql_select)
            result=cursor.fetchall()
        except InternalError as error:
            print(error)
            print ("Error: unable to fetch data")
        
        mydb.close()
        n=len(result)
        return result[random.randint(0,n-1)]
    
    
    def getword_date(wordbase_id):
        '''
        根据单词添加的时间随机从词库中得到一个单词(7天前)
        '''
        #连接 本地数据库mysql
        # 获取14天前的时间

        mydb=connect_sqlite()
        print("连接成功-抽取单词")
        cursor=mydb.cursor()
        sql_select="SELECT * FROM "+wordtables[wordbase_id]
        try:
            cursor.execute(sql_select)
            result=cursor.fetchall()
        except InternalError as error:
            print(error)
            print ("Error: unable to fetch data")
        
        mydb.close()
        # print(result)
        n=len(result)
        return result[random.randint(0,n-1)]
        return result

    
    def getword_Ebbinghaus(wordbase_id):
        '''
        根据艾宾浩斯遗忘曲线记忆单词
        '''
    
        #连接本地数据库mysql
        # 获取14天前的时间
        mydb=connect_sqlite()
        print("连接成功-抽取单词")
        cursor=mydb.cursor()
        sql_select="SELECT * FROM "+wordtables[wordbase_id]
        try:
            cursor.execute(sql_select)
            result=cursor.fetchall()
        except InternalError as error:
            print(error)
            print ("Error: unable to fetch data")
        
        mydb.close()
        result=Ebbinghaus(result)
        n=len(result)
        return result[random.randint(0,n-1)]

    
    def word_update(updated_word,interval,wordbase_id):
        '''
        更新单词状态：
        1:单词每复习一次，属性复习次数加一
        2:根据用户记忆该单词的时间，计算出该单词的熟练指数
        '''
        mydb=connect_sqlite()
        print("连接成功-更新单词")
        change=get_change(interval,updated_word,wordbase_id)
        cursor=mydb.cursor()
        sql_update="UPDATE "+wordtables[wordbase_id]+"\
            SET times = times + 1,\
                master_index=%s\
            WHERE word = '%s' " %(change,updated_word)
        try:
            cursor.execute(sql_update)
            mydb.commit()
            print("更新成功")
        except InternalError as error:
            print(error)
        
        mydb.close()
    
    
    def redesign(a_word, explain,wordbase_id):
        '''
        解决释义错误的问题
        '''
        mydb=connect_sqlite()
        print("连接成功-更新单词")
        cursor=mydb.cursor()
        sql_update="UPDATE "+wordtables[wordbase_id]+"\
            SET explain='%s'\
            WHERE word = '%s' " %(explain,a_word)
        try:
            cursor.execute(sql_update)
            mydb.commit()
            print("修改成功")
        except InternalError as error:
            print(error)
        mydb.close()

    def word_length_static(wordbase_id):
        '''
        统计词库内单词长度
        '''
        mydb=connect_sqlite()
        cursor=mydb.cursor()
        sql_select="SELECT * FROM "+wordtables[wordbase_id]
        try:
            cursor.execute(sql_select)
            result=cursor.fetchall()
        except InternalError as error:
            print(error)
            print ("Error: unable to fetch data")
        mydb.close()

        length_list=[]
        length_static=[]
        length_count=[]
        for word in result:
            length_list.append(len(word[0]))
        max_length=max(length_list)

        for n in range(1,max_length+1):
            length_static.append(n)
            length_count.append(length_list.count(n))
        max_count=max(length_count)

        #添加自己的字体，matplotlib不支持中文
        myfont=matplotlib.font_manager.FontProperties \
        (fname=os.path.dirname(os.path.abspath(__file__))+"/Fonts/书法.ttf")
        matplotlib.rcParams['axes.unicode_minus'] =False
    
        #创建一个全局绘图区域
        plt.figure("static",figsize=(6,4),clear=True)
        plt.plot(length_static,length_count,'--*r')#红色，虚线，五角星为节点 
        plt.xlim(1,max_length+1)
        plt.ylim(0,max_count+100)
        plt.xlabel("length",fontproperties=myfont)
        plt.ylabel("count",fontproperties=myfont)
        plt.title("单词长度统计"+"(单词总数:{})".format(len(result)),fontproperties=myfont)
        plt.show()

    
    def search_by_explain(search_word,wordbase_id):
        '''
        根据关键字，查询类似释义的单词
        '''
        mydb=connect_sqlite()
        print("连接成功-抽取单词")
        cursor=mydb.cursor()
        sql_select="SELECT * FROM "+wordtables[wordbase_id]
        
        try:
            cursor.execute(sql_select)
            result=cursor.fetchall()
        except InternalError as error:
            print(error)
            print ("Error: unable to fetch data")
        
        mydb.close()

        search_list=[]
        for word in result:
            if Jaccard_distance(split_explain(word[1]),split_explain(search_word))<0.9:
                search_list.append(word)
        
        if len(search_list)==0:
            return None
        else:
            return search_list
        
    def getWord_Length(wordbase_id, length):
        '''
            根据单词长度抽取单词
        '''
        aim_list=[]
        mydb=connect_sqlite()
        print("连接成功-抽取单词")
        cursor=mydb.cursor()
        sql_select="SELECT * FROM "+wordtables[wordbase_id]
        try:
            cursor.execute(sql_select)
            result=cursor.fetchall()
        except InternalError as error:
            print(error)
            print ("Error: unable to fetch data")
        
        mydb.close()
        n=len(result)
        for wd in result:
            if len(wd[0])==length:
                aim_list.append(wd)
        n=len(aim_list)
        if n==0:
            return ("NONE","none",999,999,"1999-4-9")
        else: return aim_list[random.randint(0,n-1)]

def get_detail(word,wordbase_id):
    '''
        返回一个单词的详细信息，以字符串方式返回
    '''
    with open(os.path.dirname(os.path.abspath(__file__))+"/json/"+word_content[wordbase_id],'r',encoding="utf-8") as file:
        for WORD in file.readlines():
            config=json.loads(WORD)
            result=""
            if config["headWord"]==word:
                # print(WORD)
                # 音标
                try:
                    us="[" + config["content"]["word"]["content"]["usphone"]+ "] "
                    uk="["+config["content"]["word"]["content"]["ukphone"]+"]\n"
                except KeyError:
                    print("音标error")
                # 翻译
                trans_cn=""
                for trans in config["content"]["word"]["content"]["trans"]:
                    trans_cn+=trans['pos']+" "+ trans["tranCn"]+"\n"
    
                # 短语:
                try:
                    pharses=config["content"]["word"]["content"]["phrase"]["desc"]+":\n"
                    index=1
                    for pharse in config["content"]["word"]["content"]["phrase"]["phrases"]:
                        pharses+="{}. ".format(index)+pharse["pContent"]+" "+pharse["pCn"]+"\n"
                        index+=1
                except KeyError:
                    print("没有相关短语")
                    pharses=""

                # 相关联词
                try:
                    rels=config["content"]["word"]["content"]["relWord"]["desc"]+":\n"
                    for rel in config["content"]["word"]["content"]["relWord"]["rels"]:
                        rels+=rel["pos"]+". "
                        for word in rel["words"]:
                            rels+=word["hwd"]+":"+word["tran"]+"\n"
                except KeyError:
                    print("没有相关联单词")
                    rels=""
                # 例句
                try:
                    example=config["content"]["word"]["content"]["sentence"]["desc"]+":\n"
                    for sen in config["content"]["word"]["content"]["sentence"]["sentences"]:
                        example+=sen["sContent"]+"\n"
                        example+=sen["sCn"]+"\n"
                except KeyError:
                    print("没有相关例句")
                    example=""
                # 同义词
                try:
                    synos=config["content"]["word"]["content"]["syno"]["desc"]+":\n"
                    for syno in config["content"]["word"]["content"]["syno"]["synos"]:
                        synos+=syno["pos"]+". "+syno["tran"]+"\n"
                        for word in syno["hwds"]:
                            synos+=word["w"]+","
                        synos+="\n"
                except KeyError:
                    print("没有相关同义字")
                    synos=""
                result=us+uk+trans_cn+"\n"+pharses+"\n"+rels+"\n"+example+"\n"+synos
                return result

        return None


def getRelWords(word,wordbase_id):
    '''
        返回一个单词相关联单词的列表
    '''
    rels_list=[word]
    with open(os.path.dirname(os.path.abspath(__file__))+"/json/"+word_content[wordbase_id],'r',encoding="utf-8") as file:
        for WORD in file.readlines():
            config=json.loads(WORD)
            if config["headWord"]==word:
                # print(config)
                try:
                    rels=config["content"]["word"]["content"]["relWord"]["rels"]
                except KeyError:
                    return rels_list
                for rel in rels:
                   for hwd in rel["words"]:
                       rels_list.append(hwd["hwd"])
                break
    return rels_list

    
def getWord(word,wordbase_id):
    
    mydb=connect_sqlite()
    print("连接成功-抽取单词")
    cursor=mydb.cursor()
    sql_select="SELECT * FROM "+wordtables[wordbase_id]+"\
        WHERE word = '%s' "%(word)
    try:
        cursor.execute(sql_select)
        result=cursor.fetchall()
    except InternalError as error:
        print(error)
        print ("Error: unable to fetch data")
    
    mydb.close()
    return result[0]
        
def connect_sqlite():
    '''
    连接sqlite数据库文件
    '''
    sqlite=sqlite3.connect(os.path.dirname(os.path.abspath(__file__))+"/data/word.sqlite")
    return sqlite

def gettime():
    ''''
    获取当前的时间，年月日
    '''
    now=datetime.datetime.now()
    time=now.date().isoformat()
    # print(type(time))
    # print(time)
    return time
        

def get_change(interval,word,wordbase_id):
    '''
    根据用户单次记忆该单词的时间，计算出该单词的熟练指数
    '''
    index=0
    length=len(word)
    WORD=getWord(word,wordbase_id)
    explain_length=len(split_explain(WORD[1]))

    if 10>=interval>0:
        # 熟悉的单词
        index=5
        # 非常不熟悉的单词
        if WORD[2]<2 and WORD[3]<5:
            index-=3

    elif 14>=interval>10:
        index=4
        # 简单词汇
        if length<=5:
            index+=1
    elif 18>=interval>14:
        index=3
        # 有一定掌握度和复习次数
        if WORD[2]>=4 and WORD[3]>=5:
            index+=1

    elif 30>=interval>18:
        index=2
        # 有一定掌握度和复习次数
        if WORD[2]>=4 and WORD[3]>=5:
            index+=1

    elif 40>=interval>30 and interval<40:
        index=1
        # 单词释义较长 
        if explain_length>6:
            index+=2
        # 单词长度>=12
        if length>=12:
            index-=1
            
    elif interval>40:
        # 不熟练单词
        index=0
        # 因其他因素造成的interval过长
        if WORD[2]>=4 and WORD[3]>=5:
            index=3

    return index


def Ebbinghaus(word_list):
    '''
    根据艾宾浩斯遗忘曲线整理出需要记忆的单词
    '''
    short_memory=[5,30,60]  # 5,30,60 seconds
    long_memeory=[1,2,4,7,15,23,30] # 1,2,4,7,15,23,30 days
        
    Ebbinghaus_list=[]
    for word  in word_list:
        for day in long_memeory:
            day_interval=datetime.datetime.today()-timedelta(day)
            if day_interval.strftime("%Y-%m-%d")==word[4] :
                Ebbinghaus_list.append(word)
        
    return Ebbinghaus_list


def split_explain(str):
    '''
    分解单词释义到集合中
    '''
    word_set=set()
    for i in str.split(";"):
        for j in i.split("，"):
            word_set.add(j)
    return word_set


def show_tendency(word,wordbase_id):
    '''
        使用matplotlib展示单词在历年真题中出现的次数,
        将指定单词与每年统计的数据匹配,统计出该单词历年出现的曲线图
    '''
    if len(word)!=0:
        # 读取文件
        df=pd.read_csv(filepath_or_buffer=os.path.dirname(os.path.abspath(__file__))+"/csv/english.csv")
        
        rate1=[0,0,0,0,0,0,0,0,0,0,0]
        rate2=[0,0,0,0,0,0,0,0,0,0,0]
        year=[2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020]

        rels_list=getRelWords(word,wordbase_id)
        for WORD in rels_list:
            # 匹配出对应单词行
            result=df[df["word"]==WORD]
            # 分别提取出1,2的部分

            result_1=result[result["style"]=="英语一"]
            print(WORD)
            index=0
            for y in year:
                _y=result_1[result_1["year"]==y]
                rate1[index]+=_y["rate"].sum()
                index+=1

            result_2=result[result["style"]=="英语二"]
            index=0
            for y in year:
                _y=result_2[result_2["year"]==y]
                rate2[index]+=_y["rate"].sum()
                index+=1
            
        
        print(rate1)
        print(rate2)
        print(year)
        # 添加自己的字体，matplotlib不支持中文
        myfont=matplotlib.font_manager.FontProperties \
        (fname=os.path.dirname(os.path.abspath(__file__))+"/Fonts/书法.ttf")
        matplotlib.rcParams['axes.unicode_minus'] =False

        # 创建一个全局绘图区域
        plt.figure("tendency",figsize=(6,4),clear=True)
        # 第一个子区域
        # plt.subplot(111)
        plt.plot(year,rate1,'-*r',label="英语一")#红色，虚线，五角星为节点
        plt.plot(year,rate2,'-*b',label="英语二")#蓝色，虚线，五角星为节点  
        plt.legend(prop=myfont)
        # 设置范围
        plt.xlim(2009,2020)
        plt.xticks(range(2009,2020,1))
        plt.ylim(0,20)
        # 设置标签及字体
        plt.xlabel("年份",fontproperties=myfont)
        plt.ylabel("频率",fontproperties=myfont)
        plt.title(word+"历年出现的频率",fontproperties=myfont)
        # 展示
        plt.show()


def Jaccard_distance(set1,set2):
    '''
        根据jaccard距离,计算两个集合相似度
        d(x,y)=1-SIM(x,y)
    '''
    return 1-(len(set1&set2))/(len(set1|set2))



if __name__ == "__main__":
    # show_tendency('outbreak')
    # mydb=connect_mysql(3)
    # print(os.path.dirname(__file__))
    # print(getWord("insult",0))
    # print(getRelWords("dim"))

    # all_words=word.getword_date(0)
    # print(all_words)
    # mydb=connect_sqlite(0)
    # cursor=mydb.cursor()
    # for re in all_words:
    #     sql_insert="INSERT INTO WORD_KAOYAN(\
    #             word, explain, master_index, times,last_time)\
    #             VALUES ('%s', '%s', %s, %s,'%s')" %(re[0], re[1],re[2],re[3],re[4])
    #     cursor.execute(sql_insert)
    #     mydb.commit()
    # mydb.close()
    # print("保存成功")
    # print(dir(datetime.datetime))
    get_detail("sake")