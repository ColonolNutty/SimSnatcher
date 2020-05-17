"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from interactions.context import InteractionContext
from cnsimsnatcher.modinfo import ModInfo
from sims.sim import Sim
from event_testing.results import TestResult
from cnsimsnatcher.settings.setting_utils import SSSettingUtils
from sims4communitylib.classes.interactions.common_immediate_super_interaction import CommonImmediateSuperInteraction
from sims4communitylib.utils.sims.common_sim_state_utils import CommonSimStateUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.common_type_utils import CommonTypeUtils


class SSConfigureCaptiveSlaveInteraction(CommonImmediateSuperInteraction):
    """ Handles the Configure Captive/Slave interaction. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'ss_configure_captive_slave'

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> TestResult:
        from cnsimsnatcher.slavery.utils.slavery_state_utils import SSSlaveryStateUtils
        from cnsimsnatcher.abduction.utils.abduction_state_utils import SSAbductionStateUtils
        cls.get_log().debug('Testing to see if Sim can be configured.')
        if interaction_target is None or not CommonTypeUtils.is_sim_instance(interaction_target):
            cls.get_log().debug('Failed, Target is not a Sim.')
            return TestResult.NONE
        sim_info = CommonSimUtils.get_sim_info(interaction_sim)
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        if sim_info is target_sim_info:
            cls.get_log().debug('Failed, Cannot abduct self')
            return TestResult.NONE
        if not SSSettingUtils().is_enabled_for_interactions(sim_info) or not SSSettingUtils().is_enabled_for_interactions(target_sim_info):
            cls.get_log().debug('Failed, Source Sim or Target Sim is not available for interactions.')
            return TestResult.NONE
        if not SSAbductionStateUtils().has_captors(target_sim_info) and not SSSlaveryStateUtils().has_masters(target_sim_info):
            cls.get_log().debug('Failed, Target Sim is not a Captive or a Slave.')
            return TestResult.NONE
        if not SSAbductionStateUtils().is_captor_of(sim_info, target_sim_info) and not SSSlaveryStateUtils().is_master_of(sim_info, target_sim_info):
            cls.get_log().debug('Failed, Target Sim is not a Captive or a Slave of Source Sim.')
            return TestResult.NONE
        if CommonSimStateUtils.is_dying(sim_info):
            cls.get_log().debug('Failed, Source Sim is dying.')
            return cls.create_test_result(False, reason='Source Sim is dying.')
        if CommonSimStateUtils.is_dying(target_sim_info):
            cls.get_log().debug('Failed, Target Sim is dying.')
            return cls.create_test_result(False, reason='Target Sim is dying.')
        cls.get_log().debug('Success! The Sim can configure the Target Sim.')
        return TestResult.TRUE

    # noinspection PyMissingOrEmptyDocstring
    def on_started(self, interaction_sim: Sim, interaction_target: Any) -> bool:
        from cnsimsnatcher.slavery.utils.slavery_state_utils import SSSlaveryStateUtils
        from cnsimsnatcher.abduction.utils.abduction_state_utils import SSAbductionStateUtils
        if interaction_target is None or not CommonTypeUtils.is_sim_instance(interaction_target):
            self.log.debug('Failed, Target is not a Sim.')
            return False
        sim_info = CommonSimUtils.get_sim_info(interaction_sim)
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        if SSSlaveryStateUtils().is_master_of(sim_info, target_sim_info):
            pass
        if SSAbductionStateUtils().is_captor_of(sim_info, target_sim_info):
            pass
        return True
