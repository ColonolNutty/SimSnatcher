"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.enums.enumtypes.common_int import CommonInt
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils


class SSBodySide(CommonInt):
    """ Body Side"""
    NONE = 0
    BOTH = 1
    LEFT = 2
    RIGHT = 3

    @staticmethod
    def get_by_name(name: str) -> 'SSBodySide':
        """ Get a value by its name. """
        name = str(name).upper().strip()
        value: SSBodySide = CommonResourceUtils.get_enum_by_name(name, SSBodySide, default_value=SSBodySide.NONE)
        return value
