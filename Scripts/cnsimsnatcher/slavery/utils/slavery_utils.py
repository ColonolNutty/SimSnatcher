"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from cnsimsnatcher.modinfo import ModInfo
from cnsimsnatcher.settings.setting_utils import SSSettingUtils
from sims.sim_info import SimInfo
from sims4communitylib.utils.common_log_registry import CommonLogRegistry

log = CommonLogRegistry.get().register_log(ModInfo.get_identity(), 'ss_slavery_utils')


class SSSlaveryUtils:
    """ Generic Utilities used by SS Slavery. """
    def can_engage_in_slavery(self, sim_info: SimInfo) -> bool:
        """ Determine if a sim can engage in slavery. """
        if not SSSettingUtils().is_enabled_for_interactions(sim_info):
            return False
        return self.is_allowed_to_enslave_others(sim_info)\
               or self.is_allowed_to_be_enslaved(sim_info)

    def can_engage_in_slavery_autonomously(self, sim_info: SimInfo) -> bool:
        """ Determine if a sim can assault autonomously."""
        return self.can_engage_in_slavery(sim_info)

    def is_allowed_to_enslave_others(self, sim_info: SimInfo) -> bool:
        """ Determine if a sim is allowed to enslave other sims. """
        return SSSettingUtils().is_enabled_for_interactions(sim_info)

    def is_allowed_to_be_enslaved(self, sim_info: SimInfo) -> bool:
        """ Determine if a sim is allowed to be enslaved by other sims. """
        return SSSettingUtils().is_enabled_for_interactions(sim_info)
