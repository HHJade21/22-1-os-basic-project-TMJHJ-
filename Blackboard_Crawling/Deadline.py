#●처음~soup = bs(response, 'html.parser')까지 코드 생략●#

#마감예정과제 마감기한 가져오기
deadline=soup.select('.content>span>bb-translate>bdi')

for i in range(0,len(deadline)):
    deadline[i]=deadline[i].text

print(deadline)
