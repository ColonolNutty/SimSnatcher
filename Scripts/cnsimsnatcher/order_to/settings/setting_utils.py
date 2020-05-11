"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.services.common_service import CommonService
from ssutilities.commonlib.data_management.common_settings_manager import CommonSettingsManager


class SSOrderToSettingUtils(CommonService):
    """ Utilities to get SS Order To settings. """
    def __init__(self) -> None:
        super().__init__()
        from cnsimsnatcher.data_management.data_manager_utils import SSDataManagerUtils
        self._settings_manager = SSDataManagerUtils().get_order_to_mod_settings_manager()
        self.cheats = SSOrderToSettingUtils.Cheats(self._settings_manager)

    def disclaimer_has_been_shown(self) -> bool:
        """ Determine if the disclaimer has been shown already. """
        from cnsimsnatcher.order_to.settings.settings import SSOrderToSetting
        return self._settings_manager.get_setting(SSOrderToSetting.ORDER_TO_DISCLAIMER_SHOWN, variable_type=bool)

    def flag_disclaimer_as_shown(self) -> None:
        """ Flag the disclaimer as shown already so it no longer shows. """
        from cnsimsnatcher.order_to.settings.settings import SSOrderToSetting
        self._settings_manager.set_setting(SSOrderToSetting.ORDER_TO_DISCLAIMER_SHOWN, 1)

    class Cheats(CommonService):
        """ Cheat settings. """
        def __init__(self, settings_manager: CommonSettingsManager) -> None:
            super().__init__()
            self._settings_manager = settings_manager

        def should_show_debug_interactions_for_perform_interaction(self) -> bool:
            """ Determine if debug interactions should be filtered out of the Perform Interaction order. """
            from cnsimsnatcher.order_to.settings.settings import SSOrderToSetting
            return self._settings_manager.get_setting(SSOrderToSetting.SHOW_DEBUG_INTERACTIONS_FOR_PERFORM_INTERACTION_ORDER, variable_type=bool)
