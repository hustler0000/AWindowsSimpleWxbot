# 鸣谢
感谢xiaozhao在测试过程的大力协助，这里是他的博客：https://aaaaaaamua.github.io/
# WindowsSimpleWxbot
```
基于https://github.com/lich0821/WeChatFerry
一个可以记录和查询群员最后发言时间，自动提醒和移除未发言群员的简单微信机器人
```
# 安装
首先安装python以及一些必要组件：
```shell
sudo apt-get update
sudo apt-get install python-is-python3 python-pip git
```
pip安装需要的库：
```shell
python -m pip install fastapi uvicorn python-multipart apscheduler pydantic wcfhttp wcferry -i https://pypi.tuna.tsinghua.edu.cn/simple
feedparser，bs4和requests库可装可不装，项目中是为了实现定时推送
```
克隆库
```shell
git clone https://github.com/hustler0000/AWindowsSimpleWxbot
```
机器人还需要特定版本的PC微信，请到release处下载安装
# 初始化
在使用机器人之前，我们需要有一个微信账号来运行机器人，建议使用小号或者直接新注册一个微信账号，建议这个机器人账号添加常用微信号为好友，方便机器人通知反馈。运行机器人的账号必须实名，否则无法登录，也无法使用微信机器人，这是腾讯的限制，与项目无关
## 修改主程序
```
先打开cmd，键入wcfhttp，登录机器人微信账号，然后访问http://127.0.0.1:9999/docs 稍等片刻会出现示例页面，此时测试/contacts接口，会返回通信录所有的wxid，找到你主号的要部署的微信群的wxid
将项目克隆到服务器后，用vim或nano等文本编辑器打开WinSimplewxbot.py进行修改：
在程序第36和42行附近的踢人和踢人通知功能处，将所有的YourWXID和YourRoomID修改为相应的用户ID和群ID
在程序第137行附近，可以调整自动任务的执行时间，比如seconds=1，minutes=1，hours=1，day=1等
找到程序第232行附近，即"feedback"功能处，将所有的YourWXID和YourRoomID修改为相应的用户ID和群ID
```
# 主程序
该机器人适用于Windows服务器环境，linux服务器请看https://github.com/hustler0000/AWindowsSimpleWxbot
## 启动
使用命令
```cmd
wcfhttp --cb http://127.0.0.1:8080/receive_msg
python WinSimplewxbot.py
```
## 帮助/功能菜单
```
机器人会默默记下群成员的最后发言时间，@机器人发消息可以触发指令

常规指令：
help 显示本帮助文档
last 显示本人最后发言时间
search 路人甲,路人乙 输出一个或多个成员的最后发言时间的最后发言时间，要搜索的每个成员之间用英文逗号隔开
all 输出一个文件，里面是所有人的最后发言时间
check 检查机器人存活状态
feedback 反馈内容 发送反馈

注意！在群里要积极发言哦！每个月25号会在群内通知这个月还没有发言过的同学，每个月最后一天清除群内未发言同学，希望大家珍惜在群里的机会呀！

当有群成员使用发送反馈时，机器人会向你的主微信账号发送反馈内容，当有新群员加入并发言时，机器人会自动记录，如果新人一个月没有发言也将被移出
为了方便地手动操作数据库，还有一个sqlop.py文件，这个python程序提供了简单管理sqlite数据库的条件，运行该程序，并输入相应数据库语句来对你的数据库进行操作。
用get请求访问服务器8080端口下的/check 路径可以检查机器人是否掉线
```
# 原理
十分简单，因为是二次开发，就是利用wcfhttp的api收发微信信息，收到的信息通过api转发到python跑的api服务中并且处理
# 存在问题
```
1.程序可能存在sql注入漏洞，可能会导致机器人功能异常
2.微信定时掉线，似乎无解
3.因为wcfhttp的api的局限，有时会出现信息阻塞导致机器人不会工作的问题，可以自己写一个python版本的机器人而不是用wcfhttp来解决这个问题
4.微信有版本限制，可能会遇到微信更新的问题
```
