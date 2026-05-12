from flask import Flask, request
import subprocess
import json
import threading
import time
import os

app = Flask(__name__)

# Path to save downloaded files
DOWNLOAD_PATH = os.path.expanduser("~/Downloads/GitHub_Files")
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

# Dictionary to track download status
download_status = {}

@app.route('/webhook', methods=['POST'])
def github_callback():
    """GitHub calls this webhook when download is complete"""
    data = request.json
    print(f"📨 Received message: {data}")
    
    download_url = data.get('download_url')
    run_id = data.get('run_id')
    filename = data.get('filename')
    
    if download_url:
        # Start download in a separate thread
        threading.Thread(target=download_file, args=(download_url, filename, run_id)).start()
        return {"status": "downloading"}, 200
    
    return {"status": "ok"}, 200

import platform

def download_file(url, filename, run_id):
    """Download file from GitHub to local system"""
    download_status[run_id] = "downloading"
    
    filepath = os.path.join(DOWNLOAD_PATH, filename)
    
    # Download with curl and show progress
    cmd = f'curl -L -o "{filepath}" "{url}" --progress-bar'
    subprocess.run(cmd, shell=True)
    
    # Check file size
    size = os.path.getsize(filepath) / (1024*1024)  # MB
    download_status[run_id] = "completed"
    
    print(f"\n✅ Download complete: {filename} ({size:.2f} MB)")
    print(f"📁 Path: {filepath}")
    
    # Auto-open based on OS
    system = platform.system()
    if system == "Darwin":  # macOS
        subprocess.run(f'open "{filepath}"', shell=True)
    elif system == "Windows":
        subprocess.run(f'start "{filepath}"', shell=True)
    elif system == "Linux":
        subprocess.run(f'xdg-open "{filepath}"', shell=True)

@app.route('/status/<run_id>', methods=['GET'])
def get_status(run_id):
    """Get download status"""
    return {"status": download_status.get(run_id, "unknown")}

if __name__ == '__main__':
    # Get public IP using ngrok
    print("="*50)
    print("🚀 Webhook server started")
    print("To expose to internet, run: ngrok http 5000")
    print("Add ngrok URL to GitHub Secrets")
    print("="*50)
    
    app.run(host='0.0.0.0', port=5000)