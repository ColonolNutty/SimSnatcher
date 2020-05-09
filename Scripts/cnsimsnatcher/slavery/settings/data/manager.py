"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Dict
from cnsimsnatcher.modinfo import ModInfo
from cnsimsnatcher.slavery.settings.settings import SSSlaverySetting
from ssutilities.commonlib.data_management.common_settings_manager import CommonSettingsManager
from sims4communitylib.mod_support.mod_identity import CommonModIdentity


class SSSlaverySettingsManager(CommonSettingsManager):
    """ Manager of settings for SS. """
    IDENTIFIER = 'ss_slavery_settings'
    MOD_IDENTITY = ModInfo.get_identity()

    @property
    def name(self) -> str:
        """ The name of the data manager. """
        return SSSlaverySettingsManager.IDENTIFIER

    @property
    def mod_identity(self) -> CommonModIdentity:
        """ The Identity of the mod that owns this class. """
        return SSSlaverySettingsManager.MOD_IDENTITY

    @property
    def log_identifier(self) -> str:
        """ An identifier for the Log of this class. """
        return 'ss_slavery_mod_settings_manager'

    @property
    def _version(self) -> int:
        return 1

    @property
    def _default_data(self) -> Dict[str, Any]:
        """ Default Settings. """
        return {
            SSSlaverySetting.VERSION: self._version,

            # General
            SSSlaverySetting.SLAVERY_INTERACTIONS_SWITCH: 1
        }.copy()
