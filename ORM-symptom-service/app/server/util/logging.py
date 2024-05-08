import logging
from datetime import datetime

# Create a logger object
logger = logging.getLogger('my_logger')
logger.setLevel(logging.INFO)  # Set the minimum log level

# Create file handler which logs even debug messages

fh = logging.FileHandler(f"logs/{datetime.now().strftime("%Y-%m-%d-%H:%M:%S")}.log", mode='w')
fh.setLevel(logging.INFO)  # Set the level for the file handler

# Create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(fh)

# Inital message
logger.info("Starting the application.")
