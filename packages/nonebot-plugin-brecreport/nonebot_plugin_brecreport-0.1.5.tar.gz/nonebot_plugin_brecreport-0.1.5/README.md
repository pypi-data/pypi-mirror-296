
 - 这是我的第一个github项目，从[nonebot-plugin-report](https://github.com/syrinka/nonebot-plugin-report)改动而来，请务必多多指教！



# nonebot-plugin-brecreport



## 功能

该插件提供了一个位于 `/brec_report` 的路由，并和[录播姬](https://github.com/BililiveRecorder)适配，实现实现几乎实时的开播提醒 (需要安装[录播姬](https://rec.danmuji.org/))

## 使用

### nonebot2 .env配置

Field | Type | Desc | Default | Note
-- | -- | -- | -- | --
`brec_report_from` | `Optional[ID]` | 推送消息的机器人 ID | | 若不设置，任意获取一个可用的机器人
`brec_report_route` |  `str` | 路由 | `/brec_report` | 若与其它路由冲突可以更换该值
`brec_report_template` | `str` | 消息模板 | `主播{Name}开播了！标题：{Title}\n直播分区：{AreaNameParent}-{AreaNameChild}\nhttps://live.bilibili.com/{RoomId}` | 支持 `{Name}`（主播名）， `{Title}`（直播标题）， `{AreaNameParent}`（主分区）， `{AreaNameChild}`（二级分区）， `{RoomId}`（长房间号） 5个字段
`brec_report_roomids` | `Optional[List[str]]` | 要报告的B站直播间号 | | 长或短号都支持，若不设置，谁开播都不会报告
`brec_report_send_to_group` | `Optional[List[str]]` | 报告的群号 | | 

### 录播姬配置

在[录播姬](https://github.com/BililiveRecorder)的Web界面中设置Webhook V2地址为 `http://127.0.0.1:8080/brec_report` ，如果更改过nonebot2相关设置请对应更改地址。

## 原理

录播姬在监控开播情况时可以发起Webhook（详见https://rec.danmuji.org/reference/webhook/ ），取 `"EventType": "StreamStarted"` 作为直播提醒。

**Note:** 
录播姬中，对某直播房间关闭自动录制后，录播姬仍可发起 `StreamStarted`， `StreamEnded` 两种Webhook。


## Todo

- [ ] 开播封面发送
- [ ] (?)推送给好友
- [ ] (?)支持更多`EventType`

## 致谢
- [nonebot-plugin-report](https://github.com/syrinka/nonebot-plugin-report)~~（从这个抄来的）~~
- nonebot2项目
- ChatGPT
