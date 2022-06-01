import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import uart
import img_preprocess

def main():
    camera = img_preprocess.open()

    model_path = '/home/pi/AI_CAR/model/lane_navigation_final.h5'
    model = load_model(model_path)

    carState = "stop"

    try:
        while True:
            keyValue = cv2.waitKey(10)
        
            if keyValue == ord('q') :
                break
            elif keyValue == 82 :
                print("go")
                carState = "go"
            elif keyValue == 84 :
                print("stop")
                carState = "stop"
        
        image = img_preprocess.read(camera)
        pre = img_preprocess.preprocessing(image)
        cv2.imshow('pre', pre)

        x = np.asarray([pre])
        steering_angle = int(model.predict(x)[0])
        #print('predict angle: ', steering_angle)

        if carState == "go":
            if steering_angle >= 75 and steering_angle <= 105:
                    uart.uart('g')    
            elif steering_angle > 105:
                    uart.uart('r')
            elif steering_angle < 75:
                    uart.uart('l')
        elif carState == "stop":
            uart.uart('s')
            
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
    cv2.destroyAllWindows()

