from typing import Union, Optional, List

from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field, validator, root_validator
from nonebot import get_plugin_config, get_bot, get_driver
from nonebot.log import logger
from nonebot.drivers import ReverseDriver
from nonebot.plugin import PluginMetadata

from .config import Config


__plugin_meta__ = PluginMetadata(
    name='适配录播姬webhook的b站开播提醒（forked from nonebot-plugin-report）',
    description='实现几乎实时的开播提醒',
    usage='详见项目 README.md', 

    type="application",

    homepage="https://github.com/A-nemon-e/nonebot-plugin-brecreport"

    
)

driver = get_driver()
config = get_plugin_config(Config)

if not isinstance(driver, ReverseDriver) or not isinstance(driver.server_app, FastAPI):
    raise NotImplementedError('Only FastAPI reverse driver is supported.')


ID = Union[str, int]

class EventData(BaseModel):
    RoomId: int
    ShortId: int
    Name: str
    Title: str
    AreaNameParent: str
    AreaNameChild: str

class Report(BaseModel):
    # token: Optional[str] = Field(None, exclude=True)
    # title: str = Field(..., alias="EventType")  
    EventType: str
    EventTimestamp: str
    EventData: EventData
    # send_from: Optional[ID] = None
    #send_to_group: Optional[List[ID]] = None

    @root_validator(pre=True)
    def check_event_type(cls, values):
        # 只处理 EventType 为 "StreamStarted" 的请求
        # if values.get("EventType") != "StreamStarted":
        #     raise ValueError(status_code=200, detail="EventType is not StreamStarted, request discarded.")
    
        # # 获取 RoomId 和 ShortId
        # event_data = values.get("EventData", {})
        # room_id = str(event_data.get("RoomId"))
        # short_id = str(event_data.get("ShortId"))
    
        # # 获取 config 中的 brec_report_roomids 列表
        # allowed_room_ids = config.brec_report_roomids
    
        # # 如果 allowed_room_ids 列表为空，则允许继续处理
        # if allowed_room_ids:
        #     if room_id not in allowed_room_ids and short_id not in allowed_room_ids:
        #         raise ValueError(status_code=200, detail="RoomId or ShortId is not in the allowed list, request discarded.")
        
        return values

    # # 处理 send_to_group 确保它是列表
    # def _validate(cls, v):
    #     if v is None or isinstance(v, list):
    #         return v
    #     else:
    #         return [v]

    # _v_stg = validator('send_to_group', pre=True, allow_reuse=True)(_validate)



app = FastAPI()

@app.post(config.brec_report_route, status_code=200)
async def push(r: Report):
    # if config.report_token is not None \
    # and r.token != config.report_token:
    #     raise HTTPException(status.HTTP_403_FORBIDDEN)
    if r.EventType != "StreamStarted":
        return

    allowed_room_ids = config.brec_report_roomids
    
        # 如果 allowed_room_ids 列表为空，则允许继续处理
    if allowed_room_ids:
        if r.EventData.RoomId not in allowed_room_ids and r.EventData.ShortId not in allowed_room_ids:
            return
    
    msg = config.brec_report_template.format(
        # title=r.title or '',
        # content=r.content
        Name=r.EventData.Name,
        Title=r.EventData.Title,
        AreaNameParent=r.EventData.AreaNameParent,
        AreaNameChild=r.EventData.AreaNameChild,
        RoomId=r.EventData.RoomId
    )
    try:
        # bot = get_bot(r.send_from or config.report_from)
        bot = get_bot(config.brec_report_from)
    except KeyError:
        logger.warning(f'No bot with specific id: {config.brec_report_from}')
        return
    except ValueError:
        logger.warning('No bot available or driver not initialized')
        return

    # if r.send_to is None:
    #     if r.send_to_group is None:
    #         uids = config.superusers
    #     else:
    #         uids = []
    # else:
    #     uids = r.send_to

    # for uid in uids:
    #     await bot.send_msg(user_id=uid, message=msg, message_type='private')

    if config.brec_report_send_to_group is None:
        gids = []
    else:
        gids = config.brec_report_send_to_group

    for gid in gids:
        await bot.send_msg(group_id=gid, message=msg, message_type='group')

    logger.info(
        f'BrecReport pushed: {r.json()}'
    )


@driver.on_startup
async def startup():
    # if not config.report_token and config.environment == 'prod':
    #     logger.warning('You are in production environment without setting a token')

    driver.server_app.mount('/', app)
    logger.info(f'Mounted to {config.brec_report_route}')
