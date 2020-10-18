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
    EYES_BOTH: 'SSBindingBodyLocation' = 1
    EYES_LEFT: 'SSBindingBodyLocation' = 2
    EYES_RIGHT: 'SSBindingBodyLocation' = 3
    MOUTH: 'SSBindingBodyLocation' = 4
    FEET_BOTH: 'SSBindingBodyLocation' = 5
    FEET_LEFT: 'SSBindingBodyLocation' = 6
    FEET_RIGHT: 'SSBindingBodyLocation' = 7
    WRISTS_BOTH: 'SSBindingBodyLocation' = 8
    WRISTS_LEFT: 'SSBindingBodyLocation' = 9
    WRISTS_RIGHT: 'SSBindingBodyLocation' = 10
    ARMS_BOTH: 'SSBindingBodyLocation' = 11
    ARMS_LEFT: 'SSBindingBodyLocation' = 12
    ARMS_RIGHT: 'SSBindingBodyLocation' = 13
    ANKLES_BOTH: 'SSBindingBodyLocation' = 14
    ANKLES_LEFT: 'SSBindingBodyLocation' = 15
    ANKLES_RIGHT: 'SSBindingBodyLocation' = 16
    LEGS_BOTH: 'SSBindingBodyLocation' = 17
    LEGS_LEFT: 'SSBindingBodyLocation' = 18
    LEGS_RIGHT: 'SSBindingBodyLocation' = 19

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
