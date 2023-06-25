import logging
import os
import colorlog


LOG_DIR = 'logs'  # Specify the directory for log files
LOG_FILE = 'logfile.log'  # Specify the log file name
LOG_PATH = os.path.join(LOG_DIR, LOG_FILE)  # Join the directory and file name to create the log file path




class Logger:
   def __init__(self):
      # Configure the logging settings
      logging.basicConfig(
         level=logging.DEBUG,
         format='%(asctime)s [%(levelname)s] %(message)s',
         datefmt='%Y-%m-%d %H:%M:%S'
      )

      # Create a file logger directory if it does not exist
      self.CreateLoggerDirectory()

      # Create a file handler and set its level
      file_handler = logging.FileHandler(LOG_PATH)
      file_handler.setLevel(logging.DEBUG)
      file_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S'))

      # Get the logger and add the file handler
      self.logger = logging.getLogger('')
      self.logger.addHandler(file_handler)
      

   def CreateLoggerDirectory(self):
      """Create the directory for the log file if it does not exist.
      """
      if not os.path.exists(LOG_DIR):
         os.mkdir(LOG_DIR)
            
      
   def debug(self, message):
      self.logger.debug(message)


   def info(self, message):
      self.logger.info(message)


   def warning(self, message):
      self.logger.warning(message)


   def error(self, message):
      self.logger.error(message)


   def critical(self, message):
      self.logger.critical(message)
      
      
