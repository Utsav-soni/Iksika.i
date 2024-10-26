# Importing libraries
import logging
from logging.handlers import RotatingFileHandler

# Configure the logger
LOG_FILE = 'logs/app.log'

logger = logging.getLogger("vision_app")
logger.setLevel(logging.DEBUG)

# File handler with rotation
handler = RotatingFileHandler(LOG_FILE, maxBytes=1000000, backupCount=3)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Stream handler for debugging
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
