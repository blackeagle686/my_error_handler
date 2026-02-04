
import os
import sys

# Install dependencies if running in Colab and not installed
# (Common pattern in single-file Colab scripts, though usually done in cells)
try:
    import nest_asyncio
    import pyngrok
except ImportError:
    print("Installing dependencies...")
    os.system(f"{sys.executable} -m pip install nest_asyncio pyngrok uvicorn fastapi")
    import nest_asyncio
    from pyngrok import ngrok, conf

import threading
import uvicorn
from app.main import app  # Importing the FastAPI app instance

# Apply nest_asyncio to allow nested event loops in Colab
nest_asyncio.apply()

def start_colab_server(ngrok_token=None):
    """
    Starts the FastAPI server in a background thread and tunnels it via Ngrok.
    """
    # 1. Start FastAPI in background
    def run_app():
        uvicorn.run(app, host="0.0.0.0", port=8000)

    thread = threading.Thread(target=run_app, daemon=True)
    thread.start()

    # 2. Setup Ngrok
    token = ngrok_token or os.getenv("NGROK_AUTH_TOKEN", "YOUR_NGROK_TOKEN_HERE")
    
    if token == "YOUR_NGROK_TOKEN_HERE":
        print("⚠️  WARNING: Ngrok token not set. Tunneling might fail or be restricted.")
    else:
        conf.get_default().auth_token = token

    # 3. Connect Public URL
    try:
        public_url = ngrok.connect(8000).public_url
        print(f"\n🚀 Public URL: {public_url}\n")
        print("Click the link above to access the API/UI.")
    except Exception as e:
        print(f"❌ Ngrok Error: {e}")

if __name__ == "__main__":
    # You can pass the token as an argument or set NGROK_AUTH_TOKEN env var
    # Example: python colab_runner.py <your_token>
    token_arg = sys.argv[1] if len(sys.argv) > 1 else None
    start_colab_server(token_arg)
    
    # Keep main thread alive
    import time
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping server...")
