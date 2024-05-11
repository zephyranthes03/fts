from time import process_time
from app.server.util.logging import logger

def time_logger(func):
    """
    Decorator that logs the processing time of a function.
    """
    def wrapper(*args, **kwargs):
        start_time = process_time()
        result = func(*args, **kwargs)
        end_time = process_time()
        logger.info(f"Processing time of '{func.__name__}': {end_time - start_time:.4f} seconds")
        return result
    return wrapper
