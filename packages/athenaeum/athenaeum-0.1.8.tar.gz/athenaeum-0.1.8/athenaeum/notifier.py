import httpx
import yagmail
import tkinter as tk
from tkinter import messagebox
from dynaconf.base import LazySettings
from typing import Optional, Union, Dict, List, Any
from athenaeum.logger import logger
from athenaeum.tools import get_routine_name
from athenaeum.project import get_settings


class Notifier(object):
    logger = logger

    @classmethod
    def notify_by_dingding(cls) -> None:
        method_name = get_routine_name()

    @classmethod
    def notify_by_email(cls,
                        settings_object: Optional[LazySettings] = None,
                        settings_dict: Dict[str, Any] = None) -> None:
        method_name = get_routine_name()

        settings_keys = ['NOTIFY_BY_EMAIL_USERNAME', 'NOTIFY_BY_EMAIL_PASSWORD', 'NOTIFY_BY_EMAIL_HOST',
                         'NOTIFY_BY_EMAIL_TO',
                         'NOTIFIER_SUBJECT', 'NOTIFIER_CONTENT_TEMPLATE']
        if (settings := get_settings(settings_keys, settings_object, settings_dict)) is None:
            return

        func_config = {
            'user': settings['NOTIFY_BY_EMAIL_USERNAME'],
            'password': settings['NOTIFY_BY_EMAIL_PASSWORD'],
            'host': settings['NOTIFY_BY_EMAIL_HOST'],
        }
        send_kwargs = {
            'to': settings['NOTIFY_BY_EMAIL_TO'],
            'subject': settings['NOTIFIER_SUBJECT'],
            'contents': settings['NOTIFIER_CONTENT_TEMPLATE'].format(method_name),
        }
        try:
            yag = yagmail.SMTP(**func_config)
            yag.send(**send_kwargs)
        except Exception as exception:
            cls.logger.exception(f'邮件发送失败，exception：`{exception}`！')
        else:
            cls.logger.success('邮件发送成功')

    @classmethod
    def notify_by_bark(cls,
                       settings_object: Optional[LazySettings] = None,
                       settings_dict: Dict[str, Any] = None) -> None:
        method_name = get_routine_name()

        settings_keys = ['NOTIFY_BY_BARK_KEY',
                         'NOTIFIER_TITLE', 'NOTIFIER_MESSAGE_TEMPLATE']
        if (settings := get_settings(settings_keys, settings_object, settings_dict)) is None:
            return

        func_config = {
            'key': settings['NOTIFY_BY_BARK_KEY'],
            'title': settings['NOTIFIER_TITLE'],
            'message': settings['NOTIFIER_MESSAGE_TEMPLATE'].format(method_name),
        }

        try:
            url = 'https://api.day.app/{key}/{title}/{message}'.format(**func_config)
            _response = httpx.get(url)
        except Exception as exception:
            cls.logger.exception(f'推送发送失败，exception：`{exception}`！')
        else:
            cls.logger.success('推送发送成功')

    @classmethod
    def notify_by_tkinter(cls, break_cond: Union[List[Optional[bool]], Optional[bool]] = True,
                          settings_object: Optional[LazySettings] = None,
                          settings_dict: Dict[str, Any] = None) -> None:
        method_name = get_routine_name()

        settings_keys = ['NOTIFIER_TITLE', 'NOTIFIER_MESSAGE_TEMPLATE']
        if (settings := get_settings(settings_keys, settings_object, settings_dict)) is None:
            return

        func_config = {
            'title': settings['NOTIFIER_TITLE'],
            'message': settings['NOTIFIER_MESSAGE_TEMPLATE'].format(method_name),
        }

        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)

        while True:
            result = messagebox.askyesnocancel(**func_config)
            if isinstance(break_cond, list):
                if result in break_cond:
                    break
            else:
                if result == break_cond:
                    break

        root.destroy()
