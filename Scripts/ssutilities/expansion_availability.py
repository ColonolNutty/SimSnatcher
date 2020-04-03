"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import List
from sims4communitylib.services.common_service import CommonService

# noinspection PyBroadException
try:
    # noinspection PyUnresolvedReferences
    from enum import Int
except:
    # noinspection PyMissingOrEmptyDocstring
    class Int:
        pass


class CommonExpansionId(Int):
    """Identifiers for Sims 4 Expansions.
    For Use with :class:`.CommonExpansionAvailability`

    """
    CATS_AND_DOGS_DLC = 4


class CommonExpansionAvailabilityService(CommonService):
    """A utility used to determine expansion availability.

    """
    def __init__(self: 'CommonExpansionAvailabilityService'):
        self._available_expansions: List[int] = []

    def register_expansion_as_available(self, expansion_id: int):
        """Register a DLC as available.

        :param expansion_id: The identifier of the expansion to register.
        :type expansion_id: int
        """
        return self._available_expansions.append(expansion_id)

    def cats_and_dogs_expansion_is_available(self) -> bool:
        """cats_and_dogs_is_available()

        Determine if the Cats & Dogs Expansion is available.

        :return: True, if the expansion is available. False, if not.
        :rtype: bool
        """
        return self.expansion_is_available(CommonExpansionId.CATS_AND_DOGS_DLC)

    def expansion_is_available(self, expansion_id: int) -> bool:
        """is_available(expansion_id)

        Determine if the specified expansion is available.

        :param expansion_id: The expansion to locate.
        :type expansion_id: int
        :return: True, if the expansion is available. False, if not.
        :rtype: bool
        """
        return expansion_id in self._available_expansions


# Cats & Dogs DLC
try:
    from sims.sim_info_types import SpeciesExtended
    CommonExpansionAvailabilityService.get().register_expansion_as_available(CommonExpansionId.CATS_AND_DOGS_DLC)
except ModuleNotFoundError:
    pass
