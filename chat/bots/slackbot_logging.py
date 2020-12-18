import logging
import logging.config

logging.config.fileConfig('logging.conf')

bot_logger = logging.getLogger('botLogger')
