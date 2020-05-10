"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any

from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.sims.common_sim_interaction_utils import CommonSimInteractionUtils
from distributor.shared_messages import IconInfoData
from interactions.interaction_finisher import FinishingType
from cnsimsnatcher.enums.interaction_ids import SSInteractionId
from cnsimsnatcher.enums.statistic_ids import SSStatisticId
from cnsimsnatcher.enums.string_ids import SSStringId
from cnsimsnatcher.modinfo import ModInfo
from cnsimsnatcher.operations.abduction_score import SSAbductionSuccessChanceOperation
from sims.sim import Sim
from sims4communitylib.classes.interactions.common_social_mixer_interaction import CommonSocialMixerInteraction
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from sims4communitylib.utils.sims.common_sim_statistic_utils import CommonSimStatisticUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class SSAbductionAttemptToAbductInteraction(CommonSocialMixerInteraction):
    """ Handles the success outcome of an attempt to abduct. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'ss_start_abduction'

    # noinspection PyMissingOrEmptyDocstring
    def on_started(self, interaction_sim: Sim, interaction_target: Any) -> bool:
        self.log.debug('Attempting to Abduct a Sim')
        return super().on_started(interaction_sim, interaction_target)

    # noinspection PyMissingOrEmptyDocstring
    def on_performed(self, interaction_sim: Sim, interaction_target: Any):
        self.log.format_with_message('Running \'{}\' on_performed.'.format(self.__class__.__name__), interaction_sim=interaction_sim, interaction_target=interaction_target)
        return self._finish_off_interaction(interaction_sim, interaction_target)

    # noinspection PyMissingOrEmptyDocstring
    def on_killed(self, interaction_sim: Sim, interaction_target: Any) -> bool:
        self.log.format_with_message('Running \'{}\' on_killed.'.format(self.__class__.__name__), interaction_sim=interaction_sim, interaction_target=interaction_target)
        return self._finish_off_interaction(interaction_sim, interaction_target)

    # noinspection PyMissingTypeHints,PyMissingOrEmptyDocstring
    def on_reset(self):
        self.log.format_with_message('Running \'{}\' on_reset.'.format(self.__class__.__name__))
        return False

    # noinspection PyMissingOrEmptyDocstring
    def on_cancelled(self, interaction_sim: Sim, interaction_target: Any, finishing_type: FinishingType, cancel_reason_msg: str, **kwargs):
        self.log.format_with_message('Running \'{}\' on_cancelled.'.format(self.__class__.__name__), interaction_sim=interaction_sim, interaction_target=interaction_target, finishing_type=finishing_type, cancel_reason_msg=cancel_reason_msg, kwargles=kwargs)
        return self._finish_off_interaction(interaction_sim, interaction_target)

    def _finish_off_interaction(self, interaction_sim: Sim, interaction_target: Any) -> bool:
        self.log.format_with_message('Running \'{}\' _finish_off_interaction.'.format(self.__class__.__name__), interaction_sim=interaction_sim, interaction_target=interaction_target)
        sim_info = CommonSimUtils.get_sim_info(interaction_sim)
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        target_sim_instance = CommonSimUtils.get_sim_instance(target_sim_info)
        success_commodity = CommonSimStatisticUtils.get_statistic_value(sim_info, SSStatisticId.SS_ABDUCTION_COMMODITY_WAS_SUCCESS)
        self.log.format_with_message('Checking if abduction is successful.', success_commodity=success_commodity)
        if SSAbductionSuccessChanceOperation.abduction_is_successful(sim_info):
            self.log.debug('Abduction was successful.')
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
            return True
        elif SSAbductionSuccessChanceOperation.abduction_is_failure(sim_info):
            self.log.debug('Attempt not successful.')
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
            return True
        self.log.format_with_message('No outcome was decided, where did it go?', success_commodity=success_commodity)
        return False
