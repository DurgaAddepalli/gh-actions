# **DevOps Automation Scripts**

This repository contains a collection of production-ready automation scripts designed to streamline common DevOps tasks. Each script is well-documented and built to be easily modified.

## **Table of Contents**

1. [Task 1: Python File Copy Utility (copy\_if\_needed.py)](https://www.google.com/search?q=%23task-1-python-file-copy-utility-copy_if_neededpy)  
   * [Purpose](https://www.google.com/search?q=%23purpose)  
   * [Prerequisites](https://www.google.com/search?q=%23prerequisites)  
   * [Usage](https://www.google.com/search?q=%23usage)  
   * [How It Works](https://www.google.com/search?q=%23how-it-works)  
2. [Task 2: GitHub Actions PR Merged Notifier](https://www.google.com/search?q=%23task-2-github-actions-pr-merged-notifier)  
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

## **Task 2: GitHub Actions PR Merged Notifier**

A GitHub Actions workflow (.github/workflows/pr-merged-notify.yml) that automatically sends an email notification when a pull request is **successfully merged** into a specific branch.

### **Purpose**

This workflow keeps stakeholders informed about successfully integrated code changes. It provides a clear signal that a feature or fix has been incorporated into a key branch like develop or main, which is crucial for coordinating testing, deployment, or further development efforts.

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

* **Change the Monitored Branch**: To monitor a branch other than develop (e.g., main), edit the if condition in the .github/workflows/pr-merged-notify.yml file:  
  \# From  
  if: github.base\_ref \== 'develop' && github.event.pull\_request.merged \== true  
  \# To  
  if: github.base\_ref \== 'main' && github.event.pull\_request.merged \== true

* **Update the Recipient Email**: To change who receives the notification, simply update the EMAIL\_TO secret in your repository settings. No code changes are required.  
* **Modify Email Content**: The email body is defined as HTML within the workflow file. You can edit the html\_body section to add or remove information. All PR details are available through the github.event.pull\_request context object.
