"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from cnsimsnatcher.order_to.settings.data.manager import SSOrderToSettingsManager
from ssutilities.commonlib.data_management.data_manager_registry import CommonDataManagerRegistry
from cnsimsnatcher.abduction.settings.data.manager import SSAbductionSettingsManager
from cnsimsnatcher.settings.data.manager import SSSettingsManager
from cnsimsnatcher.slavery.settings.data.manager import SSSlaverySettingsManager
from sims4communitylib.services.common_service import CommonService


class SSDataManagerUtils(CommonService):
    """ Utilities for accessing data managers for SS """

    def __init__(self) -> None:
        super().__init__()
        self._global_mod_settings_manager: SSSettingsManager = None
        self._slavery_mod_settings_manager: SSSlaverySettingsManager = None
        self._abduction_mod_settings_manager: SSAbductionSettingsManager = None
        self._order_to_mod_settings_manager: SSOrderToSettingsManager = None

    def get_global_mod_settings_manager(self) -> SSSettingsManager:
        """ Retrieve the Global Settings Manager. """
        if self._global_mod_settings_manager is None:
            self._global_mod_settings_manager: SSSettingsManager = CommonDataManagerRegistry.get()\
                .locate_data_manager(
                    SSSettingsManager.MOD_IDENTITY,
                    SSSettingsManager.IDENTIFIER
                )
        return self._global_mod_settings_manager

    def get_abduction_mod_settings_manager(self) -> SSAbductionSettingsManager:
        """ Retrieve the Abduction Settings Manager. """
        if self._abduction_mod_settings_manager is None:
            self._abduction_mod_settings_manager: SSAbductionSettingsManager = CommonDataManagerRegistry.get()\
                .locate_data_manager(
                    SSAbductionSettingsManager.MOD_IDENTITY,
                    SSAbductionSettingsManager.IDENTIFIER
                )
        return self._abduction_mod_settings_manager

    def get_slavery_mod_settings_manager(self) -> SSSlaverySettingsManager:
        """ Retrieve the Slavery Settings Manager. """
        if self._slavery_mod_settings_manager is None:
            self._slavery_mod_settings_manager: SSSlaverySettingsManager = CommonDataManagerRegistry.get()\
                .locate_data_manager(
                    SSSlaverySettingsManager.MOD_IDENTITY,
                    SSSlaverySettingsManager.IDENTIFIER
                )
        return self._slavery_mod_settings_manager

    def get_order_to_mod_settings_manager(self) -> SSOrderToSettingsManager:
        """ Retrieve the Order To Settings Manager. """
        if self._order_to_mod_settings_manager is None:
            self._order_to_mod_settings_manager: SSOrderToSettingsManager = CommonDataManagerRegistry.get()\
                .locate_data_manager(
                    SSOrderToSettingsManager.MOD_IDENTITY,
                    SSOrderToSettingsManager.IDENTIFIER
                )
        return self._order_to_mod_settings_manager
