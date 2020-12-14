# 무선네트워크 프로젝트
5조 - 무럭무럭
# 팀원
김석진, 강성훈, 김수진, 정수현

# 프로젝트 정보
## 개요
＃주제 선정 이유
        
＃개발목표

＃개발방법


## 서비스
  
  a. 토양 수분 부족 시점 알림 서비스
  
        1. 토양의 수분량 측정 : 라즈베리파이와 토양 수분 센서를 이용
        
        2. 토양의 수분량과 수분 부족 임계치를 비교하여 토양에 수분이 필요한 시점을 텔레그램을 통해 알려줌 
        
        3. 수분량이 임계치 이상에 도달했을 경우 텔레그램 메시지 중단
  
  b. 식물 생장용 LED 예약 서비스 
        
        1. LED 실제 작동 부분 설계 :  Hue API 활용 
        
        2. LED 제어 : 라즈베리파이와 Hue 브릿지와의 연결과 Hue 브릿지와 LED와의 Zigbee 통신 이용
   
   ![제어](https://user-images.githubusercontent.com/71261685/102054760-35ae5500-3e2d-11eb-8336-d41d3c5b42a9.png)
        
        3. LED 예약 및 설정 : 텔레그램 메시지를 통해 LED on/off 시간 예약 및 빛/색 조절 가능

        4. LED 예약 및 설정 상태 확인 : 같은 네트워크 상에서 작동되는 Hue 어플 이용
        
        # 개발 가이드 
	       1) 네트워크 환경 조성 : 
   		무선 공유기(Wi-Fi라우터)에 연결되어야 할 항목
                  - 필립스 hue 전용 브릿지 (랜선 사용)
                  - 라즈베리파이 (랜선 사용)
                  - 핸드폰 필립스 hue 어플 (Wi-Fi 연결)
	       2) 필립스 hue 어플을 통해 Bridge IP 확인
	       3) python phue 모듈 설치 
		$ sudo pip3 install phue
		$ git clone https://github.com/studioimaginaire/phue.git
	
	
	+ 식물 생장용 LED : 빛의 파장에 따른 식물의 생리 반응
   
   ![생장11](https://user-images.githubusercontent.com/71261685/102054935-76a66980-3e2d-11eb-81cf-ae814975cc77.png)
   
   ![파장](https://user-images.githubusercontent.com/71261685/102054927-7312e280-3e2d-11eb-9e35-1e6f11158f43.png)
     
    ▶ 식물 광합성 도움 : 400nm~500nm 파장의 빛 -> 450nm 청색 빛 
    ▶ 식물 생장 도움 : 640nm~700nm 파장의 빛 -> 660nm 적색 빛
   
  c. 텔레그램 서비스 
# 프로젝트 결과

  a. 토양 수분 부족 시점 알림 서비스
  
  b. 식물 생장용 LED 예약 서비스
  
  ＊ 프로젝트 전체 설계 모습 *
  
   ![최종화면수정](https://user-images.githubusercontent.com/71261685/102105267-8dbb7a80-3e72-11eb-85dd-c9f65099e1ec.jpg)
# 참고 사이트   
  
  + 토양 관련 참고
  
  + LED 관련 참고
  
     https://github.com/studioimaginaire/phue

     https://mitny.github.io/articles/2018-11/PhilipsHue-control

     http://www.bissolled.com/page.php?menu=0102  
  + 텔레그램 관련 참고
