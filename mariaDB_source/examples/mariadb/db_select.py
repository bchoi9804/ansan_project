ㅠ# mysql-connector 테스트: mysql DB의 temperature 테이블의 데이터를 select문을 통해 읽어 오는 실습
import pymysql    # pymysql 임포트

# 전역변수 선언부 
db = None 
cur = None 

# 접속정보
db = pymysql.connect(host='20.196.223.154', user='root', password='1234', db='mysql', charset='utf8')

try:
  cur = db.cursor() # 커서생성 
  sql = "SELECT DATATIME, TEMP FROM temperature" 

  # 실행할 sql문 
  cur.execute(sql)
  
  result = cur.fetchall()
  for row in result:
    print(row[0], '|', row[1])

  # 커서로 sql문 실행
  # db.commit() # 저장 
finally:
  db.close() # 종료
