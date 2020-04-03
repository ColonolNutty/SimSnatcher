"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Dict, Any
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.logging.has_log import HasLog


class CommonDataManager(HasLog):
    """ Manage a storage of data. """
    def __init__(self: 'CommonDataManager'):
        super().__init__()
        self._storage = None
        self._loaded = False

    @property
    def name(self) -> str:
        """The name of the data manager.

        :return: The name of the data manager.
        :rtype: str
        """
        raise NotImplementedError('Missing name.')

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        raise NotImplementedError('Missing \'{}\'.'.format(self.__class__.mod_identity.__name__))

    @property
    def identifier(self) -> str:
        """The identity of the data storage.

        :return: The identity of the data storage.
        :rtype: str
        """
        return CommonDataManager._format_identifier(self.mod_identity)

    @property
    def loaded(self) -> bool:
        """Determine if data has been loaded.

        :return: True, if the data has been loaded. False, if not.
        :rtype: bool
        """
        return self._loaded

    @property
    def _storage(self) -> Dict[str, Any]:
        if not self._loaded:
            self.load()
        return self.__storage

    @_storage.setter
    def _storage(self, value: Dict[str, Any]):
        self.__storage = value

    def set_data(self, key: str, value: Any):
        """set_data(key, value)

        Set data in storage.

        :param key: The name of the data.
        :type key: str
        :param value: The value being set.
        :type value: Any
        """
        self.log.format_with_message('Setting data \'{}\''.format(key), value=value)
        self._storage[key] = value

    def get_data(self, key: str, default_value: Any=None) -> Any:
        """get_data(key, default_value=None)

        Get data from storage.

        :param key: The name of the data.
        :type key: str
        :param default_value: If data is not found using key, this value will be returned. Default is None.
        :type default_value: Any, optional
        :return: The value of the data.
        :rtype: Any
        """
        self.log.format_with_message('Getting data \'{}\''.format(key), default_value=default_value)
        if key not in self._storage:
            self._storage[key] = default_value
        return self._storage[key]

    def remove_data(self, key: str) -> bool:
        """remove_data(key)

        Remove data from storage.

        :param key: The name of the data.
        :type key: str
        :return: True, if the data was successfully removed. False, if not.
        :rtype: bool
        """
        if key not in self._storage:
            return False
        del self._storage[key]
        return True

    def load(self) -> None:
        """load()

        Load data into storage.

        """
        try:
            self.log.debug('Loading data.')
            self._loaded = False
            self._storage = self._load()
            self._loaded = True
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_identity.name, 'Error occurred while loading data \'{}\'.'.format(self.identifier), exception=ex)

    def save(self) -> bool:
        """save()

        Save data from storage.

        :return: True, if save was successful. False, if not.
        :rtype: bool
        """
        try:
            self.log.debug('Saving data.')
            return self._save()
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_identity.name, 'Error occurred while saving data store \'{}\'.'.format(self.identifier), exception=ex)
        return False

    def _load(self) -> Dict[str, Any]:
        raise NotImplementedError('\'{}\' of class \'{}\' not implemented.'.format(self.__class__._load.__name__, self.__class__.__name__))

    def _save(self) -> bool:
        raise NotImplementedError('\'{}\' of class \'{}\' not implemented.'.format(self.__class__._save.__name__, self.__class__.__name__))

    def __repr__(self) -> str:
        return self.identifier

    def __str__(self) -> str:
        return 'Data Manager: \'{}\'\n Storage:\n{}'.format(str(self.mod_identity), self._storage)

    @staticmethod
    def _format_identifier(mod_identity: CommonModIdentity):
        return repr(mod_identity)
