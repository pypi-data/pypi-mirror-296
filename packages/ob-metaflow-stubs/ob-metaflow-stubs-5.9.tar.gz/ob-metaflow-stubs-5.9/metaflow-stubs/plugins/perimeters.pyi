##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.12.20.1+ob(v1)                                                   #
# Generated on 2024-09-16T17:51:44.699852                                        #
##################################################################################

from __future__ import annotations

import typing

class MetaflowException(Exception, metaclass=type):
    def __init__(self, msg = "", lineno = None):
        ...
    def __str__(self):
        ...
    ...

CURRENT_PERIMETER_KEY: str

CURRENT_PERIMETER_URL: str

CURRENT_PERIMETER_URL_LEGACY_KEY: str

def get_perimeter_config_url_if_set_in_ob_config() -> typing.Optional[str]:
    ...

