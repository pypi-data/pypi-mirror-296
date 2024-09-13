from DrissionPage import ChromiumOptions, ChromiumPage
from athenaeum.logger import logger


class BrowserAutomation(object):
    logger = logger

    @classmethod
    def get_ChromiumPage(cls, *args, **kwargs) -> ChromiumPage:  # noqa
        co = ChromiumOptions()
        cp = ChromiumPage(addr_or_opts=co)
        return cp
