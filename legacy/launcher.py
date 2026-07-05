import subprocess
import sys
import time
import webbrowser


import requests

API_URL = "http://127.0.0.1:8000/"
FRONTEND_URL = "http://localhost:8501"

print("Starting FastAPI...")

backend = subprocess.Popen(
    [
        sys.executable,
        "-m",
        "uvicorn",
        "api.main:app",
        "--host",
        "127.0.0.1",
        "--port",
        "8000"
    ]
)

print("Waiting for API...")

while True:

    if backend.poll() is not None:
        raise RuntimeError("FastAPI failed to start.")

    try:
        r = requests.get(API_URL, timeout=1)

        if r.status_code == 200:
            break

    except requests.RequestException:
        pass

    time.sleep(1)

print("API Ready")

print("Starting Streamlit...")

frontend = subprocess.Popen(
    [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        "frontend/app.py",
        "--server.headless",
        "true"
    ]
)

print("Waiting for Streamlit...")

while True:

    try:

        r = requests.get(
            FRONTEND_URL,
            timeout=1
        )

        if r.status_code == 200:
            break

    except requests.RequestException:
        pass

    time.sleep(0.5)

webbrowser.open(FRONTEND_URL)

print("Application Ready")
try:

    while True:

        if backend.poll() is not None:
            break

        if frontend.poll() is not None:
            break

        time.sleep(1)

except KeyboardInterrupt:
    pass

finally:

    print("Closing application...")

    backend.terminate()
    frontend.terminate()

    try:
        backend.wait(timeout=5)
    except subprocess.TimeoutExpired:
        backend.kill()

    try:
        frontend.wait(timeout=5)
    except subprocess.TimeoutExpired:
        frontend.kill()