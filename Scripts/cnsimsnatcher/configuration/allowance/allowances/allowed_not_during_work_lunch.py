"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Set

from cnsimsnatcher.configuration.allowance.allowances.allowance import SSAllowanceData
from cnsimsnatcher.configuration.allowance.enums.string_ids import SSAllowanceStringId
from cnsimsnatcher.configuration.allowance.enums.trait_ids import SSAllowanceTraitId
from sims4communitylib.enums.tags_enum import CommonGameTag
from tag import Tag


class SSAllowedNotDuringWorkLunch(SSAllowanceData):
    """ Data for an allowance. """

    # noinspection PyMissingOrEmptyDocstring
    @property
    def title(self) -> int:
        return SSAllowanceStringId.ALLOWED_NOT_DURING_WORK_LUNCH

    # noinspection PyMissingOrEmptyDocstring
    @property
    def trait_id(self) -> int:
        return SSAllowanceTraitId.ALLOWED_NOT_DURING_WORK_LUNCH

    # noinspection PyMissingOrEmptyDocstring
    @property
    def appropriateness_tags(self) -> Set[Tag]:
        return {
            CommonGameTag.APPROPRIATENESS_NOT_DURING_WORK_LUNCH
        }