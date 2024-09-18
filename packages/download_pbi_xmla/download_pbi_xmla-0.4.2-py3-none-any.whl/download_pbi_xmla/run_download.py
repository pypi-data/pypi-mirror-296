#run_download.py
from dotenv import load_dotenv
import os
from pathlib import Path
from download_pbi_xmla.main import main as download_main

def main():
    # Get the current working directory
    current_dir = Path.cwd()

    # Explicitly load the .env file from the current working directory
    load_dotenv(dotenv_path=current_dir / '.env')

    # Verify environment variables
    required_vars = ['CLIENT_ID', 'CLIENT_SECRET', 'TENANT_ID', 'CONFIG_FILE', 'SAVE_PATH']
    for var in required_vars:
        if not os.getenv(var):
            print(f"Error: {var} is not set in the .env file.")
            return

    # Run the download script
    download_main()

if __name__ == "__main__":
    main()
