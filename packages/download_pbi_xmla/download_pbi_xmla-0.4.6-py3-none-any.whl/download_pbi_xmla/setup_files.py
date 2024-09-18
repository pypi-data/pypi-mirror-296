#setup_files.py
import shutil
import os
from pathlib import Path
import download_pbi_xmla

def copy_example_files():
    # Determine the package directory where example files are stored
    package_dir = Path(download_pbi_xmla.__file__).parent

    # Set the target directory to the current working directory
    target_dir = Path.cwd()

    example_files = {
        '.env_example': '.env',
        'example_config.json': 'config.json'
    }

    for src_name, dst_name in example_files.items():
        src = package_dir / src_name
        dst = target_dir / dst_name

        # Copy files to the user's project folder only if they don't already exist
        if not dst.exists():
            shutil.copy(src, dst)
            print(f"Copied {src} to {dst}")
        else:
            print(f"{dst} already exists")

def main():
    # Step 1: Copy example files to the user's project folder
    copy_example_files()

    # Step 2: Prompt user to edit the configuration files
    print("\nCreated .env and config.json files in the working folder.")
    print("\nPlease edit with your credentials and configuration details.\n")
    input("Press Enter to continue ...")

if __name__ == "__main__":
    main()
