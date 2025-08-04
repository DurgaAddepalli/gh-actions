# **DevOps Automation Scripts**

This repository contains a collection of production-ready automation scripts designed to streamline common DevOps tasks. Each script is well-documented and built to be easily modified.

## **Table of Contents**

1. [Task](https://www.google.com/search?q=%23task-1-python-file-copy-utility-copy_if_neededpy) 1: Python File Copy Utility (copy\_if\_needed.py)  
   * [Purpose](https://www.google.com/search?q=%23purpose)  
   * [Prerequisites](https://www.google.com/search?q=%23prerequisites)  
   * [Usage](https://www.google.com/search?q=%23usage)  
   * [How It Works](https://www.google.com/search?q=%23how-it-works)  
2. [Task 2: GitHub Actions PR Email Notifier](https://www.google.com/search?q=%23task-2-github-actions-pr-email-notifier)  
   * [Purpose](https://www.google.com/search?q=%23purpose-1)  
   * [Setup and Configuration](https://www.google.com/search?q=%23setup-and-configuration)  
   * [How to Customize](https://www.google.com/search?q=%23how-to-customize)

## **Task 1: Python File Copy Utility (copy\_if\_needed.py)**

A robust, cross-platform Python script to safely copy a file to a target directory, creating the directory if it doesn't exist.

### **Purpose**

This script automates the common workflow of ensuring a destination directory exists before copying a file into it. It prevents errors in build pipelines or deployment scripts that might fail if a directory is missing.

### **Prerequisites**

* Python 3.6 or higher.  
* No external libraries are needed; the script uses only standard Python libraries (pathlib, shutil, argparse).

### **Usage**

Run the script from your terminal, providing the source file and target directory as command-line arguments.

python copy\_if\_needed.py \<path-to-source-file\> \<path-to-target-directory\>

**Example:**

\# Create a dummy file for the example  
mkdir \-p ./data  
echo '{"status": "ok"}' \> ./data/report.json

\# Run the script  
python copy\_if\_needed.py ./data/report.json ./output/reports/

**Expected Output:**

📁 Target directory not found. Creating missing directory: 'output/reports'  
📄 Copied 'report.json' to 'output/reports'

If you run it again, the output will be:

✅ Directory already exists: 'output/reports'  
📄 Copied 'report.json' to 'output/reports'

### **How It Works**

1. **Argument Parsing**: It uses argparse to accept two required arguments: source\_file and target\_dir.  
2. **Source File Validation**: It first checks if the source\_file actually exists. If not, it prints an error and exits.  
3. **Directory Check**: It uses pathlib.Path to check if the target\_dir exists and is a directory.  
4. **Directory Creation**: If the directory is missing, it creates it using pathlib.Path.mkdir(parents=True, exist\_ok=True). The parents=True flag ensures that all parent folders in the path are also created (similar to the mkdir \-p command in Linux).  
5. **File Copy**: Finally, it uses shutil.copy() to copy the file from the source to the target destination.

## **Task 2: GitHub Actions PR Email Notifier**

A GitHub Actions workflow (.github/workflows/pr-notify.yml) that automatically sends an email notification when a pull request is opened against a specific branch.

### **Purpose**

This workflow keeps stakeholders informed about new development work in real-time. It's particularly useful for private repositories where team leads, QA engineers, or project managers need immediate notification of pending changes.

### **Setup and Configuration**

To enable this workflow, you must configure secrets in your GitHub repository.

1. Navigate to your repository's **Settings** \> **Secrets and variables** \> **Actions**.  
2. Click **New repository secret** for each of the following entries:

| Secret Key | Description | Example Value |
| :---- | :---- | :---- |
| SMTP\_SERVER | The hostname of your email server. | smtp.gmail.com |
| SMTP\_PORT | The port for your email server (TLS/STARTTLS). | 587 |
| SMTP\_USERNAME | The username for authentication. | your-email@gmail.com |
| SMTP\_PASSWORD | An **app-specific password** for the account. | abdcivqoxnfhplmg |
| EMAIL\_FROM | The address the email will appear to be from. | GitHub Actions \<ci@your-domain.com\> |
| EMAIL\_TO | The recipient's email address. | dev-team-leads@your-domain.com |

**Note on SMTP\_PASSWORD**: For services like Gmail, you cannot use your regular account password. You must generate an "App Password" and use that here.

### **How to Customize**

* **Change the Monitored Branch**: To monitor a branch other than develop (e.g., main), edit the if condition in the .github/workflows/pr-notify.yml file:  
  \# From  
  if: github.base\_ref \== 'develop'  
  \# To  
  if: github.base\_ref \== 'main'

* **Update the Recipient Email**: To change who receives the notification, simply update the EMAIL\_TO secret in your repository settings. No code changes are required.  
* **Modify** Email **Content**: The email body is defined as HTML within the workflow file. You can edit the html\_body section to add or remove information. All PR details are available through the github.event.pull\_request context object.
