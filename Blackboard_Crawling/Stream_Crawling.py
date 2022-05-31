##활동스트림에서 코스이름, 타이틀 내용 -> 제공예정/오늘/최근항목 으로 구분해서 가져오기 수행##

#●처음~soup = bs(response, 'html.parser')까지 코드 생략●#

##cours & title 크롤링##
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
for i in range(0,10):
    pre_cours[i]=pre_cours[i].text
    pre_title[i]=pre_title[i].text

#select()는 리스트로 담음
for i in range(len(upc_cours)):
    print(upc_cours[i])
    print(upc_title[i])
print("\n")
for i in range(len(td_cours)):
    print(td_cours[i])
    print(td_title[i])
    
print("\n")
for i in range(10):
    print(pre_cours[i])
    print(pre_title[i])
