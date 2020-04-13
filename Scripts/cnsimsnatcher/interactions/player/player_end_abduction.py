"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any
from cnsimsnatcher.modinfo import ModInfo
from cnsimsnatcher.utils.abduction_state_utils import SSAbductionStateUtils
from sims.sim import Sim
from event_testing.results import TestResult
from interactions.context import InteractionContext
from cnsimsnatcher.enums.string_identifiers import SSStringId
from cnsimsnatcher.settings.setting_utils import SSSettingUtils
from sims4communitylib.classes.interactions.common_immediate_super_interaction import CommonImmediateSuperInteraction
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from ssutilities.commonlib.utils.common_situation_utils import CommonSituationUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.common_type_utils import CommonTypeUtils
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.utils.common_log_registry import CommonLogRegistry

log = CommonLogRegistry.get().register_log(ModInfo.get_identity(), 'ss_end_abduction')


class SSAbductionEndAbductionInteraction(CommonImmediateSuperInteraction):
    """ Handle the End Abduction interaction. """
    @classmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity(), fallback_return=TestResult.NONE)
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> TestResult:
        """ on_test """
        log.debug('Checking if sim can be released from abduction.')
        if not CommonTypeUtils.is_sim_instance(interaction_target):
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
        log.debug('Success, Target Sim can be released.')
        return TestResult.TRUE

    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity(), fallback_return=False)
    def on_started(self, interaction_sim: Sim, interaction_target: Any) -> bool:
        """ on_started """
        log.debug('Attempting to release target from abduction.')
        if not CommonTypeUtils.is_sim_instance(interaction_target):
            log.debug('Failed, Target is not a sim.')
            return False
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        if SSAbductionStateUtils.clear_abduction_data(target_sim_info):
            CommonSituationUtils.make_sim_leave(target_sim_info)
            CommonBasicNotification(
                SSStringId.SIM_RELEASED,
                SSStringId.SIM_HAS_BEEN_RELEASED_PLEASE_WAIT,
                description_tokens=(target_sim_info, )
            ).show()
            return True
        return False
