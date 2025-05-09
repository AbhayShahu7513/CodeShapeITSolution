# 🗂️ Enhanced File Organizer

A Python-based console application that automatically organizes files in a folder based on their file types. Features include real-time monitoring, duplicate detection, categorization, and organization statistics.

## 🔧 Features

- ✅ Categorizes files into predefined folders (Images, Documents, Music, etc.)
- ✅ Duplicate file detection using MD5 hashing
- ✅ Auto-organize mode (watches folder for changes using `watchdog`)
- ✅ Logs all operations in a log file
- ✅ Shows file organization statistics
- ✅ Customizable via configuration

## 📁 File Categories

- Images (.jpg, .png, .webp, etc.)
- Documents (.pdf, .docx, .txt, etc.)
- Music (.mp3, .wav, etc.)
- Videos (.mp4, .avi, etc.)
- Scripts (.py, .js, .html, etc.)
- Archives (.zip, .rar, etc.)
- Executables (.exe, .msi, etc.)
- Design files (.psd, .ai, etc.)
- Databases (.db, .sql, etc.)
- Others (Anything uncategorized)

## 🚀 How to Run on Replit

1. **Fork or Import the Project**
   - Go to [Replit](https://replit.com)
   - Create a new Python Repl or import this repo

2. **Upload Your Script Files**
   - Upload the `file_organizer.py` file (your main code file)
   - Ensure your working directory has test files (to organize)

3. **Install Dependencies**
   - Go to `Packages` tab in Replit
   - Search for and install:
     - `watchdog`

4. **Enable Console**
   - Replit runs in a console. This project uses `input()` and `print()` so console access is sufficient.

5. **Run the Project**
   - Click on the green "Run" button
   - Or type in console:
     ```bash
     python file_organizer.py
     ```

6. **Choose a Folder**
   - Enter a folder path to organize (can be current working folder).
   - Or press Enter to use default Downloads directory (may not work on Replit; instead use `.` for current Replit workspace).

7. **Monitor Changes (Optional)**
   - Enable `ENABLE_AUTO_ORGANIZE` in the `CONFIG` dictionary inside the script:
     ```python
     "ENABLE_AUTO_ORGANIZE": True
     ```
   - Save and rerun.

> 📝 Note: Replit has sandboxed file access. Use the current Replit directory (`.`) and upload files there for testing.

## 📂 Log and Output

- A log file named `file_organizer_log.txt` is created in the working folder.
- It records all operations including:
  - Moved files
  - Created folders
  - Skipped duplicates
  - Errors

## ⚙️ Configuration

Customize settings inside the script:

```python
CONFIG = {
    "ENABLE_LOGGING": True,
    "LOG_FILE": "file_organizer_log.txt",
    "ENABLE_DUPLICATE_CHECK": True,
    "ENABLE_AUTO_ORGANIZE": False,
    "AUTO_ORGANIZE_INTERVAL": 300,
    "ENABLE_FILE_STATS": True
}
