import glob
import openai
import logging
import os


def summarize_portfolio():
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GPT_MODEL_PORTFOLIO = os.getenv("GPT_MODEL_PORTFOLIO", "gpt-4o")
    
    # result 폴더 내 모든 md 파일 읽기
    md_files = sorted(glob.glob("./result/*.md"))
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

    # 결과 저장
    os.makedirs("./portfolio", exist_ok=True)
    with open("./portfolio/portfolio_summary.md", "w", encoding="utf-8") as f:
        f.write("# 전체 포트폴리오 요약\n\n")
        f.write(portfolio_summary)

    logging.info("✅ 전체 포트폴리오 요약 저장 완료: ./portfolio/portfolio_summary.md") 