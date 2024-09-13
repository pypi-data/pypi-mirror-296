from dynaconf.base import LazySettings
from typing import Optional, Dict, Any
from athenaeum.project import get_settings


def create_mysql_db(settings_object: Optional[LazySettings] = None, settings_dict: Dict[str, Any] = None) -> None:
    import pymysql

    settings_keys = ['MYSQL_HOST', 'MYSQL_PORT', 'MYSQL_USERNAME', 'MYSQL_PASSWORD', 'MYSQL_DBNAME']
    if (settings := get_settings(settings_keys, settings_object, settings_dict)) is None:
        return

    db_config = {
        'user': settings['MYSQL_USERNAME'],
        'password': settings['MYSQL_PASSWORD'],
        'host': settings['MYSQL_HOST'],
        'port': settings['MYSQL_PORT'],
    }

    try:
        with pymysql.connect(**db_config) as connection:
            with connection.cursor() as cursor:
                sql = 'CREATE DATABASE IF NOT EXISTS {database}'.format(database=settings['MYSQL_DBNAME'])
                cursor.execute(sql)
    except pymysql.err.OperationalError:
        pass
