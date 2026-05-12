#!/bin/bash
# setup.sh - Auto setup script for Linux/macOS

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📥 Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo "⚠️ ngrok is not installed!"
    echo "Download from: https://ngrok.com/download"
    echo "Or install with: brew install ngrok (macOS)"
else
    echo "✅ ngrok found"
fi

# Create config file template
echo "=========================================="


if [ ! -f "config.json" ]; then
    cat > config.json << EOF
{
    "github_repo": "YOUR_USERNAME/YOUR_REPO",
    "github_token": "YOUR_GITHUB_TOKEN_HERE",
    "webhook_url": "https://YOUR_NGROK_URL.ngrok.io/webhook",
    "download_path": "~/Downloads/GitHub_Files"
}
EOF
    echo "✅ Created config.json template"
    echo "⚠️ Please edit config.json with your real values!"
else
    echo "✅ config.json already exists"
fi

# Create download directory
DOWNLOAD_DIR="${HOME}/Downloads/GitHub_Files"
mkdir -p "$DOWNLOAD_DIR"
echo "✅ Created download directory: $DOWNLOAD_DIR"

echo "Setup complete!"

echo ""
echo "Next steps:"
echo "1. Edit config.json with your GitHub token"
echo "2. Run: ngrok http 5000"
echo "3. In another terminal: source venv/bin/activate && python webhook_receiver.py"
echo "4. Run: python desktop_app.py"
echo ""