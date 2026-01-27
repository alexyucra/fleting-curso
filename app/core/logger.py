
import logging
import sys
import os
from pathlib import Path

APP_NAME = "fleting"

def is_frozen():
    return getattr(sys, "frozen", False)

def is_android():
    return sys.platform == "android"

def get_log_dir():
    # ANDROID (APK)
    if is_android():
        return Path(os.getcwd()) / "files" / "logs"

    # EXECUTABLE (PyInstaller)
    if is_frozen():
        base = Path(os.getenv("LOCALAPPDATA", Path.home()))
        return base / APP_NAME / "logs"

    # DESENVOLVIMENTO
    return Path.cwd() / "logs"

LOG_DIR = get_log_dir()
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "fleting.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

def get_logger(name: str):
    return logging.getLogger(name)
