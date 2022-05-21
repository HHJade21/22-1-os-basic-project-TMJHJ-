#데이터베이스에서 과목 이름을 가져와 폴더를 생성해주는 기능을 만들기 위한 테스트 코드
#데이터베이스 접속, 특정 데이터 가져오기, 가져온 데이터로 폴더 생성하기

#os모듈로 mkdir함수를 사용하고, sqlite3로 데이터베이스에 접속합니다.(이 코드에서는 이미 생성된 데이터베이스에 접속만 합니다.) 
import os
import sqlite3

#데이터베이스 naverDB에 접속합니다.
con = sqlite3.connect("C:/Users/user/AppData/Local/Programs/Python/Python37/naverDB")
#데이터베이스 접속 커서를 생성합니다.
cur = con.cursor()
#커서를 이용해 데이터베이스에 접속합니다. 이때 username만 가져올 것이므로 'select * from ~'이 아니라 'select username from ~'을 사용합니다.
cur.execute("SELECT userName FROM naverDB")

#커서에서 첫 번째 데이터를 가져와 폴더 이름 변수에 저장합니다.
foldername = cur.fetchone()

#제대로 저장되었나 확인
print(foldername)

#저장된 폴더명으로 폴더 생성
os.mkdir("C:\\Users\\user\\Desktop\\%s" % foldername)


con.commit()
con.close()
