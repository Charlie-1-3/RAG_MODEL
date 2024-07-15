import logging
from logging.handlers import TimedRotatingFileHandler
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)
CWD = os.path.abspath(os.getcwd())
logging.basicConfig(level=logging.DEBUG,
                    handlers=[TimedRotatingFileHandler(CWD + "\\logs\\log_file.txt", when="midnight"), logging.StreamHandler()], 
                    format='%(asctime)s - %(levelname)s - %(message)s')
