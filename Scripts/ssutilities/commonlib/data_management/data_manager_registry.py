"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Dict, Tuple
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.zone_spin.events.zone_save import S4CLZoneSaveEvent
from sims4communitylib.logging.has_class_log import HasClassLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.services.common_service import CommonService
from ssutilities.commonlib.data_management.common_data_manager import CommonDataManager
from ssutilities.modinfo import ModInfo


class CommonDataManagerRegistry(CommonService, HasClassLog):
    """ Load/unload save data. """

    def __init__(self: 'CommonDataManagerRegistry') -> None:
        super().__init__()
        self._data_managers: Dict[str, Dict[str, CommonDataManager]] = {}

    @property
    def data_managers(self) -> Dict[str, Dict[str, CommonDataManager]]:
        """ Data managers. """
        return self._data_managers

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'common_data_manager'

    @staticmethod
    def register_data_manager(data_manager: CommonDataManager):
        """ Register a new data manager. """
        CommonDataManagerRegistry.get_log().format_with_message('Registering data store.', data_store=data_manager)
        CommonDataManagerRegistry.get()._register_data_manager(data_manager)

    def _register_data_manager(self, data_manager: CommonDataManager):
        if data_manager.identifier not in self.data_managers:
            self.data_managers[data_manager.identifier] = dict()
        if data_manager.name not in self.data_managers[data_manager.identifier]:
            self.data_managers[data_manager.identifier][data_manager.name] = data_manager

    def load_data(self) -> None:
        """ Load data of all data. """
        self.log.debug('Initializing data managers.')
        for data_store_store in self.data_managers.values():
            for data_store in data_store_store.values():
                self.log.format_with_message('Loading data manager', data_store=data_store)
                data_store.load()
        self.log.debug('Done initializing data managers.')

    def save_data(self) -> None:
        """ Save data of all data. """
        self.log.debug('Saving data managers.')
        for data_store_store in self.data_managers.values():
            for data_store in data_store_store.values():
                self.log.format_with_message('Saving data manager', data_store=data_store)
                data_store.save()
        self.log.debug('Done saving data managers.')

    def get_data_managers(self, mod_identity: CommonModIdentity) -> Tuple[CommonDataManager]:
        """ Retrieve all data managers for a mod. """
        formatted_identifier = CommonDataManager._format_identifier(mod_identity)
        self.log.format_with_message('Attempting to retrieve data manager names', identifier=formatted_identifier)
        if formatted_identifier not in self.data_managers:
            self.log.format_with_message('No data managers registered \'{}\'.'.format(str(mod_identity)))
            return tuple()
        return tuple(self.data_managers[formatted_identifier].values())

    def get_data_manager_names(self, mod_identity: CommonModIdentity) -> Tuple[str]:
        """ Retrieve the names of all data managers of a mod. """
        formatted_identifier = CommonDataManager._format_identifier(mod_identity)
        self.log.format_with_message('Attempting to retrieve data manager names', identifier=formatted_identifier)
        if formatted_identifier not in self.data_managers:
            self.log.format_with_message('No data managers registered \'{}\'.'.format(str(mod_identity)))
            return tuple()
        return tuple(self.data_managers[formatted_identifier].keys())

    def locate_data_manager(self, mod_identity: CommonModIdentity, data_manager_identifier: str) -> Union[CommonDataManager, None]:
        """ Retrieve a data manager by mod and identifier. """
        formatted_identifier = CommonDataManager._format_identifier(mod_identity)
        self.log.format_with_message('Attempting to locate data manager.', identifier=formatted_identifier)
        if formatted_identifier not in self.data_managers:
            self.log.format_with_message('No data managers registered \'{}\'.'.format(str(mod_identity)))
            return None
        if data_manager_identifier not in self.data_managers[formatted_identifier]:
            self.log.format_with_message('No data manager with name \'{}\'.'.format(data_manager_identifier))
            return None
        self.log.debug('Located data manager.')
        return self.data_managers[formatted_identifier][data_manager_identifier]


# noinspection PyUnusedLocal
@CommonEventRegistry.handle_events(ModInfo.get_identity())
def _common_save_data_on_zone_save(event_data: S4CLZoneSaveEvent) -> bool:
    CommonDataManagerRegistry.get().save_data()
    return True
