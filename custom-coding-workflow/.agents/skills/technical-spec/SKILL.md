---
name: technical-spec
description: PRD를 기반으로 상세 기술 명세서(technical-spec.md)를 작성. 아키텍처, API 설계, 행동 정의, 테스트 전략을 포함.
argument-hint: "[PRD 폴더 경로 (optional)]"
---

# Technical Specification

## Overview

PRD의 "무엇을"을 "어떻게" 구현할지 상세화하는 기술 명세서를 작성한다. Brainstorming 방식으로 섹션별 질문을 통해 함께 완성한다.

**Announce at start:** "I'm using the technical-spec skill to create a detailed technical specification."

**Output location:** `docs/features/[feature-name]_[date]/technical-spec.md` (PRD와 같은 폴더)

## Workflow

### Step 1: PRD 선택

- `$ARGUMENTS`에 경로가 있으면 → 해당 폴더의 `prd.md` 읽기
- `$ARGUMENTS`가 비어있으면 → `docs/features/` 내 폴더 목록 표시 후 선택 요청

### Step 2: PRD 분석

1. `prd.md` 읽고 핵심 내용 파악
2. 기존 코드베이스 구조 확인 (관련 파일, 모듈)
3. 사용자에게 PRD 이해 확인: "PRD를 이렇게 이해했는데 맞나요?"

### Step 3: 섹션별 작성 (Brainstorming Style)

각 섹션마다:
- **한 번에 하나의 질문**만 한다
- **선택지 제공**을 선호한다 (가능할 때)
- 섹션 초안 작성 후 **피드백 요청**
- 승인 후 다음 섹션으로 진행

#### 3-1. 목적

```markdown
## 1. 목적

[PRD의 목적/문제 정의를 개발자 관점으로 요약]

**변경 전:** [현재 사용자 경험/시스템 행동]
**변경 후:** [구현 후 달라질 점]
```

- PRD 목적을 구현 관점으로 재해석
- 사용자 경험/시스템 행동 중심으로 작성

#### 3-2. 해결 (아키텍처/인터페이스 설계)

```markdown
## 2. 해결

### 2.1 아키텍처 개요

- [주요 컴포넌트/모듈 2-5개]
- [데이터 흐름]
- [외부 시스템/서비스 연동]
- [공통 유틸 재사용 여부]

### 2.2 API / 인터페이스 설계

#### `[METHOD] /path/to/endpoint`

- **Path Params:** ...
- **Query Params:** ...
- **Request Body:** ...
- **Response:** ...
- **Error Codes:** ...

### 2.3 데이터 모델 / 상태 (필요 시)

- [영향받는 테이블/컬럼]
- [새로운 enum/상태값]
- [상태 전이 다이어그램 (필요 시)]
```

질문 예시:
- "아키텍처 접근 방식으로 A, B, C 중 어떤 것이 좋을까요?"
- "기존 모듈 X를 재사용할까요, 새로 만들까요?"

#### 3-3. 행동 정의 (Behavior & Edge Cases)

```markdown
## 3. 행동 정의

### 3.1 주요 시나리오

#### 시나리오 1: [시나리오명]

- **Given:** [사전 조건]
- **When:** [사용자/시스템 액션]
- **Then:** [기대 결과]

### 3.2 Edge Cases

| 케이스 | 기대 동작 | 분류 |
|--------|----------|------|
| [에러 상황] | [동작] | MUST |
| [극단 값] | [동작] | SHOULD |
| [권한 없음] | [동작] | MUST NOT |
```

- 최소 3-5개 핵심 시나리오 포함
- Given/When/Then 형식 사용
- Edge Case는 MUST/SHOULD/MUST NOT 분류

#### 3-4. 테스트 전략

```markdown
## 4. 테스트 전략

### 5.1 테스트 시나리오

#### 시나리오 1: [시나리오명] → [E2E/Integration/Unit]

**호출/조작:**
- [테스트 액션]

**검증:**
- [검증 항목]

### 5.2 테스트 레벨 배치

| 시나리오 | 테스트 레벨 | 이유 |
|---------|------------|------|
| 시나리오 1, 2 | E2E | 전체 플로우 검증 |
| 시나리오 3 | Integration | 모듈 간 연동 |
| 핵심 로직 | Unit | 비즈니스 로직 |
```

- 행동 정의(3.1)의 시나리오와 1:1 매핑
- 각 시나리오별 테스트 레벨 명시

#### 3-5. 리스크 분석

```markdown
## 5. 리스크 분석

### 비용

- [API 호출량 증가 예상]
- [외부 서비스 과금]
- [스토리지/캐시 사용량]
- 해당 없음: [해당 없는 경우 그 이유 명시]

### 영향 범위

- [기존 API/화면 영향]
- [DB 스키마 변경 리스크]
- [설정/환경변수 변경]
- 해당 없음: [해당 없는 경우 그 이유 명시]
```

- 각 항목이 해당되지 않으면 "해당 없음"과 함께 이유를 명시한다
- 예: "해당 없음: 외부 API 호출 없이 로컬 처리만 수행"

#### 3-6. 오픈 이슈 & 결정 필요 사항

```markdown
## 6. 오픈 이슈 & 결정 필요 사항

| 이슈 | 선택지 | 추천 | 결정 |
|-----|-------|-----|-----|
| [미결정 사항] | A, B, C | B | TBD |
```

- Spec Review PR에서 리뷰어가 확인할 항목
- 구현 시 선택해야 할 옵션

### Step 4: 문서 저장 및 완료

1. `technical-spec.md` 저장
2. 완료 보고:

```
Technical specification complete!

Created:
  docs/features/[name]_[date]/
    ├── prd.md
    └── technical-spec.md

Next step: /writing-plans docs/features/[name]_[date]
```

## Key Principles

- **한 번에 하나의 질문** - 여러 질문으로 압도하지 않음
- **선택지 제공** - 가능하면 multiple choice
- **섹션별 피드백** - 각 섹션 승인 후 다음으로
- **PRD와 일관성** - PRD 내용과 모순되지 않게
- **테스트-행동 매핑** - 행동 정의와 테스트 시나리오 1:1 대응
- **구체적 수치** - "빠르게" 대신 "200ms 이내"

## Integration

**이전 skill:** `feature-planning` 또는 `prd`에서 호출

**다음 skill:** `/writing-tasks` - Plan을 2-5분 단위 task로 분해
