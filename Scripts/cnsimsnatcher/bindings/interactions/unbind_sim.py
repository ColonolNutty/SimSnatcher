"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any
from cnsimsnatcher.bindings.enums.interaction_identifiers import SSBindingInteractionId
from cnsimsnatcher.settings.setting_utils import SSSettingUtils
from event_testing.results import TestResult
from interactions.base.interaction import Interaction
from interactions.context import InteractionContext
from cnsimsnatcher.modinfo import ModInfo
from sims.sim import Sim
from sims4communitylib.classes.interactions.common_immediate_super_interaction import CommonImmediateSuperInteraction
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.resources.common_interaction_utils import CommonInteractionUtils
from sims4communitylib.utils.sims.common_sim_interaction_utils import CommonSimInteractionUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.common_type_utils import CommonTypeUtils


class SSBindingsUnbindSimInteraction(CommonImmediateSuperInteraction):
    """ Handle the interaction. """
    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'ssb_unbind_sim'

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> TestResult:
        cls.get_log().format_with_message('Running \'{}\' on_test.'.format(cls.__name__), interaction_sim=interaction_sim, interaction_target=interaction_target, interaction_context=interaction_context, kwargles=kwargs)
        if interaction_target is None or not CommonTypeUtils.is_sim_or_sim_info(interaction_target):
            return TestResult.NONE
        sim_info = CommonSimUtils.get_sim_info(interaction_sim)
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        if not SSSettingUtils().is_enabled_for_interactions(sim_info) or not SSSettingUtils().is_enabled_for_interactions(target_sim_info):
            return TestResult.NONE
        if not CommonSimInteractionUtils.has_interaction_running_or_queued(target_sim_info, SSBindingInteractionId.BOUND):
            cls.get_log().debug('Failed, Target Sim is not bound.')
            return TestResult.NONE
        return TestResult.TRUE

    # noinspection PyMissingOrEmptyDocstring
    def on_started(self, interaction_sim: Sim, interaction_target: Sim) -> bool:
        self.log.format_with_message('Running \'{}\' on_started.'.format(self.__class__.__name__), interaction_sim=interaction_sim, interaction_target=interaction_target)
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)

        def _is_interaction(_interaction: Interaction):
            return CommonInteractionUtils.get_interaction_id(_interaction) == SSBindingInteractionId.BOUND

        CommonSimInteractionUtils.cancel_all_queued_or_running_interactions(target_sim_info, cancel_reason='Unbinding Sim', include_interaction_callback=_is_interaction)
        return True
