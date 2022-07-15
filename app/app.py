import pathlib
import winsound
from datetime import datetime
from logging import Logger
from time import sleep

import yaml

from app.api import AlertApiReader
from app.config import Config
from app.settings import AppSetting

from .utils import NtServiceManager


class AlertApp:
    def __init__(self, cfg: Config, alert_api: AlertApiReader, logger: Logger):
        self.cfg = cfg
        self.alert_api = alert_api
        self.logger = logger

    def __export_regions(self):
        if not pathlib.Path(AppSetting.REGIONS_FILENAME).is_file():
            with open(AppSetting.REGIONS_FILENAME, "w") as f:
                yaml.dump(
                    self.alert_api.regions(),
                    stream=f,
                    sort_keys=False,
                    default_style=False,
                    allow_unicode=True,
                )

            if pathlib.Path(AppSetting.REGIONS_FILENAME).is_file():
                self.logger.info(f"File {AppSetting.REGIONS_FILENAME} created")

    def __play_alert_start(self):
        winsound.PlaySound(
            f"resources/{self.cfg.start_alert_filename}", winsound.SND_ALIAS
        )

    def __play_alert_finish(self):
        winsound.PlaySound(
            f"resources/{self.cfg.finish_alert_filename}", winsound.SND_ALIAS
        )

    def run(self):
        self.logger.info("Start application")
        self.__export_regions()
        alert_flag = False
        alert_count = 0
        test_alert_count = 0
        status = False

        nt_service = NtServiceManager(cfg=self.cfg, logger=self.logger)

        while True:
            try:
                if (
                    self.cfg.start_alerting
                    <= datetime.now().time()
                    <= self.cfg.finish_alerting
                ):
                    if self.cfg.region_id == 0:
                        if test_alert_count % 30 == 0:
                            status = not status
                        test_alert_count += 1
                    else:
                        status = self.alert_api.status

                    if status:
                        if alert_flag != status:
                            nt_service.stop_service(
                                service_name=self.cfg.voice_service_name
                            )
                        if alert_count % 10 == 0:
                            self.logger.info("Start air alert notification")
                            self.__play_alert_start()
                            alert_flag = True
                        alert_count += 1
                    else:
                        if alert_count != 0:
                            self.logger.info("Finish  air alert notification")
                            self.__play_alert_finish()
                            alert_count = 0
                            nt_service.start_service(
                                service_name=self.cfg.voice_service_name
                            )
                            alert_flag = False

                else:
                    if alert_count != 0:
                        alert_count = 0
                        nt_service.start_service(
                            service_name=self.cfg.voice_service_name
                        )
                        alert_flag = False

                sleep(self.cfg.delay)

            except ConnectionError as e:
                self.logger.error(f"Got network Exception.\n Details - {e}")
                sleep(self.cfg.recovery_timeout)
            except Exception as e:
                self.logger.error(f"Got Exception.\n Details - {e}")
                sleep(self.cfg.recovery_timeout)
