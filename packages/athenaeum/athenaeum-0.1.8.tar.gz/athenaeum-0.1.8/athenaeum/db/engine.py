from urllib.parse import quote_plus
from sqlalchemy import create_engine, Engine
from dynaconf.base import LazySettings
from typing import Optional, Dict, Any
from athenaeum.db import create_mysql_db
from athenaeum.project import get_settings


def get_mysql_engine(settings_object: Optional[LazySettings] = None, settings_dict: Dict[str, Any] = None) \
        -> Optional[Engine]:
    settings_keys = ['MYSQL_USERNAME', 'MYSQL_PASSWORD', 'MYSQL_HOST', 'MYSQL_PORT', 'MYSQL_DBNAME']
    if (settings := get_settings(settings_keys, settings_object, settings_dict)) is None:
        return

    db_config = {
        'username': settings['MYSQL_USERNAME'],
        'password': settings['MYSQL_PASSWORD'],
        'host': settings['MYSQL_HOST'],
        'port': settings['MYSQL_PORT'],
        'dbname': settings['MYSQL_DBNAME'],
    }

    create_mysql_db(settings_object, settings_dict)

    db_config['password'] = quote_plus(db_config['password'])  # 处理 password 中有 @ 符号
    mysql_uri = 'mysql+pymysql://{username}:{password}@{host}:{port}/{dbname}?charset=utf8mb4'.format(**db_config)
    mysql_engine = create_engine(mysql_uri)
    return mysql_engine
