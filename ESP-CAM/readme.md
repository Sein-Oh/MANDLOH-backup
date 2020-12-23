# 설치 순서
## 1. ESP32 보드 설치(기존 설치 시 생략 가능)
  1. 아두이노 IDE 환경설정에서 추가적인 보드 매니저 URLs 다음 주소 입력  
    https://dl.espressif.com/dl/package_esp32_index.json
  1. 툴 -> 보드 -> 보드매니저 에서 esp32 검색 후 설치 (다소 시간이 걸리는 경우가 있음)
  
## 2. ESP CAM 스케치 업로드
  - 툴 -> 보드 -> "WSP32 Wrover Module" 선택  
  - 툴 -> Upload Speed : "921600" 선택(권장)  
  - 툴 -> Partition Scheme : "Huge App (3MB No OTA/1MB SPIFFS)" 선택 
  - 업로드 모드로 설정 : IO0 핀과 GND 연결
  - 업로드 중 Connecting .... 에서 시간이 오래걸리면 리셋버튼을 눌러볼 

## 3. Websocket 라이브러리 설치
  1. 다음 주소에서 AsyncTCP 설치  
  https://github.com/me-no-dev/AsyncTCP  
  1. 다음 주소에서 ESPAsyncWebserver 설치  
  https://github.com/me-no-dev/ESPAsyncWebServer  
  1. 라이브러리 설치방법 : Github에서 zip 파일로 내려받은 후, 스케치 -> 라이브러리 포함하기 -> .ZIP 라이브러리  
  

## 4. 참고 링크
  1. ESP CAM 사용법  
    https://blog.naver.com/PostView.nhn?blogId=roboholic84&logNo=221601808100&categoryNo=7&parentCategoryNo=0
  2. Websocket 사용법  
    https://shawnhymel.com/1882/how-to-create-a-web-server-with-websockets-using-an-esp32-in-arduino/
