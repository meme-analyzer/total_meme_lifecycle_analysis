#!/usr/bin/env python3
"""
TOTAL MEME LIFECYCLE ANALYSIS 프로젝트 구조 설정 스크립트
"""

import os
import shutil

def create_project_structure():
    """프로젝트 디렉토리 구조 생성"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 기본 디렉토리 구조
    directories = [
        'instagram_meme_lifecycle_analysis',
        'reddit_meme_lifecycle_analysis', 
        'twitter_meme_lifecycle_analysis',
        'integrated_results',
        'integrated_results/reports',
        'integrated_results/figures',
        'integrated_results/summaries'
    ]
    
    print("📁 프로젝트 디렉토리 구조 생성 중...")
    
    for directory in directories:
        dir_path = os.path.join(base_dir, directory)
        os.makedirs(dir_path, exist_ok=True)
        print(f"  ✅ {directory}")
    
    return base_dir

def create_readme():
    """통합 README 파일 생성"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    readme_path = os.path.join(base_dir, 'README.md')
    
    readme_content = """# TOTAL MEME LIFECYCLE ANALYSIS

통합 밈 수명 주기 분석 시스템 - Instagram, Reddit, Twitter 플랫폼 통합 분석

## 📁 프로젝트 구조

```
TOTAL_MEME_LIFECYCLE_ANALYSIS/
├── main.py                              # 통합 메인 스크립트
├── setup.py                             # 프로젝트 설정
├── README.md                            # 이 파일
├── integrated_results/                  # 통합 분석 결과
│   ├── reports/                         # 통합 보고서
│   ├── figures/                         # 통합 시각화
│   └── summaries/                       # 분석 요약
├── instagram_meme_lifecycle_analysis/   # Instagram 분석
│   └── pipeline.py                      # Instagram 파이프라인
├── reddit_meme_lifecycle_analysis/      # Reddit 분석  
│   └── run_pipeline.py                  # Reddit 파이프라인
└── twitter_meme_lifecycle_analysis/     # Twitter 분석
    └── run_pipeline_twitter.py          # Twitter 파이프라인
```

## 🚀 빠른 시작

### 1. 대화형 모드 (추천)
```bash
python main.py
```

### 2. 명령어 모드
```bash
# 특정 플랫폼에서 밈 분석
python main.py --meme "chill guy" --platform reddit

# 모든 플랫폼에서 분석
python main.py --meme "wojak" --platform all

# 여러 플랫폼 선택
python main.py --meme "pepe" --platform reddit twitter

# 플랫폼 상태 확인
python main.py --list-platforms
```

## 📊 지원 플랫폼

- **Instagram**: `instagram_meme_lifecycle_analysis/pipeline.py`
- **Reddit**: `reddit_meme_lifecycle_analysis/run_pipeline.py`  
- **Twitter**: `twitter_meme_lifecycle_analysis/run_pipeline_twitter.py`

## 🔧 설정

각 플랫폼별 디렉토리에서 개별 설정 필요:
- API 키 설정
- 환경 변수 구성
- 필요한 라이브러리 설치

## 📈 결과물

- **통합 요약**: `integrated_results/summaries/`
- **플랫폼별 상세 결과**: 각 플랫폼 디렉토리 내 `results/` 폴더

## 🆘 도움말

```bash
python main.py --help
```
"""
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"📝 README.md 생성: {readme_path}")

def check_platform_scripts():
    """각 플랫폼 스크립트 존재 여부 확인"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    scripts = {
        'Instagram': 'instagram_meme_lifecycle_analysis/pipeline.py',
        'Reddit': 'reddit_meme_lifecycle_analysis/run_pipeline.py',
        'Twitter': 'twitter_meme_lifecycle_analysis/run_pipeline_twitter.py'
    }
    
    print("\n🔍 플랫폼 스크립트 확인:")
    
    missing_scripts = []
    
    for platform, script_path in scripts.items():
        full_path = os.path.join(base_dir, script_path)
        if os.path.exists(full_path):
            print(f"  ✅ {platform}: {script_path}")
        else:
            print(f"  ❌ {platform}: {script_path} (없음)")
            missing_scripts.append((platform, script_path))
    
    if missing_scripts:
        print(f"\n⚠️  누락된 스크립트 {len(missing_scripts)}개:")
        for platform, path in missing_scripts:
            print(f"  • {platform}: {path}")
        print(f"\n📝 누락된 스크립트를 해당 디렉토리에 복사하세요.")
    else:
        print(f"\n✅ 모든 플랫폼 스크립트가 준비되었습니다!")

def create_sample_config():
    """샘플 설정 파일 생성"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, 'config.sample.json')
    
    sample_config = {
        "default_platforms": ["reddit"],
        "analysis_settings": {
            "skip_collection": False,
            "skip_visualization": False, 
            "skip_analysis": False
        },
        "output_settings": {
            "integrated_results_dir": "integrated_results",
            "save_summaries": True,
            "generate_reports": True
        },
        "platform_priorities": {
            "reddit": 1,
            "twitter": 2,
            "instagram": 3
        }
    }
    
    import json
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(sample_config, f, ensure_ascii=False, indent=2)
    
    print(f"⚙️  샘플 설정 파일 생성: {config_path}")

def main():
    """설정 스크립트 메인 함수"""
    print("🎭 TOTAL MEME LIFECYCLE ANALYSIS 설정")
    print("="*50)
    
    # 1. 디렉토리 구조 생성
    base_dir = create_project_structure()
    
    # 2. README 생성
    create_readme()
    
    # 3. 샘플 설정 파일 생성
    create_sample_config()
    
    # 4. 플랫폼 스크립트 확인
    check_platform_scripts()
    
    print(f"\n🎉 설정 완료!")
    print(f"📁 프로젝트 루트: {base_dir}")
    print(f"\n다음 단계:")
    print(f"1. 각 플랫폼 디렉토리에 필요한 스크립트 복사")
    print(f"2. API 키 및 환경 설정")
    print(f"3. python main.py 실행")

if __name__ == "__main__":
    main()