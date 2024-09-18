# download.py
from download_pbi_xmla.main import fetch_tables
import argparse
import sys
from dotenv import load_dotenv
import os
import logging
import time
from datetime import datetime

# Create a logs directory if it does not exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Set up logging to file with a datestamp
log_filename = datetime.now().strftime("logs/log_%Y%m%d_%H%M%S.log")
logging.basicConfig(filename=log_filename, level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Also set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger().addHandler(console)

# Load environment variables from .env file
load_dotenv()

# Fetch secrets and other settings from environment variables
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
TENANT_ID = os.getenv('TENANT_ID')
CONFIG_FILE = os.getenv('CONFIG_FILE')
SAVE_PATH = os.getenv('SAVE_PATH')

# Ensure required environment variables are set
if not CLIENT_ID:
    logging.error("CLIENT_ID environment variable is not set.")
    sys.exit(1)

if not CLIENT_SECRET:
    logging.error("CLIENT_SECRET environment variable is not set.")
    sys.exit(1)

if not TENANT_ID:
    logging.error("TENANT_ID environment variable is not set.")
    sys.exit(1)

if not CONFIG_FILE:
    logging.error("CONFIG_FILE environment variable is not set.")
    sys.exit(1)

if SAVE_PATH:
    SAVE_PATH = SAVE_PATH.strip()
else:
    SAVE_PATH = ''  # Provide a default value or handle the absence appropriately

# Debug print statements to verify environment variables
logging.debug(f"CLIENT_ID: {CLIENT_ID}")
logging.debug(f"CLIENT_SECRET: {'*' * len(CLIENT_SECRET) if CLIENT_SECRET else None}")
logging.debug(f"TENANT_ID: {TENANT_ID}")
logging.debug(f"Config File: {CONFIG_FILE}")
logging.debug(f"Save Path: {SAVE_PATH}")

def main():
    start_time = time.time()
    
    fetch_tables(
        config_file=CONFIG_FILE,
        path=SAVE_PATH,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        tenant_id=TENANT_ID
    )
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    logging.info(f"Script runtime: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main()