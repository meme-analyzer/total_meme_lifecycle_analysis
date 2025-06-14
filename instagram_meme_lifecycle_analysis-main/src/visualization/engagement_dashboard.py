from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR))
from config.settings import RESULTS_DIR, SRC_DIR, DATA_DIR
sys.path.append(str(SRC_DIR))
from utils.input_utils import meme_name_from_user

# 스타일 설정
plt.style.use("seaborn-v0_8-muted")
sns.set_palette("rocket")

# 파일 경로
meme_name = meme_name_from_user()

df_path_before = DATA_DIR / "analysis" / f"{meme_name}" /  "engagement" / f"{meme_name}_likes_cleaned.csv"
weekly_path_before = DATA_DIR / "analysis" / f"{meme_name}" /  "engagement" / f"{meme_name}_weekly_likes.csv"
weekday_path_before = DATA_DIR / "analysis" / f"{meme_name}" /  "engagement" / f"{meme_name}_weekday_likes.csv"

output_path = RESULTS_DIR / f"{meme_name}" / "engagement"
output_path.mkdir(parents=True, exist_ok=True)
output_path_visualization = output_path / "visualization"
output_path_visualization.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(df_path_before)
weekly = pd.read_csv(weekly_path_before)
weekday = pd.read_csv(weekday_path_before, index_col=0)

# 시각화 1 - 좋아요 분포
def plot_like_distribution():
    plt.figure(figsize=(10, 6))
    sns.histplot(df["likes"], bins=30, kde=True, color="skyblue")
    plt.title(f"'{meme_name}' 좋아요 수 분포")
    plt.xlabel("좋아요 수")
    plt.ylabel("게시물 수")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path_visualization / f"{meme_name}_like_distribution.png", dpi=300)
    plt.close()

# 시각화 2 - 주간 변화
def plot_weekly_likes():
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=weekly, x="week", y="likes", marker="o", color="orange")
    plt.title(f"'{meme_name}' 좋아요 최근 동향")
    plt.xlabel("주간")
    plt.ylabel("좋아요 수")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path_visualization / f"{meme_name}_weekly_likes.png", dpi=300)
    plt.close()

# 시각화 3 - 요일별 평균
def plot_weekday_likes():
    weekday_df = weekday.reset_index()
    weekday_df.columns = ["weekday", "likes"]

    plt.figure(figsize=(10, 6))
    sns.barplot(data=weekday_df, x="weekday", y="likes", hue="weekday", palette="magma", legend=False)
    plt.title(f"'{meme_name}' 요일별 평균 좋아요 수")
    plt.xlabel("요일")
    plt.ylabel("평균 좋아요 수")
    plt.grid(True, axis="y")
    plt.tight_layout()
    plt.savefig(output_path_visualization / f"{meme_name}_weekday_likes.png", dpi=300)
    plt.close()

# 시각화 4 - 대시보드 결합
def plot_engagement_dashboard():
    fig = plt.figure(figsize=(16, 12))
    fig.suptitle(f"'{meme_name}' 반응 강도 대시보드", fontsize=18, weight="bold")

    # GridSpec: 2행 2열, 상단은 colspan
    from matplotlib.gridspec import GridSpec
    gs = GridSpec(2, 2, figure=fig, height_ratios=[1, 1])

    # 좋아요 수 분포
    ax1 = fig.add_subplot(gs[1, 0])
    sns.histplot(df["likes"], bins=30, kde=True, color="skyblue", ax=ax1)
    ax1.set_title("좋아요 수 분포", fontsize=14)
    ax1.set_xlabel("좋아요 수")
    ax1.set_ylabel("게시물 수")
    ax1.grid(True)

    # 주간 좋아요 추이
    ax2 = fig.add_subplot(gs[1, 1])
    sns.lineplot(data=weekly, x="week", y="likes", marker="o", color="orange", ax=ax2)
    ax2.set_title("주간 좋아요 추이", fontsize=14)
    ax2.set_xlabel("주간")
    ax2.set_ylabel("좋아요 수")
    ax2.grid(True)

    # 요일별 평균 좋아요 수
    ax3 = fig.add_subplot(gs[0, :])
    weekday_df = weekday.reset_index()
    weekday_df.columns = ["weekday", "likes"]
    sns.barplot(data=weekday_df, x="weekday", y="likes", hue="weekday", palette="magma", legend=False, ax=ax3)
    ax3.set_title("요일별 평균 좋아요 수", fontsize=14)
    ax3.set_xlabel("요일")
    ax3.set_ylabel("평균 좋아요 수")
    ax3.grid(True, axis="y")

    # 자동 정렬
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(output_path / f"{meme_name}_dashboard.png", dpi=300)
    plt.close()

# 실행
if __name__ == "__main__":
    plot_like_distribution()
    plot_weekly_likes()
    plot_weekday_likes()
    plot_engagement_dashboard()