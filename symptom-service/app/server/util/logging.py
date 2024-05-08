import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# configure the handler and formatter for logger2
handler = logging.FileHandler(f"logs/{__name__}.log", mode='w')
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

# add formatter to the handler
handler.setFormatter(formatter)
# add handler to the logger
logger.addHandler(handler)

logger.info(f"Testing the custom logger for module {__name__}...")
