"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Type, Union, Dict, Any

from cnsimsnatcher.abduction.settings.data.data_store import SSAbductionSettingsDataStore
from cnsimsnatcher.modinfo import ModInfo
from cnsimsnatcher.order_to.settings.data.data_store import SSOrderToSettingsDataStore
from cnsimsnatcher.persistence.ss_data_manager import SSDataManager
from cnsimsnatcher.settings.data.data_store import SSGlobalSettingsDataStore
from cnsimsnatcher.slavery.settings.data.data_store import SSSlaverySettingsDataStore
from sims4communitylib.persistence.data_management.common_data_manager_registry import CommonDataManagerRegistry
from sims4communitylib.persistence.data_stores.common_data_store import CommonDataStore
from sims4communitylib.persistence.data_stores.common_sim_data_store import CommonSimDataStore
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4.commands import Command, CommandType, CheatOutput


class SSDataManagerUtils(CommonService):
    """ Utilities for accessing data stores """
    def __init__(self) -> None:
        self._data_manager: SSDataManager = None

    @property
    def data_manager(self) -> SSDataManager:
        """ The data manager containing data for SS. """
        if self._data_manager is None:
            self._data_manager: SSDataManager = CommonDataManagerRegistry().locate_data_manager(ModInfo.get_identity())
        return self._data_manager

    def get_global_mod_settings_data_store(self) -> SSGlobalSettingsDataStore:
        """ Retrieve the Global Mod Settings Data Store. """
        data_store: SSGlobalSettingsDataStore = self._get_data_store(SSGlobalSettingsDataStore)
        return data_store

    def get_abduction_mod_settings_data_store(self) -> SSAbductionSettingsDataStore:
        """ Retrieve the Abduction Mod Settings Data Store. """
        data_store: SSAbductionSettingsDataStore = self._get_data_store(SSAbductionSettingsDataStore)
        return data_store

    def get_order_to_mod_settings_data_store(self) -> SSOrderToSettingsDataStore:
        """ Retrieve the Order To Mod Settings Data Store. """
        data_store: SSOrderToSettingsDataStore = self._get_data_store(SSOrderToSettingsDataStore)
        return data_store

    def get_slavery_mod_settings_data_store(self) -> SSSlaverySettingsDataStore:
        """ Retrieve the Slavery Mod Settings Data Store. """
        data_store: SSSlaverySettingsDataStore = self._get_data_store(SSSlaverySettingsDataStore)
        return data_store

    def get_sim_data_store(self) -> CommonSimDataStore:
        """ Retrieve the Sim Data Store. """
        data_store: CommonSimDataStore = self._get_data_store(CommonSimDataStore)
        return data_store

    def _get_data_store(self, data_store_type: Type[CommonDataStore]) -> Union[CommonDataStore, None]:
        return self.data_manager.get_data_store_by_type(data_store_type)

    def get_all_data(self) -> Dict[str, Dict[str, Any]]:
        """ Get all data. """
        return self.data_manager._data_store_data

    def save(self) -> bool:
        """ Save data. """
        return self.data_manager.save()

    def reset(self, prevent_save: bool=False) -> bool:
        """ Reset data. """
        return self.data_manager.remove_all_data(prevent_save=prevent_save)


log = CommonLogRegistry().register_log(ModInfo.get_identity(), 'ss.print_mod_data')


@Command('ss.print_mod_data', command_type=CommandType.Live)
def _ss_command_print_mod_data(_connection: int=None):
    output = CheatOutput(_connection)
    output('Printing SS Mod Data to Messages.txt file. This may take a little bit, be patient.')
    log.enable()
    log.format(data_store_data=SSDataManagerUtils().get_all_data())
    log.disable()
    output('Done')


@Command('ss.clear_mod_data', command_type=CommandType.Live)
def _ss_command_clear_global_settings(_connection: int=None):
    output = CheatOutput(_connection)
    output('Clearing SS Mod Data.')
    SSDataManagerUtils().reset(prevent_save=True)
    output('!!! PLEASE READ !!!')
    output('Settings reset to default. Please restart your game without saving.')
    output('!!!!!!!!!!!!!!!!!!!')
