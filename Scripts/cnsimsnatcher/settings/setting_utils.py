"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims.sim_info import SimInfo
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.sims.common_age_species_utils import CommonAgeSpeciesUtils
from ssutilities.commonlib.data_management.common_settings_manager import CommonSettingsManager


class SSSettingUtils(CommonService):
    """ Utilities to get SS settings. """
    def __init__(self) -> None:
        super().__init__()
        from cnsimsnatcher.data_management.data_manager_utils import SSDataManagerUtils
        self._settings_manager = SSDataManagerUtils().get_global_mod_settings_manager()
        self.cheats = SSSettingUtils.Cheats(self._settings_manager)

    def is_enabled_for_interactions(self, sim_info: SimInfo) -> bool:
        """is_enabled_for_interactions(sim_info)

        Determine if a Sim is enabled to use the Sim Snatcher interactions.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is enabled for interactions. False, if not.
        :rtype: bool
        """
        return CommonAgeSpeciesUtils.is_teen_adult_or_elder_human(sim_info)

    def disclaimer_has_been_shown(self) -> bool:
        """ Determine if the disclaimer has been shown already. """
        from cnsimsnatcher.settings.settings import SSSetting
        return self._settings_manager.get_setting(SSSetting.ORDER_TO_DISCLAIMER_SHOWN, variable_type=bool)

    def flag_disclaimer_as_shown(self) -> None:
        """ Flag the disclaimer as shown already so it no longer shows. """
        from cnsimsnatcher.settings.settings import SSSetting
        self._settings_manager.set_setting(SSSetting.ORDER_TO_DISCLAIMER_SHOWN, 1)

    class Cheats(CommonService):
        """ Cheat settings. """
        def __init__(self, settings_manager: CommonSettingsManager) -> None:
            super().__init__()
            self._settings_manager = settings_manager

        def should_show_debug_interactions_for_perform_interaction(self) -> bool:
            """ Determine if debug interactions should be filtered out of the Perform Interaction order. """
            from cnsimsnatcher.settings.settings import SSSetting
            return self._settings_manager.get_setting(SSSetting.SHOW_DEBUG_INTERACTIONS_FOR_PERFORM_INTERACTION_ORDER, variable_type=bool)
