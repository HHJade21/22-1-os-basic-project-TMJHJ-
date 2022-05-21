import sqlite3

##변수 선언 부분##
con, cur = None, None
data1, data2, data3, data4 = "", "", "", ""
sql = ""

##메인 코드 부분##
con = sqlite3.connect("C:/osproject202201/22-1-os-basic-project-TMJHJ-/StudyHelper")
cur = con.cursor()


#학번 항목에서 공백을 입력할 때까지 새로운 데이터 행을 추가함
while(True):
    #일단 data1~5 변수에 각 항목을 임시 저장
    data1 = input("학번 ==> ")
    if data1 =="":
        break;
    data2 = input("이름 ==> ")
    data3 = input("학년 ==> ")
    data4 = input("학기 ==> ")
    data5 = input("연도 ==> ")
#data1~5가 모두 정상적으로 입력되었으면 데이터베이스에 한번에 추가
    sql = "INSERT INTO User VALUES('"+ data1 + "', '"+ data2 + "', '"+ data3 + "', '"+ data4 + "', "+ data5 +")"
    cur.execute(sql)


con.commit()
con.close()
