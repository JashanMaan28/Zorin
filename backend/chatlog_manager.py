import os
import json
import shutil
from datetime import datetime
import logging

# --- Configuration ---
# Get the directory where the script itself is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory of the script's directory (assumed to be the project root)
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)

# Define the subdirectory and filename for the chatlog (relative to PROJECT_DIR)
CHATLOG_SUBDIR = 'Data'
CHATLOG_FILENAME = 'ChatLog.json'
# Define the name for the archives directory (relative to PROJECT_DIR)
ARCHIVES_DIRNAME = 'chatlog_archives'
# Define the name for the date tracking file (relative to PROJECT_DIR)
DATE_TRACKING_FILENAME = '.last_session_date'
# Define the log file name (relative to SCRIPT_DIR, so it stays in 'backend')
LOG_FILENAME = 'chatlog_manager.log'

# Construct full paths
# Paths relative to the Project Directory
chatlog_path = os.path.join(PROJECT_DIR, CHATLOG_SUBDIR, CHATLOG_FILENAME)
chatlog_dir = os.path.dirname(chatlog_path) # This correctly gets PROJECT_DIR/Data
archives_dir = os.path.join(PROJECT_DIR, ARCHIVES_DIRNAME)
date_tracking_file = os.path.join(PROJECT_DIR, DATE_TRACKING_FILENAME)
# Path relative to the Script Directory (stays within 'backend')
log_file_path = os.path.join(SCRIPT_DIR, LOG_FILENAME)

# --- Logging Setup ---
def setup_logging():
    """Sets up logging configuration."""
    # Ensure the directory for the log file exists (within backend)
    log_dir = os.path.dirname(log_file_path)
    if not os.path.exists(log_dir):
        try:
            os.makedirs(log_dir)
        except Exception as e:
            # Log to console if file logging setup fails
            print(f"CRITICAL: Failed to create log directory {log_dir}: {str(e)}")
            # Fallback to basic console logging if file setup fails
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
            logging.error("Logging directory creation failed, using console logging.")
            return # Exit setup if directory fails

    # Configure file logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename=log_file_path,
        filemode='a' # Append to the log file
    )
    # Optional: Add a handler to also print logs to console
    # console_handler = logging.StreamHandler()
    # console_handler.setLevel(logging.INFO)
    # formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    # console_handler.setFormatter(formatter)
    # logging.getLogger().addHandler(console_handler)

# --- Core Functions ---

def check_initial_chatlog_existence(path_to_check):
    """
    Checks if the chatlog file exists at the specified path at the start
    and logs the result.
    """
    if os.path.exists(path_to_check):
        logging.info(f"Initial check: ChatLog file found at {path_to_check}")
    else:
        logging.info(f"Initial check: ChatLog file NOT found at {path_to_check}")

def manage_chatlog():
    """
    Manages the chatlog.json file:
    1. Checks if today's date is different from the last session
    2. If different, backs up the old chatlog to a dated folder
    3. Creates a new empty chatlog.json file
    """
    setup_logging() # Setup logging first
    logging.info("--- Starting Chatlog Manager ---")
    logging.info(f"Project Directory: {PROJECT_DIR}")
    logging.info(f"Script Directory: {SCRIPT_DIR}")
    logging.info(f"Chatlog Path: {chatlog_path}")
    logging.info(f"Archives Path: {archives_dir}")
    logging.info(f"Tracking File Path: {date_tracking_file}")
    logging.info(f"Log File Path: {log_file_path}")


    # --- Perform the initial check for the chatlog file ---
    check_initial_chatlog_existence(chatlog_path)

    # Ensure the directory for the chatlog exists (PROJECT_DIR/Data)
    if not os.path.exists(chatlog_dir):
        try:
            os.makedirs(chatlog_dir)
            logging.info(f"Created chatlog directory at {chatlog_dir}")
        except Exception as e:
            logging.error(f"Failed to create chatlog directory {chatlog_dir}: {str(e)}")
            logging.critical("Cannot proceed without chatlog directory. Exiting.")
            return # Exit if we can't create the essential directory

    # Ensure archives directory exists (PROJECT_DIR/chatlog_archives)
    if not os.path.exists(archives_dir):
        try:
            os.makedirs(archives_dir)
            logging.info(f"Created archives directory at {archives_dir}")
        except Exception as e:
            # Log error but maybe continue? Archiving might just fail.
            logging.error(f"Failed to create archives directory {archives_dir}: {str(e)}")

    current_date = datetime.now().strftime('%Y-%m-%d')

    last_date = None
    if os.path.exists(date_tracking_file):
        try:
            with open(date_tracking_file, 'r') as f:
                last_date = f.read().strip()
                # Basic validation: check if it looks like a date YYYY-MM-DD
                datetime.strptime(last_date, '%Y-%m-%d')
        except (ValueError, Exception) as e:
            logging.warning(f"Failed to read or parse date tracking file {date_tracking_file}: {str(e)}. Treating as missing.")
            last_date = None # Treat invalid date as missing

    if last_date and current_date != last_date:
        # Date has changed, attempt to archive the old chatlog
        logging.info(f"Date changed from {last_date} to {current_date}. Archiving old chatlog.")
        backup_chatlog(chatlog_path, archives_dir, last_date)
        create_new_chatlog(chatlog_path)
        logging.info("Created new chatlog for the current date.")
    elif not last_date:
        # First run, tracking file missing, or tracking file unreadable/invalid
        logging.info("No valid last session date found (first run or issue with tracking file).")
        if os.path.exists(chatlog_path):
            # If chatlog exists but no tracking file, archive it with a generic date
            logging.warning(f"Existing chatlog found at {chatlog_path} without a valid last session date. Archiving.")
            backup_chatlog(chatlog_path, archives_dir, f"unknown_date_backup_{current_date}") # Include current date in backup folder name
            create_new_chatlog(chatlog_path)
            logging.info("Created new chatlog after archiving.")
        else:
            # No chatlog exists either, create a new one
            logging.info(f"No existing chatlog found at {chatlog_path}. Creating new one.")
            create_new_chatlog(chatlog_path)
    else:
        # Same date as last session
        logging.info(f"Same date as last session ({current_date}). Checking if chatlog exists.")
        # Ensure chatlog file exists even if date hasn't changed (e.g., if deleted manually)
        if not os.path.exists(chatlog_path):
            logging.warning(f"Chatlog file missing at {chatlog_path} despite date being current. Creating new one.")
            create_new_chatlog(chatlog_path)
        else:
            logging.info(f"Using existing chatlog at {chatlog_path}.")

    # Update the tracking file with current date
    try:
        with open(date_tracking_file, 'w') as f:
            f.write(current_date)
        logging.info(f"Updated tracking file {date_tracking_file} with current date: {current_date}")
    except Exception as e:
        logging.error(f"Failed to write to date tracking file {date_tracking_file}: {str(e)}")

    logging.info("--- Chatlog Manager Finished ---")


def backup_chatlog(source_path, archive_base_dir, date_str):
    """Backs up the existing chatlog to a dated folder within the archives directory."""
    if not os.path.exists(source_path):
        # This is a key message indicating the file wasn't found for backup
        logging.warning(f"ARCHIVE SKIPPED: No chatlog file found at {source_path} to archive for date {date_str}.")
        return

    # Create date-specific directory inside the main archives directory
    date_dir = os.path.join(archive_base_dir, date_str)
    if not os.path.exists(date_dir):
        try:
            os.makedirs(date_dir)
            logging.info(f"Created archive subdirectory: {date_dir}")
        except Exception as e:
             logging.error(f"Failed to create archive directory {date_dir}: {str(e)}")
             return # Cannot proceed with backup if directory creation fails

    # Define the backup file path
    backup_path = os.path.join(date_dir, CHATLOG_FILENAME) # Use original filename

    # Handle case where backup file already exists (e.g., script run multiple times after date change before midnight)
    if os.path.exists(backup_path):
        timestamp = datetime.now().strftime("%H%M%S")
        base, ext = os.path.splitext(CHATLOG_FILENAME)
        backup_path = os.path.join(date_dir, f"{base}_{timestamp}{ext}")
        logging.warning(f"Backup file already exists for {date_str}. Saving new backup as {backup_path}")

    # Copy the file, preserving metadata
    try:
        shutil.copy2(source_path, backup_path)
        # This message confirms the file *was* found and backed up
        logging.info(f"Successfully backed up chatlog from {source_path} to {backup_path}")
    except Exception as e:
        logging.error(f"Failed to backup chatlog from {source_path} to {backup_path}: {str(e)}")

def create_new_chatlog(path_to_create):
    """Creates a new empty chatlog json file (or overwrites existing)."""
    parent_dir = os.path.dirname(path_to_create)
    # Ensure the parent directory exists before trying to write the file
    if not os.path.exists(parent_dir):
        try:
            os.makedirs(parent_dir)
            logging.info(f"Created directory {parent_dir} before creating chatlog file.")
        except Exception as e:
            logging.error(f"Failed to create directory {parent_dir} for new chatlog: {str(e)}")
            return # Cannot create file if directory fails

    try:
        with open(path_to_create, 'w') as f:
            json.dump([], f, indent=4) # Add indent for readability if opened manually
        # This message confirms a new file was created (or overwritten)
        logging.info(f"Created/Reset chatlog file at {path_to_create}")
    except Exception as e:
        logging.error(f"Failed to create new chatlog at {path_to_create}: {str(e)}")

# --- Main Execution Guard ---
if __name__ == "__main__":
    # This allows the script to be run directly for testing or execution
    print(f"Running chatlog manager...")
    # Call setup_logging here as well in case it's run directly
    # and manage_chatlog isn't called, or if manage_chatlog exits early.
    setup_logging()
    print(f"Logging to: {log_file_path}")
    manage_chatlog()
    print("Chatlog manager finished.")

