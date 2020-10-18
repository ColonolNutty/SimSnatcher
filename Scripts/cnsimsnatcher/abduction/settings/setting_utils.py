"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from cnsimsnatcher.abduction.settings.settings import SSAbductionSetting
from cnsimsnatcher.abduction.settings.data.data_store import SSAbductionSettingsDataStore
from sims4communitylib.services.common_service import CommonService


class SSAbductionSettingUtils(CommonService):
    """ Utilities to get SS Abduction settings. """
    def __init__(self) -> None:
        super().__init__()
        from cnsimsnatcher.persistence.ss_data_manager_utils import SSDataManagerUtils
        self._data_store = SSDataManagerUtils().get_abduction_mod_settings_data_store()
        self.main = SSAbductionSettingUtils.Main(self._data_store)
        self.cheats = SSAbductionSettingUtils.Cheats(self._data_store)

    def interactions_are_enabled(self) -> bool:
        """ Determine if interactions are enabled. """
        return self._data_store.get_value_by_key(SSAbductionSetting.ABDUCTION_INTERACTIONS_SWITCH)

    class Main(CommonService):
        """ Main settings. """
        def __init__(self, data_store: SSAbductionSettingsDataStore) -> None:
            super().__init__()
            self._data_store = data_store

        def get_chance_to_succeed(self) -> float:
            """ Retrieve the chance of an Attempt To Abduct being successful. """
            return float(self._data_store.get_value_by_key(SSAbductionSetting.ATTEMPT_TO_ABDUCT_SUCCESS_CHANCE))

    class Cheats(CommonService):
        """ Cheat settings. """
        def __init__(self, data_store: SSAbductionSettingsDataStore) -> None:
            super().__init__()
            self._data_store = data_store

        def always_successful(self) -> bool:
            """ Determine if Abduction attempts will always succeed. """
            return self._data_store.get_value_by_key(SSAbductionSetting.ATTEMPT_TO_ABDUCT_ALWAYS_SUCCESSFUL)
