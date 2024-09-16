import os
import shutil
import argparse
import logging
import sys
import time
import psutil
from typing import Iterator, Tuple, List
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import tqdm
import platform

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
MAX_MEMORY_PERCENT = 80
BATCH_SIZE = 1000
MAX_DEPTH = 10  # Maximum directory depth to prevent infinite recursion

def display_ascii_art():
    """Display ASCII art."""
    ascii_art = r"""
    ╔═══════════════════════════════════════════╗
    ║   ____                      _             ║
    ║  / ___| _ __ ___   __ _ _ __| |_          ║
    ║  \___ \| '_ ` _ \ / _` | '__| __|         ║
    ║   ___) | | | | | | (_| | |  | |_          ║
    ║  |____/|_| |_| |_|\__,_|_|   \__|         ║
    ║                                           ║
    ║        Cache Cleaner                      ║
    ╚═══════════════════════════════════════════╝
    """
    print(ascii_art)

def display_welcome_message():
    """Display a welcome message with ASCII art."""
    display_ascii_art()
    print("Welcome to Smart Cache Cleaner!")
    print("\nThis utility helps you clean up unnecessary files and free up space on your computer.")
    print("It scans common cache and temporary directories, allowing you to choose which files to delete.")
    print("\nLet's get started!")
    input("\nPress Enter to continue...")

def get_cache_and_temp_dirs() -> List[str]:
    """Return a list of common cache and temp directories based on the OS."""
    system = platform.system()
    dirs = []

    if system == "Windows":
        dirs.extend([
            os.path.expandvars(r'%TEMP%'),
            os.path.expandvars(r'%LOCALAPPDATA%\Temp'),
            os.path.expandvars(r'%WINDIR%\Temp'),
            os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\Windows\INetCache'),
            os.path.expandvars(r'%USERPROFILE%\Downloads'),
        ])
    elif system == "Darwin":  # macOS
        dirs.extend([
            '/tmp',
            os.path.expanduser('~/Library/Caches'),
            os.path.expanduser('~/Library/Logs'),
            os.path.expanduser('~/.Trash'),
            os.path.expanduser('~/Downloads'),
        ])
    else:  # Linux and other Unix-like systems
        dirs.extend([
            '/tmp',
            os.path.expanduser('~/.cache'),
            '/var/tmp',
            '/var/cache',
            os.path.expanduser('~/.local/share/Trash'),
            '/var/log',
            os.path.expanduser('~/Downloads'),
        ])

    return [d for d in dirs if os.path.exists(d)]

def scan_directory(directory: str, depth: int = 0) -> Iterator[Tuple[str, int, datetime]]:
    """Scan a directory and yield file information."""
    if depth > MAX_DEPTH:
        logger.warning(f"Maximum directory depth reached in {directory}")
        return

    try:
        for entry in os.scandir(directory):
            try:
                if entry.is_file(follow_symlinks=False):
                    stats = entry.stat()
                    yield (entry.path, stats.st_size, datetime.fromtimestamp(stats.st_mtime))
                elif entry.is_dir(follow_symlinks=False):
                    yield from scan_directory(entry.path, depth + 1)
            except OSError as e:
                logger.warning(f"Error accessing {entry.path}: {e}")
    except PermissionError as e:
        logger.error(f"Permission denied when scanning {directory}: {e}")
        yield f"Permission denied: {directory}"

def human_readable_size(size: int) -> str:
    """Convert size in bytes to human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.1f}{unit}"
        size /= 1024.0

def filter_files(files: Iterator[Tuple[str, int, datetime]], min_size: int, max_age: int) -> Iterator[Tuple[str, int, datetime]]:
    """Filter files based on minimum size and maximum age."""
    now = datetime.now()
    for file_info in files:
        if isinstance(file_info, str):  # This is a permission denied message
            yield file_info
        else:
            file_path, size, mtime = file_info
            if size >= min_size and (max_age == 0 or (now - mtime).days <= max_age):
                yield (file_path, size, mtime)

def delete_file(file_path: str, original_hash: str) -> Tuple[str, bool]:
    """Delete a single file or directory after verifying its hash."""
    try:
        if original_hash == '' or verify_file_hash(file_path, original_hash):
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
            return file_path, True
        else:
            logger.warning(f"File hash mismatch for {file_path}. Skipping deletion.")
            return file_path, False
    except OSError as e:
        logger.error(f"Error deleting {file_path}: {e}")
        return file_path, False

def check_memory_usage() -> bool:
    """Check if memory usage is within acceptable limits."""
    memory_percent = psutil.virtual_memory().percent
    if memory_percent > MAX_MEMORY_PERCENT:
        logger.warning(f"High memory usage detected: {memory_percent}%. Consider processing in smaller batches.")
        return False
    return True

def process_files_in_batches(directory: str, min_size: int, max_age: int, batch_size: int = BATCH_SIZE) -> Iterator[Tuple[str, int, datetime]]:
    """Process files in batches to conserve memory."""
    batch = []
    permission_denied_files = []
    for file_info in filter_files(scan_directory(directory), min_size, max_age):
        if isinstance(file_info, tuple):
            batch.append(file_info)
            if len(batch) >= batch_size:
                yield from batch
                batch = []
                if not check_memory_usage():
                    logger.info("Pausing to allow memory cleanup...")
                    time.sleep(5)  # Give some time for memory to be freed
        elif isinstance(file_info, str):
            permission_denied_files.append(file_info)
    if batch:
        yield from batch
    if permission_denied_files:
        print("\nThe following files require higher privileges to access:")
        for file in permission_denied_files:
            print(f"  - {file}")

def verify_file_hash(file_path: str, original_hash: str) -> bool:
    """Verify the file hash hasn't changed before deletion."""
    try:
        with open(file_path, "rb") as f:
            file_hash = hashlib.md5()
            for chunk in iter(lambda: f.read(4096), b""):
                file_hash.update(chunk)
        return file_hash.hexdigest() == original_hash
    except OSError:
        return False

def main():
    display_welcome_message()

    parser = argparse.ArgumentParser(
        description="Smart Cache Cleaner: Clear caches and temp files intelligently.",
        epilog="""
During the scanning process, you will be prompted for each file:
  y: Yes, delete this file
  n: No, skip this file
  q: Quit the scanning process

You can also use the -y option to skip these prompts and delete all matched files.
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('-d', '--directory', help="Specify a custom directory to scan")
    parser.add_argument('-s', '--min-size', type=int, default=0, help="Minimum file size to consider (in bytes)")
    parser.add_argument('-a', '--max-age', type=int, default=0, help="Maximum file age to consider (in days, 0 for no limit)")
    parser.add_argument('-y', '--yes', action='store_true', help="Skip confirmation for deletion")
    parser.add_argument('-v', '--verbose', action='store_true', help="Increase output verbosity")
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    directories = [args.directory] if args.directory else get_cache_and_temp_dirs()

    files_to_delete = []
    total_size = 0
    total_files = 0
    files_by_extension = {}

    for directory in directories:
        print(f"\nScanning {directory}...")
        
        with tqdm.tqdm(desc="Scanning", unit="file", leave=False) as pbar:
            for file_path, size, last_modified in process_files_in_batches(directory, args.min_size, args.max_age):
                pbar.update(1)
                total_files += 1
                
                _, ext = os.path.splitext(file_path)
                if ext not in files_by_extension:
                    files_by_extension[ext] = {'count': 0, 'size': 0}
                files_by_extension[ext]['count'] += 1
                files_by_extension[ext]['size'] += size
                
                if not args.yes:
                    print(f"\nFile: {file_path}")
                    print(f"Size: {human_readable_size(size)}")
                    print(f"Last modified: {last_modified}")
                    choice = input("Delete this file? (y/n/q): ").lower()
                    if choice == 'q':
                        break
                    elif choice == 'y':
                        files_to_delete.append((file_path, ''))  # Empty hash for immediate deletion
                        total_size += size
                else:
                    files_to_delete.append((file_path, ''))  # Empty hash for immediate deletion
                    total_size += size

    print(f"\nScan complete! Processed {total_files} files.")

    if not files_to_delete:
        print("No files selected for deletion.")
        return

    print("\nFiles by extension:")
    for ext, info in files_by_extension.items():
        print(f"  {ext or 'No extension'}: {info['count']} files, {human_readable_size(info['size'])}")

    if not args.yes:
        confirm = input(f"\nYou've selected {len(files_to_delete)} files to delete "
                        f"(Total size: {human_readable_size(total_size)}). Proceed? (y/n): ").lower()
    else:
        confirm = 'y'
    
    if confirm == 'y':
        print("\nDeleting files:")
        with tqdm.tqdm(total=len(files_to_delete), unit="file") as pbar:
            for file_path, _ in files_to_delete:
                success = delete_file(file_path, '')[1]
                if success:
                    pbar.update(1)
                else:
                    print(f"Failed to delete: {file_path}")
        print(f"\nDeletion complete. Freed up approximately {human_readable_size(total_size)}")
    else:
        print("Deletion cancelled.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)
