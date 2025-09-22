"""
Startup script to run both Streamlit app and FastAPI server.

This script allows you to start both the web interface and API server
with a single command.
"""

import subprocess
import sys
import time
import threading
import os

def run_streamlit():
    """Run the Streamlit application."""
    print("Starting Streamlit app on http://localhost:8501")
    subprocess.run([sys.executable, "-m", "streamlit", "run", "main.py", "--server.port", "8501"])

def run_fastapi():
    """Run the FastAPI server."""
    print("Starting FastAPI server on http://localhost:8000")
    subprocess.run([sys.executable, "-m", "uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])

def main():
    """Start both servers."""
    print("=== RAG DevKaluri Server Startup ===")
    print("Starting both Streamlit app and FastAPI server...")
    print()
    
    # Start FastAPI server in a separate thread
    api_thread = threading.Thread(target=run_fastapi, daemon=True)
    api_thread.start()
    
    # Give the API server a moment to start
    time.sleep(2)
    
    # Start Streamlit app in the main thread
    try:
        run_streamlit()
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        sys.exit(0)

if __name__ == "__main__":
    main()
