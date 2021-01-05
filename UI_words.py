#-*- coding:utf-8 -*-
'''
Author: martin
Date: 2020-10-06 19:54:02
LastEditTime: 2021-01-05 18:52:11
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /py/practice/UI_words.py
'''
import re
import time
import tkinter.messagebox
from tkinter import *
import tkinter.font as tf
import TheWords
import Word_voice
from TheWords import word
from TheWords import *
from Word_voice import youdao

# 自定义UI类
class window(Tk):
    
    def __init__(self, screenName=None, baseName=None, className='Tk', useTk=1, sync=0, use=None):
        super().__init__(screenName=screenName, baseName=baseName, className=className, useTk=useTk, sync=sync, use=use)
        
        #初始化主界面
        #变化的一些元素
        self.button1_state=False
        self.testword=("martin")
        # 记一个单词的开始时间与记下一个单词的间隔
        self.start_time=0
        self.end_time=0
        # 默认设置
        self.wordbase=0 #默认单词库为考研单词
        self.way=0  #默认记忆方式为随机记忆
        self.length=7 #默认记忆长度为7

        #子窗口对象
        self.detail_ui=None
        self.about_ui=None
        self.advise_word_ui=None
        self.help_ui=None
        self.set_length_ui=None

        # 构建菜单对象
        self.mymenu=Menu(self)

        self.mainmenu = Menu(self, tearoff=0)
        self.mymenu.add_cascade(label='查看', menu=self.mainmenu)
        self.mainmenu.add_command(label='查看单词详细信息', command=lambda:self.show_detail(self))
        # 在两个菜单选项中间添加一条横线
        self.mainmenu.add_separator()
        self.mainmenu.add_command(label="退出",command=self.quit)

        self.menu1=Menu(self.mymenu,tearoff=0)
        self.mymenu.add_cascade(label="Wordsbase",menu=self.menu1)
        self.menu1.add_command(label='考研',command=lambda:self.set_wordbase(0))
        self.menu1.add_command(label='四级',command=lambda:self.set_wordbase(1))
        self.menu1.add_command(label='六级',command=lambda:self.set_wordbase(2))
        self.menu1.add_command(label='高考',command=lambda:self.set_wordbase(3))

        self.menu2=Menu(self.mymenu,tearoff=0)
        self.mymenu.add_cascade(label="Ways",menu=self.menu2)
        self.menu2.add_command(label='随机抽取',command=lambda:self.set_way(0))
        self.menu2.add_command(label='艾宾浩斯',command=lambda:self.set_way(1))
        self.menu2.add_command(label='单词指数',command=lambda:self.set_way(2))
        self.menu2.add_command(label='单词长度',command=lambda:self.set_way(3)) 
        
        # 显示菜单
        self.helpmenu = Menu(self, tearoff=0)
        self.mymenu.add_cascade(label='help', menu=self.helpmenu)
        self.helpmenu.add_command(label='about', command=self.show_about)
        self.helpmenu.add_command(label='help', command=self.show_help)
        self.helpmenu.add_command(label='advise', command=self.show_advice)
        
        self.config(menu=self.mymenu)
        

        #标签宽度，与行数，及字体大小，对齐方式
        self.show_explain=Message(self,fg="blue", font=("黑体",20),width=300,justify='left')
        # self.show_explain.bind('<Button-1>',func=lambda event:self.show_detail(event))
        self.show_word=Label(self,fg="blue", font=("黑体",50),height=2,width=20)
        
        self.begain=StringVar(self)
        self.begain.set("记忆单词")
        self.show_index_value=Label(self,text='', fg='black',width=7,justify='center',font=("黑体",20))
        self.show_times_value=Label(self,text='', fg='black',width=7,justify='center', font=("黑体",20))
        
        #固定的一些与元素
        self.show_info=Label(self,text="一起记单词吧",fg="blue", font=("黑体",25),height=2)
        self.show_info.pack()
        # 图标
        render=PhotoImage(file="/Users/litao999/word/img/fayin1.gif")
        self.fayin=Label(self, image=render,cursor="mouse")
        self.fayin.image=render
        self.fayin.place(relx=0.73,rely=0.015)
        self.fayin.bind('<Button-1>',func=lambda event:self.play_Press(event,id=0))
        self.fayin.bind('<Button-2>',func=lambda event:self.play_Press(event,id=1))
        
        self.button1=Button(self,textvariable=self.begain,font=("黑体",25),fg='blue', cursor='mouse',command=lambda:self.start())
        self.button1.place(relx=0.15,rely=0.60)
        self.button2=Button(self,text='加入单词',font=("黑体",25),fg='blue',cursor='mouse',command=lambda:self.add_ui())
        self.button2.place(relx=0.5,rely=0.60)
        self.button3=Button(self,text='单词趋势',font=("黑体",25),fg='blue',cursor='mouse',command=lambda:TheWords.show_tendency(word=self.testword[0]))
        self.button3.place(relx=0.15,rely=0.68)
        self.button4=Button(self,text='查询趋势',font=("黑体",25),fg='blue',cursor='mouse',command=lambda:self.search())
        self.button4.place(relx=0.5,rely=0.68)
        self.button5=Button(self,text='单词长度',font=("黑体",25),fg='blue',cursor='mouse',command=lambda:word.word_length_static(self.wordbase))
        self.button5.place(relx=0.15,rely=0.76)
        self.button6=Button(self,text='查询单词',font=("黑体",25),fg='blue',cursor='mouse',command=self.search_by_explainUI)
        self.button6.place(relx=0.5,rely=0.76)
        self.showindex=Label(self,text="单词指数", fg='blue',font=("黑体",20))
        self.showindex.place(relx=0.15,rely=0.85)
        self.show_time=Label(self,text="复习次数", fg='blue',font=("黑体",20))
        self.show_time.place(relx=0.55,rely=0.85)
        self.show_info=Label(self,text='Copyright © 2020-2020+ martinhyj.xyz All Rights Reserved.',font=("黑体",10),justify='center',width=50)
        self.show_info.place(relx=0,rely=0.97)

        #不能缩放
        self.resizable(False, False)
        self.geometry('350x700+600+100')

    # 展示单词信息
    '''
    单词显示后，可以消除标签
    单词居中显示
    '''
    def showword(self):
        print(self.testword[0])
        self.start_time=get_time_now()
        self.show_word.config(text=self.testword[0])
        self.show_word.pack()
        self.show_index_value.config(text=self.testword[2])
        self.show_index_value.place(relx=0.15,rely=0.9)
        self.show_times_value.config(text=self.testword[3])
        self.show_times_value.place(relx=0.55,rely=0.9)
        # 复习单词，后更新单词的信息

    #展示单词释义
    def showexplain(self):
        test_word=self.testword[1].replace(';','\n')
        if(len(test_word)!=0):
            test_word="释义:"+test_word
        # test_word='光标位于: %s,%s'%(str(event.x),str(event.y))
        self.show_explain.config(text=test_word)
        self.show_explain.place(relx=0.1,rely=0.35)
        print('展示释义')

    # 清空当前释义
    def clearexplain(self):
        self.show_explain.config(text='')
        # self.show_explain.place(relx=0.1,rely=0.4)

    #销毁部件对象
    def quitobject(self,mylabel):
        mylabel.destroy()

    #开始单词测试
    def start(self):
        # 在记下个单词之前，收集记忆上个单词的时间
        if len(self.testword)==4 and not self.button1_state:
            self.end_time=get_time_now()
            word.word_update(self.testword[0],self.end_time-self.start_time,self.wordbase)
            print(self.end_time-self.start_time)

        # 展示单词
        if not self.button1_state:
            if self.way==0:
                self.testword=word.getword_date(self.wordbase)
            elif self.way==1:
                self.testword=word.getword_Ebbinghaus(self.wordbase)
            elif self.way==2:
                self.testword=word.getword_index(self.wordbase)
            elif self.way==3:
                self.testword=word.getWord_Length(self.wordbase,self.length)
            self.showword()
            self.clearexplain()
            self.begain.set('查看释义')
            self.button1_state=True
        # 展示释义
        else:
            self.showexplain()
            self.begain.set('记忆单词')
            self.button1_state=False

    #构建添加单词的子窗口
    def add_ui(self):
        addUI=Toplevel(self)
        addUI.geometry("350x200+650+150")
        addUI.title("add word")
        addUI.resizable(False, False)

        # 布局
        tip_label=Label(addUI,text='请输入新加入词库的单词及其释义:',fg='blue',font=("黑体",15))
        tip_label.place(x=10,y=20)
        newword_label=Label(addUI,text="单词",fg="blue",font=("黑体",20))
        newword_label.place(x=10,y=50)
        newword=Entry(addUI)
        newword.place(x=70,y=50)
        newexplain_label=Label(addUI,text="释义",fg="blue",font=("黑体",20)).place(x=10,y=100)
        newexplain=Entry(addUI)
        newexplain.place(x=70,y=100)

        #按键触发
        savebutton=Button(addUI,text="保存",font=("黑体",25),fg='gray',cursor='mouse', command=lambda:self.save(newword.get(),newexplain.get()))
        savebutton.place(x=130,y=150)
        
        # 禁用button
        self.button2.config(state="disabled")
        addUI.transient(self)
        addUI.wait_visibility()
        addUI.wait_window()
        # 窗口消失后解禁
        self.button2.config(state="normal")
    
    def save(self,a_word,explain):
        '''
        保存输入的单词对象
        1:进行错误检测（是否存在非法符号，单词只能为英文，解释为中文）
        2:任意栏为空则禁止保存
        '''
        print(a_word,explain)
        # 判断词库中是否已经存在该单词
        # 如果没有找到，就add the word
        if not word.findword(a_word,self.wordbase):
            if self.jugde(a_word,explain):
                 new_word=word(a_word.lower(),explain)
                 new_word.storage(self.wordbase)
        # 如果找到，需要判断是否修改
        else:
            answer=tkinter.messagebox.askokcancel(title="提示",message="词库中已存在该单词，是否更新？")
            # 修改
            if answer:
                if self.jugde(a_word,explain):
                    word.redesign(a_word,explain,self.wordbase)
            # 不修改
            
    def jugde(self,stuff1,stuff2):
        '''
            单词和释义的规范判断
        '''
        if(isempty(stuff1) or isempty(stuff2)):
            tkinter.messagebox.showerror("错误",'输入不能为空')
            return False
        elif(isword(stuff1)):
            tkinter.messagebox.showerror('错误','单词或释义填写不规范')
            return False
        elif(isexplain(stuff2)):
            tkinter.messagebox.showerror('错误','单词或释义填写不规范')
            return False
        return True
    
    #查询单词，显示其历年考试的趋势
    def search(self):
       addUI=Toplevel(self)
       addUI.geometry("350x100+650+150")
       addUI.title("search word")
       addUI.resizable(False, False)
       #布局
       tip_label=Label(addUI,text='请输入你想查询的单词',fg='blue',font=("黑体",15))
       tip_label.pack()
       newword=Entry(addUI)
       newword.pack()

       #按键触发
       searchbutton=Button(addUI,text="查询",font=("黑体",25),fg='gray',cursor='mouse', command=lambda:TheWords.show_tendency(word=newword.get()))
       searchbutton.pack()

       # 禁用button
       self.button4.config(state="disabled")
       addUI.transient(self)
       addUI.wait_visibility()
       addUI.wait_window()
       # 窗口消失后解禁
       self.button4.config(state="normal")
    # 设置记忆单词的长度
    def set_length(self):
        if not self.set_length_ui:
            self.set_length_ui=Toplevel(self)
            self.set_length_ui.geometry("350x100+650+150")
            self.set_length_ui.title("set length")
            self.set_length_ui.resizable(False, False)
            #布局
            tip_label=Label(self.set_length_ui,text='请设置单词的长度(1-18)',fg='blue',font=("黑体",15))
            tip_label.pack()
            len_str=Spinbox(self.set_length_ui,from_=1,to=18,justify="center",command=lambda:self.setlen(int(len_str.get())))
            len_str.pack()

            self.set_length_ui.protocol(name="WM_DELETE_WINDOW", func=lambda:self.close_window(4))
        
    def setlen(self,len):
        self.length=len
        print("当前记忆单词长度为{}".format(len))

    # 播放当前单词的发音
    def play_Press(self,event,id):
        voice = youdao(type=id)
        path=voice.down(self.testword[0])
        # 检测是否连接网络
        if path:
            Word_voice.play(path)
        else:
            tkinter.messagebox.showwarning('警告','未连接网络！')


    def search_by_explainUI(self):
        '''
            展示查询结果
        '''
        addUI=Toplevel(self)
        addUI.geometry("350x100+650+150")
        addUI.title("search word")
        addUI.resizable(False, False)
        #布局
        tip_label=Label(addUI,text='请输入你想查询的单词的释义(用“，”分隔)',fg='blue',font=("黑体",15))
        tip_label.pack()
        Str=Entry(addUI)
        Str.pack()

        #wordlist
        wordlist=[]
        #按键触发
        searchbutton=Button(addUI,text="查询",font=("黑体",25),fg='gray',cursor='mouse', command=lambda:self.show_search_result(Str.get()))
        searchbutton.pack()

        # 禁用button
        self.button6.config(state="disabled")
        self.show_word.config(state="disabled")
        addUI.transient(self)
        addUI.wait_visibility()
        addUI.wait_window()
        # 窗口消失后解禁
        self.button6.config(state="normal")
        self.show_word.config(state="normal")
    
    def show_search_result(self,Str):
        if len(Str)==0:
            print("输入为空")
        else:
            results=word.search_by_explain(Str,self.wordbase)
            print(Str)
            print(results)
            text="查询结果:"

            if results:
                for result in results:
                    text=text+result[0]+", "
            self.show_word.config(text="")
            self.show_explain.config(text=text[0:-2])
            self.show_explain.place(relx=0.1,rely=0.35)
            print('展示查询结果')
    
    def set_wordbase(self,id):
        '''
        设置当前词库
        '''
        list=["考研","四级","六级","高考"]
        if id !=0:
           tkinter.messagebox.showwarning('提示','该功能正在路上') 
        else:
            self.wordbase=id
            print("当词库:{}".format(list[id]))

    def set_way(self,id):
        '''
            设置当前记忆方式
        '''
        list=["随机抽取","艾宾浩斯","单词指数","单词长度"]
        self.way=id
        if id==3:
            self.set_length()
        print("当前记忆方式:{}".format(list[id]))

    def show_detail(self,event):
        '''
        展示单词所有细节
        '''
        if not self.detail_ui:
            # 获取detail
            detail_text=get_detail(self.testword[0])
            # print(detail_text)
            # 检测是否查询到
            # rollbar
            if detail_text==None:
                tkinter.messagebox.showwarning("提示","对不起，未找到该单词")
            else:
                self.detail_ui=Toplevel(self)
                self.detail_ui.geometry("450x450+800+150")
                self.detail_ui.title("单词详情")
                self.detail_ui.resizable(False, False)
                self.detail_ui.transient(self)
                
                sb=Scrollbar(self.detail_ui)
                sb.pack(side='right',fill='y')
                
                detail_massage=Text(self.detail_ui,height=50,selectbackground="pink",yscrollcommand=sb.set,exportselection=True,pady=8,padx=6)
                
                #text_tag 
                detail_massage.tag_config("tag_word",foreground="black",font=tf.Font(family='微软雅黑',size=25))
                detail_massage.tag_config("tag_trans",spacing1=3,font=tf.Font(family="仿宋_GB2312",size=12))
                
                detail_massage.insert("insert",self.testword[0]+"\n","tag_word")
                detail_massage.insert("end",detail_text,"tag_trans")
            
                detail_massage.config(state="disabled",selectbackground='black')
                detail_massage.pack()
                
                sb.config(command=detail_massage.yview)

    def show_about(self):
        '''
            应用信息
        '''
        if not self.about_ui:
            self.about_ui=Toplevel(self,bg="#e7e7e7")
            self.about_ui.geometry("300x150+800+150")
            self.about_ui.resizable(False, False)
            
            text="关于\n\n这是一个集众多功能的强大的记单词工具\n版本2.1\nwww.marttinhyj.xyz保留一切权利。"
            info=Message(self.about_ui,width=200,bg="#e7e7e7",justify="center",text=text).pack()
            self.about_ui.protocol(name="WM_DELETE_WINDOW", func=lambda:self.close_window(1))
   
    def show_advice(self):
        '''
            展示邮箱
        '''
        if not self.advise_word_ui:
            self.advise_word_ui=Toplevel(self,bg="#e7e7e7")
            self.advise_word_ui.geometry("300x150+800+150")
            self.advise_word_ui.resizable(False, False)

            text="\n\n\n相关意见，请您及时发送到我们的工作邮箱\nmartinhyj1999@163.com"
            info=Message(self.advise_word_ui,width=200,bg="#e7e7e7",justify="center",text=text).pack()
            self.advise_word_ui.protocol(name="WM_DELETE_WINDOW", func=lambda:self.close_window(3))
        # tkinter.messagebox.showinfo("建议","相关意见，请您及时发送到我们的工作邮箱\nmartinhyj1999@163.com")

    def show_help(self):
        '''
            展示网址
        '''
        if not self.help_ui:
            self.help_ui=Toplevel(self,bg="#e7e7e7")
            self.help_ui.geometry("300x150+800+150")
            self.help_ui.resizable(False, False)
            
            text="\n\n\n相关问题请在www.martinhyj.xyz查阅相关文档"
            info=Message(self.help_ui,width=200,bg="#e7e7e7",justify="center",text=text).pack()
            self.help_ui.protocol(name="WM_DELETE_WINDOW", func=lambda:self.close_window(2))
        # tkinter.messagebox.showinfo("帮助","相关问题请在www.martinhyj.xyz查阅相关文档")

    def close_window(self,index):
        '''
            关闭窗口时设置其对象为None
        '''
        if index==0:
            self.detail_ui.destroy()
            self.detail_ui=None
        elif index==1:
            self.about_ui.destroy()
            self.about_ui=None
        elif index==2:
            self.help_ui.destroy()
            self.help_ui=None
        elif index==3:
            self.advise_word_ui.destroy()
            self.advise_word_ui=None
        elif index==4:
            self.set_length_ui.destroy()
            self.set_length_ui=None


#检测字符是否为空或为全空格
def isempty(str):
    if(len(str)==0 or str.isspace()==True):
        return 1
    return 0

#检测字符串是否为一个正确的单词格式
#是否只由英文字母组成
def isword(str):
    if str.isalpha():
        return 0
    return 1

#检测字符串中是否有非法符号
def isexplain(str):
    if not re.search(u'^[（）(),;、，；.a-zA-Z0-9\u4e00-\u9fa5]+$', str):
        return 1
    return 0

def get_time_now():
    # 获取当前时间
    '''
    Return the current time in seconds since the Epoch. 
    Fractions of a second may be present if the system clock provides them.
    '''
    return time.time()

    
if __name__ == "__main__":
    # print(get_time_now())
    print(help(tkinter))
