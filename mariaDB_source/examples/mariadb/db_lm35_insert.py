import time
import Adafruit_DHT    # 온습도 센서 라이브러리 임포트
import pymysql    # pymysql 임포트

def Temp_read(pin):     # 온도 읽고 반환하는 함수
    t = Adafruit_DHT.read_retry(sensor, pin)
    if (t is not None):
        return t

# 전역변수 선언부 
db = None 
cur = None 
sensor = Adafruit_DHT.DHT11  #온습도 센서 지정

# 접속정보
db = pymysql.connect(host='192.168.1.235', user='root', password='pi', db='mysql', charset='utf8')  

try:
  cur = db.cursor() # 커서생성 
  
  while True:
    temp = Temp_read(4)
    print ("%2.1f°C" % temp)  # 입력할 온도값 출력
	
    sql = "INSERT INTO temperature(TEMP) VALUES (%4.1f)" %  temp
    print(sql)

    # 실행할 sql문 
    cur.execute(sql)
	
    # 커서로 sql문 실행
    db.commit() # 저장 
	
    time.sleep(10)
except KeyboardInterrupt:
  pass	
finally:
  db.close() # 종료