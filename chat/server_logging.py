import logging
import logging.config

logging.config.fileConfig('logging.conf')

server_logger = logging.getLogger('serverLogger')
