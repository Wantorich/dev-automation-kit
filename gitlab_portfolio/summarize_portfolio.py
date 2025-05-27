import glob
import openai
import logging
import os
import requests
from dotenv import load_dotenv

def get_project_name(BASE_URL, HEADERS):
    url = f"{BASE_URL}"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    project_name = resp.json()['name']
    logging.info(f"📋 프로젝트 이름: {project_name}")
    return project_name

def summarize_portfolio():
    # 환경 변수 로드
    load_dotenv()
    
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GPT_MODEL_PORTFOLIO = os.getenv("GPT_MODEL_PORTFOLIO", "gpt-4o")
    GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")
    GITLAB_HOST = os.getenv("GITLAB_HOST")
    PROJECT_ID = os.getenv("PROJECT_ID")
    
    HEADERS = {"PRIVATE-TOKEN": GITLAB_TOKEN}
    BASE_URL = f"https://{GITLAB_HOST}/api/v4/projects/{PROJECT_ID}"
    
    # 프로젝트 이름 가져오기
    project_name = get_project_name(BASE_URL, HEADERS)
    
    # 프로젝트 폴더 내 모든 md 파일 읽기
    project_dir = f"./result/{project_name}"
    md_files = sorted(glob.glob(f"{project_dir}/*.md"))
    summaries = []
    for file in md_files:
        with open(file, "r", encoding="utf-8") as f:
            summaries.append(f.read())

    # 프롬프트 템플릿 불러오기
    with open("./prompt/portfolio_summary.txt", "r", encoding="utf-8") as pf:
        prompt = pf.read()

    # 각 배치 요약을 프롬프트에 추가
    for idx, summary in enumerate(summaries):
        prompt += f"\n\n---\n\n[Batch {idx+1} 요약]\n{summary}"

    # GPT에게 요청
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model=GPT_MODEL_PORTFOLIO,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )
    portfolio_summary = response.choices[0].message.content

    # 결과 저장 (같은 프로젝트 폴더에 저장)
    portfolio_dir = f"{project_dir}/portfolio"
    os.makedirs(portfolio_dir, exist_ok=True)
    with open(f"{portfolio_dir}/portfolio.md", "w", encoding="utf-8") as f:
        f.write(f"# {project_name} 포트폴리오\n\n")
        f.write(portfolio_summary)

    logging.info(f"✅ 전체 포트폴리오 요약 저장 완료: {project_dir}/portfolio.md") 