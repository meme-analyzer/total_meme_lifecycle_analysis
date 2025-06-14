from pathlib import Path
import pandas as pd
import sys
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR))
from config.settings import DATA_DIR, DATA_DIR, SRC_DIR

sys.path.append(str(SRC_DIR))
from utils.input_utils import meme_name_from_user

# 파일 경로
meme_name = meme_name_from_user()
input_path = DATA_DIR / "preprocessed" / f"{meme_name}_instagram.csv"
output_path = DATA_DIR / "analysis" / f"{meme_name}" /  "engagement"
output_path.mkdir(parents=True, exist_ok=True)

# 숫자 변환 함수
def convert_count(val):
    val = str(val).strip().upper()
    if val.endswith("K"):
        return int(float(val[:-1]) * 1_000)
    elif val.endswith("M"):
        return int(float(val[:-1]) * 1_000_000)
    elif val.endswith("B"):
        return int(float(val[:-1]) * 1_000_000_000)
    else:
        return int(val)

# 분석 실행
def run_engagement_analysis():
    df = pd.read_csv(input_path)
    df["upload_time"] = pd.to_datetime(df["upload_time"])
    df["likes"] = df["likes"].apply(convert_count)

    # 요일 계산 (영문 → 한글)
    weekday_map = {
        "Monday": "월", "Tuesday": "화", "Wednesday": "수",
        "Thursday": "목", "Friday": "금", "Saturday": "토", "Sunday": "일"
    }
    df["weekday_kr"] = df["weekday"].map(weekday_map)

    # 주간 합산
    df["week"] = df["upload_time"].dt.to_period("W").dt.start_time
    weekly_likes = df.groupby("week")["likes"].sum().reset_index()
    weekday_likes = df.groupby("weekday_kr")["likes"].mean().reindex(
        ["월", "화", "수", "목", "금", "토", "일"]
    )

    # 저장
    df.to_csv(output_path / f"{meme_name}_likes_cleaned.csv", index=False, encoding="utf-8-sig")
    weekly_likes.to_csv(output_path / f"{meme_name}_weekly_likes.csv", index=False, encoding="utf-8-sig")
    weekday_likes.to_frame(name="avg_likes").to_csv(output_path / f"{meme_name}_weekday_likes.csv", encoding="utf-8-sig")

if __name__ == "__main__":
    run_engagement_analysis()
