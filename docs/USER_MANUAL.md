# 타로 이미지 생성기 (Tarot Image Generator) 사용 설명서

이 프로젝트는 Google Gemini API(Flash Image Preview)를 사용하여 타로 카드 덱 전체 이미지를 자동으로 생성하는 도구입니다.

## 1. 사전 준비 (Prerequisites)

- **Python**: 3.13 이상이 필요합니다.
- **uv**: 패키지 및 환경 관리를 위해 `uv` 사용을 권장합니다.
- **Gemini API Key**: [Google AI Studio](https://aistudio.google.com/)에서 API 키를 발급받아야 합니다.

## 2. 설치 및 설정 (Setup)

### 패키지 설치
`uv`를 사용하여 필요한 의존성을 설치합니다.
```bash
uv sync
```

### 환경 변수 설정
프로젝트 루트 디렉토리에 `.env` 파일을 생성하고 발급받은 API 키를 입력합니다. `.env.example` 파일을 복사하여 사용할 수 있습니다.

```bash
cp .env.example .env
```

`.env` 파일 내용:
```text
GEMINI_API_KEY="여러분의_API_키_여기에_입력"
```

## 3. 실행 방법 (Usage)

이미지 생성을 시작하려면 다음 명령어를 실행하세요.

```bash
uv run python generate_tarot_assets.py
```

### 실행 프로세스
1. `.env` 파일에서 API 키를 로드합니다.
2. `tarot_prompts.json` 파일에서 카드별 프롬프트 데이터를 읽어옵니다.
3. 메이저 아르카나(22장) → 마이너 아르카나(56장) 순서로 이미지를 생성합니다.
4. 생성된 이미지는 `assets/cards/` 폴더 내에 저장됩니다.

> [!NOTE]
> 무료 티어 API 사용 시 Quota 제한(429 Error)이 발생할 수 있습니다. 스크립트에는 자동으로 대기 후 재시도하는 로직이 포함되어 있습니다.

## 4. 파일 구조
- `generate_tarot_assets.py`: 메인 실행 스크립트
- `tarot_prompts.json`: 각 카드 제작을 위한 상세 프롬프트 데이터
- `assets/cards/`: 생성된 결과물 파일이 저장되는 곳 (Git 제외 대상)
- `docs/`: 프로젝트 문서 관리 폴더

## 5. 주의 사항
- 생성된 이미지는 `assets/cards/` 폴더에 누적됩니다. 
- API 키는 절대 Git에 커밋하지 마세요. (현재 `.gitignore`에 자동 포함되어 있습니다.)
