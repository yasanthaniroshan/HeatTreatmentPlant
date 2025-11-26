# 🔄 Automatic Backup System - Quick Start

Your Heat Treatment Plant Control system now includes automatic backup functionality!

---

## ⚡ Quick Setup (2 Steps)

### Step 1: Install Package

```bash
pip install schedule
```

### Step 2: Start Automatic Backups

Choose one option:

#### Option A: Manual Backup (Run Anytime)

```bash
# Complete backup now
cd smartAquarium
python manage.py backup_database

# View status
python manage.py backup_database --status
```

#### Option B: Scheduled Automatic Backups (Windows)

```bash
# Run in terminal (keeps running)
python scheduled_backup.py
```

#### Option C: Windows Task Scheduler (Background Automation)

1. Press `Win + R`, type `tasksched.msc`
2. Click "Create Basic Task"
3. Name: `Heat Treatment Plant Control Backup`
4. Trigger: Daily at 2:00 AM
5. Action: Start a program
6. Program: `C:\Python\python.exe` (your Python path)
7. Arguments: `C:\...\smartAquarium\scheduled_backup.py`

---

## 📁 Where Your Backups Are Stored

```
smartAquarium/backups/
├── database/          ← SQLite database backups
├── csv_exports/       ← Excel-friendly exports
└── json_exports/      ← Integration-friendly exports
```

---

## 🎯 What Gets Backed Up

✅ **Database** - Complete snapshot of your data
✅ **CSV** - Readable in Excel or any spreadsheet
✅ **JSON** - Perfect for data analysis and integration

---

## 📊 Backup Schedule (Automatic)

If using `scheduled_backup.py`:

| When | What |
|------|------|
| **Every Hour** | Complete backup (DB + CSV + JSON) |
| **Daily 2 AM** | Complete backup + cleanup old files |
| **Sunday 3 AM** | Complete backup + statistics |

---

## 🚀 Common Commands

```bash
# Backup right now
python manage.py backup_database

# View backup status and statistics
python manage.py backup_database --status

# Backup only database
python manage.py backup_database --type db

# Backup only CSV
python manage.py backup_database --type csv

# Backup only JSON
python manage.py backup_database --type json

# Clean up backups older than 30 days
python manage.py backup_database --cleanup
```

---

## 💾 Example Output

```
$ python manage.py backup_database
Database backed up to backups/database/db_backup_20250111_143022.sqlite3
Readings exported to CSV: backups/csv_exports/readings_20250111_143022.csv
Readings exported to JSON: backups/json_exports/readings_20250111_143022.json
Backup completed!
```

---

## 📈 View Your Data

### Windows

```bash
# Open backups folder
cd smartAquarium\backups
explorer .

# Or open a CSV file in Excel
start csv_exports\readings_*.csv
```

### Linux / Raspberry Pi

```bash
# List all backups
ls -lah backups/

# View CSV in terminal
cat backups/csv_exports/readings_*.csv

# Copy to USB drive
cp -r backups/ /mnt/backup/
```

---

## 🔐 Protection Tips

1. **Automatic Backups** - Use scheduled_backup.py
2. **External Backup** - Copy to USB drive or cloud
3. **Regular Cleanup** - Old files are deleted automatically (30+ days)
4. **Check Logs** - View `backups/scheduled_backup.log`

---

## ✨ You Now Have

✅ Local database backups
✅ CSV exports for Excel/analysis
✅ JSON exports for integration
✅ Automatic scheduling support
✅ Old backup cleanup
✅ Activity logging

**Your data is protected!** 🎉

---

## 📚 More Info

Full guide: [BACKUP_GUIDE.md](BACKUP_GUIDE.md)

Next step: Run your first backup!
```bash
python manage.py backup_database --status
```
