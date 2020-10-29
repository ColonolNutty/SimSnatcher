"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any

from cnsimsnatcher.bindings.dialog.configure_bindings_dialog import SSConfigureBindingsDialog
from cnsimsnatcher.persistence.ss_sim_data_storage import SSSimData
from cnsimsnatcher.settings.setting_utils import SSSettingUtils
from cnsimsnatcher.slavery.settings.setting_utils import SSSlaverySettingUtils
from event_testing.results import TestResult
from interactions.context import InteractionContext
from cnsimsnatcher.modinfo import ModInfo
from sims.sim import Sim
from sims4communitylib.classes.interactions.common_immediate_super_interaction import CommonImmediateSuperInteraction
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.common_type_utils import CommonTypeUtils


class SSBindingConfigureBindingsInteraction(CommonImmediateSuperInteraction):
    """ Handle the interaction. """
    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'ssb_configure_bindings'

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> TestResult:
        cls.get_log().format_with_message('Running \'{}\' on_test.'.format(cls.__name__), interaction_sim=interaction_sim, interaction_target=interaction_target, interaction_context=interaction_context, kwargles=kwargs)
        if not SSSlaverySettingUtils().interactions_are_enabled():
            cls.get_log().debug('Failed, Slavery interactions are disabled.')
            return TestResult.NONE
        if interaction_target is None or not CommonTypeUtils.is_sim_instance(interaction_target):
            cls.get_log().debug('Failed, Target is invalid.')
            return TestResult.NONE
        sim_info = CommonSimUtils.get_sim_info(interaction_sim)
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        if not SSSettingUtils().is_enabled_for_interactions(sim_info) or not SSSettingUtils().is_enabled_for_interactions(target_sim_info):
            cls.get_log().debug('Failed, Active Sim or Target Sim are not enabled for interactions.')
            return TestResult.NONE
        target_sim_data = SSSimData(target_sim_info)
        if not target_sim_data.is_slave_or_captive:
            cls.get_log().debug('Failed, Target Sim is not captured.')
            return TestResult.NONE
        cls.get_log().debug('Success, showing {} interaction on Target.'.format(cls.__name__))
        return TestResult.TRUE

    # noinspection PyMissingOrEmptyDocstring
    def on_started(self, interaction_sim: Sim, interaction_target: Sim) -> bool:
        self.log.format_with_message('Running \'{}\' on_started.'.format(self.__class__.__name__), interaction_sim=interaction_sim, interaction_target=interaction_target)
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        SSConfigureBindingsDialog(target_sim_info).open()
        return True
