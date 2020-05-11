"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from cnsimsnatcher.modinfo import ModInfo
from cnsimsnatcher.settings.setting_utils import SSSettingUtils
from sims.sim_info import SimInfo
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.services.common_service import CommonService


class SSAbductionUtils(CommonService, HasLog):
    """ Generic Utilities used by SS Abduction. """

    def __init__(self) -> None:
        super().__init__()
        self._setting_utils = SSSettingUtils()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'ssa_utils'

    def can_engage_in_abduction(self, sim_info: SimInfo) -> bool:
        """ Determine if a Sim can engage in abduction. """
        if not self._setting_utils.is_enabled_for_interactions(sim_info):
            return False
        return self.is_allowed_to_abduct_others(sim_info)\
               or self.is_allowed_to_be_abducted(sim_info)

    def can_engage_in_abduction_autonomously(self, sim_info: SimInfo) -> bool:
        """ Determine if a Sim can assault autonomously."""
        return self.can_engage_in_abduction(sim_info)

    def is_allowed_to_abduct_others(self, sim_info: SimInfo) -> bool:
        """ Determine if a Sim is allowed to abduct other Sims. """
        return self._setting_utils.is_enabled_for_interactions(sim_info)

    def is_allowed_to_be_abducted(self, sim_info: SimInfo) -> bool:
        """ Determine if a Sim is allowed to be abducted by other Sims. """
        return self._setting_utils.is_enabled_for_interactions(sim_info)
