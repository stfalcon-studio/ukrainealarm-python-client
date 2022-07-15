import os
from logging import Logger
from typing import Optional

from app.config import Config


class NrServiceException(Exception):
    pass


class NtServiceManager:
    def __init__(self, cfg: Config, logger: Logger):
        self.cfg = cfg
        self.logger = logger

    def __start_service(self, service_name: str) -> bool:
        try:
            res = os.system(f"net start {service_name}")
            if res == 2:
                raise NrServiceException
            self.logger.info(f"Try start {service_name}. Status - {res}")
            return True
        except NrServiceException:
            self.logger.error(f"Error starting service {service_name}")
            return False

    def __stop_service(self, service_name: str) -> bool:
        try:

            res = os.system(f"net stop {service_name}")
            if res == 2:
                raise NrServiceException
            self.logger.info(f"Try stop {service_name}. Status - {res}")
            return True
        except NrServiceException as e:
            self.logger.error(f"Error stopping service {service_name}")
            return False

    def start_service(self, service_name: Optional[str]) -> bool:
        if not self.cfg.stop_voice_service_mode:
            return True

        if not service_name:
            service_name = self.cfg.voice_service_name
        return self.__start_service(service_name=service_name)

    def stop_service(self, service_name: Optional[str]) -> bool:
        if not self.cfg.stop_voice_service_mode:
            return True

        if not service_name:
            service_name = self.cfg.voice_service_name
        return self.__stop_service(service_name=service_name)
