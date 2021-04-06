from pydantic import BaseModel
from typing import List, Optional, Set

'''
主要设置 request_data models配置
'''

#飞书消息通用数据结构
class BaseMessageModel(BaseModel):
    root_id: str=""
    chat_id: str=""
    open_id: str=""
    open_ids: list=None
    chat_ids: list=None

#普通消息, 图片消息 body体数据结构
class Message(BaseMessageModel):
    message_type: str
    content: str
    at_open_id: str=""


class PostMessage(BaseModel):
    tag: str
    text: Optional[str] = None
    href: Optional[str] = None
    user_id: Optional[str] = None
    image_path: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None

#富文本消息 body体数据结构
class MessagePost(BaseMessageModel):
    # chat_id  open_id user_id email 任意一个 不能同时为空
    title: str
    content: Optional[List[PostMessage]]

class ChatMessage(BaseModel):
    share_chat_id: str

#群名片
class MessageChat(BaseMessageModel):
    content: Optional[ChatMessage]

#卡片消息
class CardConfig(BaseModel):
    wide_screen_mode: bool=True
    enable_forward: bool=True

#卡片标题
class CardTitle(BaseModel):
    title: str
    template: str="blue"

#卡片内容是普通文本
class CardContentField(BaseModel):
    is_short: Optional[bool]=False
    text: Optional[str]=None

#卡片内容是图片数据
class CardContentImg(BaseModel):
    image_url: Optional[str]
    text: Optional[str]

#卡片内容是交互模块数据
class CardAction(BaseModel):
    tag: Optional[str]
    text: Optional[dict] = None
    type: Optional[str] = None
    options: Optional[list] = None
    initial_option: Optional[str] = None
    initial_date: Optional[str] = None
    placeholder: Optional[dict] = None


#卡片内容
class CardContent(BaseModel):
    tag: str
    content: str
    text: Optional[str] = None
    field: Optional[List[CardContentField]] = None
    title: Optional[str] = None
    images: Optional[List[CardContentImg]] = None
    actions: Optional[List[CardAction]] = None
    other: Optional[dict] = None

#卡片消息
class CardCard(BaseModel):
    elements: Optional[List[CardContent]]

#消息卡片
class MessageCard(BaseMessageModel):
    config: Optional[CardConfig]
    header: Optional[CardTitle]
    card: Optional[CardCard]

#创建群组
class CreateGroup(BaseModel):
    name: str
    description: str
    open_ids: list
    only_owner_add: bool=False
    share_allowed: bool=True
    only_owner_at_all: bool=False
    only_owner_edit:bool=False

#update群组数据
class UpdateGroup(BaseModel):
    chat_id: str
    owner_open_id: str=""
    name: str=""
    only_owner_add: bool=False
    share_allowed: bool=True
    only_owner_at_all: bool=False
    only_owner_edit:bool=False

#新增用户
class AddMember(BaseModel):
    chat_id: str
    open_ids: list

#对应用接口数据模型
class OpenApiData(BaseModel):
    action: Optional[str]
    is_markdown: Optional[bool] = False
    app_id: Optional[str] = None
    app_name: Optional[str] = None
    group_id: Optional[str] = None
    user_ids: Optional[str] = None
    message: Optional[str] = None
    callback_url: Optional[str] = None
    root_id: Optional[str] = None

#注册使用罗伯特平台
class RobotApp(BaseModel):
    feishu_app_id: Optional[str]
    feishu_app_secret: Optional[str]
    feishu_token: Optional[str]
    app_name: Optional[str]
    owner: Optional[str]
    description: Optional[str]

