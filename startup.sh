#!/bin/bash
# 1. Update the OS and install required packages
apt-get update
apt-get install -y python3 python3-pip python3-venv git

# 2. Create a folder for your application
mkdir -p /opt/webapp
cd /opt/webapp

# 3. Clone your code from GitHub 
# IMPORTANT: Replace the URL below with your actual public GitHub repository URL!
git clone https://github.com/sujiv1204/cloud-deploy.git .

# 4. Set up the Python environment
python3 -m venv venv
source venv/bin/activate
pip3 install Flask

# 5. Start the Flask application in the background
nohup python3 app.py > webapp.log 2>&1 &