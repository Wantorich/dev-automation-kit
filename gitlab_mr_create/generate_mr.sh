#!/bin/bash

# 🔧 사용자 입력 받기
read -p "🌐 출력 언어를 선택하세요 (ko/en): " LANG_OPTION
if [[ "$LANG_OPTION" != "ko" && "$LANG_OPTION" != "en" ]]; then
  echo "❌ 'ko' 또는 'en' 중 하나를 입력해주세요."
  exit 1
fi

read -p "🎯 소스 브랜치를 입력하세요: " BRANCH
read -p "📦 가져올 커밋 개수를 입력하세요: " COMMIT_COUNT
read -p "📁 MR 타입을 입력하세요 (feature / refactor / bugfix): " MR_TYPE


# 🔐 환경 설정
GITLAB_HOST="lab.ssafy.com"
GITLAB_TOKEN=$(cat "./credentials/glab-token.txt")
echo "🔑 GitLab 토큰: ${GITLAB_TOKEN:0:4}..."  # 토큰의 첫 4자리만 표시
OPENAI_API_KEY=$(cat "./credentials/share-openai-key.txt")
PROJECT_ID="1002024"  # 직접 확인한 프로젝트 ID
TEMPLATE_FILE="templates/${MR_TYPE}.md"
OUTPUT_FILE="mr_description.md"


if [ ! -f "$TEMPLATE_FILE" ]; then
  echo "❌ 해당 MR 타입 템플릿이 존재하지 않습니다: $TEMPLATE_FILE"
  exit 1
fi

MR_TEMPLATE=$(cat "$TEMPLATE_FILE")


# API 응답 확인 함수
check_api_response() {
    local response="$1"
    if echo "$response" | jq -e '.message' > /dev/null 2>&1; then
        local error_message=$(echo "$response" | jq -r '.message')
        echo "❌ API 오류: $error_message"
        echo "프로젝트 ID($PROJECT_ID)와 GitLab 토큰을 확인해주세요."
        exit 1
    fi
}

# 📌 최근 커밋 메시지 가져오기
COMMITS=$(curl --silent --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "https://$GITLAB_HOST/api/v4/projects/$PROJECT_ID/repository/commits?ref_name=$BRANCH&per_page=$COMMIT_COUNT")

echo "📄 COMMITS API 응답 원문 ↓"
echo "$COMMITS" | jq .

# API 응답 확인
check_api_response "$COMMITS"

# 📌 최신 / 최초 커밋 SHA 가져오기
LATEST_COMMIT=$(echo "$COMMITS" | jq -r '.[0] | .id')
EARLIEST_COMMIT=$(echo "$COMMITS" | jq -r '.[-1] | .id')


# 🔁 각 커밋마다 커밋 메시지 + diff 쌍으로 구성
COMMIT_ENTRIES=""

for (( i=$COMMIT_COUNT-1; i>=0; i-- ))
do
  COMMIT_ID=$(echo "$COMMITS" | jq -r ".[$i].id")
  COMMIT_MSG=$(echo "$COMMITS" | jq -r ".[$i].message")

  echo "🔍 커밋 $((COMMIT_COUNT-i)): $COMMIT_ID 메시지 수집 중..."

  # 커밋별 diff 가져오기
  SINGLE_DIFF=$(curl --silent --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
    "https://$GITLAB_HOST/api/v4/projects/$PROJECT_ID/repository/commits/$COMMIT_ID/diff" \
    | jq -r '.[]?.diff // empty')

  # 커밋별 메시지+diff 조립
  COMMIT_ENTRIES+=$'\n'"[$(($COMMIT_COUNT-i))). 커밋 메시지: $COMMIT_MSG"$'\n'"코드 변경:"$'\n'"$SINGLE_DIFF"$'\n\n'
done


# 🧠 GPT에게 보낼 프롬프트 생성
if [ "$LANG_OPTION" == "ko" ]; then
  PROMPT=$(cat <<EOF
다음은 GitLab의 브랜치 '$BRANCH'에서 최근 $COMMIT_COUNT개의 커밋 메시지와 변경 내용입니다.

[커밋 및 변경 내용]
$COMMIT_ENTRIES

Merge Request 설명은 다음 항목 중심으로 작성해 주세요.  
**동료 개발자가 소스코드를 직접 열어보지 않아도 주요 변경사항과 맥락을 명확히 이해할 수 있도록** 작성하는 것이 목표입니다.

---

1. **변경 배경 및 기능 흐름**
   - 어떤 문제를 해결하거나, 어떤 기능을 추가하려 했는지 서술해 주세요.
   - 여러 커밋이 함께 하나의 목표를 향해 나아갔다면, 그 전개 흐름을 간결하게 설명해 주세요.

2. **주요 변경 사항**
   - 어떤 **파일 또는 모듈**이 변경되었고, 어떤 **기능적 변화**가 발생했는지 기술해 주세요.
   - 해당 변경이 **기존 동작 방식에 어떤 영향을 주는지**, 혹은 **UX / API 응답 / 성능 / 구조 설계 측면에서 어떤 개선**이 있었는지를 명확히 해주세요.
   - 예시:  
     - "Header.vue의 로그인 상태 렌더링 로직 수정 (useAuth 훅 추가)"  
     - "inference.py에 Beam Search 추가 → 응답 품질 향상"  
     - "docker-compose.yml에서 Redis 연결 방식 변경 (healthcheck 추가)"

3. **검증 및 테스트 방법**
   - 실제 어떤 방식으로 변경사항을 테스트했는지 기술해 주세요.
   - 예시:  
     - "로그인 후 사용자 이름이 헤더에 정상 출력되는지 크롬 개발자 도구로 확인"  
     - "새 모델로 5개 샘플 문장을 inference 후 예상된 요약이 출력되는지 수동 검토"  
     - "배포 후 Grafana에서 CPU 사용량이 기존보다 20% 감소한 것 확인"

4. **고려사항 및 한계**
   - 기능 구현이나 리팩토링 시 고민한 지점, 의도적으로 제외한 범위, 추후 개선 여지 등을 기술해 주세요.
   - 예:  
     - "현재는 로컬에서는 정상 동작하지만, SSR 환경에 대한 고려는 추후 진행 예정"  
     - "Latency 개선은 이루어졌지만, accuracy는 기존 모델과 차이가 없음"

---

또한, 이 변경 사항을 대표하는 **Merge Request 제목**(Title)을 함께 작성해주세요. 제목은 전체 변경의 핵심을 1줄로 요약하고, 다음 규칙을 따릅니다:

- 최대한 간결하고 명확하게 작성 (예: "QueryDSL 도입 및 Conflict 보안 로직 개선")
- 관례적으로 첫 글자는 소문자가 아닌 대문자로 시작
- 접두사: [Feature], [Refactor], [Bugfix] 등 변경의 성격을 나타내는 태그 포함 가능

최종적으로, 다음 항목을 모두 포함한 마크다운 형태로 상세히 작성해주세요(이모지 적극 사용):
1. MR 제목
2. MR 설명 (템플릿 형식)

[Tip] 커밋 메시지나 diff에 등장하는 **구체적인 클래스명 / 메서드 / 변수 / UI 요소 이름**을 명시하면 더 좋습니다.  
[⚠ 주의] 단순히 "기능을 추가했다" 식의 서술이 아니라 **"왜"**, **"어디에"**, **"어떻게" 바꿨는지**가 포함되어야 합니다.
[중요] 커밋 메시지나 코드 diff에 등장하는 클래스명, 메서드명, 필드명을 가능한 한 직접 명시하여 작성하세요.

$MR_TEMPLATE
EOF
)
else
  PROMPT=$(cat <<EOF
  The following contains the last $COMMIT_COUNT commits and their corresponding code changes from the GitLab branch '$BRANCH'.

[Commits & Diffs]
$COMMIT_ENTRIES

Please write a detailed Merge Request description based on the following instructions.  
The goal is to help reviewers quickly understand the purpose, scope, and effect of the changes **without reading the entire code diff**.

---

1. **Background & Feature Overview**
   - What problem is this solving or what functionality is being added?
   - If multiple commits contribute to one goal, explain the progression.

2. **Key Changes**
   - What files or modules were changed and why?
   - Mention any changes in UX/API/performance/design, etc.

3. **Validation & Testing**
   - How was the change tested and verified?

4. **Considerations or Limitations**
   - Any known edge cases, trade-offs, or future improvements?

---

Also generate a **concise MR title** that summarizes the change (e.g., "Refactor login flow and add token renewal").

$MR_TEMPLATE
EOF
)
fi

# echo "$PROMPT"

# JSON 바디를 파일로 저장
cat <<EOF > payload.json
{
  "model": "gpt-4o",
  "temperature": 0.4,
  "messages": [
    {
      "role": "user",
      "content": $(jq -Rs <<< "$PROMPT")
    }
  ]
}
EOF

# 🤖 GPT API 호출
RAW_RESPONSE=$(curl -s https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d @payload.json)

# 📦 응답 전체 출력 (에러 확인용)
echo "📦 GPT 응답 원문 ↓"
echo "$RAW_RESPONSE" | jq .

# 👀 정제된 응답만 추출
RESPONSE=$(echo "$RAW_RESPONSE" | jq -r '.choices[0].message.content // empty')

# ⛔ 응답 없을 경우 경고
if [ -z "$RESPONSE" ]; then
  echo "❌ GPT 응답이 비어 있습니다. 에러가 포함되어 있을 수 있습니다."
  exit 1
fi

# ✅ 정상일 경우 파일 저장
echo "$RESPONSE" > "$OUTPUT_FILE"
echo "✅ MR 설명이 '$OUTPUT_FILE' 파일에 저장되었습니다!"