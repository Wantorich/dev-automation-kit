import requests
import logging
import os
import glob
import shutil

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


def validate_project_exists(BASE_URL, HEADERS):
    url = f"{BASE_URL}"
    logging.info(f"🔍 프로젝트 존재 여부 확인 중: {url}")
    try:
        resp = requests.get(url, headers=HEADERS)
        if resp.status_code == 200:
            logging.info("✅ 프로젝트가 존재합니다.")
            return True
        elif resp.status_code == 404:
            logging.error("❌ 프로젝트를 찾을 수 없습니다. PROJECT_ID가 잘못되었을 수 있습니다.")
        elif resp.status_code == 401 or resp.status_code == 403:
            logging.error("❌ 인증 실패: PRIVATE-TOKEN이 유효하지 않거나 권한이 부족합니다.")
        else:
            logging.error(f"❌ 알 수 없는 응답 상태 코드: {resp.status_code}")
    except Exception as e:
        logging.error(f"❌ 프로젝트 존재 확인 중 예외 발생: {e}")
    return False

def cleanup_result_directory():
    # 이 함수는 더 이상 사용하지 않음
    pass