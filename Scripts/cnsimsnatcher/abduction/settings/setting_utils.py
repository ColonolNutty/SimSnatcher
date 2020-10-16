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
        self.cheats = SSAbductionSettingUtils.Cheats(self._data_store)

    def interactions_are_enabled(self) -> bool:
        """ Determine if the Abduction interactions are enabled. """
        return self._data_store.get_value_by_key(SSAbductionSetting.ABDUCTION_INTERACTIONS_SWITCH)

    class Cheats(CommonService):
        """ Cheat settings. """
        def __init__(self, data_store: SSAbductionSettingsDataStore) -> None:
            super().__init__()
            self._data_store = data_store

        def always_successful(self) -> bool:
            """ Determine if Abduction attempts will always succeed. """
            return self._data_store.get_value_by_key(SSAbductionSetting.ABDUCTION_ALWAYS_SUCCESSFUL_SWITCH)
