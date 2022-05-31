## 과제/공지사항/성적/강의자료 카테고리 분류하기 - 속성값 이용##

##전역변수 선언##
category_index=0 #속성값 추출할 때 사용할 category의 index

#●처음~soup = bs(response, 'html.parser')까지 코드 생략●#

##제공예정##
upc_cours=soup.select('.js-upcomingStreamEntries.activity-group.columns.main-column>ul.activity-feed>li>div>div>div>div>div>a')
upc_title=soup.select('.js-upcomingStreamEntries.activity-group.columns.main-column>ul.activity-feed>li>div>div>div>div>div.name>ng-switch>a')

##오늘##
td_cours=soup.select('.js-todayStreamEntries.activity-group.columns.main-column>ul.activity-feed>li>div>div>div>div>div>a')
td_title=soup.select('.js-todayStreamEntries.activity-group.columns.main-column>ul.activity-feed>li>div>div>div>div>div.name>ng-switch>a')

##최근항목##
pre_cours=soup.select('.js-previousStreamEntries.activity-group.columns.main-column>ul.activity-feed>li>div>div>div>div>div>a')
pre_title=soup.select('.js-previousStreamEntries.activity-group.columns.main-column>ul.activity-feed>li>div>div>div>div>div.name>ng-switch>a')

##카테고리 구분##
category=soup.select('svg[class="MuiSvgIconroot-0-2-37 makeStylesdirectionalIcon-0-2-36 makeStylesstrokeIcon-0-2-35 MuiSvgIconcolorPrimary-0-2-38 MuiSvgIconfontSizeLarge-0-2-45"]')

#aria-label의 속성값만 추출
for icon in category:
    category[category_index]=icon['aria-label']
    category_index+=1

print('<제공예정>')
for i in range(0,len(upc_cours)):
    print(category[i])
print('\n<오늘>')
for i in range(len(upc_cours),len(upc_cours)+len(td_cours)):
    print(category[i])
print('\n<최근항목>')
for i in range(len(upc_cours)+len(td_cours),len(upc_cours)+len(td_cours)+10):
    print(category[i])
