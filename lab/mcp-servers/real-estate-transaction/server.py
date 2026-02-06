#!/usr/bin/env python3
"""
국토교통부 부동산 실거래가 Open API MCP 서버
아파트, 오피스텔, 연립다세대, 단독다가구, 토지 등 실거래가 조회
"""

import os
import json
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# 환경 변수 로드 (.env)
load_dotenv()

mcp = FastMCP("real-estate-transaction")

API_BASE_URL = "https://apis.data.go.kr/1613000"
REGION_CODE_API_URL = "https://apis.data.go.kr/1741000/StanReginCd/getStanReginCdList"

# 부동산 유형별 API 엔드포인트
ENDPOINTS = {
    # 아파트
    "아파트_매매": "/RTMSDataSvcAptTrade/getRTMSDataSvcAptTrade",
    "아파트_전월세": "/RTMSDataSvcAptRent/getRTMSDataSvcAptRent",
    # 오피스텔
    "오피스텔_매매": "/RTMSDataSvcOffiTrade/getRTMSDataSvcOffiTrade",
    "오피스텔_전월세": "/RTMSDataSvcOffiRent/getRTMSDataSvcOffiRent",
    # 연립다세대
    "연립다세대_매매": "/RTMSDataSvcRHTrade/getRTMSDataSvcRHTrade",
    "연립다세대_전월세": "/RTMSDataSvcRHRent/getRTMSDataSvcRHRent",
    # 단독/다가구
    "단독다가구_매매": "/RTMSDataSvcSHTrade/getRTMSDataSvcSHTrade",
    "단독다가구_전월세": "/RTMSDataSvcSHRent/getRTMSDataSvcSHRent",
    # 토지
    "토지_매매": "/RTMSDataSvcLandTrade/getRTMSDataSvcLandTrade",
    # 분양입주권
    "분양입주권_매매": "/RTMSDataSvcSilvTrade/getRTMSDataSvcSilvTrade",
    # 상업업무용
    "상업업무용_매매": "/RTMSDataSvcNrgTrade/getRTMSDataSvcNrgTrade",
    # 공장창고
    "공장창고_매매": "/RTMSDataSvcInduTrade/getRTMSDataSvcInduTrade",
}

# 부동산 유형
PROPERTY_TYPES = ["아파트", "오피스텔", "연립다세대", "단독다가구", "토지", "분양입주권", "상업업무용", "공장창고"]

# 거래 유형
TRADE_TYPES = {
    "아파트": ["매매", "전월세"],
    "오피스텔": ["매매", "전월세"],
    "연립다세대": ["매매", "전월세"],
    "단독다가구": ["매매", "전월세"],
    "토지": ["매매"],
    "분양입주권": ["매매"],
    "상업업무용": ["매매"],
    "공장창고": ["매매"],
}

# 주요 시군구 코드 (서울 중심)
SIGUNGU_CODES = {
    # 서울
    "서울_종로구": "11110",
    "서울_중구": "11140",
    "서울_용산구": "11170",
    "서울_성동구": "11200",
    "서울_광진구": "11215",
    "서울_동대문구": "11230",
    "서울_중랑구": "11260",
    "서울_성북구": "11290",
    "서울_강북구": "11305",
    "서울_도봉구": "11320",
    "서울_노원구": "11350",
    "서울_은평구": "11380",
    "서울_서대문구": "11410",
    "서울_마포구": "11440",
    "서울_양천구": "11470",
    "서울_강서구": "11500",
    "서울_구로구": "11530",
    "서울_금천구": "11545",
    "서울_영등포구": "11560",
    "서울_동작구": "11590",
    "서울_관악구": "11620",
    "서울_서초구": "11650",
    "서울_강남구": "11680",
    "서울_송파구": "11710",
    "서울_강동구": "11740",
    # 경기 주요 지역
    "경기_수원_장안구": "41111",
    "경기_수원_권선구": "41113",
    "경기_수원_팔달구": "41115",
    "경기_수원_영통구": "41117",
    "경기_성남_수정구": "41131",
    "경기_성남_중원구": "41133",
    "경기_성남_분당구": "41135",
    "경기_고양_덕양구": "41281",
    "경기_고양_일산동구": "41285",
    "경기_고양_일산서구": "41287",
    "경기_용인_처인구": "41461",
    "경기_용인_기흥구": "41463",
    "경기_용인_수지구": "41465",
    "경기_부천시": "41190",
    "경기_안양_만안구": "41171",
    "경기_안양_동안구": "41173",
    "경기_안산_상록구": "41271",
    "경기_안산_단원구": "41273",
    "경기_화성시": "41590",
    "경기_평택시": "41220",
    "경기_파주시": "41480",
    "경기_김포시": "41570",
    "경기_광명시": "41210",
    "경기_하남시": "41450",
    # 부산
    "부산_중구": "26110",
    "부산_서구": "26140",
    "부산_동구": "26170",
    "부산_영도구": "26200",
    "부산_부산진구": "26230",
    "부산_동래구": "26260",
    "부산_남구": "26290",
    "부산_북구": "26320",
    "부산_해운대구": "26350",
    "부산_사하구": "26380",
    "부산_금정구": "26410",
    "부산_강서구": "26440",
    "부산_연제구": "26470",
    "부산_수영구": "26500",
    "부산_사상구": "26530",
    "부산_기장군": "26710",
    # 인천
    "인천_중구": "28110",
    "인천_동구": "28140",
    "인천_미추홀구": "28177",
    "인천_연수구": "28185",
    "인천_남동구": "28200",
    "인천_부평구": "28237",
    "인천_계양구": "28245",
    "인천_서구": "28260",
    "인천_강화군": "28710",
    "인천_옹진군": "28720",
    # 대구
    "대구_중구": "27110",
    "대구_동구": "27140",
    "대구_서구": "27170",
    "대구_남구": "27200",
    "대구_북구": "27230",
    "대구_수성구": "27260",
    "대구_달서구": "27290",
    "대구_달성군": "27710",
    # 대전
    "대전_동구": "30110",
    "대전_중구": "30140",
    "대전_서구": "30170",
    "대전_유성구": "30200",
    "대전_대덕구": "30230",
    # 광주
    "광주_동구": "29110",
    "광주_서구": "29140",
    "광주_남구": "29155",
    "광주_북구": "29170",
    "광주_광산구": "29200",
    # 울산
    "울산_중구": "31110",
    "울산_남구": "31140",
    "울산_동구": "31170",
    "울산_북구": "31200",
    "울산_울주군": "31710",
    # 세종
    "세종특별자치시": "36110",
}


def find_sigungu_code_local(query: str) -> list:
    """
    지역명으로 시군구 코드 검색 (로컬 캐시)
    예: "영등포" -> [("서울_영등포구", "11560")]
    """
    query = query.strip().replace(" ", "")
    results = []

    for name, code in SIGUNGU_CODES.items():
        # 정확히 일치하는 경우 (구 이름만)
        district = name.split("_")[-1]  # "영등포구"
        if query == district or query == district.replace("구", "") or query == district.replace("시", "") or query == district.replace("군", ""):
            results.append((name, code))
        # 부분 일치
        elif query in name.replace("_", ""):
            results.append((name, code))

    return results


def search_region_code_api(region_name: str) -> dict:
    """
    행정안전부 법정동코드 API를 통해 지역 코드 검색

    Args:
        region_name: 검색할 지역명 (예: "서울특별시 영등포구", "영등포구", "강남")

    Returns:
        {"success": True, "results": [...]} 또는 {"success": False, "error": "..."}
    """
    api_key = os.environ.get("DATA_GO_KR_API_KEY")
    if not api_key:
        return {"success": False, "error": "DATA_GO_KR_API_KEY 환경변수가 설정되지 않았습니다."}

    params = urllib.parse.urlencode({
        "serviceKey": api_key,
        "type": "json",
        "pageNo": "1",
        "numOfRows": "100",
        "flag": "Y",
        "locatadd_nm": region_name,
    }, quote_via=urllib.parse.quote)

    url = f"{REGION_CODE_API_URL}?{params}"

    try:
        req = urllib.request.Request(url)
        req.add_header("User-Agent", "Mozilla/5.0 (compatible; RealEstateBot/1.0)")
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))

            # 응답 파싱
            stan_regin = data.get("StanReginCd", [])
            if len(stan_regin) < 2:
                return {"success": True, "results": []}

            rows = stan_regin[1].get("row", [])

            results = []
            seen_codes = set()  # 중복 제거용

            for row in rows:
                sido_cd = row.get("sido_cd", "")
                sgg_cd = row.get("sgg_cd", "")

                # 시군구 코드 생성 (시도코드 + 시군구코드 = 5자리)
                if sido_cd and sgg_cd and sgg_cd != "000":
                    lawd_cd = sido_cd + sgg_cd
                    if lawd_cd not in seen_codes:
                        seen_codes.add(lawd_cd)
                        results.append({
                            "lawd_cd": lawd_cd,
                            "full_address": row.get("locatadd_nm", ""),
                            "lowest_name": row.get("locallow_nm", ""),
                            "region_cd": row.get("region_cd", ""),
                        })

            return {"success": True, "results": results}

    except urllib.error.HTTPError as e:
        return {"success": False, "error": f"HTTP 오류: {e.code}"}
    except urllib.error.URLError as e:
        return {"success": False, "error": f"네트워크 오류: {e.reason}"}
    except json.JSONDecodeError as e:
        return {"success": False, "error": f"JSON 파싱 오류: {e}"}
    except Exception as e:
        return {"success": False, "error": f"오류: {e}"}


def parse_xml_response(xml_text: str) -> dict:
    """XML 응답을 파싱하여 딕셔너리로 반환"""
    try:
        root = ET.fromstring(xml_text)

        # 결과 코드 확인 (공공데이터포털 표준 응답)
        result_code = root.findtext(".//resultCode", "")
        result_msg = root.findtext(".//resultMsg", "")

        result = {
            "resultCode": result_code,
            "resultMsg": result_msg,
            "items": []
        }

        # 에러 체크
        if result_code and result_code != "00":
            error_msgs = {
                "01": "어플리케이션 에러",
                "02": "DB 에러",
                "03": "데이터 없음",
                "04": "HTTP 에러",
                "05": "서비스 연결 실패",
                "10": "잘못된 요청 파라미터",
                "11": "필수 파라미터 누락",
                "12": "서비스키 인증 실패",
                "20": "트래픽 초과",
                "21": "일일 호출건수 초과",
                "22": "서비스 시간 외",
                "30": "등록되지 않은 서비스키",
                "31": "기한만료된 서비스키",
                "32": "등록되지 않은 IP",
            }
            result["error"] = error_msgs.get(result_code, f"알 수 없는 오류 (코드: {result_code}, 메시지: {result_msg})")
            return result

        # 항목들 파싱 (item 태그)
        for item in root.iter("item"):
            item_dict = {}
            for child in item:
                if child.text:
                    item_dict[child.tag] = child.text.strip()
            if item_dict:
                result["items"].append(item_dict)

        return result
    except ET.ParseError as e:
        return {"error": f"XML 파싱 오류: {e}", "raw": xml_text[:1000]}


def format_price(price_str: str) -> str:
    """가격을 읽기 쉬운 형식으로 변환 (만원 단위)"""
    try:
        # 쉼표 제거 후 숫자 변환
        price = int(price_str.replace(",", "").replace(" ", ""))
        if price >= 10000:
            억 = price // 10000
            만 = price % 10000
            if 만 > 0:
                return f"{억}억 {만:,}만원"
            return f"{억}억원"
        return f"{price:,}만원"
    except (ValueError, AttributeError):
        return price_str


def format_apt_trade_result(result: dict, sigungu_code: str, year_month: str, total_count: int, page_no: int, num_of_rows: int) -> str:
    """아파트 매매 결과를 마크다운 형식으로 포맷팅"""
    if "error" in result:
        return f"오류: {result['error']}"

    total_pages = (total_count + num_of_rows - 1) // num_of_rows if total_count > 0 else 1
    start_idx = (page_no - 1) * num_of_rows + 1
    end_idx = min(page_no * num_of_rows, total_count)

    output = ["## 아파트 매매 실거래가 조회 결과"]
    output.append(f"- 지역코드: {sigungu_code}")
    output.append(f"- 계약년월: {year_month}")
    output.append(f"- **총 {total_count}건 중 {start_idx}~{end_idx}건 표시 (page {page_no}/{total_pages})**\n")

    if not result["items"]:
        output.append("검색 결과가 없습니다.")
        return "\n".join(output)

    for i, item in enumerate(result["items"], start_idx):
        apt_name = item.get("aptNm", item.get("아파트", "정보없음"))
        price = format_price(item.get("dealAmount", item.get("거래금액", "0")))
        area = item.get("excluUseAr", item.get("전용면적", ""))
        floor = item.get("floor", item.get("층", ""))
        dong = item.get("umdNm", item.get("법정동", ""))
        year = item.get("dealYear", item.get("년", ""))
        month = item.get("dealMonth", item.get("월", ""))
        day = item.get("dealDay", item.get("일", ""))
        build_year = item.get("buildYear", item.get("건축년도", ""))

        output.append(f"### {i}. {apt_name}")
        output.append(f"- **거래금액**: {price}")
        output.append(f"- **전용면적**: {area}㎡")
        output.append(f"- **층**: {floor}층")
        output.append(f"- **법정동**: {dong}")
        output.append(f"- **계약일**: {year}.{month}.{day}")
        output.append(f"- **건축년도**: {build_year}년")

        # 추가 정보
        if item.get("dealingGbn", item.get("거래유형")):
            output.append(f"- **거래유형**: {item.get('dealingGbn', item.get('거래유형'))}")
        if item.get("rgstDate", item.get("등기일자")):
            output.append(f"- **등기일자**: {item.get('rgstDate', item.get('등기일자'))}")
        output.append("")

    if page_no < total_pages:
        output.append(f"\n※ 더 보려면 page_no={page_no + 1} 로 조회하세요.")

    return "\n".join(output)


def format_apt_rent_result(result: dict, sigungu_code: str, year_month: str, total_count: int, page_no: int, num_of_rows: int) -> str:
    """아파트 전월세 결과를 마크다운 형식으로 포맷팅"""
    if "error" in result:
        return f"오류: {result['error']}"

    total_pages = (total_count + num_of_rows - 1) // num_of_rows if total_count > 0 else 1
    start_idx = (page_no - 1) * num_of_rows + 1
    end_idx = min(page_no * num_of_rows, total_count)

    output = ["## 아파트 전월세 실거래가 조회 결과"]
    output.append(f"- 지역코드: {sigungu_code}")
    output.append(f"- 계약년월: {year_month}")
    output.append(f"- **총 {total_count}건 중 {start_idx}~{end_idx}건 표시 (page {page_no}/{total_pages})**\n")

    if not result["items"]:
        output.append("검색 결과가 없습니다.")
        return "\n".join(output)

    for i, item in enumerate(result["items"], start_idx):
        apt_name = item.get("aptNm", item.get("아파트", "정보없음"))
        deposit = format_price(item.get("deposit", item.get("보증금액", "0")))
        monthly = item.get("monthlyRent", item.get("월세금액", "0"))
        area = item.get("excluUseAr", item.get("전용면적", ""))
        floor = item.get("floor", item.get("층", ""))
        dong = item.get("umdNm", item.get("법정동", ""))

        rent_type = "전세" if monthly == "0" or monthly == "" else "월세"

        output.append(f"### {i}. {apt_name} ({rent_type})")
        output.append(f"- **보증금**: {deposit}")
        if rent_type == "월세":
            output.append(f"- **월세**: {monthly}만원")
        output.append(f"- **전용면적**: {area}㎡")
        output.append(f"- **층**: {floor}층")
        output.append(f"- **법정동**: {dong}")

        # 계약 정보
        contract_type = item.get("contractType", item.get("계약구분", ""))
        if contract_type:
            output.append(f"- **계약구분**: {contract_type}")
        contract_term = item.get("contractTerm", item.get("계약기간", ""))
        if contract_term:
            output.append(f"- **계약기간**: {contract_term}")
        output.append("")

    if page_no < total_pages:
        output.append(f"\n※ 더 보려면 page_no={page_no + 1} 로 조회하세요.")

    return "\n".join(output)


def format_general_result(result: dict, property_type: str, trade_type: str, sigungu_code: str, year_month: str, total_count: int, page_no: int, num_of_rows: int) -> str:
    """일반 부동산 거래 결과를 마크다운 형식으로 포맷팅"""
    if "error" in result:
        return f"오류: {result['error']}"

    total_pages = (total_count + num_of_rows - 1) // num_of_rows if total_count > 0 else 1
    start_idx = (page_no - 1) * num_of_rows + 1
    end_idx = min(page_no * num_of_rows, total_count)

    output = [f"## {property_type} {trade_type} 실거래가 조회 결과"]
    output.append(f"- 지역코드: {sigungu_code}")
    output.append(f"- 계약년월: {year_month}")
    output.append(f"- **총 {total_count}건 중 {start_idx}~{end_idx}건 표시 (page {page_no}/{total_pages})**\n")

    if not result["items"]:
        output.append("검색 결과가 없습니다.")
        return "\n".join(output)

    for i, item in enumerate(result["items"], start_idx):
        # 부동산명 추출 (여러 필드명 시도)
        name = (item.get("aptNm") or item.get("offiNm") or item.get("mhouseNm") or
                item.get("아파트") or item.get("단지") or item.get("연립다세대") or
                item.get("법정동", "정보없음"))

        output.append(f"### {i}. {name}")

        # 거래금액 (매매인 경우)
        if trade_type == "매매":
            price = item.get("dealAmount", item.get("거래금액", ""))
            if price:
                output.append(f"- **거래금액**: {format_price(price)}")

        # 보증금/월세 (전월세인 경우)
        if trade_type == "전월세":
            deposit = item.get("deposit", item.get("보증금액", item.get("보증금", "")))
            monthly = item.get("monthlyRent", item.get("월세금액", item.get("월세", "")))
            if deposit:
                output.append(f"- **보증금**: {format_price(deposit)}")
            if monthly and monthly != "0":
                output.append(f"- **월세**: {monthly}만원")

        # 면적
        area = item.get("excluUseAr", item.get("전용면적", item.get("계약면적", "")))
        if area:
            output.append(f"- **면적**: {area}㎡")

        # 층
        floor = item.get("floor", item.get("층", ""))
        if floor:
            output.append(f"- **층**: {floor}층")

        # 법정동
        dong = item.get("umdNm", item.get("법정동", ""))
        if dong:
            output.append(f"- **법정동**: {dong}")

        # 건축년도
        build_year = item.get("buildYear", item.get("건축년도", ""))
        if build_year:
            output.append(f"- **건축년도**: {build_year}년")

        output.append("")

    if page_no < total_pages:
        output.append(f"\n※ 더 보려면 page_no={page_no + 1} 로 조회하세요.")

    return "\n".join(output)


@mcp.tool()
def search_real_estate_transaction(
    sigungu_code: str,
    year_month: str,
    property_type: str = "아파트",
    trade_type: str = "매매",
    num_of_rows: int = 30,
    page_no: int = 1
) -> str:
    """
    부동산 실거래가 조회

    Args:
        sigungu_code: 시군구코드 5자리 (예: "11680" 강남구, "11650" 서초구)
            - 서울 강남구: 11680, 서초구: 11650, 송파구: 11710
            - 경기 성남 분당구: 41135, 용인 수지구: 41465
            - find_region_code() 도구로 지역명으로 코드 검색 가능
        year_month: 계약년월 6자리 (예: "202401" = 2024년 1월)
        property_type: 부동산 유형
            - 아파트, 오피스텔, 연립다세대, 단독다가구, 토지, 분양입주권, 상업업무용, 공장창고
        trade_type: 거래 유형
            - 매매, 전월세 (토지/분양입주권/상업업무용/공장창고는 매매만 가능)
        num_of_rows: 한 페이지에 표시할 건수 (기본: 30, 최대: 100)
        page_no: 페이지 번호 (기본: 1). 더 많은 결과를 보려면 증가시키세요.

    Returns:
        실거래가 목록 (단지명, 거래금액, 면적, 층, 계약일 등)
        - 총 건수와 현재 페이지 정보 포함
        - 더 많은 결과가 있으면 다음 페이지 안내
    """
    api_key = os.environ.get("DATA_GO_KR_API_KEY")
    if not api_key:
        return "오류: DATA_GO_KR_API_KEY 환경변수가 설정되지 않았습니다.\n공공데이터포털(data.go.kr)에서 API 키를 발급받아 설정해주세요."

    # 유효성 검사
    if property_type not in PROPERTY_TYPES:
        return f"오류: 잘못된 부동산 유형입니다. 가능한 값: {', '.join(PROPERTY_TYPES)}"

    available_trades = TRADE_TYPES.get(property_type, ["매매"])
    if trade_type not in available_trades:
        return f"오류: {property_type}의 가능한 거래 유형: {', '.join(available_trades)}"

    if len(sigungu_code) != 5 or not sigungu_code.isdigit():
        return "오류: 시군구코드는 5자리 숫자여야 합니다. (예: 11680)"

    if len(year_month) != 6 or not year_month.isdigit():
        return "오류: 계약년월은 6자리 숫자여야 합니다. (예: 202401)"

    # num_of_rows 범위 제한
    num_of_rows = max(1, min(100, num_of_rows))
    page_no = max(1, page_no)

    # 엔드포인트 결정
    endpoint_key = f"{property_type}_{trade_type}"
    endpoint = ENDPOINTS.get(endpoint_key)
    if not endpoint:
        return f"오류: 지원하지 않는 조합입니다: {property_type} {trade_type}"

    # API 호출
    params = urllib.parse.urlencode({
        "serviceKey": api_key,
        "LAWD_CD": sigungu_code,
        "DEAL_YMD": year_month,
        "numOfRows": str(num_of_rows),
        "pageNo": str(page_no),
    }, quote_via=urllib.parse.quote)

    url = f"{API_BASE_URL}{endpoint}?{params}"

    try:
        req = urllib.request.Request(url)
        req.add_header("User-Agent", "Mozilla/5.0 (compatible; RealEstateBot/1.0)")
        with urllib.request.urlopen(req, timeout=30) as response:
            xml_text = response.read().decode("utf-8")
            result = parse_xml_response(xml_text)

            # totalCount 추출
            import xml.etree.ElementTree as ET
            root = ET.fromstring(xml_text)
            total_count = int(root.findtext(".//totalCount", "0"))

            # 결과 포맷팅
            if property_type == "아파트" and trade_type == "매매":
                return format_apt_trade_result(result, sigungu_code, year_month, total_count, page_no, num_of_rows)
            elif property_type == "아파트" and trade_type == "전월세":
                return format_apt_rent_result(result, sigungu_code, year_month, total_count, page_no, num_of_rows)
            else:
                return format_general_result(result, property_type, trade_type, sigungu_code, year_month, total_count, page_no, num_of_rows)

    except urllib.error.HTTPError as e:
        return f"HTTP 오류: {e.code} - {e.reason}"
    except urllib.error.URLError as e:
        return f"네트워크 오류: {e.reason}"
    except Exception as e:
        return f"오류 발생: {e}"


@mcp.tool()
def find_region_code(query: str) -> str:
    """
    지역명으로 시군구 코드(LAWD_CD) 검색 - 행정안전부 법정동코드 API 사용

    Args:
        query: 검색할 지역명 (예: "영등포구", "서울특별시 강남구", "분당구", "해운대구")
            - "서울특별시 영등포구" 형식 권장
            - "영등포구"만 입력해도 검색 가능

    Returns:
        검색된 시군구명과 LAWD_CD 코드 (실거래가 조회에 사용)
    """
    output = [f"## '{query}' 지역코드 검색 결과\n"]

    # 1. 먼저 API로 검색 시도
    api_result = search_region_code_api(query)

    if api_result["success"] and api_result["results"]:
        results = api_result["results"]

        # 시군구 레벨 코드만 추출 (중복 제거됨)
        unique_codes = {}
        for r in results:
            code = r["lawd_cd"]
            if code not in unique_codes:
                # 주소에서 시군구 부분 추출
                addr_parts = r["full_address"].split()
                if len(addr_parts) >= 2:
                    sigungu_name = " ".join(addr_parts[:2])  # "서울특별시 영등포구"
                else:
                    sigungu_name = r["full_address"]
                unique_codes[code] = sigungu_name

        output.append("### 검색된 지역 (API)")
        for code, name in unique_codes.items():
            output.append(f"- **{name}**: `{code}`")

        if len(unique_codes) == 1:
            code, name = list(unique_codes.items())[0]
            output.append(f"\n✅ 실거래가 조회에 이 코드를 사용하세요: `{code}`")
        else:
            output.append(f"\n⚠️ {len(unique_codes)}개 지역이 검색되었습니다. 원하는 지역의 코드를 선택하세요.")

        return "\n".join(output)

    # 2. API 실패 시 로컬 캐시에서 검색
    local_results = find_sigungu_code_local(query)

    if local_results:
        output.append("### 검색된 지역 (로컬 캐시)")
        for name, code in local_results:
            output.append(f"- **{name}**: `{code}`")

        if len(local_results) == 1:
            output.append(f"\n✅ 이 코드를 사용하세요: `{local_results[0][1]}`")
        else:
            output.append(f"\n⚠️ {len(local_results)}개 지역이 검색되었습니다.")
    else:
        # 광역시/도 필터 시도
        filtered = {k: v for k, v in SIGUNGU_CODES.items() if query in k}
        if filtered:
            output.append(f"### {query} 지역 목록 (로컬 캐시)")
            for name, code in sorted(filtered.items()):
                district = "_".join(name.split("_")[1:])
                output.append(f"- {district}: `{code}`")
        else:
            if api_result.get("error"):
                output.append(f"API 오류: {api_result['error']}\n")
            output.append("검색 결과가 없습니다.\n")
            output.append("### 검색 팁")
            output.append("- 정확한 지역명: `서울특별시 강남구`, `경기도 성남시 분당구`")
            output.append("- 구/군 이름만: `강남구`, `분당구`, `해운대구`")

    return "\n".join(output)


@mcp.tool()
def list_all_regions() -> str:
    """
    지원되는 전체 지역 목록 조회

    Returns:
        광역시/도별 시군구 코드 전체 목록
    """
    output = ["## 전체 시군구 코드 목록\n"]

    current_region = ""
    for name, code in sorted(SIGUNGU_CODES.items()):
        region_name = name.split("_")[0]
        if region_name != current_region:
            current_region = region_name
            output.append(f"\n### {current_region}")

        district = "_".join(name.split("_")[1:])
        output.append(f"- {district}: `{code}`")

    output.append("\n---")
    output.append(f"총 {len(SIGUNGU_CODES)}개 지역")
    output.append("\n※ 더 많은 지역코드는 행정표준코드관리시스템(code.go.kr)에서 확인 가능")
    return "\n".join(output)


@mcp.tool()
def get_property_types() -> str:
    """
    조회 가능한 부동산 유형 및 거래 유형 목록

    Returns:
        부동산 유형별 가능한 거래 유형 목록
    """
    output = ["## 조회 가능한 부동산 유형\n"]

    for prop_type in PROPERTY_TYPES:
        trades = TRADE_TYPES.get(prop_type, ["매매"])
        output.append(f"### {prop_type}")
        output.append(f"- 거래유형: {', '.join(trades)}")

        # 설명 추가
        descriptions = {
            "아파트": "공동주택 중 아파트 (5층 이상)",
            "오피스텔": "업무시설 중 오피스텔",
            "연립다세대": "연립주택, 다세대주택",
            "단독다가구": "단독주택, 다가구주택",
            "토지": "토지 거래",
            "분양입주권": "아파트 분양권 및 입주권",
            "상업업무용": "상가, 사무실 등 상업/업무용 부동산",
            "공장창고": "공장, 창고 등 산업시설",
        }
        output.append(f"- 설명: {descriptions.get(prop_type, '')}\n")

    return "\n".join(output)


if __name__ == "__main__":
    mcp.run()
