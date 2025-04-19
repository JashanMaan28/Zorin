import os
import json
import shutil
from datetime import datetime
import logging

def manage_chatlog():
    """
    Manages the chatlog.json file:
    1. Checks if today's date is different from the last session
    2. If different, backs up the old chatlog to a dated folder
    3. Creates a new empty chatlog.json file
    """
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename='chatlog_manager.log'
    )
    
    # Define paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    chatlog_path = os.path.join(base_dir, 'Data/chatlog.json')
    date_tracking_file = os.path.join(base_dir, '.last_session_date')
    archives_dir = os.path.join(base_dir, 'chatlog_archives')
    
    # Ensure archives directory exists
    if not os.path.exists(archives_dir):
        os.makedirs(archives_dir)
        logging.info(f"Created archives directory at {archives_dir}")
    
    # Get current date
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    # Check if we have a tracking file
    if os.path.exists(date_tracking_file):
        with open(date_tracking_file, 'r') as f:
            last_date = f.read().strip()
        
        if current_date != last_date:
            # Date has changed, archive the old chatlog
            backup_chatlog(chatlog_path, archives_dir, last_date)
            create_new_chatlog(chatlog_path)
            logging.info(f"Date changed from {last_date} to {current_date}. Archived old chatlog and created new one.")
        else:
            logging.info(f"Same date as last session ({current_date}). Using existing chatlog.")
    else:
        # First run or tracking file was deleted
        if os.path.exists(chatlog_path):
            # If chatlog exists but no tracking file, assume it's from a previous date
            backup_chatlog(chatlog_path, archives_dir, "unknown_date")
            create_new_chatlog(chatlog_path)
            logging.info("No date tracking file found. Archived existing chatlog and created new one.")
        else:
            # No chatlog exists either, create a new one
            create_new_chatlog(chatlog_path)
            logging.info("First run. Created new chatlog.")
    
    # Update the tracking file with current date
    with open(date_tracking_file, 'w') as f:
        f.write(current_date)
    
    logging.info(f"Updated tracking file with current date: {current_date}")

def backup_chatlog(chatlog_path, archives_dir, date):
    """Backs up the existing chatlog to a dated folder"""
    if not os.path.exists(chatlog_path):
        logging.warning(f"No chatlog file found at {chatlog_path} to archive.")
        return
    
    # Create date-specific directory
    date_dir = os.path.join(archives_dir, date)
    if not os.path.exists(date_dir):
        os.makedirs(date_dir)
    
    # Copy the file
    backup_path = os.path.join(date_dir, 'chatlog.json')
    try:
        shutil.copy2(chatlog_path, backup_path)
        logging.info(f"Successfully backed up chatlog to {backup_path}")
    except Exception as e:
        logging.error(f"Failed to backup chatlog: {str(e)}")

def create_new_chatlog(chatlog_path):
    """Creates a new empty chatlog.json file"""
    try:
        with open(chatlog_path, 'w') as f:
            json.dump([], f)
        logging.info(f"Created new empty chatlog at {chatlog_path}")
    except Exception as e:
        logging.error(f"Failed to create new chatlog: {str(e)}")

if __name__ == "__main__":
    # This allows the script to be run directly for testing
    manage_chatlog()