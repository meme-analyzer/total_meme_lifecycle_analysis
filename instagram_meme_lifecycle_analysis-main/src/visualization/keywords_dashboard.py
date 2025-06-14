import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.font_manager as fm
import seaborn as sns
import networkx as nx
from wordcloud import WordCloud
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR))
from config.settings import DATA_DIR, RESULTS_DIR, SRC_DIR

sys.path.append(str(SRC_DIR))
from utils.input_utils import meme_name_from_user

# 데이터 파일 경로
meme_name = meme_name_from_user()
input_path = DATA_DIR / "analysis" / f"{meme_name}" /  "keywords" / f"{meme_name}_keywords.csv"

# 스타일
plt.style.use("seaborn-v0_8-colorblind")
sns.set_palette("Set2")

# macOS의 Apple Gothic 폰트 경로
font_path = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
font_prop = fm.FontProperties(fname=font_path)

# 전역 폰트 설정
plt.rcParams['font.family'] = font_prop.get_name()

df = pd.read_csv(input_path)

# 폴더 생성
output_path = RESULTS_DIR / f"{meme_name}" / "keywords"
output_path.mkdir(parents=True, exist_ok=True)
output_path_visualization = output_path / "visualization"
output_path_visualization.mkdir(parents=True, exist_ok=True)

# 시각화 1 - 막대그래프
def plot_bar_chart(df, meme_name):
    fig, ax = plt.subplots(figsize=(10, 6))
    top = df.head(20)
    ax.barh(top["word"], top["count"], color="skyblue")
    ax.invert_yaxis()
    ax.set_title(f"Top 20 Keywords for '{meme_name}'", fontsize=15, weight="bold")
    ax.set_xlabel("Frequency")
    fig.tight_layout()
    plt.savefig(output_path_visualization / f"{meme_name}_bar_chart.png", dpi=300)
    plt.close()

# 시각화 2 - 워드클라우드
def plot_wordcloud(df, meme_name):
    freq = dict(zip(df["word"], df["count"]))

    wc = WordCloud(
        font_path=font_path,
        background_color="white",
        width=800,
        height=400
    ).generate_from_frequencies(freq)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    fig.tight_layout()
    plt.savefig(output_path_visualization / f"{meme_name}_wordcloud.png", dpi=300)
    plt.close()

# 시각화 3 - 네트워크 그래프
def plot_network(df, meme_name):
    G = nx.Graph()
    words = df.head(20)["word"].tolist()
    counts = df.head(20)["count"].tolist()

    for word, count in zip(words, counts):
        G.add_node(word, size=count)

    for i in range(len(words)):
        for j in range(i+1, len(words)):
            if abs(len(words[i]) - len(words[j])) <= 1:
                G.add_edge(words[i], words[j])

    pos = nx.spring_layout(G, seed=42)
    fig, ax = plt.subplots(figsize=(10, 6))
    sizes = [G.nodes[n]["size"] * 10 for n in G.nodes]
    nx.draw(G, pos, with_labels=True, node_size=sizes, node_color="lightgreen", edge_color="gray", font_size=10, font_family=font_prop.get_name(), ax=ax)
    plt.title(f"Keyword Network for '{meme_name}'", fontsize=14, weight="bold")
    plt.savefig(output_path_visualization / f"{meme_name}_keyword_network.png", dpi=300)
    plt.close()

# 시각화 4 - 대시보드
def plot_dashboard(df, meme_name):
    # 준비
    freq = dict(zip(df["word"], df["count"]))
    words = df.head(20)["word"].tolist()
    counts = df.head(20)["count"].tolist()

    # 워드클라우드용 마스크 (없으면 None)
    wc = WordCloud(
        font_path=font_path,
        background_color="white",
        width=800,
        height=400
    ).generate_from_frequencies(freq)

    # 네트워크 그래프 준비
    G = nx.Graph()
    for word, count in zip(words, counts):
        G.add_node(word, size=count)
    for i in range(len(words)):
        for j in range(i+1, len(words)):
            if abs(len(words[i]) - len(words[j])) <= 1:
                G.add_edge(words[i], words[j])
    pos = nx.spring_layout(G, seed=42)

    # 대시보드 레이아웃 설정
    fig = plt.figure(figsize=(16, 12))
    gs = gridspec.GridSpec(2, 2, height_ratios=[1, 1])

    # 전체 제목
    fig.suptitle(f"인스타그램 키워드 분석 대시보드 - '{meme_name}'", fontsize=18, weight="bold")

    # 네트워크 그래프 (왼쪽 위)
    ax1 = fig.add_subplot(gs[0, 0])
    sizes = [G.nodes[n]["size"] * 10 for n in G.nodes]
    nx.draw(
        G, pos,
        with_labels=True,
        node_size=sizes,
        node_color="lightgreen",
        edge_color="gray",
        font_size=10,
        font_family=font_prop.get_name(),
        ax=ax1
    )
    ax1.set_title("Keyword Network", fontsize=14, weight="bold")

    # 워드클라우드 (오른쪽 위)
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.imshow(wc, interpolation="bilinear")
    ax2.axis("off")
    ax2.set_frame_on(False)
    ax2.set_title("WordCloud", fontsize=14, weight="bold")

    # 막대그래프 (아래 전체 너비)
    ax3 = fig.add_subplot(gs[1, :])
    top = df.head(20)
    ax3.barh(top["word"], top["count"], color="skyblue")
    ax3.invert_yaxis()
    ax3.set_title("Top 20 Keywords", fontsize=14, weight="bold")
    ax3.set_xlabel("Frequency")

    # 자동 여백 조정
    plt.tight_layout(rect=[0, 0, 1, 0.95])  # suptitle 공간 확보
    plt.savefig(output_path / f"{meme_name}_dashboard.png", dpi=300)
    plt.close()

# 실행
if __name__ == "__main__":
    plot_bar_chart(df, meme_name)
    plot_wordcloud(df, meme_name)
    plot_network(df, meme_name)
    plot_dashboard(df, meme_name)