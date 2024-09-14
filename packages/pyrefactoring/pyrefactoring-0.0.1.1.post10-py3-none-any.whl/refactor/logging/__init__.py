import os
import logging
from logging import *
from .stdout import add_stdout_handler, add_file_handler

# Set root log level from env.
root = logging.getLogger()
root.setLevel(os.getenv('LOG_LEVEL', logging.DEBUG))
# Log to stdout.
add_stdout_handler()
# Log to file?
if os.getenv('LOG_FILE', False):
  add_file_handler()
