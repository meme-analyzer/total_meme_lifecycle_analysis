# 📊 Meme Lifecycle Analysis Project

> SNS에서 유행하는 밈(Meme)의 생성부터 소멸까지의 수명 주기를 데이터 기반으로 분석하는 프로젝트입니다.

---

## 📌 프로젝트 개요

밈은 현대 인터넷 문화의 핵심 요소로, 빠르게 생성되고 빠르게 소멸합니다.  
본 프로젝트는 밈의 생애 주기를 분석하고, 확산 속도, 영향 요인, 플랫폼별 패턴 등을 시각화하여 **디지털 트렌드와 정보 전파 메커니즘**을 이해하고자 합니다.

---

## 👥 팀 정보

- **팀명**: 오차봉임
- **팀원**:
  - 오수민 (20212308) – 데이터 전처리 및 분석
  - 차지태 (20202768) – 데이터 수집 및 크롤링
  - 봉가은 (팀장, 20202705) – 시각화 및 결과 해석

---

## 🛠️ 기술 스택 및 도구

- **언어**: Python 3.9+
- **수집 도구**: `snscrape`, `PRAW`, `Instaloader`, `Selenium`
- **분석 도구**: `pandas`, `numpy`, `scikit-learn`, `spaCy`, `lifelines`, `NetworkX`
- **시각화 도구**: `matplotlib`, `seaborn`, `plotly`, `Dash`, `Pyvis`
- **환경변수 관리**: `python-dotenv`

---

## 📂 프로젝트 구조

요약

```
meme-lifecycle-analysis/
├── data/               # 수집 및 전처리된 데이터
├── notebooks/          # Jupyter 분석 노트북
├── src/                # 주요 기능별 Python 모듈
├── dashboard/          # 대시보드 앱
├── models/             # 분석 모델 저장소
├── results/            # 결과 이미지 및 통계
├── reports/            # 보고서 및 발표자료
├── tests/              # 유닛 테스트
├── .env                # (비공개) API 키 등 민감 정보
├── .env.example        # 환경변수 템플릿
├── requirements.txt    # 설치 패키지 목록
└── README.md           # 현재 문서
```

전체

```
meme-lifecycle-analysis/
src/
├── config/
│   ├── __init__.py        # config 모듈로 인식되게 함
│   ├── env.py             # .env 로딩 및 환경변수 접근
│   └── settings.py        # 공통 설정 변수 정의 (예: 경로, 상수 등)
│
├── data/                            # 데이터 저장 폴더
│   ├── raw/                         # 원시 데이터
│   ├── preprocessed/                   # 전처리 완료 데이터
│   └── external/                    # 외부 참고 자료
│
├── notebooks/                       # 분석용 Jupyter 노트북
│   ├── 01_data_collection.ipynb
│   ├── 02_preprocessing.ipynb
│   ├── 03_analysis.ipynb
│   └── 04_visualization.ipynb
│
├── src/                             # 프로젝트 코드 모듈
│   ├── data_collection/             # SNS 크롤러 코드
│   ├── preprocessing/               # 정제 및 변환 코드
│   ├── analysis/                    # 분석 및 모델링 코드
│   ├── visualization/               # 시각화 함수
│   └── utils/                       # 공통 유틸리티 함수
│
├── dashboard/                       # 대시보드 코드 (Dash, Streamlit 등)
│   └── app.py
│
├── models/                          # 모델 파일 저장 폴더
│
├── results/                         # 분석 결과 및 이미지
│
├── reports/                         # 문서 및 발표자료
│   ├── final_report.pdf
│   └── presentation.pptx
│
├── tests/                           # 테스트 코드
│
├── .env                             # [🔒 Git에 올리지 않음] 민감정보 저장
├── .env.example                     # [공유용] .env 템플릿
├── .gitignore                       # Git 제외 파일 설정
├── requirements.txt                 # 패키지 리스트
└── README.md                        # 프로젝트 설명서
```

---

## ⚙️ 설치 및 실행 방법

1. **패키지 설치**

```bash
pip install -r requirements.txt
```

2. **환경 변수 설정**
   `.env.example`을 참고하여 `.env` 파일을 생성하고 필요한 API 키를 입력하세요.

3. **노트북 실행 또는 분석 스크립트 실행**

```bash
jupyter notebook
# 또는
python src/analysis/meme_lifecycle_analysis.py
```

---

## 📈 기대 효과

- SNS 밈 수명 주기의 정량 분석 및 시각화
- 마케팅, 트렌드 예측, 디지털 문화 연구에 활용 가능한 분석 프레임워크 제공
- 인터랙티브 대시보드를 통한 실시간 트렌드 모니터링

---

## 📄 라이선스

본 프로젝트는 학습 및 연구 목적이며, 상업적 용도로의 무단 사용을 금합니다.
