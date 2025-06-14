import json, sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR))
from config.settings import CACHE_DIR

cache_meme_name = CACHE_DIR / "meme_name.json"

def meme_name_from_user():
    if cache_meme_name.exists():
        with open(cache_meme_name, "r", encoding="utf-8") as f:
            return json.load(f)["meme_name"]

    #  meme_name = input("검색할 밈을 입력하세요 : ").strip().lstrip("#")
    meme_name = "sample"
    with open(cache_meme_name, "w", encoding="utf-8") as f:
        json.dump({"meme_name": meme_name}, f, ensure_ascii=False)
    return meme_name