import sympy as sp
from sympy import sstr
import logging
from io import StringIO
import os
from pathlib import Path

class SympyPrettyPrintHandler(logging.StreamHandler):
    def emit(self, record):
        try:
            msg = self.format(record)
            if isinstance(record.msg, sp.Basic):
                # Use sstr for SymPy expressions
                msg = sstr(record.msg)
            elif isinstance(record.args, tuple) and any(isinstance(arg, sp.Basic) for arg in record.args):
                # Handle mixed messages with SymPy expressions
                formatted_msg = record.msg % record.args
                output = StringIO()
                for arg in record.args:
                    if isinstance(arg, sp.Basic):
                        output.write(sstr(arg))
                    else:
                        output.write(str(arg))
                msg = formatted_msg.replace('%s', output.getvalue())
            stream = self.stream
            stream.write(msg + self.terminator)
            self.flush()
        except Exception:
            self.handleError(record)

def configure_logging(logger_name='PyCAMPSLogger', log_file='app.log', log_to_console=True, log_to_file=False):
    """
    Configures the logging settings for the application.

    This function sets up the logging configuration for the application. It allows you to log messages to the console,
    a file, or both. The log level can be controlled via the `LOG_LEVEL` environment variable.

    Args:
        logger_name (str): The name of the logger. Default is 'PyCAMPSLogger'.
        log_file (str): The name of the log file. Default is 'app.log'.
        log_to_console (bool): If True, logs will be printed to the console. Default is True.
        log_to_file (bool): If True, logs will be saved to a file. Default is False.

    Environment Variables:
        LOG_LEVEL (str): The log level for the logger. Can be 'DEBUG', 'INFO', 'WARNING', 'ERROR', or 'CRITICAL'.
                         Default is 'INFO'.

    Example:
        >>> configure_logging(log_to_console=True, log_to_file=True)

    Notes:
        - If both `log_to_console` and `log_to_file` are set to False, no logs will be output.
        - The log file will be saved in the user's home directory if `log_to_file` is True.
        - Existing handlers are cleared before adding new ones to avoid duplicate logs.

    """
    logger = logging.getLogger(logger_name)
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()  # Default to INFO if not set
    logger.setLevel(getattr(logging, log_level, logging.INFO))
    
    # Clear existing handlers to avoid duplicate logs
    if logger.hasHandlers():
        logger.handlers.clear()
    
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    
    if log_to_console:
        # Create a console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    if log_to_file:
        # Create a file handler
        if not os.path.exists('results/logs'):
            os.makedirs('results/logs')
        log_file_path = os.path.join('results/logs', log_file)
        file_handler = logging.FileHandler(log_file_path, mode='w')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    logger.propagate = False
    return logger