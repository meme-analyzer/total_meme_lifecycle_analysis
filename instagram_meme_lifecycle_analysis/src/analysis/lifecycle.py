from pathlib import Path
import pandas as pd
import sys

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR))
from config.settings import DATA_DIR, SRC_DIR

sys.path.append(str(SRC_DIR))
from utils.input_utils import meme_name_from_user

# 입력/출력 경로 설정
meme_name = meme_name_from_user()
input_path = DATA_DIR / "preprocessed" / f"{meme_name}_instagram.csv"
output_path = DATA_DIR / "analysis" / f"{meme_name}" /  "lifecycle"
output_path.mkdir(parents=True, exist_ok=True)

def run_lifecycle_analysis():
    df = pd.read_csv(input_path, parse_dates=["upload_time"])

    # 날짜 기준 집계
    df["date"] = df["upload_time"].dt.date
    daily_counts = df.groupby("date").size()
    daily_df = daily_counts.reset_index(name="count")
    daily_df["date"] = pd.to_datetime(daily_df["date"])

    # ✅ 요일(한글) 컬럼 추가
    weekday_kor = {
        0: "월요일",
        1: "화요일",
        2: "수요일",
        3: "목요일",
        4: "금요일",
        5: "토요일",
        6: "일요일"
    }
    daily_df["weekday"] = daily_df["date"].dt.weekday.map(weekday_kor)

    # 이동 평균 & 누적
    daily_df["moving_avg"] = daily_df["count"].rolling(window=7, min_periods=1).mean()
    daily_df["cumulative"] = daily_df["count"].cumsum()

    # 구간 감지
    daily_df["delta"] = daily_df["moving_avg"].diff().rolling(window=3, min_periods=1).mean()

    def classify_phase(x):
        if x > -10.5:
            return "성장기"
        elif x < -10.3:
            return "쇠퇴기"
        else:
            return "정체기"

    daily_df["phase"] = daily_df["delta"].apply(classify_phase)

    # 저장
    daily_df.to_csv(output_path / f"{meme_name}_lifecycle.csv", index=False, encoding="utf-8-sig")


# from pathlib import Path
# import pandas as pd
# import sys

# BASE_DIR = Path(__file__).resolve().parent.parent.parent
# sys.path.append(str(BASE_DIR))
# from config.settings import DATA_DIR, SRC_DIR

# sys.path.append(str(SRC_DIR))
# from utils.input_utils import meme_name_from_user

# # 입력/출력 경로 설정
# meme_name = meme_name_from_user()
# input_path = DATA_DIR / "preprocessed" / f"{meme_name}_instagram.csv"
# output_path = DATA_DIR / "analysis" / f"{meme_name}" /  "lifecycle"
# output_path.mkdir(parents=True, exist_ok=True)

# def run_lifecycle_analysis():
#     df = pd.read_csv(input_path, parse_dates=["upload_time"])

#     # 날짜 기준 집계
#     df["date"] = df["upload_time"].dt.date
#     daily_counts = df.groupby("date").size()
#     daily_df = daily_counts.reset_index(name="count")
#     daily_df["date"] = pd.to_datetime(daily_df["date"])

#     # 이동 평균 & 누적
#     daily_df["moving_avg"] = daily_df["count"].rolling(window=7, min_periods=1).mean()
#     daily_df["cumulative"] = daily_df["count"].cumsum()

#     # 구간 감지
#     daily_df["delta"] = daily_df["moving_avg"].diff().rolling(window=3, min_periods=1).mean()

#     def classify_phase(x):
#         if x > -10.5:
#             return "성장기"
#         elif x < -10.3:
#             return "쇠퇴기"
#         else:
#             return "정체기"

#     daily_df["phase"] = daily_df["delta"].apply(classify_phase)

#     # 저장
#     daily_df.to_csv(output_path / f"{meme_name}_lifecycle.csv", index=False, encoding="utf-8-sig")
    
# if __name__ == "__main__":
#     run_lifecycle_analysis()