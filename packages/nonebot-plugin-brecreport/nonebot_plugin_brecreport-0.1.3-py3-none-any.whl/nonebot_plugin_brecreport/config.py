from typing import Optional, List, Union
from pydantic import BaseModel, Extra


ID = Union[str, int]

class Config(BaseModel, extra=Extra.ignore):
    # report_token: Optional[str] = None
    brec_report_from: Optional[ID] = None
    brec_report_route: str = '/brec_report'
    brec_report_template: str = '主播{Name}开播了！标题：{Title}\n直播分区：{AreaNameParent}-{AreaNameChild}\nhttps://live.bilibili.com/{RoomId}'
    # environment: str
    # superusers: List[str]
    brec_report_roomids: Optional[List[str]] = None
    brec_report_send_to_group: Optional[List[str]] = None
