'''
Author: martin
Date: 2020-10-06 20:01:21
LastEditTime: 2021-01-04 18:30:30
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /py/practice/main.py
'''
#-*- coding:utf-8 -*-
'''
That ambition to sky is in head at childhood, and promised to be the royal man of the world
'''

from UI_words import *

def main():
    # 打开app
    # 1:review word
    # 2:add new word
    # 3:show the tendency for past tenyears of the word
    # 4:show the tendency for past tenyears of the word by inputed

    mywin=window(screenName="word",className=" ")
    mywin.mainloop()

if __name__ == "__main__":
    # 运行程序
    main()