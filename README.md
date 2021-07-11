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
## V2X(VEHICLE TO EVERYTHING) (:page_facing_up:관련논문 : [v2x.pdf](https://github.com/colin9597/Analysis_Of_Credit_Card_Company_Data/files/6796931/v2x.pdf))
차량이 네트워크를 통해 다른 차량 및 인프라가 구축된 사물과 정보를 교환하는 통신기술
![v2x](https://user-images.githubusercontent.com/80561963/125195654-9140a400-e291-11eb-94f6-ed11d23f3313.JPG)  
- V2N(Vehicle to Network) : 교통상황을 제공받아 네트워크가 차량을 판단 및 주행제어
- V2V(Vehicle to Vehicle) : 차량간 통신 제어, 군집주행
- V2I(Vehicle to Infrastructure) : 차량과 인프라 간 통신, 신호체계 제어