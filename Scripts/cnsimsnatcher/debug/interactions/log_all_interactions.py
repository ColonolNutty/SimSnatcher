"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from pprint import pformat
from typing import Any
from event_testing.results import TestResult
from interactions.context import InteractionContext
from cnsimsnatcher.modinfo import ModInfo
from cnsimsnatcher.settings.setting_utils import SSSettingUtils
from sims.sim import Sim
from sims4communitylib.classes.interactions.common_immediate_super_interaction import CommonImmediateSuperInteraction
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.objects.common_object_interaction_utils import CommonObjectInteractionUtils
from sims4communitylib.utils.resources.common_interaction_utils import CommonInteractionUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class SSDebugLogAllInteractionsInteraction(CommonImmediateSuperInteraction):
    """ Log All Interactions of an object. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'ss_log_all_interactions'

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> TestResult:
        cls.get_log().format_with_message('Running \'{}\' on_test.'.format(cls.__name__), interaction_sim=interaction_sim, interaction_target=interaction_target, interaction_context=interaction_context, kwargles=kwargs)
        sim_info = CommonSimUtils.get_sim_info(interaction_sim)
        if not SSSettingUtils().is_enabled_for_interactions(sim_info):
            cls.get_log().debug('Failed, Active Sim or Target Sim are not enabled for abduction.')
            return TestResult.NONE
        if interaction_target is None:
            cls.get_log().debug('Failed, No target found.')
            return TestResult.NONE
        cls.get_log().debug('Success, can show Log All Interactions interaction.')
        return TestResult.TRUE

    # noinspection PyMissingOrEmptyDocstring
    def on_started(self, interaction_sim: Sim, interaction_target: Any) -> bool:
        self.log.format_with_message('Running \'{}\' on_started.'.format(self.__class__.__name__), interaction_sim=interaction_sim, interaction_target=interaction_target)
        interactions = CommonObjectInteractionUtils.get_all_interactions_registered_to_object_gen(interaction_target)
        self.log.debug('printing names')
        for interaction in interactions:
            try:
                self.log.format(
                    interaction=interaction,
                    interaction_name=CommonInteractionUtils.get_interaction_display_name(interaction),
                    interaction_short_name=CommonInteractionUtils.get_interaction_short_name(interaction),
                    interaction_display_name_string_id=interaction.display_name._string_id
                )
            except Exception as ex:
                self.log.error('problem with interaction {}'.format(pformat(interaction)), exception=ex)
                continue
        self.log.debug('Done.')
        self.log.disable()
        return True
