import io
import socket
import struct
from PIL import Image
import matplotlib.pyplot as pl

server_socket = socket.socket() # 소켓 생성
server_socket.bind(('192.168.0.44', 8000))  # ADD IP HERE # 소켓에 주소를 결합하다
server_socket.listen(0) # 클라이언트 연결 요청 수신을 듣다 -> 연결 요청을 확인하며 대기
# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb') # 실질적인 데이터 송수신이 이루어진다. 연결 요청을 수락하고 파일을 읽는다
try:
    img = None
    while True:
        # Read the length of the image as a 32-bit unsigned int. If the
        # length is zero, quit the loop
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break
        # Construct a stream to hold the image data and read the image
        # data from the connection
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        # Rewind the stream, open it as an image with PIL and do some
        # processing on it
        image_stream.seek(0)
        image = Image.open(image_stream)
        
        if img is None:
            img = pl.imshow(image)
        else:
            img.set_data(image)

        pl.pause(0.01)
        pl.draw()

        print('Image is %dx%d' % image.size)
        image.verify()
        print('Image is verified')
finally:
    connection.close() # accept API 호출에 의해 생성된 소켓
    server_socket.close() # 최초 생성한 서버 소켓