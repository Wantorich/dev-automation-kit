import os
from dotenv import load_dotenv
import logging
from precheck import validate_project_exists
from batch_markdown import batch_markdown
from summarize_portfolio import summarize_portfolio

# Load environment variables
load_dotenv()

# Configuration from .env
GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")
GITLAB_HOST = os.getenv("GITLAB_HOST")
PROJECT_ID = os.getenv("PROJECT_ID")
AUTHOR_NAME = os.getenv("AUTHOR_NAME")
BRANCH = os.getenv("BRANCH")

HEADERS = {"PRIVATE-TOKEN": GITLAB_TOKEN}
BASE_URL = f"https://{GITLAB_HOST}/api/v4/projects/{PROJECT_ID}"

def main():
    try:
        if not validate_project_exists(BASE_URL, HEADERS):
            raise SystemExit("⛔ 프로젝트가 존재하지 않으므로 스크립트를 중단합니다.")
        batch_markdown(BASE_URL, HEADERS, BRANCH, AUTHOR_NAME, num_files=10)
        summarize_portfolio()
        
    except Exception as e:
        logging.error(f"❌ 실행 중 오류 발생: {e}")
        raise SystemExit(f"❌ 중단됨: {e}")

if __name__ == "__main__":
    main()
