"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.services.common_service import CommonService
from ssutilities.commonlib.data_management.common_settings_manager import CommonSettingsManager


class SSAbductionSettingUtils(CommonService):
    """ Utilities to get SS Abduction settings. """
    def __init__(self) -> None:
        super().__init__()
        from cnsimsnatcher.data_management.data_manager_utils import SSDataManagerUtils
        from cnsimsnatcher.abduction.settings.data.manager import SSAbductionSettingsManager
        self._settings_manager: SSAbductionSettingsManager = SSDataManagerUtils().get_abduction_mod_settings_manager()
        self.cheats = SSAbductionSettingUtils.Cheats(self._settings_manager)

    def interactions_are_enabled(self) -> bool:
        """ Determine if the Abduction interactions are enabled. """
        from cnsimsnatcher.abduction.settings.settings import SSAbductionSetting
        return self._settings_manager.get_setting(SSAbductionSetting.ABDUCTION_INTERACTIONS_SWITCH, variable_type=bool)

    class Cheats(CommonService):
        """ Cheat settings. """
        def __init__(self, settings_manager: CommonSettingsManager) -> None:
            super().__init__()
            self._settings_manager = settings_manager

        def always_successful(self) -> bool:
            """ Determine if Abduction attempts will always succeed. """
            from cnsimsnatcher.abduction.settings.settings import SSAbductionSetting
            return self._settings_manager.get_setting(SSAbductionSetting.ABDUCTION_ALWAYS_SUCCESSFUL_SWITCH, variable_type=bool)
