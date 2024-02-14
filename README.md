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
# 初始化
在使用机器人之前，我们需要有一个微信账号来运行机器人，建议使用小号或者直接新注册一个微信账号，建议这个机器人账号添加常用微信号为好友，方便机器人通知反馈。运行机器人的账号必须实名，否则无法登录，也无法使用微信机器人，这是腾讯的限制，与项目无关
## 修改主程序
```
将项目克隆到服务器后，用vim或nano等文本编辑器打开WinSimplewxbot.py进行修改：
在程序第64行处，将YourWXname修改为你的微信用户名
在程序第72行处，可以调整自动任务的执行时间，比如seconds=1，minutes=1，hours=1，day=1等
找到程序第159行左右，即"all"功能处，将群名修改为你要部署的群的群名称，将路径改为你存放all_menbers.txt的相应绝对路径
找到程序第176行左右，即"feedback"功能处，将微信名称改为你的微信名称
```
