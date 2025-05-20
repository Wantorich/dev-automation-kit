import os
import requests
import openai
from datetime import datetime
from dotenv import load_dotenv
import time
import logging
import glob
import math

# Load environment variables
# Configuration from .env
GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")
GITLAB_HOST = os.getenv("GITLAB_HOST")
PROJECT_ID = os.getenv("PROJECT_ID")
AUTHOR_NAME = os.getenv("AUTHOR_NAME")
AUTHOR_EMAIL = os.getenv("AUTHOR_EMAIL")
BRANCH = os.getenv("BRANCH")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "10"))

openai.api_key = OPENAI_API_KEY
GPT_MODEL = "gpt-4o-mini"
GPT_MODEL_PORTFOLIO = "gpt-4o"

HEADERS = {"PRIVATE-TOKEN": GITLAB_TOKEN}
BASE_URL = f"https://{GITLAB_HOST}/api/v4/projects/{PROJECT_ID}"

# 로그 설정
LOG_FILE = "progress.log"
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# UTF-8 인코딩된 파일 핸들러 설정
file_handler = logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# 핸들러 적용
logger.addHandler(file_handler)

def list_all_branches(BASE_URL, HEADERS):
    url = f"{BASE_URL}/repository/branches"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    branches = [b['name'] for b in resp.json()]
    logging.info(f"📋 현재 브랜치 목록: {branches}")
    return branches

def get_all_commits(BASE_URL, HEADERS, BRANCH, AUTHOR_NAME):
    all_commits = []
    page = 1
    while True:
        params = {
            "ref_name": BRANCH,
            "author": AUTHOR_NAME,
            "per_page": 100,
            "page": page
        }
        logging.info(f"📦 커밋 페이지 {page} 요청 중...")
        resp = requests.get(f"{BASE_URL}/repository/commits", headers=HEADERS, params=params)
        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            break
        all_commits.extend(batch)
        page += 1
        time.sleep(0.1)
    logging.info(f"✅ 총 커밋 수: {len(all_commits)}")
    return all_commits[::-1]

def get_diff(BASE_URL, HEADERS, commit_id):
    url = f"{BASE_URL}/repository/commits/{commit_id}/diff"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    diffs = [d["diff"] for d in resp.json()]
    return "\n".join(diffs)[:5000]

def summarize_commits(BASE_URL, HEADERS, batch, index):
    logging.info(f"🔹 Batch {index+1} 요약 시작")
    with open("./prompt/commit_summary.txt", "r", encoding="utf-8") as pf:
        prompt = pf.read()

    for commit in batch:
        commit_id = commit["id"]
        message = commit["message"]
        logging.info(f"➡️ diff 추출 중: {commit_id[:8]} - {message.splitlines()[0][:50]}")
        diff = get_diff(BASE_URL, HEADERS, commit_id)
        prompt += f"\n---\n\n✅ 커밋 메시지: {message}\n📄 Diff 내용:\n{diff}\n"
        time.sleep(0.2)

    # 실제로는 GPT 요약 결과를 summary에 넣으세요!
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )
    summary = response.choices[0].message.content

    filename = f"./result/summary_batch_{index+1}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(summary)

    logging.info(f"✅ Batch {index+1} 결과 저장: {filename}")

def batch_markdown(BASE_URL, HEADERS, BRANCH, AUTHOR_NAME, num_files=10):
    list_all_branches(BASE_URL, HEADERS)
    total_commits = get_all_commits(BASE_URL, HEADERS, BRANCH, AUTHOR_NAME)
    if not total_commits:
        raise ValueError("커밋이 존재하지 않음 또는 조회 실패")

    batch_size = math.ceil(len(total_commits) / num_files)
    total_batches = (len(total_commits) + batch_size - 1) // batch_size
    logging.info(f"batch_size: {batch_size}")
    logging.info(f"total_batches: {total_batches}")

    for i in range(total_batches):
        batch = total_commits[i*batch_size : (i+1)*batch_size]
        summarize_commits(BASE_URL, HEADERS, batch, i)
    logging.info("🎉 전체 요약 완료")