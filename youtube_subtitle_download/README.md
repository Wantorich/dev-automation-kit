# 📘 YouTube 자막 추출기

이 스크립트는 `video_urls.txt`에 있는 유튜브 영상 URL 목록을 기반으로, 각 영상의 **자막을 크롤링하여 텍스트 파일로 저장**합니다. 자막은 `youtube-transcript-api` 라이브러리를 통해 수집되며, 영상 하나당 하나의 `.txt` 파일이 생성됩니다.

---

## 📦 설치 방법

Python 3.x 환경에서 다음 명령어를 통해 필요한 라이브러리를 설치하세요:

```bash
pip install youtube-transcript-api
```

---

## 📁 입력 파일 구조

스크립트와 동일한 디렉토리에 `video_urls.txt` 파일을 생성하고, **유튜브 영상 URL을 한 줄에 하나씩** 작성하세요.

예시:

```
https://www.youtube.com/watch?v=dQw4w9WgXcQ
https://youtu.be/3JZ_D3ELwOQ
```

---

## ▶️ 실행 방법

터미널 또는 커맨드라인에서 다음 명령어로 실행하세요:

```bash
python download_subs.py
```

- 성공적으로 자막을 추출하면 `video_id.txt` 형식으로 파일이 생성됩니다.
- 예: `dQw4w9WgXcQ.txt`, `3JZ_D3ELwOQ.txt`

---

## 📌 주의사항

- 자막이 **공개**되어 있는 영상만 처리됩니다.
- 자동 생성 자막(오토 자막)은 유튜브 설정에 따라 불러오지 못할 수 있습니다.
- 유효하지 않은 URL 또는 비공개 영상은 스킵되며, 콘솔에 에러 메시지가 출력됩니다.

---

## 📂 결과 예시

실행 후 디렉토리에 다음과 같은 파일이 생성됩니다:

```
project/
├─ video_urls.txt
├─ download_subs.py
├─ dQw4w9WgXcQ.txt
├─ 3JZ_D3ELwOQ.txt
```
