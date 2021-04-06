import json
import requests

from rBase.apollo_config import FeiShuBaseUrl

#FeiShuBaseUrl = "http://192.168.47.107:9003"

def feishu_action_main(app_id_data, request_data):
    #TODO 未来可优化点,通过dict减少if层级逻辑
    print("app_id_data: ", app_id_data)

    func_dict = {
                "create": create_feishu_group,
                "addMember": feishu_group_add_member,
                "removeMember": feishu_group_del_member,
                "updateTitle": update_feishu_group_title,
                "disband": feishu_disband_group,
                "auth": update_feishu_group_auth,
                "send": send_feishu_message
            }

    feishu_app_id = app_id_data.get("data").get("feishu_app_id")
    feishu_app_secret = app_id_data.get("data").get("feishu_app_secret")

    print("feishu_action_main:", request_data)
    user_ids = request_data.get("user_ids")
    if user_ids:
        search_users = [i for i in user_ids.split(",") if not i.startswith("ou_")]
        if search_users:
            user_ids = get_feishu_users(",".join(search_users))

    action = request_data.get("action", None)
    print("action: ", action)
    if action == "create":
        # TODO 需要callback相关地址
        return create_feishu_group(request_data.get("message"), user_ids, feishu_app_id, feishu_app_secret)
    if action == "addMember":
        return feishu_group_add_member(request_data.get("group_id"), user_ids, feishu_app_id, feishu_app_secret)
    if action == "removeMember":
        return feishu_group_del_member(request_data.get("group_id"), user_ids, feishu_app_id, feishu_app_secret)
    if action == "updateTitle":
        return update_feishu_group_title(request_data.get("group_id"), request_data.get("message"), feishu_app_id, feishu_app_secret)
    if action == "auth":
        return update_feishu_group_auth(request_data.get("group_id"), feishu_app_id, feishu_app_secret)
    if action == "disband":
        return feishu_disband_group(request_data.get("group_id"), feishu_app_id, feishu_app_secret)
    if action == "send":
        group_id = request_data.get("group_id", "")
        open_ids = user_ids

        if request_data.get("is_markdown", False):
            #markdown 数据类型
            if group_id:
                if user_ids:
                    at_open_id = user_ids
                    open_ids = ""
                else:
                    at_open_id = ""
                return send_feishu_markdown_message(feishu_app_id, 
                                                    feishu_app_secret, 
                                                    request_data.get("message"), 
                                                    group_id, 
                                                    open_ids, 
                                                    at_open_id, 
                                                    request_data.get("root_id"))
            else:
                return send_feishu_markdown_message(feishu_app_id, 
                                                    feishu_app_secret, 
                                                    request_data.get("message"), 
                                                    group_id, 
                                                    open_ids, 
                                                    "", 
                                                    request_data.get("root_id"),
                                                    True)
        else:
            #普通消息数据类型
            if group_id: #群组和用户数据都存在 为 群组内@消息
                if user_ids:
                    at_open_id = user_ids
                    open_ids = ""
                else:
                    at_open_id = ""
                return send_feishu_message("text", 
                                            request_data.get("message"), 
                                            feishu_app_id, 
                                            feishu_app_secret,
                                            group_id, 
                                            open_ids, 
                                            at_open_id,
                                            request_data.get("root_id"))
            else: #群组数据不存在 为单聊数据
                return send_feishu_message("text",
                                            request_data.get("message"),
                                            feishu_app_id, 
                                            feishu_app_secret,
                                            group_id,
                                            open_ids,
                                            "",
                                            request_data.get("root_id"),
                                            True)



def get_feishu_users(emails):
    path = "/v1/users/"
    query = "?usernames="+emails
    data = requests.get(FeiShuBaseUrl+path+query)
    users = list()
    if data.json()["code"] == 0:
        for x, y in data.json().get("data").get("email_users").items():
            users.append(y[0].get("open_id"))
    return ",".join(users)



'''
{
  "code": 0,
  "data": {
    "chat_id": "oc_f6f4140444ddc58cadccf333f6693844",
    "invalid_open_ids": [],
    "invalid_user_ids": []
  },
  "msg": "ok"
}
'''
def create_feishu_group(group_name, open_ids, app_id, app_secret):
    path = "/v1/group/create/"
    query = "?app_id={app_id}&app_secret={app_secret}".format(app_id=app_id, app_secret=app_secret)
    data = {
            "name": group_name or "融合云为您服务",
            "description": group_name or "融合云为您服务",
            "open_ids": open_ids.split(","),
            "only_owner_add": False,
            "share_allowed": True,
            "only_owner_at_all": False,
            "only_owner_edit": False
        }

    return requests.post(FeiShuBaseUrl + path + query, data=json.dumps(data)).json()

'''
获取机器人所在群列表
{
    "code": 0,
    "data": {
        "groups": [
            {
                "avatar": "http://p3.pstatp.com/origin/78c0000676df676a7f6e",
                "chat_id": "oc_9e9619b938c9571c1c3165681cdaead5",
                "description": "description1",
                "name": "test1",
                "owner_open_id": "ou_194911f90c43ec42d1ba0e93f22b8fb1",
                "owner_user_id": "ca51d83b"
            },
            {
                "avatar": "http://p4.pstatp.com/origin/dae10015cfb346541010",
                "chat_id": "oc_5ce6d572455d361153b7cb51da133945",
                "description": "description2",
                "name": "test2",
                "owner_open_id": "ou_194911f90c43ec42d1ba0e93f22b8fb1",
                "owner_user_id": "ca51d83b"
            }
        ],
        "has_more": false,
        "page_token": "0"
    },
    "msg": "ok"
}
'''
def get_feishu_group_list(app_id, app_secret, page_size=100, page_token="", l=list()):
    path = "/v1/group/list/"
    query = "?page_size={page_size}&page_token={page_token}".format(page_size=page_size, page_token=page_token)

    data = requests.get(FeiShuBaseUrl+path+query)
    #递归获取群组数据
    if data.json().get("data", dict()).get("page_token", None):
        l += data.json().get("data", dict()).get("groups", list())
        get_feishu_group_list(app_id, app_secret, l)

    group_data = data.json()
    group_data["data"]["groups"] = l
    return group_data


'''
获取群组内成员列表
{
    "code": 0,
    "data": {
        "chat_id": "oc_92c3f700c2ae31369cefee459fb93870",
        "has_more": true,
        "members": [
            {
                "open_id": "ou_56799ac95e82434b49e1cf00c3a3a251",
                "user_id": "1g6gbf73",
                "name": "张三"
            },
            {
                "open_id": "ou_9c7a2ce4f61e78dfe00ffa8b11524e2a",
                "user_id": "296f8dfb",
                "name": "李四"
            }
        ],
        "page_token": "1559288627"
    },
    "msg": "ok"
}
'''
def get_feishu_group_members_list(chat_id, app_id, app_secret, page_size=100, page_token="", l=list()):
    path = "/v1/group/members/"
    query = "?page_size={page_size}&page_token={page_token}".format(page_size=page_size, page_token=page_token)

    data = requests.get(FeiShuBaseUrl+path+query)
    #递归获取群成员数据
    page_token = data.json().get("data", dict()).get("page_token", None)
    if page_token:
        l += data.json().get("data", dict()).get("groups", list())
        get_feishu_group_members_list(chat_id, app_id, app_secret, page_size, page_token, l)

    group_members_data = data.json()
    group_members_data["data"]["groups"] = l
    return group_members_data


'''
修改群标题
'''
def update_feishu_group_title(chat_id, title_name, app_id, app_secret):
    path = "/v1/group/update/"
    query = "?app_id={app_id}&app_secret={app_secret}".format(app_id=app_id, app_secret=app_secret)
    data = {
            "chat_id": chat_id,
            "name": title_name
        }

    return requests.post(FeiShuBaseUrl+path+query, data=json.dumps(data)).json()
    
'''
修改群权限-只有群主能加人
'''
def update_feishu_group_auth(chat_id, app_id, app_secret):
    path = "/v1/group/update/"
    query = "?app_id={app_id}&app_secret={app_secret}".format(app_id=app_id, app_secret=app_secret)
    data = {
            "chat_id": chat_id,
            "only_owner_add": True
        }

    return requests.post(FeiShuBaseUrl+path+query, data=json.dumps(data)).json()


'''
加人
'''
def feishu_group_add_member(chat_id, open_ids, app_id, app_secret):
    path = "/v1/group/member/add/"
    query = "?app_id={app_id}&app_secret={app_secret}".format(app_id=app_id, app_secret=app_secret)

    data = {
            "chat_id": chat_id,
            "open_ids": open_ids.split(",")
        }

    return requests.post(FeiShuBaseUrl+path+query, data=json.dumps(data)).json()

'''
踢人
'''
def feishu_group_del_member(chat_id, open_ids, app_id, app_secret):
    path = "/v1/group/member/delete/"
    query = "?app_id={app_id}&app_secret={app_secret}".format(app_id=app_id, app_secret=app_secret)
    
    data = {
            "chat_id": chat_id,
            "open_ids": open_ids.split(",")
        }

    return requests.post(FeiShuBaseUrl+path+query, data=json.dumps(data)).json()


'''
解散群组
'''
def feishu_disband_group(chat_id, app_id, app_secret):
    path = "/v1/group/disband/"
    query = "?chat_id={chat_id}&app_id={app_id}&app_secret={app_secret}".format(chat_id=chat_id, app_id=app_id, app_secret=app_secret)

    return requests.post(FeiShuBaseUrl+path+query).json()


'''
实现老版本罗伯特发送消息
结果: 
{
  "code": 0,
  "data": {
    "message_id": "om_41cdda61f020a6dbc609978d54ceb3b3"
  },
  "msg": "ok"
}
'''
def send_feishu_message(message_type, content, app_id, app_secret, chat_id="", open_ids="", at_open_id="", root_id="", is_batch=False):
    path = "/v1/message/send/"
    #query = "?app_id={app_id}&app_secret={app_secret}".format(app_id=app_id, app_secret=app_secret)
    query = "?app_id={app_id}&app_secret={app_secret}&is_batch={is_batch}".format(app_id=app_id, app_secret=app_secret, is_batch=is_batch)
    data = {
              "root_id": root_id,
              "message_type": message_type,
              "content": content,
              "at_open_id": at_open_id
            }
    if chat_id:
        data["chat_id"] = chat_id
    if open_ids:
        data["open_ids"] = open_ids.split(",")

    return requests.post(FeiShuBaseUrl + path + query, data=json.dumps(data)).json()

'''
实现markdown发送格式数据
'''
def send_feishu_markdown_message(app_id, app_secret, message, chat_id="", open_ids="", at_open_id="", root_id="", is_batch=False):
    robot_message_title = "罗伯特平台提供技术支持"

    path = "/v1/message/send/card/"
    query = "?app_id={app_id}&app_secret={app_secret}&is_batch={is_batch}".format(app_id=app_id, app_secret=app_secret, is_batch=is_batch)
    
    if at_open_id:
        message = "".join(["<at id=%s></at>"%i for i in at_open_id.split(",")]) + message

    data = {
              "config": {
                "wide_screen_mode": True,
                "enable_forward": True
              },
              "header": {
                "title": robot_message_title,
                "template": "blue"
              },
              "card": {
                "elements": [
                  {
                    "tag": "div",
                    "text": "plain_text",
                    "title": "罗伯特工单支持",
                    "field": [
                      {
                        "is_short": False,
                        "text": message
                      }
                    ],
                  }
                ]
              }
            }

    if root_id:
        data["root_id"] = root_id
    if open_ids:
        data["open_ids"] = open_ids.split(",")
    if chat_id:
        data["chat_id"] = chat_id

    print("card_data2:", data)

    return requests.post(FeiShuBaseUrl + path + query, data=json.dumps(data)).json()
