# 🧠 GitLab Commit 기반 MR Description 자동 생성기

## 📌 소개

이 스크립트는 GitLab 프로젝트의 특정 브랜치에서 최근 커밋 메시지와 코드 변경 사항(diff)을 추출하여, OpenAI GPT 모델을 통해 **Merge Request 설명 템플릿**을 자동으로 생성합니다.

> ✅ *매번 반복되는 MR 설명 작성, 이제는 AI에게 맡기세요.*

---

## 🧰 사용 기술

- Bash
- GitLab REST API (via `curl`)
- OpenAI API (`gpt-4o` 지원)
- [`jq`](https://stedolan.github.io/jq/) - JSON 파싱 CLI 툴

---

## 📁 디렉토리 구조

```bash
.
├── generate_mr.sh               # 메인 스크립트
├── templates/                  # MR 템플릿 디렉토리
│   ├── feature.md
│   ├── refactor.md
│   └── bugfix.md
├── payload.json                # GPT 요청 바디 확인용 (자동 생성)
├── mr_description.md           # 결과물: 자동 생성된 MR 설명
└── credentials/                # (Windows 예시) API 키 보관용 텍스트 파일
    ├── glab-token.txt
    └── openai-key.txt
```

---

## ⚙️ 사전 준비

### 1. `jq` 설치

1. jq 설치
🪟 Windows (수동 설치)
https://stedolan.github.io/jq/download/ 접속

하단의 Windows jq 1.7.1 AMD64 version download

다운로드한 파일을 C:\Program Files\jq\jq.exe 와 같이 적절한 위치에 저장 (이름 변경)

해당 경로를 환경 변수 PATH에 추가

"시스템 환경 변수 편집" → 환경 변수 → Path 편집 → jq.exe 위치 추가

설치 확인:
```bash
jq --version
```

---

### 2. GitLab Personal Access Token 발급

1. `https://lab.ssafy.com/-/profile/personal_access_tokens` 접속  
2. `read_api`, `read_repository` 권한 포함한 토큰 생성  
3. 안전한 경로에 저장  
   - 예: `~/Desktop/Credentials/glab-token.txt`


### 3. project Id 설정
1. gitlab setting -> general -> project ID 확인
2. PROJECT_ID 부분에 값 할당
---

## ▶️ 실행 방법

```bash
chmod +x generate_mr.sh
./generate_mr.sh
```

실행 시 다음 정보를 입력 받습니다:

- 🎯 타겟 브랜치 (예: `feature/conflict/be`)
- 📦 가져올 커밋 개수 (예: `10`)
- 📁 MR 템플릿 타입 (feature / refactor / bugfix 중 택 1)

---

## ✅ 결과물

- `mr_description.md` 파일에 자동 생성된 **Merge Request 설명**이 저장됩니다.
- Markdown 형식이며 GitLab MR 작성 시 그대로 붙여넣을 수 있습니다.

---

## 📎 템플릿 추가/수정 방법

- `templates/` 폴더 내에 Markdown 템플릿을 관리합니다.
- 이름은 `feature.md`, `refactor.md`, `bugfix.md` 처럼 맞춰야 합니다.
- 원하는 템플릿 예시:

```md
# 🚀 Feature

## ✨ 개요

## ✅ 주요 기능

## 🔍 테스트 방법

## 🧠 고려 사항

## 📎 관련 이슈
```

---

## 🧨 오류 해결

| 증상 | 해결 방법 |
|------|-----------|
| `jq: command not found` | jq가 설치되지 않았습니다. 위 설치 방법 참고 |
| `404 Project Not Found` | GitLab 프로젝트 ID가 올바른지 확인 (숫자 ID 필요) |
| `OPENAI 응답이 null` | 잘못된 JSON 형식 → 스크립트의 `PROMPT` 또는 `payload.json` 확인 |
| `glab` 명령 실패 | 현재 스크립트는 `glab` 없이 `curl` 기반으로 동작하도록 작성됨 |

---

## 💡 사용 예시

```bash
$ ./generate_mr.sh
🎯 타겟 브랜치를 입력하세요: feature/conflict/be
📦 가져올 커밋 개수를 입력하세요: 5
📁 MR 타입을 입력하세요 (feature / refactor / bugfix): refactor
🔑 GitLab 토큰: x6_G...
✅ MR 설명이 'mr_description.md' 파일에 저장되었습니다!
```

---

## 👨‍💻 개발자 팁

- `payload.json`은 매 요청마다 생성되어 GPT 호출 내용을 디버깅하는 데 유용합니다
- `diff`까지 반영된 MR 설명은 특히 큰 리팩터링이나 보안 이슈에 효과적입니다

---

## 🪪 작성자

- **최효재**  
  - GitLab API와 GPT 기반 자동화 워크플로우 구축  
  - Spring Boot & DevOps 환경 자동화 경험 보유