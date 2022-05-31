##성적 가져오기 - 내 성적 / 만점성적##

##성적##
myScore=soup.select('span[class="grade-input-display ready"]')
max_score=soup.select('span[class="points-text"]')

for i in range(0,len(myScore)):
    myScore[i]=myScore[i].text
    max_score[i]=max_score[i].text
    
for i in range(0,len(myScore)):
    score.append(myScore[i]+max_score[i])

for i in range(0,len(myScore)):
    print(score[i])
