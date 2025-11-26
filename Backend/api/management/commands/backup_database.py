"""
Django management command to perform database backups
Usage: python manage.py backup_database
"""

from django.core.management.base import BaseCommand
from django.conf import settings
from pathlib import Path
import sys

# Add parent directory to path to import backup_manager
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backup_manager import DatabaseBackupManager


class Command(BaseCommand):
    help = 'Backup the database and export readings to CSV/JSON'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--type',
            type=str,
            default='all',
            choices=['all', 'db', 'csv', 'json'],
            help='Type of backup to perform'
        )
        
        parser.add_argument(
            '--cleanup',
            action='store_true',
            help='Delete backups older than 30 days'
        )
        
        parser.add_argument(
            '--status',
            action='store_true',
            help='Show backup status and statistics'
        )
    
    def handle(self, *args, **options):
        backup_manager = DatabaseBackupManager()
        
        # Show status if requested
        if options['status']:
            backup_manager.print_status()
            return
        
        # Perform cleanup if requested
        if options['cleanup']:
            self.stdout.write(self.style.WARNING('Cleaning up old backups...'))
            backup_manager.cleanup_old_backups(days_to_keep=30)
        
        # Perform backup
        backup_type = options['type']
        
        if backup_type == 'all':
            self.stdout.write(self.style.SUCCESS('Starting complete backup...'))
            results = backup_manager.backup_everything()
            
            if results['database']:
                self.stdout.write(self.style.SUCCESS(f'✓ Database backed up'))
            if results['csv']:
                self.stdout.write(self.style.SUCCESS(f'✓ CSV exported'))
            if results['json']:
                self.stdout.write(self.style.SUCCESS(f'✓ JSON exported'))
        
        elif backup_type == 'db':
            self.stdout.write('Backing up database...')
            result = backup_manager.backup_database()
            if result:
                self.stdout.write(self.style.SUCCESS(f'✓ Database backed up: {result}'))
        
        elif backup_type == 'csv':
            self.stdout.write('Exporting to CSV...')
            result = backup_manager.export_readings_to_csv()
            if result:
                self.stdout.write(self.style.SUCCESS(f'✓ CSV exported: {result}'))
        
        elif backup_type == 'json':
            self.stdout.write('Exporting to JSON...')
            result = backup_manager.export_readings_to_json()
            if result:
                self.stdout.write(self.style.SUCCESS(f'✓ JSON exported: {result}'))
        
        self.stdout.write(self.style.SUCCESS('\nBackup completed!'))
