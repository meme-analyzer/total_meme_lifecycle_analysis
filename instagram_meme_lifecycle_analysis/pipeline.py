from pathlib import Path
from src.utils.input_utils import meme_name_from_user
import subprocess, sys, shutil

# 설정된 상수 불러오기
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
from config.settings import SRC_DIR

def run_script(relative_path):
    script_path = SRC_DIR / relative_path
    result = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"오류 발생: {script_path}")
        print(result.stderr)
    else:
        print(f"완료: {script_path}")
        print(result.stdout)


if __name__ == "__main__":
    width = shutil.get_terminal_size().columns
    print("=" * 50)
    print("\n\"밈 생명주기 분석\" 파이프라인 시작")
    meme_name = meme_name_from_user()
    print(f"대상 밈: #{meme_name}\n")

    # 1. Instagram 수집 및 전처리
    print("=" * 50)
    print("\n[1] Instagram 수집 (수동 로그인 필요)\n")
    # run_script("data_collection/instagram.py")  # 필요 시 주석 해제

    # 2. Engagement 분석 및 대시보드
    print("=" * 50)
    print("\n[2] Engagement 분석 및 대시보드")
    run_script("preprocessing/instagram.py")
    run_script("analysis/engagement.py")
    run_script("visualization/engagement_dashboard.py")

    # 3. Keyword 분석 및 대시보드
    print("=" * 50)
    print("\n[3] Keyword 분석 및 대시보드")
    run_script("preprocessing/instagram.py")
    run_script("analysis/keywords.py")
    run_script("visualization/keywords_dashboard.py")

    # 4. Lifecycle 분석 및 대시보드
    print("=" * 50)
    print("\n[4] Lifecycle 분석 및 대시보드")
    run_script("preprocessing/instagram.py")
    run_script("analysis/lifecycle.py")
    run_script("visualization/lifecycle_dashboard.py")

    print("=" * 50)
    print("\n모든 분석 및 시각화 완료\n")
    print("=" * 50)
