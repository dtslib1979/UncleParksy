#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 UncleParksy 옵시디언 백업 트리거
간편한 수동 실행을 위한 래퍼 스크립트

사용법:
python run_obsidian_backup.py

작가지망생 박씨의 마감작업을 위한 간편 백업 도구
"""

import subprocess
import sys
from pathlib import Path

def main():
    """🚀 옵시디언 백업 실행"""
    print("🎯 UncleParksy 옵시디언 백업 시작...")
    print("📝 현재 설정에 따라 모든 콘텐츠를 백업합니다\n")
    
    # 백업 스크립트 경로
    script_path = Path(__file__).parent / "scripts" / "obsidian_comprehensive_backup.py"
    
    if not script_path.exists():
        print(f"❌ 백업 스크립트를 찾을 수 없습니다: {script_path}")
        return 1
    
    try:
        # 백업 스크립트 실행
        result = subprocess.run([
            sys.executable, str(script_path)
        ], cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print("\n🎉 백업 완료!")
            print("📁 Obsidian에서 '_obsidian/_imports' 폴더를 볼트로 열어보세요!")
            print("📋 백업 상세는 '_obsidian/_imports/BACKUP_INDEX.md'에서 확인하세요")
        else:
            print(f"\n❌ 백업 실패 (종료 코드: {result.returncode})")
            return result.returncode
            
    except Exception as e:
        print(f"❌ 백업 실행 오류: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())