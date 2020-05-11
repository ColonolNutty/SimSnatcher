"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Dict
from cnsimsnatcher.modinfo import ModInfo
from cnsimsnatcher.order_to.settings.settings import SSOrderToSetting
from ssutilities.commonlib.data_management.common_settings_manager import CommonSettingsManager
from sims4communitylib.mod_support.mod_identity import CommonModIdentity


class SSOrderToSettingsManager(CommonSettingsManager):
    """ Manager of settings for SS Order To. """
    IDENTIFIER = 'ss_order_to_settings'
    MOD_IDENTITY = ModInfo.get_identity()

    @property
    def name(self) -> str:
        """ The name of the data manager. """
        return SSOrderToSettingsManager.IDENTIFIER

    @property
    def mod_identity(self) -> CommonModIdentity:
        """ The Identity of the mod that owns this class. """
        return SSOrderToSettingsManager.MOD_IDENTITY

    @property
    def log_identifier(self) -> str:
        """ An identifier for the Log of this class. """
        return 'sso_mod_settings_manager'

    @property
    def _version(self) -> int:
        return 1

    @property
    def _default_data(self) -> Dict[str, Any]:
        """ Default Settings. """
        return {
            SSOrderToSetting.VERSION: self._version,

            # Cheats
            SSOrderToSetting.ORDER_TO_DISCLAIMER_SHOWN: 0,

            # Cheats
            SSOrderToSetting.SHOW_DEBUG_INTERACTIONS_FOR_PERFORM_INTERACTION_ORDER: 0
        }.copy()
