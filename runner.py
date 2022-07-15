from app.api import AlertApiReader
from app.app import AlertApp
from app.config import load_config
from app.logger import get_logger

if __name__ == "__main__":
    cfg = load_config()
    logger = get_logger(cfg=cfg)
    alert_api = AlertApiReader(cfg=cfg, logger=logger)

    app = AlertApp(cfg=cfg, alert_api=alert_api, logger=logger)
    app.run()
