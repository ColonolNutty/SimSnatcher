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
        from cnsimsnatcher.data_management.data_manager_utils import SSDataManagerUtils
        self._settings_manager = SSDataManagerUtils().get_slavery_mod_settings_manager()

    def interactions_are_enabled(self) -> bool:
        """ Determine if slavery interactions are enabled. """
        return self._settings_manager.get_setting(SSSlaverySetting.SLAVERY_INTERACTIONS_SWITCH, variable_type=bool)
