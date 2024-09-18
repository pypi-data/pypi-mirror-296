# omnimark/utils/utils.py

import logging

def setup_logging():
    """
    Set up logging configuration.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )
def notify_user(message: str):
    """
    Notify the user with a message.

    Args:
        message (str): The message to display.
    """
    print(message)

def log_error(message):
    logging.error(message)

def notify_user(message: str):
    """Notify the user with a message."""
    print(message)  # Or implement a more sophisticated notification system

# Update __all__ to include log_error
__all__ = ['setup_logging', 'log_error', 'notify_user']
