from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
import re

def extract_video_id(url: str) -> str:
    """
    다양한 유형의 유튜브 URL에서 video ID를 추출
    """
    parsed = urlparse(url.strip())

    if 'youtube' in parsed.netloc:
        return parse_qs(parsed.query).get('v', [None])[0]
    elif 'youtu.be' in parsed.netloc:
        return parsed.path.lstrip('/')
    else:
        return None

def save_transcript(video_id: str, filename: str):
    """
    자막을 가져와 텍스트 파일로 저장
    """
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko', 'en'])
        with open(filename, 'w', encoding='utf-8') as f:
            for entry in transcript:
                f.write(entry['text'] + '\n')
        print(f"✅ 저장 완료: {filename}")
    except Exception as e:
        print(f"❌ 실패 ({video_id}): {e}")

if __name__ == "__main__":
    with open('video_urls.txt', 'r', encoding='utf-8') as file:
        urls = file.readlines()

    for url in urls:
        video_id = extract_video_id(url)
        if video_id:
            save_transcript(video_id, f'{video_id}.txt')
        else:
            print(f"⚠️ video ID 추출 실패: {url.strip()}")
