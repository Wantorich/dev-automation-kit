
# 🧠 GPT 기반 포트폴리오 자동화 프로젝트

이 프로젝트는 GitLab에 기록된 커밋 내용을 자동으로 분석하여, 기술 포트폴리오 문서를 작성하는 자동화 도구입니다.  
GPT-4o 모델을 활용하여 커밋 내용을 요약하고, 마크다운 형식의 기술 문서를 생성합니다.

---

## 📌 주요 기능

### 1. 커밋 수집
- GitLab API를 통해 특정 브랜치의 커밋 목록을 최신순이 아닌 **과거 → 최신순**으로 가져옵니다.
- 커밋은 특정 작성자(author_name) 기준으로 필터링할 수 있습니다.
- 10개의 마크다운 파일을 만들도록 적절히 커밋을 분할하여 처리합니다.

### 2. GPT 요약 요청
- 커밋 메시지 + diff를 바탕으로, **10개 단위로 묶어 GPT에 요약 요청**을 보냅니다.
- `gpt-4o` 모델 혹은 `gpt-4o-mini`을 사용하여 비용 대비 효율적인 응답을 확보합니다.
- 요약된 결과는 `summary_batch_N.md`로 저장됩니다.

### 3. 기술 포트폴리오 문서 생성
- 생성된 batch 파일들을 기반으로 GPT에게 **기술 중심 보고서 형식의 포트폴리오 챕터**를 작성하도록 지시합니다.
- 커밋 내역을 바탕으로 GPT가 직접 **핵심 주제를 도출**하고, 아래와 같은 구성으로 자세히 작성합니다:
  - 기능 개요
  - 설계 및 구조
  - 기술 선택 이유
  - 구현 및 리팩토링
  - 트러블슈팅
  - 개선 효과
  - 전체 성과 요약

---

## 🧩 기술 스택

- Python 3.x
- GitLab REST API
- OpenAI API (GPT-4o 사용)
- Markdown2
- dotenv (환경 변수 관리)

---

## 🧪 사용 방법

### `.env` 파일 생성 및 API Key 설정:

```
GITLAB_TOKEN=...
GITLAB_HOST=lab.ssafy.com
PROJECT_ID=...
AUTHOR_NAME=최효재
BRANCH=be
OPENAI_API_KEY=sk-...
```

### GitLab Personal Access Token 발급

-  `https://lab.ssafy.com/-/profile/personal_access_tokens` 접속  
-  `read_api`, `read_repository` 권한 포함한 토큰 생성  

### project Id 설정
- gitlab setting -> general -> project ID 확인
- PROJECT_ID 부분에 값 할당


## 실행 방법

```bash
# 가상환경 생성
python -m venv .venv

# 가상환경 활성화
source .venv\\Scripts\\activate # Window
# source .venv/bin/activate   # not Window

# 필요 패키지 설치
pip install -r requirements.txt

# python 실행
python main.py
```

## 결과 확인

- `progress.log` : 현재 진행상황 로그 확인
- `summary_batch_*.md`: 각 커밋 요약
- `portfolio.md`, `portfolio.pdf`: 전체 포트폴리오 기술 문서

---

## 🧠 GPT 요청 제한과 토큰 정보

- GPT API는 **입력 + 출력 토큰 총량**으로 제한됩니다.
- `gpt-4o`는 최대 128,000 tokens까지 지원하므로, 긴 응답에도 유리합니다.
- 요청 시 `max_tokens`로 응답 최대 길이를 조정할 수 있습니다.

---

## 📄 결과물 예시

- `summary_batch_1.md ~ 10.md`: 커밋 기반 요약 마크다운
- `portfolio.md`: 기술 챕터 방식의 포트폴리오 문서

---

## 유의 사항

- result 폴더 밑의 `summary_batch_1.md ~ 10.md`은 새로운 명령어를 실행할때 삭제되므로 적절한 백업하길 권장드립니다.
- `summary_batch_1.md ~ 10.md`과 prompt 폴더의 `portfolio_summary.txt`를 GPT 홈페이지에서 **심층 리서치** 기능을 활용하면 더욱 풍부한 보고서를 얻을 수 있습니다.
- **일반적으로 한번 실행할때 1~2$ 정도의 비용이 청구됩니다.**

---

## 🪪 라이센스

이 프로젝트는 MIT 라이선스를 따릅니다.
