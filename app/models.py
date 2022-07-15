import datetime
from typing import Any, List, Optional

from pydantic import BaseModel


class AlertRespond(BaseModel):
    activeAlerts: Optional[List[Any]]
    lastUpdate: datetime.datetime
    regionId: int
    regionName: str
    regionType: str
