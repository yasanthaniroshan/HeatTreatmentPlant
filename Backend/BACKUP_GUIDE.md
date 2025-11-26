# Automatic Data Backup Guide

## Overview

Your Heat Treatment Plant Control system now includes **automatic backup** functionality to protect your temperature data. The system can:

- ✅ Back up the SQLite database automatically
- ✅ Export readings to CSV format (for Excel/analysis)
- ✅ Export readings to JSON format (for integration)
- ✅ Schedule backups hourly, daily, and weekly
- ✅ Automatically clean up old backups
- ✅ Store backups locally on your computer

---

## 📁 Backup Structure

All backups are stored in the `backups/` folder:

```
smartAquarium/
└── backups/
    ├── scheduled_backup.log         ← Backup activity log
    ├── database/
    │   ├── db_backup_20250111_080000.sqlite3
    │   ├── db_backup_20250111_090000.sqlite3
    │   └── ...
    ├── csv_exports/
    │   ├── readings_20250111_080000.csv
    │   ├── readings_20250111_090000.csv
    │   └── ...
    └── json_exports/
        ├── readings_20250111_080000.json
        ├── readings_20250111_090000.json
        └── ...
```

---

## 🚀 Quick Setup (3 Steps)

### Step 1: Install Scheduler Package

```bash
pip install schedule
```

### Step 2: Create Backup Folders

The folders are created automatically on first use.

### Step 3: Start Automatic Backups

#### Option A: Manual Backup (Anytime)

```bash
# Complete backup (database + CSV + JSON)
python manage.py backup_database

# Or specific backups
python manage.py backup_database --type db      # Database only
python manage.py backup_database --type csv     # CSV only
python manage.py backup_database --type json    # JSON only

# View status and statistics
python manage.py backup_database --status

# Clean up backups older than 30 days
python manage.py backup_database --cleanup
```

#### Option B: Scheduled Automatic Backups

Run the scheduler as a background service:

```bash
# Windows - Run in background
python scheduled_backup.py

# Or use Windows Task Scheduler (see below)
```

#### Option C: Windows Task Scheduler (Automated)

Create a scheduled task that runs automatically:

```batch
# 1. Open Task Scheduler
tasksched.msc

# 2. Create Basic Task
# - Name: "Heat Treatment Plant Control Backup"
# - Trigger: Daily at 2:00 AM (or your preferred time)
# - Action: Start a program
# - Program: C:\Python\python.exe (your Python path)
# - Arguments: C:\path\to\smartAquarium\scheduled_backup.py
# - Settings: Run with highest privileges
```

---

## 📊 What Gets Backed Up

### Database Backup (SQLite)
- Complete database snapshot
- All temperature readings
- All configuration settings
- Admin user accounts
- File size: ~100KB - 1MB (depending on data volume)

### CSV Export
- Human-readable format
- Can open in Excel/LibreOffice
- Columns: Water Temp, Air Temp, Humidity, Setpoint, PID Output, Timestamp
- Great for analysis and charts

### JSON Export
- Machine-readable format
- Structured data format
- Perfect for integration with other systems
- Easy to parse and process

---

## 📈 Backup Schedule

Default automatic backup schedule (if using scheduled_backup.py):

| Frequency | Time | What |
|-----------|------|------|
| **Hourly** | Every hour | Complete backup (DB + CSV + JSON) |
| **Daily** | 2:00 AM | Complete backup + cleanup old files |
| **Weekly** | Sunday 3:00 AM | Complete backup + statistics |

---

## 💾 Examples

### Manual Backup Now

```bash
cd smartAquarium
python manage.py backup_database
```

Output:
```
Database backed up to backups/database/db_backup_20250111_143022.sqlite3
Readings exported to CSV: backups/csv_exports/readings_20250111_143022.csv
Readings exported to JSON: backups/json_exports/readings_20250111_143022.json
Backup completed!
```

### View Backup Status

```bash
python manage.py backup_database --status
```

Output:
```
============================================================
HEAT TREATMENT PLANT CONTROL - BACKUP STATUS
============================================================

Backup Location: C:\...\smartAquarium\backups

Database Backups: 10
CSV Exports: 10
JSON Exports: 10

Database Statistics:
  Total Readings: 1,234
  Water Temp Range: 20.50°C - 28.75°C
  Water Temp Avg: 25.12°C
  Air Temp Range: 22.00°C - 29.50°C
  Air Temp Avg: 25.80°C
  Humidity Avg: 65.23%

Latest Reading:
  Water: 25.43°C
  Air: 26.20°C
  Humidity: 60.50%
  Setpoint: 25.00°C
  Time: 2025-01-11 14:30:22
============================================================
```

### Clean Up Old Backups

```bash
# Keep only backups from last 30 days
python manage.py backup_database --cleanup

# Or modify in backup_manager.py:
backup_manager.cleanup_old_backups(days_to_keep=7)  # Keep 7 days
backup_manager.cleanup_old_backups(days_to_keep=90) # Keep 90 days
```

---

## 🔍 Understanding Your Backups

### CSV Format Example

```csv
Water Temp (°C),Air Temp (°C),Humidity (%),Setpoint (°C),PID Output,Timestamp
24.50,26.20,60.50,25.00,120,2025-01-11 14:30:22
24.52,26.18,60.48,25.00,115,2025-01-11 14:30:24
24.54,26.15,60.45,25.00,110,2025-01-11 14:30:26
```

### JSON Format Example

```json
[
  {
    "water_temperature": 24.50,
    "air_temperature": 26.20,
    "humidity": 60.50,
    "setpoint": 25.00,
    "pid_output": 120,
    "timestamp": "2025-01-11 14:30:22"
  },
  {
    "water_temperature": 24.52,
    "air_temperature": 26.18,
    "humidity": 60.48,
    "setpoint": 25.00,
    "pid_output": 115,
    "timestamp": "2025-01-11 14:30:24"
  }
]
```

---

## 📱 Accessing Your Backups

### On Windows

```bash
# Open backups folder
cd smartAquarium\backups

# List all files
dir /s

# Open in Explorer
explorer .
```

### On Raspberry Pi / Linux

```bash
# Open backups folder
cd smartAquarium/backups

# List all files
ls -la

# View CSV file
cat csv_exports/readings_*.csv

# View JSON file
cat json_exports/readings_*.json
```

---

## 🛡️ Backup Protection

### Best Practices

1. **Regular Backups** - Use automated scheduling
2. **Multiple Locations** - Copy backups to external drive
3. **Check Backups** - Verify files are created
4. **Delete Old Files** - Use cleanup feature
5. **Test Restore** - Periodically test recovery

### Create Remote Backup (Windows)

```bash
# Copy backups to external drive
xcopy backups\ "D:\Backup\HeatTreatment\" /E /Y

# Or to network location
xcopy backups\ "\\backup-server\data\" /E /Y
```

### Create Remote Backup (Linux/Raspberry Pi)

```bash
# Copy to external USB drive
cp -r backups/ /mnt/backup/

# Or to network location
cp -r backups/ /mnt/nas/heattreatment/

# Or use rsync for selective backup
rsync -avz backups/ user@backup-server:/backups/heat-treatment/
```

---

## 🔧 Advanced Configuration

### Modify Backup Schedule

Edit `scheduled_backup.py`:

```python
def schedule_all(self):
    # Backup every 30 minutes instead of hourly
    schedule.every(30).minutes.do(self.run_hourly_backup)
    
    # Backup daily at 11:00 PM
    schedule.every().day.at("23:00").do(self.run_daily_backup)
    
    # Backup every Monday at 4 AM
    schedule.every().monday.at("04:00").do(self.run_weekly_backup)
```

### Modify Cleanup Period

Edit `backup_manager.py`:

```python
# In backup_everything() method:
backup_manager.cleanup_old_backups(days_to_keep=7)   # Keep 7 days
backup_manager.cleanup_old_backups(days_to_keep=90)  # Keep 90 days
```

### Custom Backup Location

Edit `backup_manager.py`:

```python
# Use custom backup location
backup_manager = DatabaseBackupManager(
    db_path='db.sqlite3',
    backup_dir='D:/MyBackups/HeatTreatment'  # Custom path
)
```

---

## 📊 Monitoring Backups

### Check Backup Log

```bash
# View backup log
tail -f backups/scheduled_backup.log

# Windows PowerShell
Get-Content backups\scheduled_backup.log -Tail 20 -Wait
```

### Backup Size Management

```bash
# Windows - Check disk usage
dir backups /s

# Linux/Mac - Check disk usage
du -sh backups/
du -sh backups/*
```

---

## ⚠️ Troubleshooting

### Problem: "schedule module not found"

**Solution:**
```bash
pip install schedule
```

### Problem: Permission denied when creating backups

**Solution:**
- Ensure backup directory is writable
- Run as administrator (Windows)
- Check folder permissions (Linux/Mac)

### Problem: Backup runs but files aren't created

**Solution:**
1. Check database exists: `ls db.sqlite3`
2. Check backup directory: `ls backups/`
3. Check logs: `tail backups/scheduled_backup.log`
4. Run manually: `python manage.py backup_database --status`

### Problem: Disk space running out

**Solution:**
```bash
# Reduce retention period
python manage.py backup_database --cleanup

# Then modify to keep fewer days
# Edit backup_manager.py and change days_to_keep to 7 or 14
```

---

## 📋 Backup Checklist

- [ ] Install schedule package: `pip install schedule`
- [ ] Run manual backup: `python manage.py backup_database`
- [ ] Check backups created: `ls backups/`
- [ ] View status: `python manage.py backup_database --status`
- [ ] Set up scheduled backups (Windows Task Scheduler or scheduled_backup.py)
- [ ] Copy backups to external drive
- [ ] Test restore process (optional but recommended)
- [ ] Set reminder to check backups monthly

---

## 📈 Data Storage Estimates

| Duration | Readings | Database Size | CSV Size | JSON Size |
|----------|----------|---------------|----------|-----------|
| 1 week | 302,400 | 50 MB | 30 MB | 40 MB |
| 1 month | 1.3M | 200 MB | 120 MB | 160 MB |
| 1 year | 15.8M | 2.5 GB | 1.5 GB | 2 GB |

*Estimates based on 1 reading every 2 seconds*

---

## 🎯 Recommended Setup

### For Home/Lab Setup

```bash
# Automatic hourly backups to local computer
python scheduled_backup.py

# Manually copy weekly to USB drive
# Schedule: Every Friday at 6 PM
```

### For Production Deployment

```bash
# Automatic backups via systemd (Linux)
# Or Windows Task Scheduler

# Backup to network location
# Keep 90 days of data

# External backup to cloud storage
# (rsync to AWS S3, Google Drive, OneDrive, etc.)
```

---

## ✅ Summary

Your Heat Treatment Plant Control system now has:

✅ Automatic local database backups
✅ CSV export for analysis
✅ JSON export for integration
✅ Scheduled backup support
✅ Automatic cleanup of old files
✅ Status monitoring
✅ Logging of all backup activity

**Your data is now protected!** 🎉

---

## 📚 Related Documentation

- [DEPLOYMENT_CHECKLIST.md](../../DEPLOYMENT_CHECKLIST.md) - Full deployment guide
- [RASPBERRY_PI_SETUP_GUIDE.md](../../RASPBERRY_PI_SETUP_GUIDE.md) - Remote backups on Raspberry Pi
- [backup_manager.py](backup_manager.py) - Backup code
- [scheduled_backup.py](scheduled_backup.py) - Scheduling code

---

**Backup files are stored in:** `smartAquarium/backups/`

**To access:** Open the backups folder with File Explorer or terminal
