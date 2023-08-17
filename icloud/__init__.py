from izBasar.secret import ICLOUD_USERNAME, ICLOUD_PASSWORD
from lib import icloud

iService = icloud.IcloudService(ICLOUD_USERNAME, ICLOUD_PASSWORD, True)