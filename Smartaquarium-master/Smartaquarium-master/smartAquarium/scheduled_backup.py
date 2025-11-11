"""
Automatic Scheduled Backup Script
Runs periodically to backup database and export readings
"""

import schedule
import time
import logging
from pathlib import Path
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('backups/scheduled_backup.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ScheduledBackupService:
    """Service to run scheduled database backups"""
    
    def __init__(self):
        """Initialize the scheduled backup service"""
        from backup_manager import DatabaseBackupManager
        self.backup_manager = DatabaseBackupManager()
        logger.info("Scheduled backup service initialized")
    
    def run_hourly_backup(self):
        """Run hourly backup (database + CSV + JSON)"""
        logger.info("=" * 60)
        logger.info("Starting hourly backup...")
        try:
            results = self.backup_manager.backup_everything()
            logger.info(f"Hourly backup completed: DB={results['database']}, CSV={results['csv']}, JSON={results['json']}")
        except Exception as e:
            logger.error(f"Hourly backup failed: {e}")
    
    def run_daily_backup(self):
        """Run daily backup with cleanup"""
        logger.info("=" * 60)
        logger.info("Starting daily backup with cleanup...")
        try:
            # Backup everything
            self.backup_manager.backup_everything()
            
            # Cleanup old backups (keep 30 days)
            self.backup_manager.cleanup_old_backups(days_to_keep=30)
            
            # Print status
            self.backup_manager.print_status()
            
            logger.info("Daily backup with cleanup completed")
        except Exception as e:
            logger.error(f"Daily backup failed: {e}")
    
    def run_weekly_backup(self):
        """Run weekly backup with comprehensive statistics"""
        logger.info("=" * 60)
        logger.info("Starting weekly backup with statistics...")
        try:
            # Backup everything
            self.backup_manager.backup_everything()
            
            # Get comprehensive statistics
            stats = self.backup_manager.get_statistics()
            if stats:
                logger.info(f"Weekly statistics: {stats}")
            
            logger.info("Weekly backup completed")
        except Exception as e:
            logger.error(f"Weekly backup failed: {e}")
    
    def schedule_all(self):
        """Schedule all backup jobs"""
        # Hourly backup every hour
        schedule.every().hour.at(":00").do(self.run_hourly_backup)
        logger.info("Scheduled: Hourly backup at minute 0")
        
        # Daily backup at 2 AM
        schedule.every().day.at("02:00").do(self.run_daily_backup)
        logger.info("Scheduled: Daily backup at 02:00")
        
        # Weekly backup on Sunday at 3 AM
        schedule.every().sunday.at("03:00").do(self.run_weekly_backup)
        logger.info("Scheduled: Weekly backup on Sunday at 03:00")
    
    def start(self):
        """Start the scheduler and run indefinitely"""
        logger.info("Starting backup scheduler...")
        self.schedule_all()
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            logger.info("Backup scheduler stopped")


def main():
    """Main entry point"""
    logger.info("Heat Treatment Plant Control - Scheduled Backup Service")
    logger.info("Starting automatic backup service...")
    
    service = ScheduledBackupService()
    service.start()


if __name__ == '__main__':
    main()
