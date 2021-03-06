import os
import sqlite3
import shutil
import schedule
import time

##전역 변수 선언 부분##
subnum = 0


##함수 선언 부분##

#데이터베이스 생성
def MakingTable() :


    #사용자 정보 테이블과 과목정보 테이블을 각각 생성
    cur.execute("CREATE TABLE IF NOT EXISTS User(stdid int, userName char(15), grade int, semester int, year int)")
    cur.execute("CREATE TABLE IF NOT EXISTS Subject(Subname char(15), Professor char(15), Firsttime char(5), Secondtime char(5))")
    cur.execute("CREATE TABLE IF NOT EXISTS KeyWord(keyword1 char(15),keyword2 char(15), keyword3 char(15), keyword4 char(15), keyword5 char(15), keyword6 char(15), keyword7 char(15), keyword8 char(15), keyword9 char(15), keyword10 char(15))")


    return 0


#테이블 존재 여부 확인. 있으면 1, 없으면 0 반환
def TableExistCheck() :
    table_name = 'User'
    sql = f'SELECT * FROM sqlite_master WHERE type = "table" AND name = "{table_name}"'
    cur.execute(sql)
    rows = cur.fetchall()
    if rows :
        return 1
    else :
        return 0

#사용자 정보 입력 함수
def InsertUserData() :
    con, cur = None, None
    data1, data2, data3, data4 = "", "", "", ""
    sql = ""
    con = sqlite3.connect("C:\\StudyHelper\\StudyHelper")
    cur = con.cursor()

    data1 = input("학번 ==> ")
    data2 = input("이름 ==> ")
    data3 = input("학년 ==> ")
    data4 = input("학기 ==> ")
    data5 = input("연도 ==> ")
    #data1~5가 모두 정상적으로 입력되었으면 데이터베이스에 한번에 추가
    sql = "INSERT INTO User VALUES('"+ data1 + "', '"+ data2 + "', '"+ data3 + "', '"+ data4 + "', "+ data5 +")"
    cur.execute(sql)

    return 0


#과목명으로 폴더 생성 함수
def MakingFolder() :
    #데이터베이스 StudyHelper에 접속합니다.
    con = sqlite3.connect("C:\\StudyHelper\\StudyHelper")
    cur = con.cursor()
    #커서를 통해 Subject 테이블에서 Subname 열만 추출
    cur.execute("SELECT Subname FROM Subject")


    for i in range(0, subnum, 1) :
        #커서에서 첫 번째 데이터를 가져와 폴더 이름 변수에 저장합니다.
        foldername = cur.fetchone()

        #저장된 폴더명으로 폴더 생성
        os.mkdir("C:\\Users\\user\\Desktop\\%s" % foldername)


    return 0

#폴더 이동 함수
def MoveFolder():
    source = 'C:\\Users\\user\\Downloads'
    destination = 'C:\\Users\\user\\Desktop\\open'
    shutil.move(source,destination)
    schedule.every(5).seconds.do(shutil.move(source,destination))
    return 0

#생성 시간에 따른 검색 함수
def SearchWithTime() :
    #생성 시간 읽어오기까지 구현. 검색은 미구현
    import os.path, time

    file = "C:\\osproject202201\\22-1-os-basic-project-TMJHJ-\\searching\\searching.txt"

    print(os.path.getmtime(file)) #파일 생성 시간 데이터 확인
    print(time.ctime(os.path.getmtime(file))) #생성 시간 데이터를 str형으로 변환하여 '요일, 월, 일, 시간, 연도'순으로 출력

    print(type(time.ctime(os.path.getmtime(file)))) #str형인 것을 확인
    return 0


# 과목 정보 입력 함수
def InsertSubData():
    con, cur = None, None
    data1, data2, data3, data4 = "", "", "", ""
    sql = ""
    con = sqlite3.connect("C:\\StudyHelper\\StudyHelper")
    cur = con.cursor()

    i = 0
    subnum = int(input("이번 학기 수강 과목 수 : "))
    for i in range (subnum):
        data1 = input("교과목명 ==> ")
        data2 = input("교수명 ==> ")
        data3 = input("수업 시간1 ==> ")
        data4 = input("수업 시간2 ==> ")
        # data1~4가 모두 정상적으로 입력되었으면 데이터베이스에 한번에 추가
        sql = "INSERT INTO Subject VALUES('" + data1 + "', '" + data2 + "', '" + data3 + "', '" + data4 + "')"
        cur.execute(sql)

    return 0


# 키워드 정보 입력 함수
def InsertKeywords():
    con, cur = None, None
    data1, data2, data3, data4, data5, data6, data7, data8, data9, data10 = "", "", "", "", "", "", "", "", "", ""
    sql = ""
    con = sqlite3.connect("C:\\StudyHelper\\StudyHelper")
    cur = con.cursor()
    # 학번 항목에서 공백을 입력할 때까지 새로운 데이터 행을 추가함
    for i in range (0, subnum, 1):

        data1 = input("키워드 1 ==> ")
        data2 = input("키워드 2 ==> ")
        data3 = input("키워드 3 ==> ")
        data4 = input("키워드 4 ==> ")
        data5 = input("키워드 5 ==> ")
        data6 = input("키워드 6 ==> ")
        data7 = input("키워드 7 ==> ")
        data8 = input("키워드 8 ==> ")
        data9 = input("키워드 9 ==> ")
        data10 = input("키워드 10 ==> ")
        # data1~10가 모두 정상적으로 입력되었으면 데이터베이스에 한번에 추가
        sql = "INSERT INTO User VALUES('" + data1 + "', '" + data2 + "', '" + data3 + "', '" + data4 + "', " + data5 + ", '" + data6 + "', '" + data7 + "', '" + data8 + "', '" + data9 + "', '" + data10 + "' )"
        cur.execute(sql)

    return 0


##메인 코드 부분##

if not os.path.exists("C:\\StudyHelper") : #프로그램 로컬 디렉토리 생성
        os.mkdir("C:\\StudyHelper")

con, cur = None, None   #데이터베이스 접속
con = sqlite3.connect("C:\\StudyHelper\\StudyHelper")
cur = con.cursor()



#테이블 존재 여부 확인
if (TableExistCheck() == 0) :

    #없으면 새로 만들기
    MakingTable()

    #사용자 정보 입력
print('사용자 정보를 입력합니다.')
InsertUserData()
InsertSubData()
InsertKeywords()
    #과목 정보 입력(이름, 수업시간, 과목별 키워드 입력까지)
        
    #과목명으로 폴더 생성
MakingFolder()


    
    

#사용자 정보 등록 여부 확인
#cur.execute("SELECT stdid FROM USer")
#if(cur.fetchone()) :
    
    
    





#일정주기마다 아래 루틴 실행하기
#폴더 검사 함수(키워드 검색, 시간검색)
#폴더 이동 실행
#MoveFolder()
