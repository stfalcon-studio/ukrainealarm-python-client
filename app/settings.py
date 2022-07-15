from enum import Enum, unique

from pydantic import BaseModel


@unique
class AppSetting(str, Enum):
    CONFIG_FILENAME = "config.yaml"
    REGIONS_FILENAME = "regions.yaml"
    LOG_FILENAME = "log.txt"
    DEFAULT_LOG_LEVEL = "INFO"
    DEFAULT_LOG_SIZE = 5000000
    DEFAULT_LOG_BACKUP_COUNT = 5
