"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from cnsimsnatcher.settings.data.manager import SSSettingsManager
from sims.sim_info import SimInfo
from sims4communitylib.utils.sims.common_age_species_utils import CommonAgeSpeciesUtils


class SSSettingUtils:
    """ Utilities to get SS settings. """
    @staticmethod
    def is_enabled_for_interactions(sim_info: SimInfo) -> bool:
        """is_enabled_for_interactions(sim_info)

        Determine if a Sim is enabled to use the Sim Snatcher interactions.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is enabled for interactions. False, if not.
        :rtype: bool
        """
        return CommonAgeSpeciesUtils.is_teen_adult_or_elder_human(sim_info)

    @staticmethod
    def disclaimer_has_been_shown() -> bool:
        """ Determine if the disclaimer has been shown already. """
        from cnsimsnatcher.settings.settings import SSSetting
        return SSSettingUtils._get_settings_manager().get_setting(SSSetting.ABDUCTION_DISCLAIMER_SHOWN, variable_type=bool)

    @staticmethod
    def flag_disclaimer_as_shown() -> None:
        """ Flag the disclaimer as shown already so it no longer shows. """
        from cnsimsnatcher.settings.settings import SSSetting
        SSSettingUtils._get_settings_manager().set_setting(SSSetting.ABDUCTION_DISCLAIMER_SHOWN, 1)

    @staticmethod
    def interactions_are_enabled() -> bool:
        """ Determine if abduction interactions are enabled. """
        from cnsimsnatcher.settings.settings import SSSetting
        return SSSettingUtils._get_settings_manager().get_setting(SSSetting.ABDUCTION_INTERACTIONS_SWITCH, variable_type=bool)

    class Cheats:
        """ Cheats. """
        @staticmethod
        def always_successful() -> bool:
            """ Determine if attempted abductions will always succeed. """
            from cnsimsnatcher.settings.settings import SSSetting
            return SSSettingUtils._get_settings_manager().get_setting(SSSetting.ABDUCTION_ALWAYS_SUCCESSFUL_SWITCH, variable_type=bool)

        @staticmethod
        def should_show_debug_interactions_for_perform_interaction() -> bool:
            """ Determine if debug interactions should be filtered out of the Perform Interaction order. """
            from cnsimsnatcher.settings.settings import SSSetting
            return SSSettingUtils._get_settings_manager().get_setting(SSSetting.SHOW_DEBUG_INTERACTIONS_FOR_PERFORM_INTERACTION_ORDER, variable_type=bool)

    @staticmethod
    def _get_settings_manager() -> SSSettingsManager:
        from cnsimsnatcher.data_management.data_manager_utils import SSDataManagerUtils
        return SSDataManagerUtils.get_mod_settings_manager()
