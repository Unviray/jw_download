"""
jw_download.config
==================

Handle configuration.
"""

import confuse
from confuse import exceptions


class Config:
    """
    Handle configuration.
    """

    def __init__(self):
        self.conf = confuse.Configuration('jw_download', __name__)

    def __call__(self, arg, cast, default=None):
        try:
            return self.conf[arg].get(cast)
        except exceptions.NotFoundError:
            return default

    @property
    def date(self):
        return self("date", cast=str)

    @property
    def pub(self):
        return self("pub", cast=str)

    @property
    def fileformat(self):
        return self("fileformat", cast=str)

    @property
    def lang(self):
        return self("lang", cast=str)

    @property
    def dest(self):
        return self("dest", cast=str)
