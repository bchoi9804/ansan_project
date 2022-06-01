import time,board,busio
import numpy as np
import adafruit_mlx90640
import pymysql

def mlx_cam():
    i2c = busio.I2C(board.SCL, board.SDA, frequency=400000) # setup I2C
    mlx = adafruit_mlx90640.MLX90640(i2c) # begin MLX90640 with I2C comm
    mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ # set refresh rate

    frame = np.zeros((24*32,)) # setup array for storing all 768 temperatures
    while True:
        try:
            mlx.getFrame(frame) # read MLX temperatures into frame var
            # print out the average temperature from the MLX90640
            print('Max MLX90640 Temperature: {0:2.1f}C'.\
                format(np.max(frame)))
            # print out the average temperature from the MLX90640
            print('Average MLX90640 Temperature: {0:2.1f}C'.\
                format(np.mean(frame)))
            return frame

        except ValueError:
            continue # if error, just read again

# 전역변수 선언부 
db = None 
cur = None 

# 접속정보
db = pymysql.connect(host='20.200.220.207', user='azureuser', password='1234', db='DCTDB', charset='utf8')  

try:
    cur = db.cursor() # 커서생성 
    
    while True:
        frame = mlx_cam()
        max_temp = np.max(frame)
        avg_temp = np.mean(frame)
            
        sql = "INSERT INTO thermal_camera(MAX, AVG) VALUES (%2.1f, %2.1f)" % (max_temp, avg_temp)
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