"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Set

from cnsimsnatcher.configuration.allowance.utils.allowance_utils import SSAllowanceUtils
from cnsimsnatcher.modinfo import ModInfo
from sims4communitylib.enums.tags_enum import CommonGameTag
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.persistence.common_sim_data_storage import CommonSimDataStorage


class SSSimDataStorage(CommonSimDataStorage):
    """ Data storage for SS. """
    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'ss_sim_data_storage'

    @property
    def allowances(self) -> Set[CommonGameTag]:
        """ Retrieve the allowances for the Sim. """
        return self.get_data(default=SSAllowanceUtils().get_appropriateness_tags(self.sim_info))

    @allowances.setter
    def allowances(self, value: Set[CommonGameTag]):
        self.set_data(value)
