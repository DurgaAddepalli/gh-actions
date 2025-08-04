#!/usr/bin/env python3

import argparse
import pathlib
import shutil
import sys

def copy_file_to_dir(source_file: str, target_dir: str) -> None:
    """
    Ensures a target directory exists and copies a source file into it.

    This function checks for the existence of the source file and the target directory.
    If the target directory does not exist, it creates it, including any necessary
    parent directories. Finally, it copies the source file to the target directory.

    Args:
        source_file (str): The path to the source file to be copied.
        target_dir (str): The path to the destination directory.

    Raises:
        FileNotFoundError: If the source_file does not exist.
    """
    # Use pathlib for robust, cross-platform path handling
    source_path = pathlib.Path(source_file)
    target_path = pathlib.Path(target_dir)

    # --- 1. Validate Source File ---
    # Ensure the source file actually exists before doing anything else.
    if not source_path.is_file():
        # Log error to stderr and exit with a non-zero status code for automation
        print(f"❌ Error: Source file not found at '{source_path}'", file=sys.stderr)
        raise FileNotFoundError(f"Source file not found: {source_path}")

    # --- 2. Check and Create Target Directory ---
    # Check if the target directory already exists.
    if target_path.is_dir():
        print(f"✅ Directory already exists: '{target_path}'")
    else:
        # If it doesn't exist, create it.
        # `parents=True` creates any missing parent folders (like mkdir -p).
        # `exist_ok=True` prevents errors if the dir is created by another process
        # between our check and this command.
        print(f"📁 Target directory not found. Creating missing directory: '{target_path}'")
        target_path.mkdir(parents=True, exist_ok=True)

    # --- 3. Copy the File ---
    # Use shutil.copy to perform the file copy operation.
    # This preserves file metadata and permissions where possible.
    try:
        shutil.copy(source_path, target_path)
        print(f"📄 Copied '{source_path.name}' to '{target_path}'")
    except (IOError, shutil.SameFileError) as e:
        print(f"❌ Error: Failed to copy file. Reason: {e}", file=sys.stderr)
        # Re-raise the exception to halt any automation script that depends on this.
        raise

def main():
    """
    Main function to parse command-line arguments and execute the copy operation.
    """
    # Set up the argument parser for a clean command-line interface.
    parser = argparse.ArgumentParser(
        description="Check/create a target directory and copy a source file into it.",
        epilog="Example: python copy_if_needed.py ./data/report.json ./output/reports/"
    )
    # Define the required command-line arguments.
    parser.add_argument("source_file", help="Path to the source file that needs to be copied.")
    parser.add_argument("target_dir", help="Path to the target directory where the file should be placed.")
    
    args = parser.parse_args()

    try:
        # Execute the core logic.
        copy_file_to_dir(args.source_file, args.target_dir)
    except Exception as e:
        # Catch any exceptions raised from the function to ensure a clean exit.
        # The specific error messages are already printed within the function.
        print(f"\nOperation failed.", file=sys.stderr)
        sys.exit(1) # Exit with an error code

# --- Script Entry Point ---
# This block ensures the `main()` function is called only when the script is
# executed directly from the command line (e.g., `python copy_if_needed.py ...`).
if __name__ == '__main__':
    main()
