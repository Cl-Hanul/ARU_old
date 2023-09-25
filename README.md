## 소개
`아르(ARU)`는 디스코드 다(多) 기능 봇입니다.

모든 코드는 오픈소스이며, 라이선스만 지킨다면 누구든 사용 가능합니다.

## 사용법
### 1.설치
1. [파이썬(3.10.6)]을 설치합니다.
2.  아르 소스코드 다운 후, `launch_set.py` 실행
3.  [api 리스트]에서 각각 키를 발급 후 `key.json`에 작성
4. `launch.py`를 실행

### 2.초대
[봇 초대 링크]를 통해 손쉽게 추가하세요

## 사용 API 리스트
(체크 == 아르 봇 적용 여부)
<!-- 이거 국가 데이터는 data.go.kr로 옮겨야 될듯 -->
- [X] [Discord Bot API]
- [ ] naver API
- [X] [Twitch API]
- [ ] Korean Dictionary API
- [x] [Neis API]
- [ ] [기상청 API]
- [ ] [국가 법률 API]

## 기능
아르 봇의 기능

### 트위치

| 명령어 | 설명 |
|-|-|
| `/트위치 방송정보` | 트위치 스트리머의 방송 정보를 가져옵니다 |
<br>


### 나이스

| 명령어 | 설명 |
|-|-|
| `/급식 학교설정` | 급식과 관련된 명령어에 이용될 학교 정보입니다 |
| `/급식 정보` | 원하는 날짜의 급식을 불러옵니다 |
| `급식 알림추가` | 원하는 시간에 급식에 대한 알림을 추가합니다 |
<br>


### 아이템

| 명령어 | 설명 |
|-|-|
| `/정보` | 아이템의 정보를 봅니다 |
| `/제작` | 아이템을 제작합니다 |
| `/판매`(예정) | 아이템을 판매하여 `아르 코인`을 획득합니다 |
<br>


### 프로필(예정)

| 명령어 | 설명 |
|-|-|
| `/프로필` | 아르가 지원하는 프로필을 보여줍니다 |
| `/프로필 사진` | 원하는 유저의 프로필 사진을 가져옵니다 |
| `/프로필 뱃지` | 현재까지 획득한 뱃지를 보여줍니다 |
| `/프로필 뱃지설정` | 아르가 지원하는 프로필에 대표로 보여질 뱃지를 설정합니다 |
<br>


### 레벨링(예정)

| 명령어 | 설명 |
|-|-|
| `/출석체크` | 해당 날짜에 출석을 하여 경험치를 획득하며, 연속 출석시 더 줍니다 |
| `/쓰다듬기` | 아르를 쓰다듬어 줍니다. |
<br>


### 유저 알림(예정)

| 명령어 | 설명 |
|-|-|
| `/입장알림` | 유저의 서버 입장을 알려줍니다 |
| `/퇴장알림` | 유저의 서버 퇴장을 알려줍니다 |
| `/생일축하` | 유저의 생일을 축하할 날짜를 설정합니다 |
<br>


### 봇 설정(예정)

| 명령어 | 설명 |
|-|-|
| `/말투 설정` | 아르가 보내는 메세지의 말투를 설정합니다 (반말체, 존댓말체, 겸체) |
<br>


### 기타

| 명령어 | 설명 |
|-|-|
| `/무게` | 아르 봇의 크가를 알려줍니다 |
| `/프사` | 프사를 구해줍니다 |
| `/핑` | 아르 봇의 통신 속도를 측정합니다 |
| `/수면시간` | 일어날 시간에 대해 적절한 수면 시간을 알려줍니다 |
<br>

## 제작 예정
- [x] v0.0 (작동은 하게 만들어 보자..)
- [ ] v1.0 아르 봇 1.0 릴리즈 출시 및 임베드•말투 통합
- [ ] v2.0 아르 봇 다국어 지원 기능
- [ ] v3.0 전면적 아르 봇 기능 최적화 또는 작동 방식 변경

### 기타
현재 버전 : v0.3a
> 색깔
> - 퍼스널 컬러 ![#ffd8ee](https://placehold.co/15x15/ffd8ee/ffd8ee.png)`#ffd8ee` (정상 응답 + 정보)
> - 퍼스널 컬러 ![#ffa4c6](https://placehold.co/15x15/ffa4c6/ffa4c6.png)`#ffa4c6`

> 임베드
> - 빨강 ![#ee6666](https://placehold.co/15x15/ee6666/ee6666.png)`#ee6666` (코드 오류, 치명적인 오류)
> - 파랑 ![#6666ff](https://placehold.co/15x15/6666ff/6666ff.png)`#6666ff` (시스템 정보)
> - 노랑 ![#ffff66](https://placehold.co/15x15/ffff66/ffff66.png)`#ffff66` (경고, 밴, 킥)
> - 초록 ![#66ff66](https://placehold.co/15x15/66ff66/66ff66.png)`#66ff66` (정상 응답)
> - 주황 ![#ffaa66](https://placehold.co/15x15/ffaa66/ffaa66.png)`#ffaa66` (입력 오류)

> 아이템(예정)
> - 흔함
> - 일반
> - 레어
> - 유물
> - 전설
> - 신화
> - 신
> - 아르

## 매우 기타 등등
[개인정보 이용 방침](https://github.com/Cl-Hanul/ARU/blob/main/DOCS/privacy.md)

[파이썬(3.10.6)]: https://www.python.org/downloads/release/python-3106/
[api 리스트]: https://github.com/Cl-Hanul/ARU/blob/main/README.md#%EC%82%AC%EC%9A%A9-api-%EB%A6%AC%EC%8A%A4%ED%8A%B8
[Discord Bot API]: https://discord.com/developers/applications
[Twitch API]: https://dev.twitch.tv/console/apps
[Neis API]: https://open.neis.go.kr/portal/myPage/actKeyPage.do
[기상청 API]: https://apihub.kma.go.kr
[봇 초대 링크]: https://discord.com/api/oauth2/authorize?client_id=1067254933553958953&permissions=8&scope=bot
[국가 법률 API]: https://open.law.go.kr/LSO/openApi/guideList.do
