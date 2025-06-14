from pathlib import Path
from collections import Counter
from difflib import SequenceMatcher
import pandas as pd
import sys

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR))
from config.settings import DATA_DIR, SRC_DIR

sys.path.append(str(SRC_DIR))
from utils.input_utils import meme_name_from_user

# 데이터 파일 경로
meme_name = meme_name_from_user()
filename_before = f"{meme_name}_instagram.csv"
filename_after = f"{meme_name}_keywords.csv"

input_path = DATA_DIR / "preprocessed" / filename_before
output_path = DATA_DIR / "analysis" / f"{meme_name}" /  "keywords"
output_path.mkdir(parents=True, exist_ok=True)


df = pd.read_csv(input_path, converters={"caption_tokens": eval})
print(type(df["caption_tokens"].iloc[0]))


CHO = ["ㄱ", "ㄲ", "ㄴ", "ㄷ", "ㄸ", "ㄹ", "ㅁ", "ㅂ", "ㅃ", "ㅅ",
       "ㅆ", "ㅇ", "ㅈ", "ㅉ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]
JUNG = ["ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ", "ㅔ", "ㅕ", "ㅖ", "ㅗ", "ㅘ",
        "ㅙ", "ㅚ", "ㅛ", "ㅜ", "ㅝ", "ㅞ", "ㅟ", "ㅠ", "ㅡ", "ㅢ", "ㅣ"]
JONG = ["", "ㄱ", "ㄲ", "ㄳ", "ㄴ", "ㄵ", "ㄶ", "ㄷ", "ㄹ", "ㄺ",
        "ㄻ", "ㄼ", "ㄽ", "ㄾ", "ㄿ", "ㅀ", "ㅁ", "ㅂ", "ㅄ",
        "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]

# 음절 조합 함수
def combine_units(units):
    result = ""
    i = 0
    while i < len(units):
        if i + 1 < len(units) and "CHO" in units[i] and "JUNG" in units[i + 1]:
            cho_idx = CHO.index(units[i]["CHO"])
            jung_idx = JUNG.index(units[i + 1]["JUNG"])
            if i + 2 < len(units) and "JONG" in units[i + 2]:
                jong_idx = JONG.index(units[i + 2]["JONG"])
                i += 3
            else:
                jong_idx = 0
                i += 2
            result += chr(0xAC00 + cho_idx * 588 + jung_idx * 28 + jong_idx)
        else:
            for val in units[i].values():
                result += val
            i += 1
    return result

def extract_keywords(df):
    counter = Counter()
    for token_list in df["caption_tokens"]:
        for token in token_list:
            if len(token) == 1 and "ENG" in token[0]:
                word = token[0]["ENG"]
            else:
                word = combine_units(token)
            counter[word] += 1
    return counter.most_common()

keywords = extract_keywords(df)

# 저장
import pandas as pd
top_df = pd.DataFrame(keywords, columns=["word", "count"])
top_df.to_csv(output_path / f"{meme_name}_keywords.csv", index=False, encoding="utf-8-sig")