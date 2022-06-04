##과제마감시간 슬랙으로 알림##

#문자열 분석해서 .이랑 :이거를 죄다 ,(쉼표)로 바꿔서 datetime에 넣기 -> 22,6,5,23,59
for i in range(0,len(DA_deadline)):
    DA_deadline[i]=DA_deadline[i].replace('.',',')
    DA_deadline[i]=DA_deadline[i].replace(':',',')
    DA_deadline[i]=DA_deadline[i].replace(' ','') #공백없애기

#input으로 사용자한테 받아야함
token = "[사용자 토큰]" #사용자 토큰
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
            
        if remain[i]<=60:
            text_[i]=DeadlineAss_cours[i]+"의 ["+DeadlineAss_title[i][4:]+"] 과제가 1시간 남았습니다."
        
    if pre_text[i]!=text_[i]:
        text=text_[i]
        requests.post("https://slack.com/api/chat.postMessage",
            headers={"Authorization": "Bearer "+token},
            data={"channel": channel,"text": text})
        pre_text[i]=text_[i] #이전 텍스트에 넣어서 중복여부 파악
