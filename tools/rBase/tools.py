
#获取飞书 access_token
def get_tenant_access_token(app_id="cli_9fe681baedff100e", app_secret="M67a77yl97BT3JkwboZ0UfgOTMi1PTtW"):
    import json
    import requests

    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
    headers = {"Content-Type": "application/json"}
    data = {"app_id": app_id, "app_secret": app_secret}

    return requests.post(url, headers=headers, data=json.dumps(data)).json()

#封装飞书所有接口请求, 在header中增加authorization控制
def feishu_requests_main(method, url, data=dict(), app_id="cli_9fe681baedff100e", app_secret="M67a77yl97BT3JkwboZ0UfgOTMi1PTtW"):
    import json
    import requests

    token_data = get_tenant_access_token(app_id, app_secret)
    if token_data.get("code", "") == 0:
        headers = {"Content-Type": "application/json", "Authorization": "Bearer "+token_data.get("tenant_access_token")}
    else:
        return {"code": 403, "msg": "获取token失败"}

    if method.upper() in ["GET", "POST", "PUT", "DELETE"]:
        if isinstance(data, dict):
            if method.upper() == "GET":
                response_data = requests.get(url, headers=headers).json()
            elif method.upper() == "POST":
                response_data = requests.post(url, headers=headers, data=json.dumps(data)).json()
            elif method.upper() == "PUT":
                response_data = requests.put(url, headers=headers, data=json.dumps(data)).json()
            elif method.upper() == "POST":
                response_data = requests.delete(url, headers=headers, data=json.dumps(data)).json()
            return response_data
        else:
            return {"code": 400, "msg": "data error"}
    else:
        return {"code": 400, "msg": "method %s not allow"%method}

#飞书上传图片统一接口 图片地址转换成飞书官方image_id
def feishu_upload_image(image_path, app_id="cli_9fe681baedff100e", app_secret="M67a77yl97BT3JkwboZ0UfgOTMi1PTtW"):
    import requests
    with open(image_path, 'rb') as f:
        image = f.read()
    resp = requests.post(
        url='https://open.feishu.cn/open-apis/image/v4/put/',
        headers={'Authorization': get_tenant_access_token(app_id, app_secret).get("tenant_access_token")},
        files={
            "image": image
        },
        data={
            "image_type": "message"
        },
        stream=True)
    resp.raise_for_status()
    content = resp.json()

    return content

#封装飞书card 内容模块数据
def feishu_card_div(title, fields):
    elements = list()

    temp_x = {"tag": "div"}
    if title:
        temp_x["text"] = {
                        "tag": "plain_text",
                        "content": title
                    }
    temp_x["fields"] = list()
    for y in fields:
        temp_y = {
                    "is_short": y.get("is_short"),
                    "text": {
                        "tag": "lark_md",
                        "content": y.get("text")
                    }
                }
        temp_x["fields"].append(temp_y)
    elements.append(temp_x)

    return elements

#封装飞书card 图片模块数据
def feishu_card_img(title, images):
    import copy
    elements = list()

    temp_x = {
            "tag": "img",
            "title": {
                "tag": "plain_text",
                "content": title
            }
        }

    for image in x.get("images"):
        temp_image = copy.deepcopy(temp_x)
        image_data = feishu_upload_image(image.get("image_url"))
        if image_data.get("code", "") == 0:
            temp_image["image_key"] = image_data.get("data", dict()).get("image_key", "")
        temp_image["alt"] = {
                    "tag": "plain_text",
                    "content": image.get("text")
                }
        elements.append(temp_image)

    return elements

#封装飞书card 备注模块数据
def feishu_card_note(title, elements):
    pass

#封装飞书card 交互模块数据
def feishu_card_action(actions, layout=None):
    elements = list()

    action_temp = {"tag": "action", "actions": actions}

    if layout:
        action_temp["layout"] = layout

    elements.append(action_temp)
    return elements

#封装飞书markdown类型数据
def feishu_card_markdown(message):
    return {"tag": "markdown", "content": message}
