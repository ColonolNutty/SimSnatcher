"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple

from sims4communitylib.enums.enumtypes.common_int import CommonInt
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils


class SSBindingBodyLocation(CommonInt):
    """ Binding Types. """
    NONE: 'SSBindingBodyLocation' = 0
    EYES: 'SSBindingBodyLocation' = 1
    MOUTH: 'SSBindingBodyLocation' = 2
    FEET: 'SSBindingBodyLocation' = 3
    WRISTS: 'SSBindingBodyLocation' = 4
    ARMS: 'SSBindingBodyLocation' = 5
    ANKLES: 'SSBindingBodyLocation' = 6
    LEGS: 'SSBindingBodyLocation' = 7

    @classmethod
    def get_all(cls) -> Tuple['SSBindingBodyLocation']:
        """ Get all body location values. """
        return tuple(cls.values)

    @staticmethod
    def get_by_name(name: str) -> 'SSBindingBodyLocation':
        """ Get a value by its name. """
        name = str(name).upper().strip()
        value: SSBindingBodyLocation = CommonResourceUtils.get_enum_by_name(name, SSBindingBodyLocation, default_value=SSBindingBodyLocation.NONE)
        return value
