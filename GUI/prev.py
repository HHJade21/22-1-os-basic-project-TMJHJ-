#위젯스킨
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap import utility
from tkinter import messagebox
#현재 3.14.1 selenium 버전 사용중
from selenium import webdriver
#webdriverwait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#멀티쓰레딩
from threading import Thread
#BeautifulSoup
from time import sleep
import requests
from bs4 import BeautifulSoup as bs
#창 설정
root = ttk.Window(
    title = "Python Project",
    themename = "litera",
    size = (730,500), # window size
    position = (100,100), # window position
    minsize = (0,0), # minimum width and height of the window
    maxsize = (1920,1080), # maximum width and height of window
    resizable = (True,False) # sets whether the window can be resized
)

#idtext,pwtext 텍스트 박스
idtext_content=ttk.StringVar()
pwtext_content=ttk.StringVar()
idtext = ttk.Entry(root,show=None,width=24,textvariable=idtext_content).grid(row=1, column=1, sticky=ttk.W,padx = 20,pady = 5)
pwtext = ttk.Entry(root,show="*",width=24,textvariable=pwtext_content).grid(row=2, column=1, sticky=ttk.W,padx = 20,pady = 5)

#로그인버튼 클릭시 gui 멈춤 현상 방지를 위한 멀티스레드
def th():
    th = Thread(target=Button_Click)
    th.daemon = True
    th.start()
#로그인
def Login() :
    user_id = idtext_content.get()
    sleep(0.5)
    driver.find_element_by_name('uid').send_keys(user_id)
    user_pw = pwtext_content.get()
    sleep(0.5)
    driver.find_element_by_name('pswd').send_keys(user_pw)
    driver.find_element_by_xpath('//*[@id="entry-login"]').click()
    
#사용자 이름 불러오기
def Find_Name():
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="base_tools"]/bb-base-navigation-button[3]/div/li/a')))
    sleep(0.5)
    driver.find_element_by_xpath('//*[@id="base_tools"]/bb-base-navigation-button[3]/div/li/a')
    html = driver.page_source
    soup = bs(html,'html.parser')
    myname = soup.text[(soup.text.find("."))+1:soup.text.find(".")+4]
    return myname
            
# 로그인 버튼 클릭시 이벤트
def Button_Click():
    ttk.Label(root, text = "          로그인중...",font = ("나눔고딕", 10)).grid(row=1,column=3,rowspan=2,padx=5,ipady=25,ipadx=50)
    try:
        Login()
        ttk.Label(root, text = "               "+Find_Name()+"님 환영합니다.",font = ("나눔고딕", 10)).grid(row=1,column=3,rowspan=2,padx=5,ipady=25,ipadx=40)
        driver.get('https://ecampus.chungbuk.ac.kr/ultra/stream')
        messagebox.showinfo('로그인','로그인 성공')
    except:
        messagebox.showerror('로그인', '로그인 실패')
        ttk.Label(root, text = "               게스트님 환영합니다.",font = ("나눔고딕", 10)).grid(row=1,column=3,rowspan=2,padx=5,ipady=25,ipadx=40)
        pass 
#로그인 버튼
a =ttk.Button(root,text="LOGIN", bootstyle=(PRIMARY, "outline-toolbutton"),command=th).grid(row=1, column=2,rowspan=2,sticky=ttk.W,ipady = 25,ipadx=40)
#로그인 버튼 우측 라벨
ttk.Label(root, text = "               게스트님 환영합니다.",font = ("나눔고딕", 10)).grid(row=1,column=3,rowspan=2,padx=5,ipady=25,ipadx=40)
#탭
f = ttk.Frame(root)
f.grid(row=3,column=1,columnspan = 3 ,pady=10,ipadx =0)
nb = ttk.Notebook(f)
nb.pack(
    side=LEFT,
    padx=(10, 0),
    expand=YES,
    fill=BOTH
)
#탭1(메인)
nb.add(ttk.Label(nb, text="This is a notebook tab.\nYou can put any widget you want here."), text="    MAIN    ", sticky=NW)
#탭2(공지)
nb.add(child=ttk.Label(nb, text="notebook tab 2."),text="  공지사항  ",sticky=NW)
#탭3(과제)
f2 = ttk.Frame(nb)
tv2 = ttk.Treeview(
        master=f2,
        columns=[0, 1,2],
        show=HEADINGS,
        height=15
    )
table_data = [
    (1,'one' , 'a'),
    (2, 'two','b'),
    (3, 'three','c'),
    (4, 'four','d'),
    (5, 'five','e')
]
for row in table_data:
    tv2.insert('', END, values=row)
# print(tv.get_children())#('I001', 'I002', 'I003', 'I004', 'I005')
tv2.selection_set('I002')
tv2.heading(0, text='과목명')
tv2.heading(1, text='과제')
tv2.heading(2, text='마감기한')
tv2.column(0, width=100)
tv2.column(1, width=350, anchor=CENTER)
tv2.column(2, width=200)
tv2.pack(side=LEFT, anchor=NE, fill=X,padx = 20,pady = 10)
nb.add(f2, text='    과제    ',sticky =NW)
#탭4(성적)
f3 = ttk.Frame(nb)
tv = ttk.Treeview(
        master=f3,
        columns=[0, 1],
        show=HEADINGS,
        height=15
    )
table_data = [
    (1,'one'),
    (2, 'two'),
    (3, 'three'),
    (4, 'four'),
    (5, 'five')
]
for row in table_data:
    tv.insert('', END, values=row)
# print(tv.get_children())#('I001', 'I002', 'I003', 'I004', 'I005')
tv.selection_set('I002')
tv.heading(0, text='과목명')
tv.heading(1, text='성적')
tv.column(0, width=100)
tv.column(1, width=550, anchor=CENTER)
tv.pack(side=LEFT, anchor=NE, fill=X,padx = 20,pady = 10)
nb.add(f3,text = "     성적     ",sticky=NW)
# 창 숨기는 옵션 추가
options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome('C:\Chrome_Driver\chromedriver.exe',options=options)

#크롬으로 블랙보드 로그인 화면 접속
url = "https://ecampus.chungbuk.ac.kr/"
driver.get(url)




root.mainloop()
