"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any
from event_testing.results import TestResult
from interactions.context import InteractionContext
from cnsimsnatcher.modinfo import ModInfo
from cnsimsnatcher.operations.order_operations import SSAbductionDemandOperations
from cnsimsnatcher.settings.setting_utils import SSSettingUtils
from cnsimsnatcher.utils.abduction_state_utils import SSAbductionStateUtils
from sims.sim import Sim
from sims4communitylib.classes.interactions.common_super_interaction import CommonSuperInteraction
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.sims.common_sim_location_utils import CommonSimLocationUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.common_type_utils import CommonTypeUtils

log = CommonLogRegistry.get().register_log(ModInfo.get_identity().name, 'ss_order_to_go_to_residence')


class SSOrderToGoToResidenceInteraction(CommonSuperInteraction):
    """ Handles the Order To... Go To Residence interaction. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=TestResult.NONE)
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> TestResult:
        log.debug('Checking if Sim can be demanded to go to residence.')
        if interaction_target is None or not CommonTypeUtils.is_sim_instance(interaction_target):
            log.debug('Failed, Target is not a Sim.')
            return TestResult.NONE
        sim_info = CommonSimUtils.get_sim_info(interaction_sim)
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        if sim_info is target_sim_info:
            log.debug('Failed, Active Sim and Target Sim are the same.')
            return TestResult.NONE
        if not SSSettingUtils.is_enabled_for_interactions(sim_info) or not SSSettingUtils.is_enabled_for_interactions(target_sim_info):
            log.debug('Failed, Active Sim or Target Sim are not enabled for interactions.')
            return TestResult.NONE
        if not SSAbductionStateUtils.has_been_abducted(target_sim_info):
            log.debug('Failed, Target Sim has not been abducted.')
            return TestResult.NONE
        if CommonSimLocationUtils.is_at_home(sim_info):
            return TestResult.NONE
        log.debug('Success, Target Sim can be ordered around.')
        return TestResult.TRUE

    # noinspection PyUnusedLocal,PyMissingOrEmptyDocstring
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=False)
    def on_run(self, interaction_sim: Sim, interaction_target: Any, timeline):
        log.debug('Running go to residence interaction')
        sim_info = CommonSimUtils.get_sim_info(interaction_sim)
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        return SSAbductionDemandOperations.demand_sim_go_to_home_lot(sim_info, target_sim_info)
