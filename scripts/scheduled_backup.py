#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scheduled Backup System for UncleParksy Obsidian
Automated backup scheduling with email notifications and health monitoring

Usage:
  python scheduled_backup.py --mode=full     # Full backup
  python scheduled_backup.py --mode=validate # Validation only
  python scheduled_backup.py --mode=quick    # Quick tistory sync only
"""

import os
import argparse
import logging
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
import json
import subprocess
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/runner/work/UncleParksy/UncleParksy/backup/scheduled_backup.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ScheduledBackupManager:
    """Automated backup scheduling and monitoring"""
    
    def __init__(self):
        self.repo_root = Path(__file__).parent.parent
        self.backup_root = self.repo_root / "backup"
        self.scripts_dir = self.repo_root / "scripts"
        
        # Backup configuration
        self.config = {
            'full_backup_interval_hours': 24,
            'validation_interval_hours': 6,
            'quick_sync_interval_hours': 2,
            'max_backup_age_days': 30,
            'notification_email': None,  # Set if email notifications needed
            'retention_days': 30
        }
        
    def load_last_run_info(self, backup_type: str) -> datetime:
        """Load timestamp of last backup run"""
        info_file = self.backup_root / f"last_{backup_type}_run.json"
        
        if info_file.exists():
            try:
                with open(info_file, 'r') as f:
                    data = json.load(f)
                return datetime.fromisoformat(data['last_run'])
            except Exception as e:
                logger.warning(f"Could not load last run info: {e}")
        
        return datetime.min
    
    def save_last_run_info(self, backup_type: str, result: dict):
        """Save backup run information"""
        info_file = self.backup_root / f"last_{backup_type}_run.json"
        info_file.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            'last_run': datetime.now().isoformat(),
            'status': result.get('status', 'unknown'),
            'result': result
        }
        
        with open(info_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def should_run_backup(self, backup_type: str) -> bool:
        """Check if backup should run based on schedule"""
        last_run = self.load_last_run_info(backup_type)
        
        interval_hours = {
            'full': self.config['full_backup_interval_hours'],
            'validate': self.config['validation_interval_hours'],
            'quick': self.config['quick_sync_interval_hours']
        }.get(backup_type, 24)
        
        next_run_time = last_run + timedelta(hours=interval_hours)
        should_run = datetime.now() >= next_run_time
        
        logger.info(f"Backup type '{backup_type}': last run {last_run}, next due {next_run_time}, should run: {should_run}")
        return should_run
    
    def run_full_backup(self) -> dict:
        """Execute full backup using obsidian_full_backup.py"""
        logger.info("🚀 Starting scheduled full backup...")
        
        try:
            # Run the full backup script
            result = subprocess.run([
                sys.executable, 
                str(self.scripts_dir / "obsidian_full_backup.py")
            ], capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                logger.info("✅ Full backup completed successfully")
                return {
                    'status': 'success',
                    'stdout': result.stdout,
                    'stderr': result.stderr,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                logger.error(f"❌ Full backup failed with code {result.returncode}")
                return {
                    'status': 'error',
                    'error': f"Exit code {result.returncode}",
                    'stdout': result.stdout,
                    'stderr': result.stderr,
                    'timestamp': datetime.now().isoformat()
                }
                
        except subprocess.TimeoutExpired:
            logger.error("❌ Full backup timed out")
            return {
                'status': 'timeout',
                'error': 'Backup process timed out after 5 minutes',
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"❌ Full backup failed: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def run_validation(self) -> dict:
        """Execute backup validation using backup_validator.py"""
        logger.info("🔍 Starting scheduled validation...")
        
        try:
            result = subprocess.run([
                sys.executable,
                str(self.scripts_dir / "backup_validator.py")
            ], capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                logger.info("✅ Validation completed successfully")
                return {
                    'status': 'success',
                    'stdout': result.stdout,
                    'stderr': result.stderr,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                logger.warning(f"⚠️ Validation completed with warnings (code {result.returncode})")
                return {
                    'status': 'warning',
                    'stdout': result.stdout,
                    'stderr': result.stderr,
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"❌ Validation failed: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def run_quick_sync(self) -> dict:
        """Execute quick Tistory sync only"""
        logger.info("⚡ Starting quick sync...")
        
        try:
            # Import and run tistory backup
            sys.path.append(str(self.scripts_dir))
            from tistory_backup import main as tistory_main
            
            # Capture current status
            tistory_main()
            
            logger.info("✅ Quick sync completed")
            return {
                'status': 'success',
                'message': 'Tistory sync completed',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Quick sync failed: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def cleanup_old_backups(self):
        """Clean up old backup files"""
        logger.info("🧹 Cleaning up old backup files...")
        
        cutoff_date = datetime.now() - timedelta(days=self.config['retention_days'])
        cleaned_count = 0
        
        # Clean up old manifests
        manifest_dir = self.backup_root / "json"
        if manifest_dir.exists():
            for manifest_file in manifest_dir.glob("backup_manifest_*.json"):
                try:
                    file_date = datetime.fromtimestamp(manifest_file.stat().st_mtime)
                    if file_date < cutoff_date:
                        manifest_file.unlink()
                        cleaned_count += 1
                        logger.info(f"🗑️ Deleted old manifest: {manifest_file.name}")
                except Exception as e:
                    logger.warning(f"Could not delete {manifest_file}: {e}")
        
        # Clean up old snapshots
        snapshots_dir = self.backup_root / "snapshots"
        if snapshots_dir.exists():
            for snapshot_dir in snapshots_dir.iterdir():
                if snapshot_dir.is_dir():
                    try:
                        dir_date = datetime.fromtimestamp(snapshot_dir.stat().st_mtime)
                        if dir_date < cutoff_date:
                            import shutil
                            shutil.rmtree(snapshot_dir)
                            cleaned_count += 1
                            logger.info(f"🗑️ Deleted old snapshot: {snapshot_dir.name}")
                    except Exception as e:
                        logger.warning(f"Could not delete {snapshot_dir}: {e}")
        
        logger.info(f"🧹 Cleanup completed: {cleaned_count} items removed")
    
    def send_notification(self, subject: str, content: str, status: str = 'info'):
        """Send email notification (if configured)"""
        if not self.config.get('notification_email'):
            return
        
        # Email notification implementation would go here
        # For now, just log the notification
        logger.info(f"📧 Notification: {subject}")
        logger.info(f"Content: {content}")
    
    def generate_status_summary(self) -> str:
        """Generate a status summary for notifications"""
        summary_lines = [
            "🎯 UncleParksy Backup Status Summary",
            f"⏰ Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "📊 Recent Backup Operations:"
        ]
        
        # Check recent backup operations
        for backup_type in ['full', 'validate', 'quick']:
            last_run = self.load_last_run_info(backup_type)
            if last_run != datetime.min:
                hours_ago = (datetime.now() - last_run).total_seconds() / 3600
                summary_lines.append(f"  • {backup_type.title()}: {hours_ago:.1f}h ago")
            else:
                summary_lines.append(f"  • {backup_type.title()}: Never run")
        
        summary_lines.extend([
            "",
            "🔗 Dashboard: backup/backup_status_dashboard.html",
            "📋 Logs: backup/scheduled_backup.log"
        ])
        
        return "\n".join(summary_lines)
    
    def run_scheduled_tasks(self, force_mode: str = None):
        """Run scheduled tasks based on configuration"""
        logger.info("⏰ Starting scheduled backup tasks...")
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'tasks_executed': [],
            'overall_status': 'success'
        }
        
        # Determine which tasks to run
        tasks_to_run = []
        
        if force_mode:
            tasks_to_run.append(force_mode)
        else:
            if self.should_run_backup('full'):
                tasks_to_run.append('full')
            elif self.should_run_backup('validate'):
                tasks_to_run.append('validate')
            elif self.should_run_backup('quick'):
                tasks_to_run.append('quick')
        
        # Execute tasks
        for task in tasks_to_run:
            logger.info(f"🎯 Executing task: {task}")
            
            if task == 'full':
                result = self.run_full_backup()
                self.save_last_run_info('full', result)
                
                # Also update validation time since full backup includes validation
                self.save_last_run_info('validate', result)
                
            elif task == 'validate':
                result = self.run_validation()
                self.save_last_run_info('validate', result)
                
            elif task == 'quick':
                result = self.run_quick_sync()
                self.save_last_run_info('quick', result)
            
            results['tasks_executed'].append({
                'task': task,
                'result': result
            })
            
            if result['status'] not in ['success', 'warning']:
                results['overall_status'] = 'error'
                self.send_notification(
                    f"❌ Backup Task Failed: {task}",
                    f"Task '{task}' failed: {result.get('error', 'Unknown error')}",
                    'error'
                )
        
        # Run cleanup
        self.cleanup_old_backups()
        
        # Send summary notification if tasks were executed
        if tasks_to_run:
            summary = self.generate_status_summary()
            status_icon = "✅" if results['overall_status'] == 'success' else "⚠️" if results['overall_status'] == 'warning' else "❌"
            self.send_notification(
                f"{status_icon} Backup Tasks Completed",
                summary,
                results['overall_status']
            )
        
        # Save results
        results_file = self.backup_root / f"scheduled_results_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"⏰ Scheduled tasks completed. Status: {results['overall_status']}")
        return results

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description='Scheduled backup system for UncleParksy')
    parser.add_argument('--mode', choices=['full', 'validate', 'quick', 'auto'], 
                       default='auto', help='Backup mode to run')
    parser.add_argument('--force', action='store_true', 
                       help='Force run regardless of schedule')
    
    args = parser.parse_args()
    
    manager = ScheduledBackupManager()
    
    try:
        if args.mode == 'auto':
            # Run based on schedule
            results = manager.run_scheduled_tasks()
        else:
            # Force specific mode
            force_mode = args.mode if args.force else None
            if force_mode or manager.should_run_backup(args.mode):
                results = manager.run_scheduled_tasks(force_mode=args.mode)
            else:
                print(f"⏭️ Skipping {args.mode} - not due to run yet")
                return 0
        
        # Print summary
        print(f"\n⏰ Scheduled backup completed!")
        print(f"📊 Status: {results['overall_status']}")
        print(f"🎯 Tasks executed: {len(results['tasks_executed'])}")
        
        for task_result in results['tasks_executed']:
            task_name = task_result['task']
            task_status = task_result['result']['status']
            status_icon = "✅" if task_status == 'success' else "⚠️" if task_status == 'warning' else "❌"
            print(f"  {status_icon} {task_name}: {task_status}")
        
        return 0 if results['overall_status'] in ['success', 'warning'] else 1
        
    except Exception as e:
        logger.error(f"❌ Scheduled backup failed: {e}")
        return 1

if __name__ == "__main__":
    exit(main())