from peewee import SqliteDatabase
from dynaconf.base import LazySettings
from typing import Optional, Dict, Any
from athenaeum.project import get_settings


def get_sqlite_orm(settings_object: Optional[LazySettings] = None, settings_dict: Dict[str, Any] = None) -> Any:
    settings_keys = ['SQLITE_PATH']
    if (settings := get_settings(settings_keys, settings_object, settings_dict)) is None:
        return

    db_config = {
        'database': settings['SQLITE_PATH']
    }

    sqlite_orm = SqliteDatabase(**db_config)
    return sqlite_orm
