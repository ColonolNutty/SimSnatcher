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
from cnsimsnatcher.utils.abduction_state_utils import SSAbductionStateUtils
from sims.sim import Sim
from sims4communitylib.classes.interactions.common_immediate_super_interaction import CommonImmediateSuperInteraction
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.common_type_utils import CommonTypeUtils

log = CommonLogRegistry.get().register_log(ModInfo.get_identity().name, 'ss_clear_abduction_data')


class SSAbductionClearDataInteraction(CommonImmediateSuperInteraction):
    """ Handle the Clear Abduction Data interaction. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=TestResult.NONE)
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> TestResult:
        log.format_with_message('Running \'{}\' on_test.'.format(cls.__name__), interaction_sim=interaction_sim, interaction_target=interaction_target, interaction_context=interaction_context, kwargles=kwargs)
        if not SSSettingUtils.interactions_are_enabled():
            log.debug('Failed, Abduction interactions are disabled.')
            return TestResult.NONE
        if interaction_target is None or not CommonTypeUtils.is_sim_instance(interaction_target):
            log.debug('Failed, Target is invalid.')
            return TestResult.NONE
        sim_info = CommonSimUtils.get_sim_info(interaction_sim)
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        if not SSSettingUtils.is_enabled_for_interactions(sim_info) or not SSSettingUtils.is_enabled_for_interactions(target_sim_info):
            log.debug("Failed, Active Sim or Target Sim are not enabled for interactions.")
            return TestResult.NONE
        log.debug('Success, showing interaction on target.')
        return TestResult.TRUE

    # noinspection PyMissingOrEmptyDocstring
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=False)
    def on_started(self, interaction_sim: Sim, interaction_target: Any) -> bool:
        log.format_with_message('Running \'{}\' on_started.'.format(self.__class__.__name__), interaction_sim=interaction_sim, interaction_target=interaction_target)
        if interaction_target is None or not CommonTypeUtils.is_sim_instance(interaction_target):
            log.debug('Failed, no Target or they were not a Sim.')
            return False
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        log.format_with_message('Attempting to clear abduction data from Sim.', sim=CommonSimNameUtils.get_full_name(target_sim_info))
        return SSAbductionStateUtils.clear_abduction_data(target_sim_info)
