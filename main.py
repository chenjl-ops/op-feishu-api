from fastapi import FastAPI, Query
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

from rBase.tools import *
from rBase.feishu_main import *
from rBase.models import *

import uvicorn

app_name = "op-feishu"
app = FastAPI(
    title="op-feishu",
    description="基于飞书接口服务",
    version="0.1.0",
)

origins = [
    "http://192.168.47.107:8085",
    "http://op-feishu-api.dev.k8s.chj.cloud",
    "http://op-feishu-api.prod-devops.k8s.chj.cloud",
    "http://op-feishu-robot-api.dev.k8s.chj.cloud",
    "http://op-feishu-robot-api.prod-devops.k8s.chj.cloud",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app_id="cli_9fe681baedff100e" 
app_secret="M67a77yl97BT3JkwboZ0UfgOTMi1PTtW"

log_config = uvicorn.config.LOGGING_CONFIG
log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
log_config["formatters"]["default"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"


@app.get("/v1/users/", summary="获取用户信息(企业应用open_id和user_id)", tags=["FeishuUser"])
def get_feishu_users_info(usernames: str, app_id: str=app_id, app_secret: str=app_secret):
    url = "https://open.feishu.cn/open-apis/user/v1/batch_get_id?"
    s = "&".join(["emails=%s@lixiang.com"%x for x in usernames.split(",")])
    return feishu_requests_main("get", url+s, app_id=app_id, app_secret=app_secret)

@app.get("/v1/users/open_ids/", summary="获取用户信息(通过open_id)", tags=["FeishuUser"])
def get_feishu_users_info_by_open_ids(open_ids: str, app_id: str=app_id, app_secret: str=app_secret):
    url = "https://open.feishu.cn/open-apis/contact/v1/user/batch_get?"
    s = "&".join(["open_ids=%s"%x for x in open_ids.split(",")])
    return feishu_requests_main("get", url+s, app_id=app_id, app_secret=app_secret)


@app.post("/v1/message/send/", summary="发送消息(普通消息,图片消息)", tags=["FeishuMessage"])
def feishu_send_message(request_data: Message, app_id: str=app_id, app_secret: str=app_secret, is_batch: bool=False):
    if is_batch:
        url = "https://open.feishu.cn/open-apis/message/v4/batch_send/"
    else:
        url = "https://open.feishu.cn/open-apis/message/v4/send/"

    request_data = request_data.dict()
    message_type = request_data.get("message_type")

    data = {
           "content":{
            }
        }

    #查看是否存在回复id
    if request_data.get("root_id"):
        data["root_id"] = request_data.get("root_id")

    if request_data.get("chat_id"):
        data["chat_id"] = request_data.get("chat_id")
    elif request_data.get("open_id"):
        data["open_id"] = request_data.get("open_id")
    elif request_data.get("chat_ids"):
        data["chat_ids"] = request_data.get("chat_ids")
    elif request_data.get("open_ids"):
        data["open_ids"] = request_data.get("open_ids")
    else:
        return {"code": 400, "message": "[open_id|chat_id|open_ids|chat_ids] not all none"}

    if message_type == "image":
        data["msg_type"] = message_type
        image_data = feishu_upload_image(request_data.get("content"))
        if image_data.get("code", "") == 0:
            data["content"]["image_key"] = image_data.get("data", dict()).get("image_key", "")

    elif message_type == "text":
        data["msg_type"] = message_type
        data["content"]["text"] = request_data.get("content")
        if request_data.get("at_open_id"):
            s = "".join(["<at user_id=\"{at_open_id}\"></at>".format(at_open_id=i) for i in request_data.get("at_open_id").split(",")])
            data["content"]["text"] = s + data["content"]["text"]
    else:
        return {"code": 400, "message": "消息类型不支持 [text|image]"}

    return feishu_requests_main("post", url, data, app_id, app_secret)


@app.post("/v1/message/send/post/", summary="发送消息(富文本)", tags=["FeishuMessage"])
def feishu_send_message_post(request_data: MessagePost, app_id: str=app_id, app_secret: str=app_secret):
    url = "https://open.feishu.cn/open-apis/message/v4/send/"
    request_data = request_data.dict()

    data = {
            "msg_type": "post", 
            "content":{
            }
        }

    #查看是否存在回复id
    if request_data.get("root_id"):
        data["root_id"] = request_data.get("root_id")

    if request_data.get("chat_id"):
        data["chat_id"] = request_data.get("chat_id")
    elif request_data.get("open_id"):
        data["open_id"] = request_data.get("open_id")
    else:
        return {"code": 400, "message": "[open_id|chat_id] not all none"}

    contents = request_data.get("content")
    for x in contents:
        for y in x:
            if y.get("tag") == "img": #图片类型数据需要上传
                image_data = feishu_upload_image(y.get("image_url"))
                if image_data.get("code", "") == 0:
                    y["image_key"] = image_data.get("data", dict()).get("image_key", "")

    data["content"]["zh_cn"] = {
                                "title": request_data.get("title"),
                                "content": contents 
                            }
    
    return feishu_requests_main("post", url, data, app_id, app_secret)

@app.get("/v1/message/read_info/", summary="获取消息已读状态", tags=["FeishuMessage"])
def feishu_get_message_readinfo(message_id: str, app_id: str=app_id, app_secret: str=app_secret):
    url = "https://open.feishu.cn/open-apis/message/v4/read_info/"
    data = {"message_id": message_id}
    return feishu_requests_main("post", url, data, app_id, app_secret)


@app.post("/v1/message/send/chat/", summary="发送消息(群名片)", tags=["FeishuMessage"])
def feishu_send_message_chat(request_data: MessageChat, app_id: str=app_id, app_secret: str=app_secret):
    url = "https://open.feishu.cn/open-apis/message/v4/send/"
    request_data = request_data.dict()

    data = {
            "msg_type": "share_chat",
            "content":{
            }
        }

    #查看是否存在回复id
    if request_data.get("root_id"):
        data["root_id"] = request_data.get("root_id")

    if request_data.get("chat_id"):
        data["chat_id"] = request_data.get("chat_id")
    elif request_data.get("open_id"):
        data["open_id"] = request_data.get("open_id")
    elif request_data.get("chat_ids"):
        data["chat_ids"] = request_data.get("chat_ids")
    elif request_data.get("open_ids"):
        data["open_ids"] = request_data.get("open_ids")
    else:
        return {"code": 400, "message": "[open_id|chat_id] not all none"}

    data.update(request_data)
    return feishu_requests_main("post", url, data, app_id, app_secret)

@app.post("/v1/message/send/card/", summary="发送消息(卡片)", tags=["FeishuMessage"])
def feishu_send_message_card(request_data: MessageCard, app_id: str=app_id, app_secret: str=app_secret, is_batch: bool=False):
    import copy

    if is_batch:
        url = "https://open.feishu.cn/open-apis/message/v4/batch_send/"
    else:
        url = "https://open.feishu.cn/open-apis/message/v4/send/"
    request_data = request_data.dict()

    data = {
            "msg_type": "interactive",
            "card": {}
        }

    #查看是否存在回复id
    if request_data.get("root_id"):
        data["root_id"] = request_data.get("root_id")

    if request_data.get("chat_id"):
        data["chat_id"] = request_data.get("chat_id")
    elif request_data.get("open_id"):
        data["open_id"] = request_data.get("open_id")
    elif request_data.get("chat_ids"):
        data["chat_ids"] = request_data.get("chat_ids")
    elif request_data.get("open_ids"):
        data["open_ids"] = request_data.get("open_ids")
    else:
        return {"code": 400, "message": "[open_id|chat_id] not all none"}

    #处理card数据config字段
    data["card"]["config"] = request_data.get("config")

    #处理card数据header字段
    data["card"]["header"] = {
                    "title": {
                        "tag": "plain_txt",
                        "content": request_data.get("header").get("title")
                    },
                    "template": request_data.get("header").get("template")
                }

    #TODO 需要处理card数据字段
    elements = list()
    for x in request_data.get("card", dict()).get("elements"):
        if x.get("tag") == "div": #普通文本
            elements += feishu_card_div(x.get("title", ""), x.get("field"))

        if x.get("tag") == "hr": #分隔符
            elements.append({"tag": x.get("tag")})

        if x.get("tag") == "img": #图片类型
            elements += feishu_card_img(x.get("title"), x.get("images"))

        if x.get("tag") == "note": #备注类型
            pass

        if x.get("tag") == "action": #交互类型
            elements += feishu_card_action(x.get("actions"))

        if x.get("tag") == "markdown": #markdown 类型
            elements.append(feishu_card_markdown(x.get("content")))

    data["card"]["elements"] = elements
    print("card_data:", data)

    return feishu_requests_main("post", url, data, app_id, app_secret)


@app.post("/v1/group/create/", summary="创建群", tags=["FeishuGroup"])
def feishu_create_group(request_data: CreateGroup, app_id: str=app_id, app_secret: str=app_secret):
    request_data = request_data.dict()

    url = "https://open.feishu.cn/open-apis/chat/v4/create/"

    data = {
            "name": request_data.get("name"),
            "description": request_data.get("description"),
            "user_ids": [
            ],
            "open_ids": request_data.get("open_ids"),
            "only_owner_add": request_data.get("only_owner_add"),
            "share_allowed": request_data.get("share_allowed"),
            "only_owner_at_all": request_data.get("only_owner_at_all"),
            "only_owner_edit": request_data.get("only_owner_edit")
        }

    return feishu_requests_main("post", url, data, app_id, app_secret)


@app.get("/v1/group/list/", summary="获取群列表", tags=["FeishuGroup"])
def feishu_get_group_list(page_size: int=100, page_token: str="", app_id: str=app_id, app_secret: str=app_secret):
    url = "https://open.feishu.cn/open-apis/chat/v4/list"

    url = url + "?page_size=%s"%page_size
    if page_token:
        url = url + "&page_token=%s"%page_token
        
    return  feishu_requests_main("get", url, dict(), app_id, app_secret)


@app.get("/v1/group/members/", summary="获取群成员列表", tags=["FeishuGroup"])
def feishu_get_group_members_list(chat_id: str, page_size: int=100, page_token: str="", app_id: str=app_id, app_secret: str=app_secret):
    url = "https://open.feishu.cn/open-apis/chat/v4/members"
    
    url = url + "?page_size=%s"%page_size
    if page_token:
        url = url + "&page_token=%s"%page_token

    return  feishu_requests_main("get", url, dict(), app_id, app_secret)


@app.get("/v1/group/info/", summary="获取群信息", tags=["FeishuGroup"])
def feishu_get_group_info(chat_id: str, app_id: str=app_id, app_secret: str=app_secret):
    url = "https://open.feishu.cn/open-apis/chat/v4/info"

    return feishu_requests_main("get", url + "?chat_id=%s"%chat_id, dict(), app_id, app_secret)


@app.post("/v1/group/update/", summary="更新群信息", tags=["FeishuGroup"])
def feishu_update_group_info(request_data: UpdateGroup, app_id: str=app_id, app_secret: str=app_secret):
    url = "https://open.feishu.cn/open-apis/chat/v4/update/"

    request_data = request_data.dict()
    data = {
            "chat_id": request_data.get("chat_id")
        }

    if request_data.get("name"):
        data["name"] = request_data.get("name")
    if request_data.get("owner_open_id"):
        data["owner_open_id"] = request_data.get("owner_open_id")
    if request_data.get("only_owner_add"):
        data["only_owner_add"] = request_data.get("only_owner_add")
    if request_data.get("share_allowed"):
        data["share_allowed"] = request_data.get("share_allowed")
    if request_data.get("only_owner_at_all"):
        data["only_owner_at_all"] = request_data.get("only_owner_at_all")
    if request_data.get("only_owner_edit"):
        data["only_owner_edit"] = request_data.get("only_owner_edit")

    return feishu_requests_main("post", url, data, app_id, app_secret)

@app.post("/v1/group/member/add/", summary="拉用户进飞书群", tags=["FeishuGroup"])
def add_member_feishu_group(request_data: AddMember, app_id: str=app_id, app_secret: str=app_secret):
    url = "https://open.feishu.cn/open-apis/chat/v4/chatter/add/"
    request_data = request_data.dict()
    
    data = {
            "chat_id": request_data.get("chat_id"),
            "open_ids": request_data.get("open_ids")
        }

    return feishu_requests_main("post", url, data, app_id, app_secret)

@app.post("/v1/group/member/delete/", summary="移除群用户", tags=["FeishuGroup"])
def del_member_feishu_group(request_data: AddMember, app_id: str=app_id, app_secret: str=app_secret):
    url = "https://open.feishu.cn/open-apis/chat/v4/chatter/delete/"
    request_data = request_data.dict()

    data = {
            "chat_id": request_data.get("chat_id"),
            "open_ids": request_data.get("open_ids")
        }

    return feishu_requests_main("post", url, data, app_id, app_secret)

@app.post("/v1/group/disband/", summary="解散飞书群", tags=["FeishuGroup"])
def feishu_disband_group(chat_id: str, app_id: str=app_id, app_secret: str=app_secret):
    url = "https://open.feishu.cn/open-apis/chat/v4/disband"
    data = {"chat_id": chat_id}
    return feishu_requests_main("post", url, data, app_id, app_secret)


@app.get("/v1/messages/", summary="获取聊天信息", tags=["FeishuMessage"])
def feishu_message(message_id: str, page_token: str="", page_size: int=50, star_time: str="0", end_time: str="0", message_type: str="chat", app_id: str=app_id, app_secret: str=app_secret):
    host = "https://open.feishu.cn"
    path = "/open-apis/im/v1/messages"

    query = "?container_id_type={message_type}&container_id={message_id}&star_time={star_time}&end_time={end_time}&page_size={page_size}&page_token={page_token}".format(message_type=message_type, message_id=message_id, star_time=star_time, end_time=end_time, page_size=page_size, page_token=page_token)

    print(host+path+query)

    return feishu_requests_main("get", host+path+query, dict(), app_id, app_secret)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='FastApi Run Server Args')
    parser.add_argument('--port', type=int)
    args = parser.parse_args()
    port = args.port
    uvicorn.run(app, log_config=log_config, port=port, host="0.0.0.0")
