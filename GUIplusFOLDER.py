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
import threading
#BeautifulSoup
from time import sleep
import requests
from bs4 import BeautifulSoup as bs
import datetime
#날짜
dt = datetime.datetime(2022, 1, 1)
#데이터베이스, 폴더
import time
import sqlite3
import shutil
import os


category_index=0 #속성값 추출할 때 사용할 category의 index

cours,title=[],[] #코스이름, 타이틀내용
category=[] #카테고리
my_score,max_score,score=[],[],[] #내성적, 만점성적, 내성적/만점성적
deadline=[] #마감기한
sub_name,sub_day,sub_start,sub_end=[],[],[],[]#과목이름,과목요일,과목시작일자,종료일자
key1,key2,key3 = [],[],[] #키워드1,2,3

#GUI카테고리 - 공지사항, 성적, 강의자료, 추가된 과제, 마감예정과제 (각각 코스와 타이틀 내용 따로 담음)
Notice_cours, Score_cours, Document_cours, Ass_cours, DeadlineAss_cours=[],[],[],[],[]
Notice_title, Score_title, Document_title, Ass_title, DeadlineAss_title=[],[],[],[],[]



#경로변수들
BFR = os.path.expanduser('~') #바탕화면 경로 자동 지정 변수. Basic Folder Root
DesktopRoot = os.path.join(BFR, 'Desktop') #바탕화면 경로 문자열
DownloadsRoot = os.path.join(BFR, 'Downloads')  #다운로드 폴더 경로 문자열
KDRoot = os.path.join(os.path.join(BFR, 'Documents'), '카카오톡 받은 파일')
folderroot = [] #검색함수에서 사용할 폴더 경로 리스트

##홍은성 추가 함수
#DB저장 로컬 디렉토리 생성. 메인 루프에서 if로 존재여부 검사해도 되겠지만 시간관계상 얘랑 테이블생성함수는 걍 넣어서 쓸 것
def MakingLocDir() :
    if not os.path.exists("C:\\StudyHelper") : #프로그램 로컬 디렉토리 생성
        os.mkdir("C:\\StudyHelper")

#블랙보드 로그인 정보 존재 여부 확인. 있으면 1, 없으면 0 반환
def BBInfoExist() :
    table_name = 'BBID'
    sql = f'SELECT * FROM sqlite_master WHERE type = "table" AND name = "{table_name}"'
    cur.execute(sql)
    rows = cur.fetchall()
    if rows :
        return 1
    else :
        return 0

#데이터베이스 생성
def MakingTable() :

    #사용자 정보 테이블과 과목정보 테이블을 각각 생성
    cur.execute("CREATE TABLE IF NOT EXISTS User(userName char(15), grade int, semester int)")
    cur.execute("CREATE TABLE IF NOT EXISTS Subject(Subname char(15), Subday char(5), classstart int, classend int)")
    cur.execute("CREATE TABLE IF NOT EXISTS KeyWords(keyword1 char(15),keyword2 char(15), keyword3 char(15))")
    cur.execute("CREATE TABLE IF NOT EXISTS BBLoginInfo(BBID int, BBPW char(15))")
    cur.execute("CREATE TABLE IF NOT EXISTS Subnum(snumber int)")
    cur.execute("CREATE TABLE IF NOT EXISTS Semester(semyear int, semmonth int, semday int)") #시작날짜 처음 설정할때 저장

    return 0

#블랙보드 아이디 반환 함수
def BlackboardID() :
    con, cur = None, None
    data1, data2 = "", ""
    sql = ""
    con = sqlite3.connect("C:\\StudyHelper\\StudyHelper")
    cur = con.cursor()
    cur.execute("SELECT BBID FROM BBLoginInfo")

    BBuserID = cur.fetchone()

    return BBuserID

# 블랙보드 패스워드 반환 함수
def BlackboardPW():
    con, cur = None, None
    data1, data2 = "", ""
    sql = ""
    con = sqlite3.connect("C:\\StudyHelper\\StudyHelper")
    cur = con.cursor()
    cur.execute("SELECT BBPW FROM BBLoginInfo")

    BBuserPW = cur.fetchone()

    return BBuserPW

#과목명으로 폴더 생성 함수
def MakingFolder(subnum) :
    #데이터베이스 StudyHelper에 접속합니다.
    con = sqlite3.connect("C:\\StudyHelper\\StudyHelper")
    cur = con.cursor()
    #커서를 통해 Subject 테이블에서 Subname 열만 추출
    cur.execute("SELECT Subname FROM Subject")
    for i in range(0, subnum, 1) :
        #커서에서 첫 번째 데이터를 가져와 폴더 이름 변수에 저장합니다.
        foldername = cur.fetchone()
        #저장된 폴더명으로 폴더 생성
        if not os.path.exists("%s\\Desktop\\%s" % (BFR, foldername[0])):
            os.mkdir("%s\\Desktop\\%s" % (BFR, foldername[0]))

    return 0

#키워드로 검색하는 함수
def SearchKeywords() :
    # subnum 받아오기
    con, cur = None, None
    con = sqlite3.connect("C:\\StudyHelper\\StudyHelper")
    cur = con.cursor()
    cur.execute("SELECT snumber FROM Subnum")
    temp = cur.fetchone()
    subnum = int(temp[0])

    # 우선 옮겨갈 폴더 경로 지정
    con, cur = None, None
    con = sqlite3.connect("C:\\StudyHelper\\StudyHelper")
    cur = con.cursor()
    cur.execute("SELECT Subname FROM Subject")

    for i in range(0, subnum, 1):  # 경로  지정  리스트 생성
        folder_name = cur.fetchone()
        folderroot.append("%s\\%s" % (DesktopRoot, folder_name[0]))  # 각각의 경로를 문자열로 리스트에 저장

    con, cur = None, None  # 키워드별 검색 단계로 넘어가기 위해 커서 재지정
    con = sqlite3.connect("C:\\StudyHelper\\StudyHelper")
    cur = con.cursor()
    cur.execute("SELECT * FROM KeyWords")  # 키워드 테이블에서 하나씩 전부 읽어올거임

    for j in range(0, subnum, 1):  # 과목별 반복 실행
        keyword_search = cur.fetchone()  # 한 과목의 키워드 목록을 튜플 keyword_search에 저장
        for k in range(0, 3, 1):  # 키워드별 검색 실행. 이때 공백이 아닐경우만 실행할것
            if ((keyword_search[k] != "") & (keyword_search[k] != None)):  # 공백이 아니라면(사용자가 키워드를 설정해놨다면)
                for root, subdirs, files in os.walk(r"%s" % DesktopRoot):  # 바탕화면에서 검색 실행
                    for f in files:
                        if keyword_search[k] in f:
                            file_to_move = os.path.join(root, f)
                            try:
                                shutil.move(file_to_move, r"%s" % folderroot[j])  # folderroot[j]는 과목명으로 된 폴더. 여기로 이동시킴
                            except:
                                pass

                for root, subdirs, files in os.walk(r"%s" % DownloadsRoot):  # 다운로드 폴더에서 검색 실행
                    for f in files:
                        if keyword_search[k] in f:
                            file_to_move = os.path.join(root, f)
                            try:
                                shutil.move(file_to_move, r"%s" % folderroot[j])
                            except:
                                pass

                for root, subdirs, files in os.walk(r"%s" % KDRoot):  # 카톡 받은파일 폴더에서 검색 실행
                    for f in files:
                        if keyword_search[k] in f:
                            file_to_move = os.path.join(root, f)
                            try:
                                shutil.move(file_to_move, r"%s" % folderroot[j])
                            except:
                                pass
    #threading.Timer(3600, SearchKeywords).start()
    return 0

#생성 시간에 따른 검색 함수
def ClassTimeSearch(root) :
    #subnum 받아오기
    con, cur = None, None
    con = sqlite3.connect("C:\\StudyHelper\\StudyHelper")
    cur = con.cursor()
    cur.execute("SELECT snumber FROM Subnum")
    temp = cur.fetchone()
    subnum = int(temp[0])

    # 우선 옮겨갈 폴더 경로 먼저 지정
    con, cur = None, None
    con = sqlite3.connect("C:\\StudyHelper\\StudyHelper")
    cur = con.cursor()
    cur.execute("SELECT Subname FROM Subject")
    for i in range(0, subnum, 1):  # 경로  지정  리스트 생성
        folder_name = cur.fetchone()
        folderroot.append("%s\\%s" % (root, folder_name[0]))  # 각각의 경로를 문자열로 리스트에 저장

    # 검색대상 폴더 위치 지정
    os.chdir(root)
    all_files = os.listdir()
    outputs = os.getcwd()

    # 시간 정보 이름 지정
    days = ['월', '화', '수', '목', '금', '토', '일']
    times = ['12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '00', '01', '02', '03', '04',
             '05', '06', '07', '08', '09', '10', '11,', '12']

    for files in all_files:
        try:
            # 디렉터리 파일로 이동
            inputs = glob.glob(files + "\\*")

            # 이제 다시 통과하기 위한 루프를 실행합니다.
            # 폴더 안의 모든 파일
            for ele in inputs:
                # 이제 파일을 하나씩 이동합니다.
                shutil.move(ele, outputs)

            # 폴더에서 파일을 추출한 후
            # 그 폴더를 삭제하다
            shutil.rmtree(files)
        except:
            pass

    #학기시작일 받아오기
    semtemp = date1.entry.get()
    tempyear = int(semtemp[0:4])
    tempmonth = int(semtemp[5:7])
    tempday = int(semtemp[8:10])

    # 다시 현재 디렉토리에 있는 모든 파일에 대해서
    for files in os.listdir('.'):
        # 파일 생성에 대한 모든 세부 정보 가져오기 및 수정
        time_format = time.gmtime(os.path.getctime(files))
        if time_format.tm_year >= tempyear and (time_format.tm_mon >= tempmonth) :  # gui랑 합칠 때 학기시작일 불러온 뒤 데이터형에 맞추도록 수정
            # 이제 년, 월 및 일만 추출합니다.
            datetime_object = datetime.datetime.strptime(str(time_format.tm_mon),
                                                         "%m")  # time_format.tm_mon = 월(0-11; 1월 = 0)
            # 숫자를 입력하고 월을 찾습니다.
            full_month_name = datetime_object.strftime("%b")  # %b는 월 출력 포맷
            full_weekday_name = datetime_object.strftime("%w")

            # 파일 생성 요일과 시간을 각각 변수에 저장
            fileday = days[time_format.tm_wday]
            filetime = times[(time_format.tm_hour) - 3]

            con, cur = None, None  # 과목별로 시간표랑 대조해야되니까 데이터베이스 다시 불러오기
            con = sqlite3.connect("C:\\StudyHelper\\StudyHelper")
            cur = con.cursor()
            cur.execute("SELECT * FROM Subject")

            # files에 대해, 과목 시간표를 불러와 시간정보를 대조해봅니다.
            # 아래 조건식들은 gui파트랑 맞춰서 갈아엎을것!!!
            for i in range(0, subnum, 1):  # subnum만큼 fetchone해서 과목별로 실행
                tempsubdata = cur.fetchone()  # 해당 과목의 시간표 변수인 문자열을 불러와 tempsubdata에 저장.
                classday = str(tempsubdata[1])  # 수업요일
                classstart = int(tempsubdata[2])  # 수업시작시간
                classend = int(tempsubdata[3])  # 수업종료시간

                if (fileday == classday):
                    for m in range(classstart, classend, 1):
                        if (filetime == m):
                            try:
                                shutil.move(files, r"%s" % folderroot[i])
                            except:
                                pass

    #threading.Timer(3600, ClassTimeSearch(root)).start()
    return 0

##홍은성 추가 함수 끝



#태그내용에서 text부분만 가져오는 함수 - 파이썬은 list를 넘기면 자동으로 참조에 의한 호출
def change_text(list):
    for i in range(0,len(list)):
        list[i]=list[i].text

#로그인버튼 클릭시 gui 멈춤 현상 방지를 위한 멀티스레드
def th():
    th = Thread(target=Button_Click)
    th.daemon = True
    th.start()
#과목정보 불러와 리스트에 삽입 후 트리뷰에 추가
def insert_sub():
    subnum = int(cbo1.get())
    con, cur = None, None
    data1, data2, data3, data4 = "", "", "", ""
    sql = ""
    con = sqlite3.connect("C:\\StudyHelper\\StudyHelper")
    cur = con.cursor()
    sql = "INSERT INTO Subnum VALUES('"+ str(subnum) + "')"
    con.execute(sql)
    con.commit()


    for i in range(0,subnum):
        con, cur = None, None
        data1, data2, data3, data4 = "", "", "", ""
        sql = ""
        con = sqlite3.connect("C:\\StudyHelper\\StudyHelper")
        cur = con.cursor()

        sub_name[i] = sub_name[i].get()
        sub_day[i] = sub_day[i].get()
        sub_start[i] = sub_start[i].get()
        sub_end[i] = sub_end[i].get()

        sql = "INSERT INTO Subject VALUES('" + str(sub_name[i]) + "', '" + str(sub_day[i]) + "', '" + str(sub_start[i]) + "', '" + str(sub_end[i]) + "')"
        con.execute(sql)
        con.commit()

    #폴더 생성
    MakingFolder(subnum)

    '''#학기시작날짜 받아오기 (폴더 정리 함수 내부에서 직접 추출하기로 수정)
    con, cur = None, None  # db에서 과목수 불러오기
    con = sqlite3.connect("C:\\StudyHelper\\StudyHelper")
    cur = con.cursor()
    semtemp = date1.entry.get()
    print(semtemp)
    tempyear = semtemp[0:4]
    print(tempyear)
    tempmonth = semtemp[5:7]
    print(tempmonth)
    tempday = semtemp[8:10]
    print(tempday)
    sql = "INSERT INTO Semester VALUES('" + tempyear + "', '" + tempmonth + "', '" + tempday + "')"
    cur.execute(sql)
    con.commit()'''

    tv4.delete(*tv4.get_children())
    for i in range(len(sub_name)):
            tv4.insert('', END, values=(sub_name[i],sub_day[i],str(sub_start[i]) + " ~ "+str(sub_end[i])))
#키워드 불러와 리스트에 삽입
def insert_keyword():
    con, cur = None, None #db에서 과목수 불러오기
    con = sqlite3.connect("C:\\StudyHelper\\StudyHelper")
    cur = con.cursor()
    cur.execute("SELECT snumber FROM Subnum")
    temp = cur.fetchone()
    subnum = temp[0]


    for i in range(0,subnum):
        key1[i] = key1[i].get()
        key2[i] = key2[i].get()
        key3[i] = key3[i].get()
    print(key1)
    print(key2)
    print(key3)

    con, cur = None, None #db에 추가
    sql = ""
    con = sqlite3.connect("C:\\StudyHelper\\StudyHelper")

    for i in range(0, subnum, 1) :
        sql = "INSERT INTO Keywords VALUES('" + key1[i] + "', '" + key2[i] + "', '" + key3[i] + "')"
        con.execute(sql)
        con.commit()

#과목 입력창 자식 프로세스
def child1():


    info = ttk.Toplevel(root, alpha = 1)

    if(sub_name):
        del sub_name[0:]
        del sub_day[0:]
        del sub_start[0:]
        del sub_end[0:]

    con, cur = None, None  # db접속
    sql = ""
    con = sqlite3.connect("C:\\StudyHelper\\StudyHelper")
    cur = con.cursor()
    sname, sday = "", ""
    sstart, sday = 0, 0

    for i in range(0,int(cbo1.get())):


        sub_name.append(ttk.StringVar())
        sub_day.append(ttk.StringVar())
        sub_start.append(ttk.IntVar())
        sub_end.append(ttk.IntVar())


        ttk.Label(info, text = str(i+1) + "번째 과목명",font = ("나눔고딕", 9)).grid(row=i,column=0,padx=15,pady=3)
        ttk.Entry(info,show=None,width=20,textvariable=sub_name[i]).grid(row=i,column=1,padx=10,pady=5)
        
        ttk.Label(info, text = "요일",font = ("나눔고딕", 9)).grid(row=i,column=2,padx=15,pady=3)
        ttk.Combobox(master=info,bootstyle = PRIMARY,font = ("나눔고딕", 9),values=['월', '화', '수','목','금','토','일'],textvariable = sub_day[i],width =3).grid(row=i,column=3,padx=10,pady=3)
        
        ttk.Label(info, text = "시작/종료시간",font = ("나눔고딕", 9)).grid(row=i,column=4,padx=15,pady=3)
        ttk.Entry(info,show=None,width=3,textvariable=sub_start[i]).grid(row=i,column=5,padx=10,pady=5)
        ttk.Label(info, text = "~",font = ("나눔고딕", 9)).grid(row=i,column=6,padx=5,pady=3)
        ttk.Entry(info,show=None,width=3,textvariable=sub_end[i]).grid(row=i,column=7,padx=10,pady=5)
        
    ttk.Button(info,text="완료", bootstyle=PRIMARY,command=lambda:[insert_sub(),info.destroy()]).grid(row=i+1, column=0,columnspan=8,ipady = 25,ipadx=360)
    info.mainloop()

#키워드 입력창 자식 프로세스
def child2():
    
    keyword = ttk.Toplevel(root, alpha = 1)

    if(key1):
        del key1[0:]
        del key2[0:]
        del key3[0:]


    for i in range(0,int(cbo1.get())):
        
        key1.append(ttk.StringVar())
        key2.append(ttk.StringVar())
        key3.append(ttk.StringVar())


        ttk.Label(keyword, text = sub_name[i],font = ("나눔고딕", 9)).grid(row=i,column=0,padx=15,pady=3)
        ttk.Label(keyword, text = "     키워드1",font = ("나눔고딕", 9)).grid(row=i,column=1,padx=15,pady=3)
        ttk.Entry(keyword,show=None,width=20,textvariable=key1[i]).grid(row=i,column=2,padx=10,pady=5)
        ttk.Label(keyword, text = "키워드2",font = ("나눔고딕", 9)).grid(row=i,column=3,padx=15,pady=3)
        ttk.Entry(keyword,show=None,width=20,textvariable=key2[i]).grid(row=i,column=4,padx=10,pady=5)
        ttk.Label(keyword, text = "키워드3",font = ("나눔고딕", 9)).grid(row=i,column=5,padx=15,pady=3)
        ttk.Entry(keyword,show=None,width=20,textvariable=key3[i]).grid(row=i,column=6,padx=10,pady=5)
        
    ttk.Button(keyword,text="완료", bootstyle=PRIMARY,command=lambda:[insert_keyword(),keyword.destroy()]).grid(row=i+1, column=0,columnspan=7,ipady = 25,ipadx=500)
    keyword.mainloop()
        
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
    WebDriverWait(driver, 99).until(EC.presence_of_element_located((By.XPATH, '//*[@id="base_tools"]/bb-base-navigation-button[3]/div/li/a')))
    sleep(0.5)
    driver.find_element_by_xpath('//*[@id="base_tools"]/bb-base-navigation-button[3]/div/li/a')
    html = driver.page_source
    soup = bs(html,'html.parser')
    myname = soup.text[(soup.text.find("."))+1:soup.text.find(".")+4]
    return myname
def Blackboard():
    global category_index #속성값 추출할 때 사용할 category의 index
    category_index = 0
    global cours,title #코스이름, 타이틀내용
    global category #카테고리
    global my_score,max_score,score #내성적, 만점성적, 내성적/만점성적
    global deadline #마감기한
    
#GUI카테고리 - 공지사항, 성적, 강의자료, 추가된 과제, 마감예정과제 (각각 코스와 타이틀 내용 따로 담음)
    driver.get('https://ecampus.chungbuk.ac.kr/ultra/stream')
    WebDriverWait(driver, 99).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="activity-stream"]/div[2]'))) #최근항목 구분div xpath
    response=driver.find_element_by_xpath('//*[@id="body-content"]').get_attribute('innerHTML')

    soup = bs(response, 'html.parser')

    ##전체 코스이름&타이틀내용##
    ##제공예정##
    upc_cours=soup.select('.js-upcomingStreamEntries.activity-group.columns.main-column>ul.activity-feed>li>div>div>div>div>div>a')
    upc_title=soup.select('.js-upcomingStreamEntries.activity-group.columns.main-column>ul.activity-feed>li>div>div>div>div>div.name>ng-switch>a')

    ##오늘##
    td_cours=soup.select('.js-todayStreamEntries.activity-group.columns.main-column>ul.activity-feed>li>div>div>div>div>div>a')
    td_title=soup.select('.js-todayStreamEntries.activity-group.columns.main-column>ul.activity-feed>li>div>div>div>div>div.name>ng-switch>a')

    ##최근항목##
    pre_cours=soup.select('.js-previousStreamEntries.activity-group.columns.main-column>ul.activity-feed>li>div>div>div>div>div>a')
    pre_title=soup.select('.js-previousStreamEntries.activity-group.columns.main-column>ul.activity-feed>li>div>div>div>div>div.name>ng-switch>a')

    change_text(upc_cours)
    change_text(upc_title)
    change_text(td_cours)
    change_text(td_title)
    change_text(pre_cours)
    change_text(pre_title)

    cours=upc_cours+td_cours+pre_cours
    title=upc_title+td_title+pre_title


    ##카테고리 구분##
    category=soup.select('svg[class="MuiSvgIconroot-0-2-37 makeStylesdirectionalIcon-0-2-36 makeStylesstrokeIcon-0-2-35 MuiSvgIconcolorPrimary-0-2-38 MuiSvgIconfontSizeLarge-0-2-45"]')

    #aria-label의 속성값만 추출
    for icon in category:
        category[category_index]=icon['aria-label']
        category_index+=1

    ##성적##
    my_score=soup.select('span[class="grade-input-display ready"]')
    max_score=soup.select('span[class="points-text"]>bdi')

    change_text(my_score)
    change_text(max_score)
        
    for i in range(0,len(my_score)):
        score.append(my_score[i]+"/"+max_score[i])

    #마감예정과제 마감기한 가져오기
    deadline=soup.select('.content>span>bb-translate>bdi')

    change_text(deadline)
    
#GUI카테고리별로 들어갈 내용 분류 함수
def GUI_category():
    for i in range(len(category)):
        if(category[i]=="공지 사항"):
            Notice_cours.append(cours[i])
            Notice_title.append(title[i])
        elif(category[i]=="성적"):
            Score_cours.append(cours[i])
            Score_title.append(title[i])
        elif(category[i]=="과제"):
            #추가된 과제
            if(title[i][0]=="추"):
                Ass_cours.append(cours[i])
                Ass_title.append(title[i])
            #마감예정과제
            elif(title[i][0]=="마"):
                DeadlineAss_cours.append(cours[i])
                DeadlineAss_title.append(title[i])
        elif(category[i]=="프레젠테이션" or "텍스트 문서" or "pdf"):
            Document_cours.append(cours[i])
            Document_title.append(title[i])
            
# 로그인 버튼 클릭시 이벤트
def Button_Click():
    try:
        ttk.Label(root, text = "          로그인중...",font = ("나눔고딕", 10)).grid(row=1,column=3,rowspan=2,padx=5,ipady=25,ipadx=50)
        Login()
        Blackboard()
        messagebox.showinfo('로그인','로그인 성공')
        ttk.Label(root, text = "               "+Find_Name()+"님 환영합니다.",font = ("나눔고딕", 10)).grid(row=1,column=3,rowspan=2,padx=5,ipady=25,ipadx=40)
        GUI_category()
        print(Notice_cours)
        for i in range(len(score)):
            tv.insert('', END, values=(Score_cours[i],Score_title[i],score[i]))
        for i in range(len(DeadlineAss_cours)):
            tv2.insert('', END, values=(DeadlineAss_cours[i],DeadlineAss_title[i],deadline[i]))
        for i in range(len(Notice_cours)):
            tv3.insert('', END, values=(Notice_cours[i],Notice_title[i]))
    except:
        messagebox.showerror('로그인', '로그인 실패')
        ttk.Label(root, text = "               게스트님 환영합니다.",font = ("나눔고딕", 10)).grid(row=1,column=3,rowspan=2,padx=5,ipady=25,ipadx=40)
        pass 

    
#메인 창 설정  
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

#로그인 버튼
ttk.Button(root,text="LOGIN", bootstyle=(PRIMARY, "outline-toolbutton"),command=th).grid(row=1, column=2,rowspan=2,sticky=ttk.W,ipady = 25,ipadx=40)

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
f5 = ttk.Frame(nb)
nb.add(f5, text="     메인     ", sticky=NW)
ttk.Label(f5, text = "폴더 관리기능 켜기",font = ("나눔고딕", 9)).grid(row=1,column=1,padx=25,pady=10)

#폴더관리ONOFF 체크버튼
chk = ttk.IntVar()
ttk.Checkbutton(f5, text="",variable = chk, bootstyle="round-toggle").grid(row=1,column=2,pady=3,sticky=ttk.W)

ttk.Label(f5, text = "     학기 시작일",font = ("나눔고딕", 9)).grid(row=2,column=1,padx=25,pady=3)
#학기시작날짜 버튼
date1 = ttk.DateEntry(f5,bootstyle=PRIMARY,startdate=dt)
date1.grid(row=2, column=2,columnspan = 2, sticky=ttk.W, pady=3)

ttk.Label(f5, text = "     수강 과목 수",font = ("나눔고딕", 9)).grid(row=3,column=1,padx=25,pady=3)

#과목 수 선택 콤보박스
cbo1 = ttk.Combobox(master=f5,bootstyle = PRIMARY,font = ("나눔고딕", 8),values=['1', '2', '3','4','5','6','7','8','9','10'],width =1)
cbo1.current (4)
cbo1.grid(row=3,column=2,sticky = ttk.W,pady=3,ipadx = 9)

#과목정보,키워드입력 버튼
ttk.Button(f5,text="과목 정보 입력", bootstyle=PRIMARY,command=child1).grid(row=3, column=3,sticky=ttk.W,ipadx=2,padx=3)
ttk.Button(f5,text="과목 키워드 입력", bootstyle=PRIMARY,command=child2).grid(row=3, column=4,sticky=ttk.W)

ttk.Label(f5, text = "     ",font = ("나눔고딕", 9)).grid(row=3,column=5,padx=25,pady=3)

#과목입력정보 트리뷰( *tv = treeview 약자 )
tv4 = ttk.Treeview(
        master=f5,
        columns=[0, 1,2],
        show=HEADINGS,
        height=9
    )
tv4.heading(0, text='과목명')
tv4.heading(1, text='요일')
tv4.heading(2, text='시작/종료시간')
tv4.column(0, width=250,anchor=CENTER)
tv4.column(1, width=100, anchor=CENTER)
tv4.column(2, width=300,anchor=CENTER)
tv4.grid(row=4,column=1,columnspan=5,padx=20,pady=10)


#탭2(공지)
f4 = ttk.Frame(nb)

#트리뷰
tv3 = ttk.Treeview(
        master=f4,
        columns=[0, 1],
        show=HEADINGS,
        height=15
    )
tv3.heading(0, text='과목명')
tv3.heading(1, text='내용')
tv3.column(0, width=190 , anchor=CENTER)
tv3.column(1, width=460, anchor=CENTER)
tv3.pack(side=LEFT, anchor=NE, fill=X,padx = 20,pady = 10)

nb.add(f4,text="  공지사항  ",sticky=NW)


#탭3(과제)
f2 = ttk.Frame(nb)

#트리뷰
tv2 = ttk.Treeview(
        master=f2,
        columns=[0, 1,2],
        show=HEADINGS,
        height=15
    )
tv2.heading(0, text='과목명')
tv2.heading(1, text='과제')
tv2.heading(2, text='마감기한')
tv2.column(0, width=190,anchor=CENTER)
tv2.column(1, width=350, anchor=CENTER)
tv2.column(2, width=110)
tv2.pack(side=LEFT, anchor=NE, fill=X,padx = 20,pady = 10)
nb.add(f2, text='    과제    ',sticky =NW)


#탭4(성적)
f3 = ttk.Frame(nb)

#트리뷰
tv = ttk.Treeview(
        master=f3,
        columns=[0, 1,2],
        show=HEADINGS,
        height=15
    )
tv.heading(0, text='과목명')
tv.heading(1, text='내용')
tv.heading(2, text='성적')
tv.column(0, width=190 , anchor=CENTER)
tv.column(1, width=350, anchor=CENTER)
tv.column(2, width=110, anchor=CENTER)
tv.pack(side=LEFT, anchor=NE, fill=X,padx = 20,pady = 10)
nb.add(f3,text = "     성적     ",sticky=NW)
# 창 숨기는 옵션 추가
options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome('C:\Chrome_Driver\chromedriver.exe',)

#크롬으로 블랙보드 로그인 화면 접속
url = "https://ecampus.chungbuk.ac.kr/"
driver.get(url)

#db접속
con, cur = None, None
con = sqlite3.connect("C:\\StudyHelper\\StudyHelper")
cur = con.cursor()

#로컬디렉토리, 테이블 존재 여부 확인 - 없을 시 생성
MakingLocDir()
MakingTable()

#폴더관리기능 실행
ClassTimeSearch(DesktopRoot)
ClassTimeSearch(DownloadsRoot)
ClassTimeSearch(KDRoot)
SearchKeywords()


root.mainloop()
