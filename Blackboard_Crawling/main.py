##전체 소스코드##

#현재 3.14.1 selenium 버전 사용중
from xml.etree.ElementPath import prepare_predicate
from selenium import webdriver
from time import sleep #타임 객체 선언
import requests
from bs4 import BeautifulSoup as bs

#현재 시간 가져오기
from datetime import datetime
import requests #슬랙

#Webdrive쓰기 위해 import
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

##프로그램 반복실행 시 절대 다시 돌리면 안되는 변수 - 초기화 시키면X ##
diff=[0 for i in range(20)] #뺀 시간
remain=["" for i in range(20)] #남은 시간
text_=["" for i in range(20)] #슬랙 메세지
pre_text=["" for i in range(20)] #슬랙 이전 메세지 (중복방지)
DA=["" for i in range(20)] #날짜/시간 콤마로 짤라 넣을 리스트

while(1):
    ##전역변수 선언##
    user_id, uesr_pw="",""
    login_stop=1 #로그인 예외처리 변수
    category_index=0 #속성값 추출할 때 사용할 category의 index

    upc_cours,upc_title,td_cours,td_title,pre_cours,pre_title=[],[],[],[],[],[] #제공예정, 오늘, 최근항목
    cours,title=[],[] #코스이름, 타이틀내용
    category=[] #카테고리
    my_score,max_score,score=[],[],[] #내성적, 만점성적, 내성적/만점성적
    deadline,DA_deadline=[],[] #마감기한, 마감예정과제의 마감기한

    #GUI카테고리 - 공지사항, 성적, 강의자료, 추가된 과제, 마감예정과제 (각각 코스와 타이틀 내용 따로 담음)
    Notice_cours, Score_cours, Document_cours, Ass_cours, AddAss_cours, DeadlineAss_cours=[],[],[],[],[],[]
    Notice_title, Score_title, Document_title, Ass_title, AddAss_title, DeadlineAss_title=[],[],[],[],[],[]

    #시간
    month,day,hour,minute=0,0,0,0 #현재시간 담을 변수
    token,channess_montl,text="","",""
    colon=0


    ##함수 선언##
    #태그내용에서 text부분만 가져오는 함수 - 파이썬은 list를 넘기면 자동으로 참조에 의한 호출
    def change_text(list):
        for i in range(0,len(list)):
            list[i]=list[i].text
        
    #GUI카테고리별로 들어갈 내용 분류 함수
    def GUI_category():
        for i in range(len(category)):
            if(category[i]=="공지 사항"):
                Notice_cours.append(cours[i])
                Notice_title.append(title[i])
            elif(category[i]=="성적"):
                if(title[i][0]!="새"):
                    Score_cours.append(cours[i])
                    Score_title.append(title[i])
            elif(category[i]=="과제"):
                #과제 전부
                Ass_cours.append(cours[i])
                Ass_title.append(title[i])
                #추가된 과제
                if(title[i][0]=="추"):
                    AddAss_cours.append(cours[i])
                    AddAss_title.append(title[i])
                #마감예정과제
                elif(title[i][0]=="마"):
                    DeadlineAss_cours.append(cours[i])
                    DeadlineAss_title.append(title[i])
            elif(category[i]=="프레젠테이션" or "텍스트 문서" or "pdf" or "여러 문서"):
                Document_cours.append(cours[i])
                Document_title.append(title[i])

    #크롬 웹 드라이버 경로
    driver = webdriver.Chrome('C:\Chrome_Driver\chromedriver.exe')

    #로그인 실패 예외처리 - 실패시 다시 로그인 / 성공시 넘어감
    while(login_stop):
        try:
            #크롬으로 블랙보드 로그인 화면 접속
            url = "https://ecampus.chungbuk.ac.kr/"
            driver.get(url)

            #아이디와 비밀번호 입력(0.5초씩 기다리기) - 너무 빠르면 대형 사이트는 트래픽 공격으로 인식
            print('user_id : ')
            user_id = input()
            sleep(0.5)
            driver.find_element_by_name('uid').send_keys(user_id)

            print('user_pw : ')
            user_pw = input()
            sleep(0.5)
            driver.find_element_by_name('pswd').send_keys(user_pw)

            #Xpath
            driver.find_element_by_xpath('//*[@id="entry-login"]').click()

            #사이트 이동
            driver.get('https://ecampus.chungbuk.ac.kr/ultra/stream')

            #while반복 멈추기
            login_stop=0
        except:
            pass

    #활동스트림 내용 담은 element 가져오기
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="activity-stream"]/div[2]'))) #최근항목 구분div xpath
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

    ##GUI카테고리 리스트 구분##
    GUI_category()

    #마감예정과제 마감기한 가져오기
    deadline=soup.select('.content>span>bb-translate>bdi')

    change_text(deadline)

    #추가된 과제의 마감기한까지 나오는데 Ass_title을 이용해서 추가된 과제 마감기한은 없애야돼
    for i in range(0,len(deadline)):
        if(Ass_title[i][0]=="마"):
            DA_deadline.append(deadline[i])

    ##과제마감시간 슬랙으로 알림##

    #문자열 분석해서 .이랑 :이거를 죄다 ,(쉼표)로 바꿔서 datetime에 넣기 -> 22,6,5,23,59
    for i in range(0,len(DA_deadline)):
        DA_deadline[i]=DA_deadline[i].replace('.',',')
        DA_deadline[i]=DA_deadline[i].replace(':',',')
        DA_deadline[i]=DA_deadline[i].replace(' ','') #공백없애기

    #input으로 사용자한테 받아야함
    token = "[사용자토큰]" #사용자 토큰
    channel = "#chatbot" #채널이름

    #하루, 1시간 전으로 테스트
    for i in range(0,len(DA_deadline)):
        #몇분 남았는지 계산
        now = datetime.now()
        DA=DA_deadline[i].split(',')
        future = datetime(int("20"+DA[0]),int(DA[1]),int(DA[2]),int(DA[3]),int(DA[4]))
        print(future)
        diff[i]=future-now
        remain[i]=(diff[i].days*1440)+(diff[i].seconds/60) #일수*1440(하루 1440분)+시간 차이의 초를 /60으로 나눠서 분으로 만듦
        
        #remain[i]은 과제까지 남은 '분'
        if remain[i]<=24*60:
            text_[i]=DeadlineAss_cours[i]+"의 ["+DeadlineAss_title[i][4:]+"] 과제가 1일(24시간) 남았습니다."

            if remain[i]<=5*60:
                text_[i]=DeadlineAss_cours[i]+"의 ["+DeadlineAss_title[i][4:]+"] 과제가 1시간 남았습니다."
                
                if remain[i]<=60:
                    text_[i]=DeadlineAss_cours[i]+"의 ["+DeadlineAss_title[i][4:]+"] 과제가 1시간 남았습니다."
        
        if pre_text[i]!=text_[i]:
            text=text_[i]
            requests.post("https://slack.com/api/chat.postMessage",
                headers={"Authorization": "Bearer "+token},
                data={"channel": channel,"text": text})
            pre_text[i]=text_[i] #이전 텍스트에 넣어서 중복여부 파악
    
    #5초 뒤 반복실행
    for i in range(5,0,-1):
        print(str(i)+"...")
        sleep(1)

