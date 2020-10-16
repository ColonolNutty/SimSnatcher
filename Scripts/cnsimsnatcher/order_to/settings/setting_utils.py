"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from cnsimsnatcher.order_to.settings.data.data_store import SSOrderToSettingsDataStore
from sims4communitylib.services.common_service import CommonService


class SSOrderToSettingUtils(CommonService):
    """ Utilities to get SS Order To settings. """
    def __init__(self) -> None:
        super().__init__()
        from cnsimsnatcher.persistence.ss_data_manager_utils import SSDataManagerUtils
        self._data_store = SSDataManagerUtils().get_order_to_mod_settings_data_store()
        self.cheats = SSOrderToSettingUtils.Cheats(self._data_store)

    def disclaimer_has_been_shown(self) -> bool:
        """ Determine if the disclaimer has been shown already. """
        from cnsimsnatcher.order_to.settings.settings import SSOrderToSetting
        return self._data_store.get_value_by_key(SSOrderToSetting.ORDER_TO_DISCLAIMER_SHOWN)

    def flag_disclaimer_as_shown(self) -> None:
        """ Flag the disclaimer as shown already so it no longer shows. """
        from cnsimsnatcher.order_to.settings.settings import SSOrderToSetting
        self._data_store.set_value_by_key(SSOrderToSetting.ORDER_TO_DISCLAIMER_SHOWN, True)

    class Cheats(CommonService):
        """ Cheat settings. """
        def __init__(self, data_store: SSOrderToSettingsDataStore) -> None:
            super().__init__()
            self._data_store = data_store

        def should_show_debug_interactions_for_perform_interaction(self) -> bool:
            """ Determine if debug interactions should be filtered out of the Perform Interaction order. """
            from cnsimsnatcher.order_to.settings.settings import SSOrderToSetting
            return self._data_store.get_value_by_key(SSOrderToSetting.SHOW_DEBUG_INTERACTIONS_FOR_PERFORM_INTERACTION_ORDER)
