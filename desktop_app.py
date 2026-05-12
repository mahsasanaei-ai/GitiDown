# desktop_app.py - Main application 
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
import threading
import uuid
import json
import socket

class GitHubWebhookClient:
    def __init__(self, root):
        self.root = root
        self.root.title("🐙 Telegram to GitHub Downloader")
        self.root.geometry("750x600")
       
        # Configuration 
        self.github_repo = "YOUR_USERNAME/YOUR_REPO"
        self.github_token = "YOUR_GITHUB_TOKEN"  # Get from environment variable
        self.webhook_url = "https://abc123.ngrok.io/webhook"  # Your ngrok URL
       
        # Create UI elements
        self.create_widgets()
       
    def create_widgets(self):
        # URL input
        tk.Label(self.root, text="🔗 Telegram or Direct URL:", font=("Arial", 10, "bold")).pack(pady=5)
        self.url_entry = tk.Entry(self.root, width=80, font=("Arial", 10))
        self.url_entry.pack(pady=5, padx=20, fill=tk.X)
       
        # Optional password
        tk.Label(self.root, text="🔐 Archive password (optional):").pack(pady=5)
        self.password_entry = tk.Entry(self.root, width=30, show="*")
        self.password_entry.pack(pady=5)
       
        # Start button
        self.start_btn = tk.Button(self.root, text="🚀 Start GitHub Download",
                                   command=self.start_download,
                                   bg="#2ea44f", fg="white", font=("Arial", 12, "bold"))
        self.start_btn.pack(pady=15)
       
        # Progress bar
        self.progress = ttk.Progressbar(self.root, mode='indeterminate')
        self.progress.pack(fill=tk.X, padx=20, pady=5)
       
        # Log display
        tk.Label(self.root, text="📋 Operation Log:", font=("Arial", 10, "bold")).pack(anchor=tk.W, padx=20)
        self.log_text = scrolledtext.ScrolledText(self.root, height=20, font=("Courier", 9))
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
       
    def log(self, message, color="black"):
        """Add message to log display"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update()
       
    def trigger_github_download(self, file_url, password, run_id, callback_url):
        """Send request to GitHub Action via repository_dispatch"""
        url = f"https://api.github.com/repos/{self.github_repo}/dispatches"
       
        headers = {
            "Authorization": f"Bearer {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
       
        payload = {
            "event_type": "download-request",
            "client_payload": {
                "url": file_url,
                "password": password,
                "run_id": run_id,
                "callback_url": callback_url
            }
        }
       
        response = requests.post(url, json=payload, headers=headers)
        return response.status_code == 204
   
    def convert_telegram_url(self, telegram_url):
        """Convert Telegram URL to direct download link"""
        # TODO: Implement actual Telegram URL conversion
        # Method 1: Use Telegram Bot API
        # Method 2: Use public services like tgdrive
        # Method 3: Use pyrogram library
       
        self.log("🔄 Converting Telegram link...")
        # Placeholder - replace with actual conversion logic
        time.sleep(2)
        direct_url = telegram_url.replace("t.me", "direct.example.com")
        return direct_url
   
    def start_download(self):
        """Main process"""
        url = self.url_entry.get().strip()
        password = self.password_entry.get().strip()
       
        if not url:
            messagebox.showerror("Error", "Please enter a URL")
            return
       
        # Disable button during processing
        self.start_btn.config(state=tk.DISABLED)
        self.progress.start()
       
        def worker():
            try:
                run_id = str(uuid.uuid4())[:8]
               
                # Get callback URL 
                callback_url = self.webhook_url
               
                self.log(f"📤 Sending request to GitHub... (ID: {run_id})")
               
                # Step 1: Convert Telegram URL
                if "t.me" in url or "telegram" in url:
                    url = self.convert_telegram_url(url)
                    self.log(f"✅ Converted URL: {url}")
               
                # Step 2: Send to GitHub
                success = self.trigger_github_download(url, password, run_id, callback_url)
               
                if success:
                    self.log("✅ Request sent to GitHub successfully")
                    self.log("⏳ GitHub will start downloading...")
                    self.log(f"🔍 Check status: https://github.com/{self.github_repo}/actions")
                    self.log("📥 File will be automatically downloaded to your system when complete")
                else:
                    self.log("❌ Failed to send request to GitHub")
                   
            except Exception as e:
                self.log(f"❌ Error: {str(e)}")
            finally:
                self.progress.stop()
                self.start_btn.config(state=tk.NORMAL)
       
        # Run in separate thread to keep UI responsive
        threading.Thread(target=worker, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = GitHubWebhookClient(root)
    root.mainloop()