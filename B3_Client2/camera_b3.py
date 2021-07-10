# -*- coding: utf-8 -*-

import io
import struct
import time
import picamera

class Camera(object):
    def __init__(self, server):
        self.server = server.makefile('wb')

    def run(self):
        with picamera.PiCamera() as camera :
            camera.resolution = (320, 240)
            camera.color_effects = (128, 128)
            camera.framerate = 20

            camera.start_preview()
            time.sleep(0.1)

            start = time.time()
            stream = io.BytesIO()
            for foo in camera.capture_continuous(stream, 'jpeg', use_video_port = True):
                self.server.write(struct.pack('<L', stream.tell())) # Unsigned Long, current stream position
                self.server.flush() # socket 버퍼 비우기
                stream.seek(0) # stream 내 위치 설정
                self.server.write(stream.read())
                if time.time() - start > 600 : # 시간이 너무 오래걸리면 반복문 종료
                    break
                stream.seek(0)
                stream.truncate() # stream 현재 위치로 크기를 조정
        self.server.write(struct.pack('<L', 0))
        # struct.pack(format, v1, v2, ...) v1, v2, … 값을 포함하고 format에 따라 패킹된 바이트 열객체를 반환






