##전체 소스코드##

#현재 3.14.1 selenium 버전 사용중
from selenium import webdriver
from time import sleep #타임 객체 선언
import requests
from bs4 import BeautifulSoup as bs

#Webdrive쓰기 위해 import
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

##전역변수 선언##
user_id, uesr_pw="",""
login_stop=1 #로그인 예외처리 변수
category_index=0 #속성값 추출할 때 사용할 category의 index

cours,title=[],[] #코스이름, 타이틀내용
category=[] #카테고리
my_score,max_score,score=[],[],[] #내성적, 만점성적, 내성적/만점성적
deadline=[] #마감기한

#GUI카테고리 - 공지사항, 성적, 강의자료, 추가된 과제, 마감예정과제 (각각 코스와 타이틀 내용 따로 담음)
Notice_cours, Score_cours, Document_cours, Ass_cours, DeadlineAss_cours=[],[],[],[],[]
Notice_title, Score_title, Document_title, Ass_title, DeadlineAss_title=[],[],[],[],[]

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
cours=soup.select('.context.ellipsis>a')
title=soup.select('.js-title-link')

change_text(cours) 
change_text(title)

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

##GUI카테고리 리스트 구분##
GUI_category()

print(score)
