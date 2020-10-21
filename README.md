# 11-BeerBnB-backend

> 숙박 공유 서비스 에어비앤비 클론 프로젝트
> ![schema](https://user-images.githubusercontent.com/54208214/93005168-71652480-f589-11ea-9b5c-3a3645df2628.png)

## Table of contents

- [General info](#general-info)
- [Demo](#demo)
- [Technologies](#technologies)
- [Features](#features)
- [Contact](#contact)

## General info

- 숙박 공유 서비스 에어비앤비 클론 프로젝트
- 개발기간 : 2020.08.31 ~ 2020.09.11
- 팀원 : Front-end(황연욱, 이조은, 최예흠) Back-end(김해준, 고지원)
- [Front-end Github](https://github.com/wecode-bootcamp-korea/11-BeerBnB-frontend)
- [Back-end Github](https://github.com/wecode-bootcamp-korea/11-BeerBnB-backend)

## Demo

- [WebSite](http://13.58.71.103)
- [Youtube](https://youtu.be/qarYlUGYmAc)

## Technologies

### Tools

- Git(Control Commit history by Squash and Rebase)
- [Trello](https://trello.com/b/LtTyYYHK/beer-bnb)
- AWS
- Docker
- PostMan(Share API documentation)
(https://kibon1.postman.co/collections/12272060-a0c065a6-fe78-4884-93ff-1f5943650f4a?version=latest&workspace=98d1890f-e298-45cd-9e3e-ad983c00a976)
- Aquery

### Front-End

- JavaScript(+ ES6 syntax)
- React.js(setting with CRA)
- Styled-Component
- react-router-dom
- Redux
- Google Social Login
- react-google-maps
- react-dates

### Back-End

- Python
- Django Web Framework
- CORS headers
- Selenium
- MySQL
- Bcrypt, JWT
- Google Social Login
- RESTful API
- AWS RDS 연동 후 Docker container를 EC2 Server를 통한 배포
- 각 엔드포인트 Unit Test 구현

## Features

### 회원가입 / 로그인 페이지

- 모달창의 요소 모두 컴포넌트화 이후 재활용
- Fetch()의 GET, POST 방식을 통해 서버와의 통신
- 이메일 로그인 및 회원가입 구글 로그인 및 회원가입 모달 창 구현
- 로그인 및 회원가입 유효성 검사 및 그에 맞는 경고창 구현
- Redux 통해 로그인 후 상태 관리
- Oauth2.0로 Google API 호출 소셜 로그인 구현

### 메인 페이지

- grid를 통해 레이아웃
- Map 함수를 통해 불필요한 중복 제거
- AirBnB/react-dates 를 이용한 체크인, 체크아웃 날짜 선택 기능
- Redux를 통한 체크인 - 체크아웃 날짜 연동 기능(Nav bar의 달력 및 상세페이지에 존재하는 2개의 달력 총 3개의 달력 연동)

### 숙소 리스트 페이지

- Redux를 통한 체크인 - 체크아웃 날짜 연동 기능을 통해 리스트 상단 여행 일정을 알맞게 보여주는 기능
- 상단 필터 옵션 각각 모달창 생성 및 Redux를 통해 State관리하여 알맞게 리스트가 필터링 되는 기능
- 각 숙소 정보들의 이미지들에게 setTimeout과 transition을 State로 관리하는 것을 통한 Infinity Image Slider 기능
- Custom Hook을 통해 Redux 에서 State를 관리하는 로직과 실제 UI부분의 분리
- async, await를 통해 리스트를 fetch함수로 받아오는 시간동안 로딩중 애니메이션 구현
- 페이지에 알맞게 offset 값을 부여해 숙소 데이터를 받아오는 Pagination 기능
- react-google-maps 를 이용해 각 숙소별 위도 경도를 넣어 지도상에 가격표를 알맞은 위치에 띄워서 보여주는 기능
- 숙소리스트의 각 숙소 마우스 hover시 지도에서 hover 된 숙소의 가격표만 스타일이 바뀌어 보여주는 기능
- 지도상의 각 숙소마다 가격표 클릭시 숙소정보 모달창으로 띄워지는 기능
- 지도 왼쪽 상단의 close 버튼 클릭시 지도가 사라지고 숙소 리스트의 스타일과 레이아웃이 바뀌는 기능
- 페이지 크기가 일정이상 줄어들면 지도가 없어지고 리스트만 남는 반응형 웹 기능

### 숙소 상세 페이지

- Url 정보를 이용한 동적 라우팅
- 침대, 침구 유형이 4개 이상일 경우 슬라이더 형태로 레이아웃 변경되는 기능
- 리뷰의 평균 점수 Progress bar로 표현
- AirBnB/react-dates 를 이용한 체크인, 체크아웃 날짜 선택 기능
- Redux를 통한 체크인 - 체크아웃 날짜 연동 기능(Nav bar의 달력 및 상세페이지에 존재하는 2개의 달력 총 3개의 달력 연동)
- Custom Hook을 통해 Redux 에서 State를 관리하는 로직과 실제 UI부분의 분리
- 리뷰 모두보기 모달 창 구현 및 Observation API & Query String을 통한 Infinity Scroll 기능

## Contact

### Front-end

- 황연욱
  - [Github](https://github.com/younuk23)
  - [Blog](https://velog.io/@younuk23)
- 이조은
  - [Github](https://github.com/jjo-niixx)
  - [Blog](https://velog.io/@jjo-niixx)
- 최예흠
  - [Github](https://github.com/cyheum)
  - [Blog](https://velog.io/@cyheum)

### Back-end

- 김해준
  - [Github](https://github.com/hj8853)
  - [Blog](https://velog.io/@hj8853)
- 고지원
  - [Github](https://github.com/Gxone)
  - [Blog](https://gxone.github.io)
