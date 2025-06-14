from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from pathlib import Path
import sys, time, json

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR))
from config.env import INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD
from config.settings import DATA_DIR, SRC_DIR

sys.path.append(str(SRC_DIR))
from utils.input_utils import meme_name_from_user

# 밈 검색
meme_name = meme_name_from_user()
search_url = f"https://www.instagram.com/explore/search/keyword/?q=%23{meme_name}"

# Selenium 설정
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0")

driver = webdriver.Chrome(options=options)

# 로그인 절차
driver.get("https://www.instagram.com/accounts/login/")
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "username"))
)
driver.find_element(By.NAME, "username").send_keys(INSTAGRAM_USERNAME)
driver.find_element(By.NAME, "password").send_keys(INSTAGRAM_PASSWORD + Keys.RETURN)

input("🔐 로그인 완료 후 Enter를 누르세요...")

driver.get(search_url)

# 첫 번째 썸네일 클릭
try:
    first_thumb = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "_aagw"))
    )
    first_thumb.click()
    time.sleep(3)
except Exception as e:
    print("썸네일 클릭 실패:", e)

all_data = []

# while True:
for i in range(3):  # 예시로 10개의 게시물만 수집
    try:
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # 게시 시간
        time_tag = soup.find("time", attrs={"datetime": True})
        post_time = time_tag["datetime"] if time_tag else ""

        # # 좋아요 수
        likes = 0
        target_class = "html-span xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1hl2dhg x16tdsg8 x1vvkbs"
        like_tag = next(
            (tag for tag in soup.find_all("span") if tag.get("class") and " ".join(tag.get("class")) == target_class),
            None
        )
        if like_tag:
            try:
                likes = int(like_tag.get_text(strip=True).replace(",", ""))
            except ValueError:
                likes = 0

        # 설명 텍스트
        caption = ""
        target_caption_class = "_ap3a _aaco _aacu _aacx _aad7 _aade"
        caption_tag = next(
            (tag for tag in soup.find_all("h1") if tag.get("class") and " ".join(tag.get("class")) == target_caption_class),
            None
        )
        if caption_tag:
            caption = caption_tag.get_text(separator=" ", strip=True)

        # 작성자 계정명
        username = ""
        target_user_class = "x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz _aswp _aswq _aswv _aswz _asw_ _asx2 _a6hd"
        user_tag = next(
            (tag for tag in soup.find_all("a") if tag.get("class") and " ".join(tag.get("class")) == target_user_class),
            None
        )
        if user_tag:
            username = user_tag.get_text(strip=True)

        # 데이터 저장
        data = {
            "username": username,
            "upload_time": post_time,
            "likes": likes,
            "caption": caption,
        }
        all_data.append(data)
        input("넘어가기")
        # 다음 버튼 클릭
        next_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//button[.//svg[@aria-label="다음"] or .//*[text()="다음"]]'))
        )
        next_button.click()
        print("✅ 다음 게시물로 이동")

    except Exception:
        print("📍 더 이상 다음 게시물이 없습니다.")
        break

# 결과 저장
Path("data/analysis").mkdir(parents=True, exist_ok=True)
with open(f"data/raw/{meme_name}_instagram.json", "w", encoding="utf-8") as f:
    json.dump(all_data, f, ensure_ascii=False, indent=2)

input("\n👋 Enter를 누르면 브라우저를 종료합니다...")
driver.quit()