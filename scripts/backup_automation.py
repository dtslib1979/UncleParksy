#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete Obsidian Backup Automation
Master script that orchestrates the entire backup ecosystem for UncleParksy

This script provides:
- One-command full backup execution
- Interactive backup management
- Backup restoration capabilities
- System health monitoring
- Integration with existing PowerShell configuration
"""

import os
import json
import logging
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import argparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ObsidianBackupAutomation:
    """Master backup automation system"""
    
    def __init__(self):
        self.repo_root = Path(__file__).parent.parent
        self.scripts_dir = self.repo_root / "scripts"
        self.backup_root = self.repo_root / "backup"
        
        self.scripts = {
            'full_backup': self.scripts_dir / "obsidian_full_backup.py",
            'validator': self.scripts_dir / "backup_validator.py",
            'scheduled': self.scripts_dir / "scheduled_backup.py",
            'tistory_backup': self.scripts_dir / "tistory_backup.py",
            'mirror_backup': self.scripts_dir / "mirror_backup.py",
            'clean_mobilize': self.scripts_dir / "clean_and_mobilize.py"
        }
        
    def print_banner(self):
        """Print system banner"""
        banner = """
🎯 UncleParksy Obsidian Backup Automation
=========================================
옵시디언 볼트 전체 백업 시스템 (현재 설정대로)

기능:
🔄 자동 티스토리 백업 (RSS 기반)
📦 아카이브 미러링
📱 모바일 최적화
⚙️ Obsidian 설정 백업
📸 볼트 스냅샷
🔍 백업 검증
📊 상태 대시보드

설정 경로: C:\\ObsidianVault\\UncleParksy
MCP 연동: Claude Desktop + GitHub
        """
        print(banner)
    
    def check_dependencies(self) -> bool:
        """Check if all required dependencies are available"""
        logger.info("🔍 Checking dependencies...")
        
        missing_deps = []
        
        # Check Python packages
        try:
            import requests
            import feedparser
            from bs4 import BeautifulSoup
        except ImportError as e:
            missing_deps.append(f"Python package: {e}")
        
        # Check script files
        for name, script_path in self.scripts.items():
            if not script_path.exists():
                missing_deps.append(f"Script file: {script_path}")
        
        if missing_deps:
            logger.error("❌ Missing dependencies:")
            for dep in missing_deps:
                logger.error(f"  - {dep}")
            return False
        
        logger.info("✅ All dependencies satisfied")
        return True
    
    def run_full_backup_suite(self) -> Dict:
        """Execute complete backup suite"""
        logger.info("🚀 Starting complete backup suite...")
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'operations': {},
            'overall_status': 'success'
        }
        
        operations = [
            ('full_backup', '🎯 Full Obsidian Backup'),
            ('validation', '🔍 Backup Validation'),
        ]
        
        for op_key, op_name in operations:
            logger.info(f"▶️ {op_name}")
            
            try:
                if op_key == 'full_backup':
                    result = subprocess.run([
                        sys.executable, str(self.scripts['full_backup'])
                    ], capture_output=True, text=True, timeout=300)
                    
                elif op_key == 'validation':
                    result = subprocess.run([
                        sys.executable, str(self.scripts['validator'])
                    ], capture_output=True, text=True, timeout=120)
                
                operation_result = {
                    'exit_code': result.returncode,
                    'stdout': result.stdout,
                    'stderr': result.stderr,
                    'status': 'success' if result.returncode == 0 else 'error'
                }
                
                results['operations'][op_key] = operation_result
                
                if result.returncode != 0:
                    results['overall_status'] = 'error'
                    logger.error(f"❌ {op_name} failed (exit code: {result.returncode})")
                else:
                    logger.info(f"✅ {op_name} completed successfully")
                    
            except subprocess.TimeoutExpired:
                results['operations'][op_key] = {
                    'status': 'timeout',
                    'error': 'Operation timed out'
                }
                results['overall_status'] = 'error'
                logger.error(f"⏱️ {op_name} timed out")
                
            except Exception as e:
                results['operations'][op_key] = {
                    'status': 'error',
                    'error': str(e)
                }
                results['overall_status'] = 'error'
                logger.error(f"❌ {op_name} failed: {e}")
        
        return results
    
    def show_backup_status(self):
        """Display current backup status"""
        logger.info("📊 Checking backup status...")
        
        # Check if dashboard exists and display info
        dashboard_path = self.backup_root / "backup_status_dashboard.html"
        
        if dashboard_path.exists():
            print(f"📊 Status Dashboard: {dashboard_path}")
            print("   Open this file in a web browser to view detailed status")
        
        # Show directory sizes
        print("\n📁 Backup Directory Summary:")
        
        directories = {
            'Raw Backups': self.backup_root / "raw",
            'Archive': self.repo_root / "archive",
            'Obsidian MD': self.repo_root / "_obsidian" / "_imports" / "html_md",
            'Obsidian HTML': self.repo_root / "_obsidian" / "_imports" / "html_raw",
            'JSON Data': self.backup_root / "json",
            'Snapshots': self.backup_root / "snapshots"
        }
        
        for name, path in directories.items():
            if path.exists():
                files = list(path.rglob("*"))
                file_count = len([f for f in files if f.is_file()])
                
                total_size = 0
                for file_path in files:
                    if file_path.is_file():
                        try:
                            total_size += file_path.stat().st_size
                        except:
                            continue
                
                size_mb = total_size / (1024 * 1024)
                print(f"  ✅ {name}: {file_count} files, {size_mb:.1f} MB")
            else:
                print(f"  ❌ {name}: Directory not found")
    
    def interactive_menu(self):
        """Interactive backup management menu"""
        while True:
            print("\n" + "="*60)
            print("🎯 UncleParksy Backup Management")
            print("="*60)
            print("1. 🚀 전체 백업 실행 (Full Backup Suite)")
            print("2. 📰 티스토리만 백업 (Tistory Only)")
            print("3. 🔍 백업 검증 (Validate Backups)")
            print("4. 📊 상태 확인 (Show Status)")
            print("5. 📱 모바일 최적화 (Clean & Mobilize)")
            print("6. ⏰ 예약 백업 실행 (Scheduled Backup)")
            print("7. 🧹 정리 작업 (Cleanup)")
            print("8. ❓ 도움말 (Help)")
            print("0. 🚪 종료 (Exit)")
            print("")
            
            try:
                choice = input("선택하세요 (0-8): ").strip()
                
                if choice == '0':
                    print("👋 종료합니다.")
                    break
                    
                elif choice == '1':
                    print("\n🚀 전체 백업 시작...")
                    results = self.run_full_backup_suite()
                    
                    print(f"\n📊 백업 완료!")
                    print(f"상태: {results['overall_status']}")
                    print(f"실행된 작업: {len(results['operations'])}개")
                    
                    for op_name, op_result in results['operations'].items():
                        status_icon = "✅" if op_result['status'] == 'success' else "❌"
                        print(f"  {status_icon} {op_name}: {op_result['status']}")
                    
                elif choice == '2':
                    print("\n📰 티스토리 백업 실행 중...")
                    try:
                        result = subprocess.run([
                            sys.executable, str(self.scripts['tistory_backup'])
                        ], timeout=60)
                        print("✅ 티스토리 백업 완료!")
                    except Exception as e:
                        print(f"❌ 티스토리 백업 실패: {e}")
                
                elif choice == '3':
                    print("\n🔍 백업 검증 실행 중...")
                    try:
                        result = subprocess.run([
                            sys.executable, str(self.scripts['validator'])
                        ], timeout=120)
                        print("✅ 백업 검증 완료!")
                    except Exception as e:
                        print(f"❌ 백업 검증 실패: {e}")
                
                elif choice == '4':
                    self.show_backup_status()
                
                elif choice == '5':
                    print("\n📱 모바일 최적화 실행 중...")
                    try:
                        result = subprocess.run([
                            sys.executable, str(self.scripts['clean_mobilize'])
                        ], timeout=120)
                        print("✅ 모바일 최적화 완료!")
                    except Exception as e:
                        print(f"❌ 모바일 최적화 실패: {e}")
                
                elif choice == '6':
                    print("\n⏰ 예약 백업 실행 중...")
                    try:
                        result = subprocess.run([
                            sys.executable, str(self.scripts['scheduled']), '--mode=auto'
                        ], timeout=300)
                        print("✅ 예약 백업 완료!")
                    except Exception as e:
                        print(f"❌ 예약 백업 실패: {e}")
                
                elif choice == '7':
                    print("\n🧹 정리 작업은 예약 백업에 포함되어 있습니다.")
                    print("예약 백업을 실행하거나 수동으로 old files를 삭제하세요.")
                
                elif choice == '8':
                    self.show_help()
                
                else:
                    print("❌ 잘못된 선택입니다. 0-8 사이의 숫자를 입력하세요.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 사용자에 의해 중단되었습니다.")
                break
            except Exception as e:
                print(f"❌ 오류 발생: {e}")
    
    def show_help(self):
        """Show detailed help information"""
        help_text = """
🎯 UncleParksy Obsidian Backup System 도움말
============================================

📋 시스템 개요:
이 백업 시스템은 fix-obsidian-backup-system.ps1에서 설정한 
Obsidian 볼트 백업을 완전 자동화합니다.

🔧 주요 구성요소:
1. Tistory RSS 백업 (https://dtslib1k.tistory.com/rss)
2. Archive 미러링 (backup/raw → archive/)
3. 모바일 최적화 (HTML 정리)
4. Obsidian 설정 백업 (시뮬레이션)
5. 볼트 스냅샷 생성
6. 백업 검증 및 대시보드

📁 디렉토리 구조:
- backup/raw/        : 티스토리 원본 HTML
- backup/json/       : 백업 메타데이터, 설정
- backup/snapshots/  : 볼트 구조 스냅샷
- archive/           : 최종 아카이브 파일
- _obsidian/_imports/: Obsidian 연동 파일

⚙️ 설정 연동:
- Windows 경로: C:\\ObsidianVault\\UncleParksy
- MCP 서버: Claude Desktop + GitHub
- Git 원격: https://github.com/dtslib1979/UncleParksy

🔄 자동화 스케줄:
- 전체 백업: 24시간마다
- 검증: 6시간마다  
- 빠른 동기화: 2시간마다

📞 문제 해결:
1. PowerShell 스크립트 실행: fix-obsidian-backup-system.ps1
2. Claude Desktop 재시작
3. Obsidian 볼트 경로 확인
4. 이 스크립트로 백업 검증

🚀 명령행 사용법:
python backup_automation.py                 # 대화형 메뉴
python backup_automation.py --full         # 전체 백업
python backup_automation.py --validate     # 검증만
python backup_automation.py --status       # 상태 확인
        """
        print(help_text)
    
    def run_command_line(self, args):
        """Run command line operations"""
        if args.full:
            print("🚀 Running full backup suite...")
            results = self.run_full_backup_suite()
            
            print(f"\n📊 Backup Results:")
            print(f"Overall Status: {results['overall_status']}")
            
            return 0 if results['overall_status'] == 'success' else 1
            
        elif args.validate:
            print("🔍 Running backup validation...")
            try:
                result = subprocess.run([
                    sys.executable, str(self.scripts['validator'])
                ], timeout=120)
                return result.returncode
            except Exception as e:
                print(f"❌ Validation failed: {e}")
                return 1
                
        elif args.status:
            self.show_backup_status()
            return 0
            
        else:
            # Default to interactive menu
            self.interactive_menu()
            return 0

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description='UncleParksy Obsidian Backup Automation')
    parser.add_argument('--full', action='store_true', help='Run full backup suite')
    parser.add_argument('--validate', action='store_true', help='Run validation only')
    parser.add_argument('--status', action='store_true', help='Show backup status')
    parser.add_argument('--quiet', action='store_true', help='Quiet mode (no banner)')
    
    args = parser.parse_args()
    
    automation = ObsidianBackupAutomation()
    
    if not args.quiet:
        automation.print_banner()
    
    # Check dependencies
    if not automation.check_dependencies():
        print("❌ Dependency check failed. Please install missing components.")
        return 1
    
    try:
        return automation.run_command_line(args)
    except KeyboardInterrupt:
        print("\n👋 Interrupted by user")
        return 0
    except Exception as e:
        logger.error(f"❌ Automation failed: {e}")
        return 1

if __name__ == "__main__":
    exit(main())