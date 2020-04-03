"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Type, Tuple, Dict, Union
from ssutilities.commonlib.data_management.common_persisted_data_manager import CommonPersistedDataManager
from sims4communitylib.mod_support.mod_identity import CommonModIdentity


class CommonSettingsManager(CommonPersistedDataManager):
    """CommonSettingsManager()

    Manage settings.

    """
    def __init__(self: 'CommonSettingsManager', *_, **__):
        super().__init__(*_, **__)

    # noinspection PyMissingOrEmptyDocstring
    @property
    def name(self) -> str:
        raise NotImplementedError('Missing \'{}\'.'.format(self.__class__.name.__name__))

    @property
    def _version(self) -> int:
        raise NotImplementedError('Missing \'{}\'.'.format(self.__class__._version.__name__))

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        raise NotImplementedError('Missing \'{}\'.'.format(self.__class__.mod_identity.__name__))

    @property
    def _default_data(self) -> Dict[str, Any]:
        raise NotImplementedError('\'{}\' not implemented'.format(self.__class__._default_data.__name__))

    @property
    def settings(self) -> Dict[str, Any]:
        """Settings.

        :return: A dictionary of settings.
        :rtype: Dict[str, Any]
        """
        return super()._storage

    @settings.setter
    def settings(self, value: Dict[str, Any]):
        super()._storage = value

    def remove_settings(self) -> bool:
        """remove_settings()

        Remove settings from storage.

        :return: True, if settings were successfully removed. False, if not.
        :rtype: bool
        """
        return super().remove()

    def set_setting(self, key: str, value: Any):
        """set_setting(key, value)

        Set a setting.

        :param key: The name of the setting.
        :type key: str
        :param value: The value being set.
        :type value: Any
        """
        self.settings[key] = value

    def get_setting(self, key: str, variable_type: Type=None) -> Any:
        """get_setting(key, variable_type=None)

        Get the value of a setting.

        :param key: The name of the setting.
        :type key: str
        :param variable_type: The type of the setting. Default is None.
        :type variable_type: Type, optional
        :return: The value of the setting.
        :rtype: Any
        :exception AttributeError: When the setting with the specified key is not found.
        """
        if key not in self.settings:
            setting_value = self._locate_backwards_compatible_setting(key)
            if not setting_value:
                raise AttributeError('No setting was found with key \'{}\''.format(key))
            self.set_setting(key, setting_value)
        if variable_type is None:
            return self.settings[key]
        return variable_type(self.settings[key])

    def get_default_setting(self, key: str, variable_type: Type=None) -> Any:
        """get_default_setting(key, variable_type=None)

        Get the default value of a setting.

        :param key: The name of the setting.
        :type key: str
        :param variable_type: The type of the setting. Default is None.
        :type variable_type: Type, optional
        :return: The value of the setting.
        :rtype: Any
        :exception AttributeError: When no default value for the setting with the specified key is found.
        """
        if key not in self._default_data:
            raise AttributeError('No default setting was found with key \'{}\''.format(key))
        if variable_type is None:
            return self._default_data[key]
        return variable_type(self._default_data[key])

    def _is_backwards_compatible(self, key: str) -> bool:
        return key in self._backwards_compatible_setting_keys

    def _locate_backwards_compatible_setting(self, key: str) -> Union[Any, None]:
        if not self._is_backwards_compatible(key):
            return None
        backwards_compatible_keys = self._backwards_compatible_setting_keys[key]
        for _key in backwards_compatible_keys:
            if _key not in self.settings:
                continue
            return self.settings[_key]
        return None

    @property
    def _backwards_compatible_setting_keys(self) -> Dict[str, Tuple[str]]:
        """_backwards_compatible_setting_keys()

        A dictionary containing backwards compatible names.

        :Example:

            When looking for a setting with the name 'new_setting_name', we will also attempt to locate
             'old_setting_name_1' and 'old_setting_name_2' in case they exist.
            {
                'new_setting_name': ['old_setting_name_1', 'old_setting_name_2']
            }

        :return: A dictionary mapping new setting names to old setting names.
        :rtype: Dict[str, Tuple[str]]
        """
        return dict()
