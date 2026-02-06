# 재건축 정보 Agent 구축 계획

> 최종 업데이트: 2026-02-04

## 목표

재건축 관련 정보를 종합적으로 제공하는 AI Agent 시스템 구축
- 법령 정보, 실거래가, 건축물 정보, 정비사업 현황 등을 통합 조회
- 사용자가 특정 지역/단지의 재건축 가능성, 시세, 관련 법률을 쉽게 파악

---

## 완료된 기능

### 1. 법령 검색 MCP (korea-law)
- **상태**: ✅ 완료
- **위치**: `/mcp-servers/korea-law/`
- **기능**:
  - 재건축 관련 법률 검색 (도시정비법, 주택법, 건축법 등)
  - 법령해석례, 판례 조회

### 2. 부동산 실거래가 MCP (real-estate-transaction)
- **상태**: ✅ 완료
- **위치**: `/mcp-servers/real-estate-transaction/`
- **API 키**: `DATA_GO_KR_API_KEY` 환경변수 사용

### 3. 건축물대장 MCP (building-register)
- **상태**: ✅ 완료
- **위치**: `/mcp-servers/building-register/`
- **API 키**: `DATA_GO_KR_API_KEY` 환경변수 사용

#### 오퍼레이션 목록

| 오퍼레이션 | API | 설명 |
|-----------|-----|------|
| 기본개요 | `getBrBasisOulnInfo` | 건축물 기본 정보 (대장구분, 주소, 지역지구구역) |
| 총괄표제부 | `getBrRecapTitleInfo` | ⭐ 단지 전체 정보 (사용승인일, 면적, 세대수, 용적률) |
| 표제부 | `getBrTitleInfo` | 동별 상세 정보 (구조, 용도, 층수, 승강기, 내진설계) |
| 층별개요 | `getBrFlrOulnInfo` | 층별 구조, 용도, 면적 |
| 부속지번 | `getBrAtchJibunInfo` | 건축물 부속지번 정보 |
| 전유공용면적 | `getBrExposPubuseAreaInfo` | 전유/공용 면적 상세 |
| 오수정화시설 | `getBrWclfInfo` | 오수정화시설 정보 |
| 주택가격 | `getBrHsprcInfo` | 공동주택 공시가격 |
| 전유부 | `getBrExposInfo` | 집합건물 세대별 정보 (동/호) |
| 지역지구구역 | `getBrJijiguInfo` | 용도지역/지구/구역 |

#### 제공 도구 (Tools)

| 도구명 | 설명 |
|--------|------|
| `search_building_basic` | 기본개요 조회 |
| `search_building_recap_title` | 총괄표제부 조회 (⭐재건축 핵심) |
| `search_building_title` | 표제부 조회 (동별 상세) |
| `search_building_floor` | 층별개요 조회 |
| `search_building_expos` | 전유부 조회 (세대별) |
| `search_building_price` | 주택가격 조회 |
| `search_building_zone` | 지역지구구역 조회 |
| `get_building_operations` | 오퍼레이션 목록 조회 |

#### 필수 파라미터
- `sigungu_cd`: 시군구코드 5자리 (예: 11680 강남구)
- `bjdong_cd`: 법정동코드 5자리 (예: 10300 개포동)
- 코드 조회: [행정표준코드관리시스템](https://www.code.go.kr)

#### 승인된 API 목록

| API | 엔드포인트 | 상태 |
|-----|-----------|------|
| 아파트 매매 | `/RTMSDataSvcAptTrade/getRTMSDataSvcAptTrade` | ✅ |
| 아파트 전월세 | `/RTMSDataSvcAptRent/getRTMSDataSvcAptRent` | ✅ |
| 오피스텔 매매 | `/RTMSDataSvcOffiTrade/getRTMSDataSvcOffiTrade` | ✅ |
| 연립다세대 매매 | `/RTMSDataSvcRHTrade/getRTMSDataSvcRHTrade` | ✅ |
| 연립다세대 전월세 | `/RTMSDataSvcRHRent/getRTMSDataSvcRHRent` | ✅ |
| 법정동코드 | `/1741000/StanReginCd/getStanReginCdList` | ✅ |

#### 제공 도구 (Tools)

| 도구명 | 설명 |
|--------|------|
| `search_real_estate_transaction` | 실거래가 조회 (페이지네이션 지원) |
| `find_region_code` | 지역명 → LAWD_CD 변환 |
| `list_all_regions` | 전체 지역코드 목록 |
| `get_property_types` | 부동산/거래 유형 목록 |

#### 주요 특징
- 페이지네이션: `num_of_rows` (기본 30, 최대 100), `page_no` 지원
- 지역코드 자동 검색: "강남구" → "11680" 변환
- User-Agent 헤더 필수: `Mozilla/5.0 (compatible; RealEstateBot/1.0)`

---

## 미완료 기능 (우선순위순)

### 1. 정비사업 현황 API 🔴 높음
- **필요성**: 재건축/재개발 사업 진행 단계 확인
- **API 후보**:
  - 서울시 클린업시스템 API
  - 국토부 정비사업정보시스템
- **주요 정보**:
  - 조합설립인가, 사업시행인가, 관리처분인가 단계
  - 사업 진행률, 예상 일정
- **작업**:
  - [ ] API 조사 및 신청
  - [ ] MCP 서버에 도구 추가

### 2. 공시가격 API 🟡 중간
- **필요성**: 토지/주택 가격 → 조합원 분담금 추정
- **API**: 국토교통부 공시가격 알리미
- **주요 정보**: 공동주택 공시가격, 개별공시지가
- **작업**:
  - [ ] API 신청
  - [ ] MCP 서버에 도구 추가

### 3. 안전진단 정보 🟡 중간
- **필요성**: 재건축 추진 가능 여부 판단
- **정보 출처**:
  - 세움터 (건축행정시스템)
  - 지자체 정밀안전진단 결과
- **주요 정보**: 안전등급 (A~E), 진단 일자
- **작업**:
  - [ ] API 존재 여부 확인
  - [ ] 없으면 웹 스크래핑 또는 수동 조회 안내

### 4. 추가 실거래가 API 🟢 낮음
- **현재 미승인**:
  - 단독다가구 매매/전월세
  - 토지 매매
  - 분양입주권 매매
  - 상업업무용 매매
  - 공장창고 매매
- **작업**: 필요시 공공데이터포털에서 추가 신청

---

## 기술 스택

```
MCP Server: FastMCP (Python)
API: 공공데이터포털 (data.go.kr)
설정: .mcp.json
환경변수: DATA_GO_KR_API_KEY, KOREA_LAW_API_KEY
```

## 파일 구조

```
/mcp-servers/
├── korea-law/
│   └── server.py          # 법령 검색 MCP
├── real-estate-transaction/
│   ├── server.py          # 실거래가 MCP
│   ├── requirements.txt   # mcp[cli]>=1.0.0
│   └── .env.example
└── building-register/
    ├── server.py          # 건축물대장 MCP
    ├── requirements.txt   # mcp[cli]>=1.0.0
    └── .env.example

/.mcp.json                 # MCP 서버 설정
```

---

## 다음 작업

1. **정비사업 현황 API 조사** → 사업 진행 단계 확인
2. **통합 Agent 테스트** → 실제 재건축 단지 조회 시나리오
3. **공시가격 API 조사** → 조합원 분담금 추정

---

## API 키 정보

```
# 공공데이터포털 API 키 (동일 키로 여러 API 사용)
DATA_GO_KR_API_KEY=b350193ffdca5d21d3584bd98418d8ce768f996db6277f0a4f61218d90e30ad7

# 법령 API 키
KOREA_LAW_API_KEY=${KOREA_LAW_API_KEY}
```

---

## 참고 링크

- [공공데이터포털](https://www.data.go.kr)
- [국토교통부 실거래가 공개시스템](https://rt.molit.go.kr)
- [서울시 클린업시스템](https://cleanup.seoul.go.kr)
- [세움터](https://www.eais.go.kr)
- [법제처 국가법령정보센터](https://www.law.go.kr)
