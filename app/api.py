from logging import Logger
from typing import Dict, List, Optional

import requests

from app.config import Config
from app.models import AlertRespond


class AlertApiReader:
    def __init__(self, cfg: Config, logger: Logger):
        self.cfg = cfg
        self.logger = logger

    def __request(self, url: str) -> dict:
        headers = dict(accept="application/json", Authorization=self.cfg.api_key)
        if self.cfg.use_local:
            res = requests.get(f"{url}", headers=headers)
        else:
            res = requests.get(
                f"{url}", headers=headers, verify=f"certs/{self.cfg.local_cert_name}"
            )

        self.logger.debug(
            f"Api request status - {res.status_code}. \n Response data: {res.json()}"
        )

        if res.status_code == 200:
            self.logger.info(
                self.logger.error(f"Api request status - {res.status_code}.")
            )
            return res.json()
        elif res.status_code == 401:
            self.logger.error(
                f"Api request status - {res.status_code}. Reason - {res.reason}"
            )
        elif res.status_code == 500:
            self.logger.error(
                f"Api request status - {res.status_code}. Reason - {res.reason}"
            )
        else:
            self.logger.error(
                f"Api request status - {res.status_code}. Reason - {res.reason}"
            )

    def get_all(self) -> List[Optional[AlertRespond]]:
        url = f"{self.cfg.url}/alerts"
        return [AlertRespond(**i) for i in self.__request(url=url)]

    def get_by_region_id(self) -> AlertRespond:
        url = f"{self.cfg.url}/alerts/{self.cfg.region_id}"
        data = self.__request(url=url)
        return AlertRespond(**data[0])

    def regions(self) -> Dict:
        url = f"{self.cfg.url}/regions"
        return self.__request(url=url)

    @property
    def status(self) -> bool:
        return bool(self.get_by_region_id().activeAlerts)
