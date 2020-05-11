"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any

from cnsimsnatcher.settings.setting_utils import SSSettingUtils
from event_testing.results import TestResult
from interactions.context import InteractionContext
from cnsimsnatcher.modinfo import ModInfo
from sims.sim import Sim
from sims4communitylib.classes.interactions.common_terrain_interaction import CommonTerrainInteraction
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.common_type_utils import CommonTypeUtils


class SSOpenSettingsInteraction(CommonTerrainInteraction):
    """ Handle the interaction to Open Settings. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'ss_open_settings'

    def __init__(self, *_, **__) -> None:
        super().__init__(*_, **__)
        from cnsimsnatcher.settings.dialog import SSSettingsDialog
        self._settings_dialog = SSSettingsDialog()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> TestResult:
        cls.get_log().format_with_message('Running \'{}\' on_test.'.format(cls.__name__), interaction_sim=interaction_sim, interaction_target=interaction_target, interaction_context=interaction_context, kwargles=kwargs)
        if interaction_target is None or not CommonTypeUtils.is_sim_instance(interaction_target):
            cls.get_log().debug('Failed, Target is not a Sim.')
            return TestResult.NONE
        sim_info = CommonSimUtils.get_sim_info(interaction_sim)
        if not SSSettingUtils().is_enabled_for_interactions(sim_info):
            cls.get_log().debug('Failed, \'{}\' not enabled for interactions.'.format(CommonSimNameUtils.get_full_name(sim_info)))
            return TestResult.NONE
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        if not SSSettingUtils().is_enabled_for_interactions(target_sim_info):
            cls.get_log().debug('Failed, \'{}\' not enabled for interactions.'.format(CommonSimNameUtils.get_full_name(target_sim_info)))
            return TestResult.NONE
        cls.get_log().debug('Success, can open SS settings.')
        return TestResult.TRUE

    # noinspection PyMissingOrEmptyDocstring
    def on_started(self, interaction_sim: Sim, interaction_target: Any) -> bool:
        self.log.format_with_message('Running \'{}\' on_started.'.format(self), interaction_sim=interaction_sim, interaction_target=interaction_target)
        self._settings_dialog.open()
        return True
