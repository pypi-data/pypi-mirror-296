from .netcook import checked_cookies

__all__ = ['checked_cookies']

import sys

def inject_checked_cookies():
    importer_module = sys.modules['__main__']
    setattr(importer_module, 'checked_cookies', checked_cookies)

inject_checked_cookies()

