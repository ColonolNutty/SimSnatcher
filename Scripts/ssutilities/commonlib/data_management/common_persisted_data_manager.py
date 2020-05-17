"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import json
from typing import Dict, Any

from sims.household import Household
from ssutilities.commonlib.data_management.common_data_manager import CommonDataManager
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils


class CommonPersistedDataManager(CommonDataManager):
    """ Manage data for the current Save. """
    def __init__(self, *_, **__) -> None:
        super().__init__()
        self._can_be_saved = True

    @property
    def _can_be_saved(self) -> bool:
        return self.__can_be_saved

    @_can_be_saved.setter
    def _can_be_saved(self, val: bool):
        self.__can_be_saved = val

    @property
    def name(self) -> str:
        """ The name of the data manager. """
        raise NotImplementedError('Missing name.')

    @property
    def mod_identity(self) -> CommonModIdentity:
        """ The Identity of the mod that owns this class. """
        raise NotImplementedError('Missing mod_identity.')

    @property
    def _version(self) -> int:
        raise NotImplementedError('Missing _version for \'{}\'.'.format(self.__class__.__name__))

    @property
    def _default_data(self) -> Dict[str, Any]:
        """ The default data. """
        raise NotImplementedError('\'{}\' not implemented'.format(self.__class__._default_data.__name__))

    @property
    def _data_name(self) -> str:
        return 'do_not_remove_{}_{}'.format(self.identifier, self.name).lower()

    def _load(self) -> Dict[str, Any]:
        """ Load data from the current Save. """
        self.log.debug('Loading data. \'{}\'.'.format(self.identifier))
        data_name = self._data_name
        self.log.debug('Attempting to locate data \'{}\'.'.format(data_name))
        loaded_data: Dict[str, Any] = None
        loaded_household: Household = None

        def _load_data_from_household(household: Household) -> Dict[str, Any]:
            # noinspection PyPropertyAccess
            self.log.format_with_message('Attempting to read data stored within household. \'{}\''.format(household.name), household_id=household.id)
            # noinspection PyPropertyAccess
            raw_data = household.description
            if not raw_data:
                self.log.format_with_message('No raw data found, returning default data.', data=household)
                return dict()
            self.log.debug('Data found, attempting to parse data.')
            return json.loads(raw_data)

        self.log.debug('Attempting to locate data by exact name \'{}\''.format(data_name))
        located_household = CommonHouseholdUtils.locate_household_by_name(data_name)
        if located_household is not None:
            self.log.debug('Located data with exact name \'{}\'.'.format(data_name))
            loaded_data = _load_data_from_household(located_household)
            if loaded_data is not None:
                loaded_household = located_household

        self.log.debug('Attempting to locate data containing name \'{}\''.format(data_name))
        for persisted_household in CommonHouseholdUtils.locate_households_by_name_generator(data_name, allow_partial_match=True):
            if persisted_household is None or (loaded_household is not None and persisted_household is loaded_household):
                continue
            # noinspection PyPropertyAccess
            household_name = persisted_household.name
            if loaded_data is not None:
                # noinspection PyPropertyAccess
                self.log.format_with_message('Duplicate household found, attempting to remove duplicate. \'{}\''.format(household_name), household_id=persisted_household.id)
                if CommonHouseholdUtils.delete_household(persisted_household):
                    self.log.debug('Successfully deleted duplicate household. \'{}\''.format(household_name))
                else:
                    self.log.debug('Failed to delete duplicate household \'{}\'.'.format(household_name))
                continue
            loaded_data = _load_data_from_household(persisted_household)
            if loaded_data is not None:
                loaded_household = persisted_household

        if loaded_data is None:
            self.log.debug('No persisted data, returning default data.')
            return dict(self._default_data)

        if ('version' not in loaded_data or int(loaded_data['version']) != int(self._version)) and 'version' in self._default_data:
            self.log.debug('Data was outdated, returning loaded data with new data.')
            new_data = dict(loaded_data)
            default_data = dict(self._default_data)
            for default_data_key in default_data.keys():
                # If Data has the key, we don't want to override it. Keep the old data.
                if default_data_key in new_data:
                    continue
                new_data[default_data_key] = default_data[default_data_key]
            return new_data
        self.log.format_with_message('Done loading data \'{}\'.'.format(data_name), data=loaded_data)
        return loaded_data

    def _save(self) -> bool:
        """ Save data to the current Save. """
        if not self._can_be_saved:
            return True
        self.log.format_with_message('Saving data \'{}\'.'.format(self.identifier))
        data_name = self._data_name
        self.log.debug('Attempting to locate data \'{}\'.'.format(data_name))
        persisted_data_storage = CommonHouseholdUtils.locate_household_by_name(data_name)
        if persisted_data_storage is None:
            self.log.debug('No persisted data found, creating new persisted data.')
            persisted_data_storage = CommonHouseholdUtils.create_empty_household(as_hidden_household=True)
            if persisted_data_storage is None:
                self.log.debug('Failed to persisted data.')
                return False
            self.log.debug('Persisted data created successfully. Setting properties.')
            persisted_data_storage.name = data_name
            persisted_data_storage.creator_id = 0
            persisted_data_storage.creator_name = data_name
            persisted_data_storage.creator_uuid = b''
        self.log.format_with_message('Done loading persisted data. Attempting to save data.', data=persisted_data_storage)
        try:
            self.log.format(data_being_saved=self._storage)
            json_save_data = json.dumps(self._storage)
            persisted_data_storage.description = json_save_data
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_identity.name, 'Failed to save data \'{}\'.'.format(data_name), ex)
            raise ex
        self.log.format_with_message('Done saving data \'{}\'.'.format(data_name))
        return True

    def remove(self) -> bool:
        """ Remove data. """
        self.log.format_with_message('Removing data \'{}\'.'.format(self.identifier))
        data_name = self._data_name
        self.log.format_with_message('Attempting to remove data \'{}\'.'.format(data_name))
        result = CommonHouseholdUtils.delete_households_with_name(data_name, allow_partial_match=True)
        if not result:
            self.log.debug('Failed to delete data \'{}\'.'.format(data_name))
            return result
        self.log.debug('Data deleted successfully \'{}\'.'.format(data_name))
        return result

    def reset(self, prevent_save: bool=False):
        """reset(prevent_save=False)

        Reset the data store to default values.

        :param prevent_save: If True, when the game is saved, the data will not be persisted. Default is False.
        :type prevent_save: bool, optional
        """
        try:
            self.remove()
            self._storage = dict(self._default_data)
            if prevent_save:
                self._can_be_saved = False
        except Exception as ex:
            self.log.error('Error while resetting settings.', exception=ex)
