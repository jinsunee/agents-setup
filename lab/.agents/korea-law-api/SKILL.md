---
name: korea-law-api
description: 국가법령정보 공유 서비스 Open API를 사용하여 법령, 행정규칙, 자치법규, 조약, 법령해석례, 헌재결정례 등 다양한 법률 정보를 조회. 법령 검색, 법률 정보 확인, 법적 근거 조사, 관련 법규 찾기 등의 작업 시 사용.
---

# 국가법령정보 Open API

법제처에서 제공하는 국가법령정보 공유 서비스 API로, 현행 법령부터 행정규칙, 자치법규, 조약 등 다양한 법률 정보를 XML 형식으로 조회.

## 기본 정보

- **기본 URL**: `http://apis.data.go.kr/1170000/law/`
- **인증**: 공공데이터포털 발급 `ServiceKey` 필수
- **통신 방식**: REST (GET)
- **응답 형식**: XML
- **데이터 갱신**: 일 1회

## 서비스 대상 (target)

| target | 서비스명 | 검색 필드 |
|--------|----------|-----------|
| `law` | 법령정보 | lawNm (법령명) |
| `admrul` | 행정규칙정보 | admRulNm (행정규칙명) |
| `ordin` | 자치법규정보 | ordinNm (자치법규명) |
| `trty` | 조약정보 | trtyNm (조약명) |
| `expc` | 법령해석례정보 | itmNm (해석례명) |
| `detc` | 헌재결정례정보 | evtNm (사건명) |
| `licbyl` | 별표서식정보 | bylNm (별표명) |
| `lstrm` | 법령용어정보 | tn_lstrm_list |

## 요청 파라미터

| 파라미터 | 필수 | 설명 |
|----------|------|------|
| `serviceKey` | O | 공공데이터포털 발급 인증키 |
| `target` | O | 서비스 대상 (law, admrul, ordin 등) |
| `query` | X | 검색어 (기본값: `*`) |
| `numOfRows` | X | 한 페이지 결과 수 |
| `pageNo` | X | 페이지 번호 |

## 사용 예시

### 법령 검색

```bash
curl "http://apis.data.go.kr/1170000/law/lawSearch?serviceKey={SERVICE_KEY}&target=law&query=개인정보보호법&numOfRows=10&pageNo=1"
```

### 행정규칙 검색

```bash
curl "http://apis.data.go.kr/1170000/law/lawSearch?serviceKey={SERVICE_KEY}&target=admrul&query=시행규칙&numOfRows=10&pageNo=1"
```

### 자치법규 검색

```bash
curl "http://apis.data.go.kr/1170000/law/lawSearch?serviceKey={SERVICE_KEY}&target=ordin&query=조례&numOfRows=10&pageNo=1"
```

## 응답 항목

- `resultCode`: 결과코드
- `resultMsg`: 결과메시지
- `totalCnt`: 전체 검색건수
- 각 법령/규칙의 일련번호, 명칭, ID, 공포일자, 소관부처명
- `법령상세링크`: 상세 정보 확인 링크

## 에러 코드

| 코드 | 설명 |
|------|------|
| `01` | 잘못된 요청 파라미터 |
| `02` | 인증키 오류 (미설정) |
| `03` | 필수 파라미터 누락 |
| `09`, `99` | 시스템 오류 |

## 구현 시 주의사항

1. `ServiceKey`는 URL 인코딩하여 전송
2. XML 응답 파싱 필요 (BeautifulSoup, lxml 등 사용)
3. 검색어에 특수문자 포함 시 URL 인코딩 필요
4. 페이지네이션 활용하여 대량 데이터 조회
