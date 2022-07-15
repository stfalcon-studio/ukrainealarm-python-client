import datetime
import pathlib
import random
from typing import Optional, Union

import yaml
from pydantic import BaseModel, validator
from yaml import SafeLoader

from app.exceptions import ConfigurationError
from app.settings import AppSetting


class Config(BaseModel):
    api_key: str
    url: str
    time_delay: int = 60
    use_time_delay_delta: bool = True
    recovery_timeout: int = 60
    period_replaying: int = 600
    log: str = "log.txt"
    log_level: str = "INFO"
    log_size_bytes: int = 5000000
    log_backup_count: int = 5
    region_id: int = 14
    store_name: Optional[str] = None
    local_cert_name: Optional[str] = None
    use_local: bool = False
    voice_service_name: Optional[str] = None
    stop_voice_service_mode: bool = False

    start_alerting: datetime.time
    finish_alerting: datetime.time

    start_alert_filename: str
    finish_alert_filename: str

    @validator("log_level")
    def time_delta_check(cls, v):
        if v not in ["INFO", "DEBUG", "WARN", "CRITICAL"]:
            raise ValueError(
                "Error in config file. Log level must be one from [INFO, DEBUG, WARN, CRITICAL]"
            )

        return v

    @property
    def delay(self):
        # дельта нужна для снижения количества одновременнх запросов по ключу,
        # запросы к АПИ будут по задержке +- 30%
        delta = 0
        if self.use_time_delay_delta:
            delta = self.time_delay * 30 // 100

        return self.time_delay + random.choice([-1, 1]) * random.randint(0, delta)


def load_config(config_file: Union[pathlib.Path, str] = None) -> Config:
    if not config_file:
        config_file = pathlib.Path(f"./{AppSetting.CONFIG_FILENAME}")

    if isinstance(config_file, str):
        config_file = pathlib.Path(config_file)

    if not config_file.is_file():
        print(f"Cannot open config file {config_file}")

    if config_file.suffix in [".yaml", ".yml"]:
        with open(config_file, "r") as f:
            return Config(**yaml.load(f, Loader=SafeLoader))
    else:
        print(
            f"Only .yaml, .yml are supported. Cannot process file type {config_file.suffix}"
        )
        raise ConfigurationError(
            f"Only .yaml, .yml are supported. Cannot process file type {config_file.suffix}"
        )
