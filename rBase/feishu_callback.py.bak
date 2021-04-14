#!/usr/bin/env python
# --coding:utf-8--

import json
import requests

from rBase.apollo_config import *
from sql_app.db_play import app_id_retrieve, feishu_token_retrieve

class FeishuCallBack(object):

    def __init__(self, data):
        self.data = data
        self.event = self.data.get("event", dict())

    def get_app_token(self):
        return self.data.get("token", "")

    def get_app_id(self):
        return self.event.get("app_id")

    def get_msg_type(self):
        return self.event.get("msg_type", "")

    def get_chat_type(self):
        return self.event.get("chat_type", "")

    def get_message_id(self):
        return self.event.get("open_message_id", "")

    def get_chat_id(self):
        return self.event.get("chat_id", "")

    def get_open_chat_id(self):
        return self.event.get("open_chat_id", "")

    def get_open_id(self):
        return self.event.get("open_id", "")

    def get_without_message_data(self):
        return self.event.get("text_without_at_bot", "")

    def get_message_data(self):
        return self.event.get("text", "")

    def get_message_list_data(self):
        return self.event.get("msg_list", list())

    def get_merge_forward_message(self, msg_list):
        # 处理合并转发数据
        data = list()
        for msg in msg_list:
            msg_type = msg.get("msg_type")
            open_id = msg.get("open_id")
            user_info = get_user_info(open_id)
            if msg_type == "text":
                data.append("{Time} {User}: {Msg}".format(Time=time_to_str(msg.get("create_time")), User=user_info["nick_name"], Msg=msg.get("text")))
            elif msg_type == "image":
                data.append("{Time} {User}: {Msg}".format(Time=time_to_str(msg.get("create_time")), User=user_info["nick_name"], Msg="![Image](%s)"%msg.get("text")))

        return "\n".join(data)
    
    # 获取合并转发数据里聊天人员，包含发送消息人员 随机人员为 问题人
    def get_merge_forward_user_ids(self, msg_list):
        sponsor_ids = list(set([i.get("open_id", "") for i in msg_list]))
        if len(sponsor_ids) >= 2:
            sponsor_ids.remove(self.get_processing_person_id)
        return sponsor_ids
    
    # 获取发送消息人员id 标识为处理人
    def get_processing_person_id(self):
        return self.event.get("open_id", "")
                
    def get_app_info(self):
        feishu_token = self.get_app_token()
        if feishu_token:
            return feishu_token_retrieve(feishu_token)
        else:
            return dict()


#处理callback主逻辑
def feishu_callback(data):
    feishu_data = FeishuCallBack(data)
    
    # appinfo数据
    app_info = feishu_token_retrieve(feishu_data.get_app_token())
    # 获取会话类型
    chat_type = feishu_data.get_chat_type()
    # 获取会话类型
    msg_type = feishu_data.get_msg_type()
    # 获取去除@机器人数据的message
    message = feishu_data.get_without_message_data()
    # 获取合并转发数据
    msg_list = feishu_data.get_message_list_data()
    forward_message = "  帮忙处理下, 刚才聊天记录如下:\n" + feishu_data.get_merge_forward_message(msg_list)

    # 获取处理人 和 问题人列表
    processing_person_id = feishu_data.get_processing_person_id()
    sponsor_ids = feishu_data.get_merge_forward_user_ids(msg_list)

    if chat_type in ["group", "private"]:
        return feishu_message(app_info, message, msg_type, processing_person_id, sponsor_ids, forward_message)
    else: #其他类型暂时飞书未知
        return {"code": -1, "error_message": "飞书未知类型,暂不支持"}


#处理消息数据逻辑
def feishu_message(app_info, message, msg_type, processing_person_id, sponsor_ids, forward_message=None):
    import datetime

    if msg_type == "text": #文本服务
        data = feishu_rebot_message_auto(message, app_info) 
    elif msg_type == "post": #富文本
        data = feishu_rebot_message_auto(message, app_info)
    elif msg_type == "merge_forward": #合并转发数据
        # 获取所有用户数据
        users = sponsor_ids + [processing_person_id]
        sponsor_id = sponsor_ids[0]
        sponsor_data = get_user_info(sponsor_id)
        processing_person_data = get_user_info(processing_person_id) 
        department_id = sponsor_data.get("department_id", 0)
        sponsor = sponsor_data.get("nick_name")
        processing_person = processing_person_data.get("nick_name")

        # 创群操作
        create_data = cloud_help_create_group("融合云为您服务", ",".join(list(set(users))))
        print(create_data)
        # 获取创群 群id
        group_id = create_data.get("data", dict()).get("chat_id")
        # 创建工单
        create_ticket(group_id, department_id, sponsor, sponsor_id, processing_person, processing_person_id)
        # 修改群名称
        ticket_data = get_ticket(group_id)
        title = "{status}-{name}-{sponsor}-{processing_person}-{group_id}-{date}".format(status=robotStatus[0], \
                        name=ticket_data["desc"], sponsor=ticket_data["sponsor"], group_id=group_id, \
                        processing_person=ticket_data["processing_person"], date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        cloud_help_update_title(title, group_id)
        # 发送合并转发数据 和首次同志修改群名称功能
        for x in [forward_message, robot_help_result_message_notice_change_title]:
            cloud_help_send_msg(group_id, processing_person_id, x, True)
        data = {"code": 0, "message": "合并转发拉群成功"}

    else:
        data = {"code": 0, "message": "暂时不支持数据类型"}

    return data

# 处理自动回复相关数据
def feishu_rebot_message_auto(message, app_info):
    import requests
    from sql_app.db_play import auto_ask_config_retrieve

    app_id = app_info.get("data", dict()).get("app_id")
    app_name = app_info.get("data", dict()).get("app_name")

    message = message.strip() #去除首尾空格
    if message.find(" ") != -1:
        messages = message.split()
        searchKey = messages[0]
        message = messages[0]+" "
        keyword = " ".join(messages[1:])
    else:
        searchKey = message
        keyword = message

    get_auto_ask_data = auto_ask_config_retrieve(message, app_id, app_name)
    #没查到指令 保底查找help信息
    if get_auto_ask_data:
        get_auto_ask_data = auto_ask_config_retrieve("help", app_id, app_name)
        keyword = "help"

    Messages = list()
    if get_auto_ask_data:
        #组装请求url
        if message.find(" ") != -1:
            if keyword == "help":
                QueryString = "username=%s&keyword=%s&messageId=%s&unknownKeyword=%s"%(username, keyword, messageId, " ".join(messages))
            else:
                QueryString = "username=%s&keyword=%s&messageId=%s&unknownKeyword=%s"%(username, message + keyword, messageId, " ".join(messages))
        else:
            QueryString = "username=%s&keyword=%s&messageId=%s&unknownKeyword=%s"%(username, keyword, messageId, message)

        for x in get_auto_ask_data:
            if x.answer_message.strip().startswith("http://") or x.answer_message.strip().startswith("https://"):
                if urlparse(x.answer_message.strip()).query:
                    url = x.answer_message.strip() + "&{query}".format(query=QueryString)
                else:
                    url = x.answer_message.strip() + "?{query}".format(query=QueryString)

                logger.info("URLXXXXXXX: %s"%url)
                try:
                    data = requests.get(url, timeout=5, verify=False)
                    logger.info("dataXXXXXXX: %s"%data.content)
                    if data.status_code == 200 and data.json().get("data", list()):
                        Messages += [{"message": i.get("content"), "isMarkdown": i.get("isMarkdown", False)} for i in data.json().get("data")]
                    elif data.status_code >= 400: #http状态码大于400 为异常错误
                        Messages += [{"message": "指令接口异常, 请联系相关应用负责人 %s "%app_info["data"]["owner"], "isMarkdown": False}]
                        logger.error("关键字应答回调错误, 接口: %s , 状态: %s"%(url, data.status_code))
                except Exception as e:
                    logger.error("Errorrrrrrrr关键字应答回调异常: %s"%str(e))
            else:
                Messages.append({"message": x.answer_message.strip(), "isMarkdown": False})
    else:
        Messages.append({"message": "无指令数据, 请联系相关应用负责人 %s  完善help信息"%app_info["data"]["owner"], "isMarkdown": False})
    logger.info("returnNNNNNNNNNN:%s"%Messages)
    return {"code": 0, "data": Messages}


# 获取用户信息
def get_user_info(keyword):
    if keyword == "ou_dbbd3de4dd2e2eb18642de72f4017fe5":
        return {"username": "shijinyue", "nick_name": "石金月", "department_id": 9003}
    else:
        return {"username": "chenjiliang", "nick_name": "陈继亮", "department_id": 9003}

# 时间戳转换成时间
def time_to_str(t):
    import time
    if len(str(t)) > 10:
        t = int(str(t)[:10])
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))

# 融合云助手方式调用创群接口
def cloud_help_create_group(title, users):
    from rBase.feishu_main import feishu_action_main

    data = { 
              "action": "create",
              "is_markdown": False,
              "app_name": "op-robot-cloud-helper-service",
              "group_id": "",
              "user_ids": users,
              "message": title,
              "callback_url": "",
              "root_id": ""
            }
    app_id_data = app_id_retrieve(data["app_name"])
    return feishu_action_main(app_id_data, data)


# 修改群名称
def cloud_help_update_title(title, group_id):
    from rBase.feishu_main import feishu_action_main
    data = { 
              "action": "updateTitle",
              "is_markdown": False,
              "app_name": "op-robot-cloud-helper-service",
              "group_id": group_id,
              "user_ids": "",
              "message": title,
              "callback_url": "",
              "root_id": ""
            }

    app_id_data = app_id_retrieve(data["app_name"])
    return feishu_action_main(app_id_data, data)

# 发送消息
def cloud_help_send_msg(group_id, user_ids, message, is_markdown=False):
    from rBase.feishu_main import feishu_action_main
    data = {
              "action": "send",
              "is_markdown": is_markdown,
              "app_name": "op-robot-cloud-helper-service",
              "group_id": group_id,
              "user_ids": user_ids,
              "message": message,
              "callback_url": "",
              "root_id": ""
            }

    app_id_data = app_id_retrieve(data["app_name"])
    return feishu_action_main(app_id_data, data)


#创建工单
def create_ticket(group_id, department_id, sponsor, sponsor_id, processing_person, processing_person_id):
    import json, requests
    print("create ticket......")
    ticketData = {
                        "message_id": group_id,
                        "department_id": department_id,
                        "sponsor": sponsor,
                        "sponsor_id": sponsor_id,
                        "processing_person": processing_person,
                        "processing_person_id": processing_person_id,
                        "jira_id": "",
                        "desc": "融合云为您服务",
                        "is_inspection": False,
                        "ticket_type": 0
                    }

    return requests.post(TicketUrl, data=json.dumps(ticketData)).json()

#获取工单数据
def get_ticket(group_id):
    import requests
    data = requests.get(TicketUrl, data=json.dumps({"message_id": group_id}))
    try:
        return data.json().get("data", dict())
    except:
        return dict()

