import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, UniqueConstraint, Index, func

import sys, os
import imp
imp.reload(sys)

HERE = os.path.abspath(__file__)
HOME_DIR = os.path.split(os.path.split(HERE)[0])[0]
os.sys.path.append(HOME_DIR)
#script_path = os.path.join(HOME_DIR, "tools")


from sql_app.database import Base
#from database import Base

STRFTIME_FORMAT = "%Y-%m-%d %H:%M:%S"
STRFDATE_FORMAT = "%Y-%m-%d"

class AppId(Base):
    __tablename__ = "robot_api_app_id"

    id = Column(Integer, primary_key=True)
    app_id = Column(String(128), unique=True, comment="app_id信息")
    app_name = Column(String(128), index=True, nullable=False, comment="应用名称")
    feishu_app_id = Column(String(256), comment="飞书app_id信息")
    feishu_app_secret = Column(String(256), comment="飞书app_secret信息")
    feishu_token = Column(String(256), comment="飞书token信息")
    owner = Column(String(64), nullable=False, comment="负责人")
    description = Column(String(1024), comment="描述")
    is_create = Column(Boolean, default=False, comment="合并转发是否创群")
    create_user = Column(String(64), default="sys", comment="创建用户")
    create_time = Column(DateTime, server_default=func.now(), comment="创建时间")
    last_modified_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="最后修改时间")
    last_modified_user = Column(String(64), default="sys", comment="最后变更人")
    is_active = Column(Boolean, default=True, comment="是否在线")

    @property
    def to_dict(self):
        return {"id": self.id,
                "app_id": self.app_id,
                "app_name": self.app_name, 
                "feishu_app_id": self.feishu_app_id,
                "feishu_app_secret": self.feishu_app_secret,
                "feishu_token": self.feishu_token,
                "owner": self.owner, 
                "description": self.description, 
                "is_create": self.is_create, 
                "create_user": self.create_user,
                "create_time": self.create_time.strftime(STRFTIME_FORMAT),
                "last_modified_time": self.last_modified_time.strftime(STRFTIME_FORMAT), 
                "last_modified_user": self.last_modified_user,
                "is_active": self.is_active
            }

    @property
    def to_api(self):
        return {"id": self.id, 
                "app_id": self.app_id, 
                "app_name": self.app_name, 
                "feishu_app_id": self.feishu_app_id,
                "feishu_app_secret": self.feishu_app_secret,
                "feishu_token": self.feishu_token,
                "owner": self.owner, 
                "description": self.description, 
                "is_create": self.is_create
            }


class RobotOpenApi(Base):
    __tablename__ = "robot_api_open_api"

    id = Column(Integer, primary_key=True)
    app_id = Column(String(64), index=True, comment="应用")
    app_name = Column(String(64), index=True, comment="应用名称")
    action = Column(String(32), comment="动作")
    root_id = Column(String(64), comment="回复消息ID")
    mid = Column(String(32), comment="唯一消息ID")
    group_id = Column(String(128), nullable=True, comment="群ID")
    user_ids = Column(Text, nullable=True, comment="用户ids")
    message = Column(Text, nullable=True, comment="内容")
    is_markdown = Column(Boolean, default=False, comment="markdown标识")
    status = Column(Boolean, default=False, comment="状态")
    callback_url = Column(String(1024), nullable=True, comment="回调url")
    feishu_api_response = Column(Text, nullable=True, comment="飞书接口返回结果")
    create_time = Column(DateTime, server_default=func.now(), comment="创建时间")
    last_modified_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="最后修改时间")

    @property
    def to_dict(self):
        return {"id": self.id,
                "app_id": self.app_id,
                "app_name": self.app_name,
                "action": self.action,
                "root_id": self.root_id,
                "mid": self.mid,
                "group_id": self.group_id,
                "user_ids": self.user_ids,
                "message": self.message,
                "is_markdown": self.is_markdown,
                "status": self.status,
                "callback_url": self.callback_url,
                "feishu_api_response": self.feishu_api_response, 
                "create_time": self.create_time.strftime(STRFTIME_FORMAT),
                "last_modified_time": self.last_modified_time.strftime(STRFTIME_FORMAT)
            }

class RobotGroup(Base):
    __tablename__ = "robot_api_group"

    id = Column(Integer, primary_key=True)
    app_id = Column(String(64), index=True, comment="应用")
    app_name = Column(String(64), index=True, comment="应用名称")
    group_id = Column(String(128), comment="群组ID")
    group_name = Column(String(128), comment="群名称")
    mid = Column(String(64), comment="唯一消息ID")
    create_time = Column(DateTime, server_default=func.now(), comment="创建时间")

    @property
    def to_dict(self):
        return {"id": self.id,
                "app_id": self.app_id,
                "app_name": self.app_name,
                "group_id": self.group_id,
                "group_name": self.group_name,
                "mid": self.mid,
                "create_time": self.create_time.strftime(STRFTIME_FORMAT)
            }

class AutoAskConfig(Base):
    __tablename__ = "robot_api_auto_ask_config"
    id = Column(Integer, primary_key=True)
    app_id = Column(String(64), index=True, comment="应用")
    app_name = Column(String(64), index=True, comment="应用名称")
    keyword = Column(String(128), comment="关键字")
    answer_message = Column(Text, comment="应答")
    create_time = Column(DateTime, server_default=func.now(), comment="创建时间")
    last_modified_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="最后修改时间")

    @property
    def to_dict(self):
        return {"id": self.id,
                "app_id": self.app_id,
                "app_name": self.app_name,
                "keyword": self.keyword,
                "answer_message": self.answer_message,
                "create_time": self.create_time.strftime(STRFTIME_FORMAT),
                "last_modified_time": self.last_modified_time.strftime(STRFTIME_FORMAT)
            }



def init_db():
    from database import engine
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    print("ok")
    init_db()
