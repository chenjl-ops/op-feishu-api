import os
import sys

HERE = os.path.abspath(__file__)
HOME_DIR = os.path.split(os.path.split(HERE)[0])[0]
os.sys.path.append(HOME_DIR)

from tools import apollo_manage
app_name = "op-robot-feishu-api"

# 初始化实例
apollo_manage = apollo_manage.ApolloConfig(app_name)

DB_HOST = apollo_manage.get_apollo_config("DB_HOST")
DB_USER = apollo_manage.get_apollo_config("DB_USER")
DB_PASSWD = apollo_manage.get_apollo_config("DB_PASSWD")
DB_PORT = apollo_manage.get_apollo_config("DB_PORT")
DB_NAME = apollo_manage.get_apollo_config("DB_NAME")

FeiShuBaseUrl = apollo_manage.get_apollo_config("FeiShuBaseUrl")
ACTIONS = eval(apollo_manage.get_apollo_config("ACTIONS"))
TicketUrl = apollo_manage.get_apollo_config("ticket_url")
APPID = apollo_manage.get_apollo_config("app_id")
robotStatus = eval(apollo_manage.get_apollo_config("robot_status"))
EcmUrl = apollo_manage.get_apollo_config("ecm_url")
MustUserIds = apollo_manage.get_apollo_config("robot_must_add_people_uid")

notice_time = apollo_manage.get_apollo_config("notice_time")

oncall_url = apollo_manage.get_apollo_config("oncall_url")
oncall_name = apollo_manage.get_apollo_config("oncall_name")
robot_help_result_message_notice_change_title = apollo_manage.get_apollo_config("robot_help_result_message_notice_change_title")


if __name__ == "__main__":
    #print(mysql_db_name, mysql_db_user, mysql_db_host, mysql_db_port, mysql_db_passwd)
    print("Robot-Api apolloConfig")
