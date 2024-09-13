from peewee import PostgresqlDatabase
from dynaconf.base import LazySettings
from typing import Optional, Dict, Any
from athenaeum.project import get_settings


def get_postgresql_orm(settings_object: Optional[LazySettings] = None, settings_dict: Dict[str, Any] = None) -> \
        Optional[PostgresqlDatabase]:
    settings_keys = ['POSTGRESQL_HOST', 'POSTGRESQL_PORT', 'POSTGRESQL_USERNAME', 'POSTGRESQL_PASSWORD',
                     'POSTGRESQL_DBNAME']
    if (settings := get_settings(settings_keys, settings_object, settings_dict)) is None:
        return

    db_config = {
        'host': settings['POSTGRESQL_HOST'],
        'port': settings['POSTGRESQL_PORT'],
        'user': settings['POSTGRESQL_USERNAME'],
        'password': settings['POSTGRESQL_PASSWORD'],
        'database': settings['POSTGRESQL_DBNAME'],
    }

    postgresql_orm = PostgresqlDatabase(**db_config)
    return postgresql_orm
