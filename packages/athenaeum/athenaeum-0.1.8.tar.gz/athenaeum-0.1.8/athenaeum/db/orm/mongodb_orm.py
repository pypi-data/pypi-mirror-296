from mongoengine import connect
from dynaconf.base import LazySettings
from typing import Optional, Dict, Any
from athenaeum.project import get_settings


def get_mongodb_orm(settings_object: Optional[LazySettings] = None, settings_dict: Dict[str, Any] = None) -> Any:
    settings_keys = ['MONGODB_HOST', 'MONGODB_PORT', 'MONGODB_USERNAME', 'MONGODB_PASSWORD', 'MONGODB_DBNAME']
    if (settings := get_settings(settings_keys, settings_object, settings_dict)) is None:
        return

    db_config = {
        'host': settings['MONGODB_HOST'],
        'port': settings['MONGODB_PORT'],
        'username': settings['MONGODB_USERNAME'],
        'password': settings['MONGODB_PASSWORD'],
        'db': settings['MONGODB_DBNAME'],
    }

    mongodb_orm = connect(**db_config)
    return mongodb_orm
