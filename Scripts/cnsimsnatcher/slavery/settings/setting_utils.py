"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from cnsimsnatcher.slavery.settings.settings import SSSlaverySetting


class SSSlaverySettingUtils:
    """ Utilities to get SS Slavery settings. """
    def __init__(self) -> None:
        from cnsimsnatcher.persistence.ss_data_manager_utils import SSDataManagerUtils
        self._data_store = SSDataManagerUtils().get_slavery_mod_settings_data_store()

    def interactions_are_enabled(self) -> bool:
        """ Determine if slavery interactions are enabled. """
        return self._data_store.get_value_by_key(SSSlaverySetting.SLAVERY_INTERACTIONS_SWITCH)
