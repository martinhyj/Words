![Words](https://socialify.git.ci/martinhyj/Words/image?description=1&descriptionEditable=%E8%AE%B0%E5%8D%95%E8%AF%8D%E6%A1%8C%E9%9D%A2%E5%BA%94%E7%94%A8&font=Inter&forks=1&issues=1&language=1&owner=1&pattern=Plus&pulls=1&stargazers=1&theme=Light)
### word in my way

---

#### word in my way
* 用我自己的方式，记单词！！
* 结合书籍与与编程语言python，进行科学高效的记单词



#### 开发工具

	python3.x以及相关第三方库(sqlite3,tkinter，pandas,matplotlib)
	sqlite(sqlite manager)



#### 开发日志

* 2020-10-1:项目开始
* 2020-10-15:

​		项目UI以及程序主体基本实现

​																				UI: 界面一,主界面

<img src="https://tva1.sinaimg.cn/large/007S8ZIlly1gjw2upd6tkj309u0k5t9m.jpg" style="zoom:30%;" />

​															界面二：输入单词界面（为界面一的子窗口）

<img src="https://tva1.sinaimg.cn/large/007S8ZIlly1gjw2v0f3o9j309v06gaag.jpg" style="zoom:30%;" />

​		功能包含：用户能手动输入单词，储存到自己的单词库（表列包括：单词名，单词释义，单词指数，复习次数）

​							用户可以随机的从自己的单词库中抽取单词，复习（抽取单词标准默认为抽取单词指数小于4的单词）

* 2020-10-20:

  ​		增添单词对象列：添加日期（单词的添加日期，xxxx-xx-xx）
  
* 2020-10-21:

​		增添查询某单词是否已存在数据库（用户词库）中的函数findword(),以解决在储存单词时用户不清楚该单词，是否已在词库中的问题；*但使用该操作，将会在储存单词时两次请求连接数据库，开销增大，所以在存储单词函数storage()中添加检测部分。*

* 2020-10-28:

​		增添功能一：查看词库中单词在历年考试中出现的频率（tendency）,可通过折线图，直观的观察该单词在考试中出现的次数。

<img src="https://tva1.sinaimg.cn/large/0081Kckwly1gk59yn2251j309w0k3jsp.jpg" style="zoom:30%;" />

<img src="https://tva1.sinaimg.cn/large/0081Kckwly1gk59zpsrngj30gs0czq3h.jpg" style="zoom:30%;" />

​		增添功能二：支持手动输入任意单词查看其在历年考试中出现的频率（tendency）



<img src="https://tva1.sinaimg.cn/large/0081Kckwly1gk5a16lg72j30ce0k3gnp.jpg" style="zoom:30%;" />

* 2020-11-3:
  1.调整了单词趋势图的大小(之前两个趋势图有重合部分)
  2.单词熟练指数开始使用，定义标准为用户在记忆该单词时所用的时间，程序经过计算为该单词计算出一个合适熟练指数
  3.新添”艾宾浩斯遗忘曲线（Ebbinghaus）“的方法，来高效，科学的复习单词
  
* 2020-11-17:
	改进了在添加已有单词时，用户会接收到提示，其可以选择，取消操作和更新操作（但需要多调用数据库一次）
	
* 2020-11-26

  1:增添了对当前词库中单词长度进行统计的功能，可以加深用户对单词长度的认知

  <img src="https://tva1.sinaimg.cn/large/0081Kckwly1gl2mhz8c3uj30lc0k47g0.jpg" style="zoom:30%;" />

  2:增加了单词发音功能，单击单词就能得到该单词的美式发音(可修改为英式发音)；单词音频使用了有道词典的[接口](http://dict.youdao.com/dictvoice?type=0&audio=）,python媒体库（播放音频),使用了第三方库pygame;也可以使用第三方库playsound,其跨平台，使用更简单，但暂时使用不了
  
* 2020-12-9

  增添了根据汉语意思查询相关英语单词的功能，汉语意思的输入需要有相应的格式，然后通过Jaccard距离，来得到词库中与该意思相接近的单词，然后显示
  
* 2020-12-13
  
  更新：将考研单词：英语一，英语二的趋势图合并到了一个图中
  
  <img src="https://tva1.sinaimg.cn/large/0081Kckwly1gmcsn8ygy4j30go0bv3z7.jpg" style="zoom:30%;" />
  
* 2020-12-15

  找到了显示菜单的方法，增加了选择词库，选择记忆方式，以及编辑，帮助的功能，可能根据自己的需要进行设置。目前仅有考研一个词库，记忆方式有按index，随机，艾宾浩斯遗忘曲线三种记忆方式。

* 2020-12-16

  增添了，右键单击单词，播放该单词的英式发音
  
* 2020 12-31 

  完善和更新了各记忆方法
  完成mysql到sqlite的移植，不再依赖mysql
  
* 2020 1-2
  
  增加根据设置单词长度的方式来记忆单词的功能
  
  
  
* 2021 1-3
  增加查看详细信息的功能：记忆单词时，在菜单栏：查看菜单中，选择查看该单词详细信息查看
  
  <img src="https://tva1.sinaimg.cn/large/0081Kckwly1gmcsf2a9jrj30cj0d6t9p.jpg" style="zoom:30%;" />
  
* 2021 1-4
  1:发音方式改变：点击发音喇叭播放单词发音，左键：英音，右键：美音

  <img src="https://tva1.sinaimg.cn/large/0081Kckwly1gmcsiggrxaj309p0k2gmt.jpg" style="zoom:25%;" />
  
* 2021 1-21
  
  加入了大学四六级词库
  
  
  
  
  
#### 问题
* 查看单词在历年考试中的趋势图的功能中，由于单词在文章中可能会出现改变形态的原因，但词库中的单词都是一般形态，所以不能够更加准确的匹配与搜索。 2020-1-1 已解决。
* 在使用根据汉语意思查询单词的功能时，显示单词标签的内容会变为空，但是显示单词的标签仍有焦点，若之前使用了记忆单词的功能，那么点击显示单词的标签时，会播放上次显示单词的发音。2020 1-4 已解决
* 在Windows上运行，界面布局可能会有所不适应。



#### 参考
* *Python程序设计基础（第二版） 李东方，文欣秀 张向东 电子工业出版社*
* *Python语言程序设计基础（第二版） 嵩天 礼欣 黄天羽 高等教育出版社*

* [菜鸟教程](https://www.runoob.com)

