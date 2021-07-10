# -*- coding: utf-8 -*-
import server_socket_b3
import server_video_b3
import threading


if __name__ == '__main__':
    # host, port
    host, port= '141.223.140.21', 10250 #client1 포트  # ipconfig를 통해 ip확인 가능, 우리 13기 파이팅 ^~^
    print("서버 시작")

    client = server_socket_b3.Server(host, port)

    # loop
    video_object = server_video_b3.VideoStreaming(client.Get_Client())
    video_object.streaming()