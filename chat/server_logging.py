import logging
import logging.config

logging.config.fileConfig('logging.conf')

# create logger
server_logger = logging.getLogger('serverLogger')
