"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from cnsimsnatcher.settings.data.manager import SSSettingsManager


class SSDataManagerUtils:
    """ Utilities for accessing data managers for SS """
    _mod_settings_manager: SSSettingsManager = None

    @staticmethod
    def get_mod_settings_manager() -> SSSettingsManager:
        """ Retrieve the Settings Manager. """
        if SSDataManagerUtils._mod_settings_manager is None:
            from ssutilities.commonlib.data_management.data_manager_registry import CommonDataManagerRegistry
            SSDataManagerUtils._mod_settings_manager = CommonDataManagerRegistry.get()\
                .locate_data_manager(
                    SSSettingsManager.MOD_IDENTITY,
                    SSSettingsManager.IDENTIFIER
                )
        return SSDataManagerUtils._mod_settings_manager
