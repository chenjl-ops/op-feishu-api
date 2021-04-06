from sqlalchemy.orm import sessionmaker
from sql_app.database import engine
from sql_app.models import *

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def model_create(model, request_data, fields):
    session = SessionLocal()
    
    data = model()
    for field in fields:
        if getattr(data, field) != request_data.get(field, ""):
            setattr(data, field, request_data.get(field, ""))
    session.add_all([
        data
        ])
    session.commit()
    session.close()
    return True


def model_update(model, id, request_data, fields):
    session = SessionLocal()
    data = session.query(model).filter_by(id=id).first()
    for field in fields:
        if getattr(data, field) != request_data.get(field):
            setattr(data, field, request_data.get(field))

    session.commit()
    session.close()
    return True


def model_delete(model, id, request_data, fields):
    session = SessionLocal()

    if id:
        data = session.query(model).filter_by(id=id).first().delete()
        session.commit()
        session.close
        return True
    else:
        return False


def app_id_retrieve(app_name=None, app_id=None):
    session = SessionLocal()

    if app_name:
        data = session.query(AppId).filter_by(app_name=app_name).first()

    if app_id:
        data = session.query(AppId).filter_by(app_id=app_id).first()

    data = data.to_dict
    session.commit()
    session.close()
    return {"data": data}

def feishu_token_retrieve(feishu_token):
    session = SessionLocal()

    data = session.query(AppId).filter_by(feishu_token=feishu_token).first()

    data = data.to_dict
    session.commit()
    session.close()
    return {"data": data}

# 获取自动应答相关数据 AutoAskConfig
def auto_ask_config_retrieve(keyword, app_id=None, app_name=None):
    session = SessionLocal()

    if app_name:
        data = session.query(AutoAskConfig).filter_by(app_name=app_name)

    if app_id:
        data = session.query(AutoAskConfig).filter_by(app_id=app_id)

    session.commit()
    session.close()
    return data
