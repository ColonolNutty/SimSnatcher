"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Dict

from cnsimsnatcher.abduction.settings.settings import SSAbductionSetting
from cnsimsnatcher.modinfo import ModInfo
from cnsimsnatcher.settings.settings import SSSetting
from ssutilities.commonlib.data_management.common_settings_manager import CommonSettingsManager
from sims4communitylib.mod_support.mod_identity import CommonModIdentity


class SSAbductionSettingsManager(CommonSettingsManager):
    """ Manager of settings for SS Abduction. """
    IDENTIFIER = 'ss_abduction_settings'
    MOD_IDENTITY = ModInfo.get_identity()

    @property
    def name(self) -> str:
        """ The name of the data manager. """
        return SSAbductionSettingsManager.IDENTIFIER

    @property
    def mod_identity(self) -> CommonModIdentity:
        """ The Identity of the mod that owns this class. """
        return SSAbductionSettingsManager.MOD_IDENTITY

    @property
    def log_identifier(self) -> str:
        """ An identifier for the Log of this class. """
        return 'ss_abduction_mod_settings_manager'

    @property
    def _version(self) -> int:
        return 1

    @property
    def _default_data(self) -> Dict[str, Any]:
        """ Default Settings. """
        return {
            SSAbductionSetting.VERSION: self._version,

            # Main
            SSAbductionSetting.ABDUCTION_INTERACTIONS_SWITCH: 1,

            # Cheats
            SSAbductionSetting.ABDUCTION_ALWAYS_SUCCESSFUL_SWITCH: 0
        }.copy()
