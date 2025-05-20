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
    """
    result 디렉토리의 모든 파일을 삭제합니다.
    """
    result_dir = "./result"
    if os.path.exists(result_dir):
        logging.info("🧹 result 디렉토리 정리 중...")
        for file in glob.glob(os.path.join(result_dir, "*")):
            try:
                if os.path.isfile(file):
                    os.remove(file)
                    logging.info(f"✅ 파일 삭제 완료: {file}")
                elif os.path.isdir(file):
                    shutil.rmtree(file)
                    logging.info(f"✅ 디렉토리 삭제 완료: {file}")
            except Exception as e:
                logging.error(f"❌ 파일 삭제 중 오류 발생: {file} - {str(e)}")
        logging.info("✨ result 디렉토리 정리 완료")
    else:
        logging.info("ℹ️ result 디렉토리가 존재하지 않습니다.")