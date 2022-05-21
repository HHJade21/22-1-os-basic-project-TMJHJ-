##데이터베이스 생성 코드
import sqlite3

con, cur = None, None
##괄호 안에 적힌 주소에 해당 데이터베이스가 있으면 접속. 없으면 생성 후 접속
con = sqlite3.connect("C:/osproject202201/22-1-os-basic-project-TMJHJ-/StudyHelper")
cur = con.cursor()

#사용자 정보 테이블과 과목정보 테이블을 각각 생성
cur.execute("CREATE TABLE IF NOT EXISTS User(stdid int, userName char(15), grade int, semester int, year int)")
cur.execute("CREATE TABLE IF NOT EXISTS Subject(Subname char(15), Professor char(15), Firsttime char(5), Secondtime char(5))")



    
con.commit()
con.close()

