from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform

BASE_DIR = Path(__file__).resolve().parent.parent

# 주요 폴더 경로 설정
CACHE_DIR = BASE_DIR / "cache"
DATA_DIR = BASE_DIR / "data"
RESULTS_DIR = BASE_DIR / "results"
SRC_DIR = BASE_DIR / "src"

# 공통 한글 폰트 설정
def set_global_font():
    system = platform.system()
    if system == "Darwin":  # macOS
        font_path = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
    elif system == "Windows":
        font_path = "C:/Windows/Fonts/malgun.ttf"
    else:
        font_path = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"  # 예시

    font_prop = fm.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()
    return font_prop.get_name()

# 실제로 한 번 설정 적용
DEFAULT_FONT = set_global_font()