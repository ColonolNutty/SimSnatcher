"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Dict

from cnsimsnatcher.slavery.settings.settings import SSSlaverySetting
from sims4communitylib.persistence.data_stores.common_data_store import CommonDataStore


class SSSlaverySettingsDataStore(CommonDataStore):
    """ Manages Slavery settings for SS. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_identifier(cls) -> str:
        return 'ss_slavery_settings'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def _version(self) -> int:
        return 1

    # noinspection PyMissingOrEmptyDocstring
    @property
    def _default_data(self) -> Dict[str, Any]:
        return {
            SSSlaverySetting.VERSION: self._version,

            # General
            SSSlaverySetting.SLAVERY_INTERACTIONS_SWITCH: False
        }.copy()
