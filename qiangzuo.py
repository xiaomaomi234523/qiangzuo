# 打开这个网站http://seat.lib.dlut.edu.cn/yanxiujian/client/index.php#
# 点击座位预约
# 点击OK
# 输入账号
# 输入密码
# 点击登录
# 点击座位预约
# 点击下一天
# 点击图书馆
# 点击房间号
# 点击手动选择
# 点击座位号
# 点击确定

import time
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
import streamlit as st
import os,inspect
from PIL import Image


# 获取绝对地址（不知道为什么用不了相对地址）
current_path = inspect.getfile(inspect.currentframe())
dir_name = os.path.dirname(current_path)
file_abs_path = os.path.abspath(dir_name)

st.title("图书馆抢座")
#image = Image.open(file_abs_path+r'\pic.png')
#st.image(image)

# 预先启动时间
tq = "08:45:40"
# 抢座时间
time_list = ["08:46:01","08:47:01"]
# 首选 令希图书馆 401 243
# 次选 令希图书馆 401 186
# 次次选 伯川图书馆 301 116


    # [library, room, seat] = list(input("首选:").split())
    # [library1, room1, seat1] = list(input("次选:").split())
    # [library2, room2, seat2] = list(input("次次选:").split())
[library, room, seat] = ["令希图书馆", "401", "243"]
[library1, room1, seat1] = ["令希图书馆", "401", "186"]
[library2, room2, seat2] = ["伯川图书馆", "301", "116"]
    # print("输入值不合法，采用默认")
    # print("首选:令希图书馆 401 243")
    # print("次选:令希图书馆 401 186")
    # print("次次选:令希图书馆 301 116")
# print()
# print("将于",time_list[0],"开始抢座")
# print()

def qiangzuo1(library,room):
    s = Service(executable_path=file_abs_path+r'\geckodriver(1).exe')
    dr = webdriver.Firefox(service=s)
    dr.get('http://seat.lib.dlut.edu.cn/yanxiujian/client/index.php#')
    #dr.maximize_window()

    #座位预约
    location= dr.find_element(By.LINK_TEXT,"座位预约")
    location.click()
    sleep(0.4)
    #ok
    location = dr.find_element(By.XPATH,"/html/body/div[3]/div/div/div[3]/button[2]")
    location.click()
    sleep(0.4)
    #账号
    location = dr.find_element(By.XPATH,"//*[@id='un']")
    location.send_keys('201964080')
    #密码
    location = dr.find_element(By.XPATH,'//*[@id="pd"]')
    location.send_keys('lbdzjszqx7018589')
    #登录
    location = dr.find_element(By.XPATH,'/html/body/form[1]/div[2]/div/div[2]/div[2]/div[1]/span/input')
    location.click()
    #座位预约
    location= dr.find_element(By.LINK_TEXT,"座位预约")
    location.click()
    sleep(0.4)
    #点击下一天
    location= dr.find_element(By.XPATH,'//*[@id="nextDayBtn"]')
    location.click()
    sleep(0.4)
    #选择图书馆
    location = dr.find_element(By.XPATH,'//h4[text()={}]'.format("\""+' '+library+"\""))
    location.click()
    sleep(0.4)
    # 选择房间号
    location = dr.find_element(By.XPATH,'//h4[text()={}]'.format("\""+' '+library+room+'阅览室'+"\""))
    location.click()
    sleep(0.4)
    return dr

def qiangzuo2(seat,dr):
    #手动选择
    location = dr.find_element(By.XPATH,'//html/body/div[4]/div/div/div[3]/button[2]')
    location.click()
    sleep(0.19)
    #座位
    location = dr.find_element(By.XPATH,'//i[text()='+seat+']')
    location.click()
    sleep(0.19)
    #确认
    location = dr.find_element(By.XPATH,'//*[@id="btn_submit_addorder"]')
    location.click()

flag = 1
while flag: # 提前20s到达选座方式页面等候开放
    time_now = time.strftime("%H:%M:%S",time.localtime())
    if time_now == tq:
        dr=qiangzuo1(library=library,room=room)
        flag = 0
flag = 1
while True: # 到开放时间就开始选座，两个备选
    time_now = time.strftime("%H:%M:%S", time.localtime()) # 刷新
    if time_now in time_list and flag: #此处设置每天定时的时间
        flag=0
        start=time.time()
        try:
            if time_now != time_list[0]:
                dr = qiangzuo1(library=library,room=room)
            qiangzuo2(seat=seat,dr=dr)
            print("--------------------------------------------")
            print("于",time.strftime("%H:%M:%S", time.localtime()),"抢到了首选",library,room,seat)
        except Exception :
            try:
                dr=qiangzuo1(library=library1, room=room1)
                qiangzuo2(seat=seat1,dr=dr)
                print("--------------------------------------------")
                print("于",time.strftime("%H:%M:%S", time.localtime()),"抢到了次选",library1,room1,seat1)
            except Exception :
                try:
                    dr=qiangzuo1(library=library2, room=room2)
                    qiangzuo2(seat=seat2, dr=dr)
                    print("--------------------------------------------")
                    print("于",time.strftime("%H:%M:%S", time.localtime()),"抢到了次次选",library2,room2,seat2)
                except Exception :
                    print("--------------------------------------------")
                    print("啥也没抢着")
                    flag = 1
        finally:
            end = time.time()
            print("用时",end-start,"秒")
            print("--------------------------------------------")
            print()
            if not flag:
                print('冲冲冲冲冲冲冲')

