import os
import sys

HERE = os.path.abspath(__file__)
HOME_DIR = os.path.split(os.path.split(HERE)[0])[0]
os.sys.path.append(HOME_DIR)

from tools import apollo_manage
appName = "op-robot-feishu-api"

DB_HOST = apollo_manage.get_apollo_config("DB_HOST", appName)
DB_USER = apollo_manage.get_apollo_config("DB_USER", appName)
DB_PASSWD = apollo_manage.get_apollo_config("DB_PASSWD", appName)
DB_PORT = apollo_manage.get_apollo_config("DB_PORT", appName)
DB_NAME = apollo_manage.get_apollo_config("DB_NAME", appName)

FeiShuBaseUrl = apollo_manage.get_apollo_config("FeiShuBaseUrl", appName)
#userAccount = eval(apollo_manage.get_apollo_config("userAccount", appName))
ACTIONS = eval(apollo_manage.get_apollo_config("ACTIONS", appName))
#REURL = apollo_manage.get_apollo_config("reUrl", appName)
#CLUSTER = apollo_manage.get_apollo_config("redis_cluster", appName)
#SENTINELS = apollo_manage.get_apollo_config("redis_sentinels", appName)
#PASSWD = apollo_manage.get_apollo_config("redis_password", appName)
TicketUrl = apollo_manage.get_apollo_config("ticket_url", appName)
APPID = apollo_manage.get_apollo_config("app_id", appName)
robotStatus = eval(apollo_manage.get_apollo_config("robot_status", appName))

#mysql_db_name = apollo_manage.get_apollo_config("mysql_db_name", appName)
#mysql_db_user = apollo_manage.get_apollo_config("mysql_db_user", appName)
#mysql_db_host = apollo_manage.get_apollo_config("mysql_db_host", appName)
#mysql_db_port = apollo_manage.get_apollo_config("mysql_db_port", appName)
#mysql_db_passwd = apollo_manage.get_apollo_config("mysql_db_passwd", appName)

EcmUrl = apollo_manage.get_apollo_config("ecm_url", appName)
MustUserIds = apollo_manage.get_apollo_config("robot_must_add_people_uid", appName)

notice_time = apollo_manage.get_apollo_config("notice_time", appName)

oncall_url = apollo_manage.get_apollo_config("oncall_url", appName)
oncall_name = apollo_manage.get_apollo_config("oncall_name", appName)

robot_help_result_message_notice_change_title = apollo_manage.get_apollo_config("robot_help_result_message_notice_change_title", appName)


if __name__ == "__main__":
    #print(mysql_db_name, mysql_db_user, mysql_db_host, mysql_db_port, mysql_db_passwd)
    print("Robot-Api apolloConfig")
