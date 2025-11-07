import os
import time
from loguru import logger

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_path = os.path.join(os.getcwd(), "logs")
os.makedirs(log_path, exist_ok=True)
log_path_error = os.path.join(log_path, f"{time.strftime('%Y-%m-%d')}_error.log")
logger.add(log_path_error, rotation="50MB", encoding="utf-8", enqueue=True, compression="zip")
