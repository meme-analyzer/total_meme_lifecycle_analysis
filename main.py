#!/usr/bin/env python3
"""
TOTAL MEME LIFECYCLE ANALYSIS - 통합 메인 스크립트
모든 플랫폼(Instagram, Reddit, Twitter)의 밈 분석을 통합 관리
"""

import os
import sys
import subprocess
import argparse
import time
from datetime import datetime
import json

class TotalMemeAnalyzer:
    def __init__(self):
        """통합 밈 분석기 초기화"""
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.platforms = {
            'instagram': {
                'dir': 'instagram_meme_lifecycle_analysis',
                'script': 'pipeline.py',
                'name': 'Instagram'
            },
            'reddit': {
                'dir': 'reddit_meme_lifecycle_analysis', 
                'script': 'run_pipeline.py',
                'name': 'Reddit'
            },
            'twitter': {
                'dir': 'twitter_meme_lifecycle_analysis',
                'script': 'run_pipeline_twitter.py', 
                'name': 'Twitter'
            }
        }
        
        # 결과 저장용 디렉토리
        self.results_dir = os.path.join(self.base_dir, 'integrated_results')
        os.makedirs(self.results_dir, exist_ok=True)
    
    def check_platform_availability(self):
        """각 플랫폼 스크립트 존재 여부 확인"""
        available_platforms = {}
        
        for platform, config in self.platforms.items():
            platform_dir = os.path.join(self.base_dir, config['dir'])
            script_path = os.path.join(platform_dir, config['script'])
            
            if os.path.exists(script_path):
                available_platforms[platform] = {
                    'path': script_path,
                    'dir': platform_dir,
                    'name': config['name'],
                    'available': True
                }
                print(f"✅ {config['name']} 파이프라인 발견: {script_path}")
            else:
                available_platforms[platform] = {
                    'path': script_path,
                    'dir': platform_dir, 
                    'name': config['name'],
                    'available': False
                }
                print(f"❌ {config['name']} 파이프라인 없음: {script_path}")
        
        return available_platforms
    
    def run_platform_analysis(self, platform, meme_name, additional_args=None):
        """특정 플랫폼에서 밈 분석 실행"""
        available_platforms = self.check_platform_availability()
        
        if platform not in available_platforms:
            print(f"❌ 지원하지 않는 플랫폼: {platform}")
            return False
        
        platform_info = available_platforms[platform]
        
        if not platform_info['available']:
            print(f"❌ {platform_info['name']} 파이프라인을 찾을 수 없습니다.")
            return False
        
        print(f"\n{'='*60}")
        print(f"🚀 {platform_info['name']} 파이프라인 실행 시작")
        print(f"밈: {meme_name}")
        print(f"시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        
        # 명령어 구성
        cmd = [sys.executable, platform_info['path'], '--meme', meme_name]
        
        # 추가 인자가 있으면 포함
        if additional_args:
            cmd.extend(additional_args)
        
        # 작업 디렉토리를 플랫폼 디렉토리로 변경
        original_cwd = os.getcwd()
        
        try:
            os.chdir(platform_info['dir'])
            print(f"📁 작업 디렉토리: {platform_info['dir']}")
            print(f"🔧 실행 명령어: {' '.join(cmd)}")
            print()
            
            # 파이프라인 실행
            start_time = time.time()
            result = subprocess.run(cmd, capture_output=False, text=True)
            end_time = time.time()
            
            if result.returncode == 0:
                print(f"\n✅ {platform_info['name']} 분석 완료!")
                print(f"⏱️  소요 시간: {end_time - start_time:.2f}초")
                return True
            else:
                print(f"\n❌ {platform_info['name']} 분석 실패 (종료 코드: {result.returncode})")
                return False
                
        except Exception as e:
            print(f"❌ {platform_info['name']} 실행 중 오류: {e}")
            return False
        finally:
            os.chdir(original_cwd)
    
    def run_multi_platform_analysis(self, platforms, meme_name, additional_args=None):
        """여러 플랫폼에서 동시 분석"""
        print(f"\n🎯 다중 플랫폼 분석 시작")
        print(f"밈: {meme_name}")
        print(f"플랫폼: {', '.join([p.title() for p in platforms])}")
        
        results = {}
        total_start_time = time.time()
        
        for platform in platforms:
            print(f"\n🔄 {platform.title()} 분석 중...")
            success = self.run_platform_analysis(platform, meme_name, additional_args)
            results[platform] = success
            
            if success:
                print(f"✅ {platform.title()} 완료")
            else:
                print(f"❌ {platform.title()} 실패")
            
            # 플랫폼 간 대기 시간 (API 제한 고려)
            if platform != platforms[-1]:  # 마지막이 아니면
                print("⏳ 플랫폼 전환 대기... (10초)")
                time.sleep(10)
        
        total_end_time = time.time()
        
        # 결과 요약
        print(f"\n{'='*60}")
        print(f"🏁 다중 플랫폼 분석 완료")
        print(f"⏱️  총 소요 시간: {total_end_time - total_start_time:.2f}초")
        print(f"{'='*60}")
        
        success_count = sum(results.values())
        total_count = len(results)
        
        print(f"📊 성공률: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")
        
        for platform, success in results.items():
            status = "✅" if success else "❌"
            print(f"  {status} {platform.title()}")
        
        # 결과 저장
        self.save_analysis_summary(meme_name, platforms, results)
        
        return results
    
    def save_analysis_summary(self, meme_name, platforms, results):
        """분석 결과 요약 저장"""
        summary = {
            'meme_name': meme_name,
            'analysis_date': datetime.now().isoformat(),
            'platforms_analyzed': platforms,
            'results': results,
            'success_rate': sum(results.values()) / len(results),
            'total_platforms': len(platforms),
            'successful_platforms': sum(results.values())
        }
        
        summary_file = os.path.join(
            self.results_dir, 
            f"{meme_name.replace(' ', '_').lower()}_analysis_summary.json"
        )
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        print(f"📄 분석 요약 저장: {summary_file}")
    
    def list_available_platforms(self):
        """사용 가능한 플랫폼 목록 출력"""
        print("\n🌐 플랫폼 상태 확인")
        print("="*50)
        
        available_platforms = self.check_platform_availability()
        
        available = []
        unavailable = []
        
        for platform, info in available_platforms.items():
            if info['available']:
                available.append(platform)
            else:
                unavailable.append(platform)
        
        if available:
            print(f"\n✅ 사용 가능한 플랫폼 ({len(available)}개):")
            for platform in available:
                print(f"  • {platform.title()}")
        
        if unavailable:
            print(f"\n❌ 사용 불가능한 플랫폼 ({len(unavailable)}개):")
            for platform in unavailable:
                print(f"  • {platform.title()}")
                print(f"    경로: {available_platforms[platform]['path']}")
        
        return available, unavailable
    
    def interactive_mode(self):
        """대화형 모드"""
        print("\n🎭 TOTAL MEME LIFECYCLE ANALYSIS")
        print("="*50)
        print("대화형 모드에 오신 것을 환영합니다!")
        
        # 플랫폼 확인
        available, unavailable = self.list_available_platforms()
        
        if not available:
            print("\n❌ 사용 가능한 플랫폼이 없습니다.")
            return
        
        # 밈 이름 입력
        print(f"\n📝 분석할 밈 이름을 입력하세요:")
        meme_name = input("밈 이름: ").strip()
        
        if not meme_name:
            print("❌ 밈 이름이 입력되지 않았습니다.")
            return
        
        # 플랫폼 선택
        print(f"\n🌐 분석할 플랫폼을 선택하세요:")
        print("1. 모든 플랫폼")
        for i, platform in enumerate(available, 2):
            print(f"{i}. {platform.title()}만")
        print(f"{len(available)+2}. 커스텀 선택")
        
        try:
            choice = int(input("선택 (번호): "))
        except ValueError:
            print("❌ 올바른 번호를 입력하세요.")
            return
        
        if choice == 1:
            selected_platforms = available
        elif 2 <= choice <= len(available)+1:
            selected_platforms = [available[choice-2]]
        elif choice == len(available)+2:
            print(f"\n분석할 플랫폼을 선택하세요 (쉼표로 구분):")
            for i, platform in enumerate(available):
                print(f"  {platform}")
            
            platform_input = input("플랫폼들: ").strip()
            selected_platforms = [p.strip().lower() for p in platform_input.split(',')]
            selected_platforms = [p for p in selected_platforms if p in available]
            
            if not selected_platforms:
                print("❌ 올바른 플랫폼이 선택되지 않았습니다.")
                return
        else:
            print("❌ 올바른 선택이 아닙니다.")
            return
        
        # 실행 확인
        print(f"\n🎯 실행 설정:")
        print(f"  밈: {meme_name}")
        print(f"  플랫폼: {', '.join([p.title() for p in selected_platforms])}")
        
        confirm = input("\n실행하시겠습니까? (y/N): ").strip().lower()
        
        if confirm == 'y':
            if len(selected_platforms) == 1:
                self.run_platform_analysis(selected_platforms[0], meme_name)
            else:
                self.run_multi_platform_analysis(selected_platforms, meme_name)
        else:
            print("❌ 실행이 취소되었습니다.")

def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(
        description='TOTAL MEME LIFECYCLE ANALYSIS - 통합 밈 분석 시스템',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  # 대화형 모드
  python main.py
  
  # Reddit에서 특정 밈 분석
  python main.py --meme "chill guy" --platform reddit
  
  # 모든 플랫폼에서 분석
  python main.py --meme "wojak" --platform all
  
  # 여러 플랫폼 선택
  python main.py --meme "pepe" --platform reddit twitter
  
  # 플랫폼 상태 확인
  python main.py --list-platforms
        """
    )
    
    parser.add_argument('--meme', type=str,
                       help='분석할 밈 이름')
    parser.add_argument('--platform', nargs='+', 
                       choices=['instagram', 'reddit', 'twitter', 'all'],
                       help='분석할 플랫폼')
    parser.add_argument('--list-platforms', action='store_true',
                       help='사용 가능한 플랫폼 목록 출력')
    parser.add_argument('--interactive', action='store_true',
                       help='대화형 모드 실행')
    parser.add_argument('--skip-collection', action='store_true',
                       help='데이터 수집 건너뛰기 (모든 플랫폼에 적용)')
    parser.add_argument('--skip-visualization', action='store_true',
                       help='시각화 건너뛰기 (모든 플랫폼에 적용)')
    parser.add_argument('--skip-analysis', action='store_true',
                       help='분석 건너뛰기 (모든 플랫폼에 적용)')
    
    args = parser.parse_args()
    
    # 통합 분석기 생성
    analyzer = TotalMemeAnalyzer()
    
    # 플랫폼 목록 출력
    if args.list_platforms:
        analyzer.list_available_platforms()
        return
    
    # 대화형 모드 또는 인자 없을 때
    if args.interactive or (not args.meme and not args.platform):
        analyzer.interactive_mode()
        return
    
    # 밈 이름 필수 체크
    if not args.meme:
        print("❌ --meme 인자가 필요합니다. --help를 참고하세요.")
        return
    
    if not args.platform:
        print("❌ --platform 인자가 필요합니다. --help를 참고하세요.")
        return
    
    # 추가 인자 구성
    additional_args = []
    if args.skip_collection:
        additional_args.append('--skip-collection')
    if args.skip_visualization:
        additional_args.append('--skip-visualization') 
    if args.skip_analysis:
        additional_args.append('--skip-analysis')
    
    # 플랫폼 처리
    if 'all' in args.platform:
        available, _ = analyzer.list_available_platforms()
        platforms = available
    else:
        platforms = args.platform
    
    # 실행
    try:
        if len(platforms) == 1:
            analyzer.run_platform_analysis(platforms[0], args.meme, additional_args)
        else:
            analyzer.run_multi_platform_analysis(platforms, args.meme, additional_args)
    except KeyboardInterrupt:
        print("\n\n⛔ 사용자에 의해 중단되었습니다.")
    except Exception as e:
        print(f"\n❌ 실행 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()