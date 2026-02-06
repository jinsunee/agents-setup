#!/usr/bin/env python3
"""
건축HUB 건축물대장정보 서비스 MCP 서버
건축물대장 기본개요, 표제부, 층별개요, 전유부 등 조회
"""

import os
import http.client
import urllib.parse
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# 환경 변수 로드 (.env)
load_dotenv()

mcp = FastMCP("building-register")

API_BASE_URL = "https://apis.data.go.kr/1613000/BldRgstHubService"

# 오퍼레이션 목록
OPERATIONS = {
    "기본개요": "getBrBasisOulnInfo",
    "총괄표제부": "getBrRecapTitleInfo",
    "표제부": "getBrTitleInfo",
    "층별개요": "getBrFlrOulnInfo",
    "부속지번": "getBrAtchJibunInfo",
    "전유공용면적": "getBrExposPubuseAreaInfo",
    "오수정화시설": "getBrWclfInfo",
    "주택가격": "getBrHsprcInfo",
    "전유부": "getBrExposInfo",
    "지역지구구역": "getBrJijiguInfo",
}


def parse_xml_response(xml_text: str) -> dict:
    """XML 응답을 파싱하여 딕셔너리로 반환"""
    try:
        root = ET.fromstring(xml_text)

        result_code = root.findtext(".//resultCode", "")
        result_msg = root.findtext(".//resultMsg", "")
        total_count = int(root.findtext(".//totalCount", "0"))
        num_of_rows = int(root.findtext(".//numOfRows", "10"))
        page_no = int(root.findtext(".//pageNo", "1"))

        result = {
            "resultCode": result_code,
            "resultMsg": result_msg,
            "totalCount": total_count,
            "numOfRows": num_of_rows,
            "pageNo": page_no,
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

        # 항목들 파싱
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


def format_area(area_str: str) -> str:
    """면적을 읽기 쉬운 형식으로 변환"""
    try:
        area = float(area_str)
        pyeong = area / 3.3058
        return f"{area:.2f}㎡ ({pyeong:.1f}평)"
    except (ValueError, TypeError):
        return area_str or "-"


def format_price(price_str: str) -> str:
    """가격을 읽기 쉬운 형식으로 변환 (원 단위)"""
    try:
        price = int(float(price_str))
        if price >= 100000000:
            억 = price // 100000000
            만 = (price % 100000000) // 10000
            if 만 > 0:
                return f"{억}억 {만:,}만원"
            return f"{억}억원"
        elif price >= 10000:
            return f"{price // 10000:,}만원"
        return f"{price:,}원"
    except (ValueError, TypeError):
        return price_str or "-"


def format_date(date_str: str) -> str:
    """날짜를 읽기 쉬운 형식으로 변환 (YYYYMMDD -> YYYY-MM-DD)"""
    if date_str and len(date_str) == 8:
        return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
    return date_str or "-"


def calculate_building_age(use_apr_day: str) -> str:
    """사용승인일로부터 건축연수 계산"""
    if not use_apr_day or len(use_apr_day) < 4:
        return "-"
    try:
        from datetime import datetime
        build_year = int(use_apr_day[:4])
        current_year = datetime.now().year
        age = current_year - build_year
        return f"{age}년"
    except (ValueError, TypeError):
        return "-"


def format_basis_result(result: dict, sigungu_cd: str, bjdong_cd: str, bun: str, ji: str) -> str:
    """기본개요 조회 결과 포맷팅"""
    if "error" in result:
        return f"오류: {result['error']}"

    total = result["totalCount"]
    page_no = result["pageNo"]
    num_of_rows = result["numOfRows"]
    total_pages = (total + num_of_rows - 1) // num_of_rows if total > 0 else 1

    output = ["## 건축물대장 기본개요 조회 결과"]
    output.append(f"- 시군구코드: {sigungu_cd}, 법정동코드: {bjdong_cd}")
    if bun:
        output.append(f"- 번: {bun}, 지: {ji or '0000'}")
    output.append(f"- **총 {total}건 (page {page_no}/{total_pages})**\n")

    if not result["items"]:
        output.append("검색 결과가 없습니다.")
        return "\n".join(output)

    for i, item in enumerate(result["items"], 1):
        plat_plc = item.get("platPlc", "-")
        new_plat_plc = item.get("newPlatPlc", "-")
        bld_nm = item.get("bldNm", "-")
        regstr_gb_cd_nm = item.get("regstrGbCdNm", "-")
        regstr_kind_cd_nm = item.get("regstrKindCdNm", "-")

        output.append(f"### {i}. {bld_nm}")
        output.append(f"- **지번주소**: {plat_plc}")
        output.append(f"- **도로명주소**: {new_plat_plc}")
        output.append(f"- **대장구분**: {regstr_gb_cd_nm} ({regstr_kind_cd_nm})")

        # 지역지구구역 정보
        jiyuk = item.get("jiyukCdNm", "")
        jigu = item.get("jiguCdNm", "")
        guyuk = item.get("guyukCdNm", "")
        if jiyuk or jigu or guyuk:
            zones = [z for z in [jiyuk, jigu, guyuk] if z]
            output.append(f"- **지역지구구역**: {', '.join(zones)}")
        output.append("")

    if page_no < total_pages:
        output.append(f"\n※ 더 보려면 page_no={page_no + 1} 로 조회하세요.")

    return "\n".join(output)


def format_recap_title_result(result: dict, sigungu_cd: str, bjdong_cd: str, bun: str, ji: str) -> str:
    """총괄표제부 조회 결과 포맷팅 - 재건축 판단에 중요한 정보"""
    if "error" in result:
        return f"오류: {result['error']}"

    total = result["totalCount"]
    page_no = result["pageNo"]
    num_of_rows = result["numOfRows"]
    total_pages = (total + num_of_rows - 1) // num_of_rows if total > 0 else 1

    output = ["## 건축물대장 총괄표제부 조회 결과"]
    output.append(f"- 시군구코드: {sigungu_cd}, 법정동코드: {bjdong_cd}")
    if bun:
        output.append(f"- 번: {bun}, 지: {ji or '0000'}")
    output.append(f"- **총 {total}건 (page {page_no}/{total_pages})**\n")

    if not result["items"]:
        output.append("검색 결과가 없습니다.")
        return "\n".join(output)

    for i, item in enumerate(result["items"], 1):
        plat_plc = item.get("platPlc", "-")
        new_plat_plc = item.get("newPlatPlc", "-")
        bld_nm = item.get("bldNm", "-")

        output.append(f"### {i}. {bld_nm}")
        output.append(f"- **지번주소**: {plat_plc}")
        output.append(f"- **도로명주소**: {new_plat_plc}")

        # 핵심 정보: 사용승인일 (건축년도 판단)
        use_apr_day = item.get("useAprDay", "")
        if use_apr_day and use_apr_day.strip():
            building_age = calculate_building_age(use_apr_day)
            output.append(f"- **🏗️ 사용승인일**: {format_date(use_apr_day)} (건축연수: {building_age})")
        else:
            output.append(f"- **🏗️ 사용승인일**: 정보없음")

        # 면적 정보
        plat_area = item.get("platArea", "0")
        arch_area = item.get("archArea", "0")
        tot_area = item.get("totArea", "0")
        bc_rat = item.get("bcRat", "0")
        vl_rat = item.get("vlRat", "0")

        output.append(f"- **대지면적**: {format_area(plat_area)}")
        output.append(f"- **건축면적**: {format_area(arch_area)}")
        output.append(f"- **연면적**: {format_area(tot_area)}")
        output.append(f"- **건폐율**: {bc_rat}%, **용적률**: {vl_rat}%")

        # 용도 정보
        main_purps = item.get("mainPurpsCdNm", "-")
        etc_purps = item.get("etcPurps", "")
        output.append(f"- **주용도**: {main_purps}")
        if etc_purps:
            output.append(f"- **기타용도**: {etc_purps}")

        # 세대/호수 정보
        hhld_cnt = item.get("hhldCnt", "0")
        ho_cnt = item.get("hoCnt", "0")
        main_bld_cnt = item.get("mainBldCnt", "0")
        output.append(f"- **세대수**: {hhld_cnt}세대, **호수**: {ho_cnt}호, **주건축물수**: {main_bld_cnt}동")

        # 주차 정보
        tot_pkng_cnt = item.get("totPkngCnt", "0")
        output.append(f"- **총주차대수**: {tot_pkng_cnt}대")

        # 에너지/친환경 등급
        engr_grade = item.get("engrGrade", "")
        gn_bld_grade = item.get("gnBldGrade", "")
        if engr_grade:
            output.append(f"- **에너지효율등급**: {engr_grade}")
        if gn_bld_grade:
            output.append(f"- **친환경건축물등급**: {gn_bld_grade}")

        output.append("")

    if page_no < total_pages:
        output.append(f"\n※ 더 보려면 page_no={page_no + 1} 로 조회하세요.")

    return "\n".join(output)


def format_title_result(result: dict, sigungu_cd: str, bjdong_cd: str, bun: str, ji: str) -> str:
    """표제부 조회 결과 포맷팅 - 동별 상세 정보"""
    if "error" in result:
        return f"오류: {result['error']}"

    total = result["totalCount"]
    page_no = result["pageNo"]
    num_of_rows = result["numOfRows"]
    total_pages = (total + num_of_rows - 1) // num_of_rows if total > 0 else 1

    output = ["## 건축물대장 표제부 조회 결과"]
    output.append(f"- 시군구코드: {sigungu_cd}, 법정동코드: {bjdong_cd}")
    if bun:
        output.append(f"- 번: {bun}, 지: {ji or '0000'}")
    output.append(f"- **총 {total}건 (page {page_no}/{total_pages})**\n")

    if not result["items"]:
        output.append("검색 결과가 없습니다.")
        return "\n".join(output)

    for i, item in enumerate(result["items"], 1):
        plat_plc = item.get("platPlc", "-")
        bld_nm = item.get("bldNm", "-")
        dong_nm = item.get("dongNm", "-")

        output.append(f"### {i}. {bld_nm} ({dong_nm})")
        output.append(f"- **대지위치**: {plat_plc}")

        # 주/부속 구분
        main_atch = item.get("mainAtchGbCdNm", "-")
        output.append(f"- **주부속구분**: {main_atch}")

        # 사용승인일
        use_apr_day = item.get("useAprDay", "")
        if use_apr_day and use_apr_day.strip():
            building_age = calculate_building_age(use_apr_day)
            output.append(f"- **🏗️ 사용승인일**: {format_date(use_apr_day)} (건축연수: {building_age})")

        # 구조 정보
        strct_cd_nm = item.get("strctCdNm", "-")
        etc_strct = item.get("etcStrct", "")
        output.append(f"- **구조**: {strct_cd_nm}")
        if etc_strct and etc_strct != strct_cd_nm:
            output.append(f"- **기타구조**: {etc_strct}")

        # 지붕 정보
        roof_cd_nm = item.get("roofCdNm", "")
        if roof_cd_nm:
            output.append(f"- **지붕**: {roof_cd_nm}")

        # 용도 정보
        main_purps = item.get("mainPurpsCdNm", "-")
        etc_purps = item.get("etcPurps", "")
        output.append(f"- **주용도**: {main_purps}")
        if etc_purps:
            output.append(f"- **기타용도**: {etc_purps}")

        # 면적 정보
        arch_area = item.get("archArea", "0")
        tot_area = item.get("totArea", "0")
        output.append(f"- **건축면적**: {format_area(arch_area)}")
        output.append(f"- **연면적**: {format_area(tot_area)}")

        # 층수 정보
        grnd_flr = item.get("grndFlrCnt", "0")
        ugrnd_flr = item.get("ugrndFlrCnt", "0")
        heit = item.get("heit", "0")
        output.append(f"- **층수**: 지상 {grnd_flr}층, 지하 {ugrnd_flr}층")
        if heit and float(heit) > 0:
            output.append(f"- **높이**: {heit}m")

        # 승강기 정보
        ride_elvt = item.get("rideUseElvtCnt", "0")
        emgen_elvt = item.get("emgenUseElvtCnt", "0")
        if int(ride_elvt) > 0 or int(emgen_elvt) > 0:
            output.append(f"- **승강기**: 승용 {ride_elvt}대, 비상용 {emgen_elvt}대")

        # 내진설계
        rserthqk = item.get("rserthqkDsgnApplyYn", "0")
        rserthqk_ablty = item.get("rserthqkAblty", "")
        if rserthqk == "1":
            output.append(f"- **내진설계**: 적용 ({rserthqk_ablty})" if rserthqk_ablty else "- **내진설계**: 적용")

        output.append("")

    if page_no < total_pages:
        output.append(f"\n※ 더 보려면 page_no={page_no + 1} 로 조회하세요.")

    return "\n".join(output)


def format_floor_result(result: dict, sigungu_cd: str, bjdong_cd: str, bun: str, ji: str) -> str:
    """층별개요 조회 결과 포맷팅"""
    if "error" in result:
        return f"오류: {result['error']}"

    total = result["totalCount"]
    page_no = result["pageNo"]
    num_of_rows = result["numOfRows"]
    total_pages = (total + num_of_rows - 1) // num_of_rows if total > 0 else 1

    output = ["## 건축물대장 층별개요 조회 결과"]
    output.append(f"- 시군구코드: {sigungu_cd}, 법정동코드: {bjdong_cd}")
    if bun:
        output.append(f"- 번: {bun}, 지: {ji or '0000'}")
    output.append(f"- **총 {total}건 (page {page_no}/{total_pages})**\n")

    if not result["items"]:
        output.append("검색 결과가 없습니다.")
        return "\n".join(output)

    # 층별로 그룹화
    current_dong = ""
    for i, item in enumerate(result["items"], 1):
        dong_nm = item.get("dongNm", "-")
        flr_gb_nm = item.get("flrGbCdNm", "-")
        flr_no_nm = item.get("flrNoNm", "-")
        strct_cd_nm = item.get("strctCdNm", "-")
        main_purps = item.get("mainPurpsCdNm", "-")
        etc_purps = item.get("etcPurps", "")
        area = item.get("area", "0")
        main_atch = item.get("mainAtchGbCdNm", "-")

        if dong_nm != current_dong:
            current_dong = dong_nm
            output.append(f"### 동: {dong_nm}")

        purps = etc_purps if etc_purps else main_purps
        output.append(f"- **{flr_gb_nm} {flr_no_nm}**: {purps}, {format_area(area)}, {strct_cd_nm}")

    if page_no < total_pages:
        output.append(f"\n※ 더 보려면 page_no={page_no + 1} 로 조회하세요.")

    return "\n".join(output)


def format_expos_result(result: dict, sigungu_cd: str, bjdong_cd: str, bun: str, ji: str) -> str:
    """전유부 조회 결과 포맷팅 - 세대별 정보"""
    if "error" in result:
        return f"오류: {result['error']}"

    total = result["totalCount"]
    page_no = result["pageNo"]
    num_of_rows = result["numOfRows"]
    total_pages = (total + num_of_rows - 1) // num_of_rows if total > 0 else 1

    output = ["## 건축물대장 전유부 조회 결과"]
    output.append(f"- 시군구코드: {sigungu_cd}, 법정동코드: {bjdong_cd}")
    if bun:
        output.append(f"- 번: {bun}, 지: {ji or '0000'}")
    output.append(f"- **총 {total}건 (page {page_no}/{total_pages})**\n")

    if not result["items"]:
        output.append("검색 결과가 없습니다.")
        return "\n".join(output)

    for i, item in enumerate(result["items"], 1):
        bld_nm = item.get("bldNm", "-")
        dong_nm = item.get("dongNm", "-")
        ho_nm = item.get("hoNm", "-")
        flr_gb_nm = item.get("flrGbCdNm", "-")
        flr_no = item.get("flrNo", "-")
        new_plat_plc = item.get("newPlatPlc", "-")

        output.append(f"### {i}. {bld_nm} {dong_nm}동 {ho_nm}")
        output.append(f"- **도로명주소**: {new_plat_plc}")
        output.append(f"- **층**: {flr_gb_nm} {flr_no}층")
        output.append("")

    if page_no < total_pages:
        output.append(f"\n※ 더 보려면 page_no={page_no + 1} 로 조회하세요.")

    return "\n".join(output)


def format_hsprc_result(result: dict, sigungu_cd: str, bjdong_cd: str, bun: str, ji: str) -> str:
    """주택가격 조회 결과 포맷팅"""
    if "error" in result:
        return f"오류: {result['error']}"

    total = result["totalCount"]
    page_no = result["pageNo"]
    num_of_rows = result["numOfRows"]
    total_pages = (total + num_of_rows - 1) // num_of_rows if total > 0 else 1

    output = ["## 건축물대장 주택가격 조회 결과"]
    output.append(f"- 시군구코드: {sigungu_cd}, 법정동코드: {bjdong_cd}")
    if bun:
        output.append(f"- 번: {bun}, 지: {ji or '0000'}")
    output.append(f"- **총 {total}건 (page {page_no}/{total_pages})**\n")

    if not result["items"]:
        output.append("검색 결과가 없습니다.")
        return "\n".join(output)

    for i, item in enumerate(result["items"], 1):
        bld_nm = item.get("bldNm", "-")
        new_plat_plc = item.get("newPlatPlc", "-")
        hsprc = item.get("hsprc", "0")
        std_day = item.get("stdDay", "")

        output.append(f"### {i}. {bld_nm}")
        output.append(f"- **도로명주소**: {new_plat_plc}")
        output.append(f"- **주택가격**: {format_price(hsprc)}")
        if std_day:
            output.append(f"- **기준일자**: {format_date(std_day)}")
        output.append("")

    if page_no < total_pages:
        output.append(f"\n※ 더 보려면 page_no={page_no + 1} 로 조회하세요.")

    return "\n".join(output)


def format_jijugu_result(result: dict, sigungu_cd: str, bjdong_cd: str, bun: str, ji: str) -> str:
    """지역지구구역 조회 결과 포맷팅"""
    if "error" in result:
        return f"오류: {result['error']}"

    total = result["totalCount"]
    page_no = result["pageNo"]
    num_of_rows = result["numOfRows"]
    total_pages = (total + num_of_rows - 1) // num_of_rows if total > 0 else 1

    output = ["## 건축물대장 지역지구구역 조회 결과"]
    output.append(f"- 시군구코드: {sigungu_cd}, 법정동코드: {bjdong_cd}")
    if bun:
        output.append(f"- 번: {bun}, 지: {ji or '0000'}")
    output.append(f"- **총 {total}건 (page {page_no}/{total_pages})**\n")

    if not result["items"]:
        output.append("검색 결과가 없습니다.")
        return "\n".join(output)

    for i, item in enumerate(result["items"], 1):
        new_plat_plc = item.get("newPlatPlc", "-")
        jijigu_gb_nm = item.get("jijiguGbCdNm", "-")
        jijigu_cd_nm = item.get("jijiguCdNm", "-")
        repr_yn = item.get("reprYn", "0")
        etc_jijigu = item.get("etcJijigu", "")

        repr_mark = "★ " if repr_yn == "1" else ""
        output.append(f"- {repr_mark}**{jijigu_gb_nm}**: {jijigu_cd_nm}")
        if etc_jijigu and etc_jijigu != jijigu_cd_nm:
            output.append(f"  - 상세: {etc_jijigu}")

    if page_no < total_pages:
        output.append(f"\n※ 더 보려면 page_no={page_no + 1} 로 조회하세요.")

    return "\n".join(output)


def call_api(operation: str, params: dict) -> dict:
    """건축물대장 API 호출"""
    api_key = os.environ.get("DATA_GO_KR_API_KEY")
    if not api_key:
        return {"error": "DATA_GO_KR_API_KEY 환경변수가 설정되지 않았습니다."}

    # serviceKey는 별도로 처리 (인코딩하지 않음)
    encoded_params = urllib.parse.urlencode(params)
    path = f"/1613000/BldRgstHubService/{operation}?serviceKey={api_key}&{encoded_params}"

    try:
        conn = http.client.HTTPSConnection("apis.data.go.kr", timeout=30)
        conn.request("GET", path, headers={
            "User-Agent": "Mozilla/5.0 (compatible; BuildingRegisterBot/1.0)",
            "Accept": "*/*"
        })
        response = conn.getresponse()

        if response.status != 200:
            return {"error": f"HTTP 오류: {response.status} - {response.reason}"}

        xml_text = response.read().decode("utf-8")
        conn.close()
        return parse_xml_response(xml_text)
    except http.client.HTTPException as e:
        return {"error": f"HTTP 오류: {e}"}
    except Exception as e:
        return {"error": f"오류: {e}"}


@mcp.tool()
def search_building_basic(
    sigungu_cd: str,
    bjdong_cd: str,
    bun: str = "",
    ji: str = "",
    plat_gb_cd: str = "0",
    num_of_rows: int = 10,
    page_no: int = 1
) -> str:
    """
    건축물대장 기본개요 조회 - 건축물 기본 정보 (대장구분, 지번/도로명주소, 지역지구구역)

    Args:
        sigungu_cd: 시군구코드 5자리 (예: "11680" 강남구)
        bjdong_cd: 법정동코드 5자리 (예: "10300" 개포동)
            - 행정표준코드관리시스템(code.go.kr)에서 확인 가능
        bun: 번 4자리 (예: "0012") - 옵션
        ji: 지 4자리 (예: "0000") - 옵션
        plat_gb_cd: 대지구분코드 (0: 대지, 1: 산, 2: 블록) - 기본값 "0"
        num_of_rows: 한 페이지에 표시할 건수 (기본: 10, 최대: 100)
        page_no: 페이지 번호 (기본: 1)

    Returns:
        건축물 기본개요 목록 (건물명, 주소, 대장구분, 지역지구구역 등)
    """
    params = {
        "sigunguCd": sigungu_cd,
        "bjdongCd": bjdong_cd,
        "platGbCd": plat_gb_cd,
        "numOfRows": str(min(100, max(1, num_of_rows))),
        "pageNo": str(max(1, page_no)),
    }
    if bun:
        params["bun"] = bun.zfill(4)
    if ji:
        params["ji"] = ji.zfill(4)

    result = call_api(OPERATIONS["기본개요"], params)
    return format_basis_result(result, sigungu_cd, bjdong_cd, bun, ji)


@mcp.tool()
def search_building_recap_title(
    sigungu_cd: str,
    bjdong_cd: str,
    bun: str = "",
    ji: str = "",
    plat_gb_cd: str = "0",
    num_of_rows: int = 10,
    page_no: int = 1
) -> str:
    """
    건축물대장 총괄표제부 조회 - 단지 전체 정보 (대지면적, 연면적, 세대수, 사용승인일 등)

    ⭐ 재건축 판단 시 가장 중요한 정보:
    - 사용승인일 → 건축연수 계산 (30년 이상이면 재건축 대상 가능)
    - 세대수, 연면적, 용적률 → 사업성 판단

    Args:
        sigungu_cd: 시군구코드 5자리 (예: "11680" 강남구)
        bjdong_cd: 법정동코드 5자리 (예: "10300" 개포동)
        bun: 번 4자리 (예: "0012") - 옵션
        ji: 지 4자리 (예: "0000") - 옵션
        plat_gb_cd: 대지구분코드 (0: 대지, 1: 산, 2: 블록) - 기본값 "0"
        num_of_rows: 한 페이지에 표시할 건수 (기본: 10, 최대: 100)
        page_no: 페이지 번호 (기본: 1)

    Returns:
        총괄표제부 정보 (사용승인일, 대지면적, 건축면적, 연면적, 건폐율, 용적률, 세대수 등)
    """
    params = {
        "sigunguCd": sigungu_cd,
        "bjdongCd": bjdong_cd,
        "platGbCd": plat_gb_cd,
        "numOfRows": str(min(100, max(1, num_of_rows))),
        "pageNo": str(max(1, page_no)),
    }
    if bun:
        params["bun"] = bun.zfill(4)
    if ji:
        params["ji"] = ji.zfill(4)

    result = call_api(OPERATIONS["총괄표제부"], params)
    return format_recap_title_result(result, sigungu_cd, bjdong_cd, bun, ji)


@mcp.tool()
def search_building_title(
    sigungu_cd: str,
    bjdong_cd: str,
    bun: str = "",
    ji: str = "",
    plat_gb_cd: str = "0",
    num_of_rows: int = 10,
    page_no: int = 1
) -> str:
    """
    건축물대장 표제부 조회 - 동별 상세 정보 (구조, 용도, 층수, 면적, 승강기, 내진설계 등)

    Args:
        sigungu_cd: 시군구코드 5자리 (예: "11680" 강남구)
        bjdong_cd: 법정동코드 5자리 (예: "10300" 개포동)
        bun: 번 4자리 (예: "0012") - 옵션
        ji: 지 4자리 (예: "0000") - 옵션
        plat_gb_cd: 대지구분코드 (0: 대지, 1: 산, 2: 블록) - 기본값 "0"
        num_of_rows: 한 페이지에 표시할 건수 (기본: 10, 최대: 100)
        page_no: 페이지 번호 (기본: 1)

    Returns:
        표제부 정보 (동명칭, 구조, 지붕, 용도, 면적, 층수, 높이, 승강기, 내진설계 등)
    """
    params = {
        "sigunguCd": sigungu_cd,
        "bjdongCd": bjdong_cd,
        "platGbCd": plat_gb_cd,
        "numOfRows": str(min(100, max(1, num_of_rows))),
        "pageNo": str(max(1, page_no)),
    }
    if bun:
        params["bun"] = bun.zfill(4)
    if ji:
        params["ji"] = ji.zfill(4)

    result = call_api(OPERATIONS["표제부"], params)
    return format_title_result(result, sigungu_cd, bjdong_cd, bun, ji)


@mcp.tool()
def search_building_floor(
    sigungu_cd: str,
    bjdong_cd: str,
    bun: str = "",
    ji: str = "",
    plat_gb_cd: str = "0",
    num_of_rows: int = 50,
    page_no: int = 1
) -> str:
    """
    건축물대장 층별개요 조회 - 층별 구조, 용도, 면적 정보

    Args:
        sigungu_cd: 시군구코드 5자리 (예: "11680" 강남구)
        bjdong_cd: 법정동코드 5자리 (예: "10300" 개포동)
        bun: 번 4자리 (예: "0012") - 옵션
        ji: 지 4자리 (예: "0000") - 옵션
        plat_gb_cd: 대지구분코드 (0: 대지, 1: 산, 2: 블록) - 기본값 "0"
        num_of_rows: 한 페이지에 표시할 건수 (기본: 50, 최대: 100)
        page_no: 페이지 번호 (기본: 1)

    Returns:
        층별개요 정보 (동명칭, 층구분, 층번호, 구조, 용도, 면적)
    """
    params = {
        "sigunguCd": sigungu_cd,
        "bjdongCd": bjdong_cd,
        "platGbCd": plat_gb_cd,
        "numOfRows": str(min(100, max(1, num_of_rows))),
        "pageNo": str(max(1, page_no)),
    }
    if bun:
        params["bun"] = bun.zfill(4)
    if ji:
        params["ji"] = ji.zfill(4)

    result = call_api(OPERATIONS["층별개요"], params)
    return format_floor_result(result, sigungu_cd, bjdong_cd, bun, ji)


@mcp.tool()
def search_building_expos(
    sigungu_cd: str,
    bjdong_cd: str,
    bun: str = "",
    ji: str = "",
    dong_nm: str = "",
    ho_nm: str = "",
    plat_gb_cd: str = "0",
    num_of_rows: int = 30,
    page_no: int = 1
) -> str:
    """
    건축물대장 전유부 조회 - 집합건물(아파트 등)의 세대별 정보

    Args:
        sigungu_cd: 시군구코드 5자리 (예: "11680" 강남구)
        bjdong_cd: 법정동코드 5자리 (예: "10300" 개포동)
        bun: 번 4자리 (예: "0012") - 옵션
        ji: 지 4자리 (예: "0000") - 옵션
        dong_nm: 동명칭 (예: "101") - 옵션
        ho_nm: 호명칭 (예: "101호") - 옵션
        plat_gb_cd: 대지구분코드 (0: 대지, 1: 산, 2: 블록) - 기본값 "0"
        num_of_rows: 한 페이지에 표시할 건수 (기본: 30, 최대: 100)
        page_no: 페이지 번호 (기본: 1)

    Returns:
        전유부 정보 (건물명, 동명칭, 호명칭, 층정보)
    """
    params = {
        "sigunguCd": sigungu_cd,
        "bjdongCd": bjdong_cd,
        "platGbCd": plat_gb_cd,
        "numOfRows": str(min(100, max(1, num_of_rows))),
        "pageNo": str(max(1, page_no)),
    }
    if bun:
        params["bun"] = bun.zfill(4)
    if ji:
        params["ji"] = ji.zfill(4)
    if dong_nm:
        params["dongNm"] = dong_nm
    if ho_nm:
        params["hoNm"] = ho_nm

    result = call_api(OPERATIONS["전유부"], params)
    return format_expos_result(result, sigungu_cd, bjdong_cd, bun, ji)


@mcp.tool()
def search_building_price(
    sigungu_cd: str,
    bjdong_cd: str,
    bun: str = "",
    ji: str = "",
    plat_gb_cd: str = "0",
    num_of_rows: int = 30,
    page_no: int = 1
) -> str:
    """
    건축물대장 주택가격 조회 - 공시가격 정보

    Args:
        sigungu_cd: 시군구코드 5자리 (예: "11680" 강남구)
        bjdong_cd: 법정동코드 5자리 (예: "10300" 개포동)
        bun: 번 4자리 (예: "0012") - 옵션
        ji: 지 4자리 (예: "0000") - 옵션
        plat_gb_cd: 대지구분코드 (0: 대지, 1: 산, 2: 블록) - 기본값 "0"
        num_of_rows: 한 페이지에 표시할 건수 (기본: 30, 최대: 100)
        page_no: 페이지 번호 (기본: 1)

    Returns:
        주택가격 정보 (건물명, 주소, 주택가격, 기준일자)
    """
    params = {
        "sigunguCd": sigungu_cd,
        "bjdongCd": bjdong_cd,
        "platGbCd": plat_gb_cd,
        "numOfRows": str(min(100, max(1, num_of_rows))),
        "pageNo": str(max(1, page_no)),
    }
    if bun:
        params["bun"] = bun.zfill(4)
    if ji:
        params["ji"] = ji.zfill(4)

    result = call_api(OPERATIONS["주택가격"], params)
    return format_hsprc_result(result, sigungu_cd, bjdong_cd, bun, ji)


@mcp.tool()
def search_building_zone(
    sigungu_cd: str,
    bjdong_cd: str,
    bun: str = "",
    ji: str = "",
    plat_gb_cd: str = "0",
    num_of_rows: int = 30,
    page_no: int = 1
) -> str:
    """
    건축물대장 지역지구구역 조회 - 용도지역/지구/구역 정보

    Args:
        sigungu_cd: 시군구코드 5자리 (예: "11680" 강남구)
        bjdong_cd: 법정동코드 5자리 (예: "10300" 개포동)
        bun: 번 4자리 (예: "0012") - 옵션
        ji: 지 4자리 (예: "0000") - 옵션
        plat_gb_cd: 대지구분코드 (0: 대지, 1: 산, 2: 블록) - 기본값 "0"
        num_of_rows: 한 페이지에 표시할 건수 (기본: 30, 최대: 100)
        page_no: 페이지 번호 (기본: 1)

    Returns:
        지역지구구역 정보 (용도지역, 용도지구, 용도구역 등)
    """
    params = {
        "sigunguCd": sigungu_cd,
        "bjdongCd": bjdong_cd,
        "platGbCd": plat_gb_cd,
        "numOfRows": str(min(100, max(1, num_of_rows))),
        "pageNo": str(max(1, page_no)),
    }
    if bun:
        params["bun"] = bun.zfill(4)
    if ji:
        params["ji"] = ji.zfill(4)

    result = call_api(OPERATIONS["지역지구구역"], params)
    return format_jijugu_result(result, sigungu_cd, bjdong_cd, bun, ji)


@mcp.tool()
def get_building_operations() -> str:
    """
    건축물대장 API에서 조회 가능한 오퍼레이션 목록

    Returns:
        조회 가능한 오퍼레이션 목록 및 설명
    """
    output = ["## 건축물대장 조회 가능 오퍼레이션\n"]

    descriptions = {
        "기본개요": "건축물 기본 정보 (대장구분, 지번/도로명주소, 지역지구구역)",
        "총괄표제부": "⭐ 단지 전체 정보 (사용승인일, 대지면적, 연면적, 세대수, 용적률) - 재건축 판단 핵심",
        "표제부": "동별 상세 정보 (구조, 용도, 층수, 면적, 승강기, 내진설계)",
        "층별개요": "층별 구조, 용도, 면적 정보",
        "부속지번": "건축물 관련 부속지번 정보",
        "전유공용면적": "전유/공용 면적 상세 정보",
        "오수정화시설": "오수정화시설 형식, 용량 정보",
        "주택가격": "공동주택 공시가격 정보",
        "전유부": "집합건물 세대별 정보 (동/호명칭, 층)",
        "지역지구구역": "용도지역, 용도지구, 용도구역 정보",
    }

    for op_name, api_name in OPERATIONS.items():
        desc = descriptions.get(op_name, "")
        output.append(f"### {op_name}")
        output.append(f"- API: `{api_name}`")
        output.append(f"- 설명: {desc}\n")

    output.append("---")
    output.append("### 필수 파라미터")
    output.append("- **sigungu_cd**: 시군구코드 5자리 (예: 11680 강남구)")
    output.append("- **bjdong_cd**: 법정동코드 5자리 (예: 10300 개포동)")
    output.append("")
    output.append("### 선택 파라미터")
    output.append("- **bun**: 번 4자리 (예: 0012)")
    output.append("- **ji**: 지 4자리 (예: 0000)")
    output.append("- **plat_gb_cd**: 대지구분코드 (0:대지, 1:산, 2:블록)")
    output.append("")
    output.append("### 코드 조회")
    output.append("- 시군구코드/법정동코드: [행정표준코드관리시스템](https://www.code.go.kr)")
    output.append("- 법정동코드목록조회 메뉴에서 확인 가능")

    return "\n".join(output)


if __name__ == "__main__":
    mcp.run()
