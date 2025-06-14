from pathlib import Path
import json
import pandas as pd
import sys, re, string

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR))
from config.settings import DATA_DIR, SRC_DIR

sys.path.append(str(SRC_DIR))
from utils.input_utils import meme_name_from_user

# 데이터 파일 경로
meme_name = meme_name_from_user()
filename_before = f"{meme_name}_instagram.json"
filename_after = f"{meme_name}_instagram.csv"
input_path = DATA_DIR / "raw" / filename_before
output_path = DATA_DIR / "preprocessed" / filename_after
output_path.parent.mkdir(parents=True, exist_ok=True)

# 파일 로드
with open(input_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# JSON 데이터 로드
df = pd.read_json(input_path)

# 작업 1 - 날짜 처리
df["upload_time"] = pd.to_datetime(df["upload_time"])

# 작업 2 - 결측치 처리
df = df.dropna(subset=["likes"])

# 작업 3 - 파생 변수 생성
df["year"] = df["upload_time"].dt.year
df["month"] = df["upload_time"].dt.month
df["day"] = df["upload_time"].dt.day
df["weekday"] = df["upload_time"].dt.day_name()

# 작업 4 - caption 토큰화
CHO = ["ㄱ", "ㄲ", "ㄴ", "ㄷ", "ㄸ", "ㄹ", "ㅁ", "ㅂ", "ㅃ", "ㅅ",
       "ㅆ", "ㅇ", "ㅈ", "ㅉ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]
JUNG = ["ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ", "ㅔ", "ㅕ", "ㅖ", "ㅗ", "ㅘ",
        "ㅙ", "ㅚ", "ㅛ", "ㅜ", "ㅝ", "ㅞ", "ㅟ", "ㅠ", "ㅡ", "ㅢ", "ㅣ"]
JONG = ["", "ㄱ", "ㄲ", "ㄳ", "ㄴ", "ㄵ", "ㄶ", "ㄷ", "ㄹ", "ㄺ",
        "ㄻ", "ㄼ", "ㄽ", "ㄾ", "ㄿ", "ㅀ", "ㅁ", "ㅂ", "ㅄ",
        "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]

def clean_text(text):
    return re.sub(r'[^A-Za-z0-9가-힣ㄱ-ㅎ\s]', '', str(text))

def decompose_hangul(ch):
    code = ord(ch)
    if 0xAC00 <= code <= 0xD7A3:
        base = code - 0xAC00
        cho = CHO[base // 588]
        jung = JUNG[(base % 588) // 28]
        jong_idx = base % 28
        jong = JONG[jong_idx] if jong_idx != 0 else None
        return cho, jung, jong
    elif 0x3131 <= code <= 0x314E:
        return ch, None, None
    elif 0x314F <= code <= 0x3163:
        return None, ch, None
    return None, None, None

def compress_decompose(text):
    text = clean_text(text)
    result = []

    for word in text.split():
        buffer = ""
        group = []

        for ch in word:
            if ch in string.ascii_letters:
                buffer += ch
                continue
            else:
                if buffer:
                    result.append([{"ENG": buffer}])
                    buffer = ""

            cho, jung, jong = decompose_hangul(ch)
            units = []
            if cho: units.append({"CHO": cho})
            if jung: units.append({"JUNG": jung})
            if jong: units.append({"JONG": jong})

            if len(units) == 1:
                result.append(units)
            elif units:
                group.extend(units)

        if buffer:
            result.append([{"ENG": buffer}])
        if group:
            result.append(group)

    return result

df["caption_tokens"] = df["caption"].apply(compress_decompose)
df.drop(columns=["caption"], inplace=True)

# 결과 저장
df.to_csv(output_path, index=False, encoding="utf-8-sig")