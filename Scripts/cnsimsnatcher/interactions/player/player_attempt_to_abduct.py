"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any

from sims4communitylib.utils.sims.common_sim_interaction_utils import CommonSimInteractionUtils
from distributor.shared_messages import IconInfoData
from interactions.interaction_finisher import FinishingType
from cnsimsnatcher.enums.interaction_identifiers import SSInteractionId
from cnsimsnatcher.enums.statistic_identifiers import SSStatisticId
from cnsimsnatcher.enums.string_identifiers import SSStringId
from cnsimsnatcher.modinfo import ModInfo
from cnsimsnatcher.operations.abduction_score import SSAbductionSuccessChanceOperation
from sims.sim import Sim
from sims4communitylib.classes.interactions.common_social_mixer_interaction import CommonSocialMixerInteraction
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from sims4communitylib.utils.sims.common_sim_statistic_utils import CommonSimStatisticUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils

log = CommonLogRegistry.get().register_log(ModInfo.get_identity().name, 'ss_start_abduction')


class SSAbductionAttemptToAbductInteraction(CommonSocialMixerInteraction):
    """ Handles the success outcome of an attempt to abduct. """

    # noinspection PyMissingOrEmptyDocstring
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=False)
    def on_started(self, interaction_sim: Sim, interaction_target: Any) -> bool:
        log.debug('Attempting to Abduct a Sim')
        return super().on_started(interaction_sim, interaction_target)

    # noinspection PyMissingOrEmptyDocstring
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name)
    def on_performed(self, interaction_sim: Sim, interaction_target: Any):
        log.format_with_message('Running \'{}\' on_performed.'.format(self.__class__.__name__), interaction_sim=interaction_sim,
                                interaction_target=interaction_target)
        return self._finish_off_interaction(interaction_sim, interaction_target)

    # noinspection PyMissingOrEmptyDocstring
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=False)
    def on_killed(self, interaction_sim: Sim, interaction_target: Any) -> bool:
        log.format_with_message('Running \'{}\' on_killed.'.format(self.__class__.__name__), interaction_sim=interaction_sim,
                                interaction_target=interaction_target)
        return self._finish_off_interaction(interaction_sim, interaction_target)

    # noinspection PyMissingTypeHints,PyMissingOrEmptyDocstring
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, )
    def on_reset(self):
        log.format_with_message('Running \'{}\' on_reset.'.format(self.__class__.__name__))
        return False

    # noinspection PyMissingOrEmptyDocstring
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name)
    def on_cancelled(self, interaction_sim: Sim, interaction_target: Any, finishing_type: FinishingType, cancel_reason_msg: str, **kwargs):
        log.format_with_message('Running \'{}\' on_cancelled.'.format(self.__class__.__name__), interaction_sim=interaction_sim,
                                interaction_target=interaction_target, finishing_type=finishing_type,
                                cancel_reason_msg=cancel_reason_msg, kwargles=kwargs)
        return self._finish_off_interaction(interaction_sim, interaction_target)

    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=False)
    def _finish_off_interaction(self, interaction_sim: Sim, interaction_target: Any):
        log.format_with_message('Running \'{}\' _finish_off_interaction.'.format(self.__class__.__name__), interaction_sim=interaction_sim,
                                interaction_target=interaction_target)
        sim_info = CommonSimUtils.get_sim_info(interaction_sim)
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        target_sim_instance = CommonSimUtils.get_sim_instance(target_sim_info)
        success_commodity = CommonSimStatisticUtils.get_statistic_value(sim_info, SSStatisticId.SS_ABDUCTION_COMMODITY_WAS_SUCCESS)
        log.format_with_message('Checking if abduction is successful.', success_commodity=success_commodity)
        if SSAbductionSuccessChanceOperation.abduction_is_successful(sim_info):
            log.debug('Abduction was successful.')
            if CommonSimInteractionUtils.queue_interaction(
                sim_info,
                SSInteractionId.SS_ABDUCTION_ATTEMPT_TO_ABDUCT_HUMAN_SUCCESS_OUTCOME,
                target=target_sim_instance,
                must_run_next=True
            ):
                CommonBasicNotification(
                    SSStringId.ABDUCTION,
                    SSStringId.SIM_HAS_ABDUCTED_SIM,
                    description_tokens=(sim_info, target_sim_info)
                ).show(
                    icon=IconInfoData(obj_instance=sim_info),
                    secondary_icon=IconInfoData(obj_instance=target_sim_info)
                )
            return
        elif SSAbductionSuccessChanceOperation.abduction_is_failure(sim_info):
            log.debug('Attempt not successful.')
            if CommonSimInteractionUtils.queue_interaction(
                sim_info,
                SSInteractionId.SS_ABDUCTION_ATTEMPT_TO_ABDUCT_HUMAN_FAILURE_OUTCOME,
                target=target_sim_instance,
                must_run_next=True
            ):
                CommonBasicNotification(
                    SSStringId.ABDUCTION,
                    SSStringId.SIM_FAILED_TO_ABDUCT_SIM,
                    description_tokens=(sim_info, target_sim_info)
                ).show(
                    icon=IconInfoData(obj_instance=sim_info),
                    secondary_icon=IconInfoData(obj_instance=target_sim_info)
                )
            return
        log.format_with_message('No outcome was decided, where did it go?', success_commodity=success_commodity)
