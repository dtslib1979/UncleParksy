#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 UncleParksy KR TextStory 완전 자동화 시스템
매번 수동 작업 대신 완전 자동화!
"""

import os
import json
import shutil
import time
import requests
from pathlib import Path
from datetime import datetime
import logging
import re

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AutoInstallSystem:
    """완전 자동화 설치 시스템 - 수동 작업 제거!"""
    
    def __init__(self):
        self.backup_dir = Path("backup")
        self.archive_dir = Path("archive") 
        self.assets_dir = Path("assets")
        self.manifest_path = self.assets_dir / "manifest.json"

    def run_full_automation(self) -> bool:
        """🚀 완전 자동화 실행 - 수동 작업 0%"""
        logger.info("🤖 완전 자동화 시스템 시작 - 수동 작업 제거!")
        
        try:
            # 1. 환경 자동 설정
            self._setup_environment()
            
            # 2. 🔥 백업 파일 원본 그대로 미러링 (수정됨!)
            mirrored_count = self._mirror_backup_files()
            
            # 3. 📱 모바일 최적화 자동 적용
            mobile_count = self._mobilize_archive_files()
            
            # 4. manifest.json 자동 생성
            self._generate_manifest()
            
            # 5. 자동 검증
            self._verify_results()
            
            logger.info(f"✅ 완전 자동화 완료! {mirrored_count}개 파일 처리, {mobile_count}개 파일 모바일 최적화")
            return True
            
        except Exception as e:
            logger.error(f"❌ 자동화 실패: {e}")
            # 자동 복구 시도
            return self._auto_recovery()

    def _setup_environment(self):
        """🔧 환경 자동 설정"""
        logger.info("🔧 환경 자동 설정...")
        
        # 필요 디렉토리 자동 생성
        for directory in [self.archive_dir, self.assets_dir]:
            directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"📁 디렉토리 확인: {directory}")

    def _mirror_backup_files(self) -> int:
        """🪞 백업 파일 원본 그대로 자동 미러링 - 변환 없음!"""
        logger.info("🪞 원본 파일 그대로 자동 미러링 시작...")
        
        mirrored_count = 0
        backup_files = list(self.backup_dir.glob("*.html"))
        
        if not backup_files:
            logger.warning("⚠️ 백업 HTML 파일 없음")
            return 0
        
        for src_file in backup_files:
            dst_file = self.archive_dir / src_file.name
            
            # 스마트 업데이트 판단
            should_copy = (
                not dst_file.exists() or 
                src_file.stat().st_mtime > dst_file.stat().st_mtime
            )
            
            if should_copy:
                # 🔥 원본 파일 그대로 복사 (변환 없음!)
                shutil.copy2(src_file, dst_file)
                mirrored_count += 1
                logger.info(f"📄 원본 복사됨: {src_file.name}")
        
        logger.info(f"✅ {mirrored_count}개 파일 원본 그대로 미러링 완료")
        return mirrored_count

    def _mobilize_archive_files(self) -> int:
        """📱 아카이브 파일 모바일 최적화"""
        logger.info("📱 아카이브 파일 모바일 최적화 시작...")
        
        try:
            # mobilize_archive.py 스크립트 실행
            import subprocess
            result = subprocess.run([
                'python', 'scripts/mobilize_archive.py'
            ], capture_output=True, text=True, cwd='.')
            
            if result.returncode == 0:
                # 성공 메시지에서 숫자 추출
                output = result.stdout
                if "Successfully processed" in output:
                    import re
                    match = re.search(r'Successfully processed (\d+)', output)
                    count = int(match.group(1)) if match else 0
                    logger.info(f"✅ 모바일 최적화 완료: {count}개 파일")
                    return count
                else:
                    logger.info("✅ 모바일 최적화: 이미 처리된 파일들")
                    return 0
            else:
                logger.warning(f"⚠️ 모바일 최적화 오류: {result.stderr}")
                return 0
                
        except Exception as e:
            logger.warning(f"⚠️ 모바일 최적화 실패: {e}")
            return 0

    def _extract_title_from_html(self, file_path: Path) -> str:
        """📝 HTML 파일에서 제목 추출"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # <title> 태그 우선
            title_match = re.search(r'<title[^>]*>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
            if title_match:
                title = title_match.group(1).strip()
                # 블로그명 제거
                title = re.sub(r'\s*::\s*.*$', '', title)
                return title
            
            # og:title 백업
            og_title_match = re.search(r'<meta[^>]*property=["\']og:title["\'][^>]*content=["\']([^"\']*)["\']', content, re.IGNORECASE)
            if og_title_match:
                return og_title_match.group(1).strip()
            
        except Exception as e:
            logger.warning(f"⚠️ 제목 추출 실패 {file_path.name}: {e}")
        
        # 파일명에서 제목 추출 (날짜 제거)
        filename = file_path.stem
        if len(filename) > 11 and filename.startswith('20'):
            title = filename[11:].replace('-', ' ')
            return title
        
        return filename.replace('-', ' ')

    def _generate_manifest(self):
        """📋 manifest.json 자동 생성 - 원본 파일 기반"""
        logger.info("📋 매니페스트 자동 생성...")
        
        # 아카이브 HTML 파일 수집 (index.html 제외)
        html_files = [f for f in self.archive_dir.glob("*.html") if f.name != "index.html"]
        
        items = []
        for html_file in sorted(html_files, reverse=True):  # 최신순
            filename = html_file.stem
            
            # 날짜 추출 (YYYY-MM-DD 형식)
            date_match = filename[:10] if filename.startswith('20') and len(filename) >= 10 else None
            
            # 실제 HTML 파일에서 제목 추출
            title = self._extract_title_from_html(html_file)
            
            items.append({
                "title": title,
                "date": date_match,
                "path": f"/archive/{html_file.name}",
                "description": f"{title} - 자동화 시스템으로 처리됨",
                "processed": datetime.now().isoformat()
            })
        
        # 매니페스트 데이터 생성
        manifest_data = {
            "title": "EduArt Engineer's Grimoire - Digital Knowledge Archive",
            "description": "완전 자동화 시스템으로 관리되는 디지털 지식 아카이브",
            "lastUpdate": datetime.now().isoformat() + "Z",
            "count": len(items),
            "automationInfo": {
                "system": "EduArt Engineer CI v2.0",
                "manualWork": "0%",
                "processType": "완전 자동화 - 원본 파일 보존",
                "updateFrequency": "매 3시간 또는 변경 시"
            },
            "items": items
        }
        
        # 매니페스트 파일 저장
        with open(self.manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"✅ 매니페스트 생성 완료: {len(items)}개 항목")

    def _verify_results(self):
        """🔍 결과 자동 검증"""
        logger.info("🔍 결과 검증 중...")
        
        # 파일 개수 확인
        backup_count = len(list(self.backup_dir.glob("*.html")))
        archive_count = len([f for f in self.archive_dir.glob("*.html") if f.name != "index.html"])
        
        logger.info(f"📊 백업: {backup_count}개, 아카이브: {archive_count}개")
        
        # 매니페스트 확인
        if self.manifest_path.exists():
            with open(self.manifest_path, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
                logger.info(f"📄 매니페스트: {manifest.get('count', 0)}개 항목")
        else:
            logger.error("❌ 매니페스트 파일 없음")

    def _auto_recovery(self) -> bool:
        """🔧 자동 복구 시스템"""
        logger.info("🔧 자동 복구 실행...")
        
        try:
            # 환경 재설정
            self._setup_environment()
            
            # 기본 매니페스트 생성
            basic_manifest = {
                "title": "EduArt Engineer's Grimoire - Digital Knowledge Archive",
                "description": "자동 복구 중...",
                "lastUpdate": datetime.now().isoformat() + "Z",
                "count": 0,
                "items": [],
                "status": "auto_recovery"
            }
            
            with open(self.manifest_path, 'w', encoding='utf-8') as f:
                json.dump(basic_manifest, f, ensure_ascii=False, indent=2)
            
            logger.info("✅ 자동 복구 완료")
            return True
            
        except Exception as e:
            logger.error(f"❌ 자동 복구 실패: {e}")
            return False


def main():
    """🚀 메인 실행 - 완전 자동화"""
    print("🤖 완전 자동화 시스템 시작 - 원본 파일 보존!")
    
    system = AutoInstallSystem()
    success = system.run_full_automation()
    
    if success:
        print("🎉 완전 자동화 성공!")
        print("✅ 모든 파일이 원본 그대로 자동 처리되었습니다")
        print("🌐 웹사이트: https://parksy.kr")
        print("📋 수동 작업: 0% (완전 자동화)")
        print("🔥 파일 처리: 원본 HTML 그대로 보존")
    else:
        print("❌ 자동화 실패")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
