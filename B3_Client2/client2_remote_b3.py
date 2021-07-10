# -*- coding: utf-8 -*-

import socket
import camera_b3
import threading
import connect_b3
import time
import RPi.GPIO as GPIO

def client_program():
    # IP 클라이언트2
    HOST = '141.223.140.21'
    PORT = 10251
    main_socket = connect_b3.Connect(HOST, PORT)

    # Master<->Slave 블루투스 서버
    hostMACAddress = 'DC:A6:32:F1:6E:A6' # 포틀리 서버 주소
    port = 5
    bt_socket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    bt_socket.bind((hostMACAddress, port))
    bt_socket.listen(1)
    bt_client, bt_address = bt_socket.accept()

    time.sleep(0.01)

    camera = camera_b3.Camera(main_socket.Get_Socket())
    camera_thread = threading.Thread(target=camera.run, args=())
    camera_thread.start()

    i = 0
    left = 0
    right = 0

    while True:
        # 블루투스 서버 연결
        accel = bt_client.recv(64)
        accel = accel.decode()
        # print(accel) # up, down, keep

        #time.sleep(0.1)
        data = main_socket.Get_Data()  # receive response
        #print('Received from server: ' + data)  # show in terminal
        if i == 0:
            time.sleep(6)
        i += 1

        steering_angle = int(data)

        # speed = 20
        # lastTime = 0
        # lastError = 0
        #
        # now = time.time()
        # dt = now - lastTime
        #
        # kp = 0.4
        # kd = kp * 0.65

        deviation = steering_angle - 190
        #print(deviation)
        # error = abs(deviation)

        if deviation < 11 and deviation > -11:
            deviation = 0
            error = 0
            GPIO.output(in3, GPIO.LOW)
            GPIO.output(in4, GPIO.LOW)
            steering.stop()
            time.sleep(0.05)

            if accel == 'up':
                throttle.start(25)
                time.sleep(1)
                throttle.start(20)
            elif accel == 'down':
                throttle.start(15)
                time.sleep(1)
                throttle.start(20)
            else:
                throttle.start(20)

            if i % 10 == 0:
                steering.ChangeDutyCycle(70) # Hit를 70 만큼 침
                GPIO.output(in3, GPIO.HIGH)
                time.sleep(0.07)
                GPIO.output(in3, GPIO.LOW)
                steering.ChangeDutyCycle(60) # 다시 기본으로
                print('HIT')


        elif deviation > 11:
            right += 1  ## 수정
            GPIO.output(in3, GPIO.HIGH)
            GPIO.output(in4, GPIO.LOW)
            #time.sleep(1)
            #GPIO.output(in3, GPIO.LOW)
            #GPIO.output(in4, GPIO.HIGH)
            steering.start(60)
            throttle.start(20)
            #time.sleep(2)
            ## 수정
            #if right % 8 == 0:
            #    for i in range(4):
            #        time.sleep(0.01)
            #        GPIO.output(in3, GPIO.LOW)
            #        GPIO.output(in4, GPIO.HIGH)
            #        steering.start(40)


        elif deviation < -11:
            left += 1 ## 수정
            GPIO.output(in3, GPIO.LOW)
            GPIO.output(in4, GPIO.HIGH)
            #time.sleep(1)
            #GPIO.output(in3, GPIO.HIGH)
            #GPIO.output(in4, GPIO.LOW)
            steering.start(60)
            throttle.start(20)
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
        throttle.start(20)  # 수정

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

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(in1, GPIO.OUT)
    GPIO.setup(in2, GPIO.OUT)
    GPIO.setup(in3, GPIO.OUT)
    GPIO.setup(in4, GPIO.OUT)

    GPIO.setup(throttlePin, GPIO.OUT)
    GPIO.setup(steeringPin, GPIO.OUT)

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
