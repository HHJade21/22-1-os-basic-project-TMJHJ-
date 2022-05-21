#데이터베이스에서 데이터를 가져와 출력

import sqlite3

con, cur = None, None
##괄호 안에 적힌 주소에 해당 데이터베이스가 있으면 접속. 없으면 생성 후 접속
con = sqlite3.connect("C:/osproject202201/22-1-os-basic-project-TMJHJ-/StudyHelper")
cur = con.cursor()

#어떤 테이블에서 어떤 데이터를 가져올 지 선택
cur.execute("SELECT * FROM User")



while(True):
    #루프마다 새 행을 가져와서 row 배열에 저장
    row = cur.fetchone()

    #공백 행이  나타나면 탈출
    if row == None :
        break;
    #열을 이동하며 데이터 가져옴
    data1 = row[0]
    data2 = row[1]
    data3 = row[2]
    data4 = row[3]
    data5 = row[4]
    #읽어온 행 데이터를 한번에 출력
    print("%d %s %d %d %d" % (data1, data2, data3, data4, data5))

    
con.commit()
con.close()
