# iot 과제 제출을 위한 레포

- 백엔드 프레임워크
    - Django
- 프론트
    - Bootstrap

- 그 외
    - mqtt broker

- 배포 과정
    - 좀 생각해보게ㅐㅆ습ㅈㄴ

## firt step

- 새로운 파이썬 가상환경 생성
    - `virtualenv venv --python=python3`
    - venv라는 이름의 가상환경 생성
    - `python3 -m pip freeze > requirements.txt` 이용하여
    - 이 프로젝트에 필요한 requriment 를 뽑아낸다.
    
## 작업 중 문제 발생
- Django에서 정상적인 방법으로 mqtt client를 구현하는건 쉽지 않다.
- Channel이라는 asgi 프로토콜? 이용 방법이 있다고하는데 오늘 제출이라 일단 포기

### 작업 방법

- django 개발 서버가 뜰 때, flask-socketio 서버를 multiprocess로 fork한다.
- 이놈은 9999번 포트 쓸 것임.
- 웹 프론트 페이지에서  localhost:9999번과 socketio 사용해서 실시간 데이터 출력 할 예정 (아주 원시적인...)
- 참 어렵다

### 아두이노는 다음과 같이 데이터를 5초 주기로 올린다.

```json
{
    "temp" : 24.5,
    "humid" : 42,
    "light" : 123
}
```

- ardu.py는 다음과 같은 역할을 수행한다.
    - mqtt client와 커넥션 맺는다.
    - 받은 데이터를 MySQL에 꽂아준다.
    - 동시에 class 내 buffer에 해당 데이터를 갖고있는다

- socketio 요청이 들어오면 ardu.py 안의 클래스에 있는 buffer의 값을 읽어 웹으로 보내준다.