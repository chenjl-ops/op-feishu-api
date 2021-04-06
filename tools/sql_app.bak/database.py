from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from rBase.apollo_config import *
print(DB_HOST, DB_USER, DB_PASSWD, DB_PORT, DB_NAME)

#DB_HOST = "192.168.47.107"
#DB_USER = "admin"
#DB_PASSWD = "chenjiliang"
#DB_PORT = 3306
#DB_NAME = "op_feishu_robot"

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://{user}:{passwd}@{host}:{port}/{db_name}?charset=utf8mb4".format(user=DB_USER, passwd=DB_PASSWD, host=DB_HOST, port=DB_PORT, db_name=DB_NAME)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    max_overflow = 10,
    pool_size = 20,
    pool_timeout = 30,
    pool_recycle = 3600,
    pool_pre_ping=True
)

Base = declarative_base()
