#!/usr/bin/env python3

import argparse
import os
import sys
import paramiko

def remote_copy_file(
    hostname: str,
    port: int,
    username: str,
    password: str,
    source_file: str,
    target_dir: str
) -> None:
    """
    Connects to a remote server via SSH to ensure a target directory exists
    and copies a local source file into it.

    Args:
        hostname (str): The remote server's hostname or IP address.
        port (int): The SSH port on the remote server.
        username (str): The username for the SSH connection.
        password (str): The password for the SSH connection.
                        (Note: For production, SSH key auth is recommended).
        source_file (str): The path to the LOCAL source file to be copied.
        target_dir (str): The path to the REMOTE destination directory.
    """
    # --- 1. Validate Local Source File ---
    if not os.path.isfile(source_file):
        print(f"❌ Error: Local source file not found at '{source_file}'", file=sys.stderr)
        raise FileNotFoundError(f"Local source file not found: {source_file}")

    ssh_client = None
    try:
        # --- 2. Establish SSH Connection ---
        print(f"🔌 Connecting to {username}@{hostname}:{port}...")
        ssh_client = paramiko.SSHClient()
        # Automatically add the server's host key. For high security,
        # you might want to load from a known_hosts file instead.
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        ssh_client.connect(
            hostname=hostname,
            port=port,
            username=username,
            password=password,
            timeout=10
        )
        print("✅ Connection successful.")

        # --- 3. Open SFTP Session and Check/Create Remote Directory ---
        sftp = ssh_client.open_sftp()
        print(f"Checking for remote directory: '{target_dir}'")
        
        try:
            # Check if the directory exists by trying to access its attributes.
            sftp.stat(target_dir)
            print(f"✅ Remote directory already exists.")
        except FileNotFoundError:
            # If it doesn't exist, create it recursively.
            print(f"📁 Remote directory not found. Creating missing directory...")
            # SFTP doesn't have a built-in 'mkdir -p', so we create each parent dir.
            current_dir = ''
            # Ensure we handle both absolute and relative paths
            dir_parts = target_dir.strip('/').split('/')
            if target_dir.startswith('/'):
                current_dir = '/'
            
            for part in dir_parts:
                # Append the next part of the path
                if not current_dir.endswith('/'):
                    current_dir += '/'
                current_dir += part
                try:
                    sftp.stat(current_dir)
                except FileNotFoundError:
                    print(f"   Creating '{current_dir}'")
                    sftp.mkdir(current_dir)

        # --- 4. Copy the File Remotely ---
        remote_file_path = os.path.join(target_dir, os.path.basename(source_file)).replace("\\", "/")
        print(f"📄 Copying local file '{source_file}' to remote path '{remote_file_path}'...")
        sftp.put(source_file, remote_file_path)
        print("✅ File copied successfully.")
        
        sftp.close()

    except paramiko.AuthenticationException:
        print("❌ Error: Authentication failed. Please check your username and password.", file=sys.stderr)
        sys.exit(1)
    except paramiko.SSHException as e:
        print(f"❌ Error: SSH connection failed. Reason: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        # --- 5. Ensure Connection is Closed ---
        if ssh_client:
            ssh_client.close()
            print("🔌 Connection closed.")

def main():
    """Main function to parse CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Connects to a remote server via SSH to copy a file to a specified directory.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    # SSH Connection Arguments
    parser.add_argument("--host", required=True, help="Remote server hostname or IP.")
    parser.add_argument("--port", type=int, default=22, help="SSH port (default: 22).")
    parser.add_argument("--user", required=True, help="SSH username.")
    parser.add_argument("--password", required=True, help="SSH password.\n(For better security, consider using SSH keys and modifying the script).")
    
    # File Operation Arguments
    parser.add_argument("source_file", help="Path to the LOCAL file to copy.")
    parser.add_argument("target_dir", help="Absolute path to the REMOTE target directory.")
    
    args = parser.parse_args()
    
    remote_copy_file(args.host, args.port, args.user, args.password, args.source_file, args.target_dir)

if __name__ == '__main__':
    main()
