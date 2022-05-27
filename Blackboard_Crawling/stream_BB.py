#현재 3.14.1 selenium 버전 사용중
from selenium import webdriver
#타임 객체 선언
from time import sleep
import requests
from bs4 import BeautifulSoup as bs

#크롬 웹 드라이버 경로
driver = webdriver.Chrome('C:\Chrome_Driver\chromedriver.exe')

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
    

#활동스트림 내용 담은 element 가져오기
sleep(5)
response=driver.find_element_by_xpath('//*[@id="body-content"]').get_attribute('innerHTML')

soup = bs(response, 'html.parser')
soup=soup.find("span")
print(soup) #soup.prettify() : html구조를 파악하기 쉽게 바꿔줌
