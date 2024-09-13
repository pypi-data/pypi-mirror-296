from peewee import MySQLDatabase
from dynaconf.base import LazySettings
from typing import Optional, Dict, Any
from athenaeum.project import get_settings
from athenaeum.db import create_mysql_db


def get_mysql_orm(settings_object: Optional[LazySettings] = None, settings_dict: Dict[str, Any] = None) -> \
        Optional[MySQLDatabase]:
    settings_keys = ['MYSQL_HOST', 'MYSQL_PORT', 'MYSQL_USERNAME', 'MYSQL_PASSWORD', 'MYSQL_DBNAME']
    if (settings := get_settings(settings_keys, settings_object, settings_dict)) is None:
        return

    db_config = {
        'host': settings['MYSQL_HOST'],
        'port': settings['MYSQL_PORT'],
        'user': settings['MYSQL_USERNAME'],
        'password': settings['MYSQL_PASSWORD'],
        'database': settings['MYSQL_DBNAME'],
        'charset': 'utf8mb4',
        'use_unicode': True,
        'init_command': "SET time_zone='+8:00'"
    }
    create_mysql_db(settings_object, settings_dict)

    mysql_orm = MySQLDatabase(**db_config)
    return mysql_orm
