import random
from dataclasses import dataclass
from dynaconf.base import LazySettings
from typing_extensions import Self
from typing import Optional, Dict, Any
from athenaeum.project import get_settings


@dataclass
class AccountEntity(object):
    """
    使用教程：
        /project/settings/settings.toml

        [default.account.baidu.user1]
        owner = "xxx"
        username = "111111"
        password = "999999"

        [default.account.360.user1]
        owner = "yyy"
        username = "222222"
        password = "888888"

    """
    platform: str
    owner: str
    username: str
    password: str

    @classmethod
    def get_a_random_account_entity(cls,
                                    platform: str,
                                    settings_object: Optional[LazySettings] = None,
                                    settings_dict: Dict[str, Any] = None) -> Optional[Self]:
        settings_keys = ['ACCOUNT']
        if (settings := get_settings(settings_keys, settings_object, settings_dict)) is None:
            return

        func_config = {
            'account': settings['ACCOUNT'],
        }
        users = func_config['account'][platform]
        user = users[random.choice(list(users.keys()))]
        return cls(
            platform=platform,
            owner=user.owner,
            username=user.username,
            password=user.password
        )
