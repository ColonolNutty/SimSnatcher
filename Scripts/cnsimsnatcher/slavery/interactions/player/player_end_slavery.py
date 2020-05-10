"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any
from cnsimsnatcher.modinfo import ModInfo
from cnsimsnatcher.slavery.utils.slavery_state_utils import SSSlaveryStateUtils
from sims.sim import Sim
from event_testing.results import TestResult
from interactions.context import InteractionContext
from cnsimsnatcher.enums.string_ids import SSStringId
from cnsimsnatcher.settings.setting_utils import SSSettingUtils
from sims4communitylib.classes.interactions.common_immediate_super_interaction import CommonImmediateSuperInteraction
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.common_type_utils import CommonTypeUtils


class SSSlaveryEndSlaveryInteraction(CommonImmediateSuperInteraction):
    """ Handle the End Slavery interaction. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'ss_end_slavery'

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> TestResult:
        cls.get_log().debug('Checking if sim can be released from slavery.')
        if not CommonTypeUtils.is_sim_instance(interaction_target):
            cls.get_log().debug('Failed, Target is not a Sim.')
            return TestResult.NONE
        sim_info = CommonSimUtils.get_sim_info(interaction_sim)
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        if sim_info is target_sim_info:
            cls.get_log().debug('Failed, Active Sim and Target Sim are the same.')
            return TestResult.NONE
        if not SSSettingUtils().is_enabled_for_interactions(sim_info) or not SSSettingUtils().is_enabled_for_interactions(target_sim_info):
            cls.get_log().debug('Failed, Active Sim or Target Sim are not enabled for interactions.')
            return TestResult.NONE
        if not SSSlaveryStateUtils().is_slave_of(target_sim_info, sim_info):
            cls.get_log().debug('Failed, Target Sim has not been enslaved.')
            return TestResult.NONE
        cls.get_log().debug('Success, Target Sim can be released.')
        return TestResult.TRUE

    # noinspection PyMissingOrEmptyDocstring
    def on_started(self, interaction_sim: Sim, interaction_target: Any) -> bool:
        self.log.debug('Attempting to release target from slavery.')
        if not CommonTypeUtils.is_sim_instance(interaction_target):
            self.log.debug('Failed, Target is not a sim.')
            return False
        source_sim_info = CommonSimUtils.get_sim_info(interaction_sim)
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        if SSSlaveryStateUtils().release_slave(target_sim_info, releasing_sim_info=source_sim_info):
            self.log.debug('Sim released.')
            CommonBasicNotification(
                SSStringId.SIM_RELEASED,
                SSStringId.SIM_HAS_BEEN_RELEASED_PLEASE_WAIT,
                description_tokens=(target_sim_info, )
            ).show()
            return True
        self.log.debug('Done ending slavery.')
        return False
