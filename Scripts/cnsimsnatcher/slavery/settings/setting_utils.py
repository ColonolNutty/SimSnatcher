"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from cnsimsnatcher.slavery.settings.data.data_store import SSSlaverySettingsDataStore
from cnsimsnatcher.slavery.settings.settings import SSSlaverySetting
from sims4communitylib.services.common_service import CommonService


class SSSlaverySettingUtils(CommonService):
    """ Utilities to get SS Slavery settings. """
    def __init__(self) -> None:
        from cnsimsnatcher.persistence.ss_data_manager_utils import SSDataManagerUtils
        self._data_store = SSDataManagerUtils().get_slavery_mod_settings_data_store()
        self.main = SSSlaverySettingUtils.Main(self._data_store)
        self.cheats = SSSlaverySettingUtils.Cheats(self._data_store)

    def interactions_are_enabled(self) -> bool:
        """ Determine if interactions are enabled. """
        return self._data_store.get_value_by_key(SSSlaverySetting.SLAVERY_INTERACTIONS_SWITCH)

    class Main(CommonService):
        """ Main settings. """
        def __init__(self, data_store: SSSlaverySettingsDataStore) -> None:
            super().__init__()
            self._data_store = data_store

        def get_chance_to_succeed(self) -> float:
            """ Retrieve the chance of an Attempt To Enslave being successful. """
            return float(self._data_store.get_value_by_key(SSSlaverySetting.ATTEMPT_TO_ENSLAVE_SUCCESS_CHANCE))

    class Cheats(CommonService):
        """ Cheat settings. """
        def __init__(self, data_store: SSSlaverySettingsDataStore) -> None:
            super().__init__()
            self._data_store = data_store

        def always_successful(self) -> bool:
            """ Determine if Attempts to Enslave will always succeed. """
            return self._data_store.get_value_by_key(SSSlaverySetting.ATTEMPT_TO_ENSLAVE_ALWAYS_SUCCESSFUL)
