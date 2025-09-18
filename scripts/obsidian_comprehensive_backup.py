#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 UncleParksy 옵시디언 종합 백업 시스템
현재 설정에 따라 모든 콘텐츠를 Obsidian으로 완전 백업

작가지망생 박씨의 마감작업을 위한 통합 백업 솔루션
"""

import os
import json
import shutil
import subprocess
import time
from pathlib import Path
from datetime import datetime
import logging
import sys

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('_obsidian/_imports/backup.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

class ObsidianComprehensiveBackup:
    """🎯 옵시디언 종합 백업 시스템"""
    
    def __init__(self):
        self.root_dir = Path(".")
        self.obsidian_imports = Path("_obsidian/_imports")
        self.backup_dir = Path("backup")
        self.archive_dir = Path("archive") 
        self.category_dir = Path("category")
        self.assets_dir = Path("assets")
        
        # Obsidian 백업 구조
        self.obsidian_raw = self.obsidian_imports / "html_raw"
        self.obsidian_md = self.obsidian_imports / "html_md"
        self.obsidian_assets = self.obsidian_imports / "assets"
        self.obsidian_category = self.obsidian_imports / "category"
        self.obsidian_backup = self.obsidian_imports / "backup"
        self.obsidian_archive = self.obsidian_imports / "archive"
        
        self.setup_obsidian_structure()

    def setup_obsidian_structure(self):
        """🏗️ Obsidian 백업 디렉토리 구조 설정"""
        logger.info("🏗️ Obsidian 백업 디렉토리 구조 설정...")
        
        directories = [
            self.obsidian_imports,
            self.obsidian_raw,
            self.obsidian_md,
            self.obsidian_assets,
            self.obsidian_category,
            self.obsidian_backup,
            self.obsidian_archive
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"📁 디렉토리 준비: {directory}")

    def run_comprehensive_backup(self) -> bool:
        """🚀 종합 백업 실행 - 현재 설정에 따라 모든 콘텐츠 백업"""
        logger.info("🎯 ===== 옵시디언 종합 백업 시작 =====")
        logger.info("📝 현재 설정에 따라 모든 콘텐츠를 Obsidian으로 백업합니다")
        
        start_time = datetime.now()
        backup_summary = {
            "timestamp": start_time.isoformat(),
            "components": {},
            "total_files": 0,
            "errors": []
        }
        
        try:
            # 1단계: Tistory 최신 백업 실행
            logger.info("\n🔥 1단계: Tistory RSS 백업 실행")
            tistory_result = self._run_tistory_backup()
            backup_summary["components"]["tistory"] = tistory_result
            
            # 2단계: 백업 파일을 Obsidian으로 미러링
            logger.info("\n📄 2단계: 백업 파일 Obsidian 미러링")
            backup_mirror_result = self._mirror_backup_to_obsidian()
            backup_summary["components"]["backup_mirror"] = backup_mirror_result
            
            # 3단계: 아카이브 파일을 Obsidian으로 미러링
            logger.info("\n📚 3단계: 아카이브 파일 Obsidian 미러링")
            archive_mirror_result = self._mirror_archive_to_obsidian()
            backup_summary["components"]["archive_mirror"] = archive_mirror_result
            
            # 4단계: 카테고리 파일을 Obsidian으로 동기화 (RAW + Markdown)
            logger.info("\n🗂️ 4단계: 카테고리 파일 Obsidian 동기화")
            category_sync_result = self._sync_category_to_obsidian()
            backup_summary["components"]["category_sync"] = category_sync_result
            
            # 5단계: Assets 백업
            logger.info("\n🎨 5단계: Assets 백업")
            assets_result = self._backup_assets_to_obsidian()
            backup_summary["components"]["assets"] = assets_result
            
            # 6단계: 메타데이터 및 설정 백업
            logger.info("\n⚙️ 6단계: 메타데이터 및 설정 백업")
            metadata_result = self._backup_metadata_to_obsidian()
            backup_summary["components"]["metadata"] = metadata_result
            
            # 7단계: 백업 요약 및 인덱스 생성
            logger.info("\n📋 7단계: 백업 요약 및 인덱스 생성")
            self._generate_backup_index(backup_summary)
            
            # 계산 총계
            total_files = sum(
                result.get("files_processed", 0) 
                for result in backup_summary["components"].values()
            )
            backup_summary["total_files"] = total_files
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            logger.info(f"\n✅ ===== 옵시디언 종합 백업 완료 =====")
            logger.info(f"🕐 소요시간: {duration:.2f}초")
            logger.info(f"📊 총 처리 파일: {total_files}개")
            logger.info(f"📁 백업 위치: {self.obsidian_imports}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ 종합 백업 실패: {e}")
            backup_summary["errors"].append(str(e))
            return False
    
    def _run_tistory_backup(self) -> dict:
        """🔥 Tistory RSS 백업 실행"""
        logger.info("🔥 Tistory RSS 백업 시작...")
        
        try:
            result = subprocess.run([
                sys.executable, 'scripts/tistory_backup.py'
            ], capture_output=True, text=True, cwd=self.root_dir)
            
            if result.returncode == 0:
                # 새 파일 개수 파싱
                output = result.stdout
                if "새 파일:" in output:
                    import re
                    match = re.search(r'새 파일: (\d+)개', output)
                    new_files = int(match.group(1)) if match else 0
                else:
                    new_files = 0
                
                logger.info(f"✅ Tistory 백업 완료: {new_files}개 새 파일")
                return {
                    "status": "success",
                    "files_processed": new_files,
                    "message": f"Tistory RSS 백업 완료: {new_files}개 새 파일"
                }
            else:
                logger.error(f"❌ Tistory 백업 실패: {result.stderr}")
                return {
                    "status": "error",
                    "files_processed": 0,
                    "message": f"Tistory 백업 실패: {result.stderr}"
                }
                
        except Exception as e:
            logger.error(f"❌ Tistory 백업 오류: {e}")
            return {
                "status": "error",
                "files_processed": 0,
                "message": f"Tistory 백업 오류: {e}"
            }
    
    def _mirror_backup_to_obsidian(self) -> dict:
        """📄 백업 파일을 Obsidian으로 미러링"""
        logger.info("📄 백업 파일 Obsidian 미러링 시작...")
        
        mirrored_count = 0
        
        try:
            # backup/raw 폴더의 HTML 파일들을 _obsidian/_imports/backup으로 복사
            backup_raw_dir = self.backup_dir / "raw"
            if backup_raw_dir.exists():
                for html_file in backup_raw_dir.glob("*.html"):
                    dst_file = self.obsidian_backup / html_file.name
                    
                    # 새 파일이거나 수정된 파일만 복사
                    if (not dst_file.exists() or 
                        html_file.stat().st_mtime > dst_file.stat().st_mtime):
                        
                        shutil.copy2(html_file, dst_file)
                        mirrored_count += 1
                        logger.info(f"📄 백업 복사: {html_file.name}")
            
            # backup 폴더의 직접 HTML 파일들도 복사
            for html_file in self.backup_dir.glob("*.html"):
                dst_file = self.obsidian_backup / html_file.name
                
                if (not dst_file.exists() or 
                    html_file.stat().st_mtime > dst_file.stat().st_mtime):
                    
                    shutil.copy2(html_file, dst_file)
                    mirrored_count += 1
                    logger.info(f"📄 백업 복사: {html_file.name}")
            
            logger.info(f"✅ 백업 파일 미러링 완료: {mirrored_count}개 파일")
            return {
                "status": "success",
                "files_processed": mirrored_count,
                "message": f"백업 파일 미러링 완료: {mirrored_count}개 파일"
            }
            
        except Exception as e:
            logger.error(f"❌ 백업 파일 미러링 실패: {e}")
            return {
                "status": "error",
                "files_processed": 0,
                "message": f"백업 파일 미러링 실패: {e}"
            }
    
    def _mirror_archive_to_obsidian(self) -> dict:
        """📚 아카이브 파일을 Obsidian으로 미러링"""
        logger.info("📚 아카이브 파일 Obsidian 미러링 시작...")
        
        mirrored_count = 0
        
        try:
            # archive 폴더의 HTML 파일들을 _obsidian/_imports/archive로 복사
            for html_file in self.archive_dir.glob("*.html"):
                if html_file.name == "index.html":
                    continue  # index.html 제외
                
                dst_file = self.obsidian_archive / html_file.name
                
                # 새 파일이거나 수정된 파일만 복사
                if (not dst_file.exists() or 
                    html_file.stat().st_mtime > dst_file.stat().st_mtime):
                    
                    shutil.copy2(html_file, dst_file)
                    mirrored_count += 1
                    logger.info(f"📚 아카이브 복사: {html_file.name}")
            
            logger.info(f"✅ 아카이브 파일 미러링 완료: {mirrored_count}개 파일")
            return {
                "status": "success",
                "files_processed": mirrored_count,
                "message": f"아카이브 파일 미러링 완료: {mirrored_count}개 파일"
            }
            
        except Exception as e:
            logger.error(f"❌ 아카이브 파일 미러링 실패: {e}")
            return {
                "status": "error",
                "files_processed": 0,
                "message": f"아카이브 파일 미러링 실패: {e}"
            }
    
    def _sync_category_to_obsidian(self) -> dict:
        """🗂️ 카테고리 파일을 Obsidian으로 동기화 (기존 워크플로우 재사용)"""
        logger.info("🗂️ 카테고리 파일 Obsidian 동기화 시작...")
        
        try:
            # 현재 설정에 따른 카테고리 동기화 (기존 워크플로우 로직 사용)
            synced_files = 0
            converted_files = 0
            
            # RAW HTML 동기화
            if self.category_dir.exists():
                categories = [
                    "blog-transformation",
                    "device-chronicles", 
                    "system-configuration",
                    "thought-archaeology",
                    "webappsbook-codex",
                    "webappsbookcast",
                    "writers-path"
                ]
                
                for category in categories:
                    category_path = self.category_dir / category
                    if category_path.exists():
                        dst_category_path = self.obsidian_raw / category
                        dst_category_path.mkdir(parents=True, exist_ok=True)
                        
                        # HTML 파일 복사
                        for html_file in category_path.glob("*.html"):
                            dst_file = dst_category_path / html_file.name
                            
                            if (not dst_file.exists() or 
                                html_file.stat().st_mtime > dst_file.stat().st_mtime):
                                
                                shutil.copy2(html_file, dst_file)
                                synced_files += 1
                                logger.info(f"🗂️ 카테고리 동기화: {category}/{html_file.name}")
                
                # HTML → Markdown 변환
                logger.info("🔄 HTML → Markdown 변환 시작...")
                
                for category in categories:
                    category_path = self.category_dir / category
                    if category_path.exists():
                        dst_md_category = self.obsidian_md / category
                        dst_md_category.mkdir(parents=True, exist_ok=True)
                        
                        for html_file in category_path.glob("*.html"):
                            md_file = dst_md_category / f"{html_file.stem}.md"
                            
                            # Pandoc으로 변환 (가능한 경우)
                            try:
                                result = subprocess.run([
                                    'pandoc', str(html_file), 
                                    '-f', 'html', '-t', 'gfm', 
                                    '-o', str(md_file)
                                ], capture_output=True, text=True, timeout=30)
                                
                                if result.returncode == 0:
                                    converted_files += 1
                                    logger.info(f"📝 Markdown 변환: {category}/{html_file.stem}.md")
                                else:
                                    logger.warning(f"⚠️ Markdown 변환 실패: {html_file.name}")
                                    
                            except (subprocess.TimeoutExpired, FileNotFoundError):
                                # Pandoc이 없거나 시간 초과시 기본 변환
                                self._basic_html_to_markdown(html_file, md_file)
                                converted_files += 1
                                logger.info(f"📝 기본 Markdown 변환: {category}/{html_file.stem}.md")
            
            total_processed = synced_files + converted_files
            logger.info(f"✅ 카테고리 동기화 완료: RAW {synced_files}개, MD {converted_files}개")
            return {
                "status": "success",
                "files_processed": total_processed,
                "message": f"카테고리 동기화 완료: RAW {synced_files}개, MD {converted_files}개"
            }
            
        except Exception as e:
            logger.error(f"❌ 카테고리 동기화 실패: {e}")
            return {
                "status": "error",
                "files_processed": 0,
                "message": f"카테고리 동기화 실패: {e}"
            }
    
    def _basic_html_to_markdown(self, html_file: Path, md_file: Path):
        """📝 기본적인 HTML → Markdown 변환 (Pandoc 없을 때)"""
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # 간단한 HTML → Markdown 변환
            import re
            
            # HTML 태그 제거 및 기본 변환
            content = html_content
            content = re.sub(r'<title[^>]*>(.*?)</title>', r'# \1', content, flags=re.IGNORECASE | re.DOTALL)
            content = re.sub(r'<h1[^>]*>(.*?)</h1>', r'# \1', content, flags=re.IGNORECASE | re.DOTALL)
            content = re.sub(r'<h2[^>]*>(.*?)</h2>', r'## \1', content, flags=re.IGNORECASE | re.DOTALL)
            content = re.sub(r'<h3[^>]*>(.*?)</h3>', r'### \1', content, flags=re.IGNORECASE | re.DOTALL)
            content = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', content, flags=re.IGNORECASE | re.DOTALL)
            content = re.sub(r'<br[^>]*/?>', '\n', content, flags=re.IGNORECASE)
            content = re.sub(r'<[^>]+>', '', content)  # 나머지 태그 제거
            content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)  # 빈 줄 정리
            
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(content.strip())
                
        except Exception as e:
            logger.warning(f"⚠️ 기본 HTML→MD 변환 실패 {html_file.name}: {e}")
    
    def _backup_assets_to_obsidian(self) -> dict:
        """🎨 Assets 백업"""
        logger.info("🎨 Assets 백업 시작...")
        
        copied_count = 0
        
        try:
            if self.assets_dir.exists():
                # assets 폴더 전체를 Obsidian으로 복사
                for item in self.assets_dir.rglob("*"):
                    if item.is_file():
                        relative_path = item.relative_to(self.assets_dir)
                        dst_file = self.obsidian_assets / relative_path
                        dst_file.parent.mkdir(parents=True, exist_ok=True)
                        
                        if (not dst_file.exists() or 
                            item.stat().st_mtime > dst_file.stat().st_mtime):
                            
                            shutil.copy2(item, dst_file)
                            copied_count += 1
                            logger.info(f"🎨 Asset 복사: {relative_path}")
            
            logger.info(f"✅ Assets 백업 완료: {copied_count}개 파일")
            return {
                "status": "success",
                "files_processed": copied_count,
                "message": f"Assets 백업 완료: {copied_count}개 파일"
            }
            
        except Exception as e:
            logger.error(f"❌ Assets 백업 실패: {e}")
            return {
                "status": "error",
                "files_processed": 0,
                "message": f"Assets 백업 실패: {e}"
            }
    
    def _backup_metadata_to_obsidian(self) -> dict:
        """⚙️ 메타데이터 및 설정 백업"""
        logger.info("⚙️ 메타데이터 및 설정 백업 시작...")
        
        copied_count = 0
        
        try:
            # 주요 설정 파일들 백업
            config_files = [
                "README.md",
                "manifest.webmanifest",
                "requirements.txt",
                "feed.xml",
                "sitemap.xml",
                "CNAME",
                ".nojekyll"
            ]
            
            config_backup_dir = self.obsidian_imports / "config"
            config_backup_dir.mkdir(exist_ok=True)
            
            for config_file in config_files:
                src_file = self.root_dir / config_file
                if src_file.exists():
                    dst_file = config_backup_dir / config_file
                    shutil.copy2(src_file, dst_file)
                    copied_count += 1
                    logger.info(f"⚙️ 설정 백업: {config_file}")
            
            # GitHub 워크플로우 백업
            github_dir = self.root_dir / ".github"
            if github_dir.exists():
                dst_github_dir = config_backup_dir / ".github"
                if dst_github_dir.exists():
                    shutil.rmtree(dst_github_dir)
                shutil.copytree(github_dir, dst_github_dir)
                copied_count += len(list(github_dir.rglob("*")))
                logger.info("⚙️ GitHub 워크플로우 백업 완료")
            
            logger.info(f"✅ 메타데이터 백업 완료: {copied_count}개 파일")
            return {
                "status": "success",
                "files_processed": copied_count,
                "message": f"메타데이터 백업 완료: {copied_count}개 파일"
            }
            
        except Exception as e:
            logger.error(f"❌ 메타데이터 백업 실패: {e}")
            return {
                "status": "error",
                "files_processed": 0,
                "message": f"메타데이터 백업 실패: {e}"
            }
    
    def _generate_backup_index(self, backup_summary: dict):
        """📋 백업 인덱스 및 요약 생성"""
        logger.info("📋 백업 인덱스 생성 중...")
        
        try:
            # 백업 요약 JSON 저장
            summary_file = self.obsidian_imports / "backup_summary.json"
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(backup_summary, f, ensure_ascii=False, indent=2)
            
            # 백업 인덱스 마크다운 생성
            index_file = self.obsidian_imports / "BACKUP_INDEX.md"
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            index_content = f"""# 🎯 UncleParksy 옵시디언 종합 백업 인덱스
            
**백업 완료 시간**: {timestamp}
**총 처리 파일**: {backup_summary['total_files']}개

## 📊 백업 구성 요소

"""
            
            for component, result in backup_summary["components"].items():
                status_emoji = "✅" if result["status"] == "success" else "❌"
                index_content += f"### {status_emoji} {component.replace('_', ' ').title()}\n"
                index_content += f"- **상태**: {result['status']}\n"
                index_content += f"- **처리 파일**: {result['files_processed']}개\n"
                index_content += f"- **메시지**: {result['message']}\n\n"
            
            index_content += f"""
## 📁 백업 디렉토리 구조

```
_obsidian/_imports/
├── 📄 backup/          # Tistory RSS 백업 파일
├── 📚 archive/         # 아카이브 HTML 파일
├── 🗂️ html_raw/        # 카테고리 원본 HTML
├── 📝 html_md/         # 카테고리 Markdown 변환
├── 🎨 assets/          # 리소스 파일
├── ⚙️ config/          # 설정 및 메타데이터
├── 📋 backup_summary.json   # 백업 요약 데이터
└── 📝 backup.log       # 백업 로그
```

## 🚀 사용법

1. **Obsidian에서 볼트 열기**: `_obsidian/_imports` 폴더를 Obsidian 볼트로 설정
2. **콘텐츠 탐색**: 각 하위 폴더에서 백업된 콘텐츠 확인
3. **검색 활용**: Obsidian의 강력한 검색 기능으로 콘텐츠 탐색

## 📱 연동 정보

- **GitHub Repository**: https://github.com/dtslib1979/UncleParksy
- **웹사이트**: https://parksy.kr
- **작가지망생 박씨의 마감작업 시스템**

---
*🤖 자동 생성된 백업 인덱스 - {timestamp}*
"""
            
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(index_content)
            
            logger.info("✅ 백업 인덱스 생성 완료")
            
        except Exception as e:
            logger.error(f"❌ 백업 인덱스 생성 실패: {e}")


def main():
    """🚀 메인 실행 함수"""
    print("🎯 ===== UncleParksy 옵시디언 종합 백업 시스템 =====")
    print("📝 현재 설정에 따라 모든 콘텐츠를 Obsidian으로 백업합니다")
    print("🚀 작가지망생 박씨의 마감작업을 위한 통합 백업 솔루션\n")
    
    backup_system = ObsidianComprehensiveBackup()
    success = backup_system.run_comprehensive_backup()
    
    if success:
        print("\n🎉 ===== 종합 백업 완료! =====")
        print("✅ 모든 콘텐츠가 Obsidian 형식으로 백업되었습니다")
        print("📁 백업 위치: _obsidian/_imports/")
        print("📋 백업 상세: _obsidian/_imports/BACKUP_INDEX.md")
        print("🚀 Obsidian에서 _obsidian/_imports 폴더를 볼트로 열어보세요!")
        return 0
    else:
        print("\n❌ 백업 실패")
        print("📝 로그 확인: _obsidian/_imports/backup.log")
        return 1


if __name__ == "__main__":
    exit(main())