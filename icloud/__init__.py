import logging

from izBasar.secret import ICLOUD_USERNAME, ICLOUD_PASSWORD
from lib import icloud

iService = icloud.IcloudService(ICLOUD_USERNAME, ICLOUD_PASSWORD, True)
logging.info("这是一个INFO信息")
logging.debug("这是一个调试信息")