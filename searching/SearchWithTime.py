#생성 시간 읽어오기까지 구현. 검색은 미구현
import os.path, time

file = "C:\\osproject202201\\22-1-os-basic-project-TMJHJ-\\searching\\searching.txt"

print(os.path.getmtime(file)) #파일 생성 시간 데이터 확인
print(time.ctime(os.path.getmtime(file))) #생성 시간 데이터를 str형으로 변환하여 '요일, 월, 일, 시간, 연도'순으로 출력

print(type(time.ctime(os.path.getmtime(file)))) #str형인 것을 확
