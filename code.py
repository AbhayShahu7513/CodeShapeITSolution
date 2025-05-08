import os
import shutil
import time
from datetime import datetime
import hashlib
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Define categories and their associated file extensions
FILE_CATEGORIES = {
    "Images": ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.tiff'],
    "Documents": ['.pdf', '.docx', '.doc', '.txt', '.xlsx', '.pptx', '.odt', '.rtf', '.csv'],
    "Videos": ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm'],
    "Music": ['.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a'],
    "Archives": ['.zip', '.rar', '.tar', '.gz', '.7z', '.bz2', '.xz'],
    "Scripts": ['.py', '.js', '.php', '.html', '.css', '.sh', '.bat', '.json', '.xml'],
    "Executables": ['.exe', '.msi', '.dmg', '.pkg', '.deb', '.rpm'],
    "Databases": ['.db', '.sql', '.sqlite', '.mdb'],
    "Design": ['.psd', '.ai', '.sketch', '.fig', '.xd'],
    "Others": []  # Files not matching any category
}

# Default paths
DEFAULT_PATHS = {
    "Windows": os.path.join(os.path.expanduser("~"), "Downloads"),
    "Linux": os.path.join(os.path.expanduser("~"), "Downloads"),
    "Darwin": os.path.join(os.path.join(os.path.expanduser("~")), "Downloads")
}

# Configuration
CONFIG = {
    "ENABLE_LOGGING": True,
    "LOG_FILE": "file_organizer_log.txt",
    "ENABLE_DUPLICATE_CHECK": True,
    "ENABLE_AUTO_ORGANIZE": False,
    "AUTO_ORGANIZE_INTERVAL": 300,  # 5 minutes in seconds
    "ENABLE_FILE_STATS": True
}

class FileOrganizer:
    def __init__(self, target_folder):
        self.target_folder = target_folder
        self.file_stats = {category: 0 for category in FILE_CATEGORIES}
        self.file_stats['Total'] = 0
        self.duplicates_found = 0

    def get_file_category(self, extension):
        """Return the category name based on file extension."""
        for category, extensions in FILE_CATEGORIES.items():
            if extension.lower() in extensions:
                return category
        return "Others"

    def create_folder_if_not_exists(self, path):
        """Create folder if it doesn't already exist."""
        if not os.path.exists(path):
            os.makedirs(path)
            if CONFIG["ENABLE_LOGGING"]:
                self.log_message(f"Created folder: {os.path.basename(path)}")

    def calculate_file_hash(self, filepath):
        """Calculate MD5 hash of a file for duplicate detection."""
        hash_md5 = hashlib.md5()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def is_duplicate(self, filepath, dest_folder):
        """Check if file is a duplicate in destination folder."""
        if not CONFIG["ENABLE_DUPLICATE_CHECK"]:
            return False
            
        filename = os.path.basename(filepath)
        dest_path = os.path.join(dest_folder, filename)
        
        # If file with same name exists, compare hashes
        if os.path.exists(dest_path):
            source_hash = self.calculate_file_hash(filepath)
            dest_hash = self.calculate_file_hash(dest_path)
            return source_hash == dest_hash
        return False

    def handle_duplicate(self, filepath, dest_folder):
        """Handle duplicate files by renaming or skipping."""
        filename, extension = os.path.splitext(os.path.basename(filepath))
        counter = 1
        
        while True:
            new_filename = f"{filename}_{counter}{extension}"
            new_dest_path = os.path.join(dest_folder, new_filename)
            
            if not os.path.exists(new_dest_path):
                return new_dest_path
            counter += 1

    def log_message(self, message):
        """Log messages to file and print to console."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - {message}"
        print(log_entry)
        
        if CONFIG["ENABLE_LOGGING"]:
            with open(os.path.join(self.target_folder, CONFIG["LOG_FILE"]), 'a') as log_file:
                log_file.write(log_entry + "\n")

    def organize_files(self):
        """Main logic to organize files in the target folder."""
        if not os.path.isdir(self.target_folder):
            self.log_message(f"Invalid folder path: {self.target_folder}")
            return False

        self.log_message(f"Starting organization of: {self.target_folder}")
        
        # List all files in the folder
        for filename in os.listdir(self.target_folder):
            source_path = os.path.join(self.target_folder, filename)

            # Skip if it's a folder or the log file
            if os.path.isdir(source_path) or filename == CONFIG["LOG_FILE"]:
                continue

            # Get file extension
            _, extension = os.path.splitext(filename)

            # Determine category
            category = self.get_file_category(extension)

            # Create destination folder
            dest_folder = os.path.join(self.target_folder, category)
            self.create_folder_if_not_exists(dest_folder)

            # Check for duplicates
            if self.is_duplicate(source_path, dest_folder):
                self.duplicates_found += 1
                self.log_message(f"Duplicate found, skipping: {filename}")
                continue

            # Handle naming conflicts
            dest_path = os.path.join(dest_folder, filename)
            if os.path.exists(dest_path):
                dest_path = self.handle_duplicate(source_path, dest_folder)
                self.log_message(f"Renaming duplicate: {filename} → {os.path.basename(dest_path)}")

            # Move the file
            try:
                shutil.move(source_path, dest_path)
                self.file_stats[category] += 1
                self.file_stats['Total'] += 1
                self.log_message(f"Moved: {filename} → {category}")
            except Exception as e:
                self.log_message(f"Error moving {filename}: {str(e)}")

        # Print summary statistics
        if CONFIG["ENABLE_FILE_STATS"]:
            self.print_stats()
            
        return True

    def print_stats(self):
        """Print organization statistics."""
        self.log_message("\n=== Organization Statistics ===")
        for category, count in self.file_stats.items():
            if count > 0:
                self.log_message(f"{category}: {count} files")
        
        if self.duplicates_found > 0:
            self.log_message(f"\nDuplicate files skipped: {self.duplicates_found}")
        
        self.log_message("=" * 30 + "\n")

class AutoOrganizeHandler(FileSystemEventHandler):
    def __init__(self, organizer):
        self.organizer = organizer

    def on_modified(self, event):
        if not event.is_directory:
            time.sleep(2)  # Wait a bit for file operations to complete
            self.organizer.organize_files()

def get_default_folder():
    """Get default folder based on operating system."""
    system = os.name
    if system == 'nt':
        return DEFAULT_PATHS["Windows"]
    elif system == 'posix':
        if os.uname().sysname == 'Darwin':
            return DEFAULT_PATHS["Darwin"]
        else:
            return DEFAULT_PATHS["Linux"]
    return os.path.expanduser("~")

def start_auto_organize(organizer):
    """Start watching the folder for changes."""
    event_handler = AutoOrganizeHandler(organizer)
    observer = Observer()
    observer.schedule(event_handler, organizer.target_folder, recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def main():
    print("=== Enhanced File Organizer ===")
    print("Features: Auto-categorization, Duplicate detection, Real-time monitoring, Statistics\n")
    
    default_folder = get_default_folder()
    user_input = input(f"Enter folder path (or press Enter for default [{default_folder}]): ").strip()
    folder_to_scan = user_input if user_input else default_folder

    organizer = FileOrganizer(folder_to_scan)
    
    # Initial organization
    organizer.organize_files()
    
    # Start auto-organize if enabled
    if CONFIG["ENABLE_AUTO_ORGANIZE"]:
        print("\nAuto-organize mode enabled. Monitoring folder for changes...")
        print("Press Ctrl+C to stop\n")
        start_auto_organize(organizer)

if __name__ == "__main__":
    main()