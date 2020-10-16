"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Dict

from cnsimsnatcher.order_to.settings.settings import SSOrderToSetting
from sims4communitylib.persistence.data_stores.common_data_store import CommonDataStore


class SSOrderToSettingsDataStore(CommonDataStore):
    """ Manages Order To settings for SS. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_identifier(cls) -> str:
        return 'ss_order_to_settings'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def _version(self) -> int:
        return 1

    # noinspection PyMissingOrEmptyDocstring
    @property
    def _default_data(self) -> Dict[str, Any]:
        return {
            SSOrderToSetting.VERSION: self._version,

            # Main
            SSOrderToSetting.ORDER_TO_DISCLAIMER_SHOWN: False,

            # Cheats
            SSOrderToSetting.SHOW_DEBUG_INTERACTIONS_FOR_PERFORM_INTERACTION_ORDER: False
        }.copy()
