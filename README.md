# 🛠️ AI 자동화 스크립트 모음집

이 저장소는 **개발 생산성을 높이기 위한 자동화 스크립트 3종**을 제공합니다.  
GitLab Merge Request(MR) 설명 자동 생성기와 YouTube 자막 다운로드기 두 가지 유틸리티를 통해, 반복 작업을 줄이고 더 중요한 일에 집중하세요!

---

## 📁 프로젝트 구조

```
.
├── gitlab_mr_create/             # GitLab MR 설명 자동 생성기 디렉토리
│   ├── generate_mr.sh
│   ├── templates/
│   ├── credentials/
│   ├── mr_description.md
│   └── payload.json
├── youtube_subtitle_download/   # YouTube 자막 다운로드기 디렉토리
│   ├── download_subs.py
│   └── video_urls.txt
├── portfolio/                    # GitLab 커밋 기반 포트폴리오 생성기
│   ├── main.py
│   ├── summarize_portfolio.py
│   ├── batch_markdown.py
│   ├── precheck.py
│   ├── .env
│   ├── requirements.txt
│   ├── result/
│   ├── prompt/
│   └── portfolio/
└── README.md                     # 🧾 현재 문서
```

---

## 📦 포함 스크립트

### 1. 🧠 GitLab MR 설명 자동 생성기 (`gitlab_mr_create/`)

GitLab 커밋 메시지와 diff를 기반으로 GPT 모델을 활용하여 MR 설명을 자동으로 생성합니다.

- Bash 기반 CLI 인터페이스
- OpenAI GPT API 연동
- MR 템플릿 분기 처리 (feature/refactor/bugfix)
- 결과물: `mr_description.md`

[👉 상세 사용법 보기](./gitlab_mr_create/README.md)

### 2. 📘 YouTube 자막 다운로드기 (`youtube_subtitle_download/`)

`video_urls.txt`에 있는 유튜브 URL을 기반으로 영상 자막을 텍스트 파일로 저장합니다.

- `youtube-transcript-api` 라이브러리 활용
- 자동 생성 자막 지원 (단, 유튜브 정책에 따라 일부 제외)
- 영상 하나당 `.txt` 파일 1개 생성

[👉 상세 사용법 보기](./youtube_subtitle_download/README.md)

---

### 3. 📂 포트폴리오 자동 생성기 (`portfolio/`)

GitLab 프로젝트의 커밋을 기반으로 GPT가 자동으로 **기술 포트폴리오 문서**를 생성합니다.

- GitLab REST API로 커밋 및 diff 수집
- 커밋을 10개 단위로 분할해 GPT에게 요약 요청
- `summary_batch_*.md` 파일 생성
- 요약 결과를 GPT로 다시 입력해 **기술 챕터 단위의 포트폴리오 문서** 생성

```
- 결과물:
  - `summary_batch_1.md ~ 10.md`: 커밋 요약
  - `portfolio.md`: 기술 중심 문서
  - `portfolio.pdf`: 포맷팅된 출력물 (선택)
```

[👉 상세 사용법 보기](./gitlab_portfolio/README.md)

---

## 🛠️ 사용 전 준비사항

- Python 3.x (YouTube 자막용)
- `youtube-transcript-api` 패키지 설치
- `jq` 설치 (GitLab MR 스크립트용)
- GitLab Personal Access Token 발급
- OpenAI API 키 발급

---

## 🙋‍♂️ 작성자

**최효재**  
- SSAFY 수료생, Spring Boot & DevOps 환경에 강점  
- GitLab API 및 OpenAI API를 활용한 자동화 도구 개발자

---

## 📜 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다. 자유롭게 사용하되, 출처를 명시해주세요.