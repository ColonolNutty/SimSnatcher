"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any

from cnsimsnatcher.configuration.allowance.dialogs.allowance_config_dialog import SSAllowanceConfigDialog
from cnsimsnatcher.persistence.ss_sim_data import SSSimData
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


class SSConfigureAllowancesInteraction(CommonImmediateSuperInteraction):
    """ Handles the interaction. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'ss_configure_allowances'

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> TestResult:
        cls.get_log().format_with_message('Running \'{}\' on_test.'.format(cls.__name__), interaction_sim=interaction_sim, interaction_target=interaction_target, interaction_context=interaction_context)
        if interaction_target is None or not CommonTypeUtils.is_sim_instance(interaction_target):
            cls.get_log().debug('Failed, Target is not a Sim.')
            return TestResult.NONE
        sim_info = CommonSimUtils.get_sim_info(interaction_sim)
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        if not SSSettingUtils().is_enabled_for_interactions(sim_info):
            cls.get_log().debug('Failed, Active Sim or Target Sim is not available for interactions.')
            return TestResult.NONE
        if not SSSettingUtils().is_enabled_for_interactions(sim_info) or not SSSettingUtils().is_enabled_for_interactions(target_sim_info):
            cls.get_log().debug('Failed, Active Sim or Target Sim are not enabled for interactions.')
            return TestResult.NONE
        if CommonSimStateUtils.is_dying(sim_info):
            cls.get_log().debug('Failed, Active Sim is dying.')
            return cls.create_test_result(False, reason='Active Sim is dying.')
        if CommonSimStateUtils.is_dying(target_sim_info):
            cls.get_log().debug('Failed, Target Sim is dying.')
            return cls.create_test_result(False, reason='Target Sim is dying.')
        target_sim_data = SSSimData(target_sim_info)
        if not target_sim_data.is_slave_or_captive:
            cls.get_log().debug('Failed, Target Sim is not a Captive or Slave.')
            return TestResult.NONE
        cls.get_log().debug('Success! The Sim can enslave the Target Sim.')
        return TestResult.TRUE

    # noinspection PyMissingOrEmptyDocstring
    def on_started(self, interaction_sim: Sim, interaction_target: Sim) -> bool:
        self.log.format_with_message('Running \'{}\' on_started.'.format(self.__class__.__name__), interaction_sim=interaction_sim, interaction_target=interaction_target)
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        SSAllowanceConfigDialog().open(target_sim_info)
        return True
