"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Set

from cnsimsnatcher.configuration.allowance.allowances.allowance import SSAllowanceData
from cnsimsnatcher.configuration.allowance.enums.string_ids import SSAllowanceStringId
from sims4communitylib.enums.tags_enum import CommonGameTag


class SSAllowedSinging(SSAllowanceData):
    """ Data for an allowance. """

    # noinspection PyMissingOrEmptyDocstring
    @property
    def title(self) -> int:
        return SSAllowanceStringId.ALLOWED_SINGING

    # noinspection PyMissingOrEmptyDocstring
    @property
    def appropriateness_tags(self) -> Set[CommonGameTag]:
        return {
            CommonGameTag.APPROPRIATENESS_SINGING
        }
