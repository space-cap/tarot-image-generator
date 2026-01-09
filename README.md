# 🔮 Tarot Image Generator

> **Google Gemini API를 활용한 타로 카드 자동 이미지 생성 도구**

[![Python Version](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/)
[![Package Manager](https://img.shields.io/badge/manager-uv-green.svg)](https://github.com/astral-sh/uv)

이 프로젝트는 Google의 **Gemini 2.5 Flash Image Preview** 모델을 사용하여 78장의 타로 카드 덱 전체를 자동으로 생성합니다. 상세한 프롬프트 설정을 통해 일관성 있고 아름다운 타로 카드 에셋을 구축할 수 있습니다.

## ✨ 주요 기능

-   **자동화**: 메이저(22장) 및 마이너(56장) 아르카나 전체 자동 생성.
-   **안정성**: 무료 티어 API의 할당량 제한(Rate Limit) 자동 대기 및 재시도 로직 포함.
-   **유연성**: `tarot_prompts.json` 수정을 통한 커스텀 디자인 가능.
-   **보안**: 환경 변수(`.env`) 기반의 API 키 관리.

## 🚀 빠른 시작 (Quick Start)

### 1. 요구 사항
-   Python 3.13 이상
-   [uv](https://github.com/astral-sh/uv) 패키지 매니저 권장

### 2. 설정
```bash
# 의존성 설치
uv sync

# 설정 파일 복사
cp .env.example .env

# .env 파일에 GEMINI_API_KEY 입력
```

### 3. 실행
```bash
uv run python generate_tarot_assets.py
```

## 📂 프로젝트 구조

-   `generate_tarot_assets.py`: 메인 생성 스크립트.
-   `tarot_prompts.json`: 카드별 디자인 프롬프트 데이터.
-   `docs/USER_MANUAL.md`: **[상세 사용 설명 가이드](docs/USER_MANUAL.md)**.
-   `assets/cards/`: 생성된 이미지가 저장되는 디렉토리 (자동 생성).

## 📖 문서화
더 자세한 설정 및 실행 방법은 [사용 설명서(User Manual)](docs/USER_MANUAL.md)를 참고해 주세요.

---
*Disclaimer: 본 프로젝트는 이미지 생성을 위해 Google Gemini API를 사용하며, API 사용량에 따라 요금이 발생하거나 할당량이 제한될 수 있습니다.*
