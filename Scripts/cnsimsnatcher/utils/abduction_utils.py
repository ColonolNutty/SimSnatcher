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

log = CommonLogRegistry.get().register_log(ModInfo.get_identity(), 'ss_abduction_utils')


class SSAbductionUtils:
    """ Generic Utilities used by SS Abduction. """
    @staticmethod
    def can_engage_in_abduction(sim_info: SimInfo) -> bool:
        """ Determine if a sim can engage in abduction. """
        if not SSSettingUtils().is_enabled_for_interactions(sim_info):
            return False
        return SSAbductionUtils.is_allowed_to_abduct_others(sim_info)\
               or SSAbductionUtils.is_allowed_to_be_abducted(sim_info)

    @staticmethod
    def can_engage_in_abduction_autonomously(sim_info: SimInfo) -> bool:
        """ Determine if a sim can assault autonomously."""
        return SSAbductionUtils.can_engage_in_abduction(sim_info)

    @staticmethod
    def is_allowed_to_abduct_others(sim_info: SimInfo) -> bool:
        """ Determine if a sim is allowed to abduct other sims. """
        return SSSettingUtils().is_enabled_for_interactions(sim_info)

    @staticmethod
    def is_allowed_to_be_abducted(sim_info: SimInfo) -> bool:
        """ Determine if a sim is allowed to be abducted by other sims. """
        return SSSettingUtils().is_enabled_for_interactions(sim_info)
