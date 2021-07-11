:car:    :blue_car:
# <Autonomous_Driving_And_Platooning>
[POSCO_AC_Project] 네트워크 기반 V2X 자율주행 및 군집주행

---
## 개발 환경
- Ubuntu 18.04
- Cuda 10.2
- Cudnn 8.0.2
- OpenCV 4.5.1  
---
## 구성도
![시스템 설계](https://user-images.githubusercontent.com/80561963/125196645-9a337480-e295-11eb-9545-7b319aa85d12.png)
---
## 활용기술
- V2X(VEHICLE TO EVERYTHING)
차량이 네트워크를 통해 다른 차량 및 인프라가 구축된 사물과 정보를 교환하는 통신기술
![v2x](https://user-images.githubusercontent.com/80561963/125195654-9140a400-e291-11eb-94f6-ed11d23f3313.JPG)  
> V2N(Vehicle to Network) : 교통상황을 제공받아 네트워크가 차량을 판단 및 주행제어
> V2V(Vehicle to Vehicle) : 차량간 통신 제어, 군집주행
> V2I(Vehicle to Infrastructure) : 차량과 인프라 간 통신, 신호체계 제어  
(:page_facing_up:관련논문 : [v2x.pdf](https://github.com/colin9597/Analysis_Of_Credit_Card_Company_Data/files/6796931/v2x.pdf))

- Lane Detection
> 계산된 Angle 값을 서버로부터 받아옴.
> 파이카메라로부터 영상을 받을 때부터 gray scale을 적용하여 라즈베리파이에서 속도를 높임.  
![lane detection](https://user-images.githubusercontent.com/80561963/125197201-ae787100-e297-11eb-81b5-33df325caaeb.jpg)

- YOLO
> Master Car에 표지판 클래스 총 6개를 훈련시킴.
> Slave Car에 표지판과 Master Car 뒷모습을 훈련시킴.
> 각 클래스 당 600 ~ 1000장을 훈련시킴.
![YOLOv4](https://user-images.githubusercontent.com/80561963/125197223-be905080-e297-11eb-845f-4e09574ea629.png)


- MobileNet
> MobileNet은 컴퓨터 성능이 제한되거나 배터리 퍼포먼스가 중요한 곳에서 사용될 목적으로 설계뙨 CNN 구조
> Server와 Yolo V4 모델을 연동하려고 하였으나 개발환경에서 GPU가 백엔드로 올라가지 않아 어려움을 겪음
> => Yolo V4 대신 MobileNet 모델을 사용함으로써 CPU 기반으로 잘 작동.
![mobilenet](https://user-images.githubusercontent.com/80561963/125197273-e7b0e100-e297-11eb-90f5-393db36ca22d.png)  

- TCP/IP & Bluetooth Socekt
> 라즈베리파이 연산 능력을 초과하는 YOLO와 주행 영상은 TCP 통신으로 Work Station에서 처리
> 간단한 주행 신호는 BL Socket 통신으로 처리
---
