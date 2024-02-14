from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
import sqlite3 as sl
import datetime
import requests
import json
import os
from bs4 import BeautifulSoup
import feedparser


executor = ThreadPoolExecutor(20)
app = FastAPI()
headers = {"content-type":"application/json"}
scheduler = BackgroundScheduler(executors={'default': executor},max_instances=20)


class MSG(BaseModel):
    id:int
    ts:int
    sign:str
    type:int
    xml:str
    sender:str
    roomid:str
    content: str
    thumb: str
    extra: str
    is_at: bool
    is_self: bool
    is_group: bool

def kickout():
    wxids=kickoutnotice(say="以上同学因为本月未发言被移除出群，想再次进群可以练习钘哥说明情况，希望在我看不见的地方，你也在努力哦，让我们江湖再见！")
    jspayload = {"roomid": "34629253960@chatroom", "wxids": wxids}
    url1 = "http://127.0.0.1:9999/chatroom-member"
    requests.delete(url=url1, json=jspayload)

def kickoutnotice(say):
    conn1 = sl.connect('menbers.db')
    cursor1 = conn1.cursor()
    url1 = "http://127.0.0.1:9999/chatroom-member?roomid=34629253960%40chatroom"
    res = requests.get(url=url1)
    res = json.loads(res.text)
    res = res.get("data")
    res = res.get("members")
    wxids=''
    word=''
    for wid,name1 in res.items():
        print(wid)
        sql="select last_time from POST where wxid='%s'" % (wid)
        cursor1.execute(sql)
        data = cursor1.fetchall()
        print(data)
        if(len(data)==0):
            word=word+"@"+name1+"\u2005"
            wxids = wxids + wid+","
            continue
        data =data[0]
        data = str(data)
        data = data.split(" ")
        data = data[0]
        data = data.split("-")
        month=int(data[1])
        nowmonth=datetime.datetime.now().strftime('%m')
        nowmonth=int(nowmonth)
        if(nowmonth!=month):
            word=word+"@" +name1+"\u2005"
            wxids=wxids+wid+","
    wxids=wxids[:-1]
    print(wxids)
    conn1.commit()
    conn1.close()
    url1="http://127.0.0.1:9999/text"
    word=word+say
    jspayload = {"msg": word, "receiver": "34629253960@chatroom","aters":wxids}
    headers = {"content-type": "application/json"}
    requests.post(url1, json=jspayload, headers=headers)
    return wxids

def getrss(strings,url):
    d=feedparser.parse(url)
    strings=strings+d.entries[0].title+"\n"
    strings=strings+"链接："+d.entries[0].link+"\n"
    strings = strings +"来源："+ d.feed.title + "\n"
    return strings

def roomdailynews():
    newurl="https://www.ddosi.org/category/%E6%B8%97%E9%80%8F%E6%B5%8B%E8%AF%95/"
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    }
    response = requests.get(url=newurl, headers=header)
    response.raise_for_status()
    response = response.content.decode('utf-8')
    response = BeautifulSoup(response, 'lxml')
    response = response.find_all(attrs={"class": "entry-title"})
    newlink = response[0].a.attrs['href']
    newtitle= response[0].text
    todaytime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S %A')
    news=""
    count=1
    rssfile=open("rss.txt")
    rsslist=rssfile.readlines()
    for line in rsslist:
        if(count==1):
            news=news+"早上好！现在是"+todaytime+"\n\n每日快讯:\n"
        if(count==3):
            news=news+"\n威胁情报：\n"
        if(count==7):
            news=news+"\n漏洞报告：\n"
        if(count==9):
            news=news+"\n最新CVE报告：\nhttps://cassandra.cerias.purdue.edu/CVE_changes/today.html\n部分链接需梯子"+"\n\n安全文章：\n"+newtitle+"\n"+newlink+"\n来源：https://www.ddosi.org/category/%E6%B8%97%E9%80%8F%E6%B5%8B%E8%AF%95/\n"
        news=getrss(news,line)
        count=count+1
    news=news+"以上就是今早的新内容，一起来学习呀！"
    url1 = 'http://127.0.0.1:9999/text'
    jspayload = {"msg":news,"receiver":"34629253960@chatroom"}
    requests.post(url1,json=jspayload,headers=headers)

def wxautocheck():
    url1 = "http://127.0.0.1:9999/text"
    jspayload = {"msg": "I'm still alive!(auto send)", "receiver": "wxid_m8k6ethe81ib32"}
    requests.post(url1, json=jspayload, headers=headers)


@app.on_event("startup")
async def app_start():
    scheduler.add_job(kickout, 'cron', month='*',day='last')
    scheduler.add_job(roomdailynews, 'cron', hour=7)
    scheduler.add_job(wxautocheck, 'cron', hour='*')
    scheduler.add_job(kickoutnotice(say="以上群成员本月内还未发言，请注意哦！"), 'cron', month='*',day=25)
    scheduler.start()

@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()

@app.get("/check")
async def check():
    a="success!"
    url1 = "http://127.0.0.1:9999/text"
    jspayload = {"msg": "I'm still alive!(controled by api)", "receiver": "wxid_m8k6ethe81ib32"}
    requests.post(url1, json=jspayload, headers=headers)
    return a

@app.post("/receive_msg")
async def recv_msg(msg:MSG):
    print(msg)
    words = "真闲！不过如果你真的无聊的话，可以试试sql注入我，帮助主人找漏洞哦！先在此谢过了！"
    url="http://127.0.0.1:9999/alias-in-chatroom?wxid="+msg.sender+"&roomid="+msg.roomid
    res=requests.get(url)
    res=json.loads(res.text)
    res=res.get("data")
    name=res.get("alias")
    time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(name)
    print(msg.sender)
    conn = sl.connect('menbers.db')
    cursor = conn.cursor()
    if(msg.sender=="" and msg.content.find("加入了群聊")!=-1):
        words="欢迎新成员加入HackTB实验室的大家庭，不如先自我介绍一下吧！以下是本实验室守则，请仔细阅读哦！\n\n实验室规章制度：\n0 在校的同学进群后请自觉介绍自己\n1 养成提出高质量问题的习惯，还有乐于和高质量回应群友提问的习惯\n2 多共享有价值的视频，技术或工具\n3 本群主要方向是SRC和渗透，其他技术也欢迎\n4 要经常分享学习到的知识当巩固练习\n5 保持活跃度，回答or提问 长时间不出现或者敷衍了事就移出\n钘哥的主页:dgut.uk\n\n实验室的其他资源请阅读群公告，希望以后我们能一起成长共同进步哦！\n\n@我输入help可以呼出我的帮助菜单"
        url = "http://127.0.0.1:9999/text"
        jsonpayload = {"msg": words, "receiver": msg.roomid}
        headers = {"content-type": "application/json"}
        requests.post(url, json=jsonpayload, headers=headers)
    if(msg.is_at==False and msg.sender!=""):
        sql="delete from POST where wxid='%s'" % (msg.sender)
        cursor.execute(sql)
        sql = "insert into POST(wxid,roomname,last_time) values('%s','%s','%s')" % (msg.sender,name,time)
        cursor.execute(sql)
    elif(msg.is_at==True):
        cmd = msg.content.split("\u2005")
        if (len(cmd) > 1):
            cmd = cmd[1]
            cmd = cmd.split(" ", maxsplit=1)
            if(len(cmd)>1):
                args=cmd[1]
                args = args.split(",")
            cmd=cmd[0]
        if(cmd=="check"):
            words="I'm still alive!"
        if(cmd=="help"):
            words="我是Scr1ptKidB0t，我会默默记下大家的最后发言时间\n@我发消息可以触发指令，大家@我的时候要我回复了才能继续@哦：\n\nhelp 显示本帮助文档\nlast 显示本人最后发言时间\nsearch 路人甲,路人乙 输出一个或多个成员的最后发言时间的最后发言时间，要搜索的每个成员之间用英文逗号隔开\nall 输出一个文件，里面是所有人的最后发言时间\ncheck 检查机器人存活状态\nfeedback 反馈内容 发送反馈\n\n项目地址：https://github.com/hustler0000/AWindowsSimpleWxbot\n\n注意！在群里要积极发言哦！每个月25号会在群内通知这个月还没有发言过的同学，每个月最后一天清除群内未发言同学，希望大家珍惜在群里的机会呀！\n\n希望大家珍惜我，不要@我刷屏，不要连续@我，玩坏了掉线了及时告知我的主人，希望能和大家一起进步呀"
        if(cmd=="last"):
            sql="select last_time from POST where wxid='%s'" % (msg.sender)
            cursor.execute(sql)
            data = cursor.fetchall()
            data = str(data)
            data = data.split(",")
            data=data[0]
            dtime=data[3:-1]
            words="你好"+name+"\n你最后的发言时间是："+dtime+"\n记得要多发言，营造活跃的群内气氛哦！"
        if(cmd=="search"):
            words = "你好" + name+"，以下成员的最后发言时间是："
            for arg in args:
                sql="select last_time from POST where roomname='%s'" % (arg)
                cursor.execute(sql)
                data = cursor.fetchall()
                data = str(data)
                data = data.split(",")
                data=data[0]
                dtime=data[3:-1]
                words=words+"\n\n成员："+arg+"\n"+"最后发言时间："+dtime
        if(cmd=="all"):
            os.system("del all_menbers.txt")
            sql = "select roomname,last_time from POST"
            cursor.execute(sql)
            data = cursor.fetchall()
            with open("all_menbers.txt", "a") as f:
                for item in data:
                    item = str(item)
                    item = item.split(",")
                    roomname = item[0]
                    roomname = roomname[2:-1]
                    time = item[1]
                    time = time[2:-2]
                    f.write(roomname + " " + time + "\n")
                f.close()
            url="http://127.0.0.1:9999/file"
            jsonpayload = {"path": "all_menbers.txt", "receiver": msg.roomid}
            requests.post(url, json=jsonpayload, headers=headers)
            words="以上是大家的发言时间记录，请大家踊跃发言，一起成长呀"
        if(cmd=="feedback"):
            words="实验室的"+name+"发送了反馈，内容为"+args+"，请迅速处理!"
            url = "http://127.0.0.1:9999/text"
            jsonpayload = {"msg": words, "receiver": "wxid_m8k6ethe81ib32"}
            headers = {"content-type": "application/json"}
            requests.post(url, json=jsonpayload, headers=headers)
            words=name+"，你的反馈已收到，感谢你的支持！"
        url = "http://127.0.0.1:9999/text"
        jsonpayload = {"msg": "@"+name+"\u2005"+words, "receiver": msg.roomid,"aters":msg.sender}
        headers = {"content-type": "application/json"}
        requests.post(url, json=jsonpayload, headers=headers)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)