"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Dict

from cnsimsnatcher.abduction.settings.settings import SSAbductionSetting
from sims4communitylib.persistence.data_stores.common_data_store import CommonDataStore


class SSAbductionSettingsDataStore(CommonDataStore):
    """ Manages abduction settings for SS. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_identifier(cls) -> str:
        return 'ss_abduction_settings'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def _version(self) -> int:
        return 1

    # noinspection PyMissingOrEmptyDocstring
    @property
    def _default_data(self) -> Dict[str, Any]:
        return {
            SSAbductionSetting.VERSION: self._version,

            # Main
            SSAbductionSetting.ABDUCTION_INTERACTIONS_SWITCH: True,

            SSAbductionSetting.ATTEMPT_TO_ABDUCT_SUCCESS_CHANCE: 50.0,

            # Cheats
            SSAbductionSetting.ATTEMPT_TO_ABDUCT_ALWAYS_SUCCESSFUL: False
        }.copy()
