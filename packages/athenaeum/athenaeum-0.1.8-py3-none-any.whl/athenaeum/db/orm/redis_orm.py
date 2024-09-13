from walrus import Database
from dynaconf.base import LazySettings
from typing import Optional, Dict, Any
from athenaeum.project import get_settings


def get_redis_orm(settings_object: Optional[LazySettings] = None, settings_dict: Dict[str, Any] = None) -> \
        Optional[Database]:
    settings_keys = ['REDIS_HOST', 'REDIS_PORT', 'REDIS_PASSWORD', 'REDIS_DBNAME']
    if (settings := get_settings(settings_keys, settings_object, settings_dict)) is None:
        return

    db_config = {
        'host': settings['REDIS_HOST'],
        'port': settings['REDIS_PORT'],
        'db': settings['REDIS_DBNAME'],
        'password': settings['REDIS_PASSWORD'],
    }

    redis_orm = Database(**db_config)
    return redis_orm
