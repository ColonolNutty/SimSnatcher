"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any

from cnsimsnatcher.abduction.enums.interaction_ids import SSAbductionInteractionId
from cnsimsnatcher.abduction.settings.setting_utils import SSAbductionSettingUtils
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.sims.common_sim_interaction_utils import CommonSimInteractionUtils
from interactions.context import InteractionContext
from cnsimsnatcher.modinfo import ModInfo
from cnsimsnatcher.abduction.operations.abduction_score import SSAbductionSuccessChanceOperation
from cnsimsnatcher.abduction.utils.abduction_state_utils import SSAbductionStateUtils
from sims.sim import Sim
from event_testing.results import TestResult
from cnsimsnatcher.settings.setting_utils import SSSettingUtils
from cnsimsnatcher.abduction.utils.abduction_utils import SSAbductionUtils
from sims4communitylib.classes.interactions.common_immediate_super_interaction import CommonImmediateSuperInteraction
from sims4communitylib.utils.sims.common_sim_state_utils import CommonSimStateUtils
from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.common_type_utils import CommonTypeUtils


class SSAbductionStartAbductionInteraction(CommonImmediateSuperInteraction):
    """ Handles the Attempt To Abduct interaction. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'ssa_start_abduction'

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> TestResult:
        cls.get_log().debug('Testing to see if sim can be abducted')
        if not SSAbductionSettingUtils().interactions_are_enabled():
            cls.get_log().debug('Failed, Abduction interactions are disabled.')
            return TestResult.NONE
        if not CommonTypeUtils.is_sim_instance(interaction_target):
            cls.get_log().debug('Failed, Target is not a Sim.')
            return TestResult.NONE
        sim_info = CommonSimUtils.get_sim_info(interaction_sim)
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        if not SSSettingUtils().is_enabled_for_interactions(sim_info) or not SSSettingUtils().is_enabled_for_interactions(target_sim_info):
            cls.get_log().debug('Failed, Active Sim or Target Sim is not available for interactions.')
            return TestResult.NONE
        if not SSAbductionUtils().can_engage_in_abduction(sim_info) or not SSAbductionUtils().can_engage_in_abduction(target_sim_info):
            cls.get_log().debug('Failed, Active Sim or Target Sim cannot engage in abduction.')
            return TestResult.NONE
        if sim_info is target_sim_info:
            cls.get_log().debug('Failed, Cannot abduct self')
            return TestResult.NONE
        if not SSAbductionUtils().is_allowed_to_abduct_others(sim_info):
            cls.get_log().debug('Failed, Active Sim not allowed to abduct other sims.')
            return TestResult.NONE
        if not SSAbductionUtils().is_allowed_to_be_abducted(target_sim_info):
            cls.get_log().debug('Failed, Target Sim is not allowed to be abducted.')
            return TestResult.NONE
        if CommonSimStateUtils.is_dying(sim_info):
            cls.get_log().debug('Failed, Active Sim is dying.')
            return cls.create_test_result(False, reason='Active Sim is dying.')
        if CommonSimStateUtils.is_dying(target_sim_info):
            cls.get_log().debug('Failed, Target Sim is dying.')
            return cls.create_test_result(False, reason='Target Sim is dying.')
        if CommonHouseholdUtils.is_in_same_household(sim_info, target_sim_info):
            cls.get_log().debug('Failed, Target Sim is part of the Active Sims household.')
            return TestResult.NONE
        if SSAbductionStateUtils().has_captor(target_sim_info):
            cls.get_log().debug('Failed, Target Sim is already a hostage.')
            return TestResult.NONE
        from cnsimsnatcher.slavery.utils.slavery_state_utils import SSSlaveryStateUtils
        if SSSlaveryStateUtils().has_master(target_sim_info):
            cls.get_log().debug('Failed, Target Sim is enslaved.')
            return TestResult.NONE
        cls.get_log().debug('Success! The Sim can abduct the Target Sim.')
        return TestResult.TRUE

    # noinspection PyMissingOrEmptyDocstring
    def on_started(self, interaction_sim: Sim, interaction_target: Any) -> bool:
        if interaction_target is None or not CommonTypeUtils.is_sim_instance(interaction_target):
            self.log.debug('Failed, Target is not a Sim.')
            return False
        sim_info = CommonSimUtils.get_sim_info(interaction_sim)
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        SSAbductionSuccessChanceOperation.remove_abduction_success_statistic(sim_info)
        SSAbductionSuccessChanceOperation.remove_abduction_success_statistic(target_sim_info)
        self.log.debug('Queuing "Attempt To Abduct" interaction.')
        queue_result = CommonSimInteractionUtils.queue_interaction(
            sim_info,
            SSAbductionInteractionId.TRIGGER_ATTEMPT_TO_ABDUCT_HUMAN_DEFAULT,
            target=CommonSimUtils.get_sim_instance(interaction_target),
            skip_if_running=True
        )
        self.log.format_with_message('Done queuing interaction.', queue_result=queue_result)
        return queue_result.test_result
