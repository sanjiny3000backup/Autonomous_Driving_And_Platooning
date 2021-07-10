# -*- coding: utf-8 -*-

import numpy as np
import cv2
import warnings
import lane_detection2_b3


class VideoStreaming(object):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)

    def __init__(self, client):
        self.client = client

    def server_program(self, data):
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = str(data + 100)
        self.client.send(data.encode())  # send data to the client

    def streaming(self):
        try:
            print("Streaming...")
            print("Press 'q' to exit")

            # need bytes here
            stream_bytes = b' '
            while True:
                stream_bytes += self.client.recv(1024)
                first = stream_bytes.find(b'\xff\xd8')
                last = stream_bytes.find(b'\xff\xd9')
                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    frame2 = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    cv2.imshow('image', frame)
                    #cv2.imshow("original", frame)

                    ## lane
                    edges = lane_detection2_b3.detect_edges(frame)
                    roi = lane_detection2_b3.region_of_interest(edges)
                    line_segments = lane_detection2_b3.detect_line_segments(roi)
                    lane_lines = lane_detection2_b3.average_slope_intercept(frame, line_segments)
                    lane_lines_image = lane_detection2_b3.display_lines(frame, lane_lines)
                    steering_angle = lane_detection2_b3.get_steering_angle(frame, lane_lines) #pass value through socket
                    #print(steering_angle)
                    self.server_program(steering_angle)
                    heading_image = lane_detection2_b3.display_heading_line(lane_lines_image, steering_angle)
                    cv2.imshow("heading line", heading_image)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
        finally:
            self.client.close()

if __name__ == '__main__':
    VideoStreaming()
