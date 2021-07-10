# -*- coding: utf-8 -*-

import socket
import camera_b3
import threading
import connect_b3
import time
import RPi.GPIO as GPIO

def client_program():
    HOST = '141.223.140.21'
    # HOST = '172.20.10.7'
    PORT = 10250
    main_socket = connect_b3.Connect(HOST, PORT)
    time.sleep(0.01)

    #############################################
    # Master <-> Slave 블루투스 클라이언트
    hostMACAddress = 'DC:A6:32:F1:6E:A6' # 포틀리 서버 주소
    port = 5
    bt_socket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    bt_socket.connect((hostMACAddress, port))

    # depth 카메라 블루투스 서버
    hostMACAddress2 = 'DC:A6:32:BD:83:6E' # depth 카메라 서버 주소
    port2 = 1
    bt_socket2 = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    bt_socket2.bind((hostMACAddress2, port2))
    bt_socket2.listen(1)
    bt_client2, bt_address2 = bt_socket2.accept()

    # 신호등 서버
    # hostMACAddress3 =  # 신호등 서버 MAC Address
    # port3 = # port 번호
    # bt_socket3 = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    # bt_socket3.bind((hostMACAddress3, port3))
    # bt_socket3.listen(1)
    # bt_client3, bt_address3 = bt_socket3.accept()
    #############################################

    camera = camera_b3.Camera(main_socket.Get_Socket())
    camera_thread = threading.Thread(target=camera.run, args=())
    camera_thread.start()

    i = 0
    left = 0
    right = 0
    traffic = 0
    while True:
        ###################################################
        #신호등 서버 연결
        # traffic = bt_client3.recv(1)
        # traffic = int(traffic.decode())
        #
        # while traffic == 1:
        #     GPIO.output(in1, GPIO.LOW)
        #     GPIO.output(in2, GPIO.LOW)
        #     traffic = bt_client3.recv(1)
        #     traffic = int(traffic.decode())
        #     if traffic == 0:
        #         break

        # 블루투스 서버 연결
        dist = bt_client2.recv(64) # 거리 정보
        dist = float(dist.decode())
        if dist > 2:
            bt_socket.send('up'.encode()) # slave로 전송
        elif dist < 1:
            bt_socket.send('down'.encode())
        else :
            bt_socket.send('keep'.encode())
        #####################################################

        # 포미니 주행
        #time.sleep(0.1)
        data = main_socket.Get_Data()  # receive response
        print('Received from server: ' + data)  # show in terminal
        if i == 0:
            # left, right light
            GPIO.output(in5, GPIO.LOW)
            GPIO.output(in6, GPIO.HIGH)
            GPIO.output(in7, GPIO.HIGH)
            GPIO.output(in8, GPIO.LOW)
            time.sleep(6)
            GPIO.output(in5, GPIO.LOW)
            GPIO.output(in6, GPIO.LOW)
            GPIO.output(in7, GPIO.LOW)
            GPIO.output(in8, GPIO.LOW)
        i += 1

        steering_angle = int(data)

        # speed = 20
        # lastTime = 0
        # lastError = 0

        # now = time.time()
        # dt = now - lastTime
        #
        # kp = 0.4
        # kd = kp * 0.65

        deviation = steering_angle - 190
        print(deviation)
        # error = abs(deviation)

        if deviation < 11 and deviation > -11:
            deviation = 0
            error = 0
            GPIO.output(in3, GPIO.LOW)
            GPIO.output(in4, GPIO.LOW)
            steering.stop()
            time.sleep(0.05)
            if i % 10 == 0:
                steering.ChangeDutyCycle(35)
                GPIO.output(in3, GPIO.HIGH)
                time.sleep(0.07)
                GPIO.output(in3, GPIO.LOW)
                steering.ChangeDutyCycle(30)
                print('HIT')

        # right
        elif deviation > 11:
            GPIO.output(in3, GPIO.HIGH)
            GPIO.output(in4, GPIO.LOW)
            steering.start(40)
            throttle.start(25)
            if deviation > 30:
                right += 1
                if right >= 3:
                    GPIO.output(in5, GPIO.LOW)
                    GPIO.output(in6, GPIO.HIGH)
                    time.sleep(1)
                    GPIO.output(in5, GPIO.LOW)
                    GPIO.output(in6, GPIO.LOW)
                    right = 0

            #time.sleep(1)
            #GPIO.output(in3, GPIO.LOW)
            #GPIO.output(in4, GPIO.HIGH)
            #time.sleep(2)
            ## 수정
            #if right % 8 == 0:
            #    for i in range(4):
            #        time.sleep(0.01)
            #        GPIO.output(in3, GPIO.LOW)
            #        GPIO.output(in4, GPIO.HIGH)
            #        steering.start(40)

        # left
        elif deviation < -11:
            GPIO.output(in3, GPIO.LOW)
            GPIO.output(in4, GPIO.HIGH)
            steering.start(40)
            throttle.start(25)
            if deviation < -30:
                left += 1
                if left >= 3:
                    GPIO.output(in7, GPIO.HIGH)
                    GPIO.output(in8, GPIO.LOW)
                    time.sleep(1)
                    GPIO.output(in7, GPIO.LOW)
                    GPIO.output(in8, GPIO.LOW)
                    left = 0

            #time.sleep(2)
            ## 수정
            #if left % 8 == 0:
            #    for i in range(4):
            #        time.sleep(0.01)
            #        GPIO.output(in3, GPIO.HIGH)
            #        GPIO.output(in4, GPIO.LOW)
            #        steering.start(40)


        # derivative = kd * (error - lastError) / dt
        # proportional = kp * error
        # PD = int(speed + derivative + proportional)
        # spd = abs(PD)
        # print(spd)

        # if spd > 35:
        #    spd = 35

        # throttle.start(spd)
        throttle.start(30)  # 수정

        # lastError = error
        # lastTime = time.time()

    cli_soc.close()  # close the connection

if __name__ == '__main__':
    print('start')
    GPIO.setwarnings(False)

    # throttle
    throttlePin = 25  # Physical pin 22
    in1 = 24
    in2 = 23

    # Steering of front wheels
    steeringPin = 12
    in3 = 7
    in4 = 8

    # light
    leftlightPin = 10
    in5 = 9
    in6 = 11

    rightlightPin = 5
    in7 = 6
    in8 = 13

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(in1, GPIO.OUT)
    GPIO.setup(in2, GPIO.OUT)
    GPIO.setup(in3, GPIO.OUT)
    GPIO.setup(in4, GPIO.OUT)
    GPIO.setup(in5, GPIO.OUT)
    GPIO.setup(in6, GPIO.OUT)
    GPIO.setup(in7, GPIO.OUT)
    GPIO.setup(in8, GPIO.OUT)

    GPIO.setup(throttlePin, GPIO.OUT)
    GPIO.setup(steeringPin, GPIO.OUT)
    GPIO.setup(leftlightPin, GPIO.OUT)
    GPIO.setup(rightlightPin, GPIO.OUT)

    # light
    leftlight = GPIO.PWM(leftlightPin, 0.5)
    leftlight.start(50)

    rightlight = GPIO.PWM(rightlightPin, 0.5)
    rightlight.start(50)

    # Steering
    # in3 = 0 and in4 = 1 -> Left
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)
    steering = GPIO.PWM(steeringPin, 30)
    steering.stop()

    # Throttle
    # in1 = 1 and in2 = 0 -> Forward
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    throttle = GPIO.PWM(throttlePin, 30)
    throttle.start(20)  # 수정
    # GPIO.output(in1, GPIO.LOW) #수정
    # time.sleep(5)
    throttle.stop()

    client_program()

    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)
    throttle.stop()
    steering.stop()
