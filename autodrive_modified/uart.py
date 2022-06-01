import serial

def uart(data):

    ser = serial.Serial(port = '/dev/ttyAMA1',
                        baudrate = 9600,
                        timeout = 1)

    ser.write(data.encode('utf-8'))
