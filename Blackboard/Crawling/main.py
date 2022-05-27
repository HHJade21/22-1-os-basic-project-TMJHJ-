##전체 소스코드##

#현재 3.14.1 selenium 버전 사용중
from selenium import webdriver
#타임 객체 선언
from time import sleep
import requests
from bs4 import BeautifulSoup as bs

#Webdrive쓰기 위해 import
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

##전역변수 선언##
login_stop=1 #로그인 예외처리 변수
category_index=0 #속성값 추출할 때 사용할 category의 index
score=[] #내 성적 / 만점 성적

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

##제공예정##
upc_cours=soup.select('.js-upcomingStreamEntries.activity-group.columns.main-column>ul.activity-feed>li>div>div>div>div>div>a')
upc_title=soup.select('.js-upcomingStreamEntries.activity-group.columns.main-column>ul.activity-feed>li>div>div>div>div>div.name>ng-switch>a')

##오늘##
td_cours=soup.select('.js-todayStreamEntries.activity-group.columns.main-column>ul.activity-feed>li>div>div>div>div>div>a')
td_title=soup.select('.js-todayStreamEntries.activity-group.columns.main-column>ul.activity-feed>li>div>div>div>div>div.name>ng-switch>a')

##최근항목##
pre_cours=soup.select('.js-previousStreamEntries.activity-group.columns.main-column>ul.activity-feed>li>div>div>div>div>div>a')
pre_title=soup.select('.js-previousStreamEntries.activity-group.columns.main-column>ul.activity-feed>li>div>div>div>div>div.name>ng-switch>a')

#문자열만 추출 - len() : 리스트 크기
for i in range(0,len(upc_cours)):
    upc_cours[i]=upc_cours[i].text
    upc_title[i]=upc_title[i].text
for i in range(0,len(td_cours)):
    td_cours[i]=td_cours[i].text
    td_title[i]=td_title[i].text
for i in range(0,len(pre_cours)):
    pre_cours[i]=pre_cours[i].text
    pre_title[i]=pre_title[i].text

##카테고리 구분##
category=soup.select('svg[class="MuiSvgIconroot-0-2-37 makeStylesdirectionalIcon-0-2-36 makeStylesstrokeIcon-0-2-35 MuiSvgIconcolorPrimary-0-2-38 MuiSvgIconfontSizeLarge-0-2-45"]')

#aria-label의 속성값만 추출
for icon in category:
    category[category_index]=icon['aria-label']
    category_index+=1

##성적##
myScore=soup.select('span[class="grade-input-display ready"]')
max_score=soup.select('span[class="points-text"]')

for i in range(0,len(myScore)):
    myScore[i]=myScore[i].text
    max_score[i]=max_score[i].text
    
for i in range(0,len(myScore)):
    score.append(myScore[i]+max_score[i])

print(category)
