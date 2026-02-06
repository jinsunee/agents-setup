#!/usr/bin/env python3
"""
국가법령정보 Open API MCP 서버
법령, 행정규칙, 자치법규, 조약 등 법률 정보 검색
"""

import os
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# 환경 변수 로드 (.env)
load_dotenv()

mcp = FastMCP("korea-law")

API_BASE_URL = "https://apis.data.go.kr/1170000/law"

# 각 서비스별 엔드포인트 (.do 확장자 필수)
ENDPOINTS = {
    "law": "/lawSearchList.do",
    "admrul": "/admrulSearchList.do",
    "ordin": "/ordinSearchList.do",
    "trty": "/trtySearchList.do",
    "expc": "/expcSearchList.do",
    "detc": "/detcSearchList.do",
    "licbyl": "/licbylSearchList.do",
    "lstrm": "/lstrmSearchList.do",
}

TARGETS = {
    "law": "법령정보",
    "admrul": "행정규칙정보",
    "ordin": "자치법규정보",
    "trty": "조약정보",
    "expc": "법령해석례정보",
    "detc": "헌재결정례정보",
    "licbyl": "별표서식정보",
    "lstrm": "법령용어정보",
}

# 각 타입별 주요 필드
TITLE_FIELDS = {
    "law": "법령명한글",
    "admrul": "행정규칙명",
    "ordin": "자치법규명",
    "trty": "조약명",
    "expc": "해석례명",
    "detc": "사건명",
    "licbyl": "별표명",
    "lstrm": "용어명",
}


def parse_xml_response(xml_text: str, target: str) -> dict:
    """XML 응답을 파싱하여 딕셔너리로 반환"""
    try:
        root = ET.fromstring(xml_text)

        # 결과 코드 확인
        result_code = root.findtext(".//resultCode", "")
        result_msg = root.findtext(".//resultMsg", "")
        total_cnt = root.findtext(".//totalCnt", "0")

        result = {
            "resultCode": result_code,
            "resultMsg": result_msg,
            "totalCnt": total_cnt,
            "items": []
        }

        # 에러 체크
        if result_code and result_code != "00":
            error_msgs = {
                "01": "요청 파라미터 값이 잘못되었습니다",
                "02": "인증키가 누락되었거나 유효하지 않습니다",
                "03": "필수 파라미터가 설정되지 않았습니다",
                "09": "시스템 오류가 발생했습니다",
                "99": "시스템 오류가 발생했습니다",
            }
            result["error"] = error_msgs.get(result_code, f"알 수 없는 오류 (코드: {result_code})")
            return result

        # 항목들 파싱
        for item in root.iter():
            if item.tag == target:
                item_dict = {}
                for child in item:
                    if child.text:
                        item_dict[child.tag] = child.text.strip()
                if item_dict:
                    result["items"].append(item_dict)

        return result
    except ET.ParseError as e:
        return {"error": f"XML 파싱 오류: {e}", "raw": xml_text[:500]}


def format_result(result: dict, target: str, query: str) -> str:
    """결과를 마크다운 형식으로 포맷팅"""
    if "error" in result:
        return f"오류: {result['error']}"

    title_field = TITLE_FIELDS.get(target, "제목")
    output = [f"## {TARGETS[target]} 검색 결과"]
    output.append(f"검색어: {query}")
    output.append(f"총 {result['totalCnt']}건\n")

    if not result["items"]:
        output.append("검색 결과가 없습니다.")
        return "\n".join(output)

    for i, item in enumerate(result["items"], 1):
        # 제목 추출
        title = item.get(title_field, "제목없음")
        output.append(f"### {i}. {title}")

        # 주요 필드 우선 출력
        priority_fields = ["시행일자", "공포일자", "소관부처명", "법령상세링크"]
        for field in priority_fields:
            if field in item and field != title_field:
                output.append(f"- {field}: {item[field]}")

        # 나머지 필드 출력
        for key, value in item.items():
            if key not in [title_field] + priority_fields:
                output.append(f"- {key}: {value}")
        output.append("")

    return "\n".join(output)


@mcp.tool()
def search_law(
    query: str,
    target: str = "law",
    num_of_rows: int = 10,
    page_no: int = 1
) -> str:
    """
    국가법령정보 검색

    Args:
        query: 검색어 (예: "개인정보보호법", "근로기준법", "건축법")
        target: 검색 대상
            - law: 법령정보 (법률, 대통령령, 총리령 등)
            - admrul: 행정규칙정보 (훈령, 예규, 고시 등)
            - ordin: 자치법규정보 (조례, 규칙)
            - trty: 조약정보
            - expc: 법령해석례정보
            - detc: 헌재결정례정보
            - licbyl: 별표서식정보
            - lstrm: 법령용어정보
        num_of_rows: 한 페이지 결과 수 (기본: 10, 최대: 100)
        page_no: 페이지 번호 (기본: 1)

    Returns:
        검색 결과 (법령명, 시행일자, 공포일자, 소관부처, 상세링크 등)
    """
    api_key = os.environ.get("KOREA_LAW_API_KEY")
    if not api_key:
        return "오류: KOREA_LAW_API_KEY 환경변수가 설정되지 않았습니다."

    if target not in TARGETS:
        return f"오류: 잘못된 target 값입니다. 가능한 값: {', '.join(TARGETS.keys())}"

    endpoint = ENDPOINTS[target]
    # 쿼리 파라미터는 개별 인코딩 (serviceKey는 소문자)
    params = urllib.parse.urlencode({
        "serviceKey": api_key,
        "target": target,
        "query": query,
        "numOfRows": num_of_rows,
        "pageNo": page_no,
    }, quote_via=urllib.parse.quote)

    url = f"{API_BASE_URL}{endpoint}?{params}"

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=30) as response:
            xml_text = response.read().decode("utf-8")
            result = parse_xml_response(xml_text, target)
            return format_result(result, target, query)

    except urllib.error.HTTPError as e:
        return f"HTTP 오류: {e.code} - {e.reason}"
    except urllib.error.URLError as e:
        return f"네트워크 오류: {e.reason}"
    except Exception as e:
        return f"오류 발생: {e}"


@mcp.tool()
def list_law_targets() -> str:
    """사용 가능한 법령 검색 대상(target) 목록 및 설명 조회"""
    output = ["## 검색 가능한 법령 정보 유형\n"]
    descriptions = {
        "law": "현행 법률, 대통령령, 총리령, 부령 등",
        "admrul": "훈령, 예규, 고시 등 행정규칙",
        "ordin": "지방자치단체 조례, 규칙",
        "trty": "국제 조약 정보",
        "expc": "법령해석례 (법제처 해석)",
        "detc": "헌법재판소 결정례",
        "licbyl": "법령 별표/서식 (HWP, PDF 다운로드 가능)",
        "lstrm": "법령에서 사용되는 용어 정의",
    }
    for key, value in TARGETS.items():
        output.append(f"- `{key}`: {value}")
        output.append(f"  - {descriptions.get(key, '')}")
    return "\n".join(output)


if __name__ == "__main__":
    mcp.run()
