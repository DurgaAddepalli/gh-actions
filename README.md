# **DevOps Automation Scripts**

This repository contains a collection of production-ready automation scripts designed to streamline common DevOps tasks. Each script is well-documented, secure, and built to be easily modified for different environments.

## **Table of Contents**

1. [**Task 1: Remote File Copy Utility via SSH**](https://www.google.com/search?q=%23task-1-remote-file-copy-utility-via-ssh)  
   * [Purpose](https://www.google.com/search?q=%23purpose)  
   * [Prerequisites](https://www.google.com/search?q=%23prerequisites)  
   * [Usage](https://www.google.com/search?q=%23usage)  
   * [Security Best Practices](https://www.google.com/search?q=%23security-best-practices)  
2. **Task 2: GitHub Actions PR Merged Notifier**  
   * [Purpose](https://www.google.com/search?q=%23purpose-1)  
   * [How It Works](https://www.google.com/search?q=%23how-it-works)  
   * [Setup and Configuration](https://www.google.com/search?q=%23setup-and-configuration)  
3. **CI/CD Integration Example**  
   * [Combining Both Scripts for Automated Deployments](https://www.google.com/search?q=%23combining-both-scripts-for-automated-deployments)

## **Task 1: Remote File Copy Utility via SSH**

A Python script (remote\_copy\_if\_needed.py) to connect to a remote server, ensure a directory exists, and upload a local file to it securely using SSH.

### **Purpose**

This script automates the deployment task of copying build artifacts, configuration files, or other assets to a remote server. It safely handles the creation of remote directories before uploading, preventing script failures caused by missing paths on the server.

### **Prerequisites**

* Python 3.6 or higher.  
* The paramiko Python library must be installed:  
  pip install paramiko

* SSH access to the target remote server.

### **Usage**

Run the script from your terminal, providing the remote server connection details and the file paths as arguments.

python remote\_copy\_if\_needed.py \\  
  \--host \<IP\_OR\_HOSTNAME\> \\  
  \--user \<USERNAME\> \\  
  \--password \<PASSWORD\> \\  
  \<path-to-local-source-file\> \\  
  \<absolute-path-to-remote-target-directory\>

**Example:**

To copy a local file named config.json to the /opt/app/configs directory on a server at 192.168.1.100:

\# Create a dummy file locally for the example  
echo '{"setting": "new\_value"}' \> ./config.json

\# Run the script to upload it  
python remote\_copy\_if\_needed.py \\  
  \--host 192.168.1.100 \\  
  \--user deploy-user \\  
  \--password "YourSecurePassword" \\  
  ./config.json \\  
  /opt/app/configs

### **Security Best Practices**

Passing a password as a command-line argument is convenient for testing but is **not** recommended for production **environments**. For better security, you should use **SSH key-based authentication**. This involves modifying the script to connect using a private key file instead of a password.

## **Task 2: GitHub Actions PR Merged Notifier**

A GitHub Actions workflow (.github/workflows/pr-merged-notify.yml) that automatically sends an email notification when a pull request is **successfully merged** into a protected branch like develop or main.

### **Purpose**

This workflow provides immediate, automated communication to stakeholders (like developers, QA teams, or project managers) that new code has been successfully integrated. This is a key signal for triggering subsequent actions like testing, documentation updates, or deployments.

### **How It Works**

The workflow is configured to trigger only when a pull request is closed. It then uses a conditional check (if: ... && github.event.pull\_request.merged \== true) to ensure it only proceeds if the pull request's final state was "merged".

### **Setup and Configuration**

To enable this workflow, you must configure the following secrets in your GitHub repository under **Settings** \> **Secrets** and **variables** \> **Actions**:

| Secret Key | Description | Example Value |
| :---- | :---- | :---- |
| SMTP\_SERVER | The hostname of your email server. | smtp.gmail.com |
| SMTP\_PORT | The port for your email server (TLS/STARTTLS). | 587 |
| SMTP\_USERNAME | The username for authentication. | your-email@gmail.com |
| SMTP\_PASSWORD | An **app-specific password** for the account. | abdcivqoxnfhplmg |
| EMAIL\_FROM | The address the email will appear to be from. | GitHub Actions \<ci@your-domain.com\> |
| EMAIL\_TO | The recipient's email address. | dev-team-leads@your-domain.com |

## **CI/CD Integration Example**

### **Combining Both Scripts for Automated Deployments**

These two scripts can be combined to create a simple, yet powerful, continuous deployment pipeline. When a PR is merged, the GitHub Action can trigger the Python script to deploy a file to your server.

Here is a conceptual example of how you could add a deployment step to your GitHub Action workflow:

\# Inside .github/workflows/pr-merged-notify.yml

\# ... (previous steps for sending email)

      \- name: 'Deploy Configuration File'  
        if: success() \# Only run if the email step succeeded  
        run: |  
          \# Install Python dependencies  
          pip install paramiko  
            
          \# Run the deployment script  
          python remote\_copy\_if\_needed.py \\  
            \--host ${{ secrets.DEPLOY\_SERVER\_HOST }} \\  
            \--user ${{ secrets.DEPLOY\_SERVER\_USER }} \\  
            \--password ${{ secrets.DEPLOY\_SERVER\_PASSWORD }} \\  
            ./path/to/your/app.conf \\  
            /etc/production/configs/

In this scenario, you would add new secrets (DEPLOY\_SERVER\_HOST, etc.) to your repository for the deployment target. This setup ensures that every merged PR automatically and reliably deploys the latest configuration to your production environment.
