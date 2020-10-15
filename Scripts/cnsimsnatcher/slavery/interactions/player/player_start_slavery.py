"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any

from cnsimsnatcher.slavery.enums.interaction_ids import SSSlaveryInteractionId
from cnsimsnatcher.slavery.operations.enslave_score import SSEnslaveAttemptSuccessChanceOperation
from cnsimsnatcher.slavery.settings.setting_utils import SSSlaverySettingUtils
from cnsimsnatcher.slavery.utils.slavery_state_utils import SSSlaveryStateUtils
from cnsimsnatcher.slavery.utils.slavery_utils import SSSlaveryUtils
from cnsimsnatcher.abduction.utils.abduction_state_utils import SSAbductionStateUtils
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.sims.common_sim_interaction_utils import CommonSimInteractionUtils
from interactions.context import InteractionContext
from cnsimsnatcher.modinfo import ModInfo
from sims.sim import Sim
from event_testing.results import TestResult
from cnsimsnatcher.settings.setting_utils import SSSettingUtils
from sims4communitylib.classes.interactions.common_immediate_super_interaction import CommonImmediateSuperInteraction
from sims4communitylib.utils.sims.common_sim_state_utils import CommonSimStateUtils
from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.common_type_utils import CommonTypeUtils


class SSSlaveryStartSlaveryInteraction(CommonImmediateSuperInteraction):
    """ Handles the Attempt To Enslave interaction. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'ss_start_slavery'

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> TestResult:
        cls.get_log().debug('Testing to see if sim can be abducted')
        if not SSSlaverySettingUtils().interactions_are_enabled():
            cls.get_log().debug('Failed, Slavery interactions are disabled.')
            return TestResult.NONE
        if not CommonTypeUtils.is_sim_instance(interaction_target):
            cls.get_log().debug('Failed, Target is not a Sim.')
            return TestResult.NONE
        sim_info = CommonSimUtils.get_sim_info(interaction_sim)
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        if not SSSettingUtils().is_enabled_for_interactions(sim_info) or not SSSettingUtils().is_enabled_for_interactions(target_sim_info):
            cls.get_log().debug('Failed, Active Sim or Target Sim is not available for interactions.')
            return TestResult.NONE
        if not SSSlaveryUtils().can_engage_in_slavery(sim_info) or not SSSlaveryUtils().can_engage_in_slavery(target_sim_info):
            cls.get_log().debug('Failed, Active Sim or Target Sim cannot engage in slavery.')
            return TestResult.NONE
        if sim_info is target_sim_info:
            cls.get_log().debug('Failed, Cannot enslave self')
            return TestResult.NONE
        if not SSSlaveryUtils().is_allowed_to_enslave_others(sim_info):
            cls.get_log().debug('Failed, Active Sim not allowed to enslave other sims.')
            return TestResult.NONE
        if not SSSlaveryUtils().is_allowed_to_be_enslaved(target_sim_info):
            cls.get_log().debug('Failed, Target Sim is not allowed to be enslaved.')
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
        if SSSlaveryStateUtils().has_masters(target_sim_info):
            cls.get_log().debug('Failed, Target Sim already has masters.')
            return TestResult.NONE
        if not SSAbductionStateUtils().has_captors(target_sim_info):
            cls.get_log().debug('Failed, Target Sim must already have been abducted to be enslaved.')
            return TestResult.NONE
        cls.get_log().debug('Success! The Sim can enslave the Target Sim.')
        return TestResult.TRUE

    # noinspection PyMissingOrEmptyDocstring
    def on_started(self, interaction_sim: Sim, interaction_target: Any) -> bool:
        if interaction_target is None or not CommonTypeUtils.is_sim_instance(interaction_target):
            self.log.debug('Failed, Target is not a Sim.')
            return False
        interaction_target: Sim = interaction_target
        sim_info = CommonSimUtils.get_sim_info(interaction_sim)
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        SSEnslaveAttemptSuccessChanceOperation.remove_attempt_success_statistic(sim_info)
        SSEnslaveAttemptSuccessChanceOperation.remove_attempt_success_statistic(target_sim_info)
        self.log.debug('Queuing "Attempt To Enslave" interaction.')
        queue_result = CommonSimInteractionUtils.queue_interaction(
            sim_info,
            SSSlaveryInteractionId.TRIGGER_ATTEMPT_TO_ENSLAVE_HUMAN,
            target=interaction_target,
            skip_if_running=True
        )
        self.log.format_with_message('Done queuing interaction.', queue_result=queue_result)
        return queue_result.test_result
