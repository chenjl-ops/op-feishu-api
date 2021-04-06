# op-feishu-api
封装飞书相关接口

## 简介
op-feishu-api主要封装飞书api提供相关api服务
对外提供如下能力(基于飞书):

飞书用户:
1. 通过用户邮箱前缀搜索用户信息
2. 通过用户open_id获取用户信息

飞书消息
1. 发送普通消息，图片消息
2. 发送富文本消息
3. 发送卡片消息
4. 发送群名片
5. 获取消息已读状态

飞书群组
1. 创建 解散群
2. 获取群列表
3. 获取群成员列表
4. 获取群信息
5. 更新群信息
6. 群内 加人 踢人

## 环境依赖
python >= 3.6
fastapi==0.49.0
uvicorn==0.11.3

详见文件 requirements.txt

## 外部依赖
飞书open api接口

## Run Server
```
python main.py --port xxxx
```

## TODO
1. 其他功能集合扩展

## 启动 验证
![image](https://user-images.githubusercontent.com/81603118/113654795-3401e900-96cb-11eb-8203-61298428e9f7.png)
![image](https://user-images.githubusercontent.com/81603118/113654862-60b60080-96cb-11eb-8eed-b5bf54266a17.png)
![image](https://user-images.githubusercontent.com/81603118/113654907-79261b00-96cb-11eb-9b44-1c961d45edb8.png)



