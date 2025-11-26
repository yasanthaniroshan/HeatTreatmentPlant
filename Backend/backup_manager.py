"""
Automatic Database Backup Manager
Backs up SQLite database and exports readings to CSV/JSON files
"""

import os
import json
import csv
import shutil
from datetime import datetime
from pathlib import Path
import sqlite3
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DatabaseBackupManager:
    """Manages automatic backups of the Heat Treatment Plant Control database"""
    
    def __init__(self, db_path='db.sqlite3', backup_dir='backups'):
        """
        Initialize backup manager
        
        Args:
            db_path: Path to the SQLite database
            backup_dir: Directory to store backups (relative to project root)
        """
        self.db_path = db_path
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        self.db_backup_dir = self.backup_dir / 'database'
        self.csv_backup_dir = self.backup_dir / 'csv_exports'
        self.json_backup_dir = self.backup_dir / 'json_exports'
        
        self.db_backup_dir.mkdir(exist_ok=True)
        self.csv_backup_dir.mkdir(exist_ok=True)
        self.json_backup_dir.mkdir(exist_ok=True)
        
        logger.info(f"Backup manager initialized. Backup directory: {self.backup_dir}")
    
    def backup_database(self):
        """Create a backup copy of the SQLite database"""
        if not os.path.exists(self.db_path):
            logger.warning(f"Database not found at {self.db_path}")
            return None
        
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_filename = f'db_backup_{timestamp}.sqlite3'
            backup_path = self.db_backup_dir / backup_filename
            
            # Copy database file
            shutil.copy2(self.db_path, backup_path)
            
            logger.info(f"Database backed up to {backup_path}")
            return backup_path
        except Exception as e:
            logger.error(f"Error backing up database: {e}")
            return None
    
    def export_readings_to_csv(self):
        """Export all temperature readings to CSV file"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get all readings
            cursor.execute('''
                SELECT water_temperature, air_temperature, humidity, 
                       setpoint, pid_output, created_at
                FROM api_temperaturereading
                ORDER BY created_at DESC
            ''')
            
            readings = cursor.fetchall()
            conn.close()
            
            if not readings:
                logger.info("No readings to export")
                return None
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            csv_filename = f'readings_{timestamp}.csv'
            csv_path = self.csv_backup_dir / csv_filename
            
            # Write CSV file
            with open(csv_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([
                    'Water Temp (°C)', 'Air Temp (°C)', 'Humidity (%)',
                    'Setpoint (°C)', 'PID Output', 'Timestamp'
                ])
                writer.writerows(readings)
            
            logger.info(f"Readings exported to CSV: {csv_path}")
            return csv_path
        except Exception as e:
            logger.error(f"Error exporting to CSV: {e}")
            return None
    
    def export_readings_to_json(self):
        """Export all temperature readings to JSON file"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get all readings
            cursor.execute('''
                SELECT water_temperature, air_temperature, humidity, 
                       setpoint, pid_output, created_at
                FROM api_temperaturereading
                ORDER BY created_at DESC
            ''')
            
            rows = cursor.fetchall()
            conn.close()
            
            if not rows:
                logger.info("No readings to export")
                return None
            
            # Convert to JSON format
            readings = []
            for row in rows:
                readings.append({
                    'water_temperature': row[0],
                    'air_temperature': row[1],
                    'humidity': row[2],
                    'setpoint': row[3],
                    'pid_output': row[4],
                    'timestamp': row[5]
                })
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            json_filename = f'readings_{timestamp}.json'
            json_path = self.json_backup_dir / json_filename
            
            # Write JSON file
            with open(json_path, 'w') as jsonfile:
                json.dump(readings, jsonfile, indent=2)
            
            logger.info(f"Readings exported to JSON: {json_path}")
            return json_path
        except Exception as e:
            logger.error(f"Error exporting to JSON: {e}")
            return None
    
    def get_latest_reading(self):
        """Get the latest temperature reading"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT water_temperature, air_temperature, humidity, 
                       setpoint, pid_output, created_at
                FROM api_temperaturereading
                ORDER BY created_at DESC
                LIMIT 1
            ''')
            
            reading = cursor.fetchone()
            conn.close()
            
            if reading:
                return {
                    'water_temperature': reading[0],
                    'air_temperature': reading[1],
                    'humidity': reading[2],
                    'setpoint': reading[3],
                    'pid_output': reading[4],
                    'timestamp': reading[5]
                }
            return None
        except Exception as e:
            logger.error(f"Error getting latest reading: {e}")
            return None
    
    def get_statistics(self):
        """Get statistics about the readings"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Count readings
            cursor.execute('SELECT COUNT(*) FROM api_temperaturereading')
            total_readings = cursor.fetchone()[0]
            
            # Get temperature stats
            cursor.execute('''
                SELECT 
                    MIN(water_temperature), MAX(water_temperature), AVG(water_temperature),
                    MIN(air_temperature), MAX(air_temperature), AVG(air_temperature),
                    AVG(humidity)
                FROM api_temperaturereading
            ''')
            
            stats = cursor.fetchone()
            conn.close()
            
            return {
                'total_readings': total_readings,
                'water_temp_min': stats[0],
                'water_temp_max': stats[1],
                'water_temp_avg': stats[2],
                'air_temp_min': stats[3],
                'air_temp_max': stats[4],
                'air_temp_avg': stats[5],
                'humidity_avg': stats[6]
            }
        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            return None
    
    def backup_everything(self):
        """Perform a complete backup (database + CSV + JSON)"""
        logger.info("Starting complete backup...")
        
        results = {
            'database': self.backup_database(),
            'csv': self.export_readings_to_csv(),
            'json': self.export_readings_to_json()
        }
        
        logger.info("Complete backup finished!")
        return results
    
    def cleanup_old_backups(self, days_to_keep=30):
        """Delete backups older than specified days"""
        try:
            cutoff_time = datetime.now().timestamp() - (days_to_keep * 24 * 3600)
            deleted_count = 0
            
            for backup_dir in [self.db_backup_dir, self.csv_backup_dir, self.json_backup_dir]:
                for file in backup_dir.iterdir():
                    if file.is_file() and file.stat().st_mtime < cutoff_time:
                        file.unlink()
                        deleted_count += 1
                        logger.info(f"Deleted old backup: {file.name}")
            
            logger.info(f"Cleanup completed. Deleted {deleted_count} old backups.")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
    
    def print_status(self):
        """Print backup status and statistics"""
        print("\n" + "="*60)
        print("HEAT TREATMENT PLANT CONTROL - BACKUP STATUS")
        print("="*60)
        
        # Backup directory stats
        db_backups = list(self.db_backup_dir.glob('*.sqlite3'))
        csv_files = list(self.csv_backup_dir.glob('*.csv'))
        json_files = list(self.json_backup_dir.glob('*.json'))
        
        print(f"\nBackup Location: {self.backup_dir.absolute()}")
        print(f"Database Backups: {len(db_backups)}")
        print(f"CSV Exports: {len(csv_files)}")
        print(f"JSON Exports: {len(json_files)}")
        
        # Database statistics
        stats = self.get_statistics()
        if stats:
            print(f"\nDatabase Statistics:")
            print(f"  Total Readings: {stats['total_readings']}")
            print(f"  Water Temp Range: {stats['water_temp_min']:.2f}°C - {stats['water_temp_max']:.2f}°C")
            print(f"  Water Temp Avg: {stats['water_temp_avg']:.2f}°C")
            print(f"  Air Temp Range: {stats['air_temp_min']:.2f}°C - {stats['air_temp_max']:.2f}°C")
            print(f"  Air Temp Avg: {stats['air_temp_avg']:.2f}°C")
            print(f"  Humidity Avg: {stats['humidity_avg']:.2f}%")
        
        # Latest reading
        latest = self.get_latest_reading()
        if latest:
            print(f"\nLatest Reading:")
            print(f"  Water: {latest['water_temperature']:.2f}°C")
            print(f"  Air: {latest['air_temperature']:.2f}°C")
            print(f"  Humidity: {latest['humidity']:.2f}%")
            print(f"  Setpoint: {latest['setpoint']:.2f}°C")
            print(f"  Time: {latest['timestamp']}")
        
        print("="*60 + "\n")


if __name__ == '__main__':
    # Example usage
    backup_manager = DatabaseBackupManager()
    
    # Perform complete backup
    backup_manager.backup_everything()
    
    # Print status
    backup_manager.print_status()
    
    # Cleanup old backups (keep last 30 days)
    backup_manager.cleanup_old_backups(days_to_keep=30)
