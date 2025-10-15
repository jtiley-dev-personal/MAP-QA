#!/bin/bash
###############################################################################
# 🧠 MAP QA Tool Launcher (macOS)
# Safely launches the Streamlit MAP QA app with self-healing and dependency setup
###############################################################################

# --- SELF-HEALING PERMISSIONS + QUARANTINE FIX ---
chmod +x "$0" 2>/dev/null
xattr -d com.apple.quarantine "$0" 2>/dev/null

echo "───────────────────────────────────────────────"
echo " 🚀  Launching MAP QA Tool (macOS Version)"
echo "───────────────────────────────────────────────"
echo ""

# --- MOVE TO SCRIPT DIRECTORY (important for relative paths) ---
cd "$(dirname "$0")" || {
  echo "❌ Failed to access script directory. Exiting."
  exit 1
}

# --- CHECK PYTHON INSTALLATION ---
if ! command -v python3 &>/dev/null; then
  echo "⚠️  Python 3 not found on this Mac."
  echo "   Please install it via Homebrew:"
  echo "   ➤ brew install python"
  exit 1
fi

# --- VIRTUAL ENVIRONMENT SETUP ---
if [ ! -d "venv" ]; then
  echo "🔧 Creating virtual environment..."
  python3 -m venv venv
  if [ $? -ne 0 ]; then
    echo "❌ Failed to create virtual environment."
    exit 1
  fi
fi

# --- ACTIVATE VENV ---
source venv/bin/activate

# --- INSTALL DEPENDENCIES IF MISSING ---
if [ ! -f "requirements.txt" ]; then
  echo "⚠️  No requirements.txt found. Proceeding without dependency check."
else
  echo "📦 Checking and installing Python dependencies..."
  pip install --upgrade pip >/dev/null 2>&1
  pip install -r requirements.txt >/dev/null 2>&1
fi

# --- LAUNCH STREAMLIT APP ---
if [ ! -f "app.py" ]; then
  echo "❌ app.py not found in the current directory."
  exit 1
fi

echo ""
echo "🌐 Starting Streamlit App... (this may take a few seconds)"
echo ""

# Use nohup to keep the terminal open even if user closes it early
nohup streamlit run app.py >/dev/null 2>&1 &

sleep 3
echo "✅ MAP QA Tool is now running!"
echo "💻 It should open automatically in your default browser."
echo "   If not, visit: http://localhost:8501"
echo ""
echo "───────────────────────────────────────────────"
echo "   To stop the app: close the browser tab or press Ctrl+C in Terminal"
echo "───────────────────────────────────────────────"
echo ""
exit 0
