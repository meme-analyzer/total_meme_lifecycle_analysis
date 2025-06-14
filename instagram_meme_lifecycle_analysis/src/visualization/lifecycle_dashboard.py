from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
from matplotlib.lines import Line2D


BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR))
from config.settings import DATA_DIR, RESULTS_DIR, SRC_DIR

sys.path.append(str(SRC_DIR))
from utils.input_utils import meme_name_from_user

# 경로 설정
meme_name = meme_name_from_user()
input_path = DATA_DIR / "analysis" / f"{meme_name}" /  "lifecycle" / f"{meme_name}_lifecycle.csv"

output_path = RESULTS_DIR / f"{meme_name}" / "lifecycle"
output_path.mkdir(parents=True, exist_ok=True)
output_path_visualization = output_path / "visualization"
output_path_visualization.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(input_path, parse_dates=["date"])

# 구간 배경색 정의
def add_phase_background(ax, df, phase_column="phase", x_column="date", phase_colors=None, alpha=0.3, return_legend=False):
    if phase_colors is None:
        phase_colors = {
            "성장기": "#6fa640",
            "정체기": "#a38cc2",
            "쇠퇴기": "#6c80b5"
        }

    used_phases = set()

    for _, group in df.groupby((df[phase_column] != df[phase_column].shift()).cumsum()):
        phase = group[phase_column].iloc[0]
        color = phase_colors.get(phase, "#ffffff")
        ax.axvspan(group[x_column].iloc[0], group[x_column].iloc[-1], color=color, alpha=alpha)
        used_phases.add(phase)

    if return_legend:
            # 범례용 가짜 선만 생성
            handles = [
                Line2D([0], [0], color="#6fa640", lw=10, alpha=0.3, label="성장기"),
                Line2D([0], [0], color="#a38cc2", lw=10, alpha=0.3, label="정체기"),
                Line2D([0], [0], color="#6c80b5", lw=10, alpha=0.3, label="쇠퇴기")
            ]
            return handles
    
# 시각화 1 - 일별 게시물 수와 이동 평균
def plot_daily_trend():
    plt.figure(figsize=(12, 6))
    ax = plt.gca()
    ax.plot(df["date"], df["count"], label="일일 게시물 수", alpha=0.3)
    ax.plot(df["date"], df["moving_avg"], label="7일 이동 평균", color="blue", linewidth=2)
    ax.legend()
    ax.set_title(f"'{meme_name}' 일일 트렌드 변화", fontsize=14)
    ax.set_xlabel("날짜")
    ax.set_ylabel("게시물 수")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path_visualization / f"{meme_name}_daily_trend.png", dpi=300)
    plt.close()

# 시각화 2 - 누적 게시물 수
def plot_cumulative_trend():
    plt.figure(figsize=(12, 6))
    ax = plt.gca()
    legend_handles = add_phase_background(ax, df, return_legend=True)
    ax.legend(handles=legend_handles)
    ax.plot(df["date"], df["cumulative"], label="누적 게시물 수", color="green")
    ax.fill_between(df["date"], df["cumulative"], color="green", alpha=0.2)
    ax.set_title(f"'{meme_name}' 누적 게시물 변화", fontsize=14)
    ax.set_xlabel("날짜")
    ax.set_ylabel("누적 수")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path_visualization / f"{meme_name}_cumulative_trend.png", dpi=300)
    plt.close()

# # 시각화 3 - 날짜-시간 히트맵
# def plot_heatmap_by_time():

#     temp_df = df.copy()
#     temp_df["upload_time"] = pd.to_datetime(temp_df["upload_time"])
#     temp_df["date"] = temp_df["upload_time"].dt.date
#     temp_df["hour"] = temp_df["upload_time"].dt.hour

#     heatmap_data = temp_df.groupby(["date", "hour"]).size().unstack(fill_value=0)

#     plt.figure(figsize=(14, 8))
#     sns.heatmap(heatmap_data, cmap="YlOrRd", linewidths=0.3, linecolor='gray')
#     plt.title(f"'{meme_name}' 시간대별 게시물 업로드 히트맵")
#     plt.xlabel("시간")
#     plt.ylabel("날짜")
#     plt.tight_layout()
#     plt.savefig(output_path_visualization / f"{meme_name}_time_heatmap.png", dpi=300)
#     plt.close()

# 시각화 4 - 전체 대시보드
def plot_lifecycle_dashboard():
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    fig.suptitle(f"'{meme_name}' 밈 수명 주기 대시보드", fontsize=18, weight="bold")

    # 일일 게시물 수
    ax1.plot(df["date"], df["count"], label="일일 게시물 수", alpha=0.3)
    ax1.plot(df["date"], df["moving_avg"], label="7일 이동 평균", color="blue", linewidth=2)
    ax1.set_ylabel("게시물 수")
    ax1.set_title("일일 트렌드 변화")
    ax1.grid(True, alpha=0.3)
    ax1.legend()

    # 누적 게시물 수 + 구간 배경 표시
    legend_handles = add_phase_background(ax2, df, return_legend=True)
    ax2.legend(handles=legend_handles)
    ax2.plot(df["date"], df["cumulative"], label="누적 게시물 수", color="green")
    ax2.fill_between(df["date"], df["cumulative"], color="green", alpha=0.2)
    ax2.set_ylabel("누적 수")
    ax2.set_xlabel("날짜")
    ax2.set_title("누적 게시물 증가")
    ax2.grid(True, alpha=0.3)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(output_path / f"{meme_name}_lifecycle.png", dpi=300)
    plt.close()

if __name__ == "__main__":
    plot_daily_trend()
    plot_cumulative_trend()
    # plot_heatmap_by_time()
    plot_lifecycle_dashboard()