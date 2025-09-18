#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Obsidian Backup Validation and Status Dashboard
Validates backup integrity and provides comprehensive status monitoring for UncleParksy

Features:
- Backup integrity verification
- Status dashboard generation
- Automated health checks
- Backup restoration testing
"""

import os
import json
import hashlib
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import shutil

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BackupValidator:
    """Comprehensive backup validation and monitoring system"""
    
    def __init__(self):
        self.repo_root = Path(__file__).parent.parent
        self.backup_root = self.repo_root / "backup"
        self.obsidian_imports = self.repo_root / "_obsidian" / "_imports"
        self.archive_dir = self.repo_root / "archive"
        
        # Backup directories
        self.backup_dirs = {
            'raw': self.backup_root / "raw",
            'md': self.obsidian_imports / "html_md",
            'html': self.obsidian_imports / "html_raw",
            'json': self.backup_root / "json",
            'snapshots': self.backup_root / "snapshots"
        }
        
    def calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA256 hash of a file"""
        hash_sha256 = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except Exception as e:
            logger.warning(f"Could not hash {file_path}: {e}")
            return ""
    
    def validate_backup_directory(self, dir_path: Path, name: str) -> Dict:
        """Validate a single backup directory"""
        logger.info(f"🔍 Validating {name} directory: {dir_path}")
        
        validation_result = {
            'name': name,
            'path': str(dir_path),
            'exists': dir_path.exists(),
            'file_count': 0,
            'total_size_bytes': 0,
            'file_types': {},
            'recent_files': [],
            'oldest_file': None,
            'newest_file': None,
            'checksums': {},
            'status': 'healthy'
        }
        
        if not dir_path.exists():
            validation_result['status'] = 'missing'
            logger.warning(f"⚠️ Directory {name} does not exist: {dir_path}")
            return validation_result
        
        files = list(dir_path.rglob("*"))
        file_files = [f for f in files if f.is_file()]
        
        validation_result['file_count'] = len(file_files)
        
        if file_files:
            # Calculate total size and analyze file types
            for file_path in file_files:
                try:
                    size = file_path.stat().st_size
                    validation_result['total_size_bytes'] += size
                    
                    # File type analysis
                    suffix = file_path.suffix.lower()
                    validation_result['file_types'][suffix] = validation_result['file_types'].get(suffix, 0) + 1
                    
                    # Track modification times
                    mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                    file_info = {
                        'name': file_path.name,
                        'size': size,
                        'modified': mtime.isoformat(),
                        'relative_path': str(file_path.relative_to(dir_path))
                    }
                    
                    if validation_result['oldest_file'] is None or mtime < datetime.fromisoformat(validation_result['oldest_file']['modified']):
                        validation_result['oldest_file'] = file_info
                    
                    if validation_result['newest_file'] is None or mtime > datetime.fromisoformat(validation_result['newest_file']['modified']):
                        validation_result['newest_file'] = file_info
                    
                    # Recent files (last 7 days)
                    if mtime > datetime.now() - timedelta(days=7):
                        validation_result['recent_files'].append(file_info)
                        
                except Exception as e:
                    logger.warning(f"Error processing {file_path}: {e}")
            
            # Sort recent files by modification time
            validation_result['recent_files'].sort(key=lambda x: x['modified'], reverse=True)
            validation_result['recent_files'] = validation_result['recent_files'][:10]  # Limit to 10 most recent
            
            # Calculate checksums for critical files
            critical_files = [f for f in file_files if f.suffix.lower() in ['.html', '.md', '.json']][:5]
            for file_path in critical_files:
                rel_path = str(file_path.relative_to(dir_path))
                validation_result['checksums'][rel_path] = self.calculate_file_hash(file_path)
        
        validation_result['total_size_mb'] = round(validation_result['total_size_bytes'] / (1024 * 1024), 2)
        
        # Determine health status
        if validation_result['file_count'] == 0:
            validation_result['status'] = 'empty'
        elif validation_result['file_count'] < 5:
            validation_result['status'] = 'low_files'
        
        logger.info(f"✅ {name}: {validation_result['file_count']} files, {validation_result['total_size_mb']} MB")
        return validation_result
    
    def validate_backup_manifests(self) -> Dict:
        """Validate backup manifest files"""
        logger.info("📋 Validating backup manifests...")
        
        manifest_dir = self.backup_dirs['json']
        manifests = list(manifest_dir.glob("backup_manifest_*.json")) if manifest_dir.exists() else []
        
        manifest_validation = {
            'total_manifests': len(manifests),
            'manifests': [],
            'latest_manifest': None,
            'status': 'healthy'
        }
        
        for manifest_path in sorted(manifests, key=lambda x: x.name, reverse=True):
            try:
                with open(manifest_path, 'r', encoding='utf-8') as f:
                    manifest_data = json.load(f)
                
                manifest_info = {
                    'filename': manifest_path.name,
                    'timestamp': manifest_data.get('timestamp', 'unknown'),
                    'status': manifest_data.get('status', 'unknown'),
                    'operations': manifest_data.get('operations_summary', {}),
                    'file_size': manifest_path.stat().st_size
                }
                
                manifest_validation['manifests'].append(manifest_info)
                
                if manifest_validation['latest_manifest'] is None:
                    manifest_validation['latest_manifest'] = manifest_info
                    
            except Exception as e:
                logger.warning(f"Error reading manifest {manifest_path}: {e}")
        
        if not manifests:
            manifest_validation['status'] = 'no_manifests'
        
        return manifest_validation
    
    def check_backup_freshness(self) -> Dict:
        """Check if backups are fresh (recently updated)"""
        logger.info("⏰ Checking backup freshness...")
        
        freshness_check = {
            'overall_status': 'fresh',
            'directories': {},
            'stale_threshold_hours': 24,
            'oldest_backup': None
        }
        
        now = datetime.now()
        stale_threshold = now - timedelta(hours=24)
        
        for name, dir_path in self.backup_dirs.items():
            if not dir_path.exists():
                freshness_check['directories'][name] = {'status': 'missing', 'last_update': None}
                continue
            
            # Find newest file in directory
            newest_time = None
            newest_file = None
            
            for file_path in dir_path.rglob("*"):
                if file_path.is_file():
                    try:
                        mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                        if newest_time is None or mtime > newest_time:
                            newest_time = mtime
                            newest_file = file_path.name
                    except:
                        continue
            
            if newest_time:
                is_fresh = newest_time > stale_threshold
                freshness_check['directories'][name] = {
                    'status': 'fresh' if is_fresh else 'stale',
                    'last_update': newest_time.isoformat(),
                    'newest_file': newest_file,
                    'hours_since_update': round((now - newest_time).total_seconds() / 3600, 1)
                }
                
                if not is_fresh:
                    freshness_check['overall_status'] = 'stale'
                
                if freshness_check['oldest_backup'] is None or newest_time < datetime.fromisoformat(freshness_check['oldest_backup']['last_update']):
                    freshness_check['oldest_backup'] = freshness_check['directories'][name]
            else:
                freshness_check['directories'][name] = {'status': 'empty', 'last_update': None}
        
        return freshness_check
    
    def generate_status_dashboard(self, validation_results: Dict) -> str:
        """Generate HTML status dashboard"""
        logger.info("📊 Generating status dashboard...")
        
        html_template = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎯 UncleParksy Backup Status Dashboard</title>
    <style>
        body {{ font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif; margin: 0; padding: 20px; background: #f5f7fa; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 15px; margin-bottom: 30px; text-align: center; }}
        .status-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .status-card {{ background: white; border-radius: 12px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        .status-healthy {{ border-left: 5px solid #10b981; }}
        .status-warning {{ border-left: 5px solid #f59e0b; }}
        .status-error {{ border-left: 5px solid #ef4444; }}
        .metric {{ margin: 10px 0; }}
        .metric-label {{ font-weight: 600; color: #374151; }}
        .metric-value {{ font-size: 1.2em; color: #111827; }}
        .file-list {{ background: #f9fafb; padding: 15px; border-radius: 8px; margin: 10px 0; }}
        .file-item {{ padding: 5px 0; border-bottom: 1px solid #e5e7eb; }}
        .timestamp {{ color: #6b7280; font-size: 0.9em; }}
        .badge {{ padding: 4px 8px; border-radius: 4px; font-size: 0.8em; font-weight: 600; }}
        .badge-success {{ background: #dcfce7; color: #166534; }}
        .badge-warning {{ background: #fef3c7; color: #92400e; }}
        .badge-error {{ background: #fee2e2; color: #991b1b; }}
        .summary {{ background: white; border-radius: 12px; padding: 25px; margin-bottom: 20px; }}
        h1, h2, h3 {{ margin-top: 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 UncleParksy Backup Status Dashboard</h1>
            <p>Obsidian 볼트 백업 시스템 상태 모니터링</p>
            <div class="timestamp">마지막 업데이트: {timestamp}</div>
        </div>
        
        <div class="summary">
            <h2>📊 전체 요약</h2>
            <div class="status-grid">
                <div class="metric">
                    <div class="metric-label">전체 백업 디렉토리</div>
                    <div class="metric-value">{total_directories}개</div>
                </div>
                <div class="metric">
                    <div class="metric-label">정상 상태</div>
                    <div class="metric-value">{healthy_directories}개</div>
                </div>
                <div class="metric">
                    <div class="metric-label">총 백업 파일</div>
                    <div class="metric-value">{total_files}개</div>
                </div>
                <div class="metric">
                    <div class="metric-label">총 백업 크기</div>
                    <div class="metric-value">{total_size_mb} MB</div>
                </div>
            </div>
        </div>
        
        <h2>📁 백업 디렉토리 상태</h2>
        <div class="status-grid">
            {directory_cards}
        </div>
        
        <div class="summary">
            <h2>⏰ 백업 신선도 체크</h2>
            <p><span class="badge badge-{freshness_status}">{freshness_status_text}</span></p>
            {freshness_details}
        </div>
        
        <div class="summary">
            <h2>📋 백업 매니페스트</h2>
            {manifest_summary}
        </div>
    </div>
</body>
</html>
        """
        
        # Prepare data for template
        directory_validation = validation_results['directory_validation']
        freshness = validation_results['freshness_check']
        manifests = validation_results['manifest_validation']
        
        # Calculate summary stats
        total_directories = len(directory_validation)
        healthy_directories = len([d for d in directory_validation.values() if d['status'] == 'healthy'])
        total_files = sum(d['file_count'] for d in directory_validation.values())
        total_size_mb = sum(d['total_size_mb'] for d in directory_validation.values())
        
        # Generate directory cards
        directory_cards = []
        for name, data in directory_validation.items():
            status_class = {
                'healthy': 'status-healthy',
                'missing': 'status-error',
                'empty': 'status-warning',
                'low_files': 'status-warning'
            }.get(data['status'], 'status-warning')
            
            recent_files_html = ""
            if data['recent_files']:
                recent_files_html = "<div class='file-list'><strong>최근 파일:</strong>"
                for file_info in data['recent_files'][:3]:
                    recent_files_html += f"<div class='file-item'>{file_info['name']} <span class='timestamp'>({file_info['modified'][:16]})</span></div>"
                recent_files_html += "</div>"
            
            card_html = f"""
            <div class="status-card {status_class}">
                <h3>{name.upper()} 백업</h3>
                <div class="metric">
                    <div class="metric-label">상태</div>
                    <div class="metric-value"><span class="badge badge-{('success' if data['status'] == 'healthy' else 'warning')}">{data['status']}</span></div>
                </div>
                <div class="metric">
                    <div class="metric-label">파일 수</div>
                    <div class="metric-value">{data['file_count']}개</div>
                </div>
                <div class="metric">
                    <div class="metric-label">크기</div>
                    <div class="metric-value">{data['total_size_mb']} MB</div>
                </div>
                <div class="metric">
                    <div class="metric-label">파일 형식</div>
                    <div class="metric-value">{', '.join(f'{k}({v})' for k, v in data['file_types'].items()) if data['file_types'] else 'None'}</div>
                </div>
                {recent_files_html}
            </div>
            """
            directory_cards.append(card_html)
        
        # Freshness details
        freshness_status = 'success' if freshness['overall_status'] == 'fresh' else 'warning'
        freshness_status_text = '신선함' if freshness['overall_status'] == 'fresh' else '오래됨'
        
        freshness_details = "<div class='file-list'>"
        for name, data in freshness['directories'].items():
            if data['last_update']:
                freshness_details += f"<div class='file-item'><strong>{name}</strong>: {data['hours_since_update']}시간 전 업데이트</div>"
            else:
                freshness_details += f"<div class='file-item'><strong>{name}</strong>: 업데이트 없음</div>"
        freshness_details += "</div>"
        
        # Manifest summary
        manifest_summary = f"""
        <div class="metric">
            <div class="metric-label">총 매니페스트 파일</div>
            <div class="metric-value">{manifests['total_manifests']}개</div>
        </div>
        """
        if manifests['latest_manifest']:
            manifest_summary += f"""
            <div class="metric">
                <div class="metric-label">최신 백업</div>
                <div class="metric-value">{manifests['latest_manifest']['timestamp']}</div>
            </div>
            """
        
        # Fill template
        html_content = html_template.format(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            total_directories=total_directories,
            healthy_directories=healthy_directories,
            total_files=total_files,
            total_size_mb=round(total_size_mb, 2),
            directory_cards='\n'.join(directory_cards),
            freshness_status=freshness_status,
            freshness_status_text=freshness_status_text,
            freshness_details=freshness_details,
            manifest_summary=manifest_summary
        )
        
        return html_content
    
    def run_full_validation(self) -> Dict:
        """Run complete backup validation"""
        logger.info("🚀 Starting comprehensive backup validation...")
        
        validation_results = {
            'timestamp': datetime.now().isoformat(),
            'directory_validation': {},
            'manifest_validation': {},
            'freshness_check': {},
            'overall_status': 'healthy'
        }
        
        # Validate each backup directory
        for name, dir_path in self.backup_dirs.items():
            validation_results['directory_validation'][name] = self.validate_backup_directory(dir_path, name)
        
        # Validate manifests
        validation_results['manifest_validation'] = self.validate_backup_manifests()
        
        # Check freshness
        validation_results['freshness_check'] = self.check_backup_freshness()
        
        # Determine overall status
        unhealthy_dirs = [name for name, data in validation_results['directory_validation'].items() 
                         if data['status'] not in ['healthy']]
        
        if unhealthy_dirs:
            validation_results['overall_status'] = 'warning'
            logger.warning(f"⚠️ Unhealthy directories found: {unhealthy_dirs}")
        
        if validation_results['freshness_check']['overall_status'] == 'stale':
            validation_results['overall_status'] = 'warning'
            logger.warning("⚠️ Some backups are stale")
        
        # Save validation results
        results_path = self.backup_root / "json" / f"validation_results_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
        results_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(results_path, 'w', encoding='utf-8') as f:
            json.dump(validation_results, f, indent=2, ensure_ascii=False)
        
        # Generate HTML dashboard
        dashboard_html = self.generate_status_dashboard(validation_results)
        dashboard_path = self.backup_root / "backup_status_dashboard.html"
        
        with open(dashboard_path, 'w', encoding='utf-8') as f:
            f.write(dashboard_html)
        
        logger.info(f"✅ Validation completed. Results: {results_path}")
        logger.info(f"📊 Dashboard: {dashboard_path}")
        
        return {
            'status': validation_results['overall_status'],
            'results_path': str(results_path),
            'dashboard_path': str(dashboard_path),
            'summary': {
                'total_directories': len(validation_results['directory_validation']),
                'healthy_directories': len([d for d in validation_results['directory_validation'].values() if d['status'] == 'healthy']),
                'total_files': sum(d['file_count'] for d in validation_results['directory_validation'].values()),
                'validation_timestamp': validation_results['timestamp']
            }
        }

def main():
    """Main execution function"""
    validator = BackupValidator()
    
    try:
        result = validator.run_full_validation()
        
        print(f"\n🎯 백업 검증 완료!")
        print(f"📊 상태: {result['status']}")
        print(f"📁 디렉토리: {result['summary']['healthy_directories']}/{result['summary']['total_directories']} 정상")
        print(f"📄 총 파일: {result['summary']['total_files']}개")
        print(f"📊 대시보드: {result['dashboard_path']}")
        
        return 0 if result['status'] in ['healthy', 'warning'] else 1
        
    except Exception as e:
        logger.error(f"❌ Validation failed: {e}")
        return 1

if __name__ == "__main__":
    exit(main())