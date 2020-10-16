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
from cnsimsnatcher.slavery.utils.slavery_state_utils import SSSlaveryStateUtils
from cnsimsnatcher.abduction.utils.abduction_state_utils import SSAbductionStateUtils
from cnsimsnatcher.slavery.refresh._summon_enslaved_sims import _SSSlaverySummonSlaves
from cnsimsnatcher.abduction.refresh._summon_abducted_sims import _SSAbductionSummonCaptives


class SSSummonCaptivesAndSlavesInteraction(CommonImmediateSuperInteraction):
    """ Handles the interaction. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'ss_summon_captives_and_slaves'

    def __init__(self, *_, **__) -> None:
        super().__init__(*_, **__)
        self._slavery_state_utils = SSSlaveryStateUtils()
        self._abduction_state_utils = SSAbductionStateUtils()

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
        if CommonSimStateUtils.is_dying(sim_info):
            cls.get_log().debug('Failed, Active Sim is dying.')
            return cls.create_test_result(False, reason='Active Sim is dying.')
        if not SSSlaveryStateUtils().has_slaves(target_sim_info, instanced_only=False) and not SSAbductionStateUtils().has_captives(target_sim_info, instanced_only=False):
            cls.get_log().debug('Failed, Target Sim has no Captives or Slaves.')
            return TestResult.NONE
        cls.get_log().debug('Success, can summon the captives and slaves of the Target.')
        return TestResult.TRUE

    # noinspection PyMissingOrEmptyDocstring
    def on_started(self, interaction_sim: Sim, interaction_target: Sim) -> bool:
        self.log.format_with_message('Running \'{}\' on_started.'.format(self.__class__.__name__), interaction_sim=interaction_sim, interaction_target=interaction_target)
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        if self._slavery_state_utils.has_slaves(target_sim_info, instanced_only=False):
            _SSSlaverySummonSlaves()._summon_slaves_for(target_sim_info)
        if self._abduction_state_utils.has_captives(target_sim_info, instanced_only=False):
            _SSAbductionSummonCaptives()._summon_captives_for(target_sim_info)
        return True
